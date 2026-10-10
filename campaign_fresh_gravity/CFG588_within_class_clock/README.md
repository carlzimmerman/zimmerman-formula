# CFG588: ACE within-class colour clock. SPLIT as frozen (a hair's-breadth threshold case): a real within-class clock, strong in early types, weak in late types

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (23fd031bc). Model: `../MODEL_accumulating_cold_energy_2026-10-10.md`.
- **Script:** `cfg588_within.py` → `cfg588_within.out`, `cfg588_results.json`; MUTATE `CFG588_MUTATE=1` → `_MUTATE`.
- **Machinery:** cfg585_age.py's head executed unedited (CFG531 estimator, CFG529 validated environment).
- κ = ½ fitted; footings never pooled; cold energy's mass still required; not theory closed.

## Groups (colour-residual tertiles inside each class, at that class's mass quintiles)
| class | tertile | N | median δc | median log M* | ε K9 (A canonical) |
|---|---|---|---|---|---|
| early | blue | 8,850 | −0.174 | 10.800 | +0.26 |
| early | mid | 8,879 | −0.001 | 10.800 | +0.72 |
| early | red | 8,843 | +0.080 | 10.800 | +1.20 |
| late | blue | 10,211 | −0.183 | 10.524 | −0.27 |
| late | mid | 10,287 | +0.000 | 10.634 | −0.38 |
| late | red | 10,195 | +0.167 | 10.542 | +0.07 |

## Result (K9 primary; separate class intercepts; joint jackknife covariance)
| cell | common slope b (Z) | b_early (Z) | b_late (Z) | slope difference | call |
|---|---|---|---|---|---|
| A canonical | +2.05 ± 0.68 (+3.01) | +3.36 ± 1.27 (+2.6) | +1.05 ± 1.06 (+0.995) | 1.23σ | EARLY-ONLY CLOCK |
| A alt | +1.87 ± 0.62 (+3.02) | +3.08 ± 1.16 (+2.7) | +0.97 ± 0.97 (+0.999) | 1.22σ | EARLY-ONLY CLOCK |
| B canonical | +2.04 ± 0.68 (+3.01) | +3.35 ± 1.27 (+2.6) | +1.05 ± 1.06 (+0.999) | 1.22σ | EARLY-ONLY CLOCK |
| B alt | +1.87 ± 0.62 (+3.02) | +3.06 ± 1.16 (+2.6) | +0.97 ± 0.97 (+1.003) | 1.22σ | CLOCK IN BOTH CLASSES |

- **Verdict as frozen: SPLIT.** The late-type slope sits at Z = 0.995–1.003 against the frozen threshold Z ≥ 1, so the call
  flips on the third decimal. Read it as: a common within-class clock at Z = 3.0, clearly present in early types, positive
  but not significant in late types, with slopes consistent at 1.2σ.
- K-in (reported): common slope +1.6–1.7 (Z +1.68), same pattern.
- Controls: C1 early tertiles matched exactly (spread 0.000 dex); **C1 FAILS for late types (spread 0.110 dex: the middle
  tertile is heavier)**, so the late-type pattern is mass-confounded; C2 reproduces CFG585 exactly (+1.197 / +0.256).
- MUTATE (δc shuffled within class × mass): common slope Z +0.35 in every cell, NO CLOCK — the within-class colour signal is
  real, not an artefact of the binning.

## Reading (not a verdict)
- A colour clock exists INSIDE the classes (Z = 3.0, no class step can produce it): at fixed mass and class, redder galaxies
  carry more excess. This is ACE's core signature, now beyond the old/young pair of CFG585/586.
- It is strong in early types and weak in late types (whose test is also mass-confounded). ACE's "same clock in both
  classes" is consistent (1.2σ) but not established; a late-type test with matched mass is the open piece.
- Colour still also tracks dust, metallicity and M/L; the excess needs ≈ 2× mass between groups ≈ 0.25 mag apart, beyond
  plausible M/L slopes.
