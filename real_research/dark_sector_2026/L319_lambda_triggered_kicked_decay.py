#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L319 -- THE LAMBDA-TRIGGERED KICKED DECAY: the one dark-sector door the record left untested, through the forest and S8.

WHY.  The record's dark-sector ledger (hermes_push/CONTEXT_DIGEST.md; L166 certified necessity) needs a real cold component
whose retained fraction RISES WITH HOST MASS: the CMB >= 0.988 of a cold budget; clusters ~0.58 of a CDM-like halo at R500;
disc galaxies <= 0.2 (dwarfs) to <= 0.5 (massive discs) by the SPARC dynamics bound (hunt_2026/h_kids_halo_bound_CORRECTION,
which withdrew the old KiDS 6-14%).  Kicked two-body decay gives exactly that mass trend (daughters escape shallow wells,
stay in deep ones).  It was closed ONLY for a UNIVERSAL lifetime -- the "lifetime pincer" of L167/L168: the Lyman-alpha
forest needs tau >= 41 Gyr (few decays by z = 3) while galaxies need tau <= 20 Gyr -- and the record's open-door statement
explicitly excludes only "a decay/kick with a universal lifetime".  A decay rate that SWITCHES ON WHEN THE VACUUM DOMINATES
evades the pincer by construction: nothing decays at z >= 2 (the forest, recombination), most of it decays at z < 1.  It
also ties the dark sector to the same rho_Lambda that sets a0 in this framework.  This lane tests it on the two quantitative
gates that killed the universal version, with the SAME validated exact linear-response solver (L168, copied, not edited).

THE MODEL.  X -> Y + (light), isotropic kick v_k to the daughter, which inherits the mother's position and bulk velocity;
energy to the light product (~v_k/c) neglected.  Rate
      Gamma(a) = Gamma_0 [Omega_Lambda(a)/Omega_Lambda,0]^p ,   Omega_Lambda(a) = OL/(Om a^-3 + Or a^-4 + OL),
p in {1, 2}, Gamma_0 set by the decayed fraction today f_d(0).  Survival S(t) = exp(-int Gamma dt); everything else is L168.

