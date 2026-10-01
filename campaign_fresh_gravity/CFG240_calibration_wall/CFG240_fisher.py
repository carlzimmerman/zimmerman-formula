#!/usr/bin/env python3
"""CFG240 numeric companion: the baryon-calibration wall as a Fisher-information statement.

Law (declared): g_obs = (f g) nu((f g)/a0), one multiplicative calibration f > 0 on g_bar, the same f and a0 at every point.
Parameters theta = (log10 f, log10 a0); data d_i = log10 g_obs(g_i), independent Gaussian errors sigma dex.
y := f0 g/a0 at the TRUE (f0, a0) (the argument fed to nu).  The Fisher matrix depends on the sample only through y_i:
    d log g_obs / d log f = 1 - b(y),  d log g_obs / d log a0 = b(y)
    P2:      b = 1/(2(1+y));   nu_mono: b = s/(2 (e^s - 1)), s = sqrt(y).
Lean (ChainCert/CalibrationWall.lean) certifies the algebra; this script is the numeric table.  No empirical fact here.

Usage:  python3 CFG240_fisher.py                 main run, exit 0 iff every pass line holds
        MUTATE=k python3 CFG240_fisher.py        control k in 1..6; exit 1 iff the pass lines catch the mutation
"""
import json, math, os, re, sys
from pathlib import Path
import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
MUT = int(os.environ.get("MUTATE", "0"))
TAG = "" if MUT == 0 else f"_MUTATE{MUT}"
LN10 = math.log(10.0)

# ---------------------------------------------------------------- kernels, closed forms
def nu(kernel, y):
    y = np.asarray(y, dtype=float)
    if kernel == "P2":
        return np.sqrt(1.0 + 1.0 / y)
    if kernel == "nu_mono":
        return 1.0 / (-np.expm1(-np.sqrt(y)))
    raise ValueError(kernel)

def gobs(kernel, f, a0, g):
    x = f * np.asarray(g, dtype=float)
    return x * nu(kernel, x / a0)

def b_closed(kernel, y):
    """b(y) = d log g_obs / d log a0 = 1 - d log g_obs / d log f (closed form)."""
    y = np.asarray(y, dtype=float)
    if kernel == "P2":
        if MUT == 1:                       # MUTATE 1: wrong kernel (the deep value) in the analytic rows
            return np.full_like(y, 0.5)
        return 0.5 / (1.0 + y)
    s = np.sqrt(y)
    return 0.5 * s / np.expm1(s)

def fisher_entries(kernel, y, sigma):
    b = b_closed(kernel, y); A = 1.0 - b
    s2 = 1.0 if MUT == 2 else sigma ** 2   # MUTATE 2: sigma^2 dropped from F
    return np.array([[np.sum(A * A), np.sum(A * b)], [np.sum(A * b), np.sum(b * b)]]) / s2

def design(ymin, ymax, N):
    i = np.arange(N)
    return ymin * (ymax / ymin) ** (i / (N - 1))

def stats(kernel, y, sigma, tau=None):
    """sigma-scaled closed-form statistics of the sample (stable D formula)."""
    b = b_closed(kernel, y); A = 1.0 - b; N = len(y)
    SA, SB, SAB = float(np.sum(A * A)), float(np.sum(b * b)), float(np.sum(A * b))
    D = N * float(np.sum((b - b.mean()) ** 2))          # = (1/2) sum_ij (b_i - b_j)^2
    s2 = 1.0 if MUT == 2 else sigma ** 2             # MUTATE 2: F built without the 1/sigma^2
    p = 0.0 if tau is None else s2 / tau ** 2           # prior strength in units of sigma^2
    var_a0 = s2 * (SA + p) / (D + p * SB) if (D + p * SB) > 0 else float("inf")
    var_f = s2 * SB / (D + p * SB) if (D + p * SB) > 0 else float("inf")
    F11, F12, F22 = (SA + p) / s2, SAB / s2, SB / s2
    sig_cond = 1.0 / math.sqrt(F22) if F22 > 0 else float("inf")
    sgn = -1.0 if MUT == 4 else 1.0                     # MUTATE 4: sign of the F12 term in rho
    rho = sgn * (-F12 / math.sqrt(F11 * F22)) if F11 * F22 > 0 else float("nan")
    det = (D + p * SB) / s2 ** 2
    tr = F11 + F22
    lmax = 0.5 * (tr + math.sqrt(max(tr * tr - 4 * det, 0.0)))
    lmin = det / lmax if lmax > 0 else float("nan")
    cond = lmax / lmin if lmin > 0 else float("inf")
    cond_norm = (1 + abs(rho)) / (1 - abs(rho)) if abs(rho) < 1 else float("inf")
    return dict(sigma_marg=math.sqrt(var_a0), sigma_cond=sig_cond, sigma_f_marg=math.sqrt(var_f),
                rho=rho, cond=cond, cond_norm=cond_norm, detF=det, D=D, F=[[F11, F12], [F12, F22]])

