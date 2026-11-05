# Release-day runbook: Gaia DR4 wide binaries (DR4 due 2026-12-02 per ESA, provisional)

Lane DP3 (criteria `FROZEN_CRITERIA.md`, d66d012f57). Modelled on `finish_2026_11_04/FN2_dated_tests/RELEASE_DAY_RUNBOOK.md`.
κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. It edits no frozen file
and implements the record as filed: `PREREGISTRATION_DR4.md` + 22 amendments, `RELEASE_DAY_CHECKLIST.md` (§1-7), CFG943 README §5/§7,
the D2 note and A1-A3, the 10-21 kill-line note, and the two owner decisions of 2026-11-05 (413c1c8e24 D1-D6; d71a111d1d D7-D8).

**Nothing below queries the archive, logs in, or runs CFG825's once-only `--dr4` until the owner says yes in chat, naming the
step, the table, the size and the time.** The session then writes `GO <step>` into `OWNER_APPROVAL_DR4.md` in this folder; the
wrapper `dr4_release_day.sh --run` refuses every gated step without that line (exit 10, the log says which step and what it costs).
Every command runs from the repo root. Wrapper modes: `--check` (no data), `--run` (resumable: done steps leave
`release_2026_12_02/.done_<step>`), `--dry-run-dr3` (the same chain on DR3, offline).

## 0. Before release day (and again on the morning)

```
bash dr4_push_2026_11_05/DP3_release_day/dr4_release_day.sh --check
```
- 27 pinned sha256 (the four checklist §3 files incl. `wide_binary_pipeline.py` 7c884e0e..., the prereg = Amendment 22's "after"
  digest 20677265..., both 11-05 owner decisions, the D2 note, the kill-line note, CFG825's four files, the dr4_ready_1 tools and
  the manifest template, the D2 σ_sys recipe). Any mismatch: stop and find out why (exit 6 in `--run`).
- CFG825's once-only slot `campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/cfg816_r_dr4_results.json` must be absent.
- Guard: free disk ≥ 20 GB; no 1024³ run; **no python job > 2 GB live** (the frozen pipeline peaked 3.95 GB on DR3 in this lane's dry run, CFG943 N11 said ~3 GB; DP1's rung
  build peaked 4.25 GB on DR3). `--run` refuses otherwise (exit 5).
- Availability: by date (before 2026-12-02 it prints "DR4 not yet available"). `DP3_PROBE=1` adds one HTTP HEAD to the public ESA
  archive GDR4 documentation page (information only). The real availability test is the schema probe of step G7.
- DP1 state (NSS-off rung): read from `dr4_push_2026_11_05/DP1_nss_off_rung/dr3_check.json` (REPRODUCED on 2026-11-05, f732b84221).
- Owner items that must exist before the data are opened (none may be decided after): the approval file; the decisions already
  filed (D1-D8); the open issues O1-O3 below.

Rehearsal: `DP3_ALLOW_LIVE_JOBS=1 bash dr4_push_2026_11_05/DP3_release_day/dr4_release_day.sh --dry-run-dr3` (results in §4).

## 1. The ordered list (G = needs `GO <step>`; O = offline, no yes needed)

