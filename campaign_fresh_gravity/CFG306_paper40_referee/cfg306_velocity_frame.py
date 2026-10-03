#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG306 (PAPER40 referee): which velocity frame are the MIGHTEE-HI COSMOS catalogue W50 values in?  Referee diagnostic, not frozen.

PAPER40 divides the catalogue W50 by (1 + z) (reads it as observed-frame) and lists "rest-frame" as a +0.098 dex systematic to be
"confirmed with the catalogue's authors".  Three tests:

  F1  the catalogue paper itself (Maksymowicz-Maciata et al. 2026, arXiv:2605.28731, Appendix D example spectra) prints each example's W50
      both in km/s and in channels (26.126 kHz channels).  The km/s-per-channel factor tells the conversion:
        rest-frame width:      dv = c * dnu / nu_obs              (= 5.514 (1+z) km/s per channel)
        observed (cz) width:   dv = c * dnu * nu0 / nu_obs^2      (= 5.514 (1+z)^2 km/s per channel)
      The five example values were transcribed from the local copy of the arXiv PDF (outside the repository; re-read here with pdftotext
      when present) and matched to catalogue rows by position.
  F2  CFG302's raw rest-frame widths (58 frozen detections): the slope of log10(W_ours/W_cat) on log10(1+z) is 0 if the catalogue is
      rest-frame and -1 if it is observed-frame.
  F3  CFG304's ALFALFA pairs: ALFALFA W50 is observed-frame (H18: no cosmological correction), so log10(W_cat/W_ALFALFA) on log10(1+z)
      has slope -1 if the catalogue is rest-frame and 0 if observed-frame (weak: z <= 0.047).
