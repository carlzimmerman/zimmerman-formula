# CFG52 — is the a₀(z) test at z ≈ 2.5 possible with the data on disk? (feasibility, not a test of B)

Scripts: `feas.py` (inventory, counts, per-galaxy table `feas_per_galaxy.csv`, `feas_results.json`), `mock_bias.py`, `pooled.py`; outputs `.out`. Written by a delegated agent, re-run here from the repo (outputs identical). This lane is a feasibility count, not a hypothesis test, so it has no MUTATE control.

**Bottom line: the flat-a₀ against a₀ ∝ H(z) test at z ≈ 2.5 cannot be run on the repo's data.** At z ≥ 1.5 there is no clean object with g_bar < 0.3 a₀. This agrees with CFG1 O4's "0 of 2".

## Method and assumptions

Inventory of every high-z rotation-curve table in the repo (RC100 100, MSA-3D 30, KMOS3D 135, KROSS 381, MUSE-DARK II 95, a lensed/CO ledger 23). Baryons as an exact Freeman disc with R_d = R_e/1.68 (a point mass as the upper bound on g_bar); the same ν_mono; a₀ canonical; σ_V/V of 10% where the tables carry none; a 0.20-dex mass floor; the rival a₀·E(z) with Ω_m = 0.3138. Validation: the disc g_bar matches RC100's own (1 − f_DM) g_obs to −0.01 dex.

## Counts (canonical footing)

| set | g_bar < a₀ | g_bar < 0.3 a₀ | at z ≥ 1.5: g_bar < a₀ | at z ≥ 1.5: g_bar < 0.3 a₀ |
|---|---|---|---|---|
| RC100 | 26 | 4 | 9 | 1 (a bad row: GS4 01529 has g_obs = 7.5 a₀ against its own f_DM implying g_bar ≈ 6.7 a₀) |
| MSA-3D (with gas) | 19 | 4 | 3 | 0 (stars-only 3, but those are lower bounds on g_bar; with gas 0.54–0.60 a₀) |
| KMOS3D | 16 | 5 | 2 | 0 |
| KROSS | 106 | 15 | 0 | 0 |
| MUSE-DARK II | 74 | 43 | 0 (z ≤ 1.45) | 0 |

- The point-mass bracket leaves no z ≥ 1.5 object below 0.3 a₀.
- Of 242 galaxies with g_bar < a₀, only 16 have a prediction gap between the two laws above 1σ, and none above 2σ (the typical gap is 0.10–0.19 dex against σ ≈ 0.13–0.16).
- **Pooled, z ≥ 1.5 and g_bar < a₀ (N = 14):** ⟨Δ_flat⟩ = +0.135, ⟨Δ_rival⟩ = −0.037; with a correlated 0.2-dex mass calibration the significance is +1.0σ and −0.3σ. A mock with the flat law true and selection on noisy g_bar predicts a +0.03 to +0.11 dex bias, which absorbs most of it. No discrimination.
- **The deepest sample on disk, MUSE-DARK II at z ≈ 1.2 (N = 21, g_bar < 0.3 a₀):** both laws over-predict (flat −0.22, rival −0.35 dex), flat favoured by about 1σ, dominated by model-mediated gas (the sign matches the Jeanneau refit).

## What a decisive test needs

The gap is 0.23–0.27 dex in g_obs at g_bar/a₀ = 0.05–0.3. Two to four discs at z ≈ 2.5 with σ_V/V = 5–10% and independent mass errors of 0.1–0.2 dex would give 3σ (this matches the repo's "3 at ±0.10 or 4 at ±0.20"). A **correlated** 0.2-dex mass-scale systematic caps the significance near 2.3σ whatever N is, so the mass calibration must reach about 0.1 dex. Data kind: resolved 3D kinematics (JWST NIRSpec IFU) out to R ≳ 8–10 kpc, ALMA CO for measured gas, low lensing-magnification uncertainty, V/σ > 1.5, log M_bar ≲ 10.

Nothing here says the theory is closed.

## Referee corrections (09-28 audit of the lane READMEs against their outputs; appended, the text above is unchanged)
- 'No clean object at z >= 1.5 with g_bar < 0.3 a0' is the canonical footing: in the alt-footing table (feas.out) RC100 has 2 such objects (the second is zC 410041, z = 2.45, about 0.295 a0 alt). The typical prediction gap is 0.08-0.13 dex in the per-set medians, not 0.10-0.19.
