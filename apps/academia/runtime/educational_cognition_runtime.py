from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from threading import Lock
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter

router = APIRouter()


class EducationalCognitionRuntime:
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
            conn.commit()

    def _save_learning_record(self, learning_record: dict[str, Any]) -> None:
        with self._db_lock:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO learning_memory (
                        timestamp,
                        student_id,
                        subject,
                        event,
                        progression_score,
                        retention_score
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        learning_record["timestamp"],
                        learning_record["student_id"],
                        learning_record["subject"],
                        learning_record["event"],
                        learning_record["progression_score"],
                        learning_record["retention_score"],
                    ),
                )
                conn.commit()

    def _events_in_memory(self) -> int:
        with self._db_lock:
            with sqlite3.connect(self._db_path) as conn:
                row = conn.execute("SELECT COUNT(*) FROM learning_memory").fetchone()
        return int(row[0] if row else 0)

    def learning_history(
        self,
        student_id: str | None = None,
        subject: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        query = (
            "SELECT timestamp, student_id, subject, event, progression_score, retention_score "
            "FROM learning_memory"
        )
        filters: list[str] = []
        params: list[Any] = []

        if student_id:
            filters.append("student_id = ?")
            params.append(student_id)

        if subject:
            filters.append("subject = ?")
            params.append(subject)

        if filters:
            query = f"{query} WHERE {' AND '.join(filters)}"

        query = f"{query} ORDER BY id DESC LIMIT ?"
        params.append(safe_limit)

        with self._db_lock:
            with sqlite3.connect(self._db_path) as conn:
                rows = conn.execute(query, params).fetchall()

        return [
            {
                "timestamp": row[0],
                "student_id": row[1],
                "subject": row[2],
                "event": row[3],
                "progression_score": row[4],
                "retention_score": row[5],
            }
            for row in rows
        ]

    def learning_analytics(
        self,
        student_id: str | None = None,
        subject: str | None = None,
        limit: int = 200,
    ) -> dict[str, Any]:
        safe_limit = max(1, min(limit, 1000))
        query = (
            "SELECT timestamp, student_id, subject, progression_score, retention_score "
            "FROM learning_memory"
        )
        filters: list[str] = []
        params: list[Any] = []

        if student_id:
            filters.append("student_id = ?")
            params.append(student_id)

        if subject:
            filters.append("subject = ?")
            params.append(subject)

        if filters:
            query = f"{query} WHERE {' AND '.join(filters)}"

        query = f"{query} ORDER BY id ASC LIMIT ?"
        params.append(safe_limit)

        with self._db_lock:
            with sqlite3.connect(self._db_path) as conn:
                rows = conn.execute(query, params).fetchall()

        if not rows:
            return {
                "sample_size": 0,
                "avg_progression_score": 0.0,
                "avg_retention_score": 0.0,
                "adaptive_cognition_tracking": 0.0,
                "educational_reasoning_index": 0.0,
                "progression_trend": "insufficient-data",
                "retention_trend": "insufficient-data",
                "window": {
                    "from": None,
                    "to": None,
                },
            }

        progression_values = [float(row[3]) for row in rows]
        retention_values = [float(row[4]) for row in rows]
        avg_progression = round(sum(progression_values) / len(progression_values), 4)
        avg_retention = round(sum(retention_values) / len(retention_values), 4)

        def _trend(first: float, last: float) -> str:
            delta = round(last - first, 4)
            if delta > 0.01:
                return "ascending"
            if delta < -0.01:
                return "descending"
            return "stable"

        progression_trend = _trend(progression_values[0], progression_values[-1])
        retention_trend = _trend(retention_values[0], retention_values[-1])

        return {
            "sample_size": len(rows),
            "avg_progression_score": avg_progression,
            "avg_retention_score": avg_retention,
            "adaptive_cognition_tracking": round((avg_progression + avg_retention) / 2, 4),
            "educational_reasoning_index": round(avg_progression * 0.55 + avg_retention * 0.45, 4),
            "progression_trend": progression_trend,
            "retention_trend": retention_trend,
            "window": {
                "from": rows[0][0],
                "to": rows[-1][0],
            },
        }

    def federated_subject_analytics(
        self,
        limit: int = 20,
        min_events: int = 1,
    ) -> dict[str, Any]:
        safe_limit = max(1, min(limit, 200))
        safe_min_events = max(1, min(min_events, 1000))

        with self._db_lock:
            with sqlite3.connect(self._db_path) as conn:
                rows = conn.execute(
                    """
                    SELECT
                        subject,
                        COUNT(*) AS events,
                        AVG(progression_score) AS avg_progression,
                        AVG(retention_score) AS avg_retention
                    FROM learning_memory
                    GROUP BY subject
                    HAVING COUNT(*) >= ?
                    ORDER BY ((AVG(progression_score) * 0.55) + (AVG(retention_score) * 0.45)) DESC
                    LIMIT ?
                    """,
                    (safe_min_events, safe_limit),
                ).fetchall()

        rankings: list[dict[str, Any]] = []
        for index, row in enumerate(rows, start=1):
            avg_progression = round(float(row[2]), 4)
            avg_retention = round(float(row[3]), 4)
            reasoning_score = round(avg_progression * 0.55 + avg_retention * 0.45, 4)
            rankings.append(
                {
                    "rank": index,
                    "subject": row[0],
                    "events": int(row[1]),
                    "avg_progression_score": avg_progression,
                    "avg_retention_score": avg_retention,
                    "educational_reasoning_score": reasoning_score,
                }
            )

        return {
            "subjects_ranked": len(rankings),
            "min_events": safe_min_events,
            "rankings": rankings,
        }

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        subject = str(payload.get("subject", "general")).strip() or "general"
        student_id = str(payload.get("student_id", "anonymous")).strip() or "anonymous"
        skill_signals = payload.get("skill_signals", {})

        if not isinstance(skill_signals, dict):
            skill_signals = {}

        progression_score = float(payload.get("progression_score", 0.72))
        retention_score = float(payload.get("retention_score", 0.76))

        learning_record = {
            "timestamp": self._utc_now(),
            "student_id": student_id,
            "subject": subject,
            "event": payload.get("event", "learning-session"),
            "progression_score": progression_score,
            "retention_score": retention_score,
        }
        self._save_learning_record(learning_record)

        skill_mapping = {
            "subject": subject,
            "skills": skill_signals,
            "mapped_at": self._utc_now(),
        }

        learning_trajectory = {
            "student_id": student_id,
            "current_stage": payload.get("current_stage", "intermediate"),
            "target_stage": payload.get("target_stage", "advanced"),
            "next_cycle_hours": payload.get("next_cycle_hours", 24),
        }

        educational_analytics = {
            "events_in_memory": self._events_in_memory(),
            "adaptive_cognition_tracking": round((progression_score + retention_score) / 2, 4),
            "educational_reasoning_index": round(progression_score * 0.55 + retention_score * 0.45, 4),
            "federated_educational_intelligence": True,
            "civilization_continuity": "active",
            "sovereign_pedagogy_intelligence": "enabled",
        }

        return {
            "runtime_identity": "Educational Cognition Runtime",
            "learning_memory": learning_record,
            "cognitive_progression": {
                "progression_score": progression_score,
                "status": "evolving" if progression_score >= 0.7 else "stabilizing",
            },
            "skill_mapping": skill_mapping,
            "knowledge_retention": {
                "retention_score": retention_score,
                "status": "retained" if retention_score >= 0.7 else "reinforcement-needed",
            },
            "learning_trajectory": learning_trajectory,
            "educational_analytics": educational_analytics,
            "generated_at": self._utc_now(),
        }


runtime = EducationalCognitionRuntime()


@router.post("/education/educational-cognition")
async def educational_cognition(payload: dict[str, Any]) -> dict[str, Any]:
    return runtime.process(payload)


@router.get("/education/educational-cognition/history")
async def educational_cognition_history(
    student_id: str | None = None,
    subject: str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    history = runtime.learning_history(student_id=student_id, subject=subject, limit=limit)
    return {
        "runtime_identity": "Educational Cognition Runtime",
        "filters": {
            "student_id": student_id,
            "subject": subject,
            "limit": max(1, min(limit, 500)),
        },
        "records": history,
        "total_returned": len(history),
    }


@router.get("/education/educational-cognition/analytics")
async def educational_cognition_analytics(
    student_id: str | None = None,
    subject: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    safe_limit = max(1, min(limit, 1000))
    analytics = runtime.learning_analytics(student_id=student_id, subject=subject, limit=safe_limit)
    return {
        "runtime_identity": "Educational Cognition Runtime",
        "filters": {
            "student_id": student_id,
            "subject": subject,
            "limit": safe_limit,
        },
        "analytics": analytics,
    }


@router.get("/education/educational-cognition/federated-analytics")
async def educational_cognition_federated_analytics(
    limit: int = 20,
    min_events: int = 1,
) -> dict[str, Any]:
    safe_limit = max(1, min(limit, 200))
    safe_min_events = max(1, min(min_events, 1000))
    analytics = runtime.federated_subject_analytics(limit=safe_limit, min_events=safe_min_events)
    return {
        "runtime_identity": "Educational Cognition Runtime",
        "federated_intelligence": "enabled",
        "filters": {
            "limit": safe_limit,
            "min_events": safe_min_events,
        },
        "analytics": analytics,
    }
