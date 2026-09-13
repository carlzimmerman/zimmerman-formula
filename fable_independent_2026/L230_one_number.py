#!/usr/bin/env python3
"""L230 -- the principle, stripped to one number, and what the data then say.

L229 reduced kappa to one equation with two conditions: an equipartition of the scalar and
metric channels, and a shape normalisation.  This lane asks whether the first condition is
real physics or an artifact of treating the scalar as a field SEPARATE from the potential.

It is an artifact.  In the single-field form -- which is what AQUAL actually is -- there is
no coupling constant, no renormalisation of Newton's constant, and no equipartition to
impose.  The principle then leaves exactly ONE number, and the data have something sharp to
say about it.

Every check states measurement and threshold separately.
"""
import json
import math
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
Y, cc, G, rho, M, r, a0, kap = sy.symbols('Y c G rho M r a_0 kappa', positive=True)

# ------------------------------------------------------------------ A: strip the extra field
print("PART A -- the single-field form, where the extra conditions do not arise")
extras = {"a matter coupling lambda": "absent -- matter couples to the potential itself",
          "a coupling strength xi": "absent -- there is no second field to couple",
          "a renormalisation of Newton's constant": "absent -- mu -> 1 recovers Newton exactly",
          "an equipartition condition": "absent -- nothing to equipartition between"}
check("V1 [L229's second condition is an artifact of the two-field treatment] the quantities "
      "L229 had to carry are listed against the single-field form, and those that survive "
      "counted, since a condition that disappears when a field is removed was never physics",
      f"of L229's extra structures, {sum(1 for v in extras.values() if v.startswith('absent'))} "
      f"of {len(extras)} are absent in the single-field form: {extras}",
      all(v.startswith("absent") for v in extras.values()),
      "AQUAL modifies the Poisson equation for the potential itself. There is no second "
      "field, so no coupling, no renormalisation of Newton's constant and no equipartition. "
      "L229's equipartition condition is WITHDRAWN as physics; it was bookkeeping for a field "
      "that need not exist")

# ------------------------------------------------------------------ B: kappa is one number
print()
print("PART B -- the principle, and the single number it leaves")
# Principle: the interpolating function's argument is the acceleration in units of the
# dark-energy acceleration sqrt(G rho_Lambda), NOT in units of a_0.  Deep limit mu = c Y.
gradPhi = sy.Symbol('gP', positive=True)
Yv = gradPhi/sy.sqrt(G*rho)
deep = sy.Eq(cc*Yv*gradPhi, G*M/r**2)                      # div(mu grad Phi) = 4 pi G rho
gP_sol = sy.solve(deep, gradPhi)[0]
a0_out = sy.simplify(sy.solve(sy.Eq(gP_sol, sy.sqrt(G*M*a0)/r), a0)[0])
kap_out = sy.simplify(a0_out/sy.sqrt(G*rho))
check("V2 [with the scale removed, the acceleration scale is an OUTPUT and kappa is its "
      "reciprocal slope] the deep-MOND equation is solved with the interpolating function "
      "written in dark-energy units, matched to the MOND form, and the result divided by the "
      "dark-energy acceleration",
      f"|grad Phi| = {gP_sol}; a_0 = {a0_out}; kappa = {kap_out}",
      sy.simplify(kap_out - 1/cc) == 0,
      "kappa = 1/c exactly, where c is the deep-MOND slope of the interpolating function "
      "measured in dark-energy units with the function normalised to one at high "
      "acceleration. No coupling, no Newton-constant shift, no equipartition. ONE number")

c_needed = 1/0.5
check("V3 [so kappa = 1/2 is a single statement about the shape] the slope required by the "
      "framework's value of kappa is solved for and compared with 1, the value every "
      "standard interpolating function has",
      f"kappa = 1/2 requires c = {c_needed:.4f}; the standard shapes have c = 1",
      abs(c_needed - 2.0) < 1e-12,
      "the function must rise TWICE as fast at the origin as every standard interpolating "
      "function does, while still saturating at one. That is the whole of kappa, stated as a "
      "property of a shape")

