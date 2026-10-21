# W4-15: does the outward a₀ decline follow the external field? INTERMEDIATE, opposite sign to an EFE origin

**Bottom line.** W4-14 found that the inferred a₀ falls outward inside SPARC galaxies. If an external-field effect caused it,
galaxies in stronger environmental fields would decline more, giving ρ > 0. They decline **less**:

- **ρ(s, log e_N) = −0.250, p = 0.030** (Chae+2021 maxclu, 76 galaxies). The noclu variant gives −0.260 (p = 0.024).
- The median-split difference in slope, high minus low e_N, is −0.55 ± 0.14.
- The frozen verdict is **INTERMEDIATE**: ρ < 0 at p = 0.03, neither EFE-consistent (needs ρ > 0) nor a clean null.
- The sign is opposite to the EFE prediction. The post-hoc power check (below) shows a true EFE-driven ρ ≈ +0.3 would sit about
  4.7σ above what is observed.

So the outward decline does **not** look like an environmental EFE. What it is stays open. It does not track gas fraction
(ρ −0.04) or disc surface brightness (+0.01). Remaining candidates are outskirts kinematics (warps, non-circular motions,
pressure support), a radial M/L gradient, or the deep-regime slope. **κ = ½ is FITTED.** Not theory closed.

## Numbers (`w4_15.out`)

- **Sample:** 76 SPARC galaxies (Q ≤ 2, i ≥ 30°, at least 8 valid points, present in Chae's table).
- **The decline itself:** mean d log a₀/d log g_bar = +0.096, median +0.115 (positive means a₀ falls outward); RAR cross-check
  median +0.128.
- **Correlations:** PRIMARY ρ −0.250 (p 0.0298); noclu ρ −0.260 (p 0.0240). Nuisance: gas fraction −0.039, log SBdisk +0.011.

## Controls

- **M2 (e_N shuffled):** p = 0.066. Null as expected.
- **M1 (planted ρ ≈ 0.3, as frozen): FAILED** (`w4_15_MUTATE.out`, exit 2). My recipe added β(log e_N − mean) to the real
  slopes, which already anti-correlate with e_N. The plant only offset that, reaching ρ = +0.07 instead of +0.3. This is a
  control-design flaw and is reported as such.
- **Post-hoc power check** (`w4_15_posthoc_power.py`, `.out`; **no verdict weight**): the same recipe on a shuffled
  (uncorrelated) baseline, 200 realisations. Median achieved ρ +0.299; detected at p < 0.05 in 76% and at 3σ in 35%. The test
  has moderate power at ρ ≈ 0.3, and the observed −0.25 lies well below that.

## Files

`FROZEN_CRITERIA.md` (5bc61b902), `w4_15.py` (numpy/scipy, seconds), `w4_15.out` / `_results.json`, `w4_15_MUTATE.out` /
`_results_MUTATE.json`, `w4_15_posthoc_power.py` / `.out`.

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_15_outward_decline_vs_external_field/w4_15.py > why_4_puzzle/W4_15_outward_decline_vs_external_field/w4_15.out

Chae+2021's environmental e_N were recovered by an earlier lane (`real_research/reviews/directional_efe_2026/laneB_data`,
tracked) and are read only here. Nothing was downloaded.
