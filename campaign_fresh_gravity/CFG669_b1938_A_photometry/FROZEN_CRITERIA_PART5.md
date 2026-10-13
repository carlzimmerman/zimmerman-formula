# CFG674 PART 5 FROZEN CRITERIA (2026-10-13): does the excess at A survive A's own mass in the lens model?

Committed ALONE before Part 5 is run. Seen: Part 4 (A light 13.2 ± 3.5 nJy, S 3.8, above all 11 controls; tooth 29.0 AB S 2.63 →
NOT DIAGNOSTIC). The obvious mimic: A's mass perturbation of the arc is absent from the model, so its residual can be absorbed by a
point of light at A. Same data, same stage-2 ML lens model (`cfg674_stage2_ml_nm.json`), same stage-3 machinery and error budget.

## Variants (A's mass as a separate lens-plane galaxy at A's published position, singular isothermal sphere)
- **M1 fixed:** θE,sub from Vegetti+2012's M3D(<0.6 kpc) = 1.13e8 M☉ via SIS (σ² = G M/2r; θE = 4π σ²/c² D_ls/D_s, Planck18
  distances): ≈ 0.005″ (computed in this commit's message).
- **M2 free:** θE,sub ∈ [0, 0.05″] chosen by maximising the likelihood (bounded 1-D optimisation, linear re-solve, A light in).
- **M3 no light:** M2's best mass with A's light component removed — the likelihood difference ΔlogL(light) is reported.

## Rules (unchanged from Part 4 — no goalpost moves)
Per variant: f_A, σ_tot (stat ⊕ 11 same-radius controls re-run with the same A-mass in place ⊕ mesh), S, controls rank; tooth 29.0 AB
(S ≥ 3, |Δm| ≤ 0.5); CFG673 verdict rules. **Diagnostic statement (no verdict weight):** the excess is "robust to A's mass" iff it
stays ≥ 3σ above the controls in both M1 and M2; "absorbed by A's mass" iff it drops below 2σ in either.
