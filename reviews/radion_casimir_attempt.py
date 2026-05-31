#!/usr/bin/env python3
"""
A genuine attempt at the 'last piece': can the radion Casimir energy of the
ACTUAL field content on M4 x T^3/Z2 stabilize at R = Z^2 l_P/(2pi)?
====================================================================================

This is the one route left standing. We compute honestly, no answer inserted.

Setup: massless bulk field, KK masses |n|/R on the Z2-projected cubic lattice.
The 4D Casimir energy density is (heat-kernel / zeta form)
    V(R) = (1/2) sum_fields (+/-) Tr log(-box + |n|^2/R^2)  ->  V(R) = C / R^4
with C a pure number from the field content (Epstein zeta of the lattice).

We test three things:
  (1) the SHAPE: V = C/R^4 is monotonic for ANY content -> no minimum (airtight);
  (2) the CONTENT: SM is not supersymmetric (n_B != n_F) -> C != 0 -> runaway;
      and if you force SUSY (n_B = n_F) -> V == 0 -> still no minimum;
  (3) so a minimum REQUIRES a second scale mu, and then R_min is set by mu -> tunable.

Pure stdlib + numpy.  Run:  python reviews/radion_casimir_attempt.py
"""

import math
import numpy as np

PI = math.pi
R_TARGET = (32 * PI / 3) / (2 * PI)        # = 16/3 = 5.3333 (radius in Planck units)


def theta_lattice(u, box=30):
    """theta(u) = sum_{n in Z^3} e^{-u|n|^2} (cubic lattice)."""
    ns = np.arange(-box, box + 1)
    g = np.exp(-u * ns**2)
    return float(g.sum()**3)


def casimir_coefficient(project_Z2=False, box=24):
    """
    Regularized Casimir number C for a single massless scalar:
        V(R) = C / R^4 ,  C = -(1/2)(4pi)^{-2} * FP int_0^inf du u^{-3}[theta(u)-1].
    We extract the finite part (FP) by subtracting the small-u Weyl terms
    (Poisson: theta(u) ~ (pi/u)^{3/2}) which renormalize the bulk vacuum energy.
    The Z2 projection keeps the even modes: theta_proj(u) = (theta(u)+ (#even))/2
    (schematic; the sign/scaling structure is what matters, not the 3rd digit).
    """
    # numerical finite-part via split at u0=1 with Poisson subtraction for u<1
    from scipy.integrate import quad
    def integrand_high(u):
        return u**-3 * (theta_lattice(u) - 1.0)
    def integrand_low(u):
        # subtract leading Weyl term (pi/u)^{3/2} (the renormalized-away piece)
        return u**-3 * (theta_lattice(u) - (PI / u)**1.5)
    hi, _ = quad(integrand_high, 1.0, np.inf, limit=200)
    lo, _ = quad(integrand_low, 1e-6, 1.0, limit=200)
    # analytic-continued tail of the subtracted Weyl piece: int_0^1 u^{-3}(pi/u)^{3/2}du
    #   = pi^{3/2} int_0^1 u^{-9/2} du  -> zeta-reg value 1/(-7/2) = -2/7
    weyl_tail = PI**1.5 * (-2.0 / 7.0)
    finite = hi + lo + weyl_tail
    C = -0.5 * (4 * PI)**-2 * finite
    return C


def main():
    print("=" * 80)
    print("(1) SHAPE: V(R) = C/R^4 is monotonic for ANY content -> no minimum")
    print("=" * 80)
    print("   A massless bulk field has only one scale (R), so dimensional analysis")
    print("   forces V(R) = C/R^4.  dV/dR = -4C/R^5, which is never 0 at finite R.")
    print("   The Z2 projection and the 8 fixed points change C, NOT the 1/R^4 shape.")
    print("   => no field content whatsoever can make Casimir alone stabilize R.\n")

    print("=" * 80)
    print("(2) CONTENT: compute C; check if the SM can self-stabilize")
    print("=" * 80)
    try:
        C_scalar = casimir_coefficient()
        print(f"   single massless scalar:  C = {C_scalar:.6e}")
        print(f"   sign of C: {'NEGATIVE -> dims collapse (R->0)' if C_scalar < 0 else 'POSITIVE -> dims decompactify (R->inf)'}")
    except Exception as e:
        print(f"   (numeric C skipped: {e}); the SIGN/shape argument below is what matters")
    print()
    print("   Net coefficient for many fields:  C_net = (bosons - fermions) weighted.")
    print("   Standard Model degrees of freedom (4D, schematic count):")
    n_B = 2 + 3*2 + 8*2 + 4          # gamma(2)+W,Z(6)+gluons(16)+Higgs(4) ~ 28 boson dof
    n_F = 3 * (2*2*3 + 2 + 2)        # 3 gen x (quarks 12 + e 2 + nu 2) ~ 48 fermion dof
    print(f"     bosonic dof  ~ {n_B}")
    print(f"     fermionic dof~ {n_F}")
    print(f"     n_B - n_F = {n_B - n_F}  != 0  (the SM is NOT supersymmetric)")
    print("   => C_net != 0  =>  V ~ 1/R^4 runs away. No stabilization, at any R.")
    print("   And the only way to get C_net = 0 is exact SUSY (n_B = n_F with matched")
    print("   boundary conditions) -- but then ALL Casimir terms cancel and V == 0,")
    print("   which ALSO has no minimum.  Heads you runaway, tails you get nothing.\n")

    print("=" * 80)
    print("(3) A minimum needs a SECOND scale -> R_min is set by it (tunable)")
    print("=" * 80)
    print("   Add anything with its own scale (bulk CC, flux, brane tension, a mass m,")
    print("   gaugino condensate): e.g. V = -C/R^4 + D/R^6  ->  R_min = sqrt(3D/2C).")
    print(f"   To land R_min on the target {R_TARGET:.4f} l_P you SOLVE D/C = {2/3*R_TARGET**2:.3f}.")
    print("   Sweep shows R_min slides smoothly with the input; 16/3 is not preferred:")
    for DC in [2, 8, 18.96, 40, 100]:
        print(f"      D/C={DC:>7.2f} l_P^2 ->  R_min = {math.sqrt(1.5*DC):.3f} l_P"
              + ("   <- target (by construction)" if abs(math.sqrt(1.5*DC)-R_TARGET) < 0.03 else ""))
    print()

    print("=" * 80)
    print("VERDICT (honest, no answer inserted)")
    print("=" * 80)
    print("   The radion Casimir route does NOT derive 32pi/3:")
    print("   * massless Casimir is V ~ 1/R^4, monotonic, NO minimum -- for ANY content;")
    print("   * the real (non-SUSY) SM content gives C != 0 -> the extra dimensions run")
    print("     away (collapse or decompactify); exact SUSY gives V == 0;")
    print("   * any finite minimum needs an added scale, which then SETS R_min by hand.")
    print("   No known modulus-stabilization mechanism lands a modulus on a clean")
    print("   transcendental (32pi/3) without tuning -- KKLT/LVS/racetrack values are")
    print("   flux- and coupling-tuned. So R = Z^2 l_P/(2pi) remains an INPUT.")
    print()
    print("   This was the last standing route. It closes the same way as the other")
    print("   five: 32pi/3 is a SCALE, and a scale is set, not derived.")


if __name__ == "__main__":
    main()
