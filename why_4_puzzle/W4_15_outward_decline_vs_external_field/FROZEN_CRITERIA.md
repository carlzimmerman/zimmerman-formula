# W4-15: does the outward a₀ decline follow the external field? (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-15 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
Observational lane (`obs`). **κ = ½ is FITTED.** Not theory closed.

## Question

W4-14 found that, inside SPARC galaxies, the inferred a₀ falls outward. Gas and star points agree at matched g_bar (−0.10 ± 0.11),
while the within-galaxy gap is −0.44 ± 0.06. One candidate cause is an external-field effect (EFE): a galaxy in a stronger external
field loses more of its boost at low internal acceleration. **Does the outward decline correlate with the galaxy's external
field, estimated independently from its environment?**

## Data (on disk, read only)

- SPARC rotmod and master table, via CFG4_common.
- Chae+2021 environmental external-field amplitudes: `real_research/reviews/directional_efe_2026/laneB_data/chae21_env.csv`
  (tracked; 109 SPARC galaxies). log e_N under two clustering assumptions: maxclu (PRIMARY) and noclu (secondary).

## Statistic (fixed)

- **Sample:** SPARC Q ≤ 2 and i ≥ 30°, matched by name to Chae's table, with at least 8 valid points (g_obs > g_bar > 0;
  Υ_d 0.5, Υ_b 0.7).
- **Per galaxy:** the weighted least-squares slope s of log a₀,ᵢ against log g_bar (simple μ: a₀,ᵢ = g_obs(g_obs − g_bar)/g_bar).
  The weights are 1/σ², with σ_log a₀ ≈ (dln a₀/dln g_obs) σ_log g and σ_log g = 2e_V/(V ln 10).
  - s > 0 means a₀ is lower at lower g_bar, i.e. it falls outward.
  - Also reported: the sample's mean s (the outward decline itself) and the RAR-inversion cross-check.
- **PRIMARY test:** Spearman ρ(s, log e_N,maxclu), with a permutation p-value (10 000 shuffles, seed 64, two-sided). The EFE
  predicts ρ > 0.
- **Secondary:**
  - the same test with log e_N,noclu;
  - the median-split difference in s (high-e_N half minus low-e_N half) with a bootstrap σ;
  - nuisance correlations of s with gas fraction (MHI / (MHI + 0.5 L36)) and log SBdisk, reported only.

## Verdict (frozen)

- **EFE-CONSISTENT:** ρ > 0 with p < 0.0027 on the PRIMARY.
- **NO EFE SIGNAL:** p > 0.05 on the PRIMARY. This must be read with the power from control M1. If M1 shows the test would detect
  ρ ≈ 0.3, the null disfavours an EFE origin at that strength.
- **INTERMEDIATE:** otherwise.

**Hand expectation (disclosed):** uncertain. Chae et al. report EFE signatures in SPARC outer rotation curves, which would give
ρ > 0. With about 100 galaxies and noisy slopes, the power may be modest.

## Controls (`W4_15_MUTATE=1`, separate outputs, exit 1 when both bite)

- **M1, power.** Plant s' = s + β(log e_N − mean), with β chosen so that ρ(s', log e_N) ≈ 0.3 by construction:
  β = 0.3 std(s)/std(log e_N). The PRIMARY must then reach p < 0.0027 or at least p < 0.05. Report which; it is the test's
  power at ρ ≈ 0.3.
- **M2, shuffle e_N across galaxies** (seed 64). p must be above 0.05.

## Register

One `obs` row, then `kappa_campaign_lee.py` rerun. Nothing downloaded.
