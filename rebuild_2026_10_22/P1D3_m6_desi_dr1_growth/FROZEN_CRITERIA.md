# P1D3_m6_desi_dr1_growth: FROZEN CRITERIA (committed alone, before any P1D value is read)

**Question.** Does the DESI DR1 Lyman-α P1D at z = 2.2–4.4 (Karaçaylı et al. 2025, optimal estimator, arXiv:2505.07974;
Zenodo 10.5281/zenodo.16943723) allow X57's M6 at X57's bound? M6's signature is a frozen comoving gas excess, and its
ratio to the adiabatic power grows as 1/D(z)² toward high z. The test uses the large scales, where the native linear model
was adequate on Boera (P1D1 V-kcut p 0.97) and where DESI has per-cent errors.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 0. Data (owner-approved download 2026-10-27, "swing this"; untracked)

**`_external_data/desi_dr1_p1d_qmle/raw/data_points.tar`**

- Size: 131624960 bytes.
- md5 33d7fc21bfd3d745ed71a0bbe80ca433, matching the Zenodo record.
- sha256 07cd613944a7ee18af7b2e2044c08a48df5e4354a1e1ccd1e2f457ff0e89ade8.

**What is used.** From that tar, `desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits`:

- HDU `P1D_BLIND`, with column **PLYA** (km/s) at Z, K (s/km). Its header reads `BLINDING = desi_y1` (ledger C3).
- HDU `COVARIANCE` (1020 × 1020).

At commit time only the column names, the Z grid (12 bins, 2.2–4.4) and the K grid (85 per z, 0.00025–0.0527 s/km) have
been seen. No P1D value or covariance element has been read.

**Bins (the paper's own cut).** 0.001 < k < 0.5π/R_z, with R_z = c Δλ / ((1 + z) λ_Lyα), Δλ = 0.8 Å,
λ_Lyα = 1215.67 Å and c = 299792.458 km/s. This gives k_max ≈ 0.0255 s/km at z = 2.2 and ≈ 0.043 s/km at z = 4.4.

## 1. Step 0 (stop rule)

- **S0a.** The md5 matches.
- **S0b.** 12 z bins of 85 rows, with the grid as above.
- **S0c.** COVARIANCE is symmetric and positive definite on the selected bins. It equals COVARIANCE_STAT + COVARIANCE_SYST
  within 1e-6 relative (Frobenius). If it does not, report which is total and use the sum: STOP only if neither matches
  E_PK.
- **S0d.** √diag(COVARIANCE) equals E_PK within 15 % in every selected bin. This identifies E_PK and COVARIANCE as
  belonging to the same quantity. If the match fails for COVARIANCE but holds for COVARIANCE_STAT, STOP: the quantity
  match is ambiguous.
- **S0e.** P1D1's native M6 numbers are reproduced from P1D1's committed JSON to 4 decimals.

## 2. Model (P1D1 §3 verbatim, applied per DESI z bin)

P_F(k) = b_z² (k/k_p)^{α_z} P1D_gas(k; R_J,z) [1 + μ S_z(k; R_J,z)].

- The background is NATIVE, from L1: Ω_m 0.2976016, h 0.6856427, ω_b 0.0223081. σ₈ is 0.827959. n_s is 0.965, which is
  disclosed as not native.
- The M6 amplitude is the NATIVE F_b,max(z = 3), giving A = 0.07598 (Mpc/h)³ on both footings.
- **Nuisance per z:** b_z² > 0, R_J,z ∈ [0.02, 0.30] Mpc/h, α_z ∈ [−1, 1], with k_p = 0.01 s/km.
- **μ ≥ 0** is common to all z.
- The fit uses the full covariance on the selected bins, so cross-z correlations are kept.

## 3. Gates and verdict (each footing; identical by construction, both run)

These are as in P1D1 §4, with the same thresholds.

- **G0.** The null joint p ≥ 0.01, and every per-z p ≥ 0.001. A failure gives NOT DIAGNOSTIC (LINEAR NATIVE MODEL
  INADEQUATE).
- **G1.** The Asimov Δχ²(μ = 1 vs 0), profiled, is ≥ 9. A failure gives NOT DIAGNOSTIC (NUISANCE ABSORBS M6).
- **Verdict.**
  - M6 AT X57's BOUND EXCLUDED if Δχ²₁ ≥ 9.
  - M6-SHAPED EXCESS PRESENT if Δχ²₀ ≥ 9.
  - NOT EXCLUDED otherwise.
  - μ̂, μ_95 and F_b,95 are reported in every case.
- **Robustness.** ROBUST if all variants give the same class; otherwise FRAGILE, with the flipping variants named.
  - **V-k02:** k ≤ 0.02 s/km.
  - **V-stat:** COVARIANCE_STAT only.
  - **V-ns:** n_s ∈ {0.92, 1.00}.
  - **V-tilt0:** α_z ≡ 0.
  - **V-smoothz (the growth fingerprint):** R_J and α are linear in z across all 12 bins (4 nuisance parameters instead
    of 24), and b_z² stays free per z. This limits the nuisance's ability to mimic a 1/D² trend.
  - **V-hiz:** z ≥ 3.6 only.
- **Reported only.**
  - The inherited background.
  - The cov_diag_inflation file, applied as a diagonal multiplier only if its length is 1020 and every value is ≥ 1.
  - Per-z μ̂, from separate fits with μ free per z. These show whether any excess follows 1/D²; they are never graded.

## 4. Checks and twin

- **K1.** Parser and bin cut (S0b; bins per z reported).
- **K2.** μ = 0 gives the null exactly.
- **K3.** A planted μ = 1 (null best fit at μ = 1, plus covariance noise, seed 0) is recovered with μ̂ ∈ [0.5, 1.5] and
  Δχ²₀ ≥ 9 when G1 passes.
- **K4.** A planted null gives μ_95 < 1 when G1 passes.
- **K5.** Units: k(0.01 s/km, z) on the native E(z), exact round trip.
- **K6.** Peak RSS < 1 GB, one thread.
- **MUTATE (`P1D3_MUTATE=1`, separate outputs).**
  - m1: S sign flipped.
  - m2: PRAW instead of PLYA.
  - m3: the S0e target × 1.01.
  - The twin must fail S0e and K3 (K3 only if it is live).

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I p1d3_m6_desi.py`. Amendments only in `AMENDMENTS.md`,
each committed before the run it affects. No change to a gate, threshold or model after any P1D value is read.
