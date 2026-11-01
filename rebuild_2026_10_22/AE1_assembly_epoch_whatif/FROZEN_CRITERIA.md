# AE1_assembly_epoch_whatif: FROZEN CRITERIA (2026-10-31, before any number)

**Question (Argon's door D3, second transmission, `../ARGON_REPLY_2026-10-31_EVENING_SCORED.md`).** X43's Σ_coll(M) evaluates the collapse surface density at the half-mass formation epoch z_f (Lacey–Cole, f = 0.5, δ_c 1.686, ω 0.974). Argon proposes that a cored halo's core strength freezes when the core's own mass fraction has assembled: f_s = B(√2)/B(a) with a = r_vir/r₀ (0.144 at a 13.34), or f = 0.25 inside 2 r₀. Evaluating Σ_coll at z(f_s) raises S more at low mass. Applied as a ratio to 10¹² (so as not to double-count the zooms, which already contain their own collapse), does it put the dwarf bins in ET1's intervals without a floor?

**This is a what-if on an analytic convention, not a measurement.** The zooms evolve the full collapse from the initial conditions, so any early core assembly is already in their measured η at z_f; this factor can only be physical if the zooms' inner core is unresolved at z(f_s). X80's measured ratios (ρ₁₀ 1.128, ρ₁₁ 0.938) are the record; this lane reports what the convention would give beside them. Owner rules: native inputs only; no scan (one f_s fixed by the profile, with f = 0.25 reported beside it); κ = ½ FITTED; footings never pooled; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.

## Computation
1. X43's own σ(M) and D(z) (EM1's native backgrounds A_c2b_refit and B_cfg886_bg, executed read-only as X43 does), δ_c 1.686, ω 0.974, same interpolation.
2. z(f, M) from δ_c/D = δ_c + ω√(σ²(fM) − σ²(M)) for f ∈ {0.5, 0.25, f_s}, f_s = B(√2)/B(13.34) with B(x) = asinh(x) − x/√(1+x²) (the smooth core's enclosed-mass function), at M = 10¹⁰, 10¹¹, 10¹², 10¹⁴ M☉ (M as X43 uses it).
3. Boost R_f(M) = [(1+z(f,M))/(1+z(0.5,M))]². Relative ratios ρ₁₀ = R_f(10¹⁰)/R_f(10¹²), ρ₁₁ = R_f(10¹¹)/R_f(10¹²).
4. `../NF1_no_floor_rule/nf1_native_read.py --rho ρ₁₀ ρ₁₁` for f_s (graded) and f = 0.25 (reported): SPARC line on both backgrounds, S and Υ by V_flat bin, as X80's what-if table.

## Gate: G1 + G9 (Argon's lines, as sent)
- **PASS:** S in the 20–60, 60–100, 100–150 km/s bins inside ET1's intervals [52, 85], [81, 124], [118, 200] M☉/pc², SPARC rms ≤ 0.110 with median Υ ∈ [0.50, 0.80] on both backgrounds.
- **FAIL:** any bin outside its interval, or Υ outside [0.50, 0.80] on either background.
- LITTLE THINGS is not graded here (ND1's grader is pinned to X80's measured ratios by assertion); reported as not run.

## Predictions on record
- Argon: absolute S 71 / 101 / 131 (multipliers 1.51 / 1.46 / 1.39 on N0's 47 / 69 / 94), SPARC Υ 0.54 / 0.55, LITTLE THINGS +0.045: PASS.
- This session: Argon's multipliers include 10¹²'s own factor (1.33), which the zoom already holds. As ratios to 10¹² they are about 1.14 and 1.07, within X80's measured band and near the what-if row 1.1 / 1.049 (S 52 / 73 / 98, Υ 0.67 / 0.68): bins 60–100 and 100–150 fall below ET1's intervals: **FAIL**, with the SPARC line passing.

## Checks
- K1: f = 0.5 reproduces X43's z_f at 10¹¹–10¹⁵ (1.14, 0.94, 0.75, 0.56, 0.39 on background A) to 0.01.
- K2: f_s computed from B equals 0.144 ± 0.002 at a 13.34.
- K3: `nf1_native_read.py --check` reproduces NF1's N0 (Υ 0.71 / 0.73) before the what-if runs.
- MUTATE: ω doubled must move z(f_s, 10¹⁰) by more than 0.1; else stop.

## Cost
Minutes, one thread, under 1 GB. No new data, no zoom.
