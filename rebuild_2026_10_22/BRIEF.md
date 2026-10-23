# From-scratch empirical rebuild of the remaining failures (2026-10-22)

The owner's instruction: "we need to figure this out empirically from scratch again and make sure no assumptions were
made or new findings that we have when calculated with the data don't make sense after all."

## The failures to rebuild

1. **Cluster cores:** raw KiDS lensing stacked on 318 eRASS1 clusters sits at 1.91× (canonical) / 1.75× (alt) the law
   inside ~1 Mpc (status board column 3; CFG949, CFG954, CFG959, CFG962 and neighbours).
2. **Isolated-galaxy lensing beyond ~0.4 Mpc:** the prediction falls short (Δχ² ≈ +100 canonical); the two-halo term
   does not close it (status board column 2; CFG801–804, CFG902 and neighbours).
3. **Structure growth and cosmic shear:** growth on the full gravitating mass 15–19 % too clumpy at 512³ (CFG555/556);
   canonical settling rules excluded by raw KiDS ξ± (CFG596, Δχ² +68.7). CFG960 (1024³ native, running now) is the
   native rerun — do not touch or duplicate it.
4. **No-go:** "one local theory with the law, the right growth and no external-field effect" (status board column 5).

## What changed since those verdicts were scored (each must be applied, or shown not to matter)

- The theory's field equation is **AQUAL** with μ = x/(1+x), not QUMOND (doors E2; covariant C4). Earlier lanes that used
  QUMOND or an additive EFE recipe used standard-MOND machinery as a hidden ingredient.
- The surviving theory is **screened**: stiffness L★ ≥ 21.7 / 22.9 pc (D10), relevant only for small systems.
- The covariant theory's cold sector is **Blanchet–Skordis K(Q) dust** with abundance as an initial condition (C2, C4, C5);
  its linear growth is GR growth on that dust (C2: γ = 0.555, f(0) = 0.510 on the dust-limit background). a₀ is absent
  at linear order on FRW.
- The framework's **native H₀ is 67.2–68.6** (C2, A78 BBN bound), not 55–57.5. Distances and h-conventions in every
  lensing/cluster pipeline must be checked against it.
- Doors E1/E4: SPS stellar masses, h = 0.70 conventions (CFG687), r200c/splashback labels and the alt footing's
  inputs were flagged as soft or ΛCDM-processed.

## Rules (in addition to `doors_push_2026_10_22/BRIEF.md` and `BRIEF_E_AUDIT.md`, which apply)

1. **Rebuild independently.** Write your own pipeline from the rawest data on disk. Use the record's earlier scripts only
   as a cross-check you must reproduce first (to show you read the same data), never as the source of your verdict.
2. **Assumption ledger first.** Before any number, list every assumption and inherited ingredient of the original verdict
   and of your rebuild, classified RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED /
   STANDARD-MOND-MACHINERY, with file references. Commit it with the frozen criteria.
3. **Apply each change above** (AQUAL, screening, BS dust, native H₀, E1/E4 flags) one at a time, and report how the
   failure statistic moves with each. A failure that survives every correction is a real failure; say so plainly.
   A failure that disappears must be explained by a named ingredient, and the cure must not be a new fitted knob.
4. **No new free parameters.** No knob scans to make a failure pass.
5. **Compute:** CFG960 (1024³, ~31–40 GB) is running. Every run: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes.
   No PM simulations. No downloads (if raw data are missing, list exactly what and stop).
6. Frozen criteria committed alone first; checks + `--mutate`; pathspec commits of your lane only; never push.
   Lane dirs: `rebuild_2026_10_22/<lane>/`. κ = ½ FITTED; both footings, never pooled; no dark-matter particle;
   never "theory closed"; never "the data favour the framework".
