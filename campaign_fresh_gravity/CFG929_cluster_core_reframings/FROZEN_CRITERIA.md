# CFG929: four small reframings of the cluster-core excess (FROZEN, before any script or new number)

- **Block:** CFG920–929 (LEDGER row 663: "CFG929 = small reframings for the cluster-core excess"). Date 2026-10-20.
- **Label:** HYPOTHESIS TEST (four reframings, pre-registered), each with zero new constants. Owner request: "small reframing
  possibilities".
- **Settings:** κ = ½ FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. Extra mass is "cold energy",
  never a particle. Raw data and framework-native models only: no HMcode, BAHAMAS, ΛCDM mass function or halo template enters any
  verdict. Not "theory closed". Nothing here may say the data favour the framework. NO EFFECT and BREAKS are reported as plainly
  as RESOLVES. Any post-freeze change is a dated, labelled amendment in the README.

## 0. What I read before freezing (targeted, disclosed) and what I expect
- **READMEs / criteria:** CFG922 (criteria, README, `cfg922.py` in full, K and MUTATE outs), CFG686 (README; the grid and projection
  lines of `cfg686_shear.py`), CFG687 (README, criteria, `law()` in `cfg687_stack.py`), CFG726 (README), CFG727 (README, criteria),
  CFG808, CFG809, CFG815 (READMEs), CFG916 (README to the D section), CFG921 (README to the A1 diagnostics), CFG925 and CFG926
  (README heads), CFG634, CFG651, CFG652 (README heads), CFG640 (README; `cfg640_split.py`; `cfg640_split.out` tail; the
  cooling-rule source lines 535–575 and constants lines 66–90 of `cfg640_pm.py`, read as text only), CFG650 (README),
  CFG468 (README), CFG903 and CFG805 (README heads), CFG4 (`CFG4_common.py` kernels; `CFG4_galaxy_law.py` lines 66–244; the
  committed `CFG4_galaxy_law.out`; the head of the committed `CFG4_clusters.out`), THEORY_CANONICAL_2026-10-18.md (whole),
  THEORY_CANONICAL_2026-10-16.md (to line 80), the 10-14 file (grep for clusters / condensed).
- **Numbers seen before freezing (stored, not recomputed):**
  - Excess (ν_s, CFG916 LR-c = plain law): eRASS1 MID 1.9068 ± 0.1184 / 1.7510 ± 0.1087, OUTER 1.0109 ± 0.0868 /
    0.9258 ± 0.0795; ACCEPT MID 1.6862 / 1.5622, OUTER 1.019. CFG687 (ν_mono) MID 1.9102 / 1.7536, OUTER 1.0118 / 0.9265;
    Newtonian MID 10.17 ± 0.65.
  - CFG922: concentrated extra needed λ = 2.2369 / 1.8444 × gas_cyl; A1 census central MID 2.060 / 1.890; S_up ~ 9.5e11, S_cen
    ~ 3.5e11 M☉ (medians); every baryon component CANNOT; any baryon fix overshoots OUTER.
  - CFG727 (condensed source + free reservoir): eRASS1 MID 0.93, OUTER 1.05 (terciles 1.29 / 1.32 / 0.64), ACCEPT OUTER 0.48.
    CFG809 H-EX: MID 0.76, OUTER 0.64. CFG726 memory: MID 1.54, OUTER 0.76. CFG640 split: f_c − 0.10 ≤ 5.9e-4 for every mass and
    z ≤ 2; brackets χ(r_M) 0.03–1, χ(age) ≤ 0.06.
  - CFG4 SPARC (weighted rms, Υ profiled): P2 0.108272 @0.70 / 0.103549 @0.65; ν_mono 0.100329 @0.61 / 0.099103 @0.57;
    ν_β best β 0.4847 (rms 0.101143, Υ 0.44) / 0.5533 (0.100433, Υ 0.46), 95% band [0.3974, 0.5912] / [0.4537, 0.7705].
    CFG468: SPARC Δχ² vs ν_mono (T-free / T-fix): simple +12.8 / −7.0, standard +242 / +408, ν_RAR −30.2 / −1.1, P2 +138 / +139;
    ν/ν_mono at y = 0.05 / 1 / 3: simple 1.002 / 1.023 / 1.038, standard 0.907 / 0.804 / 0.862, ν_RAR 1.000 / 1.000 / 0.998.
