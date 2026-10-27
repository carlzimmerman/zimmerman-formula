# P1D4_m6_native_3d_forest: AMENDMENTS

## A1 (committed alone, after a Step-0 S0c failure, before any table or data fit)

The first launch failed S0c: the box Gaussian P1D deviated from the analytic projection by 7.76 % at k ≈ 7.6 h/Mpc, with
skewer stride 4. The run was stopped before any table was built, and no data fit was ever made. Its header lines remain in
`p1d4_m6_3d.out` (append mode).

| stride | max deviation, k_f..8 h/Mpc | max deviation, k_f..6 h/Mpc |
|---|---|---|
| 4 | 7.76 % | 4.89 % |
| 2 | 4.48 % | 3.19 % |
| 1 | 3.95 % | — |

All deviations were measured on synthetic fields only.

- **Diagnosis.** The excess deviation near the box Nyquist (12.6 h/Mpc) is the truncated transverse integral of the 1D
  projection. Stride adds skewer-sampling noise on top of it.
- **Change 1: S0c range.** k_f ≤ k ≤ 6 h/Mpc. The largest k actually used is 5.5 h/Mpc (DESI z = 4.4,
  0.043 s/km × cz).
- **Change 2: stride 2.** Every mock uses stride 2, so 128² = 16384 skewers. Stride 4 would pass at 4.89 %, at the edge
  of the 5 % line, so the safer stride was chosen.
- **Disclosure.** Both choices were made after seeing these synthetic S0c numbers. No DESI value entered.
- **Unchanged:** model, grids, gates, thresholds and variants.

## A2 (committed before the restart): sharded table build (code only)

The serial table build would take about 10 h: no table finished in the first 27 min. The tables are independent per
(footing, z), so `P1D4_SHARD="i/n"` runs a table-only worker that builds the jobs with index ≡ i (mod n) and exits.
Five single-thread workers are used, each under 1 GB, in line with the small-job rule while the peer X48 zooms run. The
main script then reads all 24 tables; it refuses to fit if any table is missing.

- **Ordering.** Job order is canonical z-list first, then alt. An alt table whose canonical μ = 0 slice is not yet on disk
  is built in full, which yields an identical μ = 0 slice.
- **Unchanged:** grids, model, gates and fits.
