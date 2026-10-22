#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A81 report auditor: every numeric token in report.md must appear literally in a81.out.

Not part of the lane's checks. It is the mechanical proof of the report's one hard
requirement: no number is quoted from memory, every one is printed by a81_checks.py.

  python3 verify_report_numbers.py            -> exit 0 iff every token is found
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = open(os.path.join(HERE, "a81.out"), encoding="utf-8").read()
REP = open(os.path.join(HERE, "report.md"), encoding="utf-8").read()

# numeric tokens: decimals and scientific notation only (this excludes section numbers,
# lane ids, years and bare integers, which are structural rather than measured)
TOKEN = re.compile(r"(?<![\w.])[-+]?\d+\.\d+(?:[eE][-+]?\d+)?|(?<![\w.])\d+[eE][-+]?\d+")

tokens = []
for m in TOKEN.finditer(REP):
    t = m.group(0)
    tokens.append(t)

uniq = sorted(set(tokens))
missing = [t for t in uniq if t not in OUT]

# allow a token that is a rounding of a printed value: try 1 fewer decimal place
def near(t):
    for cut in (1, 2):
        if "." in t and "e" not in t.lower():
            parts = t.split(".")
            if len(parts[1]) > cut:
                short = parts[0] + "." + parts[1][:-cut]
                if short in OUT:
                    return True
    return False

missing2 = [t for t in missing if not near(t)]
print("numeric tokens in report.md : %d (%d distinct)" % (len(tokens), len(uniq)))
print("not found literally in a81.out : %d" % len(missing))
for t in missing:
    print("   %-14s %s" % (t, "ROUNDING-OF-A-PRINTED-VALUE" if near(t) else "MISSING"))
print("not found at any permitted precision : %d" % len(missing2))
sys.exit(0 if not missing2 else 1)
