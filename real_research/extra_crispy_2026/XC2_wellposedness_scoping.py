#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XC2 -- NONLINEAR WELL-POSEDNESS OF C-H/K, SCOPED: L340's first open item ("NOT computed yet, in the order they decide:
nonlinear well-posedness ...").  A full theorem is not attempted.  This lane establishes the pieces that CAN be settled
and reduces the rest to a named literature question.

THE STRUCTURE.  C-H/K (L340) is a mixed elliptic-hyperbolic system: the metric and the khronon evolve; the auxiliary
sector (U, W, L, lambda_0) is solved on each preferred leaf.  For a fixed metric and lapse N the U-equation is the
Euler-Lagrange equation of
    E[U] = Int N sqrt(h) { 2 |D U - D ln N|^2 + 2 alpha_M^2 q(|D S U|^2 / alpha_M^2) },   S = exp((xi^2/2) Delta_h).

WHAT IS CHECKED (each check can fail)
  B1 [sympy] the Hessian of the q-integrand Q(p) = 2 alpha^2 q(|p|^2/alpha^2) has eigenvalues 4 C_T (twice, transverse)
     and 4 C_L (along p), with q' = C_T = nu - 1 and C_L = q' + 2 Y q'' = d(y nu)/dy - 1.
  B2 [spectral lemma] the heat filter never increases the Dirichlet energy on ANY closed leaf:
     ||D S f||^2 = sum_j lambda_j e^{-2 b lambda_j} |f_j|^2 <= ||D f||^2 (sympy per mode), checked numerically on a curved
     periodic leaf (random metric weights, matrix exponential of the weighted Laplacian).
  B3 [the convexity threshold] by B1 + B2 the second variation of E obeys d2E >= 4 (1 + min(0, C_min)) ||D dU||^2 (in the
     N-weighted norm), so E is strictly convex -- the constraint has exactly one solution (mod a constant) -- whenever
     C_min > -1.  Tabulated for every kernel on the record: nu_mono, nu_RAR, mu_exp (QUMOND form), mu_2, mu_5, mu_10.
  B4 [numerical demonstration] 2-D periodic leaf, non-constant lapse, filter xi = 2.5 cells: minimising E from four
     random starts gives the same U (nu_mono and nu_RAR), and the lowest non-trivial Hessian eigenvalue is positive.
  B5 [the MOND sector is lower order] the linearised MOND operator is S^T D^T C D S: at |k| >= K it is suppressed by
     e^{-xi^2 K^2} relative to the principal part 4k^2 (numerically on the grid).  With XC1 A3 (U = ln N kills the C-H
     term) the principal symbol of C-H/K is that of GR + the BPS khronon (alpha_c, lambda - 1 = c_2, beta = 0).
  B6 [the khronon's cone] the decoupling-limit khronon operator is Lap (alpha_c d_t^2 - c_2 Lap) (XC1 A1): its
     characteristic set is k^2 (alpha_c w^2 - c_2 k^2) = 0, a finite cone c_s^2 = c_2/alpha_c for alpha_c > 0.  At
     alpha_c = 0 the time derivatives drop out: the elliptic-lapse structure of minimal Horava gravity, whose Cauchy
     problem fails after a dust shell collapses (Jacobson & Pulakkat 2025, J. Phys. A 58 315404).  Control, in-lane.
  B7 [the zero-field limit] near a zero of the filtered field the deep-MOND flux is F(p) = |p|^{1/2} p/|p| (not
     Lipschitz).  Continuum quadrature of ||F(p + eps e) - F(p)|| / eps for zero sets of codimension 1, 2, 3: Lipschitz
     for isolated zeros (codim 2, 3 -- generic after filtering), log-Lipschitz ~ sqrt(ln(1/eps)/2) for a planar zero set
     (codim 1, symmetric configurations only).  The log modulus satisfies Osgood's uniqueness criterion
     (Int de/(e sqrt ln(1/e)) diverges).

  MUTATE=1 replaces the constitutive coefficients by C_T = C_L = -1.5 (below the threshold): E is unbounded below, the
  four starts do not agree and the Hessian has a negative eigenvalue -- B4 must FAIL.  rc = 1.

SCOPE.  What is NOT established: strong hyperbolicity of GR + the BPS khronon on arbitrary nonlinear backgrounds (the
reduced question).  Einstein-aether theory is strongly hyperbolic under conditions on its couplings (Sarbach, Barausse &
Preciado-Lopez 2019, CQG 36 165007); no general theorem for the hypersurface-orthogonal (khronometric) case is used
here; its alpha -> 0 limit is known to fail (B6).  B4 is a 2-D demonstration on a flat periodic leaf with a lapse weight,
not a proof; B3's inequality is the proof.  Units: a0 = 1 inside the numerics.

Run from the repository root:  python3 real_research/extra_crispy_2026/XC2_wellposedness_scoping.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from scipy.optimize import brentq, minimize
from scipy.integrate import quad
from scipy.sparse.linalg import LinearOperator, eigsh

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "XC2", "XC2_wellposedness_scoping"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()
RNG = np.random.default_rng(20260926)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("WHAT IS CHECKED")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: C_T = C_L = -1.5 (below the convexity threshold); B4 must FAIL ***")

# ============================================================================================ kernels (a0 = 1)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore", invalid="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.clip(y, 1e-300, 1e4))), 0.0)
def dh_rar(y, e_=1e-6):
    return (h_rar(y * (1 + e_)) - h_rar(y * (1 - e_))) / (2 * y * e_)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-14, 12, 260001); YG = 10**LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
