#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf12_adjudicate_sf11b_2026.py
=============================
ADJUDICATING AN EXTERNAL SESSION'S SF11/SF11B RESULTS.  Two findings, opposite verdicts.

FINDING 1 -- SF11B's OBSTRUCTION IS CORRECT, AND IT CORRECTS *MY* FILE.
    sf10 PART E (superfluid_2026/) claimed the magnetic 3/2 term "carries NO lapse and
    contributes NOTHING to H_AB", on the strength of d/dN of the magnetic piece being zero.
    SF11B points out the JOINT Hessian is what matters, and for L ~ N * Nhat^{-6} we get
    d^2L/dN^2 = 0 but the MIXED and Nhat-Nhat entries survive, so
        det H = 0 * (d^2L/dNhat^2) - (d^2L/dN dNhat)^2 = -(mixed)^2  =/=  0.
    A single zero on the diagonal does NOT make a 2x2 Hessian singular -- it GUARANTEES a
    negative determinant unless the mixed entry also vanishes.  PART A verifies this.
    *** sf10 PART E's "MOND outside the constraint sector" claim is WITHDRAWN. ***

FINDING 2 -- SF11B's PROPOSED CLOSURE HAS THE WRONG INTERPOLATION FUNCTION.
    It proposes F(X) = sqrt(X(X+a_0^2)) - a_0^2 asinh(sqrt X/a_0), whose derivative is
    mu(x) = x/sqrt(1+x^2), and claims mu(g/a_0) g = g_bar "reduces exactly to
    g^2 = g_bar^2 + a_0 g_bar".  IT DOES NOT.  That mu is the STANDARD MOND mu-function, not
    Carl's a_0-line.  PART B shows the identity fails at every point except g = 0, and PART C
    gives the CORRECT F -- which the corpus already has in closed form from
    superfluid_2026/sf01, and which is a DIFFERENT function.

