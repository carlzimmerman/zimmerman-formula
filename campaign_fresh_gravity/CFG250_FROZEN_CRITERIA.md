# CFG250 — a mass-normalisation-free a₀ at z ≈ 1.5 from the SHAPE of the KURVS outer rotation curves: flat a₀ against a₀ ∝ H(z). FROZEN CRITERIA

Written 2026-09-29, in phase 1, before any measured KURVS velocity or dispersion was used by this lane. Phase 1 consists of this file, the theory script and the mock pre-flight in `CFG250_massfree_slope_a0/`. Nothing below may change after a measured value is used. Any later deviation goes in the lane README as a disclosed departure.

**This is NOT a blind test.** Section 1 lists what the analyst already knew.

## 0. Order of work (stated first)

1. I read the earlier KURVS lanes for conventions (listed in section 1).
2. I wrote and ran `CFG250_slope_theory.py`, which uses catalogue columns only.
3. I wrote and ran `CFG250_preflight.py` on mocks only.
4. After the first mock runs I made the design changes listed in section 9. None of them was informed by data.
5. I then wrote this file.
6. The pre-flight outcome (section 8) was computed before this file was finished. It is part of the frozen gate.

## 1. What the analyst had seen (not blind)

**Earlier results known in advance:**

| lanes | result |
|---|---|
| CFG140/141 | P1/P2 both under-predict at realistic gas |
| CFG160/165 | the model-velocity decision cell under Kretschmer leans toward the rival: flat +3.3σ, rival −0.1σ at μ = 0.67 |
| CFG162/164 | the crossing s_mid = 0.67; the gas prior is non-diagnostic |
| CFG184 | beam smearing of the outer σ is minor, about 9% of σ² |
| CFG189/194 | the measured markers keep the lean but make it fragile: flat +2.4σ, rival −0.4σ; the class turns on which radius counts as "outer"; a coherent 4.5% lower V removes it; P0 at the markers leans flat |

**Measured numbers seen while reading those READMEs and notes:**
- the ten discs' σ₀ (40–74 km/s) and σ_out (28–77 km/s), from CFG141's table; σ_out/σ₀ median 1.05;
- the V_c²/V_obs² ranges: 1.5–6.1 under P2 and 1.19–2.52 under P4;
- CFG184's σ_bs per disc;
- CFG189's per-disc measured-versus-model outer V, −22% to +11%;
- two model velocities (KURVS-3 208.6/209.8 km/s, KURVS-15 113.2/112.2 km/s), one tabulated velocity (KURVS-4, 8.0 km/s) and one marker error (KURVS-3, ±32.9 km/s);
- the paper's sample-median V(R′₆D)/σ₀ = 1.6 (16–84%: 1.0–2.0), from `KURVS_DEFINITIONS_NOTE.md` and `KURVS_SIGMA_METHODS_NOTE.md`.

**What was NOT read:**
- No marker velocity (`v_obs_kms`) and no marker dispersion (`sigma_obs_kms`).
- No σ₀ or V/σ₀ column, and no f_DM value.
- No rotation-curve shape.

