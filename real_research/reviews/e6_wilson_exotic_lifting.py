#!/usr/bin/env python3
"""
The E6 skyscraper, the HARD floor: can we lift the exotics? (open problem #1)
============================================================================

Every 27 of E6 is one chiral generation PLUS unwanted baggage:

    27  --SO(10)-->  16_{+1}  +  10_{-2}  +  1_{+4}      (U(1)_psi charges)
                     ^chiral    ^vector-like exotics^

The 16 is exactly one SM generation (good). The 10 (= 5 + 5bar of SU(5): a
color-triplet down-type quark D + Dbar, and a lepton doublet L + Lbar) and the
1 (an SO(10) singlet) are VECTOR-LIKE exotics. With 3 generations we have
3x16 (want) + 3x(10+1) (must lift to ~M_GUT). Producing a clean 3x16 spectrum
with NOTHING else light is THE exotic-free-vacuum problem -- decades-hard, the
core of heterotic/orbifold string phenomenology (Faraggi; heterotic MSSM scans).

This script is HONEST about it. It does NOT manufacture an exotic-free vacuum.
It (1) states the spectrum, (2) tries the simplest lifting tool -- a single
U(1)_psi Wilson line -- and PROVES BY ENUMERATION that it cannot work, for a
clean arithmetic reason, and (3) lays out what a real solution needs and why it
is a search, not a formula. The result is a correct characterization of the
open problem, which is the honest deliverable.

Pure stdlib.  Run:  python reviews/e6_wilson_exotic_lifting.py
"""

# E6 -> SO(10) x U(1)_psi : the 27 and its U(1)_psi charges.
# (traceless check: 16*(+1) + 10*(-2) + 1*(+4) = 16 - 20 + 4 = 0)
REPS = [("16  (one SM generation, CHIRAL)", 16, +1),
        ("10  (D+Dbar, L+Lbar exotics)",    10, -2),
        ("1   (SO(10) singlet exotic)",      1, +4)]


def part0_spectrum():
    print("=" * 78)
    print("(0) The spectrum we have to clean up:  3 x 27")
    print("=" * 78)
    tot = sum(d for _, d, _ in REPS)
    print(f"   27 = 16 + 10 + 1   ({tot} states); under SO(10) x U(1)_psi:")
    for name, dim, q in REPS:
        role = "KEEP (chiral)" if dim == 16 else "LIFT (vector-like)"
        print(f"     {name:<36} dim={dim:>2}  q_psi={q:+d}   -> {role}")
    print("   Goal: 3 x 16 light, and the 3 x (10 + 1) all heavy (~M_GUT).")
    print("   The 16 is chiral -> protected, cannot be paired away (no 16bar).")
    print("   The 10, 1 are vector-like -> CAN be lifted, IF the embedding cooperates.\n")


def part1_mechanism():
    print("=" * 78)
    print("(1) The tool: an orbifold Wilson line projects states by their charge")
    print("=" * 78)
    print("   A Wilson line W = exp(2pi i k * Q_psi / N) (order-N, level k) multiplies")
    print("   each piece by a phase exp(2pi i k q / N). On the orbifold a state keeps")
    print("   its massless zero mode only if that phase is trivial (= +1); otherwise")
    print("   it is projected to a KK mass ~ 1/R. So IN PRINCIPLE a Wilson line can")
    print("   separate the 16 from the 10+1 -- IF their charges have the right")
    print("   arithmetic. We now test whether they do.\n")


def survives(k, q, N):
    """Zero mode kept iff the Wilson phase exp(2pi i k q/N) is trivial: N | k*q."""
    return (k * q) % N == 0


