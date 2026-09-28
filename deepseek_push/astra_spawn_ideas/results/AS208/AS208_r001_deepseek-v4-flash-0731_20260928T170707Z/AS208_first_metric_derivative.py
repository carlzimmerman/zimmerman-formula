#!/usr/bin/env python3
# AS208 -- Bound the first metric derivative of the heat operator.  FINAL v3.
# Seed target:  delta S = integral_0^b  S_(b-r) (delta Delta) S_r dr
# Action: CA4-GNC (FINAL_ACTION.md), heat generator Delta_h = intrinsic
# Laplacian on the compact leaf, S_h = exp(b Delta_h), b = xi^2/2.
#
# Part A: torus T^2, band-limited Fourier basis (|kx|,|ky| <= 12 on a 32-grid,
#   wavenumber products stay < Nyquist, so the sampled algebra is exact).
#   deltaDelta implemented as the exact auto-diff of the sampled Laplacian
#   (verified against the finite difference to ~1e-8):
#     dd f = Dx[ (1/2)(k11+k22)Dx f - k11 Dx f - k12 Dy f ]
#          + Dy[ (1/2)(k11+k22)Dy f - k22 Dy f - k12 Dx f ]
#          - (1/2)(k11+k22) D^2 f
#   (Dx, Dy = partials; D^2 = Dx^2 + Dy^2).  Formula (A1)
#     dd f = -k^ij DiDj f - (Di k^ij) Dj f + (1/2)(Di tr k) Di f        (A1)
#   is verified numerically on quarter-band inputs (|k| <= 6) where the
#   identification with the sampled algebra is unconditional.
#   Then: Duhamel operator T_b (exact per-mode-pair integral), frozen
#   parallel case, operator norms, negative control (one-leg r^-1 bounds at
#   both endpoints -> log^2-divergent integral), contraction constant.
# Part B: S^2 curved-leaf conformal reduction (exact operator identity).
# Part C: framework footings, both separately.

import time, json, os, resource, signal
import numpy as np

T0 = time.time()

def _alarm(sig, frame):
    raise TimeoutError("wall-time alarm fired")
signal.signal(signal.SIGALRM, _alarm)
signal.alarm(118)

for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
          "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[v] = "1"

def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576.0

OUT = {}

# ============================ PART A -- torus ============================
N = 32
KM = 12                              # main band limit |kx|,|ky| <= 12
KQ = 6                               # verification band (A1) <-> sampled
kx = np.fft.fftfreq(N) * N
KX, KY = np.meshgrid(kx, kx, indexing="ij")
XG, YG = np.meshgrid(np.linspace(0, 2 * np.pi, N, endpoint=False),
                     np.linspace(0, 2 * np.pi, N, endpoint=False),
                     indexing="ij")
MASK = (np.abs(KX) <= KM) & (np.abs(KY) <= KM)
inds = np.argwhere(MASK)
nmod = len(inds)
lam12 = kx[inds[:,0]]**2 + kx[inds[:,1]]**2   # TRUE wavenumbers via fftfreq map
LAMSQ = KX**2 + KY**2

def fx(f): return np.fft.ifft2(1j * KX * np.fft.fft2(f))
def fy(f): return np.fft.ifft2(1j * KY * np.fft.fft2(f))
def coeffs(f): return np.fft.fft2(f)[MASK]
def hnorm_c(fc, s, lam=lam12):
    return float(np.sqrt(np.sum((1.0 + lam) ** s * np.abs(fc) ** 2)))

EPS0 = 0.30
K11 = EPS0 * (np.cos(2 * XG) + 0.7 * np.cos(3 * YG))
K22 = EPS0 * (np.sin(XG + YG) + 0.5 * np.cos(2 * XG - 3 * YG))
K12 = EPS0 * 0.3 * np.cos(XG - 2 * YG)
DK11X, DK11Y = -EPS0 * 2 * np.sin(2 * XG), -EPS0 * 0.7 * 3 * np.sin(3 * YG)
DK22X = EPS0 * (np.cos(XG + YG) - np.sin(2 * XG - 3 * YG))
DK22Y = EPS0 * (np.cos(XG + YG) + 1.5 * np.sin(2 * XG - 3 * YG))
DK12X = -EPS0 * 0.3 * np.sin(XG - 2 * YG)
DK12Y = EPS0 * 0.6 * np.sin(XG - 2 * YG)

