# CFG669: on near-IR masses the age signal fades, the early-type excess stays

**Labels as frozen:** T1 (age signal, Ks) **PARTIAL**; T2 (early-type excess, Ks) **EXCESS PERSISTS**; combined **NOT ROBUST**
(because T1 falls below 2σ on Ks). **Reading:** the KiDS old-vs-young age signal exists only with LePhare masses; the early-vs-late
excess at matched baryonic mass is real on the least colour-dependent estimator. This corrects CFG668's tentative softening, which
came from the optical colour–M/L estimator.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (c42424774), 2026-10-12. Last number of block CFG660–669.
- **Settings:** raw lensing; no ΛCDM ingredient; CFG529/531's ε not used; the only framework statement is morphology-blindness. Not
  "theory closed"; nothing here says the data favour the framework.
- **Script:** `cfg669.py` (CFG585's head and CFG531's `esd_loo` executed unedited) → `cfg669.out`, `cfg669_results.json`. MUTATE
  `CFG669_M=M1` (label shuffle) and `M2` (linearity) each exit 1 (both bite).
- Ks masses: log M*_K = 0.4(5.08 − MAG_ABS_Ks) + c_K, c_K = −0.3528 (global, matching the LePhare median over f30 lenses; it changes
  no ranking).

## Results (K9; patch jackknife; the three estimators recomputed on one common finite sample)

| estimator | T1 age: OLD/YOUNG (early) | T2 early/late at matched M_b | T2 matching: mean / max offset |
|---|---|---|---|
| LePhare (SED fit) | +0.186 ± 0.081 (Z 2.29) | +0.249 ± 0.103 (Z 2.40) | +0.005 / 0.181 dex |
| Taylor+11 (optical colour–M/L) | +0.036 ± 0.077 (Z 0.46) | +0.181 ± 0.109 (Z 1.66) | +0.003 / 0.095 |
| **Ks light (constant M/L_K)** | **+0.082 ± 0.089 (Z 0.93)** | **+0.280 ± 0.083 (Z 3.37)** | **+0.001 / 0.044** |

- Median log M*_X − log M*_L: OLD − YOUNG +0.078 (Taylor), +0.026 (Ks); early − late +0.084 (Taylor), **−0.060 (Ks)**.
- Inner band (bins 9–14), T2: LePhare +0.220, Taylor +0.097, Ks +0.281.

## Reading

1. **The age signal is not robust.** It is 2.3σ with LePhare and below 1σ with both Taylor and Ks masses. CFG700's AGE SIGNAL and the
   ACE motivation should be treated as estimator artefacts until shown otherwise (CFG667 + this lane).
2. **The early-type excess is robust on near-IR masses.** Matched in Ks-based baryonic mass, early types carry ×1.9 the lensing of late
   types (+0.280, Z 3.4), with the tightest matching of the three estimators. Optical colour–M/L (Taylor) is the outlier: it assigns red
   galaxies higher M/L than near-IR light implies. The law's morphology-blindness is **in tension** with this at the ~3σ level on raw
   lensing, which is the record's existing early-type tension, now checked against estimator choice.
3. **Caveat that cuts against the excess:** a constant M/L_K ignores that older populations have somewhat higher near-IR M/L. If early
   types' true M/L_K is ~0.1–0.15 dex higher, matching on true mass would lower the excess, plausibly by ~0.05–0.15, leaving it positive.
   An age-aware near-IR M/L or dynamical masses would sharpen this.
4. **CFG668's reading is superseded:** the "not significant on Taylor masses" result reflects the optical estimator, not the tension
   disappearing.
