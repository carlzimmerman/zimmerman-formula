# FINAL-7F (FORMATION READING) — integral of a history, or function of a present state? (2026-11-12)

FINAL MILE, lane **FINAL-7F (FORMATION READING)**. TEST lane, quarantined. Adopts nothing, relabels
nothing, registers nothing. Footings never pooled (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10
m/s^2). Cold dark energy is a gravitating field component; no particle is added anywhere.
**kappa = 1/2 FITTED; not theory closed.** This lane edits nothing outside its own folder.

**Lane id.** The brief names this lane FINAL-7 (formation reading). The id **FINAL-7 is already taken**
in the record by `hy4_preview_push/FINAL-7_what_it_is` (the M5 medium triage, label NO MEDIUM). To keep
the two lanes separable I take the short id **FINAL7F** and the folder
`closure_2026_11_12/FINAL7F_formation_reading/`. Checked free: no `*/FINAL7F*` exists and no commit
subject names FINAL-7F or FINAL7F. The existing FINAL-7 is not touched, regraded or quoted as an
authority; it is a different question.

**Committed alone, before any FINAL7F script exists and before any FINAL7F number is computed.**

---

## 0. Honesty flag on the pre-registration

I write this file **after** reading DD1's `RESULT.md`, FINAL-2's `RESULT.md`, HIS1's and HIS1R's
`RESULT.md`, and FINAL-15's `PREREGISTER.md`, every one of which prints the measured per-class
residuals (SPARC ~0.00; KiDS +0.13; X-COP +0.50; CLASH +0.55; MW ultra-faints +0.59; tidal dwarfs
−0.69; DF2/DF4 −0.84; faint rotators −0.24; groups +0.16; the bipolar spread 1.435 dex).
**This is therefore not a blind pre-registration of the residual pattern.** What is fixed here before
any number is computed, and what the arithmetic will not be allowed to revise: the variable list and
its definitions (§3), the estimator and the permutation scheme (§4), the multiplicity family (§5), the
label vocabulary and the thresholds (§6), the known answers (§7) and the mutation arms (§8). The
*expectation* I record in §9 is derived from the printed pattern and is a hypothesis, not a result.

---

## 1. Question

Across DD1's 16 classes, the measured class median residual against the law spans about 1.4 dex and is
bipolar. Two readings of that spread:

- **Force reading (present-state).** The law acts now. Whatever departs from it does so because of a
  *present* property of the system — the field it sits in, its surface density, its depth. The residual
  is then a function of a variable measured today, and a monotone rank correlation with that variable
  must show up. (The plainest form of the reading, d = 0 for every class, is already excluded by the
  spread; see P0 in §6.)
- **Formation reading (integral of a history).** The amount was written on the assembly surface and
  since then only transport moves it: `X = X_L(g_bar/F_b) · F_C/F_b` (FINAL-15 §3). `F_C` and `F_b` are
  **integrals over each system's history**, not present-state variables. The reading therefore predicts
  that the class residual is **not** a function of any present-day variable — including the surface
  densities — and, because a0 does not evolve (FRZ2), not of the event's date either (FINAL-15 T-epoch).

**The question, made testable: is the class-median residual a monotone function of any measured
present-day variable, or of the epoch? If it is a function of the present state, the formation reading
loses its distinguishing feature. If it is a function of neither, that is the formation reading's
signature (and equally the signature of "the spread is organised by something not in the table").**

This lane computes only correlations. It does not fit a rule, does not propose a variable, and does not
re-grade DD1, HIS1, HIS1R, FINAL-2 or FINAL-15.

---

## 2. Data and the residual (frozen)

DD1's frozen table `fable52_push/DD1_deduce_from_data/dd1_table.csv`, **main bracket only**
(`bracket == ''`), 3419 points, **626 systems, 16 classes**. Columns used: `cls, sys, r_kpc, lgb, lgo,
eY, z, lSig, last`. No new data. Nothing outside the table.

