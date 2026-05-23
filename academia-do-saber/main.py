from contextlib import asynccontextmanager
from typing import Any, Callable
import os
import json
import hashlib
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response

from agents.john_professor import JohnProfessor
from certifications.certification_runtime import SovereignCertificationRuntime
from federation.subjects import ACADEMIA_SUBJECTS
from federation.runtime import federation_runtime
from graph.knowledge_graph import register_knowledge
from holographic.holographic_classrooms import HolographicClassroomRuntime
from interplanetary.interplanetary_runtime import InterplanetaryEducationRuntime
from observability import otel  # noqa: F401
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from runtime.collective_learning import CollectiveLearningRuntime
from runtime.education.cognition.adaptive_learning_runtime import AdaptiveLearningRuntime
from runtime.education.cognition.autonomous_learning_mesh import AutonomousLearningMesh
from runtime.education.cognition.cognition_propagation_runtime import CognitionPropagationRuntime
from runtime.education.cognition.federated_education_sync import FederatedEducationSync
from runtime.education.cognition.sovereign_knowledge_engine import SovereignKnowledgeEngine
from runtime.education.governance.adaptive_curriculum_runtime import AdaptiveCurriculumRuntime
from runtime.education.governance.cognition_ethics_runtime import CognitionEthicsRuntime
from runtime.education.governance.educational_policy_runtime import EducationalPolicyRuntime
from runtime.education.governance.knowledge_integrity_engine import KnowledgeIntegrityEngine
from runtime.education.governance.sovereign_learning_governance import SovereignLearningGovernance
from runtime.education.observability.cognition_trace_runtime import CognitionTraceRuntime
from runtime.education.observability.educational_telemetry_stream import EducationalTelemetryStream
from runtime.education.observability.knowledge_lineage_runtime import KnowledgeLineageRuntime
from runtime.education.observability.learning_metrics_runtime import LearningMetricsRuntime
from runtime.education.observability.sovereign_education_monitor import SovereignEducationMonitor
from runtime.identity_runtime import generate_learning_identity


APP_INSTRUMENTED = False


DEFAULT_POLICY: dict[str, list[str]] = {
    "courses.create": ["admin", "operator", "professor"],
    "certifications.issue": ["admin", "certifier", "professor"],
    "knowledge.register": ["admin", "researcher", "professor"],
    "collective.synchronize": ["admin", "operator"],
    "holographic.rooms.create": ["admin", "operator", "professor"],
    "interplanetary.curriculum": ["admin", "researcher", "professor"],
    "agents.john.mentor": ["admin", "operator", "professor"],
    "education.runtime.read": ["admin", "operator", "researcher", "professor"],
    "education.metrics.read": ["admin", "operator", "researcher", "professor"],
    "admin.rbac.status": ["admin"],
    "admin.rbac.reload": ["admin"],
}


def _parse_jwt_secrets() -> list[str]:
    secrets_from_list = os.getenv("JWT_SECRETS", "")
    parsed = [item.strip() for item in secrets_from_list.split(",") if item.strip()]
    if parsed:
        return parsed

    single_secret = os.getenv("JWT_SECRET", "liceu-academia-secret")
    return [single_secret]


def _normalize_permissions(loaded: dict[str, Any]) -> dict[str, list[str]]:
    permissions_source = loaded.get("permissions", loaded)
    if not isinstance(permissions_source, dict):
        return DEFAULT_POLICY

    normalized: dict[str, list[str]] = {}
    for key, value in permissions_source.items():
        if isinstance(key, str) and isinstance(value, list):
            normalized[key] = [str(role) for role in value]
    return normalized or DEFAULT_POLICY


def _policy_checksum(version: str, permissions: dict[str, list[str]]) -> str:
    canonical = json.dumps(
        {"version": version, "permissions": permissions},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode()).hexdigest()


