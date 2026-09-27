#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR32_common.py -- shared machinery for review lane XR32 (does the chain's late-time dark-fluid conversion lower the
weak-lensing S8 by the right amount, and does it keep CMB lensing, cluster counts, RSD and sum m_nu consistent?).

Loaded by XR32_matter_power.py, XR32_survey_s8.py and XR32_consistency.py.  Read-only on every other file:
  * L357's head (L319's validated two-component linear solver, and L357's halo-model escape function esc()) is exec'd
    from its committed text, unedited; a component-returning copy of L319's solve() is made by one string substitution
    of its return line (the recombination is checked bit-for-bit against run());
  * XR19's conversion histories are rebuilt exactly as XR19_web_runaway.py builds them, from its results JSON (on disk,
    UNCOMMITTED when this lane ran); FP10 A8's web bracket from FP10's committed results JSON;
  * GP0's observed bound baryons (the MOND phantom's source) are imported; nu_mono is BK1's committed table (XC4 splice);
  * the published survey inputs are read locally: DES Y3's official 2pt file (n(z), xi+-, covariance) and the KiDS-1000
    DR4.1 gold weak-lensing catalogue (Z_B, Z_B_MIN, Z_B_MAX, weight) for the KiDS-1000 n(z) shapes.
Normalisation: Planck 2018 (TT,TE,EE+lowE+lensing posterior means, sum m_nu = 0.06 eV, one massive state).  This is an
ASSUMPTION pending XR26 (whether the chain's early universe is LCDM).
No constant is added.  kappa = 1/2 does not enter.  a0 enters only through the phantom stand-in (both footings).
"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
os.environ["OMP_NUM_THREADS"] = "2"                                    # CAMB's OpenMP: at most two threads
import sys, io, json, math, time, contextlib, warnings
import numpy as np
from scipy import special, interpolate, optimize
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
_trap = getattr(np, "trapezoid", None) or np.trapz

# ================================================================================================ constants and inputs
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}                    # FP0's footings, m/s^2
L_STANDIN = 1.7                                                       # Mpc (physical): H_Y's z = 0 band-pass length
L_LAMBDA, OL0 = 2.46, 0.6847                                          # FP9 H_Y: L(z) = L_Lambda Omega_L(z) (n = 2)
G_SI, MSUN, MPC_M, C_KMS = 6.67430e-11, 1.98892e30, 3.0856775814913673e22, 299792.458
P18 = dict(H0=67.36, ombh2=0.02237, omch2=0.1200, mnu=0.06, ns=0.9649, As=math.exp(3.044) * 1e-10, tau=0.0544)
P18_QUOTED = dict(S8=(0.832, 0.013), sigma8=(0.8111, 0.0060), Om=(0.3153, 0.0073))   # Planck 2018 VI, Table 2
H_P = P18["H0"] / 100.0

# published values (value, +err, -err): read from the papers' abstracts/tables during this lane
PUB_WL = {
    "KiDS-1000 xi+- (Asgari+21 Table 3, best fit+PJ-HPD)": (0.764, 0.018, 0.017),
    "KiDS-1000 COSEBIs (Asgari+21 fiducial)": (0.759, 0.024, 0.021),
    "KiDS-Legacy (Wright+25)": (0.815, 0.016, 0.021),
    "DES Y3 (Amon+22/Secco+22 fiducial)": (0.759, 0.025, 0.023),
    "DES Y3 (Amon+22/Secco+22 LCDM-optimised)": (0.772, 0.018, 0.017),
    "HSC Y3 (Li+23 xi+-)": (0.769, 0.031, 0.034),
    "HSC Y3 (Dalal+23 C_ell)": (0.776, 0.032, 0.033),
}
PUB_OTHER = {
    "ACT DR6 A_lens vs Planck18 LCDM (Qu+24)": (1.013, 0.023),
    "ACT DR6 + Planck lensing + BAO sigma8 (Madhavacheril+24)": (0.812, 0.013),
    "ACT DR6 + Planck lensing + BAO S8 (Madhavacheril+24)": (0.831, 0.023),
    "eRASS1 clusters S8 (Ghirardini+24)": (0.86, 0.01),
    "eRASS1 clusters sigma8 (Ghirardini+24)": (0.88, 0.02),
    "SPT clusters S8 (Bocquet+24)": (0.795, 0.029),
    "SPT clusters sigma8 (Bocquet+24)": (0.817, 0.026),
    "DESI DR1 FS+BAO sigma8 (DESI 2024 VII)": (0.842, 0.034),
    "DESI DR2 BAO+CMB sum m_nu 95% upper (DESI DR2 II)": (0.0642, None),
    "DESI DR2 BAO+CMB sigma(sum m_nu) (Elbers+25)": (0.020, None),
    "DESI DR2 BAO+CMB sigma(sum m_nu,eff) (Elbers+25)": (0.053, None),
}
# DES Y3 LCDM-optimised scale cuts (cosmosis-standard-library examples/des-y3-LCDM-optimised-scale-cuts.ini), arcmin
DES_CUTS = {"xip": {(1, 1): 2.475, (1, 2): 2.475, (1, 3): 3.116, (1, 4): 2.475, (2, 2): 3.923, (2, 3): 4.938, (2, 4): 4.938,
                    (3, 3): 3.923, (3, 4): 4.938, (4, 4): 3.923},
            "xim": {(1, 1): 24.750, (1, 2): 19.660, (1, 3): 24.750, (1, 4): 19.660, (2, 2): 31.158, (2, 3): 39.226,
                    (2, 4): 39.226, (3, 3): 49.383, (3, 4): 49.383, (4, 4): 39.226}}
DES_M = [-0.0063, -0.0198, -0.0241, -0.0369]                          # DES Y3 shear-calibration prior means (real-data control only)
# KiDS-1000 (Asgari+21 Table 1 and Table A.1): Z_B edges, n_eff [arcmin^-2], sigma_e, SOM n(z) mean and std
KIDS = dict(edges=[(0.1, 0.3), (0.3, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.2)], neff=[0.62, 1.18, 1.85, 1.26, 1.31],
            sige=[0.27, 0.26, 0.27, 0.25, 0.27], zmean=[0.26, 0.40, 0.56, 0.79, 0.98], zstd=[0.16, 0.16, 0.20, 0.16, 0.25],
            area_deg2=777.4, theta=(0.5, 300.0, 9), xim_min=4.0)
DES_FITS = os.path.join(REPO, "deepseek_push", "data2", "des_y3_2pt_redmagic.fits")
KIDS_CAT = os.path.join(REPO, "real_research", "data", "lensing_rar", "KiDS_DR4.1_SOM_gold_WL_cat.fits")
C1RHO = 0.0134                                                        # NLA: C1 rho_crit (Bridle & King 2007)


class Log:
    """print to stdout and to the script's own .out file."""
    def __init__(self, path):
        self.f = open(path, "w")

    def __call__(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True); self.f.write(s + "\n"); self.f.flush()


def quiet_exec(src, ns):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src, ns)


