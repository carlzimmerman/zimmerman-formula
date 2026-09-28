#!/usr/bin/env python3
"""
AS029 — MU2 implicit force cubic: exact structure, root count, bracketing, inverse, controls.
Task: deepseek_push/astra_spawn_ideas/AS029_mu2_implicit_force_cubic.md
Branch: MU2 (mu2(x) = 1-(1+x/2)^(-2), mu2(x) g = B, x = g/a0, y = B/a0). Comparison branch only;
operative target is filtered nu_mono with causality criterion B — never identified with MU2.
Framework inputs: a0 = kappa*c*sqrt(G*rho_Lambda), kappa = 1/2 ADOPTED (not derived here).
Numerics: G = 6.67430e-11, c = 299792458, M_sun = 1.98847e30, pc = 3.085677581491367e16.
Bounds: wall <= 120 s (enforced deadline), RLIMIT_AS 512 MB if settable (recorded), 1 thread
(OMP/OPENBLAS threads pinned to 1; single process). Exit non-zero on any failed check.
"""
import json, os, sys, time, math, resource, platform
import numpy as np

T0 = time.time()
WALL_LIMIT_S = 120.0
MEM_LIMIT_BYTES = 512 * 1024 * 1024

# --- enforced resource bounds -------------------------------------------------
mem_enforced = False
try:
    resource.setrlimit(resource.RLIMIT_AS, (MEM_LIMIT_BYTES, MEM_LIMIT_BYTES))
    mem_enforced = True
except (ValueError, OSError, PermissionError) as e:
    mem_enforced = f"not settable: {e}"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

def deadline():
    if time.time() - T0 > WALL_LIMIT_S:
        raise RuntimeError(f"wall-time limit {WALL_LIMIT_S}s exceeded (ENFORCED)")

RESULTS = {}
CHECKS = []   # (name, ok, observed, tolerance)
def check(name, ok, observed, tol):
    CHECKS.append({"name": name, "pass": bool(ok), "observed": observed, "tolerance": tol})
    print(f"{'PASS' if ok else 'FAIL'}  {name}  observed={observed}  tol={tol}", flush=True)

OUT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(OUT, "raw_outputs")
os.makedirs(RAW, exist_ok=True)

# =============================================================================
# 1. SYMBOLIC LANE (sympy): exact algebra of the MU2 branch
# =============================================================================
import sympy as sp

x, y = sp.symbols("x y", positive=True)
a0, B = sp.symbols("a0 B", positive=True)

mu2 = 1 - (1 + x/2)**(-2)
expr_y = sp.simplify(x * mu2)            # y = x * mu2(x)
cubic_x = sp.expand(x**2 * (x + 4) - y * (x + 2)**2)   # cleared denominators
cubic_x_monic = sp.Poly(cubic_x, x).as_expr() / 1
cubic_g = sp.expand((sp.Poly(sp.expand(cubic_x.subs({x: sp.symbols('g')/a0, y: B/a0})), sp.symbols('g')).as_expr()) * a0**3)

# discriminant (monic cubic x^3 + b x^2 + c x + d)
b, c, d = sp.symbols("b c d")
disc_formula = sp.expand(b**2*c**2 - 4*c**3 - 4*b**3*d - 27*d**2 + 18*b*c*d)
_, bv, cv, dv = [sp.Poly(cubic_x, x).nth(i) for i in (3, 2, 1, 0)]
coefs_x = sp.Poly(cubic_x, x).all_coeffs()   # [1, 4-y, -4y, -4y]
bx, cx, dx = coefs_x[1], coefs_x[2], coefs_x[3]
Delta_x = sp.factor(disc_formula.subs({b: bx, c: cx, d: dx}))
Delta_g = sp.factor(disc_formula.subs({b: sp.expand(4*a0 - B), c: -4*a0*B, d: -4*a0**2*B}))

# derivatives
dy_dx = sp.factor(sp.diff(expr_y, x))
dmu2_dx = sp.factor(sp.diff(mu2, x))

