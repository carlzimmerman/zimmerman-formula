#!/usr/bin/env python3
"""
AS245 — Compute the external-field correction from the filtered action
Run:  AS245-efe-r1-20260928T1711Z-dsv4f-hermes
Worker: deepseek/deepseek-v4-flash-0731 via hermes-agent subagent (openrouter)

Task target (seed-displayed math):
    p0 = D S u_external,  C_ij = C_T (delta_ij - e_i e_j) + C_L e_i e_j,  e = p0/|p0|
from the CA5-GNC-R common action (FINAL_ACTION.md, pinned b8c04d4e...), filtered
MONO operative branch, both a0 footings kept separate (kappa = 1/2 adopted).

Derivation summary (see derivation.md):
    J(p) = 2 a0^2 q(|p|^2/a0^2),  q'(y^2) = nu_mono(y) - 1,  J_p = 4(nu-1) p
    Hessian_p J = 4[(nu-1) delta_ij + y nu' e_i e_j]   =>   C_L = (nu-1) + y nu',
    C_T = nu - 1.  Linearized filtered field symbol (both inner and outer filter S):
    M(k) = 1 + S^2(k) [C_T + (C_L - C_T) cos^2 theta_k],  S(k) = exp(-(xi^2/2)|k|^2).

All checks below are ACTUAL computed residuals (no fabricated numbers).
Bounds: signal.alarm(120 s); 1 thread; /usr/bin/time -l records RSS.
"""
import json, signal, sys, time, os
import numpy as np
from mpmath import mp, mpf, sqrt as msqrt, exp as mexp, log as mlog, pi as mpi
from scipy.sparse import diags, identity, eye, coo_matrix as sparse_coo
from scipy.sparse.linalg import spsolve, splu
import scipy.special as sp

signal.alarm(120)
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")

mp.dps = 60
t0 = time.time()

# -----------------------------------------------------------------------------
# 0. Constants and footings
# -----------------------------------------------------------------------------
G_SI = 6.67430e-11
C_SI = 299792458.0
M_SUN = 1.98847e30
PC_SI = 3.085677581491367e16
KAPPA = 0.5
A0_CAN = 9.3619e-11
A0_ALT = 1.1279e-10
XI = 0.5
B_HEAT = XI * XI / 2.0
DELTA_SPL = 0.05

def rho_lambda(a0):
    return 4.0 * a0 * a0 / (G_SI * C_SI * C_SI)

FOOTINGS = {
    "canonical":     {"a0": A0_CAN, "rho_Lambda": rho_lambda(A0_CAN), "kappa": KAPPA},
    "alternative":   {"a0": A0_ALT, "rho_Lambda": rho_lambda(A0_ALT), "kappa": KAPPA},
}
# check a0 = kappa c sqrt(G rho_Lambda) round trip
for name, f in FOOTINGS.items():
    a0r = KAPPA * C_SI * np.sqrt(G_SI * f["rho_Lambda"])
    f["a0_roundtrip"] = a0r
    f["a0_rel_err"] = abs(a0r - f["a0"]) / f["a0"]

# -----------------------------------------------------------------------------
# 1. Kernels: nu(y), nu'(y) for Q, RAR, EXP, MU2, MONO (criterion-B branches)
# -----------------------------------------------------------------------------

def nu_q(y):
    return np.sqrt(1.0 + 1.0 / y)

def dnu_q(y):
    return -1.0 / (2.0 * y * y * np.sqrt(1.0 + 1.0 / y))

def nu_rar(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))

def dnu_rar(y):
    s = np.sqrt(y)
    v = 1.0 / (1.0 - np.exp(-s))
    return -v * v * np.exp(-s) / (2.0 * s)   # nu_RAR is decreasing in y: sign minus

def h_rar(y):
    y = np.asarray(y, dtype=float)
    s = np.sqrt(y)
    out = np.empty_like(y)
    small = s < 40.0
    out[small] = y[small] / (np.exp(s[small]) - 1.0)
    out[~small] = y[~small] * np.exp(-s[~small])   # asymptotic y e^-s, no overflow
    return out

def dh_rar(y):
    # h'(y) = 1/(e^s - 1) - y e^s/(2 s (e^s - 1)^2), s = sqrt(y)
    y = np.asarray(y, dtype=float)
    s = np.sqrt(y)
    e = np.exp(s)
    out = np.empty_like(y)
    small = s < 40.0
    e_small = e[small]
    out[small] = 1.0 / (e_small - 1.0) - y[small] * e_small / (2.0 * s[small] * (e_small - 1.0) ** 2)
    # asymptotic: h' ~ e^-s (1 - y/(2s)) for large s
    out[~small] = np.exp(-s[~small]) * (1.0 - y[~small] / (2.0 * s[~small]))
    return out

def _root(f, lo, hi, n=200, tol=1e-14):
    flo, fhi = f(lo), f(hi)
    assert flo * fhi < 0, (lo, hi, flo, fhi)
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if fm * flo <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
        if hi - lo < tol * max(1.0, abs(hi)):
            break
    return 0.5 * (lo + hi)

