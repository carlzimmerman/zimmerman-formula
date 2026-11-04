#!/usr/bin/env python3
"""FN4c POST-RESULT diagnostics (written after stage 1 read REBUILD MATCHES; no label changes; not in FROZEN_CRITERIA.md).

Why: stage 1's match rests on a flux-scale stand-in (+0.18 dex) for 93 % of isolated lenses, because MAG_GAAP_r is measured
for only 3.7 % of bright rows. This script asks how much of the match that stand-in carries.
  Q0  known answer: this script's copy of the machinery returns stage 1's primary N (255,052) exactly.
  Q1  V8: MAG_GAAP_r rebuilt for every row from LePhare's own output, m = MAG_ABS_r + DM(z) + K_COR_r + c, with LePhare's
      default cosmology (H0 70, Om 0.3, OL 0.7) and c = median(MAG_GAAP_r - m) over the matched rows. Measured rows keep
      their measured value. Rows with no valid MAG_ABS_r keep the stage-1 stand-in.
  Q2  constant flux scale for every row: 0.10, 0.15, 0.1823 (the matched median), 0.20, 0.25 dex.
  Q3  B21's mean masses without the 1e11 cut (B21: full sample 10.77, r < 17.5 sample 10.78).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -I fn4c_post.py -> fn4c_post.out / .json. kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys, time, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.spatial import cKDTree
from astropy.io import fits
from astropy.cosmology import LambdaCDM, FlatLambdaCDM

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
BRIGHT = os.path.join(REPO, "_external_data", "lam1_kids_bright_2026_11_03")
CACHE = os.path.join(HERE, "cache")
TARGET = 259383; OUT = []; R = {}; T0 = time.time()


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def tm(): return f"[{time.time() - T0:.0f} s, max RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB]"


b = fits.open(os.path.join(BRIGHT, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
L = fits.open(os.path.join(BRIGHT, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
assert np.array_equal(np.asarray(b["ID"]), np.asarray(L["ID"]))
ra = np.array(b["RAJ2000"], "f8"); dec = np.array(b["DECJ2000"], "f8"); rmag = np.array(b["MAG_AUTO_CALIB"], "f8")
z = np.array(b["zphot_ANNz2"], "f8"); masked = np.array(b["masked"], "i8"); mbest = np.array(L["MASS_BEST"], "f8")
mabs = np.array(L["MAG_ABS_r"], "f8"); kcor = np.array(L["K_COR_r"], "f8"); zlp = np.array(L["REDSHIFT"], "f8"); filt = np.array(L["MABS_FILTr"], "i8")
NROWS = len(z); del b, L

# stage 1's flux scale, rebuilt from its cache exactly as fn4c_rebuild.py does (P3a, P3b)
W = np.load(os.path.join(CACHE, "wl_match.npz"))
matched = np.isfinite(W["gaap"]) & (W["gaap"] < 90)
fs_match = np.where(matched, (W["gaap"] - rmag) / 2.5, np.nan)
bedges = np.arange(10.0, 20.5001, 0.25); bi = np.clip(np.digitize(rmag, bedges) - 1, 0, len(bedges) - 2)
gmed = float(np.median(fs_match[matched])); med = np.full(len(bedges) - 1, gmed)
for k_ in range(len(bedges) - 1):
    s_ = matched & (bi == k_)
    if s_.sum() >= 50: med[k_] = float(np.median(fs_match[s_]))
fs1 = np.where(matched, fs_match, med[bi])

COS = LambdaCDM(H0=70.0, Om0=0.2793, Ode0=0.7207)


def dc_astropy(zv):
    zu, inv = np.unique(zv, return_inverse=True)
    return COS.comoving_distance(zu).value[inv]


def unitv(ra_deg, dec_deg):
    r_ = np.radians(ra_deg); d_ = np.radians(dec_deg)
    return np.stack([np.cos(d_) * np.cos(r_), np.cos(d_) * np.sin(r_), np.sin(d_)], axis=-1)


U = unitv(ra, dec); EDGES = np.linspace(7.0, 13.0, 1001)


def thresholds(lmp):
    bb = np.searchsorted(EDGES, lmp, side="left") - 1; inr = (bb >= 0) & (bb < 1000)
    s = np.bincount(bb[inr], weights=10 ** lmp[inr], minlength=1000); c = np.bincount(bb[inr], minlength=1000)
    mean = np.where(c > 0, s / np.maximum(c, 1), np.nan); thr = np.full(len(lmp), np.nan); thr[inr] = np.log10(0.1 * mean[bb[inr]])
    return thr, inr


def isolate(X, lmp, lens, thr, inr, rad=3.0, chunk=20000):
    tree = cKDTree(X); iso = np.zeros(len(lens), bool)
    for i0 in range(0, len(lens), chunk):
        sl = lens[i0:i0 + chunk]; lists = tree.query_ball_point(X[sl], r=rad)
        cnt = np.fromiter((len(x) for x in lists), np.int64, len(lists)); k = np.repeat(np.arange(len(sl)), cnt)
        j = np.fromiter((q for x in lists for q in x), np.int64, int(cnt.sum())); i = sl[k]
        bad = (j != i) & (lmp[j] > thr[i]); flag = np.ones(len(sl), bool); flag[np.unique(k[bad])] = False; iso[i0:i0 + chunk] = flag
    return iso & inr[lens]


def rebuild(fs_arr, gl=0.056):
    lm = mbest + fs_arr; pool = np.isfinite(lm) & (z > 0) & (z < 0.5); ip = np.nonzero(pool)[0]; zp = z[ip]; lmp = lm[ip]
    X = U[ip] * (dc_astropy(zp) / (1 + zp))[:, None]; thr, inr = thresholds(lmp)
    cand = (masked[ip] == 0) & (zp > 0.1) & (zp < 0.5) & (lmp + gl >= 0) & (lmp + gl < 11.0); il = np.nonzero(cand)[0]
    iso = isolate(X, lmp, il, thr, inr)
    return int(iso.sum()), dict(ip=ip, il=il, iso=iso, lmp=lmp, zp=zp)


P("FN4c POST-RESULT diagnostics (no label changes). kappa = 1/2 FITTED; not theory closed.")
n0, st0 = rebuild(fs1)
q0 = n0 == 255052; R["Q0"] = dict(N=n0, stage1=255052, passed=q0)
P(f"Q0 this script's copy, stage-1 flux scale: N {n0:,} against stage 1's 255,052 -> {'PASS' if q0 else 'FAIL'} {tm()}")

# Q1: LePhare reconstruction
ok = np.isfinite(mabs) & (mabs > -40) & (mabs < 0) & (filt > 0) & (zlp > 0.002) & np.isfinite(kcor)
DM = np.full(NROWS, np.nan); DM[ok] = FlatLambdaCDM(H0=70.0, Om0=0.3).distmod(zlp[ok]).value
mrec = mabs + DM + kcor
cal = matched & ok; off = float(np.median(W["gaap"][cal] - mrec[cal])); mad = float(np.median(np.abs((W["gaap"][cal] - mrec[cal]) - off)))
fs_rec = (mrec + off - rmag) / 2.5
dfs = (fs_rec - fs_match)[cal]
fs8 = np.where(matched, fs_match, np.where(ok, fs_rec, fs1))
n8, st8 = rebuild(fs8)
fsb = fs_rec[ok & (rmag < 18)]; fsf = fs_rec[ok & (rmag >= 19.5)]
R["Q1"] = dict(offset_mag=off, mad_mag=mad, n_cal=int(cal.sum()), rows_rebuilt=int((ok & ~matched).sum()),
               fs_rec_minus_fs_measured=dict(median=float(np.median(dfs)), mad=float(np.median(np.abs(dfs - np.median(dfs))))),
               fs_rec_median_r_lt_18=float(np.median(fsb)), fs_rec_median_r_ge_19p5=float(np.median(fsf)),
               N=n8, deviation=round(n8 / TARGET - 1, 5))
P(f"Q1 LePhare-rebuilt MAG_GAAP_r: offset c = {off:+.4f} mag (MAD {mad:.4f}) on {cal.sum():,} matched rows; fs_rec - fs_measured median {np.median(dfs):+.4f} dex (MAD {R['Q1']['fs_rec_minus_fs_measured']['mad']:.4f})")
P(f"   rebuilt fs median: r < 18 {np.median(fsb):+.3f} dex, r >= 19.5 {np.median(fsf):+.3f} dex (stage-1 stand-in +{gmed:.3f})")
P(f"   V8 N = {n8:,} ({100 * (n8 / TARGET - 1):+.1f} % against 259,383) {tm()}")

# Q2: constant scan
R["Q2"] = {}
for c in (0.10, 0.15, 0.1823, 0.20, 0.25):
    n, _ = rebuild(np.full(NROWS, c)); R["Q2"][f"{c:.4f}"] = dict(N=n, deviation=round(n / TARGET - 1, 5))
    P(f"Q2 constant fs {c:+.4f} dex: N {n:,} ({100 * (n / TARGET - 1):+.1f} %) {tm()}")

# Q3: mean masses without the 1e11 cut (stage-1 flux scale, +0.056)
lm = mbest + fs1 + 0.056; base = (masked == 0) & (z > 0.1) & (z < 0.5) & np.isfinite(lm)
q3 = dict(all_no_cut=float(np.log10(np.mean(10 ** lm[base]))), bright_no_cut=float(np.log10(np.mean(10 ** lm[base & (rmag < 17.5)]))),
          all_no_cut_V8=float(np.log10(np.mean(10 ** (mbest + fs8 + 0.056)[base]))))
R["Q3"] = q3
P(f"Q3 log mean M* without the 1e11 cut: all {q3['all_no_cut']:.3f} (B21 10.77), r < 17.5 {q3['bright_no_cut']:.3f} (B21 10.78); V8 flux scale, all {q3['all_no_cut_V8']:.3f}")

# V8 inventory for an optional stage-2 regrade (post-result)
sel = st8["il"][st8["iso"]]
np.savez(os.path.join(CACHE, "fn4c_lenses_V8.npz"), z=st8["zp"][sel], logM=st8["lmp"][sel] + 0.056)
P(f"done {tm()}")
json.dump(R, open(os.path.join(HERE, "fn4c_post.json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, "fn4c_post.out"), "w").write("\n".join(OUT) + "\n")
