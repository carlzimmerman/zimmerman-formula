# D10_native_Lstar: the L★ floor measured with the theory's own field equation

## Verdict: CRISP FINDING — the native floor holds at ≈ 22 pc with SPS M/L; with MF-slope M/L it falls to 3–10 pc

κ = ½ is FITTED. Not theory closed. Nothing here says the data favour the framework over ΛCDM.

- We solved the stiffened field equation of the healthy C4-literal form (γ_F = 0, grad-div stiffness) for each cluster
  in the Galaxy's field. Each cluster is a Plummer sphere at its own R_GC. No ν_RAR, no EFE recipe, no Wolf shortcut.
- **Central floor (P1 SPS Υ_V, E_mid, f_b = 0.3): L★_95 = 21.68 pc (canonical), 22.85 pc (alt).**
  That is within 10 % of CFG820 (23.96 / 24.72), so the frozen line reads **FLOOR HOLDS**. E4's isolated native value
  (28.85 / 29.12) drops once the external field is solved.
- **Band over the Υ prior and the MW-field bracket: 2.93–22.67 pc (canonical), 4.40–23.80 pc (alt).**
  Against the [20, 90] pc window the band **STRADDLES the 20 pc edge** on both footings.
  - P1 (SPS logN(1.6, 0.15 dex)) gives 19.8–22.7 / 21.2–23.8 pc.
  - P2/P3 (CFG332 Route 2 MF-slope M/L, branches K/S) give 2.9–9.6 / 4.4–10.6 pc. Pal 4's MF-slope Υ_V is 0.60–0.67.
    At that Υ_V even the unscreened Pal 4 boost is much smaller.
  - The MW field bracket (M_b 4e10 → 1.2e11 M☉) moves the floor by only ≈ 3 pc (P1). The Υ prior is the dominant systematic.
- **AQUAL (L★ = 0) is excluded in all 18 cells** (Δχ² 4.9–22.8). **No finite L★ beats Newton** (Δχ²_Newton ≤ 2.5).
  So the globulars give a lower bound only.
- **The constraint is Pal 4 and Pal 14.** Δχ² at AQUAL: Pal 4 12.8, Pal 14 5.3, NGC 2419 1.4 (canonical, central).
  Pal 3 prefers AQUAL (Δχ² 1.85 at Newton). With all four clusters the floor is 18.99 / 20.25 pc.

## The numbers (all in `d10_native_lstar_results.json`)

| footing | central | P1 (E_lo/mid/hi) | P2 (K) | P3 (S) | window |
|---|---|---|---|---|---|
| canonical | 21.68 | 22.67 / 21.68 / 19.76 | 6.90 / 5.73 / 2.93 | 9.64 / 8.41 / 5.76 | STRADDLES 20 |
| alt | 22.85 | 23.80 / 22.85 / 21.21 | 7.72 / 6.58 / 4.40 | 10.64 / 9.55 / 7.37 | STRADDLES 20 |

Reported sensitivities (P1, E_mid; canonical / alt):
- **Binary fraction:** f_b = 0 gives 17.21 / 18.30; 0.1 gives 18.59 / 19.70; 0.3 gives 21.68 / 22.85; 0.5 gives 25.94 / 26.99.
  Binaries inflate the measured σ, which leaves less room for a field boost, so the floor rises.
