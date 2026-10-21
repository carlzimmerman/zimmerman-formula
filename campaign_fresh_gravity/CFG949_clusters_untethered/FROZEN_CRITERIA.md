# CFG949: clusters as UNTETHERED cold energy (H-UT). FROZEN, before any script or new number

- **Block:** CFG940–949 (LEDGER row 665 reserves CFG949: "clusters as UNTETHERED cold energy … one parameter-free test of the
  core excess AND the outer M^0.9 scaling"). Date 2026-10-20.
- **Label:** HYPOTHESIS TEST, POST HOC (H-UT was formed after CFG686/687/688, CFG721/726/727/777/808–812, CFG916, CFG922,
  CFG929, CFG930, CFG932 and CFG941 were read). Zero new fitted constants; every input is a record convention, declared below.
- **Settings:** κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻² are never pooled. The extra mass is "cold energy", the
  framework's own cold component; no particle species is added. Framework-native inputs only: no HMcode, BAHAMAS, ΛCDM mass
  function, ΛCDM-simulation c(M) relation or halo template enters any verdict. Not "theory closed". Nothing here may say the data
  favour the framework. FAILS is reported as plainly as EXPLAINS.

## 1. What I read before freezing (targeted, disclosed)
- READMEs: CFG686, CFG687 (+ criteria, `cfg687_stack.py` in full), CFG922 (+ criteria; `cfg922.py` lines 1–200: CFG686/687
  exec slices, vectorised engine, `Stack`), CFG941 (+ DERIVATION §1–5), CFG932 (README; `cfg932.py` lines 1–330 and the main
  loop header), CFG930 (criteria §3–4.1, README results table; `cfg930.py` lines 60–228 and 259–268, 571–600), CFG727, CFG777,
  CFG808 (`cfg808.py` lines 1–216), CFG637 (README head), CFG934 (criteria §2.2–2.3).
- LEDGER rows: CFG686, 687, 688, 721, 726, 808–812, 817, 916, 920–929 / 930–939 / 940–949 reservations, 921, 922, 926, 929,
  930, 932, 932-audit, 934, 936, 938, 939, 940, 941.
- `cfg686_shear.py` lines 1–114 (constants, distances, RGRID 1e-3–30 Mpc × 3000, U_GRID, `sigma_proj`, `law_dsigma`, SIS test).
- Data structure only: CFG654 `cfg654_delta_ta_cmb.json` (z nodes 0, 0.25, 0.5, …; Δ_ta(0) = 11.898), `cfg654_ics_tables_cmb.npz`
  key list; CFG652 model constants (COLD_PER_B 5.364, F_COND_FLOOR 0.10, F_RET_XCOP 0.90).

## 2. Numbers seen before freezing (disclosed)
- CFG687 stored (ν_mono, β 2/3, r_c 0.15 R500, f* 0.20): A_MID 1.9102 ± 0.1186 / 1.7536 ± 0.1089, A_OUTER 1.0118 ± 0.0869 /
  0.9265 ± 0.0796; Newton (a0 → 0) MID 10.17 ± 0.65, OUTER 7.26 ± 0.62; T2 s_obs 0.8958 ± 0.2093, s_law 0.4658, s_Newton
  0.8361; tercile median Mgas500 3.69e12 / 1.16e13 / 2.92e13 M☉; n = 318.
- CFG916/922 ν_s: eRASS1 MID 1.9068 ± 0.1184 / 1.7510 ± 0.1087. CFG688: λ-binned outer slope 1.01 ± 0.29 vs Mgas-binned
  0.42 ± 0.14 on the same 76 clusters (mass scaling NOT SETTLED).
- CFG932 cluster-core (M_ta 1.645e15, f_ret 0.90, r_ta 9414 kpc, r_obs 500 kpc): c_ta 3.96 / 8.58 / 11.44 / 15.11 (PS1, EPS 0.2 /
  0.05 / 0.01); native cold inside 500 kpc 2.95 / 6.35 / 8.38 / 10.84 e13 M☉ vs law phantom 5.99e13 (can) / 6.73e13 (alt) and
  baryons 3.41e13; X_ret (max of phantom and native) −0.00 / +0.020 / +0.098 / +0.181 dex (can), 0.00 / +0.006 / +0.065 / +0.148
  (alt).
- CFG930 median cluster (M_b = 1.2 × median Mgas500): M_ta 1.221e14 (census f_ret); native debris inside a 0.5 Mpc cylinder
  3.99e13 M☉ (C 3000, r_ta) and 1.10e14 (C 6000, r_vir, ×2); CFG922 needed extra 2.43e13 (window 1.76–3.11e13). CFG930 graded
  clusters only as "law + debris" (N-B, over-predicted) and never as debris without the law (R1 cluster NOT EVALUATED).
- CFG727 (hot-gas share free, Method A placement): eRASS1 MID 0.93, OUTER 1.05 but tercile cancellation; CFG809 (expelled share
  free) overshoots (MID 0.76, OUTER 0.64); CFG721 cond source s 0.88 / 0.76.
- **Hand estimate (before freezing, disclosed):** for a median eRASS1 cluster (Mgas500 1.2e13, pipeline gas to 3 Mpc ≈ 4.5 ×
  Mgas500, census f_ret ≈ 0.9, M_ta ≈ 4.6e14, NFW c_ta ≈ 27 at C 3000), the untethered model's 3D mass is ≈ 1.5 × the law's at
  0.8 Mpc and ≈ 0.75 × at 2 Mpc. Expectation: core excess largely absorbed, outer possibly short; the outcome is not known. This
  is why the class rule below requires BOTH bands and the slope, and why supply and collapse brackets are wide.

## 3. Prior tests and why this one is new
- CFG727/808/809/721/637: a tethered law profile is kept for some or all baryons and only an overflow is free, placed by CFG637
  Method A (secondary infall in the total potential). CFG930 N-B: the law PLUS all native debris (double count). CFG932 Q2:
  max(phantom, native) at one representative cluster, 3D at 0.5 Mpc. **No lane has scored "cluster mass = baryons + the whole
  cosmic-ratio cold supply as untethered native collapse debris, with no law boost on the cold part", per cluster, on both bands
  and the T2 slope.** That is H-UT (reading B0 below).
- Theorem D-T (CFG941): a tethered medium whose phantom is its own mass has no self-gravity and no mutual gravity. Untethered cold
  energy is ordinary self-gravitating cold matter (CFG649/654: before collapse it is cold collisionless matter at Ω_c/Ω_b = 5.364).
  H-UT: in clusters (hot, merging, never in tethered equilibrium) none of the cold energy is tethered on cluster scales.

## 4. Data, harness and engine (reused read-only)
- **Clusters and shear:** CFG687's `cfg687_percluster.npz` (D, E, mg = Mgas500 [M☉], R500 [Mpc], z, ra, dec, PL, PN), 318
  eRASS1 clusters. Weights 1/E², bands MID = bins 3–5 (R 0.556, 0.808, 1.175 Mpc) and OUTER = bins 6–7; 30 equal-count RA patches,
  jackknife. A = Σ W D / Σ W P per band.
- **T2 slope:** CFG687's own statistic: Mgas500 terciles, OUTER stack Σ W·X / Σ W per tercile, slope of log10(stack) vs
  log10(median Mgas500); s_obs ± jackknife from D; s_model from the model arrays through the same function.
- **Engine:** CFG922's vectorised projection (exec'd from `cfg922.py` text with CFG686's exec'd setup; identical algebra to
  CFG687 `law()`), used verbatim for every LAW component.
