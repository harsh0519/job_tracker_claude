#!/usr/bin/env python3
"""log.py '<json>' -- append one application row to applog.jsonl, then sync the tracker.
Keys: date, platform, company, title, loc, mode, posted, link, resume, cover, status, contact, notes.
ALWAYS pass "date" (YYYY-MM-DD). Use a unique "link" per job."""
import os, sys, json, subprocess, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
APPLOG = os.path.join(ROOT, "applog.jsonl")

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: log.py '<json>'")
    row = json.loads(sys.argv[1])
    if not row.get("date"):
        sys.exit("ERROR: 'date' is required (YYYY-MM-DD). Refusing to log with a default date.")
    # validate date format
    datetime.date.fromisoformat(row["date"])
    with open(APPLOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"logged: {row.get('company','?')} | {row.get('title','')} | {row.get('status','')}")
    # rebuild tracker
    sync = os.path.join(ROOT, "sync.py")
    if os.path.exists(sync):
        subprocess.run([sys.executable, sync], check=False)

if __name__ == "__main__":
    main()
