#!/usr/bin/env python3
"""L219 -- the effective theory's ultraviolet cutoff.

L218 showed the criticality window's existence turns on kappa = k/H at the shortest scale
the instability acts on, and that the programme has never determined it.  L217 makes it
determinable: the closure is a single logarithmic kinetic function

    P(X) = -(U/2) log(U - 2 d X),

so EVERY derivative is fixed, the expansion parameter is known with no freedom, and the
breakdown scale is the remaining distance to the speed limit.  This lane computes it, gets
a number, and finds that the number withdraws L218's headline.

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
X, U, dd, q = sy.symbols('X U d qbar', positive=True)
m = U - 2*dd*X
P = -(U/2)*sy.log(m)

# ------------------------------------------------------------------ A: the expansion parameter
print("PART A -- the expansion parameter, with no freedom left")
derivs = [sy.simplify(sy.diff(P, X, n)) for n in range(1, 6)]
pred = [sy.simplify(sy.factorial(n-1)*(2*dd/m)**(n-1)*U*dd/m) for n in range(1, 6)]
agree = all(sy.simplify(a - b) == 0 for a, b in zip(derivs, pred))
check("V1 [the logarithm fixes every derivative] the first five derivatives of the kinetic "
      "function are computed and compared term by term with the closed form "
      "(n-1)! (2d/m)^(n-1) U d/m",
      f"P^(1..5) match the closed form: {agree}; ratio P'''/P'' = "
      f"{sy.simplify(derivs[2]/derivs[1])}, P''/P' = {sy.simplify(derivs[1]/derivs[0])}",
      agree,
      "successive derivatives grow by 2d/m, 4d/m, 6d/m: the expansion parameter of the "
      "theory is exactly (2d/m) times the excursion in X, with no coefficient left free. "
      "This is what makes the cutoff calculable rather than assumed")

dX_max = sy.simplify(sy.solve(sy.Eq((2*dd/m)*sy.Symbol('dX', positive=True), 1),
                              sy.Symbol('dX', positive=True))[0])
Xstar = U/(2*dd)
frac = sy.simplify(dX_max/Xstar)
check("V2 [and the breakdown is the remaining distance to the speed limit] the excursion at "
      "which the expansion parameter reaches one is solved for, and expressed as a fraction "
      "of the speed-limit invariant",
      f"dX_max = {dX_max}, X* = {Xstar}, dX_max/X* = {sy.simplify(frac)} = m/U = m_rel",
      sy.simplify(frac - m/U) == 0,
      "the theory breaks down exactly when a fluctuation moves the field the remaining "
      "distance to its own speed limit. That is what a speed limit always does, and it is "
      "why a small margin means a low cutoff")

# ------------------------------------------------------------------ B: convert to a momentum
print()
print("PART B -- converting the field-space distance into a momentum")
A_quad = sy.simplify(sy.diff(P, X) + 2*X*sy.diff(P, X, 2))
cs2 = sy.simplify(sy.diff(P, X)/A_quad)
mrel_s = sy.Symbol('m_rel', positive=True)
cs2_closed = sy.simplify(cs2.subs(X, (U - mrel_s*U)/(2*dd)))
check("V3 [the quadratic action, from the same function] the coefficients of the squared "
      "time derivative and of the gradient are formed from the kinetic function and their "
      "ratio taken, then written in terms of the margin",
      f"A = P_X + 2 X P_XX = {A_quad}, c_s^2 = P_X/A = {cs2}, "
      f"= {cs2_closed} in terms of the margin",
      sy.simplify(cs2_closed - mrel_s/(2 - mrel_s)) == 0,
      "the scalar's own sound speed is m_rel/(2 - m_rel), so a field close to its speed "
      "limit is also a field with a tiny sound speed. Both effects lower the cutoff and "
      "both are now fixed by one number")

# fluctuation of physical momentum k: delta_chi ~ k/(2 pi sqrt(2 A c_s)), delta_X ~ 2 qbar c_s k delta_chi
k = sy.Symbol('k', positive=True)
cs = sy.sqrt(mrel_s/2)
A_small = sy.simplify(2*U**2*dd/(mrel_s*U)**2)                   # A with m = m_rel U, m << U
dchi = k/(2*sy.pi*sy.sqrt(2*A_small*cs))
dX_of_k = sy.simplify(2*q*cs*k*dchi)
k_sol = sy.solve(sy.Eq(sy.simplify((2*dd/(mrel_s*U))*dX_of_k), 1), k)
k_max = sy.simplify([s for s in k_sol if s.is_positive][0].subs(dd, U/(2*q**2)))
check("V4 [the cutoff momentum] the fluctuation amplitude at physical momentum k is formed, "
      "the excursion it produces is set equal to the breakdown excursion of V2, the result "
      "is solved for k, and its dependence on the scalar's velocity is measured",
      f"k_max = {k_max}, d k_max/d qbar = {sy.simplify(sy.diff(k_max, q))}",
      sy.simplify(sy.diff(k_max, q)) == 0,
      "the scalar's velocity cancels, which matters because it was never determined. The "
      "cutoff is fixed by the clock coefficient and the margin alone: "
      "k_max^2 = pi sqrt(2) sqrt(U) (2/m_rel)^(1/4)")

# ------------------------------------------------------------------ C: the number
print()
print("PART C -- the number, and what it does to L218")
rho_d = 9.75e-12          # eV^4, the cold sector today
W_CEIL, S0 = 5.66e-7, 1.5e7
mrel_v = W_CEIL/(S0 - 1)
U_v = mrel_v*rho_d
k_max_v = float((sy.pi*sy.sqrt(2)).evalf())**0.5 * U_v**0.25 * (2.0/mrel_v)**0.125
length_m = 1.0/(k_max_v*5.068e6)                                  # 1 eV^-1 = 1.973e-7 m
H0_eV, H3_over_H0 = 1.437e-33, 4.568
kappa_max = k_max_v/(H0_eV*H3_over_H0)
check("V5 [the cutoff, in units a person can picture] the cutoff momentum is evaluated at "
      "the margin the solar system and the flat law together force, converted to a length, "
      "and compared with a micron to check it is a laboratory scale rather than a Planckian "
      "or a cosmological one",
      f"m_rel = {mrel_v:.2e}, U = {U_v:.3e} eV^4, k_max = {k_max_v:.3e} eV, "
      f"length 1/k_max = {length_m*1e3:.2f} mm",
      length_m > 1e-6,
      "a cutoff at millimetres. That is the familiar scale of dark-sector effective "
      "theories built on the dark energy density, and it is reached here from the margin "
      "rather than assumed")

KAPPA_FOREST = 3.2e4
margin = kappa_max/KAPPA_FOREST
check("V6 [and it clears the forest requirement by an enormous margin] the cutoff expressed "
      "as kappa at the forest epoch is divided by the kappa the forest demands, and the "
      "ratio compared against 1",
      f"kappa_max(z=3) = {kappa_max:.3e} against the forest's {KAPPA_FOREST:.1e}; "
      f"margin = {margin:.2e}, i.e. {sy.log(margin, 10).evalf():.0f} orders",
      margin > 1.0,
      "twenty-three orders of margin. Nothing about the forest gate or the residual was "
      "ever close to the cutoff, so L194's 'sub-Mpc scales are enormously larger than any "
      "cutoff of this effective theory' is now a computed statement rather than an assertion")

kappa_rec = kappa_max*0.05335                                     # (aH)_3/(aH)_1100, L218
floor_true = 2.0/kappa_rec**2
floor_L218 = 1.48e-8
check("V7 [L218 V4 CORRECTED -- the two-sided window is withdrawn] the criticality floor is "
      "re-evaluated at the ACTUAL cutoff rather than at the forest's minimum kappa, and "
      "compared with the floor L218 reported",
      f"floor at the true cutoff = {floor_true:.2e}, against L218's {floor_L218:.2e}; "
      f"lower by {floor_L218/floor_true:.1e}",
      floor_true < floor_L218,
      "L218 computed its floor at the SMALLEST kappa the forest tolerates, not at the "
      "cutoff. At the cutoff the floor collapses by forty-five orders, so criticality "
      "imposes no practical lower bound and w is bounded from ABOVE only. L218's headline, "
      "the first two-sided determination of w, is WITHDRAWN")

# ------------------------------------------------------------------ D: the cost
print()
print("PART D -- what the high cutoff costs")
resid_true = 1.0/kappa_max**2
rate_at_cutoff = 2*kappa_max*(W_CEIL/2)**0.5
check("V8 [the residual is now entirely a cutoff quantity] the residual sound speed is "
      "evaluated at the true cutoff and compared with the forest's requirement of 1e-9, and "
      "the instability's growth rate at that same scale is evaluated in e-folds",
      f"residual c_s^2 = {resid_true:.2e} vs forest 1e-9; growth rate at the cutoff = "
      f"{rate_at_cutoff:.2e} per e-fold",
      resid_true < 1e-9 and rate_at_cutoff > 1.0,
      "the sector ends up colder than any measurement could register, but the number is set "
      "by the shortest scale in the theory and by nothing in the action. And at that scale "
      "the instability grows 1e25 times per e-fold, which is the effective theory failing "
      "at its own cutoff exactly as it should. So the coldness is a genuine prediction of "
      "the MECHANISM and not a calculable number within the EFT: L194's 'nothing has to be "
      "tuned' stands, and its price is that the value is not computable here")

for fac, label in [(1e6, "a million"), (1e12, "a million million")]:
    m2 = (kappa_max/fac**0.5)/KAPPA_FOREST
    print(f"    if the fluctuation amplitude is wrong by {label}: margin still {m2:.1e}")
check("V9 [and the verdict is robust to the one soft step] the cutoff is recomputed with the "
      "fluctuation amplitude wrong by a factor of a million million, and the remaining "
      "margin over the forest requirement is compared against 1",
      f"margin with an amplitude error of 1e12 = {(kappa_max/1e6)/KAPPA_FOREST:.1e}",
      (kappa_max/1e6)/KAPPA_FOREST > 1.0,
      "the only convention-sensitive step is the size of a fluctuation at momentum k, and "
      "the conclusion survives an error of twelve orders there. The verdict does not rest "
      "on that step")

print()
print("READING")
print("""
  The cutoff is a millimetre, and it is high enough to withdraw L218's headline.

  L217's logarithm did more than explain the clock rate.  Because the closure is ONE
  function, every derivative is fixed and the expansion parameter of the theory is exactly
  (2d/m) times the excursion in X, with nothing free (V1).  The theory therefore breaks down
  when a fluctuation moves the field the remaining distance to its own speed limit (V2) --
  which is what a speed limit always does, and which is why a small margin means a low
  cutoff.  Converting that field-space distance into a momentum, using the quadratic
  normalisation and sound speed that the SAME function fixes (V3), the scalar's velocity
  cancels and

      k_max^2  =  pi sqrt(2) sqrt(U) (2/m_rel)^(1/4)  ,

  free of the one quantity the programme never determined (V4).  At the margin the solar
  system and the flat law together force, that is 8.5e-5 eV, a length of 2.3 millimetres
  (V5) -- the familiar scale of dark-sector effective theories, reached here from the margin
  rather than assumed.

  Expressed as kappa it is 1.3e28 at the forest epoch, twenty-three orders above what the
  forest needs (V6).  And that withdraws L218's headline.  L218 computed its lower bound on
  w at the SMALLEST kappa the forest tolerates rather than at the cutoff; at the cutoff the
  floor collapses by forty-five orders (V7).  Criticality imposes no practical lower bound,
  and w is bounded from ABOVE only.  The first two-sided determination of w is withdrawn.

  The high cutoff has a price.  The residual coldness is 1/kappa^2 = 6e-57, set by the
  shortest scale in the theory and by nothing in the action, and at that scale the
  instability grows 1e25 times per e-fold, which is the effective theory failing at its own
  cutoff as it should (V8).  So the sector's coldness remains a genuine prediction of the
  MECHANISM -- L194's 'nothing has to be tuned' stands -- but its numerical value is not
  computable inside this effective theory.  That is a real limitation and it is stated as
  one.

  LIMITS.  The one convention-sensitive step is the amplitude of a fluctuation at momentum
  k; the verdict survives an error of twelve orders there (V9), so it does not rest on that
  step.  The excursion is estimated from the time-derivative piece of X alone, taking the
  gradient piece to be no larger.  The cutoff is evaluated at today's coefficient values and
  its evolution is not computed.  The margin m_rel = 3.8e-14 comes from L216's clock rate
  and L217's ceiling, so every limit of those lanes is inherited.  Nothing here addresses
  the strong-coupling question L216 raised, which is about the SCALAR's kinetic coefficient
  rather than about the cutoff.  a_0 does not enter, so the result is the same on both
  footings and is quoted once.
""")
print(f"L219 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("fable_independent_2026/L219_results.json", "w"), indent=1)
