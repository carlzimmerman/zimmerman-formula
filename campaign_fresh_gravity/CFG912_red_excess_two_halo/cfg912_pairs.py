#!/usr/bin/env python3
"""CFG912 stage B (criteria FROZEN_CRITERIA.md, 96de8091f): neighbour-pair histograms for one B21 mass bin, around the lenses
and around their random clones, in x = d / rho_l (rho_l = sqrt(G M_l / g_10)).  CFG903's pair loop (same pool, same cuts, same
chunking and order), plus:
  main   cell = (class9, lens-mass cell, x bin, neighbour M_b cell, less-massive flag, |dchi| bin), unmasked neighbours,
         weight W_l x c1w x M_b,j
  jk     (patch, colour3, lens-mass cell, coarse x, coarse M_b, flag) for I0, |dchi| < 500, unmasked (random half A as well)
  k0b    CFG903's v0 histogram (its cells and weights) for control K0b
No model, no kernel, no amplitude here.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -u cfg912_pairs.py BIN        (BIN = 1..4)
     CFG912_MUTATE=1 ... cfg912_pairs.py BIN    (MUTATE: injected red-only hosts at 0.4 Mpc, separate outputs)
     CFG912_MUTATE=B ... cfg912_pairs.py BIN    (MUTATE-B, AMENDMENT_A1.md: hosts at 0.01 Mpc)
Output (git-ignored): ../../../_external_data/cfg912_work/cfg912_hist_bin{BIN}[_MUTATE]_{lens,random}.npz ; log cfg912_pairs_bin{BIN}[_MUTATE].out
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, time
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg912_lib as C
L = C.L

BIN = int(sys.argv[1]); assert BIN in (1, 2, 3, 4)
MUT = C.MUT_MODE != ""; SFX = C.MUT_SFX                                # A1: CFG912_MUTATE=B -> MUTATE-B (d 0.01 Mpc)
L.start_watchdog(f"CFG912 pairs bin {BIN}{SFX}")
OUT = []
def P(s=""):
    s = f"[{time.time() - L.T0:7.1f} s, {L.cur_rss() / 1e6:5.0f} MB] {s}"; print(s, flush=True); OUT.append(s)

S = np.load(os.path.join(C.WORK903, "cfg903_stage.npz"))
CO = np.load(os.path.join(C.WORK, "cfg912_colour.npz"))
binall = S["L_bin"]
lb = np.where(binall == BIN - 1)[0]
NO = len(lb)
LZ = {k: S["L_" + k][lb] for k in ("ra", "dec", "z", "chi", "Mgal", "mlim", "fC1", "W_B21", "I0", "I1", "I5", "patch", "self_nb")}
RZ = dict(ra=S["R_ra"][lb], dec=S["R_dec"][lb], patch=S["R_patch"][lb])
col3 = CO["col3"][lb]; iso = CO["iso3"][lb]
NBx, NBchi, NBlb, NBls, NBm = S["NB_xyz"], S["NB_chi"], S["NB_logMb"], S["NB_logMs"], S["NB_masked"].astype(np.int64)
NBMb = 10 ** NBlb; NBmb = L.mbin_of(NBlb)
# MUTATE: every INJ_EVERY-th I0 red (u-r > 2.0) lens in global table order (all bins)
inj_all = np.where(S["L_I0"] & (CO["col3"] >= 1))[0][::C.INJ_EVERY]
inj_mask_all = np.zeros(len(binall), bool); inj_mask_all[inj_all] = True
INJ = inj_mask_all[lb] if MUT else np.zeros(NO, bool)
del S, CO
assert np.all(NBmb >= C.NM_OFF) and np.all(NBmb < C.NM_OFF + C.NNM)
P(f"bin {BIN}{SFX}: {NO:,} lenses (I0 {int(LZ['I0'].sum()):,}, I5 {NO:,}); neighbour pool {len(NBlb):,}; injected hosts {int(INJ.sum()):,}")
tree = cKDTree(NBx)
P("neighbour tree built")

W = LZ["W_B21"]; I0 = LZ["I0"]
OBJ0 = I0 * W                                                    # CFG903 v0 per-object factor (exact expression)
DA = LZ["chi"] / (1 + LZ["z"])
CHMAX = 2 * np.sin(L.D_MAX / DA / 2)
logMl = np.log10(LZ["Mgal"]); LMC = C.lm_of(logMl); RHO = C.rho_Mpc(LZ["Mgal"])
CLS = iso * 3 + col3
assert np.all((logMl >= C.LM_LO) & (logMl < C.LM_LO + C.NLM * C.LM_DL))
NNORM = np.bincount(CLS, weights=W * LZ["Mgal"], minlength=C.NCLS)          # sum W_l M_l per class (lenses = clones)

def run(sample):
    if sample == "lens":
        xyz = L.unitvec(LZ["ra"], LZ["dec"]); patch = LZ["patch"]; selfj = LZ["self_nb"]
    else:
        xyz = L.unitvec(RZ["ra"], RZ["dec"]); patch = RZ["patch"]; selfj = np.full(NO, -1, np.int64)
    H903 = np.zeros(L.NCELL)
    HM = np.zeros(int(np.prod(C.SHAPE_MAIN)))
    HJ = np.zeros(int(np.prod(C.SHAPE_JK)))
    HJA = np.zeros(int(np.prod(C.SHAPE_JK))) if sample == "random" else None
    halfA = (np.arange(NO) % 2 == 0)
    npair = 0; nover = 0; CH = 250
    for i0 in range(0, NO, CH):
        o = np.arange(i0, min(i0 + CH, NO))
        lists = tree.query_ball_point(xyz[o], r=CHMAX[o])
        cnt = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists))
        k = np.repeat(np.arange(len(o)), cnt)
        j = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=int(cnt.sum()))
        del lists
        ko = o[k]
        m = j != selfj[ko]
        dchi = np.abs(NBchi[j] - LZ["chi"][ko])
        m &= dchi < 1000.0
        k, j, ko, dchi = k[m], j[m], ko[m], dchi[m]
        ch = np.linalg.norm(NBx[j] - xyz[ko], axis=1)
        d = 2 * np.arcsin(np.minimum(ch / 2, 1.0)) * DA[ko]
        m = d < L.D_MAX
        j, ko, dchi, d = j[m], ko[m], dchi[m], d[m]
        # ---- K0b: CFG903's v0 histogram, verbatim cells and weights
        db = L.dbin_of(d); mb = NBmb[j]
        flag = (NBMb[j] < LZ["Mgal"][ko]).astype(np.int64)
        wb = np.searchsorted(L.WEDGES[:4], dchi, side="right")
        mk = NBm[j]
        cell = (((db * L.NM + mb) * 2 + flag) * L.NW + wb) * 2 + mk
        inwin = (NBls[j] >= LZ["mlim"][ko]) & (NBls[j] < LZ["mlim"][ko] + 0.5)
        c1w = 1.0 + LZ["fC1"][ko] * inwin
        Mb = NBMb[j]
        H903 += np.bincount(cell, weights=OBJ0[ko] * Mb * c1w, minlength=L.NCELL)
        npair += len(j)
        # ---- this lane: unmasked neighbours, x = d / rho_l
        u = mk == 0
        ko_, d_, dchi_, flag_, mb_, Mbw = ko[u], d[u], dchi[u], flag[u], mb[u], (W[ko] * c1w * Mb)[u]
        if sample == "lens" and MUT:
            ki = o[INJ[o]]                                            # injected hosts, seen only by their own lens
            if len(ki):
                Minj = 10 ** C.INJ_LOGMB
                ko_ = np.concatenate([ko_, ki]); d_ = np.concatenate([d_, np.full(len(ki), C.INJ_D)])
                dchi_ = np.concatenate([dchi_, np.zeros(len(ki))])
                flag_ = np.concatenate([flag_, (Minj < LZ["Mgal"][ki]).astype(np.int64)])
                mb_ = np.concatenate([mb_, np.full(len(ki), int(L.mbin_of(np.array([C.INJ_LOGMB]))[0]))])
                Mbw = np.concatenate([Mbw, W[ki] * 1.0 * Minj])          # c1w = 1 (log M* tag 7.5 < every m_lim)
        x = d_ / RHO[ko_]
        xb = C.xbin_of(x); nover += int((x >= C.X_EDGES[-1]).sum())
        nm = mb_ - C.NM_OFF
        w3 = np.searchsorted(C.WB_EDGES, dchi_, side="right")
        cm = ((((CLS[ko_] * C.NLM + LMC[ko_]) * C.NX + xb) * C.NNM + nm) * 2 + flag_) * C.NWB + w3
        np.add.at(HM, cm, Mbw)
        jm = I0[ko_] & (dchi_ < 500.0)
        cj = (((((patch[ko_[jm]] * 3 + col3[ko_[jm]]) * C.NLM + LMC[ko_[jm]]) * C.NXC + C.xc_of_xb(xb[jm])) * C.NNMC + nm[jm] // 4) * 2 + flag_[jm])
        np.add.at(HJ, cj, Mbw[jm])
        if HJA is not None:
            a = halfA[ko_[jm]]
            np.add.at(HJA, cj[a], Mbw[jm][a])
        if (i0 // CH) % 80 == 0:
            P(f"  {sample}: {i0 + len(o):,}/{NO:,} objects, {npair:,} pairs (all flags) kept")
    out = dict(H903=H903, HM=HM, HJ=HJ, npair=npair, nover=nover)
    # per-patch normalisations for the jackknife (I0, by colour3): sum W_l M_l
    out["NJ"] = np.bincount(patch * 3 + col3, weights=I0 * W * LZ["Mgal"], minlength=L.NPATCH * 3).reshape(L.NPATCH, 3)
    if HJA is not None:
        out["HJA"] = HJA
        out["NJA"] = np.bincount((patch * 3 + col3)[halfA], weights=(I0 * W * LZ["Mgal"])[halfA], minlength=L.NPATCH * 3).reshape(L.NPATCH, 3)
    P(f"  {sample}: done, {npair:,} pairs ({npair / NO:.0f} per object); x beyond the last edge: {nover}")
    return out

RES = dict(lane="CFG912", stage="B", bin=BIN, mutate=MUT, n_objects=int(NO), n_injected=int(INJ.sum()), nnorm=NNORM.tolist())
for sample in ("lens", "random"):
    R = run(sample)
    np.savez_compressed(os.path.join(C.WORK, f"cfg912_hist_bin{BIN}{SFX}_{sample}.npz"), NNORM=NNORM,
                        **{k: v for k, v in R.items() if isinstance(v, np.ndarray)})
    RES[f"pairs_{sample}"] = int(R["npair"]); RES[f"x_overflow_{sample}"] = int(R["nover"])
    del R
    P(f"  {sample} histograms saved")
RES.update(runtime_s=round(time.time() - L.T0, 1), peak_current_rss_MB=round(L.PEAK_CUR[0] / 1e6, 1))
json.dump(RES, open(os.path.join(C.HERE, f"cfg912_pairs_bin{BIN}{SFX}.json"), "w"), indent=1)
P(f"saved; runtime {time.time() - L.T0:.0f} s; peak current RSS {L.PEAK_CUR[0] / 1e6:.0f} MB")
open(os.path.join(C.HERE, f"cfg912_pairs_bin{BIN}{SFX}.out"), "w").write("\n".join(OUT) + "\n")
