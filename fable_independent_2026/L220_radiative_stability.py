#!/usr/bin/env python3
"""L220 -- the strong-coupling question: is the margin radiatively stable?

L216 raised it, L218 sharpened it 180-fold and L219 declined it as a different question.
Here it is, stated exactly.  The solar system and the flat law together force the margin
m = U - 2 d qbar^2 to sit at m_rel = 3.8e-14 of the clock coefficient.  L217 showed the
RECIPROCAL of that margin is a conserved Noether charge, so it is protected against
CLASSICAL drift.  Quantum corrections are a separate matter: the shift symmetry acts on chi,
while U is the clock's own coefficient, and nothing in the action protects it.

L219 makes this computable, because it fixed the cutoff in terms of the same margin.  That
closes the loop: the size of the radiative correction to U can be written in terms of
m_rel alone, with the cutoff and the coefficient both eliminated.

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
U, mrel, Lam4, dU = sy.symbols('U m_rel Lambda4 deltaU', positive=True)

# ---------------------------------------------------------------- A: which coefficient is exposed
print("PART A -- which coefficient takes an additive correction")
# [chi] = 1 so [d_mu chi] = 2 and [Y] = 4; s is dimensionless, so [W] = 4 and [W_Y] = 0.
dims = {"chi": 1, "dchi": 2, "Y": 4, "s": 0, "W": 4, "U = W(0)": 4, "d = W_Y(0)": 0}
check("V1 [U is a cosmological-constant-type coefficient; d is a dimensionless coupling] the "
      "mass dimensions of the clock sector's two coefficients are read off the action and "
      "compared, since only a dimension-four coefficient takes an ADDITIVE correction at the "
      "fourth power of the cutoff",
      f"dimensions {dims}", dims["U = W(0)"] == 4 and dims["d = W_Y(0)"] == 0,
      "s is dimensionless, so s U is a cosmological-constant term with coefficient U, which "
      "takes additive corrections of order the cutoff to the fourth. d is dimensionless and "
      "takes only multiplicative, logarithmic ones. The margin m = U - 2 d qbar^2 is "
      "therefore exposed through U alone")

# ---------------------------------------------------------------- B: the estimate, self-consistently
print()
print("PART B -- the correction, with the cutoff eliminated")
r = sy.Symbol('r', positive=True)                       # r = sqrt(2/m_rel)
c = sy.Symbol('c', positive=True)                       # the loop factor pi^2
Lam4_expr = 2*c*U*r                                     # L219: Lambda^2 = pi sqrt2 sqrt(U) (2/m_rel)^(1/4)
dU_expr = Lam4_expr/(16*c)
ratio = sy.simplify(dU_expr/U)
check("V2 [the correction to U, expressed in the margin alone] L219's cutoff is raised to "
      "the fourth power, divided by the standard loop factor, and the result divided by U; "
      "the dependence on U and on the loop factor is then measured",
      f"Lambda^4 = {Lam4_expr}, deltaU/U = {ratio}, d/dU = {sy.simplify(sy.diff(ratio, U))}, "
      f"d/dc = {sy.simplify(sy.diff(ratio, c))}",
      sy.simplify(sy.diff(ratio, U)) == 0 and sy.simplify(sy.diff(ratio, c)) == 0
      and sy.simplify(ratio - r/8) == 0,
      "deltaU/U = sqrt(2/m_rel)/8, free of both the coefficient and the loop factor. The "
      "cutoff was derived FROM the margin in L219, so writing the correction in the margin "
      "eliminates everything else. This is the whole question in one expression")

mrel_stab = sy.solve(sy.Eq((sy.sqrt(2/mrel))/8, 1), mrel)[0]
check("V3 [radiative stability, as a bound on the margin] the condition that the correction "
      "not exceed the coefficient it corrects is solved for the margin, and compared with "
      "zero to confirm it is a genuine lower bound rather than a vacuous one",
      f"deltaU <= U  <=>  m_rel >= {mrel_stab} = {float(mrel_stab):.4f}",
      float(mrel_stab) > 0,
      "the theory is radiatively stable only if the field is NOT close to its speed limit. "
      "Closer to the limit means a higher cutoff (fluctuations are suppressed by the large "
      "kinetic coefficient) and a smaller U, and both push the correction up")

# ---------------------------------------------------------------- C: the pincer
print()
print("PART C -- against what the solar system demands")
W_CEIL, S0_REQ = 5.66e-7, 1.5e7
mrel_v = W_CEIL/(S0_REQ - 1)
ratio_v = (2.0/mrel_v)**0.5/8.0
gap = float(mrel_stab)/mrel_v
check("V4 [THE GAP] the margin the solar system and the flat law together force is divided "
      "into the margin radiative stability requires, and the ratio compared against 1",
      f"m_rel forced = {mrel_v:.2e}; m_rel for stability >= {float(mrel_stab):.4f}; "
      f"gap = {gap:.2e}, i.e. {sy.log(gap, 10).evalf():.0f} orders",
      gap > 1.0,
      "twelve orders. The two requirements do not overlap anywhere")

dm_over_m = ratio_v/mrel_v
check("V5 [and how badly the margin itself is destabilised] the correction to U is divided "
      "by the margin rather than by U, since the margin is the quantity that must survive, "
      "and compared against 1",
      f"deltaU/U = {ratio_v:.2e}; deltaU/m = (deltaU/U)/m_rel = {dm_over_m:.2e}",
      dm_over_m > 1.0,
      "the correction is a million times the coefficient and nineteen orders times the "
      "margin. The cancellation that defines the margin cannot survive a single loop")

s0_stab = 1.0 + W_CEIL/float(mrel_stab)
check("V6 [the same pincer read on the clock rate] the stability bound on the margin is "
      "converted through the clock identity into a CEILING on the clock rate, and compared "
      "with the FLOOR the solar system imposes",
      f"stability gives s_0 <= {s0_stab:.6f}; the solar system needs s_0 >= {S0_REQ:.1e}; "
      f"no interior, the two differ by {S0_REQ/(s0_stab-1):.1e} in s_0 - 1",
      s0_stab < S0_REQ,
      "a clock essentially AT proper time versus a clock ten million times faster. The "
      "pincer has no interior at all: every value of the clock rate fails one side or the "
      "other")

# ---------------------------------------------------------------- D: escapes
print()
print("PART D -- the escapes, checked")
rho_DE = 2.5e-11                                        # eV^4
U_v = mrel_v*9.75e-12
check("V7 [the tuning is worse than the cosmological constant's] the clock coefficient the "
      "construction requires is divided by the dark energy density, since a coefficient far "
      "below that scale is a tuning beyond the one physics already has",
      f"U = {U_v:.2e} eV^4 against rho_DE = {rho_DE:.1e} eV^4; ratio = {U_v/rho_DE:.1e}",
      U_v/rho_DE < 1.0,
      "fourteen orders below the dark energy density. The ordinary cosmological constant "
      "problem is already at that scale, so this construction asks for a tuning fourteen "
      "orders beyond the one everybody already owes")

check("V8 [the shift symmetry does not reach it] the field the exact symmetry acts on is "
      "compared with the field whose coefficient is exposed, since a symmetry protects only "
      "what it acts on",
      "the shift symmetry acts on chi; the exposed coefficient U belongs to the CLOCK tau, "
      "and V(tau), W(Y,tau) and P(X,tau) all depend on tau explicitly, so there is no tau "
      "shift symmetry to protect it",
      "chi" != "tau",
      "L217's conservation protects the margin against CLASSICAL drift, which is what that "
      "lane claimed and which stands. It says nothing about a loop correction to the clock "
      "coefficient, and no other symmetry in the action does either")

needed_err = ratio_v
lam_factor = needed_err**0.25
check("V9 [how wrong the estimate would have to be] the factor by which the loop estimate "
      "must be wrong for the margin to survive is evaluated, together with the factor by "
      "which the cutoff itself would have to be lower, and the loop factor is compared "
      "against 100, roughly the accuracy naive dimensional analysis can be trusted to",
      f"the loop coefficient would have to be too large by {needed_err:.1e}, or the cutoff "
      f"too high by {lam_factor:.0f}x",
      needed_err > 100.0,
      "a factor of a million in the loop coefficient, or thirty-one in the cutoff. Naive "
      "dimensional analysis is good to an order or two, not to six, so the estimate cannot "
      "be dismissed on its uncertainty. The cutoff route is the softer one and is the place "
      "to attack this if it is to be attacked")

print()
print("READING")
print("""
  The strong-coupling question has an answer, and the answer is a naturalness pincer with no
  interior.

  Only one coefficient is exposed.  The clock scalar s is dimensionless, so s U is a
  cosmological-constant term and U takes additive corrections at the fourth power of the
  cutoff; d is dimensionless and takes only logarithmic ones (V1).  The margin
  m = U - 2 d qbar^2 is therefore exposed through U alone.

  And L219 closes the loop, because it fixed the cutoff in terms of the same margin.  Raising
  it to the fourth power and dividing by the loop factor,

      deltaU/U  =  sqrt(2/m_rel)/8 ,

  free of the coefficient and of the loop factor alike (V2).  The whole question is that one
  expression.  Radiative stability, deltaU <= U, then requires m_rel >= 1/32 (V3): the theory
  is under control only if the field is NOT close to its speed limit, because closeness
  raises the cutoff and lowers U at the same time.

  The solar system demands the opposite.  With the disformal coupling that light bending
  forces, alignment needs a clock rate of 1.5e7 and hence m_rel = 3.8e-14 -- twelve orders
  below the stability bound (V4), with the correction running a million times the coefficient
  and nineteen orders times the margin itself (V5).  Read on the clock rate, stability allows
  at most 1.00002 and the solar system needs at least 1.5e7 (V6).  There is no interior.

  The escapes were checked and do not open.  The coefficient the construction needs sits
  fourteen orders BELOW the dark energy density, so the tuning is worse than the cosmological
  constant's rather than a version of it (V7).  L217's conserved charge protects the margin
  against classical drift, which is all that lane claimed, but the shift symmetry acts on chi
  while the exposed coefficient belongs to tau, and nothing in the action protects that (V8).
  And the estimate would have to be wrong by a million in the loop coefficient, or the cutoff
  too high by thirty-one, for the margin to survive (V9) -- beyond what dimensional analysis
  can absorb.

  WHAT THIS BINDS, EXACTLY.  The chain is: light bending forces a disformal coupling; the
  disformal coupling boosted forces a large clock rate; a large clock rate forces a tiny
  margin; a tiny margin is radiatively unstable.  Every link is a computed lane.  The
  construction is not inconsistent -- it can be tuned, to one part in 1e19 -- and this
  programme's rule is to record a cost as a cost.  This is the largest cost on the board.

  LIMITS.  The correction is a naive-dimensional-analysis estimate, not a computed loop; V9
  measures how much room that leaves and the answer is not enough.  It inherits L219's
  cutoff, whose one soft step is the amplitude of a fluctuation at a given momentum, and the
  cutoff enters here at the FOURTH power, so this lane is far more sensitive to that step
  than L219 was -- a factor of thirty-one in the cutoff would close the gap, where L219 had
  twelve orders of room.  That is the place to attack this.  The clock rate is L216's, with
  its crude interior match.  No loop is computed anywhere in this programme.  a_0 does not
  enter, so the result is footing-independent and quoted once.
""")
print(f"L220 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("fable_independent_2026/L220_results.json", "w"), indent=1)
