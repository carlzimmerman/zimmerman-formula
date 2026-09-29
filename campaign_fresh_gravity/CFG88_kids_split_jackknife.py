#!/usr/bin/env python3
"""CFG88 -- DOES THE KiDS EARLY/LATE SPLIT SURVIVE A DATA-DRIVEN COVARIANCE?  The split in CFG61's seven 1-halo bins (K1), scored
with the repo's own leave-one-patch-out jackknife covariance (50 sky patches) of its own June 2026 re-measurement from the KiDS-1000
catalogues, for B's colour-blind law (zero difference) and for CFG67's colour-split LCDM.

Criteria frozen and committed before any K1 number: campaign_fresh_gravity/CFG88_FROZEN_CRITERIA.md (7db367888).
  data     real_research/data/lensing_rar/lr_esd_jackknife.npz: the estimator sums (wgE, W, NN) per (patch, class, g_bar bin), 50 patches x
           2 classes (0 late, 1 early; u-r > 2.0) x 15 bins, built by real_research/reviews/lensing_rar/agentK_jackknife_stack.py from 181,477
           isolated lenses (lr_lenses.npz) and 21.3 M KiDS-1000 SOM-gold sources; ESD = sum wgE / sum W in Msun/pc^2 (the June convention).
  models   L (B's law, colour-blind): D = 0 (CFG61 C4 / CFG77: |D_L|/sigma < 3.3e-3; every colour-blind model's prediction).
           LCDM: D = me - ml from CFG67's committed results (built lens by lens from the same lr_lenses; amplitude 1, no refit).
  stat     K1 = [8..14]; C = the K1 block of Cd = (N-1)/N sum (D_(p) - Dbar)(D_(p) - Dbar)^T, N = 50; chi2 = D^T C^-1 D x h,
           h = (N - p - 2)/(N - 1) = 41/49 (Hartlap, p = 7); p-value from chi2 with 7 dof.
PRE-DECLARED (from the frozen file)
  C1  CONTROL  the June analysis reproduced from the per-patch sums (esd, d, all-15 chi2 raw 125.9599 / Hartlap 84.8301) to 1e-9 relative.
  C2  CONTROL  K1 = CFG61's committed K1; the June g_bar edges = CFG61's EDGES to 1e-12.
  C3  CONTROL  covariance calibration: 200 random halvings of the 50 patches (seed 88); for each, D_null = ESD_early(half A) -
               ESD_early(half B) on K1 with its own leave-one-patch-out covariance and Hartlap factor; mean chi2_null in [4.9, 9.1].
  H1  [HEADLINE; MUTATE must fail] the colour-blind zero model is rejected on K1 under the jackknife covariance: p < 0.0027.
  H2  CFG67's LCDM colour-split difference is consistent on K1 under the jackknife covariance: p > 0.01.
  R1-R7 (reported): raw and diagonal-only chi2; 25 merged patches; the error inflation to p = 0.0027 / 0.05; jackknife sigma vs
               Brouwer's released sigma in K1; all 15 bins; LCDM's best-fit amplitude; K1 with each bin dropped.
MUTATE=1: in each patch the early and late class sums are swapped with probability 1/2 (seed 88) before stacking -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG88_kids_split_jackknife.py   (MUTATE=1 for the control)
"""
import os, sys, json
import numpy as np
from scipy.stats import chi2 as CHI2, norm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG88_kids_split_jackknife", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: per-patch random early/late swap (p = 1/2, seed 88) -- H1 must FAIL ***")

LR = os.path.join(C.REPO, "real_research", "data", "lensing_rar")
J = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))
JA = np.load(os.path.join(LR, "lr_esd_jackknife_analysis.npz"))
KG = 1.989e30 / (3.0857e16) ** 2          # kg/m^2 per Msun/pc^2 (the June convention, agentK_jackknife_stack.py)
wgE0, W0 = J["wgE"].astype(float), J["W"].astype(float)
NP = wgE0.shape[0]
K1 = [8, 9, 10, 11, 12, 13, 14]
PK = len(K1)


def hartlap(n, p):
    return (n - p - 2) / (n - 1)


def pval(x, k):
    return float(CHI2.sf(x, k))


def zsig(p):
    return float(norm.isf(p / 2)) if p > 0 else float("inf")


def stack(wgE, W):
    """per-class ESD from the total sums, and the leave-one-patch-out ESDs (the June estimator)."""
    tg, tw = wgE.sum(0), W.sum(0)
    esd = tg / np.maximum(tw, 1e-300) / KG
    loo = (tg[None] - wgE) / np.maximum(tw[None] - W, 1e-300) / KG
    return esd, loo


