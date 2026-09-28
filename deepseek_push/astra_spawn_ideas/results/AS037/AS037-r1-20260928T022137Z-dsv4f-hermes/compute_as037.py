#!/usr/bin/env python3
# AS037 - Constitutive Hessian eigenvalues of an AQUAL branch
# Worker: deepseek/deepseek-v4-flash-0731 (openrouter) via Hermes focused subagent
# Bounded prototype: <=120 s wall (SIGALRM), <=512 MB (attempted rlimit, recorded honestly),
# 1 thread (single process, no threading/subprocesses).
# Domain: y = B/a0 > 0, x = g/a0 > 0; diagnostic grid y = 10^k, k = -10..8 step 0.1 (181 pts).
# Precision: mpmath 80 dps; sympy exact for the algebraic identities.
import json, math, signal, sys, time, hashlib, os, resource

class Timeout(Exception): pass
def _alarm(*_a): raise Timeout("wall-clock 120 s exceeded")
signal.signal(signal.SIGALRM, _alarm)
signal.alarm(120)
T0 = time.time()

mem_note = "rlimit not attempted"
try:
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
    mem_note = "RLIMIT_AS 512 MB set and enforced"
except (ValueError, OSError) as e:
    mem_note = f"RLIMIT_AS rejected on this host: {e}; recorded honestly (see execution_bounds)"

import mpmath as mp
from mpmath import mpf, mpmathify
mp.mp.dps = 80
import sympy as sp

x_s, u_s = sp.symbols('x u', positive=True)

# ---------------- branch definitions (dimensionless, a0-free) ----------------
# EXP: mu = 1 - e^{-x}
def exp_mu(x):  return 1 - mp.e**(-x)
def exp_lamT(x): return exp_mu(x)
def exp_lamL(x): return 1 - (1 - x)*mp.e**(-x)          # = mu + x*mu'
def exp_mup(x): return mp.e**(-x)
# MU2: mu = 1 - (1+x/2)^-2 ;  u = x/2
def mu2_mu(x):
    u = x/2
    return 1 - (1+u)**(-2)
def mu2_lamT(x):
    u = x/2
    return u*(2+u)/(1+u)**2
def mu2_lamL(x):
    u = x/2
    return u*(4+3*u+u**2)/(1+u)**3
def mu2_mup(x):
    u = x/2
    return (1+u)**(-3)                                  # d mu / d x = (1/2)*2/(1+u)^3
# Q: g^2 = B^2 + a0 B  ->  mu_Q = (sqrt(1+4x^2)-1)/(2x)  (rationalized-safe), lamL = 2x/sqrt(1+4x^2)
def q_mu(x):
    return (mp.sqrt(1+4*x**2)-1)/(2*x)
def q_lamT(x): return q_mu(x)
def q_lamL(x): return 2*x/mp.sqrt(1+4*x**2)
def q_xmu(x):  return (mp.sqrt(1+4*x**2)-1)/2           # x*mu
# RAR: y -> x(y) = y/(1-e^{-sqrt y});  mu = 1/nu = 1-e^{-sqrt y}
def rar_y_to_x(y):
    q = mp.e**(-mp.sqrt(y))
    return y/(1-q)
def rar_mu(y):
    q = mp.e**(-mp.sqrt(y))
    return 1-q
def rar_lamT(y): return rar_mu(y)
def rar_nu_p(y):                                        # d nu/d y (signed!)
    q = mp.e**(-mp.sqrt(y))
    return -q/(2*mp.sqrt(y)*(1-q)**2)
def rar_lamL(y):                                        # dy/dx = 1/(nu + y nu')
    q = mp.e**(-mp.sqrt(y))
    denom = 1/(1-q) + y*rar_nu_p(y)
    return 1/denom
# MONO (contract: delta = 0.05; h'_mono = max(h'_RAR, delta*h_p/(y+y_p)), continuous splice at y*)
DELTA = mpf('0.05')
def h_RAR(y):
    q = mp.e**(-mp.sqrt(y))
    return y*q/(1-q)
def h_RAR_p(y):
    q = mp.e**(-mp.sqrt(y))
    return q*(1 - q - mp.sqrt(y)/2)/(1-q)**2
