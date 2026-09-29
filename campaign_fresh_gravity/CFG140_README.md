# CFG140 — a₀ at z ≈ 1.5 from KURVS-CDFS's outermost measured rotation points: flat a₀ against a₀ ∝ H(z)

- **Criteria:** frozen in `CFG140_FROZEN_CRITERIA.md` (28dca75b8), with a pre-run C2 correction (49baf209f), before any acceleration number.
- **Script:** `CFG140_kurvs_a0z.py`, under a second.
- **Runs:**
  - The main run passes 11 of 12 and exits 0. The one miss is the reported H2 verdict.
  - The MUTATE run (every KURVS velocity × 2) fails H1 in all 48 cells and exits 1.
  - The two runs differ on H1, so the control is informative.

## Bottom line

**NON-DIAGNOSTIC over the declared brackets. The answer turns on one unmeasured quantity: the pressure support at the outermost radius.**

The sample is in the right regime. At the last measured point (R_max = 9–13 kpc, 4–7 disc scale lengths, median z = 1.53), the 10 rotation-supported discs sit at g_bar/a₀ = 0.06–0.67 for the paper's own gas fraction. The test has statistical power: flat a₀ and a₀ ∝ H(z) (E = 2.4) are separated by 3.1–5.1σ in every cell before the systematics. But the two pressure-support treatments give opposite answers:

| pressure support at R_max | a₀ ∝ H(z), the rival | flat a₀, the framework |
|---|---|---|
| **none: V_c = V_obs** (a strict lower bound on the circular speed) | **over-predicts in all 24 cells**, −3.2σ to −9.6σ | disfavoured in 0 of 24; it also over-predicts once the assumed gas is large |
| **Burkert constant-σ drift: V_c² = V² + 2σ₀²R/R_d** (large at 4–7 R_d) | disfavoured in 0 of 24 | **under-predicts in 21 of 24 cells** |

- **What each reading requires:** the rival survives only if the outer pressure support is close to the full constant-σ correction; flat a₀ survives only if it is small. The anchor-corrected central cell (μ = 0.67, P1) gives Δ′_flat = +0.40 ± 0.07 and Δ′_H = +0.24 ± 0.07.
- **The z ≈ 0.85 KROSS control** (390 discs, same pipeline) points to over-correction in P1.
  - With no correction, the KURVS − KROSS differential is +0.017 ± 0.058 dex. Flat predicts 0 and the rival +0.083, so both are consistent.
  - With the Burkert correction the differential is +0.27 ± 0.07, about 2.7σ beyond even the rival's +0.08. The constant-σ correction at KURVS's larger R/R_d manufactures an "evolution" neither reading predicts.
  - That is a caution on P1, not a verdict.

## The numbers (anchor-corrected by the SPARC same-pipeline z = 0 anchor; canonical, δ = 0)