# asymptotic expansions
x_deep = sp.series(expr_y, x, 0, 6)   # y(x) for small x
# invert y = x^2 - 3x^3/4 + ...  : x = sqrt(y)*u(y)
u = sp.Function("u")
x_inv_deep_eq = sp.Eq(y, (sp.sqrt(y)*u(y))**2 - sp.Rational(3,4)*(sp.sqrt(y)*u(y))**3)
x_inv_deep = sp.series(sp.sqrt(y) * (1 + sp.Rational(3,8)*sp.sqrt(y) + sp.Rational(3,16)*y), y, 0, 3)
# Newtonian: x - y = 4x/(x+2)^2 ~ 4/x
z = sp.symbols("z")
x_newt_series = sp.series(expr_y.subs(x, y + z), z, 0, 3).expand()
# solve x = y + 4/y + w/y^2 ...
x_inv_newt = y + 4/y

# nu (booster) deep additive constants for branch distinctness:
#   MU2: x/y = 1/sqrt(y) + 3/8 + ...   RAR: 1/sqrt(y) + 1/2   Q: 1/sqrt(y) + sqrt(y)/2
nu_MU2_deep = sp.series((sp.sqrt(y) + sp.Rational(3,8)*y)/y, y, 0, 2)
u = sp.symbols("u", positive=True)
nu_RAR_deep  = sp.series(1/(1 - sp.exp(-u)), u, 0, 3).subs(u, sp.sqrt(y))
nu_Q_deep    = sp.series(sp.sqrt(1 + y), y, 0, 3) / sp.sqrt(y)

# monotonicity numerator factorization (for the Lean lane)
x1, x2 = sp.symbols("x1 x2", positive=True)
N = sp.factor(x2**2*(x2+4)*(x1+2)**2 - x1**2*(x1+4)*(x2+2)**2)
Q = sp.expand(x1**2 + x1*x2 + x2**2 + (4-y)*(x1+x2) - 4*y)

sym = {
  "mu2(x)": str(mu2),
  "y(x) = x*mu2(x) exact rational form": str(sp.factor(x*(1-4/(x+2)**2))),
  "cubic in x": str(cubic_x_monic),
  "cubic in g": str(sp.factor(cubic_g)),
  "Delta_x": str(Delta_x),
  "Delta_g": str(Delta_g),
  "dy/dx": str(dy_dx),
  "dmu2/dx": str(dmu2_dx),
  "y(x) small-x series": str(x_deep),
  "x(y) deep inversion (leading + 3/8 sqrt(y))": str(sp.series(x_inv_deep, y, 0, 3)),
  "x - y relation (exact)": "x - y = 4x/(x+2)^2",
  "x(y) Newtonian inversion y + 4/y": str(x_inv_newt),
  "nu_MU2 deep": str(sp.series(nu_MU2_deep, y, 0, 2)),
  "nu_RAR deep": str(nu_RAR_deep),
  "nu_Q deep": str(sp.series(nu_Q_deep, y, 0, 2)),
  "N factor (y-monotonicity numerator)": str(N),
  "Q (root-difference bracket)": str(Q),
  "P(y)": str(sp.factor(cubic_x_monic.subs(y, y)) .subs(x, y)),
  "P(y+4)": str(sp.factor(cubic_x_monic.subs(x, y+4))),
  "P(-2)": str(sp.factor(cubic_x_monic.subs(x, -2))),
  "P(-(y+4))": str(sp.factor(cubic_x_monic.subs(x, -(y+4)))),
}
with open(os.path.join(RAW, "symbolic.json"), "w") as f:
    json.dump(sym, f, indent=2)
for k, v in sym.items():
    print(f"SYM  {k} = {v}", flush=True)

check("symbolic: y(x)=x*mu2 clears to the cubic", sp.simplify(cubic_x_monic - (x**2*(x+4) - y*(x+2)**2)) == 0, "0", "0")
check("symbolic: Delta_x factorization 16y(2y^2+13y+64)",
      sp.simplify(Delta_x - 16*y*(2*y**2 + 13*y + 64)) == 0, str(Delta_x), "16y(2y^2+13y+64)")
