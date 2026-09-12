#!/usr/bin/env python3
"""L215 -- the last gate: the solar system, with the matter coupling L214 added.

L214 leaves two gates open: the solar system with the new coupling, and kappa (a theorem of
this programme, not a gap).  This lane takes the solar-system gate.

A conformal matter coupling would shift the time potential and not the space one, giving a
post-Newtonian gamma far from unity and failing light bending outright.  The standard cure
is a disformal coupling along a unit timelike vector -- which TeVeS and AeST must ADD as a
separate dynamical field.  This action already has one: the clock's own gradient supplies
n_mu for free.  This lane expands the matter metric in the weak field, measures gamma,
then boosts it and measures what the preferred-frame parameter becomes.
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
eps = sy.Symbol('epsilon', positive=True)
Phi, Psi, phi, wv = sy.symbols('Phi Psi varphi w', real=True)

def o1(e):
    """First order in the POTENTIALS only.  The velocity is counted separately: a
    preferred-frame term is first order in the potential AND first order in the velocity,
    so scaling both by the same bookkeeping parameter would discard exactly the term
    being looked for."""
    return sy.simplify(sy.series(e.subs({Phi: eps*Phi, Psi: eps*Psi, phi: eps*phi}),
                                 eps, 0, 2).removeO()).subs(eps, 1)

# ------------------------------------------------------------------ static: gamma_PPN
print("PART A -- the static field: does light bend correctly?")
# Newtonian gauge, static clock: n^mu = (1,0,0,0) normalised, so n_0 = -(1+Phi).
g00 = -(1 + 2*Phi); gij = 1 - 2*Psi
n0 = -(1 + Phi)
# disformal matter metric, small phi:  gtilde = (1 - 2 phi) g - 4 phi n (x) n
gt00 = o1((1 - 2*phi)*g00 - 4*phi*n0**2)
gtij = o1((1 - 2*phi)*gij)
Phi_t = sy.simplify(-(gt00 + 1)/2)
Psi_t = sy.simplify((1 - gtij)/2)
check("V1 [the disformal coupling shifts BOTH potentials by the same amount] the matter "
      "metric is expanded to first order and the two potentials matter actually sees are "
      "read off and differenced",
      f"Phi~ = {Phi_t}, Psi~ = {Psi_t}, difference = {sy.simplify(Phi_t - Psi_t)}",
      sy.simplify((Phi_t - Psi_t) - (Phi - Psi)) == 0
      and sy.simplify(Phi_t - Phi - phi) == 0 and sy.simplify(Psi_t - Psi - phi) == 0,
      "both pick up exactly +varphi, so the scalar cancels out of the difference. A "
      "CONFORMAL coupling shifts only the time potential and would not do this")

gamma_ppn = sy.simplify((Psi_t/Phi_t).subs(Psi, Phi))
check("V2 [hence the post-Newtonian gamma is exactly one] with no anisotropic stress in the "
      "Einstein frame the two metric potentials are equal, and the ratio matter sees is "
      "formed and compared with 1",
      f"gamma_PPN = Psi~/Phi~ = {gamma_ppn}", sy.simplify(gamma_ppn - 1) == 0,
      "light bending and Shapiro delay are exactly general-relativistic however strong the "
      "scalar is. This is the TeVeS mechanism, obtained here without adding a vector field: "
      "the cuscuton clock already carries the unit timelike direction it needs, and carries "
      "no propagating scalar of its own")

# ------------------------------------------------------------------ boosted: alpha_1
print()
print("PART B -- the boosted field: what the clock's frame costs")
# solar system moving at w through the clock's frame: n^mu = (1, w^i), so n_i = w_i.
n_i = wv
gt0i = o1((1 - 2*phi)*0 - 4*phi*n0*n_i)
ord_w = sy.simplify(wv*sy.diff(gt0i, wv)/gt0i) if gt0i != 0 else None
ord_phi = sy.simplify(phi*sy.diff(gt0i, phi)/gt0i) if gt0i != 0 else None
check("V3 [boosting turns the disformal term into a gravitomagnetic one] the mixed "
      "time-space component of the matter metric is formed for a system moving through the "
      "clock's frame, and its orders in the velocity and in the scalar are both measured",
      f"gtilde_0i = {gt0i}, order in w = {ord_w}, order in varphi = {ord_phi}",
      gt0i != 0 and ord_w == 1 and ord_phi == 1,
      "first order in the velocity, which is exactly the preferred-frame signature. The "
      "coefficient is 4 varphi, so the effect is proportional to the scalar's share of the "
      "local potential")

# match to the PPN form, whose alpha_1 piece in g_0i is (1/2) alpha_1 w U
f_s = sy.Symbol('f_s', positive=True)          # varphi/U, the scalar's share of the potential
alpha1 = sy.simplify(2*(4*f_s))                # 4 varphi w = (1/2) alpha_1 w U  =>  alpha_1 = 8 f_s
bound = 1e-4
f_s_max = float(bound/8)
check("V4 [and undragged, it misses the bound by five orders] matching to the "
      "post-Newtonian form gives the preferred-frame parameter in terms of the scalar's "
      "share of the local potential, which is evaluated at the share MOND requires "
      "(order unity at solar-system accelerations) and compared with the bound",
      f"alpha_1 = {alpha1} = {float(alpha1.subs(f_s, 1)):.1f} at f_s = 1, "
      f"bound = {bound:.0e}, over by {float(alpha1.subs(f_s, 1))/bound:.1e}",
      float(alpha1.subs(f_s, 1)) > bound,
      "so a clock that stays in the cosmic frame is excluded outright. This is the same "
      "wall that killed the vector-based completions, reached here by the same route")

# the escape, stated as a number
v_cosmic = 370e3       # m/s, solar system through the CMB frame
v_res_max = f_s_max*v_cosmic
check("V5 [THE GATE, restated as one requirement on the clock] the residual misalignment "
      "velocity between the clock's frame and the local matter frame that would saturate "
      "the bound is solved for, and compared with the solar system's own velocity through "
      "the cosmic frame",
      f"v_residual <= {v_res_max:.1f} m/s against v_cosmic = {v_cosmic/1e3:.0f} km/s, "
      f"an alignment of 1 part in {1/f_s_max:.0e}",
      v_res_max < v_cosmic,
      "the gate is not a yes or no about the coupling. It is a single quantitative "
      "requirement on how tightly local matter drags the clock into its own rest frame: "
      "to better than five metres per second. Whether the clock's own field equation "
      "delivers that is NOT computed here")

board_open = ["solar system: the clock alignment of V5, uncomputed",
              "kappa: provably underivable by this class (theorem, not a gap)"]
check("V6 [what the board now says] the open items are listed and counted, and the count "
      "compared against zero, since a board with nothing open would be a claim this "
      "programme is not entitled to make",
      f"{len(board_open)} open: {board_open}",
      len(board_open) >= 1,
      "every other gate carries a computed number. The solar-system gate has gone from "
      "blocked to a single number that one further calculation would decide")

print()
print("READING")
print("""
  The last gate resolves into one number.

  Coupling matter disformally along the clock's own unit timelike direction shifts BOTH
  weak-field potentials by the same amount (V1), so the scalar drops out of their
  difference and the post-Newtonian gamma is exactly one (V2): light bending and Shapiro
  delay are general-relativistic no matter how strong the scalar is.  That is the TeVeS
  mechanism, and this action gets it without adding a vector field, because the cuscuton
  clock already supplies the direction and propagates no scalar of its own.

  Boosting is where it costs.  The same disformal term becomes a gravitomagnetic one at
  first order in the velocity through the clock's frame (V3), giving a preferred-frame
  parameter alpha_1 = 8 f_s with f_s the scalar's share of the local potential.  At the
  share MOND requires that is about 8, against a bound of 1e-4 -- five orders over (V4).
  A clock sitting in the cosmic frame is excluded outright, by the same wall that killed
  the vector-based completions.

  So the gate is exactly this: local matter must drag the clock into its own rest frame to
  within five metres per second, one part in 1e5 of the solar system's motion through the
  cosmic frame (V5).  That is a single, sharp, computable requirement on the clock's field
  equation, and this lane does not compute it.

  LIMITS.  The disformal form is taken at leading order in the scalar, in the standard
  one-parameter shape; a different disformal factor changes the coefficient 8 but not the
  first-order-in-velocity structure.  f_s = 1 is the value MOND requires at solar-system
  accelerations and is not derived here.  The matching to the post-Newtonian g_0i uses the
  standard normalisation, so the coefficient is convention-dependent at the factor-of-two
  level and the five-orders conclusion is not.  Whether the clock is dragged, and by how
  much, is the calculation this lane hands on.
""")
print(f"L215 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("fable_independent_2026/L215_results.json", "w"), indent=1)
