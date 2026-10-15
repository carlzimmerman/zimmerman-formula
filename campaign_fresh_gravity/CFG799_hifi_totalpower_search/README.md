# CFG799: total-power search of archival Herschel/HIFI data for a mirror line at 541.7 GHz

**Class: NULL** under the frozen rule (FROZEN_CRITERIA.md + addendum A, committed before any target statistic).
- No line at 541.664 GHz (primary) or 541.700 GHz (secondary), in the spacecraft frame.
- A 3.2σ hint at 541.700 GHz is reported. It is not a detection.
- The framework predicts no line, so this result is consistent with the framework. It is not a confirmation, and not
  "theory closed".

**What was tested.**
- Hypothesis: a kinetically mixed vector of mass 2.240 meV would make the Herschel primary emit a narrow line at a
  fixed RF.
- Such a line cancels in Level-1 data, because the DBS ON and OFF phases both view the sky via the primary.
- It survives in total power: sky phases against the internal hot/cold loads.
- This lane rebuilt total power from Level-0 counts:
  - zero spectrum scaled by dark pixels;
  - hot/cold loads from bbtype 6005;
  - Level-1 frequency axes, spacecraft frame;
  - timing scale anchored on Level-1.
- Statistic: a fixed-width Gaussian (FWHM 1.14 MHz) plus a degree-3 baseline over ±50 MHz in each spectrum, stacked in
  RF across observations, LO settings and polarisations.

**Data.**
- 95 band-1a observations cover 541.7 GHz (CFG798 list):
  - 5 LoadChop/raster observations were excluded by the frozen mode rule (0.77 h).
  - **55 observations were reduced.** These are all 53 DBS/FastDBS point observations plus 2 DBS spectral scans.
  - **53 passed the Level-1 anchor**; 2 failed.
  - **49 contributed spectra:** 150 fitted spectra out of 152 after masks. Their CFG798 integration time is **6.99 h**
    of the 13.1 h.
- 35 DBS spectral scans (4.23 h) were **not downloaded**:
  - the HSA server cuts transfers of about 1 GB and does not support resume;
  - the owner asked to finalise.
  - One scan, 1342250735, was retried once from zero and succeeded.

| | 541.664 GHz (primary) | 541.700 GHz (secondary) |
|---|---|---|
| stacked a (DSB peak) | −6.7 ± 7.7 mK, z = −0.86 | +20.5 ± 6.5 mK, z = +3.17 |
| REF-only / Level-1 z | −0.93 / −0.72 | +3.15 / +0.03 |
| low-IF / high-IF z | +0.16 / −1.66 | +2.58 / +1.93 |
| a95 | 12.7 mK | 31.1 mK |
| ε95, S = 10 / 50 / 1000 | 8.6e-12 / **1.9e-11** / 8.6e-11 | 1.3e-11 / **3.0e-11** / 1.3e-10 |

**Reading against the CFG797/CFG798 targets.**
- **Converter window (ε ≈ 4e-9): closed** by ×200 (S = 50) and by ×47 even at S = 1000.
- **Kill line (1e-12): not reached.** The primary case misses it by ×19.
- The stack is limited by baseline structure (χ²_ν = 2.8), not by radiometer noise. CFG798's 5.7–7.8e-12 forecast
  assumed radiometer-limited data.

**Controls (all pass).**
- C1 injection, 10σ: r = 1.000. This is exact by linearity of the estimator. As an informational check, a
  mismatched profile (FWHM 1.10 MHz, +0.2 MHz offset) gives r = 0.94.
- C2 null offsets ±5/10/20 MHz: z = −0.26, −1.53, −0.93, −1.25, −1.76, +0.23 (p = 0.24).
- C3 IF-shuffle: 3040 fits, z = +0.20.
- C4 Level-1 anchor: 53/55 observations pass.
- Informational scan (±40 MHz, 161 steps): max |z| = 4.45 at +38 MHz, i.e. the 541.700 hint region. No step reaches
  |z| ≥ 5.
- The scan and the 541.700 hint are worth one look in the scan data not downloaded. They are not a candidate:
  - the hint is below 5σ;
  - it falls in the look-elsewhere region;
  - it lies inside the Doppler range of source lines across epochs.

**MUTATE.** A 77 mK line injected at 541.664 GHz into total power only, not into Level-1, is recovered at z = +9.1.
- REF-only z = +10.1.
- Level-1 z = −0.7, as expected because the line was not injected there.
- RF-not-IF tests pass.
- It is classed **LINE CANDIDATE**. The pipeline bites.

**Converter-window tier (addendum A, single observation).** 48 of 48 observations individually exclude A_conv at 5σ for
S = 10, 50 and 1000 (A_conv = 2.8e3, 557 and 27.9 K DSB peak). Verdict at all three: **EXCLUDED**.

**Observations not used.**
- Level-1 anchor failed: 1342192348 and 1342192349 (G34.26).
- Reduced, but no spectrum survived the water-image or sub-band-edge masks: 1342213736 (NGC1068, IF 7.94 GHz),
  1342222311, 1342245598 and 1342271258 (IRC+10216).
- Excluded by mode: 1342218527, 1342239609, 1342190826, 1342192215 and 1342207574.
- Not downloaded (35 scans): 1342191504, 1342203743, 1342205491, 1342218633, 1342191499, 1342191481, 1342203742, 1342194491, 1342194178, 1342214341, 1342196516, 1342201077, 1342207575, 1342232978, 1342210754, 1342180458, 1342190219, 1342190099, 1342239610, 1342194492, 1342194483, 1342205468, 1342221429, 1342227163, 1342242817, 1342231526, 1342232812, 1342246470, 1342246495, 1342246463, 1342244791, 1342246489, 1342246474, 1342249631, 1342238588.

**Deviations from the frozen text (disclosed; made before the final run).**
- **D1.** The anchor uses MAD in place of std, after dropping flagged channels and channels more than 10 MAD out. The
  std version was wrecked by isolated Level-1 spike channels; on Mars it reached 1e3 K in two sub-bands.
- **D2.** t_S is the median over well-anchored datasets (corr ≥ 0.9). Pass rule: at least 30% of datasets well
  anchored, with scatter ≤ 10%. REF-only spectra use only those datasets. The reason: in FastDBS nod-B datasets, the
  ON/REF labels taken from Level-1 kept rows do not reproduce Level-1.
- **Engineering only.** Download retries, and point observations fetched before scans.

**Caveats (provisional).**
- S is a geometry/coupling bracket (literature, provisional).
- HIFI sideband gain is taken as 0.5 (the ×2 DSB→SSB factor).
- Load coupling efficiencies are taken as 1.
- WBS response is modelled as a Gaussian; profile mismatch is about ±10%.
- The Level-1 timing anchor sets the amplitude scale. On the test file it agrees with Level-1 continua to 4–10%.
- ν ∝ √a₀: the last quoted digit of a₀ moves ν by about 3 MHz, and the physical a₀ uncertainty moves it by GHz. So this
  null excludes a line only near the two declared frequencies. It does not exclude the mass.
- κ = ½ is fitted. ρ = 0.01 M☉ pc⁻³ assumes the hypothesis under test.

**Files.**
- `cfg799_fetch.py`: download one observation, extract the target boxes, delete the tars, reduce to npz. The data
  live outside the repository.
- `cfg799.py`: analysis.
- `cfg799.out` and `cfg799_results.json`: main run.
- `cfg799_MUTATE.out` and `cfg799_results_MUTATE.json`: MUTATE run.
- `cfg799_manifest.csv`: per-observation status and anchor.
- `cfg799_stack.png`: stacked residual and scan.
