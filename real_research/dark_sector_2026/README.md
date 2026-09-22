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

1. **On RC100 the framework alone beats ΛCDM on both the level and the trend of high-z dark fractions.** This depends on RC100's model-dependent f_DM and its uncontrolled selection, the same caveats that h16 records.
2. **The forest–RC100 pincer applies to any carrier.** The forest needs a cold component clustered in the intergalactic medium on 0.1–1 Mpc scales at z = 2–3. RC100 says galaxies at that same epoch carry no cold halo. Kicks remove matter from shallow wells first, so they deplete the intergalactic medium before galaxy halos, which is the wrong order. A carrier would have to be absent from galaxy halos while present in the intergalactic medium at z ≈ 2, and also present in clusters today: a switch that is non-monotonic in potential depth. The record has found no such switch (f22).

**Standing:** the Λ-triggered carrier passes the forest and S8 but is disfavoured at about 3σ by RC100. The structural conflict between closing the dark sector and the framework's flat-a₀(z) galaxies is now explicit.
