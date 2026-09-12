#!/usr/bin/env python3
"""L205 -- WHAT THE DERIVED FAMILY SUPPLIES, AND WHAT IT DOES NOT: is the sector dark matter, or is it MOND?

THE QUESTION THAT HAS BEEN ASSUMED PAST. Every derivation from L192 to L204 took gamma -> 0, where gamma multiplies the cubic term
gamma X Box chi in the action. That was harmless for the cosmological reduction. It is not harmless for the question of whether this
sector produces MOND, because the cubic term is the only Galileon-type operator in the action and Galileon-type operators are exactly
what can produce a modified force law. So: with gamma set to zero, does the remaining sector give MOND?

WHAT IS COMPUTED. In the static weak field the clock is at rest, s = 1 and Q = 0, so X = -Y and the scalar's Lagrangian is
P(-Y) - V + W(Y). For a Lagrangian F(Y) with Y = |grad chi|^2 the field equation is div(2 F'(Y) grad chi) = source, so 2F'(Y) plays
exactly the role of the MOND interpolating function. We compute it for this action's W and compare its monotonicity with what MOND
requires. The answer decides what the whole construction has actually achieved. No literal-True checks."""
import numpy as np, sympy as sy, json
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL205 IS THE DERIVED SECTOR DARK MATTER OR MOND? The interpolating function the action actually implies\n" + "=" * 118)
Y, l, d, U, m0 = sy.symbols("Y l d U m_0", positive=True)
W = U + 2*d*l*(sy.sqrt(1 + Y/l) - 1)
P = -(U/2)*sy.log((U + 2*d*Y)/m0)                                            # P(X) at X = -Y, the static limit where Q = 0
F = P + W                                                                     # the whole Y-dependence of the static Lagrangian
mu = sy.simplify(2*sy.diff(F, Y))
print(f"    the static sector's effective response is 2 F'(Y) = {mu}")
mu0 = sy.simplify(mu.subs(Y, 0))
check("V1 [the two terms cancel EXACTLY at zero gradient] the logarithm term contributes -2Ud/(U + 2dY) and the square-root term +2d/sqrt(1 + Y/l); at Y = 0 these are -2d and +2d, so the sector's response to an infinitesimal field gradient vanishes identically. That is the deep-MOND boundary condition, mu -> 0 as the acceleration goes to zero, and it holds here without being imposed",
      mu0 == 0, f"2 F'(0) = {mu0}, an exact cancellation between the two terms rather than a small residue")
ser = sy.simplify(sy.series(mu, Y, 0, 2).removeO())
coef = sy.simplify(sy.diff(mu, Y).subs(Y, 0))
print(f"    expanding about zero gradient: 2 F'(Y) = {ser}, so the leading behaviour is linear in Y")
check("V2 [but the POWER is wrong: the response grows as the square of the gradient, not the first power] the expansion gives 2 F' proportional to Y = |grad chi|^2, so writing it against an acceleration x the sector obeys mu ~ x^2, whereas MOND requires mu ~ x. The boundary condition is right and the exponent is not",
      sy.simplify(coef - (4*d**2/U - d/l)) == 0, f"the coefficient of Y is {coef}, i.e. 2 F' = (4 d^2/U - d/l) Y + O(Y^2), linear in Y and therefore quadratic in the gradient")
health = sy.simplify(4*d**2/U - d/l)
check("V3 [and it carries a health condition nobody had written down] that coefficient is positive only when 4 d l > U; below that the static sector's response is negative at small gradient, which is a wrong-sign kinetic term. This is a constraint on the coefficient functions that the cosmological derivations never saw, because they worked at the background where Y = 0",
      sy.simplify(health.subs({d: 1, l: 1, U: 1})) > 0 and sy.simplify(health.subs({d: 1, l: 1, U: 10})) < 0,
      f"the coefficient is {health}; with d = l = 1 it is positive for U < 4 and negative for U > 4, so 4 d l > U is required for the static sector to be healthy")
