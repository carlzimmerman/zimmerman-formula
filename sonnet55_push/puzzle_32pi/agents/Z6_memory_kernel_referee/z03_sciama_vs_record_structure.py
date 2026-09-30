#!/usr/bin/env python3
"""z03: STRUCTURE.  Does the record's kernel have the Sciama structure (linear retarded response of the inertial force to the particle's own
acceleration history, weight (G rho/c^2) dV/r, strength fixed by G rho), or is 'M1 = (2/3) R_c/c' just a moment of an unrelated weight?
Premise for the Sciama side (X3's, stated once): F/m = -(1/c^2) int G rho a(t - r/c) dV/r = - int w_S(u) a(t-u) du, w_S(u) = 4 pi G rho u on [0,T], u = r/c.
Record side: Theta(tau) = int ds K(s) theta(tau, tau-s), theta = rapidity gap (exact), inertia = m mu(Theta).  c = 1."""
import sympy as sp
from sympy import pi, sqrt, Rational as Rat, symbols
import sys

PASS = FAIL = CO = CB = 0


def chk(n, c, d=""):
    global PASS, FAIL
    if c: PASS += 1; print("  ok  ", n, d)
    else: FAIL += 1; print("  FAIL", n, d)


def ctrl(n, c, d=""):
    global CO, CB
    if not c: CO += 1; print("  ctrl-ok ", n, d)
    else: CB += 1; print("  CTRL-BAD", n, d)


def zero(e): return sp.simplify(e) == 0


t, u, s, T, Cc, Gr, tt = symbols('t u s T C G_rho t_step', positive=True)
al0, al1, al2, al3 = symbols('alpha0 alpha1 alpha2 alpha3', real=True)

print("== S1: Sciama's force is LINEAR in the acceleration history; only M0 acts on a steady acceleration, M1 multiplies the JERK ==")
a_t = al0 + al1 * t + al2 * t ** 2                                  # a general polynomial acceleration history
w = Cc * u                                                          # weight ~ r dr on [0, T]
force = sp.integrate(w * a_t.subs(t, t - u), (u, 0, T))             # int w(u) a(t-u) du  (= -F/m)
Mk = lambda k: sp.integrate(u ** k * w, (u, 0, T))
taylor = Mk(0) * a_t - Mk(1) * sp.diff(a_t, t) + Mk(2) / 2 * sp.diff(a_t, t, 2)
chk("int w(u) a(t-u) du = M0 a - M1 adot + (M2/2) addot  (exact for a quadratic a(t); w = C u on [0,T])", zero(force - taylor))
chk("M0 = C T^2/2, M1 = C T^3/3: for a STEADY acceleration F/(m a) = -M0 (= -I): the response is a constant, independent of |a|", zero(Mk(0) - Cc * T ** 2 / 2) and zero(Mk(1) - Cc * T ** 3 / 3) and zero(sp.diff(force.subs({al1: 0, al2: 0}) / al0, al0)))
Y = symbols('Y', positive=True)
mu2 = sqrt((-1 + sqrt(1 + 4 * Y ** 4)) / 2) / Y
chk("record: steady-state Theta = M1 |a|/c, and the inertia ratio mu_2(Theta) DOES depend on |a| (d mu/d Theta != 0): the a0 of the record is the point where the NONLINEAR mu(Theta) crosses over", sp.diff(mu2, Y).subs(Y, 1).evalf() != 0)
ctrl("control: the Sciama response ratio F/(m a) has a crossover in |a| (d/d|a| != 0)", not zero(sp.diff(force.subs({al1: 0, al2: 0}) / al0, al0)))
print("   => for a steady acceleration Sciama's kernel never sees M1 (the moment that defines the record's a0 = (2/3)c/M1); M1/M0 is the mean retardation, which enters only through adot")

print("\n== S2: how the two objects are related for the SAME kernel: Sciama's force contains d/dt of the record-type Theta, not Theta ==")
v0, v1, v2, v3 = symbols('v0 v1 v2 v3', real=True)
v_t = v0 + v1 * t + v2 * t ** 2 / 2 + v3 * t ** 3 / 6              # velocity history (monotone locally): rapidity phi = v (c = 1, NR)
a_from_v = sp.diff(v_t, t)
K_S = Cc * s                                                        # K := Sciama weight, [0,T]
Theta_S = sp.integrate(K_S * (v_t - v_t.subs(t, t - s)), (s, 0, T))           # record-type functional Int K(s) [phi(t) - phi(t-s)] ds (monotone case: no absolute value)
KstarA = sp.integrate(K_S * a_from_v.subs(t, t - s), (s, 0, T))               # Sciama:  int K_S(s) a(t-s) ds
M0S, M1S = sp.integrate(K_S, (s, 0, T)), sp.integrate(s * K_S, (s, 0, T))
chk("identity: Sciama's force  int K_S a(t-s) ds = M0 a(t) - dTheta_S/dt  where Theta_S = int K_S [phi(t) - phi(t-s)] ds is the record's functional evaluated with K = K_S", zero(KstarA - (M0S * a_from_v - sp.diff(Theta_S, t))))
chk("steady acceleration (v = a t): Theta_S = M1 a and dTheta_S/dt = 0, so the record's Theta drops out of Sciama's force", zero((Theta_S.subs({v0: 0, v2: 0, v3: 0}) - M1S * v1)) and zero(sp.diff(Theta_S.subs({v0: 0, v2: 0, v3: 0}), t)))
ctrl("control: the identity holds with M1 in place of M0", zero(KstarA - (M1S * a_from_v - sp.diff(Theta_S, t))))
print("   => Sciama: force = -m (M0 a - dTheta/dt);  record: inertia = m mu(Theta).  Same kernel, different functionals: M0 controls the steady inertia in one, M1 controls the threshold in the other.")

