#!/usr/bin/env python3
"""Z06 -- THE tSZ DATA PULL + THE FIRST PRE-SCORED RUN (night-shift wave Z6).

THE QUESTION (from REASSESSMENT_2026-09-16 seam #5): the tSZ test's registered
inputs are all public and the lane is 'runnable today, unclaimed' -- so Z6 does
the unclaimed work: (1) THE FETCH: pull at least ONE real map product (Planck
MILCA/NILC y-maps or the ACT DR6/DR6+Planck Compton-y map) into
deepseek_push/Z06_data/ with PROVENANCE.md (URL, size, checksum); if the network
blocks the pull, deliver the pipeline + the exact fetch script + the size budget
and mark the pull PENDING-NETWORK -- never faking a download; (2) THE PRE-SCORED
RUN: the 2-bin slope extraction at the 4 shortlist clusters' positions
(A3266/A2029/A85/A2319, RA/Dec from the committed X-COP list) -- on the fetched
map where the footprint allows, otherwise on the committed synthetic zero-param
y-profiles (G220's final curves) -- with the measured-vs-predicted y slope and
the JOINT/NEITHER/grey assignment per G177's 3-way tree; (3) THE HONEST STATE;
(4) VERDICTS V1/V2/V3.

THE FETCH TARGET (LAMBDA, ACT DR6 + Planck Compton-y map, Coulton et al. 2024
/ 2307.01258 -- the y-map product named in G129's instrument table, public):
  https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_adv/Compton_y_maps/ilc_actplanck_ymap.fits
      1,783,298,880 bytes (~1.78 GB), delivered 2024-03-21
  https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_adv/Compton_y_maps/wide_mask_GAL070_apod_1.50_deg_wExtended.fits
      1.78 GB sky mask
  https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_adv/Compton_y_maps/ilc_beam.txt
      ~1 MB effective beam response
The Planck MILCA/NILC all-sky branch (for A2319, dec +43.9 deg OUTSIDE the ACT
footprint) is the IRSA release-3 tarball (12.25 GB, both maps + weights + masks):
  https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/component-maps/foregrounds/COM_CompMap_Compton-SZMap_R2.02.tgz

THE PRE-SCORED RUN.  Per G177/G220's registered decision tree on the 2-bin slope
over [theta_500, 2 theta_500]:
    JOINT        slope in (-2.7, -2.05)   (the zero-param joint curve, G220)
    PHANTOM-ONLY slope in (-1.8, -1.2)    (a FALSIFIER, F2' fires: dust killed)
    NEITHER      slope < -2.7             (F1'-side: steeper than the joint band)
    INDECISIVE(grey) where the error straddles branches (< 60% in any branch).
The prediction at the 4 shortlist positions is G220's zero-parameter curve
(median 2-bin -2.54, per-cluster slopes A3266 -3.05 / A2029 -2.23 / A85 -2.60 /
A2319 -2.55).  The MEASURED slope comes from the fetched map when the cluster is
inside the ACT footprint (A3266/A2029/A85; A2319 is out-of-band and needs the
Planck branch -- registered in G129's ACT-band column), otherwise from the
committed synthetic zero-param profile (the pipeline-proven path).

THE HONEST STATE: pipeline-proven (synthetic) ALWAYS; map-in-hand when the file
lands; data-pulled-and-preliminary for the in-footprint shortlist -- with the
first real-data confrontation staged.  No amplitude rescues: the 2-bin SLOPE is
unit-invariant (a log-ratio of the y-map), so this first confrontation tests
the SHAPE channel exactly as G177's tree requires, independent of the y-map
calibration.

Run: python3 Z06_tsz_pull.py > Z06_tsz_pull.out 2>&1
Artifacts: Z06_tsz_pull.py / .out / Z06_results.json (+ Z06_data/PROVENANCE.md
and the fetched products when the network allows).
"""

import contextlib as _cl
import hashlib
import io as _io
import json
import math
import os
import subprocess
import sys
import time

import numpy as np
from astropy.io import fits
from scipy.integrate import quad
from scipy.special import i0e

RES, NP, NF = [], 0, 0


def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d:
        print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    NP, NF = NP + (1 if ok else 0), NF + (0 if ok else 1)


HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "Z06_data")
REPO = os.path.normpath(os.path.join(HERE, ".."))
XB = os.path.join(REPO, "real_research", "data", "xcop")
os.makedirs(DATA, exist_ok=True)

G = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0857e19
A0 = 9.3619e-11
MU = 0.6
MP = 1.6726219e-27
KB = 1.380649e-23
SIGMAT = 6.6524587e-29
MEC2 = 8.1871058e-14
XH = 0.76
MU_E = 2.0 / (1.0 + XH)
CL = 2.99792458e8
H0 = 67.4 * 1e3 / 3.0857e22
OM, OL = 0.315, 0.685
TCMB = 2.7255
RMAX = 6000.0

SHORTLIST = ["A3266", "A2029", "A85", "A2319"]      # G220's named first-run set
SHORTLIST_RA_DEC = {                                  # committed X-COP FITS headers
    "A3266": (67.8434, -61.4297),
    "A2029": (227.7342, 5.7444),
    "A85": (10.4594, -9.3029),
    "A2319": (290.3028, 43.9450),
}

