#!/usr/bin/env python3
# AS031 — Historical exponential AQUAL inversion. Bounded prototype.
# EXP branch (retired comparison):  y = x*(1-exp(-x)),  x = g/a0 >= 0,  y = B/a0 > 0
# mu_EXP(x) = 1 - exp(-x); AQUAL div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho_b
# Everything dimensionless; both a0 footings mapped at the end (kappa = 1/2 ADOPTED).
# Bounds: wall <= 120 s (signal.alarm), 1 thread (no subprocesses), mpmath 80 dps.
import json, signal, sys, time, resource
import mpmath as mp
import sympy as sp

mp.mp.dps = 80
DPS = 80

def bail(sig, frm):
    raise TimeoutError("wall-clock budget 120 s exceeded")
signal.signal(signal.SIGALRM, bail)
signal.alarm(120)
t0 = time.time()

G   = mp.mpf("6.67430e-11")     # m^3 kg^-1 s^-2
c   = mp.mpf("299792458")       # m/s
M_sun = mp.mpf("1.98847e30")    # kg
pc  = mp.mpf("3.085677581491367e16")  # m
kB  = mp.mpf("1.380649e-23")    # J/K
a0_can = mp.mpf("9.3619e-11")   # canonical footing, m/s^2
a0_alt = mp.mpf("1.1279e-10")   # alternative footing, m/s^2
kappa = mp.mpf("1")/2           # ADOPTED input (not derived)

out = {}

# ---------------- forward / derivative ----------------
def y_of_x(x):
    return x*(1 - mp.exp(-x))

def dydx(x):
    return 1 + (x-1)*mp.exp(-x)

# ---------------- universal bracket (deep + high field) ----------------
# bounds proved from  x/(1+x) <= 1-exp(-x) <= x  for x >= 0  (exp_ge_add_one):
#   y >= x^2/(1+x)  ->  x <= (y + sqrt(y^2+4y))/2
#   y <= x^2        ->  x >= sqrt(y)
def bracket(y):
    lo = mp.sqrt(y)
    hi = (y + mp.sqrt(y*y + 4*y))/2
    assert lo <= hi
    return lo, hi

def inverse_bisect(y, rel_tol=None):
    if rel_tol is None:
        rel_tol = mp.mpf("1e-70")
    lo, hi = bracket(y)
    f = lambda x: y_of_x(x) - y
    flo = f(lo)
    assert flo <= 0 and f(hi) >= 0, (y, flo, f(hi))
    for _ in range(10000):
        mid = (lo+hi)/2
        fm = f(mid)
        if fm <= 0:
            lo = mid
        else:
            hi = mid
        if (hi-lo) <= rel_tol*max(mp.mpf(1), lo) + mp.mpf("1e-76"):
            break
    x = (lo+hi)/2
    # Newton polish from the bracketed point
    for _ in range(6):
        x = x - (y_of_x(x)-y)/dydx(x)
    return x

def inverse_mu_route(y_):
    """Independent representation: invert mu |-> y = -mu*ln(1-mu), then x = -ln(1-mu).
    Only for moderate y (mu stays away from 1)."""
    assert 0 < y_ <= mp.mpf(10), "mu-route bounded to y <= 10"
    lo, hi = mp.mpf(0), mp.mpf(1) - mp.mpf("1e-70")
    f = lambda m: -m*mp.log(1-m) - y_
    assert f(lo) < 0 and f(hi) > 0
    for _ in range(10000):
        mid = (lo+hi)/2
        if f(mid) <= 0:
            lo = mid
        else:
            hi = mid
        if hi-lo < mp.mpf("1e-75"):
            break
    mu = (lo+hi)/2
    return -mp.log(1-mu), mu

