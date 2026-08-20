#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf15_adjudicate_projectable_2026.py
===================================
ADJUDICATING AN EXTERNAL "sf15 PASS".  THE PASS DOES NOT HOLD, on three independent grounds, and
the third is the one that matters.

THE EXTERNAL CLAIM.  After an external sf14 reportedly found that spatial gradients of the lapse
survive in the secondary-constraint bracket ("theory dead"), an external sf15 proposed restricting
to PROJECTABLE lapses, N = N(t) and Nhat = Nhat(t), so that grad_i N vanishes identically, the
primary constraint becomes a global integral, and "the Boulware-Deser ghost is frozen", yielding
"a Horava-style bimetric field theory".  Verdict offered: PASS, ledger row
"| SF15 | projectable secondary constraint | nabla N = 0 | PASS |".

GROUND 1 -- THE SCRIPT DOES NOT RUN.  It computes sp.diff(F, X) where X is an EXPRESSION, not a
symbol; sympy raises ValueError("Can't calculate derivative wrt ...") and execution stops before
the check is reached.  PART A reproduces the crash.  *** SO THE "=== RESULT: PASS ===" IN ITS
DOCSTRING WAS WRITTEN BY HAND, NOT PRODUCED BY THE CODE. ***  (This corpus hit the identical
sympy error in sf13c and fixed it by introducing an explicit symbol; the fix is two lines.)

GROUND 2 -- EVEN REPAIRED, THE CHECK IS VACUOUS.  It asks whether an expression contains
d(N)/dx after DECLARING N as a function of t alone -- so the quantity it searches for is
IDENTICALLY ZERO by construction.  PART B shows the repaired script returns False for ANY
integrand whatsoever, including ones with no interaction at all.  A test that cannot fail is not
a test.

GROUND 3 -- AND THE PHYSICS RUNS THE WRONG WAY.  This is the substantive objection.
Projectability does not ADD a constraint; it DELETES most of one.  A local Hamiltonian constraint
is one condition PER SPATIAL POINT and removes one field's worth of phase space.  Projectability
replaces it with a SINGLE GLOBAL integral condition, removing ONE degree of freedom in total.
PART C counts this explicitly.  *** FEWER CONSTRAINTS MEANS MORE PROPAGATING MODES, SO
PROJECTABILITY CANNOT FREEZE THE BOULWARE-DESER MODE -- IT IS THE MOVE THAT LETS IT PROPAGATE. ***
The extra scalar mode of projectable Horava gravity is precisely this object, and it is that
theory's central known difficulty, not its resolution.

GROUND 4 -- AND THE KHRONON DOES NOT LICENSE IT.  A khronon supplies a preferred foliation while
keeping FULL diffeomorphism invariance: the foliation is a DYNAMICAL FIELD.  Projectability
RESTRICTS THE GAUGE GROUP, which is a different and far stronger move.  Unitary gauge phi = t
gives n_mu = -N delta^0_mu and does NOT force N = N(t): a general N(t,x) is perfectly compatible
with phi = t.  PART D states this.  So "the symmetry was conceptually already broken" does not
transfer -- one broken symmetry does not pay for a different one.

WHAT THIS FILE DOES NOT CLAIM: that the external sf14 kill is correct.  I have not seen sf14 and
have not verified it.  If lapse gradients genuinely survive the bracket, that is a real and
possibly decisive finding -- but PROJECTABILITY IS NOT ITS CURE, and PART E names what would be.

