# P1D4_m6_native_3d_forest: FROZEN CRITERIA (committed alone, before any fit to data)

**Question.** P1D1–P1D3 all ended NOT DIAGNOSTIC, because the framework's forest model was too crude: linear or 1D,
and missing redshift-space distortions. This lane asks whether a **framework-native 3D forest model** fits DESI DR1
P1D (z 2.2–4.4, the same data and checksums as P1D3), and if it does, whether M6 at X57's bound is allowed. The model
contains:

- a fixed-amplitude Gaussian field in a periodic box from the native linear power;
- pressure filtering;
- lognormal baryons;
- FGPA;
- **linear Kaiser redshift-space displacement from the same modes**;
- thermal broadening;
- M6 patches as compensated **3D** spheres.

No ΛCDM hydrodynamic simulation is used. The data download was owner-approved on 2026-10-27; the files are untracked.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 1. Model (`forest3d.py`, as committed with these criteria)

- **Background.** NATIVE, as P1D1–P1D3: L1's Ω_m 0.2976016, h 0.6856427 and ω_b 0.0223081, with σ₈ 0.827959 and n_s 0.965
  (disclosed as not native).
  - f(z) = d ln D / d ln a, computed on that background.
  - cz = 100 E(z)/(1 + z) km/s per Mpc/h.
- **Box.**
  - N = 256, L = 64 Mpc/h.
  - Fixed-amplitude modes, phase seed 0, and scipy.fft in single precision.
  - Skewers along z on a sub-lattice with stride 4: 64² = 4096 skewers for the tables.
- **Baryons.**
  - Δ = exp(δ_G − σ²/2), with δ_G filtered by exp(−k²R_J²/2) in amplitude.
  - M6 multiplies Δ by the compensated patch factor 1 + δ_b,in I_s − f_V,eff δ_b,in (1 − I_s)/(1 − f_V,eff). I_s is the
    3D sphere indicator (radius R_L 0.4419 Mpc/h, stratified tags in μ as P1D2 A1) smoothed by R_J. f_V and δ_b,in
    are the native per-footing values.
- **Flux.**
  - τ_real ∝ Δ^β with β = 2 − 0.7(γ − 1).
  - τ is shifted by f ψ_z with cloud-in-cell weights along the line of sight.
  - It is then convolved with a Gaussian of velocity width b/√2, with b constant at mean density.
  - F = exp(−A τ), with A set so that ⟨F⟩ = F̄.
  - P1D is computed from δ_F = F/⟨F⟩ − 1 along each skewer, in km/s.
- **Model at DESI k.** Log-log interpolation of the mock P1D across the box line-of-sight modes.
- **Bins used.** DESI's cut (0.001 < k < 0.5π/R_z, as P1D3) and also k ≥ 2 k_f / cz(z), where k_f = 2π/L.

**Nuisance per z.**

| parameter | grid / range | status |
|---|---|---|
| γ | {1.0, 1.3, 1.6} | grid |
| R_J | {0.05, 0.12, 0.20} Mpc/h | grid |
| b | 7 nodes, 6–35 km/s | tabulated |
| F̄ | 10 nodes, 0.15–0.90 | tabulated |

- The model P1D is tabulated on γ × R_J × μ × b × F̄. The (b, F̄) dependence is interpolated by a bicubic spline in
  (b, logit F̄) on log P.
- The profile χ² minimises over (b, F̄) continuously at each (γ, R_J) node and then takes the best node.
- dof count 4 nuisance parameters per z.

**μ.** The grid is {0, 0.25, 0.5, 1, 2}, common to all z. The profile χ²(μ) is interpolated piecewise-quadratically
between grid nodes, and μ̂ and μ_95 (Δχ² = 3.84) are taken from that interpolation.

**Covariance.** The per-z diagonal blocks of COVARIANCE are used. The cross-z blocks are dropped, since the mean |r| is
5e-4. The maximum |r| is reported, and so is the full-covariance χ² evaluated at the per-z best fits.

**Model MC variance.** At the null best fit per z, the model P1D is recomputed with phase seeds 1 and 2. The variance
across seeds 0, 1 and 2 is added to the diagonal, and everything is refit (two passes, as P1D2 A1).

## 2. Step 0 (stop rule)

- **S0a.** DESI md5, as P1D3.
- **S0b.** P1D1 native M6 numbers reproduced to 4 decimals.
- **S0c.** The box Gaussian P1D at z = 3, R_J = 0.1 equals the analytic 1D projection within 5 % at k_f ≤ k ≤ 8 h/Mpc.
  This checks normalisation, units and the projection.
- **S0d.** The 3D patch covered fraction equals f_V within 3 Poisson σ for each footing.
- **S0e.** The interpolation check: at 5 random interior (b, F̄) points per z (seed 7), the interpolated log P equals a
  direct evaluation within 1.5 % in every used bin.

## 3. Gates and verdict (per footing; thresholds as P1D1–P1D3)

- **G0.** Null joint p ≥ 0.01 and every per-z p ≥ 0.001. A failure gives NOT DIAGNOSTIC (NATIVE 3D MODEL INADEQUATE).
- **G1.** Asimov Δχ²(μ = 1 vs 0) ≥ 9. A failure gives NOT DIAGNOSTIC (NUISANCE ABSORBS M6).
- **Verdict.** M6 AT X57's BOUND EXCLUDED (Δχ²₁ ≥ 9), M6-SHAPED EXCESS PRESENT (Δχ²₀ ≥ 9), or NOT EXCLUDED. μ̂ and μ_95
  are reported.
- **Robustness.** ROBUST if all variants agree; otherwise FRAGILE, with the flipping variants named.
  - **V-stat:** COVARIANCE_STAT blocks.
  - **V-floor2:** add (0.02 P_model)² to the diagonal. This is a declared model-systematic floor.
  - **V-hiz:** z ≥ 3.6 only.
- **Reported only.**
  - The full-covariance χ².
  - Per-z μ̂.
  - A comparison of the best-fit F̄(z) and b(z) with published ranges. That comparison is not used in the fit.

## 4. Checks and twin

- **K1.** Bin selection per z is reported.
- **K2.** μ = 0 tables are identical across footings.
- **K3.** A planted μ = 1 (null best fit at μ = 1 plus covariance noise, seed 0) is recovered with μ̂ ∈ [0.5, 1.5] and
  Δχ²₀ ≥ 9 when G1 passes. **The injection uses the footing's actual positive-δ_b patches; the fit uses the same
  tables. The m1 twin flips the patch sign in the tables only, not in the injection, so K3 can see it** (repairing the
  P1D3 twin flaw).
- **K4.** A planted null gives μ_95 < 1 when G1 passes.
- **K5.** Peak RSS < 1 GB, one thread. The run is preemptible: there is a checkpoint per (footing, z) table, and on
  SIGTERM it exits after the current table.
- **MUTATE (`P1D4_MUTATE=1`, separate outputs and checkpoint).**
  - m1: δ_b,in → −0.8 δ_b,in in the fit tables only.
  - m2: the S0b target × 1.01.
  - The twin must fail S0b and K3 (K3 only if it is live).

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I p1d4_m6_3d.py`. Amendments only in `AMENDMENTS.md`,
each committed before the run it affects. No gate, threshold, grid or model change after any data fit is seen.
