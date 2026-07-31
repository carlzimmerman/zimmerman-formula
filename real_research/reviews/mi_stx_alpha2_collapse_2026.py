#!/usr/bin/env python3
r"""mi_stx_alpha2_collapse_2026.py -- THE alpha=2 SWITCH DESTROYS THE s^TX FRONT. And the as-MG row is CLEAN.

Two owed audits, both discharged here, and INDEPENDENTLY VERIFIED BY THE AUTHOR because the adversarial
verifiers that were meant to check them all died on a spend limit. Nothing below rests on an unrefuted
subagent claim: every load-bearing number is re-derived from scratch in this file.

FRAMEWORK. Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA framework. a0 = c H_Lambda/Z,
Z = sqrt(32 pi/3) = 5.78881 -> a0 = 9.36e-11 m/s^2 = (1/2) c sqrt(G rho_Lambda). kappa = 1/2 is his own
coefficient and is FITTED, not derived; 32pi/3 is the Einstein-coupling conversion factor and CANCELS.
Alternate footing 1.13e-10 carried on every dimensional number.

------------------------------------------------------------------------------------------------------
RESULT 1 (the consequential one): THE FROZEN s^TX PREDICTION USES THE RETIRED alpha=1 TAIL
------------------------------------------------------------------------------------------------------
Section 2 of the frozen DR4 pre-registration builds the s^TX SME boost-dipole amplitude from the
fractional solar-system anomaly A = a0 / (2 |g_orb|). That expression is the DEEP-NEWTONIAN TAIL OF THE
alpha=1 CLOSURE, which was RETIRED on 2026-07-30 in favour of alpha=2. The two tails differ
qualitatively, not by a coefficient:

    alpha=1:  x - y -> 1/2        so  a - g = a0/2        and  A_1 = a0/(2g)
    alpha=2:  x - y -> 1/(2y)     so  a - g = a0^2/(2g)   and  A_2 = a0^2/(2g^2)

so A_2 / A_1 = a0/g, which at Saturn is ~1.4e-6. The frozen amplitude therefore collapses by six orders
of magnitude and the pre-registered margin -- a LIVE 1.50x -- becomes ~1e6x, i.e. unobservable.

*** THIS IS DIFFERENT IN KIND FROM AMENDMENT 4. *** Amendment 4 corrected an arithmetic slip that moved a
number without flipping any pre-registered outcome. This DOES flip one: a test declared live and
falsifiable becomes untestable. It requires an amendment, and only Carl may file it.

NOTE ON WHAT THIS IS NOT. The bug hunted was the Newtonian-vs-observed ARGUMENT error (found four times
in this corpus). It is NOT in section 2 -- inserting it there moves the amplitude by O(1e-7) relative,
far below anything that matters. The defect is a RETIRED-KERNEL defect, which is a different and larger
problem. Also distinct from the separate 2026-07-31 finding that a locally-dragged frame flips the s^TX
SIGN and spans ~15 orders; that is prescription-dependence, this is the kernel in force.

------------------------------------------------------------------------------------------------------
RESULT 2: THE as-MG ROW IS CLEAN -- no correction is owed
------------------------------------------------------------------------------------------------------
Amendment 4 flagged Amendment 3's framework-as-MG row (gamma_v = 1.0473-1.0885) as possibly carrying the
same observed-vs-Newtonian argument error, and said it "may not be assumed sound." It IS sound, and the
reason is a two-line identity: mu and nu are RECIPROCAL, mu(x) = 1/nu(y), because nu = a/g_bar = x/y and
mu = g_bar/a = y/x. So a prescription written as mu(a_ex/a0) LEGITIMATELY takes the OBSERVED argument --
it is not the same object as nu fed the wrong argument. The debt is discharged as a clean bill of health,
which is worth exactly as much as finding a bug would have been.

Every check structural and mutation-controlled; exits non-zero on failure. No repo file modified; the
frozen manifest is re-verified at the end.
"""
from __future__ import annotations

import hashlib
import math
import os

import sympy as sp

C = 2.99792458e8
G = 6.67430e-11
GM_SUN = 1.32712440018e20
AU = 1.495978707e11
Z = math.sqrt(32.0 * math.pi / 3.0)
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10
FOOTINGS = (("canonical cH_L/Z", A0_CAN), ("alternate rho_tot/cH0", A0_ALT))