# ================================================================================================ the record's machinery
P19 = os.path.join(REPO, "real_research", "dark_sector_2026", "L319_lambda_triggered_kicked_decay.py")
P57 = os.path.join(REPO, "real_research", "dark_sector_2026", "L357_virialization_triggered_carrier.py")
_MARK19 = "# ============================================================================================ controls"
_MARK57 = "# ================================================================================ L321 retention machinery (as L354)"
_REC = {}


def record():
    """L357's head (which execs L319's head) with the loaded lane's MUTATE forced off; plus solve_comp."""
    if _REC: return _REC
    src = open(P57).read(); assert src.count(_MARK57) == 1
    head = src.split(_MARK57)[0].replace('P(__doc__.split("METHOD")[0].strip())', "pass")
    ns = {"__name__": "l357", "__file__": P57}
    saved = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    try:
        quiet_exec(head, ns)
    finally:
        if saved is None: os.environ.pop("MUTATE", None)
        else: os.environ["MUTATE"] = saved
    assert ns["MUTATE"] is False
    G19 = ns["G19"]
    s19 = open(P19).read().split(_MARK19)[0]
    i, j = s19.index("def solve(k, surv, vk_kms):"), s19.index("def run(surv, vk):")
    fsrc = s19[i:j]
    old = "    return (rho_cold * dc + rho_d * dd) / (rho_cold + rho_d)\n"
    assert fsrc.count(old) == 1
    fsrc = fsrc.replace("def solve(k, surv, vk_kms):", "def solve_comp(k, surv, vk_kms):").replace(old, "    return dc, dd, rho_cold, rho_d\n")
    exec(fsrc, G19)
    _REC.update(ns=ns, G19=G19, run=G19["run"], solve_comp=G19["solve_comp"], a_grid=G19["a_grid"], K_H=G19["K_H"],
                N_A=G19["N_A"], T2f=G19["T2"], S8_of=G19["S8_of"], LC=ns["LC"], S8_LCDM=ns["S8_LCDM"], esc=ns["esc"],
                c_dm14=ns["c_dm14"], mfn57=ns["mfn"], MH57=ns["MH"], h19=G19["h"], Om19=G19["Om"])
    return _REC


def run_comp(S, vk):
    """L319's solve for every k, with the components: delta_cold, delta_daughter (44 x N_A), rho_cold, rho_d (N_A);
    the total recombined with L319's own expression (bit-identical to run())."""
    R = record(); dc, dd = [], []
    for k in R["G19"]["K"]:
        c_, d_, rc, rd = R["solve_comp"](k, S, vk); dc.append(c_); dd.append(d_)
    dc, dd = np.array(dc), np.array(dd)
    tot = (rc * dc + rd * dd) / (rc + rd)
    return dict(dc=dc, dd=dd, rc=rc, rd=rd, tot=tot)


# ================================================================================================ conversion histories
XR19_JSON = os.path.join(HERE, "XR19_web_runaway_results.json")
FP10_JSON = os.path.join(REPO, "real_research", "derivation_chain_2026", "FP10_internal_splitting_dark_sector_results.json")
ZS19 = [6.0, 5.0, 4.0, 3.5, 3.0, 2.75, 2.5, 2.25, 2.0, 1.75, 1.5, 1.25, 1.0, 0.75, 0.5, 0.25, 0.0]
ZG57 = np.array([0, 0.1, 0.25, 0.4, 0.6, 0.8, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4, 5, 6, 8, 10, 12, 15, 20, 30])
_X19 = {}


def xr19():
    if not _X19: _X19.update(json.load(open(XR19_JSON))["numbers"])
    return _X19


def fh_of(lab):
    d = xr19()["B"][lab]
    zz = np.array(sorted(float(k) for k in d))
    FF = np.array([d[str(z)][0] for z in zz]); Fb = np.array([d[str(z)][1] for z in zz])
    return (lambda z: float(np.interp(z, zz, FF))), (lambda z: float(np.interp(z, zz, Fb))), zz


def fesc_hist(runkey):
    """XR19_web_runaway.py's Fesc_hist(runkey), rebuilt from its JSON: F_esc = F_b,esc + (F_tot - F_halo), monotone."""
    X = xr19(); lab = X["runs"][runkey]["kw"].get("fh_lab", "nominal 5.31")
    Fh, Fb, _ = fh_of(lab)
    FT = {float(k): v for k, v in X["F_tot"][runkey].items()}
    zs = np.array(ZS19[::-1])
    fe = np.array([min(1.0, Fb(z) + (FT[z] - Fh(z))) for z in zs])
    fe = np.maximum.accumulate(fe[::-1])[::-1]
    zz = np.concatenate([zs, [8.0, 10.0, 15.0]]); ff = np.concatenate([fe, [Fb(8.0), Fb(10.0), Fb(15.0)]])
    o = np.argsort(zz)
    return zz[o], ff[o]


def halo_only_hist():
    """XR19's 'halo only (nominal)' history: F_b,esc of the nominal budget."""
    Fh, Fb, zz = fh_of("nominal 5.31")
    return zz, np.array([Fb(z) for z in zz])


def S_of(Fz):
    a = record()["a_grid"]
    return np.clip(1.0 - np.interp(1 / a - 1, Fz[0], Fz[1], right=0.0), 0.0, 1.0)


def fp10_a8_S(zw):
    """FP10 A8's maximal web bracket from FP10's committed budget (v_k 600, K_MID): S = 1 - F_b with F_b = 1 below z_web."""
    Fbc = np.array(json.load(open(FP10_JSON))["numbers"]["A6"]["budget"]["600|185"]["Fb"])
    Fw = np.where(ZG57 <= zw, 1.0, Fbc)
    a = record()["a_grid"]
    return 1 - np.interp(1 / a - 1, ZG57, Fw, right=0.0)


# (label, XR19 run key or special, kick used in the solver)
HISTORIES = [("halo only", "HALO", 600.0), ("nominal (dt0 5.31)", "nominal", 600.0), ("most conservative", "most conservative", 600.0),
             ("pump s = 1", "pump s = 1", 600.0), ("dt0 7.54 (forest floor)", "dt0 forest floor 7.54", 600.0),
             ("dt0 14.6 (canonical top)", "dt0 canonical top+up 14.6", 600.0), ("dt0 22.8 (alt top)", "dt0 alt top+up 22.8", 600.0),
             ("dt0 25 (FK1 upper)", "dt0 FK1 upper 25", 600.0), ("v_k 575", "v_k 575", 575.0), ("v_k 650", "v_k 650", 650.0)]
XR19_X_KEYS = {"halo only": "halo only (nominal)", "nominal (dt0 5.31)": "nominal", "most conservative": "most conservative",
               "pump s = 1": "pump s = 1", "dt0 14.6 (canonical top)": "dt0 canonical top+up 14.6",
               "dt0 22.8 (alt top)": "dt0 alt top+up 22.8", "dt0 25 (FK1 upper)": "dt0 FK1 upper 25"}
FOOT_HIST = {"canonical": ("dt0 7.54 (forest floor)", "dt0 14.6 (canonical top)"), "alt": ("dt0 7.54 (forest floor)", "dt0 22.8 (alt top)")}


def history(key, mutate=False):
    """(z, F_esc) of a named history; MUTATE: conversion switched off (F_esc = 0 at every z)."""
    if key == "HALO": zz, ff = halo_only_hist()
    else: zz, ff = fesc_hist(key)
    if mutate: ff = np.zeros_like(ff)
    return zz, ff


