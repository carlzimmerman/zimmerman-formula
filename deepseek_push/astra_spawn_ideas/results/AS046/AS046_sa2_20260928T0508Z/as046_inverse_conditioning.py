#!/usr/bin/env python3
"""
AS046 - Numerical inverse conditioning (seed AS046_numerical_inverse_conditioning.md)
Worker: deepseek-v4-flash-0731 (openrouter) via Hermes subagent sa-2-0197cc40

Claim audited: for B = F^{-1}(g) on each declared branch, dB/dg = 1/F'(B) and the
relative condition number is kappa = g/(B F'(B)).  Branches (dimensionless,
x = g/a0 > 0, y = B/a0 > 0, a0 = kappa*c*sqrt(G*rho_Lambda), kappa=1/2 ADOPTED):

  Q    : x^2 = y^2 + y        (algebraic a0 line)
  RAR  : x = y*nu_RAR(y), nu_RAR = 1/(1-exp(-sqrt(y)))
  MU2  : y = x*mu2(x), mu2 = 1-(1+x/2)^(-2)                    (contract cell)
  EXP  : y = x*(1-exp(-x))                                     (historical AQUAL cell)
  MONO : x = y*nu_mono(y), nu_mono = 1 + h_mono(y)/y, heat-filter splice

Every branch: kappa(y) analytic/exact formula, mpmath high-precision finite
difference check, empirical inversion check (perturb g, invert, measure).
Negative controls: NC1 absolute-as-relative conditioning (unit dependence),
NC2 deep (y->0, kappa->2) and Newtonian (y->inf, kappa->1) limits with
leading neglected terms.  Grid y = 10^k, k = -10..8 step 0.1.  Roots
(y_p, y*) solved by explicit bisection with printed brackets.

Bounds: 1 thread, target < 120 s, < 512 MB (wall and RSS recorded).
"""
import math, time, json, resource, sys
import mpmath as mp

mp.mp.dps = 50
t0 = time.time()

# ---------------------------------------------------------------- branches
def nu_rar(y):
    s = mp.sqrt(y)
    return 1/(1 - mp.e**(-s))

def h_rar(y):
    """h_RAR(y) = y*(nu_RAR(y)-1) = y/(e^sqrt(y) - 1)"""
    s = mp.sqrt(y)
    return y/(mp.e**s - 1)

def h_rar_deriv(y):
    """exact h_RAR'(y).  h = y/(e^s-1), s=sqrt(y):
       h' = [(e^s-1) - y e^s/(2s)]/(e^s-1)^2  (with y=s^2 -> s e^s/2 in numerator)"""
    s = mp.sqrt(y)
    es = mp.e**s
    return (es - 1 - s*es/2)/(es - 1)**2

# --- MONO landmarks: y_p = argmax h_RAR, then y* solves h'_RAR(y*) = delta*h_p/(y*+y_p)
def solve_bisect(f, lo, hi, tol=mp.mpf(10)**(-40), maxit=300):
    flo, fhi = f(lo), f(hi)
    assert flo*fhi < 0, (lo, hi, flo, fhi)
    for _ in range(maxit):
        mid = (lo+hi)/2
        fm = f(mid)
        if fm == 0 or (hi-lo)/2 < tol*max(1, abs(mid)):
            return mid
        if flo*fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo+hi)/2

# y_p: peak of h_RAR: bracket by scan since h_RAR' - 0 crosses near y ~ 2.54
yp_lo, yp_hi = mp.mpf('2.0'), mp.mpf('3.5')
assert h_rar_deriv(yp_lo) > 0 and h_rar_deriv(yp_hi) < 0
y_p = solve_bisect(lambda y: h_rar_deriv(y), yp_lo, yp_hi)
h_p = h_rar(y_p)
delta = mp.mpf('0.05')

# y*: h'_RAR(y*) = delta*h_p/(y*+y_p)  ->  f(y) = h'_RAR(y) - delta*h_p/(y+y_p)
def cross_f(y):
    return h_rar_deriv(y) - delta*h_p/(y + y_p)
ylo, yhi = mp.mpf('2.0'), y_p
assert cross_f(ylo) > 0 and cross_f(yhi) < 0, (cross_f(ylo), cross_f(yhi))
y_star = solve_bisect(cross_f, ylo, yhi)

