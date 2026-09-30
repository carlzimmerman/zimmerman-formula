# CFG201 — does CFG198's mass-route drift appear in a prior-anchored sample? Price+2021 RC41 (z 0.66–2.45). FROZEN CRITERIA

Written 2026-09-29 in the calculation chat, before any CFG201 number. **κ = ½ FITTED, NOT DERIVED.**

## Why

CFG198 found that MUSE-DARK's DC14-fitted disc mass (no SED prior) drifts against the SED stellar mass by −0.72 dex per unit z, and that this drift carries III's a₀ rise. Price+2021's RC41 disc–halo fits anchor M_bar with a 0.2-dex Gaussian prior centred on the SED M* plus the gas. Does the fitted mass still drift with z?
- If it does, the drift is a generic property of joint disc–halo fits at z ~ 1–2.
- If it does not, it is specific to prior-free fits.
This lane tests the mass route only. It computes no a₀. CFG199 showed that the absolute acceleration scale from these tables cannot be reconstructed reliably.

## What was known when this was written

- The data chat's note (`data_assembly/price2021_rc41/README.md`, ada32e710):
  - the fitted log M_bar minus log(M*_SED + M_gas) has a median of +0.05 dex (16–84%: −0.08 to +0.33) and exceeds 0.3 dex for 7 of 41;
  - f_DM(R_e) has a median of 0.43;
  - the gas mixes measured values with scaling-relation values, with no per-galaxy flag.
- No z-dependence of anything was reported, and this lane has computed none.
- **Hand expectation, disclosed:** a 0.2-dex prior should damp any drift. I expect a slope well below CFG198's 0.72 in size, but I do not know its sign.

## Data and quantities

- **Data:** `data_assembly/price2021_rc41/price2021_rc41.csv`, all 41 galaxies.
- **Δ_bar** = `logMbar_1D` − log₁₀(10^`logMstar_SED` + 10^`logMgas`): the fitted minus the prior-centre baryonic mass.
- **Statistic:** the Theil–Sen slope of Δ_bar on z, with a 95% CI from 10,000 bootstrap resamples over galaxies (seed 201).
- **Also reported:**
  - the same slope divided by the prior width (0.2 dex per unit z as the scale);
  - Spearman ρ(Δ_bar, z);
  - the Theil–Sen slope of f_DM(R_e) on z (descriptive, not graded);
  - the median Δ_bar in z-halves.

## Decision rows (95%)

- **D1:**
  - If the CI excludes 0 and its sign is negative (fitted below the prior centre at high z, as in MUSE-DARK): **"the drift appears in a prior-anchored sample"**.
  - If the CI excludes 0 and the sign is positive: **"a drift of the opposite sign"**.
  - If the CI contains 0: **"no significant drift"**.
- **D2 (comparison with CFG198):** does the CI exclude −0.72, CFG198's P1 slope?
  - Yes: this sample's drift is smaller than MUSE-DARK's at 95%.

## Controls

- **C1:** the 41 rows parse, with z in [0.65, 2.46], and every Δ_bar is finite.
- **C2:** on a synthetic sample with an injected slope of −0.5 dex per unit z and 0.1 dex scatter on the real z values, the estimator recovers −0.5 within its own 95% CI.
- **MUTATE=1:** Δ_bar → Δ_bar − 0.5 (z − median z). The slope must fall by 0.5 ± 0.05, and D1 must read "the drift appears". Outputs are written separately.
