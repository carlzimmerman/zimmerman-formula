#!/usr/bin/env python3
"""LWB1 (FROZEN_CRITERIA.md f4b3128cc1; AMENDMENT_A1 3f7cfa2127, KA1 check tail only): the weak-lensing amplitude row on the DESI DR1 Lensing Without Borders vectors.
Delta Sigma (KiDS-1000 / DES Y3 / HSC Y3 sources, conservative pairs, R >= 8 h^-1 Mpc) + wp (bias cancels), form B's spectrum
P_lin0 (engine EH, COPIED from BX1's bx1_pm.py) x N (BX1 pair A 512^3 splice) x R_tot (CO1), at KL1's neutrino-floor sigma8.
  nice -n 19 python3 lwb1.py                      -> lwb1.json, lwb1.out
  LWB1_MUTATE=MU1|MU2|MU3 nice -n 19 python3 lwb1.py -> lwb1_MUTATE_<id>.json, lwb1_MUTATE_<id>.out
Run from anywhere; paths are relative to this file. Data (outside git): ../_external_data/desi_dr1_lensing/extracted/.
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import sys, json, math, time
import numpy as np
from scipy.special import jv, spherical_jn
from scipy.optimize import minimize
from scipy.stats import chi2 as CH
from scipy.integrate import quad
from astropy.io import fits
trapz = getattr(np, "trapezoid", None) or np.trapz

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.join(REPO, "..", "_external_data"); DD = os.path.join(EXT, "desi_dr1_lensing", "extracted")
MUT = os.environ.get("LWB1_MUTATE", "")
TAG = f"_MUTATE_{MUT}" if MUT else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
FOOTS = ("canonical", "alt")

# ------------------------------------------------------------------ data: CFG315's loader (COPIED, MUTATE hooks added)
SURV = {"KiDS": 1, "DES": 2, "HSCY3": 3}
RMAX_OPT = {"KiDS": 1, "DES": 2, "HSCY3": 4}
LENS = {  # name: (sample, zmin, zmax, ilens in the joint covariance, conservative combos {survey: [1-based source bins]}, wp file tag)
    "BGS1": ("BGS_BRIGHT", 0.1, 0.2, 1, {"KiDS": [4, 5], "DES": [3, 4], "HSCY3": [2, 3, 4]}, "BGS_BRIGHT_GCcomb_0.1_0.2"),
    "BGS2": ("BGS_BRIGHT", 0.2, 0.3, 2, {"KiDS": [4, 5], "DES": [3, 4], "HSCY3": [2, 3, 4]}, "BGS_BRIGHT_GCcomb_0.2_0.3"),
    "BGS3": ("BGS_BRIGHT", 0.3, 0.4, 3, {"KiDS": [4, 5], "DES": [3, 4], "HSCY3": [2, 3, 4]}, "BGS_BRIGHT_GCcomb_0.3_0.4"),
    "LRG1": ("LRG", 0.4, 0.6, 1, {"KiDS": [4, 5], "DES": [4], "HSCY3": [3, 4]}, "LRG_GCcomb_0.4_0.6"),
    "LRG2": ("LRG", 0.6, 0.8, 2, {"HSCY3": [3, 4]}, "LRG_GCcomb_0.6_0.8"),
}
def fname(L, sv, k, bmode=False):
    s, a, b = LENS[L][:3]
    return os.path.join(DD, "ggl", sv, f"{'bmodes_' if bmode else ''}deltasigma_{s}_zmin_{a}_zmax_{b}_lenszbin_{k - 1}_blindA_boost_False.fits")
def load_cov(kind, x=False):
    base = os.path.join(DD, "covariances")
    idx = np.loadtxt(os.path.join(base, f"bin_ds_kids1000desy3hscy3_desiy1{kind}.dat"), comments="#")
    raw = np.loadtxt(os.path.join(base, f"{'dx' if x else 'ds'}covcorr_kids1000desy3hscy3_desiy1{kind}_pzwei.dat"), skiprows=1)
    n = len(idx); Cm = np.zeros((n, n)); Cm[raw[:, 0].astype(int) - 1, raw[:, 1].astype(int) - 1] = raw[:, 2]
    key = {(int(r[1]), int(r[2]), int(r[3]), int(r[4])): i for i, r in enumerate(idx)}
    return Cm, key
COV = {k: load_cov(k) for k in ("bgs", "lrg")}; COVX = {k: load_cov(k, True) for k in ("bgs", "lrg")}
RMAXT = np.loadtxt(os.path.join(DD, "covariances", "rmax_values.dat"), comments="#")
def rmax(L, sv):
    li = LENS[L][3] if LENS[L][0].startswith("BGS") else LENS[L][3] + 3
    return float(RMAXT[(RMAXT[:, 0] == RMAX_OPT[sv]) & (RMAXT[:, 1] == li), 2][0])
DATA = {}
for L, (s, a, b, il, combos, _) in LENS.items():
    kind = "bgs" if s.startswith("BGS") else "lrg"; key = COV[kind][1]
    for sv, ks in combos.items():
        for k in ks:
            t = fits.open(fname(L, sv, k))[1].data; tx = fits.open(fname(L, sv, k, True))[1].data
            ds = np.array(t["ds"], float); mb = np.array(t["magnification_bias"], float)
            if MUT == "MU1": ds, mb = ds * 0.85, mb * 0.85
            if MUT == "MU3" and sv == "KiDS": ds, mb = ds * 1.2, mb * 1.2
            DATA[(L, sv, k)] = dict(rp=np.array(t["rp"], float), lo=np.array(t["rp_min"], float), hi=np.array(t["rp_max"], float),
                                   ds=ds, mb=mb, dx=np.array(tx["ds"], float), zl=float(np.mean(t["z_l"])), kind=kind,
                                   cidx=np.array([key[(SURV[sv], il, k, i + 1)] for i in range(15)]))
WP = {}
for L in LENS:
    w = np.loadtxt(os.path.join(DD, "wp", f"wp_{LENS[L][5]}_default_angular_bitwise_log2_njack64_nran4_split20.txt"), comments="#")
    m = (w[:, 1] >= 5) & (w[:, 1] <= 20)
    WP[L] = dict(rp=w[m, 1], wp=w[m, 2] * (1.3 if MUT == "MU2" else 1.0), err=w[m, 3], all_rp=w[:, 1])
RP = {L: next(d for (l, _, _), d in DATA.items() if l == L)["rp"] for L in LENS}
ZL = {L: float(np.mean([d["zl"] for (l, _, _), d in DATA.items() if l == L])) for L in LENS}
P(f"LWB1{TAG}: {len(DATA)} Delta Sigma vectors; lens z_eff " + ", ".join(f"{L} {z:.3f}" for L, z in ZL.items())
  + "; wp radii kept " + ", ".join(f"{L} {np.round(WP[L]['rp'], 2).tolist()}" for L in LENS))
assert all(len(WP[L]["rp"]) == 2 for L in LENS)
for kind, (Cm, _) in COV.items():
    assert np.max(np.abs(Cm - Cm.T)) / np.max(np.diag(Cm)) < 1e-8 and np.linalg.eigvalsh(Cm).min() > 0
    assert COVX[kind][0].shape == Cm.shape

# ------------------------------------------------------------------ model: engine EH spectrum (COPIED from bx1_pm.py), growth, N, R_tot
h = 0.6736; om_b, om_c = 0.02237, 0.1200; Om_eng = (om_b + om_c) / h ** 2; NS, SIG8 = 0.965, 0.811
def T_eh(k):
    OB = om_b / h ** 2; omh2, fb = Om_eng * h * h, OB / Om_eng
    s = 44.5 * math.log(9.83 / omh2) / math.sqrt(1 + 10 * (OB * h * h) ** 0.75)
    ag = 1 - 0.328 * math.log(431 * omh2) * fb + 0.38 * math.log(22.3 * omh2) * fb ** 2
    gam = Om_eng * h * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
    q = k * (2.7255 / 2.7) ** 2 / (gam * h)
    L0 = np.log(2 * math.e + 1.8 * q); C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)
_KG = np.geomspace(1e-5, 100, 40000); _PK = _KG ** NS * T_eh(_KG * h) ** 2
_W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
_PK *= SIG8 ** 2 / (trapz(_PK * _W8(_KG * 8.0) ** 2 * _KG ** 2, _KG) / (2 * math.pi ** 2))
def P_lin0(k): return np.interp(np.log(np.maximum(k, 1e-5)), np.log(_KG), _PK, left=0, right=0)
def Dgrow(a, Om):
    E = lambda u: math.sqrt(Om / u ** 3 + 1 - Om)
    g = lambda x: quad(lambda u: 1.0 / (u * E(u)) ** 3, 0, x)[0] * E(x)
    return g(a) / g(1.0)
def fgrow(a, Om, e=1e-4): return (math.log(Dgrow(a * (1 + e), Om)) - math.log(Dgrow(a * (1 - e), Om))) / (2 * e)
KL1NU = json.load(open(os.path.join(REPO, "closure_2026_11_10", "KL1_lensing_amplitude_survey_assumptions", "kl1_nu.json")))["A1"]
TGT = {ft: KL1NU[ft]["sigma8_nu"] for ft in FOOTS}; OMF = {ft: KL1NU[ft]["Omega_m"] for ft in FOOTS}
SPL = json.load(open(os.path.join(REPO, "closure_2026_11_10", "BX1_fixed_amplitude_reference", "bx1_splice_pairA_N512.json")))["snap"]
KS = np.array(SPL["z0"]["k"]); NODE = {0.0: "z0", 0.5: "z0.5", 1.0: "z1"}
LNN = {z: np.log(np.array(SPL[n]["P"]) / (SPL[n]["D"] ** 2 * P_lin0(KS))) for z, n in NODE.items()}
def Nfac(k, z):
    zs = sorted(NODE); i = 0 if z <= 0.5 else 1; w = (z - zs[i]) / 0.5
    ln = LNN[zs[i]] + w * (LNN[zs[i + 1]] - LNN[zs[i]])
    out = np.exp(np.interp(np.log(k), np.log(KS), ln)); return np.where(k < KS[0], 1.0, out)
HM = json.load(open(os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed", "co1_hm.json"))); KH = np.array(HM["k"])
def Rtot(k, ft): return np.interp(np.log(k), np.log(KH), np.asarray(HM["primary"][ft]["R_tot"], float))
RHO = 2.775366e11 * 1e-12                     # h^2 Msun Mpc^-3 x (Mpc -> pc)^2 per Mpc: Delta Sigma in h Msun pc^-2

KK = np.geomspace(1e-4, 60.0, 120000); DAMP = np.exp(-(KK / 30.0) ** 2)
def ds_mm(Pk, Om, lo, hi, nsub=24):
    """bin area-averaged Delta Sigma_mm [h Msun pc^-2] for a spectrum array Pk on KK (bins whose upper edge is below 3 h^-1 Mpc: nan, never used)"""
    out = []
    for a, b in zip(lo, hi):
        if b < 3.0: out.append(np.nan); continue
        R = np.linspace(a, b, nsub); v = np.array([trapz(KK * Pk * DAMP * jv(2, KK * r), KK) / (2 * math.pi) for r in R])
        out.append(trapz(v * R, R) / trapz(R, R))
    return Om * RHO * np.array(out)
SG = np.geomspace(1.5, 320.0, 200); KX = np.geomspace(1e-4, 20.0, 40000); DAMPX = np.exp(-(KX / 10.0) ** 2)
def xi_ell(Pk, ell):
    """xi multipole base integral on SG from a spectrum array Pk on KK (re-sampled on KX)"""
    Px = np.exp(np.interp(np.log(KX), np.log(KK), np.log(np.maximum(Pk, 1e-300))))
    return np.array([trapz(KX ** 2 * Px * DAMPX * spherical_jn(ell, KX * s), KX) for s in SG]) / (2 * math.pi ** 2)
def wp_terms(Pk, rps, pimax):
    """[3, n_rp]: the b^2, b f and f^2 parts of the Kaiser wp (Hamilton 1992), integrated to pimax"""
    X0, X2, X4 = xi_ell(Pk, 0), -xi_ell(Pk, 2), xi_ell(Pk, 4)
    out = np.zeros((3, len(rps)))
    for j, rp in enumerate(rps):
        pi = np.linspace(0, pimax, 4001); s = np.sqrt(rp ** 2 + pi ** 2); mu = pi / s
        L2 = 0.5 * (3 * mu ** 2 - 1); L4 = (35 * mu ** 4 - 30 * mu ** 2 + 3) / 8
        x0 = np.interp(np.log(s), np.log(SG), X0); x2 = np.interp(np.log(s), np.log(SG), X2); x4 = np.interp(np.log(s), np.log(SG), X4)
        out[0, j] = 2 * trapz(x0, pi)
        out[1, j] = 2 * trapz(2 / 3 * x0 + 4 / 3 * x2 * L2, pi)
        out[2, j] = 2 * trapz(x0 / 5 + 4 / 7 * x2 * L2 + 8 / 35 * x4 * L4, pi)
    return out

# ------------------------------------------------------------------ templates per footing / variant at the target sigma8
def spectrum(ft, z, variant):
    Om = OMF[ft]; D = Dgrow(1 / (1 + z), Om)
    if variant.startswith("camb"):
        return CAMBP[variant](z, KK) * (Rtot(KK, ft) if variant == "camb_B" else 1.0)
    Pk = P_lin0(KK) * D ** 2 * (TGT[ft] / SIG8) ** 2
    if variant != "linear": Pk = Pk * Nfac(KK, z)
    return Pk * Rtot(KK, ft)
CAMBP = {}
def camb_setup():
    import camb
    def mk(H0, ombh2, omch2, ns, s8_target, Om_note):
        p = camb.CAMBparams(); p.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, mnu=0.06, num_massive_neutrinos=1)
        p.InitPower.set_params(As=2.1e-9, ns=ns); p.set_matter_power(redshifts=[0.0], kmax=60.0)
        p.NonLinear = camb.model.NonLinear_both; p.NonLinearModel.set_params(halofit_version="takahashi")
        r = camb.get_results(p); s8 = float(r.get_sigma8_0()); fac = (s8_target / s8) ** 2      # linear sigma8; As rescaled, then rerun
        p.InitPower.set_params(As=2.1e-9 * fac, ns=ns); r = camb.get_results(p)
        PI = camb.get_matter_power_interpolator(p, nonlinear=True, hubble_units=True, k_hunit=True, kmax=60.0, zmax=1.2,
                                                var1="delta_tot", var2="delta_tot")
        return (lambda z, k: np.where(k <= 60.0, PI.P(z, np.minimum(k, 60.0)), 0.0)), float(r.get_sigma8_0())
    out = {}
    out["camb_B"], out["camb_B_s8"] = mk(100 * h, om_b, om_c, NS, TGT["canonical"], OMF["canonical"])
    out["camb_P18"], out["camb_P18_s8"] = mk(67.66, 0.02242, 0.11933, 0.9665, 0.8102, 0.3097)
    return out

def templates(ft, variant, pimax, Om=None):
    Om = OMF[ft] if Om is None else Om; T = {}
    for L in LENS:
        z = ZL[L]; Pk = spectrum(ft, z, variant)
        d0 = next(d for (l, _, _), d in DATA.items() if l == L)
        f = fgrow(1 / (1 + z), Om)
        T[L] = dict(ds=ds_mm(Pk, Om, d0["lo"], d0["hi"]), wp=wp_terms(Pk, WP[L]["rp"], pimax), f=f)
    return T

# ------------------------------------------------------------------ the fit
def vector(svs, rmin=8.0, use_mb=True, wpcorr=0.0, cross=False):
    rows = []                                                  # (L, sv, k, mask)
    for L in LENS:
        for sv in svs:
            for k in LENS[L][4].get(sv, []):
                d = DATA[(L, sv, k)]; m = (d["rp"] >= rmin) & (d["rp"] <= rmax(L, sv))
                if m.any(): rows.append((L, sv, k, m))
    lenses = [L for L in LENS if any(r[0] == L for r in rows)]
    blocks = []; dvec = []; lab = []
    for kind in ("bgs", "lrg"):
        rr = [r for r in rows if DATA[r[:3]]["kind"] == kind]
        if not rr: continue
        ii = np.concatenate([DATA[r[:3]]["cidx"][r[3]] for r in rr]); C = (COVX if cross else COV)[kind][0]
        blocks.append(C[np.ix_(ii, ii)])
        for r in rr:
            d = DATA[r[:3]]; v = d["dx"] if cross else (d["ds"] - (d["mb"] if use_mb else 0.0)); dvec.append(v[r[3]])
            lab += [(r[0], np.where(r[3])[0][j]) for j in range(int(r[3].sum()))]
    nds = sum(len(b) for b in blocks)
    for L in lenses:
        e = WP[L]["err"]; c = np.diag(e ** 2); c[0, 1] = c[1, 0] = wpcorr * e[0] * e[1]; blocks.append(c); dvec.append(WP[L]["wp"])
    n = sum(len(b) for b in blocks); C = np.zeros((n, n)); o = 0
    for b in blocks: C[o:o + len(b), o:o + len(b)] = b; o += len(b)
    return dict(d=np.concatenate(dvec), Ci=np.linalg.inv(C), C=C, lab=lab, nds=nds, lenses=lenses, svs=svs, rows=rows)

def model(V, T, s, b, B=None):
    dsv = []
    for (L, i) in V["lab"]:
        j = V["lenses"].index(L); val = b[j] * s * T[L]["ds"][i]
        if B is not None: val = val + B[j] / RP[L][i] ** 2
        dsv.append(val)
    wpv = [s * (b[j] ** 2 * T[L]["wp"][0] + b[j] * T[L]["f"] * T[L]["wp"][1] + T[L]["f"] ** 2 * T[L]["wp"][2]) for j, L in enumerate(V["lenses"])]
    return np.concatenate([np.array(dsv)] + wpv)

def chi2_at(V, T, s, pm=False, x0=None):
    nl = len(V["lenses"]); npar = nl * (2 if pm else 1)
    def f(x):
        r = V["d"] - model(V, T, s, x[:nl], x[nl:] if pm else None); return float(r @ V["Ci"] @ r)
    starts = [np.r_[np.full(nl, 1.5), np.zeros(nl if pm else 0)]] if x0 is None else [x0]
    best = None
    for st in starts:
        r = minimize(f, st, method="L-BFGS-B", bounds=[(0.2, 5.0)] * nl + [(-1e3, 1e3)] * (nl if pm else 0), options=dict(ftol=1e-13, gtol=1e-9, maxiter=2000))
        if best is None or r.fun < best.fun: best = r
    return float(best.fun), best.x

GRID = np.arange(0.70, 0.9001, 0.0125)
def scan(V, T, tgt, pm=False):
    res = {}; x0 = None
    def ev(s8):
        nonlocal x0
        c, x = chi2_at(V, T, (s8 / tgt) ** 2, pm, x0); x0 = x; return c, x
    for s8 in GRID: res[round(float(s8), 6)] = ev(float(s8))
    while True:
        ss = sorted(res); c2 = np.array([res[s][0] for s in ss]); i = int(np.argmin(c2))
        if i == 0 and ss[0] > 0.50 + 1e-9: s = round(ss[0] - 0.0125, 6); res[s] = ev(s); continue
        if i == len(ss) - 1 and ss[-1] < 1.10 - 1e-9: s = round(ss[-1] + 0.0125, 6); res[s] = ev(s); continue
        break
    ss = np.array(sorted(res)); c2 = np.array([res[s][0] for s in ss]); i = int(np.argmin(c2))
    lo_, hi_ = max(i - 2, 0), min(i + 3, len(ss)); co = np.polyfit(ss[lo_:hi_], c2[lo_:hi_], 2)
    sb = float(-co[1] / (2 * co[0])) if co[0] > 0 else float(ss[i]); wid = 1 / math.sqrt(co[0]) if co[0] > 0 else float("nan")
    cmin, xb = chi2_at(V, T, (sb / tgt) ** 2, pm)
    N = len(V["d"]); npar = 1 + len(V["lenses"]) * (2 if pm else 1); dof = N - npar
    c_t, _ = chi2_at(V, T, 1.0, pm)
    return dict(best_sigma8=sb, width=wid, chi2_min=cmin, N=N, dof=dof, p=float(CH.sf(cmin, dof)), b=[float(v) for v in xb[:len(V["lenses"])]],
                gap=(tgt - sb) / wid, chi2_target=c_t, dchi2_target=c_t - cmin, edge=bool(i in (0, len(ss) - 1)))

def label(r):
    if r["p"] < 0.01: return "NO VERDICT (fit p < 0.01)"
    if not (r["width"] <= 0.05): return "NO POWER"
    g = r["gap"]
    if -2 <= g <= 2: return "AMPLITUDE CONSISTENT"
    if 2 < g <= 3: return "GAP STAYS"
    return "TENSION (theory above the data)" if g > 3 else "TENSION (data above the theory)"

VEC = {"J": ["KiDS", "DES", "HSCY3"], "KiDS": ["KiDS"], "DES": ["DES"], "HSCY3": ["HSCY3"], "K+D": ["KiDS", "DES"]}
RES = dict(lane="LWB1", criteria="f4b3128cc1", amendment_A1="3f7cfa2127", mutate=MUT or None, note="kappa = 1/2 FITTED; not theory closed; adopts nothing; TEST lane",
           target=TGT, Omega_m=OMF, z_eff=ZL, KA={}, primary={}, brackets={}, labels={})

# ------------------------------------------------------------------ known answers that do not need the data
if not MUT:
    g = 1.8; Ppl = KK ** (g - 3.0); r0 = 1.0
    from scipy.special import gamma as Gm
    A = Gm(g - 1) * math.sin(math.pi * (g - 1) / 2) / (2 * math.pi ** 2)      # analytic: P = k^(g-3) -> xi = A r^-g
    rps = np.array([2.0, 5.0, 10.0, 30.0]); wpa = A * rps ** (1 - g) * math.sqrt(math.pi) * Gm((g - 1) / 2) / Gm(g / 2)
    X0 = xi_ell(Ppl, 0); wpn = []
    for rp in rps:
        pi = np.geomspace(1e-3, 3000, 20001); s = np.sqrt(rp ** 2 + pi ** 2)
        xs = np.where(s <= SG[-1], np.interp(np.log(s), np.log(SG), X0), A * s ** (-g)); wpn.append(2 * trapz(xs, pi) + 2 * A * pi[-1] ** (1 - g) / (g - 1))   # AMENDMENT A1: analytic tail beyond pi 3000
    wpn = np.array(wpn); dsa = A * rps ** (1 - g) * math.sqrt(math.pi) * Gm((g - 1) / 2) / Gm(g / 2) * (g - 1) / (3 - g)
    dsn = np.array([trapz(KK * Ppl * DAMP * jv(2, KK * r), KK) / (2 * math.pi) for r in rps])
    e1 = float(np.max(np.abs(wpn / wpa - 1))); e2 = float(np.max(np.abs(dsn / dsa - 1)))
    RES["KA"]["KA1"] = dict(wp_max_rel=e1, ds_max_rel=e2, pass_=bool(e1 <= 0.01 and e2 <= 0.01))
    P(f"KA1 transforms (power law gamma 1.8, r_p 2-30): wp max rel err {e1:.4f}, Delta Sigma {e2:.4f} -> {'PASS' if RES['KA']['KA1']['pass_'] else 'FAIL'}")
    ka2 = {}
    for ft in FOOTS:
        Pk = P_lin0(_KG) * (TGT[ft] / SIG8) ** 2; s8 = math.sqrt(trapz(Pk * _W8(_KG * 8.0) ** 2 * _KG ** 2, _KG) / (2 * math.pi ** 2))
        ka2[ft] = dict(sigma8=s8, rel=s8 / TGT[ft] - 1, pass_=bool(abs(s8 / TGT[ft] - 1) <= 0.003))
    RES["KA"]["KA2"] = ka2; P("KA2 normalisation: " + "; ".join(f"{ft} {v['sigma8']:.5f} vs {TGT[ft]:.5f} -> {'PASS' if v['pass_'] else 'FAIL'}" for ft, v in ka2.items()))
    nk = {z: [float(np.exp(np.interp(np.log(kk), np.log(KS), LNN[z]))) for kk in (0.05, 0.1, 0.2, 0.5, 1.0)] for z in LNN}
    RES["N_pairA"] = nk; P("reported: BX1 pair A nonlinear ratio N at k 0.05, 0.1, 0.2, 0.5, 1: " + "; ".join(f"z {z}: " + " ".join(f"{v:.3f}" for v in nk[z]) for z in nk))

# ------------------------------------------------------------------ primary and brackets
VV = {nm: vector(sv) for nm, sv in VEC.items()}
for nm, V in VV.items(): P(f"vector {nm}: {V['nds']} Delta Sigma points + {2 * len(V['lenses'])} wp points; lens bins {V['lenses']}")
for ft in FOOTS:
    T40 = templates(ft, "pair", 40.0); RES["primary"][ft] = {}; RES["labels"][ft] = {}
    P(f"\n[{ft}] target sigma8 {TGT[ft]:.4f}, Omega_m {OMF[ft]:.5f}")
    for nm, V in VV.items():
        if MUT and nm not in ("J", "KiDS", "DES"): continue
        r = scan(V, T40, TGT[ft]); r["label"] = label(r); RES["primary"][ft][nm] = r
        P(f"  {nm:6s} best sigma8 {r['best_sigma8']:.4f} +- {r['width']:.4f}  gap {r['gap']:+.2f} widths  chi2 {r['chi2_min']:.2f}/{r['dof']} p {r['p']:.3f}  "
          f"Delta chi2 at target {r['dchi2_target']:+.2f}  b {np.round(r['b'], 3).tolist()} -> {r['label']}{'  [edge]' if r['edge'] else ''}")
    if MUT: continue
    br = {}
    for pm_ in (80.0, 100.0, 300.0):
        T = templates(ft, "pair", pm_); br[f"pimax_{int(pm_)}"] = {nm: scan(VV[nm], T, TGT[ft]) for nm in VEC}
    br["point_mass"] = {nm: scan(VV[nm], T40, TGT[ft], pm=True) for nm in VEC}
    for rm in (5.0, 12.0): br[f"rmin_{int(rm)}"] = {nm: scan(vector(VEC[nm], rmin=rm), T40, TGT[ft]) for nm in VEC}
    br["no_magnification_column"] = {nm: scan(vector(VEC[nm], use_mb=False), T40, TGT[ft]) for nm in VEC}
    br["wp_corr_0p5"] = {nm: scan(vector(VEC[nm], wpcorr=0.5), T40, TGT[ft]) for nm in VEC}
    Tl = templates(ft, "linear", 40.0); br["N_equals_1"] = {nm: scan(VV[nm], Tl, TGT[ft]) for nm in VEC}
    if not CAMBP: CAMBP.update(camb_setup())
    Tc = templates(ft, "camb_B", 40.0); br["camb_halofit_B"] = {nm: scan(VV[nm], Tc, TGT[ft]) for nm in VEC}
    for k_, v_ in br.items():
        for nm, r in v_.items(): r["label"] = label(r)
        P(f"  bracket {k_:24s} " + "  ".join(f"{nm} {r['best_sigma8']:.4f}+-{r['width']:.4f} g {r['gap']:+.2f} p {r['p']:.2f}" for nm, r in v_.items()))
    RES["brackets"][ft] = br
    lj = RES["primary"][ft]["J"]["label"]; pim = [lj] + [br[f"pimax_{p_}"]["J"]["label"] for p_ in (80, 100)]
    flips = {nm: sorted({k_ for k_, v_ in br.items() if v_[nm]["label"] != RES["primary"][ft][nm]["label"]}) for nm in VEC}
    RES["labels"][ft] = dict(pimax_labels_J=pim, pimax_agree=bool(len(set(pim)) == 1), flips=flips)
    P(f"  J label across pi_max 40 / 80 / 100: {pim}; brackets that flip a label: {flips}")

if not MUT:
    # KA3 null: cross component, template b_L x Delta Sigma_mm from J canonical primary
    T40 = templates("canonical", "pair", 40.0); bJ = dict(zip(VV["J"]["lenses"], RES["primary"]["canonical"]["J"]["b"])); ka3 = {}
    for nm in ("KiDS", "DES", "HSCY3", "J"):
        V = vector(VEC[nm], cross=True); n = V["nds"]; d = V["d"][:n]; C = V["C"][:n, :n]; Ci = np.linalg.inv(C)
        t = np.array([bJ[L] * T40[L]["ds"][i] for (L, i) in V["lab"]]); F = t @ Ci @ t; A_ = (t @ Ci @ d) / F; sA = 1 / math.sqrt(F)
        ka3[nm] = dict(A=float(A_), sigma=float(sA), z=float(A_ / sA), chi2_null=float(d @ Ci @ d), N=n, pass_=bool(abs(A_ / sA) < 3))
    RES["KA"]["KA3"] = ka3; P("\nKA3 cross-component amplitude (fraction of the E-mode template): " + "; ".join(f"{k} {v['A']:+.3f} +- {v['sigma']:.3f} ({v['z']:+.1f} sigma)" for k, v in ka3.items())
                             + f" -> {'PASS' if all(v['pass_'] for v in ka3.values()) else 'FAIL'}")
    # KA4 blinding slope: survey ratio to DES per lens bin, all released radii above the blending cut and below both R_max
    ka4 = {}
    for sv in ("KiDS", "HSCY3"):
        cs, ws = [], []
        for L in LENS:
            if "DES" not in LENS[L][4] or sv not in LENS[L][4]: continue
            kind = DATA[(L, "DES", LENS[L][4]["DES"][0])]["kind"]; Cm = COV[kind][0]
            prof = {}
            for s_ in (sv, "DES"):
                ks = LENS[L][4][s_]; rp = DATA[(L, s_, ks[0])]["rp"]
                m = (rp >= 0.25) & (rp <= min(rmax(L, sv), rmax(L, "DES")))
                ii = np.concatenate([DATA[(L, s_, k)]["cidx"][m] for k in ks]); d = np.concatenate([(DATA[(L, s_, k)]["ds"] - DATA[(L, s_, k)]["mb"])[m] for k in ks])
                X = np.vstack([np.eye(int(m.sum()))] * len(ks)); Ci = np.linalg.inv(Cm[np.ix_(ii, ii)]); F = X.T @ Ci @ X
                Wt = np.linalg.solve(F, X.T @ Ci); prof[s_] = (Wt @ d, Wt, ii, rp[m])
            (a_, Wa, ia, rr), (b_, Wb, ib, _) = prof[sv], prof["DES"]
            Cab = lambda i1, i2: Cm[np.ix_(i1, i2)]
            Caa = Wa @ Cab(ia, ia) @ Wa.T; Cbb = Wb @ Cab(ib, ib) @ Wb.T; Cba = Wa @ Cab(ia, ib) @ Wb.T
            r = a_ / b_; Ja = np.diag(1 / b_); Jb = np.diag(-a_ / b_ ** 2)
            Cr = Ja @ Caa @ Ja.T + Jb @ Cbb @ Jb.T + Ja @ Cba @ Jb.T + Jb @ Cba.T @ Ja.T
            X = np.vstack([np.ones_like(rr), np.log(rr)]).T; Ci = np.linalg.inv(Cr); F = X.T @ Ci @ X; par = np.linalg.solve(F, X.T @ Ci @ r)
            cs.append(par[1]); ws.append(1 / np.linalg.inv(F)[1, 1])
        cs, ws = np.array(cs), np.array(ws); cbar = float(np.sum(cs * ws) / ws.sum()); sc = float(1 / math.sqrt(ws.sum()))
        ka4[sv] = dict(slopes=cs.tolist(), slope=cbar, sigma=sc, z=cbar / sc, pass_=bool(abs(cbar / sc) < 3))
    RES["KA"]["KA4"] = ka4; P("KA4 survey/DES ratio slope in ln R (pooled over lens bins): " + "; ".join(f"{k} {v['slope']:+.4f} +- {v['sigma']:.4f} ({v['z']:+.1f} sigma)" for k, v in ka4.items())
                             + f" -> {'PASS' if all(v['pass_'] for v in ka4.values()) else 'FAIL'}")
    # KA5 Planck18 LCDM on K+D
    OmP = 0.3097; ZLs = ZL
    def spectrumP(z): return CAMBP["camb_P18"](z, KK)
    TP = {}
    for L in LENS:
        d0 = next(d for (l, _, _), d in DATA.items() if l == L); Pk = spectrumP(ZL[L])
        TP[L] = dict(ds=ds_mm(Pk, OmP, d0["lo"], d0["hi"]), wp=wp_terms(Pk, WP[L]["rp"], 40.0), f=fgrow(1 / (1 + ZL[L]), OmP))
    r = scan(VV["K+D"], TP, 0.8102); S8 = r["best_sigma8"] * math.sqrt(OmP / 0.3); wS = r["width"] * math.sqrt(OmP / 0.3)
    tol = 2 * math.sqrt(wS ** 2 + 0.023 ** 2)
    RES["KA"]["KA5"] = dict(sigma8=r["best_sigma8"], width=r["width"], S8=S8, S8_width=wS, ref=0.794, tol=tol, p=r["p"], camb_s8=CAMBP["camb_P18_s8"],
                            pass_=bool(abs(S8 - 0.794) <= tol), provisional_source=True)
    P(f"KA5 Planck18 LCDM (CAMB halofit) on K+D: sigma8 {r['best_sigma8']:.4f} +- {r['width']:.4f}, S8 {S8:.4f} +- {wS:.4f} vs 0.794 +- 0.023 (tol {tol:.3f}), p {r['p']:.3f} "
      f"-> {'PASS' if RES['KA']['KA5']['pass_'] else 'FAIL'} (PROVISIONAL source)")
    RES["KA_ok"] = bool(RES["KA"]["KA1"]["pass_"] and all(v["pass_"] for v in RES["KA"]["KA2"].values()) and all(v["pass_"] for v in ka3.values())
                        and all(v["pass_"] for v in ka4.values()) and RES["KA"]["KA5"]["pass_"])
    for ft in FOOTS:
        lj = RES["primary"][ft]["J"]["label"]
        final = lj if (RES["KA_ok"] and RES["labels"][ft]["pimax_agree"]) else "NO VERDICT"
        RES["labels"][ft]["lane"] = final
        P(f"LANE LABEL [{ft}]: {final}  (J primary {lj}; KA_ok {RES['KA_ok']}; pi_max agree {RES['labels'][ft]['pimax_agree']})")
P(f"\ndone in {time.time() - T0:.0f} s")
json.dump(RES, open(os.path.join(HERE, f"lwb1{TAG}.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
open(os.path.join(HERE, f"lwb1{TAG}.out"), "w").write("\n".join(OUT) + "\n")
