#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG260 core: loader, membership, baryon recipe, the implied-a0 estimator (CFG223's s*), bootstrap, bands.  Frozen criteria: FROZEN_CRITERIA.md (00f20121d).
THE LOADER NEVER READS THE WIDTH COLUMNS unless the caller passes widths=True (only the measurement script does; the pre-flight never).  kappa = 1/2 FITTED."""
import os, sys, csv, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, LANES)
import CFG4_common as K

G, MSUN, KPC, PC, CKMS = 6.6743e-11, 1.98847e30, 3.0857e19, 3.0857e16, 299792.458
H0_TAB, OM = 70.0, 0.3
NU, NU_P2 = K.nu_mono, K.nu_p2
A0 = dict(K.A0)                                                         # canonical 9.3603e-11, alt 1.1312e-10
CSV = os.path.join(REPO, "data_assembly", "high_z_tf_tables", "budhies_joined.csv")
NONWIDTH = ("cluster", "index", "rah", "ram", "ras", "de_sign", "ded", "dem", "des", "z_hi", "dlum_mpc", "sint_mjykms", "e_sint", "mhi_1e9msun", "e_mhi",
            "profile_type", "pa_deg", "z_opt", "bmag", "bmag_flag", "rmag", "rmag_flag", "z_opt_hi_mismatch_flag")
WIDTH_COLS = ("w50_kms", "e_w50")                                       # read only by the measurement
FORBIDDEN = ("w20_kms", "e_w20", "w50_kms", "e_w50")                    # the pre-flight never reads these

# ------------------------------------------------------------------------------------------------ geometry and membership (CFG212's rule and constants)
def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def DA_mpc(z, h0=H0_TAB):
    return CKMS / h0 * quad(lambda x: 1 / E(x), 0, z)[0] / (1 + z)


def DL_mpc(z, h0=H0_TAB):
    return (1 + z) ** 2 * DA_mpc(z, h0)


def hms(h, m, s):
    return 15 * (float(h) + float(m) / 60 + float(s) / 3600)


def dms(sign, d, m, s):
    v = float(d) + float(m) / 60 + float(s) / 3600
    return -v if sign.strip() == "-" else v


def sep_rad(ra1, de1, ra2, de2):
    ra1, de1, ra2, de2 = map(np.radians, (ra1, de1, ra2, de2))
    s = np.sin((de2 - de1) / 2) ** 2 + np.cos(de1) * np.cos(de2) * np.sin((ra2 - ra1) / 2) ** 2
    return 2 * np.arcsin(np.sqrt(s))


CL = {"A963": dict(z=0.206, ra=hms(10, 17, 14.22), dec=dms(" ", 39, 1, 22.1), sig=993.0),
      "A2192": dict(z=0.188, ra=hms(16, 26, 36.99), dec=dms(" ", 42, 40, 10.1), sig=653.0)}
DA_CL = {k: DA_mpc(v["z"]) for k, v in CL.items()}
R_INNER = 2.0                                                           # Mpc, frozen
PB_FWHM_ARCMIN = 61.0 * math.sqrt(math.log(2) / math.log(4))           # WSRT primary beam: FWQM 61' at 1190 MHz (BUDHIES IV via the data chat's summariser read, UNVERIFIED) -> FWHM 43.1'; pointing taken at the cluster centre
C_MIN = 1.0                                                             # Addendum 2: completeness ratio of the PRIMARY set PC
M_HI_CUT = 3.0e9                                                        # Msun, frozen


def load_galaxies(widths=False):
    cols = NONWIDTH + (WIDTH_COLS if widths else ())
    rows = []
    with open(CSV, newline="") as f:
        for r in csv.DictReader(f):
            rows.append({k: r[k] for k in cols})
    gals = []
    for r in rows:
        c = CL[r["cluster"]]; z = float(r["z_hi"])
        dv = CKMS * abs(z - c["z"]) / (1 + c["z"])
        ra, de = hms(r["rah"], r["ram"], r["ras"]), dms(r["de_sign"], r["ded"], r["dem"], r["des"])
        R = float(sep_rad(ra, de, c["ra"], c["dec"])) * DA_CL[r["cluster"]]
        g = dict(cl=r["cluster"], idx=int(r["index"]), z=z, dl=float(r["dlum_mpc"]), mhi=float(r["mhi_1e9msun"]) * 1e9, sint=float(r["sint_mjykms"]), esint=float(r["e_sint"]),
                 ptype=int(r["profile_type"]), bmag=float(r["bmag"]), rmag=float(r["rmag"]), sdss=bool(r["bmag_flag"].strip() or r["rmag_flag"].strip()),
                 mem=bool(dv < 3 * c["sig"]), dv=dv, R=R)
        g["e0"] = (g["cl"], g["idx"]) == ("A963", 68)
        g["inner"] = bool(g["mem"] and g["R"] < R_INNER)
        if widths:
            g["w50"] = float(r["w50_kms"]); g["e_w50"] = float(r["e_w50"])
        gals.append(g)
    # Addendum 2: the completeness ratio c = (S_int / W_edge) PB(theta) / S_lim,pk, from NON-WIDTH inputs only (W_edge = predicted edge-on width, nominal recipe, a0 canonical)
    a = Arr(gals)
    _, _, Mb, Rm = baryons(a, REC0)
    gb = G * Mb * MSUN / Rm ** 2
    go = gb * nuv(NU, gb / A0["canonical"])
    Wedge = 2 * np.sqrt(go * Rm) / 1e3 * (1 + a.z) + REC0["delta"]
    theta = np.array([g["R"] / DA_CL[g["cl"]] * (180 / math.pi) * 60 for g in gals])
    pb = np.exp(-4 * math.log(2) * (theta / PB_FWHM_ARCMIN) ** 2)
    c = (a.sint / Wedge) * pb / a.spk_lim
    for g, th, p_, c_, we in zip(gals, theta, pb, c, Wedge):
        g["theta"], g["pb"], g["c"], g["wedge"] = float(th), float(p_), float(c_), float(we)
    return gals


SUBSETS = {
    "P":  lambda g: (not g["e0"]) and (not g["inner"]) and g["mhi"] >= M_HI_CUT,
    "S1": lambda g: (not g["e0"]) and g["inner"] and g["mhi"] >= M_HI_CUT,
    "S2": lambda g: (not g["e0"]) and (not g["mem"]) and g["mhi"] >= M_HI_CUT,
    "S3": lambda g: (not g["e0"]) and g["mem"] and (not g["inner"]) and g["mhi"] >= M_HI_CUT,
    "S4": lambda g: SUBSETS["P"](g) and g["ptype"] == 1,
    "S5": lambda g: SUBSETS["P"](g) and g["ptype"] in (1, 3),
    "S6": lambda g: (not g["e0"]) and (not g["inner"]),
    "S7": lambda g: (not g["e0"]) and (not g["inner"]) and g["mhi"] >= 5.0e9,
    "S8": lambda g: SUBSETS["P"](g) and (not g["sdss"]),
    "PC":    lambda g: SUBSETS["P"](g) and g["c"] >= C_MIN,
    "PC125": lambda g: SUBSETS["P"](g) and g["c"] >= 1.25,
    "PC15":  lambda g: SUBSETS["P"](g) and g["c"] >= 1.5,
}
SUBSET_LABEL = {"P": "P-all (outside 2 Mpc or non-member; M_HI >= 3e9; selection-biased)", "S1": "inner members (< 2 Mpc), M_HI >= 3e9", "S2": "field only (non-members), M_HI >= 3e9",
                "S3": "members beyond 2 Mpc, M_HI >= 3e9", "S4": "primary, profile type 1 only", "S5": "primary, types 1 and 3", "S6": "primary without the M_HI cut",
                "S7": "primary with M_HI >= 5e9", "S8": "primary without the SDSS-converted magnitudes",
                "PC": "PRIMARY (Addendum 2): P with completeness ratio c >= 1.0", "PC125": "P with c >= 1.25", "PC15": "P with c >= 1.5"}


def select(gals, key):
    return [g for g in gals if SUBSETS[key](g)]


class Arr:
    """galaxy arrays of a selected set (shape (n,))"""
    def __init__(self, gals):
        self.gals = gals
        self.n = len(gals)
        for key in ("z", "dl", "mhi", "bmag", "rmag", "sint", "R", "esint"):
            setattr(self, key, np.array([g[key] for g in gals], float))
        self.spk_lim = (2.0e9 * (1 + self.z) / (2.356e5 * self.dl ** 2)) * 1e3 / 150.0      # mJy: S_int,lim (2e9 Msun) / 150 km/s, field centre
        self.pb = np.array([g.get("pb", 1.0) for g in gals], float)                         # primary-beam attenuation (Addendum 2)
        self.spk_thr = self.spk_lim / self.pb                                               # the detection threshold at the galaxy's position, f = 1


# ------------------------------------------------------------------------------------------------ the recipe (frozen, section 3)
REC0 = dict(delta=28.0, k=1, sini=math.sin(math.radians(60.0)), tau_ms=0.0, tau_gas=0.0, tau_b=0.0, kscale=1.0, rdex=0.0, hubble=70.0, h2=0.0, kernel="nu_mono")


def baryons(a, rec, eps_ms=0.0, eps_r=0.0):
    """gas, stars, total baryon mass (Msun) and the radius R (m); every rec value and eps may be an array broadcasting against the galaxy arrays"""
    ds = H0_TAB / np.asarray(rec["hubble"], float)                                         # distance scale: D_L, M_HI and M* scale as D^2
    z, Ks = a.z, rec["kscale"]
    KB, KR = 2.75 * z * Ks, 1.00 * z * Ks
    bmr = (a.bmag - a.rmag) - (KB - KR)
    MR = a.rmag - 5 * np.log10(a.dl * ds * 1e6 / 10.0) - KR - 0.03
    LR = 10 ** (-0.4 * (MR - 4.61))
    Ms = LR * 10 ** (-0.523 + 0.683 * bmr) * 10 ** (rec["tau_ms"] + eps_ms)
    Mhi = a.mhi * ds ** 2
    Mg = (1.33 + rec["h2"]) * Mhi * 10 ** rec["tau_gas"]
    tb = 10 ** np.asarray(rec["tau_b"], float)
    Mgas, Mstar = Mg * tb, Ms * tb
    R = 0.5 * 10 ** (0.506 * np.log10(Mhi) - 3.293 + rec["rdex"] + eps_r) * KPC
    return Mgas, Mstar, Mgas + Mstar, R


def derive(a, W, rec):
    """the analyst's per-galaxy quantities from tabulated widths W (km/s; shape (n,) or (M, n)) under the recipe rec"""
    Mgas, Mstar, Mb, R = baryons(a, rec)
    Wc = (np.asarray(W, float) - rec["delta"]) / (1 + a.z) ** rec["k"]
    ok = Wc > 0
    V = np.where(ok, Wc, np.nan) / (2 * rec["sini"]) * 1e3                                 # m/s
    gb = G * Mb * MSUN / R ** 2
    go = V ** 2 / R
    return dict(D=go / gb, gb=gb, go=go, V=V, ok=ok, Mb=Mb, Mgas=Mgas, Mstar=Mstar, R=R, y=gb / A0["canonical"])


