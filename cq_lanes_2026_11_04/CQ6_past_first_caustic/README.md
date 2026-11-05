# CQ6_past_first_caustic: IN PROGRESS (status file; the headline will be replaced by the result)

κ = ½ FITTED; not theory closed. Criteria `FROZEN_CRITERIA.md` (8131404df6, committed alone first). Not blind. Adopts nothing. No particle; the cold sector stays retired.

**Where this stopped (status).**
- `cq6.py` is written. The frozen ladder (`python3 cq6.py all`) is running, writing `cq6.out` and `runs/`.
- A post-result diagnostic, `cq6_explicit_diag.py` (no label weight), runs after it and writes `cq6_explicit_diag.out`.
- **Bug fix before the frozen runs.** The first smoke test had a wrong velocity update in the implicit-midpoint step
  (2(y−x)/dt − v instead of 4(y−x)/dt − v). It was found because nothing moved. It is fixed in the committed script.
- **What the smoke tests showed** (N 256, scratch output, not the frozen runs). The regulated run fails at 64 substeps
  just after the first bounce: t = 3.216 at dt 1e-3, 3.180 at dt 2e-4 and 3.274 at dt 5e-5. Its energy error first
  exceeds the 1e-3 line at about t 3.1–3.2. With λ = 0 the run crosses at t = 3.000025, against t_c = 3.

If this file still says IN PROGRESS, read `cq6.out` and `cq6_explicit_diag.out`. The label follows FROZEN_CRITERIA
section 6.