Per footing, **never pooled** (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2):

    X_L(g_bar; a0)  = (sqrt(1 + 4 a0/g_bar) - 1)/2                  [DD1 L0 / SHP1]
    Y_L(g_bar; a0)  = log10(1 + X_L) = log10( g_law / g_bar ),
                      g_law = ½( g_bar + sqrt(g_bar^2 + 4 a0 g_bar) )  [DD1 KA4 identity]
    Y               = lgo - lgb = log10(g_obs/g_bar)
    d_point         = Y - Y_L(g_bar; a0)                             (dex in g_obs at fixed g_bar)
    d_sys           = median of d_point over the system's main-table points
    d_cls           = median of d_sys over the systems of the class   <- THE CLASS MEDIAN RESIDUAL
    e_sys           = median of the system's finite eY
    se_cls          = max( 1.2533 · 1.4826 · MAD(d_sys) / sqrt(n_sys),  sqrt(sum e_sys^2)/n_sys ),
                      and = e_sys when n_sys = 1

This is DD1's own statistic and FINAL-15 §7's, exactly. `d_cls` is the 16-number vector the whole lane
correlates. Both footings are carried through every step and reported side by side; no footing is ever
formed by combining the two.

---

## 3. The variables (frozen, definitions and coverage)

Each variable is built the same way: value per point → **median over the system's points** → **median
over the class's systems** (the system-median of a system-median, so a 2700-point class and a 6-point
class enter as one number each). Log10 throughout. Constants are dropped where a correlation is
invariant to them.

### 3.1 Epoch

| id | variable | definition | note |
|---|---|---|---|
| **E1** | `zz` | log10(z + 0.001) | DD1's variable (g) |