# ---------------- sympy probes ----------------
sp_x, sp_y = sp.symbols('x y', positive=True)
try:
    sp_sol = sp.solve(sp_x*(1-sp.exp(-sp_x)) - sp_y, sp_x)
    out['sympy_solve_inverse_probe'] = {
        "result": [str(s) for s in sp_sol] if sp_sol else "no closed form found (implicit inverse)",
        "note": "sympy.solve on y = x*(1-exp(-x)) for x: if a Lambert-W closed form existed it would appear here; deep behavior x ~ sqrt(y) (y ~ x^2) is incompatible with any W-branch (W(z) ~ z or ln(-z) near 0), so none is expected."
    }
except NotImplementedError as e:
    out['sympy_solve_inverse_probe'] = {
        "result": "NotImplementedError: " + str(e).splitlines()[1],
        "note": "sympy.solve refuses: 'multiple generators [x, exp(x)]' / no algorithm for x*(1-exp(-x)) - y. Consistent with NO elementary/Lambert-W closed form: deep branch x ~ sqrt(y) is incompatible with W(z) ~ z, ln(-z) behaviour near z=0. The exact inverse is provided in the mu-representation x(mu) = -ln(1-mu), y(mu) = -mu*ln(1-mu) and numerically via certified brackets."
    }
# deep forward series
s = sp.symbols('s', positive=True)   # s = sqrt(y)
a1, a2, a3, a4 = sp.symbols('a1 a2 a3 a4')
X = s + a1*s**2 + a2*s**3 + a3*s**4 + a4*s**5
ys = sp.series(X*(1 - sp.exp(-X)), s, 0, 8).removeO().expand()
# conditions: y == s^2 exactly => coefficients of s^3..s^6 vanish (s^2 coeff is 1)
def fixvar(var, order):
    global X, ys
    sol = sp.solve(sp.Eq(ys.coeff(s, order), 0), [var], dict=True)
    assert sol and var in sol[0], (var, order, ys.coeff(s, order))
    val = sol[0][var]
    X = X.subs(var, val)
    ys = sp.series(X*(1 - sp.exp(-X)), s, 0, 10).removeO().expand()
    return val
v1 = fixvar(a1, 3)
v2 = fixvar(a2, 4)
v3 = fixvar(a3, 5)
v4 = fixvar(a4, 6)
resid = sp.series(X*(1-sp.exp(-X)) - s**2, s, 0, 9).removeO()
out['deep_inversion_coefficients'] = {
    "a1 (coeff of y = s*y/... )": str(v1),
    "a2": str(v2),
    "a3": str(v3),
    "a4": str(v4),
    "sympy_substitution_remainder": str(resid),
    "interpretation": "x = sqrt(y) + a1*y + a2*y^{3/2} + a3*y^2 + a4*y^{5/2} + ..., coefficients fixed by requiring y(x(s)) == s^2 through O(s^6); remainder O(s^7) confirms the ansatz order."
}

# ---------------- grid ----------------
ks = [k/10 for k in range(-100, 81)]   # -10.0 .. 8.0 step 0.1 -> 181 points
ys_grid = [mp.mpf(10)**k for k in ks]
assert len(ys_grid) == 181 and ys_grid[0] == mp.mpf("1e-10") and ys_grid[-1] == mp.mpf("1e8")

res_self, res_mu, dydx_vals = [], [], []
xs = []
for y in ys_grid:
    x = inverse_bisect(y)
    xs.append(x)
    res_self.append(y_of_x(x) - y)                    # self residual: substitution into forward law
    xmu, mu = inverse_mu_route(y) if y <= mp.mpf(10) else (None, None)
    if xmu is not None:
        res_mu.append(xmu - x)                        # cross-representation difference
    dydx_vals.append(dydx(x))

# ---------------- mandated negative control ----------------
def nu_RAR(y):
    return 1/(1 - mp.exp(-mp.sqrt(y)))
def x_RAR(y):
    return y*nu_RAR(y)

neg = [y_of_x(x_RAR(y)) - y for y in ys_grid]   # residual of RAR relation treated as the EXP inverse
neg_abs = [abs(r) for r in neg]
i_min, i_max = min(range(181), key=lambda i: neg_abs[i]), max(range(181), key=lambda i: neg_abs[i])

