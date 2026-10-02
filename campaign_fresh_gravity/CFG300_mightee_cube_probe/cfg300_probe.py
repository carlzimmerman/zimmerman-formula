#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG300 -- the MIGHTEE-HI DR1 cube probe: can resolved rotation curves be extracted from the L2 cubes at z 0.02-0.09, or only HI widths?  Three targets (the paper's public example rows), r0p0 and r0p5 cutouts by HTTP range requests.

Criteria frozen and committed before any cube voxel was read: campaign_fresh_gravity/CFG300_mightee_cube_probe/FROZEN_CRITERIA.md (d14e5082a) (+ the pre-run addendum on MUTATE=1 in FROZEN_CRITERIA_ADDENDUM_1.md).
  STAGE=S   the SYNTHETIC SELFTEST of the analysis (a fabricated rotating disc and a noise-only cube); no archive access.
  STAGE=F   the fetch: headers + one contiguous row-block per channel plane through data_assembly/fetch_range_logged.py (SARAO only; cumulative hard cap 10 GB); one run; cutouts saved OUTSIDE the repository.
  STAGE=B   the analysis of the local cutouts; STAGE=B MUTATE=1 (the line window shifted by +(W50 + 150) km/s) or MUTATE=2 (the velocity axis reversed): separate outputs.
This is a data-feasibility probe, not an a0 measurement: at z <= 0.093 the rival differs from FLAT by <= 4.5 %.  kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, json, math, time
sys.dont_write_bytecode = True
import numpy as np
from scipy import ndimage as ndi
from scipy.stats import spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE); REPO = os.path.dirname(CFG)
EXT = os.path.join(os.path.dirname(REPO), "_external_data", "mightee_probe")                      # outside the repository
STAGE = os.environ.get("STAGE", "").strip().upper(); MUTATE = int(os.environ.get("MUTATE", "0"))
assert STAGE in ("S", "F", "B"), "set STAGE=S, STAGE=F or STAGE=B"
assert not (MUTATE and STAGE != "B"), "MUTATE applies to stage B"
SFX = {"S": "_SELFTEST", "F": "_fetch", "B": "_stageB" + (f"_MUTATE{MUTATE}" if MUTATE else "")}[STAGE]
LOG, CHK, NUM = [], [], {}
C_KMS = 299792.458; PIX = 2.0                                                                    # arcsec per pixel (r0p0, r0p5)
BEAM = {"r0p0": 12.27, "r0p5": 16.33}                                                            # medians of the per-channel beam tables (step 0, bdbf6c282)
BASE = "https://archive-gw-1.kat.ac.za/public/repository/10.48479/jkc0-g916/data/"


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok, load_bearing=True):
    CHK.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


# the three targets fixed by rule from the paper's public example rows (arXiv:2605.28731 Table 3): SNR_3D >= 10, the three largest log M_HI
TARGETS = {
    "T1": dict(id="MGTH_J100357.1+022505", ra=150.988, dec=2.418, nu_mhz=1383.623, z=0.0266, logMHI=9.93, snr3d=19.1, w50=392.0, w50_err=12.0, incl=75.0, S_cat=12782.92, S_cat_err=672.47, sub="3001-4055", half=150.0, weights=["r0p0", "r0p5"], rhi_pred_arcsec=100.0),
    "T2": dict(id="MGTH_J100256.4+023440", ra=150.735, dec=2.578, nu_mhz=1360.267, z=0.0442, logMHI=9.45, snr3d=13.4, w50=167.0, w50_err=7.0, incl=44.0, S_cat=1471.09, S_cat_err=109.80, sub="2001-3055", half=100.0, weights=["r0p0"], rhi_pred_arcsec=35.0),
    "T3": dict(id="MGTH_J095951.4+014224", ra=149.964, dec=1.707, nu_mhz=1385.660, z=0.0251, logMHI=8.81, snr3d=16.0, w50=101.0, w50_err=7.0, incl=61.0, S_cat=1074.15, S_cat_err=68.53, sub="3001-4055", half=100.0, weights=["r0p0"], rhi_pred_arcsec=29.0)}


# ================================================================== the analysis (frozen in the criteria, section 3)
def mad_sigma(a):
    a = a[np.isfinite(a)]
    return 1.4826 * np.median(np.abs(a - np.median(a))) if a.size else float("nan")


