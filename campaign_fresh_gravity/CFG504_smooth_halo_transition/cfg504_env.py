#!/usr/bin/env python3
"""CFG504 environment tables (FROZEN_CRITERIA.md sections 1, 5, 7; criteria commit 333a5fce4). The HOD / host / stripping loop is a copy of
CFG503's cfg503_env.py (f56e146a1 / b78648975), restricted to the primary two-halo mode 'nlz' (CAMB halofit xi_NL x Tinker+05 zeta).

Per SHMR (moster primary, behroozi) and grid point (log M*, z):
  sharp (CFG503):  HOLE = -DS[rho_bar on r < r_ta],  S2H = DS[rho_bar zeta xi_NL on r > r_ta]          (rebuilt; C0 = CFG503's E tables)
  smooth (CFG504): HS_v = -DS[rho_bar f_t(r/r_ta)],  SS_v = DS[rho_bar zeta xi_NL (1 - f_t(r/r_ta))]    on r in [5e-3, 200] Mpc
  E_v = HS_v + (1 - f) b_c A SS_v + f [T_host + b_h A SS_v]   (assembled in cfg504_score.py; A = 1 except the reported variant c)
Window variants v (x_t from cfg504_calib_results.json): prim, lo (x_t - sigma_tot), hi (x_t + sigma_tot), ext (x_t linear in log M_ta
of the lens, clipped to [0.1, 3]), steep (C9: beta 64, gamma 128, x_t = 1).
Output: ../../../_external_data/cfg504_work/cfg504_env_table.npz ; cfg504_env.out ; cfg504_env_results.json
Run: nice -n 15 python3 cfg504_env.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import math, json, time
import numpy as np
from scipy.special import jv

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg504_envlib as EL                                                   # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK2 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg502_work"))
WORK3 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg503_work"))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg504_work"))
T0 = time.time()
LOG, CHK = [], {}
RES = {"lane": "CFG504", "script": "cfg504_env"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}{'' if lb else ' (reported)'}: {msg}")


CAL = json.load(open(os.path.join(HERE, "cfg504_calib_results.json")))["primary"]
XTP, XSIG = CAL["x_t"], CAL["sigma_tot"]
TR0, TR1 = CAL["trend_intercept_at_13p8"], CAL["trend_slope_per_dex"]
WIN = {"prim": (XTP, 4.0, 8.0), "lo": (max(XTP - XSIG, 0.1), 4.0, 8.0), "hi": (XTP + XSIG, 4.0, 8.0), "ext": (None, 4.0, 8.0),
       "steep": (1.0, 64.0, 128.0)}
P(f"windows: " + ", ".join(f"{k}: x_t {v[0] if v[0] is not None else 'trend'} beta {v[1]} gamma {v[2]}" for k, v in WIN.items())
  + f"; trend x_t = {TR0:.4f} + {TR1:.4f} (log M_ta[Msun/h] - 13.8)")
RES["windows"] = {k: list(v) for k, v in WIN.items()}

S = np.load(os.path.join(WORK2, "cfg502_stage.npz"))
ZB, DE, H_in, H_an = S["ZB"], S["DE"], S["H_in"], S["H_an"]
area_ratio = 0.3 ** 2 / (6.0 ** 2 - 4.0 ** 2)
EX = H_in - H_an * area_ratio
dmid = 0.5 * (DE[1:] + DE[:-1])
zc = 0.5 * (ZB[1:] + ZB[:-1])
pW = {W: np.array([EX[i][np.abs(dmid) < W].sum() / EX[i].sum() for i in range(len(zc))]) for W in (10, 30)}


def pW_of(z, W):
    return float(np.interp(z, zc, pW[W]))


def mlim_of(z):
    return float(np.interp(z, S["Z0"], S["mlim"]))


LMS = np.round(np.arange(8.5, 11.0001, 0.05), 3)
ZG = np.round(np.arange(0.10, 0.5001, 0.05), 3)
RG = np.geomspace(0.005, 10.0, 120)
LMHC = np.round(np.arange(11.0, 15.5001, 0.05), 3)
KH = np.geomspace(1e-4, 1e4, 300000); LK = np.log(KH)
J2M = jv(2, KH[None, :] * RG[:, None])
DLK = np.gradient(LK)


def hank(Fk):
    return (J2M * (KH * KH * Fk * DLK)[None, :]).sum(1) / (2 * math.pi)


P(f"CAMB halofit xi tables at z = {ZG.tolist()} ...")
X = EL.CambXi(ZG)


def xi_nlz(r, z):
    rc = np.asarray(r, float) * (1 + z) * EL.H
    x = X.xi(True, rc, z)
    return EL.zeta_T05(x) * x


def ft(x, xt, be, ga):
    return (1.0 + (x / xt) ** be) ** (-ga / be)


def smooth_terms(z, rta, xt, be, ga):
    rmax = 200.0
    r = np.geomspace(5e-3, rmax, 4000)
    rm = np.sqrt(r[1:] * r[:-1])
    f = ft(rm / rta, xt, be, ga)
    dM2 = 4 * math.pi * rm ** 2 * EL.rho_m(z) * xi_nlz(rm, z) * (1 - f) * np.diff(r)
    S2 = EL.LL.dsigma(RG, r, np.concatenate([[0.0], np.cumsum(dM2)]))
    rh = np.geomspace(1e-5, max(10 * xt, 8.0) * rta, 3000)
    rhm = np.sqrt(rh[1:] * rh[:-1])
    dMh = 4 * math.pi * rhm ** 2 * EL.rho_m(z) * ft(rhm / rta, xt, be, ga) * np.diff(rh)
    M0 = 4 * math.pi / 3 * rh[0] ** 3 * EL.rho_m(z)
    Hs = -EL.LL.dsigma(RG, rh, np.concatenate([[M0], M0 + np.cumsum(dMh)]))
    return Hs, S2


def lMta_h(rta, z):
    return math.log10(4 * math.pi / 3 * rta ** 3 * EL.rho_m(z) * EL.LL.dta(z) * EL.H)


P(f"\nbuilding tables ({time.time() - T0:.0f} s)")
DSOFF = np.zeros((len(ZG), len(LMHC), len(RG)))
for iz, z in enumerate(ZG):
    for j, lm in enumerate(LMHC):
        c, r200 = EL.nfw_params(10 ** lm, z)
        u = EL.u_nfw(KH, c, r200)
        DSOFF[iz, j] = 10 ** lm * hank(u * u)


def coarse(wfine):
    idx = np.clip(np.round((EL.LMH - LMHC[0]) / 0.05).astype(int), 0, len(LMHC) - 1)
    return np.bincount(idx, weights=wfine, minlength=len(LMHC))


KEYS = ("W10", "W30", "ALL")
SHMRS = ("moster", "behroozi")
SH = (len(LMS), len(ZG))
OUT = {}
for shmr in SHMRS:
    T = {k: dict(f=np.zeros(SH), bc=np.zeros(SH), bh=np.zeros(SH), Thost=np.zeros(SH + (len(RG),))) for k in KEYS}
    HOLE = np.zeros(SH + (len(RG),)); S2H = np.zeros(SH + (len(RG),)); RTA = np.zeros(SH); XTE = np.zeros(SH)
    HSv = {v: np.zeros(SH + (len(RG),)) for v in WIN}; SSv = {v: np.zeros(SH + (len(RG),)) for v in WIN}
    for iz, z in enumerate(ZG):
        hod = EL.HOD(z, shmr)
        for im, lms in enumerate(LMS):
            rta, M200 = EL.r_ta_lcdm(lms, z, shmr)
            RTA[im, iz] = rta
            S2H[im, iz] = EL.T2h_shape_gen(RG, z, rta, xi_nlz)
            HOLE[im, iz] = EL.hole(RG, z, rta)
            XTE[im, iz] = float(np.clip(TR0 + TR1 * (lMta_h(rta, z) - 13.8), 0.1, 3.0))
            for v, (xt, be, ga) in WIN.items():
                HSv[v][im, iz], SSv[v][im, iz] = smooth_terms(z, rta, XTE[im, iz] if xt is None else xt, be, ga)
            for k in KEYS:
                if k == "ALL":
                    p = hod.pieces(lms, 0.0, mlim_of(z), isolate=False)
                else:
                    p = hod.pieces(lms, pW_of(z, 10 if k == "W10" else 30), mlim_of(z), isolate=True)
                hw = coarse(p["host_w"])
                t = T[k]
                t["f"][im, iz] = p["f_W"]; t["bc"][im, iz] = p["b_c"]; t["bh"][im, iz] = p["b_h"]
                t["Thost"][im, iz] = hw @ DSOFF[iz]
        P(f"  [{shmr}] z = {z:.2f} done ({time.time() - T0:.0f} s); x_t(ext) at log M* 10.5: {XTE[40, iz]:.3f}")
    for k in KEYS:
        t = T[k]; f = np.clip(t["f"], 0, 1)[..., None]
        OUT[f"E_{shmr}_sharp_{k}"] = HOLE + (1 - f) * t["bc"][..., None] * S2H + f * (t["Thost"] + t["bh"][..., None] * S2H)
        for q in ("f", "bc", "bh", "Thost"):
            OUT[f"{shmr}_{k}_{q}"] = t[q]
    OUT[f"{shmr}_HOLE"] = HOLE; OUT[f"{shmr}_S2H"] = S2H; OUT[f"{shmr}_RTA"] = RTA; OUT[f"{shmr}_XTE"] = XTE
    for v in WIN:
        OUT[f"{shmr}_HS_{v}"] = HSv[v]; OUT[f"{shmr}_SS_{v}"] = SSv[v]

OUT.update(LMS=LMS, ZG=ZG, RG=RG)
np.savez(os.path.join(WORK, "cfg504_env_table.npz"), **OUT)
P(f"\nwrote cfg504_env_table.npz ({time.time() - T0:.0f} s)")

E3 = np.load(os.path.join(WORK3, "cfg503_env_table.npz"))
dmax = max(float(np.max(np.abs(OUT[f"E_{s}_sharp_{k}"] - E3[f"E_{s}_nlz_{k}"]) / (np.abs(E3[f"E_{s}_nlz_{k}"]) + 1e3)))
           for s in SHMRS for k in KEYS)
check("C0 the copied CFG503 path (sharp window, nlz) rebuilds CFG503's E tables (both SHMR, W10/W30/ALL)", dmax < 1e-9,
      f"max |diff| / (|E| + 1e3 Msun/Mpc^2) = {dmax:.1e}")
for q in ("f", "bc", "bh"):
    dq = max(float(np.max(np.abs(OUT[f"{s}_{k}_{q}"] - E3[f"{s}_{k}_{q}"]))) for s in SHMRS for k in KEYS)
    check(f"C0{q} HOD piece '{q}' equals CFG503's table", dq < 1e-12, f"max |diff| {dq:.1e}")
iz = 3
P("\n  E pieces at z 0.25, log M* 10.5 (Msun/pc^2), R = 0.44 / 0.78 / 1.04 / 1.38 / 1.82 / 2.17 Mpc (r_ta "
  f"{OUT['moster_RTA'][40, iz]:.2f} Mpc):")
for lab, arr in (("HOLE sharp", OUT["moster_HOLE"]), ("HS prim", OUT["moster_HS_prim"]), ("S2H sharp (b=1)", OUT["moster_S2H"]),
                 ("SS prim (b=1)", OUT["moster_SS_prim"]), ("HS steep", OUT["moster_HS_steep"]), ("SS steep", OUT["moster_SS_steep"])):
    P(f"    {lab:16s}: " + " ".join(f"{np.interp(math.log(R_), np.log(RG), arr[40, iz]) * 1e-12:7.3f}" for R_ in (0.44, 0.78, 1.04, 1.38, 1.82, 2.17)))
RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, "cfg504_env_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg504_env.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if any(c["load_bearing"] and not c["ok"] for c in CHK.values()) else 0)
