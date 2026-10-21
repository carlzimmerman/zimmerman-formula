#!/usr/bin/env python3
"""CFG930 -- energy-limited settling of primordial cold energy (H-ELS).
Criteria: FROZEN_CRITERIA.md (3dec25afe), clarifications AMENDMENT_A1.md (written before any run).
Run (one core, nice 10, < 1 GB, nothing downloaded):  CFG930_MODE = K | MUTATE_eps0 | MUTATE_epsinf | MUTATE_K | MAIN (default)
CFG42 / CFG827 / CFG874 code is exec'd read-only (writes refused); other lanes' JSON files are only read.
kappa = 1/2 FITTED; footings never pooled; cold energy, not a particle; not theory closed."""
import os, sys, math, json, csv, glob, hashlib, time
import numpy as np
from scipy.special import erfc
from scipy.optimize import brentq
from scipy.integrate import simpson, quad, cumulative_trapezoid
from scipy.stats import spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MODE = os.environ.get("CFG930_MODE", "MAIN")
SUF = {"K": "_K", "MUTATE_eps0": "_MUTATE_eps0", "MUTATE_epsinf": "_MUTATE_epsinf", "MUTATE_K": "_MUTATE_K", "MAIN": ""}[MODE]
for _v in ("MUTATE", "CFG827_MUTATE", "CFG874_MUTATE"):
    os.environ.pop(_v, None)                                   # the source lanes in their main configuration
