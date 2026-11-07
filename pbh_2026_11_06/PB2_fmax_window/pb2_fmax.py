#!/usr/bin/env python3
"""PB2: ceiling f_max(M) on primordial black holes, 1e0-1e9 Msun, standard vs framework.

Criteria: FROZEN_CRITERIA.md (committed alone first, 06450918d1). Every literature anchor below carries its
source and status; see SOURCES. f_b = Omega_PBH / Omega_b. STD f_b = 5.364 x f_DM(literature).
Run: python3 pb2_fmax.py  (writes pb2_fmax_results.json; stdout -> pb2_fmax.out). Exit 1 if a check fails.
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, sys, math
from functools import lru_cache
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

# ---------------------------------------------------------------- constants (frozen, section 3)
OMB, S, H = 0.049, 5.364, 0.674
OMC = OMB * S
OMM = OMB + OMC
G, C, MSUN, KPC, PC, KB, MP = 6.674e-11, 2.998e8, 1.989e30, 3.0857e19, 3.0857e16, 1.380649e-23, 1.6726e-27
RHOC_MSUN_MPC3 = 2.775e11 * H**2
RHOC_SI = 1.8785e-26 * H**2  # kg/m^3
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LOGM = np.round(np.arange(0.0, 9.0001, 0.05), 4)
MGRID = 10**LOGM
TABLE_M = [1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9]
XS = [1.0, 0.2, 1e-2, 1e-4]
X_MAIN = 0.2


def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


# ---------------------------------------------------------------- literature rows (f_DM anchors)
PR, RU = "page-read, provisional", "recalled, unverified"
SRC_PBHB = "PBHbounds compilation file text (github bradkav/PBHbounds), page-read, provisional"
ROWS = {}


def row(rid, name, cls, src, status, anchors=None, func=None, note=""):
    ROWS[rid] = dict(id=rid, name=name, cls=cls, src=src, status=status, anchors=anchors, func=func, note=note)


row("A1", "CMB accretion, spherical, naked (AHK 2017, collisional ionisation)", "R", "1612.05644 Fig.14 via PBHbounds old_bounds/CMB_withoutDM.txt",
    SRC_PBHB, anchors=[(132.926, 0.98729), (215.227, 0.38903), (328.113, 0.16761), (564.250, 0.051173), (970.330, 0.016027),
                       (1351.46, 0.0080475), (2060.30, 0.0032530), (2784.42, 0.0017633), (3651.40, 0.00096813), (1e10, 1e-6)],
    note="last anchor (1e10, 1e-6) is the compiler's extrapolation, not AHK's; AHK abstract (page-read): f=1 excluded above ~1e2 Msun")
row("A2", "CMB accretion, disk, naked (Poulin+2017 / Serpico+2020)", "C", "1707.04206; 2002.10771", PR, anchors=None,
    note="NOT LOCATED as a curve: only 'f=1 excluded above ~2 Msun' (1707.04206 abstract) and 'naked bounds ~4x stronger than 1707.04206' (2002.10771 text)")
row("A3", "CMB accretion, CDM-halo dressed (Serpico+2020, spherical w/ DM halo)", "C", "2002.10771 Fig.6 via PBHbounds CMB.txt", SRC_PBHB,
    anchors=[(13.857, 1.21677), (29.774, 0.26298), (39.139, 0.0043521), (50.742, 0.00087028), (99.622, 4.9155e-5),
             (1001.89, 4.7877e-8), (8950.54, 8.9030e-9), (21048.5, 5.8502e-9), (1e10, 2.9e-9)],
    note="criteria named the disk-dressed curve; only the spherical-dressed curve was located (disclosed). Last anchor = Eddington floor f<2.9e-9 (2002.10771 Eq.25, page-read)")
row("X1", "X-ray / radio from accreting Galactic PBHs (Manshanden+2019)", "C", "1812.07967 Fig.5 via PBHbounds X-ray.txt, Radio.txt", SRC_PBHB,
    anchors=[(20.03, 0.0024736), (23.90, 0.0024736), (28.52, 0.0018447), (33.41, 0.0010854), (37.49, 0.00084211), (44.28, 0.00064321),
             (50.10, 0.00054714), (55.37, 0.00049876), (62.46, 0.00045461), (72.50, 0.00040179), (83.97, 0.00036618), (100.09, 0.00033113)],
    note="min(X-ray, radio) on the union of anchor masses; radio from 23.9 Msun")
row("D1", "Wide binaries (Monroy-Rodriguez & Allen 2014)", "R", "1406.5169 Fig.9 via PBHbounds WideBinaries.txt", SRC_PBHB,
    anchors=[(2.7095, 1.01164), (3.9313, 0.90301), (4.6653, 0.73424), (6.0188, 0.60233), (7.7655, 0.46654), (11.269, 0.34627),
             (23.297, 0.20660), (65.169, 0.10184), (1.71079e8, 0.10378)])
row("D2", "UFD / Eridanus II star cluster (Brandt 2016)", "R", "1605.03665 Fig.3 via PBHbounds UFdwarfs.txt", SRC_PBHB,
    anchors=[(11.810, 1.02613), (21.902, 0.57425), (44.584, 0.30129), (110.63, 0.13895), (262.02, 0.065755), (650.19, 0.030324),
             (1594.6, 0.014350), (3910.8, 0.0071506), (9816.7, 0.0036093), (11555.9, 0.0031725)])
row("D3", "Galactic disk heating (Carr & Sakellariadou 1999 form)", "R", "2002.12778 Eq.(78)", PR,
    func=lambda M: (M / 3e6)**-1.0, note="f < (M/3e6)^-1 for M < 3e9 (review text, page-read)")


def _df(M):
    M = np.asarray(M, float)
    return np.where(M < 5e5, (M / 2e4)**(-10 / 7), np.where(M < 2e6, (M / 4e4)**-2, np.where(M < 1e8, (M / 0.1)**-0.5, M / 1e12)))


row("D4", "Dynamical friction to the Galactic centre (Carr & Sakellariadou 1999, r_c = 2 kpc)", "R", "2002.12778 Eq.(79)", PR, func=_df,
    note="review: low-M branch is drag by spheroid stars, high-M by halo objects; > 1e8 branch is incredulity M/M_halo")
row("L1", "Galactic microlensing toward LMC (EROS-2)", "R", "astro-ph/0607207 Fig.15 via PBHbounds EROS.txt", SRC_PBHB,
    anchors=[(0.4905, 0.084242), (1.8458, 0.14764), (3.1742, 0.20309), (15.199, 0.52857)])
row("L2", "Quasar microlensing (Esteban-Gutierrez+2022)", "C", "2203.04777 via PBHbounds Quasars.txt", SRC_PBHB,
    anchors=[(10.0, 0.013), (30.0, 0.011), (60.0, 0.011)])
row("L3", "Millilensing of compact radio sources (Wilkinson+2001, review approximation)", "R", "astro-ph/0101328 via 2002.12778 Eq.(69)", PR,
    func=lambda M: np.where(np.asarray(M) < 1e5, (np.asarray(M) / 2e4)**-2.0, np.where(np.asarray(M) < 1e8, 0.06, (np.asarray(M) / 4e8)**2)),
    note="review Eq.(69) text partly garbled in extraction; branches read as (M/2e4)^-2, 0.06, (M/4e8)^2 (continuous at 1e5, 1e8)")
row("L4", "FRB lensing (CHIME, Leung+2022)", "C", "2204.06001 Fig.5 via PBHbounds FRB-Leung2022.txt", SRC_PBHB, anchors=None,
    note="f_PBH >= 1 for every M >= 0.53 Msun in the file: no bound on this grid. GRB lensing: forecasts / a detection claim, not scored")
row("G1", "LVK merger rate of early binaries (Kavanagh+2018)", "R", "1805.09034 Fig.11 + 1904.08976 via PBHbounds LIGO.txt", SRC_PBHB,
    anchors=[(0.66689, 0.032146), (0.80324, 0.025266), (1.00414, 0.018807), (10.0, 0.0041282), (20.0, 0.0023600), (40.0, 0.0013667), (100.0, 0.00077436), (200.0, 0.0017405), (300.0, 0.0044122)])
row("G2", "PTA SIGW, Gaussian peaks (NANOGrav 11-yr)", "G", "1910.12239 Fig.2 via PBHbounds NANOGrav.txt", SRC_PBHB,
    anchors=[(0.9, 1.0999e-8), (1.0, 5.6700e-10), (1.6, 0.00083366), (1.8, 4.5518)])
row("S1", "mu distortion, Gaussian peaks (FIRAS)", "G", "1710.06945 abstract; 2002.12778 text", PR,
    func=lambda M: np.where(np.asarray(M) >= 1e5, 1e-30, np.inf),
    note="'exclude PBHs in this mass range from playing any interesting cosmological role' (Gaussian); encoded as 1e-30 for M >= 1e5 (Nakama); review says 1e4 < M < 1e12 (bracket)")
row("P1", "Lyman-alpha Poisson power (Murgia+2019)", "R", "1903.10509 abstract via PBHbounds Lyalphaforest.txt", PR,
    anchors=[(60.0, 1.0), (600.0, 0.1), (6000.0, 0.01), (60000.0, 0.001)], note="f M < 60 Msun (2 sigma, Gaussian z_reion prior); 170 with flat prior")


def p2_fdm(M, k=0.1, beta=0.04, As=2.1e-9):
    """Derived Planck CDI limit from PBH Poisson noise (FM-P): f_DM,max = D2lim 2pi^2 Omega_c rho_c / (k^3 M)."""
    d2 = beta / (1 - beta) * As
    return d2 * 2 * math.pi**2 * OMC * RHOC_MSUN_MPC3 / (k**3 * np.asarray(M, float))


row("P2", "Planck CDI isocurvature from Poisson noise (DERIVED here)", "R", "Planck 2018 X, 1807.06211: beta_iso = 0.04 at k = 0.1 /Mpc (recalled, unverified)", RU,
    func=p2_fdm)


def interp_row(r, M):
    M = np.asarray(M, float)
    if r["func"] is not None:
        v = np.asarray(r["func"](M), float)
        return np.where(np.isfinite(v), v, np.inf)
    if r["anchors"] is None:
        return np.full_like(M, np.inf)
    a = np.array(r["anchors"])
    lm, lf = np.log10(a[:, 0]), np.log10(a[:, 1])
    out = np.full_like(M, np.inf)
    ins = (np.log10(M) >= lm[0]) & (np.log10(M) <= lm[-1])
    out[ins] = 10**np.interp(np.log10(M[ins]), lm, lf)
    return out


def std_fdm(rid, M):
    if rid == "X1":
        xr = [(20.03, 0.0024736), (21.39, 0.0024728), (23.30, 0.0025101), (26.17, 0.0025475), (28.69, 0.0025858), (32.10, 0.0026244),
              (36.28, 0.0027046), (39.94, 0.0027876), (43.78, 0.0028733), (48.68, 0.0029614), (53.47, 0.0030995), (58.86, 0.0031947),
              (66.39, 0.0033434), (74.43, 0.0035532), (85.16, 0.0038341), (92.78, 0.0039521), (100.27, 0.0040738)]
        rd = [(23.90, 0.0070735), (28.52, 0.0018447), (33.41, 0.0010854), (34.06, 0.0010207), (37.49, 0.00084211), (44.28, 0.00064321),
              (50.10, 0.00054714), (55.37, 0.00049876), (62.46, 0.00045461), (72.50, 0.00040179), (83.97, 0.00036618), (100.09, 0.00033113)]
        a = interp_row(dict(func=None, anchors=xr), M)
        b = interp_row(dict(func=None, anchors=rd), M)
        return np.minimum(a, b)
    return interp_row(ROWS[rid], M)


# ---------------------------------------------------------------- FM-H: galaxy-hosted PBH spheroid (PB3 convention)
RHOC07_KPC = 2.775e11 * 0.70**2 / 1e9  # Msun/kpc^3 (PB3's h = 0.70 inside r_vir rule only)
MW_MBT, RS_NFW, RHO8 = 6e10, 20.0, 0.0105  # Msun, kpc, Msun/pc^3
VC_MW = 220e3


def rvir(Mbt, F, s=1.0):
    return s * (3 * (1 + F) * Mbt / (4 * math.pi * 200 * RHOC07_KPC))**(1 / 3)


def rho_nfw(r):
    rhos = RHO8 * (8 / RS_NFW) * (1 + 8 / RS_NFW)**2
    x = r / RS_NFW
    return rhos / (x * (1 + x)**2)


def rho_fw1(r, Mbt, F, s):
    """FW PBH density (Msun/pc^3) at f_b = 1 normalisation, r_vir evaluated at F."""
    rv = rvir(Mbt, F, s)
    return np.where(r < rv, Mbt / (4 * math.pi * rv * r**2) / 1e9, 0.0)


def tau_ratio_LMC(Mbt, F, s, m3=False):
    l, b, R0, L = math.radians(280.5), math.radians(-32.9), 8.0, 50.0
    rr = lambda D: math.sqrt(R0**2 + D**2 - 2 * R0 * D * math.cos(b) * math.cos(l))
    k = lambda D: D * (L - D) / L
    tdm = quad(lambda D: rho_nfw(rr(D)) * k(D), 0, L, limit=200)[0]
    if m3:
        return S
    tfw = quad(lambda D: float(rho_fw1(rr(D), Mbt, F, s)) * k(D), 0, L, limit=200, points=[rvir(Mbt, F, s)] if rvir(Mbt, F, s) < 58 else None)[0]
    return tdm / tfw


def mw_hernquist_factors(a0, r_kpc=2.0, Mb=6e10, a_kpc=3.0):
    """D4 medium factor sqrt(rho_dyn / (nu rho_real)) at r (law on Hernquist toy)."""
    GM = G * Mb * MSUN

    def g_law(r):
        gN = GM / (r + a_kpc * KPC)**2
        return nu(gN / a0) * gN

    r = r_kpc * KPC
    dr = 1e-4 * r
    d = ((r + dr)**2 * g_law(r + dr) - (r - dr)**2 * g_law(r - dr)) / (2 * dr)
    rho_dyn = d / (4 * math.pi * G * r**2)
    rho_real = Mb * MSUN * a_kpc * KPC / (2 * math.pi * r * (r + a_kpc * KPC)**3)
    gN = GM / (r + a_kpc * KPC)**2
    nr = float(nu(gN / a0))
    return math.sqrt(rho_dyn / (nr * rho_real)), dict(rho_dyn=rho_dyn, rho_real=rho_real, nu=nr)


ERI = dict(sigma=6.9e3, rh_pc=280.0, Mstar=6e4)


def eri_masses():
    Mdyn = 4 * ERI["sigma"]**2 * ERI["rh_pc"] * PC / G / MSUN
    Mst_in = ERI["Mstar"] / 2**1.5  # Plummer mass inside a = r_h
    return Mdyn, Mst_in


def solve_F(target, Mbt, s, rfun):
    """f_b such that f_b * rho_fw1(F=f_b) = target (rho in same units); rfun(F) returns rho_fw1."""
    f = target / rfun(0.0)
    for _ in range(60):
        f_new = target / rfun(f)
        if abs(f_new - f) <= 1e-13 * max(f, 1e-300):
            f = f_new
            break
        f = f_new
    return f


# ---------------------------------------------------------------- FM-A: law baryon dressing
@lru_cache(maxsize=None)
def accretion_E(M, a0, z, e):
    T = 2.7255 * (1 + z)
    cs = math.sqrt(5 / 3 * KB * T / (1.22 * MP))
    vbc = 30e3 * (1 + z) / 1000
    v2 = cs**2 + vbc**2
    GM = G * M * MSUN
    rB = GM / v2

    def glaw(r):
        gN = GM / r**2
        return nu((gN + e * a0) / a0) * gN

    rs = np.logspace(math.log10(rB) - 1, math.log10(rB) + 4, 4000)
    gNs = GM / rs**2
    h = rs * nu((gNs + e * a0) / a0) * gNs - v2
    idx = np.where(np.sign(h[:-1]) != np.sign(h[1:]))[0]
    if len(idx) == 0:
        ra = rs[-1]
    else:
        i = idx[-1]
        ra = brentq(lambda r: r * glaw(r) - v2, rs[i], rs[i + 1], xtol=1e-12 * rs[i])
    up = 100 * rB
    phix = 0.0
    if up > ra:
        phix = quad(lambda lr: (glaw(math.exp(lr)) - GM / math.exp(lr)**2) * math.exp(lr), math.log(ra), math.log(up), limit=200)[0]
    E = (ra / rB)**2 * math.exp(phix / v2)
    rho = OMB * RHOC_SI * (1 + z)**3
    mdot = 4 * math.pi * rho * GM**2 / v2**1.5
    medd = 1.26e31 * M / (0.1 * C**2)
    return E, mdot / medd, dict(ra_over_rB=ra / rB, phix_over_v2=phix / v2, v_eff_kms=math.sqrt(v2) / 1e3)


def E_L(M, a0, z, e, p):
    E, mN, _ = accretion_E(M, a0, z, e)
    Eeff = min(E, max(1.0, 1.0 / mN)) if mN < 1 else 1.0
    return Eeff**p


# ---------------------------------------------------------------- FM-G
SIG_EQ = 0.005


def fm_g(fdm_std, sigma_fw):
    fm = fdm_std * OMC / OMM
    Rs = fm**2 * (fm**2 + SIG_EQ**2)**(-21 / 74)
    g = lambda f: math.log(f**2 * (f**2 + sigma_fw**2)**(-21 / 74)) - math.log(Rs)
    f_fw = brentq(g, 1e-12, 1e3, xtol=1e-16, rtol=1e-14) if sigma_fw != SIG_EQ else fm
    return f_fw * OMM / OMB  # f_b


# ---------------------------------------------------------------- FM-P: P1 linear growth
OMR = 9.1e-5 * (0.674 / H)**2


def Hz2(a):  # (H/H0)^2 standard background (A_BG)
    return OMM * a**-3 + OMR * a**-4 + (1 - OMM - OMR)


def growth_delta_b(om_pbh, om_cdm, z_end=3.0, z_rel=1100.0, z_ini=1e5):
    """delta_b(z_end) for unit initial PBH Poisson delta (isocurvature), clustering = CDM + PBH (+ baryons after z_rel)."""
    a_rel = 1 / (1 + z_rel)

    def rhs(x, y):
        a = math.exp(x)
        dP, dPp, dC, dCp, dB, dBp = y
        h2 = Hz2(a)
        dlnH = 0.5 * (-3 * OMM * a**-3 - 4 * OMR * a**-4) / h2
        src = 1.5 / h2 * a**-3 * (om_pbh * dP + om_cdm * dC + (OMB * dB if a > a_rel else 0.0))
        fr = -(2 + dlnH)
        out = [dPp, fr * dPp + src, dCp, fr * dCp + src, 0.0, 0.0]
        if a > a_rel:
            out[4], out[5] = dBp, fr * dBp + src
        return out

    sol = solve_ivp(rhs, [math.log(1 / (1 + z_ini)), math.log(1 / (1 + z_end))], [1, 0, 0, 0, 0, 0], rtol=1e-9, atol=1e-12)
    return sol.y[4, -1]


@lru_cache(maxsize=None)
def p1_fw_fb(M, mods=True):
    fdm = 60.0 / M
    if fdm > 1.0:
        return np.inf
    om_s = fdm * OMC
    if not mods:
        return fdm * S
    db_s = growth_delta_b(om_s, OMC - om_s)
    Plim = db_s**2 / om_s  # P ~ M delta_b^2 / Omega (same M)
    g = lambda lom: math.log(growth_delta_b(math.exp(lom), 0.0)**2 / math.exp(lom)) - math.log(Plim)
    lo, hi = math.log(1e-12), math.log(10 * OMB)
    if g(hi) < 0:
        return np.inf  # FW power below the limit even at f_b = 10
    if g(lo) > 0:
        return 1e-12 / OMB
    return math.exp(brentq(g, lo, hi, xtol=1e-10)) / OMB


# ---------------------------------------------------------------- assemble FW rows
def build(a0, br=None, mods=True, m3=False, planted=False, incred="frozen", a1_ext=True):
    br = dict(Mbt=MW_MBT, s=1.0, eta=3.0, z=600.0, e=0.026) | (br or {})
    M = MGRID
    std = {rid: S * std_fdm(rid, M) for rid in ROWS}
    if not a1_ext:
        std["A1"] = np.where(M > 3651.40, np.inf, std["A1"])
    if planted:
        std["PL"] = np.where((M >= 1e3) & (M <= 1e4), S * 1e-6, np.inf)
    fw, info = {}, {}
    Mbt, s = br["Mbt"], br["s"]
    Mhost_std_mw, (Mdyn_eri, Mst_in) = 1e12, eri_masses()
    for rid in std:
        fdm = std[rid] / S
        if not mods:
            fw[rid] = std[rid].copy()
            continue
        if rid in ("D1", "D3", "X1", "L2", "D4", "L1"):
            r = {"D1": 8.0, "D3": 8.0, "L2": 8.0, "X1": 1.0, "D4": 2.0, "L1": None}[rid]
            out = np.full_like(M, np.inf)
            for i, Mi in enumerate(M):
                if not np.isfinite(fdm[i]):
                    continue
                if m3:
                    f = fdm[i] * S
                elif rid == "L1":
                    f = solve_F(fdm[i], Mbt, s, lambda F: 1.0 / tau_ratio_LMC(Mbt, F, s))
                else:
                    f = solve_F(fdm[i] * rho_nfw(r), Mbt, s, lambda F: float(rho_fw1(r, Mbt, F, s)))
                if not m3 and rid == "D1":
                    eMW = VC_MW**2 / (8 * KPC) / a0
                    nb = float(nu(eMW))
                    ni = float(nu((G * Mi * MSUN / (0.1 * PC)**2 + VC_MW**2 / (8 * KPC)) / a0))
                    f *= nb / ni**2
                if not m3 and rid == "D4":
                    f *= mw_hernquist_factors(a0)[0]
                host = Mhost_std_mw if m3 else Mbt
                if f * host < Mi:
                    f = np.inf if incred == "frozen" else max(f, Mi / host)
                out[i] = f
            fw[rid] = out
        elif rid == "D2":
            if m3:
                fw[rid] = std[rid].copy()
                continue
            fac = (Mdyn_eri - Mst_in) / (br["eta"] * Mst_in)
            f = fdm * fac
            host = br["eta"] * ERI["Mstar"]
            bad = f * host < M
            f = np.where(bad, np.inf if incred == "frozen" else np.maximum(f, M / host), f)
            fw[rid] = f
        elif rid == "A1":
            out = np.full_like(M, np.inf)
            for i, Mi in enumerate(M):
                if np.isfinite(std[rid][i]):
                    out[i] = std[rid][i] / E_L(float(Mi), a0, br["z"], br["e"], 2)
            fw[rid] = out
        elif rid == "A3":
            fw[rid] = np.full_like(M, np.inf)  # no CDM dressing in FW
        elif rid == "G1":
            fw[rid] = np.array([fm_g(x, 0.0) if np.isfinite(x) else np.inf for x in fdm])
        elif rid == "P1":
            anchors = [60.0, 600.0, 6000.0, 60000.0]
            vals = [p1_fw_fb(m) for m in anchors]
            info["P1_fw_anchors_fb"] = dict(zip([str(m) for m in anchors], vals))
            fw[rid] = interp_row(dict(func=None, anchors=list(zip(anchors, vals))), M) if all(np.isfinite(vals)) else np.full_like(M, np.inf)
        else:  # L3, L4, P2, S1, G2, A2, PL: FM-L / FM-P(P2) / FM-S unchanged
            fw[rid] = std[rid].copy()
    return std, fw, info


def envelopes(rows, include_planted=False):
    keys = [k for k in rows]
    cls = lambda k: "R" if k == "PL" else ROWS[k]["cls"]
    def env(sel):
        ks = [k for k in keys if cls(k) in sel]
        arr = np.vstack([rows[k] for k in ks])
        j = np.argmin(arr, axis=0)
        return arr.min(axis=0), [ks[i] if np.isfinite(arr[i, n]) else "none" for n, i in enumerate(j)]
    return {"ROBUST": env({"R"}), "AGGRESSIVE": env({"R", "C"}), "GAUSSIAN": env({"R", "C", "G"})}


def at(M0, arr):
    return float(arr[np.argmin(abs(LOGM - math.log10(M0)))])


def open_ranges(env, X):
    ok = env >= X
    rngs, start = [], None
    for i, o in enumerate(ok):
        if o and start is None:
            start = LOGM[i]
        if (not o or i == len(ok) - 1) and start is not None:
            end = LOGM[i] if o else LOGM[i - 1]
            rngs.append((float(start), float(end)))
            start = None
    return rngs


def fmt(x):
    return "none" if not np.isfinite(x) else f"{x:.3g}"


# ---------------------------------------------------------------- main
def main():
    res = dict(criteria="06450918d1", definitions=dict(f_b="Omega_PBH/Omega_b", f_DM="f_b/5.364", f_m="f_b/6.364"),
               sources={k: dict(name=v["name"], cls=v["cls"], src=v["src"], status=v["status"], note=v["note"]) for k, v in ROWS.items()},
               footings={})
    ok_all = True
    lines = []
    P = lambda s="": lines.append(s)
    P("PB2 f_max(M), 1e0-1e9 Msun. f_b = Omega_PBH/Omega_b; f_DM-equiv = f_b/5.364; f_m = f_b/6.364. Criteria 06450918d1.")
    P("Adopts nothing. kappa = 1/2 FITTED; not theory closed. Every literature value provisional or recalled (see json sources).")
    std0, _, _ = build(FOOT["canonical"], mods=False)
    envS = envelopes(std0)
    # KA1
    ka_ref = {1e1: (3e-3, "recalled 3e-3; page-read 2002.12778 text: LVK '1e-3 to 1e-2'"), 1e3: (1e-3, "recalled, unverified"), 1e5: (1e-4, "recalled, unverified")}
    ka1 = {}
    for M0, (ref, note) in ka_ref.items():
        v = at(M0, envS["ROBUST"][0]) / S
        va = at(M0, envS["AGGRESSIVE"][0]) / S
        ka1[str(M0)] = dict(std_robust_fDM=v, std_aggressive_fDM=va, ref=ref, ratio=v / ref, passed=bool(1 / 3 <= v / ref <= 3), ref_note=note,
                            independent=False, independence_note="rows from PBHbounds/review, the same compilations the review envelopes use")
    res["KA1"] = ka1
    ka1_pass = all(d["passed"] for d in ka1.values())
    P(f"\nKA1 (STD ROBUST envelope vs review/recalled, factor 3): " + "; ".join(
        f"M={float(k):.0e}: {d['std_robust_fDM']:.3g} vs {d['ref']:.0e} (x{d['ratio']:.2g}) {'PASS' if d['passed'] else 'FAIL'} [aggressive {d['std_aggressive_fDM']:.3g}]" for k, d in ka1.items()))
    ok_all &= ka1_pass
    # KA2
    res["KA2"] = dict(status="NOT LOCATED: no literature CMB-Poisson f(M) value read; P2 derived only",
                      P2_fDM={str(m): float(p2_fdm(m)) for m in TABLE_M})
    P("KA2: literature CMB-Poisson value NOT LOCATED; P2 derived f_DM < %.3g/M (Msun)" % float(p2_fdm(1.0)))
    # KA3
    test = [fm_g(x, SIG_EQ) / S / (x) for x in (1e-3, 1e-2)]
    ka3 = all(abs(t - 1) < 1e-12 for t in test)
    res["KA3"] = dict(passed=ka3, ratios=test)
    P(f"KA3 FM-G with sigma_eq kept returns STD: {'PASS' if ka3 else 'FAIL'} {test}")
    ok_all &= ka3

    for fname, a0 in FOOT.items():
        std, fw, info = build(a0)
        envF = envelopes(fw)
        fo = dict(a0=a0, info=info, table=[], labels={}, open_ranges={}, fragile={}, factors={}, brackets={}, mutate={})
        # per-row table at TABLE_M
        P(f"\n===== footing {fname} (a0 = {a0:.4e}) =====")
        P("rows at table masses, f_b,max STD -> FW (factor):")
        for rid in ROWS:
            cells = []
            for M0 in TABLE_M:
                s_, f_ = at(M0, std[rid]), at(M0, fw[rid])
                if not np.isfinite(s_) and not np.isfinite(f_):
                    cells.append("-")
                else:
                    fac = f_ / s_ if np.isfinite(s_) and np.isfinite(f_) else float("nan")
                    cells.append(f"{fmt(s_)}->{fmt(f_)}" + (f"(x{fac:.3g})" if np.isfinite(fac) else ""))
            fo["factors"][rid] = {str(M0): [at(M0, std[rid]), at(M0, fw[rid])] for M0 in TABLE_M}
            P(f"  {rid} [{ROWS[rid]['cls']}] " + " | ".join(f"{M0:.0e}:{c}" for M0, c in zip(TABLE_M, cells)))
        P("\nENVELOPES (f_b; f_DM-equiv = /5.364), dominant row:")
        for M0 in TABLE_M:
            i = np.argmin(abs(LOGM - math.log10(M0)))
            rowd = dict(M=M0)
            for en in ("ROBUST", "AGGRESSIVE", "GAUSSIAN"):
                rowd[f"STD_{en}"] = [float(envS[en][0][i]) if fname == "canonical" else float(envelopes(std)[en][0][i]), envelopes(std)[en][1][i]]
                rowd[f"FW_{en}"] = [float(envF[en][0][i]), envF[en][1][i]]
            fo["table"].append(rowd)
            P(f"  M={M0:.0e}: ROBUST STD {fmt(rowd['STD_ROBUST'][0])} ({rowd['STD_ROBUST'][1]}) FW {fmt(rowd['FW_ROBUST'][0])} ({rowd['FW_ROBUST'][1]}) | "
              f"AGGR STD {fmt(rowd['STD_AGGRESSIVE'][0])} ({rowd['STD_AGGRESSIVE'][1]}) FW {fmt(rowd['FW_AGGRESSIVE'][0])} ({rowd['FW_AGGRESSIVE'][1]}) | "
              f"GAUSS FW {fmt(rowd['FW_GAUSSIAN'][0])}")
        # brackets
        BR = [("Mbt", 1.5e11), ("s", 0.5), ("s", 2.0), ("eta", 1.0), ("eta", 10.0), ("z", 300.0), ("z", 1000.0), ("e", 0.006), ("e", 0.1)]
        benv = {}
        for k, v in BR:
            _, fwb, _ = build(a0, {k: v})
            benv[f"{k}={v}"] = envelopes(fwb)["ROBUST"][0]
            fo["brackets"][f"{k}={v}"] = {str(M0): at(M0, benv[f"{k}={v}"]) for M0 in TABLE_M}
        P("\nLABELS on FW ROBUST (primary), X in " + str(XS) + "; FRAGILE if any one bracket flips:")
        for X in XS:
            labs = []
            for M0 in TABLE_M:
                o = at(M0, envF["ROBUST"][0]) >= X
                flip = [b for b, e in benv.items() if (at(M0, e) >= X) != o]
                lab = ("OPEN" if o else "CLOSED") + (" FRAGILE" if flip else "")
                fo["labels"][f"X={X}|M={M0:.0e}"] = dict(label=lab, flipped_by=flip)
                labs.append(f"{M0:.0e}:{lab}")
            fo["open_ranges"][f"FW_ROBUST|X={X}"] = open_ranges(envF["ROBUST"][0], X)
            fo["open_ranges"][f"STD_ROBUST|X={X}"] = open_ranges(envelopes(std)["ROBUST"][0], X)
            fo["open_ranges"][f"FW_AGGRESSIVE|X={X}"] = open_ranges(envF["AGGRESSIVE"][0], X)
            P(f"  X={X}: " + ", ".join(labs))
            P(f"     open log10 M ranges: FW_ROBUST {fo['open_ranges'][f'FW_ROBUST|X={X}']}  STD_ROBUST {fo['open_ranges'][f'STD_ROBUST|X={X}']}  FW_AGGR {fo['open_ranges'][f'FW_AGGRESSIVE|X={X}']}")
        # diagnostics
        fac_d4, d4i = mw_hernquist_factors(a0)
        acc = {str(m): dict(zip(["E", "mdot_N", "detail"], accretion_E(float(m), a0, 600.0, 0.026))) for m in TABLE_M}
        for m in TABLE_M:
            acc[str(m)]["E_L_p2"] = E_L(m, a0, 600.0, 0.026, 2)
        fo["diag"] = dict(D4_medium_factor=fac_d4, D4_detail=d4i, accretion=acc,
                          rvir_MW_kpc=rvir(MW_MBT, 0.0), rho_ratio_8kpc=float(rho_nfw(8.0) / rho_fw1(8.0, MW_MBT, 0.0, 1.0)),
                          rho_ratio_1kpc=float(rho_nfw(1.0) / rho_fw1(1.0, MW_MBT, 0.0, 1.0)), rho_ratio_2kpc=float(rho_nfw(2.0) / rho_fw1(2.0, MW_MBT, 0.0, 1.0)),
                          tau_ratio_LMC=tau_ratio_LMC(MW_MBT, 0.0, 1.0), eri_factor_eta3=(eri_masses()[0] - eri_masses()[1]) / (3 * eri_masses()[1]),
                          eri_Mdyn=eri_masses()[0], nu_e_MW=float(nu(VC_MW**2 / (8 * KPC) / a0)))
        P(f"\ndiagnostics: r_vir(MW) {fo['diag']['rvir_MW_kpc']:.1f} kpc; rho_NFW/rho_fw1 at 1, 2, 8 kpc = {fo['diag']['rho_ratio_1kpc']:.3g}, {fo['diag']['rho_ratio_2kpc']:.3g}, {fo['diag']['rho_ratio_8kpc']:.3g}; "
          f"tau_NFW/tau_fw1 (LMC) {fo['diag']['tau_ratio_LMC']:.3g}; Eri II rho_DM/(eta rho_*) {fo['diag']['eri_factor_eta3']:.3g} (M_dyn {fo['diag']['eri_Mdyn']:.3g}); "
          f"nu(e_MW) {fo['diag']['nu_e_MW']:.4f}; D4 medium factor {fac_d4:.4f}")
        P("accretion dressing at z=600, e=0.026: " + "; ".join(f"{float(k):.0e}: E {v['E']:.4g} (r_a/r_B {v['detail']['ra_over_rB']:.4g}, Phi_x/v2 {v['detail']['phix_over_v2']:.3g}) mdot_N {v['mdot_N']:.3g} E_L {v['E_L_p2']:.4g}" for k, v in acc.items()))
        # sensitivities (not scored)
        _, fw_inc, _ = build(a0, incred="max")
        e_inc = envelopes(fw_inc)["ROBUST"][0]
        hbo = {z: math.sqrt(Hz2(1 / (1 + z))) / math.sqrt((OMB) * (1 + z)**3 + OMR * (1 + z)**4 + (1 - OMB - OMR)) for z in (300, 600, 1000)}
        a1_noext = S * interp_row(dict(func=None, anchors=ROWS["A1"]["anchors"][:-1]), MGRID)
        stdN, fwN, _ = build(a0, a1_ext=False)
        eSN, eFN = envelopes(stdN)["ROBUST"], envelopes(fwN)["ROBUST"]
        fo["sensitivity_no_A1_extrapolation_ROBUST"] = {str(M0): dict(STD=[at(M0, eSN[0]), eSN[1][int(np.argmin(abs(LOGM - math.log10(M0))))]],
                                                                       FW=[at(M0, eFN[0]), eFN[1][int(np.argmin(abs(LOGM - math.log10(M0))))]]) for M0 in TABLE_M}
        P("sensitivity (not scored): ROBUST without A1's compiler extrapolation above 3651 Msun, STD -> FW (dominant): " + ", ".join(
            f"{M0:.0e}:{fmt(v['STD'][0])}({v['STD'][1]})->{fmt(v['FW'][0])}({v['FW'][1]})" for M0, v in zip(TABLE_M, fo["sensitivity_no_A1_extrapolation_ROBUST"].values())))
        fo["sensitivity"] = dict(incredulity_max_rule_ROBUST={str(M0): at(M0, e_inc) for M0 in TABLE_M},
                                 baryon_only_background_H_std_over_H_bo=hbo,
                                 A1_without_compiler_extrapolation_STD={str(M0): at(M0, a1_noext) for M0 in TABLE_M},
                                 D4_alt_reading_spheroid_medium_factor=float(1 / math.sqrt(d4i["nu"])))
        P("sensitivity (not scored): incredulity max() rule ROBUST FW " + ", ".join(f"{M0:.0e}:{fmt(at(M0, e_inc))}" for M0 in TABLE_M))
        P("  baryon-only background H_std/H_bo at z=300,600,1000: " + ", ".join(f"{v:.3f}" for v in hbo.values()) + " (energy injection per Hubble time up by this; accretion f_max down by it)")
        # FW-RAR
        frar = solve_F(0.2589, MW_MBT, 1.0, lambda F: 30.0 / rvir(MW_MBT, F) * MW_MBT / MW_MBT)
        fo["FW_RAR_fb_max"] = frar
        P(f"FW-RAR (reported only, PB3 territory): f_b <= {frar:.3g} keeps MW outer g within 0.05 dex (mass independent)")
        # MUTATE
        _, fwM1, _ = build(a0, planted=True)
        stdM1 = {**std, "PL": np.where((MGRID >= 1e3) & (MGRID <= 1e4), S * 1e-6, np.inf)}
        eS1, eF1 = envelopes(stdM1)["ROBUST"][0], envelopes(fwM1)["ROBUST"][0]
        m1 = all(at(m, eS1) <= S * 1e-6 * 1.0000001 and at(m, eF1) <= S * 1e-6 * 1.0000001 and at(m, eF1) < 1e-4 for m in (1e3, 3e3, 1e4)) \
            and at(1e3, envF["ROBUST"][0]) != at(1e3, eF1)
        stdM2, fwM2, _ = build(a0, mods=False)
        d2 = max(float(np.nanmax(np.abs(np.where(np.isfinite(stdM2[k]), fwM2[k] - stdM2[k], 0)))) for k in stdM2)
        same_inf = all(np.array_equal(np.isfinite(stdM2[k]), np.isfinite(fwM2[k])) for k in stdM2)
        m2 = d2 == 0.0 and same_inf
        _, fwM3, _ = build(a0, m3=True)
        d3 = 0.0
        for k in ("D1", "D2", "D3", "D4", "L1", "L2", "X1"):
            msk = np.isfinite(std[k])
            if not np.array_equal(msk, np.isfinite(fwM3[k])):
                d3 = float("inf")
            else:
                d3 = max(d3, float(np.max(np.abs(fwM3[k][msk] / std[k][msk] - 1))) if msk.any() else d3)
        m3 = d3 <= 1e-12
        fo["mutate"] = dict(M1_planted_moves_and_closes=m1, M2_mods_off_max_diff=d2, M2_pass=m2, M3_max_rel_diff=d3, M3_pass=m3)
        P(f"MUTATE: M1 planted bound {'BITES' if m1 else 'FAILS TO BITE'}; M2 mods-off max|FW-STD| = {d2} {'PASS' if m2 else 'FAIL'}; M3 normalised halo max rel diff {d3:.2e} {'PASS' if m3 else 'FAIL'}")
        ok_all &= m1 and m2 and m3
        res["footings"][fname] = fo
    res["exit_ok"] = bool(ok_all)
    P(f"\nchecks: {'ALL PASS' if ok_all else 'AT LEAST ONE CHECK FAILS (see KA1/KA3/MUTATE lines)'}; exit {0 if ok_all else 1}")
    print("\n".join(lines))

    def clean(o):
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, (np.floating, float)):
            return None if not np.isfinite(o) else float(o)
        if isinstance(o, np.bool_):
            return bool(o)
        return o
    with open(__file__.replace("pb2_fmax.py", "pb2_fmax_results.json"), "w") as fh:
        json.dump(clean(res), fh, indent=1)
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