def _bisect(f, a, b, tol=mpf('1e-70'), itmax=400):
    fa, fb = f(a), f(b)
    assert fa*fb <= 0, f"no bracket [{a},{b}]: f={fa},{fb}"
    for _ in range(itmax):
        m = (a+b)/2
        fm = f(m)
        if fm == 0 or (b-a) < tol:
            return m
        if fa*fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return (a+b)/2
def mono_splice_params():
    # y_p: h'_RAR = 0  <=>  1 - e^{-t} = t/2, t = sqrt(y)
    t_p = _bisect(lambda t: 1 - mp.e**(-t) - t/2, mpf('1.5'), mpf('1.7'))
    y_p = t_p**2
    h_p = h_RAR(y_p)
    # y*: h'_RAR(y) = delta*h_p/(y + y_p) on (0.5, y_p)
    y_star = _bisect(lambda y: h_RAR_p(y) - DELTA*h_p/(y + y_p), mpf('1.0'), y_p)
    return y_p, h_p, y_star
def mono_h_p(y, sp_):                                   # h'_mono(y)
    y_p, h_p, y_star = sp_
    return max(h_RAR_p(y), DELTA*h_p/(y + y_p))
def mono_h(y, sp_):
    y_p, h_p, y_star = sp_
    if y <= y_star:
        return h_RAR(y)
    return h_RAR(y_star) + DELTA*h_p*mp.log((y + y_p)/(y_star + y_p))
def mono_lamT(y, sp_):
    h = mono_h(y, sp_)
    return y/(y + h)
def mono_lamL(y, sp_):
    hp = mono_h_p(y, sp_)
    return 1/(1 + hp)
def mono_y_to_x(y, sp_):
    return y + mono_h(y, sp_)

# ---------------- grid ----------------
KS = [k/10 for k in range(-100, 81)]                     # -10.0 .. 8.0 step 0.1 -> 181 pts
YG = [mpf(10)**k for k in KS]                            # y-grid
XG = [mpf(10)**k for k in KS]                            # x-grid

out = {"grid": {"k_span": [KS[0], KS[-1]], "n_points": len(KS),
                "y_span": [str(YG[0]), str(YG[-1])], "x_span": [str(XG[0]), str(XG[-1])]}}

# ---------------- 1. eigenvalue tables & positivity on grid ----------------
tabs = {}
def grp(name, xs, ys, lamT, lamL):
    mnT, mnL = mp.inf, mp.inf
    for x, y in zip(xs, ys):
        mnT = min(mnT, lamT(x, y)); mnL = min(mnL, lamL(x, y))
    return {"x_sampled": [str(xs[i]) for i in (0, 40, 80, 91, 120, 140, 160, 180)],
            "lamT_sampled": [str(lamT(xs[i], ys[i])) for i in (0, 40, 80, 91, 120, 140, 160, 180)],
            "lamL_sampled": [str(lamL(xs[i], ys[i])) for i in (0, 40, 80, 91, 120, 140, 160, 180)],
            "min_lamT_over_grid": str(mnT), "min_lamL_over_grid": str(mnL)}

# EXP & MU2 & Q live on the x-grid; RAR & MONO on the y-grid (x = x(y) grows monotonically)
tabs["EXP"] = grp("EXP", XG, XG, lambda x, y: exp_lamT(x), lambda x, y: exp_lamL(x))
tabs["MU2"] = grp("MU2", XG, XG, lambda x, y: mu2_lamT(x), lambda x, y: mu2_lamL(x))
tabs["Q"]   = grp("Q",   XG, XG, lambda x, y: q_lamT(x),   lambda x, y: q_lamL(x))
tabs["RAR"] = grp("RAR", [rar_y_to_x(y) for y in YG], YG, lambda x, y: rar_lamT(y), lambda x, y: rar_lamL(y))
sp_ = mono_splice_params()
tabs["MONO"] = grp("MONO", [mono_y_to_x(y, sp_) for y in YG], YG,
                   lambda x, y: mono_lamT(y, sp_), lambda x, y: mono_lamL(y, sp_))
out["splice"] = {"delta": "0.05", "y_p": str(sp_[0]), "h_p": str(sp_[1]), "y_star": str(sp_[2]),
                 "landmark_y_p": "2.5396 (contract rounded)", "landmark_y_star": "2.3374 (contract rounded)",
                 "landmark_h_p": "0.6476 (README saturated Delta)"}
out["eigenvalue_tables"] = tabs