OUT, CHECKS = [], []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, detail, ok):
    CHECKS.append(dict(name=name, detail=str(detail), ok=bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


sys.path.insert(0, LANES)
import CFG7_common as C
C4 = C.C4
sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
import hunt_lib as HL

P("CFG930  energy-limited settling of primordial cold energy (H-ELS)   mode " + MODE)
P("  kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; native inputs only in verdicts; not theory closed")

# ================================================================================================ source lanes (read-only)
J42 = json.load(open(os.path.join(LANES, "CFG42_satellites_rule_results.json")))["numbers"]
ns42, _ = C4.exec_slices(os.path.join(LANES, "CFG42_satellites_rule.py"), [(None, "reading = (")], name="cfg42")
SAMPLES, UL, infall_gas = ns42["SAMPLES"], ns42["UL"], ns42["infall_gas"]
halo_mass, nfw_enclosed, edge_phantom, FB42 = ns42["halo_mass"], ns42["nfw_enclosed"], ns42["edge_phantom"], ns42["FB"]
A0H, a_int, km_median, boot42 = ns42["A0H"], ns42["a_int"], ns42["km_median"], ns42["boot"]
ns827, _ = C4.exec_slices(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827.py"), [(None, 'P("CFG827 (= CFG824b)')], name="cfg827")
J827 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
SSP, ssp, SFH, ups_sfh = ns827["SSP"], ns827["ssp"], ns827["SFH"], ns827["ups_sfh"]
ns874, _ = C4.exec_slices(os.path.join(LANES, "CFG874_isolated_dwarfs_pooled", "cfg874.py"), [(None, 'P("CFG874  all isolated')], name="cfg874")
J874 = json.load(open(os.path.join(LANES, "CFG874_isolated_dwarfs_pooled", "cfg874_results.json")))
J828 = json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))
J921 = json.load(open(os.path.join(LANES, "CFG921_excess_selector_posits", "cfg921_results.json")))
J823 = json.load(open(os.path.join(LANES, "CFG823_dsph_cold_budget", "cfg823_results.json")))
J922 = json.load(open(os.path.join(LANES, "CFG922_cluster_core_baryon_recheck", "cfg922_results.json")))["results"]
CEN922 = json.load(open(os.path.join(LANES, "CFG922_cluster_core_baryon_recheck", "cfg922_census_A1.json")))["eRASS1"]
PC7 = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
J654 = json.load(open(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_ics_results.json")))

# ================================================================================================ constants
G, Msun, PC, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19         # the reused estimators' constants
A0X = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
ESN = 1.0e42                                                          # J per Msun formed (1e49 erg, declared)
SUP = 5.364; FBN = 1.0 / (1.0 + SUP)
DELTA_C, FPROG, MED_HN = 1.686, 0.01, 0.6744897501960817               # sqrt(2) erfcinv(1/2)
XE = 0.40
PLUM = 1.0 / math.sqrt(2 ** (2.0 / 3.0) - 1.0)                         # Plummer 3D half-mass radius / a
GK = C.GMPC * 1e3                                                      # kpc (km/s)^2 / Msun
AGN_HI = 3.0e62 * 1e-7                                                 # J
NG = 2401
INF = math.inf


def nu_e(y):
    y = np.maximum(np.asarray(y, float), 1e-15); return 1.0 / (-np.expm1(-np.sqrt(y)))


def nu_si(y):
    y = np.maximum(np.asarray(y, float), 1e-15); return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))


def nu_hl(y):                                                          # hunt_lib's exponential kernel (CFG42's a_int), vectorised
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


KERN = {"nu_e": nu_e, "nu_simple": nu_si}

# ================================================================================================ native cosmology (CFG654 cmb tables)
TS = np.load(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_scorer_tables_cmb.npz"))
TI = np.load(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_ics_tables_cmb.npz"))
DTA = json.load(open(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_delta_ta_cmb.json")))
h_, Om, Or, OL, NS = float(TS["h"]), float(TS["Om"]), float(TS["Or"]), float(TS["OL"]), float(TI["ns"])
KH, PK = np.asarray(TS["kh"], float), np.asarray(TS["Plin_z0"], float)
LNA_T, LND_T = np.asarray(TS["lna"], float), np.asarray(TS["lnD"], float)
ZTA, DTAV = np.array(DTA["z"], float), np.array(DTA["D"], float); DTA0 = float(DTAV[0])
RHOC_H = 3 * 100.0 ** 2 / (8 * math.pi * C.GMPC)                       # (Msun/h)/(Mpc/h)^3
RHOM0_H = Om * RHOC_H
RHOM0_KPC = Om * RHOC_H * h_ ** 2 / 1e9                                # Msun / kpc^3
GAM = Om * h_
KK = np.logspace(-4, 5, 9001); LKK = np.log(KK); KMAX = float(KH[-1])
PT = np.exp(np.interp(LKK, np.log(KH), np.log(PK)))
_ext = KK > KMAX


def p_ext(k):
    return PK[-1] * (k / KMAX) ** (NS - 4.0) * (np.log1p(2.34 * k / GAM) / math.log1p(2.34 * KMAX / GAM)) ** 2


PT[_ext] = p_ext(KK[_ext])


def W_th(x):
    x = np.asarray(x, float); out = np.empty_like(x); s = x < 1e-3
    out[s] = 1.0 - x[s] ** 2 / 10.0; xx = x[~s]; out[~s] = 3.0 * (np.sin(xx) - xx * np.cos(xx)) / xx ** 3
    return out


def sig2_R(R):                                                         # R in Mpc/h
    return float(np.trapz(KK ** 3 * PT * W_th(KK * R) ** 2, LKK) / (2 * math.pi ** 2))


LMG = np.arange(0.0, 17.0001, 0.01)
SIG2G = np.array([sig2_R((3 * 10 ** lm * h_ / (4 * math.pi * RHOM0_H)) ** (1.0 / 3.0)) for lm in LMG])


def sig2M(M):
    return float(np.exp(np.interp(math.log10(M), LMG, np.log(SIG2G))))


LND0 = float(np.interp(0.0, LNA_T, LND_T)); LNDN = LND_T - LND0
assert LNA_T[-1] >= 0.0 and np.all(np.diff(LNDN) > 0)


def D_of_z(z):
    return float(math.exp(np.interp(-math.log1p(z), LNA_T, LNDN)))


def z_of_D(D):
    return float(math.exp(-np.interp(math.log(D), LNDN, LNA_T)) - 1.0)


def zcoll(M):
    ds2 = sig2M(FPROG * M) - sig2M(M)
    if ds2 <= 0:
        return 0.0, 1.0, ds2
    Dc = 1.0 / (1.0 + MED_HN * math.sqrt(ds2) / DELTA_C)
    return z_of_D(Dc), Dc, ds2


# native background time and the virial overdensity (spherical collapse r_vir = r_ta/2 at t_c = 2 t_ta)
_lna = np.linspace(-20.0, 0.0, 20001); _a = np.exp(_lna)
_H = 100 * h_ * np.sqrt(Om / _a ** 3 + Or / _a ** 4 + OL)
_t = cumulative_trapezoid(1.0 / _H, _lna, initial=0.0) + 0.5 / (100 * h_ * math.sqrt(Or)) * _a[0] ** 2
T_NOW = float(_t[-1]); A_TA = float(np.exp(np.interp(0.5 * T_NOW, _t, _lna))); Z_TA = 1.0 / A_TA - 1.0
DVIR = 8.0 * float(np.interp(Z_TA, ZTA, DTAV)) * (1.0 + Z_TA) ** 3


def m_(x):
    x = np.asarray(x, float)
    return np.where(x < 1e-3, x * x / 2 - 2 * x ** 3 / 3 + 3 * x ** 4 / 4, np.log1p(x) - x / (1 + x))


def conc_from(rhs):
    return math.exp(brentq(lambda lc: math.log(float(m_(math.exp(lc)))) - 3 * lc - math.log(rhs), math.log(1e-4), math.log(1e8), xtol=1e-13))


def fret_of(lM):                                                       # CFG416 / CFG556 / CFG804, verbatim
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)


def mta_fixed(Mb):                                                     # CFG804's N_of fixed point (f_b = 1/(1+5.364))
    f = 0.10; lMb = math.log10(Mb)
    for _ in range(200):
        lMta = lMb - math.log10(f * FBN); fn = fret_of(lMta)
        if abs(fn - f) < 1e-12: break
        f = 0.5 * (f + fn)
    return f, 10 ** lMta


def rta_law(Mb, a0, nu):                                               # kpc; the law's untruncated mean density = Delta_ta(0) rho_m0
    a0k = a0 * KPC / 1e6; tgt = math.log(DTA0 * RHOM0_KPC)
    f = lambda lr: math.log(Mb * float(nu(GK * Mb / math.exp(2 * lr) / a0k)) / (4 * math.pi / 3 * math.exp(3 * lr))) - tgt
    return math.exp(brentq(f, math.log(1e-4), math.log(1e8), xtol=1e-13))


class Halo:                                                            # NATIVE primordial cold halo
    def __init__(s, Mb, a0, nu, cor):
        s.fret, Mta0 = mta_fixed(Mb); s.Mta = Mta0 * cor["smult"] * cor.get("Nx", 1.0); s.Mc = (1 - FBN) * s.Mta
        s.zc, s.Dc, s.ds2 = zcoll(s.Mta)
        Db = DTA0 if cor["bnd"] == "rta" else DVIR
        s.rb = (3 * s.Mta / (4 * math.pi * Db * RHOM0_KPC)) ** (1.0 / 3.0)
        s.rhos = cor["C"] * RHOM0_KPC * (1 + s.zc) ** 3
        s.c = conc_from(Db / (3 * cor["C"] * (1 + s.zc) ** 3)); s.rs = s.rb / s.c; s.mc = float(m_(s.c))
        s.re = XE * rta_law(Mb, a0, nu)
        s.Mph_e = Mb * (float(nu(GK * Mb / s.re ** 2 / (a0 * KPC / 1e6))) - 1.0)
        s.fex_A = max(0.0, 1.0 - s.Mph_e / s.Mc)
        s.fex = s.fex_A if cor["reading"] == "NA" else 1.0

    def Mnfw(s, r):
        r = np.minimum(np.asarray(r, float), s.rb); return s.Mta * m_(r / s.rs) / s.mc

    def dMdr(s, r):
        x = np.asarray(r, float) / s.rs; return np.where(np.asarray(r) <= s.rb, s.Mta / (s.mc * s.rs) * x / (1 + x) ** 2, 0.0)

    def Mdeb(s, r):
        return s.fex * (1 - FBN) * s.Mnfw(r)

    def McNFW(s, r):
        return (1 - FBN) * s.Mnfw(r)


class HaloK:                                                           # CFG42's inputs (Moster + Dutton-Maccio, CFG35 edge) -- K / MUTATE only
    def __init__(s, Mb, Mh, foot):
        s.Mh = Mh; s.Mc = (1 - FB42) * Mh
        s.fex = max(0.0, 1.0 - edge_phantom(Mb, foot, 0.40) / ((1 - FB42) * Mh)); s.fex_A = s.fex
        s.re = 0.40 * float(C.r_ta_law(Mb, C.A0[foot], C.nu_mono, 1.0)) * 1e3

    def Mdeb(s, r):
        return s.fex * (1 - FB42) * np.asarray(nfw_enclosed(s.Mh, np.asarray(r, float)), float)

    def McNFW(s, r):
        return (1 - FB42) * np.asarray(nfw_enclosed(s.Mh, np.asarray(r, float)), float)


def law_profile(r, Mb, rh3, a0, nu):                                   # Plummer baryons; returns g_N, g_law (SI)
    a = rh3 / PLUM; rm = r * KPC; Mbr = Mb * r ** 3 / (r * r + a * a) ** 1.5
    gN = G * Mbr * Msun / rm ** 2; return gN, gN * nu(gN / a0)


def energy(halo, Mb, rh3, a0, nu, selfgrav=False, table=False):
    """dE = int_0^re g(r) M_deb(<r) dr  [J]  (= lifting the debris inside re out to re); optional Form-B table."""
    re = halo.re; r = np.logspace(math.log10(re) - 6, math.log10(re), NG); rm = r * KPC
    _, g = law_profile(r, Mb, rh3, a0, nu); Md = halo.Mdeb(r)
    if selfgrav: g = g + G * Md * Msun / rm ** 2
    f = g * Md * Msun; dE = float(simpson(f, x=rm)) if np.any(Md > 0) else 0.0
    tab = None
    if table:
        A = cumulative_trapezoid(f, rm, initial=0.0); Bc = cumulative_trapezoid(g, rm, initial=0.0)
        tab = (r, A + Md * Msun * (Bc[-1] - Bc))
    return dE, tab


def r1_energy(halo, Mb, rh3, a0, nu):
    """R1: dU = U_settled - U_primordial = int g_law [M_cNFW(<r) - min(M_ph(<r), M_c)] dr  [J]; and the supply edge."""
    def mph(r):
        gN, g = law_profile(r, Mb, rh3, a0, nu); return g, (g - gN) * (r * KPC) ** 2 / G / Msun
    fsup = lambda lr: float(mph(np.array([math.exp(lr)]))[1][0]) - halo.Mc
    lo, hi = math.log(1e-7 * halo.rb), math.log(1e9)
    rsup = math.exp(hi) if fsup(hi) < 0 else math.exp(brentq(fsup, lo, hi, xtol=1e-12))
    Rmax = max(halo.rb, rsup); r = np.logspace(math.log10(Rmax) - 7, math.log10(Rmax), NG)
    g, Mph = mph(r)
    return float(simpson(g * (halo.McNFW(r) - np.minimum(Mph, halo.Mc)) * Msun, x=r * KPC)), rsup


def proj_mass(halo, R):
    """debris inside the cylinder of radius R (kpc), truncated NFW (3D part + shell part with r = R cosh u)."""
    if halo.rb <= R:
        return float(halo.Mdeb(halo.rb))
    u = np.linspace(0.0, math.acosh(halo.rb / R), 4001); r = R * np.cosh(u)
    shell = simpson(halo.fex * (1 - FBN) * halo.dMdr(r) * (1 - np.tanh(u)) * R * np.sinh(u), x=u)
    return float(halo.Mdeb(R)) + float(shell)


# ================================================================================================ stellar mass formed
def _norm(s):
    return s.lower().replace("andromeda", "and").replace(" ", "").replace("_", "").replace(".", "")


SFHN = {_norm(k): k for k in SFH}
for _k, _v in {"and1": "Andromeda I", "and2": "Andromeda II", "and3": "Andromeda III", "and5": "Andromeda V", "and6": "Andromeda VI",
               "and7": "Andromeda VII", "and11": "Andromeda XI", "and13": "Andromeda XIII"}.items():
    if _v in SFH: SFHN.setdefault(_k, _v)


def mform_per_L(B, Z):
    return sum(dm for _, dm in B) / sum(dm * ssp(Z, t)[1] for t, dm in B)


MEDML = {Z: float(np.median([mform_per_L(SFH[k], Z) for k in J827])) for Z in (-1.31, -1.71, -0.71)}
BURST = {Z: 1.0 / ssp(Z, 13.3)[1] for Z in (-1.31, -1.71, -0.71)}
MREM_CONST = {Z: float(np.mean([ssp(Z, t)[0] for t in np.linspace(0.0, 13.3, 2661)[1:]])) for Z in (0.0, -1.31)}
MREM_BURST0 = ssp(0.0, 13.3)[0]
MATCHED = {}


def mformed(name, LV, Z=-1.31, mode="burst"):
    k = SFHN.get(_norm(name))
    if k:
        MATCHED[name] = k; return LV * mform_per_L(SFH[k], Z)
    return LV * (MEDML[Z] if mode == "median" else BURST[Z])


# ================================================================================================ samples
def sparc_load():
    Q = {}
    for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
        v = l.split()
        if len(v) >= 18 and v[1].isdigit():
            try: Q[v[0]] = (float(v[5]), int(v[17]))
            except ValueError: pass
    MAST = HL.read_master(); gals = []
    for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
        name = os.path.basename(fn).replace("_rotmod.dat", ""); inc, q = Q.get(name, (0, 3))
        if q > 2 or inc < 30: continue
        rows = []
        for l in open(fn):
            if l.startswith("#") or not l.strip(): continue
            R, V, eV, Vg, Vd, Vb = [float(x) for x in l.split()[:6]]
            if V <= 0 or R <= 0 or eV / V >= 0.10: continue
            g_b = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPC)
            if g_b <= 0: continue
            rows.append((R, Vg * abs(Vg), Vd * abs(Vd), Vb * abs(Vb), V * V * 1e6 / (R * KPC)))
        if not rows: continue
        a = np.array(rows); m = MAST[name]
        gals.append(dict(name=name, R=a[:, 0], gg=a[:, 1], gd=a[:, 2], gbul=a[:, 3], gobs=a[:, 4], L36=m["L36"] * 1e9, MHI=m["MHI"] * 1e9, Rd=m["Rdisk"]))
    return gals


SPARC = sparc_load()
_ms = np.array([0.5 * g["L36"] for g in SPARC]); _t1 = np.percentile(_ms, 100.0 / 3.0)
for g in SPARC:
    g["faint"] = bool(0.5 * g["L36"] <= _t1)
ISO_ALL = ns874["SAMPLE"]
CLS_NAMES = ("U", "UL", "C", "Mc", "Ml", "I", "S")


# ================================================================================================ objects and worlds
class Obj:
    def __init__(s, **kw):
        s.__dict__.update(kw)

    def fs(s, eps, reading):
        if eps == INF:
            return 1.0
        if reading == "R1":                                            # dU <= 0: settling is downhill, not energy-limited (criteria 3.4)
            return 1.0 if s.dU <= 0 else min(1.0, max(0.0, eps * s.E1 / s.dU))
        if eps == 0.0:
            return 0.0
        if not (s.dE > 0):                                             # no debris inside r_e: nothing to settle
            return 1.0
        return min(1.0, max(0.0, eps * s.E1 / s.dE))

    def g(s, eps, form="A", reading="NA"):
        f = s.fs(eps, reading)
        if reading == "R1":
            return s.gN + G * (np.minimum(s.Mph, f * s.halo.Mc) + (1 - f) * s.McN) * Msun / s.rm ** 2
        if form == "A" or f in (0.0, 1.0) or s.tab is None:
            Md = (1 - f) * s.Md
        else:
            r, F = s.tab; rc = float(np.interp(eps * s.E1, F, r)); Md = s.Md - s.halo.Mdeb(np.minimum(s.r, rc))
        return s.glaw + G * Md * Msun / s.rm ** 2


def make_halo(inp, Mb, foot, cor, a0, nu, Mh=None):
    return HaloK(Mb, Mh, foot) if inp == "K" else Halo(Mb, a0, nu, cor)


def build_world(inp, foot, cor, uf=1.0, var=None, need_r1=False, need_e=True):
    var = var or {}
    form, kern, Z, mmode = var.get("form", "A"), var.get("kern", "nu_e"), var.get("Z", -1.31), var.get("mform", "burst")
    selfg = var.get("selfgrav", False)
    if inp == "K":
        a0, nu = A0H[foot], nu_hl
    else:
        a0, nu = A0X[foot], KERN[kern]
    reading = cor["reading"] if inp == "N" else "NA"
    W = {k: [] for k in CLS_NAMES}; W["meta"] = dict(inp=inp, foot=foot, cor=dict(cor), uf=uf, var=dict(var))
    ups = 2.0 * uf

    def finish(o, halo, Mb, rh3):
        o.halo = halo; o.Md = halo.Mdeb(o.r); o.McN = halo.McNFW(o.r); o.Mph = (o.glaw - o.gN) * o.rm ** 2 / G / Msun
        o.tab = None; o.dE = 0.0; o.dU = 0.0
        if need_e and reading != "R1":
            o.dE, o.tab = energy(halo, Mb, rh3, a0, nu, selfgrav=selfg, table=(form == "B"))
        if need_r1 or reading == "R1":
            o.dU, o.rsup = r1_energy(halo, Mb, rh3, a0, nu)
        return o

    for key, src in (("U", SAMPLES["ufd"]), ("UL", UL), ("C", SAMPLES["cls"]), ("Mc", SAMPLES["col"]), ("Ml", SAMPLES["m31"])):
        for d in src:
            gas = 1.33 * d["MHI"] if key in ("U", "UL") else max(1.33 * d["MHI"], infall_gas(d))
            Mb = ups * d["LV"] + gas; rh_pc = (4.0 / 3.0) * d["rh"]; r = rh_pc / 1000.0; rm = rh_pc * PC
            gN = G * 0.5 * Mb * Msun / rm ** 2
            glaw = a_int(gN, 0.0, a0) if inp == "K" else float(gN * nu(gN / a0))
            o = Obj(name=d["name"], key=key, Mb=Mb, LV=d["LV"], r=r, rm=rm, gN=gN, glaw=glaw, sig=(d["sig_ul"] if key == "UL" else d["sig"]),
                    E1=ESN * mformed(d["name"], d["LV"], Z, mmode))
            halo = make_halo(inp, Mb, foot, cor, a0, nu, Mh=(float(halo_mass(2.0 * d["LV"])) if inp == "K" else None))
            W[key].append(finish(o, halo, Mb, r))
    for d in ISO_ALL:
        L = 10 ** (0.4 * (4.83 - d["MV"])); r12_pc = (4.0 / 3.0) * d["rh"]; r = r12_pc / 1000.0; rm = r12_pc * PC
        Ms = ups * L; Mg = ns874["gas_in"](d["lHI"], r12_pc, "disc")
        gb = G * (Ms / 2 + Mg) * Msun / rm ** 2
        if inp == "K":
            glaw = float(gb * nu_hl(gb / a0))
        else:                                                          # CFG874's own scalar kernel for nu_e (exact K3 arithmetic)
            glaw = gb * float(ns874["nu_e"](gb / a0)) if kern == "nu_e" else float(gb * nu(gb / a0))
        o = Obj(name=d["name"], key="I", grp=d["grp"], dmin=d["dmin"], lg=math.log10(gb), sv=d["s"], r=r, rm=rm, gN=gb, glaw=glaw,
                E1=ESN * mformed(d["name"], L, Z, mmode), Mb=Ms + (1.33 * 10 ** d["lHI"] if d["lHI"] is not None else 0.0))
        if d["grp"] == "I" and d["dmin"] >= 300.0:
            halo = make_halo(inp, o.Mb, foot, cor, a0, nu, Mh=(float(halo_mass(2.0 * L)) if inp == "K" else None))
            W["I"].append(finish(o, halo, o.Mb, r))
        elif d["grp"] == "S":
            W.setdefault("I_S", []).append(o)
    yd, yb = 0.5 * uf, 0.7 * uf
    for gl in SPARC:
        gbar = (gl["gg"] + yd * gl["gd"] + yb * gl["gbul"]) * 1e6 / (gl["R"] * KPC); mk = gbar > 0
        if mk.sum() == 0: continue
        Mb = yd * gl["L36"] + 1.33 * gl["MHI"]; r = gl["R"][mk]; rm = r * KPC; gbr = gbar[mk]
        glaw = gbr * (nu_hl(gbr / a0) if inp == "K" else nu(gbr / a0))
        o = Obj(name=gl["name"], key="S", faint=gl["faint"], r=r, rm=rm, gN=gbr, glaw=glaw, gobs=gl["gobs"][mk], Mb=Mb,
                E1=ESN * 0.5 * gl["L36"] / MREM_CONST[0.0], npts_drop=int((~mk).sum()))
        halo = make_halo(inp, Mb, foot, cor, a0, nu, Mh=(float(halo_mass(0.5 * gl["L36"])) if inp == "K" else None))
        W["S"].append(finish(o, halo, Mb, 1.68 * gl["Rd"]))
    return W


def sig_off(objs, eps, form, reading):
    return np.array([math.log10(o.sig / (math.sqrt(float(o.g(eps, form, reading)) * o.rm / 3.0) / 1e3)) for o in objs])


def iso_D(objs, eps, form, reading):
    return np.array([math.log10(3 * (o.sv * 1e3) ** 2 / o.rm / float(o.g(eps, form, reading))) for o in objs])


def sparc_gal(objs, eps, form, reading, faint=False):
    return np.array([float(np.median(np.log10(o.gobs / o.g(eps, form, reading)))) for o in objs if (o.faint or not faint)])


_IDX874 = {}


def iso_se(W, D):
    I = W["I"]; lgI = [o.lg for o in I]; lo, hi = min(lgI) - 0.5, max(lgI) + 0.5
    nS = sum(1 for o in W["I_S"] if lo <= o.lg <= hi); nI = len(I); key = (nI, nS)
    if key not in _IDX874:
        rng = np.random.default_rng(874); M = np.empty((4000, nI), int)
        for b in range(4000):
            M[b] = rng.integers(0, nI, nI); rng.integers(0, nS, nS)
        _IDX874[key] = M
    return float(np.std(D[_IDX874[key]].mean(axis=1)))


def raw_stats(W, eps, form, reading):
    x = sig_off(W["U"], eps, form, reading); xu = sig_off(W["UL"], eps, form, reading)
    out = {"U": (float(km_median(x, xu)), x, xu)}
    for k in ("C", "Mc", "Ml"):
        v = sig_off(W[k], eps, form, reading); out[k] = (float(np.median(v)), v)
    D = iso_D(W["I"], eps, form, reading); out["I"] = (float(D.mean()), D)
    for k, fa in (("S", False), ("S3", True)):
        v = sparc_gal(W["S"], eps, form, reading, faint=fa); out[k] = (float(np.median(v)), v)
    return out


def label(z):
    a = abs(z); return "CONSISTENT" if a < 2 else ("TENSION" if a < 3 else "CONTRADICTED")


RANK = {"CONSISTENT": 0, "TENSION": 1, "CONTRADICTED": 2}
_GCACHE = {}


def grade(Ws, eps, form, reading):
    """per class: statistic, statistical error, Upsilon floor, total, z, label (uniform recipe)."""
    keyb = []
    for uf in (1.0, 0.5, 2.0):
        for k in ("U", "UL", "C", "Mc", "Ml", "I", "S"):
            for o in Ws[uf][k]:
                keyb.append(np.round(np.log10(np.atleast_1d(o.g(eps, form, reading))), 12).tobytes())
    key = (id(Ws), hashlib.md5(b"".join(keyb)).hexdigest())
    if key in _GCACHE:
        return _GCACHE[key]
    n, lo, hi = (raw_stats(Ws[uf], eps, form, reading) for uf in (1.0, 0.5, 2.0))
    res = {}
    for k in ("U", "C", "Mc", "Ml", "I", "S", "S3"):
        st = n[k][0]; fu = 0.5 * abs(hi[k][0] - lo[k][0])
        if k == "U":
            es = float(boot42(n["U"][1], n["U"][2]))
        elif k == "I":
            es = iso_se(Ws[1.0], n["I"][1])
        else:
            v = n[k][1]; es = 1.2533 * float(np.std(v)) / math.sqrt(len(v))
        tot = math.sqrt(es ** 2 + fu ** 2); z = st / tot if tot > 0 else 0.0
        res[k] = dict(stat=st, err_stat=es, f_ups=fu, tot=tot, z=z, label=label(z), n=int(len(n[k][1]) + (len(n["U"][2]) if k == "U" else 0)))
    res["M"] = dict(label=max(res["Mc"]["label"], res["Ml"]["label"], key=lambda s: RANK[s]), parts=("Mc", "Ml"))
    _GCACHE[key] = res
    return res


GAL = ("U", "M", "I", "S", "S3")
EGRID = [0.0] + list(np.logspace(-4, 0, 41))


def calibrate(Ws, form, reading):
    Wn = Ws[1.0]
    offC = lambda e: float(np.median(sig_off(Wn["C"], e, form, reading)))
    o0, oi = offC(0.0), offC(INF); cal = dict(off0=o0, offinf=oi, root=None, status=None)
    if o0 <= 0.0 <= oi and oi > o0:
        if o0 == 0.0:
            cal.update(root=0.0, status="root")
        elif offC(1e-8) >= 0.0:
            cal.update(root=1e-8, status="root (<= 1e-8)")
        elif offC(1e4) < 0.0:
            cal.update(root=INF, status="root > 1e4 (UNPHYSICAL)")
        else:
            t = brentq(lambda t: offC(10 ** t), -8.0, 4.0, xtol=1e-10); cal.update(root=10 ** t, status="root")
    else:
        cal["status"] = "no root"
    return cal


def evaluate(Ws, form="A", reading="NA"):
    """calibrate on C, grade, overall per the frozen rule (one footing)."""
    cal = calibrate(Ws, form, reading); ev = dict(cal=cal)
    if cal["status"].startswith("root") and cal["root"] != INF:
        eps = cal["root"]; gr = grade(Ws, eps, form, reading); ev.update(eps=eps, grades=gr)
        ev["calib_z"] = gr["C"]["z"]
        labs = {k: gr[k]["label"] for k in GAL}
        if eps > 1.0:
            ov = "CONTRADICTED (UNPHYSICAL eps* > 1)"
        elif any(v == "CONTRADICTED" for v in labs.values()):
            ov = "CONTRADICTED"
        elif all(v == "CONSISTENT" for v in labs.values()):
            ov = "SURVIVES"
        else:
            ov = "NOT SURVIVING (TENSION)"
        A = [e for e in EGRID if abs(grade(Ws, e, form, reading)["C"]["z"]) < 2]
        ev.update(labels=labs, overall=ov, A=[float(a) for a in A])
        return ev
    if cal["root"] == INF:
        gr = grade(Ws, 1e4, form, reading); ev.update(eps=INF, grades=gr, labels={k: gr[k]["label"] for k in GAL}, overall="CONTRADICTED (UNPHYSICAL eps* > 1e4)", A=None)
        return ev
    A, per = [], {}
    for e in EGRID:
        gr = grade(Ws, e, form, reading)
        if abs(gr["C"]["z"]) < 2:
            A.append(e); per[e] = gr
    if not A:
        gr = grade(Ws, 0.0, form, reading)
        ev.update(eps=None, grades=gr, labels={k: gr[k]["label"] for k in GAL}, overall="CONTRADICTED (CALIBRATION IMPOSSIBLE)", A=[])
        return ev
    best = {k: min((per[e][k]["label"] for e in A), key=lambda s: RANK[s]) for k in GAL}
    joint = [e for e in A if all(per[e][k]["label"] == "CONSISTENT" for k in GAL)]
    allc = {k: all(per[e][k]["label"] == "CONTRADICTED" for e in A) for k in GAL}
    ov = "SURVIVES" if joint else ("CONTRADICTED" if any(allc.values()) else "NOT SURVIVING (TENSION)")
    pos = [e for e in A if e > 0]; emid = pos[len(pos) // 2] if pos else 0.0
    ev.update(eps=None, A=[float(a) for a in A], eps_mid=emid, grades=per[emid] if emid in per else per[A[0]], labels=best, joint=[float(j) for j in joint], overall=ov)
    return ev


def eps_used(ev):
    if ev.get("eps") is not None and ev["eps"] != INF:
        return ev["eps"]
    return ev.get("eps_mid", 0.0)


def final_label(ovs):
    if all(o == "SURVIVES" for o in ovs): return "SURVIVES"
    if any(o.startswith("CONTRADICTED") for o in ovs): return "CONTRADICTED"
    return "NOT SURVIVING (TENSION)"


def worlds(inp, foot, cor, var=None, need_r1=False):
    return {uf: build_world(inp, foot, cor, uf, var, need_r1=need_r1) for uf in (1.0, 0.5, 2.0)}


# ================================================================================================ clusters (median eRASS1 cluster)
MG_MED = float(np.median(PC7["mg"])); R500_MED = float(np.median(PC7["R500"])) * 1e3
BCG = {"med": float(np.median([c["bcg_med"] for c in CEN922])), "sup": float(np.median([c["bcg_sup"] for c in CEN922]))}


def cluster_window(foot):
    r = J922[f"eRASS1|s|{foot}"]; need = r["needed_masses"]["U"]["needed"]; lam = r["needed_masses"]["U"]["lam"]
    lz2 = r["U_lambda_conc_on_gascyl"]["Z2"]["value"]; mgc = need / lam
    return need, lz2 * mgc, 2 * need - lz2 * mgc


def cluster_grade(foot, cor, eps, var=None):
    var = var or {}; kern = var.get("kern", "nu_e"); a0, nu = A0X[foot], KERN[kern]
    if cor["reading"] == "R1":
        return dict(label="NOT EVALUATED (R1)")
    need, lo, hi = cluster_window(foot); pts = {}
    for mbf in (1.0, 1.2, 2.0):
        Mb = mbf * MG_MED; halo = Halo(Mb, a0, nu, cor); dE, _ = energy(halo, Mb, R500_MED, a0, nu, selfgrav=var.get("selfgrav", False))
        m2 = proj_mass(halo, 500.0)
        for agn in (0.0, AGN_HI):
            for bk in ("med", "sup"):
                E = (eps if eps is not None else 0.0) * ESN * BCG[bk] / MREM_BURST0 + agn
                fs = 1.0 if dE <= 0 else min(1.0, max(0.0, E / dE))
                pts[(mbf, agn, bk)] = dict(M2D=(1 - fs) * m2, fs=fs, dE=dE, fex=halo.fex, fex_A=halo.fex_A, Mta=halo.Mta)
    inw = lambda v: lo <= v <= hi
    prim = [pts[(1.2, 0.0, "med")]["M2D"], pts[(1.2, AGN_HI, "med")]["M2D"]]
    if all(inw(v) for v in prim):
        lab = "CONSISTENT (MID only; OUTER not computed)"
    elif all(v["M2D"] < lo for v in pts.values()) or all(v["M2D"] > hi for v in pts.values()):
        lab = "CONTRADICTED"
    else:
        lab = "UNDERDETERMINED"
    return dict(label=lab, window=[lo, hi], needed=need, primary_M2D=prim, corners={f"{k[0]}|{'AGN' if k[1] else 'noAGN'}|{k[2]}": v for k, v in pts.items()})


# ================================================================================================ K tests
def run_K():
    P("\n" + "=" * 110 + "\nK TESTS\n" + "=" * 110)
    # K1a: CFG42 exec'd read-only reproduces its committed numbers
    dev = 0.0
    for (foot, rule), v in ns42["UF"].items():
        ref = J42["UF"][f"{foot}|{'rule' if rule else 'law'}"]
        for k in ("km", "err", "f_ups", "f_mh", "tot", "z"): dev = max(dev, abs(v[k] - ref[k]))
    for (key, foot, rule), v in ns42["CL"].items():
        ref = J42["CL"][f"{key}|{foot}|{'rule' if rule else 'law'}"]
        for k in ("med", "tot", "z", "fex"): dev = max(dev, abs(v[k] - ref[k]))
    h4 = dict(n=len(ns42["rows"]), nfex=int((ns42["fz"] > 0).sum()))
    check("K1a CFG42 exec'd read-only reproduces its committed H1/H2/H4 numbers (UF km/err/f_ups/f_mh/tot/z, CL med/tot/z/fex, H4)",
          f"max |d| {dev:.1e}; H4 n {h4['n']} nfex {h4['nfex']}; UFD rule KM {ns42['UF'][('canonical', True)]['km']:+.4f} / {ns42['UF'][('alt', True)]['km']:+.4f}",
          dev <= 1e-9 and h4 == dict(n=110, nfex=0))
    # K1b: this lane's H-ELS path with K inputs at f_s = 0 reproduces CFG42's rule (and at f_s = 1 its law)
    d1 = 0.0
    for foot in FOOTS:
        W = build_world("K", foot, dict(reading="NA"), need_e=False)
        for rule, eps in ((True, 0.0), (False, INF)):
            x = sig_off(W["U"], eps, "A", "NA"); xu = sig_off(W["UL"], eps, "A", "NA")
            d1 = max(d1, abs(km_median(x, xu) - J42["UF"][f"{foot}|{'rule' if rule else 'law'}"]["km"]))
            for key, k42 in (("C", "cls"), ("Mc", "col"), ("Ml", "m31")):
                d1 = max(d1, abs(float(np.median(sig_off(W[key], eps, "A", "NA"))) - J42["CL"][f"{k42}|{foot}|{'rule' if rule else 'law'}"]["med"]))
    check("K1b / K7b this lane's H-ELS code path with CFG42's inputs: f_s = 0 equals CFG42's rule, f_s = 1 its law (UFD KM, cls, col, m31 medians; both footings)",
          f"max |d| {d1:.1e}", d1 <= 1e-9)
    # K2: CFG827
    d2 = 0.0
    for r in ns827["rows"]:
        nm = r["name"]; U = ups_sfh(SFH[nm], -1.31); ref = J827[nm]
        E = math.log(r["so"] / ns827["law"](r["MV"], r["rhl"], ns827["A0"]["canonical"], U))
        d2 = max(d2, abs(U - ref["ups"]), abs(ups_sfh(SFH[nm], -1.71) - ref["ups_lo"]), abs(ups_sfh(SFH[nm], -0.71) - ref["ups_hi"]), abs(E - ref["E_SFH"]))
    check("K2 CFG827's Ups_SFH (3 metallicities) and E_SFH reproduced for all 36 dwarfs", f"N {len(ns827['rows'])}; max |d| {d2:.1e}", d2 <= 1e-12 and len(ns827["rows"]) == 36)
    # K3: CFG874
    d3 = 0.0; txt = []
    for foot in FOOTS:
        r = ns874["analyse"](ns874["build"](foot, gas="disc")); ref = J874[foot]["primary"]
        W = build_world("N", foot, dict(reading="NA", C=3000, bnd="rta", smult=1), need_e=False)
        D = iso_D(W["I"], INF, "A", "NA"); E, se = float(D.mean()), iso_se(W, D)
        d3 = max(d3, abs(r["E"] - ref["E"]), abs(r["se_E"] - ref["se_E"]), abs(E - ref["E"]), abs(se - ref["se_E"]))
        txt.append(f"{foot}: E {E:+.4f} +- {se:.4f} (CFG874 {ref['E']:+.4f} +- {ref['se_E']:.4f})")
    z = {n: x for n, x in ((o["name"], o) for o in ns874["build"]("canonical", gas="zero", sig_mut=False))}
    ref860 = {m["name"]: m["d"] for k in ("I0", "IG") for m in ns874["R860"][k]}
    dk1 = max(abs(z[n]["D"] - v) for n, v in ref860.items())
    check("K3 CFG874 primary isolated E and se_E (exec'd and by this lane's replay of its bootstrap) + its K1 identity, both footings",
          "; ".join(txt) + f"; K1 identity max {dk1:.1e}", d3 <= 1e-12 and dk1 < 1e-9)
    # K4: source facts
    pts = np.concatenate([np.log10(o.gobs / o.glaw) for o in build_world("N", "canonical", dict(reading="NA", C=3000, bnd="rta", smult=1), need_e=False)["S"]])
    k4a = abs(float(np.median(pts)) - J828["canonical|nu_e"]["sparc_median_all"])
    rr = J828["canonical|nu_e"]["rows"]; rho828 = float(spearmanr([q["lgbar"] for q in rr], [q["delta"] for q in rr])[0])
    o921 = J921["observed"]["canonical"]; nb804 = 1.0 / mta_fixed(10 ** 10.5)[0]
    cw = cluster_window("canonical")
    check("K4 source facts: CFG828 SPARC overall median (recomputed), CFG828 rho(Delta, g_bar) over 29 dwarfs, CFG921 F0/F10, CFG823 median q, CFG922 U need, CFG804 census N",
          f"SPARC median {np.median(pts):+.4f} (|d| {k4a:.1e}, {len(pts)} pts, {len(SPARC)} galaxies); rho {rho828:+.3f} (N {len(rr)}); F0 {o921['F0']['obs']:+.3f}, "
          f"F10 {o921['F10']['obs']:+.3f}; q {J823['ups2']['median_q']:.3f}; U need {cw[0]:.3e} window [{cw[1]:.3e}, {cw[2]:.3e}]; N(10.5) {nb804:.4f}",
          k4a < 1e-9 and abs(rho828 + 0.47) < 0.005 and len(rr) == 29 and abs(o921["F10"]["obs"] + 1.356) < 5e-4 and abs(J823["ups2"]["median_q"] - 0.303) < 5e-4
          and abs(nb804 - 10.0) < 1e-9)
    # K5: native tables
    s8 = math.sqrt(sig2_R(8.0)); s8ref = J654["sets"]["NATIVE_CMB"]["sigma8_lin_native_growth"]
    cont = float(p_ext(np.array([KMAX]))[0] / PK[-1]); sl_tab = float(np.polyfit(np.log(KH[-50:]), np.log(PK[-50:]), 1)[0])
    kk2 = np.array([KMAX, KMAX * 1.01]); sl_ext = float(np.diff(np.log(p_ext(kk2)))[0] / math.log(1.01))
    check("K5 native tables: sigma8 from Plin_z0 vs CFG654 NATIVE_CMB; Delta_ta(0); D(0) = 1; P(k) extension continuous with matching slope",
          f"sigma8 {s8:.5f} vs {s8ref:.5f}; Delta_ta(0) {DTA0:.4f}; D(0) {D_of_z(0.0):.12f}; P_ext(kmax)/P {cont:.12f}; slope table {sl_tab:+.3f} ext {sl_ext:+.3f}; "
          f"Delta_vir {DVIR:.1f} (z_ta {Z_TA:.3f}); t0 {T_NOW * C.UNIT_GYR:.3f} Gyr",
          abs(s8 - s8ref) < 2e-3 and abs(DTA0 - 11.8977) < 1e-4 and abs(D_of_z(0.0) - 1) < 1e-12 and abs(cont - 1) < 1e-12 and abs(sl_tab - sl_ext) < 0.1)
    # K6: numerics
    cor = dict(reading="NB", C=3000, bnd="rta", smult=1); hal = Halo(1e6, A0X["canonical"], nu_e, cor)
    rq = 0.3 * hal.rs; num = quad(lambda r: 4 * math.pi * r * r * hal.rhos / ((r / hal.rs) * (1 + r / hal.rs) ** 2), 0, rq, epsrel=1e-12)[0]
    k6a = abs(num / float(hal.Mnfw(rq)) - 1)
    zc, Dc, ds2 = zcoll(hal.Mta); k6b = abs(erfc(DELTA_C * (1 / Dc - 1) / math.sqrt(2 * ds2)) - 0.5) + abs(D_of_z(zc) / Dc - 1)
    Mb, rh3, a0 = 1e6, 0.4, A0X["canonical"]; dE, _ = energy(hal, Mb, rh3, a0, nu_e)
    fq = lambda lr: (lambda r: float(law_profile(np.array([r]), Mb, rh3, a0, nu_e)[1][0]) * float(hal.Mdeb(r)) * Msun * r * KPC)(math.exp(lr))
    dq = quad(fq, math.log(hal.re) - 6 * math.log(10), math.log(hal.re), epsrel=1e-11, limit=400)[0]; k6c = abs(dE / dq - 1)
    Rp = 0.5 * hal.rb; sig = lambda R_: 2 * quad(lambda zz: float(hal.dMdr(math.hypot(R_, zz))) / (4 * math.pi * (R_ * R_ + zz * zz)) * hal.fex * (1 - FBN),
                                                    0, math.sqrt(max(hal.rb ** 2 - R_ ** 2, 0.0)), epsrel=1e-10, limit=200)[0]
    m2n = quad(lambda R_: 2 * math.pi * R_ * sig(R_), 0, Rp, epsrel=1e-8, limit=200)[0]; k6d = abs(proj_mass(hal, Rp) / m2n - 1)
    rr_ = np.logspace(-3, 1, 400); gN_, g_ = law_profile(rr_, Mb, rh3, a0, nu_e); phi_cum = simpson(g_, x=rr_ * KPC)
    phi_q = quad(lambda r: float(law_profile(np.array([r]), Mb, rh3, a0, nu_e)[1][0]) * KPC, 1e-3, 10.0, epsrel=1e-11, limit=400)[0]; k6e = abs(phi_cum / phi_q - 1)
    check("K6 numerics: NFW M(<r) vs quadrature; z_coll root (erfc = 1/2, D inverse); dE vs quadrature; projected mass vs double integral; law potential vs quadrature",
          f"{k6a:.1e}; {k6b:.1e}; {k6c:.1e}; {k6d:.1e}; {k6e:.1e}  (test halo: Mta {hal.Mta:.3e}, z_c {hal.zc:.2f}, c_b {hal.c:.1f}, r_s {hal.rs * 1e3:.1f} pc, r_b {hal.rb:.2f} kpc)",
          k6a < 1e-8 and k6b < 1e-8 and k6c < 1e-6 and k6d < 1e-4 and k6e < 1e-6)
    # K7a: f_s = 1 equals the bare law in every class (native, primary corner)
    d7 = 0.0
    for foot in FOOTS:
        W = build_world("N", foot, dict(reading="NB", C=3000, bnd="rta", smult=1))
        for k in ("U", "UL", "C", "Mc", "Ml", "I"):
            for o in W[k]: d7 = max(d7, abs(float(o.g(INF)) / o.glaw - 1))
        for o in W["S"]: d7 = max(d7, float(np.max(np.abs(o.g(INF) / o.glaw - 1))))
    check("K7a f_s = 1 (eps -> inf) equals the bare law in every class (native N-B, both footings)", f"max rel {d7:.1e}", d7 <= 1e-12)
    P(f"\n  SFH matches for M_formed ({len(set(MATCHED))} objects): " + ", ".join(f"{a}->{b}" for a, b in sorted(MATCHED.items())))


# ================================================================================================ driver
RES = dict(lane="CFG930", criteria="3dec25afe", mode=MODE)
PRIM = dict(reading="NA", C=3000, bnd="rta", smult=1)
FSTAR = dict(reading="NB", C=6000, bnd="rvir", smult=2)


def summarize(ev, foot):
    g = ev["grades"]
    s = f"    [{foot}] cal {ev['cal']['status']} (off0 {ev['cal']['off0']:+.3f}, offinf {ev['cal']['offinf']:+.3f})"
    s += (f"  eps* {ev['eps']:.3e}" if ev.get("eps") not in (None, INF) else (f"  A = {len(ev['A'])} grid pts" if ev.get("A") is not None else ""))
    s += f"  -> {ev['overall']}"
    P(s)
    for k in ("U", "C", "Mc", "Ml", "I", "S", "S3"):
        q = g[k]; P(f"        {k:3s} stat {q['stat']:+.3f}  err {q['err_stat']:.3f} (+) Ups {q['f_ups']:.3f} = {q['tot']:.3f}  z {q['z']:+.2f}  {q['label']}")


def jev(ev):
    out = {k: v for k, v in ev.items() if k not in ("grades",)}
    out["grades"] = {k: v for k, v in ev["grades"].items()}
    return out


if MODE == "K":
    run_K()

elif MODE == "MUTATE_eps0":
    P("\n" + "=" * 110 + "\nMUTATE M0: eps = 0 through the H-ELS path with CFG42's inputs (must reproduce CFG42's classical over-prediction)\n" + "=" * 110)
    d0 = 0.0; zs = {}
    for foot in FOOTS:
        W = build_world("K", foot, dict(reading="NA"), need_e=False)
        for key, k42 in (("C", "cls"), ("Mc", "col"), ("Ml", "m31")):
            med = float(np.median(sig_off(W[key], 0.0, "A", "NA"))); ref = J42["CL"][f"{k42}|{foot}|rule"]
            d0 = max(d0, abs(med - ref["med"])); zs[(key, foot)] = med / ref["tot"]
            P(f"    {foot:9s} {key}: median {med:+.4f} (CFG42 {ref['med']:+.4f}); z with CFG42's error {med / ref['tot']:+.2f}")
    bites = all(zs[(k, f)] < -1.5 for k in ("C", "Ml") for f in FOOTS)
    check("M0 eps = 0 (K inputs) reproduces CFG42's rule medians and over-predicts the MW classicals and the M31 LVD (z < -1.5)", f"max |d| {d0:.1e}; bites {bites}", d0 <= 1e-9 and bites)
    RES["native_eps0"] = {}
    for tag, cor in (("primary", PRIM), ("Fstar", FSTAR)):
        for foot in FOOTS:
            Ws = worlds("N", foot, cor); g = grade(Ws, 0.0, "A", cor["reading"])
            RES["native_eps0"][f"{tag}|{foot}"] = g
            P(f"    native eps = 0, {tag} {foot}: " + "  ".join(f"{k} {g[k]['stat']:+.3f} ({g[k]['z']:+.1f})" for k in ("U", "C", "Mc", "Ml", "I", "S", "S3")))
    RES["M0"] = dict(maxdev=d0, z=zs and {f"{k}|{f}": v for (k, f), v in zs.items()}, bites=bites)

elif MODE == "MUTATE_epsinf":
    P("\n" + "=" * 110 + "\nMUTATE Minf: eps -> inf (f_s = 1) must give the bare law in every class, both input sets\n" + "=" * 110)
    dK = 0.0
    for foot in FOOTS:
        W = build_world("K", foot, dict(reading="NA"))
        x = sig_off(W["U"], INF, "A", "NA"); xu = sig_off(W["UL"], INF, "A", "NA"); dK = max(dK, abs(km_median(x, xu) - J42["UF"][f"{foot}|law"]["km"]))
        for key, k42 in (("C", "cls"), ("Mc", "col"), ("Ml", "m31")):
            dK = max(dK, abs(float(np.median(sig_off(W[key], INF, "A", "NA"))) - J42["CL"][f"{k42}|{foot}|law"]["med"]))
    dN = 0.0; RES["native_law"] = {}; ncap = {}
    for foot in FOOTS:
        for cor in (PRIM, FSTAR, dict(reading="R1", C=3000, bnd="rta", smult=1)):
            W = build_world("N", foot, cor)
            for k in ("U", "UL", "C", "Mc", "Ml", "I", "S"):
                for o in W[k]:
                    ref = o.gN * nu_e(o.gN / A0X[foot]) if k != "I" else o.glaw
                    if cor["reading"] == "R1":                         # R1's f_s = 1 limit is the supply-capped law (A1 item 6)
                        capped = np.minimum(o.Mph, o.halo.Mc) < o.Mph; ncap[foot] = ncap.get(foot, 0) + int(np.sum(capped))
                        ref = o.gN + G * np.minimum(o.Mph, o.halo.Mc) * Msun / o.rm ** 2
                    dN = max(dN, float(np.max(np.abs(np.atleast_1d(o.g(INF, "A", cor["reading"])) / np.atleast_1d(ref) - 1))))
        g = grade(worlds("N", foot, PRIM), INF, "A", "NA"); RES["native_law"][foot] = g
        P(f"    bare law (native footing {foot}): " + "  ".join(f"{k} {g[k]['stat']:+.3f} ({g[k]['z']:+.1f})" for k in ("U", "C", "Mc", "Ml", "I", "S", "S3")))
    check("Minf f_s = 1: K inputs reproduce CFG42's committed law numbers (UFD KM, cls/col/m31 medians)", f"max |d| {dK:.1e}", dK <= 1e-9)
    check("Minf f_s = 1: native N-A and N-B F* equal the bare law at every object; R1 equals the supply-capped law", f"max rel {dN:.1e}; R1 points where the census supply caps the phantom: {ncap}", dN <= 1e-12)
    RES["R1_capped_points"] = ncap

elif MODE == "MUTATE_K":
    P("\n" + "=" * 110 + "\nMUTATE MK: full H-ELS calibration + grading with CFG42's LCDM inputs (capability check; NOT a verdict)\n" + "=" * 110)
    RES["MK"] = {}
    for foot in FOOTS:
        Ws = {uf: build_world("K", foot, dict(reading="NA"), uf) for uf in (1.0, 0.5, 2.0)}
        ev = evaluate(Ws, "A", "NA"); summarize(ev, foot); RES["MK"][foot] = jev(ev)
    ok = all(RES["MK"][f]["cal"]["status"].startswith("root") for f in FOOTS)
    check("MK the selector can act: with CFG42's inputs the calibrator (MW classicals) has a root on both footings", "; ".join(f"{f}: {RES['MK'][f]['cal']['status']}" for f in FOOTS), ok)

else:   # MAIN
    P("\n" + "=" * 110 + "\nMAIN: native inputs; 36 corners per footing; primary corner = N-A, C 3000, r_ta, census supply, Form A\n" + "=" * 110)
    P(f"  native: h {h_:.4f}  Om {Om:.4f}  Delta_ta(0) {DTA0:.4f}  Delta_vir {DVIR:.1f}  sigma8 {math.sqrt(sig2_R(8.0)):.4f}")
    CORN = []
    for rd in ("NA", "NB", "R1"):
        for Cc in (1500, 3000, 6000):
            for bnd in ("rta", "rvir"):
                for sm in (1, 2):
                    CORN.append(dict(reading=rd, C=Cc, bnd=bnd, smult=sm))
    RES["corners"] = {}; EVS = {}
    for cor in CORN:
        tag = f"{cor['reading']}|C{cor['C']}|{cor['bnd']}|x{cor['smult']}"; RES["corners"][tag] = {}
        for foot in FOOTS:
            Ws = worlds("N", foot, cor); ev = evaluate(Ws, "A", cor["reading"]); EVS[(tag, foot)] = (ev, Ws)
            cl = cluster_grade(foot, cor, eps_used(ev))
            ev["cluster"] = cl; RES["corners"][tag][foot] = jev(ev)
        fl = final_label([RES["corners"][tag][f]["overall"] for f in FOOTS]); RES["corners"][tag]["final"] = fl
        lab = lambda f: " ".join(f"{k}:{RES['corners'][tag][f]['labels'][k][:4]}" for k in GAL)
        P(f"  {tag:22s} final {fl:26s} | can {RES['corners'][tag]['canonical']['overall'][:12]:12s} {lab('canonical')} | alt {RES['corners'][tag]['alt']['overall'][:12]:12s} {lab('alt')}"
          f" | cluster {RES['corners'][tag]['canonical']['cluster']['label'][:12]}/{RES['corners'][tag]['alt']['cluster']['label'][:12]}")
    ptag = "NA|C3000|rta|x1"; ftag = "NB|C6000|rvir|x2"
    P("\n  PRIMARY CORNER (" + ptag + ")")
    for foot in FOOTS: summarize(EVS[(ptag, foot)][0], foot)
    P("\n  FAVOURABLE CORNER F* (" + ftag + ")")
    for foot in FOOTS: summarize(EVS[(ftag, foot)][0], foot)
    finals = [RES["corners"][t]["final"] for t in RES["corners"]]
    RES["primary_final"] = RES["corners"][ptag]["final"]
    RES["robust"] = all(f == RES["primary_final"] for f in finals)
    RES["corner_counts"] = {lab: finals.count(lab) for lab in sorted(set(finals))}
    P(f"\n  FINAL (primary corner): {RES['primary_final']}   robust over 36 corners: {RES['robust']}   counts {RES['corner_counts']}")
    # ---------------------------------------------------------------- variants at primary and F*
    P("\n  VARIANTS (reported; a flip marks the class FRAGILE)")
    VARS = {"formB": dict(form="B"), "selfgrav": dict(selfgrav=True), "nu_simple": dict(kern="nu_simple"), "mform_median": dict(mform="median"),
            "Z-1.71": dict(Z=-1.71), "Z-0.71": dict(Z=-0.71)}
    RES["variants"] = {}
    for base, cor in (("primary", PRIM), ("Fstar", FSTAR)):
        for vn, var in VARS.items():
            r_ = {}
            for foot in FOOTS:
                Ws = worlds("N", foot, cor, var); ev = evaluate(Ws, var.get("form", "A"), cor["reading"]); r_[foot] = jev(ev)
            r_["final"] = final_label([r_[f]["overall"] for f in FOOTS])
            bt = ptag if base == "primary" else ftag
            flips = sorted({k for f in FOOTS for k in GAL if r_[f]["labels"][k] != RES["corners"][bt][f]["labels"][k]})
            r_["flips"] = flips; RES["variants"][f"{base}|{vn}"] = r_
            P(f"    {base:7s} {vn:13s} final {r_['final']:26s} flips {flips if flips else '-'}  eps can {r_['canonical'].get('eps')}  alt {r_['alt'].get('eps')}")
    # ---------------------------------------------------------------- diagnostics
    P("\n  DIAGNOSTICS (no class weight)")
    D = {}
    for foot in FOOTS:
        W1 = build_world("N", foot, dict(reading="R1", C=3000, bnd="rta", smult=1))
        D1 = {}
        for k in ("U", "C", "Mc", "Ml", "I", "S"):
            du = np.array([o.dU for o in W1[k]]); D1[k] = dict(median=float(np.median(du)), frac_neg=float(np.mean(du < 0)), n=int(len(du)))
        D4 = {}
        for k in ("U", "C", "Mc", "Ml", "I"):
            q = np.array([float(o.McN / o.Mph) for o in W1[k]]); D4[k] = dict(median=float(np.median(q)), min=float(q.min()), max=float(q.max()), frac_gt1=float(np.mean(q > 1)))
        # D5: R1 maximum excess over all f_s (no energy rule), per object, then the class statistic
        fsg = np.linspace(0, 1, 201); D5 = {}
        for k in ("U", "UL", "C", "I"):
            best = []
            for o in W1[k]:
                gs = [float(o.gN + G * (min(float(o.Mph), f * o.halo.Mc) + (1 - f) * float(o.McN)) * Msun / o.rm ** 2) for f in fsg]
                best.append(max(gs) / float(o.gN * nu_e(o.gN / A0X[foot])))
            D5[k] = np.array(best)
        Wl = build_world("N", foot, PRIM, need_e=False)
        xU = sig_off(Wl["U"], INF, "A", "NA") - 0.5 * np.log10(D5["U"]); xUL = sig_off(Wl["UL"], INF, "A", "NA") - 0.5 * np.log10(D5["UL"])
        xC = sig_off(Wl["C"], INF, "A", "NA") - 0.5 * np.log10(D5["C"]); xI = iso_D(Wl["I"], INF, "A", "NA") - np.log10(D5["I"])
        D5o = dict(U_KM=float(km_median(xU, xUL)), U_law=float(km_median(sig_off(Wl["U"], INF, "A", "NA"), sig_off(Wl["UL"], INF, "A", "NA"))),
                   C_median=float(np.median(xC)), I_mean=float(xI.mean()), max_gain_U_dex_sigma=float(0.5 * np.log10(D5["U"]).max()),
                   median_gain_U_dex_sigma=float(0.5 * np.median(np.log10(D5["U"]))))
        # D2: who is starved (f_s with the N-B debris energy) at the primary (C, r_b, supply) and F*
        D2 = {}
        for tag, cor in (("NB|C3000|rta|x1", dict(reading="NB", C=3000, bnd="rta", smult=1)), (ftag, FSTAR)):
            ev, Ws = EVS[(tag, foot)]; e = eps_used(ev); Wn = Ws[1.0]; D2[tag] = dict(eps=e)
            for k in ("U", "C", "Mc", "Ml", "I", "S"):
                fs = np.array([o.fs(e, "NB") for o in Wn[k]]); mb = np.array([o.Mb for o in Wn[k]])
                rho = float(spearmanr(fs, mb)[0]) if np.ptp(fs) > 0 else float("nan")
                D2[tag][k] = dict(rho_fs_Mb=rho, fs_median=float(np.median(fs)), fs_min=float(fs.min()), fs_max=float(fs.max()),
                                  E1_over_dE_median=float(np.median([o.E1 / o.dE for o in Wn[k] if o.dE > 0])) if any(o.dE > 0 for o in Wn[k]) else None)
        D[foot] = dict(D1=D1, D4=D4, D5=D5o, D2=D2)
        P(f"    [{foot}] D1 R1 dU = U_set - U_prim: " + "  ".join(f"{k} med {D1[k]['median']:+.2e} J (neg {100 * D1[k]['frac_neg']:.0f}%)" for k in D1))
        P(f"    [{foot}] D4 Q_ap = M_cNFW(<r_ap)/M_ph(<r_ap): " + "  ".join(f"{k} med {D4[k]['median']:.3f} [{D4[k]['min']:.3f}, {D4[k]['max']:.3f}] >1: {100 * D4[k]['frac_gt1']:.0f}%" for k in D4))
        P(f"    [{foot}] D5 R1 max excess over f_s: U KM {D5o['U_KM']:+.3f} (law {D5o['U_law']:+.3f}; median gain {D5o['median_gain_U_dex_sigma']:+.3f}, max {D5o['max_gain_U_dex_sigma']:+.3f} dex in sigma);"
          f" C median {D5o['C_median']:+.3f}; I mean {D5o['I_mean']:+.3f}")
        for tag in D2:
            P(f"    [{foot}] D2 {tag} eps {D2[tag]['eps']:.3e}: " + "  ".join(
                f"{k} rho(fs,Mb) {D2[tag][k]['rho_fs_Mb']:+.2f} fs med {D2[tag][k]['fs_median']:.2f} E1/dE med {D2[tag][k]['E1_over_dE_median'] if D2[tag][k]['E1_over_dE_median'] is None else format(D2[tag][k]['E1_over_dE_median'], '.3g')}"
                for k in ("U", "C", "Ml", "I", "S")))
    # D3: the supply multiplier that would close the ultra-faints at eps = 0 under N-B
    D3 = {}
    for foot in FOOTS:
        def uoff(lnx):
            W = build_world("N", foot, dict(reading="NB", C=3000, bnd="rta", smult=1, Nx=10 ** lnx), need_e=False)
            return float(km_median(sig_off(W["U"], 0.0, "A", "NB"), sig_off(W["UL"], 0.0, "A", "NB")))
        u0, u5 = uoff(0.0), uoff(5.0)
        if u0 > 0 > u5:
            lx = brentq(uoff, 0.0, 5.0, xtol=1e-4); Nx = 10 ** lx
            cor = dict(reading="NB", C=3000, bnd="rta", smult=1, Nx=Nx); evx = {f: evaluate(worlds("N", f, cor), "A", "NB") for f in FOOTS}
            D3[foot] = dict(Nx=Nx, f_ret_equiv=0.10 / Nx, u0=u0, u5=u5, overall={f: evx[f]["overall"] for f in FOOTS}, eps={f: evx[f].get("eps") for f in FOOTS},
                            labels={f: evx[f]["labels"] for f in FOOTS}, cal={f: evx[f]["cal"] for f in FOOTS},
                            stats={f: {k: evx[f]["grades"][k]["stat"] for k in ("U", "C", "Mc", "Ml", "I", "S", "S3")} for f in FOOTS},
                            z={f: {k: evx[f]["grades"][k]["z"] for k in ("U", "C", "Mc", "Ml", "I", "S", "S3")} for f in FOOTS})
        else:
            D3[foot] = dict(Nx=None, u0=u0, u5=u5)
        P(f"    [{foot}] D3 supply multiplier closing the UFDs at eps = 0 (N-B): " + (f"N_x {D3[foot]['Nx']:.3g} (f_ret {D3[foot]['f_ret_equiv']:.2e}); UFD at x1 {u0:+.3f}, x1e5 {u5:+.3f}"
                                                                                      if D3[foot]["Nx"] else f"none in [1, 1e5] (x1 {u0:+.3f}, x1e5 {u5:+.3f})"))
        if D3[foot]["Nx"]:
            for f in FOOTS:
                P(f"          at N_x: [{f}] cal {D3[foot]['cal'][f]['status']} eps {D3[foot]['eps'][f]}  -> {D3[foot]['overall'][f]}  " + "  ".join(
                    f"{k} {D3[foot]['stats'][f][k]:+.3f} ({D3[foot]['z'][f][k]:+.1f})" for k in ("U", "C", "Mc", "Ml", "I", "S", "S3")))
    for foot in FOOTS: D[foot]["D3"] = D3[foot]
    RES["diagnostics"] = D
    # ---------------------------------------------------------------- sealed predictions (model output only; no data for them is read)
    SP = {}
    for tag in (ptag, ftag):
        SP[tag] = {}
        for foot in FOOTS:
            ev, Ws = EVS[(tag, foot)]; e = eps_used(ev); cor = dict(Ws[1.0]["meta"]["cor"]); a0 = A0X[foot]; rd = cor["reading"]
            grid = []
            for Ms in (1e5, 3e5, 1e6):
                for gr in (1.0, 3.0, 10.0):
                    for lgb in (-12.5, -12.0, -11.5):
                        out = {}
                        for kind, Mb, E1 in (("rotator", Ms * (1 + gr), ESN * Ms / MREM_CONST[-1.31]), ("dSph", Ms, ESN * Ms * BURST[-1.31] * ssp(-1.31, 13.3)[1] / ssp(-1.31, 13.3)[0])):
                            gb = 10 ** lgb; rm = math.sqrt(G * 0.5 * Mb * Msun / gb); r = rm / KPC
                            hal = Halo(Mb, a0, nu_e, cor); glaw = gb * float(nu_e(gb / a0))
                            o = Obj(r=r, rm=rm, gN=gb, glaw=glaw, E1=E1, halo=hal, Md=hal.Mdeb(r), McN=hal.McNFW(r), Mph=(glaw - gb) * rm ** 2 / G / Msun, tab=None, dE=0.0, dU=0.0)
                            if rd == "R1": o.dU, _ = r1_energy(hal, Mb, r, a0, nu_e)
                            else: o.dE, _ = energy(hal, Mb, r, a0, nu_e)
                            out[kind] = float(math.log10(float(o.g(e, "A", rd)) / glaw))
                        grid.append(dict(Ms=Ms, gas_over_Ms=gr, log_gbar=lgb, excess_rotator_dex_g=out["rotator"], excess_dSph_dex_g=out["dSph"],
                                         diff=out["rotator"] - out["dSph"]))
            Wn = Ws[1.0]; exc = np.array([math.log10(float(o.g(e, "A", rd)) / o.glaw) for o in Wn["C"]]); mf = np.array([o.E1 / ESN for o in Wn["C"]])
            rho = float(spearmanr(exc, mf)[0]) if np.ptp(exc) > 0 else None
            SP[tag][foot] = dict(eps=e, S2=grid, S3=dict(rho_excess_Mformed=rho, n=int(len(exc)), excess=[float(v) for v in exc], M_formed=[float(v) for v in mf],
                                                        names=[o.name for o in Wn["C"]]))
    # non-blind check of S3 on CFG827's seen values (MW classicals in CFG827, train set)
    nb = [(n, J827[n]["E_SFH"], mformed(n, 10 ** (0.4 * (4.83 - ns827["LVD"][n]["MV"])))) for n in J827 if J827[n]["train"]]
    rho_nb = float(spearmanr([x[1] for x in nb], [x[2] for x in nb])[0])
    RES["sealed"] = SP; RES["S3_nonblind_CFG827"] = dict(rho=rho_nb, rows=nb)
    lines = ["# CFG930 SEALED PREDICTIONS (model output of the frozen H-ELS model; written by the main run before any data for them is read)", "",
             "Criteria 3dec25afe (section 9). kappa = 1/2 FITTED; footings never pooled; not theory closed.", "",
             "## S1 tidal dwarf galaxies", "H-ELS assigns a tidal dwarf no primordial halo: predicted excess = 0 at every eps (same as the bare law).",
             "A TDG sample (gas counted, the same estimator) with mean excess > 2 se above the law contradicts H-ELS.", ""]
    for tag in (ptag, ftag):
        for foot in FOOTS:
            s = SP[tag][foot]
            lines.append(f"## {tag} | {foot} | eps used {s['eps']:.6e}")
            lines.append("S2 faint gas-rich rotators vs gas-poor dSphs at the same g_bar (excess = log10 g_HELS/g_law at the aperture, dex in g):")
            for q in s["S2"]:
                lines.append(f"  M* {q['Ms']:.0e}  gas/M* {q['gas_over_Ms']:>4.0f}  log g_bar {q['log_gbar']:+.1f}:  rotator {q['excess_rotator_dex_g']:+.4f}  dSph {q['excess_dSph_dex_g']:+.4f}  diff {q['diff']:+.4f}")
            r3 = s["S3"]["rho_excess_Mformed"]
            lines.append(f"S3 Spearman rho(predicted excess, M_formed) over the {s['S3']['n']} MW classical dSphs: " + ("undefined (zero predicted excess)" if r3 is None else f"{r3:+.3f}"))
            lines.append("")
    lines.append(f"S3 non-blind check (CFG827 E_SFH of its 8 MW classicals, seen before sealing; no weight): rho(E, M_formed) = {rho_nb:+.3f}")
    sp_txt = "\n".join(lines) + "\n"
    open(os.path.join(HERE, "SEALED_PREDICTIONS.md"), "w").write(sp_txt)
    hsh = hashlib.sha256(sp_txt.encode()).hexdigest()
    open(os.path.join(HERE, "SEALED_PREDICTIONS_SHA256.txt"), "w").write(f"{hsh}  SEALED_PREDICTIONS.md\n")
    RES["sealed_sha256"] = hsh
    P(f"\n  SEALED_PREDICTIONS.md sha256 {hsh}")
    P(f"  S3 non-blind (CFG827 MW classicals): rho(E, M_formed) {rho_nb:+.3f}")
    # K7 quick check inside MAIN: f_s = 1 equals the law at the primary corner
    d7 = 0.0
    for foot in FOOTS:
        Wn = EVS[(ptag, foot)][1][1.0]
        for k in ("U", "C", "Mc", "Ml", "I"):
            for o in Wn[k]: d7 = max(d7, abs(float(o.g(INF)) / o.glaw - 1))
    check("K7 (in MAIN) f_s = 1 equals the bare law at the primary corner", f"max rel {d7:.1e}", d7 <= 1e-12)
    RES["fex_A_stats"] = {}
    for foot in FOOTS:
        Wn = EVS[(ptag, foot)][1][1.0]
        RES["fex_A_stats"][foot] = {k: dict(max=float(max(o.halo.fex_A for o in Wn[k])), n_pos=int(sum(o.halo.fex_A > 0 for o in Wn[k])), n=len(Wn[k]),
                                            median_supply_over_edge_phantom=float(np.median([o.halo.Mc / o.halo.Mph_e for o in Wn[k]])))
                                    for k in ("U", "C", "Mc", "Ml", "I", "S")}
        P(f"  [{foot}] N-A leftover fraction f_ex: " + "  ".join(f"{k} n>0 {v['n_pos']}/{v['n']} max {v['max']:.3f} M_c/M_ph,edge med {v['median_supply_over_edge_phantom']:.3f}"
                                                         for k, v in RES["fex_A_stats"][foot].items()))
    # halo facts at the primary corner (canonical) for the README
    Wn = EVS[(ptag, "canonical")][1][1.0]; HF = {}
    for k in ("U", "C", "I", "S"):
        HF[k] = dict(zc_median=float(np.median([o.halo.zc for o in Wn[k]])), c_median=float(np.median([o.halo.c for o in Wn[k]])),
                     rs_kpc_median=float(np.median([o.halo.rs for o in Wn[k]])), rb_kpc_median=float(np.median([o.halo.rb for o in Wn[k]])),
                     Mta_over_Mb_median=float(np.median([o.halo.Mta / o.Mb for o in Wn[k]])))
    RES["halo_facts_canonical"] = HF
    P("  native halo facts (primary, canonical): " + "  ".join(f"{k}: z_c {v['zc_median']:.2f} c_b {v['c_median']:.0f} r_s {v['rs_kpc_median']:.3g} kpc r_b {v['rb_kpc_median']:.3g} kpc M_ta/M_b {v['Mta_over_Mb_median']:.1f}" for k, v in HF.items()))

# ================================================================================================ write
RES["checks"] = CHECKS; RES["runtime_s"] = round(time.time() - T0, 1)
try:
    import resource
    RES["peak_rss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 1)
except Exception:
    pass
nf = sum(not c["ok"] for c in CHECKS)
P(f"\n  {len(CHECKS) - nf}/{len(CHECKS)} checks pass   ({RES['runtime_s']} s)")


def _j(x):
    if isinstance(x, dict): return {str(k): _j(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [_j(v) for v in x]
    if isinstance(x, (np.floating, float)): return None if (isinstance(x, float) and math.isnan(x)) else (float(x) if math.isfinite(float(x)) else str(x))
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, np.ndarray): return _j(x.tolist())
    return x


json.dump(_j(RES), open(os.path.join(HERE, f"cfg930_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg930{SUF}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if nf else 0)
