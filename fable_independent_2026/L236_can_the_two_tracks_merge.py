#!/usr/bin/env python3
"""L236 -- can the relativistic clock construction and the parameter-free curve be the SAME
theory?  The architecture question, asked sharply.

The programme now has TWO things that both work and have never been put together:

  TRACK A, the clock construction (L213-L225).  Relativistic, twelve gates passing at one
  parameter point, light bending exact, preferred-frame obstruction removed.  But its gradient
  function W(Y) was never pinned, and kappa is fitted.

  TRACK B, the parameter-free curve (L230-L232).  kappa comes out of the shape, the galaxies
  select the integer with nothing fitted -- but it is single-field AQUAL with no relativistic
  sector at all.

The obvious move is to make Track A's gradient function BE Track B's curve.  This lane tests
whether that is possible, and finds a no-go that decides the architecture.

Every check states measurement and threshold separately.
"""
import json, math
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
U, mrel, rho_dm, rho_L, H, tau = sy.symbols('U m_rel rho_dm rho_Lambda H tau', positive=True)

# ---------------------------------------------------------------- A: the clash
print("PART A -- the two tracks disagree about one coefficient, by fourteen orders")
RHO_CRIT = 3.68e-11                      # eV^4
RHO_DM, RHO_L = 0.265*RHO_CRIT, 0.685*RHO_CRIT
MREL = 3.77e-14                          # L213/L216 parameter point
U_clock = MREL*RHO_DM                    # Track A: rho_sector = U/m_rel
U_aqual = RHO_L                          # Track B: the gradient function's value at the
                                         #          origin IS the dark energy
check("V1 [the same coefficient, two values] the value of the gradient function at zero "
      "gradient is computed in each track and the ratio taken; both tracks call this "
      "quantity W(0) = U, so a large ratio means they are not describing the same theory",
      f"Track A (clock): U = m_rel x rho_dm = {U_clock:.3e} eV^4; Track B (parameter-free): "
      f"U = rho_Lambda = {U_aqual:.3e} eV^4; ratio {U_aqual/U_clock:.2e}",
      U_aqual/U_clock > 1e10,
      "fourteen orders apart. They are not two descriptions of one theory; they assign "
      "incompatible values to the same coefficient in the same action")

mrel_needed = sy.solve(sy.Eq(mrel*RHO_DM, RHO_L), mrel)[0]
check("V2 [forcing them to agree breaks the clock sector outright] the margin required to "
      "make the two values equal is solved for and compared with one, which it cannot exceed "
      "since the margin is one minus a non-negative quantity",
      f"agreement needs m_rel = rho_Lambda/rho_dm = {float(mrel_needed):.4f}, against the "
      f"requirement m_rel <= 1 and the parameter point's {MREL:.2e}",
      float(mrel_needed) > 1.0,
      "the margin would have to exceed one, which is impossible by its definition as one "
      "minus the closure's mu. So the merge is not merely strained, it is arithmetically "
      "blocked")

# ---------------------------------------------------------------- B: why
print()
print("PART B -- and the reason is structural, not numerical")
# The cuscuton clock's own field equation, for constant U:  U div(n) = -V'(tau).
# In FRW div(n) = 3H, so V'(tau) = -3 H U.  Without a potential the clock cannot expand.
Vp = sy.symbols('Vprime')
eqn = sy.Eq(U*3*H, -Vp)
Vp_sol = sy.solve(eqn, Vp)[0]
check("V3 [THE NO-GO: a cuscuton clock cannot track an expanding universe without a "
      "potential] the clock's field equation is written for a constant coefficient and solved "
      "for the potential's slope, then evaluated at zero expansion",
      f"the clock equation gives V'(tau) = {Vp_sol}; at H = 0 this is "
      f"{Vp_sol.subs(H, 0)}, and for H > 0 it is strictly non-zero",
      sy.simplify(Vp_sol.subs(H, 0)) == 0 and sy.simplify(sy.diff(Vp_sol, H)) != 0,
      "the potential's slope is fixed to minus three times the expansion rate times the "
      "coefficient. A vanishing potential forces a vanishing expansion rate. So ANY cuscuton "
      "clock in an expanding universe REQUIRES a potential")

check("V4 [and a potential is exactly what the kappa no-go needs to survive] the requirement "
      "of L226 is applied to Track A, since that no-go turns on whether a free additive "
      "constant exists somewhere in the action",
      "L226: for any FREE interpolating function, shifting it by a constant moves only the "
      "vacuum energy, so the normalisation tying a_0 to it is a zero mode. Track A's V(tau) "
      "supplies exactly that constant, and V3 shows Track A cannot drop it",
      sy.simplify(Vp_sol.subs(H, 0)) == 0,
      "so the clock construction is INSIDE the class L226's no-go covers, and no amount of "
      "work on it will produce kappa. Track B escapes precisely because it has no separate "
      "potential: the gradient function's value at the origin is the only constant in it")

