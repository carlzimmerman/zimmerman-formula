# Z2-WAVE_BRIEF (spawned conductor tick 2026-09-26 ~09:00 EDT)

House rules: deepseek_push/LOOP_CONDUCTOR.md 1-10, binding. Append-only; honest FAILs;
no fabrication (every number from a loaded file on disk); kills below are PRE-REGISTERED
before any lane prints a physics number. 3 lanes, distinct OPEN doors, single-process
(light) each — wave cut from the 3-7 band under the recorded load gate (box load 45.9 on
16 cores at spawn, live-lab pools L373/L379/L380/L354/L359 running; register ops-note
precedent: heavy lanes under load reproduce the silent-death mode). No lane touches
another lane's files. Leaf lanes do NOT commit; the conductor commits.

## Lane A2 - atlas sufficiency for the volume-branch U-OUT door (V03c-derived)
Door (register 04:36 ops note): V03c decision tree, volume branch: 10/18 cells read
U-OUT vs the N04-record atlas, 4 NOT-CENTRAL - atlas sufficiency undecided.
Owns: A2_* in deepseek_push/. Inputs (loaded, never transcribed):
V03b_trio_results.json (cells: U, se_U_block, cov; decision_tree rows), N04_raw_cells.json
(record atlas raw cells, tag-matched 'is'->'iso').
Measurement: for every V03 volume tag, matched-config z of
dU = U_v03 - U_n04, sigma = sqrt(se_U_block_v03^2 + se_U_block_n04^2) (independent MC runs).
PRE-REGISTERED branches (fixed before any number):
- K1: any matched-config |z_U| >= 3 -> that config is ATLAS-CONTESTED (V03 engine and the
  N04-record atlas disagree at the same config) - list them.
- K2: ALL volume |z| < 3 -> the atlas reproduces the V03 cells at matched config; the
  tree's U-OUT is an artefact of the band-rule reference (atlas-sufficiency holds);
  verdict ATLAS-RULE-ARTEFACT, tree read needs a successor rule lane.
- K3: if the disputed configs share one sign of dU -> systematic offset (n: 8e5 vs 1e6,
  engine delta) -> verdict ATLAS-SHIFT (atlas must be re-derived at V03's n before the
  volume branch can be scored).
Any branch reached cleanly = a result. Missing required field -> honest exit 1.
Deliverable: A2_atlas_sufficiency.json/.out (+ verdict line).

## Lane QF2 - noise-floor gate on the Q-functional closure door (QF1 honest FAIL, best 13.68 SE)
Door (register 04:36): Q-closure OPEN, sharpened by QF1: no closed family within 3 SE.
Owns: QF2_* in deepseek_push/. Input: L02_results.json (table_central/table_volume:
q, tau0, E_Q, s_Q). Gates VERBATIM from QF1/L02: in-fit max <= 3 SE AND leave-one-tau0-out
holdout max <= 5 SE, central AND volume. NO SE re-tuning (house rule 3).
PRE-REGISTERED decision (fixed before any number):
- B1 per q: leave-one-tau0-out local quadratic through the 3 nearest training tau0.
- B2 per q: natural cubic spline through ALL training tau0 (maximal smoothness floor).
- Branch P1: B1 or B2 passes both gates -> CLOSURE-FLOOR-LIVE: the table supports a smooth
  closure at the gate; QF1's 13.68 SE failure is family structure, not noise; record the
  floor SE as the target the next closed-form family must beat. exit 0.
- Branch P2: neither passes -> GATE-MISCALIBRATED-AT-CURRENT-SE: no smooth closure of ANY
  form can meet the 3-SE bank gate on these tables; the door is recast as an SE-shrink
  requirement (n scaling), not a family search. banked=false, exit 1, honest.
Deliverable: QF2_q_noise_floor.json/.out.

## Lane OB2 - JWST observing-block recipe (OB1 FEASIBLE-JWST follow-through)
Door (register 04:36): minimal registered config N=3, S/N=10, f=20, rate 0.9998 needs
its per-target recipe folded with K11's T5 falsifier and L05's budget.
Owns: OB2_* in deepseek_push/. Inputs (loaded): L05_results.json (power, budget,
sample), OB1_results.json, K11_results.json (consolidated tests verbatim).
PRE-REGISTERED branches (fixed before any number):
- R1: recompute OB1's minimal config from L05's power grid; rate must reproduce to the
  printed 4 decimals (0.9998). Mismatch -> exit 1 (loaded-number break).
- R2: per-target T5 recipe from L05 sample table rows (truth central: J10I window [4/3,2];
  kill >=3sigma outside; sharp: R > 1.5 r_B kills q=0, R > 2 r_B kills all q - verbatim).
- R3: exposure recipe from L05 budget dict (sn_N10_2x factor, n_SN30_2x) verbatim units;
  if any needed field absent -> RECIPE-UNDERDETERMINED, exit 1, NOT fabricated.
Deliverable: OB2_jwst_block_recipe.json/.out + OB2_JWST_BLOCK_RECIPE.md.

Barred (register, verbatim): SPARC-deep deficit sizing; V04 factorized N=1 route;
N01 density-locality; KILLED doors in the register; ai_slop/autoresearch_v3 (live lab).
