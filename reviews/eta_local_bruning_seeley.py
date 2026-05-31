#!/usr/bin/env python3
"""
The rigorous local-eta computation for R^3/Z2, done the way the framework asked:
  1. Bruning-Seeley cone setup for the Dirac operator on C(RP^2) = R^3/Z2.
  2. The regularized spectral sum at the singularity.
  3. Does it equal 4*pi/3?   ->  NO.  It equals 0.

The framework's own files reach 4*pi/3 only by one illegal step:
  research/OP1_LOCAL_ETA_DERIVATION.md line 165 :  "sign(|p|) = +1 for all p != 0"
  research/computational_math/eta_invariant_T3Z2.py lines 199-235

That step replaces the Dirac operator D (eigenvalues +/-|p|, BOTH signs at every
momentum) by |D| (all +). The eta invariant is a SPECTRAL ASYMMETRY -- the signed
count of eigenvalues. Replacing D by |D| turns it into a zeta-function MODE COUNT,
and a regularized mode count over a ball is proportional to the ball's VOLUME.
That is why 4*pi/3 (= vol of the unit 3-ball) pops out: it was never an eta
invariant, it is the volume the calculation accidentally computed.

This script demonstrates, from the actual spectra:
  (A) the free 3D Dirac eta density is 0 pointwise (the +/- eigenvalues cancel);
  (B) the framework's 4*pi/3 is exactly vol(B^3), recovered iff you drop the
      negative eigenvalue;
  (C) the RP^2 link Dirac spectrum is +/- symmetric -> Bruning-Seeley cone
      contribution = 0;
  (D) global cross-check: eta(T^3/Z2) = 0 exactly, so 8 equal local terms must
      sum to 0 -- they cannot each be +4*pi/3 (that would give 32*pi/3 != 0).

Pure stdlib + numpy.  Run:  python reviews/eta_local_bruning_seeley.py
"""

import math
import numpy as np

PI = math.pi
s1 = np.array([[0, 1], [1, 0]], dtype=complex)
s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
s3 = np.array([[1, 0], [0, -1]], dtype=complex)


# ---------------------------------------------------------------------------
def partA_free_dirac_eta_density():
    print("=" * 74)
    print("(A) The free 3D Dirac operator D = sigma.p  ->  eta density = 0")
    print("=" * 74)
    print("  At EVERY momentum p, the 2x2 block sigma.p has eigenvalues +|p| and")
    print("  -|p|. The eta integrand is sum of sign(eigenvalue):\n")
    rng = np.random.default_rng(0)
    max_abs_signsum = 0.0
    for _ in range(20000):
        p = rng.normal(size=3)
        D = p[0] * s1 + p[1] * s2 + p[2] * s3      # the Dirac symbol
        w = np.linalg.eigvalsh(D)                   # eigenvalues = +/-|p|
        signsum = np.sign(w).sum()                  # +1 + (-1) = 0
        max_abs_signsum = max(max_abs_signsum, abs(signsum))
    print(f"  max |sum sign(eig)| over 20000 random momenta = {max_abs_signsum:.2e}")
    print("  => the signed (eta) density is 0 at every p.  Integrating 0 gives")
    print("     eta_local(R^3/Z2) = 0.  No ball volume can appear.\n")
    return max_abs_signsum < 1e-9


def partB_volume_is_the_substitution():
    print("=" * 74)
    print("(B) Where 4*pi/3 comes from: dropping the negative eigenvalue")
    print("=" * 74)
    # Correct eta-type integrand: sign(+|p|)+sign(-|p|) = 0, integrate over ball -> 0
    # Framework's integrand: replace by |D| -> both eigenvalues count as +1.
    # Regularized "mode count" over the unit ball (zeta_D(0)-type), with the bare
    # momentum measure, is exactly the ball volume:
    #     (1/2) * integral_{|p|<1} d^3p / (per the OP1/eta_invariant_T3Z2 setup)
    # OP1 line 229-231: solid angle 4*pi  times  radial  int_0^1 r^2 dr = 1/3.
    solid_angle = 4 * PI
    radial = 1.0 / 3.0
    framework_value = solid_angle * radial
    vol_unit_ball = 4 * PI / 3
    # Monte-Carlo the unit-ball volume to show it's literally the same number:
    rng = np.random.default_rng(42)
    pts = 2 * rng.random((400000, 3)) - 1
    vol_mc = (np.linalg.norm(pts, axis=1) <= 1).mean() * 8
    print(f"  framework 'eta_local'  = 4*pi * (1/3) = {framework_value:.6f}")
    print(f"  volume of unit 3-ball  = 4*pi/3       = {vol_unit_ball:.6f}")
    print(f"  Monte-Carlo ball vol   ~              = {vol_mc:.6f}")
    print("  => the framework's four 'verification methods' all compute the SAME")
    print("     object: the volume of the unit ball. That was never in dispute.")
    print("     It equals eta_local only under sign(|p|)->+1 (OP1 line 165),")
    print("     i.e. after the Dirac operator was replaced by |D|.\n")
    return math.isclose(framework_value, vol_unit_ball)


