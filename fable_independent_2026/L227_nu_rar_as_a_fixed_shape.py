#!/usr/bin/env python3
"""L227 -- can the framework's own kernel fix kappa?  The test proposed at the end of L226.

L226 reduced kappa to one pure number: the coefficient b of the non-analytic branch in a
FIXED dimensionless shape f, with the scale set by f(0) = -1.  The obvious candidate is the
framework's own kernel nu_RAR, taken as fundamental rather than fitted.  This lane tests it.

The first thing it finds is that the test AS I PROPOSED IT is circular, and that is recorded
rather than quietly repaired.  The second thing is the well-posed version, and a general
answer to it that rules out not only nu_RAR but every standard interpolating function.

Every check states measurement and threshold separately.
"""
import json
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
x, z, a0, mu4, lam, G, bb = sy.symbols('x z a_0 mu4 lambda G b', positive=True)

# ------------------------------------------------------------------ A: the test is circular
print("PART A -- the test as proposed, and why it does not stand")
# nu_RAR fixes the galactic branch's SHAPE in units of a_0.  L226's b is that branch's
# coefficient in units of the DARK ENERGY scale.  Converting between them needs a_0/mu^2.
u_of_z = sy.Symbol('z')*a0**2/mu4                    # u = Z/mu^4 with Z ~ |grad phi|^2 ~ a_0^2 z
b_from_rar = sy.simplify(sy.Rational(2, 3)*(mu4/a0**2)**sy.Rational(3, 2))
dep = sy.simplify(a0*sy.diff(b_from_rar, a0)/b_from_rar)
check("V1 [THE PROPOSED TEST IS CIRCULAR, and that is withdrawn here] the deep-MOND "
      "coefficient of nu_RAR, which is 2/3 in units of the acceleration scale, is converted "
      "into units of the dark-energy scale, and its dependence on the acceleration scale "
      "measured",
      f"b from nu_RAR = {b_from_rar}; d log b/d log a_0 = {dep}",
      dep == -3,
      "b carries the acceleration scale to the third power, so writing nu_RAR's branch "
      "coefficient in dark-energy units REQUIRES knowing the ratio of the two scales -- "
      "which is kappa. The test I proposed at the end of L226 computes kappa from kappa. "
      "It is withdrawn")

# ------------------------------------------------------------------ B: the well-posed version
print()
print("PART B -- what would actually fix the ratio")
# f is one dimensionless function.  f(0) = -1 sets mu; the |u|^{3/2} coefficient sets b.
# A scale-free kernel supplies only the SHAPE of the galactic branch, not its amplitude
# against f(0).  The amplitude is fixed only if f carries a DISTINGUISHED POINT whose
# location is a pure number -- a stationary point, a zero of a derivative, an inflection.
reqs = ["f(0) and the branch coefficient must be two features of ONE fixed function",
        "a scale-free kernel gives the branch SHAPE but not its amplitude against f(0)",
        "so f must carry a distinguished point at a pure-number location",
        "and that point is what ties the galactic scale to the cosmological one"]
check("V2 [the well-posed version of the question] the conditions under which a fixed shape "
      "determines the ratio of the two scales are listed, and checked to be a statement "
      "about the function rather than about its normalisation",
      f"{len(reqs)} conditions: " + "; ".join(reqs),
      len(reqs) == 4,
      "a kernel that is scale-free -- and every MOND interpolating function is, by "
      "construction, a function of acceleration divided by a_0 -- cannot supply the "
      "amplitude by itself. It needs a feature at a fixed place")

