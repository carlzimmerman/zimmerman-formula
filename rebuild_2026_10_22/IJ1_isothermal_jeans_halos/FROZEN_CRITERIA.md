# IJ1_isothermal_jeans_halos — FROZEN CRITERIA (committed alone, with the assumption ledger, before any graded number)

Written 2026-10-26. κ = ½ FITTED. Footings canonical / alt, computed and graded separately, never pooled. Cold dark energy
(a self-coupled field component, not matter, never a particle). Nothing here says the data favour the framework or ΛCDM.
Not "theory closed". Light compute: one thread, < 1 GB, nothing downloaded.

Before freezing, the solver was prototyped on synthetic NFW + exponential-disc halos only (scratch, outside the repo). No
SPARC, cluster, group, SLUGGS or dwarf number has been computed.

## 0. Hypothesis IJ (the isothermal-Jeans halo of a self-coupled cold dark energy)

The fixed Burkert core of X38 / OS1 is replaced by the standard isothermal-Jeans construction.

- **Outside r₁:** the record's collisionless route-E halo, an NFW profile with:
  - log M200 = a + b (log M_b − 10), from EM1's R1 rows (background A: 11.18 / 0.90; background B: 11.20 / 0.90);
  - c200 = EM1's Bullock+01 c(M200, z) on that background's CLASS P(k) (K = 4, F = 0.01; `cB` in `em1_emergent.py`,
    executed read-only up to its halo-profile block);
  - R200 at 200 ρ_c(z) of the same background.
- **Inside r₁:** the cold dark energy is isothermal with one-dimensional dispersion σ₀ in the TOTAL potential (its own
  mass plus baryons):

      d ln ρ/dr = −G [M(r) + M_b(r)] / (σ₀² r²),   dM/dr = 4π r² ρ,   ρ(0) = ρ₀, M(0) = 0.

- **Interaction radius r₁:** ρ_NFW(r₁) · s(v) · v · t = 1, with t = 13.8 Gyr for every system and v = (4/√π) σ₀.
- **Matching:** ρ_iso(r₁) = ρ_NFW(r₁) and M_iso(r₁) = M_NFW(r₁). These two conditions fix (ρ₀, σ₀) per system. The halo
  is M_iso(r) for r < r₁ and M_NFW(r) for r ≥ r₁; enclosed mass is continuous at r₁ by construction.
- **Branch rule (frozen).** The isothermal-Jeans problem can have more than one solution. The solution used is:
  1. the lowest-ρ₀ root of the no-baryon problem (exact Lane–Emden; for fixed σ₀ the cored member is the first rising
     branch of h(ξ) = e^ψ ψ′/ξ, then a 1-D root in σ₀ on a log grid 0.3–10⁴ km/s, 600 points, bisected);
  2. continued in the baryon strength λ from 0 to 1 in 8 equal steps, by damped 2-D Newton in (ln σ₀, ln ρ₀) at each
     step (outward RK4, 400 steps in ln r from 10⁻⁵ r₁ to r₁; residual tolerance 1e-9, converged if < 1e-7).

  A system whose continuation does not converge, or with no λ = 0 root, is **unconverged**. It is graded with its pure NFW
  halo, and counted per class (check K3).

**s(v) — PRIMARY, zero free parameters.** BU1's fully fixed cross-section per mass,
s(v) = K (√π/4)^(1−n) v^(−n), i.e. s·v = K σ₀^(1−n), with:
- n = 2 q_f − 1 = 0.784 (canonical) / 0.496 (alt);
- K = 9 σ_ref^(1+n) / (4π G t Σ_a0²) (SC1 anchor, σ_ref = 70.50 km/s);
- K and n read from `BU1_bullet_cross_section/bu1_cross_section_results.json` (824adf757c), never moved;
- s(159 km/s) = 0.155 / 0.106 cm²/g.

**Reported variant (not class-setting).** s → A·s with n kept. A is calibrated **once, on SPARC alone** per footing:
argmin of SPARC background-A rms over log₁₀ A ∈ [−2, 2] in steps of 0.1, then refined in steps of 0.02 within ±0.1 of the
coarse minimum. Every class below is then reported at A_f with the same rules, labelled REPORTED. The bound margins of
BU1 (s(3000) vs 1.25, s(1000) vs 0.47, s(1900) vs 0.35) are reported at A_f.

## 1. Baryons in the Jeans potential, and the halo M_b per class (fixed now)

