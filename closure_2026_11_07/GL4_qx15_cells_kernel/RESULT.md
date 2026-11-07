# GL4: QX15's cells C1-C4 and P1 re-read with the Limber k^-4 restored. C3 MOVES (TENSION -> PASS) on both footings; C1, C2, C4 and P1 HOLD

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (626564bed8), pushed alone before any
script. Script: gl4.py (main 54 s, peak RSS 0.87 GB; MUTATE 23 s, 0.73 GB). Outputs: gl4.json / gl4.out, gl4_MUTATE.*,
run_main.txt, run_mutate.txt. QX15 and QX10 are imported or exec'd read-only, and no other lane's file is written.

**Moved labels are REPORTED here, not rewritten in QX15. The owner decides.**

- **The error** (F1A 7026dcb48e; GL2 d0c3692fc6 CONFIRMED). QX15's `do_cells` execs QX10 iter_1's `jcheck`, whose
  `Sfull` has no (chi/(L + 1/2))^4. GL4 rebuilds `do_cells`' source with QX15's own patches plus one exponent patch:
  n = 0 is the record, n = 4 is corrected, n = 2 is the MUTATE.
- **Corrected S.** With n = 4, max |1 - S| is 2.8e-6 / 1.6e-6 / 1.0e-5 / 2.8e-6 (C1-C4), against 0.124 / 0.061 / 0.525 /
  0.111 in the record. With the correct weight, these cells' Jeans suppression does not reach the scales that lens the
  CMB.

## Per cell: old vs corrected (canonical / alt)

| Cell | Record Delta_cell (refit) | Record label | Corrected Delta_0 (n = 4, no refit) | Corrected label | Verdict |
|---|---|---|---|---|---|
| C1 | +0.66 / +0.67 | PASS | +1.1e-5 / +1.1e-5 | PASS | **HOLDS** |
| C2 | +0.27 / +0.28 | PASS | +6.5e-6 / +6.6e-6 | PASS | **HOLDS** |
| C3 | +5.95 / +6.03 | TENSION | +4.1e-5 / +4.2e-5 | PASS | **MOVES** to PASS |
| C4 | +0.57 / +0.58 | PASS | +1.1e-5 / +1.1e-5 | PASS | **HOLDS** |
| P1 (flat S = 0.5, power control) | +192.46 / +189.91, bites | control bites | kernel-free (reproduced exactly, KA1) | bites | **HOLDS** |

- Delta_0 is at the main-fit theta. A refit can only lower it, so Delta_0 <= 4 is a PASS without a refit, and no refit
  ran.
- P1 still bites, so C1-C4 keep their power and are labelled.
- QX15's main fits (PASS) and MB control are kernel-free (F1A step 2) and untouched.

## Known answers and MUTATE

- **KA0, error re-inserted (n = 0):** S equals QX15's parts/cellS.npz in all four cells, max |d| 0.0. The fully covered
  L is 917 / 917. **PASS.**
- **KA1:** QX15's objective at each recorded best-fit theta, with the recorded S, reproduces every recorded chi^2_PA:
  main, C1-C4 and P1, both footings. The largest |d| is 1.1e-9, and Delta_cell is reproduced to 4 decimals. **PASS.**
  - The nuisance profile was started at each record's own nuisances (disclosed).
- **KA2:** n = 4 max |1 - S| at L <= 2500 is 6.3e-6 / 4.4e-6 / 1.8e-5 / 7.2e-6, consistent with GL1's L9 (<= 1.8e-5).
  **PASS.**
- **MUTATE M1 (n = 2):**
  - max |1 - S| is 3.8e-3 / 1.9e-3 / 1.6e-2 / 3.4e-3, different from both n 0 and n 4.
  - Delta_0 is +0.018 / +0.009 / +0.096 / +0.016 (canonical) and +0.019 / +0.009 / +0.098 / +0.017 (alt), different
    from n 4.
  - **BITES.**

## Limits

- **Grid ceiling, as recorded.** Both n's keep QX15's coverage clamp: S is held at its L 917 value above L 917, because
  the solver's k grid stops at 10 /Mpc. At n = 4 the clamped value is within 1e-5 of 1, so the clamp is harmless here.
- **Same framework, separate code.** The kernel itself was checked independently by GL2, not by GL4.
- **Not independent evidence for the sector.** These cells were already killed elsewhere (QX10 G6: hosts retain the
  sector, and KiDS is over-predicted). GL4 changes only the primary-CMB cell reading.

Kappa = 1/2 FITTED; not theory closed.