| step | command (wrapper runs it) | size / time (record) | yes |
|---|---|---|---|
| R0 | self-tests: `dry_run_driver.py --self-test`, `amdt14_distances.py --self-test`, `arm_c_rows.py --self-test`, `make_pair_table.py --self-test`, `dr4_outcome_map.py --self-test` | ~1 min | no |
| G1 | save the published DR4 data model (URL, UTC, sha256) in `release_2026_12_02/datamodel/`; write `spec_dr4.json` (renames only; `--spec-json`, never a code edit) and `manifest_dr4.json` from `prep_2026/gaia_dr4_prep/dr4_ready_1/manifest_template_dr4.json` (every null filled; cut 12 counted tables per Amendment 17; cut 9 = SFD98 per Amendment 16(a)) | one page / PDF, a few MB; ~1 h of reading | **yes (download)** |
| G2 | registered Gaia archive account: the owner logs in himself; this lane never handles a password. `SKIP G2` = anonymous | — | **yes (account)** |
| G3 | `caffeinate -i python3 -B prep_2026/gaia_dr4_prep/catalog_builder/fetch_extract.py --release dr4` (12 async jobs + Σ₁₈ map) | DR3: 4,582,547 rows, ~400 MB, 6,461 s. DR4 central ×1.54: ~7 M rows, ~620 MB, ~2.8 h | **yes (archive)** |
| G4 | `python3 -B prep_2026/gaia_dr4_prep/catalog_builder/build_catalog.py --release dr4` (stages A-F cached; its own stage G is information only and fetches correlations) | DR3: 16 min on 16 cores; stage A ~0.5 GB | **yes (archive, stage G)** |
| G5 | cut 12 + joins: the ADQL of `cut12_nss_union.adql_nss(table, two_source)` for the 6 Amendment 17 counted tables (`nss_acceleration_astro`, `nss_multiple_orbits`, `nss_non_linear_spectro`, `nss_resolved_pair` (both id columns), `nss_two_body_orbit`, `nss_vim_fl`) and the `all_source_flags.non_single_star` join file; record table, solution types, row counts in the manifest | uploads of the sample ids, < 10 MB | **yes (archive, each table)** |
| G6 | `python3 -B prep_2026/gaia_dr4_prep/dr4_ready_1/dry_run_driver.py --release dr4 --manifest M --allow-network --cut13 extract-builder --dump-candidates C.csv`; then `dr4_q1_estimate.py --pairs-csv C.csv` (the pre-brief, read to the owner), `q1_cones_dr4.py --print-count-queries`, `q1_cones_dr4.py --spec dr4_all_source --spec-json S --stage-a <dr4_extract>/stage_A.npz --pairs-csv C.csv ... --plan-only` | ~49,000 candidates at N 30,000 (DR3 ratio 1.65) | **yes (correlations)** |
| G7 | the Q1 neighbour-cone fetch (cut 13 primary, Amendment 16(b)): `caffeinate -i python3 -B .../q1_cones_dr4.py --spec dr4_all_source ... --cap-accepted-mb A --cap-received-mb R --max-queries Q --owner-go-recorded "<text>"` (resumable). The GO line carries the caps. Optional tables (`gaia_source_environment`, `crowded_field_source`) only if the owner decides, recorded in the neighbours manifest. A sharded parallel fetch (lane DP4) is an alternative only if its README says it passed and the owner says yes | central ~39,000 queries, ~1.7 GB accepted (2.1 GB received), **~47 h serial** at the DR3 pace (low/high 25k/64k queries, 31/77 h; a 2× slower archive doubles it). Suggested caps (1.5× central): 2,540 MB / 3,100 MB / 58,900 | **yes (archive, caps)** |
| G8 | **primary build:** `dry_run_driver.py --release dr4 --manifest M --allow-network --cut13 cones-literal --neighbours-manifest NM --out-csv wide_binaries_dr4.csv` (`--cut13 cones-literal` passed explicitly, D7 N9; never the default `extract-literal`); `--corr-transport sync` only if async fails, recorded (Amendment 19) | stage-G correlations; minutes | **yes (archive)** |
| O9 | `python3 -B prep_2026/gaia_dr4_prep/wide_binary_pipeline.py --catalog wide_binaries_dr4.csv > pipeline_dr4.log`, then `amdt14_distances.py --log` and `arm_c_rows.py --log` | 3.95 GB peak on DR3 (measured 2026-11-05), ~35 s on DR3; more on DR4 | no |
| G10 | Amendment 18: `seed_sweep.py --release dr4 --mode g-only --K 50 --cut13 extract-builder --fit --ladder --allow-network --tag dr4_g50` (extract-builder mode, recorded, D7 N9), then `seed_label.py --evaluate <manifest>` | ~100 pipeline fits, ~1-2 h, one job; delta correlation fetches | **yes (archive)** |
| G11 | NSS-off rung (D7 N4): only if DP1 reads REPRODUCED: `python3 -B dr4_push_2026_11_05/DP1_nss_off_rung/nss_off_rung.py --release dr4 --manifest M --cut13 cones-literal --neighbours-manifest NM --allow-network --out-csv nss_off_rung_dr4.csv`; otherwise the wrapper prints NOT IMPLEMENTED and σ_sys(b) is computed without it, stated | DR3 peak 4.25 GB | **yes (archive)** |
| O12 | `dp3_sigma_sys.py --base wide_binaries_dr4.csv --nss-off nss_off_rung_dr4.csv --seed-manifest <G10 manifest> --out-json sigma_sys_dr4.json` (σ_sys (a), (b), (e), (g2) by the D2 lane's recipe); `make_pair_table.py --catalogue wide_binaries_dr4.csv --per-star <dr4_extract>/stage_A.npz --out pairs_dr4.csv --declare-neutral non_single_star` (R input = the registered catalogue, D7 N5) | ~1 GB, minutes | no |
| G14 | **ONCE ONLY:** `python3 -B campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/cfg816_r.py --dr4 pairs_dr4.csv`. It writes `cfg816_r_dr4_results.json` and refuses a second run; any later change is a Departure. The CFG825 variant catalogue (`build_variant_catalogue.py --release dr4 ...`) is information only, no verdict weight | seconds (B = 2,000) | **yes (once)** |
| O15 | **final scoring:** `python3 -B dr4_push_2026_11_05/DP3_release_day/dr4_outcome_map.py --pipeline-log pipeline_dr4.log --sigma-json sigma_sys_dr4.json --r-json campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/cfg816_r_dr4_results.json --tag "DR4 <date>" --out outcome_map_dr4.out --json-out outcome_map_dr4.json` | seconds | no |

Paths in the table are relative to `release_2026_12_02/` of this lane for M, S, NM, C.csv and the outputs; the DR4 extract is
`real_research/data/widebinaries/dr4_extract/` (git-ignored). Variants run beside the primary and are never substituted:
`--cut13 cones-orbit`, `--variant allsource_15c`, V17a / V17b, the `ap_*` A_V route.

## 2. What the final scoring step prints (and what the words mean)

Per footing, never pooled (`dr4_outcome_map.py`, frozen order):
1. **GUARD_ZONE** γ̂ > 1.23: no verdict for every reading (never survival).
2. **SUB_NEWTON_NO_VERDICT** γ̂ ≤ 1 − 3σ: pipeline or contamination fault; no verdict for every reading (D4).
3. **UNDECIDED_GATE** σ_sys(b) ≥ 0.048 canonical / 0.058 alt (D2 A1).
4. D2 rows under (b), σ = √(σ_fit² + σ_sys(b)²), anchor = Arm A floor 1.1614 / 1.1917 (D2(a)), Newton 1.000 (D3(a)):
   **LAW_FIRST_EXCLUDED** (anchor − γ̂ ≥ 3σ) → "Newton side: **v3s survives** (not confirmed); bare law excluded";
   **SCREENED_EXCLUDED** (γ̂ − 1 ≥ 3σ, not below the anchor by 3σ) → "v3s EXCLUDED (screened reading); bare law survives this test";
   **BOTH_EXCLUDED** (both, the alt overlap 1.083-1.109 at N 30k, D5) → neither reading fits;
   **UNDECIDED** otherwise.
5. A3.2 robustness: (a) 0.020, (e) jackknife, (g2) √(0.020² + σ_build²) must give the identical label, else **UNDECIDED_ROBUSTNESS**.

Beside it, information only: each frozen g_ext (primary 1.778e-10, alternative 2.078e-10) with A3's AQUAL anchor (1.167 / 1.145
canonical, 1.199 / 1.173 alt) and a printed "information split" if that reading differs; CW1 (1.149 / 1.208), D2 §4, FN6. The edges,
both distances, every σ. **R** per the kill line: KILLED iff R − 1 ≥ max(0.01, 3σ_R), σ_R from N_R (N1); UNDECIDED is neither a
kill nor a survival; CONSISTENT is unreachable; the size a kill needs is printed (~1.22 at N_R ~2,100). **Splits** are printed as
splits, never merged: canonical vs alt, γ̂ rows vs R (N6). Fixed lines: the NSS-off rung status (D7 N4.1), N4.3 (~40 %
false-failure rate of the 3-20 kAU rung beside any systematic-limited reading), N7 (CFG740 falsifier 1 beyond ~37 kAU and falsifier
2 not scored), D8 (mock-triple injection information only).

