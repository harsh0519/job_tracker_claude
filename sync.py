#!/usr/bin/env python3
"""sync.py -- rebuild Job_Applications_Tracker.xlsx (Applications sheet) from applog.jsonl."""
import os, json
from openpyxl import Workbook
from openpyxl.styles import Font

ROOT = os.path.dirname(os.path.abspath(__file__))
APPLOG = os.path.join(ROOT, "applog.jsonl")
XLSX = os.path.join(ROOT, "Job_Applications_Tracker.xlsx")

COLS = ["#", "Date", "Platform", "Company", "Title", "Location", "Mode",
        "Posted", "Link", "Resume", "Cover Letter", "Status", "Follow-up", "Contact", "Notes"]

def main():
    rows = []
    if os.path.exists(APPLOG):
        for line in open(APPLOG, encoding="utf-8"):
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    wb = Workbook()
    ws = wb.active
    ws.title = "Applications"
    ws.append(COLS)
    for c in ws[1]:
        c.font = Font(bold=True)
    for i, r in enumerate(rows, 1):
        ws.append([i, r.get("date", ""), r.get("platform", ""), r.get("company", ""),
                   r.get("title", ""), r.get("loc", ""), r.get("mode", ""), r.get("posted", ""),
                   r.get("link", ""), r.get("resume", ""), r.get("cover", ""), r.get("status", ""),
                   r.get("followup", ""), r.get("contact", ""), r.get("notes", "")])
    wb.save(XLSX)
    applied = sum(1 for r in rows if r.get("status", "").lower().startswith("applied"))
    print(f"tracker rebuilt: {len(rows)} rows ({applied} Applied) -> {os.path.basename(XLSX)}")

if __name__ == "__main__":
    main()
