import argparse
import json
import os
import sys
from pathlib import Path


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run civilization learning runtime")
    parser.add_argument("--limit", type=int, default=int(os.getenv("CIVILIZATION_LEARNING_LIMIT", "20")))
    return parser.parse_args()


def run_runtime(limit: int) -> dict[str, object]:
    workspace_root = Path(__file__).resolve().parents[2]
    apps_academia_root = workspace_root / "apps" / "academia"

    if str(apps_academia_root) not in sys.path:
        sys.path.insert(0, str(apps_academia_root))

    from runtime.civilization_brain_runtime import runtime as civilization_runtime

    return civilization_runtime.synchronize(limit=limit)


def main() -> None:
    args = _parse_args()
    result = run_runtime(limit=args.limit)
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
