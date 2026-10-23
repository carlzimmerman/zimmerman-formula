# S4_v3_muK_clusters — FROZEN CRITERIA (before any script or number of this lane)

Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. Task: batches **R6** (main) and
**R4** (lowest priority) of `rebuild_2026_10_22/N0_board_audit/AUDIT.md`. κ = ½ FITTED. Footings a₀ = 9.3603e-11
(canonical) / 1.1312e-10 m/s² (alt), never pooled. No dark-matter particle: the cold sector is the Blanchet–Skordis K(Q)
dust ("cold energy"). Never "theory closed"; never "the data favour the framework". Compute: `OMP_NUM_THREADS=1 nice -n 15`,
one thread, < 1 GB RSS, minutes; no downloads; no PM simulation. Inputs and classes: `ASSUMPTION_LEDGER.md` (committed
with this file).

## R6.0 The question

F1 (clusters) and F2 (isolated-lens outer lensing) were rebuilt with AQUAL μ = x/(1+x) and **without** v3's μ_K²ψ term.
v3's static equation (BS24 Eq. 35, re-derived from the action in C4 K1, residual 0) is

    ∇·[μ(|∇ψ|/a₀) ∇ψ] + μ_K² ψ = 4πG ρ_b ,   μ(x) = x/(1+x),   ϕ = ψ (lensing = dynamics, BS24 Eq. 24 / C4 K1).