# ------------------------------------------------------------------------------------------------ the estimator (CFG223's s*: bisection on log10 s in [-3, 3], 64 iterations)
LO_LS, HI_LS, NIT = -3.0, 3.0, 64


def nuv(nu, y):
    y = np.asarray(y, float)
    return nu(y.ravel()).reshape(y.shape)


def implied(D, gb, nu, a0):
    """log10 s* per row-set: the root of median_i log10[D_i / nu(gb_i / (a0 s))] = 0 (NaN galaxies ignored).  D, gb: (n,) or (B, n).  Returns (log10 s*, UNBOUNDED flag)."""
    D = np.atleast_2d(np.asarray(D, float)); gb = np.atleast_2d(np.asarray(gb, float))
    logD = np.log10(D)
    Bn = D.shape[0]

    def f(ls):
        return np.nanmedian(logD - np.log10(nuv(nu, gb / (a0 * 10.0 ** ls[:, None]))), axis=1)
    a = np.full(Bn, LO_LS); b = np.full(Bn, HI_LS)
    unb = ~((f(a) > 0) & (f(b) < 0))
    for _ in range(NIT):
        m = 0.5 * (a + b)
        pos = f(m) > 0
        a = np.where(pos, m, a); b = np.where(pos, b, m)
    return 0.5 * (a + b), unb


