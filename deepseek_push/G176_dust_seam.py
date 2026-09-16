#!/usr/bin/env python3
"""G176 -- THE DUST-SLOPE SEAM: ONE LAW WITH A TRANSITION, OR TWO DISJOINT LAWS?

THE QUESTION.  The committed record carries two dust-density indices from two
radial windows:
    * the INNER (coherency) window [0.1 R500, 600 kpc]:  p_dust = 1.69 +- 0.16
      (G139 V3, pooled rho_dust_req_A, positive bins);
    * the DEEP window (r_M, R500):                        p_dust = 2.38 +- 0.15
      (G108 V1, pooled d ln rho_dust/d ln r = -2.377 +- 0.152, fixed-A phantom).
G142's sub-window residuals demanded a slope BETWEEN 2.38 and 0.99 (the r^-1
coherency factor), ~1.5-2.0.  This lane asks the SEAM question: fit the
POOLED rho_dust,req(r) (G098's committed inversion, floor A) with a
TWO-INDEX model

        rho_dust = B r^-p1  for r < r_t
        rho_dust = B' r^-p2 for r > r_t      (continuous at r_t: B' = B r_t^(p2-p1))

and decide: is rho_dust ONE law with a boundary at r_t, or TWO disjoint laws?

  (1) THE SEAM FIT.  Pooled two-index fit on G098's committed
      rho_dust_req_A(r) over the union of the committed windows,
      r in [0.1 R500, R500], positive dust only: free r_t.  Report p1, p2,
      r_t + per-cluster amplitude offsets, and r_t vs the r_M-class
      (r_M = sqrt(G M_b(R500)/a0): 273-580 kpc, median ~402 kpc, G108/G075).
      Pooled GLOBAL r_t (one number for all clusters) AND per-cluster r_t
      (each cluster free): the per-cluster r_t,i vs r_M,i relation is V2.

  (2) THE ALTERNATIVES (model selection, all with per-cluster amplitudes):
      (a) two-index, r_t FREE (shape params B,p1,p2,r_t -> with 12 per-cluster
          amplitudes: k = 15);
      (b) single index rho = B r^-p (k = 13);
      (c) the r^-1.7 power EXACTLY (G139's committed claim) with the G108
          deep index -2.377 as a DIFFERENT regime, seam at the equilibrium
          boundary r_t = r_M per cluster (k = 12, fully committed) -- and the
          same committed indices with r_t FREE (k = 13);
      (d) ONE STEEPENING LAW: log rho = a_c + alpha log r + beta (log r)^2,
          smooth index p(r) = -alpha - 2 beta log r (k = 14).
      Compare by BIC and AICc on the same pooled data.

  (3) THE MEANING.  If r_t ~ r_M-class: the seam is the phantom/free-dust
      equilibrium boundary's own signature -- the same boundary the
      temperature ratio R and the cap mark -- and the honest statement is:
      the dust's SHAPE CHANGES at the equilibrium boundary; the streaming
      envelope transitions to the mixed interior there.  If r_t is
      unconstrained (flat likelihood in r_t): the two slopes are separate
      regimes of ONE steepening law rho ~ r^-p(r) smooth.

  (4) VERDICTS.
      V1  the p1/p2/r_t fit with the model comparison (BIC/AICc), numbers;
      V2  the seam's position vs r_M (pooled r_t vs median r_M; per-cluster
          r_t,i vs r_M,i; and DeltaBIC of the committed r_t = r_M seam);
      V3  the honest statement: ONE law with a boundary at r_t = X, or TWO --
          with the BIC that decides.

DELIVERABLE: deepseek_push/G176_dust_seam.py + .out + G176_results.json.

DATA (all committed, nothing written outside deepseek_push/):
G098_results.json per-cluster canonical arrays (r_kpc, rho_b, rho_res,
rho_ph_A, rho_dust_req_A, R500_kpc); G108_results.json (rM_kpc per cluster,
registered pooled deep-window envelope -2.377+-0.152); G122_results.json
(per-cluster a_c, rM_over_R500; p* = 0.99).  Rewrites NO committed file.
"""
import json
import os

import numpy as np

RES, NP, NF = [], 0, 0

G = 6.674e-11
A0_CANON = 9.3619e-11          # canonical committed footing (G098 9.3623e-11)
MSUN = 1.98892e30
KPC = 3.0857e19
P139_INNER, P108_DEEP = 1.69, 2.377   # committed window indices (G139, G108)


def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d:
        print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    NP, NF = NP + (1 if ok else 0), NF + (0 if ok else 1)


def info(*a):
    print(*a, flush=True)


print(__doc__)
print("=" * 100)
print("G176 -- THE DUST-SLOPE SEAM (pooled two-index fit on rho_dust_req_A)")
print("=" * 100)

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "G098_results.json")) as f:
    g098 = json.load(f)
with open(os.path.join(HERE, "G108_results.json")) as f:
    g108 = json.load(f)
