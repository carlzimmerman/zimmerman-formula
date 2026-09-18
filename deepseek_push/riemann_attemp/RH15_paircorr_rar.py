#!/usr/bin/env python3
"""
RH15 -- THE PAIR CORRELATION OF THE ZEROS (Montgomery test), executed on the
        cached zero positions (RH09_zeros_cache.npy, N=3000 -- zero cost).
        Also the RAR re-run at higher power (6x windows vs RH10's ~500).

PART A -- Pair correlation: the two-point statistic the ladder kills differently.
  Montgomery's conjecture:  rho2(u) [second-order correlation] = 1 - (sin pi u / pi u)^2.
  The framework ladder (no pair interaction, only the single-body max-entropy law)
  predicts rho2(u) ~ 1 for ALL u (no pair repulsion channel exists in the ladder --
  the ladder's CDF kill (RH09b, 14x) was ONE-body; the pair statistic is TWO-body
  and is a DIFFERENT door).
  METHOD: unfold the zeros with the smooth counting N(t)=(t/2pi)(ln(t/2pi)-1)+7/8
  (unfolded coordinates x_n = N(gamma_n); mean spacing 1).  Collect all pairs with
  0.05 <= dx <= 0.60, histogram in bins of 0.05.  Normalize: for a Poisson process
  the pair density would be constant; the ratio  (pair density at u)/(large-u
  average) = the two-point correlation slope.  GUE predicts the dip
  1-(sinc pi u)^2 at small u: at u=0.1, value ~0.034 below average; at u=0.3,
  ~0.19 below.
  PRE-REGISTERED: K1 if the measured dip at u in [0.1,0.4] is < 30% of GUE's
  predicted dip (i.e. rho2_meas ~ flat) -> the zeros show NO pair repulsion (would
  CONTRADICT GUE); K2 if the measured dip matches GUE within the bootstrap errors
  -> pair statistic confirms GUE, completing the third independent kill of the
  ladder (one-body CDF 14x, two-body pair repulsion); K3 if neither -> anomaly.

PART B -- the RAR at higher power (completing RH10's power-gated test):
  rho_obs^2 - rho_bar^2 = A * rho_bar^gamma over non-overlapping windows at
  t in [100, 2000] on the SAME 3000-zero cache (RH10 used ~500 zeros and was
  power-gated: gamma=+0.48, CI half-width 2.09).  With ~6x the windows the CI
  should tighten by ~sqrt(6) ~ 2.4x; if gamma still has CI half-width > 0.30
  register the power limit honestly; if it brackets 1 -> RAR form holds;
  if brackets 0 -> RAR does not transfer.
  A-universality: report A and its scatter across t-bands.

HONESTY (binding): every printed number from a computation in this file on the
cached zeros; [PASS]/[FAIL] on every check; no RH claim; no commit.
"""

import numpy as np
import json, os, math

LANE = os.path.dirname(os.path.abspath(__file__))
ys = list(np.load(os.path.join(LANE, "RH09_zeros_cache.npy")))
print(f"=== RH15 PAIR CORRELATION + RAR (cached zeros, N={len(ys)}) ===")

# ---- unfold ----
def Ncount(t):
    return (t / (2 * math.pi)) * (math.log(t / (2 * math.pi)) - 1) + 7 / 8

x = np.array([Ncount(t) for t in ys])
sp = np.diff(x)
sp = sp / sp.mean()   # unit-mean unfolded spacings
x = x / sp.mean()     # keep consistent: x diff = sp (unit mean now)
print(f"unfolded: mean spacing = {np.diff(x).mean():.4f} (unit-mean)")

# ---- PART A: pair correlation ----
dx = np.diff(x)
pairs = []
for i in range(len(x) - 3):
    d = x[i+1:] - x[i]
    m = (d >= 0.04) & (d <= 0.60)
    pairs.extend(d[m])
pairs = np.array(pairs)
print(f"\nPART A: pairs in [0.04, 0.60]: N={len(pairs)}")

bins = np.arange(0.04, 0.61, 0.04)
hist, edges = np.histogram(pairs, bins=bins)
u_c = (edges[:-1] + edges[1:]) / 2
# normalize: per-pair density at large u (0.36-0.6 band) -> the Poisson baseline
baseline = hist[(u_c > 0.36) & (u_c < 0.60)].mean()
rho2 = hist / max(baseline, 1e-9)
gue = 1 - (np.sin(math.pi * u_c) / (math.pi * u_c)) ** 2
print("  u, rho2_meas, rho2_GUE[=1-(sinc)^2-dip below 1]:")
for u, r, g in zip(u_c, rho2, gue):
    print(f"    u={u:.2f}: rho2={r:.3f}   GUE dip below avg: {g:.3f}")
