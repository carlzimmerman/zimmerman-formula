# GH1_matched_lensing_satellites: FROZEN CRITERIA (committed alone, before any shear is read)

**Question.** In the same route E model, KiDS lensing of B21's isolated lenses wants M200 +0.30 to +0.50 dex above
EM1's SPARC relation (X53 / X74_smooth_core_lensing). GAMA satellites around G09 centrals want +0.78 (X75). X78 showed
the two probes disagree by ~0.3–0.4 dex at fixed M★ in *any* gravity model. Is that gap a **sample difference**
(isolated lenses vs centrals) or a **method systematic** (lensing vs dynamics)?

**Test:** measure KiDS-1000 lensing around **exactly X75's G09 central hosts**, over the satellites' own aperture
(50–300 kpc), and fit the same model.

## Data (on disk; no fetch)

- **Lenses:** X75's frozen host sample, rebuilt by X75's committed code unchanged: 9,049 G09 centrals, 0.05 ≤ z ≤ 0.25,
  B21 bins.
- **Sources:** `_external_data/cfg652_work/cfg652_sources.npz`, the KiDS-1000 DR4.1 SOM-gold sources in the G9 box
  (1.24 M; RA, Dec, e1, e2, weight, Z_B), staged by CFG652's committed `cfg652_stage.py`.

## Estimator (CFG652's committed estimator; only the background changes)

- **Sources per lens:** Z_B > z_l + 0.2.
- **ΔΣ** = Σ w_s Σ_crit⁻¹ e_t / Σ w_s Σ_crit⁻², with Σ_crit from point Z_B.
- **Background: native, not CFG652's flat (0.3, 0.7):** h 0.679 and Ω_m 0.3085, F2's native background as X53/X75.
- **Radial bins:** 12 log bins, 30–3000 kpc physical. Graded radii: 50 ≤ R ≤ 300 kpc (bin centres inside).
- **Randoms:** 5 per host, uniform over occupied 0.1° source cells, z drawn from the host z's. The random signal is
  subtracted.
- **Covariance:** 30 jackknife patches (equal-count RA slices; randoms share the edges), all four bins jointly.
- **Calibration:** no multiplicative m-correction (|m| ≈ 1–2 % in KiDS-1000) and no boost correction. Both are
  disclosed. The boost (lens/random weighted source counts) is reported only.

## Model (identical to X75)

- **(H):** route E smooth-core halos, M200 from EM1's SPARC relation shifted by a common Δ (log M200), truncated at
  R200, plus F2 baryons. X53 machinery, as in X75.
- **(L):** the isolated law with F2 baryons.
- **Stacking:** per radial bin, ΔΣ_model(R_k) = Σ_i W_ik ΔΣ(lm_i, R_k) / Σ_i W_ik, with W_ik the measured lens weight
  (Σ w Σ_crit⁻²) of host i in bin k. No two-halo term inside 300 kpc; this is disclosed, and the term is reported via
  the 300–3000 kpc residual.

## Statistic and verdict (frozen)

- **Δ_lens:** the common log M200 shift minimising χ² over all four bins at 50–300 kpc with the jackknife covariance
  (Hartlap-corrected). Grid −0.5 to +1.5, step 0.01; 1σ from Δχ² = 1.
- **Δ_sat:** X75's frozen +0.79 [+0.75, +0.82] canonical and +0.78 alt.
- **Classes, per footing:**
  - **PROBES AGREE ON MATCHED HOSTS:** |Δ_lens − Δ_sat| < 2√(σ_lens² + σ_sat²). The earlier gap is the sample.
  - **PROBES DISAGREE ON MATCHED HOSTS (lensing lighter / heavier):** otherwise. A method systematic, e.g. velocity
    bias, anisotropy, interlopers, or photo-z dilution.
- **Reported:**
  - law χ² on the same lensing points;
  - Δ_lens per bin;
  - Δ_lens with a boost correction;
  - the cross-shear null (χ² of ΔΣ_× at 50–300 kpc against zero);
  - Δ_lens at 50–200 kpc.

## Checks

- **K1:** the estimator reproduces CFG652's committed ΔΣ for its 148 eFEDS groups in its own (0.3, 0.7) background
  to 1e-6 relative.
- **K2:** the host sample equals X75's committed counts: hosts [3651, 2411, 1690, 1297], pairs [318, 468, 574, 727].
- **K3:** the model at Δ = 0 equals X75's mass_H (exact).
- **MUTATE:** rotating source ellipticities by 45° (e_t → e_×) must give a ΔΣ consistent with zero (χ² p > 0.01), and
  the Δ fit must hit the grid floor or be undefined.

κ = ½ FITTED; c_f EXTERNAL; footings never pooled; cold dark energy is a gravitating field component, never a particle;
not theory closed; nothing here says the data favour the framework. One thread, nice 15, RSS < 1 GB (X48 A4 is live).