def sigma_d(Fz, vk, z):
    """1D velocity dispersion of the free daughters at z: cohorts born at z_c > z at v_k (web daughters leave at v_k;
    halo escapees climb out slower, so this is an upper bound on the speed), Hubble-cooled as 1/a."""
    zc = np.linspace(z, 15.0, 3001); F = np.interp(zc, Fz[0], Fz[1])
    w = -np.diff(F); zm = 0.5 * (zc[1:] + zc[:-1])
    if w.sum() <= 0: return vk / math.sqrt(3.0)
    v = vk * (1 + z) / (1 + zm)
    return math.sqrt(float(np.sum(w * v * v) / w.sum()) / 3.0)


# ================================================================================================ transfers on (k, z)
class Transfer:
    """T^2(k, z) of the chain's linear solution relative to the solver's own LCDM (total, cold, daughters, cross);
    k in h/Mpc, 44 solver wavenumbers (0.02-30); below 0.02 the suppression fades as k^2, above 30 it is held."""
    def __init__(self, comp, LC):
        R = record(); self.kh = np.array(R["K_H"]); self.a = np.array(R["a_grid"]); self.lnk = np.log(self.kh)
        self.lna = np.log(self.a)
        L2 = LC ** 2
        self.t2 = {"tot": comp["tot"] ** 2 / L2, "cc": comp["dc"] ** 2 / L2, "dd": comp["dd"] ** 2 / L2, "cd": comp["dc"] * comp["dd"] / L2}
        self.fcold = comp["rc"] / (comp["rc"] + comp["rd"])
        self.tot, self.LC = comp["tot"], LC

    def __call__(self, k, z, which="tot"):
        k = np.atleast_1d(np.asarray(k, float)); lna = -math.log1p(z)
        T = self.t2[which]
        j = np.clip(np.searchsorted(self.lna, lna) - 1, 0, len(self.lna) - 2); w = (lna - self.lna[j]) / (self.lna[j + 1] - self.lna[j])
        col = (1 - w) * T[:, j] + w * T[:, j + 1]
        lk = np.log(np.clip(k, self.kh[0], self.kh[-1]))
        out = np.interp(lk, self.lnk, col)
        lo = k < self.kh[0]
        if which in ("tot", "cc"):
            out = np.where(lo, 1 - (1 - col[0]) * (k / self.kh[0]) ** 2, out)
        return out

    def fcold_z(self, z):
        return float(np.interp(-math.log1p(z), self.lna, self.fcold))

    def growth_rate(self, kq, z, which="tot"):
        """f = d ln delta / d ln a at the solver wavenumber nearest kq (the chain), and the solver's LCDM."""
        i = int(np.argmin(np.abs(self.kh - kq)))
        d = self.tot[i] if which == "tot" else self.LC[i]
        fl = np.gradient(np.log(np.abs(d)), self.lna)
        return float(np.interp(-math.log1p(z), self.lna, fl)), float(self.kh[i])


# ================================================================================================ CAMB
import camb


def camb_setup(Om=None, mnu=0.06, nmass=1, zs=None, kmax=100.0, nl="mead2020", A_bary=None, As=None, ns=None, lensing=False,
               theta=None):
    pars = camb.CAMBparams()
    h = H_P
    kw = dict(ombh2=P18["ombh2"], omch2=P18["omch2"], mnu=mnu, num_massive_neutrinos=nmass, omk=0, tau=P18["tau"])
    if theta is not None:
        pars.set_cosmology(cosmomc_theta=theta, **kw)
    else:
        pars.set_cosmology(H0=P18["H0"], **kw)
        if Om is not None:
            omnu = pars.omnuh2
            pars.set_cosmology(H0=P18["H0"], ombh2=P18["ombh2"], omch2=Om * h * h - P18["ombh2"] - omnu, mnu=mnu,
                               num_massive_neutrinos=nmass, omk=0, tau=P18["tau"])
    pars.InitPower.set_params(As=P18["As"] if As is None else As, ns=P18["ns"] if ns is None else ns)
    if zs is not None:
        pars.set_matter_power(redshifts=sorted(list(zs), reverse=True), kmax=kmax, nonlinear=True)
    pars.NonLinear = camb.model.NonLinear_both if lensing else camb.model.NonLinear_pk
    if nl == "mead2016":
        pars.NonLinearModel.set_params(halofit_version="mead2016", HMCode_A_baryon=A_bary, HMCode_eta_baryon=0.98 - 0.12 * A_bary)
    else:
        pars.NonLinearModel.set_params(halofit_version=nl)
    pars.WantCls = lensing; pars.DoLensing = lensing
    if lensing:
        pars.set_for_lmax(2500, lens_potential_accuracy=1)
    return pars


def om_of(res):
    p = res.Params
    return (p.ombh2 + p.omch2 + p.omnuh2) / (p.H0 / 100) ** 2


class Cosmo:
    """one CAMB cosmology: linear and nonlinear P(k, z) tables (h/Mpc units), distances, sigma8(z), growth D(z)."""
    def __init__(self, res, zs):
        self.res = res; self.Om = om_of(res); self.h = res.Params.H0 / 100
        kh, z, pl = res.get_linear_matter_power_spectrum(hubble_units=True, k_hunit=True)
        kh2, z2, pn = res.get_nonlinear_matter_power_spectrum(hubble_units=True, k_hunit=True)
        self.kh, self.z = kh, np.array(z); self.lnk = np.log(kh)
        self.lpl, self.lpn = np.log(pl), np.log(pn)
        self._spl = interpolate.RectBivariateSpline(self.z, self.lnk, self.lpn, kx=3, ky=3)
        self._spll = interpolate.RectBivariateSpline(self.z, self.lnk, self.lpl, kx=3, ky=3)
        self.slope_hi = (self.lpn[:, -1] - self.lpn[:, -4]) / (self.lnk[-1] - self.lnk[-4])

    def P(self, k, z, lin=False):
        """P(k, z) with k (array) in h/Mpc at one z; power-law continuation beyond the table's k range."""
        k = np.atleast_1d(k); lk = np.log(k)
        spl = self._spll if lin else self._spl
        lkc = np.clip(lk, self.lnk[0], self.lnk[-1])
        out = spl(z, lkc, grid=False) if np.ndim(z) else spl(np.full_like(lkc, z), lkc, grid=False)
        hi = lk > self.lnk[-1]
        if np.any(hi):
            sl = np.interp(z, self.z, self.slope_hi) if not lin else -3.0
            out = np.where(hi, out + sl * (lk - self.lnk[-1]), out)
        lo = lk < self.lnk[0]
        if np.any(lo):
            out = np.where(lo, out + P18["ns"] * (lk - self.lnk[0]), out)
        return np.exp(out)

    def chi(self, z):                                                  # comoving distance, Mpc/h
        return np.asarray(self.res.comoving_radial_distance(z)) * self.h

    def Hh(self, z):                                                   # H(z)/c in h/Mpc
        return np.asarray(self.res.hubble_parameter(z)) / C_KMS / self.h

    def D(self, z):
        return np.sqrt(self.P(np.array([0.01]), z, lin=True)[0] / self.P(np.array([0.01]), 0.0, lin=True)[0])


