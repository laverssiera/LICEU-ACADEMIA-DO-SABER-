import argparse
import asyncio
import json
import os
import sys
from pathlib import Path


def _load_dotenv() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the planet education runtime")
    parser.add_argument("--planet", default=os.getenv("PLANET_NAME", "earth"))
    parser.add_argument("--track", default=os.getenv("PLANET_TRACK", "foundational-education"))
    parser.add_argument("--student-id", default=os.getenv("PLANET_STUDENT_ID", "earth-cycle-student"))
    parser.add_argument("--researcher", default=os.getenv("PLANET_RESEARCHER", "earth-cycle-researcher"))
    parser.add_argument("--discipline", default=os.getenv("PLANET_DISCIPLINE", "earth_systems"))
    parser.add_argument("--certification", default=os.getenv("PLANET_CERTIFICATION", "earth_runtime_mastery"))
    parser.add_argument("--cognition-score", type=float, default=float(os.getenv("PLANET_COGNITION", "0.9")))
    parser.add_argument("--consistency", type=float, default=float(os.getenv("PLANET_CONSISTENCY", "0.86")))
    parser.add_argument("--engagement", type=float, default=float(os.getenv("PLANET_ENGAGEMENT", "0.93")))
    parser.add_argument(
        "--scientific-finding",
        default=os.getenv("PLANET_SCIENTIFIC_FINDING", "planetary learning loops improve retention"),
    )
    parser.add_argument(
        "--model",
        default=os.getenv("PLANET_MODEL", "earth adaptive model"),
    )
    parser.add_argument(
        "--lesson-learned",
        default=os.getenv("PLANET_LESSON_LEARNED", "continuous feedback improves educational continuity"),
    )
    parser.add_argument(
        "--engineering-knowledge",
        default=os.getenv("PLANET_ENGINEERING_KNOWLEDGE", "distributed school labs increase infrastructure resilience"),
    )
    parser.add_argument(
        "--economic-knowledge",
        default=os.getenv("PLANET_ECONOMIC_KNOWLEDGE", "micro-credentials improve workforce mobility"),
    )
    parser.add_argument(
        "--climate-knowledge",
        default=os.getenv("PLANET_CLIMATE_KNOWLEDGE", "community observatories accelerate climate adaptation"),
    )
    return parser.parse_args()


async def run_runtime() -> dict[str, object]:
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    _load_dotenv()

    from interplanetary.interplanetary_runtime import InterplanetaryEducationRuntime

    runtime = InterplanetaryEducationRuntime()
    return await runtime.planetary_curriculum()


async def _run_earth_knowledge_cycle(args: argparse.Namespace) -> dict[str, object]:
    from earth_knowledge_runtime import run_runtime_async as earth_knowledge_run_runtime

    earth_payload = {
        "student_id": args.student_id,
        "researcher": args.researcher,
        "discipline": args.discipline,
        "certification": args.certification,
        "cognition_score": args.cognition_score,
        "consistency": args.consistency,
        "engagement": args.engagement,
        "scientific_finding": args.scientific_finding,
        "model": args.model,
        "lesson_learned": args.lesson_learned,
        "engineering_knowledge": args.engineering_knowledge,
        "economic_knowledge": args.economic_knowledge,
        "climate_knowledge": args.climate_knowledge,
    }
    return await earth_knowledge_run_runtime(earth_payload)


async def _main() -> None:
    args = _parse_args()
    result = await run_runtime()
    earth_result = None
    if args.planet.strip().lower() == "earth":
        # Earth cycles always persist the runtime learnings into the knowledge stack.
        earth_result = await _run_earth_knowledge_cycle(args)

    payload = {
        "planet": args.planet,
        "track": args.track,
        **result,
    }
    if earth_result is not None:
        payload["earth_knowledge_persistence"] = earth_result

    print(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    asyncio.run(_main())
