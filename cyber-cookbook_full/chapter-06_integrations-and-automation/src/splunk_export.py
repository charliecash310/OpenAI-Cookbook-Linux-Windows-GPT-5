from __future__ import annotations
import os, json, sys, csv
from pathlib import Path

def main():
    if len(sys.argv)<2:
        print("Usage: python splunk_export.py <json_report_path>")
        raise SystemExit(1)
    src = Path(sys.argv[1])
    if not src.exists():
        raise SystemExit(f"Not found: {src}")
    data = json.load(open(src,"r",encoding="utf-8"))
    rows = []
    def flatten(prefix, obj):
        if isinstance(obj, dict):
            for k,v in obj.items():
                flatten(f"{prefix}.{k}" if prefix else k, v)
        elif isinstance(obj, list):
            for i,v in enumerate(obj):
                flatten(f"{prefix}[{i}]", v)
        else:
            rows.append((prefix, obj))
    flatten("", data)
    out_dir = Path("reports/csv"); out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / (src.stem + ".csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["key","value"]); w.writerows(rows)
    print(f"Wrote {out}  (import into Splunk as CSV)")

if __name__ == "__main__":
    main()
