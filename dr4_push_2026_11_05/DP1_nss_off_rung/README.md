# DP1: the NSS-off rung: REPRODUCED ON DR3, rung IMPLEMENTED (owner decision D7 N4.1)

Criteria `FROZEN_CRITERIA.md` (06a321493b), committed alone before the code. New code only; no frozen file edited (K5:
frozen sha256 unchanged, pipeline 7c884e0e). DR3 numbers are code-path tests, never results; NON-SCORING; no verdict
words. κ = ½ FITTED; not theory closed.

## Verdict
Under the owner decision `prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-05b_DR4_D7_D8.md` (D7 N4.1):
- The rung `build(drop_nss=True, smax_kau=30)` reproduces the D2 lane's DR3 NSS-off probe. **REPRODUCED.**
- The MUTATE run (drop_nss=False) reads **NOT REPRODUCED**, and P1 fails, as §5 requires.
- **So the rung counts as IMPLEMENTED for DR4.** Its DR4 path is not yet tested; it runs on release day.

| check | main run | MUTATE (drop_nss=False) |
|---|---|---|
| K1 registered build = on-disk catalogue (6,210, 6fff64d9) | PASS | PASS |
| K2 wrapper = `build_variant_catalogue.build(...)` | PASS (rung 6,282 pairs, 1dbdf21a) | PASS (= registered) |
| K3 build(True, 50) = CFG816 variant 80c12924 | PASS | PASS |
| K4 the 12 D2 fits reproduced (max Δ 0) | PASS | PASS |
| K5 frozen files unchanged | PASS | PASS |
| K6 rung ≤ 30 kAU, NSS-flagged pairs present (99) | PASS | FAIL (0 flagged) |
| P1 pair level: NSS-flagged Jaccard ≥ 0.90; other flips ≤ 5 % | PASS (0.990; 2.6 / 2.3 %) | **FAIL** (0.000) |
| P2 D2 estimator shift vs probe (tol 0.0704 / 0.0597) | PASS (+0.045 vs +0.075 can; +0.030 vs +0.0575 alt) | FAIL (−0.010 / −0.0025) |
| P3 pipeline `--catalog` fit shift vs probe | PASS (+0.0675 vs +0.075; +0.025 vs +0.0425) | FAIL |
| P4 8 reseeded builds, mean(rung − probe) (tol 0.0249 / 0.0211) | PASS (−0.006 / −0.005) | PASS: **no power** |

P4 does not bite. Its tolerance is wider than the small ensemble NSS-off shift, so it cannot tell the rung from no change.
P1, P2 and P3 carry the check. §2 of the criteria allows a check to lack power and requires this to be reported.

**Mislabel in the MUTATE output, disclosed.** `dr3_check_MUTATE.out` prints "CODE FAULT" and the run exits 1. That label is a flaw in the verdict code: it applies K6 (≥ 20 NSS-flagged pairs) as a known-answer check to the mutated rung too, which has none by design. It is not a code fault. The governing §5 reading is P1 failing, which makes the run NOT REPRODUCED. The label is left unfixed in this commit; any fix goes forward in a new commit.

## Reported beside the verdict (information, no weight; D8 option (a) stands)
- **Most of DR3's +0.075 NSS-off shift looks like build noise at the registered seed.**
  - Over 8 reseeded builds the mean NSS-off shift of the probe is +0.010 canonical (SD 0.043) and +0.006 alt (SD 0.029).
  - For the rung it is +0.004 (SD 0.031) and +0.0006 (SD 0.015).
  - This changes no σ_sys definition, band or verdict.
  - It means σ_sys(b) on DR4 depends on one stage-G realisation: the single-seed NSS-off shift scatters by about 0.03–0.04.
- **D7 N4.2 reading (|shift| < 1 σ_fit passes the NSS-off condition):**
  - P2: passes on both footings.
  - P3: the canonical shift (+0.0675) is ≥ 1 σ_fit (0.055) and does not pass.
- The SD of rung − probe per seed (0.048) is larger than the √2·σ_G ≈ 0.035 assumed in the criteria.
- Peak RSS 4.25 GB in the main run, from the frozen pipeline's own `--catalog` fit, just over the stated 4 GB. MUTATE
  run 0.88 GB.

## DR4 command (release day; untested on DR4)
`python3 -B dr4_push_2026_11_05/DP1_nss_off_rung/nss_off_rung.py --release dr4 --manifest M.json --cut13 cones-literal --neighbours-manifest NM.json --allow-network --out-csv nss_off_rung_dr4.csv --fit --baseline-csv <primary build csv>`
Every archive step needs the owner's go.

## Files
`nss_off_rung.py`, `nss_off_rung_selftest.out/.json`, `dr3_check.out/.json`, `dr3_check_MUTATE.out/.json`,
`nss_off_rung_dr3[_MUTATE].csv` + manifests. `run_main.log` / `run_mutate.log` are git-ignored (*.log) and kept locally. `work/` (derived D2 probe CSV) is not committed.
This lane was run by a sub-agent; the lead session read the MUTATE result and wrote this README.
