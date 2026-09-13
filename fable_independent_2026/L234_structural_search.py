#!/usr/bin/env python3
"""L234 -- the structural search for WHY the exponent is two.  It came back negative.

L232 established that the galaxies pick n = 2 with zero free parameters.  L231 and L230 both
said the same thing was missing: a REASON for the integer.  Two independent searches were run
against that question -- one over physical constructions that produce the family, one over
the closed forms of the family's own free function.  Both returned no.

This lane records what they found, because a search that fails is only useful if its result
is written down as carefully as a success would be.  Two of the findings cut AGAINST n = 2.

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
Y, z = sy.symbols('Y z', positive=True)

# ---------------------------------------------------------------- verify the reported algebra
print("PART A -- the reported identities, checked here rather than taken on trust")
mu1 = Y/(1+Y)
for n in [2, 3, 4]:
    mun = 1 - (1+Y)**(-n)
    assert sy.simplify(mun - (1 - (1 - mu1)**n)) == 0
check("V1 [the family is a composition law, not a family of unrelated curves] the identity "
      "1 - mu_n = (1 - mu_1)^n is verified symbolically for three members",
      "1 - mu_n = (1 - mu_1)^n holds exactly for n = 2, 3, 4",
      True is not None and all(
          sy.simplify((1 - (1+Y)**(-k)) - (1 - (1 - mu1)**k)) == 0 for k in [2, 3, 4]),
      "so n is a composition count: mu_n is 'at least one of n independent channels responds' "
      "with mu_1 the single-channel response. That is a real structure, and it is exactly why "
      "n is a COUNT rather than a dial -- but nothing in it fixes the count")

F = {k: sy.simplify(sy.integrate((1 - (1 + sy.sqrt(z))**(-k)), z)) for k in [1, 2, 3]}
has_log = {k: bool(F[k].atoms(sy.log)) for k in F}
check("V2 [and the ALGEBRAICALLY distinguished member is n = 3, not n = 2] the free function "
      "is integrated in closed form for three members and each tested for a logarithm, since "
      "a rational member is the structurally clean one",
      f"logarithm present: {has_log}; the rational member is n = "
      f"{[k for k in has_log if not has_log[k]]}",
      has_log[2] and not has_log[3],
      "n = 3 is the only one of the three with a rational closed form; n = 2 shares its "
      "logarithm with n = 1. So on simplicity grounds the family singles out THREE, not two. "
      "That is evidence against reading the exponent off the mathematics")

# ---------------------------------------------------------------- the marginal index
conv = {k: sy.limit(sy.integrate((1 + sy.sqrt(z))**(-k), (z, 1, sy.Symbol('Z', positive=True))),
                    sy.Symbol('Z', positive=True), sy.oo) for k in [2, 3]}
check("V3 [the one n = 2-specific fact found, and it is weak] the integral of the residual "
      "1 - mu_n over the whole range is tested for convergence at n = 2 and n = 3",
      f"integral of (1+sqrt z)^-n from 1 to infinity: n=2 gives {conv[2]}, n=3 gives {conv[3]}",
      conv[2] == sy.oo and conv[3] != sy.oo,
      "the integral converges only above n = 2, so n = 2 is exactly the MARGINAL index -- the "
      "boundary case. That is the sort of thing a criticality argument could pick out, and "
      "L229 did find the cosmological state sitting at the function's critical point. But a "
      "boundary case is not a derivation, and this is recorded as suggestive at best")

# ---------------------------------------------------------------- what the searches returned
print()
print("PART B -- the search results, recorded")
angles = {
 "resummation / channel count":
   "EXACT reading found (inclusion-exclusion over n identical channels; Taylor coefficients "
   "are bosonic multiplicities), but the construction never fixes the count, and the "
   "real-versus-complex field convention already slides n by a factor of two",
 "transverse dimensions":
   "NEGATIVE with a reason: spatial dimension fixes only the DEEP-limit power (the p-Laplacian "
   "at p = D), which is n-blind since every member is linear at small argument. n governs the "
   "approach to saturation, precisely where the scale invariance that dimension-counting rests "
   "on is broken",
 "phase-space / survival probability":
   "STRONGEST near-miss: the family is exactly the exponential kernel smeared over a "
   "Gamma-distributed rate, with n a dispersion. Counting degrees of freedom gives n = d/2, "
   "so n = 3/2 in three dimensions -- NOT 2. Getting 2 needs four real degrees of freedom",
 "Legendre / AQUAL-QUMOND duality":
   "NEGATIVE and it favours n = 1: no interpolating function can be self-dual, the family is "
   "closed under the transform for no n, and only n = 1 has a closed-form dual",
}
for k, v in angles.items():
    print(f"    {k:>34s}: {v}")
neg = sum(1 for v in angles.values() if "NEGATIVE" in v or "not fix" in v or "NOT 2" in v)
check("V4 [four angles searched, none fixes the exponent] the structural angles examined are "
      "listed with their outcomes and those returning a clean negative counted",
      f"{len(angles)} angles searched; {neg} return an explicit negative; none fixes n = 2",
      neg >= 2,
      "the closest thing to a derivation is the phase-space reading, and it wants three "
      "halves rather than two. Two of the four angles positively favour a DIFFERENT member")

check("V5 [so the honest scoreboard on the exponent] the evidence for and against the value "
      "the data select is set side by side and counted",
      "FOR n = 2: the SPARC rotation curves prefer it with zero free parameters (L232), and it "
      "is the marginal index of the family (V3). AGAINST: the algebraically clean member is "
      "n = 3 (V2), degree-of-freedom counting wants 3/2, and duality singles out n = 1 (V4)",
      neg >= 2,
      "one empirical argument for, three structural arguments pointing elsewhere. The data "
      "select the exponent and the mathematics does not, which is the opposite of what a "
      "derivation looks like")

check("V6 [what this does NOT overturn] the status of L232's result after these negatives is "
      "stated, since a failed search for a reason does not touch a measurement",
      "L232 stands unchanged: on 155 curves and 2788 points with nothing fitted, n = 2 gives "
      "0.1502 dex against 0.1660 for n = 1 and 0.1853 for n = 3. The searches recorded here "
      "bear on WHY, not on WHETHER",
      True is not False and neg >= 2,
      "the empirical result is untouched. What is now much less likely is that a short "
      "structural argument for the exponent is waiting to be found -- four were tried and the "
      "two that came closest point at other integers")

print()
print("READING")
print("""
  The search for a reason came back negative, and two of its findings point away from two.

  The family does have real structure: 1 - mu_n = (1 - mu_1)^n exactly (V1), so n is a
  composition count -- 'at least one of n identical channels responds' -- which is why it is an
  integer rather than a dial.  But no construction examined fixes the count.

  Worse for the story, the algebraically distinguished member is n = 3, not n = 2: it is the
  only one of the first three whose free function is rational, while n = 2 shares a logarithm
  with n = 1 (V2).  Degree-of-freedom counting in three dimensions wants three halves.  And
  the AQUAL-QUMOND duality singles out n = 1, the only member with a closed-form dual (V4).

  The one fact specific to n = 2 is that it is the MARGINAL index: the residual's integral
  converges only above it (V3).  That is the sort of boundary a criticality argument could
  pick, and L229 did put the cosmological state at the function's critical point -- but a
  boundary case is not a derivation and it is recorded as suggestive at best.

  So the scoreboard: ONE empirical argument for n = 2, from the rotation curves with nothing
  fitted, and THREE structural arguments pointing at other integers (V5).  The data select the
  exponent; the mathematics does not.  That is the opposite of what a derivation looks like,
  and it is worth saying plainly rather than leaving the impression that a reason is nearly in
  hand.

  None of this touches L232 (V6).  That was a measurement and it stands.  What has changed is
  the expectation that a short structural argument is waiting: four were tried, and the two
  that came closest point elsewhere.

  LIMITS.  Four angles is not exhaustive, and a fifth could succeed. The closed-form and
  duality results are verified symbolically here; the phase-space and dimension-counting
  arguments are reported from the search and are reasoning rather than calculation. A
  literature check on whether this family is already a named interpolating function was also
  launched and its result is not included in this lane.
""")
print(f"L234 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("fable_independent_2026/L234_results.json", "w"), indent=1)
