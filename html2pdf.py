#!/usr/bin/env python3
"""html2pdf.py <input.html> [output.pdf]
Author a resume/cover-letter as HTML, convert to PDF with Python.
Uses headless Chrome (no LibreOffice/wkhtmltopdf needed on this Mac)."""
import os, sys, subprocess, time

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def html_to_pdf(src, out=None):
    src = os.path.abspath(src)
    if not os.path.exists(src):
        sys.exit(f"not found: {src}")
    if not out:
        out = os.path.splitext(src)[0] + ".pdf"
    out = os.path.abspath(out)
    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={out}", f"file://{src}",
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # chrome writes async-ish; wait briefly
    for _ in range(20):
        if os.path.exists(out) and os.path.getsize(out) > 0:
            break
        time.sleep(0.1)
    if not (os.path.exists(out) and os.path.getsize(out) > 0):
        sys.exit("PDF generation failed")
    print(f"{out} ({os.path.getsize(out)} bytes)")
    return out

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: html2pdf.py <input.html> [output.pdf]")
    html_to_pdf(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
