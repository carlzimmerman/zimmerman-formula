# OWNER DECISION, 2026-11-15 (second note of the day, pre-data): the Gaia DR4 gaps left open by the registry map

**Status: filed.** The owner answered in chat on 2026-11-15, before any DR4 byte exists (DR4 due 2026-12-02), to the
decision sheet `closure_2026_11_15/DR4DS1_gaia_dr4_decision_sheet/DR4_DECISION_SHEET.md` (sha256 62025483fc02...,
full digest in section 5): **"Accept all recommended"**. That adopts option (a) of each of the sheet's questions Q1 to
Q10 and a yes to its text items T1 to T3. The options as presented, with the ones not chosen, are in the sheet and are
not repeated here. Committed alone; never edited after commit; any change goes in a new dated file. It edits no frozen
file: not PREREGISTRATION_DR4.md or its 22 amendments, not the D2 note or A1-A3, not the three decision notes of
2026-11-05, not the first note of 2026-11-15, not CQ2's seal, not CFG816's criteria, and no scorer, wrapper or runbook.
No prediction, estimator, cut, threshold or verdict row changes. kappa = 1/2 FITTED; footings never pooled; not theory
closed. Nothing here says the data favour the framework.

## 1. What is decided: the headline label

- **Q1 (map C3). The filed seed-mean entry is to be wired into the release-day path.** A pre-data fix is commissioned:
  a new step in the wrapper and the runbook for the DR4 K = 50 seed-mean sweep, the option `--nss-off-seed-mean` passed
  at step O12, and the option's help text corrected. It is new code with its own criteria committed alone first, a DR3
  equivalence check and a mutation, all before any DR4 byte. Decision 11-05c is unchanged; this makes the path compute
  what that decision says.
- **Q2 (map C3). Cone coverage for the NSS-off rung on DR4 is the fallback.** Pairs of the rung that have no cone are
  handled with `--missing-cones extract-fallback`, and the number of fallback pairs is stated in the result. This
  settles the item that 11-05c left as "the owner's call on release day, not decided here".
- **Q3 (map C4). The R label quoted is CFG816's own**, from the once-only run of `cfg816_r.py` under its frozen
  criteria. Where the word that `dr4_outcome_map.py` recomputes differs, both are stated in the same sentence. Stated
  with the choice: this is the reading under which a kill is harder. R bears on CFG740's stiffness construction only
  and is never merged with the gamma-hat rows.
- **Q4 (map C5). Each footing has its own verdict line.** A canonical / alt split is reported as a split, with no
  single headline. The prereg's phrase "(canonical footing decides; alt footing reported)" is read as superseded for
  the D2 rows by the later rulings (D2 A3 of 2026-10-22, and the note of 2026-11-05). The prereg's text is not edited.
- **Q5 (map C6, runbook O6). The rungs that enter sigma_sys(b) on DR4 are the D2 recipe's three:** R_chance < 0.001,
  3-20 kAU and the NSS-off entry, the last as 11-05c and Q1 leave it. The RUWE < 1.2 rung is run and reported as
  information, with no weight in sigma_sys(b).
- **Q6 (map section 6). A pre-data check of CQ2 under the adopted blend is commissioned:** CQ2's screening margin
  recomputed with the Pi^6 blend adopted on 2026-11-07, criteria committed alone first, reported beside the seal. The
  seal is never edited. If the margin does not hold, that is recorded before the data and comes back to the owner.

## 2. What is decided: what is printed beside the headline

- **Q7 (map C9). The September ridge rows are information rows.** Matrix row 1 (G088 / G165 / Z03), G018 and E6 / E7
  are not scored for the adopted theory, and `dr4_scorer.py` is not run. The result says in one sentence what the
  pooled gamma-hat shows against each row's own level band, as far as a pooled number can, names the identification
  each row belongs to, and says the period-separation part was not evaluated. A fail of an earlier identification is
  recorded as a fail.
- **Q8 (map C12). Amendment 14(c)'s separation-resolved statistic is run on the day,** after the label steps and
  report-only, given a DR3 code-path check in the same lane as Q1's fix. If that check fails, the result declares it
  NOT RUN. It cannot change a label.
- **Q9 (map C10). No Milky Way row is scored for form B or v3s.** When a published Jeans, Oort or K_z analysis exists,
  each seal (CFG553, S3, GD1, matrix rows 2, 3, 26, 29 and 31) is scored as frozen for the form that sealed it, as
  history. No Milky Way reading is registered for the adopted theory.
- **Q10 (map C7). The optional neighbour tables for cut 13 are not searched.** `crowded_field_source` and
  `gaia_source_environment` are not searched; their counts are recorded in the manifest before the data are opened, as
  Amendment 16(b) requires, and this choice is recorded there on the day with a pointer to this note.

## 3. What is decided: text only

- **T1 (map C13).** The pipeline's current sha256 is recorded in a dated note.
- **T2 (map C14).** The root `STANDING.md` gets a dated DR4 addendum. PAPER67's wording is the owner's act and is not
  touched.
- **T3 (map C8, runbook O3).** Access stays anonymous, as rehearsed. No login hook is added.

## 4. What is not decided here

- **What happens if the fix lane of Q1, Q2 and Q8 is not finished and checked before the data, or its DR3 check
  fails.** The sheet stated a fallback only for Q8 (NOT RUN). For Q1 and Q2 none was put to the owner; if the case
  arises it needs its own dated decision before the data.
- The first question of the map's C1, whether the stability requirements should gate an exclusion. The ruling of
  2026-10-22 stands, as the first note of 2026-11-15 says.
- Whether CFG553's round rule is inside form B (the map's unresolved point). Q9 (a) does not need it.
- Any code. The fix lane and the check lane are commissioned by this note and are not part of it. Until the fix lane
  lands, `dr4_release_day.sh` is as the map found it.
- Any archive step. Each still needs its own `GO <step>` on the day.

## 5. Sources

The sheet, `closure_2026_11_15/DR4DS1_gaia_dr4_decision_sheet/DR4_DECISION_SHEET.md`, sha256
62025483fc026cb7345fa494b57a78921c35347f846e99bcc054201e11a5e8af, with its quotation audit (29 of 29) and mutation
twin (26 of 26); `closure_2026_11_12/DR4MAP_gaia_dr4_registry_map/DR4_MAP.md` (sections 4 and 6); in this folder, the
decision notes of 2026-11-05 (05, 05b, 05c) and `OWNER_DECISION_2026-11-15_DR4_FORM_B_READING.md`,
`PREREGISTRATION_DR4.md` (section 1.5, Amendments 14(c) and 16(b)) and `NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md` (A3);
`dr4_push_2026_11_05/DP3_release_day/RELEASE_DAY_RUNBOOK_DR4.md` (section 5);
`campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/FROZEN_CRITERIA.md`.

kappa = 1/2 FITTED; not theory closed.
