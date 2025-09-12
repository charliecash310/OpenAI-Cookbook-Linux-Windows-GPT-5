from __future__ import annotations
import os, json, subprocess
from openai import OpenAI
from utils.common import write_json, require_api_key

def get_events(log="Security", count=200):
    cmd = f"wevtutil qe {log} /c:{count} /rd:true /f:text"
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=120)
        return p.stdout
    except Exception as e:
        return f"[error] {e}"

def main():
    if os.name != "nt":
        raise SystemExit("Windows only.")
    require_api_key()
    sec = get_events("Security", 200)
    syslog = get_events("System", 100)
    app = get_events("Application", 100)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = [
        {"role":"system","content":"You are a Windows defender. Return JSON with: summary, risk_score, notable_events[], recommendations[]"},
        {"role":"user","content": f"Security:\n{sec}\n\nSystem:\n{syslog}\n\nApplication:\n{app}"}
    ]
    r = client.chat.completions.create(model="gpt-5", messages=messages, temperature=0.1, max_tokens=2500)
    raw = r.choices[0].message.content.strip()
    try:
        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()
        data = json.loads(raw)
    except Exception:
        data = {"summary":"Model did not return JSON","raw":raw,"risk_score":0,"recommendations":[]}
    p = write_json(data, "reports/json/ch03_win_event_triage")
    print(f"Wrote {p}")

if __name__ == "__main__":
    main()
