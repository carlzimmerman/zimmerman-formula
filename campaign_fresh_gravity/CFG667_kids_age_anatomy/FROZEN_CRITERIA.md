# CFG667 FROZEN CRITERIA: what is the KiDS age signal? (stellar-mass bias vs extra mass, on raw lensing)

Date: 2026-10-12. Written and committed ALONE, before any CFG667 code or score. Block CFG660–669. Nothing below may be edited
after this commit.

Raw data only (owner's 10-10 rule): the raw KiDS excess surface density of the CFG700 / CFG589 early-type tertiles, no law, no κ,
no footing, no environment model, no ΛCDM or MOND ingredient. Not "theory closed". Nothing will be phrased as "the data favour the
framework".

## 0. What has been seen (stated before any choice below)

- CFG700 (raw): OLD vs YOUNG f30 early types at identical LePhare M*: K9 ratio ×1.46 (A = +0.166, empirical Z +2.33); per band
  K-in ×1.65 (Z 1.57), K-mid ×1.70 (Z 2.42), K-out ×1.28 (Z 0.86). Bands are in bin index; K-in = bins 12–14 (highest g_bar,
  innermost), K-out = bins 6–8. CFG700's own caveat: LePhare masses of the reddest galaxies may be biased low.
- **Author's expectation, before any score:** the per-band numbers lean inner-concentrated (stellar-mass-like), but CFG700 did
  not measure the radial shape; both parts below may come out undecided.
- The dark-energy clock (CFG666) is closed; this lane tests the anomaly itself, not a model of it.
- No colour → age mapping is used (none exists on the record, and one typed from memory would be a knob).

## 1. Part A (primary): the radial shape of the raw OLD/YOUNG ratio

Same masks and estimator as CFG700 (CFG585's head and CFG531's `esd_loo`, executed unedited; CFG589's stratified tertiles).
Per bin k = 6…14 (K9): log-ratio ℓ_k = log10(ΔΣ_OLD,k / ΔΣ_YOUNG,k); covariance from the patch leave-one-out arrays
(jackknife, as CFG700). Fit ℓ_k = A + S·(k − 10)/8 by generalised least squares with the jackknife covariance (if its condition
number exceeds 1e8, the diagonal is used and this is reported). S is the inner-minus-outer change of the log-ratio across K9.
- **INNER-CONCENTRATED** (stellar-mass-like) if S > 0 with Z = S/σ_S ≥ 2;
- **OUTER-RISING** (extra-mass-like) if S < 0 with Z ≤ −2;
- **NOT DECIDED** if |Z| < 2.

## 2. Part B: an independent stellar-mass estimator

Taylor et al. 2011 colour–M/L relation (GAMA, Chabrier IMF): log10 M*_T = −0.68 + 0.70 (g − i) + 0.4 (4.58 − M_i), with g, i the
LePhare rest-frame absolute magnitudes (MAG_ABS_g, MAG_ABS_i) of the same matched lenses. It shares photometry with LePhare but not
the SED fit.
- B1 (reported): median[log M*_T − LMSL] for OLD minus YOUNG (they are matched in LMSL by construction).
- B2: rebuild the tertiles at fixed log M*_T (10 decile bins of M*_T within the same early-type f30 set; within each bin, tertiles
  of the u−r residual, as CFG589) and recompute the K9 amplitude A_T with the patch jackknife.
  - **M\* BIAS EXPLAINS** if A_T ≤ 0.05 and |Z_T| < 1;
  - **SIGNAL PERSISTS** if A_T ≥ 0.12 and Z_T ≥ 2;
  - **PARTIAL** otherwise.
  Stated limit: both estimators are colour-based; a bias common to both is not tested.

## 3. Combined label

- **STELLAR-MASS ARTEFACT LIKELY** if Part A is INNER-CONCENTRATED or Part B is M* BIAS EXPLAINS (and neither points the other way);
- **EXTRA MASS LIKELY** if Part A is OUTER-RISING and Part B is SIGNAL PERSISTS;
- **UNDECIDED** otherwise, with each part stated.

## 4. MUTATE (`CFG667_MUTATE=1`, separate outputs, exit 1 iff both bite)

- M1 (linearity): OLD weights × 0.8 must shift A by log10(0.8) within 0.002 and leave S unchanged within 0.002.
- M2 (power): OLD weights × 1.5 in bins 12–14 only (an injected inner excess) must give S > 0 with Z ≥ 2.

## 5. Machine rules

Light: one process, `nice -n 10`; reuses the precomputed per-lens stacks; allowed while the 1024³ run is live.