- **Hand estimates made before freezing (disclosed; they protect against over-claiming):**
  - (a) Every declared ν has the deep limit y^−½. They differ only in the offset: ν_s and ν_e ≈ y^−½ + ½; P2 and ν_2 ≈ y^−½;
    ν_β(β < ½) ≈ y^−½ + y^(β−½)/(2β). At y ≈ 0.02 / 0.005 (MID / OUTER) ν_β(0.48)/ν_s ≈ 1.08 / 1.04 and ν_β(0.40)/ν_s ≈ 1.18 / 1.11.
    Expected: ν_e, ν_mono NO EFFECT; P2, ν_2 WORSENS; ν_β at the record's best β NO EFFECT (~15% removed); the β = 0.40 band edge
    possibly PARTIAL, with its SPARC Υ below the H2 window.
  - (b) **Theorem (written before any number).** In the record's settled field (QUMOND, CFG921 P5) the lensing mass inside a
    cluster-centred sphere is the flux M_L(<r) = (r²/G)⟨ν(|g_N|/a0) g_N·r̂⟩ (the curl part carries no flux). To first order in a
    member's field δ, the flux change is (1/4πG)∮[ν + gν′](g_s) δ_r dA = [ν + gν′](g_s(r)) × m_enc: exactly the smooth model's
    response. Clumpiness therefore enters only at second order and in the members' nonlinear near zones; in the deep regime the
    second-order coefficients are negative (−ν/8g for δ_r², −ν/4g for δ_⊥²). Expected: NO EFFECT, tiny and negative. The algebraic
    bracket (each member keeps its own isolated halo, Σ ν(g_i) g_i) gives ΔM_L/M_L ≈ ½ f_mem ≈ 8% with the baseline stars, i.e.
    ~15% of the excess: NO EFFECT.
  - (c) **Shell theorem.** In a stacked (spherically averaged) profile, mass at 3D radius s > R contributes ΔΣ(R) ≤ 0, in Newton and
    under the spherical law (the law changes M_L only outside s). Only mass physically inside R can raise MID. Expected: NO EFFECT;
    the X-ray neighbour term small or negative.
  - (d) **Monotonicity.** Condensed ⊂ all baryons at every r, and h(y) = y(ν − 1) is non-decreasing for ν_s and ν_mono (CFG468:
    h′ ≥ 0). So M2's settled cold energy ≤ the plain law's at every r, for any amount of cooling: the module cannot remove any of
    the excess through its settled part. Expected: the M2 reading BREAKS OUTER (hot gas stops sourcing); the cooled mass is tiny.
- **Already tested, not redone:** the unsettled-reservoir reading of the condensed source (CFG721/727, CFG652, CFG634); merger
  memory of member halos (CFG726, CFG916); expelled-gas free cold energy (CFG808/809/815); IMF and fossil a0 on clusters (CFG926);
  baryon census (CFG922). Their stored numbers are quoted, never re-graded.

## 1. Common harness
- **Samples:** eRASS1 318 (`cfg687_percluster.npz`), decisive. ACCEPT 8 (`cfg686_results.json`), reported with no class weight.
- **Baseline baryons:** CFG687 / CFG916: β-model gas (β = 2/3, r_c = 0.15 R500, normalised to Mgas500, cut at 3 Mpc) with stars
  f* = 0.20 ∝ gas (gas × 1.2); ACCEPT: CFG686's gas × 1.2. Engine, projection and band amplitudes are CFG922's (exec'd read-only
  from `cfg922.py`, the slice from `def nu_s` to the census header; never its output-file lines).
- **Bands:** A = Σ W ΔΣ_obs / Σ W ΔΣ_model; MID = bins 3–5 (0.556, 0.808, 1.175 Mpc), OUTER = bins 6–7; σ by CFG687's 30-patch RA
  jackknife (eRASS1) or CFG686's bootstrap (ACCEPT). Z = (A − 1)/σ.