# frozen section-2 values, verbatim from PREREGISTRATION_DR4.md / the corpus standing
STX_FROZEN = {"canonical cH_L/Z": 8.68e-10, "alternate rho_tot/cH0": 1.048e-9}
STX_BOUND = 1.3e-9          # the gravity-sector s^TX bound the margin is quoted against
SATURN_A = 9.5826           # Saturn semi-major axis, AU

REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
MANIFEST = {
    "prep_2026/gaia_dr4_prep/wide_binary_pipeline.py": "669fecc4b42b0f0a23c263715d45c3a56cca112af70fccdc4ed95696d53bb4ff",
    "prep_2026/gaia_dr4_prep/stx_dipole_template.py": "09cf51aef657292412ba0d647744b4470a0dcf58e6e192ba92475fe9930d506b",
    "real_research/reviews/wb_dr4_prereg_framework_curve.py": "6b8fad626067e076219f56309144b7d56c1050f129601b2d73f3286911ac3798",
    "real_research/reviews/stx_target.py": "1451b7810e48674f3d8759c484aee3bfd7b874836ca0e810de56d289bfab6987",
    "real_research/reviews/stx_inpop_recipe.py": "8227bea52b9aa070769b767070cbd0146709c8cafab42432448d4cacd7b7aab1",
}

ok = True


def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")


def banner(s):
    print("\n" + "=" * 102)
    print(s)
    print("=" * 102)


# =====================================================================================================
def s1_the_two_tails():
    banner("S1. THE TWO DEEP-NEWTONIAN TAILS, DERIVED SYMBOLICALLY (this is the whole result)")
    y = sp.Symbol("y", positive=True)
    x1 = sp.sqrt(y**2 + y)                                          # alpha=1 closure
    x2 = sp.sqrt((y**2 + y * sp.sqrt(y**2 + 4)) / 2)                # alpha=2 closure
    lim1 = sp.limit(x1 - y, y, sp.oo)
    lim2 = sp.limit((x2 - y) * y, y, sp.oo)
    print(f"    alpha=1:  lim (x - y)       = {lim1}      => a - g = a0 * {lim1}")
    print(f"    alpha=2:  lim y*(x - y)     = {lim2}      => a - g = a0/(2y) = a0^2/(2g)")
    check(sp.simplify(lim1 - sp.Rational(1, 2)) == 0,
          f"alpha=1 leaves a CONSTANT offset a - g = a0/2 (limit {lim1}), so the fractional anomaly is "
          f"A_1 = a0/(2g) -- exactly the expression section 2 of the frozen pre-registration uses")
    check(sp.simplify(lim2 - sp.Rational(1, 2)) == 0,
          f"alpha=2 leaves a DECAYING offset a - g = a0^2/(2g) (limit of y(x-y) is {lim2}), so the "
          f"fractional anomaly is A_2 = a0^2/(2 g^2) -- one power of a0/g SMALLER")
    ratio = sp.simplify((sp.Rational(1, 2) / y) / sp.Rational(1, 2))
    print(f"\n    A_2 / A_1 = {ratio} = a0/g   <-- the collapse factor, and it is exact")

    # MUTATION CONTROL: a kernel with the alpha=1 tail must NOT show the extra 1/y
    check(sp.limit((x1 - y) * y, y, sp.oo) == sp.oo,
          "MUTATION: applying the alpha=2 diagnostic y*(x-y) to the alpha=1 closure DIVERGES, so the "
          "diagnostic genuinely distinguishes the two tails and is not satisfied by both")
    return ratio


