from openai import OpenAI
import os
from utils.common import require_api_key

def main():
    require_api_key()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = [
        {"role": "system", "content": "You are a helpful cybersecurity assistant."},
        {"role": "user", "content": "Summarize this log line: Sep  8 22:16:30 kali sshd[1205]: Failed password for root from 203.0.113.5 port 50221 ssh2"}
    ]
    resp = client.chat.completions.create(model="gpt-5", messages=messages, temperature=0.2)
    print(resp.choices[0].message.content)

if __name__ == "__main__":
    main()
