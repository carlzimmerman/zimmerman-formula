# CSM2: single-L search and native estimator stress test

The target remains open: one consistent L passing the fixed corrected model's
unchanged observational criteria. No fitted parameter has been added. See
`TARGET.md` for the predeclared portfolio and finite grid.

## Completed finding: native crossing instability

Changing only radial edges exposes an earlier descending -2 crossing in two
of the three completed ng64 profiles. The prescribed first-crossing rule then
selects a different feature:

| Seed | c_f, 21 edges | c_f, primary 25 edges | c_f, 29 edges |
|---:|---:|---:|---:|
|3|3.010853|3.138159|16.803760|
|7|2.426993|2.441598|11.798147|
|8|4.068233|4.010123|4.038780|

All tested binnings pass the original synthetic c=4 control. That benchmark
and the `ok` flag alone therefore do not establish robustness on these profiles.
Independent reconstruction reproduces the original selected radii and shows:

- Seed 3: 29-edge crossings at 7.89 and 41.69 kpc, compared with one primary
  crossing at 42.27 kpc. The extra inner crossing encloses 541 particles.
- Seed 7: 29-edge crossings at 11.68 and 56.06 kpc, compared with one primary
  crossing at 56.45 kpc. The extra inner crossing encloses 984 particles.
- Seed 8 has one crossing near 33 kpc under all three tested binnings.

This does not identify which feature is physically correct or justify choosing
the outer crossing to restore a preferred L. The original primary results
remain unchanged. Their L proxies 1.972/1.535/2.521 are conditional partial
measurements, not a robust derivation. The 29-edge fixed-reference proxies
are diagnostics, not alternative recalibrated L estimates: the entire ng48
reference was not refit under each variant.

Paired ng64/ng48 c_f ratios for seeds 3/7/8 are 0.438/0.457/0.307. Multiplying
by 7.31 gives paired diagnostics 3.201/3.343/2.241; these do not replace the
prescribed ensemble-reference normalization. They show why seed variation and
resolution transfer need separate checks.

`native_diagnostic_001/` passes 4/4 controls, including reproduction of cached
ng48 and published ng64 measurements. `crossing_002/` independently reproduces
all nine profile variants with 3/3 controls. Both have bounded manifests,
input hashes, scripts, raw results and pre-computation criteria. Neither a raw
simulation nor an old measurement was changed.

The first crossing run's inherited contract text incorrectly described six
snapshots although its actual hashed inputs were the three ng64 snapshots.
That metadata record is retained in `crossing_001/`. A corrected-description
contract and fresh `crossing_002/` reproduce its scientific JSON byte for byte;
the corrected run is authoritative for this diagnostic.

## Active necessary-constraint search

`run_001/` is an active bounded grid, not a final result. The group-only
reduction and cached-template lens score reproduced full CSM1 before new cells.
It grades groups first and lensing where canonical groups pass. Any surviving
point still needs every remaining full criterion. A failed finite grid cannot
exclude all real L. The active run directory is excluded from the initial
completed-audit publication. See `CONTINUATION.md` for pending work.
