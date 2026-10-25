# X42_core_rise_above_galaxies — FROZEN CRITERIA (committed alone, before any script or number of this lane)

Lane id: X42 (X41 is taken by `X41_collapse_floor_sigma`, 0ea05957ee, a first-principles collapse floor with no fitted
amplitude; this lane is independent of it and does not edit it).

**Question.** X38 (route E, Burkert cold dark energy cores at ρ₀r₀ = Σ_a₀ ≡ a₀/(2πG)) passes SPARC and the cluster OUTER
band but under-predicts heavy cluster cores and the groups line (P4 T3, Z +2.48 / +2.29). X40b (b09db13390 / ba368d2ba1)
found no framework-native rule (max(a₀, g_b), a₀(z_f)) that switches on, and that with galaxies pinned the clusters need
S ∝ M^α, α ≈ 0.25–0.30 above the pivot 2.93e12 M☉ (cluster cores 3–5 × Σ_a₀). **Does either of two physically motivated
rules produce the core rise above galaxy scale without a constant tuned to the graded data, keeping SPARC and passing groups
and clusters?**

Standing rules: κ = ½ FITTED. Footings (canonical a₀ 9.3603e-11, alt 1.1312e-10 m s⁻²) never pooled. Route E: gravity
Newtonian on baryons + cold dark energy, the law emergent. Cold dark energy is a gravitating field component, not matter and
not a particle. Not "theory closed". Nothing here may say the data favour the framework.

## 0. Step 0 (stop rule)

X40b's committed script is copied to a scratch directory (only its output directory redirected; inputs read from the record)
and rerun. Its graded numbers must equal the committed `x40b_sd_scaling_results.json` to 1e-6: per footing and rule (A, A′, B)
the SPARC rms and median Υ on both backgrounds, every cluster key's pred in both h cells, the groups mean and Z (X38 baseline
and each rule), and (C)'s α_best and χ² scan. In particular the groups failure (Z +2.48 / +2.29) and α_best 0.30 / 0.25 must
reappear. **If not, the lane stops** and reports the mismatch.

## 1. The halo (common)

Exactly X38 + A1 as executed by X40b: Burkert, Σ ≡ ρ₀r₀ = s · Σ_a₀, s ≥ 1 set by the hypothesis, compact root, SATURATED
counted. Galaxies: M200 from EM1's committed relation (A 11.18 / 0.90, B 11.20 / 0.90), R200 at 200 ρ_c(0). Clusters: X30's
machinery read-only, M_h(<r_ta) = M_fair = 5.364 M_b. Groups: P4 T3's estimator with X40b's halo (EM1 relation on background
A, extrapolated, truncated at R200). Gravity Newtonian on M_b + M_h. The machinery is X40b's code executed read-only (only its
output paths redirected into this lane); the rule dispatch is replaced by H1 / H2 below.

