#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR12 (2/4) -- IF FK1's TRIGGER FIRES IN THE STREAMS' FILAMENTS AND CLUMPS, WHAT HAPPENS TO THE LYMAN-ALPHA FOREST?

WHY.  XR12_filament_trigger.py finds that FK1's n^2 trigger (the fluid's own density, K-gated, threshold
n_t(z) = delta_t0 nbar_0 E^4) is local: it resolves every clump the infall streams carry, and at the nominal cell
(delta_t0 = 5.31, the linear cell's matter reading) every collapsed halo is above it for z <~ 6.  The record met this case
once, as L357's V1 ("the plain virialization trigger at its natural threshold ... FAILS the forest"; "the two lanes bracket
the plain trigger, and the verdict hinges on whether the carrier's small halos fire").  FK1's rate says they fire.  This
lane scores the forest for FK1's trigger with the record's own halo model, and asks what normalisation would pass.

METHOD (the record's machinery; nothing re-chosen).
  * Halo model: L357's, re-implemented line for line (CLASS linear P(k) in L319's cosmology, Sheth-Tormen mass function
    and peak-background bias, Dutton & Maccio 2014 NFW, L357's escape table for the kicked daughters, the running maximum
    in time).  FK1's trigger in a halo: the carrier's own density exceeds n_t(z); for a tracer halo that is a total density
    rho/rho_crit(z) > zeta delta_t0 Omega_m0 E(z)^2 (the carrier fraction cancels), zeta = 1 nominal.  'cleared' picture.
  * The decayed fraction that matters for large-scale power is bias-weighted, F_b(z) (L357).  L319's validated linear
    solver (its definitions executed from the committed file, as L357 does; nothing edited) is then run with
    S(t) = 1 - F_b(t).
  * TWO forest proxies.  (i) L357's gate: the TOTAL matter T^2(k = 5 h/Mpc) at z = 3 and 2 against the 5.3 keV relic
    (strict) or 0.9 (loose).  (ii) the GAS proxy: the forest traces the gas, which follows the solver's COLD component
    (baryons + unconverted carrier, one fluid), not the hot daughters.  Its 3D ratio T_c^2(k) is projected to the 1D flux
    power, P1D(k_par) ~ int_{k_par} (1 + beta k_par^2/k^2)^2 P_lin T_c^2 exp(-(k/k_F)^2) k dk (beta = 1.5, k_F = 5 h/Mpc
    as a PM-like cut, 12 h/Mpc physical), and scored with DE11's rule: worst |ratio - 1| <= 0.10 for k_par in [0.2, 2]
    h/Mpc at z = 3 and 2.
  * CALIBRATION against the record's particle mesh (C2): L366's own decay history -- its committed decayed fractions
    (0.1587 at z = 3, 0.2754 at z = 2, x~ > 5, 600 km/s) extended with a lognormal whose width is fitted to z = 2 and
    scaled by D(z), bias-weighted with the bias measured here from L388's z = 2 LCDM field -- is run through both proxies
    and compared with L366's MEASURED flux-power deviations (from its JSON: 0.0056 at z = 3, 0.0418 at z = 2).
CHECKS
  C1 CONTROL: L357's V1 cell (x_v = 30, p = 0, 'cleared', 700 km/s) reproduced EXACTLY: F_b(z = 2, 3) = 0.4583/0.4293,
     T^2(k = 5) = 0.3014/0.3670 (committed).
  C2 CALIBRATION [load-bearing claim]: on L366's own history the gas proxy reproduces the PM's measured flux deviation
     within a factor 2 at z = 2 (and stays <= 2% at z = 3), while the total-matter proxy FAILS L357's loose gate for the
     same history -- so the total-matter proxy is not a forest proxy for a kicked carrier, and the gas proxy is.
  H1 [load-bearing claim] at FK1's nominal cell every halo above M_min converts WHOLE for z <= 3 (the trigger radius lies
     beyond r_200), and the bias-weighted converted fraction is >= 0.35 by z = 3 -- and it starts earlier than the PM's
     mesh trigger (F_b(z = 4) >= 2x the PM's).
  H2 [the forest verdict, reported with its calibration] the calibrated gas-proxy deviation at z = 2 for the nominal cell
     (M_min = 1e8, the record's cut; 1e6, the FDM half-mode at 2e-19 eV) and at FK1's upper bracket (delta_t0 = 25); the
     total-matter proxy for both.
  W  [the window] zeta-scan of the threshold factor, plain and with FK1's own sqrt(sigma) modulation (the threshold of a
     halo scaled by (sigma/sigma_F)^(1/2), anchored on the flagship host): zeta_forest, the smallest factor that keeps the
     calibrated gas proxy <= 10% at z = 2 and 3.  Two flagship bounds at r_F = sqrt(G M_b/0.1 a0), z = 2.5 (M_b = 1e11,
     M_200 = 7e11 / 1e12 / 3e12, BOTH footings): the REACH, zeta_F = rho(r_F)/rho_t (the trigger still fires there); and the
     own-density CAP, zeta_cap = 0.059 rho_bar(<r_F)/rho_t (a fast trigger that reads the fluid's own density holds the cold
     carrier at or below n_t -- conversion stops below it, since re-seeding needs n_t -- so a region refilled up to the cap
     keeps S_cap = rho_t/rho_bar(<r_F): the worst case; XR12_stream_shells F2a/W2 give the full bound with the daughters).
  K  (reported, ESTIMATE) the cone-enhanced smooth web (XR12_filament_trigger E: cold sheets/filaments convert at
     ~0.21 n_t): the non-halo carrier above that threshold added to F_b.
MUTATE=1: the trigger reads a mesh-smoothed density (only halos that dominate a 0.39 Mpc/h cell fire: M_min = 1e11 Msun).
H1 must then FAIL (rc = 1): it is exactly the resolution the lane says the PM runs lacked.

A0 FOOTINGS.  The halo model and the forest carry no a0 (kernel-invisible carrier, Newtonian halos).  a0 enters only through
the flagship radius r_F: 38.6 kpc (canonical, 9.3619e-11) and 35.1 kpc (alt, 1.1279e-10); zeta_F is given on both.

SCOPE AND DISCLOSURE.  Linear forest proxies with a calibration, not a hydrodynamic flux computation; the 'cleared'
picture; halos only (the smooth web's conversion is the K estimate); no back-reaction of the conversion on halo formation
(L357's back-reaction variant lowered F_b by ~0.1-0.15 in V1).  Scratch runs of every component (the V1 reproduction, the
nominal cell's F_b and both proxies, the PM calibration) preceded the checks' wording; nothing was retuned after.
HISTORY.  First committed-form run: 5/6 (K, an estimate, failed as pre-declared and is kept).  After XR12_stream_shells'
first run showed that what the flagship retains grows with the threshold, W gained the own-density cap bound and H2 the
'cap' (refilled) picture; no threshold, proxy or calibration changed.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR12_forest_halo_model.py
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, json, math, time, io, contextlib, warnings
import numpy as np
from scipy.optimize import brentq
from scipy.special import erfc
from scipy.interpolate import RegularGridInterpolator
import scipy.fft as sfft
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR12_forest_halo_model"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR12", "part": "2/4 forest (halo model)", "mutate": MUTATE, "checks": {}, "numbers": {}}
_trap = getattr(np, "trapezoid", None) or np.trapz


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split(" ")[0]] = {"ok": ok, "claim": name, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 112); P(t); P("=" * 112)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: a mesh-smoothed trigger (M_min = 1e11 Msun): H1 must FAIL ***")

# ============================================================================================ L319's solver (definitions only)
P19 = os.path.join(DS, "L319_lambda_triggered_kicked_decay.py")
G19 = {"__name__": "l319", "__file__": P19}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(P19).read().split("# ============================================================================================ controls")[0], G19)
h, Om, OL, a_grid, N_A = G19["h"], G19["Om"], G19["OL"], G19["a_grid"], G19["N_A"]
K_H, k5, T2f, T2_53, K_ = G19["K_H"], G19["k5"], G19["T2"], G19["T2_53"], G19["K"]
LC = G19["run"](np.ones(N_A), 0.0)


