#!/usr/bin/env python3
"""
G136 -- THE LENSING-CORE REGISTRY: numbers for the pre-registered D2 instrument
================================================================================
Registered instrument geometry: Einstein-radius-class strong-lensing cores
(r_E) + inner weak lensing of the 12 X-COP clusters (A1644 A1795 A2029 A2142
A2255 A2319 A3158 A3266 A644 A85 RXC1825 ZW1215), decision window r < 0.1 R500
(G096's D2 resolution cap, H012 D2 registration).

Everything here is derived from committed artifacts only:
  - real_research/data/xcop/xcop_r500_ettori2019.json  (Ettori+19 A&A 621, A39: z, R500, M500, R200, M200)
  - deepseek_push/G096_results.json                    (the committed D2 test: inner slopes,
                                                        per-cluster window-honest NFW rs/R500)
Conventions: flat LCDM, H0 = 70 km/s/Mpc, Omega_m = 0.3.

1. Einstein-radius class: SIS matched to the committed M200 (sigma_v^2 = G M200/(2 R200)),
   theta_E = 4 pi (sigma_v/c)^2 D_ls/D_s ; r_E = D_l * theta_E ; sources z_s = 1 and 2.
   Flat-universe identity: D_ls = D_s - (1+z_l)/(1+z_s) D_l .
2. Window-honest NFW residual slope at r < 0.1 R500 from the COMMITTED per-cluster
   rs/R500 (G096): s(r) = -1 - 2 (r/rs)/(1 + r/rs).
3. Precision requirement: sigma_slope <= 0.5/3 (3-sigma separation of -1 vs -1.5
   in the decision window r < 0.1 R500; the projected image d ln Sigma/d ln R = s + 1
   carries the same 0.5 separation).
4. Binning / surface-density sensitivity: N log-spaced bins over [r_min, 0.1] R500;
   per-bin relative ESD precision eps from Var(b) = 12 eps^2 / (h^2 N (N^2-1)),
   h = ln(0.1/r_min)/N.
"""
import json
import math
import os
import statistics

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(f"{REPO}/real_research/data/xcop/xcop_r500_ettori2019.json"))
g096 = json.load(open(f"{REPO}/deepseek_push/G096_results.json"))
CLUSTERS = ["A1644", "A1795", "A2029", "A2142", "A2255", "A2319", "A3158",
            "A3266", "A644", "A85", "RXC1825", "ZW1215"]
H0, OM, OL, C_KM = 70.0, 0.3, 0.7, 299792.458
GK = 4.3009e-6  # kpc (km/s)^2 / Msun


def Da(z):
    """Angular diameter distance (Mpc), flat LCDM, H0=70."""
    def E(zz): return math.sqrt(OM * (1 + zz) ** 3 + OL)
    n = 20000
    dz = z / n
    s = 0.0
    for i in range(n):
        s += 1.0 / E((i + 0.5) * dz)
    return (C_KM / H0) * dz * s / (1 + z)


print("=" * 80)
print("G136 -- THE LENSING-CORE REGISTRY: pre-registered D2 instrument numbers")
print("=" * 80)

Dl = {c: Da(data[c]["z"]) for c in CLUSTERS}
Ds = {1: Da(1.0), 2: Da(2.0)}

rows = []
for cl in CLUSTERS:
    d = data[cl]
    z = d["z"]
    R500k = d["R500"] * 1000.0
    M200 = d["M200"] * 1e14
    R200k = d["R200"] * 1000.0
    sig = math.sqrt(GK * M200 / (2 * R200k))
    dl = Dl[cl]
    vals = {}
    for zs in (1, 2):
        Dls = Ds[zs] - (1 + z) / (1 + zs) * dl
        th = 4 * math.pi * (sig / C_KM) ** 2 * Dls / Ds[zs]
        vals[zs] = (th * 206265.0, dl * th * 1000.0)   # (arcsec, physical kpc at the lens)
    rows.append(dict(cluster=cl, z=z, R500_kpc=R500k, M200=M200, sig=sig,
                     vals=vals, r01_kpc=0.1 * R500k))

print("\n%-8s %6s %6s %8s %5s %8s %7s %7s %7s %6s" %
      ("cluster", "z", "R500", "M200e14", "sig", "thE(z1)", "rE(z1)", "rE(z2)", "0.1R500", "rE2/r01"))