HINT_MONO = np.concatenate([[0.0], np.cumsum(0.5 * (H_MONO[1:] + H_MONO[:-1]) * np.diff(YG))])   # Int_0^y h
DH_RAR = dh_rar(YG); H_RARG = h_rar(YG)
HINT_RAR = np.concatenate([[0.0], np.cumsum(0.5 * (H_RARG[1:] + H_RARG[:-1]) * np.diff(YG))])
KERNELS = {
    "nu_mono": dict(h=lambda y: np.interp(np.log10(y), LYG, H_MONO), dh=lambda y: np.interp(np.log10(y), LYG, DH_MONO),
                    Hint=lambda y: np.interp(np.log10(y), LYG, HINT_MONO)),
    "nu_RAR": dict(h=lambda y: np.interp(np.log10(y), LYG, H_RARG), dh=lambda y: np.interp(np.log10(y), LYG, DH_RAR),
                   Hint=lambda y: np.interp(np.log10(y), LYG, HINT_RAR)),
}
def CT_of(name, y): return KERNELS[name]["h"](y) / y           # nu - 1
def CL_of(name, y): return KERNELS[name]["dh"](y)               # d(y nu)/dy - 1

# ============================================================================================ B1
banner("B1  THE HESSIAN OF THE q-INTEGRAND (sympy, generic q)")
px, py_, pz, al_ = sp.symbols('p_x p_y p_z alpha', real=True)
# The Hessian at a point depends only on q'(Y0) and q''(Y0); a cubic q with symbolic coefficients makes both free,
# so the identity below is the general statement.
c1, c2c, c3 = sp.symbols('c1 c2 c3')
Qt = 2 * al_**2 * (c1 * (px**2 + py_**2 + pz**2) / al_**2 + c2c * ((px**2 + py_**2 + pz**2) / al_**2)**2 + c3 * ((px**2 + py_**2 + pz**2) / al_**2)**3)
Ht = sp.hessian(Qt, (px, py_, pz)).subs({py_: 0, pz: 0})
Y0 = px**2 / al_**2
qp = c1 + 2 * c2c * Y0 + 3 * c3 * Y0**2                            # q'(Y)
qpp = 2 * c2c + 6 * c3 * Y0                                        # q''(Y)
b1_T = sp.simplify(Ht[1, 1] - 4 * qp) == 0 and sp.simplify(Ht[2, 2] - 4 * qp) == 0
b1_L = sp.simplify(Ht[0, 0] - 4 * (qp + 2 * Y0 * qpp)) == 0
b1_off = all(sp.simplify(Ht[i, j]) == 0 for i in range(3) for j in range(3) if i != j)
P(f"    on-axis Hessian of 2 alpha^2 q(|p|^2/alpha^2): transverse = 4 q'(Y): {b1_T};  along p = 4 (q' + 2 Y q''): {b1_L};  "
  f"off-diagonal zero: {b1_off}")