print("\n== S3: step responses.  X3: Sciama inertia builds as (t/T)^2.  The record's Theta (exact rapidity gap) builds LINEARLY in t ==")
I_t = sp.integrate(4 * pi * Gr * u, (u, 0, tt))                    # F/(m a) for a step of duration tt < T
chk("Sciama step: F/(m a) = 2 pi G rho t^2 for t < T (quadratic in the duration; a-independent)", zero(I_t - 2 * pi * Gr * tt ** 2))
M0w = symbols('M0w', positive=True)
Kn = M0w * 2 * s / T ** 2                                          # unit-shape (2s/T^2), weight M0w
a_step = symbols('a_step', positive=True)
# exact rectilinear rapidity gap of a step a for duration t:  phi(t) - phi(t-s) = a min(s, t)
Th_step = sp.integrate(Kn * a_step * s, (s, 0, tt)) + sp.integrate(Kn * a_step * tt, (s, tt, T))
chk("record's Theta after a step of acceleration a for duration t < T (exact rapidity gap): Theta = M0 a (t - t^3/(3 T^2)) -- LINEAR in t at small t", zero(Th_step - M0w * a_step * (tt - tt ** 3 / (3 * T ** 2))))
Th_dc = sp.integrate(s * Kn, (s, 0, T)) * a_step
ratio = sp.simplify(Th_step / Th_dc)
chk("relative to its steady value M1 a: Theta(t)/Theta_DC = (3/2)(t/T)(1 - t^2/(3 T^2)) -> (3/2)(t/T) for t << T", zero(ratio - Rat(3, 2) * (tt / T) * (1 - tt ** 2 / (3 * T ** 2))) and sp.limit(ratio / (tt / T), tt, 0) == Rat(3, 2))
chk("for t << T: Theta -> M0 a t = M0 x (speed gained): the record's mu-argument is a function of the SPEED (long-memory branch), not of |a|/a0", sp.limit(Th_step / (M0w * a_step * tt), tt, 0) == 1)
ctrl("control: the record's step response is quadratic in t at small t (as Sciama's), i.e. Theta/t^2 stays finite", bool(sp.limit(Th_step / tt ** 2, tt, 0, '+').is_finite))
print("   (the record's own midpoint form Theta = (1/c) int K s |a(tau - s/2)| ds is a small-lag expansion and is NOT used for a step; the exact gap is)")

print("\n== S4: dimensionally, the record's kernel K and Sciama's weight w_S are both 1/time; the record's 'a0' comes from the RAPIDITY (c), Sciama's mean lag gives only a frequency ==")
M0s, M1s = symbols('M0s M1s', positive=True)
om, vv = symbols('omega v', positive=True)
# oscillating acceleration a e^{i omega t}: response  int w(u) e^{-i omega u} du = M0 - i omega M1 + ...; ratio of the jerk term to the steady term = omega M1/M0
tau_bar = Rat(2, 3) * T
om_c = sp.solve(sp.Eq(om * tau_bar, 1), om)[0]
chk("Sciama kernel: the jerk term equals the steady term at omega_c = 1/(mean lag) = 3/(2T): a FREQUENCY threshold, linear in the response", zero(om_c - Rat(3, 2) / T))
a_c = sp.simplify(vv * om_c)                                       # to state it as an acceleration one needs a velocity (a = v omega for circular motion)
a0sym = symbols('a0', positive=True)
a_c_at = sp.simplify(a_c.subs(T, 1 / a0sym))                       # T = c/a0
chk("with T = c/a0 the frequency threshold is an acceleration a_c = (3/2)(v/c) a0: velocity dependent (1e-3 a0 at galactic speeds); the record's a0 has no v/c", zero(a_c_at - Rat(3, 2) * vv * a0sym))
ctrl("control: the crossover acceleration of the Sciama kernel is independent of v", zero(sp.diff(a_c_at, vv)))

print("\n== S5: what the identification does and does not say ==")
print("   TRUE (arithmetic): the mean lag M1/M0 of the normalised sharp r dr weight on [0,T] is (2/3)T (z02 M5).")
print("   TRUE (conditional): for a record kernel of that SHAPE, unit weight M0 = 1 and T = c/a0, M1 = (2/3)c/a0 (z02 M1).")
print("   NOT TRUE: 'the record's kernel is Sciama's kernel': (i) Sciama's strength at T = c/a0 is M0 = 8 pi, not 1 (z02 M5a); (ii) the record's action has no G, no rho, no dV (z01);")
print("             (iii) Theta and Sciama's force are different functionals of a kernel (S2, S3); (iv) the record's shape is invisible (z02 M4), the requirement fixes only M1 (z02 M1).")
print(f"\n== TOTAL: {PASS} pass, {FAIL} fail; controls rejected {CO}, not rejected {CB} ==")
sys.exit(0 if FAIL == 0 and CB == 0 else 1)
