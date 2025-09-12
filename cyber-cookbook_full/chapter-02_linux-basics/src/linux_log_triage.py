from __future__ import annotations
import os, sys, json
from pathlib import Path
from openai import OpenAI
from utils.common import write_json, require_api_key

def read_text(maybe_path: str) -> str:
    p = Path(maybe_path)
    if p.exists() and p.is_file():
        return p.read_text(errors="ignore")
    return maybe_path

def main():
    require_api_key()
    source = sys.argv[1] if len(sys.argv) > 1 else "Sep  8 22:16:30 kali sshd[1205]: Failed password for root from 203.0.113.5 port 50221 ssh2"
    text = read_text(source)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = [
        {"role":"system","content":"You are a Linux blue-team analyst. Return strict JSON."},
        {"role":"user","content":(
            "Analyze Linux logs below. Identify brute-force, suspicious IPs, and commands. "
            "Output JSON with keys: summary, risk_score (0-10), indicators (list), "
            "recommended_actions (list), mitre_techniques (list).\n\n"
            f"{text[:20000]}"
        )}
    ]
    resp = client.chat.completions.create(model="gpt-5", messages=messages, temperature=0.1, max_tokens=2000)
    raw = resp.choices[0].message.content.strip()
    try:
        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()
        data = json.loads(raw)
    except Exception:
        data = {"summary":"Model did not produce JSON","raw":raw,"risk_score":0,"indicators":[],"recommended_actions":[],"mitre_techniques":[]}

    path = write_json({"source": source, "report": data}, "reports/json/ch02_linux_log_triage")
    print(f"Wrote {path}")

if __name__ == "__main__":
    main()