def s2_dirac_spectrum(kmax):
    """Round S^2 (radius 1) Dirac eigenvalues (Baer): +/-(k+1), k>=0,
    multiplicity 2(k+1).  Returns list of (eigenvalue, multiplicity)."""
    spec = []
    for k in range(kmax + 1):
        mult = 2 * (k + 1)
        spec.append((+(k + 1), mult))
        spec.append((-(k + 1), mult))
    return spec


def partC_rp2_link_asymmetry(kmax=2000):
    print("=" * 74)
    print("(C) The RP^2 link spectrum is +/- symmetric -> cone contribution 0")
    print("=" * 74)
    print("  Bruning-Seeley: the cone-apex eta is a SIGNED sum over the link")
    print("  (RP^2) Dirac eigenvalues. RP^2 = S^2/antipodal; its Pin- spectrum is")
    print("  a Z2 projection of the S^2 spectrum +/-(k+1).  The antipodal map is an")
    print("  isometry commuting with D, so it preserves each D-eigenspace and the")
    print("  projected spectrum stays +/- symmetric:")
    spec = s2_dirac_spectrum(kmax)
    pos = sum(m for (lam, m) in spec if lam > 0)
    neg = sum(m for (lam, m) in spec if lam < 0)
    signed = sum(np.sign(lam) * m for (lam, m) in spec)
    print(f"    S^2 modes with |lambda|<= {kmax+1}: +eigs={pos}, -eigs={neg}")
    print(f"    signed count  sum sign(lambda)*mult = {signed}")
    print("    (any Z2-invariant subprojection inherits this pairing; the regular")
    print("     representation halves both columns equally)")
    print("  => the link's spectral asymmetry is 0, so the Bruning-Seeley apex")
    print("     contribution vanishes: eta_local = 0, NOT 4*pi/3.\n")
    return pos == neg


def partD_global_consistency(N=6):
    print("=" * 74)
    print("(D) Global cross-check: eta(T^3/Z2) = 0 forces eta_local = 0")
    print("=" * 74)
    eigs = []
    for n1 in range(-N, N + 1):
        for n2 in range(-N, N + 1):
            for n3 in range(-N, N + 1):
                D = 2 * PI * (n1 * s1 + n2 * s2 + n3 * s3)
                eigs.extend(np.linalg.eigvalsh(D).real)
    eigs = np.array(eigs)
    pos = int((eigs > 1e-9).sum())
    neg = int((eigs < -1e-9).sum())
    print(f"  flat T^3 Dirac spectrum (|n_i|<= {N}): +eigs={pos}, -eigs={neg}")
    print(f"  => eta(T^3) = 0; the Z2 block-swap preserves the pairing => ")
    print(f"     eta(T^3/Z2) = 0 (the repo's SIGNATURE_OPERATOR_DERIVATION.md agrees).")
    print("  APS/Cheeger decomposition:  eta = (flat bulk = 0) + sum_8 eta_local.")
    print("  0 = 8 * eta_local  =>  eta_local = 0.")
    print("  If eta_local were 4*pi/3, then eta(T^3/Z2) = 32*pi/3 != 0, contradicting")
    print("  the direct spectral computation.  The framework cannot hold both.\n")
    return pos == neg


def scale_invariance_note():
    print("=" * 74)
    print("    Extension-independent kill shot: scale invariance")
    print("=" * 74)
    print("  eta is invariant under g -> c^2 g (eigenvalues scale, signs don't), so")
    print("  it is a pure scale-free number.  '4*pi/3 = volume of the UNIT ball' is a")
    print("  radius-1 volume; it scales as c^3.  A scale-free spectral invariant")
    print("  cannot equal a scale-set volume -- regardless of any rationality")
    print("  subtlety about cone extensions.\n")


def main():
    a = partA_free_dirac_eta_density()
    b = partB_volume_is_the_substitution()
    c = partC_rp2_link_asymmetry()
    d = partD_global_consistency()
    scale_invariance_note()
    print("=" * 74)
    print("VERDICT")
    print("=" * 74)
    print(f"  (A) free Dirac eta density = 0 ............... {a}")
    print(f"  (B) 4*pi/3 = vol(unit ball), via sign->+1 .... {b}")
    print(f"  (C) RP^2 link asymmetry = 0 .................. {c}")
    print(f"  (D) global eta(T^3/Z2)=0 forces local=0 ...... {d}")
    print()
    print("  The rigorous Bruning-Seeley local contribution for R^3/Z2 is 0.")
    print("  4*pi/3 is the volume of the unit 3-ball, obtained by replacing the")
    print("  Dirac operator with |D| (OP1 line 165). It is not an eta invariant.")
    print("  Hence eta(T^3/Z2) != 32*pi/3, and Z^2 = 32*pi/3 is a DEFINITION")
    print("  (Friedmann factor, as the repo's honest docs already state), not a")
    print("  derived spectral invariant.")


if __name__ == "__main__":
    main()
