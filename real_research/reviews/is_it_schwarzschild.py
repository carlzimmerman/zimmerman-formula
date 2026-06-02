#!/usr/bin/env python3
"""
Can we PROVE the factor of 2 is Schwarzschild?  -- chase the horizon structure down.
====================================================================================

There IS a clean Schwarzschild fact in the cosmology, and it is worth taking seriously:
the Hubble sphere is its OWN Schwarzschild radius. So a horizon surface gravity is a
legitimate candidate for a0. We follow it to the end and see exactly where it lands --
and why the data then block it.

a0 (framework) = (c/2) sqrt(G rho_c) = c^2/(2R),  R = c/sqrt(G rho_c) = cH/Z, Z=2sqrt(8pi/3).

Run: python <thisfile>   (needs numpy)
"""
import numpy as np

c, G, Mpc = 2.99792458e8, 6.674e-11, 3.0857e22
H0 = 67.4e3 / Mpc
rho_c = 3 * H0 ** 2 / (8 * np.pi * G)
RH = c / H0
A0_OBS = 1.2e-10


def main():
    print("=" * 82)
    print("STEP 1 -- the clean Schwarzschild fact: the Hubble sphere is its own horizon")
    print("=" * 82)
    M_H = (4 * np.pi / 3) * rho_c * RH ** 3        # mass within the Hubble radius
    Rs_MH = 2 * G * M_H / c ** 2                    # its Schwarzschild radius
    print(f"  Hubble radius      R_H        = {RH/Mpc:.0f} Mpc")
    print(f"  mass within R_H    M_H        = {M_H:.3e} kg")
    print(f"  Schwarzschild rad. R_s(M_H)   = {Rs_MH/Mpc:.0f} Mpc   ->  R_s(M_H)/R_H = {Rs_MH/RH:.3f}")
    print("  So R_s(M_H) = R_H EXACTLY: the Hubble sphere IS a Schwarzschild horizon.")
    print("  This is real, and it makes 'horizon surface gravity' a legitimate candidate for a0.\n")

    print("=" * 82)
    print("STEP 2 -- the surface gravity there, and what a0 it predicts")
    print("=" * 82)
    g_surf = c ** 2 / (2 * RH)                      # Schwarzschild surface gravity at R_H
    print(f"  surface gravity at the cosmic horizon  g = c^2/(2 R_H) = cH/2 = {g_surf:.3e} m/s^2")
    print(f"  => this IS a clean Schwarzschild a0 candidate, with Z = 2.")
    print(f"  But:  cH/2 = {g_surf*1e10:.2f}e-10  vs observed a0 = {A0_OBS*1e10:.2f}e-10")
    print(f"        ratio = {g_surf/A0_OBS:.1f}x TOO BIG.")
    print("  The clean Schwarzschild value (Z=2) is RULED OUT by SPARC by a factor ~2.7.\n")

    print("=" * 82)
    print("STEP 3 -- where the framework's radius actually sits (and why it is NOT a horizon)")
    print("=" * 82)
    R_fw = c / np.sqrt(G * rho_c)                   # framework radius
    M_fw = (4 * np.pi / 3) * rho_c * R_fw ** 3
    Rs_fw = 2 * G * M_fw / c ** 2
    print(f"  framework R = c/sqrt(G rho_c) = {R_fw/RH:.3f} R_H = sqrt(8pi/3) R_H (LARGER than R_H)")
    print(f"  mass within R: its Schwarzschild radius R_s = {Rs_fw/R_fw:.2f} R = 8pi/3 R = {Rs_fw/RH:.1f} R_H")
    print(f"  so the enclosed mass's horizon ({Rs_fw/RH:.0f} R_H) is 8.4x BEYOND R: R is deep INSIDE")
    print("  its own would-be horizon. 'c^2/2R' at the framework R is therefore NOT a surface")
    print("  gravity -- it is the Schwarzschild FORM applied to a non-horizon radius.\n")

    print("=" * 82)
    print("STEP 4 -- the gap, named exactly")
    print("=" * 82)
    print(f"  a0(framework) / (cH/2)  =  2/Z  =  {2/(2*np.sqrt(8*np.pi/3)):.3f}  =  1/sqrt(8pi/3).")
    print("  i.e. the framework = (Hubble-horizon surface gravity) DIVIDED by sqrt(8pi/3).")
    print("  sqrt(8pi/3) is exactly the ratio H/sqrt(G rho) -- the HUBBLE rate over the FREE-FALL")
    print("  rate. So the framework replaces the expansion rate H by the local collapse rate")
    print("  sqrt(G rho). That substitution is physically motivated (MOND is local dynamics, not")
    print("  global expansion) -- but it is the POSIT; it is not horizon physics.\n")

    print("=" * 82)
    print("STEP 5 -- scan the actual cosmological horizons: does ANY give Z=5.789?")
    print("=" * 82)
    print(f"  {'horizon':28}{'R/R_H':>7}{'Z=2 R/R_H':>11}{'a0(0)':>8}")
    for name, x in [("Hubble / apparent horizon", 1.00), ("event horizon (LCDM today)", 1.12),
                    ("framework radius (NOT a horizon)", np.sqrt(8*np.pi/3)),
                    ("particle horizon (observable U)", 3.23)]:
        Z = 2 * x                                   # surface gravity c^2/2(x R_H) = cH/(2x)
        a0 = c * H0 / Z * 1e10
        print(f"  {name:28}{x:>7.2f}{Z:>11.2f}{a0:>8.2f}")
    print("  The framework's Z=5.789 needs a horizon at 2.894 R_H. No standard horizon sits there:")
    print("  the apparent horizon gives Z=2 (a0 too big); the particle horizon gives Z~6.5 (a0 a")
    print("  bit too small, ~Milgrom/Verlinde). 5.789 falls in the gap, matching none.\n")

    print("=" * 82)
    print("VERDICT -- can we prove it is Schwarzschild?  No, and the data say why.")
    print("=" * 82)
    print("  * The cleanest Schwarzschild structure is REAL: the Hubble sphere is its own")
    print("    Schwarzschild radius, surface gravity cH/2. But that is Z=2, and SPARC RULES IT")
    print("    OUT (a0 would be ~2.7x too big). So the clean Schwarzschild a0 is the WRONG number.")
    print("  * The framework's correct a0 needs Z=5.789, i.e. the horizon surface gravity divided")
    print("    by sqrt(8pi/3) = H/sqrt(G rho). At that radius (2.894 R_H) space is not a horizon,")
    print("    so c^2/2R is not a surface gravity. The factor of 2 is borrowed, not earned.")
    print("  * CONCLUSION: it is provably NOT clean-Schwarzschild -- the data exclude the only")
    print("    self-consistent Schwarzschild value (Z=2). The honest status is unchanged and now")
    print("    sharper: sqrt(8pi/3) is Friedmann (real); the leading 2 is a posit that the")
    print("    Schwarzschild route cannot supply without contradicting the measured a0.")
    print("=" * 82)


if __name__ == "__main__":
    main()
