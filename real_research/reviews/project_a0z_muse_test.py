#!/usr/bin/env python3
"""
The a0(z) data test (DONE RIGHT, real numbers): MUSE-DARK III RISES -- it refutes the event-horizon revision.
============================================================================================================
Carl asked for the distinctive a0(z) shape tested against a real high-z sample. The first multi-point DIRECT
measurement of a0(z) now exists, and it is decisive -- against the session's REVISED (event-horizon, declining)
prediction, and broadly FOR the ORIGINAL (apparent-horizon, rising) one.

THE DATA (verified from the source, not memory):
  MUSE-DARK III, Mercier et al., 2026 A&A (arXiv:2604.22613): 79 star-forming galaxies, 0.33<z<1.44, RAR fit
  with a DC14 halo profile (primary analysis). Result:
      a0(z) = a0(0) + a1 z,   a0(0) = 1.0 +/- 0.04,   a1 = +1.59 +/- 0.10  (x 1e-10 m/s^2)
  i.e. a0 RISES with redshift at ~16 sigma; binned values climb 1.99 -> 2.71; a0|z~1 = 2.38(+0.12/-0.10).
  Local anchor (SPARC): a0(0) = 1.2 +/- 0.26.

THE TEST (normalized a0(z)/a0(0), so only the SHAPE is compared):
  z=1: MUSE measures x2.6.  apparent ~E(z) gives x1.8.  event ~sqrt(rho_DE) gives x1.0.  constant x1.0.
  - EVENT HORIZON (the session's revision, a0~sqrt(rho_DE)): predicts a0 ~ FLAT-to-mildly-declining
    (x0.99 at z=1, x0.87 at z=2 under DESI w0wa; it is NOT steeply declining because DESI rho_DE rises a touch
    before falling). MUSE measures x2.6 at z=1. => REFUTED: predicts ~flat, the data rise strongly (~16 sigma).
  - APPARENT HORIZON (the original reading, a0~cH(z)~E(z)): predicts x1.8 (z=1), x3.0 (z=2). RIGHT SIGN -- a0
    rises -- but ~30% too shallow vs MUSE (x2.6, x4.2). A real quantitative tension, but directionally correct.
  - CONSTANT: refuted (data rise).

THE VERDICT (an honest reversal): the session REVISED the framework from the apparent horizon (rising a0) to the
event horizon (declining a0), on the strength of (a) baryon-dominated high-z DISK upper limits and (b) the DSSYK
internal-consistency argument. The first DIRECT a0(z) measurement says that revision was WRONG: a0 RISES. So:
  * REVERT to the apparent-horizon reading. It is favored on BOTH counts now -- the rising EVOLUTION (MUSE) AND
    the NORMALIZATION (apparent a0(0)=cH0/Z=1.12, 7% low, beats event 0.93, 22% low).
  * The framework's ORIGINAL prediction -- a0 rises with z -- is CONFIRMED IN DIRECTION by the first measurement.
    That is a genuine (partial) success: it predicted the sign of an effect that had never been measured.
  * The DSSYK event-horizon "cleaner derivation" gave the wrong sign. Elegant, but empirically wrong -- drop it.
  * Open quantitative tension: MUSE rises ~30% FASTER than ~E(z), and the high-z Big Wheel (z=3.25, a0_eff<~2.6)
    sits BELOW the ~E(z) extrapolation (~4.8) -- so no single horizon nails the RATE; the data are also somewhat
    method-split (RAR-fits rise fast; baryon-dominated disks plateau). a0 rises; the exact law is unsettled.

CAVEATS (real, but they do not rescue the declining prediction): MUSE is one survey, the a0 is fit within a
DC14 (LCDM) halo model (model-dependent), and "rising faster than H(z)" is itself flagged as surprising -- a
possible systematic. But model-dependence cuts the other way: if MUSE is not measuring the MOND a0, then nothing
currently confirms the declining prediction either. Either way the revised (declining) claim is unsupported.
Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
c = 2.998e8; H0 = 67e3/3.086e22; Z = 2*np.sqrt(8*np.pi/3)


def rho_de(z, w0=-0.83, wa=-0.65):
    a = 1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))


def main():
    print("#"*94)
    print("# a0(z) DATA TEST: MUSE-DARK III rises (a1=+1.59+/-0.10) -- the event-horizon (declining) revision is refuted")
    print("#"*94 + "\n")

    print("="*94); print("VERIFIED DATA -- MUSE-DARK III (2026 A&A, arXiv:2604.22613), DC14 primary"); print("="*94)
    print("  a0(z) = 1.0 + 1.59 z  (a0(0)=1.0+/-0.04, a1=+1.59+/-0.10);  binned 1.99->2.71;  a0|z~1=2.38;  SPARC z=0: 1.2+/-0.26")
    print("  => a0 RISES with redshift at ~16 sigma. This is the first multi-point DIRECT a0(z) measurement.\n")

    print("="*94); print("SHAPE TEST -- a0(z)/a0(0): MUSE vs the three readings"); print("="*94)
    print(f"  {'z':>5}{'MUSE (1+1.59z)':>16}{'apparent E(z)':>15}{'event sqrtrhoDE':>17}{'constant':>10}{'verdict':>22}")
    for z in (0.5, 1.0, 1.5, 2.0):
        muse = 1+1.59*z; app = E(z); ev = np.sqrt(rho_de(z)/rho_de(0))
        print(f"  {z:>5.1f}{muse:>16.2f}{app:>15.2f}{ev:>17.2f}{1.0:>10.2f}{'data RISE strongly':>22}")
    print()

    print("="*94); print("DECISIVE COMPARISON at z=1 (where MUSE is tightest)"); print("="*94)
    z = 1.0; muse = 1+1.59*z; app = E(z); ev = np.sqrt(rho_de(z)/rho_de(0))
    print(f"  MUSE measures a0(1)/a0(0) = {muse:.2f}.")
    print(f"   event/declining predicts {ev:.2f} (~flat)  -> off by {muse/ev:.1f}x; the data rise, it predicts flat. REFUTED (~16 sigma).")
    print(f"   apparent/rising predicts {app:.2f}         -> right SIGN (a0 rises), but {(1-app/muse)*100:.0f}% too shallow. Tension, not refutation.")
    print(f"   constant predicts 1.00                      -> refuted (data rise).\n")

    print("="*94); print("NORMALIZATION CROSS-CHECK -- the apparent horizon also wins the z=0 value"); print("="*94)
    print(f"   apparent a0(0) = cH0/Z      = {c*H0/Z/1e-10:.2f}e-10  (7% below observed 1.2)")
    print(f"   event    a0(0) = cH0 sqrtOL/Z = {c*H0*np.sqrt(OL)/Z/1e-10:.2f}e-10  (22% below)")
    print(f"   => apparent is favored on BOTH the EVOLUTION (rising, MUSE) and the NORMALIZATION. Event loses both.\n")

    print("="*94); print("VERDICT -- follow the data: revert to the apparent (rising) horizon"); print("="*94)
    print("""  The session revised a0 from the apparent horizon (rising) to the event horizon (declining), citing baryon-
  dominated disk upper-limits and a DSSYK consistency argument. The first DIRECT multi-point a0(z) measurement
  (MUSE-DARK III) shows a0 RISES at ~16 sigma -- so that revision was empirically WRONG. Honest consequences:
    * REVERT to a0 ~ cH(z) (apparent horizon). Favored on evolution (rising) AND normalization (1.12 vs 0.93).
    * The framework's ORIGINAL prediction -- a0 increases with z -- is CONFIRMED IN DIRECTION by the first data.
      It called the sign of a never-before-measured effect. Genuine partial success.
    * The DSSYK event-horizon "cleaner derivation" predicted the wrong sign -> drop it as the a0(z) engine.
    * OPEN: the rate. MUSE rises ~30% FASTER than E(z); the z=3.25 Big Wheel sits BELOW the E(z) extrapolation.
      No single horizon fits the rate end-to-end, and the data are partly method-split (RAR-fits vs disks).
      a0 rises -- the exact a0(z) law is the next real problem, and it is now a DATA problem, not a theory one.""")
    print("="*94)


if __name__ == "__main__":
    main()