The μ_K²ψ term is the K(Q) dust in hydrostatic balance (L1 §1: 4πG δρ_K = −μ_K²ψ; F3 K1(ii): the dust Jeans wavenumber
is μ_K to O(Q̄ − 1)). Questions:
(a) Recompute F1's 326-cluster stack and F2's isolated-lens stack with the full static equation, μ_K over BS24 Eq. 39's
    allowed range (μ_K⁻¹ ≥ 100 kpc ⇔ μ_K ≤ 10 Mpc⁻¹ physical = 14.8 h/Mpc at F3's h) and at F3's growth-motivated values.
    Report cluster A_MID / A_OUTER / profile χ² and the outer-lensing amplitudes, old → v3.
(b) Does the Khronon version differ from H2's AeST analogue (ramp, then oscillation)? Sign and profile.
(c) (coordinator, M2 follow-up) the radial profile of the dust contribution in clusters vs an isolated galaxy at
    μ_K⁻¹ = 0.1, 0.3 and 1 Mpc; whether any allowed μ_K gives ×1.4–1.8 at 0.3–1 Mpc, ≈ 0 beyond, and ≈ 0 around isolated
    galaxies; the sign and any oscillation.

Stated before computing (an identity, to be checked numerically, not assumed): in spherical symmetry, with
r²μ(|ψ′|/a₀)ψ′ = G[M_b(r) + M_K(r)] and M_K(r) = −(μ_K²/G)∫₀^r ψ r′² dr′, this is term for term H2's AeST system with
μ → μ_K. K2 below tests that by reproducing H2's numbers with an independent solver and projector.

## R6.1 Model and grids

- Spherical exact solve per object: state (ψ, M_K), ψ′ = sgn(M_b + M_K) · g_AQUAL(G|M_b + M_K|/r²), g_AQUAL(y) the root of
  g²/(g + a₀) = y; M_K′ = −μ_K² r² ψ / G. Fixed-step RK4 in r on a hybrid grid (log steps, then uniform steps no longer
  than a fixed fraction of 2π/μ_K), from r_min to r_max with a series start. Lensing mass M_L(r) = r²ψ′/G.
- **Zero point** (μ_K² makes ψ's constant physical; every regular solution decays at infinity, so no boundary condition
  fixes it): H2's convention, i.e. VSZ's λ = λ_max(μ_K, r_M) + Δ imposed on the μ_K = 0 solution at 3 Mpc,
  λ_max = (2/3)(1 − ln(3√2/(μ_K r_M))), M = M_b(< 3 Mpc), r_M = √(GM/a₀), s = √(GMa₀). **Primary Δ = 0.**
  Envelope: one universal Δ ∈ [−8, +2] step 0.25 (a free constant: counted +1 if it is what makes anything pass).
- **μ_K grid (physical Mpc⁻¹), allowed:** 0.015637 (BS24's own value, 1e-31 eV; F3 K4 "BS24 scale"), 0.03, 0.1, 0.3, 0.5,
  0.7, 1.0, 2.0, 3.333 (μ_K⁻¹ = 0.3 Mpc), 5.0, 10.0 (μ_K⁻¹ = 0.1 Mpc, the cap).
  **Growth-motivated (F3 K5; EXCLUDED by BS24 Eq. 39; reported, never graded):** 243.78, 277.82, 1718.0 Mpc⁻¹
  (μ_K⁻¹ = 4.102 / 3.600 / 0.582 kpc = F3's 360.7 / 411.1 / 2542 h/Mpc). Δ ∈ {−8, −4, −2, −1, 0, +1, +2} there.
- **Clusters:** F1's PRIMARY recipe, read from F1's measurement cache `f1_meas.pkl` (argv, sha256 recorded; as H2/J1/K1/M2):
  gas rescaled q^{5/2}, R500 × q, β-model G0 to 3 Mpc, × 1.20 (f★ = 0.20), data boost applied, catalogue miscentring;
  cells = footing {canonical, alt} × h {0.672, 0.686}. A1-clipped boost reported.
- **Projectors.** P1 = F1's convention (Σ on F1's 90-point grid from the exact shell projection of piecewise-linear M_L,
  catalogue miscentring, F1's ΔΣ formula, value at the bin centre); used for K1/K2 and reported. **P3 (graded, allowed
  μ_K)** = the same chain on a 1200-point grid, bin value = the area-weighted annulus average over the bin edges (an
  oscillating prediction must be averaged as the data are; at μ_K = 0 P3 − P1 is reported). P2 = exact annulus average from
  the shells, no miscentring (growth μ_K, where P1/P3 cannot resolve the oscillation; with its own μ_K = 0 baseline).
- **Isolated galaxies (F2 Track A):** B21 Fig. 3 (4 M★ bins × 15 radii, released covariance), F2's native conversion
  (h 0.679, Ω_m 0.3085, T_Ωm 1.0128), F2's per-lens inventory (M★ LePhare + 0.15, cold-gas relation, hot CGM 0.5 M★ uniform
  to 100 kpc) and lens weights. **y_e = 0: exact** (spherical). **y_e = noclu: APPROXIMATION** — v3's μ_K profile × F2's
  point-mass EFE ratio C(r; y_e) (F2's own extended-baryon convention). A uniform external field is not a solution of the
  μ_K equation (μ_K² x_e z ≠ 0), so the in-field problem is not posed exactly here; labelled, never graded.
  Graded galaxy quantities use annulus averages over B21's bins (edges at geometric midpoints of the radius labels),
  r_max = 30 Mpc with M_L constant beyond, for the law (μ_K = 0) and v3 alike. The F2-convention law (point values,
  linear tail) is reported as the reproduction.

## R6.2 Statistics

- Cluster: A_band = Σ W D / Σ W P over clusters and band bins (INNER 0–2, MID 3–5, OUTER 6–7 of F1's 8 log bins
  0.15–3 Mpc), jackknife over F1's 30 RA patches; Z_MID = (A_MID − 1)/σ, Z_OUT = (A_OUT − 1)/σ; **profile χ²** = H2 A1's
  (residual stack over bins 3–7, jackknife covariance, Hartlap (30−5−2)/29), line 11.07; stacked ratio per bin
  R_j = Σ_i W_ij P_ij(v3) / Σ_i W_ij P_ij(law).
- Galaxy: per B21 bin and radius, the lens-weighted stacked ΔΣ; ratio v3/law; Track A χ²_all (60 points), GLS amplitudes
  A_in (R ≤ 0.31), A_O1 (0.4–1.1), A_O2 (> 1.1 Mpc), as F2.

## R6.3 Verdict rule (graded; both footings; the weaker verdict if they split, split stated)

A cluster cell passes at (μ_K, Δ) iff |Z_MID| ≤ 2 AND |Z_OUT| ≤ 2 AND profile χ² ≤ 11.07 (P3).
**Galaxy guard** at the same (μ_K, Δ, footing): in each of the four B21 bins, |ΔΣ_v3/ΔΣ_law − 1| ≤ 0.14 at every B21
radius with label ≤ 1.1 Mpc (y_e = 0, annulus averages; 0.14 is K1/M2's isolated-galaxy line).

- **v3's μ_K TERM CAN SUPPLY IT:** at Δ = 0 some allowed μ_K passes all four cluster cells and the guard.
- **CAN ONLY WITH A FITTED ZERO POINT:** no Δ = 0 pass, but one universal Δ at one allowed μ_K passes all four cells and
  the guard (+1 fitted constant; not a cure, rebuild rule 4).
- **CANNOT:** no allowed (μ_K, Δ) passes all four cells with the guard. Reported why: the best A_MID with |Z_OUT| ≤ 2, the
  minimum profile χ², cluster-only passes that the guard removes, and the shape (ramp / oscillation radii).
- **UNDECIDED:** any of K1–K7 fails.

Reported, never graded: growth μ_K (P2); y_e = noclu galaxy rows; Track A χ²/amplitudes at every μ_K (the "old → v3"
table, old = F2's L4 / T_central rows); μ_K,gal = the smallest grid μ_K whose Δ = 0 guard fails.

**Shape test (the coordinator's question; frozen definition, reported):** at each allowed μ_K (Δ = 0, and the best Δ):
R_MID (W-weighted stacked ratio over bins 3–5) ∈ [1.4, 1.8] AND R_6, R_7 ∈ [0.9, 1.1] AND the isolated galaxies'
|ratio − 1| ≤ 0.10 at all B21 radii ≤ 2.6 Mpc in all four bins. Also its literal 0.3–1 Mpc form (bins 2–4) and > 1 Mpc
(bins 5–7).

**Profiles (reported):** at μ_K⁻¹ = 0.1, 0.3, 1 Mpc (μ_K = 10, 3.333, 1.0), Δ = 0, both footings, h 0.672: stacked cluster
ratios per bin; for the median cluster and for each B21 bin's weighted-mean lens: M_K(r)/M_b(r), M_L(v3)/M_L(law),
δρ_K/ρ_b at fixed radii (cluster 0.05–3 Mpc; galaxy 0.035–2.6 Mpc); the radii of the first zero of ψ (dust density changes
sign), of M_K and of M_L (medians over clusters).

**Dust-sign diagnostic (reported):** ρ̄_K(z) = Ω_K ρ_crit,0 (1+z)³ on L1's model B (Ω_m 0.2976016, h 0.6856427,
ω_b 0.0223081; Ω_K = Ω_m − Ω_b, FITTED abundance). Volume fraction in 0.15–3 Mpc (clusters, at each z) and 0.035–2.6 Mpc
(galaxies, z_eff) where δρ_K < −ρ̄_K, i.e. the hydrostatic branch needs a negative absolute dust density.

## R6.4 Checks (`s4_v3_muk_clusters.py <dir holding f1_meas.pkl> [--mutate]`; one line each; exit 0 iff all pass)

- **K1** μ_K = 0, P1: F1 PRIMARY A_MID and A_OUTER in all 4 cells to ≤ 0.01 (F1's JSON).
- **K2** H2 reproduction (the identity of R6.0): P1 stacked ratios R_0…R_7 at μ = 0.1, 0.3, 0.5, 0.7, 1.0 Mpc⁻¹, Δ = 0,
  all 4 cells, against H2's `boost_vs_law`: max |difference| ≤ 0.02.
- **K3** Newtonian homogeneous Helmholtz (ρ_b = 0, a₀ → 0): ψ = Φ_c sin(μr)/(μr) to ≤ 1e-6 of Φ_c for r ≤ 20/μ, at
  μ = 10 and 1718 Mpc⁻¹ on the grids used there.
- **K4** Newtonian sourced Helmholtz, top-hat a = 0.3 Mpc, μ = 3.333 Mpc⁻¹: ψ′ against the analytic solution ≤ 1e-5 of max.
- **K5** projectors on a Plummer sphere (M 1e14 M☉, a 0.2 Mpc), no miscentring: P1 point values and P2/P3 annulus averages
  against the analytic ΔΣ = MR²/(π(a²+R²)²) (annulus averages by quadrature): ≤ 2e-3 relative in bins 0–7.
- **K6** F2 reproduction at μ_K = 0 (F2 convention): rows "OAT EFE y_e = 0" and "L5 T_central", both footings:
  |ΔA| ≤ 0.005 for A_in, A_O1, A_O2 and |Δχ²_all| ≤ 0.5 (F2's JSON).
- **K7** convergence: halving every ODE step changes the cluster stacked ratios R_0…R_7 by ≤ 0.005 at μ_K = 10 (P3,
  Δ = 0, canonical h 0.672) and by ≤ 0.01 at μ_K = 1718 (P2); and the galaxy stacked ratios at μ_K = 10 by ≤ 0.005.
- Reported, not graded: r_max 30 → 60 Mpc at μ_K = 0.1 and 1.0 (clusters).
- **K8** peak RSS < 1 GB.
- **`--mutate`:** μ_K² → −μ_K² (Yukawa); K2, K3 and K4 must FAIL (exit 1); outputs `*_MUTATE.out`, `*_results_MUTATE.json`.

## R4 Kernel-only recomputes (lowest priority; tiles 22, 33, 34; galaxy groups are lane P4's)

Method: each committed script is run unchanged in a wrapper (`s4_r4_kernel_swaps.py`) that (i) replaces `nu_mono` in
`campaign_fresh_gravity/CFG4_common.py`'s module object (the record's ν_mono, FP1/L340) by v3's ν₁(y) = (1 + √(1 + 4/y))/2
before the script imports it, and (ii) redirects every file the script writes into this lane (`r4_out/`); the record's
lanes are hashed before and after.
- Tile 22: `CFG528_sluggs_centrals_mechanism/cfg528b_measured_tracers.py`; plus the v3 reading "all baryons, no ownership":
  the R-own reading replaced by R-bar (gas extrapolated, no host ownership), so its joint best case J uses R-bar.
- Tile 33: `CFG303_lcdm_free_inputs/cfg303_{amvrosiadis,cfg90_noema,kurvs,musedark,rc100_cristal,xcop}_LCDMFREE.py`.
- Tile 34: `CFG307_aless122_stress_test/cfg307_stress.py`, `CFG308_cristal_stress_test/cfg308_cristal_stress.py`.
Checks (per script): **R4-K0** the wrapper with ν_mono reproduces the committed results JSON (every numeric leaf,
relative ≤ 1e-9 or absolute ≤ 1e-12; a script that cannot run on disk data is reported N/A with what is missing, not PASS);
**R4-K1** the swap reached the kernel (a probe ν(1) = 1.6180 inside the run, and at least one numeric leaf changes);
**R4-K2** no file in the record's lanes changed (sha256 before/after). Reported: each script's headline numbers old → v3
and its own printed verdict/class. **Verdict-safe** iff the record's own class/verdict words are unchanged under ν₁.
`--mutate`: the reproduction run uses ν₁, so R4-K0 must FAIL.

## Not done here

No PM run, no aspherical solve, no in-field μ_K solve, no Track B (F2) re-score, no new data, no fitted amplitude.
Anything not computed is said so in the README.