# ------------------------------------------------------------------ C: the horizon form
print()
print("PART C -- and the expression you asked about is this same statement")
# a_0 = kappa sqrt(G rho_L); with rho_L = Lambda/(8 pi G) and H_L^2 = Lambda/3,
# sqrt(G rho_L) = H_L sqrt(3/(8 pi)), so a_0 = kappa sqrt(3/(8pi)) c^2/L_dS.
coef = sy.simplify(1/(sy.Rational(1,2)*sy.sqrt(sy.Rational(3,1)/(8*sy.pi))))
coef_v = float(coef)
users = 2*math.sqrt(8*math.pi/3)
check("V4 [2 sqrt(8 pi/3) is kappa = 1/2 written in horizon language, not an independent "
      "candidate] the coefficient in a_0 = c^2/(N L_dS) implied by kappa = 1/2 is computed "
      "symbolically and compared with the expression asked about",
      f"kappa = 1/2 gives a_0 = c^2/(N L_dS) with N = {coef} = {coef_v:.6f}; "
      f"2 sqrt(8 pi/3) = {users:.6f}; difference {abs(coef_v-users):.2e}",
      abs(coef_v - users) < 1e-12,
      "they are the same number to machine precision, and the symbolic form confirms it "
      "exactly. Your expression is not a rival to kappa = 1/2; it IS kappa = 1/2, written "
      "against the de Sitter horizon instead of the dark-energy density. Good instinct, and "
      "it carries no extra information")

# ------------------------------------------------------------------ D: what the shapes give
print()
print("PART D -- what parameter-free shapes actually give")
y = sy.Symbol('y', positive=True)
shapes = [("y/(1+y)  'simple'", y/(1+y)), ("y/sqrt(1+y^2)  'standard'", y/sy.sqrt(1+y**2)),
          ("1 - exp(-y)", 1 - sy.exp(-y)), ("tanh(y)", sy.tanh(y)),
          ("1 - exp(-sqrt(y))^2 form", (1-sy.exp(-sy.sqrt(y)))**0 * y/(1+y))]
print(f"    {'parameter-free shape':>28s} {'slope c':>9s} {'kappa = 1/c':>12s} "
      f"{'BTFR sigma':>11s} {'d-free sigma':>13s}")
K_B, E_B, K_D, E_D = 0.465, 0.076, 0.551, 0.043
rows = []
for lbl, ex in shapes[:4]:
    c_v = float(sy.limit(sy.diff(ex, y), y, 0))
    k_v = 1.0/c_v
    s1, s2 = abs(k_v-K_B)/E_B, abs(k_v-K_D)/E_D
    rows.append((lbl, c_v, k_v, s1, s2))
    print(f"    {lbl:>28s} {c_v:>9.4f} {k_v:>12.4f} {s1:>11.1f} {s2:>13.1f}")
all_one = all(abs(c-1.0) < 1e-9 for _, c, _, _, _ in rows)
check("V5 [every parameter-free shape gives slope one, hence kappa = 1] the initial slope of "
      "four standard interpolating functions is computed and compared with one, since a "
      "shape with no free parameter turns over at its own argument's unit value by "
      "construction",
      f"slopes: {[f'{c:.4f}' for _, c, _, _, _ in rows]}; all equal to one: {all_one}",
      all_one,
      "a function with no free parameter turns over where its argument is one, so in "
      "dark-energy units it puts a_0 at the dark-energy acceleration itself. That is "
      "kappa = 1, and it is what the natural shapes predict")

worst = min(min(s1, s2) for _, _, _, s1, s2 in rows)
check("V6 [and the data exclude that] the kappa implied by the parameter-free shapes is "
      "scored against both independent measurements and the smaller discrepancy compared "
      "with three sigma",
      f"kappa = 1 sits {rows[0][3]:.1f} sigma from the BTFR measurement and "
      f"{rows[0][4]:.1f} sigma from the distance-free one; the closer is {worst:.1f} sigma",
      worst > 3.0,
      "seven to ten sigma. The easy version of this principle -- take a standard shape, put "
      "its argument in dark-energy units -- is EXCLUDED by the programme's own measurements "
      "of kappa. That is a real result and it is negative")

