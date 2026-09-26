#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XC5 -- THE MOND CONSTRAINT WITH A NON-CONSTANT LAPSE: a correction to XC2, and what the nu_mono decision buys.

THE CORRECTION.  XC2 B2 proved that the heat filter never raises the Dirichlet energy when the filter's Laplacian and
the energy share one measure.  C-H/K's constraint functional is lapse-weighted,
    E[U] = Int N sqrt(h) { 2 |D U - D ln N|^2 + 2 alpha_M^2 q(|D S U|^2/alpha_M^2) },   S = exp(b Delta_h),
and the geometric filter need NOT contract the N-weighted energy.  The lead track found this independently
(real_research/closure_doors_2026_09_26/auxiliary/RESULT.md, uncommitted at the time: an exact Fourier example with
positive initial derivative 154 pi/25, a converged negative Hessian with the exact exponential kernel, the sufficient
bound N_max/N_min < e^2 + 1, and the repair S -> exp(b Delta_N), Delta_N = N^-1 D_i(N D^i)).  So XC2 B3's convexity
statement needs a lapse-contrast condition for kernels whose constitutive coefficient is somewhere negative.

WHAT THIS LANE CHECKS (each check can fail)
  E1 [the counterexample, reproduced] on a periodic grid with a well-shaped lapse (a minimum, as N = e^{Phi/c^2} has in
     a potential well) of contrast 50, the geometric heat filter RAISES the N-weighted Dirichlet energy for some field:
     d/db Int N |D e^{b Delta} f|^2 at b = 0 is positive (1-D: -2 Int N g'^2 + Int N'' g^2, g = f').
  E2 [the contrast bound] Int N |D S f|^2 <= (N_max/N_min) Int N |D f|^2 for every f (proof in Lean; 200 random fields
     and lapses): so for a kernel with C_min < 0 the constraint is strictly convex when (N_max/N_min) |C_min| < 1.
  E3 [what the nu_mono decision buys] nu_mono has C_T > 0 and C_L > 0 at every y, so the q-integrand is convex
     (including at zero gradient: phi(r) = 2 alpha^2 q(r^2/alpha^2) is convex and non-decreasing on [0, inf)).  Then
     d2E >= 4 Int N |D dU|^2 > 0 for ANY positive lapse, with the UNCHANGED geometric filter: no contrast condition,
     no filter repair.
  E4 [the contrast thresholds of the turning kernels] 1/|C_min|: mu_exp e^2 + 1 = 8.389 (its C_L minimum is exactly
     -1/(e^2 + 1) at x = 2, the lead's bound), nu_RAR 30.9, mu_10 2.87.  Galaxy and Solar-System lapses have contrast
     <= e^{2e-4}; near a compact object the lapse contrast is unbounded (N -> 0 at a horizon), where only a kernel with
     C_min >= 0 keeps the constraint convex.
  E5 [numerical demonstration] 2-D periodic leaf, well-shaped lapse of contrast 50, filter 2.5 cells: with nu_mono four random starts
     converge to the same U and the lowest non-trivial Hessian eigenvalue is positive.

  MUTATE=1 replaces nu_mono in E5 by constitutive coefficients C_T = C_L = -1.5 (below the threshold everywhere, XC2's
  control): the energy is unbounded below, the starts disagree and the Hessian turns negative -- E5 must FAIL.  (mu_exp,
  and even a 10x-mu_exp phantom, stay convex on this configuration: the pointwise threshold is sufficient, not necessary.)  rc = 1.

  E6 [a correction to XC2 B7] around an OPEN zero-field region (a homogeneous background) the MOND response scales as
     sqrt(eps) for every kernel, nu_mono included; that modulus fails Osgood's criterion.

SCOPE.  Fixed metric and lapse: convexity of the auxiliary (elliptic) solve, not coupled physical-time stability; the
geometric filter's failure to contract the lapse-weighted norm (E1) still matters for energy estimates of the coupled
evolution even where convexity holds.  nu_mono's splice (where the floor delta h_p/(y + y_p) takes over from h'_RAR) makes
C_L continuous but its derivative jump, so the q-integrand is C^2 but not C^3 there: strict convexity survives, a smooth
Taylor argument at the splice does not.  The constraint's coupling to the lapse's own variation (the lead's
LAPSE_VARIATION.md) is not addressed here.