def analyze(cube, freq, nu_c, w50_cat, beam, xc, yc, r_in_px, shift_kms=0.0, reverse=False):
    """cube (nchan, ny, nx) in Jy/beam, freq ascending [Hz]; nu_c [Hz] the catalogue frequency; (xc, yc) the target in cube pixel coordinates; beam [arcsec]."""
    nch, ny, nx = cube.shape
    cube = np.nan_to_num(cube)
    if reverse: cube = cube[::-1].copy()                                                         # velocity axis reversed (frequencies kept)
    v = C_KMS * (nu_c - freq) / nu_c                                                              # radio velocity, + = receding (decreases with channel index)
    yy, xx = np.mgrid[0:ny, 0:nx]; rr = np.hypot(xx - xc, yy - yc); ring = rr > r_in_px
    sig_c = np.array([mad_sigma(cube[i][ring]) for i in range(nch)]); sig_med = float(np.median(sig_c[sig_c > 0]))
    sm = ndi.uniform_filter1d(cube, size=3, axis=0, mode="nearest")
    sig_s = np.array([mad_sigma(sm[i][ring]) for i in range(nch)]); sigma_s = float(np.median(sig_s[sig_s > 0]))
    snr = sm / sigma_s
    win = np.abs(v - shift_kms) <= (w50_cat / 2 + 50.0); free = np.abs(v) > (w50_cat / 2 + 80.0)
    r3 = 3 * beam / PIX
    cand = (snr >= 3) & win[:, None, None]
    seed = (snr >= 5) & win[:, None, None] & (rr <= r3)[None]
    lab, nl = ndi.label(cand, structure=ndi.generate_binary_structure(3, 1))
    keep = np.unique(lab[seed]); keep = keep[keep > 0]
    out = dict(sigma_chan=sig_med, sigma_smooth=sigma_s, n_free_seeds=int(((snr >= 5) & free[:, None, None] & (rr <= r3)[None]).sum()), n_ring_seeds=int(((snr >= 5) & win[:, None, None] & ring[None]).sum()), n_labels=int(nl), n_seed_labels=int(keep.size))
    if keep.size == 0:
        out.update(detected=False); return out
    mask = np.isin(lab, keep)
    nbeam = 1.1331 * (beam / PIX) ** 2; dnu = float(abs(freq[1] - freq[0]))
    I = np.where(mask, cube, 0.0); M0 = I.sum(0) * dnu; fp = mask.any(0)
    nvox = int(mask.sum()); S_int = float(M0.sum() / nbeam); snr_int = float(I.sum() / (sig_med * math.sqrt(nvox * nbeam)))
    if fp.sum() < 2 * nbeam:
        out.update(detected=False, n_footprint_px=int(fp.sum())); return out
    ys, xs = np.nonzero(fp); w = M0[ys, xs].clip(min=0)
    xcen = float((w * xs).sum() / w.sum()); ycen = float((w * ys).sum() / w.sum())
    cov = np.cov(np.vstack([xs - xcen, ys - ycen])); ev, evec = np.linalg.eigh(cov); u = evec[:, 1]                    # major axis (unit vector in pixel coordinates)
    proj = (xs - xcen) * u[0] + (ys - ycen) * u[1]; L_arcsec = float((proj.max() - proj.min() + 1) * PIX)
    D_dec = math.sqrt(max(L_arcsec ** 2 - beam ** 2, 0.0)); n_beams = D_dec / beam
    spec = I.sum((1, 2)); sps = ndi.uniform_filter1d(spec, size=3, mode="nearest"); pk = int(np.argmax(sps)); half = 0.5 * sps[pk]
    above = np.nonzero(sps >= half)[0]; lo, hi = int(above.min()), int(above.max())
    def cross(i0, i1):                                                                                           # linear interpolation of the 50 % crossing between channels i0 (below) and i1 (above)
        y0, y1 = sps[i0], sps[i1]; t = (half - y0) / (y1 - y0) if y1 != y0 else 0.5
        return v[i0] + t * (v[i1] - v[i0])
    va = cross(lo - 1, lo) if lo > 0 else v[lo]; vb = cross(hi + 1, hi) if hi < nch - 1 else v[hi]
    w50 = float(abs(va - vb))
    perp_half = beam / PIX / 2.0; binw = beam / PIX
    vox = np.argwhere(mask); iv = I[mask]; vv = v[vox[:, 0]]
    dx = vox[:, 2] - xcen; dy = vox[:, 1] - ycen
    along = dx * u[0] + dy * u[1]; perp = -dx * u[1] + dy * u[0]; instrip = np.abs(perp) <= perp_half
    kb = np.floor(along / binw + 0.5).astype(int); pts = []
    for k in np.unique(kb[instrip]):
        sel = instrip & (kb == k)
        if sel.sum() >= 2 * nbeam and iv[sel].sum() > 0: pts.append((int(k), float((iv[sel] * vv[sel]).sum() / iv[sel].sum())))
    npos = sum(1 for k, _ in pts if k > 0); nneg = sum(1 for k, _ in pts if k < 0)
    rho = float(spearmanr([k for k, _ in pts], [x for _, x in pts])[0]) if len(pts) >= 5 else float("nan")
    cen_sep = float(math.hypot(xcen - xc, ycen - yc) * PIX)
    out.update(detected=True, S_int=S_int, snr_int=snr_int, nvox=nvox, n_footprint_px=int(fp.sum()), centroid_xy=[xcen, ycen], centroid_sep_arcsec=cen_sep, major_axis_pa_deg=float(math.degrees(math.atan2(u[1], u[0]))), extent_arcsec=L_arcsec, extent_deconv_arcsec=D_dec,
               n_beams=n_beams, w50=w50, pv_points=pts, pv_n_pos=npos, pv_n_neg=nneg, pv_rho=rho, v_peak_channel=float(v[pk]))
    out["RC_CAPABLE"] = bool(n_beams >= 6 and snr_int >= 10 and npos >= 3 and nneg >= 3 and np.isfinite(rho) and abs(rho) >= 0.8)
    return out


