# CFG338 FROZEN CRITERIA: is the cold share set by the original (pre-reionisation) baryons?

**Lane:** orchestrator; the lead flagged by CFG336. The owner asked for "deep dive solutions" to the UFD failure.

**Hypothesis.** Each dwarf's cold component is the cosmic share of its ORIGINAL baryons, M_c = R_ind · M_b,now / f_b, while the law still reads today's baryons. R_ind is the baryon-loss factor measured independently of dynamics: CFG317's leaky-box effective yield, at the fiducial yield −0.2. Population medians:

| population | log R_ind | R_ind |
|---|---|---|
| MW UFDs | 2.069 | 117 |
| MW classicals | 1.484 | 30.5 |
| M31 Collins | 1.349 | 22.3 |
| M31 LVD | 1.349 | 22.3 |
| LV field | 0.769 | 5.9 |

These values come only from CFG317's committed JSON (numbers.RIND["-0.2"]); none is tuned.

## Method
- Base: CFG336's harness, copied, with exactly the same samples, estimator, errors and both footings.
- Change: its global multiplier on M_c becomes the population's R_ind.
- Readings:
  - **(M) primary:** CFG4 T5 max bookkeeping, g = g_N + max(phantom, cold).
  - **(S):** B's f_ex rule; reported.
- Profiles:
  - **PB (primary):** the whole cold share inside r. This is the most favourable case, and an upper bound on the effect.
  - **P1 (reported):** z_f = 8 for UFDs, 3 for the others, as in CFG336.

## Decision (reading M, profile PB, both footings)
- **SOLVES:** UFDs within 2σ, AND the MW classicals, M31 Collins, M31 LVD and LV field all within 2σ.
- **PARTIAL:** the UFD offset is halved or better, with at most one other population pushed beyond 2σ.
- **NOT:** otherwise.

## Controls
- **C1:** with R_ind = 1 everywhere, the run reproduces CFG336's M·PB row.
- **MUTATE** (CFG338_MUTATE=1, separate outputs): the R_ind values are permuted across populations. The decision row must change or degrade.

## Pre-freeze disclosure
- Known before freezing: CFG336's k-needed values (PB: 5.9 for 2σ, 13.2 for zero) and CFG317's R_ind medians.
- Expected tension: the same rule also raises the classical and LV cold mass.
