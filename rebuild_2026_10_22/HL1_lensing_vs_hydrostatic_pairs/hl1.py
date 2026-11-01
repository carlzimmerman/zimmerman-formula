#!/usr/bin/env python3
"""HL1 (FROZEN_CRITERIA.md): M_WL, M_hydro, M_gas on one radius, Mahdavi+13. LITERATURE-INPUT bracket, never a framework grade.
    python3 hl1.py [--mutate]   kappa = 1/2 FITTED; not theory closed."""
import math, os, re, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(os.path.dirname(os.path.dirname(HERE)), "_external_data", "gs4", "mahdavi13", "x"); MUT = "--mutate" in sys.argv; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def rows(f): return [l for l in open(os.path.join(D, f)) if "&" in l and "\\\\" in l and "colhead" not in l and "multicolumn" not in l and not l.lstrip().startswith("%")]
def num(c):
    m = re.search(r"-?\d+\.?\d*", c.replace("$", "")); return float(m.group()) if m and "nodata" not in c else float("nan")
ZZ = {}
for l in rows("table1.tex"):
    c = l.split("&")
    if len(c) > 3: ZZ[c[0].strip()] = num(c[3])
R = []; skip = []; raw = rows("table2.tex")
for l in raw:
    c = l.split("&"); n = c[0].strip()
    if n not in ZZ or len(c) < 5: skip.append(n + " (no z or columns)"); continue
    a = [num(c[i]) for i in (1, 2, 3, 4)]
    if not all(np.isfinite(a)) or min(a) <= 0: skip.append(n + " (missing value)"); continue
    R.append((n, ZZ[n], *a))
P(f"HL1: {len(raw)} data rows, {len(R)} with M_WL, M_gas, M_hydro; skipped {skip}")
z, r5, mw, mg, mh = (np.array([q[i] for q in R]) for i in range(1, 6)); okk = True
H0 = 70e3 / 3.0857e22; G = 6.674e-11; rc = 3 * H0 ** 2 * (0.3 * (1 + z) ** 3 + 0.7) / (8 * math.pi * G); mx = 500 * rc * 4 / 3 * math.pi * (r5 * 3.0857e22) ** 3 / 1.989e44; k1 = float(np.median(np.abs(mx / mw - 1))); dk = mx / mw - 1; so = float(np.median(dk)); wd = float(np.percentile(dk, 84) - np.percentile(dk, 16)); P(f"K1 as frozen, median |diff| {k1:.4f} against 0.03: {'PASS' if k1 <= 0.03 else 'FAIL'}"); g_ = abs(so) <= 0.05 and wd <= 0.03; okk &= g_; P(f"K1 AMENDMENT A1: signed offset {so:+.4f}, 16-84 width {wd:.4f}: {'PASS' if g_ else 'FAIL'}")
g_ = len(R) + len(skip) == len(raw); okk &= g_; P(f"K2 rows accounted for: {'PASS' if g_ else 'FAIL'}")
if not okk: P("K FAILED: no verdict"); open(os.path.join(HERE, "hl1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1)
def bs(x, seed=1):
    r = np.random.default_rng([20261031, seed]); return float(np.std([np.median(x[r.integers(0, len(x), len(x))]) for _ in range(5000)], ddof=1))
L = np.log10(mw / mh); g = float(np.median(L)); s = bs(L)
def cl(g, s): return "NOT POWERED" if s > 0.04 else "NO GAP" if abs(g) <= 2 * s else "REVERSED" if g < -2 * s else "GAP AS LARGE" if abs(g - 0.12) <= 2 * s else "GAP SMALLER" if g + 2 * s < 0.12 else "GAP LARGER"
if MUT:
    L2 = np.log10(mh / mw); sh = np.log10(mw / np.random.default_rng(1).permutation(mh)); a = abs(np.median(L2) + g) < 1e-12; b = sh.std() > L.std(); P(f"MUTATE swap flips g: {'BITES' if a else 'FAIL'}; shuffle rms {L.std():.3f} -> {sh.std():.3f}: {'BITES' if b else 'FAIL'}"); open(os.path.join(HERE, "hl1_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if a and b else 1)
P(f"g = median log(M_WL/M_hydro) {g:+.3f} +- {s:.3f}, mean {L.mean():+.3f}, rms {L.std():.3f}, n {len(L)}: {cl(g, s)}")
C0 = cl(g, s); Cs = {cl(g - 0.014, s), cl(g + 0.014, s), C0}; TAGC = C0 + (" [OFFSET-DEPENDENT]" if len(Cs) > 1 else ""); P(f"class, conditional on AMENDMENT A1: {TAGC} (g-0.014 {cl(g - 0.014, s)}, g+0.014 {cl(g + 0.014, s)})")
RES = dict(cls_a1=TAGC, n=len(L), g=g, se=s, cls=cl(g, s), mean=float(L.mean()), rms=float(L.std()))
for fs in (0.034, 0.0615):
    a = np.log10(mg * (1 + fs) / mw / 0.15945); b = np.log10(mg * (1 + fs) / mh / 0.15945); P(f"f* {fs}: log Y_WL {np.median(a):+.3f} +- {bs(a, 2):.3f}, log Y_hyd {np.median(b):+.3f} +- {bs(b, 3):.3f}"); RES[f"Y_{fs}"] = [float(np.median(a)), bs(a, 2), float(np.median(b)), bs(b, 3)]
for lab, v in (("M_WL", mw), ("z", z)):
    m = np.median(v)
    for t, sel in (("above", v >= m), ("below", v < m)): P(f"  {lab} {t} {m:.3g}: n {sel.sum()}, g {np.median(L[sel]):+.3f} +- {bs(L[sel], 4):.3f}, log Y_WL(f* 0.034) {np.median(np.log10(mg[sel] * 1.034 / mw[sel] / 0.15945)):+.3f}")
json.dump(RES, open(os.path.join(HERE, "hl1_results.json"), "w"), indent=1); open(os.path.join(HERE, "hl1.out"), "w").write("\n".join(OUT) + "\n")
