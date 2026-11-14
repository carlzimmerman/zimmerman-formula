# AGB7 — CFG684 and CFG689 re-read with the age slope that is left in the DES distances

2026-11-14. Criteria: `FROZEN_CRITERIA.md` (committed alone, before any script). No amendment. A re-read of two of
this repository's own lanes; adopts nothing, edits no ledger.

## Verdict
**At the slope actually left in the DES distances (0.23 of the published size) both lanes hold.** CFG689's tracking
curve is STABLE at every redshift, in both modes and both samples, and stays so at the 0.35 bracket. CFG684's
flat-a0 Ω_m moves by 0.010, just inside its combined error, and reads ROBUST; at the bracket it moves by 0.015 and
reads AGE-DEPENDENT.

| lane | label at A = 0.23 | second word (A = 0.35) |
|---|---|---|
| CFG684 A2, flat-a0 Ω_m (all four sample × combination cases) | ROBUST | FRAGILE (0.35: AGE-DEPENDENT) |
| CFG684 A1, degeneracy | NOT BROKEN | ROBUST |
| CFG684 A3, floor at z 2.33 | FLOOR HOLDS (`full`), FLOOR LOST (`des_only`) | ROBUST (both as at A = 0) |
| CFG689 B1, tracking √X at z* 1.0, 1.2, 1.5, 2.33 (D5 and TD5F, `full` and `des_only`: 16 cases) | STABLE | ROBUST |
| CFG689 B2, class (4 cases) | CLASS UNCHANGED | ROBUST |

For comparison, AGB1's Part B at the full published size (A = 1): CFG684 AGE-DEPENDENT; CFG689 SHIFTED at z* 1.0
and 1.2.

**One reported number does move** (no label under the frozen rules): CFG689's own test of free nodes against
constant dark energy, on the whole sample. See below.

## Harness checks
| check | result | |
|---|---|---|
| H1, CFG684 `full` at A = 0 against the committed `cfg684_results.json` | largest difference 0 | PASS |
| H2, CFG684 `full` at A = 1 against AGB1's committed run | largest difference 0 | PASS |
| H3, CFG689 TD5F `des_only` at A = 1 against AGB1's committed run | largest difference 0.0000 in the tracking quantiles | PASS |

All 17 runs completed; none exited on a guard; every CFG689 chain check is ok at the frozen 60,000 steps.

## CFG684 (each run against A = 0 of the same sample)
| sample, combination | Ω_m at A = 0 | at 0.23 | shift | combined sd | at 0.35 | shift |
|---|---|---|---|---|---|---|
| `full`, BAO+DES5 | 0.3067 ± 0.0074 | 0.3166 ± 0.0075 | +0.0099 | 0.0105 | 0.3220 ± 0.0075 | +0.0153 |
| `full`, BAO+DES5+CC | 0.3070 ± 0.0073 | 0.3170 ± 0.0075 | +0.0100 | 0.0105 | 0.3218 ± 0.0076 | +0.0149 |
| `des_only`, BAO+DES5 | 0.2917 ± 0.0085 | 0.3004 ± 0.0084 | +0.0087 | 0.0120 | 0.3050 ± 0.0083 | +0.0133 |
| `des_only`, BAO+DES5+CC | 0.2920 ± 0.0080 | 0.3009 ± 0.0085 | +0.0089 | 0.0116 | 0.3054 ± 0.0080 | +0.0134 |

- The shift scales with the amplitude: 0.21 to 0.23 of the A = 1 shift at 0.23, and 0.32 to 0.35 of it at 0.35.
- On `full` the ROBUST reading at 0.23 is thin: 0.0099 against 0.0105.
- Δχ²_max stays below 2 everywhere (NOT BROKEN). The tracking band at z 2.33 on `full` moves from 0.69–2.17 to
  0.87–2.28 (0.23) and 1.12–2.33 (0.35).
- Reported, the sample's own drift at 0.35 in the place of the cosmic-average template: Ω_m shifts by +0.0097 on
  `full` (would read ROBUST) and by +0.002 on `des_only`.

