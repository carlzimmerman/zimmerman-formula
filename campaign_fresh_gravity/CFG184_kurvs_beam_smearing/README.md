# CFG184 — how much of the KURVS outer σ can be beam-smeared rotation, and the pressure-support scale the data then allow

- **Criteria:** frozen in `FROZEN_CRITERIA.md` (cb1e8a77b), before any number.
  - The measured V(R) markers (`kurvs_rc_points.csv`) were not read, and are not read here; they are reserved for CFG189.
  - This lane reads only the authors' model curves and the data chat's control file.
- **Script:** `cfg184_beam_smearing.py`, about 20 s.
  - It runs CFG141's pipeline read-only and unmutated in every mode.
  - The three laws come from CFG175's machinery: flat, a₀ ∝ H(z), and a₀ ∝ t(z)/t₀.
- **Runs:**
  - The main run and both MUTATE runs exit 1, because of one kept control failure (C3, disclosed below). Every other check passes.
  - MUTATE=1 (FWHM × 3): the sample-mean f_bs rises from 0.087 to 0.731 and s_eff(1) falls from 0.931 to 0.501, as required.
  - MUTATE=2 (FWHM → 0.01″, bin → 0.1″): f_bs = 0.002 and s_eff(1) = 0.999, as required.
  - The first run is kept as `*_firstrun*`. It is identical, apart from two post-hoc reported additions.

## Bottom line

**Under the primary forward model, beam smearing is minor: it supplies 8.7% of the outer σ² on average (at most 23%, for KURVS-11). Kretschmer's correction then acts like s_eff = 0.93, and the decision cell barely moves. But the declared variant range reaches s_eff(1) = 0.40, below the crossing, in its most pessimistic corner. So both declared readings fire. Stated plainly: smearing moves K21 across the crossing only if the intrinsic rotation curve is steeper inside than the authors' own fit.**

