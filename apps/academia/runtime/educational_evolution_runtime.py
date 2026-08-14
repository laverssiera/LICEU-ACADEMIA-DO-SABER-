from __future__ import annotations

import math
import os
import sqlite3
from collections import defaultdict
from pathlib import Path
from threading import Lock
from typing import Any

from fastapi import APIRouter

router = APIRouter()


class EducationalEvolutionRuntime:
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

    def _trend(self, first: float, last: float) -> str:
        delta = round(last - first, 4)
        if delta > 0.01:
            return "ascending"
        if delta < -0.01:
            return "descending"
        return "stable"

    def _safe_limit(self, value: int, max_value: int) -> int:
        return max(1, min(value, max_value))

    def _fetch_series(
        self,
        student_id: str,
        subject: str | None = None,
        limit: int = 120,
    ) -> list[dict[str, Any]]:
        safe_limit = self._safe_limit(limit, 2000)
        query = (
            "SELECT id, timestamp, student_id, subject, progression_score, retention_score "
            "FROM learning_memory WHERE student_id = ?"
        )
        params: list[Any] = [student_id]

        if subject:
            query += " AND subject = ?"
            params.append(subject)

        query += " ORDER BY id ASC LIMIT ?"
        params.append(safe_limit)

        with self._db_lock:
            with sqlite3.connect(self._db_path) as conn:
                rows = conn.execute(query, params).fetchall()

        return [
            {
                "id": int(row[0]),
                "timestamp": row[1],
                "student_id": row[2],
                "subject": row[3],
                "progression_score": float(row[4]),
                "retention_score": float(row[5]),
                "composite_score": round(float(row[4]) * 0.55 + float(row[5]) * 0.45, 4),
            }
            for row in rows
        ]

    def longitudinal_evolution(
        self,
        student_id: str,
        subject: str | None = None,
        limit: int = 120,
    ) -> dict[str, Any]:
        series = self._fetch_series(student_id=student_id, subject=subject, limit=limit)

        if not series:
            return {
                "student_id": student_id,
                "subject": subject,
                "sample_size": 0,
                "cognitive_evolution": {
                    "trend": "insufficient-data",
                    "evolution_delta": 0.0,
                },
                "learning_trajectory": {
                    "direction": "insufficient-data",
                    "projected_mastery_cycles": None,
                },
                "mastery_prediction": {
                    "mastery_target": 0.9,
                    "current_mastery": 0.0,
                    "mastery_probability_30d": 0.0,
                    "status": "insufficient-data",
                },
                "regression_detection": {
                    "regression_events": 0,
                    "latest_regression": False,
                    "risk_level": "unknown",
                },
                "temporal_educational_memory": {
                    "first_event_at": None,
                    "last_event_at": None,
                    "events": 0,
                },
                "sovereign_learning_analytics": {
                    "temporal_reasoning": "insufficient-data",
                    "continuity": "bootstrapping",
                    "federated_evolution_ready": True,
                },
            }

        composites = [row["composite_score"] for row in series]
        first_composite = composites[0]
        last_composite = composites[-1]
        trend = self._trend(first_composite, last_composite)
        evolution_delta = round(last_composite - first_composite, 4)

        progression_values = [row["progression_score"] for row in series]
        retention_values = [row["retention_score"] for row in series]

        slope = 0.0
        if len(composites) > 1:
            slope = round((last_composite - first_composite) / (len(composites) - 1), 4)

        mastery_target = 0.9
        current_mastery = round(last_composite, 4)
        if current_mastery >= mastery_target:
            projected_cycles = 0
        elif slope <= 0:
            projected_cycles = None
        else:
            projected_cycles = math.ceil((mastery_target - current_mastery) / slope)

        forecast_gain = max(0.0, slope) * 30
        mastery_probability_30d = round(min(0.99, max(0.01, current_mastery + forecast_gain)), 4)

        regression_events = 0
        latest_regression = False
        for index in range(1, len(composites)):
            delta = round(composites[index] - composites[index - 1], 4)
            if delta < -0.03:
                regression_events += 1
                if index == len(composites) - 1:
                    latest_regression = True

        if latest_regression or regression_events >= 2:
            risk_level = "high"
        elif trend == "descending" or regression_events == 1:
            risk_level = "medium"
        else:
            risk_level = "low"

        avg_progression = round(sum(progression_values) / len(progression_values), 4)
        avg_retention = round(sum(retention_values) / len(retention_values), 4)

        return {
            "student_id": student_id,
            "subject": subject,
            "sample_size": len(series),
            "cognitive_evolution": {
                "trend": trend,
                "evolution_delta": evolution_delta,
                "avg_progression": avg_progression,
                "avg_retention": avg_retention,
            },
            "learning_trajectory": {
                "direction": trend,
                "projected_mastery_cycles": projected_cycles,
                "current_cycle_score": current_mastery,
            },
            "mastery_prediction": {
                "mastery_target": mastery_target,
                "current_mastery": current_mastery,
                "mastery_probability_30d": mastery_probability_30d,
                "status": "on-track" if mastery_probability_30d >= 0.85 else "watch",
            },
            "regression_detection": {
                "regression_events": regression_events,
                "latest_regression": latest_regression,
                "risk_level": risk_level,
            },
            "temporal_educational_memory": {
                "first_event_at": series[0]["timestamp"],
                "last_event_at": series[-1]["timestamp"],
                "events": len(series),
            },
            "sovereign_learning_analytics": {
                "temporal_reasoning": "enabled",
                "continuity": "active",
                "federated_evolution_ready": True,
            },
        }

    def federated_evolution_analytics(
        self,
        limit: int = 20,
        min_events: int = 3,
    ) -> dict[str, Any]:
        safe_limit = self._safe_limit(limit, 200)
        safe_min_events = self._safe_limit(min_events, 1000)

        with self._db_lock:
            with sqlite3.connect(self._db_path) as conn:
                rows = conn.execute(
                    """
                    SELECT id, timestamp, student_id, subject, progression_score, retention_score
                    FROM learning_memory
                    ORDER BY subject ASC, id ASC
                    """
                ).fetchall()

        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            grouped[str(row[3])].append(
                {
                    "timestamp": row[1],
                    "student_id": row[2],
                    "progression": float(row[4]),
                    "retention": float(row[5]),
                    "composite": round(float(row[4]) * 0.55 + float(row[5]) * 0.45, 4),
                }
            )

        rankings: list[dict[str, Any]] = []
        for subject, events in grouped.items():
            if len(events) < safe_min_events:
                continue

            composites = [event["composite"] for event in events]
            trend = self._trend(composites[0], composites[-1])
            slope = 0.0
            if len(composites) > 1:
                slope = round((composites[-1] - composites[0]) / (len(composites) - 1), 4)

            regression_events = 0
            for index in range(1, len(composites)):
                if round(composites[index] - composites[index - 1], 4) < -0.03:
                    regression_events += 1

            avg_progression = round(sum(event["progression"] for event in events) / len(events), 4)
            avg_retention = round(sum(event["retention"] for event in events) / len(events), 4)
            evolution_score = round(avg_progression * 0.55 + avg_retention * 0.45 + slope, 4)

            rankings.append(
                {
                    "subject": subject,
                    "events": len(events),
                    "avg_progression_score": avg_progression,
                    "avg_retention_score": avg_retention,
                    "trend": trend,
                    "regression_events": regression_events,
                    "evolution_score": evolution_score,
                }
            )

        rankings.sort(key=lambda item: item["evolution_score"], reverse=True)
        for index, item in enumerate(rankings, start=1):
            item["rank"] = index

        rankings = rankings[:safe_limit]

        return {
            "subjects_ranked": len(rankings),
            "min_events": safe_min_events,
            "rankings": rankings,
            "civilization_scale_continuity": "active",
            "sovereign_educational_continuity": True,
        }


runtime = EducationalEvolutionRuntime()


@router.get("/education/educational-evolution")
async def educational_evolution(
    student_id: str,
    subject: str | None = None,
    limit: int = 120,
) -> dict[str, Any]:
    safe_limit = max(1, min(limit, 2000))
    evolution = runtime.longitudinal_evolution(student_id=student_id, subject=subject, limit=safe_limit)
    return {
        "runtime_identity": "Educational Evolution Runtime",
        "filters": {
            "student_id": student_id,
            "subject": subject,
            "limit": safe_limit,
        },
        "evolution": evolution,
    }


@router.get("/education/educational-evolution/federated-analytics")
async def educational_evolution_federated_analytics(
    limit: int = 20,
    min_events: int = 3,
) -> dict[str, Any]:
    safe_limit = max(1, min(limit, 200))
    safe_min_events = max(1, min(min_events, 1000))
    analytics = runtime.federated_evolution_analytics(limit=safe_limit, min_events=safe_min_events)
    return {
        "runtime_identity": "Educational Evolution Runtime",
        "filters": {
            "limit": safe_limit,
            "min_events": safe_min_events,
        },
        "analytics": analytics,
    }
