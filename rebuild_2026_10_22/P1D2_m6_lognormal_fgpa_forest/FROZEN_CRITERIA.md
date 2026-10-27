# P1D2_m6_lognormal_fgpa_forest: FROZEN CRITERIA (committed alone, before any script or fit)

**Why this lane.** P1D1 (`P1D1_m6_boera_high_z_forest`) returned NOT DIAGNOSTIC. Its linear native flux proxy could not fit
Boera et al. 2019's z = 4.2 / 4.6 / 5.0 P1D (null χ² 137.6 / 39). The misfit sits in the k > 0.1 s/km bins, where the
real flux is exp(−τ) of a nonlinear field. The proxy also treats M6's patches (gas at δ_b,in ≈ +4.2 to +5.1, f_V ≈ 1 %) as
extra Gaussian power, whereas they are localised, saturating lumps. This lane replaces the proxy with a
**framework-native nonlinear forward model**: a lognormal gas field from the native linear power, the fluctuating
Gunn–Peterson approximation (FGPA) and thermal broadening (Bi & Davidsen 1997 class). M6's patches are inserted **in real
space**.

- No hydrodynamic simulation is used, because those run on a ΛCDM background, which is banned.
- Same data as P1D1, already approved and checksummed. No new download.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 0. Data and background

- **Data.** As P1D1 §0, with identical checksums: the resolution-corrected P_k (km/s) at z = 4.2 / 4.6 / 5.0, 16 bins each,
  and the published covariances.
- **NATIVE background, as P1D1 §2.** L1's Ω_m 0.2976016, h 0.6856427, ω_b 0.0223081; σ₈ 0.827959; n_s 0.965 (disclosed).
- **M6.** Per footing, M6 on that background as P1D1 computed it: δ_b,in, f_V at F_b,max(z = 3), and R_L 0.4419 Mpc/h.
  - Canonical: δ_b,in +4.2358, f_V 0.01171.
  - Alt: δ_b,in +5.1296, f_V 0.00799.
  - Step 0 reproduces these from P1D1's committed JSON to 4 decimals.

## 1. Forward model (frozen), per z and per parameter set

1. **Gas field.** A 1D Gaussian field g(x) along a periodic skewer whose power is the 1D projection of the native linear
   3D gas power P_ad(k) D(z)² exp(−k²R_J²). This is P1D1's `p1d`, on the same KG grid.
   - The lognormal gas overdensity is Δ_ad = exp(g − σ_g²/2).
2. **M6 patches.** Spheres placed by a Poisson process in 3D, with radius R_L.
   - A skewer crosses them at line rate λ = 3 μ f_V / (4 R_L).
   - The chord half-length is R_L √(1 − u), with u uniform on [0, 1). This is exact for random impact parameters.
   - The patch indicator I(x) (1 on a chord) is smoothed in 1D by a Gaussian of σ = R_J (gas pressure), giving I_s.
   - Gas density: Δ = Δ_ad · [1 + δ_b,in I_s − μ f_V δ_b,in (1 − I_s) / (1 − μ f_V)]. This conserves mean baryon density
     (compensation outside).
   - μ = 1 is M6 at X57's bound. μ = 0 is the null.
3. **FGPA.** τ_real = A_τ Δ^β, with β = 2 − 0.7 (γ − 1).
   - τ is convolved in velocity with a Gaussian of width b/√2 (thermal broadening, Doppler parameter b).
   - Peculiar velocities are omitted (ledger D3).
4. **Flux.** F = exp(−τ). A_τ is set by bisection so that ⟨F⟩ = F̄ (the mean-flux nuisance). The statistic is
   δ_F = F/⟨F⟩ − 1.
5. **P1D.** Computed by FFT in velocity units, with dv = dx · 100 E(z)/(1+z) on the native E(z). It is averaged over each
   Boera bin (log₁₀ k ± 0.05) on the mock modes.
6. **Numerics.** Each z uses a periodic skewer set of total length 4000 Mpc/h comoving (20 skewers of 200 Mpc/h) with pixel
   0.02 Mpc/h.
   - The Gaussian field uses **fixed-amplitude modes with random phases** (Angulo & Pontzen 2016), so the input power is
     reproduced without cosmic variance.
   - The random numbers are common across all parameter sets: seed 0 for the phases, seed 1 for the patches.
     The model is therefore smooth in its parameters.
   - u and the chord positions are drawn once at μ = 1, and a chord is kept if its uniform tag is ≤ μ. This gives common
     random numbers in μ for μ ≤ 1. For μ > 1, extra chords come from an independent stream (seed 2).