- **Primary model** (the authors' model curve deprojected by sin i_SFR; Gaussian PSF FWHM 0.57″; 0.6″ bins; Hα scale R_eff/1.68), at CFG141's radii:

  | disc | σ_out (km/s) | σ_bs (km/s) | f_bs |
  |---|---|---|---|
  | KURVS-3 | 55.3 | 21.2 | 0.147 |
  | KURVS-7 | 69.1 | 14.8 | 0.046 |
  | KURVS-8 | 27.9 | 8.2 | 0.087 |
  | KURVS-9 | 51.3 | 15.7 | 0.094 |
  | KURVS-11 | 65.8 | 31.7 | 0.232 |
  | KURVS-13 | 61.3 | 7.0 | 0.013 |
  | KURVS-15 | 67.1 | 11.9 | 0.031 |
  | KURVS-16 | 73.0 | 23.1 | 0.100 |
  | KURVS-17 | 61.7 | 18.4 | 0.089 |
  | KURVS-21 | 76.8 | 14.2 | 0.034 |

  - Sample mean 0.087, median 0.088.
  - s_eff at the placed prescriptions: 1 → 0.931; 1.42 → 1.315; 1.62 → 1.498; 1.69 → 1.561; 3.00 → 2.747.
- **The declared variants** (108 in all: V(R) shape × PSF 0.32/0.57/0.82″ × bin 0.3/0.6/0.9″ × Hα scale ×0.7/1/1.5 × i_SFR or i*):
  - The sample-mean f_bs spans 0.021–0.710. The largest single-disc f_bs is 1.83, where the smearing alone would exceed the observed σ.
  - The maximal-smearing variant is the Freeman V(R), FWHM 0.82″, 0.9″ bins, R_d × 0.7 and i_SFR. It gives s_eff at the placed prescriptions: 1 → 0.396; 1.42 → 0.526; 1.62 → 0.584; 1.69 → 0.603; 3.00 → 0.939.
- **Post hoc, reported only:** s_eff(1) across all 108 variants.
  - Median 0.898; 16–84% range [0.759, 0.954]; minimum 0.367.
  - 11.1% of variants fall below s_mid = 0.67, and every one of them uses the Freeman shape.
  - With the authors' model curve, no variant crosses (minimum 0.762).
  - The Freeman shape normalised to V(R_max) puts a steep, peaked inner curve inside R_max, and it is that inner gradient the wide kernel mixes in.

## What it does to the three laws (decision cell μ = 0.67, s = 1, KURVS)

| input | flat | a₀ ∝ H(z) | a₀ ∝ t(z)/t₀ | break-even μ at s = 1 (flat / rival / T) | fit point s₀ (flat / rival / T) |
|---|---|---|---|---|---|
| σ_out (CFG160, CFG175) | +0.144 (+3.3σ) | −0.006 (−0.1σ) | +0.323 (+6.9σ) | 2.11 / 0.62 / 4.34 | 0.39 / 1.03 / < 0 |
| σ_int, primary model | +0.131 (+3.0σ) | −0.019 (−0.4σ) | +0.310 (+6.7σ) | 1.95 / 0.52 / 4.12 | 0.42 / 1.11 / < 0 |
| σ_int, maximal smearing | +0.002 (+0.0σ) | −0.147 (−2.8σ) | +0.179 (+3.5σ) | 0.69 / none / 2.28 | 0.98 / 3.38 / < 0 |

- **Under the primary model** the verdicts are those of CFG160 and CFG175:
  - the lean toward the rival at μ = 0.67;
  - T is gas-excluded under K21 (it needs μ = 4.1).
- **Under maximal smearing, K21's cell reads flat** (0.0σ), with the rival at −2.8σ.
  - T's break-even at s = 1 falls to 2.28, below the declared ceiling of 3.47.
  - T still under-predicts the decision cell by 3.5σ.
- **P0 (s = 0) is unchanged by construction.** No pressure term is used, so smearing does not enter: flat −2.3σ, rival −4.6σ, T +0.9σ.
- **The Girard+2021 scenario** (reported only; not the default reading): if the pressure-bearing dispersion were the molecular layer's, K21 would act as s = 0.167.
  - Flat −1.4σ, rival −4.1σ, T +2.1σ.
  - The Hα velocities need the Hα gas's own pressure support, so this scenario is not the default.

## Reading

- **The data allow a K21-scaled pressure correction with an effective scale of 0.93 under the authors' own rotation-curve model, and 0.76–0.96 across all its declared variants.** On that footing, beam smearing does not change where K21 sits relative to the crossing.
- **Only an intrinsic curve steeper inside than the authors' fit,** combined with the wide-PSF, big-bin and compact-Hα corner, moves K21 across the crossing (to 0.37–0.66). There the decision cell leans flat.
- **Cannot be separated with these data (stated plainly):** turbulent pressure support against unresolved bulk or non-circular motion and outflow broadening. σ_int is an upper bound on the pressure-bearing dispersion, not a measurement of it.
- **The a₀(z) front stays where CFG162, CFG167 and CFG168 left it:** a lean that depends on the calibration, the gas and now also the rotation-curve shape. It is not a detection either way.
- **The next test is CFG189:** the measured outer markers in place of the model velocity. It is proposed, and its criteria will be frozen before the markers are read.

## Disclosed departures

1. **C3 fails as frozen:** 1.762 km/s against a 0.5 km/s line. It is kept, and it makes every run exit 1.
   - A flat V(R) with FWHM → 0 still gives about 1.8 km/s with a 0.1″ bin. The pseudo-slit's off-axis spaxels (|y_s| up to 0.3″) span a real V_los gradient across 0.1″.
   - The frozen expectation was too tight, not the model wrong.
   - A post-hoc check with a 0.01″ bin gives 0.000 km/s (reported, not load-bearing).
2. **Both declared readings fire.** The frozen forms overlap: the primary gives "minor" and the maximal variant gives "can move K21 across the crossing". Both are reported, and the summary sentence says both.
3. **"The primary sample f_bs"** is implemented as the mean over the ten discs; the median and maximum are also given.
4. **The post-hoc distribution of s_eff(1)** over all 108 variants was added after the first run. It is reported, not a frozen reading.

## Controls

- **C0:** the angular scale is 8.46 kpc/″ at z = 1.54.
- **C1:** my re-implementation of CFG141's radii and weights reproduces its σ_out for all ten discs, to 10⁻⁹.
- **C2:** a face-on flat curve gives σ_bs = 0.
- **C4:** with σ_int = σ_out, the pipeline reproduces CFG160's cell (+0.1441 / −0.0060) and CFG175's T cell (+0.3227).

## Untested (declared)

- the Hα surface-brightness profile;
- the PSF shape: Moffat wings would add smearing;
- the per-spaxel bin size;
- disc thickness;
- non-circular motions;
- whether the authors' model is itself smeared (if so, f_bs here is biased low);
- the model-velocity provenance (CFG189);
- the COSMOS half of KURVS.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour any model, or that the theory is closed.