def solve_parts(k, surv, vk_kms):
    """L319's solve() with the cold component returned too (the ONLY change: two return values)."""
    g = G19
    I_mat, eta, d_eta, H, H0, P_cl, f_init, j0 = g["I_mat"], g["eta"], g["d_eta"], g["H"], g["H0"], g["P_cl"], g["f_init"], g["j0"]
    Ob, Oc = g["Ob"], g["Oc"]
    v = vk_kms / g["C_KMS"]
    w = np.append(-np.diff(surv), 0.0)
    W = np.cumsum(w) - w
    fd = 1 - surv
    d0 = np.sqrt(np.interp(k, K_, P_cl[100.0]))
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
        Gm = np.zeros((N_A, N_A))
        for l in range(N_A):
            Gm[:, l] = (w[:l + 1][None, :] * j0(k * v * a_grid[None, :l + 1] * I_mat[:, l][:, None])).sum(1)
    else:
        Gm = np.cumsum(w)[None, :] * np.ones((N_A, 1))
    lower = (np.arange(N_A)[None, :] < np.arange(N_A)[:, None]).astype(float)
    Dji = a_grid[None, :] * I_mat
    A = np.zeros((2 * N_A, 2 * N_A)); b = np.zeros(2 * N_A)
    A[:N_A, :N_A] = np.eye(N_A) - I_mat * src_c[None, :]
    A[:N_A, N_A:] = -I_mat * src_d[None, :]
    b[:N_A] = d0 - th0 * Dm0
    Cmat = w[None, :] * J * lower
    Vmat = (w[None, :] * J * lower * Dji) @ Dm
    A[N_A:, :N_A] = -(Cmat + Vmat) - I_mat * Gm * src_c[None, :]
    A[N_A:, N_A:] = np.diag(W) - I_mat * Gm * src_d[None, :]
    for j in np.where(W <= 0)[0]:
        A[N_A + j, :] = 0.0; A[N_A + j, N_A + j] = 1.0; A[N_A + j, j] = -1.0
    sol = np.linalg.solve(A, b)
    dc, dd = sol[:N_A], sol[N_A:]
    return dc, (rho_cold * dc + rho_d * dd) / (rho_cold + rho_d)


def run_parts(surv, vk):
    o = [solve_parts(k, surv, vk) for k in K_]
    return np.array([x[0] for x in o]), np.array([x[1] for x in o])


DC0, TOT0 = run_parts(np.ones(N_A), 0.0)
JZ = {z: G19["idx_z"](z) for z in (2.0, 3.0)}
KF_MASK = (K_H >= 0.2) & (K_H <= 2.0)
_KK = np.geomspace(0.02, 30.0, 2000)
_LPZ = {z: np.interp(np.log(_KK), np.log(K_H), np.log(G19["P_cl"][z])) for z in (2.0, 3.0)}
KPAR = np.array([0.2, 0.3, 0.5, 0.7, 1.0, 1.4, 2.0])


def p1d_ratio(t2c, z, kF, beta=1.5):
    t2 = np.interp(np.log(_KK), np.log(K_H), t2c); out = []
    for kp in KPAR:
        m = _KK >= kp
        wgt = (1 + beta * kp ** 2 / _KK[m] ** 2) ** 2 * np.exp(_LPZ[z][m]) * np.exp(-(_KK[m] / kF) ** 2) * _KK[m]
        out.append(float(_trap(wgt * t2[m], _KK[m]) / _trap(wgt, _KK[m])))
    return np.array(out)


_CACHE = {}


def proxies(S, vk):
    key = (np.round(S, 9).tobytes(), float(vk))
    if key not in _CACHE:
        dcm, tot = run_parts(S, vk); r = {}
        for z in (3.0, 2.0):
            j = JZ[z]
            t2t = tot[:, j] ** 2 / TOT0[:, j] ** 2; t2c = dcm[:, j] ** 2 / DC0[:, j] ** 2
            c5 = p1d_ratio(t2c, z, 5.0)
            r[str(z)] = dict(T2tot_k5=float(t2t[k5]), T2cold_k5=float(t2c[k5]), cold3d_dev=float(np.max(np.abs(t2c[KF_MASK] - 1))),
                             p1d_kF5=float(np.max(np.abs(c5 - 1))), p1d_kF5_curve=c5.tolist(),
                             p1d_kF12=float(np.max(np.abs(p1d_ratio(t2c, z, 12.0) - 1))))
        _CACHE[key] = r
    return _CACHE[key]


P(f"  L319 solver loaded (N_A = {N_A}); LCDM reference reproduced by the two-output copy: "
  f"max |total - L319 run| = {float(np.max(np.abs(TOT0 - LC))):.1e}   [{time.time() - T0:.0f}s]")

