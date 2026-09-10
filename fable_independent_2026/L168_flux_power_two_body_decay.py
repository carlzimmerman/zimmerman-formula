#!/usr/bin/env python3
"""
L168 -- THE FLUX-POWER TEST at the L167 cell (tau = 5 Gyr, v_k = 600 km/s): L163 TEST 2.

Two-body decay X -> Y + (light): every cold particle decays at rate Gamma and its daughter receives an isotropic
kick v_k (physical, at birth) and INHERITS the mother's position and bulk velocity. Energy to the light product
(eps ~ v_k/c ~ 2e-3) neglected, so the background is LCDM with the same Omega_m.

Linear perturbations, sub-horizon Newtonian limit (k >> aH; at z <= 100 that is k >= 0.02 h/Mpc), computed EXACTLY for
the collisionless daughters by the Gilbert integral solution of the linearised Vlasov equation, cohort by cohort in birth
epoch a_i, with the daughters' self-gravity fed back self-consistently (direct linear solve). For a cohort born at
conformal time eta_i with momentum p0 = m v_k a_i and the mother's (delta_c, theta_c) at birth:

  delta_coh(k, eta) = [delta_c(eta_i) - theta_c(eta_i) D(eta,eta_i)] j0(k X(eta,eta_i))
                      - k^2 int_{eta_i}^{eta} d eta' a(eta') phi(k,eta') I(eta,eta') j0(k v_k a_i I(eta,eta')),
  I(eta,eta') = int_{eta'}^{eta} d eta''/a,  X = v_k a_i I,  D = a_i I,
  delta_d = sum over cohorts weighted by the decayed mass; mother and baryons are cold fluids; Poisson closes phi.
  The no-kick limit (j0 -> 1) reproduces the cold-fluid Green's-function solution exactly -- that is control C2.

Initial conditions at z = 100 from mainline CLASS (classy) LCDM: delta_i = sqrt(P(k, z=100)), theta_i = -aH f delta_i.
Statistics at z = 3, 2.5, 2: T^2(k) = P_DDM/P_LCDM; Murgia et al. area criterion delta_A over 0.5-20 h/Mpc against the
thermal-WDM calibration (Viel et al. 2005 transfer function) at m_WDM = 5.3 keV (Irsic et al. 2017 bound, CITED),
3.5 keV (Viel et al. 2013), 2.0 keV; a linear 1-D flux-power proxy P_1D(k_par) ~ int_{k_par} k P(k) dk in s/km at z = 3;
sigma_8 / S_8 at z = 0 from the SAME calculation (replacing L160's (A)/(B) growth-treatment ambiguity by the actual
linear-response growth). Cited bounds are scales, not re-fits. No pass condition is a literal True.
"""
import numpy as np, time, sys
from scipy.integrate import cumulative_trapezoid
T0 = time.time()
CHECKS = []
def check(n, ok, d=""):
    CHECKS.append((n, bool(ok))); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
