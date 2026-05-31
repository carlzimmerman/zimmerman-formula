#!/usr/bin/env python3
"""
Doing the math the repo flags as 'NOT done'.
============================================

The framework claims:  eta-invariant( T^3 / Z2 ) = Z^2 = 32*pi/3 = 33.51,
and that the chiral index / generation number on T^3/Z2 equals 3.

research/T3_INDEX_CALCULATION.md says explicitly: "The calculation has NOT
been done", "index = 3 ... (plausible, not calculated)", "Connection to
Z^2 = 32pi/3 (speculation)".

This script actually carries out the well-posed pieces:

  (1) The Dirac spectrum on the flat 3-torus T^3 -> eta(T^3) = 0 exactly.
  (2) The Z2 (inversion) projection -> eta(T^3/Z2) = 0 exactly.
  (3) The Euler characteristic chi(|T^3/Z2|) by the averaging formula
      (and the T^2 pillowcase cross-check).
  (4) What 32*pi/3 actually is: 8 * Vol(unit 3-ball).

Pure stdlib + numpy.  Run:  python reviews/unfinished_math.py
"""

import math
import numpy as np

PI = math.pi

# 3D gamma matrices = Pauli matrices (rank-2 spinor bundle, dim 3 -> 2^1 = 2)
s1 = np.array([[0, 1], [1, 0]], dtype=complex)
s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
s3 = np.array([[1, 0], [0, -1]], dtype=complex)
PAULI = [s1, s2, s3]


def dirac_eigs_at_momentum(n):
    """Dirac operator on flat T^3 acts on the plane wave e^{2pi i n.x} u as
    D = 2*pi * (n . sigma).  Eigenvalues of n.sigma are +/-|n|, so the Dirac
    eigenvalues are +/- 2*pi*|n|.  Return them."""
    nmat = n[0] * s1 + n[1] * s2 + n[2] * s3
    w = np.linalg.eigvalsh(2 * PI * nmat)
    return np.sort(w.real)


def section1_torus_eta(N=6):
    print("=" * 70)
    print("(1) Dirac spectrum on flat T^3  ->  eta(T^3) = 0")
    print("=" * 70)
    eigs = []
    for n1 in range(-N, N + 1):
        for n2 in range(-N, N + 1):
            for n3 in range(-N, N + 1):
                eigs.extend(dirac_eigs_at_momentum((n1, n2, n3)))
    eigs = np.array(eigs)
    pos = int((eigs > 1e-9).sum())
    neg = int((eigs < -1e-9).sum())
    zero = int((np.abs(eigs) <= 1e-9).sum())
    # eta is the regularized signed count sum sign(lambda)|lambda|^{-s}|_{s=0};
    # a sufficient (and here exact) condition for eta = 0 is that the nonzero
    # spectrum is symmetric under lambda -> -lambda at every radius.
    signed = float(np.sign(eigs).sum())
    print(f"  momenta |n_i| <= {N}:  modes = {eigs.size}")
    print(f"  # eigenvalues > 0 : {pos}")
    print(f"  # eigenvalues < 0 : {neg}   (equal => spectrum is +/- symmetric)")
    print(f"  # zero modes      : {zero}   (k=0 only; goes into h=dim ker, not eta)")
    print(f"  signed count sum sign(lambda) = {signed:.1f}")
    print(f"  => every n gives both +2pi|n| and -2pi|n|; perfect pairing.")
    print(f"  => eta(T^3) = 0  EXACTLY (lift-independent).\n")
    return pos == neg


