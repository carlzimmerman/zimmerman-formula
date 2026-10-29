# NL1_native_level_L: the native zooms give L ≈ 4.9; at that level three cluster keys over-pull (native level fails; convergence inconclusive)

**Provenance:**
- Criteria `FROZEN_CRITERIA.md` (7493e2902a) and the script (52b354a1f3) were committed **before any ng 64 zoom
  finished**.
- A1 (8ecf0a1a04): a forked-pool pickling fix, code only. It was committed alone after the measurement printed and
  before any grade; the first log is kept as `run1_pickle_error.log`.

κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

## Measurement (X48's own `measure()`, all 9 ng 64 seeds at 10^12 M☉ flagged ok)

| seed | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| c_f | 6.10 | 9.24 | 3.14 | 14.50 | 10.02 | 7.74 | 2.44 | 4.01 | 15.09 |

- **Median** c64 = 7.74, against 11.63 at ng 48, so R = 0.6655.
- **L_nat = 7.31 R = 4.865**, with a 68 % bootstrap interval of [3.831, 5.805].

## Verdict (frozen): **NATIVE LEVEL FAILS: G-MID-T3, G-OUT-all, G-IN-Mall (all OVER) [CONVERGENCE INCONCLUSIVE]**

| graded at | canonical | alt |
|---|---|---|
| **L_nat 4.865, T 12.3 (PRIMARY)** | **FAIL**: G-MID-T3, G-OUT-all, G-IN-Mall (OVER) | adds the SPARC line and MW ultra-faints (known alt lines) |
| L68 low 3.831, T 12.3 | FAIL: groups only, Z **+2.05** (the line is 2.00) | known alt lines + groups |
| L68 high 5.805 | FAIL: 5 cluster keys (OVER) | as canonical + known alt lines |
| CL3 crossover T 11.59 at L_nat | FAIL: clusters + lensing (+400.4) | as canonical |
| uncorrected L 7.31 (R = 1) | FAIL: 8 cluster keys (OVER) | as canonical |

## Reading

- **Resolution moves the native level toward the data, but not fully.** It goes from 7.31 at ng 48 to about 4.9 at
  ng 64, a factor 0.67, against the ≈ 3.6–4.2 band where every canonical line passes (LEE1).
- **At the central value the cluster cores are too dense** (OVER). The low end of the 68 % interval misses only the
  groups line, by 0.05σ.
- **Convergence is not established.** The per-seed spread is 2.4–15.1. A parallel audit (CSM2, c259bbc116) found the
  first-crossing estimator binning-sensitive for some seeds. The ng 64 runs are not the same realisations as ng 48.
  A further resolution step would be needed before the native L can be called measured.
- **The CL3 "T from L" variant fails lensing badly here too (+400).** That is consistent with the parallel CSM1
  correction: the constant-coefficient switch is inconsistent with the S9 core.

**L stays located by data.** The native zooms are compatible with it at the edge of their 68 % range, not at their
centre.

## Checks: 4/4

- **K0:** X48's `measure()` passes its synthetic NFW control (3.837 against 4); LEE1's Step-0 checks pass.
- **K1:** the A2 medians are re-read exactly.
- **K2:** peak RSS < 1 GB.
- **Rerun:** byte-identical.
- **MUTATE twin** (A2 reference × 1.1): K1 fails, exit 1.
