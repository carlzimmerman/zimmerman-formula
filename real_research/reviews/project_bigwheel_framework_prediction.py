#!/usr/bin/env python3
"""
DONE PROPERLY: what the framework PREDICTS for the Big Wheel, three independent ways -- and why baryon-richness
is not an excuse but the mechanism of exclusion.
==============================================================================================================
"What is the problem with being baryon-rich?" -- answered rigorously, given the framework's own implications.

The framework predicts a0(z) = cH(z)/Z = a0(0) E(z); at z=3.25, a0 = 1.2e-10 * 4.99 = 5.99e-10 (a x5 rise).
We confront that with the Big Wheel (V_rot=280+-31 km/s at R_eff=9.6 kpc; M_star=3.7(+2.6/-2.2)e11 SED or
1.7e11 parametric; M_gas(H2,CO)=1.8(+1.0/-0.8)e11; inc 48-52 deg) three independent, complementary ways.

The MOND inertial interpolation g_obs = nu(g_bar/a0) g_bar (equivalently g_bar = mu(g_obs/a0) g_obs); the
deep-MOND BTFR limit V_flat^4 = G a0 M_bar is interpolation-INDEPENDENT, so the headline does not depend on
the choice of mu. The DSSYK-derived interpolation gives the same deep-MOND limit (verified separately).

TEST 1 -- PREDICTED ROTATION SPEED. Given the measured baryons, predict V_flat under the framework vs local.
TEST 2 -- IMPLIED BARYONIC MASS. Given the observed g_obs, what M_bar does each a0 require? (vs the gas floor.)
TEST 3 -- PHANTOM DARK-MATTER FRACTION & ITS TREND. Higher a0 => deeper MOND => MORE phantom DM. The framework
          predicts the Big Wheel (and high-z disks generally) should be MORE dark-matter-dominated; observed
          high-z disks are LESS (Genzel/RC100 declining curves). The framework predicts the WRONG trend.

THE ANSWER TO THE QUESTION: baryon-richness is NOT a loophole that rescues the framework. A baryon-rich galaxy
has g_bar ~ g_obs, which forces nu ~ 1, which forces a0 << g_obs -- so abundant baryons + a modest measured
rotation speed PIN a0 LOW. High a0 can only hide in baryon-POOR systems (where you cannot tell a strong boost
of few baryons from a weak boost of more baryons). The Big Wheel has too much baryonic mass -- the gas ALONE
exceeds what a0=6e-10 allows -- so its baryon-richness is exactly what EXCLUDES the x5 rise. The limitation
baryon-richness imposes is only on PRECISION (it cannot distinguish local from a mild rise), not on the
exclusion of the strong rise. Needs numpy.
"""
import numpy as np

G = 6.674e-11; Msun = 1.989e30; kpc = 3.086e19
Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
A0L = 1.2e-10
HE = 1.36
Z = 3.25
A0F = A0L*E(Z)                 # framework prediction at z=3.25
Reff = 9.6*kpc

# simple interpolation (mu inertial): g_bar = mu(g_obs/a0) g_obs, mu(x)=x/(1+x); nu(y): g_obs=nu(g_bar/a0)g_bar
mu = lambda x: x/(1+x)
def nu_of_y(y):                # invert g_bar=mu(g_obs/a0)g_obs to g_obs=nu(g_bar/a0)g_bar
    return 0.5 + np.sqrt(0.25 + 1/y)


def Vflat_pred(a0, Mbar_e11):
    """Deep-MOND BTFR asymptotic flat speed (interpolation-independent): V = (G a0 M_bar)^(1/4)."""
    return (G*a0*Mbar_e11*1e11*Msun)**0.25/1e3