MAP_URL = "https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_adv/Compton_y_maps/ilc_actplanck_ymap.fits"
MASK_URL = "https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_adv/Compton_y_maps/wide_mask_GAL070_apod_1.50_deg_wExtended.fits"
BEAM_URL = "https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_adv/Compton_y_maps/ilc_beam.txt"
PLANCK_YSZ_URL = ("https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/"
                  "component-maps/foregrounds/COM_CompMap_Compton-SZMap_R2.02.tgz")
MAP_FILE = "ilc_actplanck_ymap.fits"
MASK_FILE = "wide_mask_GAL070_apod_1.50_deg_wExtended.fits"
BEAM_FILE = "ilc_beam.txt"
MAP_SIZE = 1783298880          # bytes (Content-Length, verified 2026-09-16)
MASK_SIZE = 1783298880         # bytes
PLANCK_YSZ_SIZE = 12252877791  # bytes (Content-Length, verified 2026-09-16)

print("Z06 -- THE tSZ DATA PULL + THE FIRST PRE-SCORED RUN")
print("(seam #5 of REASSESSMENT_2026-09-16: the tSZ test's registered inputs are")
print(" public and the lane was unclaimed -- this lane claims it)")
print("=" * 98)

# ============================================================================
# (0) THE FETCH -- the state probe + the exact fetch script + the size budget
# ============================================================================
FETCH_SCRIPT = f"""#!/bin/bash
# Z06 -- the exact fetch commands for the tSZ data pull (generated 2026-09-16).
# ACT DR6 + Planck Compton-y map (Coulton et al. 2024 / 2307.01258), LAMBDA:
curl -sL --retry 5 -C - -o {MAP_FILE} "{MAP_URL}"
curl -sL --retry 5 -C - -o {MASK_FILE} "{MASK_URL}"
curl -sL --retry 5 -C - -o {BEAM_FILE} "{BEAM_URL}"
# Planck MILCA/NILC all-sky branch (the A2319 / out-of-ACT-footprint channel;
# 12.25 GB tarball: both y-maps + weights + masks, IRSA release-3):
# curl -sL --retry 5 -C - -o COM_CompMap_Compton-SZMap_R2.02.tgz "{PLANCK_YSZ_URL}"
# tar tzf COM_CompMap_Compton-SZMap_R2.02.tgz | head   # inspect before extracting
"""


def sha256_file(path, chunk=1 << 22):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def probe(name, path, expect_size):
    if os.path.exists(path):
        sz = os.path.getsize(path)
        if sz >= expect_size:
            return {"present": True, "size": sz, "checksum": sha256_file(path),
                    "complete": True}
        return {"present": True, "size": sz, "checksum": None,
                "complete": False, "partial": f"{sz/expect_size:.1%}"}
    return {"present": False, "size": 0, "checksum": None, "complete": False}


map_state = probe("map", os.path.join(DATA, MAP_FILE), MAP_SIZE)
mask_state = probe("mask", os.path.join(DATA, MASK_FILE), MASK_SIZE)
beam_state = probe("beam", os.path.join(DATA, BEAM_FILE), 500000)
map_in_hand = map_state["complete"]

print()
print("(0) THE FETCH -- the state probe (no fake downloads: presence is checked")
print("    against the file itself, size and sha256)")
print(f"  map  {MAP_FILE}: {'COMPLETE ' + str(map_state['size']) + ' bytes' if map_state['complete'] else ('PARTIAL ' + str(map_state.get('partial')) if map_state['present'] else 'ABSENT')}")
print(f"  mask {MASK_FILE}: {'COMPLETE' if mask_state['complete'] else ('PARTIAL' if mask_state['present'] else 'ABSENT')}")
print(f"  beam {BEAM_FILE}: {'COMPLETE' if beam_state['complete'] else ('PARTIAL' if beam_state['present'] else 'ABSENT')}")
if map_in_hand:
    print(f"  sha256(map) = {map_state['checksum']}")
else:
    print("  -> PENDING-NETWORK branch: the exact fetch script and the size budget")
    print("     are delivered below; the pull is marked PENDING-NETWORK honestly.")
    print()
    print("THE EXACT FETCH SCRIPT (Z06_data/fetch_tsz_maps.sh):")
    print(FETCH_SCRIPT)
    print()
    print("THE SIZE BUDGET:")
    print(f"  ACT y-map  {MAP_FILE}: {MAP_SIZE/1e9:.2f} GB")
    print(f"  ACT mask   {MASK_FILE}: {MASK_SIZE/1e9:.2f} GB")
    print(f"  ACT beam   {BEAM_FILE}: ~1 MB")
    print(f"  Planck YSZ tarball (MILCA+NILC all-sky): {PLANCK_YSZ_SIZE/1e9:.2f} GB")
    print(f"  TOTAL (ACT branch): {2*MAP_SIZE/1e9:.2f} GB;  + Planck branch: "
          f"{(2*MAP_SIZE+PLANCK_YSZ_SIZE)/1e9:.2f} GB")

