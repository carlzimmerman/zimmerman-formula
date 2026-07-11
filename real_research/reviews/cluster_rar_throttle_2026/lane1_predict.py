#!/usr/bin/env python3
"""
LANE 1 -- Branch B throttled cluster RAR: the PREDICTION and the KILL-CHECK.

Framework-first (modified INERTIA), NOT standard MOND:
  - horizon a0 = c H_Lambda / Z, Z = sqrt(32 pi / 3) = 5.789
  - framework's OWN dS-Unruh interpolation nu(y) = sqrt(1 + 1/y),  y = g_bar / a0
      (g_obs = nu * g_bar reproduces g_obs = sqrt(g_bar^2 + g_bar a0) since
       nu = sqrt(1 + 1/y), g_obs = nu g_bar = g_bar sqrt(1+ a0/g_bar) = sqrt(g_bar^2 + g_bar a0). CHECK.)
  - Branch B elastic dark-ENERGY medium (Zenodo 21303747) has a DERIVED response
    cutoff at y_c = Z/2 = 2.894 (Verlinde entropy-budget pin, Zenodo 21300855).
  - Throttle (depletion reading, n=1 minimal budget-consistent; n=2 bracket):
        T(y) = min(1, (y_c / y)^n)
        g_obs = [1 + (nu(y) - 1) T(y)] g_bar
    Below y_c: T=1 -> standard MOND-like boost.
    Above y_c: T<1 -> the phantom boost DEPLETES.

Two footings for a0 (both reported; y_c is dimensionless, fixed by construction):
  canonical: a0 = 9.36e-11  (rho_DE / c H_Lambda)
  alt:       a0 = 1.13e-10  (rho_total / c H0)

Cluster regime: y ~ 1-30 (cores high-y/high-accel -> mid-radii lower-y).

Prove-by-moving-the-number: every load-bearing quantity printed, no free knobs.
"""
import numpy as np

# ------------------------------------------------------------------ constants
Z   = np.sqrt(32.0 * np.pi / 3.0)      # 5.7888...
y_c = Z / 2.0                          # 2.8944...  Verlinde-budget cutoff
A0_CANON = 9.36e-11                    # m/s^2  canonical (pure-Lambda)
A0_ALT   = 1.13e-10                    # m/s^2  alt footing

def nu(y):
    """framework dS-Unruh interpolation; y = g_bar/a0."""
    return np.sqrt(1.0 + 1.0 / y)

def throttle(y, n=1):
    return np.minimum(1.0, (y_c / y) ** n)

def g_ratio_mond(y):
    """plain MOND (T=1): g_obs/g_bar = nu."""
    return nu(y)

def g_ratio_throttled(y, n=1):
    """Branch B throttled: g_obs/g_bar = 1 + (nu-1)T."""
    return 1.0 + (nu(y) - 1.0) * throttle(y, n)

def break_dex(y, n=1):
    """deviation of throttled from plain MOND, in dex (log10)."""
    return np.log10(g_ratio_mond(y) / g_ratio_throttled(y, n))

print("=" * 74)
print("LANE 1 -- Branch B throttled cluster RAR: PREDICTION + KILL-CHECK")
print("=" * 74)
print(f"Z = sqrt(32pi/3)         = {Z:.6f}")
print(f"y_c = Z/2 (break locus)  = {y_c:.6f}   (dimensionless -> footing-independent)")
print(f"a0 canonical             = {A0_CANON:.3e} m/s^2")
print(f"a0 alt                   = {A0_ALT:.3e} m/s^2")
print(f"physical g_bar AT break  = y_c*a0:  canon {y_c*A0_CANON:.3e},  alt {y_c*A0_ALT:.3e} m/s^2")
print()

# ------------------------------------------------------------------ (1) THE BREAK
print("-" * 74)
print("(1) THE FINGERPRINT / BREAK  (deviation of throttled RAR from plain MOND)")
print("-" * 74)
print("    Delta(y) = log10[ (1+(nu-1)) / (1+(nu-1)T) ]   in dex")
print("    (extends the banked SPARC fingerprint: 0.017 dex at y~6)")
print()
hdr = f"{'y':>6} {'g_bar_canon':>12} {'nu-1':>9} {'T(n=1)':>8} {'T(n=2)':>8} " \
      f"{'dex n=1':>9} {'dex n=2':>9}"