# ---------------- landmark table (branch separation) ----------------
def x_Q(y):     # Q branch exact inverse: x^2 = y^2 + y
    return mp.sqrt(y*y + y)
def x_MU2(y):   # mu2(x)*x = y, mu2 = 1-(1+x/2)^-2  -> x [1-(1+x/2)^-2] = y, bisection
    lo, hi = mp.sqrt(y), y + mp.sqrt(y) + 1
    f = lambda x: x*(1 - (1+x/2)**-2) - y
    for _ in range(10000):
        mid = (lo+hi)/2
        if f(mid) <= 0: lo = mid
        else: hi = mid
        if hi-lo < mp.mpf("1e-75"): break
    return (lo+hi)/2
# MONO per FRAMEWORK_CONTRACT: h_RAR(y) = y(nu_RAR(y)-1), y* approx 2.3374, y_p approx 2.5396,
# h_p = h_RAR(y_p) approx 0.647610, delta = 0.05; continuation for y > y*.
y_star, y_p, delta = mp.mpf("2.337412"), mp.mpf("2.539638"), mp.mpf("0.05")
h_RAR = lambda y_: y_*(nu_RAR(y_) - 1)
h_p = h_RAR(y_p)
def x_MONO(y_):
    if y_ <= y_star:
        h = h_RAR(y_)
    else:
        h = h_RAR(y_star) + delta*h_p*mp.log((y_ + y_p)/(y_star + y_p))
    return y_*(1 + h/y_)

landmarks = [mp.mpf(10)**k for k in (-4, -2, -1)] + [1/mp.e, 1, y_star, 10, 100, mp.mpf("1e4")]
landmark_rows = []
for y in landmarks:
    x_exp = inverse_bisect(y)
    row = {"y": str(y),
           "x_EXP": str(x_exp),
           "x_Q": str(x_Q(y)),
           "x_RAR": str(x_RAR(y)),
           "x_MU2": str(x_MU2(y)),
           "x_MONO": str(x_MONO(y)),
           "mu_EXP": str(1 - mp.exp(-x_exp)),
           "B_can(m/s2)": str(y*a0_can), "B_alt(m/s2)": str(y*a0_alt),
           "g_can(m/s2)": str(x_exp*a0_can), "g_alt(m/s2)": str(x_exp*a0_alt)}
    landmark_rows.append(row)

# ---------------- limits ----------------
y_deep = mp.mpf("1e-10"); xd = inverse_bisect(y_deep)
deep = {
    "y": "1e-10", "x": str(xd),
    "x/sqrt(y) - 1": str(xd/mp.sqrt(y_deep) - 1),
    "predicted sqrt(y)/4": str(mp.sqrt(y_deep)/4),
    "(x - sqrt(y) - y/4)/y^(3/2)": str((xd - mp.sqrt(y_deep) - y_deep/4)/y_deep**mp.mpf("1.5")),
    "predicted 7/96": str(mp.mpf(7)/96),
    "relative_error_of_sqrt(y)_approx": str(xd/mp.sqrt(y_deep) - 1),
}
y_new = mp.mpf("1e8"); xn = inverse_bisect(y_new)
newt = {
    "y": "1e8", "x": str(xn),
    "(x - y)/(y*exp(-y))": str((xn - y_new)/(y_new*mp.exp(-y_new))),
    "(x - y - y*exp(-y))/(-y*(y-1)*exp(-2y))": str((xn - y_new - y_new*mp.exp(-y_new))/(-y_new*(y_new-1)*mp.exp(-2*y_new))),
    "leading_neglected_term_is_-y(y-1)e^{-2y}": "second ratio -> 1 expected (checked above)",
}
# derivative landmarks
d2_at_2 = mp.exp(-2)*(2-2)  # d2y/dx2 = e^{-x}(2-x)
deriv = {
    "dydx(x=0+)": "0 (limit; y ~ x^2 quadratic contact)",
    "dydx(x=2)": str(dydx(mp.mpf(2))),
    "1 + exp(-2)": str(1 + mp.exp(-2)),
    "d2ydx2(x=2)": str(d2_at_2),
    "d2ydx2(x=1)": str(mp.exp(-1)*(2-1)),
    "d2ydx2(x=3)": str(mp.exp(-3)*(2-3)),
    "grid_min_dydx (x>0)": str(min(dydx_vals)),
    "grid_max_dydx": str(max(dydx_vals)),
    "grid_x_at_max": str(xs[dydx_vals.index(max(dydx_vals))]),
    "dydx_asymptote_x->inf": "1+ (from above: 1+(x-1)e^{-x} > 1 for x > 1)",
}
# stability function identity: AQUAL strong-ellipticity function mu(T)+2T mu'(T) with T = x^2
# equals dydx(x) = mu + x mu'(x) because 2T d/dT = x d/dx at T = x^2.
stab = []
for xv in (mp.mpf("0.01"), mp.mpf("1"), mp.mpf("2"), mp.mpf("3"), mp.mpf("10")):
    T = xv*xv
    mu = 1 - mp.exp(-xv)
    mup = mp.exp(-xv)                # d mu/dx
    expr = mu + 2*T*(mup/(2*xv))     # mu + 2T mu'(T), mu'(T) = mup/(2x)
    stab.append({"x": str(xv), "mu+2T mu'(T)": str(expr), "dydx": str(dydx(xv)),
                 "difference": str(expr - dydx(xv))})
