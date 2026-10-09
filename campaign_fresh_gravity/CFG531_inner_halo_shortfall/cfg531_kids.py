#!/usr/bin/env python3
"""CFG531 KiDS arm (FROZEN_CRITERIA.md, criteria commit 750fa1f55): the inner-bin deficit as eps = Delta M(<r)/M_pred(<r).
Machinery: CFG529's cfg529_score.py exec'd read-only up to its controls block (data, f30-matched environment, constructions A / B,
own-profile mixing, SHMR delta in the covariance).  New: the GLS amplitude eps of the stacked own law profile per band; LAW_RTA own
tables rebuilt per group (CFG503's cfg503_own.py law code, copied) for stellar-mass shifts, an IMF rising with mass and two kernels;
stripping variants; early / late split; mass tertiles.  Construction B: shifts enter additively (declared in the criteria).
Rebuilt tables are cached in ../../../_external_data/cfg531_work/ (not committed).
MUTATE (CFG531_MUTATE=1, outputs *_MUTATE.*): MU1 uniform injection, MU2 isothermal injection (method), MU3 type shuffle, MU4 null mock.
Run: nice -n 10 python3 cfg531_kids.py ; CFG531_MUTATE=1 nice -n 10 python3 cfg531_kids.py
"""
import os, sys, io, math, json, time, contextlib, multiprocessing as mp
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy import stats
from scipy.interpolate import RegularGridInterpolator

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
MUTATE = os.environ.get("CFG531_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg531_work"))
os.makedirs(WORK, exist_ok=True)
LOG, CHK = [], {}
RES = {"lane": "CFG531", "script": "cfg531_kids", "mutate": MUTATE, "criteria_commit": "750fa1f55",
       "settings": "kappa = 1/2 FITTED; footings never pooled; nu_mono; cold energy mass still required; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


try:
    os.nice(10)
except OSError:
    pass

# ------------------------------------------------------------------ CFG529 machinery (read-only exec up to its controls block)
P529 = os.path.join(LANES, "CFG529_f30_matched_environment", "cfg529_score.py")
_src = open(P529).read()
_cut = _src.index("# ------------------------------------------------------------------ controls K2-K6")
NS = {"__file__": P529, "__name__": "cfg529_ro"}
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(_src[:_cut], "cfg529_score", "exec"), NS)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
C, LL = NS["C"], NS["LL"]
SHMRS, FOOTS, CONS = NS["SHMRS"], NS["FOOTS"], NS["CONS"]
GP, F30, WW, WG, patch = NS["GP"], NS["F30"], NS["WW"], NS["WG"], NS["patch"]
MEAS, HOD, env_cfg, evec, own_rec, model_score, edge_tabs = (NS[k] for k in ("MEAS", "HOD", "env_cfg", "evec", "own_rec", "model_score", "edge_tabs"))
ET3, OT3, OT4, T29, hart, KG = NS["ET3"], NS["OT3"], NS["OT4"], NS["T29"], NS["hart"], NS["KG"]
LMS, ZG, LRG, NPATCH = NS["LMS"], NS["ZG"], NS["LRG"], NS["NPATCH"]
gi, GM, GZ, GS = GP.gi, GP.GM, GP.GZ, GP.GS
NGRP = GP.NG
P(f"CFG529 machinery exec'd read-only ({len(_buf.getvalue().splitlines())} lines of its header output suppressed); "
  f"K1 / K7 of CFG529: {[k for k, v in NS['CHK'].items() if v['ok']]}")
lens = NS["lens"]
TYP = lens["typ"].astype(int)
LMSL = lens["logM"].astype(float)
MGL = lens["Mgal"].astype(float)
J529 = json.load(open(os.path.join(LANES, "CFG529_f30_matched_environment", "cfg529_score_results.json")))
J468 = json.load(open(os.path.join(LANES, "CFG468_kernel_family", "cfg468_kernel_family_results.json")))
A0F = {f: C.A0[f] for f in FOOTS}                                                # internal units ((km/s)^2/Mpc)
A0SI = dict(C.A0_SI)

# ------------------------------------------------------------------ bands
BANDS = {"K-in": [12, 13, 14], "K-mid": [9, 10, 11], "K-out": [6, 7, 8], "K9": list(range(6, 15))}
GE = C.GEDGE_K
GC_ = np.sqrt(GE[:-1] * GE[1:])


