#!/usr/bin/env python3
"""cfg157_b1 -- CFG157: independent re-derivation of CFG121's B1 medium budget F_req and Q*.
F_req(x) = M_c(<r) / (4 pi eps_c Q r^3 rho_tgt(r)), eps_c = Q = 1, rho_tgt r^3 g_tot = (a0/4pi) m(<r), g_tot = G (m+M_c)/r^2, so
F_req = w v / (x^2 mu) in units M, r_M (w = M_c/M, v = (m+M_c)/M, mu = m/M).  Q* = max_x F_req / 0.10 (pass line F_allow = 0.10).
Target ODE (CFG44 (T)): (m+M_c) dM_c/dr = (a0/G) r m, M_c(0)=0  ->  dv/dx = mu' + x mu / v,  dimensionless, beta = h/r_M.
Frozen: CFG157_FROZEN_CRITERIA.md.  MUTATE=pm_target: the ODE solution is replaced by the point-mass closed form w = sqrt(1+x^2)-1 on the extended baryons.
Exit: main 0 (integrity pass) / 2; MUTATE 1 if it bites, else 0.  README numbers are targets read, not blind predictions."""
import os, sys, math, json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import gammainc
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg157_common import *

MUTATE = os.environ.get("MUTATE", "")
assert MUTATE in ("", "pm_target")
TAG = "" if not MUTATE else "_MUTATE_" + MUTATE
T = Tee(os.path.join(HERE, "cfg157_b1%s.out" % TAG))
P = T.P
FAL = 0.10
README = {"Qstar": 9.68, "Fmax": 0.97, "Fmin": 0.41}

def mu_f(x, beta):
    return gammainc(3.0, x / beta)
def mup_f(x, beta):
    s = x / beta
    return (s * s * np.exp(-s) / 2.0) / beta

def solve_v(beta, xs_eval, x0f=1e-9, rtol=1e-12, xmax=None):
    """v(x) = (m+M_c)/M by integrating dv/dlnx = x[mu' + x mu/v] from x0 = x0f*beta, start from the analytic deep series w0^2 = (2/5) c x^5, c = 1/(6 beta^3)"""
    x0 = x0f * beta
    c = 1.0 / (6.0 * beta ** 3)
    w0 = math.sqrt(0.4 * c * x0 ** 5)
    v0 = float(mu_f(x0, beta)) + w0
    xmax = xmax or float(xs_eval.max())
    f = lambda lx, v: [math.exp(lx) * (mup_f(math.exp(lx), beta) + math.exp(lx) * mu_f(math.exp(lx), beta) / v[0])]
    sol = solve_ivp(f, [math.log(x0), math.log(xmax)], [v0], method="DOP853", rtol=rtol, atol=1e-300, dense_output=True)
    return sol.sol(np.log(xs_eval))[0]

def Freq(x, v, mu):
    w = v - mu
    return w * v / (x * x * mu)

def analysis(beta, x, mutate=False, **kw):
    mu = mu_f(x, beta)
    if mutate:
        v = mu + (np.sqrt(1 + x * x) - 1.0)
    else:
        v = solve_v(beta, x, **kw)
    return mu, v, Freq(x, v, mu)

res = {"mutate": MUTATE, "footings": {}}
P("CFG157 B1 (MUTATE=%s).  README targets read before deriving: F_req 0.41-0.97, Q*=9.68 (pass line F_allow 0.10)." % (MUTATE or "none"))
P("Path handling prints only bare names / <repo>-relative names.\n")

x121 = grid_x(121, 0.1, 30)
x03 = grid_x(121, 0.3, 30)
P("=== integrity checks ===")
ok_e = True
# (e) point-mass ODE reproduction: mu = 1
def pm_solve(xs):
    f = lambda lx, v: [math.exp(lx) * (math.exp(lx) / v[0])]
    x0 = 1e-8
    sol = solve_ivp(f, [math.log(x0), math.log(xs.max())], [1.0], method="DOP853", rtol=1e-13, atol=1e-300, dense_output=True)
    return sol.sol(np.log(xs))[0]
