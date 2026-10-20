#!/usr/bin/env python3
"""CFG903 stage B (criteria FROZEN_CRITERIA.md bb665cf4f; completeness AMENDMENT_A1.md 26ecb00ce): neighbour-pair
histograms for one B21 mass bin, around the lenses and around their random clones.  No model, no chi2 here.
Histogram cell = (d bin, log M_b bin, less-massive-than-lens flag, |dchi| bin, masked flag), weight = per-object factor
x per-pair completeness weight x M_b,j.  Variants (per-object factor):
  v0 primary  I0 x W_B21 x C1'      v1 C0  I0 x W_B21           v2 C2'  I0 x W_B21 x R_C2'
  v3 uniform  I0 x 1 x C1'          v4 I1  I1 x W_B21 x C1'     v5 I2   I2 x W_B21 x C1'
  v6 I5       I5 x W_B21 x C1'      v7 (A1 diagnostic) I0 & z >= 0.17 x W_B21 x C1'
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -u cfg903_pairs.py BIN   (BIN = 1..4)    [CFG903_SUBSAMPLE=f optional fallback]
Output (git-ignored): ../../../_external_data/cfg903_work/cfg903_hist_bin{BIN}.npz ; log cfg903_pairs_bin{BIN}.out
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, time
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg903_lib as L

BIN = int(sys.argv[1]); assert BIN in (1, 2, 3, 4)
SUBF = float(os.environ.get("CFG903_SUBSAMPLE", "1.0"))
L.start_watchdog(f"CFG903 pairs bin {BIN}")
OUT = []
def P(s=""):
    s = f"[{time.time() - L.T0:7.1f} s, {L.cur_rss() / 1e6:5.0f} MB] {s}"; print(s, flush=True); OUT.append(s)

S = np.load(os.path.join(L.WORK, "cfg903_stage.npz"))
lb = np.where(S["L_bin"] == BIN - 1)[0]
if SUBF < 1.0:
    rng = np.random.default_rng(903); lb = np.sort(rng.choice(lb, int(round(SUBF * len(lb))), replace=False))
NO = len(lb)
LZ = {k: S["L_" + k][lb] for k in ("ra", "dec", "z", "chi", "Mgal", "mlim", "fC1", "RcC2", "W_B21", "I0", "I1", "I2", "I5", "patch", "self_nb")}
RZ = dict(ra=S["R_ra"][lb], dec=S["R_dec"][lb], patch=S["R_patch"][lb])
NBx, NBchi, NBlb, NBls, NBm = S["NB_xyz"], S["NB_chi"], S["NB_logMb"], S["NB_logMs"], S["NB_masked"].astype(np.int64)
NBMb = 10 ** NBlb; NBmb = L.mbin_of(NBlb)
del S
P(f"bin {BIN}: {NO:,} lenses (union I0 u I5; subsample fraction {SUBF}); I0 {int(LZ['I0'].sum()):,}, I5 {int(LZ['I5'].sum()):,}; neighbour pool {len(NBlb):,}")
tree = cKDTree(NBx)
P("neighbour tree built")

W = LZ["W_B21"]; I0, I1, I2, I5 = LZ["I0"], LZ["I1"], LZ["I2"], LZ["I5"]; z17 = LZ["z"] >= 0.17
# per-object factor and whether the C1' faint-end weight applies
OBJ = [(I0 * W, "C1"), (I0 * W, "C0"), (I0 * W * LZ["RcC2"], "C0"), (I0 * 1.0, "C1"),
       (I1 * W, "C1"), (I2 * W, "C1"), (I5 * W, "C1"), ((I0 & z17) * W, "C1")]
NORM = np.array([float((I0 * W).sum()), float((I0 * W).sum()), float((I0 * W).sum()), float(I0.sum()),
                 float((I1 * W).sum()), float((I2 * W).sum()), float((I5 * W).sum()), float(((I0 & z17) * W).sum())])
NV = len(OBJ)
DA = LZ["chi"] / (1 + LZ["z"])
CHMAX = 2 * np.sin(L.D_MAX / DA / 2)

def run(sample):
    if sample == "lens":
        xyz = L.unitvec(LZ["ra"], LZ["dec"]); patch = LZ["patch"]; selfj = LZ["self_nb"]
    else:
        xyz = L.unitvec(RZ["ra"], RZ["dec"]); patch = RZ["patch"]; selfj = np.full(NO, -1, np.int64)
    H = np.zeros((NV, L.NCELL)); HJ = np.zeros(L.NPATCH * L.NCELL_JK)
    HA = np.zeros(L.NCELL) if sample == "random" else None
    HJA = np.zeros(L.NPATCH * L.NCELL_JK) if sample == "random" else None
    halfA = (np.arange(NO) % 2 == 0)
    npair = 0; CH = 250
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
        db = L.dbin_of(d); mb = NBmb[j]
        flag = (NBMb[j] < LZ["Mgal"][ko]).astype(np.int64)
        wb = np.searchsorted(L.WEDGES[:4], dchi, side="right")
        mk = NBm[j]
        cell = (((db * L.NM + mb) * 2 + flag) * L.NW + wb) * 2 + mk
        inwin = (NBls[j] >= LZ["mlim"][ko]) & (NBls[j] < LZ["mlim"][ko] + 0.5)
        c1w = 1.0 + LZ["fC1"][ko] * inwin
        Mb = NBMb[j]
        for v, (fac, cm) in enumerate(OBJ):
            w = fac[ko] * Mb * (c1w if cm == "C1" else 1.0)
            H[v] += np.bincount(cell, weights=w, minlength=L.NCELL)
        jm = (wb <= 3) & (mk == 0)
        cj = patch[ko[jm]] * L.NCELL_JK + (db[jm] * L.NM + mb[jm]) * 2 + flag[jm]
        w0 = (OBJ[0][0][ko] * Mb * c1w)[jm]
        HJ += np.bincount(cj, weights=w0, minlength=L.NPATCH * L.NCELL_JK)
        if HA is not None:
            a = halfA[ko]
            HA += np.bincount(cell[a], weights=(OBJ[0][0][ko] * Mb * c1w)[a], minlength=L.NCELL)
            aj = a[jm]
            HJA += np.bincount(cj[aj], weights=w0[aj], minlength=L.NPATCH * L.NCELL_JK)
        npair += len(j)
        if (i0 // CH) % 80 == 0:
            P(f"  {sample}: {i0 + len(o):,}/{NO:,} objects, {npair:,} pairs kept")
    # per-patch normalisations (v0) and A-half normalisations
    NJ = np.bincount(patch, weights=OBJ[0][0], minlength=L.NPATCH).astype(float)
    out = dict(H=H, HJ=HJ.reshape(L.NPATCH, L.NCELL_JK), NJ=NJ, npair=npair)
    if HA is not None:
        out.update(HA=HA, HJA=HJA.reshape(L.NPATCH, L.NCELL_JK), NA=float((OBJ[0][0] * halfA).sum()),
                   NJA=np.bincount(patch[halfA], weights=OBJ[0][0][halfA], minlength=L.NPATCH).astype(float))
    P(f"  {sample}: done, {npair:,} pairs kept ({npair / NO:.0f} per object)")
    return out

RL = run("lens"); RR = run("random")
np.savez_compressed(os.path.join(L.WORK, f"cfg903_hist_bin{BIN}.npz"),
                    HL=RL["H"], HJL=RL["HJ"], NJL=RL["NJ"], HR=RR["H"], HJR=RR["HJ"], NJR=RR["NJ"],
                    HA=RR["HA"], HJA=RR["HJA"], NA=RR["NA"], NJA=RR["NJA"], NORM=NORM, NO=NO, SUBF=SUBF)
RES = dict(lane="CFG903", stage="B", bin=BIN, n_objects=int(NO), subsample=SUBF, pairs_lens=int(RL["npair"]), pairs_random=int(RR["npair"]),
           norm=NORM.tolist(), variants=L.VARIANTS, runtime_s=round(time.time() - L.T0, 1), peak_current_rss_MB=round(L.PEAK_CUR[0] / 1e6, 1))
json.dump(RES, open(os.path.join(L.HERE, f"cfg903_pairs_bin{BIN}.json"), "w"), indent=1)
P(f"saved; runtime {time.time() - L.T0:.0f} s; peak current RSS {L.PEAK_CUR[0] / 1e6:.0f} MB")
open(os.path.join(L.HERE, f"cfg903_pairs_bin{BIN}.out"), "w").write("\n".join(OUT) + "\n")