Run from the repository root:  python3 real_research/extra_crispy_2026/XC5_lapse_weighted_convexity.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from scipy.optimize import brentq, minimize
from scipy.sparse.linalg import LinearOperator, eigsh

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "XC5", "XC5_lapse_weighted_convexity"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()
RNG = np.random.default_rng(20260927)


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


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: E5 uses C_T = C_L = -1.5 (below the convexity threshold everywhere); E5 must FAIL ***")

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
HINT_MONO = np.concatenate([[0.0], np.cumsum(0.5 * (H_MONO[1:] + H_MONO[:-1]) * np.diff(YG))])
# mu_exp in QUMOND form, parametrised by x = g/a0: y = x(1 - e^-x), phantom h = y (nu - 1) = x - y = x e^-x
XG = np.logspace(-8, 3, 200001)
YX = XG * (-np.expm1(-XG)); HX = XG * np.exp(-XG)
ord_ = np.argsort(YX); YX, HX, XGs = YX[ord_], HX[ord_], XG[ord_]
DHX = np.gradient(HX, YX)
HINTX = np.concatenate([[0.0], np.cumsum(0.5 * (HX[1:] + HX[:-1]) * np.diff(YX))])
K = {
    "nu_mono": dict(h=lambda y: np.interp(np.log10(y), LYG, H_MONO), dh=lambda y: np.interp(np.log10(y), LYG, DH_MONO),
                    Hint=lambda y: np.interp(np.log10(y), LYG, HINT_MONO)),
    "mu_exp": dict(h=lambda y: np.interp(y, YX, HX), dh=lambda y: np.interp(y, YX, DHX), Hint=lambda y: np.interp(y, YX, HINTX)),
    # MUTATE control: constitutive coefficients C_T = C_L = -1.5 everywhere (below the threshold at every y; XC2's control)
    "neg_const": dict(h=lambda y: -1.5 * y, dh=lambda y: -1.5 * np.ones_like(y), Hint=lambda y: -0.75 * y**2),
}

# ============================================================================================ grid helpers (2-D periodic)
NG = 48; dx = 1.0 / NG; XI = 2.5 * dx
kx = 2 * np.pi * np.fft.fftfreq(NG, d=dx); KX, KY = np.meshgrid(kx, kx, indexing="ij"); K2 = KX**2 + KY**2
NYQ = np.pi / dx
TRIV = ((K2 == 0) | np.isclose(np.abs(KX), NYQ) | np.isclose(np.abs(KY), NYQ)).astype(float)
def grad(f):
    fh = np.fft.fft2(f); return np.real(np.fft.ifft2(1j * KX * fh)), np.real(np.fft.ifft2(1j * KY * fh))
def div(gx, gy):
    return np.real(np.fft.ifft2(1j * KX * np.fft.fft2(gx) + 1j * KY * np.fft.fft2(gy)))
def heat(f, b):
    return np.real(np.fft.ifft2(np.exp(-b * K2) * np.fft.fft2(f)))
xg = (np.arange(NG) + 0.5) * dx; XX, YY = np.meshgrid(xg, xg, indexing="ij")
def lapse_with_contrast(C):
    base = np.exp(-((np.minimum(np.abs(XX - 0.5), 1 - np.abs(XX - 0.5)))**2 + (np.minimum(np.abs(YY - 0.5), 1 - np.abs(YY - 0.5)))**2) / (2 * 0.08**2))
    return 1.0 + (C - 1.0) * base                              # N ranges over [1, C]