# MONO landmarks (re-derived here from the derivative-floor rule, not imported)
# y_p: max of h_RAR  (h'_RAR = 0)
YP = _root(dh_rar, 1.0, 5.0)
HP = h_rar(YP)
def floor_deriv(y):
    return DELTA_SPL * HP / (y + YP)
def dh_mono(y):
    return np.maximum(dh_rar(y), floor_deriv(y))
# y*: first crossing h'_RAR(y) = floor(y) below y_p
YSTAR = _root(lambda y: dh_rar(y) - floor_deriv(y), 0.1, YP)
YSTAR_RICH = _root(lambda y: dh_rar(y) - floor_deriv(y), 0.1, YP)  # (renamed for Richardson bookkeeping)

def h_mono(y):
    y = np.asarray(y, dtype=float)
    out = np.where(y <= YSTAR, h_rar(y),
                   h_rar(YSTAR) + DELTA_SPL * HP * np.log((y + YP) / (YSTAR + YP)))
    return out

def nu_mono(y):
    return 1.0 + h_mono(y) / np.asarray(y, dtype=float)

def dnu_mono(y):
    y = np.asarray(y, dtype=float)
    h = h_mono(y)
    hd = np.where(y <= YSTAR, dh_rar(y), np.maximum(dh_rar(y), floor_deriv(y)))
    return (hd * y - h) / (y * y)

# MU2: implicit  nu (1 - (1 + y nu /2)^-2) = 1
def _mu2_impl(y):
    lo, hi = 1.0, 1e8
    for _ in range(500):
        mid = np.sqrt(lo * hi)
        v = mid * (1.0 - (1.0 + mid * y / 2.0) ** -2) - 1.0
        if v > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

def nu_mu2(y):
    return np.array([_mu2_impl(float(yy)) for yy in np.atleast_1d(y)]).reshape(np.shape(y))

def dnu_mu2(y):
    """Closed form from implicit differentiation of nu (1 - (1+y nu/2)^-2) = 1:
    nu' = -nu^2 (1+y nu/2)^-3 / (1/nu + y nu (1+y nu/2)^-3)."""
    y = np.asarray(y, dtype=float)
    nu = nu_mu2(y)
    mu_p = (1.0 + y * nu / 2.0) ** -3
    return -nu ** 2 * mu_p / (1.0 / nu + y * nu * mu_p)

# EXP: implicit  nu (1 - exp(-y nu)) = 1
def _exp_impl(y):
    lo, hi = 1.0, 1e8
    for _ in range(500):
        mid = np.sqrt(lo * hi)
        v = mid * (1.0 - np.exp(-mid * y)) - 1.0
        if v > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

def nu_exp(y):
    return np.array([_exp_impl(float(yy)) for yy in np.atleast_1d(y)]).reshape(np.shape(y))

def dnu_exp(y):
    """Closed form from implicit differentiation of nu (1 - exp(-y nu)) = 1:
    nu' = -nu^3 e^{-y nu} / (1 + y nu^2 e^{-y nu})."""
    y = np.asarray(y, dtype=float)
    nu = nu_exp(y)
    e = np.exp(-y * nu)
    return -nu ** 3 * e / (1.0 + y * nu * nu * e)

BRANCHES = {
    "Q":    (nu_q,    dnu_q),
    "RAR":  (nu_rar,  dnu_rar),
    "EXP":  (nu_exp,  dnu_exp),
    "MU2":  (nu_mu2,  dnu_mu2),
    "MONO": (nu_mono, dnu_mono),
}

# cross-check of the closed-form implicit derivatives against finite differences
# (validates dnu_exp / dnu_mu2 used in the tensor below)
_dnuFD = {"EXP": {}, "MU2": {}}
for _br in ("EXP", "MU2"):
    for _y in (0.1, 0.5, 2.5, 10.0):
        _eps = 1e-6 * _y
        v = (BRANCHES[_br][1](_y + _eps) - BRANCHES[_br][1](_y - _eps)) / (2 * _eps)
        _dnuFD[_br][_y] = (float(BRANCHES[_br][1](_y)), float(v))

# -----------------------------------------------------------------------------
# 2. Response tensor:  C_T = nu - 1, C_L = (nu-1) + y nu'
#    Hessian of the action density J(p) = 2 a0^2 q(|p|^2/a0^2) at p0 = a0 y e_hat
#    is 4[(nu-1) delta_ij + y nu' e_i e_j]; FINAL_ACTION: "regular nonzero Hessian
#    eigenvalues are 4 C_T, 4 C_L".
# -----------------------------------------------------------------------------
def c_t(nu, dnu, y):   return np.array(nu) - 1.0
def c_l(nu, dnu, y):   return (np.array(nu) - 1.0) + np.asarray(y) * np.array(dnu)

