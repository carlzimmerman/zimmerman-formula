#!/usr/bin/env python3
"""
PROJECT 6b: the gas-INDEPENDENT CMB test of rising a0 -- the breakthrough (and it cuts against the framework).
=============================================================================================================
Every galaxy-scale a0(z) test is gas-limited (projects 10b-d). The CMB is NOT: it uses Omega_b and Omega_dm
from BBN/CMB, no galaxy gas census. And it turns out to be the SHARPEST test of rising a0, decidable with
existing Planck data. The result is a genuine, gas-independent finding -- and an honest one: it strongly
DISFAVORS the framework's rising-a0 bet, unless a specific cancellation holds. Reported straight, because a
decisive test that leans the 'wrong' way is exactly what the integrity contract is for. Needs numpy.

*** RETRACTED -- see project06c_cmb_correction.py. This argument is WRONG: it applies the GALAXY MOND boost
nu=sqrt(a0/g) to small CMB perturbations, but in AeST the MOND invariant Y is the spatial gradient of phi
with Ybar=0, so J(Y)=Y^{3/2} is THIRD order in CMB perturbations -- negligible regardless of a0. The CMB does
NOT cleanly constrain rising a0. Kept for the record (and the regime-flip in Part 1 is real); the conclusion
is withdrawn. ***
"""
import numpy as np

c, Mpc = 2.99792458e8, 3.0857e22
H0 = 67.4e3/Mpc
Om, OL, Ob = 0.315, 0.685, 0.0493
Odm = Om - Ob
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
a0 = 1.2e-10
zr = 1100


def main():
    print("#"*92); print("# PROJECT 6b -- the gas-independent CMB test of rising a0"); print("#"*92 + "\n")
    Phi = 3e-5; lam = 147*Mpc/(1+zr)
    g = 2*np.pi/lam*Phi*c**2

    print("="*92); print("PART 1 -- rising a0 puts recombination in DEEP MOND (constant a0 does not)"); print("="*92)
    print(f"  Acoustic-scale gravitational acceleration at recombination: g ~ k Phi c^2 = {g:.2e} m/s^2.")
    for name, a0z in [("RISING  a0(z_rec)=a0 E(1100)", a0*E(zr)), ("CONSTANT a0", a0)]:
        r = g/a0z; nu = np.sqrt(a0z/g) if r < 1 else 1.0
        print(f"  {name:30}={a0z:.2e}: g/a0={r:.1e} [{'DEEP MOND' if r<1 else 'Newtonian':9}]  boost nu={nu:.0f}x")
    nu = np.sqrt(a0*E(zr)/g)
    print(f"""  This is the crux: the framework's a0 rises by E(1100)~{E(zr):.0e}, so the SAME acoustic perturbations that
  are firmly NEWTONIAN under constant a0 (g/a0~34) are DEEP IN MOND under rising a0 (g/a0~1.7e-3). The two
  readings put recombination in opposite regimes -- and the CMB is measured to ~0.1%.\n""")

    print("="*92); print("PART 2 -- the size of the effect (gas-independent)"); print("="*92)
    print(f"""  In deep MOND the baryon self-gravity is boosted by nu=sqrt(a0/g)~{nu:.0f}: the effective gravitating
  baryon density is Omega_b*nu = {Ob*nu:.2f}, versus the real dark sector Omega_dm = {Odm:.2f} -- about
  {Ob*nu/Odm:.0f}x too much gravitational driving of the acoustic oscillations. Worse, MOND-boosted BARYONS load
  and oscillate (they are not pressureless), so they cannot even mimic the CDM-like driving the CMB needs --
  the peak structure would be qualitatively wrong, not just rescaled. All of this uses only Omega_b, Omega_dm
  (BBN + CMB), NO galaxy gas census -- it is immune to the wall that limits projects 10b-d.\n""")

    print("="*92); print("PART 3 -- the cancellation rising a0 needs (and constant a0 never does)"); print("="*92)
    print(f"""  AeST passes Planck with CONSTANT a0 because recombination is Newtonian there (nu=1) -- the MOND sector is
  dormant, and the K(Q) mode supplies the CDM-like driving. For RISING a0 the MOND sector is ACTIVE at
  recombination, so the framework needs the AeST cancellation (delta q^00=0) to remove the nu~{nu:.0f}x boost to
  ~{100*(1-1/nu):.0f}%+ precision -- a requirement constant a0 never faces. That cancellation was CONSTRUCTED for constant
  a0; whether it survives a TIME-DEPENDENT a0 is unproven and non-trivial (the time-dependence a0_dot/a0 ~ H is
  exactly the scale of the acoustic dynamics).\n""")

    print("="*92); print("PART 4 -- the honest verdict, and the steelman"); print("="*92)
    print("""  STEELMAN (the escape the framework needs): if delta q^00=0 is a STRUCTURAL identity of AeST -- true
  regardless of the MOND regime and regardless of a0(t) -- then the linear boost is cancelled exactly, rising
  a0 is CMB-safe at linear order, and the only residual is the second-order non-Gaussianity of project 6
  (small). The framework's viability HINGES on this being structural, not regime-dependent.
  VERDICT: the CMB is a gas-independent, existing-data test that strongly DISFAVORS rising a0 -- it forces the
  acoustic perturbations into deep MOND at recombination, an ~5x over-driving that constant a0 never produces,
  requiring a >95% cancellation the theory was not built to guarantee for time-dependent a0. It is NOT a proof
  of exclusion (the structural-cancellation escape is real and must be checked), but it is the sharpest
  gas-independent reason to doubt the rise, and it is decidable now via a second-order AeST/Boltzmann analysis
  of Planck -- no telescope time, no gas census. This is the breakthrough: a decisive test that escapes the
  gas wall. That it leans against the framework is reported straight; the one calculation that could rescue
  rising a0 (prove delta q^00=0 is structural under a0(t)) is now precisely identified.""")
    print("="*92)


if __name__ == "__main__":
    main()