- **Kernel:** ν_s (g_N = g²/(g + a0), the law as stated) decides (b)–(d); ν_mono is the bracket. A different ν_mono class marks
  the reframing FRAGILE (kernel). For (a) the kernel is the reframing.

## 2. Classes (per reframing, per footing; eRASS1 decides; both footings must agree, else SPLIT with both shown)
- f_rem = (A_MID,base − A_MID,new)/(A_MID,base − 1), with A_MID,base the same kernel-and-footing baseline (for (a): ν_s).
- **OUTER kept:** |Z_OUTER,new| < 2 (the baseline has |Z| < 2 on both footings). **SPARC kept:** the reframing's SPARC rule (§3).
- **BREAKS SOMETHING:** OUTER not kept or SPARC not kept. This overrides every other class; f_rem is still reported.
- **RESOLVES:** |Z_MID,new| < 2, OUTER kept, SPARC kept.
- **PARTIAL:** f_rem ≥ 0.25, OUTER kept, SPARC kept, not RESOLVES.
- **NO EFFECT:** −0.25 < f_rem < 0.25, nothing broken.
- **WORSENS** (declared extra label): f_rem ≤ −0.25, nothing broken.
- **Brackets:** if a declared bracket's class differs from the primary's, the reframing is BRACKET-DEPENDENT (both shown).
- **Bounds:** where a computed quantity is an upper bound rather than a prediction (c-G below), a bound that removes ≥ 25% is
  graded NOT DECIDED (bound only), never PARTIAL or RESOLVES.

## 3. The reframings
### (a) Interpolation-function family (every ν declared in the record)
- **Kernels:** ν_s (= ν_1 simple; the baseline); ν_e = ν_RAR = 1/(1 − e^−√y) (CFG4_common, CFG921/925); ν_mono (FP1 via
  CFG4_common); P2 = √(1 + 1/y) (the framework postulate); ν_2 standard = e^(asinh(y/2)/2)/√y (CFG468); ν_β(y) =
  (1 + y^−β)^(1/2β) at the record's stored SPARC best β (0.4847 canonical / 0.5533 alt; CFG4 H3), primary for the family. The
  stored 95% band edges (0.3974 / 0.5912 canonical; 0.4537 / 0.7705 alt) are brackets. Excluded, stated: the CFG468 splices S1/S2
  (identical to ν_mono at every observed y) and the CFG468 kinked kernel (a control, not a candidate).
- The kernel replaces ν_s everywhere in the cluster law (baseline baryons). Each kernel is graded on its own; the (a) answer is
  the best class among the primary kernels (seven chances, disclosed).
- **SPARC rule:** CFG4's statistic (exec'd read-only from `CFG4_galaxy_law.py`, data and `sums`/`best`), at the framework a0 per
  footing, one global Υ_disk: SPARC kept ⇔ min over Υ_disk ∈ [0.50, 0.80] of the weighted rms ≤ 0.110 dex (CFG4 H2's threshold
  and window). The full-grid optimum and CFG468's stored Δχ² class are reported, no class weight.
### (b) Superposition / clumpiness
- **b-QUMOND (primary).** Per member clump i (Hernquist, R_e = 15 kpc, CFG922's BCG convention) at 3D radius r_i in the smooth
  host (the full baseline baryons, field g_h), the exact nonlinear flux correction through each cluster-centred sphere,
  q_i(r) = (r²/G)·½∫[F(host + clump) − F(host) − f′(g_h) g_c,r] dμ, F = ν(|g|/a0) g_r, f(g) = gν(g/a0), computed as a 1-D
  axisymmetric integral (variable d = |x − x_i|, log-spaced). ΔM_L(r) = Σ w_i q_i(r) is added to the baseline's law M_L and
  re-projected with CFG922's projection algebra. The first-order term is zero by the theorem of §0 (in expectation over the
  template placement), so it is not added. Clump–clump overlaps are neglected (their incidence is reported).
  - **Members (primary): the A1 census central** (`cfg922_census_A1.json`: S_cen − bcg_med per cluster), 3D-distributed ∝ the gas
    template (CFG922; projected mass inside 0.5 Mpc = S_cen − bcg_med, 3D to 3 Mpc), masses drawn from CFG922's declared central
    Schechter shape (α = −1.0, log M_char = 11.0) above each cluster's stored M_lim(z); the mass below M_lim stays smooth; seed 929.
  - **Brackets:** A1 upper (S_up − bcg_sup, α = −1.5); MAX = the baseline's whole stellar component (0.20 × gas to 3 Mpc) in clumps
    of exactly M_char = 10¹¹ M☉.
