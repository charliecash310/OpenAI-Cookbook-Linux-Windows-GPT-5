from __future__ import annotations
import subprocess

ALLOWLIST = {"whoami","id","hostname","pwd","ls","echo","uname -a","ip a","ifconfig","cat /etc/os-release"}

def main():
    print("Kali Guidance Mode. Type a command or 'quit'. Allowed commands will execute; others are printed only.")
    while True:
        try:
            cmd = input("$ ").strip()
        except EOFError:
            break
        if cmd in {"quit","exit"}:
            break
        if not cmd:
            continue
        if cmd in ALLOWLIST:
            try:
                out = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                print(out.stdout or out.stderr)
            except Exception as e:
                print(f"[error] {e}")
        else:
            print(f"[guided only] {cmd} (not executed)")

if __name__ == "__main__":
    main()