- **Truncation-aware projection (declared deviation for Newtonian components):** CFG686's `sigma_proj` interpolates log ρ over
  positive cells only, so beyond a truncation radius it holds the last positive density constant out to 30 Mpc. A law profile is
  never truncated (its phantom density stays positive), but a Newtonian profile is (gas at 3 Mpc, cold NFW at r_b). For every
  Newtonian component this lane uses the same vectorised algebra with log ρ floored at 1e-300 in every row (no clamped fallback),
  so a truncated density projects as zero beyond its edge. K5 validates it. The record's own projection is kept for the K/MUTATE
  reproductions of stored numbers, and the effect on CFG687's stored Newton column is reported (K4b, no class weight here).
- **Baryons (CFG687 pipeline, primary):** β-model gas, β = 2/3, r_c = 0.15 R500, normalised to Mgas500 at R500, cut at 3 Mpc;
  stars f* = 0.20 × M_gas(<r). M_ret = (1 + f*) M_gas(<3 Mpc). Variants (one at a time, reported): β 0.6 / 0.8; r_c 0.10 / 0.20
  R500; f* 0.10 / 0.30.

## 5. The H-UT model (framework-native, parameter-free)
### 5.1 Supply (cosmic-ratio catchment)
f_b = 1/(1 + 5.364). M_c = (1 − f_b) M_ta = 5.364 × catchment baryons.
- **S-cen (primary):** M_ta solves M_ta = M_ret/(f_ret(M_ta) f_b), with the record's census f_ret (CFG416/CFG804 `fret_of`,
  verbatim as CFG930's `mta_fixed`, log M_ta in M☉: 0.10 below 12.5, linear to 0.55 at 13.5, +0.30/dex, cap 0.90).
