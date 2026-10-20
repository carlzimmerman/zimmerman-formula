# CFG914 FROZEN CRITERIA: one common density threshold for the law's open excesses?

Reservation: orchestrator block CFG910–919 (LEDGER row "CFG910–919 RESERVED", CFG914 = "common density threshold across dwarfs,
spheroids, cluster cores"). This file is committed ALONE, before any script exists and before any density is computed.
κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10 m/s², never pooled; raw data and framework-native mass models only (no ΛCDM halo
profiles); no dark-matter particle; not theory closed.

## Hypothesis under test
The law's three open failures, (i) faint dwarfs above the law (CFG828/880/890), (ii) red / spheroidal isolated lenses above the
law (CFG829/850/851/885/912), (iii) cluster cores above the law (CFG686/687), are ONE phenomenon: extra cold mass retained where
matter is DENSE. Diffuse systems (SPARC rotators, blue lenses, cluster outskirts) follow the law. Prediction: across all
sectors the excess over the law orders by one common local density variable, with a threshold ρ*: excess ≈ 0 below ρ*,
positive above, in every sector. Globulars are dense and (CFG883) carry no excess over their Newtonian (class-E) baseline;
they are a PRE-DECLARED TEST sector, not an exclusion.

## Common quantities (identical definition in every sector)
- **Excess** E ≡ ln(g_obs / g_law) at the measurement radius r, i.e. ln of observed over law-predicted enclosed dynamical mass.
  Dwarfs: E = 2 ln(σ_obs/σ_law). Lensing / clusters: E = ln A, A = observed over law-predicted signal (each source lane's
  estimator). E > 0 means extra mass.
- **PRIMARY density** ρ̄_law(<r) ≡ 3 g_law(r) / (4π G r): the mean TOTAL density inside the measurement radius from the law's own
  mass model (baryons + the law's cold energy), in M☉/pc³. It does not contain the observed excess, so it is not circular.
- **GRADED VARIANT V1** ρ̄_b(<r) ≡ 3 g_bar(r) / (4π G r): the mean baryonic density inside r.
- g_bar, g_law, r are each sector's own (source-lane) values. For discs and projected (lensing/cluster) radii the
  spherical-equivalent form 3g/(4πGr) with r = the measurement radius is used as defined; this is declared, not a physical
  claim that the systems are spheres.

## Sectors (7 graded) and how each gives (log ρ, E) points with covariance
Each sector keeps its source lane's law kernel and baryon model (so the K-tests reproduce exactly). Footings are run separately.
1. **DW dwarfs** (failing): CFG880's 83 LVD dwarfs (sample, Υ_V = 2, gas inside r12 per CFG874, r12 = (4/3) r_h, ν_e, no EFE).
   σ_law recomputed with CFG880's code; g_bar = G M_b12/r12² with M_b12 = M*/2 + M_gas(<r12); g_law = 3σ_law²/r12.
   Per-dwarf σ_E = 2 e/σ_obs with e the error on the side toward the law. Binning: 8 equal-count bins in log ρ (np.array_split
   of the sorted order). Bin value = unweighted mean E; SE = max(std(ddof=1)/√n, √(Σσ_E²)/n). Bins independent.
2. **SS SPARC small rotators** (diffuse control) and 3. **SL SPARC large rotators** (diffuse control): CFG828's point selection
   (Q ≤ 2, i ≥ 30°, e_V/V < 0.10, Υ_disk 0.5, Υ_bul 0.7, g_bar > 0, ν_e); small/large split at CFG870's M_b = 0.5 L[3.6] +
   1.33 M_HI ≤ 3e9 M☉. Each RC point: E = ln(g_obs/g_law), ρ from its own g at its R. Fixed 0.5-dex grid in log ρ (edges at
   integer and half-integer values). Bin value = mean over galaxies of each galaxy's mean E in the bin; bin ≥ 5 galaxies.
   Covariance across bins: galaxy bootstrap, 1000 resamples, seed 914 (pairwise, ignoring empty draws).
4. **LR red lenses** (failing) and 5. **LB blue lenses** (diffuse control): B21 Fig-8 colour bins, read with CFG829's `load`
   (exec'd read-only); red with CFG850's primary M★ shift +0.123 dex on g_bar (blue unshifted); ν_e. Points with shifted
   g_bar in [10^−13.3, 10^−10.9) m/s² (CFG829 window + calibration window). Radius per point R = √(G M_l / g_bar) with M_l =
   the median lens baryonic mass of the record's B21 reconstruction (cfg912_colour.out: log M_gal red(2.0) 10.81, blue(2.0)
   10.45; red + 0.123 under the shift). Fixed 0.5-dex grid; per bin the full-covariance amplitude A_b over the points in the
   bin (CFG829's estimator restricted to the bin); Cov(A_b, A_c) = w_bᵀ C w_c; E = ln A, Cov_E = Cov_A/(A_b A_c). A bin is
   dropped if A_b ≤ 0 or σ_A/A_b > 1.
6. **CL eRASS1 clusters** (failing): CFG687's 318 clusters, per-cluster arrays `cfg687_percluster.npz` (observed ΔΣ, errors,
   law prediction at canonical, primary bracket β 2/3, r_c 0.15 R500, f* 0.20, ν_mono). The law prediction and mass profile are
   recomputed with CFG687's `law()` (copied, same constants and grid) for both footings. Radius bins j = 3..7 (MID 0.5–1.2 Mpc +
   OUTER 1.2–3 Mpc; INNER not used, as in CFG686/687). Each (cluster, j) pair gets ρ from M_L(<R_j) (resp. M_b(<R_j)) of its
   own law profile at r = R_j. Fixed 0.5-dex grid over pairs; bin amplitude A = Σ W D / Σ W P (W = 1/err², CFG687's estimator);
   bin needs ≥ 20 distinct clusters and Σ W P > 0. Covariance across bins: CFG687's 30-patch RA jackknife.
7. **GC globulars** (pre-declared test): CFG883's primary T1 rows (RV bins inside r_t, Baumgardt data), each footing's
   tidally safe set (31). Baseline = the record's class-E Newton law for globulars, Υ_V fixed at the SPS 1.6 (CFG883's `s_B`).
   Measurement radius = the outermost RV bin R_out; E = 2 ln(σ_obs/σ_B) there; σ_E² = (2 √(e_ln² + 0.05²))² + (0.15 ln 10)²
   (CFG883's ln error toward the model, 5% floor, Υ prior width). ρ̄ from M(<R_out) = 1.6 L_V × the King (or Plummer fallback)
   tracer's enclosed fraction at r = R_out (CFG883's tracer, exec'd read-only); class E ⇒ ρ̄_law = ρ̄_b. Binning: 5 equal-count
   bins; bin value and SE as for DW.

**Systematic floor:** σ_floor = 0.05 dex in g (= 0.1151 in E), the law's calibration tolerance (CFG828 K1). It is added fully
correlated within each sector (σ_floor² added to every element of the sector's covariance) for the sector tests, and to the
diagonal (SE² + σ_floor²) for the fit weights. Each bin's representative log ρ is the mean log ρ of its members (SPARC:
galaxy-weighted; lensing: amplitude-weighted; clusters: W·P-weighted).

## The test (per footing, per density variable)
- **Common monotone-threshold model (generous form):** f(ρ) = 0 for ρ < ρ*, f non-decreasing and ≥ 0 above (weighted
  isotonic regression by pool-adjacent-violators, weights 1/(SE² + σ_floor²), clipped at 0). ρ* candidates: midpoints between
  consecutive sorted bin densities, plus below-all and above-all. Choose the candidate with minimum diagonal χ² (ties → lower
  ρ*). The effective threshold ρ*_eff = midpoint between the last bin with f = 0 and the first with f > 0.
- **Per-sector test:** χ²_s = rᵀ C_s⁻¹ r with r = E_sb − f(ρ_sb) and C_s the sector covariance incl. the correlated floor;
  p_s = χ²-survival with n_s (number of the sector's bins) degrees of freedom (no parameter subtraction: generous);
  z_s = one-sided Gaussian equivalent. **A sector violates if z_s > 2.**
- **Valid threshold:** ≥ 1 bin below ρ*_eff and ≥ 1 above in the set being fit; and the excess above ρ*_eff is positive at
  ≥ 3σ (diagonal-weighted mean of the bins above / its SE).
- **Greedy subset:** if any sector violates, drop the sector with the largest z_s, refit on the rest, repeat until no
  remaining sector violates (or < 2 sectors remain). The dropped sectors, in order, are the named violators.

## Classes (headline = PRIMARY density ρ̄_law, canonical footing)
- **COMMON THRESHOLD:** the all-sector fit has a valid threshold and NO sector violates (globulars included).
- **PARTIAL:** not the above, but the greedy survivors contain ≥ 2 of the failing sectors {DW, LR, CL} and ≥ 1 diffuse control
  {SS, SL, LB}, and their fit has a valid threshold. Violators are named.
- **NO COMMON ORDERING:** otherwise.
- The alt footing and V1 (ρ̄_b) are classified identically. If alt differs, the headline carries "(footing-dependent)"; if V1
  differs, "(density-variable dependent)".

## Reported (not graded)
- Strict step model f = E_hi H(ρ − ρ*) (one common level): ρ*, E_hi, per-sector z_s.
- Pooled Spearman of (log ρ, E) over all graded bins, permutation p (10,000, seed 914); within-sector GLS slope dE/dlog ρ
  (sectors with ≥ 3 bins) and its z; the mirrored "inverted" fit (excess only BELOW a threshold) and its violators.
- Variants: R1 g_bar as the ordering variable; R2 ρ̄_obs = 3 g_obs/(4πGr) (CIRCULAR: contains E; flagged); R3 floor 0 and
  0.1 dex; R4 lens masses ± 0.3 dex; R5 red lenses without the M★ shift; R6 globulars with ≥ 50 RV stars only; R7 globulars
  against CFG883's law+EFE baseline (ρ̄_law then carries that ν); R8 cluster INNER band included.
- Plots as tables: every sector's bins (log ρ, E ± σ, n, f, residual) and every per-system row (83 dwarfs, 31 globulars) in
  the output / JSON.
- **Framework scales (post hoc, stated as such):** ρ*_eff (all-sector and survivors' fits) against ρ_crit(h = 0.70) =
  3H0²/(8πG); ρ_DE ≡ a0²/(κ² G c²) = 4a0²/(Gc²) (κ = ½ fitted); ρ_a0(L) = 3a0/(4πG L) for L = 104 pc (CFG870 core), 1 kpc and
  100 kpc; CFG870's clump central density ≈ 0.6 M☉/pc³. Any match is post hoc and is not a result.

## Controls
- **K1 dwarfs:** recomputed σ_law = CFG880's committed `law` for all 83 dwarfs, both footings; CFG880's `pred_univ`
  reproduced from its committed σ̄_univ (tests r12, gas, clump code). Tolerance ≤ 1e-9 relative.
- **K2 SPARC:** CFG828's n_sparc and SPARC overall median (canonical and alt, ν_e); CFG870's sparc_D and its bootstrap σ with
  the committed V_x (both footings). ≤ 1e-9.
- **K3 lensing:** CFG850's canonical/alt (+0.123, 0) rows (A_red, A_blue, z_colour) and CFG829's blue canonical window A.
  ≤ 1e-9. Lens medians parsed from cfg912_colour.out (10.81 / 10.45).
- **K4 clusters:** recomputed canonical law prediction = the npz `PL` (≤ 1e-9 relative, all 318 × 8); CFG687's primary
  A (INNER, MID, OUTER; value and jackknife σ) on both footings from the npz + recomputed predictions. ≤ 1e-9.
- **K5 globulars:** CFG883's primary rows reproduced for the tidally safe set: R_pc, s_obs and s_B (≤ 1e-9); 31 safe per footing.
- **MUTATE-SHUFFLE (null):** within each sector, densities are permuted among its systems / points / pairs / B21 points (seeded);
  re-binned and re-tested. 200 realisations. Pre-declared pass: for every sector with ≥ 3 bins, the fraction of shuffles with
  |z_slope| ≥ 2 is ≤ 0.15 (the within-sector ordering disappears). Cross-sector ordering is NOT expected to vanish (sector
  density ranges are preserved by a within-sector shuffle); reported. One representative realisation is classified.
- **MUTATE-INJECT (power):** each sector's bin values are replaced by f_inj(ρ_b) + a draw from that sector's full covariance
  (incl. the correlated floor), with f_inj = 0.7 H(log ρ − log ρ*_inj), log ρ*_inj = the median log ρ of all graded bins
  (per footing and variable), seed 914. Pre-declared pass: COMMON THRESHOLD on both footings for the primary and V1, with the
  recovered log ρ*_eff within 0.5 dex of the injected value.
- MUTATE modes write separate outputs (`CFG914_MUTATE=shuffle|inject`).

## Disclosures fixed now
- **Not blind.** Every sector's excess was already known from the source lanes (dwarfs +0.44 dex; red lenses ×1.45; cluster
  MID ×1.9; SPARC flat; blue lenses on the law; globulars Newtonian). No density was computed before this file was committed.
  While designing the bins I made order-of-magnitude hand estimates (not from the data files) of ρ̄_law: dwarfs ~1e-3–1e-1,
  SPARC ~1e-4–1, lenses ~1e-5–1e-3, cluster MID/OUTER ~1e-5–1e-4, globulars ≳ 0.1 M☉/pc³. They suggest SPARC overlaps the
  dwarfs in density, so a fail was anticipated as plausible; the classes above do not depend on that estimate.
- Each sector keeps its source lane's kernel (ν_e for galaxies / dwarfs / lenses, ν_mono for clusters, class-E Newton for
  globulars) and baryon model; the "law" is therefore the record's law per sector, not one formula re-derived here.
- No EFE for dwarfs (as CFG880); stacked lensing points carry the median lens mass only (the spread of lens masses spreads ρ by
  ≈ ½ of it in dex; R4 brackets it); 3D radius taken equal to the projected radius for lensing and clusters.
- Compute: one core (OMP_NUM_THREADS=1, nice 10), one process < 1 GB, no downloads, beside the live 1024³ run.
