# CFG746: sealed hot-gas prediction for massive quiescent galaxies (cold energy retained in proportion to hot gas)

**SEALED 2026-10-13.** SHA-256 of `cfg746_predictions.json`:
`79140240f3317e2b7a44cc9ed687c2e186809036ad9c5453d35d2bff88b9f937` (`PREDICTIONS_HASH.txt`). Never edit these files; any change
goes in a new dated file. Predictions, not results: no SZ or X-ray profile data were read.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first.
- **Script:** `python3 cfg746_predict.py` reproduces the JSON byte for byte. `CFG746_MUTATE=1` exits 1 (k → 2k halves P1).
- **Settings:** κ = ½ FITTED; k from CFG745; the cold energy's mass is required; no particle species; not "theory closed".

| footing, f_hot,cl | M_hot(<100 kpc) | kT | Y D_A² [Mpc²] | L_X(0.5–2 keV), Z = 0.1 / 0.3 / 1 [erg/s] |
|---|---|---|---|---|
| canonical, 0.85 | 1.40e10 M☉ (0.22 M*) | 0.114 keV | 2.27e-10 | 2.6–8.2e38 / 0.7–2.2e39 / 2.4–7.1e39 |
| canonical, 0.95 | 1.56e10 M☉ (0.25 M*) | 0.115 keV | 2.56e-10 | 3.3–10e38 / 0.9–2.7e39 / 3.0–8.9e39 |
| alt, 0.85 | 1.08e10 M☉ (0.17 M*) | 0.119 keV | 1.83e-10 | 1.6–4.9e38 / 0.4–1.3e39 / 1.4–4.2e39 |
| alt, 0.95 | 1.20e10 M☉ (0.19 M*) | 0.120 keV | 2.06e-10 | 2.0–6.1e38 / 0.5–1.6e39 / 1.8–5.3e39 |

Galaxies at log M* = 10.8, all gas inside 100 kpc, isothermal. V_c(100 kpc) is 191–196 km/s, including the cold energy C = k M_hot.

**Reading.**
- The predicted gas is cool (~0.11–0.12 keV, the virial temperature in this potential) and faint in X-rays: 10³⁸·²–10³⁹·⁹ erg/s,
  below the eROSITA stack's 1.1 × 10⁴⁰. Consistent, but not a test, since that stack's detection can include other sources.
- The decisive measurement is a **mass**: SZ (Y D_A² ≈ 2 × 10⁻¹⁰ Mpc²) or X-ray mass profiles. **Falsifier:** a measured
  M_hot(<100 kpc) for log M* 10.5–11.0 quiescent galaxies below half the tabled values kills the selector as the explanation
  of the early-type shortfall.

**Disclosure.** The first run omitted the cold-energy term in V_c, contrary to frozen P2. It was fixed before the seal, and no
data were read in between. The fix raised kT by about 6%; M_hot is unchanged.
