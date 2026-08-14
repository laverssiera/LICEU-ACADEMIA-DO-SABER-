from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from threading import Lock
from typing import Any

from fastapi import APIRouter

router = APIRouter()


class CivilizationBrainRuntime:
    def __init__(self) -> None:
        default_db = Path(__file__).resolve().parents[1] / "data" / "educational_cognition.db"
        self._db_path = Path(os.getenv("ACADEMIA_COGNITION_DB_PATH", str(default_db)))
        self._db_lock = Lock()
        self._init_storage()

    def _init_storage(self) -> None:
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS learning_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    student_id TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    event TEXT NOT NULL,
                    progression_score REAL NOT NULL,
                    retention_score REAL NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS civilization_memory_sync (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    synced_at TEXT NOT NULL,
                    global_events INTEGER NOT NULL,
                    subjects INTEGER NOT NULL,
                    students INTEGER NOT NULL,
                    collective_intelligence_score REAL NOT NULL
                )
                """
            )
            conn.commit()

    def _compute_global_state(self) -> dict[str, Any]:
        with self._db_lock:
            with sqlite3.connect(self._db_path) as conn:
                row = conn.execute(
                    """
                    SELECT
                        COUNT(*) AS events,
                        COUNT(DISTINCT subject) AS subjects,
                        COUNT(DISTINCT student_id) AS students,
                        COALESCE(AVG(progression_score), 0.0) AS avg_progression,
                        COALESCE(AVG(retention_score), 0.0) AS avg_retention,
                        MIN(timestamp) AS first_event,
                        MAX(timestamp) AS last_event
                    FROM learning_memory
                    """
                ).fetchone()

        events = int(row[0] if row else 0)
        subjects = int(row[1] if row else 0)
        students = int(row[2] if row else 0)
        avg_progression = round(float(row[3] if row else 0.0), 4)
        avg_retention = round(float(row[4] if row else 0.0), 4)
        first_event = row[5] if row else None
        last_event = row[6] if row else None

        collective_intelligence_score = round(avg_progression * 0.55 + avg_retention * 0.45, 4)

        return {
            "global_knowledge_state": {
                "events": events,
                "subjects": subjects,
                "students": students,
                "avg_progression_score": avg_progression,
                "avg_retention_score": avg_retention,
            },
            "collective_educational_intelligence": {
                "score": collective_intelligence_score,
                "status": "active" if events > 0 else "bootstrapping",
            },
            "temporal_window": {
                "first_event_at": first_event,
                "last_event_at": last_event,
            },
            "civilization_learning_intelligence": {
                "sovereign": True,
                "distributed_consciousness": "enabled",
                "cognition_propagation": "active" if events > 0 else "warming-up",
            },
        }

    def _federated_learning_signals(self, limit: int) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 1000))
        with self._db_lock:
            with sqlite3.connect(self._db_path) as conn:
                rows = conn.execute(
                    """
                    SELECT subject,
                           COUNT(*) AS events,
                           AVG(progression_score) AS avg_progression,
                           AVG(retention_score) AS avg_retention
                    FROM learning_memory
                    GROUP BY subject
                    ORDER BY events DESC
                    LIMIT ?
                    """,
                    (safe_limit,),
                ).fetchall()

        signals: list[dict[str, Any]] = []
        for row in rows:
            subject = str(row[0])
            events = int(row[1])
            avg_progression = round(float(row[2]), 4)
            avg_retention = round(float(row[3]), 4)
            cognition_signal = round(avg_progression * 0.55 + avg_retention * 0.45, 4)
            signals.append(
                {
                    "subject": subject,
                    "events": events,
                    "cognition_signal": cognition_signal,
                    "signal_payload": {
                        "topic": subject,
                        "avg_progression": avg_progression,
                        "avg_retention": avg_retention,
                        "civilization_propagation": True,
                    },
                }
            )

        return signals

    def synchronize(self, limit: int = 20) -> dict[str, Any]:
        state = self._compute_global_state()
        signals = self._federated_learning_signals(limit=limit)
        score = float(state["collective_educational_intelligence"]["score"])

        with self._db_lock:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO civilization_memory_sync (
                        synced_at,
                        global_events,
                        subjects,
                        students,
                        collective_intelligence_score
                    )
                    VALUES (datetime('now'), ?, ?, ?, ?)
                    """,
                    (
                        state["global_knowledge_state"]["events"],
                        state["global_knowledge_state"]["subjects"],
                        state["global_knowledge_state"]["students"],
                        score,
                    ),
                )
                conn.commit()

        return {
            "runtime_identity": "Civilization Brain Runtime",
            "education_to_civilization_brain": "synchronized",
            "learning_signals_federation": {
                "signals": signals,
                "total_signals": len(signals),
            },
            "global_knowledge_state": state["global_knowledge_state"],
            "collective_educational_intelligence": state["collective_educational_intelligence"],
            "civilization_memory_sync": {
                "status": "completed",
                "shared_memory": True,
            },
            "civilization_learning_intelligence": state["civilization_learning_intelligence"],
            "temporal_window": state["temporal_window"],
        }

    def sync_history(self, limit: int = 20) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        with self._db_lock:
            with sqlite3.connect(self._db_path) as conn:
                rows = conn.execute(
                    """
                    SELECT synced_at, global_events, subjects, students, collective_intelligence_score
                    FROM civilization_memory_sync
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (safe_limit,),
                ).fetchall()

        return [
            {
                "synced_at": row[0],
                "global_events": int(row[1]),
                "subjects": int(row[2]),
                "students": int(row[3]),
                "collective_intelligence_score": float(row[4]),
            }
            for row in rows
        ]


runtime = CivilizationBrainRuntime()


@router.post("/education/civilization-brain/sync")
async def civilization_brain_sync(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    limit = int(data.get("limit", 20))
    return runtime.synchronize(limit=limit)


@router.get("/education/civilization-brain/state")
async def civilization_brain_state(limit: int = 20) -> dict[str, Any]:
    sync_state = runtime.synchronize(limit=limit)
    return {
        "runtime_identity": "Civilization Brain Runtime",
        "global_knowledge_state": sync_state["global_knowledge_state"],
        "collective_educational_intelligence": sync_state["collective_educational_intelligence"],
        "civilization_learning_intelligence": sync_state["civilization_learning_intelligence"],
        "temporal_window": sync_state["temporal_window"],
    }


@router.get("/education/civilization-brain/sync-history")
async def civilization_brain_sync_history(limit: int = 20) -> dict[str, Any]:
    records = runtime.sync_history(limit=limit)
    return {
        "runtime_identity": "Civilization Brain Runtime",
        "records": records,
        "total_returned": len(records),
    }
