# CFG883 — FROZEN CRITERIA: do systems that never cooled their own gas carry the CFG877 cold clump?

Frozen before any script (owner block 880–889, CFG883 reserved in the LEDGER). κ = ½ fitted; footings 9.3603e-11
(canonical) and 1.1312e-10 (alt), never pooled; ν_e(y) = 1/(1 − e^{−√y}); raw data, framework-native only; no dark-matter
particle; not theory closed.

## Hypothesis and kill prediction (source: CFG878 Part C, route 2; POST-HOC candidate, disclosed there)
Each faint dwarf carries one bound cold-energy clump (CFG877: σ_x ≈ 7.5 km/s, ~5e6 M_⊙, ~100–200 pc) because the clump froze
in when the dwarf's progenitor was one of the first systems able to cool gas by atomic hydrogen (σ ≈ 7.4–8.2 km/s).
**Kill prediction:** stellar systems that did not form as their own first-cooling well — globular clusters, tidal dwarfs,
collision debris, ultra-compact dwarfs/stripped nuclei — carry **no** clump. The record already puts globulars and tidal
dwarfs in class E ("formed embedded, without a cold component: NEWTONIAN", FG001; CFG332, CFG820).

## Clump model (fixed by earlier lanes; nothing tuned here)
- V_x from `CFG870_cored_component_joint/cfg870_results.json` (10.6547 canonical / 10.5870 alt km/s); σ_x = V_x/√2;
  r_c = 104 pc; M_cl = 81 σ_x⁴/(4 G a0) (5.25e6 / 4.24e6 M_⊙).