OUT["numbers"]["B1"] = {"transverse": b1_T, "longitudinal": b1_L, "offdiag_zero": b1_off}
check("B1 the q-integrand's Hessian has eigenvalues 4 C_T (x2) and 4 C_L: Q is convex in grad S U iff C_T, C_L >= 0",
      f"transverse {b1_T}, longitudinal {b1_L}, off-diagonal {b1_off}", b1_T and b1_L and b1_off)

# ============================================================================================ B2
banner("B2  THE HEAT FILTER NEVER RAISES THE DIRICHLET ENERGY (any closed leaf)")
lam, bb = sp.symbols('lambda b', nonnegative=True)
per_mode = sp.simplify(lam * sp.exp(-2 * bb * lam) - lam)          # (filtered - unfiltered) per eigenmode
per_mode_ok = sp.simplify(per_mode + lam * (1 - sp.exp(-2 * bb * lam))) == 0
# numerical: curved periodic 2-D leaf, weighted Laplacian L = -G^T W G / w, self-adjoint in the w-weighted inner product
n2 = 20
Wx = np.exp(0.6 * RNG.standard_normal((n2, n2))); Wy = np.exp(0.6 * RNG.standard_normal((n2, n2))); wv = np.exp(0.4 * RNG.standard_normal((n2, n2)))
idx = lambda i, j: (i % n2) * n2 + (j % n2)
Gx = np.zeros((n2 * n2, n2 * n2)); Gy = np.zeros_like(Gx)
for i in range(n2):
    for j in range(n2):
        Gx[idx(i, j), idx(i + 1, j)] += 1; Gx[idx(i, j), idx(i, j)] -= 1
        Gy[idx(i, j), idx(i, j + 1)] += 1; Gy[idx(i, j), idx(i, j)] -= 1
Wm = np.diag(np.concatenate([Wx.ravel()])); Wmy = np.diag(Wy.ravel()); w = wv.ravel()
# NOTE: Apple-Accelerate BLAS raises spurious floating-point flags on these dense matmuls; the results are checked
# below to be finite and to agree with an independent eigenbasis route to 1e-8, so the flags are silenced here only.
_errs = np.seterr(all='ignore')
Kmat = Gx.T @ Wm @ Gx + Gy.T @ Wmy @ Gy                             # Dirichlet form: f^T K f
isw = 1.0 / np.sqrt(w)
Ms = isw[:, None] * Kmat * isw[None, :]                            # W^-1/2 K W^-1/2, symmetric: -Delta_h in the w-metric
lam_s, V_s = np.linalg.eigh(Ms)
Sb = (isw[:, None] * V_s) @ np.diag(np.exp(-0.3 * lam_s)) @ (V_s.T * np.sqrt(w)[None, :])   # e^{b Delta_h}, b = 0.3 cells^2
worst, worst_eig = -np.inf, -np.inf
for _ in range(50):
    f = RNG.standard_normal(n2 * n2)
    ef, esf = f @ Kmat @ f, (Sb @ f) @ Kmat @ (Sb @ f)
    worst = max(worst, esf / ef)
    g = V_s.T @ (np.sqrt(w) * f)                                    # independent route: the same ratio in the eigenbasis
    worst_eig = max(worst_eig, float(np.sum(lam_s * np.exp(-0.6 * lam_s) * g**2) / np.sum(lam_s * g**2)))
finite_ok = bool(np.all(np.isfinite(Sb)) and np.all(np.isfinite(Kmat)))
np.seterr(**_errs)
P(f"    per mode: lambda e^(-2 b lambda) - lambda = -lambda (1 - e^(-2 b lambda)) <= 0: {per_mode_ok}")
P(f"    curved periodic leaf ({n2}x{n2}, random metric weights): max over 50 random f of ||D S f||^2/||D f||^2 = {worst:.6f} "
  f"(eigenbasis route {worst_eig:.6f}; all entries finite: {finite_ok})")
