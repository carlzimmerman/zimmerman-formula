# NP2_admissible_rule: an admissible leaf rule holds gates 1-5 in L3 and RQ3 still rejects it. IC 1613 and the Υ rows A5-A7 fail in train's hull; profiling Υ doesn't rescue them. L5 can't be made admissible off the enforcement set

Criteria `FROZEN_CRITERIA.md` (920b03ef9d), committed alone. Amendments, each committed alone:
- `AMENDMENT_A1.md` (cbb520abc2), pre-result.
- `AMENDMENT_A2.md`, after an aborted controls run.
- `AMENDMENT_A3.md` (d49cd94fc6), after a second aborted controls run.
- `AMENDMENT_A4.md`, **post-control**, before any real fit.

Scripts:
- `np2_core.py`: the constrained Gaussian process, the Υ loader and profile, the checker, the hull.
- `np2.py`: modes `controls` and `real`, run as `--only L3` and `--only L5`.
- `np2_cand.py`, `np2_stage3.py`: RQ3 run unedited.

Outputs are `np2_<mode>_<arm>.{json,out}`, `rules/*.npz` and `results/np2_real_<arm>_<F|U>.{json,out}`. Run with `PYTHONHASHSEED=0 nice -n 10 python3 -I np2.py <mode> --only <arm>`, one thread. Physical footprint peak was 0.32-0.43 GB. Max RSS reads 1.3-3.6 GB because macOS counts freed pages (A3).

**Not blind.** κ = ½ FITTED. No cold component, no particle; the cold sector stays retired, and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. A pass is a description of data, not a theory.

## What was done
- **The rule:** NP1's Gaussian-process rule for log B on the leaves (same split, leaves, kernel, step-A ML), projected onto the admissible set. g must rise with g_b when stars alone are added and when gas alone is added (slope d log g / d log g_b ≥ 0.05). This is enforced by a non-negative QP on derivative functionals over a Sobol constraint box, train leaves and a wide refinement set.
- **Smoothness:** λ chosen by grouped train CV on {¼ … 32}. A λ is eligible only if every fold fit is admissible on its set.
- **Checking:** an independent checker tests strict monotonicity in three directions on its own wide Sobol set, train rows, every holdout and CX1 row, and end to end through the RQ3 candidate.
- **Mode U:** Υ_disc is profiled per train galaxy on CRG1 SPEC set E's grid (0.30-1.20, bulge 1.4 Υ; the record's FG1 range), in two fixed passes (law, then rule).

## Verdicts (per arm, mode, footing; never pooled)

| Cell | Label (A4 controls) | Label under frozen control 4 |
|---|---|---|
| L3 F canonical | **ADMISSIBLE RULE FAILS ON** A10, A5, A6, A7, A12, A13, A30, A23b, A26b, B2, B7, B17 | UNDETERMINED (controls) |
| L3 F alt | **ADMISSIBLE RULE FAILS ON** A10, A5, A6, A7, A12, A13, A30, A23b, B9, B10, B11, B14, B16 | same |
| L3 U canonical | **UNDETERMINED (UNDERFIT)**: train X-COP rms 0.119 > 0.10 | UNDETERMINED (controls) |
| L3 U alt | **ADMISSIBLE RULE FAILS ON** G4 (LT +0.205), G5 (tilt 0.16), A9, A10, A5, A6, A7, A12, A13, A24, A26a, A30, A23b, B9 | same |
| L5 F canonical, alt | **UNDETERMINED (INADMISSIBLE)**: 8 and 5 checker violations, min slope −0.045 | UNDETERMINED (controls) |
| L5 U canonical, alt | **UNDETERMINED (INADMISSIBLE)**: 92 and 203 violations, min −0.23 and −0.34, incl. SPARC even holdout points | UNDETERMINED (controls) |

Planted N0 failed its frozen control in L3 canonical and both L5 cells (A4). C1 (planets, Z +16492 / +19931) fails in every cell; it is decided by the prior, as frozen (C5).

## Train fit and gates 1-5

All gates are passes unless marked F.