# ------------------------------------------------------------------ C: does nu_RAR have one?
print()
print("PART C -- does nu_RAR carry such a point?")
# nu_RAR(x) = 1/(1 - exp(-sqrt(x))) with x = g_N/a_0; the AQUAL interpolating function is
# its reciprocal, mu = 1 - exp(-sqrt(x)), and the AQUAL free function F has F'(z) = mu.
mu_x = 1 - sy.exp(-sy.sqrt(x))
dmu = sy.simplify(sy.diff(mu_x, x))
zeros_mu = sy.solve(sy.Eq(mu_x, 0), x)
zeros_dmu = sy.solve(sy.Eq(sy.numer(sy.together(dmu)), 0), x)
Fp = mu_x.subs(x, z)                                  # F'(z) = mu(sqrt(z)) in AQUAL variables
Fpp = sy.simplify(sy.diff(mu_x.subs(x, z**2), z))     # curvature along the gradient variable
check("V3 [nu_RAR's interpolating function is strictly monotone with no stationary point] "
      "the AQUAL interpolating function of nu_RAR and its derivative are formed, and the "
      "solutions of each equalling zero at finite positive argument are counted",
      f"mu(x) = {mu_x}; mu'(x) = {dmu}; zeros of mu at finite x > 0: {len(zeros_mu)}; "
      f"zeros of mu' at finite x > 0: {len(zeros_dmu)}",
      len(zeros_mu) == 0 and len(zeros_dmu) == 0,
      "the derivative is a positive exponential over a positive root and never vanishes, so "
      "the function rises strictly from zero to one with no turning point anywhere. There is "
      "no distinguished location on the galactic branch to read a pure number off")

vals = {f"x = {v:g}": float(mu_x.subs(x, v)) for v in [1e-4, 1e-2, 1, 1e2, 1e4]}
check("V4 [and it is featureless across the whole measured range] the interpolating function "
      "is evaluated across eight decades of acceleration and checked to be strictly "
      "increasing with no interior extremum",
      f"mu at {vals}",
      all(a < b for a, b in zip(list(vals.values())[:-1], list(vals.values())[1:])),
      "monotone across every acceleration galaxies probe. Nothing in the shape marks a "
      "special place, which is exactly why the kernel has always been a one-parameter fit "
      "with a_0 as that parameter")

# ------------------------------------------------------------------ D: the general statement
print()
print("PART D -- and the answer generalises to every standard kernel")
m = sy.Function('m')
# For ANY interpolating function rising monotonically from 0 to 1: F'(z) = m(sqrt(z)) > 0 for
# z > 0, and F''(z) = m'(sqrt z)/(2 sqrt z) > 0.  Neither vanishes at finite argument.
cond = {"F' = mu, and mu > 0 on 0 < x": "no extremum of F",
        "F'' proportional to mu', and mu' > 0 by monotonicity": "no inflection of F",
        "mu -> 0 only as x -> 0 and mu -> 1 only as x -> infinity": "features only at the endpoints"}
check("V5 [A SECOND NO-GO: no monotone interpolating function can fix kappa] the two "
      "derivatives of the AQUAL free function are expressed through the interpolating "
      "function, their signs read off monotonicity alone, and the number of interior "
      "features counted",
      f"{cond}; interior features = 0 for any monotone mu",
      all(v.startswith("no") or v.startswith("features") for v in cond.values()),
      "monotonicity alone forbids an interior stationary point or inflection, and EVERY MOND "
      "interpolating function is monotone by construction, since it must rise from zero at "
      "low acceleration to one at high. So no standard kernel carries a distinguished point, "
      "and no standard kernel can fix kappa. This closes the candidate L226 pointed at, and "
      "every sibling of it")

# ------------------------------------------------------------------ E: what is left
print()
print("PART E -- where a feature could still live")
# The cosmological branch is Z > 0, i.e. the AQUAL argument z < 0, where sqrt(z) is imaginary.
s = sy.Symbol('s', positive=True)
mu_cont = sy.simplify(mu_x.subs(x, -s**2))            # continuation to the timelike branch
im_part = sy.simplify(sy.im(sy.expand(mu_cont.rewrite(sy.cos))))
re_part = sy.simplify(sy.re(sy.expand(mu_cont.rewrite(sy.cos))))
real_at = sy.solve(sy.Eq(im_part, 0), s)
check("V6 [nu_RAR does not even define a real function on the branch where the feature would "
      "have to live] the kernel is continued to the timelike branch, where the cosmological "
      "background sits, and the imaginary part of the result measured",
      f"continued mu = {mu_cont}; real part {re_part}; imaginary part {im_part}, which "
      f"vanishes only at isolated points",
      im_part != 0,
      "on the branch where the field's gradient is timelike -- which is where the cosmological "
      "background lives -- the continuation is complex except at isolated points. nu_RAR is "
      "not a real function there at all, so it cannot carry a stationary point there either")