print("-" * 78)
for r in rows:
    print("%-8s %6.4f %6.0f %8.2f %5.0f %8.1f %7.1f %7.1f %7.0f %6.2f" % (
        r["cluster"], r["z"], r["R500_kpc"], r["M200"] / 1e14, r["sig"],
        r["vals"][1][0], r["vals"][1][1], r["vals"][2][1], r["r01_kpc"],
        r["vals"][2][1] / r["r01_kpc"]))

rE1 = [r["vals"][1][1] for r in rows]
rE2 = [r["vals"][2][1] for r in rows]
th1 = [r["vals"][1][0] for r in rows]
r01 = [r["r01_kpc"] for r in rows]
print("\nr_E(z_s=1):  %5.1f - %5.1f kpc   |  theta_E(z_s=1): %4.1f - %4.1f arcsec" % (min(rE1), max(rE1), min(th1), max(th1)))
print("r_E(z_s=2):  %5.1f - %5.1f kpc" % (min(rE2), max(rE2)))
print("0.1 R500 window: %5.1f - %5.1f kpc" % (min(r01), max(r01)))

# --- 2. window-honest NFW band at r < 0.1 R500 (committed G096 rs values) ---
rsmap = {c["cluster"]: c["rs_over_R500"]
         for c in g096["honest_limits"]["NFW_asymptote"]["per_cluster"]}
print("\nwindow-honest NFW residual slope s(r) = -1 - 2(r/rs)/(1+r/rs), over the 12 (committed rs):")
for frac in (0.02, 0.05, 0.10):
    vals = [-1 - 2 * (frac / rsmap[c]) / (1 + frac / rsmap[c]) for c in CLUSTERS]
    print("  s(%.2f R500): median %+.3f  range %+.3f .. %+.3f" %
          (frac, statistics.median(vals), min(vals), max(vals)))
print("  median rs/R500 = %.3f" % statistics.median(rsmap[c] for c in CLUSTERS))

# --- 3. precision requirement ---
sig_req = 0.5 / 3.0
print("\nprecision requirement: sigma_s <= 0.5/3 = %.4f (3-sigma separation of -1 vs -1.5, r < 0.1 R500)" % sig_req)
print("  G096 committed baseline: mean per-cluster HSE-based slope error %.3f -> x%.1f improvement required"
      % (g096["mean_MC_error"], g096["mean_MC_error"] / sig_req))

# --- 4. binning and surface-density sensitivity ---
print("\nbinning / surface-density sensitivity (per-bin relative ESD precision needed for sigma_s = 0.167):")
for rmin_frac, N in [(0.02, 6), (0.02, 8), (0.03, 5), (0.03, 6)]:
    lnr0 = math.log(0.1) - math.log(rmin_frac)
    h = lnr0 / N
    varb = 12.0 / (h * h * N * (N * N - 1))
    eps = sig_req / math.sqrt(varb)
    print("  window [%.2f, 0.1] R500, N=%d bins: spacing h=%.3f ln (%.3f dex) -> per-bin ESD precision %.1f%%"
          % (rmin_frac, N, h, h / math.log(10), eps * 100))

print("\n12-cluster pooled decision: SE(median) noise-only (per-cluster 0.17): %.3f;"
      " scatter-driven (between-cluster 0.25): %.3f" % (0.17 / math.sqrt(12), 0.25 / math.sqrt(12)))
print("projected image: d ln Sigma/d ln R = s + 1 -> NFW cusp 0.0 vs theory -0.5 (0.5 separation, same 3-sigma budget).")
print("r_E(z_s=2) / 0.1R500 across the 12: %.2f .. %.2f" %
      (min(r["vals"][2][1] / r["r01_kpc"] for r in rows), max(r["vals"][2][1] / r["r01_kpc"] for r in rows)))
print("\npublished-reach cross-checks (lensing TODAY):")
print("  A85 HSC inner WL cut (HyeongHan et al. 2025, arXiv:2511.02323): 90 kpc excluded -> %.3f R500" % (90 / (1000 * data["A85"]["R500"])))
a2142_90 = 1.5 * math.pi / 180 / 60 * Dl["A2142"]
print("  A2142 Subaru Suprime-Cam inner cut ~1.5 arcmin (Umetsu+09 class): %.0f kpc = %.3f R500" %
      (a2142_90 * 1000, a2142_90 / data["A2142"]["R500"]))
print("Done.")