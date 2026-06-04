#!/usr/bin/env python3
"""
The parameter space of the framework's MOND sector: a 2-parameter, theory-bounded box.
======================================================================================
After the deep-geometry / candidate analysis, the surviving family is a single form -- the apparent-horizon
surface gravity reduced by a 3D-density factor -- with exactly TWO parameters:

    a0(z) = (c H0 / Z_eff) * E(z)^alpha ,   E(z) = sqrt(Om(1+z)^3 + OL).

  PARAMETER 1: Z_eff -- the z=0 coefficient = 2 x (3D-density factor).
     geometric requirement (principled factors sqrt(8pi/3)=2.894, pi=3.142, volume 3): Z_eff in [5.79, 6.28]
       -- a ~9% band. The framework point is the exact Friedmann conversion, Z_eff = 2 sqrt(8pi/3) = 5.789.
     data normalization (a0 = 1.2 +- 0.26, H0 = 67-73): Z_eff = cH0/a0 in ~[4.5, 7.5].
     => what survives both: Z_eff ~ 5.79-6.28.

  PARAMETER 2: alpha -- the evolution exponent, a0(z)/a0(0) = E(z)^alpha.
     alpha = 1 : apparent horizon, a0 ~ cH(z) -- the FRAMEWORK prediction (rising).
     alpha = 0 : event horizon / constant a0 (Lambda-tracking) -- EXCLUDED by MUSE.
     alpha < 0 : declining -- EXCLUDED by MUSE.
     MUSE-DARK III (a0 = 1 + 1.59z) measures effective alpha ~ 1.3-1.6 (rising, steeper than apparent).

THE ALLOWED BOX (requirements + data): Z_eff in [5.79, 6.28] (9% wide, geometric) x alpha in [~1, ~1.6] (rising).
  framework natural point (Z_eff, alpha) = (5.79, 1.0);  MUSE-favoured ~(5.4, 1.3-1.6) -> the RATE TENSION (the
  one live tension: the data want a0 to rise a bit faster than the apparent-horizon alpha=1).

VS STANDARD MOND: standard MOND has a0 = a FREE universal constant (fit ~1.2e-10) plus the interpolation shape =
a FREE function (2 free). The framework instead DERIVES a0's scale (= cH(z)/Z_eff, Z_eff bounded to a 9% band),
PREDICTS the evolution (alpha=1), and DERIVES the interpolation shape (the DSSYK chord measure, ~q-independent).
So it has ZERO truly-free parameters -- two bounded-but-not-fully-pinned ones (Z_eff, alpha) -- a strictly
SMALLER, more predictive parameter space than standard MOND. The decisive shrink: a ~6% a0 measurement pins
Z_eff, and a clean a0 at z~2-3 pins alpha. Needs numpy.
"""
import numpy as np

c = 2.998e8; Mpc = 3.086e22; Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def main():
    print("#"*92)
    print("# Parameter space: a0(z) = (c H0 / Z_eff) * E(z)^alpha  -- 2 parameters, both theory-bounded")
    print("#"*92 + "\n")
    fr = 2*np.sqrt(8*np.pi/3)

    print("="*92); print("PARAMETER 1 -- Z_eff (z=0 coefficient = 2 x 3D-density factor)"); print("="*92)
    print(f"  geometric family (3D factors sqrt(8pi/3),pi,3):  Z_eff in [{fr:.2f}, {2*np.pi:.2f}]   (~9% band)")
    print(f"  data normalization (a0=1.2+-0.26, H0=67-73):     Z_eff = cH0/a0 in [{c*67e3/Mpc/1.46e-10:.1f}, {c*73e3/Mpc/0.94e-10:.1f}]")
    print(f"  framework point: Z_eff = 2 sqrt(8pi/3) = {fr:.3f}  (a0=1.12 at H0=67; =1.2 at H0=71.5)\n")

    print("="*92); print("PARAMETER 2 -- alpha (evolution exponent), a0(z)/a0(0) = E(z)^alpha"); print("="*92)
    print(f"  alpha = 1 : apparent horizon (a0~cH(z))  -- FRAMEWORK prediction (rising)")
    print(f"  alpha = 0 : event horizon / constant a0  -- EXCLUDED by MUSE")
    print(f"  alpha < 0 : declining                    -- EXCLUDED by MUSE")
    for z in (1.0, 2.0):
        print(f"  MUSE (a0=1+1.59z): effective alpha = {np.log(1+1.59*z)/np.log(E(z)):.2f} at z={z:.0f}  (rising, steeper than apparent)\n" if z == 2 else
              f"  MUSE (a0=1+1.59z): effective alpha = {np.log(1+1.59*z)/np.log(E(z)):.2f} at z={z:.0f}  (rising, steeper than apparent)")

    print("="*92); print("THE ALLOWED BOX, and vs standard MOND"); print("="*92)
    print(f"""  BOX (requirements + data):  Z_eff in [5.79, 6.28] (9% wide)  x  alpha in [~1, ~1.6] (rising).
    framework natural point (5.79, 1.0);  MUSE-favoured ~(5.4, 1.3-1.6) -> the one live tension is the RATE (alpha).

  STANDARD MOND parameter space:  a0 = FREE constant (~1.2e-10)  +  interpolation shape = FREE function.  (2 free)
  THIS FRAMEWORK:                 a0 = cH(z)/Z_eff (Z_eff bounded to 9%)  +  alpha PREDICTED=1  +  shape DERIVED.
    => 0 truly-free parameters; 2 bounded-not-pinned. Strictly SMALLER and more predictive than standard MOND --
       it removes the free a0 constant and the free shape. Decisive shrink: 6% a0 pins Z_eff; a0 at z~2-3 pins alpha.""")
    print("="*92)


if __name__ == "__main__":
    main()