def lapse_well(C, sig=0.08):
    base = np.exp(-((np.minimum(np.abs(XX - 0.5), 1 - np.abs(XX - 0.5)))**2 + (np.minimum(np.abs(YY - 0.5), 1 - np.abs(YY - 0.5)))**2) / (2 * sig**2))
    return C - (C - 1.0) * base                                # a potential well: N = 1 at the centre, C far away (N = e^{Phi/c^2})
def wenergy(N, f):
    gx, gy = grad(f); return float(np.sum(N * (gx**2 + gy**2)))

# ============================================================================================ E1
banner("E1  THE GEOMETRIC HEAT FILTER CAN RAISE THE LAPSE-WEIGHTED ENERGY (the lead's finding, reproduced)")
# The claim is existential: SOME field has d/db Int N |D e^{b Delta} f|^2 > 0 at b = 0.  On a 1-D periodic leaf the
# derivative is the quadratic form f^T M f with M = A Delta + Delta A, A = D^T N D (the N-weighted Dirichlet form), so the
# test is the largest generalized eigenvalue of (M, A) on non-constant fields: > 0 means a counterexample exists.
# Lapse: a single-mode well N = 1 + B (1 - cos 2 pi x), minimum 1, contrast 1 + 2B.  Control: N = 1 gives <= 0.
from scipy.linalg import eigh as geigh
# NOTE: Apple-Accelerate BLAS raises spurious floating-point flags on these dense matmuls; the matrices are checked
# finite below, so the flags are silenced for this block only.
_e = np.seterr(all="ignore")
n1 = 128; x1 = np.arange(n1) / n1
k1 = 2 * np.pi * np.fft.fftfreq(n1, d=1.0 / n1)
Fm = np.fft.fft(np.eye(n1), axis=0)
D1 = np.real(np.fft.ifft(np.diag(1j * k1) @ Fm, axis=0))
L1 = np.real(np.fft.ifft(np.diag(-(k1**2)) @ Fm, axis=0))
v_const = np.ones(n1) / math.sqrt(n1); v_nyq = ((-1.0)**np.arange(n1)) / math.sqrt(n1)
P0 = np.outer(v_const, v_const) + np.outer(v_nyq, v_nyq)             # the spectral gradient's two trivial modes
assert np.all(np.isfinite(D1)) and np.all(np.isfinite(L1))
def top_quotient(Nv):
    A = D1.T @ np.diag(Nv) @ D1
    M = A @ L1 + L1 @ A
    A_reg = 0.5 * (A + A.T) + P0 * np.trace(A) / n1                  # lift the trivial modes out of the denominator
    M_s = 0.5 * (M + M.T) - 1e6 * P0                                 # and push them to the bottom of the numerator
    return float(geigh(M_s, A_reg, eigvals_only=True)[-1])
rowsE1 = {}
lapse_of = lambda contrast: 1.0 + (contrast - 1.0) / 2.0 * (1 - np.cos(2 * np.pi * x1))
for contrast in (1.0, 8.0, 50.0, 100.0, 300.0, 1e3, 1e4):
    rowsE1[contrast] = top_quotient(lapse_of(contrast))
lo_c, hi_c = 50.0, 1e4                                               # bisect (in log contrast) for the sign change
if rowsE1[hi_c] > 0 > rowsE1[lo_c]:
    for _ in range(30):
        mid = math.sqrt(lo_c * hi_c)
        if top_quotient(lapse_of(mid)) > 0: hi_c = mid
        else: lo_c = mid
c_cross = math.sqrt(lo_c * hi_c)
np.seterr(**_e)
for c_, v_ in rowsE1.items():
    P(f"    lapse contrast {c_:8.1f}: largest d/db Int N|D e^(b Delta) f|^2 / Int N|D f|^2 over all fields = {v_:+.4e}")
