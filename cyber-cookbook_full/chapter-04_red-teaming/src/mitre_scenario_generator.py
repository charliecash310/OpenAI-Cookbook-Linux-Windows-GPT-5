from __future__ import annotations
import os, sys
from openai import OpenAI
from utils.common import write_json, require_api_key

def main():
    require_api_key()
    target = sys.argv[1] if len(sys.argv) > 1 else "Small Windows AD environment with a web front-end"
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages=[
        {"role":"system","content":"You are a red-team planner. Provide ethical, high-level simulation plans that DO NOT include real-world exploitation steps."},
        {"role":"user","content": f"Create a benign red-team EXERCISE plan mapped to MITRE ATT&CK for: {target}. Include objectives, ATT&CK technique IDs, lab pre-reqs, and blue-team detection ideas."}
    ]
    r = client.chat.completions.create(model="gpt-5", messages=messages, temperature=0.3, max_tokens=1800)
    out = {"target": target, "plan_markdown": r.choices[0].message.content}
    p = write_json(out, "reports/json/ch04_mitre_scenario")
    print(f"Wrote {p}")

if __name__ == "__main__":
    main()