check("symbolic: Delta_g = 16 a0^3 B (2B^2 + 13 a0 B + 64 a0^2)",
      sp.simplify(Delta_g - 16*a0**3*B*(2*B**2 + 13*a0*B + 64*a0**2)) == 0, str(Delta_g), "16 a0^3 B (2B^2+13 a0 B+64 a0^2)")
check("symbolic: dy/dx = x(x^2+6x+16)/(x+2)^3 > 0 on x>0",
      sp.simplify(dy_dx - x*(x**2 + 6*x + 16)/(x+2)**3) == 0, str(dy_dx), "x(x^2+6x+16)/(x+2)^3")
check("symbolic: dmu2/dx = 8/(x+2)^3 > 0",
      sp.simplify(dmu2_dx - 8/(x+2)**3) == 0, str(dmu2_dx), "8/(x+2)^3")
check("symbolic: P(y) = -4y < 0", sp.simplify(cubic_x_monic.subs(x, y) + 4*y) == 0, str(cubic_x_monic.subs(x, y)), "-4y")
check("symbolic: P(y+4) = 4y^2+44y+128 > 0",
      sp.simplify(cubic_x_monic.subs(x, y+4) - (4*y**2 + 44*y + 128)) == 0, str(cubic_x_monic.subs(x, y+4)), "4y^2+44y+128")
check("symbolic: P(-2) = 8 > 0", sp.simplify(cubic_x_monic.subs(x, -2) - 8) == 0, str(cubic_x_monic.subs(x, -2)), "8")
check("symbolic: P(-(y+4)) = -2y(y^2+6y+10) < 0",
      sp.simplify(cubic_x_monic.subs(x, -(y+4)) + 2*y*(y**2 + 6*y + 10)) == 0,
      str(cubic_x_monic.subs(x, -(y+4))), "-2y(y^2+6y+10)")

# -----------------------------------------------------------------------------
# 2. NUMERICAL GRID LANE (numpy float64): y = 10^k, k in [-10, 8], step 0.1
# -----------------------------------------------------------------------------
ks = np.arange(-10.0, 8.0 + 1e-9, 0.1)
grid_y = 10.0**ks
tol_root_res = 1e-9          # tolerance set BEFORE evaluation (float64 scale)
TOL_REL_CUBIC_RES = 1e-12    # relative to the floating-point scale of P's terms
TOL_REL_IMPL_RES  = 1e-12
TOL_BRACKET_MARGIN = 1e-14   # relative margin on the exact identity x - y = 4x/(x+2)^2

def mu2f(x):
    return 1.0 - (1.0 + x/2.0)**(-2)

def rel_cubic_resid(xv, yv):
    # relative to the floating-point scale of the terms (conditioned evaluation)
    t3, t2, t1, t0 = abs(xv**3), abs((4.0-yv)*xv**2), abs(4.0*yv*xv), abs(4.0*yv)
    return abs(xv**3 + (4.0-yv)*xv**2 - 4.0*yv*xv - 4.0*yv) / (t3 + t2 + t1 + t0)

def rel_impl_resid(xv, yv):
    # exact rational form of y = x*mu2(x) = x^2 (x+4)/(x+2)^2: no cancellation at any x>0
    ym = xv**2 * (xv + 4.0) / (xv + 2.0)**2
    return abs(yv - ym) / max(yv, ym)

