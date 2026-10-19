# CFG824 FROZEN CRITERIA: does the dwarf mass excess grow with formation age? ("fossil binding"; committed before any age data is read)

## Hypothesis H-FOSSIL (framework-motivated, NOT derived)
Cold energy is collisionless. Whatever a dwarf captured while it assembled keeps the phase-space density of its capture
epoch; it does not relax to today's settled law. A dwarf that assembled and quenched early captured from a denser universe
(ρ̄ ∝ (1+z)³) and so keeps a denser inner cold core. **Prediction:** the excess over the galaxy law,
E = ln(σ_obs / σ_law), increases with the stellar quenching lookback time τ90 (older → larger E).

## Disclosure: the hypothesis is POST-HOC for the MW 11
It was suggested by the CFG821/822 residuals: Draco, Ursa Minor, Sextans and CVn I (ancient) sit ~2× above the law; Fornax and
Leo I (extended star formation) sit on it. **The MW 11 are therefore the TRAINING set and are reported, never scored.**
The verdict comes ONLY from the out-of-sample set below.

## Data
- τ90 (lookback, Gyr) and τ50: Weisz et al. 2014, ApJ 789, 147 (HST CMD star-formation histories of Local Group dwarfs; VizieR
  J/ApJ/789/147), read once, as published.
- σ_obs, e_σ, M_V, r_h: the LVD tables in `real_research/data/dsph/` (`lvd_dwarf_mw.csv`, `lvd_dwarf_m31.csv`,
  `lvd_dwarf_local_field.csv`), same column rules as CFG821.
- **Out-of-sample set:** every dwarf with a Weisz+14 τ90 AND an LVD σ_obs AND r_h, that is NOT one of the CFG821 MW 11, and is
  not a rotating dIrr without a dispersion (no σ in LVD → excluded automatically). Ultra-faint MW satellites are included if
  they meet the rule.

## Prediction σ_law
- CFG821's isolated law, unchanged (`cfg821.py` `pred(g, a0, 0, False)`: Wolf estimator with M_b/2, ν(y) = 1/(1 − e^{−√y})),
  M_b = Υ_V L_V.
- **Primary:** Υ_V = 2, canonical a0 = 9.3603e-11. Alt footing 1.1312e-10 reported separately, never pooled.
- **Control C-ML (age-dependent stellar M/L, MUST be reported beside the primary):** Υ_V(τ50) = 2 × (τ50 / 10 Gyr)^0.7
  (an SSP-like scaling: younger mean age → lower M/L), clipped to [0.5, 4]. Old populations have higher M/L, so part of an
  age trend could be a stellar-mass systematic; H-FOSSIL is SUPPORTED only if the trend survives C-ML.
- No EFE in the primary (isolated law); EFE omitted, declared.

## Statistic and classes (out-of-sample set, primary)
- One-sided Spearman ρ(E, τ90) and a weighted linear slope dE/dτ90 with weights 1/[(e_σ/σ)² + 0.075²].
- **SUPPORTS** if N ≥ 8, ρ > 0 with one-sided p < 0.05 in the primary AND ρ > 0 with p < 0.10 under C-ML.
- **NO SIGNAL** if N ≥ 8 and the SUPPORTS condition fails with ρ ≥ 0 or p ≥ 0.05 either sign.
- **OPPOSITE** if N ≥ 8, ρ < 0 with one-sided p < 0.05.
- **NOT DIAGNOSTIC** if N < 8 or the τ90 range of the set spans < 4 Gyr (no lever arm).
- Report the training-set (MW 11) ρ and slope beside it, labelled TRAINING (not a verdict).

## Controls
- K1: σ_law for Draco equals CFG821's 4.61 km/s to 0.01.
- MUTATE (separate output): replace E with E_inj = 0.06 × τ90 + noise(σ = 0.1, seed 824) on the out-of-sample set → must
  class SUPPORTS; and shuffle τ90 (seed 824) on the real E → must NOT class SUPPORTS.

κ = ½ fitted; cold energy mass required; not theory closed. H-FOSSIL is a hypothesis; a SUPPORTS would motivate deriving
the capture density from the action, not establish it.
