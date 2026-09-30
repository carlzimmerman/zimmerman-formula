# CFG217 — the attack on CFG216: does RC100's "the rival's z-dependence is not in the data" survive gas-prior, pressure and selection systematics? FROZEN CRITERIA

Written 2026-09-29 in the calculation chat, at the orchestrator's request, before any CFG217 number. **κ = ½ FITTED, NOT DERIVED.** The aim is to break CFG216's result, not to protect it. Author decompositions, not a direct a₀ measurement.

## What is being attacked

CFG216 (364b63b0e): within RC100 (100 discs, z 0.61–2.52), the slope of δ on z is −0.029 [−0.071, +0.002] for the flat law and −0.092 [−0.128, −0.055] for the rival. That is 5.5σ and 4.9σ from the rival's expected slopes. The outcome was W-flat, in all four kernel/footing cells.

## Exposure, disclosed

- CFG216's numbers, including the sensitivities and the post hoc a₀(z) index (p = −0.72 ± 0.42, flat 1.7σ away, rival 4.8σ away).
- The orchestrator's referee brief for this lane.
- The Tacconi+2018 molecular-gas scaling μ(z, M★), as coded in CFG90 (read as source).
- The RC41 table's columns. Its per-galaxy SED masses and gas masses have not been looked at as numbers in this lane; CFG215 used them without printing them.
- **The key vulnerability, from hand estimation before any run:** μ_T18 for M★ = 10^10.7 grows from about 0.25 at z = 0.6 to about 1.05 at z = 2.5. That is +0.21 dex in M_bar. A gas fraction that did not grow with z would lower high-z baryons by that amount. In the mock below, that is about the size needed to turn a rival-true world into the observed slopes. So the outcome of G1 is a live risk, not a formality.

## Data

- `real_research/data/rc100_nestorshachar2023_table3.csv`: z, log M_bar, R_e, f_DM, V_c(R_e), σ₀. Baseline: exactly CFG216's sample and quantities.
- `data_assembly/price2021_rc41/price2021_rc41.csv`: SED M★ and log M_gas, for the RC41 galaxies found in RC100 by name (space ↔ underscore).
- **Held fixed in every variant:** g_obs = V_c²/R_e, except in G3. The fit's baryonic shape is unchanged, so g_bar scales with the baryonic mass. D = g_obs/g_bar.
- **δ, the laws, the kernels and the footings are as in CFG216.** ν_mono and canonical decide.

## G1 — the gas prior and its z-dependence

RC100's table has no separate M★ or gas. So M★ is reconstructed per galaxy by solving M★(1 + μ_T18(z, M★)) = M_bar (assumption A1: the prior centre was SED + Tacconi+18 molecular gas, with no HI).

- **Reconstruction check (C-recon).** For the RC41 galaxies in RC100, compare the reconstructed M★ with the SED M★.
  - Accept the reconstruction if the median |Δ log M★| ≤ 0.15 dex.
  - Otherwise G1 is run on the RC41 overlap only, using the actual M★ and M_gas, and labelled so.
- **Variants** (μ′ replaces μ at fixed M★; g_bar′ = g_bar (1 + μ′)/(1 + μ)):
  - **V1:** gas fraction held fixed with z: μ′ = μ_T18(z = 1.5, M★).
  - **V2:** μ′ = 0.5 μ.
  - **V3:** μ′ = 2 μ.
  - **V4:** μ′ = 0.18 μ (α_CO 0.8 instead of 4.36).
  - **V5:** μ′ = 1.49 μ (α_CO 6.5 instead of 4.36).
- Each variant is reported for both laws: the slope with a 95% bootstrap CI, the median δ, and the z-scores against the two expectations.

## G2 — is f_DM prior-driven?