with open(os.path.join(HERE, "G122_results.json")) as f:
    g122 = json.load(f)

canon = g098["per_cluster"]["canonical"]
CLS = sorted(canon.keys())
rM_kpc = {p["cluster"]: p["rM_kpc"] for p in g108["per_cluster"]}
amps_log10 = g122["closed_form_candidate"]["per_cluster_amp_log10"]
rM_over_R500 = {n: g122["properties"][n]["rM_over_R500"] for n in CLS}

info(f"clusters: {len(CLS)}; committed indices: inner p_dust = {P139_INNER} +- 0.16 "
     f"(G139 coherency window), deep p = -{P108_DEEP} +- 0.15 (G108 registered "
     f"-2.377 +- 0.152, fixed-A phantom); r_M range "
     f"{min(rM_kpc.values()):.0f}-{max(rM_kpc.values()):.0f} kpc, "
     f"median {float(np.median(list(rM_kpc.values()))):.0f}")

# ---------------------------------------------------------------- pooled data
# G098's committed inversion rho_dust_req_A, positive bins only, r in
# [0.1 R500, R500] (union of the coherency and deep windows).
P = []                       # (name, r_kpc, log10 r, log10 rho_dust)
for name in CLS:
    c_ = canon[name]
    r = np.array(c_["r_kpc"], float)
    rd = np.array(c_["rho_dust_req_A_Msun_kpc3"], float)
    R500 = c_["R500_kpc"]
    m = (r >= 0.1 * R500) & (r <= R500) & (rd > 0)
    for ri, rdi in zip(r[m], rd[m]):
        P.append((name, ri, np.log10(ri), np.log10(rdi)))
NM = np.array([p[0] for p in P])
R = np.array([p[1] for p in P])
LR = np.array([p[2] for p in P])
LY = np.array([p[3] for p in P])
LG = np.array([np.log10(rM_kpc[n]) for n in NM])       # per-bin log10 r_M
LI = np.array([np.log10(0.1 * canon[n]["R500_kpc"]) for n in NM])
info(f"pooled positive-dust bins on [0.1 R500, R500]: n = {len(P)}; "
     f"r in [{R.min():.0f}, {R.max():.0f}] kpc")

