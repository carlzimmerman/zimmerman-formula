#!/usr/bin/env python3
"""GH7 positive control: the same apertures and velocities on all BGS above log M* 10.5, 11, 11.25."""
import os, sys, json, math
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data"); W = os.path.join(EXT, "gh7_work")
FN = os.path.join(EXT, "act_dr6_nilc", "act-planck_dr6.02_nilc_blackbody_T.fits"); RES = {"checks": {}}
def check(n, ok, msg): RES["checks"][n] = bool(ok); print(("PASS " if ok else "FAIL ") + n + ": " + msg, flush=True)
assert os.path.getsize(FN) == 1783298880
NX, NY, OFF = 43200, 10320, 2880; hdr = fits.Header.fromstring(open(FN, "rb").read(2880).decode("ascii")); print({k: hdr.get(k) for k in ("NAXIS", "NAXIS1", "NAXIS2", "BUNIT", "CDELT1", "CRVAL1", "CRPIX1", "CRVAL2", "CRPIX2")}, flush=True)
def col_of(ra): ra = np.where(ra >= 180, ra - 360, ra); return 21600.0 - 120.0 * ra
def row_of(dec): return 7559.5 + 120.0 * dec
tp = np.array([[12.3, -5.0], [133.7, 1.2], [200.1, -30.5], [355.2, 2.9]]); px = WCS(hdr, naxis=2).all_world2pix(tp, 0); d = float(np.max(np.abs(np.c_[col_of(tp[:, 0]), row_of(tp[:, 1])] - px)))
check("K2_pixel_geometry", d < 0.01, f"max |d pix| {d:.2e}")
TH = np.array([1, 1.5, 2, 3, 4, 6, 8, 10.]); EDGES = np.unique(np.r_[TH, TH * math.sqrt(2)]); M = 30                # stamp half width, pixels
JJ, II = np.mgrid[-M:M + 1, -M:M + 1]
def shells(st, dr, cosd, dcol, drow):
    x = (II - dcol) * .5 * cosd; y = (JJ - drow) * .5; r2 = x * x + y * y; ix = np.searchsorted(EDGES ** 2, r2.ravel()); s = np.bincount(ix, st.ravel(), len(EDGES) + 1); n = np.bincount(ix, minlength=len(EDGES) + 1)
    return np.cumsum(s)[:len(EDGES)], np.cumsum(n)[:len(EDGES)]
IDX_IN = np.searchsorted(EDGES, TH); IDX_OUT = np.searchsorted(EDGES, TH * math.sqrt(2))
def caps(cs, cn):
    return cs[IDX_IN] / cn[IDX_IN] - (cs[IDX_OUT] - cs[IDX_IN]) / (cn[IDX_OUT] - cn[IDX_IN])
D = np.load(os.path.join(EXT, "gh6_work", "gh6_bgs.npz")); s_ = (D["z"] >= .1) & (D["z"] <= .5) & (D["lm"] >= 10.5) & (D["de"] > -60) & (D["de"] < 22); ra, de, z, lm = D["ra"][s_], D["de"][s_], D["z"][s_], D["lm"][s_]; print("control lenses", len(z), flush=True)
c0, r0 = col_of(ra), row_of(de); o = np.argsort(r0); ra, de, z, lm, c0, r0 = ra[o], de[o], z[o], lm[o], c0[o], r0[o]; CAP = np.full((len(z), len(TH)), np.nan, np.float32)
mm = np.memmap(FN, dtype=">f4", mode="r", offset=OFF, shape=(NY, NX)); BL = 300; b0 = int(r0.min()) - M - 1
while b0 < r0.max():
    a, b = np.searchsorted(r0, [b0 + M + 1, b0 + M + 1 + BL]); y0 = max(b0, 0)
    if b > a:
        A = np.array(mm[y0:min(b0 + BL + 2 * M + 3, NY)], dtype=np.float32)
        for s in range(a, b):
            ic, ir = int(round(c0[s])), int(round(r0[s])); jr = ir - y0
            if jr - M < 0 or jr + M + 1 > A.shape[0]: continue
            st = A[jr - M:jr + M + 1][:, np.arange(ic - M, ic + M + 1) % NX]
            if np.all(np.isfinite(st)) and not np.any(st == 0): CAP[s] = caps(*shells(st, 0, math.cos(math.radians(de[s])), c0[s] - ic, r0[s] - ir))
    b0 += BL
OM, BET = 0.3085, 0.44; zz = np.linspace(0, 1, 4001); EZ = np.sqrt(OM * (1 + zz) ** 3 + 1 - OM); CHI = np.r_[0, np.cumsum(.5 * (1 / EZ[1:] + 1 / EZ[:-1]) * np.diff(zz))] * 2997.92458
J = json.load(open(os.path.join(HERE, "gh7_vel.json"))); Nm, Lb, CELL = J["mesh"], J["box"], 8.0; F = np.load(os.path.join(W, "gh7_psi.npy"), mmap_mode="r"); ch = np.interp(z, zz, CHI); rr, dd = np.radians(ra), np.radians(de); rh = np.c_[np.cos(dd) * np.cos(rr), np.cos(dd) * np.sin(rr), np.sin(dd)]; P = ch[:, None] * rh
i = ((P + Lb / 2) / CELL).astype(int) % Nm; v = np.interp(z, zz, EZ) * 100 / (1 + z) * sum(np.array(F[a][i[:, 0], i[:, 1], i[:, 2]]) * rh[:, a] for a in range(3)) / 299792.458
tem = np.einsum("ij,ijk", np.ones((10, 4)) / 40, np.load(os.path.join(W, "gh7_cap.npz"))["m1.8"]); tem = tem / tem.max(); RES["template"] = tem.tolist(); rng = np.random.default_rng(808); best = 0
def that(c, u): return -np.sum(c * u[:, None], axis=0) / np.sum(u * u)
for thr in (10.5, 11.0, 11.25):
    g = np.isfinite(CAP[:, 0]) & (lm >= thr); c, u, zg = CAP[g].astype(np.float64), v[g].astype(np.float64), z[g]; zb = np.quantile(zg, np.linspace(0, 1, 11)); iz = np.clip(np.searchsorted(zb, zg) - 1, 0, 9)
    for b in range(10): c[iz == b] -= c[iz == b].mean(axis=0)
    def sh():
        o = u.copy()
        for b in range(10):
            q = np.where(iz == b)[0]; o[q] = u[rng.permutation(q)]
        return o
    T = that(c, u); NS = np.array([that(c, sh()) for _ in range(300)]); Ci = (300 - 8 - 2) / 299 * np.linalg.inv(np.cov(NS.T)); fac = tem @ Ci / (tem @ Ci @ tem); A = float(fac @ T); sA = float((NS @ fac).std()); chi = float(T @ Ci @ T); best = max(best, A / sA)
    RES[str(thr)] = dict(N=int(g.sum()), That=T.tolist(), err=np.sqrt(np.diag(Ci * 0 + np.cov(NS.T))).tolist(), A=A, s=sA, snr=A / sA, null_chi2=chi); print(f"M* > {thr}: N {g.sum()}, rms v {u.std() * 299792.458:.0f}; That {np.round(T, 2)}; matched peak {A:.2f}+-{sA:.2f} uK, S/N {A / sA:.2f}, null chi2 {chi:.1f}/8", flush=True)
RES["best_snr"] = best; RES["validated"] = bool(best >= 4); print("CONTROL best S/N", round(best, 2), "validated", RES["validated"], flush=True); json.dump(RES, open(os.path.join(HERE, "gh7_control.json"), "w"), indent=1, sort_keys=True)
