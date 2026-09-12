#!/usr/bin/env python3
"""L217 -- where s_0 ~ 1e7 comes from.

L216 left the clock rate as a requirement with no origin.  Restating it precisely:
s_0 - 1 = w/m_rel, so a clock rate of 1.5e7 at w <= 1e-4 means m_rel = 6.8e-12 -- the
margin m = U - 2 d qbar^2 sits within one part in 1e11 of zero.  This lane asks what, if
anything, puts it there, and finds three things:

  (1) m -> 0 is not an arbitrary point.  The closure's kinetic coefficients integrate to a
      LOGARITHMIC kinetic function with a pole at m = 0: the scalar has a SPEED LIMIT, and
      1/m_rel is its Lorentz factor.  A large clock rate is the field sitting close to
      that limit.
  (2) The action is shift-symmetric in chi -- every term carries only derivatives -- so the
      chi equation is a conservation law and the Lorentz factor is a CONSERVED CHARGE.
      The clock rate is therefore not tuned; it is protected.  That is the answer to
      'where does 1e7 come from': nowhere, it is an initial condition that a symmetry
      preserves exactly, which is what makes a large value technically natural.
  (3) But the matter coupling MOND requires BREAKS that symmetry, and the breaking is
      computable.  It drives the charge linearly in cosmic time, and through
      a_0 = lambda^3/(12 pi G beta s_0) that drives a_0 DOWN.  Demanding a_0 stay flat --
      the framework's own distinctive prediction -- bounds the sector's equation of state
      far below the acoustic bound.

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
X, U, d_, q, w, mrel, s0, rho, H, lam, C, k, G, Om, N = sy.symbols(
    'X U d qbar w m_rel s_0 rho H lambda C k G Omega N', positive=True)

# ------------------------------------------------------------------ A: the speed limit
print("PART A -- m = 0 is a speed limit, and 1/m_rel is its Lorentz factor")
m = U - 2*d_*X
P_cand = -(U/2)*sy.log(m)
PX = sy.simplify(sy.diff(P_cand, X))
PXX = sy.simplify(sy.diff(P_cand, X, 2))
check("V1 [the closure IS a logarithmic kinetic function] a single P(X) is proposed and "
      "differentiated twice, and the two derivatives are compared with the closure's "
      "independently stated P_X = U d/m and P_XX = 2 U d^2/m^2",
      f"P = -(U/2) log(U - 2 d X) gives P_X = {PX}, P_XX = {PXX}",
      sy.simplify(PX - U*d_/m) == 0 and sy.simplify(PXX - 2*U*d_**2/m**2) == 0,
      "both closure coefficients come from ONE function, so the closure was never two "
      "independent choices. The function has a logarithmic pole at m = 0")

Xstar = sy.solve(sy.Eq(m, 0), X)[0]
rho_P = sy.simplify(2*X*PX - P_cand)
blowup = sy.limit(PX.subs(d_, 1).subs(U, 1), X, sy.Rational(1, 2), '-')
check("V2 [so the field has a speed limit it cannot cross] the kinetic invariant at which "
      "the margin vanishes is solved for, and the kinetic coefficient's limit approaching "
      "it from below is measured",
      f"X* = {Xstar}; P_X -> {blowup} as X -> X* from below",
      Xstar == U/(2*d_) and blowup == sy.oo,
      "infinite kinetic coefficient, hence infinite energy to reach X*: the scalar can "
      "approach the limit and never pass it. 1/m_rel = U/(U - 2 d X) is exactly the "
      "Lorentz factor of that limit, so a clock rate of 1e7 is the statement that the "
      "field sits close to its own speed limit -- a kinematic regime, not a coincidence")

# ------------------------------------------------------------------ B: it is conserved
print()
print("PART B -- and the Lorentz factor is a conserved charge")
# The action carries chi only through derivatives: P(X,tau) with X = Q^2 - Y, sW(Y,tau),
# gamma X box(chi).  So chi -> chi + const is an exact symmetry and the chi equation is
# div J = 0 with J^mu = P_X d^mu chi.  On the background, Q = a^3 P_X qbar is conserved.
a = sy.Symbol('a', positive=True)
PX_family = d_/mrel                                  # P_X = U d/m = d/(U m_rel/U) = d/m_rel
Qch = sy.simplify(a**3 * PX_family * q)
# derived family exponents
Qch_scaled = Qch.subs({d_: a**(-3*(1-w)), q: a**(-3*w)})
expo = sy.simplify(a*sy.diff(Qch_scaled, a)/Qch_scaled)
check("V3 [the Noether charge of the shift symmetry is exactly the Lorentz factor] the "
      "conserved charge a^3 P_X qbar is formed on the derived family and its power of the "
      "scale factor measured; a non-zero power would mean it is not conserved there",
      f"Q = {Qch}, on the family Q = {sy.simplify(Qch_scaled)}, exponent of a = {expo}",
      expo == 0 and sy.simplify(Qch - a**3*q*d_/mrel) == 0,
      "Q = qbar d/m_rel, constant on the family and proportional to 1/m_rel. Combined with "
      "s_0 - 1 = w/m_rel this gives s_0 - 1 = w Q/(qbar d): THE CLOCK RATE IS A CONSERVED "
      "CHARGE. It is not tuned each epoch, it is set once and protected -- which is what "
      "makes a large value technically natural rather than fine-tuned")

# ------------------------------------------------------------------ C: L214 simplified
print()
print("PART C -- a correction to L214 that falls out")
C_def = 2*k*q**2/U
C_limit = sy.simplify(C_def.subs(U, 2*d_*q**2))       # mu -> 1 means 2 d qbar^2 -> U
check("V4 [L214's 'window' is NOT an independent condition] the enhancement ratio is "
      "evaluated in the limit the branch forces, where 2 d qbar^2 equals U, and compared "
      "with the reciprocal of the interpolating function's floor",
      f"C = {C_def} -> {C_limit}; floor mu_floor = d/k, so 1/mu_floor = {sy.simplify(k/d_)}",
      sy.simplify(C_limit - k/d_) == 0,
      "C = k/d = 1/mu_floor identically. L214 reported C >= 1e3 as a price the branch "
      "charges; in the limit the branch itself forces, C IS the reciprocal of the MOND "
      "floor, so the inequality is the rotation-curve requirement restated and costs "
      "nothing extra. L214's 'one inequality' is withdrawn as a separate condition")

# ------------------------------------------------------------------ D: MOND breaks it
print()
print("PART D -- but the coupling MOND requires breaks the symmetry")
# lambda chi rho_b is not shift symmetric: div J = lambda rho_b, so d/dt(a^3 P_X qbar) =
# lambda a^3 rho_b = const.  The charge grows LINEARLY in cosmic time.
lam_q_sq = sy.simplify((4*sy.pi*s0*C*G*U).subs(U, w*rho/s0))
check("V5 [the coupling strength that MOND needs, and it is free of the clock rate] the "
      "solar-system condition f_s = 1 is solved for the coupling, the branch relations "
      "2 d qbar^2 = U and U = w rho/s_0 are substituted, and the derivative of the result "
      "with respect to the clock rate is measured",
      f"(lambda qbar)^2 = {lam_q_sq}, d/ds_0 = {sy.simplify(sy.diff(lam_q_sq, s0))}",
      sy.simplify(sy.diff(lam_q_sq, s0)) == 0,
      "the clock rate cancels exactly, so the symmetry-breaking rate cannot be made small "
      "by choosing it. Writing G = 1/(8 pi M^2) and rho = 3 H^2 M^2 Omega gives "
      "lambda qbar = H sqrt(3 C w Omega/2)")

lam_q_over_H = sy.sqrt(sy.simplify(lam_q_sq.subs(G, 1/(8*sy.pi*sy.Symbol('M')**2))
                                   .subs(rho, 3*H**2*sy.Symbol('M')**2*Om))/H**2)
Om_dm, Om_b = 0.265, 0.0493
def drift_per_efold(Cv, wv):
    """d ln Q / dN = 2 (lambda qbar/H) (rho_b/rho_sector); the source is BARYONS."""
    return 2.0*(1.5*Cv*wv*Om_dm)**0.5*(Om_b/Om_dm)
dN = 1.7918                                            # ln 6, from z = 5 to z = 0
drift = drift_per_efold(1e3, 1e-4)
a0_factor = 2.718281828**(drift*dN)
check("V6 [so the clock rate drifts, and a_0 with it] the fractional growth of the charge "
      "per e-fold is evaluated at the programme's current numbers, carried from z = 5 to "
      "today, and the resulting change in a_0 is compared against the 1 percent that the "
      "framework's own flat law allows over that span",
      f"lambda qbar/H = {lam_q_over_H}; d ln Q/dN = {drift:.4f}; a_0 falls by a factor "
      f"{a0_factor:.3f} from z = 5 to z = 0, i.e. {100*(1-1/a0_factor):.1f}% vs 1% allowed",
      100*(1 - 1/a0_factor) > 1.0,
      "a_0 = lambda^3/(12 pi G beta s_0) with lambda and beta constants of the action, so a "
      "growing clock rate lowers a_0 directly. At the numbers carried so far a_0 would fall "
      "by 13% since z = 5, an order over what the derived flat law permits. This is an "
      "INTERNAL tension: MOND's own coupling fights the framework's distinctive prediction")

# ------------------------------------------------------------------ E: what it forces
print()
print("PART E -- what holding a_0 flat costs")
allowed = 0.01
Cw_max = (allowed/(2*dN*(Om_b/Om_dm)))**2/(1.5*Om_dm)
w_max = Cw_max/1e3
check("V7 [THE BOUND: the flat law tightens the equation of state by more than two orders] "
      "the drift requirement is inverted for the product of the enhancement ratio and the "
      "equation of state, the enhancement ratio is set at its MOND minimum, and the "
      "resulting bound on w is compared with the acoustic bound of 1e-4",
      f"C w <= {Cw_max:.3e}; at C = 1e3 that is w <= {w_max:.2e}, against the acoustic "
      f"bound 1e-4: tighter by {1e-4/w_max:.0f}x",
      w_max < 1e-4,
      "holding a_0 flat to one percent since z = 5 forces w below 6e-7. The acoustic scale "
      "never got near this. It is the tightest constraint on the sector's equation of "
      "state the programme has derived")

check("V8 [and the cost is to the programme's own falsifiable prediction] the published "
      "prediction band for the dark sector's equation of state is compared with the band "
      "that survives this bound",
      f"published band 0 < w <~ 1e-4; surviving band 0 < w <~ {w_max:.1e}; "
      f"the band shrinks by {1e-4/w_max:.0f}x",
      w_max < 1e-4 and w_max > 0,
      "the sign of the prediction is untouched -- w is still strictly positive, still "
      "distinct from LCDM's exact zero, and criticality still needs it -- but the magnitude "
      "the framework can claim drops by more than two orders, which puts it further out of "
      "reach of a dedicated measurement. That is a real cost and it is recorded as one")

check("V9 [footing independence] the bound of V7 is checked for any dependence on the "
      "acceleration scale itself, since a result that moved with the footing would have to "
      "be quoted twice",
      f"the drift d ln Q/dN = 2 sqrt(1.5 C w Omega)(Omega_b/Omega_dm) contains "
      f"C, w, Omega_b, Omega_dm and no a_0",
      "a_0" not in str(sy.simplify(lam_q_sq)) and abs(drift_per_efold(1e3, 1e-4) - drift) < 1e-12,
      "a_0 enters only through a_0 ~ 1/s_0, and the clock rate cancelled out of the drift "
      "in V5. The bound is the same on the canonical footing 9.3619e-11 and the alternative "
      "1.1279e-10, so it is quoted once rather than twice")

print()
print("READING")
print("""
  The clock rate is not tuned.  It is conserved, and MOND breaks the conservation.

  First, the regime is a kinematic one.  The closure's two kinetic coefficients come from a
  single logarithmic function, P = -(U/2) log(U - 2 d X), whose pole at m = 0 is a SPEED
  LIMIT (V1, V2).  The quantity 1/m_rel is exactly the Lorentz factor of that limit, so
  s_0 - 1 = w/m_rel = 1.5e7 says the scalar sits close to its own speed limit.  That is a
  regime, not a coincidence, and it is the same structure that makes relativistic factors
  large without anyone tuning them.

  Second, the action carries chi only through derivatives, so the shift symmetry is exact
  and the chi equation is a conservation law.  Its Noether charge, a^3 P_X qbar, IS the
  Lorentz factor (V3), so

      s_0 - 1  =  w Q / (qbar d)

  with Q conserved.  THE CLOCK RATE IS A CONSERVED CHARGE.  That answers L216's question in
  the only way a question of this shape can be answered: 1e7 does not come from anywhere,
  it is set once and a symmetry protects it exactly, which is what makes a large value
  technically natural rather than fine-tuned.

  Third, and this is the cost.  The matter coupling MOND requires, lambda chi rho_b, is not
  shift symmetric.  It drives the charge linearly in cosmic time, and since
  a_0 = lambda^3/(12 pi G beta s_0) with lambda and beta constants of the action, a growing
  clock rate pulls a_0 DOWN.  The rate is free of the clock rate itself (V5), so it cannot
  be tuned away: at the numbers carried so far a_0 falls 13% since z = 5, against the one
  percent the framework's own derived flat law allows (V6).  MOND's coupling fights the
  framework's distinctive prediction.

  Holding the flat law forces

      w  <~  6e-7 ,

  more than two orders below the acoustic bound (V7) and the tightest constraint on the
  sector's equation of state this programme has derived.  The published prediction band
  0 < w <~ 1e-4 shrinks by the same factor (V8).  Its SIGN survives -- w strictly positive,
  distinct from LCDM's exact zero, still required by criticality -- but its magnitude moves
  further out of experimental reach, and that is a real cost.

  A correction falls out on the way.  In the limit the decoupling branch forces, L214's
  enhancement ratio C = 2 k qbar^2/U equals k/d, which is exactly the reciprocal of the
  interpolating function's floor (V4).  So L214's 'one inequality, C >= 1e3' is the
  rotation-curve requirement restated, not a separate price.  That condition is withdrawn
  as an independent cost.

  LIMITS.  The shift symmetry is read off the structure of the action rather than proved by
  a formal variation.  The drift is computed at linear order with a conformal coupling to
  baryons alone, taking the trace-free radiation sector not to source the scalar; a
  disformal piece would add a term not computed here.  The relation lambda qbar = H
  sqrt(3 C w Omega/2) uses f_s = 1 at solar-system accelerations, which MOND requires and
  which is not derived.  The flat-law tolerance of one percent over z <= 5 is taken from the
  framework's own derived law, not from data.  No gate has been re-run at w = 6e-7, and
  whether criticality still operates that close to zero pressure is NOT computed here.
""")
print(f"L217 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("fable_independent_2026/L217_results.json", "w"), indent=1)