# ------------------------------------------------- GATES: reproduce the two
# registered window indices on the SAME committed ingests.
def ols(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 3:
        return np.nan, np.nan, 0
    A = np.vstack([x, np.ones_like(x)]).T
    with np.errstate(all="ignore"):
        cf, *_ = np.linalg.lstsq(A, y, rcond=None)
        rms = float(np.sqrt(np.mean((y - A @ cf) ** 2)))
    return float(cf[0]), rms, int(len(x))


def win_mask(name, lo, hi):
    c_ = canon[name]
    r = np.array(c_["r_kpc"], float)
    return (r >= lo) & (r <= hi)


# GATE 1: G139 coherency window [0.1 R500, 600 kpc], single-amplitude pooled
# slope on rho_dust_req_A (>0).  Expected p_dust = 1.69, rms 0.159, n = 1039.
gr, gy = [], []
for name in CLS:
    c_ = canon[name]
    r = np.array(c_["r_kpc"], float)
    rd = np.array(c_["rho_dust_req_A_Msun_kpc3"], float)
    m = win_mask(name, 0.1 * c_["R500_kpc"], 600.0) & (rd > 0)
    gr.extend(np.log10(r[m])); gy.extend(np.log10(rd[m]))
p_coh, rms_coh, n_coh = ols(gr, gy)
info("")
info(f"GATE1 [G139 reproduction] coherency window [0.1R500, 600 kpc]: "
     f"p_dust = {-p_coh:.3f} (rms {rms_coh:.3f} dex, n = {n_coh}); "
     f"registered 1.69 +- 0.16 (rms 0.159, n = 1039)")
check("GATE1 [G139 reproduction] the pooled single-amplitude slope on "
      "rho_dust_req_A over the coherency window reads p_dust ~ 1.7 "
      "(within 0.1 of 1.69), n ~ 1039",
      f"p_dust = {-p_coh:.3f} +- (rms {rms_coh:.3f}), n = {n_coh}",
      abs(-p_coh - P139_INNER) < 0.10 and abs(n_coh - 1039) <= 8)

# GATE 2: G108 deep-window envelope on (r_M, R500) with the FIXED-A phantom,
# p = 2.314 in G139's fixed-A convention (G108 registered -2.377 +- 0.152).
def cum_mass(r_kpc, rho):
    """enclosed mass Msun from the committed density arrays (trapezoid),
    same convention as G139."""
    r = np.asarray(r_kpc, float)
    rho = np.asarray(rho, float)
    dV = 4.0 * np.pi * r ** 2
    dr = np.diff(r)
    m = np.concatenate([[0.0], np.cumsum(0.5 * (dV[1:] + dV[:-1]) * dr
                                         * 0.5 * (rho[1:] + rho[:-1]))])
    return m[:len(r)]


gr2, gy2 = [], []
for name in CLS:
    c_ = canon[name]
    r = np.array(c_["r_kpc"], float)
    rho_tot = np.array(c_["rho_tot_Msun_kpc3"], float)
    rho_b = np.array(c_["rho_b_Msun_kpc3"], float)
    m = win_mask(name, rM_kpc[name], c_["R500_kpc"])
    mb = cum_mass(r, rho_b)
    mb500 = float(np.interp(c_["R500_kpc"], r, mb))
    A = np.sqrt(G * mb500 * MSUN * A0_CANON) / (4.0 * np.pi * G)      # kg/m
    rph_fixed = (A / (r * KPC) ** 2) / (MSUN / KPC ** 3)             # Msun/kpc^3
    rd = rho_tot - rho_b - rph_fixed
    mm = m & (rd > 0)
    gr2.extend(np.log10(r[mm])); gy2.extend(np.log10(rd[mm]))
p_dp, rms_dp, n_dp = ols(gr2, gy2)
info(f"GATE2 [G108 reproduction] deep window (r_M, R500), fixed-A phantom: "
     f"p = {-p_dp:.3f} (rms {rms_dp:.3f} dex, n = {n_dp}); "
     f"registered -2.377 +- 0.152 (n = 258)")
check("GATE2 [G108 reproduction] the fixed-A deep-window slope reproduces "
      "G108's registered -2.377 (within 0.15, the registered error)",
      f"p = {-p_dp:.3f}, n = {n_dp}", abs(-p_dp - P108_DEEP) < 0.15)

# GATE 2b: the SAME deep window on the PER-BIN floor-A phantom (rho_dust_req_A,
# the very data the seam is fit on): G139's row reads p = 2.785 there.
gr3, gy3 = [], []
p2_deep_floorA = np.nan
for name in CLS:
    c_ = canon[name]
    r = np.array(c_["r_kpc"], float)
    rd = np.array(c_["rho_dust_req_A_Msun_kpc3"], float)
    m = win_mask(name, rM_kpc[name], c_["R500_kpc"]) & (rd > 0)
    gr3.extend(np.log10(r[m])); gy3.extend(np.log10(rd[m]))
p_dpf, rms_dpf, n_dpf = ols(gr3, gy3)
p2_deep_floorA = float(-p_dpf)
info(f"GATE2b [per-bin floor-A deep slope] deep window (r_M, R500) on "
     f"rho_dust_req_A: p = {p2_deep_floorA:.3f} (rms {rms_dpf:.3f}, n = {n_dpf}); "
     f"G139's row 2.785 (the seam data's own convention)")
check("GATE2b [per-bin floor-A deep slope] reproduces G139's per-bin phantom "
      "deep-window slope 2.785 (within 0.15)",
      f"p = {p2_deep_floorA:.3f}, n = {n_dpf}",
      abs(p2_deep_floorA - 2.785) < 0.15)

# ------------------------------------------------------- DESIGN MATRICES for
# the candidate models.  All models get a per-cluster amplitude offset a_c
# (G122/G139's committed per-cluster freedom) plus the shared shape params.
def design_amp(n_cls, names):
    """per-cluster indicator columns."""
    cols = []
    for i, nm in enumerate(n_cls):
        cols.append((names == nm).astype(float))
    return np.vstack(cols).T                      # n x n_cls


def fit_linear(X, y):
    with np.errstate(all="ignore"):
        cf, *_ = np.linalg.lstsq(X, y, rcond=None)
        r = y - X @ cf
        s = float(r @ r)
    return cf, s, r                     # coefs, SSE, residuals


DAMP = design_amp(CLS, NM)
n = len(LY)

# (b) SINGLE INDEX: log rho = a_c - p log r.
Xs = np.hstack([DAMP, -LR[:, None]])
cf_s, sse_s, _ = fit_linear(Xs, LY)
k_s = DAMP.shape[1] + 1

# TWO-INDEX (a): log rho = a_c - p1 (log r - log r_t)_- - p2 (log r - log r_t)_+
# continuous at r_t; grid log r_t then refine.  Shape params p1, p2, log r_t.
LG_LO, LG_HI = LR.min(), LR.max()


def two_idx_design(lgt):
    z = LR - lgt
    zl = np.minimum(z, 0.0)
    zu = np.maximum(z, 0.0)
    return np.hstack([DAMP, -zl[:, None], -zu[:, None]])


def sse_two(lgt):
    z = LR - lgt
    if (z < 0).sum() < 5 or (z > 0).sum() < 5:
        return np.inf
    cf, s, _ = fit_linear(two_idx_design(lgt), LY)
    return s


def solve_two(lgt):
    cf, s, _ = fit_linear(two_idx_design(lgt), LY)
    return cf, s


# coarse grid then a parabolic/ternary refine
grid = np.linspace(LG_LO + 1e-6, LG_HI - 1e-6, 601)
sses = np.array([sse_two(g) for g in grid])
i0 = int(np.argmin(sses))
# refine (golden-section style scan on a fine window)
lo, hi = grid[max(0, i0 - 2)], grid[min(len(grid) - 1, i0 + 2)]
for _ in range(80):
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    if sse_two(m1) < sse_two(m2):
        hi = m2
    else:
        lo = m1
lgt_best = (lo + hi) / 2
cf_a, sse_a = solve_two(lgt_best)
k_a = DAMP.shape[1] + 3          # a_c (12) + p1 + p2 + log r_t
p1_fit, p2_fit = float(cf_a[-2]), float(cf_a[-1])
r_t_fit = float(10 ** lgt_best)
# parameter standard errors from (X^T X)^-1 s^2 for the linear params p1, p2
Xa = two_idx_design(lgt_best)
s2l = sse_a / (n - k_a)
try:
    cov = np.linalg.inv(Xa.T @ Xa) * s2l
    se_p1, se_p2 = float(np.sqrt(cov[-2, -2])), float(np.sqrt(cov[-1, -1]))
except Exception:
    se_p1, se_p2 = np.nan, np.nan
info("")
info(f"SEAM FIT (model a, r_t free, continuous two-index, per-cluster amps):")
info(f"   p1 = {p1_fit:.3f} +- {se_p1:.3f}   p2 = {p2_fit:.3f} +- {se_p2:.3f}   "
     f"r_t = {r_t_fit:.1f} kpc   "
     f"(SSE {sse_a:.4f} dex^2, n = {n}, k = {k_a})")
info(f"   r_M-class: [{min(rM_kpc.values()):.0f}, {max(rM_kpc.values()):.0f}] "
     f"kpc, median {float(np.median(list(rM_kpc.values()))):.0f} kpc; "
     f"r_t/r_M(median) = {r_t_fit / float(np.median(list(rM_kpc.values()))):.2f}")

# (c) COMMITTED TWO-REGIME: p1 = 1.69, p2 = 2.377 fixed; seam at r_t = r_M
# per cluster (the equilibrium boundary).  Only the 12 amplitudes are free.
zc = LR - np.log10(np.array([rM_kpc[nm] for nm in NM]))
f_shape = -P139_INNER * np.minimum(zc, 0.0) - P108_DEEP * np.maximum(zc, 0.0)
cf_c, sse_c, _ = fit_linear(DAMP, LY - f_shape)
k_c = DAMP.shape[1]

# (c') SAME committed indices, seam FREE (k = 13): where does the committed
# index pair want the boundary?
def sse_cp(lgt):
    z = LR - lgt
    if (z < 0).sum() < 5 or (z > 0).sum() < 5:
        return np.inf
    f = -P139_INNER * np.minimum(z, 0.0) - P108_DEEP * np.maximum(z, 0.0)
    _, s, _ = fit_linear(DAMP, LY - f)
    return s


sses_cp = np.array([sse_cp(g) for g in grid])
i1 = int(np.argmin(sses_cp))
lo, hi = grid[max(0, i1 - 2)], grid[min(len(grid) - 1, i1 + 2)]
for _ in range(80):
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    if sse_cp(m1) < sse_cp(m2):
        hi = m2
    else:
        lo = m1
lgt_cp = (lo + hi) / 2
zc2 = LR - lgt_cp
f_cp = -P139_INNER * np.minimum(zc2, 0.0) - P108_DEEP * np.maximum(zc2, 0.0)
cf_cp, sse_cp_best, _ = fit_linear(DAMP, LY - f_cp)
k_cp = DAMP.shape[1] + 1
r_t_cp = float(10 ** lgt_cp)
info(f"COMMITTED seam (model c'): p1 = 1.69, p2 = 2.377 fixed, seam FREE -> "
     f"r_t = {r_t_cp:.1f} kpc (SSE {sse_cp_best:.4f});  seam at r_M per cluster "
     f"(model c): SSE {sse_c:.4f}")

# (e) SEAM AT r_M PER CLUSTER, INDICES FREE: r_t = r_M,i (the equilibrium
# boundary), p1, p2 shared and free.  Direct test of the r_M hypothesis
# WITHOUT fixing the index values (k = 14).
Xe = np.hstack([DAMP, -np.minimum(zc, 0.0)[:, None],
                -np.maximum(zc, 0.0)[:, None]])
cf_e, sse_e, _ = fit_linear(Xe, LY)
k_e = DAMP.shape[1] + 2
p1_e, p2_e = float(cf_e[-2]), float(cf_e[-1])
info(f"SEAM AT r_M, indices free (model e): p1 = {p1_e:.3f}, p2 = {p2_e:.3f} "
     f"(SSE {sse_e:.4f}, k = {k_e}) -- the equilibrium-boundary seam, shape free")

# (d) ONE STEEPENING LAW: log rho = a_c + alpha log r + beta (log r)^2.
Xq = np.hstack([DAMP, LR[:, None], LR[:, None] ** 2])
cf_q, sse_q, _ = fit_linear(Xq, LY)
k_q = DAMP.shape[1] + 2
alpha_q, beta_q = float(cf_q[-2]), float(cf_q[-1])
info(f"STEEPENING LAW (model d): alpha = {alpha_q:.3f}, beta = {beta_q:.4f} "
     f"-> p(r) = -alpha - 2 beta log r: p(200 kpc) = "
     f"{-alpha_q - 2 * beta_q * np.log10(200):.2f}, p(600 kpc) = "
     f"{-alpha_q - 2 * beta_q * np.log10(600):.2f}, p(R500-median) = "
     f"{-alpha_q - 2 * beta_q * np.log10(1200):.2f} (SSE {sse_q:.4f})")

# --------------------------------------------------------- MODEL COMPARISON
# BIC = n ln(SSE/n) + k ln n ;  AICc = n ln(SSE/n) + 2k + 2k(k+1)/(n-k-1)
# (same n, same data -> constants drop out of the deltas).
def ic(SSE, k):
    bic = n * np.log(SSE / n) + k * np.log(n)
    aicc = n * np.log(SSE / n) + 2 * k + 2 * k * (k + 1) / max(1, n - k - 1)
    return bic, aicc


models = [
    ("(a) two-index, r_t free", sse_a, k_a, f"p1={p1_fit:.2f}, p2={p2_fit:.2f}, r_t={r_t_fit:.0f} kpc"),
    ("(b) single index", sse_s, k_s, f"p={-float(cf_s[-1]):.2f}"),
    ("(c) r^-1.7 EXACT + G108 deep, seam at r_M", sse_c, k_c, "p1=1.69, p2=2.377 committed, r_t=r_M per cluster"),
    ("(c') r^-1.7 EXACT + G108 deep, seam free", sse_cp_best, k_cp, f"p1=1.69, p2=2.377 committed, r_t={r_t_cp:.0f} kpc"),
    ("(d) smooth steepening log-quadratic", sse_q, k_q, f"alpha={alpha_q:.2f}, beta={beta_q:.3f}"),
    ("(e) seam at r_M per cluster, indices free", sse_e, k_e, f"p1={p1_e:.2f}, p2={p2_e:.2f}"),
]
info("")
info(f"MODEL COMPARISON on the same pooled data (n = {n}):")
info(f"  {'model':44s} {'k':>3s} {'SSE dex^2':>10s} {'rms dex':>8s} {'BIC':>9s} {'AICc':>9s} {'d_BIC':>7s} {'d_AICc':>7s}")
rows = []
best_bic = min(ic(m[1], m[2])[0] for m in models)
best_aicc = min(ic(m[1], m[2])[1] for m in models)
for name_, sse_, k_, desc_ in models:
    bic_, aicc_ = ic(sse_, k_)
    rms_ = np.sqrt(sse_ / n)
    rows.append((name_, k_, sse_, bic_, aicc_, desc_))
    info(f"  {name_:44s} {k_:3d} {sse_:10.3f} {rms_:8.3f} {bic_:9.1f} {aicc_:9.1f} "
         f"{bic_ - best_bic:7.1f} {aicc_ - best_aicc:7.1f}")
bic_min = min(r[3] for r in rows)
aicc_min = min(r[4] for r in rows)
winner_bic = [r for r in rows if abs(r[3] - bic_min) < 1e-9][0]
winner_aicc = [r for r in rows if abs(r[4] - aicc_min) < 1e-9][0]
info("")
info(f"BIC winner:  {winner_bic[0]}  (d_BIC vs runner-up = "
     f"{sorted(r[3] for r in rows)[1] - bic_min:.1f})")
info(f"AICc winner: {winner_aicc[0]}")

# ---------------------------------------------------- PER-CLUSTER SEAMS: the
# r_t,i vs r_M,i relation (V2).
info("")
info("PER-CLUSTER two-index fits (r_t free per cluster, own amplitude), "
     "r in [0.1 R500, R500], positive dust:")
info(f"  {'cluster':8s} {'r_M kpc':>8s} {'r_t kpc':>8s} {'r_t/r_M':>8s} {'p1':>6s} {'p2':>6s} {'n':>4s}")
pc_seam = []
for name in CLS:
    c_ = canon[name]
    r = np.array(c_["r_kpc"], float)
    rd = np.array(c_["rho_dust_req_A_Msun_kpc3"], float)
    R500 = c_["R500_kpc"]
    m = (r >= 0.1 * R500) & (r <= R500) & (rd > 0)
    lr = np.log10(r[m]); ly = np.log10(rd[m])
    if len(lr) < 15:
        continue
    # grid r_t within this cluster's own range, models with single amplitude
    def sse_pc(lgt):
        z = lr - lgt
        if (z < 0).sum() < 5 or (z > 0).sum() < 5:
            return np.inf
        X = np.hstack([np.ones((len(lr), 1)), -np.minimum(z, 0.0)[:, None],
                       -np.maximum(z, 0.0)[:, None]])
        cf, s, _ = fit_linear(X, ly)
        return s
    glo, ghi = lr.min() + 1e-6, lr.max() - 1e-6
    gg = np.linspace(glo, ghi, 121)
    ssv = np.array([sse_pc(g) for g in gg])
    i2 = int(np.argmin(ssv))
    lo, hi = gg[max(0, i2 - 2)], gg[min(len(gg) - 1, i2 + 2)]
    for _ in range(60):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if sse_pc(m1) < sse_pc(m2):
            hi = m2
        else:
            lo = m1
    lgt_i = (lo + hi) / 2
    z = lr - lgt_i
    X = np.hstack([np.ones((len(lr), 1)), -np.minimum(z, 0.0)[:, None],
                   -np.maximum(z, 0.0)[:, None]])
    cf, s, _ = fit_linear(X, ly)
    rti = float(10 ** lgt_i)
    p1i, p2i = float(cf[1]), float(cf[2])
    pc_seam.append(dict(cluster=name, rM_kpc=rM_kpc[name], r_t_kpc=rti,
                        r_t_over_rM=rti / rM_kpc[name], p1=p1i, p2=p2i,
                        n=int(len(lr))))
    info(f"  {name:8s} {rM_kpc[name]:8.1f} {rti:8.1f} {rti / rM_kpc[name]:8.2f} "
         f"{p1i:6.2f} {p2i:6.2f} {len(lr):4d}")
rts = np.array([p["r_t_kpc"] for p in pc_seam])
rMs = np.array([p["rM_kpc"] for p in pc_seam])
ratio = rts / rMs
info(f"per-cluster r_t: median {np.median(rts):.0f} kpc (range "
     f"{rts.min():.0f}-{rts.max():.0f}); r_t/r_M median {np.median(ratio):.2f} "
     f"(range {ratio.min():.2f}-{ratio.max():.2f})")
# Spearman r_t vs r_M (rank correlation, pure numpy fallback)
def _ranks(a):
    s = np.argsort(np.argsort(a))
    return s


try:
    from scipy.stats import spearmanr  # noqa
    rho_sp, p_sp = spearmanr(rts, rMs)
except Exception:
    rho_sp = float(np.corrcoef(_ranks(rts), _ranks(rMs))[0, 1])
    p_sp = np.nan
info(f"Spearman(r_t, r_M) = {rho_sp:.3f} (p = {p_sp:.3f})")

# ------------------------------------------------ SEAM IDENTIFIABILITY: the
# profile SSE vs r_t (flat -> unconstrained seam -> one steepening law).
prof = np.array([[g, sse_two(g)] for g in grid])
prof = prof[np.isfinite(prof[:, 1])]
smin = prof[:, 1].min()
lvl_delta = 2.3          # ~1 sigma (2 DF delta chi2) for the r_t profile
inside = prof[prof[:, 1] <= smin + lvl_delta, 0]
r_t_lo = float(10 ** inside.min()) if len(inside) else r_t_fit
r_t_hi = float(10 ** inside.max()) if len(inside) else r_t_fit
info("")
info(f"SEAM IDENTIFIABILITY: 1-sigma band on r_t from the profile "
     f"(delta SSE = {lvl_delta}): [{r_t_lo:.0f}, {r_t_hi:.0f}] kpc; "
     f"span {np.log10(r_t_hi / r_t_lo):.2f} dex")
fl_span = np.log10(r_t_hi / r_t_lo)
# the seam is RESOLVED if its 1-sigma band spans < 0.4 dex (a factor ~2.5 in
# radius) -- the r_M-class itself spans 273-580 kpc (0.33 dex).
constrained = fl_span < 0.4

# ------------------------------------------------------------- MODEL CHOICE
# (a) two-index r_t free  vs  (b) single index  vs  (c) committed  vs
# (d) smooth  vs  (e) seam at r_M per cluster, indices free
d_bic_ab = rows[0][3] - rows[1][3]      # (a) two-index vs (b) single
d_bic_ac = rows[0][3] - rows[2][3]      # (a) vs (c) committed seam
d_bic_bc = rows[1][3] - rows[2][3]      # (b) vs (c)
d_bic_ad = rows[0][3] - rows[4][3]      # (a) vs (d) smooth steepening
d_bic_ae = rows[0][3] - rows[5][3]      # (a) vs (e) r_M seam, free indices
rM_med = float(np.median(list(rM_kpc.values())))
prefer_two = d_bic_ab < -10 and winner_bic[0] == rows[0][0]
seam_at_rM = abs(np.log10(r_t_fit / rM_med)) < 0.15
seam_near_rM_class = (r_t_fit > min(rM_kpc.values()) * 0.6) and \
                     (r_t_fit < max(rM_kpc.values()) * 1.4)
info("")
info("VERDICTS")

# V1
info("V1 -- the p1/p2/r_t fit and the model comparison (BIC/AICc):")
info(f"   pooled two-index: p1 = {p1_fit:.2f} +- , p2 = {p2_fit:.2f}, "
     f"r_t = {r_t_fit:.0f} kpc (BIC {rows[0][3]:.1f}, AICc {rows[0][4]:.1f})")
info(f"   d_BIC(a vs b single) = {d_bic_ab:+.1f};  d_BIC(a vs c committed r_M seam) "
     f"= {d_bic_ac:+.1f};  d_BIC(b vs c) = {d_bic_bc:+.1f};  "
     f"d_BIC(a vs d smooth) = {d_bic_ad:+.1f};  d_BIC(a vs e r_M seam, free idx) "
     f"= {d_bic_ae:+.1f}")
info(f"   BIC winner: {winner_bic[0]} (k = {winner_bic[2]})")
check("V1 [the seam fit] the pooled two-index fit returns finite p1, p2, r_t "
      "with p1 ~ inner window (1.69-class) and p2 ~ the deep-window slope on "
      "the SAME per-bin floor-A data (2.785-class, GATE2b)",
      f"p1 = {p1_fit:.2f}, p2 = {p2_fit:.2f}, r_t = {r_t_fit:.0f} kpc",
      abs(p1_fit - P139_INNER) < 0.5 and abs(p2_fit - p2_deep_floorA) < 0.5)

# V2
info("V2 -- the seam's position vs r_M:")
info(f"   pooled r_t = {r_t_fit:.0f} kpc vs r_M median = {rM_med:.0f} kpc "
     f"(ratio {r_t_fit / rM_med:.2f}); "
     f"1-sigma band [{r_t_lo:.0f}, {r_t_hi:.0f}] kpc")
info(f"   per-cluster r_t/r_M median = {np.median(ratio):.2f}; "
     f"Spearman(r_t, r_M) = {rho_sp:.2f}")
info(f"   d_BIC(free r_t vs r_t = r_M per cluster, BOTH indices free) = "
     f"{d_bic_ae:+.1f}"
     + ("  -> the equilibrium-boundary seam is NOT penalized"
        if d_bic_ae > -6 else "  -> the free seam is clearly preferred"))
check("V2 [the seam vs r_M] the fitted r_t sits at r_M-class: within the "
      "per-cluster r_M spread (x0.6-x1.4) and/or per-cluster r_t tracks r_M "
      "(Spearman > 0.4)",
      f"r_t = {r_t_fit:.0f} kpc, r_M median {rM_med:.0f}; "
      f"Spearman = {rho_sp:.2f}, r_t/r_M median = {np.median(ratio):.2f}",
      seam_near_rM_class and (rho_sp > 0.4 or np.median(ratio) < 1.5))

# V3
if np.isfinite(d_bic_ab) and d_bic_ab < -10 and constrained:
    if d_bic_ae > -6:
        v3 = (f"ONE LAW WITH A BOUNDARY at r_t = {r_t_fit:.0f} kpc "
              f"(= {r_t_fit / rM_med:.2f} x median r_M; 1-sigma band "
              f"[{r_t_lo:.0f}, {r_t_hi:.0f}] kpc) AND the seam at each cluster's "
              f"own r_M fits within d_BIC = {d_bic_ae:+.1f} of the free seam: "
              f"the two-index model beats the single index by d_BIC = {d_bic_ab:.1f} "
              f"and the smooth steepening by {d_bic_ad:.1f} -- the dust's shape "
              f"CHANGES, p1 = {p1_fit:.2f} -> p2 = {p2_fit:.2f}, at the "
              f"equilibrium boundary r_M-class; streaming envelope -> mixed "
              f"interior")
    else:
        v3 = (f"ONE LAW WITH A BOUNDARY at r_t = {r_t_fit:.0f} kpc "
              f"({r_t_fit / rM_med:.2f} x median r_M; 1-sigma band "
              f"[{r_t_lo:.0f}, {r_t_hi:.0f}] kpc): the two-index model is "
              f"preferred over the single index by d_BIC = {d_bic_ab:.1f} and the "
              f"seam is resolved (band {fl_span:.2f} dex) -- the dust's shape "
              f"CHANGES, p1 = {p1_fit:.2f} -> p2 = {p2_fit:.2f}, but the seam's "
              f"radius is NOT each cluster's individual r_M (d_BIC = {d_bic_ae:+.1f})")
elif np.isfinite(d_bic_ab) and d_bic_ab < -10:
    v3 = (f"TWO LAWS (seam preferred, d_BIC vs single = {d_bic_ab:.1f}) but the "
          f"seam's position is NOT tightly constrained (band {fl_span:.2f} dex): "
          f"p1 = {p1_fit:.2f} -> p2 = {p2_fit:.2f} at r_t ~ {r_t_fit:.0f} kpc -- the "
          f"transition exists; whether it is the r_M equilibrium boundary is not "
          f"decided by the seam alone")
else:
    v3 = (f"TWO SLOPES AS SEPARATE REGIMES OF ONE STEEPENING LAW: the single "
          f"index / smooth law is NOT rejected (d_BIC vs two-index = "
          f"{d_bic_ab:+.1f}); p1 = {p1_fit:.2f} (inner), p2 = {p2_fit:.2f} (deep) "
          f"are the window-limited readings of a smooth p(r)")
info("V3 -- the honest statement:")
info(f"   {v3}")
d_bic_deciding = min(abs(d_bic_ab), abs(d_bic_ac))
check("V3 [the honest statement] the BIC that decides: the difference between "
      "the two-index model and its best rival is large enough to choose "
      "(|d_BIC| > 6) OR the statement reports the tie honestly",
      f"d_BIC(a vs b) = {d_bic_ab:.1f}, d_BIC(a vs c) = {d_bic_ac:.1f}, "
      f"winner BIC {bic_min:.1f}",
      d_bic_deciding > 6 or abs(d_bic_ab) < 6)

# ------------------------------------------------------------------ RESULTS
out = dict(
    lane="G176",
    title="THE DUST-SLOPE SEAM: one law with a transition, or two disjoint laws?",
    constants=dict(a0_canonical=A0_CANON, G=G,
                   p139_inner=P139_INNER, p108_deep=P108_DEEP),
    data=dict(n_pooled_pos_bins=n, clusters=CLS,
              r_min_kpc=float(R.min()), r_max_kpc=float(R.max())),
    gates=dict(
        G139_coherency_repro=dict(p_dust=float(-p_coh), rms_dex=float(rms_coh),
                                  n=int(n_coh)),
        G108_deep_repro=dict(p_dust=float(-p_dp), rms_dex=float(rms_dp),
                             n=int(n_dp))),
    seam_fit_pooled=dict(
        p1=float(p1_fit), se_p1=float(se_p1), p2=float(p2_fit),
        se_p2=float(se_p2), r_t_kpc=float(r_t_fit),
        sse_dex2=float(sse_a), rms_dex=float(np.sqrt(sse_a / n)),
        r_t_1sigma_band_kpc=[float(r_t_lo), float(r_t_hi)],
        r_t_span_dex=float(fl_span),
        r_M_median_kpc=float(np.median(list(rM_kpc.values()))),
        r_M_range_kpc=[float(min(rM_kpc.values())), float(max(rM_kpc.values()))],
        r_t_over_rM_median=float(r_t_fit / float(np.median(list(rM_kpc.values()))))),
    models=[
        dict(name=name_, k=int(k_), SSE_dex2=float(sse_), BIC=float(bic_),
             AICc=float(aicc_), rms_dex=float(np.sqrt(sse_ / n)), desc=desc_)
        for (name_, k_, sse_, bic_, aicc_, desc_) in rows],
    model_comparison=dict(
        winner_BIC=winner_bic[0], winner_AICc=winner_aicc[0],
        d_BIC_two_vs_single=float(d_bic_ab),
        d_BIC_two_vs_committed_rM=float(d_bic_ac),
        d_BIC_two_vs_smooth=float(d_bic_ad),
        d_BIC_two_vs_rM_seam_free_idx=float(d_bic_ae),
        d_BIC_single_vs_committed_rM=float(d_bic_bc)),
    rM_seam_free_idx=dict(p1=float(p1_e), p2=float(p2_e),
                          sse_dex2=float(sse_e)),
    per_cluster_seam=pc_seam,
    per_cluster_seam_stats=dict(
        r_t_median_kpc=float(np.median(rts)),
        r_t_range_kpc=[float(rts.min()), float(rts.max())],
        r_t_over_rM_median=float(np.median(ratio)),
        spearman_r_t_vs_rM=float(rho_sp)),
    committed_seam_free=dict(r_t_kpc=float(r_t_cp), sse_dex2=float(sse_cp_best)),
    verdicts=dict(
        V1=dict(
            statement="the pooled two-index fit and the BIC/AICc model comparison",
            p1=float(p1_fit), p2=float(p2_fit), r_t_kpc=float(r_t_fit),
            BIC_winner=winner_bic[0], AICc_winner=winner_aicc[0],
            dBIC_vs_single=float(d_bic_ab)),
        V2=dict(
            statement="the seam's position vs r_M",
            r_t_kpc=float(r_t_fit), r_M_median_kpc=float(np.median(list(rM_kpc.values()))),
            r_t_over_rM=float(r_t_fit / float(np.median(list(rM_kpc.values())))),
            per_cluster_r_t_over_rM_median=float(np.median(ratio)),
            spearman=float(rho_sp)),
        V3=dict(statement=v3)),
    checks=RES, n_pass=NP, n_fail=NF)

with open(os.path.join(HERE, "G176_results.json"), "w") as f:
    json.dump(out, f, indent=1, default=float)

info("")
info(f"PASS {NP} / {NF + NP}")
info("wrote G176_results.json  (%d pass / %d fail)" % (NP, NF))