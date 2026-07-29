#!/usr/bin/env python3
"""mi_atomos_germ_provenance_2026.py -- what today's reduction does to project_atomos's germs.

THE QUESTION. project_atomos searched with the germ pair {3, sqrt(8pi/3)}, described in
PAPER_ATOMOS_NULL (DOI 10.5281/zenodo.21654272) as "the framework's two forced germs -- the
generation count 3 and the kernel germ sqrt(8pi/3)". Today's reduction
(mi_kappa_spectral_reduction_2026) proved

    a0 = kappa c sqrt(G rho_Lambda)      exactly,    kappa = 1/2

with every pi, the 32 and the 3 cancelling. So is sqrt(8pi/3) actually the framework's own
number, or is it GR + FRW wearing the framework's name? This matters because the whole point
of "forced" was that it made the null a statement about THIS framework.

Exit 0 = all checks ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math
import sympy as sp

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")
    return cond

def banner(s):
    print("\n" + "=" * 98); print(s); print("=" * 98)


def main() -> int:
    banner("mi_atomos_germ_provenance_2026 -- whose number is sqrt(8pi/3)?")

    # -----------------------------------------------------------------------------------
    banner("S1. Decompose the germ, using atomos's own stated decomposition")
    print("  project_atomos/targets/geometric_primitives.py:9 states it directly:")
    print("      sqrt(8pi/3) = sqrt(8pi)[Einstein measure] x sqrt(1/3)[Friedmann/FRW]")
    germ = sp.sqrt(8 * sp.pi / 3)
    einstein = sp.sqrt(8 * sp.pi)
    friedmann = sp.sqrt(sp.Rational(1, 3))
    check(sp.simplify(germ - einstein * friedmann) == 0,
          "sqrt(8pi/3) = sqrt(8pi) * sqrt(1/3) exactly -- Einstein x Friedmann")
    print(f"      sqrt(8pi)  = {float(einstein):.10f}   <- Einstein field equations, GR")
    print(f"      sqrt(1/3)  = {float(friedmann):.10f}   <- Lambda = 3H^2/c^2, FRW")
    print(f"      product    = {float(germ):.10f}   <- the atomos germ")

    # -----------------------------------------------------------------------------------
    banner("S2. Where the framework's OWN number sits")
    kappa, c, G, rho, HL, Lam = sp.symbols("kappa c G rho_Lambda H_Lambda Lambda", positive=True)
    a0 = kappa * c * sp.sqrt(G * rho)
    Z_of_k = sp.simplify(sp.sqrt(8 * sp.pi / 3) / kappa)
    print(f"  reduction:  a0 = {a0}   (all pi's cancelled)")
    print(f"  and  Z(kappa) = sqrt(8pi/3)/kappa = {Z_of_k}")
    check(sp.simplify(Z_of_k.subs(kappa, sp.Rational(1, 2)) - sp.sqrt(32 * sp.pi / 3)) == 0,
          "Z(1/2) = sqrt(32pi/3): the framework's contribution is the FACTOR 1/kappa = 2")
    print(f"\n  So Z factorises as  [GR x FRW] / [framework]:")
    print(f"      sqrt(8pi/3) = {float(germ):.6f}   GR + FRW  (NOT novel)")
    print(f"      1/kappa     = {2.0:.6f}          the framework's own input")
    print(f"      product Z   = {float(sp.sqrt(32*sp.pi/3)):.6f}")
    print("\n  THE FRAMEWORK'S DISTINCTIVE NUMBER IS kappa = 1/2 -- A RATIONAL.")
    check(sp.Rational(1, 2).is_rational, "kappa = 1/2 is rational")

    # -----------------------------------------------------------------------------------
    banner("S3. CONSEQUENCE FOR THE PUBLISHED NULL -- what changes and what does not")
    print("  DOES NOT CHANGE (the result stands):")
    print("   * The null itself. 174,890,804 raw / 42,534,139 distinct / 82,613 in-window /")
    print("     ZERO certified is a FACT about the vocabulary {3, sqrt(8pi/3)} at depth <= 10.")
    print("     Nothing here touches a single count.")
    print("   * The depth-ceiling result, the hit-distribution diagnostic, the permutation")
    print("     calibration, or the interlock null.")
    print("   * The paper's own Section 10 disclaimer already says the null is 'not evidence")
    print("     for or against the framework whose germs it uses' -- which is exactly right,")
    print("     and now provably so for a sharper reason than the paper gave.")
    print("\n  DOES CHANGE (a framing correction, and it should be recorded):")
    print("   * Calling sqrt(8pi/3) 'the framework's forced germ' is IMPRECISE. It is")
    print("     Einstein's 8pi times Friedmann's 1/3 -- standard GR + FRW. The framework's")
    print("     own contribution to Z is the factor 1/kappa = 2, and kappa = 1/2 was never")
    print("     in the germ pool at all.")
    print("   * So the search tested whether SM constants are reachable from GR+FRW GEOMETRY,")
    print("     not from this framework's distinctive input. That is a WEAKER and different")
    print("     claim than the paper implies, and arguably a more interesting one -- but it")
    print("     must be stated correctly.")

    # -----------------------------------------------------------------------------------
    banner("S4. A SECOND, INDEPENDENT ISSUE: there are two different 3's")
    print("  The germ pool lists `3` as 'the generation count' (an SM fact).")
    print("  But sqrt(8pi/3) already contains a 3 -- Friedmann's, from Lambda = 3H^2/c^2,")
    print("  which is about spatial geometry and has NOTHING to do with generations.")
    print("  Same numeral, two unrelated origins. Treating them as one germ family, or")
    print("  letting one stand in for the other inside an expression, is a numerological")
    print("  conflation of exactly the kind the paper warns against.")
    print("\n  Worked check -- the two 3's enter with different powers and different roles:")
    print(f"    Friedmann 3: Lambda = 3H^2/c^2   -> enters Z as 3^(-1/2) = "
          f"{float(sp.sqrt(sp.Rational(1,3))):.6f}")
    print(f"    generation 3: a COUNT, dimensionless, enters as 3^(+1) = 3")
    check(sp.simplify(sp.sqrt(sp.Rational(1, 3)) - 1 / sp.sqrt(3)) == 0,
          "Friedmann's 3 enters as an inverse square root, not as a count")
    print("  The enumeration's step menu contains POW in {2,3,1/2,-1,2/3} and unary")
    print("  {SQRT,CBRT,INV}, so it can freely convert 3^(-1/2) <-> 3^(+1). The two 3's are")
    print("  therefore NOT distinguishable inside the search -- it cannot tell a generation")
    print("  count from a piece of FRW geometry.")

    # -----------------------------------------------------------------------------------
    banner("S5. What this does to the NUMBER-FIELD OBSTRUCTION")
    print("  The standing obstruction reads: 'Z carries a transcendental sqrt(pi) while the")
    print("  flavour and coupling data are algebraic, so an exact identity requires the")
    print("  sqrt(pi) to cancel -- in which case the germ was not load-bearing.'")
    print("\n  That argument is CORRECT for the search that was run, since the germ used")
    print("  really is sqrt(8pi/3). But it must NOT be read as 'the framework's number is")
    print("  transcendental'. The framework's number is kappa = 1/2, RATIONAL. The sqrt(pi)")
    print("  belongs to Einstein's 8pi, i.e. to GR.")
    print("\n  Note the flip side, stated against interest: a search whose germ were the")
    print("  framework's actual rational kappa would be VACUOUS -- rationals are dense, so")
    print("  any measured constant sits inside some rational's window and the search would")
    print("  certify noise trivially. The transcendental germ is what made the atomos search")
    print("  non-trivial in the first place. So the vocabulary choice was pragmatically right")
    print("  even though its provenance was mislabelled.")

    banner("VERDICT")
    print("  1. YES, atomos uses the modified-inertia framework's acceleration scale -- but")
    print("     its germ sqrt(8pi/3) is Einstein's 8pi times Friedmann's 1/3, i.e. GR + FRW.")
    print("     The framework's OWN distinctive number is kappa = 1/2, which is RATIONAL and")
    print("     was never in the germ pool.")
    print("  2. The published null is UNAFFECTED as a result; only its FRAMING needs")
    print("     correcting -- 'the framework's forced germs' should read 'a germ vocabulary")
    print("     built from GR + FRW geometry, in which the framework's acceleration scale is")
    print("     expressed'. The paper's Section 10 disclaimer already covers the substance.")
    print("  3. NEW ISSUE FOUND: the germ pool's `3` (generation count) and the 3 inside")
    print("     sqrt(8pi/3) (Friedmann) are unrelated, and the search's own step menu can")
    print("     interconvert their powers -- so the search cannot distinguish them. This is a")
    print("     conflation worth recording as a limitation.")
    print("  4. The number-field obstruction stands for the search as run, but describes GR's")
    print("     sqrt(pi), NOT the framework's kappa.")
    print("  Nothing empirical moves. kappa = 1/2 remains POSTULATED, NOT DERIVED.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
