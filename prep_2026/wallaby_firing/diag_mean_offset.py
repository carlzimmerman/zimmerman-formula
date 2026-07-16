#!/usr/bin/env python3
"""
DIAGNOSTIC (Lane W1 QA) -- why is the direction-blind ensemble mean of
A_preregistered nonzero (+0.104, QC pass N=50)?
================================================================================
FIREWALL: N~237 -> ~1-1.5 sigma at AQUAL amplitude; NEITHER pre-registered kill
condition (3-sigma AQUAL-vs-BranchB, N~1157 canonical a0=9.36e-11 / N~1424 alt
a0=1.13e-10) CAN TRIGGER on this sample.  This script diagnoses an EXTRACTION
systematic; it attaches no direction and renders no physics verdict.

HYPOTHESIS (coherent-offset): if the map velocity minus WKAPP VSys_model
carries a constant per-galaxy offset delta (e.g. optical-vs-radio cz
convention mismatch: v_opt - v_rad = v^2/c, +4 km/s at cz=1100 rising to
+120 km/s at cz=6000), then per-side
    v_rec_est ~ v_rot + delta/(sin i <cth>),   v_app_est ~ v_rot - delta/(...)
    => A_pre bias ~ +2 delta / (v_rot sin i <cth>)   (coherent, positive if delta>0)
while the two-side MEAN cancels delta at first order (sanity ratio blind to it).

TESTS (all computed, none asserted):
  T1  delta_emp per galaxy = intensity-weighted median[v_map - VSys_model] over
      the minor-axis strip |cos theta| < 0.2 (v_los = vsys there exactly).
  T2  Correlation of A_preregistered with the predicted bias
      b_pred = 2 delta_emp / (v_rot_out sin i * 0.79)  (0.79 = <1/|cth|>^-1 over
      the |cth|>=0.5 wedge, uniform-azimuth approximation).
  T3  Correlation of A_preregistered with cz (the radio-vs-optical mismatch
      grows ~ cz^2; a flat delta_emp vs cz kills that specific sub-hypothesis).
  T4  Re-extraction (DIAGNOSTIC ONLY, not the frozen deliverable) with
      vsys := VSys_model + delta_emp; the frozen CSV is NOT modified.
exit 0.
"""
import os, sys, csv, math, json, warnings
import numpy as np

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
PREP = "/Users/carlzimmerman/new_physics/prep_2026/wallaby_prep"
sys.path.insert(0, PREP)
import perside_extractor as pe
from astropy.io import fits
from astropy.wcs import WCS

C_KMS = 299792.458
F0_HI = 1420405751.77
DATA = os.path.join(HERE, "data")
PILOT = os.path.join(PREP, "pilot_data")


def path(fn):
    p = os.path.join(PILOT, fn)
    return p if os.path.exists(p) else os.path.join(DATA, fn)


rows = [r for r in csv.DictReader(
    l for l in open(os.path.join(HERE, "perside_237.csv")) if not l.startswith("#"))]
qc = [r for r in rows if r["qc_pass"] == "True"]
print(f"QC-pass galaxies: {len(qc)}")

recs = []
for r in qc:
    avg = r["model_file"]
    mom1 = avg.replace("_Kin", "").replace("_AvgMod.txt", "_mom1.fits")
    if not os.path.exists(path(mom1)):
        mom1 = mom1.replace("NGC5044", "NGC_5044")
    mom0 = mom1.replace("mom1", "mom0")
    geo, rc = pe.parse_avgmod(path(avg))
    pa = geo.get("PA_model_g", geo.get("PA_model"))
    hdu1 = fits.open(path(mom1))[0]
    vmap = C_KMS * (F0_HI / np.squeeze(hdu1.data).astype(float) - 1.0)
    w0 = np.squeeze(fits.open(path(mom0))[0].data).astype(float)
    w = WCS(hdu1.header).celestial
    x0, y0 = w.wcs_world2pix([[geo["RA_model"], geo["DEC_model"]]], 0)[0]
    pix_as = (hdu1.header["CDELT1"] * 3600.0, hdu1.header["CDELT2"] * 3600.0)
    ny, nx = vmap.shape
    R, cth = pe.disk_coords(nx, ny, x0, y0, pix_as, pa, geo["Inc_model"])
    rads = np.array([q[0] for q in rc])
    dr = np.median(np.diff(rads)) if len(rads) > 1 else 15.0
    Rmax = rads[-1] + dr / 2
    vsys = geo["VSys_model"]
    # T1: minor-axis empirical offset
    strip = (np.abs(cth) < 0.2) & (R < Rmax) & np.isfinite(vmap) & \
            np.isfinite(w0) & (w0 > 0) & (np.abs(vmap - vsys) < 600)
    if strip.sum() < 10:
        continue
    vv, ww = vmap[strip], w0[strip]
    order = np.argsort(vv)
    cw = np.cumsum(ww[order]); cw /= cw[-1]
    delta = float(np.interp(0.5, cw, vv[order]) - vsys)   # weighted median - vsys
    vrot_out = 0.5 * (float(r["v_rec"]) + float(r["v_appr"]))
    sini = math.sin(math.radians(float(r["inc"])))
    b_pred = 2.0 * delta / (vrot_out * sini) * 0.79
    # T4: re-extract with corrected vsys (diagnostic only)
    ring_edges = np.concatenate([[max(rads[0] - dr / 2, 0.0)], rads + dr / 2])
    geom = {"x0": float(x0), "y0": float(y0), "pa_deg": float(pa),
            "inc_deg": float(geo["Inc_model"]), "vsys": vsys + delta}
    res = pe.extract(vmap, w0, geom, ring_edges, pix_as=pix_as, nboot=100)
    A_corr = -res["A"] if res else np.nan   # pre-registered ordering (no flips in sample)
    recs.append(dict(jname=r["jname"], cz=float(r["cz"]), delta=delta,
                     A_pre=float(r["A_preregistered"]), b_pred=b_pred,
                     A_pre_corr=float(A_corr), vrot=vrot_out,
                     sig=float(r["sigma_boot"])))

