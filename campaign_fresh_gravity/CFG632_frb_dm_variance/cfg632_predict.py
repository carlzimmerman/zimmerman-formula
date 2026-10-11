#!/usr/bin/env python3
"""CFG632 prediction (FROZEN_CRITERIA.md sec. 3): the framework's mean <DM_cosmic>(z) and sightline scatter sigma_DM(z) of the
cosmic dispersion measure, from candidate B's gas: census-retained baryons (CFG416/CFG515 fret_of), isothermal at sigma^2 = V_f^2/2
and hydrostatic (self-gravitating, with central stars) in the law's field g = g_N nu_mono(g_N/a0) out to the census edge
r_edge = r_M / ln(1 + f_ret f_b/(1 - f_b)).  Non-retained ionized gas is diffuse (primary) or in the shell r_edge..r_ta (bracket).

  sigma^2 = sigma^2_1h (Poisson halo crossings, real-space projected columns) + sigma^2_2h (linear clustering of the ionized gas)

INHERITED (labelled; none is a yardstick): catchment mass function = Tinker08 on the PM's EH no-wiggle spectrum (sigma8 0.811), Tinker10
bias, LCDM linear growth D(z) (cold energy = cold matter outside bound systems), NFW/Duffy08 c200m for M_ta and r_ta, Delta_ta(z)
interpolation, Moster+13 SHMR (recalled, PROVISIONAL), Hernquist stars a = 0.015 r200c/(1+sqrt2) (CFG556 convention), MD14 stellar
mass density (Chabrier), cold-gas densities (the authors' rho_H2 fit and rho_H2/rho_HI table), chi_e = 1 - Y/2.

Variants per footing: gas reading B-lo (gas = M_b - M*) / B-hi (all retained baryons ionized, no stars); profile H (hydrostatic) /
BETA (CFG556's declared beta-model, core 0.1 r200c, truncated at r_edge); non-retained gas DIFF (diffuse) / SHELL (rho ~ r^-2 between
r_edge and r_ta).  f_ret modes: census (prediction), one (f_ret = 1, MUTATE MU1), dep (f_ret = 0.01, gas-free extreme, MUTATE MU2).

Run: nice -n 10 python3 -I cfg632_predict.py   -> cfg632_predict.json / .out   (~ minutes, < 1 GB)
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import json, math, sys, time
from pathlib import Path
import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# ------------------------------------------------------------------ constants (PM cosmology, cfg361_pm.py / CFG556)
h = 0.6736; om_b, om_c = 0.02237, 0.1200
Om = (om_b + om_c) / h ** 2; Ob = om_b / h ** 2; OL = 1 - Om
FB = om_b / (om_b + om_c)                    # engine f_b = 0.15713 (CFG515 FB)
NS, SIG8 = 0.965, 0.811
G = 4.30091e-9                               # Mpc (km/s)^2 / Msun
MPC_M = 3.0856775814913673e22; MPC_CM = MPC_M * 100; PC_CM = MPC_CM / 1e6
MSUN_G = 1.98847e33; M_P = 1.67262192e-24; C_KMS = 299792.458
CHI_E = 1 - 0.2453 / 2
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0MPC = {f: v * MPC_M / 1e6 for f, v in A0.items()}   # (km/s)^2 / Mpc
RHO_CRIT0 = 2.77536627e11 * h * h            # Msun / Mpc^3 (physical, z = 0)
RHO_B0 = Ob * RHO_CRIT0                      # Msun / Mpc^3 comoving
NE0 = CHI_E * RHO_B0 * MSUN_G / M_P / MPC_CM ** 3      # cm^-3, all baryons ionized
DC = 1.686

def T_eh(k):  # cfg361_pm.py verbatim (via CFG556)
    OB = om_b / h ** 2; omh2, fb = Om * h * h, OB / Om
    s = 44.5 * math.log(9.83 / omh2) / math.sqrt(1 + 10 * (OB * h * h) ** 0.75)
    ag = 1 - 0.328 * math.log(431 * omh2) * fb + 0.38 * math.log(22.3 * omh2) * fb ** 2
    gam = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
    q = k * (2.7255 / 2.7) ** 2 / (gam * h)
    L0 = np.log(2 * math.e + 1.8 * q); C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)
_KG = np.geomspace(1e-5, 100, 40000)
_PK = _KG ** NS * T_eh(_KG * h) ** 2
_W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
_PK *= SIG8 ** 2 / (np.trapz(_PK * _W8(_KG * 8.0) ** 2 * _KG ** 2, _KG) / (2 * math.pi ** 2))

# ---- nu_mono, copied verbatim from CFG596_lean_pm_1024/cfg596_pm.py (as CFG628)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y

def fret_of(lM):
    """CFG416 cfg416_pm.py fret_of, copied verbatim (via cfg515_lib.py, FRETX = 1); lM = log10 M_ta [Msun/h]."""
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)

# ------------------------------------------------------------------ background, growth, mass function
def Ez(z): return np.sqrt(Om * (1 + z) ** 3 + OL)
def Omz(z): return Om * (1 + z) ** 3 / Ez(z) ** 2
def growth(z):
    """LCDM linear growth (Heath integral), normalised D(0) = 1 (INHERITED: cold energy = cold matter outside bound systems)."""
    def D_un(zz):
        a = np.geomspace(1e-5, 1 / (1 + zz), 4000)
        E = np.sqrt(Om / a ** 3 + OL)
        return 2.5 * Om * np.sqrt(Om / (1 / (1 + zz)) ** 3 + OL) * np.trapz(1 / (a * E) ** 3, a)
    return D_un(z) / D_un(0.0)

LM = np.arange(9.0, 16.0 + 1e-9, 0.05); MM = 10 ** LM; DLM = 0.05 * math.log(10)   # M200m [Msun/h]
RHO_M = Om * 2.77536627e11                                                        # Msun/h / (Mpc/h)^3 comoving
def sigma_R(R):
    x = np.outer(R, _KG); w = _W8(np.maximum(x, 1e-6))
    return np.sqrt(np.trapz(_PK * w ** 2 * _KG ** 2, _KG, axis=1) / (2 * math.pi ** 2))
SIG0 = sigma_R((3 * MM / (4 * math.pi * RHO_M)) ** (1 / 3))
yD = math.log10(200.0)
A10 = 1 + 0.24 * yD * math.exp(-(4 / yD) ** 4); a10 = 0.44 * yD - 0.88; B10, b10 = 0.183, 1.5
C10 = 0.019 + 0.107 * yD + 0.19 * math.exp(-(4 / yD) ** 4); c10 = 2.4
def hmf(z):
    """Tinker08 Delta = 200m with its z-evolution of (A, a, b); Tinker10 bias.  Returns n dM/dlnM [(h/Mpc)^3 comoving], bias."""
    D = growth(z); S = SIG0 * D
    dlns = np.gradient(np.log(S), LM * math.log(10))
    alpha = 10 ** (-(0.75 / math.log10(200 / 75.0)) ** 1.2)
    A = 0.186 * (1 + z) ** -0.14; a = 1.47 * (1 + z) ** -0.06; b = 2.57 * (1 + z) ** -alpha
    f = A * ((S / b) ** -a + 1) * np.exp(-1.19 / S ** 2)
    n = f * RHO_M / MM * (-dlns)
    nu = DC / S
    bias = 1 - A10 * nu ** a10 / (nu ** a10 + DC ** a10) + B10 * nu ** b10 + C10 * nu ** c10
    return n, bias

m_nfw = lambda x: np.log1p(x) - x / (1 + x)
def DTA(z):
    """turnaround overdensity w.r.t. the mean matter density: 11.81 at z = 0 (PM value, CFG504/555) -> 5.55 (EdS); declared
    interpolation 5.55 Omega_m(z)^-0.654 (exact at both ends)."""
    return 5.55 * Omz(z) ** -0.654
def halo_basics(M, z):
    """comoving Mpc/h, Msun/h.  Duffy08 c200m with (1+z)^-1.01; r_ta at Delta_ta(z); r200c at 200 rho_c(z)."""
    c = 10.14 * (M / 2e12) ** -0.081 * (1 + z) ** -1.01
    r2 = (3 * M / (4 * math.pi * 200 * RHO_M)) ** (1 / 3); mc = m_nfw(c)
    dta = DTA(z); om = Omz(z)
    xta = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - dta / 200.0, 0.2, 60.0, xtol=1e-12)
    xc = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - 1.0 / om, 0.05, 1.0, xtol=1e-12)
    return dict(M=M, c=c, r200=r2, rta=xta * r2, Mta=M * m_nfw(c * xta) / mc, r200c=xc * r2, M200c=M * m_nfw(c * xc) / mc)

def moster_mstar(M200c_sun, z):
    """Moster+13 SHMR with its z-evolution (parameters recalled, PROVISIONAL, INHERITED); M in Msun -> M* in Msun."""
    a = z / (1.0 + z)
    lM1 = 11.590 + 1.195 * a; N = 0.0351 - 0.0247 * a; b = 1.376 - 0.826 * a; g = 0.608 + 0.329 * a
    x = M200c_sun / 10 ** lM1
    return M200c_sun * 2 * N / (x ** (-b) + x ** g)

# ------------------------------------------------------------------ stellar mass density -> f_d(z) (INHERITED)
def rho_star(z, imf="chabrier"):
    """MD14 eq. 15 SFRD integrated with return fraction R = 0.27; Chabrier = Salpeter x 0.61. Msun/Mpc^3 (comoving)."""
    zz = np.linspace(z, 20.0, 4000)
    psi = 0.015 * (1 + zz) ** 2.7 / (1 + ((1 + zz) / 2.9) ** 5.6)
    H0s = 100 * h / (MPC_M / 1e3) * 3.15576e7            # 1/yr
    dtdz = 1.0 / (H0s * (1 + zz) * Ez(zz))
    val = (1 - 0.27) * np.trapz(psi * dtdz, zz)
    return val * (0.61 if imf == "chabrier" else 1.0)
def rho_H2(z): return 5.3e6 * ((1 + z) ** 3.6) / (1 + ((1 + z) / 2.1) ** 5.9)          # authors' fit (Msun/Mpc^3)
_H2HI = None
def rho_H2_HI(z):
    global _H2HI
    if _H2HI is None:
        p = Path(os.environ.get("CFG632_DATA", str(HERE.parents[2] / "_external_data" / "frb_sharma26" / "repo"))) / "data" / "f_diffuse" / "rhoH2_rhoHI.csv"
        a = np.loadtxt(p, delimiter=",", skiprows=1); _H2HI = (a[:, 0], a[:, 1])
    return np.interp(z, *_H2HI)
def f_d(z, imf="chabrier"):
    z = np.atleast_1d(z)
    rs = np.array([rho_star(x, imf) for x in z])
    cold = rho_H2(z) * (1 + 1 / rho_H2_HI(z))
    return 1 - (rs + cold) / RHO_B0

# ------------------------------------------------------------------ gas profiles (physical Mpc, Msun)
NR = 360
XG = np.concatenate([[0.0], np.geomspace(1e-4, 1.0, NR)])          # r / r_edge nodes
def hydro_profiles(Mgas, Mst, ast, re, a0, sig2):
    """vectorised over halos.  Isothermal rho = rho0 exp(-psi), dpsi/dr = g/sig2, g = g_N nu_mono(g_N/a0),
    g_N = G (M*(<r) + M_gas(<r)) / r^2; stars Hernquist (M*, a).  Shoot rho0 (bisection in log) so M_gas(<r_edge) = Mgas.
    Returns shell densities rho[i, j] on the shells (XG[j], XG[j+1]) * re[i]."""
    nH = len(Mgas)
    r = re[:, None] * XG[None, :]
    dr = np.diff(r, axis=1); rm = 0.5 * (r[:, 1:] + r[:, :-1])
    Ms_enc = Mst[:, None] * rm ** 2 / (rm + ast[:, None]) ** 2
    rhou = 3 * Mgas / (4 * math.pi * re ** 3)
    lo = np.log(np.maximum(rhou, 1e-300)) - 2.0; hi = np.log(np.maximum(rhou, 1e-300)) + 40.0
    def run(lr0):
        rho0 = np.exp(lr0); psi = np.zeros(nH); Mg = np.zeros(nH); rho = np.empty((nH, NR))
        for j in range(NR):
            rj = rho0 * np.exp(-psi)
            # predictor-corrector across the shell
            Mmid = Mg + 4 * math.pi * rm[:, j] ** 2 * rj * dr[:, j] * 0.5
            gN = G * (Ms_enc[:, j] + Mmid) / rm[:, j] ** 2
            g = gN * nu_mono(gN / a0)
            psi_mid = psi + g / sig2 * dr[:, j] * 0.5
            rmid = rho0 * np.exp(-psi_mid)
            rho[:, j] = rmid
            Mg = Mg + 4 * math.pi * rm[:, j] ** 2 * rmid * dr[:, j]
            psi = psi + g / sig2 * dr[:, j]
        return Mg, rho
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        Mg, _r = run(mid)
        too = Mg > Mgas
        hi = np.where(too, mid, hi); lo = np.where(too, lo, mid)
    Mg, rho = run(0.5 * (lo + hi))
    rho *= (Mgas / np.maximum(Mg, 1e-300))[:, None]
    return rho, Mg / np.maximum(Mgas, 1e-300)

def beta_profiles(Mgas, rc, re):
    """CFG556 declared beta-model (rho ~ 1/(1 + (r/rc)^2), core 0.1 r200c) truncated at r_edge, normalised to Mgas."""
    r = re[:, None] * XG[None, :]; rm = 0.5 * (r[:, 1:] + r[:, :-1]); dr = np.diff(r, axis=1)
    rho = 1.0 / (1 + (rm / rc[:, None]) ** 2)
    M = np.sum(4 * math.pi * rm ** 2 * rho * dr, axis=1)
    return rho * (Mgas / np.maximum(M, 1e-300))[:, None]

def column_sq_integral(rho, redges):
    """int 2 pi b Sigma(b)^2 db for shell-constant densities (exact shell projection); Sigma in Msun/Mpc^2.  rho (nH, NR),
    redges (nH, NR+1)."""
    nH = rho.shape[0]; NB = 220
    out = np.zeros(nH)
    for i in range(nH):
        re_ = redges[i]; Rmax = re_[-1]
        if Rmax <= 0 or not np.any(rho[i] > 0):
            continue
        b = np.concatenate([np.geomspace(re_[1] * 1e-2, Rmax, NB)])
        b2 = b[:, None] ** 2
        s_hi = np.sqrt(np.maximum(re_[None, 1:] ** 2 - b2, 0)); s_lo = np.sqrt(np.maximum(re_[None, :-1] ** 2 - b2, 0))
        with np.errstate(all="ignore"):          # Accelerate BLAS emits spurious matmul warnings; finiteness checked below
            Sig = 2 * (s_hi - s_lo) @ rho[i]
        if not np.all(np.isfinite(Sig)):
            raise FloatingPointError("non-finite column")
        f = 2 * math.pi * b * Sig ** 2
        out[i] = np.trapz(f, b) + math.pi * b[0] ** 2 * Sig[0] ** 2
    return out

def u_of_k(rho, redges, k):
    """normalised Fourier transform of the shell profile (comoving k and r handled by the caller)."""
    rm = 0.5 * (redges[:, 1:] + redges[:, :-1]); dM = 4 * math.pi * rm ** 2 * rho * np.diff(redges, axis=1)
    Mt = np.maximum(dM.sum(1), 1e-300)
    x = k[None, None, :] * rm[:, :, None]
    j0 = np.where(x > 1e-6, np.sin(x) / np.maximum(x, 1e-30), 1.0)
    return np.einsum("ij,ijk->ik", dM, j0) / Mt[:, None]

# ------------------------------------------------------------------ one redshift slice
ZG = np.array([0.0, 0.03, 0.07, 0.12, 0.18, 0.25, 0.33, 0.42, 0.52, 0.65, 0.8, 1.0, 1.25, 1.55, 1.9, 2.25])
KK = np.geomspace(1e-3, 50.0, 220)     # h/Mpc comoving

def slice_z(z, foot, fmode, reading, prof, outer, cache):
    n, bias = cache["hmf"][z]
    HB = cache["hb"][z]
    Mta = np.array([hb["Mta"] for hb in HB])                         # Msun/h
    if fmode == "census":
        fr = np.array([fret_of(math.log10(m)) for m in Mta])
    elif fmode == "one":
        fr = np.ones_like(Mta)
    else:
        fr = np.full_like(Mta, 0.01)
    Mb = fr * FB * Mta / h                                           # Msun
    a0 = A0MPC[foot]
    rM = np.sqrt(G * Mb / a0)                                        # physical Mpc
    re = rM / np.log1p(fr * FB / (1 - FB))
    rta_phys = np.array([hb["rta"] for hb in HB]) / h / (1 + z)
    re = np.minimum(re, rta_phys)
    r200c_phys = np.array([hb["r200c"] for hb in HB]) / h / (1 + z)
    if reading == "lo":
        Mst = np.minimum(np.array([moster_mstar(hb["M200c"] / h, z) for hb in HB]), Mb)
        Mgas = np.maximum(Mb - Mst, 0.0)
    else:
        Mst = np.zeros_like(Mb); Mgas = Mb.copy()
    ast = 0.015 * r200c_phys / (1 + math.sqrt(2))
    Vf2 = np.sqrt(G * Mb * a0)                                       # (km/s)^2
    sig2 = 0.5 * Vf2
    Mgas = np.where(Mgas > 1e-6 * Mb, Mgas, 0.0)                    # B-lo round-off: M* = M_b leaves no gas
    ok = Mgas > 0
    rho = np.zeros((len(Mb), NR)); norm_err = np.ones(len(Mb))
    nfall = 0
    if prof == "H":
        with np.errstate(all="ignore"):
            rr, ne_ = hydro_profiles(Mgas[ok], Mst[ok], ast[ok], re[ok], a0, sig2[ok])
        bad = ~(np.isfinite(ne_) & (np.abs(ne_ - 1) < 1e-6) & np.all(np.isfinite(rr), axis=1))
        # declared fallback: a halo whose hydrostatic solve cannot normalise (the stellar-pileup degeneracy of CFG628
        # disclosure 5: all gas inside the innermost shell) takes the BETA profile; counts reported
        if np.any(bad):
            idx = np.nonzero(ok)[0][bad]
            rr[bad] = beta_profiles(Mgas[idx], 0.1 * r200c_phys[idx], re[idx]); ne_[bad] = 1.0
            nfall = int(bad.sum())
        rho[ok] = rr; norm_err[ok] = ne_
    else:
        rho[ok] = beta_profiles(Mgas[ok], 0.1 * r200c_phys[ok], re[ok])
    redges = re[:, None] * XG[None, :]
    # non-retained ionized gas
    fdz = float(f_d(z)[0])
    Mnr = np.maximum(fr * 0 + (1 - fr) * FB * Mta / h, 0.0)          # catchment baryons not retained (Msun)
    if outer == "SHELL":
        # rho ~ r^-2 between r_edge and r_ta (equal mass per radius), appended as extra shells
        NS_ = 40
        out_edges = re[:, None] * (rta_phys / np.maximum(re, 1e-30))[:, None] ** (np.linspace(0, 1, NS_ + 1)[None, :])
        rm_o = 0.5 * (out_edges[:, 1:] + out_edges[:, :-1]); dr_o = np.diff(out_edges, axis=1)
        rho_o = 1.0 / rm_o ** 2
        Mo = np.sum(4 * math.pi * rm_o ** 2 * rho_o * dr_o, axis=1)
        has = (rta_phys > re * (1 + 1e-6)) & (Mo > 0)
        Mo = np.where(has, Mo, 1.0)
        rho_o = np.where(has[:, None], rho_o * (Mnr / Mo)[:, None], 0.0)
        rho_all = np.concatenate([rho, rho_o], axis=1)
        edges_all = np.concatenate([redges, out_edges[:, 1:]], axis=1)
        Mhalo = Mgas + np.where(has, Mnr, 0.0)
    else:
        rho_all = rho; edges_all = redges; Mhalo = Mgas
    # overlap rule: halo gas cannot exceed the cosmic ionized gas
    w = n * DLM                                                       # (h/Mpc)^3 per grid mass
    F_halo = float(np.sum(w * Mhalo * h) / (RHO_B0 / h ** 2))         # Msun/h * (h/Mpc)^3 / (Msun/h / (Mpc/h)^3)
    resc = min(1.0, fdz / F_halo) if F_halo > 0 else 1.0
    Mh_eff = Mhalo * resc; rho_eff = rho_all * resc
    # 1-halo: dsigma^2/dl_phys = n_phys int 2 pi b DM(b)^2 db,  DM(b) = chi_e Sigma / m_p / (1+z) [pc cm^-3]
    Q = column_sq_integral(rho_eff, edges_all)                        # Msun^2 / Mpc^2
    conv = (CHI_E * MSUN_G / M_P / MPC_CM ** 2 / PC_CM / (1 + z)) ** 2  # (pc cm^-3)^2 per (Msun/Mpc^2)^2
    n_phys = w * h ** 3 * (1 + z) ** 3                                 # Mpc^-3
    d1 = float(np.sum(n_phys * Q * conv))                              # (pc cm^-3)^2 / Mpc (physical)
    # per-mass decade contributions (for the report)
    dec = {}
    for lo_ in range(9, 16):
        m = (LM >= lo_) & (LM < lo_ + 1)
        dec[f"{lo_}-{lo_+1}"] = float(np.sum((n_phys * Q * conv)[m]) / max(d1, 1e-300))
    # 2-halo: I(k) = sum n b M u / rho_b + b_d * (f_d - F)   with total large-scale ionized bias 1
    kphys = KK * h * (1 + z)                                           # 1/Mpc physical for comoving k [h/Mpc]
    U = np.zeros((len(Mb), len(KK)))
    good = Mh_eff > 0
    U[good] = u_of_k(rho_eff[good], edges_all[good], kphys)
    Fh = min(F_halo * resc, fdz)
    Ib = float(np.sum(w * bias * Mh_eff * h) / (RHO_B0 / h ** 2))
    # declared rule: b_diff = (f_d - Ib)/(f_d - F) clipped at >= 0; if Ib > f_d (overlapping catchments, e.g. f_ret = 1) the halo
    # two-halo amplitude is renormalised by f_d / Ib so the ionized gas has large-scale bias 1 (the CFG556 NORM_TA analogue)
    bd = max((fdz - Ib) / max(fdz - Fh, 1e-12), 0.0) if fdz - Fh > 1e-6 else 0.0
    hn = min(1.0, fdz / Ib) if Ib > 0 else 1.0
    with np.errstate(all="ignore"):
        I = hn * np.sum((w * bias * Mh_eff * h)[:, None] * U, axis=0) / (RHO_B0 / h ** 2) + bd * (fdz - Fh)
    Dz = cache["D"][z]
    Pl = np.interp(np.log(KK), np.log(_KG), _PK) * Dz ** 2              # (Mpc/h)^3
    kint = np.trapz(KK * Pl * I ** 2 / (2 * math.pi), KK)              # Mpc/h (comoving), I in units of rho_b (f_d inside)
    d2_com = kint / h                                                  # comoving Mpc
    return dict(n_fallback=nfall, d1=d1, d2_com=d2_com, F_halo=F_halo, resc=resc, b_diff=bd, Ib=Ib, halo2h_norm=hn, f_d=fdz, decades=dec,
                norm_err_max=float(np.max(np.abs(norm_err[ok] - 1))) if np.any(ok) else 0.0,
                fret_at={str(x): float(np.interp(x, LM, fr)) for x in (11, 12, 13, 14, 15)},
                re_over_rta_at={str(x): float(np.interp(x, LM, re / rta_phys)) for x in (12, 13, 14, 15)})

def sigma_of_z(sl):
    """integrate dsigma^2: 1-halo per physical length dl = c dz / ((1+z) H); 2-halo per comoving dchi with W = n_e0 (1+z) f.
    Returns cumulative sigma(z) [pc cm^-3] on ZG, and the 1h / 2h split."""
    H0 = 100 * h                                                       # km/s/Mpc
    dl = C_KMS / (H0 * (1 + ZG) * Ez(ZG))                              # Mpc per unit z (physical)
    dchi = C_KMS / (H0 * Ez(ZG))
    f1 = np.array([s["d1"] for s in sl]) * dl
    f2 = np.array([s["d2_com"] for s in sl]) * dchi * (NE0 * (1 + ZG)) ** 2 * (MPC_CM / PC_CM) ** 2  # (pc cm^-3)^2 per unit z
    c1 = np.concatenate([[0], np.cumsum(0.5 * (f1[1:] + f1[:-1]) * np.diff(ZG))])
    c2 = np.concatenate([[0], np.cumsum(0.5 * (f2[1:] + f2[:-1]) * np.diff(ZG))])
    return np.sqrt(c1 + c2), np.sqrt(c1), np.sqrt(c2)

def mean_dm(zs):
    zz = np.linspace(0, max(np.max(zs), 1e-3), 400)
    fd = np.interp(zz, ZG, f_d(ZG))
    H0 = 100 * h
    integ = NE0 * fd * (1 + zz) * C_KMS / (H0 * Ez(zz)) * (MPC_CM / PC_CM)
    cum = np.concatenate([[0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(zz))])
    return np.interp(zs, zz, cum)

VARIANTS = [(r, p, o) for r in ("lo", "hi") for p in ("H", "BETA") for o in ("DIFF", "SHELL")]
PRIMARY = ("lo", "H", "DIFF")

def main():
    t0 = time.time()
    say("CFG632 prediction -- FROZEN_CRITERIA.md sec. 3. kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
    say(f"Om {Om:.5f} Ob {Ob:.5f} f_b {FB:.5f} n_e0 {NE0:.4e} cm^-3  chi_e {CHI_E:.5f}")
    cache = {"hmf": {}, "hb": {}, "D": {}}
    for z in ZG:
        cache["hmf"][z] = hmf(z); cache["hb"][z] = [halo_basics(M, z) for M in MM]; cache["D"][z] = growth(z)
    fdz = f_d(ZG)
    say("f_d(z) [MD14 Chabrier + authors' cold gas; INHERITED]: " + " ".join(f"{z:.2f}:{v:.4f}" for z, v in zip(ZG, fdz)))
    say("f_d Salpeter (reported): " + " ".join(f"{z:.2f}:{v:.4f}" for z, v in zip(ZG, f_d(ZG, 'salpeter'))))
    res = dict(lane="CFG632", z=ZG.tolist(), f_d=fdz.tolist(), mean_dm=mean_dm(ZG).tolist(), cases={})
    for foot in ("canonical", "alt"):
        for fmode in ("census", "one", "dep"):
            vlist = VARIANTS if fmode == "census" else [PRIMARY, ("hi", "H", "DIFF"), ("lo", "BETA", "DIFF"), ("hi", "H", "SHELL")]
            for (rd, pf, ou) in vlist:
                sl = [slice_z(z, foot, fmode, rd, pf, ou, cache) for z in ZG]
                s, s1, s2 = sigma_of_z(sl)
                key = f"{foot}|{fmode}|{rd}|{pf}|{ou}"
                res["cases"][key] = dict(sigma=s.tolist(), sigma_1h=s1.tolist(), sigma_2h=s2.tolist(),
                                         F_halo=[x["F_halo"] for x in sl], resc=[x["resc"] for x in sl],
                                         b_diff=[x["b_diff"] for x in sl], decades_z0p25=sl[5]["decades"],
                                         norm_err_max=max(x["norm_err_max"] for x in sl),
                                         n_fallback=[x["n_fallback"] for x in sl],
                                         fret_at=sl[0]["fret_at"], re_over_rta_z0=sl[0]["re_over_rta_at"])
                i3, i5, i10 = 6, 8, 11
                say(f"{key:34s} sigma(0.33/0.52/1.0) {s[i3]:7.1f} {s[i5]:7.1f} {s[i10]:7.1f}  1h/2h(0.52) {s1[i5]:6.1f}/{s2[i5]:6.1f}"
                    f"  F_halo(0) {sl[0]['F_halo']:.3f} resc {sl[0]['resc']:.3f}  normerr {res['cases'][key]['norm_err_max']:.1e} fallback {sum(res['cases'][key]['n_fallback'])}  [{time.time()-t0:.0f}s]")
    json.dump(res, open(HERE / "cfg632_predict.json", "w"), indent=1)
    open(HERE / "cfg632_predict.out", "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()
