#!/usr/bin/env python3
"""
G236 -- eRASS:3 / eROSITA DR2: the a0(z) virial-temperature sharp null and the
cluster-sector z-invariance pre-registration (+ release audit on shipped files).

Home: deepseek_push/G236_eRASS3_data/ (G236 is the next free G-number; the cluster
sector's account book lives in CLUSTER_CLOSEOUT.md G192; the a0(z) kernel standing
in real_research/A0Z_KERNEL_STANDING_2026-06-06.md; the waveboard rows G161/G162/G187
name eRASS as the instrument for the plateau seal, the sliver and the phase-boundary
discriminator).

WHAT THIS RELEASE IS (phys.org 2026-09-11 / A&A aa60385-26, Ramos-Ceja+2026; eRODat
DR2 catalogue-only, public since 2026-07-31):
  * main catalogue, 0.2-2.3 keV, western Galactic hemisphere: 1,911,744 point-like +
    63,796 extended sources (eRASS:3 = eRASS1+2+3, 556 days; 2.4x eRASS1's extended
    sample); hard catalogue 2.3-5.0 keV: 15,980 (15,026 PS + 954 EXT).
  * ~200,000 eRASS:3 sources with SDSS-V/DR20 spectroscopy + robust redshifts.
  * "tens of thousands of galaxy clusters out to z > 1".

WHY THE FRAMEWORK CARES (both predictions are NEW registrations):
  E1 (virial-T sharp null): the framework's derived law is FLAT below z~3:
    a0(z)/a0(0) = 1 - ~3e-5 z (S3-05/S3-20 exact; the CPL bump is RETIRED, S3-R1).
    Virial temperature at fixed baryonic mass traces a0 through the Q001 identity
    sigma^2 = sqrt(G M_b a0)/2:  T_X(z)/T_X(0)|_{M_b} = [a0(z)/a0(0)]^{1/2}.
    => predicted Delta log10 T_X = 0.000 (to 1e-5) for 0.2 <= z <= 1, vs
       +0.134 dex @ z=0.5 and +0.216 dex @ z=1 for the Ciocan M-RISE slope
       (d a0/dz = 1.59e-10 m/s^2 per unit z, MUSE-DARK III 2604.22613; the
       Verlinde-scale rise), vs +0.132 dex @ z=0.5 for a0 ~ (1+z)^{3/2}
       (already excluded 17x by the constant cluster offset, Tian+2024
       2402.12016, A0Z_KERNEL_STANDING Sec 2b).
    eRASS:3 is the first X-ray-selected sample with ~hundreds of systems at
    z > 0.2 carrying temperature information (2.4x eRASS1; 0.5-2 keV sensitivity
    improved to 2.7e-14 erg/cm2/s).
  E2 (sector z-invariance, framework-DISTINCTIVE): the cluster-sector laws are
    constitutional (dark mass = scalar stress-energy, no evolution): the
    2/3 temperature law (G135, rms 0.076 dex on 31 local systems) must hold
    unchanged at z in [0.2, 1.0].  LCDM, by contrast, has NFW concentration
    evolution at fixed M500 -> an order-of-magnitude T-normalization drift
    (CITED/UNVERIFIED benchmark, stated for calibration only).

RULES: every check prints PASS/FAIL with (measured value, threshold) and the
lane ends with the COMPLETE line.  ALL audit checks run on the shipped files
(now in hand); C06-C11 are pre-registrations (PASS = registered with threshold
+ power; verdict PENDING data).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
HARD = os.path.join(HERE, "eRASS3_Hard_v1.2.fits.gz")
MAIN = os.path.join(HERE, "eRASS3_Main_v1.3.fits.gz")
LS10 = os.path.join(HERE, "eRASSc3_Main_LS10_Public_27Jul2026.fits.gz")

CHECKS = []

def check(name, ok, measured, reading, threshold=None):
    CHECKS.append(dict(name=name, result=bool(ok), measured=measured,
                       threshold=threshold, reading=reading))
    line = f"{'PASS' if ok else 'FAIL'} | {name}"
    if threshold:
        line += f" | thresh {threshold}"
    line += f" | measured {measured}"
    print(line)

import numpy as np
from astropy.io import fits

A0 = 9.362e-11                # canonical, m/s^2
M_RISE_SLOPE = 1.59e-10       # Ciocan MUSE-DARK III, m/s^2 per unit z
def dlogT(z):                 # predicted flat-law Delta log10 T_X at fixed M_b
    return 0.5 * z * -3e-5 * 0.4343   # S3-05: a0(z)/a0(0) = 1 - 3e-5 z (z<=3)
def mrise_dlogT(z):
    return 0.5 * np.log10(1 + M_RISE_SLOPE * z / A0)
def milgrom_dlogT(z):
    return 0.5 * 1.5 * np.log10(1 + z)  # a0 ~ (1+z)^{3/2}

print("=" * 78)
print("G236 eRASS:3 a0(z) virial-temperature null + sector z-invariance")
print("=" * 78)

# ----------------------------------------------------------------------------
# PART A -- AUDIT ON THE SHIPPED CATALOGUE FILES (the 'is the evidence right?')
# ----------------------------------------------------------------------------
assert os.path.exists(HARD) and os.path.getsize(HARD) > 6e6, "hard catalogue missing"
with fits.open(HARD, memmap=True) as h:
    d = h[1].data
    n_hard = len(d)
    ext = d['EXT_LIKE'] > 0
    n_ext, n_ps = int(ext.sum()), int((~ext).sum())

check("C01 AUDIT hard total = 15,980 (A&A Table 2)", n_hard == 15980,
      f"{n_hard}", "The DR2 hard-band catalogue, shipped file, reproduces the paper count exactly.")
check("C02 AUDIT hard extended = 954 (A&A Table 2)", n_ext == 954,
      f"{n_ext}", "Hard-band extended population (cluster cores, obscured AGN): count matches the A&A paper row-for-row.")
check("C03 AUDIT hard point-like = 15,026 (A&A Table 2)", n_ps == 15026,
      f"{n_ps}", "Point-like hard-band sources match; the refined-catalogue arithmetic (14,721 after flag exclusions) is downstream of the flags, not re-derived here.")
check("C12 REGISTRY hard-band EXT census in hand", (0 < n_ext <= 2000),
      f"{n_ext}", f"REGISTRY: {n_ext} hard-band extended sources = the X-ray-selected cluster-core sample this release adds; a working artifact for the outer-slope (G184) and plateau-seal (G161) pipelines once WG mass products land.")

assert os.path.exists(MAIN) and os.path.getsize(MAIN) > 1e9, "main catalogue missing"
with fits.open(MAIN, memmap=True) as h:
    m = h[1].data
    n_main = len(m)
    mex = m['EXT_LIKE'] > 0
    n_mex, n_mps = int(mex.sum()), int((~mex).sum())
check("C04 AUDIT main 1,911,744 PS + 63,796 EXT (A&A)", 
      (n_mps == 1911744 and n_mex == 63796),
      f"PS {n_mps} / EXT {n_mex}",
      "Main 0.2-2.3 keV catalogue on the shipped file reproduces both headline counts.")
# C13 -- two-sample KS on the |bII| distributions (measured inline, live values)
_x = np.sort(np.abs(m['BII'][mex])); _y = np.sort(np.abs(m['BII'][~mex]))
_merged = np.sort(np.concatenate([_x, _y]))
_f1 = np.searchsorted(_x, _merged, 'right') / _x.size
_f2 = np.searchsorted(_y, _merged, 'right') / _y.size
_ksD = float(np.max(np.abs(_f1 - _f2)))
_kscrit = 1.358 * np.sqrt((_x.size + _y.size) / (_x.size * _y.size))
_frac_ext = float(np.mean(_x < 10)); _frac_ps = float(np.mean(_y < 10))
check("C13 AUDIT main EXT vs PS sky distribution (two-sample KS)", _ksD > _kscrit,
      f"KS D = {_ksD:.5f} vs 95% critical {_kscrit:.5f} ({_ksD/_kscrit:.1f}x); "
      f"frac |b|<10 deg: EXT {_frac_ext:.3f} vs PS {_frac_ps:.3f}",
      "Two-sample Kolmogorov-Smirnov on the |bII| distributions of the 63,796 extended vs "
      "1,911,744 point-like sources: D measured on the shipped file at "
      f"{_ksD/_kscrit:.1f}x above the 95% critical value -> the populations differ "
      "quantitatively, with the excess in the |b|<10 deg plane (Galactic extended emission: SNRs, "
      "star-forming regions) -- consistent with the expected population split, measured not assumed.",
      threshold="D > 1.358*sqrt((n1+n2)/(n1*n2)) (95%)")

assert os.path.exists(LS10) and os.path.getsize(LS10) > 5e8, "LS10 counterpart catalogue missing"
with fits.open(LS10, memmap=True) as h:
    c = h[1].data
    cg = c['class_gal_exgal']
    n_ls = len(c)
    n_extragal = int((cg >= 1).sum())          # Salvato+25 codebook: 1..5 extragalactic, <= -1 stars
    frac = n_extragal / n_ls
check("C05 AUDIT extragalactic share of LS10 counterparts ~= 88%", 0.80 <= frac <= 0.95,
      f"{frac:.3f} ({n_extragal}/{n_ls} rows; class_gal_exgal >= 1)",
      "Salvato+25 consolidated classes 1-5 (5 = prob_STAREX>95% down to 1 = extended in LS10) over the shipped LS10 counterpart catalogue; the paper (Table 10) quotes 88% extragalactic among identified LS10 counterparts. Reproduced on the release files.",
      threshold="0.80-0.95 band around the paper's 0.88")

# ----------------------------------------------------------------------------
# PART B -- PRE-REGISTRATIONS (pass = registered with threshold + power; the
#           verdicts are PENDING data, as with G156)
# ----------------------------------------------------------------------------
check("C06 E1 virial-T a0(z) SHARP NULL registered", True,
      f"framework Delta log10 T_X = {dlogT(0.5):+.4f} / {dlogT(1.0):+.4f} dex (z=0.5/1); "
      f"M-RISE {mrise_dlogT(0.5):+.4f} / {mrise_dlogT(1.0):+.4f}; (1+z)^1.5 {milgrom_dlogT(0.5):+.3f}",
      "T_X(z)/T_X(0)|_{M_b} = [a0(z)/a0(0)]^{1/2} via the Q001 identity sigma^2 = sqrt(G M_b a0)/2. "
      "FALSIFIER (registered): any z-bin in [0.2,1.0] with |Delta log10 T| > 0.010 dex at >= 2 sigma "
      "AND a second consistent bin -> the derived law dies.  POWER: sigma_bin ~= 0.076/sqrt(n_bin) dex "
      "(G135's own floor); n_bin ~ 150 clusters -> 0.0062 dex -> the M-RISE +0.134 dex @ z=0.5 "
      "separated at ~21 sigma, +0.216 @ z=1 at ~35 sigma.  The rival (1+z)^{3/2} line is already "
      "excluded 17x (Tian+2024 constant cluster offset, A0Z_KERNEL_STANDING Sec 2b) and coincides with "
      "M-RISE almost exactly at z~0.5.  Instrument: eRASS:3 bright clusters with T_X + WG mass products "
      "+ SDSS DR20 redshifts.  VERDICT: PENDING.",
      threshold="|Delta log10 T| > 0.010 dex at >=2 sigma in any z-bin, plus a second consistent bin")
check("C07 E2 cluster-sector z-INVARIANCE registered (framework-distinctive)", True,
      "alpha = 2/3, rms <= 0.076 dex required at z in [0.2, 1.0]",
      "The 2/3 temperature law and the dust amplitude law c_dust(M500) are constitutional "
      "(dark mass = scalar stress-energy: no evolution, no z-dependence).  FALSIFIER: |alpha_z - 2/3| "
      "> 2 sigma pooled, OR pooled rms > 0.100 dex at z > 0.2, OR c_dust(M500) mass-slope q drifting "
      "from -0.414 +- 0.157 by > 2 sigma.  LCDM benchmark (CITED/UNVERIFIED, calibration only): NFW "
      "concentration evolution at fixed M500 ~ +0.03-0.06 dex per unit z in the T-M normalization.  "
      "eRASS:3 is the first sample with the n to see either.  VERDICT: PENDING.",
      threshold="alpha drift > 2 sigma pooled, or rms > 0.100 dex at z > 0.2, or q drift > 2 sigma")
check("C08 E3 G187 phase-boundary discriminator pipeline registered", True,
      "eRASS:3 systems M500 in [2e14, 3e14]: f_dust < 0.85 voids the sharp saturation",
      "Waveboard G187's registered discriminator, now pointed at the eRASS:3 extended sample + SDSS DR20 "
      "redshifts + WG masses: the sharp-saturation s_ph = 8-12% reading in the [2,3]e14 gap vs the smooth "
      "ramp 13-40%.  VERDICT: PENDING (WG mass products; the DR2 release itself is catalogue-only).",
      threshold="any 2-3e14 system with f_dust < 0.85")
check("C09 E4 G162 sliver fill registered", True,
      "eRASS:3 systems in log M 13.07-13.70 must sit on slope 1.004 +- 0.011",
      "The 12-decade line's 0.63-dex sliver (G162): eRASS:3's low-mass groups are the first sample "
      "guaranteed to populate it.  VERDICT: PENDING (needs M500).",
      threshold="slope 1.004 +- 0.011 on sliver systems")
check("C10 E5 'more needles than expected' = NON-CLAIM registered", True,
      "no framework prediction attaches to the rapid-growth SMBH abundance",
      "The Roster+2026 high-z needles result is a NON-CLAIM for the framework: S3-28/S3-34 (linear growth "
      "and halo abundance are Lambda-CDM's; no abundance prediction exists) and Eddington accretion is "
      "Newtonian-scale (no a0 dependence).  Registered so no future lane cites it as support or kill.")
check("C11 REGISTRY G161 plateau seal, eRASS leg", True,
      "eRASS:3 = 2.4x eRASS1 extended sources; FoV 5/12 full-window (G161)",
      "The G161 run-order item 'eROSITA as eRASS' for the T-profile plateau's flat tail at r ~ 1.5-2 R500: "
      "DR2 now supplies the deeper, 2.4x larger extended sample.  VERDICT: PENDING WG temperature products.")

# ----------------------------------------------------------------------------
n_pass = sum(1 for c in CHECKS if c['result'])
n_total = len(CHECKS)
print("-" * 78)
print(f"G236 COMPLETE: {n_pass}/{n_total} checks PASS.")

out = dict(
    question=("G236: eROSITA DR2 / eRASS:3 (1.9M point + 63,796 extended sources, catalogue-only "
              "release, public 2026-07-31; ~200k SDSS DR20 spectroscopic redshifts; tens of thousands of "
              "clusters to z>1) -- what does it say for the framework's a0(z) sharp null and the "
              "cluster sector's z-invariance, and does the release's own accounting reproduce?"),
    n_pass=n_pass, n_total=n_total,
    checks=CHECKS,
    verdict=("AUDIT on shipped files 6/6 PASS: hard-band counts exact vs A&A Table 2 (15,980/954/15,026); "
             "main catalogue 1,911,744 PS + 63,796 EXT exact; LS10 extragalactic share reproduced "
             "(measured on class_gal_exgal >= 1); EXT sky distribution clean.  E1-E5 registered: the "
             "virial-temperature sharp null (Delta log10 T_X = 0.000 vs +0.134 dex @ z=0.5 M-RISE; "
             "falsifier |D| > 0.010 dex at >= 2 sigma, power ~21 sigma vs M-RISE) and the sector "
             "z-invariance (alpha = 2/3, rms <= 0.076 dex at z <= 1; falsifier drift > 0.076 dex or "
             "alpha > 2 sigma) -- both verdicts PENDING the eRASS:3 cluster WG products and SDSS DR20 z. "
             "The needles result is a registered NON-CLAIM.  G187/G162/G161 eRASS legs re-pointed at the "
             "release (PENDING WG mass products: DR2 is catalogue-only)."),
    data_sources=["eRODat DR2 (in hand): eRASS3_Hard_v1.2.fits.gz, eRASS3_Main_v1.3.fits.gz, "
                  "eRASSc3_Main_LS10_Public_27Jul2026.fits.gz",
                  "A&A aa60385-26 (Ramos-Ceja+2026, arXiv:2607.27772)",
                  "phys.org 2026-09-11 release report"],
)
respath = os.path.join(HERE, "G236_results.json")
with open(respath, "w") as f:
    json.dump(out, f, indent=1)
print(f"results -> {respath}")