# CFG881 — FROZEN CRITERIA: how much clump-like extra mass can SPARC galaxies hide?

Frozen before any script (owner block 880–889, reserved 183d844e6). κ = ½ FITTED; ν_e; footings 9.3603e-11 (canonical, primary)
and 1.1312e-10 (alt), reported separately, never pooled. Not theory closed. No dark-matter particle; no ΛCDM inputs.

## Question
CFG877: one bound cold-energy clump per faint dwarf, σ_x = V_x/√2 (V_x from cfg870_results.json), M_cl = 81σ_x⁴/(4Ga0)
(5.25e6 M_⊙ canonical / 4.24e6 alt). CFG878 (post-hoc hypothesis, route 2): the clump forms once in first atomic-cooling systems
("blocks", σ ≈ 7.4–8.2 km/s) and is retained ("overfill"). A block's baryonic mass in the law is M_block ≈ 81σ_b⁴/(4Ga0).
If a galaxy of baryonic mass M_b was assembled from N_blocks = M_b/M_block blocks and a fraction F_ret of their clumps was kept,
it carries extra mass F_ret · N_blocks · M_cl. SPARC sits on the law, so SPARC bounds F_ret.

## Data and cuts (CFG870's sparc(), unchanged except the mass cut)
SPARC_Lelli2016c.mrt + sparc_data/*_rotmod.dat. Q ≤ 2, Inc ≥ 30°, points with V > 0, R > 0, eV/V < 0.10, g_bar > 0;
g_bar = (Vgas|Vgas| + 0.5 Vdisk|Vdisk| + 0.7 Vbul|Vbul|)/R; M_b = 0.5 L[3.6] + 1.33 M_HI (CFG870's definition). **All masses**:
"massive" M_b ≥ 1e9 M_⊙ (class sample), "dwarf" M_b < 1e9 (reported, no class). Law g_law = g_bar ν_e(g_bar/a0).

## Per-galaxy bound (one statistic, four retained-mass shapes)
For points i in a window W: r_i = log10(g_obs,i/g_law,i), σ_i = 2 eV_i/(V_i ln10).
- δ_W = median r_i; σ_med = 1.2533 · max(√⟨σ_i²⟩, std(r_i)) / √n; σ_W = √(σ_med² + floor²), **floor = 0.10 dex** per galaxy
  (distance / inclination / Υ; variant 0.20 dex reported).
- Upper limit δ_up = max(δ_W, 0) + 2σ_W (one-sided; a galaxy below the law is not allowed to tighten its own bound).
- M_max solves median_{i∈W} log10(1 + g_x,i(M)/g_law,i) = δ_up (bisection; monotone in M), where the extra mass adds its
  Newtonian pull g_x = G M_x(<R)/R² on top of the law (**convention A**, the one CFG870/877 used for M_x and M_cl).
  Variant **convention B** (extra mass is a source through the law: g_law(g_bar + g_x)/g_law) reported, not deciding.

Shapes (M_x(<R) = M · s(R)) and windows:
1. **CORE1** (clumps sunk to the centre): uniform sphere, s = min(R/1 kpc, 1)³; W = points with R ≤ 3 kpc, n ≥ 3.
2. **CORE3**: uniform sphere radius 3 kpc; W = points with R ≤ 6 kpc, n ≥ 3.
3. **BARYON** (disrupted clump material spread like the stars and gas it came in with): g_x = F g_bar, i.e. M_x(<R) = F × the
   baryons' own enclosed (Newtonian-equivalent) mass; W = all points (n ≥ 3). F_max is read directly; M_max = F_max M_b.
4. **FLAT** (spread as M ∝ R out to the last point, everything within R_last): s = R/R_last; W = all points (n ≥ 3).
Mass beyond the last measured point is invisible to rotation curves (stated, not bounded).

## Clump units and retained fraction
N_max = M_max/M_cl. F_max = M_max/(N_blocks M_cl) = (M_max/M_b)(M_block/M_cl). **Primary: σ_b = σ_x, so M_block = M_cl and
F_max = M_max/M_b** (BARYON: F_max directly). Variants: σ_b = 7.36 and 8.22 km/s (CFG878's bracket) → F × 0.913 / × 1.42.
N_blocks = M_b/M_block assumes all baryons came through first-cooling blocks (an upper bound on blocks), so **F_max bounds the
product φ·F_ret**, φ = fraction of the baryons assembled through blocks. No record-based smaller φ exists; none is used.

## Classes (per footing; massive sample; population median of F_max per shape)
Per shape: EXCLUDED if median ≤ 0.1 (clumps must drain or disrupt ≥ 90%); ALLOWED if median ≥ 1; PARTIAL in between.
- **RETENTION EXCLUDED IN BIG GALAXIES:** all four shapes EXCLUDED.
- **RETENTION ALLOWED:** all four shapes ALLOWED.
- **SHAPE-DEPENDENT:** at least one shape EXCLUDED and at least one ALLOWED (named).
- **PARTIAL:** anything else.
Both footings must agree; else reported as "canonical (alt X)". Also reported: 16/84th percentiles, fraction of galaxies with
F_max ≤ 0.1, the floor-0.20 and convention-B variants, the σ_b variants, dwarfs, and N_max.

## Controls
- **K1 (code identity):** with the same per-point arrays, the script reproduces CFG877's canonical SPARC D (0.029482523013537265,
  clump finite, M_b ≤ 3e9) and CFG870's canonical T1 D (0.012706462151106651) to < 1e-9.
- **K2 (solver round trip):** for each massive galaxy, set g_obs := g_law + g_x(M_test) exactly (M_test = 0.3 M_b, CORE1 and FLAT),
  floor 0 and no statistical error, δ_up = δ_W: the solver must return M_test to < 1e-6 relative.
- **MUTATE** (`CFG881_MUTATE=full|tenth`, separate output files): inject extra mass F_inj M_b (F_inj = 1 or 0.1) into g_obs with
  each shape's own form (convention A), re-run. Required: `full` → every shape median F_max ≥ 1 (class RETENTION ALLOWED);
  `tenth` → no shape EXCLUDED (median F_max > 0.1). Also reported: fraction of massive galaxies with δ_W − 2σ_W > 0 (detection).

## Pre-freeze disclosures
- Data coverage only was inspected before freezing (no law, no residuals): 147 galaxies pass the cuts, 122 massive / 25 dwarf;
  massive galaxies with ≥ 3 points at R ≤ 3 kpc: 48; at R ≤ 6 kpc: 95. The windows were set from these counts.
- Hand expectation before any run (order of magnitude, from G·1e11 M_⊙/(1 kpc)² ≫ typical inner g_obs): CORE1 F_max ~ 0.01–0.05,
  BARYON ~ 0.3, FLAT ~ 1. Disclosed so the outcome can be checked against it.
- CFG878's route 2 is itself post-hoc; this lane bounds it, it does not test whether first-cooling blocks exist.
- M_b from 0.5 L[3.6] treats bulge light at Υ 0.5 (bulges' curves use 0.7): M_b slightly low → F_max slightly high (conservative).
