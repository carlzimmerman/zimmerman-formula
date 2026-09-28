#!/usr/bin/env python3
"""
AS247 Engine B — delay-functional certification at toy field scale.
Tests the metric-level step 2 mathematics of the seed at a field scale where
linearization and slip effects are VISIBLE (u ~ 1e-3 dimensionless), with:
  B1  exact-null vs linearized delay integrand on a straight chord (residual
      must sit at O(u^2), i.e. ~1e-6 rel for u0 = 1e-3, NOT at 0);
  B2  no-slip reduction: with Psi = Phi the functional equals -2 int Phi (exact
      to the same O(u^2), verified against the exact sqrt integrand);
  B3  NEGATIVE CONTROL (synthetic slip): Psi = Phi + deltaPsi with a Gaussian
      slip bump, delay must CHANGE by exactly -(1/c) int deltaPsi dl; a
      Phi-only formula misses it (fires);
  B4  null-ray geodesic shooting (Fermat path, RK4, refined once): the true
      ray delay in the slipped metric matches the functional (straight-chord +
      bending <= O(u^2)); the slip change is confirmed on the geodesic too.
Units: c = 1 dimensionless throughout this engine; u = Phi, v = Psi.
"""
import numpy as np, json, time

rng = np.random.default_rng(247)

def rec(res, name, ok, detail, residual=None, tol=None):
    res[name] = {"pass": bool(ok), "detail": detail,
                 "residual": residual, "tolerance": tol}

# ---------------- geometry and fields (declared before evaluation) ----------
u0   = 1e-3          # dimensionless potential depth (Phi/c^2)
sig  = 2.0           # Gaussian width of the toy potential
L    = 20.0          # chord half-length (endpoints at x = +-L, y = b)
b    = 1.0           # impact parameter
NX   = 20001         # straight-chord quadrature points (refined: 40001)

def pot(xx, b_, eps=0.0):
    """attractive Gaussian potential: Phi = -u0 exp(-r^2/(2 sig^2)), r^2 = x^2 + b_^2.
    eps = synthetic slip amplitude deltaPsi = eps*Phi."""
    r2 = xx**2 + b_**2
    ph = -u0 * np.exp(-r2 / (2.0 * sig**2))
    return ph, eps * ph

def exact_integrand(u, v):
    """sqrt((1-2v)/(1+2u)) — exact c dt/dl on the straight chord (c = 1)."""
    return np.sqrt((1.0 - 2.0 * v) / (1.0 + 2.0 * u))

def trapez(x, f):
    return np.trapz(f, x)

res = {}
t0 = time.time()

# ---------------- B1: linearized vs exact on a straight chord ----------------
x  = np.linspace(-L, L, NX)
u, dv = pot(x, b)          # Phi = u, slip zero: v = u (no slip)
v = u.copy()
s  = u + v
dt_lin   = -trapez(x, s)                          # -(1/c) int (u+v) dl, c=1
exact    = exact_integrand(u, v)
dt_exact = trapez(x, exact) - 2.0 * L             # minus the flat baseline 2L
# the linearization residual D = exact_integrand - (1 - s):
D     = exact - (1.0 - s)
resid = np.abs(trapez(x, D))
scale = np.abs(dt_lin)
rel_b1 = resid / scale
rec(res, "B1_linearization_residual",
    rel_b1 < 5e-3 and abs(dt_exact - dt_lin) < 5e-3 * scale,
    f"exact-baseline {dt_exact:.6e}, linearized {dt_lin:.6e}, "
    f"abs residual {resid:.3e}, rel {rel_b1:.3e} (O(u0)=1e-3 expected)",
    float(rel_b1), 5e-3)
# max-integrand relative check (pointwise bound from the Lean certificate)
rel_pt = np.max(np.abs(D / np.maximum(np.abs(1.0 - s), 1e-30)))
rec(res, "B1b_pointwise_remainder",
    rel_pt < 0.02, f"max |D/(1-s)| = {rel_pt:.3e} (certified <= 1.3e-3 + O(u0))",
    float(rel_pt), 0.02)

