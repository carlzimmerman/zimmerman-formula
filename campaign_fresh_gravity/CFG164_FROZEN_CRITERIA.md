# CFG164 — a measured gas prior for the KURVS discs from PHIBSS (Tacconi et al. 2013), and the decision-cell verdict marginalised over it. FROZEN CRITERIA

Written 2026-09-29, at the orchestrator's go, before any PHIBSS gas value has been examined. Only sample-definition fields (flags, z, M*) were counted in order to fix the rule below. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## Why

- **CFG162 reduced the KURVS a₀(z) test to one quantity, the total cold gas.** Across the published pressure prescriptions (s = 1.0–1.7 in units of Kretschmer's α):
  - flat a₀ fits for μ = M_gas/M* ≈ 2.1–3.7;
  - the rival a₀ ∝ H(z) fits for μ ≈ 0.6–1.7.
- **The KURVS gas is unmeasured.** This lane replaces the declared bracket with a prior measured on the nearest CO sample in the repo.
- **An honest "the prior is uncertain by X" is the point.** A non-diagnostic answer is valid.

## Data

- **The table:** `data_assembly/kmos3d_phibss/phibss13_joined.csv`, the 73 rows of Tacconi et al. 2013 (ApJ 768, 74), tables 1 and 2.
- **The clean set,** which reproduces the orchestrator's count of 51:
  - co_upper_limit = 0, so the 6 CO upper limits are out;
  - fgas_inconsistent_in_source = 0, so the 3 documented inconsistent rows are out;
  - Mmol, M* and z_CO are all finite;
  - comp ≠ "se", so the one secondary-component row is out.
- **μ_mol = Mmol/M*,** as tabulated. Tacconi et al. used the Galactic conversion factor; their Mmol carries a stated 50% systematic and M* a 30% one.

## The priors (declared rules)

- **Primary: the mass- and redshift-matched rows.** z_CO ∈ [1.0, 1.7] and log M* ∈ [9.5, 10.8], which is KURVS's ten-disc range, 9.55–10.68, padded by about 0.1 dex. N = 17.
  - **The fact that decides the reading:** every clean PHIBSS row at z < 1.7 has log M* ≥ 10.40, while 8 of the 10 KURVS discs lie below 10.4. The matched rows therefore sample only KURVS's high-mass edge.
  - Each KURVS disc draws its μ_mol independently and uniformly from these 17 rows.
- **Variant M (mass-scaled):**
  - Fit log μ_mol = a + b (log M* − 10.5) by ordinary least squares to all clean z < 1.7 rows (N = 38).
  - Each KURVS disc gets 10^(a + b(lm_i − 10.5) + ε), where ε is drawn from the fit's residual scatter.
  - For discs below log M* 10.40 this is an extrapolation, flagged as such.
- **Variant Z (redshift-scaled):** the primary draws multiplied by [(1 + z_i)/(1 + z_CO,j)]^2.5, with z_i the KURVS disc's redshift and z_CO,j the PHIBSS row's. The exponent 2.5 is a round declared value, not a fit; this variant sizes the redshift offset only.
- **Coherent systematics per draw** (one factor applied to all ten discs in a draw):
  - the Mmol systematic, a lognormal with σ_ln = ln 1.5;
  - the PHIBSS M* systematic, a lognormal with σ_ln = ln 1.3 dividing μ.
- **The α_CO bracket, reported and not drawn:** Galactic (the primary, as Tacconi et al. used) and ULIRG-like (× 0.8/4.36).
- **The HI bracket, reported as separate priors and not drawn; it is not data:** μ = μ_mol × (1 + h), with h ∈ {0, 0.5, 1}. No HI is measured at z ≈ 1.5.
- **Draws:** 4,000 per prior, seed 164.

## What is computed

- **P1, the prior against CFG162's windows.** The fraction of draws whose sample-level μ̄ lies:
  - in the rival window [0.6, 1.7];
  - in the flat window [2.1, 3.7];
  - between the two windows (1.7–2.1);
  - below 0.6;
  - above 3.7.
  - μ̄ is the median of the ten per-disc μ_i in a draw. The same fractions for the per-disc μ_i are reported.
- **P2, the decision-cell verdict marginalised over the prior** (δ = 0, canonical, CFG160's pipeline with a per-disc μ_i):
  - For each draw, Δ′_flat and Δ′_H (anchor-corrected; SPARC with its measured gas) are classified by CFG160's map: lean flat, lean rival, both within 2σ, or neither.
  - The probability of each class is reported at the placed prescriptions s = 1.00 (Kretschmer, the primary), 1.42 (Dalcanton & Stilp), 1.62 (fixed height), 1.69 (Price) and 3.00 (self-gravitating), as s × K21's α.
  - The medians and 16–84% ranges of Δ′_flat/σ and Δ′_H/σ are reported.
- **P3, the KURVS-15 check:** the prior's μ draws for KURVS-15 against its dust limit from CFG163. That limit is μ_dust < 1.90 at the nominal calibration and < 3.79 with gas-to-dust × 2. The fraction of the prior above each is reported.
- **The size of the uncertainty,** X: the spread of the P2 class probabilities, and of μ̄'s median, across the primary prior, Variant M, Variant Z, the α_CO bracket and the HI bracket.

## Selection differences (stated before the data, with their expected directions)

- **Stellar mass.** PHIBSS at z < 1.7 spans log M* 10.40–11.23; KURVS spans 9.55–10.68. Gas fractions rise toward lower mass, so the primary prior likely UNDER-states KURVS's gas. Variant M sizes this.
- **Redshift.** PHIBSS here is at z 1.0–1.53, KURVS at 1.33–1.61. Gas fractions rise with z, so this is again an UNDER-statement. Variant Z sizes it.
- **CO detection.** Dropping the 6 upper limits biases the prior toward gas-rich galaxies, an OVER-statement. It is not corrected.
- **Selection.** PHIBSS is SFR- or optically selected massive main-sequence galaxies; KURVS is Hα-selected and rotation-supported (KGES/KMOS3D). The net effect is unknown.

## Checks

- **C1 CONTROL:** with every KURVS disc at μ_i = 0.67, the per-disc pipeline reproduces CFG160's committed decision cell (Δ′_flat +0.1441, Δ′_H −0.0060, 4 decimals).
- **C2 CONTROL:** the clean count is 51 and the matched count 17.
- **C3 CONTROL:** fgas_recomputed = Mmol/(Mmol + M*) holds on the clean rows to 1e-6.
- **R0 POWER** (printed before P2): the 16–84% width of μ̄ under the primary prior, in dex, against the 0.53-dex separation of the break-evens at s = 1 (0.62 and 2.11).
- **H1 [HEADLINE, reported]:** the class probabilities at s = 1 under the primary prior with h = 0. The result is "diagnostic" if one class reaches ≥ 68%, and "NON-DIAGNOSTIC" otherwise.

## MUTATE (two pinned controls)

- **MUTATE=1:** every PHIBSS μ is multiplied by 4. The lean-rival probability at s = 1 must fall below 32%.
- **MUTATE=2:** every μ is multiplied by 0.25. The lean-flat probability at s = 1 must fall below 5%.
- Each run exits 0 when it behaves as required.

## Readings (declared)

- **A diagnostic outcome** is a statement about the gas prior: "given PHIBSS-like gas, CFG162's map puts KURVS at …". It is conditional on the prior's selection and on the pressure prescription. It is not an a₀ verdict.
- **A non-diagnostic outcome** means the measured prior is too broad, or too uncertain in its matching, to decide. X is then the result.
- **Untested (declared):**
  - HI (bracketed only);
  - the PHIBSS–KURVS selection difference beyond Variants M and Z;
  - α_CO beyond the bracket;
  - the pressure prescription (only the placed values are used);
  - PHIBSS-2 and Tacconi et al. 2018 (not in the repo).

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
