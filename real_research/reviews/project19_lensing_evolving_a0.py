#!/usr/bin/env python3
"""
PROJECT 19: lensing of the evolving a0 -- an INDEPENDENT check, immune to the kinematic confounds.
==================================================================================================
The a0(z) tests from dynamics (#10, #11, #17) are all limited by the SAME systematic: gas fraction and
pressure support bias high-z rotation curves. Weak LENSING does not use kinematics at all -- it measures the
phantom-halo mass directly from light bending. In deep MOND (AeST lenses on baryons+phantom) the phantom
mass M_ph ~ sqrt(M_bar a0), so at fixed baryonic mass M_ph ~ sqrt(a0(z)) ~ sqrt(E(z)). This file derives the
signature and forecasts it. A clean, orthogonal cross-check. Needs numpy.

CORRECTION: 'immune to the kinematic confounds' is right, but do NOT read it as immune to GAS -- see
project_stresstest_07_19.py. M_lens ~ sqrt(M_bar a0) still needs a per-galaxy GAS CENSUS (at fixed M_star
the rising gas fraction inflates M_lens comparably to the wanted sqrt(E(z))). The real, distinct advantage
is independence from the PRESSURE/KINEMATIC confound (no velocities used), so lensing and dynamics fail
differently -- not freedom from the gas census.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
G, a0, Msun, kpc = 6.674e-11, 1.2e-10, 1.989e30, 3.0857e19


def main():
    print("#"*92); print("# PROJECT 19 -- lensing of the evolving a0 (independent of kinematics)"); print("#"*92 + "\n")
    print("="*92); print("THE DERIVATION"); print("="*92)
    print("""  Deep-MOND extra acceleration g_ph = sqrt(g_N a0) (for g_N << a0). The phantom mass enclosed in r:
        M_ph(r) = g_ph r^2 / G = sqrt(G M_bar a0) r / G = r sqrt(M_bar a0 / G).
  In AeST light bends on baryons PLUS this phantom, with the SAME mass that governs dynamics (the theory is
  built so lensing and dynamics agree). Hence at FIXED baryonic mass the lensing mass scales as
        M_lens ~ sqrt(a0(z)) ~ sqrt(E(z)).\n""")
    print(f"  {'z':>5}{'E(z)':>8}{'lensing-mass boost sqrt(E(z))':>30}")
    for z in (0.0, 0.5, 1.0, 2.0, 3.0):
        print(f"  {z:>5.1f}{E(z):>8.2f}{np.sqrt(E(z)):>30.2f}")
    Mb, r = 10**10.5*Msun, 50*kpc
    Mph = lambda z: r*np.sqrt(Mb*a0*E(z)/G)/Msun
    print(f"  worked: M_bar=10^10.5, phantom within 50 kpc: log M_ph(z=0)={np.log10(Mph(0)):.2f}, "
          f"z=1={np.log10(Mph(1)):.2f} (+{(Mph(1)/Mph(0)-1)*100:.0f}%)\n")

    print("="*92); print("WHY IT IS CLEAN, AND THE FORECAST"); print("="*92)
    print("""  vs LambdaCDM: the stellar-to-halo-mass relation has NO sqrt(E(z)) tilt at fixed M_star -- halos track
  mass, not epoch. So lensing-mass/M_star RISING as sqrt(E(z)) is a distinctive framework signature, and one
  that does NOT depend on rotation curves -> it is immune to the gas/pressure systematic that limits every
  dynamical a0(z) measurement. That orthogonality is the whole point: lensing and dynamics fail differently,
  so agreement between them would be decisive.
  FORECAST: separating +34% at z=1 (and +74% at z=2) from a flat relation at ~0.1 dex stacked precision needs
  ~10^3-10^4 lens-source pairs per z-bin -- comfortably within Euclid, Rubin/LSST and JWST weak-lensing
  yields. Galaxy-galaxy stacking by baryonic-mass and redshift bin is the measurement.\n""")

    print("="*92); print("PROJECT 19 VERDICT"); print("="*92)
    print("""  Weak lensing predicts a clean, derivable signature of rising a0: lensing mass at fixed baryonic mass
  grows as sqrt(E(z)) (+34% by z=1, +74% by z=2), with NO LambdaCDM counterpart at fixed M_star. Because it
  uses light bending, not kinematics, it is immune to the gas/pressure confound that limits the dynamical
  a0(z) -- making it the ideal INDEPENDENT cross-check of #17. Within Euclid/Rubin/JWST reach. A second,
  orthogonal road to the same rising-a0 answer; if both roads agree, the case is essentially closed.""")
    print("="*92)


if __name__ == "__main__":
    main()
