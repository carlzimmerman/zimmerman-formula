#!/usr/bin/env python3
"""X14_caustic_completion: are caustics generic for v3s's khronon dust, and does a caustic-free completion exist that adds
no new scale?  Frozen criteria: FROZEN_CRITERIA.md (committed alone with ASSUMPTION_LEDGER.md and LITERATURE_MAP.md).

Part R  reproductions of X3 (B1-S dispersion, B2-S nonlinear identities)           -> checks R0, R1
Part F  step 3: analytic folds from v3s's own PN equations (planar, spherical)      -> checks F1a..F5d
Part P  step 2: the frozen completion classes C1..C9 against v3s's passes          -> checks C*_P1..P6, FT, SC
Verdicts (i), (ii) by FROZEN_CRITERIA section 5.

Run:  OMP_NUM_THREADS=1 nice -n 15 python3 x14_caustic_completion.py            (exit 0 iff all required checks pass)
      X14_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 x14_caustic_completion.py (m1..m4; exit 1 by design)

kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. No dark-matter particle.
Not theory closed. No data comparison.
"""
import json
import math
import os
import resource
import sys
import time

import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations

MUTATE = os.environ.get("X14_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "_MUTATE" if MUTATE else ""
OUT = os.path.join(HERE, f"x14_caustic_completion{TAG}.out")
JS = os.path.join(HERE, f"x14_caustic_completion_results{TAG}.json")
T0 = time.time()
_lines = []
CHECKS = []
RES = {"mutate": MUTATE, "checks": CHECKS}


def log(s=""):
    print(s, flush=True)
    _lines.append(s)


def check(cid, ok, value, line, required=True):
    ok = bool(ok)
    CHECKS.append({"id": cid, "pass": ok, "value": str(value), "line": line, "required": required})
    log(f"  [{'PASS' if ok else 'FAIL'}] {cid}: {value}   (line: {line})")
    return ok


def rss_gb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e9 if sys.platform == "darwin" else r * 1024 / 1e9


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return float(o)
    if isinstance(o, (np.integer, int)) and not isinstance(o, bool):
        return int(o)
    if isinstance(o, (bool, np.bool_)):
        return bool(o)
    if isinstance(o, sp.Basic):
        return str(o)
    return o


# ------------------------------------------------------------------------------------------------ constants (RAW)
G = 6.67430e-11
C_SI = 299792458.0
GM_SUN = 1.32712440018e20
KPC = 3.0856775814913673e19
MPC = 1e3 * KPC
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}            # FITTED (kappa = 1/2)
LSTAR_PC = {"canonical": 21.682, "alt": 22.849}                 # FITTED (X3 D4 switched floor)
PC = KPC / 1e3
H0_SI = 67.2e3 / MPC                                            # native H0 lower end (conservative)
M_MW = 6e10                                                     # ILLUSTRATIVE (X8/X10)
W_KMS = [68.75, 74.8]                                           # X10 O2 / O1 t_i 3 MW speeds
R_FOLD_KPC = [11.0, 33.0, 73.0, 91.0, 156.0]                    # X8 h5 events; X10 events / wake
MUK_S4 = 0.1 / MPC                                              # S4 isolated-galaxy guard edge [1/m]
MUK_GAL = 0.03 / MPC                                            # S4 galaxies-survive edge
MUK_CAP = 10.0 / MPC                                            # BS24 Eq. 39 cap

# ================================================================================================ PART R
log("X14_caustic_completion" + ("  [MUTATE m1-m4]" if MUTATE else ""))
log("=" * 110)
log("PART R: reproductions of X3 (B1-S linear dispersion, B2-S nonlinear PN identities)")

k, om = sp.symbols("k omega", positive=True)
r0 = sp.Symbol("rho0", real=True)          # background khronon charge rho_tau, either sign
th = sp.Symbol("theta", real=True)
ML, MT = sp.symbols("M_L M_T", positive=True)
K, gL, muK = sp.symbols("K gamma_L mu_K", positive=True)
Bc = sp.Symbol("B", positive=True)          # C1 coefficient B = beta c^2/(2+3beta) > 0 (ghost-free side)
lst = sp.Symbol("ell_star", positive=True)  # C2 scale
s2 = sp.Symbol("s", real=True)              # C2 sign
nu = sp.Symbol("nu", positive=True)         # C5 nu = hbar/m
W2 = sp.Symbol("W2")
Mth_expr = 1 / (sp.cos(th) ** 2 / ML + sp.sin(th) ** 2 / MT)
Mth = sp.Symbol("M_theta", positive=True)


def disp(theta_val, cont_extra=0, pois_factor=1, bern_extra=0, muK2=None, roots=False):
    """X3's disp_switched (x3_switched_stiffness.py, B1-S; copied with provenance), extended by one class term.
    Equations: Poisson, rho_tau = div P - mu^2 Xi/K, continuity, Bernoulli, P equation with Theta gamma_L.
    cont_extra: extra coefficient multiplying k^2 dsigma in continuity (C1: B k^2 / K).
    pois_factor: Poisson -k^2 (pois_factor) dphi = K drho (C2: 1 + s ell^2 k^2).
    bern_extra: extra term in Bernoulli proportional to drho (C5: nu^2 k^2 / (4 rho0)).
    muK2: replacement for mu_K^2 (C4)."""
    dphi, dsig, dXi, drho = sp.symbols("dphi dsigma dXi drho")
    dP = sp.symbols("dP0:3")
    kh = sp.Matrix([0, 0, 1])
    Ph = sp.Matrix([sp.sin(th), 0, sp.cos(th)])
    Hm = K * (MT * sp.eye(3) + (ML - MT) * Ph * Ph.T)
    dPv = sp.Matrix(dP)
    mu2 = muK ** 2 if muK2 is None else muK2
    Peq = sp.I * k * kh * dXi - theta_val * gL * k ** 2 * kh * (kh.dot(dPv)) - Hm * dPv
    eqs_ = [-k ** 2 * pois_factor * dphi - K * drho, drho - (sp.I * k * kh.dot(dPv) - mu2 * dXi / K),
            -sp.I * om * drho + (r0 + cont_extra) * k ** 2 * dsig, dXi - (dphi + sp.I * om * dsig + bern_extra * drho)] \
        + list(Peq)
    Msys = sp.linear_eq_to_matrix(eqs_, [dphi, dsig, dXi, drho] + list(dP))[0]
    det = sp.factor(sp.simplify(Msys.det()))
    poly_deg = sp.degree(sp.expand(sp.numer(sp.together(det))), om)
    sol_ = sp.solve(sp.Eq(det.subs(om, sp.sqrt(W2)), 0), W2)
    w2 = sp.simplify(sol_[0]) if len(sol_) == 1 else None
    if roots:
        return w2, poly_deg, len(sol_)
    return w2


def to_Mth(expr):
    """rewrite in terms of M_theta (the H4 combination)."""
    e = sp.simplify(expr.subs(ML, 1 / ((1 / Mth - sp.sin(th) ** 2 / MT) / sp.cos(th) ** 2)))
    return sp.simplify(e)


def chi(theta_val, mu2=None):
    m2 = muK ** 2 if mu2 is None else mu2
    return k ** 2 / (K * Mth + theta_val * gL * k ** 2) + m2 / K


w2_exp = {tv: sp.simplify(r0 * (k ** 2 / chi(tv) - K)) for tv in (1, 0)}
w2_v3 = {}
t_r0 = time.time()
for tv in (1, 0):
    w, deg, nroot = disp(tv, roots=True)
    w2_v3[tv] = w
    resid = sp.simplify(to_Mth(w) - w2_exp[tv])
    RES.setdefault("R0", {})[f"Theta{tv}"] = {"omega2": str(to_Mth(w)), "expected": str(w2_exp[tv]),
                                              "residual": str(resid), "det_degree_in_omega": deg, "n_W2_roots": nroot}
log(f"  X3 B1-S system rebuilt ({time.time() - t_r0:.1f} s)")
r0ok = all(RES["R0"][f"Theta{tv}"]["residual"] == "0" for tv in (1, 0))
check("R0", r0ok, f"omega^2 - rho0[k^2/chi - K] = {RES['R0']['Theta1']['residual']} (Theta 1), "
      f"{RES['R0']['Theta0']['residual']} (Theta 0); det degree in omega {RES['R0']['Theta1']['det_degree_in_omega']}",
      "X3's B1-S reproduced on both sides (residual 0)")

