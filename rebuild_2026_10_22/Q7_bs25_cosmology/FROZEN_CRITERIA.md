# Q7_bs25_cosmology FROZEN CRITERIA (2026-10-23): does Blanchet–Skordis 2025's DBI cosmological sector rescue v3's cosmology?

Written and committed alone, before any script or number of this lane. Rules: `rebuild_2026_10_22/BRIEF.md`,
`covariant_push_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. κ = ½ FITTED. Footings
9.3603e-11 / 1.1312e-10 m/s², never pooled (neither enters: a₀ is absent at linear order on FRW, Q6 D0). No dark-matter
particle: the cold sector is the Blanchet–Skordis K(Q) dust ("cold energy"). Never "theory closed". Never "the data
favour the framework". No ΛCDM-processed input is used as a framework input. **Compute:** `OMP_NUM_THREADS=1 nice -n 15`,
one thread, < 1 GB RSS, CLASS runs strictly one at a time, builds `make -j1`; `compute_queue/heavyq.py status` checked
before each heavy step. No downloads.

## 0. The question and what was read before this file

**Conflict.** Q6_v3_class (386ab3c2bb…383a1600ae), F3_growth_audit and M1_trilemma find that v3's BS quadratic
K = μ_K²(Q−1)² fails cosmologically at BS's galaxy cap μ_K ≤ 14.8 h/Mpc: no radiation era (BBN needs μ_K ≥ 1.84e8 h/Mpc)
and linear growth starved (Boltzmann R_B = σ₈/σ₈,dust = 0.073 at the cap; 5 % needs μ_K > 2542 h/Mpc). Blanchet & Skordis
2025 (BS25, arXiv:2507.00912) claim agreement with the standard cosmological model and the CMB using a DBI-form K.

**Read before writing this file (WebFetch of the arXiv abstract and HTML pages, 2026-10-23; PROVISIONAL, the summariser
can garble; nothing downloaded):**
- **BS25** (6-page Moriond proceedings, v1 only): Eq. 1 action S = (c³/16πG)∫√−g[R − 2J(Y) + 2K(Q)] + S_m; Eqs. 2–3 Q, n_μ,
  A_μ, Y = A·A/c⁴; Eq. 4a J = 0 for Y ≫ a₀²/c⁴; Eq. 4b J = Λ − Y + (2c²/3a₀)Y^{3/2} + O(Y²) for Y ≪ a₀²/c⁴; Eq. 5 quadratic
  K; **Eq. 6 K_DBI = (2μ²/λ_D)[1 − √(1 − λ_D(Q−1)²)]**; Eqs. 7–13 PN system (Eq. 11 ρ_τ = −(1/4πG)[∇·(J_Y∇Ξ) + μ²Ξ],
  Ξ = φ − σ̇ + ½|∇σ|²; Eq. 13 stationary ∇·[(1+J_Y)∇φ] + μ²φ = 4πGρ_m); Eqs. 14–16 background ρ̄_K = (Q̄K_Q − K)/8πG,
  P̄_K = K/8πG, w, c_ad² = K_Q/(Q̄K_QQ), K_Q = I₀/a³; Eq. 17 quadratic background. Linear perturbations are said to map
  onto GDM with c_s²(t,k), c_vis²(t,k) — **no formulas, no μ or λ_D values in the text, no Boltzmann code named**. Fig. 2:
  w(a) curves against a "yellow region allowed by CMB data"; two DBI models said compatible with MOND and the CMB.
- **BS24** (arXiv:2404.06584v2 = JCAP 11 (2024) 040), cosmology section, as numbered in today's fetch of the v2 HTML:
  Eqs. 43a–48 background; Eq. 53 Q̄ = 1 + I₀/(2μ²a³); Eqs. 54, 57, 58 quadratic ρ̄, w, c_ad²; **Eq. 62
  Υ = φ − (σ̇ + 3Hc_ad²σ)/Q̄; Eqs. 66a–d δ_K, θ_K, Π_K, Σ_K = 0 (66a contains ∇²Υ/(4πGa²ρ̄_K)); Eq. 67
  ∇²Υ = 4πGρ̄_Ka²{(1+w)Υ/c_ad² + Δ_K}; Eqs. 69–71 Π_nad and c_s²(t,k) = c_ad²[1 + c_ad²k²/(4πGa²ρ̄_K(1+w))]⁻¹;
  c_vis² = 0; Eqs. 74–75 fluid equations**; Eqs. 76–80 bounds (GDM: w ≲ 0.0164 near a ~ 10^-4.5 ⇒ w̃₀ < 5.3e-16 ⇒
  μ⁻¹ ≲ 0.22 kpc; galaxies: μ⁻¹ ≳ 100 kpc ⇒ w̃₀ ≳ 1.06e-10, with H₀ ~ 70, Ω_K,0 ~ 0.26); **Eq. 87 DBI K; Eq. 88
  Q̄ = 1 + [λ_D + (2μ²a³/I₀)²]^{-1/2}, 1 ≤ Q̄ < 1 + λ_D^{-1/2}; Eqs. 89a–b ρ̄, P̄; Eqs. 90a–b limits
  (early ρ̄ ≃ (1 + λ_D^{-1/2})I₀/(8πGa³)); Eqs. 92–95 w, c_ad² in q = Q̄ − 1 and in 𝒵 = I₀/(2μ²a³), late/early limits.**
  **Fig. 1 caption: DBI models μ⁻¹ ~ 223 kpc with λ_D ~ 30, and μ⁻¹ ~ 22.3 Mpc with λ_D ~ 1**, both "compatible with a MOND
  limit and the CMB"; the CMB region is the 99 % region of the binned GDM "var-w" analysis (Planck power spectra, w in
  eight bins). §4.3.3: the GDM constraints "do not directly apply, as they correspond to purely time-dependent sound speed
  and viscosity" (their sound speed is k-dependent); "a proper comparison of the Khronon model with data is left for a
  future investigation". No CLASS/CAMB run is mentioned.
- The record: C4 README (BS24/BS25 transcription, K7: Ω_K FITTED, DBI adds λ_D), `opus_48_extended_research/reviews/
  door_runs/doorB_quadratic_vs_dbi.py` + `doorB_SKEPTIC_verify.py` (2026-06-19: same DBI form, then numbered Eq. 96/97;
  K″(1) = 2μ² shared, K⁗(1) = 6μ²λ_D; "λ_D ~ 1"; μ⁻¹ ~ 22.3 Mpc and ~ 223 kpc), Q6 README/FROZEN_CRITERIA/scripts,
  F3 README, M1 README head. Equation numbers differ between the fetches (87/88 today vs 96/97 in June): **this lane cites
  equation content, and gives today's numbers only as labels.**

**Stated before any number (an analytic reading, not a result of this lane; every item is checked or measured below):**
1. BS24 Eq. 71 is identical to Q6's rest-frame sound speed c_s² = Q̄K′/(Q̄²K″ − 2j₁k²/a²) at j₁ = J′(0) = −1, for any K
   (because 4πGρ̄(1+w) = Q̄K′/2 and c_ad² = K′/(Q̄K″)). So BS's own perturbation equations contain the J′(0) = −1 "hold"
   that F3/M1/Q6 found; the quasi-static kernel is s = a²M²/(k² + a²M²) with **M² ≡ Q̄²K″/2** (from BS24 Eq. 67).
2. For the DBI K, K″ = 2μ²(1 − λ_Dq²)^{-3/2} = 2μ²(1 + λ_D𝒵²)^{3/2}, so M ≫ μ while λ_D𝒵² ≫ 1 (early) and M → μ late.
   DBI therefore makes the khronon dust-like early (no a⁻⁶ era: w → 0, c_ad² → 0, ρ̄ → (1 + λ_D^{-1/2}) × dust) and
   restores the hold k > aμ late. The comoving hold scale a·M(a) has a minimum k_min ≈ 1.21 μ a₁ (3.5 λ_D)^{1/6} (Q̄ ≈ 1,
   a₁³ ≡ I₀/(2μ²)); at the cap a₁ ≈ 1/1706 (Q6 step B), so k_min ≈ 0.0105 (3.5 λ_D)^{1/6} h/Mpc. **Expectation:** BBN is
   rescued for λ_D ≳ O(1); growth within 5 % needs k_min ≳ O(0.3–1) h/Mpc, i.e. λ_D of order 1e8–1e12 at the cap, far
   above BS's 1 and 30; at BS's two published parameter sets linear growth fails.
3. On BS's stationary branch (Ξ = φ, BS25 Eqs. 11/13) |Q − 1| ≈ |φ|/c² ~ v_c²/c² (order of magnitude). The DBI root is
   real only for |Q − 1| < λ_D^{-1/2}. A large growth-rescuing λ_D therefore meets a ceiling inside galaxies and clusters.

## 1. External inputs (cited)

- **BS24, BS25** as listed in §0 (PROVISIONAL WebFetch transcriptions; self-consistency is checked in step S).
- **Q6_v3_class** (`rebuild_2026_10_22/Q6_v3_class/`): `khronon.patch` (pristine CLASS v3.3.4 → Khronon tree; types 0 DUST,
  3 LIT, 4 LOB; `aest_K2` = μ_K² [Mpc⁻²]; `aest_lambda_c` = j₁), `q6_make_patch.py`, `PROVENANCE.md` (pristine tree
  `../_external_data/class_public_v3.3.4_2026_10_22/class_public-3.3.4`, C7's vanilla binary), `q6_native.py` (C2
  likelihood loader, run helper, Gauss–Newton, step-B background block, BBN constants), `q6_validate.py` (A3 gate forms),
  `q6_native_results.json` (σ₈(LOB 14.8) = 0.0607512, σ₈(DUST) = 0.827959, μ_K,BBN = 1.8364e8 h/Mpc, ΔN_eff,equiv(1 MeV) at
  14.8 h/Mpc = 7.698e13; ΛCDM χ² 1003.47 at C7's refit).
- **C2/C7** (`covariant_push_2026_10_22/C2_aest_cosmology/c2b_native_cmb.py` likelihood block executed read-only;
  `C7_aest_class/c7_native_results.json` ΛCDM refit parameters).
- **F3** (`growth_ratio`, K4 numbers) — used only for a reported ODE cross-check.

## 2. Assumption ledger (classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / POSITED / EXTERNAL)

| ingredient | this lane's choice | class | source |
|---|---|---|---|
| action | BS25 Eq. 1 = BS24 Eq. 6: R − 2J + 2K, J with J(0) = Λ, J′(0) = −1 (BS25 Eq. 4b); v3: J = J_x (same J(0), J′(0)) | EXTERNAL (BS) / FRAMEWORK-NATIVE (v3) | §0, C4 |
| K shape | **DBI**, K = (2μ²/λ_D)[1 − √(1 − λ_D(Q−1)²)] | EXTERNAL POSTULATE (BS24/BS25), one new constant λ_D | §0 |
| λ_D, μ at BS's published sets | P1 = (μ⁻¹ = 223 kpc, λ_D = 30), P2 = (μ⁻¹ = 22.3 Mpc, λ_D = 1) | EXTERNAL (BS24 Fig. 1 caption, WebFetch; BS25 gives no values) | §0 |
| BS galaxy cap | μ⁻¹ ≥ 100 kpc ⇔ μ ≤ 9.998 Mpc⁻¹ = 14.8 h/Mpc at h_ref = 0.67552 | EXTERNAL premise (BS24) | Q6 grid |
| J at linear order | only J(0) = Λ and j₁ = J′(0) = −1 enter on FRW (Y = O(ε²)); a₀ first at Y^{3/2} | DERIVED (Q6 D0); BS25 Eq. 4b checked in S10 | Q6 |
| P covector, β = η = 0, γ_L (v3 only) | absent from BS; at linear order on FRW P̄ = 0, P's effect at γ_L = 0 is J's Legendre dual (already the j₁ term); γ_L corrections ≤ 8e-7 (Q6 ledger) | FRAMEWORK-NATIVE, neglected at linear order (Q6's stated estimate) | C4 K3, Q6 |
| khronon perturbations | exact fluid (no shear), δp from c_s² = Q̄K′/(Q̄²K″ − 2j₁k²/a²), conservation exact (Q6 D2–D4), general K | DERIVED (Q6 D2) = BS24 Eq. 71 (checked S7) | Q6, BS24 |
| background | exact DBI background (no dropped term): Q̄ from K′(Q̄) = I₀/a³ | DERIVED from the action | BS24 Eq. 88 (S2) |
| dust abundance ω_K | late-time (a = 1) value; FITTED in fits; = C7 ΛCDM-refit ω_dm at fixed parameters (as Q6) | FITTED (initial condition I₀) | C2, C4 K7 |
| G_cosmo/G_N | 1 (Y ≡ 0 on FRW) | DERIVED | Q6 D1 |
| A_s, n_s, ω_b, θ_s, τ | fixed at C7's ΛCDM refit (growth runs) / fitted (fits) | FRAMEWORK-NATIVE form, values from plik-lite | C7 |
| neutrinos, BBN He table, recombination | massless N_ur = 3.044; CLASS defaults | external standard physics | C7 |
| plik-lite + low-ℓ TT/EE (C2 numpy) | data | SURVEY-CALIBRATION (plik-lite's foreground marginalisation done on ΛCDM-like spectra: ΛCDM-PROCESSED to that extent) | C2 |
| τ prior | C2's low-ℓ scan | SURVEY-CALIBRATION | C2 |
| BBN line | ΔN_eff,equiv(T = 1 MeV) ≤ 0.5 (Q6's definition, same constants) | EXTERNAL (conservative BBN-era line) | Q6 §7 |
| ω_cdm = 1e-8 inert species | numerical (fixes CLASS's synchronous gauge) | numerical | C7 |
| comparison model | ΛCDM refit, pristine binary, same likelihood/optimiser/precision | same-pipeline control | C7, Q6 |
| galaxy/cluster potentials for the DBI ceiling (reported only) | |Q − 1| ~ v_c²/c², v_c = 220 km/s (Milky Way) and 1000 km/s (cluster) | order-of-magnitude, POSITED reading of BS25 Eqs. 11/13 (Ξ = φ) | §0 item 3 |
| STANDARD-MOND-MACHINERY | none (no QUMOND, no EFE recipe, no a₀) | — | — |

## 3. Models and parameter sets

- **DBI (new, `aest_K_type` 5):** λ_D carried in C7's unused `aest_Z0` (no `input.c` edit; types 0/3/4 untouched). With
  𝒵 = K′/(2μ²) = I₀/(2μ²a³) and r = √(1 + λ_D𝒵²): Q̄ = 1 + 𝒵/r, K = 2μ²𝒵²/(r(r+1)), K′ = I₀/a³, K″ = 2μ²r³,
  c_ad² = 𝒵/(r²(r + 𝒵)); perturbations as Q6 with c_s² = Q̄K′/(Q̄²K″ − 2j₁k²/a²), j₁ = −1. (Cancellation-free forms; their
  equality with BS24 Eqs. 87–94 is check S2–S4 and V_unit.)
- **DUST** (type 0), **LIT** (type 3), **LOB** (type 4): Q6's, unchanged.
- **Published BS sets:** **P1** μ = 1/0.223 Mpc⁻¹ = 4.4843 Mpc⁻¹, λ_D = 30; **P2** μ = 1/22.3 Mpc⁻¹ = 0.044843 Mpc⁻¹, λ_D = 1.
- **Cap sets (BS's λ_D values at the cap):** **C1** μ = 9.998 Mpc⁻¹ (14.8 h/Mpc × 0.67552), λ_D = 1; **C30** same μ, λ_D = 30.
- **Requirement scans (REPORTED requirements, like F3's μ_min; never adopted, never fitted, not a verdict knob):** R_B
  versus λ_D at fixed μ ∈ {cap, P1's μ, P2's μ}: λ_D = 10⁰, 10², …, 10²⁴ (cap, P1's μ) and 10⁰ … 10³⁰ (P2's μ); then the
  first bracket where R_B crosses 0.95 is bisected 5 times in log₁₀λ_D (one CLASS run each) and λ_D,95 is the linear
  interpolation of R_B in log λ_D across the final bracket. Not bracketed ⇒ "beyond the grid".

## 4. Step S: the source, checked (`q7_source.py`, sympy; exit 0 iff all pass)

- **S1** K_DBI: λ_D → 0 limit = μ²(Q−1)²; K(1) = K′(1) = 0, K″(1) = 2μ², K‴(1) = 0, K⁗(1) = 6μ²λ_D.
- **S2** Eq. 88 solves K′_DBI(Q̄) = I₀/a³ (residual 0) and 1 ≤ Q̄ < 1 + λ_D^{-1/2}; the coded forms Q̄ = 1 + 𝒵/r, K, K″ = 2μ²r³
  equal the DBI expressions on Eq. 88.
- **S3** Eqs. 89a/b equal (Q̄K′ − K, K)/8πG on Eq. 88; ρ̄′ + 3ℋ(ρ̄ + p̄) = 0 identically given a³K′ = I₀.
- **S4** Eqs. 92, 93 (in q) and 94a/b (in 𝒵) equal Eqs. 45/46 on Eq. 88; coded c_ad² equals 94b.
- **S5** Eqs. 95a/b (late/early leading terms) and 90a/b (limits) follow from 94/89 (series/limits, residual 0).
- **S6** Q6's quadratic background (Q6 step B: 8πGρ̄ = I₀/a³ + I₀²/(4μ²a⁶)) is the λ_D → 0 limit of 89a.
- **S7** BS24 Eq. 71 c_s²(t,k) ≡ Q6's c_s² with j₁ = −1, for a general K (residual 0). **This is the test of "our lanes vs
  BS's own equations".**
- **S8** (a) the BS24 Eq. 67 constraint gives Υ = −4πGρ̄_Ka²Δ_K/(k² + a²M²) with M² = Q̄²K″/2 for general K (exact); (b) with
  Q̄ → 1, K″ = 2μ² this is F3/BSK2's s = a²μ²/(k² + a²μ²) (Q6 D5); (c) Υ (BS24 Eq. 62, cosmic time, π_BS = σ/Q̄, Q̄˙ = −3Hc_ad²Q̄
  from Eq. 48) equals Q6's Ξ = Ψ − π′ − ℋπ (conformal, π = π_BS/a) identically; (d) the ∇²Υ term of Eq. 66a equals Q6's
  2j₁(k/a)²Ξ term of 8πGδρ at j₁ = −1.
- **S9** BS24's bounds reproduce from the transcribed formulas (w̃₀ = 3H₀²Ω_K/(4μ²c²), H₀ = 70, Ω_K = 0.26): w ≤ 0.0164 at
  a = 10^-4.5 ⇒ w̃₀ ≤ 5.3e-16 and μ⁻¹ ≤ 0.22 kpc; μ⁻¹ = 100 kpc ⇒ w̃₀ = 1.06e-10. PASS = each within 3 % of the quoted value.
- **S10** BS25 Eq. 4b ⇒ J(0) = Λ, J′(0) = −1, a₀ first at Y^{3/2}; BS25 Eqs. 14–17 = BS24 Eqs. 44–47, 54, 57; BS25 Eq. 6 = BS24 Eq. 87.
- **S11** BS25 Eq. 11 (static, linear) equals Q6's 8πGδρ = Q̄K″δQ + 2j₁(k/a)²Ξ with δQ = −Ξ, Q̄ = 1, K″ = 2μ², j₁ = −1.
- **MUTATE** (`Q7_MUTATE=1`): Q6's c_s² is used with j₁ = +1 in S7 and S8(d); both must FAIL.

## 5. Step P: the patch (`q7_make_patch.py` → `dbi.patch`)

Copy the pristine tree; `patch -p1 < rebuild_2026_10_22/Q6_v3_class/khronon.patch` (must apply cleanly); add the DBI case
(type 5) **only inside `background_aest_K()` and `perturbations_aest_rhs()`** (anchor edits, each matching once); write the
unified diff Q6-tree → DBI-tree as `dbi.patch`. `--mutate` writes `dbi_MUTATE.patch` with K″ = 2μ²/r³ (wrong power) in the
perturbation c_s² only. Builds under `../_external_data/class_khronon_dbi_build_2026_10_23/` (`class_dbi/`,
`class_dbi_mutate/`), `OMP_NUM_THREADS=1 nice -n 15 make -j1 class`.

## 6. Step V: validation (`q7_validate.py`)

Spectra: lensed TT, TE, EE, φφ, 2 ≤ ℓ ≤ 2500; P(k, z = 0), 1e-4 ≤ k ≤ 1 Mpc⁻¹. Parameters: C7's V1 Planck-like set (as Q6).
"ΛCDM units" = |ΔX|/X_ΛCDM (Q6 A3 form, TE by √(TT·EE)_ΛCDM).
- **V_prov** tree = pristine + Q6 `khronon.patch` + `dbi.patch`; vs Q6's built tree only the two functions differ.
- **V_unit** a C harness compiled (same `-O3`) from the two function texts extracted from the built tree:
  (i) λ_D = 0 exactly: DBI's (Q̄, K, K′, c_ad², δp/ρ) equal LIT's to ≤ 1e-13 relative at ≥ 200 (a, k) points,
  a ∈ [1e-14, 1], k ∈ [1e-5, 10] Mpc⁻¹, μ ∈ {cap, 1e6 h/Mpc};
  (ii) λ_D ∈ {1e-6, 1, 30, 1e6, 1e12, 1e24}, same points: Q̄ vs BS Eq. 88, ρ̄ and p̄ vs 89a/b, w and c_ad² vs 94a/b, the
  rest-frame c_s² vs BS Eq. 71 (all in mpmath, 50 digits) to ≤ 1e-10 relative.
- **V0** types 0 and 4 (DUST; LOB at 14.8 h/Mpc) bit-identical to Q6's binary.
- **V1 (λ_D → 0: the gate against Q6's quadratic model where they agree):** μ_gate = the smallest of {1e13, 1e14, 1e15, 1e16,
  1e17} h/Mpc at which Q6's binary runs LIT at these parameters; DBI with λ_D = 1e-25 vs LIT at μ_gate: every spectrum
  ≤ 1e-5 relative. LIT vs DUST at μ_gate is reported beside it (the gate's discriminating power). No μ_gate ⇒ V1 FAIL.
- **V2 (λ_D → ∞):** DBI at the cap with λ_D = 1e30 vs DUST, synchronous and Newtonian: every spectrum ≤ 1e-4; 100θ_s and
  r_drag ≤ 1e-6. (Q̄ − 1 ≤ 1e-15 and the hold scale > 1e8 Mpc⁻¹: DBI must be dust.)
- **V3 gauge** (A3 form): DBI P1 and C30, synchronous vs Newtonian, ΛCDM units ≤ max(1e-3, 3 × vanilla).
- **V4 convergence** (A3 form, same k grid): DBI P1, default (`k_per_decade_for_pk = 20`) vs C7 high precision, ΛCDM units
  ≤ max(2e-3, 2 × vanilla).
- **V5 IC attractor** (A3 form): DBI P1, start × 0.25 vs × 0.125: C_ℓ relative, P(k) in ΛCDM units, ≤ vanilla + 1e-4.
- **MUTATE** (`Q7_MUTATE=1`, MUTATE binary): V_unit (ii) and V2 must FAIL.
- **"DBI ready"** iff every V line passes in the normal build and MUTATE breaks V_unit (ii) and V2.

## 7. Step B: BBN (`q7_native.py`, Python background before any spectrum)

Q6's step-B block (same constants, `a_of_T`, BBN dictionary, h_ref = 0.67552, ω_K = C7 refit ω_dm) generalised to DBI:
I₀ from 8πGρ̄(a = 1) = 3H₀²Ω_K (root), ρ̄_K(a) from 89a in the cancellation-free form.
- **K0c (reproduce first):** at λ_D → 0 (the quadratic formula) the block reproduces Q6's μ_K,BBN = 1.8364e8 h/Mpc and
  ΔN_eff,equiv(1 MeV) = 7.698e13 at 14.8 h/Mpc, each to ≤ 1e-3 relative.
- Rows: P1, P2, C1, C30 and (μ, λ_D,95(μ)) when found. Per row: ρ̄_K/ρ_r and ΔN_eff,equiv at 1 MeV and 0.07 MeV; the early
  abundance ratio ρ̄_K a³ (a = 1e-8) / ρ̄_K a³ (a = 1); max w over 1e-6 ≤ a ≤ 1e-2 and w(10^-4.5) beside BS's 0.0164 line
  (reported); whether the DBI binary starts at the fixed parameters (CLASS's own radiation test).
- **λ_D,BBN at the cap** = smallest λ_D with ΔN_eff,equiv(1 MeV) ≤ 0.5 (root in log λ_D; reported).
- **Reading (frozen, per row):** **"BBN-VIABLE"** iff ΔN_eff,equiv(1 MeV) ≤ 0.5 and CLASS starts; **"NO RADIATION ERA
  (BBN-EXCLUDED)"** iff ΔN_eff,equiv(1 MeV) > 0.5; otherwise "BBN-VIABLE, CLASS REFUSES".

## 8. Step G: growth at fixed parameters (`q7_native.py`; only if "DBI ready")

- **K0a** pristine ΛCDM χ² at C7's refit within 2 of 1003.47. **K0b** this lane's binary at the same parameters reproduces
  Q6's σ₈(DUST) = 0.827959 and σ₈(LOB 14.8) = 0.0607512, each to ≤ 1e-4 relative.
- Runs (C7 high precision + start × 0.25, P_k_max = 10 h/Mpc, lensed C_ℓ to ℓ = 2508), at C7's ΛCDM refit with ω_K = ω_dm:
  DUST, P1, P2, C1, C30, the requirement scans (§3). Per run: σ₈, S₈, χ² parts (A_planck = C7's), P/P_DUST at
  k = 0.1, 0.3, 1, 3, 10 h/Mpc, TT/TT_DUST at ℓ = 220, 540, 1000, **R_B = σ₈(DBI)/σ₈(DUST)**.
- **N0 (the native dust check):** DBI at the cap with λ_D = 1e30 gives σ₈/σ₈(DUST) within 1e-3 of 1 (MUTATE must FAIL).
- **Reading per published/cap set (frozen):** **"GROWTH RESCUED"** iff R_B ≥ 0.95; **"GROWTH FAILS"** iff R_B < 0.95.
- λ_D,95(μ) for μ ∈ {cap, P1's μ, P2's μ} (reported requirements) and, beside each, the DBI root ceiling λ_D,95^{-1/2}
  against v_c²/c² = 5.38e-7 (220 km/s) and 1.11e-5 (1000 km/s) (reported, order of magnitude, PROVISIONAL).
- **Reported cross-check (not gating):** F3's `growth_ratio` copied with the kernel replaced by s = a²M²/(k² + a²M²), M from
  the DBI background (§0 item 1), start a_i = 1e-4 and 1e-3, on DUST's CLASS P(k), at P1, P2, C1, C30: R_ODE beside R_B.

## 9. Step F: fits (`q7_native.py`)

C7/Q6 Gauss–Newton (4 iterations, halving line search, ≤ 150 CLASS runs per model; start C7's ΛCDM refit; free ω_b,
ω_K (FITTED), 100θ_s, ln10¹⁰A_s, n_s, τ, A_planck) for ΛCDM (pristine), P1, P2, C1, C30, and (reported) the cap at
λ_D,95(cap) if found. Reported: Δχ² vs the ΛCDM refit, H₀, σ₈, Ω_m, S₈, converged or not. **Numbers only**, except as
used in §10. RUNAWAY (C7 A4) models are reported, not fitted.

## 10. Step C: the verdict (frozen; one of three forms, as the coordinator asked)

Evaluated in this order:
- **(C) OUR LANES HAVE AN ERROR (named)** if S7 or S8 FAILS (Q6/F3/M1's linear khronon equations differ from BS's own in a
  term that enters growth), or K0b FAILS, or V1 FAILS because DBI at λ_D → 0 and Q6's LIT disagree inside CLASS (an error in
  Q6's code). The error is named from the failing line.
- **(A) BS25'S SECTOR RESCUES v3 AT GALAXY-ALLOWED μ_K** if at least one of P1, P2, C1, C30 is "BBN-VIABLE" and "GROWTH
  RESCUED" and its fitted Δχ² vs the ΛCDM refit is ≤ +10.
- **(B) IT FIXES BBN ONLY; GROWTH STILL FAILS** if every one of P1, P2, C1, C30 is "BBN-VIABLE" and none satisfies (A).
- Otherwise **"(B−) NOT EVEN BBN at BS's sets"**, stated plainly.

Reported with the verdict: λ_D,95 at each μ with its ceiling comparison; the fitted Δχ² of P1, P2, C1, C30; where BS's
claim comes from (S9 reproduces their background-only w(a) criterion; their c_s²(t,k) is S7's); whether BS's published
sets lie inside the cap (they do by construction of §3: 223 kpc and 22.3 Mpc ≥ 100 kpc). A λ_D,95 is never adopted: a
DBI constant set to make growth pass is a new constant at a value chosen by the failure (rule 4), reported as a door.

## 11. Files, rules, verdict word

Scripts `q7_source.py`, `q7_make_patch.py`, `q7_validate.py`, `q7_native.py`, each writing `<name>.out`,
`<name>_results.json` and `*_MUTATE.*` under `Q7_MUTATE=1`; each prints `<check> PASS/FAIL value threshold` lines and ends
`<NAME> COMPLETE: N/M checks PASS.` (exit 0 iff all pass). README verdict first (CRISP FINDING, RUNNABLE NOW,
DATA-GATED, SCOPED NO-GO, NOTHING NEW) plus the (A)/(B)/(C) line. CLASS source not committed (only `dbi.patch`,
scripts, outputs). Commit only this lane's paths; never push. Any change to this file is an append-only AMENDMENT marked
pre- or post-result. If any step needs BS24/BS25's exact TeX (a transcription the self-consistency checks cannot settle),
the README says so and stops that step.