# ---------------------------------------------------------------- reporting helpers
lines_out = []
def out(*a):
    s = " ".join(str(x) for x in a); print(s); lines_out.append(s)

PASS = {}
# the pass lines each control is designed to break (the control "bites" iff ALL of these fail)
EXPECT = {1: ["PL1", "PL2"], 2: ["PL1", "PL7"], 3: ["PL1"], 4: ["PL4"], 5: ["PL9"], 6: ["PL5"]}
def check(name, ok, detail=""):
    PASS[name] = bool(ok)
    out(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")

def fmt_y(v):  return "none" if v is None else f"{v:.3g}"

# ---------------------------------------------------------------- PL1: analytic vs finite-difference Fisher
def fd_fisher(kernel, f0, a0, g, sigma, h=1e-3):
    """Fisher from a 4-point central stencil on log10 g_obs(theta), theta = (log10 f, log10 a0)."""
    def d(idx):
        def val(dx):
            th = np.array([math.log10(f0), math.log10(a0)]); th[idx] += dx
            return np.log10(gobs(kernel, 10 ** th[0], 10 ** th[1], g))
        return (-val(2 * h) + 8 * val(h) - 8 * val(-h) + val(-2 * h)) / (12 * h)
    J = np.stack([d(0), d(1)], axis=1)
    return J.T @ J / sigma ** 2, J

def pl1():
    worst = 0.0
    designs = [(1e-3, 1.0, 12), (1e-3, 30.0, 20), (1e-2, 10.0, 20), (1e-2, 30.0, 50), (1e-1, 30.0, 20), (1e-2, 1.0, 5),
               (3e-3, 3.0, 7), (1e-1, 10.0, 100), (1e-3, 3e-2, 10), (5e-2, 30.0, 33), (1.0, 30.0, 9), (1e-2, 0.5, 15)]
    for kernel in ("P2", "nu_mono"):
        for f0 in (0.5, 1.0, 1.7):
            for a0 in (1.0, 0.3):
                for (ymin, ymax, N) in designs:
                    y = design(ymin, ymax, N); g = y * a0 / f0
                    Ffd, J = fd_fisher(kernel, f0, a0, g, 0.1)
                    y_arg = g / a0 if (MUT == 3 and f0 != 1.0) else y   # MUTATE 3: y_nom = g/a0 used as the true y
                    Fa = fisher_entries(kernel, y_arg, 0.1)
                    scale = max(np.max(np.abs(Fa)), 1e-300)
                    for i in range(2):
                        for j in range(2):
                            den = max(abs(Fa[i, j]), 1e-6 * scale)     # floor only for entries < 1e-6 of the largest
                            worst = max(worst, abs(Ffd[i, j] - Fa[i, j]) / den)
    check("PL1 analytic Fisher == finite-difference Fisher of gObs (rel <= 1e-8)", worst <= 1e-8, f"worst rel {worst:.2e}")
    return worst

# ---------------------------------------------------------------- PL2: closed form == sympy
def pl2():
    s, t, g, N_ = sp.symbols("s t g N", positive=True)
    f, a0 = sp.exp(s), sp.exp(t)
    y_sym = f * g / a0
    sym_kernels = {"P2": lambda y: sp.sqrt(1 + 1 / y), "nu_mono": lambda y: 1 / (1 - sp.exp(-sp.sqrt(y)))}
    worst = 0.0
    sym_dump = {}
    for kernel, nuf in sym_kernels.items():
        ell = sp.log(f * g * nuf(f * g / a0))              # log g_obs from the DEFINITION
        ds, dt = sp.diff(ell, s), sp.diff(ell, t)
        sym_dump[kernel] = dict(dlogf=str(sp.simplify(ds)) if kernel == "P2" else "(numeric check only)",
                                dloga=str(sp.simplify(dt)) if kernel == "P2" else "(numeric check only)")
        for yv in np.logspace(-4, 2, 20):
            sv, tv = 0.37, -0.21
            gv = yv * math.exp(tv - sv)
            vs = float(ds.subs({s: sv, t: tv, g: gv}).evalf(30)); vt = float(dt.subs({s: sv, t: tv, g: gv}).evalf(30))
            bb = float(b_closed(kernel, np.array([yv]))[0])
            worst = max(worst, abs(vt - bb) / bb, abs(vs - (1 - bb)) / (1 - bb))
    # symbolic identities: det = b2 - b1 and the covariance formulas for N = 3 points, generic b
    b1, b2, b3, sg, tau = sp.symbols("b1 b2 b3 sigma tau", positive=True)
    bs = [b1, b2, b3]
    Fm = sp.Matrix([[sum((1 - b) ** 2 for b in bs), sum((1 - b) * b for b in bs)], [sum((1 - b) * b for b in bs), sum(b ** 2 for b in bs)]]) / sg ** 2
    D = sp.Rational(1, 2) * sum((bi - bj) ** 2 for bi in bs for bj in bs)
    C = Fm.inv()
    r_var_a0 = sp.simplify(C[1, 1] - sg ** 2 * sum((1 - b) ** 2 for b in bs) / D)
    r_var_f = sp.simplify(C[0, 0] - sg ** 2 * sum(b ** 2 for b in bs) / D)
    r_cov = sp.simplify(C[0, 1] + sg ** 2 * sum((1 - b) * b for b in bs) / D)
    Fp = Fm + sp.Matrix([[1 / tau ** 2, 0], [0, 0]])
    p = sg ** 2 / tau ** 2
    r_prior = sp.simplify(Fp.inv()[1, 1] - sg ** 2 * (sum((1 - b) ** 2 for b in bs) + p) / (D + p * sum(b ** 2 for b in bs)))
    r_det = sp.simplify((1 - b1) * b2 - b1 * (1 - b2) - (b2 - b1))
    r_p2 = sp.simplify(((1 + 2 * sp.Symbol("y1", positive=True)) / (2 * (1 + sp.Symbol("y1", positive=True)))) * (1 / (2 * (1 + sp.Symbol("y2", positive=True))))
                       - (1 / (2 * (1 + sp.Symbol("y1", positive=True)))) * ((1 + 2 * sp.Symbol("y2", positive=True)) / (2 * (1 + sp.Symbol("y2", positive=True))))
                       - (sp.Symbol("y1", positive=True) - sp.Symbol("y2", positive=True)) / (2 * (1 + sp.Symbol("y1", positive=True)) * (1 + sp.Symbol("y2", positive=True))))
    resid = [r_var_a0, r_var_f, r_cov, r_prior, r_det, r_p2]
    symok = all(r == 0 for r in resid)
    check("PL2 closed form == sympy (derivatives at 20 y per kernel <= 1e-12; covariance/prior/det identities symbolic = 0)",
          worst <= 1e-12 and symok, f"worst rel {worst:.2e}; symbolic residuals {[str(r) for r in resid]}")
    out("   sympy P2 d(log g_obs)/d(log f) =", sym_dump["P2"]["dlogf"], "; d/d(log a0) =", sym_dump["P2"]["dloga"])
    return worst

# ---------------------------------------------------------------- PL3: T1 numeric
def pl3():
    out("-- T1: deep-limit factorisation through f*a0")
    gs = np.logspace(-8, 2, 30)
    worst_deep = 0.0
    nudeep = lambda f, a0, g: (f * g) * (1.0 / np.sqrt(f * g / a0))
    for (f, a0) in [(2.0, 0.5), (0.25, 4.0), (1.0, 1.0)]:
        r = nudeep(f, a0, gs) / nudeep(1.0, 1.0, gs)
        worst_deep = max(worst_deep, float(np.max(np.abs(r - 1))))
    # P2 equal-product relative difference of g_obs^2 = (rho^2 - 1) y/(1 + y)
    # the relative difference of g_obs^2 is ~ y at small y, so double precision loses ~ 1e-16/y; evaluate with mpmath (50 digits)
    import mpmath as mp
    mp.mp.dps = 50
    def g2_mp(kf, ka, gv):
        x = kf * gv; return (x * mp.sqrt(1 + 1 / (x / ka))) ** 2
    f, a0, rho = 1.0, 1.0, 2.0
    ys = np.logspace(-6, 3, 40); g = ys * a0 / f
    rel = np.array([float((g2_mp(rho * f, a0 / rho, mp.mpf(float(gv))) - g2_mp(f, a0, mp.mpf(float(gv)))) / g2_mp(f, a0, mp.mpf(float(gv)))) for gv in g])
    ref = (rho ** 2 - 1) * ys / (1 + ys)
    err = float(np.max(np.abs(rel - ref) / np.abs(ref)))
    ysm = np.logspace(-6, -3, 13); gm = ysm * a0 / f
    relm = np.array([abs(float((g2_mp(rho * f, a0 / rho, mp.mpf(float(gv))) - g2_mp(f, a0, mp.mpf(float(gv)))) / g2_mp(f, a0, mp.mpf(float(gv))))) for gv in gm])
    slope = np.polyfit(np.log10(ysm), np.log10(relm), 1)[0]
    bound_ok = bool(np.all(np.abs(rel) <= abs(1 - rho ** 2) * ys * (1 + 1e-12)))
    # nu_mono: equal-product relative difference of g_obs decays as y -> 0 (T1e)
    def relmono(y):
        gg = np.array([y]); return abs(float((gobs("nu_mono", rho * f, a0 / rho, gg) / gobs("nu_mono", f, a0, gg) - 1)[0]))
    ratio_mono = relmono(1e-6) / relmono(1e-2)
    check("PL3a deep kernel: g_obs equal for equal products (rel <= 1e-14)", worst_deep <= 1e-14, f"worst {worst_deep:.2e}")
    check("PL3b P2: (g'^2-g^2)/g^2 = (rho^2-1) y/(1+y) (mpmath 50 digits, rel <= 1e-12), bound |1-rho^2| y holds", err <= 1e-12 and bound_ok, f"max rel err {err:.2e}")
    check("PL3c P2: relative difference is linear in y as y -> 0 (log-log slope 1 +- 0.01)", abs(slope - 1) <= 0.01, f"slope {slope:.4f}")
    check("PL3d nu_mono: equal-product g_obs ratio -> 1 (value at y=1e-6 < 0.05 x value at y=1e-2)", ratio_mono < 0.05, f"ratio {ratio_mono:.3e} (expected ~1e-2: O(sqrt y))")
    return dict(deep_worst=worst_deep, p2_err=float(err), slope=float(slope), mono_ratio=float(ratio_mono))

# ---------------------------------------------------------------- PL4 / PL5 / PL6 / PL7 / PL8
def pl4(table_cells):
    neg = all(c["rho"] < 0 for c in table_cells)
    singular = []
    for k in ("P2", "nu_mono"):
        for y0 in (1e-3, 1.0, 100.0):
            st = stats(k, np.full(10, y0), 0.1)
            singular.append(st["rho"])
    sing_ok = all(abs(r + 1) <= 1e-12 for r in singular) if MUT != 4 else all(abs(r + 1) <= 1e-12 for r in singular)
    corner = []
    for k in ("P2", "nu_mono"):
        y = design(1e-3, 1.0001e-3, 20); corner.append(stats(k, y, 0.1)["rho"])
    corner_ok = all(r < -0.999 for r in corner)
    check("PL4 rho < 0 in EVERY grid cell; single-y design rho = -1 (1e-12); deep corner rho < -0.999", neg and sing_ok and corner_ok,
          f"all negative: {neg}; single-y rho {[round(r,12) for r in singular]}; corner rho {[round(r,6) for r in corner]}")

def pl5():
    rng = np.random.default_rng(240)
    const = 3.1 if MUT == 6 else 3.0                     # MUTATE 6: floor constant 3 -> 3.1
    worst = 1e9; nfail = 0; tried = 0
    for trial in range(20000):
        N = int(rng.integers(2, 201)); sigma = float(10 ** rng.uniform(-2, 0))
        if trial % 2 == 0:
            b = rng.uniform(0.0, 0.5, N)
        else:
            kern = "P2" if (trial // 2) % 2 == 0 else "nu_mono"
            ylo = 10 ** rng.uniform(-4, 1); y = ylo * 10 ** rng.uniform(0, 4) * rng.uniform(0.5, 1.0, N)
            b = b_closed(kern, y)
        A = 1.0 - b; SA = float(np.sum(A * A)); D = N * float(np.sum((b - b.mean()) ** 2))
        if D <= 1e-14: continue
        tried += 1
        sig = sigma * math.sqrt(SA / D)
        ratio = sig / (const * sigma / math.sqrt(N))
        worst = min(worst, ratio)
        if ratio < 1 - 1e-12: nfail += 1
    # equality design: 2m points at b = 1/2 (deep), m at b = 0 (Newtonian)
    eq_err = 0.0
    for m in range(1, 41):
        N = 3 * m; b = np.array([0.5] * (2 * m) + [0.0] * m); A = 1 - b
        D = N * float(np.sum((b - b.mean()) ** 2)); sig = 0.1 * math.sqrt(float(np.sum(A * A)) / D)
        eq_err = max(eq_err, abs(sig / (3.0 * 0.1 / math.sqrt(N)) - 1))
        eq_err = max(eq_err, abs(sig / (const * 0.1 / math.sqrt(N)) - 1) if MUT == 6 else 0.0)
    ok = (nfail == 0) and (eq_err <= 1e-12)
    check("PL5 design bound sigma(log a0) >= 3 sigma/sqrt(N): 0 violations in random designs; equality at the 2/3-deep two-cluster design (1e-12)",
          ok, f"designs {tried}, violations {nfail}, min ratio sigma_a0/(c sigma/sqrtN) = {worst:.6f}, equality-design err {eq_err:.2e}")
    return dict(designs=tried, violations=nfail, min_ratio=float(worst), eq_err=float(eq_err))

def pl6():
    yy = np.logspace(-4, 3, 200)
    worst = 0.0; worst_p2 = 0.0; mx = 0.0
    for k in ("P2", "nu_mono"):
        b = b_closed(k, yy); A = 1 - b
        det = A[:, None] * b[None, :] - b[:, None] * A[None, :]           # rows (A_i, b_i): det = A_i b_j - b_i A_j
        ref = b[None, :] - b[:, None]
        worst = max(worst, float(np.max(np.abs(det - ref))))
        mx = max(mx, float(np.max(np.abs(det))))
        if k == "P2":
            y1, y2 = yy[:, None], yy[None, :]
            worst_p2 = float(np.max(np.abs(det - (y1 - y2) / (2 * (1 + y1) * (1 + y2)))))
    # finite-difference Jacobian determinant at a few points
    fd_ok = True
    for k in ("P2", "nu_mono"):
        for (y1, y2) in [(0.01, 3.0), (0.5, 0.7), (10.0, 0.1)]:
            _, J = fd_fisher(k, 1.0, 1.0, np.array([y1, y2]), 0.1)
            det_fd = J[0, 0] * J[1, 1] - J[0, 1] * J[1, 0]
            det_cl = float(b_closed(k, np.array([y2]))[0] - b_closed(k, np.array([y1]))[0])
            if abs(det_fd - det_cl) > 1e-9: fd_ok = False
    check("PL6 two-point Jacobian det = b(y2)-b(y1) (1e-14), |det| < 1/2 on 200x200 y grid, P2 closed form (y1-y2)/(2(1+y1)(1+y2)), FD det (1e-9)",
          worst <= 1e-14 and worst_p2 <= 1e-14 and mx < 0.5 and fd_ok, f"worst {worst:.1e}, P2 closed form {worst_p2:.1e}, max|det| {mx:.4f}, fd_ok {fd_ok}")

def pl7():
    y = design(1e-2, 30.0, 20)
    ok = True; det = []
    for k in ("P2", "nu_mono"):
        s1 = stats(k, y, 0.1)["sigma_marg"]; s2 = stats(k, y, 0.2)["sigma_marg"]
        yr = np.repeat(y, 4); sk = stats(k, yr, 0.1)["sigma_marg"]
        e1 = abs(s2 / s1 - 2); e2 = abs(sk / s1 - 0.5)
        det.append((k, e1, e2)); ok = ok and e1 <= 1e-12 and e2 <= 1e-12
    check("PL7 sigma_marg exactly linear in sigma; k-fold replicated design scales as 1/sqrt(k) (1e-12)", ok, f"{det}")

def pl8():
    u = np.linspace(-20, 3.5, 4000); y = np.exp(u)
    eta = {k: 1 - b_closed(k, y) for k in ("P2", "nu_mono")}
    mono = all(bool(np.all(np.diff(v) > 0)) for v in eta.values()) and eta["nu_mono"][0] > 0.5 and eta["nu_mono"][-1] < 1
    bP2 = float(b_closed("P2", np.array([1e4]))[0]); bM = float(b_closed("nu_mono", np.array([1e4]))[0])
    # T3 numeric: g_obs/g -> f and a0 drops out
    t3 = True
    for k in ("P2", "nu_mono"):
        f0 = 1.7; g = np.array([1e4])
        t3 = t3 and abs(float(gobs(k, f0, 1.0, g)[0] / g[0]) - f0) < 1e-3 * f0
        r = float(gobs(k, f0, 1.0, g)[0] / gobs(k, f0, 3.0, g)[0]); t3 = t3 and abs(r - 1) < 1e-3
    check("PL8 eta = 1-b strictly increasing (grid, not a proof) with eta(-20)>1/2, eta(3.5)<1; b(1e4): P2 = 5e-5, nu_mono < 1e-30; T3 numeric limits",
          mono and abs(bP2 - 1 / (2 * 10001)) < 1e-12 and bM < 1e-30 and t3, f"b(1e4) P2 {bP2:.3e}, nu_mono {bM:.1e}, T3 {t3}")

# ---------------------------------------------------------------- the table
KERNELS = ("P2", "nu_mono"); YMINS = (1e-3, 1e-2, 1e-1); NS = (5, 10, 20, 50, 100); SIGMAS = (0.05, 0.1, 0.2); TAUS = (None, 0.15, 0.3)
YMAX_CAP = 1e4; STEP = 50  # y_max grid: y_min * 10^(k/50), up to the cap

def ymax_grid(ymin):
    K = int(math.floor(STEP * math.log10(YMAX_CAP / ymin) + 1e-9))
    return np.array([ymin * 10 ** (k / STEP) for k in range(1, K + 1)])

def cell(kernel, ymin, N, sigma, tau, target):
    yg = ymax_grid(ymin)
    sig = []; sts = []
    for ym in yg:
        st = stats(kernel, design(ymin, ym, N), sigma, tau); sts.append(st)
        sig.append(st["sigma_cond"] if MUT == 5 else st["sigma_marg"])   # MUTATE 5: conditional instead of marginal sigma
    sig = np.array(sig); below = sig < target
    first = int(np.argmax(below)) if below.any() else None
    stable = None
    if below.any():
        j = len(below)
        while j > 0 and below[j - 1]: j -= 1
        stable = j if j < len(below) else None
    imin = int(np.argmin(sig))
    def at(i):
        if i is None: return None
        st = sts[i]
        return dict(y_max=float(yg[i]), rho=float(st["rho"]), sigma_log_a0=float(st["sigma_marg"]), cond=float(st["cond"]), cond_normalised=float(st["cond_norm"]))
    return dict(kernel=kernel, y_min=ymin, N=N, sigma_dex=sigma, prior_log_f_dex=tau, target_dex=target,
                y_max_first=None if first is None else float(yg[first]), y_max_stable=None if stable is None else float(yg[stable]),
                at_stable=at(stable), at_first=at(first),
                sigma_min=float(sig[imin]), y_max_argmin=float(yg[imin]), floor_3sigma_over_sqrtN=3 * sigma / math.sqrt(N),
                monotone=bool(np.all(np.diff(sig) <= 1e-15)))

def table_markdown(cells01):
    idx = {(c["kernel"], c["y_min"], c["N"], c["sigma_dex"], c["prior_log_f_dex"]): c for c in cells01}
    def yv(c): return "none" if c["y_max_stable"] is None else f"{c['y_max_stable']:.3g}"
    rows = ["| kernel | y_min | N | sigma (dex) | y_max* (no prior) | rho | sigma(log a0) | cond(F) | y_max* (tau=0.15) | y_max* (tau=0.3) |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for k in KERNELS:
        for ymin in YMINS:
            for N in NS:
                for sg in SIGMAS:
                    c0 = idx[(k, ymin, N, sg, None)]; c1 = idx[(k, ymin, N, sg, 0.15)]; c2 = idx[(k, ymin, N, sg, 0.3)]
                    a = c0["at_stable"]
                    mid = f"{a['rho']:.3f} | {a['sigma_log_a0']:.4f} | {a['cond']:.3g}" if a else "- | - | -"
                    rows.append(f"| {k} | {ymin:g} | {N} | {sg:g} | {yv(c0)} | {mid} | {yv(c1)} | {yv(c2)} |")
    return "\n".join(rows)

def finish(code):
    (HERE / f"CFG240_fisher{TAG}.out").write_text("\n".join(lines_out) + "\n")
    sys.exit(code)

def main():
    out("CFG240 Fisher companion", "MUTATE=%d" % MUT if MUT else "main run")
    out("law: g_obs=(f g) nu((f g)/a0); theta=(log10 f, log10 a0); y=f0 g/a0 at the TRUE f0 (argument of nu); closed form rows (1-b, b)")
    w1 = pl1(); w2 = pl2(); t1 = pl3()
    # the table
    cells01 = []; cells02 = []
    for k in KERNELS:
        for ymin in YMINS:
            for N in NS:
                for sg in SIGMAS:
                    for tau in TAUS:
                        cells01.append(cell(k, ymin, N, sg, tau, 0.1)); cells02.append(cell(k, ymin, N, sg, tau, 0.2))
    allrho = []
    for c in cells01:
        for key in ("at_stable", "at_first"):
            if c[key]: allrho.append(c[key])
    # rho over EVERY cell of the grid (not just at break-even): recompute across y_max grid at no prior and prior
    rho_cells = []
    for k in KERNELS:
        for ymin in YMINS:
            for N in NS:
                for tau in TAUS:
                    for ym in ymax_grid(ymin)[::7]:
                        rho_cells.append(dict(rho=stats(k, design(ymin, ym, N), 0.1, tau)["rho"]))
    pl4(rho_cells)
    t5 = pl5(); pl6(); pl7(); pl8()
    # PL9 break-even logic
    ok9 = True; msgs = []
    idx = {(c["kernel"], c["y_min"], c["N"], c["sigma_dex"], c["prior_log_f_dex"]): c for c in cells01}
    for c in cells01:
        if c["y_max_first"] is not None and c["y_max_stable"] is not None and c["y_max_first"] > c["y_max_stable"] * (1 + 1e-12): ok9 = False
        if c["y_max_first"] is not None:
            if not (c["at_first"]["sigma_log_a0"] < 0.1 or MUT == 5): ok9 = False
        # floor consistency: a break-even can only exist if the T4 floor is < target
        if (c["y_max_first"] is not None) and not (c["floor_3sigma_over_sqrtN"] < 0.1 * (1 + 1e-12)): ok9 = False
    for k in KERNELS:
        for ymin in YMINS:
            for tau in (None,):
                for (N, sg) in ((5, 0.1), (20, 0.2)):
                    c = idx[(k, ymin, N, sg, tau)]
                    if c["y_max_first"] is not None: ok9 = False; msgs.append(f"{k} ymin={ymin} N={N} sigma={sg} reached target below the T4 floor")
    check("PL9 break-even logic: first <= stable; sigma<target at first; never below the T4 floor (N=5,sigma=0.1 and N=20,sigma=0.2 return none)", ok9, "; ".join(msgs))
    # PL10: JSON table == README table
    md = table_markdown(cells01)
    readme = HERE / "README.md"
    ok10 = False
    if readme.exists():
        txt = readme.read_text()
        m = re.search(r"<!-- TABLE-BEGIN -->\n(.*?)\n<!-- TABLE-END -->", txt, re.S)
        ok10 = bool(m) and m.group(1).strip() == md.strip()
    check("PL10 README break-even table agrees with the JSON-derived table", ok10, "" if ok10 else "(README block missing or different; the generated table is in CFG240_break_even_table.md)")
    # records
    allpass = all(PASS.values())
    results = dict(lane="CFG240", mutate=MUT, pass_lines=PASS, all_pass=allpass, fd_worst_rel=w1, sympy_worst_rel=w2, t1=t1, design_bound=t5)
    if MUT == 0:
        header = dict(record="header",
            definitions=dict(
                y="y = f g_bar / a0 at the TRUE (f, a0): the argument fed to nu; y_nom = g_bar/a0 = y/f.",
                law="g_obs = (f g) nu((f g)/a0), one multiplicative calibration f on g_bar, same f and a0 at every point",
                kernels="P2: nu = sqrt(1+1/y), b = 1/(2(1+y)); nu_mono: nu = 1/(1-exp(-sqrt y)), b = s/(2(e^s-1)), s = sqrt(y)",
                design="N points, y_i = y_min (y_max/y_min)^((i-1)/(N-1)) (log-uniform, endpoints included)",
                y_max_cap=YMAX_CAP, y_max_grid="y_min * 10^(k/50), k = 1.. up to the cap",
                y_max_break_even="smallest grid y_max such that sigma(log a0) < 0.1 dex for ALL larger grid y_max up to the cap (null = never within the cap); y_max_first = smallest grid y_max with sigma < 0.1",
                sigma_log_a0="marginal sigma of log10 a0 = sqrt((F^-1)_22), f free (with the Gaussian prior on log10 f when prior_log_f_dex is not null)",
                rho="correlation of the estimates of (log10 f, log10 a0) = -F12/sqrt(F11 F22); NEGATIVE in every cell (both parameters raise g_obs, degenerate direction f*a0 fixed)",
                cond="ratio of the eigenvalues of F (raw); cond_normalised = (1+|rho|)/(1-|rho|)",
                at_break_even="rho, sigma(log a0) and cond are evaluated at y_max_break_even (the stable one); at_first is the same at y_max_first"),
            ladder=dict(T4_floor="sigma(log a0) >= 3 sigma/sqrt(N) for any sample (f free)"))
        recs = []
        for c in cells01:
            at = c["at_stable"]
            recs.append(dict(record="case", kernel=c["kernel"], y_min=c["y_min"], N=c["N"], sigma_dex=c["sigma_dex"],
                             prior_log_f_dex=c["prior_log_f_dex"], target_dex=0.1,
                             y_max_break_even=c["y_max_stable"], y_max_first=c["y_max_first"],
                             rho_at_break_even=None if at is None else at["rho"],
                             sigma_log_a0_at_break_even=None if at is None else at["sigma_log_a0"],
                             cond_at_break_even=None if at is None else at["cond"],
                             at_first=c["at_first"], sigma_min=c["sigma_min"], y_max_argmin=c["y_max_argmin"],
                             floor_3sigma_over_sqrtN=c["floor_3sigma_over_sqrtN"]))
        (HERE / "CFG240_break_even_table.json").write_text(json.dumps([header] + recs, indent=1, sort_keys=True) + "\n")
        (HERE / "CFG240_break_even_table.md").write_text(md + "\n")
        results["cells_target_0.1"] = cells01; results["cells_target_0.2"] = cells02
    else:
        # mutation: record only a small sample of cells
        results["cells_sample"] = cells01[:6]
    (HERE / f"CFG240_fisher{TAG}_results.json").write_text(json.dumps(results, indent=1, sort_keys=True, default=float) + "\n")
    if MUT == 0:
        out("ALL PASS" if allpass else "SOME FAILED"); finish(0 if allpass else 1)
    else:
        failed = [k.split()[0] for k, v in PASS.items() if not v]
        bites = all(e in failed for e in EXPECT[MUT])
        if not bites:
            out(f"MUTATE {MUT}: CONTROL DID NOT BITE (expected failures {EXPECT[MUT]}; failed: {failed})"); finish(0)
        out(f"MUTATE {MUT}: CONTROL BITES (expected {EXPECT[MUT]} all failed; all failed lines: {failed})"); finish(1)

if __name__ == "__main__":
    main()