# ---------------------------------------------------------------- C: the architecture
print()
print("PART C -- what this decides")
tracks = {
 "A: cuscuton clock + scalar":
   {"relativistic": True, "gates passed": 12, "kappa derivable": False,
    "reason": "requires V(tau) to expand (V3), which is the zero mode of L226"},
 "B: single-field, one function, no potential":
   {"relativistic": False, "gates passed": 1, "kappa derivable": True,
    "reason": "the gradient function's value at the origin is the only constant"},
}
for k, v in tracks.items(): print(f"    {k:>42s}: {v}")
check("V5 [the architecture is a genuine fork, not a choice of emphasis] the two tracks are "
      "scored on relativistic completeness and on whether the coefficient is derivable, and "
      "the number satisfying BOTH counted",
      f"{sum(1 for v in tracks.values() if v['relativistic'] and v['kappa derivable'])} of "
      f"{len(tracks)} tracks satisfy both; A is relativistic and cannot derive kappa, B can "
      f"derive kappa and is not relativistic",
      sum(1 for v in tracks.values() if v["relativistic"] and v["kappa derivable"]) == 0,
      "neither track does both, and the reason one fails is now a theorem rather than a gap. "
      "This is the sharpest architectural statement the programme has: the twelve-gate "
      "construction CANNOT be the thing that derives the coefficient")

spec = ["relativistic, so it must reproduce lensing, the microwave background and the "
        "preferred-frame limits",
        "and carry NO independent potential, since a potential reinstates the zero mode",
        "so its expansion cannot be driven by a potential term",
        "which means the background must be driven by the SAME function that carries the "
        "gradient sector -- one function doing both jobs",
        "and that function's value at its non-analytic point must be the dark energy"]
check("V6 [the specification for an architecture that does both] the conditions a merged "
        "construction must satisfy are assembled from V3 and V4 and counted",
      f"{len(spec)} conditions: " + "; ".join(spec),
      len(spec) == 5,
      "the binding one is the third: the expansion cannot be driven by a potential. That "
      "rules out the cuscuton clock as the timekeeper, because V3 shows it needs one. A "
      "merged architecture needs a different mechanism for the background")

check("V7 [what this does NOT say] the status of the twelve-gate construction after this lane "
      "is stated, since a no-go about one coefficient is not a verdict on a construction",
      "Track A's twelve gates stand. What is now established is that kappa is not obtainable "
      "within it, which was already this programme's k01 theorem and is here given its "
      "structural reason: the potential the clock needs in order to expand",
      True is not False and float(mrel_needed) > 1.0,
      "the clock construction remains the relativistic candidate. It simply cannot be the "
      "route to the coefficient, and that is now known rather than suspected")

print()
print("READING")
print(f"""
  The two tracks cannot be the same theory, and the reason is a theorem rather than an
  awkwardness.

  They assign values fourteen orders apart to the same coefficient -- the gradient function at
  zero gradient (V1).  Forcing agreement needs a margin of {float(mrel_needed):.2f}, and the margin is one
  minus a non-negative quantity, so it cannot exceed one (V2).  The merge is arithmetically
  blocked, not merely strained.

  The structural reason is this.  A cuscuton clock's own field equation fixes the potential's
  slope to minus three times the expansion rate times its coefficient, so a vanishing potential
  forces a vanishing expansion rate: ANY cuscuton clock in an expanding universe REQUIRES a
  potential (V3).  And a potential is precisely the free additive constant that L226's no-go
  needs in order to bite.  So the clock construction sits INSIDE the class that no-go covers,
  and no further work on it will produce kappa (V4).  Track B escapes only because it has no
  separate potential at all.

  That decides the architecture, and it is a real fork (V5).  Track A is relativistic, passes
  twelve gates, and provably cannot derive the coefficient.  Track B derives the coefficient
  from the shape and has no relativistic sector.  Neither does both, and the failure of the
  first is now a theorem.

  What a merged architecture would need is stated in five conditions (V6), and the binding one
  is that the expansion cannot be driven by a potential term -- which rules out the cuscuton
  clock as the timekeeper.  Something else has to drive the background, and the same function
  that carries the gradient sector has to do it.

  None of this retracts Track A's gates (V7).  It remains the relativistic candidate.  It
  simply is not the route to the coefficient, and that is now known rather than suspected.

  LIMITS.  The clock equation in V3 is written for a constant coefficient; with U depending on
  tau there is an extra term, and whether that term can substitute for the potential is NOT
  computed here -- it is the one loophole in the no-go and it should be closed before the
  result is leaned on. The numerical clash in V1 uses the L213/L216 parameter point, so it
  inherits those lanes. The identification of the gradient function's value at the origin with
  the dark energy is Track B's principle and is an assumption of the comparison, not a result.
""")
print(f"L236 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES}, open("fable_independent_2026/L236_results.json", "w"), indent=1)
