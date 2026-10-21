# CFG925 FROZEN CRITERIA: three small reframings of the pressure-supported excess (A: estimator, self-sourcing, EFE sign)

Block 920–929 (reserved 2026-10-20 ~14:30 for "small reframings A"). Committed alone, before any script or number of this lane.
Kind: HYPOTHESIS TEST of three zero-constant reframings. κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are run
separately and never pooled. Raw data and framework-native quantities only. Extra mass is cold energy, never a particle. Not
"theory closed". Nothing here may be worded as "the data favour the framework".

## 0. What was read before freezing (not blind)
- THEORY_CANONICAL_2026-10-18.md with all its addenda and notes (through CFG918–923).
- CFG921 README + cfg921.py (fact list F0–F10, CFG919 re-use pattern, obs_struct / fact operators, K tests, the observed facts in
  cfg921_results.json: canonical F0 +0.856 ± 0.102, F1 +0.293, F2 +0.008, F3 +0.137, F4 +0.002, F5 +0.560 in ln units).
- CFG919 README + cfg919.py (cells, GLS, CFG828/829/849 K tests); CFG914's input section; CFG880's input section (Wolf law2,
  gas_in, sample of 83); CFG883's law+EFE code; CFG874 README + cfg874.py; CFG838 README; CFG839 header; CFG888 README; CFG478
  README; CFG828, CFG827, CFG870 READMEs; LEDGER rows for CFG884, CFG921, CFG920–929 and targeted greps (Jeans, Plummer, Wolf, EFE).
- **Earlier lanes that overlap.** No lane ran a law-Jeans σ_los for the whole dwarf sample against the Wolf estimator. CFG884 did
  whole-population Plummer Jeans for Sextans only (and noted that flat-V_c forms give σ² = V_c²/3 for every Plummer tracer; it
  also noted that the MW external field lowers all predictions). CFG858 solved stiffness BVPs for six dSphs. CFG838/842 recorded
  that the framework's external field pushes the wrong way. CFG888 decided that no record formulation lets cold energy source
  the law; CFG722 rejected that coupling (G) as double counting. These are cited and not redone; this lane quantifies.
