# CFG668: the KiDS early-type excess under an independent stellar-mass estimator

**Label as frozen: ARTEFACT EXPLAINS THE EXCESS — but the frozen matching control failed, and the post-hoc fine-bin diagnostic does
not support "explains".** The robust reading: on a morphology-blind raw-lensing test, the early-type excess is significant with
LePhare masses (Z 3.4 as frozen, 2.4 with tight matching) and **not significant with Taylor+11 masses** (Z ≈ 1.7 either way);
the reduction itself is not significant once the matching is tight. The early-type excess is **not a robust tension**, and it is not
shown to vanish.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (2352c8767), 2026-10-12. Block CFG660–669.
- **Settings:** raw lensing; no ΛCDM ingredient (CFG529/531's ε, whose environment term is ΛCDM-built, is not used). The only framework
  statement is morphology-blindness (the law reads baryons only, so early and late types match at equal baryonic mass). κ fitted
  elsewhere, not used here; not "theory closed"; nothing here says the data favour the framework.
- **Scripts:** `cfg668.py` (CFG585's head and CFG531's `esd_loo` executed unedited) → `cfg668.out`, `cfg668_results.json`; MUTATE
  `CFG668_M=M1` (label shuffle) and `M2` (linearity) each exit 1 (both bite). `cfg668_finebin_diag.py` → `cfg668_finebin_diag.json`
  (post hoc, no verdict weight).

## Results (K9 primary; inner band = bins 9–14)

| matching | estimator | A (early/late, log10) | Z | inner A |
|---|---|---|---|---|
| frozen deciles | LePhare (table Mgal) | +0.308 ± 0.090 | +3.41 | +0.276 ± 0.094 |
| frozen deciles | Taylor+11 + per-type gas | **+0.185 ± 0.109** | +1.70 | +0.099 ± 0.089 |
| post-hoc 40 bins | LePhare | +0.249 ± 0.103 | +2.40 | +0.220 ± 0.105 |
| post-hoc 40 bins | Taylor | +0.181 ± 0.109 | +1.66 | +0.097 ± 0.089 |

| difference A_L − A_T (paired jackknife) | K9 | inner |
|---|---|---|
| frozen deciles | +0.122 ± 0.059 | +0.177 ± 0.056 |
| post-hoc 40 bins | +0.068 ± 0.076 | +0.123 ± 0.079 |

- Matching control (frozen: per-bin median log M_b early − late within 0.02 dex): **FAILED**, max 0.161 (L) / 0.125 (T) dex. With 40
  bins the mean offset is +0.005 / +0.003 dex (edge bins still reach 0.18 / 0.09).
- At fixed LePhare mass, early types are +0.084 dex heavier than late types on Taylor masses (log M*_T − log M*_L).
- Frozen rule applied: |A_T| = 0.185 < 2σ_T = 0.218 and Δ = 0.122 ≥ 0.10 → ARTEFACT EXPLAINS. It rests on the failed decile matching.

## Reading

1. **The early-type excess is estimator-dependent and not robust.** It is ≥ 2.4σ with LePhare masses and about 1.7σ with Taylor masses.
   Together with CFG667 (the within-early-type age signal vanishes on Taylor masses), the KiDS "massive old early types exceed the law"
   tension rests on a colour-dependent stellar-mass calibration as much as on lensing.
2. **It is not shown to vanish.** A_T ≈ +0.18 ± 0.11 remains (×1.5 in lensing at matched baryonic mass), consistent with zero at 2σ
   and with the LePhare value at about 1σ. A real early-type excess of that size is still allowed.
3. **What would decide it:** a stellar-mass estimator not based on optical colour (for example near-IR or dynamical masses for a subset),
   or a larger sample. Out of scope here.
4. **For the record's assessment:** the early-type / massive-old tension should carry the caveat "estimator-dependent: ≥ 2.4σ (LePhare)
   vs ~1.7σ (Taylor+11), CFG667/CFG668".