- **b-ALG (declared upper bracket; the literal Σ ν(g_i) g_i).** Each member keeps its own isolated law halo out to its equality radius
  r_e,i (its Newtonian field = the host field), i.e. contributes m_i ν(g_h(r_i)/a0) instead of the smooth response f′(g_h) m_i:
  M_L^ALG(<r) = M_L,law(all)(<r) + ∫_0^r [ν(g_h) − f′(g_h)] dM_mem. Members = the baseline's whole 0.20 × gas stellar component
  (generous: CFG922 measured ×2.5–7 fewer); A1 central and upper reported. Halos end at r_e,i (median reported against CFG726's
  supply edges 175–886 kpc), so no outer memory is reintroduced.
- (b)'s class comes from b-QUMOND; b-ALG is its upper bracket (BRACKET-DEPENDENT if the classes differ).
- **SPARC:** unchanged by construction (an isolated galaxy's own field is untouched; the members-in-host term does not exist for
  SPARC discs).
### (c) Projection / line-of-sight structure
- **c-X (computed): eRASS1 X-ray neighbours.** Every other row of the eRASS1 main table (`erass1_main.tsv`, valid z, Mgas500, R500)
  within 5 Mpc projected (at the target's BAO-raw D_A) and |Δz| ≤ 0.05(1 + z_t) (CFG922's census window). Each neighbour's
  baseline law profile (own Mgas500/R500, gas × 1.2, the reframing's kernel) is projected on its own scale, mapped to the target's
  angular scale, azimuthally averaged around the target, and its ΔΣ added. Σ_crit ratio set to 1 inside the window (generous).
  The target itself is excluded by position (< 0.1′) and |Δz| < 1e-3.
- **c-G (computed upper bound): KiDS bright galaxies.** With CFG922's A1 masses and its census algebra (photo-z window, 2.5–5.0 Mpc
  annulus background, upper = MASS_SUP + 2σ_bkg, c_up for non-BCG, A1 coverage rule), the projected member stellar mass S_up(R)
  inside R = 0.5, 0.556, 0.808, 1.175 Mpc. LOS extra X = max_R max(0, S_up(R) − 0.20 gas_cyl(R)). Bound: 6X (the record's
  f* = 0.20 baryon-per-star convention; ×1 reported) placed as a central Hernquist mass (R_e = 15 kpc), the placement that
  maximises the MID ΔΣ per unit mass. Graded as a bound (§2).
- **Primary (c) = c-X + c-G (×6) together.** The shape bound (the largest MID removal the c-X / c-G templates allow before OUTER
  reaches Z = −2) is reported, no class weight.
