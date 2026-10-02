#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG300 -- POST HOC diagnostics of the failed controls (written AFTER the first stage-B run, a5018f01c; dated 2026-10-02; NOT frozen; no verdict of the frozen map is changed by anything here).

Question: the first run failed C2 (integrated flux vs the catalogue S_HI: 0.569 / 0.756 / 0.235 / 0.586), C4 for T2 and T3 (W50 26 km/s narrower than the catalogue) and C5 (>= 5 sigma seeds in the line-free channels / the off-source ring for T1).
Are these (a) the frozen detection mask's S/N threshold, (b) real extra emission or non-Gaussian noise, or (c) a flux-scale question that stays OPEN?  No archive access: the four local cutouts only.

Everything below is fixed BEFORE it is computed (the rules are in this docstring and in the printed header):
  PH0  same-chain control: the mask rebuilt here (the frozen lines of analyze(), copied verbatim) reproduces the first run's nvox, S_int, W50 and n_beams (1e-6 relative).
  D1   the C5 seeds: counts of >= 5 sigma and <= -5 sigma voxels in the same two regions C5 used (free channels within three beams; the ring in the line window) and over the whole line-free part of the cube; connected clumps of the positive seeds with their offsets (arcsec) and velocities.
       Reading rule: positive and negative counts within a factor of 2 of each other -> heavy-tailed (non-Gaussian) noise; positives >> negatives in compact clumps -> real emission or artefact at that position/velocity; neither is a verdict on the frozen control (C5 stays FAIL).
  D2   the curve of growth of the UNMASKED circular-aperture flux in the frozen line window |v| <= W50_cat/2 + 50 km/s, centred on the catalogue position, for radii R = f x (frozen mask major axis / 2), f in {0.5, 0.75, 1, 1.25, 1.5, 2} (only apertures that fit inside the cutout), with the noise-propagated sigma_S = sigma_med dnu sqrt(N_vox / n_beam).
       Reading rule: if S_ap(R = 1.0 or 1.5 x R_mask) is within 25 % of S_cat -> the C2 deficit is the mask threshold; if it stays below 0.75 S_cat by more than 2 sigma_S -> the flux-scale question stays OPEN (not resolved here).
  D3   W50 from the unmasked aperture spectrum (R = 1.0 and 1.5 x R_mask; 3-channel boxcar; 50 % of the smoothed peak; the frozen interpolation) and its noise scatter (200 noise realisations at the aperture-spectrum sigma, seed 3001).
       Reading rule: within max(3 sigma_cat, 25 km/s) of the catalogue -> the narrow W50 is a mask effect; otherwise it is not.
  NULL control (can fail): the unmasked aperture flux per channel in the line-free channels (|v| > W50/2 + 80) is consistent with zero: |z| < 3 with z = mean / (sigma_ap / sqrt(n_free)), sigma_ap = sigma_med sqrt(N_pix n_beam).

