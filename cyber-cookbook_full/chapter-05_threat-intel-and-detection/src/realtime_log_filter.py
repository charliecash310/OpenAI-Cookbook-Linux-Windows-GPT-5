from __future__ import annotations
import sys, re, time, os
from utils.common import timestamped

def main():
    if len(sys.argv) < 3:
        print("Usage: python realtime_log_filter.py <log_file> <regex>")
        raise SystemExit(1)
    path, pattern = sys.argv[1], sys.argv[2]
    rx = re.compile(pattern, re.I)
    out = timestamped("reports/md/ch05_log_hits", ".md")
    with open(out, "w", encoding="utf-8") as md:
        md.write(f"# Log hits for `{pattern}`\n\n")
        with open(path, "r", errors="ignore") as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.25); continue
                if rx.search(line):
                    md.write(f"- {line}")
                    md.flush()
                    print(line, end="")

if __name__ == "__main__":
    main()
