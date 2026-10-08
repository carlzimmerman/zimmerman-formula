#!/usr/bin/env python3
"""CFG503 own-profile tables with tidal stripping of leaked satellites (FROZEN_CRITERIA.md sections 3-4; f56e146a1).

Per lens group (CFG377 grouping; stack P / f30 groups and the ALL groups of CFG502's staging) and per footing, every model's 15-bin own
ESD [Msun/pc^2] in variants:
  full_<shmr>        : unstripped (= CFG502's own profile; for shmr = moster this is CFG495's / CFG487's / CFG413's vector)
  tr_<shmr>_<key>    : the leaked-satellite version, distributed own mass M_d(r) -> sum_j w_j M_d(min(r, r_t,j)), with w the tidal-radius
                       weights of the passed-satellite hosts of sample key (W10, W30; ALL for the ALL groups), interpolated to the group.
Model code copied from CFG502's cfg502_score.py (kids_vec) and CFG495's lens_model (imported read-only); not edited.
Output: ../../../_external_data/cfg503_work/cfg503_own_tables.npz ; cfg503_own.out
Run: nice -n 15 python3 cfg503_own.py   (4 worker processes, 1 thread each)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import math, json, time
import numpy as np
from multiprocessing import Pool
from scipy.interpolate import RegularGridInterpolator

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
import cfg503_envlib as EL                                                   # noqa: E402

WORK2 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg502_work"))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg503_work"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
FOOTS = ("canonical", "alt")
SHMRS = ("moster", "behroozi")
LOG = []
T0 = time.time()


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def groups(z, Mgal, logMs):
    lmg = np.log10(Mgal)
    key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(z / 0.03).astype(np.int64)
    _, gi, cnt = np.unique(key, return_inverse=True, return_counts=True)
    gi = gi.ravel()
    return gi, 10 ** (np.bincount(gi, weights=lmg) / cnt), np.bincount(gi, weights=z) / cnt, np.bincount(gi, weights=logMs) / cnt, cnt


ET = np.load(os.path.join(WORK, "cfg503_env_table.npz"))
LMS, ZG, RTC = ET["LMS"], ET["ZG"], ET["RTC"]
RTI = {f"{s}_{k}": RegularGridInterpolator((LMS, ZG), ET[f"{s}_{k}_RTW"], bounds_error=False, fill_value=None)
       for s in SHMRS for k in ("W10", "W30", "ALL")}


def rt_weights(tag, lms, z):
    w = RTI[tag]([[min(max(lms, LMS[0]), LMS[-1]), min(max(z, ZG[0]), ZG[-1])]])[0]
    w = np.maximum(w, 0.0)
    return w / w.sum()


def truncate(r, Md, w):
    """sum_j w_j Md(min(r, r_t,j)) + w_unstripped Md(r)."""
    out = w[-1] * Md
    nz = np.nonzero(w[:-1] > 0)[0]
    if len(nz):
        rt = RTC[nz]
        out = out + (w[nz, None] * np.interp(np.minimum(r[None, :], rt[:, None]), r, Md)).sum(0)
    return out


SC = LB.ShellClock(Om=C.OM)
RHO_M0_MPC = C.OM * C.RHOC0


def m_profile(rho_ratio, a_obs):
    return SC.m_of_rho(rho_ratio, a_obs, conservative=False)[0]


def kids_Md(Mg, zl, a0, rout, mfun=None):           # CFG487's kids_vec, split: the distributed mass on its grid
    r = np.geomspace(1e-4, rout, 1500)
    Md = Mg * (C.nu_mono(C.G_MPC * Mg / r ** 2 / a0) - 1.0)
    if mfun is not None:
        mm = mfun(r)
        dM = np.diff(np.concatenate([[0.0], Md]))
        mmid = np.concatenate([[mm[0]], 0.5 * (mm[1:] + mm[:-1])])
        Md = np.cumsum(mmid * dM)
    return r, Md


def kids_fin(Mg, r, Md):
    return C._finish(lambda R: C.dsigma(R, r, Md) + Mg / (math.pi * R ** 2), Mg)


def ll_fin(Mg, r, M):
    return LL.finish(lambda R: LL.dsigma(R, r, M) + Mg / (math.pi * R ** 2), Mg)


def ll_fin_nopm(Mg, r, M):
    return LL.finish(lambda R: LL.dsigma(R, r, M), Mg)


def work_P(args):
    """stack-P group: every model, both footings, both SHMR, variants full + tr W10 / W30."""
    Mg, zl, lms = args
    out = {}
    W = {f"{s}_{k}": rt_weights(f"{s}_{k}", lms, zl) for s in SHMRS for k in ("W10", "W30")}
    for foot in FOOTS:
        a0 = C.A0[foot]; ao = 1.0 / (1.0 + zl)
        rta = C.r_ta_law(Mg, a0, zl)
        re1 = float(LB.r_edge(Mg, C.G_MPC, a0))
        rho1 = lambda r: Mg * C.nu_mono(C.G_MPC * Mg / r ** 2 / a0) / (4 * math.pi / 3 * r ** 3) / RHO_M0_MPC
        law = {"LAW_RTA": kids_Md(Mg, zl, a0, rta), "LAW_X05": kids_Md(Mg, zl, a0, 0.5 * rta), "EDGE": kids_Md(Mg, zl, a0, re1),
               "V1": kids_Md(Mg, zl, a0, rta, lambda r: m_profile(rho1(r), ao))}
        for k, (r, Md) in law.items():
            v = kids_fin(Mg, r, Md)
            for s in SHMRS:
                out[f"{foot}|{k}|full_{s}"] = v
                for key in ("W10", "W30"):
                    out[f"{foot}|{k}|tr_{s}_{key}"] = kids_fin(Mg, r, truncate(r, Md, W[f"{s}_{key}"]))
        for s in SHMRS:
            dl = 0.0 if s == "moster" else EL.SHMR_INV[s](lms, zl) - LL.inv_moster(lms, zl)
            m = LL.lens_model(Mg, zl, lms, foot, dlogM=dl)
            r = m["r"]
            for k, M, pm in (("LCDM", m["M_lcdm"], True), ("F_NODD", m["M_nodd"], True), ("PROP", m["D_prop"], False)):
                fn = ll_fin if pm else ll_fin_nopm
                out[f"{foot}|{k}|full_{s}"] = fn(Mg, r, M)
                for key in ("W10", "W30"):
                    out[f"{foot}|{k}|tr_{s}_{key}"] = fn(Mg, r, truncate(r, M, W[f"{s}_{key}"]))
    return out


def work_A(args):
    """ALL group: LCDM only (footing-free), both SHMR, variants full + tr ALL."""
    Mg, zl, lms = args
    out = {}
    for s in SHMRS:
        w = rt_weights(f"{s}_ALL", lms, zl)
        dl = 0.0 if s == "moster" else EL.SHMR_INV[s](lms, zl) - LL.inv_moster(lms, zl)
        m = LL.lens_model(Mg, zl, lms, "canonical", dlogM=dl)
        out[f"LCDM|full_{s}"] = ll_fin(Mg, m["r"], m["M_lcdm"])
        out[f"LCDM|tr_{s}_ALL"] = ll_fin(Mg, m["r"], truncate(m["r"], m["M_lcdm"], w))
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
    P(f"stack P groups {len(GM)}; ALL groups {len(GMA)}")
    # control C7: no stripping (all weight in the unstripped slot) returns the full vector
    wnone = np.zeros(len(RTC) + 1); wnone[-1] = 1.0
    r, Md = kids_Md(GM[100], GZ[100], C.A0["canonical"], C.r_ta_law(GM[100], C.A0["canonical"], GZ[100]))
    c7 = float(np.max(np.abs(kids_fin(GM[100], r, truncate(r, Md, wnone)) / kids_fin(GM[100], r, Md) - 1)))
    wbig = np.zeros(len(RTC) + 1); wbig[-2] = 1.0                           # r_t = 19 Mpc > every r_ta
    c7b = float(np.max(np.abs(kids_fin(GM[100], r, truncate(r, Md, wbig)) / kids_fin(GM[100], r, Md) - 1)))
    P(f"  [{'PASS' if max(c7, c7b) < 1e-9 else 'FAIL'}] C7 stripping code with r_t beyond r_ta returns the unstripped vector: "
      f"max rel {c7:.1e} (unstripped slot), {c7b:.1e} (r_t = {RTC[-1]:.1f} Mpc)")
    with Pool(4) as pool:
        resP = pool.map(work_P, list(zip(GM, GZ, GS)), chunksize=8)
        P(f"  stack P own tables done ({time.time() - T0:.0f} s)")
        resA = pool.map(work_A, list(zip(GMA, GZA, GSA)), chunksize=8)
        P(f"  ALL own tables done ({time.time() - T0:.0f} s)")
    TP = stackup(resP); TA = stackup(resA)
    np.savez(os.path.join(WORK, "cfg503_own_tables.npz"), gi=gi, GM=GM, GZ=GZ, GS=GS, giA=giA, GMA=GMA, GZA=GZA, GSA=GSA,
             C7=max(c7, c7b), **{f"P|{k}": v for k, v in TP.items()}, **{f"A|{k}": v for k, v in TA.items()})
    P(f"wrote cfg503_own_tables.npz ({time.time() - T0:.0f} s)")
    open(os.path.join(HERE, "cfg503_own.out"), "w").write("\n".join(LOG) + "\n")
    sys.exit(0 if max(c7, c7b) < 1e-9 else 1)
