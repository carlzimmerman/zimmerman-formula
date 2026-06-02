#!/usr/bin/env python3
"""
Widening the consequences of a0 = (c/2)sqrt(G rho) = cH/Z, responsibly.
======================================================================

PhD discipline: each result is derived, its assumptions stated, and labelled
  [DERIVED]  forced by algebra + standard (deep-)MOND;
  [FOLLOWS]  a clean but weaker consequence / interpretation;
  [LIMIT]    an honest place the framework FAILS or cannot be tested;
  [OPEN]     a real, currently-contested test.

We push into the solar system, clusters, the Machian reading, the acceleration hierarchy,
and the secular drift. Run: python <thisfile>   (needs numpy)
"""
import numpy as np

c, G, hbar, Msun, pc, kpc, AU, Mpc, yr = (2.99792458e8, 6.674e-11, 1.0546e-34, 1.989e30,
                                          3.0857e16, 3.0857e19, 1.496e11, 3.0857e22, 3.156e7)
OM, OL = 0.315, 0.685
Z = 2 * np.sqrt(8 * np.pi / 3)
H0 = 67.4e3 / Mpc
A0 = 1.2e-10
E = lambda z: np.sqrt(OM * (1 + z) ** 3 + OL)


def a_solar_system_efe():
    print("=" * 80); print("[A, DERIVED] why MOND is HIDDEN in the solar system: the Galactic field")
    print("=" * 80)
    V, R0 = 230e3, 8.2 * kpc                          # MW circular speed, Sun's radius
    g_ext = V ** 2 / R0
    print(f"  The Milky Way pulls on the Sun with g_ext = V^2/R0 = ({V/1e3:.0f} km/s)^2/(8.2 kpc)")
    print(f"     g_ext = {g_ext:.2e} m/s^2,   eta = g_ext/a0 = {g_ext/A0:.2f}.")
    print("  Since eta ~ 1.7 > 1, the solar system sits in a MODERATE external field: the External")
    print("  Field Effect partially Newtonises it, so deep-MOND deviations are SUPPRESSED locally.")
    print("  THIS is why MOND is not glaring in planetary orbits -- not because a0 is absent, but")
    print("  because the Galaxy's field exceeds it. [DERIVED]")
    print(f"  Evolution: eta(z) = g_ext/a0(z) = {g_ext/A0:.2f}/E(z); the Galactic field is ~fixed but")
    print("  a0 grew, so a comparable star+host at high z was DEEPER in MOND (the EFE 1/E(z) again).\n")


def b_secular_drift():
    print("=" * 80); print("[B, DERIVED but unmeasurable] the present-day drift of a0")
    print("=" * 80)
    dlnE_dz0 = 0.5 * 3 * OM / E(0) ** 2               # = 0.4725
    a0dot_over_a0 = -dlnE_dz0 * H0                    # d ln a0/dt at z=0 (a0 decreasing)
    per_yr = a0dot_over_a0 * yr
    print(f"  a0dot/a0 = d ln a0/dt = -(d ln E/dz) H0 = {a0dot_over_a0:.2e} /s = {per_yr:.1e} /yr.")
    print(f"  So a0 decreases by ~{abs(per_yr):.0e} per year -- a 1% change takes ~{0.01/abs(per_yr):.0e} yr.")
    print("  Real, but utterly unmeasurable by direct monitoring. The evolution is only accessible")
    print("  through HIGH-REDSHIFT galaxies, where E(z) is large -- not through local drift. [DERIVED]\n")


def c_cluster_problem():
    print("=" * 80); print("[C, LIMIT] the cluster residual-mass problem -- evolving a0 does NOT fix it")
    print("=" * 80)
    print("  MOND under-predicts galaxy-CLUSTER dynamical masses by a factor ~2 (the long-standing")
    print("  'MOND missing baryons in clusters'). Cluster-core accelerations are ~a0, so they ARE")
    print("  in the MOND regime, yet MOND gives only ~half the lensing/X-ray mass.")
    print("  Does the evolving scale help? The residual factor ~2 is seen mostly at z ~ 0-0.5, where")
    print("  a0(z) ~ a0(0) (E(0.3)=1.16, only +16%). So the evolution is far too small to supply the")
    print("  missing factor of 2 locally. Evolving a0 does NOT solve the cluster problem -- the same")
    print("  unsolved issue standard MOND has. (It may need real residual mass, e.g. sterile-nu/hot")
    print("  dark matter in clusters, or the relativistic sector's extra fields.) [LIMIT -- stated plainly]\n")