vpm = pm_solve(x121)
e_pm = float(np.max(np.abs(vpm ** 2 - (1 + x121 ** 2)) / (1 + x121 ** 2)))
T.check("(e1) point-mass ODE: (M+M_c)^2 = M^2(1+x^2) to 1e-8 (max rel %.2e)" % e_pm, e_pm < 1e-8)
for fname, a0 in A0.items():
    P("\n-- footing %s: a0 = %.4e" % (fname, a0))
    rec = {}
    Fall121, Fall03 = [], []
    for M in MASSES:
        beta = h_of_M(M) / rM(M * MSUN, a0, G_CFG121)
        xmax = max(30.0, 31 * beta + 2)
        xfull = np.unique(np.concatenate([x121, x03, [30.0], np.array([31 * beta + 1])]))
        if not MUTATE:
            v_a = solve_v(beta, xfull, xmax=xmax)
            v_b = solve_v(beta, xfull, x0f=1e-10, rtol=1e-13, xmax=xmax)     # start radius / 10 and tighter tolerance
            e_conv = float(np.max(np.abs(v_a / v_b - 1)))
            T.check("(e2) M=%.0e %s: ODE start r0/10 and rtol 1e-13 change v by %.2e (< 1e-8)" % (M, fname, e_conv), e_conv < 1e-8) if True else None
            # first integral outside the baryons: v^2 - v_e^2 = x^2 - x_e^2, s_e = 30
            xe = 30 * beta
            xo = np.array([xe, 31 * beta + 1]) if 31 * beta + 1 > xe else None
            ve, vo = solve_v(beta, np.array([xe, max(30.0, xe + 1)]), xmax=xmax)
            fi = abs((vo ** 2 - ve ** 2) - (max(30.0, xe + 1) ** 2 - xe ** 2)) / max(30.0, xe + 1) ** 2
            T.check("(e3) M=%.0e %s: first integral (M+M_c)^2-(M+M_c,e)^2=(a0M/G)(r^2-r_e^2) outside s=30: rel %.2e (< 1e-6)" % (M, fname, fi), fi < 1e-6)
        mu, v, F = analysis(beta, x121, MUTATE == "pm_target")
        mu3, v3, F3 = analysis(beta, x03, MUTATE == "pm_target")
        # residual of the target ODE (mutation makes it fail): dv/dlnx by centred difference of the returned v on the log grid
        xx = grid_x(2001, 0.1, 30)
        mm, vv, _ = analysis(beta, xx, MUTATE == "pm_target")
        dvdx = np.gradient(vv, xx)
        resid = np.max(np.abs((dvdx - mup_f(xx, beta) - xx * mm / vv) / (xx * mm / vv))[5:-5])
        rec[str(M)] = {"beta": beta, "Fmin_0.1_30": float(F.min()), "Fmax_0.1_30": float(F.max()), "x_at_Fmin": float(x121[np.argmin(F)]),
                       "Fmin_0.3_30": float(F3.min()), "Fmax_0.3_30": float(F3.max()), "x_at_Fmin_0.3": float(x03[np.argmin(F3)]),
                       "F_at_x0.3": float(analysis(beta, np.array([0.3]), MUTATE == "pm_target")[2][0]),
                       "ode_residual": float(resid), "F_at_x": {("%g" % xx_): float(analysis(beta, np.array([xx_]), MUTATE == "pm_target")[2][0]) for xx_ in (0.1, 0.3, 1, 3, 10, 30)}}
        Fall121.append(F); Fall03.append(F3)
        P("  M=%.0e beta=%.3f: F_req on [0.1,30]: min %.4f (x=%.3f) max %.4f; on [0.3,30]: min %.4f (x=%.3f) max %.4f; F(0.3)=%.4f; ODE residual (2001-pt gradient) %.2e" % (
            M, beta, F.min(), x121[np.argmin(F)], F.max(), F3.min(), x03[np.argmin(F3)], F3.max(), rec[str(M)]["F_at_x0.3"], resid))
    A121, A03 = np.concatenate(Fall121), np.concatenate(Fall03)
    ov = {"Fmin_0.1_30": float(A121.min()), "Fmax_0.1_30": float(A121.max()), "Fmin_0.3_30": float(A03.min()), "Fmax_0.3_30": float(A03.max())}
    ov["Qstar_0.1_30"] = ov["Fmax_0.1_30"] / FAL
    ov["Qstar_0.3_30"] = ov["Fmax_0.3_30"] / FAL
    rec["overall"] = ov
    P("  OVERALL (all masses): F_req range [0.1,30]: %.4f - %.4f; [0.3,30]: %.4f - %.4f; Q* = max/0.10 = %.3f ([0.1,30]) / %.3f ([0.3,30])" % (
        ov["Fmin_0.1_30"], ov["Fmax_0.1_30"], ov["Fmin_0.3_30"], ov["Fmax_0.3_30"], ov["Qstar_0.1_30"], ov["Qstar_0.3_30"]))
    # analytic point-mass check of F: y+1-sqrt(y^2+y)
    xa = np.array([0.3, 3.0, 30.0]); ya = 1 / xa ** 2
    P("  point-mass closed form F = y+1-sqrt(y^2+y) at x=0.3,3,30: %s ; small-r deep limit 2/5 = 0.4" % " ".join("%.5f" % (yy + 1 - math.sqrt(yy * yy + yy)) for yy in ya))
    res["footings"][fname] = rec