def sigma_R(kh, P, R=8.0):
    x = kh * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return math.sqrt(_trap(kh ** 2 * P * W ** 2, kh) / (2 * math.pi ** 2))


# ================================================================================================ nu_mono (BK1's committed table)
def _h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"): return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def _dh_rar(y, e=1e-6): return (_h_rar(y * (1 + e)) - _h_rar(y * (1 - e))) / (2 * y * e)


_YP = optimize.brentq(lambda y: float(_dh_rar(y)), 1, 5); _HP = float(_h_rar(_YP))
_LYG = np.linspace(-14, 14, 280001); _YG = 10 ** _LYG; _DH = np.maximum(_dh_rar(_YG), 0.05 * _HP / (_YG + _YP))
_HM = float(_h_rar(_YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (_DH[1:] + _DH[:-1]) * np.diff(_YG))])


def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-14); return 1.0 + np.interp(np.log10(y), _LYG, _HM) / y


def nu_rar(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.asarray(y, float))))


# ================================================================================================ the phantom stand-in
_XS = 4.0                                                             # beyond x = r/r_M = 4: g = x - 1/2 + 1/(12x) + O(2e-5)
_XG = np.concatenate([np.geomspace(1e-4, 0.5, 400)[:-1], np.linspace(0.5, _XS, 1500)])
_GX = nu_mono(1.0 / _XG ** 2) - 1.0                                   # M_ph(<r)/M_b as a function of x = r/r_M (y = 1/x^2)


def _j1(x):
    x = np.asarray(x, float); xs = np.where(np.abs(x) < 1e-3, 1.0, x)
    return np.where(np.abs(x) < 1e-3, x / 3 - x ** 3 / 30, np.sin(xs) / xs ** 2 - np.cos(xs) / xs)


def _j0(x):
    x = np.asarray(x, float); xs = np.where(np.abs(x) < 1e-4, 1.0, x)
    return np.where(np.abs(x) < 1e-4, 1 - x * x / 6, np.sin(xs) / xs)


def _tail(kap, a, b):
    """int_a^b (x - 1/2 + 1/(12 x)) kappa j1(kappa x) dx, analytic (a = _XS, b = X_L > a)."""
    kap = np.maximum(kap, 1e-12)
    ua, ub = kap * a, kap * b
    Sa, Sb = special.sici(ua)[0], special.sici(ub)[0]
    t1 = (Sb - np.sin(ub) - Sa + np.sin(ua)) / kap                    # int x kappa j1 = (Si(u) - sin u)/kappa
    t2 = -0.5 * (_j0(ua) - _j0(ub))                                   # int kappa j1 = j0(kappa a) - j0(kappa b)
    Iu = lambda u: 0.5 * (np.cos(u) / u + special.sici(u)[0] - np.sin(u) / u ** 2)   # int j1(u)/u du
    t3 = (kap / 12.0) * (Iu(ub) - Iu(ua))
    return t1 + t2 + t3


def phantom_transform(kc, Mb, rM, XL):
    """rho~_ph(k) / M_b for a point-mass baryon source with nu_mono, band-passed (compensated) at X_L = L/r_M.
    kc: comoving k (h/Mpc) array; rM: comoving MOND radius sqrt(G M_b/a0) in Mpc/h; returns (len(Mb), len(kc)).
    Direct trapezoid on x <= min(X_L, 4) (Delta x <= 0.0023), analytic tail beyond (x - 1/2 + 1/(12x))."""
    out = np.zeros((len(Mb), len(kc)))
    for i in range(len(Mb)):
        kap = np.asarray(kc) * rM[i]
        if XL[i] <= _XS:
            xg = np.concatenate([np.geomspace(1e-4, min(0.5, 0.5 * XL[i]), 400)[:-1], np.linspace(min(0.5, 0.5 * XL[i]), XL[i], 1500)])
            gx = nu_mono(1.0 / xg ** 2) - 1.0
        else:
            xg, gx = _XG, _GX
        f = gx[None, :] * kap[:, None] * _j1(kap[:, None] * xg[None, :])
        out[i] = _trap(f, xg, axis=1)
        if XL[i] > _XS:
            out[i] += _tail(kap, _XS, XL[i])
    return out


# ================================================================================================ halo model
_GP0 = None


def gp0():
    global _GP0
    if _GP0 is None:
        sys.path.insert(0, os.path.join(REPO, "real_research", "generated_phantom_2026"))
        with contextlib.redirect_stdout(io.StringIO()):
            import GP0_bound_baryon_census as g
        _GP0 = g
    return _GP0


def nfw_uk(kc, rs, c):
    """normalised Fourier transform of an NFW truncated at c r_s; kc (Nk,), rs, c (NM,) -> (NM, Nk)."""
    x = np.outer(rs, kc); cc = c[:, None]
    si1, ci1 = special.sici((1 + cc) * x); si0, ci0 = special.sici(x)
    m = np.log1p(c) - c / (1 + c)
    return (np.sin(x) * (si1 - si0) - np.sin(cc * x) / ((1 + cc) * x) + np.cos(x) * (ci1 - ci0)) / m[:, None]