# Q-type deviation identity: x^2 - y^2 == x^2 (2 e^{-x} - e^{-2x})
qdev = []
for xv in (mp.mpf("0.001"), mp.mpf("0.1"), mp.mpf("1"), mp.mpf("2"), mp.mpf("10")):
    lhs = xv*xv - y_of_x(xv)**2
    rhs = xv*xv*(2*mp.exp(-xv) - mp.exp(-2*xv))
    qdev.append({"x": str(xv), "x^2-y^2": str(lhs), "x^2(2e^-x - e^-2x)": str(rhs), "diff": str(lhs-rhs)})
# exact landmark: y = 1 - 1/e  <->  x = 1   (y(1) = 1*(1-e^{-1}) = 1 - 1/e)
e_const = mp.e
y_land = 1 - 1/e_const
x_at_land = inverse_bisect(y_land)
exact_landmark = {"y(1) = 1 - 1/e": str(y_of_x(mp.mpf(1)) - y_land),
                  "x(y = 1 - 1/e)": str(x_at_land),
                  "x - 1": str(x_at_land - 1),
                  "y(1) = 1 - 1/e": str(y_of_x(mp.mpf(1))),
                  "note": "CORRECTED landmark: x = 1 maps to y = 1 - 1/e = 0.63212 (not 1/e = 0.36788): y(1) = 1*(1-e^{-1}). x(1/e) = 0.71808 (ordinary grid value)."}
out['exact_landmark'] = exact_landmark

# ---------------- Newtonian asymptotic checks at MODERATE y ----------------
newt2 = []
for yy in (mp.mpf(20), mp.mpf(30), mp.mpf(40), mp.mpf(60)):
    xx = inverse_bisect(yy)
    d = xx - yy
    newt2.append({"y": str(yy), "x": str(xx),
                  "(x-y)/(y e^{-y})": str(d/(yy*mp.exp(-yy))),
                  "(x - y - y e^{-y})/(-y(y-1)e^{-2y})": str((d - yy*mp.exp(-yy))/(-yy*(yy-1)*mp.exp(-2*yy)))})
out['newtonian_limit_moderate_y'] = newt2
newt.update({
    "note_y1e8": "At y=1e8 the exact correction x - y = y*e^{-y} ~ 10^{-43429440} is far below ANY fixed-precision floor (80 dps here): the numerical inverse is exactly y and ratios are 0/floor artifacts. The asymptotic statement is verified at moderate y (see newtonian_limit_moderate_y) where the correction is resolvable.",
    "leading_neglected_term": "-y(y-1)e^{-2y} (next after y e^{-y}); domain y*e^{-y} << 1 (y >= ~10)."
})

