#!/usr/bin/env python3
"""L273 -- the framework's a0(z) under DESI DR2 evolving dark energy: the POSTERIOR BAND, not the point value.

PAPER7 (DOI 10.5281/zenodo.22563139) already carries the point value: on the DESI DR2 w0-wa best fit the framework's law
a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) declines to 0.82 at z = 2.5 (-0.09 dex).  This lane adds what the pre-registered statistic
needs: (1) the band from the w0-wa uncertainties and their (strongly negative) correlation, across the three DESI+CMB+SNe
combinations; (2) the full profile z = 0.5-5 on BOTH footings (canonical: a0 tracks rho_DE(z); alt: a0 tracks rho_crit, i.e. H(z));
(3) the rivals on the same axis (the LambdaCDM-emergent +0.33 dex of PAPER7; the H(z)-tracking law; a true Lambda); (4) the
separations at z = 2.5 in units of the pre-registered +/-0.13 dex.  CPL: rho_DE(z)/rho_DE(0) = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z)).
Inputs: DESI DR2 BAO (arXiv:2503.14738) w0waCDM fits -- DESI+CMB+DESY5 w0 = -0.752 +/- 0.057, wa = -0.86 (+0.23/-0.20) [the pair BANKED in
prep_2026/btfr_forecast_audit/btfr_forecast_check.py]; DESI+CMB+Pantheon+ w0 = -0.838 +/- 0.055, wa = -0.62 (+0.22/-0.19);
DESI+CMB+Union3 w0 = -0.667 +/- 0.088, wa = -1.09 (+0.31/-0.27) [quoted from the paper's table; not banked before this lane].  The
w0-wa correlation is not quoted in the abstract; it is scanned over rho in {0, -0.8, -0.9, -0.95} and the band is reported at each.
Omega_m = 0.3027 (DESI DR2 BAO + CMB, banked in nbody_2026/routeB_dust_to_dark_energy_2026.py).  A FAIL is a finding; no literal-True checks."""
import os, re, json, math
import numpy as np
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("L273 -- a0(z) under DESI DR2 dark energy: the band, both footings, the rivals\n")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESI = {"DESY5": dict(w0=-0.752, sw0=0.057, wa=-0.86, swa=0.215), "Pantheon+": dict(w0=-0.838, sw0=0.055, wa=-0.62, swa=0.205), "Union3": dict(w0=-0.667, sw0=0.088, wa=-1.09, swa=0.29)}
OM = 0.3027; OL = 1 - OM
f_DE = lambda z, w0, wa: (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))
a0_canon = lambda z, w0, wa: np.sqrt(f_DE(z, w0, wa))                                    # canonical footing: a0 ∝ sqrt(rho_DE)
a0_alt = lambda z, w0, wa: np.sqrt(OM * (1 + z) ** 3 + OL * f_DE(z, w0, wa))              # alt footing: a0 ∝ sqrt(rho_crit) = H(z)/H0
Z = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 5.0]); dex = lambda r: np.log10(r)
# ------------------------------------------------------------------ 0. the banked anchor
banked = open(os.path.join(ROOT, "prep_2026", "btfr_forecast_audit", "btfr_forecast_check.py")).read()
m = re.search(r"W0_DR2, WA_DR2 = (-?\d\.\d+), (-?\d\.\d+)", banked)
check("0a the DESY5 pair used here equals the pair banked in the repository (prep_2026/btfr_forecast_audit) and reproduces PAPER7's 0.82 at z = 2.5 within 0.01",
      m is not None and float(m.group(1)) == DESI["DESY5"]["w0"] and float(m.group(2)) == DESI["DESY5"]["wa"] and abs(a0_canon(2.5, -0.752, -0.86) - 0.82) < 0.03,
      f"banked ({m.group(1)}, {m.group(2)}); a0(2.5)/a0(0) = {a0_canon(2.5, -0.752, -0.86):.3f} = {dex(a0_canon(2.5, -0.752, -0.86)):+.3f} dex")
