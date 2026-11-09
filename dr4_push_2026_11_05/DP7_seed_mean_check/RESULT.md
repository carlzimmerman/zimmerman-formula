# DP7 — the DR3 code-path check for the seed-mean NSS-off entry: **CHECK PASSED**

Criteria: `FROZEN_CRITERIA.md` frozen at 1b87706e49, plus AMENDMENT_A1 (committed alone before the graded sweep, f78c3dd35c; the
orchestrator's decision "AMEND, do not fail"). Owner's words 2026-11-08: "Yes, check and file". Grader: `dp7_grade.py` ->
`dp7_grade.out` / `dp7_grade.json`. Run date 2026-11-08.

**NON-SCORING.** Every number here is a DR3 code-path test, never a result (Amendment 7(e)). kappa = 1/2 is FITTED. The two footings
(canonical, alt) are reported separately and never pooled. Nothing here is a verdict about gravity; not theory closed.

Filing the draft amendment (`prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-05c_DR4_SEED_MEAN_NSS_OFF_DRAFT.md`, section 4) is the
orchestrator's act on this label, not this lane's.

## 1. Label and the information-only reading

Label rule (section 6): K1-K6 pass, M1 and M2 bite, the K = 50 cones-literal pipeline-fit sweep completes on both footings, and the
section-4 hook reproduces D6 with the option off. All ten required checks pass -> **CHECK PASSED**.

Information only, DR3 (the quantity the DR4 amendment would use, measured on DR3 by the registered fit path, frozen pipeline
`--catalog`, seed 20261216, cones-literal cut 13, K = 50 stage-G seed offsets):

| footing   | Delta_bar | SE     | SD (K = 50) | single-seed shift Delta_0 | gamma_hat_0 (base, k = 0) | seed-mean NSS-off entry | single-seed entry |
|-----------|-----------|--------|-------------|---------------------------|---------------------------|-------------------------|-------------------|
| canonical | +0.0123   | 0.0034 | 0.0241      | +0.0000                   | 1.1375 +- 0.0575          | 1.1499                  | 1.1375            |
| alt       | +0.0147   | 0.0033 | 0.0235      | -0.0100                   | 1.0875 +- 0.0537          | 1.1021                  | 1.0775            |

Delta_bar = mean_k [gamma_hat(rung_k) - gamma_hat(base_k)], k = 0..50 (K = 50 offsets plus k = 0); SD with ddof 1; SE = SD / sqrt(51).
The pipeline's gamma grid step is 0.0025, so every Delta_k is a multiple of 0.0025. N4.2 applied to Delta_bar: |shift| < 1 sigma_fit on
both footings (the same reading the single-seed shift gives). Per-k numbers: `dp7.out`, `parts/dp7_k00..k50.json`.

## 2. Every check, with numbers

| id | result | what was checked |
|----|--------|------------------|
| K1 | PASS | `--cut13 extract-builder --fit-path d2 --K 8` reproduces DP1 P4 bit for bit: 72/72 per-k values identical; mean rung shift canonical +0.0040625 (SD 0.030965), alt +0.000625 (SD 0.014745), all exact. Commit 7130904ecf. |
| K2 | PASS | registered pipeline fit at k = 0 on the extract-builder base (6,210 pairs, sha 6fff64d9) and rung (6,282, sha 1dbdf21a) = DP1 P3 exactly: base 1.0750 +- 0.0550 / 1.0775 +- 0.0512, rung 1.1425 +- 0.0637 / 1.1025 +- 0.0525; max diff 0. Commit 010c5ba057. |
| K3 | PASS | cones-literal k = 0 BASE = the DP3 dry run's build: 6,180 pairs, sha256 c5cb89e8f95bfe3d, bytes equal `DP3_release_day/dry_run_dr3/wb_dr3_cones_literal.csv`. |
| K4 | PASS | extract-builder base_k equals the G50 seed-sweep build on disk (`seed_k<k>/final_g50.csv`) at 51 of 51 k; none missing, none unequal (the DP7 base at offset k IS the G50 build at offset k). |
| K5 | PASS | 32 pinned frozen files (DP1's five + DP3's 27, pipeline 7c884e0e) unchanged before and after every run; none off its pinned value. |
| K6 | PASS | the pipeline's own self-test at seed 20261216 passed on all 102 fitted catalogues of the sweep (and on every fit of K2, M1, M2, C1). |
| SWEEP | PASS | `--cut13 cones-literal --fit-path pipeline --K 50 --rung-missing-cones extract-fallback` complete, 51 of 51 k, both footings; 4,010 s wall. |
| M1 | BITES | `--mutate-k0` (every k reads the k = 0 build): Delta_bar == Delta_0 and SD == 0 at 1e-12, every Delta_k bit-identical to Delta_0, entry == gamma_hat(rung_0): canonical +0.000000, alt -0.010000. `dp7_MUTATE1.out`. |
| M2 | BITES | `--keep-nss` (rung built without dropping NSS): Delta_k == 0 within 1e-9 at every k, rung bytes == base bytes at every k, both footings. `dp7_MUTATE2.out`. |
| S4 | PASS | `dp3_sigma_sys.py` with the new option OFF reproduces the dry run's `sigma_sys_dr3.json`: 74 numbers, max diff 0, none beyond 1e-9; (b) 0.0375 / 0.0412. `dp3_d6_replay.out`, commit 62509bcee6. |
| C1 | BOUND = measured change (AMENDMENT_A1 item 3; informational, the label stands with the number beside it) | see section 3. |

## 3. AMENDMENT_A1: the rung's missing cones, the bias bound and control C1

At the first graded build the NSS-off RUNG had 10,370 pairs reaching cut 13 against the registered 10,231; the 139 extra are exactly
the NSS-flagged pairs the registered screen removes before cut 13, and the DR3 cones were fetched for the registered set only.
`cones_cut13` refuses an uncovered pair by design, fetching cones is an archive query the owner's note excludes for this lane, and the
set is seed-independent (the stage-G seed enters only the vtilde-error cut, after cut 13). Under the amendment the rung uses the
driver's own `--missing-cones extract-fallback` for those 139 pairs; the base stays strict (K3 untouched).

Bias bound printed in `dp7.out`: the fallback flags 0 of the 139; the cones flag 7 of 10,231 (rate 6.8e-4), so a real cone fetch
would be expected to flag ~0.10 of the 139. The rung is at most about one tenth of a pair heavy at every k.

Control C1 (`dp7_C1.out`, `dp7_C1.json`): flag one randomly chosen uncovered pair (numpy default_rng seed 1103 -> index 58 of 139,
pair 2590927961771849856 / 2590927961771850112, not already flagged; the fallback was called exactly once) and refit the k = 0 rung
by the registered path on both footings.

| footing   | rung k = 0 (fallback) | one uncovered pair flagged | change   | below 1e-3 |
|-----------|-----------------------|----------------------------|----------|------------|
| canonical | 1.1375 +- 0.0575      | 1.1200 +- 0.0550           | -0.0175  | no         |
| alt       | 1.0775 +- 0.0537      | 1.1025 +- 0.0512           | +0.0250  | no         |

The amendment's rule applies: the bound is reported as the measured change, beside the label. Reading of that change, recorded in
`dp7_C1.json` (`final_pair_set_difference`): the final catalogue went from 6,311 to 6,289 pairs, and the two final pair sets differ by
304 pairs (163 only in the reference, 141 only in the one-flagged build). One flag at cut 13 removes one pair before the stage-G
vtilde-error Monte Carlo, which is drawn (`B.vt_error_mc`, seed SEED + k) over the post-cut-13 pair set; the stream re-aligns and the
stochastic cut re-draws for every later pair. The measured change is therefore one draw of the stage-G seed noise, the very quantity
this lane measures (per-k SD of Delta_k 0.024, the same size as the C1 changes), not the effect of one pair's membership. C1 as
frozen cannot resolve a ~0.1-pair bias below the seed noise; the 0.10-pair expectation from the cones' own flag rate is the bound
that stands. No frozen text was changed to say so; this is the reading beside the label.

## 4. Section 4: sigma_sys(b) under both NSS-off entries (information only, DR3)

`dp3_sigma_sys.py` gained exactly one non-default option, `--nss-off-seed-mean DP7.json` (default off; off = byte-identical behaviour,
S4 above). With it on, the NSS-off entry of (b) and (e) is gamma_hat(V0 base) + Delta_bar[footing], and the single-seed values are
printed beside it. Note that the recipe fits with its own estimator (the D2 lane's 1e6 master), so its V0 base is 1.0750 / 1.0700 on
these inputs; Delta_bar from the registered pipeline path is added to that base, as the draft writes it.

| run | footing | (b) single-seed | (b) seed-mean | (e) single-seed | (e) seed-mean | spread single-seed -> seed-mean |
|-----|---------|-----------------|---------------|-----------------|---------------|---------------------------------|
| D6 inputs (NSS-off = the D2 probe, `dp3_seedmean_d6inputs.out`) | canonical | 0.0375 | 0.0200 | 0.0162 | 0.0067 | 0.0750 -> 0.0325 |
| D6 inputs | alt | 0.0412 | 0.0200 | 0.0182 | 0.0085 | 0.0825 -> 0.0396 |
| release-day path (NSS-off = DP1 rung, `dp3_seedmean_releasepath.out`) | canonical | 0.0225 | 0.0200 | 0.0099 | 0.0067 | 0.0450 -> 0.0325 |
| release-day path | alt | 0.0287 | 0.0200 | 0.0124 | 0.0085 | 0.0575 -> 0.0396 |

On DR3 the single-seed NSS-off rung sets the spread in every case (+0.0750 / +0.0575 on the D6 inputs, +0.0450 / +0.0325 on the
release-day path); replacing it with base + Delta_bar (+0.0123 / +0.0147) leaves the 3-20 kAU rung to set the spread (0.0325 /
0.0396), and (b) falls to its 0.020 floor on both footings. This is what the draft's section 3 left open ("direction unknown"): on
DR3 the seed-mean entry LOWERS sigma_sys(b) to the floor. DR3, information only; the DR4 numbers are the release-day session's.

The DP3 release-day script is not edited. The DR4 invocation, should the amendment be filed, is the O12 line with the option added:
`dp3_sigma_sys.py --base <PRIM> --nss-off <OUT>/nss_off_rung_dr4.csv --seed-manifest <OUT>/seed_sweep_manifest_dr4_g50.json
--nss-off-seed-mean <DP7 dr4 json> --tag DR4 --out-json <OUT>/sigma_sys_dr4.json`.

## 5. Hand estimates

| id | estimate | outcome |
|----|----------|---------|
| HE-a | Delta_bar canonical in [-0.005, +0.015], SE <= 0.007 | **HIT** (+0.0123, SE 0.0034) |
| HE-b | Delta_bar alt in [-0.005, +0.010], SE <= 0.005 | **MISS** (+0.0147 is above +0.010; SE 0.0033 inside) |
| HE-c | the DR3 seed-mean entry does not change sigma_sys(b) (the 3-20 kAU rung sets the spread) | **MISS**: the NSS-off rung set the DR3 spread; (b) 0.0375 / 0.0412 -> 0.0200 / 0.0200 |
| HE-d | K1 reproduces bit for bit on the first run | **HIT** |

## 6. Cost (section 5)

| run | builds | pipeline fits | from cache | wall | per k | per fit | fit peak RSS | wrapper peak RSS |
|-----|--------|---------------|------------|------|-------|---------|--------------|------------------|
| K1 (d2 path, K 8) | 18 | 18 (D2 estimator, in-process) | 0 | 67 s | 6.0 s | - | - | 2.12 GB |
| K2 (pipeline, k 0) | 2 | 2 | 0 | 77 s | 76 s | 35 s | 3.92 GB | 1.21 GB |
| graded sweep (K 50) | 153 | 102 | 0 | 4,010 s | 76 / 78 / 83 s (min / median / max) | 33.7 s | 4.01 GB | 3.38 GB |
| M1 | 153 | 102 | 102 | 549 s | 10.7 s | - | (cached) | 3.36 GB |
| M2 | 153 | 102 | 102 | 470 s | 9.2 s | - | (cached) | 3.39 GB |
| C1 | 2 | 2 | 0 (first run) | 45 s | - | 33 s | 4.28 GB | 2.70 GB |
| dp3 seed-mean, two runs | - | 12 recipe fits each | - | 12 s + 11 s | - | - | - | 1.59 / 1.52 GB |

Per k in the sweep: 3 builds (base, rung, and the extract-builder base for K4), 2 fits, base build ~3.1 s, rung build ~4.6 s, fit
~33-36 s each. One process at a time, nice 10, OMP_NUM_THREADS 1 throughout. The fit RSS is the registered pipeline's own
`--catalog` run (4.25 GB in DP1), allowed and recorded. The wrapper RSS (up to 3.4 GB) exceeds the "everything else under 1 GB" rule:
it is the driver's own inputs (stage_A plus the 3.2 M-row DR3 cones table) held by DP1's `rung_build`; nothing of DP7's adds to it.
Disclosed, not fixed. Checkpoint per k in `parts/`; the sweep was not interrupted.

## 7. The DR4 repetition (NOT run) and its cost projection

Not run: every k >= 1 stage-G correlation fetch is an archive query needing the owner's go on release day. The exact command, after
G8 (primary build, cones-literal), G10 (G50 seed sweep) and G11 (NSS-off rung) of the runbook have produced the DR4 manifest M, the
neighbours manifest NM and the seed caches:

```
OMP_NUM_THREADS=1 nice -n 10 python3 -B dr4_push_2026_11_05/DP7_seed_mean_check/dp7_seed_mean.py \
    --release dr4 --manifest <OUT>/manifest_dr4.json --neighbours-manifest <OUT>/neighbours_manifest_dr4.json \
    --cut13 cones-literal --fit-path pipeline --K 50 --rung-missing-cones extract-fallback --allow-network --out dp7_dr4
```
then `dp3_sigma_sys.py ... --nss-off-seed-mean dp7_dr4.json` (section 4). `--allow-network` is refused by the DR3 run of this script
(DR4 not run); on release day it is the switch the runbook passes to every build.

Projection at the DP2 central N ~ 8,039 (low 7,025 / high 8,618): the pipeline fit time is set by the 3,000,000-pair MC master, not by
N, so ~33-36 s per fit and 2 fits per k stay; the builds scale with the candidate set, ~1.3x DR3 -> ~4 s base, ~6 s rung. Offline
part: ~80-90 s per k, ~70-80 min for 51 k, fit RSS ~4.0-4.3 GB per fit, wrapper RSS above the DR3 3.4 GB (the DR4 cones table is
~1.7 GB accepted at G7; expect 4-5 GB). Archive part: the base_k builds ARE the G10 seed-sweep builds (K4), so their stage-G
correlations are already in `seed_k<k>/` caches after G10; the rung's cut-13 set is seed-independent, so G11's single stage-G fetch
covers the rung at every k if the rung builds read that cache. With both caches in place no new archive query is needed; otherwise one
delta correlation fetch per k, of the kind G10 budgets at "~1-2 h single job" for its own 50. Checkpoint per k; a SIGTERM loses one k.

## Release-day item for the owner

Runbook `dr4_release_day.sh` step G6 dumps the Q1 candidate set from the REGISTERED build (`--cut13 extract-builder
--dump-candidates`, i.e. after the NSS screen, cut 12), and G7 fetches the DR4 neighbour cones for that set. Step G11 then builds the
NSS-off rung in cones-literal mode on DR4; its cut-13 set is the PRE-NSS candidate set, which on DR3 was 139 pairs larger than the
registered one. On DR4 G11 will hit the same `ConeCoverageError` that DP7 hit here unless either (i) G7's Q1 cones query covers the
pre-NSS candidate set (the set before cut 12; more queries and accepted MB than the G7 GO line budgets), or (ii) G11 passes
`--missing-cones extract-fallback` as DP7's amended rung does (the frozen builder's third-star function on the extract for the
uncovered pairs; on DR3 it flagged 0 of 139 where the cones would flag ~0.1). Either is an archive-query scope or runbook change
that only the owner approves on release day; neither DP7 nor the orchestrator decides it. The same choice governs the DP7 DR4 rung
above.

## Disclosures

- AMENDMENT_A1 was filed after K1 and K2 had passed and before the graded sweep was run or read; the graded invocation differs from
  section 1 only by `--rung-missing-cones extract-fallback`. The strict (`error`) rung cannot be built offline on DR3.
- `dp7_grade.py` was written while the sweep was running, before its summary was read; its thresholds are the frozen ones.
- A sha-keyed fit cache (`work/fit_cache.json`, not committed; key = sha256 of the catalogue, seed, pipeline sha) served M1 and M2
  (102 of 102 fits each) and the C1 rerun that added the pair-set report (the first C1 run fitted fresh). The graded sweep took 0
  from the cache.
- Disk went to 0 bytes free once during K2 (other sessions' writes); K2 was rerun clean. The free space was 3.0 GiB at the start of
  the sweep and 9.2 GiB at its end. Pushes use a `--no-checkout` detached worktree of origin/main (a full checkout does not fit).
- The checkout this session works in is ~235 behind / ~88 ahead of origin/main; the DP7 and DP3 files were taken from origin/main
  by `git show` and committed back with explicit paths.
- Logs (`run_*.log`) are git-ignored; `work/` is not committed.
- No frozen file was edited (K5). No network access (socket guard; `--allow-network` refused on DR3). No DR4 data touched.

## Files

`dp7_seed_mean.py`, `dp7_grade.py`, `k1.json/.out`, `k2.json/.out`, `dp7.json/.out`, `dp7_MUTATE1.json/.out`, `dp7_MUTATE2.json/.out`,
`dp7_C1.json/.out`, `dp3_d6_replay.json/.out`, `dp3_seedmean_d6inputs.json/.out`, `dp3_seedmean_releasepath.json/.out`,
`dp7_grade.json/.out`, `parts/` (k1 9, k2 1, dp7 51, dp7_MUTATE1 51, dp7_MUTATE2 51 per-k json), `FROZEN_CRITERIA.md` (+ AMENDMENT_A1),
`BRIEF_2026_11_08.md`, `OWNER_DECISION_2026-11-08_DP7_CHECK_AND_FILE.md`, and the one-option diff of
`../DP3_release_day/dp3_sigma_sys.py`.