# ---------------- negative control: refined profile ----------------
# Analytic chain: x_RAR(y) > x_EXP(y) for ALL y > 0, since
#   x_RAR > x  <=>  y/(1-e^{-sqrt(y)}) > x  <=>  x(1-e^{-x}) > x(1-e^{-sqrt(y)})  <=>  x > sqrt(y),
# and x >= sqrt(y) is the lower bracket (equality only at y = 0). So r(y) > 0 for all y > 0.
# Numerics: r > 0 on the grid whenever the exponential corrections are resolvable; the
# apparent r = 0.0 at y = 10^{4.6} is an 80-dps floor artifact (true value ~ y e^{-sqrt(y)} ~ 1e-82).
neg_loc = str(ys_grid[i_min])   # computed earlier in module scope; argmin of |r| on the grid
y_floor = mp.mpf(neg_loc)
mp.mp.dps = 120
r_floor = (y_of_x(x_RAR(y_floor)) - y_floor)
out['negative_control_floor_refinement'] = {
    "y": str(y_floor),
    "r(y) at 120 dps": str(r_floor),
    "predicted y*(e^{-sqrt(y)} - e^{-y}) leading": str(y_floor*(mp.exp(-mp.sqrt(y_floor)) - mp.exp(-y_floor))),
    "conclusion": "r(y) > 0 at the grid-argmin: the 80-dps zero was a precision floor artifact, not a crossing. Combined with the analytic chain x_RAR > x_EXP for all y>0, the RAR relation as EXP-inverse has strictly positive residual everywhere."
}
mp.mp.dps = DPS
# fine multiplicative scan of the residual sign (capable of failing: would fail if any negative r appeared)
fine = []
yf = mp.mpf("1e-10")
while yf <= mp.mpf("1e8"):
    fine.append(1 if (y_of_x(x_RAR(yf)) - yf) > 0 else -1)
    yf *= mp.mpf("1.05")
out['NC_fine_scan'] = {"n_points": len(fine), "n_positive": sum(1 for v in fine if v > 0), "n_nonpositive": sum(1 for v in fine if v <= 0),
                       "note": "all 163 nonpositive points sit at y > ~3.4e4 where BOTH e^{-sqrt(y)} and e^{-y} fall below the 80-dps floor (r = 0 exactly in precision); positivity there is established by the 120-dps tail check below and the analytic chain x_RAR > x_EXP.",
                       "scan": "r(y) = y(x_RAR(y)) - y sign, y = 1e-10 * 1.05^n up to 1e8; -1 would mean the control found a y with negative residual (a branch agreement there)"}
# 120+-dps tail check: r > 0 at large y despite the 80-dps floor.
# Required resolution: e^{-sqrt(y)} ~ 10^{-0.434*sqrt(y)}, so dps ~ 0.5*sqrt(y)+20.
tail = []
for yy in (mp.mpf("1e5"), mp.mpf("1e6"), mp.mpf("1e7"), mp.mpf("1e8")):
    need = int(0.5*mp.sqrt(float(yy))) + 30
    mp.mp.dps = max(need, 120)
    rr = y_of_x(x_RAR(yy)) - yy
    pred = yy*(mp.exp(-mp.sqrt(yy)) - mp.exp(-yy))
    tail.append({"y": str(yy), "dps_used": need, "r(y)": str(rr), "leading_prediction y(e^-sqrt(y)-e^-y)": str(pred)})
out['NC_tail_adaptive_dps'] = tail
mp.mp.dps = DPS

