#!/usr/bin/env python3
"""extract_rc100_journal_col6.py -- column 6 (SED stellar mass, log M*/Msun) of Table B1 of the JOURNAL version of RC100
(Nestor Shachar et al. 2023, ApJ 944:78, doi 10.3847/1538-4357/aca9cf), read from the publisher's PDF.

v3.3 (CFG310 #4).  The published-table CSV of CFG305 carries no stellar-mass column, and the native RC100 route of the paper
uses CFG303's transcription of column 6 from the arXiv-v1 raster.  This script reads the journal PDF's text layer
(pdftotext -layout), takes for each of the 100 rows the number printed immediately before the 'log M_baryon (err)' and
'log M_bulge (err)' pairs, and writes real_research/data/rc100_nestorshachar2023_tableB1_logMstar_JOURNAL.csv.
paper_numbers.py (check S5t) compares that file, row by row, with CFG303's transcription.

The PDF is NOT part of the repository (publisher's copyright); pass its path as the only argument:
    python3 extract_rc100_journal_col6.py /path/to/the/journal/pdf
Only the 100 numbers are written."""
import os, re, sys, csv, subprocess, tempfile, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUTCSV = os.path.join(ROOT, "real_research", "data", "rc100_nestorshachar2023_tableB1_logMstar_JOURNAL.csv")

if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
    sys.exit("usage: extract_rc100_journal_col6.py <journal PDF of ApJ 944:78>")
with tempfile.TemporaryDirectory() as td:
    txt = os.path.join(td, "layout.txt")
    subprocess.run(["pdftotext", "-layout", sys.argv[1], txt], check=True)
    L = open(txt, encoding="utf-8").read().splitlines()
sha = hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest()
start = [i for i, l in enumerate(L) if "Table B1" in l][1]          # the first hit is the text that announces the table
# optional page number, the row index, ..., M* (int or decimal), log M_baryon (err), log M_bulge (err)
pat = re.compile(r"^\s*(?:\d{1,2}\s+)?(\d{1,3})\s+.*?\s(\d+(?:\.\d+)?)\s+(\d+\.\d+) \((\d\.\d+)\)\s+(\d+\.\d+) \((\d\.\d+)\)")
rows = {}
for l in L[start:]:
    m = pat.match(l)
    if m and 1 <= int(m.group(1)) <= 100 and int(m.group(1)) not in rows:
        rows[int(m.group(1))] = (m.group(2), m.group(3))
missing = sorted(set(range(1, 101)) - set(rows))
if missing:
    sys.exit(f"FAIL: rows not parsed: {missing}")
with open(OUTCSV, "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["idx", "logMstar_journal", "logMbaryon_journal"])
    for i in range(1, 101):
        w.writerow([i, rows[i][0], rows[i][1]])
print(f"wrote {os.path.relpath(OUTCSV, ROOT)}: 100 rows (source PDF sha256 {sha})")