Map at the registered error (N 30,000, σ_sys 0.020; 413c1c8e24 §2a-c), reproduced by the scorer's self-test (20/20):
canonical ≤ 0.917 sub-Newton, 0.917-1.079 law-first excluded (v3s survives), 1.079-1.083 UNDECIDED, 1.083-1.23 screened
excluded, > 1.23 guard. Alt: 1.083-1.109 BOTH EXCLUDED. With N 6,210 and σ_sys 0.0375 a Newtonian sky (1.00) reads UNDECIDED.

## 3. Recording the result (never editing a frozen file)
1. `release_2026_12_02/` keeps every `.out`, manifest and JSON (`*.log` is git-ignored; the fit lines are copied to
   `pipeline_dr4_fitlines.out`). The DR4 extract and cone FITS stay in the git-ignored data folder.
2. Write `RESULT_2026-12-02.md`: per footing the label line verbatim, raw γ̂, σ_fit, every σ_sys, both distances, R block, splits,
   the NSS-off status, the A14/A20/Arm C lines, σ_build and the seed label. No verdict word beyond the filed labels; "v3s survives",
   never "confirmed". The `[aniso]` split is quoted only where Amendment 20 calls it measurable.
3. `grep -rl "$HOME" dr4_push_2026_11_05/DP3_release_day` must print nothing. Commit with explicit paths only
   (`git commit -m "..." -- <paths>`); never `git add -A`. A PAPER67 addendum and any deposit are the owner's act.

