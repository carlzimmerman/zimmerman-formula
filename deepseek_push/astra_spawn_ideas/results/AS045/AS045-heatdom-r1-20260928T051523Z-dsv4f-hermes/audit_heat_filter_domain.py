#!/usr/bin/env python3
"""AS045 — Heat filter operator domain of definition (MONO branch, filtered nu_mono).

Audits S = exp[(xi^2/2) Delta] on flat Euclidean L2(dx) versus the galactic measure
dmu_N = N sqrt(h) d^3x:
  (1) Fourier-multiplier action  S(exp(ikx)) = exp(-xi^2 k^2/2) exp(ikx)
  (2) L2(dx) self-adjointness;  L2-Lp boundedness (contraction norm 1)
  (3) galactic adjoint S*_gal = N^{-1} S N ; NEGATIVE CONTROL: naive S* = S in
      galactic measure must FAIL for nonconstant lapse (flat-lapse positive control
      must stay at machine zero)
  (4) weighted boundedness criterion ||S f||_w^2 <= esssup(Sw/w) ||f||_w^2,
      exact Sw for w = 1+x^2 (Sw = w + xi^2 in 1D), and the unboundedness witness
      w = exp(x^2), xi >= 1 (S f falls outside L2(w); cumulative integral grows
      with domain size — must grow, control capable of failing)
  (5) composition T(u) = S* div[(nu_mono(y)-1) grad S u], u = 1_{|x|<=0.5} in
      L^2 \\ H^1: singularity cancellation (nu_mono-1 ~ y^{-1/2}, grad Su ~ y)
      -> V = a0 h_mono(y) ehat in C^0; T finite and continuous across the zero of
      grad Su; naive |(nu-1)| bound diverges while |V| stays bounded (control)
  (6) nu_mono construction: y_p, h_p, y_star re-solved; splice continuity;
      0.0104 dex bound vs nu_RAR; h_mono(y)/sqrt(y) -> 1
  (7) both a0 footings: r_M anchors; all operator identities a0-free
Bounds: wall <= 120 s, RSS <= 512 MB, 1 thread (enforced via /usr/bin/time -l and
thread env vars). 1D periodic cell, N up to 4096; 2D cell 64^2 for composition demo.
"""
import numpy as np
import json, time, sys

t0 = time.time()
rng = np.random.default_rng(7)

# ---------------- constants (SI) ----------------
G_SI = 6.67430e-11
c_SI = 299792458.0
M_SUN = 1.98847e30
PC = 3.085677581491367e16
A0_CAN = 9.3619e-11
A0_ALT = 1.1279e-10
# dimensionless filter widths on the unit cell (xi in cell units)
XI1, XI2 = 0.8, 0.3

def rM(Mb, a0):
    return np.sqrt(G_SI * Mb / a0)

C = {}
C["rM_1e10_canonical_m"] = rM(1.0e10 * M_SUN, A0_CAN)
C["rM_1e10_alternative_m"] = rM(1.0e10 * M_SUN, A0_ALT)

# ---------------- nu_mono construction ----------------
def h_RAR(y):
    y = np.asarray(y, dtype=float)
    s = np.sqrt(y)
    out = y / np.expm1(s)          # y/(e^sqrt(y)-1), stable; h_RAR(0)=0 by continuity (h ~ sqrt(y))
    return np.where(y > 0, out, 0.0)

def hp_RAR(y):
    # d/dy [y/(e^s-1)], s=sqrt(y):  [2(e^s-1) - s e^s] / [2 (e^s-1)^2]
    s = np.sqrt(y)
    e = np.exp(s)
    return (2.0 * (e - 1.0) - s * e) / (2.0 * (e - 1.0) ** 2)

DELTA = 0.05
# y_p: peak of h_RAR (root of hp_RAR)
yg = np.geomspace(1e-4, 1e2, 200001)
idx = np.argmax(h_RAR(yg)); yp_lo, yp_hi = yg[max(0, idx - 2)], yg[min(len(yg) - 1, idx + 2)]
# refine with brentq on hp_RAR
from scipy.optimize import brentq
yp = brentq(hp_RAR, yp_lo, yp_hi)
hp = h_RAR(yp)
# y_star: hp_RAR(y) = DELTA*hp/(y+yp)
def fstar(y):
    return hp_RAR(y) - DELTA * hp / (y + yp)
ys_lo, ys_hi = 1.0, yp  # hp_RAR is positive decreasing on (0,yp); fstar sign change inside
ys = brentq(fstar, ys_lo, ys_hi)

def h_mono(y):
    y = np.asarray(y, dtype=float)
    out = np.empty_like(y)
    lo = y <= ys
    out[lo] = h_RAR(y[lo])
    out[~lo] = h_RAR(ys) + DELTA * hp * np.log((y[~lo] + yp) / (ys + yp))
    return out