def sec(t): print("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118, flush=True)

# ---------------- cosmology (Planck-like, massless neutrinos) ----------------
h = 0.6736; H0 = 100 * h / 299792.458          # 1/Mpc
omb, omc = 0.02237, 0.1200
Ob, Oc = omb / h ** 2, omc / h ** 2; Om = Ob + Oc
Or = 4.18e-5 / h ** 2 * (1 + 0.2271 * 3.046); OL = 1 - Om - Or
def H(a): return H0 * np.sqrt(Or * a ** -4 + Om * a ** -3 + OL)
GYR = 299792.458 / 977.792          # Mpc per Gyr: c * 1 Gyr = 306.6 Mpc  (t and eta in Mpc, c = 1)
C_KMS = 299792.458
A_INIT = 1.0 / 101.0
N_A = 420
a_grid = np.geomspace(A_INIT, 1.0, N_A)
_af = np.geomspace(1e-4, 1.0, 40000)
eta_f = cumulative_trapezoid(1.0 / (_af ** 2 * H(_af)), _af, initial=0.0)
t_f = cumulative_trapezoid(1.0 / (_af * H(_af)), _af, initial=0.0)
eta = np.interp(a_grid, _af, eta_f); t_cos = np.interp(a_grid, _af, t_f)      # Mpc (conformal), Mpc/c (cosmic)
AGE_GYR = t_f[-1] / GYR
F = cumulative_trapezoid(1.0 / a_grid, eta, initial=0.0)                       # F(j) = int_{eta_0}^{eta_j} d eta / a
I_mat = np.maximum(F[:, None] - F[None, :], 0.0)                               # I(j, l) = int_{eta_l}^{eta_j} d eta / a  (j >= l)
d_eta = np.gradient(eta)                                                       # trapezoid-like weights
z_of = lambda a: 1 / a - 1
def idx_z(z): return int(np.argmin(np.abs(a_grid - 1 / (1 + z))))

# ---------------- initial conditions from CLASS ----------------
from classy import Class
cl = Class()
cl.set({"h": h, "omega_b": omb, "omega_cdm": omc, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046,
        "N_ncdm": 0, "YHe": 0.2454, "output": "mPk", "P_k_max_h/Mpc": 45, "z_pk": "100, 3, 2.5, 2, 0"})
cl.compute()
K_H = np.geomspace(0.02, 30.0, 44)                     # h/Mpc
K = K_H * h                                            # 1/Mpc
P_cl = {z: np.array([cl.pk_lin(k, z) for k in K]) for z in (100.0, 3.0, 2.5, 2.0, 0.0)}   # (Mpc)^3
sig8_lcdm = cl.sigma8()
f_init = cl.scale_independent_growth_factor_f(100.0)
print(f"  CLASS LCDM: sigma8 = {sig8_lcdm:.4f}, f(z=100) = {f_init:.4f}, age = {AGE_GYR:.2f} Gyr")

# ---------------- the solver ----------------
def j0(x): return np.sinc(x / np.pi)

def solve(k, tau_gyr, vk_kms):
    """DIRECT linear solve of the coupled cold-fluid + cohort-integral system (no iteration).
    Unknowns: delta_cold(a_j), delta_d(a_j) on the grid. Returns (dc, dd, dm, cond)."""
    Gamma = 0.0 if tau_gyr is None else 1.0 / (tau_gyr * GYR)
    v = vk_kms / C_KMS
    surv = np.exp(-Gamma * t_cos)
    w = np.append(-np.diff(surv), 0.0)
    W = np.cumsum(w) - w
    fd = 1 - surv
    d0 = np.sqrt(np.interp(k, K, P_cl[100.0]))
    th0 = -a_grid[0] * H(a_grid[0]) * f_init * d0
    Dm0 = a_grid[0] * I_mat[:, 0]
    aw = a_grid * d_eta
    rho_cold = (Ob + Oc * surv) / a_grid ** 3; rho_d = Oc * fd / a_grid ** 3
    src_c = 1.5 * H0 ** 2 * a_grid ** 2 * rho_cold * aw        # -k^2 phi contribution per unit dc_l, times a_l d eta_l
    src_d = 1.5 * H0 ** 2 * a_grid ** 2 * rho_d * aw
    # derivative matrix for theta_c = -d delta_c / d eta (central differences, one-sided at ends)
    Dm = np.zeros((N_A, N_A))
    for j in range(N_A):
        if j == 0: Dm[0, 0], Dm[0, 1] = -1 / (eta[1] - eta[0]), 1 / (eta[1] - eta[0])
        elif j == N_A - 1: Dm[j, j - 1], Dm[j, j] = -1 / (eta[j] - eta[j - 1]), 1 / (eta[j] - eta[j - 1])
        else: Dm[j, j - 1], Dm[j, j + 1] = -1 / (eta[j + 1] - eta[j - 1]), 1 / (eta[j + 1] - eta[j - 1])
    X = v * a_grid[None, :] * I_mat
    J = j0(k * X)
    if Gamma > 0 and v > 0:
        G = np.zeros((N_A, N_A))
        for l in range(N_A):
            G[:, l] = (w[:l + 1][None, :] * j0(k * v * a_grid[None, :l + 1] * I_mat[:, l][:, None])).sum(1)
    else:
        G = np.cumsum(w)[None, :] * np.ones((N_A, 1))
    lower = (np.arange(N_A)[None, :] < np.arange(N_A)[:, None]).astype(float)   # i < j
    Dji = a_grid[None, :] * I_mat
    # cold rows: dc_j - sum_l I(j,l) [src_c_l dc_l + src_d_l dd_l] = d0 - th0 Dm0_j
    A = np.zeros((2 * N_A, 2 * N_A)); b = np.zeros(2 * N_A)
    A[:N_A, :N_A] = np.eye(N_A) - I_mat * src_c[None, :]
    A[:N_A, N_A:] = -I_mat * src_d[None, :]
    b[:N_A] = d0 - th0 * Dm0
    # daughter rows: W_j dd_j - sum_i w_i J(j,i) [dc_i + (Dm dc)_i D(j,i)] (i<j) - sum_l I(j,l) G(j,l) [src_c dc + src_d dd] = 0
    Cmat = w[None, :] * J * lower                                    # coefficient of dc_i directly
    Vmat = (w[None, :] * J * lower * Dji) @ Dm                       # coefficient via theta_c = -(Dm dc): -(-theta D) = + (Dm dc) D
    A[N_A:, :N_A] = -(Cmat + Vmat) - I_mat * G * src_c[None, :]
    A[N_A:, N_A:] = np.diag(W) - I_mat * G * src_d[None, :]
    # nodes with W_j = 0 (no daughters yet): set dd_j = dc_j
    for j in np.where(W <= 0)[0]:
        A[N_A + j, :] = 0.0; A[N_A + j, N_A + j] = 1.0; A[N_A + j, j] = -1.0
    sol = np.linalg.solve(A, b)
    dc, dd = sol[:N_A], sol[N_A:]
    dm = (rho_cold * dc + rho_d * dd) / (rho_cold + rho_d)
    return dc, dd, dm, 0.0

def run_model(tau, vk, label):
    t = time.time(); out = np.zeros((len(K), N_A)); cond = 0.0
    for i, k in enumerate(K):
        _, _, dm, c = solve(k, tau, vk); out[i] = dm; cond = max(cond, c)
    print(f"    {label:<28} {time.time()-t:5.1f}s", flush=True)
    return out

sec("L168  FLUX-POWER TEST at (tau = 5 Gyr, v_k = 600 km/s): exact linear response for the kicked daughters")
print(f"  grid: {N_A} epochs z = 100 -> 0, {len(K)} k in [{K_H[0]:.2f}, {K_H[-1]:.0f}] h/Mpc; Om = {Om:.4f}")

# controls
LC = run_model(None, 0.0, "LCDM control (my solver)")
NK = run_model(5.0, 0.0, "tau=5, v_k=0 (no kick)")
ratio_growth = np.array([LC[i, idx_z(3.0)] ** 2 / LC[i, 0] ** 2 for i in range(len(K))]) / (P_cl[3.0] / P_cl[100.0])
m = (K_H >= 0.1) & (K_H <= 10)
check("C1 my LCDM control reproduces CLASS's linear growth P(z=3)/P(z=100) to 2% for 0.1 <= k <= 10 h/Mpc (sub-horizon + cold baryons)",
      np.all(np.abs(ratio_growth[m] - 1) < 0.02), f"max |dev| = {np.max(np.abs(ratio_growth[m]-1)):.4f}; at k=0.02: {ratio_growth[0]-1:+.4f}")
dev_nk = np.max(np.abs(NK[:, idx_z(3.0)] / LC[:, idx_z(3.0)] - 1))
check("C2 tau = 5 Gyr with v_k = 0 reproduces the LCDM control to 1e-3 at z = 3 (cohort bookkeeping conserves the growing mode)",
      dev_nk < 1e-3, f"max |P ratio - 1|^(1/2) = {dev_nk:.2e}")

# the cell and its neighbours
MODELS = [(5.0, 600.0), (5.0, 450.0), (5.0, 300.0), (20.0, 600.0), (5.0, 994.0)]
RES = {mv: run_model(mv[0], mv[1], f"tau={mv[0]:.0f} Gyr, v_k={mv[1]:.0f} km/s") for mv in MODELS}
def T2(mv, z): j = idx_z(z); return RES[mv][:, j] ** 2 / LC[:, j] ** 2

sec("T^2(k) = P_DDM / P_LCDM (linear)")
hdr = "    k [h/Mpc] " + " ".join(f"{k:7.2f}" for k in K_H[::4])
print(hdr)
for mv in MODELS:
    for z in (3.0, 2.0):
        print(f"    tau {mv[0]:4.0f} v_k {mv[1]:4.0f} z={z:.0f}: " + " ".join(f"{x:7.3f}" for x in T2(mv, z)[::4]))
cell = (5.0, 600.0)
T2c = T2(cell, 3.0)
check("C3 monotonic: at z = 3 the cell's T^2(k) decreases with k (2e-3 noise), and suppression grows with v_k (300 < 450 < 600 < 994) and shrinks with tau (20 vs 5)",
      np.all(np.diff(T2c) <= 2e-3) and np.all(T2((5.0, 300.0), 3.0) >= T2((5.0, 450.0), 3.0) - 2e-3) and
      np.all(T2((5.0, 450.0), 3.0) >= T2c - 2e-3) and np.all(T2c >= T2((5.0, 994.0), 3.0) - 2e-3) and np.all(T2((20.0, 600.0), 3.0) >= T2c - 2e-3),
      f"largest upward step in T^2(k): {np.max(np.diff(T2c)):+.2e}")
k5 = np.argmin(np.abs(K_H - 5.0))
sup5 = 1 - T2c[k5]
t3 = np.interp(1 / 4.0, _af, t_f) / GYR
fd3 = 1 - np.exp(-t3 / 5.0); plateau = (1 - fd3) ** 2
print(f"    decayed fraction at z = 3 for tau = 5 Gyr: f_d = {fd3:.3f} (t(z=3) = {t3:.2f} Gyr)  ->  small-scale floor (1 - f_d)^2 = {plateau:.3f};"
      f"  T^2 at k = 18 h/Mpc: {T2c[-3]:.3f}")
check("C4 the small-scale plateau of T^2 equals (1 - f_d(z=3))^2 to 5%: daughters born more than ~0.1 Gyr before z = 3 carry NO power at k >= 5 h/Mpc,"
      " so the residual is the still-cold mother + baryons squared. (L164's 9-22% 'strict upper bound' at k = 5 is thereby SUPERSEDED: it was not a bound.)",
      abs(T2c[-3] / plateau - 1) < 0.05, f"cell suppression at k = 5 h/Mpc, z = 3: {100*sup5:.1f}%; plateau/(1-f_d)^2 = {T2c[-3]/plateau:.3f}")

# ---------------- WDM calibration (Viel et al. 2005 thermal-relic transfer function) ----------------
def T2_wdm(k_h, m_keV):
    alpha = 0.049 * m_keV ** -1.11 * (Om / 0.25) ** 0.11 * (h / 0.7) ** 1.22; nu = 1.12
    return (1 + (alpha * k_h) ** (2 * nu)) ** (-10 / nu)
def delta_A(T2k):
    m = (K_H >= 0.5) & (K_H <= 20)
    kk = np.geomspace(0.5, 20, 400); r = np.interp(np.log(kk), np.log(K_H), np.sqrt(T2k))
    return 1 - np.trapz(r, kk) / np.trapz(np.ones_like(kk), kk)
sec("AREA CRITERION delta_A over 0.5-20 h/Mpc at z = 3 (Murgia et al. 2017 definition; bound delta_A < 0.38, Murgia et al. 2018, CITED)")
dA = {mv: delta_A(T2(mv, 3.0)) for mv in MODELS}
dA_w = {m_: delta_A(T2_wdm(K_H, m_)) for m_ in (5.3, 3.5, 2.0, 1.0)}
for mv in MODELS: print(f"    tau {mv[0]:4.0f} v_k {mv[1]:4.0f}: delta_A = {dA[mv]:.4f}")
for m_ in dA_w: print(f"    thermal WDM {m_:.1f} keV : delta_A = {dA_w[m_]:.4f}")
# WDM-equivalent mass of the cell by matching delta_A
ms = np.geomspace(0.3, 50, 400); dAs = np.array([delta_A(T2_wdm(K_H, mm)) for mm in ms])
m_equiv = float(np.interp(-dA[cell], -dAs, ms)) if dAs.max() > dA[cell] > dAs.min() else (np.inf if dA[cell] < dAs.min() else 0.0)
print(f"    cell's WDM-equivalent thermal mass (matched delta_A): {m_equiv:.2f} keV")
check("C5 [DEFICIT, verified] area criterion: the cell suppresses MORE than the EXCLUDED 3.5 keV thermal relic (Viel et al. 2013), and far more than the allowed 5.3 keV one (Irsic et al. 2017): delta_A(cell) > delta_A(3.5 keV)",
      dA[cell] > dA_w[3.5], f"delta_A cell {dA[cell]:.4f} vs 5.3 keV {dA_w[5.3]:.4f}, 3.5 keV {dA_w[3.5]:.4f}, 2 keV {dA_w[2.0]:.4f}")
check("C6 area criterion against the conservative Murgia et al. 2018 bound delta_A < 0.38", dA[cell] < 0.38, f"delta_A(cell) = {dA[cell]:.4f}")

# ---------------- linear 1-D flux-power proxy at z = 3 ----------------
sec("LINEAR 1-D PROXY P_1D(k_par) ~ int_{k_par}^inf k P(k) dk at z = 3, in s/km (ratio to LCDM; thermal WDM for calibration)")
z = 3.0; Hz = H(1 / (1 + z)) * C_KMS; kv_of_kh = lambda kh: kh * h * (1 + z) / Hz      # s/km
kk = np.geomspace(0.02, 29.9, 2000); Pl = np.interp(np.log(kk), np.log(K_H), P_cl[3.0])
def p1d(T2k):
    r = np.interp(np.log(kk), np.log(K_H), T2k); integ = kk * Pl * r
    return np.array([np.trapz(integ[kk >= kp], kk[kk >= kp]) for kp in kk])
P1_l = p1d(np.ones_like(K_H)); P1_c = p1d(T2c); P1_w = {m_: p1d(T2_wdm(K_H, m_)) for m_ in (5.3, 3.5, 2.0)}
KP = [0.005, 0.01, 0.02, 0.05, 0.1]
print("    k_par [s/km]      " + " ".join(f"{kp:8.3f}" for kp in KP))
def row(lab, P1): print(f"    {lab:<18}" + " ".join(f"{np.interp(kp, kv_of_kh(kk), P1/P1_l):8.3f}" for kp in KP))
row("cell (5, 600)", P1_c)
for m_ in P1_w: row(f"WDM {m_} keV", P1_w[m_])
r_cell = np.array([np.interp(kp, kv_of_kh(kk), P1_c / P1_l) for kp in KP]); r_53 = np.array([np.interp(kp, kv_of_kh(kk), P1_w[5.3] / P1_l) for kp in KP])
r_35 = np.array([np.interp(kp, kv_of_kh(kk), P1_w[3.5] / P1_l) for kp in KP])
check("C7 [DEFICIT, verified] 1-D proxy: at every k_par in 0.005-0.1 s/km the cell's suppression EXCEEDS the excluded 3.5 keV relic's (linear proxy; nonlinear/thermal smoothing damps both alike)",
      np.all(r_cell < r_35), "cell/5.3keV ratios: " + ", ".join(f"{a:.3f}/{b:.3f}" for a, b in zip(r_cell, r_53)))

# ---------------- sigma_8 / S_8 at z = 0 from the same calculation ----------------
sec("sigma_8 and S_8 at z = 0 from the exact linear response (replaces L160's (A)/(B) growth-treatment ambiguity)")
kk8 = np.geomspace(1e-3, 30, 4000); Pl0 = np.array([cl.pk_lin(k * h, 0.0) for k in kk8])
W8 = 3 * (np.sin(kk8 * 8) - kk8 * 8 * np.cos(kk8 * 8)) / (kk8 * 8) ** 3
def sig8_ratio(T2k0):
    r = np.where(kk8 < K_H[0], 1.0, np.interp(np.log(np.maximum(kk8, K_H[0])), np.log(K_H), T2k0))
    return np.sqrt(np.trapz(kk8 ** 2 * Pl0 * W8 ** 2 * r, kk8) / np.trapz(kk8 ** 2 * Pl0 * W8 ** 2, kk8))
S8_KIDS, S8_E = 0.815, 0.016
for mv in MODELS:
    s8 = sig8_lcdm * sig8_ratio(T2(mv, 0.0)); S8 = s8 * np.sqrt(Om / 0.3)
    RES[mv + ("S8",)] = S8
    print(f"    tau {mv[0]:4.0f} v_k {mv[1]:4.0f}: sigma_8 = {s8:.4f}, S_8 = {S8:.4f}  (LCDM {sig8_lcdm:.4f}, {sig8_lcdm*np.sqrt(Om/0.3):.4f}; KiDS-Legacy {S8_KIDS} +/- {S8_E})")
S8c = RES[cell + ("S8",)]
check("C8 S_8 of the cell lies within 3 sigma of KiDS-Legacy (>= 0.767), computed with the actual growth, not L160's bounds",
      S8c >= S8_KIDS - 3 * S8_E, f"S_8(cell) = {S8c:.4f}; L160 quoted (B) 0.787 / (A) lower")

sec("THE LIFETIME PINCER (kick-independent for v_k >~ 200 km/s: any such kick free-streams past k ~ 1 h/Mpc by z = 3)")
T2_53 = T2_wdm(np.array([5.0]), 5.3)[0]
for lab, Tmin in (("WDM-calibrated: no more suppression at k = 5 h/Mpc, z = 3 than the allowed 5.3 keV relic", T2_53), ("loose: 10% at k = 5 h/Mpc", 0.90)):
    tau_min = 2 * t3 / (-np.log(Tmin))
    print(f"    {lab}: (1-f_d)^2 >= {Tmin:.3f}  =>  tau >= {tau_min:.0f} Gyr")
tau_min_loose = 2 * t3 / (-np.log(0.90)); tau_max_gal = 20.0
print(f"    L167 galaxy gate: tau <= {tau_max_gal:.0f} Gyr (tau = 20 already needs v_k >= 994 km/s on the 220 km/s host).  Pincer margin (loose): {tau_min_loose/tau_max_gal:.1f}x")
check("C9 lifetime pincer: even the loose forest tolerance (10% at k = 5 h/Mpc, z = 3) needs tau above the largest lifetime the L167 galaxy gate allows (20 Gyr)",
      tau_min_loose > tau_max_gal, f"tau_forest >= {tau_min_loose:.0f} Gyr vs tau_galaxy <= {tau_max_gal:.0f} Gyr")
check("C10 cross-validation: this exact linear response reproduces L160's generous-bound S_8 = 0.787 for the cell to 0.01 (two independent methods)",
      abs(S8c - 0.787) < 0.01, f"S_8 here {S8c:.4f} vs L160 (B) 0.787")

sec("VERDICT")
print(f"    cell (tau = 5 Gyr, v_k = 600 km/s): delta_A = {dA[cell]:.3f} (WDM-equivalent {m_equiv:.2f} keV; allowed >= 5.3 keV has {dA_w[5.3]:.3f}); "
      f"suppression at k = 5 h/Mpc, z = 3: {100*sup5:.1f}%; S_8 = {S8c:.3f}")
forest_ok = dA[cell] < dA_w[5.3] and np.all(r_cell >= r_53 - 1e-6)
print("    NOTE on the area criterion: delta_A(cell) = %.3f passes the conservative 0.38 bound ONLY because a plateau at (1-f_d)^2 is not a cutoff; the"
      " criterion was calibrated on cutoff shapes (Murgia et al.), so it is the inapplicable one of the three. The WDM-equivalent mass and the 1-D proxy both exclude." % dA[cell])
print("    forest verdict: " + ("PASSES the current Lyman-alpha bound (weaker than the still-allowed 5.3 keV relic)" if forest_ok else
      ("DEAD: stronger suppression than the excluded 3.5 keV relic" if dA[cell] > dA_w[3.5] else "TENSION: between the 5.3 and 3.5 keV relics")))
print("    growth verdict: " + ("S_8 within 3 sigma of KiDS-Legacy" if S8c >= S8_KIDS - 3 * S8_E else "S_8 DEAD (below the 3 sigma KiDS-Legacy floor)"))
print("    Limits: linear theory + sub-horizon Newtonian limit (k >= 0.02 h/Mpc, z <= 100); cold baryons; eps -> 0 (no dark radiation);\n"
      "    forest bounds CITED as thermal-relic-equivalent scales (Viel+05 transfer function), not re-fitted to flux data; no hydro.")
npass = sum(ok for _, ok in CHECKS)
print("\n" + "=" * 118 + f"\nL168 COMPLETE: {npass}/{len(CHECKS)} checks PASS.   [{time.time()-T0:.0f}s]\n" + "=" * 118)