OUT["numbers"]["B2"] = {"per_mode": per_mode_ok, "max_ratio": worst, "max_ratio_eigenbasis": worst_eig, "finite": finite_ok}
check("B2 ||D S f|| <= ||D f|| on any closed leaf (spectral identity; curved discrete leaf, 50 random fields, two routes)",
      f"per-mode identity {per_mode_ok}; max ratio {worst:.6f} / {worst_eig:.6f}", per_mode_ok and finite_ok and worst <= 1 + 1e-12
      and abs(worst - worst_eig) < 1e-8,
      "so the filtered MOND term can lower the second variation by at most |C_min| times the unfiltered Dirichlet energy")

# ============================================================================================ B3
banner("B3  THE CONVEXITY THRESHOLD, C_min > -1, FOR EVERY KERNEL ON THE RECORD")
ys = np.logspace(-10, 8, 20001)
def qumond_from_mu(mu, dmu):
    """C_T, C_L of the QUMOND form of an AQUAL kernel mu(x): g = x a0 with mu(x) x = y."""
    xs = np.logspace(-6, 7, 40001)
    yv = mu(xs) * xs
    CT = xs / yv - 1.0
    CL = 1.0 / (mu(xs) + xs * dmu(xs)) - 1.0                      # dg/dg_N - 1
    return CT, CL
table = {}
for nm in ("nu_mono", "nu_RAR"):
    table[nm] = (float(np.min(CT_of(nm, ys))), float(np.min(CL_of(nm, ys))))
mus = {"mu_exp (1 - e^-x)": (lambda x: -np.expm1(-x), lambda x: np.exp(-x)),
       "mu_2 (x/sqrt(1+x^2))": (lambda x: x / np.sqrt(1 + x**2), lambda x: (1 + x**2)**-1.5),
       "mu_5": (lambda x: x / (1 + x**5)**0.2, lambda x: (1 + x**5)**-1.2),
       "mu_10": (lambda x: x / (1 + x**10)**0.1, lambda x: (1 + x**10)**-1.1)}
for nm, (mu, dmu) in mus.items():
    CT, CL = qumond_from_mu(mu, dmu)
    table[nm] = (float(CT.min()), float(CL.min()))
for nm, (ct, cl) in table.items():
    P(f"    {nm:22s}  min C_T = {ct:+.4f}   min C_L = {cl:+.4f}   1 + min(0, C) = {1 + min(0.0, ct, cl):.4f}")
cmin_all = min(min(v) for v in table.values())
OUT["numbers"]["B3"] = {k: {"min_CT": v[0], "min_CL": v[1]} for k, v in table.items()}
check("B3 every kernel on the record has C_min > -1, so E[U] is strictly convex and the MOND constraint has exactly one "
      "solution on every leaf (d2E >= 4(1 + min(0, C_min)) ||D dU||^2, from B1 + B2)",
      f"lowest C over all kernels = {cmin_all:+.4f} (nu_mono: {table['nu_mono'][1]:+.4f}; nu_RAR's turnover {table['nu_RAR'][1]:+.4f})",
      cmin_all > -1.0,
      "uniqueness of the constraint does not need the monotone law; L340 needs it for the khronon's momentum channel, "
      "not for the elliptic solve")

# ============================================================================================ B4
banner("B4  NUMERICAL DEMONSTRATION: 2-D periodic leaf, non-constant lapse, filter xi = 2.5 cells")
NG = 48; dx = 1.0 / NG; XI = 2.5 * dx
kx = 2 * np.pi * np.fft.fftfreq(NG, d=dx); KX, KY = np.meshgrid(kx, kx, indexing="ij"); K2 = KX**2 + KY**2
SK = np.exp(-0.5 * XI**2 * K2)
NYQ = np.pi / dx
TRIV = ((K2 == 0) | np.isclose(np.abs(KX), NYQ) | np.isclose(np.abs(KY), NYQ)).astype(float)   # modes with zero spectral gradient
xg = (np.arange(NG) + 0.5) * dx; XX, YY = np.meshgrid(xg, xg, indexing="ij")
def per_d2(x0, y0):
    ddx = np.minimum(np.abs(XX - x0), 1 - np.abs(XX - x0)); ddy = np.minimum(np.abs(YY - y0), 1 - np.abs(YY - y0))
    return ddx**2 + ddy**2
