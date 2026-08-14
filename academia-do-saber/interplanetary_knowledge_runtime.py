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
    parser = argparse.ArgumentParser(description="Run the interplanetary knowledge runtime")
    parser.add_argument("--researcher", default=os.getenv("INTERPLANETARY_RESEARCHER", "scientific-demo"))
    parser.add_argument("--track", default=os.getenv("INTERPLANETARY_TRACK", "orbital-systems"))
    return parser.parse_args()


async def run_runtime() -> dict[str, object]:
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    _load_dotenv()

    from interplanetary.interplanetary_runtime import InterplanetaryEducationRuntime

    runtime = InterplanetaryEducationRuntime()
    return await runtime.planetary_curriculum()


async def _main() -> None:
    args = _parse_args()
    result = await run_runtime()
    payload = {
        "researcher": args.researcher,
        "track": args.track,
        **result,
    }
    print(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    asyncio.run(_main())