def e_mach_horizon():
    print("=" * 80); print("[E, FOLLOWS] the Machian reading, quantified: MOND onset = the cosmic horizon")
    print("=" * 80)
    RH = c / H0
    print(f"  Rewrite a0 = cH/Z = c^2/(Z R_H), R_H = c/H = {RH/Mpc:.0f} Mpc the Hubble radius.")
    print("  A particle accelerating at g has a Rindler (acceleration) horizon at distance c^2/g.")
    print("  Setting that horizon equal to the cosmic horizon, c^2/g = Z R_H, gives g = c^2/(Z R_H) = a0.")
    print("  => MOND switches on EXACTLY when a particle's acceleration-horizon reaches ~the cosmic")
    print("     horizon (within the factor Z). Inertia 'below a0' is where local and cosmic horizons")
    print("     merge -- a concrete realisation of Mach's principle / horizon thermodynamics. [FOLLOWS]\n")


def f_acceleration_hierarchy():
    print("=" * 80); print("[F, FOLLOWS] where a0 sits: the acceleration hierarchy of nature")
    print("=" * 80)
    Lp = np.sqrt(G * hbar / c ** 3)
    a_planck = c ** 2 / Lp
    a_floor = A0 * np.sqrt(OL)
    print(f"   {'scale':28}{'a [m/s^2]':>14}")
    for name, a in [("de Sitter floor (a0 min)", a_floor), ("a0 today", A0),
                    ("Earth surface gravity", 9.81), ("Planck acceleration (max)", a_planck)]:
        print(f"   {name:28}{a:>14.2e}")
    span = np.log10(a_planck / a_floor)
    gm = np.sqrt(a_floor * a_planck)
    print(f"  Accelerations span ~{span:.0f} orders of magnitude, floor (Lambda) to ceiling (Planck).")
    print(f"  a0 sits near the COSMIC-MINIMUM end -- a0 is small BECAUSE the universe is old and")
    print(f"  dilute (a0 ~ sqrt(G rho_cosmic)). The geometric mean is {gm:.1e} (NOT a0), so the naive")
    print("  'a0 = geometric mean of Planck and Hubble' large-number coincidence does NOT hold. [FOLLOWS]\n")


def g_wide_binaries():
    print("=" * 80); print("[G, OPEN] wide binary stars -- the local deep-MOND test, EFE-complicated")
    print("=" * 80)
    s = 1e4 * AU
    g_int = G * (1.5 * Msun) / s ** 2
    print(f"  A wide binary at separation ~1e4 AU has internal g = GM/s^2 ~ {g_int:.1e} m/s^2 ~ "
          f"{g_int/A0:.1f} a0,")
    print("  i.e. nominally deep-MOND. BUT the Galactic field (eta~1.7 a0, [A]) exceeds it, so the")
    print("  binaries are in the EFE regime and the predicted MOND boost is partly suppressed and")
    print("  orientation-dependent. This is exactly why the wide-binary test is hard and currently")
    print("  CONTESTED (Chae finds a MOND signal; Pittordis-Sutherland and others do not). The")
    print("  evolving a0 makes no NEW local prediction here (z~0). A genuine, unsettled frontier. [OPEN]\n")


def main():
    a_solar_system_efe(); b_secular_drift(); c_cluster_problem()
    e_mach_horizon(); f_acceleration_hierarchy(); g_wide_binaries()
    print("=" * 80); print("LEDGER -- widened consequences, by honesty class")
    print("=" * 80)
    print("  DERIVED: solar-system EFE hides MOND locally (eta~1.7) [A]; the secular drift is real")
    print("           but ~1e-11/yr, unmeasurable [B].")
    print("  FOLLOWS: MOND onset = local acceleration-horizon meeting the cosmic horizon (Mach) [E];")
    print("           a0 sits at the cosmic-minimum end of a ~62-order acceleration hierarchy [F].")
    print("  LIMIT:   the galaxy-cluster factor-of-2 residual mass is NOT fixed by evolving a0 [C].")
    print("  OPEN:    wide binaries -- a real local deep-MOND test, EFE-complicated and contested [G].")
    print("  PhD bottom line: the framework explains why MOND hides locally and gives a clean Machian")
    print("  reading, but it inherits standard MOND's cluster failure and adds no new LOCAL test -- the")
    print("  distinctive content remains the HIGH-Z evolution, not anything in the solar neighbourhood.")
    print("=" * 80)


if __name__ == "__main__":
    main()
