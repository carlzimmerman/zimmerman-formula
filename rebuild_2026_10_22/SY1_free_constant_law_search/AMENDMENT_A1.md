# SY1 Amendment A1, 2026-11-02, committed alone, before any real-run number

Owner's instruction. This changes only the start condition.

The criteria's Run section says the search starts when BF1's `L4.done` exists. Instead, it starts now and runs alongside BF1's live L4 run, at nice 10, on about 8 cores. It still yields to any 1024^3 run or compute_queue heavy job, checkpoints on SIGTERM, and resumes.

Gates, data, split, controls and labels are unchanged. Run length isn't affected by this amendment; it's fixed in the README before launch.

kappa = 1/2 FITTED; not theory closed.