- **Expectations formed before freezing (analytic only, no data number of this lane):**
  - R1: NO EFFECT. Deep-law virial theorem: the global σ_los⁴ = (4/81) G M a0 for any anisotropy, i.e. ~3% in σ below the
    Wolf-law value (σ_W⁴ = G M a0/18). The R_e aperture should sit close to Wolf.
  - R2: the literal fixed point has no solution; the record's closest well-defined form has an acceleration floor (expected
    WORSENS, rotators broken); the argument-only form lowers every prediction (expected WORSENS).
  - R3: WORSENS (the EFE lowers the law's prediction for satellites; CFG838/842).

## 1. Shared machinery (read-only re-use; nothing in other lanes edited)
- CFG921's source up to its "posit engines" marker is exec'd read-only (writes refused, exits trapped). That exec's CFG919, and
  through it CFG914/CFG880/CFG883/CFG687. CFG921's `obs_struct`, `fact_values`, `obs_facts`, `boot_ops`, `ols_obs` are extracted
  by AST and exec'd in the same namespace. Structure V0 = floor 0.05 dex per cell, +0.123 dex M* on n > 2 lenses.
- Facts (CFG921 definitions, ln units; dex = E/ln 10): excess facts F0 dwarfs (DW), F1 red/spheroidal lenses (LS), F5 eRASS1
  clusters (CL); rotator facts F2 blue/disc lenses (LD), F3 SPARC small (SS), F4 SPARC large (SL). Reported only: F6 cluster
  slope, F7 DW − LS, F8b dwarf slope.
- A reframing gives a per-element predicted log-shift pe = ln(g_new/g_law) (dwarfs: at r12; SPARC: per point; lenses: per bin;
  clusters: per (cluster, band), CFG921's "ΔΣ excess ≈ g excess per band" convention). Cell predictions follow CFG921's
  sec_dw / sec_sp / sec_lens / sec_cl conventions. Residual cells = observed − predicted. Residual facts come from CFG921's
  fixed GLS operators of the observed V0 structure; their se are the observed se.

## 2. The three reframings
### R1 (estimator): law-Jeans σ_los instead of Wolf
- Sample and inputs exactly as CFG880/919 (83 LVD dwarfs, Υ_V = 2, CFG874 extended-root HI disc).
- Stars: Plummer with projected half-light radius a = rhalf_sph_physical (= ¾ r12), M* = Υ_V L_V, M*(<r) = M* x³/(1+x²)^{3/2}.
- Gas: M_g(<r) = the CFG874/CFG880 gas function evaluated at radius r (the record's spherical treatment of the disc). Own copy;
  K4 checks it equals CFG880's gas_in at r12 for all 83 dwarfs.
- Law potential: g(r) = g_N(r) ν_e(g_N(r)/a0), g_N(r) = G[M*(<r) + M_g(<r)]/r². No EFE (as the baseline).
- Spherical Jeans for the Plummer tracer, p = ν_* σ_r² → 0 at infinity. Anisotropy bracket (declared):
  - J0 β = 0 (primary);
  - J1 Osipkov–Merritt β(r) = r²/(r² + r_a²) with r_a = a (the r_h of Wolf's r12 = (4/3) r_h);
  - J2 β = 0.5 constant.
- Observable: the luminosity-weighted ⟨σ_los²⟩ inside a projected aperture R_ap. A1 R_ap = a = R_e (primary); A2 R_ap = ∞
  (global). Computed with the exact 3-D cylinder weight w(r) = (1 − c) − β[(1 − c) − (1 − c³)/3], c = √(1 − R_ap²/r²) for r > R_ap,
  w = 1 − 2β/3 inside. Under A2 the three β give the same σ (virial theorem; checked by K5), so there are 4 distinct corners.
- E_J = 2 ln(σ_obs/σ_J); pe_R1 = 2 ln(σ_J/σ_W), with σ_W = CFG880's σ_law. Only DW moves (lensing, rotation and shear
  estimators are untouched by construction). Reported: F0 under Wolf and Jeans; the plain mean of E at g_bar < 1e-12; CFG828's
  28 dwarfs (CFG827 SFH Υ, CFG824 σ, no gas, as CFG828): the g_bar < 10^−11.9 mean Δ under Wolf and Jeans.

### R2 (self-sourcing): cold energy's own mass in the law's argument
- **R2-0 literal.** g = ν((g_b + g_c)/a0)(g_b + g_c), with g_c = the whole non-baryonic part (g_c = g − g_b, the record's ID
  ρ_c = ρ_ph). Then g = ν(g/a0) g, which has no finite solution because ν_e(y) > 1 for every finite y. The iteration
  g_{n+1} = ν(g_n/a0) g_n grows without limit. Status: **ILL-POSED** (no class; K6 demonstrates it numerically).
- **R2-A primary (the record's closest well-defined form).** CFG638's phantom target built from the total Newtonian source
  ρ_b + ρ_c instead of ρ_b, keeping ρ_c = ρ_ph (equivalently, CFG722's coupling G applied to the tethered cold energy).
  Spherical / algebraic: the quantity entering ν is g_N[ρ_b + ρ_c], which equals g. So g_c = (ν(g/a0) − 1) g, i.e.
  **g_b = g (2 − ν(g/a0))**.
  - Real solutions need ν < 2, i.e. g > y_f a0 with ν(y_f) = 2 (ν_e: y_f = (ln 2)²). The solution is unique (h(y) = y(2 − ν)
    is increasing there) and stable under the CFG638 drift.
  - Newtonian limit g → g_b. It agrees with the plain law to first order in (ν − 1).
- **R2-B secondary (argument-only).** ν takes the total field, the prefactor stays baryonic: g = ν(g/a0) g_b. Newtonian limit
  g → g_b; deep limit g = a0^{1/3} g_b^{2/3}.
- Kernels: ν_e for dwarfs, SPARC and lenses; ν_mono (CFG4_common) for clusters, as in the record's cluster law.
- **Stated in advance:** R2-A and R2-B depend on g_b alone. At matched g_bar they shift red and blue lenses alike, so they
  cannot create or remove the red/blue split (F1 − F2 moves only through the two classes' g_bar distributions).
- **Diagnostic R2-S (no class).** If a bound cold surplus existed (CFG877's H-LINK = coupling G on the surplus), compare the
  surplus needed at r12 to reach σ_obs under self-sourcing (g = law(g_b + g_x)) with Newtonian addition (class A,
  g = law(g_b) + g_x). Median ratio M_x,A/M_x,S over dwarfs with an excess. Needs a supply; it is not a zero-constant prediction.

### R3 (EFE sign)
- **E0, no EFE.** The record's class-A round rule (phantom from the region's own baryons, CFG888 Q1) and CFG478's material
  reading. This is the baseline of CFG880/914/919/921/873–875 (K4 / K7 verify the CFG880 / CFG874 paths carry no EFE).
  "Removing the EFE" therefore equals the baseline: ΔF0 = 0 by construction.
- **E1 primary, the record's coded EFE** (CFG883 / CFG919 V4): g = g_N,i ν_e((g_N,i + g_N,e)/a0).
- **E2 bracket, 1-D QUMOND subtraction** (canonical action, "the tether reads g_N of all baryons", CFG722):
  g = (g_N,i + g_N,e) ν_e((g_N,i + g_N,e)/a0) − g_N,e ν_e(g_N,e/a0).
- Host field g_N,e: Newtonian baryonic point masses, MW 6.0e10 M_⊙ (CFG820/838/839/883; bracket 8.0e10) and M31 1.0e11 M_⊙
  (CFG838; bracket 1.5e11), at LVD distance_gc / distance_m31.
  - Vector sum, with the angle from the law of cosines; the MW–M31 separation is LVD's distance_gc of M 32.
  - Other hosts (LMC, M33, NGC 3109, ...) are omitted. This is a lower bound on g_e for their satellites.
- Applied to:
  - the 83 dwarfs: F0, plus the satellite and field means;
  - CFG874's satellite–field statistic (its code exec'd read-only; c and E with its own class rule), with every dwarf shifted by
    its own EFE (isolated dwarfs included).
- Satellite / field = CFG874's grouping: minimum distance to MW or M31 < 300 kpc / ≥ 300 kpc.

## 3. Grading (per reading and footing; 0.05 dex = 0.1151 in ln units)
- For excess facts X ∈ {F0, F1, F5}: ΔX = |X_res| − |X_obs|. A sign flip past zero counts through |X_res|.
- **DAMAGE:** any rotator fact X ∈ {F2, F3, F4} with |X_res| ≥ |X_obs| + 0.05 dex AND |X_res| ≥ 2 se.
- **SPLIT broken:** F2 damaged, or F1_res − F2_res ≤ −2 √(se1² + se2²) (reversed).
- **RESOLVES:** |F0_res| ≤ 0.5 |F0_obs|, no DAMAGE, no SPLIT, and neither F1 nor F5 has ΔX ≥ +0.05 dex.
- **WORSENS:** DAMAGE, or SPLIT, or any excess fact with ΔX ≥ +0.05 dex. WORSENS takes precedence over PARTIAL.
- **PARTIAL:** not WORSENS, not RESOLVES, and at least one excess fact with ΔX ≤ −0.05 dex.
- **NO EFFECT:** otherwise.
- **Primary classes:**
  - R1 at (J0, A1);
  - R2 = R2-A, with R2-B graded and reported beside it;
  - R3 = E1 at the nominal host masses ("include EFE"); "remove EFE" = E0, NO EFFECT by construction.
- **Robustness:** R1 over its 4 distinct corners; R3 over {E1, E2} × host-mass brackets.
  - ROBUST: every corner shares the primary class.
  - Otherwise BRACKET-DEPENDENT, with the range reported.
- **Satellite–field (R3):** reports c ± se and E ± se, and CFG874's class under E0, E1 and E2. "Changes the comparison" = the
  class changes or |Δc| ≥ 0.05 dex.
- **Trials:** three reframings, zero constants, nothing calibrated. No sealed prediction unless a reframing RESOLVES on both
  footings.

## 4. Controls (any K failure stops the lane; no class is reported)
- **K1** CFG919 exec'd read-only: all its checks pass, including CFG828 reproduced exactly and CFG914's 9.
- **K2** CFG921 prefix exec'd read-only: its K1–K4 and K6 pass. CFG919's V0 cells are reproduced.
- **K3** CFG921's observed facts (F0–F8b with se, both footings) are reproduced from cfg921_results.json to ≤ 1e-9.
- **K4** Wolf path through this lane's own inputs:
  - σ_law of CFG880 reproduced for all 83 dwarfs (rel ≤ 1e-9); own gas copy = CFG880 gas_in at r12 (≤ 1e-12);
  - CFG828's 28 rows Δ and its out-of-range mean reproduced (≤ 1e-9).
- **K5** Jeans solver:
  - Newtonian isotropic Plummer aperture ⟨σ²⟩(<X) for X ∈ {0.1, 0.5, 1, 2, ∞} vs the analytic
    (πGM/32a)(1 − (1+X²)^{−3/2})/(1 − (1+X²)^{−1}): < 1% (task bar; target < 0.1%);
  - projected L(<X) vs X²/(1+X²);
  - virial identity, global ⟨σ²⟩ independent of β (OM, 0.5, 0.9) vs (1/3M)∫ρ r g dV: < 1%;
  - deep-law global σ⁴ = (4/81) G M a0: < 1%.
- **K6** R2: fixed-point residuals ≤ 1e-10. Newtonian limit: |ln(g/g_law)| ≤ 1e-6 at y_b = 100 for R2-A and R2-B. R2-0:
  ν_e > 1 on the whole grid, and its iteration is monotone increasing with no fixed point.
- **K7** R3:
  - g_e → 0 gives the isolated law exactly;
  - EFE-dominated limits: E1 → ν(y_e), E2 → ν(y_e)(1 + L_e), bracketing the exact linear QUMOND value ν(y_e)(1 + L_e/3) (CFG478 K3);
  - CFG874's primary c, se_c, E, se_E reproduced from cfg874_results.json at E0 (≤ 1e-9, both footings).
- **MUTATE** (separate outputs `cfg925_MUTATE.out`, `cfg925_results_MUTATE.json`; exit 1 = all teeth bite):
  - M1: R1 with β = 0.9 constant, A1. F0_J must move by ≥ 0.02 dex from the J0 value.
  - M2: a0 × 10. R1 F0_J, R2-A ΔF0 and R3-E1 ΔF0 must each move by ≥ 0.02 dex from main.
  - M3: host masses × 10. The satellite mean EFE shift must grow by ≥ 0.02 dex.
  - A toothless MUTATE is reported, and the affected reading is flagged.

## 5. Running and wording
- Compute: one process, OMP_NUM_THREADS=1, `nice -n 10`, < 1 GB RSS (measured with `/usr/bin/time -l`), minutes at most, run
  beside the live 1024³ job under the owner's 2026-10-20 small-job allowance. Nothing downloaded.
- Order: K-only run (`CFG925_KONLY=1` → `_K` outputs), then MUTATE, then main.
- Any post-hoc change goes in a dated, labelled AMENDMENT file. NO EFFECT and WORSENS are reported as plainly as RESOLVES.
