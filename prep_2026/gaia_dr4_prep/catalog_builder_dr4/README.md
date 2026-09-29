# catalog_builder_dr4: release-day scaffolding for cuts 12 and 13 (NEW files only)

Written 2026-09-28. **Nothing here changes a frozen cut.** `PREREGISTRATION_DR4.md`, every `*_HASH.txt`, every
`AMENDMENT*.md`, `catalog_builder/*.py` and `wide_binary_pipeline.py` are untouched (read-only imports only, bytecode
writing disabled). No network, no downloads. Which criterion is primary is an owner decision (Amendment 16 draft,
item (b) open point); these files only make both runnable side by side.

Run: `python3 test_cut13.py` (about 3 s; exit 0 only if every real test passes AND the MUTATE control is caught) and
`python3 cut12_stub.py` (self-test).

## Implemented

- `cut13.py`: `third_star_literal(cat, a, b, ...)` and `third_star_orbit_aware(cat, a, b, ...)`, identical signatures,
  both return `ThirdResult(flags, n_neigh, n_no_g, n_no_g_kin, n_hit)`.
  - Literal = frozen row 13 text: `dpar < 3`, `dmu < 5*sdmu`, `G < 20`, within 30 kAU (projected, from the primary's
    parallax) of either component. Reference star for "the pair" = the primary by default (same as the existing
    code, so the two differ only in the PM bound); `reference="mean"` is available. That reading of "the pair" is my
    interpretation, the frozen text does not say.
  - Orbit-aware = `build_catalog.py` `third_star_flags` (lines 364-387): `dpar < 3`, `dmu < orb + 2*sdmu`,
    `orb = 0.44428*plx^1.5*theta^-0.5`, `G < 20`. Reproduced exactly, including two quirks: theta and the parallax/PM
    reference are taken from the PRIMARY even for a third found near component b.
  - Sources with no G value are never flagged (NaN < 20 is False) and are counted separately: `n_no_g` (all
    neighbours in the radius) and `n_no_g_kin` (those passing the kinematic test, i.e. the thirds the G < 20 lookup
    would silently drop). Never folded into `flags`.
- `test_cut13.py` (synthetic only): error-model drift check against `wide_binary_pipeline.py` lines 200-206; a 66-cell
  grid (third G 15-20, d = 100/150/250 pc, third at 29.9 and 10 kAU) in which the real functions' PM thresholds must
  bracket the analytic `5*sdmu` and `orb + 2*sdmu` (240-point delta scan, so exact to one grid step); Amendment 16
  arithmetic; boundaries (G strict, NaN G, 3 sigma, 30 kAU, near b); agreement of the orbit-aware function with the
  builder's own `third_star_flags` on 300 random pairs (0 mismatches; builder 126 hits, literal 48); MUTATE control
  (PM inequality inverted: T1 and T3 both fail as required).

## Result of the comparison (approximate DR4 error model, pair at G = 17, third at the 30 kAU edge)

"Flags more" means the accepted PM window is wider, not that more stars are removed; the count depends on the real
distribution of thirds, which is not modelled here. The 5 sigma window (literal) wins only when `3*sdmu > orb`.

| d | orbit-aware flags more | literal flags more | crossover third-G |
|---|---|---|---|
| 100 pc | every G 15-20 (equal within 0.03 mas/yr at G 20) | none | none in range |
| 150 pc | G 15-19 | G 19.5-20 | 19.46 |
| 250 pc | G 15-18.5 | G 19-20 | 18.90 |

At 10 kAU (interior) the orbit-aware window is larger still; literal wins only at 150 and 250 pc for G = 20.
This matches the Amendment 16 draft arithmetic: orb(250 pc, 120") = 0.3245 mas/yr, crossover sdmu = 0.1082 mas/yr,
per-star DR4 errors 0.026/0.052/0.111/0.259 at G = 17/18/19/20. G = 19 at 250 pc is a near-tie (0.570 vs 0.553
mas/yr). "At 100 pc the code flags more throughout" holds, barely, at G = 20.
The synthetic grid's top column is planted at G = 19.999, because G < 20 is strict and a G = 20.0 third is never flagged.

## Stub

- `cut12_stub.py`: `nss_union_flags(source_ids, ids_by_table, counted_tables, excluded)` returns a per-source boolean
  flag plus a manifest-ready report; `pair_nss_flags` reduces to pairs (either component). The list of counted tables
  is a run-time parameter; the only table name in the file is the documented placeholder `PLACEHOLDER_NSS_TABLE`,
  which raises if used. It refuses an empty list, unknown tables, and any supplied table that is neither counted nor
  excluded with a written reason. **Which `nss_*` tables count is not decided here** (judgement about their content
  from the published data model; checklist section 0 item E). There is no table loader.

## NOT tested

- Any real DR3 or DR4 join, table, column name, or row count. `all_source_astrometry` / `all_source_photometry`
  search, the join on `source_id`, and how many sources lack G there are all untested; the functions take arrays.
- Search performance at 2.8 billion sources (the loop here is per-pair and only sized for tests; a real all-source
  run needs a spatial index or a server-side cross-match, which would need its own dry run).
- The real NSS tables (names, solution types, overlap between tables, whether any table counts).
- The error model is the repo's approximate one (DR3 table x 0.372), not a published DR4 table; the regime table is
  arithmetic on that model.
- Whether a real third star's PM offset distribution favours either criterion (needs a data run of both; Amendment 16
  draft says the same).
- The literal reading of "of the pair" (primary vs mean reference) has not been measured against the alternative on
  data.
- Cuts 9 (SFD98 vs `ap_*`), 11, variant (c) and the join code of checklist items C/D are not addressed here.