# R1: X3 B2-S identities from L1 (copied with provenance)
t, z = sp.symbols("t z", real=True)
mu1 = sp.Symbol("mu", nonnegative=True)
phi = sp.Function("phi")(t, z)
sig = sp.Function("sigma")(t, z)
Pz = sp.Function("P")(t, z)
rhom = sp.Function("rho_m")(z)
Ff = sp.Function("F")
Wf = sp.Function("W")
Xi = phi - sp.diff(sig, t) + sp.diff(sig, z) ** 2 / 2
s_ = sp.diff(Pz, z)
L1 = (-sp.diff(phi, z) ** 2 / (2 * K) - rhom * phi + Pz * sp.diff(Xi, z) - Wf(K * Pz) - gL / 2 * Ff(s_)
      + mu1 ** 2 * Xi ** 2 / (2 * K))
eqsL = euler_equations(L1, [phi, sig, Pz], [t, z])
rt = s_ - mu1 ** 2 * Xi / K
vv = -sp.diff(sig, z)
r_cont = sp.simplify(sp.expand(eqsL[1].lhs + (sp.diff(rt, t) + sp.diff(rt * vv, z))))
xs = sp.Symbol("xs")
hP = sp.diff(Xi, z) - K * sp.Subs(sp.diff(Wf(xs), xs), xs, K * Pz).doit() + sp.diff(
    gL / 2 * sp.Subs(sp.diff(Ff(xs), xs), xs, s_).doit(), z)
r_P = min((sp.simplify(sp.expand((eqsL[2].lhs - sg_ * hP).doit())) for sg_ in (1, -1)), key=lambda e: len(str(e)))
r_eu = sp.simplify(sp.expand(sp.diff(vv, t) + vv * sp.diff(vv, z) - (sp.diff(Xi, z) - sp.diff(phi, z))))
r_phi = min((sp.simplify(sp.expand(eqsL[0].lhs - sg_ * (sp.diff(phi, z, 2) / K - rhom - rt))) for sg_ in (1, -1)),
            key=lambda e: len(str(e)))
RES["R1"] = {"continuity": str(r_cont), "P_equation": str(r_P), "Euler": str(r_eu), "Poisson": str(r_phi)}
check("R1", r_cont == 0 and r_P == 0 and r_eu == 0 and r_phi == 0,
      f"sigma-EL + continuity {r_cont}; P-EL - [Xi_z - K W'(KP) + d_z((gL/2)F'(s))] {r_P}; D_t v - (Xi_z - phi_z) "
      f"{r_eu}; phi-EL - [phi_zz/K - rho_m - rho_tau] {r_phi}",
      "X3's B2-S identities reproduced from L1, plus Poisson for all charge (residual 0)")

# ================================================================================================ PART F
log("")
log("PART F (step 3): analytic folds from v3s's own PN equations")
a0 = sp.Symbol("a_0", positive=True)
y = sp.Symbol("y", real=True)
yp = sp.Symbol("y_p", positive=True)
mu_f = lambda X: X / (1 + X)
U = (yp if MUTATE else a0 * yp / (a0 - yp))      # m1: inverse hold flux replaced by the identity (MOND removed)
U_true = a0 * yp / (a0 - yp)
# F1a: u(1 - mu(u/a0)) = y for the true U (positive branch; the negative branch by oddness)
r_F1a_pos = sp.simplify(U_true * (1 - mu_f(U_true / a0)) - yp)
yn = sp.Symbol("y_n", positive=True)            # y = -y_n
Un = -a0 * yn / (a0 - yn)
r_F1a_neg = sp.simplify(Un * (1 - mu_f(-Un / a0)) - (-yn))
RES["F1"] = {"U": "a0 y/(a0 - |y|), |y| < a0", "F1a_residual_pos": str(r_F1a_pos), "F1a_residual_neg": str(r_F1a_neg)}
check("F1a", r_F1a_pos == 0 and r_F1a_neg == 0, f"u(1-mu(|u|/a0)) - y = {r_F1a_pos} (y>0), {r_F1a_neg} (y<0)",
      "U(y) = a0 y/(a0-|y|) inverts the hold flux exactly; flux cap |y| < a0")
# F1b: U'(y) = (1 + |U|/a0)^2 = M_L
r_F1b = sp.simplify(sp.diff(U, yp) - (1 + U / a0) ** 2)
r_F1b_neg = sp.simplify(-sp.diff(-a0 * yn / (a0 - yn), yn) - (1 + a0 * yn / (a0 - yn) / a0) ** 2)   # dU/dy = -dU/dy_n
RES["F1"]["F1b_residual"] = str(r_F1b)
RES["F1"]["F1b_residual_neg"] = str(r_F1b_neg)
check("F1b", r_F1b == 0 and r_F1b_neg == 0, f"U'(y) - (1+|U|/a0)^2 = {r_F1b} (y>0), {r_F1b_neg} (y<0)",
      "U' = (1+x)^2 = M_L (the longitudinal P mass)")

# F1c: Gauss-integrated planar fields satisfy the EL equations of L1 (mu_K = 0, Theta = 0, W'(y) = U(y)/K)
Mtot = sp.Function("Mtot")(t, z)    # baryon + khronon column to the left
Sx = sp.Function("S")(t, z)         # khronon column to the left
rho_b = sp.Function("rho_b")(t, z)
rho_t = sp.Function("rho_tau")(t, z)
vel = sp.Function("v")(t, z)
C1c, C2c = sp.symbols("C_1 C_2")
phi_z = K * Mtot + C1c
P_f = Sx + C2c
Ux = sp.Function("Ucal")
Xi_z = Ux(K * P_f)
subs_cols = {sp.Derivative(Mtot, z): rho_b + rho_t, sp.Derivative(Sx, z): rho_t}
r_pois = sp.simplify((sp.diff(phi_z, z) / K - (rho_b + rho_t)).subs(subs_cols))
r_hold = sp.simplify((sp.diff(P_f, z) - rho_t).subs(subs_cols))
# the khronon column is label-invariant: S_t = -rho_tau v (flux) => D_t S = 0
r_DS = sp.simplify((sp.diff(Sx, t) + vel * sp.diff(Sx, z)).subs({sp.Derivative(Sx, t): -rho_t * vel,
                                                                    sp.Derivative(Sx, z): rho_t}))
# label force F(q, x) = Xi_z - phi_z = U(K S(q)) - K (Sigma_b(<x) + S(q)) (constants absorbed); J equation
qq, tt = sp.symbols("q t_l", real=True)
xq = sp.Function("x")(qq, tt)
Sq = sp.Function("S_l")(qq)
Sigb = sp.Function("Sigma_b")
Uc = sp.Function("Ucal")
Fq = Uc(K * Sq) - K * (Sigb(xq) + Sq)
Jdd = sp.diff(Fq, qq)
rho0q = sp.Function("rho_tau0")(qq)
rhob_f = sp.Function("rho_bx")
Jsym = sp.Symbol("J")
MLq = sp.Symbol("M_Lq")
Jdd_s = Jdd.subs({sp.Derivative(Sq, qq): rho0q, sp.Derivative(xq, qq): Jsym})


def _rep_sub(e):
    inner = e.expr if isinstance(e, sp.Subs) else e
    if inner.has(Uc):
        return MLq
    if inner.has(Sigb):
        return rhob_f(xq)
    return e


Jdd_s = Jdd_s.replace(lambda e: isinstance(e, (sp.Subs, sp.Derivative)) and (e.has(Uc) or e.has(Sigb)), _rep_sub)
expectedJ = -K * rhob_f(xq) * Jsym + K * rho0q * (MLq - 1)
r_F1d = sp.simplify(sp.expand(Jdd_s - expectedJ))
RES["F1"].update({"F1c_poisson": str(r_pois), "F1c_hold": str(r_hold), "F1c_label_invariance": str(r_DS),
                  "F1c_label_force": "x_tt = U(K S(q)) - K[Sigma_b(<x) - Sigma_b,tot/2] - K S(q)  (Theta = 0, mu_K = 0)",
                  "F1d_Jdd": str(Jdd_s), "F1d_residual": str(r_F1d),
                  "F1d_equation": "J_tt = -K rho_b(x) J + K rho_tau0(q) (M_L(q) - 1)"})
check("F1c", r_pois == 0 and r_hold == 0 and r_DS == 0,
      f"Poisson {r_pois}, hold (P_z = rho_tau) {r_hold}, D_t S = {r_DS}; with Xi_z = U(KP) from the P-EL (F1a) and "
      f"D_t v = Xi_z - phi_z (R1)", "Gauss-integrated 1D fields satisfy L1's EL equations; khronon column label-invariant")
check("F1d", r_F1d == 0, f"J_tt - [-K rho_b J + K rho_tau0 (M_L - 1)] = {r_F1d}",
      "exact Jacobian equation before first crossing (Theta = 0, mu_K = 0)")

