# DR9 AMENDMENT A1, written after the first run, committed before the second

**What failed.** MUTATE as frozen: eta_PG inverted must move overall Upsilon by more than 0.02. It moved 0.70 to 0.68, exactly 0.02 on the 0.01 grid. So the first run's verdict is NOT DECIDED (`dr9.out`, first run, kept in git history of this note only by these numbers: K0 0, K1 5.6e-6, K2 4.6e-4, K3 true, K4 0, K5 3.4e-3).

**Cause.** My line read the wrong statistic. The inverted form lifts dwarfs and lowers spirals, so the all-galaxy median nearly cancels; in that same row the tilt goes +0.33 to +0.69 and the bins go 0.48, 1.10, 0.90, 0.51, 0.49, 0.77 to 1.20, 1.17, 0.90, 0.51, 0.48, 0.57. The wiring plainly responds. That is a reading of numbers I have seen, so it doesn't by itself clear the frozen check.

**Change.** A second mutation, line stated here before it runs: MUTATE_A1, RET_FIT's C x 0.01, must move overall Upsilon background A by more than 0.02. The first MUTATE stays reported as a miss. No other line moves, and no row is rerun.

**Seen before this was written.** All rows and the label they would give. This is disclosed: the amendment can't be blind, and it can't change any row.

**Second disclosure, a defect in my rule on groups.** Groups Z reads 1.4979 in every row, including C 1e9. Traced with a one-group debug run: for groups the frozen E_undo is 0 (W(M_f) above W(M_0)), so the frozen "nothing to undo, f = 1" fires and the gate never acts. Likely cause, not proved: this grid's baryons are clamped to a central point mass under the first XG radius, and W doesn't count mass inside the grid's first point. So **no row here tests groups under the rule.** The frozen line isn't moved. The endpoints are read instead: NR3 f 0 Z +1.467, f 1 Z +1.498, both inside |Z| <= 2, so groups don't decide any row, but that is a bracket, not a grade.
