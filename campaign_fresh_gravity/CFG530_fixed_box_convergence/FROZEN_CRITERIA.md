# CFG530 FROZEN CRITERIA: fixed-box resolution study of the CFG527 law-respecting engine, box-size check at matched resolution, and the L200 512^3 growth gate

Committed alone, before any code or run. Date 2026-10-09.

## Why

CFG527 (law-respecting engine: compensation drawn only from the shell D = turnaround catchment AND NOT census edge, weight s_c, existing 1/q cap, per-catchment conservation, unfiltered MOND source) was LAW-CONSISTENT (core R 0.94-0.98, L200-L25) and GROWTH OK at L200 256^3 (max|P-1| k <= 1: 0.090 canonical / 0.097 alt), but PARTIAL: P/P_S0 at k = 2, 4 did not converge across L = 100 -> 50 -> 25 at fixed N = 256.

Method issue: varying L at fixed N changes two things at once, the cell size AND the box (missing large-scale modes, a few dominant catchments; a 25 Mpc/h box is barely larger than the largest turnaround spheres, where catchments percolated and the cap emptied shells). A convergence test varies RESOLUTION AT FIXED BOX. This lane does that, separates box size from resolution at matched cell size, and runs the 512^3 L200 growth gate CFG527 deferred.

Settings (unchanged from CFG527): kappa = 1/2 FITTED; footings 9.3603e-11 (canonical) and 1.1312e-10 (alt), judged separately and never pooled; a0 FLAT; nu_mono; T1 switch eps = 0.077; census fret_of (CFG416), census edge, turnaround catchments (CFG424); expelled baryons gravitate (CFG518); LCDM background; EH ICs at z_i = 49 (the only LCDM input); step grid; seed 359. The cold energy's MASS is still required. Not "theory closed". Nothing downloaded.

## Engine: CFG527 UNCHANGED

- `cfg527_pm.py` is IMPORTED from `CFG527_law_respecting_engine/` (not edited, not copied). sha256 at freeze: `aeabd0ba4ca5ff1a3b1cc3c17a895821670608397928cfa42d3f03707bd50df0`. The launcher checks this hash before every job and refuses to run on a mismatch.
- The launcher (`run_530.py`) sets, exactly as cfg527_pm.py's `__main__` would: environment CFG527_* (THREADS, NSEED, FRET_MODE, NOCOMP, DRAW, L, RMIN, MUTATE = 0) before import; then module globals RC = 0, MIX, FRETX = 1; then calls `run("RES"|"S0", "FLAT", foot, N)`. The only override is the module's output directory `WORK` (and the read-only Delta_ta table path `DTA_FILE`, pointed at a byte-identical copy, sha256 checked), set to a per-job folder under `_external_data/cfg530_work/runs/<job>/`, so nothing is written into CFG527's folder and run tags with different NSEED / RMIN never collide.
- Law statistic: CFG526's `cfg526_profiles.py` (sha256 `c174adfd2f8c203535324b146b32483ca404e3b3e3ea04203fcd48f2cadbe8ba`) imported as a module, as CFG527 did. Changes, all declared: (i) the module global NP is set per run to that run's N (it is the mesh size; CFG526 hard-coded 256); (ii) the cache directory WORK is set per N (`profiles/N<N>/`), so the matched S0 at that (L, N) is the one used (`S0_L<L>` inside each N folder); (iii) each run's engine is loaded with its own RMIN and mix (module attributes set after CFG526's loader, as CFG527 did for the mix); (iv) in `analyse` the one line `rmin = 2 * L / 256 if L != 200 else 1.56` is replaced by `rmin = mod.RMIN_PHYS` (source substitution, asserted to occur exactly once). For every run CFG526/527 ever scored these are the same number (2L/256 at L != 200; 1.56 at L200), so the statistic is unchanged; the BX runs below need it because their RMIN differs from 2L/256. Identity check: the patched statistic applied to CFG527's own LRcan/LRalt L100 and L200 256^3 caches must reproduce cfg527_profiles.json core R to 1e-12 (else the lane is INVALID).

## Fixed physics across resolutions (declared)

