from __future__ import annotations
import os, json, sys
from openai import OpenAI
from utils.common import write_json, require_api_key

SCHEMA = {
  "type": "object",
  "properties": {
    "summary":{"type":"string"},
    "risk_score":{"type":"number"},
    "ioc_like_indicators":{"type":"array","items":{"type":"string"}},
    "recommended_actions":{"type":"array","items":{"type":"string"}}
  },
  "required":["summary","risk_score","recommended_actions"]
}

SAMPLE = "Sep  8 22:16:30 kali sshd[1205]: Failed password for root from 203.0.113.5 port 50221 ssh2"

def main():
    require_api_key()
    text = sys.stdin.read().strip() or SAMPLE
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages=[
        {"role":"system","content":"You are a senior SOC analyst. Return strict JSON only."},
        {"role":"user","content": f"Analyze the following snippet and produce JSON conforming to this schema: {json.dumps(SCHEMA)}\n\n{text}"}
    ]
    resp = client.chat.completions.create(model="gpt-5", messages=messages, temperature=0.1, max_tokens=1200)
    raw = resp.choices[0].message.content.strip()
    try:
        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()
        data = json.loads(raw)
    except Exception:
        data = {"summary":"Model did not return valid JSON","raw":raw,"risk_score":0,"recommended_actions":[]}
    path = write_json({"input_bytes": len(text), "report": data}, "reports/json/ch01_structured_demo")
    print(f"Wrote {path}")

if __name__ == "__main__":
    main()
