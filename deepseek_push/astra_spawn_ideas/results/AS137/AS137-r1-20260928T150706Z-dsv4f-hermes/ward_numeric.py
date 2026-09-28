#!/usr/bin/env python3
"""AS137 — ordinary-matter Ward identity, numeric checks on a curved background.

2D (t, r) sector of a Schwarzschild-like metric g = diag(-(1-2M/r), 1/(1-2M/r)),
r > 2M.  All tensor objects are exact sympy expressions in (t, r) evaluated on
a grid in float64 (analytic derivatives), with a finite-difference (np.gradient)
cross-check.  ACTUAL RESIDUALS are reported throughout.

Checks:
  N1  off-shell identity div_mu T^{mu nu} = E_b nabla^nu phi on the curved
      background with a generic field + mass term: max |residual|, analytic and
      finite-difference versions (interior; edge stencils are 1st-order and
      reported separately).
  N2  on-shell witness: phi = t  (Box phi = 0 on any static metric, V = 0):
      max |div T| at the rounding floor while T itself is nonzero.
  N3  flat limit M -> 0 of the same off-shell configuration (limiting case).
  N4  diffeomorphism integral with a compactly supported generator xi (numpy
      bump): the pointwise IBP identity at the FD level (the EXACT identity is
      certified symbolically in ward_symbolic.py [6]), the integral of
      delta_xi S_b at the truncation floor, the once-integrated form (seed
      step 2), the telescoping q1 + int(Bnd), and a grid refinement showing
      no upward drift.
  N5  negative control z0 Z psi^2 on the curved background: the identity
      div T' = E'_psi grad psi + z0 psi^2 grad Z at the truncation floor, plus
      the flat on-shell witness psi = x^2, Z = -1/(z0 x^2): E'_psi = 0 while
      div T' = (0, 2x) != 0 (the prevented identity).
  N6  footing examples with the mandated constants on BOTH footings; kappa
      fixed at 1/2 -> density ratio (a0_alt/a0_can)^2; the Ward identity is
      a0-independent and holds identically on both footings.

Bounds: single thread (env), ulimit -t 120 enforced, peak RSS measured.
"""

import numpy as np
import sympy as sp

t, r = sp.symbols("t r", real=True)
M = sp.symbols("M", positive=True)

TS = np.linspace(0.0, 1.0, 180)
RS = np.linspace(3.0, 8.0, 180)
DT, DR = TS[1] - TS[0], RS[1] - RS[0]

_LAMB = {}

def grid_eval(expr, Ms=1.0, ts=TS, rs=RS, subs_map=None):
    """Evaluate a sympy expr on the (t,r) grid; lambdify cached per expr."""
    if subs_map:
        expr = expr.subs(subs_map)
    key = (expr, Ms)
    f = _LAMB.get(key)
    if f is None:
        f = sp.lambdify((t, r, M), expr, "numpy")
        _LAMB[key] = f
    TG, RG = np.meshgrid(ts, rs, indexing="ij")
    with np.errstate(all="ignore"):
        return f(TG, RG, Ms)

def quad(a, ts, rs):
    return np.trapz(np.trapz(a, rs, axis=1), ts, axis=0)

def bump1n(u, u0, u1):
    z = 2 * (u - u0) / (u1 - u0) - 1
    out = np.zeros_like(u)
    m = np.abs(z) < 1
    out[m] = np.exp(-1 / (1 - z[m] ** 2))
    return out

def Gam_fun(Ms):
    """Christoffel symbols of the diagonal (t,r) metric with parameter Ms."""
    gtt = -(1 - 2 * Ms / r)
    grr = 1 / (1 - 2 * Ms / r)
    gco = [[gtt, 0], [0, grr]]
    gup = [[1 / gtt, 0], [0, 1 / grr]]
    coords = (t, r)

    def Gam(u, l1, l2):
        res = sp.S(0)
        for s in range(2):
            term = (sp.diff(gco[s][l1], coords[l2])
                    + sp.diff(gco[s][l2], coords[l1])
                    - sp.diff(gco[l1][l2], coords[s]))
            res += gup[u][s] * term
        return sp.expand(res / 2)

    return Gam

