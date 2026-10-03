#!/usr/bin/env python3
"""CFG315 POST HOC (labelled; written after the frozen main and MUTATE runs; changes no frozen verdict).
Diagnoses the three failed gated controls:
  P1  C5: the law's deviation from the deep-MOND SIS asymptote as a function of g_bar (was the 5% at g_bar = 1e-12 a mis-specified threshold?)
  P2  MUTATE: the KiDS amplitude ratio moved from 0.914 to 1.096, i.e. by x1.199; S2 p as a function of the KiDS scale factor,
      including the factor that puts KiDS 20% ABOVE the others (1.2 / 0.914), i.e. the power of S2 against a net survey offset.
  P3  C2: how much of the relabelled S2 excess is the total (within-survey) scatter: relabelling with the covariance inflated by s1^2.
Run from the repository root:  python3 campaign_fresh_gravity/CFG315_desi_dr1_lensing/cfg315_posthoc.py
"""
import os, sys, io, math, contextlib
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "cfg315_run.py")).read()
cut = src.index("# ------------------------------------------------------------------ (a)")
g = {"__file__": os.path.join(HERE, "cfg315_run.py"), "__name__": "cfg315"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], "cfg315_run", "exec"), g)
lines = []


def P(s=""):
    print(s); lines.append(s)


P(__doc__.split("Run from")[0].strip())
C, DATA, run_a, kids_ratio, BGS = g["C"], g["DATA"], g["run_a"], g["kids_ratio"], g["BGS"]

# src of the projector/law (defined after the cut) -- re-exec just those functions
fsrc = src[src.index("G_SI, MSUN, MPC = 6.67430e-11"):src.index('P("\\n== C4 / C5')]
exec(compile(fsrc, "cfg315_law", "exec"), g)
project = g["project"]; G_SI, MSUN, MPC = g["G_SI"], g["MSUN"], g["MPC"]

P("\n== P1: law / SIS-asymptote vs g_bar (untruncated law, canonical, M_b = 1e10 and 1e11)")
RG3 = np.geomspace(1e-6, 600.0, 4000)
for gg in (1e-12, 1e-13, 1e-14):
    devs = []
    for Mb in (1e10, 1e11):
        a0 = C.A0["canonical"]
        Rp = math.sqrt(G_SI * Mb * MSUN / gg) / MPC
        ML = np.asarray(C.M_law(Mb, RG3, a0, C.nu_mono), float)
        ds = project(RG3, ML - Mb, np.array([Rp]))[0] + Mb / (math.pi * Rp ** 2)
        sis = math.sqrt(Mb * a0 / C.GMPC) / (4 * Rp)
        devs.append(ds / sis - 1)
    y = gg / C.A0_SI["canonical"]
    P(f"  g_bar {gg:.0e} (y = {y:.2e}): law/SIS - 1 = {devs[0]:+.4f}, {devs[1]:+.4f}; leading correction ~ (pi/4+1/2...) sqrt(y) scale: sqrt(y) = {math.sqrt(y):.3f}")

P("\n== P2: S2 (pooled BGS small scales) vs the KiDS scale factor")
orig = {k: (v["ds"].copy(), v["mb"].copy()) for k, v in DATA.items()}
for f in (0.8, 0.9, 1.0, 1.1, 1.2, 1.2 / 0.914, 1.4):
    for k, v in DATA.items():
        v["ds"] = orig[k][0] * (f if k[1] == "KiDS" else 1.0)
    res, tot = run_a("small", BGS, "gls")
    kr = kids_ratio(res)
    P(f"  KiDS x {f:.3f}: S2 chi2 {tot['chi2']:.2f}/6 p {tot['p2']:.2e}; S1 p {tot['p1']:.2e}; KiDS/(DES,HSC) {kr[0]:.3f} +- {kr[1]:.3f}")
for k, v in DATA.items():
    v["ds"] = orig[k][0]

P("\n== P3: C2 relabelling with Cov(A) inflated by the observed s1^2 (is the false-flag rate the within-survey excess?)")
res, tot = run_a("small", BGS, "gls")
s1sq = tot["s1"][0] ** 2
rng = np.random.default_rng(316)
base = {}
for L in BGS:
    d, Cs, keys, m = g["build"](L, "small")
    A, CA, sj, t = g["amplitudes"](d, Cs, keys, m, "gls")
    base[L] = (A, CA * s1sq, keys)
flags = 0
for it in range(2000):
    chi = 0.0
    for L in BGS:
        A, CA, keys = base[L]
        perm = rng.permutation(len(keys))
        kp = [(keys[i][0], keys[perm[i]][1], keys[i][2]) for i in range(len(keys))]
        chi += g["between"](A, CA, kp)[3]
    flags += stats.chi2.sf(chi, 6) < 0.01
P(f"  s1^2 = {s1sq:.3f}; relabelled false-flag rate with inflated covariance {flags / 2000:.3f} (frozen C2 threshold 0.05; uninflated 0.116)")
open(os.path.join(HERE, "cfg315_posthoc.out"), "w").write("\n".join(lines) + "\n")
