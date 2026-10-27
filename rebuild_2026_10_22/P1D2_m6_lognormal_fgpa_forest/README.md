# P1D2_m6_lognormal_fgpa_forest: M6 against Boera et al. 2019 with a native lognormal + saturation forest model

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (d89e0f9469).
- **A1** (219abb9fb3): stratified patches, two-pass MC variance and the μ grid.
- **A2** (4c20e2c9c5): memory caps and warm starts. The first launch was stopped at 0.97 GB and restarted; the restarted
  primary reproduces it exactly.

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen rule, both footings): **NOT DIAGNOSTIC (NATIVE FGPA MODEL INADEQUATE)**

The class is FRAGILE: V-kcut flips it to the other NOT DIAGNOSTIC sub-class.

- **The fit improves but still fails.** The null χ² is 95.32/36, against P1D1's linear 137.6/39. γ sits at its floor of
  1.0 and R_J near its floor at z 4.6–5.0.
- **Saturation hides M6 at z 4.2–5.0.**
  - At X57's bound, M6 changes the FGPA flux power by only about −1 % to +2 %. The linear proxy gave +11 % to +22 %.
  - The Asimov Δχ² is **0.44 (canonical) / 0.16 (alt)** in the primary, and at most 0.44 over all eight configurations.
- **Where the null fits** (V-kcut, k ≤ 0.1 s/km, p 0.93), M6 is undetectable (Asimov 0.32 / 0.17).
- **μ fits are reported only.** μ̂ sits at the grid edge (≈ 8) in the inadequate configurations; the template is absorbing
  misfit.

## Checks: 7/7

K1, S0 (checksums, tables, P1D1's M6, Gaussian field and units, patch fraction), K2, K3 and K4 are vacuous because G1
fails. K5 (mean baryon conservation) and K6 (0.78 GB) pass.

**MUTATE twin (`P1D2_MUTATE=1`): exit 1.**

- It fails S0c (m3: the P1D1 target × 1.01), as required.
- **It does not fail K5 (m1).** Patch gas at δ_b,in = −1.5 is clipped to zero density. That shifts ⟨Δ⟩ by only +0.6 %,
  inside K5's Poisson tolerance of 0.8 %, so the anti-density control does not break mean conservation detectably. This
  is a twin-design miss, disclosed and not repaired post hoc.
- m2 (the uncorrected data column) runs.

**Rerun-identical:** pending.

## What this means

The high-z Lyman-α forest power cannot test M6 at X57's bound. The flux is saturated at the patch overdensities.

## Files

- `p1d2_m6_fgpa.py`
- `p1d2_m6_fgpa.out` (append mode, with the stopped first launch at the top) and `p1d2_m6_fgpa_results.json`