# F2: a cold stream crossing a thin sheet (the planar point mass), exact closed form
x0, V, gs, tc, tau = sp.symbols("x_0 V g t_c tau", positive=True)
fq = sp.Function("f")(x0)        # per-label self force F_self(q) (constant in time, F1)
g_sheet = -gs if MUTATE else gs  # m3: repulsive sheet
a1 = -g_sheet + fq               # acceleration before crossing (toward the sheet at x = 0)
a2 = g_sheet + fq                # after crossing (field reversed)
tc_f = sp.Function("t_c")(x0)
pre = x0 - V * tc_f + a1 * tc_f ** 2 / 2           # = 0 defines t_c(x0)
dtc = sp.solve(sp.Eq(sp.diff(pre, x0), 0), sp.Derivative(tc_f, x0))[0]
w_c = V - a1 * tc_f                                  # speed at crossing (moving toward -x)
post = -w_c * tau + a2 * tau ** 2 / 2                # position after crossing, tau = t - t_c(x0)
# J at fixed t: d/dx0 with tau = t - t_c(x0)
Jpost = sp.diff(post, x0) + sp.diff(post, tau) * (-sp.Derivative(tc_f, x0))
Jpost = sp.simplify(Jpost.subs(sp.Derivative(tc_f, x0), dtc))
Jc = 1 + sp.diff(fq, x0) * tc_f ** 2 / 2
wp2 = sp.Symbol("omega_p2", real=True)
Jpost_expected = Jc + (sp.diff(fq, x0) * tc_f - 2 * g_sheet * Jc / w_c) * tau + sp.diff(fq, x0) * tau ** 2 / 2
r_F2_general = sp.simplify(sp.expand(Jpost - Jpost_expected))
# zero charge (mimetic limit): f' = 0
J0 = sp.simplify(Jpost.subs(sp.Derivative(fq, x0), 0).subs(fq, 0))
J0 = sp.simplify(J0.subs(sp.Derivative(fq, x0), 0))
wv = sp.Symbol("w", positive=True)
J0w = sp.simplify(J0.subs(V, wv - g_sheet * tc_f))      # V - a1 t_c = w (crossing speed)
KS = sp.Symbol("K_Sigma", positive=True)          # K Sigma_b = 2 g
J0w = sp.simplify(J0w.subs(gs, KS / 2))
tau_roots = [r_ for r_ in sp.solve(sp.Eq(J0w, 0), tau) if r_.is_positive]
tau_f = tau_roots[0] if tau_roots else None
tau_turn = sp.simplify(wv / (KS / 2))
f2_ok = (tau_f is not None) and sp.simplify(tau_f - wv / KS) == 0 and sp.simplify(tau_f / tau_turn - sp.Rational(1, 2)) == 0
# charged: fold condition at t_c -> 0 (J_c = 1, Jdot_c = 0): J = 1 - (K Sigma/w) tau + omega_p^2 tau^2/2
Jch = 1 - (KS / wv) * tau + wp2 * tau ** 2 / 2
disc = sp.simplify(sp.discriminant(sp.Poly(Jch, tau)))
fold_cond = sp.simplify(sp.solve(sp.Ge(disc, 0), wp2))
RES["F2"] = {"J_post_general_residual": str(r_F2_general), "J_post_general": str(Jpost_expected),
             "J_zero_charge": str(J0w), "tau_fold": str(tau_f), "tau_turnaround": str(tau_turn),
             "charged_J": str(Jch), "discriminant": str(disc), "fold_condition_omega_p2": str(fold_cond),
             "fold_condition_dimensionless": "omega_p tau_f <= 1/sqrt(2) with tau_f = w/(K Sigma_b) (rho_tau0 > 0); "
                                             "every datum folds if omega_p^2 <= 0 (rho_tau0 <= 0)"}
check("F2", f2_ok and r_F2_general == 0,
      f"J(tau) = {J0w}; fold tau_f = {tau_f}, turnaround {tau_turn}; general J residual {r_F2_general}; "
      f"charged fold iff {fold_cond}",
      "zero-charge stream folds at tau_f = w/(K Sigma_b) < turnaround for every w, Sigma_b; exact closed form")
# soft labels: J_tt <= -|omega_p^2| < 0 => fold for any (J0, Jdot0)
J0s, Jd0 = sp.symbols("J_0 Jdot_0", real=True)
A_s = sp.Symbol("A", positive=True)
Jsoft = J0s + Jd0 * tau - A_s * tau ** 2 / 2
J0p = sp.Symbol("J_0p", positive=True)
r_plus = (Jd0 + sp.sqrt(Jd0 ** 2 + 2 * A_s * J0p)) / A_s
res_soft = sp.simplify(Jsoft.subs(J0s, J0p).subs(tau, r_plus))
grid_soft = [float(r_plus.subs({J0p: j_, Jd0: d_, A_s: a_})) for j_ in (0.01, 1.0) for d_ in (-5.0, 0.0, 5.0)
             for a_ in (1e-3, 1.0)]
soft_ok = res_soft == 0 and all(v_ > 0 for v_ in grid_soft)
RES["F2"]["soft_fold_time"] = "tau_* = [Jdot0 + sqrt(Jdot0^2 + 2 A J0)]/A, A = K|rho_tau0|(M_L - 1) + (sheet term >= 0)"
check("F2-soft", soft_ok, f"J = J0 + Jdot0 tau - A tau^2/2 has the positive root [Jdot0 + sqrt(Jdot0^2 + 2AJ0)]/A for "
      f"every J0 > 0, Jdot0", "soft (rho_tau0 < 0) planar labels fold in finite time for every initial datum")

# F3: phase mixing of held oscillations (exact displacement equation, linear J)
xi = sp.Function("xi")(qq, tt)
Sb = sp.Function("Sigma_b")
# equilibrium: F(q, q) = 0  =>  F(q, q + xi) = -K[Sigma_b(q + xi) - Sigma_b(q)]
Fq_eq = Uc(K * Sq) - K * (Sb(qq) + Sq)            # = 0 at equilibrium
Fq_disp = Uc(K * Sq) - K * (Sb(qq + xi) + Sq)
r_F3 = sp.simplify((Fq_disp - Fq_eq) + K * (Sb(qq + xi) - Sb(qq)))
xi0 = sp.Function("xi_0")(qq)
omq = sp.Function("omega")(qq)
xi_lin = xi0 * sp.cos(omq * tt)
J_lin = 1 + sp.diff(xi_lin, qq)
tn = sp.Symbol("t_n", positive=True)
# at phases where cos(omega t) = 0 and sin(omega t) = sign(xi0 omega'): J = 1 - |xi0 omega'| t_n
J_at = sp.simplify(J_lin.subs(tt, tn).subs(sp.cos(omq * tn), 0).subs(sp.sin(omq * tn), 1))
RES["F3"] = {"displacement_residual": str(r_F3), "J_linear": str(J_lin), "J_at_quarter_phases": str(J_at),
             "fold_bound": "t_* <= 1/|xi0 omega'| + 2 pi/omega (linear theory, omega^2 = K rho_b(q)); Dawson-type"}
check("F3", r_F3 == 0 and sp.simplify(J_at - (1 - xi0 * sp.diff(omq, qq) * tn)) == 0,
      f"xi_tt = -K[Sigma_b(q+xi) - Sigma_b(q)] residual {r_F3}; J at quarter phases = {J_at}",
      "held planar oscillations phase-mix to J <= 0 by t ~ 1/|xi0 omega'| whenever omega'(q) != 0")