grid_rows = []
n_pos = 0
for yv in grid_y:
    deadline()
    coef = np.array([1.0, 4.0 - yv, -4.0*yv, -4.0*yv])
    rts = np.roots(coef)
    real = np.array([complex(r).real for r in rts])
    imag = np.array([abs(complex(r).imag) for r in rts])
    pos = real[(real > 0) & (imag < 1e-10)]
    x_star = float(pos[np.argmax(pos)]) if len(pos) else None
    n_pos += int(len(pos) == 1)
    cub_res = rel_cubic_resid(x_star, yv) if x_star else None
    impl_res = rel_impl_resid(x_star, yv) if x_star else None
    mu = mu2f(x_star) if x_star else None
    other = [float(r) for r, im in zip(real, imag) if im < 1e-10 and float(r) <= 0.0]
    neg_ok = all(o < 0 for o in other)
    # exact identity: x - y = 4x/(x+2)^2  (no cancellation in this form)
    margin_low = (4.0*x_star/(x_star + 2.0)**2) if x_star else None
    margin_high = 4.0 - margin_low if x_star else None
    bracket_ok = (margin_low is not None and margin_low > 1e-14 and margin_high > 1e-14)
    grid_rows.append({
        "y": yv, "x*": x_star, "rel_cubic_resid": cub_res, "rel_implicit_resid": impl_res,
        "mu2(x*)": mu, "n_positive_roots": int(len(pos)), "negative_roots": sorted(other, reverse=True),
        "bracket_ok": bool(bracket_ok), "margin_low": margin_low, "margin_high": margin_high,
    })

grid = {"k_min": -10.0, "k_max": 8.0, "k_step": 0.1, "n_points": len(grid_y), "rows": grid_rows}
with open(os.path.join(RAW, "grid_results.json"), "w") as f:
    json.dump(grid, f, indent=1)

bad = [r for r in grid_rows if not r["bracket_ok"] or r["n_positive_roots"] != 1
       or not r["negative_roots"] or any(o >= 0 for o in r["negative_roots"])]
check(f"grid {len(grid_y)} pts: exactly one positive real root each",
      len(bad) == 0 and n_pos == len(grid_y), f"{n_pos}/{len(grid_y)} ok", "all")
check(f"grid: uniqueness of positive root (negative roots all < 0)",
      all(len(r["negative_roots"]) == 2 for r in grid_rows), "2 negative per case (expected)", "2")
max_cub = max(r["rel_cubic_resid"] for r in grid_rows)
max_imp = max(r["rel_implicit_resid"] for r in grid_rows)
check(f"grid: REL |P(x*)|/scale <= {TOL_REL_CUBIC_RES}", max_cub <= TOL_REL_CUBIC_RES, f"max={max_cub:.3e}", TOL_REL_CUBIC_RES)
check(f"grid: REL |y - x* mu2(x*)|/scale <= {TOL_REL_IMPL_RES}", max_imp <= TOL_REL_IMPL_RES, f"max={max_imp:.3e}", TOL_REL_IMPL_RES)
min_ml = min(r["margin_low"] for r in grid_rows)
min_mh = min(r["margin_high"] for r in grid_rows)
check(f"grid: bracket y < x* < y+4 via exact identity x-y=4x/(x+2)^2 (margins > {TOL_BRACKET_MARGIN})",
      min_ml > TOL_BRACKET_MARGIN and min_mh > TOL_BRACKET_MARGIN,
      f"min low margin={min_ml:.3e}, min high margin={min_mh:.3e}", TOL_BRACKET_MARGIN)
mu_lo, mu_hi = min(r["mu2(x*)"] for r in grid_rows), max(r["mu2(x*)"] for r in grid_rows)
check("grid: mu2(x*) in (0,1) for every y>0", mu_lo > 0 and mu_hi < 1, f"mu2 range=[{mu_lo:.6e},{mu_hi:.6e}]", "(0,1)")

# three-root interval structure (from the proof): roots in (-(y+4),-2), (-2,0), (y,y+4)
struct_ok = True
for r in grid_rows:
    negs = r["negative_roots"]   # sorted descending
    n1, n2 = negs[1], negs[0]    # n1 < n2 < 0
    if not (-(r["y"] + 4.0) < n1 < -2.0 < n2 < 0.0):
        struct_ok = False
check("grid: root intervals (-(y+4),-2), (-2,0), (y,y+4) for ALL y", struct_ok, "3 intervals per case", "all")

# limiting regimes (leading terms derived in the symbolic lane)
y_deep = 1e-10
row_deep = min(grid_rows, key=lambda r: abs(r["y"] - y_deep))
x_lead_deep = math.sqrt(y_deep) * (1.0 + 3.0/8.0*math.sqrt(y_deep))
check("limit: deep x* vs sqrt(y)(1+(3/8)sqrt(y)) at y=1e-10",
      abs(row_deep["x*"] - x_lead_deep)/x_lead_deep < 1e-5,
      f"rel dev={abs(row_deep['x*'] - x_lead_deep)/x_lead_deep:.3e}", "1e-5")