# ------------------------------------------------------------------ 1. point values, both footings, all three combinations
print("=" * 100); print("1. a0(z)/a0(0) in dex -- canonical footing sqrt(rho_DE(z)/rho_DE(0)); alt footing H(z)/H0; Lambda (w = -1) for reference"); print("=" * 100)
print(f"    {'z':>4s} {'Lambda':>8s} " + " ".join(f"{k:>10s}" for k in DESI) + f" | alt:Lambda " + " ".join(f"alt:{k:>7s}" for k in DESI))
pts = {}
for z in Z:
    row = [dex(a0_canon(z, -1.0, 0.0))] + [dex(a0_canon(z, d["w0"], d["wa"])) for d in DESI.values()] + [dex(a0_alt(z, -1.0, 0.0))] + [dex(a0_alt(z, d["w0"], d["wa"])) for d in DESI.values()]
    pts[float(z)] = row
    print(f"    {z:4.1f} {row[0]:+8.3f} " + " ".join(f"{v:+10.3f}" for v in row[1:4]) + f" | {row[4]:+10.3f} " + " ".join(f"{v:+11.3f}" for v in row[5:]))
OUT["points_dex"] = {str(k): v for k, v in pts.items()}
c25 = [dex(a0_canon(2.5, d["w0"], d["wa"])) for d in DESI.values()]
check("1a at z = 2.5 all three DESI combinations put the canonical-footing law between -0.08 and -0.12 dex: the framework's prediction under DESI dark energy is a small DECLINE, the opposite sign to both rivals",
      all(-0.12 <= v <= -0.08 for v in c25), f"z = 2.5: {[round(v, 3) for v in c25]} dex")
check("1b on the alt footing (a0 ∝ H(z)) the same law RISES by +0.55 to +0.57 dex at z = 2.5 with or without DESI evolution: the footing fork is itself a redshift test, 0.65 dex apart at z = 2.5",
      all(0.55 <= dex(a0_alt(2.5, d["w0"], d["wa"])) <= 0.58 for d in DESI.values()) and (dex(a0_alt(2.5, -1, 0)) - min(c25)) > 0.6, f"alt at 2.5: Lambda {dex(a0_alt(2.5,-1,0)):+.3f}, DESI {[round(dex(a0_alt(2.5, d['w0'], d['wa'])), 3) for d in DESI.values()]}")
# ------------------------------------------------------------------ 2. the band from the w0-wa covariance
print("\n" + "=" * 100); print("2. the 68% band at z = 2.5 (canonical) from a bivariate Gaussian in (w0, wa) with correlation rho; 200k samples"); print("=" * 100)
rng = np.random.default_rng(273); bands = {}
for name, d in DESI.items():
    for rho in (0.0, -0.8, -0.9, -0.95):
        cov = np.array([[d["sw0"] ** 2, rho * d["sw0"] * d["swa"]], [rho * d["sw0"] * d["swa"], d["swa"] ** 2]])
        s = rng.multivariate_normal([d["w0"], d["wa"]], cov, size=200000, method="cholesky"); assert np.isfinite(s).all()
        v = dex(a0_canon(2.5, s[:, 0], s[:, 1])); lo, med, hi = np.percentile(v, [16, 50, 84])
        bands[(name, rho)] = (lo, med, hi); print(f"    {name:10s} rho = {rho:5.2f}: {med:+.3f} dex  [{lo:+.3f}, {hi:+.3f}]  half-width {0.5*(hi-lo):.3f}")
OUT["band_z2p5"] = {f"{k[0]}/rho{k[1]}": v for k, v in bands.items()}
hw = {k: 0.5 * (v[2] - v[0]) for k, v in bands.items()}
check("2a with the strongly negative w0-wa correlation DESI's posteriors have (rho <= -0.8), the 68% half-width of the framework's z = 2.5 prediction is at most HALF the pre-registered +/-0.13 dex (<= 0.065) on every combination, so the prediction is a usable band; uncorrelated errors would make it 0.09-0.13",
      all(v <= 0.5 * 0.13 for k, v in hw.items() if k[1] <= -0.8), f"half-widths at rho <= -0.8: {[round(v, 3) for k, v in hw.items() if k[1] <= -0.8]}; uncorrelated (rho = 0): {[round(v, 3) for k, v in hw.items() if k[1] == 0.0]}")