| Cell | λ (CV, all interior) | G1 X-COP train | G2 SPARC train (line) | G3 SPARC even (line) | G3 X-COP unseen | G4 LT | G5 A1 / A2 / A3 |
|---|---|---|---|---|---|---|---|
| L3 F can | 2 | +0.007 / 0.052 | 0.129 (0.175) | 0.181 (0.195) | +0.010 / 0.038 | +0.074 | 0.053 / 0.50 / 0.03 |
| L3 F alt | 4 | +0.012 / 0.066 | 0.140 (0.177) | 0.178 (0.196) | +0.002 / 0.045 | +0.046 | 0.051 / 0.50 / 0.07 |
| L3 U can | 4 | +0.046 / **0.119 F** | 0.095 (0.142) | 0.139 (0.159) | +0.017 / **0.105 F** | **+0.193 F** | 0.050 / 0.56 / **0.18 F** |
| L3 U alt | 2 | +0.006 / 0.054 | 0.088 (0.145) | 0.143 (0.162) | +0.008 / 0.035 | **+0.205 F** | 0.047 / 0.52 / **0.16 F** |
| L5 F can | 4 | +0.009 / 0.058 | 0.130 (0.175) | 0.179 (0.195) | +0.007 / 0.035 | +0.077 | 0.055 / 0.51 / 0.06 |
| L5 F alt | 4 | +0.009 / 0.059 | 0.130 (0.177) | 0.179 (0.196) | +0.006 / 0.035 | +0.075 | 0.054 / 0.51 / 0.06 |
| L5 U can | 2 | +0.006 / 0.050 | 0.076 (0.142) | 0.142 (0.159) | +0.009 / 0.042 | **+0.119 F** | 0.046 / 0.55 / 0.12 |
| L5 U alt | 2 | +0.006 / 0.050 | 0.075 (0.145) | 0.143 (0.162) | +0.008 / 0.043 | **+0.100 F** (edge) | 0.045 / 0.50 / 0.10 |

- **Mode U, gates 2-3:** the law's own Υ profile sets the line. Medians of Υ:
  - train U0 (law): 0.51 canonical, 0.44 alt;
  - train U1 (rule): 0.49-0.53;
  - holdouts profiled under the rule: 0.53-0.59.
- **λ is now interior in every cell** (2 or 4). NP1 sat at its grid edge, 4. The small λ (¼-2) were ineligible in L3: the fold fits couldn't be made admissible.

## RQ3 rows, with hull status (NP1's method)

**Dwarfs (A11-A13).**
- **A11** stays NOT COMPUTABLE in every cell, by RQ3's construction: only the law has LW1's cached AQUAL solves.
- **A12 and A13 are now computable** in every admissible cell, and in L5 F and L5 U canonical. They fail, and are worse than the plain law (law A12 +4.9, A13 +7.8):

| Cell | A12 | A13 |
|---|---|---|
| L3 F canonical | +6.4 | +13.7 (UFD class) |
| L3 F alt | +8.3 | +8.5 |
| L3 U canonical | +6.9 | +14.9 |
| L3 U alt | +5.9 | +17.1 |
| L5 F canonical | +7.6 | +8.1 |
| L5 U canonical | +6.2 | +10.3 |

- The dwarf line is **OUT OF HULL**: Dw is 40 % in hull in L3 F, 74 % in L3 U, and 0 % in L5 (s = −2 stand-in).
- L5 U alt's dwarf block raises a domain error (3 non-monotone dwarf rows). A11-A13 read NOT COMPUTABLE there.

**Υ rows A5 / A6 / A7, Z, fixed (F) against profiled (U).** NP1: +4.1 / +6.0 / −2.3. Plain law: +5.6 / +7.6 / −3.0 (canonical).

| Arm, footing | F | U |
|---|---|---|
| L3 canonical | +3.6 / +5.2 / −2.1 | +5.1 / +7.0 / −2.8 |
| L3 alt | +3.8 / +5.4 / −2.0 | +4.5 / +6.3 / −2.8 |
| L5 canonical | +4.1 / +5.3 / A7 passes (−1.3) | +4.9 / +6.7 / −2.7 |
| L5 alt | +4.1 / +5.3 / A7 passes (−1.3) | +3.9 / +5.6 / −2.4 |

- **Profiling Υ doesn't move A5-A7 toward a pass.** It makes them worse, back toward the law's values.
- In L3, all three are **IN HULL** (SPARC 0.93 F, 0.91-0.92 U).
- In L5 they are out of hull (SPARC 0.87-0.90, below the 0.90 line, as in NP1).

**Other rows.**
- **A10 IC 1613:**
  - L3: −4.3 (F), −2.8 / −2.3 (U), **IN HULL** (1.00).
  - L5: −3.6 to −3.9, out of hull through the s = −2 stand-in.
  - U lifts IC 1613 by ~0.25 dex but doesn't pass it.
