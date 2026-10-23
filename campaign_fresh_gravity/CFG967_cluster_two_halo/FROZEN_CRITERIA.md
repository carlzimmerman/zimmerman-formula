# CFG967 FROZEN CRITERIA: the framework's catalogue two-halo term around the 318 eRASS1 clusters (NA-5); does it move the outer ΔΣ–M_gas slope? (committed alone, before any script or number)

Block CFG960–969 (LEDGER reservation row, 2026-10-21). Angle NA-5 of `NEW_ANGLES_SCOUT_2026-10-21.md` (b54828855).
κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled. Raw KiDS data, framework-native model: no HMcode,
BAHAMAS, ΛCDM mass function or ΛCDM halo-model two-halo term. Not "theory closed". Nothing here says the data favour the framework.

## 1. Why

- CFG687 (criteria 12cb826e8) stacked raw KiDS-1000 shear around 318 eRASS1 clusters. T2 found ΔΣ_OUTER (1.2–3 Mpc) ∝
  M_gas500^s with **s_obs = 0.896 ± 0.209** (30-patch jackknife), against the law's **s_law = 0.466** and Newton's 0.836:
  "FOLLOWS NEWTON". A_OUTER by gas tercile 0.57 / 0.96 / 1.38; A_MID 1.91 ± 0.12 (canonical), 1.75 ± 0.11 (alt).
- CFG687 named environment below X-ray detection (correlated neighbours, a two-halo term that grows with mass in any theory) as
  an open mechanism. It only tested eRASS1 neighbours (post hoc: flat with mass; isolated clusters give s 0.85).
- CFG903 (bb665cf4f, A1 26ecb00ce, A2 a6449299a) built the framework's own no-free-amplitude catalogue two-halo term (KiDS-bright
  neighbours, each with its baryons plus catchment cold energy on CFG804's truncated law profile, random-clone subtracted). It
  has never been run around the clusters. CFG815/817: the middle gas tercile's shortfall is real, not a selection artefact.

## 2. The law statement used for the cluster prediction (coordinator note, 2026-10-23)

- **Record's current statement:** the action gives AQUAL, ∇·[μ(|∇Φ|/a0)∇Φ] = 4πGρ with **μ(x) = x/(1+x)**
  (doors_push_2026_10_22/E2; PAPER58). For a spherically symmetric source the curl term vanishes and AQUAL reduces exactly to
  g = ν(g_N/a0) g_N with **ν_s(y) = ½ + √(¼ + 1/y)**. The screening length L★ (24–90 pc) has no effect on 0.1–3 Mpc cluster
  shells and is not modelled.
- **CFG687 used** the algebraic law with **ν_mono** (FP1's monotone repair of ν_RAR, `CFG4_common.nu_mono`) on its spherical
  β-model. In spherical symmetry AQUAL and the algebraic (QUMOND-form) law coincide for a matched ν, so the only difference is
  the interpolating function: ν_mono vs ν_s.
- **Primary law kernel: ν_s (AQUAL μ = x/(1+x)).** ν_mono rows are computed in full as CFG687's continuity rows (and are what K1
  reproduces). CFG903's neighbour profile (ρ ∝ 1/(2π s √(1+4s²))) is already the μ = x/(1+x) point-mass phantom, so the primary
  is one consistent statement.

## 3. Inputs (on disk; no download; all read-only)

- `CFG687_erass1_shear_stack/cfg687_percluster.npz`: per cluster D (random-subtracted ΔΣ, 8 bins), E, PL (ν_mono canonical law),
  PN (Newton), mg = Mgas500, z, ra, dec, R500. CFG687's `law()` (exec'd slice) and CFG686's distances / projection (exec'd
  slices without the KiDS source columns, CFG949's recipe).
- CFG903: `cfg903_lib.py` (imported: pool definitions, N_of_declared, edge_of, d/m binning, watchdog);
  `cfg903_score.py` (exec'd slices: profile, F2, point_I, kernel, twoh_table, T_at); `cfg903_stage_results.json` (completeness:
  Z0, m_lim, slab ρ_tot, m_f); `../_external_data/cfg903_work/cfg903_stage.npz` (the neighbour pool NB_*), and
  `cfg903_hist_bin{1-4}.npz` (only for K2). Bright sample FITS (RA, Dec, masked only) for the random mask, as CFG903 stage A.

## 4. The two-halo term per cluster (CFG903 verbatim unless stated)

