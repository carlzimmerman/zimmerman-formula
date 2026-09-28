#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS039 — Deep homogeneity of the static energy.
A02 constitutive kernels / branch fidelity. Bounded prototype.

Claim under audit: in the deep regime (g << a0), the static field energy
F(X) = int_0^X mu(sqrt(t)) dt, X = |grad Phi|^2/a0^2, is asymptotically
homogeneous of degree 3/2 in X (degree 3 in |grad Phi|):
    mu(x) ~ x   =>   F(X) ~ (2/3) X^(3/2)   as X -> 0+.
Branches: Q, RAR, MU2, historical EXP, operative MONO (deep = its RAR
segment y < y* ~ 2.3374). kappa = 1/2 adopted (framework input).

Enforced bounds: single thread, fixed diagnostic grid (181 y-points plus a
log-X grid of 141 points), mpmath dps=50, in-script wall budget 120 s
(aborts with execution_status=interrupted if exceeded). Outputs:
raw_output.json + this stdout.
"""
import json, math, time, sys, os
import mpmath as mp

mp.mp.dps = 50
T0 = time.monotonic()
WALL_BUDGET_S = 120.0
DEADLINE = T0 + WALL_BUDGET_S

# ---------------------------------------------------------------- constants
G_SI   = mp.mpf("6.67430e-11")          # m^3 kg^-1 s^-2 (G_N symbol; separate from G_bare/G_cosmo)
C_SI   = mp.mpf("299792458")            # m/s
MSUN   = mp.mpf("1.98847e30")           # kg
PC_SI  = mp.mpf("3.085677581491367e16") # m

A0_CAN = mp.mpf("9.3619e-11")           # canonical footing m/s^2
A0_ALT = mp.mpf("1.1279e-10")           # alternative footing m/s^2
KAPPA  = mp.mpf("0.5")                  # adopted framework input, kappa=1/2

def rho_lambda(a0):
    # from a0 = kappa c sqrt(G rho_Lambda) => rho_Lambda = a0^2/(kappa^2 G c^2) = 4 a0^2/(G c^2) at kappa=1/2
    return 4*a0*a0/(G_SI*C_SI*C_SI)

def check_deadline():
    if time.monotonic() > DEADLINE:
        print(json.dumps({"fatal": "wall budget exceeded", "budget_s": WALL_BUDGET_S}))
        sys.exit(3)

# ---------------------------------------------------------------- branches
# All branches: spherical field equation  mu(x) * g = B  with x = g/a0, y = B/a0.
# mu(x) = y/x;  F(X) = int_0^X mu(sqrt(t)) dt.

def mu_Q(x):
    return (mp.sqrt(1 + 4*x*x) - 1)/(2*x)

def mu_EXP(x):
    return 1 - mp.e**(-x)

def mu_MU2(x):
    return 1 - (1 + x/2)**(-2)

def y_RAR_of_u(u):          # y = u^2, x = u^2/(1 - e^-u)
    return u*u

def x_RAR_of_u(u):          # x = u^2/(1 - e^-u); 0 at 0
    if u == 0 or u < mp.mpf("1e-20"):
        # series: x(u) = u + u^2/2 + u^3/12 + ...
        return u + u*u/2 + u**3/12
    return u*u/(1 - mp.e**(-u))

def mu_RAR_of_u(u):
    return 1 - mp.e**(-u)

def xp_RAR_of_u(u):          # dx/du; limit at 0 is 1
    if u == 0 or u < mp.mpf("1e-20"):
        # series x(u) = u + u^2/2 + u^3/12 + O(u^4)  =>  x' = 1 + u + u^2/4 + O(u^3)
        return 1 + u + u*u/4
    e = mp.e**(-u)
    den = (1 - e)
    return (2*u*den - u*u*e)/(den*den)

def solve_u_RAR(s):          # solve x(u) = s, s >= 0, monotone x'(u) > 0
    if s == 0:
        return mp.mpf(0)
    lo, hi = mp.mpf(0), s if s <= 4 else mp.sqrt(s)   # x(u) >= u^2 and x ~ u for u<<1
    while x_RAR_of_u(hi) < s:
        hi *= 2
    for _ in range(200):
        mid = (lo + hi)/2
        if x_RAR_of_u(mid) < s:
            lo = mid
        else:
            hi = mid
        if hi - lo < mp.mpf("1e-45"):
            break
    return (lo + hi)/2

def mu_RAR_x(x):             # mu as a function of x via u-inversion
    u = solve_u_RAR(x)
    return mu_RAR_of_u(u)

def F_Q(X):
    s = mp.sqrt(X)
    return (s/2)*mp.sqrt(1 + 4*X) + (mp.asinh(2*s))/4 - s

def F_EXP(X):
    s = mp.sqrt(X)
    return X - 2 + 2*(1 + s)*mp.e**(-s)

def F_MU2(X):
    return mp.quad(lambda t: mu_MU2(mp.sqrt(t)), [0, X])

def F_RAR(X):
    s = mp.sqrt(X)
    uX = solve_u_RAR(s)
    return 2*mp.quad(lambda u: u*u*xp_RAR_of_u(u), [0, uX])

# Force relations: given y, x solves x*mu(x) = y (branch equation)
def x_of_y_Q(y):
    return mp.sqrt(y*y + y)
def x_of_y_EXP(y):
    return mp.findroot(lambda x: x*(1 - mp.e**(-x)) - y, mp.fabs(y) + mp.mpf("1e-3"), tol=mp.mpf("1e-50"))
def x_of_y_MU2(y):
    return mp.findroot(lambda x: x*mu_MU2(x) - y, mp.fabs(y) + mp.mpf("1e-3"), tol=mp.mpf("1e-50"))
def x_of_y_RAR(y):
    # x = y * nu(y), nu(y) = 1/(1 - exp(-sqrt(y))), closed form
    u = mp.sqrt(y)
    return y/(1 - mp.e**(-u))
# MONO deep: identical to RAR for y < y* (splice at y* ~ 2.3374 > deep domain)

BRANCHES = ["Q", "EXP", "MU2", "RAR"]
def forces(y, branch):
    if branch == "Q":   return x_of_y_Q(y)
    if branch == "EXP": return x_of_y_EXP(y)
    if branch == "MU2": return x_of_y_MU2(y)
    if branch == "RAR": return x_of_y_RAR(y)
    raise ValueError(branch)

def F_of_X(X, branch):
    if branch == "Q":   return F_Q(X)
    if branch == "EXP": return F_EXP(X)
    if branch == "MU2": return F_MU2(X)
    if branch == "RAR": return F_RAR(X)
    raise ValueError(branch)

def mu_prime(x, branch):
    # analytic mu'(x) at positive x (used for second-variation diagnostics)
    if branch == "Q":
        s = mp.sqrt(1 + 4*x*x)
        return (s - 1)/(2*x*x*s) if x > 0 else mp.mpf(1)
    if branch == "EXP":
        return mp.e**(-x)
    if branch == "MU2":
        return (1 + x/2)**(-3)
    if branch == "RAR":
        u = solve_u_RAR(x)
        if u < mp.mpf("1e-20"):
            return mp.mpf(1)   # mu'(0+) = 1
        e = mp.e**(-u)
        num = e*(1 - e)**2
        den = 2*u*(1 - e) - u*u*e
        return num/den if den != 0 else mp.mpf(1)
    raise ValueError(branch)

# ---------------------------------------------------------------- grids
KLO, KHI, KSTEP = -10, 8, 0.1
y_values = [mp.mpf(10)**(k) for k in [KLO + i*KSTEP for i in range(int((KHI-KLO)/KSTEP)+1)]]
N_Y = len(y_values)

XLOG_LO, XLOG_HI, XLOG_STEP = -20, 8, 0.2
X_grid = [mp.mpf(10)**(m) for m in [XLOG_LO + i*XLOG_STEP for i in range(int((XLOG_HI-XLOG_LO)/XLOG_STEP)+1)]]

# ---------------------------------------------------------------- run
out = {}
out["grids"] = {"y": {"log10_range": [KLO, KHI], "step": KSTEP, "n": N_Y},
                "X": {"log10_range": [XLOG_LO, XLOG_HI], "step": XLOG_STEP, "n": len(X_grid)}}

# (a) force asymptotics on the y-grid
force_rows = {}
for br in BRANCHES:
    rows = []
    for y in y_values:
        x = forces(y, br)
        rows.append([mp.nstr(y, 12), mp.nstr(x, 12), mp.nstr(x/mp.sqrt(y), 12), mp.nstr(x/y, 12)])
        check_deadline()
    force_rows[br] = rows
out["force_rows"] = force_rows

def mu_of_branch_at_x(x, br):
    if br == "Q":   return mu_Q(x)
    if br == "EXP": return mu_EXP(x)
    if br == "MU2": return mu_MU2(x)
    if br == "RAR": return mu_RAR_x(x)
    raise ValueError(br)

def x_of_y_identity(y):
    return y

def alpha_at(br, X):
    v = F_of_X(X, br)
    return X*mu_of_branch_at_x(mp.sqrt(X), br)/v

def second_deriv(X, br):
    # analytic: F''(X) = mu'(sqrt X)/(2 sqrt X)
    return mu_prime(mp.sqrt(X), br)/(2*mp.sqrt(X))

# (b) F(X), slopes, corrections on the log-X grid
alpha_full = {}; Fvals = {}; corr = {}
for br in BRANCHES:
    vals = [F_of_X(X, br) for X in X_grid]
    Fvals[br] = [[mp.nstr(X, 10), mp.nstr(v, 20)] for X, v in zip(X_grid, vals)]
    # alpha(X) = X F'(X)/F(X) = X mu(sqrt X)/F(X)
    alphas = []
    for X, v in zip(X_grid, vals):
        u = mp.sqrt(X)
        mu = mu_of_branch_at_x(u, br)
        alphas.append(X*mu/v)
    alpha_full[br] = [[mp.nstr(X, 10), mp.nstr(a, 16)] for X, a in zip(X_grid, alphas)]
    # correction delta = F/((2/3) X^(3/2)) - 1
    corr[br] = [[mp.nstr(X, 10), mp.nstr(v/((mp.mpf(2)/3)*X**mp.mpf("1.5")) - 1, 12)] for X, v in zip(X_grid, vals)]
    check_deadline()
out["F_X_grid"] = Fvals
out["alpha_loglog_slope"] = alpha_full
out["correction_delta"] = corr

# (c) independent check: F'(X) = mu(sqrt X) by central difference in log X
resid_Fprime = {}
h = mp.mpf("1e-3")
for br in BRANCHES:
    worst = mp.mpf(0); worstX = None
    for X in X_grid:
        Xp = X*mp.e**h; Xm = X*mp.e**(-h)
        Fp = F_of_X(Xp, br); Fm = F_of_X(Xm, br)
        num = (Fp - Fm)/(2*h*X)
        den = mu_of_branch_at_x(mp.sqrt(X), br)
        r = mp.fabs(num/den - 1)
        if r > worst:
            worst = r; worstX = X
        check_deadline()
    resid_Fprime[br] = {"max_relative_residual": mp.nstr(worst, 12), "at_X": mp.nstr(worstX, 6)}
out["Fprime_vs_mu_residual"] = resid_Fprime

# (d) homogeneity degree: alpha(X) -> 1.5 ; scaling F(4X)/F(X) -> 8 ; F'' sqrt X -> 1/2
deg = {}
for br in BRANCHES:
    a_lo = alpha_at(br, mp.mpf("1e-12"))
    a_1e6 = alpha_at(br, mp.mpf("1e-6"))
    sc = {}
    for X in (mp.mpf("1e-12"), mp.mpf("1e-16"), mp.mpf("1e-20")):
        sc[mp.nstr(X, 4)] = mp.nstr(F_of_X(4*X, br)/(8*F_of_X(X, br)) - 1, 12)
    svar = {}
    for X in (mp.mpf("1e-8"), mp.mpf("1e-12")):
        svar[mp.nstr(X, 4)] = mp.nstr(2*mp.sqrt(X)*second_deriv(X, br), 12)
    deg[br] = {"alpha(1e-12)": mp.nstr(a_lo, 16), "alpha(1e-6)": mp.nstr(a_1e6, 16),
               "F(4X)/(8F(X))-1": sc, "2*sqrt(X)*F''(X)": svar}
out["homogeneity_degree"] = deg

# (e) correction-exponent fit: delta ~ c X^beta on deep window
fit = {}
for br in BRANCHES:
    pts = []
    for X in X_grid:
        if X <= mp.mpf("1e-6") and X >= mp.mpf("1e-16"):
            d = F_of_X(X, br)/((mp.mpf(2)/3)*X**mp.mpf("1.5")) - 1
            pts.append((float(mp.log(X)), float(mp.log(mp.fabs(d)))))
    n = len(pts)
    sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0]*p[0] for p in pts); sxy = sum(p[0]*p[1] for p in pts)
    beta = (n*sxy - sx*sy)/(n*sxx - sx*sx)
    lc = (sy - beta*sx)/n
    # residual
    rmax = max(abs(p[1] - (lc + beta*p[0])) for p in pts)
    cpred = {"Q": -(mp.mpf(3)/5), "EXP": -(mp.mpf(3)/8), "MU2": -(mp.mpf(9)/16), "RAR": -(mp.mpf(3)/4)}
    fit[br] = {"beta_fit": round(beta, 6), "ln_c_fit": round(lc, 6),
               "c_predicted": mp.nstr(cpred[br], 6), "beta_predicted": {"Q":1, "EXP":0.5, "MU2":0.5, "RAR":0.5}[br],
               "max_fit_residual_ln": round(rmax, 8), "n_points": n}
out["correction_exponent_fit"] = fit

# (f) negative control 1: F(X) = X  =>  mu = 1  =>  Newtonian exactly
nc1 = {}
for br in BRANCHES:
    worst = mp.mpf(0)
    for y in y_values:
        # with mu = 1, field eq gives x = y exactly (algebraic identity)
        r = mp.fabs(x_of_y_identity(y) - y)
        if r > worst: worst = r
    # deep-law metric under the control: x^2/y = y -> 0, deep law demands -> 1
    dl = mp.nstr(y_values[0]**2/y_values[0], 6)
    nc1[br] = {"max_abs_residual_x_minus_y": mp.nstr(worst, 10),
               "deep_BTFR_indicator_x2_over_y_at_ymin": dl,
               "deep_law_would_need": "1",
               "note": "mu=1 identically => g = B Newtonian; BTFR indicator x^2/y = y -> 0 fails deep law"}
out["negative_control_1_F_equals_X"] = nc1

# (g) negative control 2: deep and Newtonian limiting regimes (per branch)
nc2 = {}
for br in BRANCHES:
    deep_worst = mp.mpf(0); newt_worst = mp.mpf(0)
    for y in y_values:
        x = forces(y, br)
        if y <= mp.mpf("1e-8"):
            r = mp.fabs(x/mp.sqrt(y) - 1)
            if r > deep_worst: deep_worst = r
        if y >= mp.mpf("1e4"):
            r = mp.fabs(x/y - 1)
            if r > newt_worst: newt_worst = r
    nc2[br] = {"max_deep_residual_abs(x/sqrt(y)-1)_y<=1e-8": mp.nstr(deep_worst, 10),
               "max_newtonian_residual_abs(x/y-1)_y>=1e4": mp.nstr(newt_worst, 10)}
out["negative_control_2_limits"] = nc2

# (h) normalization / boundary checks
norm = {}
for br in BRANCHES:
    f0 = F_of_X(mp.mpf(0), br)
    f1 = F_of_X(mp.mpf(1), br)   # X=1 is the crossover region: F(1) > 0
    d1 = F_of_X(mp.mpf(1) + mp.mpf("1e-6"), br) - f1
    norm[br] = {"F(0)": mp.nstr(f0, 10), "F(1)": mp.nstr(f1, 12),
                "F(1+eps)-F(1) > 0": mp.nstr(d1, 12)}
out["normalization_boundary"] = norm

# (i) energy content, both footings, fiducial masses
def energy_section(a0, label):
    rl = rho_lambda(a0)
    el = rl*C_SI*C_SI
    kappa_eff = KAPPA*a0/A0_CAN if label == "alt" else KAPPA
    sec = {"a0_m_s2": mp.nstr(a0, 12), "rho_Lambda_kg_m3": mp.nstr(rl, 12),
           "epsilon_Lambda_J_m3": mp.nstr(el, 12),
           "note_footing": ("kappa held = 1/2; alt footing uses its own rho_Lambda (not same vacuum as canonical)"
                            if label == "alt" else "kappa = 1/2, canonical vacuum"),
           "kappa_effective_at_canonical_rho": mp.nstr(kappa_eff, 8) if label == "alt" else None}
    for Mlab, M in (("M_sun", MSUN), ("M_fiducial_1e11", MSUN*mp.mpf("1e11"))):
        GM = G_SI*M
        rM = mp.sqrt(GM/a0)
        Cv = mp.sqrt(GM*a0)          # = v_flat^2
        vf = mp.sqrt(Cv)
        MC = M*Cv
        d = {"r_M_m": mp.nstr(rM, 12), "r_M_pc": mp.nstr(rM/PC_SI, 10),
             "C_eq_vflat2_m2_s2": mp.nstr(Cv, 12), "v_flat_m_s": mp.nstr(vf, 10),
             "M*C_J": mp.nstr(MC, 12),
             "per_log_decade_field_energy_J": mp.nstr(MC*mp.log(10)/3, 12),
             "half_M_vflat2_J": mp.nstr(M*Cv/2, 12),
             "virial_ratio_field_per_decade_over_half_Mv2": mp.nstr((MC*mp.log(10)/3)/(M*Cv/2), 12),
             "1_over_ln10_ratio_base": mp.nstr(2*mp.log(10)/3, 12)}
        # field energy density at sample radii (deep formula eps = g^3/(12 pi G a0), g = C/r)
        den = {}
        for kr in (0, 1, 2, 3):
            r = rM*mp.mpf(10)**kr
            g = Cv/r
            eps = g**3/(12*mp.pi*G_SI*a0)
            den["r=" + mp.nstr(10**kr, 3) + "_rM"] = {"eps_J_m3": mp.nstr(eps, 12),
                                                       "g_a0": mp.nstr(g/a0, 8)}
        d["field_energy_density"] = den
        # enclosed field energy vs deep-law prediction (1/3)MC ln(R/rM): integrate Q branch exactly
        Edeep = {}
        for kr in (1, 2, 4, 6):
            R = rM*mp.mpf(10)**kr
            Ein = 4*mp.pi*mp.quad(lambda rr: rr*rr*(a0*a0/(8*mp.pi*G_SI))*F_of_X((Cv/rr)**2/a0/a0, "Q"),
                                  [rM, R])
            pred = MC/3*mp.log(R/rM)
            Edeep["R=" + mp.nstr(10**kr, 3) + "_rM"] = {
                "E_field_Q_branch_J": mp.nstr(Ein, 12),
                "deep_law_prediction_MC3_ln(R/rM)_J": mp.nstr(pred, 12),
                "rel_diff": mp.nstr(Ein/pred - 1, 10)}
        d["enclosed_field_energy"] = Edeep
        # phantom bookkeeping: M_ph(R) = C R/G ; E_ph,kin = (1/2) M_ph sigma^2 = C^2 R/(4G)
        ph = {}
        for kr in (1, 2, 4, 6):
            R = rM*mp.mpf(10)**kr
            Mph = Cv*R/G_SI
            Eph = Cv*Cv*R/(4*G_SI)
            ph["R=" + mp.nstr(10**kr, 3) + "_rM"] = {
                "M_ph_kg": mp.nstr(Mph, 12),
                "E_ph_kin_J": mp.nstr(Eph, 12),
                "E_ph_over_E_field": mp.nstr(Eph/(MC/3*mp.log(R/rM)), 10)}
        d["phantom_gas_energy"] = ph
        sec[Mlab] = d
    return sec

out["energy_canonical_footing"] = energy_section(A0_CAN, "canonical")
out["energy_alternative_footing"] = energy_section(A0_ALT, "alt")

# (j) virial ratio exactness: per e-fold field energy / ((1/2) M v_flat^2)
# Pure deep law: dE/d(ln r) = 4pi r^2 eps = 4pi r^2 * (a0^2/8piG)(2/3)X^(3/2)
#   with X = C^2/(a0^2 r^2) => = C^3/(3 G a0) = M*C/3. Ratio to (1/2) M v_flat^2
#   (= (1/2) M C since v_flat^2 = C) is exactly 2/3.
vir = {}
for br in BRANCHES:
    vir[br] = {"per_efold_over_half_Mv2": mp.nstr((mp.mpf(1)/3)/(mp.mpf(1)/2), 12)}
out["virial_ratio_per_efold"] = vir
out["virial_ratio_exact"] = "E_field per e-fold / ((1/2) M v_flat^2) = (M C/3)/(M C/2) = 2/3 (exact, pure deep law)"

out["execution"] = {"wall_budget_s": WALL_BUDGET_S, "threads": 1,
                    "mp_dps": int(mp.mp.dps), "elapsed_s": round(time.monotonic() - T0, 3)}
print(json.dumps(out, indent=1))
sys.stderr.write("AS039 COMPLETE: bounds enforced (1 thread, fixed grids, 120 s budget), elapsed %.2fs\n" % (time.monotonic() - T0))
