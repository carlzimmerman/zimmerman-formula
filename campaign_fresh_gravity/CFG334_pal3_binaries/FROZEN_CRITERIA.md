# CFG334 FROZEN CRITERIA: can unresolved binaries inflate Pal 3's dispersion from Newton's value to the measured one?

**Lane:** orchestrator. The owner said "check the binaries on pal 3".

**Question.** CFG332 found the record's class-E rule (globulars are Newtonian) fails only because of Pal 3. Its measured σ is 1.70 (+0.38/−0.30) km/s from 22 stars, while Newton with the stellar-population M/L 1.6 predicts 0.44 × 1.70 ≈ 0.75 km/s. No individual radial velocities are on disk, so the test is a single-epoch binary Monte Carlo.

## Model (fixed before running)
- **Intrinsic velocities:** Gaussian with σ_int = 0.75 km/s (CFG332's Newtonian prediction). Bracket: 0.65 and 0.85.
- **Measurement errors:** each star gets an error e. Bracket: e = 0.5, 1.0 and 1.5 km/s; 1.0 is the primary.
- **The dispersion estimator:** a deconvolved Gaussian ML σ with known errors, matching how published dispersions are made, applied to N = 22 single-epoch velocities.
- **Binaries.** The fraction of stars that are binaries is f = 0.1, 0.3 or 0.5. Low-density outer-halo clusters are expected to have high binary fractions; 0.3 is the primary. Each binary has:
  - a primary mass of 0.8 M☉ (red giants and subgiants dominate the spectroscopic samples);
  - a flat mass ratio q in 0.1–1;
  - periods from Duquennoy & Mayor (1991): log-normal, mean log P = 4.8, σ = 2.3 (P in days);
  - thermal eccentricities;
  - random orientation and phase.
- **Truncation for giants:** periodastron separation ≥ 3 × 10 R☉, so the giant does not overflow its Roche lobe. Wide binaries are truncated at the cluster's tidal limit, a < 0.1 pc.
- **Draws:** 20,000 per configuration.

## Statistic and decision
For each configuration, report P(σ_obs ≥ 1.70) and the median σ_obs.
- **BINARIES EXPLAIN:** P ≥ 0.05 at the primary (σ_int 0.75, e 1.0, f 0.3).
- **PLAUSIBLE:** P ≥ 0.05 only at f = 0.5 or with e = 1.5.
- **NOT:** P < 0.05 in every configuration within the brackets.

## Controls
- **C1:** with f = 0 and e = 0, the median σ_obs recovers σ_int to within 3%.
- **C2:** with f = 0 and e = 1.0, the ML deconvolution is unbiased to within 5%.
- **C3:** a known orbit check. A circular binary with P = 1 yr, q = 1 and M₁ = 0.8 M☉ gives a semi-amplitude K ≈ 15.6 km/s × sin i, by direct formula; checked analytically.
- **MUTATE** (CFG334_MUTATE=1): set f = 0. P must fall far below the primary's value.

## Scope
This tests plausibility, not a measurement. Only multi-epoch velocities of Pal 3 members can settle it.

## Pre-freeze disclosure
- Known before freezing: the general literature expectation that sub-km/s systems are strongly binary-inflated (e.g. McConnachie & Côté 2010).
- No configuration had been run.
