# HIS1R COMPARISON: the blind regrade against HIS1's RESULT.md (2026-11-10)

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Written after HIS1R's label was committed
and pushed alone (READING origin fefd1d3437, RESULT_BLIND origin 882d9fa389). Only then were HIS1's RESULT.md,
`his1.json`, `his1.out` and `his1.py` opened. `his1r_compare.py` -> `his1r_compare.out` sets the two JSON files side
by side, number by number. It also runs the two checks that explain the differences.

Reminder: HIS1R is not clean-blind. HIS1's commit subjects were in the session context from the start (READING.md,
exposure 1). The agreement below is an agreement of arithmetic, from separate code. It is not an independent judgement
on the points those subjects named.

## Verdict

| footing | HIS1 | HIS1R (blind) | verdict |
|---|---|---|---|
| canonical | HOLDS EXCEPT H3 (fails), H5 (no power); force 1 / 5; no rule 1 / 4 | HOLDS EXCEPT H3 (FAILS), H5 (NO POWER); force 1 / 5; no rule 1 / 4 | **AGREES WITH DIFFERENCES THAT DO NOT MOVE A LABEL** |
| alt | HOLDS EXCEPT H3 (fails), H5 (no power); force 1 / 5; no rule 1 / 4 | HOLDS EXCEPT H3 (FAILS), H5 (NO POWER); force 1 / 5; **no rule 2 / 4** | **AGREES WITH DIFFERENCES THAT DO NOT MOVE A LABEL** |

All five test outcomes agree on both footings. The force score agrees. 145 of 148 compared numbers agree to 5e-12.
The three that differ are the F4 standard error (both footings) and the no-rule count on the alt footing. Neither
touches a label.

## Number by number (canonical / alt; equal to 5e-12 unless marked)

| quantity | HIS1 | HIS1R | same? |
|---|---|---|---|
| H1 tidal dwarfs median Y, se | +0.067, 0.115 | +0.067, 0.115 | yes |
| H1 median d_L, se | -0.687 / -0.725, 0.115 | -0.687 / -0.725, 0.115 | yes |
| H2 (a) systems below -3 e | 0 of 626 | 0 of 626 | yes |
| H2 (b) classes below -3 se | none | none | yes |
| H2 (c) DF2 Y, d_L, e | +0.128, -0.743 / -0.781, 0.344 | the same | yes |
| H2 (c) DF4 Y, d_L, e | -0.104, -0.943 / -0.981, 0.349 | the same | yes |
| H3 SPARC (n 149) | +0.004 / -0.023 +- 0.012 | the same | yes |
| H3 SPARC f_g >= 0.5 (n 62) | +0.026 / -0.010 +- 0.021 | the same | yes |
| H3 faint rotators Ti1 < 0 (n 9) | -0.278 / -0.315 +- 0.080 / 0.081 | the same | yes |
| H3 KiDS, LG field, ATLAS3D outside Virgo | +0.137 / +0.097; -0.090 / -0.130; +0.081 / +0.069 | the same | yes |
| H3 MW bright, ultra-faints, M31, Coma, groups | +0.065, +0.592, +0.090, +0.319, +0.161 (canonical) | the same | yes |
| H3 faint-rotator brackets (M_* x 2, x 0.5; D x 0.8, x 1.2) | isolated -3.5 -> -4.2, -3.0, -2.3, -4.5 se (canonical) | the same | yes |
| H4 | HOLDS (RB1's rb1.json) | HOLDS (RB1's RESULT.md) | yes |
| H4 X at last point, X-COP | 4.94 [4.30, 6.11] | 4.940 [4.643, 5.479] | median yes; interval differs (see below) |
| H4 X at last point, groups | 9.07 [8.49, 9.73] | 9.066 [8.499, 9.730] | median yes; interval method differs |
| H5 rho, p, n for G1-G6 | G1 +0.011 / -0.034, G2 +0.109 / +0.113, G3 -0.545, G4 -0.215, G5 -0.007, G6 -0.391 | the same | yes |
| F1 | fails | fails | yes |
| F2 count below the law | 12 / 15 | 12 / 15 | yes |
| F3 sets off the law | FR Ti1 < 0, ATLAS3D outside Virgo, MW ultra-faints, groups, NGC 1052 UDGs | the same without NGC 1052 UDGs (it is in under ALT-HOST) | outcome yes, list differs |
| F4 X-COP last points median d_L | +0.154 / +0.119 | +0.154 / +0.119 | yes |
| **F4 se** | **0.0124** | **0.0154** | **no** |
| F5 | passes | passes | yes |
| force score | 1 / 5 | 1 / 5 | yes |
| **no rule (seed 7)** | 1 / 4: H1 F, H2 H, H3 F, H5 NO POWER, both footings | canonical 1 / 4 (H5 FAILS); **alt 2 / 4** (H3 HOLDS) | **count differs on alt** |
| KA1 | max dev 0 | 2.2e-16 | yes |
| KA2 IVW | +0.0831 +- 0.0958 | +0.0831 +- 0.0958 | yes |
| KA2 table-Y check | max 0.044 dex | max 0.0135 dex | both pass; basis differs |
| KA3, KA4 | PASS | PASS | yes |
| M1, M3, M4 | bite | bite | yes |
| M2 | does not bite (one of the four has e 0.20) | does not bite (D512-2, e_sys 0.203) | yes |
| ATLAS3D at Salpeter (reported) | median Y -0.047 +- 0.011, 4.3 se below; 1 below 3 e | -0.047 +- 0.011, -4.27 se; 1 | yes |
| SPARC Ti1 (reported) | rho -0.37, p 0.04 | -0.374, p 0.038 | yes |
| ATLAS3D Virgo / outside (reported) | +0.031 / +0.081 | +0.031 / +0.081 | yes |