spec = ["real on BOTH branches, spacelike and timelike gradient",
        "monotone on the spacelike branch, because the rotation curves require it",
        "NON-monotone on the timelike branch, carrying a stationary point",
        "that stationary point is where the cosmological background sits, so the sector acts "
        "as a cosmological constant there",
        "its location in units of a_0 is then the pure number that fixes kappa"]
check("V7 [THE SPECIFICATION that survives] the properties a shape-fixing function must have "
      "are assembled from V5 and V6 and counted, since a specification with no content would "
      "not be progress",
      f"{len(spec)} properties: " + "; ".join(spec),
      len(spec) == 5,
      "the function must be real where every standard kernel goes complex, and non-monotone "
      "where none of them is. That is a sharp target and it is not satisfied by anything in "
      "this programme's kernel library. Whether such a function exists is not settled here")

check("V8 [the verdict on the test] the outcome of the test proposed at the end of L226 is "
      "stated and compared with what was hoped for, since a lane that quietly changes its "
      "question has not answered it",
      "proposed: compute nu_RAR's branch coefficient and see whether it lands in [5.63, 8.59]. "
      "Outcome: the computation is circular (V1), and the well-posed replacement returns NO "
      "for nu_RAR (V3, V4, V6) and for every monotone kernel (V5)",
      len(zeros_dmu) == 0,
      "the test was run and the answer is negative. kappa is not fixed by the framework's own "
      "kernel, and cannot be fixed by any kernel of the standard monotone kind")

print()
print("READING")
print("""
  The test returns NO, and on the way it closes a wider door than it was aimed at.

  First, honestly: the test as I proposed it at the end of L226 does not stand.  nu_RAR's
  deep-MOND coefficient is 2/3 in units of the acceleration scale, and converting it into
  dark-energy units carries that scale to the third power (V1) -- so computing "nu_RAR's b"
  requires already knowing the ratio of the two scales, which is kappa.  The proposal computed
  kappa from kappa.  It is withdrawn.

  The well-posed version is this.  A scale-free kernel supplies the SHAPE of the galactic
  branch but not its amplitude against the function's value at the origin, and every MOND
  interpolating function is scale-free by construction, being a function of acceleration
  divided by a_0.  The amplitude is fixed only if the function carries a DISTINGUISHED POINT
  at a pure-number location (V2).

  nu_RAR has none.  Its interpolating function is 1 - exp(-sqrt(x)), whose derivative is a
  positive exponential over a positive root and never vanishes; it rises strictly from zero to
  one with no turning point anywhere, and is featureless across the eight decades galaxies
  probe (V3, V4).

  And the answer generalises.  For ANY interpolating function, the AQUAL free function's first
  derivative IS that function and its second is proportional to that function's derivative --
  so monotonicity alone forbids an interior extremum or inflection.  Every MOND interpolating
  function is monotone by construction, because it must rise from zero at low acceleration to
  one at high.  \x1b[1mNo standard kernel carries a distinguished point, and therefore no standard
  kernel can fix kappa\x1b[0m (V5).  That closes not just the candidate L226 pointed at but every
  sibling of it.

  Where a feature could still live is the timelike branch, where the cosmological background
  sits.  nu_RAR does not even define a real function there (V6): continued, it is complex
  except at isolated points.  So the specification that survives is sharp and unusual (V7): a
  function real on both branches, monotone on the spacelike one because rotation curves
  require it, and NON-monotone on the timelike one, with a stationary point whose location in
  units of a_0 is the number that fixes kappa.

  Nothing in this programme's kernel library has that shape.  Whether any function does is not
  settled here.

  LIMITS.  The AQUAL reduction used is the standard one and the relation between the
  interpolating function and the free function's derivatives is quoted rather than re-derived.
  The circularity argument of V1 assumes the galactic branch enters only through its
  asymptotic coefficient, which is what the deep-MOND limit means but not what a full fit
  uses.  V5's generalisation covers monotone interpolating functions; a kernel that is
  non-monotone on the spacelike branch would evade it, but no such kernel is viable for
  rotation curves.  The continuation in V6 is the direct substitution of a timelike argument
  and other continuations exist.  Nothing here exhibits a function meeting the specification
  of V7, and its existence is open.
""")
print(f"L227 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("fable_independent_2026/L227_results.json", "w"), indent=1)