| gas μ = M_gas/M* | P0: Δ′_flat | P0: Δ′_H | P1: Δ′_flat | P1: Δ′_H |
|---|---|---|---|---|
| 0.25 | −0.070 ± 0.057 | −0.222 | +0.459 ± 0.071 | +0.302 |
| 0.67 (the paper's 40% molecular) | −0.130 ± 0.057 | −0.279 | +0.398 ± 0.070 | +0.244 |
| 1.5 | −0.222 ± 0.057 | −0.365 | +0.307 ± 0.070 | +0.158 |
| 4 (stacked HI at z ≈ 1) | −0.400 ± 0.057 | −0.530 | +0.133 ± 0.070 | −0.004 |

The alt footing moves these by 0.01 or less; the δ = ±0.2 dex stellar-mass bracket is in the JSON.

- **Per galaxy** (central cell, P1, unanchored): Δ_flat from +0.23 to +0.88 and Δ_H from +0.09 to +0.73. At μ = 0.67, g_bar/a₀ at R_max runs from 0.06 to 0.67.
- **Variants** (P1 central cell, unanchored):
  - all 19 of the 22 with v/σ₀ ≥ 1: Δ_flat +0.53;
  - the paper's model-extrapolated velocities at 6 R_d: Δ_flat +0.54.
- **The gas bracket alone** spans about 0.33 dex even at z = 0. SPARC run with μ = 0.25 → 4 in place of its measured gas gives Δ from +0.10 to −0.23 (R6).

## Controls

- **C1:** the SPARC anchor (75 galaxies, Q ≤ 2, i ≥ 30°, log M* ≥ 9.5, last rotmod point, measured gas, same pipeline) has median Δ_flat = +0.064 dex (pooled +0.092 ± 0.013). That is the simplified pipeline's own z = 0 offset, and every KURVS number above is corrected by it cell by cell.
- **C2:** ν_mono's limits hold to 5 × 10⁻⁷ and 1.5 × 10⁻¹².
- **C3:** the 10 selected galaxies are exactly the paper's rotation-supported (f_DM) rows.
- **MUTATE:** with the velocities doubled, flat a₀ is disfavoured in all 48 cells and H1 fails.

## What is data and what is assumption

- **Measured:** the inclination-corrected rotation velocity at the last observed point, and its radius (KURVS Table column 3; see `data_assembly/arxiv_tables/KURVS_DEFINITIONS_NOTE.md`). Also σ₀, R_eff, z and MAGPHYS stellar masses (±0.2 dex).
- **Assumed:**
  - the gas: unmeasured, so the bracket μ = 0.25–4;
  - the pressure support: P0 and P1;
  - the baryon geometry: thin exponential discs, gas at 2 R_d, spherical shortcut;
  - g_obs = V²/R, a spherical surrogate;
  - the inclination error: a declared ±5°.
- **What would settle it:**
  - a measured outer dispersion profile, or a pressure-free tracer (CO or HI kinematics with V/σ > 5) at R_max;
  - a measured cold-gas mass.
  - With those, the test has 3–5σ statistical power, subject to CFG52's correlated mass-scale floor of about 2.3σ against a₀ ∝ H(z).
  - The COSMOS half of KURVS (21 galaxies, forthcoming) would add sample.

## Disclosures

- **C2 was corrected before any run** (49baf209f). The frozen tolerance ignored ν_mono's sub-leading terms.
- **SPARC's data rows are parsed by whitespace field order.** The file's header byte columns do not match its rows. This was found and fixed in development, before any lane number.

## Reading

- **KURVS-CDFS is the first on-disk sample in the decisive regime (g_bar < a₀ at z ≈ 1.5), and it cannot yet decide.**
- **The one robust statement is conditional.** If the outer pressure support is small, a₀ ∝ H(z) over-predicts the outer rotation at every gas and stellar-mass bracket. Flat a₀ then fits only if the gas is modest.
- **B's decisive a₀(z) test therefore waits on the dispersion profile and the gas,** not on more galaxies of this kind.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## Correction (appended 2026-09-29; the text above is unchanged)

- CFG140 correction (logic; the orchestrator's check). The observed velocity is a lower bound on the circular speed, because pressure support only raises V_c. A lower bound can exclude only a model that predicts V_c below V_obs. Under P0 both readings predict at or above the observed accelerations in every cell (the largest P0 Δ′ is −0.035 for flat and −0.196 for the rival), so the bound excludes neither. The P0 rows are the NO-PRESSURE-SUPPORT SCENARIO (V_c = V_obs), not a bound in the excluding direction. 'a₀ ∝ H(z) over-predicts in all 24 cells' holds only if the outer pressure support is zero; it means the rival needs substantial outer pressure support to survive. 'Flat a₀ under-predicts in 21 of 24 cells' holds only in the constant-σ Burkert scenario (P1); it means flat a₀ needs the outer pressure support well below that level. Neither reading is excluded by the data alone. The frozen verdict (NON-DIAGNOSTIC), the anchor, the KROSS control, the power row and the MUTATE are unchanged.
- In the table and the Reading above, read '(a strict lower bound on the circular speed)' as 'the no-pressure-support scenario'. 'The one robust statement' is a statement about that scenario only.
