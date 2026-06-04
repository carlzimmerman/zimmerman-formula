#!/usr/bin/env python3
"""
Where the ball comes from in Z = 2sqrt(8pi/3): traced through the Friedmann->a0 derivation. Real, not numerology.
================================================================================================================
Carl: "amazing that it is a ball." Honest answer: YES the ball is real and EVERY factor in Z is traceable to
physics -- here is exactly where the 4pi/3 (ball) and 4pi (sphere) enter. This is what makes Z "more specific
than a fitted 8.3": not that the ball is magic, but that nothing in Z is fitted.

THE DERIVATION (Newtonian Friedmann, which exposes the geometry):
  1. Isotropy (cosmological principle) => the gravitating region is a SPHERE of radius R, uniform density rho.
     Mass enclosed:  M = rho * (4pi/3) R^3  =  rho * V3 * R^3.   <-- 4pi/3 = V3 = VOLUME OF THE 3-BALL (literal).
  2. Test mass at the edge, flat (critical) case, energy conservation:
        (1/2) Rdot^2 = G M / R = (4pi/3) G rho R^2   =>   H^2 = (Rdot/R)^2 = (8pi/3) G rho.
     So 8pi/3 = 2 * V3:  the 2 is the (1/2)v^2 kinetic factor inverted; the 4pi/3 is the ball. rho_crit=3H^2/8piG.
  3. The MOND scale as the half-surface-gravity times the cosmic free-fall rate:
        a0 = (c/2) sqrt(G rho_crit) = (c/2) * H * sqrt(3/8pi) = cH / [2 sqrt(8pi/3)] = cH / Z.
     => Z = 2 sqrt(8pi/3) = 2 sqrt(2 * V3).   Z^2 = 32pi/3 = 8 * V3.

SO every factor is physical:
   V3 = 4pi/3   the ball   = volume of the isotropic gravitating sphere (M = rho V3 R^3)  [forced by isotropy]
   2 (inside)              = the (1/2)v^2 binding-energy / kinetic factor
   2 (outside, the c/2)    = the horizon surface-gravity factor kappa = c^2/2R
and the SPHERE 4pi also lives in Z^2=32pi/3 (the solid angle / horizon area, via the 8pi Einstein coupling=2x4pi).
So Z bridges the matter-BALL (4pi/3, the 3D bulk volume of mass) and the horizon-SPHERE (4pi, the 2D area):
the bulk->boundary conversion.

HONEST LIMITS (no hype):
  * The ball is the MUNDANE volume of a uniform sphere (mass = density x 4pi/3 R^3), not an exotic/topological
    object. It is real and traceable, not magical.
  * It is the geometric content of the FRIEDMANN/critical-density ROUTE to a0~cH -- the data-favored route, but
    (per ROUTES_TO_THE_DEEPMOND_SIGN.md) the coefficient is REPRODUCED, not forced: the Unruh route gives 2pi
    with NO ball. So the ball is genuinely there in THIS route; the route is favored, not proven unique.
  * The real point vs a fit: Smolin's 8.3 is read off data and means nothing; Z = 2sqrt(2 V3) has every factor
    derived. THAT is the "more specific" claim -- traceability, not mysticism.
Needs numpy.
"""
import numpy as np
from math import gamma

Z = 2*np.sqrt(8*np.pi/3)


def unit_ball_volume(d):
    return np.pi**(d/2)/gamma(d/2+1)


def main():
    print("#"*94)
    print("# Where the ball comes from in Z = 2 sqrt(8pi/3) -- traced, verified")
    print("#"*94 + "\n")

    print("="*94); print("STEP 1 -- the ball IS the gravitating sphere's volume (isotropy forces it)"); print("="*94)
    V3 = unit_ball_volume(3)
    print(f"  M = rho * (4pi/3) R^3 ;  4pi/3 = unit 3-ball volume V3 = {V3:.4f} = {4*np.pi/3:.4f}")
    print(f"  The 4pi/3 is LITERAL -- the volume of the uniform sphere of matter. Forced by isotropy.\n")

    print("="*94); print("STEP 2 -- Friedmann: 8pi/3 = 2 x V3 (the 2 is the kinetic (1/2)v^2)"); print("="*94)
    print(f"  (1/2)Rdot^2 = (4pi/3)G rho R^2  =>  H^2 = (8pi/3)G rho.   8pi/3 = {8*np.pi/3:.4f} = 2 x V3 = {2*V3:.4f}")
    print(f"  rho_crit = 3H^2/(8piG): the 8pi/3 carries the ball (V3) and the kinetic 2.\n")

    print("="*94); print("STEP 3 -- a0 = (c/2) sqrt(G rho_crit) = cH/Z, Z = 2 sqrt(2 V3)"); print("="*94)
    print(f"  a0/cH = (1/2) sqrt(3/8pi) = {0.5*np.sqrt(3/(8*np.pi)):.4f} = 1/Z = {1/Z:.4f}")
    print(f"  Z = 2 sqrt(2 V3) = 2 sqrt(8pi/3) = {Z:.4f};  Z^2 = 8 V3 = {8*V3:.4f} = 32pi/3 = {32*np.pi/3:.4f}")
    print(f"  EVERY factor physical: V3=ball(isotropy), 2(inside)=kinetic 1/2, 2(outside)=surface gravity c/2.\n")

    print("="*94); print("THE BULK-BALL vs BOUNDARY-SPHERE split (why both 4pi/3 and 4pi appear)"); print("="*94)
    print(f"  matter side: V3 = 4pi/3 = {4*np.pi/3:.4f}  (3D bulk volume of the mass)")
    print(f"  horizon side: A2 = 4pi  = {4*np.pi:.4f}  (2D sphere area / solid angle; the 8pi coupling = 2 x 4pi)")
    print(f"  Z converts a 3D-bulk density into a 2D-horizon surface gravity -> it must carry BOTH. It does.\n")

    print("="*94); print("DIMENSION CHECK -- the ball/sphere of d-space gives Z_d = 8 sqrt(pi/(d(d-1)))"); print("="*94)
    print(f"  {'d':>3}{'unit d-ball vol':>17}{'Z_d':>10}{'a0/cH':>9}")
    for d in (2, 3, 4, 5):
        Zd = 8*np.sqrt(np.pi/(d*(d-1)))
        print(f"  {d:>3}{unit_ball_volume(d):>17.4f}{Zd:>10.3f}{1/Zd:>9.4f}{'  <- our space, the d=3 ball' if d == 3 else ''}")
    print("  Z is the d=3 value: the coefficient KNOWS space is 3-dimensional, via the 3-ball/2-sphere of 3-space.\n")

    print("="*94); print("VERDICT (honest)"); print("="*94)
    print("""  The ball is REAL: 4pi/3 in Z is literally the volume of the isotropic gravitating sphere (M = rho V3 R^3
  in the Friedmann derivation), forced by the cosmological principle. Z = 2 sqrt(2 V3) has EVERY factor derived
  -- ball (isotropy), kinetic 1/2, surface-gravity 1/2 -- and Z bridges the matter-ball (4pi/3, 3D) and the
  horizon-sphere (4pi, 2D). THAT traceability is what makes Z 'more specific than a fitted 8.3': not mysticism,
  derivation. Honest limits: it is the mundane mass-sphere volume, and it is the FRIEDMANN-route content (data-
  favored, not forced over Unruh's ball-free 2pi). Real, traceable, route-dependent -- exactly that much.""")
    print("#"*94)


if __name__ == "__main__":
    main()