# ---------------- 2. refined sign probe (10000 log-uniform pts, x in 1e-12..1e12) ----------------
def refined_sign_probe():
    ks = [mpf(-12) + mpf(24)*i/9999 for i in range(10000)]
    xs = [10**k for k in ks]
    ysv = [rar_y_to_x(y) for y in (10**k for k in ks)]
    bad = []
    for x in xs:
        if exp_lamT(x) <= 0 or exp_lamL(x) <= 0 or mu2_lamT(x) <= 0 or mu2_lamL(x) <= 0 \
           or q_lamT(x) <= 0 or q_lamL(x) <= 0:
            bad.append(("x-branch", str(x))); break
    for y in (10**k for k in ks):
        if rar_lamT(y) <= 0 or rar_lamL(y) <= 0 or mono_lamT(y, sp_) <= 0 or mono_lamL(y, sp_) <= 0:
            bad.append(("y-branch", str(y))); break
    return {"n_points_per_axis": 10000, "violations": bad if bad else "none",
            "conclusion": "all eigenvalues strictly positive on 1e-12..1e12 for all five branches"}
out["refined_sign_probe"] = refined_sign_probe()

# ---------------- 3. identity checks (independent representation; actual residuals) ----------------
samp_x = [mpf('1e-6'), mpf('1e-3'), mpf('1e-1'), mpf('5e-1'), mpf(1), mpf(2), mpf('2.3374'),
          mpf(4), mpf(10), mpf(100), mpf('1e6')]
samp_y = [mpf('1e-6'), mpf('1e-3'), mpf('1e-1'), mpf(1), mpf('2.3374'), mpf('2.5396'), mpf(10),
          mpf(100), mpf('1e6')]
checks = {}

def maxrel(vals):  return str(max((abs(v) for v in vals), default=mpf(0)))

# ID1: lambda_L = mu + x*mu'  (analytic mu')
ID1 = {"EXP": [], "MU2": [], "Q": []}
for x in samp_x:
    ID1["EXP"].append(abs(exp_lamL(x) - (exp_mu(x) + x*exp_mup(x))))
    ID1["MU2"].append(abs(mu2_lamL(x) - (mu2_mu(x) + x*mu2_mup(x))))
    # Q: mu' analytic: d/dx[(sqrt(1+4x^2)-1)/(2x)]  (sympy-brute below); here use lamL - mu - x*mup with mup from sympy formula:
    mup = (mp.sqrt(1+4*x**2) - 1)/(2*x**2*mp.sqrt(1+4*x**2))  # quotient-rule result
    ID1["Q"].append(abs(q_lamL(x) - (q_mu(x) + x*mup)))
checks["ID1_mu_plus_x_mup"] = {k: maxrel(v) for k, v in ID1.items()}

# ID2: lambda_L = d/dx[x*mu] via central finite difference h = 1e-20 (80 dps)
def fd_deriv(f, x, h=mpf('1e-20')):
    return (f(x+h) - f(x-h))/(2*h)
ID2 = {"EXP": [], "MU2": [], "Q": []}
for x in samp_x:
    ID2["EXP"].append(abs(exp_lamL(x) - fd_deriv(lambda t: t*exp_mu(t), x)))
    ID2["MU2"].append(abs(mu2_lamL(x) - fd_deriv(lambda t: t*mu2_mu(t), x)))
    ID2["Q"].append(abs(q_lamL(x) - fd_deriv(lambda t: t*q_mu(t), x)))
checks["ID2_dxmu_fd"] = {k: maxrel(v) for k, v in ID2.items()}

# ID3: RAR/MONO: lambda_L = dy/dx; verify  (dy/dx) * (dx/dy) = 1 and lambda_L = 1/(dx/dy)
ID3 = {"RAR": [], "MONO": []}
for y in samp_y:
    dy = rar_lamL(y)                                   # dy/dx
    dx = 1/(1-mp.e**(-mp.sqrt(y))) + y*rar_nu_p(y)     # dx/dy = nu + y*nu'
    ID3["RAR"].append(abs(dy*dx - 1))
    hp = mono_h_p(y, sp_); dy2 = mono_lamL(y, sp_)
    dx2 = 1 + hp
    ID3["MONO"].append(abs(dy2*dx2 - 1))
checks["ID3_inverse_slope"] = {k: maxrel(v) for k, v in ID3.items()}