- **Estimator:** E-V (global virial) gives 21.19 / 22.47. E-W (the record's Wolf estimator) gives 25.89 / 26.75.
- **Predicted σ_p at Υ_V 1.67 (canonical),** in the order AQUAL / L★ 24 / 50 / 90 pc / Newton, against the observed value:
  - Pal 4: 2.16 / 1.28 / 1.07 / 1.01 / 0.97 km/s, against 0.88.
  - Pal 14: 1.41 / 0.90 / 0.71 / 0.62 / 0.56, against 0.71.
  - NGC 2419: 5.81 / 5.54 / 5.02 / 4.64 / 4.36, against 4.77.
- **Mechanism.** Embedded in the Galactic field, the cluster responds with kernel m/(1 − m + κ²m/2). Screening sets in
  at kL★ ≳ 1.4, so the screening length is L★ itself, not the isolated l_γ = L★²/2r_M. Even so, the boost at L★ ≈ 24 pc
  is about ×1.3 in σ for Pal 4 and ×1.6 for Pal 14. The external field (x_e = 0.07–0.21) is too weak to suppress it.

## Checks: 10/10 PASS (exit 0, 989 s, single thread, peak RSS 0.909 GB)

- **K1:** sympy confirms p = v/(1+|v|) inverts h. The linear response equals C6's kernel. The L★ = 0 limit is AQUAL.
- **K2:** the 2D solve agrees with an independent 1D BVP to 3.2e-4.
- **K3:** the L★ = 0 isolated case agrees with the algebraic law to 1.7e-4.
- **K4:** the linear EFE case agrees with the Fourier route to 2.6e-3.
- **K5:** the Newton limit is recovered to 1.7e-8.
- **K6:** convergence changes the answer by 5.4e-5.
- **K7:** Jeans numerics are good to 5e-5. Amendment A1 corrects the frozen K7 constant from 3π/64 to π/32; this was pre-result.
- **K8:** CFG334 is reproduced (P = 0.264, median 1.155).
- **K9:** E4 N1 is reproduced exactly (28.853 / 29.123).
- **K10:** peak RSS is under 1 GB.

All 9000 production Newton solves converged (worst scaled residual 1.0e-10).
`--mutate` (L★² in place of L★²/2 in the 2D solver) breaks K2 (0.27) and K4 (0.20): 8/10, exit 1. That mode runs the
validations only.

## Input ledger

| input | class | source |
|---|---|---|
| σ_obs, eso, N; RV-bin radii | RAW | Baumgardt profile table via CFG332 json; `real_research/data/globular_clusters/` |
| V mag → L_V (distance, E(B−V)) | RAW + SURVEY-CALIBRATION | CFG332 |
| r_h,l, Plummer a = r_h,l, mass = light | SURVEY-CALIBRATION (structural fit) + model assumption | CFG332 / Baumgardt |
| R_GC | SURVEY-CALIBRATION (distance) | Baumgardt parameters |
| Υ_V P1 logN(1.6, 0.15 dex) | SURVEY-CALIBRATION (SPS) | CFG332 |
| Υ_V P2/P3 MF-slope | SURVEY-CALIBRATION, conditional (slopes from Newtonian N-body fits to star counts) | CFG332 route2 |
| MW M_b 6e10 (4e10, E_hi 1.23e11 / 1.15e11), Hernquist 3 kpc | SURVEY-CALIBRATION (E_lo is a stated round bracket, not from a source on disk) | A60 / CFG332; E_hi from D7b's E2 kinematic total |
| MW field law, the cluster field equation, Jeans on the monopole | FRAMEWORK-NATIVE | C4/C5/C6 frozen form; this lane |
| binary population (DM91, f_b 0.3), per-star error e_c fitted to eso/so | SURVEY-CALIBRATION | CFG334 |
| a₀ footings; κ = ½ | FITTED | FP0 |
| ΛCDM inputs | none | |
| STANDARD-MOND machinery | none in the verdict. ν_RAR + recipe appear only in K9's bridge to E4 (and E4's record value) | |

## What this does not show

- **Isotropic Jeans on the monopole is an approximation.** The EFE field is anisotropic. E-V is exact for the
  orientation-averaged global σ and agrees to 0.5 pc.
- **Not modelled:** mass segregation, tides, and departures from Plummer.
- **Per-star errors are not on disk.** e_c is calibrated to the published error. NGC 2419's e_c = 1.40 km/s absorbs its spread.
- **The D7d vector-Laplacian form (γ_F = γ_L) is not solved embedded.** It agrees with this form only when isolated.
- **The floor is set by the Υ_V prior.** The globulars cannot pin L★ above 20 pc unless Pal 4's M/L is known to ±0.15 dex
  near the SPS value. Multi-epoch RVs (binaries) and a direct Pal 4 M/L would settle it.

## Run
```
OMP_NUM_THREADS=1 nice -n 15 python3 doors_push_2026_10_22/D10_native_Lstar/d10_native_lstar.py            # ~17 min
OMP_NUM_THREADS=1 nice -n 15 python3 doors_push_2026_10_22/D10_native_Lstar/d10_native_lstar.py --mutate   # ~6 s
```