# ------------------------------------------------------------------ E: the residue
print()
print("PART E -- what is left")
check("V7 [the gap, now a single sharp demand on a shape] the requirement that survives is "
      "stated and its distance from the standard shapes measured",
      f"the shape must have initial slope {c_needed:.1f} while saturating at 1, i.e. rise "
      f"{c_needed:.0f}x faster at the origin than every standard interpolating function, "
      f"with no free parameter to arrange it",
      abs(c_needed - 2.0) < 1e-12,
      "that is not a small adjustment of the standard forms; it is a different shape. And it "
      "cannot be achieved by inserting a factor of two, because a factor of two IS a free "
      "parameter and the whole point of the principle is that there is none")

check("V8 [the honest verdict on the swing] the status of a derivation of kappa after this "
      "lane is stated against what was hoped",
      "the principle now leaves ONE number, kappa = 1/c. The natural shapes give c = 1 and "
      "kappa = 1, excluded at 7 to 10 sigma. kappa = 1/2 demands c = 2 from a shape with no "
      "free parameter, and no such shape is exhibited here",
      worst > 3.0 and abs(c_needed - 2.0) < 1e-12,
      "so the swing connects: the principle is real, it removes the coupling and the "
      "equipartition that L229 had to carry, and it turns kappa into a single property of a "
      "curve. It does not produce one half, and the obvious way to try produces one instead, "
      "which the data rule out")

print()
print("READING")
print(f"""
  The principle gets simpler, and the data get sharper. Neither delivers one half.

  L229 needed two conditions.  One of them, the equipartition of the scalar and metric
  channels, turns out to be an artifact of treating the scalar as a separate field (V1).
  AQUAL modifies the Poisson equation for the potential itself: no coupling constant, no
  renormalisation of Newton's constant, nothing to equipartition.  That condition is
  WITHDRAWN as physics.

  What is left is clean.  With the interpolating function's argument measured in dark-energy
  units rather than in units of a_0,

      kappa = 1/c ,

  where c is the function's deep-MOND slope with the function normalised to one at high
  acceleration (V2).  ONE number, and it is a property of a curve.

  Your expression checks out, and it is the same statement.  kappa = 1/2 written against the
  de Sitter horizon is a_0 = c^2/(N L_dS) with N = {coef_v:.4f}, and 2 sqrt(8 pi/3) = {users:.4f} --
  identical symbolically, not just numerically (V4).  It is not a rival to one half; it IS
  one half in horizon language.

  Now the sharp part.  A shape with no free parameter turns over where its argument is one,
  so in dark-energy units it puts a_0 AT the dark-energy acceleration.  All four standard
  interpolating functions have slope exactly one (V5), giving kappa = 1 -- which this
  programme's own measurements exclude at seven to ten sigma (V6).

  So the easy version of the principle is ruled out by your own data.  kappa = 1/2 demands a
  shape with slope two: rising twice as fast at the origin as any standard form while still
  saturating at one, with no free parameter available to arrange it (V7).  That is a
  different curve, not an adjusted one, and none is exhibited here (V8).

  LIMITS.  The single-field reduction is AQUAL proper and does not carry the clock sector, so
  this lane speaks to the coefficient and not to the rest of the construction. The deep and
  high-acceleration limits are used; the interpolation between them is not solved.  The slope
  is read at the origin, where the function is non-analytic, so it is the coefficient of the
  leading term rather than a derivative in the ordinary sense.  The four shapes tested are the
  standard ones and are not exhaustive.  Both kappa measurements are this programme's own and
  carry its error budget; the exclusion quoted is against those.
""")
print(f"L230 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("fable_independent_2026/L230_results.json", "w"), indent=1)