# F4: spherical shells
r_s, Gs, Mb, m_s = sp.symbols("r G M_b m", positive=True)
# hold law r^2 (1-mu) Xi' = G m  =>  Xi' = U(G m / r^2);  phi' = G (M_b + m)/r^2
Xi_p = U_true.subs(yp, Gs * m_s / r_s ** 2)
r_F4_hold = sp.simplify(r_s ** 2 * (1 - mu_f(Xi_p / a0)) * Xi_p - Gs * m_s)
F_shell = Xi_p - Gs * (Mb + m_s) / r_s ** 2
# (a) m = 0: cycloid r = q cos^2 eta, t = sqrt(q^3/(2GM))(eta + sin eta cos eta)
eta, qsh = sp.symbols("eta q", positive=True)
r_cyc = qsh * sp.cos(eta) ** 2
t_cyc = sp.sqrt(qsh ** 3 / (2 * Gs * Mb)) * (eta + sp.sin(eta) * sp.cos(eta))
rdd = sp.diff(sp.diff(r_cyc, eta) / sp.diff(t_cyc, eta), eta) / sp.diff(t_cyc, eta)
r_F4a = sp.simplify(rdd + Gs * Mb / r_cyc ** 2)
t_ff = sp.simplify(t_cyc.subs(eta, sp.pi / 2))
t_ff_exp = sp.pi / 2 * sp.sqrt(qsh ** 3 / (2 * Gs * Mb))
# (b) m < 0: U(y) - y = y|y|/(a0-|y|) < 0  =>  r_tt <= -G M_b / r^2
yneg = sp.Symbol("y_n", positive=True)
gap_neg = sp.simplify((-a0 * yneg / (a0 - yneg)) - (-yneg))
# (c) m > 0: wall at y -> a0 (log-divergent barrier); held radial frequency omega^2 = 2 a0 x^2 / r
eps_w = sp.Symbol("epsilon", positive=True)
r_w = sp.sqrt(Gs * m_s / a0)
U_near = sp.simplify(U_true.subs(yp, Gs * m_s / (r_w * (1 + eps_w)) ** 2))
U_lead = sp.limit(U_near * eps_w, eps_w, 0)
xh = sp.Symbol("x", positive=True)
# equilibrium: G(M_b+m)/r^2 = U(y), y = a0 x/(1+x)
yeq = a0 * xh / (1 + xh)
dFdr = sp.diff(F_shell, r_s)
mass_sub = sp.solve(sp.Eq(Gs * m_s / r_s ** 2, yeq), m_s)[0]
Mb_sub = sp.solve(sp.Eq(Gs * (Mb + m_s) / r_s ** 2, U_true.subs(yp, yeq)), Mb)[0]
om2_shell = sp.simplify((-dFdr).subs(Mb, Mb_sub).subs(m_s, mass_sub))
r_F4c = sp.simplify(om2_shell - 2 * a0 * xh ** 2 / r_s)
RES["F4"] = {"hold_residual": str(r_F4_hold), "shell_force": str(F_shell), "F4a_residual": str(r_F4a),
             "t_ff": str(t_ff), "U_minus_y_negative_branch": str(gap_neg),
             "wall_radius": "r_w = sqrt(G m / a0)", "U_times_eps_at_wall": str(U_lead),
             "held_radial_omega2": str(om2_shell), "held_radial_omega2_residual": str(r_F4c)}
check("F4a", r_F4_hold == 0 and r_F4a == 0 and sp.simplify(t_ff - t_ff_exp) == 0,
      f"spherical hold law residual {r_F4_hold}; cycloid r_tt + GM/r^2 = {r_F4a}; t_ff = {t_ff}",
      "zero-charge shells reach r = 0 (hoop J -> 0) at t_ff = (pi/2) sqrt(q^3/(2 G M_b))")
check("F4b", bool(sp.simplify(gap_neg + yneg ** 2 / (a0 - yneg)) == 0),
      f"U(y) - y = {gap_neg} < 0 for y < 0, so r_tt <= -G M_b/r^2", "negative-charge shells fall at least as fast as "
      "Kepler with M_b: r = 0 (or the flux cap, where U -> -inf) within t_ff")
# dω/dq != 0 for the point-mass AQUAL phantom: x^2/(1+x) = G M/(a0 r^2)
rr = sp.Symbol("r", positive=True)
GMs = sp.Symbol("GM", positive=True)
x_of_r = sp.solve(sp.Eq(xh ** 2 / (1 + xh), GMs / (a0 * rr ** 2)), xh)
x_of_r = [e for e in x_of_r if sp.simplify(e.subs({GMs: 1, a0: 1, rr: 1})).is_positive][0]
dln = sp.simplify(sp.diff(sp.log(2 * a0 * x_of_r ** 2 / rr), rr) * rr)
dln_vals = [float(dln.subs({GMs: 1, a0: 1, rr: v_})) for v_ in (0.1, 1.0, 10.0)]
RES["F4"]["dln_omega2_dln_r"] = str(dln)
RES["F4"]["dln_omega2_dln_r_values_at_r_over_rM_0.1_1_10"] = dln_vals
check("F4c", r_F4c == 0 and U_lead != 0 and all(v_ < 0 for v_ in dln_vals),
      f"U near the wall ~ {U_lead}/eps (log-divergent barrier); omega^2 - 2 a0 x^2/r = {r_F4c}; "
      f"dln omega^2/dln r = {[round(v_, 3) for v_ in dln_vals]}",
      "positive charge: wall excludes hoop collapse; held shells phase-mix (domega/dq != 0) -> shell crossing")

# F5: pressure
tau_s = sp.Symbol("tau_s", positive=True)      # specific volume 1/rho
cpar, Acp = sp.symbols("c A", positive=True)
p_forms = {"stiffness (gL/2) rho^2": gL / 2 / tau_s ** 2, "K(Q) K rho^2/(2 mu^2)": K / (2 * muK ** 2) / tau_s ** 2,
           "isothermal c^2 rho": cpar ** 2 / tau_s, "Chaplygin -A/rho": -Acp * tau_s}
gnl = {}
for nm, p_ in p_forms.items():
    pp = sp.simplify(sp.diff(p_, tau_s, 2))
    gnl[nm] = {"p_tau_tau": str(pp), "genuinely_nonlinear": bool(pp != 0)}
chap_work = sp.integrate(-Acp * tau_s, (tau_s, 0, 1))
RES["F5"] = {"GNL": gnl, "Chaplygin_work_to_J0_finite": str(chap_work)}
f5a_ok = gnl["stiffness (gL/2) rho^2"]["genuinely_nonlinear"] and gnl["K(Q) K rho^2/(2 mu^2)"]["genuinely_nonlinear"] \
    and not gnl["Chaplygin -A/rho"]["genuinely_nonlinear"] and chap_work.is_finite
check("F5a", f5a_ok, f"p''(tau_s): " + "; ".join(f"{k_}: {v_['p_tau_tau']}" for k_, v_ in gnl.items())
      + f"; Chaplygin work to J = 0: {chap_work} (finite)",
      "stiffness and K(Q) pressures genuinely nonlinear (shock after compression); Chaplygin linearly degenerate but "
      "finite at J -> 0 (does not stop the fold)")
# (b) cold-fold depth for gamma = 2: work (c0^2/2)(1/J - 1) = w^2/2
Jst, c0s, wws = sp.symbols("J_* c_0 w", positive=True)
rho0p = sp.Symbol("rho_0", positive=True)
work = sp.integrate(gL / 2 * (rho0p / (tau_s * rho0p)) ** 2 * 0 + gL / 2 / tau_s ** 2, (tau_s, Jst / rho0p, 1 / rho0p))
work = sp.simplify(work.subs(gL, c0s ** 2 / rho0p))
Jstar = sp.solve(sp.Eq(work, wws ** 2 / 2), Jst)
Jstar = [e for e in Jstar if e.is_positive or e.subs({c0s: 1, wws: 2}).is_positive][0]
r_F5b = sp.simplify(Jstar - 1 / (1 + (wws / c0s) ** 2))
RES["F5"].update({"work_per_mass": str(work), "J_star": str(Jstar), "J_star_residual": str(r_F5b)})
check("F5b", r_F5b == 0, f"work = {work}; J_* = {Jstar}", "a gamma = 2 pressure stops the cold fold only at "
      "J_* = 1/(1 + Mach^2)")


# numbers: AQUAL point mass, phantom, Mach, K(Q) inertness
def aqual_point(r_m, a0v, GM):
    gN = GM / r_m ** 2
    g = 0.5 * (gN + math.sqrt(gN * gN + 4 * a0v * gN))
    Krho = 2 * a0v * GM / (r_m * math.sqrt(GM * GM + 4 * a0v * GM * r_m * r_m))   # 4 pi G rho_phantom
    return g, g / a0v, Krho


