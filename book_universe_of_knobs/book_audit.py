#!/usr/bin/env python3
"""Audit for The Universe of Knobs. Exit 0 only if:
  1. every figure the text places exists, and every figure file is placed exactly once;
  2. every quoted number in the list below appears both in the book's text and in the source paper it is quoted from;
  3. no DOI placeholder is left in the front matter.
Run: python3 book_audit.py"""
import glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
FC = os.path.join("..", "qwen_claude_field_theory", "papers_2026", "LCDM_FRIED_CHICKEN", "lcdm_fried_chicken.tex")
P67 = os.path.join("..", "qwen_claude_field_theory", "papers_2026", "PAPER67_galaxy_law_and_what_it_leaves_2026.tex")

book = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob("*.tex")))
src = {"FC": open(FC, encoding="utf-8").read(), "P67": open(P67, encoding="utf-8").read()}
fails = []

# 1. figures
placed = re.findall(r"\\fig(?:\[[^\]]*\])?\{([A-Za-z0-9_]+)\}", book) + re.findall(r"figures/([A-Za-z0-9_]+)\.pdf", book)
files = {os.path.splitext(os.path.basename(f))[0] for f in glob.glob("figures/*.pdf")}
for name in set(placed):
    if name not in files:
        fails.append(f"figure placed but missing: {name}")
for name in files:
    if placed.count(name) != 1:
        fails.append(f"figure {name} placed {placed.count(name)} times")

# 2. quoted numbers: (book string, source key, source string)
QUOTES = [
    ("0.0415", "FC", "0.0415"), ("0.0445", "FC", "0.0445"), ("0.1951", "FC", "0.1951"), ("0.1953", "FC", "0.1953"),
    ("0.0275", "FC", "0.0275"), ("0.1933", "FC", "0.1933"), ("0.0152", "FC", "0.0152"), ("9.331", "FC", "9.331"),
    ("15.76", "FC", "15.76"), ("1066", "FC", "1066"), ("3373", "FC", "3373"), ("0.0392", "FC", "0.0392"),
    ("0.0252", "FC", "0.0252"), ("0.0222", "FC", "0.0222"), ("199,584", "FC", "199584"), ("62.1", "FC", "62.1"),
    ("17804.6", "FC", "17804.6"), ("19744.2", "FC", "19744.2"), ("154 of 171", "FC", "154 of 171"),
    ("1.1\\times10^{-5}", "FC", "1.1\\times10^{-5}"), ("0.461", "FC", "0.461"), ("3.432", "FC", "3.432"),
    ("1.404", "FC", "1.404"), ("0.1941", "FC", "0.1941"), ("276.1", "FC", "276.1"), ("145.2", "FC", "145.2"),
    ("69.6", "FC", "69.6"), ("5.01", "FC", "5.014"), ("0.398", "FC", "0.398"), ("61.6", "FC", "61.6"),
    ("+0.101", "FC", "+0.101"), ("0.516", "FC", "0.516"), ("9.2 and 13.7", "FC", "9.2 and 13.7"),
    ("0.0541", "P67", "0.0541"), ("9.3603", "P67", "9.3603"), ("1.1312", "P67", "1.1312"), ("1.0766", "P67", "1.0766"),
    ("63.90", "P67", "63.90"), ("2.93", "P67", "2.93"), ("1.91", "P67", "1.91"), ("0.0887", "P67", "0.0887"),
    ("5.22", "P67", "5.22"), ("0.593", "P67", "0.593"), ("0.277", "P67", "0.277"), ("1.239", "P67", "1.239"),
    ("4.8\\times10^7", "P67", "4.8\\times10^7"), ("5.1\\times10^{-32}", "P67", "5.1e-32"),
    ("0.91 [0.76, 1.03]", "P67", "0.91 [0.76, 1.03]"), ("3.49", "P67", "3.49"), ("2.38^{+0.12}_{-0.10}", "P67", "2.38^{+0.12}_{-0.10}"),
    ("1.59\\pm0.10", "P67", "1.59\\pm0.10"), ("+0.570\\pm0.094", "P67", "+0.570\\pm0.094"), ("1.149", "P67", "1.149"),
    ("13.29", "P67", "13.29"), ("0.90\\pm0.21", "P67", "0.90\\pm0.21"), ("550", "P67", "550"), ("41 galaxies", "P67", "41 galaxies"),
    ("289 match", "P67", "289 match"), ("-0.016\\pm0.061", "P67", "-0.016\\pm0.061"),
]
for b, key, s in QUOTES:
    if b not in book:
        fails.append(f"quote not in book: {b}")
    if s not in src[key]:
        fails.append(f"quote not in {key}: {s}")

# 3. DOI placeholder
if re.search(r"zenodo\.X+", book):
    fails.append("DOI placeholder left in the text")

for f in fails:
    print("FAIL:", f)
print(f"audit: {len(QUOTES)} quotes checked against the sources, {len(files)} figures; {len(fails)} failures")
sys.exit(1 if fails else 0)
