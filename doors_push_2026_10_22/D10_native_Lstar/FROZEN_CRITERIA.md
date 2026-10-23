# D10_native_Lstar — FROZEN CRITERIA (written and committed before any script or number)

## Question

CFG820 set the stiffness floor L★ ≥ 23.96 / 24.72 pc (canonical / alt) from NGC 2419, Pal 4 and Pal 14 using ν_RAR
and the additive EFE recipe (standard-MOND machinery). E4 reran it with the native law, no recipe: 28.85 / 29.12 pc
isolated, 23.87 / 24.66 with the recipe, and one shared Υ_V shifted ±0.15 dex spans 20–42 pc. C3 lists the EFE-aware
floor as OPEN. This lane **solves the stiffened field equation in the Galaxy's field** for each cluster's own mass profile,
predicts the line-of-sight dispersion as a function of L★, and scores it against the raw dispersions with a
**per-cluster** Υ_V marginalised over a stated SPS prior and binaries treated as in CFG334.

## The theory solved (FRAMEWORK-NATIVE; no new posit)

The healthy C4-literal static sector (C5; C6 frozen criteria, commit 1b2ced55a4): γ_F = 0, longitudinal stiffness
γ_L = K L★²/2, K = 4πG, a₀ units for accelerations:

    (L)   ∇²Φ = Kρ + ∇·p          (P_L)  ∇Φ + (L★²/2) ∇(∇·p) = a₀ p / (a₀ − |p|).

(P_L) makes h(p) an exact gradient ∇χ with χ = Φ + (L★²/2)∇·p, so p = ∇χ / (1 + |∇χ|/a₀). With Φ = Φ_N + ψ the system
is exactly two scalar equations (to be confirmed by sympy in K1, not assumed):

    ∇²ψ = ∇·p(∇χ),      χ = Φ_N + ψ + (L★²/2) ∇·p(∇χ).

The stars feel ∇Φ = ∇Φ_N + ∇ψ. L★ → 0 is AQUAL with μ = x/(1+x) (E2); L★ → ∞ is Newton. The Galaxy enters as the
uniform background ∇χ_e = g_e ẑ (total external field), perturbations decaying at infinity. D7d's vector-Laplacian form
(γ_F = γ_L) is not solved here; it coincides with this one only in the isolated (curl-free) case.

## Method

- **Own axisymmetric solver** (spherical (ln r, θ) finite volume, Newton with an exact sparse Jacobian), unknowns δχ, δψ
  about the background; fluxes are p(v) − p(v_e) so the uniform background has no discrete source. Inner boundary
  r_in = 1e-3 a (zero perturbation flux), outer boundary r_out ≥ 1e4 a (monopole Robin ∂_r f = −f/r embedded; exact
  Gauss flux for the isolated validation). Units: a = Plummer scale, accelerations in a₀. D7d/C6 code is not imported.
- **Mass profile:** Plummer with a = r_h,l (CFG332's choice; the Baumgardt 3D r_h,m / r_h,l = 1.33 vs Plummer 1.305),
  mass = light (no segregation), M = Υ_V L_V.
- **Dispersion (primary estimator E-P):** isotropic spherical Jeans on the solid-angle monopole of the radial field,
  projected σ_p at the RV bin's mean radius R_bin (raw profile table: Pal 4 26.71″, Pal 14 77.12″, Pal 3 24.15″ at the
  Baumgardt distance; NGC 2419 at R = r_h,l, which is where CFG332 interpolated its value).
  Variants (reported, not verdict): **E-V** global virial σ² = −(1/3M)∫ρ r·g dV (exact orientation average; depends on the
  monopole only) and **E-W** the record's Wolf estimator σ² = r g_r(r)/3 at r = (4/3) r_h,l.
- **External field (MW):** A60's framework MW, Hernquist M_b with a_H = 3 kpc, the law g = (g_N/2)(1 + √(1 + 4a₀/g_N)),
  at the cluster's R_GC. Bracket: **E_lo** M_b = 4e10 M☉, **E_mid** 6e10 M☉ (A60 / CFG332), **E_hi** the Hernquist mass whose
  law field at 8 kpc equals the record's kinematic E2 total 2.2 × 9.36e-11 m/s² (D7b inputs), per footing.
- **Υ_V priors (per cluster, independent):** **P1** log-normal centre 1.6, 0.15 dex (CFG332 SPS); **P2/P3** CFG332 Route 2
  MF-slope branches K and S (centres and widths from `cfg332_globulars_results.json`, route2.ups_mf). Marginalised on a
  fixed Υ grid (0.2–6, log), σ_pred interpolated in log Υ.