- **A30 lensing:** +9 to +14, **OUT OF HULL** (L 0.18) everywhere.
- **Keys:** they fail only on X-COP lines that are out of hull (X-COP holdouts 53-60 % in hull).
  - L3 F canonical: B7, B17. L3 F alt: B9-B11, B14, B16.
  - L3 U: B24 (rms 0.113), B7, B9.
  - L5: B9, B10, B11, B14, B16, B17, B19, B20.
  - B23 and B25 pass in every cell.
- **NOT LOCATED:** A23b (−3.0 to −3.7) in every cell; A24, A26a, A26b and B2 in some.
- **L5 point-rule passes not counted:** A9, A20, A23a, A25, A26b, B2.

## Controls (`np2_controls_L3.out`, `np2_controls_L5.out`)

| Control | Result |
|---|---|
| 1. Known answer | X-COP +0.4675 (35 rows), LT −0.0252, exact |
| 8. Υ loader at 0.5 | reproduces BF1's ST and SH bit for bit |
| 3. Checker | flags the planted bump (3287) and NP1's frozen rule (4247; end to end 30/50 dwarf rows, 2/2 IC 1613, 173 SPARC); passes the zero rule |
| 2. Zero-weight rule through RQ3 | reproduces RQ3's law card on 74 rows, 0 mismatches; 22 skipped by design (NaN inputs, `--no-keys`, `--no-bullet`) |
| 4. Planted (1 + f) log1p(1/y), N1 | recovered in all 4 cells (G3 SPARC 0.140-0.144, X-COP ≤ +0.001, LT +0.07-0.09) |
| 4. Same form, N0 (frozen) | **fails** at L3 canonical (G3 X-COP +0.095) and both L5 cells (LT +0.12, +0.13); passes at L3 alt. The form is inadmissible on 80 % of train rows; no λ eligible, the fit doesn't converge (A4) |
| 5. Class boost ±0.25 | G3 SPARC 0.290-0.291, fails as it must |
| 7. Admissible plant law(g_b, a0(1 + 0.5 f)), N0 and N1 | recovered, 0 checker violations, every cell |
| 6. MUTATE | bites in every cell, F and U, through X-COP (+0.45 to +0.50) |

## Reading
- **Admissibility costs nothing on the gates in L3.** The admissible L3 rule passes gates 1-5 like NP1's did (X-COP unseen +0.002 to +0.010, SPARC even 0.178-0.181), with zero checker violations and an interior λ. So NP1's non-monotone dwarf corner wasn't what carried its pass.
- **It doesn't rescue RQ3. In L3 the failures that sit in train's hull are IC 1613 (A10) and the Υ rows A5-A7.** That is the same in-hull list as NP1's L3 no-go.
  - The dwarf rows the admissible rule now makes computable fail outright, out of hull, and worse than the law.
  - Profiling Υ makes A5-A7 worse and breaks LITTLE THINGS and the tilt (G4 +0.19 to +0.21, G5 tilt 0.16-0.18).
- **L5 can't be held admissible** off its enforcement set at the CV-chosen smoothness:
  - mode F: 5-8 violations, small (min slope −0.045);
  - mode U: up to 203, including SPARC holdout points.
  - So no L5 statement is made.
- **Not closure for the class.** This is a statement about this GP class, these leaves and this smoothness. In-hull failures carry the L3 cells. No oracle was run, so it isn't shown that no admissible rule at any smoothness fits train and IC 1613 / A5-A7 together.

## Departures, all disclosed
1. **Four amendments.**
   - A1, pre-result: solver tolerance, working-set shrink, overflow safety, two processes.
   - A2, after an aborted run: zero-card comparison, enforcement pool, working-set cap, control 7 moved to an admissible plant.
   - A3, after a second aborted run: footprint metering, grow-only working set, CV eligibility.
   - A4, post-control: planted N0 dropped from the label's control 4, with both labels printed.

   A2-A4 were written after control numbers had been read; no real number had been.
2. **Under the frozen criteria,** L3 canonical and every L5 cell read UNDETERMINED (controls).
3. **No oracle** (declared in the criteria).
4. **Memory.** Two processes ran at once for part of the run. Each process's physical footprint peaked at 0.32-0.43 GB, so the two together may briefly have exceeded 0.8 GB. Max RSS figures are inflated by macOS's freed-page accounting.
5. **Ignored files.** RQ3 stage-3 logs, caches and smoke files are gitignored.

κ = ½ FITTED. Not theory closed.
