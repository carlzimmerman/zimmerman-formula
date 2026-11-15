# DR4DS1: Gaia DR4 decision sheet (draft for the owner; decides nothing)

Drafted 2026-11-15 by the lead. Gaia DR4 is due 2026-12-02 (ESA, provisional). This sheet turns the gaps still open in
the registry map (`closure_2026_11_12/DR4MAP_gaia_dr4_registry_map/DR4_MAP.md`, sections 4 and 6) into questions with
options. It decides nothing, edits no frozen file, changes no scorer and registers no prediction. Each recommendation
is the lead's and carries no weight until the owner answers. An answer becomes a new dated decision file in
`prep_2026/gaia_dr4_prep/`, committed alone, before any DR4 byte exists. kappa = 1/2 FITTED; footings never pooled; not
theory closed. Nothing here says the data favour the framework.

The gaps were re-read against the files on 2026-11-15. `dr4ds1_audit.py` checks every quotation below against its
file, and that the release-day script still lacks the seed-mean step (Q1).

## 0. How to answer

One line is enough: "Accept all recommended", or the letters, for example "Q1 a, Q2 a, Q3 b". A question left
unanswered stays open, and the runbook's rule for its open issues is that "none can be decided after the data".

## 1. Already settled (no answer needed)

| map gap | settled by |
|---|---|
| C2, and the headline clause of C1 | Owner decision 2026-11-15, `prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-15_DR4_FORM_B_READING.md`: "Form B's headline score on Gaia DR4 wide binaries is the 11-05 reading." |
| C1, first question (do the stability requirements gate an exclusion?) | Not reopened by that decision: "The ruling of 2026-10-22 stands and no scorer is changed." The requirements are computed and reported with no verdict weight. Reopening it needs a new dated decision. |
| C11 (Newton reference) | D3 (a) of 2026-11-05: 1.000; the pipeline's own Newton draws are information. |
| C15 (which law-first anchor) | D2 (a) of 2026-11-05: Arm A's floor; the other anchors print as an information split. |

## 2. Questions that can change the headline label

### Q1 (map C3). Wire the filed seed-mean entry into the release-day path?

- The record: decision 11-05c is "FILED 2026-11-08" and makes the NSS-off entry of sigma_sys(b) the K = 50 seed mean.
  The release script (`dr4_push_2026_11_05/DP3_release_day/dr4_release_day.sh`) still calls `dp3_sigma_sys.py` without
  `--nss-off-seed-mean`; the option's help text still reads "OPTIONAL, default off (DP7, draft
  OWNER_DECISION_2026-11-05c, NOT FILED)"; and the script has no step for the DR4 seed-mean sweep.
- On the day, run as scripted, the binding error term would be the single-seed entry that the owner replaced.
- **(a) Commission the pre-data fix.** A new step in the wrapper and the runbook for the DR4 K = 50 seed-mean sweep,
  the option passed at step O12, and the help text corrected. New code with its own criteria committed alone first, a
  DR3 equivalence check and a mutation. **Recommended:** the decision is filed, so the path should compute what it
  says.
- **(b) Withdraw 11-05c** by a new dated note. D8 (a)'s single-seed entry then stands and the script is right as it
  is.
- Cost on the day under (a), as the map quotes DP7: "about 70-80 min, 4.0-4.3 GB per fit", plus archive delta fetches
  that each need a GO.

### Q2 (map C3). Cone coverage for the NSS-off rung on DR4

- 11-05c left this open: "that is the owner's call on release day, not decided here." The cut-13 cone query covers
  the candidate set after the NSS screen; the NSS-off rung also needs cones for the pairs that screen had removed.
