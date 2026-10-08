#!/usr/bin/env python3
"""CFG502 environment table (FROZEN_CRITERIA.md section 2, 5; cacadd50d). Builds E(R; log M*, z) for W = 10, 30 and ALL from the
frozen halo model, with p_W measured from the staged close-pair histograms; runs controls C3, C4; the photometric contamination check.
No lensing data are read here.  MUTATE (CFG502_MUTATE=1) is applied in the scoring script, not here.
Output: ../../../_external_data/cfg502_work/cfg502_env_table.npz ; cfg502_env.out ; cfg502_env_results.json
Run: nice -n 15 python3 cfg502_env.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import math, json, time
import numpy as np
from scipy.special import jv, erfinv

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg502_envlib as EL                                                   # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg502_work"))
T0 = time.time()
LOG, CHK = [], {}
RES = {"lane": "CFG502", "script": "cfg502_env"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


S = np.load(os.path.join(WORK, "cfg502_stage.npz"))
# ------------------------------------------------------------------ p_W(z) from close pairs
ZB, DE, H_in, H_an = S["ZB"], S["DE"], S["H_in"], S["H_an"]
area_ratio = 0.3 ** 2 / (6.0 ** 2 - 4.0 ** 2)
EX = H_in - H_an * area_ratio
dmid = 0.5 * (DE[1:] + DE[:-1])
zc = 0.5 * (ZB[1:] + ZB[:-1])
pW = {}
P("photo-z leakage (close pairs R_p < 0.3 Mpc, companion log M* > log M*_lens - 1; background 4-6 Mpc annulus)")
P("  z_bin     excess_pairs  p_10    p_30    sigma_pair(Gauss-eq, Mpc)  sigma_single(Mpc)")
RES["pW"] = {}
for W in (10, 30):
    pW[W] = np.array([EX[i][np.abs(dmid) < W].sum() / EX[i].sum() for i in range(len(zc))])
sig_pair = 10.0 / (math.sqrt(2) * erfinv(np.clip(pW[10], 1e-6, 0.999)))
for i in range(len(zc)):
    P(f"  {ZB[i]:.2f}-{ZB[i + 1]:.2f}  {EX[i].sum():12.0f}  {pW[10][i]:.4f}  {pW[30][i]:.4f}  {sig_pair[i]:8.1f}  {sig_pair[i] / math.sqrt(2):8.1f}")
RES["pW"] = dict(zc=zc.tolist(), p10=pW[10].tolist(), p30=pW[30].tolist(), sigma_pair=sig_pair.tolist(), excess=EX.sum(1).tolist())
# consistency: p_30 vs the Gaussian with the p_10 sigma (reported)
pg30 = [math.erf(30 / (s_ * math.sqrt(2))) for s_ in sig_pair]
P("  Gaussian check p_30 from the p_10 sigma: " + " ".join(f"{a:.3f}/{b:.3f}" for a, b in zip(pW[30], pg30)) + "  (measured / Gaussian)")
zi = 0.25
sig1_025 = float(np.interp(zi, zc, sig_pair)) / math.sqrt(2)
RES["sigma_single_z025_Mpc"] = sig1_025
P(f"  single-galaxy Gaussian-equivalent sigma_chi at z = 0.25: {sig1_025:.1f} Mpc ({sig1_025 * EL.H:.1f} Mpc/h)")


def pW_of(z, W):
    return float(np.interp(z, zc, pW[W]))


def mlim_of(z):
    return float(np.interp(z, S["Z0"], S["mlim"]))


# ------------------------------------------------------------------ grids
LMS = np.round(np.arange(8.5, 11.0001, 0.05), 3)
ZG = np.round(np.arange(0.10, 0.5001, 0.05), 3)
RG = np.geomspace(0.005, 10.0, 120)                                          # physical Mpc
LMHC = np.round(np.arange(11.0, 15.5001, 0.05), 3)
KH = np.geomspace(1e-4, 1e4, 300000); LK = np.log(KH)   # run 1 used (1e-4..1e3, 40000): C4 failed at 1.2% (disclosed)
J2M = jv(2, KH[None, :] * RG[:, None])                                       # (R, k)
DLK = np.gradient(LK)


def hank(Fk):
    return (J2M * (KH * KH * Fk * DLK)[None, :]).sum(1) / (2 * math.pi)


# C4 with this grid
c4 = []
for M in (1e12, 1e13, 1e14):
    c, r200 = EL.nfw_params(M, 0.25)
    a = M * hank(EL.u_nfw(KH, c, r200))
    sel = (RG >= 0.05) & (RG <= 2.0)
    b = EL.ds_nfw_trunc_real(M, 0.25, RG[sel])
    c4.append(float(np.max(np.abs(a[sel] / b - 1))))
check("C4 offset kernel at zero offset (u_s = 1) = centred truncated NFW, R 0.05-2 Mpc, within 1%", max(c4) < 0.01, f"max rel {max(c4):.2e}")
# C3
c3 = []
for z in (0.15, 0.25, 0.4):
    Rt = np.array([0.5, 1.0, 2.0, 5.0])
    a = EL.T2h_shape(Rt, z, 1.0, exclude=False); b = EL.T2h_hankel_noexcl(Rt, z)
    c3.append(float(np.max(np.abs(a / b - 1))))
check("C3 T2h (no exclusion) shell projector = Hankel b rho Int P J2, R 0.5-5 Mpc, within 2%", max(c3) < 0.02, f"max rel {max(c3):.2e}")

# ------------------------------------------------------------------ offset-host table per z
P(f"\nbuilding tables ({time.time() - T0:.0f} s)")
DSOFF = np.zeros((len(ZG), len(LMHC), len(RG)))
PPROJ = np.zeros((len(ZG), len(LMHC)))
for iz, z in enumerate(ZG):
    for j, lm in enumerate(LMHC):
        c, r200 = EL.nfw_params(10 ** lm, z)
        u = EL.u_nfw(KH, c, r200)
        DSOFF[iz, j] = 10 ** lm * hank(u * u)
        PPROJ[iz, j] = EL.P2D_proj_frac(10 ** lm, z, 0.5 / (1 + z))          # 0.5 Mpc comoving -> physical
P(f"  offset-host table done ({time.time() - T0:.0f} s)")


def coarse(wfine):
    idx = np.clip(np.round((EL.LMH - LMHC[0]) / 0.05).astype(int), 0, len(LMHC) - 1)
    return np.bincount(idx, weights=wfine, minlength=len(LMHC))


KEYS = ("W10", "W30", "ALL")
SH = (len(LMS), len(ZG))
T = {k: dict(f=np.zeros(SH), fpar=np.zeros(SH), bc=np.zeros(SH), bh=np.zeros(SH), Thost=np.zeros(SH + (len(RG),)),
             pred_count=np.zeros(SH), lMh_host=np.zeros(SH), lMh_cen=np.zeros(SH), Pc=np.zeros(SH), Ps=np.zeros(SH)) for k in KEYS}
S2H = np.zeros(SH + (len(RG),)); HOLE = np.zeros(SH + (len(RG),)); RTA = np.zeros(SH); WPD = np.zeros(len(ZG))
for iz, z in enumerate(ZG):
    hod = EL.HOD(z)
    # disc-integrated projected linear correlation, comoving R1 = 0.5 Mpc, |pi| < 300 Mpc comoving
    Rg = np.linspace(1e-3, 0.5, 60); pig = np.linspace(-300, 300, 3001)
    rr = np.sqrt(Rg[:, None] ** 2 + pig[None, :] ** 2)
    xi = EL.COSMO.correlationFunction(np.maximum(rr.ravel() * EL.H, 1.01e-3), z).reshape(rr.shape)
    WPD[iz] = float(np.trapz(2 * math.pi * Rg * np.trapz(xi, pig, axis=1), Rg))
    for im, lms in enumerate(LMS):
        rta, M200 = EL.r_ta_lcdm(lms, z)
        RTA[im, iz] = rta
        S2H[im, iz] = EL.T2h_shape(RG, z, rta)
        HOLE[im, iz] = EL.hole(RG, z, rta)
        for k in KEYS:
            if k == "ALL":
                p = hod.pieces(lms, 0.0, mlim_of(z), isolate=False)
            else:
                p = hod.pieces(lms, pW_of(z, 10 if k == "W10" else 30), mlim_of(z), isolate=True)
            hw = coarse(p["host_w"])
            t = T[k]
            t["f"][im, iz] = p["f_W"]; t["fpar"][im, iz] = p["f_par"]; t["bc"][im, iz] = p["b_c"]; t["bh"][im, iz] = p["b_h"]
            t["Thost"][im, iz] = hw @ DSOFF[iz]
            t["lMh_host"][im, iz] = p["lMh_host_mean"]; t["lMh_cen"][im, iz] = p["lMh_cen_mean"]
            t["Pc"][im, iz] = p["Pc_mean"]; t["Ps"][im, iz] = p["Ps_mean"]
            # satellite companions (central + more-massive siblings) inside 0.5 Mpc comoving, per lens
            Nsib = EL.Nsat_gt(lms, z)
            t["pred_count"][im, iz] = p["f_W"] * float((p["host_w"] * np.interp(EL.LMH, LMHC, PPROJ[iz]) * (1 + Nsib)).sum())
    P(f"  z = {z:.2f} done ({time.time() - T0:.0f} s): W10 f at log M* 9.5/10.5/11.0 = "
      f"{T['W10']['f'][20, iz]:.3f}/{T['W10']['f'][40, iz]:.3f}/{T['W10']['f'][50, iz]:.3f} (parent {T['W10']['fpar'][40, iz]:.3f}); "
      f"b_c {T['W10']['bc'][40, iz]:.2f} b_h {T['W10']['bh'][40, iz]:.2f}; r_ta(10.5) {RTA[40, iz]:.2f} Mpc")


def E_of(k, fscale=1.0):
    t = T[k]
    f = np.clip(t["f"] * fscale, 0, 1)[..., None]
    return HOLE + (1 - f) * t["bc"][..., None] * S2H + f * (t["Thost"] + t["bh"][..., None] * S2H)


np.savez(os.path.join(WORK, "cfg502_env_table.npz"), LMS=LMS, ZG=ZG, RG=RG, S2H=S2H, HOLE=HOLE, RTA=RTA,
         **{f"{k}_{q}": v for k in KEYS for q, v in T[k].items()}, E_W10=E_of("W10"), E_W30=E_of("W30"), E_ALL=E_of("ALL"),
         E_W10_f0=E_of("W10", 0.0), WPD=WPD, pW10=pW[10], pW30=pW[30], zc=zc)
P(f"\nwrote cfg502_env_table.npz ({time.time() - T0:.0f} s)")

# ------------------------------------------------------------------ section 5: companion counts around ISO lenses
iso_idx = S["iso_idx"]
zl = S["z"][iso_idx]; lml = S["logM"][iso_idx]
area_in = math.pi * 0.25; area_an = math.pi * 20.0
meas = S["cin"] - S["can"] * area_in / area_an
n3d = S["can50"] / (area_an * 100.0)                                         # comoving Mpc^-3, more-massive pool galaxies
wlens = S["WW"][iso_idx].sum(1)


def interp2(tab, lm, z):
    from scipy.interpolate import RegularGridInterpolator
    f = RegularGridInterpolator((LMS, ZG), tab, bounds_error=False, fill_value=None)
    return f(np.c_[np.clip(lm, LMS[0], LMS[-1]), np.clip(z, ZG[0], ZG[-1])])


t = T["W10"]
pred_sat = interp2(t["pred_count"], lml, zl)
fW = interp2(t["f"], lml, zl); bc = interp2(t["bc"], lml, zl); bh = interp2(t["bh"], lml, zl)
beff = (1 - fW) * bc + fW * bh
pred_2h = n3d * beff * bc * np.interp(zl, ZG, WPD)
pred = pred_sat + pred_2h
RES["counts"] = {}
P("\nsection 5: more-massive companions within 0.5 Mpc (10 < |dchi| < 600), excess over the 4-6 Mpc annulus, per ISO lens")
P("  z_bin      n_lens   measured  pred_sat  pred_2h  pred   meas/pred")
for i in range(len(ZB) - 1):
    m = (zl >= ZB[i]) & (zl < ZB[i + 1])
    if m.sum() == 0:
        continue
    a, b_, c_ = meas[m].mean(), pred_sat[m].mean(), pred_2h[m].mean()
    P(f"  {ZB[i]:.2f}-{ZB[i + 1]:.2f}  {m.sum():7d}  {a:8.4f}  {b_:8.4f}  {c_:7.4f}  {b_ + c_:6.4f}  {a / (b_ + c_):6.3f}")
    RES["counts"][f"{ZB[i]:.2f}"] = dict(n=int(m.sum()), meas=float(a), pred_sat=float(b_), pred_2h=float(c_))
rw = float((wlens * meas).sum() / (wlens * pred).sum()); ru = float(meas.mean() / pred.mean())
RES["counts"]["ratio_stack_weighted"] = rw; RES["counts"]["ratio_unweighted"] = ru
lab = 0.67 <= rw <= 1.5
RES["label_contamination"] = None if lab else "CONTAMINATION NOT CONFIRMED BY COUNTS"
P(f"  measured / predicted: stack-weighted {rw:.3f}, unweighted {ru:.3f}  -> tolerance [0.67, 1.5]: "
  f"{'within' if lab else 'OUTSIDE -> label CONTAMINATION NOT CONFIRMED BY COUNTS'}")
mw = float((wlens * meas).sum() / wlens.sum())
P(f"  stack-weighted measured excess {mw:.4f} per lens; predicted satellites {float((wlens * pred_sat).sum() / wlens.sum()):.4f}, "
  f"two-halo {float((wlens * pred_2h).sum() / wlens.sum()):.4f}")
# stack-weighted f_W of the ISO sample and of ALL
fall = interp2(T["ALL"]["f"], S["logM"], S["z"])
wall = S["WW"].sum(1)
RES["f_W_iso_stack_weighted"] = float((wlens * fW).sum() / wlens.sum())
RES["f_par_all_stack_weighted"] = float((wall * fall).sum() / wall.sum())
P(f"  satellite fraction: ISO (W = 10) stack-weighted f_W {RES['f_W_iso_stack_weighted']:.3f}; ALL f_par {RES['f_par_all_stack_weighted']:.3f}")
RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, "cfg502_env_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg502_env.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