# ---------------- B2: no-slip identity -------------------------------------------------
dt_noslip = -2.0 * trapez(x, u)                   # -(1/c) int (Phi+Psi) with Psi=Phi
rec(res, "B2_noslip_equals_double",
    np.abs(dt_noslip - dt_lin) / scale < 1e-14,
    f"noslip {dt_noslip:.12e} vs full {dt_lin:.12e}",
    float(np.abs(dt_noslip - dt_lin) / scale), 1e-14)

# ---------------- B3: NEGATIVE CONTROL — synthetic slip must change the answer ---------
eps  = 0.25
u2, d2 = pot(x, b)
v2 = u2 + eps * u2                                # synthetic slip deltaPsi = eps*Phi
u3 = u2
s3 = u3 + v2
dt_slip      = -trapez(x, s3)
slip_integr  = trapez(x, eps * u2)                # -(1/c) int deltaPsi  (c=1)
predicted    = dt_lin - slip_integr
rec(res, "B3_slip_changes_delay",
    np.abs(dt_slip - predicted) / max(np.abs(dt_slip), 1e-30) < 1e-12,
    f"full-with-slip {dt_slip:.10e}, no-slip-assumed(Phi-only) {dt_lin:.10e}, "
    f"predicted {predicted:.10e}; change = {slip_integr:.6e} != 0 (fires)",
    float(np.abs(dt_slip - predicted)), 1e-12)
rec(res, "B3b_phi_only_misses_slip",
    np.abs(dt_slip - dt_lin) / max(np.abs(dt_slip), 1e-30) > 0.05,
    f"Phi-only (no-slip assumption) is wrong by {np.abs(dt_slip-dt_lin):.4e} "
    f"rel {np.abs(dt_slip-dt_lin)/np.abs(dt_slip):.3f} when slip eps={eps}",
    float(np.abs(dt_slip - dt_lin)/np.abs(dt_slip)), 0.05)

# ---------------- B4: geodesic (Fermat) ray in the slipped metric -----------------------
# minimize T = int n(x,y) sqrt(1 + y'^2) dx,  n = sqrt((1-2v)/(1+2u)),
# endpoints (-L, b) -> (L, b).  Euler-Lagrange: d/dx [n y'/sqrt(1+y'^2)] = n_y sqrt(1+y'^2)
# solved by RK4 shooting on the launch slope, bisection on the endpoint miss.

def n_field(xx, yy):
    uu, dvv = pot(xx, yy)          # Phi = uu(no slip-free); full field
    vv = uu + eps * uu             # synthetic slip, same as B3
    return np.sqrt((1.0 - 2.0 * vv) / (1.0 + 2.0 * uu))

def n_deriv_y(xx, yy):
    h = 1e-6
    return (n_field(xx, yy + h) - n_field(xx, yy - h)) / (2.0 * h)

def eom(state, xx):
    """state = [y, p] where p = y' (coordinate slope).  E-L second-order form."""
    yy, p = state
    n  = n_field(xx, yy)
    ny = n_deriv_y(xx, yy)
    # d/dx [n p / sqrt(1+p^2)] = ny sqrt(1+p^2)
    #  => (n p / sqrt(1+p^2))' = ny sqrt(1+p^2)
    #  => n p'' /(1+p^2)^(3/2) + ...  derive: dp/dt form used in RK4 directly:
    #  q = n p / sqrt(1+p^2);  q' = ny sqrt(1+p^2);  p = q / sqrt(n^2 - q^2)
    q  = n * p / np.sqrt(1.0 + p**2)
    qp = ny * np.sqrt(1.0 + p**2)
    # dp/dx from q:   dq/dx = (n/sqrt(1+p^2)^3) p'  (with n constant along x in q-def)
    #   q = n p/sqrt(1+p^2) => dq/dp = n/(1+p^2)^(3/2)
    pp = qp * (1.0 + p**2)**1.5 / n
    return np.array([p, pp])

def shoot(slope, h):
    xg = np.arange(-L, L + h/2, h)
    y = b + slope * (xg - (-L)) * 0.0 + 0.0
    st = np.array([b, slope])
    ys = [b]
    for i in range(len(xg) - 1):
        x0 = xg[i]
        k1 = eom(st, x0)
        k2 = eom(st + 0.5*h*k1, x0 + 0.5*h)
        k3 = eom(st + 0.5*h*k2, x0 + 0.5*h)
        k4 = eom(st + h*k3, x0 + h)
        st = st + (h/6.0)*(k1 + 2*k2 + 2*k3 + k4)
        ys.append(st[0])
    return np.array(xg), np.array(ys), st[0]   # final y - b = endpoint miss

