#!/usr/bin/env python3
"""CFG302 -- raw HI widths and fluxes (and, where possible, rotation) re-measured from the MIGHTEE-HI DR1 L2 r1p0 cubes
and compared with the catalogue's busy-function values.  Frozen criteria: FROZEN_CRITERIA.md (commit 7d317dd4f), written
before any spectrum was extracted.  A raw-measurement check, not an a0 measurement: no a0 number is computed; kappa = 1/2 is FITTED.

Run:  python3 cfg302_raw_widths.py            -> cfg302_raw_widths.out, cfg302_raw_widths_results.json, cfg302_per_galaxy.csv
      MUTATE=1 python3 cfg302_raw_widths.py   -> the same with the _MUTATE suffix (the line window shifted off the line)
The cube folder comes from $MIGHTEE_R1P0_DIR, default ../_external_data/mightee_hi_dr1 relative to the repository root.
The cubes are read through np.memmap (big-endian float32); nothing cube-sized is written.
"""
import os, sys, json, math, time, hashlib, resource
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from scipy.stats import spearmanr
from astropy.io import fits
from astropy.wcs import WCS

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.environ.get("MIGHTEE_R1P0_DIR", os.path.join(os.path.dirname(REPO), "_external_data", "mightee_hi_dr1"))
DATA_REL = os.path.relpath(DATA, REPO)
CAT = os.path.join(REPO, "data_assembly", "mightee_hi_catalogue_2026-10-02", "MIGHTEE_HI_COSMOS_catalogue.csv")
CFG300_JSON = os.path.join(REPO, "campaign_fresh_gravity", "CFG300_mightee_cube_probe", "cfg300_stageB_results.json")
MUTATE = int(os.environ.get("MUTATE", "0"))
SFX = "_MUTATE" if MUTATE else ""
OUT = os.path.join(HERE, f"cfg302_raw_widths{SFX}")
CSV = os.path.join(HERE, f"cfg302_per_galaxy{SFX}.csv")

