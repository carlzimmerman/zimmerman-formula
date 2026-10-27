# X63_displacement_forest_prediction: FROZEN CRITERIA (committed alone, before any script or number)

κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11, alt 1.1312e-10 m/s², never pooled. **Cold dark energy** is the
gravitating w ≈ 0 clumping field component paired with dark energy; it is not matter and not a particle. No
dark-matter particle. Framework-native inputs only. No downloads. No fitting. Not "theory closed". Nothing here may say
the data favour the framework; results are phrased "this test …".

Lane id: X62 is taken by the peer's `X62_environment_keyed_switch` (8c7768d26d), so this lane is X63.

## Question

X57 (`X57_exclusion_mechanism`, criteria 6cadf4f9b0, result 436ff03cb9) left class M6 (displacement) NOT DECIDABLE on
canonical and EXCLUDED on alt by its R4b line alone, and named the deciding observation: small-scale Lyman-α forest gas
power at z ≈ 4–5.5. This lane computes M6's prediction for that observable, at the largest amplitude X57's bounds
allow, and checks whether the record's own forest gates already exclude it.

## 1. The M6 model (as X57 defined it; X57 FROZEN_CRITERIA §3 M6, script L393–430)

- Galaxies form in cold dark energy deficits. The initial conditions anticorrelate baryons and cold dark energy on
  galaxy scales: compensated patches with ρ_b δ_b + ρ_c δ_c = 0 (total gravitating density unperturbed).
- Inside the galaxies' Lagrangian patches δ_c,in = −(1 − f_max), so δ_b,in = 5.364 (1 − f_max), with X22's f_max
  (0.196 canonical / 0.0269 alt).
- The isocurvature gas perturbation is frozen (it does not grow; total δ_m = 0 in the patches). The adiabatic power
  grows as D(z)².
- Positivity bounds the depleted Lagrangian volume: f_V ≤ 1/(1 + 5.364 (1 − f_max)) = 0.188 / 0.161.
- The forest bounds the fraction of all baryons in depleted patches: F_b ≤ F_b,max = 0.2 σ²_ad(R_L, z)/[δ_in²/(1 + δ_in)],
  graded at the tighter of z = 3 and z = 2, i.e. F_b,max(z = 3) = 0.060 / 0.048 (X57 JSON, re-read in Step 0).
- The CMB is blind to the compensated mode (max |ΔC_ℓ/C_ℓ| 7.4e-6, X57 JSON).

## 2. The spectral realisation used here (new in this lane; ledger B1–B6)

- **Patches:** Poisson-placed, non-overlapping top-hat Lagrangian patches of comoving radius R_L = X22's median
  0.442 Mpc/h (the value X57 used), volume V_p = 4π R_L³/3, volume fraction f_V = F_b/(1 + δ_b,in), uniform compensation
  outside. The gas isocurvature power is then P_iso(k) = f_V δ_b,in² V_p W²(k R_L) (k > 0), W the top-hat window.
- **Amplitude (primary, "as large as X57's bounds allow"): F_b = F_b,max(z = 3)** on each footing, f_V checked against the
  positivity bound.
- **Envelope (reported only, N2):** the amplitude at which the top-hat-smoothed isocurvature variance at R_L equals
  0.2 σ²_ad(R_L, z = 3), i.e. X57's ±20 % band applied to the smoothed rather than the point variance. This exceeds X57's
  stated F_b bound and is never graded.
- **Adiabatic power:** linear; X57's record BBKS shape (h 0.674, Ω_m 0.315, Ω_b 0.0493, n_s 0.965 as in X57's code),
  σ₈ = 0.82742 (EM1 own, as X57), growth D(z) from X22's `D_lcdm` on X22's background (Ω_b 0.0493, Ω_c = 5.364 Ω_b).
- **Gas filtering (PROVISIONAL):** both parts multiplied by exp(−k² R_J²) in power, R_J = 0.1 Mpc/h comoving (the record's
  own pressure scale in `real_research/g03_audit_2026/L347_switch_forest_flux_power.py`). Variants R_J = 0.05 and
  0.2 Mpc/h are reported. The filtering scale is not fitted.
- **1D projection:** P1D(k∥) = (1/2π) ∫_{k∥}^{k_max} k P3D(k) dk, k_max = 200 h/Mpc.
- **Flux-power proxy:** linear flux δ_F = b_F δ_gas with one bias for both parts; thermal broadening and the mean
  transmission act on k∥ alone. All of these cancel in the ratio, so the proxy ratio is the gas 1D-power ratio. Redshift
  -space distortions are not included (the frozen mode carries no peculiar velocity; a Kaiser boost on the adiabatic part
  alone would lower the ratio, so omitting it is generous to the signal).
- **Velocity units:** k[h/Mpc] = k[s/km] × 100 E(z)/(1 + z), E(z) from X22's background.

## 3. The predicted observable

R(z, k) = P1D_gas(adiabatic + M6)/P1D_gas(adiabatic) = 1 + P1D_iso/P1D_ad, at z = 4.2, 4.6, 5.0, 5.4 and k = 0.005–0.1 s/km
(20 log-spaced points), on both footings. The signal is S = R − 1. Also reported: S at z = 3, 2 for reference, and the
z-scaling S(5.4)/S(4.2), which must equal [D(4.2)/D(5.4)]² for a frozen mode.

## 4. Record forest gates (do they constrain an excess?)

