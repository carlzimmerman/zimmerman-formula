#!/usr/bin/env python3
"""
JWST high-z test of an evolving MOND scale: exact predicted rotation speeds.
===========================================================================

Pre-registered, fixed-coefficient predictions for the one falsifiable claim:
    a0(z) = a0(0) * E(z),  E(z) = sqrt(Om(1+z)^3 + OL)  (Z-INDEPENDENT).

Deep-MOND baryonic Tully-Fisher (parameter-free for rotation):
    v_flat = (G * M_bar * a0(z))^(1/4)          [f_geom = 1, exact]
    sigma  = (4/9)^(1/4) * v_flat = 0.816 v_flat [isothermal sphere]

Coefficients fixed in advance (no per-galaxy tuning). Stellar masses from JWST
SED fits (uncertain ~0.3-0.5 dex -> ~20-30% in v); gas would raise v by ~(M_bar/M*)^1/4.

Pure stdlib.  Run:  python reviews/jwst_rotation_predictions.py
"""

import math

A0 = 1.2e-10        # m/s^2
OM, OL = 0.315, 0.685
G = 6.674e-11
MSUN = 1.989e30

def E(z): return math.sqrt(OM * (1 + z) ** 3 + OL)
def vflat(M_solar, z, evolving=True):
    a0 = A0 * (E(z) if evolving else 1.0)
    return (G * M_solar * MSUN * a0) ** 0.25 / 1e3   # km/s

# (name, z, log10(M*/Msun), reference, measured-so-far)
TARGETS = [
    ("GN-z11",          10.60, 9.0, "Tacchella+23 / Xu+24",
        "MEASURED: v_rot=257(+138/-117), sigma=91(+18/-32)"),
    ("GHZ2 / GLASS-z12", 12.34, 8.9, "Castellano+24 / Calabro+24", "not yet measured"),
    ("JADES-GS-z14-0",  14.32, 8.6, "Carniani+24", "not yet measured"),
    ("MoM-z14-0",       14.44, 8.7, "Naidu+25", "not yet measured"),
]

# mass uncertainty -> velocity uncertainty: v ~ M^(1/4); use +/-0.35 dex
DEX = 0.35
VFRAC = 10 ** (DEX / 4) - 1   # ~+/- factor in v

def main():
    print("=" * 92)
    print("Predicted rotation speed v_flat (km/s): a0 EVOLVING vs CONSTANT  [+/-%.0f%% from mass]"
          % (VFRAC * 100))
    print("=" * 92)
    print(f"  {'galaxy':<18}{'z':>6}{'M*':>10}{'E(z)':>7}"
          f"{'v_EVOLVING':>13}{'v_const':>10}{'sigma_evo':>11}{'factor':>8}")
    for name, z, logM, ref, meas in TARGETS:
        M = 10 ** logM
        ve, vc = vflat(M, z, True), vflat(M, z, False)
        se = 0.816 * ve
        dv = VFRAC * ve
        print(f"  {name:<18}{z:>6.1f}{M:>10.1e}{E(z):>7.1f}"
              f"   {ve:>4.0f}+/-{dv:<3.0f}{vc:>9.0f}{se:>11.0f}{ve/vc:>8.2f}")
    print()
    print("  sigma_evo = isothermal dispersion (0.816 v_flat); constant-a0 sigma = 0.816 v_const.")
    print()
    print("=" * 92)
    print("THE TEST (what to send)")
    print("=" * 92)
    print("  * Evolving a0:  v_flat ~ 120-140 km/s  (sigma ~ 100-115 km/s) at z = 12-14.5")
    print("  * Constant a0:  v_flat ~  50-60  km/s  (sigma ~  40-50  km/s)")
    print("  * They differ by a FACTOR ~2.2-2.4 (= E(z)^1/4), far larger than the ~25-30%")
    print("    mass-uncertainty band -- so a single NIRSpec line width or resolved")
    print("    velocity gradient at z>12 separates them cleanly.")
    print()
    print("  GN-z11 (the only z>10 galaxy measured so far): predicted v_flat=137, sigma=112,")
    print("  consistent within ~1 sigma with v_rot=257(+138/-117), sigma=91(+18/-32).")
    print()
    print("  FALSIFIER: if GHZ2 / JADES-GS-z14 / MoM-z14 come in near the CONSTANT-a0")
    print("  values (~50-60 km/s rotation, ~40-50 km/s dispersion), the evolving-a0")
    print("  hypothesis is dead.")
    print()
    print("  CAVEATS to state honestly: v_flat is the asymptotic deep-MOND value (valid")
    print("  where internal a < a0(z)); the measured velocity at the half-light radius may")
    print("  be lower for compact systems. Masses are stellar (lower bound on baryonic).")
    print("  The sharp, model-independent test is the REDSHIFT TREND of the BTFR zero-point,")
    print("  not any single galaxy. LCDM dark-matter halos predict a different M-v scaling")
    print("  and are a separate comparison.")


if __name__ == "__main__":
    main()
