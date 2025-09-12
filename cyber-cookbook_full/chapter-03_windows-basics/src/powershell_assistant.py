from __future__ import annotations
import os, sys
from openai import OpenAI
from utils.common import require_api_key

def main():
    require_api_key()
    if len(sys.argv) < 2:
        print("Usage: python powershell_assistant.py <path_to_ps1_or_code>")
        raise SystemExit(1)
    path_or_text = sys.argv[1]
    text = open(path_or_text, "r", encoding="utf-8").read() if os.path.exists(path_or_text) else path_or_text

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    msgs=[
        {"role":"system","content":"You are a PowerShell expert. Explain code line by line, then produce a safer, commented rewrite."},
        {"role":"user","content": text[:20000]}
    ]
    r = client.chat.completions.create(model="gpt-5", messages=msgs, temperature=0.2, max_tokens=2500)
    print(r.choices[0].message.content)

if __name__ == "__main__":
    main()
