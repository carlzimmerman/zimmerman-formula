# L319–L320 — the Λ-triggered kicked-decay carrier, and the pincer it exposes

## L319 — the one dark-sector door the record left untested

`L319_lambda_triggered_kicked_decay.py` reuses the validated exact linear-response solver from L168, copied rather than edited, with CLASS initial conditions. Its controls:

- The ΛCDM growth matches CLASS to 1.1%.
- With v_k = 0 the model reproduces ΛCDM. The residual is first-order discretisation: 1.56e-3, 1.11e-3 and 7.7e-4 at N_A = 300, 420 and 600 (`L319_c2_convergence.py`).
- It reproduces L168's universal-lifetime cell: S8 = 0.7865, with the forest failing.

`MUTATE=1` replaces the trigger with a universal lifetime of the same f_d(0); the forest then fails and rc = 1. A resolution re-run is recorded in `_NA600.out`.

**Model.** X → Y + light, with an isotropic kick v_k given to the daughter. The decay rate is Γ ∝ [Ω_Λ(a)/Ω_Λ,0]^p. The record closed kicked decay only for a *universal* lifetime (the forest needs τ ≥ 41 Gyr, galaxies need τ ≤ 20 Gyr). A rate triggered by vacuum domination avoids that pincer by construction.

| Cell | f_d at z = 3 / 2 / 1 | Power at k = 5 h/Mpc (z = 3, z = 2) | S8 |
|---|---|---|---|
| p = 2, f_d(0) = 0.8, v_k = 600 | 0.0004 / 0.0031 / 0.048 | 0.9996, 0.9965: **strict forest pass** (≥ the 5.3 keV relic) | **0.826** |
| p = 2, f_d(0) = 0.8, v_k = 1000 | same | 0.9995, 0.9957: strict pass | **0.803** |

For comparison, KiDS-Legacy measures 0.815 ± 0.016 and Planck 0.834. **This is the first carrier on the record to pass both the forest and S8** while depleting 80% of the cold component by today, which is what galaxies need.

## L320 — the price at high redshift, and a framework result

`L320_carrier_highz_price_rc100.py` (4/4; `MUTATE=1` sets the retained fraction to zero, and the rise and overshoot findings fail, rc = 1). Each of RC100's galaxies (z = 0.6–2.5) is predicted under three models and pushed through the data's own closed-form inversion. The systematic grid covers disc geometry, gas fraction and a₀ footing.

| Model | d log a₀/dz | Median f_DM inside R_e |
|---|---|---|
| **RC100 data** | −0.112 ± 0.062 | 0.29 |
| Framework alone | 0 (flat, exactly) | **0.23–0.31** |
| Framework + L319 carrier | +0.07 to +0.10 (**3.0–3.4σ against the data**) | 0.48–0.59 |
| ΛCDM alone (Moster+13 halo masses, Dutton–Macciò concentrations, no contraction) | +0.13 to +0.15 | 0.38–0.49 |

**Two results:**

1. ~~On RC100 the framework alone beats ΛCDM on both the level and the trend.~~ **Corrected by L323: the LEVEL is a tie.** Given its fair systematic range (NFW, a −0.2 dex lighter halo, or −0.1 dex lower concentration), ΛCDM also matches RC100's median f_DM. **The TREND is robust:** every ΛCDM variant, including a maximal feedback core and the combination most favourable to ΛCDM, predicts a₀ rising at +0.13 to +0.16 dex/z, 3.7–4.1σ above RC100's trend, while the framework is flat (1.6σ). RC100's caveats apply: its f_DM is model-dependent and its selection is uncontrolled.
2. **The forest–RC100 pincer applies to any carrier.** The forest needs a cold component clustered in the intergalactic medium on 0.1–1 Mpc scales at z = 2–3. RC100 says galaxies at that same epoch carry no cold halo. Kicks remove matter from shallow wells first, so they deplete the intergalactic medium before galaxy halos, which is the wrong order. A carrier would have to be absent from galaxy halos while present in the intergalactic medium at z ≈ 2, and also present in clusters today: a switch that is non-monotonic in potential depth. The record has found no such switch (f22).

**Standing:** the Λ-triggered carrier passes the forest and S8 but is disfavoured at about 3σ by RC100. The structural conflict between closing the dark sector and the framework's flat-a₀(z) galaxies is now explicit.

## L321 — the z = 0 gates on the real X-COP sample, with both couplings

`L321_carrier_z0_retention_gate.py` (4/4; `MUTATE` v_k = 0 fails G1, rc = 1). Retention is computed by exact phase-mixing in the framework's gravity (ν_RAR plus the SW01 magnitude-based external-field rule), relative to a no-decay control drawn with identical random numbers. C2 reproduces the record's 0.576 by an independent route: the additive median over 12 X-COP clusters is 0.476.

- **Universal coupling** (the carrier sources the MOND field) is **dead at z = 0 on clusters**. Retained daughters are MOND-boosted, and X-COP overshoots by 1.56–1.84× at every kick S8 allows. ⚠️ Correction from L322's mutation run: the *galaxy* failure (+0.08–0.10 dex) holds at f_d(0) = 0.8 only; at f_d = 0.9 universal galaxies pass (+0.042 dex).
- **Additive coupling** (a metric-coupled carrier) passes every galaxy host. X-COP overshoots by 1.34 at the kicks S8 allows.
- ⇒ **A dark carrier in this framework must not source the MOND field.** The binding reason is the clusters, not the galaxies.