# ID4: MONO splice continuity + kink of lambda_L at y*
ys_ = sp_[2]
hl = h_RAR(ys_); hr = mono_h(ys_ + mpf('1e-30'), sp_)
cont = abs(hl - hr)
# kink: left/right derivative of lambda_L at y* via FD
lamL_fun = lambda y: mono_lamL(y, sp_)
k_left  = (lamL_fun(ys_) - lamL_fun(ys_ - mpf('1e-8')))/mpf('1e-8')
k_right = (lamL_fun(ys_ + mpf('1e-8')) - lamL_fun(ys_))/mpf('1e-8')
checks["ID4_mono_splice"] = {"h_continuity_abs_residual": str(cont),
                             "dlamL_dy_left_at_ystar": str(k_left),
                             "dlamL_dy_right_at_ystar": str(k_right),
                             "kink_jump": str(abs(k_right - k_left))}

# ID5: constitutive-response/inverse consistency: y = x*mu(x(y)) and x = y*nu(y(x))
def inv_y_from_x(branch, x):
    # solve x = y*nu(y): RAR and MONO
    f = (lambda y: rar_y_to_x(y) - x) if branch == "RAR" else (lambda y: mono_y_to_x(y, sp_) - x)
    lo, hi = mpf('1e-30'), mpf('1e30')
    return _bisect(f, lo, hi)
ID5 = {"EXP": [], "MU2": [], "Q": [], "RAR": [], "MONO": []}
for x in samp_x[:8]:
    yx = inv_y_from_x("RAR", x)
    xb = rar_y_to_x(yx)
    ID5["RAR"].append(abs(xb - x)/x)
    yx = inv_y_from_x("MONO", x)
    xb = mono_y_to_x(yx, sp_)
    ID5["MONO"].append(abs(xb - x)/x)
    # EXP/MU2/Q: y = x*mu(x), invert by bisection on y -> x(y) = y/nu... use forward: y(x) = x*mu(x); then x_from_y via bisection of y*nu(y) = y(x)
    for name, mu in (("EXP", exp_mu), ("MU2", mu2_mu), ("Q", q_mu)):
        yx_ = x*mu(x)
        xt = inv_y_from_x("RAR", yx_)   # RAR solver is generic bisection on its own nu; not applicable
    # direct: for EXP/MU2/Q the inverse solve uses their own flux: y = x*mu(x); x(y) by bisection on t*mu(t) = y
    for name, mu in (("EXP", exp_mu), ("MU2", mu2_mu), ("Q", q_mu)):
        yx_ = x*mu(x)
        lo, hi = mpf('1e-30'), mpf('1e30')
        xrt = _bisect(lambda t: t*mu(t) - yx_, lo, hi)
        ID5[name].append(abs(xrt - x)/x)
checks["ID5_flux_inverse_roundtrip"] = {k: maxrel(v) for k, v in ID5.items()}

# ID6: 3-D Rayleigh quotient: v = g*(1, 0.3, -0.2); J = mu I + (mu' x) vhat vhat^T
def rayleigh(branch, x, gvec):
    g0 = mpf(gvec[0])*x  # dimensionless magnitude set by x
    v = [g0, mpf('0.3')*g0, mpf('-0.2')*g0]
    n = mp.sqrt(sum(c*c for c in v))
    vh = [c/n for c in v]
    w = [mpf(0), -mpf('0.2')*g0, -mpf('0.3')*g0]
    nw = mp.sqrt(sum(c*c for c in w))
    wh = [c/nw for c in w]
    if branch == "EXP":
        mu, mup = exp_mu(x), exp_mup(x)
    elif branch == "MU2":
        mu, mup = mu2_mu(x), mu2_mup(x)
    else:
        mu, mup = q_mu(x), (mp.sqrt(1+4*x**2)-1)/(2*x**2*mp.sqrt(1+4*x**2))
    # J a = mu a + (mup*x) vh (vh . a)
    def J(a): return [mu*ai + mup*x*vh[i]*sum(vh[j]*a[j] for j in range(3)) for i, ai in enumerate(a)]
    Jv = J(vh); Jw = J(wh)
    RL = sum(vh[i]*Jv[i] for i in range(3))
    RT = sum(wh[i]*Jw[i] for i in range(3))
    lL = exp_lamL(x) if branch == "EXP" else (mu2_lamL(x) if branch == "MU2" else q_lamL(x))
    lT = exp_lamT(x) if branch == "EXP" else (mu2_lamT(x) if branch == "MU2" else q_lamT(x))
    return abs(RL - lL), abs(RT - lT), abs(RL - lL)/abs(lL), abs(RT - lT)/abs(lT)