d = {k: np.array([x[k] for x in recs]) for k in recs[0]
     if k != "jname"}
n = len(recs)
print(f"analyzed: {n}")
print(f"\nT1  delta_emp (map minor-axis median - VSys_model), km/s:")
print(f"    mean={d['delta'].mean():+.2f}  median={np.median(d['delta']):+.2f} "
      f" rms={d['delta'].std(ddof=1):.2f}  frac>0: {(d['delta']>0).mean():.2f}")
cz_opt_rad = d["cz"] ** 2 / C_KMS
print(f"    optical-radio prediction at these cz: median {np.median(cz_opt_rad):.1f} km/s"
      f" (range {cz_opt_rad.min():.1f}..{cz_opt_rad.max():.1f})")
r_dcz = np.corrcoef(d["delta"], cz_opt_rad)[0, 1]
print(f"    corr(delta_emp, cz^2/c) = {r_dcz:+.3f}")

r12 = np.corrcoef(d["A_pre"], d["b_pred"])[0, 1]
print(f"\nT2  corr(A_pre, predicted coherent-offset bias) = {r12:+.3f}")
slope = np.polyfit(d["b_pred"], d["A_pre"], 1)
print(f"    A_pre = {slope[0]:.2f} * b_pred + {slope[1]:+.4f}  (slope 1 = pure offset artifact)")

r13 = np.corrcoef(d["A_pre"], d["cz"])[0, 1]
print(f"\nT3  corr(A_pre, cz) = {r13:+.3f}")

mA, mC = d["A_pre"].mean(), d["A_pre_corr"].mean()
semA = d["A_pre"].std(ddof=1) / math.sqrt(n)
semC = d["A_pre_corr"].std(ddof=1) / math.sqrt(n)
print(f"\nT4  DIAGNOSTIC re-extraction with vsys += delta_emp (frozen CSV untouched):")
print(f"    mean A_pre  frozen    = {mA:+.4f} +/- {semA:.4f}   rms {d['A_pre'].std(ddof=1):.4f}")
print(f"    mean A_pre  corrected = {mC:+.4f} +/- {semC:.4f}   rms {d['A_pre_corr'].std(ddof=1):.4f}")
print(f"    median frozen {np.median(d['A_pre']):+.4f} -> corrected {np.median(d['A_pre_corr']):+.4f}")

verdict = []
if abs(r12) > 0.5 and abs(mC) < 0.5 * abs(mA):
    verdict.append("COHERENT-OFFSET SYSTEMATIC CONFIRMED: the nonzero direction-blind "
                   "mean is (mostly) a vsys-offset artifact")
elif abs(mC) < 0.5 * abs(mA):
    verdict.append("vsys correction removes most of the mean (correlation weak -- "
                   "offset structure more complex than a single delta)")
else:
    verdict.append("vsys offset does NOT explain the nonzero mean -- unresolved "
                   "systematic; flag to the firing lane")
if abs(r_dcz) > 0.5:
    verdict.append("delta_emp tracks cz^2/c -> consistent with an optical-vs-radio "
                   "cz convention mismatch (map optical vs WKAPP radio)")
print("\nVERDICT (computed):")
for v in verdict:
    print("  - " + v)

json.dump({"n": n, "records": recs, "corr_A_bpred": float(r12),
           "corr_A_cz": float(r13), "corr_delta_cz2": float(r_dcz),
           "mean_A_frozen": float(mA), "mean_A_corrected": float(mC)},
          open(os.path.join(HERE, "diag_mean_offset.json"), "w"), indent=1)
print(f"\nwritten: diag_mean_offset.json")
sys.exit(0)
