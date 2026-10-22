# D8b_sigma_universality: does the dwarf HI σ behave like one universal σ_c?

## Verdict: CRISP FINDING

Stilp+2013's 23 dwarfs (200 pc beam) split the tethered-state premise of L* = σ_c²/a0 into two parts. The first part holds and the second fails.

1. **σ is not driven by star formation or mass.** The frozen T1 verdict is **FLOOR FAVOURED**.
   - None of the 4 primary tests is significant at the Bonferroni level, α = 0.0125.
   - σ_m2 vs ⟨Σ_SFR⟩: ρ = +0.474, p = 0.023. This is the closest call.
   - σ_m2 vs M_baryon: ρ = +0.29, p = 0.18.
   - σ_central vs ⟨Σ_SFR⟩: ρ = +0.28. σ_central vs M_baryon: ρ = −0.17.
   - Slope of log σ_m2 vs log Σ_SFR: +0.088, 95 % CI [+0.026, +0.149]. The CI excludes the driven benchmark 1/3, i.e. σ³ ∝ Σ_SFR.
   - A planted b = 1/3 signal is detected in 100 % of noise draws (K3), so the test can see a driven law.
   - Resolution at n = 23: |ρ|_crit = 0.515, and ρ ≥ 0.65 is detectable with 80 % power.
2. **The spread is not measurement noise. It is real, and it tracks the HI gas column.** The frozen T2 verdict is **INTRINSIC SCATTER**.
   - σ_central has the table's own errors (±0.5–0.6 km/s). χ² = 99.3 / 22 (p = 9e-12). The intrinsic scatter is 0.96 km/s (12 %).
   - σ_m2's errors are only assumed (CONDITIONAL, by error transfer). χ² = 133 / 22. The intrinsic scatter is 1.40 km/s (15 %).
   - The L* 84/16 ratio for σ_m2 is 1.995. Under noise alone it would be 1.28 (95 % upper 1.40), with p < 1e-5.
   - So D8's "just under 2" is not one constant blurred by error.
   - The scatter tracks ⟨Σ_HI⟩:
     - σ_m2: ρ = +0.613, p = 0.0024. This is significant even at the secondary Bonferroni-16 level.
     - σ_central: ρ = +0.534, p = 0.0095. This reproduces Stilp's own bold entry, 0.536.
   - The gas column is a property of the local gas. A universal medium constant should not follow it.
3. **If σ_c is a floor (the lower envelope), L* falls below the CFG820 globular floor.** The floor is 23.64 pc canonical and 24.48 pc alt.

| σ statistic | σ (km/s) | L* canonical (pc) | L* alt (pc) |
|---|---|---|---|
| σ_m2 median (D8's number) | 9.30 | 29.9 | 24.8 |
| σ_m2 5th percentile | 7.81 | 21.1 | 17.5 |
| σ_m2 minimum (DDO 125) | 7.00 | 17.0 | 14.1 |
| σ_central median | 7.70 | 20.5 | 17.0 |
| σ_central minimum | 6.00 | 12.5 | 10.3 |

**What it means.** Dwarf σ is not set by star-formation feedback, which is what a floor needs. But it is not one number either:
- it carries about 1 km/s of real scatter;
- that scatter follows the local HI column;
- the reading "σ_c is the floor" puts L* below the globular bound on both footings.

L* ≈ 25–30 pc comes only from taking the **median** of the second moment. That is a typical value, not a demonstrated constant, so this lane **does not strengthen** the conditional L* ≈ 25–30 pc prediction. The prediction survives only if σ_c is a typical value set by the gas column, and then L* depends on environment. That conflicts with CFG820/CFG821, which apply one universal L* to gas-free systems.

## What it does not show

- It does not rule out L* = σ_c²/a0. No action term defines the tethered state, so this lane tests a premise, not a derivation.
- The Σ_HI trend may be partly instrumental. Stilp flag resolution effects that correlate with distance and mass. Here the trend is a secondary variable with no verdict weight under the frozen rules.
- The σ_m2 errors are assumed. The noise-only rejection rests on σ_central, whose errors are tabulated.
- There are 23 galaxies from one survey pair (THINGS + VLA-ANGST). A trend with ρ < 0.5 cannot be excluded.

## Files and checks

- Criteria: `FROZEN_CRITERIA.md`, committed alone (97ec7892fa) before any copy, script or correlation.
- Script: `d8b_sigma_universality.py`, 5/5 PASS, exit 0, about 47 s single thread, < 100 MB.
  - K1: sha256 of all tables.
  - K2: 23/23 exact-name join, and σ identical to D8's rows.
  - K3: planted driven and null controls (power 1.00, false positives 0.014).
  - K4: reproduces Stilp's 8 published σ_central Spearman coefficients, max |Δρ| = 0.017.
  - K5: the noise MC gives a χ² mean of 22.006.
- `D8B_MUTATE=1` replaces σ_m2 with a planted σ ∝ Σ_SFR^(1/3). K2 then fails, the verdict flips to DRIVEN, and the run exits 1.
- A post-run fix, which is not a criteria change: the K4 label parser first matched "SFR / M_HI" as M_HI, so the first run showed K4 FAIL with 7 pairs. Fixing the match order gives 8 pairs, max |Δρ| 0.017. The permutation-null sum was also rewritten to avoid a spurious BLAS warning, and the values did not change.
- Rules: κ = ½ is FITTED. σ is footing-free. Every L* is given on both footings, never pooled. No particle. The theory is not closed.