- For the RC41 galaxies in RC100 with actual SED + gas: Δ_prior = log M_bar,fit − log(M★ + M_gas).
- Report the Spearman ρ between δ_flat and Δ_prior.
- **"Prior-driven"** iff |ρ| ≥ 0.3 and p < 0.05.
- Also report the slope of δ_flat on z after removing the Δ_prior dependence (Theil–Sen on the residuals of δ_flat regressed on Δ_prior).

## G3 — the pressure term

- V_c is taken to include the Burkert term, so V_c² = V_rot² + 3.36 σ₀² at R_e (A2: assumed, for RC100 as for RC41).
- Variants: α = 1.68 and α = 0, with V_c′² = V_c² − (3.36 − α) σ₀², g_bar fixed and D′ = g_obs′/g_bar.
- The expected slopes are recomputed with each g_obs′.

## G4 — the negative flat slope

- The δ_flat slope in the 62 non-RC41 galaxies (−0.055 [−0.099, −0.007] in CFG216) is recomputed under every G1 and G3 variant.
- **"Gas-scaling-sensitive"** iff its 95% CI contains 0 under V1.

## G5 — the mock (can a gas mis-scaling alone produce the pattern?)

- The mis-scaling is g_bar,analysis = g_bar,true × 10^(β log₁₀((1 + z)/2.5)), with β in dex per dex. The galaxies' own g_obs and z are kept.
- **M1, flat truth:** g_bar,true from the flat inversion. Find the β at which the mock's δ_flat slope equals the observed −0.029.
- **M2, rival truth:** g_bar,true from the rival inversion. Find the β that minimises χ² against BOTH observed slopes (δ_flat −0.029 ± 0.018, δ_rival −0.092 ± 0.019). Report the χ² there.
- For each β, the implied differential M_bar mis-scaling between z = 0.6 and z = 2.5 is ΔlogM = β log₁₀(3.5/1.6).
- **Plausible** iff |ΔlogM| ≤ 0.2 dex. That is a factor of about 2.3 in gas at a gas fraction of 0.5 differing between the two redshifts.
- **M2 "produces the pattern"** iff the minimum χ² < 2 (both slopes within 1σ on average) at a plausible |ΔlogM|.

## G7 — is the z-slope just a g_bar slope?

- Regress δ on log₁₀(g_bar/a₀) with Theil–Sen (slope b_g). Then take the Theil–Sen slope of the residuals on z (the whole procedure is bootstrapped).
- Report b_g and the residual z-slope for both laws.
- The expected residual z-slopes under each truth come from the same procedure on the mocks.

## Decision rows

- **D1.** The deficit SURVIVES a variant iff the rival's slope has a CI whose upper end is below 0 and the z-score against the rival's expectation 0 is ≥ 3.
- **D2.**
  - "ROBUST to the gas prior" iff it survives V1–V5. Otherwise the row is "gas-dependent", and the variants that break it are listed.
  - The same rule applies to G3 ("robust to the pressure term").
- **D3 (headline).** CFG216's outcome is
  - "attack-robust" iff it survives G1, G3 and G7, M2 does NOT produce the pattern at a plausible |ΔlogM|, and G2 finds no prior-driven dependence;
  - "attack-broken" if any of those fails;
  - "attack-mixed" otherwise.
- Every row is reported in full; there is no threshold tuning after the numbers are seen.
- **Language:** no sentence says the data favour the framework.

## Controls

- **C1.** A synthetic galaxy placed exactly on each law returns δ = 0.
- **C2.** The baseline slopes, medians and z-scores reproduce CFG216's committed values to 1e-9.
- **C-recon.** As above, reported.
- **C4 (mock machinery).** In the flat-truth mock at β = 0, the slopes are exactly (0, −0.060) (CFG216's expectations). At a known β, the mock's g_bar,analysis / g_bar,true equals the injected factor to 1e-12.
- **MUTATE=1.** D_obs × 10^(0.2 (z − z_med)) in the baseline. The baseline δ_flat slope must move by +0.2 to 1e-9, and the variants' slopes must move by amounts within 0.05 of it. Outputs are written separately.