print(hdr)
for y in [1, 2, 2.894, 3, 5, 7, 10, 15, 20, 30]:
    gbar = y * A0_CANON
    line = (f"{y:>6.3f} {gbar:>12.3e} {nu(y)-1:>9.4f} "
            f"{throttle(y,1):>8.4f} {throttle(y,2):>8.4f} "
            f"{break_dex(y,1):>9.4f} {break_dex(y,2):>9.4f}")
    print(line)
print()

# locate the peak of the fingerprint
ygrid = np.linspace(y_c, 30, 20000)
d1 = break_dex(ygrid, 1)
d2 = break_dex(ygrid, 2)
print(f"    n=1 fingerprint PEAK: {d1.max():.4f} dex at y = {ygrid[d1.argmax()]:.3f}")
print(f"    n=2 fingerprint PEAK: {d2.max():.4f} dex at y = {ygrid[d2.argmax()]:.3f}")
print(f"    => same order as banked SPARC 0.017 dex @ y~6; peaks in the")
print(f"       cluster mid-radius band, DECLINES again toward the high-y cores.")
print()

# report the requested y = 3,5,10,20 explicitly
print("    Requested points (dex):")
for y in [3, 5, 10, 20]:
    print(f"      y={y:>3}:  n=1 {break_dex(y,1):.4f} dex   n=2 {break_dex(y,2):.4f} dex")
print()

# ------------------------------------------------------------------ (2) KILL-CHECK
print("-" * 74)
print("(2) KILL-CHECK -- does the throttle WORSEN the known cluster deficit?")
print("-" * 74)
print("    Known context: clusters have a RESIDUAL DEFICIT -- MOND (and the")
print("    framework's shared MOND-limit) UNDER-predicts cluster lensing mass")
print("    by ~2-10x, WORST in the high-accel CORES. eta(R500) ~ 1.0-1.3.")
print("    The throttle DEPLETES the boost above y_c -> removes phantom exactly")
print("    where clusters already need MORE.  Quantify the harm.")
print()
print("    Depletion removed from g_obs/g_bar:  D(y) = (nu-1)(1-T)")
print("    Fractional change in predicted g_obs vs plain MOND:")
print("        frac = g_throttled/g_mond - 1 = [1+(nu-1)T]/nu - 1  (<=0, a LOSS)")
print()
hdr2 = f"{'y':>6} {'nu-1':>9} {'(nu-1)(1-T) n=1':>16} {'%loss g_obs n=1':>16} {'%loss g_obs n=2':>16}"
print(hdr2)
for y in [3, 5, 7, 10, 15, 20, 30, 50]:
    D1 = (nu(y)-1)*(1-throttle(y,1))
    fr1 = 100.0*(g_ratio_throttled(y,1)/g_ratio_mond(y) - 1.0)
    fr2 = 100.0*(g_ratio_throttled(y,2)/g_ratio_mond(y) - 1.0)
    print(f"{y:>6.1f} {nu(y)-1:>9.4f} {D1:>16.4f} {fr1:>16.2f} {fr2:>16.2f}")
print()

# worst-case loss over the cluster core-to-mid band y in [3,50]
yb = np.linspace(3, 50, 50000)
loss1 = 100.0*(g_ratio_throttled(yb,1)/g_ratio_mond(yb) - 1.0)
loss2 = 100.0*(g_ratio_throttled(yb,2)/g_ratio_mond(yb) - 1.0)
print(f"    WORST %loss in g_obs over cluster band y in [3,50]:")
print(f"      n=1:  {loss1.min():.2f}%  at y={yb[loss1.argmin()]:.2f}")
print(f"      n=2:  {loss2.min():.2f}%  at y={yb[loss2.argmin()]:.2f}")
print()