**Nuisance per z** (fitted; bounded):

| parameter | range |
|---|---|
| F̄ | [0.02, 0.70] |
| γ | [1.0, 1.8] |
| b | [4, 30] km/s |
| R_J | [0.02, 0.30] Mpc/h |

μ ≥ 0 is common to all z. b̂² is not used, because FGPA fixes the amplitude through F̄. The fit minimises χ² with the
published covariance by bounded optimisation from a deterministic coarse grid.

## 2. Step 0 (stop rule)

- **S0a.** Data checksums.
- **S0b.** Tables parse as in P1D1.
- **S0c.** P1D1's M6 numbers are reproduced (§0).
- **S0d. Field and units.** The mock power of the Gaussian field g, measured with the same FFT, velocity conversion and
  bin averaging as δ_F, must equal the input 1D power (converted to km/s) within 5 % in every Boera bin. This is the MC
  tolerance at 4000 Mpc/h, and it checks the 1D field construction, the units and the binning.
- **S0e. Patch line rate.** At μ = 1 the mock's patch-covered skewer fraction must equal f_V within 3 Poisson σ, on each
  footing.

## 3. Gates and verdict (each footing separately; they now differ physically)

Same structure and thresholds as P1D1 §4:

- **G0.** Null (μ = 0) joint p ≥ 0.01 over 48 bins − 12 nuisance = 36 dof, and every per-z p ≥ 0.001. A failure gives
  NOT DIAGNOSTIC (NATIVE FGPA MODEL INADEQUATE).
- **G1.** Asimov Δχ²(μ = 1 vs μ = 0), profiled, must be ≥ 9. A failure gives NOT DIAGNOSTIC (NUISANCE ABSORBS M6).
- **Verdict.**
  - M6 AT X57's BOUND EXCLUDED if Δχ²₁ ≥ 9.
  - M6-SHAPED EXCESS PRESENT if Δχ²₀ ≥ 9.
  - NOT EXCLUDED otherwise.
  - μ̂, μ_95 and F_b,95 are reported in every case.

**Model Monte-Carlo noise.** The mock P1D's relative MC error per bin is estimated from the 20-skewer scatter. Its
variance is **added to the data covariance**, to be generous to M6.

**Robustness qualifier.** ROBUST if every variant below gives the same class; otherwise FRAGILE, with the flipping
variants named.

- **V-kcut:** k ≤ 0.1 s/km.
- **V-diag:** diagonal data covariance.
- **V-nosmooth:** patches unsmoothed (I_s = I).
- **V-ns:** n_s ∈ {0.92, 1.00}.
- **V-gamma15:** γ ≡ 1.5.
- **V-seed:** phase / patch seeds 10 / 11 (μ > 1 stream 12).

**Reported only.**

- The flux-PDF fraction of pixels with F < 0.05, μ = 1 against μ = 0. This is a pointer for a future test on spectra and
  is never graded.
- The comparison with P1D1's linear-proxy S at the same k, which shows how much FGPA saturation removes.

## 4. Checks and twin

- **K1.** Parser as P1D1.
- **K2.** μ = 0 gives a patch layer identical to 1.
- **K3.** A planted μ = 1 (null best fit at μ = 1, plus covariance noise, seed 0) is recovered with μ̂ ∈ [0.5, 1.5]
  and Δχ²₀ ≥ 9 when G1 passes.
- **K4.** A planted null gives μ_95 < 1 when G1 passes.
- **K5.** Mean baryon conservation: |⟨Δ⟩ − ⟨Δ_ad⟩| / ⟨Δ_ad⟩ ≤ 3 Poisson σ of the patch term at μ = 1.
- **K6.** Peak RSS < 1 GB, one thread. The run is preemptible (checkpointed per configuration and footing, resumable on
  SIGTERM). Runtime is reported.
- **MUTATE twin (`P1D2_MUTATE=1`, separate outputs).**
  - m1: δ_b,in → −1.5 (unphysical: patch gas density negative). Densities are clipped at 0 before FGPA, so mean
    baryon conservation must break.
  - m2: the uncorrected data column.
  - m3: the S0c target × 1.01.
  - The twin must fail S0c (m3) and K5 (m1).

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I p1d2_m6_fgpa.py`. Amendments only in `AMENDMENTS.md`,
each committed before the run it affects. No gate, threshold or model change after any fit is seen.
