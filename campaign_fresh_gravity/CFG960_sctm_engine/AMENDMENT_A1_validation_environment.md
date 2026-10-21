# CFG960 AMENDMENT A1 (2026-10-21): allocator setting for the 128³ validation processes (engineering only; committed alone)

Added after FROZEN_CRITERIA.md (6fc440225), during the validation stage, before any gate was evaluated. No rule, input, statistic,
tolerance or gate line changes.

**What happened.** The first pass of the 128³ job set ran VS0 (peak RSS 0.85 GB) and VK (0.95 GB) to completion; VC was stopped by
the in-script 1 GB RSS guard at 1.017 GB, after which the remaining jobs were cancelled. Their physical footprint never exceeded
0.24 GB. A probe of the same engine functions (`vmmap --summary` on the probe's own process) shows where the difference comes from.
macOS counts in RSS:
- 400 MB of freed but unreclaimed large blocks (MALLOC_LARGE_REUSABLE);
- 250 MB of empty medium-zone regions;
- about 370 MB of shared-library text and link-edit pages.

None of this is live memory. With the macOS allocator's space-efficient mode (`MallocSpaceEfficient=1` in the process environment),
the probe's RSS falls from 1.08 GB to 0.24 GB at the same footprint.

**Change.**
- Every CFG960 validation process (the six 128³ jobs, LAW, SCOREK) is started with `MallocSpaceEfficient=1`.
- The in-script guard is unchanged: it still aborts at 1 GB of peak RSS (`ru_maxrss`), and V-MEM is still graded on RSS.
- All six 128³ jobs are rerun with the setting, so every gate uses one uniform set.
- The first-pass outputs are superseded and were not graded. VS0's and VK's first-pass JSONs were not compared with anything; the
  cancelled VC / VSC attempts left no complete JSON.

**Why this is not a science change.** The setting changes only how freed memory is returned to the kernel. Arithmetic does not depend
on it: the stored density and gravitating fields of differently allocated runs were bit-identical in the 64³ smoke tests (see the
README). The 1024³ production environment is fixed in FROZEN_CRITERIA_1024.md.

**Also disclosed.**
- Before any 128³ number existed, `stage()` markers were added to the engine's own passes. These are the CFG654 engine's
  malloc-relief calls; they change no number.
- 64³ smoke runs were made in a scratch folder outside the repository: SCT, conversion-off and S0REF, with numbers not used. In them,
  conversion-off reproduced S0REF's fields bit for bit. Only one particle-P(k) snapshot differed, by 3.4e-8, which is
  measurement-level and inside V-K's 1e-6 line.

κ = ½ FITTED; footings never pooled; not theory closed.