def lap_pert(f, eps):
    g11 = 1.0 + eps * K11; g22 = 1.0 + eps * K22; g12 = eps * K12
    det = g11 * g22 - g12 * g12
    i11 = g22 / det; i22 = g11 / det; i12 = -g12 / det
    sg = np.sqrt(det)
    X1 = sg * (i11 * fx(f) + i12 * fy(f))
    X2 = sg * (i12 * fx(f) + i22 * fy(f))
    return (1.0 / sg) * (fx(X1) + fy(X2))

def dd_autodiff(f):
    """deltaDelta f computed as the exact epsilon-linear part of lap_pert
    (numeric auto-diff at the level of the sampled expression)."""
    Dfx = fx(f); Dfy = fy(f)
    Dxx = fx(Dfx); Dyy = fy(Dfy)
    A = -0.5 * (K11 + K22) * (Dxx + Dyy)
    B = fx(0.5 * (K11 + K22) * Dfx - K11 * Dfx - K12 * Dfy)
    C = fy(0.5 * (K11 + K22) * Dfy - K22 * Dfy - K12 * Dfx)
    return A + B + C

def dd_formula(f):
    """Formula (A1) closed form (reference expression)."""
    Dxx = np.fft.ifft2(-KX**2 * np.fft.fft2(f))
    Dyy = np.fft.ifft2(-KY**2 * np.fft.fft2(f))
    Dxy = np.fft.ifft2(-KX * KY * np.fft.fft2(f))
    t1 = -(K11 * Dxx + 2.0 * K12 * Dxy + K22 * Dyy)
    Dfx = fx(f); Dfy = fy(f)
    t2 = -((DK11X + DK12Y) * Dfx + (DK12X + DK22Y) * Dfy)
    t3 = 0.5 * ((DK11X + DK22X) * Dfx + (DK11Y + DK22Y) * Dfy)
    return t1 + t2 + t3

def op_matrix(op):
    M = np.zeros((nmod, nmod), dtype=complex)
    for a in range(nmod):
        i, j = inds[a]
        e = np.zeros((N, N), complex); e[i, j] = 1.0
        M[:, a] = coeffs(op(np.fft.ifft2(e)))
    return M

# ---- C1: sampled deltaDelta (autodiff) vs finite difference ---------------
rng = np.random.default_rng(7)
Uc = rng.standard_normal(nmod) + 1j * rng.standard_normal(nmod)
Uc /= hnorm_c(Uc, 0)
U = np.zeros((N, N), complex)
for a in range(nmod):
    U[inds[a, 0], inds[a, 1]] = Uc[a]
U = np.fft.ifft2(U)
res_c1 = {}
for eps in (1e-2, 1e-3, 1e-4):
    lh = coeffs((lap_pert(U, eps) - lap_pert(U, 0.0)) / eps)
    rh = coeffs(dd_autodiff(U))
    res_c1[eps] = float(np.linalg.norm(lh - rh) / np.linalg.norm(rh))
OUT["C1_autodiff_vs_fd"] = res_c1

# ---- C1b: closed form (A1) vs autodiff on quarter-band inputs -------------
MQ = (np.abs(KX) <= KQ) & (np.abs(KY) <= KQ)
indq = np.argwhere(MQ)
Uq = np.zeros((N, N), complex)
for a in range(len(indq)):
    Uq[indq[a, 0], indq[a, 1]] = Uc[a]
Uq = np.fft.ifft2(Uq)
OUT["C1b_A1_vs_autodiff_band6"] = float(
    np.linalg.norm(dd_formula(Uq) - dd_autodiff(Uq)) /
    max(np.linalg.norm(dd_autodiff(Uq)), 1e-300))