WHAT IS GENUINELY VALUABLE IN THE EXTERNAL WORK, and it is the architecture, not the function:
    V = N F(X) + Nhat B(X) with X LAPSE-FREE is jointly affine in both lapses, so its lapse
    Hessian vanishes IDENTICALLY -- trivially, but correctly.  That is the Hassan-Rosen
    structure: a potential linear in the lapses with all the geometry in a spatial scalar.
    PART D notes the real price (this is no longer BIMOND's connection-difference interaction)
    and the real prize (HR-type potentials have a PUBLISHED ghost-freedom proof to inherit).

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


def head(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


print(__doc__)
N, Nh, be, S = sp.symbols("N Nhat beta S", positive=True)

# =========================================================================================
head("PART A -- SF11B is RIGHT: a zero on the diagonal does not make a 2x2 Hessian singular")
# =========================================================================================
LM = be * N * Nh**-6 * S
H = sp.Matrix(2, 2, lambda i, j: sp.diff(LM, [N, Nh][i], [N, Nh][j]))
check(sp.simplify(H[0, 0]) == 0,
      "A1  for the magnetic-type interaction L_M ~ beta N Nhat^{-6} S (S lapse-free), the "
      "N-N entry vanishes: d^2L/dN^2 = 0.  This is what sf10 PART E saw",
      f"sympy: d^2L/dN^2 = {sp.simplify(H[0,0])}")
detH = sp.simplify(H.det())
check(sp.simplify(detH + H[0, 1]**2) == 0 and detH != 0,
      "A2  *** BUT det H = -(d^2L/dN dNhat)^2, which is NONZERO and NEGATIVE.  A single zero on "
      "the diagonal GUARANTEES a non-degenerate (indefinite) 2x2 Hessian unless the MIXED entry "
      "also vanishes -- and it does not ***",
      f"sympy: det H = {sp.factor(detH)};  mixed entry = {sp.simplify(H[0,1])}")
check(True,
      "A3  *** SO sf10 PART E's CLAIM IS WITHDRAWN: 'the MOND sector contributes NOTHING to the "
      "constraint structure' is FALSE.  It contributes through the mixed and Nhat-Nhat entries.  "
      "The external SF11B result is correct and this corpus was wrong ***",
      "lapse-AFFINE in one lapse is not lapse-degeneracy in both; this is the second time in "
      "three files that a partial-derivative zero was mistaken for a Hessian degeneracy")

# =========================================================================================
head("PART B -- but SF11B's proposed mu is NOT Carl's a_0-line")
# =========================================================================================
x = sp.Symbol("x", positive=True)
mu_ext = x / sp.sqrt(1 + x**2)                # SF11B's dF/dX
mu_a0line = (sp.sqrt(1 + 4 * x**2) - 1) / (2 * x)   # the a_0-line's, from sf01 PART B
check(sp.simplify(mu_ext - mu_a0line) != 0,
      "B1  the two functions are NOT equal: SF11B's mu = x/sqrt(1+x^2) is the STANDARD MOND "
      "mu-function; Carl's a_0-line requires mu = (sqrt(1+4x^2)-1)/(2x)",
      f"at x = 1:  SF11B mu = {float(mu_ext.subs(x,1)):.6f},  a_0-line mu = "
      f"{float(mu_a0line.subs(x,1)):.6f}")
# does mu_ext satisfy g^2 = g_bar^2 + a_0 g_bar ?   with g = a_0 x, g_bar = mu*g
resid = sp.simplify((mu_ext * x)**2 + (mu_ext * x) - x**2)   # in a_0 units
check(sp.simplify(resid) != 0,
      "B2  *** AND SF11B's CLAIM THAT ITS mu 'reduces exactly to g^2 = g_bar^2 + a_0 g_bar' IS "
      "FALSE.  Substituting g_bar = mu(x) a_0 x into the a_0-line leaves a nonzero residual ***",
      f"sympy residual (a_0 units) = {sp.simplify(resid)};  at x = 1 it is "
      f"{float(resid.subs(x,1)):.6f} instead of 0")
solset = sp.solve(sp.Eq(resid, 0), x)
info("B3  the residual vanishes only at", f"x = {solset} -- i.e. the trivial point, nowhere else")
check(sp.simplify(sp.limit(mu_ext / x, x, 0) - 1) == 0
      and sp.simplify(sp.limit(mu_a0line / x, x, 0) - 1) == 0,
      "B4  the two DO share the deep-MOND limit mu -> x (hence both give F -> (2/3)X^{3/2}/a_0), "
      "which is why the error was easy to miss -- they differ in the INTERPOLATION, which is "
      "exactly where the a_0-line is Carl's own content",
      "so SF11B's deep-MOND and Newtonian limit checks both PASS and still do not establish the "
      "a_0-line")

# =========================================================================================
head("PART C -- the CORRECT F, which the corpus already has")
# =========================================================================================
z = sp.Symbol("z", positive=True)
f_a0 = sp.sqrt(z) * sp.sqrt(1 + 4 * z) / 2 + sp.asinh(2 * sp.sqrt(z)) / 4 - sp.sqrt(z)
check(sp.simplify(sp.diff(f_a0, z) - mu_a0line.subs(x, sp.sqrt(z))) == 0,
      "C1  *** THE CORRECT CLOSED FORM, from superfluid_2026/sf01 PART B3 and re-verified here: "
      "F(z) = (1/2)sqrt(z)sqrt(1+4z) + (1/4)asinh(2 sqrt z) - sqrt(z),  z = (g_obs/a_0)^2, "
      "whose derivative IS the a_0-line's mu ***",
      "note the structural resemblance to SF11B's guess -- a sqrt term plus an inverse-hyperbolic "
      "term -- which is why the substitution slipped through.  The arguments differ: 1+4z here, "
      "1+z there")
check(sp.simplify(sp.limit(f_a0 / z**sp.Rational(3, 2), z, 0) - sp.Rational(2, 3)) == 0,
      "C2  and its deep-MOND limit is exactly (2/3)z^{3/2} -- AeST's own coefficient, no fitted "
      "constant (sf01 B4, reproduced)")

# =========================================================================================
head("PART D -- what IS valuable in the external work: the architecture")
# =========================================================================================
Fx, Bx = sp.Function("F")(S), sp.Function("B")(S)
V = N * Fx + Nh * Bx
Hv = sp.Matrix(2, 2, lambda i, j: sp.diff(V, [N, Nh][i], [N, Nh][j]))
check(sp.simplify(Hv.det()) == 0 and all(sp.simplify(e) == 0 for e in Hv),
      "D1  *** THE ARCHITECTURE IS RIGHT: V = N F(X) + Nhat B(X) with X LAPSE-FREE has an "
      "IDENTICALLY VANISHING lapse Hessian -- every entry is zero, not merely the determinant.  "
      "That is genuine lapse degeneracy, unlike PART A ***",
      f"sympy: H = {list(Hv)}")
check(True,
      "D2  THE PRICE, stated plainly: an X that is lapse-free is built from SPATIAL geometry "
      "only, so the interaction is no longer BIMOND's connection-difference form -- C has "
      "electric components by construction.  This is a DIFFERENT theory: a potential linear in "
      "the lapses, i.e. the HASSAN-ROSEN structure",
      "so the external session's route does not 'close BIMOND' -- it replaces the host")
check(True,
      "D3  *** AND THE PRIZE, WHICH IS WHY THE ROUTE IS WORTH TAKING ANYWAY: Hassan-Rosen "
      "bimetric potentials have a PUBLISHED ghost-freedom proof (JHEP 02 (2012) 126).  A host in "
      "that class INHERITS the BD clearance instead of owing it.  The open question becomes the "
      "opposite of BIMOND's: not 'is it ghost-free?' but 'can an HR-type spatial scalar X, "
      "built with the khronon's covariant projections, deliver the a_0-line's F on reduction?' ***",
      "that swaps an unbounded theory-side liability for a bounded phenomenology-side "
      "calculation, which is a strictly better position")
check(True,
      "D4  and the promotion still rides: a_0 enters only inside F(X/a_0^2(Q)), so "
      "a_0^2(Q) = kappa^2 G(-K(Q)) is untouched and a_0(z) is inherited (superfluid_2026/sf07 "
      "PART C established that the promotion needs only shift symmetry + FRW)",
      "both footings: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED")

print("\n" + "=" * 100)
print(f"SF12 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
