#!/usr/bin/env python3
"""CFG504 own-profile tables with the calibrated transition window (FROZEN_CRITERIA.md section 5; criteria commit 333a5fce4).
Model code copied from CFG503's cfg503_own.py (CFG487 kids_vec, CFG495 lens_model; imported libraries read-only), plus:
  - every model's distributed enclosed mass is CONTINUED beyond the record's r_ta truncation by the record's own formula to
    r_ext = max(8 x_t, 6) r_ta,LCDM (and >= 6 x the record boundary); model-intrinsic boundaries (5.85 r_M edge; law to 0.5 r_ta,law;
    V1's own turnaround latch) are kept (nothing beyond them);
  - window: M_w(r) = M(r0) f_t(r0) + Int f_t dM, f_t = [1 + (r / (x_t r_ta))^4]^-2 with r_ta = the lens's LCDM-equivalent r_ta (SHMR);
  - leaked satellites: CFG503's stripping M_d(min(r, r_t)) on the continued profile, then the same window.
Variants (per group): sharp = the record's arrays (CFG503, exactly); prim / lo / hi / ext windows; 'own' = framework own profiles windowed
in units of their own r_ta,law with the primary x_t (reported variant e).
Output: ../../../_external_data/cfg504_work/cfg504_own_tables.npz ; cfg504_own.out
Run: nice -n 15 python3 cfg504_own.py   (4 worker processes, 1 thread each)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import math, json, time
import numpy as np
from multiprocessing import Pool
from scipy.interpolate import RegularGridInterpolator
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(LANES, "CFG487_settled_fraction_switch"))
sys.path.insert(0, os.path.join(LANES, "CFG100_kids_mass_rederivation"))
sys.path.insert(0, os.path.join(LANES, "CFG495_drawdown_shell"))
import cfg487_lib as LB                                                      # noqa: E402  (read-only)
import cfg100_lib as C                                                       # noqa: E402  (read-only)
import cfg495_lenslib as LL                                                  # noqa: E402  (read-only)
import cfg504_envlib as EL                                                   # noqa: E402

WORK2 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg502_work"))
WORK3 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg503_work"))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg504_work"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
FOOTS = ("canonical", "alt")
SHMRS = ("moster", "behroozi")
LOG = []
T0 = time.time()
CAL = json.load(open(os.path.join(HERE, "cfg504_calib_results.json")))["primary"]
XTP, XSIG = CAL["x_t"], CAL["sigma_tot"]
TR0, TR1 = CAL["trend_intercept_at_13p8"], CAL["trend_slope_per_dex"]
WINS = ("prim", "lo", "hi", "ext")
NEXT = 700


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def groups(z, Mgal, logMs):
    lmg = np.log10(Mgal)
    key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(z / 0.03).astype(np.int64)
    _, gi, cnt = np.unique(key, return_inverse=True, return_counts=True)
    gi = gi.ravel()
    return gi, 10 ** (np.bincount(gi, weights=lmg) / cnt), np.bincount(gi, weights=z) / cnt, np.bincount(gi, weights=logMs) / cnt, cnt


ET = np.load(os.path.join(WORK3, "cfg503_env_table.npz"))
LMS, ZG, RTC = ET["LMS"], ET["ZG"], ET["RTC"]
RTI = {f"{s}_{k}": RegularGridInterpolator((LMS, ZG), ET[f"{s}_{k}_RTW"], bounds_error=False, fill_value=None)
       for s in SHMRS for k in ("W10", "W30", "ALL")}


def rt_weights(tag, lms, z):
    w = RTI[tag]([[min(max(lms, LMS[0]), LMS[-1]), min(max(z, ZG[0]), ZG[-1])]])[0]
    w = np.maximum(w, 0.0)
    return w / w.sum()


def truncate(r, Md, w):
    """sum_j w_j Md(min(r, r_t,j)) + w_unstripped Md(r)   (CFG503's, copied)."""
    out = w[-1] * Md
    nz = np.nonzero(w[:-1] > 0)[0]
    if len(nz):
        rt = RTC[nz]
        out = out + (w[nz, None] * np.interp(np.minimum(r[None, :], rt[:, None]), r, Md)).sum(0)
    return out


def ft(x, xt):
    return (1.0 + (x / xt) ** 4) ** -2.0


def window(r, M, rw, xt):
    """M_w(r) = M(r0) f(r0) + cumulative Int f dM, f = f_t(r / rw)."""
    rm = np.sqrt(r[1:] * r[:-1])
    f0 = ft(r[0] / rw, xt)
    return np.concatenate([[M[0] * f0], M[0] * f0 + np.cumsum(ft(rm / rw, xt) * np.diff(M))])


def xt_of(win, lMta_h):
    return {"prim": XTP, "lo": max(XTP - XSIG, 0.1), "hi": XTP + XSIG}.get(win) if win != "ext" else float(np.clip(TR0 + TR1 * (lMta_h - 13.8), 0.1, 3.0))


SC = LB.ShellClock(Om=C.OM)
RHO_M0_MPC = C.OM * C.RHOC0


def m_profile(rho_ratio, a_obs):
    return SC.m_of_rho(rho_ratio, a_obs, conservative=False)[0]


def kids_Md_ext(Mg, zl, a0, rout, rext, mfun=None, intrinsic=False):
    """CFG487 kids_vec's distributed mass on its record grid geomspace(1e-4, rout, 1500), continued to rext by the same formula
    (intrinsic=True: model-intrinsic edge, nothing beyond rout).  Returns (r_record, Md_record, r_ext, Md_ext)."""
    r0 = np.geomspace(1e-4, rout, 1500)
    r = np.concatenate([r0, np.geomspace(rout, max(rext, 1.01 * rout), NEXT)[1:]])
    Md = Mg * (C.nu_mono(C.G_MPC * Mg / r ** 2 / a0) - 1.0)
    if intrinsic:
        Md[1500:] = Md[1499]
    if mfun is not None:
        mm = mfun(r)
        dM = np.diff(np.concatenate([[0.0], Md]))
        mmid = np.concatenate([[mm[0]], 0.5 * (mm[1:] + mm[:-1])])
        Md = np.cumsum(mmid * dM)
    Md0 = Md[:1500].copy()
    return r0, Md0, r, Md


def lens_model_ext(Mg, z, lMs, foot, rext_fac, nr=2500, dlogM=0.0):
    """cfg495_lenslib.lens_model (copied) on its record grid, plus the same formulas continued beyond r_ta to rext_fac x r_ta."""
    a0 = LL.A0[foot]
    M200 = 10 ** (LL.inv_moster(lMs, z) + dlogM)
    Menc, rho, c, r200 = LL.nfw(M200, z)
    rho_ta = LL.OM * LL.RHOC0 * (1 + z) ** 3 * LL.dta(z)
    rta = math.exp(brentq(lambda lr: math.log(float(Menc(math.exp(lr)))) - math.log(4 * math.pi / 3 * math.exp(3 * lr) * rho_ta),
                          math.log(r200 * 0.5), math.log(r200 * 50)))
    Mta = float(Menc(rta))
    fret = min(Mg / (LL.FB * Mta), 1.0)
    rM = math.sqrt(LL.G_MPC * Mg / a0)
    redge = min(rM / math.log(1 + fret * LL.FB / (1 - LL.FB)), rta)
    r = np.geomspace(1e-4, rta, nr)
    Mph = Mg * (LL.nu_mono(LL.G_MPC * Mg / r ** 2 / a0) - 1.0)
    rho_ph = np.gradient(Mph, r) / (4 * math.pi * r ** 2)
    rho_c = (1 - LL.FB) * rho(r)
    Mc = (1 - LL.FB) * Menc(r)
    dV = np.diff(r) * 4 * math.pi * (0.5 * (r[1:] + r[:-1])) ** 2

    def cum(dens):
        mid = 0.5 * (dens[1:] + dens[:-1])
        return np.concatenate([[0.0], np.cumsum(mid * dV)])
    inside = r <= redge
    exc = np.where(inside, np.maximum(rho_ph - rho_c, 0.0), 0.0)
    Mexc = cum(exc)
    Me = float(Mexc[-1])
    Mc_ta = float(Mc[-1])
    q = Me / Mc_ta
    rec = dict(M_lcdm=(1 - LL.FB * fret) * Menc(r), M_nodd=LL.FB * (1 - fret) * Menc(r) + Mc + Mexc, D_prop=-q * Mc)
    re_ = np.concatenate([r, np.geomspace(rta, rext_fac * rta, NEXT)[1:]])
    Me_ = Menc(re_); Mc_ = (1 - LL.FB) * Me_
    Mexc_ = np.concatenate([Mexc, np.full(NEXT - 1, Me)])
    ext = dict(M_lcdm=(1 - LL.FB * fret) * Me_, M_nodd=LL.FB * (1 - fret) * Me_ + Mc_ + Mexc_, D_prop=-q * Mc_)
    return r, rec, re_, ext, rta


def kids_fin(Mg, r, Md):
    return C._finish(lambda R: C.dsigma(R, r, Md) + Mg / (math.pi * R ** 2), Mg)


def ll_fin(Mg, r, M):
    return LL.finish(lambda R: LL.dsigma(R, r, M) + Mg / (math.pi * R ** 2), Mg)


def ll_fin_nopm(Mg, r, M):
    return LL.finish(lambda R: LL.dsigma(R, r, M), Mg)


def lMta_h(rta, z):
    return math.log10(4 * math.pi / 3 * rta ** 3 * EL.rho_m(z) * EL.LL.dta(z) * EL.H)


def work_P(args):
    """stack-P group: every model, both footings, both SHMR; variants sharp / windows; full + tr W10 / W30."""
    Mg, zl, lms = args
    out = {}
    W = {f"{s}_{k}": rt_weights(f"{s}_{k}", lms, zl) for s in SHMRS for k in ("W10", "W30")}
    RTL = {s: EL.r_ta_lcdm(lms, zl, s)[0] for s in SHMRS}
    XTW = {s: {w: xt_of(w, lMta_h(RTL[s], zl)) for w in WINS} for s in SHMRS}
    for foot in FOOTS:
        a0 = C.A0[foot]; ao = 1.0 / (1.0 + zl)
        rta = C.r_ta_law(Mg, a0, zl)
        re1 = float(LB.r_edge(Mg, C.G_MPC, a0))
        rho1 = lambda r: Mg * C.nu_mono(C.G_MPC * Mg / r ** 2 / a0) / (4 * math.pi / 3 * r ** 3) / RHO_M0_MPC
        rext = max(max(8 * XTW[s][w] * RTL[s] for s in SHMRS for w in WINS), 6 * rta)
        law = {"LAW_RTA": kids_Md_ext(Mg, zl, a0, rta, rext), "LAW_X05": kids_Md_ext(Mg, zl, a0, 0.5 * rta, rext, intrinsic=True),
               "EDGE": kids_Md_ext(Mg, zl, a0, re1, max(rext, 6 * re1), intrinsic=True),
               "V1": kids_Md_ext(Mg, zl, a0, rta, rext, lambda r: m_profile(rho1(r), ao))}
        for k, (r0, Md0, r, Md) in law.items():
            v = kids_fin(Mg, r0, Md0)
            tr0 = {key: {s: kids_fin(Mg, r0, truncate(r0, Md0, W[f"{s}_{key}"])) for s in SHMRS} for key in ("W10", "W30")}
            trx = {key: {s: truncate(r, Md, W[f"{s}_{key}"]) for s in SHMRS} for key in ("W10", "W30")}
            for s in SHMRS:
                out[f"{foot}|{k}|sharp|full_{s}"] = v
                for key in ("W10", "W30"):
                    out[f"{foot}|{k}|sharp|tr_{s}_{key}"] = tr0[key][s]
                for w in WINS:
                    xt = XTW[s][w]
                    out[f"{foot}|{k}|{w}|full_{s}"] = kids_fin(Mg, r, window(r, Md, RTL[s], xt))
                    for key in ("W10", "W30"):
                        out[f"{foot}|{k}|{w}|tr_{s}_{key}"] = kids_fin(Mg, r, window(r, trx[key][s], RTL[s], xt))
                # variant e: framework own windowed in its own r_ta,law units (primary x_t)
                out[f"{foot}|{k}|own|full_{s}"] = kids_fin(Mg, r, window(r, Md, rta, XTP))
                for key in ("W10", "W30"):
                    out[f"{foot}|{k}|own|tr_{s}_{key}"] = kids_fin(Mg, r, window(r, trx[key][s], rta, XTP))
        for s in SHMRS:
            dl = 0.0 if s == "moster" else EL.SHMR_INV[s](lms, zl) - LL.inv_moster(lms, zl)
            rext_fac = max(8 * max(XTW[s].values()), 6.0)
            r0, rec, r, ext, rta_l = lens_model_ext(Mg, zl, lms, foot, rext_fac, dlogM=dl)
            for k, nm, pm in (("LCDM", "M_lcdm", True), ("F_NODD", "M_nodd", True), ("PROP", "D_prop", False)):
                fn = ll_fin if pm else ll_fin_nopm
                out[f"{foot}|{k}|sharp|full_{s}"] = fn(Mg, r0, rec[nm])
                for key in ("W10", "W30"):
                    out[f"{foot}|{k}|sharp|tr_{s}_{key}"] = fn(Mg, r0, truncate(r0, rec[nm], W[f"{s}_{key}"]))
                trx = {key: truncate(r, ext[nm], W[f"{s}_{key}"]) for key in ("W10", "W30")}
                for w in WINS + ("own",):
                    xt = XTP if w == "own" else XTW[s][w]
                    out[f"{foot}|{k}|{w}|full_{s}"] = fn(Mg, r, window(r, ext[nm], RTL[s], xt))
                    for key in ("W10", "W30"):
                        out[f"{foot}|{k}|{w}|tr_{s}_{key}"] = fn(Mg, r, window(r, trx[key], RTL[s], xt))
    return out


def work_A(args):
    """ALL group: LCDM only (footing-free), both SHMR; sharp + windows; full + tr ALL."""
    Mg, zl, lms = args
    out = {}
    for s in SHMRS:
        w_ = rt_weights(f"{s}_ALL", lms, zl)
        dl = 0.0 if s == "moster" else EL.SHMR_INV[s](lms, zl) - LL.inv_moster(lms, zl)
        rtl = EL.r_ta_lcdm(lms, zl, s)[0]
        xtw = {w: xt_of(w, lMta_h(rtl, zl)) for w in WINS}
        r0, rec, r, ext, _ = lens_model_ext(Mg, zl, lms, "canonical", max(8 * max(xtw.values()), 6.0), dlogM=dl)
        out[f"LCDM|sharp|full_{s}"] = ll_fin(Mg, r0, rec["M_lcdm"])
        out[f"LCDM|sharp|tr_{s}_ALL"] = ll_fin(Mg, r0, truncate(r0, rec["M_lcdm"], w_))
        trx = truncate(r, ext["M_lcdm"], w_)
        for w in WINS:
            out[f"LCDM|{w}|full_{s}"] = ll_fin(Mg, r, window(r, ext["M_lcdm"], rtl, xtw[w]))
            out[f"LCDM|{w}|tr_{s}_ALL"] = ll_fin(Mg, r, window(r, trx, rtl, xtw[w]))
    return out


def stackup(res):
    keys = res[0].keys()
    return {k: np.array([r_[k] for r_ in res]) for k in keys}


if __name__ == "__main__":
    lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
    z = lens["z"].astype(float); Mgal = lens["Mgal"].astype(float); logMs = lens["logM"].astype(float)
    gi, GM, GZ, GS, cnt = groups(z, Mgal, logMs)
    S = np.load(os.path.join(WORK2, "cfg502_stage.npz"))
    giA, GMA, GZA, GSA, cntA = groups(S["z"], S["Mgal"], S["logM"])
    P(f"stack P groups {len(GM)}; ALL groups {len(GMA)}; x_t prim {XTP:.4f}, lo {max(XTP - XSIG, 0.1):.4f}, hi {XTP + XSIG:.4f}, "
      f"ext {TR0:.4f} + {TR1:.4f} (log M_ta - 13.8)")
    # control: the continued grid with the window at x_t -> infinity returns the continued (untruncated) profile; and the record part
    r0, Md0, r, Md = kids_Md_ext(GM[100], GZ[100], C.A0["canonical"], C.r_ta_law(GM[100], C.A0["canonical"], GZ[100]), 10.0)
    cw = float(np.max(np.abs(window(r, Md, 1.0, 1e6) / Md - 1)))
    crec = float(np.max(np.abs(Md[:1500] / Md0 - 1)))
    P(f"  [{'PASS' if max(cw, crec) < 1e-9 else 'FAIL'}] C12 window(x_t -> inf) = identity (max rel {cw:.1e}); continued grid's record part = "
      f"record (max rel {crec:.1e})")
    with Pool(4) as pool:
        resP = pool.map(work_P, list(zip(GM, GZ, GS)), chunksize=8)
        P(f"  stack P own tables done ({time.time() - T0:.0f} s)")
        resA = pool.map(work_A, list(zip(GMA, GZA, GSA)), chunksize=8)
        P(f"  ALL own tables done ({time.time() - T0:.0f} s)")
    TP = stackup(resP); TA = stackup(resA)
    # control: sharp variant = CFG503's committed own tables
    O3 = np.load(os.path.join(WORK3, "cfg503_own_tables.npz"))
    dmax = 0.0
    for k in TP:
        foot, m, v, var = k.split("|")
        if v == "sharp":
            dmax = max(dmax, float(np.max(np.abs(TP[k] - O3[f"P|{foot}|{m}|{var}"]) / (np.abs(O3[f"P|{foot}|{m}|{var}"]) + 1e-3))))
    for k in TA:
        m, v, var = k.split("|")
        if v == "sharp":
            dmax = max(dmax, float(np.max(np.abs(TA[k] - O3[f"A|{m}|{var}"]) / (np.abs(O3[f"A|{m}|{var}"]) + 1e-3))))
    P(f"  [{'PASS' if dmax < 1e-9 else 'FAIL'}] C13 sharp own variants = CFG503's committed own tables: max rel {dmax:.1e}")
    np.savez(os.path.join(WORK, "cfg504_own_tables.npz"), gi=gi, GM=GM, GZ=GZ, GS=GS, giA=giA, GMA=GMA, GZA=GZA, GSA=GSA,
             C12=max(cw, crec), C13=dmax, **{f"P|{k}": v for k, v in TP.items()}, **{f"A|{k}": v for k, v in TA.items()})
    P(f"wrote cfg504_own_tables.npz ({time.time() - T0:.0f} s)")
    open(os.path.join(HERE, "cfg504_own.out"), "w").write("\n".join(LOG) + "\n")
    sys.exit(0 if max(cw, crec, dmax) < 1e-9 else 1)
