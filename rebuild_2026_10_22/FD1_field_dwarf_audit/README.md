# FD1_field_dwarf_audit: the on-disk data close about half of IC 1613's gap, not all; IC 1613 STANDS

Criteria: `FROZEN_CRITERIA.md` (44fd23a71c). Amendment A1 (ae0b838549, pre-result): HO3's actual error column and
X51's binary correction. Both were committed alone before any number.

κ = ½ FITTED. Footings never pooled. Cold dark energy is not matter and not a particle. Not "theory closed". Nothing here
says the data favour the framework.

**HG2's sign is parked** as an open, underpowered tension (DS1, GA1, DY1).

## Verdict (frozen): **IC 1613 STANDS** on both footings; **FIELD FAILS (law)**: S1, S2, S3

| run (13 LG field dwarfs, law branch) | IC 1613 E (Z), canonical | alt | field S1 / S2 / S3 (canonical) |
|---|---|---|---|
| Step 0 (X1 inputs = HO3) | −0.535 (−6.75) | −0.572 (−7.46) | HO3: fails S1, S3 |
| **PRIMARY: M★ from K + HI gas + rotation** | **−0.305 (−3.85)** | −0.343 (−4.47) | **fail / fail / fail** |
| M only (M★ = 0.6 L_K) | −0.303 (−3.82) | −0.341 (−4.45) | fail / fail / fail |
| G only (1.33 M_HI) | −0.618 (−7.80) | −0.654 (−8.52) | ok / fail / fail |
| K only (UNGC vAmp) | −0.364 (−4.59) | −0.401 (−5.23) | fail / fail / fail |
| M + G | −0.477 (−6.01) | −0.514 (−6.70) | fail / **ok** / fail |
| PRIMARY, Υ_K 0.5 / 0.8 | −0.286 / −0.340 | −0.324 / −0.378 | fail |

**"REDUCED" was missed narrowly.** That class needed |Z| ≤ 3.38 and IC 1613 reached 3.85, so the frozen class is STANDS.

## What the audit shows

**IC 1613's gap is about half a data issue.**
- UNGC's K-band light gives log M★ 7.85 (Υ_K 0.6), against X1's 8.28. That alone removes 0.23 of the 0.54 dex
  over-prediction.
- Counting the HI gas works the other way (+0.08 dex).
- The rotation term (vAmp 13 km/s) adds +0.06.
- About 0.3 dex remains: the law still predicts twice IC 1613's pull.

**The audit's rotation term is too crude to grade the field.** UNGC vAmp is the *outer* HI rotation amplitude, not the
rotation at r₁₂. Adding it in full over-corrects the strong rotators:
- NGC 6822 moves from about −0.05 to +0.56 (Z +9.0, vAmp 64 km/s);
- Phoenix and Leo A move apart in the other direction.

A fair rotation term needs each dwarf's rotation curve at r₁₂, which is not on disk (LITTLE THINGS, for example). The
field verdict is therefore a statement about these on-disk inputs, not about the law.

**Stated, not graded:**
- IC 1613's input mass is the largest single lever. X1's 1.9e8 M☉ against K-band 7e7 M☉ is a 2.7× disagreement between
  two published values.
- A fair test of IC 1613 needs:
  - a resolved stellar-mass estimate (CMD or SED);
  - its HI rotation curve at r₁₂.

  Neither is on disk, and fetching them needs the owner's approval.

## Checks: 5/5

- **K0 (both footings):** Step 0 reproduces HO3's E for all 13 to 0.0000; IC 1613 matches −0.5352 / −0.5725.
- **K1:** names matched through BS1's map. Antlia B has no UNGC row, so its X1 values are kept (disclosed).
- **K2:** peak RSS 0.27 GB.
- **Rerun:** the results JSON is byte-identical (`95b52ca2…62ad`).
- **MUTATE twin** (`FD1_MUTATE=1`): K0 fails against the ×1.1 target and the run exits 1.
  - Disclosed: after printing that failure, the twin stops on a math-domain error, because the flipped rotation term
    makes 3σ² − v_rot² negative for NGC 6822. So it writes no `_MUTATE` files.
