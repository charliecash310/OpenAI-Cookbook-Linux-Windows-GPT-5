from __future__ import annotations
import os, sys, json
from pathlib import Path
from utils.common import write_json
try:
    from scapy.all import rdpcap
except Exception as e:
    rdpcap = None

def main():
    if len(sys.argv) < 2:
        print("Usage: python pcap_analyzer.py <pcap_file>")
        raise SystemExit(1)

    pcap_path = Path(sys.argv[1])
    if not pcap_path.exists():
        raise SystemExit(f"PCAP not found: {pcap_path}")

    if rdpcap is None:
        res = {"error":"Scapy not installed or not usable. Install with: pip install scapy"}
    else:
        pkts = rdpcap(str(pcap_path))
        total = len(pkts)
        protos = {}
        for p in pkts[:10000]:
            layer = p.summary().split()[0]
            protos[layer] = protos.get(layer, 0) + 1
        res = {"file": str(pcap_path), "packets": total, "top_layers": sorted(protos.items(), key=lambda x: x[1], reverse=True)[:10]}

    path = write_json(res, "reports/json/ch02_pcap_stats")
    print(f"Wrote {path}")

if __name__ == "__main__":
    main()
