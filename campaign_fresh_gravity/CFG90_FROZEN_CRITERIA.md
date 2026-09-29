# CFG90 — does B's own stellar-mass calibration account for the KiDS early/late split? FROZEN CRITERIA

Written 2026-09-29, before any number of this lane was computed. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## Why

The KiDS early/late split is B's one failure specific to B in shared machinery. It survives a data-driven covariance (CFG88: 4.4σ in the 1-halo bins).

- **What would close it.** CFG61's R4, recomputed by CFG77 under the stated formula, found that B's colour-blind law fits the split if early-type lenses carry more baryons than their catalogue stellar masses say, relative to late types: acceptable from about +25% (p > 0.0027) and from about +50% (p > 0.05).
- **Why stars would do it.** Stellar mass placed inside the lens acts as a point mass at these radii (K1 starts at 44 kpc), which is exactly what that diagnostic assumed.
- **What B already says.** B's own dynamics already calibrate the stellar M/L of early types (CFG33's α_dyn(σ), from ATLAS3D JAM masses under the law) and of discs (SPARC's Υ_disk).

**The frozen question:** with no new constant, does that calibration supply the differential offset, so that B's law fits the split?

## The calibration (declared once)

- **Early types:** true M* = α_dyn,foot(σ) × M_Salp.
  - α_dyn,foot(σ) = 10^(a + b (log σ − 2.3)), the CFG33 / CFG55-C2 fit of log(M_law / M_Salp) against log σ_e. It is recomputed here on both footings with CFG55's own `law_mass` over the same ATLAS3D set (qual ≥ 1, N = 187). The canonical fit must reproduce the committed slope +0.204 and ×0.72 / ×0.83 / ×0.90 at σ = 100 / 200 / 300 km/s.
  - σ for a KiDS lens comes from an ordinary least-squares fit of log σ_e on log M_Salp over the same ATLAS3D set, with M_Salp = (M/L)_Salp L_r.
  - M_Salp = 10^0.25 × M*_Chabrier. The KiDS stellar masses (LePhare) are taken as Chabrier-IMF masses.
  - So δ_early(M*) = log10 α_dyn(σ(M*)) + 0.25.
- **Late types (discs):** δ_late = log10(Υ_SPARC / 0.5).
  - Υ_SPARC is B's committed SPARC fit with ν_mono: 0.61 canonical, 0.57 alt (CFG4_galaxy_law).
  - 0.5 is SPARC's population-synthesis reference Υ_3.6 for a Chabrier-like IMF.
  - So δ_late = +0.086 dex canonical and +0.057 dex alt.
- **What changes.** Only the stellar mass: M_b,true = 10^δ M* + M_gas, with M_gas = f_cold(M*) M* as in CFG61 (Brouwer's gas relation at the catalogue M*).
- **How the true mass enters.** Each lens keeps its measured-mass radius for its g_bar bin, as in CFG61's R4. The law's ΔΣ at the true M_b is interpolated linearly in log M_b between CFG61's profile nodes, not quantised, together with the true-mass point-mass term.
- **Everything else** is CFG61's forward model, executed read-only.

## Data and statistic

- **The released split:** Brouwer+2021 Fig. 8 colour bins with its 30 × 30 covariance on K1 (CFG61's seven 1-halo bins). C_D = C_ee + C_ll − C_el − C_le. χ² = (D_obs − D_model)ᵀ C_D⁻¹ (D_obs − D_model), with 7 degrees of freedom.
- **The re-measured split:** the June 2026 re-measurement on the same K1, with CFG88's 50-patch jackknife covariance of the difference (Hartlap 41/49). The data files are git-ignored; they are listed in CFG61 and CFG88.

## Checks

- **C1 CONTROL:** with δ = 0 for both classes, the new stack reproduces CFG61's committed model stacks (ml, me, canonical) to 1e-9 relative, and the released-covariance χ² equals CFG61's 28.07.
- **C2 CONTROL:** the canonical α_dyn fit reproduces CFG33's committed calibration: slope +0.204 and ×0.72 / ×0.83 / ×0.90, each to its printed digits.
- **C3 CONTROL:** the log-M_b interpolation of the law's ΔΣ matches a directly computed profile at three off-node masses to 1% at the K1 radii.
- **H1 [HEADLINE; MUTATE must fail]:** with B's own calibration, B's law fits the released split on K1: p > 0.01 on both footings.
- **H2:** the same for the re-measured split under the jackknife covariance: p > 0.01 on both footings.

## Reported rows

- **R1:** the per-class δ as a function of M* over the KiDS lens mass range, and the lens-weighted mean δ_early − δ_late.
- **R2, the late-type bracket:**
  - δ_late = 0, the discs at their catalogue masses;
  - a reference Υ_3.6 = 0.6 in place of 0.5, giving δ_late ≈ 0.
- **R3:** the Salpeter/Chabrier offset at 0.20 and 0.30 dex.
- **R4:** α_dyn at the median σ with no σ-slope, i.e. a constant α.
- **R5:** χ²(Δ) for a uniform differential offset Δ = δ_early − δ_late on a declared grid, 0 to 0.5 dex in 0.025 steps, on both data sets. The Δ ranges with p > 0.0027 and p > 0.05 are a diagnostic of what is needed, not a fit.
- **R6:** the absolute profiles on K1, early and late separately, with B's calibration, on the released data (per-class blocks of the 30 × 30).

## MUTATE

MUTATE=1: δ_early = δ_late = 0 (B's calibration removed). This returns CFG61's 28.07/7, so H1 must fail and the script must exit 1. The README says whether the control is informative, which is only the case if the main run passes H1.

## Readings (declared)

- **H1 and H2 PASS:** B's own stellar-mass calibrations account for the KiDS split. B's one specific failure is then explained, with no new constant, by the early-type M/L that B's own ATLAS3D dynamics already require.
- **H1 or H2 FAIL:** the split survives B's own calibration. R2 and R5 say how far off it is, and what differential offset would be needed.
- **Either way,** the result is conditional on the declared conversions: the Salpeter/Chabrier offset, the SPARC reference Υ, and the LePhare-Chabrier reading of the KiDS masses. R2 and R3 bracket these.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