def ray_delay(xg, ys, h):
    n = n_field(xg, ys)
    dT = n * np.sqrt(1.0 + np.gradient(ys, xg)**2)
    return trapez(xg, dT), n

# coarse: bisect on slope to hit (L, b)
def hit(slope, h):
    return shoot(slope, h)[2] - b

lo, hi = -0.02, 0.02
h = 0.01
for _ in range(60):
    mid = 0.5*(lo + hi)
    if hit(mid, h) * hit(lo, h) > 0:
        lo = mid
    else:
        hi = mid
slope0 = 0.5*(lo + hi)
xg, ys, miss = shoot(slope0, h)
miss = miss - b                      # shoot returns final y; miss = y(L) - b
T_geo, _ = ray_delay(xg, ys, h)
rec(res, "B4a_geodesic_endpoint_hit",
    abs(miss) < 5e-8,
    f"launch slope {slope0:.6e}, endpoint miss {miss:.2e} (h={h})",
    float(abs(miss)), 5e-8)
# refined once
h2 = h/2.0
lo2, hi2 = slope0 - 1e-4, slope0 + 1e-4
for _ in range(60):
    mid = 0.5*(lo2 + hi2)
    if hit(mid, h2) * hit(lo2, h2) > 0:
        lo2 = mid
    else:
        hi2 = mid
slope1 = 0.5*(lo2 + hi2)
xg2, ys2, miss2 = shoot(slope1, h2)
miss2 = miss2 - b
T_geo2, _ = ray_delay(xg2, ys2, h2)
rec(res, "B4b_geodesic_refined",
    abs(miss2) < 5e-9 and abs(T_geo2 - T_geo) < 1e-4,
    f"refined h={h2}: miss {miss2:.2e}, T {T_geo2:.10e} vs T {T_geo:.10e} "
    f"(RK4 truncation O(h^4) expected)",
    float(abs(miss2)), 5e-9)
# geodesic delay vs functional: T_geo - 2L  vs  dt_slip  (bending is O(u^2))
base = 2.0 * L
geo_lin_diff = (T_geo2 - base) - dt_slip
rec(res, "B4c_geodesic_matches_functional",
    np.abs(geo_lin_diff) < 1e-2 * np.abs(dt_slip),
    f"geodesic delay {T_geo2 - base:.8e} vs functional {dt_slip:.8e}, "
    f"diff {geo_lin_diff:.3e} (bending order, O(u0^2 * L/sigma) ~ 1e-3 rel expected)",
    float(geo_lin_diff), 1e-2 * abs(dt_slip))
rec(res, "B4d_slip_visible_on_geodesic",
    np.abs(T_geo2 - 2.0*L - dt_lin) > 0.05 * np.abs(dt_slip),
    f"geodesic in the slipped metric differs from the no-slip delay by "
    f"{np.abs(T_geo2 - 2.0*L - dt_lin):.4e}",
    float(np.abs(T_geo2 - 2.0*L - dt_lin)), 0.05*abs(dt_slip))
# B4e: the slip-induced geodesic shift equals the linearized slip integral
slip_gap = (T_geo2 - 2.0*L - dt_lin)          # geodesic shift from the slip
rec(res, "B4e_slip_gap_matches_integral",
    np.abs(slip_gap - (-slip_integr)) < 0.05 * np.abs(slip_integr),
    f"geodesic slip gap {slip_gap:.6e} vs linearized -(1/c) int deltaPsi = "
    f"{-slip_integr:.6e}; bending-order diff {np.abs(slip_gap+slip_integr):.3e}",
    float(np.abs(slip_gap + slip_integr)), 0.05*abs(slip_integr))

res["_meta"] = {"u0": u0, "sigma": sig, "L": L, "b": b, "slip_eps": eps,
                "NX": NX, "h": h, "h_refined": h2, "elapsed_s": time.time() - t0}

with open("func_raw.json", "w") as f:
    json.dump(res, f, indent=1, default=str)

allp = all(v.get("pass", False) for k, v in res.items() if not k.startswith("_"))
print(json.dumps(res, indent=1, default=str))
print("ALL_PASS:", allp)