#!/usr/bin/env python3
"""
AS043-audit: smoothing kernel statistical interpretation (dispatched seed content)
Run id: AS043-smk-r1-20260928T040643Z-dsv4f-hermes

Audits the claim: the heat filter S = exp[(xi^2/2) Delta] can be read statistically
as a Gaussian smoothing kernel of width xi in Euclidean measure.

Checks:
 C1 kernel form: S f == G_xi * f (FFT multiplier exp(-xi^2 k^2/2) vs direct Gaussian conv)
 C2 probability reading: G_xi >= 0, integral = 1 (1D and 3D normalization), var = xi^2
 C3 statistical expectation: (S f)(x) = E_Z[f(x + xi Z)], Monte Carlo vs FFT
 C4 L2 adjoint: <S u, v>_L2 == <u, S v>_L2 (self-adjoint in Euclidean measure)
 C5 GALACTIC measure adjoint (lapse-weighted proper volume dmu = N sqrt(h) d^3x):
    <v, S u>_N == <N^-1 S (N v), u>_N  (correct weighted adjoint)
    and negative control: <v, S u>_N == <v, S*_naive u>_N with S*_naive = S must FAIL
 C6 deep/Newtonian limits + boundary case: periodic vs free Gaussian (wrapped images)
 C7 both footings: dimensionless claim stated; r_M examples at both footings

Forces: numpy FFT on periodic 1D/3D grids; linear algebra only. Bounded: <=120 s.
"""
import json, time, numpy as np

t0 = time.time()
G = 6.67430e-11
c = 299792458.0
MSUN = 1.98847e30
A0_CAN = 9.3619e-11   # canonical footing
A0_ALT = 1.1279e-10   # alternative footing
results = {"checks": {}}

# ---------- C1: exact kernel form in Euclidean measure (periodic 1D) ----------
N = 512
L = 4.0
xi = 0.05
x = np.arange(N) * L / N
k = np.fft.fftfreq(N, d=L / N) * 2 * np.pi          # angular freq
# Gaussian kernel in real space (periodized)
def G1(xx, xi):
    return np.exp(-xx**2 / (2 * xi**2)) / (xi * np.sqrt(2 * np.pi))
S_fft = np.exp(-xi**2 * k**2 / 2)                    # symbol of S
rng = np.random.default_rng(7)
f = np.exp(-((x - 1.3) ** 2) / (2 * 0.4**2)) + 0.3 * np.cos(7 * x) + 0.1 * x
Sf_fft = np.fft.ifft(S_fft * np.fft.fft(f)).real
# direct convolution with periodized Gaussian (sum over images, ~6 sigmas)
dx = L / N
Sf_conv = np.zeros_like(f)
for i in range(N):
    d = np.minimum(np.abs(x - x[i]), L - np.abs(x - x[i]))
    Sf_conv[i] = np.sum(G1(d, xi) * f) * dx
res1 = np.max(np.abs(Sf_fft - Sf_conv))
results["checks"]["C1_kernel_form_periodic1D"] = {
    "residual_max": float(res1),
    "method": "FFT symbol exp(-xi^2 k^2/2) vs direct periodized Gaussian convolution",
    "threshold": 1e-8, "pass": bool(res1 < 1e-8),
    "kernel": "G_xi(r) = (2 pi xi^2)^(-3/2) exp(-|r|^2/(2 xi^2)) in 3D; (2 pi xi^2)^(-1/2) exp(-r^2/(2 xi^2)) in 1D"
}

# ---------- C2: probability reading ----------
# 1D normalization on the same grid
norm1 = np.sum(G1(np.minimum(np.abs(x - x[0]), L - np.abs(x - x[0])), xi)) * dx
# exact 1D integral = 1; grid quadrature approx
results["checks"]["C2_1D_norm"] = {"integral": float(norm1), "expected": 1.0,
                                   "thresh": 1e-6, "pass": bool(abs(norm1 - 1) < 1e-6)}
# 3D normalization exact = product of three 1D = 1 (analytic); verify 1D variance xi^2 analytically via
# int x^2 G = xi^2: closed form
results["checks"]["C2_variance"] = {"variance_formula": "int x^2 G_xi dx = xi^2",
                                    "value_xi": xi, "expected_xi2": xi**2,
                                    "analytic": True,
                                    "note": "var of N(0, xi^2 I_3) is xi^2 per axis; width = xi std"}

# ---------- C3: statistical expectation ----------
def Sf(xi, f, k):  # f defined on periodic grid, symbol S_fft
    return np.fft.ifft(np.exp(-xi**2 * k**2 / 2) * np.fft.fft(f)).real
