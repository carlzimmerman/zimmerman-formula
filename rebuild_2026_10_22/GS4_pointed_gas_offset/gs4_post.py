#!/usr/bin/env python3
"""GS4 post-result audit, not graded: the low offset checked as hard as a high one. Reads gs4_matched.csv and the eRASS1 catalogue. kappa = 1/2 FITTED; not theory closed."""
import csv, os, math, sys
import numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
E = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data
R = list(csv.DictReader(open(os.path.join(HERE, "gs4_matched.csv"))))
for r in R:
    for k in ("j",): r[k] = int(r[k])
    for k in ("sep", "z", "lgM", "d", "d_own", "dlgR", "cts", "lgMgp"): r[k] = float(r[k])
def be(x):
    x = np.asarray(x); rng = np.random.default_rng(0); return float(np.median(x)), float(np.std(np.median(x[rng.integers(0, len(x), (5000, len(x)))], axis=1)))
def uniq(rows, key="d", noV=True):
    D = {}
    for r in rows:
        if noV and r["cat"] == "V09": continue
        D.setdefault(r["j"], []).append(r)
    return np.array([np.median([q[key] for q in L]) for L in D.values()]), np.array([L[0]["lgM"] for L in D.values()]), np.array([np.median([q["dlgR"] for q in L]) for L in D.values()])
v, m, dr = uniq(R); P(f"All masses, V09 out: N {len(v)}, median d {be(v)[0]:+.3f} +- {be(v)[1]:.3f}; slope {np.polyfit(m - 14.25, v, 1)[0]:+.3f}")
for a, b in ((12.5, 13.64), (13.64, 14.135), (14.135, 14.378), (14.378, 14.748), (14.748, 15.0), (15.0, 16)):
    s = (m >= a) & (m < b)
    if s.sum() > 1: P(f"  lg M500 {a}-{b}: N {s.sum()}, d {be(v[s])[0]:+.3f} +- {be(v[s])[1]:.3f}, own-radius d {be(uniq([r for r in R if a <= r['lgM'] < b], 'd_own')[0])[0]:+.3f}, median dlgR(eRASS - pub) {np.median(dr[s]):+.3f}")
    elif s.sum(): P(f"  lg M500 {a}-{b}: N 1, d {v[s][0]:+.3f}")
P("\nIn the range, each row, sorted by M500:")
inr = sorted([r for r in R if 4.4e13 <= 10 ** r["lgM"] <= 5.6e14], key=lambda r: r["lgM"])
for r in inr: P(f"  {r['cat']:4s} {r['name'][:18]:18s} {r['erass']} sep {r['sep']:.1f}' z {r['z']:.3f} lgM {r['lgM']:.2f} d {r['d']:+.3f} own {r['d_own']:+.3f} dlgR {r['dlgR']:+.3f} cts {r['cts']:.0f} PCONT {float(E['PCONT'][r['j']]):.2f} zt {str(E['BEST_Z_TYPE'][r['j']]).strip()}{' LENS' if r['inlens'] == 'True' else ''}")
open(os.path.join(HERE, "gs4_post.out"), "w").write("\n".join(OUT) + "\n")
