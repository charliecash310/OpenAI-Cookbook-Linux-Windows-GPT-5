from __future__ import annotations
import os, json, subprocess
from openai import OpenAI
from utils.common import write_json, require_api_key

MODEL = "gpt-5"
TIMEOUT = 120

def run_cmd(cmd: str) -> str:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=TIMEOUT)
        out = proc.stdout.strip()
        err = proc.stderr.strip()
        return (out + ("\n[stderr]\n" + err if err else "")).strip()
    except Exception as e:
        return f"[error running '{cmd}'] {e}"

def collect():
    arts = {}
    arts["processes"] = run_cmd("tasklist /v")
    arts["netstat"] = run_cmd("netstat -ano")
    arts["schtasks"] = run_cmd("schtasks /query /fo LIST /v")
    arts["security_log"] = run_cmd("wevtutil qe Security /c:200 /rd:true /f:text")
    return arts

def main():
    if os.name != "nt":
        raise SystemExit("This script must run on Windows.")
    require_api_key()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    arts = collect()

    messages=[
        {"role":"system","content":"You are a SOC analyst. Return strict JSON with keys: summary, risk_score, suspicious_processes, suspicious_connections, persistence_or_tasks, recommended_actions."},
        {"role":"user","content": f"Processes:\n{arts['processes']}\n\nNetstat:\n{arts['netstat']}\n\nTasks:\n{arts['schtasks']}\n\nSecurity Log (tail):\n{arts['security_log']}"}
    ]
    resp = client.chat.completions.create(model=MODEL, messages=messages, temperature=0.2, max_tokens=3000)
    raw = resp.choices[0].message.content.strip()
    try:
        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()
        data = json.loads(raw)
    except Exception:
        data = {"summary":"Model did not return JSON","raw":raw,"risk_score":0,"recommended_actions":[]}
    p = write_json({"host": os.getenv("COMPUTERNAME","unknown"), "report": data}, "reports/json/ch03_apt_triage")
    print(f"Wrote {p}")

if __name__ == "__main__":
    main()