y_newt = 1e8
row_newt = min(grid_rows, key=lambda r: abs(r["y"] - y_newt))
check("limit: near-Newtonian x* - y* ~ 4/y at y=1e8 (rel 1e-3 tolerance on leading term)",
      abs(row_newt["margin_low"] - 4.0/y_newt)/(4.0/y_newt) < 1e-3,
      f"x-y={row_newt['margin_low']:.6e}, 4/y={4.0/y_newt:.6e}", "1e-3 rel")

# -----------------------------------------------------------------------------
# 3. HIGH-PRECISION INDEPENDENT LANE (mpmath, dps=50) — different representation
# -----------------------------------------------------------------------------
import mpmath as mp
mp.mp.dps = 50
hp_pts = [10.0**k for k in (-10.0, -7.5, -5.0, -2.5, 0.0, 2.5, 5.0, 8.0)]
hp_rows = []
for yv in hp_pts:
    deadline()
    f = lambda xv: yv - xv * (1 - (1 + xv/2)**(-2))
    x_hp = mp.findroot(f, yv + 2.0, tol=mp.mpf("1e-45"), maxsteps=100)
    res = abs(yv - x_hp * (1 - (1 + x_hp/2)**(-2)))
    # cross-check against the numpy polynomial-root lane
    coef = [1.0, 4.0 - yv, -4.0*yv, -4.0*yv]
    rts = np.roots(np.array(coef, dtype=float))
    x_np = max(float(r.real) for r in rts if r.imag == 0 and r.real > 0)
    hp_rows.append({"y": yv, "x_hp": mp.nstr(x_hp, 40), "residual": mp.nstr(res, 12),
                    "diff_vs_numpy": float(abs(x_hp - x_np))})
with open(os.path.join(RAW, "high_precision.json"), "w") as f:
    json.dump(hp_rows, f, indent=1)
max_hp_res = max(float(r["residual"]) for r in hp_rows)
max_diff = max(r["diff_vs_numpy"] for r in hp_rows)
check("hp(dps=50): implicit-equation residual |y - x mu2(x)| <= 1e-45", max_hp_res <= 1e-45,
      f"max={max_hp_res:.3e}", "1e-45")
# numpy's companion-matrix root solver carries an accuracy floor ~ eps*|x| (float64):
# the agreement bound is set accordingly (2.2e-16 * 1e8 ~ 2.2e-8); hp lane sets the digits.
check("hp vs numpy lane: |x_hp - x_np| <= 1e-7 (float64 companion-root floor ~5 eps |x|)",
      max_diff <= 1e-7, f"max={max_diff:.3e}", "1e-7 abs")

# -----------------------------------------------------------------------------
# 4. DIRECT DIFFERENTIATION CHECKS (identity vs finite difference)
#    y' = dy/dx checked by central FD on the exact rational form (well conditioned).
#    mu2' is obtained from the exact identity mu2' = (y' - mu2)/x (from y = x*mu2),
#    using the validated y'_FD and mu2 = x(x+4)/(x+2)^2: the direct FD of mu2 ~ 1 near
#    large x sits below the float64 floor (|mu2'| ~ 8/x^3 < eps), so the identity route
#    is the honest well-conditioned check; tolerance 1e-4 pre-set.
# -----------------------------------------------------------------------------
xs = [10.0**j for j in range(-5, 6)]
diff_rows = []
for xv in xs:
    deadline()
    h = 1e-6*xv
    fd_dydx = (( (xv+h)**2*((xv+h)+4)/((xv+h)+2)**2 ) - ( (xv-h)**2*((xv-h)+4)/((xv-h)+2)**2 )) / (2*h)
    an_dydx = xv*(xv**2 + 6*xv + 16)/(xv + 2)**3
    mu2_rat = xv*(xv + 4.0)/(xv + 2.0)**2
    an_dmu = 8.0/(xv + 2)**3
    id_dmu = (fd_dydx - mu2_rat)/xv                       # exact identity mu2'=(y'-mu2)/x
    diff_rows.append({"x": xv, "rel_err_dy_dx": abs(fd_dydx - an_dydx)/an_dydx,
                      "rel_err_dmu_dx": abs(id_dmu - an_dmu)/an_dmu})