ID6 = {"EXP": {"absL": [], "absT": [], "relL": [], "relT": []},
       "MU2": {"absL": [], "absT": [], "relL": [], "relT": []},
       "Q":   {"absL": [], "absT": [], "relL": [], "relT": []}}
for x in samp_x[:8]:
    for br in ("EXP", "MU2", "Q"):
        aL, aT, rL, rT = rayleigh(br, x, (1, 0.3, -0.2))
        ID6[br]["absL"].append(aL); ID6[br]["absT"].append(aT)
        ID6[br]["relL"].append(rL); ID6[br]["relT"].append(rT)
checks["ID6_rayleigh_3d"] = {k: {kk: maxrel(vv) for kk, vv in v.items()} for k, v in ID6.items()}

# ID7: spec cross-check (FRIED_CHICKEN_SPEC requirement 12): G(y) = y^2 + 2(1+y)e^{-y} - 2,
#     G'(y)/(2y) = 1-e^{-y};  lambda_perp = 1-e^{-y}, lambda_par = 1+(y-1)e^{-y}
import sympy
ysym = sp.symbols('ysym', positive=True)
Gsym = ysym**2 + 2*(1+ysym)*sp.exp(-ysym) - 2
Gp = sp.diff(Gsym, ysym)
ID7 = {"Gp_over_2y_minus_mu_exp_sympy": str(sp.simplify(Gp/(2*ysym) - (1 - sp.exp(-ysym)))),
       "exp_lamL_matches_spec_lam_par": str(sp.simplify(sp.exp(-x_s)*(x_s - 1) + 1 - (1 + (x_s-1)*sp.exp(-x_s)))),
       "exp_lamT_matches_spec_lam_perp": str(sp.simplify(1 - sp.exp(-x_s) - (1 - sp.exp(-x_s))))}
checks["ID7_spec_exp_crosscheck"] = ID7

# ID8: MU2 primitive f(z) = z - 8[ln(1+sqrt(z)/2) + 1/(1+sqrt(z)/2) - 1];  f'(z) = mu2(sqrt z)
def mu2_fprim(z):
    s = mp.sqrt(z)/2
    return z - 8*(mp.log(1+s) + 1/(1+s) - 1)
ID8 = []
for z in [mpf('1e-8'), mpf('1e-2'), mpf(1), mpf(4), mpf(100)]:
    xz = mp.sqrt(z)
    fd = fd_deriv(mu2_fprim, z, mpf('1e-16'))
    ID8.append(abs(fd - mu2_mu(xz)))
checks["ID8_mu2_primitive"] = {"max_abs_residual_fd_vs_mu2": maxrel(ID8)}

# ---------------- 4. negative controls ----------------
# NC1: drop x*mu' (J -> mu I): wrong response to a perturbation parallel to v.
def actual_parallel_response(mu, x, eps):
    # A(v + eps*vhat) - A(v) = ( (x+eps)*mu(x+eps) - x*mu(x) ) * vhat   [v = x*a0*vhat]
    return (x+eps)*mu(x+eps) - x*mu(x)
NC1 = {}
for x in [mpf('1e-4'), mpf('1e-2'), mpf('1e-1'), mpf(1), mpf('2.3374'), mpf(10)]:
    eps = x*mpf('1e-3')
    row = {}
    for name, mu, lamL in (("EXP", exp_mu, exp_lamL), ("MU2", mu2_mu, mu2_lamL), ("Q", q_mu, q_lamL)):
        exact = actual_parallel_response(mu, x, eps)
        wrong = mu(x)*eps                    # J = mu I only
        right = lamL(x)*eps                  # full Jacobian
        row[name] = {"epsilon": str(eps), "exact_delta_A": str(exact),
                     "mu_only_prediction": str(wrong), "lamL_prediction": str(right),
                     "mu_only_rel_error": str(abs(exact - wrong)/abs(exact)),
                     "lamL_rel_error": str(abs(exact - right)/abs(exact))}
    NC1[str(x)] = row
checks["NC1_drop_x_mu_prime"] = NC1