## 4. Rehearsals on record (2026-11-05)

See `DRY_RUN_2026-11-05.md` in this folder for the `--check`, `--run` (refused) and `--dry-run-dr3` outcomes.

## 5. Open issues (need the owner before 2026-12-02; none can be decided after the data)

- **O1 (blocking for G3).** The frozen `fetch_extract.py` (d826f688) SELECTs `non_single_star` from `gaiadr4.gaia_source`; the
  draft data model puts it only in `all_source_flags`, so the stage-A query would fail as written. The script has no `--spec-json`.
  Options: a names-only edit checked by the checklist §3 diff rule (conflicts with "renames only via --spec-json"), or a new
  wrapper that imports it read-only and takes the column list from the spec JSON, with a DR3 equivalence test, filed pre-data.
- **O2.** No DR4 fetch tool exists for the cut-12 NSS id files or the `all_source_flags` join file; G5 is the ADQL text of
  `cut12_nss_union.adql_nss()` run by hand after the yes. `all_source_rvs` likewise, if RVs are not in `gaia_source`.
- **O3.** None of the tools logs in: `fetch_extract.py` / `build_catalog.py` use anonymous `astroquery.gaia`, the cone fetch its
  own TAP client. A registered account's quota helps only if a login hook is added (new code, tested, before release).
- **O4.** σ_sys(g2) needs σ_build from the DR4 K 50 sweep; without a manifest `dp3_sigma_sys.py` uses the DR3 bound 0.44 × 0.019
  and says PLACEHOLDER. `dp3_sigma_sys.py` follows the D2 lane's recipe (1,000,000-pair master, boot 200), as A3 requires; the
  γ̂ and σ_fit in the rows come from the frozen pipeline's own `--catalog` log.
- **O5.** DP1's rung peaked 4.25 GB on DR3 and the frozen pipeline 3.95 GB; on DR4 both grow. Run each alone (the guard refuses
  `--run` while any other python job > 2 GB is live).
- **O6 (owner decision, pre-data).** Which rungs enter σ_sys(b)'s "frozen robustness ladder" on DR4. The D2 recipe (A2) used
  R_chance < 0.001, 3-20 kAU and the NSS-off probe, declaring RUWE 1.4 → 1.2 and RV-screened unimplementable on DR3; yet
  `seed_sweep.py --ladder` does implement RUWE < 1.2 by a stage-A lookup. `dp3_sigma_sys.py --stage-a <stage_A.npz>` adds that
  rung (off by default = the D2 recipe). On DR3 (information) it leaves canonical (b) at 0.0375 and moves alt from 0.0412 to 0.0350.
  The RV-screened rung has no implementation anywhere.
- **O7 (finding).** σ_sys(b) in the D2 recipe is sensitive to the bootstrap RNG stream: adding one fit before the alt footing
  moved the DR3 alt NSS-off shift from +0.0575 to +0.0375 (same data). DP1 found the same in builds (8-reseed mean +0.010 / +0.006).
  As frozen (D8 (a)) the single-stream value is binding; this is reported, not repaired.
