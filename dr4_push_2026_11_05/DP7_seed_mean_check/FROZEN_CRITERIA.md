# DP7 frozen criteria: the DR3 code-path check that conditions filing the seed-mean NSS-off amendment

Frozen before any new code exists. Owner's words (2026-11-08, in the orchestrator session, to "File the DR4 seed-mean
amendment after its DR3 code-path check?"): "Yes, check and file". This lane is the check named in section 4 of
`prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-05c_DR4_SEED_MEAN_NSS_OFF_DRAFT.md` (4d8711da63). It is NON-SCORING:
DR3 numbers are code-path tests, never results (Amendment 7(e)); no verdict words about gravity. Kappa = 1/2 FITTED;
footings never pooled; not theory closed. No frozen file is edited: PREREGISTRATION_DR4.md, every *_HASH.txt, the
owner-decision notes, `wide_binary_pipeline.py` (sha 7c884e0e...), the D2 lane, CFG740/800/825/943, DP1's committed
files. New code only, in `dr4_push_2026_11_05/DP7_seed_mean_check/`, plus ONE non-default option added to
`dr4_push_2026_11_05/DP3_release_day/dp3_sigma_sys.py` (section 4 below), whose existing D6 known answer must still pass.

## 1. What is built

`dp7_seed_mean.py`: a sweep wrapper over DP1's `rung_build(...)` (imported from
`dr4_push_2026_11_05/DP1_nss_off_rung/nss_off_rung.py`, unchanged) and the registered base build at the same stage-G
seed offset k, both in the same cut-13 mode, fitted by the registered fit path (the frozen pipeline's `--catalog` fit,
seed 20261216, via DP1's `SS.fit_via_pipeline_cli` or an identical call), one footing at a time. Output per k and
footing: gamma_hat(base_k), gamma_hat(rung_k), the paired difference Delta_k = gamma_hat(rung_k) - gamma_hat(base_k),
sigma_fit of each. Then Delta_bar = mean_k Delta_k over k = 1..K, its SD and standard error, and the seed-mean NSS-off
entry gamma_hat_NSS-off = gamma_hat_0 + Delta_bar with gamma_hat_0 the registered k = 0 primary fit.

Modes: `--cut13 extract-builder` (DP1's DR3 mode, for the exact reproduction in K1) and `--cut13 cones-literal` with
the DR3 cones files (the release-day primary form, D7 N9; the files the DP3 dry run used: `q1_full_neighbours.fits` +
`wide_binaries_dr3.csv`, `q1_delta_neighbours.fits` + `q1_delta_pairs.csv` under the external data root), which is the
graded mode. `--fit-path {d2,pipeline}`: `d2` = DP1's `est.fit_fresh` (for K1 only), `pipeline` = the registered path
(graded). `--K`, `--mutate-k0` (section 3).

## 2. Known answers (all must pass before Delta_bar at K = 50 is read)

- K1 (exact reproduction of DP1 P4). With `--cut13 extract-builder --fit-path d2 --K 8`, every per-k value of base,
  probe-free rung and their difference must equal DP1's `dr3_check.json` `ensemble[k]` entries bit for bit (|delta| = 0
  at the printed precision) for k = 1..8, both footings; the means must equal DP1's `P4.mean_rung_shift`
  +0.0040625 canonical / +0.000625 alt and SDs 0.0310 / 0.0147 to 1e-6.
- K2 (the registered fit path reproduces DP1 P3 at k = 0). `--fit-path pipeline` at k = 0 on the DR3 extract-builder
  base and rung must give DP1's P3 fits: base 1.0750 +- 0.0550 / 1.0775 +- 0.0512, rung 1.1425 +- 0.0637 canonical
  (and the alt rung value in `dr3_check.json` P3.fits.rung.alt), to 1e-4.
- K3 (cones-literal base = the dry run). The k = 0 cones-literal base build must equal the DP3 dry run's
  `wb_dr3_cones_literal.csv` record: 6,180 pairs, sha256 c5cb89e8f95bfe3d.
- K4 (seed identity with Amendment 18). For k where the G10/G50 extract-builder base exists on disk
  (`seed_k<k>/final_g50.csv` under the DR3 external root), the extract-builder base_k built here must equal it byte for
  byte (DP1's `base_equals_g50_build` check, repeated).
- K5 (frozen files unchanged). sha256 of every pinned frozen file before and after, identical; `wide_binary_pipeline.py`
  7c884e0e.
- K6 (the pipeline's self-test passes at the registered seed on every fitted catalogue; a failure is printed and that
  k is still counted, flagged).

## 3. MUTATE (must bite)

- M1 `--mutate-k0`: the wrapper returns the k = 0 paired difference for every k. Delta_bar must equal the single-seed
  shift exactly and the SD must read 0; the printed seed-mean entry must equal the registered single-seed NSS-off
  value. If the grader still prints a different Delta_bar, the pipeline is broken and nothing is read.
- M2 `--keep-nss` passed through to the rung (drop_nss = False): Delta_bar must read 0 within 1e-9 at every k (the rung
  equals the base when the NSS line is kept and smax is the base's), both footings.

## 4. The sigma_sys(b) hook (section 4.4 of the draft)

`dp3_sigma_sys.py` gains `--nss-off-seed-mean DP7.json` (default off; with it off the file's behaviour and its D6
known answer are unchanged: the DP3 dry run's `sigma_sys_dr3.json` values must be reproduced to 1e-9 by the unchanged
call). With it on, the NSS-off entry in (b) and (e) is gamma_hat_0 + Delta_bar from the DP7 json, and the output
carries both entries side by side: sigma_sys(b) single-seed and sigma_sys(b) seed-mean, per footing, with the words
"information only, DR3". The DP3 release-day script is NOT edited; the DR4 invocation is written into RESULT.md.

## 5. Cost (recorded, section 4.3 of the draft)

Per footing and k: builds (2 per k: base, rung), pipeline fits (2 per k), wall time, peak RSS (the frozen pipeline's own
`--catalog` fit took 4.25 GB in DP1; that figure is allowed here because it is the registered path's, and it is recorded;
one process at a time, nice 10, OMP_NUM_THREADS 1; everything else under 1 GB). Checkpoint per k (json per k in
`parts/`), so a SIGTERM loses at most one k. The DR4 repetition is NOT run: every k >= 1 stage-G correlation fetch is an
archive query needing the owner's go on release day; RESULT.md writes the exact DR4 command and the cost projection at
central N ~ 8,000 (DP2).

## 6. Label rule

- CHECK PASSED: K1-K6 pass, M1 and M2 bite, the K = 50 cones-literal pipeline-fit sweep completes on both footings,
  section 4's hook reproduces D6 with the option off. The lane then reports, information only: Delta_bar +- SE, SD, the
  single-seed shift beside it, and DR3 sigma_sys(b) under both entries per footing.
- CHECK FAILED: any K fails, or a MUTATE does not bite, or the sweep does not complete by 2026-12-01. The draft then
  lapses and D8 (a) stands, as the draft says.
- Filing is NOT this lane's act. On CHECK PASSED the orchestrator files the draft (commit alone, retitled "filed", the
  owner's words quoted) and the DP3 runbook is left for the release-day session.

Hand estimates (HIT/MISS in RESULT.md): HE-a Delta_bar canonical in [-0.005, +0.015] with SE <= 0.007; HE-b alt in
[-0.005, +0.010] with SE <= 0.005; HE-c the DR3 sigma_sys(b) seed-mean entry does NOT change sigma_sys(b) because the
3-20 kAU rung sets the spread (direction unknown, draft section 3); HE-d K1 reproduces bit for bit on the first run.

Outputs: dp7_seed_mean.py, dp7_grade.py, dp7.json, dp7.out, dp7_MUTATE1.out, dp7_MUTATE2.out, parts/ (per-k json),
RESULT.md, the one-option diff of dp3_sigma_sys.py with its D6 replay output `dp3_d6_replay.out`. Commit with explicit
paths; push via a temp detached worktree of origin/main. Logs (*.log) git-ignored.
