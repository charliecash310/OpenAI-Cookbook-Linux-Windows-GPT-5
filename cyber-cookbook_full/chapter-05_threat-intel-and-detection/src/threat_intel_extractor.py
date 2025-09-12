from __future__ import annotations
import re, sys
from utils.common import write_json

IOC_PATTERNS = {
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "domain": re.compile(r"\b([a-z0-9-]+\.)+[a-z]{2,}\b", re.I),
    "sha256": re.compile(r"\b[a-f0-9]{64}\b", re.I),
    "md5": re.compile(r"\b[a-f0-9]{32}\b", re.I),
}

def main():
    text = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not text and len(sys.argv) > 1 and sys.argv[1] != "-":
        with open(sys.argv[1], "r", errors="ignore") as f:
            text = f.read()
    if not text:
        print("Usage: cat report.txt | python threat_intel_extractor.py")
        raise SystemExit(1)

    found = {k: sorted(set(p.findall(text))) for k,p in IOC_PATTERNS.items()}
    p = write_json({"counts": {k: len(v) for k,v in found.items()}, "indicators": found}, "reports/json/ch05_ioc_extract")
    print(f"Wrote {p}")

if __name__ == "__main__":
    main()