GM_MW = M_MW * GM_SUN
NUM = {}
mach_min = {}
qk = {}
for foot, a0v in FOOT.items():
    Ls = LSTAR_PC[foot] * PC
    NUM[foot] = []
    for r_k in R_FOLD_KPC:
        g, xv, Krho = aqual_point(r_k * KPC, a0v, GM_MW)
        c0 = Ls * math.sqrt(Krho / 2.0)                    # c0^2 = gamma_L rho = (K L*^2/2) rho
        row = {"r_kpc": r_k, "g_m_s2": g, "x": xv, "K_rho_ph_s-2": Krho, "rho_ph_kg_m3": Krho / (4 * math.pi * G),
               "c0_stiffness_m_s": c0, "M_theta_minus_1_bracket": [xv, xv * xv + 2 * xv]}
        row["Mach"] = {f"{w_}": w_ * 1e3 / c0 for w_ in W_KMS}
        row["J_star"] = {f"{w_}": 1.0 / (1.0 + (w_ * 1e3 / c0) ** 2) for w_ in W_KMS}
        Mup = (1 + xv) ** 2
        row["q_K"] = {"S4_0.1": math.sqrt(Mup) * MUK_S4 * r_k * KPC, "gal_0.03": math.sqrt(Mup) * MUK_GAL * r_k * KPC,
                      "BS_cap_10": math.sqrt(Mup) * MUK_CAP * r_k * KPC}
        # K(Q) pressure would need c_s^2 = K rho_d / mu^2 >= w^2: the dust density this requires at the S4 edge
        row["rho_d_needed_for_cs_ge_w_at_S4_kg_m3"] = (max(W_KMS) * 1e3) ** 2 * MUK_S4 ** 2 / (4 * math.pi * G)
        NUM[foot].append(row)
    mach_min[foot] = min(min(r_["Mach"].values()) for r_ in NUM[foot])
    qk[foot] = {"S4_decisive_11_156": max(r_["q_K"]["S4_0.1"] for r_ in NUM[foot] if r_["r_kpc"] in (11.0, 156.0)),
                "S4_all": max(r_["q_K"]["S4_0.1"] for r_ in NUM[foot]),
                "cap_all": max(r_["q_K"]["BS_cap_10"] for r_ in NUM[foot])}
RES["F5"]["numbers"] = NUM
RES["F5"]["Mach_min"] = mach_min
RES["F5"]["q_K_max"] = qk
for foot in FOOT:
    log(f"  {foot}: " + "; ".join(f"r {r_['r_kpc']:.0f} kpc x {r_['x']:.3f} c0 {r_['c0_stiffness_m_s']:.1f} m/s "
                                  f"Mach {min(r_['Mach'].values()):.0f} q_K(S4) {r_['q_K']['S4_0.1']:.4f} "
                                  f"q_K(cap) {r_['q_K']['BS_cap_10']:.2f}" for r_ in NUM[foot]))
check("F5c", all(mach_min[f_] >= 10 for f_ in FOOT),
      f"min Mach over fold locations and w: canonical {mach_min['canonical']:.0f}, alt {mach_min['alt']:.0f}",
      "stiffness Mach >= 10 at every fold location, both footings")
# (d) K(Q) inert at k^2 >> M mu^2
w2_mu = to_Mth(w2_v3[0])
lim_mu = sp.simplify(sp.limit(w2_mu, k, sp.oo))
w2_mu0 = sp.simplify(w2_mu.subs(muK, 0))
r_F5d = sp.simplify(lim_mu - K * r0 * (Mth - 1))
crossover = sp.simplify(sp.together(w2_mu - w2_mu0))
RES["F5"]["Kq_large_k_limit"] = str(lim_mu)
RES["F5"]["Kq_correction"] = str(crossover)
RES["F5"]["Kq_condition"] = ("K(Q) acts as a pressure (c_s^2 = K rho_d/mu_K^2) only for k^2 <~ M_theta mu_K^2; it can halt a "
                             "fold of scale l and speed w only if sqrt(M_theta) mu_K l >~ 1 AND K rho_d/mu_K^2 >~ w^2; "
                             "even then p ~ rho^2 is genuinely nonlinear (shock)")
check("F5d", r_F5d == 0 and all(qk[f_]["S4_decisive_11_156"] < 1 for f_ in FOOT),
      f"lim_k->inf omega^2 = {lim_mu} (mu_K-independent); K(Q) correction = {crossover}; q_K at mu_K = 0.1 Mpc^-1 "
      f"(l 11, 156 kpc): canonical {qk['canonical']['S4_decisive_11_156']:.4f}, alt {qk['alt']['S4_decisive_11_156']:.4f}"
      f"; at the BS cap up to {qk['canonical']['cap_all']:.2f} / {qk['alt']['cap_all']:.2f}",
      "K(Q) is inert at the fold scale for S4-allowed mu_K (q_K < 1), both footings")

# ================================================================================================ PART P
log("")
log("PART P (step 2): the frozen completion classes")
rp = sp.Symbol("r_p", positive=True)
dMp = sp.Symbol("dM", positive=True)   # M_theta - 1 > 0 (H4)
CL = {}


def large_k(w2, n):
    return sp.simplify(sp.limit(w2 / k ** n, k, sp.oo))


def exponent_table(w2):
    """leading large-k exponent and coefficient of omega^2 for rho0 = +r_p and -r_p."""
    out = {}
    for sgn, lab in ((1, "rho+"), (-1, "rho-")):
        e = sp.simplify(w2.subs(r0, sgn * rp).subs(Mth, 1 + dMp))
        lead = None
        for n in (6, 4, 2, 0):
            c_ = large_k(e, n)
            if c_ != 0 and c_.is_finite is not False and c_ not in (sp.oo, -sp.oo):
                lead = (n, sp.simplify(c_))
                break
        out[lab] = {"n": lead[0] if lead else None, "coef": str(lead[1]) if lead else None,
                    "coef_positive": bool(sp.simplify(lead[1]).is_positive) if lead else None,
                    "coef_expr": lead[1] if lead else None}
    return out


def ptab(tag, d):
    return {k_: {kk: vv for kk, vv in v_.items() if kk != "coef_expr"} for k_, v_ in d.items()}


# ---------------- C1: K^2 operator, PN -(B/(2K)) (lap sigma)^2  (m2: B -> -B; m4: B = 0)
B_use = (-Bc if MUTATE else Bc)
C1 = {}
# C1-R: the PN Lagrangian term gives the continuity flux and the record form rho -> rho + B k^2/K
sigm = sp.Function("sigma")(t, z)
L_c1 = -(Bc / (2 * K)) * sp.diff(sigm, z, 2) ** 2
el_c1 = euler_equations(L_c1, [sigm], [t, z])[0].lhs
r_c1R = sp.simplify(el_c1 + (Bc / K) * sp.diff(sigm, z, 4))     # EL contribution = -(B/K) sigma_zzzz
C1["PN_EL_contribution"] = str(el_c1)
C1["PN_check_residual"] = str(r_c1R)
w2c1 = {}
for tv in (1, 0):
    w2c1[tv] = to_Mth(disp(tv, cont_extra=(B_use * k ** 2 / K)))
w2c1_dropped = to_Mth(disp(0, cont_extra=0))
C1["omega2_Theta1"] = str(w2c1[1])
C1["omega2_Theta0"] = str(w2c1[0])
r_c1form = sp.simplify(w2c1[0] - (r0 + B_use * k ** 2 / K) * (k ** 2 / chi(0) - K))
C1["record_form_residual"] = str(r_c1form)
check("C1-R", r_c1R == 0 and r_c1form == 0, f"EL of -(B/2K) sigma_zz^2 = {el_c1}; omega^2 - (rho + Bk^2/K)(k^2/chi - K) "
      f"= {r_c1form}", "C1's PN term reproduces the record form (X3 E2 / C5): rho_tau -> rho_tau + B k^2/K")
et1 = {tv: exponent_table(w2c1[tv].subs(muK, 0)) for tv in (1, 0)}
C1["exponents"] = {f"Theta{tv}": ptab("", et1[tv]) for tv in (1, 0)}
# P1/P2: static branch sigma = -C t (+ const): the EL contribution vanishes; covariant K = div n = 0 for tau = t static
Cst = sp.Symbol("C_s")
p1_c1 = sp.simplify(el_c1.subs(sigm, -Cst * t).doit())
C1["P1"] = {"EL_on_static": str(p1_c1), "grade": "PASS" if p1_c1 == 0 else "FAIL"}
C1["P2"] = {"grade": C1["P1"]["grade"], "note": "static operator: C6/X3-D2 screened solution unchanged; moving-Sun / "
                                                "PPN alpha_1,2 not checked"}
# P4: one omega^2 root in the scalar determinant + 2 tensor; C5's table (beta > 0, eta = 0: 3)
_, deg1, nr1 = disp(0, cont_extra=(B_use * k ** 2 / K), roots=True)
C1["P4"] = {"det_degree_in_omega": deg1, "n_W2_roots": nr1, "total_DOF": nr1 + 2,
            "record": "C5 table: beta > 0, eta = 0 -> 3", "grade": "PASS" if nr1 + 2 == 3 else "FAIL"}
