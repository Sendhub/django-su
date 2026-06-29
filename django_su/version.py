import re
from pathlib import Path


def get_version() -> str:
    try:
        raw = Path(__file__).with_name("VERSION").read_text(encoding="utf-8").strip()
        m = re.search(r'^\s*(?:VERSION\s*=\s*)?["\']?(\d+(?:\.\d+)*)["\']?\s*$', raw)
        if not m:
            raise RuntimeError(f"VERSION file malformed: {raw!r}")
        return m.group(1)
    except Exception:
        return "1.0.0"


VERSION: str = get_version()