# ============================================================================================ L357's halo model (line for line)
from classy import Class
cls = Class()
cls.set({"h": h, "omega_b": 0.02237, "omega_cdm": 0.1200, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046,
         "N_ncdm": 0, "YHe": 0.2454, "output": "mPk", "P_k_max_h/Mpc": 200, "z_max_pk": 12})
cls.compute()
KH = np.geomspace(1e-4, 190, 2500); P0 = np.array([cls.pk_lin(k * h, 0.0) for k in KH]) * h ** 3
_DGC = {}


def DG(z):
    if z not in _DGC: _DGC[z] = cls.scale_independent_growth_factor(z)
    return _DGC[z]


LGM = np.linspace(5.0, 16.0, 221); MH = 10 ** LGM                             # Msun/h
RHOM_H = 2.775e11 * Om
RH = (3 * MH / (4 * np.pi * RHOM_H)) ** (1 / 3)
_X = np.outer(RH, KH); _WT = 3 * (np.sin(_X) - _X * np.cos(_X)) / _X ** 3
SIG0 = np.sqrt(_trap(KH ** 2 * P0 * _WT ** 2, KH, axis=1) / (2 * np.pi ** 2))
del _X, _WT
AST, QST, PST, DC = 0.3222, 0.707, 0.3, 1.686
f_st = lambda nu: AST * np.sqrt(2 * QST / np.pi) * (1 + (QST * nu ** 2) ** (-PST)) * np.exp(-QST * nu ** 2 / 2)
b_st = lambda nu: 1 + (QST * nu ** 2 - 1) / DC + 2 * PST / (DC * (1 + (QST * nu ** 2) ** PST))


def mfn(x):
    x = np.asarray(x, dtype=float)
    return np.where(x < 1e-4, x * x / 2 - 2 * x ** 3 / 3 + 3 * x ** 4 / 4,
                    np.log1p(np.maximum(x, 1e-4)) - np.maximum(x, 1e-4) / (1 + np.maximum(x, 1e-4)))


GK = 4.30091727e-6
RHOC0_KPC = 277.5 * h ** 2
Ez2 = lambda z: Om * (1 + z) ** 3 + OL
Om_z = lambda z: Om * (1 + z) ** 3 / Ez2(z)
OL_z = lambda z: OL / Ez2(z)


def c_dm14(Mh, z):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * np.log10(Mh / 1e12))


def y_of(ratio):
    t = np.log(np.maximum(np.minimum(ratio, ratio ** (1 / 3)), 1e-12))
    lr = np.log(ratio)
    for _ in range(60):
        e = np.exp(t); g = t + 2 * np.log1p(e) - lr; t = t - g / (1 + 2 * e / (1 + e))
    return np.exp(t)


_rng = np.random.default_rng(11); _g = _rng.standard_normal((6000, 3)); _n = _rng.standard_normal((6000, 3))
_n /= np.linalg.norm(_n, axis=1)[:, None]
UG = np.linspace(0.0, 6.0, 121); SGR = np.linspace(0.02, 1.2, 60)
_PE = np.array([[np.mean(np.sum((s * _g + u * _n) ** 2, axis=1) > 1.0) for s in SGR] for u in UG])
PESC = RegularGridInterpolator((UG, SGR), _PE, bounds_error=False, fill_value=None)


def V200_of(z):
    M200 = MH / h; r200 = (3 * M200 / (4 * np.pi * 200 * RHOC0_KPC * Ez2(z))) ** (1 / 3)
    return np.sqrt(GK * M200 / r200)


def trig(z, rhv, picture="cleared"):
    """L357's trig(), with the threshold rhv (rho_crit(z) units, scalar or per-mass array) supplied."""
    cs = c_dm14(MH, z); dch = 200 / 3 * cs ** 3 / mfn(cs)
    y = np.minimum(y_of(dch / rhv), cs)
    m_in = mfn(y) / mfn(cs)
    m = m_in if picture == "cleared" else np.maximum(0.0, m_in - rhv * (y / cs) ** 3 / 200)
    return m, y, cs, dch


def esc(z, vk, y, cs, dch, picture="cleared", rhv=0.0):
    """L357's esc()."""
    if vk <= 0: return np.zeros_like(y)
    M200 = MH / h; r200 = (3 * M200 / (4 * np.pi * 200 * RHOC0_KPC * Ez2(z))) ** (1 / 3); V200 = np.sqrt(GK * M200 / r200)
    s = np.geomspace(1e-3, 1.0, 50)[None, :]; yy = y[:, None] * s; xx = yy / cs[:, None]
    phi = -np.log1p(yy) / (xx * mfn(cs)[:, None]) + (np.log1p(cs) / mfn(cs))[:, None] - 1.0
    vesc = V200[:, None] * np.sqrt(np.maximum(-2 * phi, 1e-12))
    vc = V200[:, None] * np.sqrt(mfn(yy) / (mfn(cs)[:, None] * xx))
    pe = PESC(np.stack([np.clip(vk / vesc, 0, 6.0), np.clip(vc / np.sqrt(2) / vesc, 0.02, 1.2)], axis=-1))
    rho = dch[:, None] / (yy * (1 + yy) ** 2)
    rhv_ = np.broadcast_to(np.asarray(rhv, float), y.shape)[:, None] if np.ndim(rhv) else rhv
    wgt = (rho if picture == "cleared" else np.maximum(rho - rhv_, 0.0)) * yy ** 3
    den = _trap(wgt, np.log(yy), axis=1)
    return np.where(den > 0, _trap(wgt * pe, np.log(yy), axis=1) / np.maximum(den, 1e-300), 1.0)


def Fb(z, rhv, vk, m_min, weight="bias", picture="cleared"):
    s = SIG0 * DG(z); nu = DC / s
    w = f_st(nu) * np.abs(np.gradient(nu, np.log(MH)))
    m, y, cs, dch = trig(z, rhv, picture)
    fe = esc(z, vk, y, cs, dch, picture, rhv) if vk > 0 else 1.0
    sel = MH >= m_min * h
    wb = w * (b_st(nu) if weight == "bias" else 1.0)
    return float(_trap((wb * m * fe)[sel], np.log(MH)[sel]))


ZG = np.array([0, 0.1, 0.25, 0.4, 0.6, 0.8, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4, 5, 6, 8, 10, 12, 15, 20, 30])
for _z in list(ZG): DG(float(_z))
ZA = 1 / a_grid - 1


def to_S(Fz):
    Fz = np.where(np.asarray(Fz) < 1e-10, 0.0, np.asarray(Fz))
    Fc = np.maximum.accumulate(Fz[::-1])[::-1]
    return 1 - np.interp(ZA, ZG, Fc, right=0.0), Fc


