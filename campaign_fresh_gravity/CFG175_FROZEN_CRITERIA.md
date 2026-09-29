# CFG175 — a third a₀(z) law, a₀ ∝ t(z)/t₀ (CFG174's accumulation reading), through the KURVS/KROSS pipeline under P0, P4 and the CFG162 s-axis. FROZEN CRITERIA

Written 2026-09-29, at the orchestrator's request, before any number of this lane was computed. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## Forking paths (stated first)

- **The data have been seen many times.** CFG140, 141, 142, 160–165, 167, 168 and 170 analysed these samples. The flat and rival rows are known:
  - the KURVS decision cell: flat +0.144, rival −0.006;
  - the break-evens at s = 1: KURVS 2.109 / 0.621, KROSS 0.636 / 0.052;
  - the crossing s_mid = 0.67.
- **The law T is post-hoc too.** The orchestrator's chat wrote it in CFG174 (eb2e3e066), from the owner's picture, with the KURVS results already known to that chat.
- **My hand expectation, disclosed before any number:**
  - T predicts less than flat at z ≈ 1.5 (a₀ lower by 0.51 dex; roughly 0.15–0.2 dex lower g_pred in the transition regime).
  - So T should fit near s ≈ 0 (P0) at a moderate gas fraction, and need μ well above 2 under the published prescriptions.
  - Whatever the numbers show is reported.

## The laws

- **flat:** a₀(z) = a₀.
- **rival:** a₀(z) = a₀ E(z).
- **T:** a₀(z) = a₀ t(z)/t₀, where t is the flat-ΛCDM age on the pipeline's own background (CFG140's E(z), Ω_m = 0.315):
  - t(z)/t₀ = asinh(√(Ω_Λ/Ω_m) (1+z)^(−3/2)) / asinh(√(Ω_Λ/Ω_m)).
  - The ratio does not depend on H₀.
- The pipeline's kernel and the canonical a₀ footing are unchanged.

## The pipeline (unchanged)

- **Code:** CFG141's pipeline, exec'd read-only and unmutated in every mode; CFG160's P4 functions copied verbatim; CFG170's root-finding.
- **KURVS:** the ten discs with measured σ_out.
- **KROSS:** the 390 discs of CFG140's selection, with σ₀ at R = 2 r_im.
- **The anchor:** SPARC with its measured gas, at the same s and under the same law (each law evaluated at the SPARC redshifts). The cell is δ = 0, canonical.
- **The pressure axis:** s ∈ {0 (P0), 1 (P4, Kretschmer), 1.42, 1.62, 1.69, 3.00}. These are CFG162's placements, reproduced by CFG168. The continuous s-axis is used for the fit points.
- **The gas:**
  - CFG162's bracket, μ ∈ {0.25, 0.67, 1.5, 4};
  - break-evens μ_be in [0.01, 30] (brentq on a log grid, as in CFG170), with 1σ intervals from the roots of Δ′ = ±σ.
- **The measured gas evidence (declared here, not re-derived):**
  - CFG164's primary prior: median μ 1.01, 16–84% range 0.60–1.69;
  - its most gas-rich declared variant (HI equal to the molecular gas): median 2.05, range 1.19–3.47;
  - KURVS-15's dust limit (CFG163): μ < 1.90 nominal, < 3.8 with the gas-to-dust ratio doubled (one disc).
- **The GAS CEILING is 3.47:** the 84th percentile of the most gas-rich declared prior.

## Statistics (reported for all three laws)

1. **The KURVS decision cell** (μ = 0.67, s = 1): Δ′ ± σ and z for each law. The same at s = 0.
2. **The map:** Δ′ ± σ for each law, at each s and each μ in the bracket (KURVS); and KROSS at μ = 0.67.
3. **Break-evens:** μ_be with its 1σ interval, per law and per s, for KURVS and for KROSS. "No break-even" if there is no root in [0.01, 30].
4. **The fit point on the s-axis** at μ = 0.67: s₀(law) is the root of Δ′_law(s) = 0 in s ∈ [0, 6] (Δ′ increases with s).
   - Report "s₀ < 0" if Δ′_law(0) > 0, and "s₀ > 6" if Δ′_law(6) < 0.
   - For KURVS and for KROSS.
5. **The two-epoch ratio for T** (CFG170's statistic): R_T = μ_be(KURVS)/μ_be(KROSS) at each s.
   - Compared with CFG170's brackets: in-repo 2σ [0.73, 1.39]; literature, abstract-level, [1.61, 2.42].
   - Reported, not the headline.

## The verdict rule (declared; applied to all three laws alike)

- **At each s, a law is:**
  - "**gas-excluded**" if its KURVS break-even's lower 1σ edge exceeds the gas ceiling 3.47, or if it has no break-even because it under-predicts even at μ = 30;
  - "**gas-allowed**" if its KURVS break-even's 1σ interval overlaps [0, 3.47];
  - "**over-predicts**" if it has no break-even because Δ′ < 0 already at μ = 0.01.
- **The rule is printed for flat and the rival alongside T,** so it is not aimed at T. For example, flat at s = 3 has break-even 6.85.
- **HEADLINE:** the status of the three laws at s = 1 (Kretschmer, CFG160's decision prescription) and at each published placement (1.42–3.00). The declared summary sentence:
  - "**T is gas-excluded under every published prescription**" if T is gas-excluded at s = 1, 1.42, 1.62, 1.69 and 3.00;
  - with "**and gas-allowed only without pressure support**" added if T is also gas-allowed at s = 0;
  - otherwise the matrix is reported as it is.
- **"Strongly disfavoured"** (the orchestrator's phrase) is used only if both hold:
  - T is gas-excluded at every published placement;
  - at the decision cell (μ = 0.67, s = 1), T under-predicts by more than 3σ (z > +3).

## Checks

- **C1 CONTROL:** with CFG174's cosmology (Ω_m = 0.3111), t(z)/t₀ reproduces CFG174's Q3 values, −0.33 / −0.51 / −0.72 dex at z = 0.85 / 1.5 / 2.5, to 0.01 dex. The values at the pipeline's Ω_m = 0.315 are printed.
- **C2 CONTROL:**
  - flat and the rival at the KURVS decision cell reproduce CFG160 (+0.1441 / −0.0060, to 4 decimals);
  - their break-evens reproduce CFG170 (KURVS 2.109 / 0.621 at s = 1; KROSS 0.636 / 0.052, to 1e-3).
- **C3 CONTROL:** T's SPARC anchor differs from flat's by less than 0.01 dex. The anchor sits at z ≈ 0, where the laws coincide.
- **R0 POWER** (printed before any verdict): Δ′_T − Δ′_flat at the decision cell, against σ.

## MUTATE (two pinned controls of the plumbing)

- **MUTATE=1:** T is replaced by flat (t(z)/t₀ → 1). T's rows must then equal flat's to 1e-9, and the headline must change.
- **MUTATE=2:** T is replaced by the rival (E(z)). T's rows must then equal the rival's to 1e-9.
- Each run exits 0 when it behaves as required.

## Readings (declared)

- **T's standing depends on the outer pressure support and the gas,** as flat's and the rival's do. The lane reports where on the (s, μ) plane T fits, plainly, in either direction.
- **This is not a kill line for the owner's picture.** T is one reading of CFG174's Q3, the accumulation reading. A non-accumulating reading makes no a₀(z) prediction here.
- **Untested (declared):**
  - pressure beyond the placed prescriptions;
  - the COSMOS half of KURVS;
  - KROSS's gas;
  - t(z) beyond flat ΛCDM.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour any model, or that the theory is closed.
