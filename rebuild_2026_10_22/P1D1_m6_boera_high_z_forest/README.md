# P1D1_m6_boera_high_z_forest: does measured z 4.2–5.0 Lyman-α P1D allow X57's M6 at its bound?

**Fix-forward correction (2026-10-27):** read
[CORRECTION_2026_10_27.md](CORRECTION_2026_10_27.md) and amendment A3 before using
this lane. Its completed NOT DIAGNOSTIC result stands. The frozen upper-envelope
interpretation is invalid, and the historical K3 mutation did not independently
test the sign. A separately planted, unconditional regression is now provided;
it supplies no observational M6 exclusion or physical baryon-fraction limit.

## Provenance

- **Criteria and ledger:** `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (8f6e3db4bc), committed alone before any P1D value
  was read.
- **A1** (e6d278b747): S0e is met by an independent re-implementation, because importing X63 would overwrite its outputs.
- **A2** (47515516e6): a check-code fix after a Step-0 STOP at S0e 4/8. Its output is kept as `*_STOP_preA2.*`. The cause
  was that the inherited background needs X57's separate shape Ω_m (0.315) and D(z) Ω_m (0.31375).

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

**Data.** Boera et al. 2019 (arXiv:1809.06980v2), owner-approved download 2026-10-27. The files are untracked under
`_external_data/boera2019_p1d/raw/`, with checksums frozen.

## Verdict (frozen rule, both footings): **NOT DIAGNOSTIC (LINEAR NATIVE MODEL INADEQUATE)**

The qualifier is FRAGILE: only V-kcut flips, and it flips to the other NOT DIAGNOSTIC sub-class.

- **G0 fails.** The native linear gas proxy cannot fit the measured flux power.
  - The null χ² is 137.63 on 39 dof (p 6e-13).
  - Per z: 35.5, 69.5 and 32.7 on 13 dof.
  - The misfit sits in the bins with k > 0.1 s/km. With those bins cut (V-kcut) the null fits, with χ² 17.1 / 30 and
    p 0.97.
  - The primary scan's μ̂ ≈ 2.9 (Δχ²₀ 28) is the M6 template **absorbing model misfit**. It is not an excess and is
    not graded.
- **G1 fails as well.** The Asimov Δχ²(μ = 1 vs 0) is 5.58, below 9. A free tilt and a free R_J per z soak up most of
  the linear M6 shape.
- **Where the proxy is adequate (V-kcut, k ≤ 0.1 s/km; reported, not graded):**
  - μ̂ = 0.48, Δχ²(μ = 1) = 1.83, μ_95 = 1.26.
  - So M6 at X57's bound is **allowed** by the data there, but the test has Asimov power of only 8.14.
- **Variants.** All other variants are NOT DIAGNOSTIC (model inadequate): ns 0.92 / 1.00, tilt0, diag and RJfix.
- **Inherited background (reported):** the same class.
- **Footings agree.** The linear signal is footing-independent by construction, since A = 0.2 σ²_ad D₃² V_p.

## Native background swap (graded)

L1's BAO + BBN background, with no CMB, gives the following against X57/X63's inherited 5.364 / h 0.674:

| quantity | native | inherited |
|---|---|---|
| Ω_c/Ω_b | 5.2715 | 5.364 |
| F_b,max(z = 3), canonical / alt | 0.06132 / 0.04895 | 0.06038 / 0.04822 |
| δ_b,in, canonical / alt | +4.2358 / +5.1296 | — |
| f_V, canonical / alt | 0.01171 / 0.00799 | — |

## What this means

The linear proxy is the wrong instrument at k > 0.1 s/km. It also treats M6's patches as Gaussian power, when they
are saturating lumps of gas. The successor lane `P1D2_m6_lognormal_fgpa_forest` replaces it with a native lognormal +
FGPA forward model, with the patches inserted in real space.

## Checks

- **Main: 7/7 PASS, exit 0.**
  - S0 (checksums, tables, covariances, √diag = table σ to 6e-4, and X63/X57 reproduced 8/8).
  - K1–K6.
  - K3 and K4 are vacuous, because G1 fails. Peak RSS 0.18 GB.
- **Rerun.** Identical apart from timing: one JSON leaf (K6 elapsed).
- **MUTATE (`P1D1_MUTATE=1`): exit 1.**
  - It fails S0e (m3) and K3 (m1, sign flipped: Asimov 10.39, so K3 is live, but planted Δχ²₀ 7.59), as required.
  - m2 uses the uncorrected column.

## Files

- `p1d1_m6_boera.py`
- `p1d1_m6_boera.out` and `p1d1_m6_boera_results.json`
- `*_MUTATE.*` (control, not physics)
- `*_STOP_preA2.*` (the first run, which stopped at Step 0)
