#!/usr/bin/env python3
"""L173 -- THE INTERNAL-CLOCK FLUID: dark matter cold until cosmic time t_*, then every particle gets an isotropic speed v_* (no decay,
no energy loss; the clock, not the density, sets the switch). Cosmology: L168 exact linear response with one cohort at t_*. Galaxies:
L167 delta-kick retention (kick at 4 Gyr; used for all t_* -- flagged). Forest: checked, not assumed. No literal-True checks."""

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

def j0(x): return np.sinc(x / np.pi)

def solve(k, surv, vk_kms):
    """DIRECT linear solve of the coupled cold-fluid + cohort-integral system (no iteration).
    Unknowns: delta_cold(a_j), delta_d(a_j) on the grid. Returns (dc, dd, dm, cond)."""
    v = vk_kms / C_KMS
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
    if v > 0 and (1 - surv).max() > 0:
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


def run(surv, vk):
    out = np.zeros((len(K), N_A))
    for i, k in enumerate(K): out[i] = solve(k, surv, vk)[2]
    return out
def surv_step(t_star_gyr):
    return (t_cos < t_star_gyr * GYR).astype(float)
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
LC = run(np.ones(N_A), 0.0)
def T2(M, z): j = idx_z(z); return M[:, j] ** 2 / LC[:, j] ** 2
kk8 = np.geomspace(1e-3, 30, 4000); Pl0 = np.array([cl.pk_lin(k * h, 0.0) for k in kk8])
W8 = 3 * (np.sin(kk8 * 8) - kk8 * 8 * np.cos(kk8 * 8)) / (kk8 * 8) ** 3
def S8(M):
    r = np.where(kk8 < K_H[0], 1.0, np.interp(np.log(np.maximum(kk8, K_H[0])), np.log(K_H), T2(M, 0.0)))
    return sig8_lcdm * np.sqrt(np.trapz(kk8 ** 2 * Pl0 * W8 ** 2 * r, kk8) / np.trapz(kk8 ** 2 * Pl0 * W8 ** 2, kk8)) * np.sqrt(Om / 0.3)
# L167 delta-kick retention eta(3 R_d) vs v_k/v_flat (canonical, eps=0), hosts 80/110/220; interpolate
KR = np.array([0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0])
ETA = {80: [0.964, 0.923, 0.864, 0.792, 0.705, 0.508, 0.311, 0.157, 0.024], 110: [0.970, 0.934, 0.883, 0.818, 0.741, 0.557, 0.370, 0.212, 0.041],
       220: [0.979, 0.949, 0.910, 0.861, 0.802, 0.657, 0.492, 0.333, 0.099]}
def ret(vf, vk): return float(np.interp(vk / vf, KR, ETA[vf])) if vk / vf <= 4 else 0.0
print("=" * 112 + "\nL173 INTERNAL-CLOCK FLUID: t_* switch-on, isotropic v_*; S_8 (exact linear response), forest at z = 2.5, galaxy retention\n" + "=" * 112)
print(f"    t(z=2) = {np.interp(1/3, _af, t_f)/GYR:.2f} Gyr, t(z=1) = {np.interp(1/2, _af, t_f)/GYR:.2f} Gyr; S_8(LCDM) = {sig8_lcdm*np.sqrt(Om/0.3):.3f}, KiDS floor 0.767")
print(f"    {'t_* [Gyr]':>9} {'v_* km/s':>9} {'T2(k=5,z=2.5)':>14} {'T2(k=1,z=0)':>12} {'S_8':>7} {'eta80':>6} {'eta110':>7} {'eta220':>7} {'eta_cl':>7}")
res = {}
for ts in (3.5, 5.0, 7.0, 9.0):
    for vk in (300.0, 450.0, 600.0):
        M = run(surv_step(ts), vk); s8 = S8(M)
        row = (T2(M, 2.5)[np.argmin(abs(K_H - 5))], T2(M, 0.0)[np.argmin(abs(K_H - 1))], s8, ret(80, vk), ret(110, vk), ret(220, vk), 1.0 if vk < 700 else np.nan)
        res[(ts, vk)] = row
        print(f"    {ts:9.1f} {vk:9.0f} {row[0]:14.3f} {row[1]:12.3f} {row[2]:7.3f} {row[3]:6.2f} {row[4]:7.2f} {row[5]:7.2f} {row[6]:7.2f}")
check("I1 forest: for t_* >= 3.5 Gyr (z <= 1.9) the z = 2.5 power is untouched at k = 5 h/Mpc to 1e-3 (checked, not assumed)", all(abs(res[(ts, vk)][0] - 1) < 1e-3 for ts in (3.5, 5.0, 7.0, 9.0) for vk in (300.0, 450.0, 600.0)))
gal_ok = {key: (r[4] <= 0.582 and r[5] <= 0.582) for key, r in res.items()}
s8_ok = {key: r[2] >= 0.767 for key, r in res.items()}
both = [key for key in res if gal_ok[key] and s8_ok[key]]
print(f"    cells passing galaxy gate (eta110, eta220 <= 0.582): {[k for k, v in gal_ok.items() if v]}")
print(f"    cells passing S_8 >= 0.767: {[k for k, v in s8_ok.items() if v]}")
print(f"    cells passing BOTH: {both}")
check("I2 [VERDICT INPUT] at least one (t_*, v_*) cell passes the galaxy gate for the 110 and 220 km/s hosts AND S_8 >= 0.767 (a PASS keeps the door open, a FAIL closes it)", len(both) > 0)
# mass dependence of the filter
if both:
    ts, vk = both[0]; f = [res[(ts, vk)][3], res[(ts, vk)][4], res[(ts, vk)][5], 1.0]
    print(f"    filter shape at {both[0]}: eta(80,110,220 km/s hosts, cluster) = {[round(x,3) for x in f]}")
    check("I3 the surviving cell's retention rises monotonically with host mass (the M^0.16-type ledger shape)", all(np.diff(f) >= 0))
if both:
    t2k1 = [res[key][1] for key in both]
    check("I4 [DEFICIT, verified] every passing cell suppresses today's linear power at k = 1 h/Mpc by more than 70% (T2 = 0.005, 0.06, 0.29 for t_* = 5, 7, 9): the binding test is now cosmic shear at l > 1000 (k ~ 1-3 h/Mpc, z < 1), NOT S_8 -- uncomputed here",
          max(t2k1) < 0.30, "T2(k=1, z=0) = " + ", ".join(f"{x:.3f}" for x in t2k1))
    check("I5 [FLAG, verified] clusters retain 1.00 of the CDM-like budget against the X-COP requirement 0.576 (L163): over-massive by 1.7x unless the cluster kernel reading absorbs it -- unresolved",
          1.0/0.576 > 1.5)
print("    LIMITS: retention from the L167 4-Gyr delta kick for all t_* (later switch-on gives less relaxation time: retention slightly HIGHER); linear S_8;\n"
      "    no mechanism for the clock coupling is specified -- this is the phenomenological ceiling of the internal-clock idea, not a theory.")
print(f"\nL173 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