kappa = 1/2 is FITTED.  A data-feasibility diagnostic, not an a0 measurement.  No verdict words.
"""
import os, sys, json, math, re, time
sys.dont_write_bytecode = True
import numpy as np
from scipy import ndimage as ndi

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE); REPO = os.path.dirname(CFG)
EXT = os.path.join(os.path.dirname(REPO), "_external_data", "mightee_probe")
C_KMS = 299792.458; PIX = 2.0; BEAM = {"r0p0": 12.27, "r0p5": 16.33}
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok, load_bearing=True):
    CHK.append((name, bool(ok), load_bearing)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


# the targets: read from the frozen script's own text (no re-typing)
src = open(os.path.join(HERE, "cfg300_probe.py"), encoding="utf-8").read()
TARGETS = eval(re.search(r"TARGETS = (\{.*?\})\n\n", src, re.S).group(1), {"dict": dict})
first = json.load(open(os.path.join(HERE, "cfg300_stageB_results.json")))["numbers"]["results"]


def mad_sigma(a):                                                                               # verbatim from cfg300_probe.py
    a = a[np.isfinite(a)]
    return 1.4826 * np.median(np.abs(a - np.median(a))) if a.size else float("nan")


def build(cube0, freq, nu_c, w50_cat, beam, xc, yc, r_in_px):
    """the frozen lines of analyze() (cfg300_probe.py, lines 55-73), unchanged, returning the arrays the diagnostics need"""
    nch, ny, nx = cube0.shape
    cube = np.nan_to_num(cube0)
    v = C_KMS * (nu_c - freq) / nu_c
    yy, xx = np.mgrid[0:ny, 0:nx]; rr = np.hypot(xx - xc, yy - yc); ring = rr > r_in_px
    sig_c = np.array([mad_sigma(cube[i][ring]) for i in range(nch)]); sig_med = float(np.median(sig_c[sig_c > 0]))
    sm = ndi.uniform_filter1d(cube, size=3, axis=0, mode="nearest")
    sig_s = np.array([mad_sigma(sm[i][ring]) for i in range(nch)]); sigma_s = float(np.median(sig_s[sig_s > 0]))
    snr = sm / sigma_s
    win = np.abs(v) <= (w50_cat / 2 + 50.0); free = np.abs(v) > (w50_cat / 2 + 80.0)
    r3 = 3 * beam / PIX
    cand = (snr >= 3) & win[:, None, None]
    seed = (snr >= 5) & win[:, None, None] & (rr <= r3)[None]
    lab, nl = ndi.label(cand, structure=ndi.generate_binary_structure(3, 1))
    keep = np.unique(lab[seed]); keep = keep[keep > 0]
    mask = np.isin(lab, keep) if keep.size else np.zeros_like(cand)
    return dict(cube=cube, v=v, rr=rr, ring=ring, sig_med=sig_med, sigma_s=sigma_s, snr=snr, win=win, free=free, r3=r3, mask=mask, nch=nch, ny=ny, nx=nx)


def w50_of(spec, v):
    """the frozen W50 rule on a spectrum: 3-channel boxcar, 50 % of the smoothed peak, linear interpolation of the crossings"""
    sps = ndi.uniform_filter1d(spec, size=3, mode="nearest"); pk = int(np.argmax(sps)); half = 0.5 * sps[pk]
    above = np.nonzero(sps >= half)[0]; lo, hi = int(above.min()), int(above.max()); nch = len(spec)

    def cross(i0, i1):
        y0, y1 = sps[i0], sps[i1]; t = (half - y0) / (y1 - y0) if y1 != y0 else 0.5
        return v[i0] + t * (v[i1] - v[i0])
    va = cross(lo - 1, lo) if lo > 0 else v[lo]; vb = cross(hi + 1, hi) if hi < nch - 1 else v[hi]
    return float(abs(va - vb))


P(__doc__.strip()); P("\nPOST HOC DIAGNOSTICS (2026-10-02; not frozen)")
out = {}
for tag, t in TARGETS.items():
    for wt in t["weights"]:
        k = f"{tag}_{wt}"; z = np.load(os.path.join(EXT, f"cfg300_{tag}_{wt}.npz"), allow_pickle=True)
        beam = BEAM[wt]; nu_c = t["nu_mhz"] * 1e6; r_in = 50 if tag == "T1" else 30
        B = build(z["cube"], z["freq"], nu_c, t["w50"], beam, float(z["xc"]), float(z["yc"]), r_in)
        cube, v, rr, snr, mask = B["cube"], B["v"], B["rr"], B["snr"], B["mask"]
        dnu = float(abs(z["freq"][1] - z["freq"][0])); nbeam = 1.1331 * (beam / PIX) ** 2
        f1 = first[k]; R = {}
        # ---- PH0 same-chain control
        I = np.where(mask, cube, 0.0); S_int = float(I.sum(0).sum() * dnu / nbeam); nvox = int(mask.sum())
        spec = I.sum((1, 2)); w50_m = w50_of(spec, v)
        ok0 = (nvox == f1["nvox"]) and abs(S_int / f1["S_int"] - 1) < 1e-6 and abs(w50_m / f1["w50"] - 1) < 1e-6
        check(f"PH0 {k}: the rebuilt frozen mask reproduces the first run (nvox, S_int, W50) to 1e-6", f"nvox {nvox} vs {f1['nvox']}; S_int {S_int:.4f} vs {f1['S_int']:.4f}; W50 {w50_m:.3f} vs {f1['w50']:.3f}", ok0)
        R["PH0"] = ok0
        # ---- D1 the C5 seeds
        free3 = B["free"][:, None, None] & (rr <= B["r3"])[None]; ringw = B["win"][:, None, None] & B["ring"][None]
        sets = {"free channels within 3 beams": free3, "ring in the line window": ringw}
        d1 = {}
        for nm, m in sets.items():
            pos = (snr >= 5) & m; neg = (snr <= -5) & m
            lab, nl = ndi.label(pos, structure=ndi.generate_binary_structure(3, 3))
            clumps = []
            for c in range(1, nl + 1):
                idx = np.argwhere(lab == c); n = len(idx); ch, yy_, xx_ = idx.mean(0)
                clumps.append(dict(nvox=int(n), dx_arcsec=float((xx_ - float(z["xc"])) * PIX), dy_arcsec=float((yy_ - float(z["yc"])) * PIX), v_kms=float(np.interp(ch, np.arange(len(v)), v)), peak_snr=float(snr[lab == c].max())))
            d1[nm] = dict(n_pos=int(pos.sum()), n_neg=int(neg.sum()), n_region_voxels=int(m.sum()), n_clumps=nl, clumps=clumps)
            P(f"  {k} D1 {nm}: >= +5 sigma {int(pos.sum())}, <= -5 sigma {int(neg.sum())} of {int(m.sum())} voxels; positive clumps {nl}: " + "; ".join(f"[{c['nvox']} vox at ({c['dx_arcsec']:+.0f}, {c['dy_arcsec']:+.0f}) arcsec, v {c['v_kms']:+.0f} km/s, peak {c['peak_snr']:.1f}]" for c in clumps[:6]))
        allfree = B["free"][:, None, None] & np.ones_like(snr, dtype=bool); nall = int(allfree.sum())
        pos_all = int(((snr >= 5) & allfree).sum()); neg_all = int(((snr <= -5) & allfree).sum()); posr = int(((snr >= 5) & allfree & B["ring"][None]).sum()); negr = int(((snr <= -5) & allfree & B["ring"][None]).sum())
        d1["whole line-free part (all pixels)"] = dict(n_voxels=nall, n_pos=pos_all, n_neg=neg_all, gaussian_expectation_per_tail=nall * 2.867e-7)
        d1["line-free channels, ring pixels only"] = dict(n_pos=posr, n_neg=negr)
        P(f"  {k} D1 whole line-free channel range (all pixels, {nall} voxels): >= +5 sigma {pos_all}, <= -5 sigma {neg_all} (Gaussian expectation per tail {nall * 2.867e-7:.2f}); ring pixels only: +{posr} / -{negr}")
        R["D1"] = d1
        # ---- D2 curve of growth
        L = f1["extent_arcsec"]; Rm = L / 2.0; xc, yc = float(z["xc"]), float(z["yc"]); half_box = (B["nx"] - 1) / 2.0 - 1.0
        cg = []
        for f in (0.5, 0.75, 1.0, 1.25, 1.5, 2.0):
            Rpx = f * Rm / PIX
            if Rpx > half_box: continue
            ap = rr <= Rpx; npx = int(ap.sum()); nv = npx * int(B["win"].sum())
            S = float(cube[B["win"]][:, ap].sum() * dnu / nbeam); sg = float(B["sig_med"] * dnu * math.sqrt(nv / nbeam))
            cg.append(dict(f=f, R_arcsec=f * Rm, S_Jy_Hz=S, sigma_S=sg, ratio_to_cat=S / t["S_cat"], ratio_err=sg / t["S_cat"]))
        R["D2"] = cg; P(f"  {k} D2 unmasked aperture flux in the line window (S_cat {t['S_cat']:.0f} +- {t['S_cat_err']:.0f}; frozen mask S_int {f1['S_int']:.0f}, ratio {f1['S_int'] / t['S_cat']:.3f}): " + "; ".join(f"R {c['R_arcsec']:.0f}\" ({c['f']}x): {c['S_Jy_Hz']:.0f} +- {c['sigma_S']:.0f} = {c['ratio_to_cat']:.2f}" for c in cg))
        # ---- D3 W50 of the unmasked aperture spectrum
        d3 = []
        rng = np.random.default_rng(3001)
        for f in (1.0, 1.5):
            Rpx = f * Rm / PIX
            if Rpx > half_box: continue
            ap = rr <= Rpx; npx = int(ap.sum()); spec_ap = cube[:, ap].sum(1)
            sg_ch = B["sig_med"] * math.sqrt(npx * nbeam)                                       # per-channel noise of the aperture sum (correlated over the beam)
            w = w50_of(spec_ap, v); sc = [w50_of(spec_ap + rng.normal(0, sg_ch, spec_ap.size), v) for _ in range(200)]
            d3.append(dict(f=f, R_arcsec=f * Rm, w50=w, w50_noise_median=float(np.median(sc)), w50_noise_p16=float(np.percentile(sc, 16)), w50_noise_p84=float(np.percentile(sc, 84)), peak_over_sigma=float(ndi.uniform_filter1d(spec_ap, 3).max() / (sg_ch / math.sqrt(3)))))
        R["D3"] = d3; tol = max(3 * t["w50_err"], 25.0)
        P(f"  {k} D3 W50: frozen mask {f1['w50']:.1f}; catalogue {t['w50']:.0f} +- {t['w50_err']:.0f} (tolerance {tol:.0f}); unmasked aperture " + "; ".join(f"R {d['R_arcsec']:.0f}\" ({d['f']}x): {d['w50']:.1f} (noise 16-84 % {d['w50_noise_p16']:.1f}-{d['w50_noise_p84']:.1f}; peak {d['peak_over_sigma']:.1f} sigma)" for d in d3))
        # ---- NULL control: the unmasked aperture flux per channel in the line-free channels is consistent with zero
        ap = rr <= (Rm / PIX if Rm / PIX <= half_box else half_box); npx = int(ap.sum()); fr = B["free"]
        per_ch = cube[fr][:, ap].sum(1); sg_ap = B["sig_med"] * math.sqrt(npx * nbeam); zsc = float(per_ch.mean() / (sg_ap / math.sqrt(per_ch.size)))
        R["NULL"] = dict(n_free_channels=int(per_ch.size), mean_per_channel=float(per_ch.mean()), sigma_ap=float(sg_ap), z=zsc)
        check(f"NULL {k}: the unmasked aperture flux per channel in the {per_ch.size} line-free channels is consistent with zero (|z| < 3)", f"mean {per_ch.mean():.3e} Jy/beam summed, sigma/sqrt(n) {sg_ap / math.sqrt(per_ch.size):.3e}: z = {zsc:+.2f}", abs(zsc) < 3.0)
        out[k] = R
NUM["diagnostics"] = out
nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - T0:.0f} s)")
open(os.path.join(HERE, "cfg300_posthoc_diagnostics.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>").replace(os.path.dirname(REPO), "<repo-parent>") + "\n")


def _jc(o):
    if isinstance(o, dict): return {str(k): _jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_jc(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o


json.dump(dict(stage="POSTHOC", checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=_jc(NUM)), open(os.path.join(HERE, "cfg300_posthoc_diagnostics_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