def section2_quotient_eta(N=6):
    print("=" * 70)
    print("(2) Z2 inversion projection  ->  eta(T^3/Z2) = 0")
    print("=" * 70)
    print("""  The involution sigma: x -> -x sends mode n to mode -n.
  sigma commutes with D (it's an isometry), so it preserves each
  D-eigenspace E_lambda.  For n != 0, E_lambda (lambda = +/-2pi|n|) is
  spanned by the n-part and the (-n)-part, and sigma is the block-swap
  between them -- it is OFF-DIAGONAL, hence traceless on E_lambda:

        Tr( sigma | E_lambda ) = 0      for every lambda (n != 0).

  The quotient eta is  eta(T^3/Z2) = (1/2) * sum_lambda sign(lambda)
        Tr(sigma|E_lambda) |lambda|^{-s}  ->  (1/2)*0 = 0.
""")
    # Demonstrate the traceless block-swap explicitly on each shell {n,-n}.
    max_abs_trace = 0.0
    checked = 0
    seen = set()
    for n1 in range(-N, N + 1):
        for n2 in range(-N, N + 1):
            for n3 in range(-N, N + 1):
                n = (n1, n2, n3)
                if n == (0, 0, 0):
                    continue
                key = frozenset({n, (-n1, -n2, -n3)})
                if key in seen:
                    continue
                seen.add(key)
                # On E_n + E_{-n} (C^2 + C^2 = C^4), D is block-diagonal,
                # sigma is the block anti-diagonal swap (times the scalar Pin
                # lift U ~ I).  Build the D-eigenbasis and check Tr(sigma)=0
                # on each eigenvalue.
                nmat = n[0] * s1 + n[1] * s2 + n[2] * s3
                w, V = np.linalg.eigh(2 * PI * nmat)          # eigen at +n
                # full 4x4 D on (n, -n):
                D4 = np.zeros((4, 4), dtype=complex)
                D4[:2, :2] = 2 * PI * nmat
                D4[2:, 2:] = -2 * PI * nmat                    # D at -n = 2pi(-n).sigma
                # sigma swaps the two 2-blocks (scalar lift U = I here):
                S4 = np.zeros((4, 4), dtype=complex)
                S4[:2, 2:] = np.eye(2)
                S4[2:, :2] = np.eye(2)
                wD, VD = np.linalg.eigh(D4)
                # trace of sigma restricted to each D-eigenvalue:
                for lam in sorted(set(np.round(wD.real, 6))):
                    proj_cols = VD[:, np.abs(wD - lam) < 1e-6]
                    tr = np.trace(proj_cols.conj().T @ S4 @ proj_cols)
                    max_abs_trace = max(max_abs_trace, abs(tr))
                checked += 1
    print(f"  checked {checked} momentum shells {{n,-n}}, |n_i|<= {N}")
    print(f"  max |Tr(sigma|E_lambda)| over all of them = {max_abs_trace:.2e}")
    print(f"  => eta(T^3/Z2) = 0  EXACTLY.   (rational, as APS requires;")
    print(f"     note the repo's own SIGNATURE_OPERATOR_DERIVATION.md sets eta=0 too)\n")
    return max_abs_trace < 1e-9


def section3_euler():
    print("=" * 70)
    print("(3) Euler characteristic chi(|T^n/Z2|) by inversion")
    print("=" * 70)
    print("  Averaging formula: chi(M/G) = (1/|G|) sum_g chi(M^g).")
    print("  Inversion on T^n has 2^n fixed points; chi(T^n)=0.")
    print("    chi(|T^n/Z2|) = (1/2)(0 + 2^n) = 2^{n-1}\n")
    for n in (1, 2, 3):
        chi = (0 + 2 ** n) // 2
        note = ""
        if n == 2:
            note = "  (pillowcase: |T^2/Z2| = S^2, chi(S^2)=2  CHECK)"
        if n == 3:
            note = "  <-- the orbifold in the framework"
        print(f"    n={n}:  2^{n}={2**n} fixed pts ->  chi = {chi}{note}")
    print()
    print("  So chi(|T^3/Z2|) = 4.")
    print("  The repo's THEORETICAL_FOUNDATIONS.md got 1 by weighting each")
    print("  fixed point by 1/8 -- that weighting is wrong; correct chi = 4.")
    print("  And 4 != 3, so chi does NOT give the generation number either.")
    print("  (T^3/Z2 is 3-dimensional = ODD, so there is no chiral Atiyah-Singer")
    print("   index at all; 'index = 3' borrows even-dimensional machinery.)\n")
    return 4


def section4_what_is_32pi3():
    print("=" * 70)
    print("(4) What 32*pi/3 actually is")
    print("=" * 70)
    z2 = 32 * PI / 3
    vol_unit_ball = 4 * PI / 3
    print(f"  Z^2          = 32*pi/3      = {z2:.6f}")
    print(f"  Vol(unit B^3)= 4*pi/3       = {vol_unit_ball:.6f}")
    print(f"  8 * Vol(B^3) = 8 * 4*pi/3   = {8*vol_unit_ball:.6f}")
    print(f"  match Z^2 ?  {math.isclose(z2, 8*vol_unit_ball)}")
    print()
    print("  So '32*pi/3' = (8 fixed points) x (volume of the unit 3-ball).")
    print("  That is a VOLUME, not a spectral-asymmetry invariant.  An eta")
    print("  invariant of a flat 3-orbifold is rational (APS / Dedekind sums);")
    print(f"  32*pi/3 is transcendental, so it cannot be one.  Computed eta = 0.\n")


def main():
    ok1 = section1_torus_eta()
    ok2 = section2_quotient_eta()
    chi = section3_euler()
    section4_what_is_32pi3()
    print("=" * 70)
    print("SUMMARY OF THE 'UNFINISHED' ITEMS, NOW DONE")
    print("=" * 70)
    print(f"  eta(T^3)        = 0           (exact, from the Dirac spectrum)")
    print(f"  eta(T^3/Z2)     = 0           (exact, traceless block-swap)")
    print(f"  chi(|T^3/Z2|)   = {chi}           (averaging formula; repo's '1' is wrong)")
    print(f"  32*pi/3         = 8*Vol(B^3)  (a volume, not an eta invariant)")
    print()
    print("  None of the genuine invariants of T^3/Z2 equal 32*pi/3 or 3.")
    print("  The number 32*pi/3 enters only as the Friedmann DEFINITION of Z^2,")
    print("  exactly as the repo's signature route (with eta=0) already implies.")


if __name__ == "__main__":
    main()