def cov_diff(loo, idx):
    """leave-one-out covariance of the early-minus-late difference on the bins idx."""
    Dp = loo[:, 1, idx] - loo[:, 0, idx]
    Rd = Dp - Dp.mean(0)
    n = Dp.shape[0]
    return (n - 1) / n * (Rd.T @ Rd)


def chi2_of(D, Cm, h):
    return float(D @ np.linalg.solve(Cm, D)) * h


# ------------------------------------------------------------------ MUTATE: random per-patch class swap
wgE, W = wgE0.copy(), W0.copy()
if MUTATE:
    rng_m = np.random.default_rng(88)
    sw = rng_m.random(NP) < 0.5
    wgE[sw] = wgE0[sw][:, ::-1, :]
    W[sw] = W0[sw][:, ::-1, :]
    P(f"  MUTATE: {int(sw.sum())} of {NP} patches swapped")

# ================================================================== C1 / C2
R.banner("C1 / C2  CONTROLS")
esd0, loo0 = stack(wgE0, W0)
d0 = esd0[1] - esd0[0]
Cd0 = cov_diff(loo0, list(range(15)))
chi_all_raw = float(d0 @ np.linalg.solve(Cd0, d0))
chi_all_h = chi_all_raw * hartlap(NP, 15)
dev1 = max(float(np.max(np.abs(esd0 / JA["esd"] - 1))), float(np.max(np.abs(d0 / JA["d"] - 1))),
           abs(chi_all_raw / float(JA["chi2"]) - 1), abs(chi_all_h / float(JA["chi2_hartlap"]) - 1))
check("C1 CONTROL: the June analysis reproduced from the per-patch sums (esd, d, all-15 chi2 raw 125.9599 / Hartlap 84.8301) to 1e-9",
      f"all-15 chi2 raw {chi_all_raw:.4f} (June {float(JA['chi2']):.4f}), Hartlap {chi_all_h:.4f} (June {float(JA['chi2_hartlap']):.4f}); "
      f"max relative deviation {dev1:.1e}  [computed on the UNMUTATED sums]", dev1 < 1e-9)
k61 = json.load(open(os.path.join(HERE, "CFG61_kids_colour_split_results.json")))["numbers"]["K1"]
EDGES = np.logspace(np.log10(1e-15), np.log10(5e-12), 16)            # CFG61's EDGES, line 93
dev2 = float(np.max(np.abs(np.log10(J["gbar_edges"]) - np.log10(EDGES))))
check("C2 CONTROL: K1 = CFG61's committed K1; the June g_bar edges = CFG61's EDGES to 1e-12 (in log10)",
      f"K1 {K1} vs committed {k61}; max |d log10 edge| {dev2:.1e}", list(k61) == K1 and dev2 < 1e-12)

# ================================================================== the scored stack (mutated or not)
esd, loo = stack(wgE, W)
D = (esd[1] - esd[0])[K1]
CK = cov_diff(loo, K1)
H7 = hartlap(NP, PK)
g67 = json.load(open(os.path.join(HERE, "CFG67_lcdm_control_kids_split_results.json")))["numbers"]["lcdm"]
DL = (np.array(g67["me"]) - np.array(g67["ml"]))[K1]
P(f"\n  K1 g_bar centres (log10 m/s^2): {np.round(np.log10(np.sqrt(EDGES[K1] * EDGES[np.array(K1) + 1])), 2).tolist()}")
P(f"  measured early - late (Msun/pc^2): {np.round(D, 3).tolist()}")
P(f"  jackknife sigma of the difference:  {np.round(np.sqrt(np.diag(CK)), 3).tolist()}")
P(f"  LCDM (CFG67) early - late:          {np.round(DL, 3).tolist()}")
cor = CK / np.sqrt(np.outer(np.diag(CK), np.diag(CK)))
offd = cor[~np.eye(PK, dtype=bool)]
P(f"  jackknife correlation of the difference, off-diagonal: max |r| {np.max(np.abs(offd)):.2f}, mean r {np.mean(offd):+.2f}")