# effect on eta: eta_throttled = eta_mond * (g_throttled/g_mond)
# take representative eta_mond over the shared-MOND deficit range
print("    Effect on the eta(R500) deficit  (eta_new = eta_MOND * g_throttled/g_mond):")
print("    (a LARGER eta = worse deficit; here g_throttled<g_mond LOWERS predicted")
print("     lensing g_obs, so to match data eta must RISE by the same factor)")
for eta_m in [1.0, 1.3, 2.0]:
    # representative mid-radius y~5 and core y~15
    for y in [5, 15]:
        fac = g_ratio_mond(y)/g_ratio_throttled(y,1)  # extra deficit factor n=1
        print(f"      eta_MOND={eta_m:.1f}, y={y:>3}:  eta_new(n=1) = {eta_m*fac:.4f}  "
              f"(+{100*(fac-1):.2f}%)")
print()

# ------------------------------------------------------------------ (3) FOOTINGS
print("-" * 74)
print("(3) BOTH FOOTINGS + cluster-a0-offset context")
print("-" * 74)
print("    The break is in DIMENSIONLESS y; y_c=2.894 fixed by Z -> the dex")
print("    fingerprint Delta(y) is IDENTICAL on both footings.  Only the PHYSICAL")
print("    acceleration of the break shifts:")
print(f"      canonical a0=9.36e-11 : break at g_bar = {y_c*A0_CANON:.3e} m/s^2")
print(f"      alt       a0=1.13e-10 : break at g_bar = {y_c*A0_ALT:.3e} m/s^2")
print(f"      ratio = {A0_ALT/A0_CANON:.3f}x  (=alt/canon)")
print()
print("    Tian+2020 cluster-a0 offset context: CLASH RAR fits an EFFECTIVE")
print("    a0_cluster ~ 5-10x the galaxy a0. In the framework's own y = g_bar/a0")
print("    (a0 = framework value, NOT the fitted cluster value), a FIXED physical")
print("    g_bar maps to the SAME y on both footings up to the 1.2x a0 ratio.")
print("    With canonical a0, cluster cores (g_bar ~ 1e-9) sit at y ~ 10.7, mid")
print("    radii (g_bar ~ 2-3e-10) at y ~ 2-3 -> straddles y_c. The throttle")
print("    break IS inside the CLASH acceleration window.")
gb_core, gb_mid = 1.0e-9, 2.5e-10
print(f"      g_bar core  ~ {gb_core:.1e}: y_canon={gb_core/A0_CANON:.2f}, y_alt={gb_core/A0_ALT:.2f}")
print(f"      g_bar mid   ~ {gb_mid:.1e}: y_canon={gb_mid/A0_CANON:.2f}, y_alt={gb_mid/A0_ALT:.2f}")
print()

# ------------------------------------------------------------------ VERDICT
print("=" * 74)
print("LANE 1 VERDICT")
print("=" * 74)
peak1 = d1.max(); peak1_y = ygrid[d1.argmax()]
print(f" * BREAK SIZE: a KINK at y_c={y_c:.3f}, fingerprint peaks {peak1:.3f} dex "
      f"(n=1)")
print(f"   at y~{peak1_y:.1f}, {d2.max():.3f} dex (n=2). Order 0.01-0.03 dex in the")
print(f"   cluster band -- extends the banked SPARC 0.017 dex @ y~6.")
print(f" * KILL-CHECK: throttle lowers predicted cluster g_obs by AT MOST "
      f"{abs(loss1.min()):.1f}% (n=1),")
print(f"   {abs(loss2.min()):.1f}% (n=2) over y in [3,50]. Because nu-1 is ALREADY")
print(f"   small at high y (Newtonian regime), the depleted boost is tiny.")
print(f" * vs the cluster deficit (2-10x = 100-900%%): the throttle worsens eta by")
print(f"   only a few %% -> NEGLIGIBLY AFFECTS the deficit. NOT a cure, NOT a kill.")
print(f"   The residual cluster deficit is SHARED-MOND, not Branch-B-specific.")
print(f" * FOOTINGS: dex fingerprint footing-independent; physical break locus")
print(f"   {y_c*A0_CANON:.2e} (canon) vs {y_c*A0_ALT:.2e} m/s^2 (alt).")
print("=" * 74)
