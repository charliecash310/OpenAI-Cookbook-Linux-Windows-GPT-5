from __future__ import annotations
import os, json, sys
from openai import OpenAI
from utils.common import write_json, require_api_key

TEMPLATE = {
  "type":"object",
  "properties":{
    "yara":{"type":"array","items":{"type":"string"}},
    "sigma":{"type":"array","items":{"type":"string"}},
    "kql":{"type":"array","items":{"type":"string"}}
  },
  "required":["yara","sigma","kql"]
}

def main():
    require_api_key()
    src = sys.argv[1] if len(sys.argv)>1 else None
    data = {}
    if src and os.path.exists(src):
        data = json.load(open(src,"r",encoding="utf-8"))
    else:
        data = {"indicators":["203.0.113.5","/tmp/.x"],"behaviors":["multiple failed ssh","suspicious cron entries"]}

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    msgs=[
        {"role":"system","content":"You generate detection content. Return JSON only (yara[], sigma[], kql[])."},
        {"role":"user","content": f"Create YARA, Sigma, and KQL rules for these artifacts/behaviors: {json.dumps(data)}. Ensure syntactic correctness and include brief comments inline where supported."}
    ]
    r = client.chat.completions.create(model="gpt-5", messages=msgs, temperature=0.1, max_tokens=2200)
    raw = r.choices[0].message.content.strip()
    try:
        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()
        rules = json.loads(raw)
    except Exception:
        rules = {"error":"Model did not return JSON","raw":raw}

    p = write_json(rules, "rules/generated/ch05_rules")
    print(f"Wrote {p}")

if __name__ == "__main__":
    main()