RHO_SIG_F = None                                                                  # the flagship host's sigma (set below)


def rhv_fk1(z, dt0, zeta, sqrt_sigma=False):
    base = zeta * dt0 * Om * Ez2(z)                                               # rho_crit(z) units, carrier fraction cancels
    if not sqrt_sigma:
        return base
    return base * np.sqrt(V200_of(z) / RHO_SIG_F)                                 # FK1's '~ sqrt(sigma) in the threshold'


def fk1_history(dt0=2.5 * 2 / 3 / 0.3138, zeta=1.0, vk=600.0, m_min=1e8, sqrt_sigma=False, weight="bias", picture="cleared"):
    Fz = [Fb(z, rhv_fk1(z, dt0, zeta, sqrt_sigma), vk, m_min, weight, picture) for z in ZG]
    return to_S(Fz)


DT0_LIN = (2.0 / 3.0) * 2.5 / 0.3138
P(f"  halo model ready: CLASS sigma8 = {cls.sigma8():.4f}; FK1 nominal delta_t0 = {DT0_LIN:.3f}   [{time.time() - T0:.0f}s]")

# ============================================================================================ C1 L357's V1 reproduced
banner("C1  CONTROL: L357's V1 cell (x_v = 30, p = 0, 'cleared', 700 km/s, M_min = 1e8) reproduced exactly")
R357 = json.load(open(os.path.join(DS, "L357_virialization_triggered_carrier_results.json")))["numbers"]["V1"]["30/700/cleared"]
S_v1, Fc_v1 = to_S([Fb(z, Om_z(z) + 2 / 3 * 30.0, 700.0, 1e8) for z in ZG])
R_v1 = G19["run"](S_v1, 700.0)
v1 = dict(Fb_z2=float(np.interp(2, ZG, Fc_v1)), Fb_z3=float(np.interp(3, ZG, Fc_v1)),
          t2=float(T2f(R_v1, LC, 2.0)[k5]), t3=float(T2f(R_v1, LC, 3.0)[k5]))
dv1 = max(abs(v1[k_] - R357[k_]) for k_ in v1)
pv1 = proxies(S_v1, 700.0)
P(f"    F_b(z=2,3) = {v1['Fb_z2']:.6f}/{v1['Fb_z3']:.6f} (L357 {R357['Fb_z2']:.6f}/{R357['Fb_z3']:.6f}); T^2(k=5) z=2,3 = "
  f"{v1['t2']:.6f}/{v1['t3']:.6f} (L357 {R357['t2']:.6f}/{R357['t3']:.6f})")
P(f"    the same cell on the gas proxy: T_c^2(k=5) z=3,2 = {pv1['3.0']['T2cold_k5']:.3f}/{pv1['2.0']['T2cold_k5']:.3f}; 1D (k_F = 5) worst "
  f"{pv1['3.0']['p1d_kF5']:.3f}/{pv1['2.0']['p1d_kF5']:.3f}")
OUT["numbers"]["C1"] = dict(reproduced=v1, committed={k_: R357[k_] for k_ in v1}, max_dev=dv1, gas_proxy=pv1)
check("C1 CONTROL: L357's V1 cell reproduced exactly by the re-implemented halo model and L319's solver",
      f"max |dev| = {dv1:.1e} over F_b(z=2,3) and T^2(k=5, z=2,3)", dv1 < 1e-9)