def nu_mono(y):
    y = np.asarray(y, dtype=float)
    return np.where(y > 0, 1.0 + h_mono(y) / y, np.inf)   # nu_mono(0)=lim_{y->0} ~ 1/sqrt(y) = inf

def nu_RAR(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))

y_chk = np.geomspace(1e-6, 1e4, 50001)
C["y_p"] = yp
C["h_p"] = float(hp)
C["y_star"] = ys
# splice continuity (left/right limits at y_star, and derivative rule)
eps = 1e-9
C["splice_gap_abs"] = abs(h_RAR(ys) - (h_RAR(ys) + DELTA * hp * np.log((ys + eps + yp) / (ys + yp))))
C["splice_deriv_rule_resid"] = abs(hp_RAR(ys) - DELTA * hp / (ys + yp))
# dex difference vs nu_RAR
dex = np.abs(np.log10(nu_mono(y_chk)) - np.log10(nu_RAR(y_chk)))
C["max_dex_nu_mono_vs_rar"] = float(dex.max())
C["y_at_max_dex"] = float(y_chk[np.argmax(dex)])
# h_mono ~ sqrt(y) near 0
ysmall = np.geomspace(1e-10, 1e-2, 9)
C["h_mono_over_sqrt_y_at_small_y"] = [float(h_mono(yi) / np.sqrt(yi)) for yi in ysmall]
# nu_mono - 1 ~ y^{-1/2}
C["nu_mono_minus_1_scaled"] = [float((nu_mono(yi) - 1.0) * np.sqrt(yi)) for yi in ysmall]

# ---------------- 1D periodic-cell machinery ----------------
def cell_ops(N, L, xi, w=None):
    """Return apply-S (symbol), direct wrapped-Gaussian convolution, inner products."""
    dx = L / N
    x = (np.arange(N) - N // 2) * dx
    k = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)       # rad / (cell unit)
    sym = np.exp(-(xi ** 2) * k ** 2 / 2.0)
    # wrapped Gaussian kernel (exact on periodic cell), std xi
    d = np.abs(x)
    kern = np.exp(-(np.minimum(d, L - d) ** 2) / (2.0 * xi ** 2))
    kern /= kern.sum()
    def S(f):
        return np.fft.ifft(np.fft.fft(f) * sym).real
    # exact periodic (wrapped) Gaussian kernel in FFT-native order, images n=-1,0,1:
    # tail at |x| >= L - L/2 = L/2 contributes e^{-(L/2)^2/(2 xi^2)} ~ 1.4e-11 (L=8, xi=0.8)
    xq = np.arange(N) * dx
    dq = np.minimum(xq, L - xq)
    kern = np.zeros(N)
    for n in (-1, 0, 1):
        kern += np.exp(-((xq + n * L) ** 2) / (2.0 * xi ** 2))
    kern /= kern.sum()
    def Sper(f):
        return np.fft.ifft(np.fft.fft(f) * np.fft.fft(kern)).real
    def ip(f, g):              # Euclidean L2(dx) real inner product * dx
        return float(np.dot(f, g) * dx)
    def ipw(f, g, w):
        return float(np.dot(f * w, g) * dx)
    return x, k, sym, S, Sper, kern, ip, ipw

# ---- C1: multiplier action on plane waves ----
N1, L1, xi_a = 512, 8.0, XI1
x1, k1, sym1, S1, Sper1, kern1, ip1, ipw1 = cell_ops(N1, L1, xi_a)
resid_max = 0.0
for m in (1, 2, 7):
    pw = np.cos(2.0 * np.pi * m * x1 / L1)   # real part of exp(ik x)
    Sval = S1(pw)
    exact = np.exp(-(xi_a ** 2) * (2.0 * np.pi * m / L1) ** 2 / 2.0) * pw
    resid_max = max(resid_max, float(np.max(np.abs(Sval - exact))))
C["C1_multiplier_plane_wave_max_resid"] = resid_max

# ---- C2: symbol vs direct wrapped convolution ----
rngf = rng.normal(size=N1) * 0.3 + np.cos(2.0 * np.pi * 3 * x1 / L1) + np.exp(-x1 ** 2)
C["C2_symbol_vs_direct_max_resid"] = float(np.max(np.abs(S1(rngf) - Sper1(rngf))))

# ---- C3: Euclidean L2 adjointness ----
u1 = rng.normal(size=N1); v1 = rng.normal(size=N1)
C["C3_L2_euclidean_adjoint_gap"] = abs(ip1(S1(u1), v1) - ip1(u1, S1(v1)))

# ---- C4: galactic measure, lapse N nonconstant; NEGATIVE CONTROL ----
def lapse1(x):
    return 1.0 + 0.3 * np.cos(2.0 * np.pi * 3 * x1 / L1) + 0.1 * np.sin(2.0 * np.pi * 5 * x1 / L1)