def nu_mono(y):
    """operative filtered MONO response (scalar argument, RAR piece + continuation)"""
    s = mp.sqrt(y)
    if y <= y_star:
        return (1 + h_rar(y)/y) if y > 0 else mp.mpf(1)
    h = h_rar(y_star) + delta*h_p*mp.log((y + y_p)/(y_star + y_p))
    return 1 + h/y

def h_mono(y):
    if y <= y_star:
        return h_rar(y)
    return h_rar(y_star) + delta*h_p*mp.log((y + y_p)/(y_star + y_p))

def h_mono_deriv(y):
    if y <= y_star:
        return h_rar_deriv(y)
    return delta*h_p/(y + y_p)

# --- conditioning (dimensionless; kappa = g/(B F'(B)), F' = dg/dB = dx/dy)
def kappa_Q(y):
    return 2*(y+1)/(2*y+1)

def kappa_RAR(y):
    s = mp.sqrt(y)
    return 1/(1 - (s/2)*mp.e**(-s)/(1 - mp.e**(-s)))

def kappa_MU2(x):
    mu2 = 1 - (1 + x/2)**(-2)
    mu2p = (1 + x/2)**(-3)          # exact derivative d/dx[1-(1+x/2)^-2]
    return 1 + x*mu2p/mu2

def kappa_EXP(x):
    return 1 + x*mp.e**(-x)/(1 - mp.e**(-x))

def kappa_MONO(y):
    hm, hpd = h_mono(y), h_mono_deriv(y)
    return (1 + hm/y)/(1 + hpd)

# --- forward maps x(y)
def x_q(y):   return mp.sqrt(y*y + y)
def x_rar(y): return y*nu_rar(y)
def x_mu2(y):
    # solve y = x*mu2(x), monotone increasing x -> bisect with exponential bracket
    lo, hi = mp.mpf('0.0'), mp.mpf('1.0')
    while x_mu2_f(hi) < y:
        hi *= 2
    return solve_bisect(lambda x: x_mu2_f(x) - y, lo, hi)
def x_mu2_f(x):
    mu2 = 1 - (1 + x/2)**(-2)
    return x*mu2
def x_exp(y):
    lo, hi = mp.mpf('0.0'), mp.mpf('1.0')
    while x_exp_f(hi) < y:
        hi *= 2
    return solve_bisect(lambda x: x_exp_f(x) - y, lo, hi)
def x_exp_f(x):
    return x*(1 - mp.e**(-x))
def x_mono(y): return y*nu_mono(y)

# --- inverse maps y(x) (for branch ordering at fixed x)
def y_q(x):
    return (mp.sqrt(1 + 4*x*x) - 1)/2
def y_rar(x):
    lo, hi = mp.mpf(10)**(-60), mp.mpf('1.0')
    while x_rar(hi) < x:
        hi *= 2
    return solve_bisect(lambda y: x_rar(y) - x, lo, hi)
def y_mu2(x):
    # MU2 relation y = x*mu2(x) is EXPLICIT in y given x: no inversion needed
    return x*(1 - (1 + x/2)**(-2))
def y_exp(x):
    # EXP relation y = x*(1-e^{-x}) is EXPLICIT in y given x
    return x*(1 - mp.e**(-x))
def y_mono(x):
    lo, hi = mp.mpf(10)**(-60), mp.mpf('1.0')
    while x_mono(hi) < x:
        hi *= 2
    return solve_bisect(lambda y: x_mono(y) - x, lo, hi)

# ---------------------------------------------------------------- grid run
grid = []
for k in range(-100, 81, 1):            # k/10 from -10.0 .. 8.0 step 0.1
    grid.append(mp.mpf(10)**(mp.mpf(k)/10))
assert len(grid) == 181

rows = []
for y in grid:
    x_Q, x_MU2, x_EXP = x_q(y), x_mu2(y), x_exp(y)
    x_RAR, x_MONO = x_rar(y), x_mono(y)
    rows.append({
        "log10y": float(mp.log(y, 10)),
        "y": float(y),
        "kappa_Q": float(kappa_Q(y)),
        "kappa_RAR": float(kappa_RAR(y)),
        "kappa_MU2": float(kappa_MU2(x_MU2)),
        "kappa_EXP": float(kappa_EXP(x_EXP)),
        "kappa_MONO": float(kappa_MONO(y)),
        "x_Q": float(x_Q), "x_RAR": float(x_RAR), "x_MU2": float(x_MU2),
        "x_EXP": float(x_EXP), "x_MONO": float(x_MONO),
    })

