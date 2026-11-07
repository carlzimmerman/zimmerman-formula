# AK1 criteria addendum A1: three regime exponents (reported, not gating)

Filed after CRITERIA.md (local 8ed1798939, origin c61447452a) and before the AK1 run. It follows the addendum to
closure_2026_11_07/ARGON_AK1_PROTOCOL_2026_11_07.md. It changes no gate and no label line. Kappa = 1/2 FITTED; not
theory closed.

Disclosure: before this addendum, one code-check run was made, clock-only AC2q row 1 at N 4000. It confirmed that the
core equals FS2's file (t_reg, t_fold, J_min and the step count are identical) and that the snapshot fields are
filled. It is a single row and enters no fit.

## Exponents, per footing, with bootstrap errors

Bootstrap: 2000 resamples over rows, seed 12345, 16-84 % interval. Fits use the graded rows (AC2q clock-only and
phantom) at Delta = 0.5, N 8000. Rows whose reading is zero or non-finite are dropped, and their count is stated.

- **alpha_L = d ln(width) / d ln L\*.**
  - The L* sweep is the lower L* (21.7 / 22.9 pc), x2, and 90 pc. A row enters if it has all three, with every other
    parameter equal.
  - Width = R_delta's FWHM. W, the collapsed-layer thickness, is reported too.
  - Per row: the least-squares slope over the three L* values. Reported as the median over rows.
- **alpha_v = d ln v_post / d ln v_f** across the AC14 depth grid (5 hosts x w x M - 1), at the lower L*.
  - v_f is the row's max |v| up to t_reg.
  - One pooled least-squares slope per footing and kind.
  - M234 / M490 are not fold runs, so they are absent (CRITERIA.md, Disclosure 2).
- **alpha_M = ln(v_post[Pi^6] / v_post[Pi^4]) / ln sqrt 2.**
  - This machinery switches with max(Pi, 0). A Pi^6 or Pi^4 core differs only for Pi near 0, so alpha_M is computed
    from the run-wide min Pi on pressure cells.
  - If min Pi / s^2 (clock-only) and min Pi / Pi0 (phantom) stay >= 0.5 on every graded row, no pressure cell enters
    any blend confined to Pi in [0, s^2/2]. alpha_M is then reported as 0 by construction, with those minima.
  - Otherwise alpha_M is reported as "not computed: the blend region is visited", with the rows named.

## Regime reading (the protocol's table, reported beside the frozen label)

| | alpha_L | alpha_v | alpha_M |
|---|---|---|---|
| Regime I | 1 | > 0 | — |
| Regime II | 2/3 | 2/3 | ~0 |
| Regime III | 2/3 | 0 | 1 |

The three measured exponents are printed next to these rows. AK1's label stays the one CRITERIA.md freezes.
