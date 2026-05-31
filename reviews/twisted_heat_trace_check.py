#!/usr/bin/env python3
"""
Honest check of the 'spinorial local spectral charge' sigma(p) = 4pi/3 claim.
=============================================================================

The proposal (research/computational_math/spinorial_heat_kernel.py) defines
    sigma(p) = (1/dim S) lim_{t->0} (4 pi t)^{3/2} Tr^{tw}(e^{-tD^2})|_p
and claims sigma(p) = 4pi/3 per Z2 fixed point, so 8 * 4pi/3 = 32pi/3 = Z^2.

But in that script the 4pi/3 is HARD-CODED:
    spinorial_heat_kernel.py line 163:  vol_effective = (4*PI/3) * R**3
and the script itself admits the two choices it makes:
    line 156: 'which volume do we use?'   (picks the full ball over the
              fundamental domain 2pi/3)
    line 202: 'To get 4pi/3, we need to divide by 2 somewhere.'

Here we compute the genuine twisted (equivariant) heat trace honestly and show
it gives an INTEGER (1 per point -> 8 total), never 4pi/3. The 4pi/3 only
appears if you multiply the point heat-kernel density by the volume of a
radius-1 ball -- i.e. insert a scale and call a density times a volume a 'trace'.

Pure stdlib + numpy.  Run:  python reviews/twisted_heat_trace_check.py
"""

import math
import numpy as np

PI = math.pi
s1 = np.array([[0, 1], [1, 0]], dtype=complex)
s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
s3 = np.array([[1, 0], [0, -1]], dtype=complex)


def scalar_equivariant_trace(t, box=8.0, n=240):
    """Genuine twisted trace  Tr(sigma e^{-t Delta})  for the inversion
    sigma: x -> -x on R^3, scalar Laplacian:
        Tr = integral K(t; -x, x) d^3x ,  K(t;y,x)=(4pi t)^{-3/2} e^{-|y-x|^2/4t}.
    K(t;-x,x) = (4pi t)^{-3/2} e^{-|x|^2/t}.  Exact value = 1/8."""
    xs = np.linspace(-box, box, n)
    dx = xs[1] - xs[0]
    # separable Gaussian: integral factorizes
    g = np.exp(-xs**2 / t) * dx
    I = g.sum()**3                      # (int e^{-x^2/t}dx)^3
    return (4 * PI * t) ** (-1.5) * I


def main():
    print("=" * 78)
    print("(1) The genuine twisted trace is FINITE = 1/8 (scalar), no 4pi/3")
    print("=" * 78)
    for t in (0.5, 0.2, 0.1):
        val = scalar_equivariant_trace(t)
        print(f"   t={t:>4}:  Tr(sigma e^-tDelta) = {val:.5f}   (exact 1/8 = 0.125)")
    print("   The (4pi t)^{-3/2} and the Gaussian integral (pi t)^{3/2} cancel to a")
    print("   pure number 1/8 = 1/|det(I - (-I))| = 1/8.  No volume, no 4pi/3.\n")

    print("=" * 78)
    print("(2) The Pin- Clifford element gamma (gamma^2=-1) is TRACELESS")
    print("=" * 78)
    for name, g in [("sigma_1", s1), ("sigma_2", s2), ("sigma_3", s3)]:
        print(f"   tr_S[{name}] = {np.trace(g).real:+.1f}   (gamma^2 = -I, used for the Z2 spin lift)")
    print("   => the genuine equivariant SPINOR trace Tr(gamma e^-tD^2) = tr_S[gamma]*(1/8)")
    print("      = 0.  The twisted (gamma) piece contributes NOTHING.\n")

    print("=" * 78)
    print("(3) So their own definition, done honestly, gives sigma(p) = 1, total 8")
    print("=" * 78)
    print("   Their method of images (spinorial_heat_kernel.py lines 129-134) gives")
    print("   the pointwise twisted kernel  tr_S[(1-gamma)] (4pi t)^{-3/2}")
    tr_1_minus_g = np.trace(np.eye(2) - s3).real        # tr(I) - tr(gamma) = 2 - 0
    print(f"     tr_S[I - gamma] = {tr_1_minus_g:.0f}   (= 2 - 0)")
    sigma_honest = tr_1_minus_g / 2                      # (4pi t)^{3/2} cancels; /dim S = /2
    print(f"     sigma(p) = (4pi t)^{{3/2}} * [{tr_1_minus_g:.0f} (4pi t)^{{-3/2}}] / dimS"
          f" = {tr_1_minus_g:.0f}/2 = {sigma_honest:.0f}")
    print(f"     total over 8 fixed points = 8 * {sigma_honest:.0f} = {8*sigma_honest:.0f}")
    print("   => the honest answer is the INTEGER 8 (= #fixed points = dim H*(T^3)),")
    print("      the real invariant -- NOT 32pi/3.\n")

    print("=" * 78)
    print("(4) Where 4pi/3 actually comes from: a hard-coded unit-ball volume")
    print("=" * 78)
    t = 0.1
    K00 = (4 * PI * t) ** -1.5                # heat-kernel DENSITY at the point
    vol_unit_ball = 4 * PI / 3               # spinorial_heat_kernel.py line 163
    fake = (4 * PI * t) ** 1.5 * (2 * K00 * vol_unit_ball) / 2
    print(f"   density K(t;0,0) = (4pi t)^-3/2 ;  multiply by Vol(B^3,R=1) = 4pi/3:")
    print(f"     (4pi t)^{{3/2}} * [2 * K00 * (4pi/3)] / 2 = {fake:.5f} = 4pi/3")
    print("   But 'density at a point times the volume of a radius-1 ball' is NOT a")
    print("   trace. A real trace localizes via the Gaussian (width sqrt(t)->0) to the")
    print("   finite 1/8 of part (1). The 4pi/3 needs (a) choosing R=1 [a scale] and")
    print("   (b) multiplying a density by a volume. Same insertion as the eta and the")
    print("   OP1 zeta 'derivations' -- third time.\n")

    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    print("   Genuine twisted heat trace at a Z2 fixed point: finite & algebraic")
    print("   (1/8 scalar; 0 for the gamma-twist; sigma(p)=1 => total 8). The 4pi/3 is")
    print("   inserted (line 163) and the /2 is an admitted fudge (line 202). A")
    print("   transcendental 4pi/3 cannot be an equivariant fixed-point term -- those")
    print("   are algebraic. So this does NOT derive 32pi/3; it re-inserts it.")


if __name__ == "__main__":
    main()