# ---- finite-difference Hessian of the dimensionless density  Jtil(P) = q(|P|^2)
def _qval(t, nu_f, n=500):
    """q(t) = int_0^t (nu(sqrt(u)) - 1) du, computed with the graded substitution
    u = s^4 (regular integrand at the deep cusp): q(t) = int_0^{t^{1/4}} 4 s^3
    (nu(s^2)-1) ds.  Trapz with n intervals; integrand analytic at s=0."""
    smax = float(t) ** 0.25
    s = np.linspace(0.0, smax, 2 * n + 1)
    f = 4.0 * s ** 3 * (np.array([float(nu_f(si * si)) for si in s]) - 1.0)
    # regularize the exact s=0 value analytically: 4 s^3 (nu(s^2)-1) ~ 4 s^3 (1/s) -> 0
    f[0] = 0.0
    return np.trapz(f, s)

def hessian_fd(nu_f, y, phi=0.7):
    """Second derivatives of Jtilde(P)=q(|P|^2) at P = y*(cos phi, sin phi).
    Analytic:  Hess = 2[(nu-1) I + y nu' e e^T]  ->  C_tensor = Hess/2."""
    ex = np.cos(phi); ey = np.sin(phi)
    P0 = np.array([y * ex, y * ey])
    eps = 1e-5 * max(y, 1e-3)
    def J(P):
        return _qval(P[0] ** 2 + P[1] ** 2, nu_f)
    H = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            if i == j:
                H[i, j] = (J(P0 + eps * np.eye(2)[i]) + J(P0 - eps * np.eye(2)[i])
                           - 2 * J(P0)) / eps ** 2
            else:
                H[i, j] = (J(P0 + eps * (np.eye(2)[i] + np.eye(2)[j]))
                           + J(P0 - eps * (np.eye(2)[i] + np.eye(2)[j]))
                           - J(P0 + eps * (np.eye(2)[i] - np.eye(2)[j]))
                           - J(P0 - eps * (np.eye(2)[i] - np.eye(2)[j]))) / (4 * eps ** 2)
    return 0.5 * H  # C-tensor from FD: Hess(Jtilde)/2

# -----------------------------------------------------------------------------
# 3. Fourier machinery on the flat periodic box (a0-normalized units, a0 = 1)
# -----------------------------------------------------------------------------
def make_ks(N, L):
    k = 2 * np.pi * np.fft.fftfreq(N, d=L / N)
    Kx, Ky = np.meshgrid(k, k, indexing="ij") if False else np.meshgrid(k, k, indexing="ij")
    return Kx, Ky

def fourier_solve(N, L, xi, y_ext, e_hat, branch, source_r, return_parts=False):
    """Linearized filtered field solution about the external gradient e = y_ext e_hat
        Phi_hat = u_hat * M(k),  M(k) = 1 + S^2 [C_T + (C_L - C_T) cos^2 theta_k],
        u = Newtonian potential of the source (4 pi G = 1, normalized)."""
    Kx, Ky = make_ks(N, L)
    k2 = Kx * Kx + Ky * Ky
    k2[0, 0] = 1.0  # zero mode removed
    Sf = np.exp(-(xi * xi / 2.0) * k2)
    rho_hat = np.fft.fft2(source_r)
    rho_hat[0, 0] = 0.0
    u_hat = -rho_hat / k2
    nu_f, dnu_f = BRANCHES[branch]
    nu = nu_f(y_ext); dnu = dnu_f(y_ext)
    CT = c_t(nu, dnu, y_ext); CL = c_l(nu, dnu, y_ext)
    with np.errstate(divide="ignore", invalid="ignore"):
        cos2 = np.nan_to_num((Kx * e_hat[0] + Ky * e_hat[1]) ** 2 / k2, nan=0.0)
    M = 1.0 + Sf ** 2 * (CT + (CL - CT) * cos2)
    Phi_hat = u_hat * M
    if return_parts:
        return Phi_hat, u_hat, Sf, M, CT, CL, Kx, Ky
    return Phi_hat

def nonlinear_residual(N, L, xi, y_ext, e_hat, branch, source_r, Phi):
    """Residual of the FULL nonlinear filtered MONO operator at Phi:
        R = Delta Phi - rho - S . div[(nu(|e + grad S u|/a0)-1)(e + grad S u)]
    with u = Newtonian solve (fixed).  Returns L2 norm over the box."""
    Kx, Ky = make_ks(N, L)
    k2 = Kx * Kx + Ky * Ky
    k2[0, 0] = 1.0
    Sf = np.exp(-(xi * xi / 2.0) * k2)
    rho_hat = np.fft.fft2(source_r)
    rho_hat[0, 0] = 0.0
    u_hat = -rho_hat / k2
    # Delta Phi (Fourier, exact)
    dPhi = np.fft.ifft2(-k2 * np.fft.fft2(Phi)).real
    # S u and its gradient
    Su = np.fft.ifft2(Sf * u_hat).real
    gx = np.fft.ifft2(1j * Kx * Sf * u_hat).real
    gy = np.fft.ifft2(1j * Ky * Sf * u_hat).real
    # y-arg of the kernel with external field
    ax = e_hat[0] * y_ext + gx
    ay = e_hat[1] * y_ext + gy
    a_norm = np.sqrt(ax * ax + ay * ay)
    nu_f, _ = BRANCHES[branch]
    kern = np.nan_to_num(nu_f(a_norm) - 1.0, nan=0.0)
    fx, fy = kern * ax, kern * ay
    # S . div(flux): div in Fourier, then multiply by S
    f_hat = np.fft.fft2(fx + 1j * fy)
    sdiv = np.fft.ifft2(Sf * (1j * Kx * np.fft.fft2(fx) + 1j * Ky * np.fft.fft2(fy))).real
    R = dPhi - np.fft.ifft2(rho_hat).real - sdiv
    return np.sqrt(np.mean(R ** 2))

