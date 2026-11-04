# FN2_dated_tests: the three dated tests, scoreable as frozen

**Labels (criteria 755f05c3cf, committed alone first).**
- **ALMA, 2026-11-06 02:42:31 UTC: DATE CONFIRMED.** Scorer runs today: ENV IDENTICAL (pinned v1.4 environment), ENV OK, NUMBERS DRIFT (default `python3`). Scorecard known answers 7 of 7. Dry run of the release steps 4 of 4. Runbook: `RELEASE_DAY_RUNBOOK.md`. Downloads: 34.7 GB + 38.6 GB, streamed, waiting for the owner's yes.
- **GS4_24110, 2026-11-28 18:25:24 UTC: DATE CONFIRMED.** The frozen MUTATE cannot run on the released window.
- **Gaia DR4, 2 December 2026: DATE CONFIRMED, PROVISIONAL** (ESA's release page).
- **Bare-law decision rule: RULE EXISTS, ANCHOR NOT THE BARE LAW'S OWN NUMBER.** The D2 note's law-first rows. FN2c not opened.
- **Amendment drafts marked NOT FILED: 10, all filed.** None pending.

κ = ½ FITTED. Footings never pooled. The cold sector is retired. No particle. One disc excludes no model. Not theory closed. No byte of any release was downloaded.

## Part A. ALMA, MOUS uid://A001/X3788/Xbfd2 (2024.1.00100.L, U4_28473)

### A1. The scorer today (`fn2_a1_env.py`)
| environment | checks | label | wall | peak RSS |
|---|---|---|---|---|
| pinned v1.4: python 3.9.6, numpy 1.26.4, scipy 1.11.4, astropy 6.0.1 (`/tmp/alma_v14_pydeps`) | 10 of 10 | ENV IDENTICAL: results JSON byte-identical to v1.4 (A1-K PASS) | 223 s | 0.70 GB |
| default `python3`: 3.13.9, numpy 1.26.4, scipy 1.14.1, astropy 7.2.0 | 10 of 10 | ENV OK, NUMBERS DRIFT | 297 s | 1.05 GB |

Every decision is identical to v1.4 in both. The default run's drift: two unscored fits (FIT NOT CONSTRAINED) quote σ(V_c) = NaN, so their tolerance is undefined and the frozen script counts it as zero; they differ by at most 1.3e-6 km/s. The largest difference anywhere is 7.2e-6, in a S/N. The default run's 1.05 GB is above the 1 GB small-job line. `/tmp` can be cleared by a reboot; the default environment is the fallback.

### A2. Scorecard rows (`fn2_scorecard.py`, `fn2_scorecard.out`)
| row | output that fills it | gap |
|---|---|---|
| A | `cfg942_u4_RELEASE_results.json`: `results.measured.G1` (selection-aware S/N decides), `SN_selection`, `logMgas_UL`, `results.score.overall` | none |
| B0 | `ac1_score_RELEASE.json`: `detected`, `gate`, `G1_3D`, `G1_frozen` (beside), `sig_ch`·√(dv/10), `beam`, `fits.<incl>.valid` | the tex gives no numeric test of "the sister noise and beam hold"; ratios printed |
| B1 | `fits.<incl>.V`, `error_calibration`, `R_score`; Newton rows of `score` | no stored Newton grid at R_score; computed from the frozen inputs |
| B2 | `score.<branch>.<lgM*|shape>.<reading>.{nominal, lo, hi, class_}` | lg M★ 11.11 is not a stored key (recomputed with `alpha_req`); "near 430" has no width in the tex; applies only at R_score = 3 kpc |
| B3 | the same fields for flat, F-DESI, band low, band high; rule `ac1_score.separated` | computed (the scorer prints only flat vs R-H) |
| B4 | the scorer's printed "flat vs R-H" line; the same fields elsewhere | none |
| B5 | `route N|…` entries, record only | no live score |

Known answers against the tex, all PASS: B1 431 (431.42); B2 0.88 and 0.07 (0.879, 0.073); every S1 branch FLOOR; B3 2 (1.65); B4 22 (22.43); B5 9 and 22 (8.77, 22.09); the reader's flat vs R-H call equals the scorer's on 20 MOCK cells. MUTATE (R31 × 10) fails B2 and exits 1.

### A3. Archive metadata (`fn2_archive_meta.py`; raw `a3_*`)
- Release 2026-11-06T02:42:31 UTC; data rights Proprietary today; HEAD on the cube URLs returns 403.
- Science target UDS28473 at AC1's phase centre (0.0″). Seven calibrators share the MOUS.
- Windows: spw23 94.7944–96.6657, spw25 97.5953–98.6216, spw27 106.7520–108.7277, spw29 108.7437–110.6148 GHz.
- Products: one 193.5 GB product tar, a 3.2 GB auxiliary tar, ten raw tars (301 GB). Inside the product tar, individual files are listed with sizes:

| file | bytes | inferred shape |
|---|---|---|
| `member.uid___A001_X3788_Xbfd2.UDS28473_sci.spw25.cube.I.pbcor.fits` (CO(3-2), rows B) | 34,749,031,680 | 4500 × 4500 × 429 |
| `member.uid___A001_X3788_Xbfd2.UDS28473_sci.spw23.cube.I.pbcor.fits` (CO(2-1), row A) | 38,556,031,680 | 4500 × 4500 × 476 |

These replace AC1's estimate of about 115 GB per spw. Coverage (information): AC1's window and its MUTATE (+1000) lie inside spw25. **CFG806's MUTATE window (+2000 ± 500) is only 7 % inside spw23**, so row A's MUTATE can only bite for lack of data; there is no frozen fallback.

### A4. Runbook
`RELEASE_DAY_RUNBOOK.md` gives the commands in order. The download is shown, not run. Cubes stream through `ac1_stream_cutout.py`; only cutouts are kept (0.28–0.83 GB for U4_28473 at ±4.5″; 2.55–7.62 GB for U4_27928 at ±13″; `fn2_runbook_numbers.out`). Outputs go to this lane (`release_2026_11_06/`) and, for row A, where the CFG942 harness puts them by the owner's A-X7 ruling. The result is recorded in a new dated note; no frozen file is edited.

Dry run on MOCK (`fn2_a4_dryrun.out`), 4 of 4 PASS: AC1's cutout test; the runbook's stream-cutout pipe (source SHA-256 and bytes match); `ac1_score.py --cube` on that cutout (G1-3D PASS, V_c 431 ± 1 of 430, 37 s, 0.98 GB, no result file for a MOCK); the reader on MOCK JSONs.

## Part B. GS4_24110 ([CI](2-1), 2025.1.01377.L)
- **Date: DATE CONFIRMED,** 2026-11-28T18:25:24 UTC. MOUS uid://A001/X3845/X3a (new to the record), target "Pointing-F", 0.42″ from GS4_24110, single pointing, 13,941 s, beam 0.089″.
- **Files:** `member.uid___A001_X3845_X3a.Pointing-F_sci.spw31.cube.I.pbcor.fits`, 7,018,934,400 bytes (1920 × 1920 × 476); continuum `…spw25_27_29_31.cont.I.pbcor.fits`, 14,777,280 bytes.
- **Coverage:** spw31 (269.5896–271.4609 GHz) runs from −1615 to +462 km/s about 270.006 GHz. The ±300 G1 window fits. **The frozen MUTATE (+2000) and its fallback (+1000) both lie wholly outside**, so the harness will exit 2 with no MUTATE control (CFG809 addendum A §2).
- **What the frozen plan scores** (CFG809, 966d50a87, owner's governing plan of 10-20; clarification and addenda A–F; harness `cfg942_gs4.py`): G1 ([CI](2-1) S/N ≥ 5 against a selection-aware null); gas size (G3); gas mass by routes never averaged (CI21 primary; CO43, CI10, dust re-quoted); Δ_v at R_e with σ from flux ⊕ 0.2 dex route ⊕ 0.2 dex M★; "consistent" or "in tension" at 2σ; FLOOR rule; ROBUST only if every detected route agrees. Verdict kernel ν_mono (CFG571 seal); n = 1, n = 2 and the v3 AQUAL disc are labelled parallel readings.
- **It cannot separate n = 1 from n = 2:** the largest separation on any branch is 0.51σ (D4, 0.5124; K-B3 PASS).
- **On the date:** the owner's yes for the two files, then the commands in the runbook's §4. Nothing must be filed before. Two optional owner items: a substitute MUTATE control (only by a dated pre-data addendum); and the plan's flat ΛCDM (H0 70, Ωm 0.3) for angular size and D_L, frozen on 10-15, before the owner's 10-25 rule (CFG806 has the same). Flagged only.

## Part C. Gaia DR4
- **Date:** "Gaia DR4 (based on 66 months of data) 2 December 2026", https://www.cosmos.esa.int/web/gaia/release, read 2026-11-04T18:34:30Z (`c1_esa_gaia_release_extract.json`). PROVISIONAL.
- **Which frozen lines could grade the bare law** (`fn2_dr4.out`):

| line | names the bare law | rule against it | kernel behind its numbers |
|---|---|---|---|
| PREREG §1.5 (07-16) | no (n = 2 framework) | z rule on 1.00 / 1.09 / 1.137 / 1.33 | ν = √(1 + 1/y) |
| PREREG Amendments 10–11, Arm A | no ("the frozen kernel") | γ̂ ≤ 1.007 falsifies Arm A, … | Route A, ν = 1/(1 − e^(−√y)) |
| **D2 note (owner-approved 10-22) + A1–A3** | **yes: "the canonical law g_N = g²/(g + a₀) holds at every scale, read with the Galactic external field"** | **law-first excluded iff Arm A floor − γ̂ ≥ 3σ** | rows anchored on Arm A's floor (Route A); A1 and A3 quote n = 1 AQUAL values |
| CW1 seal (df7801238b) | yes (PQ) | none: separation labels only | n = 1 |
| CFG800 / Amendment 22 | no (CFG740 construction) | R rule | — |

- **So a frozen rule exists, and its anchor is not the bare law's own number.** Arm A's floor is 1.1614 (canonical) / 1.1917 (alt). CW1's plain QUMOND with the law's ν, through the frozen pipeline, gives 1.149 ± 0.027 / 1.208 ± 0.007 (reproduced from `cw1.json`). The offsets are 0.43 and 0.59 σ_tot. A3's wording also names A1's AQUAL values (1.167 / 1.199 at the primary g_ext) as the law-first value. FN2c was not opened: a second frozen rule for one hypothesis would make two governing plans.
- **The D2 rows, mechanically** (σ = √(σ_fit² + σ_sys²); the floor at the primary g_ext):

| case | footing | σ | law-first excluded at γ̂ ≤ | medium-first excluded at γ̂ ≥ |
|---|---|---|---|---|
| registered: σ_fit 0.019, σ_sys 0.020 | canonical | 0.0276 | 1.0786 | 1.0828 |
| registered | alt | 0.0276 | 1.1089 | 1.1089 |
| DR3 definition (b): σ_sys 0.0375 / 0.041 (non-scoring) | canonical | 0.0420 | 1.0353 | 1.1261 |
| same | alt | 0.0452 | 1.0561 | 1.1356 |

Under every row, a Newtonian 1.000 reads "law-first EXCLUDED" and CW1's plain-QUMOND value reads "medium-first EXCLUDED". A3 still requires σ_sys (b), measured on DR4, with (a), (e) and (g2) agreeing at ≥ 3σ; otherwise UNDECIDED.
- **AQUAL engine:** the record has one. E2 (`doors_push_2026_10_22/E2_field_equation/aqual_axi.py`, `aqual_fft.py`) gives 1.167 / 1.199 for a 1 + 1 M☉ binary at 20 kAU; it has not been run through the frozen pipeline. Amendment 10's solver is hard-wired to the Route A ν.
- **Drafts marked NOT FILED** (Amendments 9, 12, 15–22): all 10 are filed in the prereg, each with its hash file; the hash chain ends at the current prereg (K-C3 PASS). The file names are stale. Rows changed by the filed text: Amendment 9 (MG target, no-verdict edge 1.20 → 1.26; superseded by Amendment 10) and Amendment 12 (Arm B's kill threshold ≥ 1.129 → ≥ 1.084). Amendments 15–22 change no decision row, by their own text.
- Known answers 7 of 7 PASS (prereg, pipeline, seal and D2 hashes; CW1 PQ; Arm A floors in text and code; D2 ceilings). MUTATE (one prereg byte flipped, CW1's LOC3 read as PQ) fails both and exits 1.

## Failed checks (kept)
1. **K-A3, run 1, FAILED as implemented.** It compared all 32 ObsCore rows, seven calibrators included, so the phase-centre and window checks failed. Run 2 uses the science target's rows (UDS28473, as AC1's criteria name it): both PASS. A 1e-9 float guard added to the 0.01 GHz check changes nothing (the windows equal PAPER66's exactly). Run 1's outputs: `fn2_archive_meta_run1_KA3_FAILED.*`.
2. **A1, default environment:** ENV OK, NUMBERS DRIFT, not ENV OK (see A1).
3. **Peak RSS 1.05 GB** in the default-environment selftest, above 1 GB.

## What needs the owner
1. ALMA: yes to stream `…spw25.cube.I.pbcor.fits` (34,749,031,680 bytes) and `…spw23.cube.I.pbcor.fits` (38,556,031,680 bytes) from almascience.eso.org/dataPortal, keeping only the cutouts.
2. GS4: yes to the spw31 cube (7,018,934,400 bytes) and the continuum (14,777,280 bytes). Optional: a substitute MUTATE, by a dated pre-data addendum.
3. DR4: optional dated clarification, before 2 December, of the D2 law-first anchor (Arm A's floor, A1's AQUAL value, or the bare law's own pipeline value).
4. Note only: row A's MUTATE is hollow on spw23; CFG806 and CFG809 use flat ΛCDM for angular size.

## Files
Scripts: `fn2_a1_env.py`, `fn2_scorecard.py`, `fn2_archive_meta.py`, `fn2_a4_dryrun.py`, `fn2_runbook_numbers.py`, `fn2_dr4.py`. Outputs: their `.out` and `.json`, `_MUTATE` twins, `a1_selftest_default/`, `a1_selftest_pinned/`, raw metadata `a3_*`, `b2_*`, `c1_*`. Runbook: `RELEASE_DAY_RUNBOOK.md`.