- **(a) The fallback.** `--missing-cones extract-fallback` for those pairs, with the number of fallback pairs stated
  in the result. **Recommended:** it is the path DP7 checked on DR3 (139 pairs; "bias bound ~0.1 pair from the cones'
  own flag rate"), and it adds no archive load to a cone step the map puts at "about 39,000 queries, about 47 h
  serial".
- **(b) The wider query.** Extend the cone query to the candidate set before the NSS screen: the literal cut 13 for
  every pair of the rung. More queries (the count is unknown until the DR4 candidate dump) and a path not rehearsed on
  DR3.

### Q3 (map C4). Which R label is quoted

- CFG816's frozen criteria: if the kill threshold is met on the primary but not on the NSS-screened branch, or the
  tail fraction differs between regimes by more than its 2 sigma, "the result is labelled CONTAMINATION-LIMITED, not
  KILLED". The final scorer (`dr4_outcome_map.py`) recomputes the label from R, sigma_R and N alone, so in that case it
  prints KILLED.
- Under D7 N5 the NSS-screened branch equals the primary, so only the tail-fraction leg can fire.
- **(a) CFG816's own label is the R label**, from the once-only run of `cfg816_r.py` under its frozen criteria. Where
  the scorer's word differs, both are stated in the same sentence. **Recommended:** it is the R rule as frozen. Said
  plainly, this is the reading under which a kill is harder; the criteria's own words are "This makes a kill harder
  than a literal reading of CFG800".
- **(b) The scorer's KILLED is the R label**, with CFG816's downgrade stated beside it. This is the stricter reading
  against the stiff-hedgehog construction.
- Either way R bears on CFG740's stiffness construction only and is never merged with the gamma-hat rows.

### Q4 (map C5). The headline footing when canonical and alt split

- Prereg section 1.5: "(canonical footing decides; alt footing reported)". D2 A3 (owner, 2026-10-22): "Canonical and
  alt are scored separately, never pooled; each footing gets its own verdict line."
- **(a) Each footing has its own verdict line.** A split is reported as a split, with no single headline; the
  prereg's phrase is read as superseded for the D2 rows by the later rulings. **Recommended:** it matches the standing
  rule that footings are never pooled, and an exclusion on alt cannot hide behind a survival on canonical.
- **(b) Canonical is the headline;** alt is reported beside it.

### Q5 (map C6, runbook O6). Which rungs enter sigma_sys(b) on DR4

- The D2 recipe used R_chance < 0.001, 3-20 kAU and the NSS-off entry, and left RUWE < 1.2 out as unimplementable on
  DR3. That rung now exists (`dp3_sigma_sys.py --stage-a`, off by default). From the runbook: "On DR3 (information) it
  leaves canonical (b) at 0.0375 and moves alt from 0.0412 to 0.0350." "The RV-screened rung has no implementation
  anywhere."
- **(a) The D2 recipe's three entries**, with the NSS-off entry as Q1 leaves it; RUWE < 1.2 is run and reported as
  information. **Recommended:** D8 reads "Option (a) adopted: σ_sys(b) stays as frozen", and adding a rung to the
  binding error term after DR3 showed its effect would read as tuning. Against it: the reason D2 gave for leaving the
  rung out no longer holds.
- **(b) RUWE < 1.2 enters as a fourth rung.**

### Q6 (map section 6). CQ2's sealed number under the adopted blend

- CQ2 was computed with v3s's raw kink. The Pi^6 blend was adopted as the stiffness on 2026-11-07, and the map found
  that "the blend decision says labels are unchanged but records no wide-binary re-run". No commit since has re-run
  it.
- **(a) Commission a pre-data check:** CQ2's screening margin recomputed with the adopted blend, criteria committed
  alone first, reported beside the seal. The seal is never edited. If the margin does not hold, that is recorded
  before the data and comes back to the owner. **Recommended:** it is the one sealed number computed for a stiffness
  the record has since replaced, and a check made after the data would read as post hoc.
- **(b) No check.** Scored as frozen, with the gap disclosed in the result.

## 3. Questions on what is printed beside the headline

### Q7 (map C9). The September ridge rows and `dr4_scorer.py`

- Matrix row 1 (G088 / G165 / Z03), G018 and E6 / E7 are still marked ARMED, and no decision retires or keeps them.
  `dr4_scorer.py` needs per-pair rows that the frozen pipeline does not produce, and it prints CONFIRMED, against the
  wording rule D6. On a Newtonian sky row 1 reads a kill of the September identification while v3s reads survival,
  "so the record would print a kill and a survival for one result".
- **(a) Information rows.** `dr4_scorer.py` is not run. The result says in one sentence what the pooled gamma-hat
  shows against each row's own level band, as far as a pooled number can (the rows were written for binned and
  per-pair statistics), names the identification each row belongs to, and says the period-separation part was not
  evaluated. **Recommended:** no new code, nothing hidden, and a fail of an earlier identification is recorded as a
  fail.
