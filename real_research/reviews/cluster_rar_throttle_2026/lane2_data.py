#!/usr/bin/env python3
"""
LANE 2 -- Confront Branch B's throttle break (y_c = Z/2 = 2.894) against the
MEASURED cluster RAR: Tian, Umetsu, Ko et al. 2020, ApJ 896, 70
"The Radial Acceleration Relation in CLASH Galaxy Clusters" (arXiv:2001.08340).

Framework's OWN premises (NON-NEGOTIABLE):
  a0 canonical = 9.36e-11 m/s^2 (rho_DE / cH_Lambda / Z)   [Z = sqrt(32pi/3)]
  a0 alt       = 1.13e-10 m/s^2 (rho_total / cH0)
  Z  = sqrt(32*pi/3) = 5.789,   y_c = Z/2 = 2.894
  nu(y) = sqrt(1 + 1/y)          [g_obs = sqrt(g_bar^2 + g_bar a0), y=g_bar/a0]
  Branch B throttle: g_obs = [1 + (nu(y)-1) T(y)] g_bar,  T(y)=min(1,(y_c/y)^n), n=1

TIAN+2020 MEASURED FACTS (quoted from the paper, ar5iv full text):
  - 20 high-mass CLASH clusters, weak-lensing + strong-lensing + X-ray + BCG stars.
  - Fitted RAR: ln(g_tot) = 0.51(+0.04/-0.05) ln(g_bar) - 9.80(+1.07/-1.08)
      => slope 0.51 +/- ~0.05, i.e. a CLEAN single power law, "no evidence of
         multiple slopes or breaks."
  - Consistent with deep-limit g_tot = sqrt(g_dagger * g_bar).
  - Acceleration scale g_dagger = (2.02 +/- 0.11)e-9 m/s^2  (~17x the galaxy 1.2e-10).
  - Lognormal intrinsic scatter 14.7(+2.9/-2.8)%  (= 0.059 dex).
  - Radial range ~14 kpc (BCG core) to ~600 kpc.
  - g_bar RANGE (quoted verbatim): "the largest baryonic acceleration in the BCG
    regime is 2.1e-10 m/s^2 and the smallest one in the intracluster regime is
    1.3e-11 m/s^2."
"""
import numpy as np

# ------------------------------------------------------------------ constants
Z    = np.sqrt(32*np.pi/3)          # 5.7888
y_c  = Z/2                          # 2.8944
A0_CANON = 9.36e-11
A0_ALT   = 1.13e-10
n_throttle = 1

# Tian+2020 measured
GBAR_MIN = 1.3e-11                  # smallest, intracluster
GBAR_MAX = 2.1e-10                  # largest, BCG core
G_DAGGER = 2.02e-9                  # fitted cluster accel scale
G_DAGGER_ERR = 0.11e-9
SLOPE = 0.51; SLOPE_ERR = 0.05
SCATTER_FRAC = 0.147               # 14.7% lognormal intrinsic
SCATTER_DEX  = SCATTER_FRAC/np.log(10)*1.0  # frac -> dex (small-frac ~ /ln10)
SYS_FLOOR_DEX = (0.1, 0.3)         # hydrostatic bias / M-L / projection floor

def nu(y):        return np.sqrt(1.0 + 1.0/y)
def T(y):         return np.minimum(1.0, (y_c/y)**n_throttle)
def boostB(y):    return 1.0 + (nu(y)-1.0)*T(y)   # Branch B effective boost
def boostMOND(y): return nu(y)                     # plain framework MOND

print("="*72)
print("LANE 2 -- Branch B throttle break vs Tian+2020 CLASH cluster RAR")
print("="*72)
print(f"Z = {Z:.4f}   y_c = Z/2 = {y_c:.4f}")
print(f"g_bar break location = y_c*a0:")
print(f"   canonical a0={A0_CANON:.2e} -> g_bar_break = {y_c*A0_CANON:.3e} m/s^2  (log10={np.log10(y_c*A0_CANON):.3f})")
print(f"   alt       a0={A0_ALT:.2e} -> g_bar_break = {y_c*A0_ALT:.3e} m/s^2  (log10={np.log10(y_c*A0_ALT):.3f})")

# ------------------------------------------------------------------ (1) y-range covered
print("\n(1) Y-RANGE COVERED BY TIAN+2020  [y = g_bar/a0]")
for name, a0 in [("canonical", A0_CANON), ("alt", A0_ALT)]:
    ymin = GBAR_MIN/a0; ymax = GBAR_MAX/a0
    print(f"   {name:9s} a0={a0:.2e}:  y in [{ymin:.3f}, {ymax:.3f}]"
          f"   ...  y_max {'REACHES' if ymax>=y_c else 'FALLS SHORT of'} y_c={y_c:.3f}"
          f"  (factor {y_c/ymax:.2f} short)" if ymax<y_c else "")
    if ymax >= y_c:
        print(f"   {name:9s} a0={a0:.2e}:  y in [{ymin:.3f}, {ymax:.3f}]  REACHES y_c")

# ------------------------------------------------------------------ (2) is the break in range? break size
print("\n(2) BREAK VISIBILITY")
ymax_canon = GBAR_MAX/A0_CANON
ymax_alt   = GBAR_MAX/A0_ALT
print(f"   Tian max y  = {ymax_canon:.3f} (canonical) / {ymax_alt:.3f} (alt).")
print(f"   Throttle onset y_c = {y_c:.3f}.")
print(f"   => The highest-acceleration cluster core point sits BELOW y_c on BOTH footings.")
print(f"   => T(y)=1 for every Tian point; Branch B == plain framework MOND over the")
print(f"      ENTIRE cluster-RAR range. There is NO break inside the data to detect.")