# P5: unitary gauge K for a TT perturbation is second order -> K^2 has no quadratic TT term
hp = sp.Function("h_p")(t, z)
hx = sp.Function("h_x")(t, z)
eps = sp.Symbol("epsilon")
hij = sp.Matrix([[1 + eps * hp, eps * hx, 0], [eps * hx, 1 - eps * hp, 0], [0, 0, 1]])
Ktr = sp.diff(sp.log(hij.det()), t) / 2                         # K = (1/2N) h^ij dh_ij/dt, N = 1, no shift
Kser = sp.series(Ktr, eps, 0, 3).removeO()
K1 = sp.simplify(Kser.coeff(eps, 1))
K2sq = sp.simplify(sp.series(Ktr ** 2, eps, 0, 3).removeO().coeff(eps, 2))
C1["P5"] = {"K_first_order_TT": str(K1), "K2_quadratic_TT": str(K2sq), "grade": "PASS" if (K1 == 0 and K2sq == 0) else "FAIL"}
# P6a: -omega^2 bounded above for both signs on both sides
p6a = {}
for tv in (1, 0):
    for sgn, lab in ((1, "rho+"), (-1, "rho-")):
        e = sp.simplify(-w2c1[tv].subs(muK, 0).subs(r0, sgn * rp).subs(Mth, 1 + dMp))
        lim_ = sp.limit(e, k, sp.oo)
        p6a[f"Theta{tv}|{lab}"] = str(lim_)
c1_p6a_ok = all(v_ not in (str(sp.oo),) for v_ in p6a.values())
C1["P6a_limits_of_minus_omega2"] = p6a
# P6c: IR band (C5): rate^2 = c^2 mu^2 beta/(2+3 beta) <= H0^2  ->  beta <= 2 H0^2/(c^2 mu^2 - 3 H0^2)
beta_max = {lab: 2 * H0_SI ** 2 / (C_SI ** 2 * mu_ ** 2 - 3 * H0_SI ** 2) for lab, mu_ in (("mu_0.1", MUK_S4), ("mu_0.03", MUK_GAL))}
C1["P6c_beta_max"] = beta_max
C1["P6b"] = "no ghost for beta > 0 on the 2+3beta > 0 branch (C5, record)"
C1["P6d"] = "function of sigma only: both signs of rho_tau and its zero crossing allowed"
c1_p6 = "PASS-WITH-BOUND" if c1_p6a_ok else "FAIL"
C1["P6"] = {"grade": c1_p6}
# FT: n on Theta 0 for both signs (m4: B = 0 must give n = 0)
ft_src = exponent_table(w2c1_dropped.subs(muK, 0)) if MUTATE else et1[0]
n_soft = [ft_src[l_]["n"] for l_ in ("rho+", "rho-")]
pos_soft = [ft_src[l_]["coef_positive"] for l_ in ("rho+", "rho-")]
C1["FT_soft_side"] = {"n": n_soft, "coef_positive": pos_soft, "source": "B = 0 (m4)" if MUTATE else "B > 0"}
# subsonic window: c_A^2 = (M_theta - 1) beta c^2/(2+3beta) >= w^2 at all fold locations (M-1 = x, conservative)
beta_min = {}
for foot in FOOT:
    bm = []
    for r_ in NUM[foot]:
        for w_ in W_KMS:
            ww = (w_ * 1e3) ** 2
            den = r_["x"] * C_SI ** 2 - 3 * ww
            bm.append(2 * ww / den if den > 0 else float("inf"))
    beta_min[foot] = max(bm)
    # upper bracket (M-1 = x^2 + 2x), reported
beta_min_upper = {foot: max(2 * (max(W_KMS) * 1e3) ** 2 / ((r_["x"] ** 2 + 2 * r_["x"]) * C_SI ** 2 - 3 * (max(W_KMS) * 1e3) ** 2)
                            for r_ in NUM[foot]) for foot in FOOT}
window = {foot: {lab: bool(beta_min[foot] <= bmx) for lab, bmx in beta_max.items()} for foot in FOOT}
C1["FT_window"] = {"beta_min_conservative(M-1=x)": beta_min, "beta_min_upper_bracket(M-1=x^2+2x)": beta_min_upper,
                   "beta_max": beta_max, "window_nonempty": window,
                   "c_A_at_beta_max_mu0.1_km_s": {foot: [math.sqrt(r_["x"] * beta_max["mu_0.1"] * C_SI ** 2 /
                                                                   (2 + 3 * beta_max["mu_0.1"])) / 1e3 for r_ in NUM[foot]]
                                                  for foot in FOOT}}
if all(n_ == 2 for n_ in n_soft) and all(pos_soft):
    ft1 = "COND"
elif all(n_ is not None and n_ >= 4 for n_ in n_soft) and all(pos_soft):
    ft1 = "PASS-LIT"
else:
    ft1 = "FAIL"
c1_removes = (ft1 == "COND" and all(any(window[f_].values()) for f_ in FOOT)) or ft1 == "PASS-LIT"
C1["FT"] = {"grade": ft1, "removes_fold": c1_removes}
C1["SC"] = {"new_constants": ["beta (dimensionless; sets the velocity scale c sqrt(beta (M-1)/2))"],
            "allowed": f"beta_min {beta_min} <= beta <= beta_max {beta_max} (mu_K-dependent upper edge)",
            "how_fixed": "nothing in v3s fixes beta (no derivation); bounded only; X3 E2: not adopted"}
check("C1-P6a", c1_p6a_ok, f"lim -omega^2 (k->inf): {p6a}", "C1: no Hadamard growth on either side, either sign")
check("C1-FT", ft1 in ("COND", "PASS-LIT"), f"soft side large-k exponents {n_soft}, coefficient positive {pos_soft} "
      f"({C1['FT_soft_side']['source']})", "C1 adds a positive k^2 (or higher) term on the soft side for both signs")
log(f"  C1 window: beta_min {beta_min}, beta_max {beta_max}, non-empty {window}")
CL["C1"] = C1

# ---------------- C2: higher-spatial-curvature potential, Poisson (1 + s l^2 k^2)
C2 = {}
w2c2 = {sv: to_Mth(disp(0, pois_factor=(1 + sv * lst ** 2 * k ** 2))) for sv in (1, -1)}
C2["omega2_Theta0"] = {str(sv): str(w2c2[sv]) for sv in (1, -1)}
et2 = {sv: exponent_table(w2c2[sv].subs(muK, 0)) for sv in (1, -1)}
C2["exponents_Theta0"] = {str(sv): ptab("", et2[sv]) for sv in (1, -1)}
# pole for s = -1 at k = 1/l
pole = sp.limit(w2c2[-1].subs(muK, 0).subs(r0, rp), k, 1 / lst, "-")
C2["s=-1_limit_at_k->1/l-"] = str(pole)
# codim-1 kick invariant: the k -> 0 moment of the modified Green function is unchanged
kick_ratio = sp.limit(1 / (1 + s2 * lst ** 2 * k ** 2), k, 0)
C2["sheet_kick_ratio_k0"] = str(kick_ratio)
C2["P1"] = {"grade": "PASS-WITH-BOUND", "note": "modifies Newton/AQUAL at r <~ l_*; unchanged as l_* -> 0"}
C2["P2"] = {"grade": "PASS-WITH-BOUND"}
_, deg2, nr2 = disp(0, pois_factor=(1 + lst ** 2 * k ** 2), roots=True)
C2["P4"] = {"grade": "PASS" if nr2 + 2 == 3 else "FAIL", "det_degree_in_omega": deg2, "n_W2_roots": nr2,
            "note": "potential terms only, no new time derivatives (HL counting, literature)"}
C2["P5"] = {"grade": "PASS-WITH-BOUND", "note": "R_ij R^ij-type terms change the tensor dispersion at k ~ 1/l_*; c at k -> 0"}
C2["P6"] = {"grade_s+1": "PASS", "grade_s-1": "FAIL (pole: omega^2 -> -inf as k -> 1/l for rho > 0)" if pole in (-sp.oo,) else str(pole)}
n_c2 = [et2[sv][l_]["n"] for sv in (1, -1) for l_ in ("rho+", "rho-")]
C2["FT"] = {"grade": "FAIL" if all(n_ == 0 for n_ in n_c2) and kick_ratio == 1 else "CHECK",
            "removes_fold": False, "n": n_c2}
C2["SC"] = {"new_constants": ["l_* (UV length) and its coefficient"], "how_fixed": "nothing in v3s"}
check("C2-FT", all(n_ == 0 for n_ in n_c2) and kick_ratio == 1,
      f"large-k exponents {n_c2} (k-independent); sheet kick ratio at k -> 0 = {kick_ratio}",
      "C2 leaves n = 0 and the codimension-1 sheet fold unchanged (FT-FAIL), as Mukohyama states for codim 1")
CL["C2"] = C2