GATES (thresholds from L168, not re-chosen):
  F  the forest: T^2(k = 5 h/Mpc) at z = 3 AND z = 2 no lower than the ALLOWED 5.3 keV thermal relic's (Irsic+2017,
     the strict WDM-calibrated reading); the loose 10% reading also reported.
  S  S_8 at z = 0 within 3 sigma of KiDS-Legacy (>= 0.767, as L168 used); DES-Y3 and Planck also printed.
  G  galaxies: the decayed fraction today must deplete the halo to the dynamics bound (f_d(0) >= 0.8 for dwarfs, with full
     escape), and the kick must escape a disc: v_k >~ 2-3 v_flat (L167's N-body: eta(3R_d) = 0.58 at v_k = 1.8-2.2 v_flat).
     Recorded as a requirement on (f_d(0), v_k), not re-simulated here.
CONTROLS: C1 LCDM growth vs CLASS; C2 v_k = 0 reproduces LCDM (cohort bookkeeping); C3 the universal tau = 5 Gyr, 600 km/s
cell reproduces L168's S_8 = 0.787 and its forest failure; MUTATE=1 replaces the trigger by the universal lifetime with the
same f_d(0): the forest gate must then FAIL (rc = 1).

Run from the repository root:  python3 real_research/dark_sector_2026/L319_lambda_triggered_kicked_decay.py
"""
import os, sys, json, time, warnings
import numpy as np
# spurious Accelerate-BLAS matmul warnings (results are finite and cross-checked by C1-C3); silenced so no machine path is printed
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*encountered in matmul")
from scipy.integrate import cumulative_trapezoid

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L319_lambda_triggered_kicked_decay"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L319", "mutate": MUTATE, "checks": {}, "numbers": {}}


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


P(__doc__)
# ---------------- cosmology and grids: identical to L168 ----------------
h = 0.6736; H0 = 100 * h / 299792.458
omb, omc = 0.02237, 0.1200
Ob, Oc = omb / h ** 2, omc / h ** 2; Om = Ob + Oc
Or = 4.18e-5 / h ** 2 * (1 + 0.2271 * 3.046); OL = 1 - Om - Or
def H(a): return H0 * np.sqrt(Or * a ** -4 + Om * a ** -3 + OL)
GYR = 299792.458 / 977.792
C_KMS = 299792.458
A_INIT = 1.0 / 101.0
N_A = int(os.environ.get('L319_NA', '420'))
a_grid = np.geomspace(A_INIT, 1.0, N_A)
_af = np.geomspace(1e-4, 1.0, 40000)
eta_f = cumulative_trapezoid(1.0 / (_af ** 2 * H(_af)), _af, initial=0.0)
t_f = cumulative_trapezoid(1.0 / (_af * H(_af)), _af, initial=0.0)
eta = np.interp(a_grid, _af, eta_f); t_cos = np.interp(a_grid, _af, t_f)
AGE_GYR = t_f[-1] / GYR
F = cumulative_trapezoid(1.0 / a_grid, eta, initial=0.0)
I_mat = np.maximum(F[:, None] - F[None, :], 0.0)
d_eta = np.gradient(eta)
def idx_z(z): return int(np.argmin(np.abs(a_grid - 1 / (1 + z))))

from classy import Class
cl = Class()
cl.set({"h": h, "omega_b": omb, "omega_cdm": omc, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046,
        "N_ncdm": 0, "YHe": 0.2454, "output": "mPk", "P_k_max_h/Mpc": 45, "z_pk": "100, 3, 2.5, 2, 0"})
cl.compute()
K_H = np.geomspace(0.02, 30.0, 44); K = K_H * h
P_cl = {z: np.array([cl.pk_lin(k, z) for k in K]) for z in (100.0, 3.0, 2.5, 2.0, 0.0)}
sig8_lcdm = cl.sigma8()
f_init = cl.scale_independent_growth_factor_f(100.0)
P(f"  CLASS LCDM: sigma8 = {sig8_lcdm:.4f}, age = {AGE_GYR:.2f} Gyr")


# ---------------- decay histories ----------------
def omega_L(a):
    return OL / (Om * a ** -3 + Or * a ** -4 + OL)


def surv_universal(tau_gyr):
    return np.exp(-t_cos / (tau_gyr * GYR))


def surv_triggered(fd0, p):
    """Gamma = Gamma0 (Omega_L(a)/Omega_L0)^p, normalised so that 1 - S(today) = fd0."""
    shape = (omega_L(_af) / omega_L(1.0)) ** p / (_af * H(_af))          # dt/da * rate-shape
    cum = cumulative_trapezoid(shape, _af, initial=0.0)                   # int shape dt (in Mpc units)
    g0 = -np.log(1 - fd0) / cum[-1]
    return np.exp(-g0 * np.interp(a_grid, _af, cum)), g0


def j0(x): return np.sinc(x / np.pi)


def solve(k, surv, vk_kms):
    """L168's direct linear solve, with the survival function S(t) supplied (the ONLY change)."""
    v = vk_kms / C_KMS
    w = np.append(-np.diff(surv), 0.0)
    W = np.cumsum(w) - w
    fd = 1 - surv
    d0 = np.sqrt(np.interp(k, K, P_cl[100.0]))
    th0 = -a_grid[0] * H(a_grid[0]) * f_init * d0
    Dm0 = a_grid[0] * I_mat[:, 0]
    aw = a_grid * d_eta
    rho_cold = (Ob + Oc * surv) / a_grid ** 3; rho_d = Oc * fd / a_grid ** 3
    src_c = 1.5 * H0 ** 2 * a_grid ** 2 * rho_cold * aw
    src_d = 1.5 * H0 ** 2 * a_grid ** 2 * rho_d * aw
    Dm = np.zeros((N_A, N_A))
    for j in range(N_A):
        if j == 0: Dm[0, 0], Dm[0, 1] = -1 / (eta[1] - eta[0]), 1 / (eta[1] - eta[0])
        elif j == N_A - 1: Dm[j, j - 1], Dm[j, j] = -1 / (eta[j] - eta[j - 1]), 1 / (eta[j] - eta[j - 1])
        else: Dm[j, j - 1], Dm[j, j + 1] = -1 / (eta[j + 1] - eta[j - 1]), 1 / (eta[j + 1] - eta[j - 1])
    X = v * a_grid[None, :] * I_mat
    J = j0(k * X)
    if w.sum() > 0 and v > 0:
        G = np.zeros((N_A, N_A))
        for l in range(N_A):
            G[:, l] = (w[:l + 1][None, :] * j0(k * v * a_grid[None, :l + 1] * I_mat[:, l][:, None])).sum(1)
    else:
        G = np.cumsum(w)[None, :] * np.ones((N_A, 1))
    lower = (np.arange(N_A)[None, :] < np.arange(N_A)[:, None]).astype(float)
    Dji = a_grid[None, :] * I_mat
    A = np.zeros((2 * N_A, 2 * N_A)); b = np.zeros(2 * N_A)
    A[:N_A, :N_A] = np.eye(N_A) - I_mat * src_c[None, :]
    A[:N_A, N_A:] = -I_mat * src_d[None, :]
    b[:N_A] = d0 - th0 * Dm0
    Cmat = w[None, :] * J * lower
    Vmat = (w[None, :] * J * lower * Dji) @ Dm
    A[N_A:, :N_A] = -(Cmat + Vmat) - I_mat * G * src_c[None, :]
    A[N_A:, N_A:] = np.diag(W) - I_mat * G * src_d[None, :]
    for j in np.where(W <= 0)[0]:
        A[N_A + j, :] = 0.0; A[N_A + j, N_A + j] = 1.0; A[N_A + j, j] = -1.0
    sol = np.linalg.solve(A, b)
    dc, dd = sol[:N_A], sol[N_A:]
    return (rho_cold * dc + rho_d * dd) / (rho_cold + rho_d)


def run(surv, vk):
    return np.array([solve(k, surv, vk) for k in K])


def T2(res, lc, z):
    j = idx_z(z); return res[:, j] ** 2 / lc[:, j] ** 2


def T2_wdm(k_h, m_keV):
    alpha = 0.049 * m_keV ** -1.11 * (Om / 0.25) ** 0.11 * (h / 0.7) ** 1.22; nu = 1.12
    return (1 + (alpha * k_h) ** (2 * nu)) ** (-10 / nu)


kk8 = np.geomspace(1e-3, 30, 4000); Pl0 = np.array([cl.pk_lin(k * h, 0.0) for k in kk8])
W8 = 3 * (np.sin(kk8 * 8) - kk8 * 8 * np.cos(kk8 * 8)) / (kk8 * 8) ** 3


def S8_of(T2k0):
    r = np.where(kk8 < K_H[0], 1.0, np.interp(np.log(np.maximum(kk8, K_H[0])), np.log(K_H), T2k0))
    s8 = sig8_lcdm * np.sqrt(np.trapz(kk8 ** 2 * Pl0 * W8 ** 2 * r, kk8) / np.trapz(kk8 ** 2 * Pl0 * W8 ** 2, kk8))
    return s8 * np.sqrt(Om / 0.3)


k5 = int(np.argmin(np.abs(K_H - 5.0)))
T2_53 = float(T2_wdm(np.array([K_H[k5]]), 5.3)[0])
S8_KIDS, S8_E = 0.815, 0.016
S8_FLOOR = S8_KIDS - 3 * S8_E

# ============================================================================================ controls
banner("CONTROLS")
one = np.ones(N_A)
LC = run(one, 0.0)
ratio_growth = (LC[:, idx_z(3.0)] ** 2 / LC[:, 0] ** 2) / (P_cl[3.0] / P_cl[100.0])
m = (K_H >= 0.1) & (K_H <= 10)
check("C1 LCDM control reproduces CLASS's growth P(z=3)/P(z=100) to 2% on 0.1-10 h/Mpc", f"max dev {np.max(np.abs(ratio_growth[m]-1)):.4f}",
      np.all(np.abs(ratio_growth[m] - 1) < 0.02))
sT, g0 = surv_triggered(0.9, 1)
NK = run(sT, 0.0)
dev = float(np.max(np.abs(NK[:, idx_z(0.0)] / LC[:, idx_z(0.0)] - 1)))
check("C2 the triggered decay with v_k = 0 reproduces LCDM at z = 0 to 2e-3 in delta (0.4% in P, 5x below the smallest "
      "S_8 effect reported); the residual is FIRST-ORDER DISCRETISATION: 1.56e-3 / 1.11e-3 / 7.7e-4 at N_A = 300 / 420 / "
      "600 (L319_c2_convergence.py)", f"max |ratio - 1| = {dev:.2e} at N_A = {N_A}", dev < 2e-3)
U5 = run(surv_universal(5.0), 600.0)
S8_u = S8_of(T2(U5, LC, 0.0)); t2u = T2(U5, LC, 3.0)[k5]
OUT["numbers"]["control_universal_5Gyr_600"] = dict(S8=S8_u, T2_k5_z3=t2u)
check("C3 the universal tau = 5 Gyr, v_k = 600 km/s cell reproduces L168: S_8 = 0.787 +/- 0.01, and fails the forest",
      f"S_8 = {S8_u:.4f}; T^2(k=5, z=3) = {t2u:.3f} vs the allowed 5.3 keV {T2_53:.3f}",
      abs(S8_u - 0.787) < 0.01 and t2u < T2_53)

# ============================================================================================ scan
banner("THE SCAN: Gamma ~ Omega_Lambda(a)^p, f_d(0) and v_k; the forest (z = 3 and 2) and S_8 (z = 0)")
rows = []
for p in (1, 2):
    for fd0 in (0.8, 0.9):
        surv, _ = (surv_triggered(fd0, p) if not MUTATE else (surv_universal(-AGE_GYR / np.log(1 - fd0)), None))
        fd_z3 = 1 - surv[idx_z(3.0)]; fd_z2 = 1 - surv[idx_z(2.0)]; fd_z1 = 1 - surv[idx_z(1.0)]
        for vk in (400.0, 600.0, 800.0, 1000.0):
            R = run(surv, vk)
            t3, t2 = T2(R, LC, 3.0)[k5], T2(R, LC, 2.0)[k5]
            s8 = S8_of(T2(R, LC, 0.0))
            row = dict(p=p, fd0=fd0, vk=vk, fd_z3=float(fd_z3), fd_z2=float(fd_z2), fd_z1=float(fd_z1),
                       T2_k5_z3=float(t3), T2_k5_z2=float(t2), S8=float(s8),
                       forest_strict=bool(t3 >= T2_53 and t2 >= T2_53), forest_loose=bool(t3 >= 0.9 and t2 >= 0.9),
                       S8_ok=bool(s8 >= S8_FLOOR))
            rows.append(row)
            P(f"    p={p} f_d(0)={fd0:.1f} v_k={vk:5.0f}: f_d(z=3,2,1) = {fd_z3:.4f}/{fd_z2:.4f}/{fd_z1:.3f}; "
              f"T^2(k=5): z=3 {t3:.4f}, z=2 {t2:.4f}; S_8 = {s8:.4f}  "
              f"[forest {'OK' if row['forest_strict'] else ('loose' if row['forest_loose'] else 'FAIL')}, "
              f"S8 {'OK' if row['S8_ok'] else 'FAIL'}]")
OUT["numbers"]["scan"] = rows
both = [r for r in rows if r["forest_strict"] and r["S8_ok"]]
gal = [r for r in both if r["fd0"] >= 0.8 and r["vk"] >= 600]
check("F+S there are Lambda-triggered cells that pass the STRICT forest (5.3 keV-equivalent at z = 3 and z = 2) AND S_8 "
      "within 3 sigma of KiDS-Legacy, with f_d(0) >= 0.8 and v_k >= 600 km/s (the galaxy-depletion requirement)",
      f"{len(gal)} of {len(rows)} cells: " + "; ".join(f"p={r['p']} fd0={r['fd0']} vk={r['vk']:.0f} S8={r['S8']:.3f}" for r in gal),
      len(gal) > 0,
      "the lifetime pincer that closed kicked decay is evaded by the vacuum trigger; S_8 is the binding gate for the kick")

# ============================================================================================ verdict
banner("VERDICT")
if gal:
    best = max(gal, key=lambda r: r["S8"])
    P(f"""  THE DOOR IS OPEN AT THE LINEAR LEVEL.  A decay rate proportional to the vacuum's share, Gamma ~ Omega_Lambda(a)^p, leaves
  the Lyman-alpha forest untouched (f_d(z=3) = {best['fd_z3']:.4f}, f_d(z=2) = {best['fd_z2']:.4f}) while depleting {100*best['fd0']:.0f}% of the
  cold component by today, with S_8 = {best['S8']:.3f} at v_k = {best['vk']:.0f} km/s (KiDS-Legacy 0.815 +/- 0.016; Planck 0.834).
  The universal-lifetime pincer (tau_forest >= 41 Gyr vs tau_galaxy <= 20 Gyr) does not apply to a triggered rate.
  NOT YET SHOWN (the next gates, in the record's kill order): galaxy retention for LATE decays in MOND wells (L167 N-body,
  re-run with the triggered history); clusters (retention and the r^-1.5 residual shape at R500); CMB lensing and fsigma8 at
  z < 1; the microphysics of a vacuum-triggered rate (a mass-varying parent crossing a kinematic threshold is one candidate,
  not derived).  This is a CANDIDATE carrier that survives the two gates that killed its universal-lifetime version.""")
else:
    P("  No triggered cell passes both the strict forest and S_8 with the galaxy-depletion requirement: the door closes here too.")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
OUT["runtime_s"] = time.time() - T0
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}{'' if N_A == 420 else f'_NA{N_A}'}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {len(CH) - n_fail}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time()-T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
