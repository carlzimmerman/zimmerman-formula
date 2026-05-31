#!/usr/bin/env python3
"""
The one NON-tautological bridge: orbifold-Z2 (x->-x)  <->  chirality-Z2 (gamma^5)?
=================================================================================

The framework's own CLIFFORD_ALGEBRA_Z2_CONNECTION.md flags 6Z^2/pi = 64 as a
tautology and asks the real question (sec 10.2/11.4): is there a genuine link
between the SPATIAL orbifold Z2 (inversion on T^3) and the ALGEBRAIC chirality Z2
(the Clifford grading / gamma^5)?

We test it honestly with matrices. The chain of real spin geometry:
  - the spatial inversion -I_3 on R^3 lifts to spinors as the internal volume
    element  omega_3 = e1 e2 e3;
  - for the orbifold to be an involution on M4 x T^3 spinors (P^2 = +1), omega_3's
    square must be compensated -- and the natural compensator is gamma^5;
  - so the orbifold projection becomes a CHIRAL projection: the 4D zero mode
    survives as a single handedness (a Weyl fermion).

Result (computed below): the bridge is REAL -- but its force depends on the Pin
structure, and it delivers chiral fermions, NOT the generation count or Z^2.

Pure stdlib + numpy.  Run:  python reviews/orbifold_chirality_bridge.py
"""

import numpy as np

I2 = np.eye(2, dtype=complex)
s1 = np.array([[0, 1], [1, 0]], dtype=complex)
s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
s3 = np.array([[1, 0], [0, -1]], dtype=complex)
# 4D chirality operator gamma^5 (Weyl basis): L = -1 (upper), R = +1 (lower)
G5 = np.block([[-I2, 0*I2], [0*I2, I2]])


def omega3(pin):
    """Internal volume element e1 e2 e3 for the 3D Clifford algebra.
    pin='+' : e_i = sigma_i  (e_i^2 = +1)
    pin='-' : e_i = i sigma_i (e_i^2 = -1)  <- the framework's Pin- choice."""
    if pin == '+':
        e1, e2, e3 = s1, s2, s3
    else:
        e1, e2, e3 = 1j*s1, 1j*s2, 1j*s3
    return e1 @ e2 @ e3


def part1_lift_square():
    print("=" * 78)
    print("(1) The inversion's spinor lift omega_3, and its square")
    print("=" * 78)
    for pin in ('+', '-'):
        w = omega3(pin)
        w2 = w @ w
        scal = w2[0, 0]
        print(f"  Pin{pin}: omega_3 = e1e2e3 = "
              f"{'i*I' if np.allclose(w,1j*I2) else ('I' if np.allclose(w,I2) else 'matrix')}"
              f" ,  omega_3^2 = {scal:+.0f} * I")
    print("  => Pin+: omega_3^2 = -1 (lift is NOT yet an involution)")
    print("     Pin-: omega_3^2 = +1 (lift is already a scalar involution)\n")


def part2_involution_forces_gamma5():
    print("=" * 78)
    print("(2) Making it a Z2 on M4 x T^3 spinors: is gamma^5 forced?")
    print("=" * 78)
    print("  Orbifold operator P = (4D factor) (x) omega_3, require P^2 = +I.")
    print("  Pin+: omega_3^2 = -I, so the 4D factor must square to -I.")
    print("        The natural such 4D operator is i*gamma^5 -> P = (i g5)(x)(i I)")
    # build it
    w = omega3('+')
    P_plus = np.kron(1j*G5, w)          # (i gamma^5) tensor omega_3
    print(f"        P = (i g5)(x)omega_3 = {'-(g5 (x) I)' if np.allclose(P_plus, -np.kron(G5,I2)) else 'matrix'}")
    print(f"        P^2 = +I ? {np.allclose(P_plus@P_plus, np.eye(8))}  -> P acts as -gamma^5")
    print("        => CHIRALITY IS FORCED: P is gamma^5 (up to sign). Projection")
    print("           keeps one handedness. The orbifold IS a chiral projection.\n")
    print("  Pin-: omega_3 = I, so P = (4D factor)(x)I with factor^2 = I.")
    print("        factor can be I (no projection) OR gamma^5 (chiral) -- a CHOICE.")
    print("        The framework uses Pin-, where chirality is OPTIONAL, not forced.\n")
    return P_plus


