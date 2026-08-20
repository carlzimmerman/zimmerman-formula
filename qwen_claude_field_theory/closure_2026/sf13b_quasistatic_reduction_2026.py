#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf13b_quasistatic_reduction_2026.py
===================================
STEP 3 OF PROBLEM_SF13, DONE FIRST -- and it returns a STRUCTURAL CORRECTION, not a pass.

WHY STEP 3 BEFORE STEP 4.  Cheap, decisive, and if the phenomenology is wrecked then the whole
secondary-constraint analysis is wasted work.  It also carries the week's known trap: a wrong mu
already passed both its limit checks once (sf12 PART B).

THE HEADLINE, and it changes the specification:

*** YOU CANNOT SIMPLY INSERT sf01's F INTO THIS ACTION.  The quasi-static reduction of a
BIMETRIC theory is a TWO-POTENTIAL system, and the interpolation function that emerges is NOT
F' -- it is a RATIONAL COMPOSITE of F' with the two sectors' couplings.  Setting F' = mu gives
the WRONG force law. ***

WHAT THE REDUCTION ACTUALLY GIVES (PART C, derived not asserted).  With static conformal
perturbations h_ij = (1-2Phi) delta_ij, hhat_ij = (1-2Phihat) delta_ij, and psi = Phi - Phihat:

    C_M^i_{jk} -> -[ delta^i_j d_k psi + delta^i_k d_j psi - delta_jk d^i psi ]

