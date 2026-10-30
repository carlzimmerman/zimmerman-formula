#!/usr/bin/env python3
"""GH7 per-lens compensated apertures from the ACT NILC T map (no velocity is read here), and the gas model."""
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
# K4: a known beam source through the same aperture code, against its analytic CAP
FW = 1.6; SB = FW / (2 * math.sqrt(2 * math.log(2))); dc, dr = .3, -.2; cd = 1.0; x = (II - dc) * .5 * cd; y = (JJ - dr) * .5; G0 = np.exp(-.5 * (x * x + y * y) / SB ** 2)
c4 = caps(*shells(G0, 0, cd, dc, dr)); ana = lambda t: 2 * np.pi * SB ** 2 * (1 - np.exp(-.5 * t * t / SB ** 2)) / (np.pi * t * t); an = ana(TH) - (ana(TH * math.sqrt(2)) * 2 - ana(TH)); k4 = float(np.max(np.abs(c4 / an - 1)[TH >= 2]))
check("K4_aperture_vs_analytic", k4 < .02, f"max rel err {k4:.3%} at theta >= 2' (1' and 1.5' sampled by 0.5' pixels: {np.abs(c4 / an - 1)[:2]})")
# gas model (criteria: as GH3-GH5)
L_ = np.load(os.path.join(W, "gh7_lenses.npz")); ra, de, z, lm = L_["ra"], L_["dec"], L_["z"], L_["lm"]
H, OM = 0.679, 0.3085; DH = 299792.458 / (100 * H); zz = np.linspace(0, 1, 4001); EE = np.sqrt(OM * (1 + zz) ** 3 + 1 - OM); CH = np.r_[0, np.cumsum(.5 * (1 / EE[1:] + 1 / EE[:-1]) * np.diff(zz))]
DA = lambda x: DH * np.interp(x, zz, CH) / (1 + x); ZTF = np.array([[9, 82.], [9.5, 102.], [10, 131.], [10.5, 178.], [10.75, 210.], [11, 295.], [11.25, 480.], [11.5, 950.]]); Rv = lambda l: np.interp(l, ZTF[:, 0], ZTF[:, 1])
BETA, RCK, NORM, MUE = .43, 6., 1.84, 1.14; MSUN, KPC, MP, SIGT, TCMB = 1.98847e30, 3.0856776e19, 1.67262192e-27, 6.6524587e-29, 2.72548e6
_R, _r = 30., 6.; _l = np.linspace(0, 3e5, 3000001); k1 = 2 * np.trapz((1 + (_R ** 2 + _l ** 2) / _r ** 2) ** -1., _l) / (math.pi * _r ** 2 / math.sqrt(_r ** 2 + _R ** 2)) - 1; check("K1_projection_closed_form", abs(k1) < 1e-4, f"{k1:+.1e}")
def tau_tab(l, k):
    R0 = float(Rv(l)); rr = np.linspace(0, R0, 20001); sh = (1 + (rr / RCK) ** 2) ** (-1.5 * BETA); ne0 = NORM * 10 ** l * MSUN / (np.trapz(4 * np.pi * rr ** 2 * sh, rr) * KPC ** 3) / (MUE * MP); Rk = np.r_[0, np.geomspace(.1, k * R0, 500)]; o = np.zeros_like(Rk)
    for i, R in enumerate(Rk[:-1]):
        ll = np.linspace(0, math.sqrt((k * R0) ** 2 - R * R), 2001); o[i] = 2 * np.trapz((1 + (R * R + ll * ll) / RCK ** 2) ** (-1.5 * BETA), ll) * KPC
    return Rk, SIGT * ne0 * o
FG = .05; nf = int(16 / FG); fx = (np.arange(2 * nf + 1) - nf) * FG; FXX, FYY = np.meshgrid(fx, fx); FTH = np.hypot(FXX, FYY); BK = np.exp(-.5 * FTH ** 2 / SB ** 2); BK /= BK.sum(); BF = np.fft.rfft2(np.fft.ifftshift(BK))
ibin = np.searchsorted(EDGES, FTH.ravel()); nall = np.cumsum(np.bincount(ibin, minlength=len(EDGES) + 1))[:len(EDGES)]
def model_cap(zc, l, k):
    Rk, t = tau_tab(l, k); da = DA(zc) * 1e3; img = np.interp(FTH * da * math.pi / 180 / 60, Rk, t, right=0); cv = np.fft.irfft2(np.fft.rfft2(img) * BF, s=img.shape); s = np.cumsum(np.bincount(ibin, cv.ravel(), len(EDGES) + 1))[:len(EDGES)]; return caps(s, nall)
# real CAPs: read the map row-block by row-block
inmap = (de > -60) & (de < 22); idx = np.where(inmap)[0]; print("lenses in Dec range", len(idx), flush=True)
c0, r0 = col_of(ra[idx]), row_of(de[idx]); o = np.argsort(r0); idx, c0, r0 = idx[o], c0[o], r0[o]; CAP = np.full((len(ra), len(TH)), np.nan, np.float32)
mm = np.memmap(FN, dtype=">f4", mode="r", offset=OFF, shape=(NY, NX)); BL = 300; rmin = int(r0.min()) - M - 1; b0 = rmin
while b0 < r0.max():
    sel = np.where((r0 >= b0 + M + 1) & (r0 < b0 + M + 1 + BL))[0]; top = b0 + BL + 2 * M + 3
    if len(sel):
        A = np.array(mm[max(b0, 0):min(top, NY)], dtype=np.float32); y0 = max(b0, 0)
        for s in sel:
            ic, ir = int(round(c0[s])), int(round(r0[s])); jr = ir - y0
            if jr - M < 0 or jr + M + 1 > A.shape[0]: continue
            st = A[jr - M:jr + M + 1][:, np.arange(ic - M, ic + M + 1) % NX]
            if not np.all(np.isfinite(st)) or np.any(st == 0): continue
            CAP[idx[s]] = caps(*shells(st, 0, math.cos(math.radians(de[idx[s]])), c0[s] - ic, r0[s] - ir))
    b0 += BL
    del_ok = True
good = np.isfinite(CAP[:, 0]); print("lenses with valid stamps", int(good.sum()), flush=True)
# gas model per (z, lm) cell, no velocity needed
zb = np.quantile(z[good], np.linspace(0, 1, 11)); lb = np.array([10.6, 10.7, 10.8, 10.9, 11.0]) + 2 * np.log10(.704 / H); lg = lm + 2 * np.log10(.704 / H); iz = np.clip(np.searchsorted(zb, z) - 1, 0, 9); il = np.clip(np.searchsorted(lb, lg) - 1, 0, 3)
MC = {}
for k in (1.0, 1.8, 3.0):
    a = np.zeros((10, 4, len(TH)))
    for i in range(10):
        zc = float(z[good & (iz == i)].mean())
        for j in range(4): a[i, j] = model_cap(zc, float((lb[j] + lb[j + 1]) / 2), k)
    MC[str(k)] = a
np.savez(os.path.join(W, "gh7_cap.npz"), cap=CAP, good=good, iz=iz, il=il, TH=TH, **{"m" + k: v for k, v in MC.items()})
json.dump(RES, open(os.path.join(HERE, "gh7_cap.json"), "w"), indent=1, sort_keys=True); print("done", flush=True)
