import argparse
import json
import os
import sys
from pathlib import Path


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run civilization memory runtime")
    parser.add_argument("--student-id", default=os.getenv("SCIENTIFIC_MEMORY_STUDENT_ID", "scientific-demo"))
    parser.add_argument("--discipline", default=os.getenv("SCIENTIFIC_MEMORY_DISCIPLINE", "scientific_memory"))
    parser.add_argument("--cognition-score", type=float, default=float(os.getenv("SCIENTIFIC_MEMORY_COGNITION", "0.88")))
    parser.add_argument("--consistency", type=float, default=float(os.getenv("SCIENTIFIC_MEMORY_CONSISTENCY", "0.84")))
    parser.add_argument("--engagement", type=float, default=float(os.getenv("SCIENTIFIC_MEMORY_ENGAGEMENT", "0.91")))
    return parser.parse_args()


def run_runtime(payload: dict[str, object]) -> dict[str, object]:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from scientific_memory_runtime import run_runtime as memory_run_runtime

    return memory_run_runtime(payload)


def main() -> None:
    args = _parse_args()
    payload = {
        "student_id": args.student_id,
        "discipline": args.discipline,
        "cognition_score": args.cognition_score,
        "consistency": args.consistency,
        "engagement": args.engagement,
    }
    result = run_runtime(payload)
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