def kernel_of(rec):
    return NU if rec.get("kernel", "nu_mono") == "nu_mono" else NU_P2


def s_star(a, W, rec, foot="canonical"):
    d = derive(a, W, rec)
    ok = d["ok"]
    l, u = implied(d["D"][ok], d["gb"][ok], kernel_of(rec), A0[foot])
    return float(l[0]), bool(u[0]), int(ok.sum())


def s_btfr(a, W, rec, foot="canonical"):
    """the deep-limit route: median_i V^4 / (G M_b) over a0"""
    d = derive(a, W, rec)
    ok = d["ok"]
    a0i = d["V"][ok] ** 4 / (G * d["Mb"][ok] * MSUN)
    return float(np.log10(np.median(a0i) / A0[foot])), int(ok.sum())


def boot_interval(D, gb, nu, a0, B=10000, tag=0):
    n = len(D)
    I = np.random.default_rng(np.random.SeedSequence([260, n, tag])).integers(0, n, size=(B, n))
    l0, u0 = implied(D, gb, nu, a0)
    lb, ub = implied(np.asarray(D)[I], np.asarray(gb)[I], nu, a0)
    q = np.percentile(10 ** lb, [2.5, 16, 84, 97.5])
    return dict(n=n, log_s=float(l0[0]), s=10 ** float(l0[0]), unbounded=bool(u0[0]), unb_frac=float(ub.mean()), sd_log=float(np.std(lb)),
                lo95=float(q[0]), lo68=float(q[1]), hi68=float(q[2]), hi95=float(q[3])), lb, I