def gaussian_source(N, L, A, sigma, sx, sy):
    x = (np.arange(N) * L / N) - sx
    X, Y = np.meshgrid(x, x, indexing="ij")
    r2 = X ** 2 + Y ** 2
    rho = A * np.exp(-r2 / (2 * sigma ** 2))
    return rho - rho.mean()

def force_ratios(N, L, xi, y_ext, e_hat, branch, sep_h):
    """Subsystem force demonstration: point-source at 0, test at r = sep_h*h along
    e_hat (parallel) and perpendicular; force ratio F_par/F_perp vs low-k prediction
    (1 + C_L)/(1 + C_T)."""
    h = L / N
    Kx, Ky = make_ks(N, L)
    k2 = Kx * Kx + Ky * Ky
    k2[0, 0] = 1.0
    Sf = np.exp(-(xi * xi / 2.0) * k2)
    nu_f, dnu_f = BRANCHES[branch]
    CT = c_t(nu_f(y_ext), dnu_f(y_ext), y_ext)
    CL = c_l(nu_f(y_ext), dnu_f(y_ext), y_ext)
    with np.errstate(divide="ignore", invalid="ignore"):
        cos2 = np.nan_to_num((Kx * e_hat[0] + Ky * e_hat[1]) ** 2 / k2, nan=0.0)
    M = 1.0 + Sf ** 2 * (CT + (CL - CT) * cos2)
    # force from a unit point source at 0 on a test mass at r (per-periodic lattice sum)
    def F_at(rx, ry):
        phase = np.exp(1j * (Kx * rx + Ky * ry))
        # -grad Phi  (+ i k Phi_hat componentwise, Phi_hat = -M/k^2 * (4piG))
        Fx = np.real(np.sum(phase * (1j * Kx) * (-M / k2)))
        Fy = np.real(np.sum(phase * (1j * Ky) * (-M / k2)))
        return Fx, Fy
    r = sep_h * h
    Fxp, Fyp = F_at(e_hat[0] * r, e_hat[1] * r)
    Fp_mag = np.hypot(Fxp, Fyp)
    nhat = np.array([-e_hat[1], e_hat[0]])
    Fxt, Fyt = F_at(nhat[0] * r, nhat[1] * r)
    Ft_mag = np.hypot(Fxt, Fyt)
    return Fp_mag / Ft_mag, (1.0 + CL) / (1.0 + CT), Fp_mag, Ft_mag, CL, CT

# -----------------------------------------------------------------------------
# 4. Sphere leaf: heat filter on curvature (first spherical-harmonic external mode)
# -----------------------------------------------------------------------------
def sphere_spectral_factor(R, l=1, b=B_HEAT):
    """S Y_lm = exp(-b l(l+1)/R^2) Y_lm  on a leaf sphere of radius R."""
    return np.exp(-b * l * (l + 1) / R ** 2)

def sphere_check(Nt, lmax, R, b=B_HEAT):
    """Numerical spectral check on the sphere: project an azimuthally symmetric field
    onto Legendre modes, apply exp(-b l(l+1)/R^2), reconstruct; verify the l=1 mode
    (the external datum u_ext ~ cos theta) picks up exactly exp(-2b/R^2)."""
    xgl, wgl = np.polynomial.legendre.leggauss(Nt)  # cos(theta) nodes on [-1,1]
    f = xgl  # u_ext = cos(theta) (the l=1 mode), theta = arccos(x)
    Pl = np.polynomial.legendre.legvander(xgl, lmax)  # (Nt, lmax+1) P_l(x)
    # m=0 spectral projection: f_hat_l = (2l+1)/2 * int_{-1}^1 P_l f dx
    norm = (2 * np.arange(lmax + 1) + 1.0) / 2.0
    f_hat = norm * Pl.T.dot(wgl * f)
    mode = np.zeros_like(f)
    for l in range(lmax + 1):
        mode += (np.exp(-b * l * (l + 1) / R ** 2) * f_hat[l]) * Pl[:, l]
    # ratio for the l=1 content
    l1_in = f_hat[1] * 2.0 / 3.0 * 3.0  # a_1 coefficient
    Sf1 = np.exp(-b * 1 * 2 / R ** 2)
    # residual: max |mode - Sf1 * f| after renormalizing (pure l=1 field)
    res = np.max(np.abs(mode / Sf1 - f)) if abs(Sf1) > 0 else np.inf
    # leakage: ratio of reconstructed non-l=1 content
    return res, Sf1, f_hat