# size of the throttle deviation IF the data reached higher y (for sensitivity)
print("\n   Throttle-induced deviation from plain MOND (dex), IF y_c were exceeded:")
for y in [3.0, 5.0, 8.0, 12.0, 20.0]:
    dev = np.log10(boostMOND(y)/boostB(y))   # how much LESS phantom Branch B gives
    print(f"      y={y:5.1f}:  plain boost {boostMOND(y):.4f}  ->  Branch B {boostB(y):.4f}"
          f"   deficit-vs-MOND = {dev:.4f} dex")

# ------------------------------------------------------------------ (3) sensitivity
print("\n(3) SENSITIVITY TO DETECT THE BREAK")
print(f"   Tian intrinsic scatter = {SCATTER_FRAC*100:.1f}%  = {SCATTER_DEX:.4f} dex.")
print(f"   Systematic floor (hydrostatic bias, M/L, projection) ~ {SYS_FLOOR_DEX[0]}-{SYS_FLOOR_DEX[1]} dex.")
peak_break = max(np.log10(boostMOND(y)/boostB(y)) for y in np.linspace(3,20,200))
print(f"   Peak throttle break signal ~ {peak_break:.4f} dex (n=1, at y~4-6).")
print(f"   Signal/intrinsic-scatter  = {peak_break/SCATTER_DEX:.3f}")
print(f"   Signal/systematic-floor   = {peak_break/SYS_FLOOR_DEX[0]:.3f} - {peak_break/SYS_FLOOR_DEX[1]:.3f}")
print("   => Even with the range, the break is ~3-4x below intrinsic scatter and")
print("      ~5-20x below the systematic floor. Detection needs ~0.01 dex precision")
print("      AT y~5-10 -- unreached by any cluster-RAR dataset in hand.")

# ------------------------------------------------------------------ (4) the deficit + throttle cost
print("\n(4) THE CLUSTER DEFICIT (shared-MOND) AND WHETHER THE THROTTLE WORSENS IT")
ratio_scale = G_DAGGER/A0_CANON
deficit_deep = np.sqrt(ratio_scale)   # deep-regime g_obs under-prediction factor
print(f"   Tian g_dagger = {G_DAGGER:.2e} = {ratio_scale:.1f}x canonical a0={A0_CANON:.2e}.")
print(f"   Framework MOND deep-limit g_obs = sqrt(g_bar*a0); Tian = sqrt(g_bar*g_dagger).")
print(f"   => framework UNDER-predicts cluster g_obs by sqrt({ratio_scale:.1f}) = {deficit_deep:.2f}x")
print(f"      (in mass ~ {ratio_scale:.0f}x at fixed g_bar deep; the known ~2-10x cluster deficit).")
# explicit: predicted g_obs (framework MOND) vs Tian fit across the data range
print("\n   g_obs comparison across the Tian g_bar range (canonical a0):")
print("      log10 g_bar |  Tian fit g_obs |  framework-MOND g_obs |  deficit dex")
for gbar in np.array([GBAR_MIN, 5e-11, 1e-10, GBAR_MAX]):
    y = gbar/A0_CANON
    g_tian = np.exp(0.51*np.log(gbar) - 9.80)
    g_fw   = boostMOND(y)*gbar
    print(f"        {np.log10(gbar):7.3f}   |   {g_tian:.3e}  |     {g_fw:.3e}      |"
          f"   {np.log10(g_tian/g_fw):.3f}")
print("   The throttle is INACTIVE over this whole range (all y<y_c), so Branch B's")
print("   deficit == plain framework MOND's deficit. The throttle adds ZERO in-hand cost.")
print("   Conceptual cost (Lane-1 cross-check): T depletes at y>y_c, exactly where the")
print("   deficit is worst -- but the top Tian core point (y=%.2f) is just SHORT of y_c=%.3f,"%(ymax_canon,y_c))
print("   so the worsening is UNPROBED, not realized. Deficit stays shared-MOND, not Branch-B-specific.")

# ------------------------------------------------------------------ verdict
print("\n" + "="*72)
print("VERDICT")
print("="*72)
print("""  UNDERPOWERED / OUT-OF-RANGE (not FLAT-DISFAVORS, not BREAK-DETECTED).
  - Tian+2020 max y = 2.24 (canonical) / 1.86 (alt) < y_c = 2.894 -> the throttle
    break sits ABOVE the top edge of the cluster data on BOTH footings. Branch B is
    identically plain framework MOND everywhere Tian measures; there is no break in
    the data to find. Tian's clean slope-0.51 no-break fit therefore neither supports
    nor disfavors the throttle.
  - Even if the range were reached, the break is ~0.015-0.017 dex (n=1), ~3-4x under
    Tian's 0.059 dex intrinsic scatter and ~5-20x under the 0.1-0.3 dex systematic
    floor. Need ~0.01 dex precision at y~5-10; no cluster-RAR set reaches it.
  - The cluster deficit is real and shared-MOND: g_dagger=2.02e-9 = 21.6x canonical a0,
    framework MOND under-predicts g_obs by ~4.6x deep. The throttle does NOT worsen it
    in-hand (inactive below y_c; data stops at y=2.24). Branch B is cluster-viable in
    exactly the same (deficient) way plain MOND is -- the throttle adds no measurable
    cost, and its predicted worsening at y>y_c is beyond Tian's reach.""")
print("[exit 0]")
