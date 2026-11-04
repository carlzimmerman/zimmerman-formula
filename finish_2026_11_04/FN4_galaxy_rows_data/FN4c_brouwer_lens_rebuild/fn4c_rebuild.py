#!/usr/bin/env python3
"""FN4c stage 1: rebuild Brouwer+21's isolated KiDS-bright lenses (target 259,383) with the authors' own conventions.

Criteria: FROZEN_CRITERIA.md (commit d62a6b6b53), committed alone before this script.
Recipe P1-P7 is the authors' public code (github.com/margotbrouwer/EG_project @ 4cc0a57826), re-implemented here:
  isolated_lens_selection.py  -> pool = finite logM & 0<z<0.5 (no mask cut); binned 0.1 mass ratio; D_A = D_C/(1+z); 3D distance
  modules_EG.import_kidscat   -> logM = MASS_BEST + (MAG_GAAP_r - MAG_AUTO_CALIB)/2.5
  mass_range_selection.py     -> lens mask: R_iso > 3 & masked == 0 & 0.1 < z < 0.5
  create_weightcat.py, configs/run_shearcode.py -> mass cut on logM + 0.056 ('GL') < 11
MAG_GAAP_r is not in the public bright files; it is read from the KiDS-1000 SOM-gold shear catalogue on disk (stand-in S1/S2).
K5 copies NV2's step-0 lines (rebuild_2026_10_22/NV2_external_field_xcop_lenses/nv2_e1.py, mode_lenses) to reproduce its count.

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 -I fn4c_rebuild.py          -> fn4c_rebuild.out / .json
      FN4C_MUTATE=1 (same command)                                     -> fn4c_rebuild_MUTATE.out / .json (z shuffled in the pool)
kappa = 1/2 FITTED; not theory closed.
"""
import hashlib, json, math, os, resource, sys, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.spatial import cKDTree
from astropy.io import fits
from astropy.cosmology import LambdaCDM

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
BRIGHT = os.path.join(REPO, "_external_data", "lam1_kids_bright_2026_11_03")
WLCAT = os.path.join(os.path.dirname(REPO), "_external_data", "kids_lensing_zsplit", "KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits")
CACHE = os.path.join(HERE, "cache"); os.makedirs(CACHE, exist_ok=True)
MUT = os.environ.get("FN4C_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
SHA = {"KiDS_DR4_brightsample.fits": "8baab69942bcb8f20cbff445107cd6e84b3efc3b6edd4ad64bdf3a349fa36fd6",
       "KiDS_DR4_brightsample_LePhare.fits": "36e35e31a31f8a1c3c88de8a26dee824424adf74a09f7cc0db659848e89b4ca1"}
NROWS = 1239422
TARGET = 259383
OUT = []; R = {}; T0 = time.time()


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def tm():
    return f"[{time.time() - T0:.0f} s, max RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB]"


# ------------------------------------------------------------------ K1: catalogue identity
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 24), b""):
            h.update(blk)
    return h.hexdigest()


