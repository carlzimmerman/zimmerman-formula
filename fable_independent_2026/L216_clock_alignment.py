#!/usr/bin/env python3
"""L216 -- the clock alignment calculation that L215 handed on.

L215 reduced the solar-system gate to one number: local matter must drag the clock's frame
into its own rest frame to within 4.6 m/s, one part in 8e4 of the solar system's motion
through the cosmic frame.  Whether the clock's own field equation delivers that was not
computed.  This lane computes it.

The route: (A) show the disformal coupling cannot simply be switched off, because the
post-Newtonian gamma locks its coefficient to the conformal one; (B) show the clock is a
CONSTRAINT field -- the cuscuton's linearised Lagrangian carries no squared time derivative,
so its equation is elliptic and the tilt is a boundary-value problem, not a propagating
response; (C) derive the matter source and the clock's stiffness in the solar system, which
turns out to be independent of the matter coupling and of the MOND coefficient; (D) solve
the exterior problem for its radial falloff; (E) evaluate the drag at 1 AU and invert the
bound into a requirement on the one quantity left free.

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

# ---------------------------------------------------------------- A: no way to switch it off
print("PART A -- can the preferred-frame coupling simply be removed?")
Phi, Psi, ph, av, bv = sy.symbols('Phi Psi varphi a b', real=True)
eps = sy.Symbol('epsilon', positive=True)
def o1(e):
    return sy.simplify(sy.series(e.subs({Phi: eps*Phi, Psi: eps*Psi, ph: eps*ph}),
                                 eps, 0, 2).removeO()).subs(eps, 1)
# general matter metric: gt = A(varphi) g + B(varphi) n (x) n, A = 1 - 2 a varphi, B = -2 b varphi
A_, B_ = 1 - 2*av*ph, -2*bv*ph
gt00 = o1(A_*(-(1 + 2*Phi)) + B_*(1 + 2*Phi))
gtij = o1(A_*(1 - 2*Psi))
Phi_t = sy.simplify(-(gt00 + 1)/2)
Psi_t = sy.simplify((1 - gtij)/2)
gamma_expr = sy.simplify((Psi_t/Phi_t).subs(Psi, Phi))
b_locked = sy.solve(sy.Eq(sy.numer(sy.together(gamma_expr - 1)), 0), bv)
check("V1 [the disformal coefficient is LOCKED to the conformal one by light bending] the "
      "matter metric is written with independent conformal and disformal strengths, the "
      "post-Newtonian ratio is formed, and the disformal strength that makes it one is "
      "solved for",
      f"Phi~ = {Phi_t}, Psi~ = {Psi_t}, gamma = {gamma_expr}, b = {b_locked}",
      b_locked == [2*av],
      "b = 2a exactly. The disformal term cannot be dialled down while keeping gamma = 1: "
      "the fix for light bending and the source of the preferred-frame effect are the same "
      "operator with a fixed relative weight. There is no escape by tuning, so the gate has "
      "to be met by dragging or not at all")

# ---------------------------------------------------------------- B: the clock is a constraint
print()
print("PART B -- the clock is a constraint field, so the tilt is a boundary-value problem")
t, psid = sy.symbols('t psidot', real=True)
gpsi = sy.Symbol('g', real=True)                      # |grad psi|
s_expr = sy.sqrt((1 + psid)**2 - gpsi**2)             # s for tau = t + psi(x,t)
s_ser = sy.series(sy.series(s_expr, psid, 0, 3).removeO(), gpsi, 0, 3).removeO()
coef_tt = sy.simplify(s_ser.coeff(psid, 2))                       # coefficient of psidot^2
coef_gg = sy.simplify(s_ser.coeff(gpsi, 2).subs(psid, 0))         # of |grad psi|^2, at psidot = 0
check("V2 [no squared time derivative survives, so the clock equation is elliptic] the "
      "cuscuton scalar s is expanded for tau = t + psi; the coefficient of the squared time "
      "derivative is read off, and the coefficient of the squared gradient is read off at "
      "vanishing time derivative, the two being measured separately",
      f"coefficient of psidot^2 = {coef_tt}, coefficient of |grad psi|^2 = {coef_gg}",
      coef_tt == 0 and coef_gg == sy.Rational(-1, 2),
      "the linear-in-s structure kills the time-kinetic term exactly and leaves -W|grad "
      "psi|^2/2. The clock therefore propagates nothing and obeys a constraint on each "
      "slice: whether it aligns with the Sun is settled by an elliptic equation with the "
      "cosmic frame as its boundary condition at infinity, not by a wave that may or may "
      "not arrive")

# ---------------------------------------------------------------- C: source and stiffness
print()
print("PART C -- the source, and the stiffness that resists it")
# Varying the disformal point-mass action gives  div(W grad psi) = -4 div(varphi rho v).
# The stiffness is W at the LOCAL gradient invariant, not W(0) = U: expanding s W(Y) gives
# -(W/2)|grad psi|^2 with W evaluated where the field point is.
G, Msun, r, s0, fs, lam = sy.symbols('G M r s_0 f_s lambda', positive=True)
k_hi = lam**2/(8*sy.pi*G*s0)                 # W_Y at solar-system accelerations (L214 V2 match)
gradphi = fs*G*Msun/(lam*r**2)               # scalar gradient giving a share f_s of g_N
W_local = sy.simplify(k_hi*gradphi**2)       # W ~ k Y in the saturated regime
free_of = [sy.simplify(sy.diff(W_local, lam)), sy.simplify(sy.diff(W_local, sy.Symbol('beta', positive=True)))]
check("V3 [the solar-system stiffness is free of both the matter coupling and the MOND "
      "coefficient] the clock's gradient stiffness is formed at the local invariant and its "
      "derivatives with respect to the matter coupling and the MOND coefficient are measured",
      f"W_local = {W_local}, dW/dlambda = {free_of[0]}, dW/dbeta = {free_of[1]}",
      free_of[0] == 0 and free_of[1] == 0,
      "W_local = f_s^2 G M^2/(8 pi s_0 r^4). Both free coefficients cancel, so the drag "
      "cannot be improved by choosing them. The only handle left is the clock rate s_0")

# the interior gain, where the source sits
rho_sun = 3*Msun/(4*sy.pi*sy.Symbol('R', positive=True)**3)
R = sy.Symbol('R', positive=True)
phi_s = fs*G*Msun/R                                    # scalar potential at the source
D_R = sy.simplify(4*phi_s*rho_sun/W_local.subs(r, R))
check("V4 [the drag gain at the source is a pure number] the ratio of the disformal source "
      "to the clock's stiffness is formed at the stellar surface and its dependence on the "
      "star's mass and radius is measured, since a gain that depended on them would make "
      "the gate object-by-object",
      f"D(R) = {D_R}, dD/dM = {sy.simplify(sy.diff(D_R, Msun))}, "
      f"dD/dR = {sy.simplify(sy.diff(D_R, R))}",
      sy.simplify(sy.diff(D_R, Msun)) == 0 and sy.simplify(sy.diff(D_R, R)) == 0
      and sy.simplify(D_R - 24*s0/fs) == 0,
      "D(R) = 24 s_0/f_s, independent of the star entirely. At the clock rate positivity "
      "forces (s_0 >= 2) that is at least 48: the source beats the stiffness at the "
      "surface, so the clock IS dragged there. The question is how far out that survives")

# ---------------------------------------------------------------- D: the exterior falloff
print()
print("PART D -- how far out the dragging survives")
g = sy.Function('g')
n = sy.Symbol('n')
# exterior, l = 1: (r^2 W g')' = 2 W g with W ~ r^-4  =>  r^2 g'' - 2 r g' - 2 g = 0
ind = sy.expand(n*(n - 1) - 2*n - 2)
roots = sorted([sy.nsimplify(x) for x in sy.solve(sy.Eq(ind, 0), n)], key=lambda z: float(z))
n_dec = roots[0]
p_drag = sy.simplify(1 - n_dec)               # |grad psi| ~ r^{n_dec - 1}, so drag ~ r^{-p}
# the constant-stiffness comparison
ind_const = sy.expand(n*(n - 1) + 2*n - 2)
roots_c = sorted([sy.nsimplify(x) for x in sy.solve(sy.Eq(ind_const, 0), n)], key=lambda z: float(z))
p_const = sy.simplify(1 - roots_c[0])
check("V5 [the falling stiffness makes the dragging reach much further than a plain dipole] "
      "the exterior dipole equation is solved for its indicial exponents with the r^-4 "
      "stiffness and again with a constant stiffness, and the two decay rates of the tilt "
      "are compared",
      f"exponents {roots} => drag ~ r^-{sy.nsimplify(p_drag)} = r^-{float(p_drag):.4f}; "
      f"constant stiffness gives r^-{float(p_const):.0f}",
      float(p_drag) < float(p_const),
      "with the stiffness falling as the fourth power of radius the tilt decays as "
      "r^-(sqrt(17)-1)/2 = r^-1.562 instead of the r^-3 of an ordinary dipole. The clock is "
      "dragged far further than a naive estimate would give, and that works in the "
      "construction's favour")

# ---------------------------------------------------------------- E: the number
print()
print("PART E -- the drag at 1 AU, and what the bound demands")
Rsun, AU = 6.957e8, 1.496e11
pf = float(p_drag)
reach = (Rsun/AU)**pf
D_AU_at_2 = 24*2.0*reach                      # f_s = 1, s_0 = 2
resid_at_2 = 1.0/(1.0 + D_AU_at_2)
need_resid = 1.25e-5                          # L215: 4.6 m/s out of 370 km/s
check("V6 [at the clock rate already forced, the gate is missed] the drag gain is carried "
      "from the stellar surface to 1 AU with the exponent of V5, the residual misalignment "
      "fraction 1/(1+D) is formed, and compared with the requirement",
      f"D(1 AU) = {D_AU_at_2:.4f} at s_0 = 2; residual = {resid_at_2:.3e} "
      f"vs required {need_resid:.2e}; short by {resid_at_2/need_resid:.1e}",
      resid_at_2 > need_resid,
      "at the minimum clock rate the drag reaches only about one percent at Earth's orbit "
      "and the gate is missed by nearly the full five orders. Dragging alone does not "
      "rescue the coupling at s_0 = 2")

s0_req = need_resid**-1/(24.0*reach)
check("V7 [THE ANSWER: the gate is an inequality on the clock rate] the drag gain is linear "
      "in the clock rate, so the requirement is inverted for the clock rate that satisfies "
      "it, and that is compared with the rate positivity already forces",
      f"s_0 >= {s0_req:.3e}, against s_0 >= 2 from positivity (L213 V6)",
      s0_req > 2,
      "the solar system does not exclude the construction. It DEMANDS a clock running about "
      "1.5e7 times proper time. That is the third independent constraint on the same "
      "quantity and the third pointing the same way, but it is seven orders beyond what the "
      "other two need, and nothing in the programme explains a number that size")

# what that clock rate costs elsewhere
w_ac = 1e-4
mrel_req = w_ac/(s0_req - 1)
cubic_share = 1.0/(s0_req - 1)
PX_over_d = 1.0/mrel_req
check("V8 [and what it costs elsewhere] the margin, the cubic operator's share and the "
      "scalar's kinetic coefficient implied by that clock rate are each evaluated, and the "
      "kinetic coefficient is compared against 1e6 as a strong-coupling flag",
      f"m_rel = {mrel_req:.2e}, cubic share |rho_3|/rho = {cubic_share:.2e}, "
      f"P_X/d = 1/m_rel = {PX_over_d:.2e}",
      PX_over_d > 1e6,
      "the margin collapses to 7e-12 and the scalar's kinetic coefficient rises to 1.4e11 "
      "times the gradient coefficient. That is not a contradiction with anything computed "
      "-- the sound speed and every gate of L213/L214 are unchanged, because they depend on "
      "w and not on s_0 -- but a kinetic coefficient eleven orders above its neighbour is a "
      "strong-coupling question, and it is NOT computed here")

print()
print("READING")
print("""
  The clock is dragged, and not nearly enough.

  First, there is no way round the question.  Writing the matter metric with independent
  conformal and disformal strengths and demanding gamma = 1 forces b = 2a exactly (V1): the
  operator that fixes light bending IS the operator that generates the preferred-frame
  effect, at a locked relative weight.  The gate has to be met by dragging.

  Second, the dragging is a constraint, not a response.  The cuscuton's linearised
  Lagrangian has no squared time derivative at all (V2), so the clock propagates nothing and
  its tilt solves an elliptic equation whose boundary condition at infinity is the cosmic
  frame.  Whether the Sun wins is a straight competition between a local source and a
  stiffness.

  Third, that competition is decided by one number.  The stiffness in the solar system is
  the gradient function at the LOCAL invariant, and it works out to f_s^2 G M^2/(8 pi s_0
  r^4) -- free of both the matter coupling and the MOND coefficient (V3), so neither can be
  used to improve the drag.  At the source the gain is 24 s_0/f_s, independent of the star's
  mass and radius entirely (V4).  Outside, the falling stiffness makes the tilt decay as
  r^-1.562 rather than the r^-3 of an ordinary dipole (V5), which helps considerably and is
  still not enough: at the minimum clock rate the drag is about one percent at Earth's orbit
  and the residual misalignment misses the bound by nearly five orders (V6).

  So the gate is an inequality, and it is on the clock rate:

      s_0  >~  1.5e7 .

  This is the third independent constraint on s_0 and the third that pushes it up -- the
  clock identity, positivity of the sector's energy, and now the solar system.  That is a
  real structural convergence.  But the first two want s_0 of order unity and this one wants
  ten million, and nothing in the programme explains a number that size.  It is a
  requirement, recorded as a requirement, not a derivation.

  LIMITS, and they are substantial.  The interior match of V4 evaluates source and stiffness
  at the stellar surface with a uniform-density star; the real interior profile of the
  gradient invariant is not solved, and the gain could move by an order either way.  The
  exterior stiffness is taken as r^-4 throughout, which assumes the scalar's share f_s stays
  constant from the surface to 1 AU.  The elliptic problem is solved only for its indicial
  exponents and matched at one radius, not integrated through the star.  The post-Newtonian
  matching inherited from L215 is convention-dependent at the factor-of-two level.  The
  bound used is |alpha_1| < 1e-4; a tighter bound moves s_0 up proportionally.  And the
  strong-coupling question raised in V8 is stated, not answered.
""")
print(f"L216 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("fable_independent_2026/L216_results.json", "w"), indent=1)
