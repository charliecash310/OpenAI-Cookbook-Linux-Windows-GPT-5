from __future__ import annotations
import sys, json
from pathlib import Path

def main():
    if len(sys.argv)<2:
        print("Usage: python security_onion_export.py <json_report_path>")
        raise SystemExit(1)
    src = Path(sys.argv[1])
    if not src.exists():
        raise SystemExit(f"Not found: {src}")
    data = json.load(open(src,"r",encoding="utf-8"))
    out = Path("reports/md") / (src.stem + "_so.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("# Security Onion Ingest Preview\n\n")
        f.write("`````\n")
        json.dump(data, f, indent=2)
        f.write("\n`````\n")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