C = 299792.458                      # km/s
NU0 = 1290123036.077                # Hz, global channel 0
DNU = 26124.84126282                # Hz per channel
NG = 4055                           # global channels 0..4054
PIX = 8.0                           # arcsec per pixel (r1p0)
RANGES = ["0001-1055", "1001-2055", "2001-3055", "3001-4055"]
FLAGS = ["low_confidence_flag", "blended_flag", "confused_flag", "bad_ellipse_flag", "contaminated_source_flag"]
NMC = 300
T1_ID, T2_ID, T3_ID = "MGTH_J100357.1+022505", "MGTH_J100256.4+023440", "MGTH_J095951.4+014224"
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok):
    CHK.append((name, bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


def mad_sigma(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if x.size == 0: return float("nan")
    return float(1.4826 * np.median(np.abs(x - np.median(x))))


def smooth3(y):
    return ndi.uniform_filter1d(np.asarray(y, float), size=3, mode="nearest")


def fnum(x, f="{:.3g}"):
    return "nan" if x is None or not np.isfinite(x) else f.format(x)


# ------------------------------------------------------------------ the frozen width rule (outside-in, peak-relative)
def width_rule(v, y):
    """v ascending, y the (smoothed) spectrum on v. Returns dict W50, W20 (nan if edge-hit or no positive peak)."""
    out = {}
    if y.size < 3 or not np.all(np.isfinite(y)):
        return dict(W50=np.nan, W20=np.nan, P=np.nan, edge50=True, edge20=True, v50=(np.nan, np.nan))
    Pk = float(np.max(y)); out["P"] = Pk
    for f, nm in ((0.5, "50"), (0.2, "20")):
        if Pk <= 0:
            out["W" + nm] = np.nan; out["edge" + nm] = True; continue
        thr = f * Pk; ab = np.nonzero(y >= thr)[0]; lo, hi = int(ab[0]), int(ab[-1])
        if lo == 0 or hi == y.size - 1:
            out["W" + nm] = np.nan; out["edge" + nm] = True; continue
        def xint(i_out, i_in):
            y0, y1 = y[i_out], y[i_in]; t = (thr - y0) / (y1 - y0) if y1 != y0 else 0.5
            return v[i_out] + t * (v[i_in] - v[i_out])
        vlo, vhi = xint(lo - 1, lo), xint(hi + 1, hi)
        out["W" + nm] = float(vhi - vlo); out["edge" + nm] = False
        if nm == "50": out["v50"] = (float(vlo), float(vhi))
    out.setdefault("v50", (np.nan, np.nan))
    return out


# ------------------------------------------------------------------ the injected / self-test profile
def profile_fine(W, d=0.25, sig_e=8.0, du=0.25):
    u = np.arange(-W / 2 - 60.0, W / 2 + 60.0 + du / 2, du)
    base = np.where(np.abs(u) <= W / 2, 1.0 - d * (1.0 - (2 * u / W) ** 2), 0.0)
    prof = ndi.gaussian_filter1d(base, sig_e / du, mode="constant")
    prof /= prof.sum() * du                                                    # unit integral in km/s
    return u, prof


def profile_channels(W, nu_cen, gs, S_tot):
    """flux density per global channel (Jy) of a profile with box width W [km/s] centred at nu_cen, integral S_tot [Jy Hz]."""
    u, prof = profile_fine(W)
    du = u[1] - u[0]
    cdf = np.concatenate([[0.0], np.cumsum(prof) * du]); ue = np.concatenate([u - du / 2, [u[-1] + du / 2]])
    nu = NU0 + gs * DNU
    u_a = C * (nu_cen / (nu + DNU / 2) - 1); u_b = C * (nu_cen / (nu - DNU / 2) - 1)        # channel edges in velocity (u_a < u_b)
    F = np.interp(u_b, ue, cdf, left=0.0, right=1.0) - np.interp(u_a, ue, cdf, left=0.0, right=1.0)
    w_true = width_rule(u, prof)
    return S_tot * F / DNU, w_true["W50"], w_true["W20"]


# ------------------------------------------------------------------ cubes: headers, beams, memmaps
class MM:
    """a memory map opened per read and released after the copy, so mapped pages do not accumulate (keeps resident memory small)."""
    def __init__(self, path, off, shape):
        self.path, self.off, self.shape = path, off, shape

    def __getitem__(self, sl):
        mm = np.memmap(self.path, dtype=">f4", mode="r", offset=self.off, shape=self.shape)
        out = np.array(mm[sl], dtype=np.float64)
        del mm
        return out


def load_cubes():
    cubes = []
    for k, r in enumerate(RANGES):
        fn = f"MIGHTEE-HI_DR1_COSMOS_L2_r1p0_clean_conv_contsub_{r}.fits"
        path = os.path.join(DATA, fn)
        with fits.open(path, memmap=True) as hl:
            h = hl[0].header.copy(); off = hl[0].fileinfo()["datLoc"]
            bt = hl[1].data; bmaj = np.array(bt["BMAJ"], float); bmin = np.array(bt["BMIN"], float); tunit = hl[1].header.get("TUNIT1", "")
        shape = (h["NAXIS3"], h["NAXIS2"], h["NAXIS1"])
        mm = MM(path, off, shape)
        cubes.append(dict(k=k, file=fn, path=path, hdr=h, off=off, mm=mm, wcs=WCS(h).celestial, bmaj=bmaj, bmin=bmin, tunit=tunit, shape=shape))
    return cubes


def owner(g):
    return np.clip((np.asarray(g) - 28) // 1000, 0, 3)                   # g <= 1000k + 1027 from sub-cube k, else k + 1


def nu_g(g):
    return NU0 + np.asarray(g, float) * DNU


def g_of_nu(nu):
    return (np.asarray(nu, float) - NU0) / DNU


def nu_of_v(nu_cen, v):
    return nu_cen / (1.0 + np.asarray(v, float) / C)


def read_box(cube, c0, c1, ix, iy, h):
    """channels c0..c1 (local), pixels iy-h..iy+h, ix-h..ix+h; NaN-padded outside the image; float64."""
    nz, ny, nx = cube["shape"]
    out = np.full((c1 - c0 + 1, 2 * h + 1, 2 * h + 1), np.nan)
    y0, y1, x0, x1 = iy - h, iy + h, ix - h, ix + h
    ya, yb, xa, xb = max(y0, 0), min(y1, ny - 1), max(x0, 0), min(x1, nx - 1)
    if ya <= yb and xa <= xb:
        out[:, ya - y0:yb - y0 + 1, xa - x0:xb - x0 + 1] = np.asarray(cube["mm"][c0:c1 + 1, ya:yb + 1, xa:xb + 1], dtype=np.float64)
    return out


def aperture_spectrum(cubes, ra, dec, g_lo, g_hi, R_as, BMAJ_eff, A_g):
    """aperture spectrum S(g) [Jy] = sum over the aperture of I / A_beam(g), and the aperture sum of a unit point-source beam / A_beam(g)."""
    gs = np.arange(g_lo, g_hi + 1); ks = owner(gs)
    spec = np.full(gs.size, np.nan); pt = np.full(gs.size, np.nan)
    edge = False; info = []
    R = R_as / PIX; h = int(math.ceil(R)) + 2
    for k in np.unique(ks):
        sel = ks == k; c = gs[sel] - 1000 * k; cube = cubes[k]
        x, y = cube["wcs"].world_to_pixel_values(ra, dec); x, y = float(x), float(y)
        ix, iy = int(round(x)), int(round(y))
        blk = read_box(cube, int(c[0]), int(c[-1]), ix, iy, h)
        jj, ii = np.mgrid[0:2 * h + 1, 0:2 * h + 1]
        r2 = (ii - (x - ix + h)) ** 2 + (jj - (y - iy + h)) ** 2; m = r2 <= R * R
        nz, ny, nx = cube["shape"]
        inimg = (ii + ix - h >= 0) & (ii + ix - h < nx) & (jj + iy - h >= 0) & (jj + iy - h < ny)
        if np.any(m & ~inimg): edge = True
        spec[sel] = blk[:, m].sum(axis=1) / A_g[gs[sel]]
        th = BMAJ_eff[gs[sel]] / PIX
        r2m = r2[m]
        pt[sel] = np.array([np.exp(-4 * math.log(2) * r2m / t ** 2).sum() for t in th]) / A_g[gs[sel]]
        info.append(dict(cube=int(k), x=x, y=y, npix=int(m.sum())))
    return gs, spec, pt, edge, info


# ------------------------------------------------------------------ the frozen measurement
def measure(gs, spec, nu_cen, w50cat, excl=None, rng=None, nmc=NMC):
    v = C * (nu_cen / nu_g(gs) - 1.0)
    Vw = max(1.5 * w50cat, 300.0)
    W = np.abs(v) <= Vw; L = np.abs(v) <= w50cat / 2 + 50.0
    N = (np.abs(v) > Vw + 100.0) & (np.abs(v) <= 3 * Vw + 1100.0) & np.isfinite(spec)
    if excl is not None: N &= ~excl
    noise = spec[N]
    med = float(np.median(noise)) if noise.size else np.nan
    sig = mad_sigma(noise)
    idx = np.nonzero(N)[0]; runs = np.split(idx, np.nonzero(np.diff(idx) > 1)[0] + 1) if idx.size else []
    blocks = [spec[r[i:i + 8]].sum() for r in runs for i in range(0, r.size - 7, 8)]
    sm_runs = np.concatenate([smooth3(spec[r]) for r in runs if r.size >= 3]) if runs else np.array([])
    sig3 = mad_sigma(sm_runs)
    fcorr_flag = len(blocks) < 10
    fcorr = 1.0 if fcorr_flag else mad_sigma(blocks) ** 2 / (8 * sig ** 2)
    nW, nL = int(W.sum()), int(L.sum())
    S_win = float(DNU * np.sum(spec[W])); S_L = float(DNU * np.sum(spec[L]))
    sS_win = float(DNU * sig * math.sqrt(nW * fcorr)); sS_L = float(DNU * sig * math.sqrt(nL * fcorr))
    snr_L = S_L / sS_L if sS_L > 0 else np.nan; snr_win = S_win / sS_win if sS_win > 0 else np.nan
    det = bool(np.isfinite(snr_L) and snr_L >= 5.0)
    o = np.argsort(v[W]); vW = v[W][o]; yW = spec[W][o]
    w = width_rule(vW, smooth3(yW))
    res = dict(V_w=Vw, nW=nW, nL=nL, nN=int(N.sum()), sigma_ch=sig, sigma_sm3=sig3, baseline_med=med, f_corr=fcorr, f_corr_flag=fcorr_flag, n_blocks=len(blocks),
               S_win=S_win, S_win_err=sS_win, S_L=S_L, S_L_err=sS_L, snr_L=snr_L, snr_win=snr_win, detected=det,
               W50=w["W50"], W20=w["W20"], edge50=w["edge50"], edge20=w["edge20"], v50=w["v50"], peak=w["P"],
               snr_peak=(w["P"] / sig3 if sig3 and np.isfinite(sig3) and sig3 > 0 else np.nan))
    res["W50_defined"] = bool(det and np.isfinite(w["W50"])); res["W20_defined"] = bool(det and np.isfinite(w["W20"]))
    if rng is not None and noise.size > 0 and nmc > 0:
        nc = noise.size; w50s, w20s = [], []
        for _ in range(nmc):
            s0 = int(rng.integers(nc)); seg = noise[(s0 + np.arange(nW)) % nc]
            wj = width_rule(vW, smooth3(yW + seg)); w50s.append(wj["W50"]); w20s.append(wj["W20"])
        w50s, w20s = np.array(w50s), np.array(w20s)
        for nm, arr in (("W50", w50s), ("W20", w20s)):
            ok = np.isfinite(arr); res[nm + "_mc_frac"] = float(ok.mean())
            res[nm + "_err"] = float(0.5 * (np.percentile(arr[ok], 84) - np.percentile(arr[ok], 16))) if ok.sum() >= 10 else np.nan
    else:
        res.update(W50_err=np.nan, W20_err=np.nan, W50_mc_frac=np.nan, W20_mc_frac=np.nan)
    return res, v, W, L, N


# ------------------------------------------------------------------ size screen and PV
def m0_box(cubes, ra, dec, g_lo, g_hi, h):
    """moment-0 (sum over channels g_lo..g_hi of I, times DNU) in a (2h+1)^2 box; segments of different sub-cubes aligned at the rounded source pixel."""
    gs = np.arange(g_lo, g_hi + 1); ks = owner(gs); M0 = None; ref = None
    counts = {int(k): int((ks == k).sum()) for k in np.unique(ks)}; kmaj = max(counts, key=counts.get)
    for k in np.unique(ks):
        c = gs[ks == k] - 1000 * k; cube = cubes[k]
        x, y = cube["wcs"].world_to_pixel_values(ra, dec); x, y = float(x), float(y); ix, iy = int(round(x)), int(round(y))
        part = read_box(cube, int(c[0]), int(c[-1]), ix, iy, h).sum(axis=0) * DNU
        M0 = part if M0 is None else M0 + part
        if k == kmaj: ref = (x - ix + h, y - iy + h, k, ix, iy)
    return M0, ref


def size_screen(M0, bx, by, theta_as):
    th = theta_as / PIX; n = M0.shape[0]
    jj, ii = np.mgrid[0:n, 0:n]; rr = np.hypot(ii - bx, jj - by)
    ann = (rr >= 3 * th) & (rr <= 5 * th) & np.isfinite(M0)
    s = mad_sigma(M0[ann]); out = dict(sigma_M0=s, annulus_median=float(np.median(M0[ann])) if ann.any() else np.nan)
    inner = (rr <= th) & np.isfinite(M0)
    if not inner.any() or not np.isfinite(s) or s <= 0:
        out.update(footprint=False, beams_across=np.nan, fwhm_eq_arcsec=np.nan); return out
    cand = np.where(inner, M0, -np.inf); j0, i0 = np.unravel_index(int(np.argmax(cand)), M0.shape); mx = float(M0[j0, i0])
    out["peak_M0_snr"] = mx / s
    M0f = np.nan_to_num(M0, nan=-np.inf)
    lab50, _ = ndi.label(M0f >= 0.5 * mx, structure=np.ones((3, 3)))
    a50 = int((lab50 == lab50[j0, i0]).sum()) if mx > 0 and lab50[j0, i0] > 0 else 0
    out["fwhm_eq_arcsec"] = 2 * math.sqrt(a50 * PIX ** 2 / math.pi) if a50 > 0 else np.nan
    if mx < 3 * s:
        out.update(footprint=False, beams_across=np.nan); return out
    lab, _ = ndi.label(M0f >= 3 * s, structure=np.ones((3, 3))); fp = lab == lab[j0, i0]
    ys, xs = np.nonzero(fp); wgt = np.clip(M0[ys, xs], 0, None)
    xc, yc = float((wgt * xs).sum() / wgt.sum()), float((wgt * ys).sum() / wgt.sum())
    if xs.size >= 3:
        cov = np.cov(np.vstack([xs - xc, ys - yc]), aweights=wgt + 1e-30); ev, evec = np.linalg.eigh(cov); u = evec[:, 1]
    else:
        u = np.array([1.0, 0.0])
    proj = (xs - xc) * u[0] + (ys - yc) * u[1]
    D = float((proj.max() - proj.min() + 1) * PIX); Ddec = math.sqrt(max(D ** 2 - theta_as ** 2, 0.0))
    out.update(footprint=True, n_fp=int(fp.sum()), extent_arcsec=D, extent_deconv_arcsec=Ddec, beams_across=Ddec / theta_as,
               centroid_box=(xc, yc), axis=(float(u[0]), float(u[1])), touches_box_edge=bool(xs.min() == 0 or ys.min() == 0 or xs.max() == n - 1 or ys.max() == n - 1))
    return out


def pv_extract(blk, v, A, Wm, Nm, xc, yc, u, theta_px):
    nz, n, _ = blk.shape; jj, ii = np.mgrid[0:n, 0:n]; dx, dy = ii - xc, jj - yc
    along = dx * u[0] + dy * u[1]; perp = -dx * u[1] + dy * u[0]; strip = np.abs(perp) <= theta_px / 2
    kb = np.floor(along / theta_px + 0.5).astype(int); pts = []
    for k in np.unique(kb[strip]):
        sel = strip & (kb == k)
        sp = np.nansum(blk[:, sel], axis=1) / A
        sb = mad_sigma(sp[Nm]); ch = Wm & (sp >= 3 * sb)
        if ch.sum() >= 1 and sp[ch].sum() > 0: pts.append((int(k), float((sp[ch] * v[ch]).sum() / sp[ch].sum())))
    npos = sum(1 for k, _ in pts if k > 0); nneg = sum(1 for k, _ in pts if k < 0)
    rho = float(spearmanr([k for k, _ in pts], [x for _, x in pts])[0]) if len(pts) >= 5 else float("nan")
    return dict(points=pts, n_pos=npos, n_neg=nneg, rho=rho)


# ------------------------------------------------------------------ self-tests (synthetic; no voxel)
def selftests():
    P("\n== Self-tests on synthetic data (no voxel) ==")
    nu_c = 1340e6; g_c = g_of_nu(nu_c); gs = np.arange(int(g_c) - 60, int(g_c) + 61)
    Snu, w50t, w20t = profile_channels(150.0, nu_c, gs, 1000.0)
    v = C * (nu_c / nu_g(gs) - 1); o = np.argsort(v)
    w = width_rule(v[o], smooth3(Snu[o]))
    check("S1 the width rule on a noise-free channelised double-horn (box 150 km/s, 25 % trough, edges sigma 8 km/s) returns W50 within 3 km/s of the fine-grid truth",
          f"W50 {w['W50']:.2f} vs truth {w50t:.2f} km/s (W20 {w['W20']:.2f} vs {w20t:.2f}); channel {C * DNU / nu_c:.3f} km/s; integral {Snu.sum() * DNU:.4f} of 1000", abs(w["W50"] - w50t) <= 3.0)
    th = 76.0; h = 20; jj, ii = np.mgrid[0:2 * h + 1, 0:2 * h + 1]; bx, by = h + 0.3, h - 0.4
    r2 = (ii - bx) ** 2 + (jj - by) ** 2; img = np.exp(-4 * math.log(2) * r2 / (th / PIX) ** 2)
    A = math.pi * th * th / (4 * math.log(2)) / PIX ** 2; R = 1.5 * th / PIX
    ratio = img[r2 <= R * R].sum() / A
    check("S2 a synthetic point source (76 arcsec beam, 8 arcsec pixels) in a zero block: aperture flux / truth in [0.99, 1.005]", f"{ratio:.5f}", 0.99 <= ratio <= 1.005)
    # S3: a resolved disc, 8 beams across, flat 200 km/s, i = 60 deg, 75 arcsec beam, noise; receding side along +x_true
    rng = np.random.default_rng([302, 3]); th = 75.0; thp = th / PIX; h = int(math.ceil(5 * th / PIX)); n = 2 * h + 1
    dv = 5.85; vch = np.arange(-1500, 1500 + dv / 2, dv); nz = vch.size
    pa = math.radians(30.0); d_true = np.array([math.cos(pa), math.sin(pa)])
    jj, ii = np.mgrid[0:n, 0:n]; dx, dy = (ii - h) * PIX, (jj - h) * PIX
    xa = dx * d_true[0] + dy * d_true[1]; ya = -dx * d_true[1] + dy * d_true[0]
    inc = math.radians(60.0); yd = ya / math.cos(inc); Rd = np.hypot(xa, yd); Rmax = 4 * th
    vlos = np.where(Rd > 0, 200.0 * math.sin(inc) * xa / np.maximum(Rd, 1e-9), 0.0); disc = Rd <= Rmax
    cube = np.zeros((nz, n, n), np.float32)
    for kk in range(nz):
        cube[kk] = np.where(disc, np.exp(-0.5 * ((vch[kk] - vlos) / 10.0) ** 2), 0.0)
    sg = thp / 2.3548
    for kk in range(nz):
        if cube[kk].any(): cube[kk] = ndi.gaussian_filter(cube[kk], sg, mode="constant")
    pk = float(cube.max()); noise = rng.normal(0, 1, cube.shape).astype(np.float32)
    for kk in range(nz): noise[kk] = ndi.gaussian_filter(noise[kk], sg, mode="wrap")
    noise *= (pk / 15.0) / noise.std(); cube += noise
    Wm = np.abs(vch) <= max(1.5 * 2 * 200 * math.sin(inc), 300); Lm = np.abs(vch) <= 200 * math.sin(inc) + 50
    Nm = np.abs(vch) > max(1.5 * 2 * 200 * math.sin(inc), 300) + 100
    A = np.full(nz, math.pi * th * th / (4 * math.log(2)) / PIX ** 2)
    M0 = cube[Lm].sum(axis=0) * DNU
    ss = size_screen(M0, h, h, th)
    pv = pv_extract(cube, vch, A, Wm, Nm, ss["centroid_box"][0], ss["centroid_box"][1], ss["axis"], thp) if ss.get("footprint") else dict(n_pos=0, n_neg=0, rho=float("nan"), points=[])
    sgn = 1.0 if (ss.get("axis", (1, 0))[0] * d_true[0] + ss.get("axis", (1, 0))[1] * d_true[1]) > 0 else -1.0
    ok = bool(ss.get("footprint") and pv["n_pos"] >= 3 and pv["n_neg"] >= 3 and np.isfinite(pv["rho"]) and abs(pv["rho"]) >= 0.8 and np.sign(pv["rho"]) == sgn)
    check("S3 the PV code on a synthetic 8-beam disc (flat 200 km/s, i = 60 deg, 75 arcsec beam, noise) finds >= 3 bins per side, |rho| >= 0.8, receding side as built",
          f"beams across {ss.get('beams_across', float('nan')):.2f}; bins +{pv['n_pos']}/-{pv['n_neg']}; rho {pv['rho']:.3f} (expected sign {sgn:+.0f}); points {[(k, round(x, 1)) for k, x in pv['points']]}", ok)
    NUM["selftest"] = dict(S1=dict(W50=w["W50"], truth=w50t, W20=w["W20"], truth20=w20t), S2=ratio, S3=dict(beams=ss.get("beams_across"), pv=pv))


# ------------------------------------------------------------------ integrity
def integrity(cubes):
    P("\n== Integrity and grid ==")
    man = {}
    with open(os.path.join(DATA, "FETCH_MANIFEST.jsonl")) as f:
        for line in f:
            if line.strip(): r = json.loads(line); man[r["file"]] = r
    rows = []; ok_int = True
    for cb in cubes:
        size = os.path.getsize(cb["path"]); m = man.get(cb["file"], {})
        if MUTATE:
            sha = "not re-hashed in the MUTATE run"; good = size == m.get("bytes")
        else:
            hsh = hashlib.sha256()
            with open(cb["path"], "rb") as f:
                for chunk in iter(lambda: f.read(1 << 24), b""): hsh.update(chunk)
            sha = hsh.hexdigest(); good = (size == m.get("bytes")) and (sha == m.get("sha256"))
        ok_int &= good; rows.append(f"{cb['file'][-14:-5]}: {size} B, sha256 {sha[:16]}..., {'match' if good else 'MISMATCH'}")
    check("C-INT the four sub-cubes match FETCH_MANIFEST.jsonl (size" + (")" if MUTATE else " and sha256)"), "; ".join(rows), ok_int)


# ------------------------------------------------------------------ main
def main():
    P(f"CFG302 raw widths / fluxes from the MIGHTEE-HI DR1 r1p0 cubes   MUTATE={MUTATE}   frozen criteria 7d317dd4f")
    P(f"cube folder: {DATA_REL} (relative to the repository root); catalogue: {os.path.relpath(CAT, REPO)}")
    selftests()
    cubes = load_cubes()

    integrity(cubes)
    gok = True; gdet = []
    for cb in cubes:
        h = cb["hdr"]; nu_first = h["CRVAL3"] + (1 - h["CRPIX3"]) * h["CDELT3"]
        d0 = nu_first - (NU0 + 1000 * cb["k"] * DNU); dd = h["CDELT3"] - DNU
        gok &= abs(d0) <= 1.0 and abs(dd) * 1055 <= 1.0 and h["CTYPE3"].strip() == "FREQ" and h.get("BUNIT", "").strip() == "Jy/beam"
        gdet.append(f"{RANGES[cb['k']]}: first channel offset {d0:+.3f} Hz, CDELT3 offset {dd:+.2e} Hz, BUNIT '{h.get('BUNIT', '').strip()}', beam TUNIT '{cb['tunit']}'")
    check("C-GRID every sub-cube's frequency axis sits on the global grid (1290.123036077 MHz + g x 26.12484126 kHz) to 1 Hz, CTYPE3 FREQ, BUNIT Jy/beam", "; ".join(gdet), gok)

    # global beam arrays
    BMAJ = np.zeros(NG); BMIN = np.zeros(NG); VALID = np.zeros(NG, bool); OWN = owner(np.arange(NG))
    for g in range(NG):
        k = OWN[g]; c = g - 1000 * k; BMAJ[g] = cubes[k]["bmaj"][c]; BMIN[g] = cubes[k]["bmin"][c]
    VALID = (BMAJ >= 50) & (BMAJ <= 120) & (BMIN >= 50) & (BMIN <= 120)
    med_beam = {k: float(np.median(BMAJ[(OWN == k) & VALID])) for k in range(4)}
    BMAJ_eff = np.where(VALID, BMAJ, [med_beam[k] for k in OWN]); BMIN_eff = np.where(VALID, BMIN, [med_beam[k] for k in OWN])
    A_g = math.pi * BMAJ_eff * BMIN_eff / (4 * math.log(2)) / PIX ** 2
    P(f"beams (valid channels): median {np.median(BMAJ[VALID]):.2f} arcsec, range {BMAJ[VALID].min():.2f}-{BMAJ[VALID].max():.2f}; invalid global channels {int((~VALID).sum())} "
      f"(g {np.nonzero(~VALID)[0].min()}-{np.nonzero(~VALID)[0].max()}); per-sub-cube medians {[round(med_beam[k], 2) for k in range(4)]}; pixel {PIX} arcsec; beam area at 76 arcsec {math.pi * 76 * 76 / (4 * math.log(2)) / 64:.1f} px")
    NUM["beam"] = dict(median_valid=float(np.median(BMAJ[VALID])), min_valid=float(BMAJ[VALID].min()), max_valid=float(BMAJ[VALID].max()), n_invalid=int((~VALID).sum()), per_cube_median=med_beam)

    # catalogue and sample
    cat = pd.read_csv(CAT)
    gold = cat[FLAGS].sum(axis=1) == 0
    samp = gold & (cat.z_HI >= 0.02) & (cat.z_HI <= 0.093)
    P(f"\ncatalogue rows {len(cat)}; golden {int(gold.sum())}; sample (golden, 0.02 <= z <= 0.093) {int(samp.sum())}")
    targets = list(cat.index[samp]) + [int(cat.index[cat.ID_catalogue == T1_ID][0]), int(cat.index[cat.ID_catalogue == T3_ID][0])]
    cfg300 = json.load(open(CFG300_JSON))["numbers"]["results"]
    w50_cfg300_T1 = float(cfg300["T1_r0p0"]["w50"])

    allnu = cat.freq_MHz.values * 1e6; allra = np.radians(cat.RA_deg.values); alldec = np.radians(cat.Dec_deg.values); allw = cat.W_50_km_s.values
    recs = []
    for it, i in enumerate(targets):
        r = cat.loc[i]; ra, dec = float(r.RA_deg), float(r.Dec_deg); nu_c = float(r.freq_MHz) * 1e6; w50c = float(r.W_50_km_s)
        insample = bool(samp.loc[i]); Vw = max(1.5 * w50c, 300.0); vO = 2 * Vw + 100.0
        # O placement (coverage of [vO - Vw, vO + Vw] on the + side, else the - side)
        def inside(va, vb, cen=nu_c):
            return g_of_nu(nu_of_v(cen, vb)) >= -0.5 and g_of_nu(nu_of_v(cen, va)) <= NG - 0.5
        if inside(vO - Vw, vO + Vw): side = +1
        elif inside(-vO - Vw, -vO + Vw): side = -1
        else: side = 0
        vO_s = side * vO; nu_O = nu_of_v(nu_c, vO_s) if side else np.nan
        trunc = not inside(-Vw, Vw)
        span = 3 * Vw + 1100.0
        v_lo = -span if side >= 0 else -(vO + span); v_hi = (vO + span) if side > 0 else span
        g_lo = max(int(math.floor(g_of_nu(nu_of_v(nu_c, v_hi)))) - 2, 0); g_hi = min(int(math.ceil(g_of_nu(nu_of_v(nu_c, v_lo)))) + 2, NG - 1)
        gall = np.arange(g_lo, g_hi + 1); vall = C * (nu_c / nu_g(gall) - 1); Wg = gall[np.abs(vall) <= Vw]
        theta = float(np.median(BMAJ[Wg][VALID[Wg]])) if VALID[Wg].any() else med_beam[int(owner(Wg[len(Wg) // 2]))]
        beamflag = bool((~VALID[Wg]).any()); stitch = bool(np.unique(owner(Wg)).size > 1)
        R_as = 1.5 * theta
        # neighbours (catalogue, all rows)
        sep = np.degrees(np.arccos(np.clip(np.sin(math.radians(dec)) * np.sin(alldec) + np.cos(math.radians(dec)) * np.cos(alldec) * np.cos(allra - math.radians(ra)), -1, 1))) * 3600
        dvn = C * (nu_c / allnu - 1); near = (sep < 2.5 * theta) & (np.arange(len(cat)) != i)
        nb = near & (np.abs(dvn) < Vw + allw / 2)
        nbO = near & (np.abs(C * (nu_O / allnu - 1)) < Vw + allw / 2) if side else np.zeros(len(cat), bool)
        gs, spec, pt, edge, info = aperture_spectrum(cubes, ra, dec, g_lo, g_hi, R_as, BMAJ_eff, A_g)
        v = C * (nu_c / nu_g(gs) - 1); Wm_real = np.abs(v) <= Vw
        nanflag = bool(~np.all(np.isfinite(spec[Wm_real])))
        Om = (np.abs(C * (nu_O / nu_g(gs) - 1)) <= Vw) if side else np.zeros(gs.size, bool)
        rec = dict(ID=r.ID_catalogue, RA_deg=ra, Dec_deg=dec, z_HI=float(r.z_HI), freq_MHz=float(r.freq_MHz), in_sample=int(insample),
                   subcubes="+".join(RANGES[k] for k in np.unique(owner(Wg))), beam_arcsec=theta, R_ap_arcsec=R_as, n_ap_pix=int(info[0]["npix"]), V_w_kms=Vw,
                   O_side=side, BEAMFLAG=int(beamflag), STITCH=int(stitch), EDGE=int(edge), NAN=int(nanflag), TRUNC=int(trunc), NBFLAG=int(nb.any()),
                   NB_IDs=";".join(cat.ID_catalogue.values[nb]), NB_in_O=int(nbO.any()),
                   W50_cat=w50c, W50_cat_err=float(r.W_50_km_s_err), S_cat=float(r.S_HI_Jy_Hz), S_cat_err=float(r.S_HI_Jy_Hz_err), SNR_3D_cat=float(r.SNR_3D),
                   log_M_HI_cat=float(r.log_M_HI), incl_deg_cat=float(r.incl_deg))
        rec["primary"] = int(insample and not (beamflag or edge or nanflag or trunc))
        rng = np.random.default_rng([302, it, 1])
        if not MUTATE:
            m, _, _, _, _ = measure(gs, spec, nu_c, w50c, excl=Om, rng=rng)
            cen = nu_c
        else:
            if side == 0:
                m = None; cen = np.nan
            else:
                m, _, _, _, _ = measure(gs, spec, nu_O, w50c, excl=None, rng=rng); cen = nu_O
        if m is not None:
            for kk in ("sigma_ch", "f_corr", "baseline_med", "S_win", "S_win_err", "S_L", "S_L_err", "snr_L", "snr_win", "detected", "W50", "W50_err", "W50_defined",
                       "W20", "W20_err", "W20_defined", "W50_mc_frac", "snr_peak", "n_blocks", "nN", "f_corr_flag"):
                rec[kk] = m[kk]
            rec["W50_obsframe"] = m["W50"] * (1 + rec["z_HI"]); rec["W20_obsframe"] = m["W20"] * (1 + rec["z_HI"])
            rec["logratio_W50"] = math.log10(m["W50"] / w50c) if np.isfinite(m["W50"]) and m["W50"] > 0 else np.nan
            rec["logratio_S"] = math.log10(m["S_win"] / rec["S_cat"]) if m["S_win"] > 0 else np.nan
            rec["ratio_S"] = m["S_win"] / rec["S_cat"]
        # line-free control (main run only): the O window with the main noise model
        if not MUTATE and side:
            vO_rel = C * (nu_O / nu_g(gs) - 1)
            Lo = np.abs(vO_rel) <= w50c / 2 + 50; Wo = np.abs(vO_rel) <= Vw
            sS_L = DNU * m["sigma_ch"] * math.sqrt(Lo.sum() * m["f_corr"]); sS_W = DNU * m["sigma_ch"] * math.sqrt(Wo.sum() * m["f_corr"])
            rec["off_SNR_L"] = float(DNU * spec[Lo].sum() / sS_L); rec["off_SNR_win"] = float(DNU * spec[Wo].sum() / sS_W)
            # injection: the S1 shape, box width W50_cat, integral S_cat, a point source at the catalogue position, into the real O window
            Snu, w50t, w20t = profile_channels(w50c, nu_O, gs, rec["S_cat"])
            spec_inj = spec + Snu * pt                                               # identical (by linearity) to adding the beam-convolved point source to the cube block and summing the aperture
            mi, _, _, _, _ = measure(gs, spec_inj, nu_O, w50c, excl=Wm_real, rng=np.random.default_rng([302, it, 2]))
            rec.update(inj_W50_true=w50t, inj_W50_rec=mi["W50"], inj_W50_err=mi["W50_err"], inj_W50_defined=mi["W50_defined"], inj_S_rec=mi["S_win"], inj_S_err=mi["S_win_err"],
                       inj_snr_L=mi["snr_L"], inj_detected=mi["detected"])
        # size screen (centred on the pipeline's window)
        if m is not None:
            vv = C * (cen / nu_g(gs) - 1); Lg = gs[np.abs(vv) <= w50c / 2 + 50]
            h = int(math.ceil(5 * theta / PIX))
            M0, ref = m0_box(cubes, ra, dec, int(Lg.min()), int(Lg.max()), h)
            ss = size_screen(M0, ref[0], ref[1], theta)
            rec["extent_beams"] = ss.get("beams_across", np.nan); rec["extent_deconv_arcsec"] = ss.get("extent_deconv_arcsec", np.nan)
            rec["fwhm_eq_arcsec"] = ss.get("fwhm_eq_arcsec", np.nan); rec["fp_touches_box_edge"] = int(bool(ss.get("touches_box_edge", False)))
            rec["RC_capable"] = 0
            if m["detected"] and np.isfinite(rec["extent_beams"]) and rec["extent_beams"] >= 6:
                k = ref[2]; Wg2 = gs[np.abs(vv) <= Vw]; Ng = gs[(np.abs(vv) > Vw + 100) & (np.abs(vv) <= 3 * Vw + 1100)]
                if Ng.size == 0: Ng = Wg2
                ga, gb = int(min(Wg2.min(), Ng.min())), int(max(Wg2.max(), Ng.max()))
                gsel = np.arange(ga, gb + 1); gsel = gsel[owner(gsel) == k]
                blk = read_box(cubes[k], int(gsel[0] - 1000 * k), int(gsel[-1] - 1000 * k), ref[3], ref[4], h)
                vb = C * (cen / nu_g(gsel) - 1)
                pv = pv_extract(blk, vb, A_g[gsel], np.abs(vb) <= Vw, (np.abs(vb) > Vw + 100) & (np.abs(vb) <= 3 * Vw + 1100), ss["centroid_box"][0], ss["centroid_box"][1], ss["axis"], theta / PIX)
                rec["PV"] = pv; rec["RC_capable"] = int(pv["n_pos"] >= 3 and pv["n_neg"] >= 3 and m["snr_L"] >= 10 and np.isfinite(pv["rho"]) and abs(pv["rho"]) >= 0.8)
        recs.append(rec)
        if (it + 1) % 25 == 0: P(f"  ... {it + 1}/{len(targets)} measured ({time.time() - T0:.0f} s)")

    df = pd.DataFrame(recs)
    samp_df = df[df.in_sample == 1]; prim = df[df.primary == 1]
    P(f"\nmeasured {len(df)} (sample {len(samp_df)} + controls T1, T3); flags in the sample: BEAMFLAG {int(samp_df.BEAMFLAG.sum())}, STITCH {int(samp_df.STITCH.sum())}, "
      f"EDGE {int(samp_df.EDGE.sum())}, NAN {int(samp_df.NAN.sum())}, TRUNC {int(samp_df.TRUNC.sum())}, NBFLAG {int(samp_df.NBFLAG.sum())}; O undefined {int((samp_df.O_side == 0).sum())}; primary set {len(prim)}")
    P(f"noise: median sigma_ch {np.nanmedian(prim.sigma_ch) * 1e3:.3f} mJy per channel in the aperture (range {np.nanmin(prim.sigma_ch) * 1e3:.3f}-{np.nanmax(prim.sigma_ch) * 1e3:.3f}); "
      f"f_corr median {np.nanmedian(prim.f_corr):.3f} (range {np.nanmin(prim.f_corr):.3f}-{np.nanmax(prim.f_corr):.3f}); f_corr flagged {int(prim.f_corr_flag.sum())}; "
      f"baseline median / sigma_ch: median {np.nanmedian(prim.baseline_med / prim.sigma_ch):+.3f}")
    NUM["counts"] = dict(n_measured=len(df), n_sample=len(samp_df), n_primary=len(prim), BEAMFLAG=int(samp_df.BEAMFLAG.sum()), STITCH=int(samp_df.STITCH.sum()), EDGE=int(samp_df.EDGE.sum()),
                         NAN=int(samp_df.NAN.sum()), TRUNC=int(samp_df.TRUNC.sum()), NBFLAG=int(samp_df.NBFLAG.sum()), O_undefined=int((samp_df.O_side == 0).sum()))
    NUM["noise"] = dict(sigma_ch_median_mJy=float(np.nanmedian(prim.sigma_ch) * 1e3), f_corr_median=float(np.nanmedian(prim.f_corr)), f_corr_min=float(np.nanmin(prim.f_corr)), f_corr_max=float(np.nanmax(prim.f_corr)))

    def robust(x):
        x = np.asarray(x, float); x = x[np.isfinite(x)]
        return dict(n=int(x.size), median=float(np.median(x)) if x.size else np.nan, robust_scatter=mad_sigma(x), mean=float(np.mean(x)) if x.size else np.nan, std=float(np.std(x, ddof=1)) if x.size > 1 else np.nan)

    t1 = df[df.ID == T1_ID].iloc[0]; t2 = df[df.ID == T2_ID].iloc[0]; t3 = df[df.ID == T3_ID].iloc[0]
    if not MUTATE:
        ndet = int(prim.detected.sum()); nwd = int(prim.W50_defined.sum())
        P(f"\n== Measurement (primary set {len(prim)}) ==")
        P(f"detected (S/N_L >= 5): {ndet}; width-defined (W50): {nwd}; W20 defined: {int(prim.W20_defined.sum())}; MC-unstable W50 (defined fraction < 0.5) among width-defined: {int((prim[prim.W50_defined].W50_mc_frac < 0.5).sum())}")
        P(f"S/N_L: median {np.nanmedian(prim.snr_L):.2f}, quartiles {np.nanpercentile(prim.snr_L, 25):.2f}/{np.nanpercentile(prim.snr_L, 75):.2f}; catalogue SNR_3D median {np.nanmedian(prim.SNR_3D_cat):.2f}; Spearman(S/N_L, SNR_3D) {spearmanr(prim.snr_L, prim.SNR_3D_cat, nan_policy='omit')[0]:.3f}")
        wd = prim[prim.W50_defined]
        RW = robust(wd.logratio_W50); sW = RW["robust_scatter"]
        outW = wd[np.abs(wd.logratio_W50 - RW["median"]) > 3 * sW]
        pullW = (wd.W50 - wd.W50_cat) / np.sqrt(wd.W50_err ** 2 + wd.W50_cat_err ** 2); poutW = wd[np.abs(pullW) > 3]
        P(f"\nWIDTHS (W50_ours / W50_cat, rest-frame ours), n = {RW['n']}: median log ratio {RW['median']:+.4f} dex (ratio {10 ** RW['median']:.3f}), robust scatter {sW:.4f} dex, mean {RW['mean']:+.4f}, std {RW['std']:.4f}")
        P(f"  outliers beyond 3 robust sigma: {len(outW)}: {[(a, round(b, 1), c) for a, b, c in zip(outW.ID, outW.W50, outW.W50_cat)]}")
        P(f"  pull outliers |W50 - W50_cat| > 3 sqrt(err^2 + err_cat^2): {len(poutW)} of {len(wd)} ({100 * len(poutW) / max(len(wd), 1):.1f} %); median |pull| {np.nanmedian(np.abs(pullW)):.2f}; median W50 error ours {np.nanmedian(wd.W50_err):.1f} km/s, catalogue {np.nanmedian(wd.W50_cat_err):.1f}")
        RWn = robust(wd[wd.NBFLAG == 0].logratio_W50)
        rz = spearmanr(wd.z_HI, wd.logratio_W50)[0]; rs = spearmanr(wd.snr_L, wd.logratio_W50)[0]
        P(f"  secondary: without NBFLAG n = {RWn['n']}, median {RWn['median']:+.4f}, scatter {RWn['robust_scatter']:.4f}; Spearman(R_W, z) {rz:+.3f}, Spearman(R_W, S/N_L) {rs:+.3f}; "
          f"observed-frame (1+z) variant median {np.nanmedian(np.log10(wd.W50_obsframe / wd.W50_cat)):+.4f} dex")
        P(f"  W20 (no catalogue W20): median W20/W50 ours {np.nanmedian(wd.W20 / wd.W50):.3f} over {int(wd.W20_defined.sum())} with W20 defined")
        RSall = dict(n=len(prim), median=float(np.nanmedian(prim.ratio_S)), robust_scatter=mad_sigma(prim.ratio_S))
        dd = prim[prim.detected & (prim.S_win > 0)]
        RS = robust(dd.logratio_S); sS = RS["robust_scatter"]
        outS = dd[np.abs(dd.logratio_S - RS["median"]) > 3 * sS]
        pullS = (dd.S_win - dd.S_cat) / np.sqrt(dd.S_win_err ** 2 + dd.S_cat_err ** 2); poutS = dd[np.abs(pullS) > 3]
        P(f"\nFLUXES (S_win / S_cat): all primary n = {RSall['n']}: median ratio {RSall['median']:.3f}, robust scatter {RSall['robust_scatter']:.3f}")
        P(f"  detected with S_win > 0, n = {RS['n']}: median log ratio {RS['median']:+.4f} dex (ratio {10 ** RS['median']:.3f}), robust scatter {sS:.4f}, mean {RS['mean']:+.4f}, std {RS['std']:.4f}")
        P(f"  outliers beyond 3 robust sigma: {len(outS)}: {[(a, round(b, 0), c) for a, b, c in zip(outS.ID, outS.S_win, outS.S_cat)]}")
        P(f"  pull outliers: {len(poutS)} of {len(dd)} ({100 * len(poutS) / max(len(dd), 1):.1f} %); median pull {np.nanmedian(pullS):+.2f}")
        RSL = robust(np.log10(dd.S_L[dd.S_L > 0] / dd.S_cat[dd.S_L > 0])); RSn = robust(dd[dd.NBFLAG == 0].logratio_S)
        P(f"  secondary: S_L median log ratio {RSL['median']:+.4f} (n {RSL['n']}); without NBFLAG {RSn['median']:+.4f} (n {RSn['n']}); Spearman(R_S, z) {spearmanr(dd.z_HI, dd.logratio_S)[0]:+.3f}, Spearman(R_S, S/N_L) {spearmanr(dd.snr_L, dd.logratio_S)[0]:+.3f}")
        nres = int(prim.RC_capable.sum()) if "RC_capable" in prim else 0
        ext = samp_df.extent_beams
        P(f"\nSIZE SCREEN: 3-sigma moment-0 extent (deconvolved, beams) over the sample: median {np.nanmedian(ext):.2f}, max {np.nanmax(ext):.2f} ({samp_df.ID.values[int(np.nanargmax(ext.values))]}); "
          f">= 6 beams: {int((ext >= 6).sum())}; footprint undefined {int(ext.isna().sum())}; footprints touching the box edge {int(samp_df.fp_touches_box_edge.sum())}; T1 {t1.extent_beams:.2f} beams")
        P("\n== Map entries (the only verdict words; findings, not controls) ==")
        wmap = "AGREES" if abs(RW["median"]) <= 0.03 else ("DIFFERS (narrower)" if RW["median"] < 0 else "DIFFERS (wider)")
        smap = "AGREES" if abs(RS["median"]) <= 0.05 else ("DIFFERS (lower)" if RS["median"] < 0 else "DIFFERS (higher)")
        wsc = "CONSISTENT WITH THE ERRORS" if len(poutW) <= 0.10 * len(wd) else "NOT CONSISTENT"
        ssc = "CONSISTENT WITH THE ERRORS" if len(poutS) <= 0.10 * len(dd) else "NOT CONSISTENT"
        P(f"  WIDTH-SCALE {wmap} (median {RW['median']:+.4f} dex, tolerance 0.03); WIDTH-SCATTER {wsc} ({len(poutW)}/{len(wd)} pull outliers)")
        P(f"  FLUX-SCALE {smap} (median {RS['median']:+.4f} dex, tolerance 0.05); FLUX-SCATTER {ssc} ({len(poutS)}/{len(dd)} pull outliers)")
        P(f"  Resolved rotation curves at r1p0: {nres}" + ("" if (ext >= 6).any() else " (no source reaches 6 beams; no PV extraction ran on the data)"))
        NUM["widths"] = dict(RW, outliers=list(outW.ID), pull_outliers=list(poutW.ID), n_pull_out=len(poutW), without_NB=RWn, spearman_z=rz, spearman_snr=rs,
                             obsframe_median=float(np.nanmedian(np.log10(wd.W50_obsframe / wd.W50_cat))), map=wmap, scatter_map=wsc)
        NUM["fluxes"] = dict(all_linear=RSall, detected_log=RS, outliers=list(outS.ID), pull_outliers=list(poutS.ID), n_pull_out=len(poutS), S_L=RSL, without_NB=RSn, map=smap, scatter_map=ssc)
        NUM["detection"] = dict(n_detected=ndet, n_width_defined=nwd, snr_L_median=float(np.nanmedian(prim.snr_L)))
        NUM["size"] = dict(median_beams=float(np.nanmedian(ext)), max_beams=float(np.nanmax(ext)), max_id=samp_df.ID.values[int(np.nanargmax(ext.values))], n_ge6=int((ext >= 6).sum()), resolved=nres, T1_beams=float(t1.extent_beams))

        P("\n== Controls ==")
        po = prim[prim.O_side != 0]; pc = po[po.NB_in_O == 0]
        nfp = int((np.abs(pc.off_SNR_L) >= 5).sum())
        check("C-OFF(a) line-free control: |S/N_L| >= 5 in the offset window for <= 5 % of the primary set (catalogued neighbours inside O not counted)",
              f"{nfp} of {len(pc)} ({100 * nfp / max(len(pc), 1):.1f} %); excluded for a neighbour in O: {len(po) - len(pc)} {list(po.ID[po.NB_in_O == 1])}; O undefined: {len(prim) - len(po)}; listed: {list(pc.ID[np.abs(pc.off_SNR_L) >= 5])}",
              nfp <= 0.05 * len(pc))
        sd = mad_sigma(po.off_SNR_win); mdo = float(np.median(po.off_SNR_win))
        check("C-OFF(b) the robust std of S/N_win in the offset windows is in [0.75, 1.33] (the noise model calibrates)", f"{sd:.3f} (plain std {np.std(po.off_SNR_win):.3f}; S/N_L robust std {mad_sigma(po.off_SNR_L):.3f}; n {len(po)})", 0.75 <= sd <= 1.33)
        check("C-OFF(c) the median S/N_win in the offset windows is within +-0.5 (no baseline offset)", f"{mdo:+.3f}", abs(mdo) <= 0.5)
        NUM["C_OFF"] = dict(n=len(pc), n_false=nfp, robust_std_win=sd, median_win=mdo, robust_std_L=mad_sigma(po.off_SNR_L))
        iw = po[po.inj_W50_defined == True]
        liw = np.log10(iw.inj_W50_rec / iw.inj_W50_true); mi_w = float(np.median(liw))
        isd = po[po.inj_S_rec > 0]; mi_s = float(np.median(np.log10(isd.inj_S_rec / isd.S_cat)))
        pul = (iw.inj_W50_rec - iw.inj_W50_true) / iw.inj_W50_err; psd = mad_sigma(pul)
        check("INJ(a) synthetic HI in real noise: median log10(W50_rec / W50_true) over width-defined injections within +-0.03 dex",
              f"{mi_w:+.4f} dex over {len(iw)} (robust scatter {mad_sigma(liw):.4f}); injection detection {int(po.inj_detected.sum())}/{len(po)} vs main run {int(po.detected.sum())}/{len(po)}", abs(mi_w) <= 0.03)
        check("INJ(b) median log10(S_win,rec / S_injected) within +-0.03 dex", f"{mi_s:+.4f} dex over {len(isd)} (robust scatter {mad_sigma(np.log10(isd.inj_S_rec / isd.S_cat)):.4f})", abs(mi_s) <= 0.03)
        check("INJ(c) the robust std of the width pulls (W50_rec - W50_true)/sigma_W50 is in [0.4, 1.5]", f"{psd:.3f} (median pull {np.median(pul):+.3f})", 0.4 <= psd <= 1.5)
        # injection bias by S/N tercile (reported)
        terc = np.nanpercentile(iw.inj_snr_L, [33.3, 66.7]) if len(iw) >= 6 else [np.nan, np.nan]
        tb = [float(np.median(liw[(iw.inj_snr_L > a) & (iw.inj_snr_L <= b)])) if ((iw.inj_snr_L > a) & (iw.inj_snr_L <= b)).any() else np.nan for a, b in ((-np.inf, terc[0]), (terc[0], terc[1]), (terc[1], np.inf))]
        P(f"  injection width bias by injected S/N_L tercile (edges {terc[0]:.1f}, {terc[1]:.1f}): {[round(x, 4) for x in tb]} dex")
        NUM["INJ"] = dict(n_width=len(iw), median_logW=mi_w, scatter_logW=mad_sigma(liw), n_flux=len(isd), median_logS=mi_s, pull_robust_std=psd, n_detected=int(po.inj_detected.sum()), n_main_detected=int(po.detected.sum()), bias_by_snr_tercile=tb)
        tol = max(25.0, 3 * t1.W50_err) if np.isfinite(t1.W50_err) else 25.0
        check("C-T1 cross-instrument: T1's r1p0 W50 within max(25 km/s, 3 sigma) of CFG300's frozen r0p0 W50",
              f"r1p0 {t1.W50:.1f} +- {t1.W50_err:.1f} km/s (S/N_L {t1.snr_L:.1f}) vs CFG300 r0p0 {w50_cfg300_T1:.1f}; tolerance {tol:.1f}; catalogue 392 +- 12; CFG300 unmasked 374.1 / 380.9",
              bool(np.isfinite(t1.W50) and abs(t1.W50 - w50_cfg300_T1) <= tol))
        P(f"  T1 flux r1p0 / catalogue {t1.ratio_S:.3f} (CFG300: 0.569 masked r0p0, 0.76 unmasked r0p0, 0.85 r0p5); NBFLAG {t1.NBFLAG} ({t1.NB_IDs}); W20 {t1.W20:.1f}; extent {t1.extent_beams:.2f} beams")
        P(f"  T2 (in the sample): W50 {t2.W50:.1f} +- {t2.W50_err:.1f} (CFG300 r0p0 140.5 masked, 145.9 / 157.0 unmasked; catalogue 167 +- 7); flux ratio {t2.ratio_S:.3f} (CFG300 0.235 masked, 0.36 unmasked); S/N_L {t2.snr_L:.1f}")
        P(f"  T3 (control, not golden): W50 {t3.W50:.1f} +- {t3.W50_err:.1f} (CFG300 74.6 masked, 86.3 / 81.9 unmasked; catalogue 101 +- 7); flux ratio {t3.ratio_S:.3f} (CFG300 0.586 masked, 0.71 unmasked); S/N_L {t3.snr_L:.1f}")
        top = prim[prim.detected].sort_values("snr_L", ascending=False).head(20)
        fb = float(np.nanmedian(top.fwhm_eq_arcsec / top.beam_arcsec))
        check("C-BEAM the header beam vs the data: median FWHM_eq / theta over the 20 highest-S/N detections in [0.85, 1.6]", f"{fb:.3f} (range {np.nanmin(top.fwhm_eq_arcsec / top.beam_arcsec):.3f}-{np.nanmax(top.fwhm_eq_arcsec / top.beam_arcsec):.3f})", 0.85 <= fb <= 1.6)
        NUM["C_T1"] = dict(W50=float(t1.W50), W50_err=float(t1.W50_err), cfg300=w50_cfg300_T1, tol=tol, ratio_S=float(t1.ratio_S), snr_L=float(t1.snr_L))
        NUM["T2"] = dict(W50=float(t2.W50), W50_err=float(t2.W50_err), ratio_S=float(t2.ratio_S), snr_L=float(t2.snr_L)); NUM["T3"] = dict(W50=float(t3.W50), W50_err=float(t3.W50_err), ratio_S=float(t3.ratio_S), snr_L=float(t3.snr_L))
        NUM["C_BEAM"] = fb
        # hand estimates
        P("\n== Hand estimates (frozen; scored as they fall) ==")
        q = float(np.nanmedian(prim.ratio_S)); rw = 10 ** RW["median"]
        he = dict(HE1=90 <= ndet <= 175, HE2=0.70 <= q <= 1.10, HE3=0.85 <= rw <= 1.05, HE4=int((ext >= 6).sum()) == 0,
                  HE5=None, HE6=bool(np.isfinite(t1.W50) and abs(t1.W50 - w50_cfg300_T1) <= tol and 340 <= t1.W50 <= 440), HE7=float(np.nanmax(ext)) <= 4)
        ctrl = {n: o for n, o in CHK}
        he["HE5"] = all(ctrl.get(n, False) for n in ctrl if n.startswith(("C-OFF", "INJ", "C-BEAM")))
        for kk, txt in (("HE1", f"detected {ndet} in 90-175"), ("HE2", f"median S_win/S_cat {q:.3f} in 0.70-1.10"), ("HE3", f"median W50 ratio {rw:.3f} in 0.85-1.05"),
                        ("HE4", f"sources >= 6 beams: {int((ext >= 6).sum())} (expected 0)"), ("HE5", "C-OFF, INJ, C-BEAM pass (M1-M3 scored in the MUTATE run)"),
                        ("HE6", f"C-T1 passes and T1 W50 {t1.W50:.1f} in 340-440"), ("HE7", f"largest extent {np.nanmax(ext):.2f} beams <= 4")):
            P(f"  {kk} ({txt}): {'hit' if he[kk] else 'MISS (kept as it falls)'}")
        NUM["hand_estimates"] = he
    else:
        pm = prim[prim.O_side != 0]
        nwd = int(pm.W50_defined.sum()); ndet = int(pm.detected.sum())
        P(f"\n== MUTATE=1: the whole pipeline centred on the off-line window O (primary set with O defined: {len(pm)}) ==")
        P(f"S/N_L in the shifted window: median {np.nanmedian(pm.snr_L):+.3f}, robust std {mad_sigma(pm.snr_L):.3f}; W50 values returned (any S/N) {int(np.isfinite(pm.W50).sum())}")
        check("M1 width-defined in the shifted window for <= 5 % of the primary set (the widths collapse)", f"{nwd} of {len(pm)} ({100 * nwd / max(len(pm), 1):.1f} %): {list(pm.ID[pm.W50_defined == True])}", nwd <= 0.05 * len(pm))
        check("M2 detected (S/N_L >= 5) in the shifted window for <= 5 % of the primary set", f"{ndet} of {len(pm)} ({100 * ndet / max(len(pm), 1):.1f} %)", ndet <= 0.05 * len(pm))
        tol = max(25.0, 3 * t1.W50_err) if np.isfinite(t1.W50_err) else 25.0
        collapsed = (not bool(t1.W50_defined)) or (not np.isfinite(t1.W50)) or abs(t1.W50 - w50_cfg300_T1) > tol
        check("M3 T1's width collapses in the shifted window (undefined, or outside the C-T1 tolerance)", f"W50 {fnum(t1.W50, '{:.1f}')} (defined {bool(t1.W50_defined)}, S/N_L {t1.snr_L:.2f}) vs CFG300 {w50_cfg300_T1:.1f}, tolerance {tol:.1f}", collapsed)
        NUM["MUTATE"] = dict(n=len(pm), n_width_defined=nwd, n_detected=ndet, snr_L_median=float(np.nanmedian(pm.snr_L)), snr_L_robust_std=mad_sigma(pm.snr_L), T1_W50=float(t1.W50) if np.isfinite(t1.W50) else None, T1_snr_L=float(t1.snr_L))

    # outputs
    cols = ["ID", "RA_deg", "Dec_deg", "z_HI", "freq_MHz", "in_sample", "primary", "subcubes", "beam_arcsec", "R_ap_arcsec", "n_ap_pix", "V_w_kms", "BEAMFLAG", "STITCH", "EDGE", "NAN", "TRUNC", "NBFLAG", "NB_IDs",
            "sigma_ch", "f_corr", "baseline_med", "S_win", "S_win_err", "S_L", "S_L_err", "snr_L", "snr_win", "detected", "W50", "W50_err", "W50_defined", "W50_mc_frac", "W20", "W20_err", "W20_defined",
            "W50_obsframe", "W20_obsframe", "snr_peak", "W50_cat", "W50_cat_err", "S_cat", "S_cat_err", "SNR_3D_cat", "log_M_HI_cat", "incl_deg_cat", "logratio_W50", "ratio_S", "logratio_S",
            "extent_beams", "extent_deconv_arcsec", "fwhm_eq_arcsec", "RC_capable", "O_side", "NB_in_O", "off_SNR_L", "off_SNR_win", "inj_W50_true", "inj_W50_rec", "inj_W50_err", "inj_W50_defined", "inj_S_rec", "inj_S_err", "inj_snr_L", "inj_detected"]
    cols = [c for c in cols if c in df.columns]
    o = df[cols].copy()
    for c in ("sigma_ch", "baseline_med"): o[c] = o[c] * 1e3
    o = o.rename(columns={"sigma_ch": "sigma_ch_mJy", "baseline_med": "baseline_med_mJy", "S_win": "S_win_Jy_Hz", "S_win_err": "S_win_err_Jy_Hz", "S_L": "S_L_Jy_Hz", "S_L_err": "S_L_err_Jy_Hz",
                          "W50": "W50_rest_kms", "W50_err": "W50_err_kms", "W20": "W20_rest_kms", "W20_err": "W20_err_kms", "W50_obsframe": "W50_obsframe_kms", "W20_obsframe": "W20_obsframe_kms"})
    o.to_csv(CSV, index=False, float_format="%.10g")
    npass = sum(ok for _, ok in CHK)
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1 << 20 if sys.platform == "darwin" else 1 << 10)
    P(f"\nper-galaxy CSV: {os.path.basename(CSV)} ({len(o)} rows); peak resident memory {usage:.0f} MB")
    P(f"\n{npass}/{len(CHK)} checks pass   ({time.time() - T0:.0f} s)")
    with open(OUT + ".out", "w") as f: f.write("\n".join(LOG) + "\n")
    def clean(x):
        if isinstance(x, dict): return {str(k): clean(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)): return [clean(v) for v in x]
        if isinstance(x, (np.bool_,)): return bool(x)
        if isinstance(x, (np.integer,)): return int(x)
        if isinstance(x, (np.floating, float)): return None if not np.isfinite(x) else float(x)
        return x
    pvs = {r["ID"]: r["PV"] for r in recs if "PV" in r}
    with open(OUT + "_results.json", "w") as f:
        json.dump(clean(dict(lane="CFG302", frozen_criteria="7d317dd4f", mutate=MUTATE, cube_folder=DATA_REL, checks=[dict(name=n, ok=o) for n, o in CHK],
                             n_pass=npass, n_checks=len(CHK), numbers=NUM, pv=pvs)), f, indent=1)


if __name__ == "__main__":
    main()
