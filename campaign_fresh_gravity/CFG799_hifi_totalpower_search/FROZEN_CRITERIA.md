# CFG799 FROZEN CRITERIA: total-power search of archival Herschel/HIFI band-1a data for a mirror line at 541.7 GHz

Committed alone, before any search statistic is computed. Data-format exploration of one test observation
(obsid 1342191482, an LO setting far from the target) was done only to learn the file layout; no spectrum near the
target frequency was looked at.

**Hypothesis under test.** A kinetically mixed vector field of mass 2.240 meV (CFG797; the identification is
equivalent to κ = ½, which is fitted) makes the Herschel primary mirror emit a narrow line (intrinsic width ~0.3 MHz)
at a fixed frequency in the spacecraft frame. **The framework predicts NO line** (PAPER52 / CFG797: a line kills the
framework; a null closes the converter window and keeps it). Not "theory closed".

**Frequencies (declared).**
- Primary ν_t = **541.664 GHz**: the value the committed CFG797 code computes from the canonical footing a₀ = 9.3603e-11.
  The last quoted digit of a₀ alone moves ν by ~3 MHz, and the physical a₀ uncertainty is much larger, so a null
  excludes a line only near this frequency. It does not exclude the mass.
- Secondary ν_2 = **541.700 GHz**: the rounded value used in PAPER52 and the lane brief.
- Each frequency is tested at 5σ. No further trials correction is applied for the two.
- Informational scan: ν_t + δ for δ = −40…+40 MHz in 0.5 MHz steps. It is reported, but it does not set the class.

**Why total power.** Level-1 sky spectra are reference-subtracted (DBS: ON chop phase minus OFF chop phase). Both
phases view the sky via the primary, so a mirror line cancels there. Total power, which compares sky phases against
the internal hot/cold loads, keeps it.

## Data and selection
- Source list: the 95 band-1a observations covering 541.7 GHz in `../CFG798_herschel_hifi_dish/cfg798_matches.csv`.
- Modes used: HifiPointModeDBS, HifiPointModeFastDBS, HifiSScanModeDBS, HifiSScanModeFastDBS.
- Excluded, declared now: LoadChop scans (4 obs) and the one FastDBS raster (1 obs). In those modes the reference
  structure differs, and they hold about 0.8 h of the 13.1 h.
- Per observation, download Level-0 and Level-1 one at a time from the ESA HSA. Keep only the WBS boxes that hold
  the science datasets with 3.9 ≤ |ν_t − LO| ≤ 8.1 GHz, plus their nearest comb/zero and hot/cold datasets. Delete
  the tars immediately. Keep a manifest.
- Disk rule: do not download if free space on the volume would fall below 25 GB.
- Spacecraft frame:
  - LO = Level-0 `LoFrequency`, which carries no Doppler correction.
  - IF axis = the Level-1 frequency axis of the hot/cold rows of the same LO setting (comb-calibrated, not
    Doppler-corrected).
  - Level-0 channels 52…2027 of each 2048-channel sub-band = the 1976 Level-1 channels.
  - RF = LO + IF in the USB and LO − IF in the LSB.
  - The sideband that holds ν_t is the one with IF in 3.9–8.1 GHz.

## Total-power calibration (per Level-0 row, per sub-band, per polarisation)
- Dark: subtract the zero spectrum (the lower row of the nearest preceding WBS_Zero_Comb dataset), scaled per channel
  parity (even/odd) by the ratio of the row's dark pixels to the zero row's dark pixels. On the test file this
  reproduces the Level-1 hot/cold counts to 1.4e-4.
- Normalisation N = (counts − dark)/t:
  - Hot and cold rows: t is the Level-1 `integrationTime` of the same row.
  - Science rows: t_S is set by the **Level-1 anchor**. For each science dataset, compute my reconstructed
    reference-subtracted spectrum D = mean(kept rows) − mean(REF rows) at t_S = 1 s. D ∝ 1/t_S exactly. Compare it
    with the mean of the Level-1 kept rows after 16-channel boxcar smoothing.
  - The scale is the reduced-major-axis ratio std(L1)/std(D), signed by the correlation.
  - t_S(obs) = median over datasets and polarisations.
- Kept / ON rows are the rows whose sequenceNumber appears in the Level-1 dataset. REF rows are the other sky rows of
  the same Level-0 dataset.
- Hot/cold:
  - Average the nearest preceding and the nearest following hot/cold datasets with |ΔLO| < 1 MHz, or use the one
    that exists.
  - Hot = the row with the larger median.
  - Load temperatures come from the `hot_cold` column, converted to Rayleigh–Jeans-equivalent J(T) at 541.7 GHz.
  - Load coupling efficiencies are taken as 1 (provisional).
- T_tp = (N_sky − N_C)/(N_H − N_C) · (J_H − J_C) + J_C. This is a DSB receiver-input scale.
- One spectrum = the mean T_tp of all sky rows (ON + REF) of all science datasets at one LO setting (rounded to
  1 MHz), per polarisation, per observation. For each spectrum, also keep:
  - the REF-only mean;
  - the Level-1 mean of kept rows (same channels);
  - the Level-1 per-channel flags;
  - the full sub-band spectra, for the IF-shuffle control.

**L1-anchor control (per observation).**
- The observation is used only if both conditions hold:
  - the relative MAD scatter of the per-dataset t_S is ≤ 10%;
  - the median correlation of the smoothed D with the smoothed L1 is ≥ 0.5.
- Failing observations are listed and excluded.
- If more than half of the downloaded observations fail, the class is INCONCLUSIVE.

