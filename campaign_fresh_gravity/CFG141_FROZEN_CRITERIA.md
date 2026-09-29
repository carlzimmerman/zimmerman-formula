# CFG141 — KURVS a₀(z) with each galaxy's MEASURED outer dispersion: the pressure-support correction from σ(R) at R_max. FROZEN CRITERIA

Written 2026-09-29, before this lane has seen any extracted σ(R) value. The data chat is extracting the profiles from the paper's vector figures, which are local files already on disk, and will send only a commit hash. This file is committed before that extraction is opened. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## Why

CFG140 was NON-DIAGNOSTIC because the outer pressure support was unmeasured. Its two scenarios pulled opposite ways:
- with no correction, a₀ ∝ H(z) over-predicts;
- with the constant-σ₀ Burkert correction, flat a₀ under-predicts.

The paper gives one σ₀ per galaxy. Its only radial test (outer-disc σ over full-profile σ = 1.13 ± 0.26) stops at R'_2.2D, well inside R_max. The per-galaxy Hα σ(R) major-axis profiles exist only as plotted curves. This lane replaces the constant σ₀ by each galaxy's own σ near R_max.

**The physics (declared):** for an isotropic, isothermal, self-gravitating disc layer, ρσ² ∝ Σ², so the asymmetric-drift term is 2σ²R/R_d with the LOCAL σ(R). The radial gradient of σ cancels. Using the Burkert form with σ = σ(R_max) is therefore the consistent generalisation, not a new assumption.

## Inputs

- **CFG140's pipeline,** verbatim: `CFG140_kurvs_a0z.py`, exec'd read-only. It supplies the samples, the baryons, g_obs, the SPARC anchor, the grid, the pooling and the error model.
- **The data chat's extraction** of the Hα σ(R) profiles (its commit). This lane reads it only after this file is committed.

## σ_out, the outer dispersion (declared)

- **Radius units:** kpc. An arcsec axis is converted with the galaxy's angular scale at its z_Hα (Planck18).
- **Two-sided profiles:** where both sides of the major axis are plotted, the two sides are averaged at |R|.
- **Reaching R_max:** if the profile reaches R_max, σ_out is its value there by linear interpolation in R.
- **Ending inside R_max:** σ_out is the error-weighted mean of the outermost three points (constant extrapolation). A galaxy whose profile does not reach 0.5 R_max is dropped, and the count is reported.
- **Beam smearing:** the plotted σ is used as plotted. If the figures show observed rather than corrected σ, this is a declared caveat: beam-smearing inflation is smallest at 4–7 R_d.
- **The error on σ_out:** from the plotted error bars (interpolated); where none are plotted, a declared 20%.

## Pressure-support variants

- **P2 (primary):** V_c² = V_obs² + 2 σ_out² (R_max/R_d), the self-gravitating isothermal layer with the local σ.
- **P3 (variant, a layer of fixed scale height):** V_c² = V_obs² + σ_out²(R_max/R_d) − R dσ²/dR at R_max. The gradient is a linear fit to the outermost three points. A negative correction is capped at zero, as declared.
- **P0 and P1** are re-reported unchanged from CFG140 for continuity.
- **The SPARC anchor** has no σ profile, so it uses its declared 10 km s⁻¹ in the same P2 and P3 formulas.

## Checks

- **C1 CONTROL:** with σ_out set to the tabulated σ₀ for every galaxy, P2 reproduces CFG140's committed P1 grid exactly (to 1e-12). The only change is σ.
- **C2 CONTROL:** for every selected galaxy the extracted profile is finite and positive, and its radius range overlaps the velocity table's R_max consistently. Per galaxy it is reported whether the profile reaches R_max, reaches 0.5 R_max, or is dropped.
- **R0 POWER** (printed before any g_obs): as CFG140, with σ_out's error included under P2.
- **H1 [HEADLINE; MUTATE must change it]:** under P2 the framework's flat a₀ is NOT disfavoured. It fails only if Δ′_flat > +2σ in every one of the 24 P2 cells (4 μ × 3 δ × 2 footings).
- **H2 (reported verdict):** under P2 the rival a₀ ∝ H(z) is disfavoured: Δ′_H < −2σ in every P2 cell.

## Reported rows

- **R1:** the P2 and P3 grids, anchor-corrected, with the cells favouring each reading.
- **R2:** per galaxy: σ₀ (tabulated), σ_out (extracted), R_max/R_d, the P2 correction factor V_c²/V_obs², and Δ_flat and Δ_H in the central cell.
- **R3:** the ratio σ_out/σ₀ across the sample, which tests the constant-σ assumption at R_max.
- **R4:** the verdicts under P3.

## MUTATE

MUTATE=1 multiplies every KURVS v_last by 10^0.3 (g_obs × 4). H1 must fail and the script must exit 1.

## Readings (declared)

- **Under P2, the rival disfavoured in every cell and flat not:** with the measured outer dispersion, a₀ ∝ H(z) is disfavoured across the gas and stellar-mass brackets. This is conditional on the isothermal-layer assumption; P3 is the check, and CFG52's correlated floor applies.
- **Under P2, flat disfavoured in every cell:** flat a₀ is disfavoured at z ≈ 1.5. A result beyond 3σ in every cell would be a kill line for the framework's flat-a₀ law.
- **Otherwise:** NON-DIAGNOSTIC, with the gas bracket then the dominant ambiguity (no measured gas exists for these discs; the data chat found none).
- **Untested (declared):**
  - anisotropic dispersion (σ_R ≠ σ_z);
  - non-isothermal vertical structure beyond P3;
  - beam smearing of the plotted outer σ;
  - the COSMOS half of the survey.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
