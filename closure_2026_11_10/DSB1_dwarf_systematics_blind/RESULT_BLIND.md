# DSB1 blind result: STOPPED AT KA-c (frozen reading; no class label)

Criteria 2c7beb7b92 (committed alone before any script). Script dsb1.py, outputs dsb1.out / dsb1.json, run 2026-11-10,
nice -n 19, one thread, about 1 s before the stop. RB2's and DG1's results were NOT opened. No form B class residual of the
real data was computed: the script stops before grading.

## Label (frozen reading)

**NO LABEL: grading stopped at known answer KA-c**, as FROZEN section 5 requires. Per class, per footing: not graded.

## Known answers

- **KA-a PASS.** X1's build copied (seed 20261031): Delta[Newton] and sdMC of all 178 rows (both footings) reproduced
  exactly (max |d| 0.0, line 1e-9). My own central-value residual function against X1's medians: median |d| 0.0035 dex,
  max 0.053 dex (lines 0.01 / 0.06).
- **KA-b PASS.** Fornax log M_1/2 = 7.976 against Campbell+2017's Wolf value 7.88 (|d| 0.096, line 0.15; PROVISIONAL look-up)
  and LVD's mass_dynamical_wolf 7.98 (|d| 0.004, line 0.05).
- **KA-c FAIL.** Form B's limits pass (r_J -> inf is the isolated law exactly, r_J -> 0 Newton to 0, deep-MOND virial 7e-6),
  and budget-off recovery of a planted +0.40 dex is exact (3e-16). The full-budget recovery of +0.40 misses the 0.10 dex line
  in two classes on both footings: MW classical +0.304 / +0.296, Coma UDGs +0.337 / +0.314 (canonical / alt); MW ultra-faint
  +0.404 / +0.400 and bright M31 +0.344 / +0.325 are inside.

## Cause of the KA-c failure (diagnosed on the mock only; no real-data residual involved)

Each term switched on alone in the canonical +0.40 mock (shift of the recovered class residual, terms above 0.005 dex):

| class | shift by term |
|---|---|
| MW ultra-faint | T11 +0.006 |
| MW classical | T10 -0.128, T1 +0.009 |
| bright M31 | T10 -0.042, T1 +0.006 |
| Coma UDGs | T8 -0.058, T17 -0.009, T1 +0.008 |

1. **T10 (binaries in the 4-10 km/s systems) is one-sided by its frozen prior** (Minor+2010 inflation U[0, 0.30]): it moves the
   class centre down by its mean effect (2 log10 1.15 ~ 0.12 dex for a class where most rows have sigma < 10 km/s). The mock
   was built at the nominal data side without that inflation, so the recovery check as frozen could not pass for a class whose
   budget has a one-sided term. This is an error in the specification of KA-c, not in the pipeline: a planted mock must be drawn
   with the budget's own truth (here, inflated dispersions), or the check must be differential.
2. **T8 on the Coma mean is a construction bias of the frozen pipeline.** Coma's errors are large (e.g. 18 +- 13 km/s), the
   draws are symmetric in sigma and the statistic is the mean of log sigma^2, so the class mean shifts down by Jensen's
   inequality (-0.06 dex). The dSph classes use a median and do not show it.

What follows is in AMENDMENT_2026-11-10_KA_c.md (committed alone, after this file) and in the amended reading of this file's
successor, both clearly post-freeze. This frozen reading stays: STOPPED AT KA-c.

## What was not checked

Everything after the known answers: no class residual, interval, MDO, label, width table or mutation exists in this reading.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
