# W4-16: what drives the outward a₀ decline inside galaxies? (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-16 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
Observational lane (`obs`). **κ = ½ is FITTED.** Not theory closed.

## Question

Inside SPARC galaxies the inferred a₀ falls outward. The W4-15 mean slope is d log a₀/d log g_bar = +0.10, and the effect is the
−0.44 dex within-galaxy gap of W4-14. It is not baryon type (W4-14), not the law's transition shape (W4-13), and not an
environmental external field (W4-15, wrong sign). **Which galaxy property does it track?** Each candidate mechanism predicts its
own signature.

## Sample and slope (fixed; as W4-15, without the Chae requirement)

- **Sample:** SPARC Q ≤ 2 and i ≥ 30°, with at least 8 valid points (g_obs > g_bar > 0; Υ_d 0.5, Υ_b 0.7).
- **s:** the WLS slope of log a₀,ᵢ against log g_bar (simple μ), with W4-15's weights.
- **s_gas:** the same slope using only gas-dominated points (V_gas|V_gas| ≥ 0.7 V_bar²), for galaxies with at least 5 of them.
  It is immune to stellar M/L.

## Mechanisms and their declared signatures

| id | mechanism | signature (the test) |
|---|---|---|
| D1 | pressure support / asymmetric drift in outer gas (V_obs < V_circ) | ρ(s, log V_flat) < 0: stronger decline in slow galaxies |
| D2 | radial stellar M/L gradient (inner Υ above the constant assumed) | the decline vanishes for gas-dominated points: the median s_gas is consistent with 0, while the median s is > 0 |
| D3 | beam smearing (inner velocities suppressed) | ρ(s, log D) ≠ 0. Smearing lowers inner a₀, so it predicts ρ < 0 and an outward **rise** at large D |
| D4 | warps / inclination errors | ρ(s, i) ≠ 0 |
| D5 | data quality | the median s differs between Q = 1 and Q = 2 (Mann–Whitney) |
| D6 | a universal deep-regime slope (true g ∝ g_N^β, β ≠ ½) | no significant correlation with D1, D3, D4 or D5, and s_gas ≈ s; then β ≈ (1 + s)/2. The record's BTFR slope (b = 1.004 ± 0.011) bounds a global β. |

- **Statistics:** Spearman ρ with a permutation p (10 000, seed 64) for D1, D3 and D4. Mann–Whitney for D5. For D2, the medians
  of s and s_gas with galaxy-bootstrap σ (2000, seed 64).
- **Significance:** Bonferroni over the five correlation-type tests, p < 0.01.
- **Υ robustness:** the median s at Υ_d 0.3, 0.5 and 0.8, reported.

## Verdict (frozen)

- **ATTRIBUTED to Dk:** exactly one mechanism's signature is met at p < 0.01, in the declared direction.
- **MIXED:** more than one is met.
- **D6 (UNIVERSAL SLOPE) LIKELY:** none is met, and s_gas ≈ s (within 2σ, both > 0). β is reported against the BTFR bound.
- **UNRESOLVED:** otherwise.

**Hand expectation (disclosed):** D1 or MIXED. Gas-rich dwarfs carry pressure support, and W4-15 found no gas-fraction trend
(ρ −0.04), which already argues against D2.

## Controls (`W4_16_MUTATE=1`, separate outputs, exit 1 when both bite)

- **M1, planted pressure-support world.** Reduce each galaxy's V_obs at points with R > R_disk by σ²/V with σ = 10 km/s
  (V'² = V² − 2σ²). D1's signature must then be met (ρ < 0, p < 0.01).
- **M2, planted radial M/L gradient.** Raise inner stellar terms by ×(1 + (R_disk/R)^{0.5}) in the data. The median s must change
  while the median s_gas does not (within 1σ). This shows D2's discriminator works.

## Register

One `obs` row, then `kappa_campaign_lee.py` rerun. Nothing downloaded.
