#!/usr/bin/env python3
"""CFG502 PM cross-check (FROZEN_CRITERIA.md section 4; cacadd50d). S0 (LCDM-equivalent) z = 0 snapshots, 256^3 in 200 Mpc/h.

Peaks: local maxima (3x3x3, periodic) of the CIC density on the 256 mesh with rho/rho_bar > 20; M_ta = particle mass inside the radius
where the mean enclosed density falls to Delta_ta rho_bar (the run's JSON); overlapping peaks (closer than the larger r_ta) keep the
heavier.  Lenses: log M_ta >= 13.3 [Msun/h], bins 13.3-13.7, 13.7-14.3.  Neighbours for isolation: log M_ta >= 12.8.
DeltaSigma: all particles projected along z (full periodic box) on a 2048^2 CIC map; comoving annuli 0.3-10 Mpc/h.
Model (same machinery as the KiDS E, at z = 0, PM cosmology Om = 0.1424/h^2, sigma_8 0.811): Duffy NFW holding M_ta inside r_ta
(own, frozen beyond) + b_T10(M200c) x T2h(outside r_ta) + mean-density hole.
Tolerance: median PM / model over R in [1.5 r_ta, 8 Mpc/h] in [0.7, 1.3] per mass bin (all peaks).
Isolation emulation (reported): PHOTO-ISO (LOS displaced by N(0, sigma_chi), sigma_chi from cfg502_env_results.json at z = 0.25),
TRUE-ISO (sigma_chi = 0); veto: another peak with M_ta > 0.3 M_lens within 2.02 Mpc/h projected and |dchi| < 6.74 Mpc/h.
Output: cfg502_pm.out, cfg502_pm_results.json.   Run: nice -n 15 python3 cfg502_pm.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import math, json, time
import numpy as np
from scipy.ndimage import maximum_filter
from scipy.spatial import cKDTree
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg502_envlib as EL                                                   # noqa: E402
from colossus.cosmology import cosmology                                     # noqa: E402
from colossus.lss import bias as cbias                                       # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
RUNS = [("S0_s359", "cfg359_work/cfg359_S0_FLAT_canonical_N256"),
        ("S0_s360", "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed360"),
        ("S0_s361", "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed361")]
h = 0.6736; OMPM = (0.02237 + 0.1200) / h ** 2
PMC = cosmology.setCosmology("cfg502pm", params=dict(flat=True, H0=100 * h, Om0=OMPM, Ob0=0.02237 / h ** 2, sigma8=0.811, ns=0.965),
                             persistence="")
RHOM_H = OMPM * 2.77536627e11                                                # h^2 Msun / Mpc^3 = (Msun/h) / (Mpc/h)^3
T0 = time.time()
LOG = []
RES = {"lane": "CFG502", "script": "cfg502_pm", "runs": {}}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


ENVJ = json.load(open(os.path.join(HERE, "cfg502_env_results.json")))
SIGCHI = ENVJ["sigma_single_z025_Mpc"] * h                                   # Mpc/h comoving
P(f"photo-z emulation sigma_chi = {SIGCHI:.1f} Mpc/h (from cfg502_env_results.json)")
RB = np.geomspace(0.3, 10.0, 21); RC = np.sqrt(RB[1:] * RB[:-1])
NMAP = 2048


def cic3(pos, N, L):
    x = pos / (L / N); i0 = np.floor(x).astype(np.int64); d = x - i0
    rho = np.zeros(N ** 3)
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (d[:, 0] if dx else 1 - d[:, 0]) * (d[:, 1] if dy else 1 - d[:, 1]) * (d[:, 2] if dz else 1 - d[:, 2])
                idx = (((i0[:, 0] + dx) % N) * N + (i0[:, 1] + dy) % N) * N + (i0[:, 2] + dz) % N
                rho += np.bincount(idx, weights=w, minlength=N ** 3)
    return rho.reshape(N, N, N)


def cic2(xy, N, L):
    x = xy / (L / N); i0 = np.floor(x).astype(np.int64); d = x - i0
    m = np.zeros(N * N)
    for dx in (0, 1):
        for dy in (0, 1):
            w = (d[:, 0] if dx else 1 - d[:, 0]) * (d[:, 1] if dy else 1 - d[:, 1])
            m += np.bincount(((i0[:, 0] + dx) % N) * N + (i0[:, 1] + dy) % N, weights=w, minlength=N * N)
    return m.reshape(N, N)


def model_profile(Mta_h, rta_h):
    """physical-unit model at z = 0 for a peak (inputs Msun/h, Mpc/h); returns own and E on RC (h Msun/pc^2 comoving = z0 units)."""
    Mta = Mta_h / h; rta = rta_h / h; R = RC / h
    lM200 = brentq(lambda l: float(EL.LL.nfw(10 ** l, 0.0)[0](rta)) - Mta, math.log10(Mta) - 2, math.log10(Mta) + 0.5)
    M200 = 10 ** lM200
    Menc = EL.LL.nfw(M200, 0.0)[0]
    r = np.geomspace(1e-4, rta, 2000)
    own = EL.LL.dsigma(R, r, Menc(r))
    b = float(cbias.haloBias(M200 * h, z=0.0, mdef="200c", model="tinker10"))
    # T2h with the PM cosmology
    rr = np.geomspace(rta, 200.0, 2500); rm = np.sqrt(rr[1:] * rr[:-1])
    rho = OMPM * EL.RHOC0 * (h / EL.H) ** 2                                  # physical Msun/Mpc^3 at z = 0 with the PM Om, h
    xi = PMC.correlationFunction(rm * h, 0.0)
    M = np.concatenate([[0.0], np.cumsum(4 * math.pi * rm ** 2 * rho * xi * np.diff(rr))])
    t2 = EL.LL.dsigma(R, rr, M)
    rh = np.geomspace(1e-5, rta, 2000)
    hole = -EL.LL.dsigma(R, rh, 4 * math.pi / 3 * rh ** 3 * rho)
    conv = 1e-12 / h                                                         # Msun/Mpc^2 physical -> h Msun/pc^2
    return own * conv, (b * t2 + hole) * conv, b, M200


for name, base in RUNS:
    t = time.time()
    J = json.load(open(os.path.join(EXT, base + ".json")))
    L = float(J["L"]); N = int(J["mesh"]); Dta = float(J["snap"]["z0"]["Delta_ta"])
    pos = np.load(os.path.join(EXT, base + "_z0.npz"))["pos"].astype(np.float64) % L
    NP = len(pos); mp = RHOM_H * L ** 3 / NP
    rho = cic3(pos, N, L); rho /= rho.mean()
    pk = (rho == maximum_filter(rho, size=3, mode="wrap")) & (rho > 20.0)
    cand = (np.argwhere(pk) + 0.5) * (L / N)
    tree = cKDTree(pos, boxsize=L)
    rg = np.geomspace(0.15, 6.0, 80)
    cnt = np.array([[len(x) for x in tree.query_ball_point(cand, rr_, workers=4)] for rr_ in rg]).T   # (ncand, nr)
    dens = cnt * mp / (4 * math.pi / 3 * rg ** 3) / RHOM_H
    Mta = np.zeros(len(cand)); rta = np.zeros(len(cand))
    for i in range(len(cand)):
        above = dens[i] >= Dta
        if not above[0]:
            continue
        j = int(np.argmin(above)) if not above.all() else len(rg) - 1
        if j == 0:
            continue
        f = (math.log(dens[i, j - 1]) - math.log(Dta)) / (math.log(dens[i, j - 1]) - math.log(dens[i, j]))
        rta[i] = math.exp(math.log(rg[j - 1]) + f * (math.log(rg[j]) - math.log(rg[j - 1])))
        Mta[i] = Dta * RHOM_H * 4 * math.pi / 3 * rta[i] ** 3
    ok = Mta > 0
    cand, Mta, rta = cand[ok], Mta[ok], rta[ok]
    o = np.argsort(-Mta); cand, Mta, rta = cand[o], Mta[o], rta[o]
    keep = np.ones(len(cand), bool); tc = cKDTree(cand, boxsize=L)
    for i in range(len(cand)):
        if not keep[i]:
            continue
        for j in tc.query_ball_point(cand[i], rta[i]):
            if j > i:
                keep[j] = False
    cand, Mta, rta = cand[keep], Mta[keep], rta[keep]
    lM = np.log10(Mta)
    nb = lM >= 12.8
    P(f"\n[{name}] particles {NP:,}, m_p {mp:.3e} Msun/h, Delta_ta {Dta:.3f}; peaks (rho > 20, deduplicated) {len(cand)}; "
      f"log M_ta >= 12.8: {nb.sum()}, >= 13.3: {(lM >= 13.3).sum()} ({time.time() - t:.0f} s)")
    # isolation flags among neighbours (log M_ta >= 12.8)
    NBp = cand[nb]; NBm = Mta[nb]
    rng = np.random.default_rng(502 + int(name[-3:]))
    flags = {}
    for lab, sig in (("PHOTO", SIGCHI), ("TRUE", 0.0)):
        zph = (NBp[:, 2] + rng.normal(0, sig, len(NBp))) % L if sig > 0 else NBp[:, 2].copy()
        t2 = cKDTree(NBp[:, :2], boxsize=L)
        isof = np.ones(len(NBp), bool)
        for i in range(len(NBp)):
            for j in t2.query_ball_point(NBp[i, :2], 2.02):
                if j == i or NBm[j] <= 0.3 * NBm[i]:
                    continue
                dz = abs(zph[j] - zph[i]); dz = min(dz, L - dz)
                if dz < 6.74:
                    isof[i] = False; break
        flags[lab] = isof
    # projected map (comoving h Msun / pc^2)
    Smap = cic2(pos[:, :2], NMAP, L) * mp / (L / NMAP * 1e6) ** 2
    del tree, pos, rho
    pix = L / NMAP
    ny = int(math.ceil(RB[-1] / pix)) + 2
    gx = (np.arange(-ny, ny + 1) * pix)
    DX, DY = np.meshgrid(gx, gx, indexing="ij")
    Rpx = np.sqrt(DX ** 2 + DY ** 2)
    out = {}
    for b0, b1 in ((13.3, 13.7), (13.7, 14.3)):
        sel = np.where((lM[nb] >= b0) & (lM[nb] < b1))[0]
        if len(sel) == 0:
            continue
        prof = []
        for i in sel:
            cx, cy = NBp[i, 0] / pix - 0.5, NBp[i, 1] / pix - 0.5
            ix, iy = int(round(cx)), int(round(cy))
            sub = Smap[np.ix_(np.arange(ix - ny, ix + ny + 1) % NMAP, np.arange(iy - ny, iy + ny + 1) % NMAP)]
            rr_ = np.sqrt((DX + (ix - cx) * pix) ** 2 + (DY + (iy - cy) * pix) ** 2)
            o_ = np.argsort(rr_.ravel()); rs = rr_.ravel()[o_]; ss = sub.ravel()[o_]
            cum = np.cumsum(ss); n_ = np.arange(1, len(ss) + 1)
            mean_in = np.interp(RC, rs, cum / n_)
            ring = np.array([ss[(rs >= RB[k]) & (rs < RB[k + 1])].mean() for k in range(len(RC))])
            prof.append(mean_in - ring)
        prof = np.array(prof)
        Mm = float(np.median(NBm[sel])); rtm = (3 * Mm / (4 * math.pi * Dta * RHOM_H)) ** (1 / 3)
        own, Ein, b, M200 = model_profile(Mm, rtm)
        # model stacked over the actual peaks (each peak's own model), cheap: 25 quantile peaks
        qs = np.quantile(NBm[sel], np.linspace(0.02, 0.98, 25))
        mods = np.array([sum(model_profile(q, (3 * q / (4 * math.pi * Dta * RHOM_H)) ** (1 / 3))[:2]) for q in qs])
        mod = mods.mean(0)
        win = (RC >= 1.5 * rtm) & (RC <= 8.0)
        rec = dict(n=int(len(sel)), logM_ta_median=math.log10(Mm), r_ta_median=rtm, b_T10=b, R=RC.tolist(),
                   pm_all=prof.mean(0).tolist(), model=mod.tolist(), model_E=Ein.tolist(), model_own=own.tolist(),
                   ratio_all_window=float(np.median(prof.mean(0)[win] / mod[win])))
        for lab in ("PHOTO", "TRUE"):
            m_ = flags[lab][sel]
            rec[f"n_{lab}"] = int(m_.sum())
            if m_.sum() >= 5:
                pr = prof[m_].mean(0)
                rec[f"pm_{lab}"] = pr.tolist()
                ext = (RC >= 1.5 * rtm) & (RC <= 8.0)
                rec[f"ratio_{lab}_over_all_beyond_rta"] = float(np.median(pr[ext] / prof.mean(0)[ext]))
                rec[f"excess_{lab}_over_all_beyond_rta"] = float(np.median((pr[ext] - own[ext]) / (prof.mean(0)[ext] - own[ext])))
        out[f"{b0}-{b1}"] = rec
        P(f"  bin {b0}-{b1}: n {len(sel)} (PHOTO-ISO {rec['n_PHOTO']}, TRUE-ISO {rec['n_TRUE']}), median log M_ta {math.log10(Mm):.2f}, "
          f"r_ta {rtm:.2f} Mpc/h, b {b:.2f}")
        P("    R [Mpc/h]     : " + " ".join(f"{x:6.2f}" for x in RC))
        P("    PM all        : " + " ".join(f"{x:6.2f}" for x in prof.mean(0)))
        P("    model         : " + " ".join(f"{x:6.2f}" for x in mod))
        for lab in ("PHOTO", "TRUE"):
            if f"pm_{lab}" in rec:
                P(f"    PM {lab:5s}-ISO : " + " ".join(f"{x:6.2f}" for x in rec[f"pm_{lab}"]))
        P(f"    PM/model median over [1.5 r_ta, 8]: {rec['ratio_all_window']:.3f}; "
          + "; ".join(f"{lab}/ALL beyond r_ta {rec.get(f'ratio_{lab}_over_all_beyond_rta', float('nan')):.3f} "
                      f"(excess over own {rec.get(f'excess_{lab}_over_all_beyond_rta', float('nan')):.3f})" for lab in ("PHOTO", "TRUE")))
    RES["runs"][name] = out
    P(f"  ({time.time() - t:.0f} s)")

rat = {b: [RES["runs"][r][b]["ratio_all_window"] for r in RES["runs"] if b in RES["runs"][r]] for b in ("13.3-13.7", "13.7-14.3")}
RES["ratio_all_window_per_bin"] = rat
okb = all(0.7 <= float(np.median(v)) <= 1.3 for v in rat.values() if v)
RES["cross_check_pass"] = okb
RES["label_2h"] = None if okb else "2h NOT CROSS-CHECKED"
P(f"\nPM cross-check (median over runs of PM/model in [1.5 r_ta, 8 Mpc/h]): " +
  ", ".join(f"{b}: {np.median(v):.3f} ({', '.join(f'{x:.3f}' for x in v)})" for b, v in rat.items() if v) +
  f" -> {'PASS' if okb else 'FAIL: label 2h NOT CROSS-CHECKED'}")
P("512^3 S0 (cfg411 N512): not run (KD-tree mass assignment on 134M particles exceeds this lane's light-CPU budget); reported as not run.")
RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, "cfg502_pm_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg502_pm.out"), "w").write("\n".join(LOG) + "\n")