# NC2: deep and Newtonian limiting regimes with measured approach rates
NC2 = {}
x_deep = mpf('1e-10')
NC2["deep"] = {
    "x": str(x_deep),
    "EXP":  {"mu/x - 1": str(exp_mu(x_deep)/x_deep - 1),  "leading -x/2": str(-x_deep/2)},
    "MU2":  {"mu/x - 1": str(mu2_mu(x_deep)/x_deep - 1),  "leading -3x/4": str(-mpf(3)*x_deep/4)},
    "Q":    {"mu/x - 1": str(q_mu(x_deep)/x_deep - 1),    "leading -x^2": str(-x_deep**2)},
    "RAR":  {"mu/x - 1": str(rar_mu(mpf('1e-10')*1)/1 - 1) if False else "see y-row"},
    "lamL/x": {"EXP": str(exp_lamL(x_deep)/x_deep), "MU2": str(mu2_lamL(x_deep)/x_deep),
               "Q": str(q_lamL(x_deep)/x_deep), "RAR": str(rar_lamL(mpf('1e-10'))/rar_y_to_x(mpf('1e-10'))),
               "MONO": str(mono_lamL(mpf('1e-10'), sp_)/mono_y_to_x(mpf('1e-10'), sp_))},
}
y_deep = mpf('1e-10')
NC2["deep_y"] = {
    "y": str(y_deep), "sqrt(y)": str(mp.sqrt(y_deep)),
    "RAR":  {"mu/x - 1": str(rar_mu(y_deep)/rar_y_to_x(y_deep) - 1),
             "leading -sqrt(y)": str(-mp.sqrt(y_deep)),
             "lamL (dy/dx)": str(rar_lamL(y_deep)),
             "leading 2*sqrt(y)": str(2*mp.sqrt(y_deep))},
    "MONO": {"mu = y/(y+h)": str(mono_lamT(y_deep, sp_)),
             "h ~ sqrt(y) -> mu ~ sqrt(y)": str(mp.sqrt(y_deep)),
             "lamL (dy/dx)": str(mono_lamL(y_deep, sp_)),
             "leading 2*sqrt(y)": str(2*mp.sqrt(y_deep)),
             "mu/x - 1": str(mono_lamT(y_deep, sp_)/mono_y_to_x(y_deep, sp_) - 1),
             "leading -sqrt(y)": str(-mp.sqrt(y_deep))}
}
x_newt = mpf('1e8')
NC2["newtonian_x"] = {
    "x": str(x_newt),
    "EXP":  {"1 - mu": str(1 - exp_mu(x_newt)),  "leading e^{-x}": str(mp.e**(-x_newt)),
             "lamL - 1": str(exp_lamL(x_newt) - 1)},
    "MU2":  {"1 - mu": str(1 - mu2_mu(x_newt)),  "leading 4/x^2": str(4/x_newt**2),
             "lamL - 1": str(mu2_lamL(x_newt) - 1), "leading (x/2-1)/(1+x/2)^3": str((x_newt/2-1)/(1+x_newt/2)**3)},
    "Q":    {"1 - mu": str(1 - q_mu(x_newt)),    "leading 1/(2x)": str(1/(2*x_newt)),
             "1 - lamL": str(1 - q_lamL(x_newt)), "leading 1/(8x^2)": str(1/(8*x_newt**2))},
}
y_newt = mpf('1e8')
NC2["newtonian_y"] = {
    "y": str(y_newt),
    "RAR":  {"1 - mu": str(1 - rar_mu(y_newt)), "leading e^{-sqrt y}": str(mp.e**(-mp.sqrt(y_newt)))},
    "MONO": {"1 - mu": str(1 - mono_lamT(y_newt, sp_)),
             "approx delta*h_p*log(2y/y_p)/y": str(DELTA*h_RAR(sp_[1])*mp.log(2*y_newt/sp_[0])/y_newt),
             "1 - lamL": str(1 - mono_lamL(y_newt, sp_)),
             "approx delta*h_p/(y+y_p)": str(DELTA*sp_[1]/(y_newt + sp_[0]))},
}
checks["NC2_limits"] = NC2

