# DP8 frozen criteria: wire the owner decision of 2026-11-15b into the Gaia DR4 release-day path (pre-data, DR3 only)

Frozen 2026-11-15, before any code, edit or number of this lane exists. Committed alone.

kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

Authority: `prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-15b_DR4_OPEN_GAPS.md` (sha256 dad0d100...; owner's words
"Accept all recommended"), with `OWNER_DECISION_2026-11-15_DR4_FORM_B_READING.md` (3641f7de...) and the three notes of
2026-11-05 (05, 05b, 05c; 05c filed 2026-11-08). The gaps are C3 to C12 of
`closure_2026_11_12/DR4MAP_gaia_dr4_registry_map/DR4_MAP.md`. This lane is the fix lane that 11-15b section 1 (Q1, Q2)
and section 2 (Q8) commission. Every DR3 number it prints is a code-path test, never a result (Amendment 7(e)).

## 0. Scope

Edited outside this folder, committed separately from the lane folder:
- `dr4_push_2026_11_05/DP3_release_day/dr4_release_day.sh` (the wrapper);
- `dr4_push_2026_11_05/DP3_release_day/RELEASE_DAY_RUNBOOK_DR4.md` (the runbook, which carries the result template);
- `dr4_push_2026_11_05/DP3_release_day/dp3_sigma_sys.py` (text only: help strings, docstring, output notes).

New, in this folder: `dp8_seed_mean_release.py` (Q1 launcher), `dp8_fallback_count.py` (Q2), `dp8_sepbins.py` (Q8),
the check runner and its outputs, `dp8_checks.json` (machine-readable check states that the wrapper reads), RESULT.md.

Not edited (run or imported read-only): every frozen file (PREREGISTRATION_DR4.md and its amendments, every
OWNER_DECISION_*.md, the D2 note, CQ2's seal, CFG816's criteria and scripts, the 28 files pinned in the wrapper's HASHES
block today), `dp7_seed_mean.py`, `nss_off_rung.py`, `dp6_with_a17.py`, `XR22_prereg_statistic.py`, DP7's committed outputs.

**Finding recorded before any code (from reading only).** `dp7_seed_mean.py` installs a socket guard at import and its
`main()` exits on `--allow-network` ("DR4 path: not run in DP7"). The DR4 command of DP7 RESULT section 7 therefore
cannot run as written. Q1's step runs `dp7_seed_mean.py` through a new launcher, `dp8_seed_mean_release.py`, which imports
it read-only and (a) on DR3 passes every argument through unchanged, with outputs redirected to a folder it is given;
(b) on DR4 lifts the refusal and the import-time socket guard only when `--release dr4 --allow-network` and an
`--owner-go-recorded` text beginning "GO G11S" are all given, else exits 2; (c) changes nothing else. Like G10 and G11,
the step runs under `dp6_with_a17.py` (A17 cut 12; runbook O8). Its DR4 network path cannot be tested here (no network,
no DR4 byte); that is a disclosure, not a check.

## 1. What is changed, item by item (Q numbers are the decision's)

