#!/usr/bin/env python3
"""
PRE-REGISTERED prediction: evolving MOND scale a0(z) at z > 10.
==============================================================

The one distinctive, framework-specific, falsifiable claim of v12:
    a0(z) = a0(0) * E(z),   E(z) = H(z)/H0 = sqrt(Om(1+z)^3 + OL).
This is Z-INDEPENDENT (Z sets only the z=0 normalization and cancels here). It
distinguishes evolving-a0 MOND from constant-a0 MOND and from LCDM.

Observable: the deep-MOND baryonic Tully-Fisher relation
    v_flat^4 = G * M_bar * a0(z)        (rotation; NO free parameter)
    sigma   = (4/9)^(1/4) * v_flat       (isothermal-sphere dispersion; fixed coeff)

PRE-REGISTRATION (timestamp 2026-05-31): the geometric coefficients are FIXED here
in advance -- f_geom = 1 for v_flat (exact MOND BTFR), and (4/9)^(1/4)=0.816 for the
isothermal dispersion. No per-galaxy tuning. Predictions for named z>10 galaxies
below are to be tested when their kinematics are measured (JWST/NIRSpec-IFU, ELT).

Pure stdlib.  Run:  python reviews/a0_evolution_predictions.py
"""

import math

A0 = 1.2e-10          # m/s^2, a0(z=0)
OM, OL = 0.315, 0.685
G = 6.674e-11
MSUN = 1.989e30
KMS = 1e3

def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)

def v_flat(M_star_solar, z, evolving=True):
    a0 = A0 * (E(z) if evolving else 1.0)
    v = (G * M_star_solar * MSUN * a0) ** 0.25     # m/s
    return v / KMS

# named z>10 galaxies: (name, z, M_star[Msun], measured kinematics or None)
GALAXIES = [
    ("GN-z11",          10.60, 1.0e9, {"sigma": (91, 18, 32), "vrot": (257, 138, 117)}),
    ("GHZ2 / GLASS-z12", 12.34, 8.0e8, None),
    ("JADES-GS-z14-0",  14.32, 4.0e8, None),
    ("MoM-z14 (cand.)", 14.44, 5.0e8, None),
]


def main():
    print("=" * 84)
    print("PRE-REGISTERED z>10 prediction (a0 evolving vs constant), fixed coefficients")
    print("=" * 84)
    print(f"  a0(0)={A0:.1e}, Om={OM}, OL={OL};  v_flat=(G M a0)^1/4, sigma=0.816 v_flat\n")
    print(f"  {'galaxy':<18}{'z':>6}{'M*':>9}{'E(z)':>7}"
          f"{'v_evolv':>9}{'v_const':>9}{'ratio':>7}{'sig_evolv':>10}   measured")
    for name, z, M, meas in GALAXIES:
        ve = v_flat(M, z, True)
        vc = v_flat(M, z, False)
        se = 0.816 * ve
        ms = ""
        if meas:
            if "sigma" in meas:
                s, ep, em = meas["sigma"]; ms += f"sigma={s}(+{ep}/-{em}) "
            if "vrot" in meas:
                v, ep, em = meas["vrot"]; ms += f"vrot={v}(+{ep}/-{em})"
        print(f"  {name:<18}{z:>6.1f}{M:>9.1e}{E(z):>7.1f}"
              f"{ve:>9.0f}{vc:>9.0f}{ve/vc:>7.2f}{se:>10.0f}   {ms}")
    print()
    print("  Units: velocities in km/s. 'ratio' = v_evolv/v_const = E(z)^(1/4).")
    print()
    print("=" * 84)
    print("THE TEST")
    print("=" * 84)
    print("  * Evolving-a0 predicts v_flat ~ 120-140 km/s at z>10; constant-a0 MOND")
    print("    predicts ~50-65 km/s -- a factor ~2.2-2.4 difference (= E(z)^1/4).")
    print("  * That gap EXCEEDS the stellar-mass uncertainty (~0.3-0.5 dex -> ~20-30% in")
    print("    v_flat), so the regimes are cleanly separable once kinematics are measured.")
    print("  * GN-z11 (the only z>10 galaxy with measured kinematics): the FIXED-coefficient")
    print("    prediction v_flat=137 km/s and sigma=112 km/s are consistent within ~1 sigma")
    print("    with vrot=257(+138/-117) and sigma=91(+18/-32) -- NOT the tuned '0.0 sigma'")
    print("    of v11 (which used f_geom=1.5); honest consistency, noisy.")
    print()
    print("  FALSIFIER: if the measured v_flat/sigma of GHZ2, JADES-GS-z14, or future z>12")
    print("  galaxies track the CONSTANT-a0 values (~50-65 km/s) or LCDM dark-matter halos")
    print("  rather than the evolving values (~120-140 km/s), a0(z) ~ H(z) is falsified.")
    print()
    print("  CAVEATS (honest): masses are stellar (gas would raise v_flat by ~2^0.25=1.19);")
    print("  v_flat is the asymptotic deep-MOND value (a<a0(z)) -- compact cores may be")
    print("  Newtonian; the prediction assumes MOND (no dark matter). The discriminator is")
    print("  the redshift TREND of the BTFR zero-point, robust to the overall normalization.")


if __name__ == "__main__":
    main()