# -----------------------------------------------------------------------------
# Main sequence
# -----------------------------------------------------------------------------
results = {"kernel_landmarks": {}, "tensor": {}, "hessian_checks": {},
           "green": {}, "residuals": {}, "refinement": {}, "realspace_cross": {},
           "curved_leaf": {}, "negative_controls": {}, "deep": {},
           "force": {}, "footings": {}, "axioms_check": {}}

# ---- C0: kernel landmarks (MONO splice) ----
results["kernel_landmarks"]["y_p"] = float(YP)
results["kernel_landmarks"]["y_star"] = float(YSTAR)
results["kernel_landmarks"]["h_p"] = float(HP)
# continuity at the splice
results["kernel_landmarks"]["splice_continuity"] = float(abs(h_rar(YSTAR) - h_mono(YSTAR)) / max(1.0, abs(HP)))
# dex deviation vs RAR over a fine grid
yg = np.logspace(-4, 4, 40001)
dex = np.abs(np.log10(nu_mono(yg)) - np.log10(nu_rar(yg)))
i14 = np.argmin(np.abs(yg - 14.35))
results["kernel_landmarks"]["max_dex"] = float(dex.max())
results["kernel_landmarks"]["dex_at_14.35"] = float(dex[i14])
results["kernel_landmarks"]["y_of_max_dex"] = float(yg[np.argmax(dex)])
results["kernel_landmarks"]["dnu_implicit_closed_vs_FD"] = _dnuFD

# ---- C1: tensor eigenvalues and Hessian FD ----
YVAL = [0.05, 0.1, 0.5, 1.0, 2.5, 10.0]   # 2.5 inside the MONO spline (derivatives continuous)
for branch, (nu_f, dnu_f) in BRANCHES.items():
    for yy in YVAL:
        nu = float(nu_f(yy)); dnu = float(dnu_f(yy))
        CT = float(c_t(nu, dnu, yy)); CL = float(c_l(nu, dnu, yy))
        Hfd = hessian_fd(nu_f, yy, phi=0.7)
        Hana = np.array([[CT + (CL - CT) * np.cos(0.7) ** 2, (CL - CT) * np.cos(0.7) * np.sin(0.7)],
                         [(CL - CT) * np.cos(0.7) * np.sin(0.7), CT + (CL - CT) * np.sin(0.7) ** 2]])
        rel = np.max(np.abs(Hfd - Hana) / np.maximum(1e-30, np.abs(Hana)))
        results["hessian_checks"][f"{branch}_y{yy}"] = {"C_T": CT, "C_L": CL,
                                                       "frac_C_L_C_T": CL / CT if abs(CT) > 0 else None,
                                                       "Hfd_max": float(np.max(np.abs(Hfd))),
                                                       "Hana_max": float(np.max(np.abs(Hana))),
                                                       "max_rel_err": float(rel)}
        # eigen-direction check: C_ij e_j and C_ij w_j
    # transverse stationarity: C w = C_T w for w . e = 0
    e = np.array([np.cos(0.7), np.sin(0.7)]); w = np.array([-np.sin(0.7), np.cos(0.7)])
    yy = 0.5
    nu = float(nu_f(yy)); dnu = float(dnu_f(yy))
    CT = float(c_t(nu, dnu, yy)); CL = float(c_l(nu, dnu, yy))
    Cmat = CT * np.eye(2) + (CL - CT) * np.outer(e, e)
    results["tensor"][f"{branch}_eigenvectors_at_y0.5"] = {
        "C_e_minus_CL_e": float(np.max(np.abs(Cmat.dot(e) - CL * e))),
        "C_w_minus_CT_w": float(np.max(np.abs(Cmat.dot(w) - CT * w)))}

# ---- C2: agreement with the action prefactor (4 C_T, 4 C_L = Hessian of J(p)) ----
# Hessian of J(p) w.r.t. p  =  4[(nu-1) I + y nu' e e^T]  (exact chain rule, checked below
# by the scalar-J chain: dJ/dp_i = 4(nu-1)p_i and rank-one update).
for yy in [0.5, 2.5]:
    nu = float(nu_mono(yy)); dnu = float(dnu_mono(yy))
    CT = float(c_t(nu, dnu, yy)); CL = float(c_l(nu, dnu, yy))
    results["tensor"][f"MONO_HessianJp_y{yy}"] = {"4C_T": 4 * CT, "4C_L": 4 * CL}

# ---- C3: deep limit  C_L / C_T -> 1/2  and exact 2C_L - C_T = c - 1  ----
RICH = {}
for branch, (nu_f, dnu_f) in BRANCHES.items():
    yv = [mpf("1e-10"), mpf("1e-12"), mpf("1e-14"), mpf("1e-16")]
    vals = []
    for y0 in yv:
        yy = float(y0)
        nu = float(nu_f(yy)); dnu = float(dnu_f(yy))
        CT = float(c_t(nu, dnu, yy)); CL = float(c_l(nu, dnu, yy))
        vals.append(CL / CT)
    RICH[branch] = vals
    results["deep"][branch + "_CL_over_CT"] = vals