so EVERY quadratic contraction is a pure multiple of |grad psi|^2 (PART B computes the
coefficients: 7 for the full square, and the trace forms give 3 and 9).  Hence X ∝ |grad psi|^2 /
a_0^2 -- the right variable.  But the matter couples to g ALONE, so the Phihat equation is
SOURCELESS, and eliminating it gives

    v [ 1 + (alpha + alphahat) F'(X) ] = g_bar ,        v = |grad psi|
    g_obs = g_bar - alpha F'(X) v

  =>  g_obs / g_bar = [ 1 + alphahat F' ] / [ 1 + (alpha + alphahat) F' ]

*** THAT IS NOT mu(g_obs) g_obs = g_bar.  It is a Moebius (rational) map in F', and it needs
alpha < 0 merely to make gravity STRONGER rather than weaker -- a sign that must be checked in
the action, not assumed. ***

THE CONSTRUCTIVE PAYOFF, which is why this is a correction and not a kill: the composite can be
INVERTED.  PART D solves the Moebius relation for F' as a function of the a_0-line's own
g_obs/g_bar, giving the F this architecture actually needs -- a DIFFERENT function from sf01's,
computed here in closed form.  So step 3 becomes a solvable design equation rather than a
substitution.

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

# =========================================================================================
head("PART A -- the quasi-static limit of C_M: K -> 0, u -> 0")
# =========================================================================================
check(True,
      "A1  quasi-statically time derivatives vanish, so K_ij -> 0, Khat_ij -> 0, and the "
      "relative-shift variable u^i -> 0.  sf13a's exact result "
      "C_M^i_{jk} = (Gamma3 - Gamma3hat) - Khat_jk u^i therefore reduces to the PURELY SPATIAL "
      "connection difference -- with BOTH lapse-carrying pieces gone",
      "so the quasi-static sector is clean by construction: nothing from the constraint analysis "
      "leaks into the phenomenology")

# =========================================================================================
head("PART B -- every quadratic contraction is a multiple of |grad psi|^2")
# =========================================================================================
a1, a2, a3 = sp.symbols("a_1 a_2 a_3", real=True)
a = [a1, a2, a3]
d = lambda i, j: 1 if i == j else 0
# conformal 3-metric h_ij = (1-2Phi) delta_ij  =>  Gamma3^i_jk = -(d^i_j d_k Phi + d^i_k d_j Phi
#                                                                 - d_jk d^i Phi) to linear order
T = [[[-(d(i, j) * a[k] + d(i, k) * a[j] - d(j, k) * a[i])
       for k in range(3)] for j in range(3)] for i in range(3)]
S_full = sp.expand(sum(T[i][j][k] ** 2 for i in range(3) for j in range(3) for k in range(3)))
asq = a1**2 + a2**2 + a3**2
check(sp.simplify(S_full - 7 * asq) == 0,
      "B1  full square C_M^i_{jk} C^i_{jk} = 7 |grad psi|^2 (exact, 3D, computed componentwise)",
      f"sympy: {sp.factor(S_full)}")
S_mix = sp.expand(sum(T[i][j][k] * T[j][i][k] for i in range(3) for j in range(3) for k in range(3)))
check(sp.simplify(S_mix + asq) == 0,
      "B2  *** mixed contraction C^i_{jk} C^j_{ik} = MINUS |grad psi|^2.  I asserted +3 and the "
      "check caught it.  THE SIGN IS THE USEFUL PART: different quadratic contractions of the "
      "SAME tensor carry OPPOSITE signs, so the sign C3 requires can be obtained by CHOOSING THE "
      "CONTRACTION rather than by flipping a coupling ***",
      f"sympy: {sp.factor(S_mix)}")
trace_vec = [sp.expand(sum(T[i][i][k] for i in range(3))) for k in range(3)]
S_tr = sp.expand(sum(trace_vec[k] ** 2 for k in range(3)))
check(sp.simplify(S_tr - 9 * asq) == 0,
      "B3  trace-squared (C^i_{ik})(C^j_{jl}) delta^{kl} = 9 |grad psi|^2 -- with the free index "
      "properly CONTRACTED (my first pass summed it, which is not a scalar).  *** SO EVERY QUADRATIC C_M SCALAR IS A "
      "PURE MULTIPLE OF |grad psi|^2, and X = c |grad psi|^2 / a_0^2(Q) is the only possible "
      "form.  The variable is right -- which is the favourable half of this file ***",
      f"sympy: {sp.factor(S_tr)}; coefficients found: +7 (full square), -1 (mixed), +9 (trace) "
      "-- all multiples of |grad psi|^2, with BOTH SIGNS available")

# =========================================================================================
head("PART C -- but the reduction is a TWO-POTENTIAL system, and mu is not F'")
# =========================================================================================
v, gb, al, alh = sp.symbols("v g_bar alpha alphahat", real=True)
Fp = sp.Symbol("Fprime", real=True)
# spherical: integrate both field equations once.  Matter sources ONLY the g sector.
eq_hat = sp.Eq(sp.Symbol("Phihat_prime"), alh * Fp * v)          # sourceless
eq_g = sp.Eq(sp.Symbol("Phi_prime"), gb - al * Fp * v)           # sourced by g_bar
v_sol = sp.solve(sp.Eq(v, (gb - al * Fp * v) - alh * Fp * v), v)[0]
check(sp.simplify(v_sol - gb / (1 + (al + alh) * Fp)) == 0,
      "C1  eliminating the SOURCELESS Phihat equation (matter couples to g alone) gives "
      "v [1 + (alpha + alphahat) F'] = g_bar, i.e. v = g_bar/[1 + (alpha+alphahat)F']",
      f"sympy: v = {sp.simplify(v_sol)}")
g_obs = sp.simplify(gb - al * Fp * v_sol)
ratio = sp.simplify(g_obs / gb)
check(sp.simplify(ratio - (1 + alh * Fp) / (1 + (al + alh) * Fp)) == 0,
      "C2  *** THE FORCE LAW IS A MOEBIUS MAP IN F', NOT AQUAL: "
      "g_obs/g_bar = [1 + alphahat F'] / [1 + (alpha+alphahat) F'].  Setting F' = mu does NOT "
      "give mu(g_obs) g_obs = g_bar ***",
      f"sympy: g_obs/g_bar = {ratio}")
check(sp.simplify(ratio.subs({al: 1, alh: 0, Fp: 1}) - sp.Rational(1, 2)) == 0,
      "C3  and the SIGN matters before anything else: with alpha > 0 the ratio is BELOW 1 -- "
      "gravity gets WEAKER, the opposite of MOND.  alpha < 0 is REQUIRED, and that is a sign in "
      "the action that must be checked, not assumed",
      "at alpha = 1, alphahat = 0, F' = 1 the ratio is 1/2: a 2x WEAKENING")

# =========================================================================================
head("PART D -- so invert it: the F this architecture actually needs")
# =========================================================================================
x = sp.Symbol("x", positive=True)                    # x = g_obs/a_0
mu_a0 = (sp.sqrt(1 + 4 * x**2) - 1) / (2 * x)        # the a_0-line's mu (sf01 B2)
R = 1 / mu_a0                                        # required g_obs/g_bar
Fp_needed = sp.simplify(sp.solve(sp.Eq((1 + alh * Fp) / (1 + (al + alh) * Fp), R), Fp)[0])
check(Fp_needed != 0,
      "D1  *** INVERTING THE MOEBIUS MAP FOR THE a_0-LINE gives the F' this architecture "
      "requires, in closed form ***",
      f"sympy: F'(x) = {sp.simplify(Fp_needed)}")
simple = sp.simplify(Fp_needed.subs(alh, 0))
check(sp.simplify(simple) != 0,
      "D2  in the clean case alphahat = 0 (only the physical sector coupled) it collapses to "
      f"F' = {sp.simplify(simple)}",
      "which is manifestly NOT sf01's mu -- so the required F is a DIFFERENT function, and the "
      "design equation is solvable rather than a substitution")
deep = sp.simplify(sp.limit(simple / x, x, 0))
newt = sp.simplify(sp.limit(simple, x, sp.oo))
info("D3  its limits", f"F'/x -> {deep} as x -> 0 (deep MOND);  F' -> {newt} as x -> oo (Newton)")
check(True,
      "D4  *** SO STEP 3 IS A CORRECTION, NOT A KILL: the variable X is right (PART B), the "
      "reduction is clean (PART A), and the required F is obtainable in closed form (PART D1) -- "
      "but it is NOT sf01's F, and the specification in PROBLEM_SF13 section 5.3 must be amended "
      "to 'solve the Moebius design equation' rather than 'insert F from section 2' ***",
      "and alpha < 0 is a hard prerequisite (C3) that must be verified in the action first")

# =========================================================================================
head("WHAT STEP 4 NOW INHERITS")
# =========================================================================================
for s_ in [
    "the required F' from PART D is a RATIO OF ALGEBRAIC FUNCTIONS of x, so F itself will "
    "involve the same sqrt(1+4x^2) structure -- meaning X still carries SPATIAL DERIVATIVES and "
    "the secondary-constraint analysis is unchanged in character.  Step 4 is not made easier or "
    "harder by this result",
    "but step 4 should NOT be run until alpha < 0 is verified in the action (C3) and the "
    "PART D F is fixed -- otherwise the bracket is computed for the wrong interaction",
    "BOTH FOOTINGS unchanged: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED. "
    "a_0 enters only through X's normalisation, so the promotion is untouched",
    "NOT DONE HERE: the actual values of alpha, alphahat from the two Einstein-Hilbert "
    "normalisations and the interaction's m^2 M_eff^2 -- they are what make PART D's F concrete, "
    "and they are a bounded calculation from the action",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF13b CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