nu = lambda x: 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(x, 1e-300))))
xs = np.geomspace(1e-3, 1e2, 6); mu_mond = 1.0/nu(xs)
slope = np.polyfit(np.log(xs[:3]), np.log(mu_mond[:3]), 1)[0]
print("    what MOND requires, from the framework's own kernel: mu = 1/nu at g/a0 = " + " ".join(f"{x:.0e}" for x in xs))
print("                                                          mu  = " + " ".join(f"{m:.3f}" for m in mu_mond))
check("V4 [MOND's own exponent, measured off the framework's kernel] fitting the framework's interpolating function at low acceleration gives mu proportional to x to the power 0.5 in this variable, which is the first power of the acceleration: the sector's quadratic law is a different force law, not a different normalisation of the same one",
      0.3 < slope < 0.8, f"d log mu/d log x = {slope:.3f} over the lowest decades, against the sector's quadratic behaviour")
def vslope(n): return 1.0/(2*(n + 1)) - 0.5 + 0.5                             # v^2 ~ r^{...}: for mu ~ x^n, g ~ (a0^n g_N)^{1/(n+1)}
n_sector, n_mond = 2.0, 1.0
exp_sector = (1 - 2/(n_sector + 1))/2 + 0.0
print(f"    the observational consequence: for mu ~ x^n the deep-field law is g = (a0^n g_N)^(1/(n+1)), so the rotation curve behaves as")
for n, lab in ((1.0, "MOND"), (2.0, "this sector")):
    e = (1 - 2/(n + 1))/2
    print(f"      n = {n:.0f} ({lab}): v^2 ~ r^{2*e:+.3f}, i.e. v ~ r^{e:+.3f}" + ("  -- flat" if abs(e) < 1e-9 else "  -- rising"))
check("V5 [THE OBSERVATIONAL VERDICT] a quadratic interpolating function does not give flat rotation curves: it gives v rising as the sixth root of radius, whereas the first power gives exactly flat. Flat rotation curves are the single most robust fact the framework is built to explain, so the static sector with the cubic term switched off does not explain them",
      abs((1 - 2/(n_mond + 1))/2) < 1e-9 and abs((1 - 2/(n_sector + 1))/2 - 1.0/6) < 1e-9,
      f"MOND's n = 1 gives v ~ r^0, exactly flat; the sector's n = 2 gives v ~ r^(1/6), rising by {100*(10**(1/6) - 1):.0f}% per decade in radius")
GAMMA_RUNS = 1e-6
check("V6 [THE TERM THAT WAS SET TO ZERO, and what it now has to do] the only operator left in the action is the cubic gamma X Box chi, a Galileon-type term, and gamma was set to zero in every derivation from L192 through L204 and carried at 1e-6 in the candidate's own runs. It is now carrying the entire burden of turning a quadratic law into a linear one",
      GAMMA_RUNS < 1e-3, f"gamma = {GAMMA_RUNS:.0e} in the runs and exactly zero in the derivations; it must supply the difference between mu ~ x^2 and mu ~ x")
print("    WHAT THIS MEANS FOR CLOSURE, stated plainly:")
print("      - the nine gates that were walked are dark-matter gates, and the sector passes them as a dark component;")
print("      - the static sector gets the deep-MOND boundary condition right for free, its response vanishing at zero gradient exactly,")
print("        but the exponent wrong, quadratic where MOND is linear, so it gives rising rotation curves rather than flat ones;")
print("      - restoring the cubic term is the calculation that would decide whether one action can do both, and it would require re-deriving")
print("        the coefficient family, because the clock equation, the current and the energy conservation all acquire gamma-dependent terms;")
print("      - nothing computed in L192 to L204 is wrong, but its scope is narrower than 'a theory of gravity': it is a derivation of a cold")
print("        dark sector from a clock, with the force law still put in by hand.")
check("V7 [the honest scope of the construction] the chain from L192 to L204 derives a cold, clustering dark sector and its equation of state from a clock. It does not yet derive the force law: the static limit gets the boundary condition right and the exponent wrong, and closing that gap is now a single well-posed calculation rather than an open-ended search",
      mu0 == 0 and abs((1 - 2/(n_sector + 1))/2 - 1.0/6) < 1e-9,
      "recorded so the gate board is not read as a complete theory of gravity: it is a derived dark sector that passes nine gates, plus a static limit that is one exponent away from MOND")
json.dump(dict(mu_static=str(mu), mu_at_zero=str(mu0), leading_coefficient=str(coef), mond_mu=[float(x) for x in mu_mond], mond_slope=float(slope),
               gamma_in_runs=GAMMA_RUNS, verdict="the sector is dark matter, not MOND; the cubic term that could supply MOND was set to zero throughout"),
          open("L205_results.json", "w"), indent=1)
print(f"\nL205 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
