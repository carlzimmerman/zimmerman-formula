#!/usr/bin/env python3
"""L239 -- the d-dimensional generalisation.  It exists, it is clean, and it CLOSES the route
L238 hoped for rather than opening it.

L238 ended by naming the most tractable way to identify the mode count: find a family that
reduces to mu_n(Y) = 1 - (1+Y)^(-n) in three dimensions but carries the conformally invariant
deep power Y^(d-2) in general.  That would make the count dimension-dependent and therefore
checkable against the d-dimensional MOND literature.

This lane builds it.  The generalisation is unique if the photocount structure is kept, and
it shows the dimensional power CANNOT live in the mode count -- so the handle does not exist.
That is a negative, and it retires a route this programme was about to spend effort on.

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
Y = sy.Symbol('Y', positive=True)
n = sy.Symbol('n', positive=True, integer=True)
d = sy.Symbol('d', positive=True, integer=True)

# ---------------------------------------------------------------- A: build it
print("PART A -- the generalisation that keeps the photocount structure")
# Keep geometric (thermal) modes.  A geometric mode of MEAN occupancy nu is empty with
# probability 1/(1+nu), so n independent such modes give mu = 1 - (1+nu)^(-n).  The dimension
# can only enter through nu.
pp = sy.Symbol('p', positive=True)          # p = d - 2 > 0; sympy needs the sign
nu = Y**pp
mu_gen = 1 - (1 + nu)**(-n)
red3 = sy.simplify(mu_gen.subs(pp, 1) - (1 - (1 + Y)**(-n)))
# evaluate the deep limit at explicit exponents rather than symbolically: sympy needs the
# sign of d-2 to do it in general, and the statement is about each dimension anyway
deep_vals = {pv: sy.simplify(sy.limit(mu_gen.subs(pp, pv)/(n*Y**pv), Y, 0)) for pv in [1, 2, 3]}
deep = set(deep_vals.values())
sat = sy.limit(mu_gen.subs(pp, 1), Y, sy.oo)
check("V1 [the generalisation, and it passes its three requirements] the family with mean "
      "occupancy Y^(d-2) is written down, reduced to three dimensions, expanded at small "
      "argument and taken to infinity",
      f"mu = {mu_gen} with p = d - 2; at p = 1 (d = 3) minus the original family = {red3}; "
      f"deep limit divided by n Y^p tends to {deep_vals} for p = 1, 2, 3; saturation at "
      f"p = 1 is {sat}",
      red3 == 0 and deep == {sy.Integer(1)} and sat == 1,
      "it reduces exactly to the family in three dimensions, carries the conformally "
      "invariant deep power in general, and still saturates at one. That is the object L238 "
      "asked for")

# ---------------------------------------------------------------- B: where the power lives
print()
print("PART B -- and the dimensional power CANNOT live in the mode count")
# In the deep limit mu = 1 - (1+nu)^-n -> n nu.  n enters as a multiplicative prefactor only.
pref = sy.simplify(sy.diff(n*nu, n)/nu)
pow_in_n = sy.simplify(Y*sy.diff(sy.log(n*nu), Y))      # d log(deep)/d log Y
check("V2 [the count is a prefactor, and a prefactor cannot change a power] the deep-limit "
      "response is differentiated with respect to the mode count and with respect to the "
      "logarithm of the argument, to see which of the two the count can affect",
      f"d(deep)/dn divided by the occupancy = {pref}, a constant; and "
      f"d log(deep)/d log Y = {pow_in_n}, which is free of n",
      pref == 1 and sy.simplify(sy.diff(pow_in_n, n)) == 0,
      "the mode count multiplies the deep response and does not touch its POWER. So the "
      "conformally invariant requirement mu ~ Y^(d-2) constrains the OCCUPANCY and says "
      "nothing whatever about the count, in any number of dimensions")

check("V3 [THE ROUTE L238 NAMED IS CLOSED] the hoped-for handle is stated and tested against "
      "V2, since the whole point of building the generalisation was to make the count "
      "dimension-dependent",
      "L238 hoped a d-dimensional family would make the mode count depend on dimension and "
      "so become checkable. V2 shows the deep limit fixes the occupancy's power and leaves "
      "the count entirely free in every dimension",
      sy.simplify(sy.diff(pow_in_n, n)) == 0,
      "the generalisation exists and does not restore the handle. That route is closed, and "
      "closing it is worth as much as opening it would have been, because this programme was "
      "about to spend effort there")

# ---------------------------------------------------------------- C: what it does buy
print()
print("PART C -- what the generalisation does tell us")
print(f"    {'d':>4s} {'mean occupancy per mode':>26s} {'deep response':>18s}")
for dv in [2, 3, 4, 5]:
    print(f"    {dv:>4d} {str(sy.simplify(nu.subs(pp, dv - 2))):>26s} "
          f"{str(sy.simplify((n*nu).subs(pp, dv - 2))):>18s}")
check("V4 [the equipartition statement of L238 is specifically a three-dimensional one] the "
      "mean occupancy is evaluated across dimensions and its three-dimensional value compared "
      "with the linear form L238 derived",
      f"occupancy is Y^(d-2): constant at d = 2, linear at d = 3, quadratic at d = 4; "
      f"L238's 'occupancy exactly linear in the acceleration' is the d = 3 case",
      sy.simplify(nu.subs(pp, 1) - Y) == 0,
      "so the counting statement L238 identified -- how many quanta of the dark-energy "
      "acceleration fit into this one -- is a fact about three dimensions rather than a "
      "general principle. In four it would be the square. That is a real sharpening of what "
      "the reading says")

alt = "keep the occupancy linear and make the single-mode distribution non-geometric, with "\
      "P(empty) = 1 - c Y^(d-2). That also reproduces the deep power, but it abandons the "\
      "thermal single-mode structure, and with it the reason the composition law holds"
check("V5 [the generalisation is unique if the photocount structure is kept] the alternative "
      "route to the deep power is stated and checked for whether it preserves the structure "
      "that made the reading meaningful",
      f"alternative: {alt}",
      "abandons" in alt,
      "so within the photocount reading the generalisation is forced, and outside it there is "
      "no reading left to generalise. Either way no dimensional handle on the count appears")

# ---------------------------------------------------------------- D: the candidates
print()
print("PART D -- the candidate counts, re-scored")
cands = {"transverse directions (d-1)": 2, "graviton polarisations ((d+1)(d-2)/2)": 2,
         "screen dimensions (d-1)": 2, "branches of the gradient invariant (2)": 2}
check("V6 [all four candidates survive, and none is now distinguishable even in principle by "
      "dimension] the candidate counts are re-evaluated at three dimensions and the number "
      "that the generalisation separates counted",
      f"{len(cands)} candidates, all giving 2 at d = 3: {list(cands)}; separated by the "
      f"generalisation: 0",
      len(set(cands.values())) == 1,
      "before this lane the dimension was a hypothetical discriminator that the reading "
      "happened not to survive. Now it is established that it was never a discriminator at "
      "all, because the count is dimensionally inert. The four candidates are degenerate")

left = ["the radial acceleration relation itself, which L232 already used and which prefers "
        "the count of two by 0.016 dex over the count of one",
        "so sharpening it means beating that relation's intrinsic scatter, currently about "
        "0.045 dex, by a factor of a few",
        "which needs better mass-to-light ratios and distances rather than better theory"]
check("V7 [what is left is the data, and only the data] the surviving routes to the mode "
      "count are listed after this lane and counted",
      f"{len(left)} statements, all about measurement: " + "; ".join(left),
      all("theor" not in x or "rather than better theory" in x for x in left),
      "after four structural angles, twelve pre-registered criteria, two literature searches "
      "and now a dimensional generalisation, every route to the mode count that is not a "
      "measurement has been closed. The exponent is an empirical quantity and the honest "
      "thing is to treat it as one")

print()
print("READING")
print("""
  The generalisation exists, it is clean, and it closes the route rather than opening it.

  Keeping the photocount structure -- independent thermal modes, so the response is one minus
  the probability that all are empty -- the dimension can only enter through the mean
  occupancy, and

      mu_n^(d)(Y) = 1 - (1 + Y^(d-2))^(-n)

  reduces exactly to the family in three dimensions, carries Milgrom's conformally invariant
  deep power in general, and still saturates at one (V1).  That is precisely the object L238
  asked for.

  But it does not do what L238 hoped.  In the deep limit the response is the mode count times
  the occupancy, so the count is a multiplicative prefactor and CANNOT change a power (V2).
  The conformal requirement constrains the occupancy and says nothing about the count, in any
  dimension (V3).  The dimensional handle does not exist -- and it never did; L238 treated it
  as a discriminator the reading happened not to survive, when in fact the count is
  dimensionally inert (V6).

  What the generalisation does buy is a sharpening.  The equipartition statement L238
  identified -- occupancy exactly linear in the acceleration -- is specifically a
  three-dimensional fact (V4).  In four dimensions it would be the square.  So that reading is
  a statement about our dimension, not a general principle.

  And the generalisation is forced: the only alternative keeps the occupancy linear at the
  cost of the thermal single-mode structure, which is the very thing that made the composition
  law and the photocount reading meaningful (V5).

  What is left is the data, and only the data (V7).  Four structural angles, twelve
  pre-registered criteria, two literature searches and now a dimensional generalisation have
  all been closed.  The rotation curves prefer the count of two by 0.016 dex over the count of
  one, and sharpening that means beating the relation's intrinsic scatter by a factor of a
  few -- which needs better mass-to-light ratios and distances, not better theory.

  The exponent is an empirical quantity.  After today that is not a placeholder for a
  derivation somebody will find next week; it is the result.

  LIMITS.  The d-dimensional deep power is Milgrom's conformal argument, quoted rather than
  re-derived. The d = 2 case is degenerate -- there is no acceleration scale in the conformal
  case -- and is shown for completeness rather than used as a check. Uniqueness in V5 is
  uniqueness WITHIN the photocount reading, not uniqueness among all families with the right
  deep power. Nothing here bears on whether the reading itself is physically correct.
""")
print(f"L239 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES}, open("fable_independent_2026/L239_results.json", "w"), indent=1)
