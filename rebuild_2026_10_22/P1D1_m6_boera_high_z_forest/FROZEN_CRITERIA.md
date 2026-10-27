# P1D1_m6_boera_high_z_forest: FROZEN CRITERIA (committed alone, before any P1D value is read)

**Question.** Does the measured high-redshift Lyman-α flux power, P1D at z = 4.2, 4.6 and 5.0 (Boera et al. 2019, ApJ 872,
101; arXiv:1809.06980v2), allow X57's M6 (displacement: compensated, anticorrelated cold-dark-energy/baryon patches)
at the amplitude X57 allows? X63 (`X63_displacement_forest_prediction`) predicted, at that amplitude, a gas-power excess
S = R − 1 of +0.26 / +0.30 / +0.35 at z = 4.2 / 4.6 / 5.0, peaking near k ≈ 0.024–0.028 s/km.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 0. Data (owner-approved download, 2026-10-27; set A only)

Kept untracked under `_external_data/boera2019_p1d/raw/` (third-party data; never committed). SHA-256:

| file | bytes | sha256 |
|---|---|---|
| `src_1809.06980v2.tar.gz` (arXiv source; P1D values in its Tables at .tex L1600–1683) | 814920 | 9583568fe3076be9687567f54e81716a8dd452b4061da1e9476e1d299931f1a8 |
| `Cov_Matrixz=4.2.dat` (NumPy .npy, 16×16, f8, Fortran order) | 2128 | 872daaf273d3f212968b750b5b263c4b03c3cd57091b144ae120a480e76bb4dc |
| `Cov_Matrixz=4.6.dat` | 2128 | 44e75dc183fab9083add6a924dd3b2787869c2579bc1ea152592c1e864d261ed |
| `Cov_Matrixz=5.0.dat` | 2128 | c44356e7f2f05d47a4a20dd274fc1d5f7812f09f8327636322c89063ff167d05 |

At commit time only the table captions and file headers have been seen. No P1D value or covariance element has been read.

- The lane's script parses the three tables from `PSpaperApJRef_New.tex`.
- It uses the **resolution-corrected** column (the caption's "third column") and the published covariance at each z.
- The script runs from its own folder and reads the data by path (`python3 -I`).

## 1. Step 0 (stop rule: any failure → STOP, report, no grading)

- **S0a. Checksums** match the table above.
- **S0b. Tables.** Each z has 16 rows, with log₁₀(k / s km⁻¹) from −2.2 to −0.7 in steps of 0.1 (within ±0.01), and positive power.
- **S0c. Covariances.** Each is 16×16, symmetric (relative asymmetry ≤ 1e-8) and positive definite.
- **S0d. Quantity match.** If the tables carry an error column, √diag(Cov) must equal it within 15 % in every bin. If they
  carry none, √diag/P must be finite and between 0.01 and 2.0. A failure means the covariance is not for the tabulated
  quantity (for example kP/π against P): STOP. A single global unit conversion (P ↔ kP/π) is permitted only if it brings
  every bin inside the 15 % line; it is then recorded.
- **S0e. X63 reproduced.** X63's inherited-background M6 numbers are reproduced by importing its formulas, not
  re-typing them: max S at R_J 0.1 of +0.261 / +0.302 / +0.346 at z 4.2 / 4.6 / 5.0, and F_b,max(z = 3) of
  0.06038 / 0.04822. Tolerance: 3 decimals.

## 2. Backgrounds (owner rule 10-25: no ΛCDM / Planck inputs in what is graded)

- **NATIVE (primary, graded).** L1's background: flat, Ω_m = 0.2976016, h = 0.6856427 (CFG886 GR fit to BAO + BBN, no
  CMB), and Ω_b = ω_b/h² with ω_b = 0.0223081.
  - This gives Ω_c/Ω_b = (Ω_m − Ω_b)/Ω_b, which replaces X57/X63's 5.364.
  - σ₈ is Q7's native 0.827959 (σ₈(DUST)).
  - n_s is 0.965 in the primary. It is CMB-derived and disclosed in the ledger; variant V-ns tests it.
  - D(z) and E(z) are computed on this background.
  - X57's F_b,max, δ_c,in, δ_b,in and f_V are **recomputed** on it with X57's own formulas, through X63's imported
    functions with the background swapped.
- **INHERITED (reported only).** X63 exactly as committed (Ω_c/Ω_b 5.364, h 0.674). It exists to show the size of the swap,
  and is never graded.

## 3. Model (frozen)

Per redshift z ∈ {4.2, 4.6, 5.0}, the observed flux power is modelled as

  P_F(k) = b_z² · (k/k_p)^{α_z} · P1D_gas(k; R_J,z) · [1 + μ · S_z(k; R_J,z)]

The pieces:

- **P1D_gas.** X63's linear adiabatic gas 1D power on the NATIVE background. The 3D power is filtered by exp(−k²R_J²),
  then projected with X63's `p1d`. k is converted from s/km to h/Mpc with the NATIVE E(z).
