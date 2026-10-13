# CFG721: SUPPLY OVERFLOW (H-OF) for the extra core mass in massive systems. FROZEN CRITERIA

Committed alone, before any script of this lane exists and before any target comparison is computed. Date 2026-10-13.
Lane number: CFG720 is taken (merger-stopwatch lane, criteria 7687ef48c); CFG721 is the next free number in the owner chat's
reserved block CFG720–729 (no directory, no commit, no LEDGER row carried it).

**Settings.** κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. Kernels ν_mono (CFG4_common)
and CFG695's ν_s(y) = ½ + √(¼ + 1/y), never pooled. "Cold energy" throughout; its mass is still required; no particle species.
Not "theory closed". No ΛCDM halo, mass function or standard-MOND yardstick enters any verdict.

## 0. Status of this test: POST-HOC, every target already seen

Every data target below has already been measured and read in the record (CFG669, CFG658, CFG652, CFG687, CFG686, CFG637, CFG656,
SPARC). This lane is a **post-hoc mechanism test**: it asks whether one framework-derived mechanism with no new constant
reproduces numbers that motivated it. A pass would be an accommodation, not a prediction.

Prior expectations, disclosed before computing:
- H-OF with the **all-baryon** source is CFG637's candidate-B derivation. CFG637 and CFG656 found its reservoir EMPTY in galaxies,
  groups and all 12 X-COP clusters, for every supply up to ×29. If that holds here, H-OF(all) has no overflow at any target mass,
  M_b,OF lies above every target, and H-OF(all) reduces to the plain law with the phantom cut at the supply edge.
- H-OF with the **condensed** source is CFG637's H-CB / CFG652's "Theory v2 (a)". CFG652 already scored it on eFEDS (BOTH
  EXCLUDED, χ² p 0.0035 / 0.0043) and CFG637 on X-COP (headline FAIL, inner band PASS). A benchmark run while writing these criteria
  (cfg652_model.system, one group-like and two cluster-like systems, canonical) gave condensed-source reservoir/supply 0.58–0.79
  and all-baryon 0.000. That is a derivation number, not a target comparison.
- KiDS early/late is a ratio at MATCHED baryonic mass. A mass-threshold mechanism can only produce it if early and late types of
  the same M_b sit on different sides of the threshold.

## 1. The derivation (zero new constants)

Machinery: CFG637 Method A (`cfg637_lib.derive`, unchanged), wrapped exactly as CFG652's `cfg652_model.system` (catchment rule,
supply, f_ret, M_ta, gate-unit rescale), with only the baryon profiles and the kernel passed in.
- **Supply** = 5.364 × catchment baryons. Catchment = max(M_cond/0.10, (M_cond + M_hot,tot)/0.90) (CFG652's one rule spanning
  CFG543 P2 and CFG634/637 X-COP); f_ret = (M_cond + M_hot,tot)/catchment; M_ta = catchment/f_b.
- **Settled phantom** = the law's round phantom of the SOURCE, cut at the supply edge (R2), confined to r_ta.
  Sources: **all** (all retained baryons) and **cond** (condensed baryons only). Both are reported; never pooled.
- **Overflow** = the Method A reservoir: supply − settled, collisionless, placed by infall in the total potential.
- **H-OF lensing mass** M_HOF(<r) = baryons(<r) + settled(<r) + overflow(<r) (overflow and settled from Method A, confined to r_ta).

**D1 threshold ladder.** M_b = 10^9 … 10^15 in 0.5-dex steps (13 points); condensed fraction f_cond ∈ {1, 0.5, 0.25, 0.1, 0.05}
for the cond source and {1, 0.1} for the all source; both kernels, both footings; z = 0 (primary) and z = 0.3 (reported).
Profiles: CFG652's family (condensed: half Hernquist R_e 15 kpc, half Hernquist R_e 0.5 R_X; hot gas β = 2/3, r_c = 0.234 R_X, to
2 R_X), with R_X from the eRASS1 catalogue's own Mgas500–R500 power law fitted on the 318 CFG687 clusters (aperture convention
only), evaluated at M_hot (or at M_b when f_cond = 1). N = 600 shells.
**M_b,OF(f_cond)** = the lowest M_b at which reservoir/supply ≥ 0.01, log-interpolated between ladder points; "> 10^15" if never.
Also reported: the analytic deep-regime capacity √(M_src a₀/G)·r_ta / supply at each ladder point.

## 2. Targets, statistics and pass rules (per source × kernel × footing)

**T-K KiDS f30 early/late at matched Ks M_b (CFG669 T2: +0.280 ± 0.083).** Prediction = CFG658's law value −0.027 (same for both
kernels and both footings) + Δ_OF, where Δ_OF = log10[ΔΣ_HOF,early/ΔΣ_HOF,late] − log10[ΔΣ_law,early/ΔΣ_law,late] at 50–100 kpc,
averaged over the ladder masses 10^10, 10^10.5, 10^11, 10^11.5 (the lens range), early = f_cond 0.5 (a hot halo equal to the
condensed mass: the most favourable bracket for an early-type overflow), late = f_cond 1. If the reservoir is empty in both, Δ_OF = 0
exactly. **PASS** iff |prediction − 0.280| < 2 × 0.083.