# ============================================================================================ C2 calibration on the PM
banner("C2  CALIBRATION: L366's own decay history through both proxies, against its MEASURED flux power")
R366 = json.load(open(os.path.join(DS, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]["runs"]
meas = {}
for z in ("3.0", "2.0"):
    kp = np.array(R366["lcdm"][z]["kpar"]); rr = np.array(R366["x5_v600"][z]["p1d"]) / np.array(R366["lcdm"][z]["p1d"])
    msk = (kp >= 0.2) & (kp <= 2.0); meas[z] = float(np.max(np.abs(rr[msk] - 1)))
shape_pm = {}
for z in ("3.0", "2.0"):
    kp = np.array(R366["lcdm"][z]["kpar"]); rr = np.array(R366["x5_v600"][z]["p1d"]) / np.array(R366["lcdm"][z]["p1d"])
    shape_pm[z] = [float(np.interp(q, kp, rr)) for q in KPAR]
fd3, fd2 = R366["x5_v600"]["3.0"]["decayed"], R366["x5_v600"]["2.0"]["decayed"]
thr_pm = lambda z: 1 + 5.0 / (1.5 * Om_z(z))                                     # L365/L366's x~ > 5 on the mesh
Fln = lambda sig, t: 0.5 * erfc((math.log(t) - sig ** 2 / 2) / (math.sqrt(2) * sig))
sig2 = brentq(lambda s: Fln(s, thr_pm(2.0)) - fd2, 0.2, 4.0)
f3_pred = Fln(sig2 * DG(3.0) / DG(2.0), thr_pm(3.0))
# the bias of the mesh mass above the PM trigger, measured on L388's z = 2 LCDM fields (3 boxes)
FD = os.path.join(DS, "_L388_fields"); bias = []
for sd in ("7", "17", "29"):
    rho = np.load(os.path.join(FD, f"s{sd}_lcdm_z2_rho.npy"))                      # float32 on disk
    x = np.where(rho > thr_pm(2.0), rho, np.float32(0.0)); x = (x / x.mean() - 1.0).astype(np.float32)
    dk_ = sfft.rfftn(rho - np.float32(1.0), workers=1); xk = sfft.rfftn(x, workers=1); del x, rho
    kx = (2 * np.pi * np.fft.fftfreq(256, d=100.0 / 256)).astype(np.float32); kz = (2 * np.pi * np.fft.rfftfreq(256, d=100.0 / 256)).astype(np.float32)
    KK = np.sqrt(kx[:, None, None] ** 2 + kx[None, :, None] ** 2 + kz[None, None, :] ** 2)
    msk = (KK > 0) & (KK < 0.25)
    bias.append(float(np.sum((xk * np.conj(dk_)).real[msk]) / np.sum((np.abs(dk_) ** 2)[msk])))
    del dk_, xk, KK, msk
b_pm = float(np.mean(bias))
Fpm = [min(b_pm * (Fln(sig2 * DG(z) / DG(2.0), thr_pm(z)) if z > 2.0 else fd2), 0.95) for z in ZG]
S_pm, Fc_pm = to_S(Fpm)
ppm = proxies(S_pm, 600.0)
_dcm, _ = run_parts(S_pm, 600.0)
shape_px = {z: p1d_ratio(_dcm[:, JZ[float(z)]] ** 2 / DC0[:, JZ[float(z)]] ** 2, float(z), 5.0).tolist() for z in ("3.0", "2.0")}
cal = {z: ppm[z]["p1d_kF5"] / meas[z] for z in ("3.0", "2.0")}
P(f"    L366 measured worst |P1D/P1D_LCDM - 1| (k_par 0.2-2): z = 3 {meas['3.0']:.4f}, z = 2 {meas['2.0']:.4f}")
P(f"    history: lognormal width at z = 2 fitted to f_d = {fd2:.4f} -> sigma_ln = {sig2:.3f}; predicts f_d(z = 3) = {f3_pred:.4f} "
  f"(L366 {fd3:.4f}); bias of the triggered mesh mass (L388 z = 2, k < 0.25 h/Mpc) = {', '.join(f'{b:.2f}' for b in bias)}")
P(f"    bias-weighted F_b: " + ", ".join(f"z={z:g}: {f:.3f}" for z, f in zip(ZG, Fc_pm) if 2 <= z <= 6))
P(f"    total-matter proxy T^2(k=5): z = 3 {ppm['3.0']['T2tot_k5']:.3f}, z = 2 {ppm['2.0']['T2tot_k5']:.3f}   (L357's loose gate needs >= 0.9)")
P(f"    gas proxy, 1D worst deviation: k_F = 5: z = 3 {ppm['3.0']['p1d_kF5']:.4f}, z = 2 {ppm['2.0']['p1d_kF5']:.4f};  k_F = 12: "
  f"{ppm['3.0']['p1d_kF12']:.4f}, {ppm['2.0']['p1d_kF12']:.4f};  3D cold (0.2-2): {ppm['3.0']['cold3d_dev']:.4f}, {ppm['2.0']['cold3d_dev']:.4f}")
P(f"    calibration factor (proxy / PM measured, k_F = 5): z = 3 {cal['3.0']:.2f}, z = 2 {cal['2.0']:.2f}")
for z in ("3.0", "2.0"):
    P(f"    shape at z = {z}: k_par = " + " ".join(f"{q:4.2f}" for q in KPAR) + "\n      PM measured ratio:   "
      + " ".join(f"{v:.4f}" for v in shape_pm[z]) + "\n      gas proxy ratio:     " + " ".join(f"{v:.4f}" for v in shape_px[z]))
P("    -> the proxy matches the PM's worst |deviation| and its large-scale end; at k_par >= 0.5 the PM's flux power RISES "
  "(nonlinear flux response) where the linear proxy falls, so the proxy is a magnitude calibration with a ~2x systematic")
KCAL = cal["2.0"]
OUT["numbers"]["C2"] = dict(measured=meas, shape_pm=shape_pm, shape_proxy=shape_px, k_par=KPAR.tolist(), sigma_ln_z2=sig2, f_d3_pred=f3_pred, f_d3_L366=fd3, bias=bias, b_pm=b_pm,
                            Fb=dict(zip(map(float, ZG), map(float, Fc_pm))), proxies=ppm, calibration=cal)
check("C2 CALIBRATION: on L366's own history the gas proxy reproduces the PM's measured flux deviation within a factor 2 at "
      "z = 2 (<= 2% at z = 3), while the total-matter proxy FAILS L357's loose gate for the same, passing, construction",
      f"gas proxy/PM at z = 2: {cal['2.0']:.2f} ({ppm['2.0']['p1d_kF5']:.4f} vs {meas['2.0']:.4f}); z = 3: {ppm['3.0']['p1d_kF5']:.4f}; "
      f"total-matter T^2(k=5) {ppm['2.0']['T2tot_k5']:.3f}/{ppm['3.0']['T2tot_k5']:.3f}",
      0.5 <= cal["2.0"] <= 2.0 and ppm["3.0"]["p1d_kF5"] <= 0.02 and min(ppm["2.0"]["T2tot_k5"], ppm["3.0"]["T2tot_k5"]) < 0.9,
      "the forest sees the gas, which follows the cold component; the hot daughters' missing clustering is in the total "
      "matter T^2 but not in the absorbers.  L357's V1 ('destroys the forest') was scored on the total matter; on the gas "
      "proxy V1 reads " + f"{pv1['2.0']['p1d_kF5']:.3f} at z = 2 -- a fail on DE11's rule, but by far less than T^2 = 0.30 says")

# ============================================================================================ H1 FK1's nominal cell
banner("H1  FK1's TRIGGER, LOCAL, AT THE NOMINAL CELL (delta_t0 = 5.31): which halos convert, when, and how much")
M_MIN_MAIN = 1e11 if MUTATE else 1e8
zw = {}
for zt in (1.0, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0):
    m_, y_, cs_, _ = trig(zt, rhv_fk1(zt, DT0_LIN, 1.0))
    sel = MH >= M_MIN_MAIN * h
    zw[str(zt)] = float(np.mean((y_ >= cs_ - 1e-12)[sel]))
P("    fraction of halos (by number of mass bins >= M_min) converting WHOLE (trigger radius beyond r_200): "
  + ", ".join(f"z={k_}: {v:.2f}" for k_, v in zw.items()))
S_nom, Fc_nom = fk1_history(m_min=M_MIN_MAIN)
_, Fu_nom = fk1_history(m_min=M_MIN_MAIN, weight="plain")
Fpm_z4 = float(np.interp(4.0, ZG, Fc_pm)); Fnom_z4 = float(np.interp(4.0, ZG, Fc_nom))
P("    FK1 nominal, bias-weighted F_b: " + ", ".join(f"z={z:g}: {f:.3f}" for z, f in zip(ZG, Fc_nom) if z <= 8))
P("    FK1 nominal, unweighted F_u:    " + ", ".join(f"z={z:g}: {f:.3f}" for z, f in zip(ZG, Fu_nom) if z <= 8))
P(f"    against the PM's mesh trigger (C2): F_b(z = 3) {float(np.interp(3.0, ZG, Fc_nom)):.3f} vs {float(np.interp(3.0, ZG, Fc_pm)):.3f}; "
  f"F_b(z = 4) {Fnom_z4:.3f} vs {Fpm_z4:.3f} ({Fnom_z4 / max(Fpm_z4, 1e-9):.1f}x); F_b(z = 5) {float(np.interp(5.0, ZG, Fc_nom)):.3f} vs "
  f"{float(np.interp(5.0, ZG, Fc_pm)):.3f}")
_, Fu_up25 = fk1_history(dt0=25.0, m_min=M_MIN_MAIN, weight="plain")
OUT["numbers"]["H1"] = dict(M_min=M_MIN_MAIN, whole_fraction=zw, Fb=dict(zip(map(float, ZG), map(float, Fc_nom))),
                            Fu=dict(zip(map(float, ZG), map(float, Fu_nom))), Fu_upper25=dict(zip(map(float, ZG), map(float, Fu_up25))))
check("H1 at FK1's nominal cell every halo above M_min converts WHOLE for z <= 3, the bias-weighted converted fraction is "
      ">= 0.35 by z = 3, and it starts earlier than the PM's mesh trigger (F_b(z = 4) >= 2x)",
      f"whole at z = 1/2/3: {zw['1.0']:.2f}/{zw['2.0']:.2f}/{zw['3.0']:.2f}; F_b(3) = {float(np.interp(3.0, ZG, Fc_nom)):.3f}; "
      f"F_b(4) = {Fnom_z4:.3f} vs PM {Fpm_z4:.3f}",
      min(zw["1.0"], zw["2.0"], zw["3.0"]) >= 0.999 and float(np.interp(3.0, ZG, Fc_nom)) >= 0.35 and Fnom_z4 >= 2 * Fpm_z4,
      "the streams' clumps convert as they collapse, from z ~ 6: the forest's dark scaffolding is kicked earlier and more "
      "uniformly than the PM runs model")

# ============================================================================================ H2 the forest verdict
banner("H2  THE FOREST: FK1's cell on both proxies (gas proxy calibrated by C2's factor)")
H2 = {}
cases = {"nominal 5.31, M_min 1e8, 600": dict(), "nominal 5.31, M_min 1e6 (FDM floor), 600": dict(m_min=1e6),
         "nominal 5.31, M_min 1e8, 575": dict(vk=575.0), "nominal 5.31, M_min 1e8, 650": dict(vk=650.0),
         "upper 25, M_min 1e8, 600": dict(dt0=25.0), "upper 25, M_min 1e6, 600": dict(dt0=25.0, m_min=1e6),
         "nominal 5.31, M_min 1e8, 600, 'cap' (refilled)": dict(picture="cap")}
for lab, kw in cases.items():
    kw2 = dict(kw)
    if MUTATE: kw2["m_min"] = max(kw2.get("m_min", 1e8), 1e11)
    S_, Fc_ = fk1_history(**kw2)
    pr = proxies(S_, kw2.get("vk", 600.0))
    cald = {z: pr[z]["p1d_kF5"] / KCAL for z in ("3.0", "2.0")}
    H2[lab] = dict(Fb2=float(np.interp(2.0, ZG, Fc_)), Fb3=float(np.interp(3.0, ZG, Fc_)), proxies=pr, calibrated=cald)
    P(f"    {lab:46s}: F_b(2,3) {H2[lab]['Fb2']:.3f}/{H2[lab]['Fb3']:.3f} | total T^2(k5) z3,z2 {pr['3.0']['T2tot_k5']:.3f}/"
      f"{pr['2.0']['T2tot_k5']:.3f} | gas 1D raw kF5 {pr['3.0']['p1d_kF5']:.3f}/{pr['2.0']['p1d_kF5']:.3f}, kF12 "
      f"{pr['3.0']['p1d_kF12']:.3f}/{pr['2.0']['p1d_kF12']:.3f} | CALIBRATED {cald['3.0']:.3f}/{cald['2.0']:.3f}   [{time.time() - T0:.0f}s]")
OUT["numbers"]["H2"] = H2
nom, upp, fdm = H2["nominal 5.31, M_min 1e8, 600"], H2["upper 25, M_min 1e8, 600"], H2["nominal 5.31, M_min 1e6 (FDM floor), 600"]
cap_ = H2["nominal 5.31, M_min 1e8, 600, 'cap' (refilled)"]
P("    the z = 2 curves, calibrated deficit 1 - P1D ratio (k_par = " + " ".join(f"{q:g}" for q in KPAR) + " h/Mpc); C2 validated the proxy "
  "against the PM at k_par <= 0.3-0.5, where both fall, and NOT at k_par >= 1, where the PM's flux power rose:")
for lab in ("nominal 5.31, M_min 1e8, 600", "nominal 5.31, M_min 1e8, 600, 'cap' (refilled)", "nominal 5.31, M_min 1e6 (FDM floor), 600",
            "upper 25, M_min 1e8, 600"):
    cv = [(1 - v) / KCAL for v in H2[lab]["proxies"]["2.0"]["p1d_kF5_curve"]]
    H2[lab]["calibrated_curve_z2"] = cv
    P(f"      {lab:46s}: " + " ".join(f"{v:.3f}" for v in cv))
val_nom = max(nom["calibrated_curve_z2"][:3])
ratio_pm = nom["proxies"]["2.0"]["p1d_kF5"] / ppm["2.0"]["p1d_kF5"]
P(f"    the nominal cell's gas deficit at z = 2 is {ratio_pm:.1f}x the PM mesh trigger's (the record's passing 4%)")
check("H2 (the forest verdict) on the calibrated gas proxy FK1's nominal cell sits AT DE11's 10% line at z = 2 (8-20%), "
      "above it at the FDM floor, at >= 2x the PM's own deficit; FK1's upper bracket (25) passes (<= 10%); the total-matter "
      "proxy fails L357's loose gate at both brackets",
      f"calibrated z = 2: nominal {nom['calibrated']['2.0']:.3f} ('cap' {cap_['calibrated']['2.0']:.3f}; {val_nom:.3f} at k_par <= 0.5), FDM floor "
      f"{fdm['calibrated']['2.0']:.3f}, upper {upp['calibrated']['2.0']:.3f} "
      f"(z = 3: {nom['calibrated']['3.0']:.3f}/{fdm['calibrated']['3.0']:.3f}/{upp['calibrated']['3.0']:.3f}); nominal/PM {ratio_pm:.1f}x; "
      f"total T^2(k5) z = 2: {nom['proxies']['2.0']['T2tot_k5']:.2f} / {upp['proxies']['2.0']['T2tot_k5']:.2f}",
      0.08 <= nom["calibrated"]["2.0"] <= 0.20 and fdm["calibrated"]["2.0"] > 0.10 and ratio_pm >= 2.0
      and upp["calibrated"]["2.0"] <= 0.10 and upp["calibrated"]["3.0"] <= 0.10
      and nom["proxies"]["2.0"]["T2tot_k5"] < 0.9 and upp["proxies"]["2.0"]["T2tot_k5"] < 0.9,
      "the forest neither clearly passes nor clearly fails the nominal cell: it constrains the normalisation (W).  The PM's "
      "4% pass does NOT carry over to FK1's local trigger")

# ============================================================================================ W the window in zeta
banner("W   THE WINDOW: threshold factor zeta (delta_t0 = 5.31 zeta) -- forest from below, flagship from above")
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
GSI, MSUN, KPC_M = 6.674e-11, 1.989e30, 3.0857e19
rF = {f_: math.sqrt(GSI * 1e11 * MSUN / (0.1 * a0)) / KPC_M for f_, a0 in A0.items()}
zF = 2.5
Mh_F = {"7e11": 7e11, "1e12": 1e12, "3e12": 3e12}            # 7e11: the smallest host whose f_b M holds M_b = 1e11


def nfw_rho_over_crit(M200, z, r):
    c = float(c_dm14(M200 * h, z)); r200 = (3 * M200 / (4 * math.pi * 200 * RHOC0_KPC * Ez2(z))) ** (1 / 3)
    x = r / (r200 / c); dch = 200 / 3 * c ** 3 / float(mfn(c))
    return dch / (x * (1 + x) ** 2), c, r200, math.sqrt(GK * M200 / r200)


zetaF = {}
for mk, M_ in Mh_F.items():
    for f_, r_ in rF.items():
        rho_r, c_, r200_, v200_ = nfw_rho_over_crit(M_, zF, r_)
        xx_ = r_ / (r200_ / c_); dch_ = 200 / 3 * c_ ** 3 / float(mfn(c_))
        rbar = 3 * dch_ * float(mfn(xx_)) / xx_ ** 3                               # mean enclosed density / rho_crit
        zetaF[f"{mk}/{f_}"] = dict(r_F_kpc=r_, rho_over_crit=rho_r, zeta_F=rho_r / rhv_fk1(zF, DT0_LIN, 1.0), c=c_, r200=r200_,
                                   rho_bar_enclosed=rbar, zeta_cap=0.059 * rbar / rhv_fk1(zF, DT0_LIN, 1.0))   # S_cap <= 0.059
_, _, _, v200F = nfw_rho_over_crit(1e12, zF, rF["canonical"])
RHO_SIG_F = v200F                                                                  # anchor of the sqrt(sigma) variant
P("    flagship: r_F = " + ", ".join(f"{f_} {r_:.1f} kpc" for f_, r_ in rF.items()) + f" (M_b = 1e11, z = {zF}); zeta_F = rho_NFW(r_F)/rho_t:")
for k_, v in zetaF.items():
    P(f"      host M_200 = {k_:16s}: c = {v['c']:.2f}, r_200 = {v['r200']:.0f} kpc, rho(r_F) = {v['rho_over_crit']:.0f} rho_crit -> zeta_F = "
      f"{v['zeta_F']:.1f};  rho_bar(<r_F) = {v['rho_bar_enclosed']:.0f} rho_crit -> cap bound zeta <= {v['zeta_cap']:.2f}")
zF_min = min(v["zeta_F"] for v in zetaF.values())
zFl = {k_: v["zeta_cap"] for k_, v in zetaF.items()}
P("    the own-density CAP (a fast own-density trigger holds the cold carrier at or below n_t; a region refilled to the cap keeps "
  "S_cap = rho_t/rho_bar(<r_F)): the worst case S_cap <= 0.059 needs zeta <= " + ", ".join(f"{k_} {v:.2f}" for k_, v in zFl.items()))
ZETAS = (1.0, 1.5, 2.0, 3.0, 25.0 / DT0_LIN, 8.0)
Wrow = {}
for var in ("plain", "sqrt_sigma"):
    for zt in ZETAS:
        S_, Fc_ = fk1_history(zeta=zt, sqrt_sigma=(var == "sqrt_sigma"), m_min=M_MIN_MAIN)
        pr = proxies(S_, 600.0)
        cd = max(pr[z]["p1d_kF5"] for z in ("3.0", "2.0")) / KCAL
        Wrow[f"{var}/{zt:g}"] = dict(zeta=zt, Fb2=float(np.interp(2.0, ZG, Fc_)), calibrated_worst=cd,
                                     T2tot_k5=min(pr[z]["T2tot_k5"] for z in ("3.0", "2.0")))
        P(f"    {var:10s} zeta = {zt:5.3g} (delta_t0 = {DT0_LIN * zt:6.1f}): F_b(2) {Wrow[f'{var}/{zt:g}']['Fb2']:.3f}, calibrated gas worst "
          f"{cd:.3f}, total T^2(k5) {Wrow[f'{var}/{zt:g}']['T2tot_k5']:.3f}   [{time.time() - T0:.0f}s]")


def zeta_cross(var, level=0.10):
    xs = [Wrow[f"{var}/{zt:g}"]["zeta"] for zt in ZETAS]; ys = [Wrow[f"{var}/{zt:g}"]["calibrated_worst"] for zt in ZETAS]
    if ys[0] <= level: return xs[0]
    for i in range(len(xs) - 1):
        if ys[i] > level >= ys[i + 1]:
            return float(math.exp(np.interp(level, [ys[i + 1], ys[i]], [math.log(xs[i + 1]), math.log(xs[i])])))
    return float("inf")


zf = {var: zeta_cross(var) for var in ("plain", "sqrt_sigma")}
fl_can = {k_: v for k_, v in zFl.items() if k_.endswith("canonical")}; fl_alt = {k_: v for k_, v in zFl.items() if k_.endswith("alt")}
win = {}
for var in zf:
    win[var] = dict(zeta_forest=zf[var], zeta_reach_min=zF_min, window_reach=bool(zf[var] < zF_min),
                    zeta_cap={k_: v for k_, v in zFl.items()},
                    window_cap_fiducial_1e12={f_: bool(zf[var] < zFl[f"1e12/{f_}"]) for f_ in ("canonical", "alt")},
                    window_cap_all_hosts={f_: bool(zf[var] < min(v for k_, v in zFl.items() if k_.endswith(f_))) for f_ in ("canonical", "alt")})
    P(f"    {var:10s}: forest needs zeta >= {zf[var]:.2f};  reach bound zeta <= {zF_min:.1f} -> "
      + ("window" if win[var]["window_reach"] else "none") + ";  CAP bound (worst case): 1e12 host zeta <= "
      + f"{zFl['1e12/canonical']:.2f} (canonical) / {zFl['1e12/alt']:.2f} (alt) -> "
      + ", ".join(f"{f_} {'OPEN' if o else 'CLOSED'}" for f_, o in win[var]["window_cap_fiducial_1e12"].items())
      + f"  [delta_t0 {DT0_LIN * zf[var]:.1f}-{DT0_LIN * zFl['1e12/canonical']:.1f} canonical]")
OUT["numbers"]["W"] = dict(r_F=rF, zeta_F=zetaF, scan=Wrow, window=win)
check("W (reported; the cap bound was added after XR12_stream_shells' first run) with the trigger's REACH as the flagship bound "
      "a window exists; with the own-density CAP as the worst-case bound the window is the band [zeta_forest, zeta_cap] -- "
      "reported open or closed per variant and footing",
      "; ".join(f"{var}: forest >= {w_['zeta_forest']:.2f}, cap(1e12) <= {zFl['1e12/canonical']:.2f}/{zFl['1e12/alt']:.2f}, "
                f"open(can/alt) = {w_['window_cap_fiducial_1e12']['canonical']}/{w_['window_cap_fiducial_1e12']['alt']}"
                for var, w_ in win.items()),
      all(w_["window_reach"] for w_ in win.values()),
      "the trigger's reach is not what bounds FK1's normalisation from above: what the flagship retains is -- the capped cold "
      "carrier plus the daughters of conversions near r_F, both growing with the threshold.  A band, not a wide window; its "
      "upper end from the resolved shells is XR12_stream_shells W2.  On L357's total-matter gate there is no window at any "
      "zeta scanned", load_bearing=False)

# ============================================================================================ K the cone-enhanced smooth web
banner("K   ESTIMATE: the cone-enhanced smooth web (cold sheets/filaments convert at ~0.21 n_t, XR12_filament_trigger E)")
ZETA_CONE = 0.21
Kr = {}
for lab, dt0 in (("nominal 5.31", DT0_LIN), ("upper 25", 25.0)):
    Fz = []
    for z in ZG:
        fb_h = Fb(z, rhv_fk1(z, dt0, 1.0), 600.0, M_MIN_MAIN)
        fu_h = Fb(z, rhv_fk1(z, dt0, 1.0), 600.0, M_MIN_MAIN, weight="plain")
        t_cone = ZETA_CONE * dt0 * (Ez2(z) ** 2) / (1 + z) ** 3                 # rho/rho_bar at the cone threshold
        f_s = Fln(sig2 * DG(z) / DG(2.0), max(t_cone, 1.0001)) if z <= 6 else 0.0
        Fz.append(min(fb_h + b_pm * max(1.0 - fu_h, 0.0) * f_s, 0.95))
    S_, Fc_ = to_S(Fz)
    pr = proxies(S_, 600.0)
    Kr[lab] = dict(Fb2=float(np.interp(2.0, ZG, Fc_)), calibrated=max(pr[z]["p1d_kF5"] for z in ("3.0", "2.0")) / KCAL)
    P(f"    {lab:14s}: F_b(2) with the smooth web {Kr[lab]['Fb2']:.3f} (halos only: "
      f"{(nom if lab.startswith('nominal') else upp)['Fb2']:.3f}); calibrated gas worst {Kr[lab]['calibrated']:.3f}")
OUT["numbers"]["K"] = Kr
check("K (ESTIMATE) with the smooth web's cone enhancement both of FK1's brackets exceed DE11's 10% on the calibrated gas "
      "proxy", "; ".join(f"{k_}: {v['calibrated']:.3f}" for k_, v in Kr.items()),
      all(v["calibrated"] > 0.10 for v in Kr.values()),
      "if the second-order-sweep estimate holds, the smooth filaments themselves convert and the window of W narrows or "
      "closes; this rests on O(1) factors (the smooth web's local density on the mesh, its bias) and is flagged, not scored",
      load_bearing=False)

# ============================================================================================ summary
banner("SUMMARY")
P(f"""  The forest under FK1's local trigger (question A, the forest):
  - Controls: L357's V1 reproduced exactly (C1).  The gas proxy, fed L366's own history and the measured bias of its
    triggered mass, reproduces the PM's measured flux deviation (x{KCAL:.2f} at z = 2); the total-matter proxy would fail that
    same passing construction (T^2(k=5) = {ppm['2.0']['T2tot_k5']:.2f}) -- so it is not a forest proxy for kicked carriers (C2).
  - FK1's trigger converts every halo above M_min whole for z <= 3 (nominal cell), F_b = {float(np.interp(3.0, ZG, Fc_nom)):.2f} by z = 3,
    earlier than the PM's mesh trigger (H1).
  - Calibrated gas proxy at z = 2: nominal {nom['calibrated']['2.0']:.3f}, FDM floor {fdm['calibrated']['2.0']:.3f}, upper bracket {upp['calibrated']['2.0']:.3f}
    against DE11's 0.10 (H2): the nominal cell is AT the line, not safely inside it.
  - Window (W): forest zeta >= {zf['plain']:.2f} (plain) / {zf['sqrt_sigma']:.2f} (sqrt sigma); the flagship's worst-case bound is the
    own-density cap, zeta <= {zFl['1e12/canonical']:.2f} (canonical) / {zFl['1e12/alt']:.2f} (alt) for the 1e12 host (the trigger's reach
    alone would allow {zF_min:.1f}); the resolved bound is XR12_stream_shells W2.
  - The smooth web's cone enhancement (an estimate) gives nominal {Kr['nominal 5.31']['calibrated']:.3f} / upper {Kr['upper 25']['calibrated']:.3f}
    (K; its pre-declared 'both brackets over 10%' did not hold: the smooth web converts late, z <~ 2.5, when F_b(2) jumps to
    {Kr['nominal 5.31']['Fb2']:.2f} -- harmless to the z = 2-3 gas but a threat to everything after it, flagged for S8 / X-COP).""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["summary"] = dict(load_bearing_failed=n_fail, n_checks=len(CH), runtime_s=round(time.time() - T0, 1))
suffix = "_MUTATE" if MUTATE else ""
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results{suffix}.json"), "w"), indent=1, default=str)
P(f"\n  checks: {sum(ok for _, ok, _ in CH)}/{len(CH)} pass; load-bearing failures: {n_fail}   [{time.time() - T0:.0f}s]")
sys.exit(1 if n_fail else 0)