# ------------------------------------------------- independent check 1: mpmath
# finite difference of forward map at B (dimensionless): F'(y) = dx/dy ~ [x(y+d)-x(y-d)]/(2d)
# kappa_FD = x/(y*F'); compare with analytic kappa.
mp.mp.dps = 60
fd_checks = {}
for y in [mp.mpf(10)**(mp.mpf(-4)), mp.mpf(1), mp.mpf(10)**4, mp.mpf(10)**8]:
    d = mp.mpf(10)**(-45) * max(mp.mpf(1), y)
    for name, xfn, kfn in [("Q", x_q, kappa_Q), ("RAR", x_rar, kappa_RAR),
                           ("MONO", x_mono, kappa_MONO)]:
        fd = (xfn(y+d) - xfn(y-d))/(2*d)
        k_fd = xfn(y)/(y*fd)
        fd_checks[f"{name}@y={float(y):.1e}"] = {
            "kappa_analytic": float(kfn(y)),
            "kappa_finite_diff": float(k_fd),
            "abs_residual": float(abs(k_fd - kfn(y))),
        }
# MU2/EXP: use the EXPLICIT forward map y = y(x) (no bisection) so the finite
# difference is a true independent representation.  kappa = x/(y F') with
# F' = dx/dy = 1/(dy/dx), so kappa = x*(dy/dx)/y.
def y_mu2_of_x(x):
    return x*(1 - (1 + x/2)**(-2))
def y_exp_of_x(x):
    return x*(1 - mp.e**(-x))
for y in [mp.mpf(1), mp.mpf(10)**4, mp.mpf(10)**8]:
    x_M2 = x_mu2(y); x_EX = x_exp(y)
    d = mp.mpf(10)**(-30) * max(mp.mpf(1), x_M2)
    dy_M2 = (y_mu2_of_x(x_M2+d) - y_mu2_of_x(x_M2-d))/(2*d)
    dy_EX = (y_exp_of_x(x_EX+d) - y_exp_of_x(x_EX-d))/(2*d)
    kfd_M2 = x_M2*dy_M2/y
    kfd_EX = x_EX*dy_EX/y
    fd_checks[f"MU2@y={float(y):.1e}"] = {
        "kappa_analytic": float(kappa_MU2(x_M2)),
        "kappa_finite_diff": float(kfd_M2),
        "abs_residual": float(abs(kfd_M2 - kappa_MU2(x_M2))),
    }
    fd_checks[f"EXP@y={float(y):.1e}"] = {
        "kappa_analytic": float(kappa_EXP(x_EX)),
        "kappa_finite_diff": float(kfd_EX),
        "abs_residual": float(abs(kfd_EX - kappa_EXP(x_EX))),
    }

# --------------------------------------------- independent check 2: empirical
# conditioning by actual inversion: perturb g by +0.1%, invert to B, measure
empirical = {}
for y in [mp.mpf(10)**(mp.mpf(-3)), mp.mpf(1), mp.mpf(10)**3]:
    for name, yinv in [("Q", y_q), ("RAR", y_rar), ("MU2", y_mu2),
                       ("EXP", y_exp), ("MONO", y_mono)]:
        x = None
        if name == "Q": x = x_q(y)
        elif name == "RAR": x = x_rar(y)
        elif name == "MU2": x = x_mu2(y)
        elif name == "EXP": x = x_exp(y)
        elif name == "MONO": x = x_mono(y)
        eps = mp.mpf('0.001')
        xp, xm = x*(1+eps), x*(1-eps)
        yp, ym = yinv(xp), yinv(xm)
        relB = (yp - ym)/(2*eps*y)
        kappa_true = {"Q": kappa_Q(y), "RAR": kappa_RAR(y), "MU2": kappa_MU2(x_mu2(y)),
                      "EXP": kappa_EXP(x_exp(y)), "MONO": kappa_MONO(y)}[name]
        empirical[f"{name}@y={float(y):.1e}"] = {
            "kappa_true": float(kappa_true),
            "kappa_empirical": float(relB),
            "rel_residual": float(abs(relB - kappa_true)/kappa_true),
        }