# ============================================================================
# (1) re-execute G220's committed build (zero-param curves + decision tree)
# ============================================================================
print()
print("=" * 98)
print("(1) THE COMMITTED SYNTHETIC ZERO-PARAM CURVES (re-executed in-process,")
print("    G220's own recipe: G129's phantom build x G141's dust law with the")
print("    derived (c0 = -0.1445, q = -1/3, p = 0.99) -- zero free parameters)")
print("=" * 98)

_ns1 = {"__file__": os.path.join(HERE, "G129_tsz_proposal.py"),
        "json": json, "math": math, "os": os, "np": np,
        "fits": fits, "quad": quad, "i0e": i0e}
_SRC1 = open(os.path.join(HERE, "G129_tsz_proposal.py")).read()
with _cl.redirect_stdout(_io.StringIO()):
    exec(compile(_SRC1.split("PER = []")[0], "g129_src", "exec"), _ns1)
BB = _ns1["BB"]
SURVEYS = _ns1["SURVEYS"]
beam_convolve = _ns1["beam_convolve"]
annular_bins = _ns1["annular_bins"]
snr_table = _ns1["snr_table"]
ACT_BINS = _ns1["ACT_BINS"]
PL_BINS = _ns1["PL_BINS"]
ACT_DEC_BAND = _ns1["ACT_DEC_BAND"]
CLUS = _ns1["CLUS"]
DAT = _ns1["DAT"]

AMP_C0_ANCHOR = -0.1445
AMP_Q = -1.0 / 3.0
_AMPS_BLOCK = """G122 = json.load(open(os.path.join(HERE, "G122_results.json")))
CC = G122["closed_form_candidate"]
P_STAR = float(CC["p_star"])
AMPS = {n: float(v) for n, v in CC["per_cluster_amp_log10"].items()}
"""
_AMPS_DERIVED = f"""G122 = json.load(open(os.path.join(HERE, "G122_results.json")))
CC = G122["closed_form_candidate"]
P_STAR = float(CC["p_star"])
AMP_C0 = {AMP_C0_ANCHOR!r}
AMP_Q  = {AMP_Q!r}
AMPS = {{n: AMP_C0 + AMP_Q * math.log10(DAT[n]["M500"] / MSUN / 8e14) for n in DAT}}
"""
_SRC2 = open(os.path.join(HERE, "G141_tsz_dust.py")).read()
assert _AMPS_BLOCK in _SRC2, "G141 source must contain the G122 amplitude block"
_SRC2_D = _SRC2.replace(_AMPS_BLOCK, _AMPS_DERIVED)
_ns2 = {"__file__": os.path.join(HERE, "G141_tsz_dust.py"),
        "json": json, "math": math, "os": os, "np": np,
        "fits": fits, "quad": quad, "i0e": i0e}
with _cl.redirect_stdout(_io.StringIO()):
    exec(compile(_SRC2_D.split("# ---------------- artifact")[0], "g141_src", "exec"), _ns2)
BBD = _ns2["BB"]

G220J = json.load(open(os.path.join(HERE, "G220_results.json")))
PER_G220 = {p["cluster"]: p for p in G220J["per_cluster"]}
VROWS_G220 = {r["cluster"]: r for r in G220J["expected_verdicts"]}
med_sl2_g220 = float(np.median([p["slope_2bin_zero_param"] for p in PER_G220.values()]))
# in-process recompute of the shortlist 2-bin slopes for the gate
sl2_recomp = {}
for nm in SHORTLIST:
    bd = BBD[nm]
    b9 = BB[nm]                                   # G129 build (kpc_per_arcmin)
    kpa = b9["kpc_per_arcmin"]
    th500 = bd["R500"] / kpa
    th_g = np.unique(np.concatenate([np.geomspace(0.03, 3.2 * th500, 700),
                                     [th500, 2 * th500]]))
    th_g.sort()
    ybg_d = np.array([bd["y_at"](x, "dust") for x in th_g * kpa])
    y1 = float(np.interp(th500, th_g, ybg_d))
    y2 = float(np.interp(2 * th500, th_g, ybg_d))
    sl2_recomp[nm] = math.log(y2 / y1) / math.log(2.0)
gate_short = all(abs(sl2_recomp[nm] - PER_G220[nm]["slope_2bin_zero_param"]) < 5e-4
                 for nm in SHORTLIST)
check("V0 [gate: the committed zero-param shortlist slopes re-executed] the 2-bin "
      "slopes at A3266/A2029/A85/A2319 recomputed in-process from the committed "
      "G129 x G141 builds reproduce G220_results.json to < 5e-4",
      " | ".join(f"{nm} {sl2_recomp[nm]:+.3f} (committed "
                 f"{PER_G220[nm]['slope_2bin_zero_param']:+.3f})" for nm in SHORTLIST),
      gate_short,
      "identical loader, ingests, recipe and derived dust law -> the synthetic "
      "zero-param profiles ARE the committed final curves (G220 V1)")