- **Binaries (as CFG334):** single epoch, f_b = 0.3 primary (0.1 / 0.5 and 0 reported), DM91 log P ~ N(4.8, 2.3) d,
  flat q ∈ [0.1, 1], thermal e, M₁ = 0.8 M☉, a(1 − e) ≥ 30 R☉, a < 0.1 pc; CFG334's deconvolved ML estimator. Per-star
  error e_c per cluster: the value for which the f_b = 0 simulated spread of ln σ̂ at σ_int = σ_obs equals eso/so
  (e_c = 0 if the binomial spread already exceeds it). The likelihood of the observed σ is the KDE density of the simulated
  ln σ̂ at ln σ_obs, as a function of σ_int (fixed seed). This replaces eso (no double count).
- **Statistic:** χ²(L★) = −2 Σ_c ln ∫ prior(Υ) p(ln σ_obs | σ_pred(Υ, L★)) dΥ. L★ grid: 0 (AQUAL), 24 log points 2–500 pc,
  ∞ (Newton). L★_95 = the lowest L★ with χ² − χ²_min ≤ 3.84 (χ²_min over the grid incl. Newton), crossing interpolated in
  ln L★. Primary set: NGC 2419, Pal 4, Pal 14 (as CFG820); all four reported.
- Footings never pooled: canonical a₀ = 9.36e-11, alt 1.13e-10 m/s². Budget: single thread, nice, < 1 GB RSS.

## Checks (script prints `Kn PASS/FAIL value threshold`; exit 0 iff all pass)

- **K1** sympy: (a) the scalar reduction satisfies (L) and (P_L) for arbitrary χ, ψ; (b) its linear Fourier response about
  a uniform background equals C6's frozen kernel ψ̂/Φ̂_N = m/(1 − m + κ²m/2), m = k̂·(∂p/∂v)·k̂, κ = kL★; (c) at L★ = 0 it is
  AQUAL ∇·[μ(|∇χ|)∇χ] = ∇²Φ_N with μ = x/(1+x). All residuals 0.
- **K2** isolated (g_e = 0): the 2D solver's monopole field and σ_p equal an independent 1D radial BVP of the same
  equations to < 2e-3 at Λ = L★/a ∈ {0.5, 2, 8} and y_M ∈ {0.04, 3} (Pal 14-like, NGC 2419-like).
- **K3** isolated L★ = 0: 2D σ_p equals the algebraic law (exact for spherical AQUAL) to < 2e-3.
- **K4** linear EFE (y_M = 1e-4 x_e, x_e = 0.1): the 2D monopole radial field at r = a equals the Fourier route (C6 kernel,
  Plummer source, orientation-averaged) to < 2e-2 at Λ ∈ {0, 1, 4}.
- **K5** Newton limit: Λ = 1e4 gives σ_p within 2e-3 of the Newtonian Jeans value.
- **K6** convergence at NGC 2419 / Pal 14, E_mid, canonical, Λ = 1: doubling N_r and N_θ and r_out × 10 changes σ_p by < 5e-3.
- **K7** Jeans numerics: Newtonian Plummer global σ² = (3π/64) G M / a to < 1e-3, and the luminosity-weighted σ_p² over all
  R equals the virial value to < 2e-3.
- **K8** binaries: CFG334's primary (N = 22, σ_int 0.75, e 1.0, f 0.3) reproduced: P(σ̂ ≥ 1.70) within 0.03 of 0.26 and
  median within 0.05 of 1.16 km/s.
- **K9** bridge: E4's N1 machinery (Wolf, ν_L, CFG691 S(s), Υ 1.6, CFG820 χ²) re-implemented here gives 28.853 / 29.123 pc
  to ±0.02.
- **K10** peak RSS < 1 GB.

`--mutate`: the 2D solver uses L★² instead of L★²/2 in the stiffness term (the 1D BVP and Fourier route untouched).
It must break K2 and/or K4. Outputs `*_MUTATE.out`, `*_results_MUTATE.json`.

## Verdict lines

- **V1 (number):** L★_95 per footing at the central cell (P1, E_mid, f_b 0.3, E-P), and the **band** = [min, max] over the
  9 cells P1–P3 × E_lo/E_mid/E_hi (f_b 0.3, E-P).
- **V2 (window):** the band against [20, 90] pc: **ABOVE** (band min > 90), **INSIDE** (band ⊂ [20, 90]), **BELOW**
  (band max < 20), else **STRADDLES** the named edge. Per footing.
- **V3 (move):** **FLOOR MOVES** if the central L★_95 differs from CFG820's 23.96 / 24.72 by > 10 %, else **FLOOR HOLDS**.
- **V4:** whether AQUAL (L★ = 0) is excluded (Δχ² > 3.84) and whether any finite L★ beats Newton by Δχ² > 3.84
  (an upper bound / detection). If no grid L★ is excluded: **NO BOUND**.
- Reported only: f_b ∈ {0, 0.1, 0.5}, estimators E-V and E-W, the all-four set, per-cluster Δχ².
- **UNDECIDED** if any of K2–K6 fails (the solve is not validated): say which.

Input classes are listed in the README ledger: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM / STANDARD-MOND.
κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the
framework over ΛCDM.
