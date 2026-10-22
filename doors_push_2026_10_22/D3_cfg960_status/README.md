# D3_cfg960_status: what happened to the CFG960 1024³ run

**Verdict: CRISP FINDING (about the run, not about the physics).** The pre-registered SC1x job (canonical footing) was killed
four times by its own frozen abort rule (swap growth > 4 GB) and the chain stopped at 2026-10-22 01:01 local. It reached step 89 of
150 (a = 0.19). SC2x (alt) never started. No scored output exists, so there is **no verdict on either footing**. A restart under the
frozen files is expected to die at the same place.

This lane is read-only forensics. Nothing was scored, so no FROZEN_CRITERIA.md or checks script was needed (lane brief). Every
number below is read directly from the log lines cited. `EXT` = `../_external_data/cfg960_work/` relative to the repository root
(one level above it), where `chain960.sh` writes.

## 1. What happened

| try | start (local) | end | how it ended | evidence |
|---|---|---|---|---|
| 0 | 10-21 17:41 | 10-21 23:14 | killed in step 81 (after checkpoint 79) | `EXT/SC1x/watch.log:997` "ABORT (frozen rule): rss 19.37 swap growth 4729" |
| 1 | 10-21 23:14 | 10-22 00:35 | resumed at 79, wrote checkpoint 89, killed in force call 90 | `watch.log:1244` swap growth 6281 MB |
| 2 | 10-22 00:35 | 10-22 00:48 | resumed at 89, killed in force call 90 (≈ 12.7 min) | `watch.log:1285` swap growth 8596 MB |
| 3 | 10-22 00:48 | 10-22 01:01 | resumed at 89, killed in force call 90 (≈ 12.7 min) | `watch.log:1326` swap growth 6151 MB |

- `EXT/chain960.log` ends: "chain960 stopped after SC1x failure" (01:01:54). All 3 resumes used; `chain960_state/` holds no `.ok` file.
- `EXT/run_960_launcher.log`: every try "SC1x rc -9" (killed by the launcher, not an exception, not the OS).
- Not disk: free disk never fell below 61.8 GB (guard 3 GB). Not the 52 GB RSS rule: it never fired.
- Force call 90 is a census refresh (engine: `refresh_now = calls % 10 == 0`, `cfg960_sctm_pm.py:715`). It has now killed the job
  3 times out of 3. The death is reproducible, not bad luck.

## 2. Why: the engine outgrows the 64 GB machine

- Machine memory 68.7e9 bytes (64 GiB). The process **footprint** (the launcher's `proc_pid_rusage` column, which counts compressed
  pages) peaked at 51.4 / 63.9 / 59.2 / 65.2 GB in tries 0–3 (`watch.log:994, 1240, 1284, 1321`). The OS then swapped, swap grew
  by more than 4 GB, and the frozen rule killed the job.
- The `ps` RSS that the 52 GB guard watches read only 11–19 GB at each kill. It drops when macOS compresses pages, so **the RSS
  guard cannot see this failure**; only the swap rule can.
- The engine's own maxrss climbed with the number of SCT domains: 39.2 GB to step 65, 46.7 GB at step 79, 49.6 GB at step 85
  (`EXT/SC1x/engine.log:28, 32`). Domains: 22 (step 30), 3 382 (40), 58 470 (50), 286 764 (60), 720 373 (70), 1 243 688 (80).
- FROZEN_CRITERIA_1024 §3 estimated a peak of 43–47 GB per footing. That was already exceeded at step 85, with 65 steps and the
  most structure still to come.

## 3. Is anything reportable from the partial run?

**No.** Under FROZEN_CRITERIA_1024 §4 (V3) a run with a missing snapshot is VOID. Only the zi snapshot was written
(`EXT/SC1x/cfg960sctm_m3_SCT_canonical_N1024_L100_ns1024_lean.json`, 17:47). The first scored snapshot, z = 1, comes at a = 0.5.
The run JSON does carry the right pins (`engine_sha256` = e1fe3b3d…74d5, `sct.own_baryons` = "census f_ret (A5 primary)"), and
the per-step mass book stayed at ≤ 7e-15. Those are health checks, not a verdict. Nothing about the shear test was learned.

## 4. What a restart would need

- **Checkpoint.** `EXT/SC1x/cfg960sctm_m3_SCT_canonical_N1024_L100_ns1024_lean_ckpt/` (meta `n_done` 89, `calls` 90; 32.4 GB on
  disk). It is intact, and the four pinned files still match ADDENDUM A1's sha256 values (checked 2026-10-22).
- **Memory: the binding constraint.** The step-90 refresh already needs a footprint of ≈ 60–65 GB, and the domain count is still
  growing. Under the frozen files, a resume on this machine is expected to be killed again at force call 90. Freeing other apps
  helps by a few GB at most: tries 1–3 started with 54–59 GB free + inactive and still died. Any real fix changes something frozen:
  - a lower-memory engine (for example streaming the refresh/partition over domain chunks) changes `engine_sha256`, and V1 then
    makes the run VOID unless a dated pre-result amendment re-pins it; or
  - changing the abort rule (swap or footprint) changes `run_960.py`, which needs the same amendment; or
  - running unchanged on a machine with ≥ 96–128 GB.

  It is not known whether the refresh checkpointed at step 89 replays bit-identically under a new engine. The amendment would have
  to state that, or restart from zi.
- **Wall time.** Steps 0–80 took 5.4 h (`engine.log:29`, t = 19 547 s). Steps 80–89 took ≈ 410 s per step. The remaining 61 steps
  plus 5 snapshots are ≥ 7–10 h, and SC2x needs a full ≈ 15–25 h after that, if memory allowed.
- **Disk.** 74 GB free now (the volume is 96% full). The gate needs ≥ 45 GB. SC2x needs another ≈ 32 GB checkpoint plus about 4 GB
  of labels, so the SC1x checkpoint must stay until SC1x finishes.

## 5. Is anything heavy running now? (2026-10-22, ≈ 13:20 local)

No. No CFG6xx/960 engine, launcher, chain or llama-server. No python process is above 1 GB; the largest processes are
Firefox (≈ 8 GB summed). But free + inactive memory is ≈ 37 GB, below the gate's 46 GB, so `chain960.sh` would sit in its gate
until memory is freed.

## 6. Errors in the record

- `campaign_fresh_gravity/LEDGER.md:731` says "chain960.sh STARTED 2026-10-21" with no outcome. It should record that SC1x was
  killed 4× by the frozen swap rule at force call 90 (step 89/150), and that there is no verdict.
- `campaign_fresh_gravity/CFG960_sctm_engine/README.md:17` still says "Nothing has been started". This is stale.
- `FROZEN_CRITERIA_1024.md` §3 gives a peak memory of 43–47 GB. The measured value was 49.6 GB maxrss by step 85, with a 65 GB
  footprint at step 90.

These files belong to the CFG960 lane. This lane does not edit them.

## What this does not show

It says nothing about whether SCT-M passes or fails the shear side. The 128³ previews remain NOT A VERDICT. κ = ½ FITTED; footings
never pooled; not theory closed.

Restart command, as frozen (expected to be killed again at force call 90 unless memory is fixed under an amendment), from the
repository root:

    cd campaign_fresh_gravity/CFG960_sctm_engine && nohup bash chain960.sh > ../../../_external_data/cfg960_work/chain960_nohup.log 2>&1 &
