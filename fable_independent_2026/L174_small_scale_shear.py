#!/usr/bin/env python3
"""L174 -- SMALL-SCALE COSMIC SHEAR for the internal-clock fluid (bracketed: linear-suppressed halofit as lower bound, frozen small-scale nonlinear power at t_* as upper bound); Limber, KiDS-like n(z); L173 machinery.
L173 header:: dark matter cold until cosmic time t_*, then every particle gets an isotropic speed v_* (no decay,
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
from scipy.integrate import cumulative_trapezoid as ctz
# nonlinear LCDM power from CLASS halofit on a z grid
cln = Class(); cln.set({"h": h, "omega_b": omb, "omega_cdm": omc, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046, "N_ncdm": 0,
                        "YHe": 0.2454, "output": "mPk", "P_k_max_h/Mpc": 60, "z_max_pk": 3.0, "non_linear": "halofit"}); cln.compute()
ZS = np.linspace(0.0, 2.5, 26); KK = np.geomspace(0.01, 50, 160)     # k in h/Mpc
PNL = np.array([[cln.pk(k * h, zz) for k in KK] for zz in ZS])          # (Mpc)^3
LC = run(np.ones(N_A), 0.0)
def T2grid(M):
    """linear T^2(k, z) on (ZS, KK); T^2 = 1 for k < K_H[0]; extrapolate flat above K_H[-1]"""
    out = np.ones((len(ZS), len(KK)))
    for i, zz in enumerate(ZS):
        j = idx_z(zz); t2 = M[:, j] ** 2 / LC[:, j] ** 2
        out[i] = np.where(KK < K_H[0], 1.0, np.interp(np.log(np.clip(KK, K_H[0], K_H[-1])), np.log(K_H), t2))
    return out
# Limber
zf = np.linspace(1e-3, 2.5, 400); af = 1 / (1 + zf)
chi = np.array([np.interp(1.0, _af, eta_f) - np.interp(a_, _af, eta_f) for a_ in af])          # comoving distance [Mpc]
nz = zf ** 2 * np.exp(-(zf / 0.5) ** 1.5); nz /= np.trapz(nz, zf)
# lensing efficiency q(chi) = int_chi^inf n(chi') (chi'-chi)/chi' dchi'
dchi_dz = np.gradient(chi, zf); nchi = nz / dchi_dz
q = np.array([np.trapz(nchi[i:] * (chi[i:] - chi[i]) / np.maximum(chi[i:], 1e-6), chi[i:]) for i in range(len(zf))])
W = 1.5 * Om * H0 ** 2 * (1 + zf) * chi * q
def Cl(Pfun, ells):
    out = []
    for l in ells:
        k = (l + 0.5) / np.maximum(chi, 1e-3) / h        # h/Mpc
        integrand = W ** 2 / np.maximum(chi, 1e-3) ** 2 * np.array([Pfun(kk_, zz) for kk_, zz in zip(k, zf)])
        out.append(np.trapz(integrand, chi))
    return np.array(out)
def P_of(grid):   # 2-D interpolator in (z, log k) of a power grid on (ZS, KK)
    def f(k_, z_):
        if k_ > KK[-1] or k_ < KK[0]: return 0.0
        i = np.clip(np.searchsorted(ZS, z_) - 1, 0, len(ZS) - 2); w = (z_ - ZS[i]) / (ZS[i + 1] - ZS[i])
        row = (1 - w) * grid[i] + w * grid[i + 1]
        return float(np.exp(np.interp(np.log(k_), np.log(KK), np.log(np.maximum(row, 1e-300)))))
    return f
ELLS = np.array([100, 300, 1000, 2000, 3000])
Cl_lcdm = Cl(P_of(PNL), ELLS)
print("=" * 112 + "\nL174 SMALL-SCALE COSMIC SHEAR: C_l ratio to LCDM (KiDS-like n(z), z0 = 0.5), lower/upper bounds\n" + "=" * 112)
print(f"    {'cell':>14} {'bound':>7} " + " ".join(f"l={l:>5}" for l in ELLS))
TOL = 0.10   # cited scale: KiDS-1000 / DES-Y3 band-power precision ~10% at l ~ 300-1500; baryon feedback allows ~10-20% at l ~ 3000
verd = {}
for ts in (5.0, 7.0, 9.0):
    M = run(surv_step(ts), 600.0); T2 = T2grid(M)
    lower = PNL * T2
    iz = np.searchsorted(ZS, 1 / np.interp(ts * GYR, t_f, _af) - 1)     # index of z_*
    frozen = PNL.copy()
    for i in range(len(ZS)):
        if ZS[i] < ZS[min(iz, len(ZS) - 1)]:
            frozen[i] = np.maximum(lower[i], np.where(KK > 0.3, PNL[min(iz, len(ZS) - 1)], lower[i]))
    rl = Cl(P_of(lower), ELLS) / Cl_lcdm; ru = Cl(P_of(frozen), ELLS) / Cl_lcdm
    verd[ts] = (rl, ru)
    print(f"    t_*={ts:4.1f} v=600 {'lower':>7} " + " ".join(f"{x:7.3f}" for x in rl))
    print(f"    {'':>14} {'upper':>7} " + " ".join(f"{x:7.3f}" for x in ru))
i1000 = list(ELLS).index(1000); i300 = list(ELLS).index(300)
check("S1 [DEFICIT, verified] LOWER bound (linear suppression on halofit): every passing cell loses more than 30% of the shear power at l = 1000",
      all(verd[ts][0][i1000] < 0.70 for ts in verd), ", ".join(f"{ts}: {verd[ts][0][i1000]:.2f}" for ts in verd))
check("S2 [DECISIVE DEFICIT, verified] even the UPPER bound (all small-scale nonlinear power frozen at t_*) falls below the ~10% band-power tolerance at l = 1000 for every cell: the internal-clock fluid is DEAD by small-scale cosmic shear",
      all(verd[ts][1][i1000] < 1 - TOL for ts in verd), ", ".join(f"{ts}: l300 {verd[ts][1][i300]:.2f}, l1000 {verd[ts][1][i1000]:.2f}" for ts in verd))
check("S3 the bracket is real: upper >= lower at every l for every cell", all(np.all(verd[ts][1] >= verd[ts][0] - 1e-9) for ts in verd))
print("    LIMITS: no N-body for this fluid; the upper bound keeps ALL nonlinear power formed by t_* (true only for hosts with v_esc > 600 km/s, i.e. groups\n"
      "    and clusters; galaxy-scale halos evaporate and their 1-halo power is lost), so the truth lies between the bounds and closer to the lower one at\n"
      "    l >~ 1000; single broad source bin; tolerance is a cited scale, not a re-fit to KiDS/DES band powers.")
print(f"\nL174 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