# ------------------------------------------------------------------ data per mask (CFG529's estimator; LOO kept for the class difference)
def esd_loo(mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch[mask], weights=WG[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch[mask], weights=WW[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev, loo


def gstack(tab, mask):
    """CFG529's GSet.stack (stack-weighted group average) for an arbitrary lens mask."""
    out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NGRP)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out


def fo_of(fg):
    return np.clip(GP.interp(np.clip(fg, 0, 1)), 0, 1)[:, None]


# ------------------------------------------------------------------ own law tables (rebuild; CFG503 cfg503_own.py law code, copied)
RTC = ET3["RTC"]
RTI = {f"{s}_W30": RegularGridInterpolator((LMS, ZG), ET3[f"{s}_W30_RTW"], bounds_error=False, fill_value=None) for s in SHMRS}


def rt_weights(tag, lms, z):
    w = RTI[tag]([[min(max(lms, LMS[0]), LMS[-1]), min(max(z, ZG[0]), ZG[-1])]])[0]
    w = np.maximum(w, 0.0)
    return w / w.sum()


def truncate(r, Md, w):
    out = w[-1] * Md
    nz = np.nonzero(w[:-1] > 0)[0]
    if len(nz):
        rt = RTC[nz]
        out = out + (w[nz, None] * np.interp(np.minimum(r[None, :], rt[:, None]), r, Md)).sum(0)
    return out


def nu_simple(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def nu_standard(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.exp(0.5 * np.arcsinh(0.5 * y)) / np.sqrt(y)


KERN = {"mono": C.nu_mono, "simple": nu_simple, "standard": nu_standard}


def r_ta_law_k(Mb, a0, z, nu):
    from scipy.optimize import brentq
    a = 1 / (1 + z)
    rho = C.OM * C.RHOC0 / a ** 3 * C.dta(z)
    f = lambda lr: math.log(Mb * float(nu(C.G_MPC * Mb / math.exp(2 * lr) / a0))) - math.log(4 * math.pi / 3 * math.exp(3 * lr) * rho)
    return math.exp(brentq(f, math.log(1e-5), math.log(1e3), xtol=1e-12))


def fin(Mnode, Mpt, r, Md):
    """CFG503's kids_fin with the bin radii fixed by the data's M_gal (Mnode) and the model's point mass Mpt."""
    return C._finish(lambda R: C.dsigma(R, r, Md) + Mpt / (math.pi * R ** 2), Mnode)


def law_vecs(args):
    """per group: full, tr_moster_W30, tr_behroozi_W30 for both footings; Mg' = Mg + M*(10^dl - 1); kernel kn; a0 x afac."""
    Mg, zl, lms, dl, kn, afac, lms_w = args
    nu = KERN[kn]
    Ms = 10 ** lms
    Mp = Mg + Ms * (10 ** dl - 1.0)
    W = {s: rt_weights(f"{s}_W30", lms_w, zl) for s in SHMRS}
    out = np.zeros((2, 3, 15))
    for i, foot in enumerate(FOOTS):
        a0 = A0F[foot] * afac
        rta = C.r_ta_law(Mp, a0, zl) if kn == "mono" else r_ta_law_k(Mp, a0, zl, nu)
        r = np.geomspace(1e-4, rta, 1500)
        Md = Mp * (nu(C.G_MPC * Mp / r ** 2 / a0) - 1.0)
        out[i, 0] = fin(Mg, Mp, r, Md)
        for j, s in enumerate(SHMRS):
            out[i, 1 + j] = fin(Mg, Mp, r, truncate(r, Md, W[s]))
    return out


GSEL = np.asarray(T29["GSEL"])
ms_f30 = np.bincount(gi[F30], minlength=NGRP) > 0
assert np.array_equal(np.sort(GSEL), np.nonzero(ms_f30)[0]), "GSEL != f30 groups"
a0r = {k: {t: J468["sparc"]["kernels"][f"nu_{k}"][t]["a0"] / J468["sparc"]["kernels"]["nu_mono"][t]["a0"] for t in ("T-free", "T-fix")}
       for k in ("simple", "standard")}
imf = lambda lms: 0.25 * np.clip((lms - 10.3) / 1.0, 0, 1)
DELTAS = (0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40)
VARS = {"d0": (0.0, "mono", 1.0, False)}
for d_ in DELTAS:
    VARS[f"d{d_:.2f}"] = (d_, "mono", 1.0, False)
VARS["IMF"] = ("imf", "mono", 1.0, False)
for d_ in (0.15, 0.20):
    VARS[f"d{d_:.2f}_envshift"] = (d_, "mono", 1.0, True)
for k in ("simple", "standard"):
    for t in ("T-free", "T-fix"):
        VARS[f"kern_{k}_{t}"] = (0.0, k, a0r[k][t], False)
CACHE = os.path.join(WORK, "cfg531_law_tables.npz")
if os.path.exists(CACHE):
    TAB = dict(np.load(CACHE))
    P(f"law tables read from cache ({len(TAB)} variants)")
else:
    TAB = {}
    ctx = mp.get_context("fork")
    with ctx.Pool(4) as pool:
        for name, (d_, kn, af, envs) in VARS.items():
            args = []
            for g in GSEL:
                dl = float(imf(GS[g])) if d_ == "imf" else d_
                args.append((float(GM[g]), float(GZ[g]), float(GS[g]), dl, kn, af, float(GS[g] + (dl if envs else 0.0))))
            res = pool.map(law_vecs, args, chunksize=16)
            TAB[name] = np.array(res)
            P(f"  law tables {name:24s} done ({time.time() - T0:.0f} s)")
    np.savez(CACHE, **TAB)
RES["a0_ratio_CFG468"] = a0r


def own_from_tab(name, foot):
    """(NG, 15) per SHMR, full and tr_W30, construction A, with every non-f30 group = CFG503's committed rows (zero weight in f30)."""
    i = FOOTS.index(foot)
    out = {}
    for j, s in enumerate(SHMRS):
        full = OT3[f"P|{foot}|LAW_RTA|full_{s}"].copy(); tr = OT3[f"P|{foot}|LAW_RTA|tr_{s}_W30"].copy()
        full[GSEL] = TAB[name][:, i, 0]; tr[GSEL] = TAB[name][:, i, 1 + j]
        out[s] = (full, tr)
    return out


# K2: rebuilt d0 tables = CFG503's committed ones
k2 = 0.0
for foot in FOOTS:
    i = FOOTS.index(foot)
    for j, s in enumerate(SHMRS):
        a = TAB["d0"][:, i, 0]; b = OT3[f"P|{foot}|LAW_RTA|full_{s}"][GSEL]
        k2 = max(k2, float(np.max(np.abs(a / b - 1))))
        a = TAB["d0"][:, i, 1 + j]; b = OT3[f"P|{foot}|LAW_RTA|tr_{s}_W30"][GSEL]
        k2 = max(k2, float(np.max(np.abs(a / b - 1))))
check("K2 rebuilt LAW_RTA tables at delta = 0 (full, tr_moster_W30, tr_behroozi_W30) = CFG503's committed tables for the f30 groups (1e-9 rel)",
      k2 < 1e-9, f"max rel {k2:.1e}")


# ------------------------------------------------------------------ components: stacked E and own per SHMR for (construction, footing, mask)
EC30 = {c: env_cfg(c, "f30", MEAS["f30"], MEAS["f30"], "meas") for c in CONS}


def own_mix(c, foot, model, fO, tabname=None, s=None):
    """per-group own vectors with the stripping mix fO; LAW_RTA from a rebuilt table (A; B additive) if tabname is given."""
    if tabname is None or tabname == "d0":
        return own_rec(c, "f30", foot, model, s, "W30", fO[s])
    fo = fo_of(fO[s])
    full, tr = own_from_tab(tabname, foot)[s]
    vA = (1 - fo) * full + fo * tr
    if c == "A":
        return vA
    full0, tr0 = own_from_tab("d0", foot)[s]
    return own_rec("B", "f30", foot, model, s, "W30", fO[s]) + (vA - ((1 - fo) * full0 + fo * tr0))


def census_own(c, foot, s, fO):
    fo = fo_of(fO[s])
    full, tr = edge_tabs(c, foot, "census", None, s, "W30")
    v = (1 - fo) * full + fo * tr
    return np.where(np.isfinite(v), v, 0.0)


def comps(c, foot, mask, model="LAW_RTA", fE=None, fO=None, tab=None, Eover=None, mixtab=None):
    """returns dict s -> (E_stack, own_stack).  mixtab = (tabname, lens-mask) : lenses in the mask use the rebuilt table (IMF2)."""
    fE = MEAS["f30"] if fE is None else fE; fO = MEAS["f30"] if fO is None else fO
    out = {}
    for s in SHMRS:
        Eg = evec(GP, c, s, "W30", fE[s], f"cfg531|{id(fE)}|W30") if Eover is None else Eover[s]
        if model == "CENSUS":
            og = census_own(c, foot, s, fO)
        else:
            og = own_mix(c, foot, model, fO, tab, s)
        if mixtab is None:
            out[s] = (gstack(Eg, mask), gstack(og, mask))
        else:
            o2 = own_mix(c, foot, model, fO, mixtab[0], s)
            m1, m0 = mask & mixtab[1], mask & ~mixtab[1]
            num = np.zeros(15); den = np.zeros(15)
            for k in range(15):
                w1 = np.bincount(gi[m1], weights=WW[m1, k], minlength=NGRP); w0 = np.bincount(gi[m0], weights=WW[m0, k], minlength=NGRP)
                num[k] = w1 @ o2[:, k] + w0 @ og[:, k]; den[k] = w1.sum() + w0.sum()
            out[s] = (gstack(Eg, mask), num / den)
    return out


def fit_eps(d, Cv, cp, idx):
    """GLS amplitude of the own profile in the bins idx; CFG529's covariance C/hart(n) + delta delta^T (SHMR)."""
    idx = np.asarray(idx)
    Em, om = cp["moster"]; Eb, ob = cp["behroozi"]
    mM = Em + om; dl = (Eb + ob) - mM
    Ct = Cv[np.ix_(idx, idx)] / hart(len(idx)) + np.outer(dl[idx], dl[idx])
    W = np.linalg.inv(Ct)
    r = d[idx] - mM[idx]; o = om[idx]
    F = float(o @ W @ o)
    eps = float(o @ W @ r) / F
    chi0 = float(r @ W @ r); chi1 = float((r - eps * o) @ W @ (r - eps * o))
    return dict(eps=eps, sig=F ** -0.5, Z=eps * F ** 0.5, chi2_eps0=chi0, p_eps0=float(stats.chi2.sf(chi0, len(idx))), chi2_fit=chi1,
                p_fit=float(stats.chi2.sf(chi1, len(idx) - 1)), n=len(idx), wvec=(W @ o / F).tolist())


def all_bands(d, Cv, cp):
    out = {b: fit_eps(d, Cv, cp, ix) for b, ix in BANDS.items()}
    out["per_bin"] = {int(k): {kk: v for kk, v in fit_eps(d, Cv, cp, [k]).items() if kk in ("eps", "sig")} for k in range(6, 15)}
    return out


def fmt(fb):
    return " | ".join(f"{b} {fb[b]['eps']:+.3f}+-{fb[b]['sig']:.3f} (Z {fb[b]['Z']:+.1f})" for b in ("K-in", "K-mid", "K-out", "K9"))


d30, C30, L30 = esd_loo(F30)
assert np.allclose(d30, NS["d30"], rtol=1e-12, atol=0)

# ------------------------------------------------------------------ K1: reproduce CFG529 (LAW_RTA, LCDM chi2 and inner-9 chi2)
k1 = 0.0
for c in CONS:
    for foot in FOOTS:
        for m in ("LAW_RTA", "LCDM"):
            a = model_score(EC30[c], m, foot); b = J529["rescore_f30"][c][foot]["rows"][m]
            k1 = max(k1, abs(a["chi2"] - b["chi2"]), abs(a["chi2_inner9"] - b["chi2_inner9"]))
check("K1 CFG529 machinery reproduces its committed f30 LAW_RTA / LCDM chi2 and inner-9 chi2 (A, B, both footings) within 0.01", k1 <= 0.01,
      f"max |d| {k1:.2e}")
# K2b: own_mix from the d0 table path equals own_rec (construction A) and the additive B path is an identity at d0
k2b = 0.0
for c in CONS:
    for foot in FOOTS:
        for s in SHMRS:
            fo = fo_of(MEAS["f30"][s]); full, tr = own_from_tab("d0", foot)[s]
            vA = (1 - fo) * full + fo * tr
            k2b = max(k2b, float(np.max(np.abs(vA[GSEL] - own_rec("A", "f30", foot, "LAW_RTA", s, "W30", MEAS["f30"][s])[GSEL]))))
check("K2b own mixing from the rebuilt tables equals CFG529's own_rec (construction A, f30 groups)", k2b < 1e-9, f"max abs {k2b:.1e}")

# geometry: radii per band
RB = np.sqrt(C.G_MPC * MGL[:, None] / GC_[None, :]) * 1e3                       # kpc, per lens per bin
GEO = {}
for b, ix in BANDS.items():
    w = WW[F30][:, ix].ravel(); R = RB[F30][:, ix].ravel(); o = np.argsort(R); cw = np.cumsum(w[o]) / w.sum()
    lm = np.repeat(LMSL[F30], len(ix)) if False else np.tile(LMSL[F30][:, None], (1, len(ix))).ravel()
    GEO[b] = dict(R_mean_kpc=float((w * R).sum() / w.sum()), R16_kpc=float(R[o][np.searchsorted(cw, 0.16)]), R84_kpc=float(R[o][np.searchsorted(cw, 0.84)]),
                  R_min_kpc=float(R.min()), R_max_kpc=float(R.max()),
                  r_over_rM={f: [float(np.sqrt(A0F[f] / GE[max(ix) + 1])), float(np.sqrt(A0F[f] / GE[min(ix)]))] for f in FOOTS},
                  logMs_wmean=float((w * lm).sum() / w.sum()))
RES["geometry"] = GEO
RES["f30_logMs_percentiles"] = {p: float(np.percentile(LMSL[F30], p)) for p in (5, 16, 50, 84, 95, 99)}
P("\n== band geometry (f30, stack weights) ==")
for b, g in GEO.items():
    P(f"  {b:5s}: R mean {g['R_mean_kpc']:.0f} kpc (16-84% {g['R16_kpc']:.0f}-{g['R84_kpc']:.0f}); r/r_M can {g['r_over_rM']['canonical'][0]:.2f}-"
      f"{g['r_over_rM']['canonical'][1]:.2f}, alt {g['r_over_rM']['alt'][0]:.2f}-{g['r_over_rM']['alt'][1]:.2f}; weighted log M* {g['logMs_wmean']:.2f}")
P(f"  f30 log M* percentiles 5/50/95/99: {RES['f30_logMs_percentiles'][5]:.2f} / {RES['f30_logMs_percentiles'][50]:.2f} / "
  f"{RES['f30_logMs_percentiles'][95]:.2f} / {RES['f30_logMs_percentiles'][99]:.2f}")

EARLY = TYP == 1
if not MUTATE:
    # ------------------------------------------------------------------ base
    P("\n== BASE: eps = Delta M/M_pred per band, validated f30 environment (GLS; SHMR delta in the covariance) ==")
    BASE = {}
    for c in CONS:
        for foot in FOOTS:
            for m in ("LAW_RTA", "CENSUS"):
                fb = all_bands(d30, C30, comps(c, foot, F30, m))
                BASE[f"{c}|{foot}|{m}"] = fb
                P(f"  [{c} {foot:9s} {m:7s}] {fmt(fb)}; K9 chi2(eps=0) {fb['K9']['chi2_eps0']:.2f} (p {fb['K9']['p_eps0']:.1e}), "
                  f"after eps {fb['K9']['chi2_fit']:.2f} (p {fb['K9']['p_fit']:.2f})")
            P(f"      per bin (LAW_RTA): " + " ".join(f"{k}:{v['eps']:+.2f}+-{v['sig']:.2f}" for k, v in BASE[f'{c}|{foot}|LAW_RTA']['per_bin'].items()))
    RES["base"] = BASE
    KS = {foot: all(BASE[f"{c}|{foot}|LAW_RTA"]["K9"]["Z"] >= 3 for c in CONS) for foot in FOOTS}
    RG = {foot: all(BASE[f"{c}|{foot}|LAW_RTA"]["K-in"]["Z"] >= 2 for c in CONS) for foot in FOOTS}
    P(f"  KS (K9 eps >= 3 sigma, both constructions): {KS};  RG (K-in eps >= 2 sigma): {RG}")
    RES["KS"], RES["RG"] = KS, RG

    # ------------------------------------------------------------------ mass tertiles
    P("\n== mass dependence: f30 log M* tertiles (by lens count), LAW_RTA ==")
    q = np.percentile(LMSL[F30], [100 / 3, 200 / 3])
    TER = {}
    for t, (lo, hi) in enumerate([(-np.inf, q[0]), (q[0], q[1]), (q[1], np.inf)]):
        mk = F30 & (LMSL > lo) & (LMSL <= hi)
        dt, Ct, _ = esd_loo(mk)
        for c in CONS:
            for foot in FOOTS:
                fb = all_bands(dt, Ct, comps(c, foot, mk))
                TER[f"T{t + 1}|{c}|{foot}"] = dict(logMs_median=float(np.median(LMSL[mk])), n=int(mk.sum()), bands={b: fb[b] for b in BANDS})
                P(f"  T{t + 1} (median log M* {np.median(LMSL[mk]):.2f}, n {mk.sum()}) [{c} {foot:9s}] {fmt(fb)}")
    RES["tertiles"] = TER

    # ------------------------------------------------------------------ (a) stellar mass / IMF
    P("\n== (a) stellar-mass scale / IMF (environment fixed = CFG529 validated; B additive) ==")
    A_ = {}
    for name in ["d0"] + [f"d{x:.2f}" for x in DELTAS] + ["IMF", "IMF2_early_only", "d0.15_envshift", "d0.20_envshift"]:
        for c in CONS:
            for foot in FOOTS:
                if name == "IMF2_early_only":
                    cp = comps(c, foot, F30, mixtab=("IMF", EARLY))
                elif name.endswith("_envshift"):
                    dl = float(name[1:5])
                    GPs = NS["GSet"]("Pshift", gi, GM, GZ, GS + dl, WW)
                    Eo = {s: np.array([LL.finish(lambda R, e=e_: np.interp(np.log(R), LRG, e), GM[g])
                                       for g, e_ in enumerate(GPs.interp(NS["Egrid"](c, s, "W30", MEAS["f30"][s])))]) for s in SHMRS}
                    cp = comps(c, foot, F30, tab=name, Eover=Eo)
                else:
                    cp = comps(c, foot, F30, tab=name)
                fb = all_bands(d30, C30, cp)
                A_[f"{name}|{c}|{foot}"] = {b: fb[b] for b in BANDS}
                P(f"  {name:16s} [{c} {foot:9s}] {fmt(fb)}; K9 law chi2 {fb['K9']['chi2_eps0']:.2f} (p {fb['K9']['p_eps0']:.1e})")
    RES["a"] = A_
    # delta_close and the frozen rule
    grid = [0.0] + list(DELTAS)
    DCL, EXPA = {}, {}
    for foot in FOOTS:
        for c in CONS:
            e = [A_[f"{'d0' if x == 0 else f'd{x:.2f}'}|{c}|{foot}"]["K9"]["eps"] for x in grid]
            dc = None
            for i in range(len(grid) - 1):
                if e[i] > 0 >= e[i + 1]:
                    dc = grid[i] + (grid[i + 1] - grid[i]) * e[i] / (e[i] - e[i + 1]); break
            DCL[f"{c}|{foot}"] = dc
            e2 = [A_[f"{'d0' if x == 0 else f'd{x:.2f}'}|{c}|{foot}"]["K-in"]["eps"] for x in grid]
            dc2 = None
            for i in range(len(grid) - 1):
                if e2[i] > 0 >= e2[i + 1]:
                    dc2 = grid[i] + (grid[i + 1] - grid[i]) * e2[i] / (e2[i] - e2[i + 1]); break
            DCL[f"{c}|{foot}|K-in"] = dc2
        ok = {}
        for name in ("d0.05", "d0.10", "d0.15", "IMF", "IMF2_early_only"):
            ok[name] = all(abs(A_[f"{name}|{c}|{foot}"]["K9"]["Z"]) < 2 and A_[f"{name}|{c}|{foot}"]["K9"]["p_eps0"] > 0.01 for c in CONS)
        EXPA[foot] = dict(by_shift=ok, explained=any(ok.values()))
        P(f"  [{foot}] delta_close (K9) A {DCL[f'A|{foot}']}, B {DCL[f'B|{foot}']}; (K-in) A {DCL[f'A|{foot}|K-in']}, B {DCL[f'B|{foot}|K-in']}; "
          f"allowed shifts that close (both constructions): {[k for k, v in ok.items() if v] or 'none'} -> EXPLAINED BY (a): {EXPA[foot]['explained']}")
    RES["a_delta_close"] = DCL; RES["a_verdict"] = EXPA

    # ------------------------------------------------------------------ (b) stripping
    P("\n== (b) stripping / satellite term ==")
    ZERO = {s: np.zeros_like(MEAS["f30"][s]) for s in SHMRS}
    HALF = {s: 0.5 * MEAS["f30"][s] for s in SHMRS}
    ET2 = np.load(os.path.join(NS["EXT"], "cfg502_work", "cfg502_env_table.npz"))
    assert np.array_equal(ET2["LMS"], LMS) and np.array_equal(ET2["ZG"], ZG) and np.array_equal(ET2["RG"], NS["RG"])
    E502g = GP.interp(ET2["E_W30"])
    E502 = np.array([LL.finish(lambda R, e=e_: np.interp(np.log(R), LRG, e), GM[g]) for g, e_ in enumerate(E502g)])
    Bv = {}
    for nm, kw in (("S-off", dict(fO=ZERO)), ("S-half", dict(fO=HALF)), ("zero-leakage (E and own f=0; reported)", dict(fE=ZERO, fO=ZERO)),
                   ("S-502", dict(fO=ZERO, Eover={s: E502 for s in SHMRS}))):
        for c in CONS:
            if nm == "S-502" and c == "B":
                continue
            for foot in FOOTS:
                fb = all_bands(d30, C30, comps(c, foot, F30, **kw))
                lc = comps(c, foot, F30, model="LCDM", **kw)
                mm = lc["moster"][0] + lc["moster"][1]; dd = (lc["behroozi"][0] + lc["behroozi"][1]) - mm
                chiL = NS["chi2c"](d30, C30, hart(15), mm, dd)
                Bv[f"{nm}|{c}|{foot}"] = dict(bands={b: fb[b] for b in BANDS}, LCDM_chi2=chiL, LCDM_p=float(stats.chi2.sf(chiL, 15)))
                P(f"  {nm:40s} [{c} {foot:9s}] {fmt(fb)}; LCDM f30 chi2 {chiL:.2f} (p {stats.chi2.sf(chiL, 15):.3f})")
    DEPB = {foot: any(all(abs(Bv[f"{nm}|{c}|{foot}"]["bands"]["K9"]["Z"]) < 2 for c in (CONS if nm != "S-502" else ("A",))) for nm in ("S-off", "S-502"))
            for foot in FOOTS}
    P(f"  DEPENDS ON (b): {DEPB}")
    RES["b"] = Bv; RES["b_depends"] = DEPB

    # ------------------------------------------------------------------ (c) early vs late
    P("\n== (c) early (typ 1) vs late (typ 0), f30 ==")
    Cc = {}
    for cls, mk in (("early", F30 & EARLY), ("late", F30 & ~EARLY)):
        dcl, Ccl, Lcl = esd_loo(mk)
        for c in CONS:
            for foot in FOOTS:
                cp = comps(c, foot, mk)
                fb = all_bands(dcl, Ccl, cp)
                mM = cp["moster"][0] + cp["moster"][1]
                loo_eps = {b: (Lcl[:, ix] - mM[ix][None, :]) @ np.array(fb[b]["wvec"]) - 0.0 for b, ix in BANDS.items()}
                # wvec applies to r = d - mM:  eps_loo = wvec . (d_loo - mM)
                Cc[f"{cls}|{c}|{foot}"] = dict(n=int(mk.sum()), logMs_median=float(np.median(LMSL[mk])), bands={b: fb[b] for b in BANDS},
                                              loo={b: v.tolist() for b, v in loo_eps.items()})
                P(f"  {cls:5s} (n {mk.sum()}, median log M* {np.median(LMSL[mk]):.2f}) [{c} {foot:9s}] {fmt(fb)}")
    CAR, DIFF = {}, {}
    for foot in FOOTS:
        for c in CONS:
            for b in BANDS:
                e, l_ = Cc[f"early|{c}|{foot}"], Cc[f"late|{c}|{foot}"]
                dv = np.array(e["loo"][b]) - np.array(l_["loo"][b])
                vj = (NPATCH - 1) / NPATCH * np.sum((dv - dv.mean()) ** 2)
                vq = e["bands"][b]["sig"] ** 2 + l_["bands"][b]["sig"] ** 2
                den = math.sqrt(max(vj, vq))
                DIFF[f"{c}|{foot}|{b}"] = dict(diff=e["bands"][b]["eps"] - l_["bands"][b]["eps"], sig_jk=math.sqrt(vj), sig_quad=math.sqrt(vq),
                                              Z=(e["bands"][b]["eps"] - l_["bands"][b]["eps"]) / den)
        ze = [Cc[f"early|{c}|{foot}"]["bands"]["K9"]["Z"] for c in CONS]; zl = [Cc[f"late|{c}|{foot}"]["bands"]["K9"]["Z"] for c in CONS]
        if all(z >= 3 for z in ze) and all(abs(z) < 2 for z in zl):
            CAR[foot] = "CARRIED BY EARLY TYPES"
        elif all(z >= 3 for z in zl) and all(abs(z) < 2 for z in ze):
            CAR[foot] = "CARRIED BY LATE TYPES"
        elif all(z >= 2 for z in ze) and all(z >= 2 for z in zl):
            CAR[foot] = "BOTH"
        else:
            CAR[foot] = "MIXED/UNRESOLVED"
        P(f"  [{foot}] K9 Z early {['%+.1f' % z for z in ze]}, late {['%+.1f' % z for z in zl]} -> {CAR[foot]}; early-late diff K9: "
          + "; ".join(f"{c} {DIFF[f'{c}|{foot}|K9']['diff']:+.3f} (Z {DIFF[f'{c}|{foot}|K9']['Z']:+.1f})" for c in CONS)
          + "; K-in: " + "; ".join(f"{c} {DIFF[f'{c}|{foot}|K-in']['diff']:+.3f} (Z {DIFF[f'{c}|{foot}|K-in']['Z']:+.1f})" for c in CONS))
    for k in Cc:
        Cc[k].pop("loo")
    RES["c"] = Cc; RES["c_diff"] = DIFF; RES["c_reading"] = CAR

    # ------------------------------------------------------------------ (d) kernel
    P("\n== (d) kernel (report only; a0 rescaled by CFG468's SPARC fit; B additive) ==")
    Dk = {}
    for k in ("simple", "standard"):
        for t in ("T-free", "T-fix"):
            for c in CONS:
                for foot in FOOTS:
                    fb = all_bands(d30, C30, comps(c, foot, F30, tab=f"kern_{k}_{t}"))
                    Dk[f"{k}|{t}|{c}|{foot}"] = {b: fb[b] for b in BANDS}
                    P(f"  nu_{k:8s} {t:6s} (a0 x {a0r[k][t]:.4f}) [{c} {foot:9s}] {fmt(fb)}")
    RES["d"] = Dk
    RES["d_sparc_CFG468"] = {k: dict(dchi2_free=J468["sparc"]["kernels"][f"nu_{k}"]["T-free"]["dchi2"],
                                     dchi2_fix=J468["sparc"]["kernels"][f"nu_{k}"]["T-fix"]["dchi2"],
                                     sparc_pass=J468["sparc"]["kernels"][f"nu_{k}"]["pass"]) for k in ("simple", "standard")}
    P(f"  CFG468 SPARC: {RES['d_sparc_CFG468']}")

    # ------------------------------------------------------------------ mechanism check M-b (extended baryons, sign) on K-in
    P("\n== mechanism M-b: Hernquist baryons (a = 3 kpc, sign check) instead of the point mass, construction A, K-in ==")
    MB = {}
    for foot in FOOTS:
        i = FOOTS.index(foot); a0 = A0F[foot]
        tabH = np.zeros((len(GSEL), 3, 15))
        for n_, g in enumerate(GSEL):
            Mg, zl = float(GM[g]), float(GZ[g])
            rta = C.r_ta_law(Mg, a0, zl); r = np.geomspace(1e-4, rta, 1500); ah = 3e-3
            Mb = Mg * r ** 2 / (r + ah) ** 2
            Mtot = Mb * C.nu_mono(C.G_MPC * Mb / r ** 2 / a0)
            fullH = C._finish(lambda R: C.dsigma(R, r, Mtot), Mg)
            tabH[n_, 0] = fullH
            for j, s in enumerate(SHMRS):
                w = rt_weights(f"{s}_W30", float(GS[g]), zl)
                tabH[n_, 1 + j] = C._finish(lambda R: C.dsigma(R, r, truncate(r, Mtot, w)), Mg)
        TAB_H = TAB.copy(); TAB_H["hern"] = TAB["d0"].copy(); TAB_H["hern"][:, i] = tabH
        TAB.update({"hern_" + foot: TAB_H["hern"]})
        fb = all_bands(d30, C30, comps("A", foot, F30, tab="hern_" + foot))
        b0 = RES["base"][f"A|{foot}|LAW_RTA"]
        MB[foot] = {b: dict(eps=fb[b]["eps"], d_eps_vs_point=fb[b]["eps"] - b0[b]["eps"]) for b in BANDS}
        P(f"  [{foot}] eps with extended baryons: " + "; ".join(f"{b} {fb[b]['eps']:+.3f} (vs point {fb[b]['eps'] - b0[b]['eps']:+.4f})" for b in BANDS))
    RES["mech_Mb"] = MB

else:
    P("\n== MUTATE ==")
    # MU1 uniform injection
    mu1 = 0.0
    for c in CONS:
        for foot in FOOTS:
            cp = comps(c, foot, F30)
            dm = cp["moster"][0] + 1.4 * cp["moster"][1]
            fb = all_bands(dm, C30, cp)
            mu1 = max(mu1, max(abs(fb[b]["eps"] - 0.4) for b in BANDS))
    check("MU1 mock d = E + 1.4 own: eps = 0.400 in every band (A, B, both footings) to 1e-6", mu1 < 1e-6, f"max |eps - 0.4| {mu1:.1e}")
    # MU4 null mock
    ks0 = {}
    for foot in FOOTS:
        zz = []
        for c in CONS:
            cp = comps(c, foot, F30); dm = cp["moster"][0] + cp["moster"][1]
            zz.append(all_bands(dm, C30, cp)["K9"]["Z"])
        ks0[foot] = all(z >= 3 for z in zz)
    check("MU4 null mock (d = model): KS reads false on both footings", not any(ks0.values()), f"KS {ks0}")
    # MU2 isothermal injection: Delta M(<r) = 0.3 M_gal (r / 50 kpc), r <= r_ta,law
    mu2 = {}
    okall = True
    for foot in FOOTS:
        a0 = A0F[foot]; i = FOOTS.index(foot)
        Xg = np.zeros((NGRP, 15)); TRg = np.zeros((NGRP, 15))
        for g in GSEL:
            Mg, zl = float(GM[g]), float(GZ[g])
            rta = C.r_ta_law(Mg, a0, zl); r = np.geomspace(1e-4, rta, 1500)
            dM = 0.3 * Mg * r / 0.05
            Xg[g] = C._finish(lambda R: C.dsigma(R, r, dM), Mg)
            Rn = np.sqrt(C.G_MPC * Mg / C.GN); Wn = C.WN
            Ml = Mg * C.nu_mono(C.G_MPC * Mg / Rn ** 2 / a0)
            ratio = np.where(Rn <= rta, 0.3 * Mg * (Rn / 0.05) / Ml, 0.0)
            TRg[g] = (Wn * ratio).sum(1) / Wn.sum(1)
        X = gstack(Xg, F30); TR = gstack(TRg, F30)
        wb = WW[F30].sum(0)
        for c in CONS:
            cp = comps(c, foot, F30)
            dm = cp["moster"][0] + cp["moster"][1] + X
            fb = all_bands(dm, C30, cp)
            for b, ix in BANDS.items():
                true = float((TR[ix] * wb[ix]).sum() / wb[ix].sum())                    # stack-weighted (frozen definition)
                ok = abs(fb[b]["eps"] - true) <= 0.25 * true + 0.02
                mu2[f"{c}|{foot}|{b}"] = dict(recovered=fb[b]["eps"], true=true, ok=bool(ok))
                if b != "K-out":
                    okall &= ok
                P(f"  MU2 [{c} {foot:9s}] {b:5s}: recovered {fb[b]['eps']:+.3f}, true {true:+.3f} {'ok' if ok else 'MISS'}{' (reported)' if b == 'K-out' else ''}")
    check("MU2 isothermal injection recovered within 0.25 true + 0.02 in K-in, K-mid, K9 (A, B, both footings)", okall,
          "; ".join(f"{k} {v['recovered']:+.3f}/{v['true']:+.3f}" for k, v in mu2.items() if k.endswith("K9")))
    RES["MU2"] = mu2
    # MU3 type shuffle within groups
    rng = np.random.default_rng(531)
    typ_s = TYP.copy()
    idx30 = np.nonzero(F30)[0]
    for g in np.unique(gi[idx30]):
        m = idx30[gi[idx30] == g]
        typ_s[m] = rng.permutation(TYP[m])
    ES = typ_s == 1
    mu3 = {}
    okk = True
    for c in CONS:
        for foot in FOOTS:
            r_ = {}
            for cls, mk in (("early", F30 & ES), ("late", F30 & ~ES)):
                dcl, Ccl, Lcl = esd_loo(mk); cp = comps(c, foot, mk); fb = fit_eps(dcl, Ccl, cp, BANDS["K9"])
                mM = cp["moster"][0] + cp["moster"][1]
                r_[cls] = (fb, (Lcl[:, BANDS["K9"]] - mM[BANDS["K9"]][None, :]) @ np.array(fb["wvec"]))
            dv = r_["early"][1] - r_["late"][1]
            vj = (NPATCH - 1) / NPATCH * np.sum((dv - dv.mean()) ** 2); vq = r_["early"][0]["sig"] ** 2 + r_["late"][0]["sig"] ** 2
            Z = (r_["early"][0]["eps"] - r_["late"][0]["eps"]) / math.sqrt(max(vj, vq))
            mu3[f"{c}|{foot}"] = Z; okk &= abs(Z) < 2.5
            P(f"  MU3 [{c} {foot:9s}] shuffled 'early' K9 eps {r_['early'][0]['eps']:+.3f}+-{r_['early'][0]['sig']:.3f}, shuffled 'late' "
              f"{r_['late'][0]['eps']:+.3f}+-{r_['late'][0]['sig']:.3f}, diff Z {Z:+.2f}  (diagnostic print added 2026-10-09 after the first MUTATE run)")
            RES.setdefault("MU3_eps", {})[f"{c}|{foot}"] = dict(early=r_["early"][0]["eps"], late=r_["late"][0]["eps"])
    check("MU3 type labels shuffled within (M_gal, z) groups: early-late K9 difference |Z| < 2.5 (A, B, both footings)", okk,
          "; ".join(f"{k} {v:+.2f}" for k, v in mu3.items()))
    RES["MU3"] = mu3

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg531_kids_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg531_kids{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