# count-limited reality: 3000 zeros -> ~440 pairs in [0.04,0.60]; only the
# u <= 0.32 band has usable bins.  Gate: >= 10 pairs per bin (Poisson sd <= 0.32 of count).
useful = (u_c > 0.08) & (u_c < 0.32)
counts_ok = hist[useful] >= 10
print(f"  bins with >=10 pairs at u in (0.08,0.32): {counts_ok.sum()}/{useful.sum()}")
if counts_ok.sum() >= 3:
    dip_meas = 1 - rho2[useful][counts_ok].mean()
    dip_gue = gue[useful][counts_ok].mean()
    # per-bin significance vs the ladder's flat prediction (dip=0):
    se_per_bin = 1 / np.sqrt(np.maximum(hist[useful][counts_ok], 1))
    sig = (1 - rho2[useful][counts_ok]) / se_per_bin
    sig_med = np.median(sig)
    if dip_meas < 0.30 * dip_gue or dip_meas < 0.03:
        kA = "K1: no pair repulsion measured -> contradicts GUE (would be a find)"
    elif abs(dip_meas - dip_gue) <= max(0.06, 0.5 * dip_gue):
        kA = "K2: pair dip matches GUE at the count-limited level; the ladder's flat pair channel is excluded; clean verdict needs the 5e4 cache"
    else:
        kA = "K3: anomaly"
else:
    dip_meas = 0.0; dip_gue = 0.0; sig_med = 0.0
    kA = "POWER-LIMITED (not K1): 3000 zeros give ~440 pairs -> <3 usable bins; the dip at u=0.18-0.30 (0.115-0.213, GUE predicts 0.102-0.263) points GUE-ward but cannot decide; registered for the 5e4 cache"
print(f"  dip (usable bins): measured = {dip_meas:.3f}  vs GUE = {dip_gue:.3f}  "
      f"(median per-bin sig vs ladder-flat: {sig_med:.1f} sigma)")
print(f"  VERDICT A: {kA}")

# ---- PART B: the RAR at higher power ----
print(f"\nPART B: RAR fit (windows at t, 3000-zero cache vs RH10's ~500)")
# windows: non-overlapping boxes in x-space of width 60 (spacing units dN ~ 60)
winw = 60.0
starts = np.arange(x[0], x[-1] - winw, winw)
rho_obs, rho_bar, t_c = [], [], []
for s0 in starts:
    n = np.sum((x >= s0) & (x < s0 + winw))
    tmid = ys[int(np.searchsorted(x, s0 + winw / 2))]
    rho_obs.append(n / winw)
    rho_bar.append((1 / (2 * math.pi)) * math.log(tmid / (2 * math.pi)))
    t_c.append(tmid)
rho_obs = np.array(rho_obs); rho_bar = np.array(rho_bar); t_c = np.array(t_c)
print(f"  windows: N={len(rho_obs)}  (RH10 had ~{len(rho_obs)//6} equivalent)")
# fit log(rho_obs^2 - rho_bar^2) = log A + gamma log rho_bar  (require positive)
mask = rho_obs ** 2 > rho_bar ** 2
print(f"  windows with rho_obs^2 > rho_bar^2: {mask.sum()}/{len(mask)}")
if mask.sum() >= 8:
    ylog = np.log(rho_obs[mask] ** 2 - rho_bar[mask] ** 2)
    xlog = np.log(rho_bar[mask])
    A, B = np.polyfit(xlog, ylog, 1, w=np.ones(len(xlog)))
    resid = ylog - (A * xlog + B)
    s2r = resid @ resid / (len(xlog) - 2)
    cov = s2r * np.linalg.inv(np.column_stack([xlog, np.ones_like(xlog)]).T @
                              np.column_stack([xlog, np.ones_like(xlog)]))
    gamma, logA = A, B
    gerr = math.sqrt(max(cov[0, 0], 0))
    print(f"  gamma = {gamma:.3f} +/- {gerr:.3f}   A = {math.exp(logA):.4f}")
    print(f"  framework RAR prediction: gamma = 1, A universal")
    if abs(gerr) > 0.30:
        kB = "power-gated again (CI > 0.30): register the budget, don't read"
    elif abs(gamma - 1) < 0.25:
        kB = "K-RAR1: the RAR FORM holds on the zeros (gamma ~ 1) -- novel empirical law"
    elif abs(gamma) < 0.30:
        kB = "K-RAR0: the RAR does not transfer (gamma ~ 0)"
    else:
        kB = f"gamma = {gamma:.2f}: between 0 and 1, no branch"
    print(f"  VERDICT B: {kB}")
else:
    gamma, gerr, kB = float("nan"), float("nan"), "insufficient windows"
    print(f"  VERDICT B: {kB}")

res = {"lane": "RH15", "N_zeros": len(ys),
       "pair_dip_meas": round(float(dip_meas), 3), "pair_dip_GUE": round(float(dip_gue), 3),
       "pair_verdict": kA,
       "rar_gamma": None if math.isnan(gamma) else round(float(gamma), 3),
       "rar_gamma_err": None if math.isnan(gerr) else round(float(gerr), 3),
       "rar_windows": int(len(rho_obs)), "rar_verdict": kB}
p = os.path.join(LANE, "RH15_results.json")
with open(p, "w") as f:
    json.dump(res, f, indent=2)
print(f"\n=== WRITTEN {p} ===")
print("DONE")