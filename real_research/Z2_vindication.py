#!/usr/bin/env python3
"""
Can Z^2 = 32pi/3 be vindicated? Every route, worked honestly.
=============================================================

Carl asked me to ultrathink whether there's a vindication I missed. I tried hard to
FIND one (not to dismiss). Here is the complete map: the strongest genuine case FOR
Z, every route that fails and exactly why, and the one observation that would settle it.

STRUCTURE (what Z^2 actually is):
  Z^2 = 32pi/3 = 4 * (8pi/3).  The 8pi/3 is FORCED by Friedmann (H^2 = (8pi/3) G rho).
  The only free content is the '4' = 2^2, i.e. the factor of 1/2 in
      a0 = (c/2) sqrt(G rho_c) = c^2/(2 R_dyn),   R_dyn = c/sqrt(G rho_c).
  So "vindicate Z^2=32pi/3" == "justify a0 = HALF the surface gravity of the cosmic
  DYNAMICAL scale" -- one dimensionless number, the coefficient a0/cH = 1/Z = 0.1727.

Run:  python real_research/Z2_vindication.py
"""

import math

c = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
Z = math.sqrt(32 * math.pi / 3)
A0_SPARC = 1.13e-10


def main():
    print("=" * 76)
    print("(A) The strongest genuine case FOR Z (steelman -- I tried to make it work)")
    print("=" * 76)
    print("  1. a0 ~ cH0 is an established empirical fact (Milgrom 1983 coincidence).")
    print("  2. MOND modifies GRAVITY, so the relevant cosmic clock is the GRAVITATIONAL")
    print("     dynamical time t_dyn = 1/sqrt(G rho), NOT the expansion time 1/H. Using it,")
    print("     a0 = (c/2) sqrt(G rho) -- a principled CHOICE of scale, not arbitrary.")
    print("  3. The 1/2 is the Schwarzschild surface-gravity factor a0 = c^2/(2R): MOND")
    print("     as the surface gravity of a cosmic horizon. Via Friedmann this is EXACTLY")
    print("     cH/Z, Z^2 = 32pi/3 -- with NO further free parameter.")
    print("  4. Empirically it is COMPETITIVE-TO-BEST among the coefficient candidates,")
    print("     and -- the real point -- it is favoured specifically at the PLANCK H0:")
    print(f"     {'H0':>6}{'cH0':>11}{'best-fit coeff for SPARC a0=1.13e-10':>40}")
    for H0 in (67.4, 70.0, 73.0):
        cH = c * H0 * 1e3 / MPC
        best = min([("1/Z (this)", 1/Z), ("1/6 Verlinde", 1/6),
                    ("1/2pi Milgrom", 1/(2*math.pi))],
                   key=lambda t: abs(t[1]*cH - A0_SPARC))[0]
        print(f"     {H0:>6.1f}{cH:>11.2e}{best:>40}")
    print("  => IF the Hubble tension resolves toward the early-universe (Planck) value,")
    print("     Z is the best coefficient. That is a real, falsifiable, conditional claim.\n")

    print("=" * 76)
    print("(B) Every route that does NOT vindicate it -- and exactly why")
    print("=" * 76)
    print("  * TOPOLOGY (Z^2 = eta-invariant of T^3/Z2): FALSE. The rigorous spectral")
    print("    eta-invariant is exactly 0 (verified over 4e6 modes); '4pi/3' only appears")
    print("    by replacing D with |D|. Z^2=32pi/3 is a DEFINITION (Friedmann), not a")
    print("    topological derivation.")
    print("  * RIGOROUS free-fall: the proper collapse time t=sqrt(3pi/32 G rho) gives")
    print(f"    a0 = cH/pi (coeff {1/math.pi:.3f}), NOT cH/Z. Z uses the LOOSE t=1/sqrt(Grho).")
    print("  * CLEAN horizon identity: the Hubble radius IS its own Schwarzschild radius")
    print("    (exact), but its surface gravity is cH/2 (coeff 0.5) -- it OVERSHOOTS the")
    print("    observed a0 by ~3x. Getting to Z needs the dynamical-scale swap, which is")
    print("    the un-principled step.")
    print("  * ENTROPY / horizon thermodynamics: Verlinde -> 1/6, Gibbons-Hawking -> 1/2pi.")
    print("    Neither gives 1/sqrt(32pi/3). (And Verlinde is contested.)")
    print("  * NUMEROLOGY (4Z^2+3 = alpha^-1, etc.): false-discovery -- an arbitrary O(100)")
    print("    target is hit to <0.004% ~20% of the time. ~0 bits of evidence.")
    print("  * GEOMETRY '8 x 4pi/3 = cube x ball': just the trivial identity 4*(8pi/3) =")
    print("    8*(4pi/3); it relabels the Friedmann number, it does not derive it.\n")

    print("=" * 76)
    print("(C) Is there ANY Z-dependent prediction to test? (the honest blocker)")
    print("=" * 76)
    print("  The evolving law a0(z)/a0(0) = E(z) is Z-INDEPENDENT (Z cancels). The de Sitter")
    print("  temperature T_a0 = T_dS/Z and the dynamical scale R_dyn = (Z/2)R_H are both")
    print("  unobservable. So the ONLY Z-dependent observable is the ABSOLUTE a0/cH0 = 1/Z,")
    print("  and that is degenerate with H0 (Hubble tension) and a0's ~20% M/L systematic.\n")

    print("=" * 76)
    print("(D) The one observation that WOULD vindicate it")
    print("=" * 76)
    d_Z6 = abs(1/Z - 1/6) / (1/6) * 100
    print(f"   Measure a0/cH0 to ~2%: 1/Z=0.1727 vs 1/6=0.1667 ({d_Z6:.1f}% apart) needs")
    print(f"   sigma(a0/cH0) < {d_Z6/2:.1f}%. That requires BOTH:")
    print("     (i) a0 to ~2% from GAS-DOMINATED rotators (HI mass, no stellar M/L) --")
    print("         feasible with WALLABY-class samples (random scatter averages down);")
    print("     (ii) the Hubble tension resolved to ~2%.")
    print("   IF then a0/cH0 = 0.173 (not 0.167 or 0.159) AND H0 is the Planck value,")
    print("   Z is vindicated over its rivals. Anything else falsifies it. It is a real,")
    print("   demanding, but well-defined observational program.\n")

    print("=" * 76)
    print("VERDICT -- honestly, after trying to make it work")
    print("=" * 76)
    print("  * No, Z^2=32pi/3 is NOT vindicated now. Its entire non-trivial content is the")
    print("    coefficient 1/Z = 0.173, one member of a family {1/2, 1/pi, 1/6, 1/2pi, 1/Z}")
    print("    that the data cannot currently separate (H0 + a0 systematics ~22%, fork ~4%).")
    print("  * The HONEST best case is real and I had under-credited it: a0 = (c/2)sqrt(Grho)")
    print("    is the natural GRAVITATIONAL-dynamical-scale reading, and Z is the best-fit")
    print("    coefficient at the PLANCK H0. That makes Z a falsifiable CONDITIONAL bet:")
    print("    'if early-universe H0 is right and a0/cH0=0.173, Z wins.'")
    print("  * But every DERIVATION route gives a different number (pi, 1/2, 1/6, 1/2pi) or")
    print("    is false (the topology). So Z is a defensible, near-miss-favoured POSIT --")
    print("    not a theorem. Vindicating it is one precise measurement away, not a proof.")


if __name__ == "__main__":
    main()
