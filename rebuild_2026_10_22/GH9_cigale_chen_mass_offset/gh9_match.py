#!/usr/bin/env python3
"""GH9 offset: DESI CIGALE vs SDSS Wisconsin PCA (Chen+12 method) at fixed CIGALE mass, plus the GKV redshift bridge. Catalogues only."""
import os, json, csv
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data"); RES = {"checks": {}}
def check(n, ok, msg): RES["checks"][n] = bool(ok); print(("PASS " if ok else "FAIL ") + n + ": " + msg, flush=True)
def mad(x): return float(1.4826 * np.median(np.abs(x - np.median(x))))
def unit(r, d): r, d = np.radians(r), np.radians(d); return np.c_[np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)]
h = fits.open(os.path.join(EXT, "desi_dr1_bgs", "BGS_BRIGHT_full_HPmapcut.dat.fits"), memmap=True)[1].data
ra, de, z, zw, dc = [np.array(h[k]) for k in ("RA", "DEC", "Z_not4clus", "ZWARN", "DELTACHI2")]; tid = np.array(h["TARGETID"])
g = (zw == 0) & (dc > 40) & (z > 0.005) & (z < 0.6); ra, de, z, tid = ra[g], de[g], z[g], tid[g]
c = fits.open(os.path.join(EXT, "desi_dr1_cigale", "IronPhysProp_v1.2.fits"), memmap=True)[1].data
ct, cm, cf = np.array(c["TARGETID"]), np.array(c["LOGM"]), np.array(c["LOGSFR"])
k = (np.char.strip(np.array(c["SURVEY"]).astype(str)) == "main") & (np.char.strip(np.array(c["PROGRAM"]).astype(str)) == "bright"); ct, cm, cf = ct[k], cm[k], cf[k]
s = np.argsort(ct); i = np.searchsorted(ct[s], tid); i[i >= len(s)] = 0; ok = ct[s][i] == tid
lm, sf = np.full(len(z), np.nan), np.full(len(z), np.nan); lm[ok] = cm[s][i[ok]]; sf[ok] = cf[s][i[ok]]
m = np.isfinite(lm) & (lm >= 10.6) & (lm <= 11); ra, de, z, lm, sf = ra[m], de[m], z[m], lm[m], sf[m]; print("DESI parent 10.6-11", len(z), flush=True)
del h, c, ct, cm, cf, tid, zw, dc
w = fits.open(os.path.join(EXT, "sdss_wisconsin_pca", "wisconsin_pca_bc03-26.fits.gz"), memmap=False)[1].data
wm, we, wz, wr, wd, ww, ws = [np.array(w[n]) for n in ("MSTELLAR_MEDIAN", "MSTELLAR_ERR", "Z", "RA", "DEC", "WARNING", "SPECOBJID")]; del w
q = np.isfinite(wm) & (ww == 0) & (we > 0); print("Wisconsin rows", len(wm), "usable", int(q.sum()), flush=True); o = np.argsort(ws[q]); wm, wz, wr, wd = wm[q][o], wz[q][o], wr[q][o], wd[q][o]
T = cKDTree(unit(wr, wd)); rmax = 2 * np.sin(np.radians(1.5 / 3600) / 2); P = T.query_ball_point(unit(ra, de), rmax)
ia, ib = [], []
for a, lst in enumerate(P):
    lst = [b for b in lst if abs(wz[b] - z[a]) < 0.001]
    if lst: ia.append(a); ib.append(min(lst))
ia, ib = np.array(ia), np.array(ib); sep = np.degrees(2 * np.arcsin(np.linalg.norm(unit(ra[ia], de[ia]) - unit(wr[ib], wd[ib]), axis=1) / 2)) * 3600; dz = np.abs(wz[ib] - z[ia])
check("K1_match", np.median(dz) < 2e-4 and np.median(sep) < .5, f"pairs {len(ia)}, median |dz| {np.median(dz):.1e}, sep {np.median(sep):.3f} arcsec")
D = lm[ia] - wm[ib]; zp, lp, ss, rp = z[ia], lm[ia], (sf - lm)[ia], ra[ia]; ov = (zp >= .1) & (zp <= .19); cell = np.clip(((lp - 10.6) / .1).astype(int), 0, 3)
pz = (z >= .1) & (z <= .19); RES["N_overlap"] = int(ov.sum()); RES["frac_of_parent_0.1_0.19"] = float(ov.sum() / pz.sum()); print("overlap pairs", int(ov.sum()), f"= {ov.sum() / pz.sum():.3f} of DESI parent at 0.1-0.19", flush=True)
rng = np.random.default_rng(909)
def cells(x, sel):
    o = []
    for j in range(4):
        q = sel & (cell == j); o.append(float(np.median(x[q])) if q.sum() else np.nan)
    return np.array(o)