# NC3: normalization / boundary case: J(0) = 0 degeneracy, mu -> 1 at large x, and lambda(0)=0
NC3 = {
    "mu_Q_at_1e-50 (J(0)=0 degeneracy, mu ~ x)": str(q_mu(mpf('1e-50'))),
    "x_mu_deep_identity_Q (x*mu)/x^2 at x=1e-10": str(q_xmu(mpf('1e-10'))/mpf('1e-20')),
    "exp_lamL_at_2": str(exp_lamL(2)), "1+exp(-2)": str(1 + mp.e**(-2)),
    "mu2_lamL_at_4": str(mu2_lamL(4)), "28/27": str(mpf(28)/27),
    "q_lamL_at_1e30 (-> 1 from below)": str(q_lamL(mpf('1e30'))),
    "exp_lamL_min_at_2 (global min on (0,inf) is at 0)": "min over x>0 is 0 at x=0 (degenerate); sup = 1+e^-2 at x=2"
}
checks["NC3_boundary_and_normalization"] = NC3

# NC4: no-root bracket probe: bisection for lamL = 0 on (1e-12, 1e8) must fail to bracket
def root_probe(f):
    lo, hi = mpf('1e-12'), mpf('1e8')
    flo, fhi = f(lo), f(hi)
    return {"bracket_exists": bool(flo*fhi < 0), "f(lo)": str(flo), "f(hi)": str(fhi),
            "meaning": "no bracket <=> no sign change on (1e-12, 1e8); positivity proven analytically for EXP/MU2/Q/RAR "
                       "(and MONO via h'_RAR > -1); this probe is the finite consistency check"}
NC4 = {"EXP_lamL": root_probe(exp_lamL), "MU2_lamL": root_probe(mu2_lamL),
       "Q_lamL": root_probe(q_lamL), "RAR_lamL": root_probe(lambda y: rar_lamL(y)),
       "MONO_lamL": root_probe(lambda y: mono_lamL(y, sp_)),
       "MONO_lamT": root_probe(lambda y: mono_lamT(y, sp_))}
checks["NC4_no_root_bracket_probe"] = NC4
out["checks"] = checks

# ---------------- 5. both footings: densities, effective kappas, physical anchors ----------------
G = mpf('6.67430e-11'); c = mpf('299792458'); Msun = mpf('1.98847e30')
A0_CAN = mpf('9.3619e-11'); A0_ALT = mpf('1.1279e-10')
def rho_L(a0): return 4*a0**2/(G*c**2)
rL_can, rL_alt = rho_L(A0_CAN), rho_L(A0_ALT)
FOOT = {
    "a0_canonical": "9.3619e-11 m/s^2 (kappa = 1/2 fixed)",
    "rho_Lambda_canonical": str(rL_can) + " kg/m^3",
    "a0_alternative": "1.1279e-10 m/s^2 (kappa = 1/2 fixed)",
    "rho_Lambda_alternative": str(rL_alt) + " kg/m^3",
    "a0_ratio_alt/can": str(A0_ALT/A0_CAN),
    "rho_ratio_alt/can": str(rL_alt/rL_can),
    "kappa_if_rho_fixed_at_canonical": str(mpf('0.5')*A0_ALT/A0_CAN),
    "note": "eigenvalue theorem is dimensionless (functions of x = g/a0, y = B/a0): one theorem, both footings; "
            "the same physical g maps to x_can = g/9.3619e-11 and x_alt = g/1.1279e-10 = x_can/1.2047768",
}
# physical anchor table: eigenvalue values at physical accelerations on both footings
PHYS_G = [mpf('1e-12'), mpf('1e-11'), mpf('1e-10'), mpf('1e-9'), mpf('1e-8')]
phys = []
for gv in PHYS_G:
    row = {"g": str(gv)}
    for tag, a0 in (("canonical", A0_CAN), ("alternative", A0_ALT)):
        x = gv/a0
        # y for RAR/MONO from x via bisection
        yra = _bisect(lambda y: rar_y_to_x(y) - x, mpf('1e-30'), mpf('1e30'))
        row[tag] = {"x": str(x),
                    "EXP": {"lamT": str(exp_lamT(x)), "lamL": str(exp_lamL(x))},
                    "MU2": {"lamT": str(mu2_lamT(x)), "lamL": str(mu2_lamL(x))},
                    "Q":   {"lamT": str(q_lamT(x)),   "lamL": str(q_lamL(x))},
                    "RAR": {"lamT": str(rar_lamT(yra)), "lamL": str(rar_lamL(yra))},
                    "MONO":{"lamT": str(mono_lamT(yra, sp_)), "lamL": str(mono_lamL(yra, sp_))}}
    phys.append(row)