# ================================================================== C3: covariance calibration by random halvings of the early class
R.banner("C3  CONTROL: covariance calibration (random halvings of the patches, early class)")
rng = np.random.default_rng(88)
nulls = []
for t in range(200):
    perm = rng.permutation(NP)
    A, B = np.zeros(NP, bool), np.zeros(NP, bool)
    A[perm[:NP // 2]] = True
    B[perm[NP // 2:]] = True
    gA, wA = wgE[A, 1][:, K1].sum(0), W[A, 1][:, K1].sum(0)
    gB, wB = wgE[B, 1][:, K1].sum(0), W[B, 1][:, K1].sum(0)
    Dn = gA / wA / KG - gB / wB / KG
    reps = []
    for p in range(NP):
        if A[p]:
            ga, wa, gb, wb = gA - wgE[p, 1, K1], wA - W[p, 1, K1], gB, wB
        else:
            ga, wa, gb, wb = gA, wA, gB - wgE[p, 1, K1], wB - W[p, 1, K1]
        reps.append(ga / wa / KG - gb / wb / KG)
    reps = np.array(reps)
    Rr = reps - reps.mean(0)
    Cn = (NP - 1) / NP * (Rr.T @ Rr)
    nulls.append(chi2_of(Dn, Cn, H7))
nulls = np.array(nulls)
mnull = float(np.mean(nulls))
check("C3 CONTROL: covariance calibration -- the mean Hartlap chi2 of 200 random-halving nulls (early class, K1) lies in [4.9, 9.1] (7 +- 30%)",
      f"mean {mnull:.2f}, median {np.median(nulls):.2f}, 16-84% {np.percentile(nulls, 16):.2f}-{np.percentile(nulls, 84):.2f}; "
      f"fraction with p < 0.0027: {np.mean([pval(x, PK) < 0.0027 for x in nulls]):.3f}", 4.9 <= mnull <= 9.1)

# ================================================================== H1 / H2
R.banner("H1 / H2  THE SPLIT ON K1 UNDER THE JACKKNIFE COVARIANCE")
cL = chi2_of(D, CK, H7)
pL = pval(cL, PK)
cA = chi2_of(D - DL, CK, H7)
pA = pval(cA, PK)
check("H1 [HEADLINE] THE COLOUR-BLIND ZERO MODEL (B's law) IS REJECTED ON K1 UNDER THE JACKKNIFE COVARIANCE: p < 0.0027"
      + ("  [MUTATE: per-patch class swap]" if MUTATE else ""),
      f"chi2_L = {cL:.2f}/7 (Hartlap {H7:.3f}), p = {pL:.2e} ({zsig(pL):.2f} sigma); released-covariance value (CFG61) 28.1/7, p 2.1e-4", pL < 0.0027)
check("H2 CFG67's LCDM COLOUR-SPLIT DIFFERENCE IS CONSISTENT ON K1 UNDER THE JACKKNIFE COVARIANCE: p > 0.01",
      f"chi2_LCDM = {cA:.2f}/7, p = {pA:.3f}; released-covariance value (CFG67) 6.5/7, p 0.48", pA > 0.01)

# ================================================================== reported rows
R.banner("REPORTED ROWS")
rawL, rawA = cL / H7, cA / H7
dgL = float(np.sum(D ** 2 / np.diag(CK)))
dgA = float(np.sum((D - DL) ** 2 / np.diag(CK)))
check("R1 (reported) raw (no Hartlap) and diagonal-only chi2 on K1",
      f"L raw {rawL:.2f}, diag {dgL:.2f}; LCDM raw {rawA:.2f}, diag {dgA:.2f}", True, load_bearing=False)
g25 = np.add.reduceat(wgE, np.arange(0, NP, 2), axis=0)
w25 = np.add.reduceat(W, np.arange(0, NP, 2), axis=0)
_, loo25 = stack(g25, w25)
C25 = cov_diff(loo25, K1)
H25 = hartlap(25, PK)
c25L, c25A = chi2_of(D, C25, H25), chi2_of(D - DL, C25, H25)
check("R2 (reported) 25 merged patches (June's pairing; Hartlap N = 25, p = 7)",
      f"L {c25L:.2f}/7 (p {pval(c25L, PK):.2e}); LCDM {c25A:.2f}/7 (p {pval(c25A, PK):.3f})", True, load_bearing=False)
f3 = float(np.sqrt(cL / CHI2.isf(0.0027, PK))) if cL > CHI2.isf(0.0027, PK) else float("nan")
f5 = float(np.sqrt(cL / CHI2.isf(0.05, PK))) if cL > CHI2.isf(0.05, PK) else float("nan")
check("R3 (reported) the error inflation that brings L's Hartlap chi2 on K1 to p = 0.0027 and to p = 0.05",
      f"x {f3:.2f} (p = 0.0027), x {f5:.2f} (p = 0.05)  [CFG77, released covariance: x 1.5 gives p = 0.086]", True, load_bearing=False)
B21 = os.path.join(LR, "brouwer2021_rar")
rel = [np.loadtxt(os.path.join(B21, f"Fig-8_RAR-KiDS-isolated_Colorbin_{i}.txt")) for i in (1, 2)]
sig_rel = [r[:, 3] for r in rel]
sjk = [np.sqrt(np.diag(np.cov(np.concatenate([loo[:, 0, :], loo[:, 1, :]], axis=1).T, bias=True) * (NP - 1)))[i * 15:(i + 1) * 15]
       for i in (0, 1)]
ratio = [(sjk[i][K1] / sig_rel[i][K1]) for i in (0, 1)]
check("R4 (reported) jackknife sigma of each class vs Brouwer+2021's released sigma in K1 (plain ratio; samples differ: 181,477 vs 259,383 "
      "lenses, u-r 2.0 vs 2.5, isolation)",
      f"late: {np.round(ratio[0], 2).tolist()}; early: {np.round(ratio[1], 2).tolist()}; medians {np.median(ratio[0]):.2f} / "
      f"{np.median(ratio[1]):.2f}; sqrt(259383/181477) = {np.sqrt(259383 / 181477):.2f}", True, load_bearing=False)
Dall = esd[1] - esd[0]
Call = cov_diff(loo, list(range(15)))
DLall = np.array(g67["me"]) - np.array(g67["ml"])
aL, aA = chi2_of(Dall, Call, hartlap(NP, 15)), chi2_of(Dall - DLall, Call, hartlap(NP, 15))
check("R5 (reported) all 15 bins (the June number; the 2-halo bins are outside the isolation-reliable range and not modelled)",
      f"L {aL:.1f}/15 (p {pval(aL, 15):.1e}); LCDM {aA:.1f}/15 (p {pval(aA, 15):.1e})", True, load_bearing=False)
Ci = np.linalg.inv(CK)
Ahat = float(DL @ Ci @ D) / float(DL @ Ci @ DL)
sAh = float(1 / np.sqrt(DL @ Ci @ DL / H7))
cAb = chi2_of(D - Ahat * DL, CK, H7)
check("R6 (reported) LCDM with its best-fit amplitude on K1 under the jackknife covariance",
      f"A_hat = {Ahat:.3f} +- {sAh:.3f}; chi2 {cAb:.2f}/6 (p {pval(cAb, PK - 1):.3f})", True, load_bearing=False)
drops = []
for j in range(PK):
    keep = [K1[i] for i in range(PK) if i != j]
    Cj = cov_diff(loo, keep)
    drops.append(chi2_of((esd[1] - esd[0])[keep], Cj, hartlap(NP, PK - 1)))
check("R7 (reported) K1 with each bin dropped in turn (L, chi2/6, Hartlap p = 6)",
      "; ".join(f"drop {K1[j]}: {x:.1f} (p {pval(x, PK - 1):.1e})" for j, x in enumerate(drops)), True, load_bearing=False)

h1 = pL < 0.0027
c3 = 4.9 <= mnull <= 9.1
if not c3:
    reading = "the jackknife covariance fails its calibration null; H1 and H2 are non-diagnostic"
elif h1:
    reading = ("the 1-halo split's rejection of every colour-blind dark mass survives a covariance with cosmic variance and patch-level "
               "systematics; calibration systematics common to all patches, colour-class contamination and satellites remain open")
else:
    reading = "the 1-halo split is not robust under the data-driven covariance: B's one specific failure is downgraded"
P(f"\n    READING (declared): {reading}" + ("; LCDM's colour-split halos stay consistent" if pA > 0.01 else "; LCDM's colour-split halos do not fit either"))
R.num("K1", K1); R.num("D", D.tolist()); R.num("sigma_jk", np.sqrt(np.diag(CK)).tolist()); R.num("D_LCDM", DL.tolist())
R.num("chi2", dict(L=cL, LCDM=cA, L_raw=rawL, L_diag=dgL, L_25=c25L, LCDM_25=c25A, all15_L=aL, all15_LCDM=aA))
R.num("p", dict(L=pL, LCDM=pA)); R.num("null", dict(mean=mnull, median=float(np.median(nulls))))
R.num("R3_inflation", dict(p0027=f3, p05=f5)); R.num("R6", dict(A=Ahat, sA=sAh, chi2=cAb)); R.num("R7_drops", drops)
R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