| class | M_b for M200 | baryon mass profile M_b(r) in the Jeans equation | halo outside r₁ |
|---|---|---|---|
| SPARC (175) | EM1's M_b,ref = 0.5 L36 + 1.33 M_HI | from the rotmod: r [V_gas\|V_gas\| + Υ (V_disk² + 1.4 V_bul²)] / G, V² linear in r between points, ∝ r² inside the first point, M constant beyond the last; total clipped at ≥ 0. **Solved at every Υ of EM1's grid (0.30–1.20, 91 values)**, so the halo moves with Υ | NFW to R200, then constant (X38's truncation) |
| clusters (326 × 2 h) | X30's M_b(r_max) (gas × 1.2) | X30's `prep` M_b(r) (gas × 1.2) + CFG922 BCG, M_BCG r²/(r + 10 kpc)², matched and tercile-filled exactly as X39 / X40b | NFW, R200 at 200 ρ_c,A(z), c = cB(M200, z); constant beyond X30's r_ta (X38's truncation) |
| groups (63) | catalogue M_b | Hernquist M_b, a = R_e / 1.8153 (P4 T3's tracer) | NFW to R200, then constant |
| SLUGGS (4) | M★ (route-E JAM analogue, GR1 §1b: 0.5 M★ + M_h(< r12; M★) = 0.5 M_JAM by Brent in log M★) | Hernquist M★, a_h (CFG528) | NFW to R200, then constant |
| dwarfs (89 per footing) | M★ (X1) | Plummer M★, a = r_h (X1 `rh_pc`) | NFW to R200, then constant; isolated reading (no host stripping), as CD1 / OS1 |

Background A for clusters, groups, SLUGGS and dwarfs (as GR1). SPARC is graded on A and reported on B (as X38).

## 2. Grades per class of system (both footings; per footing PASS / IMPROVES ON OS1 / FAILS)

"OS1" means OS1's core law at q_f = 0.892 / 0.748, read from the committed JSONs: OS1 (SPARC, clusters, dwarfs) and GR1
(groups, SLUGGS, which ran OS1's law at q_f).

1. **SPARC** (EM1 / X38 machinery, P4 mask, weights, per-galaxy Υ). Line: rms ≤ 0.110 and 0.50 ≤ median Υ ≤ 0.80.
   - PASS: line passes on background A and on background B.
   - FAILS: otherwise. (OS1 passes SPARC, so IMPROVES does not apply.)
2. **Clusters** (X38's 15 eRASS1 cells via X30's machinery, read-only, both h; a cell passes if |Z| ≤ 2 at both h).
   - PASS: all 15 cells pass.
   - IMPROVES ON OS1: not PASS; at most one cell fails; and the summed |Z| of the failing cells (max over h) is below
     OS1's (5.31 / 4.40).
   - FAILS: otherwise.
3. **Groups** (GR1's P4 T3 estimator, `class_stats`, slope from ±0.01 dex in M_b).
   - PASS: verdict CONSISTENT.
   - FAILS: otherwise. (OS1 passes the groups, so IMPROVES does not apply.)
4. **SLUGGS centrals** (GR1's CFG528b machinery: measured tracers, variable-β multi-population Jeans, CFG528 `score`).
   - PASS: CFG528's `closes`.
   - IMPROVES ON OS1: not PASS; all 4 computable; none reversed (Z < −2); and |mean offset| ≤ 0.5 × OS1's
     (0.1273 / 0.1272 dex).
   - FAILS: otherwise.
5. **Dwarfs** (X1's 89 per footing; CD1 / OS1 rule). The requirement is g_h,req = g_obs − g_N at r₁₂ = (4/3) r_h, with
   g_N = G (M★/2)/r₁₂² and g_obs = g_N 10^Δ[Newton]. The prediction is the IJ halo's g_h(r₁₂). S_i = g_h,req / g_h,pred,
   and z_i = (log g_h,req − log g_h,pred) / sd_h, with sd_h exactly as CD1 / OS1 (rows with 10^Δ − 1 < 0.1 ungraded; Δ ≤ 0
   rows S = 0, z = −∞).
   - frac_up = fraction with z ≥ 2 (under-supply).
   - frac_over = fraction with z ≤ −2 among rows with finite z (over-supply; the IJ halo is a prediction, not a cap).
   - PASS: frac_up < 5 %, median S ≤ 1, and frac_over < 25 %.
   - IMPROVES ON OS1: not PASS; frac_up ≤ 0.5 × OS1's (0.652 / 0.483); and frac_over < 25 %.
   - FAILS: otherwise. The CD1 label (EXCLUDE / PARTIAL / CONSISTENT) is reported alongside.

**Motivating targets** (per footing):
- T-IC: G-IN-Mall passes (|Z| ≤ 2 at both h). IC1 found the Burkert INNER band over-predicted ≈ 2×.
- T-GR: SLUGGS PASS or IMPROVES ON OS1. GR1 found the centrals short by +0.127 dex.
- T-DW: dwarfs PASS or IMPROVES ON OS1. OS1 found them EXCLUDE.

| lane class (per footing; the verdict needs both footings to agree, else UNDECIDED) | rule |
|---|---|
| IJ PASSES | all five classes PASS |
| IJ HITS TARGETS | all three targets met, SPARC PASS, and no class that OS1 passes (SPARC, groups) FAILS, and clusters not FAILS |
| IJ PARTIAL | at least one target met, but not IJ HITS TARGETS |
| IJ FAILS | no target met |

## 3. Reported only (no class weight)

- Per class: the distribution of r₁, σ₀, ρ₀, the number of λ = 0 roots, unconverged counts, r₁ > R200 counts.
- SPARC: background B as a class input (above), and the rms and Υ at background A.
- Clusters: OS1's mass convention instead of EM1's relation (M_fair = 5.364 M_b inside r_ta, NFW normalised at R200 =
  M_fair). The 5.364 is a ΛCDM-derived ratio; this row is a comparator to OS1 only, never a grade.
- Clusters: the no-BCG reading.
- Dwarfs: grades by X1 class; the CD1 label.
- The variant at A_f (all five classes, bound margins).
- Pure NFW (no core, s → 0) per class, so that the effect of the core is visible.

## 4. Checks

- **K0** The isothermal solver reproduces IC1's Lane–Emden table (`IC1_inner_cluster_band/ic1b_lib.py` `_MU`, executed
  read-only): with M_b = 0, the RK4 integrator's M(r) / (4π ρ₀ r_c³) equals IC1's ξ²ψ′ for ξ ∈ [10⁻², 10³] to 1e-6
  (relative), and this lane's own (ψ, ψ′) table equals IC1's ξ²ψ′ to 1e-9.
- **K1** Matching conserves mass. For a frozen sample (20 SPARC (galaxy, Υ) lanes drawn with seed 20261026, 20 clusters,
  10 groups, the 4 SLUGGS, 10 dwarfs, per footing), an independent outward solve_ivp (LSODA, rtol 1e-10) from the centre
  at the solved (σ₀, ρ₀) reproduces ρ(r₁) / ρ_NFW(r₁) and M(r₁) / M_NFW(r₁) to 1e-4.
- **K2** s(v) reproduces BU1's JSON s values at 10–4700 km/s to 1e-9 (relative) on both footings.
- **K3** Unconverged systems are ≤ 1 % of every class, per footing. If K3 fails, the class is still reported, flagged.
- **K4** Record reproduction: OS1's cluster cells at q_f (Burkert path of `ic1b_lib`) equal OS1's JSON to 1e-6; GR1's
  groups mean and SLUGGS mean at q_f equal GR1's JSON to 1e-6; OS1's dwarf frac / median S reproduce to 1e-9; EM1's cB
  at 10¹² M☉ equals 11.81 (A) / 11.51 (B) to 0.005.
- **K5** Peak RSS < 1 GB, one thread.

**MUTATE (`--mutate`, separate `_MUTATE` outputs).** Baryons are removed from the Jeans potential (λ = 0 everywhere);
everything else is unchanged. The tooth bites if, on both footings:
- the SLUGGS class-mean offset moves by ≥ 0.02 dex from the real run; and
- the cluster G-IN-Mall prediction (h 0.672) moves by ≥ 2 % from the real run.

The MUTATE run exits 1 if the tooth bites, as in OS1 / GR1. If it does not bite, the README says that baryons do not
control the graded IJ cores.

## 5. Disclosed before freezing

- **ΛCDM leaks carried in.** The outer halo is the record's EM1 NFW with Bullock+01 c(M), and EM1's M200(M_b) relation was
  fitted with NFW halos. Both are on the owner's 10-25 list of ΛCDM-calibrated inputs. They are used because the hypothesis
  names "the record's collisionless route-E halo", and they are flagged in the ledger as OPEN gaps, not framework results.
  The clusters keep X30's `DA_lcdm` distance rescaling (inherited, flagged). The cluster M200 here comes from EM1's relation,
  not from the 5.364 fair share; the fair-share row is reported only.
- **Expected direction, written now.** With s ≈ 0.1–1 cm²/g at galaxy speeds, the cores sit inside a few kpc in galaxies
  and inside ~0.1 Mpc in clusters (s ≈ 0.02–0.04 cm²/g). Outside r₁ the halo is the Bullock NFW. IC1_inner_column_cores
  found that this borrowed NFW c(M) overshoots SPARC (median Υ 0.30) and over-predicts cluster cores. IJ cores may be too
  small to undo that, so SPARC may fail its Υ leg and the clusters may over-predict INNER / MID. Dwarfs gain cuspier NFW
  mass at r₁₂ than a capped Burkert, so frac_up should fall; frac_over may rise. The answer can go either way, and both
  outcomes are written down now.
- **Extrapolation.** EM1's relation is used for clusters (log M_b ≈ 13–14.5), groups, SLUGGS and dwarfs (about 4 dex below
  SPARC), as GR1 / IC1 did.
- **t = 13.8 Gyr** for every system, including clusters at z ≈ 0.1–0.6 (as the hypothesis states).