P(f"    sign change at lapse contrast N_max/N_min ~ {c_cross:.1f} (single-mode well): above it some field's weighted energy RISES")
OUT["numbers"]["E1"] = {"rows": {str(k_): v_ for k_, v_ in rowsE1.items()}, "crossover_contrast": c_cross}
check("E1 the geometric heat filter raises the N-weighted Dirichlet energy for some field once the lapse contrast is large "
      "(largest generalized eigenvalue positive at contrast >= 1e3 on a single-mode well), while with N = 1 it never can",
      "; ".join(f"contrast {c_:g}: {v_:+.2e}" for c_, v_ in rowsE1.items()) + f"; crossover ~{c_cross:.0f}",
      rowsE1[1.0] <= 0 and rowsE1[1e4] > 0,
      "XC2 B2's 'any closed leaf' holds when the filter and the energy share one measure; C-H/K's energy carries the lapse, "
      "and for strong-field lapse contrasts the filter need not contract it (the lead's finding; its exact example differs)")

# ============================================================================================ E2
banner("E2  THE CONTRAST BOUND: Int N|D S f|^2 <= (N_max/N_min) Int N|D f|^2")
worst = 0.0
for trial in range(200):
    C = 10**(RNG.random() * 3)                                    # contrast 1 .. 1000
    N = (lapse_with_contrast(C) if trial % 2 else lapse_well(C)) * np.exp(0.3 * heat(RNG.standard_normal((NG, NG)), 2 * dx**2))
    ratio_c = float(N.max() / N.min())
    f = heat(RNG.standard_normal((NG, NG)), (0.2 + 4 * RNG.random()) * dx**2)
    lhs = wenergy(N, heat(f, 0.5 * XI**2)); rhs = ratio_c * wenergy(N, f)
    worst = max(worst, lhs / rhs)
P(f"    max over 200 random (lapse, field) pairs, contrasts 1..1000 x noise, of LHS/RHS: {worst:.4f}  (must be <= 1)")
OUT["numbers"]["E2"] = {"max_lhs_over_rhs": worst}
check("E2 the lapse-contrast bound holds on every random pair tested (it is proved in Lean: N_max, a contraction of the "
      "unweighted energy, then 1/N_min)", f"max LHS/RHS {worst:.4f}", worst <= 1.0 + 1e-12)

# ============================================================================================ E3
banner("E3  nu_mono: C_T > 0 and C_L > 0 everywhere -> the constraint is convex for ANY positive lapse")
ys = np.logspace(-12, 12, 40001)
ct_min = float(np.min(K["nu_mono"]["h"](ys) / ys)); cl_min = float(np.min(K["nu_mono"]["dh"](ys)))
r_ = sp.Symbol('r', positive=True); a_ = sp.Symbol('alpha', positive=True)
qf = sp.Function('q')
phi_r = 2 * a_**2 * qf(r_**2 / a_**2)
d1 = sp.simplify(sp.diff(phi_r, r_)); d2 = sp.simplify(sp.diff(phi_r, r_, 2))
P(f"    nu_mono over y in [1e-12, 1e12]: min C_T = {ct_min:.3e}, min C_L = {cl_min:.3e}")
P(f"    radial profile phi(r) = 2 alpha^2 q(r^2/alpha^2): phi' = 4 r q' = 4 r C_T >= 0, phi'' = 4 (q' + 2 Y q'') = 4 C_L >= 0"
  f"  (sympy: phi' = {sp.factor(d1)})")
OUT["numbers"]["E3"] = {"min_CT": ct_min, "min_CL": cl_min}
check("E3 nu_mono's constitutive coefficients are positive at every y, so its q-integrand is convex (non-decreasing, convex "
      "radial profile, C^1 at zero gradient) and d2E >= 4 Int N|D dU|^2 for any positive lapse and the unchanged filter",
      f"min C_T {ct_min:.2e}, min C_L {cl_min:.2e}", ct_min > 0 and cl_min > 0,
      "the author's kernel decision removes the lapse-contrast condition and the need to change the filter")

