import os
import sys
from pathlib import Path


def _load_dotenv() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


if __name__ == "__main__":
    import uvicorn

    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    _load_dotenv()

    uvicorn.run(
        "main:app",
        host=os.getenv("ACADEMIA_RUNTIME_HOST", "0.0.0.0"),
        port=int(os.getenv("ACADEMIA_RUNTIME_PORT", "8910")),
        reload=False,
    )
