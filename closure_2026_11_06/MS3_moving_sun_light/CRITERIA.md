# MS3 frozen criteria: the moving-Sun door (v3s and AC2q), a fourth rung at both Mach numbers within 1 GB

Frozen before any MS3 script, run or number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.
No dark-matter particle, no LCDM input. Both footings graded, never pooled. AC15, AC24, MS1 and MS2 files are
read only.

## Why, and what was seen before this freeze

MS2 (criteria 92b0894440, result e70987511a) is NO VERDICT. Every number MS2 printed was seen before this
freeze; the choices below were made knowing them.

- **M490 CONV.** 6 q_B series are PRE-ASYMPTOTIC on coarse / medium / fine. Worst is G1 Earth, p 0.44, rung
  means 1.93e-2, 1.23e-2, 7.09e-3.
- **M490 MUTATE k = 0.1.** It fails in 3 cells (canonical footing, V = 220, G2 Mars, q_B). G2 is
  max - min of |a| over theta, which is not additive, so plant and base grid error mix. The planted series
  (0.188, 0.180, 0.163) reads DIVERGENT although its base is MONOTONE.
- **M234 CONV, interim.** 23 q_B series are DIVERGENT on coarse / medium / fine.
- **The fourth rung.** MS2's ultra run (M234 only) held 2.15 GB RSS against the 1 GB line and was stopped
  at t 1.6. The cause is the solver's whole-grid numpy temporaries: about 375 grid-sized float64 arrays at
  peak on the 1109 x 644 ghost grid.
- **Diagnostic D: DISTRIBUTED.** 99.85 % of the q_B rung change lies at r > 100 R_A.
  - The gate radii are Earth 27.3 / 76.7, Mars 41.6 / 116.9 and Saturn 261.4 / 735.2 R_A (V = 220 / 369).
    So r > 100 R_A is not outside the gates' region: it holds Saturn at both V, and Earth and Mars at V = 369.
  - A nested grid refined only inside the planets' region, with the outer field taken from a coarse run,
    would therefore not refine where the change is. It is rejected for that reason.

## C1. The memory choice (frozen)

The fourth rung is **ultra**: dln r = 0.00625 and 640 theta cells, half of fine in both directions, on the
whole domain r in [2, 2000] R_A. It is run at **both** M_inf = 234 and 490: TRANSMIT UNIFORM, t_end 1000,
snapshots at t = 800, 850, 900, 950, 1000.

The solver is hydro_ms3.py: AC24's hydro_ac24.py with three changes, and the diff is committed.

1. The `ultra` resolution choice, as in MS2's hydro_ms2.py.
2. **Chunked right-hand side.** rhs() is evaluated in radial blocks of `--chunk` interior rows (default 64).
   Each block reads 2 ghost rows on each side and executes the same elementwise expressions on slices.
   - bc(), the time step and the RK2 update are unchanged.
   - Storage stays float64. float32 is not used. Out-of-core storage is not used.
   - Because every operation in rhs() is elementwise, the chunked result must equal the whole-grid
     result bit for bit. KA5 checks this; if it is not exact, the run does not go ahead.
3. **An RSS guard.** Every 2000 steps the run reads its own peak RSS. If the peak exceeds 450 MB, the run
   checkpoints and exits with code 4, and that is reported.

Two ultra runs at once therefore stay under 0.9 GB together. If a run hits its guard, the two runs go one
at a time instead, with the guard at 900 MB. Grading runs only after both hydro runs end.

## C2. Ladders and convergence line (frozen)

- **M490 and M234 both:** (medium, fine, ultra).
  - The coarse rung is kept for KA1 and is reported beside the ladder, but it is not in the graded ladder.
- **The convergence line is MS2's R4, unchanged, applied to (medium, fine, ultra).**
  - R1 is the fixed-radius readout and R2 the five-snapshot time mean and spread.
  - The classes are TINY_ABS, TINY, NOISE, MONOTONE, PRE-ASYMPTOTIC, OSCILLATORY and DIVERGENT, with their
    MS2 brackets.
  - CONV passes when no series is DIVERGENT or PRE-ASYMPTOTIC.
- **R5 (brackets)** is MS2's, read with each M's ladder medium rung as X_med.

## C3. The k = 0.1 non-additivity fix (frozen; applies to both k)

MUTATE no longer re-classifies the planted series on its own. The plant is graded as a difference against
the unplanted run on the same grid.