sf = Sf(xi, f, k)
M = 400_000
Z = rng.standard_normal(M)
x0 = 1.7
# proper: evaluate f at wrapped points via nearest-grid lookup
idx = ((x0 + xi * Z) % L / dx).astype(int) % N
f_eval = f[idx]
mc = np.mean(f_eval)
fft_at_x0 = np.interp(x0, x, sf)
results["checks"]["C3_statistical_expectation"] = {
    "E[f(x0+xi Z)]_MC": float(mc),
    "(S f)(x0)_FFT": float(fft_at_x0),
    "delta": float(abs(mc - fft_at_x0)),
    "threshold": 3e-3, "pass": bool(abs(mc - fft_at_x0) < 3e-3),
    "note": "statistical reading S f(x) = E[f(x+xi Z)], Z~N(0,I); MC error ~1/sqrt(M)"
}

# ---------- C4: L2 adjoint (Euclidean measure) ----------
u = rng.standard_normal(N)
v = rng.standard_normal(N)
dot = lambda a, b: np.sum(a * b) * dx
LHS4 = dot(Sf(xi, u, k), v)
RHS4 = dot(u, Sf(xi, v, k))
results["checks"]["C4_L2_selfadjoint"] = {
    "<Su,v>": float(LHS4), "<u,Sv>": float(RHS4),
    "abs_diff": float(abs(LHS4 - RHS4)),
    "threshold": 1e-8, "pass": bool(abs(LHS4 - RHS4) < 1e-8),
    "note": "S* = S in L2(dx): heat semigroup of self-adjoint Laplacian; Gaussian kernel symmetric"
}

# ---------- C5: GALACTIC measure adjoint ----------
# Galactic measure: dmu = N(x) dx with nonconstant lapse N (1D slice of leaf measure N sqrt(h) d^3x)
Nl = 1.0 + 0.3 * np.cos(3 * x) + 0.1 * np.sin(5 * x)   # positive lapse
mu_dot = lambda a, b: np.sum(a * b * Nl) * dx
# correct galactic adjoint: S*_mu = N^-1 S N
Su = Sf(xi, u, k)
Sv = Sf(xi, v, k)
SNv = Sf(xi, Nl * v, k)
LHS5 = mu_dot(Su, v)                     # <S u, v>_N
RHS5 = mu_dot(u, Nl**-1 * SNv)           # <u, N^-1 S (N v)>_N
# negative control: naive "S* = S in galactic measure"
NAIVE5 = mu_dot(u, Sv)                   # <u, S v>_N  (would equal <Su,v>_N only if self-adjoint in mu)
results["checks"]["C5_galactic_adjoint_correct"] = {
    "<Su,v>_N": float(LHS5), "<u,N^-1 S N v>_N": float(RHS5),
    "abs_diff": float(abs(LHS5 - RHS5)),
    "threshold": 1e-8, "pass": bool(abs(LHS5 - RHS5) < 1e-8),
    "note": "S*_mu = N^-1 S N in dmu = N dx (lapse-weighted proper volume); matches AS205 identity"
}
results["checks"]["C5_negative_control_naive_selfadjoint_must_FAIL"] = {
    "<Su,v>_N": float(LHS5), "<u,Sv>_N": float(NAIVE5),
    "abs_diff": float(abs(LHS5 - NAIVE5)),
    "threshold_fail_if_below": 1e-3,
    "control_triggered": bool(abs(LHS5 - NAIVE5) > 1e-3),
    "note": "S* = S in galactic measure is FALSE for nonconstant lapse; control must detect nonzero gap"
}

# ---------- C6: boundary case: periodic wrapped kernel vs free Gaussian ----------
# On the periodic cell the exact kernel is the wrapped Gaussian (sum over images).
# Free Gaussian truncated at 4 sigma misses image mass => residual must be nonzero.
# C6 metric: L1 distance (max-abs is weak for smooth kernels); xi_b comparable to L so images matter.
xi_b = 1.1
d = np.minimum(np.abs(x - x[0]), L - np.abs(x - x[0]))
freeK = G1(d, xi_b) * dx
wrappedK = np.sum([np.exp(-((x - x[0] + m * L) ** 2) / (2 * xi_b**2)) / (xi_b * np.sqrt(2 * np.pi)) * dx
                   for m in (-2, -1, 0, 1, 2)], axis=0)
