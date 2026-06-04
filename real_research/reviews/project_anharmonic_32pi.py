#!/usr/bin/env python3
"""
What is an anharmonic coefficient, why MOND is one, and why ours is 32pi. Verified, pedagogical.
================================================================================================
HARMONIC vs ANHARMONIC. A potential/Lagrangian expanded in a field f:  V(f) = (1/2)k f^2 + g3 f^3 + g4 f^4 + ...
  * the f^2 (quadratic) term = HARMONIC -> linear restoring force F=-kf -> a simple spring/oscillator.
  * the f^3, f^4, ... terms = ANHARMONIC -> NONLINEAR. Their coefficients (g3, g4) are the anharmonic coefficients.
    Anharmonicity is what gives thermal expansion, frequency-shift-with-amplitude, mode coupling -- the nonlinear
    physics a pure spring cannot produce.

MOND IS ANHARMONIC. The gravitational Lagrangian in the potential phi:
  Newton:     L_N = -(1/8piG) (grad phi)^2                 HARMONIC (quadratic) -> linear Poisson  grad^2 phi = 4piG rho
  deep-MOND:  L_M = -(1/8piG)(2/3)|grad phi|^3 / a0          ANHARMONIC (CUBIC) -> the nonlinear MOND eqn / sqrt-law
So MOND replaces the harmonic (grad phi)^2 with an ANHARMONIC (grad phi)^3, and a0 sits in the anharmonic
coefficient 1/(8piG a0). The deep-MOND sqrt-law g=sqrt(g_N a0) is the SIGNATURE of that cubic term.

BLANCHET's dipolar-dark-matter potential is the same story written for a polarization field Pi:
  W(Pi) = Lambda/8pi  +  2pi Pi^2  +  (16pi^2/3a0) Pi^3 + ...
          ^floor=Lambda  ^HARMONIC=DM   ^ANHARMONIC=MOND, a0 in the cubic coefficient
The harmonic term acts like ordinary dark matter; the ANHARMONIC term IS MOND; a0 is its coefficient; and Lambda
is the floor. Blanchet EXPECTS Lambda ~ a0^2 (floor ~ anharmonic-scale squared).

WHY OURS IS 32pi. The 32pi is NOT the anharmonic coefficient itself -- it is the dimensionless RATIO that welds the
HARMONIC FLOOR (Lambda) to the ANHARMONIC SCALE (a0): from a0 = c^2 sqrt(Lambda/32pi),
   32pi = Lambda c^4 / a0^2     (the curvature-to-acceleration-squared ratio; dimensionless)
i.e. "the MOND nonlinearity turns on at the acceleration whose square, times 32pi, equals the cosmological-constant
curvature." And 32pi = 4 x 8pi = (surface-gravity factor 2)^2 x (Einstein coupling 8pi); geometrically 32pi = 8 x
4pi (sphere area), and Z^2 = 32pi/3 = 8 x 4pi/3 (ball volume). Blanchet's floor uses 8pi, ours 32pi -- same
structure, an O(1) (factor ~4) apart, the route-choice the forcing analysis already flagged. Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; Mpc = 3.086e22
H0 = 67.4e3/Mpc; OmL = 0.685
Lam = 3*OmL*H0**2/c**2          # cosmological constant, 1/m^2


def main():
    print("#"*92); print("# Anharmonic coefficients, MOND, and why ours is 32pi"); print("#"*92 + "\n")

    print("="*92); print("(1) HARMONIC vs ANHARMONIC -- the gravitational Lagrangian"); print("="*92)
    print("   Newton    L = -(1/8piG)(grad phi)^2          QUADRATIC = harmonic -> linear (a 'spring')")
    print("   deep-MOND L = -(1/8piG)(2/3)|grad phi|^3/a0   CUBIC = ANHARMONIC -> nonlinear, the sqrt-law")
    print("   => a0 lives in the ANHARMONIC coefficient 1/(8piG a0). MOND = the cubic term; a0 sets its strength.\n")

    print("="*92); print("(2) THE 32pi: the dimensionless ratio welding the floor (Lambda) to the anharmonic scale (a0)"); print("="*92)
    a0 = c**2*np.sqrt(Lam/(32*np.pi))            # self-consistent framework a0 (de Sitter value)
    ratio = Lam*c**4/a0**2
    print(f"   a0 = c^2 sqrt(Lambda/32pi) = {a0:.3e} m/s^2  (the framework's self-consistent a0)")
    print(f"   => Lambda c^4 / a0^2 = {ratio:.3f}  =  32pi = {32*np.pi:.3f}   (exact, by construction)")
    print(f"   meaning: MOND's nonlinearity turns on where a0^2 * 32pi = Lambda c^4 (the cosmological curvature).")
    print(f"   (with the OBSERVED a0=1.2e-10, Lambda c^4/a0^2 = {Lam*c**4/(1.2e-10)**2:.0f} -- ~off by the usual ~20-30%.)\n")

    print("="*92); print("(3) WHERE 32pi COMES FROM (pure gravity)"); print("="*92)
    print(f"   32pi = {32*np.pi:.3f} = 4 x 8pi = (surface-gravity factor 2)^2 x (Einstein coupling 8pi)")
    print(f"        = 2^3 x 4pi = (coupling factors) x (unit-sphere AREA 4pi = {4*np.pi:.3f})")
    print(f"   Z^2 = 32pi/3 = 8 x (4pi/3) = (coupling) x (unit-BALL VOLUME 4pi/3 = {4*np.pi/3:.3f})")
    print(f"   => 32pi is gravitational gearing (Einstein coupling x horizon factor), NOT particle physics.\n")

    print("="*92); print("(4) BLANCHET's potential -- the same anharmonic structure, an O(1) apart"); print("="*92)
    print("   W(Pi) = Lambda/8pi + 2pi Pi^2 + (16pi^2/3a0) Pi^3 + ...")
    print("            floor=Lambda  harmonic=DM   ANHARMONIC=MOND (a0 in the cubic coeff)")
    print(f"   Blanchet's floor uses 8pi; ours uses 32pi (a factor {32*np.pi/(8*np.pi):.0f} apart) -- same structure,")
    print("   the O(1)/route difference the forcing analysis flagged. BOTH put a0 in the anharmonic (cubic) term.\n")

    print("="*92); print("VERDICT"); print("="*92)
    print("""  An anharmonic coefficient is the coefficient of a beyond-quadratic (f^3, f^4, ...) term in a potential --
  the NONLINEARITY. MOND IS anharmonic: it replaces Newton's harmonic (grad phi)^2 with a cubic (grad phi)^3, with
  a0 in that cubic coefficient (the sqrt-law is the cubic term's signature). Blanchet's dipolar-DM potential makes
  this explicit (floor=Lambda, harmonic=DM, cubic=MOND). 'Ours is 32pi' because 32pi = Lambda c^4/a0^2 is the
  dimensionless ratio welding the cosmological-constant floor to the MOND anharmonic scale -- and 32pi is pure
  gravitational gearing (Einstein coupling 8pi x horizon factor 4 = 8 x sphere-area 4pi). Real, traceable; the
  O(1) (vs Blanchet's 8pi) is the route-choice, not uniquely forced.""")
    print("#"*92)


if __name__ == "__main__":
    main()
