#!/usr/bin/env python3
"""Ecosystem learning runtime with FastAPI, ChromaDB, Neo4j, and LangChain."""

from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import os
from typing import Any, Callable

import chromadb
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from langchain_core.prompts import ChatPromptTemplate
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError
from pydantic import BaseModel, Field


@dataclass
class RuntimeState:
    chroma_client: Any | None = None
    collection: Any | None = None
    neo4j_driver: Any | None = None
    prompt: ChatPromptTemplate = field(
        default_factory=lambda: ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an ecosystem learning planner. Return concise and practical guidance.",
                ),
                (
                    "human",
                    "Topic: {topic}\nGoal: {goal}\nPrior context: {context}",
                ),
            ]
        )
    )


state = RuntimeState()
security = HTTPBearer(auto_error=False)

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
AUTH_ENABLED = os.getenv("AUTH_ENABLED", "true").lower() == "true"

ROLE_PERMISSIONS: dict[str, list[str]] = {
    "memory.upsert": ["admin", "operator", "researcher", "professor"],
    "memory.query": ["admin", "operator", "researcher", "professor", "student"],
    "graph.ping": ["admin", "operator", "researcher"],
    "learn.compose": ["admin", "operator", "researcher", "professor", "student"],
}


def _parse_jwt_secrets() -> list[str]:
    secrets_from_list = os.getenv("JWT_SECRETS", "")
    parsed = [item.strip() for item in secrets_from_list.split(",") if item.strip()]
    if parsed:
        return parsed

    return [os.getenv("JWT_SECRET", "liceu-academia-secret")]


JWT_SECRETS = _parse_jwt_secrets()


class MemoryUpsertPayload(BaseModel):
    memory_id: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class MemoryQueryPayload(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=3, ge=1, le=20)


class LearningComposePayload(BaseModel):
    topic: str = Field(..., min_length=1)
    goal: str = Field(..., min_length=1)
    context: str = "none"


class TokenRequestPayload(BaseModel):
    subject: str = Field(..., min_length=1)
    role: str = "academy-runtime"
    expires_minutes: int = Field(default=120, ge=1, le=1440)


def create_access_token(subject: str, role: str, expires_minutes: int = 120) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {
        "sub": subject,
        "role": role,
        "exp": int(expiration.timestamp()),
    }
    return jwt.encode(payload, JWT_SECRETS[0], algorithm=JWT_ALGORITHM)


async def require_auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict[str, Any]:
    if not AUTH_ENABLED:
        return {"sub": "anonymous", "role": "admin"}

    if credentials is None:
        raise HTTPException(status_code=401, detail="missing bearer token")

    for secret in JWT_SECRETS:
        try:
            claims: dict[str, Any] = jwt.decode(
                credentials.credentials,
                secret,
                algorithms=[JWT_ALGORITHM],
            )
            return claims
        except JWTError:
            continue

    raise HTTPException(status_code=401, detail="invalid bearer token")


def require_roles(permission: str) -> Callable[[dict[str, Any]], dict[str, Any]]:
    async def dependency(claims: dict[str, Any] = Depends(require_auth)) -> dict[str, Any]:
        allowed = set(ROLE_PERMISSIONS.get(permission, []))
        role = str(claims.get("role", ""))
        if allowed and role not in allowed:
            raise HTTPException(status_code=403, detail="forbidden for this role")
        return claims

    return dependency


@asynccontextmanager
async def lifespan(_: FastAPI):
    chroma_path = os.getenv("ECOSYSTEM_CHROMA_PATH", "/tmp/academia_chroma")
    collection_name = os.getenv("ECOSYSTEM_CHROMA_COLLECTION", "learning_memory")

    state.chroma_client = chromadb.PersistentClient(path=chroma_path)
    state.collection = state.chroma_client.get_or_create_collection(collection_name)

    neo4j_uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
    if neo4j_uri and neo4j_password:
        try:
            state.neo4j_driver = GraphDatabase.driver(
                neo4j_uri,
                auth=(neo4j_user, neo4j_password),
            )
            state.neo4j_driver.verify_connectivity()
        except Exception:
            state.neo4j_driver = None

    yield

    if state.neo4j_driver is not None:
        state.neo4j_driver.close()


app = FastAPI(
    title="Ecosystem Learning Runtime",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "chroma_ready": state.collection is not None,
        "neo4j_ready": state.neo4j_driver is not None,
    }


@app.post("/auth/token")
def create_token(payload: TokenRequestPayload) -> dict[str, Any]:
    return {
        "access_token": create_access_token(
            subject=payload.subject,
            role=payload.role,
            expires_minutes=payload.expires_minutes,
        ),
        "token_type": "bearer",
    }


@app.post("/memory/upsert")
def memory_upsert(
    payload: MemoryUpsertPayload,
    _: dict[str, Any] = Depends(require_roles("memory.upsert")),
) -> dict[str, str]:
    if state.collection is None:
        raise HTTPException(status_code=503, detail="ChromaDB is not initialized")

    state.collection.upsert(
        ids=[payload.memory_id],
        documents=[payload.content],
        metadatas=[payload.metadata],
    )
    return {"status": "stored", "memory_id": payload.memory_id}


@app.post("/memory/query")
def memory_query(
    payload: MemoryQueryPayload,
    _: dict[str, Any] = Depends(require_roles("memory.query")),
) -> dict[str, Any]:
    if state.collection is None:
        raise HTTPException(status_code=503, detail="ChromaDB is not initialized")

    result = state.collection.query(
        query_texts=[payload.query],
        n_results=payload.limit,
    )

    ids = result.get("ids", [[]])[0]
    docs = result.get("documents", [[]])[0]
    distances = result.get("distances", [[]])[0]
    matches = [
        {"id": item_id, "content": doc, "distance": dist}
        for item_id, doc, dist in zip(ids, docs, distances)
    ]

    return {"matches": matches}


@app.get("/graph/ping")
def graph_ping(_: dict[str, Any] = Depends(require_roles("graph.ping"))) -> dict[str, Any]:
    if state.neo4j_driver is None:
        return {
            "enabled": False,
            "message": "Set NEO4J_URI and NEO4J_PASSWORD to enable graph checks.",
        }

    try:
        with state.neo4j_driver.session() as session:
            record = session.run("RETURN 1 AS ok").single()
        return {"enabled": True, "ok": bool(record and record.get("ok") == 1)}
    except Neo4jError as exc:
        raise HTTPException(status_code=503, detail=f"Neo4j error: {exc}") from exc


@app.post("/learn/compose")
def learn_compose(
    payload: LearningComposePayload,
    _: dict[str, Any] = Depends(require_roles("learn.compose")),
) -> dict[str, Any]:
    prompt_value = state.prompt.invoke(
        {
            "topic": payload.topic,
            "goal": payload.goal,
            "context": payload.context,
        }
    )
    return {
        "messages": [
            {"type": msg.type, "content": msg.content}
            for msg in prompt_value.messages
        ]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "ecosystem_learning_runtime:app",
        host=os.getenv("ECOSYSTEM_RUNTIME_HOST", "0.0.0.0"),
        port=int(os.getenv("ECOSYSTEM_RUNTIME_PORT", "8010")),
        reload=False,
    )