- **RMIN fixed in physical units per box**, the CFG527 value: 0.78125 Mpc/h at L = 100 (= 2 cells of the 256^3 mesh, CFG521's rule "2 cells of the 256^3 mesh"), 1.56 Mpc/h at L = 200. It is NOT rescaled with N; the host population definition is therefore the same physical one at every N. (At N = 128, L = 100 it equals 1 cell.)
- **Same realization at every N:** NSEED = 512 for every study run (N = 128, 256, 512), so the white-noise field and hence every large-scale mode common to the meshes is identical; N only adds small-scale modes. (CFG527 used NSEED = 256 at 256^3; those are a different realization, used here as the reproduction control and as a realization-noise floor.)
- Engine-internal resolution dependence, disclosed not changed: the host-radius grid Rg = geomspace(dx, 8, 14) and the discrete-ball profile radii (in cells) scale with dx.

## Runs (all z = 0 unless stated; seed 359; nice 10)

| block | job | draw | source | foot | L | N | NSEED | RMIN |
|---|---|---|---|---|---|---|---|---|
| study | S0_L100_N{128,256,512} | S0 | - | - | 100 | 128/256/512 | 512 | (unused) |
| study | S0_L200_N{128,256} | S0 | - | - | 200 | 128/256 | 512 | (unused) |
| study | S0_L200_N512 | reuse CFG411 S0 N512 if verified (below), else run | | | 200 | 512 | 512 | |
| study | LRcan / LRalt _L100_N{128,256,512} | SHELL | NOFILT | can / alt | 100 | 128/256/512 | 512 | 0.78125 |
| study | LRcan / LRalt _L200_N{128,256,512} | SHELL | NOFILT | can / alt | 200 | 128/256/512 | 512 | 1.56 |
| box check | BXcan / BXalt _L100_N{128,256} | SHELL | NOFILT | can / alt | 100 | 128/256 | 512 | 1.56 |
| control | REPcan / REPalt _L100, _L200 | SHELL | NOFILT | can / alt | 100 / 200 | 256 | 256 | CFG527 |
| control | MUTA_L100_N256 | SC (= CFG521 old draw) | MIXA | can | 100 | 256 | 512 | 0.78125 |

Scheduling: <= 256^3 jobs through a claim-based queue (mkdir claims), up to 4 workers, 4 threads each, detached with nohup. 512^3 jobs run ALONE (no other job of this lane running), 8 threads, one at a time, in this priority order: LRcan_L200_N512 (the growth gate), S0_L100_N512, LRcan_L100_N512, LRalt_L200_N512, LRalt_L100_N512. Memory is watched (no swap); a 512^3 job is not started while a <= 256^3 job of this lane runs. Any 512^3 job not finished when the lane is written up is PENDING and every verdict that needs it says PENDING.

**S0 512^3 reuse (L200).** CFG411's S0 N512 (L200, seed 359, NSEED = max(256, N) = 512) is reused only if ALL of: (a) the S0 code path is identical (initial_conditions, step_grid, Mesh, measure_pk, the S0 branch of forces, the run loop; diff shown in the README), (b) cfg527_pm.py's initial conditions at N = 512, NSEED = 512 reproduce CFG411's zi snapshot exactly (|d sigma8|/sigma8 <= 1e-12 and max|dP/P| <= 1e-10), (c) re-measuring P(k) from CFG411's saved z = 0 positions with cfg527_pm.py reproduces CFG411's z0 P to max|dP/P| <= 1e-6 (float32 positions). Otherwise S0_L200_N512 is run (after the queue above). sha256 of the reused files recorded.

## Statistics (z = 0)

- **r(k) = P_run / P_S0** at the same (L, N, NSEED), particles, nearest k bin, at k = 1, 2, 4 h/Mpc, evaluated only where k <= k_Nyq/4 = pi N / (4 L) for that N (L100: N128 k <= 1.005, N256 <= 2.01, N512 <= 4.02; L200: N128 <= 0.50, N256 <= 1.005, N512 <= 2.01).
- **Core R** = CFG526 statistic (median M_grav / M_law over scored radii <= 2 cells, 100 densest scored hosts), per run, needs >= 20 scored halos. Also reported: R at every scored radius, and median log10 R at shared physical radii N256 R = 1, 2, 4 cells = N512 R = 2, 4, 8 cells (log M_ta 12.7-14.3, >= 10 halos each), reported only.
- **Cap / percolation** (per run, from the run JSON diagnostics at z = 0 and the max over snapshots): q_max, cap_n, cap_mass_frac, cap_e_removed_frac, shell_frac, n_shell_empty, n_catch; and from the profile pass (engine forces on the z = 0 state): largest-catchment mass share (fraction of catchment mass in the biggest periodic component) and whether that component is slab-spanning (its cells occupy every one of the N planes along at least one axis; a necessary condition for percolation, reported as "spanning").

## Verdicts (per footing, never pooled)

**1. Resolution convergence (per box, L = 100 and L = 200), between the two highest N (256 and 512):**
- items: |r_N512(k) - r_N256(k)| <= 0.05 at every k in {1, 2, 4} with k <= k_Nyq/4 of N256 (L100: k = 1, 2; L200: k = 1); and |log10 coreR_N512 - log10 coreR_N256| <= 0.05 dex (both with >= 20 scored halos; if either has < 20 the R item is NOT EVALUABLE and the box verdict says so).
- box verdict CONVERGED if every evaluable item passes and the R item is evaluable; NOT CONVERGED (items named) otherwise; PENDING if a needed run is missing.
- footing verdict: CONVERGED if both boxes are CONVERGED; NOT CONVERGED if either is NOT CONVERGED; else PENDING / NOT EVALUABLE.
- k = 4 at L = 100 is resolved only at N = 512 (would need N = 1024 for a pair): reported, NOT part of the verdict. The N128 -> N256 step is reported (trend), not gating.

**2. Box-size effect (matched cell size AND matched RMIN, so the physics differs only in box size and realization):**
- pair P1: BX_L100_N128 vs LR_L200_N256 (dx = 0.78125, RMIN 1.56); pair P2: BX_L100_N256 vs LR_L200_N512 (dx = 0.390625, RMIN 1.56). Also reported (RMIN differs, as named in the task): LR_L100_N256 vs LR_L200_N512.
- items: |Delta r(k)| at k = 1, 2, 4 where both members resolve it (k <= k_Nyq/4 of each member), and |Delta log10 core R|.
- realization floor F: the same-box, same-N, different-NSEED differences REP (NSEED 256) vs study (NSEED 512) at L100 N256 and L200 N256, per item, max over the two boxes.
- BOX-SIZE EFFECT = YES if any item in P1 or P2 exceeds BOTH the tolerance (0.05 in r, 0.05 dex in R) AND 2F for that item; NO if every evaluable item is within the tolerance; NOT SEPARABLE if items exceed the tolerance but none exceeds 2F; PENDING if P2 is missing and P1 says NO (P1 alone gives a verdict if it says YES).

**3. Growth gate, L = 200 512^3 (CFG361 cuts at z = 0, k <= 1 h/Mpc, vs S0 N512):** GROWTH OK if |sigma8 ratio - 1| <= 0.05 and max|P/P_S0 - 1| <= 0.10 over every bin with k <= 1; FAIL if |sigma8 ratio - 1| > 0.2; TENSION otherwise. Canonical first; alt if it finishes (else PENDING). This is the 512^3 confirmation CFG527 deferred (stated as CONFIRMED / NOT CONFIRMED relative to CFG527's 256^3 GROWTH OK).

**4. Controls:**
- **REP (reproduction):** REPcan/REPalt at L100 and L200 must reproduce CFG527's LRcan/LRalt L100 / L200 256^3 JSONs: |d sigma8|/sigma8 <= 1e-8 and max|dP/P| <= 1e-8 at every snapshot. A failure makes the lane INVALID.
- **MUTATE (CFG521 old draw, SC + MIX-A, L100 N256 NSEED 512 canonical):** must come out NOT law-consistent (some scored radius or the core R outside 0.1 dex of 1, as in CFG526/527). If it is law-consistent, the law statistic has no teeth at this setup and every R item is NOT DIAGNOSTIC.
- **Statistic identity:** above (cfg527_profiles.json core R reproduced to 1e-12).
- **Stability (as CFG527):** each NOFILT run finite at every snapshot and P/P_S0 at the bin nearest k_Nyq/2 <= 2; an unstable run is reported and its items are INVALID.

## Reported (not gating)

r(k) at k = 0.3, 1, 2, 3, 4, 8 (resolved bins) for every run; law consistency (core R within 0.1 dex) at every N; the N128 -> 256 -> 512 trends; NSEED-256 vs NSEED-512 differences; sigma8 ratios; the cap / percolation table vs N and L.

## Caveats (declared before running)

- One realization per (L, NSEED). PM forces are softened below about one cell; halo cores are 1-2 cells, so core R at different N is at different physical radii (law consistency at each resolution, not one physical radius).
- The draw is bookkeeping of the cold share s_c; the cold energy's MASS is still required.
- The census still paints group f_ret over galaxies inside group turnaround balls (CFG521).
- kappa = 1/2 is fitted; f_b and rho_Lambda are not derived. A pass is not "theory closed".
