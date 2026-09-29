#!/usr/bin/env python3
"""CFG96 -- DO SATELLITES DRIVE THE KiDS EARLY/LATE SPLIT?  The June re-measurement's 1-halo split (CFG61's K1) re-stacked with stricter
isolation windows (|dchi| < 20 and < 30 Mpc; nested subsets of the June |dchi| < 10 sample), scored as in CFG88.

Criteria frozen and committed before any flag, stack or number: campaign_fresh_gravity/CFG96_FROZEN_CRITERIA.md (cb2876df0).
  inputs   CFG96_stage_stack.py's outputs (git-ignored): real_research/data/lensing_rar/cfg96_isoflags.npz (the W = 20 / 30 flags on the
           June lens list; C1) and cfg96_stack.npz (per-window sums per (patch, class, g_bar bin); C2 against lr_esd_jackknife.npz).
  stat     per window W: D_W = early - late ESD on K1; C_W its leave-one-patch-out covariance (50 June patches); zero-model chi2 =
           D_W^T C_W^-1 D_W x 41/49 (Hartlap); A_W = (D_10^T C_10^-1 D_W) / (D_10^T C_10^-1 D_10) with sigma_A from a JOINT
           leave-one-patch-out jackknife (both D_W and D_10 rebuilt without each patch).
PRE-DECLARED (from the frozen file)
  C1  CONTROL  the recomputed W = 10 isolated set reproduces lr_lenses.npz exactly (order and every column).
  C2  CONTROL  the W = 10 re-stack reproduces the June per-patch sums (wgE, W, NN) to 1e-9 relative, and the June patch labels exactly.
  C3  CONTROL  nesting: W = 30 within 20 within 10 (counts printed).
  H1  [HEADLINE; MUTATE must fail] at |dchi| < 20 Mpc the 1-halo split persists: the zero model is rejected on K1 at p < 0.0027 AND
      A_20 is within 2 sigma_A of 1.
  R1-R4 (reported): the same at |dchi| < 30 Mpc; class composition per window; per-bin D_W / D_10; all-15-bin zero-model chi2.
MUTATE=1: the early/late labels are swapped in the stricter windows' sums before scoring (D_W -> -D_W, A_W ~ -1) -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG96_kids_split_isolation.py   (MUTATE=1 for the control; needs CFG96_stage_stack.py's outputs)
"""
import os, sys
import numpy as np
from scipy.stats import chi2 as CHI2, norm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG96_kids_split_isolation", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: early/late labels swapped in the stricter windows' sums -- H1 must FAIL ***")

LR = os.path.join(C.REPO, "real_research", "data", "lensing_rar")
FLG = np.load(os.path.join(LR, "cfg96_isoflags.npz"))
STK = np.load(os.path.join(LR, "cfg96_stack.npz"))
J = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))
LN = np.load(os.path.join(LR, "lr_lenses.npz"))
KG = 1.989e30 / (3.0857e16) ** 2
K1 = [8, 9, 10, 11, 12, 13, 14]
PK, NPAT = len(K1), 50
HART = (NPAT - PK - 2) / (NPAT - 1)
WINS = (10, 20, 30)
S = {W: {k: STK[f"{k}_{W}"].astype(float) for k in ("wgE", "W", "NN")} for W in WINS}
if MUTATE:
    for W in (20, 30):
        for k in ("wgE", "W", "NN"):
            S[W][k] = S[W][k][:, ::-1, :].copy()


def esd_loo(W):
    g, w = S[W]["wgE"], S[W]["W"]
    tg, tw = g.sum(0), w.sum(0)
    return tg / tw / KG, (tg[None] - g) / (tw[None] - w) / KG


def pv(x, k=PK):
    return float(CHI2.sf(x, k))


def zs(p):
    return float(norm.isf(p / 2)) if p > 0 else float("inf")


# ================================================================== C1-C3
R.banner("C1-C3  CONTROLS")
n = FLG["n"]
check("C1 CONTROL: the recomputed |dchi| < 10 isolated set reproduces lr_lenses.npz exactly (order and every column)",
      f"stage verdict {bool(FLG['c1'])}; {int(n[0]):,} lenses vs lr_lenses {len(LN['ra']):,}", bool(FLG["c1"]) and int(n[0]) == len(LN["ra"]))
dev = max(float(np.max(np.abs(STK[f"{k}_10"] - J[k]) / np.maximum(np.abs(J[k]), 1e-300))) for k in ("wgE", "W", "NN"))
check("C2 CONTROL: the |dchi| < 10 re-stack reproduces the June per-patch sums (wgE, W, NN) to 1e-9 relative, and the June patch labels exactly",
      f"max relative deviation {dev:.1e}; patch labels equal: {bool(np.array_equal(STK['patch'], J['patch']))}",
      dev < 1e-9 and bool(np.array_equal(STK["patch"], J["patch"])))
f20, f30 = FLG["f20"], FLG["f30"]
nest = bool(np.all(f20[f30])) and int(f20.sum()) == int(n[1]) and int(f30.sum()) == int(n[2])
check("C3 CONTROL: nesting |dchi| < 30 within < 20 within < 10",
      f"counts 10: {int(n[0]):,}; 20: {int(n[1]):,} ({100 * n[1] / n[0]:.1f}%); 30: {int(n[2]):,} ({100 * n[2] / n[0]:.1f}%); nested {nest}", nest)