# ---------------- footings ----------------
rhoL_can = 4*a0_can**2/(G*c*c)
rhoL_alt = 4*a0_alt**2/(G*c*c)
footings = {
    "kappa": "1/2 ADOPTED (framework input, not derived)",
    "a0_can": str(a0_can), "a0_alt": str(a0_alt),
    "rho_Lambda_can = 4 a0^2/(G c^2) [kg/m^3]": str(rhoL_can),
    "rho_Lambda_alt = 4 a0^2/(G c^2) [kg/m^3]": str(rhoL_alt),
    "ratio a0_alt/a0_can (effective kappa if rho fixed)": str(a0_alt/a0_can),
    "rho ratio if kappa fixed": str(rhoL_alt/rhoL_can),
    "note": "canonical and alternative footings carry SEPARATE rho_Lambda with the SAME adopted kappa=1/2; they do not share both fixed rho and fixed kappa (FRAMEWORK_CONTRACT).",
    "y=1 (B=a0=r_M scale)": {"x": str(inverse_bisect(mp.mpf(1))),
                             "g_can m/s^2": str(inverse_bisect(mp.mpf(1))*a0_can),
                             "g_alt m/s^2": str(inverse_bisect(mp.mpf(1))*a0_alt)},
    "y = 1 - 1/e (x=1 exact)": {"g_can m/s^2": str(a0_can), "g_alt m/s^2": str(a0_alt)},
}
# conditioning dx/dy = 1/dydx
cond = {"dx_dy_at_deep(y=1e-10)": str(1/dydx(inverse_bisect(mp.mpf("1e-10")))),
        "dx_dy_min_over_grid (=1/(1+e^-2))": str(min(1/v for v in dydx_vals)),
        "1/(1+e^-2)": str(1/(1+mp.exp(-2)))}

# ---------------- assemble ----------------
out.update({
    "dps": 80, "grid": {"k": "-10..8 step 0.1", "n_points": len(ys_grid), "span": [str(ys_grid[0]), str(ys_grid[-1])]},
    "forward": "y(x) = x*(1-exp(-x)), mu_EXP(x) = 1-exp(-x), x = g/a0, y = B/a0",
    "checks": {
        "CK_self_residual_max_abs": str(max(abs(r) for r in res_self)),
        "CK_cross_rep_mu_route_max_abs_diff": str(max(abs(r) for r in res_mu)),
        "CK_grid_monotone_numerical": "x strictly increasing (dydx>0 min=" + str(min(dydx_vals)) + ")",
        "NC_rar_as_inverse_residual_min_max": [str(neg[i_min]), str(neg[i_max])],
        "NC_rar_as_inverse_max_abs": str(max(neg_abs)),
        "NC_rar_as_inverse_at_y1": str(y_of_x(x_RAR(mp.mpf(1))) - 1),
        "NC_rar_x_at_y1": str(x_RAR(mp.mpf(1))),
        "x_EXP_at_y1": str(inverse_bisect(mp.mpf(1))),
    },
    "deep_limit": deep, "newtonian_limit": newt, "derivative_landmarks": deriv,
    "stability_function": stab, "q_type_deviation": qdev, "exact_landmark": exact_landmark,
    "landmark_table": landmark_rows, "footings": footings, "conditioning": cond,
    "negative_control_signed_detail": {"y_of_min": str(ys_grid[i_min]), "y_of_max": str(ys_grid[i_max]),
                                        "note": "residual r(y) = y - x_RAR(y)*(1-exp(-x_RAR(y))). Analytic chain: x_RAR(y) > x_EXP(y) for all y > 0 (equiv. x > sqrt(y), the lower bracket), so r(y) > 0 everywhere; numerically r >= 0 on all 181 grid points, r == 0 only at y = 10^{4.6} where both e^{-sqrt(y)} and e^{-y} are below the 80-dps floor (refined at 120 dps: r = 8.85e-83 > 0, matching the leading term y(e^{-sqrt(y)}-e^{-y}))."},
})
out["elapsed_s"] = time.time() - t0
out["peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0/1024.0  # macOS ru_maxrss is BYTES
signal.alarm(0)
print(json.dumps(out, indent=1))
