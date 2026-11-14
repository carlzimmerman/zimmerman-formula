# EUC20 (MASK-APERTURE STELLAR MASS, THIRD RE-READ: THE GRADE-B LANES): FROZEN CRITERIA

Committed alone, 2026-11-14, while the grade-B mask fetch (`closure_2026_11_14/EUC19_grade_b_mask_table`) is still
running. Its table has not been opened: no mask radius of it has been read, no in-mask share and no corrected
number computed. No EUC20 script exists.

κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s², graded separately, never pooled. Not "theory
closed". A re-read: it adopts nothing, edits no ledger or scorecard, and no outcome is a pass of the lensing gate.

## 0. What this lane is

EUC17 and EUC18 re-read the Euclid lens rows on sample P and on the wide grade-B lenses with the catalogue's
stellar mass placed inside the modelling circle. They could not grade the lanes that use the other grade-B lenses,
because those lenses had no mask record. The owner's go of 2026-11-14 ("fetch the rest of the grade-B masks too",
then "re-read the grade-B lanes when the fetch lands") opens them. This lane re-reads them.

## 1. Method (frozen)

**The correction** is EUC17's primary share, unchanged: `f = M2D_frac(mask_radius, eclipse_effective_radius,
eclipse_sersic_index)`, `lm_corr = lm − log₁₀ f`, mass errors as catalogued. Masks from EUC17's table and EUC19's
table together.

**A lens without a mask record keeps its catalogued mass** (the less generous choice). Counts are reported. A row
is NOT EVALUABLE if more than 5 % of the lenses it grades have no mask.

**Routes.**
- *Own code, wrapped loader* (EUC18's method): the source lane's committed script runs unmodified with EUC1's
  loader wrapped; its writes are redirected into this lane's folder. Used for EUC8 and EUC5 (amendment A1 route).
- *Own code, one substitution*: LNJ1 reads the catalogue itself. Its source text is executed under its own path
  with one exact substitution, which must match exactly once: the expression that parses
  `eclipse_log_survived_mass_med` gets `− log₁₀ f` of that lens. Nothing else is changed.
- *Exact shift* (EUC17's method): EUC4's bins, `b` computed at full precision with EUC1's and EUC4's imported code,
  `b_corr = b + log₁₀ f`.

## 2. Rows, words and labels

| Row | Source rule, unchanged | Committed (canonical / alt) |
|---|---|---|
| **G1** EUC4 secondary bin: grade B, 1.3″ ≤ θ_E < 1.7″ (292), source at infinity, f₂₅ | WIDE LENSES BREAK THE CEILING (lower ≥ 0.25) / NOT CONFIRMED (upper ≤ 0.10) / NO VERDICT, labelled secondary | BREAK / BREAK |
| **G2** EUC8 lane word, with its family words | EUC8 criteria Part B (SLOPE NOT CONSTRAINED, RESIDUAL MUST BE CONCENTRATED, RESIDUAL MUST BE EXTENDED, SLOPE BRACKETED, NO FAMILY FITS) | SLOPE NOT CONSTRAINED / SLOPE NOT CONSTRAINED |
| **G3** LNJ1 word | LNJ1's rule before its known-answer gate (its "primary raw" word and bracket words) | NO POWER, FRAGILE / NO POWER |

**Labels, per row and footing:** the word under the corrected mass; UNCHANGED or CHANGED; FRAGILE if bracket F1a
(R_e × 0.80 in f) or F1b (R_e × 1.25) gives a different word, otherwise ROBUST. (For G3, LNJ1's own FRAGILE tag is
part of its word and is compared as such.)

**Meaning.** UNCHANGED on a failing row: the fail survives the correction. CHANGED toward the law: a hit awaiting a
blind re-grade, never a pass. G2 grades how concentrated the missing mass must be, on dispersions whose scale was
set post hoc in EUC5; EUC8 says every word of its Part B inherits that.

**Reported, no word.**
- EUC4's complement bin (grade B, θ_E < 1.0″, 2,045), committed NO VERDICT / NOT CONFIRMED, with its would-be word.
- EUC8 Part A: the missing share and excess mass of every Einstein-radius class, far and central source cases.
- EUC5 under A1: b_dyn by class and the dynamics-minus-lensing difference. Its word is NOT EVALUABLE on its
  dispersion-recovery gate, which the mass does not enter; that word cannot change here.
- EUC6: its pairs were matched at catalogue mass and its word uses only the paired richness, so a mass correction
  cannot move the word without a new control set (a new neighbour-count download, not asked for). Reported instead:
  the median difference in corrected log mass between each wide lens and its control, and the richness that
  difference would be worth on the controls' own richness–mass slope. If that is a large part of EUC6's excess
  (+3.38 galaxies), the RESULT must say EUC6 needs a re-matched control set.

## 3. Checks (frozen)

Per source lane; a failure makes that lane's rows and readings NOT EVALUABLE and leaves the others standing.

- **H0 harness.** With f = 1 the route reproduces the source lane's committed output files byte for byte, logs on
  every line that carries no elapsed time. (EUC4 bins: every committed bin statistic to 1e-9, bounds to 0.01, words
  identical.)
- **H1 source folders untouched** in git after every run.
- **H2 the right checks fail.** Under the correction exactly these source checks fail, because they assert
  uncorrected reference numbers: EUC8 K1 and K5; LNJ1 KA-1 and KA-2; EUC5 A1 none. Every other source check keeps
  its committed state.
- **H3 the shift arrives.** EUC8's K1 line under the correction prints EUC17's corrected W_B fractions (0.444 /
  0.379) to 0.001.
- **H4 mask coverage** of each row's lenses reported; the 5 % rule of §1.
- **Twin** (mode `invert`, lm + log₁₀ f, separate outputs, driver exits 1): EUC8's far-case excess mass of class W
  rises against the committed value on both footings; EUC5 A1's sample median b_dyn rises on both footings; G1's
  f₂₅ does not fall. LNJ1 has no twin of its own here.

## 4. Seen before freezing (disclosed)

EUC17's and EUC18's numbers. The committed outputs of EUC4 (bins: secondary 0.425 / 0.380, complement 0.092 /
0.082), EUC8, EUC5 A1, EUC6 and LNJ1. From EUC17's as-frozen output, the corrected statistics of the 4 secondary
and 23 complement lenses that happened to have a mask then (b_med +0.078 and −0.138 canonical); nothing else about
the grade-B lenses. The EUC19 fetch's progress counts only.
Hand estimate, not verified: the secondary bin's correction is about 0.12 dex, f₂₅ falls to about 0.2–0.3, so G1
could read BREAK or NO VERDICT; G2 stays SLOPE NOT CONSTRAINED; G3 stays NO POWER.

## 5. Not graded here

EUC5 / EUC5R words (instrument gate), EUC6's word (needs a new control set), EUC4R and EUC13R (blind twins with
their own loaders), ESZ1, EXR1 / EXR2 (map stacks; EUC18's wide-lens reading gives the change in their input),
EUC7, EUC12. CJ1's row 39 is not edited.

## 6. Not claimed

No measurement of a₀ or κ. No pass of the lensing gate under any outcome. The premise (catalogue mass = in-mask
mass) rests on the paper's text and on one lens, as in EUC17.
