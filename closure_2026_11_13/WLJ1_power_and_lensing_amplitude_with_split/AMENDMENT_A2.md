# WLJ1 AMENDMENT A2 (2026-11-14; post hoc; committed alone, before the alt polished DES rows and before any grading)

Criteria 03f9823de7; A1 49f8ed445d. Adopts nothing. Footings never pooled.

**Timing, disclosed.** Seen: every halo-model, C4, C5, P4 and HLF1 number; the KL1 / BX1 rows on canonical (all three groups)
and on alt for the Legacy and DES / KiDS-1000 groups. Not yet seen: the alt polished DES rows, every LWB1 / LWB1R row. No
label has been computed.

**What failed as frozen.** KA-G5 / KA-G6 ask that ADOPT reproduce KL1's and BX1's stored rows to 0.01 in gap and chi^2,
"Legacy, DES, KiDS-1000". On alt the DES rows of KL1's frozen scan (group deskids) do not: GATE +2.847 against the stored
+2.822, GATE_BX1 +1.811 against +1.751, GATE_R2 +1.243 against +1.273, GATE_R2b +2.364 against +3.426. Every other row
reproduces: canonical bit for bit (DES included, polished DES included), alt Legacy and C3b to 1e-6 or better, alt KiDS-1000
to 1e-5. On alt the inputs reproduce to about 1e-11 rather than exactly; on DES the frozen scan's ten-parameter L-BFGS-B fit
stops up to about 0.1 in chi^2 above its minimum (KL1 AMENDMENT C3's own diagnosis), so a 1e-11 change at the input moves the
five-point parabola by up to a width. This is the defect for which KL1 replaced DES's frozen scan by the polished scan in the
gate. **As frozen, G-KL1 and G-BX1 are NO VERDICT on alt for every case** (`wlj1_grade_asfrozen.*` reports it first).

**The amendment.** The DES rows of the frozen scan (group deskids) are reported, not gating, in KA-G5 / KA-G6; the gating DES
known answer is the polished scan's (group polish), which is the scan the gate reads. The C0 edges R2 / R2b, which KL1 runs on
the frozen scan, are reported beside the gate and not used for FRAGILE on either footing. Nothing else changes: no gate,
statistic, line, case, other bracket, twin or label rule.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
