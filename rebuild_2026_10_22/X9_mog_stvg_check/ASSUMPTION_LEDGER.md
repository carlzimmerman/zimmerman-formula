# X9_mog_stvg_check: assumption ledger (written before any number; committed with the frozen criteria)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT.
"Inherited" = taken unchanged from P4 (`P4_v3_galaxy_tiles/FROZEN_CRITERIA.md` §3), F1 (`F1_cluster_cores/ASSUMPTION_LEDGER.md`)
or X2 (`X2_cluster_outskirts/ASSUMPTION_LEDGER.md`) and classed as there. Here FRAMEWORK-NATIVE means native to the
programme's law (used only for the reference rows); MOG's own ingredients are LITERATURE-INPUT.

## A. MOG (the theory under test)

| # | ingredient | class | source | role |
|---|---|---|---|---|
| A1 | point-mass law a = −G_N M/r² [1 + α − α e^{−μr}(1 + μr)]; G_eff → G_N at r → 0 | LITERATURE-INPUT (PROVISIONAL web lookup) | MR13 Eq. 33; MRT18 Eq. 24 | sph and disc engines |
| A2 | superposition over extended sources with α, μ constant (weak-field linearity) | LITERATURE-INPUT | MR13 Eqs. 31–33 | all predictions |
| A3 | discs razor-thin, superposed over Σ (MR13 Eq. 34) | LITERATURE-INPUT (published practice) | MR13 §4 | SPARC PRIMARY geometry |
| A4 | α = 8.89 ± 0.34, μ = 0.042 ± 0.004 kpc⁻¹ (fit to 9 THINGS galaxies, then fixed) | LITERATURE-INPUT (fitted by MR13, not here) | MR13 abstract, §4.1 | verdict set U; ±1σ corners for qualifiers |
| A5 | the same α, μ for clusters | LITERATURE-INPUT | MR14 abstract, Eq. 11, Fig. 2 | cluster tile |
| A6 | light does not feel the vector (Yukawa) force; deflection = GR with G = (1 + α)G_N; M_L = (1 + α)M | LITERATURE-INPUT | MRT18 §2.4 Eqs. 29–32; MR13 Eq. 21 | P-PH (cluster PRIMARY) |
| A7 | "lensing follows the dynamical G_eff" (coordinator brief) | not the published assumption (A6) | brief | variant V-DYN only |
| A8 | Yukawa term negligible inside clusters beyond ~100–300 kpc | LITERATURE-INPUT (claim) | MR14 §4.3 | P-PH vs V-DYN comparison (reported) |
| A9 | no external-field effect (linear weak-field equations) | LITERATURE-INPUT (consequence of A2) | MR13 Eqs. 21–24 | X2 (c1) and P4's EFE inapplicable |
| A10 | parameter-free α(M) = 19 M/(√M + E)², μ(M) = D/√M, D 6250 M☉^{1/2} kpc⁻¹, E 25 000 M☉^{1/2} | LITERATURE-INPUT | MRT18 Eqs. 8–9, 11–14, 18 (Moffat & Toth 2009) | side reading S1 only |
| A11 | MSTG cluster running G(r), M₀ = 58.8e14 (M_gas/1e14)^0.39 M☉, r₀ 139.2 kpc (or r_out/10); galaxies M₀ 9.6e11 M☉, r₀ 13.92 kpc | LITERATURE-INPUT (fitted by BM06 on 106 clusters / 101 galaxies) | BM06 Eqs. 23, 31, 33 | side reading S2 only |
| A12 | S2 lensing = BM06 dynamical mass | assumption (BM06 gives dynamics only) | this lane | S2 only, labelled |
| A13 | S1 galaxy mass M = 1.33 M_HI + Υ L[3.6]; cluster mass = 1.2 × gas inside 3 Mpc | assumption (declared) | SPARC Table 1; F1 | S1 only |

## B. SPARC tile (inherited from P4 T1)

