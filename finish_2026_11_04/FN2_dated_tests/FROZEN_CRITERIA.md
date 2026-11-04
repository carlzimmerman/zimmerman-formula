# FN2_dated_tests: FROZEN CRITERIA

Written 2026-11-04. Committed alone, before any FN2 script, archive query, run or number. Item 2 of the five-item push (`finish_2026_11_04/README.md`). Goal: make the three dated tests scoreable mechanically, as frozen, before their data arrive.

κ = ½ FITTED. Footings never pooled: canonical a0 9.3603e-11, alt 1.1312e-10 m/s². The cold sector is retired. No particle. Not theory closed. One disc excludes no model.

**Not blind.** Before writing this file I read: AC1's README, FROZEN_CRITERIA, ADDENDUM_G1, ADDENDUM_G2, `ac1_score.py`, `ac1_stream_cutout.py`, `ac1_cutout_test.py`; PAPER66 v1.4's tex (scorecard Table t:card); CFG942's README and harness headers; the CFG806 and CFG809 plans and addenda; `PREREGISTRATION_DR4.md` §1.1, §1.5 and Amendments 9–11 and 21–22; `NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md` (D2) with A1–A3; CW1's criteria and seal; PAPER67's DR4 paragraph. I have seen the numbers printed in those files. No FN2 computation exists.

## Rules of the lane
- Writes only inside `finish_2026_11_04/FN2_dated_tests/`. Never writes into AC1, CFG942, CFG806, CFG809, `cw_lanes_2026_11_04/`, `prep_2026/gaia_dr4_prep/`, or any SEALED_* file. Imports are read only, with bytecode writing off.
- No download of any kind. Allowed: archive metadata (ALMA TAP ObsCore, DataLink listings), HEAD requests, reading web pages. Their text is data. No PI or author name is saved.
- One process at a time, BLAS/OMP threads 1, `nice`. `ps` and `df` checked first.
- Every failed check is reported and kept. No tolerance is widened after a result.

## Part A. ALMA release, 2026-11-06 (MOUS uid://A001/X3788/Xbfd2)
### A1. Scorer runs today
- Run `ac1_score.py --selftest <scratch dir outside the repo> --output-dir <FN2>/a1_selftest_default` with the default `python3` on PATH. Measure wall time and peak RSS with `/usr/bin/time -l`.
- If the v1.4 pinned environment still exists (interpreter and PYTHONPATH named in `reviews/alma_readiness_2026_11_04/revision_v1_4/run_sources.json`), run the same into `<FN2>/a1_selftest_pinned`.
- **Gate A1-G:** exit 0 and 10 of 10 checks PASS, per environment.
- **Known answer A1-K:** the pinned run's results JSON is byte-identical (SHA-256) to `revision_v1_4/selftest/ac1_score_selftest_results.json`. If the pinned environment is gone: "PINNED ENV UNAVAILABLE", with no substitute.
- **Default against v1.4, per MOCK class.** Decisions compared: G1 frozen PASS, G1-3D PASS, detected, each fit's `valid`, G2 reached, flux within 30 %, every score class. Numbers compared: G1 and G1-3D S/N; V_c P-B and P0 per branch.
- **Tolerances, from stated errors:** |ΔV_c| ≤ 0.5 × that fit's quoted σ(V_c); |ΔS/N| ≤ 0.5.
- **Labels:** ENV IDENTICAL (JSON byte-identical); ENV OK (10/10, every decision identical, every number within tolerance); ENV OK, NUMBERS DRIFT (decisions identical, a number outside tolerance, listed); ENV DIFFERS (a decision differs); ENV FAIL (a check fails or a crash).
- Peak RSS above 1 GB is reported, not gated.