def gbar_of_gobs(gobs, a0t, nu):
    q = gobs / a0t
    return a0t * 10 ** brentq(lambda ly: float(nu(np.array([10 ** ly]))[0]) * 10 ** ly - q, -80, 14, xtol=1e-14, rtol=1e-14)


def place(gobs, F, nu, a0):
    """CFG223's place: the galaxies placed ON a law with scale a0 F_i through their g_obs; returns D_T, g_bar,T"""
    gt = np.array([gbar_of_gobs(g, a0 * f, nu) for g, f in zip(gobs, F)])
    return gobs / gt, gt


def expectations(d_ok, z, lb, I, nu, a0):
    """expected s* of FLAT and the RIVAL for the same galaxies and the statistics-only pull (CFG223's expectations)"""
    out = {}
    for name, F in (("FLAT", np.ones(len(z))), ("RIVAL", np.array([E(float(zz)) for zz in z]))):
        Dt, gt = place(d_ok["go"], F, nu, a0)
        e0 = float(implied(Dt, gt, nu, a0)[0][0])
        eb = implied(Dt[I], gt[I], nu, a0)[0]
        sdd = float(np.std(lb - eb))
        out[name] = dict(log_s=e0, s=10 ** e0, sd_diff=sdd)
    return out


# ------------------------------------------------------------------------------------------------ bands and the recipe knobs (frozen, section 3 step 11)
TAUS = (-0.30, -0.15, 0.15, 0.30)
KNOBS = (("delta", (16.0, 40.0), "width correction (km/s)"), ("sini", (0.80, 0.92), "sin i_eff"), ("tau_ms", (-0.25, 0.25), "M* zero point (dex)"),
         ("kscale", (0.5, 1.5), "K-correction scale"), ("rdex", (-0.15, 0.15), "R scale (dex)"), ("hubble", (67.4, 73.0), "H0 (distance scale)"))


def baryon_bands(a, W, rec, foot="canonical"):
    out = {}
    for t in TAUS:
        r = dict(rec, tau_b=t)
        d = derive(a, W, r); ok = d["ok"]
        l, u = implied(d["D"][ok], d["gb"][ok], kernel_of(r), A0[foot])
        out[t] = (10 ** float(l[0]), bool(u[0]))
    return out


def recipe_band(a, W, rec, foot="canonical"):
    rows = {}
    for key, br, label in KNOBS:
        ls = []
        for v in br:
            r = dict(rec); r[key] = v
            ls.append(s_star(a, W, r, foot)[0])
        rows[key] = dict(label=label, brackets=br, log_s=ls, half=0.5 * abs(ls[1] - ls[0]))
    half = math.sqrt(sum(v["half"] ** 2 for v in rows.values()))
    single = {}
    for name, upd in (("H2 (M_H2 = 0.3 M_HI added)", dict(h2=0.3)), ("P2 kernel", dict(kernel="P2")), ("other frame (k flipped)", dict(k=1 - rec["k"]))):
        r = dict(rec); r.update(upd)
        single[name] = s_star(a, W, r, foot)[0]
    return rows, half, single


def nu_name(rec):
    return rec.get("kernel", "nu_mono")