**E1 is the only measured epoch-like column in the frozen table.** Disclosed now, and not repaired
later: `z` is the system's **observed** redshift, not an independently measured assembly redshift
`z_f`. The record has **no measured z_f per system** (the LVD age column is empty on disk — HIS1;
VSH1's settling redshifts are computed, exist only for log M_b = 9 / 10.5 / 11.5, and are theory
numbers, not measurements; FINAL-2's epoch assignments are order-of-magnitude literature values). So
the lane tests the epoch through `z` and says so: for 13 of the 16 classes z < 0.05 (they are observed
today), for RC100 z = 0.61–2.52, KiDS z ≈ 0.31, CLASH z ≈ 0.36. **What E1 can test is therefore narrow:
it asks whether the classes observed at high z sit systematically elsewhere than the classes observed
at z ≈ 0.** It cannot test an assembly epoch that the table does not carry. That limit is a property of
the record, not of the statistic.

### 3.2 Present-day baryonic surface density

| id | variable | definition | coverage |
|---|---|---|---|
| **B1** | `lgb` | log10 g_bar at the point. Since M_b(<r)/(π r²) = g_bar/(πG), `lgb` **is** log10 of the enclosed baryonic surface density at the measurement radius, up to the constant −log10(πG) | 16 classes |
| **B2** | `lgb_last` | the same at each system's **outermost** tabulated point (`last == 1`): an aperture-matched surface density, free of the within-class radius mixing that FINAL-2 flagged for X-COP (0.35 dex between all-point and last-point medians) | 16 classes |
| **B3** | `lSig` | log10 [M_b(<R_h)/(π R_h²)] in Msun/pc², DD1's variable (d) | **9 classes only** (SPARC, RC100, ATLAS3D, the five dwarf/UDG classes with a measured half-light radius). Reported, not in the Holm family |

### 3.3 Present-day dynamical surface density

| id | variable | definition | coverage |
|---|---|---|---|
| **D1** | `lgo` | log10 g_obs at the point = log10 of the enclosed **dynamical** surface density M_dyn(<r)/(π r²) = g_obs/(πG), up to the same constant | 16 classes |
| **D2** | `lgo_last` | the same at the outermost tabulated point | 16 classes |

**Degeneracy, frozen and disclosed.** `d = (lgo − lgb) − Y_L(lgb)`, so at fixed `lgb` the residual and
`lgo` are the *same* number up to a constant. A correlation of `d` with **D1/D2 is therefore partly
mechanical** and cannot on its own carry a label. Two guards, both pre-registered:
(a) every D result is reported **next to** the B result on the same aperture, and a D correlation is
called informative only if it is **not** reproduced by B at the same aperture;
(b) a **partial Kendall correlation of d with D1 controlling for B1** (and of d with B1 controlling for
D1) is computed by rank-residualisation (linear detrending of the ranks on the control's ranks, then
tau on the rank residuals). With n = 16 this has little power; it is reported as a guard, not a test.

### 3.4 The other measured present-time proxies the table carries

| id | variable | definition |
|---|---|---|
| **P1** | `lr` | log10(r_kpc), DD1's variable (f) |
| **P2** | `lMb` | log10(g_bar r²/G), the enclosed baryon mass at the point, DD1's variable (e) |
| **P3** | `dep` | log10(g_obs r / c²), the local gravitational depth, DD1's variable (c) |
| **P4** | `dsys` | the system's largest `dep`: the system depth, DD1's variable (c') |

### 3.5 Confound check (in the Holm family)

| id | variable | definition |
|---|---|---|
| **C1** | `YL` | log10(1 + X_L(g_bar; a0)) at the class's `lgb`. If `d` correlates with `YL`, part of the class spread is a **shape** mismatch of the law (a0-dependent), not a class property. Footing-dependent by construction |

**Not in the table, therefore not tested:** host distance, tidal index, gas fraction, star-formation
histories, assembly redshifts, morphological type, environment. HIS1 H5 and FINAL-15 P-3 already tested
six within-class proxies of that kind (NO POWER); this lane is the class-level counterpart and uses
only what the frozen table carries.

---

## 4. Estimator (frozen)

For each of the 10 full-coverage variables v and each footing:

- **Kendall tau-b** with tie correction, **primary statistic**. Two-sided **permutation p**:
  100 000 random permutations of the 16 `d_cls` against the fixed v, `default_rng(20261112)`.
  The normal-approximation p with the tie-corrected variance is reported alongside as a cross-check.
- **Spearman rho** on ranks, same permutation scheme, same seed. Reported with its own p.
- **Slope** `b` in dex per dex from a **least-absolute-deviation** line `d = a + b (v − median v)`;
  95 % interval from 10 000 seeded bootstrap resamples **of classes** (not of points).
- **Implied scatter.** `sigma_imp = 1.4826 · MAD( d − a − b v )` over the 16 classes, and `rms_imp`.
  Raw: `sigma_raw = 1.4826 · MAD(d_cls)`, `rms_raw`. Reported per variable:
  `f = 1 − sigma_imp/sigma_raw` (robust scatter reduction) and `R2 = 1 − var_imp/var_raw`.
- Sensitivity (reported, not graded): the same correlations with classes weighted by `n_sys`, and with
  the two extreme classes (tidal dwarfs, NGC 1052 UDGs) removed — M4 in §8 carries the graded version.

**The 16 classes are a census, not a random sample.** The permutation p is a statement about
exchangeability of the class labels, which is how DD1 and HIS1 use the same device. It is reported as
such and is not dressed up as a population p-value.

**Power, stated now.** With n = 16 the exact two-sided 0.05 critical values are about
|rho| ≥ 0.50 and |tau| ≥ 0.35. Anything weaker is invisible here and must be reported as
"not detected", never as "absent". The mutation arms M2/M3 (§8) are the power checks: they plant a
signal of known size and must be seen.

---

## 5. Multiplicity

One family, **10 tests** (E1, B1, B2, D1, D2, P1, P2, P3, P4, C1), **Holm** at 0.05 on the Kendall
permutation p, **per footing** (a footing is not a test). B3 (`lSig`, 9 classes) is reported with its
own uncorrected p and excluded from the family, with the exclusion stated.

A variable is **DETECTED** when its Holm-adjusted Kendall p ≤ 0.05 **and** sign(tau) = sign(rho).
Sign disagreement is reported as MIXED and does not count as a detection.

---

## 6. Decision rule (frozen)

**P0 (pre-check, reported before any correlation).** The plain force reading predicts `d_cls = 0` for
all 16 classes, hence `sigma_raw = 0`. If `sigma_raw ≤ 0.10 dex` **and** no class is off by more than
3 se, the label is **NO CLASS SPREAD — FORCE READING NOT EXCLUDED** and the lane stops. Otherwise the
spread is real and the correlations are graded. Also reported here: the bipolar range
`max(d_cls) − min(d_cls)`, the count of classes off by more than 3 se, and `sigma_raw` against the
median `se_cls` (is the spread larger than the errors?).

**Labels** (the graded family is the 9 present/epoch variables; C1 is a confound, and if C1 alone is
detected the label carries the suffix ", confounded by the law's shape"):

| # | condition | label |
|---|---|---|
| L1 | P0 stops the lane | **NO CLASS SPREAD — FORCE READING NOT EXCLUDED** |
| L2 | ≥ 1 of B1, B2, D1, D2, P1–P4 DETECTED **with f ≥ 0.30**, and E1 not DETECTED | **PRESENT-STATE ORGANIZED (force-like)** |
| L3 | ≥ 1 of B1, B2, D1, D2, P1–P4 DETECTED with f ≥ 0.30, **and** E1 DETECTED | **PRESENT-STATE ORGANIZED, EPOCH ALSO** |
| L4 | E1 DETECTED and no present-state variable DETECTED | **EPOCH ORGANIZED** |
| L5 | nothing DETECTED and `sigma_raw ≥ 0.25 dex` | **NOT A FUNCTION OF ANY TESTED VARIABLE (history-like)** |
| L6 | nothing DETECTED and `sigma_raw < 0.25 dex` | **NO STRUCTURE** |
| L7 | otherwise | **MIXED** |
| — | a known answer fails | **NO VERDICT** |

A detection with `f < 0.30` is reported but cannot carry L2 or L3: a correlation that leaves most of
the spread unexplained does not make the spread a function of that variable.

Each label is stated per footing. If the two footings differ, both are printed and the difference is
described; the footings are never merged.

---

## 7. Known answers (must pass, else NO VERDICT)

- **KA1 — DD1 / FINAL-2 reproduction.** This lane's `d_cls` must equal FINAL-2's measured residuals for
  the six classes it prints, within 0.02 dex: tidal dwarfs −0.687, NGC 1052 UDGs −0.843, MW
  ultra-faints +0.592, M31 dwarfs +0.090, faint rotators −0.239, X-COP +0.504 (canonical); and the
  bipolar range must be 1.435 ± 0.02 dex. The remaining ten classes are checked against DD1's published
  L0 ranges (A→B / B→A / LOCO) — inside that range, or the deviation is reported.
- **KA2 — footing offset.** median over classes of `d_cls(alt) − d_cls(can)` must lie within 0.01 dex of
  `−0.5 log10(1.1312/0.93603) = −0.0411` when restricted to the deep classes (those with
  `lgb < log10 a0`); the full 16-class median is reported.
- **KA3 — synthetic truths (power and null).** With `d_cls` replaced by a planted signal and the real
  variables untouched:
  - (i) `d = 0.30 (zz − med zz)` → E1 must be DETECTED.
  - (ii) `d = 0.30 (lgb − med lgb)` → B1 must be DETECTED.
  - (iii) `d = 0.30 (lgo − med lgo)` → D1 must be DETECTED.
  - (iv) `d = 0` for all 16 (the force reading's own truth) → P0 must stop the lane at L1.
  - (v) `d` = the 16 values shuffled (seeded) → nothing DETECTED.
  If (i)–(iii) do not fire, the lane has no power at 0.30 dex/dex and every non-detection is reported
  as NO POWER rather than as a null result.
- **KA4 — DD1's identities, numerically.** `g_bar(g + a0) = g²` and `1 + X_L = g_law/g_bar` to 1e-12 on
  a grid of `g_bar/a0` in [1e-3, 1e3], both footings.
- **KA5 — tie structure.** The number of tied pairs in each variable's Kendall computation is printed; a
  variable with more than 90 % of pairs tied (E1 is the candidate: 13 classes share z < 0.05) is
  reported as DEGENERATE and excluded from the Holm family, with the exclusion stated.

---

## 8. Mutation arms (each must change its stated outcome, else disclosed)

- **M1 — labels shuffled.** Permute the 16 `d_cls` across classes (seed 20261112). The number of
  DETECTED variables must fall to 0 and the largest |tau| must drop by ≥ 0.20.
- **M2 — plant an epoch signal.** `d += 0.5 (zz − med zz)`. E1 must become DETECTED and the label must
  move off L5.
- **M3 — plant a present-state signal.** `d += 0.5 (lgo − med lgo)`. D1 must become DETECTED with
  f ≥ 0.30 and the label must become L2 or L3.
- **M4 — drop the two R-channel classes.** Remove tidal dwarfs and NGC 1052 UDGs (n = 14 classes). The
  pre-registered expectation is that no variable becomes DETECTED that was not already; if one does,
  the result is reported as resting on two classes.
- **M5 — a0 × 2.** SPARC's `d_cls` must move off the law by > 0.05 dex (DD1's M4 analogue).
- **Lean.** `FINAL7F.lean` must compile (standard axioms only); `FINAL7F_MUTATE.lean`, with each
  structural statement negated, must fail with at least one error per false statement.

---

## 9. What I expect, and why it is a hypothesis

From the printed numbers of DD1, FINAL-2, HIS1 and FINAL-15, which this lane may not re-derive before
the run:

- P0 will not stop the lane: `sigma_raw` should land near 0.3–0.4 dex, with several classes beyond 3 se.
- **E1: not detected, and if detected, then with the wrong structure.** FINAL-2 §3 showed the pattern
  is bipolar at matched epoch ordering — the ultra-faints (assembled earliest) and X-COP/CLASH
  (assembled latest) both sit at ≈ +0.5 dex — so **a single monotone function of the epoch is already
  falsified by that pair**. And 13 of 16 classes share z < 0.05, so E1 may be near-degenerate (KA5).
- **B1/D1: not detected in the sense that matters.** DD1's *free* function of `lgb` (candidate (a))
  failed 13 of 16 classes, and of `lgo` (candidate (b)) failed 15. A monotone *linear* trend can still
  survive where a free function fails, but with f well under 0.30.
- **Predicted label: L5, NOT A FUNCTION OF ANY TESTED VARIABLE (history-like)**, on both footings, with
  the caveat that L5 is the formation reading's *signature* and is equally consistent with the spread
  being organised by something the table does not carry. It is not a demonstration of the formation
  reading.

---

## 10. Siblings consulted, not redone

DD1 (the frozen 626-system / 16-class table; NO RULE AMONG THE CANDIDATES), SHP1 (the shape on
rotation curves), HIS1 and HIS1R (the history reading; HOLDS EXCEPT H3 FAILS / H5 NO POWER; the force
reading 1 of 5), FINAL-2 (EPOCH: no candidate reproduces the spread; the a0-channel capped at
+0.25 dex; bipolarity kills any monotone epoch map), FINAL-15 (the formation ledger; P-3 no
within-class tracking), FRZ2 (a0(z) closed), RB1 / RB2 / CFG936 / G2 (per-class astrophysics),
COL1 / FLD1 / LFS1 / R541 (the closures behind the formation reading). Nothing here re-grades them.

## 11. Files

- `PREREGISTER.md` (this file, committed alone, first)
- `final7f.py` → `final7f.json` / `final7f.out`, `final7f_MUTATE.json` / `final7f_MUTATE.out`
- `FINAL7F.lean`, `FINAL7F_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`
- `RESULT.md`

Operational: stdlib only (plus `numpy` if present; the lane does not require it), one thread, seconds.
Re-run: `python3 final7f.py` from this folder.

---

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