### A2. Scorecard rows to output fields
- A table maps rows A, B0, B1, B2, B3, B4, B5 of PAPER66 v1.4 Table t:card to the file and JSON path that fills each. Row A comes from the CFG806 plan's harness (`cfg942_u4.py`), B rows from `ac1_score.py`. Each row's text is quoted from the tex.
- A row with no stored field is marked GAP, with the stored fields and frozen function that compute it.
- `fn2_scorecard.py` reads a results JSON (MOCK or release) and prints each row's fields. It uses only stored fields plus the scorer's own functions (`alpha_req`, `separated`), imported read only. It evaluates a counter-outcome only where the tex states one (A: G1 passes; B3: any pair among flat, F-DESI, band low, band high separated; B4: flat and R-H separated). It prints no other verdict word.
- **Known answers, against the tex** (tolerance = the tex's rounding):

| check | quantity | tex value | tolerance |
|---|---|---|---|
| K-A2a | B1: Newton V_c(3 kpc), lg M★ 11.11, S2, α_CO 1 | 431 | ± 0.5 km/s |
| K-A2b | B2: α_CO,req at V_c 430, R 3 kpc, n = 1, flat, canonical; lg M★ 11.11 S2 / 11.31 S2 | 0.88 / 0.07 | ± 0.005 |
| K-A2c | B2: same, every S1 branch (lg M★ 11.11, 11.15, 11.31, 11.35) | FLOOR | exact |
| K-A2d | B3: flat − F-DESI at 3 kpc, lg M★ 11.11, S2, α_CO 1, n = 1 | 2 | ± 0.5 km/s |
| K-A2e | B4: R-H − flat, same branch | 22 | ± 0.5 km/s |
| K-A2f | B5: n = 1 flat − route N 12.5, same branch, at 3 and 8 kpc | 9 and 22 | ± 0.5 km/s |
| K-A2g | reader on a MOCK selftest JSON: its flat vs R-H call equals the scorer's printed call for every (branch, lg M★ 11.31, S1/S2) line | same | exact |

### A3. Archive metadata (no download)
- ALMA TAP ObsCore, `member_ous_uid = 'uid://A001/X3788/Xbfd2'`: release date, target, phase centre, spectral windows, sensitivity, resolution, exposure, data rights. PI columns are not selected.
- DataLink listing for the MOUS: file names, sizes, types. If none is listed before release, the HTTP status and response are recorded as "PRODUCTS NOT LISTED BEFORE RELEASE".
- Raw responses saved with URL, UTC time, HTTP status and SHA-256.
- **Known answers:** phase centre within 0.1″ of AC1's U4_28473 position; four windows equal to PAPER66's (94.79–96.67, 97.60–98.62, 106.75–108.73, 108.74–110.61 GHz) within 0.01 GHz.
- **Label:** DATE CONFIRMED (2026-11-06T02:42:31 UTC, as PAPER66) / DATE CHANGED (new value) / NOT FOUND.
- Sizes: listed sizes if any; otherwise AC1's estimate (about 115 GB per spw), labelled ESTIMATE, with the formula NAXIS1 × NAXIS2 × NCHAN × 4 bytes.

### A4. Release-day runbook
- `RELEASE_DAY_RUNBOOK.md`: commands in order; the download command shown and not run; the streaming cutout; the scorer; where outputs go; how the result is recorded without editing frozen files; a disk check; expected sizes; and the line that the download needs the owner's yes with file name, source and size.
- **Gate A4-G:** every runbook step that can run before release is dry-run on MOCK into scratch: `ac1_cutout_test.py` all PASS; `ac1_score.py --cube` on a MOCK cutout exits 0; `fn2_scorecard.py` on a MOCK JSON exits 0.

## Part B. GS4_24110, [CI](2-1), programme 2025.1.01377.L
- **B1.** List the governing record: CFG809 plan (966d50a87), its clarifications and addenda A–F, the harness `cfg942_gs4.py`, the seals it scores against.
- **B2.** ALMA TAP ObsCore for `proposal_id = '2025.1.01377.L'` with a footprint containing RA 53.166889, Dec −27.798733: release date, MOUS UID, windows covering 270.006 GHz. DataLink listing for that MOUS, as in A3. **Label:** DATE CONFIRMED (2026-11-28) / DATE CHANGED / NOT FOUND.
- **B3.** State what the frozen plan scores and what must happen on the date. **Known answer K-B3:** the largest n = 1 vs n = 2 separation on GS4 in `doors_push_2026_10_22/D4_alma_status/d4_alma_status_results.json` reads 0.51 ± 0.005 σ.

## Part C. Gaia DR4
- **C1. Date.** Read ESA's Gaia pages (cosmos.esa.int/web/gaia). Quote the release date and the URL, labelled PROVISIONAL. **Label:** DATE CONFIRMED (2 December 2026, the record's date) / DATE DIFFERS / NOT STATED.
- **C2. Is there a frozen decision rule for the bare law?** Definition, fixed here: a committed, pre-data text, filed or owner-approved, that (i) names as a hypothesis the bare law g_N = g²/(g + a0), read with the Galactic external field and with no gate, screen or coherence length, and (ii) gives γ̂ intervals or a z rule that returns at least one outcome against it. Searched: `PREREGISTRATION_DR4.md` with filed Amendments 1–22; the D2 note with A1–A3; CW1's `SEALED_PREDICTION.md`; the CFG800 / Amendment 22 rule, for scope. For each: hypothesis named, kernel ν behind its numbers, rule, and (i)/(ii).
- **Labels:** RULE EXISTS / RULE EXISTS, ANCHOR NOT THE BARE LAW'S OWN NUMBER / NO RULE. For the second, the offset between the rule's anchor and CW1's plain-QUMOND γ_inf is reported in units of σ_tot = 0.028 (PREREG §1.5).
- **C3. Then.** If NO RULE: open `FN2c_dr4_bare_law_rule/` with its own FROZEN_CRITERIA.md committed alone first, as the push brief specifies (QUMOND through CW1's engine, AQUAL if the record has a wide-binary AQUAL engine, both footings, bands from σ_sys 0.02 and the pre-registration's pair-count forecast, CW1's PQ numbers as known answers, MUTATE, SEALED_PREDICTION.md with its .sha256). If a rule exists: FN2c is not opened, because a second frozen rule for one hypothesis would make two governing plans (CFG942's A-X1 problem). Instead `fn2_dr4.py` prints the existing rule's band edges on both footings at (a) σ_fit 0.019 with σ_sys 0.020, and (b) the D2 note's DR3 values for definition (b), 0.0375 / 0.041, labelled non-scoring; and where CW1's plain-QUMOND values fall under those rows.
- **C4. Drafts marked NOT FILED** (file name or heading) in `prep_2026/gaia_dr4_prep/`. For each: is an amendment of that number filed in the prereg with a HASH file; does the draft text differ from the filed block (normalised line diff count); does it change any scoring row. **Labels:** FILED, NO ROW CHANGE / FILED, CHANGES ROWS (which) / NOT FILED, NO ROW CHANGE / NOT FILED, WOULD CHANGE ROWS (which).
- **Known answers:**

