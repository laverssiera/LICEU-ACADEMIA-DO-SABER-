"""Durable storage for the academia_memory_chain.

This is the persistence layer of the institutional memory that already exists in
``educational_memory_mesh``. It does not introduce a second memory system: the
in-process ``INSTITUTIONAL_MEMORY`` registry is rehydrated from this table.
"""

from __future__ import annotations

import json
import os
import sqlite3
import time
from contextlib import closing
from pathlib import Path
from threading import Lock
from typing import Any


CHAIN_FIELDS = (
    "event",
    "cause",
    "context",
    "decision",
    "execution",
    "impact",
    "risk",
    "mitigation",
    "result",
    "lesson_learned",
)

JSON_FIELDS = (
    "source_artifacts",
    "evidence",
    "graph_nodes",
    "graph_edges",
    "scientific_memory",
)

MIGRATION_SQL = """
CREATE TABLE IF NOT EXISTS academia_memory_chain (
    knowledge_record_id TEXT PRIMARY KEY,
    lesson_learned_id TEXT NOT NULL,
    planetary_operational_state_id TEXT NOT NULL,
    wave INTEGER NOT NULL,
    recorded_at REAL NOT NULL,
    event TEXT NOT NULL,
    cause TEXT NOT NULL,
    context TEXT NOT NULL,
    decision TEXT NOT NULL,
    execution TEXT NOT NULL,
    impact TEXT NOT NULL,
    risk TEXT NOT NULL,
    mitigation TEXT NOT NULL,
    result TEXT NOT NULL,
    lesson_learned TEXT NOT NULL,
    source_artifacts TEXT NOT NULL,
    evidence TEXT NOT NULL,
    graph_nodes TEXT NOT NULL,
    graph_edges TEXT NOT NULL,
    scientific_memory TEXT NOT NULL,
    usable_for_future_decision INTEGER NOT NULL
)
"""

MIGRATION_INDEXES = (
    "CREATE INDEX IF NOT EXISTS idx_academia_memory_chain_state "
    "ON academia_memory_chain (planetary_operational_state_id)",
    "CREATE INDEX IF NOT EXISTS idx_academia_memory_chain_lesson "
    "ON academia_memory_chain (lesson_learned_id)",
)

_DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "runtime" / "storage" / "academia_memory.db"
_WRITE_LOCK = Lock()


def database_path() -> Path:
    return Path(
        os.getenv("ACADEMIA_MEMORY_DB_PATH")
        or os.getenv("ACADEMIA_COGNITION_DB_PATH")
        or str(_DEFAULT_DB_PATH)
    )


def _connect() -> sqlite3.Connection:
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def _table_exists(connection: sqlite3.Connection) -> bool:
    row = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='academia_memory_chain'"
    ).fetchone()
    return row is not None


def apply_migration() -> dict[str, Any]:
    """Apply the academia_memory_chain migration when the database lacks it."""
    with _WRITE_LOCK, closing(_connect()) as connection:
        already_applied = _table_exists(connection)
        connection.execute(MIGRATION_SQL)
        for statement in MIGRATION_INDEXES:
            connection.execute(statement)
        connection.commit()
        return {
            "database_path": str(database_path()),
            "table": "academia_memory_chain",
            "already_applied": already_applied,
            "applied_now": not already_applied,
        }


def _serialize(record: dict[str, Any]) -> dict[str, Any]:
    row = {
        "knowledge_record_id": record["knowledge_record_id"],
        "lesson_learned_id": record["lesson_learned_id"],
        "planetary_operational_state_id": record["planetary_operational_state_id"],
        "wave": int(record.get("wave", 86)),
        "recorded_at": float(record.get("recorded_at") or time.time()),
        "usable_for_future_decision": 1 if record.get("usable_for_future_decision") else 0,
    }
    chain = record.get("chain", {})
    for field in CHAIN_FIELDS:
        row[field] = str(chain.get(field, ""))
    for field in JSON_FIELDS:
        row[field] = json.dumps(record.get(field), ensure_ascii=True, sort_keys=True)
    return row


def _deserialize(row: sqlite3.Row) -> dict[str, Any]:
    record: dict[str, Any] = {
        "knowledge_record_id": row["knowledge_record_id"],
        "lesson_learned_id": row["lesson_learned_id"],
        "planetary_operational_state_id": row["planetary_operational_state_id"],
        "wave": int(row["wave"]),
        "recorded_at": float(row["recorded_at"]),
        "chain": {field: row[field] for field in CHAIN_FIELDS},
        "usable_for_future_decision": bool(row["usable_for_future_decision"]),
        "persisted": True,
    }
    for field in JSON_FIELDS:
        record[field] = json.loads(row[field])
    return record


def save_record(record: dict[str, Any]) -> dict[str, Any]:
    """Persist a chain record atomically; a replay never duplicates it."""
    apply_migration()
    row = _serialize(record)
    columns = ", ".join(row)
    placeholders = ", ".join(f":{column}" for column in row)
    with _WRITE_LOCK, closing(_connect()) as connection:
        try:
            connection.execute(
                f"INSERT INTO academia_memory_chain ({columns}) VALUES ({placeholders})",
                row,
            )
        except sqlite3.IntegrityError:
            connection.rollback()
        else:
            connection.commit()
    return fetch_record(record["knowledge_record_id"]) or record


def fetch_record(knowledge_record_id: str) -> dict[str, Any] | None:
    apply_migration()
    with closing(_connect()) as connection:
        row = connection.execute(
            "SELECT * FROM academia_memory_chain WHERE knowledge_record_id = ?",
            (knowledge_record_id,),
        ).fetchone()
    return _deserialize(row) if row is not None else None


def load_records() -> list[dict[str, Any]]:
    apply_migration()
    with closing(_connect()) as connection:
        rows = connection.execute(
            "SELECT * FROM academia_memory_chain ORDER BY recorded_at, knowledge_record_id"
        ).fetchall()
    return [_deserialize(row) for row in rows]


def count_records() -> int:
    apply_migration()
    with closing(_connect()) as connection:
        return int(connection.execute("SELECT COUNT(*) FROM academia_memory_chain").fetchone()[0])


def delete_record(knowledge_record_id: str) -> bool:
    apply_migration()
    with _WRITE_LOCK, closing(_connect()) as connection:
        cursor = connection.execute(
            "DELETE FROM academia_memory_chain WHERE knowledge_record_id = ?",
            (knowledge_record_id,),
        )
        connection.commit()
        return cursor.rowcount > 0


def hydrate(institutional_memory: list[dict[str, Any]]) -> int:
    """Rebuild the in-process institutional memory from the durable chain."""
    known = {
        record.get("knowledge_record_id")
        for record in institutional_memory
        if record.get("knowledge_record_id")
    }
    restored = 0
    for record in load_records():
        if record["knowledge_record_id"] in known:
            continue
        institutional_memory.append(record)
        restored += 1
    return restored
