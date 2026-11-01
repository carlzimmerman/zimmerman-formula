# NR1 AMENDMENT A1 (after a first run that failed K1 and K2; no verdict was issued)

The first run stopped at NOT DECIDED. Both checks failed for errors of mine in the criteria, not in the grader. **I saw that run's Υ values**, so this rerun is not blind to them. No pass line changes.

1. **K1 named the wrong map.** CE1's table is built by c_f = 4 (η/10.82)^0.8 (`ce1_grade.py`), not by inverting the NFW map, which gives 7.74 at 25.937. The wrong map ran PRIMARY at η(10¹²) 20.38, not 21.53. K1 is now: this formula at 25.937 returns 8.0503, and the grader's own reported η(10¹²) equals the intended value within 0.01 in every run.
2. **K2 named the wrong baseline.** `NF1_N0` used CE1's A3 table, not A4's, so it can't match. K2 is now: CE1's A3 table, ρ 1, 1 through this path against `NF1_N0`, |d| ≤ 1e-9.
3. **K3 added:** A4's table, ρ 1.128, 0.938, against `NF1_NATIVE`'s results, Υ and rms |d| ≤ 1e-9. That is the pass this lane regrades.
4. The first run's files are removed from the lane. Its Υ values, for the record: PRIMARY 0.77 / 0.79, ALT 0.90 / 0.91, LOW 0.85 / 0.87, HIGH 0.75 / 0.76, MUTATE 1.20 / 1.20, all with the wrong map's lower η(10¹²).

Everything else in `FROZEN_CRITERIA.md` stands. κ = ½ FITTED. Not theory closed.