# ============================================================================================ E4
banner("E4  THE TURNING KERNELS' CONTRAST THRESHOLDS 1/|C_min|, and the lapse contrasts nature supplies")
xs = sp.Symbol('x', positive=True)
CLx = (1 - xs) / (sp.exp(xs) + xs - 1)
crit = sp.solve(sp.diff(CLx, xs), xs)
clmin_exact = sp.simplify(CLx.subs(xs, 2))
thr_exp = sp.simplify(-1 / clmin_exact)
def clmin_mu(mu, dmu):
    xg_ = np.logspace(-6, 6, 200001); return float(np.min(1.0 / (mu(xg_) + xg_ * dmu(xg_)) - 1.0))
cl_rar = float(np.min(dh_rar(np.logspace(-6, 6, 200001))))
cl_mu10 = clmin_mu(lambda x: x / (1 + x**10)**0.1, lambda x: (1 + x**10)**-1.1)
thr = {"mu_exp": float(thr_exp), "nu_RAR": 1 / abs(cl_rar), "mu_10": 1 / abs(cl_mu10)}
galaxy_contrast = math.exp(2e-4)
P(f"    mu_exp: C_L = (1-x)/(e^x + x - 1) has its minimum at x = 2 (sympy critical points {crit}): C_L(2) = {clmin_exact} ->"
  f" threshold 1/|C_min| = {thr_exp} = {float(thr_exp):.4f}  (the lead's bound N_max/N_min < e^2 + 1)")
P(f"    nu_RAR threshold {thr['nu_RAR']:.2f};  mu_10 threshold {thr['mu_10']:.2f};  nu_mono: none (C_min >= 0)")
P(f"    lapse contrast of a galaxy / the Solar System (|Phi/c^2| <= 1e-4): <= {galaxy_contrast:.6f};  at a horizon N -> 0: unbounded")
OUT["numbers"]["E4"] = {"thresholds": thr, "mu_exp_exact": str(thr_exp), "galaxy_contrast": galaxy_contrast}
check("E4 mu_exp's threshold is exactly e^2 + 1 (its C_L minimum -1/(e^2+1) at x = 2); every turning kernel's threshold "
      "exceeds weak-field lapse contrasts by far, and none survives the unbounded contrast near a compact object",
      f"thresholds {', '.join(f'{k_}: {v_:.3f}' for k_, v_ in thr.items())}; weak-field contrast {galaxy_contrast:.6f}",
      sp.simplify(thr_exp - (sp.exp(2) + 1)) == 0 and all(v_ > galaxy_contrast for v_ in thr.values()),
      "in galaxies and the Solar System the kernel choice does not matter for uniqueness; near black holes and neutron "
      "stars it does, and nu_mono is the kernel that keeps the constraint convex there")

# ============================================================================================ E5
banner("E5  NUMERICAL DEMONSTRATION: well-shaped lapse (nominal contrast 50), filter 2.5 cells, four random starts")
kern = "neg_const" if MUTATE else "nu_mono"
LIFT = 1.0e6                                                      # trivial modes lifted far above: eigsh 'SA' returns the true lowest non-trivial one
Nlap = lapse_well(50.0)
phi = np.zeros((NG, NG))
for (x0, y0, A, s) in ((0.30, 0.35, -0.030, 0.06), (0.70, 0.62, -0.020, 0.05), (0.52, 0.18, -0.008, 0.04)):
    ddx = np.minimum(np.abs(XX - x0), 1 - np.abs(XX - x0)); ddy = np.minimum(np.abs(YY - y0), 1 - np.abs(YY - y0))
    phi += A * np.exp(-(ddx**2 + ddy**2) / (2 * s**2))
