import argparse
import asyncio
import json
import os
import sys
from pathlib import Path


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run civilization knowledge runtime")
    parser.add_argument("--researcher", default=os.getenv("INTERPLANETARY_RESEARCHER", "scientific-demo"))
    parser.add_argument("--track", default=os.getenv("INTERPLANETARY_TRACK", "orbital-systems"))
    return parser.parse_args()


async def run_runtime() -> dict[str, object]:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from interplanetary_knowledge_runtime import run_runtime as knowledge_run_runtime

    return await knowledge_run_runtime()


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
