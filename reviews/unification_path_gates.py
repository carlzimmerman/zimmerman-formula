#!/usr/bin/env python3
"""
A path to unification from scaling-MOND geometry -- the gates, with numbers.
===========================================================================

The honest reframe: the "geometry" worth unifying around is NOT Z^2 = 32pi/3 (the
compactification numerology -- dead: constants are search artifacts, the topology
is excluded). It is the DE SITTER HORIZON geometry, in the emergent/entropic-
gravity sense (Jacobson 1995; Padmanabhan; Verlinde 2011/2016; Milgrom 1999):
gravity + inertia emerge from horizon thermodynamics, and the FINITE cosmic
horizon adds a MOND scale a0 ~ cH(z). Scaling MOND, a0(z) = cH(z)/Z, is the
signature that the emergence is real.

This script lays out the path as four GATES, each with a concrete pass/fail test
and its CURRENT status, so the program can live or die on evidence, not faith.

Pure stdlib. Run:  python reviews/unification_path_gates.py
"""

import math

C = 2.99792458e8
MPC = 3.0857e22
A0 = 1.20e-10
A0_SYS = 0.20
Z = 2 * math.sqrt(8 * math.pi / 3)     # 5.78881
H0 = 71.5e3 / MPC
OM, OL = 0.315, 0.685
cH0 = C * H0


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def gate1():
    print("=" * 78)
    print("GATE 1 -- FALSIFICATION (near-term, decisive): the z>10 BTFR test")
    print("=" * 78)
    print("  Claim: a0(z)=a0(0)E(z) -> deep-MOND v_flat = (G M a0(z))^1/4 is LARGER")
    print("  at high z by E(z)^1/4 vs constant-a0. JWST/ALMA rotation + dispersions.")
    print(f"  {'z':>5}{'E(z)':>8}{'E(z)^1/4':>10}{'v_evolv/v_const':>16}")
    for z in (10, 12, 14):
        print(f"  {z:>5}{E(z):>8.1f}{E(z)**0.25:>10.2f}{E(z)**0.25:>16.2f}")
    print("  -> evolving vs constant differ by a FACTOR ~2.2-2.4 at z=12-14, far")
    print("     above the ~25% mass-uncertainty band. A clean separation.")
    print("  STATUS: PASS-so-far. JADES-GS-z14 (ALMA, FWHM~136 km/s) sits with the")
    print("     EVOLVING value (~121) and disfavors constant (~50). More z>10 needed.")
    print("  IF FAIL (z>10 rotations come in at constant-a0): the program is DEAD.")
    print("     Everything below is contingent on this gate. (jwst_rotation_predictions.py)\n")


def gate2():
    print("=" * 78)
    print("GATE 2 -- COSMOLOGICAL CONSISTENCY: re-fit the CMB with scaling a0(z)")
    print("=" * 78)
    zrec = 1089.9
    print(f"  Skordis-Zlosnik RelMOND fits the CMB with CONSTANT a0. Here a0 is")
    print(f"  ~{E(zrec):.0f}x larger at recombination. KEY: a0/cH = 1/Z = {1/Z:.3f} is")
    print("  CONSTANT at every epoch -> the MOND effect is a fixed fraction of horizon")
    print("  dynamics (arguably more natural than constant-a0). But whether the CMB")
    print("  power spectrum SURVIVES scaling a0(z) is an unrun Boltzmann calculation.")
    print("  TEST: modify a SZ/hi_class-type Boltzmann code with a0(z)=cH(z)/Z; demand")
    print("  the TT/EE peaks + lensing stay within Planck error. PASS or FAIL is")
    print("  computable with existing tools.")
    print("  STATUS: OPEN -- the single most important THEORY calculation. Not faked.\n")