- **The gates used by X4 / X18 / X22** (`forest_class`, X22 L154–161): T² in the six L346 bins (k 1.10–3.56 h/Mpc) at
  z = 3 and 2, and T²(k5 = 4.62 h/Mpc) at z = 3 and 2.
  - FAIL if T²(k5) < 0.9, or any bin < 0.5, or any bin > 2.0.
  - PASS if every bin is in [0.8, 1.2] and T²(k5) ≥ T²_5.3keV (L319 strict line, 0.995).
  - Otherwise UNDECIDED.
- **Applied to M6:** T²_proxy(k, z) = 1 + P_iso,gas(k)/P_ad,gas(k, z) in 3D (the filter cancels), on the primary amplitude,
  each footing.
- **Statement required:** which pieces of the gate can bite on an excess (the L346 upper edges 1.2 / 2.0) and which bite
  only on a suppression (the k5 ≥ 0.9 line, the L319 strict line, the L346 lower edges).
- Reported only: L347's P1D gate (|P1D ratio − 1| ≤ 0.10 for k∥ 0.2–2 h/Mpc at z = 3, 2) applied to the M6 proxy ratio. It is
  not one of the gates named for grading.

## 5. Verdict classes (per footing; one verdict if the footings agree)

- **M6 EXCLUDED BY RECORD FOREST LINES** if `forest_class` returns FAIL for the primary amplitude at the primary R_J. The
  failing piece (which bin, which z, which edge) is stated.
- **M6 PREDICTION COMPUTED; TESTABLE AT LEVEL X** otherwise. X = the largest S over the z = 4.2–5.4 × k = 0.005–0.1 s/km grid,
  quoted with the per-z maxima, and compared with PROVISIONAL typical per-bin fractional precisions σ_PROV (ledger B7):
  - medium-resolution surveys (eBOSS / DESI P1D; z ≤ 4.6, k ≤ 0.02 s/km for eBOSS and ≤ 0.04 s/km for DESI): 0.03;
  - high-resolution spectra (XQ-100, HIRES / MIKE / UVES; z 4.2–5.4, k up to 0.1 s/km): 0.10.
  The qualifier is **ABOVE TYPICAL PER-BIN PRECISION** if S/σ_PROV ≥ 1 in at least one bin of at least one dataset class,
  else **BELOW TYPICAL PER-BIN PRECISION**. The combined S/N over the bins (independent bins assumed) and the per-bin
  precision needed for a combined 3σ are reported. The precisions are PROVISIONAL (not transcribed by the record).
- **UNDECIDED** if, between the R_J variants (0.05, 0.1, 0.2 Mpc/h), the gate class switches between FAIL and not FAIL, or
  the testability qualifier flips.

## 6. Step 0 (stop rule)

Reproduce from committed outputs; **if any item fails, stop: nothing is graded.**
- X57 M6 (JSON `M6`): δ_c,in, δ_b,in, fV_max, Fb_max (z = 3, 2), sigma2_ad_RL_z0, var_per_Fb (both footings); CMB
  max_rel_TT_compensated. JSON floats to 1e-9 relative. My recomputation of σ²_ad(R_L, 0) and of F_b,max with X57's
  code must agree with the JSON to 1e-9 relative.
- X22 forest numbers (JSON): k5 = 4.6199 h/Mpc, T²_5.3keV = 0.99519, α_NF 0.02991 Mpc/h, λ_hm 0.4167 Mpc/h, the L346
  bins (six, 1.101–3.557 h/Mpc) and bands (identical to X4 F0a to 1e-9), and R_L median 0.442 Mpc/h.
- L347's R_J = 0.1 Mpc/h read from its script text.

## 7. Checks (all must PASS in the normal run)

- K0 Step 0 (all items in §6).
- K1 Projection: for P3D = exp(−k² s²) the numerical P1D equals exp(−k∥² s²)/(4π s²) to 1e-6 relative (s = 0.3 Mpc/h,
  k∥ = 0.5, 2, 5 h/Mpc).
- K2 M5 null: with the M6 amplitude set to zero, R ≡ 1 to 1e-12 everywhere.
- K3 Sign and positivity: δ_c,in < 0 (patches depleted of cold dark energy), 1 + δ_b,in > 0, f_V ≤ the positivity bound,
  and S > 0 at every graded (z, k).
- K4 Frozen-mode scaling: S(5.4, k)/S(4.2, k) = [D(4.2)/D(5.4)]² to 1e-6 relative at every k.
- K5 Units: k[h/Mpc] at k = 0.01 s/km, z = 5 equals 100 E(5)/6 × 0.01 to 1e-12, and the round trip is exact to 1e-12.
- K6 Peak RSS < 1 GB, one thread.

## 8. MUTATE twin (`X63_MUTATE=1`; outputs suffixed `_MUTATE`)

- m1: anticorrelation sign flipped (δ_c,in = +(1 − f_max), so δ_b,in = −5.364 (1 − f_max)).
- m2: the isocurvature mode grows with D² like the adiabatic one (not frozen).
- m3: Step 0 compares X57's F_b,max(z = 3, canonical) with the committed value × 1.01.
**Required:** K0, K3, K4 FAIL; K1, K2, K5, K6 PASS; exit code 1. Any other pattern means the twin is broken. MUTATE
outputs are control outputs, not physics.

## 9. Reported only (no grade)

The published datasets that would decide M6, with the k-range and the per-bin precision needed, each marked "needs an
owner-approved download". Nothing is downloaded.

## 10. Rules

Small jobs only (< 1 GB, OMP_NUM_THREADS=1, nice -n 15); no downloads; nothing outside this lane is edited; peer lanes
read only. Every README number comes from the committed `.out` / `_results.json`. Commit by pathspec only; no push.