phi = np.zeros((NG, NG))
for (x0, y0, A, s) in ((0.30, 0.35, -0.030, 0.06), (0.70, 0.62, -0.020, 0.05), (0.52, 0.18, -0.008, 0.04)):
    phi += A * np.exp(-per_d2(x0, y0) / (2 * s**2))
Nlap = np.exp(phi)
def grad(f):
    fh = np.fft.fft2(f); return np.real(np.fft.ifft2(1j * KX * fh)), np.real(np.fft.ifft2(1j * KY * fh))
def div(gx, gy):
    return np.real(np.fft.ifft2(1j * KX * np.fft.fft2(gx) + 1j * KY * np.fft.fft2(gy)))
def filt(f):
    return np.real(np.fft.ifft2(SK * np.fft.fft2(f)))
gphix, gphiy = grad(phi)
ymax_src = float(np.max(np.hypot(gphix, gphiy)))
SCALE = 6.0 / ymax_src                                             # |grad ln N| spans ~0 .. 6 a0 (deep MOND to Newtonian)
phi *= SCALE; gphix *= SCALE; gphiy *= SCALE
Nlap = np.exp(0.3 * phi / np.max(np.abs(phi)))      # lapse weight varying by ~30% (stronger than physical)
def energy_grad(Uf, kname, mut=MUTATE):
    U = Uf.reshape(NG, NG)
    ux, uy = grad(U); sx, sy = grad(filt(U))
    r = np.hypot(sx, sy); rs = np.maximum(r, 1e-14)
    if mut:
        qv = -1.5 * r**2; qpr = -1.5 * np.ones_like(r)
    else:
        qv = 2.0 * KERNELS[kname]["Hint"](rs); qpr = KERNELS[kname]["h"](rs) / rs     # q(y^2) = 2 Int_0^y h, q' = h/y
    E = np.sum(Nlap * (2 * ((ux - gphix)**2 + (uy - gphiy)**2) + 2 * qv)) * dx * dx
    g1 = -div(4 * Nlap * (ux - gphix), 4 * Nlap * (uy - gphiy))
    g2 = -filt(div(4 * Nlap * qpr * sx, 4 * Nlap * qpr * sy))
    return E, ((g1 + g2) * dx * dx).ravel()
def hess_vec(v, U, kname, mut=MUTATE):
    V = v.reshape(NG, NG)
    vx, vy = grad(V); sx, sy = grad(filt(U)); wx, wy = grad(filt(V))
    r = np.maximum(np.hypot(sx, sy), 1e-14); ex_, ey_ = sx / r, sy / r
    if mut:
        CT = -1.5 * np.ones_like(r); CL = CT
    else:
        CT = KERNELS[kname]["h"](r) / r; CL = KERNELS[kname]["dh"](r)
    par = wx * ex_ + wy * ey_
    fx = 4 * Nlap * (CT * wx + (CL - CT) * par * ex_); fy = 4 * Nlap * (CT * wy + (CL - CT) * par * ey_)
    out = -div(4 * Nlap * vx, 4 * Nlap * vy) - filt(div(fx, fy))
    # the spectral gradient annihilates the constant and the Nyquist lines (checkerboards): lift those trivial modes
    out = out + 50.0 * np.real(np.fft.ifft2(TRIV * np.fft.fft2(V)))
    return (out * dx * dx).ravel()