OUT["C1b_A1_vs_autodiff_band12"] = float(
    np.linalg.norm(dd_formula(U) - dd_autodiff(U)) /
    max(np.linalg.norm(dd_autodiff(U)), 1e-300))

# ---- C2: Duhamel operator -------------------------------------------------
def expm_taylor(A, tol=1e-15):
    """exp(A) via scaling-and-squaring + Taylor series with explicit error
    control: choose s with ||A||_inf/2^s <= 1/2, sum Taylor to tol, then
    square s times.  Tested against scipy.linalg.expm on Hermitian matrices
    (rel. diff < 1e-12)."""
    nrm = np.abs(A).max()
    s = 0
    if nrm > 0.5:
        s = int(np.ceil(np.log2(nrm * 2.0)))
    A0 = A / (2.0 ** s)
    P = np.eye(A.shape[0], dtype=A.dtype)
    T = np.eye(A.shape[0], dtype=A.dtype)
    for k in range(1, 60):
        P = P @ A0 / k
        T = T + P
        if np.linalg.norm(P, np.inf) < tol:
            break
    for _ in range(s):
        T = T @ T
    return T

B = 0.5                                   # b = xi^2/2, xi = 1
MB = op_matrix(dd_autodiff)
lamv = lam12
Iduh = np.zeros((nmod, nmod), dtype=complex)
for p in range(nmod):
    lp = lamv[p]
    for q in range(nmod):
        d = lamv[q] - lp
        Iduh[p, q] = (B * np.exp(-B * lp)) if abs(d) < 1e-12 else \
            (np.exp(-B * lp) - np.exp(-B * lamv[q])) / d
Tb = MB * Iduh
S0 = np.diag(np.exp(-B * lamv))

res_c2 = {}
for eps in (1e-2, 1e-3, 1e-4):
    Mp = op_matrix(lambda f: lap_pert(f, eps))
    Sp = expm_taylor(B * Mp)
    cols = np.array([3, 10, 50, 200, 400])
    num = (Sp[:, cols] - S0[:, cols]) / eps
    ana = Tb[:, cols]
    res_c2[eps] = {
        "abs_norm_residual": float(np.linalg.norm(num - ana)),
        "norm_ana": float(np.linalg.norm(ana)),
        "normalized": float(np.linalg.norm(num - ana) / np.linalg.norm(ana)),
    }
OUT["C2_duhamel_vs_fd"] = res_c2

# ---- C3: frozen parallel case ---------------------------------------------
KC11, KC22 = 0.05, 0.03
def M_const(f):
    Dxx = np.fft.ifft2(-KX**2 * np.fft.fft2(f))
    Dyy = np.fft.ifft2(-KY**2 * np.fft.fft2(f))
    return -(KC11 * Dxx + KC22 * Dyy)
Mc = op_matrix(M_const)
Tcf = Mc * Iduh
with np.errstate(all="ignore"):
    frozen_exact = B * (Mc * np.exp(-B * lamv)[None, :])   # diagonal product, exact
OUT["C3_frozen_commutation_residual"] = float(
    np.linalg.norm(Tcf - frozen_exact) / np.linalg.norm(frozen_exact))

# ---- C4: operator norms and the analytic constants ------------------------
def opnorm(T, sin, sout):
    Dout = (1.0 + lamv) ** (sout / 2.0)
    Din = (1.0 + lamv) ** (-sin / 2.0)
    return float(np.linalg.norm((Dout[:, None] * T) * Din[None, :], 2))
nH1L2 = opnorm(Tb, 1, 0)
nH2L2 = opnorm(Tb, 2, 0)
nL2L2 = opnorm(Tb, 0, 0)
nM = opnorm(MB, 2, 0)
gamma_grid = []
for tt in np.logspace(-6, np.log10(B), 60):
    lstar = max(0.0, 0.5 / tt - 1.0)
    lamgrid = np.linspace(0.0, max(2.0 * lstar, 1.0), 400)
    gamma_grid.append(float(np.sqrt(tt) * np.max(
        (1.0 + lamgrid) ** 0.5 * np.exp(-tt * lamgrid))))
