# CFG332 FROZEN CRITERIA: the outer-halo globulars under three routes

**Lane:** orchestrator. κ = ½ is FITTED and fixed. Both footings: a₀ = 9.36e-11 and 1.13e-10 m s⁻². Kernel: the record's `hunt_lib.nu_s` (exponential RAR). ν_mono equals it for y ≤ 2.34, which covers every cluster here. No downloads, no knob scans, no fitting beyond h93's own one-Υ joint fit (a control).

**Baseline.** `hunt_2026/h93_outer_halo_globulars`: NGC 2419, Pal 3, Pal 4, Pal 14. The law with the host's algebraic external field, ν(y_int + y_ext), over-predicts σ by about 1.8×. Marginalised over Υ_V ~ lognormal(1.6, 0.15 dex), the framework is excluded at 4.6σ (canonical) / 4.9σ (alt).

**Data (on disk only).** `real_research/data/globular_clusters/baumgardt_gc_parameters.tsv` and `baumgardt_gc_veldisp_profiles.tsv` (h93's inputs). `deepseek_push/data2/baumgardt_combined_table.txt` for the mass-function columns M_Low, M_High, MF slope, ΔMF. Baumgardt's dynamical mass and dynamical M/L_V columns are NEVER used as inputs, because they are Newtonian.

## Statistic (all routes)
Per cluster: the χ²_(N−1) dispersion probability, h93's `p_low`. It is marginalised over the route's Υ prior (4000 draws, seed 931), Fisher-combined over the four clusters, and converted to a one-sided Gaussian σ.
- **T (two-sided, PRIMARY):** p_i = 2·min(F, 1 − F). This is primary because a Newtonian prediction can miss on either side (Pal 3).
- **L (h93's one-sided low):** reported, used for the control.

Sensitivities are reported but not scored:
- without Pal 3;
- with the published alternative dispersions (Pal 14: Jordi+09, 0.38 ± 0.12; Pal 4: Frank+12, 0.87 ± 0.18).

## Decision rule (per route, on T)
- **MATCH:** T < 2σ on both footings.
- **PARTIAL:** T < 2σ on one footing, or T at most half the h93-configuration T on both footings.
- **NOT:** otherwise.

Routes and classifications are never pooled.

## Route 1: ownership
- **Rule.** Quote the record's rule and its location (FG001 = `CFG7_hierarchy_fg001.py`, PAPER35 §2). State whether it decides globulars.
- **(a) owned (class E, Newtonian):** σ = Wolf σ_N with Υ ~ lognormal(1.6, 0.15 dex).
- **(b) top-level**, scored two ways and kept separate:
  - **(b-EFE)** = h93: the law with the host's algebraic external field (the record's rival reading);
  - **(b-B)** = B's own top-level/accreted treatment: the isolated law ν(y_int), no external field.
- **UFD matrix.** Rows (a), (b-B), (b-EFE). UFD entries are read from `AUDIT_UFD_2026-10-03/audit_ufd_results.json`: base (+0.325 / +0.304 dex) and the EFE rival. No new UFD computation.
- **NEW POSTULATE.** If separating globulars from dwarfs needs a criterion that is not written in the record, it is flagged as a NEW POSTULATE.

## Route 2: dynamically evolved stellar M/L
- **Input.** Baumgardt's per-cluster MF slope α (dN/dm ∝ m^α over M_Low–M_High; all four have M_Low ≥ 0.47).
- **Reference population.** Kroupa (−2.3 above 0.5 M☉, −1.3 for 0.1–0.5), with Υ_ref = 1.6.
- **Cluster mass function.** Normalised to Kroupa at m_TO = 0.80, so the turn-off and giant light is fixed. The light change from removing faint dwarfs is neglected; that choice favours the framework.
- **Two low-mass branches** (both scored, never pooled):
  - **S:** a single power law α from 0.1 to 0.8;
  - **K:** α above 0.5 and α + 1 from 0.1 to 0.5 (Kroupa-shaped break).
- **Remnants.** White dwarfs come from 0.8–8 M☉ (Kroupa −2.3), with m_f = 0.109 m_i + 0.394. They are depleted by the cluster/Kroupa dN/dm ratio at min(m_f, 0.8). Neutron stars and black holes are retained at 0 in both the reference and the clusters.
- **Υ_MF.** Υ_MF = 1.6 × M_cluster/M_Kroupa. The prior is lognormal(Υ_MF, √(0.15² + δ_α²)), where δ_α is half the log spread of Υ_MF at α ± Δα.
- **Scoring.** Scored with the law, using h93's algebraic EFE (primary); the Newton row is reported.
- **Caveat (stated now).** The slopes come from Baumgardt's Newtonian N-body fits to star counts. The slope is a photometric quantity, but its independence from the kinematics cannot be verified on disk. The route is labelled CONDITIONAL.

## Route 3: full external field (QUMOND)
- **Model.** A Plummer cluster (a = r_h,l, M = Υ L_V) in a uniform Newtonian external field g_Ne = G M_MW/R_GC² (M_MW = 6e10, as in h93), along z.
- **(i) Exact monopole.** ∇·g = ∇·[ν(|g_N|/a₀) g_N] makes the flux of g through any sphere equal the flux of ν g_N. The sphere-averaged radial internal field at r₁₂ = (4/3) a is therefore an exact angular integral (Gauss–Legendre). This gives σ² = r₁₂ ⟨g_r⟩/3, the analogue of h93's estimator, and is the **PRIMARY** route-3 prediction.
- **(ii) Grid solve.** An axisymmetric (R, z) finite-difference Poisson solve of −∇²φ = ∇·(ν g_N − ν_e g_Ne), with a monopole Dirichlet boundary. It gives the tensor-virial line-of-sight σ along and across the field (the anisotropy range), and it checks (i).
- **Clusters.** All four (Pal 14, Pal 3 and Pal 4 are the targets; NGC 2419 rides along).
- **Reported.** σ_num/σ_alg per cluster, and the rescored T and L.

## Controls (must pass; a failure is kept and reported)
- **C1:** h93 reproduced: the L statistic 4.6σ / 4.9σ (±0.1), the joint Υ 0.76 (framework, canonical) and 2.14 (Newton) (±0.01), and the required Υ_F per cluster (±0.01).
- **C2:** with the external field off and the deep-MOND kernel, the global virial σ_los⁴ = (4/81) G M a₀ to 1%. This holds for the flux method and for the grid.
- **C3:** with g_ext ≫ g_int, the boost → ν_e(1 + L/3), which is h93's anisotropic trace, to 1%. With y_ext ≫ 1, the boost → 1 (Newton) to 1%.
- **C4:** the grid's sphere-averaged g_r at r₁₂ matches (i) to 2%. Doubling the domain moves the line-of-sight σ by < 2%.
- **C5:** the Route 2 Kroupa input (α = −2.3, branch K) returns Υ_MF = 1.6 exactly (1e-6).
- **MUTATE** (CFG332_MUTATE=1, separate outputs): the clusters' measured (σ, error, N) are reversed (NGC 2419 ↔ Pal 14, Pal 3 ↔ Pal 4). The T tension of every route must rise.

## Lean
One Lean 4 file certifies each route's decisive scalar claim as rational interval inequalities (norm_num), using inputs rounded outward from the results JSON. It is compiled with `lake env lean`, with no sorry. It certifies arithmetic, not statistics.