rowsB4, SOLS = {}, {}
for kname in ("nu_mono", "nu_RAR"):
    sols, Es, oks = [], [], []
    for trial in range(4):
        U0 = filt(filt(RNG.standard_normal((NG, NG)))) * 0.05 * (trial + 1)
        with np.errstate(all=("ignore" if MUTATE else "warn")):      # the MUTATE energy is unbounded below: divergence is the point
            res = minimize(energy_grad, U0.ravel(), args=(kname,), jac=True, method="L-BFGS-B",
                           options={"maxiter": 20000, "gtol": 1e-12, "ftol": 1e-16})
        U = res.x.reshape(NG, NG); U -= U.mean()
        sols.append(U); Es.append(float(res.fun)); oks.append(bool(res.success) or res.nit > 5)
    _e = np.seterr(all=("ignore" if MUTATE else "warn"))
    ref = sols[0]; SOLS[kname] = ref; scale = float(np.max(np.abs(ref))) if np.all(np.isfinite(ref)) else float("nan")
    spread = max(float(np.max(np.abs(s - ref))) for s in sols) / scale if np.isfinite(scale) and scale > 0 else float("inf")
    op = LinearOperator((NG * NG, NG * NG), matvec=lambda v, U=ref, kn=kname: hess_vec(v, U, kn), dtype=float)
    try:
        lam_min = float(eigsh(op, k=1, which="SA", tol=1e-6, maxiter=5000, return_eigenvectors=False)[0])
    except Exception as ex:
        lam_min = float("nan")
    sx, sy = grad(filt(ref)); yfil = np.hypot(sx, sy)
    rowsB4[kname] = {"energies": Es, "spread_rel": spread, "lambda_min": lam_min, "y_filtered_range": [float(yfil.min()), float(yfil.max())]}
    np.seterr(**_e)
    P(f"    {kname:8s}: energies {', '.join(f'{e_:.10g}' for e_ in Es)};  max |U_i - U_1|/max|U| = {spread:.2e};  "
      f"lowest Hessian eigenvalue {lam_min:+.3e};  filtered y in [{yfil.min():.2e}, {yfil.max():.2f}]")
OUT["numbers"]["B4"] = rowsB4
b4_ok = all(np.isfinite(v["spread_rel"]) and v["spread_rel"] < 1e-5 and np.isfinite(v["lambda_min"]) and v["lambda_min"] > 0
            for v in rowsB4.values())
check("B4 on a curved-lapse periodic leaf the MOND constraint converges to ONE solution from four random starts, and the "
      "lowest non-trivial Hessian eigenvalue is positive (nu_mono and nu_RAR; the field spans deep MOND to y ~ 6)",
      "; ".join(f"{k}: spread {v['spread_rel']:.1e}, lambda_min {v['lambda_min']:+.2e}" for k, v in rowsB4.items()), b4_ok,
      "the elliptic half of the mixed Cauchy problem is uniquely solvable at every step")

# ============================================================================================ B5
banner("B5  THE MOND SECTOR IS LOWER ORDER: the linearised operator S^T D^T C D S at high k")
if MUTATE:                                                       # B5 is independent of the mutation: re-solve un-mutated
    _r = minimize(energy_grad, np.zeros(NG * NG), args=("nu_mono", False), jac=True, method="L-BFGS-B",
                  options={"maxiter": 20000, "gtol": 1e-12, "ftol": 1e-16})
    Uref = _r.x.reshape(NG, NG) - _r.x.mean()
else:
    Uref = SOLS["nu_mono"]
def mond_lin(V, U):
    sx, sy = grad(filt(U)); wx, wy = grad(filt(V))
    r = np.maximum(np.hypot(sx, sy), 1e-14); ex_, ey_ = sx / r, sy / r
    CT = KERNELS["nu_mono"]["h"](r) / r; CL = KERNELS["nu_mono"]["dh"](r)
    par = wx * ex_ + wy * ey_
    return -filt(div(4 * (CT * wx + (CL - CT) * par * ex_), 4 * (CT * wy + (CL - CT) * par * ey_)))
ratios = {}
for Kc_xi in (2.0, 3.0, 4.0):
    Kc = Kc_xi / XI
    mask = (np.sqrt(K2) >= Kc).astype(float)
    if mask.sum() == 0:
        continue
    v = np.real(np.fft.ifft2(mask * np.fft.fft2(RNG.standard_normal((NG, NG)))))
    for _ in range(30):                                            # power iteration on the high-k block
        Mv = np.real(np.fft.ifft2(mask * np.fft.fft2(mond_lin(v, Uref))))
        nrm = np.linalg.norm(Mv); v = Mv / (nrm + 1e-300)
    princ = 4 * Kc**2
    ratios[Kc_xi] = float(nrm / princ)
    P(f"    |k| >= {Kc_xi:.0f}/xi: ||MOND block|| / (4 K^2) = {ratios[Kc_xi]:.2e}   (e^(-xi^2 K^2) = {math.exp(-Kc_xi**2):.2e})")