# ================================================================== STAGE S: the synthetic SELFTEST of the analysis
def synth(extent_fwhm_arcsec, vrot, incl, snr_target, beam, rng, nch=193, n=151, noise=1.0, pa_deg=30.0, dv=5.66):
    """a rotating exponential disc of clouds (flat rotation curve, 10 km/s dispersion), smoothed to the beam, in noise; scaled so that the integrated S/N is about snr_target"""
    Rd = extent_fwhm_arcsec / PIX / 2.0 / 1.678 * 1.0; N = 300000
    R = rng.gamma(2.0, Rd / 2.0, N); R = R[R < 5 * Rd]; phi = rng.uniform(0, 2 * np.pi, R.size)
    xs = R * np.cos(phi); ys = R * np.sin(phi) * math.cos(math.radians(incl))
    pa = math.radians(pa_deg); x = n // 2 + xs * math.cos(pa) - ys * math.sin(pa); y = n // 2 + xs * math.sin(pa) + ys * math.cos(pa)
    vlos = vrot * math.sin(math.radians(incl)) * np.cos(phi) + rng.normal(0, 10.0, R.size)
    ch = nch // 2 - vlos / dv                                                                                       # velocity decreases with channel index (frequency ascending)
    H, _ = np.histogramdd(np.c_[ch, y, x], bins=(np.arange(-0.5, nch, 1.0), np.arange(-0.5, n, 1.0), np.arange(-0.5, n, 1.0)))
    H = ndi.gaussian_filter(H, sigma=(0.6, beam / 2.3548 / PIX, beam / 2.3548 / PIX))
    nbeam = 1.1331 * (beam / PIX) ** 2
    scale = snr_target * noise * math.sqrt((H > 0.1 * H.max()).sum() * nbeam) / H[H > 0.1 * H.max()].sum() if snr_target > 0 else 0.0
    cube = H * scale + rng.normal(0, noise, H.shape)
    freq = 1.38e9 + (np.arange(nch) - nch // 2) * 26125.3
    return cube.astype("f4"), freq


if STAGE == "S":
    rng = np.random.default_rng(300); beam = 12.27; nu_c = 1.38e9 + 0.0
    P(__doc__.split("This is a data")[0].strip()); P("\nSTAGE S  SYNTHETIC SELFTEST (no archive access)")
    cases = [("A large disc: extent 100 arcsec, V sin i 190 km/s, S/N 25", 100.0, 200.0, 70.0, 25.0, True), ("B medium disc: 35 arcsec, S/N 12", 35.0, 150.0, 50.0, 12.0, False),
             ("C small disc: 15 arcsec, S/N 8", 15.0, 100.0, 60.0, 8.0, False), ("D noise only", 0.0, 0.0, 0.0, 0.0, False)]
    res = {}
    for nm, ext, vrot, inc, sn, expect_rc in cases:
        if ext > 0: cube, freq = synth(ext, vrot, inc, sn, beam, rng)
        else: cube, freq = rng.normal(0, 1.0, (193, 151, 151)).astype("f4"), 1.38e9 + (np.arange(193) - 96) * 26125.3
        w50_in = 2 * vrot * math.sin(math.radians(inc)) if ext > 0 else 100.0
        r = analyze(cube, freq, 1.38e9, w50_in, beam, 75, 75, 55 if ext >= 60 else 30)
        r2 = analyze(cube, freq, 1.38e9, w50_in, beam, 75, 75, 55 if ext >= 60 else 30, reverse=True) if r.get("detected") else {}
        res[nm] = dict(case=r, reversed=r2)
        if ext > 0 and r.get("detected"):
            P(f"  {nm}: detected; S/N_int {r['snr_int']:.1f}; extent {r['extent_arcsec']:.0f} arcsec ({r['n_beams']:.1f} beams deconvolved); W50 {r['w50']:.0f} (input {w50_in:.0f}); PV points +{r['pv_n_pos']}/-{r['pv_n_neg']}, rho {r['pv_rho']:.2f}; centroid offset {r['centroid_sep_arcsec']:.1f} arcsec; RC_CAPABLE {r['RC_CAPABLE']}")
        else:
            P(f"  {nm}: " + ("detected" if r.get("detected") else "NO detection") + f"; free-channel seeds {r['n_free_seeds']}, ring seeds {r['n_ring_seeds']}")
    A = res[cases[0][0]]["case"]; Dn = res[cases[3][0]]["case"]; B = res[cases[1][0]]["case"]; C = res[cases[2][0]]["case"]
    check("S1 the large disc is detected, W50 within 30 km/s of the input, the extent within 40 % of the input FWHM-scale 100 arcsec, the centroid within one beam, and it is RC-CAPABLE", f"W50 {A.get('w50')}, extent {A.get('extent_arcsec')}, offset {A.get('centroid_sep_arcsec')}, RC {A.get('RC_CAPABLE')}",
          bool(A.get("detected") and abs(A["w50"] - 2 * 200 * math.sin(math.radians(70))) <= 30 and abs(A["extent_arcsec"] / 100.0 - 1) <= 0.4 and A["centroid_sep_arcsec"] <= 12.27 and A["RC_CAPABLE"]))
    check("S2 the small disc is NOT RC-CAPABLE (detected or not), and the medium disc is not RC-CAPABLE with fewer than 6 deconvolved beams", f"B {B.get('RC_CAPABLE')} (n_beams {B.get('n_beams')}), C {C.get('RC_CAPABLE')}", not C.get("RC_CAPABLE", False) and not (B.get("RC_CAPABLE", False) and B.get("n_beams", 0) < 6))
    check("S3 the noise-only cube has no detection and no 5-sigma seed in the line-free channels", f"detected {Dn.get('detected')}, free seeds {Dn['n_free_seeds']}", not Dn.get("detected") and Dn["n_free_seeds"] == 0)
    Ar = res[cases[0][0]]["reversed"]
    check("S4 MUTATE=2 reactivity on the large disc: reversing the velocity axis flips the sign of the PV correlation and leaves W50, S_int and the extent unchanged", f"rho {A.get('pv_rho', float('nan')):.2f} -> {Ar.get('pv_rho', float('nan')):.2f}; W50 {A.get('w50', float('nan')):.1f} vs {Ar.get('w50', float('nan')):.1f}; S_int {A.get('S_int', float('nan')):.3g} vs {Ar.get('S_int', float('nan')):.3g}",
          bool(Ar.get("detected") and A["pv_rho"] * Ar["pv_rho"] < 0 and abs(A["w50"] - Ar["w50"]) < 1e-6 and abs(A["S_int"] / Ar["S_int"] - 1) < 1e-9 and abs(A["extent_arcsec"] - Ar["extent_arcsec"]) < 1e-9))
    cube, freq = synth(100.0, 200.0, 70.0, 25.0, beam, np.random.default_rng(301))
    sh = analyze(cube, freq, 1.38e9, 2 * 200 * math.sin(math.radians(70)), beam, 75, 75, 55, shift_kms=2 * 200 * math.sin(math.radians(70)) + 150.0)
    check("S5 MUTATE=1 reactivity on the large disc: the line window shifted by +(W50 + 150) km/s finds no detection", f"detected {sh.get('detected')}", not sh.get("detected"))
    NUM["selftest"] = res

# ================================================================== STAGE F: the fetch
if STAGE == "F":
    from astropy.io import fits
    from astropy.wcs import WCS
    sys.path.insert(0, os.path.join(REPO, "data_assembly"))
    import fetch_range_logged as FR
    os.makedirs(EXT, exist_ok=True)
    P(__doc__.split("This is a data")[0].strip()); P("\nSTAGE F  THE FETCH (SARAO only; cumulative cap 10 GB; one run)")
    P(f"ledger before: {json.load(open(FR.LEDGER))}")
    summ = {}
    for tag, t in TARGETS.items():
        for wt in t["weights"]:
            url = BASE + f"MIGHTEE-HI_DR1_L2_{wt}/MIGHTEE-HI_DR1_COSMOS_L2_{wt}_clean_conv_contsub_{t['sub']}.fits"
            b = FR.fetch_range(f"FITS header {tag} {wt} {t['sub']}", url, 0, 28799)
            cards = [b[i:i + 80].decode("ascii", "replace") for i in range(0, len(b), 80)]; end = next(i for i, c in enumerate(cards) if c.startswith("END     "))
            hdr = fits.Header.fromstring("".join(c.ljust(80)[:80] for c in cards[:end + 1]), sep=""); data_start = ((end + 1) * 80 + 2879) // 2880 * 2880
            nx, ny, nc = hdr["NAXIS1"], hdr["NAXIS2"], hdr["NAXIS3"]; assert hdr["BITPIX"] == -32 and hdr.get("BSCALE", 1.0) == 1.0 and hdr.get("BZERO", 0.0) == 0.0 and hdr["NAXIS"] == 4 and hdr["NAXIS4"] == 1
            crv, cdl, crp = hdr["CRVAL3"], hdr["CDELT3"], hdr["CRPIX3"]; assert cdl > 0 and abs(abs(hdr["CDELT1"]) * 3600 - PIX) < 1e-3
            wcs = WCS(hdr, naxis=2); xc, yc = (float(a) for a in wcs.wcs_world2pix(t["ra"], t["dec"], 0)); R = int(round(t["half"] / PIX))
            x0, x1, y0, y1 = int(round(xc)) - R, int(round(xc)) + R, int(round(yc)) - R, int(round(yc)) + R
            assert 0 <= x0 and x1 < nx and 0 <= y0 and y1 < ny, f"{tag}: the box leaves the image"
            nu_c = t["nu_mhz"] * 1e6; dvk = t["w50"] + 150.0; nu_lo, nu_hi = nu_c * (1 - dvk / C_KMS), nu_c * (1 + dvk / C_KMS)
            c_lo = int(math.floor((nu_lo - crv) / cdl + crp - 1)); c_hi = int(math.ceil((nu_hi - crv) / cdl + crp - 1)); assert 0 <= c_lo and c_hi < nc, f"{tag}: the channels leave the sub-cube"
            planes = []; nbytes = 0
            for c in range(c_lo, c_hi + 1):
                s0 = data_start + 4 * (nx * (y0 + ny * c)); e0 = data_start + 4 * (nx * (y1 + ny * c) + nx) - 1
                bb = FR.fetch_range(f"cutout {tag} {wt} ch {c}", url, s0, e0); nbytes += len(bb)
                planes.append(np.frombuffer(bb, dtype=">f4").reshape(y1 - y0 + 1, nx)[:, x0:x1 + 1].astype("f4"))
            cm = (c_lo + c_hi) // 2; s0 = data_start + 4 * (nx * (y0 + ny * cm)); e0 = data_start + 4 * (nx * (y1 + ny * cm) + nx) - 1
            again = FR.fetch_range(f"repeat read {tag} {wt} ch {cm}", url, s0, e0, log=True); c0 = bool(np.array_equal(np.frombuffer(again, dtype=">f4").reshape(y1 - y0 + 1, nx)[:, x0:x1 + 1].astype("f4"), planes[cm - c_lo]))
            cube = np.stack(planes); freq = crv + (np.arange(c_lo, c_hi + 1) - (crp - 1)) * cdl
            celhdr = fits.Header(); [celhdr.append((k, hdr[k])) for k in ("CTYPE1", "CRVAL1", "CDELT1", "CRPIX1", "CTYPE2", "CRVAL2", "CDELT2", "CRPIX2", "EQUINOX", "RADESYS") if k in hdr]
            np.savez_compressed(os.path.join(EXT, f"cfg300_{tag}_{wt}.npz"), cube=cube, freq=freq, x0=x0, y0=y0, xc=xc - x0, yc=yc - y0, c_lo=c_lo, c_hi=c_hi, wcs_header=celhdr.tostring(sep="\n"), tag=tag, weighting=wt)
            summ[f"{tag}_{wt}"] = dict(url_tail=url.split("/data/")[-1], data_start=data_start, nx=nx, ny=ny, nchan_cutout=int(cube.shape[0]), shape=list(cube.shape), c_lo=c_lo, c_hi=c_hi, x_center=xc, y_center=yc, box=[x0, x1, y0, y1],
                                       freq_lo_mhz=float(freq[0] / 1e6), freq_hi_mhz=float(freq[-1] / 1e6), bytes_read=nbytes, repeat_read_identical=c0, finite_fraction=float(np.isfinite(cube).mean()))
            P(f"  {tag} {wt}: cutout {cube.shape} (channels {c_lo}-{c_hi}, {freq[0] / 1e6:.3f}-{freq[-1] / 1e6:.3f} MHz); box x {x0}-{x1}, y {y0}-{y1}; target at ({xc - x0:.1f}, {yc - y0:.1f}); {nbytes / 1e6:.0f} MB read; repeat read identical {c0}; finite {np.isfinite(cube).mean():.4f}")
            check(f"C0 {tag} {wt}: the repeated plane read is byte-identical", f"{c0}", c0)
            ok1 = abs((xc - x0) - R) <= 0.5 and abs((yc - y0) - R) <= 0.5 and freq[0] <= nu_lo + cdl and freq[-1] >= nu_hi - cdl
            check(f"C1 {tag} {wt}: the target pixel is at the cutout centre within a pixel and the channels cover the requested frequency range", f"target ({xc - x0:.2f}, {yc - y0:.2f}) vs {R}; {freq[0] / 1e6:.3f}-{freq[-1] / 1e6:.3f} MHz vs {nu_lo / 1e6:.3f}-{nu_hi / 1e6:.3f}", ok1)
    NUM["fetch"] = summ; P(f"ledger after: {json.load(open(FR.LEDGER))}")

# ================================================================== STAGE B: the analysis of the local cutouts
if STAGE == "B":
    P(__doc__.split("This is a data")[0].strip()); P("\nSTAGE B  THE ANALYSIS" + (f" (MUTATE={MUTATE})" if MUTATE else ""))
    res = {}
    for tag, t in TARGETS.items():
        for wt in t["weights"]:
            z = np.load(os.path.join(EXT, f"cfg300_{tag}_{wt}.npz"), allow_pickle=True)
            cube, freq, xc, yc = z["cube"], z["freq"], float(z["xc"]), float(z["yc"])
            beam = BEAM[wt]; nu_c = t["nu_mhz"] * 1e6; r_in = 50 if tag == "T1" else 30
            shift = (t["w50"] + 150.0) if MUTATE == 1 else 0.0
            r = analyze(cube, freq, nu_c, t["w50"], beam, xc, yc, r_in, shift_kms=shift, reverse=(MUTATE == 2))
            res[f"{tag}_{wt}"] = r
            if r.get("detected"):
                P(f"  {tag} {wt} ({t['id']}): detected; S_int {r['S_int']:.0f} Jy Hz (catalogue {t['S_cat']:.0f} +- {t['S_cat_err']:.0f}); S/N_int {r['snr_int']:.1f}; extent {r['extent_arcsec']:.0f} arcsec = {r['extent_deconv_arcsec']:.0f} deconvolved = {r['n_beams']:.1f} beams (beam {beam} arcsec); W50 {r['w50']:.0f} km/s (catalogue {t['w50']:.0f} +- {t['w50_err']:.0f}); centroid offset {r['centroid_sep_arcsec']:.1f} arcsec; "
                  f"PV points +{r['pv_n_pos']} / -{r['pv_n_neg']}, rho {r['pv_rho']:.2f}; sigma/channel {r['sigma_chan'] * 1e3:.3f} mJy/beam; seeds in free channels {r['n_free_seeds']}, in the ring {r['n_ring_seeds']}; RC_CAPABLE {r['RC_CAPABLE']}")
            else:
                P(f"  {tag} {wt} ({t['id']}): NO detection (seed labels {r['n_seed_labels']}); sigma/channel {r['sigma_chan'] * 1e3:.3f} mJy/beam; seeds in free channels {r['n_free_seeds']}, in the ring {r['n_ring_seeds']}")
    NUM["results"] = res
    P("\nCONTROLS AND VERDICTS")
    if MUTATE == 1:
        check("M1 MUTATE=1 (reactivity): with the line window shifted by +(W50 + 150) km/s no target has a >= 5 sigma detection", f"detected {[k for k, v in res.items() if v.get('detected')]}", not any(v.get("detected") for v in res.values()))
    elif MUTATE == 2:
        main = json.load(open(os.path.join(HERE, "cfg300_stageB_results.json")))["numbers"]["results"]
        ok = all(((not main[k].get("detected")) and (not v.get("detected"))) or (main[k].get("detected") and v.get("detected") and abs(main[k]["w50"] - v["w50"]) < 1e-6 and abs(main[k]["S_int"] / v["S_int"] - 1) < 1e-9 and abs(main[k]["extent_arcsec"] - v["extent_arcsec"]) < 1e-9
                                                            and (main[k].get("pv_rho") is None or v.get("pv_rho") is None or not np.isfinite(v["pv_rho"]) or main[k]["pv_rho"] * v["pv_rho"] < 0 or main[k]["pv_rho"] == 0)) for k, v in res.items())
        check("M2 MUTATE=2 (velocity axis reversed): W50, S_int and the extent are unchanged and the PV correlation changes sign for every detection", f"{[(k, main[k].get('pv_rho'), v.get('pv_rho')) for k, v in res.items() if v.get('detected')]}", ok)
    else:
        verdict = {}
        for tag, t in TARGETS.items():
            for wt in t["weights"]:
                r = res[f"{tag}_{wt}"]; k = f"{tag}_{wt}"
                if r.get("detected"):
                    c2 = abs(r["S_int"] / t["S_cat"] - 1) <= 0.25; c3 = r["centroid_sep_arcsec"] <= BEAM[wt]; c4 = abs(r["w50"] - t["w50"]) <= max(3 * t["w50_err"], 25.0); c5 = r["n_free_seeds"] == 0 and r["n_ring_seeds"] == 0
                    check(f"C2 {k}: S_int within 25 % of the catalogue S_HI", f"ratio {r['S_int'] / t['S_cat']:.3f}", c2); check(f"C3 {k}: the HI centroid is within one beam of the catalogue position", f"{r['centroid_sep_arcsec']:.1f} arcsec vs {BEAM[wt]}", c3)
                    check(f"C4 {k}: W50 within max(3 sigma_cat, 25 km/s) of the catalogue", f"{r['w50']:.0f} vs {t['w50']:.0f} +- {t['w50_err']:.0f}", c4); check(f"C5 {k}: no 5-sigma seed in the line-free channels or the off-source ring", f"{r['n_free_seeds']} / {r['n_ring_seeds']}", c5)
                    verdict[k] = dict(RC_CAPABLE=r["RC_CAPABLE"], WIDTH_USABLE=bool(r["snr_int"] >= 5 and c4))
                else:
                    verdict[k] = dict(RC_CAPABLE=False, WIDTH_USABLE=False)
                    check(f"C2-C5 {k}: no detection (a result; the controls on the source are not evaluated)", "no seed", False, load_bearing=False)
        NUM["verdict"] = verdict
        P("\nPROBE VERDICTS (frozen map; no verdict words)")
        for k, vd in verdict.items(): P(f"  {k}: RC_CAPABLE {vd['RC_CAPABLE']}; WIDTH_USABLE {vd['WIDTH_USABLE']}")
        P(f"  resolved rotation curves: {sum(1 for k, vd in verdict.items() if k.endswith('r0p0') and vd['RC_CAPABLE'])} of 3 targets at r0p0; widths: {sum(1 for k, vd in verdict.items() if k.endswith('r0p0') and vd['WIDTH_USABLE'])} of 3")
        he = {}
        g = lambda k, f: res[k].get(f, float("nan"))
        he["HE1"] = bool(3 <= g("T1_r0p0", "n_beams") <= 10 and 1 <= g("T2_r0p0", "n_beams") <= 4 and 0.5 <= g("T3_r0p0", "n_beams") <= 3)
        he["HE2"] = bool(8 <= g("T1_r0p0", "snr_int") <= 40 and 5 <= g("T2_r0p0", "snr_int") <= 30 and 5 <= g("T3_r0p0", "snr_int") <= 30 and 1.0 <= g("T1_r0p5", "snr_int") / g("T1_r0p0", "snr_int") <= 1.8)
        he["HE3"] = bool(340 <= g("T1_r0p0", "w50") <= 440 and 130 <= g("T2_r0p0", "w50") <= 210 and 70 <= g("T3_r0p0", "w50") <= 140)
        he["HE4"] = bool(verdict["T1_r0p0"]["RC_CAPABLE"] and not verdict["T2_r0p0"]["RC_CAPABLE"] and not verdict["T3_r0p0"]["RC_CAPABLE"] and all(verdict[f"{k}_r0p0"]["WIDTH_USABLE"] for k in ("T1", "T2", "T3")))
        he["HE5"] = bool(all(res[f"{k}_r0p0"].get("detected") and abs(res[f"{k}_r0p0"]["S_int"] / TARGETS[k]["S_cat"] - 1) <= 0.25 for k in ("T1", "T2", "T3")))
        he["HE6"] = bool(all(res[f"{k}_r0p0"].get("detected") and res[f"{k}_r0p0"]["centroid_sep_arcsec"] <= BEAM["r0p0"] and res[f"{k}_r0p0"]["n_free_seeds"] == 0 and res[f"{k}_r0p0"]["n_ring_seeds"] == 0 for k in ("T1", "T2", "T3")))
        NUM["hand_estimates"] = he
        P("\nHAND ESTIMATES (frozen in the criteria, section 5)")
        P(f"    HE1 (extent in beams at r0p0: T1 3-10, T2 1-4, T3 0.5-3): {'hit' if he['HE1'] else 'MISS (kept as it falls)'}  (" + ", ".join(f"{k} {g(k + '_r0p0', 'n_beams'):.2f}" for k in ("T1", "T2", "T3")) + ")")
        P(f"    HE2 (integrated S/N at r0p0: T1 8-40, T2 5-30, T3 5-30; T1 r0p5/r0p0 1.0-1.8): {'hit' if he['HE2'] else 'MISS (kept as it falls)'}")
        P(f"    HE3 (W50: T1 340-440, T2 130-210, T3 70-140): {'hit' if he['HE3'] else 'MISS (kept as it falls)'}")
        P(f"    HE4 (T1 RC-CAPABLE, T2 and T3 not, all three width-usable): {'hit' if he['HE4'] else 'MISS (kept as it falls)'}")
        P(f"    HE5 (C2 passes for all three): {'hit' if he['HE5'] else 'MISS (kept as it falls)'};  HE6 (C3 and C5 pass for all three): {'hit' if he['HE6'] else 'MISS (kept as it falls)'}")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - T0:.0f} s)")
open(os.path.join(HERE, f"cfg300{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>").replace(os.path.dirname(REPO), "<repo-parent>") + "\n")


def _jc(o):
    if isinstance(o, dict): return {str(k): _jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_jc(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o


json.dump(dict(stage=STAGE, mutate=MUTATE, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=_jc(NUM)), open(os.path.join(HERE, f"cfg300{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