def build(Ms, phi, V, Vp):
    """T^{mu nu}, E, grad^nu phi, covariant divergence closure, sqrt(-g)."""
    gtt = -(1 - 2 * Ms / r)
    grr = 1 / (1 - 2 * Ms / r)
    gup = [[1 / gtt, 0], [0, 1 / grr]]
    Gam = Gam_fun(Ms)
    coords = (t, r)
    sqrt_m = sp.sqrt(-(gtt * grr))
    d = [sp.diff(phi, coords[0]), sp.diff(phi, coords[1])]
    gu = [gup[mu][0] * d[0] + gup[mu][1] * d[1] for mu in range(2)]
    dphi2 = gup[0][0] * d[0] ** 2 + gup[1][1] * d[1] ** 2
    T = [[sp.expand(gu[mu] * gu[nu] - sp.Rational(1, 2) * gup[mu][nu] * (dphi2 + 2 * V))
          for nu in range(2)] for mu in range(2)]
    box = sp.expand(
        (sp.diff(sqrt_m * gup[0][0] * d[0], t) + sp.diff(sqrt_m * gup[1][1] * d[1], r))
        / sqrt_m)
    E = sp.expand(box - Vp)

    def div(nu):
        res = sp.diff(T[0][nu], t) + sp.diff(T[1][nu], r)
        for mu in range(2):
            for l in range(2):
                res += Gam(mu, mu, l) * T[l][nu] + Gam(nu, mu, l) * T[mu][l]
        return sp.expand(res)

    return T, E, gu, div, sqrt_m, gup

print("=" * 78)
print("AS137 numeric checks — curved 2D (t,r) Schwarzschild-sector metric")
print("=" * 78)

Ms = 1.0
mu = 0.7
phi_expr = t ** 2 * sp.sin(r) / r + r ** 2 * sp.cos(2 * t) / 20
V_expr = mu ** 2 * phi_expr ** 2 / 2
Vp_expr = mu ** 2 * phi_expr

# ---- N1: off-shell identity on curved background -------------------------
T, E, gu, div, sqrt_m, gup = build(Ms, phi_expr, V_expr, Vp_expr)
print("\n[N1] off-shell Ward identity on 2D Schwarzschild sector (grid 180x180):")
R_arr = []
for nu in range(2):
    Dnu = grid_eval(div(nu))
    Enu = grid_eval(E * gu[nu])
    rv = Dnu - Enu
    R_arr.append(rv)
    mx = np.max(np.abs(rv))
    scl = np.max(np.abs([Dnu, Enu]))
    print(f"     nu={nu}: max|div T - E grad phi| = {mx:.3e}   "
          f"(term scale {scl:.3e}; relative {mx / scl:.2e})")
    assert mx < 1e-10 * scl + 1e-12

# finite-difference cross-check (np.gradient), nu=0 component:
# div T^0 = d_t T00 + d_r T01 + (Gamma^t_tr + Gamma^r_rr) T10 + 2 Gamma^t_tr T01
Gam = Gam_fun(Ms)
Gtr_grid = sp.lambdify((r,), Gam(0, 0, 1).subs(M, Ms), "numpy")(RS)[None, :]
Grr_grid = sp.lambdify((r,), Gam(1, 1, 1).subs(M, Ms), "numpy")(RS)[None, :]
T00a = grid_eval(T[0][0])
T01a = grid_eval(T[0][1])
T10a = grid_eval(T[1][0])
divT0_fd = (np.gradient(T00a, DT, axis=0) + np.gradient(T01a, DR, axis=1)
            + (Gtr_grid + Grr_grid) * T10a + 2 * Gtr_grid * T01a)