Writes cfg306_velocity_frame.out and cfg306_velocity_frame_results.json.
"""
import os, sys, json, math, re, subprocess, shutil
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
LOG, NUM = [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


C_KMS = 299792.458
NU0 = 1420.40575e6
DNU = 26.126e3                                     # catalogue paper Table 2 (26.126 kHz; 5.5 km/s at z = 0)
cat = pd.read_csv(os.path.join(REPO, "data_assembly", "mightee_hi_catalogue_2026-10-02", "MIGHTEE_HI_COSMOS_catalogue.csv"), dtype={"ID_catalogue": str})

# ---------------------------------------------------------------- F1
# (RA, Dec, W50 km/s, W50 channels) as printed in the catalogue paper's Appendix D example panels (arXiv:2605.28731v1)
EX = [(151.02069, 1.71759, 237.858, 40.5), (148.95077, 2.13172, 67.32, 12.0), (149.42216, 2.56842, 84.858, 14.1),
      (150.0338, 2.76513, 264.04, 46.5), (150.23852, 3.14178, 420.287, 74.0)]
pdf = os.path.join(os.path.dirname(REPO), "_external_data", "arxiv_pdf", "2605.28731.pdf")
f1_pdf = None
if os.path.exists(pdf) and shutil.which("pdftotext"):
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    kms = [float(x) for x in re.findall(r"W50 \[km/s\] = ([0-9.]+)", txt)]
    chn = [float(x) for x in re.findall(r"W50 \[channels\] = ([0-9.]+)", txt)]
    tab2 = re.search(r"Channel width\s+([0-9.]+) kHz", txt)
    f1_pdf = dict(kms=kms, channels=chn, channel_kHz=float(tab2.group(1)) if tab2 else None)
    same = sorted(kms) == sorted(e[2] for e in EX) and sorted(chn) == sorted(e[3] for e in EX)
    P(f"F1 local PDF re-read (pdftotext): W50 km/s {kms}; channels {chn}; Table 2 channel width {f1_pdf['channel_kHz']} kHz; transcription matches: {same}")
    f1_pdf["transcription_matches"] = bool(same)
else:
    P("F1 local PDF not found; using the transcribed values only")
rows = []
for ra, de, wk, wc in EX:
    sep = np.hypot((cat.RA_deg - ra) * np.cos(np.radians(de)), cat.Dec_deg - de) * 3600
    i = int(sep.idxmin()); r = cat.loc[i]
    nu = r.freq_MHz * 1e6
    per = wk / wc
    rest = C_KMS * DNU / nu
    obs = C_KMS * DNU * NU0 / nu ** 2
    rows.append(dict(ID=r.ID_catalogue, sep_arcsec=float(sep[i]), z=float(r.z_HI), freq_MHz=float(r.freq_MHz), W50_cat=float(r.W_50_km_s), W50_example=wk, channels=wc,
                     kms_per_channel=per, rest_pred=rest, obs_pred=obs, dev_rest=per / rest - 1, dev_obs=per / obs - 1, chan_rounding_frac=0.05 / wc))
    P(f"  {r.ID_catalogue} (sep {sep[i]:.1f}\", z {r.z_HI}): W50 {wk} km/s = {wc} ch -> {per:.4f} km/s/ch; rest-frame predicts {rest:.4f} ({per / rest - 1:+.4f}), "
      f"observed-frame {obs:.4f} ({per / obs - 1:+.4f}); channel rounding allows +-{0.05 / wc:.4f}; catalogue W50 {r.W_50_km_s}")
dr = np.array([x["dev_rest"] for x in rows]); do = np.array([x["dev_obs"] for x in rows])
P(f"F1 verdict data: max |dev| rest-frame {np.max(np.abs(dr)):.4f}; observed-frame deviations {np.round(do, 4).tolist()} (z-dependent, up to {np.max(np.abs(do)):.3f})")
NUM["F1"] = dict(rows=rows, max_abs_dev_rest=float(np.max(np.abs(dr))), obs_devs=do.tolist(), pdf=f1_pdf,
                 n_example_W50_equal_catalogue=int(sum(abs(x["W50_example"] - x["W50_cat"]) < 1.0 for x in rows)))

# ---------------------------------------------------------------- F2
c302 = pd.read_csv(os.path.join(CFG, "CFG302_mightee_cube_raw_widths", "cfg302_per_galaxy.csv"))
d2 = c302[(c302.primary == 1) & (c302.detected.astype(str) == "True") & (c302.W50_defined.astype(str) == "True")].copy()
d2 = d2[np.isfinite(d2.logratio_W50)]
x = np.log10(1 + d2.z_HI.values); y = d2.logratio_W50.values


def theil_sen(x, y):
    s = [(y[j] - y[i]) / (x[j] - x[i]) for i in range(len(x)) for j in range(i + 1, len(x)) if x[j] != x[i]]
    return float(np.median(s))


def clip(x, y, k=3.0):
    med = np.median(y); rs = 1.4826 * np.median(np.abs(y - med)); m = np.abs(y - med) <= k * rs
    return x[m], y[m]


rng = np.random.default_rng(3062)
out2 = {}
for nm, (xx, yy) in (("all 58", (x, y)), ("3-sigma clipped", clip(x, y))):
    ts = theil_sen(xx, yy)
    bs = []
    for _ in range(2000):
        i = rng.integers(0, len(xx), len(xx)); bs.append(theil_sen(xx[i], yy[i]))
    q = np.percentile(bs, [2.5, 16, 84, 97.5])
    out2[nm] = dict(n=len(xx), slope=ts, q=q.tolist(), z_range=[float(10 ** xx.min() - 1), float(10 ** xx.max() - 1)])
    P(f"F2 CFG302 {nm} (n {len(xx)}): Theil-Sen slope of log(W_ours_rest/W_cat) on log(1+z) {ts:+.2f} (68% {q[1]:+.2f} to {q[2]:+.2f}; 95% {q[0]:+.2f} to {q[3]:+.2f}); "
      f"rest-frame catalogue predicts 0, observed-frame predicts -1")
NUM["F2"] = out2

# ---------------------------------------------------------------- F3
p4 = pd.read_csv(os.path.join(CFG, "CFG304_mightee_flux_scale_alfalfa", "cfg304_matched_pairs.csv"))
p4 = p4[np.isfinite(p4.logW50_cat_A)]
for nm, sub in (("code 1", p4[p4.hi_code == 1]), ("codes 1+2", p4)):
    xx = np.log10(1 + sub.z_HI.values); yy = sub.logW50_cat_A.values
    ts = theil_sen(xx, yy)
    bs = []
    for _ in range(2000):
        i = rng.integers(0, len(xx), len(xx)); bs.append(theil_sen(xx[i], yy[i]))
    q = np.percentile(bs, [16, 84])
    med = float(np.median(yy)); medz = float(np.median(sub.z_HI))
    NUM.setdefault("F3", {})[nm] = dict(n=len(sub), slope=ts, q68=q.tolist(), median_logratio=med, median_z=medz, expected_if_rest=-math.log10(1 + medz))
    P(f"F3 CFG304 {nm} (n {len(sub)}, median z {medz:.4f}): median log(W_cat/W_ALFALFA) {med:+.4f}; if the catalogue is rest-frame the expectation is "
      f"{-math.log10(1 + medz):+.4f} (plus MIGHTEE's uncorrected 5.5 km/s channel broadening, positive), if observed-frame 0; slope {ts:+.2f} (68% {q[0]:+.2f} to {q[1]:+.2f})")

json.dump(dict(lane="CFG306", script=os.path.basename(__file__), note="referee diagnostic; not frozen", numbers=NUM),
          open(os.path.join(HERE, "cfg306_velocity_frame_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg306_velocity_frame.out"), "w").write(__doc__.strip() + "\n\n" + "\n".join(LOG) + "\n")
print("wrote cfg306_velocity_frame.out and cfg306_velocity_frame_results.json")