# ---------------- C3: native K(Q)
C3 = {"P1": {"grade": "PASS"}, "P2": {"grade": "PASS"}, "P4": {"grade": "PASS", "DOF": 3},
      "P5": {"grade": "PASS"}, "P6": {"grade": "PASS", "note": "X3 (c_s^2 = (Q-1)/Q >= 0 on Q >= 1, C5)"},
      "FT": {"grade": "FAIL", "removes_fold": False,
             "why": "omega^2 -> K rho (M_theta - 1), mu_K-independent, for k^2 >> M_theta mu_K^2 (F5d); q_K < 1 at "
                    "S4-allowed mu_K; p ~ rho^2 genuinely nonlinear where it acts (F5a)"},
      "SC": {"new_constants": [], "how_fixed": "mu_K exists (free, <= 0.1 Mpc^-1 by S4)"}}
CL["C3"] = C3

# ---------------- C4: DBI / BI and the de Rham-Motohashi caustic-free set
C4 = {}
Qs = sp.Symbol("Q", positive=True)
al = sp.Symbol("alpha", real=True)
sgnX = sp.Symbol("sX")                       # X = sX Q^2, sX = +-1
cs2_lin = 1 + al * sgnX * Qs ** 2
al_sol = sp.solve(sp.Eq(cs2_lin.subs(Qs, 1), 0), al)[0]
cs2_dust = sp.simplify(cs2_lin.subs(al, al_sol))
Kf = sp.Function("Kf")
ode = sp.Eq(sp.diff(Kf(Qs), Qs) / (Qs * sp.diff(Kf(Qs), Qs, 2)), cs2_dust)
Kp = sp.Function("Kp")
odep = sp.dsolve(sp.Eq(Kp(Qs) / (Qs * sp.diff(Kp(Qs), Qs)), cs2_dust), Kp(Qs))
C4["dRM_condition"] = "c_s^2 = K'/(Q K'') = 1 + alpha X, X = sX Q^2; dust c_s^2(1) = 0"
C4["alpha"] = str(al_sol)
C4["cs2_on_dust_branch"] = str(cs2_dust)
C4["K_prime_solution"] = str(odep)
cs2_at_11 = float(cs2_dust.subs(Qs, 1.1))
lam = sp.Symbol("lambda_D", positive=True)
zz = sp.Symbol("z", real=True)
K_dbi = 2 * muK ** 2 / lam * (1 - sp.sqrt(1 - lam * zz ** 2))
ser = sp.series(K_dbi, zz, 0, 6).removeO()
C4["BS25_series"] = str(sp.simplify(ser))
Kpp = sp.simplify(sp.diff(K_dbi, zz, 2))
mu2_eff = sp.simplify(Kpp / 2)
w2c4 = to_Mth(disp(0, muK2=mu2_eff.subs(zz, sp.Symbol("zbar", real=True))))
lim_c4 = sp.simplify(sp.limit(w2c4, k, sp.oo))
C4["BS25_large_k_limit"] = str(lim_c4)
C4["P1"] = {"grade": "PASS", "note": "K''(1) = 2 mu^2: same static mass (X6 X-D10)"}
C4["P2"] = {"grade": "PASS"}
C4["P4"] = {"grade": "PASS", "DOF": 3}
C4["P5"] = {"grade": "PASS"}
C4["P6"] = {"grade_BS25": "PASS", "grade_dRM_set": "FAIL" if cs2_at_11 < 0 else "PASS",
            "dRM_cs2_at_Q_1.1": cs2_at_11}
C4["FT"] = {"grade": "FAIL", "removes_fold": False,
            "why": "BS25: inert at k^2 >> M mu^2 (large-k limit mu-independent) and quadratic at lambda z^2 << 1; dRM set: "
                   "c_s^2 = 1 - Q^2 < 0 on the dust branch (Q > 1), K' ~ Q/sqrt(1-Q^2) singular at the dust point; "
                   "Babichev 2016: BI forms caustics in the dust regime"}
C4["SC"] = {"new_constants": ["lambda_D (BS25 P1 = 30, P2 = 1)", "or the Galileon/DBI scale"], "how_fixed": "published values; not derived"}
check("C4-FT", r_F5d == 0 and sp.simplify(lim_c4 - K * r0 * (Mth - 1)) == 0 and cs2_at_11 < 0,
      f"BS25 large-k omega^2 = {lim_c4}; dRM dust-branch c_s^2 = {cs2_dust} ({cs2_at_11:.3f} at Q = 1.1); K' = {odep.rhs}",
      "C4 cannot act at the fold scale (BS25) and the caustic-free set has c_s^2 < 0 on v3s's dust branch")
CL["C4"] = C4

# ---------------- C5: complex scalar (Madelung)
C5 = {}
w2c5 = {tv: to_Mth(disp(tv, bern_extra=(nu ** 2 * k ** 2 / (4 * r0)))) for tv in (1, 0)}
r_c5 = sp.simplify(w2c5[0] - (r0 * (k ** 2 / chi(0) - K) + nu ** 2 * k ** 4 / 4))
et5 = exponent_table(w2c5[0].subs(muK, 0))
C5["omega2_Theta0"] = str(w2c5[0])
C5["form_residual"] = str(r_c5)
C5["exponents_Theta0"] = ptab("", et5)
zl = sp.Symbol("z", positive=True)
sq = sp.Symbol("s_c", positive=True)
Qqp = sp.simplify(-(nu ** 2 / 2) * sp.diff(sp.sqrt(sq * zl), zl, 2) / sp.sqrt(sq * zl))
C5["quantum_potential_for_rho_linear_through_zero"] = str(Qqp)
C5["P1"] = {"grade": "PASS-WITH-BOUND", "note": "static held state gets psi = -Q_nu != const; unchanged as nu -> 0"}
C5["P2"] = {"grade": "PASS-WITH-BOUND"}
_, deg5, nr5 = disp(0, bern_extra=(nu ** 2 * k ** 2 / (4 * r0)), roots=True)
C5["P4"] = {"grade": "FAIL", "DOF": 4, "PN_n_W2_roots": nr5, "PN_det_degree_in_omega": deg5,
            "note": "the non-relativistic PN image has one omega^2 root, but BR17's completion carries two real scalar "
                    "fields (lambda, phi): 2 scalar + 2 tensor = 4 at all energies (the radial mode is heavy, ~M)"}
C5["P5"] = {"grade": "PASS"}
C5["P6"] = {"grade": "FAIL", "note": "rho = |Psi|^2 >= 0: v3s's sign-indefinite charge (soft lobes) is not representable, and "
                                     f"Q_nu = {Qqp} diverges where rho_tau crosses zero (the switch interface)"}
C5["variant_dust_only"] = "complete only rho_d >= 0: inert at mu_K -> 0, the X8/X10 regime (no K(Q) dust there): FT-FAIL"
C5["FT"] = {"grade": "PASS-LIT" if all(et5[l_]["n"] == 4 and et5[l_]["coef_positive"] for l_ in ("rho+", "rho-")) else "FAIL",
            "removes_fold": True}
C5["SC"] = {"new_constants": ["nu = hbar/m (mass M of BR17)"], "how_fixed": "nothing in v3s"}
check("C5-P3", r_c5 == 0 and sp.simplify(Qqp - nu ** 2 / (8 * zl ** 2)) == 0,
      f"omega^2 = rho0(k^2/chi - K) + nu^2 k^4/4 (residual {r_c5}); exponents {ptab('', et5)}; Q_nu(rho = s z) = {Qqp}",
      "C5 is dispersive (n = 4) but singular at rho_tau = 0 and needs rho_tau >= 0")
CL["C5"] = C5

# ---------------- C6: imperfect-DM deformation f(Y/X^2, Z/X^3)
C6 = {}
# vorticity of the foliation normal n_mu = -N d_mu tau (Minkowski, any tau, N): projected curl vanishes identically
# algebraic in first derivatives: g_a = d_a tau, dN_a = d_a N; curl_ab = d_a n_b - d_b n_a = -(dN_a g_b - dN_b g_a)
ga = sp.symbols("g0:4", real=True)
dNa = sp.symbols("dN0:4", real=True)
eta_m = sp.diag(-1, 1, 1, 1)
gvec = sp.Matrix(ga)
Xn = -(gvec.T * eta_m * gvec)[0, 0]
Nv = 1 / sp.sqrt(Xn)
nlow = -Nv * gvec
nup = eta_m * nlow
curl = sp.Matrix(4, 4, lambda a_, b_: -(dNa[a_] * ga[b_] - dNa[b_] * ga[a_]))
hproj = sp.eye(4) + nup * nlow.T                     # h^a_b = delta^a_b + n^a n_b
omg = hproj.T * curl * hproj
vort_zero = all(sp.simplify(e) == 0 for e in omg)
nn = sp.simplify((nlow.T * eta_m * nlow)[0, 0])
C6["n_dot_n"] = str(nn)
Yv = sp.Symbol("Y", positive=True)
Jx = sp.Function("J")
dJ = sp.Function("dJ")
C6["P1"] = {"grade": "FAIL unless f equals v3s's own J(Y)",
            "note": "v3s's Y = |grad Xi|^2/c^4 = A.A/c^4 is non-zero on static fields (Xi = phi + C), so any extra "
                    "acceleration dependence of the constraint function changes the static law mu(x); with f = J it is v3s"}
