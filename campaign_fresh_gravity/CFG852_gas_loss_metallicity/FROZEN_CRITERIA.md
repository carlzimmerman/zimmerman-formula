# CFG852 FROZEN CRITERIA: does the dwarf excess track gas loss (metallicity deficit at fixed stellar mass)? (before any script)

## Hypothesis (H-EX with each system's ACTUAL gas loss; no new constant)
Free cold energy = 5.364 × the baryons a system EXPELLED. A dwarf that blew out more gas through outflows carried away metals and
sits BELOW the stellar mass–metallicity relation (MZR) at fixed M★. **Prediction:** at fixed internal acceleration, the excess
over the law is LARGER for dwarfs with a more negative metallicity residual. Independent of dynamics: metallicity is chemistry.

## Sample and inputs
- **Primary:** CFG828's pressure-supported dwarfs (Υ_SFH; Δ = log10 g_obs/g_law at r_1/2, canonical, ν_e) that have an LVD
  metallicity (`metallicity` column; spectroscopic where available).
- **Secondary:** every LVD dwarf (MW, M31, field files) with σ, r_h, M_V and metallicity, pressure-supported (excluding LMC, SMC,
  and the gas-rich rotating dIrrs WLM, NGC 6822, IC 1613, Leo A, Sagittarius dIrr, Pegasus dIrr, and M 32), Υ_V = 2, same law and
  Δ as CFG828 (Wolf estimator at r_1/2 = 4/3 r_h; g_bar from M★/2).
- MZR: least-squares [Fe/H] = c0 + c1 log10 L_V over the same sample; δZ = [Fe/H] − MZR.

## Statistic and classes
- Partial Spearman of Δ with δZ controlling for log g_bar (residualise both on log g_bar by least squares; Spearman of residuals).
- **GAS-LOSS SIGNAL** if ρ < 0 with one-sided p < 0.05 in the primary AND p < 0.10 in the secondary (same sign).
- **OPPOSITE** if ρ > 0 with one-sided p < 0.05 in the primary. **NO SIGNAL** otherwise. NOT DIAGNOSTIC if primary N < 12.
- Declared confound: metallicity residuals also track star-formation duration (extended SF → higher Z), i.e. partly age; CFG827
  found no age dependence of Δ with SFH M/L, which limits but does not remove this confound.

## Controls
- K1: MZR slope c1 printed (literature for LG dwarfs ~0.3 dex per dex in L; informational, not a gate).
- MUTATE (separate output): (a) Δ_inj = −0.5 δZ + N(0, 0.1) (seed 852) must class GAS-LOSS SIGNAL; (b) δZ shuffled must not.

κ = ½ fitted; cold energy mass required; not theory closed.