## The differences and their causes

1. **F4 standard error, 0.0124 against 0.0154.** HIS1 forms the se of the last-point d_L with each system's e_sys (the
   median of eY over all its points). HIS1R uses the eY of the last point itself. The check reproduces both (0.0124
   with e_sys, 0.0154 with the last point's e). F4 fails either way: +0.154 / +0.119 is 10 / 8 se from the law.
2. **No-rule count on the alt footing, 1 / 4 against 2 / 4.** Two causes.
   - The permutation. HIS1 permutes the systems in sorted key order; HIS1R in table order. Both use
     `default_rng(7)`, so the shuffled tables differ.
   - The empty-set rule. With HIS1's permutation, no system that carries a UNGC Ti1 < 0 lands in the "faint
     rotators" label, so the isolated set is empty. HIS1 counts an empty set as failing H3 (`n > 0` is required).
     HIS1R's reading counts an empty set as not failing (READING.md, H3). HIS1's own permutation graded by HIS1R's rules
     gives H3 HOLDS on the alt footing (2 / 4) and H3 FAILS on the canonical one (another set fails there).
   - On HIS1R's own permutation the canonical H5 FAILS: a shuffled "MW ultra-faints" label carries 8 systems with a
     host distance and rho -0.905 (p 0.002). On HIS1's permutation H5 has no power. The count stays 1 / 4 either way.
   - The no-rule count sits beside the label. It does not move it. Both counts are far from 4 / 4. Over seeds 1-200,
     HIS1R never reaches 3 / 4 on the canonical footing and 2 seeds of 200 reach 3 / 4 on the alt one.
3. **F3 list.** HIS1 adds LG field dwarfs (already an H3 set) and NGC 1052 UDGs to F3. That is HIS1R's ALT-HOST
   reading. NGC 1052 UDGs are -3.44 / -3.60 se from the law, so the list grows by one. F3 fails either way.
4. **H4 intervals.** HIS1's X intervals are RB1's f_ret intervals turned into X (5.41 / f_ret). HIS1R's are a bootstrap
   of the table's last-point medians. The medians agree (4.94, 9.07). H4 is graded on RB1's f_ret numbers in both, and
   they are the same numbers. HIS1 also gives X 5.12 at R500 (5.41 / 1.057); HIS1R did not compute it (the table has
   no R500 point for X-COP).
5. **KA2 table check.** HIS1 compares the table's Y with the log of Lelli+15's rounded ratio column (max 0.044 dex).
   HIS1R compares with log10(M_dyn / M_bar) from the mass columns (max 0.0135 dex). Both pass the 0.05 line.
6. **H5 pair rule.** HIS1 needs n >= 4 for a pair and drops pairs with no p from the Holm family. HIS1R needs n >= 3 and
   keeps all six with p = 1. On the real table every pair has n >= 11, so nothing changes.
7. Present in HIS1, absent in HIS1R: the Lean file and its false twin; the post hoc M2b; a Spearman p for Virgo
   (0.006). Present in HIS1R only: the alternative-reading grid and the planted-signal and shuffle checks.

## Readings that could move a label

None found. Every alternative reading in READING.md leaves both labels unchanged (RESULT_BLIND.md, table). The one
reading where the two lanes differ in fact (empty subset under shuffled labels) moves the no-rule control on the alt
footing (1 / 4 or 2 / 4), not a label. The permutation order moves the shuffled H5 between FAILS and NO POWER, not
the count.

Two things are not readings of the criteria but would move a clause, and both lanes report them. A coherent 20 %
distance cut takes the isolated faint rotators to -2.3 / -2.7 se: H3 would hold and the label would become HOLDS EXCEPT
with H5 NO POWER and no fail. ATLAS3D at Salpeter would fail H2 (b): two fails, label FAILS. The criteria grade the
main table at the frozen distances and at Chabrier, so neither applies.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