- **S_z.** X63's ratio P1D_iso/P1D_ad on the NATIVE background, at the same R_J,z. The amplitude is NATIVE F_b,max(z = 3),
  so μ = 1 is "M6 at X57's bound".
- **Nuisance, per z (fitted).**
  - b_z² > 0 (mean-flux and flux-bias amplitude), free.
  - R_J,z ∈ [0.02, 0.30] Mpc/h (pressure and thermal cutoff; exp(−k²σ_th²) is degenerate with it at fixed z, so it is not
    added separately).
  - α_z ∈ [−1, +1] (a tilt absorbing nonlinear and FGPA shape departures of a linear proxy), with pivot
    k_p = 0.03 s/km.
- **μ ≥ 0** is common to all z, because the M6 amplitude is one number.
- **Fitting.** χ² uses the published covariance. Each z is profiled over its own nuisance on a dense grid followed by
  bounded local refinement, with a deterministic seed. All 16 bins are used.

## 4. Gates and verdict (each footing separately; X63 showed the footings give identical S by construction, and both are still run)

- **G0, null adequacy.** At μ = 0, the joint χ² over 3 × 16 bins with 9 nuisance parameters has p ≥ 0.01, and every
  per-z p is ≥ 0.001. If G0 fails, the verdict is **NOT DIAGNOSTIC (LINEAR NATIVE MODEL INADEQUATE)**: no M6 statement
  is made, and μ fits are reported only.
- **G1, power (Asimov).** Take the μ = 0 best fit as truth, with no noise. The expected
  Δχ²_A = min χ²(μ = 1) − min χ²(μ = 0), each profiled over the nuisance, must be ≥ 9. If it is not, the verdict is
  **NOT DIAGNOSTIC (NUISANCE ABSORBS THE M6 SHAPE)**.
- **Verdict on the data, if G0 and G1 pass.** Let χ²_min be the minimum over μ ≥ 0.
  - **M6 AT X57's BOUND EXCLUDED** if Δχ²₁ = χ²(μ = 1) − χ²_min ≥ 9. The lane also reports the 95 % upper limit μ_95
    (Δχ² = 3.84) and the implied maximum F_b.
  - **M6-SHAPED EXCESS PRESENT** if Δχ²₀ = χ²(μ = 0) − χ²_min ≥ 9, with μ̂ reported. This is a statement about a
    shaped excess, not support for the framework.
  - **NOT EXCLUDED** otherwise, with μ̂ and μ_95 reported.
- **Robustness qualifier.** The verdict is ROBUST if every variant below gives the same verdict class. Otherwise it is
  FRAGILE, and the variants that flip are named.
  - **V-ns:** n_s ∈ {0.92, 1.00}.
  - **V-tilt0:** α_z ≡ 0.
  - **V-kcut:** only bins with k ≤ 0.1 s/km.
  - **V-diag:** diagonal covariance only. Boera's covariance was regularised with hydrodynamic simulations (ledger C4).
  - **V-RJfix:** R_J,z ≡ 0.1 Mpc/h with α_z free.
  - **V-inherited:** the inherited background, reported for comparison. It cannot flip the graded verdict, but a flip is
    disclosed.
- **Upper-envelope caveat (inherited from X63, ledger B3/B5/B6).** S is a generous linear proxy. **EXCLUDED** therefore
  excludes the proxy at the bound, and with it any weaker realisation of M6 at that amplitude. **NOT EXCLUDED** does not
  confirm M6.
- **Where this leaves M6.** The interpretation at the bound, as X57 / X63 stated it: if M6 at the bound is excluded and
  μ_95 < 1, then M6 survives only below μ_95 · F_b,max.
  - Whether that remnant can still do X57's exclusion job is reported from X57's own numbers.
  - It is not graded here.

## 5. Checks (K) and twin

- **K1.** The parser reproduces each table's row count and k grid (S0b).
- **K2.** μ = 0 gives model ≡ null exactly.
- **K3.** A planted M6 at μ = 1, built from the μ = 0 best fit plus the published covariance noise (seed 0), is recovered
  at μ̂ ∈ [0.5, 1.5] and gives Δχ²₀ ≥ 9 whenever G1 passes.
- **K4.** A planted null gives μ_95 below 1 whenever G1 passes.
- **K5.** Unit conversion: k(0.01 s/km, z = 5) on NATIVE E(z), with an exact round trip.
- **K6.** Resources: peak RSS < 1 GB, one thread, minutes.
- **MUTATE twin (`P1D1_MUTATE=1`, separate outputs).**
  - m1: the S sign is flipped.
  - m2: one table column is swapped for the uncorrected column.
  - m3: the S0e target is multiplied by 1.01.
  - The twin must fail S0e (m3) and K3 (m1). It must not overwrite the main outputs.

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I p1d1_m6_boera.py`. Amendments only in
`AMENDMENTS.md`, each committed before the run it affects, and none may change a gate, a threshold or the model after any
P1D value is read.