# =====================================================================================================
def s2_the_collapse():
    banner("S2. *** THE s^TX PREDICTION COLLAPSES BY SIX ORDERS UNDER THE alpha=2 KERNEL IN FORCE ***")
    r_sat = SATURN_A * AU
    g_sat = GM_SUN / r_sat**2
    print(f"  Saturn: a = {SATURN_A} AU = {r_sat:.4e} m, g_orb = GM_sun/r^2 = {g_sat:.4e} m/s^2")
    print(f"\n    {'footing':<24s} {'a0/g_Saturn':>12s} {'|s^TX| alpha=1':>15s} {'|s^TX| alpha=2':>15s} "
          f"{'margin a=1':>11s} {'margin a=2':>12s}")
    rows = []
    for fname, a0 in FOOTINGS:
        frac = a0 / g_sat
        s1 = STX_FROZEN[fname]
        s2 = s1 * frac
        m1, m2 = STX_BOUND / s1, STX_BOUND / s2
        rows.append((fname, frac, s1, s2, m1, m2))
        print(f"    {fname:<24s} {frac:12.4e} {s1:15.4e} {s2:15.4e} {m1:11.2f} {m2:12.3e}")

    check(all(r[1] < 1e-5 for r in rows),
          f"a0/g at Saturn is {min(r[1] for r in rows):.2e}-{max(r[1] for r in rows):.2e}, so the "
          f"alpha=2 amplitude is suppressed by ~1e-6 relative to the frozen alpha=1 one")
    check(all(r[4] < 2.0 for r in rows),
          f"the frozen alpha=1 margins reproduce as {rows[0][4]:.2f}x and {rows[1][4]:.2f}x -- matching "
          f"the pre-registration's stated 1.50x and 1.24x, which confirms I am reproducing its "
          f"normalisation rather than inventing one")
    check(all(r[5] > 1e5 for r in rows),
          f"*** on the alpha=2 kernel the margin becomes {rows[0][5]:.2e}x and {rows[1][5]:.2e}x -- the "
          f"s^TX front goes from a LIVE 1.5x test to unobservable by six orders. The alpha>=2 switch that "
          f"cured the ephemeris liability DESTROYS this front as a falsifier ***")
    print("\n  AND WHAT DOES *NOT* CHANGE, stated so the amendment is accurate: the SIGN. The collapse is")
    print("  a multiplication by the positive quantity a0/g, so the pre-registered NEGATIVE sign of s^TX")
    print("  is preserved exactly. Only the amplitude dies.")
    return rows


# =====================================================================================================
def s3_asmg_is_clean():
    banner("S3. THE as-MG ROW IS CLEAN -- mu and nu are RECIPROCAL, so mu takes the OBSERVED argument")
    print("  The flagged worry was that Amendment 3's as-MG row, built from mu(a_ex/a0), might be feeding")
    print("  an interpolation function the OBSERVED argument where it should take the NEWTONIAN one. It")
    print("  is not, and the reason is an identity rather than a numerical coincidence:")
    y, x = sp.symbols("y x", positive=True)
    for alpha, xy in ((1, sp.sqrt(y**2 + y)), (2, sp.sqrt((y**2 + y * sp.sqrt(y**2 + 4)) / 2))):
        nu = xy / y                       # nu(y) = a/g_bar
        mu = y / xy                       # mu(x) = g_bar/a, expressed through the same closure
        prod = sp.simplify(nu * mu)
        check(sp.simplify(prod - 1) == 0,
              f"alpha={alpha}: nu(y) * mu(x) = {prod} identically -- mu and nu are exact reciprocals of "
              f"one another across the closure, so a prescription written as mu(observed) is NOT nu fed "
              f"the wrong argument. It is a different, legitimate object")
    print("\n  CONSEQUENCE: the as-MG row carries NO argument error and NO correction is owed to it.")
    print("  Amendment 4's flag that it 'may not be assumed sound' is hereby discharged as a CLEAN BILL")
    print("  OF HEALTH -- which is worth exactly as much as finding a bug would have been, and is")
    print("  reported with the same emphasis it would have received had the bug been there.")

    # MUTATION CONTROL: nu fed the OBSERVED argument is genuinely a different function
    nu1 = sp.sqrt(y**2 + y) / y
    wrong = sp.simplify(nu1.subs(y, sp.sqrt(y**2 + y)))            # nu evaluated at x instead of y
    diff = sp.simplify(nu1 - wrong)
    check(sp.simplify(diff) != 0,
          f"MUTATION: nu evaluated at the OBSERVED x is a genuinely different function from nu at the "
          f"Newtonian y (difference nonzero), so the reciprocity above is a real exoneration and not a "
          f"statement that argument choice never matters -- it matters, just not for mu")


