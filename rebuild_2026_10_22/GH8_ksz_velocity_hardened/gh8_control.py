#!/usr/bin/env python3
"""GH8 positive control, run first: hardened velocities, weights, own-mass filter, on all BGS above log M* 10.5, 11, 11.25."""
import os, sys, json, math
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np, healpy as hp
from astropy.io import fits
from astropy.wcs import WCS
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data"); W = os.path.join(EXT, "gh8_work")
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

np.savez(os.path.join(W, "gh8_ctrl_cap.npz"), cap=CAP, ra=ra, de=de, z=z, lm=lm)
J = json.load(open(os.path.join(HERE, "gh8_vel.json"))); Nm, Lb, CELL = J["mesh"], J["box"], 6.0; F = np.load(os.path.join(W, "gh8_psi.npy"), mmap_mode="r")
OM = 0.3085; zz = np.linspace(0, 1, 4001); EZ = np.sqrt(OM * (1 + zz) ** 3 + 1 - OM); CHI = np.r_[0, np.cumsum(.5 * (1 / EZ[1:] + 1 / EZ[:-1]) * np.diff(zz))] * 2997.92458
def read(P):
    g = (P + Lb / 2) / CELL - .5; i = np.floor(g).astype(int); f = g - i; o = np.zeros_like(P)
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                w = (f[:, 0] if a else 1 - f[:, 0]) * (f[:, 1] if b else 1 - f[:, 1]) * (f[:, 2] if c else 1 - f[:, 2]); ii, jj, kk = (i[:, 0] + a) % Nm, (i[:, 1] + b) % Nm, (i[:, 2] + c) % Nm
                for x in range(3): o[:, x] += w * F[x][ii, jj, kk]
    return o
ch = np.interp(z, zz, CHI); rr, dd = np.radians(ra), np.radians(de); rh = np.c_[np.cos(dd) * np.cos(rr), np.cos(dd) * np.sin(rr), np.sin(dd)]; S = ch[:, None] * rh; X = S - np.sum(read(S) * rh, axis=1)[:, None] * rh
v = 100 * np.interp(z, zz, EZ) / (1 + z) * np.sum(read(X) * rh, axis=1) / 299792.458; print("rms v_rec", round(float(v.std() * 299792.458), 1), flush=True)
H = 0.679; lg = lm + 2 * np.log10(.704 / H); lb = np.array([10.5, 10.625, 10.75, 10.875, 11, 11.125, 11.25, 11.375, 11.6]) + 2 * np.log10(.704 / H); il = np.clip(np.searchsorted(lb, lg) - 1, 0, 7)
valid = np.isfinite(CAP[:, 0]); p32 = hp.ang2pix(32, ra, de, lonlat=True); r32 = np.sqrt(np.bincount(p32[valid], CAP[valid, 2].astype(np.float64) ** 2, hp.nside2npix(32)) / np.maximum(np.bincount(p32[valid], minlength=hp.nside2npix(32)), 1)); blank = r32[p32] < 4.0; print("dropped as blank", int((valid & blank).sum()), "of", int(valid.sum()), flush=True); valid = valid & ~blank; np.save(os.path.join(W, "gh8_good32.npy"), r32 >= 4.0); zb = np.quantile(z[valid], np.linspace(0, 1, 11)); iz = np.clip(np.searchsorted(zb, z) - 1, 0, 9); MC = np.zeros((10, 8, len(TH)))
H0, OM0 = 0.679, 0.3085; DH = 299792.458 / (100 * H0); _zz = np.linspace(0, 1, 4001); _E = np.sqrt(OM0 * (1 + _zz) ** 3 + 1 - OM0); _CH = np.r_[0, np.cumsum(.5 * (1 / _E[1:] + 1 / _E[:-1]) * np.diff(_zz))]
DA = lambda x: DH * np.interp(x, _zz, _CH) / (1 + x); ZTF = np.array([[9, 82.], [9.5, 102.], [10, 131.], [10.5, 178.], [10.75, 210.], [11, 295.], [11.25, 480.], [11.5, 950.]]); Rv = lambda l: np.interp(l, ZTF[:, 0], ZTF[:, 1])
BETA, RCK, NORM, MUE = .43, 6., 1.84, 1.14; MSUN, KPC, MP, SIGT, TCMB = 1.98847e30, 3.0856776e19, 1.67262192e-27, 6.6524587e-29, 2.72548e6
def tau_tab(l, k):
    R0 = float(Rv(l)); rr = np.linspace(0, R0, 20001); sh = (1 + (rr / RCK) ** 2) ** (-1.5 * BETA); ne0 = NORM * 10 ** l * MSUN / (np.trapz(4 * np.pi * rr ** 2 * sh, rr) * KPC ** 3) / (MUE * MP); Rk = np.r_[0, np.geomspace(.1, k * R0, 500)]; o = np.zeros_like(Rk)
    for i, R in enumerate(Rk[:-1]):
        ll = np.linspace(0, math.sqrt((k * R0) ** 2 - R * R), 2001); o[i] = 2 * np.trapz((1 + (R * R + ll * ll) / RCK ** 2) ** (-1.5 * BETA), ll) * KPC
    return Rk, SIGT * ne0 * o
