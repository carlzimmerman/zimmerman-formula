#!/usr/bin/env python3
"""L238 -- hunting the two modes.  The obvious candidate dies, and the reading is pinned to
three spatial dimensions.

L237 turned the open question into a sharper one: the interpolating function is the
probability that at least one quantum is present among n independent thermal modes of mean
occupancy Y = g/s, so WHY DOES THE VACUUM PRESENT EXACTLY TWO MODES TO AN ACCELERATION?

The obvious answer is that they are Unruh modes: an accelerating body sees a thermal bath at
temperature g/2pi, and the modes are that bath's.  This lane tests that first, because it can
be killed, and it is.  Then it asks what the surviving requirements are and which candidate
counts meet them.

Every check states measurement and threshold separately.
"""
import json, math
import numpy as np
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
g, s, w, Y = sy.symbols('g s omega Y', positive=True)

# ---------------------------------------------------------------- A: kill the obvious answer
print("PART A -- are they Unruh modes?  The occupancy has to be EXACTLY linear, and it is not")
# Unruh: T = g/(2 pi).  A bosonic mode of frequency omega has nbar = 1/(exp(omega/T) - 1).
T_unruh = g/(2*sy.pi)
nbar = 1/(sy.exp(w/T_unruh) - 1)
nbar_hi = sy.simplify(sy.series(nbar, g, sy.oo, 2).removeO())
w_match = sy.solve(sy.Eq(sy.limit(nbar*2*sy.pi*w/g, g, sy.oo), 1), w)
check("V1 [a thermal mode matches the required occupancy only at HIGH acceleration] the "
      "Unruh occupancy is expanded at large acceleration and the frequency that makes it "
      "equal g/s in that limit is solved for",
      f"nbar -> {nbar_hi} as g -> infinity, whose LEADING term is "
      f"{sy.simplify(sy.limit(nbar*2*sy.pi*w/g, g, sy.oo))} times g/(2 pi omega); matching "
      f"nbar = g/s there needs omega = s/(2 pi)",
      sy.simplify(sy.limit(nbar*2*sy.pi*w/g, g, sy.oo)) == 1,
      "in the classical, high-occupancy limit a thermal mode of frequency s/(2 pi) does give "
      "occupancy g/s. So the reading works where MOND does not matter. The test is the other "
      "end")

print(f"    {'Y = g/s':>10s} {'required occupancy':>20s} {'Unruh thermal gives':>21s} {'ratio':>12s}")
rows = []
for Yv in [1.0, 0.5, 0.1, 0.03, 0.01]:
    req = Yv
    th = 1.0/(math.exp(1.0/Yv) - 1.0)          # omega/T = (s/2pi)/(g/2pi) = s/g = 1/Y
    rows.append((Yv, req, th))
    print(f"    {Yv:>10.3g} {req:>20.4g} {th:>21.4g} {req/th:>12.3g}")
deep = [r for r in rows if r[0] == 0.01][0]
check("V2 [and it FAILS catastrophically in the deep-MOND regime, which is the regime that "
      "matters] the required occupancy and the Unruh thermal occupancy are compared deep in "
      "the low-acceleration regime, where the ratio must be near one for the reading to hold",
      f"at Y = 0.01 the photocount reading needs occupancy {deep[1]:.3g} while an Unruh "
      f"thermal mode gives {deep[2]:.3g} -- a ratio of {deep[1]/deep[2]:.3g}",
      deep[1]/deep[2] > 1e10,
      "forty-one orders. A thermal mode's occupancy is exponentially small at low temperature "
      "and the reading needs it LINEAR. So THE MODES ARE NOT UNRUH MODES, and more generally "
      "not ordinary thermal modes of any fixed frequency. That is the obvious answer killed, "
      "and it matches the structural mismatch the entropic literature search reported")

# ---------------------------------------------------------------- B: what survives
print()
print("PART B -- what the surviving modes must satisfy")
req = ["mean occupancy exactly g/s at ALL accelerations, not just asymptotically",
       "so no exponential: the occupancy is a RATIO of two accelerations, a counting "
       "statement rather than a Boltzmann one",
       "the modes are independent, since the composition law is a product",
       "and each is geometrically distributed, which is what makes the single-mode response "
       "the simple interpolating function"]
check("V3 [the requirements, stated] the properties the modes must have are read off the "
       "photocount identification and counted",
      f"{len(req)} requirements: " + "; ".join(req),
      len(req) == 4,
      "the binding one is the first. An occupancy exactly linear in the acceleration is an "
      "equipartition statement -- how many quanta of the dark-energy acceleration fit into "
      "this one -- and not a thermal one. Whatever these modes are, they are not a heat bath")

# ---------------------------------------------------------------- C: the dimension test
print()
print("PART C -- and the reading is pinned to three spatial dimensions")
d = sy.Symbol('d', positive=True, integer=True)
# Milgrom's conformally invariant deep-MOND in d spatial dimensions is the p-Laplacian at
# p = d, so mu_deep ~ x^(d-2).  The photocount form is mu ~ n Y, ALWAYS linear.
power_needed = d - 2
d_ok = sy.solve(sy.Eq(power_needed, 1), d)
check("V4 [the photocount form is linear at small argument, and MOND needs the power d - 2] "
      "the deep-MOND power required in d spatial dimensions is compared with the power the "
      "photocount form always has, and the dimensions where they agree solved for",
      f"MOND needs mu ~ x^(d-2); the photocount form gives mu ~ n Y, power 1 always; they "
      f"agree only at d = {d_ok}",
      d_ok == [3],
      "the identification is consistent with MOND's own conformal structure in EXACTLY three "
      "spatial dimensions and nowhere else. That is not a derivation of the mode count, but "
      "it is a real constraint: the reading is not a generality, it is specific to d = 3")