| # | ingredient | class | source | role |
|---|---|---|---|---|
| B1 | SPARC V_obs, eV, R; V_gas (1.33 M_HI) | RAW | `real_research/data/sparc_data/*_rotmod.dat` | inherited |
| B2 | V_disk, V_bul (3.6 μm decompositions with Lelli's disc thickness), 1.4 bulge factor, Υ range 0.30–1.20 | SURVEY-CALIBRATION | rotmod; CFG4; CFG695 | inherited; thin-disc δg uses V_disk as an in-plane field (thickness enters g_N exactly, δg only at O((μ z₀)²)) |
| B3 | D, e_D, i, e_i, L[3.6], M_HI, Q | SURVEY-CALIBRATION | `SPARC_Lelli2016c.mrt` | inherited (χ² line, classes, S1 mass) |
| B4 | mask g_bar, g_obs > 0; weights (V/eV)²; per-galaxy Υ; covariance χ² with distance and inclination offsets | RAW statistics / P4 convention | P4 `fit_sample`, `pooled` | inherited, exec'd read-only |
| B5 | spherical mass function (linear V² between points, uniform core, constant mass beyond the last point) | approximation (declared by P4) | P4 `sparc_mass_fun` logic | G-SPH variant; bulge in PRIMARY |
| B6 | g_N ∝ R inside the first point, ∝ R⁻² beyond the last | approximation (declared here; matches B5's "no mass beyond") | this lane | disc engine extension |
| B7 | P4's line rms ≤ 0.110 dex, median Υ ∈ [0.50, 0.80]; χ² line 0.90 / 0.75 at p ≥ 0.001 | RAW statistics (frozen by P4) | P4 FROZEN_CRITERIA T1 | inherited unchanged |
| B8 | law reference: ν₁ (μ = x/(1+x)), footings | FRAMEWORK-NATIVE (κ = ½ FITTED) | P4 | reproduction (R2) only |

## C. Cluster tile (inherited from F1 / X2)

| # | ingredient | class | source | role |
|---|---|---|---|---|
| C1 | KiDS-1000 shear, Σ_crit from point Z_B, m = −0.01, randoms | RAW / SURVEY-CALIBRATION | F1 `esd()`; replay npz | inherited (X2 R1/R2) |
| C2 | distances: DESI DR2 D_M/r_d × 101.54/h, h 0.672 / 0.686 | RAW × FRAMEWORK-NATIVE (native h) | F1 `DM()` | inherited (both h cells) |
| C3 | eRASS1 Mgas500 (rescaled q^{5/2}), R500 (× q), positions, miscentring | RAW / SURVEY-CALIBRATION; R500 LCDM-PROCESSED | `real_research/data/erass1cl_primary_v3.2.fits` via the npz | inherited |
| C4 | gas β = 2/3, r_c = 0.15 R500, cut at 3 Mpc (C0); CFG814 r⁻³ beyond 2.2 R500 (C\*) | LITERATURE-INPUT (assumed shape) | F1 `gas_mass`; X2 `gas` | inherited |
| C5 | stars f* = 0.20 × gas | LITERATURE-INPUT | F1 | inherited |
| C6 | F1 data boost (B < 1, applied); clipped convention reported | RAW (measured) / convention | F1, X2 | inherited |
| C7 | reduced shear forward model with the model's own Σ (C\*) | RAW estimator correction | X2 (d), `redfac` | inherited; MOG's Σ = (1 + α)Σ_N |
| C8 | null-test systematics (cross shear, R − R) in σ and χ² (C\*) | RAW (conservative allowance) | X2 (e) | inherited |
| C9 | A_band, jackknife (30 RA patches), profile χ² bins 3–7 + Hartlap, line 11.07; |Z| ≤ 2 | RAW statistics | X2 `stats`; X2 §3 | inherited unchanged |
| C10 | external field (c1) | FRAMEWORK choice for the law | X2 | not applicable to MOG (A9) |
| C11 | law reference: spherical AQUAL μ = x/(1+x), footings | FRAMEWORK-NATIVE (κ = ½ FITTED) | F1, X2 | reproduction (R3, R4) only |
| C12 | Newtonian baryons (F1 `newton_h070`) | RAW-based model | F1 JSON | reproduction R5; MOG P-PH is (1 + α) × this kind of prediction |

## D. What this lane does not assume

- No α, μ, Υ (beyond P4's per-galaxy convention), f*, gas factor or boost is fitted or scanned here.
- No ΛCDM-calibrated halo or concentration enters any graded prediction.
- No dark-matter particle; MOG's extra fields are fields, not a particle species.