- M_x(<r) = min[ V_x² r³ / (G (r² + r_c²)), M_cl ] (CFG877's `Mx`). The clump's gravity is Newtonian and adds linearly to the
  potential (CFG877 adds G M_x/(3 r12) to σ²; the Jeans form below is the same idea per bin).

## Data (repo only; provenance)
- **Globulars, profiles (PRIMARY):** `real_research/data/globular_clusters/baumgardt_gc_veldisp_profiles.tsv` (measured
  σ bins, Baumgardt web catalogue, retrieved 2026-09-03) and `baumgardt_gc_parameters.tsv` (R_sun, R_GC, Mass, M/L_V, rc,
  rh_l, rt). Stellar luminosity L_V = Mass/(M/L_V) (the catalogue's own photometric luminosity; the dynamical mass cancels).
- **Globulars, global σ (SECONDARY T2):** CFG332's table (`cfg332_globulars_results.json`: NGC 2419, Pal 3, Pal 4, Pal 14).
- **Tidal dwarfs (T3a):** `real_research/data/tidal_dwarfs/lelli2015_tdg.csv` (Lelli+2015 Tables 2/4/5; 6 young TDGs).
- **Compact objects beyond the LG (T3b):** `real_research/data/dsph/lvd_dwarf_local_field_distant.csv` rows with σ:
  KV19-212/271/329/442 and Fluffy (NGC 5128), SUCD1 (NGC 4594). KDG 64 (M81, r_h 1.2 kpc) is an ordinary dSph and is
  outside this test. Fluffy (r_h 30 pc) may be an extended cluster or a faint dwarf: class unknown, reported only.
- **NGC 1052 trail (T3c):** CFG655's frozen inputs (DF2, DF4, DF9; label E is an external label, CFG655/CFG768).
- **NGC 5557 E1 (CFG448):** no resolved kinematics exist → NO DATA. **Open clusters** (Hunt+2024): not run here (the
  hunt_2026 rung found a binary floor ~0.55 km/s and super-virial dispersions, the same size as the clump's 0.2–0.6 km/s
  term; separating them needs its own lane).

## T1 — PRIMARY: globular-cluster σ profiles
**Sample.** Every cluster with ≥ 1 line-of-sight (Type = RV) bin and a parameter row, except NGC 6715 (M54, which sits in the
nucleus of the Sgr dwarf, itself a clump carrier under the hypothesis). Bins with R > rt are dropped.
**Tidal cut (primary = tidally safe only).** V_c(R) from the law with the MW baryons as a point mass (6.0e10 M_⊙, CFG820's
constant), per footing. With the flat-curve Jacobi radius r_J³ = G M R²/(2V_c²), the clump alone gives r_J² + r_c² =
(σ_x R/V_c)². A cluster is **tidally safe** if at an assumed pericentre R_p = R_GC/3 the clump keeps its core:
σ_x R_p / V_c(R_p) ≥ √2 r_c. (Current R_GC only; pericentres are not in the table: disclosed approximation.)
**Model per bin.** Isotropic Jeans, King (1962) tracer truncated at the catalogue rt, with r_c,King solved so the projected
half-light radius equals rh_l (Plummer with a = rh_l if unsolvable; counted). Stellar mass Υ L_V distributed like the tracer.
σ_los²(R) = Υ L_V k_*(R) + k_x(R) (Newton baseline + clump), with k_* and k_x the Jeans projections for unit stellar mass
and for M_x(r).
**Statistic.** ln σ residuals; per-bin ln error from the asymmetric bin errors (upper error when the prediction is above the
datum), with e_lo = ln(σ/max(σ − low, 0.1σ)); a 0.05 floor added in quadrature; Υ_V a nuisance with prior
ln Υ ~ N(ln 1.6, (0.15 ln 10)²) (CFG332/820's SPS value and width), profiled on a grid. χ²_min for B (baseline) and B+X.
- **Diagnostic power:** Asimov Δχ²_A = χ²_min(B+X | data := B at Υ = 1.6, same errors). **Diagnostic iff Δχ²_A ≥ 9.**
- **Real:** Δχ² = χ²_min(B+X) − χ²_min(B).
- **Per-cluster class:** NOT DIAGNOSTIC (Δχ²_A < 9); **NO CLUMP** (diagnostic, Δχ² ≥ +9); **CLUMP PRESENT** (diagnostic,
  Δχ² ≤ −9); UNDECIDED (diagnostic, |Δχ²| < 9); MODEL INADEQUATE (≥ 3 bins and χ²_min/N_bins > 3 for both B and B+X; not
  counted). A CLUMP PRESENT cluster is **binary-vulnerable** if its RV bins hold < 50 stars in total (binaries only inflate
  σ, so they can fake CLUMP PRESENT, never NO CLUMP).
**Overall class (per footing; if the footings differ, both are reported and the weaker one is the headline):**
- NOT DIAGNOSTIC: fewer than 2 diagnostic, adequate clusters.
- **KILLED:** robust CLUMP PRESENT ≥ 1 and ≥ the number of NO CLUMP.
- **MIXED:** robust CLUMP PRESENT ≥ 1 but fewer than NO CLUMP (the clusters are named).
- **PREDICTION HOLDS:** no robust CLUMP PRESENT and NO CLUMP ≥ 2 (binary-vulnerable CLUMP PRESENT listed as caveats;
  "HOLDS (WEAK)" if they number ≥ the NO CLUMPs).
- UNDECIDED: otherwise.
**Reported variants (not deciding):** all R_GC (no tidal cut); all bin types (PM bins read as σ_los under isotropy); floor
0.10; Plummer tracer; law+EFE baseline (σ_*² × ν_e(y_int + g_ext/a0), CFG820's algebraic form, y_int at r12 = 4/3 rh_l).
Also reported per cluster: the clump-only floor (Υ → 0), which is Υ-free.

## T2 — SECONDARY: CFG332's four outer-halo globulars, global σ (Wolf, CFG820's estimator)
σ² = σ_B² + G M_x(<r12)/(3 r12), r12 = 4/3 r_h,l, σ_B = Newton (CFG820 Υ 1.6) and law+EFE (CFG820's B). Same Υ prior,
no floor, the CFG332 error. Same per-system classes (Asimov ≥ 9 etc.). Reported, and must agree in sign with T1 for the
overlapping clusters.

## T3 — non-globular systems: diagnostic power first
- T3a TDGs: V_c at R_out; baseline Newton V_N = √(G M_bar/R_out) (class E); clump V_x² = G M_x(<R_out)/R_out; error
  √(eV² + e_VN²) with e_VN from e_Mbar. Isolated law (no EFE) reported.
- T3b LVD compact objects: Wolf at r12 = 4/3 r_h; Υ_V = 2 (LVD convention) with the 0.15 dex prior; LVD σ errors, or 20 %
  where missing (CFG877's convention, disclosed); Newton baseline, law (no EFE) reported.
- T3c NGC 1052 trail: CFG655's inputs; Newton baseline (label E); clump at r12 = 4/3 R_e; CFG655's σ and M_* errors.
- Same Asimov rule: a system with Δχ²_A < 9 is NOT DIAGNOSTIC and is not scored.

## Controls
- **K1:** T2's Newton σ for CFG332's four clusters reproduces CFG820's printed values (`cfg820.out`) to 0.005 km/s.
- **K1b:** M_x(r → ∞) equals CFG877's M_cl (`cfg877_results.json`) to 1e-9 and the cap radius equals its r_t.
- **K2:** the Jeans code reproduces the analytic self-consistent Plummer σ_los(R) to 1 % at R/a = 0.1, 1, 3.
- **K3:** the King solver returns projected R_h = rh_l to 1 % for every solvable cluster.
- **MUTATE** (`CFG883_MUTATE=1`, separate outputs): every observed σ is replaced by √(σ_obs² + k_x(R)) (each footing's clump
  injected into the data, errors kept proportional). Required: ≥ 80 % of T1's diagnostic clusters read CLUMP PRESENT and the
  T1 overall class is KILLED on both footings. T3 systems must stay NOT DIAGNOSTIC (their power does not depend on the data).

## Pre-freeze disclosures
- **Hand estimates made before freezing (Wolf form, Υ 1.6, canonical):** Pal 14 Newton 0.60, clump term 2.05, total 2.14
  against σ_obs 0.71 ± 0.16; Pal 4 1.00 / 1.22 / 1.58 against 0.88 ± 0.19; **Pal 3 0.74 / 1.54 / 1.71 against 1.70 ± 0.34**
  (the clump would explain Pal 3's known excess, which CFG334 also explains with ordinary binaries); NGC 2419 4.67 / 1.52 /
  4.91 against 4.77 ± 0.48 (not diagnostic). TDGs, UCDs and the NGC 1052 trail were estimated as far from diagnostic. The
  rules above were written after these estimates; Pal 3 is kept in the sample with the binary flag instead of excluded.
- **Weak novelty for globulars:** that globulars need no dark component is long known and already in the record (CFG332,
  CFG820). A NO CLUMP result is what the hypothesis needs but does not single out the first-cooling story; the test bites
  only if a clump IS found.
- Stripped nuclei (e.g. ω Cen, NGC 2419) could in principle keep the inner part of a host dwarf's clump; they are massive and
  the Asimov rule decides whether they say anything.
- Isotropy, King tracer shape and escapers near rt are model systematics (floor 0.05; variant 0.10).