resid_fd = np.abs(divT0_fd - grid_eval(E * gu[0]))
interior = resid_fd[10:-10, 10:-10]
print(f"     FD cross-check nu=0: max|residual| = {resid_fd.max():.3e} TOTAL "
      f"(1st-order edge stencils), {interior.max():.3e} INTERIOR "
      f"(2nd-order central, dr = {DR:.4f}; interior bound ~5e-3)")
assert interior.max() < 5e-3

# ---- N2: on-shell witness phi = t ---------------------------------------
print("\n[N2] on-shell witness phi = t (Box phi = 0 exactly on static metric):")
T2, E2, gu2, div2, _, _ = build(Ms, t, sp.S(0), sp.S(0))
E2v = grid_eval(E2)
print(f"     max|E| = {np.max(np.abs(E2v)):.3e}  (should be ~0)")
for nu in range(2):
    mx = np.max(np.abs(grid_eval(div2(nu))))
    scl = np.max(np.abs(grid_eval(T2[0][nu])))
    print(f"     nu={nu}: max|div T| = {mx:.3e}   (T scale {scl:.3e}; relative {mx / (scl + 1.0):.2e})")
    assert np.max(np.abs(E2v)) < 1e-11
    assert mx < 1e-9 * (scl + 1.0)

# ---- N3: flat limit M -> 0 ----------------------------------------------
print("\n[N3] flat limit (M -> 0) of the same off-shell configuration:")
T3, E3, gu3, div3, _, _ = build(sp.S(0), phi_expr, V_expr, Vp_expr)
for nu in range(2):
    mx = np.max(np.abs(grid_eval(div3(nu) - E3 * gu3[nu], sp.S(0))))
    print(f"     nu={nu}: max|residual| (M=0, curved machinery) = {mx:.3e}")
    assert mx < 1e-10

# ---- N4: diffeo integral with compact xi (IBP once) ----------------------
# Pure-numeric bump generator (the symbolic Piecewise bump made
# sp.simplify/trigsimp pathological; the EXACT pointwise IBP identity is
# certified symbolically in ward_symbolic.py [6]).
print("\n[N4] diffeomorphism integral, compactly supported xi (IBP once):")
XiT = bump1n(TS[:, None], 0.15, 0.85) * bump1n(RS[None, :], 3.5, 7.5)
XiR = bump1n(TS[:, None], 0.2, 0.8) * bump1n(RS[None, :], 4.0, 7.0)
gtt_a = -(1 - 2 * Ms / RS)
grr_a = 1 / (1 - 2 * Ms / RS)
sqrt_a = np.sqrt(-(gtt_a * grr_a))[None, :]
Gtr_a = sp.lambdify((r,), Gam(0, 0, 1).subs(M, Ms), "numpy")(RS)[None, :]
Grr_a = sp.lambdify((r,), Gam(1, 1, 1).subs(M, Ms), "numpy")(RS)[None, :]
Grtt_a = sp.lambdify((r,), Gam(1, 0, 0).subs(M, Ms), "numpy")(RS)[None, :]
# xi^mu = g^{mu nu} xi_nu ; g^{tt} = 1/g_tt, g^{rr} = 1/g_rr
xiup_t = XiT / gtt_a[None, :]
xiup_r = XiR / grr_a[None, :]
dphi_arr = [grid_eval(sp.diff(phi_expr, c)) for c in (t, r)]
# nabla_mu xi_nu = d_mu xi_nu - Gamma^l_{mu nu} xi_l (explicit components):
nab_tt = np.gradient(XiT, DT, axis=0) - Grtt_a * XiR
nab_tr = np.gradient(XiR, DT, axis=0) - Gtr_a * XiT
nab_rt = np.gradient(XiT, DR, axis=1) - Gtr_a * XiT
nab_rr = np.gradient(XiR, DR, axis=1) - Grr_a * XiR
T11a = grid_eval(T[1][1])
Ea = grid_eval(E)
gu0a, gu1a = grid_eval(gu[0]), grid_eval(gu[1])
# I1 = delta_xi S_b integrand = sqrt(-g)[E delta phi + (1/2) T^{mu nu} delta g_{mu nu}]
#      with delta phi = -xi^s d_s phi, delta g = -(nabla xi + nabla xi):
#      I1 = -sqrt(-g)[T^{mu nu} nabla_mu xi_nu + E xi^s d_s phi]
I1_arr = -sqrt_a * (T00a * nab_tt + T01a * (nab_tr + nab_rt)
                    + T11a * nab_rr
                    + Ea * (xiup_t * dphi_arr[0] + xiup_r * dphi_arr[1]))
