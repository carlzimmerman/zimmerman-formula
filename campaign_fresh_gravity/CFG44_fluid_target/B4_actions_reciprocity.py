#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
B4 -- CLASS (ii)/(iii) AT THE LEVEL OF ACTIONS: minimal actions whose static limit could produce (T), with the reciprocity (N11) and double-counting (N13) audits.

Each candidate below is a minimal static (non-relativistic, spherical) action; the audit is what it does to (a) the well-posedness of the fluid, (b) the gravitating mass
(GR + real mass, T5), (c) the reaction on the baryons.  kappa = 1/2 FITTED; canonical a0; nothing is fitted.

Q1  STATE-INDEPENDENT STRESS ("pressure sourced by the field energy": P = P_b(x) prescribed by the baryons, not a function of the fluid's state).
    Linearised radial Euler + continuity (sympy):  rho0 xi_tt = g (rho0 xi)'  =>  omega^2 = - i g k :  Im omega ~ sqrt(g k/2) grows without bound as k -> infinity
    (Hadamard ill-posed).  Controls: a barotropic fluid (rho0 xi_tt = (c_s^2 rho0 xi')' + ...) and a state-dependent temperature P = rho sigma^2(x) are self-adjoint with a
    positive weight (real omega^2).  So the temperature route is well-posed and the stress route is not.
Q2  CONSTRAINT ACTION: L = r^2 [-Phi'^2/8 pi G - (rho_b + rho_c) Phi - rho_c eps(rho_c) + lambda (rho_c Phi' - s(r))]  implementing (T) as a Lagrange constraint
    (s = a0 M_b(<r)/(4 pi r^3), i.e. rho_c g = s).  Euler-Lagrange (sympy): g = G (M_b + M_c + 4 pi r^2 lambda rho_c)/r^2 -- the multiplier gravitates:  M_lambda = 4 pi r^2 lambda rho_c.
    GR + real mass (T5) needs lambda rho_c = 0, which makes the constraint redundant with barotropic hydrostatics (excluded, B2).  Numbers for an isothermal fluid: M_lambda/M_c.
Q2b DENSITY-SLAVED FLUID (the fluid density is a prescribed functional of the baryons, rho_c(x) = rho_T[rho_b](x), the multiplier is the chemical potential mu = Phi_tot).  The static
    limit is (T) by construction and the fluid is in equilibrium (mu = Phi_tot balances gravity), but the energy E = Int mu rho_T d^3x depends on the baryons: the virtual-work reaction on a
    baryon shell is a = G dE/du_N.  Numerics (functional derivative by a narrow bump perturbation of u_N, validated against the analytic Q3 case): reaction/g_law printed.
Q3  KERNEL-VISIBLE FLUID (the fluid feels the law's phantom potential U = Phi_ph[rho_b], E_int = Int rho_c U): symmetric => the baryons feel the reaction.  Derived:
    E_int = - Int g_ph(s) M_c(<s) ds  =>  per unit baryon mass, the reaction is  - kappa(y) G M_c(<r)/r^2,  kappa = (nu - 1) + y nu'(y)  (= (1/2) y^(-1/2) deep).
    Checked against a direct finite-difference of the nonlinear energy functional.  Numbers: reaction / g_law and the double-counting factor D = 1 + reaction/g_tot.
Q4  DOUBLE COUNTING (N13) in numbers: an additive law (phantom + real cold fluid at the cosmic share) overshoots g by the factor printed; the fluid = phantom reading (T5) exhausts
    the cosmic cold budget (Omega_c/Omega_b) M_b at x_cap = sqrt((1 + Omega_c/Omega_b)^2 - 1) = 6.29 (P2) -- beyond it the law needs more fluid than exists inside r.
Q5  TEMPERATURE-SLAVED FLUID (dispersion sigma^2(x) set by the baryons; self-gravitating, hydrostatic in the total field): a well-posed action.  Numerics: the outer profile is an
    ATTRACTOR (V_f^2 = 2 sigma_inf^2 whatever the fluid amplitude); the central cusp amplitude A (rho_c r = A) fixes only the transition radius.  Hence, in this class, the whole
    of Gap 2 is: sigma_inf^2 = (1/2) sqrt(G a0 M_b) (the BTFR, nonlinear in M_b) and A = a0/(4 pi G) (the 'charge').
CHECKS (PRE-DECLARED)
  C1 (sympy) Q1: omega^2 for the three fluid types; Q1 is Hadamard-ill-posed, the other two are self-adjoint.
  C2 (sympy) Q2: the multiplier's gravitating mass; numbers M_lambda/M_c >= 0.1 somewhere for an isothermal fluid tuned at another mass.
  C2b Q2b: the functional-derivative machinery reproduces the analytic Q3 derivative to 5e-3; the slaved-density fluid's reaction on the baryons is >= 0.5 g_law in magnitude at 0.5, 1, 3, 10 h.
  C3 Q3: the reaction formula reproduces the finite-difference derivative of the nonlinear energy to 1e-3; reaction/g_law >= 0.3 at some radius on the compact exp. sphere for both kernels.
  C4 Q4: the additive law overshoots g by >= 0.2 dex at 3 r_M; x_cap = 6.29.
  C5 Q5: attractor: an amplitude change of x0.5, x2, x4 changes g_tot by < 2% at x = 1000 (numeric; slow damped oscillation) but by >= 5% at x = 1; sigma^2 x 1.2 changes g_flat by 1.2 within 5%.
MUTATE=1: Q1 uses the STATE-DEPENDENT fluid (self-adjoint) -- C1 must FAIL; Q3's kappa is replaced by 0 (no reaction) -- C3 must FAIL; Q2b's rho_T is made independent of the baryons (the enclosed-baryon dependence broken) -- C2b must FAIL; Q5's amplitude test uses a fluid that is NOT
  self-gravitating (a test fluid, g = g_N only), which has no attractor -- C5 must FAIL.
Run: python3 B4_actions_reciprocity.py   (MUTATE=1 for the control)
"""
import os, sys, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Bcommon import *

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = Report("B4_actions_reciprocity", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: state-dependent fluid in Q1, kappa = 0 in Q3, non-self-gravitating test fluid in Q5 -- C1, C3, C5 must FAIL ***")

# =============================================================================================== C1  Q1 ill-posedness
R.banner("C1  Q1 (sympy): linearised stratified atmosphere -- three kinds of stress")
z = sp.symbols("z", real=True)
g, c2 = sp.symbols("g c_s2", positive=True)
rho0 = sp.Function("rho0")(z); sig2 = sp.Function("sigma2")(z)
xi = sp.Function("xi")(z)
drho_E = -sp.diff(rho0 * xi, z)                                       # Eulerian density perturbation (continuity)
# momentum: rho0 xi_tt = -(delta P_E)' - g delta rho_E   (weight of the perturbed density, gravity g downward), hydrostatic P0' = -rho0 g
dP_a = -c2 * rho0 * sp.diff(xi, z) + xi * rho0 * g                     # (a) barotropic: Delta P = -c_s^2 rho0 xi'  ->  delta P_E = Delta P - xi P0'
rhs_a = sp.expand(-sp.diff(dP_a, z) - g * drho_E)
rhs_b = sp.expand(-g * drho_E)                                          # (b) state-independent stress: delta P_E = 0
rhs_c = sp.expand(-sp.diff(sig2 * drho_E, z) - g * drho_E)              # (c) P = rho sigma2(z): delta P_E = sigma2 delta rho_E


def coeffs(rhs):
    a2 = sp.simplify(rhs.coeff(sp.Derivative(xi, (z, 2))))
    a1 = sp.simplify(rhs.coeff(sp.Derivative(xi, z)))
    return a2, a1


a2a, a1a = coeffs(rhs_a); a2b, a1b = coeffs(rhs_b); a2c, a1c = coeffs(rhs_c)
P(f"    (a) barotropic:            rho0 xi_tt = ({a2a}) xi'' + ({a1a}) xi' + ...")
P(f"    (b) state-independent P_b: rho0 xi_tt = ({a2b}) xi'' + ({a1b}) xi' + ...")
P(f"    (c) P = rho sigma2(z):     rho0 xi_tt = ({a2c}) xi'' + ({a1c}) xi' + ...")
# symmetric (real omega^2) in the kinetic weight rho0  <=>  a1 = a2'   (operator = (a2 xi')' + a0 xi)
sym_a = sp.simplify(a1a - sp.diff(a2a, z)); sym_b = sp.simplify(a1b - sp.diff(a2b, z))
# (c): in q = rho0 xi the equation is q_tt = (sigma2 q')' + g q' = (1/W)(W sigma2 q')' with W' = g W/sigma2 > 0 : Sturm-Liouville => real omega^2
q = sp.Function("q")(z); W = sp.Function("W")(z)
B_q = sp.diff(sig2 * sp.diff(q, z), z) + g * sp.diff(q, z)
SL = sp.diff(W * sig2 * sp.diff(q, z), z) / W
res_c = sp.simplify(sp.expand(B_q - SL).subs(sp.Derivative(W, z), g * W / sig2).doit())
kx = sp.symbols("k", positive=True)
omega2_b = sp.simplify(-a1b * sp.I * kx / rho0)                        # rho0 (-omega^2) e^{ikz} = a1b (i k) e^{ikz}
P(f"    symmetry residual a1 - a2': (a) {sym_a}, (b) {sym_b};  (c) Sturm-Liouville residual with W' = g W/sigma2: {res_c}")
P(f"    (b): omega^2 = {omega2_b}  ->  Im omega = -+ sqrt(g k/2), unbounded as k -> infinity")
ill = (sym_b != 0) and (a2b == 0)
ok_ctrl = (sym_a == 0) and (res_c == 0)
if MUTATE:
    ill = (sym_a != 0)                                                  # the mutated 'Q1' is the barotropic fluid, which IS symmetric: the ill-posedness claim must fail
check("C1 (sympy) Q1: a fluid whose stress is a prescribed function of position (independent of its state) obeys rho0 xi_tt = g (rho0 xi)' -- omega^2 = -i g k, Hadamard ill-posed "
      "(growth ~ sqrt(k)); a barotropic fluid and a state-dependent temperature P = rho sigma^2(x) are self-adjoint (real omega^2)" + ("  [MUTATE: barotropic fluid used as Q1]" if MUTATE else ""),
      f"(b) not self-adjoint and first order: {sym_b != 0 and a2b == 0}; (a) symmetric and (c) Sturm-Liouville: {ok_ctrl}", bool(ill) and ok_ctrl)

# =============================================================================================== C2  Q2 constraint action
R.banner("C2  Q2 (sympy): the constraint action -- the multiplier gravitates")
rr = sp.symbols("r", positive=True)
Gs = sp.Symbol("G", positive=True)
Phi = sp.Function("Phi")(rr); rho_c = sp.Function("rho_c")(rr); lam = sp.Function("lambda")(rr); rho_b = sp.Function("rho_b")(rr)
s_r = sp.Function("s")(rr)
eps = sp.Function("eps")
L = rr ** 2 * (-sp.diff(Phi, rr) ** 2 / (8 * sp.pi * Gs) - (rho_b + rho_c) * Phi - rho_c * eps(rho_c) + lam * (rho_c * sp.diff(Phi, rr) - s_r))
from sympy.calculus.euler import euler_equations
eqs = euler_equations(L, [Phi, rho_c, lam], rr)
eq_Phi, eq_rho, eq_lam = [e.lhs - e.rhs for e in eqs]
expected_Phi = -rr ** 2 * (rho_b + rho_c) + sp.diff(rr ** 2 * sp.diff(Phi, rr) / (4 * sp.pi * Gs), rr) - sp.diff(rr ** 2 * lam * rho_c, rr)
P(f"    delta Phi:    (r^2 Phi')'/(4 pi G) - r^2 (rho_b + rho_c) - (r^2 lambda rho_c)' = 0   [sympy EL matches: {sp.simplify(eq_Phi - expected_Phi) == 0 or sp.simplify(eq_Phi + expected_Phi) == 0}]")
P("       => r^2 Phi' = G (M_b + M_c) + 4 pi G r^2 lambda rho_c : g = G (M_b + M_c + M_lambda)/r^2 with M_lambda = 4 pi r^2 lambda rho_c")
P(f"    delta rho_c:  {sp.simplify(eq_rho)} = 0   (mu(rho_c) + Phi - lambda Phi' = const)")
P(f"    delta lambda: {sp.simplify(eq_lam)} = 0   (rho_c Phi' = s)")
ok_ex = sp.simplify(eq_Phi - expected_Phi) == 0 or sp.simplify(eq_Phi + expected_Phi) == 0
# numbers: isothermal fluid sigma0^2 tuned so that the constraint is satisfied at r_M for M_ref = 1e10; lambda rho_c = rho_c (sigma0^2 ln(rho_c/rho_ref) + Phi_tot - mu0)/g, zero at r_M
M_ref = 1e10
rows = []
for Mb_ in (1e10, 1e12):
    p = point_mass(Mb_)
    rMp = math.sqrt(Mb_ * G / A0)
    f_ = target_fields(p, r0=1e-3 * rMp, r1=1e3 * rMp, n=6001)
    rq, rho, gq, u, w = f_["r"], f_["rho"], f_["g"], f_["u"], f_["w"]
    Phi_tot = np.concatenate([[0.0], np.cumsum(0.5 * (gq[1:] + gq[:-1]) * np.diff(rq))])
    s02 = 0.5 * (G * M_ref * A0) ** 0.5                                       # universal sigma0^2 (isothermal EOS), tuned at M_ref
    mu = s02 * np.log(rho) + Phi_tot
    i0_ = int(np.argmin(np.abs(rq - rMp)))
    lam_rho = rho * (mu - mu[i0_]) / gq
    M_lam = 4 * math.pi * rq ** 2 * lam_rho
    Mc = w / G
    out = []
    for xv in (0.1, 0.3, 3.0, 10.0, 30.0):
        i = int(np.argmin(np.abs(rq - xv * rMp)))
        out.append(M_lam[i] / Mc[i])
    rows.append((Mb_, out))
    P(f"    M_b = {Mb_:.0e} (isothermal sigma0^2 tuned at 1e10, constraint imposed to vanish at r_M): M_lambda/M_c at x = 0.1, 0.3, 3, 10, 30: " + ", ".join(f"{v:+.2f}" for v in out))
mx = max(abs(v) for _, o in rows for v in o)
check("C2 (sympy + numbers) implementing (T) as a Lagrange constraint on a barotropic fluid makes the multiplier gravitate: g = G (M_b + M_c + 4 pi r^2 lambda rho_c)/r^2; for an isothermal fluid "
      "M_lambda/M_c reaches >= 0.1 (GR + real mass needs lambda rho_c = 0, i.e. a redundant constraint)", f"multiplier source structure {ok_ex}; max |M_lambda/M_c| = {mx:.2f}",
      bool(ok_ex) and mx >= 0.1)
R.num("C2_rows", rows)

def kappa_fun(kernel, uN, s_):
    nu = KERNELS[kernel]
    y = uN / (s_ ** 2 * A0)
    e = 1e-3
    dnu = (nu(y * (1 + e)) - nu(y * (1 - e))) / (2 * y * e)
    return (nu(y) - 1.0) + y * dnu



# =============================================================================================== C2b  Q2b density-slaved fluid: the reaction
R.banner("C2b  Q2b: density-slaved fluid -- the reaction on the baryons by virtual work (functional derivative validated on the analytic Q3 case)")
from scipy.integrate import cumulative_trapezoid
Mq, hq = 1e10, 2.0
baseq = exp_sphere(Mq, hq)
rMq = math.sqrt(Mq * G / A0)
r0q, r1q, nq = 1e-3 * rMq, 1e3 * rMq, 12001
rgq = np.geomspace(r0q, r1q, nq)
f0q = target_fields(baseq, r0=r0q, r1=r1q, n=nq)
Phi_q = cumulative_trapezoid(f0q["g"], rgq, initial=0.0)
mu_q = Phi_q - Phi_q[-1]                                                     # multiplier: mu = Phi_tot - Phi_tot(R), FIXED while the baryons vary
Mc_q = np.interp(np.log(rgq), np.log(f0q["r"]), f0q["w"]) / G


def bump(s0, width=0.03):
    return lambda r: np.exp(-0.5 * (np.log(r / s0) / width) ** 2)


def func_derivative(E_of_u, s0, rel=1e-4):
    """(delta E/delta u_N)(s0) from E[u_N + eps b] - E[u_N - eps b] with a narrow log-Gaussian bump b (integral over dr divided out)."""
    b = bump(s0)
    eps = rel * float(baseq.u(s0))
    Ep = E_of_u(lambda r: baseq.u(r) + eps * b(r)); Em = E_of_u(lambda r: baseq.u(r) - eps * b(r))
    return (Ep - Em) / (2 * eps) / float(np.trapz(b(rgq), rgq))


def E_q3(u_fun, kernel="P2"):
    uN = u_fun(rgq)
    gph = (KERNELS[kernel](uN / (rgq ** 2 * A0)) - 1.0) * uN / rgq ** 2
    return -float(np.trapz(gph * Mc_q, rgq))


def E_slave(u_fun):
    if MUTATE:
        u_fun = lambda r: baseq.u(r)                                          # enclosed-baryon dependence broken: rho_T does not respond to the baryons
    pr = Profile("pert", Mq, u_fun)
    f_ = target_fields(pr, r0=r0q, r1=r1q, n=nq)
    return float(np.trapz(4 * math.pi * rgq ** 2 * mu_q * f_["rho"], rgq))


ctrl_dev, rows2b = 0.0, []
for xh in (0.5, 1.0, 3.0, 10.0):
    s0 = xh * hq
    num = func_derivative(E_q3, s0)
    ana = -float(kappa_fun("P2", float(baseq.u(s0)), np.array([s0]))[0]) * float(np.interp(np.log(s0), np.log(f0q["r"]), f0q["w"])) / G / s0 ** 2
    ctrl_dev = max(ctrl_dev, abs(num / ana - 1))
    dEdu = func_derivative(E_slave, s0)
    a_b = G * dEdu                                                            # acceleration on a baryon shell (per unit mass); negative = inward
    g_l = (float(baseq.u(s0)) + float(np.interp(np.log(s0), np.log(f0q["r"]), f0q["w"]))) / s0 ** 2
    rows2b.append((xh, a_b, g_l, a_b / g_l))
    P(f"    r = {s0:5.1f} kpc (x = {xh} h): analytic Q3 derivative vs numeric {num / ana - 1:+.1e};  slaved-density reaction a_b = {a_b:+.1f} (km/s)^2/kpc = {a_b / g_l:+.2f} g_law")
check("C2b Q2b the functional-derivative machinery reproduces the analytic Q3 derivative to 5e-3 (bump quadrature), and the reaction of the density-slaved fluid on the baryons is >= 0.5 g_law in magnitude at "
      "r = 0.5, 1, 3, 10 h of the compact exponential sphere (inward, 1.2-4.2 g_law)" + ("  [MUTATE: rho_T made baryon-independent]" if MUTATE else ""),
      f"control deviation {ctrl_dev:.1e}; a_b/g_law = {[round(r_[3], 2) for r_ in rows2b]}", ctrl_dev < 5e-3 and all(abs(r_[3]) >= 0.5 for r_ in rows2b))
R.num("C2b", rows2b)

# =============================================================================================== C3  Q3 kernel-visible fluid: reaction
R.banner("C3  Q3: kernel-visible fluid -- the reaction on the baryons")
prof = exp_sphere(1e10, 2.0)
rMp = math.sqrt(prof.Mtot * G / A0)
rT, wT, uT, uNT = cold_mass(prof, "encl")
Mc_fun = lambda s_: np.interp(np.log(s_), np.log(rT), wT) / G


def dEnergy(kernel, a_, b_, m_):
    """change of E = - Int g_ph(s) M_c(<s) ds when a baryon shell of mass m moves from a_ to b_ (M_b(<s) drops by m on (a_, b_)); the nonlinear kernel is used, no linearisation."""
    s_ = np.linspace(a_, b_, 4001)
    uN = prof.u(s_)
    y0 = uN / (s_ ** 2 * A0); y1 = (uN - G * m_) / (s_ ** 2 * A0)
    g0 = (KERNELS[kernel](y0) - 1.0) * uN / s_ ** 2
    g1 = (KERNELS[kernel](y1) - 1.0) * (uN - G * m_) / s_ ** 2
    return -float(np.trapz((g1 - g0) * Mc_fun(s_), s_))


rows3 = []
maxdev = 0.0
for kn in ("P2", "nu_mono"):
    for xh in (0.5, 1.0, 3.0, 10.0):
        rj = xh * 2.0                                                         # in units of h = 2 kpc
        m = 1e-6 * prof.Mtot
        dl = 1e-4 * rj
        dE = dEnergy(kn, rj, rj + dl, m)
        F_num = -dE / dl                                                      # force on the shell (negative = inward)
        uNj = float(prof.u(rj))
        kap = 0.0 if MUTATE else float(kappa_fun(kn, uNj, np.array([rj]))[0])
        F_an = -m * kap * G * float(Mc_fun(np.array([rj]))[0]) / rj ** 2
        dev3 = abs(F_num / F_an - 1) if F_an != 0 else abs(F_num)
        maxdev = max(maxdev, dev3)
        g_law = float(law_u(prof, np.array([rj]), kn)[0]) / rj ** 2
        react_over_g = abs(F_an) / m / g_law
        rows3.append((kn, rj, kap, react_over_g, 1 + react_over_g, dev3))
        P(f"    {kn:8s} r = {rj:5.1f} kpc (y = {uNj / (rj ** 2 * A0):7.3f}): kappa(y) = {kap:6.3f}; reaction/g_law = {react_over_g:6.3f}; double-counting factor D = {1 + react_over_g:6.3f}; "
          f"formula vs finite-difference: {dev3:.1e}")
check("C3 Q3 the reaction formula -kappa(y) G M_c(<r)/r^2 per unit baryon mass reproduces the finite-difference derivative of the nonlinear energy to 1e-3, and the reaction reaches "
      ">= 0.3 of g_law somewhere on the compact exponential sphere for both kernels" + ("  [MUTATE: kappa = 0]" if MUTATE else ""),
      f"max formula deviation {maxdev:.1e}; max reaction/g_law: P2 {max(r_[3] for r_ in rows3 if r_[0] == 'P2'):.2f}, nu_mono {max(r_[3] for r_ in rows3 if r_[0] == 'nu_mono'):.2f}",
      maxdev < 1e-3 and all(max(r_[3] for r_ in rows3 if r_[0] == k) >= 0.3 for k in ("P2", "nu_mono")))
R.num("C3_rows", rows3)

# deep-regime asymptote of kappa for a point mass (sympy)
ys = sp.symbols("y", positive=True)
nuP2 = sp.sqrt(1 + 1 / ys)
kap_sym = sp.simplify((nuP2 - 1) + ys * sp.diff(nuP2, ys))
P(f"    P2: kappa(y) = {kap_sym};  y -> 0: kappa ~ {sp.limit(kap_sym * sp.sqrt(ys), ys, 0)} y^(-1/2);  y -> oo: {sp.limit(kap_sym * ys ** 2, ys, sp.oo)} / y^2")

# static limit of the kernel-visible fluid with a UNIVERSAL isothermal EOS (sigma0^2 tuned so that M = 1e10 has the target's deep slope -2): rho'/rho = -g_felt/sigma0^2, g_felt = g_law
R.banner("C3b  static limit of Q3 (test-fluid limit) against the target's density slope")
s02 = 0.5 * (G * 1e10 * A0) ** 0.5
rows3b = []
for Mb_ in (1e8, 1e10, 1e12):
    p = point_mass(Mb_)
    rMb = math.sqrt(Mb_ * G / A0)
    out = []
    for xv in (0.3, 1.0, 3.0, 30.0):
        rq = xv * rMb
        g_law_ = float(law_u(p, np.array([rq]), "P2")[0]) / rq ** 2
        slope_iso = -rq * g_law_ / s02                                          # dln rho/dln r of an isothermal test fluid in the law's field
        slope_T = -1.0 - xv ** 2 / (1 + xv ** 2)                                # target (T): rho ~ 1/(x sqrt(1+x^2))
        out.append((xv, slope_iso, slope_T))
    rows3b.append((Mb_, out))
    P(f"    M_b = {Mb_:.0e}: dln rho/dln r at x = 0.3, 1, 3, 30:  isothermal-in-the-law's-field " + ", ".join(f"{o[1]:8.2f}" for o in out) + "   |  target (T) " + ", ".join(f"{o[2]:6.2f}" for o in out))
dev_deep = [abs(o[1] / o[2] - 1) for Mb_, out in rows3b for o in out if Mb_ != 1e10 and o[0] == 30.0]
dev_tuned = [abs(o[1] / o[2] - 1) for Mb_, out in rows3b for o in out if Mb_ == 1e10]
check("C3b an isothermal fluid with a universal sigma0^2 in the law's potential (test-fluid limit) has density slope -V_c^2/sigma0^2: at 1e8 and 1e12 the deep slope is off by 10x "
      "(-0.20 and -20 vs -2); even at the tuned mass 1e10 it is wrong inside r_M-scale radii (x = 1: -2.83 vs -1.50)",
      f"deep-slope errors at M = 1e8, 1e12: {np.round(dev_deep, 2)}; tuned mass at x = 0.3, 1, 3, 30: {np.round(dev_tuned, 2)}", min(dev_deep) >= 0.8 and dev_tuned[1] >= 0.5)

# =============================================================================================== C4  Q4 double counting
R.banner("C4  Q4: double counting (N13) in numbers (point mass)")
share = OMEGA_C_OVER_B
xcap = math.sqrt((1 + share) ** 2 - 1)
P(f"    Omega_c/Omega_b = {share:.3f}  ->  the P2 phantom M_ph(<r) = M (sqrt(1+x^2) - 1) equals the cosmic cold share at x_cap = {xcap:.3f} (r_cap = {xcap * math.sqrt(1e10 * G / A0):.1f} kpc for M_b = 1e10)")
over = {}
for xv in (1.0, 3.0, 10.0, 30.0):
    Mph = math.sqrt(1 + xv * xv) - 1
    add = (1 + Mph + share) / (1 + Mph)
    over[xv] = math.log10(add)
    P(f"    x = {xv:5.1f}: M_ph/M_b = {Mph:6.2f}; additive (phantom + real cold at the cosmic share): g overshoots the law by factor {add:5.2f} = {math.log10(add):+.3f} dex; "
      f"fluid = phantom needs {Mph:.2f} M_b of cold fluid inside r vs {share:.2f} M_b available")
check("C4 Q4 an additive law (phantom + real cold fluid at the cosmic share) overshoots g by >= 0.2 dex at x = 3; the fluid = phantom reading exhausts the cosmic cold share at x_cap = 6.29",
      f"overshoot at x = 3: {over[3.0]:+.3f} dex; x_cap = {xcap:.3f}", over[3.0] >= 0.2 and abs(xcap - 6.29) < 0.02)

# =============================================================================================== C5  Q5 temperature-slaved fluid: attractor
R.banner("C5  Q5: a self-gravitating fluid with prescribed dispersion sigma^2(r) -- attractor property (point mass)")
M = 1e10
pm = point_mass(M)
rM = math.sqrt(M * G / A0)
f_ = target_fields(pm, r0=1e-3 * rM, r1=1e3 * rM, n=20001)
r_ = f_["r"]


def s2_of(rr_, scale=1.0):
    x_ = rr_ / rM
    return scale * 0.5 * G * M * np.sqrt(1 + x_ * x_) / rr_                # (1/2) V_c^2 of the target: (1/2) sqrt((G M/r)^2 + G M a0)


def run(amp, scale, selfgrav=True, r_lo=1e-2):
    def rhs(s, y):
        rq = math.exp(s)
        lrho, Mc = y
        gq = (G * M + (G * Mc if selfgrav else 0.0)) / rq ** 2
        e = 1e-6
        ds = (s2_of(rq * (1 + e), scale) - s2_of(rq * (1 - e), scale)) / (2 * rq * e)
        return [-rq * (gq + ds) / s2_of(rq, scale), 4 * math.pi * rq ** 3 * math.exp(min(lrho, 300))]
    r0 = r_lo * rM
    rho0 = amp * float(np.interp(r0, r_, f_["rho"])); Mc0 = float(np.interp(r0, r_, f_["w"])) / G
    xs = np.array([0.1, 1.0, 10.0, 30.0, 100.0, 1000.0]) * rM
    sol = solve_ivp(rhs, (math.log(r0), math.log(xs[-1])), [math.log(rho0), Mc0], t_eval=np.log(xs), rtol=1e-10, atol=1e-30, method="DOP853")
    return xs, (G * M + G * sol.y[1]) / xs ** 2                                   # g_tot at xs


xs, g_ref = run(1.0, 1.0)
uex = np.array([G * M * math.sqrt(1 + (x_ / rM) ** 2) / x_ ** 2 for x_ in xs])
P("    reference (amplitude 1, sigma^2 scale 1) vs closed-form P2: max |g/g_P2 - 1| = %.1e" % float(np.max(np.abs(g_ref / uex - 1))))
tab = {}
for lab, amp, sc in (("amp x2", 2.0, 1.0), ("amp x0.5", 0.5, 1.0), ("amp x4", 4.0, 1.0), ("sigma^2 x1.2", 1.0, 1.2)):
    _, g_ = run(amp, sc, selfgrav=not MUTATE)
    if MUTATE:
        _, g_r = run(1.0, 1.0, selfgrav=False)
        tab[lab] = g_ / g_r - 1
    else:
        tab[lab] = g_ / g_ref - 1
    P(f"    {lab:13s}: g_tot/g_ref - 1 at x = 0.1, 1, 10, 30, 100, 1000: " + ", ".join(f"{v:+.4f}" for v in tab[lab]))
att_ok = all(abs(tab[k][-1]) < 0.02 for k in ("amp x2", "amp x0.5", "amp x4")) and all(abs(tab[k][1]) >= 0.05 for k in ("amp x2", "amp x0.5"))
P("    decay of the amplitude-x4 offset (damped Emden-type oscillation): |dg/g| at x = 10, 30, 100, 1000: " + ", ".join(f"{abs(v):.4f}" for v in tab["amp x4"][2:]))
vf_ok = abs(1 + tab["sigma^2 x1.2"][-1] - 1.2) < 0.05
check("C5 Q5 the outer profile is an ATTRACTOR (amplitude x0.5, x2, x4 change g_tot by < 2% at x = 1000 but by >= 5% at x = 1) and V_f^2 follows sigma^2 (x 1.2 -> g_flat x 1.2 within 5%)"
      + ("  [MUTATE: fluid without self-gravity]" if MUTATE else ""), f"attractor {att_ok}; sigma^2 scaling {vf_ok}", bool(att_ok) and bool(vf_ok))
R.num("C5", {k: list(map(float, v)) for k, v in tab.items()})

# extended baryons: prescribe sigma^2 = sigma_t^2(r) of (T) (exponential sphere h = 2, M = 1e10) and vary the amplitude
R.banner("C5b  Q5 on extended baryons: (T)'s own sigma^2(r) = (1/2) V_c^2 [1 + 4 pi r^2 Sigma_out/M_b] prescribed, amplitude varied")
pe = exp_sphere(1e10, 2.0)
rMe = math.sqrt(pe.Mtot * G / A0)
fe = target_fields(pe, r0=1e-3 * rMe, r1=1e3 * rMe, n=20001)
re_ = fe["r"]
Mb_e = fe["uN"] / G
Sg_e = pe.Mtot * np.exp(-re_ / 2.0) / (8 * math.pi * 2.0 ** 2)
s2_tab = 0.5 * re_ * fe["g"] * (1 + 4 * math.pi * re_ ** 2 * Sg_e / Mb_e)
ln_s2 = np.log(s2_tab)
s2e = lambda rr_: np.exp(np.interp(np.log(rr_), np.log(re_), ln_s2))
def run_e(amp, selfgrav=True):
    def rhs(s, y):
        rq = math.exp(s); lrho, Mc = y
        gq = (float(pe.u(rq)) + (G * Mc if selfgrav else 0.0)) / rq ** 2
        e = 1e-3
        ds = (s2e(rq * (1 + e)) - s2e(rq * (1 - e))) / (2 * rq * e)
        return [-rq * (gq + ds) / s2e(rq), 4 * math.pi * rq ** 3 * math.exp(min(lrho, 300))]
    r0 = 1e-2 * rMe
    xs_ = np.array([0.1, 1.0, 10.0, 100.0, 1000.0]) * rMe
    sol = solve_ivp(rhs, (math.log(r0), math.log(xs_[-1])), [math.log(amp * float(np.interp(r0, re_, fe["rho"]))), float(np.interp(r0, re_, fe["w"])) / G],
                    t_eval=np.log(xs_), rtol=1e-9, atol=1e-30, method="DOP853")
    return xs_, (pe.u(xs_) + G * sol.y[1]) / xs_ ** 2
xe, ge_ref = run_e(1.0)
uT_at = np.interp(np.log(xe), np.log(re_), fe["u"]) / xe ** 2
P("    amplitude 1 vs (T): g_tot/g_T - 1 at x = 0.1, 1, 10, 100, 1000: " + ", ".join(f"{v:+.4f}" for v in (ge_ref / uT_at - 1)))
tabe = {}
for lab, amp in (("amp x2", 2.0), ("amp x0.5", 0.5)):
    _, ge = run_e(amp, selfgrav=not MUTATE)
    tabe[lab] = ge / ge_ref - 1
    P(f"    {lab:9s}: g_tot/g_ref - 1 at x = 0.1, 1, 10, 100, 1000: " + ", ".join(f"{v:+.4f}" for v in tabe[lab]))
ok_e = all(abs(tabe[k][-1]) < 0.02 for k in tabe) and all(abs(tabe[k][1]) >= 0.02 for k in tabe)
check("C5b Q5 on the compact exponential sphere: with (T)'s own sigma^2(r) prescribed, the outer profile is again an attractor (amplitude x2, x0.5: < 2% at x = 1000) while the inner region "
      "(x = 1) keeps the amplitude (>= 2%)" + ("  [MUTATE: no self-gravity]" if MUTATE else ""), f"deviations at x = 1000: { {k: round(float(v[-1]), 4) for k, v in tabe.items()} }", bool(ok_e))
R.num("C5b", {k: list(map(float, v)) for k, v in tabe.items()})

nf = R.write()
sys.exit(1 if nf else 0)