C6["P4"] = {"grade": "OPEN (the paper defers the Hamiltonian analysis)"}
C6["FT"] = {"grade": "FAIL", "removes_fold": False,
            "why": "the foliation normal's projected curl vanishes identically (vorticity route unavailable to the folding "
                   "congruence); the acceleration route is v3s's own J(Y), already in F1-F4 and in X8/X10, which fold"}
C6["SC"] = {"new_constants": ["a free function f"], "how_fixed": "nothing"}
check("C6-FT", vort_zero, f"h.curl(n).h = 0 for n_mu = -N d_mu tau with N = X^-1/2: {vort_zero}",
      "C6's vorticity route is unavailable to the foliation; its acceleration route is v3s itself")
CL["C6"] = C6

# ---------------- C7, C8 (record / literature)
CL["C7"] = {"P4": {"grade": "FAIL", "DOF": "5 (Einstein-aether: 2 tensor + 2 vector + 1 scalar; record C5 'A33 5'); AeST + gamma_L OPEN"},
            "P5": {"grade": "PASS-WITH-BOUND", "note": "c_T^2 = 1/(1 - c13), |c13| <~ 1e-15 (record DOOR11)"},
            "P6": {"grade": "FAIL (v4 = AeST + gamma_L: omega = 0 negative-energy band, C5)"},
            "FT": {"grade": "FAIL", "removes_fold": False,
                   "why": "AeST's cold sector is the scalar's K(Q) Q-mode, a gradient flow like v3s's; Jacobson-Mattingly's "
                          "simplified aether develops gradient singularities"},
            "SC": {"new_constants": ["c1..c4 (or K_B, K_2)"], "how_fixed": "GW170817 and PPN bounds only"}}
CL["C8"] = {"P4": {"grade": "FAIL", "DOF": "infinite (distribution function) or N per-owner fields"},
            "P6": {"grade": "FAIL", "note": "a particle-like sector (house rule: no dark-matter particle); O1 K6 (no merging, "
                                            "law floor x = N - 1) and K11 (each label's exterior flow folds)"},
            "FT": {"grade": "PASS-CONSTRUCT", "removes_fold": True},
            "SC": {"new_constants": ["field multiplicity / distribution function"], "how_fixed": "nothing"}}

# ---------------- C9: adhesion / sticky continuation
m1s, m2s, v1s, v2s = sp.symbols("m_1 m_2 v_1 v_2", real=True)
vst = (m1s * v1s + m2s * v2s) / (m1s + m2s)
dE = sp.simplify(((m1s + m2s) * vst ** 2 - m1s * v1s ** 2 - m2s * v2s ** 2) / 2)
dE_expected = -m1s * m2s * (v1s - v2s) ** 2 / (2 * (m1s + m2s))
r_c9 = sp.simplify(dE - dE_expected)
dE_mixed = float(dE.subs({m1s: 1.0, m2s: -0.5, v1s: 1.0, v2s: -1.0}))
CL["C9"] = {"merged_velocity": str(vst), "energy_change": str(dE), "energy_change_residual": str(r_c9),
            "energy_change_m1=1,m2=-0.5": dE_mixed,
            "P1": {"grade": "PASS", "note": "smooth static solutions are viscosity solutions"},
            "P4": {"grade": "FAIL", "note": "non-variational (dissipative): no Hamiltonian, no constraint algebra"},
            "P5": {"grade": "PASS"},
            "P6": {"grade": "FAIL", "note": "with sign-indefinite charge the merged velocity diverges as m1 + m2 -> 0 and "
                                            "sticking can create energy (m1 m2 < 0 < m1 + m2)"},
            "FT": {"grade": "PASS-CONSTRUCT", "removes_fold": True},
            "SC": {"new_constants": [], "how_fixed": "nu -> 0+ has no scale"}}
check("C9", r_c9 == 0 and dE_mixed > 0, f"sticky merger dE = {dE}; m1 = 1, m2 = -0.5, v = +-1: dE = {dE_mixed:+.3f} (> 0)",
      "adhesion: zero-scale but ill-defined for v3s's sign-indefinite charge (energy created / v unbounded)")

# ================================================================================================ verdicts
log("")
log("VERDICTS")
# compatibility per frozen rule: P1, P2, P4, P5, P6 PASS or PASS-WITH-BOUND
def grade_ok(gr):
    return isinstance(gr, str) and gr.startswith("PASS")


comp = {}
comp["C1"] = all(grade_ok(CL["C1"][p_]["grade"]) for p_ in ("P1", "P2", "P4", "P5", "P6"))
comp["C2"] = all(grade_ok(CL["C2"][p_]["grade"]) for p_ in ("P1", "P2", "P4", "P5")) and grade_ok(CL["C2"]["P6"]["grade_s+1"])
comp["C3"] = True
comp["C4"] = True     # BS25 form; the dRM set fails P6
comp["C5"] = False
comp["C6"] = False
comp["C7"] = False
comp["C8"] = False
comp["C9"] = False
removes = {c_: bool(CL[c_]["FT"]["removes_fold"]) for c_ in CL}
zero_const = {c_: len(CL[c_]["SC"]["new_constants"]) == 0 for c_ in CL}
qualifying_zero = [c_ for c_ in CL if zero_const[c_] and removes[c_] and comp[c_]]
qualifying_scale = [c_ for c_ in CL if (not zero_const[c_]) and removes[c_] and comp[c_]]
if qualifying_zero:
    v2 = f"A ZERO-CONSTANT COMPLETION EXISTS ({', '.join(qualifying_zero)})"
elif qualifying_scale:
    v2 = "EVERY COMPLETION NEEDS A NEW SCALE"
else:
    v2 = "NO COMPLETION COMPATIBLE WITH v3s's PASSES"
need_i = ["F1a", "F1b", "F1c", "F1d", "F2", "F2-soft", "F3", "F4a", "F4b", "F4c", "F5a", "F5c", "F5d"]
ck = {c_["id"]: c_["pass"] for c_ in CHECKS}
v1 = "CAUSTICS GENERIC (shown analytically)" if all(ck.get(i_, False) for i_ in need_i) else "UNDECIDED"
RES["classes"] = clean(CL)
RES["verdict_inputs"] = {"compatible": comp, "removes_fold": removes, "zero_constant": zero_const,
                         "qualifying_zero_constant": qualifying_zero, "qualifying_with_scale": qualifying_scale}
RES["verdict_i"] = v1
RES["verdict_ii"] = v2
log(f"  (i)  {v1}")
log(f"  (ii) {v2}; qualifying with a new scale: {qualifying_scale}; zero-constant qualifying: {qualifying_zero}")
for c_ in CL:
    log(f"  {c_}: compatible {comp[c_]}, removes fold {removes[c_]} (FT {CL[c_]['FT']['grade']}), new constants "
        f"{CL[c_]['SC']['new_constants']}")

# ================================================================================================ wrap up
req_fail = [c_["id"] for c_ in CHECKS if c_["required"] and not c_["pass"]]
RES["required_failures"] = req_fail
RES["n_checks"] = len(CHECKS)
RES["n_pass"] = sum(c_["pass"] for c_ in CHECKS)
RES["runtime_s"] = time.time() - T0
RES["peak_rss_gb"] = rss_gb()
if MUTATE:
    must_fail = {"F1b": "m1", "C1-P6a": "m2", "F2": "m3", "C1-FT": "m4"}
    RES["mutate_required_failures"] = {cid: {"mutation": m_, "failed": not ck.get(cid, True)} for cid, m_ in must_fail.items()}
    log(f"  MUTATE: required failures {RES['mutate_required_failures']}")
log(f"checks {RES['n_pass']}/{RES['n_checks']} pass; required failures {req_fail}; {RES['runtime_s']:.0f} s; "
    f"peak RSS {RES['peak_rss_gb']:.3f} GB")
with open(JS, "w") as fh:
    json.dump(clean(RES), fh, indent=1)
with open(OUT, "w") as fh:
    fh.write("\n".join(_lines) + "\n")
sys.exit(0 if not req_fail else 1)