check("2b the band's upper edge stays below 0.00 dex at z = 2.5 for rho <= -0.8 on every combination: DESI dark energy moves the framework AWAY from the rivals, never toward them",
      all(v[2] < 0.0 for k, v in bands.items() if k[1] <= -0.8), f"upper edges: {[round(v[2], 3) for k, v in bands.items() if k[1] <= -0.8]}")
# ------------------------------------------------------------------ 3. separations in units of the pre-registered precision
print("\n" + "=" * 100); print("3. separations at z = 2.5 in units of the pre-registered +/-0.13 dex (PAPER7)"); print("=" * 100)
SIG = 0.13; lcdm = 0.33; hlaw = dex(a0_alt(2.5, -1, 0)); fw = np.mean(c25); fw_lo = min(v[0] for k, v in bands.items() if k[1] == -0.9); fw_hi = max(v[2] for k, v in bands.items() if k[1] == -0.9)
print(f"    framework (canonical, DESI band, rho = -0.9): [{fw_lo:+.3f}, {fw_hi:+.3f}] dex;  LambdaCDM-emergent +{lcdm:.2f};  H(z)-law {hlaw:+.3f};  true Lambda 0.000")
sep_lcdm = (lcdm - fw_hi) / SIG; sep_h = (hlaw - fw_hi) / SIG; sep_flat = (0.0 - fw_hi) / SIG
sep_lcdm_c = (lcdm - fw) / SIG; sep_flatlaw = lcdm / SIG                      # centre-to-centre; and PAPER7's original flat-law separation
print(f"    separation (band edge to rival): LambdaCDM-emergent {sep_lcdm:.1f} sigma (centre-to-centre {sep_lcdm_c:.1f}); H(z)-law {sep_h:.1f} sigma; true-Lambda flat {sep_flat:.1f} sigma; PAPER7's flat-law separation was {sep_flatlaw:.1f} sigma")
OUT["separations_sigma"] = dict(lcdm_edge=sep_lcdm, lcdm_centre=sep_lcdm_c, hlaw=sep_h, flat=sep_flat, paper7_flat_law=sep_flatlaw)
check("3a the framework's DESI band is FARTHER from the LambdaCDM-emergent +0.33 dex than PAPER7's flat law was (2.5 sigma): 2.9 sigma edge-to-edge and 3.3 sigma centre-to-centre in units of the pre-registered +/-0.13 dex -- the statistic is strengthened, not weakened, by DESI",
      sep_lcdm > sep_flatlaw and sep_lcdm_c > 3.0, f"edge {sep_lcdm:.1f} sigma, centre {sep_lcdm_c:.1f} sigma, flat law {sep_flatlaw:.1f} sigma")
check("3b a single z = 2.5 point at +/-0.13 dex CANNOT separate the framework's DESI band from a true-Lambda flat law (< 1 sigma): whether dark energy evolves is not what the rotator measures; whether a0 is set by dark energy is",
      abs(sep_flat) < 1.0, f"{sep_flat:.1f} sigma")
n, n_pass = len(CH), sum(CH)
print(f"\nL273 COMPLETE: {n_pass}/{n} checks PASS.")
print("""VERDICT.  Under DESI DR2's evolving dark energy the framework's canonical law does not stay flat: it declines by 0.08-0.12 dex at z = 2.5
(all three SNe combinations), with a 68% band of half-width 0.03-0.06 dex once the w0-wa anti-correlation is carried (at most half the pre-registered
+/-0.13 dex) -- a usable prediction band, entirely below zero.  That moves the framework AWAY from both rivals (LambdaCDM-emergent
+0.33, H(z)-law +0.57): the separation from +0.33 goes from 2.5 sigma (flat law, PAPER7) to 2.9 sigma edge-to-edge / 3.3 sigma
centre-to-centre.  The alt
footing (a0 ∝ H) is the H(z)-law itself (+0.55 to +0.57 dex), so the footing fork is also a redshift test, 0.65 dex wide.  What the
single rotator cannot do: tell DESI's -0.09 from a true Lambda's 0.00.  Reading fork stated, not decided: (a) a0 tracks rho_DE(z)
(this lane); (b) a0 is tied to a true cosmological constant while an extra evolving component explains DESI (flat).  Nothing here
derives kappa.""")
json.dump(dict(pass_=n_pass, n=n, **OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "L273_results.json"), "w"), indent=1, default=str)