def _load_rbac_policy() -> dict[str, Any]:
    if not os.path.exists(RBAC_POLICY_PATH):
        permissions = DEFAULT_POLICY
        version = "1.0.0"
        return {
            "version": version,
            "permissions": permissions,
            "checksum": _policy_checksum(version, permissions),
        }

    with open(RBAC_POLICY_PATH, "r", encoding="utf-8") as policy_file:
        loaded = json.load(policy_file)

    if not isinstance(loaded, dict):
        permissions = DEFAULT_POLICY
        version = "1.0.0"
        return {
            "version": version,
            "permissions": permissions,
            "checksum": _policy_checksum(version, permissions),
        }

    version = str(loaded.get("version", "1.0.0"))
    permissions = _normalize_permissions(loaded)
    return {
        "version": version,
        "permissions": permissions,
        "checksum": _policy_checksum(version, permissions),
    }


def _rbac_permissions() -> dict[str, list[str]]:
    permissions = RBAC_STATE.get("permissions", DEFAULT_POLICY)
    if isinstance(permissions, dict):
        return permissions
    return DEFAULT_POLICY


def _rbac_metadata() -> dict[str, str]:
    return {
        "version": str(RBAC_STATE.get("version", "1.0.0")),
        "checksum": str(RBAC_STATE.get("checksum", "")),
    }


@asynccontextmanager
async def lifespan(_: FastAPI):
    global APP_INSTRUMENTED

    if ENVIRONMENT == "production" and JWT_SECRETS[0] == "liceu-academia-secret":
        raise RuntimeError("JWT secret padrao nao permitido em producao")

    await federation_runtime.connect()
    if not APP_INSTRUMENTED:
        FastAPIInstrumentor.instrument_app(app)
        APP_INSTRUMENTED = True
    print("ACADEMIA DO SABER FEDERATION READY")
    yield


app = FastAPI(
    title="ACADEMIA DO SABER - Collective Intelligence Learning Runtime",
    lifespan=lifespan,
)