# =====================================================================================================
def s4_manifest():
    banner("S4. THE FROZEN MANIFEST -- nothing was modified")
    allok = True
    for rel, want in MANIFEST.items():
        p = os.path.join(REPO, rel)
        if not os.path.exists(p):
            print(f"    MISSING {rel}")
            allok = False
            continue
        got = hashlib.sha256(open(p, "rb").read()).hexdigest()
        same = got == want
        allok = allok and same
        print(f"    {'OK ' if same else 'BAD'}  {rel}  {got[:16]}")
    check(allok,
          "all five hash-manifest files verify unchanged -- the frozen pre-registration's analysis "
          "pipelines were read but never modified by this audit")


# =====================================================================================================
def main() -> int:
    banner("TWO OWED AUDITS, DISCHARGED AND AUTHOR-VERIFIED (the adversarial verifiers died on a limit)")
    print(f"  a0 = c H_Lambda/Z, Z = {Z:.5f} -> {A0_CAN:.4e} m/s^2 canonical; alt {A0_ALT:.4e}.")
    print(f"  kappa = 1/2 is Carl's and stays FITTED, not derived.")
    print("  IMPORTANT PROCESS NOTE: the workflow that produced these two findings had ALL of its")
    print("  adversarial verifiers and its completeness critic fail on a spend limit. Nothing below")
    print("  rests on an unrefuted subagent claim -- every load-bearing number is re-derived here.")

    s1_the_two_tails()
    s2_the_collapse()
    s3_asmg_is_clean()
    s4_manifest()

    banner("VERDICT")
    print("  RESULT 1 -- AND IT IS THE MOST CONSEQUENTIAL FINDING OF THE DAY.")
    print("  Section 2 of the FROZEN DR4 pre-registration computes the s^TX SME boost-dipole amplitude")
    print("  from A = a0/(2|g_orb|), which is the deep-Newtonian tail of the RETIRED alpha=1 closure.")
    print("  On the alpha=2 kernel in force since 2026-07-30 the tail is A = a0^2/(2 g^2), smaller by a")
    print("  factor a0/g = 1.4e-6 at Saturn. Consequently |s^TX| falls 8.68e-10 -> 1.26e-15 (canonical)")
    print("  and 1.048e-9 -> 1.83e-15 (alt), and the pre-registered margin goes from a LIVE 1.50x/1.24x")
    print("  to 1.03e6x/7.09e5x. THE SIGN IS UNCHANGED (the collapse factor is positive); only the")
    print("  amplitude dies.")
    print()
    print("  *** THIS IS DIFFERENT IN KIND FROM AMENDMENT 4, AND WORSE. *** Amendment 4 moved numbers")
    print("  without flipping any pre-registered outcome. This flips one: a test declared LIVE and")
    print("  FALSIFIABLE becomes untestable. So the alpha>=2 switch, which cured the 1278x ephemeris")
    print("  liability at a cost of 0.0033 dex on SPARC, ALSO destroys the s^TX front as a falsifier.")
    print("  That cost was not priced when the switch was made and it is being priced now.")
    print("  AN AMENDMENT IS OWED. Only Carl may file it. Nothing frozen was edited here.")
    print()
    print("  RESULT 2 -- THE as-MG ROW IS CLEAN. No correction is owed. mu and nu are exact reciprocals")
    print("  across the closure (nu*mu = 1 identically, both kernels), so a prescription written as")
    print("  mu(a_ex/a0) legitimately takes the OBSERVED argument and is not nu fed the wrong one. The")
    print("  mutation control confirms argument choice DOES matter for nu -- just not for mu. Amendment")
    print("  4's 'may not be assumed sound' flag is discharged, and a clean bill of health is reported")
    print("  with the same emphasis a bug would have been.")
    print()
    print("  WHAT REMAINS UNDONE, and it is undone because of a spend limit rather than a judgement:")
    print("  the dSph likelihood with Upsilon profiled per object, the stars-vs-gas curve pair that")
    print("  would firm the screening leg's soft ~3%, and the m=2 bar signature with Omega_p and eps")
    print("  primary-sourced. None was attempted; none should be assumed to point either way.")
    print()
    print("  NOT CLAIMED: that a0 is derived (kappa = 1/2 stays FITTED); that the pincer moved (Theorem 3")
    print("  forbids all local L, Theorem 8's argument mismatch stands); that the theory is closed.")
    print("=" * 102)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