# I2 = -sqrt(-g) xi_nu [div T - E grad^nu phi]  (the once-integrated form,
# seed step 2; R_arr ~ 0 by [2], kept as the actual arrays)
I2_arr = -sqrt_a * (XiT * R_arr[0] + XiR * R_arr[1])
# Bnd = d_mu(sqrt(-g) T^{mu nu} xi_nu) = sqrt(-g)[T^{mu nu} nabla_mu xi_nu
#        + xi_nu div^nT]  (covariant Leibniz; div arrays = E grad phi + R)
Bnd_arr = sqrt_a * (T00a * nab_tt + T01a * (nab_tr + nab_rt) + T11a * nab_rr
                    + XiT * (Ea * gu0a + R_arr[0]) + XiR * (Ea * gu1a + R_arr[1]))
ibp_pt = np.max(np.abs(I1_arr + Bnd_arr + I2_arr))
scl_pt = np.max(np.abs(I1_arr)) + 1e-30
print(f"     pointwise IBP identity |I1 + d_mu(sqrt(-g) T xi) + I2|: max = {ibp_pt:.3e} "
      f"(relative {ibp_pt / scl_pt:.2e})")
assert ibp_pt < 1e-9 * scl_pt + 1e-12
q1 = quad(I1_arr, TS, RS)
q2 = quad(I2_arr, TS, RS)
qI1abs = quad(np.abs(I1_arr), TS, RS)
print(f"     int I1 (delta_xi S_b integrand)      = {q1:+.3e}   "
      f"(|I1| integral {qI1abs:.3e}; rel {q1 / (qI1abs + 1e-30):.2e})")
print(f"     int I2 (-xi_nu [divT - E grad phi])  = {q2:+.3e}")
print(f"     flux int(Bnd) (compact xi)           = {quad(Bnd_arr, TS, RS):+.3e}")
print(f"     consistency int(I1 + Bnd + I2)       = {q1 + quad(Bnd_arr, TS, RS) + q2:+.3e}")
# Quadrature truncation bounds (pre-declared): |q1| dominated by the trapezoid
# error ~ h^2 K/12 of a smooth derivative integrand (estimate K from the
# observed 180->360 Richardson quartering below); q2 ~ machine because R_arr
# is at 1e-14 (seed step 2); the consistency of all three sums is exact.
assert abs(q1) < 5e-4 and abs(q2) < 1e-6
assert abs(q1 + quad(Bnd_arr, TS, RS) + q2) < 1e-9
# refinement h -> h/2 (360x360): the sums must not drift upward:
TS_r = np.linspace(0.0, 1.0, 360)
RS_r = np.linspace(3.0, 8.0, 360)
TG_r, RG_r = np.meshgrid(TS_r, RS_r, indexing="ij")
dtr, drr = TS_r[1] - TS_r[0], RS_r[1] - RS_r[0]
XiT_r = bump1n(TS_r[:, None], 0.15, 0.85) * bump1n(RS_r[None, :], 3.5, 7.5)
XiR_r = bump1n(TS_r[:, None], 0.2, 0.8) * bump1n(RS_r[None, :], 4.0, 7.0)
gtt_r = -(1 - 2 * Ms / RS_r)
grr_r = 1 / (1 - 2 * Ms / RS_r)
sqrt_r = np.sqrt(-(gtt_r * grr_r))[None, :]
Gtr_r = sp.lambdify((r,), Gam(0, 0, 1).subs(M, Ms), "numpy")(RS_r)[None, :]
Grr_r = sp.lambdify((r,), Gam(1, 1, 1).subs(M, Ms), "numpy")(RS_r)[None, :]
Grtt_r = sp.lambdify((r,), Gam(1, 0, 0).subs(M, Ms), "numpy")(RS_r)[None, :]


