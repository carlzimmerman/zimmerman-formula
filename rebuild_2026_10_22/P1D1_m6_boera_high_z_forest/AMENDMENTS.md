# P1D1_m6_boera_high_z_forest: AMENDMENTS

## A1 (committed alone, before any P1D value is read): how S0e reproduces X63

`x63_m6_forest.py` is a top-level script. Importing it runs it and overwrites X63's committed outputs, so its formulas
cannot be imported without side effects. S0e is therefore met by an **independent re-implementation** of X57's / X63's
M6 formulas in this lane's script. The formulas re-implemented are:

- X57 L399–428: f_max → δ_c,in, δ_b,in; σ²_ad(R_L, 0) from the BBKS shape; F_b,max.
- X63 L147–206: P_ad0, `p1d` on KG (logspace −4 to log 200, 60001 points), iso amplitude, ratio grid.
- X63 L203–206: s/km → h/Mpc.

On the inherited background, the re-implementation must reproduce X63's **committed** `x63_m6_forest_results.json` to
3 decimals, as S0e already requires: max S at R_J 0.1, z 4.2 / 4.6 / 5.0, both footings, and F_b,max(z = 3). This
is stricter than importing, because it is a second implementation checked against the first. Two things are unchanged:

- X22's f_max and R_L are read from X22's committed JSON, as X63 does.
- Gates, thresholds, model, variants and checks are unchanged.