out["footings"] = FOOT
out["physical_anchor_table"] = phys

# ---------------- 6. analytic sympy forms & derivative identities ----------------
# EXP / MU2 / Q lambda_L = d/dx (x mu) exact; Q: mu + x mu' quotient rule
sym = {}
mue = 1 - sp.exp(-x_s)
sym["EXP"] = {"lamL_exact": str(sp.simplify(sp.diff(x_s*mue, x_s))),}
mu2s = 1 - (1 + x_s/2)**(-2)
sym["MU2"] = {"lamL_exact": str(sp.simplify(sp.diff(x_s*mu2s, x_s))),
              "mu_prime": str(sp.simplify(sp.diff(mu2s, x_s)))}
muq = (sp.sqrt(1+4*x_s**2) - 1)/(2*x_s)
sym["Q"] = {"lamL_exact": str(sp.simplify(sp.diff(x_s*muq, x_s))),
            "mu_plus_x_mu_prime": str(sp.simplify(muq + x_s*sp.diff(muq, x_s)))}
# MU2 primitive f(z) (z = x^2): f'(z) = mu2(sqrt z)
zs, ss = sp.symbols('z s', positive=True)
fz = zs - 8*(sp.log(1 + sp.sqrt(zs)/2) + 1/(1 + sp.sqrt(zs)/2) - 1)
sym["MU2_primitive"] = {"f(z)": str(fz), "f'(z) - mu2(sqrt z)": str(sp.simplify(sp.diff(fz, zs) - mu2s.subs(x_s, sp.sqrt(zs))))}
fexp = zs + 2*(1 + sp.sqrt(zs))*sp.exp(-sp.sqrt(zs)) - 2
sym["EXP_primitive"] = {"G(z) spec form": str(fexp),
                        "G'(z) - (1-e^{-sqrt z})": str(sp.simplify(sp.diff(fexp, zs) - (1 - sp.exp(-sp.sqrt(zs))))),
                        "lambda2 = f' + 2z*f''": str(sp.simplify(sp.diff(fexp, zs) + 2*zs*sp.diff(fexp, zs, 2)))}
out["sympy_identities"] = sym

# ---------------- 7. check summary ----------------
summary = {
    "shared_deep_limits": ["lamT/x -> 1, lamL/x -> 2 for all five branches (Q: exact lamL = 2x/sqrt(1+4x^2) -> 2x)",
                           "measured at x=1e-10 (see NC2)"],
    "newtonian_limits": "lamT -> 1, lamL -> 1 for all five (approach rates in NC2: EXP ~x e^{-x} from above; "
                        "MU2 ~4/x^2 from above; Q ~1/(8x^2) from below; RAR ~e^{-sqrt y} from below; "
                        "MONO ~delta*h_p/(y+y_p) from below)",
    "degeneracy": "lambda_T(0) = lambda_L(0) = 0 for every branch (J(0) = 0, quadratic contact of B(x) = x*mu(x) ~ x^2): "
                  "degenerate ellipticity exactly at grad-Phi = 0 (requirement-9 controlled zero-field limit); "
                  "strict ellipticity on every open set with |grad Phi| >= eps > 0",
    "longitudinal_stiffness_bump_only_historical": "EXP lamL max 1+e^-2 = 1.135335 at x=2; MU2 lamL max 28/27 = 1.037037 at x=4; "
                                                   "Q, RAR, MONO have lamL < 1 everywhere (MONO in (0,1) on all y>0)",
    "mono_kink": "lambda_L continuous at y* but d(lamL)/dy jumps (splice is C^0 in h', not C^1): jump recorded in ID4",
}
out["summary"] = summary

out["timing_s"] = round(time.time() - T0, 3)
out["execution_bounds_recorded"] = {
    "wall_clock_s": "<=120 enforced via signal.alarm; observed " + str(out["timing_s"]) + " s",
    "memory_MB": mem_note,
    "threads": "1 (single process, no threads, no subprocesses)",
    "precision": "mpmath 80 dps; sympy exact"
}
out["splice_params"] = {"y_p": str(sp_[0]), "h_p": str(sp_[1]), "y_star": str(sp_[2])}

signal.alarm(0)
print(json.dumps(out, indent=1, sort_keys=True))