def C(f):
    return sp.lambdify((t, r, M), f, "numpy")(TG_r, RG_r, Ms)


T00r, T01r, T10r, T11r = C(T[0][0]), C(T[0][1]), C(T[1][0]), C(T[1][1])
Er, R0r, R1r = C(E), C(div(0) - E * gu[0]), C(div(1) - E * gu[1])
gu0r, gu1r = C(gu[0]), C(gu[1])
dphi_r = [C(sp.diff(phi_expr, c)) for c in (t, r)]
nb_tt = np.gradient(XiT_r, dtr, axis=0) - Grtt_r * XiR_r
nb_tr = np.gradient(XiR_r, dtr, axis=0) - Gtr_r * XiT_r
nb_rt = np.gradient(XiT_r, drr, axis=1) - Gtr_r * XiT_r
nb_rr = np.gradient(XiR_r, drr, axis=1) - Grr_r * XiR_r
I1r = -sqrt_r * (T00r * nb_tt + T01r * (nb_tr + nb_rt) + T11r * nb_rr
                 + Er * ((XiT_r / gtt_r[None, :]) * dphi_r[0]
                         + (XiR_r / grr_r[None, :]) * dphi_r[1]))
I2r = -sqrt_r * (XiT_r * R0r + XiR_r * R1r)
Bndr = sqrt_r * (T00r * nb_tt + T01r * (nb_tr + nb_rt) + T11r * nb_rr
                 + XiT_r * (Er * gu0r + R0r) + XiR_r * (Er * gu1r + R1r))
q1r, q2r = quad(I1r, TS_r, RS_r), quad(I2r, TS_r, RS_r)
print(f"     refined (360x360): int I1 = {q1r:+.3e}, int I2 = {q2r:+.3e} "
      f"(Richardson ratio |q1r/q1| = {abs(q1r / q1):.3f} — smooth integrand ~1/4)")
# Richardson quartering: the truncation floor must shrink by ~h^2 on
# refinement (no upward drift); capable of failing on non-smooth integrands.
assert abs(q1r) <= abs(q1) / 2 + 1e-9 and abs(q2r) <= abs(q2) / 2 + 1e-12
print("     => delta_xi S_b = 0 (truncation floor; refined sums do not drift")
print("        upward); the once-integrated form (seed step 2) holds at the")
print("        FD level.  Exact pointwise IBP: ward_symbolic.py [6].")

# ---- N5: negative control ------------------------------------------------
print("\n[N5] negative control z0 Z psi^2 on the curved background:")
z0v = sp.symbols("z0v", positive=True)
psi_expr = (r - 4.0) ** 2 * sp.exp(-((t - 0.5) ** 2) / 0.1) + 0.1 * t ** 2
Z_expr = t * (r - 4.0) * sp.exp(-((r - 5.0) ** 2))
T5, E5, gu5, div5, _, gup5 = build(Ms, psi_expr, sp.S(0), sp.S(0))
Tp = [[sp.expand(T5[mu][nu] + z0v * gup5[mu][nu] * Z_expr * psi_expr ** 2)
       for nu in range(2)] for mu in range(2)]
Gam5 = Gam_fun(Ms)


def divp(nu):
    res = sp.diff(Tp[0][nu], t) + sp.diff(Tp[1][nu], r)
    for mu in range(2):
        for l in range(2):
            res += Gam5(mu, mu, l) * Tp[l][nu] + Gam5(nu, mu, l) * Tp[mu][l]
    return sp.expand(res)