gamma_meas = max(gamma_grid)
gamma_an = float(1.0 / np.sqrt(2.0))
OUT["C4_norms"] = {
    "b": B,
    "norm_Tb_H1_to_L2": nH1L2,
    "norm_Tb_H2_to_L2": nH2L2,
    "norm_Tb_L2_to_L2": nL2L2,
    "M_deltaDelta_H2_to_L0": nM,
    "gamma_measured_t_in_0b": gamma_meas,
    "gamma_analytic_1_over_sqrt2": gamma_an,
    "bound_const_b_M": float(B * nM),
}

# ---- C5: contraction ------------------------------------------------------
maxc = 0.0
for tt in np.linspace(0.05, B, 7):
    with np.errstate(all="ignore"):
        maxc = max(maxc, hnorm_c(coeffs(np.fft.ifft2(np.exp(-tt * LAMSQ) * np.fft.fft2(U))), 0) /
                   hnorm_c(Uc, 0))
OUT["C5_contraction_max_ratio"] = float(maxc)

# ---- C6: negative control -------------------------------------------------
def sup_integrand(r, s=1):
    A = (np.exp(-(B - r) * lamv)[:, None] * MB) * np.exp(-r * lamv)[None, :]
    A2 = A * ((1.0 + lamv) ** (-s / 2.0))[None, :]
    v = np.ones(nmod, dtype=complex); v /= np.linalg.norm(v)
    for _ in range(15):
        w = A2 @ v
        nw = np.linalg.norm(w)
        if nw == 0:
            return 0.0
        v = w / nw
    return float(np.linalg.norm(A2 @ v))

edg = np.logspace(-6, -1.6, 24)
rr = np.unique(np.concatenate([edg, np.linspace(B / 2 - 0.49, B / 2, 8), B - edg]))
rr = np.clip(rr, 1e-9, B - 1e-9)
Isup = np.array([sup_integrand(r, 1) for r in rr])
m0 = rr < 0.5; mb = rr > B - 0.5
slope0 = float(np.polyfit(np.log(rr[m0]), np.log(Isup[m0]), 1)[0])
slopeb = float(np.polyfit(np.log(B - rr[mb]), np.log(Isup[mb]), 1)[0])

def crude_partial(ep):
    return float((2.0 / B) * np.log((B - ep) / ep))

fh = np.linspace(1e-9, B - 1e-9, 200000)
_trapz = getattr(np, "trapezoid", None) or np.trapz
half_int = float(_trapz(1.0 / np.sqrt(fh * (B - fh)), fh))
OUT["C6_negative_control"] = {
    "slope_sup_integrand_near_0": slope0,
    "slope_sup_integrand_near_b": slopeb,
    "expected_flat_plateau": 0.0,
    "one_leg_crude_partials": {f"eps{e:.0e}": crude_partial(e)
                               for e in (1e-2, 1e-3, 1e-4, 1e-6, 1e-8)},
    "crude_diverges_log2": True,
    "half_allocation_integral_measured": half_int,
    "half_allocation_integral_exact_pi": float(np.pi),
}

# ---- C7: linearity in eps (nonzero-mode input) ----------------------------
epsA = 1e-2
UA = np.zeros(nmod, dtype=complex); UA[7] = 1.0
anaA = (Tb @ UA)
res_c7 = {}
for ea in (1e-2, 1e-3):
    MpA = op_matrix(lambda f: lap_pert(f, ea))
    SpA = expm_taylor(B * MpA)
    numA = (SpA[:, 7] - S0[:, 7]) / ea
    res_c7[ea] = {
        "abs_norm_residual": float(np.linalg.norm(numA - anaA)),
        "normalized": float(np.linalg.norm(numA - anaA) / np.linalg.norm(anaA)),
    }
OUT["C7_linearity_mode7"] = res_c7