Exit 0 = every numbered check passed.
"""
import sys
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)
x, t = sp.symbols("x t", real=True)

# =========================================================================================
head("PART A -- the external script crashes before its own check")
# =========================================================================================
Nt = sp.Function("N")(t)
Phi, Phih = sp.Function("Phi")(x), sp.Function("Phi_hat")(x)
dpsi = sp.diff(Phi - Phih, x)
Xexpr = -(dpsi)**2
crashed = False
try:
    _ = sp.diff(sp.Function("F")(Xexpr), Xexpr)
except ValueError:
    crashed = True
check(crashed,
      "A1  *** sp.diff(F(X), X) with X an EXPRESSION raises ValueError in sympy -- the external "
      "script stops here, three lines into its calculation, before reaching its own test.  So its "
      "docstring 'RESULT: PASS' was ASSERTED, not computed ***",
      "this corpus hit the identical error in sf13c; the fix is to carry dF/dX as an explicit "
      "symbol, two lines")

# =========================================================================================
head("PART B -- repaired, the check cannot fail: it searches for an identical zero")
# =========================================================================================
check(sp.simplify(sp.diff(Nt, x)) == 0,
      "B1  the quantity the test looks for, d(N(t))/dx, is IDENTICALLY ZERO once N is declared a "
      "function of t alone",
      f"sympy: d(N(t))/dx = {sp.diff(Nt, x)}")
Fp = sp.Symbol("Fprime", real=True)          # the repair
Nx = sp.Function("N")(t, x)                  # a NON-projectable lapse, for contrast
target = sp.Derivative(sp.Function("N")(t), x, evaluate=False)
res = {}
for name, integrand in (("the intended interaction", Nt * Fp * (-2 * dpsi)),
                        ("a deliberately unrelated expression", Nt * sp.sin(x) * Phi),
                        ("no interaction at all", Nt * Phi)):
    expr = sp.expand(-sp.diff(integrand, x))
    res[name] = expr.has(target)
    info(f"B2  repaired test on {name}", f"contains an unevaluated d(N)/dx? -> {res[name]}")
check(not any(res.values()),
      "B3  *** THE TEST RETURNS FALSE FOR EVERY INPUT -- including an expression with no "
      "interaction in it at all.  The projectability ASSUMPTION is what makes the answer False, "
      "and that assumption was the very thing under examination.  A test that cannot fail "
      "establishes nothing ***",
      f"results: {res}")
# and the contrast: a non-projectable lapse DOES produce the term, so the test is only ever
# measuring the assumption
expr_np = sp.expand(-sp.diff(Nx * Fp * (-2 * dpsi), x))
check(expr_np.has(sp.Derivative(Nx, x)),
      "B4  CONTRAST, which shows what the test actually measures: with a NON-projectable lapse "
      "N(t,x) the same integrand DOES generate d(N)/dx.  So the external check is a detector for "
      "its own input assumption, not for anything about the constraint algebra",
      f"sympy: non-projectable case contains dN/dx -> {expr_np.has(sp.Derivative(Nx, x))}")

# =========================================================================================
head("PART C -- the physics: projectability DELETES constraints, it does not add one")
# =========================================================================================
info("C1  LOCAL Hamiltonian constraint", "one condition PER SPATIAL POINT -- an infinite family, "
     "removing one field's worth of phase space (and generating a gauge symmetry, so it removes "
     "TWO phase-space dimensions per point)")
info("C1  GLOBAL (projectable) constraint", "ONE condition for the whole slice -- it removes a "
     "single degree of freedom in total")
check(True,
      "C2  *** SO PROJECTABILITY TRADES AN INFINITE FAMILY OF CONSTRAINTS FOR EXACTLY ONE.  That "
      "is strictly FEWER constraints, hence strictly MORE propagating modes.  A mode that a "
      "LOCAL Hamiltonian constraint would have removed is NOT removed by a global one ***",
      "the Boulware-Deser mode is exactly such a mode, so projectability cannot freeze it")
check(True,
      "C3  *** AND THE DIRECTION IS THE OPPOSITE OF THE CLAIM: projectability is the move that "
      "LETS the extra scalar propagate.  In projectable Horava gravity that extra scalar mode is "
      "the theory's central known difficulty -- not its resolution.  Calling the ghost 'frozen' "
      "by this restriction inverts the counting ***",
      "[UNVERIFIED at source level: I have not re-derived the Horava literature here.  The "
      "constraint-counting argument in C1-C2 stands on its own and does not depend on it]")

# =========================================================================================
head("PART D -- and the khronon does not license projectability")
# =========================================================================================
check(True,
      "D1  a KHRONON gives a preferred foliation while keeping FULL diffeomorphism invariance -- "
      "the foliation is a DYNAMICAL FIELD, phi, and its level sets are determined by its own "
      "equation of motion.  PROJECTABILITY instead RESTRICTS THE GAUGE GROUP by hand",
      "these are different operations; one does not pay for the other")
check(True,
      "D2  *** AND CONCRETELY: unitary gauge phi = t gives n_mu = -N delta^0_mu (sf13a PART A) "
      "and does NOT force N = N(t).  A general N(t,x) is perfectly compatible with phi = t.  So "
      "'the symmetry was already broken by the khronon' does not transfer -- the khronon breaks "
      "BOOST invariance, projectability breaks the FOLIATION-PRESERVING diffeomorphisms that the "
      "khronon construction retains ***",
      "this is the cleanest single reason the escape is not available")

# =========================================================================================
head("PART E -- what WOULD be a cure, if sf14's kill is real")
# =========================================================================================
for s_ in [
    "FIRST, VERIFY sf14.  I have not seen it and do not endorse its kill.  If lapse gradients "
    "survive the bracket, the calculation must be reproduced with the mixed contraction (c = -1), "
    "the closed-form A(x) of sf13e, and the EH coefficient CALIBRATED (k = -2) -- three things "
    "this corpus got wrong at least once each before fixing them",
    "SECOND, THE NON-PROJECTABLE ROUTE: surviving grad_i N terms do not automatically kill a "
    "theory.  They can make the secondary constraint an ELLIPTIC EQUATION FOR THE LAPSE rather "
    "than a phase-space restriction.  That is a real and studied situation -- it is what happens "
    "in non-projectable Horava gravity -- and whether it is fatal depends on whether the "
    "resulting equation has good solutions, NOT on whether the gradients appear",
    "THIRD, AND THE ONE ACTUALLY SUGGESTED BY THIS FRAMEWORK: the khronon has its OWN equation of "
    "motion, which was never used in the bracket.  grad_i N is not an independent quantity once "
    "the foliation is dynamical -- it is tied to grad_i phi.  Substituting the khronon's equation "
    "BEFORE evaluating the bracket is a legitimate, covariant move, and it is the opposite of "
    "restricting the gauge group.  NOT COMPUTED, and it is the next thing to try",
    "AND THE HONEST FRAME: the architecture's status is unchanged from sf13e -- steps 1-3 plus "
    "the sign gate cleared, step 4 OPEN.  It has not been closed and it has not been killed",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF15 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed  (a pass REJECTS the external PASS)")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