OUT["numbers"]["B5"] = ratios
pref = {k_: v_ / math.exp(-k_**2) for k_, v_ in ratios.items()}         # ratio / e^{-xi^2 K^2}
vals = list(ratios.values())
b5_ok = (len(ratios) == 3 and all(vals[i + 1] < vals[i] for i in range(2)) and max(pref.values()) / min(pref.values()) < 5
         and vals[-1] < 1e-4)
P(f"    prefactor ratio / e^(-xi^2 K^2): " + ", ".join(f"{k_:.0f}/xi: {v_:.1f}" for k_, v_ in pref.items())
  + "  (bounded: the effective constitutive coefficient, largest near zero-field points)")
OUT["numbers"]["B5_prefactor"] = pref
check("B5 the linearised MOND operator falls like C_eff e^{-xi^2 K^2} relative to the principal part (bounded prefactor, "
      "monotone, < 1e-4 by K = 4/xi): an order -infinity (smoothing) operator, absent from the principal symbol; with "
      "XC1 A3 the principal symbol of C-H/K is GR + the BPS khronon",
      "; ".join(f"K = {k_:.0f}/xi: {v_:.1e} (prefactor {pref[k_]:.1f})" for k_, v_ in ratios.items()), b5_ok)

# ============================================================================================ B6
banner("B6  THE KHRONON'S CHARACTERISTIC CONE (decoupling limit, from XC1 A1), and the alpha_c -> 0 control")
w_, k_, ac_, c2_ = sp.symbols('omega k alpha_c c_2', positive=True)
sym = k_**2 * (ac_ * w_**2 - c2_ * k_**2)                          # principal symbol of Lap(alpha_c d_t^2 - c_2 Lap)
roots = sp.solve(sp.Eq(sym, 0), w_)
cone = sp.simplify(roots[0] / k_) if roots else None
sym0 = sp.simplify(sym.subs(ac_, 0))
has_time0 = sym0.has(w_)
P(f"    symbol k^2 (alpha_c w^2 - c_2 k^2): real roots w/k = {cone}  (finite cone for alpha_c > 0)")
P(f"    alpha_c = 0: symbol = {sym0}; contains omega: {has_time0}  -> no time derivative: the lapse is elliptic on each leaf")
OUT["numbers"]["B6"] = {"cone": str(cone), "alpha0_symbol": str(sym0), "alpha0_has_time": has_time0}
check("B6 for alpha_c > 0 the khronon has a finite characteristic cone (c_s^2 = c_2/alpha_c, XC1 A9's 4.4e2-7.9e5 c); at "
      "alpha_c = 0 the time derivatives vanish (minimal Horava's elliptic lapse, whose Cauchy problem fails after collapse)",
      f"cone {cone}; alpha_c = 0 symbol {sym0}", cone is not None and sp.simplify(cone - sp.sqrt(c2_ / ac_)) == 0 and not has_time0,
      "alpha_c > 0 is load-bearing a third time (after L340's negative lobes and XC1's strong coupling): it is what keeps "
      "the khronon hyperbolic")

# ============================================================================================ B7
banner("B7  THE ZERO-FIELD LIMIT: regularity of the deep-MOND flux F(p) = |p|^(1/2) p/|p| near zeros of the filtered field")
def F1(p): return np.sign(p) * np.sqrt(np.abs(p))
def ratio_codim1(eps):
    f = lambda x: (F1(x + eps) - F1(x))**2
    pts = sorted({-eps, 0.0})
    val = quad(f, -1, 1, points=pts, limit=400, epsabs=1e-30, epsrel=1e-10)[0]
    return math.sqrt(val) / eps
def ratio_codim(dim, eps):
    # isolated zero p = r (vector), perturbation eps e_1; radial x angular quadrature in dim = 2, 3
    def integrand_r(r):
        if dim == 2:
            g = lambda th: _dF2(r * math.cos(th), r * math.sin(th), 0.0, eps)
            return r * quad(g, 0, 2 * math.pi, limit=200, epsrel=1e-8)[0]
        g = lambda th: 2 * math.pi * math.sin(th) * _dF2(r * math.cos(th), r * math.sin(th), 0.0, eps)
        return r * r * quad(g, 0, math.pi, limit=200, epsrel=1e-8)[0]
    val = quad(integrand_r, 0, 1, points=[eps], limit=400, epsrel=1e-8)[0]
    return math.sqrt(val) / eps
