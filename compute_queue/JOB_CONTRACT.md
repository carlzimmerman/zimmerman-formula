# heavyq job contract

A job may be queued only if it meets every item below. `test/dummy_job.py` is the reference implementation, and
`test/test_cycle.py` runs it through every step of the cycle.

## 1. Declare `est_gb`: the peak footprint, not RSS
`--est-gb` is the job's peak **phys_footprint** in GB. macOS compresses pages, so RSS under-reports. Measure it at a smaller size
and scale up, using `footprint <pid>` or the `peak_gb` that `heavyq.py status` shows for the group.
- The queue starts a job only when free+inactive ≥ est_gb + 8 GB.
- If the job turns out larger and itself drives free+inactive below the floor (or swap up), the queue raises the job's need to
  1.1 × the observed peak (`est_gb_learned`).
- `est_gb` must be below the 52 GB hard ceiling. A footprint above 52 GB triggers an immediate SIGKILL, and the job is marked `failed`.

## 2. SIGTERM: write a checkpoint, then exit 75
Install a handler for SIGTERM and SIGINT that only sets a flag. At the next safe point (a step boundary), write the checkpoint
(see 4) and exit **75**. All of this must finish within the grace period: 300 s by default, or `--grace S` for the job. After the
grace period the whole process group gets SIGKILL. Never ignore SIGTERM. A job that ignores it is killed and loses everything
since its last checkpoint (`test_cycle` step 8 shows this).

| exit code | meaning | queue action |
|---|---|---|
| 0 | the work is **complete** (and `--done-file`, if declared, exists) | `done` |
| 75 | checkpoint written, resumable (after SIGTERM, or a voluntary yield) | `paused`; later run with `resume_cmd` |
| anything else, or killed | crash | `paused` and retried with `resume_cmd`, up to 3 times; then `failed` |

After a SIGTERM the queue treats any exit as a yield and marks the job `paused`. An exit code other than 0 or 75 at that point is
logged as a contract warning.

## 3. A `--resume` path
`resume_cmd` (usually `cmd --resume`) is used for every run after the first. It must:
- **exit 0 at once if the result is already complete.** It must be idempotent, because a job can finish just as it is told to yield.
- **continue from the newest complete checkpoint when one exists.** The result must be bit-identical to an uninterrupted run, or
  within a tolerance stated in the lane's frozen criteria. An example of such a tolerance is thread-order jitter in parallel
  reductions. Every run of a job gets the same `threads`.
- **start from scratch when there is no checkpoint.**

Prove this at a small size before queueing. Run the job once uninterrupted, then again with SIGTERM followed by `--resume`, and
compare the two outputs, as `test_cycle.py` does. Keep that evidence with the lane.

## 4. Write outputs atomically
Write every output and checkpoint the same way:
1. Write a temporary file in the same folder.
2. Flush and `fsync` it.
3. Move it into place with `os.replace()`.

The previous checkpoint stays valid until the new one is complete. A kill at any instant then leaves either the old file or the
new one, never a torn file.

Name outputs by job. Mutation and other modes write separate outputs.

## 5. Rolling checkpoints (recommended for anything longer than about 30 minutes)
Some exits leave no time to checkpoint on the spot:
- the grace kill;
- an emergency kill when swap grows by more than 4 GB (CFG960's frozen rule) or free disk drops below 5 GB;
- a crash;
- a reboot.

In each of these cases the next run resumes from the last rolling checkpoint. A reboot also stops the daemon. Once the daemon is
started again, it finds the job gone and resumes it.

## 6. Process hygiene
heavyq runs `bash -c "<cmd>"` in `--cwd` (relative to the repo root), with nohup and nice 5, in a process group of its own.
SIGTERM goes to the **whole group**.
- bash executes a single command directly, so that program receives the signal and its exit code is the job's.
- A wrapper script should `exec` its last command (`exec python3 engine.py "$@"`), or trap TERM, wait for its child and pass on
  the child's exit code.
- Leave no background process behind. The job counts as running until its process group is empty.

## 7. Environment heavyq provides
- `HEAVYQ_JOB_ID`
- `HEAVYQ_RUN` (1, 2, …)
- `HEAVYQ_RESUME` (0 or 1)
- `HEAVYQ_YIELD_EXIT=75`
- `HEAVYQ_THREADS`

`OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `VECLIB_MAXIMUM_THREADS`, `NUMEXPR_NUM_THREADS` and
`NUMBA_NUM_THREADS` are all set to the job's `--threads` (default 12, which leaves 4 cores for the lanes). Pass extra variables
with `--env K=V`.

## 8. Disk
A job starts only with at least 30 GB free. A running job yields when free disk drops below 30 GB and is killed below 5 GB.
Checkpoints count toward disk use, so state the checkpoint size in `--note`.

## 9. Frozen-criteria lanes
Adding a SIGTERM handler or a resume path to a frozen engine changes the engine. Register the change the way the lane registers
other engine changes (an amendment, before any production number), and attach the small-size resume-equivalence evidence.

An engine that already resumes from a rolling checkpoint when restarted (CFG960's engine, for example) can be queued with
`cmd` = `resume_cmd` even without a handler. SIGTERM then kills it with the default action. It loses only the work since its last
checkpoint, and the queue logs a contract warning.

## Skeleton (Python)
```python
import os, signal, sys
STOP = []
signal.signal(signal.SIGTERM, lambda s, f: STOP.append(s))
signal.signal(signal.SIGINT, lambda s, f: STOP.append(s))
YIELD_EXIT = int(os.environ.get("HEAVYQ_YIELD_EXIT", "75"))

if "--resume" in sys.argv and result_complete(): sys.exit(0)
state = load_checkpoint() if "--resume" in sys.argv and checkpoint_exists() else fresh_state()
while not state.done:
    if STOP:
        save_checkpoint_atomically(state); sys.exit(YIELD_EXIT)
    state.step()
    if state.n % EVERY == 0: save_checkpoint_atomically(state)     # rolling
write_outputs_atomically(state); sys.exit(0)
```

## Opt in
```bash
python3 compute_queue/heavyq.py add --id <JOB> --cwd <lane folder, repo-relative> \
    --cmd "python3 run.py <args>" --resume-cmd "python3 run.py <args> --resume" \
    --est-gb <peak footprint GB> --threads 12 --priority 10 --done-file <result path, relative to cwd> --note "<ckpt size, lane>"
```