## CFG689 (tracking √X, median and 68 % band; each run against A = 0 of the same sample)
| mode, sample | z* | A = 0 | A = 0.23 | A = 0.35 |
|---|---|---|---|---|
| TD5F, `full` | 1.0 | 0.973 [0.912, 1.031] | 0.994 [0.932, 1.053] | 1.005 [0.943, 1.065] |
| | 1.2 | 0.949 [0.895, 1.003] | 0.970 [0.914, 1.025] | 0.981 [0.924, 1.036] |
| | 1.5 | 0.912 [0.781, 1.032] | 0.934 [0.796, 1.055] | 0.942 [0.803, 1.065] |
| | 2.33 | 0.879 [0.678, 1.045] | 0.897 [0.693, 1.066] | 0.907 [0.703, 1.078] |
| TD5F, `des_only` | 1.0 | 0.932 [0.870, 0.991] | 0.950 [0.888, 1.011] | 0.960 [0.897, 1.023] |
| | 2.33 | 0.848 [0.654, 1.009] | 0.866 [0.669, 1.030] | 0.879 [0.679, 1.043] |
| D5, `full` | 1.0 | 0.950 [0.811, 1.057] | 0.979 [0.845, 1.085] | 0.996 [0.865, 1.101] |
| | 2.33 | 0.908 [0.338, 1.207] | 0.960 [0.432, 1.253] | 0.992 [0.487, 1.277] |
| D5, `des_only` | 1.0 | 0.934 [0.805, 1.036] | 0.963 [0.837, 1.064] | 0.978 [0.854, 1.078] |
| | 2.33 | 0.953 [0.506, 1.222] | 1.001 [0.583, 1.266] | 1.029 [0.615, 1.289] |

The medians rise by 0.02 to 0.05 at 0.23, about a fifth of the A = 1 shift, and stay well inside the bands. The
tracking curve near z 1 stays at or a few per cent below today's value (medians 0.95 to 0.99 at A = 0.23). (The
other z* rows are in `agb7_collect.out`.)

**Reported, no label: CFG689's constant-dark-energy test (its P2) and native H0.**
| mode, sample | P2 at A = 0 | at 0.23 | at 0.35 | native H0: 0 → 0.23 → 0.35 |
|---|---|---|---|---|
| TD5F, `full` | 2.00σ, HINT | **3.85σ, EVOLVING DE REQUIRED** | 4.89σ, EVOLVING DE REQUIRED | 67.73 → 66.75 → 66.24 |
| D5, `full` | 1.38σ, CONSISTENT WITH CONSTANT | 2.89σ, HINT | 3.74σ, EVOLVING DE REQUIRED | 67.85 → 66.88 → 66.38 |
| TD5F, `des_only` | 1.61σ, CONSISTENT WITH CONSTANT | 1.91σ, CONSISTENT WITH CONSTANT | 2.24σ, HINT | 69.27 → 68.31 → 67.80 |
| D5, `des_only` | 1.22σ, CONSISTENT WITH CONSTANT | 1.50σ, CONSISTENT WITH CONSTANT | 1.80σ, CONSISTENT WITH CONSTANT | 69.40 → 68.45 → 67.94 |

On the whole sample that test is sensitive to even the leftover drift: in the tight mode it goes from a 2σ hint to
3.85σ. On DES alone it stays consistent with constant dark energy. The difference is the legacy low-redshift
set again, as in LGS1 and AGB1. The native H0 falls by about 1.0 at 0.23 and 1.5 at 0.35.

## Limits
- 0.23 is AGB3's measurement on photometric host ages with a simple age model; 0.35 allows for noise in those ages
  by an estimate made after the fact (AGB6). Neither is adopted.
- The drift has the cosmic-average shape of AGB1's template. AGB3 found this sample's own age drift to be smaller
  and concentrated between the legacy set and DES; with that shape CFG684 moves less (reported row).
- A fit cannot tell age from anything else with this redshift shape.
- CFG684's ROBUST reading on `full` is 6 % inside its line.
- AGB1's Part B stands as the reading at the full published size.

## Files
`FROZEN_CRITERIA.md`; `agb7_reread.py` (harness), `agb7_collect.py`; outputs `agb7_cfg684_<sample>_<template><100 A>.{json,out}`
and `agb7_cfg689_<mode>_<sample>_S<100 A>.{json,out}`; `agb7_results.json`, `agb7_collect.out`.

Commits (local / origin): criteria 5007b5beb8 / d65e88928d; scripts 4335bfe123 / 92e3ca7de3; result e876d9717b /
f15a648071.

## Note added 2026-11-14: blind re-grade
**AGB7R** (`closure_2026_11_14/AGB7R_blind_reread_leftover_slope/`), a second harness written from
`FROZEN_CRITERIA.md` and the inputs it names, repeats the runs and reaches every label, first and second word, with
numbers identical to the printed digit. It notes, as above, that CFG689's constant-dark-energy test on the whole
sample is the number that moves.

kappa = 1/2 FITTED; not theory closed.