1. On each rung r and each snapshot, take the gate value with the plant minus the gate value without it:
   same snapshot, same grid, same R1 readout. Its five-snapshot mean is d_r.
2. Let D_d = max_r d_r - min_r d_r over the three ladder rungs.
3. The planted bracket is [max(0, L_base + min_r d_r - D_d), U_base + max_r d_r + D_d], where
   [L_base, U_base] is the unplanted series' R4 bracket.

This is the bracket that holds if the base bracket holds and the plant's true effect lies within its own
rung envelope widened by its rung spread. It is a stated assumption, like TINY_ABS's widening.

Read under C3:

- **k = 2.** Reads FAIL: L > 1 in every cell, gate, M and reading.
- **k = 0.1.** Reads PASS: U < 1 wherever U_base + 0.1 < 1. Other cells are reported as near-failures and
  are not counted.

The MS2-style direct R4 classification of the planted series is computed and reported as information only.

If either k fails under C3, NO VERDICT.

## Known answers (each must pass)

- **KA1 (MS2 exactly).** Run with MS2's ladders (coarse / medium / fine at both M, i.e. MS2's interim
  ladder) and MS2's MUTATE rule. The script must reproduce, to 1e-12 relative (inf = inf, None = None),
  every value of MS2_interim.json in these places:
  - `ladder`: X, s, cls, p, U and Lmax of all 28 entries;
  - `bracket_per_gate`: Lmin and Umax;
  - `mutate`: minL_k2, maxU_k01 and the count of k01_failures;
  - `series_classes`.
- **KA2 (readout).** MS2's KA2, extended to the ultra rungs: under R1, the planted-only field recovers k to
  within 1 % on every rung, gate, cell and k.
- **KA3 (procedure).** MS2's KA3. In addition, C3 on a synthetic base series with an exactly additive plant
  must return [L_base + k, U_base + k].
- **KA4 (ultra runs).** Each ultra done.json shows t = 1000, and there is no NaN in q, u or v on any snapshot.
- **KA5 (chunked solver).** Two checks, both run before the ultra runs start:
  - **(a)** On the AC24 fine t = 1000 final snapshots at M234 and M490, and on those states injected onto the
    ultra grid (piecewise constant), chunked rhs() equals the whole-grid rhs() bit for bit: max abs difference
    exactly 0 in all three components. Chunk sizes tested: 64, 37 and 1000.
  - **(b)** A coarse M234 TRANSMIT UNIFORM t = 1000 rerun with hydro_ms3.py reproduces AC24's coarse snapshots
    bit for bit in q, u and v, on all five snapshots.

## Labels (as MS2)

- **PASS (moving Sun, scoped).** KA1-KA5, CONV and both MUTATEs under C3 pass, and every U < 1 in every
  cell, gate, bracket and reading.
- **FAIL.** The same checks pass, and some cell has L > 1 in every bracket for some gate (worse reading
  governs). The line is named: the G1/G2 planet bound (Earth 8.7e-15, Mars 1.4e-15, Saturn 7.0e-15 m/s^2)
  or Cassini Q_eff 5.2e-27 s^-2.
- **UNDECIDED.** The same checks pass, some U >= 1, and no FAIL. The splitting bracket is named.
- **NO VERDICT.** A KA, CONV or a MUTATE fails. The bracket [min L, max U] per gate is reported.

Reported, not the label:

- Diagnostic D (MS2's band sums) for fine -> ultra at both M.
- The four-rung sequences (coarse, medium, fine, ultra) of each worst-U series.

Scope as AC15, AC24, MS1 and MS2. No PPN alpha_1 or alpha_2 is claimed. AC2q differs by s^2/rho0 ~ 4e-6.

## Compute

- **Each hydro run.** One process, one thread (OMP_NUM_THREADS=1), nice 15, in the background.
  - It is checkpointed by the solver's SIGTERM handler, and a killed run resumes from state.npz.
  - The RSS guard is as in C1.
- **Expected wall time.** Fine took 11 199 s to t = 1000. Ultra has 4 times the cells and about 2 times the
  steps, so about 25 h per run, more under load.
- **Grading.** One process, nice 15, with a row cache for resume, after both runs end.
- **Not committed.** state.npz, snapshots and logs. MS2's stopped ultra checkpoint (t 1.6) is not reused.