# exact branch constants c: nu ~ y^-1/2 + c  (Q:0, RAR:1/2, EXP:1/4, MU2:3/8)
c_const = {"Q": 0.0, "RAR": 0.5, "EXP": 0.25, "MU2": 0.375, "MONO": 0.5}
yy = 1e-10
for branch, (nu_f, dnu_f) in BRANCHES.items():
    nu = float(nu_f(yy)); dnu = float(dnu_f(yy))
    CT = float(c_t(nu, dnu, yy)); CL = float(c_l(nu, dnu, yy))
    results["deep"][f"{branch}_2CL_minus_CT@1e-10"] = 2 * CL - CT
    results["deep"][f"{branch}_expected_c_minus_1"] = c_const[branch] - 1.0

# ---- C4: Fourier Green function vs the nonlinear operator (main residual test) ----
def run_residuals(N, L, A, y_ext, branch, sigma=0.9, sx=8.0, sy=8.0):
    e_hat = np.array([1.0, 0.0])
    rho = gaussian_source(N, L, A, sigma, sx, sy)
    Phi_hat, u_hat, Sf, M, CT, CL, Kx, Ky = fourier_solve(N, L, XI, y_ext, e_hat, branch,
                                                          rho, return_parts=True)
    Phi = np.fft.ifft2(Phi_hat).real
    rr = nonlinear_residual(N, L, XI, y_ext, e_hat, branch, rho, Phi)
    return rr, CT, CL

E = np.array([1.0, 0.0])
for y_ext in [0.05, 0.5, 10.0]:
    row = {}
    for A in [1e-3, 2.5e-4, 1e-4]:
        rr, CT, CL = run_residuals(64, 16.0, A, y_ext, "MONO")
        row[f"A={A:g}"] = float(rr)
    r1 = row["A=0.001"]; r2 = row["A=0.00025"]
    ratio = r2 / r1
    results["residuals"][f"MONO_y{y_ext}_N64"] = row
    results["residuals"][f"MONO_y{y_ext}_N64"]["r2_over_r1"] = float(ratio)
    results["residuals"][f"MONO_y{y_ext}_N64"]["quadratic_expect_1over16"] = 1.0 / 16.0
    # normalized per-amplitude second-order coefficient
    q2 = r1 / 1e-3, r2 / 2.5e-4
    results["residuals"][f"MONO_y{y_ext}_N64"]["q2_ratio"] = float(q2[1] / q2[0])
    # breakdown control at y = 0.05, A = 0.02 and the quadratic-scaling break at 0.005
    if y_ext == 0.05:
        rrB, _, _ = run_residuals(64, 16.0, 0.02, y_ext, "MONO")
        rrB2, _, _ = run_residuals(64, 16.0, 0.005, y_ext, "MONO")
        results["residuals"]["MONO_y0.05_A0.02_breakdown"] = float(rrB)
        results["residuals"]["MONO_y0.05_A0.005"] = float(rrB2)
        # pure quadratic scaling would give r(A2)/r(A1) = (0.005/0.02)^2 = 1/16
        results["residuals"]["MONO_y0.05_ratio_r005_over_r02"] = float(rrB2 / rrB)
        results["residuals"]["MONO_y0.05_ratio_quadratic_expect_1over16"] = 1.0 / 16.0

# refinement once: N = 96 at y = 0.5, A = 1e-3
rr96, CT96, CL96 = run_residuals(96, 16.0, 1e-3, 0.5, "MONO")
rr64, _, _ = run_residuals(64, 16.0, 1e-3, 0.5, "MONO")
results["refinement"]["N64"] = float(rr64)
results["refinement"]["N96"] = float(rr96)