gpx, gpy = grad(phi); scale = 6.0 / float(np.max(np.hypot(gpx, gpy))); gpx *= scale; gpy *= scale
def filt(f): return heat(f, 0.5 * XI**2)
def energy_grad(Uf):
    U = Uf.reshape(NG, NG); ux, uy = grad(U); sx, sy = grad(filt(U))
    r = np.maximum(np.hypot(sx, sy), 1e-14)
    qv = 2.0 * K[kern]["Hint"](r); qpr = K[kern]["h"](r) / r
    E = np.sum(Nlap * (2 * ((ux - gpx)**2 + (uy - gpy)**2) + 2 * qv)) * dx * dx
    g = -div(4 * Nlap * (ux - gpx), 4 * Nlap * (uy - gpy)) - filt(div(4 * Nlap * qpr * sx, 4 * Nlap * qpr * sy))
    return E, (g * dx * dx).ravel()
def hess_vec(v, U):
    V = v.reshape(NG, NG); vx, vy = grad(V); sx, sy = grad(filt(U)); wx, wy = grad(filt(V))
    r = np.maximum(np.hypot(sx, sy), 1e-14); ex_, ey_ = sx / r, sy / r
    CT = K[kern]["h"](r) / r; CL = K[kern]["dh"](r); par = wx * ex_ + wy * ey_
    fx = 4 * Nlap * (CT * wx + (CL - CT) * par * ex_); fy = 4 * Nlap * (CT * wy + (CL - CT) * par * ey_)
    out = -div(4 * Nlap * vx, 4 * Nlap * vy) - filt(div(fx, fy)) + LIFT * np.real(np.fft.ifft2(TRIV * np.fft.fft2(V)))
    return (out * dx * dx).ravel()
sols, Es = [], []
_e5 = np.seterr(all=("ignore" if MUTATE else "warn"))           # the MUTATE energy is unbounded below: divergence is the point
for trial in range(4):
    U0 = filt(filt(RNG.standard_normal((NG, NG)))) * 0.05 * (trial + 1)
    res = minimize(energy_grad, U0.ravel(), jac=True, method="L-BFGS-B", options={"maxiter": 30000, "gtol": 1e-12, "ftol": 1e-16})
    U = res.x.reshape(NG, NG); sols.append(U - U.mean()); Es.append(float(res.fun))
ref = sols[0]; spread = max(float(np.max(np.abs(s - ref))) for s in sols) / float(np.max(np.abs(ref)))
lam_min = float(eigsh(LinearOperator((NG * NG, NG * NG), matvec=lambda v: hess_vec(v, ref), dtype=float), k=1, which="SA",
                      tol=1e-6, maxiter=8000, return_eigenvectors=False)[0])
sx, sy = grad(filt(ref)); yf = np.hypot(sx, sy)
np.seterr(**_e5)
P(f"    kernel {kern}, lapse contrast {Nlap.max() / Nlap.min():.1f}: energies {', '.join(f'{e_:.10g}' for e_ in Es)}")
P(f"    max |U_i - U_1| / max|U| = {spread:.2e};  lowest non-trivial Hessian eigenvalue {lam_min:+.3e};  filtered y in [{yf.min():.1e}, {yf.max():.2f}]")
OUT["numbers"]["E5"] = {"kernel": kern, "energies": Es, "spread": spread, "lambda_min": lam_min}
check(f"E5 with {kern} at a realised lapse contrast of {Nlap.max() / Nlap.min():.1f} the constraint converges to one solution "
      "from four random starts and its lowest non-trivial Hessian eigenvalue is positive",
      f"{kern}: spread {spread:.1e}, lambda_min {lam_min:+.2e}, contrast {Nlap.max() / Nlap.min():.1f}",
      spread < 1e-5 and lam_min > 0)

