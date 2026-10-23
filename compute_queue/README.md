# compute_queue: a preemptible heavy-compute queue

The owner asked for this on 2026-10-23: *"heavy compute should be able to save progress and make room for progress we are working
on and pick back up whenever they land.. that way we are constantly computing but we aren't stuck trying to push doors waiting
for large runs to finish."*

**Start** (from the repo root, once; a pidfile lock refuses a second instance):

    nohup python3 compute_queue/heavyq.py daemon >/dev/null 2>&1 &

The daemon is not running yet. The coordinator will start it once the first real job (lane L1's v3 production run) can be
queued.

## Use
- `python3 compute_queue/heavyq.py status` shows the running job, its footprint, free memory, swap, the queue, and why the next
  job is not starting. Add `--json` for the raw data. The daemon also writes `compute_queue/status.json` every 30 s.
- `python3 compute_queue/heavyq.py add --id ID --cmd ... --resume-cmd ... --est-gb G [--cwd DIR] [--priority P] [--threads T]`
  queues a job. What a job must do first is in [JOB_CONTRACT.md](JOB_CONTRACT.md).
- `python3 compute_queue/heavyq.py pause ID` makes the job checkpoint and hold. `resume ID` releases the hold (or re-queues a
  failed job). `remove ID` takes a job that is not running off the queue.
- `touch compute_queue/YIELD` makes the running job checkpoint, and nothing starts while the file exists. `rm compute_queue/YIELD`
  lets the queue resume.
- `kill $(cat compute_queue/heavyq.pid)` stops the daemon only. The job keeps running and the next daemon adopts it. To stop
  everything, touch `YIELD` first.

## Rules (defaults; override any of them in `compute_queue/config.json`, which the daemon re-reads every poll)
- **Start:** the highest-priority queued or paused job, one at a time, starts when all of these hold, and have held for 120 s:
  - no known heavy run (the 1024³ engines and launchers) is live;
  - free+inactive ≥ est_gb + 8 GB;
  - free disk ≥ 30 GB;
  - no other process has a footprint above 4 GB;
  - no `YIELD` file exists.
- **Yield:** the job gets SIGTERM, and has 300 s to checkpoint before SIGKILL, when any of these happens:
  - free+inactive drops below 6 GB;
  - swap grows by more than 2 GB since the run started;
  - a `YIELD` file appears;
  - another process goes above a 4 GB footprint;
  - a known heavy run appears;
  - free disk drops below 30 GB;
  - someone runs `pause`.

  The job is then `paused`, and is resumed with `resume_cmd` once the conditions clear.
- **Abort:** an immediate SIGKILL when the footprint passes 52 GB (the job is marked `failed`), when swap grows by more than
  4 GB, or when free disk drops below 5 GB.
- **Measurements:** memory is read through libproc phys_footprint, summed over the job's process group, because RSS
  under-reports on macOS. Free memory comes from `vm_stat` free+inactive, and swap from `sysctl vm.swapusage`. The tool uses the
  Python standard library only.

## Files
- `heavyq.py`: the daemon and the command-line interface.
- `JOB_CONTRACT.md`: what a job must do before it can be queued.
- `test/dummy_job.py` and `test/test_cycle.py`: the full-cycle test. Run it with `python3 compute_queue/test/test_cycle.py`. Its
  output is `test/test_cycle.out` and `test/test_cycle_result.json`.
- Runtime files are gitignored: `queue.json`, `status.json`, `config.json`, `logs/<id>.log`, `heavyq.log`, `heavyq.pid` and
  `YIELD`.