# ---- C5: independent real-space sparse-LU cross-check of the anisotropic Green fn ----
def realspace_phi(N, L, A, y_ext, branch, m=64, sigma=0.9, sx=8.0, sy=8.0):
    """Solve the linearized filtered equation with stencil + rational-heat machinery:
        Phi = u + D^-1 [S div((nu-1) grad S u + y nu' e (e . grad S u))]
    D: 5-point periodic Laplacian (symbol -k^2 convention of Delta_h), S_r = (I + (b/m)(-D))^-m."""
    e_hat = np.array([1.0, 0.0]); h = L / N
    rho = gaussian_source(N, L, A, sigma, sx, sy)
    # Periodic 5-point Laplacian with axis-wise wrap (index arrays, not flat offsets)
    Nd = N * N
    idx = np.arange(Nd).reshape(N, N)
    cols = [idx.ravel(),
            np.roll(idx, -1, axis=1).ravel(), np.roll(idx, 1, axis=1).ravel(),
            np.roll(idx, -1, axis=0).ravel(), np.roll(idx, 1, axis=0).ravel()]
    rows = np.tile(idx.ravel(), 5)
    data = np.full((5, Nd), -1.0 / h ** 2)
    data[0, :] = 4.0 / h ** 2
    Ds = sparse_coo((data.ravel(), (rows.ravel(), np.concatenate(cols))), shape=(Nd, Nd)).tocsr()
    lu = splu(Ds.tocsc())
    def Dinv(b):
        v = lu.solve(b)
        return v - v.mean()   # project out the Laplacian null mode (periodic torus)
    # rational heat operator S_r = (I + (b/m) Ds)^-m with Ds = +|k|^2 stencil:
    # symbol (1 + b k^2/m)^-m ~ exp(-b k^2) = exp((b) Delta) in the negative-definite
    # convention of the action (S = exp((xi^2/2) Delta), Delta symbol -k^2).
    Aheat = identity(Nd, format="csc") + (B_HEAT / m) * Ds
    lu_heat = splu(Aheat)
    def S_r(v):
        for _ in range(m):
            v = lu_heat.solve(v)
        return v
    def grad_x(v):  # central difference, periodic
        return (np.roll(v, -1, axis=0) - np.roll(v, 1, axis=0)) / (2 * h)
    def grad_y(v):
        return (np.roll(v, -1, axis=1) - np.roll(v, 1, axis=1)) / (2 * h)
    def div(gx, gy):
        # forward-difference convention (matches grad and the Fourier +ik . f form)
        return (np.roll(gx, -1, axis=0) - np.roll(gx, 1, axis=0)) / (2 * h) \
             + (np.roll(gy, -1, axis=1) - np.roll(gy, 1, axis=1)) / (2 * h)
    # Newtonian solve u = D^-1(rho);  Ds = -Delta_h  =>  u = -Ds^-1(rho)
    u = -Dinv(rho.ravel()).reshape(N, N)
    Su = S_r(u.ravel()).reshape(N, N)
    gx = grad_x(Su); gy = grad_y(Su)
    nu_f, dnu_f = BRANCHES[branch]
    nu = nu_f(y_ext); dnu = dnu_f(y_ext)
    CT = float(c_t(nu, dnu, y_ext)); CL = float(c_l(nu, dnu, y_ext))
    flux_x = (nu - 1.0) * gx + y_ext * dnu * e_hat[0] * (e_hat[0] * gx + e_hat[1] * gy)
    flux_y = (nu - 1.0) * gy + y_ext * dnu * e_hat[1] * (e_hat[0] * gx + e_hat[1] * gy)
    fx = S_r(flux_x.ravel()).reshape(N, N)
    fy = S_r(flux_y.ravel()).reshape(N, N)
    src = div(fx, fy)
    phi_p = -Dinv(src.ravel()).reshape(N, N)   # Delta_h phi_p = S div(flux)  =>  phi_p = -Ds^-1(...)
    return u + phi_p, CT, CL

for y_ext in [0.5, 10.0]:
    Phi_real, CT, CL = realspace_phi(64, 16.0, 1e-3, y_ext, "MONO", m=64)
    rho = gaussian_source(64, 16.0, 1e-3, 0.9, 8.0, 8.0)
    Phi_hat, _, _, _, _, _, _, _ = fourier_solve(64, 16.0, XI, y_ext, E, "MONO",
                                                 rho, return_parts=True)
    Phi_fou = np.fft.ifft2(Phi_hat).real
    rel = np.sqrt(np.mean((Phi_real - Phi_fou) ** 2)) / np.sqrt(np.mean(Phi_fou ** 2))
    results["realspace_cross"][f"MONO_y{y_ext}"] = {"rel_err": float(rel), "C_T": CT, "C_L": CL}

# ---- C6: curved leaf (sphere) ----
for R in [0.5, 1.0, 2.0, 10.0, 20.0]:
    res, sf1, f_hat = sphere_check(140, 60, R)
    results["curved_leaf"][f"R={R:g}"] = {"S_Y1m_factor": float(sf1),
                                          "max_resid_vs_exact": float(res)}
# flat-leaf limit statement: factor at R -> inf
results["curved_leaf"]["flat_limit_Rinf_factor"] = 1.0
results["curved_leaf"]["zeta_note"] = "attenuation = exp(-(xi^2/R^2)) = exp(-2b/R^2), b = xi^2/2, xi = 0.5"