def main():
    print("#"*92)
    print("# THE FRAMEWORK vs THE BIG WHEEL -- done properly, three ways. Why baryon-richness EXCLUDES high a0.")
    print("#"*92 + "\n")
    print(f"  framework: a0(z=3.25) = 1.2e-10 x E({Z}) = 1.2e-10 x {E(Z):.2f} = {A0F/1e-10:.2f}e-10   (local = 1.20e-10)\n")
    gobs = (280e3)**2/Reff
    print(f"  Big Wheel observed at R_eff: g_obs = V^2/R = {gobs:.2e} = {gobs/A0L:.1f} a0_local "
          f"(=> {gobs/A0F:.2f} a0_framework: still sub-a0, transition regime)\n")

    print("="*92); print("TEST 1 -- PREDICTED rotation speed vs observed 280 km/s (BTFR deep-MOND limit; MC errors)"); print("="*92)
    rng = np.random.RandomState(3)
    n = 200000
    Mstar = np.clip(rng.normal(3.7, 2.4, n), 0, None)        # SED non-parametric
    Mgas = np.clip(rng.normal(1.8, 0.9, n), 0, None)
    Mbar = Mstar + HE*Mgas
    Mbar_gasfloor = HE*Mgas                                   # robust lower bound (no stars)
    for a0, lab in [(A0F, "FRAMEWORK a0=6.0e-10"), (A0L, "LOCAL a0=1.2e-10")]:
        Vp = Vflat_pred(a0, Mbar)
        lo, md, hi = np.percentile(Vp, [16, 50, 84])
        Vp_gf = Vflat_pred(a0, Mbar_gasfloor); gflo = np.percentile(Vp_gf, 16)
        print(f"  {lab:24}: predicted V_flat = {md:.0f} (+{hi-md:.0f}/-{md-lo:.0f}) km/s   "
              f"[gas-only floor still predicts >= {gflo:.0f}]")
    print(f"  OBSERVED V_flat (max, incl-corrected) = 280 +- 31 km/s")
    Vp = Vflat_pred(A0F, Mbar)
    frac_over = np.mean(Vp > 280+2*31)
    print(f"  => the FRAMEWORK over-predicts the rotation: {np.median(Vflat_pred(A0F,Mbar)):.0f} vs 280 km/s "
          f"({100*np.median((Vflat_pred(A0F,Mbar)-280)/280):.0f}% too fast); LOCAL a0 matches.\n")

    print("="*92); print("TEST 2 -- IMPLIED baryonic mass for the observed g_obs (vs the measured gas floor)"); print("="*92)
    for a0, lab in [(A0L, "LOCAL a0"), (A0F, "FRAMEWORK a0")]:
        gbar = mu(gobs/a0)*gobs
        Mb = gbar*Reff**2/G/Msun/1e11
        print(f"  {lab:14}: requires g_bar={gbar:.2e} -> M_bar(<R_eff) = {Mb:.2f}e11 Msun")
    Mgas_in = 0.5*HE*1.8
    print(f"  MEASURED gas alone within R_eff (H2 x1.36, ~half inside) ~ {Mgas_in:.2f}e11 Msun (stars on top).")
    print(f"  => the framework needs LESS baryonic mass than the GAS ALONE -- impossible. Too many baryons for high a0.\n")

    print("="*92); print("TEST 3 -- PHANTOM dark-matter fraction, and the high-z TREND (the framework's own implication)"); print("="*92)
    for a0, lab in [(A0L, "LOCAL a0"), (A0F, "FRAMEWORK a0")]:
        fDM = 1 - mu(gobs/a0)         # phantom DM fraction = 1 - g_bar/g_obs = 1 - mu(g_obs/a0)
        print(f"  {lab:14}: predicted phantom-DM fraction at R_eff = {fDM*100:.0f}%")
    print("""  Observed: the Big Wheel is baryon-dominated (M_bar ~ M_dyn), f_DM ~ 30-40% -- matches LOCAL a0 (31%),
  NOT the framework (69%). And the BROADER implication: higher a0 => deeper MOND => MORE phantom DM, so the
  framework predicts high-z disks should be MORE dark-matter-dominated. Observed high-z disks (Genzel, RC100)
  are LESS (declining curves, baryon-dominated). The framework predicts the WRONG SIGN of the dark-fraction
  trend with redshift.\n""")

    print("="*92); print("VERDICT -- the answer to 'what is the problem with being baryon-rich?'"); print("="*92)
    print("""  It is NOT an excuse that protects the framework -- it is the mechanism that EXCLUDES it. A baryon-rich
  galaxy has g_bar ~ g_obs, which forces the MOND boost nu ~ 1, which forces a0 << g_obs. Abundant baryons plus
  a modest measured rotation speed PIN a0 LOW; a high a0 would over-boost those baryons and predict a far
  faster rotation (Test 1: ~470 vs 280 km/s) or, equivalently, demand less baryonic mass than the observed gas
  alone (Test 2). High a0 can only hide in baryon-POOR systems; the Big Wheel is the opposite. The ONLY thing
  baryon-richness costs us is PRECISION on a LOW a0 (it cannot separate local from a mild rise), but it makes
  the exclusion of the x5 rise ROBUST -- and Test 3 shows the framework even predicts the wrong direction for
  the dark-fraction-vs-redshift trend.
  STEELMAN (the framework's only escape): a0=6e-10 works ONLY if the Big Wheel's true V_flat is ~470 km/s and
  the reported 280 is a ~68% underestimate -- but beam smearing/measurement systematics are ~10-30%, not 68%,
  and the value is already inclination-corrected, so this escape is implausible. Honest caveats unchanged: one
  galaxy; M_bar SED systematics (bounded by the gas floor, which already does the job); transition not deep-
  MOND (handled by using g_obs directly).""")
    print("="*92)


if __name__ == "__main__":
    main()