- **(b) Retired** by a dated note and not mentioned in the result.
- **(c) Scored:** needs a new per-pair input with its own criteria before the data.

### Q8 (map C12). The separation-resolved statistic of Amendment 14(c)

- The amendment's heading: "The separation-resolved statistic — registered as the measurement of ξ." It is in no
  runbook step.
- **(a) Run it on the day,** after the label steps and report-only, given a DR3 code-path check in the same lane as
  Q1's fix. If that check fails, the result declares it NOT RUN. **Recommended:** it is registered, and it cannot
  change a label.
- **(b) Not run on the day;** run later as information, and the result says so.

### Q9 (map C10). The Milky Way rows

- The map: "no registration exists for the adopted theory". The seals that exist (CFG553, S3, GD1, matrix rows 2, 3,
  26, 29 and 31) belong to retired or non-adopted forms; none has a scorer for DR4 data; each needs a published Jeans,
  Oort or K_z analysis.
- **(a) None is scored for form B or v3s.** When such an analysis is published, each seal is scored as frozen for the
  form that sealed it, as history. **Recommended:** v3s's adopted scope excludes the Milky Way joint fit, and naming a
  reading now would be a new registration.
- **(b) Name CFG553's rule as form B's Milky Way reading** by a dated pre-data decision. This first needs the map's
  unresolved point settled: whether CFG553's round rule is inside form B.

### Q10 (map C7). The optional neighbour tables for cut 13

- Amendment 16(b), on `crowded_field_source` and `gaia_source_environment`: "it is decided on release day, and
  recorded, whether those tables are also searched". The manifest records their counts before the data are opened.
- **(a) Not searched.** The counts are recorded as the amendment requires, and the primary criterion's two all-source
  tables stand. **Recommended:** no tool searches them today, and DR3 offers no rehearsal.
- **(b) Searched,** if the release publishes them with the needed columns: new code with its own criteria before the
  data.
- The amendment itself places this choice on release day, before the data are opened. Answering now only takes a
  choice off the day.

## 4. Text only (one yes covers all three)

- **T1 (map C13).** Record the pipeline's current sha256 in a dated note. The map: "No filed amendment records the
  new hash."
- **T2 (map C14).** A dated DR4 addendum to the root `STANDING.md`, whose list of live fronts "still names Arm A as
  the DR4 front". PAPER67's wording is the owner's act and is not touched.
- **T3 (map C8, runbook O3).** "None of the tools logs in". Stay anonymous, as rehearsed, unless the owner wants a
  login hook (new code, tested, before release). Whether anonymous access carries the cone step on DR4 is not known.

## 5. What an answer sets in motion

1. One dated decision file in `prep_2026/gaia_dr4_prep/`, committed alone, quoting the owner's words.
2. If Q1 (a), Q2 or Q8 (a): one fix lane, with its criteria committed alone first, a DR3 check and a mutation, all
   before any DR4 byte. Its compute is not estimated here.
3. If Q6 (a): one check lane under the same discipline.
4. T1 to T3: notes only.

Drafting this sheet ran nothing, fetched nothing and launched nothing.

## 6. What this sheet did not check

- Whether `dr4_outcome_map.py`'s self-test still passes (the map did not run it either).
- Whether another session's uncommitted work bears on these gaps.
- The earlier registries the map itself did not read one by one.

## 7. Files read

`closure_2026_11_12/DR4MAP_gaia_dr4_registry_map/DR4_MAP.md`; in `prep_2026/gaia_dr4_prep/`: the decision notes of
2026-11-05 (05, 05b, 05c) and of 2026-11-15, `PREREGISTRATION_DR4.md` (section 1.5, Amendments 14(c) and 16(b)) and
`NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md` (A3); in `dr4_push_2026_11_05/DP3_release_day/`:
`RELEASE_DAY_RUNBOOK_DR4.md`, `dr4_release_day.sh`, `dp3_sigma_sys.py` and `dr4_outcome_map.py`;
`campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/FROZEN_CRITERIA.md`.

kappa = 1/2 FITTED; not theory closed.