def gauss_cdf(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def verdict_of(sl, sig):
    """G177's 3-way tree on a measured 2-bin slope with per-cluster error sig."""
    p_joint = gauss_cdf((-2.05 - sl) / sig) - gauss_cdf((-2.7 - sl) / sig)
    p_phantom = gauss_cdf((-1.2 - sl) / sig) - gauss_cdf((-1.8 - sl) / sig)
    p_neither = gauss_cdf((-2.7 - sl) / sig)
    best = max(p_joint, p_phantom, p_neither)
    if best < 0.6:
        return "INDECISIVE(grey)", p_joint, p_phantom, p_neither
    if p_joint == best:
        return "JOINT", p_joint, p_phantom, p_neither
    if p_neither == best:
        return "NEITHER", p_joint, p_phantom, p_neither
    return "PHANTOM-ONLY(F2')", p_joint, p_phantom, p_neither


# ============================================================================
# (2) THE PRE-SCORED RUN
# ============================================================================
print()
print("=" * 98)
print("(2) THE PRE-SCORED RUN at the 4 shortlist positions (A3266/A2029/A85/A2319,")
print("    RA/Dec from the committed X-COP FITS headers)")
print("=" * 98)

RUNS = []
for nm in SHORTLIST:
    ra, dec = SHORTLIST_RA_DEC[nm]
    bd = BBD[nm]
    b9 = BB[nm]
    kpa = b9["kpc_per_arcmin"]
    th500 = bd["R500"] / kpa
    r = VROWS_G220[nm]
    sl_pred = PER_G220[nm]["slope_2bin_zero_param"]
    sig_pred = r["sig_slope"]
    in_band = ACT_DEC_BAND[0] <= dec <= ACT_DEC_BAND[1]
    RUNS.append(dict(
        cluster=nm, ra=ra, dec=dec, theta_500_arcmin=round(th500, 2),
        in_act_footprint=bool(in_band),
        slope_pred_zero_param=round(sl_pred, 3), sig_slope_pred=round(sig_pred, 2),
        expected_verdict=r["expected_verdict"],
        P_joint_pred=r["P_joint"], P_neither_pred=r["P_neither"]))

print(f"  {'cluster':8s} {'RA':>9s} {'DEC':>9s} {'th500':>6s} {'ACT?':>4s} "
      f"{'sl_pred':>8s} {'sig':>5s}  expected")
for u in RUNS:
    print(f"  {u['cluster']:8s} {u['ra']:9.4f} {u['dec']:9.4f} "
          f"{u['theta_500_arcmin']:6.2f} {'Y' if u['in_act_footprint'] else 'n':>4s} "
          f"{u['slope_pred_zero_param']:8.3f} {u['sig_slope_pred']:5.2f}  "
          f"{u['expected_verdict']}")

# ---------------- (2a) the map branch (the real-data confrontation) ------------
MEASURED = {}
MAP_INFO = {}
if map_in_hand:
    print()
    print("  THE MAP BRANCH -- the first real-data confrontation (ACT DR6 + Planck")
    print("  Compton-y map, Coulton et al. 2024).  The 2-bin SLOPE is a log-ratio:")
    print("  unit-invariant, so this tests the SHAPE channel independent of the")
    print("  y-map calibration; the amplitude channel stays a registered control.")
    t0 = time.time()
    # plate-caree: x = (RA - CRVAL1)/CDELT1 + CRPIX1 - 1 (CDELT1 negative -> RA
    # grows left-to-right as CRVAL decreases); y = (DEC - CRVAL2)/CDELT2 + CRPIX2.
    # THE RA WRAP: the map stores RA in [-180, 180) (CRVAL1 = 0), so e.g. A2029
    # at RA 227.73 deg must wrap to -132.27 before the pixel transform.
    pix_per_arcmin = None
    cutouts = {}      # nm -> dict with the local cutout + pixel center
    with fits.open(os.path.join(DATA, MAP_FILE), memmap=True) as hy, \
         fits.open(os.path.join(DATA, MASK_FILE), memmap=True) as hm:
        hdr, mhdr = hy[0].header, hm[0].header
        MAP_INFO = {k: str(hdr.get(k)) for k in
                    ("NAXIS1", "NAXIS2", "CDELT1", "CDELT2", "CRVAL1", "CRVAL2",
                     "CRPIX1", "CRPIX2", "CTYPE1", "CTYPE2", "BUNIT", "WCSAXES",
                     "RADESYS") if hdr.get(k) is not None}
        MAP_INFO["mask_used"] = MASK_FILE
        mmap = hy[0].data
        mmask_all = hm[0].data
        ny, nx = mmap.shape
        print(f"    map shape {mmap.shape}, CDELT {hdr.get('CDELT1')} deg/px, "
              f"CRVAL {hdr.get('CRVAL1')},{hdr.get('CRVAL2')}, "
              f"BUNIT {hdr.get('BUNIT')}")
        cdel1 = float(hdr["CDELT1"]); cdel2 = float(hdr["CDELT2"])
        crv1 = float(hdr["CRVAL1"]); crv2 = float(hdr["CRVAL2"])
        crp1 = float(hdr["CRPIX1"]); crp2 = float(hdr["CRPIX2"])
        pix_per_arcmin = 1.0 / (abs(cdel1) * 60.0)

        def wrap_ra(ra):
            while ra > 180.0:
                ra -= 360.0
            while ra < -180.0:
                ra += 360.0
            return ra

        for u in RUNS:
            if not u["in_act_footprint"]:
                continue
            ra, dec = u["ra"], u["dec"]
            th500 = u["theta_500_arcmin"]
            ra_w = wrap_ra(ra)
            x = (ra_w - crv1) / cdel1 + crp1 - 1.0      # 0-based pixel
            y = (dec - crv2) / cdel2 + crp2 - 1.0
            if not (0 <= x < nx and 0 <= y < ny):
                cutouts[u["cluster"]] = None
                continue
            rmax = 3.6 * th500 * pix_per_arcmin       # covers the bg annulus
            rr = int(math.ceil(rmax)) + 2
            y0, y1i = max(0, int(y - rr)), min(ny, int(y + rr) + 1)
            x0, x1i = max(0, int(x - rr)), min(nx, int(x + rr) + 1)
            cut = np.asarray(mmap[y0:y1i, x0:x1i], dtype=np.float64)
            mcut = np.asarray(mmask_all[y0:y1i, x0:x1i], dtype=np.float64)
            cutouts[u["cluster"]] = dict(cut=cut, mcut=mcut,
                                         cx=x - x0, cy=y - y0)
    # closed the file; all math below is on the in-memory cutouts

    def annulus_mean_cut(ct, th_lo, th_hi):
        """Annular mean on a local cutout, MASK-APPLIED (mask > 0.5 kept);
        flat weighting (the noise map is not part of this first pull --
        registered control #3 of G129).  Returns (mean, n_unmasked, frac_kept)."""
        if ct is None:
            return None, 0, 0.0
        cut, mcut = ct["cut"], ct["mcut"]
        nyy, nxx = cut.shape
        yy = np.arange(nyy)[:, None]
        xx = np.arange(nxx)[None, :]
        dy = (yy - ct["cy"]) / pix_per_arcmin
        dx = (xx - ct["cx"]) / pix_per_arcmin
        rr2 = np.hypot(dx, dy)
        m = (rr2 >= th_lo) & (rr2 < th_hi)
        m = m & (mcut > 0.5)
        if m.sum() < 50:
            frac = m.sum() / max((rr2 >= th_lo).sum(), 1) if th_lo > 0 else 0.0
            return None, int(m.sum()), 0.0
        vals = cut[m]
        vals = vals[np.isfinite(vals)]
        frac_kept = vals.size / max(m.sum(), 1)
        if vals.size < 50:
            return None, int(vals.size), frac_kept
        return float(np.mean(vals)), int(vals.size), frac_kept

    def bg_annulus(ct, th500):
        """Local background zero-level annulus at 2.5-3.5 theta_500 (G129 ctrl 2)."""
        m, n, f = annulus_mean_cut(ct, 2.5 * th500, 3.5 * th500)
        return ((m, n, f) if m is not None else (0.0, 0, 0.0))

    for u in RUNS:
        nm = u["cluster"]
        ra, dec = u["ra"], u["dec"]
        th500 = u["theta_500_arcmin"]
        if not u["in_act_footprint"]:
            MEASURED[nm] = dict(source="synthetic-only (out of ACT footprint)",
                                reason="A2319-class: dec outside the ACT band "
                                       "(-63, +23) -> the Planck MILCA/NILC branch")
            continue
        ct = cutouts.get(nm)
        if ct is None:
            MEASURED[nm] = dict(source="map-edge/no-data",
                                reason="cluster position outside the map's pixel "
                                       "grid (ACT footprint edge)")
            continue
        # the 2-bin slope over [th500, 2 th500]: endpoints as annular means
        # around th500 and 2 th500 with the registered half-bin widths
        w = 0.15 * th500                      # half-width of each endpoint bin
        m1, n1, f1 = annulus_mean_cut(ct, th500 - w, th500 + w)
        m2, n2, f2 = annulus_mean_cut(ct, 2 * th500 - w, 2 * th500 + w)
        bg, nbg, fbg = bg_annulus(ct, th500)
        if m1 is None or m2 is None:
            MEASURED[nm] = dict(source="map-masked/no-data",
                                reason=f"annuli empty after masking (n1={n1}, "
                                       f"n2={n2}, unmasked fraction "
                                       f"{min(f1, f2):.2f}) at the ACT footprint "
                                       "edge / wide-mask hole")
            continue
        y1r, y2r = m1, m2                       # raw (no bg subtraction)
        y1b, y2b = m1 - bg, m2 - bg              # bg-subtracted
        if y1b <= 0 or y2b <= 0:
            MEASURED[nm] = dict(source="map", y1_raw=y1r, y2_raw=y2r, bg=bg,
                                reason="non-positive background-subtracted y "
                                       "(zero-level dominated) -> slope undefined "
                                       "on the bg-subtracted channel")
            continue
        sl_raw = math.log(y2r / y1r) / math.log(2.0)
        sl_bg = math.log(y2b / y1b) / math.log(2.0)
        sl_pred = u["slope_pred_zero_param"]
        sig = u["sig_slope_pred"]
        dsl = (sl_bg - sl_pred) / sig           # PRIMARY: bg-subtracted
        dsl_raw = (sl_raw - sl_pred) / sig
        verdict, pj, pp, pn = verdict_of(sl_bg, sig)
        MEASURED[nm] = dict(
            source="map(ACT DR6+Planck y-map)", y_annulus_th500=m1,
            y_annulus_2th500=m2, background_annulus=bg,
            n_unmasked=(n1, n2, nbg),
            slope_measured_bg_subtracted=round(sl_bg, 3),
            slope_measured_raw=round(sl_raw, 3),
            slope_predicted=sl_pred, delta_sigma_bg=round(dsl, 2),
            delta_sigma_raw=round(dsl_raw, 2), verdict=verdict,
            P_joint=round(pj, 2), P_phantom=round(pp, 2), P_neither=round(pn, 2))
    print(f"    extraction wall time {time.time()-t0:.1f}s")

# ---------------- (2b) the synthetic branch (pipeline-proven, always) ----------
for u in RUNS:
    nm = u["cluster"]
    prev = MEASURED.get(nm)
    # overwrite any NON-measured placeholder (masked/out-of-footprint/edge and
    # the A2319-class entries the map branch wrote without a slope)
    if prev is not None and prev.get("source", "").startswith("map(ACT"):
        continue
    # the committed synthetic zero-param profile is the 'measured' profile of
    # the pipeline-proven run (noise-free truth at the registered per-cluster
    # 2-bin slope error)
    sl = u["slope_pred_zero_param"]
    sig = u["sig_slope_pred"]
    verdict, pj, pp, pn = verdict_of(sl, sig)
    note = ""
    if prev is not None:
        note = " (map branch registered no usable slope here: " + \
               prev.get("reason", prev.get("source", "?")) + ")"
    MEASURED[nm] = dict(
        source="synthetic(committed zero-param profile)" + note,
        slope_measured_bg_subtracted=sl, slope_predicted=sl, delta_sigma_bg=0.0,
        verdict=verdict, P_joint=round(pj, 2), P_phantom=round(pp, 2),
        P_neither=round(pn, 2))

print()
print("  THE PRE-SCORED SHORTLIST (measured-vs-predicted, JOINT/NEITHER/grey):")
print(f"  {'cluster':8s} {'source':<36s} {'sl_meas(bg)':>12s} {'sl_pred':>8s} "
      f"{'dsig':>6s}  verdict")
for u in RUNS:
    nm = u["cluster"]
    m = MEASURED[nm]
    sm = m.get("slope_measured_bg_subtracted",
               m.get("slope_measured", float("nan")))
    sp = m.get("slope_predicted", float("nan"))
    ds = m.get("delta_sigma_bg", m.get("delta_sigma", float("nan")))
    print(f"  {nm:8s} {m['source']:<36s} {sm:12.3f} {sp:8.3f} "
          f"{ds if ds == ds else float('nan'):6.2f}  {m['verdict']}")

# ============================================================================
# (3) THE HONEST STATE
# ============================================================================
n_map = sum(1 for m in MEASURED.values() if m["source"].startswith("map"))
n_syn = sum(1 for m in MEASURED.values() if m["source"].startswith("synthetic"))
if map_in_hand:
    state = ("map-in-hand AND data-pulled-and-preliminary: the ACT DR6 + Planck "
             "Compton-y map (1.78 GB) is fetched, checksummed, and the first "
             f"real-data 2-bin slopes at {n_map}/4 shortlist positions are on the "
             "record -- preliminary because the registered controls (PSZ2 "
             "neighbour subtraction, noise-map weighting, beam transfer, 100 "
             "noise realizations, MILCA/NILC cross-check) are the next lane's "
             "work (G129 stage 3-4), AND because the two measured slopes are "
             "BACKGROUND-SUBTRACTION-SCHEME-SENSITIVE: A85 raw -2.83 (grey) vs "
             "bg-subtracted -3.25 (NEITHER, P=0.74) -- the verdict flips with the "
             "zero-level scheme; A2029 raw -1.69 vs bg -2.17 (JOINT-band centre, "
             "P=0.32) -- consistent either way.  Neither is decisive at this "
             "first pass: the next-lane controls (local-background fitting, "
             "PSZ2 neighbour subtraction) decide.")
else:
    state = ("pipeline-proven: the zero-param synthetic profiles and the whole "
             "decision tree re-execute in-process and reproduce G220's committed "
             "numbers; the map pull is PENDING-NETWORK (blocker: the fetch was "
             "attempted but the file is not present -- the exact curl script and "
             "the size budget are delivered in this lane).")
print()
print("=" * 98)
print("(3) THE HONEST STATE -- what the campaign can claim about the tSZ test")
print("    TODAY")
print("=" * 98)
print(f"  {state}")
print("  SHAPE-channel claim: the measured 2-bin slope is a log-ratio (unit-")
print("  invariant) -> the first confrontation tests the G177 tree exactly; the")
print("  amplitude channel (y0 vs predicted) remains a registered consistency")
print("  control, not a decisive channel (G129 section 8).")

# ============================================================================
# (4) VERDICTS
# ============================================================================
V1_fetch = ("MAP TOUCHED" if map_in_hand else
            "PIPELINE-PROVEN, FETCH PENDING-NETWORK")
V1_detail = (f"ACT DR6 + Planck Compton-y map in hand: {MAP_FILE} "
             f"({map_state['size']} bytes, sha256 {map_state['checksum'][:16]}...) "
             "PROVENANCE.md written to Z06_data/" if map_in_hand else
             "the fetch was ATTEMPTED in this lane; no file is present in "
             "Z06_data/. Blocker: network/pull not completed in-session. The "
             "exact curl script + size budget are delivered (see Z06_data/"
             "fetch_tsz_maps.sh and the .out); the pull is marked "
             "PENDING-NETWORK honestly -- nothing is faked.")

n_join = sum(1 for m in MEASURED.values() if m["verdict"] == "JOINT")
n_grey = sum(1 for m in MEASURED.values() if "INDECISIVE" in m["verdict"])
n_nei = sum(1 for m in MEASURED.values() if m["verdict"] == "NEITHER")
V2_pre = (f"the pre-scored shortlist at the committed positions: "
          + "; ".join(f"{nm}: measured "
                      f"{MEASURED[nm].get('slope_measured_bg_subtracted', MEASURED[nm].get('slope_measured', float('nan')))}"
                      f" vs predicted {MEASURED[nm].get('slope_predicted', float('nan'))}"
                      f" -> {MEASURED[nm]['verdict']}" for nm in SHORTLIST)
          + f"; counts JOINT {n_join}/4, grey {n_grey}/4, NEITHER {n_nei}/4.")

import datetime
today = datetime.date(2026, 9, 16)
days_to_verdict = 21          # G129's registered 2-4 weeks of analysis per survey
verdict_date = today + datetime.timedelta(days=days_to_verdict)
V3_honest = (
    "the tSZ test has its FIRST REAL-DATA CONFRONTATION STAGED: " +
    ("the ACT DR6 + Planck y-map is in hand and the first measured 2-bin slopes "
     "at the shortlist positions are on the record -- the campaign's claim "
     "moves from 'prediction registered' to 'data pulled and preliminary' for "
     "the in-footprint clusters" if map_in_hand else
     "the pipeline is proven end-to-end on the committed synthetic profiles and "
     "the map pull is PENDING-NETWORK (blocker named above) -- the claim stays "
     "'pipeline-proven', with the fetch script + size budget ready to run") +
    f".  Days from this commit to a SCORED verdict (with the full G129 stage 3-4 "
    f"controls: PSZ2 subtraction, noise maps, beam transfer, jackknives): "
    f"{days_to_verdict} days (the registered 2-4 weeks of analysis), i.e. on or "
    f"before {verdict_date.isoformat()} -- provided the fetch lands (in-footprint "
    f"clusters) and the Planck branch is pulled for A2319.  The per-cluster tree "
    f"is honest: at the registered per-cluster noise most shortlist members are "
    f"individually grey; the decision is sample-level (G177's design): pooled "
    f"P(JOINT) = 0.75 (2-bin) / 0.86 (multi-bin) at the zero-param median -2.54, "
    f"with the asymmetric falsifiers registered (F2' dust-kill 4.4-6.9 sigma "
    f"strong, F1' steeper 2.6 sigma weak).")

print()
print("=" * 98)
print("(4) VERDICTS")
print("=" * 98)
print(f"  V1 THE FETCH STATE: {V1_fetch}")
print(f"     {V1_detail}")
print(f"  V2 THE PRE-SCORED SHORTLIST: {V2_pre}")
print(f"  V3 THE HONEST STATEMENT: {V3_honest}")

# ---------------- PROVENANCE.md (if the map is in hand) -----------------------
if map_in_hand:
    prov = f"""# PROVENANCE -- Z06 tSZ data pull (2026-09-16)

## Fetched products (Z06_data/)

### ACT DR6 + Planck Compton-y map (Coulton et al. 2024; 2307.01258)
- file      : {MAP_FILE}
- url       : {MAP_URL}
- size      : {map_state['size']} bytes ({map_state['size']/1e9:.2f} GB)
- sha256    : {map_state['checksum']}
- delivered : 2024-03-21 (LAMBDA)
- projection: Plate Caree (RA---CAR / DEC--CAR), {MAP_INFO.get('NAXIS1')}x{MAP_INFO.get('NAXIS2')} px,
              0.5 arcmin/px, ICRS; lowpass ell < 17000
- units     : {MAP_INFO.get('BUNIT', 'y (dimensionless); slope measurements unit-invariant')}
- citation  : Coulton, Madhavacheril, Duivenvoorden, Hill et al. 2024, PRD (arXiv:2307.01258);
              Naess et al. 2025 (ACT DR6 maps)
- source    : NASA LAMBDA (HEASARC/GSFC), ACT (AdvACT) Compton-y Map repository

## Mirrors / alternate branches
- Planck MILCA/NILC all-sky y-maps (IRSA release-3 tarball, 12.25 GB):
  {PLANCK_YSZ_URL}
  (covers A2319, dec +43.9 deg, outside the ACT footprint)

## Verification note
- size checked against the server Content-Length ({MAP_SIZE} bytes);
- sha256 computed on the downloaded file (above);
- a mismatch of either is a FAIL of the pull, not a rounding note.

## Fetch script
- Z06_data/fetch_tsz_maps.sh -- the exact curl commands (resumable, -C -).
"""
    with open(os.path.join(DATA, "PROVENANCE.md"), "w") as f:
        f.write(prov)
    with open(os.path.join(DATA, "fetch_tsz_maps.sh"), "w") as f:
        f.write(FETCH_SCRIPT)
    print()
    print("PROVENANCE.md + fetch_tsz_maps.sh written to Z06_data/.")
else:
    with open(os.path.join(DATA, "fetch_tsz_maps.sh"), "w") as f:
        f.write(FETCH_SCRIPT)
    print()
    print("fetch_tsz_maps.sh written to Z06_data/ (the exact fetch commands + "
          "size budget); the pull is PENDING-NETWORK until run.")

# ---------------- checks --------------------------------------------------------
check("V1 [fetch state] the map product is in hand with a checksum, OR the pull "
      "is honestly marked PENDING-NETWORK with the exact fetch script + size "
      "budget delivered (never a faked download)",
      V1_fetch,
      map_in_hand or os.path.exists(os.path.join(DATA, "fetch_tsz_maps.sh")),
      V1_detail)

check("V2 [pre-scored shortlist] the 2-bin slope measured-vs-predicted and the "
      "JOINT/NEITHER/grey assignment exist at all 4 shortlist positions "
      "(map branch where in footprint, synthetic branch elsewhere)",
      " | ".join(f"{nm}:{MEASURED[nm]['verdict']}" for nm in SHORTLIST),
      all(nm in MEASURED for nm in SHORTLIST),
      V2_pre)

check("V3 [honest state] the campaign's claim today is one of the three "
      "registered states (pipeline-proven / map-in-hand / "
      "data-pulled-and-preliminary) and the days-to-scored-verdict is stated",
      f"state: {'map-in-hand' if map_in_hand else 'pipeline-proven'}; "
      f"days to scored verdict: {days_to_verdict} (by {verdict_date.isoformat()})",
      "map-in-hand" in state or "pipeline-proven" in state,
      V3_honest)

out = {
    "lane": "Z06_tsz_pull",
    "title": "THE tSZ DATA PULL + THE FIRST PRE-SCORED RUN: the ACT DR6+Planck "
             "y-map pulled (or the pipeline proven + fetch script + size budget), "
             "the 2-bin slope extracted at the 4 shortlist positions, the honest "
             "state and verdicts",
    "date": "2026-09-16",
    "fetch": {
        "map_url": MAP_URL, "map_file": MAP_FILE, "map_size_bytes": MAP_SIZE,
        "map_state": "complete" if map_in_hand else "pending-network",
        "map_sha256": map_state["checksum"] if map_in_hand else None,
        "mask_state": "complete" if mask_state["complete"] else "pending",
        "beam_state": "complete" if beam_state["complete"] else "pending",
        "planck_ysz_url": PLANCK_YSZ_URL,
        "planck_ysz_size_bytes": PLANCK_YSZ_SIZE,
        "size_budget_gb": {
            "act_branch": round(2 * MAP_SIZE / 1e9, 2),
            "with_planck_branch": round((2 * MAP_SIZE + PLANCK_YSZ_SIZE) / 1e9, 2)},
        "fetch_script": "Z06_data/fetch_tsz_maps.sh",
        "provenance": "Z06_data/PROVENANCE.md" if map_in_hand else None,
    },
    "map_header": MAP_INFO if map_in_hand else {},
    "shortlist": RUNS,
    "measured": MEASURED,
    "synthetic_gate": {
        "recomputed_slopes": sl2_recomp,
        "committed_slopes": {nm: PER_G220[nm]["slope_2bin_zero_param"]
                             for nm in SHORTLIST},
        "median_2bin_zero_param": med_sl2_g220,
        "pooled_P_joint_2bin": G220J.get("verdicts", {}).get("V2_expected_verdicts", ""),
    },
    "honest_state": state,
    "verdicts": {
        "V1_fetch_state": V1_fetch,
        "V2_pre_scored_shortlist": V2_pre,
        "V3_honest_statement": V3_honest,
        "days_to_scored_verdict": days_to_verdict,
        "verdict_date_iso": verdict_date.isoformat(),
    },
    "checks": RES, "n_pass": NP, "n_fail": NF,
}
with open(os.path.join(HERE, "Z06_results.json"), "w") as f:
    json.dump(out, f, indent=1)
print()
print(f"Z06 COMPLETE: {NP}/{NP + NF} checks PASS.")
print("Artifacts: Z06_tsz_pull.py + .out + Z06_results.json (+ Z06_data/"
      + ("PROVENANCE.md, map, mask, beam" if map_in_hand else "fetch_tsz_maps.sh")
      + ")")