# ================================================================== per-window scores
E, LOO = {}, {}
for W in WINS:
    E[W], LOO[W] = esd_loo(W)
D = {W: (E[W][1] - E[W][0])[K1] for W in WINS}
DP = {W: LOO[W][:, 1, K1] - LOO[W][:, 0, K1] for W in WINS}
CW = {}
for W in WINS:
    Rd = DP[W] - DP[W].mean(0)
    CW[W] = (NPAT - 1) / NPAT * (Rd.T @ Rd)
X2 = {W: float(D[W] @ np.linalg.solve(CW[W], D[W])) * HART for W in WINS}
C10i = np.linalg.inv(CW[10])


def amp(d10, dw):
    return float(d10 @ C10i @ dw) / float(d10 @ C10i @ d10)


A, SA = {}, {}
for W in WINS:
    A[W] = amp(D[10], D[W])
    reps = np.array([amp(DP[10][p], DP[W][p]) for p in range(NPAT)])
    SA[W] = float(np.sqrt((NPAT - 1) / NPAT * np.sum((reps - reps.mean()) ** 2)))
R.banner("H1  THE SPLIT UNDER STRICTER ISOLATION (K1)")
for W in WINS:
    P(f"  |dchi| < {W:2d} Mpc: D = {np.round(D[W], 2).tolist()}; jackknife sigma {np.round(np.sqrt(np.diag(CW[W])), 2).tolist()}; "
      f"zero-model chi2 {X2[W]:.2f}/7 (p {pv(X2[W]):.2e}, {zs(pv(X2[W])):.2f} sigma); A = {A[W]:.3f} +- {SA[W]:.3f}")
za = (A[20] - 1) / SA[20] if SA[20] > 0 else float("nan")
check("H1 [HEADLINE] AT |dchi| < 20 Mpc THE 1-HALO SPLIT PERSISTS: zero model rejected on K1 at p < 0.0027 AND A_20 within 2 sigma of 1"
      + ("  [MUTATE: labels swapped]" if MUTATE else ""),
      f"chi2 {X2[20]:.2f}/7, p {pv(X2[20]):.2e} ({zs(pv(X2[20])):.2f} sigma); A_20 = {A[20]:.3f} +- {SA[20]:.3f} ((A-1)/sigma {za:+.2f}); "
      f"base (|dchi| < 10): {X2[10]:.2f}/7", pv(X2[20]) < 0.0027 and abs(za) < 2)

# ================================================================== reported rows
R.banner("REPORTED ROWS")
z30 = (A[30] - 1) / SA[30] if SA[30] > 0 else float("nan")
check("R1 (reported) the same at |dchi| < 30 Mpc",
      f"chi2 {X2[30]:.2f}/7, p {pv(X2[30]):.2e} ({zs(pv(X2[30])):.2f} sigma); A_30 = {A[30]:.3f} +- {SA[30]:.3f} ((A-1)/sigma {z30:+.2f})",
      True, load_bearing=False)
typ, Mg = LN["typ"], LN["Mgal"]
comp = []
for W, f in ((10, np.ones(len(typ), bool)), (20, f20), (30, f30)):
    e = f & (typ == 1); l = f & (typ == 0)
    comp.append(f"{W}: N {int(f.sum()):,}, early {100 * e.sum() / f.sum():.1f}%, median log M_gal early {np.median(np.log10(Mg[e])):.2f} / "
                f"late {np.median(np.log10(Mg[l])):.2f}")
check("R2 (reported) class composition per window", "; ".join(comp), True, load_bearing=False)
check("R3 (reported) per-bin D_W / D_10 on K1",
      "; ".join(f"{W}: {np.round(D[W] / D[10], 2).tolist()}" for W in (20, 30)), True, load_bearing=False)
x15 = {}
for W in WINS:
    d15 = E[W][1] - E[W][0]
    dp15 = LOO[W][:, 1, :] - LOO[W][:, 0, :]
    rd = dp15 - dp15.mean(0)
    c15 = (NPAT - 1) / NPAT * (rd.T @ rd)
    x15[W] = float(d15 @ np.linalg.solve(c15, d15)) * (NPAT - 15 - 2) / (NPAT - 1)
check("R4 (reported) all-15-bin zero-model chi2 per window (Hartlap p = 15)",
      "; ".join(f"{W}: {x15[W]:.1f}/15 (p {pv(x15[W], 15):.1e})" for W in WINS), True, load_bearing=False)

h1 = pv(X2[20]) < 0.0027 and abs(za) < 2
if h1:
    reading = "removing the lenses with a qualifying neighbour inside a twice-wider line-of-sight window leaves the split unchanged: satellites, as removed by this isolation, do not drive it"
elif za <= -2:
    reading = "the split shrinks under stricter isolation: satellite contamination contributes; it needs a quantified satellite model before the split counts against B"
else:
    reading = "the stricter sample cannot decide (lost power or an amplitude above 1); non-diagnostic for satellites"
P(f"\n    READING (declared): {reading}")
R.num("chi2", X2); R.num("A", A); R.num("sigmaA", SA); R.num("D", {W: D[W].tolist() for W in WINS}); R.num("all15", x15)
R.num("counts", [int(x) for x in n]); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