FW = 1.6; SB = FW / (2 * math.sqrt(2 * math.log(2))); FG = .05; nf = int(16 / FG); fx = (np.arange(2 * nf + 1) - nf) * FG; FXX, FYY = np.meshgrid(fx, fx); FTH = np.hypot(FXX, FYY); BK = np.exp(-.5 * FTH ** 2 / SB ** 2); BK /= BK.sum(); BF = np.fft.rfft2(np.fft.ifftshift(BK))
ibin = np.searchsorted(EDGES, FTH.ravel()); nall = np.cumsum(np.bincount(ibin, minlength=len(EDGES) + 1))[:len(EDGES)]
def model_cap(zc, l, k):
    Rk, t = tau_tab(l, k); da = DA(zc) * 1e3; img = np.interp(FTH * da * math.pi / 180 / 60, Rk, t, right=0); cv = np.fft.irfft2(np.fft.rfft2(img) * BF, s=img.shape); s = np.cumsum(np.bincount(ibin, cv.ravel(), len(EDGES) + 1))[:len(EDGES)]; return caps(s, nall)

TABS = {j: None for j in range(8)}
for i in range(10):
    zc = float(z[valid & (iz == i)].mean())
    for j in range(8): MC[i, j] = model_cap(zc, float((lb[j] + lb[j + 1]) / 2), 1.8)
Rf = J["R_fm"]; MC *= TCMB * Rf; pix = hp.ang2pix(8, ra, de, lonlat=True); rng = np.random.default_rng(818); best = 0
def est(c, u, w): return -np.sum(w * c * u[:, None], axis=0) / np.sum(w * (u * u)[:, None], axis=0)
for thr in (10.5, 11.0, 11.25):
    g = valid & (lm >= thr); c, u, zi, li, pi = CAP[g].astype(np.float64), v[g].astype(np.float64), iz[g], il[g], pix[g]
    for b in range(10): c[zi == b] -= c[zi == b].mean(axis=0)
    var = c.var(axis=0); w = np.tile(1 / var, (len(c), 1))
    for p in np.unique(pi):
        q = pi == p
        if q.sum() >= 500: w[q] = 1 / c[q].var(axis=0)
    u = u.copy()
    for b in range(10):
        q = zi == b; c[q] -= np.sum(w[q] * c[q], axis=0) / np.sum(w[q], axis=0); u[q] -= u[q].mean()
    mi = MC[zi, li]; wu = np.sum(w * (u * u)[:, None], axis=0); tem = np.sum(w * mi * (u * u)[:, None], axis=0) / wu
    def sh():
        o = u.copy()
        for b in range(10):
            q = np.where(zi == b)[0]; o[q] = u[rng.permutation(q)]
        return o
    T = est(c, u, w); NS = np.array([est(c, sh(), w) for _ in range(300)]); Ci = (300 - 8 - 2) / 299 * np.linalg.inv(np.cov(NS.T)); fac = tem @ Ci / (tem @ Ci @ tem); A = float(fac @ T); sA = float((NS @ fac).std()); chi = float(T @ Ci @ T); best = max(best, A / sA)
    inj = est(c - mi * u[:, None], u, w); dA = float(fac @ (inj - T)); shn = float((fac @ est(c, sh(), w)) / sA); flip = float(np.max(np.abs(est(c, -u, w) + T)))
    RES[str(thr)] = dict(N=int(g.sum()), That=T.tolist(), err=np.sqrt(np.diag(np.cov(NS.T))).tolist(), tem=tem.tolist(), A=A, s=sA, snr=A / sA, null_chi2=chi, inj=dA, shuffled_snr=shn, flip=flip)
    print(f"M* > {thr}: N {g.sum()}; That {np.round(T, 1)}\n  err {np.round(RES[str(thr)]['err'], 1)}\n  model A=1 {np.round(tem, 1)}\n  A {A:.3f}+-{sA:.3f}, S/N {A / sA:.2f}, null chi2 {chi:.1f}/8; K4 inj {dA:.4f}; shuffled S/N {shn:+.2f}; shuffle mean A {float((NS @ fac).mean()):+.4f}; flip {flip:.1e}", flush=True)
    check(f"K4_injection_{thr}", abs(dA - 1) < .02, f"{dA:.4f}"); check(f"MUTATE_{thr}", abs(shn) < 3 and flip < 1e-9, f"shuffled {shn:+.2f}, flip {flip:.1e}")
RES["best_snr"] = best; RES["validated"] = bool(best >= 4); print("CONTROL best S/N", round(best, 2), "validated", RES["validated"], flush=True); json.dump(RES, open(os.path.join(HERE, "gh8_control.json"), "w"), indent=1, sort_keys=True)