- **Q1.** A new gated step **G11S** after G11: `dp6_with_a17.py --a17-manifest M -- dp8_seed_mean_release.py --release
  dr4 --manifest M --neighbours-manifest NM --cut13 cones-literal --fit-path pipeline --K 50 --rung-missing-cones
  extract-fallback --allow-network --out dp7_dr4 --out-dir <release folder>/G11S_seed_mean --owner-go-recorded "<GO line>"`.
  It needs `GO G11S` in the approval file (exit 10 otherwise), runs only when G11 built the rung, and refuses (exit 7)
  unless `dp8_checks.json` records the launcher's DR3 check (C7) as PASS. Step **O12** passes `--nss-off-seed-mean
  <G11S json>` to `dp3_sigma_sys.py`. If G11 built the rung but the G11S output is absent, incomplete, or not
  (release dr4, K 50, cones-literal, rung missing cones extract-fallback), O12 stops with exit 7 and prints
  "NEEDS OWNER (decision 2026-11-15b section 4)"; it never falls back to the single-seed entry. If DP1 is not
  REPRODUCED (no rung), G11S and the option are skipped as G11 is, and the report says so. The text of
  `dp3_sigma_sys.py` that says the 11-05c draft is "NOT FILED", or calls the seed-mean entry "information only, DR3",
  or calls `--stage-a` an open owner decision, is corrected (filed 2026-11-08; Q5 decided). Text only.
- **Q2.** G11 passes `--missing-cones extract-fallback` to `nss_off_rung.py`; G11S passes `--rung-missing-cones
  extract-fallback` (both flag names as the tools spell them). `dp8_fallback_count.py` writes the number of rung pairs
  that reached cut 13 without a cone, the policy, and the number the fallback flagged, for G11's rung and for the
  sweep's k = 0 rung, to `nss_off_fallback_counts.json` and the log; the result template has a line for it.
- **Q5.** O12's main call (the one whose (b) the outcome map reads) carries exactly the D2 recipe's three entries:
  R_chance < 0.001, 3-20 kAU, and the NSS-off entry (seed-mean under Q1). A second call **O12r** adds `--stage-a`
  (RUWE < 1.2) and writes `sigma_sys_dr4_ruwe_info.json`, information only; nothing reads it for (b); its failure is
  logged and does not stop the chain.
- **Q8.** A step **O16** after O15 (the label step) runs `dp8_sepbins.py --catalog <primary catalogue>`, Amendment
  14(c)'s statistic as coded in XR22's `sepbins`, report-only, and writes `sepbins_dr4.json`. It runs only if
  `dp8_checks.json` records the Q8 code-path check (C5) as PASS; otherwise, or if it fails at run time, the wrapper
  prints "Amendment 14(c) separation-resolved statistic: NOT RUN" with the reason and continues. It reads no label
  output and cannot change a label. The data-side definition: r_b = median(vtilde, catalogue) / median(vtilde, the
  frozen Newtonian model population) - 1 in s_proj bins [2, 3, 5, 7, 10, 15, 20, 30] kAU, both with the estimator's
  vtilde < VTCAP; sigma_b from a bootstrap over catalogue pairs (boot 100, rng seed 5); the model population is
  `make_population(1,500,000, default_rng(20261216), dr4=True)` as XR22's registered estimator builds it; catalogue
  vtilde by the frozen pipeline's own `ingest_csv`. vtilde and s_proj carry no a0, so the table is footing-free (one
  table, not a pooled one). The xi reading of 14(c) (a fit to XR22's committed r_b^chain(xi)) is not computed here.
- **Q3, Q4, Q7, Q9, Q10, T3 (runbook text and result template only).** The R label quoted is CFG816's own, with the
  scorer's word beside it in the same sentence where they differ; each footing has its own verdict line and a split
  has no headline; the September ridge rows (matrix row 1 / G088 / G165 / Z03, G018, E6 / E7) are information rows and
  `dr4_scorer.py` is not run; no Milky Way row is scored for the adopted theory; `crowded_field_source` and
  `gaia_source_environment` are not searched, and the manifest records their counts and this choice before the data
  are opened; access stays anonymous (`SKIP G2`). Runbook section 5: O3 (account), O6 (ladder) and the cone-coverage
  item marked decided with a pointer to 11-15b. The wrapper's STOP texts for G1, G2 and G7 quote the same choices.
- **Pins.** The sha256 of the two decision files of 2026-11-15 are added to the wrapper's HASHES block (28 -> 30) and
  `$PREP/OWNER_DECISION_2026-11-15*.md` to its prereg-directory cleanliness check, as f704278a77 did for 11-05c.
- **Dry run (`--dry-run-dr3`) gains:** D5b (the DR3 rung in cones-literal with the fallback, and its count), D5c (the
  G11S launcher's refusals on DR3), D6c (sigma_sys with the seed-mean entry on the release-day path), D6d (the RUWE
  information call), D9 (the sepbins step after D8). Existing D steps are unchanged.
- **No test hook in the real wrapper.** Checks that need another output folder, approval file, date or disk threshold
  use a generated copy, `dr4_release_day_TESTCOPY.sh` in this folder (not committed), whose `diff` against the real
  file is committed and must touch only: the three OUT lines, the APPROVAL line, the RELEASE_DATE line and the 20 GB
  disk threshold (each made an environment default whose unset value equals the real one, except OUT and APPROVAL,
  which point into this folder). Reason for the disk line: 17 GiB free at freeze time; the dry run writes < 1 GB.

## 2. Checks (each with a mutation twin written to a separate output; all offline, DR3 only)

- **C1 pins.** Real wrapper `--check`: the log has "hashes: all 30 pinned files OK" and "SUMMARY hashes OK".
  Control: a scratch mirror (copies of the 30 pinned files and DP1's state files, `git init` and one commit, the real
  wrapper copied unchanged) gives "SUMMARY hashes OK". MUTATE C1a / C1b: one byte appended to the mirror's copy of
  11-15b / of 11-15 -> a HASH MISMATCH line naming that file, "prereg directory NOT clean", "SUMMARY hashes FAIL".
  The real files are never touched; their sha256 are recorded before and after the lane, equal.
- **C2 seed-mean entry.** `dp3_sigma_sys.py --base <registered DR3 catalogue> --nss-off <DP1 DR3 rung> --seed-manifest
  <committed G50 manifest> --nss-off-seed-mean <DP7 dp7.json>` (DP7's committed K = 50 sweep reused, not re-run), in
  the dry run (D6c) and standalone: every numeric leaf equals DP7's `dp3_seedmean_releasepath.json` exactly (max |diff|
  0, both footings); string leaves may differ only by the corrected text, listed. MUTATE C2: the same call without the
  option -> (b) equals the reference's `b_single_seed` (0.0225 / 0.0287) and the C2 comparison fails. Text-only proof:
  the ASTs of `dp3_sigma_sys.py` before (HEAD) and after, with every string constant blanked, are identical, and the
  option-off run equals DP7's `dp3_d6_replay.json` in every leaf; MUTATE: a copy with one numeric constant changed
  fails the AST comparison.
- **C3 dry run.** The test copy's `--dry-run-dr3` (outputs in this folder): every D step that
  `DRY_RUN_2026-11-05.md` / DP3's committed `release_day_dryrun.out` reads PASS still reads PASS with the same numbers
  (D2 6,210 / 6fff64d964ebaa72 and 6,180 / c5cb89e8f95bfe3d; D3 canonical 1.0750; D6 shifts and (b) 0.0375 / 0.0412;
  D6b 0.0225 / 0.0287; D7 R 0.972839, N_R 348; D8 the same labels), and every new D step PASS. `dr4_outcome_map.py
  --self-test` 20/20, exit 0; its DP3_MUTATE=1 / 2 twins still exit 1 (13/20, 19/20). MUTATE C3: the comparator, fed
  DP3's committed dry-run log with one PASS line turned into FAIL, reports a failure.
- **C4 RUWE information call.** On the C2 inputs: the main call's JSON bytes (sha256) are the same before and after
  the RUWE call, a fresh main call after it is byte-identical, and the RUWE call writes only its own file. MUTATE C4:
  `--stage-a` given to the main call itself -> the main JSON differs (bytes, and (b) / (e) reported).
- **C5 sepbins (the Q8 code-path check).** (i) `dp8_sepbins.py --self-test`: XR22's own `sepbins` (source taken from
  `XR22_prereg_statistic.py` by `ast`, executed unedited) and DP8's data-side function give bit-identical rows (n,
  ratio, sig_med, frac, all 7 bins) when the data are the model population's own Newtonian vtilde (B = 1), and DP8's
  bin edges equal XR22's SEPBINS; (ii) the run on the registered DR3 catalogue completes with finite r_b and sigma_b
  in all 7 bins and two runs are byte-identical; (iii) the dry run's D9 output (after D8) is byte-identical to a
  standalone run before any label step. MUTATE C5a: `DP8_MUTATE=edges` (the 5 kAU edge moved to 6) fails (i); C5b:
  the catalogue minus its last row gives different bytes in (iii). PASS of (i)-(iii) is written as
  `q8_code_path_check: PASS` in `dp8_checks.json`.
- **C6 refusals and network.** (a) Real wrapper `--run` today: exit 3, before any step. (b) Test copy, release date
  moved to 2026-11-01, an approval file in this folder with no GO line, R0 marked done: STOP at G1, exit 10.
  (c) Markers R0..G11 and GO lines for every gated step except G11S: STOP at G11S, exit 10. MUTATE C6: (c) plus
  "GO G11S": the log shows the GO on record and the step then fails offline on its missing DR4 inputs (exit 7).
  (d) Launcher refusals (exit 2): `--allow-network` on DR3; DR4 without a "GO G11S" text; DR4 without
  `--allow-network`. (e) Every command of this lane runs under `sandbox-exec` with outbound IP connections denied, on
  top of the python socket guards; control: a python connect to 192.0.2.1:443 under the same profile is denied.
- **C7 launcher equivalence (Q1's new code) and the fallback count (Q2).** (a) DR3 pass-through, `--cut13
  cones-literal --fit-path pipeline --K 2 --rung-missing-cones extract-fallback --no-fit-cache`: for k = 0, 1, 2 the
  base and rung n_pairs and sha256, and per footing base, rung, delta, sigma_fit_base, sigma_fit_rung are
  bit-identical to DP7's committed `parts/dp7_k00..k02.json`. MUTATE C7a: `--keep-nss` -> rung sha equals base sha,
  deltas 0, the comparison fails. (b) `dp8_fallback_count.py` on D5b's DR3 rung manifest and on DP7's `dp7.json`
  reports 139 uncovered pairs, policy extract-fallback, 0 flagged by the fallback (= DP7's bias_bound). MUTATE C7b:
  the DR3 rung built with `--missing-cones error` exits non-zero (ConeCoverageError), and the count helper on a
  manifest whose policy is not extract-fallback exits non-zero. PASS of (a) is written as `q1_launcher_check: PASS`.

## 3. Labels (one per item in RESULT.md)

WIRED: code and runbook changed and every check the item depends on passed (Q1: C1, C2, C3, C6, C7a; Q2: C3's D5b,
C7b; Q5: C4; Q8: C5; pins: C1). WIRED TEXT ONLY: Q3, Q4, Q7, Q9, Q10, T3 and the O3 / O6 / cone-coverage marks.
NOT WIRED: the item's check failed or it could not be done; for Q8 the wrapper then prints NOT RUN (the decision's own
fallback). NEEDS OWNER: a choice the owner has not made. Pre-identified: decision section 4 (what happens if G11S cannot
run on the day while G11 built the rung, or if this lane's DR3 check fails for Q1 / Q2). This lane does not decide it;
the wrapper stops there with exit 7 and the words "NEEDS OWNER".

## 4. Rules

One heavy python job at a time (`ps -axo rss,command` before any step above 2 GB), `OMP_NUM_THREADS=1`, `nice -n 10`;
each heavy stage under `/usr/bin/time -l`; compute is quoted only from a tally of these stage logs. No network, no
archive query, no DR4 byte. Commit with explicit paths only; nothing pushed. No home-directory path or personal detail
in any committed file. A fail is reported as a fail; nothing above is changed after a number of this lane exists
(a change goes in a dated AMENDMENT section committed before the affected run, and is disclosed).
