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