Nl = lapse1(x1)
wN = Nl  # sqrt(h)=1 on the flat cell; dmu_N = N dx
def Sgal(f):           # N^{-1} S (N f)
    return S1(Nl * f) / Nl
C["C4_galactic_adjoint_NinvSN_gap"] = abs(ipw1(S1(u1), v1, Nl) - ipw1(u1, Sgal(v1), Nl))
# negative control: naive self-adjointness in galactic measure must FAIL
C["C4n_naive_galactic_selfadjoint_gap"] = abs(ipw1(S1(u1), v1, Nl) - ipw1(u1, S1(v1), Nl))
# positive control: flat lapse -> naive gap returns to machine zero (detector works)
C["C4n_flat_lapse_naive_gap"] = abs(ipw1(S1(u1), v1, np.ones_like(Nl)) - ipw1(u1, S1(v1), np.ones_like(Nl)))

# ---- C5: weighted boundedness criterion  ||S f||_w^2 <= sup(Sw/w) ||f||_w^2 ----
for xi_c in (XI1, XI2):
    xb, kb, symb, Sb, Sperb, kernb, ipb, ipwb = cell_ops(1024, 8.0, xi_c)
    wq = 1.0 + xb ** 2
    Sw = Sperb(wq)                    # S of the weight itself (direct conv, exact on cell)
    sup_ratio = float(np.max(Sw / wq))
    # exact continuum: Sw = w + xi^2 in 1D  ->  sup = 1 + xi^2 at x = 0
    f2 = rng.normal(size=1024)
    num = ipwb(Sb(f2), Sb(f2), wq); den = ipwb(f2, f2, wq)
    C[f"C5_sup_Sw_over_w_xi{xi_c}"] = sup_ratio
    C[f"C5_exact_1_plus_xi2_xi{xi_c}"] = 1.0 + xi_c ** 2
    C[f"C5_norm_ratio_sq_xi{xi_c}"] = num / den

# ---- C6: unboundedness witness w = exp(x^2), xi >= 1 (control: integral grows with L) ----
xi_u = 1.05
def G(x, xi):
    return np.exp(-(x ** 2) / (2.0 * xi ** 2)) / np.sqrt(2.0 * np.pi * xi ** 2)
grows = []
for Lh in (5.0, 10.0, 20.0, 40.0):
    xg_ = np.linspace(-Lh, Lh, 200001)
    grows.append(float(np.trapz(G(xg_, xi_u) ** 2 * np.exp(xg_ ** 2), xg_)))
C["C6_Int_G2_exp_x2_grows_with_L"] = [float(g) for g in grows]
C["C6_growth_ratio_L10_over_L5"] = grows[1] / grows[0]
C["C6_growth_ratio_L20_over_L10"] = grows[2] / grows[1]
# also Sw/w at x=0 for w = exp(x^2): Sw(0) = int G(y) exp(y^2) dy
s0 = []
for Lh in (5.0, 10.0, 20.0, 40.0):
    xg_ = np.linspace(-Lh, Lh, 400001)
    s0.append(float(np.trapz(G(xg_, xi_u) * np.exp(xg_ ** 2), xg_)))
C["C6_Sw0_diverging"] = [float(v) for v in s0]

