#!/usr/bin/env python3
"""RF4 (criteria 5632124ef4): the sample's own clustering. Weighted KiDS-bright tracer counts around lenses, per-lens clones and plain randoms, per patch and mass bin, all and bright/faint tracers; and a null with tracer RA shifted.
    RF4 work files come from rf4_clones.py cat, SI3's frozen si3_cats.npz gives R.
    OMP_NUM_THREADS=1 nice -n 15 python3 rf4_counts.py <work_dir> <si3_work_dir>      RF4_MUTATE=1: every tracer's RA + 5 deg. RF4_K7=1: injection check only
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math, time, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
from itertools import chain
import numpy as np
from scipy.spatial import cKDTree
T0 = time.time(); HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB); DATA = os.path.join(REPO, "real_research", "data", "lensing_rar"); sys.path.insert(0, os.path.join(REB, "SI3_nested_isolation"))
from si3_hole import patch_edges, apply_patches, SAMPLES
MUT = os.environ.get("RF4_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""; K7 = os.environ.get("RF4_K7") == "1"
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
def P(s): print(f"[{time.time() - T0:7.0f} s, {rss():.2f} GB] {s}", flush=True)
OMN, HN = 0.2976016, 0.6856427; ZG = np.linspace(0, 1.5, 3001); EE = np.sqrt(OMN * (1 + ZG) ** 3 + 1 - OMN); CHI = np.r_[0, np.cumsum(0.5 * (1 / EE[1:] + 1 / EE[:-1]) * np.diff(ZG))] * 299792.458 / (100 * HN)
DA = lambda z: np.interp(z, ZG, CHI) / (1 + z)
EDG = np.r_[np.geomspace(0.03, 3.0, 21), np.geomspace(3.0, 15.0, 7)[1:]]; NR = len(EDG) - 1; WIN = 0.1
def uvec(ra, de): r, d = np.radians(ra), np.radians(de); return np.c_[np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)]
def counts(tree, zt, tcut, ra, de, z, wt, ix, rmax, chunk=4000, skip_self=None):
    """sum over centres of w x tracers per R bin. ix = (patch, massbin). Returns C (2, 50, 4, NR), W (50, 4)."""
    C = np.zeros((3, 50, 4, NR)); W = np.zeros((50, 4)); np.add.at(W, ix, wt); U = uvec(ra, de); nb = int(np.searchsorted(EDG, rmax * 1.0001))
    for i0 in range(0, len(ra), chunk):
        s = slice(i0, min(len(ra), i0 + chunk)); D = DA(z[s]); th = rmax / D; lists = tree.query_ball_point(U[s], r=2 * np.sin(th / 2)); n = len(lists)
        cnt = np.fromiter(map(len, lists), dtype=np.int64, count=n); js = np.fromiter(chain.from_iterable(lists), dtype=np.int64, count=int(cnt.sum())); k = np.repeat(np.arange(n), cnt)
        ok = np.abs(zt[js] - z[s][k]) <= WIN; js, k = js[ok], k[ok]; d = tree.data[js] - U[s][k]; ch2 = np.einsum("ij,ij->i", d, d); ok = ch2 > (1e-5) ** 2; js, k, ch2 = js[ok], k[ok], ch2[ok]
        R = 2 * np.arcsin(np.minimum(np.sqrt(ch2) / 2, 1.0)) * D[k]; rb = np.searchsorted(EDG, R, "right") - 1; ok = (rb >= 0) & (rb < nb); js, k, rb = js[ok], k[ok], rb[ok]
        pa, mb, ww = ix[0][s][k], ix[1][s][k], wt[s][k]; np.add.at(C[0], (pa, mb, rb), ww); f = tcut[js] == 1; np.add.at(C[1], (pa[f], mb[f], rb[f]), ww[f]); np.add.at(C[2], (pa[~f], mb[~f], rb[~f]), ww[~f])
    return C, W
from astropy.io import fits
if K7:
    # injection: Poisson tracers around mock centres at known E(R) = n0 (1 + A (R/1 Mpc)^-1.5)
    rng = np.random.default_rng(7); n0 = 3.0; A = 2.0; gr_ = np.arange(40) * 1.0; ctr = np.c_[170 + np.repeat(gr_, 10), -4.5 + np.tile(np.arange(10) * 1.0, 40)]; nc = len(ctr); zc = np.full(nc, 0.25); Dz = float(DA(0.25)); tra, tde = [], []
    for i in range(nc):
        for j in range(20):
            a = math.pi * (EDG[j + 1] ** 2 - EDG[j] ** 2); Rm = math.sqrt(EDG[j] * EDG[j + 1]); nn = rng.poisson(a * n0 * A * Rm ** -1.5)
            if nn:
                R_ = np.sqrt(rng.uniform(EDG[j] ** 2, EDG[j + 1] ** 2, nn)); ph = rng.uniform(0, 2 * np.pi, nn); tde.append(ctr[i, 1] + np.degrees(R_ * np.sin(ph) / Dz)); tra.append(ctr[i, 0] + np.degrees(R_ * np.cos(ph) / Dz) / np.cos(np.radians(ctr[i, 1])))
    tra, tde = np.concatenate(tra), np.concatenate(tde); tr = cKDTree(uvec(tra, tde)); C, W = counts(tr, np.full(len(tra), 0.25), np.ones(len(tra), int), ctr[:, 0], ctr[:, 1], zc, np.ones(nc), (np.zeros(nc, int), np.zeros(nc, int)), 3.0)
    ar = np.pi * (EDG[1:] ** 2 - EDG[:-1] ** 2); got = C[0].sum((0, 1))[:20] / nc / ar[:20]; ex = n0 * A * np.sqrt(EDG[:20] * EDG[1:21]) ** -1.5; d = float(abs((got[8:] * ar[8:20]).sum() / (ex[8:] * ar[8:20]).sum() - 1)); print(f"K7 injected counts recovered, 0.3-3 Mpc total: |ratio - 1| {d:.4f}, limit 0.02: {'PASS' if d < 0.02 else 'FAIL'}"); json.dump(dict(K7=d, ok=bool(d < 0.02)), open(os.path.join(HERE, "rf4_k7.json"), "w")); sys.exit(0 if d < 0.02 else 1)
WORK, SI3W = sys.argv[1:3]; OUTF = os.path.join(WORK, f"rf4_counts{TAG}.npz")
b = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data; tra = np.array(b["RAJ2000"], "f8"); tde = np.array(b["DECJ2000"], "f8"); tz = np.array(b["zphot_ANNz2"], "f8"); tm = np.array(b["MAG_AUTO_CALIB"], "f8"); ok = (np.array(b["masked"]) == 0) & np.isfinite(tz) & np.isfinite(tm); del b; tra, tde, tz, tm = tra[ok], tde[ok], tz[ok], tm[ok]; tcut = (tm < np.median(tm)).astype(int)
nz, ez = np.histogram(tz, bins=np.arange(0, 1.01, 0.02)); json.dump(dict(nz=nz.tolist(), ez=ez.tolist(), n=int(len(tz))), open(os.path.join(HERE, "rf4_tracer_nz.json"), "w"))
tree = cKDTree(uvec((tra + 5.0) % 360 if MUT else tra, tde)); P(f"{len(tra):,} tracers")
LN = np.load(os.path.join(DATA, "lr_lenses.npz")); lra, lde, lz, llm = (np.array(LN[k], "f8") for k in ("ra", "dec", "z", "logM")); E = patch_edges(lra, lde); LB = np.digitize(llm, [8.5, 10.3, 10.6, 10.8, 11.0001]) - 1; PA = apply_patches(lra, lde, E); WW = np.load(os.path.join(DATA, "cfg110_perlens.npz"))["WW"].sum(1); OKB = (LB >= 0) & (LB < 4)
cat = np.load(os.path.join(WORK, "rf4_cats.npz")); froz = np.load(os.path.join(SI3W, "si3_cats.npz")); res = {}
if os.path.exists(OUTF): res = dict(np.load(OUTF))
def save(): np.savez(OUTF + ".tmp.npz", **res); os.replace(OUTF + ".tmp.npz", OUTF)
FAR = ("S10", "S_strict", "S_x300")
for s in SAMPLES:
    li_i = cat[f"I_{s}_li"]; mem = np.unique(li_i); ic = np.arange(len(li_i)); ncl = len(li_i) // len(mem); keep = ic[(ic % ncl) < 4]; rmax = 15.0 if s in FAR else 3.0
    for name, ra, de, li, rm in (("L", lra[mem], lde[mem], mem, rmax), ("I", cat[f"I_{s}_ra"][keep], cat[f"I_{s}_dec"][keep], li_i[keep], 3.0), ("R", froz[f"R_{s}_ra"], froz[f"R_{s}_dec"], froz[f"R_{s}_li"], rmax)):
        key = f"{s}_{name}"
        if key + "_C" in res: continue
        C, W = counts(tree, tz, tcut, ra, de, lz[li], WW[li], (apply_patches(ra, de, E), LB[li]), rm); res[key + "_C"] = C; res[key + "_W"] = W; res[key + "_rm"] = np.array(rm); save(); P(f"{key}: {len(ra):,} centres, R to {rm} Mpc")
    if s == "S10" and not MUT and "S10_Lrot_C" not in res:
        C, W = counts(tree, tz, tcut, (lra[mem] + 5.0) % 360, lde[mem], lz[mem], WW[mem], (PA[mem], LB[mem]), 3.0); res["S10_Lrot_C"] = C; res["S10_Lrot_W"] = W; save(); P("rotated null done")
res["EDG"] = EDG; save(); P("done")