# ---------------------------------------------------------------- NC1: absolute
# conditioning used as though it were relative -> catch unit/scale dependence.
nc1 = {}
for y in [mp.mpf(10)**(mp.mpf(-6)), mp.mpf(10)**(mp.mpf(-3)), mp.mpf(1)]:
    x = x_q(y)
    Fp = (2*y + 1)/(2*x)                     # dx/dy for Q
    kappa_abs = 1/Fp                         # |dB/dg| (dimensionless #)
    row = {
        "y": float(y), "x": float(x),
        "kappa_rel": float(kappa_Q(y)),
        "kappa_abs_as_rel": float(kappa_abs),
        "ratio_abs_over_rel": float(kappa_abs/kappa_Q(y)),   # = y/x
        "y_over_x": float(y/x),
    }
    # unit dependence: same physical measurement dg = 1e-13 m/s^2, expressed as
    # relative error on each footing (a0_can = 9.3619e-11, a0_alt = 1.1279e-10)
    A0_CAN, A0_ALT = mp.mpf('9.3619e-11'), mp.mpf('1.1279e-10')
    dg = mp.mpf('1e-13')
    relg_can = dg/(A0_CAN*x); relg_alt = dg/(A0_ALT*x)
    row["quot_B_rel_canonical"] = float(kappa_abs*relg_can)
    row["quot_B_rel_alt"] = float(kappa_abs*relg_alt)
    row["kappa_times_relg_can"] = float(kappa_Q(y)*relg_can)
    row["kappa_times_relg_alt"] = float(kappa_Q(y)*relg_alt)
    nc1[f"Q@y={float(y):.1e}"] = row

# ---------------------------------------------------------------- NC2: limits
nc2 = {
    "deep": {}, "newtonian": {}
}
for name, kfn in [("Q", kappa_Q), ("RAR", kappa_RAR), ("MONO", kappa_MONO)]:
    nc2["deep"][name] = {"y": float(grid[0]), "kappa": float(kfn(grid[0])),
                         "resid_vs_2": float(abs(kfn(grid[0]) - 2))}
    nc2["newtonian"][name] = {"y": float(grid[-1]), "kappa": float(kfn(grid[-1])),
                              "resid_vs_1": float(abs(kfn(grid[-1]) - 1))}
for name in ("MU2", "EXP"):
    yl, yh = grid[0], grid[-1]
    xl = x_mu2(yl) if name == "MU2" else x_exp(yl)
    xh = x_mu2(yh) if name == "MU2" else x_exp(yh)
    kfn = kappa_MU2 if name == "MU2" else kappa_EXP
    nc2["deep"][name] = {"y": float(yl), "x": float(xl), "kappa": float(kfn(xl)),
                         "resid_vs_2": float(abs(kfn(xl) - 2))}
    nc2["newtonian"][name] = {"y": float(yh), "x": float(xh), "kappa": float(kfn(xh)),
                              "resid_vs_1": float(abs(kfn(xh) - 1))}

# ---- asymptotic leading terms (analytic expansions, checked numerically)
asym = {
    "Q_deep_y_minus_x2": {"y": float(grid[0]), "y_minus_x^2": float(y_q(x_q(grid[0])) - x_q(grid[0])**2)},
    "Q_newton_y_minus_x": {"y": float(grid[-1]),
                           "y_minus_x": float(y_q(x_q(grid[-1])) - x_q(grid[-1])),
                           "minus_half_offset_resid": float(abs((y_q(x_q(grid[-1])) - x_q(grid[-1])) + mp.mpf('0.5')))},
}
# MU2/EXP y - x^2 deep leading term: x^3 coefficient
for name, xf in [("MU2", x_mu2), ("EXP", x_exp)]:
    y = grid[0]
    x = xf(y)
    asym[f"{name}_deep"] = {"y": float(y), "x": float(x),
                            "y_minus_x^2": float(y - x*x),
                            "x^3_coeff_ratio": float((y - x*x)/x**3)}
for name, xf in [("MU2", x_mu2), ("EXP", x_exp)]:
    y = grid[-1]
    x = xf(y)
    asym[f"{name}_newton"] = {"y": float(y), "x": float(x),
                              "y_minus_x": float(y - x), "x_minus_y": float(x - y)}

