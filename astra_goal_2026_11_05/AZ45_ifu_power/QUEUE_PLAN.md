# Prepared queue contract — NOT SUBMITTED

Kappa=1/2 FITTED; not theory closed. The full4032-case grid remains pending.
Do not submit before the brief's light-tier work is finished. Check live
1024-cubed processes and queue state first; preserve other jobs/checkpoints.

## Footprint and granularity

The bounded fine-rung template11, alt, flat, S/N120, free-HI pilot finished
in13.72seconds. macOS footprint sampled it every0.5seconds, recording
phys_footprint_peak153,912,040bytes (0.154GB), versus RSS378,191,872bytes.
The sanitized samples and result hash are in footprint_pilot_measurement.json.
All production cases have the same25x25x25 cube dimensions; only values,
noise, nuisance treatment and numerical rung change. Cases run serially in
fresh child processes, so the4032-case total does not multiply memory.
Declare est_gb=1.0 for the parent plus child, over six times this child's
measured peak; keep the existing1GB child-RSS emergency guard. This is an
estimate, not a guarantee of the full-grid peak; heavyq's learned footprint
and process-group safeguards remain authoritative.

Each completed case is a small JSON (fit vectors and summaries, no cubes),
with a separate runtime JSON. Allow100MB for4032 case records, checkpoints
and logs; no per-case cube archive. Each new case checks matching input,
worker and package identities before accepting saved results. Atomic fsync
writes protect completed case records. The partial current case restarts
deterministically on resume; earlier complete cases are retained. The full
batch writes grid/COMPUTE_DONE.json only after4032 completed computations,
including unresolved scientific fits. This marker does not mean scientific
calibration or power gates pass.

Worker SIGTERM/resume and idempotence are verified in resume_contract.json;
interrupted and uninterrupted scientific outputs match exactly. Batch pilot
and coverage are recorded in batch_contract/batch_checkpoint.json and
grid_plan.json. Full grading remains separate and must not drop unresolved
fits. Both footings, all controls and both numerical rungs are enumerated.

## Command to submit only after the light-tier prerequisite

From the repository root, using the already-tested installed environment:

```sh
python3 compute_queue/heavyq.py add --id az45_ifu_full \
  --cwd astra_goal_2026_11_05/AZ45_ifu_power \
  --cmd '/opt/homebrew/Caskroom/miniconda/base/bin/python3 batch.py --tag grid --resume' \
  --resume-cmd '/opt/homebrew/Caskroom/miniconda/base/bin/python3 batch.py --tag grid --resume' \
  --est-gb 1.0 --threads 1 --priority 10 \
  --done-file grid/COMPUTE_DONE.json \
  --note 'AZ45 frozen4032 cases; serial child fits; allow100MB outputs; footprint pilot0.154GB; scientific grader separate'
```

Verify the current heavyq CLI before submission. Never set HEAVYQ_JOB_ID by
hand to bypass the guard. No queue entry exists from this preparation.