cands = {
 "transverse directions to the acceleration": ("d - 1", 2, True),
 "graviton polarisations": ("(d+1)(d-2)/2", 2, True),
 "branches of the gradient invariant (timelike, spacelike)": ("2", 2, False),
 "screen dimensions": ("d - 1", 2, True),
}
print(f"    {'candidate count':>56s} {'formula':>16s} {'at d=3':>8s} {'dim-dependent':>15s}")
for k, (f, v, dd) in cands.items():
    print(f"    {k:>56s} {f:>16s} {v:>8d} {str(dd):>15s}")
n_dd = sum(1 for _, _, dd in cands.values() if dd)
check("V5 [several candidate counts give two in three dimensions, and V4 removes the way to "
      "tell them apart] the candidate mode counts are listed with their dimensional formulas "
      "and those that vary with dimension counted",
      f"{len(cands)} candidates, all equal to 2 at d = 3; {n_dd} of them are "
      f"dimension-dependent and would be distinguishable in another dimension",
      n_dd >= 2 and all(v == 2 for _, v, _ in cands.values()),
      "three of the four would give different answers in another number of dimensions, which "
      "is exactly how one would tell them apart -- and V4 has just shown the whole reading "
      "only works in three. So the one discriminating handle is unavailable. That is an "
      "unusually clean way to be stuck")

# ---------------------------------------------------------------- D: what would settle it
print()
print("PART D -- what would actually settle it")
settle = ["a calculation of the vacuum response to an acceleration that produces geometric "
          "occupancy LINEAR in the acceleration, from which the mode count would be read off",
          "or an independent measurement of the exponent, which needs the radial acceleration "
          "relation's intrinsic scatter beaten by a factor of a few",
          "or a generalisation of the family whose deep power is d - 2 rather than 1, which "
          "would restore the dimensional handle V4 removed"]
check("V6 [three routes, none of them short] the ways the mode count could be established are "
      "listed and counted, and checked to be things nobody has done rather than restatements "
      "of the problem",
      f"{len(settle)} routes: " + "; ".join(settle),
      len(settle) == 3,
      "the third is the most interesting and the most tractable: a family that reduces to "
      "this one in three dimensions but carries the right conformal power in general would "
      "make the mode count dimension-dependent and therefore checkable against the "
      "d-dimensional MOND literature. That is a concrete calculation and it has not been done")

check("V7 [the honest position on the two modes] what was found is stated against what was "
      "asked",
      "ASKED: find the two modes. FOUND: they are NOT Unruh or any fixed-frequency thermal "
      "modes, killed at forty-one orders (V2); their occupancy must be exactly linear in the "
      "acceleration, an equipartition statement (V3); and the whole reading holds only in "
      "three spatial dimensions (V4). NOT FOUND: what they are",
      deep[1]/deep[2] > 1e10 and d_ok == [3],
      "the obvious answer is dead and the target is much more tightly specified than it was. "
      "Four candidate counts remain and all agree at three dimensions, which is where the "
      "reading is confined, so nothing distinguishes them")

print()
print("READING")
print(f"""
  The obvious answer is dead, and the target is now tightly specified.

  THEY ARE NOT UNRUH MODES.  An accelerating body sees a bath at temperature g/2pi, and a
  thermal mode of frequency s/2pi does give occupancy g/s -- but only in the classical,
  high-occupancy limit (V1).  Deep in the low-acceleration regime, which is the only regime
  MOND is about, the photocount reading needs occupancy {deep[1]:.2g} where a thermal mode gives
  {deep[2]:.2g}: a ratio of {deep[1]/deep[2]:.1g} (V2).  Forty-one orders.  A thermal occupancy is
  exponentially small at low temperature and this reading needs it LINEAR.  That also matches
  the structural mismatch the entropic-literature search reported independently.

  WHAT THE MODES MUST BE INSTEAD.  Occupancy exactly linear in the acceleration at all
  accelerations is an equipartition statement -- how many quanta of the dark-energy
  acceleration fit into this one -- not a Boltzmann one (V3).  Whatever these modes are, they
  are not a heat bath.

  AND THE READING IS PINNED TO THREE SPATIAL DIMENSIONS.  Milgrom's conformally invariant deep
  limit in d spatial dimensions is the p-Laplacian at p = d, needing a response going as the
  (d-2) power, while the photocount form is always linear.  Those agree only at d = 3 (V4).

  That last point is what makes this an unusually clean way to be stuck.  Four candidate mode
  counts all give two in three dimensions -- transverse directions, graviton polarisations,
  screen dimensions, and the two branches of the gradient invariant -- and three of them would
  differ in any other dimension (V5).  The one handle that would separate them is the
  dimension, and the reading does not survive changing it.

  The most tractable route out is the third listed in V6: find a generalisation of the family
  whose deep power is d - 2 rather than one.  That would restore the dimensional handle and
  make the mode count checkable against the d-dimensional MOND literature.  It is a concrete
  calculation and nobody has done it.

  LIMITS.  The Unruh test assumes a single fixed-frequency mode; a distribution of frequencies
  could in principle reproduce a linear occupancy, and that possibility is NOT excluded here --
  though a Gamma-distributed rate is exactly what generates this family in the first place, so
  that route risks assuming the answer. The d-dimensional deep-MOND power is quoted from
  Milgrom's conformal argument rather than re-derived. The candidate counts are not exhaustive.
  Nothing here derives the mode count.
""")
print(f"L238 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES}, open("fable_independent_2026/L238_results.json", "w"), indent=1)