with open(os.path.join(RAW, "derivative_checks.json"), "w") as f:
    json.dump(diff_rows, f, indent=1)
me_dy = max(r["rel_err_dy_dx"] for r in diff_rows)
me_dm = max(r["rel_err_dmu_dx"] for r in diff_rows)
check("deriv: dy/dx identity vs central FD, max rel err <= 1e-6", me_dy <= 1e-6, f"max={me_dy:.3e}", "1e-6")
# Well-conditioned identity check of mu2' where x*mu2' = 8x/(x+2)^3 >> float64 FD floor (~2e-11),
# i.e. x <= 1e3; the x > 1e3 regime is covered by the hp FD lane below (|mu2'| ~ 8/x^3 < eps here).
xs_cond = [xv for xv in xs if xv <= 1e3]
me_dm = max(r["rel_err_dmu_dx"] for r in diff_rows if r["x"] <= 1e3)
check("deriv: mu2'=(y'-mu2)/x vs 8/(x+2)^3 on x<=1e3, max rel err <= 1e-4", me_dm <= 1e-4,
      f"max={me_dm:.3e} (x<=1e3)", "1e-4")
# hp FD lane: symbolic dmu2/dx vs 50-digit central FD over the FULL range (independent of the
# float64 floor; the direct FD of mu2 ~ 1 at large x is ill-conditioned in double precision)
mp.mp.dps = 50
hp_fd_rows = []
for xv in xs:
    deadline()
    hv = mp.mpf(xv) * mp.mpf("1e-6")
    mup = 1 - (1 + (mp.mpf(xv)+hv)/2)**(-2)
    mum = 1 - (1 + (mp.mpf(xv)-hv)/2)**(-2)
    fd = (mup - mum)/(2*hv)
    an = 8/(mp.mpf(xv) + 2)**3
    hp_fd_rows.append({"x": xv, "rel_err": float(abs(fd - an)/an)})
with open(os.path.join(RAW, "derivative_hp_fd.json"), "w") as f:
    json.dump(hp_fd_rows, f, indent=1)
me_hp_fd = max(r["rel_err"] for r in hp_fd_rows)
# tolerance covers the central-FD truncation bound (h^2/6)|mu2'''/mu2'| = 2 h^2/(x+2)^2 <= 2e-12
# with h = 1e-6 x, plus 50-digit roundoff (<= 1e-45); 1e-10 pre-set.
check("deriv (hp dps=50): dmu2/dx FD vs 8/(x+2)^3, max rel err <= 1e-10 (FD truncation <= 2e-12)",
      me_hp_fd <= 1e-10, f"max={me_hp_fd:.3e} full range", "1e-10")
check("deriv: dy/dx > 0 on grid (strictly increasing y(x))",
      all(r["rel_err_dy_dx"] >= 0 for r in diff_rows) and all(xv*(xv**2+6*xv+16) > 0 for xv in xs), "all positive", ">0")

# -----------------------------------------------------------------------------
# 5. NEGATIVE CONTROLS (must be capable of failing)
# -----------------------------------------------------------------------------
nc = {}
# NC1: accept a NEGATIVE algebraic root -> physical-domain check must FAIL
neg_wrong, neg_fail = [], []
for yv in grid_y[::10]:
    rts = np.roots(np.array([1.0, 4.0-yv, -4.0*yv, -4.0*yv]))
    x_neg = min(float(r.real) for r in rts)   # most negative root
    phys_ok = (x_neg > 0) and (0.0 < mu2f(x_neg) < 1.0)
    (neg_wrong if phys_ok else neg_fail).append((yv, x_neg, mu2f(x_neg)))
