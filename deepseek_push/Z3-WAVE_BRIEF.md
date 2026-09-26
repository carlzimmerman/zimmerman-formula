# Z3-WAVE_BRIEF (spawned conductor tick 2026-09-26 ~17:15 EDT)

House rules: deepseek_push/LOOP_CONDUCTOR.md 1-10, binding. Append-only; honest FAILs;
no fabrication (every number loaded from a file on disk); the kills below are
PRE-REGISTERED before any lane prints a physics number. 3 lanes, distinct OPEN doors,
single-process-or-small-pool each (box load 8.15/16 at spawn with the live-lab L388
Pool(8) running; registered load-gate precedent). No lane touches another lane's
files. Leaf lanes do NOT commit; the conductor commits.

## Lane QF3 - Q-closure SE-shrink (QF2's recast door)
Door: Q-closure OPEN; QF2 verdict: no smooth closure of any form meets the 3-SE bank
gate at current MC budget -- an SE-shrink (n-scaling) lane must shrink s_Q first.
Owns: QF3_* in deepseek_push/. Inputs (loaded): L02_results.json (tables; L02's
measure() engine imported, never transcribed), QF1_q_closure.evaluate,
QF2_q_noise_floor.run_table. Stage 1: every L02 grid cell (central+volume) re-measured
at n = 6e5 (4x L02's 1.5e5), fresh seeds 20260930+. PRE-REGISTERED:
- R1: median s_Q(4x)/s_Q(L02) in [0.20, 0.32] else exit 1.
- R2: per-cell z (fresh-vs-L02, combined SE): >= 90% |z| <= 3 and max <= 5 else exit 1.
- R3: max |Q - X| < 1e-9 else exit 1.
- R4 bank gate VERBATIM: family in-fit <= 3 SE AND LOO holdout <= 5 SE on central AND
  volume -> CLOSURE-BANKED, exit 0. Else NOISE-BOUND (residual shrank >= 1.6x ->
  stage 2 at n = min(ceil(n_bank), 4.8e6) on the binding-q rows, gates re-run) or
  BIAS-FLOOR (< 1.6x -> door recasts AGAIN as a finer-tau0 rerun, NOT n-scaling);
  honest exit 1 either way unless banked. NO new families; NO SE re-tuning.

## Lane A3 - U-band-rule re-derivation (A2 successor)
Door: A2 verdict ATLAS-RULE-ARTEFACT -- the N04-record atlas reproduces every V03c
volume cell at matched config; the tree's 10 volume U-OUTs are artefacts of the
nearest-row snap at the pinned (tau0,q). Owns: A3_* in deepseek_push/. Inputs
(loaded): V03b_trio_results.json (cells + stored A, dbar, U, se_U_block),
N04_raw_cells.json (record thomson atlas). PRE-REGISTERED:
- R0 control (recorded, no gate): truth-row nearest-row readout -- expect 0 volume
  U-OUT per A2.
- V1 candidate: BILINEAR atlas interpolation at the pinned (th,qh) (recomputed from
  stored A, dbar exactly as V03b; th clamped [0.5,3], qh clamped [0,10], clamps
  counted); atlas SE = max of the 4 corner se_U_block; margins 3 sigma unchanged.
- G1: central 18/18 'C' under V1; G2: volume U-OUT = 0; G3: volume V >= 12/18.
  All -> U-RULE-REBUILT exit 0; any -> RULE-RECONSTRUCTION-FAILED exit 1 verbatim.

## Lane M04b - J10-I(z) cosmography at the OB1 recipe
Door: M04 closed 14/14 under an ASSUMED S/N = 30 (stated in M04's md); OB1/Z2
registered the minimal block N = 3, S/N = 10, f = 20, rate 0.9998. Owns: M04b_* in
deepseek_push/. Method: exec M04_j10z.py source loaded from disk -- first UNPATCHED
but output-redirected (R0 control: must reproduce M04_results.json key scalars
bit-equal, else exit 1), then with only SN 30 -> 10 patched (all M04 SEs scale exactly
1/SN: seA = se_d = 1/SN, SE_r = sqrt(2)/SN). PRE-REGISTERED gates at S/N = 10:
- GA single-object lag 3-sigma at z = 1; GB window (atom incl.) 3-sigma single OR
  N = 3 stacked (same-z stack, independence assumed and stated); GC ratio-chain
  3-sigma exclusion reachable at z2 <= 2.0 (inside G237's z <= 3 law).
- All -> PASS-CHEAP exit 0; GA and GB both fail -> OB1-CANNOT-COSMOGRAPH exit 1
  (program books S/N = 30 blocks, L05 budget x5); partial -> verbatim, exit 1.

Barred (register, verbatim): SPARC-deep deficit sizing; V04 factorized N=1 route;
N01 density-locality; all KILLED doors; ai_slop/autoresearch_v3 (live lab).