class HaloModel:
    """Sheth-Tormen + NFW (Duffy+08 c_vir, Bryan-Norman Delta_vir) in h units; the chain's response
         R(k, z) = [P_lin,chain (I_1 + B_ph)^2 + P_1h,chain] / [P_lin,LCDM I_1^2 + P_1h,LCDM],
    P_1h = int n (m_c u + rho~_ph)^2 / rho_bar^2 x HMcode-2020's 1-halo damping; I_1 the halo-matter 2-halo profile factor
    (normalised to 1 at k -> 0, LCDM's for both); B_ph the phantom's 2-halo factor (compensated: -> 0 as k^2)."""
    def __init__(self, cosmo, kc, lgM=np.linspace(6.0, 16.0, 201)):
        self.c = cosmo; self.Om = cosmo.Om; self.h = cosmo.h; self.kc = np.asarray(kc)
        self.M = 10 ** lgM; self.dlnM = (lgM[1] - lgM[0]) * math.log(10)
        self.rho = 2.775e11 * self.Om                                  # (Msun/h)(Mpc/h)^-3, comoving
        self.R = (3 * self.M / (4 * math.pi * self.rho)) ** (1 / 3)
        self.kk = np.geomspace(1e-4, 300.0, 2500)
        x = np.outer(self.R, self.kk); self.W2 = (3 * (np.sin(x) - x * np.cos(x)) / x ** 3) ** 2
        fnu = cosmo.res.Params.omnuh2 / (self.Om * self.h ** 2)
        self.fnu = fnu; self.fb = P18["ombh2"] / (self.Om * self.h ** 2); self.fc = 1 - fnu - self.fb

    def sigma(self, Pk):
        return np.sqrt(_trap(self.kk ** 2 * Pk * self.W2, self.kk, axis=1) / (2 * math.pi ** 2))

    def mf(self, sig):
        nu = 1.686 / sig; qn = 0.707 * nu * nu
        nuf = 0.3222 * math.sqrt(2 * 0.707 / math.pi) * nu * (1 + qn ** -0.3) * np.exp(-qn / 2)
        dln = np.gradient(np.log(nu), np.log(self.M))
        n = self.rho / self.M * nuf * dln                             # dn/dlnM
        b = 1 + (qn - 1) / 1.686 + 2 * 0.3 / (1.686 * (1 + qn ** 0.3))
        return n, b

    def profiles(self, z):
        Omz = self.Om * (1 + z) ** 3 / (self.Om * (1 + z) ** 3 + 1 - self.Om)
        xx = Omz - 1; Dvm = (18 * math.pi ** 2 + 82 * xx - 39 * xx * xx) / Omz
        rvir = (3 * self.M / (4 * math.pi * Dvm * self.rho)) ** (1 / 3)     # comoving Mpc/h
        cv = 7.85 * (self.M / 2e12) ** -0.081 * (1 + z) ** -0.71
        return rvir, cv, Dvm

    def base(self, z, Plin_kk, Plin_kc):
        """LCDM pieces at z: n, b, u(k|M), I_1(k), sigma8(z), the 1-halo damping."""
        sig = self.sigma(Plin_kk); n, b = self.mf(sig)
        rvir, cv, Dvm = self.profiles(z); u = nfw_uk(self.kc, rvir / cv, cv)
        wb = n * b * self.M / self.rho * self.dlnM
        I1 = wb @ u + (1 - wb.sum())
        s8 = sigma_R(self.kk, Plin_kk)
        ks = 0.05618 * s8 ** -1.013; damp = (self.kc / ks) ** 4 / (1 + (self.kc / ks) ** 4)
        return dict(n=n, b=b, u=u, I1=I1, s8=s8, damp=damp, rvir=rvir, cv=cv, Dvm=Dvm, sig=sig)

    def p1h(self, B, mass_frac=None, phantom=None, n=None):
        n = B["n"] if n is None else n
        mc = self.M * (1 - self.fnu if mass_frac is None else mass_frac)
        T = mc[:, None] * B["u"] + (0.0 if phantom is None else phantom)
        return (n * self.dlnM) @ (T ** 2) / self.rho ** 2 * B["damp"]

    def bph(self, B, phantom, n=None, b=None):
        n = B["n"] if n is None else n; b = B["b"] if b is None else b
        return (n * b * self.dlnM) @ phantom / self.rho


# ------------------------------------------------------------------------------------------------ content readings
def ret_inplace(M, z, vk):
    """1 - L357's esc(): the whole halo converts (trigger radius = r200), isotropic kick v_k on a Maxwellian parent in
    the truncated NFW (Dutton-Maccio c); mass-weighted retained fraction, on L357's grid, interpolated in log M."""
    R = record(); ns = R["ns"]
    MH = ns["MH"]; cs = ns["c_dm14"](MH, z); dch = 200 / 3 * cs ** 3 / ns["mfn"](cs)
    fe = ns["esc"](z, "cleared", vk, cs.copy(), cs, dch, np.zeros_like(cs))
    return np.interp(np.log(M), np.log(MH), 1 - np.clip(fe, 0, 1))


def cap_tg(M, z, sig_d, frac, hm, rvir, cv):
    """phase-space (Tremaine-Gunn) maximal capture of the free daughters: within r_vir the daughter density cannot exceed
    f_max (4 pi/3) v_esc(r)^3, f_max = n_bar/(2 pi sigma_d^2)^(3/2) (Maxwellian proxy); relative to the carrier's
    fair NFW share.  v_esc from the truncated-NFW potential of the halo's CURRENT mass M x frac (Newtonian: the dark
    state is kernel-invisible)."""
    a = 1 / (1 + z)
    s = np.geomspace(1e-3, 1.0, 200)
    rv = rvir * a / hm.h * MPC_M                                      # physical r_vir, m
    Mk = M * frac / hm.h * MSUN
    V2 = G_SI * Mk / rv                                               # m^2/s^2
    mc = np.log1p(cv) - cv / (1 + cv)
    x = cv[:, None] * s[None, :]
    phi = np.log1p(x) / (s[None, :] * mc[:, None]) + (1 - np.log1p(cv) / mc)[:, None]
    vesc = np.sqrt(2 * V2[:, None] * phi) / 1e3                        # km/s
    rs = rv / cv
    Mfair = M / hm.h * MSUN                                           # the fair share is the LCDM-equivalent halo's
    rho_fair = (Mfair / (4 * math.pi * rs ** 3 * mc))[:, None] / (x * (1 + x) ** 2)   # kg/m^3, total-matter NFW
    rhobar = 2.775e11 * hm.Om * (1 + z) ** 3 * hm.h ** 2 * MSUN / MPC_M ** 3        # kg/m^3, physical mean matter
    rho_tg = rhobar * 0.26596 * (vesc / sig_d) ** 3                  # (4 pi/3)/(2 pi)^(3/2) = 0.26596
    w = s ** 3                                                        # d(volume) per d ln s
    return _trap(np.minimum(rho_fair, rho_tg) * w, np.log(s), axis=1) / _trap(rho_fair * w, np.log(s), axis=1)


def ret_pm_l388():
    """L388's committed retention by halo mass (v_k 600, pooled; galaxies at its fixed-cell clearing), as MS3's ret_L388."""
    L388 = json.load(open(os.path.join(REPO, "real_research", "dark_sector_2026", "L388_linear_gate_pooled_results.json")))["numbers"]
    rb = L388["retention_by_mass"]["v600"]
    cen = {"6.0e+13-1.0e+14": 7.75e13, "1.0e+14-1.5e+14": 1.22e14, "1.5e+14-2.5e+14": 1.94e14, "2.5e+14-1.0e+17": 5.0e14}
    lx = [math.log10(1e13)] + [math.log10(cen[k_]) for k_ in cen]
    ly = [float(L388["table"]["pooled"]["v600"]["clear_fixed"])] + [rb[k_][0] for k_ in cen]
    return lambda Msun: np.interp(np.log10(Msun), lx, ly, left=ly[0], right=ly[-1])


READINGS = ("phase-space recapture (primary)", "in place", "no recapture", "PM (L388)")


def content(reading, M, z, Fesc_z, sig_d, vk, hm, rvir, cv, mutate=False):
    """retained carrier fraction ret(M, z) and the halo's mass fraction f_b + f_c ret (per LCDM-equivalent mass)."""
    if mutate:
        ret = np.ones_like(M)
    elif reading == "in place":
        ret = ret_inplace(M, z, vk)
    elif reading == "no recapture":
        ret = np.minimum(ret_inplace(M, z, vk), 1 - Fesc_z)
    elif reading == "PM (L388)":
        ret = ret_pm_l388()(M / hm.h)
    else:
        ri = ret_inplace(M, z, vk); ret = ri.copy()
        for _ in range(3):
            frac = hm.fb + hm.fc * ret
            cap = cap_tg(M, z, sig_d, frac, hm, rvir, cv)
            ret = (1 - Fesc_z) * ri + Fesc_z * cap
    return np.clip(ret, 0, 1), hm.fb + hm.fc * np.clip(ret, 0, 1)