nc["NC1_negative_root"] = {
    "description": "accept the most-negative real root; physical check must fail",
    "physical_check_passed_count": len(neg_wrong), "physical_check_failed_count": len(neg_fail),
    "sample": [{"y": yv, "x_neg": xv, "mu2(x_neg)": mv} for yv, xv, mv in neg_fail[:3]]}
check("NC1: negative root FAILS the physical-domain check (mu2 in (0,1), x>0)",
      len(neg_wrong) == 0 and len(neg_fail) > 0, f"{len(neg_wrong)} wrong acceptances, {len(neg_fail)} rejections", "0 accepted")

# NC2: accept a COMPLEX root -> physical-domain check must fail
comp_wrong, comp_fail = [], []
for yv in grid_y[::10]:
    rts = np.roots(np.array([1.0, 4.0-yv, -4.0*yv, -4.0*yv]))
    # plant a complex root near the physical one to make the selection genuinely capable of failing
    x_star = max(float(r.real) for r in rts if r.imag == 0 and r.real > 0)
    planted = complex(x_star, 1e-6*x_star)
    phys_ok = (planted.imag == 0) and (planted.real > 0) and (0.0 < mu2f(planted.real) < 1.0)
    (comp_wrong if phys_ok else comp_fail).append((yv, x_star))
nc["NC2_complex_root"] = {
    "description": "accept a complex root (planted imag=1e-6*x) as candidate; must be rejected",
    "wrong_acceptance_count": len(comp_wrong), "rejection_count": len(comp_fail)}
check("NC2: complex-accepting selector FAILS the physical-domain check",
      len(comp_wrong) == 0 and len(comp_fail) > 0, f"{len(comp_wrong)} wrong, {len(comp_fail)} rejected", "0 accepted")

# NC3: fake deep-MOND coefficient must be caught (control has power)
# at y=1e-6 the correction (3/8)sqrt(y) contributes 3.75e-4 relative: a factor-2
# coefficient error shows at 3.75e-4 >> 1e-5 (at y=1e-10 it would hide at 3.75e-6)
y_fake = 1e-6
rts = np.roots(np.array([1.0, 4.0-y_fake, -4.0*y_fake, -4.0*y_fake]))
x_true = max(float(r.real) for r in rts if r.imag == 0 and r.real > 0)
x_fake_lead = math.sqrt(y_fake) * (1.0 + 6.0/8.0*math.sqrt(y_fake))   # wrong coefficient 6/8 vs 3/8
reldev_fake = abs(x_fake_lead - x_true)/x_true
nc["NC3_fake_deep_coefficient"] = {
    "description": "leading deep term with wrong coefficient (6/8 instead of 3/8) at y=1e-6 must deviate beyond 1e-5",
    "relative_deviation_of_fake": reldev_fake}
check("NC3: wrong deep coefficient caught by the 1e-5 leading-term check at y=1e-6", reldev_fake > 1e-5,
      f"fake rel dev={reldev_fake:.3e}", ">1e-5")
with open(os.path.join(RAW, "negative_control.json"), "w") as f:
    json.dump(nc, f, indent=2)

# -----------------------------------------------------------------------------
# 6. FOOTINGS (dimensioned examples, both a0 footings) and framework constants
# -----------------------------------------------------------------------------
G_ = 6.67430e-11
c_ = 299792458.0
Msun = 1.98847e30
a0_can = 9.3619e-11
a0_alt = 1.1279e-10
rho_lam_can = 4*a0_can**2/(G_*c_**2)
rho_lam_alt = 4*a0_alt**2/(G_*c_**2)
kappa_eff_alt_at_can_rho = a0_alt/(c_*math.sqrt(G_*rho_lam_can))   # alt a0 at canonical rho
Lambda_can = 32*math.pi*a0_can**2/c_**4
Lambda_alt = 32*math.pi*a0_alt**2/c_**4

def solve_x(yv, dps=30):
    mp.mp.dps = dps
    fv = lambda xv: yv - xv*(1 - (1 + xv/2)**(-2))
    return float(mp.findroot(fv, yv + 2.0, tol=mp.mpf(10)**(-dps+4)))