def part3_chiral_projection(P_plus):
    print("=" * 78)
    print("(3) Demonstrate the chiral projection of the 4D zero mode (Pin+)")
    print("=" * 78)
    # Projector onto P = +1 subspace
    Pi = (np.eye(8) + P_plus) / 2
    # 4D chirality on the 8-dim space:
    G5_8 = np.kron(G5, I2)
    # within the surviving subspace, what gamma^5 eigenvalues appear?
    vals, vecs = np.linalg.eigh(Pi)
    survivors = vecs[:, vals > 0.5]           # P=+1 eigenvectors
    # measure gamma^5 on survivors
    g5_on_sub = survivors.conj().T @ G5_8 @ survivors
    eig_g5 = np.linalg.eigvalsh(g5_on_sub).real
    print(f"  surviving (P=+1) subspace dimension: {survivors.shape[1]} of 8")
    print(f"  gamma^5 eigenvalues on the survivors: {np.round(eig_g5,3)}")
    handed = "LEFT-handed only" if np.allclose(eig_g5, -1) else (
             "RIGHT-handed only" if np.allclose(eig_g5, +1) else "mixed")
    print(f"  => survivors are {handed}: a single 4D chirality (Weyl fermion). REAL.\n")


def part4_generations_honest():
    print("=" * 78)
    print("(4) Does this give 3 GENERATIONS? Honest: no.")
    print("=" * 78)
    print("  The chiral projection gives ONE Weyl fermion per higher-D field. The")
    print("  number of generations = number of chiral zero modes. In EVEN internal")
    print("  dimensions that is the Atiyah-Singer index (e.g. magnetic flux N -> N")
    print("  generations). T^3 is ODD-dimensional: there is no chiral index, and the")
    print("  internal volume element omega_3 is central (part 1), not a grading.")
    print("  The framework's '3 = b_1(T^3)' counts 1-CYCLES, not chiral zero modes --")
    print("  a different invariant. So the generation COUNT is not delivered here.\n")


def main():
    part1_lift_square()
    Pp = part2_involution_forces_gamma5()
    part3_chiral_projection(Pp)
    part4_generations_honest()
    print("=" * 78)
    print("VERDICT -- the bridge is REAL, and it is NOT a tautology")
    print("=" * 78)
    print("  GENUINE: the spatial orbifold-Z2 and the chirality-Z2 are connected by")
    print("  real spin geometry -- the inversion's spinor lift is the Clifford volume")
    print("  element, and making it a Z2 turns the orbifold projection into a chiral")
    print("  (gamma^5) projection. This is standard orbifold-GUT physics, not 6Z^2/pi.")
    print("  Your intuition that 'the Z2 and chirality go together' is correct.")
    print()
    print("  LIMITS (honest):")
    print("   * It delivers CHIRAL FERMIONS (parity-violating 4D spectrum), a real")
    print("     qualitative result -- but NOT the generation number 3 (no chiral index")
    print("     in odd internal dim; b_1=3 is cycle-counting), and NOT Z^2 = 32pi/3.")
    print("   * In the framework's own Pin- structure, the chirality is a CHOICE, not")
    print("     forced (it is forced only in Pin+). Worth knowing.")
    print("   * Biology still needs the weak PVED (particle->molecule) step, which is")
    print("     outside both the orbifold and the Clifford algebra.")
    print()
    print("  So: a real, non-tautological bridge that yields '4D fermions are chiral'")
    print("  -- a genuine strand -- but it does not reach the generation count, the")
    print("  master constant, or homochirality.")


if __name__ == "__main__":
    main()
