#!/usr/bin/env python3
"""CFG503 environment tables (FROZEN_CRITERIA.md sections 1-4, 6; f56e146a1). Structure copied from CFG502's cfg502_env.py (not edited).

Builds, for SHMR in {moster (primary), behroozi} and xi mode in {eh (CFG502's colossus EH linear; moster only, for MUTATE M0),
nlz (PRIMARY: halofit xi_NL x Tinker+05 zeta), nl (xi_NL, zeta = 1; reported), lin (CAMB linear; MUTATE MH)}:
  E(R; log M*, z) for W = 10, W = 30 and ALL, and the tidal-radius weight tables of leaked satellites (stripping).
p_W(z) is CFG502's, recomputed from CFG502's staged close-pair histograms (identical arithmetic). No lensing data are read here.
Output: ../../../_external_data/cfg503_work/cfg503_env_table.npz ; cfg503_env.out ; cfg503_env_results.json
Run: nice -n 15 python3 cfg503_env.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import math, json, time
import numpy as np
from scipy.special import jv, erfinv

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg503_envlib as EL                                                   # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK2 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg502_work"))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg503_work"))
os.makedirs(WORK, exist_ok=True)
T0 = time.time()
LOG, CHK = [], {}
RES = {"lane": "CFG503", "script": "cfg503_env"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}{'' if lb else ' (reported)'}: {msg}")


S = np.load(os.path.join(WORK2, "cfg502_stage.npz"))
# ------------------------------------------------------------------ p_W(z) from close pairs (CFG502 arithmetic, verbatim)
ZB, DE, H_in, H_an = S["ZB"], S["DE"], S["H_in"], S["H_an"]
area_ratio = 0.3 ** 2 / (6.0 ** 2 - 4.0 ** 2)
EX = H_in - H_an * area_ratio
dmid = 0.5 * (DE[1:] + DE[:-1])
zc = 0.5 * (ZB[1:] + ZB[:-1])
pW = {W: np.array([EX[i][np.abs(dmid) < W].sum() / EX[i].sum() for i in range(len(zc))]) for W in (10, 30)}
P("p_10(z): " + " ".join(f"{x:.4f}" for x in pW[10]) + " ; p_30(z): " + " ".join(f"{x:.4f}" for x in pW[30]))
RES["pW"] = dict(zc=zc.tolist(), p10=pW[10].tolist(), p30=pW[30].tolist())


def pW_of(z, W):
    return float(np.interp(z, zc, pW[W]))


def mlim_of(z):
    return float(np.interp(z, S["Z0"], S["mlim"]))


# ------------------------------------------------------------------ grids (CFG502's)
LMS = np.round(np.arange(8.5, 11.0001, 0.05), 3)
ZG = np.round(np.arange(0.10, 0.5001, 0.05), 3)
RG = np.geomspace(0.005, 10.0, 120)
LMHC = np.round(np.arange(11.0, 15.5001, 0.05), 3)
KH = np.geomspace(1e-4, 1e4, 300000); LK = np.log(KH)
J2M = jv(2, KH[None, :] * RG[:, None])
DLK = np.gradient(LK)


def hank(Fk):
    return (J2M * (KH * KH * Fk * DLK)[None, :]).sum(1) / (2 * math.pi)


# ------------------------------------------------------------------ CAMB xi tables
P(f"CAMB halofit (Takahashi) + linear xi tables at z = {ZG.tolist()} ...")
X = EL.CambXi(ZG)
RES["camb_sigma8_0"] = X.sigma8_0
P(f"  done ({time.time() - T0:.0f} s); CAMB sigma_8(0) = {X.sigma8_0:.4f}")


def xi_mode(mode):
    if mode == "eh":
        return lambda r, z: EL.xi_lin_phys(r, z)
    nl = mode in ("nl", "nlz")
    def f(r, z):
        rc = np.asarray(r, float) * (1 + z) * EL.H
        x = X.xi(nl, rc, z)
        return EL.zeta_T05(x) * x if mode == "nlz" else x
    return f


MODES = ("eh", "nlz", "nl", "lin")
# C3n: shell projector with xi_NL (no exclusion) vs Hankel of P_NL
c3 = []
for z in (0.15, 0.25, 0.40):
    Rt = np.array([0.5, 1.0, 2.0, 5.0])
    a = EL.T2h_shape_gen(Rt, z, 1.0, xi_mode("nl"), exclude=False)
    b = EL.T2h_hankel_noexcl_P(Rt, z, lambda k, z=z: X.Pk(True, z, k))
    c3.append(float(np.max(np.abs(a / b - 1))))
check("C3n T2h(xi_NL, no exclusion) shell projector = Hankel rho Int P_NL J2, R 0.5-5 Mpc, z 0.15/0.25/0.40, within 2%",
      max(c3) < 0.02, f"max rel {max(c3):.2e}")
rr = np.array([1.0, 2.0, 5.0, 10.0, 20.0])
c3l = float(np.max(np.abs(X.xi(False, rr, 0.25) / EL.COSMO.correlationFunction(rr, 0.25) - 1)))
check("C3l CAMB linear xi vs colossus EH98 xi, r = 1-20 Mpc/h, z = 0.25", True, f"max rel diff {c3l:.3f}", lb=False)
for r_ in (0.5, 1.0, 2.0, 4.0):
    P(f"  z = 0.25, r = {r_} Mpc/h comoving: xi_EH {float(EL.COSMO.correlationFunction(r_, 0.25)):.3f}, xi_lin(CAMB) "
      f"{float(X.xi(False, r_, 0.25)):.3f}, xi_NL {float(X.xi(True, r_, 0.25)):.3f}, zeta {float(EL.zeta_T05(X.xi(True, r_, 0.25))):.3f}, "
      f"zeta xi_NL / xi_EH {float(EL.zeta_T05(X.xi(True, r_, 0.25)) * X.xi(True, r_, 0.25) / EL.COSMO.correlationFunction(r_, 0.25)):.2f}")

# ------------------------------------------------------------------ offset-host table (SHMR-independent), host D / A for stripping
P(f"\nbuilding tables ({time.time() - T0:.0f} s)")
DSOFF = np.zeros((len(ZG), len(LMHC), len(RG)))
AD = np.zeros((len(ZG), len(LMHC), EL.ND))
for iz, z in enumerate(ZG):
    for j, lm in enumerate(LMHC):
        c, r200 = EL.nfw_params(10 ** lm, z)
        u = EL.u_nfw(KH, c, r200)
        DSOFF[iz, j] = 10 ** lm * hank(u * u)
        AD[iz, j] = EL.host_D_and_A(lm, z)[1]
P(f"  offset-host + host-orbit tables done ({time.time() - T0:.0f} s)")


def coarse(wfine):
    idx = np.clip(np.round((EL.LMH - LMHC[0]) / 0.05).astype(int), 0, len(LMHC) - 1)
    return np.bincount(idx, weights=wfine, minlength=len(LMHC))


RT_EDGES = np.geomspace(1e-3, 20.0, 101)
RTC = np.sqrt(RT_EDGES[1:] * RT_EDGES[:-1])                      # bin representatives [Mpc physical]; slot 100 = unstripped (r_t >= r_ta)
KEYS = ("W10", "W30", "ALL")
SHMRS = ("moster", "behroozi")
SH = (len(LMS), len(ZG))
OUT = {}
DIAG = {}
for shmr in SHMRS:
    T = {k: dict(f=np.zeros(SH), fpar=np.zeros(SH), bc=np.zeros(SH), bh=np.zeros(SH), Thost=np.zeros(SH + (len(RG),)),
                 RTW=np.zeros(SH + (len(RTC) + 1,)), mfrac05=np.zeros(SH)) for k in KEYS}
    S2H = {m: np.zeros(SH + (len(RG),)) for m in MODES if (m != "eh" or shmr == "moster")}
    HOLE = np.zeros(SH + (len(RG),)); RTA = np.zeros(SH); LM200 = np.zeros(SH)
    for iz, z in enumerate(ZG):
        hod = EL.HOD(z, shmr)
        for im, lms in enumerate(LMS):
            rta, M200 = EL.r_ta_lcdm(lms, z, shmr)
            RTA[im, iz] = rta; LM200[im, iz] = math.log10(M200)
            for m in S2H:
                S2H[m][im, iz] = EL.T2h_shape_gen(RG, z, rta, xi_mode(m))
            HOLE[im, iz] = EL.hole(RG, z, rta)
            rt = EL.tidal_rt(math.log10(M200), z, rta, AD[iz])           # (LMHC, ND)
            Menc_s = EL.LL.nfw(M200, z)[0]
            mt = np.where(np.isfinite(rt), Menc_s(np.minimum(rt, 0.5)) / float(Menc_s(0.5)), 1.0)
            idx = np.where(np.isfinite(rt), np.clip(np.searchsorted(RT_EDGES, rt) - 1, 0, len(RTC) - 1), len(RTC))
            for k in KEYS:
                if k == "ALL":
                    p = hod.pieces(lms, 0.0, mlim_of(z), isolate=False)
                else:
                    p = hod.pieces(lms, pW_of(z, 10 if k == "W10" else 30), mlim_of(z), isolate=True)
                hw = coarse(p["host_w"])
                t = T[k]
                t["f"][im, iz] = p["f_W"]; t["fpar"][im, iz] = p["f_par"]; t["bc"][im, iz] = p["b_c"]; t["bh"][im, iz] = p["b_h"]
                t["Thost"][im, iz] = hw @ DSOFF[iz]
                wD = np.repeat(hw[:, None] / EL.ND, EL.ND, axis=1)
                t["RTW"][im, iz] = np.bincount(idx.ravel(), weights=wD.ravel(), minlength=len(RTC) + 1)
                t["mfrac05"][im, iz] = float((wD * mt).sum())
        P(f"  [{shmr}] z = {z:.2f} done ({time.time() - T0:.0f} s): W10 f at log M* 9.5/10.5/11.0 = "
          f"{T['W10']['f'][20, iz]:.3f}/{T['W10']['f'][40, iz]:.3f}/{T['W10']['f'][50, iz]:.3f}; b_c {T['W10']['bc'][40, iz]:.2f} "
          f"b_h {T['W10']['bh'][40, iz]:.2f}; r_ta(10.5) {RTA[40, iz]:.2f} Mpc; log M200(10.5) {LM200[40, iz]:.2f}; "
          f"W10 sat NFW mass kept inside 0.5 Mpc (10.5) {T['W10']['mfrac05'][40, iz]:.3f}")
    for m in S2H:
        for k in KEYS:
            t = T[k]; f = np.clip(t["f"], 0, 1)[..., None]
            OUT[f"E_{shmr}_{m}_{k}"] = HOLE + (1 - f) * t["bc"][..., None] * S2H[m] + f * (t["Thost"] + t["bh"][..., None] * S2H[m])
    for k in KEYS:
        for q in ("f", "fpar", "bc", "bh", "RTW", "mfrac05"):
            OUT[f"{shmr}_{k}_{q}"] = T[k][q]
    OUT[f"{shmr}_RTA"] = RTA; OUT[f"{shmr}_LM200"] = LM200
    for m in S2H:
        OUT[f"{shmr}_S2H_{m}"] = S2H[m]
    OUT[f"{shmr}_HOLE"] = HOLE
    # diagnostics: median r_t / r200c(sat) at log M* 10.5, z 0.25 (W10 hosts)
    iz = int(np.argmin(np.abs(ZG - 0.25))); im = 40
    w = T["W10"]["RTW"][im, iz]
    r200s = EL.nfw_params(10 ** LM200[im, iz], ZG[iz])[1]
    cw = np.cumsum(w[:-1]) / w.sum()
    med = float(RTC[np.searchsorted(cw, 0.5)]) if cw[-1] >= 0.5 else float("inf")
    DIAG[shmr] = dict(median_rt_Mpc=med, r200_sat_Mpc=float(r200s), rta_sat_Mpc=float(RTA[im, iz]), unstripped_share=float(w[-1] / w.sum()),
                      sat_mass_kept_lt_0p5Mpc=float(T["W10"]["mfrac05"][im, iz]))

OUT.update(LMS=LMS, ZG=ZG, RG=RG, RTC=RTC, RT_EDGES=RT_EDGES, pW10=pW[10], pW30=pW[30], zc=zc)
np.savez(os.path.join(WORK, "cfg503_env_table.npz"), **OUT)
P(f"\nwrote cfg503_env_table.npz ({time.time() - T0:.0f} s)")

# ------------------------------------------------------------------ checks / diagnostics
E2 = np.load(os.path.join(WORK2, "cfg502_env_table.npz"))
dmax = max(float(np.max(np.abs(OUT[f"E_moster_eh_{k}"] - E2[f"E_{k}"]) / (np.abs(E2[f"E_{k}"]) + 1e3))) for k in KEYS)
check("C0e the copied CFG502 path (moster, colossus EH, no zeta) rebuilds CFG502's E tables (W10/W30/ALL)", dmax < 1e-9,
      f"max |diff| / (|E| + 1e3 Msun/Mpc^2) = {dmax:.1e}")
P(f"  C8 (reported) leaked satellite at log M* 10.5, z 0.25, W10 hosts: " + "; ".join(
    f"{s}: median r_t {d['median_rt_Mpc']:.3f} Mpc (r200c {d['r200_sat_Mpc']:.3f}, r_ta {d['rta_sat_Mpc']:.3f}; median r_t / r200c "
    f"{d['median_rt_Mpc'] / d['r200_sat_Mpc']:.2f}), unstripped share {d['unstripped_share']:.3f}, NFW mass kept inside 0.5 Mpc "
    f"{d['sat_mass_kept_lt_0p5Mpc']:.3f}" for s, d in DIAG.items()))
RES["C8"] = DIAG
iz = 3
P("\n  E at z 0.25 (Msun/pc^2) for log M* 10.0 / 10.5, R = 0.11 / 0.44 / 1.04 / 2.17 Mpc:")
for key in ("E_moster_eh_W10", "E_moster_nl_W10", "E_moster_nlz_W10", "E_moster_lin_W10", "E_behroozi_nlz_W10"):
    vals = []
    for im in (30, 40):
        vals.append(" ".join(f"{np.interp(math.log(R_), np.log(RG), OUT[key][im, iz]) * 1e-12:6.3f}" for R_ in (0.11, 0.44, 1.04, 2.17)))
    P(f"    {key:22s}: {vals[0]}  |  {vals[1]}")
RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, "cfg503_env_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg503_env.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if any(c["load_bearing"] and not c["ok"] for c in CHK.values()) else 0)
