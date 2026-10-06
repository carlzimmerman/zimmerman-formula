# CFG357 — the heat filter vs Cassini's EFE quadrupole Q2 at kappa = 1/2

- **Criteria:** `FROZEN_CRITERIA.md` (f28b5216a), committed alone before any script.
- **Script:** `cfg357_heat_filter_q2.py` (~2 s). Main run 6/6, rc 0. `CFG357_MUTATE=1` (field at 10%): C1 fails, rc 1, as required.
- **Lean:** `cfg357_cassini_q2.lean`, 8 theorems, no sorry, rc 0.

## Bottom line
**kappa = 1/2 SURVIVES CASSINI inside the chassis, on both footings, over the whole decision window [0.030, 0.15] pc.**
The heat filter (L340 S1's Gaussian smoothing of the Sun at width xi) takes p58's +6.3 sigma (simple nu) / +8.7 sigma
(nu_mono) bare-QUMOND quadrupole down to +1.1 sigma (canonical) / +1.5 sigma (alt) at the declared floor and below
1 sigma for xi >= 0.033 pc. This is not a new floor: Cassini's 2-sigma edge sits at 0.027 / 0.028 pc, just under the
declared 0.030 pc, consistent with L340 S1 (which set the floor from the same quadrupole, with field 2.32e-10 and ceiling
5.2e-27; here 5.73e-27 at 0.031 pc with field 2.146e-10).

| xi (pc) | Q2 canonical (s^-2) | sigma | Q2 alt | sigma |
|---|---|---|---|---|
| unfiltered, simple nu | 2.195e-26 | +6.32 | — | — |
| unfiltered, nu_mono | 2.921e-26 | +8.74 | 3.205e-26 | +9.68 |
| 0.030 | 6.36e-27 | +1.12 | 7.50e-27 | +1.50 |
| 0.033 | 4.70e-27 | +0.57 | 5.52e-27 | +0.84 |
| 0.045 | 1.80e-27 | -0.40 | 2.11e-27 | -0.30 |
| 0.15 | 4.8e-29 | -0.98 | 5.6e-29 | -0.98 |

2-sigma pass for xi >= 0.0270 (canonical) / 0.0284 pc (alt); 3-sigma for xi >= 0.0248 / 0.0260 pc.

## Readings and caveats
- **Other Solar-System bounds in the same configuration.** L340 S1's Saturn-monopole floor (0.045 / 0.049 pc) is the
  binding Solar bound, so the effective lower edge of the window is there; Q2 at that edge is -0.40 / -0.30 sigma.
  The PPN/perihelion side (L340, CFG291: C-H sector filtered off at Solar wavenumbers, e^{-xi^2 k^2} with xi/AU ~ 1e4)
  is unaffected by this lane.
- **No new constraint on xi.** Q2 falls steeply (about xi^-4 near the floor), but its Cassini edge lies below the
  declared floor and below the monopole floor.
- **The external field matters.** The filtered field G_f = g_sun,filtered + g_Ne has a zero near r_0 ~ g_Ne xi^3 / GM
  (about 6000 AU at the floor). The MUTATE run at 10% field moves the zero inward, which raises Q2 at the floor to
  1.1e-25 (+35 sigma), and the 2-sigma edge moves up to 0.070 / 0.074 pc. So the pass depends on the Galactic field being
  near its observed value; it is not a large-margin pass at the floor.
- **Small xi is worse than no filter.** At xi = 1e-4 to 1e-3 pc, Q2 is about 1e-22 (the field zero sits close to
  the Sun). C3 (xi = 1e-6 pc equals unfiltered) passes only because r_0 is then below the inner grid radius (0.01 AU),
  so it is a weaker control than intended. The window results do not depend on rmin (C5).
- The published version of the bare-MOND tension is Desmond, Hees & Famaey 2024, MNRAS 530, 1781 (PROVISIONAL, from an
  abstract-level read only).
- Scope: a static QUMOND-type response with L340's filter and a point-mass Sun; the khronon sector is not in Q2.
  kappa = 1/2 is still fitted. Departures from the frozen text: C5, the crossing roots and the r_0 estimate were added
  after the first run. They are for reporting only and are not used in the decision.