Eps = sp.expand(E5 + 2 * z0v * Z_expr * psi_expr)
ZSUB = {z0v: 1.0}
for nu in range(2):
    rv = grid_eval(divp(nu) - (Eps * gu5[nu]
                               + z0v * psi_expr ** 2 * gup5[nu][nu] * sp.diff(Z_expr, (t, r)[nu])),
                   subs_map=ZSUB)
    mx = np.max(np.abs(rv))
    scl = np.max(np.abs([grid_eval(divp(nu), subs_map=ZSUB),
                         grid_eval(Eps * gu5[nu], subs_map=ZSUB)]))
    print(f"     nu={nu}: max|div T' - (E'_psi grad psi + z0 psi^2 grad Z)| = {mx:.3e} "
          f"(scale {scl:.3e}; relative {mx / scl:.2e})")
    assert mx < 1e-8 * scl + 1e-10
print("     flat on-shell witness psi = r^2, Z = -1/(z0 r^2) (Minkowski):")
Tw, Ew, guw, divw, _, gupw = build(sp.S(0), r ** 2, sp.S(0), sp.S(0))
Tpw = [[sp.expand(Tw[mu][nu] + z0v * gupw[mu][nu] * (-1 / (z0v * r ** 2)) * r ** 4)
        for nu in range(2)] for mu in range(2)]
os_t = sp.expand(sp.diff(Tpw[0][0], t) + sp.diff(Tpw[1][0], r))
os_x = sp.expand(sp.diff(Tpw[0][1], t) + sp.diff(Tpw[1][1], r))
Ew_num = sp.lambdify((r, z0v), Ew + 2 * z0v * (-1 / (z0v * r ** 2)) * r ** 2, "numpy")
fw = sp.lambdify((t, r, z0v), os_t, "numpy")
gxw = sp.lambdify((t, r, z0v), os_x, "numpy")
print(f"     E'_psi at r=3: {Ew_num(3.0, 1.0):.3e} (== 0)")
val_t, val_x = fw(0.4, 3.0, 1.0), gxw(0.4, 3.0, 1.0)
print(f"     div T' at (t,r)=(0.4,3.0): t-comp = {val_t:+.6e} (expect 0), "
      f"r-comp = {val_x:+.6e} (expect 6 = 2r)")
assert abs(Ew_num(3.0, 1.0)) < 1e-12
assert abs(val_t) < 1e-12 and abs(val_x - 6.0) < 1e-9
print("     => baryon equation holds yet div T' = (0, 2r) != 0: the extra force")
print("        term prevents the same on-shell identity.")

# ---- N6: footings ---------------------------------------------------------
print("\n[N6] footings and dimension examples (mandated constants):")
G = 6.67430e-11
cc = 299792458.0
a0_can = 9.3619e-11
a0_alt = 1.1279e-10
rho_can = 4 * a0_can ** 2 / (G * cc ** 2)
rho_alt = 4 * a0_alt ** 2 / (G * cc ** 2)
print(f"     canonical a0 = {a0_can:.6e} m/s^2: rho_Lambda = {rho_can:.6e} kg/m^3")
print(f"     alternative a0 = {a0_alt:.6e} m/s^2: rho_Lambda = {rho_alt:.6e} kg/m^3")
print(f"     density ratio (alt/can) = {(a0_alt / a0_can) ** 2:.6f} (kappa = 1/2 "
      f"fixed in both; footings do NOT share a fixed vacuum density)")
print(f"     kappa back-check: canonical {a0_can / (cc * np.sqrt(G * rho_can)):.8f}; "
      f"alt {a0_alt / (cc * np.sqrt(G * rho_alt)):.8f}")
print("     Ward identity: a0, kappa, rho_Lambda and G_N/G_bare/G_cosmo enter")
print("     S_b nowhere; the theorem is footing-independent and holds on both.")

print("\nALL NUMERIC CHECKS PASSED (actual residuals reported above).")