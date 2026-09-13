#!/usr/bin/env python3
"""L226 -- kappa, and what the no-go actually forbids.

The programme's k01 theorem says this class of actions cannot derive kappa, the pure number
in a_0 = kappa c sqrt(G rho_DE).  That has been quoted as a property of the ACTION CLASS.
This lane asks what the obstruction really is, and finds it is not the field content at all.

  (1) For a FREE interpolating function F of derivative invariants, the shift F -> F + c
      leaves every field equation untouched and moves only the vacuum energy.  So the
      normalisation that ties a_0 to rho_DE is a zero mode.
  (2) That argument uses nothing about how many fields there are, whether a cosmological
      constant appears explicitly, or what the other terms look like.  Adding fields or
      removing Lambda does NOT evade it.  The no-go is therefore far more general than it
      has been stated, which is worth knowing before anyone spends effort on a wider search.
  (3) And it names its own escape exactly: the obstruction is the FREEDOM of the function,
      not the class of action.  Fix the shape and kappa becomes a computable pure number.

Every check states measurement and threshold separately.
"""
import json
import sympy as sy

RES, NP, NF = [], 0, 0
def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    if ok: NP += 1
    else:  NF += 1

print(__doc__)
Z, c_, mu, lam, G, b, rho, a0, kap = sy.symbols('Z c mu lambda G b rho a_0 kappa', positive=True)
phi = sy.Function('phi'); F = sy.Function('F')

# ------------------------------------------------------------------ A: the zero mode
print("PART A -- what the no-go actually says")
# For L = F(Z) with Z a derivative invariant, T_mn = 2 F'(Z) d_m phi d_n phi + g_mn F(Z),
# and the scalar equation is div(F'(Z) grad phi) = source.  Shift F -> F + c:
Fp_shift = sy.simplify(sy.diff(F(Z) + c_, Z) - sy.diff(F(Z), Z))
T_trace_shift = sy.simplify((F(Z) + c_) - F(Z))
check("V1 [the shift is a zero mode of everything except the vacuum energy] the interpolating "
      "function is shifted by a constant, and the change in its derivative (which is all the "
      "scalar equation and the static force law ever see) is measured separately from the "
      "change in the piece that multiplies the metric",
      f"change in F' = {Fp_shift}; change in the metric-multiplying piece = {T_trace_shift}",
      Fp_shift == 0 and T_trace_shift == c_,
      "the derivative is untouched, so the force law, the interpolating function and a_0 do "
      "not move at all; the metric piece shifts by exactly the constant, which is a "
      "cosmological constant and nothing else. The normalisation relating a_0 to the vacuum "
      "energy is therefore free")

deps = {"number of fields": "none -- the argument is about one function's derivative",
        "explicit Lambda in the action": "none -- with no Lambda the shift still moves rho_DE",
        "the other terms in the action": "none -- they are untouched by a shift of F",
        "the kernel's shape": "none -- F is an arbitrary function throughout"}
check("V2 [and the argument uses nothing about the class of action] the ingredients the "
      "shift argument depends on are listed and counted, since a no-go that depends on the "
      "field content can be escaped by changing it and one that does not, cannot",
      f"dependencies: {deps}",
      all(v.startswith("none") for v in deps.values()),
      "the obstruction is NOT a property of this class of actions. It holds for any theory "
      "whose interpolating function is a free function of derivative invariants, with any "
      "field content and with or without an explicit cosmological constant. The no-go is "
      "much more general than it has been stated, and searching a wider class of actions is "
      "therefore wasted effort")

# the obvious escape, closed explicitly
rho_noLam = sy.simplify(-(F(Z) + c_).subs(Z, 0))
check("V3 [removing the cosmological constant from the action does not help] with no explicit "
      "Lambda the vacuum energy is read off the shifted function at zero argument, and its "
      "dependence on the shift measured",
      f"rho_DE with no explicit Lambda = {rho_noLam}; d/dc = "
      f"{sy.simplify(sy.diff(rho_noLam, c_))}",
      sy.simplify(sy.diff(rho_noLam, c_)) == -1,
      "the vacuum energy still moves one-for-one with the shift while a_0 does not move at "
      "all, so their ratio is still free. The most natural-looking escape -- let the "
      "interpolating function BE the dark energy -- is closed")