can = res["footings"]["canonical"]["overall"]
P("\n=== comparison with CFG121 README (canonical footing) ===")
def within(a, b, t):
    return abs(a - b) <= t * b
qs_ok = within(can["Qstar_0.1_30"], README["Qstar"], 0.02) or within(can["Qstar_0.3_30"], README["Qstar"], 0.02)
fx_ok = within(can["Fmax_0.1_30"], README["Fmax"], 0.02)
best_min = min((can["Fmin_0.1_30"], can["Fmin_0.3_30"]), key=lambda v: abs(v - README["Fmin"]))
fn_ok = within(best_min, README["Fmin"], 0.03)
P("  Q*: mine %.3f / %.3f vs README 9.68 (2%%: 9.48-9.87) -> %s" % (can["Qstar_0.1_30"], can["Qstar_0.3_30"], "REPRODUCES" if qs_ok else "DISAGREES"))
P("  max F_req: mine %.4f vs README 0.97 (2%%) -> %s" % (can["Fmax_0.1_30"], "REPRODUCES" if fx_ok else "DISAGREES"))
P("  min F_req: mine %.4f ([0.1,30]) / %.4f ([0.3,30]) vs README 0.41 (3%%; closest convention used) -> %s" % (can["Fmin_0.1_30"], can["Fmin_0.3_30"], "REPRODUCES" if fn_ok else "DISAGREES"))
res["B1_verdict"] = {"Qstar": "REPRODUCES" if qs_ok else "DISAGREES", "Fmax": "REPRODUCES" if fx_ok else "DISAGREES", "Fmin": "REPRODUCES" if fn_ok else "DISAGREES"}
P("  B1 verdict vs door line 0.10: F_req > 0.10 everywhere for all masses -> FAIL for the door (min %.3f)" % can["Fmin_0.1_30"])

bite = None
if MUTATE:
    P("\n=== MUTATE=pm_target control ===")
    # main-run reference computed here with the true ODE
    ref_min = 1e9
    for M in MASSES:
        beta = h_of_M(M) / rM(M * MSUN, A0["canonical"], G_CFG121)
        ref_min = min(ref_min, analysis(beta, x121)[2].min())
    mut_min = can["Fmin_0.1_30"]
    resid = max(res["footings"]["canonical"][str(M)]["ode_residual"] for M in MASSES)
    P("  min F_req: main (true ODE) %.4f -> mutated %.4f (change %.1f%%); ODE residual of the mutated target %.3e (main: ~1e-6 numerical-gradient level)" % (ref_min, mut_min, 100 * (mut_min / ref_min - 1), resid))
    bite = abs(mut_min / ref_min - 1) > 0.10
    P("  declared: min F_req rises to >= 0.5 and the ODE check fails: observed min %.4f; ODE-check %s" % (mut_min, "FAILS" if resid > 1e-3 else "does not fail"))
    P("  CONTROL %s" % ("BITES (exit 1)" if bite else "DOES NOT BITE (exit 0, kept)"))
    res["bite"] = bool(bite); res["ref_min"] = ref_min; res["mut_min"] = mut_min

res["integrity_fails"] = T.fails
json.dump(res, open(os.path.join(HERE, "cfg157_b1%s_results.json" % TAG), "w"), indent=1)
P("\nwrote cfg157_b1%s.out and cfg157_b1%s_results.json" % (TAG, TAG))
T.close()
if MUTATE:
    sys.exit(1 if bite else 0)
sys.exit(2 if T.fails else 0)