P(f"FN4c stage 1{' MUTATE (z shuffled among pool rows)' if MUT else ''}. kappa = 1/2 FITTED; not theory closed.")
k1 = {n: sha256(os.path.join(BRIGHT, n)) == s for n, s in SHA.items()}
b = fits.open(os.path.join(BRIGHT, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
L = fits.open(os.path.join(BRIGHT, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
ids_equal = bool(np.array_equal(np.asarray(b["ID"]), np.asarray(L["ID"])))
K1 = all(k1.values()) and ids_equal and len(b) == NROWS and len(L) == NROWS
R["K1"] = dict(sha256_ok=k1, rows=len(b), ids_equal=ids_equal, passed=K1)
P(f"K1 catalogue: sha256 {k1}, rows {len(b)}, ID equal {ids_equal} -> {'PASS' if K1 else 'FAIL'}")
ra = np.array(b["RAJ2000"], "f8"); dec = np.array(b["DECJ2000"], "f8")
rmag = np.array(b["MAG_AUTO_CALIB"], "f8"); z = np.array(b["zphot_ANNz2"], "f8"); masked = np.array(b["masked"], "i8")
mbest = np.array(L["MASS_BEST"], "f8")
del b, L


def unitv(ra_deg, dec_deg):
    r_ = np.radians(ra_deg); d_ = np.radians(dec_deg)
    return np.stack([np.cos(d_) * np.cos(r_), np.cos(d_) * np.sin(r_), np.sin(d_)], axis=-1)


U = unitv(ra, dec)

# ------------------------------------------------------------------ P3a: MAG_GAAP_r from the shear catalogue (chunked raw reads)
MATCH = os.path.join(CACHE, "wl_match.npz")


def wl_match():
    st = os.stat(WLCAT); key = f"{st.st_size}"
    if os.path.exists(MATCH):
        d = np.load(MATCH)
        if str(d["key"]) == key:
            return d
    # header only: touching h[1].data pulled the whole 17.7 GB file into memory in the first run (25 GB RSS, disclosed)
    with fits.open(WLCAT, memmap=True, lazy_load_hdus=True) as h:
        off = h.fileinfo(1)["datLoc"]; n = int(h[1].header["NAXIS2"]); rowlen = int(h[1].header["NAXIS1"])
        dt = h[1].columns.dtype.newbyteorder(">")   # FITS is big-endian; columns.dtype is native-endian
        for c in ("RAJ2000", "DECJ2000", "MAG_GAAP_r", "MAG_AUTO", "EXTINCTION_r"):
            i = h[1].columns.names.index(c) + 1
            assert f"TSCAL{i}" not in h[1].header and f"TZERO{i}" not in h[1].header, c
    assert dt.itemsize == rowlen, (dt.itemsize, rowlen)
    tree = cKDTree(U); tol = 2 * math.sin(math.radians(1.0 / 3600) / 2)
    best_sep = np.full(NROWS, np.inf); gaap = np.full(NROWS, np.nan); mauto = np.full(NROWS, np.nan); ext = np.full(NROWS, np.nan)
    CH = 200000; nread = 0; nbright = 0
    with open(WLCAT, "rb") as f:
        f.seek(off)
        for i0 in range(0, n, CH):
            m = min(CH, n - i0); buf = f.read(m * rowlen); arr = np.frombuffer(buf, dtype=dt, count=m)
            ma = arr["MAG_AUTO"].astype("f8"); keep = np.isfinite(ma) & (ma < 21.0)
            nread += m
            if keep.any():
                rr = arr["RAJ2000"][keep].astype("f8"); dd = arr["DECJ2000"][keep].astype("f8")
                g = arr["MAG_GAAP_r"][keep].astype("f8"); e = arr["EXTINCTION_r"][keep].astype("f8"); a = ma[keep]
                dist, j = tree.query(unitv(rr, dd), k=1, distance_upper_bound=tol)
                ok = np.isfinite(dist)
                for q in np.nonzero(ok)[0]:        # keep the nearest WL row for each bright row
                    jj = j[q]
                    if dist[q] < best_sep[jj]:
                        best_sep[jj] = dist[q]; gaap[jj] = g[q]; mauto[jj] = a[q]; ext[jj] = e[q]
                nbright += int(keep.sum())
            del buf, arr
            if (i0 // CH) % 20 == 0:
                P(f"  WL rows read {nread:,} / {n:,}; bright (MAG_AUTO<21) {nbright:,} {tm()}")
    sep_as = np.where(np.isfinite(best_sep), np.degrees(2 * np.arcsin(np.clip(best_sep, 0, 2) / 2)) * 3600, np.nan)
    np.savez(MATCH, key=key, gaap=gaap, mauto=mauto, ext=ext, sep=sep_as, nread=nread, nbright=nbright)
    return np.load(MATCH)


W = wl_match()
matched = np.isfinite(W["gaap"]) & (W["gaap"] < 90)
fs_match = np.where(matched, (W["gaap"] - rmag) / 2.5, np.nan)
dm = np.abs(rmag - (W["mauto"] - W["ext"]))[matched]
K4v = float(np.median(dm)); K4 = K4v <= 0.10
R["K4"] = dict(matched=int(matched.sum()), matched_frac=float(matched.mean()), median_abs_dmag=K4v,
               p90_abs_dmag=float(np.percentile(dm, 90)), median_sep_arcsec=float(np.nanmedian(W["sep"][matched])), passed=bool(K4))
P(f"P3a match: {matched.sum():,} of {NROWS:,} bright rows ({100 * matched.mean():.1f} %) within 1\"; median sep {R['K4']['median_sep_arcsec']:.3f}\"")
P(f"K4 match quality: median |MAG_AUTO_CALIB - (MAG_AUTO - EXTINCTION_r)| = {K4v:.4f} mag (90th pct {R['K4']['p90_abs_dmag']:.3f}); line 0.10 -> {'PASS' if K4 else 'FAIL'}")
# P3b stand-in for unmatched rows: median fs of matched rows per 0.25-mag MAG_AUTO_CALIB bin (global median if < 50 matched)
bedges = np.arange(10.0, 20.5001, 0.25); bi = np.clip(np.digitize(rmag, bedges) - 1, 0, len(bedges) - 2)
gmed = float(np.median(fs_match[matched])); med = np.full(len(bedges) - 1, gmed); nper = np.zeros(len(bedges) - 1, int)
for k_ in range(len(bedges) - 1):
    s_ = matched & (bi == k_); nper[k_] = int(s_.sum())
    if nper[k_] >= 50: med[k_] = float(np.median(fs_match[s_]))
fs = np.where(matched, fs_match, med[bi])
R["fs"] = dict(global_median_matched=gmed, p16_p84_matched=[float(np.percentile(fs_match[matched], 16)), float(np.percentile(fs_match[matched], 84))],
               bins_with_own_median=int((nper >= 50).sum()), n_bins=len(nper))
P(f"fluxscale fs = (MAG_GAAP_r - MAG_AUTO_CALIB)/2.5 on matched rows: median {gmed:+.4f} dex, 16-84 % [{R['fs']['p16_p84_matched'][0]:+.3f}, {R['fs']['p16_p84_matched'][1]:+.3f}]; stand-in bins with >= 50 matched: {R['fs']['bins_with_own_median']} of {len(nper)}")

# ------------------------------------------------------------------ P5 distances and K2
COS = LambdaCDM(H0=70.0, Om0=0.2793, Ode0=0.7207)


def dc_astropy(zv):
    zu, inv = np.unique(zv, return_inverse=True)
    return COS.comoving_distance(zu).value[inv]


def dc_trap(zq, om=0.2793, n=2_000_001):
    zz = np.linspace(0, max(zq), n); E = np.sqrt(om * (1 + zz) ** 3 + (1 - om))
    ch = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * 299792.458 / 70.0
    return np.interp(zq, zz, ch)


zt = np.array([0.05, 0.1, 0.25, 0.5]); a_ = dc_astropy(zt) / (1 + zt); t_ = dc_trap(zt) / (1 + zt)
K2v = float(np.max(np.abs(a_ / t_ - 1))); K2 = K2v <= 1e-6
R["K2"] = dict(z=zt.tolist(), DA_astropy=a_.tolist(), max_rel_dev=K2v, passed=bool(K2))
P(f"K2 distance: D_A(0.05, 0.1, 0.25, 0.5) = {np.round(a_, 3).tolist()} Mpc; astropy vs trapezoid max rel dev {K2v:.1e} -> {'PASS' if K2 else 'FAIL'}")

# ------------------------------------------------------------------ isolation machinery
EDGES = np.linspace(7.0, 13.0, 1001)


def thresholds(logm_pool, binned=True):
    """per pool row: log10 of the 'too heavy' limit (authors: 0.1 x mean M of the row's 0.006-dex bin, bins (lo, hi])."""
    if not binned:
        return logm_pool - 1.0, np.ones(len(logm_pool), bool)
    bb = np.searchsorted(EDGES, logm_pool, side="left") - 1
    inr = (bb >= 0) & (bb < 1000)
    s = np.bincount(bb[inr], weights=10 ** logm_pool[inr], minlength=1000); c = np.bincount(bb[inr], minlength=1000)
    mean = np.where(c > 0, s / np.maximum(c, 1), np.nan)
    thr = np.full(len(logm_pool), np.nan); thr[inr] = np.log10(0.1 * mean[bb[inr]])
    return thr, inr


def isolate(X, logm_pool, lens, thr, inr, rad=3.0, chunk=20000):
    """X (N,3) pool positions; lens: pool indices to test. Isolated = no pool row j != i with logm_j > thr_i within rad."""
    tree = cKDTree(X); iso = np.zeros(len(lens), bool); ok_l = inr[lens]
    for i0 in range(0, len(lens), chunk):
        sl = lens[i0:i0 + chunk]
        lists = tree.query_ball_point(X[sl], r=rad)
        cnt = np.fromiter((len(x) for x in lists), np.int64, len(lists))
        k = np.repeat(np.arange(len(sl)), cnt); j = np.fromiter((q for x in lists for q in x), np.int64, int(cnt.sum())); i = sl[k]
        bad = (j != i) & (logm_pool[j] > thr[i])
        flag = np.ones(len(sl), bool); flag[np.unique(k[bad])] = False
        iso[i0:i0 + chunk] = flag
    return iso & ok_l


# ------------------------------------------------------------------ K3 planted isolation
def k3():
    rng = np.random.default_rng(7); rows = []; truth = []; lens_ix = []
    centres = [(30 + 7 * (q % 20), -20 + 7 * (q // 20)) for q in range(60)]
    Da = 800.0; cases = [(2.95, 0.095), (2.95, 0.105), (3.05, 0.095), (3.05, 0.105)]
    for q, (ra0, de0) in enumerate(centres[:40]):
        dist, ratio = cases[q % 4]
        lm = 7.003 + 0.006 * (100 + 13 * q)          # bin centre, each lens in its own bin
        x0 = unitv(np.array([ra0]), np.array([de0]))[0] * Da
        rows.append((x0, lm)); lens_ix.append(len(rows) - 1); truth.append(not (dist <= 3.0 and ratio > 0.1))
        rows.append((x0 + np.array([0, 0, dist]), lm + math.log10(ratio)))
    for q in range(40, 42):                              # exact duplicate -> not isolated
        ra0, de0 = centres[q]; x0 = unitv(np.array([ra0]), np.array([de0]))[0] * Da; lm = 7.003 + 0.006 * (700 + q)
        rows.append((x0, lm)); lens_ix.append(len(rows) - 1); truth.append(False); rows.append((x0.copy(), lm))
    ra0, de0 = centres[45]; x0 = unitv(np.array([ra0]), np.array([de0]))[0] * Da   # outside (7, 13] -> not isolated
    rows.append((x0, 6.9)); lens_ix.append(len(rows) - 1); truth.append(False)
    X = np.array([r_[0] for r_ in rows]); lm = np.array([r_[1] for r_ in rows]); lens_ix = np.array(lens_ix)
    thr, inr = thresholds(lm); got = isolate(X, lm, lens_ix, thr, inr)
    return bool(np.array_equal(got, np.array(truth))), int(np.sum(got == np.array(truth))), len(truth)


k3ok, k3n, k3t = k3(); R["K3"] = dict(correct=k3n, total=k3t, passed=k3ok)
P(f"K3 planted isolation: {k3n} of {k3t} classified as planted -> {'PASS' if k3ok else 'FAIL'}")


# ------------------------------------------------------------------ K5: NV2's step 0, its own lines (copied)
def k5():
    CK = 299792.458
    _zg = np.linspace(0, 1.5, 30001); _E = np.sqrt(0.3 * (1 + _zg) ** 3 + 0.7); _CH = np.concatenate([[0], np.cumsum(0.5 * (1 / _E[1:] + 1 / _E[:-1]) * np.diff(_zg))])
    def DC(zq, h0): return np.interp(zq, _zg, _CH) * CK / h0
    K = dict(r=rmag, z=z, masked=masked, lm=mbest + 0.15 + 0.056)
    pool = (K["masked"] == 0) & (K["r"] < 20) & np.isfinite(K["lm"]) & np.isfinite(K["z"]) & (K["z"] > 0) & (K["lm"] > 0)
    ip = np.nonzero(pool)[0]; zz = K["z"][ip]; lm = K["lm"][ip]; u = U[ip]; chi70 = DC(zz, 70.0)
    lens = (zz > 0.1) & (zz < 0.5) & (lm < 11.0); il = np.nonzero(lens)[0]
    tree = cKDTree(u); iso = np.ones(len(il), bool); CH = 4000
    for i0 in range(0, len(il), CH):
        sl = il[i0:i0 + CH]; lists = tree.query_ball_point(u[sl], r=2 * np.sin(0.5 * 3.0 / chi70[sl]))
        k = np.repeat(np.arange(len(sl)), [len(x) for x in lists]); j = np.fromiter((q for x in lists for q in x), np.int64, int(sum(len(x) for x in lists))); i = sl[k]
        m = (j != i) & (lm[j] > lm[i] - 1.0); k, i, j = k[m], i[m], j[m]
        ang = np.arccos(np.clip((u[i] * u[j]).sum(1), -1, 1)); Rp = chi70[i] * ang; r3 = np.sqrt(Rp ** 2 + (chi70[i] - chi70[j]) ** 2)
        iso[i0 + np.unique(k[r3 < 3.0])] = False
    return int(len(ip)), int(len(il)), int(iso.sum())


k5p, k5c, k5n = k5(); K5 = (k5p, k5c, k5n) == (1000207, 773192, 486584)
R["K5"] = dict(pool=k5p, candidates=k5c, isolated=k5n, record=[1000207, 773192, 486584], passed=bool(K5))
P(f"K5 NV2 reproduction: pool {k5p:,}, candidates {k5c:,}, isolated {k5n:,} against NV2's 1,000,207 / 773,192 / 486,584 -> {'PASS' if K5 else 'FAIL'} {tm()}")


# ------------------------------------------------------------------ the rebuild (primary and variants)
def rebuild(name, fs_arr, pool_mask_cut=False, dist="DA", gl=0.056, binned=True, lens_need_match=False, zarr=None):
    zz_all = z if zarr is None else zarr
    lm_all = mbest + fs_arr
    pool = np.isfinite(lm_all) & (zz_all > 0) & (zz_all < 0.5)
    if pool_mask_cut: pool &= (masked == 0)
    ip = np.nonzero(pool)[0]; zp = zz_all[ip]; lmp = lm_all[ip]
    D = dc_astropy(zp); D = D / (1 + zp) if dist == "DA" else D
    X = U[ip] * D[:, None]
    thr, inr = thresholds(lmp, binned)
    cand = (masked[ip] == 0) & (zp > 0.1) & (zp < 0.5) & (lmp + gl >= 0) & (lmp + gl < 11.0)
    if lens_need_match: cand &= matched[ip]
    il = np.nonzero(cand)[0]
    iso = isolate(X, lmp, il, thr, inr)
    N = int(iso.sum()); dev = N / TARGET - 1
    lmgl = lmp[il] + gl; bins = np.digitize(lmgl, [8.5, 10.3, 10.6, 10.8, 11.0]) - 1
    out = dict(pool=int(len(ip)), candidates=int(len(il)), isolated=N, deviation=round(dev, 5), fraction=round(N / len(il), 5),
               per_bin_8p5_11=[int(((bins == q) & iso).sum()) for q in range(4)], below_8p5=int(((bins < 0) & iso).sum()))
    P(f"{name:<34s} pool {len(ip):>9,}  candidates {len(il):>8,}  isolated {N:>8,}  ({100 * N / len(il):5.1f} %)  vs 259,383: {100 * dev:+6.1f} % {tm()}")
    return out, (ip, il, iso, lmp, zp)


P("")
P("Rebuild (P1-P7), counts:")
zuse = None
if MUT:
    rng = np.random.default_rng(20261104); zuse = z.copy(); pidx = np.nonzero(np.isfinite(mbest + fs) & (z > 0) & (z < 0.5))[0]
    zuse[pidx] = rng.permutation(z[pidx])
prim, (ip, il, iso, lmp, zp) = rebuild("PRIMARY", fs, zarr=zuse)
R["primary"] = prim
N = prim["isolated"]; match = abs(N / TARGET - 1) <= 0.05
checks_ok = bool(K1 and K2 and k3ok and K4 and K5)
label = "NOT EVALUABLE" if not checks_ok else ("REBUILD MATCHES" if match else "REBUILD DOES NOT MATCH")
R["label"] = label

if not MUT:
    P("")
    P("Variants (diagnostic, frozen list; never replace the primary):")
    V = {}
    V["V1 fs = 0"], _ = rebuild("V1 fs = 0 (MASS_BEST only)", np.zeros(NROWS))
    V["V2 fs = +0.15"], _ = rebuild("V2 fs = +0.15 (NV2 stand-in)", np.full(NROWS, 0.15))
    V["V3 pool masked==0"], _ = rebuild("V3 pool masked == 0", fs, pool_mask_cut=True)
    V["V4 comoving"], _ = rebuild("V4 comoving D_C", fs, dist="DC")
    V["V5 no +0.056"], _ = rebuild("V5 mass cut without +0.056", fs, gl=0.0)
    V["V6 unbinned"], _ = rebuild("V6 unbinned 0.1 ratio", fs, binned=False)
    V["V7 lenses matched only"], _ = rebuild("V7 lenses need a P3a match", fs, lens_need_match=True)
    R["variants"] = V
    closest = min(V, key=lambda k_: abs(V[k_]["deviation"]))
    R["closest_variant"] = closest

    # secondary comparisons with B21 Appendix A (reported, no line)
    rl = rmag[ip]; cand = np.zeros(len(ip), bool); cand[il] = True; isoall = np.zeros(len(ip), bool); isoall[il[iso]] = True
    lmgl = lmp + 0.056
    def frac(mask_): return float(isoall[mask_].sum() / max(mask_.sum(), 1))
    poolz = (zp > 0.1) & (zp < 0.5) & (masked[ip] == 0)
    sec = dict(
        frac_bright_candidates=frac(cand & (rl < 17.5)), frac_faint_candidates=frac(cand & (rl >= 17.5)),
        frac_bright_poolz=frac(poolz & (rl < 17.5)), frac_faint_poolz=frac(poolz & (rl >= 17.5)),
        n_isolated_bright=int((isoall & (rl < 17.5)).sum()),
        logmean_Mstar_candidates=float(np.log10(np.mean(10 ** lmgl[cand]))),
        logmean_Mstar_bright_candidates=float(np.log10(np.mean(10 ** lmgl[cand & (rl < 17.5)]))),
        logmean_Mstar_isolated=float(np.log10(np.mean(10 ** lmgl[isoall]))),
        logmean_Mgal_isolated=float(np.log10(np.mean(10 ** lmgl[isoall] * (1 + 10 ** (-0.69 * lmgl[isoall] + 6.63))))),
        matched_frac_isolated=float(matched[ip][isoall].mean()))
    R["secondary"] = sec
    P("")
    P("Secondary comparisons with B21 App. A (reported, no line):")
    P(f"  isolated fraction, r < 17.5: {100 * sec['frac_bright_candidates']:.1f} % of candidates, {100 * sec['frac_bright_poolz']:.1f} % of unmasked 0.1<z<0.5 rows (B21 32.0 %)")
    P(f"  isolated fraction, r > 17.5: {100 * sec['frac_faint_candidates']:.1f} % of candidates, {100 * sec['frac_faint_poolz']:.1f} % of unmasked 0.1<z<0.5 rows (B21 36.8 %)")
    P(f"  isolated lenses with r < 17.5: {sec['n_isolated_bright']:,} (B21 about 3,800)")
    P(f"  log mean M*: candidates {sec['logmean_Mstar_candidates']:.3f} (B21 10.77), r<17.5 candidates {sec['logmean_Mstar_bright_candidates']:.3f} (10.78), isolated {sec['logmean_Mstar_isolated']:.3f} (10.61)")
    P(f"  log mean M_gal, isolated: {sec['logmean_Mgal_isolated']:.3f} (B21 10.69)")
    P(f"  share of isolated lenses whose fs is measured (P3a match): {100 * sec['matched_frac_isolated']:.1f} %")
    # lens inventory for stage 2 (gitignored cache)
    sel = il[iso]
    gi = ip[sel]
    np.savez(os.path.join(CACHE, "fn4c_lenses.npz"), row=gi, ra=ra[gi], dec=dec[gi], z=zp[sel], logM=lmp[sel] + 0.056, r=rmag[gi], matched=matched[gi])

R["checks"] = dict(K1=K1, K2=bool(K2), K3=k3ok, K4=bool(K4), K5=bool(K5))
P("")
P(f"Checks: K1 {K1}, K2 {bool(K2)}, K3 {k3ok}, K4 {bool(K4)}, K5 {bool(K5)}")
P(f"LABEL{' (MUTATE)' if MUT else ''}: {label}. Primary N = {N:,} against 259,383 ({100 * (N / TARGET - 1):+.1f} %), line 5 %.")
if not MUT:
    P(f"Closest variant: {R['closest_variant']} ({100 * R['variants'][R['closest_variant']]['deviation']:+.1f} %).")
else:
    R["mutate_bites"] = bool(not match)
    P(f"MUTATE {'BITES: N leaves the 5 % window' if not match else 'DID NOT BITE: N stays inside the 5 % window (failed check)'}.")
P(f"done {tm()}")
with open(os.path.join(HERE, f"fn4c_rebuild{TAG}.json"), "w") as f:
    json.dump(R, f, indent=1, sort_keys=True)
with open(os.path.join(HERE, f"fn4c_rebuild{TAG}.out"), "w") as f:
    f.write("\n".join(OUT) + "\n")
if MUT:
    sys.exit(1 if not match else 0)          # the twin must fail the gate; exit 0 here means it did not bite
sys.exit(0 if (checks_ok and match) else 1)