**Columns this lane read** (by `usecols`/`DictReader` key only; listed in `CFG250_preflight.py`'s header):
- `kurvs_rc_points.csv`: `kurvs_id`, `R_kpc`, `err_up_kms`, `err_lo_kms`, `clipped_white_marker`;
- `kurvs_sigma_profiles.csv`: the same five columns;
- `kurvs2023_integrated.csv`: `z_halpha`, `logMstar`, `reff_kpc`, `inc_sfr_deg`, `inc_star_deg`;
- `kurvs2023_fdm.csv` and `kurvs2023_kinematics.csv`: `kurvs_id`, `flag_star`, `R_halpha_max_kpc` (a radius: printed once while exploring, and not used by any script).

**The mock σ grid (20/30/45/60 km/s) was chosen with the KURVS σ₀ range known.** The primary mock value of 45 km/s is a literature-typical z ≈ 1.5 Hα dispersion and sits below the ten discs' median.

## 2. The idea and the theory (CFG250_slope_theory.out)

**Point-mass law.** g = ν(y) g_N with y = g_N/a₀ and Φ = yν. The log-slope of V_c² is s = 1 − 2 dlnΦ/dlny.
- Under P2: s = −y/(1+y) and y = −s/(1+s).
- a₀ = g_obs/Φ(y(s)).
- d ln a₀/ds = (s−1)/[2s(1+s)].

**Generalisation used here: the shape-aware (DS) form.** Where the baryon shape has Newtonian log-slope s_N:
- s = 1 + D(y)(s_N − 1), with D = dlnΦ/dlny, so D = (1 − s)/(1 − s_N);
- s_N = −1 recovers the point mass;
- it is still free of the mass NORMALISATION, but it needs the baryon SHAPE.

**The laws.** E(1.5) = 2.3679 exactly for Ω_m = 0.315 (log 0.374); the task's "≈ 2.2" is approximate. At the ten discs' median z of 1.529, the rival sits at +0.381 dex.

**What the theory establishes.** The typical disc here is log M* 10.14, R_d 2.29 kpc, with gas at 2R_d and μ = 0.67.
- **Point-mass bias.** The disc's Newtonian slope is s_N = +0.23, −0.24, −0.56 and −0.91 at 2, 3, 4 and 6 R_d. The MOND curve there is still rising: s = +0.43 and +0.14 at 2 and 3 R_d (flat law). So the point-mass estimator returns a₀ → ∞ at 2–3 R_d, +0.87 dex at 4 R_d and +0.11 dex (flat) / +0.24 dex (rival) at 6 R_d. The bias has the rival's sign.
- **Shape (gas) systematic of DS.** Across μ 0.25–4 and R_gas 1–3 R_d, the DS bias spans −0.31 to +0.55 dex at 4 R_d and −0.25 to +0.31 dex at 6 R_d (flat law).
- **Pressure.**
  - A mis-specified term shifts s by (ΔP/V_a²)(1 − s_c).
  - At σ = 45 km/s the k = 2 fraction of V_c² is 0.45–0.80 at 2–4 R_d (flat law). The typical flat-law disc becomes pressure-dominated (V_c² < 2σ²R/R_d) by 6 R_d, and by 3 R_d at σ = 60.
  - Analysing a k = 1 truth with k = 2 shifts s by +0.11 to +0.43.
- **Required accuracy.** A coherent slope error of +0.11 to +0.16 mimics the entire flat → rival gap.

## 3. Sample and per-galaxy exclusions (catalogue/paper flags and radii only)

- **Primary:** the ten rotation-supported discs of the f_DM table (KURVS 3, 7, 8, 9, 11, 13, 15, 16, 17, 21), as in CFG140–194.
- **Radius rule,** applied before any velocity is read: a disc is used only if its window (section 4) holds ≥ 5 unclipped markers spanning ≥ 0.25 in ln|R|. All ten pass (KURVS-17 has 5).
- **Variants (reported):**
  - S1 drops KURVS-21 (`*`, the asymmetric velocity field);
  - S2 is all 22 minus the `*` rows of either table (KURVS-10, KURVS-21), under the same radius rule;
  - S3 drops KURVS-17 (its outermost two markers are clipped, and its σ panel is offset 0.065 kpc).
- **Clipped markers** (the authors' white circles) are excluded everywhere.

## 4. The estimator (identical to the pre-flight's `analyst()` / `stacked()`)

1. **Window (primary):** |R| ≥ R_in = max(2 R_d, FWHM_kpc).
   - R_d = R_eff/1.68.
   - FWHM_kpc = 0.57″ × the angular scale at z_Hα (H₀ 70, Ω_m 0.3, as CFG184).
   - Both sides are pooled by |R|.
   - Variants: |R| ≥ 3 R_d; |R| ≥ max(2 R_d, 1.5 FWHM); |R| ≥ 2 R_d without the beam guard.
2. **Velocity:** V = v_obs · sgn(R) / sin i_SFR, with e_V = ½(err_up + err_lo)/sin i_SFR. Variant: i*.
3. **Dispersion:** σ_win is the inverse-variance-weighted mean of the unclipped σ markers with |R| in the same window, both sides, observed σ as plotted.
   - Its error is (Σ e⁻²)^(−½) × √6.
   - It is held constant across the window. Variant: the local σ(R) interpolated on the same side.
4. **Pressure (primary):** V_c² = V² + 2 σ_win² |R|/R_d.
   - Variants: P0 (none, a scenario); k = 1; Kretschmer+2021 α(|R|/R_eff − 1) σ_win² × {0.6, 1, 1.4}, clipped to [0, 4] as in CFG160.
5. **Fit:** a weighted LSQ of ln V_c² on ln|R|.
   - Weights are 1/σ_ln², with σ_ln = 2|V| e_V / V_c².
   - The result is the slope s and the intercept A at the weighted mean ℓ̄ of ln|R|.
   - Formal errors are multiplied by √6 (correlated markers: 0.6″ bins at 0.1″ sampling).
   - σ_win's error is propagated into s and A numerically.
   - The ln g_obs error also includes 2 cot i · 5° · (1 − f̄).
   - g_obs = 10⁶ e^A / (e^ℓ̄ kpc).
6. **Prediction, DS (PRIMARY).**
   - Declared baryon shape: thin exponential stars (R_d) plus thin exponential gas at 2 R_d with μ = 0.67 (the paper's 40% molecular fraction).
   - Only the shape enters: no M*, no gas mass.
   - For a trial a₀, the model is y(R) = y_piv u(R)/u(R_piv). Its normalisation is set so that the model's weighted mean of ln V_c² equals the data's intercept A.
   - The predicted slope is the same weighted fit applied to ln[Φ(y) R] at the window radii.
   - Shape variants: μ ∈ {0.25, 1.0, 1.5, 4}; R_gas/R_d ∈ {1, 3}.
7. **Prediction, PM (the idea as stated; reported):** the same with u ∝ R⁻². Also per disc, the local inversion y = −s/(1+s), which gives an a₀ lower limit if s ≥ 0 and an upper limit if s ≤ −1.
8. **Stacked statistic:** Λ̂ = log₁₀ â₀ for a common a₀.
   - χ²(Λ) = Σ_i [s_i − s_pred,i(Λ)]² / [σ_s,i² + (∂s_pred/∂ln g)² σ_lng,i²].
   - The grid is log₁₀(a₀,canonical) ± 1.5 dex in steps of 0.01, with parabolic refinement.
   - σ_stat comes from Δχ² = 1, inflated by √(χ²_min/(N−1)) when that exceeds 1.
   - A minimum at the grid edge, or a Δχ² = 1 interval leaving the grid, is a LIMIT.
   - χ² p < 0.01 means the model (shape + pressure) is REJECTED.
9. **Predictions:**
   - flat: Λ_F = log₁₀ 9.3603e-11 (canonical; the alt footing 1.1312e-10 is reported);
   - rival: Λ_R = Λ_F + log₁₀ E(z_med), with z_med the sample median z_Hα (+0.381 dex for the ten).
10. **Kernel:** P2 primary; ν_mono reported in every row.

## 5. Systematic error (fixed by the pre-flight, before data)

**Definition.** σ_sys is the quadrature sum, over the declared axes, of half the spread of the mock-mean Λ̂ (the larger of the flat and rival spreads):

| axis | what varies | what the analyst uses |
|---|---|---|
| A: pressure truth | {k1, k2, K21×0.6, K21, K21×1.4} | k2 |
| B: baryon-shape truth | μ {0.25, 0.67, 1.5, 4} at 2R_d, and R_gas {1, 3} R_d at μ 0.67 | the declared shape |
| D: inclination | truth i* | i_SFR |

**Frozen values** (the smearing-free track, DS, P2), with phase 2 interpolating at the sample's median σ_win:

| σ (km/s) | σ_sys (dex) |
|---|---|
| 20 | 0.416 |
| 30 | 0.453 |
| 45 | 0.502 |
| 60 | 0.494 |

- The components at σ 45 are A 0.298, B 0.399 and D 0.061.
- **These are LOWER bounds.** At σ ≥ 45, five of the ten axis-A cells put the stack at the grid edge and are left out of the spread.
- **Beam smearing is NOT in this σ_sys.** On seeing-limited mocks it is not a spread but a failure: see H0.

## 6. Decision lines (phase 2)

- **H0 (feasibility gate, frozen here and evaluated in the pre-flight).** Phase 2 can be DIAGNOSTIC only if both of these hold on seeing-limited KURVS-like mocks at σ = 45:
  - the primary returns a usable stack (at the grid edge or model-rejected in < 50% of mocks, for both laws);
  - it separates the laws by ≥ 2σ including σ_sys.
- **If H0 fails, the phase-2 verdict is NON-DIAGNOSTIC by construction.** The numbers are reported as a measurement only.
- **If H0 passed** (it does not; section 8), with σ_tot = √(σ_stat² + σ_sys²), z_F = (Λ̂ − Λ_F)/σ_tot and z_R = (Λ̂ − Λ_R)/σ_tot:

| outcome | condition |
|---|---|
| lean flat | \|z_F\| ≤ 2 and \|z_R\| > 2 |
| lean rival | \|z_R\| ≤ 2 and \|z_F\| > 2 |
| NON-DIAGNOSTIC (both allowed) | both ≤ 2 |
| NON-DIAGNOSTIC (both disfavoured: points at the pressure/shape/smearing model, not at a law) | both > 2 |
| NON-DIAGNOSTIC (limit, or model rejected) | a stack at the grid edge, or χ² p < 0.01 |

- **Kill line for flat a₀ at z ≈ 1.5 under this estimator:** z_F > 3 or z_F < −3 in EVERY declared variant (sections 3 and 4) while z_R is within 2. The same holds symmetrically for the rival.
- **Never** "the data favour the framework". A lean is not a detection.

## 7. Controls and MUTATE

- **C1:** a noise-free point-mass mock is recovered by PM to < 2e-3 dex.
- **C1b:** a noise-free disc mock with the declared shape is recovered by DS to < 2e-3 dex.
- **C2:** a pure-Newtonian point-mass mock gives s = −1, y → ∞, so only an a₀ UPPER limit (the stack at the lower grid edge).
- **C3 (MUTATE must fail it):** a smearing-free matched mock under flat truth is unbiased, |mean Λ̂| < 0.25 sd.
- **C4 (reported):** coverage, sd/median σ within [0.67, 1.5].
- **MUTATE (phase 1 and phase 2):** every analyst V is multiplied by (|R|/1 kpc)^0.1 before the pressure term is added.
  - Phase 1: C1, C1b, C2 and C3 must fail and the run must exit 1.
  - Phase 2: Λ̂ must move by > 2σ_stat, or the per-disc domain status (a limit versus finite) must change for ≥ 3 discs. Otherwise the MUTATE is reported as not biting, and the result is kept.
  - Outputs are written separately (`*_MUTATE*`).

## 8. Pre-flight outcome (mocks only; computed before this file was finished)

- **Beam smearing alone biases the window slope** (noise-free, flat law, no pressure):

  | smearing configuration | slope bias (per-disc range) |
  |---|---|
  | 0.57″ PSF, 0.6″ bins, Hα scale R_d (primary) | **+1.01 (+0.57 to +1.63)** |
  | 0.1″ bins | +0.70 |
  | optimistic | +0.58 |
  | pessimistic | +1.65 |
  | AO-like 0.15″ | +0.09 |

  This is 5–15 times the +0.11 that mimics the whole flat → rival gap.
- **H0 FAILS.** The seeing-limited primary stack is at the grid edge and model-rejected in 100% of mocks under both laws.
- **Even with smearing removed** (the AO / forward-model limit):
  - S_stat = 2.1 at σ 45, 2.3–2.4 at σ 20–30.
  - With σ_sys = 0.50 dex, S_tot = 0.65.
  - The frozen rule returns "both allowed" in 99% of flat-truth mocks and never a lean. P(lean rival | flat truth, marginal) = 0.00.
- **PM (the idea as stated) is unusable at KURVS radii.** Even without smearing its stack sits at a grid edge in 100% of the matched-cell mocks, and in 59–100% across the smearing-free cells. The reason is that per-disc s ≥ 0 in 42–99% of fits.

**Therefore the phase-2 verdict on KURVS, as frozen here, is NON-DIAGNOSTIC by construction.**

**Pre-registered hand expectation for phase 2** (made before any measured V or σ is used). With the paper's median V/σ₀ ≈ 1.6 and the smearing bias above:
- most discs' k = 2 corrected slopes will lie above the DS domain (s > (1 + s_N)/2), i.e. a₀ lower limits;
- the stack will hit the upper grid edge or be rejected;
- under P0 the slopes will be shallower, and the stack may give a finite Λ̂.

None of this bears on the laws.

## 9. Design changes made after the first mock runs (no measured data involved)

1. **The fitted intercept is matched, not the curve at the pivot.** The first form biased the noise-free controls by 4e-3 dex through curvature.
2. **The pseudo-slit is flux-weighted, and its half-width scales with the PSF** (0.3″ at 0.57″). The first form was an unweighted mean at a fixed 0.3″.
3. **C4 was made non-load-bearing.** The reported σ is conservative, sd/median σ = 0.66 against a line of 0.67.
4. **The pre-flight was split into two tracks:** a seeing-limited track (the H0 gate) and a smearing-free track (the systematic axes). The first run showed every seeing-limited cell at the grid edge, which left the axes undefined.
5. **The primary window, the pressure primary, the DS shape and the sample were NOT changed.**

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
