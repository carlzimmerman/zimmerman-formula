# AGB7R — blind re-grade of AGB7: result

2026-11-14. Second implementation of AGB7 (CFG684 and CFG689 re-read with the age slope left in the DES distances),
written from AGB7's `FROZEN_CRITERIA.md` and the inputs it names. No AGB7 file except the criteria, and no AGB README,
result or collector file, was opened. The reading of the rules (`READING.md`) was committed alone before any run
(local commit 38b3610272). This file, the harness, the collector and every output are committed together after it.

Files: `agb7r_harness.py` (generalised re-read harness), `run_agb7r.sh` (runner), `agb7r_collect.py` (checks and
labels; writes `agb7r_results.json`, printed as `agb7r_collect.out`); per run `agb7r_<target>_<sample>_<tpl>_A<amp>`
`.json` (the lane's own output), `.meta.json` (template, sample counts, shift range, hashes, threads, time),
`.stdout.txt` (filtered stdout); CFG689 runs also `.out` (the lane's own log); `runs_status.txt` (exit codes).

## Harness checks (judged before any label was read)
| check | what | tolerance | worst difference | result |
|---|---|---|---|---|
| H1 | `cfg684 full` A = 0 vs `cfg684_results.json`, both combinations (Δχ²_max, flat-a0 Ω_m mean and sd, tracking and rival bands at z* 1.0, 1.5, 2.33) | 1e-6 | 0 (bit-identical) | **PASS** |
| H2 | `cfg684 full` A = 1 T_S vs AGB1's `agb1_cfg684_full_A1.json`, same quantities | 1e-9 | 0 (bit-identical) | **PASS** |
| H3 | `cfg689 TD5F des_only` A = 1 T_S vs AGB1's `agb1_cfg689_TD5F_des_only_A1.json`, all five tracking √X quantiles at the four z* | 0.005 | 0 (bit-identical); K4 ok, 60,000 steps | **PASS** |

Both lanes' labels are therefore evaluable. Template side check (not a frozen check): AGB1's T_S agrees with my own
recomputation on much finer grids (quadrature for t(z), 200,001-point age integral) to ≤ 1.7e-6 mag at A = 1, z ≤ 1.

## Runs
21 runs, every one exit 0; **none NOT RUN** (no exit 75). 60,000 steps, the lanes' own seeds; `CFG689_PARALLEL=1`,
three CFG689 runs at once, CFG684 one after another, BLAS threads 2, on a machine other sessions held at load 17–27.
CFG684 runs took 63–78 s, CFG689 runs 212–297 s. Samples: `full` 1,820 supernovae (1,623 DES + 197 legacy),
`des_only` 1,623. Shift range over the supernovae: T_S at A = 0.23 0.0023–0.0388 mag, at A = 0.35 0.0035–0.0590 mag.
The lane folders CFG681, CFG684 and CFG689 are unchanged (no file newer than a marker set before the runs;
`git status` clean there).

## CFG684 labels (primary A = 0.23 T_S; second word from A = 0.35 T_S; against LGS1's A = 0 run of the same sample)
| sample, combination | A1 | A2 | A3 |
|---|---|---|---|
| full, BAO+DES5 | NOT BROKEN, ROBUST | ROBUST, FRAGILE | FLOOR HOLDS, ROBUST |
| full, BAO+DES5+CC | NOT BROKEN, ROBUST | ROBUST, FRAGILE | FLOOR HOLDS, ROBUST |
| des_only, BAO+DES5 | NOT BROKEN, ROBUST | ROBUST, FRAGILE | FLOOR LOST, ROBUST |
| des_only, BAO+DES5+CC | NOT BROKEN, ROBUST | ROBUST, FRAGILE | FLOOR LOST, ROBUST |

Numbers (flat-a0 Ω_m mean ± sd; shift from A = 0; combined error √(sd² + sd₀²); |shift| / combined error; tracking
band √X at z* 2.33):
| sample, combination | A | Δχ²_max | flat-a0 Ω_m | shift | comb. err | ratio | tracking(2.33) |
|---|---|---|---|---|---|---|---|
| full, BAO+DES5 | 0 (LGS1) | 1.668 | 0.30672 ± 0.00741 | | | | [0.6901, 2.1684] |
| | 0.23 | 1.605 | 0.31665 ± 0.00749 | +0.00993 | 0.01053 | 0.94 | [0.8713, 2.2776] |
| | 0.35 | 1.568 | 0.32203 ± 0.00749 | +0.01531 | 0.01054 | 1.45 | [1.1147, 2.3296] |
| full, BAO+DES5+CC | 0 (LGS1) | 1.716 | 0.30698 ± 0.00733 | | | | [0.6869, 2.1658] |
| | 0.23 | 1.671 | 0.31696 ± 0.00749 | +0.00998 | 0.01048 | 0.95 | [1.0005, 2.2793] |
| | 0.35 | 1.607 | 0.32184 ± 0.00764 | +0.01486 | 0.01058 | 1.40 | [1.0018, 2.3273] |
| des_only, BAO+DES5 | 0 (LGS1) | 0.112 | 0.29173 ± 0.00853 | | | | [0, 2.0187] |
| | 0.23 | 0.096 | 0.30041 ± 0.00843 | +0.00868 | 0.01199 | 0.72 | [0, 2.1357] |
| | 0.35 | 0.114 | 0.30504 ± 0.00834 | +0.01330 | 0.01193 | 1.11 | [0, 2.2004] |
| des_only, BAO+DES5+CC | 0 (LGS1) | 0.164 | 0.29199 ± 0.00800 | | | | [0, 2.0258] |
| | 0.23 | 0.182 | 0.30093 ± 0.00845 | +0.00894 | 0.01164 | 0.77 | [0, 2.1440] |
| | 0.35 | 0.084 | 0.30535 ± 0.00799 | +0.01337 | 0.01130 | 1.18 | [0, 2.2056] |

## CFG689 labels (primary A = 0.23 T_S; second word from A = 0.35 T_S; against LGS1's A = 0 run)
Gate: K4 ok and 60,000 steps in every run and in all four LGS1 references (largest R-hat in my runs 1.0012).
| mode, sample | B1 z* 1.0 | B1 z* 1.2 | B1 z* 1.5 | B1 z* 2.33 | B2 |
|---|---|---|---|---|---|
| D5, full | STABLE, ROBUST | STABLE, ROBUST | STABLE, ROBUST | STABLE, ROBUST | CLASS UNCHANGED, ROBUST |
| D5, des_only | STABLE, ROBUST | STABLE, ROBUST | STABLE, ROBUST | STABLE, ROBUST | CLASS UNCHANGED, ROBUST |
| TD5F, full | STABLE, ROBUST | STABLE, ROBUST | STABLE, ROBUST | STABLE, ROBUST | CLASS UNCHANGED, ROBUST |
| TD5F, des_only | STABLE, ROBUST | STABLE, ROBUST | STABLE, ROBUST | STABLE, ROBUST | CLASS UNCHANGED, ROBUST |

Tracking √X median [68 % band] at each z*, A = 0 (LGS1) → 0.23 → 0.35:
| mode, sample | z* 1.0 | z* 1.2 | z* 1.5 | z* 2.33 |
|---|---|---|---|---|
| D5 full | 0.9499 [0.8108, 1.0565] → 0.9790 [0.8451, 1.0851] → 0.9964 [0.8649, 1.1012] | 0.9412 [0.7801, 1.0592] → 0.9718 [0.8188, 1.0892] → 0.9901 [0.8390, 1.1059] | 0.9268 [0.6768, 1.0993] → 0.9611 [0.7189, 1.1339] → 0.9791 [0.7414, 1.1531] | 0.9076 [0.3383, 1.2068] → 0.9595 [0.4324, 1.2529] → 0.9919 [0.4873, 1.2773] |
| D5 des_only | 0.9338 [0.8051, 1.0365] → 0.9634 [0.8372, 1.0637] → 0.9783 [0.8539, 1.0784] | 0.9358 [0.7893, 1.0476] → 0.9653 [0.8267, 1.0757] → 0.9822 [0.8450, 1.0912] | 0.9372 [0.7156, 1.0991] → 0.9694 [0.7556, 1.1295] → 0.9885 [0.7794, 1.1454] | 0.9534 [0.5055, 1.2218] → 1.0009 [0.5829, 1.2655] → 1.0287 [0.6155, 1.2889] |
| TD5F full | 0.9728 [0.9123, 1.0310] → 0.9935 [0.9319, 1.0529] → 1.0051 [0.9428, 1.0648] | 0.9494 [0.8947, 1.0026] → 0.9702 [0.9144, 1.0248] → 0.9807 [0.9243, 1.0360] | 0.9124 [0.7807, 1.0320] → 0.9337 [0.7959, 1.0552] → 0.9423 [0.8033, 1.0648] | 0.8788 [0.6780, 1.0447] → 0.8974 [0.6933, 1.0663] → 0.9067 [0.7034, 1.0779] |
| TD5F des_only | 0.9315 [0.8701, 0.9913] → 0.9503 [0.8884, 1.0113] → 0.9603 [0.8972, 1.0233] | 0.9156 [0.8599, 0.9689] → 0.9333 [0.8774, 0.9880] → 0.9436 [0.8871, 1.0000] | 0.8893 [0.7620, 1.0041] → 0.9055 [0.7752, 1.0232] → 0.9161 [0.7830, 1.0372] | 0.8481 [0.6538, 1.0092] → 0.8664 [0.6687, 1.0301] → 0.8792 [0.6787, 1.0426] |

The largest move of a run's median toward the A = 0 band edge is 0.39 of the way at A = 0.23 (TD5F full, z* 1.2) and
0.59 at A = 0.35 (same cell); no B1 label is near its edge.

Classes (B2) and the reported-only numbers, A = 0 → 0.23 → 0.35:
| mode, sample | P1 | P0 | P2 (Δχ² / 5 dof, σ-equivalent, class) | native H0 median [68 %] | e_3σ at z* 1.0 / 1.2 / 1.5 / 2.33 (0.23; 0.35) |
|---|---|---|---|---|---|
| D5 full | DEGENERACY BROKEN throughout | FLAT CONSISTENT throughout | 7.78, 1.38σ CONSISTENT WITH CONSTANT → 17.35, 2.89σ HINT → 24.39, 3.74σ EVOLVING DE REQUIRED | 67.85 [67.28, 68.43] → 66.88 [66.32, 67.45] → 66.38 [65.82, 66.93] | 0.054 / 0.071 / 0.074 / 0.091; 0.054 / 0.070 / 0.073 / 0.096 |
| D5 des_only | DEGENERACY BROKEN throughout | FLAT CONSISTENT throughout | 6.96, 1.22σ → 8.46, 1.50σ → 10.14, 1.80σ, all CONSISTENT WITH CONSTANT | 69.40 [68.51, 70.26] → 68.45 [67.56, 69.33] → 67.94 [67.06, 68.81] | 0.054 / 0.069 / 0.075 / 0.099; 0.053 / 0.069 / 0.076 / 0.101 |
| TD5F full | DEGENERACY BROKEN throughout | none (flat mode) | 11.32, 2.00σ HINT → 25.34, 3.85σ EVOLVING DE REQUIRED → 35.88, 4.89σ EVOLVING DE REQUIRED | 67.73 [67.18, 68.28] → 66.75 [66.21, 67.30] → 66.24 [65.70, 66.79] | 0.069 / 0.092 / 0.100 / 0.153; 0.069 / 0.091 / 0.100 / 0.153 |
| TD5F des_only | DEGENERACY BROKEN throughout | none (flat mode) | 9.02, 1.61σ CONSISTENT WITH CONSTANT → 10.79, 1.91σ CONSISTENT → 12.82, 2.24σ HINT | 69.27 [68.42, 70.13] → 68.31 [67.45, 69.17] → 67.80 [66.93, 68.66] | 0.070 / 0.093 / 0.101 / 0.154; 0.070 / 0.092 / 0.100 / 0.154 |

## Reported only (no label)
**CFG684 at A = 0.35 with T_H** (the sample's own mean-host-age drift; linear between AGB3's bins, flat beyond):
| sample, combination | Δχ²_max | flat-a0 Ω_m | shift | comb. err | ratio | tracking(2.33) |
|---|---|---|---|---|---|---|
| full, BAO+DES5 | 2.322 | 0.31642 ± 0.00743 | +0.00971 | 0.01049 | 0.93 | [1.4090, 2.2589] |
| full, BAO+DES5+CC | 2.417 | 0.31600 ± 0.00735 | +0.00902 | 0.01038 | 0.87 | [1.4011, 2.2639] |
| des_only, BAO+DES5 | 0.128 | 0.29367 ± 0.00835 | +0.00193 | 0.01194 | 0.16 | [0, 2.0417] |
| des_only, BAO+DES5+CC | 0.086 | 0.29373 ± 0.00821 | +0.00174 | 0.01146 | 0.15 | [0, 2.0555] |

The rules, applied to these rows only for comparison, would read the same first words as the T_S primary.

**Shift in units of the A = 1 shift**, from my own A = 1 runs (for CFG684 `full` and CFG689 TD5F `des_only` these are
bit-identical to AGB1's, by H2 and H3; for the other four sample/mode pairs they are extra runs of the same code path,
since AGB1's other outputs are closed to me):
- CFG684 flat-a0 Ω_m (A = 1 shift +0.0436 / +0.0436 full, +0.0413 / +0.0411 des_only for BAO+DES5 / +CC):
  A = 0.23 T_S 0.228 / 0.229 (full), 0.210 / 0.218 (des_only); A = 0.35 T_S 0.351 / 0.341, 0.322 / 0.325;
  A = 0.35 T_H 0.223 / 0.207, 0.047 / 0.042. Tracking upper edge at 2.33: 0.24–0.25 at 0.23, 0.35–0.37 at 0.35.
  The lower edge at 2.33 moves non-linearly in `full` (0.29 / 0.43 at 0.23, 0.67 / 0.43 at 0.35, 1.14 / 0.98 with T_H)
  and is pinned at 0 in `des_only`.
- CFG689 tracking medians at z* 1.0 / 1.2 / 1.5 / 2.33: A = 0.23 0.19–0.24 everywhere; A = 0.35 0.31–0.40.
  (D5 full 0.196 / 0.198 / 0.205 / 0.212 and 0.314 / 0.316 / 0.312 / 0.345; D5 des_only 0.220 / 0.209 / 0.213 / 0.216
  and 0.330 / 0.329 / 0.340 / 0.343; TD5F full 0.213 / 0.220 / 0.240 / 0.205 and 0.332 / 0.331 / 0.337 / 0.307;
  TD5F des_only 0.210 / 0.203 / 0.189 / 0.232 and 0.321 / 0.321 / 0.312 / 0.395.)
- For the record, my A = 1 runs give AGE-DEPENDENT for A2 in all four CFG684 cells (3.3–4.6 combined sd), and
  SHIFTED at z* 1.0 and 1.2, STABLE at 1.5 and 2.33, in all four CFG689 cells, with P2 EVOLVING DE REQUIRED in all four
  (8.39σ D5 full, 4.32σ D5 des_only, 10.69σ TD5F full, 4.99σ TD5F des_only).

## Where I think the criteria are wrong or under-specified
1. **A2's threshold decides its second word.** "Within the two sd added in quadrature" I read as one combined sd
   (READING.md). On that reading the primary sits at 0.72–0.95 of it and the bracket at 1.11–1.45, hence
   ROBUST, FRAGILE in all four cells. Read as twice the combined sd, all four would be ROBUST, ROBUST. The `full`
   primary is at 0.94–0.95, close to the line. A comparison with AGB7 should check which reading it used first.
2. **A3 in `des_only` says nothing about age.** The floor is already lost at A = 0 in LGS1's own `des_only` runs, so
   FLOOR LOST, ROBUST there is inherited, not caused by the shift.
3. **A1 reads the run, not a change.** Δχ²_max is 0.08–2.4 in every run and at A = 0; the label could only move if the
   shift made Ω_m much better constrained, which it did not in any run here, up to A = 1 (0.08–2.4).
4. **B1 has little power at this amplitude.** A median has to leave a 68 % band; even at A = 1 only z* 1.0 and 1.2
   shift. The medians scale close to linearly in A (0.19–0.24 of the A = 1 shift at 0.23), so STABLE at 0.23 follows
   from the A = 1 result by scaling alone.
5. **P2 carries no label but is the number that moves.** In the `full` sample the P2 class changes at the leftover
   size: D5 from CONSISTENT WITH CONSTANT (1.38σ) to HINT (2.89σ) at 0.23 and EVOLVING DE REQUIRED (3.74σ) at 0.35;
   TD5F from HINT (2.00σ) to EVOLVING DE REQUIRED at both 0.23 (3.85σ) and 0.35 (4.89σ). `des_only` stays below 2σ
   at 0.23 (1.50σ, 1.91σ) and TD5F reaches HINT (2.24σ) at 0.35. Native H0 falls by 0.95–0.98 km/s/Mpc at 0.23 in
   every cell (1.7–1.8 of its 68 % half-width in `full`, 1.1 in `des_only`). The frozen rules call these lanes ROBUST / STABLE while their P2 class
   in the `full` sample does lean on the age question; any summary should say so.
6. **B2 in TD5F** compares P1 only: the flat mode writes no P0 (READING.md).
7. **T_H is under-specified** (interpolation, zero point). The zero point cannot matter (both lanes profile a constant
   offset); the interpolation is mine. In `full`, AGB3's curve is a step between the legacy low-z hosts (5.8 Gyr at
   z 0.03) and the DES hosts (2.3–3.7 Gyr), so at A = 0.35 T_H moves the lower tracking edge at 2.33 as much as the
   A = 1 T_S shift does (ratio 1.14 / 0.98) while moving Ω_m by only 0.21–0.22 of it.
8. **"The A = 1 shift AGB1 found"** cannot be read by a blind re-grader beyond the two check files; I used my own
   A = 1 runs. "Tracking medians" do not exist in CFG684; I report Ω_m and the 2.33 band edges there.
9. H1's tolerance (absolute or relative) is not stated; moot here, the reproduction is exact.

## What this may and may not say
As the criteria state: ROBUST / STABLE means the committed numbers do not lean on the age question at the leftover
size by these rules, not that 0.23 or 0.35 is the right amount; the template is a redshift drift, and nothing here
adopts either amplitude. Point 5 above is outside the frozen labels.

kappa = 1/2 FITTED; not theory closed.
