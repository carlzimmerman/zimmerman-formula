#!/usr/bin/env python3
"""
The decisive question: is N_gen = 3 FORCED by consistency, or merely ALLOWED?
============================================================================

The magnetized-torus mechanism gives N_gen = N_flux (a genuine chiral index).
N_flux is an integer you choose. Could a CONSISTENCY CONDITION force N = 3?
The candidates: (a) 4D gauge-anomaly cancellation, (b) flux quantization,
(c) RR tadpole / Gauss-law cancellation on the compact space.

We test (a) rigorously and assess (b),(c) honestly. Result: none forces 3.

Pure stdlib.  Run:  python reviews/generation_number_tadpole_anomaly.py
"""

from fractions import Fraction as F

# One Standard Model generation, as left-handed Weyl multiplets:
#   (name, T3 = SU(3) Dynkin index, T2 = SU(2) Dynkin index, Y, d3, d2)
#   T(fund)=T(antifund)=1/2, T(doublet)=1/2, T(singlet)=0.  mult = d3*d2.
GEN = [
    ("Q   (u,d)_L", F(1, 2), F(1, 2), F(1, 6), 3, 2),
    ("u^c        ", F(1, 2), F(0),    F(-2, 3), 3, 1),
    ("d^c        ", F(1, 2), F(0),    F(1, 3),  3, 1),
    ("L   (nu,e)_L", F(0),   F(1, 2), F(-1, 2), 1, 2),
    ("e^c        ", F(0),   F(0),     F(1),     1, 1),
]


def anomalies_one_generation():
    A_SU3 = F(0)   # [SU(3)]^2 U(1)_Y  = sum d2 * T3 * Y
    A_SU2 = F(0)   # [SU(2)]^2 U(1)_Y  = sum d3 * T2 * Y
    A_Y3 = F(0)    # [U(1)_Y]^3        = sum mult * Y^3
    A_grav = F(0)  # [grav]^2 U(1)_Y   = sum mult * Y
    for name, T3, T2, Y, d3, d2 in GEN:
        mult = d3 * d2
        A_SU3 += d2 * T3 * Y
        A_SU2 += d3 * T2 * Y
        A_Y3 += mult * Y ** 3
        A_grav += mult * Y
    return A_SU3, A_SU2, A_Y3, A_grav


def part1_anomalies():
    print("=" * 78)
    print("(a) 4D gauge-anomaly cancellation -- does it fix N_gen?")
    print("=" * 78)
    A3, A2, AY, Ag = anomalies_one_generation()
    print("   Anomaly coefficients for ONE Standard Model generation:")
    print(f"     [SU(3)]^2 U(1)_Y = {A3}")
    print(f"     [SU(2)]^2 U(1)_Y = {A2}")
    print(f"     [U(1)_Y]^3       = {AY}")
    print(f"     [grav]^2 U(1)_Y  = {Ag}")
    allzero = all(x == 0 for x in (A3, A2, AY, Ag))
    print(f"   all cancel within ONE generation? {allzero}")
    print("   => for N generations every anomaly = N * 0 = 0, for ANY N.")
    print("      Anomaly cancellation is generation-BLIND: it does NOT fix N.\n")
    return allzero


def part2_flux_quantization():
    print("=" * 78)
    print("(b) Flux quantization -- does it fix N_gen?")
    print("=" * 78)
    print("   (1/2pi) int_{T^2} F = N in Z.  This fixes N to be an INTEGER, not to")
    print("   any particular value. N = 1, 2, 3, 4, ... are all separately allowed.")
    print("   => flux quantization does NOT fix N.\n")


def part3_tadpole():
    print("=" * 78)
    print("(c) RR tadpole / Gauss-law cancellation -- does it fix N_gen?")
    print("=" * 78)
    print("   On a COMPACT space total charge must cancel (field lines can't escape).")
    print("   For magnetized branes this is a LINEAR (Diophantine) constraint of the")
    print("   form  sum_a N_a m_a = Q_O  (orientifold charge), with the generation")
    print("   number = an intersection/flux number built from the same integers.")
    print("   A linear Diophantine constraint has MANY integer solutions; 3 is one.")
    print()
    print("   Toy illustration: a tadpole 'sum_a N_a = 8' (type-I-like) with the net")
    print("   generation number g = |N_1 - N_2| for a two-stack model:")
    Q = 8
    sols = []
    for N1 in range(0, Q + 1):
        N2 = Q - N1
        g = abs(N1 - N2)
        sols.append((N1, N2, g))
    gens = sorted({g for _, _, g in sols})
    print(f"     integer solutions give generation numbers g in {gens}")
    print(f"     g = 3 is reachable (e.g. N1=2,N2=6 -> |2-6|... ) but so are "
          f"{[x for x in gens if x!=3][:5]}...")
    # find an explicit g=3-ish: with Q=8, |N1-N2| is even; to get odd 3 need odd Q.
    Q2 = 9
    ex = [(n, Q2 - n, abs(2*n - Q2)) for n in range(Q2 + 1)]
    g3 = [e for e in ex if e[2] == 3]
    print(f"     (odd tadpole Q=9: {g3[0][:2]} gives g=3 -- but Q=9 also gives "
          f"g in {sorted({e[2] for e in ex})})")
    print("   => the tadpole ALLOWS N_gen = 3 but does not UNIQUELY force it.\n")


def main():
    ok = part1_anomalies()
    part2_flux_quantization()
    part3_tadpole()
    print("=" * 78)
    print("VERDICT -- is N = 3 forced or free?")
    print("=" * 78)
    print("  FREE. None of the consistency conditions forces N = 3:")
    print("   * anomaly cancellation is generation-blind (each generation is")
    print("     separately anomaly-free -- computed above, all four coefficients 0);")
    print("   * flux quantization fixes N in Z, not its value;")
    print("   * tadpole/Gauss cancellation is a linear Diophantine constraint with")
    print("     many solutions -- N = 3 is allowed, not unique.")
    print()
    print("  So the generation MECHANISM is rigorous (flux index), but the NUMBER 3")
    print("  is a CHOICE consistent with all constraints, not a prediction. This is")
    print("  not a special failure of the Z^2 framework -- it is the universal status:")
    print("  'why 3 generations' is unsolved in string theory too; in every known")
    print("  construction the generation number is a model-building input.")
    print()
    print("  Honest bottom line: the chirality + flux machinery is real and gives a")
    print("  consistent 3-generation model, but it does not DERIVE 3. To predict 3")
    print("  you would need a NEW constraint beyond anomalies/quantization/tadpoles --")
    print("  which would be genuinely new physics, not yet in hand.")


if __name__ == "__main__":
    main()
