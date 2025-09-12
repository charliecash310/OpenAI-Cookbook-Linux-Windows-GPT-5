from __future__ import annotations
import os, sys
from openai import OpenAI
from utils.common import write_json, require_api_key

def main():
    require_api_key()
    target = sys.argv[1] if len(sys.argv) > 1 else "Acme Corp"
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    msgs = [
        {"role":"system","content":"You are an OSINT planning assistant. Provide lawful, ethical research checklists and NEVER collect data directly."},
        {"role":"user","content": f"Design an OSINT checklist for {target}. Include sources (public), what to look for, and reporting format. Output JSON with sections."}
    ]
    r = client.chat.completions.create(model="gpt-5", messages=msgs, temperature=0.2, max_tokens=1600)
    raw = r.choices[0].message.content
    p = write_json({"target":target,"osint_plan":raw}, "reports/json/ch04_osint_plan")
    print(f"Wrote {p}")

if __name__ == "__main__":
    main()