def part2_obstruction():
    print("=" * 78)
    print("(2) The attempt and its FAILURE: a single U(1)_psi Wilson line cannot do it")
    print("=" * 78)
    print("   Enumerate order-N lines (N in {2,3,4,6}, the crystallographic orders),")
    print("   all levels k. We want a row:  16 KEPT, 10 PROJECTED, 1 PROJECTED.")
    print()
    print(f"   {'N':>2} {'k':>2}  {'16(q=+1)':>10} {'10(q=-2)':>10} {'1(q=+4)':>9}   {'desired?':>9}")
    found = False
    for N in (2, 3, 4, 6):
        for k in range(N):
            s16 = survives(k, +1, N)
            s10 = survives(k, -2, N)
            s1 = survives(k, +4, N)
            want = (s16 and not s10 and not s1)
            found = found or want
            f = lambda s: "kept" if s else "proj"
            mark = "  <== YES" if want else ""
            print(f"   {N:>2} {k:>2}  {f(s16):>10} {f(s10):>10} {f(s1):>9}   "
                  f"{str(want):>9}{mark}")
        print()
    print(f"   Desired row found anywhere? {found}")
    print()
    print("   WHY (the clean reason): the 16 has |q_psi| = 1, which GENERATES the whole")
    print("   charge lattice Z. A Wilson line trivial on charge 1 (so the 16 is kept)")
    print("   is trivial on EVERY integer charge -- so it keeps the 10 and 1 too.")
    print("   The only k that preserves the 16 is k=0 (no Wilson line), which keeps")
    print("   everything. => a single U(1)_psi Wilson line CANNOT lift the exotics. X\n")


def part3_what_it_needs():
    print("=" * 78)
    print("(3) What a real solution needs -- and why it is a SEARCH, not a formula")
    print("=" * 78)
    print("   Because the simplest tool provably fails, exotic lifting requires the")
    print("   full orbifold machinery, every piece of which is a discrete CHOICE:")
    print("     (a) the Z2xZ2 twist embedded as a gauge SHIFT vector V (acts on the")
    print("         three fixed-point sectors differently -> localizes pieces apart);")
    print("     (b) SEVERAL Wilson lines in non-Abelian directions breaking E6 -> SM")
    print("         (not just the U(1)_psi phase that just failed);")
    print("     (c) SM-singlet flat-direction VEVs <S> giving the vector-like 10,1")
    print("         Dirac masses via superpotential terms S*10*10, S*1*1 once D-flat;")
    print("     (d) modular invariance / level-matching: V and the Wilson lines must")
    print("         satisfy the orbifold consistency (tadpole) conditions.")
    print()
    print("   A working vacuum is one simultaneous choice of (V, Wilson lines, flat")
    print("   directions) that lifts ALL 3x(10+1) in ALL three sectors, keeps exactly")
    print("   3x16 + one light Higgs doublet + the SM gauge group, and is modular")
    print("   invariant. There is no closed-form 'derive it' -- you SCAN. The")
    print("   heterotic/orbifold MSSM landscape (thousands of models scanned; a")
    print("   handful realistic; Faraggi free-fermionic; Lebedev-Nilles-Raby-... mini-")
    print("   landscape) is exactly this search. It is solvable in examples, never")
    print("   'derived', and never unique.\n")


def main():
    part0_spectrum()
    part1_mechanism()
    part2_obstruction()
    part3_what_it_needs()
    print("=" * 78)
    print("VERDICT -- the honest state of open problem #1")
    print("=" * 78)
    print("  * The exotics are REAL (3 x (10+1)) and they are the thing standing")
    print("    between '3x27 on the orbifold' and 'the MSSM'.")
    print("  * The lifting MECHANISM is real and standard (projection + vector-like")
    print("    Dirac masses), but the simplest version -- a U(1)_psi Wilson line --")
    print("    provably cannot do it (the 16 generates the charge lattice).")
    print("  * A genuine exotic-free 3x16 vacuum requires a full (shift + Wilson +")
    print("    flat-direction) construction satisfying modular invariance. That is a")
    print("    decades-hard SEARCH shared with all of string phenomenology -- NOT")
    print("    something this framework derives, and NOT something delivered here.")
    print("  * Honest status: the E6 orbifold GUT is a legitimate STARTING POINT for")
    print("    that search, with the right chiral content (3x16) already in place.")
    print("    The exotic-free endpoint remains OPEN. We characterized the problem")
    print("    correctly; we did not solve it, and we should not claim to.")


if __name__ == "__main__":
    main()
