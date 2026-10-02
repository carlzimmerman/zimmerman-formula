#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG288 STAGE A -- PRE-FLIGHT THEOREMS FOR "ONE FIELD: BACKGROUND = THE DARK ENERGY, CLUMPS = THE COLD COMPONENT".

Frozen in FROZEN_CRITERIA.md section 4 (committed before this script; its sha256 is printed below).  In one line each:
  A1  potential / oscillation road.  rho = phidot^2/2 + V - V_min is non-increasing (d rho/dt = -3 H phidot^2, sympy exact); a
      |phi|^(2n) minimum averages to <w> = (n-1)/(n+1) (sympy, Beta functions); so a component that is dust-like from a_d on obeys
      rho_0 <= Delta V a_d^3, i.e. Delta V >= (Omega_c/Omega_Lambda) rho_Lambda (1+z_d)^3.  Claim tested: a potential whose one scale
      is tied to rho_Lambda (height <= 1e3 rho_Lambda) cannot supply the dust.  Numerical control: the radiation-era Klein-Gordon
      solution against the exact Bessel solution.
  A2  shift-charge road.  P(X) on FRW: d(a^3 P_X phidot)/dt = 0 exactly; the charge C is an integration constant no action parameter
      fixes; rho_d = sqrt(2 X0) C a^-3, c_s^2 = rho_d/(4 M^4), w = c_s^2/2; coldness needs a second scale M; a seeding event needs a
      reservoir >= rho_c(z_s) -- the reservoirs at recombination are scored.
  A3  derived mass scale: m_q = Mbar_Pl^(1-q) (hbar H_Lambda)^q, hbar a0/c^3 (both footings), rho_Lambda^(1/4), against the window
      [2e-20 eV (Lyman-alpha), the classical-field limit].
