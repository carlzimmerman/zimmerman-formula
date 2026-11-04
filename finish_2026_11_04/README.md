# Finish push, 2026-11-04: five items, each with a verdict

The owner asked for the five things that would finish the theory, then said to do all of them rigorously. Each item is a lane here, prefix FN. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

"Finish" here means every door ends in a verdict, the distinctive claim gets its test, and outsiders can grade the record. It does not mean the theory is closed.

| Item | Lane | Verdict | Waits on |
|---|---|---|---|
| 1. Action call | `FN1_action_call/` | Decision brief written. **FN1b: NO UNIVERSAL LENGTH PASSES** on either footing in the form an action gives: Cassini and the planets pass at every length, the dwarfs only up to 0.1 kpc, the Milky Way only at 2 kpc. Option (b), a fixed-length smoothed QUMOND, fails at its static limit. Left: (a) v3s as it stands, or (c) no action, with requirement 12 stated as open | The owner's choice |
| 2. Dated tests | `FN2_dated_tests/` | **ALMA 2026-11-06 02:42:31 UTC and GS4_24110 2026-11-28 18:25:24 UTC: DATE CONFIRMED.** Scorer ENV IDENTICAL to v1.4; scorecard known answers 7 of 7; release-day runbook ready. **Gaia DR4 2 December 2026** (provisional). The bare law already has a frozen DR4 rule (the D2 note's law-first rows); no second rule sealed | The owner's yes for the ALMA cubes (34.7 + 38.6 GB streamed, 3-8 GB kept) and the GS4 cube (7.0 GB) |
| 3. a0 at z ~ 1 | `FN3_musedark_law_refit/` | **NOT DECIDABLE WITH THE EXISTING CUBES.** As frozen: Stage 0 NOT EVALUABLE (K1), Stage 1 NO VERDICT (K2a); under A2, no label (K2'). With HI unmeasured, a planted rise of the survey's size grades BAND CONSISTENT. No cutout requested | An HI mass at z ~ 0.3-1.4, or a tracer past the HI-dominated radii. The dated test of the tie stays CFG689 P6, a0 at z ~ 2.5 to 0.10 dex |
| 4. Four galaxy rows | `FN4_galaxy_rows_data/` | **Lensing: REBUILD MATCHES, GAP STANDS** (255,052 lenses against 259,383; +0.085 / +0.046 dex). **Local Group field: FIELD MOVES NOTHING** (largest class shift +0.013 dex). IC 1613, Local Group discs and HI lenses: criteria frozen (FN4a, FN4d, FN4e). Milky Way vertical force: needs new observations; no lane | The owner's yes for each listed download (`READINESS.md`); new observations |
| 5. Ship the record | `FN5_ship_record/` | **PAPER67 v1.1 ready except the BK2 L2 line**: owed fixes and the 11-02 to 11-04 lanes in, plus TX1, MB1, BF3, DB1; audit 625 of 626 (the PENDING marker). Outside summary redrafted, `rebuild_2026_10_22/EXTERNAL_SUMMARY_2026-11-04_DRAFT.md`, audit 220 of 220, unsent | BK2's L2 controls (held by another session, with the marker and the deposit); the owner sends the summary |

## Failed checks across the push, each disclosed in its lane
- FN1b: KT14's smoothing test fails at 24 pc (that Milky Way row not evaluable); the SPARC self-check fails at 24 pc (grid can't resolve it); peak memory 1.26-1.31 GiB.
- FN2: K-A3's first run compared calibrator rows too (kept; rerun passes); default environment drifts by at most 1.3e-6 km/s; 1.05 GB peak.
- FN3: K1 failed as frozen; K2a failed as frozen; K2' failed; the first K2' run crashed at its last JSON write (rerun byte-identical).
- FN4c: the frozen stage-2 MUTATE didn't bite (graders bin by mass; a post-result twin bites); the first run peaked at 25 GB (fixed; rerun byte-identical at 0.52 GB).

## Process note
Commit 93b4235c4b, titled for the outside-summary draft, also carries FN3's K2 outputs and `AMENDMENT_A2.md`, swept in through the shared git index. Nothing was rewritten; FN3's README records it. Every commit since names its paths.
