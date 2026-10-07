# CFG422: is the x = 0.4 confinement benefit robust across seeds and footings? ROBUST BENEFIT (256³)

The criteria (FROZEN_CRITERIA.md) were committed before any run. The runs used `run_422.py`, and the frozen verdict comes from `cfg422_analysis.py` (output in `cfg422_analysis.out`).

| seed | footing | confined σ₈ ratio | confined max\|P−1\| | unconfined max\|P−1\| | benefit Δ |
|---|---|---|---|---|---|
| 359 | canonical | 1.0028 | 0.041 | 0.153 | +0.112 |
| 359 | alt | 1.0037 | 0.056 | 0.193 | +0.137 |
| 360 | canonical | 1.0026 | 0.040 | 0.142 | +0.101 |
| 360 | alt | 1.0035 | 0.056 | — | — |
| 361 | canonical | 1.0025 | 0.039 | 0.139 | +0.100 |
| 361 | alt | 1.0033 | 0.051 | — | — |

- **GROWTH OK:** 6/6 confined runs pass CFG361's cuts. All 4 unconfined runs are TENSION.
- **Verdict:** ROBUST BENEFIT. Δ ≥ 0.10 in every comparison, and the confined run is never worse.

**Caveats.**
- At 256³ the 0.4 r_ta cover is under one cell for median hosts, so this is a robustness check, not a confirmation.
- The x = 0.4 radius is still set by hand. CFG416 (512³, running) tests whether each halo's own supply edge does the job with nothing tuned.
- The 512³ alt-footing run of CFG414 is still running.
