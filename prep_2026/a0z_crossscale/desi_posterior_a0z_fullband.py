#!/usr/bin/env python3
"""
FULL a0(z)/a0(0) PREDICTION BAND TABLE across all three DESI DR2 w0waCDM datasets.

Builds on desi_posterior_a0z.py (same law, same posteriors, same 2x2 correlated
Cholesky Monte Carlo over (w0,wa), same seed 0). This script EXTENDS it to:
  - the full z grid {0.1,0.2,0.35,0.5,0.9,1.0,1.5,2.0,3.0}
  - MEDIAN + 68% (16/84) + 95% (2.5/97.5) intervals from the correlated posterior
  - explicit location of the low-z BUMP peak (z_peak, max ratio)
  - the unity-crossover z (ratio -> 1 on the way down)
  - a REGRESSION CHECK that medians at z in {1,2,3} match the parent script.

THE LAW (full closed form, NEVER truncated):
  rho_DE(z)/rho_DE0 = (1+z)^{3(1+w0+wa)} * exp(-3 wa z/(1+z))          [CPL]
  a0(z)/a0(0)       = sqrt( rho_DE(z)/rho_DE0 )
                    = (1+z)^{1.5(1+w0+wa)} * exp(-1.5 wa z/(1+z))

FOOTING-INDEPENDENCE (proved by construction): the RATIO a0(z)/a0(0) depends ONLY
on (w0,wa). The horizon coefficient Z and the absolute a0(0) (canonical 9.36e-11 vs
alt 1.13e-10) enter only the absolute normalization a0(0) and CANCEL identically in
the ratio. This code never references Z or a0(0) -- there is a single ratio band, not
two. Only the absolute a0(z)=ratio*a0(0) would differ by footing.

LCDM-DISSOLUTION: if w0->-1, wa->0 then 1+w0+wa->0 and wa->0, so the ratio -> 1 for
all z (flat) and is INDISTINGUISHABLE from constant-a0 MOND. The band below is a
CONDITIONAL prediction: its entire discriminating power is inherited from whether
DESI's w0wa evolution is real (LCDM excluded 2.8-4.2 sigma), not proven here.

DEEP-MOND MEASUREMENT PENALTY (not modeled in the band, stated for honesty): measuring
a0 via a0 = g_obs^2/g_bar DOUBLES per-point log-scatter, so the error on a0 is ~2*sigma
/sqrt(N), NOT sigma/(2*sqrt(N)). The precision needed on the underlying RC/RAR data is
~2x tighter than the precision quoted on a0(z) itself.

MUSE-DARK III (Ciocan 2026) reports a0 RISING with z: that is an LCDM-degenerate
TENSION/WATCH, NOT a confirmation. The framework predicts a mild rise ONLY in the tiny
low-z bump (peak ~+3-4% near z~0.35), exactly where a0 is hardest to measure.
"""
import numpy as np
from scipy.special import erfcinv

ZGRID = [0.1, 0.2, 0.35, 0.5, 0.9, 1.0, 1.5, 2.0, 3.0]
ZFINE = np.linspace(0.0, 3.0, 30001)   # for bump-peak / crossover location on the median law

def a0ratio(z, W0, WA):
    """Full closed-form a0(z)/a0(0); z scalar or array, W0/WA arrays (posterior draws)."""
    return (1.0 + z)**(1.5*(1.0 + W0 + WA)) * np.exp(-1.5*WA*z/(1.0 + z))

def median_law(z, w0, wa):
    """Ratio evaluated at the posterior CENTRAL (w0,wa) -- used to locate bump/crossover."""
    return (1.0 + z)**(1.5*(1.0 + w0 + wa)) * np.exp(-1.5*wa*z/(1.0 + z))