Dj = cells(D, ov); Nj = [int((ov & (cell == j)).sum()) for j in range(4)]; bs = []
idx = np.where(ov)[0]
for _ in range(200):
    r = rng.choice(idx, len(idx)); bs.append([np.median(D[r][cell[r] == j]) for j in range(4)])
Ej = np.std(bs, axis=0); RES.update(Dj=Dj.tolist(), Ej=Ej.tolist(), Nj=Nj, D_all=float(np.median(D[ov])), MAD=mad(D[ov]))
print("Delta_j", np.round(Dj, 4), "+-", np.round(Ej, 4), "N", Nj, "all", round(RES["D_all"], 4), "MAD", round(RES["MAD"], 3), flush=True)
check("K4_cell_counts", min(Nj) >= 2000, str(Nj))
Dinj = lm[ia] - (wm[ib] + .2); d = float(np.max(np.abs(cells(Dinj, ov) - (Dj - .2)))); check("K3_injection", d < 1e-6, f"{d:.1e}")
sh = D.copy(); sh[idx] = lp[idx] - wm[ib][idx][rng.permutation(len(idx))]; r = mad(sh[ov]) / RES["MAD"]; check("MUTATE_shuffle_pairs", r >= 1.5, f"MAD x{r:.2f}")
for lab, sel in (("passive", ss < -11), ("star_forming", ss >= -11), ("north_RA90_280", (rp > 90) & (rp < 280)), ("south", ~((rp > 90) & (rp < 280)))):
    RES[lab] = dict(N=int((ov & sel).sum()), D=float(np.median(D[ov & sel])), Dj=cells(D, ov & sel).tolist()); print(lab, RES[lab]["N"], "Delta", round(RES[lab]["D"], 4), np.round(RES[lab]["Dj"], 3), flush=True)
ztr = (zp >= .05) & (zp <= .19); y = D[ztr] - Dj[cell[ztr]]; A = np.polyfit(zp[ztr], y, 1); bsl = [np.polyfit(zp[ztr][q], y[q], 1)[0] for q in (rng.integers(0, ztr.sum(), ztr.sum()) for _ in range(100))]; RES["slope_dDdz"] = float(A[0]); RES["slope_err"] = float(np.std(bsl))
print(f"slope dDelta/dz {A[0]:+.3f} +- {RES['slope_err']:.3f} (0.05-0.19)", flush=True)
for a, b in ((.05, .08), (.08, .11), (.11, .14), (.14, .19)):
    q = (zp >= a) & (zp < b); print(f"  z {a}-{b}: N {q.sum()} Delta {np.median(D[q]):+.3f}", flush=True)
# GKV bridge
gk = []
with open(os.path.join(EXT, "gama_dr4_gkv", "gkv_stellarmass_g09.csv")) as f:
    for r0 in csv.DictReader(f):
        try: gk.append((float(r0["RA"]), float(r0["DEC"]), float(r0["redshift"]), float(r0["logmstar"])))
        except ValueError: pass
gk = np.array(gk); gk = gk[gk[:, 3] > 5]; T2 = cKDTree(unit(gk[:, 0], gk[:, 1])); bx = (ra > 128) & (ra < 142) & (de > -3) & (de < 4); ib2 = np.where(bx)[0]; d2, j2 = T2.query(unit(ra[ib2], de[ib2])); ok2 = (d2 < rmax) & (np.abs(gk[j2, 2] - z[ib2]) < .003); bi = ib2[ok2]; B = lm[bi] - gk[j2[ok2], 3]; bz = z[bi]; ed = np.arange(.1, .51, .1); bc, bm, bn = [], [], []
for a, b in zip(ed[:-1], ed[1:]):
    q = (bz >= a) & (bz < b); bn.append(int(q.sum())); bm.append(float(np.median(B[q])) if q.sum() else np.nan); bc.append(float(np.median(bz[q])) if q.sum() else (a + b) / 2)
RES["bridge"] = dict(zc=bc, med=bm, n=bn, MAD=mad(B)); print("GKV bridge z", np.round(bc, 3), "CIGALE-GKV", np.round(bm, 3), "N", bn, flush=True)
k5 = min(bn[:3]) >= 500; check("K5_bridge_counts", k5, str(bn))
Lz = np.load(os.path.join(EXT, "gh7_work", "gh7_lenses.npz"))["z"]; zl, zo = float(np.median(Lz)), float(np.median(zp[ov])); RES.update(z_lens=zl, z_overlap=zo)
dB = float(np.interp(zl, bc, bm) - np.interp(zo, bc, bm)); dS = float(RES["slope_dDdz"] * (zl - zo)); RES.update(dD3_bridge=dB, dD3_slope=dS, dD3=dB if k5 else dS); print(f"z_lens {zl:.3f} z_overlap {zo:.3f}: D3 add bridge {dB:+.3f} slope {dS:+.3f}", flush=True)
json.dump(RES, open(os.path.join(HERE, "gh9_match.json"), "w"), indent=1, sort_keys=True)