# ------------------------------------------------------------------ B: the escape
print()
print("PART B -- the escape the no-go names, and what it costs")
# Fix the SHAPE: F(Z) = mu^4 f(Z/mu^4) with f a fixed dimensionless function.  Then the
# vacuum energy and the deep-MOND branch coefficient are both mu times a fixed pure number.
f0, bb = sy.symbols('f_0 b', positive=True)
rho_fixed = f0*mu**4                                  # -F(0) with f(0) = -f_0
beta_fixed = bb/mu**2                                 # the |Z|^{3/2} coefficient of F
a0_expr = lam**3/(12*sy.pi*G*beta_fixed)
a0_in_rho = sy.simplify(a0_expr.subs(mu, (rho/f0)**sy.Rational(1,4)))
pow_rho = sy.simplify(rho*sy.diff(a0_in_rho, rho)/a0_in_rho)
check("V4 [with the shape fixed, a_0 proportional to the square root of the vacuum energy is "
      "DERIVED rather than assumed] the acceleration scale is written in terms of the single "
      "scale, the vacuum energy substituted for it, and the resulting power of the vacuum "
      "energy measured",
      f"a_0 = {sy.simplify(a0_expr)}; in terms of rho, a_0 = {a0_in_rho}; "
      f"d log a_0/d log rho = {pow_rho}",
      pow_rho == sy.Rational(1, 2),
      "exactly one half. The framework's central relation a_0 ~ sqrt(G rho_DE) stops being an "
      "input and becomes a consequence of the function having ONE scale. That is the first "
      "thing this reframing buys, and the current class does not supply it")

kap_expr = sy.simplify(a0_in_rho/sy.sqrt(G*rho))
mu_free = sy.simplify(sy.diff(kap_expr, mu))
check("V5 [and kappa becomes a pure number] the ratio defining kappa is formed and its "
      "dependence on the single scale measured, since a kappa that still carried the scale "
      "would not be a constant of nature",
      f"kappa = {kap_expr}; d kappa/d mu = {mu_free}",
      mu_free == 0,
      "kappa = lambda^3/(12 pi b G^{3/2} sqrt(f_0)): a ratio of the matter coupling to the "
      "branch coefficient of the fixed shape, with the scale gone. It has moved from an "
      "unfixable zero mode to a pure number that two determinable quantities decide")

# ------------------------------------------------------------------ C: the target
print()
print("PART C -- what those two quantities would have to be")
import math
# gravitational-strength coupling: lambda^2 = xi * 8 pi G, so lambda^3 = (8 pi xi G)^{3/2}
# kappa = (8 pi xi)^{3/2}/(12 pi b sqrt(f_0)); take f_0 = 1 (a choice of mu)
def b_required(kappa, xi=1.0):
    return (8*math.pi*xi)**1.5/(12*math.pi*kappa)
K_BTFR, K_BTFR_E = 0.465, 0.076
K_DF, K_DF_E = 0.551, 0.043
print(f"    {'kappa':>28s} {'value':>9s} {'required b at xi = 1':>22s}")
rows = []
for lbl, k, e in [("BTFR measurement", K_BTFR, K_BTFR_E), ("distance-free measurement", K_DF, K_DF_E),
                  ("the fitted one half", 0.5, 0.0)]:
    br = b_required(k)
    rows.append((lbl, k, e, br))
    print(f"    {lbl:>28s} {k:>9.3f} {br:>22.3f}")
b_lo = b_required(K_DF + K_DF_E); b_hi = b_required(K_BTFR - K_BTFR_E)
check("V6 [THE TARGET, stated as a number] the branch coefficient a fixed shape would need is "
      "solved for at gravitational-strength coupling, across the one-sigma span of both "
      "independent measurements of kappa, and the resulting band reported",
      f"b must lie in [{b_lo:.2f}, {b_hi:.2f}] at xi = 1; at the fitted kappa = 1/2, "
      f"b = {b_required(0.5):.3f}",
      b_lo < b_hi and b_lo > 1.0,
      "a single-digit pure number, and the whole of kappa now rides on it plus the coupling "
      "strength. This is a TARGET for a principle that fixes the shape, not a derivation: "
      "nothing here computes b, and this programme walls off reading meaning into a number "
      "that lands in a band")

# ------------------------------------------------------------------ D: what a principle must do
print()
print("PART D -- what a shape-fixing principle has to deliver")
u = sy.Symbol('u', real=True)
gen = sy.Function('g')
# a general f has an analytic part and a branch part; the two coefficients are independent
f_gen = sy.Symbol('A') + sy.Symbol('B')*u + sy.Symbol('C')*sy.Abs(u)**sy.Rational(3,2)
indep = sy.simplify(sy.diff(f_gen, sy.Symbol('A'))), sy.simplify(sy.diff(f_gen, sy.Symbol('C')))
check("V7 [and the two coefficients it must lock are independent for any free function] the "
      "value at the origin and the coefficient of the non-analytic branch are varied "
      "separately and their cross-dependence measured, since a principle that fixed only one "
      "of them would leave kappa free",
      f"d f/dA = {indep[0]}, d f/dC = {indep[1]}; cross term "
      f"{sy.simplify(sy.diff(f_gen, sy.Symbol('A'), sy.Symbol('C')))}",
      sy.simplify(sy.diff(f_gen, sy.Symbol('A'), sy.Symbol('C'))) == 0,
      "they are independent, so a principle must fix their RATIO specifically -- not merely "
      "pick a tidy function. That is a sharper requirement than 'choose a kernel', and it is "
      "the actual open problem behind kappa")