**T-E eFEDS 131 groups (CFG652).** CFG652's staged inputs, stack and score code (30-patch jackknife covariance, Hartlap, 8 bins
53–783 kpc, outer band 248–783 kpc); per-group H-OF ΔΣ from M_HOF truncated at r_ta (CFG652's delta_sigma), gas to 2 R_X, M_cond
as frozen. **PASS** iff χ² p ≥ 0.01 AND |A_out| < 2 σ_A (A_out in dex).

**T-R eRASS1 318 clusters (CFG687).** CFG687's measured per-cluster ΔΣ, errors and weights (cfg687_percluster.npz), its band
definitions and its 30-patch RA jackknife. Baryons = CFG687's primary bracket (gas β = 2/3, r_c 0.15 R500, to 3 Mpc, normalised to
Mgas500; stars f* = 0.20 co-distributed); condensed = the stars; hot = the gas. H-OF ΔΣ from M_HOF projected with CFG686/687's own
projection (RGRID, sigma_proj, M2D). A = Σ W D / Σ W P per band.
**PASS** iff |A_MID − 1| < 2σ AND |A_OUTER − 1| < 2σ.
**T-R2 (the M_gas^0.90 question, reported, not in the pass rule).** CFG687's tercile slope s on the H-OF predictions. H-OF
"explains" the observed s = 0.90 ± 0.21 iff |0.90 − s_HOF| < 2 × 0.21 AND s_HOF − s_law ≥ 0.21 (it must move the slope away from the
law's 0.47, not merely sit within 2σ as the law nearly does).
Reported bracket (not in the verdict): condensed placed as CFG652's BCG + members instead of co-distributed (canonical, ν_mono).

**T-A ACCEPT 8 clusters (CFG686).** CFG686's per-cluster measured ΔΣ and errors (cfg686_results.json), its gas construction from
ACCEPT n_e (copied verbatim), primary bracket (β_out fit, f* 0.20), bootstrap over clusters (1000, seed 1).
**PASS** iff |A_MID − 1| < 2σ AND |A_OUTER − 1| < 2σ.

**T-X X-COP (CFG637/656).** H-OF(cond) is CFG637's H-CB derived reservoir (stars as source, Method A); H-OF(all) is CFG637's
candidate B. The committed CFG637 numbers (ν_mono, old supply convention) and CFG656 numbers (native supply) ARE H-OF's X-COP score;
this lane does not re-run X-COP. Rule: CFG637's frozen T3 rule on the headline η (1000 kpc) for the old supply. ν_s is NOT scored on
X-COP here (disclosed; the cell is "not run", which cannot count as a pass).

**T-S SPARC (must stay at 0.100 dex).** Guard: for every ladder point with M_b ≤ 10^12 and f_cond = 1, both sources, both kernels,
both footings: reservoir/supply = 0 AND supply-edge radius > 108.3 kpc (the largest last measured radius among the 175 SPARC rotmod
files). If the guard holds, H-OF changes no SPARC rotation-curve point and the RAR scatter change is exactly 0 → **PASS**
(|Δ| ≤ 0.005 dex). If it fails anywhere, T-S = FAIL (not verified).

**Verdict per (source, kernel).** H-OF PASSES iff T-K, T-E, T-R, T-A, T-X and T-S all pass on BOTH footings. Otherwise
"H-OF FAILS" with the failing targets listed. A cell that is not run (T-X ν_s) blocks a PASS.

## 3. MUTATE and controls

- **M0 (supply ×0 for the overflow part ⇒ the plain law).** Overflow set to 0 and the phantom of all baryons left uncut
  (infinite capacity): this lane's projection must reproduce CFG687's stored law prediction (PL, canonical primary) to ≤ 1% per
  bin (median over clusters, and the band A values to ≤ 0.01), and CFG686's stored canonical/alt primary predictions to ≤ 1%.
  For eFEDS: re-running cfg652_model.system with CFG652's own kernel (C540.nu) must reproduce cfg652_models.npz (canonical x1, both
  models) to ≤ 1% for every group. Failing M0 voids the lane.
- **M-SHUF (threshold shuffled across masses).** eRASS1: the per-cluster overflow fraction (reservoir/supply) is permuted across
  clusters (seed 721) and T-R2's slope recomputed. **Bites** iff the H-OF slope moves by ≥ 0.5 |s_HOF − s_law|. If the unshuffled
  overflow fraction carries no mass trend (|s_HOF − s_law| < 0.05), M-SHUF is reported "NOT APPLICABLE: no threshold inside the
  sample". Ladder: the same permutation of reservoir/supply across ladder masses must destroy the monotone onset (reported).
- **C1** supply = settled + reservoir to 1e-9 in every run (inherited check).

## 4. What would change the reading

Nothing in this lane is a prediction. A full pass would make H-OF a candidate needing a forward test (e.g. pre-registered stacks at
masses straddling the derived M_b,OF). A fail is scoped by source: the all-baryon fail would be CFG637's mechanism (the phantom
eats the supply out to r_ta), the condensed fail would be CFG652's (core overshoot / outer shortfall).

κ fitted; cold energy mass required; not theory closed.