- **Neighbours:** CFG903's pool (r < 20, 0.02 ≤ z_phot ≤ 0.8, finite log M★ > 7); primary masked = 0. Projected physical
  separation d < 4.61 Mpc and |Δχ_phot| < 500 Mpc (W500).
  - d = θ D_A(z_cl) with CFG687's own BAO-raw D_A (so d is on the same radius scale as CFG687's shear bins).
  - The χ window uses CFG903's χ (DC, flat Ω_m 0.3, H0 70), as the stored neighbour χ.
- **Neighbour mass:** M_b = M★(1 + f_cold) as a point, plus catchment cold energy 5.364 N M_b, N from CFG902's declared fixed
  point; cold energy on CFG804's truncated law profile (P1), shape snapped to NGRID ∪ {1.25, 1.5, 1.75}, renormalised to the
  exact mass; r_M = √(G M_b/a0) per footing.
- **Completeness:** C1′ primary (A1: neighbours within 0.5 dex above m_lim(z_cl) weighted 1 + f_C1′(z_cl)); C0 and C2′ brackets.
- **Kernel:** CFG903's kernel code exec'd with its bin edges replaced by CFG687's 8 bins (0.15–3 Mpc, 9 log edges). ΔΣ_2h is the
  area average over each annulus (CFG903's estimator); CFG687's law stays point-evaluated at the bin centres (as in CFG903).
- **Randoms:** 50 clones per cluster, drawn uniformly in CFG903's two field boxes and kept if the nearest bright-sample object
  (any flag) is within 4′ and has masked = 0 (CFG903's rule). Seed 967. Each clone inherits its cluster's z, D_A, χ, M_b,cl,
  exclusion edge and completeness factors. ΔΣ_2h(cluster) = lens sum − mean over its 50 clones.
- **Exclusion, "each cluster's own edge" (CFG903's E1 rule with the cluster as the lens):** neighbours less massive than the
  cluster (M_b,j < M_b,cl) with d < r_x are dropped, in the cluster and in its clones; more massive neighbours are kept.
  - **X1 (primary):** r_x = edge(N_cl) r_M,cl, with exact N_cl = N_of_declared(log M_b,cl) (no NGRID snap) and
    **M_b,cl = (1 + f★) M_gas(< 3 Mpc)** of CFG687's primary model (β = 2/3, r_c = 0.15 R500, f★ = 0.20): the very baryons
    the law term sources. Per footing (r_M depends on a0).
  - **X2:** the same with M_b,cl = (1 + f★) Mgas500 (the measured aperture mass only; smaller edge; more double counting).
  - **X3:** r_x = 3 Mpc, CFG687's baryon truncation (the strict no-double-count bound in projection).
  - **E0:** no exclusion (double counts the cluster's own members; reported as the upper bracket).
  - r_x is applied on CFG903's d-bin edges with its log interpolation (T_at), extended to 4.61 Mpc.
- Double counting stated in advance: under X1 and X2, neighbours between r_x and 3 Mpc partly duplicate CFG687's f★ stars
  term. CFG687's law term is the no-edge law (phantom to 30 Mpc), which CFG903 treated as its fixed reference B; adding a
  two-halo term to it is what NA-5 specifies, and it is an upper-side choice.

## 5. Score (CFG687's own stack, jackknife and T2 code, verbatim)

- Model after = law (per footing, per kernel) + ΔΣ_2h; before = law alone.
- A_band = Σ W D / Σ W P over MID (0.5–1.2 Mpc) and OUTER (1.2–3 Mpc), W = 1/E², 30 RA-ordered equal-count patches.
- Slope: CFG687's T2 (full-sample Mgas500 terciles; W-weighted OUTER stack; log–log fit to the 3 tercile medians).
  s_obs = 0.896 ± 0.209 is fixed; s_model is the slope of the model stack. The jackknife σ of s_model(after) is reported.
- Terciles: A_MID and A_OUTER per gas tercile before and after (CFG815's middle-tercile issue).
- **Systematic carried:** CFG687's M2 random-minus-random OUTER offset (+0.130 ± 0.061 canonical, +0.119 ± 0.055 alt). It enters
  the A_OUTER consistency test as σ_tot = √(σ_jk² + offset²); A_OUTER − offset is also reported.

## 6. Pre-declared reading (primary = ν_s, X1, C1′, W500, P1, unmasked; per footing)

Let Δs = s_model(after) − s_model(before). s_obs > s_law, so a move toward s_obs has Δs > 0.
- **EXPLAINS:** |s_model(after) − s_obs| ≤ 0.209 (1σ) AND |A_OUTER(after) − 1| ≤ 2 σ_tot.
- **PARTIAL:** Δs ≥ +0.10 but EXPLAINS not met (including slope reached with A_OUTER inconsistent, labelled so).
- **NO EFFECT:** |Δs| < 0.10. This kills NA-5.
- **MOVES AWAY:** Δs ≤ −0.10. This also kills NA-5.
- Headline: the class shared by both footings; if they differ, the weaker (MOVES AWAY = NO EFFECT < PARTIAL < EXPLAINS), with both shown.
- **A_MID:** "touches the core excess" if |ΔA_MID| ≥ σ_jk(A_MID, before). Not expected.
- **Kill by double counting (from NA-5):** if EXPLAINS or PARTIAL holds only in E0 or X2, NA-5 is killed all the same.
- **Robustness line:** every bracket that changes the primary class, per footing.

## 7. Brackets (one at a time from the primary; class each)

Edge X2, X3, E0; completeness C0, C2′; window W300, W1000; profile P0 (cold energy as a point), P2 (law shape cut at 2 s_max);
mask M1 (masked objects added); law kernel ν_mono (CFG687's).

**Reported only (no verdict weight):**
- **Z17:** clusters with z ≥ 0.17 only, terciles re-cut within the subset, s_obs (with its jackknife) and s_model before/after.
  This is CFG903 A1's bright-end loss: nothing brighter than r ≈ 15.3, so massive neighbours at z ≲ 0.15 are missing; the light
  tercile has median z 0.145.
- The two-halo stack per band and tercile; the random-only term; the host share (neighbours more massive than the cluster).
- The amplitude λ on ΔΣ_2h that would put s_model at s_obs, and at s_obs − 0.209.

## 8. Controls

- **K1:** this lane's ν_mono canonical law equals CFG687's stored PL (max rel ≤ 1e-9). A_MID / A_OUTER (canonical, alt; Newton
  from stored PN) and s_obs, s_err, s_law, s_N reproduce `cfg687_results.json` to ≤ 1e-6.
- **K2:** CFG903's stored two-halo vectors `T2h_primary` (both footings, 4 bins × 15) are reproduced from CFG903's committed
  histograms through this lane's exec of CFG903's kernel / exclusion code at the stored r_x: max |Δ| ≤ 1e-9 M☉ pc⁻².
- **K3:** the kernel at CFG687's edges passes CFG903's K2b limits (≤ 1e-6) and K2c: a uniform neighbour field gives
  |ΔΣ_bin| ≤ 2e-3 Σ₀ in all 8 bins (log M_b 10.5 and 12.0, P1, both footings).
- **K4:** random halves A − B (even / odd clones): the W-weighted OUTER stack of ΔΣ_A − ΔΣ_B lies within 3σ_jk of zero (primary,
  both footings).
- **K5:** ν_s solves μ(x) x = y with μ = x/(1+x) to ≤ 1e-12 on y ∈ [1e-4, 1e4].
- **MUTATE** (`CFG967_MUTATE=1`, separate `_MUTATE` outputs): amplitude × 0 must reproduce the "before" numbers exactly (equal
  arrays) and, for ν_mono, CFG687's JSON to ≤ 1e-6. Amplitude × 2 **bites** if |s(×2) − s(×0)| ≥ 0.01 and
  |s(×2) − s(×0)| > |s(×1) − s(×0)| on both footings. If it fails only because the term is too small, that is reported as such.

## 9. Compute and limits

- One process at a time, OMP_NUM_THREADS = 1, `nice -n 10`, in-script watchdog stopping at 0.95 GB current RSS. Stage A
  (`cfg967_pairs.py`: pairs, kernels, per-cluster tables) writes to `../_external_data/cfg967_work/` (not committed);
  stage B (`cfg967_score.py`) scores.
- Not modelled: the true-z lensing efficiency of neighbours; photo-z mass errors; catchment sharing (per-galaxy catchments
  over-assign supply in groups, so the term is an upper bound in that respect); mass not attached to catalogued galaxies
  beyond C1′/C2′; anisotropy of the cluster's own field.
- The census f_ret is an observational input carried in the record, not derived.

κ = ½ FITTED; footings never pooled; framework-native; not theory closed.
