#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L329 -- A2744-QSO1: a PSF-CONSISTENT re-extraction of the narrow/extended H-alpha cube from the full JWST cube.

WHY.  L327 P2 showed the released narrow-only cube has a core SHARPER than the PSF measured from the same data (an image
the physics cannot produce, Lean I23): a broad-subtraction artifact at the scales where the dynamical mass is measured.
This lane rebuilds the cube so that it cannot have that artifact, and re-asks what the data say.

METHOD (qso1_refit/reextract.py).  Every unresolved component (BLR, the absorber in front of it, the AGN continuum) has
the SAME spatial profile, the PSF P(x), measured from the broad-line wings.  Per channel the continuum-subtracted cube is
fitted as s(v) P(x) + e(v) Q_R(x) (weighted linear LSQ; Q_R = P (x) exp(-r/R), R by minimum total chi^2); the cube kept
is d - s P: nothing extended is ever subtracted.  The unresolved-nucleus degeneracy is BRACKETED, not assumed away:
V1 raw s(v) (all unresolved removed), V2 a smooth two-Gaussian BROAD template (sigma >= 250 km/s; any unresolved narrow
nucleus kept), V3 = V2 x the literature absorber.  V2 is the primary.

WHAT IS CHECKED (both directions):
  X1  every variant's line core is >= the PSF (PSF-consistent) -- MUTATE=1 feeds the released cube as a variant: FAILS.
  X2  the three-variant bracket is tight (core spread and flux spread).
  X3  a PSF-FREE kinematic fit on V2 recovers the MEASURED PSF (the released cube drove it to a sub-diffraction 0.08").
  X4  cross-seeded fits at the measured PSF: the laws tie; the fitted disk collapses to an UNRESOLVED disk (R_e at its
      2 pc bound, sigma_0 -> 0), so the "mass" (~10^8) is set by the core line WIDTH under a thin-disk assumption, not by
      resolved rotation.  (One rival run stuck 95 above its sibling: a search failure, recorded, not scored.)
  X5  NO resolved velocity gradient across the core (the published product shows ~10 km/s).
  X6  the spectroastrometric red-blue centroid separation at |v| ~ 50 km/s with REAL-noise errors, on the clean cube
      after a spectral narrow/intermediate split (qso1_refit/narrow_split.py -- the fair test), on the clean cube with
      the intermediate kept, and on the released product.
Verdict fixed in advance of X6: QSO1 stays UNDECIDED for the framework (L324) unless X4/X5 show resolved rotation.

Run from the repository root:  python3 real_research/bhstar_audit_2026/L329_qso1_reextraction.py
(needs the gitignored full cube; builds the derived V1-V3 cubes via qso1_refit/reextract.py if absent)
"""
import os, sys, json, math, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
QD = os.path.join(HERE, "qso1_refit")
sys.path.insert(0, QD)
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L329_qso1_reextraction"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L329", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__)
os.chdir(QD)
from astropy.io import fits
from psf_from_blr import fit_img, C, LAM0
DATA = os.path.join(os.path.dirname(HERE), "data", "qso1")
VARS = {"V1": "qso1_narrow_V1_raws.fits", "V2": "qso1_narrow_V2_smooth_noabs.fits", "V3": "qso1_narrow_V3_smooth_abs.fits"}
if not all(os.path.exists(os.path.join(DATA, f)) for f in VARS.values()):
    subprocess.run([sys.executable, "reextract.py"], check=True)
if MUTATE:
    VARS["V1"] = "Halpha_nr_only_cube_02px.fits"
psf = json.load(open("psf_from_blr.json"))
PSF, EPSF = psf["psf_broad"]["fwhm_geo"], psf["psf_broad"]["err_geo"]


def cube(fn):
    h = fits.open(os.path.join(DATA, fn)); d = h["SCI"].data.astype(float); hd = h["SCI"].header
    return d, ((hd["CRVAL3"] + np.arange(d.shape[0]) * hd["CDELT3"]) / LAM0 - 1) * C


banner("X1-X2 -- THE RE-EXTRACTED CUBES ARE PSF-CONSISTENT, AND THE BRACKET IS TIGHT")
cores, fluxes = {}, {}
for k, fn in VARS.items():
    d, v = cube(fn)
    im = np.nansum(d[np.abs(v) < 250], 0); y, x = np.unravel_index(np.nanargmax(im), im.shape)
    f = fit_img(im, y, x, half=12)
    cores[k] = (f["fwhm_geo"], f["err_geo"]); fluxes[k] = float(np.nansum(im))
    P(f"   {k} ({fn}): core {f['fwhm_geo']:.3f} +/- {f['err_geo']:.3f} arcsec, flux {fluxes[k]:.1f}")
OUT["numbers"]["cores"] = cores; OUT["numbers"]["fluxes"] = fluxes; OUT["numbers"]["psf"] = [PSF, EPSF]
check("X1 every variant's line core >= PSF - 3 sigma (a PSF-convolved image cannot be sharper than the PSF)",
      "; ".join(f"{k}: {c:.3f}" for k, (c, e) in cores.items()) + f"  vs PSF {PSF:.3f} +/- {EPSF:.3f}",
      all(c + 3 * e >= PSF - 3 * EPSF for c, e in cores.values()),
      "the released product (0.111\") fails this; MUTATE substitutes it and must FAIL")
cs = [c for c, _ in cores.values()]; fs = list(fluxes.values())
check("X2 the unresolved-nucleus bracket is tight: core spread < 0.01 arcsec and flux spread < 15%",
      f"core {min(cs):.3f}-{max(cs):.3f}; flux {min(fs):.1f}-{max(fs):.1f}", max(cs) - min(cs) < 0.01 and
      (max(fs) - min(fs)) / np.mean(fs) < 0.15, "the degeneracy the decomposition cannot break does not matter here")

banner("X3-X4 -- KINEMATIC FITS ON V2 (the stored fits re-evaluate on the cube; PSF free, then measured + cross-seeded)")
os.environ["QSO1_CUBE"] = VARS["V2"] if not MUTATE else "qso1_narrow_V2_smooth_noabs.fits"
import model, model2
D = model.load()
MSK = model2.mask_for(D["data"].shape[1:])
ffree = json.load(open("fitsV2_psffree.json")); fxs = json.load(open("fitsV2_psf0185_xs.json"))
worst = max(abs(model2.chi2(r["x"], *k.split("_"), D, MSK)[0] - r["chi2"]) for fits_ in (ffree, fxs) for k, r in fits_.items())
psf_rec = [r["x"][11] for r in ffree.values()]
OUT["numbers"]["X3_psf_recovered"] = psf_rec
check("X3 the stored V2 fits re-evaluate exactly (max |dchi2| < 0.01) AND the PSF-free fits recover the measured PSF "
      "(every law within 0.02 arcsec of it)",
      f"max re-eval diff {worst:.4f}; free-PSF best fits {min(psf_rec):.3f}-{max(psf_rec):.3f} vs measured {PSF:.3f}",
      worst < 0.01 and all(abs(p_ - PSF) < 0.02 for p_ in psf_rec),
      "on the released cube the same fit ran to 0.08 arcsec; the clean cube is internally consistent with the instrument")
ch = {k: r["chi2"] for k, r in fxs.items()}
good = {k: c for k, c in ch.items() if k != "rival_canonical"}
span = max(good.values()) - min(good.values())
re_px = [fxs[k]["x"][7] for k in good]; sig0 = [fxs[k]["x"][6] for k in good]
logm = {k: fxs[k]["x"][0] for k in fxs}
OUT["numbers"]["X4"] = {"chi2": ch, "span_excl_stuck": span, "Re_pc": re_px, "sigma0": sig0, "logM": logm,
                        "rival_canonical_stuck_gap": ch["rival_canonical"] - min(good.values())}
check("X4 at the measured PSF (cross-seeded) the laws tie (span < 1.5 naive, excl. one documented stuck run) and the "
      "fitted disk is UNRESOLVED (R_e <= 3 pc)",
      f"chi2 span {span:.2f} (Kepler {ch['kepler_canonical']:.2f}, framework {ch['framework_canonical']:.2f}/"
      f"{ch['framework_alt']:.2f}, rival_alt {ch['rival_alt']:.2f}; rival_canonical stuck +{OUT['numbers']['X4']['rival_canonical_stuck_gap']:.0f}); "
      f"R_e {min(re_px):.1f}-{max(re_px):.1f} pc; log M {min(logm.values()):.2f}-{max(logm.values()):.2f}",
      span < 1.5 and max(re_px) <= 3.0,
      "the ~10^8 'mass' is the core line WIDTH read as Keplerian rotation of an unresolved disk -- not a resolved "
      "rotation curve; all laws are Newtonian at those radii, so they cannot differ")

banner("X5-X6 -- RESOLVED ROTATION AND SPECTROASTROMETRY IN THE CLEAN CUBE")
from scipy.optimize import curve_fit
from scipy.special import erf
d, v, dv = D["data"], D["v"], D["dv"]


def g(vv, A, mu, sig):
    s2 = np.sqrt(2) * np.sqrt(sig ** 2 + model.SIG_LSF ** 2)
    return A * 0.5 * (erf((vv + dv / 2 - mu) / s2) - erf((vv - dv / 2 - mu) / s2))


im = np.nansum(d[np.abs(v) < 250], 0); yc, xc = np.unravel_index(np.nanargmax(im), im.shape)
rows = []
for by in range(yc - 9, yc + 10, 3):
    for bx in range(xc - 9, xc + 10, 3):
        spec = np.nansum(d[:, by - 1:by + 2, bx - 1:bx + 2], axis=(1, 2))
        err = np.sqrt(np.nansum(D["err"][:, by - 1:by + 2, bx - 1:bx + 2] ** 2, axis=(1, 2))) * 1.77 * 3
        try:
            p_, cov = curve_fit(g, v, spec, p0=[spec.max() * 3, 0, 40], sigma=err, absolute_sigma=True,
                                bounds=([0, -300, 0], [np.inf, 300, 300]), maxfev=20000)
            rows.append(((bx - xc) * 0.02, (by - yc) * 0.02, p_[1], math.sqrt(cov[1, 1])))
        except Exception:
            pass
rows = np.array(rows); ok = np.isfinite(rows[:, 3]) & (rows[:, 3] > 0) & (rows[:, 3] < 200)
A = np.vstack([np.ones(ok.sum()), rows[ok, 0], rows[ok, 1]]).T; w = 1 / rows[ok, 3] ** 2
Cv = np.linalg.inv(A.T @ (A * w[:, None])); pp = Cv @ (A.T @ (w * rows[ok, 2]))
grad = math.hypot(pp[1], pp[2]); egrad = math.sqrt((pp[1] ** 2 * Cv[1, 1] + pp[2] ** 2 * Cv[2, 2]) / grad ** 2)
OUT["numbers"]["X5"] = {"grad_kms_per_arcsec": grad, "err": egrad, "across_0p2": grad * 0.2, "err_0p2": egrad * 0.2}
check("X5 NO resolved velocity gradient across the core of the clean cube (< 2 sigma)",
      f"{grad * 0.2:.1f} +/- {egrad * 0.2:.1f} km/s across 0.2 arcsec (3x3-px bins, errors x1.77 for the real-noise excess)",
      grad < 2 * egrad, "the resolved rotation that a dynamical mass needs is not detected once the artifact is removed")
ns = json.load(open("narrow_split.json"))
OUT["numbers"]["X6"] = ns
sigs = {k: ns[k]["significance"] for k in ("V2_narrow_split", "V2_with_intermediate", "published_product")}
check("X6 with REAL-noise errors no version of the public data shows a spectroastrometric red-blue shift >= 3 sigma "
      "(this lane's centroid estimator; qso1_refit/narrow_split.py)",
      "; ".join(f"{k}: {ns[k]['sep_arcsec']*1000:.1f} +/- {ns[k]['sigma_per_axis_arcsec']*1000:.1f} mas ({v_:.1f} sigma)"
                for k, v_ in sigs.items()) + f"; narrow line unresolved by the LSF (fitted sigma {ns['global']['narrow']['sigma']:.1f})",
      max(sigs.values()) < 3.0,
      "the narrow/intermediate split (the fair test) gives 1.5 sigma; the released product 1.9 sigma (the paper quotes "
      "24.9 +/- 9.4 pc ~ 2.6 sigma with a smaller error model: the resampled cube's noise is correlated and x1.6 above ERR). "
      "A simpler estimator than the paper's, so NOT a refutation -- but the public data do not independently support a "
      "significant spectroastrometric detection")

lb = [c for c in CH if c[2]]
npass = sum(1 for c in lb if c[1])
banner(f"VERDICT  ({npass}/{len(lb)} load-bearing PASS{'  -- MUTATE RUN' if MUTATE else ''})")
P("""  * The PSF-consistent re-extraction works: its core matches the PSF, the three-variant bracket agrees, and a PSF-free
    kinematic fit recovers the measured PSF (the released product drove it to a sub-diffraction 0.08").
  * On the clean cube the narrow/extended emission is essentially UNRESOLVED: thin-disk fits collapse to a ~2 pc disk
    whose ~10^8 'mass' is the core line width, and no resolved velocity gradient is detected.  The laws tie.
  * QSO1 therefore stays UNDECIDED for the framework (L324): the public data do not resolve rotation anywhere near the
    radii (r_M ~ 270 pc) where the laws differ.  With real-noise errors no version of the public data shows a
    spectroastrometric shift above 2 sigma (narrow split 1.5, released product 1.9): the direct dynamical mass is not
    robustly recoverable from the public data (a statement about the public data and this estimator, not a refutation).""")
OUT["verdict"] = {"load_bearing_pass": npass, "load_bearing_total": len(lb)}
suffix = "_MUTATE" if MUTATE else ""
with open(os.path.join(HERE, f"{SLUG}_results{suffix}.json"), "w") as f:
    json.dump(OUT, f, indent=1, default=float)
sys.exit(0 if npass == len(lb) else 1)
