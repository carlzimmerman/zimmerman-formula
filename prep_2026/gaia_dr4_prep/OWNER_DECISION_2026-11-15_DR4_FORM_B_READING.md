# OWNER DECISION, 2026-11-15 (pre-data): which registered wide-binary reading scores form B on Gaia DR4

**Status: filed.** The owner answered in chat on 2026-11-15, before any DR4 byte exists (DR4 due 2026-12-02), to the
question "Which reading should be the headline score for form B on Gaia DR4?": **"The 11-05 rows"**. This closes gap C2
of `closure_2026_11_12/DR4MAP_gaia_dr4_registry_map/DR4_MAP.md` (9421bd61b1) and the last clause of its C1, which line
is the headline when the two readings disagree. Committed alone; never edited after commit; any change goes in a new
dated file. It edits no frozen file: not PREREGISTRATION_DR4.md or its 22 amendments, not the D2 note or A1-A3, not
the three decision notes of 2026-11-05, not CQ2's seal, and no scorer, wrapper or runbook. kappa = 1/2 FITTED;
footings never pooled; not theory closed. Nothing here says the data favour the framework.

## 1. What was put to the owner

The registry map found that form B (the form the record closes on since 2026-11-09) says only that the
pre-registration is "scored as frozen", and that two registered readings could score it. Both predict gamma = 1.000,
a Newtonian binary. They differ in how a measured boost is judged.

- **The 11-05 rows.** CQ2's sealed prediction (v3s = Newton), scored as the screened / medium-first reading of the
  frozen D2 rows plus the R rule, under D1 (a) of `OWNER_DECISION_2026-11-05_DR4_FORKS.md` (413c1c8e24), completed by
  the notes 11-05b and 11-05c. The error is sigma = sqrt(sigma_fit^2 + sigma_sys(b)^2), with sigma_sys(b) measured on
  DR4 and gated. The section 1.5 stability requirements are computed and reported beside the verdict with no verdict
  weight (D2 A3, owner, 2026-10-22).
- **The settling-model rows.** Amendment 21's settling working model, scored by Arm C's rows: z_C = (gamma-hat - 1) /
  sigma_tot with the frozen sigma_sys 0.020, falsified from above only if the frozen stability requirements pass,
  otherwise "systematic-limited, no verdict".

On a Newtonian sky both read survival. On a boost with the stability requirements failing, the first reads excluded
and the second reads no verdict; the map records that on DR3 the stability gate failed on both footings (largest
ladder shift 0.075 against sigma_fit 0.055). The lead recommended the first reading: it is the one scored
confrontation the record already holds for the adopted theory, it is the stricter of the two on a boost, and it
registers no new prediction.

## 2. What is decided

- **Form B's headline score on Gaia DR4 wide binaries is the 11-05 reading.** The word that the D2 rows and the R
  rule give for v3s, on each footing, is the word for form B on wide binaries. No new prediction is registered. Form
  B's rule 5 (a body that brought no charge has no halo) gives the same Newtonian number and stays unsealed.
- **Wording.** A Newton-side reading is survival for v3s and for form B on this row, never confirmation. An excluded
  reading counts against form B on this row in the same words as for v3s. UNDECIDED and NO VERDICT keep their
  meanings.
- **The settling-model rows are printed beside the headline as information, with no verdict weight for form B.**
  Where they disagree with the headline, both are stated in the same sentence.
- **The stability requirements keep the weight the ruling of 2026-10-22 gave them:** computed and reported beside the
  verdict, with no verdict weight. If they fail on the day, that is stated in the same sentence as the verdict.

## 3. What is not decided here

- The first question of the map's C1, whether the stability requirements should gate an exclusion. The ruling of
  2026-10-22 stands and no scorer is changed.
- The map's C3 (the seed-mean entry of 11-05c is not wired into the release-day path), C4 (which R label is quoted),
  C5 ("canonical footing decides" against one verdict per footing) and C6 to C15.
- The Milky Way rows, for which the adopted theory has no registration.
- Any code. `dr4_outcome_map.py` prints the D2 rows' word for v3s; attaching that word to form B is a rule for the
  report on the day, stated here.

## 4. Sources

`closure_2026_11_12/DR4MAP_gaia_dr4_registry_map/DR4_MAP.md` (sections 0, 2 and 4); the three notes of 2026-11-05 in
this folder; `cq_lanes_2026_11_04/CQ2_v3s_dr4_seal/SEALED_PREDICTION.md`; `closure_2026_11_07/PREDICTIONS_2026_11_07.md`
(section 1); `closure_2026_11_09/OWNER_DECISION_2026-11-09_FINAL_FORM_B.md`; and the record's closure statement,
`closure_2026_11_15/BCS1_bounded_closure_statement/BOUNDED_CLOSURE_STATEMENT.md` (Section 5, line 1).

kappa = 1/2 FITTED; not theory closed.