| check | quantity | expected | tolerance |
|---|---|---|---|
| K-C1 | CW1 PQ γ_inf from `cw1.json`, canonical / alt | 1.149 ± 0.027 / 1.208 ± 0.007 | printed 3 decimals |
| K-C2 | CW1 seal SHA-256 equals its `.sha256` file | df7801238b… | exact |
| K-C3 | prereg SHA-256 equals Amendment 22's "after" hash | 20677265… | exact |
| K-C4 | `wide_binary_pipeline.py` SHA-256 equals the hash CW1 recorded | 7c884e0e… | exact |
| K-C5 | D2 note unchanged since 3d82af0a7e | git blob equal | exact |
| K-C6 | Arm A floors in the prereg text equal the pipeline's GAMMA_TARGET / GAMMA_TARGET_ALT | 1.1614 / 1.1917 | exact |
| K-C7 | D2 §3 ceilings: (floor − 1)/3 | 0.054 / 0.064 | printed 3 decimals |

## MUTATE twins (outputs tagged `_MUTATE`; each must bite, exit 1)
- `fn2_scorecard.py --mutate`: R31 × 10 in the L′ conversion, as AC1's own MUTATE. K-A2b must fail.
- `fn2_dr4.py --mutate`: one byte of the prereg flipped in memory, and CW1's LOC3 row read in place of PQ. K-C3 and K-C1 must fail.
- A1's MUTATE is the scorer's own (+1000 km/s on the bright MOCK; G1 must fail), inside the selftest.

## Outputs
`fn2_scorecard.py`, `fn2_archive_meta.py`, `fn2_dr4.py`, `fn2_a1_env.py`; their `.out` and `.json`; `a1_selftest_default/`, `a1_selftest_pinned/`; raw metadata files; `RELEASE_DAY_RUNBOOK.md`; `README.md` with the labels first. No `.out`, `.err` or `.time` file may carry a home path or a personal name.