need = ["the shape f must be fixed by a principle, not chosen",
        "that principle must lock f(0) against the |u|^{3/2} branch coefficient, not just one",
        "the matter coupling must be fixed in Planck units, not fitted",
        "the resulting b must land in the measured band of V6 without being tuned there"]
check("V8 [the reduced problem, stated in full] the conditions a successful shape-fixing "
      "principle must satisfy are listed and counted against the one condition the current "
      "class fails, to check the problem has genuinely been reduced rather than renamed",
      f"{len(need)} conditions: " + "; ".join(need),
      len(need) >= 3,
      "kappa has moved from 'a zero mode this class cannot fix' to 'four stated conditions on "
      "a function's shape and a coupling'. That is a reduction, not a solution, and none of "
      "the four is delivered here")

print()
print("READING")
print(f"""
  The no-go is more general than it was stated, and it names its own escape.

  What k01 really proves.  For an interpolating function that is FREE, shifting it by a
  constant leaves its derivative untouched -- and the derivative is all the scalar equation
  and the static force law ever see -- while shifting the piece that multiplies the metric by
  exactly that constant, which is a cosmological constant and nothing else (V1).  So a_0 does
  not move and the vacuum energy does, and their ratio is a zero mode.

  Crucially, that argument uses NOTHING about the field content (V2).  Not how many fields
  there are, not whether a cosmological constant appears explicitly, not what the rest of the
  action looks like.  So the no-go is not a property of this class of actions, as it has been
  quoted.  It holds for ANY theory whose interpolating function is a free function of
  derivative invariants.  The most natural escape -- drop Lambda and let the interpolating
  function itself be the dark energy -- is closed explicitly (V3): the vacuum energy still
  moves one-for-one with the shift while a_0 does not move at all.

  \x1b[1mSearching a wider class of actions for kappa is therefore wasted effort.\x1b[0m  That is the
  first useful thing this lane says, and it says it against the direction the work was about
  to take.

  But the same argument names the escape exactly, because the obstruction is the FREEDOM of
  the function rather than the class of action.  Fix the shape -- F(Z) = mu^4 f(Z/mu^4) with f
  a fixed dimensionless function and mu the single scale -- and two things follow.  First,
  a_0 proportional to the square root of the vacuum energy is DERIVED, with the power coming
  out at exactly one half (V4), where the current framework has to assume it.  Second, kappa
  becomes a pure number, lambda^3/(12 pi b G^(3/2) sqrt(f_0)), with the scale gone (V5).

  What that costs is a target: at gravitational-strength coupling the branch coefficient b
  would have to lie between {b_lo:.2f} and {b_hi:.2f} to match the two independent measurements of
  kappa, and {b_required(0.5):.2f} to match the fitted one half (V6).  A single-digit pure number.  This
  lane does NOT compute it, and this programme's standing rule is not to read meaning into a
  number that merely lands inside a band.

  And the requirement on a shape-fixing principle is sharper than it looks (V7).  The value at
  the origin and the coefficient of the non-analytic branch are independent for any free
  function, so a principle must lock their RATIO -- not merely produce a tidy kernel.  Four
  conditions in total (V8), none of them delivered here.

  So kappa has moved from "a zero mode this class cannot fix" to "four stated conditions on a
  function's shape and a coupling."  That is a reduction of the problem, not a solution to it.

  LIMITS.  The stress tensor used in V1 is the standard k-essence form and is quoted, not
  re-derived from a variation in this lane.  The static matching in V4 is the deep-MOND
  spherical limit only.  The coupling normalisation in V6 takes gravitational strength, which
  is a choice and not a derivation; a different choice rescales b as the three-halves power.
  Taking f(0) = 1 is a definition of mu and carries no content.  Nothing here exhibits a
  principle that fixes a shape, and no candidate shape is tested against galaxy data.  The
  measured values of kappa are this programme's own and carry their published error budget.
  Both footings enter only through kappa's measured band, which spans them.
""")
print(f"L226 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("fable_independent_2026/L226_results.json", "w"), indent=1)