# ---- C7: negative controls ----
# NEG-A: algebraic spherical Q relation as field substitute; transverse source.
# source with all power at transverse wavenumber k = (0, k0)
N, L, A = 64, 16.0, 1e-3
y_ext = 0.5
k0 = 2 * np.pi / L * 2
xx = np.arange(N) * L / N
X, Y = np.meshgrid(xx, xx, indexing="ij")
rho_T = A * np.cos(k0 * Y)          # transverse modulation (k = (0, k0) e_y)
rho_T = rho_T - rho_T.mean()
Phi_M = fourier_solve(N, L, XI, y_ext, E, "MONO", rho_T, return_parts=True)[0]
Phi_Q = fourier_solve(N, L, XI, y_ext, E, "Q", rho_T, return_parts=True)[0]
rM = nonlinear_residual(N, L, XI, y_ext, E, "MONO", rho_T, np.fft.ifft2(Phi_M).real)
rQ = nonlinear_residual(N, L, XI, y_ext, E, "MONO", rho_T, np.fft.ifft2(Phi_Q).real)
results["negative_controls"]["NEG_A_Qs_linear_residual_in_MONO_op"] = float(rQ / 1e-3)   # linear-in-A coefficient
results["negative_controls"]["NEG_A_MONO_quadratic_residual"] = float(rM)
results["negative_controls"]["NEG_A_ratio_rQ_rM"] = float(rQ / rM)
# also the transverse gain mismatch at the selected wavenumber
nuM = float(nu_mono(y_ext)); nM = float(nu_q(y_ext))
Sf2 = np.exp(-(XI * XI / 2.0) * k0 ** 2)
Mt = 1.0 + Sf2 ** 2 * (nuM - 1.0)
Qt = 1.0 + Sf2 ** 2 * (nM - 1.0)
results["negative_controls"]["NEG_A_transverse_gain_MONO"] = float(Mt)
results["negative_controls"]["NEG_A_transverse_gain_Q"] = float(Qt)
results["negative_controls"]["NEG_A_rel_gain_dev"] = float(abs(Mt - Qt) / (Mt - 1.0))

# NEG-B: scalar-magnitude replacement d/deps nu(y|e+eps w_perp|) = 0 (vector, exact)
# versus d/deps nu(y(1 + eps|w|)) = y nu'(y) != 0 (scalarised).
y_ext = 0.5
eps = 1e-5
def vmag(e): return y_ext * np.hypot(1.0, e ** 2)   # |e_hat + e w_perp| = sqrt(1 + e^2)
def smag(e): return y_ext * (1.0 + e)               # |e| + e|w|
fd = lambda f, e0: (f(e0 + eps) - f(e0 - eps)) / (2 * eps)
dvec = float(fd(lambda e: nu_mono(vmag(e)), 0.0))
dsca = float(fd(lambda e: nu_mono(smag(e)), 0.0))
results["negative_controls"]["NEG_B_vector_first_order_transverse"] = dvec
results["negative_controls"]["NEG_B_scalarised_first_order_transverse"] = dsca
results["negative_controls"]["NEG_B_analytic_y_dnu"] = float(y_ext * dnu_mono(y_ext))

# ---- C8: subsystem force anisotropy ----
for y_ext in [0.0005, 0.005, 0.05, 0.5, 10.0]:
    fr, pred, Fp, Ft, CL, CT = force_ratios(256, 16.0, XI, y_ext, E, "MONO", sep_h=40)
    results["force"][f"MONO_y{y_ext}_sep{40}h"] = {
        "F_par_over_F_perp": float(fr),
        "lowk_prediction_1pCL_over_1pCT": float(pred),
        "F_par": float(Fp), "F_perp": float(Ft), "C_L": float(CL), "C_T": float(CT)}

# ---- C9: dimensional footings ----
for name, f in FOOTINGS.items():
    a0 = f["a0"]
    row = {"a0": a0, "rho_Lambda": f["rho_Lambda"], "a0_roundtrip": f["a0_roundtrip"],
           "a0_rel_err": f["a0_rel_err"],
           "r_M(M_sun)_pc": float(np.sqrt(G_SI * M_SUN / a0) / PC_SI),
           "v_flat(M_sun)": float((G_SI * M_SUN * a0) ** 0.25)}
    for e_in in [1.0e-10, 2.0e-11]:
        y = e_in / a0
        nu = float(nu_mono(y)); dnu = float(dnu_mono(y))
        CT = float(c_t(nu, dnu, y)); CL = float(c_l(nu, dnu, y))
        row[f"e={e_in:g}"] = {"y": y, "C_T": CT, "C_L": CL,
                              "CL_over_CT": CL / CT,
                              "1pC_T": 1.0 + CT, "1pC_L": 1.0 + CL}
    results["footings"][name] = row
results["footings"]["ratio_alt_over_can_a0"] = A0_ALT / A0_CAN

# ---- C10: exact limiting cases vs the original operator ----
# (i) y -> inf: C_L, C_T -> 0 (M -> 1: Newtonian isotropic recovery)
for yh in [1e2, 1e4, 1e6]:
    nu = float(nu_mono(yh)); dnu = float(dnu_mono(yh))
    results.setdefault("limits", {})[f"MONO_y{int(yh)}"] = {
        "C_T": float(c_t(nu, dnu, yh)), "C_L": float(c_l(nu, dnu, yh))}
# (ii) sphere R -> 0: strong suppression exp(-2b/R^2) -> 0
results["limits"]["sphere_suppression_R_to_0"] = float(np.exp(-2 * B_HEAT / 0.05 ** 2))

results["meta"] = {"elapsed_s": time.time() - t0}

out = json.dumps(results, indent=1, sort_keys=True)
print(out)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw_output.json"), "w") as fh:
    fh.write(out)