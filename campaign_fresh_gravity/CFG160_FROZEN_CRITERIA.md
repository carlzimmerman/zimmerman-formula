# CFG160 — KURVS a₀(z) with the simulation-calibrated pressure-support factor of Kretschmer et al. 2021 (P4). FROZEN CRITERIA

Written 2026-09-29, before any number under this prescription has been computed. CFG141's P0, P2 and P3 results are committed and known to the author. That is why the prescription below is taken verbatim from the published fit, with every free choice fixed here. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## Why

- **Where CFG141 stands** (corrected a843be430): KURVS's a₀(z) verdict rests on the outer pressure-support model at 4–7 R_d, where the correction dominates V_c.
  - Under P2 (a self-gravitating isothermal layer, α = 2R/R_d), both readings need about 4 M* of cold gas.
  - Under P3 (a fixed scale height, α = R/R_d plus the gradient term), at the paper's gas, flat a₀ is 3.5σ high and the rival is 1.3σ high.
- **The published calibration:** Kretschmer, Dekel, Freundlich, Lapiner, Ceverino & Primack 2021 (MNRAS 503, 5238; arXiv:2010.04629).
  - They used the VELA cosmological zoom simulations at z = 1–5 and stellar masses of 10^8.5 to above 10^11 M☉; their radial profiles are analysed above 10^9.5.
  - They found the self-gravitating-disc prediction α = 3.36 r/R_e "invalid in the simulations", because the dominant spheroid gives a weaker gradient.
  - They fit α for gas in discs (their Table 1, read verbatim from the ar5iv HTML rendering through a summarising fetch that returned the rows verbatim):
    - α(x) = −0.146 x² + 1.204 x + 1.475, with x = R/R_e − 1;
    - R_e is the half-mass radius of the analysed component;
    - the scatter is 40%.
  - It is the one simulation-calibrated high-z prescription at hand. It is adopted as published, not tuned.

## Prescription P4 (declared)

- **The correction:** V_c² = V_obs² + α(x) σ_out².
  - σ_out is CFG141's measured outer dispersion at R_max. It is the observed σ, taken as the local radial dispersion, as in P2.
- **The radius:**
  - **Primary:** x = R_max/R_eff − 1, with R_eff the paper's HST near-infrared effective radius (CFG140 uses R_d = R_eff/1.68). The tracer being corrected is Hα, whose extent follows star formation.
  - **Variant (reported, not the headline):** R_e,gas = 2 R_eff, CFG140's declared cold-gas scale in its mass model.
- **Validity:** Kretschmer et al.'s profiles extend to about 5 R_e (x ≤ 4). Where x > 4 (e.g. SPARC anchor points), α is held at α(4) = 3.955, because the quadratic turns over beyond its fitted range. Where x < 0, α(0) = 1.475 is used.
- **The SPARC anchor** keeps CFG140's declared σ = 10 km/s and uses the same P4 formula, with R_e = 1.68 R_disk.
- **The scatter:** α × 0.6 and α × 1.4 are reported as a systematic band. They are not the headline.
- **Everything else is CFG141's pipeline, exec'd read-only:**
  - the KURVS sample, baryons, g_obs, the gas bracket μ ∈ {0.25, 0.67, 1.5, 4}, the stellar-mass bracket δ ∈ {−0.2, 0, +0.2};
  - both a₀ footings, the SPARC same-pipeline anchor, the pooling and the error model;
  - σ_out and its error, from the data chat's extraction (94e4a5181), with clipped pixels excluded as in CFG141.

## Checks

- **C1 CONTROL:** with α(x) replaced by the P2 value 2R_max/R_d, the P4 code path reproduces CFG141's committed P2 grid exactly (to 1e-12).
- **C2 CONTROL:** the α(x) implementation returns α(0) = 1.475, α(1) = 2.533 and α(4) = 3.955.
- **R0 POWER** (printed before any g_obs): as CFG141, under P4.
- **H1 [HEADLINE; MUTATE must change it]:** under P4 the framework's flat a₀ is NOT disfavoured. It fails only if Δ′_flat > +2σ in every one of the 24 P4 cells (4 μ × 3 δ × 2 footings).
- **H2 (reported verdict):** under P4 the rival a₀ ∝ H(z) is disfavoured: Δ′_H < −2σ in every P4 cell.

## Reported rows

- **R1:** the P4 grid, anchor-corrected, with the cells favouring each reading. P0, P2 and P3 from CFG140/141 are shown beside it, unchanged.
- **R2:** the decision cell (μ = 0.67, the paper's 40% molecular; δ = 0; canonical): Δ′_flat and Δ′_H, each with its σ, under P4, the scatter band and the R_e variant.
- **R3:** per galaxy: x, α, V_c²/V_obs² under P4 against P2, and Δ_flat and Δ_H in the central cell.
- **R4:** the R_e,gas = 2 R_eff variant and the α × 0.6 / × 1.4 band, as full verdict rows.

## MUTATE

MUTATE=1 multiplies every KURVS v_last by 10^0.3 (g_obs × 4). H1 must fail, and the script must exit 1.

## Readings (declared)

- **P4 is one published simulation calibration.** Its α carries 40% scatter. It was fitted to VELA galaxies, whose spheroids are dominant. KURVS's ten are rotation-supported discs, and whether VELA's α applies to them is untested. Every P4 statement is therefore conditional on that calibration, and on the gas, which remains unmeasured (CFG142 is separate).
- **Flat within 2σ at the decision cell, and the rival below −2σ there:** a Kretschmer-conditional lean toward flat a₀ at z ≈ 1.5. It is NOT "the data favour the framework".
- **The rival within 2σ at the decision cell, and flat above +2σ there:** a Kretschmer-conditional lean toward the rival.
- **Both within 2σ, or both outside:** non-diagnostic under P4.
- **Across the whole grid,** H1 and H2 keep their CFG141 meaning.
- **Untested (declared):**
  - whether VELA's α applies to KURVS's discs;
  - anisotropy (σ_R ≠ σ_z);
  - the tracer's true half-mass radius (only R_eff and 2 R_eff are tried);
  - beam smearing of the observed outer σ;
  - non-equilibrium;
  - the gas;
  - the COSMOS half of KURVS;
  - Dalcanton & Stilp's (2010) prescription, which was not read.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