Halo mass M used by H1 (as X40b's (C)): SPARC and groups M200; clusters M_fair.

## 2. H1 — the self-similar collapse floor (one amplitude, calibrated on clusters only)

    Σ_core = max(Σ_a₀, Σ_ss(M)),   Σ_ss(M) = Σ_a₀ (M / M_x)^{1/3}   ⇔   s = max(1, (M/M_x)^{1/3})

- Σ_ss ∝ M^{1/3}: fixed density contrast, standard collapse (ρ r at fixed contrast ∝ R ∝ M^{1/3}).
- **The single amplitude** is the crossover mass M_x (equivalently Σ_ss(10¹⁴ M☉) in M☉ pc⁻², reported).
- **Calibration set: the CLUSTERS ONLY, MID terciles.** χ²_cal = Σ_{t=1..3} Z(G-MID-Tt, h 0.672)². Minimised over
  log₁₀ M_x ∈ [8, 16]: 0.1-dex grid, then bounded Brent inside the best grid bracket to 1e-4 dex. Per footing.
- **Out of sample:** SPARC (both backgrounds) and the groups line are graded with that M_x and nothing refit. The other 12
  cluster keys (and MID T1–T3 themselves) are also graded; MID terciles are in-sample and disclosed as such. χ²_cal and the
  15-key χ² (h 0.672) are reported.
- **α free (reported, part of the H1 report):** s = max(1, (M/M_x)^α), (α, M_x) both on χ²_cal. α on the grid 0.00, 0.05, …,
  1.00 plus 1/3, M_x profiled (same minimiser) at each α. **α = 1/3 is ALLOWED iff χ²_cal(1/3) − min_α χ²_cal(α) ≤ 4.0.**
  Reported: α_best, the α-grid interval with Δχ² ≤ 4, M_x at each. α = 0 is X38 by construction.

## 3. H2 — the baryon-retention rule (no constant beyond the galaxy-median normalisation)

    Σ_core = Σ_a₀ · max(1, f_b,sys / f_b,gal)   ⇔   s = max(1, f_b,sys / f_b,gal)

- **f_b,sys ≡ M_b(<R200) / [M_b(<R200) + M_h(<R200)]**, using the record's inputs and the X38 baseline halo (s ≡ 1; no
  iteration, disclosed). R200: radius where the mean total (baryons + cold dark energy) density = 200 ρ_c(0), ρ_c with
  background A's h (background B's h for background-B SPARC rows).
  - SPARC: M_b = 10^lMb (EM1's input, the same M_b that sets M200), all inside R200; M_h(<R200) = M200 (X38 normalisation),
    so f_b = M_b/(M_b + M200), footing-independent.
  - Groups: catalogue M_bar, M200 from EM1's relation on background A: f_b = M_bar/(M_bar + M200).
  - Clusters: X30's M_b (β-gas × 1.2: gas + stars) and X38's s = 1 halo (per footing, per h cell); R200 solved on X30's
    radial grid (if none inside the grid: r_ta, counted and reported). The CFG922 BCG is not added (X40b: 0.5–1.7 % of the
    core baryons; disclosed).
- **f_b,gal = the median f_b over SPARC, background A**, one number used everywhere (both footings, both backgrounds).
  Galaxies at or below the median have s = 1 exactly; those above get s = f_b/f_b,gal (graded, not hidden).
- **Within-SPARC f_b trend check (T-fb, verdict-bearing for H2):** per galaxy (background A), the W-weighted mean signed
  residual ⟨log g_obs − log g_pred⟩ over its OK points at its chosen Υ, under H2's own halos. Spearman ρ against log f_b.
  **STRONG TREND iff |ρ| ≥ 0.30 AND p < 0.01** (scipy two-sided); a strong trend contradicts H2. The same statistic under
  X38 (s ≡ 1) is reported. Disclosed: within SPARC, f_b is a monotone function of lMb through EM1's relation, so T-fb tests
  a trend with baryonic mass as much as with f_b.
- Everything is graded for H2 (no calibration set).
- Reported variant (no weight): clusters' f_b at r_ta (= 1/6.364 by construction) instead of R200; groups fair-share
  (f_b = 1/6.364, M200 = 5.364 M_bar).

## 4. Reported only — ΛCDM-like concentration–mass comparison curve (PROVISIONAL)

NFW surface density S_cM(M) ∝ ρ_s r_s = M200 c² / [4π R200² m(c)], m(c) = ln(1 + c) − c/(1 + c), with Dutton & Macciò
(2014) z = 0 c200: log₁₀ c = 0.905 − 0.101 log₁₀(M h / 10¹² M☉), h = 0.672. **PROVISIONAL**: quoted from the literature, not
transcribed in the record, no download. Reported: the local slope d ln S_cM / d ln M at 10¹¹ … 10¹⁵ M☉ and S_cM(10¹⁵)/S_cM(M_piv).
Reported-only variant "H1-cM": s = max(1, S_cM(M)/S_cM(M_x)) calibrated exactly as H1 and graded the same way; never a verdict.

## 5. Graded lines (each hypothesis, each footing; never pooled)

- **SPARC:** EM1's line, rms ≤ 0.110 AND median Υ ∈ [0.50, 0.80], on both backgrounds A and B (X38's line).
- **Groups:** Tian+2026 BFJR, 63 "Galaxy group" rows, P4 T3's statistic exactly as X40b used it (class mean, SE,
  σ_sys = s̄ × 0.10 dex); PASS iff CONSISTENT (|Z| < 2 and σ_tot ≤ 0.045).
- **Clusters:** X38's 15 keys with X38 / X40b grading code: G-MID-T1..T3, G-MID-b (MID KT slope), G-OUT-all, G-OUT-T1..T3,
  G-OUT-b, G-IN-all, G-OUT-Mall, G-OUT-M1..M3 (MGAS bands), G-IN-Mall; |Z| ≤ 2 in both h cells (0.672, 0.686).

## 6. Verdict classes (each needs both footings)

A hypothesis PASSES on a footing iff SPARC passes on both backgrounds AND the groups line PASSES AND every cluster key passes
in both h cells (H2 additionally: T-fb not STRONG).

- **H1 PASSES OUT OF SAMPLE** — H1 passes on both footings (its amplitude calibrated on cluster MID terciles only).
- **H2 PASSES** — H2 passes on both footings. (Both labels are reported if both pass.)
- **BOTH FAIL (name where)** — neither passes on either footing; each failing line / key is listed with its direction
  (UNDER / OVER for clusters, ABOVE / BELOW for groups).
- **UNDECIDED** — no hypothesis passes on both footings but one passes on one footing.

Reported per hypothesis: s medians (SPARC, groups, clusters by KT tercile), frac SPARC with s > 1, SATURATED counts, cluster
r₀ by tercile, f_b medians (H2).

## 7. Checks (all must pass in the normal run)

- **K0:** with s ≡ 1 this lane's code reproduces X38's committed SPARC rms / median Υ and every cluster pred (both h cells)
  to 1e-6, and X40b's X38-baseline groups mean to 1e-9.
- **K1:** Step 0 passed (§0).
- **K2 (H1 rises with mass, floor):** at the calibrated M_x every graded H1 halo has s ≥ 1, s = 1 exactly for M ≤ M_x, and
  median s(KT T3) > median s(KT T1) in the clusters (h 0.672), both footings.
- **K3 (H2 floor):** every SPARC galaxy with f_b ≤ f_b,gal has s = 1 exactly (both backgrounds), and the cluster median s > 1.
- **K4:** X40b's groups integrator with no halo equals P4's `group_logsig` (ν ≡ 1) to 1e-4 dex on 63 rows; the R200 solver
  returns mean density 200 ρ_c to 1e-8 on a test halo.
- **K5:** peak RSS < 1 GB, one thread, PYTHONHASHSEED=0, `nice -n 15`.

## 8. MUTATE

`X42_MUTATE=1`: H1's exponent 1/3 → 0 (s ≡ 1: collapses to X38) and H2's ratio inverted (s = max(1, f_b,gal / f_b,sys)).
Outputs go to `_MUTATE` files. **K2 and K3 must both FAIL** (exit 1). The MUTATE numbers are reported, never used.