res6_max = float(np.max(np.abs(freeK - wrappedK)))
res6_l1 = float(np.sum(np.abs(freeK - wrappedK)))
results["checks"]["C6_boundary_wrapped_vs_free"] = {
    "max_abs_diff": res6_max, "l1_diff": res6_l1,
    "threshold_detect_l1": 1e-3,
    "control_triggered": bool(res6_l1 > 1e-3),
    "note": "exact kernel on periodic domain is wrapped Gaussian sum of images; free Euclidean Gaussian differs at O(exp(-L^2/8 xi^2)) — boundary/domain enters the kernel, statistical reading must state domain"
}

# ---------- C1b: exact 3D kernel form via separability ----------
N3 = 64
L3 = 2.0
xi3 = 0.1
xs = np.arange(N3) * L3 / N3
k3 = np.fft.fftfreq(N3, d=L3 / N3) * 2 * np.pi
u3 = rng.standard_normal((N3, N3, N3))
S_3d_fft = np.exp(-xi3**2 * (k3[:, None, None]**2 + k3[None, :, None]**2 + k3[None, None, :]**2) / 2)
via_symbol = np.fft.ifftn(S_3d_fft * np.fft.fftn(u3)).real
# separable application: three sequential 1D filters with 1D Gaussian symbol
def apply1d(a, axis):
    shape = [1, 1, 1]
    shape[axis] = N3
    mul = np.exp(-xi3**2 * k3**2 / 2).reshape(shape)
    return np.fft.ifft(mul * np.fft.fft(a, axis=axis), axis=axis).real
via_sep = apply1d(apply1d(apply1d(u3, 0), 1), 2)
res1b = float(np.max(np.abs(via_symbol - via_sep)))
results["checks"]["C1b_3D_kernel_separable"] = {
    "residual_max": res1b, "threshold": 1e-8, "pass": bool(res1b < 1e-8),
    "method": "3D FFT symbol exp(-xi^2 |k|^2/2) vs three sequential 1D Gaussian filters",
    "note": "3D Gaussian kernel factorizes G_xi(r)=prod_i G_xi(r_i); exact kernel form (2 pi xi^2)^(-3/2) exp(-|r|^2/(2 xi^2))"
}
# 3D normalization: by separability (verified C1b at 5e-17), int_{R^3} G_xi = (int_R G_xi)^3 = 1
norm3 = float(norm1**3)   # norm1 from C2_1D_norm = 1.0000000000000002
results["checks"]["C2b_3D_norm"] = {"integral": norm3, "expected": 1.0,
                                    "thresh": 1e-3, "pass": bool(abs(norm3 - 1) < 1e-3),
                                    "note": "int_{R^3} G_xi = (int_R G_xi)^3 = 1 via product separability (C1b); probability kernel"}
# C2c: second moment (width claim): int x^2 G_xi dx = xi^2, numeric quadrature
xs2 = np.linspace(-6 * xi, 6 * xi, 200001)
sec_mom = float(np.sum(xs2**2 * G1(xs2, xi)) * (12 * xi / 200000))
results["checks"]["C2c_second_moment"] = {"int_x2_G": sec_mom, "expected_xi2": float(xi**2),
                                          "thresh": 1e-6, "pass": bool(abs(sec_mom - xi**2) < 1e-6),
                                          "note": "variance of K_xi is xi^2 per axis => std width = xi (the 'width xi' reading)"}

# ---------- C7: both footings ----------
rhoL_can = 4 * A0_CAN**2 / (G * c**2)
rhoL_alt = 4 * A0_ALT**2 / (G * c**2)
Mb = 1e10 * MSUN
rM_can = (G * Mb / A0_CAN) ** 0.5
rM_alt = (G * Mb / A0_ALT) ** 0.5
results["checks"]["C7_footings"] = {
    "a0_canonical": A0_CAN, "a0_alternative": A0_ALT,
    "rho_Lambda_canonical_from_4a0^2/Gc^2": float(rhoL_can),
    "rho_Lambda_alternative_from_4a0^2/Gc^2": float(rhoL_alt),
    "r_M(1e10 Msun)_canonical_m": float(rM_can), "r_M(1e10 Msun)_alternative_m": float(rM_alt),
    "note": "Audit itself is dimensionless in xi/(L domain); both footings fix a0 only; xi is an independent length. If xi were tied to r_M, footing changes xi by sqrt(1.1279e-10/9.3619e-11)=1.0978."
}
results["elapsed_s"] = time.time() - t0
results["bounds"] = {"wall_s": round(time.time() - t0, 2), "threads": 1,
                     "mem_est_MB": "~20 (N=512 grids, 400k MC)", "grid": "512 1D periodic cells"}

print(json.dumps(results, indent=1))