def phantom_iso(kc, rM):
    """rho~_ph,iso(k)/M_b of the UNtruncated isolated nu_mono phantom (density ~ r^-2 to infinity; Abel-convergent):
    int_0^xs g kappa j1 + g(xs) j0(kappa xs) + int_xs^inf (1 - 1/(12 x^2)) j0(kappa x) dx, the last analytic."""
    out = np.zeros((len(rM), len(kc)))
    gs = float(nu_mono(1.0 / _XS ** 2) - 1.0)
    for i in range(len(rM)):
        kap = np.maximum(np.asarray(kc) * rM[i], 1e-12)
        f = _GX[None, :] * kap[:, None] * _j1(kap[:, None] * _XG[None, :])
        U = kap * _XS; SiU = special.sici(U)[0]
        tail = (math.pi / 2 - SiU) / kap - (kap / 12.0) * (-math.pi / 4 + np.sin(U) / (2 * U * U) + np.cos(U) / (2 * U) + SiU / 2)
        out[i] = _trap(f, _XG, axis=1) + gs * _j0(U) + tail
    return out


PH_MRANGE_MSUN = (1e10, 10 ** 15.5)                                   # the record's halo-model phantom range (L363/MS3: LMH 10.0-15.5)


def phantom_rows(hm, z, a0, Lphys, mrange=PH_MRANGE_MSUN, edge="sharp"):
    """rho~_ph(k|M) [Msun/h] for the halos of hm at z inside mrange (Msun; the record's convention -- an isolated-halo sum
    over every dwarf double-counts the band-passed field, which MOND's non-additivity would not): GP0 observed bound
    baryons, nu_mono, band-passed (compensated) at L (physical Mpc)."""
    g = gp0()
    Mb = np.asarray(g.M_bound(hm.M / hm.h, z, "observed"), float) * hm.h        # Msun/h
    Mb = np.where((hm.M / hm.h >= mrange[0]) & (hm.M / hm.h <= mrange[1]), Mb, 0.0)
    a = 1 / (1 + z)
    rM_phys = np.sqrt(G_SI * (Mb / hm.h) * MSUN / a0) / MPC_M                   # Mpc physical
    rM = rM_phys / a * hm.h                                                     # comoving Mpc/h
    XL = Lphys / np.maximum(rM_phys, 1e-30)
    out = np.zeros((len(Mb), len(hm.kc))); on = Mb > 0
    if edge == "sharp":                                               # L363/MS3's convention: truncated, shell at L
        out[on] = Mb[on, None] * phantom_transform(hm.kc, Mb[on], rM[on], XL[on])
    else:                                                             # H_Y's heat-kernel band-pass: x (1 - exp(-k^2 L^2/2))
        Lc = Lphys * (1 + z) * hm.h
        out[on] = Mb[on, None] * phantom_iso(hm.kc, rM[on]) * (1 - np.exp(-(hm.kc * Lc) ** 2 / 2))[None, :]
    return out


# ================================================================================================ Limber and Hankel
class Limber:
    """cosmic-shear C_ell (GG, GI, II per unit A_IA) for tomographic n(z) in one cosmology (flat)."""
    def __init__(self, cosmo, nz_z, nz_list, zmax=4.0, nchi=360, ells=None):
        self.c = cosmo
        zi = np.linspace(1e-3, zmax, 1600); chi_i = cosmo.chi(zi)
        self.chi = np.linspace(chi_i[0], chi_i[-1], nchi); self.z = np.interp(self.chi, chi_i, zi)
        self.a = 1 / (1 + self.z); self.H = cosmo.Hh(self.z)
        pref = 1.5 * cosmo.Om / 2997.92458 ** 2
        zs = np.asarray(nz_z); chis = cosmo.chi(np.maximum(zs, 1e-6))
        self.q, self.p = [], []
        for n in nz_list:
            n = np.asarray(n, float); n = n / _trap(n, zs)
            eff = np.array([_trap(n * np.clip(1 - x / np.maximum(chis, 1e-9), 0, None) * (zs > 0), zs) for x in self.chi])
            self.q.append(pref * self.chi / self.a * eff)
            self.p.append(np.interp(self.z, zs, n) * self.H)
        self.q, self.p = np.array(self.q), np.array(self.p)
        self.ells = np.geomspace(1.0, 2e5, 170) if ells is None else ells
        self.D = np.array([cosmo.D(z) for z in self.z])

    def pk_grid(self, Pfun):
        """P(k = (ell+1/2)/chi, z(chi)) on (ell, chi); Pfun(k array, z) -> array."""
        return np.array([Pfun((self.ells + 0.5) / x, zz) for x, zz in zip(self.chi, self.z)]).T      # (Nell, Nchi)

    def cls(self, Pg, eta=0.0, z0=0.62):
        """C_ell^{GG}, C^{GI}, C^{II} (per unit A_IA and A_IA^2) for all pairs i <= j."""
        F = -C1RHO * self.c.Om / self.D * ((1 + self.z) / (1 + z0)) ** eta
        w = np.gradient(self.chi) / self.chi ** 2
        nb = len(self.q); out = {}
        for i in range(nb):
            for j in range(i, nb):
                gg = Pg @ (self.q[i] * self.q[j] * w)
                gi = Pg @ ((self.q[i] * self.p[j] + self.p[i] * self.q[j]) * F * w)
                ii = Pg @ (self.p[i] * self.p[j] * F * F * w)
                out[(i, j)] = (gg, gi, ii)
        return out


def jbar(ell, lo, hi, kind):
    """bin-averaged (weight theta d theta) J_0 or J_4, theta in radians."""
    th2 = (hi ** 2 - lo ** 2) / 2
    if kind == 0:
        f = lambda t: t * special.j1(ell * t) / ell
    else:
        def f(t):                                                    # F(x) = x J1 - 4 J0 - 12 J2 + 4, F(0) = 0 (one constant)
            x = ell * t
            full = (x * special.j1(x) - 4 * special.j0(x) - 12 * special.jv(2, x) + 4.0) / ell ** 2
            return np.where(x < 0.1, (x ** 6 / 2304.0 - x ** 8 / 153600.0) / ell ** 2, full)
    return (f(hi) - f(lo)) / th2


class Hankel:
    """xi_+-(theta bins) = int d ell ell/(2 pi) Jbar C_ell on a fine log grid; C_ell splined in ln ell (ell C_ell)."""
    def __init__(self, bins_rad, kinds, lmin=1.0, lmax=2e5, n=40000):
        self.lf = np.geomspace(lmin, lmax, n); dl = np.gradient(np.log(self.lf))
        self.Mx = np.array([self.lf ** 2 / (2 * math.pi) * jbar(self.lf, lo, hi, kd) * dl for (lo, hi), kd in zip(bins_rad, kinds)])

    def xi(self, ells, cl):
        """cl: (Nell,) or (Nell, m) -> (Ntheta,) or (Ntheta, m)."""
        cl = np.asarray(cl); two = cl.ndim == 2
        y = ells[:, None] * cl if two else ells * cl
        s = interpolate.CubicSpline(np.log(ells), y, axis=0)
        c = s(np.log(np.clip(self.lf, ells[0], ells[-1])))
        c = c / (self.lf[:, None] if two else self.lf)
        return self.Mx @ c


