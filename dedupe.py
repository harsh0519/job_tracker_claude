#!/usr/bin/env python3
"""dedupe.py "<company>" [jobid-or-link]  -- check applog.jsonl before every submit.
Exit 0 and print MATCHES if the company (and/or job id) already appears; exit 1 if clear."""
import os, sys, json

ROOT = os.path.dirname(os.path.abspath(__file__))
APPLOG = os.path.join(ROOT, "applog.jsonl")

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: dedupe.py \"<company>\" [jobid-or-link]")
    company = sys.argv[1].lower().strip()
    jobid = sys.argv[2].lower().strip() if len(sys.argv) > 2 else None
    hits = []
    with open(APPLOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            blob = json.dumps(r, ensure_ascii=False).lower()
            comp_hit = company and company in (r.get("company", "") + " " + r.get("orig", "")).lower()
            job_hit = jobid and jobid in blob
            if comp_hit or job_hit:
                hits.append(r)
    if hits:
        print(f"MATCHES ({len(hits)}): already in log --")
        for r in hits[:10]:
            print(f"  [{r.get('date','?')}] {r.get('company','?')} | {r.get('title','')} | {r.get('status','')} | {r.get('notes','')[:40]}")
        sys.exit(0)
    print("CLEAR: no match in applog.jsonl")
    sys.exit(1)

if __name__ == "__main__":
    main()
