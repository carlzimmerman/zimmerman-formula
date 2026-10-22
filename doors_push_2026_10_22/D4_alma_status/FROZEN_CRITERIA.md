# D4_alma_status FROZEN CRITERIA (committed alone, before any script or number of this lane)

Lane of the doors push 2026-10-22 (`doors_push_2026_10_22/BRIEF.md`). Door: the two sealed ALMA tests, U4_27928 (CO(2-1),
programme 2024.1.00100.L) and GS4_24110 ([CI](2-1) + dust, 2025.1.01377.L). Governing plans (owner decision 2026-10-20):
`campaign_fresh_gravity/CFG806_u4_27928_scoring/FROZEN_CRITERIA.md` (1bf70683b) + clarification + addendum A, and
`campaign_fresh_gravity/CFG809_gs4_24110_ci21_scoring/FROZEN_CRITERIA.md` (966d50a87) + clarification + addenda A–D. AG5 is a
secondary reading. Harness: `campaign_fresh_gravity/CFG942_alma_scoring_readiness/`. κ = ½ is FITTED. Footings (canonical
9.36e-11, alt 1.13e-10 m/s²) are never pooled. One disc excludes no model. Not theory closed. No download, no archive query.

**Not blind, disclosed.** Before writing this file I read: the owner decision, both plans and all their clarification/addendum
files, the CFG942 FROZEN_CRITERIA/README (incl. its R6 power and R7 sensitivity sections and committed selftest JSONs), the AG5
FROZEN_SCORING/README/power output, the AG4d (n=2) and AG4e (n=1) seal READMEs, the CFG570 archive rows for both programmes, the
LEDGER rows CFG571/CFG806/CFG809/CFG942/CFG942-1021/CFG942-ADDENDA-BCD/OWNER-DECISION-*, and THEORY_CANONICAL_2026-10-21_DRAFT §1
and §6. CFG943 is the Gaia DR4 readiness lane, not ALMA; it is not used for ALMA power.

## What is computed (all from sealed numbers and the governing plans' own statistics; no fit, no new constant)
Inputs, read only: the CFG571 seal (ν_mono; F-DESI, F-flat, R-H, L-fb), the AG4e seal (n=1), the AG4d seal (n=2), CFG571's
prediction functions (head of `cfg571_prereg.py`, executed read-only by `cfg942_common.load_cfg571`), the CFG942 harness's
GS4 `delta_v` (imported read-only) and its committed R7 forecast numbers (labelled external inputs).

**P1 (U4, CFG806 §4 statistic).** For each sealed V_c grid point (225, 250, 275, 300 km/s), footing and gas shape, the
separation between two models A and B is z = |log M_gas,req,A − log M_gas,req,B| / σ, with
- σ_floor = √(0.15² + 0.15²) = 0.212 dex (CFG806 §3.3 floor ⊕ §4 floor, CLARIFICATION A-U2), flux noise set to ZERO
  (the most favourable case; a ceiling on power), and
- σ_5 = √(σ_floor² + s_A² + s_B²), s = |d log M_gas,req/dV_c| × 5 km/s from the sealed grid (CFG942 R6's V_c error).
Pairs: framework (F-DESI, F-flat) vs rival R-H (the governing plans' rival), each footing; and n=1 vs n=2 for F-DESI and F-flat
(AG4e vs AG4d seals, same footing, shape, V_c). FLOOR on either side is reported as FLOOR (rule-based, no z).

**P2 (GS4, CFG809 §4 statistic).** Measured gas set equal to model A's sealed requirement (detected, flux error 0); model B's
Δ_v = log((V★² + V_gas²)/V²_bar,req,B) at R_e = 7.39 kpc with CFG571's Freeman functions and B's sealed logVbar2R_G; σ_Δv exactly
as `cfg942_gs4.delta_v` (gas route 0.2 dex ⊕ M★ 0.2 dex). z = |Δ_v| / σ_Δv. Pairs as P1, per M★ branch (10.89, 10.76), footing
and gas shape. If B is FLOOR, the plan's FLOOR rule applies; whether FLOOR persists at M★ − 0.2 dex is reported.

**P3 (sensitivity).** The CFG942 R7 G1 S/N at native resolution for the framework-required gas (committed numbers, quoted).

**P4 (record checks).** (a) Do the governing plans or their addenda name the AG4d/AG4e (n=2/n=1) seals? (b) Which kernel is
the canonical law (THEORY_CANONICAL draft §1) and which kernel do the governing plans score? (c) The sealed V_c grids' top
(300 km/s) against CFG806's "recompute at the measured V_c" rule, for ν_mono and for the n=1/n=2 seals. (d) CFG570's release dates
equal the plans' dates. (e) Any FITS file on disk whose name carries either programme ID or target name.

## Checks of the script (`d4_alma_status.py`; one line each; exit 0 iff all PASS)
- **K1** sha256 of the three seals equals their PREDICTIONS_HASH values (CFG571 be27457d…, AG4e 9802de0d…, AG4d d64727b5…).
- **K2** every ν_mono cell of CFG806 §2 (U4) and CFG809 §2 (GS4) tables equals the CFG571 seal within 0.005 dex; FLOOR identical.
- **K3** CFG571's functions recompute the sealed U4 ν_mono logMgas at V_c 250, canonical, F-DESI, R_g = R_d to ≤ 1e-9 dex.
- **K4** this lane's GS4 Δ_v and σ_Δv equal `cfg942_gs4.delta_v` on every ν_mono (A, B) pair to ≤ 1e-12.
- **K5** CFG570's release dates are 2026-11-06 (U4_27928, CO(2-1)) and 2026-11-28 (GS4_24110, [CI](2-1)).
- **K6** no frozen or sealed file changes during the run (sha256 before/after).
- **MUTATE** (`D4_MUTATE=1`): drop the 0.2 dex M★ term from this lane's σ_Δv. K4 must FAIL (exit 1). Outputs `*_MUTATE.*`.

## Frozen readings (decided now)
- **R-POWER:** if the largest noise-free z over every framework-vs-R-H pair (non-FLOOR) on a disc is < 3, the disc has **no ≥ 3σ
  framework-vs-rival separation under its governing plan even with perfect data**; say so plainly. Same for n=1 vs n=2.
  A z ≥ 3 is reported with its branch and is only a demonstration (one disc).
- **R-FLOOR:** a FLOOR-rule tension is a stellar-mass statement switched on by a detection; it is reported separately, with
  whether FLOOR persists at M★ − 0.2 dex, and is never counted as a σ separation.
- **R-SENS:** if the R7 G1 S/N for the framework-required gas is < 5 at native resolution, the expected release-day outcome is
  G1 FAIL / upper limit, and the expected separation is "not scored", whatever P1/P2 say.
- **R-GAP:** if no governing plan names AG4d/AG4e, the n=1 vs n=2 reading has no governing rule (AG5's reading is secondary).
  Proposed addendum wording goes in this lane's README only, never into a campaign directory.

Verdict words per the brief: CRISP FINDING, RUNNABLE NOW, DATA-GATED, SCOPED NO-GO or NOTHING NEW.