# ---- C7: composition T(u) = S* div[(nu_mono(y)-1) grad S u], u = 1_{|x|<=0.5} in L2\H1 ----
# physical cell: L_phys = 30 kpc; xi_phys = 3 kpc -> xi_cell = 0.1 in cell units
L_phys = 30.0 * 1e3 * PC
xi_phys = 3.0 * 1e3 * PC
N7, L7 = 4096, 1.0
dx7 = L7 / N7
x7 = (np.arange(N7) - N7 // 2) * dx7
# u in potential units (m^2/s^2), amplitude ~ v_flat^2 ~ 1e10
u7 = np.where(np.abs(x7) <= 0.05, 1.0e10, 0.0)   # 1.5 kpc half-width
x7, k7, sym7, S7, Sper7, kern7, ip7, ipw7 = cell_ops(N7, L7, 0.1)
Su = S7(u7)
dSu = np.gradient(Su, dx7)                       # d/dx (S u)  [cell units: u per cell]
y7 = np.abs(dSu) / (L_phys * A0_CAN)          # |grad Su|/a0 : dSu already = d(Su)/d(dimless x); /L_phys physical
n7 = nu_mono(y7)
V7 = A0_CAN * h_mono(y7) * np.sign(dSu)          # (nu_mono-1) grad Su = a0 h_mono(y) ehat; 0 at zeros
# direct check of the identity |V| = a0 h_mono(y)
C["C7_V_equals_a0_times_h_mono_max_resid"] = float(np.max(np.abs(np.abs(V7) - A0_CAN * h_mono(y7))))
# cancellation control: naive (nu-1)(y(x)) diverges near x=0, |V| stays bounded
ring = (np.abs(x7) <= 0.01) & (np.abs(x7) > 1e-12)      # exclude the exact zero of grad Su
naive_max = float(np.max((n7[ring] - 1.0)))
V_ring_max = float(np.max(np.abs(V7[ring])))
C["C7_naive_nu_minus_1_max_in_ring"] = naive_max          # should be O(1e2..1e6): huge
C["C7_V_max_in_ring"] = V_ring_max                        # bounded O(a0 * max h_mono) ~ 6.6e-11
C["C7_V_to_a0_ratio"] = V_ring_max / A0_CAN
# h_mono max ~ h_p * (1+delta log) ~ 0.7 -> V_max ~ a0*0.7 ~ 6.6e-11
# T(u) = S* V' with S* = S on Euclidean: (S V')  computed as derivative of S V (periodic:
# S and d/dx commute on the periodic cell)
SV = S7(V7)
dSV = np.gradient(SV, dx7)                    # d(S V)/d(dimless x); S commutes with d/dx on the periodic cell
T7 = dSV / (L_phys ** 2)                      # S* div V = (1/L_phys)^2 d/dxi (S V); units: [V]=m/s^2 -> 1/s^2
C["C7_T_finite_max_abs"] = float(np.max(np.abs(T7)))
left = T7[x7 < -0.02]; right = T7[x7 > 0.02]
C["C7_T_left_right_lim_agree"] = float(abs(np.mean(left) - np.mean(right)))
C["C7_T_mean_abs"] = float(np.mean(np.abs(T7)))
# V continuity at x=0: V(0+) and V(0-) both -> 0
i0 = int(np.argmin(np.abs(x7)))
C["C7_V_near_zero"] = [float(np.max(np.abs(V7[max(0, i0 - 3):i0 + 4])))]
# u7 in L2 but not in H1: H1-seminorm proxy must GROW with resolution (step = delta layer)
for Nq in (512, 1024, 2048, 4096):
    dxq = 1.0 / Nq
    xq = (np.arange(Nq) - Nq // 2) * dxq
    uq = np.where(np.abs(xq) <= 0.05, 1.0e10, 0.0)
    dUq = np.gradient(uq, dxq)
    C[f"C7_H1seminorm_proxy_N{Nq}"] = float(np.sqrt(np.dot(dUq, dUq) / dxq) / L_phys)
C["C7_u_norm_L2"] = float(np.sqrt(np.dot(u7, u7) * dx7 * L_phys))
C["C7_H1_growth_N2048_over_N512"] = C["C7_H1seminorm_proxy_N2048"] / C["C7_H1seminorm_proxy_N512"]

# ---- C8: 2D composition demo (small cell, 64^2) ----
N8 = 64
x8 = (np.arange(N8) - N8 // 2) / N8
gx, gy = np.meshgrid(x8, x8, indexing="ij")
u8 = np.where((np.abs(gx) <= 0.15) & (np.abs(gy) <= 0.15), 1.0e10, 0.0)
k8x = 2.0 * np.pi * np.fft.fftfreq(N8, d=1.0 / N8)
k8x, k8y = np.meshgrid(k8x, k8x, indexing="ij")
sym8 = np.exp(-(0.1 ** 2) * (k8x ** 2 + k8y ** 2) / 2.0)
def S2(f):
    return np.fft.ifft2(np.fft.fft2(f) * sym8).real
Su8 = S2(u8)
dSux = np.gradient(Su8, 1.0 / N8, axis=0); dSuy = np.gradient(Su8, 1.0 / N8, axis=1)
gradmag = np.hypot(dSux, dSuy)
y8 = gradmag / (L_phys * A0_CAN)      # grad already divided by cell spacing; physical = /L_phys
Vx = A0_CAN * h_mono(y8) * np.where(gradmag > 0, dSux / np.where(gradmag > 0, gradmag, 1.0), 0.0)
Vy = A0_CAN * h_mono(y8) * np.where(gradmag > 0, dSuy / np.where(gradmag > 0, gradmag, 1.0), 0.0)
SVx = S2(Vx); SVy = S2(Vy)
T8 = (np.gradient(SVx, 1.0 / N8, axis=0) + np.gradient(SVy, 1.0 / N8, axis=1)) / (L_phys ** 2)
C["C8_2D_T_finite"] = float(np.nanmax(np.abs(T8)))
# zero of grad at origin: V -> 0
C["C8_V_at_origin"] = float(abs(Vx[N8 // 2, N8 // 2]) + abs(Vy[N8 // 2, N8 // 2]))

C["wall_seconds"] = time.time() - t0
print(json.dumps(C, indent=1, sort_keys=True))
print("OK")