def arcmin(x): return np.asarray(x) * math.pi / 180 / 60


# ================================================================================================ the surveys
def des_y3():
    from astropy.io import fits
    f = fits.open(DES_FITS)
    nz = f["nz_source"].data; zmid = np.array(nz["Z_MID"]); ns = [np.array(nz[f"BIN{i}"]) for i in range(1, 5)]
    rows = []
    for q in ("xip", "xim"):
        d = f[q].data
        for r in range(len(d)):
            rows.append((q, int(d["BIN1"][r]), int(d["BIN2"][r]), int(d["ANGBIN"][r]), float(d["VALUE"][r]), float(d["ANGLEMIN"][r]),
                         float(d["ANGLEMAX"][r]), float(d["ANG"][r])))
    cov = np.array(f["COVMAT"].data)[:400, :400]
    keep = np.array([r[7] >= DES_CUTS[r[0]][(r[1], r[2])] for r in rows])
    return dict(z=zmid, nz=ns, rows=rows, cov=cov, keep=keep, data=np.array([r[4] for r in rows]))


def kids_nz(zg=np.linspace(0.0, 5.0, 501)):
    """KiDS-1000 n(z): lensfit-weighted stacks of per-galaxy Gaussians N(Z_B, (Z_B_MAX - Z_B_MIN)/2) from the DR4.1 gold
    catalogue, per Z_B bin, then an affine map to Asgari+21 Table A.1's SOM mean and std (iterated after clipping at 0).
    An approximation to the SOM n(z) (not reproducible without the spectroscopic calibration sample)."""
    import fitsio
    h = fitsio.FITS(KIDS_CAT)[1]; n = h.get_nrows(); cols = ["Z_B", "Z_B_MIN", "Z_B_MAX", "weight"]; parts = {c: [] for c in cols}
    for i0 in range(0, n, 2_000_000):
        d = h.read(columns=cols, rows=np.arange(i0, min(n, i0 + 2_000_000)))
        for c in cols: parts[c].append(np.asarray(d[c], np.float64))
    zb, zlo, zhi, w = (np.concatenate(parts[c]) for c in cols)
    sg = np.clip((zhi - zlo) / 2, 0.02, 1.0)
    out, info = [], []
    zc = 0.5 * (zg[1:] + zg[:-1])
    for (lo, hi), mu, sd in zip(KIDS["edges"], KIDS["zmean"], KIDS["zstd"]):
        s = (zb > lo) & (zb <= hi) & (w > 0)
        H, xe, ye = np.histogram2d(zb[s], sg[s], bins=[np.arange(lo, hi + 1e-9, 0.01), np.arange(0.02, 1.0001, 0.01)], weights=w[s])
        xm, ym = 0.5 * (xe[1:] + xe[:-1]), 0.5 * (ye[1:] + ye[:-1])
        pz = np.zeros_like(zc)
        for a_, x_ in enumerate(xm):
            ww = H[a_]
            if ww.sum() <= 0: continue
            pz += (ww[:, None] * np.exp(-0.5 * ((zc[None, :] - x_) / ym[:, None]) ** 2) / ym[:, None]).sum(0)
        pz = np.where(zc > 0, pz, 0); pz /= _trap(pz, zc)
        m0 = _trap(zc * pz, zc); s0 = math.sqrt(_trap((zc - m0) ** 2 * pz, zc))
        mu_e, sd_e = mu, sd
        for _ in range(40):                                           # affine map; re-aim after the clip at z = 0
            zmap = mu_e + (zc - m0) * sd_e / s0
            q = np.interp(zc, zmap, pz, left=0.0, right=0.0)
            q = np.where(zc > 0, q, 0.0); q /= _trap(q, zc)
            mq = _trap(zc * q, zc); sq = math.sqrt(_trap((zc - mq) ** 2 * q, zc))
            if abs(mq - mu) < 1e-5 and abs(sq - sd) < 1e-5: break
            mu_e += mu - mq; sd_e *= sd / sq
        out.append(q)
        info.append(dict(bin=f"{lo}-{hi}", n_gal=int(s.sum()), stack_mean=m0, stack_std=s0, mean=float(_trap(zc * q, zc)),
                         std=float(math.sqrt(_trap((zc - _trap(zc * q, zc)) ** 2 * q, zc))), frac_z_gt_2=float(_trap(q * (zc > 2), zc))))
    return zc, out, info


def kids_bins():
    lo, hi, nb = KIDS["theta"]
    e = np.geomspace(lo, hi, nb + 1)
    return [(e[i], e[i + 1]) for i in range(nb)]


def kids_layout():
    """data-vector layout: for each pair (i <= j): xi+ in all 9 bins, xi- in the bins with lower edge >= 4 arcmin."""
    b = kids_bins(); rows = []
    for i in range(5):
        for j in range(i, 5):
            for t, (lo, hi) in enumerate(b): rows.append(("xip", i + 1, j + 1, t, lo, hi))
            for t, (lo, hi) in enumerate(b):
                if lo >= KIDS["xim_min"]: rows.append(("xim", i + 1, j + 1, t, lo, hi))
    return rows


def gaussian_cov_kids(rows, ells, clgg):
    """Gaussian covariance of xi+- (Joachimi+08 form, E and B shape-noise terms), A_eff = 777.4 deg^2."""
    A = KIDS["area_deg2"] * (math.pi / 180) ** 2
    nsr = [n * (180 * 60 / math.pi) ** 2 for n in KIDS["neff"]]
    N = [s * s / n for s, n in zip(KIDS["sige"], nsr)]
    lf = np.geomspace(1.0, 2e5, 30000); dl = np.gradient(lf)
    C = {}
    for (i, j), v in clgg.items():
        s = interpolate.CubicSpline(np.log(ells), ells * v)
        C[(i, j)] = C[(j, i)] = s(np.log(lf)) / lf
    Jb = {}
    for r in rows:
        key = (r[0], r[4], r[5])
        if key not in Jb: Jb[key] = jbar(lf, arcmin(r[4]), arcmin(r[5]), 0 if r[0] == "xip" else 4)
    nr = len(rows); cov = np.zeros((nr, nr))
    for a_ in range(nr):
        qa, ia, ja, ta, loa, hia = rows[a_]
        for b_ in range(a_, nr):
            qb, ib, jb_, tb, lob, hib = rows[b_]
            i, j, k, l = ia - 1, ja - 1, ib - 1, jb_ - 1
            Cik, Cjl, Cil, Cjk = C[(i, k)], C[(j, l)], C[(i, l)], C[(j, k)]
            Nik, Njl, Nil, Njk = (N[i] if i == k else 0.0), (N[j] if j == l else 0.0), (N[i] if i == l else 0.0), (N[j] if j == k else 0.0)
            integ = Cik * Cjl + Cil * Cjk + Cik * Njl + Nik * Cjl + Cil * Njk + Nil * Cjk
            v = _trap(lf * Jb[(qa, loa, hia)] * Jb[(qb, lob, hib)] * integ, lf) / (2 * math.pi * A)
            if qa == qb and ta == tb:                                  # E + B noise-noise, closure relation
                th = (arcmin(hia) ** 2 - arcmin(loa) ** 2) / 2
                v += 2 * (Nik * Njl + Nil * Njk) / (2 * math.pi * A * th)
            cov[a_, b_] = cov[b_, a_] = v
    return cov


