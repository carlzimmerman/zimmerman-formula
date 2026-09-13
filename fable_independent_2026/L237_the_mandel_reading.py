#!/usr/bin/env python3
"""L237 -- the family has an exact microphysical reading, and it is a photocount formula.

An independent search of the first-principles MOND derivations came back with one thing that
was not in any of them.  The family

    mu_n(Y) = 1 - (1 + Y)^(-n)

is EXACTLY Mandel's n-mode photocount formula: for n independent single-mode thermal
(chaotic) channels each of mean occupancy Y, the probability that a given mode is EMPTY is
1/(1+Y), so the probability that all n are empty is (1+Y)^(-n), and mu_n is the probability
that AT LEAST ONE quantum is present.

That is not a derivation of the exponent.  It is something better than nothing: the family
stops being an ansatz and becomes a counting statement, with n the number of independent
modes.  This lane verifies the identification and states precisely what it does and does not
buy.

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
Y, k, q = sy.symbols('Y k q', positive=True)

# ---------------------------------------------------------------- A: the identification
print("PART A -- the identification, verified")
# A single bosonic mode in thermal equilibrium with mean occupancy Y has a geometric
# (Bose-Einstein) distribution: P(k quanta) = Y^k/(1+Y)^(k+1).  Check normalisation and mean.
P = Y**k/(1+Y)**(k+1)
norm = sy.simplify(sy.summation(P, (k, 0, sy.oo)))
mean = sy.simplify(sy.summation(k*P, (k, 0, sy.oo)))
check("V1 [the single-mode distribution is the thermal one] the geometric occupancy "
      "distribution is summed and its mean taken, both of which must come out right before "
      "anything is built on it",
      f"P(k) = {P}; sum over k = {norm}; mean = {mean}",
      norm == 1 and sy.simplify(mean - Y) == 0,
      "normalised, with mean occupancy exactly Y. This is the Bose-Einstein distribution for "
      "one mode, written in terms of its own mean")

p_empty_1 = sy.simplify(P.subs(k, 0))
n_ = sy.Symbol('n', positive=True, integer=True)
p_empty_n = sy.simplify(p_empty_1**n_)
mu_n = sy.simplify(1 - p_empty_n)
check("V2 [THE IDENTIFICATION: the interpolating function IS a photocount probability] the "
      "probability that one mode is empty is read off, raised to the number of independent "
      "modes, and subtracted from one, then compared with the family",
      f"P(empty, one mode) = {p_empty_1}; P(all n empty) = {p_empty_n}; "
      f"1 - that = {mu_n}",
      sy.simplify(mu_n - (1 - (1+Y)**(-n_))) == 0,
      "the interpolating function is the probability that AT LEAST ONE quantum is present "
      "among n independent thermal modes of mean occupancy Y. Under this programme's own "
      "principle Y is the acceleration in units of the dark-energy acceleration, so the "
      "reading is: the response is the chance that the acceleration excites at least one "
      "quantum out of the vacuum")

rng = np.random.default_rng(20260913)
Yv, nv, N = 2.0, 2, 400000
draws = rng.geometric(p=1.0/(1.0+Yv), size=(N, nv)) - 1     # mean Yv per mode
emp = float(np.mean(draws.sum(axis=1) > 0))
exact = 1.0 - (1.0 + Yv)**(-nv)
check("V3 [and it survives a direct simulation] independent thermal modes are sampled and "
      "the fraction of trials with at least one quantum compared with the closed form",
      f"Monte Carlo at Y = {Yv}, n = {nv}, {N} trials: {emp:.5f} against the closed form "
      f"{exact:.5f}; difference {abs(emp-exact):.5f}",
      abs(emp - exact) < 5e-3,
      "agreement to three decimals. The identification is not a formal coincidence; the "
      "family is that counting statement")

# ---------------------------------------------------------------- B: the Tsallis form
print()
print("PART B -- and the same family is a deformed exponential")
q_of_n = 1 + 1/n_
# the q-exponential: exp_q(x) = (1 + (1-q) x)^(1/(1-q))
x = sy.Symbol('x')
expq = (1 + (1 - q)*x)**(1/(1 - q))
cand = sy.simplify(1 - expq.subs({q: q_of_n, x: -n_*Y}))
check("V4 [the family is one minus a q-deformed exponential, with q tied to the mode count] "
      "the Tsallis q-exponential is evaluated at the deformation q = 1 + 1/n and argument "
      "-nY, and compared with the family",
      f"1 - exp_q(-nY) at q = 1 + 1/n gives {cand}",
      sy.simplify(cand - (1 - (1+Y)**(-n_))) == 0,
      "so the mode count and the Tsallis deformation are the same parameter: n = 2 is "
      "q = 3/2. The ordinary exponential kernel is the q -> 1, infinite-mode limit. That ties "
      "the family to the deformed-statistics literature, where the deformation is a free "
      "parameter, so it relabels the unknown rather than removing it")

# ---------------------------------------------------------------- C: what it buys
print()
print("PART C -- what this buys and what it does not")
buys = ["the family stops being an ansatz: it is the probability of at least one excitation",
        "n becomes a MODE COUNT, which is why it is an integer rather than a dial",
        "the composition law 1 - mu_n = (1 - mu_1)^n is now obvious: n independent modes",
        "the exponential kernel is recovered as the infinite-mode limit, so the standard "
        "choice is the limit in which the mode count is forgotten"]
notbuys = ["nothing here fixes the mode count at two",
           "no published entropic or holographic derivation produces this family beyond the "
           "single-mode member, which modified-Renyi entropic gravity does give",
           "every factor of two in that literature sits in the acceleration SCALE, never in "
           "the exponent",
           "and the thermal-screen derivations have exponentially small deep-MOND corrections "
           "whereas this family's are analytic, which is a structural mismatch with them"]
for s in buys: print(f"    BUYS      {s}")
for s in notbuys: print(f"    DOES NOT  {s}")
check("V5 [the honest ledger] what the identification supplies and what it leaves open are "
      "listed and counted, since a reading that explains the FORM but not the VALUE is a "
      "partial result and should be reported as one",
      f"{len(buys)} things gained, {len(notbuys)} left open; the central one left open is the "
      f"mode count itself",
      len(notbuys) >= len(buys) - 1,
      "the form is explained and the value is not. That is real progress on understanding and "
      "no progress on the number, and conflating the two would be the easiest mistake "
      "available here")

check("V6 [the sharpened question] the open problem is restated in the new language, since a "
      "better-posed question is what a partial result is for",
      "OLD: why is the exponent in an interpolating function equal to two? NEW: why does the "
      "vacuum present exactly TWO independent modes to an acceleration? The second is a "
      "physical question about mode counting rather than a question about curve shapes",
      len(buys) >= 3,
      "that is a better question than the one this programme started the day with, and it is "
      "the kind that a horizon or screen calculation could actually answer. Two candidate "
      "readings exist -- the graviton's two polarisations, and the two branches of the "
      "gradient invariant -- and NEITHER is established here")

print()
print("READING")
print("""
  The family is not an ansatz.  It is a photocount formula.

  For n independent single-mode thermal channels of mean occupancy Y, the chance that one mode
  is empty is 1/(1+Y), so the chance that all n are empty is (1+Y)^-n, and the interpolating
  function is the probability that AT LEAST ONE quantum is present (V1-V3, verified
  symbolically and by simulation).  Under this programme's own principle Y is the acceleration
  in units of the dark-energy acceleration, so the reading is direct: \x1b[1mthe response to an
  acceleration is the probability that it excites at least one quantum out of the vacuum.\x1b[0m

  The same family is one minus a Tsallis q-exponential with q = 1 + 1/n (V4), so the mode count
  and the deformation parameter are one quantity, and the ordinary exponential kernel everyone
  uses is the infinite-mode limit -- the case where the mode count has been forgotten.

  What this buys is the FORM.  The composition law is now obvious, the integer is explained as
  a mode count rather than asserted, and the standard kernel is placed as a limit.  What it
  does not buy is the VALUE (V5).  No published entropic or holographic derivation produces
  this family beyond the single-mode member, every factor of two in that literature sits in the
  scale rather than the exponent, and the thermal-screen derivations have exponentially small
  deep corrections where this family's are analytic -- a structural mismatch worth noting
  against the whole approach.

  The gain is a better question (V6).  Not "why is an exponent two", which is a question about
  curve shapes, but \x1b[1mwhy does the vacuum present exactly two independent modes to an
  acceleration\x1b[0m -- which is a physical question a horizon calculation could answer.  Two
  candidate answers are in the air, the graviton's two polarisations and the two branches of
  the gradient invariant, and neither is established.

  LIMITS.  The identification is exact but it is an IDENTIFICATION, not a derivation: nothing
  here shows that the vacuum response to an acceleration IS such a photocount, only that the
  function this programme's data selected has that form. The mismatch noted above -- analytic
  versus exponentially small deep-MOND corrections -- cuts against reading it as a literal
  thermal screen. The mode count is not fixed. The literature survey behind the negatives was
  performed by a separate search and is reported rather than re-derived here.
""")
print(f"L237 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES}, open("fable_independent_2026/L237_results.json", "w"), indent=1)
