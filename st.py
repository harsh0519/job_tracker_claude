#!/usr/bin/env python3
"""st.py "<link substring>" "<status>" "<note>"  -- update status/note on matching applog rows."""
import os, sys, json, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
APPLOG = os.path.join(ROOT, "applog.jsonl")

def main():
    if len(sys.argv) < 3:
        sys.exit('usage: st.py "<link substring>" "<status>" "<note>"')
    sub, status = sys.argv[1].lower(), sys.argv[2]
    note = sys.argv[3] if len(sys.argv) > 3 else ""
    rows, n = [], 0
    with open(APPLOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if sub in (r.get("link", "") + " " + r.get("company", "")).lower():
                r["status"] = status
                if note:
                    r["notes"] = (r.get("notes", "") + " | " + note).strip(" |")
                n += 1
            rows.append(r)
    with open(APPLOG, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"updated {n} row(s) -> {status}")
    sync = os.path.join(ROOT, "sync.py")
    if os.path.exists(sync):
        subprocess.run([sys.executable, sync], check=False)

if __name__ == "__main__":
    main()
