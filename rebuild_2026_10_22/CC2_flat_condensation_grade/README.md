# CC2_flat_condensation_grade

**Question.** Is critical condensation a calibration pass in its one consistent ungraded form? In that form c_f = 4 holds everywhere: η = 10.82 sets both the core and the switch, and a halo forms iff η Σ_coll(M) > Σ_a0. Criteria: `FROZEN_CRITERIA.md` (bca910bd02, committed alone first). The harness is CSM1's `calibrate.py`, executed as `cc2_calibrate.py` with two changes only: the tag `shpS9_L` → `shpFLAT_L` (CL3's existing FLAT shape) and the root path. Level L = 4.

## Verdict: CONDENSATION FAILS CALIBRATION, both footings

| Line | canonical | alt |
|---|---|---|
| SPARC line, background A / B, basin and own flags | PASS (rms 0.067 / 0.065 basin) | **FAIL** (the law's Υ problem, X78) |
| 63 groups | **FAIL, Z +2.02** (ABOVE LAW; 62/63 on the halo branch) | PASS, Z +1.49 |
| 15 cluster keys × 2 h | PASS | PASS |
| Lensing, H2H − law (≤ 9) | **FAIL, +22.5** (176.8 vs 154.3; pure halos 583.9) | PASS, 0.0 (every lens on the law branch) |

Canonical misses narrowly on two lines. CSM1 at S9 L 3.75 missed lensing by +415, so the flat form improves on it by about ×18. Alt fails SPARC under every switch on record.

**Crossings from the harness's own EPS.** Background A gives 12.09 canonical / 12.43 alt; background B gives 12.14 / 12.47. The coarse X43 table interpolation used in CC1 and in the spec gives 12.66 / 13.00. The two Σ_coll functions differ by up to 0.048 / 0.063 dex, but that does not account for a 0.5 dex shift in the root: the floor convention probably differs. **Open:** reconcile the two before quoting any M_crit.

**Known in advance, not rerun.** The MW takes the law branch, since the LG basin (12.39) and its own M200 (11.88) are both below the canonical crossing. HO2 has that branch failing: 0/175 box cells, K_z z +12.0 / +14.1. On this table's crossings the basin is above 12.09 / 12.14, so under basin flags the MW gets a halo. That case is untested here, because MW is not in this harness.

**Checks.**
- Baseline reproduces: CL3 at L 3.75 on all 12 lines, and X53 cf4.
- 0 decision violations; MUTATE detected.
- 700 SPARC decisions, 63 groups, 15 × 2 clusters.
- Peak RSS 0.65 GB, runtime 583 s.

**Run:** `PYTHONHASHSEED=0 nice -n 15 python3 -I rebuild_2026_10_22/CC2_flat_condensation_grade/cc2_calibrate.py --output rebuild_2026_10_22/CC2_flat_condensation_grade/run_001 --levels 4` from the repo root. Log: `run_001.log`; grades: `cc2_summary.json` (raw `run_001/` kept local: it embeds machine paths).

κ = ½ FITTED; c_f EXTERNAL; core shape empirical. Cold dark energy is a gravitating field component, never a particle. Footings are not pooled. Not theory closed. Nothing here says the data favour the framework.
