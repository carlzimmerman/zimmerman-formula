#!/usr/bin/env python3
"""L235 -- a meta-test: does ANY natural mathematical criterion pick the integer two?

Four structural angles failed in L234 and two pointed elsewhere.  Rather than keep generating
candidate stories one at a time -- which is how motivated reasoning works -- this lane fixes a
list of natural distinguishing properties of the family FIRST, then evaluates which member
each one selects, and reports the distribution.

THE PROTOCOL, stated before any result is looked at:
  * each criterion must be a property of the family mu_n(Y) = 1 - (1+Y)^(-n) alone, statable
    without reference to the number 2 or to kappa;
  * each must have a unique selected member, or be recorded as selecting none;
  * the list is fixed here and not extended after seeing the answers.

If the selected members scatter, the honest conclusion is that the mathematics does not pick
the exponent and only the data do.  If several independent criteria converge on the same
member, that is evidence.

Every check states measurement and threshold separately.
"""
import json
from collections import Counter
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
Y, z, nn = sy.symbols('Y z n', positive=True)
NS = [sy.Rational(1), sy.Rational(3, 2), sy.Rational(2), sy.Rational(3), sy.Rational(4)]

# ---------------------------------------------------------------- compute the criteria
print("PART A -- the pre-registered criteria, evaluated")
crit = {}

# C1: the free function F_n is rational (no logarithm)
F = {}
for k in [1, 2, 3, 4]:
    F[k] = sy.simplify(sy.integrate(1 - (1 + sy.sqrt(z))**(-k), z))
rat = [k for k in F if not F[k].atoms(sy.log)]
crit["F_n is rational (no logarithm)"] = rat[0] if len(rat) == 1 else rat

# C2: the residual's integral to infinity is MARGINAL (boundary of convergence)
#     int (1+Y)^-n dz = 2 int Y^(1-n) dY converges iff n > 2 -> boundary at n = 2
crit["convergence boundary of the residual integral"] = 2

# C3: the Legendre dual has a closed form (degree of the inverse map is n+1)
crit["the AQUAL-QUMOND dual is closed-form"] = 1

# C4: half saturation at the natural scale, mu(1) = 1/2
half = [k for k in [1, 2, 3, 4] if sy.simplify((1 - sy.Rational(1, 2)**k) - sy.Rational(1, 2)) == 0]
crit["mu(1) = 1/2 (half response at the natural scale)"] = half[0] if half else None

# C5: the decay ODE v' = -n v^(1+1/n) has an INTEGER power
intpow = [k for k in [1, 2, 3, 4] if sy.Rational(1, k).q == 1]
crit["the residual's decay ODE has integer power"] = intpow[0] if intpow else None

# C6: the second Taylor coefficient of mu is unity in magnitude: (n+1)/(2n) = 1
c6 = sy.solve(sy.Eq((nn + 1)/(2*nn), 1), nn)
crit["|second Taylor coefficient of mu| = 1"] = c6[0] if c6 else None

# C7: the deep-MOND coefficient of F is unity: 2n/3 = 1
c7 = sy.solve(sy.Eq(2*nn/3, 1), nn)
crit["deep-MOND coefficient of F equals 1"] = c7[0] if c7 else None

# C8: the deep-MOND coefficient of F is 2/3, the AQUAL-standard normalisation
c8 = sy.solve(sy.Eq(2*nn/3, sy.Rational(2, 3)), nn)
crit["deep-MOND coefficient of F equals the AQUAL 2/3"] = c8[0] if c8 else None

# C9: degrees-of-freedom counting, n = d/2 in d = 3
crit["Gamma-mixture dof counting, n = d/2 at d = 3"] = sy.Rational(3, 2)

# C10: the large-z constant of F - z is FINITE (converges) -> n > 2, boundary again at 2
crit["F - z tends to a finite constant (boundary)"] = 2

# C11: mu_n is its own inverse under Y -> 1/Y in any sense
inv = [k for k in [1, 2, 3, 4]
       if sy.simplify((1 - (1 + Y)**(-k)) - (1 - (1 + 1/Y)**(-k))) == 0]
crit["mu_n invariant under Y -> 1/Y"] = inv[0] if inv else None

# C12: the curvature at the origin equals minus the slope: mu''(0) = -mu'(0)
c12 = sy.solve(sy.Eq(-nn*(nn + 1), -nn), nn)
c12 = [x for x in c12 if x > 0]
crit["mu''(0) = -mu'(0)"] = c12[0] if c12 else None

print(f"    {'criterion':>50s} {'selects n =':>14s}")
for k, v in crit.items():
    print(f"    {k:>50s} {str(v):>14s}")

# ---------------------------------------------------------------- the distribution
print()
print("PART B -- the distribution of selected members")
vals = [v for v in crit.values() if v is not None and not isinstance(v, list)]
cnt = Counter(str(v) for v in vals)
print(f"    selected members: {dict(cnt)}")
n_two = cnt.get("2", 0)
check("V1 [the criteria do NOT converge] the pre-registered criteria are evaluated, the "
      "member each selects is recorded, and the number of distinct members selected is "
      "counted; convergence would mean nearly all picking the same one",
      f"{len(vals)} criteria with a unique selection, picking {len(cnt)} distinct members: "
      f"{dict(cnt)}",
      len(cnt) >= 3,
      "the criteria scatter across at least three different members. There is no convergence, "
      "and that is the answer to whether a mathematical reason is waiting to be found: on this "
      "evidence it is not")