def gate3():
    print("=" * 78)
    print("GATE 3 -- DERIVATION FORK: where does the O(1) divisor come from?")
    print("=" * 78)
    a_2pi = cH0 / (2 * math.pi)
    a_Z = cH0 / Z
    band_lo, band_hi = A0 * (1 - A0_SYS), A0 * (1 + A0_SYS)
    print(f"  a0 ~ cH is DERIVED (horizon). The divisor is the open piece:")
    print(f"    cH/2pi        = {a_2pi:.3e}  (clean Gibbons-Hawking; {(a_2pi/A0-1)*100:+.0f}%)")
    print(f"    cH/2sqrt(8pi/3)= {a_Z:.3e}  (geometric Z; {(a_Z/A0-1)*100:+.0f}%, exact)")
    print(f"    both inside a0's systematic band [{band_lo:.2e}, {band_hi:.2e}].")
    print("  THE FORK:")
    print("   (a) DERIVE 2sqrt(8pi/3) from horizon + compactification volume (the")
    print("       'coupling = sqrt(volume modulus)' conjecture). High payoff, likely")
    print("       very hard / maybe impossible -- the horizon alone gives 2pi.")
    print("   (b) ACCEPT a0 = cH/2pi (clean, free, 8% off, within systematics) and DROP")
    print("       the geometric-Z claim. Costs the 'Z links to particle physics' dream,")
    print("       keeps a clean emergent-gravity MOND. <-- the honest default.")
    print("  STATUS: FORK. Data cannot yet separate 2pi from 2sqrt(8pi/3) (8% < 20%).\n")


def gate4():
    print("=" * 78)
    print("GATE 4 -- UNIFICATION: SM (orbifold) + gravity/MOND (horizon) in one action")
    print("=" * 78)
    print("  The unified action (v12_SCALING_MOND_ACTION.md):")
    print("    S = (c^4/16piG)R  +  L_E6->SM(orbifold)  -1/2(d chi)^2 - V(chi)")
    print("        +  L_RelMOND(phi; a0[chi]=cH/Z)")
    print("  Honest content of the 'unification':")
    print("   * gravity + the DARK sector (MOND/a0) emerge from ONE principle (horizon")
    print("     thermodynamics) -- a genuine unification of gravity+inertia+dark.")
    print("   * the SM is the MATTER content of the compactification (orbifold E6->SM)")
    print("     -- attached, not derived. The constants stay inputs/moduli.")
    print("   * the deep open link: does the SAME compactification that gives the SM")
    print("     also fix the horizon coupling Z? That is the geometric pin (Gate 3a).")
    print("  STATUS: OPEN. Best honest case = 'one consistent action' (coexistence),")
    print("  NOT 'the SM derived from geometry'. That distinction is the whole ballgame.\n")


def main():
    print("#" * 78)
    print("# PATH TO UNIFICATION FROM SCALING-MOND GEOMETRY (de Sitter horizon)")
    print("#" * 78)
    print("  Reframe: geometry = the de Sitter HORIZON (emergent gravity), not the")
    print("  Z^2=32pi/3 numerology. The organizing principle: gravity+inertia emerge")
    print("  from horizon thermodynamics; the finite cosmic horizon adds a0 ~ cH(z).\n")
    gate1()
    gate2()
    gate3()
    gate4()
    print("=" * 78)
    print("VERDICT -- what kind of unified theory this honestly is")
    print("=" * 78)
    print("  IT IS: a member of the emergent/entropic-gravity family (Jacobson,")
    print("  Padmanabhan, Verlinde, Milgrom-vacuum), with the SM attached as matter")
    print("  via the orbifold, and a0(z)=cH(z)/Z as a FALSIFIABLE signature. Live,")
    print("  ambitious, near-term-testable physics.")
    print("  IT IS NOT: a theory that derives the constants from Z^2 (numerology -")
    print("  dead), nor a cosmic-topology claim (excluded). Do not sell it as a TOE.")
    print()
    print("  ORDER OF OPERATIONS (do the cheap/decisive ones first):")
    print("   1. GATE 1 -- collect z>10 BTFR data. If it fails, stop. (months-years)")
    print("   2. GATE 2 -- run the scaling-a0 CMB Boltzmann fit. (a real calculation)")
    print("   3. GATE 3 -- accept a0=cH/2pi OR attempt the horizon-volume derivation.")
    print("   4. GATE 4 -- write the SM<->horizon coupling, if 1-3 survive.")
    print("  The program is only as alive as GATE 1. That is the honest dependency,")
    print("  and it is exactly why this is science and the numerology was not.")


if __name__ == "__main__":
    main()