- **S-floor:** the record's cluster catchment used in CFG721/727 (`cfg652_model`): bc = max(f* M_gas/0.10, M_ret/0.90),
  M_ta = bc/f_b. (CFG812: for eRASS1 this pins f_ret at 0.60 through the condensed-floor clause; kept as the upper bracket.)
- **S-closed:** f_ret = 1 (M_ta = M_ret/f_b).
- **S-R500:** measured gas only, M_ret = 1.2 × Mgas500 (CFG930's ×1.2 convention), census f_ret (the lowest supply).
The lensing baryons are always the pipeline's (§4); only the cold supply changes between S-rules.

### 5.2 Profile: native collapse debris (NFW, truncated at r_b)
Each cluster at its own redshift z_i (declared generalisation; z_i = 0 is the record's rule, run as a variant and as K):
- **R930 family (primary; CFG930/CFG934 rule):** ρ_s = C ρ̄_m(z_c), C ∈ {1500, **3000**, 6000}. z_c from NFW97's EPS half-mass
  condition with f = 0.01, δ_c = 1.686, observed at z_i: D(z_c) = 1/[1/D(z_i) + 0.67449 √(σ²(0.01 M_ta) − σ²(M_ta))/δ_c] (z_c ≥ z_i
  by construction). σ(M), D(z), Om, Or, OL, h from CFG654's `cfg654_scorer_tables_cmb.npz` with CFG930's P(k) extension.
  Boundary: **r_ta(z_i)** (primary), mean density Δ_ta(z_i) ρ̄_m(z_i), Δ_ta interpolated linearly in ln(1+z) between the
  `cfg654_delta_ta_cmb.json` nodes; bracket r_vir(z_i) with Δ_vir = 8 Δ_ta(z_ta)[(1 + z_ta)/(1 + z_i)]³, t(z_ta) = t(z_i)/2
  (native background). Concentration: m(c)/c³ = Δ_b(z_i)(1 + z_i)³ / [3 C (1 + z_c)³].
- **R932 family (bracket; CFG932 `conc`):** mean density inside r_s = 18π² ρ̄_m(z_s); z_s from EPS with progenitor fraction
  F ∈ {0.2, 0.05, 0.01} or PS1, CFG932's ics-table σ(M) and power-law extension, generalised to z_i (δ_c/D(z_i) offset; z_s ≥ z_i);
  boundary r_ta(z_i). Profile corners: 3 C × 2 boundaries + 4 R932 cusps = **10**.
- Cold mass: M_c,NFW(<r) = (1 − f_b) M_ta m(min(r, r_b)/r_s)/m(c), m(x) = ln(1+x) − x/(1+x). No adiabatic contraction, no
  settling (declared).

### 5.3 Readings (does anything get a law boost?)
- **B0 (primary = H-UT as posed):** no tethered cold energy on cluster scales, hence no phantom (the phantom IS tethered cold
  energy). M_lens = M_b + M_c,NFW, all Newtonian. Footing-independent. Member galaxies' own tethered halos are part of the same
  cold budget and sit inside ~0.1 Mpc of each member; their placement does not change M_c and is not modelled.
- **B1 (ICM and galaxies tethered, budget-conserving):** the record's law on all baryons (ν kernel, per footing) plus the
  untethered remainder max(M_c − M_ph(<r_b), 0) in the R930/R932 NFW shape. (Close to CFG808's pooled reading.)
- **B2 (galaxies tethered, ICM not):** law on the stars only (f* × gas shape, CFG687's placement; ν per footing), gas Newtonian,
  remainder max(M_c − M_ph,*(<r_b), 0) as NFW. (CFG727's split with native placement instead of Method A.) Caveat: CFG941 R2 says
  free mass would enter a tethered equilibrium's argument (R(u) = g_b + g_f); B1 brackets that larger-boost direction.
- Kernel for B1/B2: ν_s (g_N = g²/(g + a0)) primary, ν_mono bracket. Both footings, never pooled.

## 6. Classes (decided on B0, primary corner: S-cen, R930 C 3000, r_ta, z_i, primary baryons)
Three tests, each at 2σ (jackknife σ of the model's A; s_err from CFG687's jackknife of s_obs):
- **T-MID:** |A_MID − 1| < 2σ. **T-OUT:** |A_OUTER − 1| < 2σ. **T-S:** |s_obs − s_HUT| < 2 s_err.
- **H-UT EXPLAINS:** all three pass.
- **PARTIAL:** at least one of T-MID / T-OUT passes but not all three (which ones are stated).
- **FAILS:** neither T-MID nor T-OUT passes. T-S alone cannot rescue it: Newtonian baryons alone (s 0.84) already pass T-S, so
  the slope test is not diagnostic without the amplitudes.
- **Per footing:** B0 contains no a0, so its class is the same number on both footings (stated as such). B1/B2 get their own
  classes per footing and kernel (reported, they do not change the H-UT class).
- **Robustness:** ROBUST if all 40 B0 corners (10 profiles × 4 supplies) at z_i give the primary class; otherwise FRAGILE, with
  the counts per class. One-at-a-time variants (z_i → 0, β, r_c, f*) are reported and counted separately.

## 7. Diagnostics (no class weight)
- λ_MID, λ_OUT: the multiplier on M_c (B0, primary profile shape) that makes A_MID = 1 and A_OUTER = 1 (root in [0, 100]);
  equal λs mean the shape is right and only the normalisation is off.
- A_MID/A_OUTER (law: 1.89 / 1.89); tercile A_MID, A_OUTER; median z_c, c, r_s, r_b, M_ta/M_ret, f_ret.
- Projected B0 excess inside 0.5 Mpc against CFG922's needed extra; the B0 analogue of CFG932's X_ret for CFG932's own cluster.
- **ACCEPT 8 (CFG686; reported, no class weight):** B0 A_MID / A_OUTER with CFG686's bootstrap replay (CFG922's `Stack`).
- **Galaxy side (Task 3):** for the median cluster, ρ_c,NFW at R = 0.25 / 0.5 / 1 Mpc, and M_c(<10, 30, 100 kpc) around a member
  at those radii over a 5e10 M☉ member's baryons (Hernquist a = 3 kpc) — the fraction by which the member's law argument would
  change if the local untethered mass enters it (CFG941 R2). The link to CFG945 (satellite hover) is stated qualitatively only;
  CFG945's directory is not read or touched.

## 8. Controls
- **K0 units:** npz Mgas500 in M☉ (median ≈ 1.2e13), R500 in Mpc; Δ_ta nodes reproduced exactly; D(0) = 1.
- **K1 CFG687:** CFG922's engine with ν_mono reproduces stored PL (max rel < 1e-9) and A_MID/A_OUTER ± σ canonical and alt
  (< 1e-6); s_obs, s_law, s_Newton (< 1e-6).
- **K2 CFG916/922 ν_s:** eRASS1 MID 1.9068 ± 0.1184 / 1.7510 ± 0.1087 (to the stored digits, < 1e-4 vs CFG922's K json).
- **K3 CFG932:** this lane's R932 profile code at z = 0 with CFG932's own supply and f_b reproduces its stored cluster-core M_ta,
  c_ta, r_ta, r_s and native cold inside r_obs (rel < 1e-6) at the 4 cusps; X_ret recomputed from those within 1e-6 dex of the
  stored +0.02…+0.18 (both footings).
- **K4 CFG930:** this lane's R930 profile code at z = 0 reproduces CFG930's stored median-cluster M_ta and projected debris
  inside 0.5 Mpc (m2 = M2D/(1 − f_s)) for C 3000 r_ta ×1.2 and C 6000 r_vir ×1.2 (rel < 1e-3, numerical projection).
  **K4b (report):** CFG687's Newton column recomputed with the record's projection equals stored PN (< 1e-9); the
  truncation-aware projection's baryons-only A is reported next to it, flagged if it differs by > 5%.
- **K5 projection:** the truncation-aware projection of an untruncated NFW (c 5, r_s 0.4 Mpc, 1e15 M☉ to 30 Mpc) matches the
  analytic Wright–Brainerd ΔΣ in the 8 bins (< 1%); a truncated NFW (r_b 5 Mpc) matches an independent scipy `quad` projection
  (< 0.5%).
- A failed K voids the piece it guards, stated in the README; no silent fix.
- **MUTATE** (`CFG949_MODE=MUTATE`, separate `_MUTATE` outputs; each arm must bite or hold as stated):
  - **MT tethered limit:** cold part replaced by the law's phantom (= the law on the baryons, ν_mono): A equals CFG687's stored
    values (< 1e-6), and with D replaced by that prediction A = 1 (< 1e-12). Must move A away from the B0 values.
  - **M0 cold × 0:** baryons-only Newtonian; with the record's projection A_OUTER = stored 7.26 (< 1e-6); the truncation-aware
    value is reported (A_OUTER must stay > 3, i.e. Newton badly short).
  - **MI injection:** mock D = B0 primary prediction with M_c × 1.5; noiseless recovery λ_OUT = 1.5 (< 1%), noisy recovery (Gaussian
    from the real E, seed 949) within 25%.
  - **MS shuffle:** M_c (per cluster) shuffled across clusters (seed 949): s_HUT must move by > 0.1 from the B0 value.

## 9. Machine and hygiene
- One process at a time, `OMP_NUM_THREADS=1 nice -n 10`, beside the live 1024³ job; in-script RSS guard aborts above 0.95 GB;
  stages K / MUTATE / MAIN run separately. Nothing downloaded; no other lane edited; no LEDGER edit.
- Outputs: `cfg949.py`; `cfg949_K.out`, `cfg949_results_K.json`; `cfg949_MUTATE.out`, `cfg949_results_MUTATE.json`; `cfg949.out`,
  `cfg949_results.json`; `README.md`.
- Any post-freeze change is a dated, labelled amendment in the README.

κ = ½ FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.
