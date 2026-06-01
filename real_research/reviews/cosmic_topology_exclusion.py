#!/usr/bin/env python3
"""
Is the 20.6 Gpc cubic-T^3 universe excluded? Planck 2015 vs 2018 -- and the
"why not Planck18?" question, answered with numbers.
===========================================================================

Context: the framework posits a cubic 3-torus with fundamental-domain edge
L = 20.6 Gpc, so the largest inscribed sphere has radius R_i = L/2 = 10.3 Gpc.
Planck's topology bound (cubic T^3, Bayesian, Delta ln L > -5): R_i > 0.97 chi_rec,
where chi_rec is the comoving distance to last scattering (~14 Gpc). The
matched-circles search equivalently requires the shortest non-contractible loop
> ~0.985 of the LSS comoving DIAMETER (= 2 chi_rec).

A skeptic asked: "why refer to Planck 2015 and not Planck 2018?" Two honest
answers, one factual and one numerical:

  (factual) There is NO dedicated Planck 2018 topology paper. The topology
    analyses are Planck 2013 (XXVI) and Planck 2015 (XVIII). The 2018 release
    (VI parameters; VII isotropy & statistics) folded geometry into the
    curvature constraint but did not repeat the matched-circle / Bayesian
    topology search. So Planck 2015 XVIII IS the latest dedicated Planck word.

  (numerical) It does not matter: this script recomputes chi_rec under BOTH the
    Planck 2015 and Planck 2018 parameter sets and shows the 20.6 Gpc cubic
    torus is excluded under EITHER. The bound is cosmic-variance-limited (it
    lives in the largest CMB scales), so 2018 cannot move it.

Pure stdlib. Run:  python reviews/cosmic_topology_exclusion.py
"""

import math

C_KMS = 299792.458    # km/s
Z_REC = 1089.9        # redshift of last scattering (Planck)

# (name, H0 [km/s/Mpc], Omega_m, Omega_r). Omega_Lambda = 1 - Om - Or (flat).
PARAMS = [
    ("Planck 2015 (XVIII params)", 67.8, 0.308, 9.1e-5),
    ("Planck 2018 (VI params)",    67.4, 0.315, 9.1e-5),
]

L_FRAME = 20.6        # Gpc, the framework's cubic fundamental-domain edge
R_I_FRAME = L_FRAME / 2.0   # inscribed-sphere radius = 10.3 Gpc
BOUND_FRAC = 0.97     # Planck 2015 XVIII cubic-T^3 Bayesian bound: R_i > 0.97 chi_rec


def E(z, Om, Or):
    OL = 1.0 - Om - Or
    return math.sqrt(Or * (1 + z) ** 4 + Om * (1 + z) ** 3 + OL)


def chi_rec_Gpc(H0, Om, Or, n=400000):
    """Comoving distance to last scattering, in Gpc (trapezoidal integration)."""
    # chi = (c/H0) * integral_0^zrec dz/E(z)
    dz = Z_REC / n
    s = 0.0
    for i in range(n + 1):
        z = i * dz
        w = 0.5 if (i == 0 or i == n) else 1.0
        s += w / E(z, Om, Or)
    integral = s * dz
    DH_Mpc = C_KMS / H0          # Hubble distance in Mpc
    return DH_Mpc * integral / 1e3   # Mpc -> Gpc


def main():
    print("=" * 80)
    print("Cubic T^3 topology: is R_i = 10.3 Gpc (L = 20.6 Gpc) excluded?")
    print("=" * 80)
    print(f"  framework: cubic torus edge L = {L_FRAME} Gpc -> R_i = L/2 = "
          f"{R_I_FRAME} Gpc")
    print(f"  Planck cubic-T^3 bound: R_i > {BOUND_FRAC} * chi_rec")
    print()
    print(f"  {'parameter set':<30}{'chi_rec':>9}{'0.97 chi_rec':>14}"
          f"{'R_i=10.3?':>12}{'shortfall':>11}")
    for name, H0, Om, Or in PARAMS:
        chi = chi_rec_Gpc(H0, Om, Or)
        bound = BOUND_FRAC * chi
        verdict = "EXCLUDED" if R_I_FRAME < bound else "allowed"
        short = (bound - R_I_FRAME) / bound * 100
        print(f"  {name:<30}{chi:>8.2f} {bound:>13.2f} {verdict:>12}{short:>+10.1f}%")
    print()
    print("  Also the matched-circles form (shortest loop vs LSS diameter 2*chi_rec):")
    for name, H0, Om, Or in PARAMS:
        chi = chi_rec_Gpc(H0, Om, Or)
        diam = 2 * chi
        loop_bound = 0.985 * diam
        verdict = "EXCLUDED" if L_FRAME < loop_bound else "allowed"
        print(f"    {name:<28} loop L={L_FRAME} Gpc  vs  0.985*diam="
              f"{loop_bound:.1f} Gpc  -> {verdict}")
    print()
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    print("  * EXCLUDED under BOTH Planck 2015 and Planck 2018 parameters, by ~24%.")
    print("    The 15-vs-18 distinction is moot: chi_rec shifts <0.5% between them,")
    print("    nowhere near enough to rescue a 24% shortfall.")
    print("  * 'Why Planck15 not Planck18?' -- because there is NO dedicated Planck")
    print("    2018 topology paper; 2015 XVIII is the latest. And the bound is")
    print("    cosmic-variance-limited (largest CMB scales), so 2018's better")
    print("    polarization / integration adds no new independent modes to move it.")
    print()
    print("  HONEST caveat (the real, current counter-argument -- not Planck18):")
    print("    The COMPACT collaboration (2024, PRL 132 171501) argues CMB does NOT")
    print("    exclude as many topologies as folklore claims. TRUE -- but that")
    print("    rescues topologies AT or BEYOND the horizon (and anisotropic/general")
    print("    manifolds), where there are no matched circles to find. It does NOT")
    print("    rescue a cubic T^3 whose domain sits INSIDE the horizon (R_i=10.3 <<")
    print("    chi_rec~14): that case WOULD show matched circles, and none are seen.")
    print("    So the strongest pro-topology argument still leaves THIS model dead.")


if __name__ == "__main__":
    main()
