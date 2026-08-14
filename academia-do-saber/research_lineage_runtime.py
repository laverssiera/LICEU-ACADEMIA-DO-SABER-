import argparse
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
    parser = argparse.ArgumentParser(description="Run the research lineage runtime")
    parser.add_argument("--include-source", action="store_true")
    return parser.parse_args()


def run_runtime() -> dict[str, object]:
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    _load_dotenv()

    from runtime.education.observability.knowledge_lineage_runtime import KnowledgeLineageRuntime

    runtime = KnowledgeLineageRuntime()
    return runtime.lineage()


def main() -> None:
    args = _parse_args()
    payload = run_runtime()
    if args.include_source:
        payload = {
            "runtime": "knowledge_lineage_runtime",
            **payload,
        }
    print(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()