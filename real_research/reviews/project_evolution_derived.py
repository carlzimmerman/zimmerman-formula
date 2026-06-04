#!/usr/bin/env python3
"""
The evolution is NOT free: deriving a0(z) from the dynamical apparent-horizon thermodynamics shrinks the box.
============================================================================================================
The parameter-space map left TWO free parameters: Z_eff (normalization) and alpha (evolution exponent,
a0(z)/a0(0) = E(z)^alpha). But alpha is not actually free -- it is FIXED by the horizon thermodynamics, and the
naive "a0 ~ cH" reading (alpha = 1) quietly used the BARE Hubble rate, ignoring that the apparent horizon is
DYNAMICAL.

THE DERIVATION. If a0 tracks the apparent-horizon surface gravity (the Unruh/emergent-gravity reading), the
proper Cai-Cao-Hu / Hayward dynamical surface gravity is
        kappa ~ H ( 1 + Hdot / 2H^2 ),   and for LCDM   Hdot/H^2 = -(3/2) Om(1+z)^3 / E^2,
so    a0(z)  ~  H(z) ( 1 - (3/4) Om(1+z)^3 / E(z)^2 ).
The (1 - ...) factor is the dynamical correction the bare reading dropped. It does NOT free a parameter -- it
REMOVES one: the evolution becomes a single derived CURVE.

THE PREDICTED CURVE (a0(z)/a0(0)):
   z=0.5  1.0  1.5  2.0  3.25
   0.94  0.96  1.06  1.21  1.77        -- nearly FLAT for z<1.5, then a mild rise.
  Effective low-z slope alpha_eff ~ 0 (flat), and it is bounded ABOVE by the bare alpha=1 (a0 can never rise
  faster than cH in an apparent-horizon reading). At z=3.25 it gives a0 ~ 2.1e-10, CONSISTENT with the Big
  Wheel (a0_eff < ~2.6).

CONSEQUENCES.
  1. The parameter space shrinks from 2D (Z_eff, alpha) to ~1D: only Z_eff is free; the EVOLUTION is derived
     (a single falsifiable curve, between the bare alpha=1 and the dynamical near-flat reading, i.e. alpha<=1).
  2. The framework PREDICTS a0 is nearly constant at z<1.5 and rises only mildly at high z -- consistent with
     the high-z disks (Big Wheel) and with Milgrom's (2017) constant reading, and in TENSION with MUSE-DARK III,
     whose steep rise (effective alpha ~ 1.3-1.6) sits ABOVE even the bare alpha=1.
  3. So MUSE's steep rate is the OUTLIER the framework predicts against. That is falsifiable: the
     model-independent (no-DC14-halo) re-extraction of the MUSE slope is the decisive test -- if the steep rise
     survives, the framework's evolution mechanism is wrong; if it flattens, the framework is confirmed.

HONEST CAVEAT: 'a0 tracks the dynamical horizon temperature' is the thermodynamic reading; the framework's
stated free-fall form a0=(c/2)sqrt(G rho_crit) tracks the BARE H (alpha=1). The two bracket the prediction:
alpha in [~0 (dynamical), 1 (bare)] -- both BELOW MUSE. The robust, reading-independent claim is alpha <= 1,
which already excludes MUSE's steep rate. Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
a0_dyn = lambda z: E(z)*(1 - 0.75*Om*(1+z)**3/E(z)**2)   # dynamical apparent-horizon surface gravity


def main():
    print("#"*92)
    print("# The evolution is DERIVED, not free: dynamical apparent-horizon thermodynamics fixes a0(z)")
    print("#"*92 + "\n")
    n = a0_dyn(0.0)
    print("="*92); print("a0(z)/a0(0): bare cH (alpha=1) vs DERIVED dynamical horizon vs the data"); print("="*92)
    print(f"  {'z':>6}{'bare E(z)':>11}{'DYNAMICAL':>11}{'MUSE 1+1.59z':>14}{'note':>20}")
    for z in (0.5, 1.0, 1.5, 2.0, 3.25):
        muse = f"{1+1.59*z:.2f}" if z <= 2 else "(extrap ~6)"
        note = "Big Wheel a0<~2.6" if z > 3 else ""
        print(f"  {z:>6.2f}{E(z):>11.2f}{a0_dyn(z)/n:>11.2f}{muse:>14}{note:>20}")
    print()
    print("="*92); print("RESULT"); print("="*92)
    print(f"""  The derived (dynamical) curve is nearly FLAT at low z [a0(1)/a0(0) = {a0_dyn(1)/n:.2f}, not the bare 1.79] and
  rises only at high z [a0(3.25) ~ {1.2*a0_dyn(3.25)/n:.1f}e-10, consistent with the Big Wheel's <~2.6]. The evolution is a
  SINGLE derived curve, bounded above by the bare alpha=1 -- it is NOT a free parameter. So:

   * the parameter space shrinks from 2D (Z_eff, alpha) to ~1D: only Z_eff (the 9% geometric band) is free;
   * the framework PREDICTS a0 nearly constant for z<1.5, rising mildly after -- siding with the high-z disks
     and Milgrom's constant reading, and AGAINST MUSE-DARK III's steep rise (effective alpha ~ 1.3-1.6, which is
     above even the bare alpha=1);
   * MUSE's steep rate is therefore the OUTLIER the framework predicts against -- decided by the
     model-independent (no-DC14) re-extraction of the MUSE slope.

  Caveat: bare (free-fall, alpha=1) vs dynamical (thermodynamic, near-flat) bracket the prediction; the robust,
  reading-independent claim is alpha <= 1, which already excludes MUSE. Trying harder removed a parameter and
  sharpened the one live tension into a single decisive measurement.""")
    print("="*92)


if __name__ == "__main__":
    main()