# ================================================================================================ fitting
class TemplateSet:
    """LCDM templates xi_GG, xi_GI(eta), xi_II(eta) on (Om, S8, [A_bary]) grids; cubic interpolation; chi^2 fits."""
    def __init__(self, axes, gg, gi, ii, etas=None):
        self.axes = axes; self.etas = etas
        self.fgg = interpolate.RegularGridInterpolator(axes, gg, method="cubic", bounds_error=False, fill_value=None)
        ax2 = axes + ((np.array(etas),) if etas is not None else ())
        self.fgi = interpolate.RegularGridInterpolator(ax2, gi, method="cubic", bounds_error=False, fill_value=None)
        self.fii = interpolate.RegularGridInterpolator(ax2, ii, method="cubic", bounds_error=False, fill_value=None)

    def model(self, p):
        """p = (Om, S8, A_IA[, A_bary][, eta])."""
        na = len(self.axes)
        x = np.array(p[:2] + ((p[3],) if na == 3 else ()))
        xe = np.concatenate([x, [p[-1]]]) if self.etas is not None else x
        A = p[2]
        return self.fgg(x)[0] + A * self.fgi(xe)[0] + A * A * self.fii(xe)[0]


def fit(ts, data, icov, bounds, starts, fixed_S8=None):
    def chi2(p):
        pp = tuple(p) if fixed_S8 is None else (p[0], fixed_S8) + tuple(p[1:])
        r = data - ts.model(pp); return float(r @ icov @ r)
    best = None
    for s0 in starts:
        x0 = list(s0) if fixed_S8 is None else [s0[0]] + list(s0[2:])
        bd = bounds if fixed_S8 is None else [bounds[0]] + list(bounds[2:])
        r = optimize.minimize(chi2, x0, method="L-BFGS-B", bounds=bd)
        r2 = optimize.minimize(chi2, r.x, method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-8, maxiter=4000))
        x = r2.x if r2.fun < r.fun else r.x; f = min(r2.fun, r.fun)
        x = np.clip(x, [b[0] for b in bd], [b[1] for b in bd]); f = chi2(x)
        if best is None or f < best[1]: best = (x, f)
    return best


def s8_profile(ts, data, icov, bounds, x_best, grid):
    out = []
    for s8 in grid:
        st = [(x_best[0], s8) + tuple(x_best[2:])]
        x, f = fit(ts, data, icov, bounds, st, fixed_S8=s8)
        out.append(f)
    return np.array(out)


def tension(val, pub, extra=0.0):
    """(val - published) in units of the published error on the side val lies (Planck's normalisation error added in
    quadrature when extra > 0)."""
    v, up, dn = pub
    s = up if val > v else dn
    return (val - v) / math.sqrt(s * s + extra * extra)


# ================================================================================================ the chain's nonlinear P(k, z)
ZR = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4.0])
KC = np.geomspace(1e-3, 100.0, 130)
ZCAMB = np.concatenate([np.linspace(0.0, 4.0, 41), [4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]])


def omega_L(z, Om=1 - OL0):
    return OL0 / (Om * (1 + z) ** 3 + OL0)


class ChainBase:
    """Planck-2018 LCDM (CAMB, HMcode-2020) + the halo model at the response epochs ZR; the chain's response
    R(k, z) = P_HM,chain / P_HM,LCDM (the method: a halo-model response applied to a calibrated LCDM P_NL)."""
    def __init__(self, zs=ZCAMB):
        pars = camb_setup(zs=zs, nl="mead2020"); self.res = camb.get_results(pars); self.C = Cosmo(self.res, zs)
        self.kc = KC; self.hm = HaloModel(self.C, KC)
        self.B = {float(z): self.hm.base(float(z), self.C.P(self.hm.kk, float(z), lin=True), None) for z in ZR}
        self._ph = {}

    def phantom(self, z, foot, L, edge="sharp", mrange=PH_MRANGE_MSUN):
        key = (float(z), foot, L, edge, mrange)
        if key not in self._ph:
            Lp = L_LAMBDA * omega_L(z) if L == "running" else float(L)
            self._ph[key] = phantom_rows(self.hm, float(z), A0[foot], Lp, mrange, edge)
        return self._ph[key]

    def response(self, T, Fz, vk, reading, ph=None, sigma_mode="lcdm", mutate=False, detail=False):
        hm = self.hm; R = np.zeros((len(ZR), len(self.kc))); det = {}
        for iz, z in enumerate(ZR):
            z = float(z); B = self.B[z]
            Pl = self.C.P(self.kc, z, lin=True)
            t2 = np.ones_like(self.kc) if (mutate or T is None) else T(self.kc, z, "tot")
            Fe = 0.0 if mutate else float(np.interp(z, Fz[0], Fz[1]))
            sd = sigma_d(Fz, vk, z)
            ret, frac = content(reading, hm.M, z, Fe, sd, vk, hm, B["rvir"], B["cv"], mutate=mutate)
            if sigma_mode == "cold" and not mutate and T is not None:
                n, b = hm.mf(hm.sigma(self.C.P(hm.kk, z, lin=True) * T(hm.kk, z, "cc")))
            else:
                n, b = B["n"], B["b"]
            phr = None if ph is None else self.phantom(z, *ph)
            Bph = 0.0 if phr is None else hm.bph(B, phr, n, b)
            num = Pl * t2 * (B["I1"] + Bph) ** 2 + hm.p1h(B, frac, phr, n)
            den = Pl * B["I1"] ** 2 + hm.p1h(B)
            R[iz] = num / den
            if detail: det[z] = dict(ret=ret, sd=sd, Fe=Fe)
        return (R, det) if detail else R


def R_fun(Rg, zmax_linear=None, T=None):
    """R(k, z): bilinear in (z, ln k) on (ZR, KC), held beyond; above ZR[-1] the linear T^2 if a Transfer is given."""
    lk = np.log(KC)

    def f(k, z):
        k = np.atleast_1d(k)
        if z > ZR[-1] and T is not None:
            return T(k, z, "tot")
        zc = min(max(z, ZR[0]), ZR[-1]); j = min(max(np.searchsorted(ZR, zc) - 1, 0), len(ZR) - 2)
        w = (zc - ZR[j]) / (ZR[j + 1] - ZR[j])
        row = (1 - w) * Rg[j] + w * Rg[j + 1]
        return np.interp(np.log(k), lk, row)
    return f


def solve_histories(names, mutate=False, workers=2):
    """run_comp for each named history (two threads; the solver is numpy/LAPACK-bound)."""
    from concurrent.futures import ThreadPoolExecutor
    R = record(); spec = {n: (k, v) for n, k, v in HISTORIES}
    def one(n):
        key, vk = spec[n]; Fz = history(key, mutate); comp = run_comp(S_of(Fz), vk)
        return n, dict(Fz=Fz, vk=vk, comp=comp, T=Transfer(comp, R["LC"]))
    with ThreadPoolExecutor(workers) as ex:
        return dict(ex.map(one, names))