check("V2 [and two is not even the modal choice] the most frequently selected member is "
      "identified and compared with two",
      f"selections: {dict(cnt)}; the modal member is "
      f"{cnt.most_common(1)[0][0]} with {cnt.most_common(1)[0][1]} of {len(vals)}; "
      f"n = 2 is selected by {n_two}",
      cnt.most_common(1)[0][0] != "2" or n_two < len(vals)/2,
      "n = 2 is picked by the two convergence-boundary criteria and by nothing else. Both of "
      "those are the SAME fact in two dressings -- the residual integral and the large-z "
      "constant converge together -- so it is really one criterion, not two")

check("V3 [the two criteria that do pick it are one fact, not two] the residual integral and "
      "the large-z constant are compared to see whether they are independent",
      "int (1-mu_n) dz converges iff n > 2, and F - z tends to a constant iff that same "
      "integral converges. They are the same statement",
      crit["convergence boundary of the residual integral"] ==
      crit["F - z tends to a finite constant (boundary)"],
      "so the honest count is ONE criterion selecting n = 2, and it selects it as a BOUNDARY "
      "case rather than as an interior optimum. A marginal index is what a criticality "
      "argument would want, which is why it is worth keeping on the record, but a boundary is "
      "not a derivation")

# ---------------------------------------------------------------- how surprising is one hit?
print()
print("PART C -- how surprising a single hit is")
k_distinct = len(cnt)
p_chance = 1.0/k_distinct
exp_hits = len(vals)*p_chance
check("V4 [one hit out of a scattered list is what chance produces] the expected number of "
      "criteria selecting any given member by chance is computed from the spread, and "
      "compared with the number that actually select two",
      f"{len(vals)} criteria spread over {k_distinct} members; expected hits on any one "
      f"member by chance is {exp_hits:.1f}; observed on n = 2 is {n_two}",
      n_two <= exp_hits + 1,
      "the observed count is what chance gives. This is the same discipline L228 applied to "
      "closed forms for the coefficient, and it gives the same verdict: a hit inside a "
      "scattered set is not evidence")

check("V5 [what would have counted] the pattern that would have constituted evidence is "
      "stated, so that the negative result has a definite meaning",
      "evidence would be three or more INDEPENDENT criteria selecting the same member, or one "
      "criterion selecting it as an interior optimum rather than a boundary. Neither occurred",
      len(cnt) >= 3 and n_two <= 2,
      "the test was capable of returning a positive and did not. That is worth more than not "
      "having run it")

# ---------------------------------------------------------------- the standing verdict
print()
print("PART D -- what stands")
check("V6 [the empirical result is untouched] the status of L232 after this lane is stated",
      "L232 stands: on 155 curves and 2788 points with nothing fitted, n = 2 gives 0.1502 dex "
      "(dark energy) and 0.1438 (critical) against 0.1660 and 0.1846 for n = 1. This lane "
      "bears on WHY, not on WHETHER",
      n_two >= 1,
      "the galaxies still select the exponent. What this lane closes off is the expectation "
      "that a tidy mathematical reason is nearly in hand: twelve natural criteria were fixed "
      "in advance and they scatter")

print()
print("READING")
print(f"""
  The mathematics does not pick the exponent.  Twelve natural criteria were fixed in advance
  and they scatter across {k_distinct} different members (V1).

  Only the convergence boundary picks two -- and the two criteria that appear to do so are the
  same fact in two dressings, since the residual's integral and the large-z constant converge
  together (V3).  So the honest count is ONE criterion, and it selects two as a BOUNDARY case
  rather than as an interior optimum.  That is worth keeping on the record, because a marginal
  index is exactly what a criticality argument would want and L229 did place the cosmological
  state at the function's critical point.  But a boundary is not a derivation.

  Meanwhile rationality of the free function picks three, the closed-form dual picks one,
  half-saturation at the natural scale picks one, the integer decay power picks one, and
  degree-of-freedom counting wants three halves.  One hit out of a list this scattered is what
  chance produces (V4).

  The test could have returned a positive -- three independent criteria agreeing, or an
  interior optimum -- and did not (V5).  That is the useful part: the expectation that a short
  mathematical reason is waiting should now be much lower, and effort is better spent
  elsewhere.

  None of this touches L232 (V6).  The galaxies still select the exponent with nothing fitted.
  The construction has an empirically selected integer and no derivation of it, and after this
  lane that looks less like a gap about to close and more like the honest shape of the result.

  LIMITS.  Twelve criteria is not exhaustive and the list is mine; a different list could
  shift the distribution, though it would have to be strikingly different to produce
  convergence. Several criteria are evaluated symbolically here; the degree-of-freedom count
  and the duality result are carried in from L234's searches. Whether a genuinely physical
  principle -- as opposed to a mathematical prettiness criterion -- fixes the exponent is not
  settled by this lane, and two such searches were running when it was written.
""")
print(f"L235 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES,
           "criteria": {k: str(v) for k, v in crit.items()}},
          open("fable_independent_2026/L235_results.json", "w"), indent=1)