JWT_SECRET = os.getenv("JWT_SECRET", "liceu-academia-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
AUTH_ENABLED = os.getenv("AUTH_ENABLED", "true").lower() == "true"
PROMETHEUS_ENABLED = os.getenv("PROMETHEUS_ENABLED", "true").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
RBAC_POLICY_PATH = os.getenv("RBAC_POLICY_PATH", "config/rbac_policy.json")
JWT_SECRETS = _parse_jwt_secrets()
RBAC_STATE = _load_rbac_policy()

security = HTTPBearer(auto_error=False)

HTTP_REQUEST_COUNTER = Counter(
    "academia_http_requests_total",
    "Total HTTP requests processed by academia runtime",
    ["method", "path", "status_code"],
)

HTTP_REQUEST_LATENCY = Histogram(
    "academia_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)

EVENT_PUBLISH_COUNTER = Counter(
    "academia_subject_events_total",
    "Total events published by federation subject",
    ["subject", "status"],
)

AUTHZ_DECISION_COUNTER = Counter(
    "academia_authorization_decisions_total",
    "Total authorization decisions by permission",
    ["permission", "decision"],
)

collective_runtime = CollectiveLearningRuntime()
holographic_runtime = HolographicClassroomRuntime()
interplanetary_runtime = InterplanetaryEducationRuntime()
certification_runtime = SovereignCertificationRuntime()
john_professor = JohnProfessor()
adaptive_learning_runtime = AdaptiveLearningRuntime()
sovereign_knowledge_engine = SovereignKnowledgeEngine()
cognition_propagation_runtime = CognitionPropagationRuntime()
federated_education_sync = FederatedEducationSync()
autonomous_learning_mesh = AutonomousLearningMesh()
educational_policy_runtime = EducationalPolicyRuntime()
knowledge_integrity_engine = KnowledgeIntegrityEngine()
cognition_ethics_runtime = CognitionEthicsRuntime()
sovereign_learning_governance = SovereignLearningGovernance()
adaptive_curriculum_runtime = AdaptiveCurriculumRuntime()
learning_metrics_runtime = LearningMetricsRuntime()
cognition_trace_runtime = CognitionTraceRuntime()
educational_telemetry_stream = EducationalTelemetryStream()
knowledge_lineage_runtime = KnowledgeLineageRuntime()
sovereign_education_monitor = SovereignEducationMonitor()


class LearningIdentityPayload(BaseModel):
    email: str | None = None
    document: str | None = None
    university: str | None = None


class CourseCreatePayload(BaseModel):
    course_id: str
    title: str
    area: str
    instructor: str


class CertificationIssuePayload(BaseModel):
    student: str
    program: str


class KnowledgeUploadPayload(BaseModel):
    user_id: str
    knowledge_area: str
    certification: str


class HolographicRoomPayload(BaseModel):
    class_id: str
    instructor: str
    topic: str


class InterplanetaryResearchPayload(BaseModel):
    researcher: str
    track: str


class TokenRequestPayload(BaseModel):
    subject: str
    role: str = "academy-runtime"
    expires_minutes: int = 120


class RoleRequestPayload(BaseModel):
    role: str


def create_access_token(subject: str, role: str, expires_minutes: int = 120) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "role": role, "exp": int(expiration.timestamp())}
    return jwt.encode(payload, JWT_SECRETS[0], algorithm=JWT_ALGORITHM)


async def require_auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict[str, Any]:
    if not AUTH_ENABLED:
        return {"sub": "anonymous", "role": "disabled"}

    if credentials is None:
        raise HTTPException(status_code=401, detail="missing bearer token")

    for secret in JWT_SECRETS:
        try:
            return jwt.decode(
                credentials.credentials,
                secret,
                algorithms=[JWT_ALGORITHM],
            )
        except JWTError:
            continue

    raise HTTPException(status_code=401, detail="invalid bearer token")


def require_roles(permission: str) -> Callable[[dict[str, Any]], dict[str, Any]]:
    async def dependency(request: Request, claims: dict[str, Any] = Depends(require_auth)) -> dict[str, Any]:
        allowed_roles = set(_rbac_permissions().get(permission, []))
        role = str(claims.get("role", ""))
        actor = str(claims.get("sub", "unknown"))

        if not allowed_roles:
            AUTHZ_DECISION_COUNTER.labels(permission=permission, decision="deny").inc()
            await publish_authorization_audit(
                actor=actor,
                role=role,
                permission=permission,
                decision="deny",
                reason="permission_not_configured",
                request=request,
            )
            raise HTTPException(status_code=500, detail=f"permission not configured: {permission}")

        if role not in allowed_roles:
            AUTHZ_DECISION_COUNTER.labels(permission=permission, decision="deny").inc()
            await publish_authorization_audit(
                actor=actor,
                role=role,
                permission=permission,
                decision="deny",
                reason="role_not_allowed",
                request=request,
            )
            raise HTTPException(status_code=403, detail="insufficient role permissions")

        AUTHZ_DECISION_COUNTER.labels(permission=permission, decision="allow").inc()
        await publish_authorization_audit(
            actor=actor,
            role=role,
            permission=permission,
            decision="allow",
            reason="granted",
            request=request,
        )
        return claims

    return dependency


async def publish_event(subject_key: str, payload: dict[str, Any]) -> None:
    subject = ACADEMIA_SUBJECTS[subject_key]
    try:
        await federation_runtime.publish(subject, payload)
        EVENT_PUBLISH_COUNTER.labels(subject=subject, status="success").inc()
    except Exception:
        EVENT_PUBLISH_COUNTER.labels(subject=subject, status="failure").inc()
        raise


async def publish_authorization_audit(
    actor: str,
    role: str,
    permission: str,
    decision: str,
    reason: str,
    request: Request,
) -> None:
    subject = ACADEMIA_SUBJECTS.get("AUTHORIZATION_AUDIT")
    if not subject:
        return

    payload = {
        "actor": actor,
        "role": role,
        "permission": permission,
        "decision": decision,
        "reason": reason,
        "path": request.url.path,
        "method": request.method,
        "client_ip": request.client.host if request.client else "unknown",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "rbac_version": _rbac_metadata()["version"],
        "rbac_checksum": _rbac_metadata()["checksum"],
    }
    try:
        await federation_runtime.publish(subject, payload)
        EVENT_PUBLISH_COUNTER.labels(subject=subject, status="success").inc()
    except Exception:
        EVENT_PUBLISH_COUNTER.labels(subject=subject, status="failure").inc()


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    if not PROMETHEUS_ENABLED:
        return await call_next(request)

    started_at = datetime.now(timezone.utc)
    try:
        response = await call_next(request)
        status_code = str(response.status_code)
    except Exception:
        status_code = "500"
        raise
    finally:
        elapsed = (datetime.now(timezone.utc) - started_at).total_seconds()
        HTTP_REQUEST_COUNTER.labels(
            method=request.method,
            path=request.url.path,
            status_code=status_code,
        ).inc()
        HTTP_REQUEST_LATENCY.labels(
            method=request.method,
            path=request.url.path,
        ).observe(elapsed)

    return response


@app.get("/health")
async def health():
    return {"status": "healthy", "runtime": "academia-do-saber"}


@app.get("/education/runtime-status")
async def education_runtime_status(
    _: dict[str, Any] = Depends(require_roles("education.runtime.read")),
):
    cognition_state = {
        **adaptive_learning_runtime.state(),
        **sovereign_knowledge_engine.memory_state(),
        **cognition_propagation_runtime.propagation_metrics(),
    }
    federation_state = federated_education_sync.readiness()
    governance_state = {
        **educational_policy_runtime.policy_state(),
        **knowledge_integrity_engine.integrity(),
        **cognition_ethics_runtime.ethics(),
        **sovereign_learning_governance.continuity(),
    }
    mesh_state = autonomous_learning_mesh.evolution()
    benchmark_state = sovereign_education_monitor.benchmarks()

    return {
        "educational_cognition_state": cognition_state,
        "federated_learning_readiness": federation_state["federated_learning_readiness"],
        "sovereign_education_integrity": governance_state["educational_integrity"],
        "autonomous_curriculum_evolution": mesh_state["adaptive_curriculum_evolution"],
        "civilization_education_readiness": mesh_state["civilization_education_readiness"],
        "education_federation_mesh": federation_state["education_federation_mesh"],
        "benchmarks": benchmark_state,
        "objective": "Perpetual Sovereign Civilization Education Intelligence Runtime",
    }


@app.get("/education/cognition-metrics")
async def education_cognition_metrics(
    _: dict[str, Any] = Depends(require_roles("education.metrics.read")),
):
    learning_metrics = learning_metrics_runtime.metrics()
    trace_metrics = cognition_trace_runtime.trace()
    federation_metrics = federated_education_sync.readiness()["knowledge_federation_metrics"]
    curriculum_metrics = adaptive_curriculum_runtime.curriculum_state()
    telemetry_metrics = educational_telemetry_stream.stream_state()
    lineage_metrics = knowledge_lineage_runtime.lineage()

    return {
        "learning_propagation_score": learning_metrics["learning_propagation_score"],
        "cognition_synchronization": trace_metrics["cognition_synchronization"],
        "knowledge_federation_metrics": federation_metrics,
        "adaptive_learning_consistency": learning_metrics["adaptive_learning_consistency"],
        "educational_continuity_metrics": {
            "continuity_score": learning_metrics["educational_continuity_metrics"],
            "governance": sovereign_learning_governance.continuity()["educational_continuity_governance"],
            "knowledge_lineage": lineage_metrics["knowledge_lineage_propagation"],
        },
        "benchmark_snapshot": {
            **sovereign_education_monitor.benchmarks(),
            "curriculum_adaptation_speed_ms": curriculum_metrics["curriculum_adaptation_speed_ms"],
            "learning_federation_throughput_rps": telemetry_metrics["learning_federation_throughput_rps"],
            "cognition_propagation_latency_ms": trace_metrics["cognition_propagation_latency_ms"],
            "knowledge_synchronization_consistency": lineage_metrics["knowledge_synchronization_consistency"],
            "educational_governance_integrity": knowledge_integrity_engine.integrity()["knowledge_integrity_score"],
        },
    }


@app.get("/metrics")
async def metrics():
    if not PROMETHEUS_ENABLED:
        raise HTTPException(status_code=404, detail="metrics disabled")
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/admin/rbac/status")
async def rbac_status(
    _: dict[str, Any] = Depends(require_roles("admin.rbac.status")),
):
    metadata = _rbac_metadata()
    return {
        "version": metadata["version"],
        "checksum": metadata["checksum"],
        "permissions": _rbac_permissions(),
        "policy_path": RBAC_POLICY_PATH,
    }


@app.post("/admin/rbac/reload")
async def rbac_reload(
    _: dict[str, Any] = Depends(require_roles("admin.rbac.reload")),
):
    global RBAC_STATE
    RBAC_STATE = _load_rbac_policy()
    metadata = _rbac_metadata()
    return {
        "reloaded": True,
        "version": metadata["version"],
        "checksum": metadata["checksum"],
        "permissions_count": len(_rbac_permissions()),
    }


@app.post("/auth/token")
async def auth_token(payload: TokenRequestPayload):
    token = create_access_token(
        subject=payload.subject,
        role=payload.role,
        expires_minutes=payload.expires_minutes,
    )
    return {"access_token": token, "token_type": "bearer"}


@app.post("/auth/validate-role")
async def validate_role(payload: RoleRequestPayload, claims: dict[str, Any] = Depends(require_auth)):
    current_role = str(claims.get("role", ""))
    return {
        "allowed": current_role == payload.role,
        "current_role": current_role,
        "expected_role": payload.role,
    }


@app.post("/identity/generate")
async def identity_generate(payload: LearningIdentityPayload):
    return generate_learning_identity(payload.model_dump())


@app.post("/courses")
async def create_course(
    payload: CourseCreatePayload,
    _: dict[str, Any] = Depends(require_roles("courses.create")),
):
    event_payload = payload.model_dump()
    await publish_event("COURSE_CREATED", event_payload)
    return {"created": True, "course": event_payload}


@app.post("/certifications/issue")
async def issue_certification(
    payload: CertificationIssuePayload,
    _: dict[str, Any] = Depends(require_roles("certifications.issue")),
):
    certification = await certification_runtime.issue_certificate(
        student=payload.student,
        program=payload.program,
    )
    await publish_event("CERTIFICATION_ISSUED", certification)
    return certification


@app.post("/knowledge/register")
async def knowledge_register(
    payload: KnowledgeUploadPayload,
    _: dict[str, Any] = Depends(require_roles("knowledge.register")),
):
    response = {"registered": True, **payload.model_dump()}
    try:
        await register_knowledge(
            user_id=payload.user_id,
            knowledge_area=payload.knowledge_area,
            certification=payload.certification,
        )
    except Exception as exc:
        response["registered"] = False
        response["graph_error"] = str(exc)

    await publish_event("KNOWLEDGE_UPLOADED", response)
    return response


@app.post("/collective/synchronize")
async def collective_synchronize(
    _: dict[str, Any] = Depends(require_roles("collective.synchronize")),
):
    sync_result = await collective_runtime.synchronize_knowledge()
    await publish_event("COLLECTIVE_LEARNING", sync_result)
    return sync_result


@app.post("/holographic/rooms")
async def holographic_rooms(
    payload: HolographicRoomPayload,
    _: dict[str, Any] = Depends(require_roles("holographic.rooms.create")),
):
    room = await holographic_runtime.create_room()
    event_payload = {**payload.model_dump(), **room}
    await publish_event("HOLOGRAPHIC_CLASS", event_payload)
    return event_payload


@app.post("/interplanetary/curriculum")
async def interplanetary_curriculum(
    payload: InterplanetaryResearchPayload,
    _: dict[str, Any] = Depends(require_roles("interplanetary.curriculum")),
):
    curriculum = await interplanetary_runtime.planetary_curriculum()
    event_payload = {**payload.model_dump(), **curriculum}
    await publish_event("INTERPLANETARY_RESEARCH", event_payload)
    return event_payload


@app.post("/agents/john/mentor")
async def john_mentor(
    _: dict[str, Any] = Depends(require_roles("agents.john.mentor")),
):
    mentoring = await john_professor.mentor()
    await publish_event("JOHN_TRAINING", mentoring)
    return mentoring