MODES: MUTATE=0 main; MUTATE=1 the kinetic sign flipped (a ghost): A1.1's monotonicity check must FAIL (rc 1).
kappa = 1/2 FITTED.  No dark-matter particle species: a cold component made of the field's oscillation is a classical field whose
quanta would be light bosons; the cold MASS is still required.  Nothing here says the theory is closed or that the data favour the
framework.
Run: python3 campaign_fresh_gravity/CFG288_one_field_dark_sector/cfg288_stageA_theorems.py   (MUTATE=1 for the control)
"""
import sys
sys.dont_write_bytecode = True
import os, math, json, time, hashlib
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.special import jv, gamma as Gam

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C

MODE = int(os.environ.get("MUTATE", "0"))
SLUG = "cfg288_stageA_theorems" + (f"_MUTATE{MODE}" if MODE else "")
R = C.Report(SLUG, False)
P, check, num = R.P, R.check, R.num
T0 = time.time()
P(__doc__.split("Run: python3")[0].strip())
FROZEN = os.path.join(HERE, "FROZEN_CRITERIA.md")
P(f"\n  FROZEN_CRITERIA.md sha256 {hashlib.sha256(open(FROZEN, 'rb').read()).hexdigest()}")
if MODE == 1:
    P("\n  *** MUTATE=1: kinetic sign flipped (a ghost) -- A1.1's monotonicity check must FAIL ***")
LB0 = MODE == 0          # in MUTATE runs only the mode's own check is load-bearing

# ================================================================================================ constants (frozen ledger, section 2)
c = 2.99792458e8; G = 6.67430e-11; hbar = 1.054571817e-34; eV = 1.602176634e-19; kB = 1.380649e-23
MPC = 3.0856775814913673e22
HC_EVM = hbar * c / eV                         # hbar c in eV m
h = 0.6736; H0 = 100 * h * 1e3 / MPC           # s^-1
ob, oc = 0.02237, 0.1200
mnu = 0.06; onu_m = mnu / 93.14                # one massive neutrino, today non-relativistic
TCMB = 2.7255; NEFF = 3.046
rho_crit = 3 * H0 ** 2 / (8 * math.pi * G)     # kg/m^3
og = (math.pi ** 2 / 15) * (kB * TCMB) ** 4 / (hbar * c) ** 3 / c ** 2 / (rho_crit / h ** 2)   # omega_gamma
o_r = og * (1 + NEFF * 7 / 8 * (4 / 11) ** (4 / 3))     # all neutrinos relativistic (true at z >= 1e3)
Om = (ob + oc + onu_m) / h ** 2
Orad0 = og * (1 + (NEFF - 1.0153) * 7 / 8 * (4 / 11) ** (4 / 3)) / h ** 2   # massless part today (2.0306 + photons), for closure only
OL = 1 - Om - Orad0
Oc, Ob = oc / h ** 2, ob / h ** 2
RATIO = Oc / OL                                 # Omega_c / Omega_Lambda today
rhoL = OL * rho_crit                            # kg/m^3
def to_eV4(rho_kgm3):
    return rho_kgm3 * c ** 2 / eV * HC_EVM ** 3
rhoL_eV4 = to_eV4(rhoL)
MPL = math.sqrt(hbar * c / (8 * math.pi * G)) * c ** 2 / eV       # reduced Planck mass, eV
HL_eV = hbar * H0 * math.sqrt(OL) / eV                            # hbar H_Lambda, eV
H0_eV = hbar * H0 / eV
def H_eV(z):                                     # hbar H(z), eV (radiation with all neutrinos relativistic at high z)
    return H0_eV * math.sqrt(o_r / h ** 2 * (1 + z) ** 4 + (ob + oc) / h ** 2 * (1 + z) ** 3 + OL)
M_MIN = 2e-20                                    # eV, Lyman-alpha (Rogers & Peiris 2021), the record's merger-gate quote
ZGRID = [1100.0, 3400.0, 1e4, 1e5, 1e6, 1e7]
P(f"\n  ledger: h {h}, omega_b {ob}, omega_c {oc}, omega_gamma {og:.4e}, omega_r(z>=1e3) {o_r:.4e}, Omega_m {Om:.5f}, Omega_Lambda {OL:.5f}")
P(f"          Omega_c/Omega_Lambda = {RATIO:.5f};  rho_Lambda = {rhoL:.4e} kg/m^3 = {rhoL_eV4:.4e} eV^4 (rho_Lambda^(1/4) = {rhoL_eV4 ** 0.25 * 1e3:.4f} meV)")
P(f"          Mbar_Pl = {MPL:.5e} eV; hbar H_Lambda = {HL_eV:.4e} eV; hbar H0 = {H0_eV:.4e} eV")
num("ledger", dict(h=h, ob=ob, oc=oc, og=og, o_r=o_r, Om=Om, OL=OL, ratio_c_L=RATIO, rhoL_kgm3=rhoL, rhoL_eV4=rhoL_eV4,
                   rhoL_quarter_meV=rhoL_eV4 ** 0.25 * 1e3, MPL_eV=MPL, HL_eV=HL_eV, H0_eV=H0_eV))

# ================================================================================================ A1
R.banner("A1  POTENTIAL / OSCILLATION ROAD: the oscillation energy is bounded by the potential's height")
t = sp.symbols("t", real=True)
s_kin = sp.Integer(-1) if MODE == 1 else sp.Integer(1)      # +1 healthy, -1 ghost (MUTATE)
a = sp.Function("a", positive=True)(t)
phi = sp.Function("phi", real=True)(t)
Vf = sp.Function("V")
Vmin = sp.symbols("V_min", real=True)
Lag = a ** 3 * (s_kin * sp.Rational(1, 2) * phi.diff(t) ** 2 - Vf(phi))
EL = sp.euler_equations(Lag, [phi], [t])[0].lhs            # = 0
phidd = sp.solve(EL, phi.diff(t, 2))[0]
rho = s_kin * sp.Rational(1, 2) * phi.diff(t) ** 2 + Vf(phi) - Vmin
drho = sp.diff(rho, t).subs(phi.diff(t, 2), phidd)
Hs = a.diff(t) / a
resid_healthy = sp.simplify(drho - (-3 * Hs * phi.diff(t) ** 2))
coef = sp.simplify(drho / (Hs * phi.diff(t) ** 2))
P(f"    d rho/dt from the Euler-Lagrange equation = {sp.simplify(drho)}  ->  coefficient of H phidot^2: {coef}")
mono = (coef == -3)
check("A1.1 [exact, sympy] d rho/dt = -3 H phidot^2 <= 0 for rho = s phidot^2/2 + V - V_min (s = the kinetic sign in the action)"
      + (" [MUTATE: must FAIL]" if MODE == 1 else ""),
      f"kinetic sign s = {int(s_kin)}; d rho/dt / (H phidot^2) = {coef}; monotone non-increasing: {mono}", mono, load_bearing=True)

# A1.2 virial average for V = lambda |phi|^(2n)
P("\n    A1.2: cycle average of w for V - V_min = lambda |phi|^(2n) (u = phi/phi_max, dt ~ du / sqrt(1 - u^(2n)))")
nn = sp.symbols("n", positive=True)
def beta_int(p, q):     # int_0^1 (1 - u^p)^q du = Gamma(1/p + 1) Gamma(q + 1) / Gamma(1/p + q + 1)
    return sp.gamma(1 / p + 1) * sp.gamma(q + 1) / sp.gamma(1 / p + q + 1)
I1 = beta_int(2 * nn, sp.Rational(1, 2)); I2 = beta_int(2 * nn, -sp.Rational(1, 2))
w_target = (nn - 1) / (nn + 1)
w_avg = sp.simplify(sp.gammasimp(sp.expand_func(2 * I1 / I2 - 1)))
okA12 = sp.simplify(sp.gammasimp(sp.expand_func(2 * I1 / I2 - 1 - w_target))) == 0
u = sp.symbols("u", positive=True)
direct = {}
for n_ in (1, 2):
    i1 = sp.integrate(sp.sqrt(1 - u ** (2 * n_)), (u, 0, 1)); i2 = sp.integrate(1 / sp.sqrt(1 - u ** (2 * n_)), (u, 0, 1))
    direct[n_] = sp.nsimplify(sp.N(2 * i1 / i2 - 1, 30), rational=True, tolerance=1e-20)
P(f"    <w>(n) = {w_avg}  (target (n-1)/(n+1)); direct quadrature: n=1 -> {direct[1]}, n=2 -> {direct[2]}")
check("A1.2 [exact, sympy] <w> = (n-1)/(n+1) for a |phi|^(2n) minimum (n = 1 dust-like; n >= 2 dilutes faster than a^-3)",
      f"Beta-function form simplifies to (n-1)/(n+1): {okA12}; direct n=1: {direct[1]}, n=2: {direct[2]}",
      okA12 and direct[1] == 0 and direct[2] == sp.Rational(1, 3), load_bearing=LB0)

# A1.3 the bound and its numbers
P("\n    A1.3: dust-like from a_d on and rho non-increasing  =>  rho_0 = rho(a_d) a_d^3 <= Delta V a_d^3")
P("          Delta V_min / rho_Lambda = (Omega_c / Omega_Lambda)(1 + z_d)^3")
A1 = {}
for zd in ZGRID:
    r = RATIO * (1 + zd) ** 3
    A1[zd] = dict(dV_over_rhoL=r, dV_quarter_eV=(r * rhoL_eV4) ** 0.25, tuning_Vmin_over_dV=1 / r)
    P(f"      z_d = {zd:9.3g}:  Delta V/rho_Lambda >= {r:.4e};  Delta V^(1/4) >= {(r * rhoL_eV4) ** 0.25:.4e} eV;  V_min/Delta V <= {1 / r:.3e}")
# the wave field at m = m_min: onset H = m (full H(z)) and the exact radiation-era Bessel number
from scipy.optimize import brentq
z_on_mmin = brentq(lambda z: H_eV(z) - M_MIN, 10.0, 1e12)
Cinf = Gam(1.25) ** 2 * math.sqrt(2) / math.pi
Or_h = o_r / h ** 2
dV_over_rho0_exact = (1 / (2 * Cinf)) * (M_MIN / (2 * H0_eV * math.sqrt(Or_h))) ** 1.5
dV_over_rhoL_wave = RATIO * dV_over_rho0_exact
P(f"      wave field at m = m_min = {M_MIN:.0e} eV: H(z_on) = m at z_on = {z_on_mmin:.4e}  ->  Delta V/rho_Lambda >= {RATIO * (1 + z_on_mmin) ** 3:.4e} (bound at z_d = z_on)")
P(f"        exact radiation-era Klein-Gordon (Bessel, constant g*):  Delta V/rho_0 = (1/(2 C_inf)) (m/(2 H0 sqrt(Omega_r)))^(3/2) = {dV_over_rho0_exact:.4e},"
  f"  Delta V/rho_Lambda = {dV_over_rhoL_wave:.4e}")
A1["m_min"] = dict(z_on=z_on_mmin, dV_over_rhoL_bound_at_zon=RATIO * (1 + z_on_mmin) ** 3, dV_over_rhoL_exact=dV_over_rhoL_wave,
                   dV_quarter_eV=(dV_over_rhoL_wave * rhoL_eV4) ** 0.25)
num("A1", {str(k): v for k, v in A1.items()})
okA14 = all(A1[zd]["dV_over_rhoL"] > 1e3 for zd in ZGRID if zd >= 3400)
check("A1.4 [claim] a single field whose potential has ONE scale tied to rho_Lambda (height <= 1e3 rho_Lambda) cannot supply the dust "
      "(PROVED iff Delta V_min/rho_Lambda > 1e3 at z_d = 3400 and above)",
      f"Delta V_min/rho_Lambda = {A1[3400.0]['dV_over_rhoL']:.3e} at z_d = 3400 (x{A1[3400.0]['dV_over_rhoL'] / 1e3:.1e} over the generous 1e3); "
      f"so the potential needs a second scale >= {A1[3400.0]['dV_quarter_eV']:.3f} eV and the dark energy is a residual tuned to "
      f"V_min/Delta V <= {A1[3400.0]['tuning_Vmin_over_dV']:.2e}", okA14, load_bearing=LB0)

# A1 numerical control: radiation-era KG vs Bessel
P("\n    A1 numerical control: phi'' + (3/2x) phi' + s^-1 phi = 0 (x = m t, radiation era), phi(0) = 1")
x0, x1 = 1e-4, 3e3
def bessel_phi(x):
    return Gam(1.25) * (x / 2) ** (-0.25) * jv(0.25, x)
def bessel_dphi(x):  # d/dx [Gamma(5/4)(x/2)^(-1/4) J_(1/4)(x)] = -Gamma(5/4) (x/2)^(-1/4) J_(5/4)(x)
    return -Gam(1.25) * (x / 2) ** (-0.25) * jv(1.25, x)
sgn = float(s_kin)
def rhs(x, y):
    return [y[1], -1.5 / x * y[1] - y[0] / sgn]    # healthy: phi'' = -3H phi' - V'; ghost: phi'' = -3H phi' + V'
if MODE == 1:
    x1 = 30.0                                   # the ghost runs away exponentially; integrate only to x = 30 (before overflow)
xs = np.unique(np.concatenate([np.geomspace(x0, 10, 4000), np.linspace(10, x1, 300001)]))
sol = solve_ivp(rhs, (x0, x1), [bessel_phi(x0), bessel_dphi(x0)], t_eval=xs, rtol=1e-12, atol=1e-14, method="DOP853")
ph, dph = sol.y
rho_num = sgn * 0.5 * dph ** 2 + 0.5 * ph ** 2
if MODE == 0:
    err_b = float(np.max(np.abs(ph - bessel_phi(xs))))
    drel = np.diff(rho_num) / rho_num[:-1]
    max_up = float(np.max(drel))
    win = (xs >= 1000) & (xs <= 3000)
    avg = float(np.trapz(rho_num[win] * xs[win] ** 1.5, xs[win]) / (xs[win][-1] - xs[win][0]))
    P(f"      max |phi_num - phi_Bessel| = {err_b:.2e};  max relative step increase of rho = {max_up:.2e};  <rho x^1.5>[1e3,3e3] = {avg:.6f} vs C_inf = {Cinf:.6f}")
    ok_ctrl = err_b < 1e-6 and max_up < 1e-10 and abs(avg / Cinf - 1) < 1e-3
    check("A1-CTRL [numerical; can fail] the ODE matches the exact Bessel solution to 1e-6, rho is non-increasing at every step to 1e-10, "
          "and <rho x^1.5> over [1e3, 3e3] equals Gamma(5/4)^2 sqrt(2)/pi to 1e-3",
          f"Bessel error {err_b:.2e}; max step increase {max_up:.2e}; <rho x^1.5>/C_inf - 1 = {avg / Cinf - 1:+.2e}", ok_ctrl, load_bearing=True)
    num("A1_ctrl", dict(err_bessel=err_b, max_step_increase=max_up, avg_rho_x15=avg, Cinf=Cinf))
    # reported: quartic (n = 2) is radiation-like
    def rhs4(x, y):
        return [y[1], -1.5 / x * y[1] - y[0] ** 3]
    # average over COMPLETE cycles (between the first and last maxima of phi in [1e3, 3e4]); a first version averaged over a fixed
    # window [1e3, 2e3] that held only ~2.5 cycles (<w> = 0.3066) -- a numerical-window fix, disclosed in the README
    s4 = solve_ivp(rhs4, (x0, 3e4), [1.0, 0.0], t_eval=np.linspace(1e3, 3e4, 2000001), rtol=1e-11, atol=1e-14, method="DOP853")
    ph4, dph4 = s4.y
    imax = np.where((dph4[:-1] > 0) & (dph4[1:] <= 0))[0]
    i0, i1 = imax[0], imax[-1]
    K4 = 0.5 * dph4[i0:i1 + 1] ** 2; V4 = 0.25 * ph4[i0:i1 + 1] ** 4; tt4 = s4.t[i0:i1 + 1]
    w4 = float(np.trapz(K4 - V4, tt4) / np.trapz(K4 + V4, tt4))
    P(f"      reported: quartic V = phi^4/4, <w> over {len(imax) - 1} complete cycles in x = [{tt4[0]:.0f}, {tt4[-1]:.0f}] = {w4:.4f} (target 1/3)")
    check("A1-REP (reported) quartic minimum: <w> = 1/3 to 1e-2", f"<w> = {w4:.4f}", abs(w4 - 1 / 3) < 1e-2, load_bearing=False)
    num("A1_quartic_w", w4)
else:
    fin = np.isfinite(rho_num)
    dr = np.diff(rho_num[fin])
    frac_up = float(np.mean(dr > 0)); grow = float(rho_num[fin][-1] / rho_num[fin][0])
    P(f"      MUTATE (ghost), x <= 30: fraction of steps where rho increases = {frac_up:.3f}; rho(x=30)/rho(x0) = {grow:.3e} (the energy grows)")
    num("A1_ghost_numeric", dict(frac_steps_rho_up=frac_up, rho_end_over_start=grow))

# ================================================================================================ A2
R.banner("A2  SHIFT-CHARGE ROAD: the dust is a conserved charge (an integration constant)")
Pf = sp.Function("P")
Xs = sp.symbols("X", positive=True)
Lag2 = a ** 3 * Pf(phi.diff(t) ** 2 / 2)
EL2 = sp.euler_equations(Lag2, [phi], [t])[0].lhs
charge = a ** 3 * sp.diff(Pf(Xs), Xs).subs(Xs, phi.diff(t) ** 2 / 2) * phi.diff(t)
resA21 = sp.simplify(EL2 + sp.diff(charge, t))
P(f"    Euler-Lagrange + d/dt(a^3 P_X phidot) = {resA21}")
check("A2.1 [exact, sympy] for shift-symmetric P(X) on FRW the equation of motion is d(a^3 P_X phidot)/dt = 0: a^3 P_X phidot = C",
      f"residual {resA21}", resA21 == 0, load_bearing=LB0)

rL, M4, X0, Cc, aa = sp.symbols("rho_Lambda M4 X0 C a", positive=True)
dX = sp.symbols("deltaX", positive=True)
Pspec = -rL + M4 / 2 * (Xs / X0 - 1) ** 2
PX = sp.diff(Pspec, Xs); PXX = sp.diff(Pspec, Xs, 2)
fX = PX * sp.sqrt(2 * Xs)                        # a^3 f(X) = C
dfX = sp.simplify(sp.diff(fX, Xs))
# f(X0) = 0, f increasing for X > X0  =>  unique X(a) for every C > 0
fX0 = sp.simplify(fX.subs(Xs, X0))
dfX_sub = sp.simplify(dfX.subs(Xs, X0 * (1 + dX)))
pos = sp.simplify(dfX_sub * sp.sqrt(2 * X0 * (1 + dX)) * X0 ** 2 / M4)   # strip positive factors
P(f"    f(X) = P_X sqrt(2X): f(X0) = {fX0}; f'(X0(1+d)) x positive factors = {sp.expand(pos)}  (> 0 for d > 0)")
pos_poly = sp.Poly(sp.expand(pos), dX)
okA22 = (fX0 == 0) and all(cf > 0 for cf in pos_poly.all_coeffs())     # all coefficients positive => f' > 0 for every d > 0
check("A2.2 [exact] for P = -rho_Lambda + (M^4/2)(X/X0 - 1)^2 a solution exists for EVERY C > 0 at fixed action parameters "
      "(a^3 P_X sqrt(2X) = C with f(X0) = 0, f' > 0 above X0): C is not fixed by any action parameter",
      f"f(X0) = {fX0}; f'(X0(1+d)) x positive factors = {sp.expand(pos)} (all coefficients > 0)", okA22, load_bearing=LB0)

# leading order: rho_d, c_s^2, w
eps = sp.symbols("epsilon", positive=True)
Xsol = X0 + eps * sp.symbols("x1") + eps ** 2 * sp.symbols("x2")
x1, x2 = sp.symbols("x1 x2")
eq = sp.series((aa ** 3 * fX.subs(Xs, Xsol) - eps * Cc), eps, 0, 3).removeO()
sol12 = sp.solve([sp.expand(eq).coeff(eps, 1), sp.expand(eq).coeff(eps, 2)], [x1, x2], dict=True)[0]
Xser = Xsol.subs(sol12)
rho_expr = 2 * Xs * PX - Pspec
rho_ser = sp.series(rho_expr.subs(Xs, Xser), eps, 0, 2).removeO()
rho_d1 = sp.simplify(sp.expand(rho_ser - rL).coeff(eps, 1))
cs2_expr = PX / (PX + 2 * Xs * PXX)
cs2_ser = sp.simplify(sp.series(cs2_expr.subs(Xs, Xser), eps, 0, 2).removeO().coeff(eps, 1))
Pd_ser = sp.series((Pspec + rL).subs(Xs, Xser), eps, 0, 3).removeO()
w_lead = sp.simplify(sp.expand(Pd_ser).coeff(eps, 2) / rho_d1)       # w = P_d/rho_d = (eps^2 term)/(eps term): leading order O(eps)
okd = sp.simplify(rho_d1 - sp.sqrt(2 * X0) * Cc / aa ** 3) == 0
okc = sp.simplify(cs2_ser - rho_d1 / (4 * M4)) == 0
okw = sp.simplify(w_lead - cs2_ser / 2) == 0
indep = (sp.diff(rho_d1, rL) == 0) and (sp.diff(rho_d1, M4) == 0)
P(f"    rho_d (O(C)) = {rho_d1};  c_s^2 (O(C)) = {cs2_ser};  w (O(C)) = {w_lead}")
check("A2.3 [sympy, leading order in C] rho_d = sqrt(2 X0) C a^-3 with d rho_d/d rho_Lambda = d rho_d/d M^4 = 0; c_s^2 = rho_d/(4 M^4); "
      "w = c_s^2/2",
      f"rho_d ok {okd}; independence of (rho_Lambda, M^4) {indep}; c_s^2 ok {okc}; w ok {okw}", okd and okc and okw and indep,
      load_bearing=LB0)

# A2.4 coldness numbers
def rho_c_over_rhoL(z):
    return RATIO * (1 + z) ** 3
M4min = {z: rho_c_over_rhoL(z) / (4 * 1e-5) for z in (1100.0, 3400.0)}
cs2_single = {z: rho_c_over_rhoL(z) / (4 * 1e3) for z in (1100.0, 3400.0)}
cs2_M4eqL = rho_c_over_rhoL(1100.0) / 4
P(f"    coldness (c_s^2 <= 1e-5): M^4/rho_Lambda >= {M4min[1100.0]:.3e} at z = 1100 (M >= {(M4min[1100.0] * rhoL_eV4) ** 0.25:.3f} eV); "
  f">= {M4min[3400.0]:.3e} at z = 3400 (M >= {(M4min[3400.0] * rhoL_eV4) ** 0.25:.3f} eV)")
P(f"    single scale: M^4 = 1e3 rho_Lambda -> c_s^2(1100) = {cs2_single[1100.0]:.3e}; M^4 = rho_Lambda -> c_s^2(1100) = {cs2_M4eqL:.3e} "
  f"(>> 1: not even in the dust regime)")
num("A2_coldness", dict(M4min_over_rhoL_z1100=M4min[1100.0], M_min_eV_z1100=(M4min[1100.0] * rhoL_eV4) ** 0.25,
                        M4min_over_rhoL_z3400=M4min[3400.0], M_min_eV_z3400=(M4min[3400.0] * rhoL_eV4) ** 0.25,
                        cs2_1100_single_1e3=cs2_single[1100.0], cs2_1100_M4_eq_rhoL=cs2_M4eqL))
check("A2.4 [finding] a ghost condensate whose ONE scale is tied to rho_Lambda (M^4 <= 1e3 rho_Lambda) holds Omega_c CMB-cold "
      "(c_s^2(1100) <= 1e-5)",
      f"c_s^2(1100) = {cs2_single[1100.0]:.2e} at M^4 = 1e3 rho_Lambda; cold needs M >= {(M4min[1100.0] * rhoL_eV4) ** 0.25:.2f} eV "
      f"(M^4 >= {M4min[1100.0]:.2e} rho_Lambda): a second scale, and P(X0) = -rho_Lambda is then tuned to rho_Lambda/M^4 <= {1 / M4min[1100.0]:.1e}",
      cs2_single[1100.0] <= 1e-5, load_bearing=LB0)

# A2.5 seeding reservoirs at z_s = 1100
zs = 1100.0
m_H_eV, m_He_eV = 938.783e6, 3727.379e6                       # hydrogen atom, helium-4 nucleus rest energies
YP = 0.245
need_over_rhob = oc / ob                                        # rho_c(z)/rho_b(z) (both a^-3)
H_bind = 13.598 * (1 - YP) / m_H_eV                             # per unit baryon rest energy: n_H = (1 - Y_p) rho_b / m_H
He_bind = 79.005 * YP / m_He_eV                                 # n_He = Y_p rho_b / m_He; 79.005 eV for both electrons
atomic = H_bind + He_bind
res = dict(
    hydrogen_binding=H_bind / need_over_rhob,
    all_atomic_binding=atomic / need_over_rhob,
    all_cmb_photons=(og / oc) * (1 + zs),
    firas_allowed_photons=6e-5 * (og / oc) * (1 + zs),
    all_radiation=(o_r / oc) * (1 + zs))
P(f"    seeding at z_s = {zs:.0f}: needed energy = rho_c(z_s) = {rho_c_over_rhoL(zs):.3e} rho_Lambda = {need_over_rhob:.3f} rho_b(z_s)")
for k, v in res.items():
    P(f"      reservoir {k:24s}: available / needed = {v:.3e}  ({'can' if v >= 1 else 'cannot'} supply; short by x{1 / v:.2e})")
P(f"      reservoir vacuum / potential       : needs a vacuum >= rho_c(z_s) = {rho_c_over_rhoL(zs):.3e} rho_Lambda (not the rho_Lambda that sets a0) -> the A1 bound + the CAMB row")
num("A2_reservoirs_z1100", res)
num("A2_vacuum_need_over_rhoL", {str(z): rho_c_over_rhoL(z) for z in ZGRID})
for k in ("hydrogen_binding", "all_atomic_binding", "all_cmb_photons", "firas_allowed_photons", "all_radiation"):
    check(f"A2.5 [finding] recombination seeding: the {k.replace('_', ' ')} reservoir supplies rho_c(1100) (available/needed >= 1)",
          f"available/needed = {res[k]:.3e}", res[k] >= 1, load_bearing=LB0)

# ================================================================================================ A3
R.banner("A3  THE DERIVED MASS SCALE: which masses the framework's own constants give, against the allowed window")
qs = [(sp.Integer(0), "0"), (sp.Rational(1, 4), "1/4"), (sp.Rational(1, 3), "1/3"), (sp.Rational(1, 2), "1/2"),
      (sp.Rational(2, 3), "2/3"), (sp.Rational(3, 4), "3/4"), (sp.Integer(1), "1")]
rho_loc = 0.4e9 * (HC_EVM * 100) ** 3                      # 0.4 GeV/cm^3 in eV^4 (hbar c in eV cm)
v_loc = 220e3 / c
m_max = (rho_loc * (2 * math.pi) ** 3 / v_loc ** 3) ** 0.25
P(f"    window: m_min = {M_MIN:.1e} eV (Lyman-alpha); m_max = {m_max:.3f} eV (n lambda_dB^3 = 1 at 0.4 GeV/cm^3, 220 km/s); "
  f"{math.log10(m_max / M_MIN):.1f} decades")
P("    onset floors m >= hbar H(z_req) for the seeding grid (reported): " +
  "; ".join(f"z {z:.0e}: {H_eV(z):.2e} eV" for z in ZGRID))
cands = {}
for q, lab in qs:
    m = MPL ** (1 - float(q)) * HL_eV ** float(q)
    cands[f"q={lab}"] = m
cands["hbar a0/c^3 canonical"] = hbar * C.A0_SI["canonical"] / c / eV
cands["hbar a0/c^3 alt"] = hbar * C.A0_SI["alt"] / c / eV
cands["rho_Lambda^(1/4)"] = rhoL_eV4 ** 0.25
land = {}
for k, m in cands.items():
    inw = M_MIN <= m <= m_max
    land[k] = inw
    miss = 0.0 if inw else (math.log10(M_MIN / m) if m < M_MIN else math.log10(m / m_max))
    P(f"      {k:24s} m = {m:.4e} eV   {'IN window' if inw else f'misses by {miss:.1f} decades'}")
num("A3_candidates_eV", cands); num("A3_in_window", land); num("A3_window", dict(m_min=M_MIN, m_max=m_max))
q_in = [k for k in land if k.startswith("q=") and land[k]]
check("A3 [finding] the mass is DERIVED: exactly one framework-native candidate lands in the window with no free exponent choice",
      f"q-family members in the window: {q_in}; the framework's distinctive scale (q = 1 / hbar a0/c^3) misses by "
      f"{math.log10(M_MIN / cands['q=1']):.1f} / {math.log10(M_MIN / cands['hbar a0/c^3 canonical']):.1f} decades; "
      f"rho_Lambda^(1/4) in window: {land['rho_Lambda^(1/4)']}", len(q_in) == 1, load_bearing=LB0)
num("mode", MODE)
P(f"\n  run time {time.time() - T0:.0f} s.  kappa = 1/2 FITTED; the cold mass is still required; nothing here says the theory is closed.")
nf = R.write(here=HERE)
sys.exit(1 if nf else 0)