def _dF2(x, y, z, eps):
    def Fv(a, b, c):
        n = math.sqrt(a * a + b * b + c * c)
        return (0.0, 0.0, 0.0) if n == 0 else (a / math.sqrt(n), b / math.sqrt(n), c / math.sqrt(n))
    f1 = Fv(x + eps, y, z); f0 = Fv(x, y, z)
    return (f1[0] - f0[0])**2 + (f1[1] - f0[1])**2 + (f1[2] - f0[2])**2
EPS = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]
r1 = [ratio_codim1(e_) for e_ in EPS]
r2 = [ratio_codim(2, e_) for e_ in EPS[:5]]
r3 = [ratio_codim(3, e_) for e_ in EPS[:5]]
pred1 = [math.sqrt(math.log(1 / e_) / 2) for e_ in EPS]
P("    eps:            " + "  ".join(f"{e_:8.0e}" for e_ in EPS))
P("    codim 1 (plane): " + "  ".join(f"{v_:8.3f}" for v_ in r1) + "   <- grows like sqrt(ln(1/eps)/2):")
P("    sqrt(ln/2):      " + "  ".join(f"{v_:8.3f}" for v_ in pred1))
P("    codim 2 (line):  " + "  ".join(f"{v_:8.3f}" for v_ in r2) + "   <- bounded (Lipschitz)")
P("    codim 3 (point): " + "  ".join(f"{v_:8.3f}" for v_ in r3) + "   <- bounded (Lipschitz)")
slope1 = (r1[-1]**2 - r1[-3]**2) / (math.log(1 / EPS[-1]) - math.log(1 / EPS[-3]))
osgood = sp.integrate(1 / (sp.Symbol('u', positive=True)**sp.Rational(1, 2)), (sp.Symbol('u', positive=True), 1, sp.oo))
OUT["numbers"]["B7"] = {"eps": EPS, "codim1": r1, "codim1_pred": pred1, "codim2": r2, "codim3": r3,
                        "d(R^2)/d ln(1/eps)": slope1, "osgood_integral": str(osgood)}
b7_ok = (abs(slope1 - 0.5) < 0.05 and max(r2) / min(r2) < 1.3 and max(r3) / min(r3) < 1.3 and osgood == sp.oo)
check("B7 the deep-MOND flux is Lipschitz at isolated zeros (codim 2, 3) and log-Lipschitz, R^2 ~ ln(1/eps)/2, at a planar "
      "zero set (codim 1); the log modulus satisfies Osgood's uniqueness criterion (Int du/sqrt(u) diverges)",
      f"d(R^2)/d ln(1/eps) = {slope1:.3f} (predicted 0.5); codim 2 range {min(r2):.3f}-{max(r2):.3f}; codim 3 range {min(r3):.3f}-{max(r3):.3f}; "
      f"Osgood integral {osgood}", b7_ok,
      "the zero-field point (spec requirement 9) is controlled: the filter makes zeros generic (isolated) and the only "
      "non-Lipschitz case, a symmetric planar zero set, is still Osgood-unique")

banner("VERDICT")
P(f"""  Nonlinear well-posedness of C-H/K, scoped.  SETTLED here: (i) the elliptic half -- the MOND constraint is a strictly
  convex variational problem on every leaf for every kernel on the record (C_min > -1; B1-B3), demonstrated numerically
  (B4); (ii) the MOND sector is lower order (B5), so with XC1 A3 the principal symbol is GR + the BPS khronon; (iii) the
  khronon is hyperbolic with a finite cone for alpha_c > 0 and degenerates to minimal Horava's elliptic lapse at alpha_c = 0
  (B6); (iv) the zero-field limit is controlled: Lipschitz at generic zeros, log-Lipschitz (Osgood-unique) at symmetric
  planar ones (B7).  REDUCED, not settled: strong hyperbolicity of GR + the BPS khronon on arbitrary nonlinear backgrounds
  -- a question about khronometric gravity itself.  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
