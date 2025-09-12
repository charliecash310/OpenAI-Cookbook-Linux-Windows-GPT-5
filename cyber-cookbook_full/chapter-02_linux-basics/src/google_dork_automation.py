#!/usr/bin/env python3
from __future__ import annotations
import sys, json
from utils.common import write_json

TEMPLATES = [
    "site:{domain} intitle:index.of",
    "site:{domain} ext:sql | ext:bak | ext:old",
    "site:{domain} \"password\" OR \"secret\" -github -gitlab",
    "site:{domain} inurl:admin | inurl:login",
    "site:{domain} filetype:pdf confidential OR internal",
]

def main():
    if len(sys.argv) < 2:
        print("Usage: python google_dork_automation.py <domain>")
        raise SystemExit(1)
    domain = sys.argv[1].strip()
    dorks = [t.format(domain=domain) for t in TEMPLATES]
    path = write_json({"domain": domain, "queries": dorks}, "reports/json/ch02_google_dorks")
    print("\n".join(dorks))
    print(f"\nSaved to {path}")

if __name__ == "__main__":
    main()
