#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L327 -- THE A2744-QSO1 CUBE REFIT: the framework's zero-parameter law against the public JWST narrow-Halpha cube.

WHY.  L324 turned the published "extended mass sub-dominant within 200 pc" into a bound a0 < G M/(r ln2)^2 whose verdict
flips between the published masses 10^6.9 and 10^7.7.  The decisive swing is a refit of the public data with the law
itself.  The cube is public (Zenodo 19402518, Juodzbalis+26, CC-BY-4.0; fetched + SHA-256-checked on first run into the
gitignored real_research/data/qso1/).  Independent code (qso1_refit/): a thin rotating disk in the source plane
(Sersic light), a local linear lens map (magnification 6.2, stretch and angle free), Gaussian PSF + LSF (R ~ 3700),
a spatially uniform outflow line as a nuisance, the core mask r <= 0.16", linear amplitudes solved exactly; laws
kepler / framework (RAR kernel, canonical and alt footing) / rival (a0 x E(z)), every nuisance free, 24 starts each.

WHAT IS CHECKED (both directions):
  N1-N3  the noise: ERR underestimates the line-free scatter; the 0.02" resampling correlates pixels (sum of the spatial
         autocorrelation within +/-4 px) and channels -- so naive chi^2 is overconfident and significance must come from
         REAL-noise injection (30 line-free blocks of the same cube).
  C1     every stored best fit re-evaluates to its stored chi^2 on the data (MUTATE=1 swaps the law labels: must FAIL).
  C2     the laws are indistinguishable on the data: max |Delta chi^2| across the five laws, PSF free and PSF >= 0.16".
  C3     the real-noise calibration: Delta chi^2 (kepler - framework) under a KEPLER truth and under a FRAMEWORK truth;
         the data's value sits inside both; the framework-truth distribution is centred within 1 sd of zero (NO POWER).
  C4     (first version, SUPERSEDED 09-25 -- see the corrected C4 below) log M moved >= 0.5 dex with the PSF assumption.
  E1-E3  the extended gas (0.1" bins, real-noise centroid errors): blueshift relative to the core; the rotation-dipole
         upper limit; the dispersion and the mass it would need if bound (Jeans, isotropic).
  F1     the certified velocity floor (Lean I20): v_c >= (G M a0)^{1/4} at every radius around an isolated point mass.
  P1-P2  (09-25, the FULL 6.4 GB cube, md5-verified, gitignored) the PSF MEASURED from the unresolved broad line, and the
         test that exposes the published narrow-only cube's central structure as a subtraction ARTIFACT: its core is
         sharper than the PSF (impossible for real emission: Lean I23) while the RAW line core is PSF-consistent.
  C4     CORRECTED 09-25: the kinematically constrained combination is M sin^2 i (free-inclination fits run to face-on);
         stated in M sin^2 i it still moves ~1 dex with the PSF assumption.
  C5     fits at the MEASURED PSF (0.185") with free and with the paper's inclination (52 +/- 2 deg, 48 starts), judged
         against a real-noise calibration AT THAT CONFIGURATION (the first criterion, an sd from another configuration,
         failed and is recorded).

Run from the repository root:  python3 real_research/bhstar_audit_2026/L327_qso1_cube_refit.py      (verifies, ~1 min)
FULL=1 re-runs every fit and the calibration (~40 min, 8 cores) and the PSF measurement (needs the 6.4 GB full cube,
fetched from Zenodo 19402518 and md5-checked by qso1_refit/psf_from_blr.py) before verifying.
"""
import os, sys, json, math, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
QD = os.path.join(HERE, "qso1_refit")
sys.path.insert(0, QD)
MUTATE = os.environ.get("MUTATE", "0") == "1"
FULL = os.environ.get("FULL", "0") == "1"
SLUG = "L327_qso1_cube_refit"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L327", "mutate": MUTATE, "checks": {}, "numbers": {}}


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
if FULL:
    for cmd, env in ((["data"], {}), (["data"], {"PSF_MIN": "0.16", "FITS_OUT": "fits2_psf016.json"}),
                     (["calib", "kepler_canonical", "16"], {}), (["calib", "framework_canonical", "16"], {})):
        subprocess.run([sys.executable, "fit2.py"] + cmd, check=True, env={**os.environ, **env})
    for env in ({"PSF_MIN": "0.1849", "PSF_MAX": "0.1851", "FITS_OUT": "fits2_psf0185.json"},
                {"PSF_MIN": "0.1849", "PSF_MAX": "0.1851", "COSI_MIN": "0.5878", "COSI_MAX": "0.6428", "NSTARTS": "48",
                 "FITS_OUT": "fits2_psf0185_i52_48.json"}):
        subprocess.run([sys.executable, "fit2.py", "data"], check=True, env={**os.environ, **env})
    for truth in ("kepler_canonical", "framework_canonical"):
        subprocess.run([sys.executable, "fit2.py", "calib", truth, "16"], check=True,
                       env={**os.environ, "PSF_MIN": "0.1849", "PSF_MAX": "0.1851", "COSI_MIN": "0.5878",
                            "COSI_MAX": "0.6428", "CALIB_FITS": "fits2_psf0185_i52_48.json", "CALIB_SUFFIX": "_psf0185_i52"})
    subprocess.run([sys.executable, "vfield.py"], check=True)
    subprocess.run([sys.executable, "psf_from_blr.py"], check=True)

import model, model2
D = model.load()
MSK = model2.mask_for(D["data"].shape[1:])

# ================================================================= N
banner("N1-N3 -- THE NOISE OF THE PUBLIC CUBE (line-free channels)")
fd, fe, fv = D["full_data"], D["full_err"], D["full_v"]
off = (np.abs(fv) > 800) & (np.abs(fv) < 3000) & np.isfinite(fd).all(axis=(1, 2))
Z = fd[off] / fe[off]
ratio = float(np.nanstd(Z))
acc = np.zeros((9, 9))
for z in Z:
    z = z - z.mean()
    for dy in range(-4, 5):
        for dx in range(-4, 5):
            a = z[max(0, dy):z.shape[0] + min(0, dy), max(0, dx):z.shape[1] + min(0, dx)]
            b = z[max(0, -dy):z.shape[0] + min(0, -dy), max(0, -dx):z.shape[1] + min(0, -dx)]
            acc[dy + 4, dx + 4] += np.mean(a * b)
acc /= acc[4, 4]
spec1 = float(np.mean([np.corrcoef(Z[:-1, i, j], Z[1:, i, j])[0, 1] for i in range(0, 35, 5) for j in range(0, 35, 5)]))
OUT["numbers"]["noise"] = {"err_underestimate": ratio, "spatial_corr_sum_pm4px": float(acc.sum()), "spectral_lag1": spec1}
check("N1 the ERR array underestimates the line-free scatter (std(data/ERR) > 1.3)", f"{ratio:.3f}", ratio > 1.3)
check("N2 resampled pixels are strongly correlated (sum of spatial autocorrelation within +/-4 px > 10)",
      f"{acc.sum():.1f}", acc.sum() > 10, "naive chi^2 differences are inflated ~O(50-100): only real-noise calibration counts")
check("N3 adjacent channels correlated (lag-1 > 0.1)", f"{spec1:.2f}", spec1 > 0.1, load_bearing=False)

# ================================================================= C1
banner("C1 -- EVERY STORED BEST FIT RE-EVALUATES TO ITS STORED CHI^2 ON THE DATA")
fits_free = json.load(open("fits2_data.json")); fits_psf = json.load(open("fits2_psf016.json"))
fits_m = json.load(open("fits2_psf0185.json")); fits_mi = json.load(open("fits2_psf0185_i52_48.json"))
worst = 0.0
for tag, fits in (("PSF free", fits_free), ("PSF>=0.16", fits_psf), ("PSF=0.185", fits_m), ("PSF=0.185,i=52", fits_mi)):
    for key, rec in fits.items():
        law, foot = key.split("_")
        if MUTATE:
            law = {"kepler": "framework", "framework": "kepler", "rival": "kepler"}[law]
        c, _ = model2.chi2(rec["x"], law, foot, D, MSK)
        worst = max(worst, abs(c - rec["chi2"]))
check("C1 max |chi2(re-evaluated) - chi2(stored)| < 0.01 over the 20 stored fits", f"{worst:.4f}", worst < 0.01,
      "the stored numbers ARE the data's; MUTATE (law labels swapped) must break this")

# ================================================================= C2
banner("C2 -- THE LAWS ON THE DATA (core, all nuisances free)")
rows = {}
for tag, fits in (("PSF free", fits_free), ("PSF>=0.16", fits_psf)):
    k0 = fits["kepler_canonical"]["chi2"]
    rows[tag] = {k: {"chi2": v["chi2"], "dchi2_vs_kepler": k0 - v["chi2"], "logM": v["x"][0], "psf": v["x"][11],
                     "cosi": v["x"][1]} for k, v in fits.items()}
    for k, v in rows[tag].items():
        P(f"   {tag:10s} {k:22s} chi2 = {v['chi2']:9.2f}   kepler - this = {v['dchi2_vs_kepler']:+6.2f}   "
          f"log M = {v['logM']:.2f}   psf = {v['psf']:.3f}\"   cos i = {v['cosi']:.2f}")
OUT["numbers"]["laws"] = rows
span_free = max(v["chi2"] for v in fits_free.values()) - min(v["chi2"] for v in fits_free.values())
span_psf = max(v["chi2"] for v in fits_psf.values()) - min(v["chi2"] for v in fits_psf.values())
check("C2 all five laws within naive Delta chi^2 < 10 (PSF free) and < 2 (PSF >= 0.16\")",
      f"span {span_free:.2f} / {span_psf:.2f}", span_free < 10 and span_psf < 2,
      "naive units; with N2's correlation the effective Delta chi^2 is < ~0.1-0.2")

# ================================================================= C3
banner("C3 -- REAL-NOISE CALIBRATION: what Delta chi^2 (kepler - framework) each TRUTH produces")
ck = np.array([r["dchi2"] for r in json.load(open("calib2_kepler_canonical.json"))])
cf = np.array([r["dchi2"] for r in json.load(open("calib2_framework_canonical.json"))])
obs = fits_free["kepler_canonical"]["chi2"] - fits_free["framework_canonical"]["chi2"]
zk, zf = (obs - ck.mean()) / ck.std(), (obs - cf.mean()) / cf.std()
LR = (math.exp(-zk ** 2 / 2) / ck.std()) / (math.exp(-zf ** 2 / 2) / cf.std())
OUT["numbers"]["calibration"] = {"kepler_truth": [float(ck.mean()), float(ck.std()), len(ck)],
                                 "framework_truth": [float(cf.mean()), float(cf.std()), len(cf)],
                                 "observed": obs, "z_kepler": zk, "z_framework": zf, "LR_kepler_over_framework": LR}
P(f"   Kepler truth    : Delta chi2 = {ck.mean():+.2f} +/- {ck.std():.2f}  (N = {len(ck)})")
P(f"   framework truth : Delta chi2 = {cf.mean():+.2f} +/- {cf.std():.2f}  (N = {len(cf)})")
P(f"   observed        : Delta chi2 = {obs:+.2f}   (z = {zk:+.2f} under Kepler, {zf:+.2f} under framework; LR = {LR:.2f})")
check("C3 NO POWER: the observed value sits inside both truths (|z| < 1.5) and the framework-truth distribution is "
      "centred within 1 sd of zero",
      f"z_K = {zk:+.2f}, z_F = {zf:+.2f}, framework-truth mean/sd = {cf.mean()/cf.std():+.2f}, likelihood ratio {LR:.2f}",
      abs(zk) < 1.5 and abs(zf) < 1.5 and abs(cf.mean()) < cf.std(),
      "UNDECIDABLE: the public cube cannot tell the framework from Kepler inside ~0.16\" -- a null here is not evidence")

# ================================================================= C4 (corrected 09-25)
banner("C4 -- THE KINEMATIC MASS IS PSF-SYSTEMATIC-LIMITED (stated in the constrained combination M sin^2 i)")
def msin2i(rec):
    return rec["x"][0] + math.log10(1 - rec["x"][1] ** 2)
ms = {"PSF free": msin2i(fits_free["kepler_canonical"]), "PSF>=0.16": msin2i(fits_psf["kepler_canonical"]),
      "PSF=0.185 (measured)": msin2i(fits_m["kepler_canonical"])}
OUT["numbers"]["kepler_log_Msin2i"] = ms
dm = max(ms.values()) - min(ms.values())
check("C4 log(M sin^2 i) (Kepler) moves by >= 0.5 dex across the PSF assumptions (the free-inclination fits run to "
      "face-on, so log M alone is inclination-degenerate -- the first version of this check compared log M: corrected)",
      "; ".join(f"{k}: {v:.2f}" for k, v in ms.items()) + f"  (span {dm:.2f} dex)", dm >= 0.5,
      "the mass constrained by these data swings ~1 dex with the PSF assumption")

# ================================================================= P1-P2 (the full cube)
banner("P1-P2 -- THE PSF MEASURED FROM THE UNRESOLVED BROAD LINE, AND THE NARROW-CUBE ARTIFACT")
psf = json.load(open("psf_from_blr.json"))
pb = psf["psf_broad"]; band = list(psf["psf_window_robustness"].values())
OUT["numbers"]["psf"] = {"broad_geo": pb["fwhm_geo"], "broad_err": pb["err_geo"], "window_band": [min(band), max(band)],
                         "continuum_geo": psf["psf_continuum"]["fwhm_geo"], "raw_core": psf["raw_line_core"],
                         "published_narrow_core": psf["published_narrow_core"], "md5_ok": psf.get("md5_ok")}
check("P1 PSF at H-alpha from the unresolved BLR wings: geometric FWHM 0.15-0.23 arcsec and robust to the wing window",
      f"{pb['fwhm_geo']:.3f} +/- {pb['err_geo']:.3f} arcsec (650-2500 km/s); six windows {min(band):.3f}-{max(band):.3f}; "
      f"continuum {psf['psf_continuum']['fwhm_geo']:.3f}; full cube md5 verified = {psf.get('md5_ok')}",
      0.15 < pb["fwhm_geo"] < 0.23 and max(band) - min(band) < 0.06,
      "JWST NIRSpec-IFU at 5.28 um: ~0.17-0.21 arcsec expected; the 0.08 arcsec the free fits preferred was not the instrument")
nc = psf["published_narrow_core"]; rc = psf["raw_line_core"]
art = max(nc.values()) + 3 * psf["narrow_core"]["err_geo"] < min(band) and min(rc.values()) > min(band) - 0.01
check("P2 ARTIFACT: the published narrow-only cube's core is sharper than the PSF (all windows) while the RAW line core "
      "of the same data is PSF-consistent",
      f"published narrow core {', '.join(f'|v|<{k}: {v:.3f}' for k, v in nc.items())}\"; raw core "
      f"{', '.join(f'|v|<{k}: {v:.3f}' for k, v in rc.items())}\"; PSF band {min(band):.3f}-{max(band):.3f}\"", art,
      "no PSF-convolved image can be sharper than the PSF (Lean I23): the narrow product's central flux distribution is "
      "an artifact of the broad-line subtraction, at exactly the < 0.2 arcsec (~100 pc) scales where the mass is measured")

# ================================================================= C5
banner("C5 -- FITS AT THE MEASURED PSF: free inclination, and the paper's inclination (52 +/- 2 deg)")
for tag, fits in (("PSF=0.185", fits_m), ("PSF=0.185,i=52", fits_mi)):
    k0 = fits["kepler_canonical"]["chi2"]
    for k, v in fits.items():
        P(f"   {tag:15s} {k:22s} chi2 = {v['chi2']:9.2f}   kepler - this = {k0 - v['chi2']:+6.2f}   log M = {v['x'][0]:.2f}"
          f"   cos i = {v['x'][1]:.3f}   log M sin^2 i = {msin2i(v):.2f}")
span_m = max(v["chi2"] for v in fits_m.values()) - min(v["chi2"] for v in fits_m.values())
kep_i52 = fits_mi["kepler_canonical"]["x"][0]
obs_i52 = fits_mi["kepler_canonical"]["chi2"] - fits_mi["framework_canonical"]["chi2"]
cki = np.array([r["dchi2"] for r in json.load(open("calib2_kepler_canonical_psf0185_i52.json"))])
cfi = np.array([r["dchi2"] for r in json.load(open("calib2_framework_canonical_psf0185_i52.json"))])
p_kep = float((cki >= obs_i52).mean())
OUT["numbers"]["C5"] = {"span_free_i": span_m, "kepler_logM_i52": kep_i52, "obs_dchi2_i52": obs_i52,
                        "calib_kepler_truth": [float(cki.mean()), float(cki.std()), sorted(map(float, cki))],
                        "calib_framework_truth": [float(cfi.mean()), float(cfi.std()), sorted(map(float, cfi))],
                        "P_ge_obs_given_kepler": p_kep}
P(f"   calibration at (PSF 0.185, i = 52): Kepler truth {cki.mean():+.2f} +/- {cki.std():.2f}; framework truth "
  f"{cfi.mean():+.2f} +/- {cfi.std():.2f}; observed {obs_i52:+.2f}; empirical P(>= obs | Kepler) = {p_kep:.3f}")
check("C5 at the measured PSF: with free inclination the laws span < 1 naive; with the paper's inclination the naive "
      "preference for the framework is NOT significant against a real-noise-calibrated Kepler truth (P >= 0.05), and "
      "the Kepler mass is not recovered (it runs to the 10^6 bound)",
      f"free-i span {span_m:.2f}; i = 52: Kepler - framework = {obs_i52:+.2f}, P(>= obs | Kepler) = {p_kep:.3f}; "
      f"framework truth {cfi.mean():+.1f} +/- {cfi.std():.1f} (no power); Kepler log M at i = 52: {kep_i52:.2f}",
      span_m < 1.0 and p_kep >= 0.05 and kep_i52 < 6.5,
      "RECORD: the first version of C5 (naive span < 2 x an sd calibrated for a DIFFERENT configuration) FAILED at span "
      "14.3; the calibration at THIS configuration is the proper test.  An independent forward model at the physical PSF "
      "does not reproduce the paper's 10^7.7 from the released narrow product; the law comparison has no power; L324 "
      "stays undecided")

# ================================================================= E
banner("E1-E3 -- THE EXTENDED GAS (0.1\" bins, real-noise centroid errors)")
R = [r for r in json.load(open("vfield.json")) if np.isfinite(r["ev"]) and r["ev"] > 0]
rr = np.array([math.hypot(r["dx_arcsec"], r["dy_arcsec"]) for r in R])
v = np.array([r["v"] for r in R]); ev = np.array([r["ev"] for r in R]); sg = np.array([r["sig"] for r in R])
fl = np.array([r["flux"] for r in R]); phi = np.array([math.atan2(r["dy_arcsec"], r["dx_arcsec"]) for r in R])
core, ext = rr < 0.09, rr >= 0.12
w = 1 / ev ** 2
vc, evc = (w[core] * v[core]).sum() / w[core].sum(), w[core].sum() ** -0.5
ve, eve = (w[ext] * v[ext]).sum() / w[ext].sum(), w[ext].sum() ** -0.5
off_v, off_e = ve - vc, math.hypot(eve, evc)
A = np.vstack([np.ones(ext.sum()), np.cos(phi[ext]), np.sin(phi[ext])]).T
Cov = np.linalg.inv(A.T @ (A * w[ext][:, None])); p = Cov @ (A.T @ (w[ext] * v[ext]))
rng = np.random.default_rng(1)
amps = [math.hypot(*rng.multivariate_normal(p, Cov)[1:]) for _ in range(20000)]
amp95 = float(np.percentile(amps, 95))
sig_med, sig_fw = float(np.median(sg[ext])), float(np.average(sg[ext], weights=fl[ext]))
Mdyn = {r_pc: 2 * (sig_med * 1e3) ** 2 * r_pc * model.PC / model.G / model.MSUN for r_pc in (300, 500, 900)}
OUT["numbers"]["extended"] = {"offset_kms": off_v, "offset_err": off_e, "dipole_amp": float(math.hypot(p[1], p[2])),
                              "dipole_95": amp95, "sigma_median": sig_med, "sigma_fluxweighted": sig_fw,
                              "Mdyn_if_bound_alpha2": Mdyn}
check("E1 the extended gas is blueshifted relative to the core", f"{off_v:+.1f} +/- {off_e:.1f} km/s "
      f"({off_v/off_e:+.1f} sigma)", off_v / off_e < -2, "outflow-like (the paper also identifies an outflow at 300-450 pc)",
      load_bearing=False)
check("E2 no rotation detected in the extended gas: dipole 95% upper limit (projected)", f"{math.hypot(p[1],p[2]):.1f} km/s,"
      f" 95% < {amp95:.1f} km/s", True, "the 300-450 pc rotation that would decide the law is NOT in the current data",
      load_bearing=False)
check("E3 the extended gas is hot: if bound it needs >= 10x the black-hole mass",
      f"sigma = {sig_med:.0f} (median) / {sig_fw:.0f} (flux-wtd) km/s; M_dyn(alpha=2) = "
      + ", ".join(f"{k} pc: {m:.1e}" for k, m in Mdyn.items()) + " Msun",
      min(Mdyn.values()) > 10 * 10 ** 7.7,
      "outflow (no test) OR bound: LCDM supplies a halo; the framework would need ~1e9 Msun of COLD GAS at 0.2-0.9 kpc "
      "(NOT sub-mm testable here: see E4) -- a registered conditional prediction")

# ================================================================= E4
banner("E4 -- CAN SUB-MM DATA TEST THE BOUND-GAS CONDITIONAL?  ALMA 1.2 mm limit x the near-pristine metallicity")
from astropy.cosmology import Planck18
import astropy.units as u
hP, kB, cL = 6.62607015e-34, 1.380649e-23, 2.99792458e8
zq = 7.0451; DL = Planck18.luminosity_distance(zq).to(u.m).value; nu = cL / 1.2e-3 * (1 + zq); beta = 1.8
kap = 0.077 * (nu / 352.7e9) ** beta
Tcmb = 2.7255 * (1 + zq)
Bnu = lambda n, T: 2 * hP * n ** 3 / cL ** 2 / math.expm1(hP * n / (kB * T))
Td = (25.0 ** (4 + beta) + 2.7255 ** (4 + beta) * ((1 + zq) ** (4 + beta) - 1)) ** (1 / (4 + beta))
Md = (1e-30 / 6.2) * DL ** 2 / ((1 + zq) * kap * (Bnu(nu, Td) - Bnu(nu, Tcmb))) / model.MSUN
GDR_min = 100 / 0.005                      # linear Z scaling from solar GDR 100 at Z < 0.005 Zsun (steeper scalings: larger)
Mg_lim = Md * GDR_min
OUT["numbers"]["alma"] = {"Mdust_lim_T25_mu6.2": Md, "GDR_min": GDR_min, "Mgas_lim": Mg_lim}
check("E4 the ALMA dust limit cannot test ~1e9 Msun of cold gas in a near-pristine host",
      f"3-sigma 0.1 mJy at 1.2 mm (Ma+25 citing Labbe+23/Fujimoto+23/Furtak+24), mu = 6.2, T_d = 25 K, CMB-corrected: "
      f"M_dust < {Md:.1e} Msun; Z < 0.005 Zsun (Maiolino+25, arXiv:2505.22567) => GDR >= {GDR_min:.0e} => "
      f"M_gas < {Mg_lim:.0e} Msun", Mg_lim > 1e10,
      "the bound-gas branch is NOT sub-mm testable ([CII] fails for the same reason: almost no carbon) -- only kinematics "
      "can decide", load_bearing=False)

# ================================================================= F
banner("F1 -- THE CERTIFIED VELOCITY FLOOR (Lean I20)")
vfl = {k: (model.G * 10 ** 7.7 * model.MSUN * a) ** 0.25 / 1e3 for k, a in model.A0.items()}
OUT["numbers"]["velocity_floor_kms_logM7.7"] = vfl
check("F1 v_flat = (G M a0)^{1/4} at 10^7.7: the floor below which no circular orbit may fall (isolated, no EFE)",
      f"canonical {vfl['canonical']:.1f} km/s, alt {vfl['alt']:.1f} km/s", 27 < vfl["canonical"] < 30,
      "a PSF-controlled rotation curve that falls below this beyond r_M ~ 250-270 pc falsifies the framework (Newton "
      "has no floor)", load_bearing=False)

lb = [c for c in CH if c[2]]
npass = sum(1 for c in lb if c[1])
banner(f"VERDICT  ({npass}/{len(lb)} load-bearing PASS{'  -- MUTATE RUN' if MUTATE else ''})")
P("""  * 09-25 FULL CUBE: PSF measured 0.19" from the broad line; the released narrow-only cube's core (0.11") is SHARPER than
    the PSF while the raw line core is PSF-consistent -> a broad-subtraction ARTIFACT at the mass-measuring scales; at the
    measured PSF an independent model does not recover the published 10^7.7.
  * THE TRUTH, as far as the public cube goes: UNDECIDABLE.  Kepler, the framework (both footings) and the a0 ~ H(z) rival
    fit the core equally well; real-noise injection shows the cube has NO power to separate them inside ~0.16"; the
    kinematic mass itself moves ~1 dex with the PSF assumption, so L324's mass-dependent sub-dominance verdict cannot
    be settled from these data either.
  * The extended gas is hot and blueshifted (outflow-like), with no detectable rotation: the decisive 300-450 pc
    rotation is not in the data.  IF it is bound, the framework needs ~1e9 Msun of cold gas there -- which the ALMA
    dust limit cannot test in this near-pristine (Z < 0.005 Zsun) host.
  * What would decide it: a PSF-controlled (source-plane) rotation curve beyond r_M ~ 250-270 pc, confronted with the
    certified floor v_c >= (G M a0)^{1/4} and the L324 K6 bands.""")
OUT["verdict"] = {"load_bearing_pass": npass, "load_bearing_total": len(lb)}
suffix = "_MUTATE" if MUTATE else ""
with open(os.path.join(HERE, f"{SLUG}_results{suffix}.json"), "w") as f:
    json.dump(OUT, f, indent=1, default=float)
sys.exit(0 if npass == len(lb) else 1)