## Masks (declared)
- **M1, water image.** Drop a spectrum if the image frequency 2·LO − ν_t is within 0.6 GHz of 556.936 GHz.
- **M2, edges.** The sub-band must contain ν_t ± 100 MHz, with the 10 outermost channels at each end excluded.
  - If two sub-bands qualify, use the one with the larger margin, never both.
  - The common window serves the target, the controls and the scan.
- **M3, astrophysical lines** (Level-1 keeps source lines, a mirror line is absent from it).
  - At each statistic centre, mask the spectrum if the Level-1 mean shows a feature: take the 3-channel smooth, after
    removing the same degree-3 baseline over ±50 MHz.
  - "Feature" means a peak within ±10 MHz of the centre whose |value| exceeds 5 × the robust (MAD) rms of that
    detrended Level-1 window.
  - The rule is identical for the target, the controls and the scan.
- **M4, flags.** Channels with a nonzero Level-1 flag get zero weight. A spectrum is dropped for a statistic if any
  flagged channel lies within ±3 MHz of the centre or if more than 20% of the window is flagged.

## Statistic
- **Profile.** A Gaussian with FWHM = √(0.3² + 1.1²) = 1.14 MHz: the intrinsic width convolved with the WBS
  resolution. Profile mismatch with the true WBS response is a ±10% amplitude systematic (provisional).
- **Per-spectrum fit.**
  - Fit window: channels with |IF − IF_c| ≤ 50 MHz, where IF_c = |ν_c − LO|.
  - Linear least squares: Legendre polynomial of degree 3 in (IF − IF_c)/50 MHz, plus the fixed-centre,
    fixed-width Gaussian.
  - Output: peak amplitude a_i, and σ_i from the covariance scaled by the residual variance.
- **Stack.** Weighted mean a = Σ w_i a_i / Σ w_i with w_i = 1/σ_i². σ_a = (Σ w_i)^(-1/2) × max(1, √χ²_ν), where
  χ²_ν is the reduced χ² of the a_i about a. z = a/σ_a. H and V enter as separate spectra.
- **95% upper limit.** a95 = max(a, 0) + 1.645 σ_a.
- **Conversion to ε.**
  - Line area on the DSB scale: W_DSB = 1.0645 · a · FWHM.
  - Single-sideband area: W_SSB = 2 W_DSB, assuming sideband gain 0.5 (provisional).
  - One polarisation receives P_pol = k_B W_SSB = ½ · (1/S) · (2/3) ε² ρ c³ A.
  - Inputs (CFG797): ρ = 0.01 M☉ pc⁻³ and A = 9.6 m². S is the geometry/coupling suppression: primary 50,
    bracket 10…1000.
  - Then ε = √(2 S k_B W_SSB / ((2/3) ρ c³ A)).
  - Report ε95 against the converter window 4e-9 and the kill line 1e-12.

## Controls (all must pass, or the class is INCONCLUSIVE)
- **C1, injection.**
  - Add a Gaussian of known peak amplitude A_inj = 10 σ_a(no-injection) at ν_t to every spectrum's total power,
    before baseline fitting.
  - Recovery r = (a_inj − a_0)/A_inj must lie in [0.8, 1.2].
- **C2, null offsets.**
  - Stack at ν_t + δ for δ ∈ {−20, −10, −5, +5, +10, +20} MHz with the same estimator and masks.
  - Each |z| < 3, and Σ z² over the six offsets must have χ²₆ p > 0.001.
- **C3, IF-shuffle.**
  - For each spectrum i, evaluate the statistic at the target IFs IF_c,j of the other spectra j. Use only cases where
    both RFs of that IF (LO_i ± IF_c,j) lie more than 60 MHz from ν_t and ν_2, and the window fits the sub-band.
  - Stack with the same weighting. |z| < 3 is required: an IF-fixed artefact would show up here.
- **C4, L1 anchor.** As above.

## Classes
- **LINE CANDIDATE.** At ν_t or ν_2, all of the following hold:
  - z ≥ +5 and C1–C4 pass;
  - RF-not-IF holds:
    - (a) the low-IF and high-IF halves of the spectra (split at the median target IF) each give z ≥ 2, and the two
      agree (p > 0.01);
    - (b) C3 passes;
  - the same estimator on the REF-only total power gives z ≥ 3, with an amplitude within 2σ of the primary;
  - **absent in Level-1**: the same estimator on the Level-1 means gives |z_L1| < 3.
- **NULL.** z < 5 at both frequencies and C1–C4 pass.
  - Report a95 and ε95 for S = 10, 50, 1000.
  - A 3 ≤ z < 5 excess is reported as a hint, not a detection.
- **INCONCLUSIVE.** Any of these:
  - any control fails;
  - fewer than 10 usable spectra;
  - z ≥ 5 that fails RF-not-IF, REF-only or the Level-1-absence test (artefact at the target);
  - z ≤ −5.

**MUTATE.**
- Separate outputs: `cfg799_MUTATE.out` and `cfg799_results_MUTATE.json`.
- Inject a line at ν_t into the total-power spectra only (not into Level-1), with peak amplitude 10 × σ_a from the
  main run's JSON, before all fitting.
- It must be classed LINE CANDIDATE, or the pipeline is declared blind.

**Machine rule.** Before each processing step, check for a running 1024³ simulation (`cfg650_pm|cfg654_pm|run_65`). If
one is running, do no computation.

External numbers are provisional: HIFI sideband gain, load coupling, WBS response and S.
