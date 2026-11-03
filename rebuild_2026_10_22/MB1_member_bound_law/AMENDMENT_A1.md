# MB1 AMENDMENT A1: readings the criteria left open. Written after the code and before any check or graded number ran

Nothing here changes a gate, tolerance, arm or label. kappa = 1/2 FITTED; not theory closed.

1. **Bullet tide.** Criteria give M_c at d 300 kpc but no gamma. F and E use gamma = 1 there, with M_c = the subcluster's own model M300, which is projected. A rough reading; it isn't varied.
2. **Bullet stars per subcluster.** Each `GAL` component carries the R of the BCG its `GROUPS` row names. KG and K use their K on all components.
3. **Harness B28 for MB1 candidates.** `merger` isn't a listed sample inside `g`, so the harness row reads the law's and is reported as such. The lane's row replaces it, as the criteria say.
4. **K fit.** K per footing by bisection on the harness's own B23 value, to |mean| < 1e-4, from `rows_xcop`. KG the same.
5. **Mass grid.** 37 points in log m, weights summing to 1. R is an average, so its grid error is checked at twice the points on X-COP's mean; over 1 % is a failed check.
6. **The harness's files.** `old_gates.py`, `tolerances.json`, `row_marks.json` are byte copies beside `mb1_acc.py`, since it runs with this lane as its directory.
7. **K6 reading.** The keys path doesn't pass Mb to `g`, so K6 logs `gb r^2/G` at r500 from the first keys call of each cell, read against the same cluster's Mgas500 in `X30`'s table, within 5 % after f* and the gas scale.