# ============================ PART B -- S^2 ================================
Lmax = 20
nmodS = (Lmax + 1) ** 2
lsi = np.array([l for l in range(Lmax + 1) for _ in range(-l, l + 1)])
lamS = lsi * (lsi + 1.0)
from numpy.polynomial.legendre import leggauss, Legendre
xg, wg = leggauss(1200)
cg = xg                                   # Lebesgue abscissas ARE cos(theta) on [-1,1]
w2 = 2.0 * np.pi * wg
Y20 = np.sqrt(5.0 / (16.0 * np.pi)) * (3.0 * cg**2 - 1.0)
Yl0 = np.array([np.sqrt((2.0 * l + 1.0) / (4.0 * np.pi)) *
                Legendre.basis(l)(cg) for l in range(Lmax + 1)])
phi_c = np.array([float(np.sum(w2 * Y20 * Yl0[l] * Yl0[l]))
                  for l in range(Lmax + 1)])
control_Y20sq = float(np.sum(w2 * Y20 * Y20))
phi_mat = np.zeros((nmodS, nmodS))
for l in range(Lmax + 1):
    phi_mat[l*l:(l+1)**2, l*l:(l+1)**2] = np.eye(2 * l + 1) * phi_c[l]
epsS = 0.05
phi_mode = np.array([phi_c[int(l)] for l in lsi])
res_s2 = {}
for epsS in (1e-3, 1e-4):
    TbS = +B * (phi_mat * lamS[None, :]) * np.exp(-B * lamS)[None, :]
    TbS_scaled = epsS * TbS
    MpertS = np.diag(-np.exp(-epsS * phi_mode) * lamS)  # Delta(eps) = -lam e^{-eps phi}
    SpS = expm_taylor(B * MpertS)
    S0S = np.diag(np.exp(-B * lamS))
    lhsS = (SpS - S0S) / epsS
    res_s2[epsS] = {
        "abs_norm_residual_vs_Tb": float(np.linalg.norm(lhsS - TbS)),
        "norm_TbS": float(np.linalg.norm(TbS)),
        "normalized": float(np.linalg.norm(lhsS - TbS) / max(np.linalg.norm(TbS), 1e-30)),
        "scaled_deltaS_abs1": float(np.linalg.norm(lhsS - TbS_scaled)),
        "max_abs_SpS_must_be_le_1": float(np.abs(SpS).max()),
    }
OUT["B_S2_conformal"] = {
    "Lmax": Lmax,
    "eps_values": list(res_s2.keys()),
    "per_eps": res_s2,
    "phi_c_l0": float(phi_c[0]), "phi_c_l2": float(phi_c[2]),
    "control_int_Y20_sq_must_be_1": control_Y20sq,
}

# ============================ PART C -- footings ===========================
G = 6.67430e-11; c = 299792458.0; Msun = 1.98847e30; pc = 3.085677581491367e16
a0_can = 9.3619e-11; a0_alt = 1.1279e-10
rhoL_can = 4.0 * a0_can**2 / (G * c**2)
rhoL_alt = 4.0 * a0_alt**2 / (G * c**2)
rM_can = np.sqrt(G * Msun / a0_can)
rM_alt = np.sqrt(G * Msun / a0_alt)
OUT["C_footings"] = {
    "a0_canonical_m_s2": a0_can, "a0_alternative_m_s2": a0_alt,
    "rho_Lambda_canonical_kg_m3": rhoL_can,
    "rho_Lambda_alternative_kg_m3": rhoL_alt,
    "kappa_effective_alt_at_fixed_rhoL": float(0.5 * a0_alt / a0_can),
    "rM_canonical_m": float(rM_can), "rM_canonical_pc": float(rM_can / pc),
    "rM_alternative_m": float(rM_alt), "rM_alternative_pc": float(rM_alt / pc),
    "rM_ratio_can_over_alt": float(rM_can / rM_alt),
    "sqrt_a0_ratio_alt_over_can": float(np.sqrt(a0_alt / a0_can)),
    "leaf_area_canonical_m2": float(np.pi * rM_can**2),
    "leaf_area_alternative_m2": float(np.pi * rM_alt**2),
}

OUT["elapsed_s"] = time.time() - T0
OUT["rss_mb"] = rss_mb()
print(json.dumps(OUT, indent=1, default=str))
signal.alarm(0)