# CFG799 ADDENDUM B: stack including the 35 added DBS spectral scans (committed before any statistic on them)

**Why.** CFG799 reduced 55 of the 90 selected observations. The other 35 (DBS and FastDBS spectral scans, 4.23 h of
CFG798 integration) could not be downloaded because the ESA HSA cut the large transfers. They are now downloaded and
reduced with the unchanged `cfg799_fetch.py` (manifest: 90 ok, 0 failed). The frozen selection already lists all four
modes, so nothing about selection, masks, statistic, controls or classes changes. The original CFG799 outputs
(`cfg799.out`, `cfg799_results*.json`, `cfg799_stack.png`, `cfg799_manifest.csv`) stay untouched.

**What was and was not looked at.** Reduction computes per-observation anchor numbers (t_S, anchor correlation). No
spectrum near 541.664 or 541.700 GHz from the 35 added scans was inspected, and no stack statistic exists for them.

**Runs (all with the unchanged `cfg799.py`; sha256 7486117b9e1c8c1e0736e811f606fc58502c311dbc96712fcd06faa840a81488
for the original and for each copy).** The script writes next to itself, so each run uses its own copy in its own
directory.
- **B1, `ADDENDUM_B_full90/`.** All 90 reduced observations. This run sets the class, under the frozen rules and
  addendum A, with no change.
- **B1-MUTATE, same directory.** The frozen MUTATE rule (line of 10 σ_a injected into total power only) must give
  LINE CANDIDATE, or the pipeline is declared blind.
- **B2, `ADDENDUM_B_new35/`.** The 35 added scans alone. They are independent of the 55 already stacked, so B2 tests
  whether anything seen in the first 55 (including the 541.700 GHz hint, z +3.17, classed HINT FADES in CFG802)
  repeats in new data. B2 is **informational**: it sets no class and adds no threshold. It is reported at both
  frequencies with the same estimator and controls.

**Not changed.** Frequencies (541.664 primary, 541.700 secondary, no trials correction), the 5σ rule, masks M1–M4,
Gaussian FWHM 1.14 MHz, degree-3 baseline, χ² inflation, ε conversion and S = 10/50/1000, controls C1–C4, classes,
addendum A tiers. Anything computed beyond B1, B1-MUTATE and B2 is exploratory and will be labelled so.

**Machine note.** The runs go beside live 1024³ simulations on the owner's instruction, at the lowest priority, with
swap watched.

The framework predicts NO line; a null keeps the converter window closed and does not close the theory. κ = ½ is
fitted.

---

## RESULT (2026-10-18; numbers from `ADDENDUM_B_full90/cfg799_results.json` and `ADDENDUM_B_new35/cfg799_results.json`)

**B1, all 90 observations: NULL.** z < 5 at both frequencies, C1–C4 pass, and the frozen MUTATE check bites
(injected line recovered at z +8.87, class LINE CANDIDATE). The framework predicts no line, so this is consistent with
it. It is not a confirmation and not "theory closed".

| | original (55 obs) | B1 (90 obs) |
|---|---|---|
| observations passing the anchor / used | 53 / 49 | 67 / 61 |
| CFG798 integration of used obs | 6.99 h | 8.53 h |
| ν_t 541.664: a ± σ, z | −6.7 ± 7.7 mK, −0.86 | −6.6 ± 5.8 mK, −1.13 |
| ν_t: ε95 at S = 10 / 50 / 1000 | 8.5e-12 / 1.9e-11 / 8.5e-11 | 7.4e-12 / 1.65e-11 / 7.4e-11 |
| ν_t: kill line 1e-12 missed by | ×8.5 / ×19 / ×85 | ×7.4 / ×16.5 / ×74 |
| ν_t: converter window 4e-9 closed by | ×468 / ×209 / ×47 | ×541 / ×242 / ×54 |
| ν_2 541.700: a ± σ, z | +20.5 ± 6.5 mK, +3.17 | +15.3 ± 5.0 mK, +3.04 |
| χ²_ν at ν_t | 2.82 | 2.63 |
| converter-window tier (A_conv, S = 10/50/1000) | EXCLUDED, 48/48 obs | EXCLUDED, 60/60 obs |

- **Little was gained.** 21 of the 35 added scans fail the anchor (the D2 rule: at least 30% of datasets well anchored,
  corr ≥ 0.9): 19 have under 30% well anchored and 2 have none. Their per-LO datasets are short and their Level-1
  correlation is low. Only 14 pass, and 12 contribute spectra, adding 1.54 h to the stack. The stack is still limited
  by baseline structure (χ²_ν 2.6), not by radiometer noise, so the kill line stays out of reach.
- **The 541.700 hint stays a hint.** z +3.04 with REF-only z +3.61 and Level-1 z +0.79. It is carried by the low-IF
  half (z +3.44 vs +0.70, split p 0.114). CFG802 classed the earlier hint HINT FADES (H polarisation only, broad).
  Scan maximum |z| is 4.84 at +38 MHz, none ≥ 5.
- **Anchor rule.** 23 of 90 observations fail it, fewer than half, so the "more than half fail → INCONCLUSIVE" rule
  is not triggered for B1.

**B2, the 35 added scans alone (informational): INCONCLUSIVE.** Only 14 of 35 pass the anchor, so C4 fails (a control
fails). Numbers are reported anyway: 12 observations used, 1.54 h.
- ν_t: a = −6.4 ± 9.0 mK, z −0.71; ν_2: a = +8.7 ± 7.8 mK, z +1.12.
- At σ = 7.8 mK the earlier hint amplitude (+15 to +20 mK) would give z of about +2.0 to +2.6. The observed +1.1 neither
  replicates the hint nor refutes it: power is too low.
- Exploratory, not a class criterion: the REF-only total power at ν_t is negative (z −3.72 in B2, −2.99 in B1; the
  original was −0.93). A mirror line would be positive. With χ²_ν 2.5 this reads as baseline structure and was not
  investigated further.

**Remaining gaps.** 5 LoadChop/raster observations stay excluded by the frozen mode rule, and 2 of the original 55
(1342192348, 1342192349) still fail the anchor. Nothing else is left to download.

External numbers stay provisional (sideband gain 0.5, load coupling 1, WBS response, S). κ = ½ is fitted.