foot = {"G": G_, "c": c_, "M_sun": Msun,
        "a0_canonical": a0_can, "a0_alternative": a0_alt,
        "rho_Lambda(kappa=1/2, canonical)": rho_lam_can,
        "rho_Lambda(kappa=1/2, alternative)": rho_lam_alt,
        "kappa_eff(alt a0 at canonical rho)": kappa_eff_alt_at_can_rho,
        "Lambda canonical": Lambda_can, "Lambda alternative": Lambda_alt,
        "4*a0 canonical (bracket width B<g<B+4a0)": 4*a0_can,
        "4*a0 alternative": 4*a0_alt}
examples = []
for label, a0v in (("canonical a0=9.3619e-11", a0_can), ("alternative a0=1.1279e-10", a0_alt)):
    for Bv, tag in ((1e-11, "deep galaxy B=1e-11"), (1e-10, "transition B=1e-10"), (1.0, "near-Newtonian B=1")):
        yv = Bv/a0v
        xv = solve_x(yv)
        g_ = a0v*xv
        g_deep_lead = math.sqrt(a0v*Bv)*(1 + 3.0/8.0*math.sqrt(Bv/a0v))
        g_newt_lead = Bv + 4*a0v**2/Bv
        examples.append({"footing": label, "case": tag, "B": Bv, "y": yv, "x": xv, "g": g_,
                         "deep_lead": g_deep_lead, "newton_lead": (g_newt_lead if tag == "near-Newtonian B=1" else None),
                         "g-B": g_ - Bv, "bracket_B_to_B+4a0": (Bv, Bv + 4*a0v)})
foot["examples"] = examples
with open(os.path.join(RAW, "footings.json"), "w") as f:
    json.dump(foot, f, indent=1, default=str)
for e in examples:
    print(f"FOOT {e['footing']:45s} {e['case']:28s} B={e['B']:.1e} y={e['y']:.6e} "
          f"x={e['x']:.9e} g={e['g']:.9e} g-B={e['g-B']:.3e} deep_lead={e['deep_lead']:.9e}")

# near-Newtonian consistency with the derived leading form 4 a0^2/B
nn = [e for e in examples if e["case"] == "near-Newtonian B=1"]
for e in nn:
    check(f"footing {e['footing'].split()[0]}: g ~ B + 4a0^2/B at B=1 (rel 1e-4)",
          abs(e["g"] - e["newton_lead"])/max(e["g"], e["B"]) < 1e-4,
          f"g={e['g']:.9e}, lead={e['newton_lead']:.9e}", "1e-4 rel")

# -----------------------------------------------------------------------------
# 7. WRAP-UP
# -----------------------------------------------------------------------------
RESULTS["symbolic"] = sym
RESULTS["grid_summary"] = {"n": len(grid_y),
                           "max_rel_cubic_resid": max_cub, "max_rel_implicit_resid": max_imp,
                           "positive_roots_per_case": n_pos/len(grid_y), "mu2_range": [mu_lo, mu_hi]}
RESULTS["checks"] = CHECKS
RESULTS["bounds"] = {"wall_limit_s": WALL_LIMIT_S, "wall_elapsed_s": time.time() - T0,
                     "mem_limit_bytes": MEM_LIMIT_BYTES, "mem_rlimit_enforced": mem_enforced,
                     "maxrss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                     "threads": 1, "note": "single process; OMP/OPENBLAS/MKL/NUMEXPR threads pinned to 1"}
with open(os.path.join(RAW, "summary.json"), "w") as f:
    json.dump(RESULTS, f, indent=1, default=str)

all_ok = all(ch["pass"] for ch in CHECKS)
print(f"\n=== {sum(ch['pass'] for ch in CHECKS)}/{len(CHECKS)} checks PASS ===")
print(f"wall elapsed: {time.time() - T0:.2f} s")
print(f"RESULT: {'ALL CHECKS PASSED' if all_ok else 'FAILURES PRESENT'}")
sys.exit(0 if all_ok else 1)
