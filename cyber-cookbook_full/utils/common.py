from __future__ import annotations
import os, json
from pathlib import Path
from datetime import datetime

def timestamped(prefix: str, ext: str = ".json") -> Path:
    t = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    p = Path(f"{prefix}_{t}{ext}")
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def write_json(obj, prefix: str) -> Path:
    p = timestamped(prefix, ".json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    return p

def require_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise SystemExit("OPENAI_API_KEY is not set. Export it first.")
    return key
