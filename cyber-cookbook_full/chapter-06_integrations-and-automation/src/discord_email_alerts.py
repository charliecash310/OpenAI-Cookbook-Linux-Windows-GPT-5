from __future__ import annotations
import os, sys, json, smtplib, ssl, requests
from email.message import EmailMessage
from pathlib import Path

def send_email(subject: str, body: str):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    recipient = os.getenv("ALERT_EMAIL_TO")
    if not all([smtp_host, smtp_user, smtp_pass, recipient]):
        print("[email] Missing SMTP_* or ALERT_EMAIL_TO env vars; skipping.")
        return
    msg = EmailMessage()
    msg["From"] = smtp_user
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)
    ctx = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=ctx)
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
    print("[email] Sent.")

def send_discord(message: str):
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("[discord] DISCORD_WEBHOOK_URL not set; skipping.")
        return
    try:
        r = requests.post(webhook, json={"content": message}, timeout=10)
        print(f"[discord] {r.status_code}")
    except Exception as e:
        print(f"[discord] error: {e}")

def main():
    if len(sys.argv)<2:
        print("Usage: python discord_email_alerts.py <json_report_path>")
        raise SystemExit(1)
    src = Path(sys.argv[1]); data = json.load(open(src,"r",encoding="utf-8"))
    subject = f"[Cookbook Alert] {src.stem}"
    body = json.dumps(data, indent=2)
    send_email(subject, body[:1900])
    send_discord(f"**{subject}**\n```json\n{body[:1800]}\n```" )

if __name__ == "__main__":
    main()