- **SPARC:** unchanged (a lensing-stack term for clusters only).
### (d) The record's cooling / condensed-source module (CFG640 / M2)
- **Inputs (CFG640, exec'd read-only from the source text of `cfg640_pm.py`: `lam_cool` and its constants; `chi_cool` for K5):**
  Λ(T) Tozzi & Norman Z = 0.3 Z☉ with CFG370's normalisation; μ = 0.6, n_e/n_H = 1.17, n/n_H = 2.3; T = μ m_p V²/2k with
  V⁴ = G M_ret a0, M_ret = the cluster's model baryons inside 3 Mpc; t_cool(r) = 3(n/n_H)kT/(2(n_e/n_H) n_H Λ), n_H from the
  measured β-model gas density.
- r_cool = the largest r with t_cool(r) ≤ t_ref(r). Primary t_ref = r/V (CFG640 K2); bracket t_ref = 1/H(z) (CFG640's age
  bracket, its E(a)). M_cool = M_gas(<r_cool). Reported against the needed λ × gas_cyl.
- **d-M2 (primary):** theory-v2's source rule: settled cold energy = the law phantom of condensed baryons only,
  M_L(<r) = M_b,all(<r) + M_c(<r)[ν(G M_c/r²a0) − 1], condensed = the baseline stars (0.20 × gas, CFG727's convention) + the
  cooled gas (gas profile inside r_cool). A1 census central stars instead of 0.20 × gas are reported.
- **d-plain (reported):** under the all-baryon source cooling only relabels phase, so A is unchanged (identity, verified).
- The reservoir reading (CFG727) is not re-run; its stored numbers and the sign of the cooling rule's change to its condensed mass
  are reported, no class.
- **SPARC:** unchanged (no hot gas in the SPARC rotmod; CFG634 T1 Δ = 0).

## 4. Controls
- **K1 CFG687:** ν_mono baseline A_MID / A_OUTER ± σ, both footings = stored (< 1e-6).
- **K2 CFG916 LR-c (= plain law, ν_s):** eRASS1 and ACCEPT A_MID / A_OUTER ± σ, both footings = stored (< 1e-6).
- **K3 CFG922 A1:** baseline_f020 and census_central MID / OUTER (eRASS1, ν_s, both footings) = stored (< 1e-6) from the stored
  census; at the stored λ the U-λ model gives A_MID = 1 (< 1e-6).
- **K4 CFG4 SPARC:** P2 and ν_mono rms and Υ (both footings) and the ν_β best-β rms = stored (< 1e-9 in rms, exact Υ).
- **K5 cooling:** this lane's t_cool / r_cool code, fed CFG640's isothermal catchment profile, reproduces the exec'd `chi_cool`
  on a grid of masses, redshifts and both footings (< 1e-9 relative).
- **K6 kernels:** ν/ν_mono at y = 0.05 / 1 / 3 for ν_s, ν_2, ν_RAR = CFG468's printed values (to 0.0005).
- **K7 census code (c-G):** at R = 0.5 Mpc the profile code reproduces the stored A1 net_sup, sig_sup and net_med for all 318,
  and bcg_sup / bcg_med for the clusters with coverage ≥ 0.5 (A1 overwrites the others), to < 1e-9 relative.
- A failed K voids the piece it guards (stated in the README); no silent fix.
- **MUTATE** (separate `_MUTATE` outputs; each arm must bite or hold):
  - Ma: a0 × 10 moves every kernel's eRASS1 A_MID by > 5σ; a0 → 0 gives the stored Newtonian A_MID 10.17 (< 1e-3 relative).
  - Mb1: b-ALG with the members smoothed (no own halos) = the plain law (< 1e-12). Mb2: b-QUMOND with every clump mass × 1e-3
    (weights × 1e3) shrinks |ΔM_L| at 0.8 Mpc by ≥ ×10 (smooth limit → 0). Mb3: a single 10⁶ M☉ clump gives |q|/(f′m) < 1e-3
    (the linear cancellation); a single 10^12.5 M☉ clump at 0.8 Mpc gives a non-zero q there (bites).
  - Mc1: a planted copy of the target at 2 Mpc offset (same z) gives ΔΣ ≤ 0 at R < 2 Mpc (shell sign) and > 0 beyond; a planted
    copy at 0.1 Mpc raises A_MID's model (bites). Mc2: c-G at 318 random positions (1–3° away) gives a mean net stellar mass within
    3 standard errors of 0.
  - Md: χ = 1 (all gas condensed) reproduces the plain law (< 1e-12); r_cool forced to 3 Mpc reproduces it too; χ = 0 gives
    condensed = stars only.

## 5. Machine and hygiene
- One process at a time, OMP_NUM_THREADS = 1, nice 10, each process < 1 GB (the KiDS read streams chunked columns with a plain
  FITS-header parser, no memory map; peak RSS printed). Nothing downloaded. Never touches running processes.
- Outputs: `cfg929.py`; `cfg929_K.out` + `cfg929_K.json`; `cfg929_MUTATE.out` + `cfg929_results_MUTATE.json`; `cfg929.out` +
  `cfg929_results.json`. Commits with explicit paths; no push.

κ = ½ fitted; footings never pooled; cold energy mass still required; not theory closed.