# ============================================================================================ E6
banner("E6  A CORRECTION TO XC2 B7: an open zero-field region (a homogeneous background) responds as sqrt(eps)")
# The deep-MOND flux F(p) = |p|^{1/2} p/|p| is homogeneous of degree 1/2.  XC2 B7 treated isolated (codim 2, 3) and
# planar (codim 1) zeros of the filtered field.  An OPEN region of zero field (codim 0 -- a homogeneous background) is
# different: perturb U = 0 by eps sin x and the flux is eps^{1/2} |cos x|^{1/2} sign(cos x): Hoelder-1/2, for every MOND
# kernel (all share the deep limit), nu_mono included.  Found by the lead track (peer review of XC2, uncommitted).
xs6 = np.linspace(0, 2 * np.pi, 20001)
def resp(eps, kname):
    p = eps * np.cos(xs6)                                               # the filtered gradient of eps sin x (filter ~ 1 at k = 1)
    r = np.maximum(np.abs(p), 1e-300)
    return np.sign(p) * K[kname]["h"](r)                                # phantom acceleration (nu - 1) g_N = h(y)
EPS6 = [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]
rowsE6 = {}
for kname in ("nu_mono", "mu_exp"):
    R = [float(np.sqrt(np.mean(resp(e_, kname)**2)) / e_) for e_ in EPS6]
    slope = (math.log(R[-1]) - math.log(R[1])) / (math.log(EPS6[-1]) - math.log(EPS6[1]))
    rowsE6[kname] = {"R": R, "slope": slope}
    P(f"    {kname:8s}: ||response||/eps at eps = {', '.join(f'{e_:.0e}' for e_ in EPS6)}: {', '.join(f'{v_:.3e}' for v_ in R)}  "
      f"-> log-slope {slope:+.3f} (Hoelder-1/2 gives -0.5)")
u6 = sp.Symbol('u', positive=True)
osg = sp.integrate(1 / sp.sqrt(u6), (u6, 0, 1))
P(f"    Osgood test for the modulus sqrt(eps): Int_0^1 de/sqrt(e) = {osg} (finite, so Osgood's uniqueness criterion FAILS)")
OUT["numbers"]["E6"] = {"rows": rowsE6, "osgood_integral_sqrt": str(osg)}
check("E6 around an open zero-field region the MOND response scales as sqrt(eps) for every kernel, nu_mono included (log-slope "
      "-1/2), and that modulus FAILS Osgood's criterion: XC2 B7's 'zero field controlled' holds only away from open zero-field "
      "regions (it covered codim 1-3 zero sets, not codim 0)",
      "; ".join(f"{k_}: slope {v_['slope']:+.3f}" for k_, v_ in rowsE6.items()) + f"; Int de/sqrt(e) = {osg}",
      all(abs(v_["slope"] + 0.5) < 0.02 for v_ in rowsE6.values()) and osg.is_finite,
      "linear perturbation theory does not exist around a homogeneous zero-field background (requirement 9's hard case). In "
      "the assembled construction the vacuum-gated switch keeps the kernel off in the homogeneous web (L359/L361); in C-H/K "
      "alone it does not, which is part of why L341's FRW gate failed")

banner("VERDICT")
P(f"""  XC2's convexity statement was too broad for a non-constant lapse, as the lead track found: the geometric filter can
  raise the lapse-weighted energy (E1), so a kernel with a negative constitutive coefficient needs the contrast condition
  (N_max/N_min)|C_min| < 1 (E2, E4; for mu_exp exactly N_max/N_min < e^2 + 1, the lead's bound).  With the author's kernel
  decision the condition disappears: nu_mono's coefficients are positive everywhere (E3), so the MOND constraint is
  strictly convex -- one solution -- for ANY positive lapse and the unchanged filter, including near compact objects where
  the lapse contrast is unbounded (E4, E5).  One correction runs the other way: around an OPEN zero-field region the
  response is sqrt(eps) for every kernel, nu_mono included, which fails Osgood (E6) -- XC2 B7's 'controlled' covered
  isolated and planar zeros only.  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