def analyze(w0, sw0, wa, swa, rho, label, N=400000):
    # correlated posterior draw, seed 0 (matches parent script's default_rng(0))
    cov = np.array([[sw0**2, rho*sw0*swa], [rho*sw0*swa, swa**2]])
    L = np.linalg.cholesky(cov)
    g = np.random.default_rng(0)
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        pair = np.array([w0, wa]) + g.standard_normal((N, 2)) @ L.T
    W0, WA = pair[:, 0], pair[:, 1]

    print(f"\n[{label}]")
    print(f"    w0={w0:+.3f}+/-{sw0:.3f}  wa={wa:+.3f}+/-{swa:.2f}  (corr {rho:+.2f})")
    print(f"    {'z':>5} | {'median':>7} | {'68% (16,84)':>17} | {'95% (2.5,97.5)':>19}")
    print(f"    {'-'*5}-+-{'-'*7}-+-{'-'*17}-+-{'-'*19}")
    table = {}
    for z in ZGRID:
        r = a0ratio(z, W0, WA)
        med = np.median(r)
        lo68, hi68 = np.percentile(r, [16, 84])
        lo95, hi95 = np.percentile(r, [2.5, 97.5])
        table[z] = (med, lo68, hi68, lo95, hi95)
        tag = ""
        if abs(z-0.35) < 1e-9: tag = "  <- bump-peak region"
        if abs(z-0.9)  < 1e-9: tag = "  <- crossover region"
        print(f"    {z:>5.2f} | {med:>7.3f} | [{lo68:>6.3f},{hi68:>6.3f}] | [{lo95:>6.3f},{hi95:>6.3f}]{tag}")

    # BUMP peak & unity crossover on the MEDIAN (central-w0,wa) law
    ml = median_law(ZFINE, w0, wa)
    ipk = int(np.argmax(ml))
    z_peak, r_peak = ZFINE[ipk], ml[ipk]
    # first z>z_peak where the median law crosses 1.0 downward
    below = np.where((ZFINE > z_peak) & (ml <= 1.0))[0]
    z_cross = ZFINE[below[0]] if below.size else float('nan')
    bump_pct = (r_peak - 1.0)*100.0
    print(f"    BUMP peak (median law): z_peak = {z_peak:.3f}, max ratio = {r_peak:.4f} "
          f"({bump_pct:+.2f}% above unity)")
    if np.isfinite(z_cross):
        print(f"    UNITY crossover (median law, downward): z_cross = {z_cross:.3f}")
    else:
        print(f"    UNITY crossover: none in [0,3] (median law stays >=1)")

    # decline significance at z=3 (parity with parent script)
    r3 = a0ratio(3.0, W0, WA)
    frac_flat_or_rise = max(np.mean(r3 >= 1.0), 0.5/N)
    sig = np.sqrt(2)*erfcinv(2*frac_flat_or_rise)
    print(f"    P(a0(3)<a0(0)) = {np.mean(r3<1.0)*100:.1f}%  => decline significance ~ {sig:.1f} sigma")
    return table, (z_peak, r_peak, z_cross)

print("="*84)
print("FULL a0(z)/a0(0) PREDICTION BAND -- DESI DR2 w0waCDM, canonical & footing-independent RATIO")
print("Constant-Lambda / LCDM-dissolution reference: a0(z)/a0(0) = 1.000 for ALL z (flat).")
print("Law: a0(z)/a0(0) = (1+z)^{1.5(1+w0+wa)} * exp(-1.5 wa z/(1+z))  [full closed form].")
print("="*84)

DATASETS = [
    (-0.838, 0.055, -0.62, 0.22, -0.86, "DESI+CMB+Pantheon+ (LCDM excl 2.8s)"),
    (-0.752, 0.057, -0.86, 0.22, -0.86, "DESI+CMB+DESY5     (LCDM excl 4.2s)"),
    (-0.667, 0.088, -1.09, 0.31, -0.87, "DESI+CMB+Union3    (LCDM excl 3.8s)"),
]

results = {}
for w0, sw0, wa, swa, rho, label in DATASETS:
    tab, feats = analyze(w0, sw0, wa, swa, rho, label)
    results[label] = (tab, feats)

# ---- REGRESSION CHECK vs parent script desi_posterior_a0z.py medians (z=1,2,3) ----
# Parent used N=200000; here N=400000. Both seed 0. Medians agree to MC precision (~1e-3).
PARENT = {
    "DESI+CMB+Pantheon+ (LCDM excl 2.8s)": {1.0: 0.989, 2.0: 0.874, 3.0: 0.775},
    "DESI+CMB+DESY5     (LCDM excl 4.2s)": {1.0: 1.009, 2.0: 0.862, 3.0: 0.737},
    "DESI+CMB+Union3    (LCDM excl 3.8s)": {1.0: 1.031, 2.0: 0.855, 3.0: 0.707},
}
print("\n" + "="*84)
print("REGRESSION CHECK vs parent desi_posterior_a0z.py (medians at z=1,2,3; tol 0.004)")
print("="*84)
ok = True
for label, (tab, _) in results.items():
    for z in (1.0, 2.0, 3.0):
        here = tab[z][0]
        there = PARENT[label][z]
        d = abs(here - there)
        flag = "OK " if d <= 0.004 else "MISMATCH"
        if d > 0.004: ok = False
        print(f"    {label[:34]:34s} z={z:.0f}: here={here:.3f} parent={there:.3f} d={d:.4f} [{flag}]")
print(f"\nREGRESSION: {'ALL MEDIANS MATCH parent to <=0.004' if ok else 'MISMATCH DETECTED'}")

# ---- footing-independence assertion (single ratio band) ----
print("\nFOOTING-INDEPENDENCE: the ratio uses only (w0,wa); Z and a0(0) never appear -> one band.")
print("Absolute a0(z) = ratio * a0(0) would differ by footing (9.36e-11 canonical vs 1.13e-10 alt).")
print("\nEXIT 0")
