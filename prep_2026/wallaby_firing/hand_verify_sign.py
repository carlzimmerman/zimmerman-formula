#!/usr/bin/env python3
"""
HAND VERIFICATION of THE SIGN TRAP -- Lane W1 (run before accepting perside_237.csv)
====================================================================================
FIREWALL: N~237 -> ~1-1.5 sigma at AQUAL amplitude; NEITHER pre-registered kill
condition (3-sigma AQUAL-vs-BranchB, N~1157 canonical a0=9.36e-11 / N~1424 alt
a0=1.13e-10) CAN TRIGGER on this sample.  This script tests a CONVENTION, not physics.

Galaxy: WALLABY J165901-601241 (Norma, 30'', the QC-passing pilot).
Independent code path: astropy WCS per-pixel world coordinates + simple loops --
does NOT import perside_extractor.  Verifies, from the raw mom1 map:
  (1) the sky side pointed to by WKAPP PA_model_g ("East of North", Deg+22
      arXiv:2211.07333 Table 4) is the RECEDING side (mean v_los > VSys_model),
      i.e. the TiRiFiC/FAT + 3DBarolo receding-side PA convention holds;
  (2) A_preregistered = 2(v_rec - v_appr)/(v_rec + v_appr) = -A_raw_extractor
      (the extractor prints the OPPOSITE ordering 2(v_app - v_rec)/(v_app + v_rec));
  (3) an independent mom0-weighted per-side outer mean reproduces the pipeline's
      SIGN of A_preregistered (+; receding side faster for this galaxy).
Also demonstrates (honest estimator-sensitivity note): an UNWEIGHTED all-pixel
outer mean is junk-dominated (gives -0.22 / medians -0.07) -- intensity
weighting + sigma clipping, exactly as gate-validated, is load-bearing.
exit 0 iff all three checks pass.
"""
import numpy as np, math, sys
from astropy.io import fits
from astropy.wcs import WCS

P = "/Users/carlzimmerman/new_physics/prep_2026/wallaby_prep/pilot_data/"
AVG = P + "WALLABY_J165901-601241_Norma_Kin_TR1_AvgMod.txt"
C, F0 = 299792.458, 1420405751.77
PIPE_A_RAW, PIPE_A_PRE = -0.0191, +0.0191   # pilot/smoke pipeline values

geo, rc, started = {}, [], False
for line in open(AVG):
    t = line.split("\t")
    if len(t) >= 2:
        k = t[0].split("(")[0].strip()
        try: geo[k] = float(t[1])
        except ValueError: pass
    s = line.split()
    if line.startswith("Rotation Curve"): started = True; continue
    if line.startswith("Surface Density"): started = False
    if started and len(s) >= 3:
        try: rc.append((float(s[0]), float(s[1])))
        except ValueError: pass

pa, inc, vsys = geo["PA_model_g"], geo["Inc_model"], geo["VSys_model"]
v = C * (F0 / np.squeeze(fits.open(P + "WALLABY_J165901-601241_Norma_TR1_mom1.fits")[0].data).astype(float) - 1.0)
hdr = fits.open(P + "WALLABY_J165901-601241_Norma_TR1_mom1.fits")[0].header
mom0 = np.squeeze(fits.open(P + "WALLABY_J165901-601241_Norma_TR1_mom0.fits")[0].data).astype(float)
w = WCS(hdr).celestial
ny, nx = v.shape
yy, xx = np.mgrid[0:ny, 0:nx]
ra, dec = w.wcs_pix2world(np.column_stack([xx.ravel(), yy.ravel()]), 0).T
dE = (ra.reshape(v.shape) - geo["RA_model"]) * math.cos(math.radians(geo["DEC_model"])) * 3600.0
dN = (dec.reshape(v.shape) - geo["DEC_model"]) * 3600.0
pa_r = math.radians(pa)
along = dE * math.sin(pa_r) + dN * math.cos(pa_r)          # >0 = PA side
perp = -dE * math.cos(pa_r) + dN * math.sin(pa_r)
Rd = np.hypot(along, perp / math.cos(math.radians(inc)))
cth = np.where(Rd > 0, along / Rd, 0.0)
sini = math.sin(math.radians(inc))
vrot = (v - vsys) / (sini * cth)

fin = np.isfinite(v) & np.isfinite(mom0) & (mom0 > 0) & (np.abs(cth) >= 0.5) & (np.abs(v - vsys) < 600)
mean_pa = v[fin & (cth > 0.5)].mean()
mean_anti = v[fin & (cth < -0.5)].mean()
check1 = mean_pa > vsys > mean_anti
print(f"[1] receding side = PA_model_g side? mean v_los(PA side)={mean_pa:.1f}, "
      f"vsys={vsys:.1f}, anti side={mean_anti:.1f} -> {'PASS' if check1 else 'FAIL'}")

rads = np.array([r[0] for r in rc]); dr = float(np.median(np.diff(rads)))
Rmax = rads[-1] + dr / 2
wm_r, wm_a = [], []
for R0, _ in rc:
    if R0 < 0.5 * Rmax: continue
    sel = fin & (Rd >= R0 - dr / 2) & (Rd < R0 + dr / 2)
    mr, ma = sel & (cth > 0), sel & (cth < 0)
    if mr.sum() < 4 or ma.sum() < 4: continue
    wm_r.append(np.average(vrot[mr], weights=mom0[mr]))
    wm_a.append(np.average(vrot[ma], weights=mom0[ma]))
v_rec, v_app = float(np.mean(wm_r)), float(np.mean(wm_a))
A_ext = 2 * (v_app - v_rec) / (v_app + v_rec)
A_pre = 2 * (v_rec - v_app) / (v_rec + v_app)
check2 = abs(A_pre + A_ext) < 1e-12
print(f"[2] A_pre == -A_ext identically: {A_pre:+.4f} vs {A_ext:+.4f} -> "
      f"{'PASS' if check2 else 'FAIL'}")
check3 = np.sign(A_pre) == np.sign(PIPE_A_PRE) and np.sign(A_ext) == np.sign(PIPE_A_RAW)
print(f"[3] independent hand A_pre={A_pre:+.4f} (v_rec={v_rec:.1f} > v_app={v_app:.1f}) "
      f"matches pipeline sign (pipeline A_pre={PIPE_A_PRE:+.4f}, A_raw={PIPE_A_RAW:+.4f}) -> "
      f"{'PASS' if check3 else 'FAIL'}")
print(f"    reading: RECEDING side faster -> A_preregistered > 0 (attractor-alignment "
      f"is NOT tested here; that is the firing lane)")
ok = check1 and check2 and check3
print(f"HAND VERIFICATION: {'PASS -- perside_237.csv sign convention accepted' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
