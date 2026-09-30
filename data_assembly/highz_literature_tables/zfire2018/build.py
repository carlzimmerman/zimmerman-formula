#!/usr/bin/env python3
"""ZFIRE z~2 COSMOS kinematics (Alcorn+2018, arXiv:1804.03669): Table 1 (morphology from F160W) and Table 3 (z, M*, SFR, V_2.2, sigma_g, j_disk per galaxy from HELA fits) parsed from the arXiv HTML fetched 2026-09-30.
One velocity per galaxy at 2.2 disc scale lengths; M* from SED; the paper estimates gas from SFR with a scaling (not a measured gas mass).  Nothing is recomputed."""
import sys, os, re, csv
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from tabutil import *
s = open(os.path.join(HERE, "..", "raw_small", "arxiv_1804.03669_html_fetched_2026-09-30.html"), errors="ignore").read()
T3 = []
for r in rows(s, "S4.T3.2")[1:]:
    if len(r) < 9 or not re.match(r"^\d+$", r[0].strip()): continue
    d = {"id": r[0].strip(), "date": r[1], "mask": r[2]}
    for k, nm in ((3, "z"), (4, "logMstar"), (5, "SFR"), (6, "V22_kms"), (7, "sigma_g_kms"), (8, "j_disk")):
        v, lo, hi, fl = val(r[k]); d[nm] = v; d[nm + "_err"] = lo
        if fl: d[nm + "_flag"] = fl
    T3.append(d)
T1 = []
for r in rows(s, "S2.T1.2")[1:]:
    if len(r) >= 7 and re.match(r"^\d+$", r[0].strip()):
        d = {"id": r[0].strip(), "field": r[1], "regular_irregular": r[2]}
        for k, nm in ((3, "Re_arcsec"), (4, "sersic_n"), (5, "axis_ratio"), (6, "PA_deg")):
            v, lo, hi, fl = val(r[k]); d[nm] = v
        T1.append(d)
write(os.path.join(HERE, "zfire_table3_kinematics.csv"), T3); write(os.path.join(HERE, "zfire_table1_morphology.csv"), T1)
msg = f"Table 3: {len(T3)} galaxies, z {min(d['z'] for d in T3):.2f}-{max(d['z'] for d in T3):.2f}, with V_2.2 for {sum(1 for d in T3 if d['V22_kms'] is not None)}; Table 1: {len(T1)} galaxies"
print(msg); open(os.path.join(HERE, "checks.txt"), "w").write(msg + "\n")