## L322 — the additive window, RC100, and a coincidence test

`L322_additive_window_and_coincidence_test.py`. All thresholds were declared before the scan.

| Threshold set | Window |
|---|---|
| Strict: S8 ≥ 0.767 (KiDS-Legacy 3σ); X-COP within 20% | **none** |
| Alternative: S8 ≥ 0.748 (DES × KiDS 3σ); X-COP corrected for the measured 6% non-thermal support | v_k 1400–1700 (f_d 0.8), 1300–1400 (f_d 0.9) |

- RC100 under additive coupling is **3.5–3.7σ against the carrier**, with f_DM 0.49–0.56 against 0.29.
- **Coincidence test, with pre-declared candidates and a look-elsewhere count:**
  - For the decay rate, Γ₀ = 5.5–8.4 H₀ and none of the 28 framework-rate candidates falls in it (chance of at least one: 0.93).
  - For the kick, 1 of 27 candidates falls in the window: √(a₀ × 1 Mpc), which uses an arbitrary length, with a chance rate of 0.84.
  - **No coincidence.**

**Standing of the carrier:**
- It passes the forest and S8.
- It must be metric-coupled.
- It survives z = 0 only in a threshold-dependent sliver.
- It is disfavoured at about 3.5σ by RC100.
- Its rate has no natural scale.

The dark-sector door is now stated as precisely as the record allows: cold in the intergalactic medium at z = 2–3, absent from galaxy halos at z ≲ 2.5, about half-present in clusters at z = 0, and not sourcing the MOND field.

## L323 — stress test of the RC100 comparison, with ΛCDM given every fair chance

`L323_rc100_framework_vs_lcdm_stress.py` (6/6; `MUTATE` +0.25 in f_DM breaks the level tie, rc = 1). ΛCDM variants tried: NFW (Moster+13 halo masses, Dutton–Macciò concentrations), a halo 0.2 dex lighter, concentration 0.1 dex lower, a maximal Read+2016 core (n = 1, r_c = 1.75 R_e), Blumenthal contraction, and all of the favourable ones together.

- **Level (median f_DM inside R_e): tie.** The framework's best cell and the NFW, lighter-halo and lower-concentration cells all contain zero offset at 68%. **The L320 level claim is withdrawn.**
- **Trend (inverted a₀ against z): every ΛCDM variant rises by +0.13 to +0.16 dex/z, 3.7–4.1σ above RC100.** The framework is flat at 1.6σ. No halo knob removes the rise, because it comes from how ΛCDM halos evolve with redshift.
- **Framework residuals** show no trend with g_bar (Spearman p = 0.29), so there is no sign of a wrong kernel at z ~ 1–2.

## L332 — the independent replication on KMOS3D: it did not happen, and L323's trend becomes conditional

`L332_kmos3d_trend_replication.py` (4/5; the fifth is the pre-declared T1, shown as FAIL; `MUTATE` replaces v_obs with the ΛCDM-NFW prediction, K1 and K2 fail, rc = 1). The data are Übler+2017 v_circ,max for 117 galaxies, cross-matched uniquely to the KMOS3D catalogue's H-band R_e. 93 of them are not in RC100.

- **The pre-declared replication failed.** Every model's residuals fall with z, the framework included: −0.070 to −0.084 dex/z (5σ), against ΛCDM's −0.094 to −0.106.
- **The cause is common-mode (K1).** Newtonian baryons alone fall at −0.11 dex/z. At z ≈ 2.3, 27–54% of galaxies (depending on geometry) rotate *slower than their own Newtonian baryons*; at z ≈ 0.9 the figure is 2–11% (Fisher p ≤ 3×10⁻⁴). Übler's gas-to-star ratio comes from scaling relations and rises from 0.46 to 1.19. No model that adds gravity can fit those galaxies.
- **KMOS3D cannot decide the question (K2).** The framework and ΛCDM predicted trends differ by ≤ 0.031 dex/z, while the data sit ≥ 0.068 dex/z off both. L323's inverted-a₀ statistic does "replicate" at 4.4σ, but it drops 50% of the z > 1.9 galaxies and only 10% at z < 1.2, so it is conditioned on the outcome and is **not** quoted.
- **R1: L323's trend is calibration-conditional.** A z-tilt of β = −0.05 dex/z in the baryonic masses, a factor 1.25 end to end over z = 0.6–2.5, brings ΛCDM's least-rising cell within 2σ of RC100. At β = −0.10 the framework is 2.7σ off. One galaxy sitting exactly at the inversion's f_DM = 0.02 edge moves RC100's slope by 0.41σ. KMOS3D shows the high-z inputs can carry a z-dependent baryon error, and its sign (baryons over-estimated at high z) moves RC100's data *toward* ΛCDM, if RC100's fitted masses share it.

**Standing:** L323's result survives every halo knob but not a baryon-calibration tilt of ~0.05–0.1 dex/z. It should be quoted as *conditional on the high-z baryonic-mass calibration*. What would decide it is high-z dark fractions from kinematics with per-galaxy gas masses (CO or dust), not scaling relations.