# ---- branch ordering at fixed x (response of inferred B/a0 for given g/a0)
xvals = [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.5'), mp.mpf(1), mp.mpf(2),
         mp.mpf(3), mp.mpf(5), mp.mpf(10), mp.mpf(100)]
ordering = []
for xv in xvals:
    ordering.append({
        "x": float(xv),
        "y_Q": float(y_q(xv)), "y_RAR": float(y_rar(xv)), "y_MU2": float(y_mu2(xv)),
        "y_EXP": float(y_exp(xv)), "y_MONO": float(y_mono(xv)),
    })

# ---- at-x=1 audit table (the dispatch-requested exact values)
x1 = mp.mpf(1)
mu_Q_1 = y_q(x1)                       # = y/x at x=1
mu_q_deriv = mp.mpf(2)/mp.sqrt(5) - (mp.sqrt(5)-1)/2
mu2_1 = 1 - (1 + x1/2)**(-2)
mu2p_1 = (1 + x1/2)**(-3)
mu_exp_1 = 1 - mp.e**(-1)
mu_exp_1p = mp.e**(-1)
y_rar_1 = y_rar(x1)
mu_rar_1 = y_rar_1                       # y/x at x=1
# dispatch-mentioned non-contract interpolant mu = x/sqrt(1+x^2):
mu_std_1 = 1/mp.sqrt(2)
mu_std_1p = (1 + 1) ** (-mp.mpf(3) / 2)   # (1+x^2)^(-3/2) at 1 = 2^(-3/2)
at_one = {
    "mu_Q(1)": float(mu_Q_1), "mu_Q'(1)": float(mu_q_deriv),
    "x*mu_Q'(1)": float(mu_q_deriv),
    "mu2_MU2(1)": float(mu2_1), "mu2'_MU2(1)": float(mu2p_1),
    "x*mu2'(1)_MU2": float(mu2p_1),
    "mu_RAR(1)": float(mu_rar_1),
    "mu_EXP(1)": float(mu_exp_1), "mu'_EXP(1)": float(mu_exp_1p),
    "x*mu'_EXP(1)": float(mu_exp_1p),
    "claim_1_over_sqrt2": float(mu_std_1),
    "claim_deriv_2^-3/2_(x/sqrt(1+x^2))": float(mu_std_1p),
    "kappa_Q(1)": float(kappa_Q(mp.mpf(1))),
    "kappa_RAR(1)": float(kappa_RAR(mp.mpf(1))),
    "kappa_MU2(1)": float(kappa_MU2(x_mu2(mp.mpf(1)))),
    "kappa_EXP(1)": float(kappa_EXP(x_exp(mp.mpf(1)))),
    "kappa_MONO(1)": float(kappa_MONO(mp.mpf(1))),
    "y_RAR(1)": float(y_rar_1),
}

# MONO splice continuity checks
splice = {
    "y_star": float(y_star), "y_p": float(y_p), "h_p": float(h_p),
    "h_RAR(y*)": float(h_rar(y_star)),
    "h_mono(y*-eps)": float(h_mono(y_star - mp.mpf('1e-30'))),
    "h_mono(y*+eps)": float(h_mono(y_star + mp.mpf('1e-30'))),
    "h'_RAR(y*)": float(h_rar_deriv(y_star)),
    "h'_mono(y*+eps)": float(h_mono_deriv(y_star + mp.mpf('1e-30'))),
    "jump_in_h_at_splice": float(abs(h_rar(y_star) - h_mono(y_star + mp.mpf('1e-30')))),
}

result = {
    "grid_size": len(grid),
    "rows": rows,
    "fd_checks": fd_checks,
    "empirical_checks": empirical,
    "nc1_absolute_as_relative": nc1,
    "nc2_limits": nc2,
    "asymptotics": asym,
    "ordering_at_fixed_x": ordering,
    "at_x_equal_1_audit": at_one,
    "mono_splice": splice,
    "bounds": {
        "wall_seconds": round(time.time() - t0, 3),
        "max_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "threads": 1,
    },
}

out = sys.argv[1] if len(sys.argv) > 1 else "as046_raw.json"
with open(out, "w") as f:
    json.dump(result, f, indent=1)
print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=1)[:6000])
print("WALL", result["bounds"])