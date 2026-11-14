# WLJ1 AMENDMENT A1 (2026-11-13; post hoc; committed alone, before RESULT.md)

Criteria 03f9823de7. Adopts nothing. Footings never pooled.

**Timing, disclosed.** Written after the halo-model part (`wlj1_hm.py`) and the C4 part (`wlj1_c4.py`) ran, while the shear,
KL1 / BX1 and LWB parts were running. Seen: every ratio of section 1 for every case, and every C4 number.

**What failed as frozen.** KA-R (criteria section 4) asks that REF give "r_eff = 1 exactly" in C4. On canonical REF gives
r_eff = 1.0000000000000002, that is 1 + 2.2e-16 (one unit in the last place of a double): S(L) for R = 1 is a ratio of two
sums of the same terms, computed in a different order. On alt it gives exactly 1. **As frozen, gate G-C4 is NO VERDICT on
canonical for every case, so the CO1 gate, the HLF1 gate and the row-24 word are NO VERDICT on canonical as frozen.**
RESULT.md reports that reading first (`wlj1_grade_asfrozen.json/.out`).

**The amendment.** KA-R in C4 reads |r_eff - 1| <= 1e-12 (floating-point rounding; the gate's own line is 0.0481). The C5 part
of KA-R is unchanged (REF there gives d_cold = 0 exactly or it fails). Nothing else changes: no gate, statistic, line, case,
bracket, twin or label rule.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
