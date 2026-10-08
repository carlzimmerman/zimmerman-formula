# CFG433 — T13's phantom dispersion vs the Milky Way satellites

**Verdict (frozen rule): NON-DIAGNOSTIC. The measured number leans high: TENSION at +2.9 sigma (canonical)
and +2.5 sigma (alt). The satellites want more circular speed than the baryons-alone phantom gives.**

This is the proper version of the falsifier T13 registered: "MW satellites probe 110-125 km/s vs
132.8/139.2". We ran a spherical Jeans analysis on the Fritz et al. 2018 Gaia DR2 3D motions
(A&A 619, A103, Table 2). Anisotropy comes from the satellites' own radial and tangential velocities,
and the tracer slope gamma comes from their own radii. The result is compared with the kernel
circular speed from MW baryons alone. Nothing was fitted.

## What was used

- Prediction: V_pred^2 = r g_N nu(g_N/a0) with nu = 1/(1-exp(-sqrt y)) and point-mass baryons.
  M_b = 6.0e10 Msun is the record's MW value (FG001 / CFG42 / CFG286 `MW_MB`). The variant
  7.3e10 is the census-high value (CFG286). T13 itself used 1e11, which is not the record's MW value.
- Estimator: V_c^2 = <v_t^2> + (gamma - 2)<v_r^2>. This is the Jeans / 3D tracer estimator in a
  flat potential. It is appropriate here because V_pred changes by only 7 % over 30-300 kpc (C3).
- Primary sample: 30-300 kpc with tangential error <= 50 km/s, which leaves 17 satellites.
  gamma_ML = 3.11 from all 31 objects in the window. beta = -0.44 (tangentially biased).

## Numbers (primary)

| | canonical (a0 9.36e-11) | alt (a0 1.13e-10) |
|---|---|---|
| V_c,obs (r_med 78 kpc) | 231.9 +- 21.4 km/s | same |
| V_pred, M_b 6.0e10 | 170.3 km/s | 178.0 km/s |
| D = (obs - pred)/sigma | **+2.87** | **+2.51** |
| D with M_b 7.3e10 | +2.45 | +2.07 |
| D with T13's 1e11 (reference) | +1.71 | +1.30 |
| V_obs / V_pred | 1.36 | 1.30 |

Declared variants, canonical / alt D: no quality cut +2.18/+1.79; e_t <= 100 +2.53/+2.18;
no LMC candidates +1.71/+1.36; no Leo I +2.91/+2.56; inner 30-100 kpc +2.29/+2.09;
outer 100-300 kpc (4 objects) +0.44/+0.15; gamma = 2 +1.80/+1.27; gamma = 3 +3.36/+2.91.
Every variant has the same sign (D > 0). None reaches the robust-FAIL bar.

The naive comparison T13 quoted does not reproduce. The satellites' 1D rms dispersion is
sqrt(<v3D^2>/3) = **131.9 km/s**. With the record's M_b of 6e10, T13's sigma_ph = (G M_b a0)^1/4/sqrt2
is 116.8 (canonical) / 122.5 (alt) km/s. The satellites therefore sit ABOVE the prediction. They do
not sit 10 km/s below it. They match T13's numbers (132.8/139.2) only because T13 used M_b = 1e11.

## Controls and MUTATE

- C1: the table parses to 39 rows, and V3D agrees with sqrt(Vrad^2 + Vtan^2) in 39 of 39. PASS.
- C2: 300 mocks in the exact kernel potential with the data's errors and sample structure. Bias
  -0.09 %, scatter 10 %, 1-sigma coverage 0.65. PASS.
- C3: V_pred is near-flat over 30-300 kpc, spread 7.1 % (canonical) / 6.5 % (alt). PASS.
- M2: scaling the real velocities x1.35 flips the verdict to FAIL (D +4.6 / +4.4). Scaling x1/1.35
  flips it to PASS (D -0.4 / -0.9). The pipeline therefore responds in both directions.
- **M1 power check FAILED.** With a planted excess of 35 % in V_c, only 29 of 100 mocks reach D > 3.
  The criteria required 80 of 100. The unmodified mocks pass in 96 of 100. With 17 satellites, a
  ~10 % sigma cannot turn a 35 % excess into a 3-sigma FAIL. The data's own excess is about that
  size, 1.30-1.36x. Under the frozen rule this makes the test **NON-DIAGNOSTIC**. That status is
  kept as it is and is not upgraded.
- M3 (informational): forcing beta = 0 gives 232.8 km/s, 0.05 sigma from the primary. With
  gamma near 3, the Jeans combination (gamma - 2 beta)/(3 - 2 beta) is near 1, so anisotropy barely
  moves V_c for this sample. The tracer slope gamma moves it: gamma = 2 gives 196.9 km/s.

## Plain reading

The Milky Way satellites, analysed properly, carry more circular speed (about 200-230 km/s at
~80 kpc) than the deep-MOND phantom of 6e10 Msun of baryons supplies (170-178 km/s). The excess is
2.5-2.9 sigma, and every declared variant gives the same sign. It is not a FAIL, and the sample has
too little power to deliver one at this size. The direction matters. An excess counts against
T13's "phantom alone sets the halo". It does not count against B as a whole, because B carries a
cold fluid that clumps like CDM (CFG344) and can supply extra dynamical mass. A deficit would have
been unrepairable, and no deficit is seen.

## Caveats

- Satellites are a sparse tracer with incompleteness bias: ultra-faints are found preferentially
  nearby, which inflates gamma. gamma is the dominant systematic, and the 2-3 bracket is the
  declared handle on it.
- Fritz et al. note that more satellites sit near pericentre than near apocentre. The population
  is therefore not in phase-mixed equilibrium, which biases kinetic energy and so V_c high.
- LMC-associated satellites add tangential velocity. Removing them gives D +1.7 / +1.4.
- The 7.3e10 baryon variant gives D +2.45 / +2.07. The MW's hot circumgalactic gas is not in the
  record's baryon model. Adding it would raise V_pred.
- Implementation detail added after the first run, disclosed: the first version of the C2/M1 mocks
  used all 31 window objects as kinematic tracers. They were changed to 31 radii with 17 kinematic
  objects, which is the "primary sample's size" of the frozen text. The real-data numbers were
  unchanged. C2 passed in both versions (bias -1.45 % before, -0.09 % after).
- This tests neither the mass law (SPARC) nor a0 or kappa. kappa = 1/2 stays FITTED.

## Files

`cfg433_satellite_jeans.py` (`CFG433_MUTATE=1` for the MUTATE run), `cfg433_satellite_jeans.out`,
`cfg433_satellite_jeans_MUTATE.out`, `cfg433_results*.json`, `FROZEN_CRITERIA.md`. The data is in
`../_external_data/cfg433_work/` (FETCH_LOG.md there; not committed). CDS has no catalogue for
J/A+A/619/A103, so Table 2 was read from the arXiv source.
