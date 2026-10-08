# CFG437: BX442 (z = 2.18 spiral) from published numbers. NOT DIAGNOSTIC: the pressure-support reading flips the answer

The criteria were committed first (a back-of-envelope estimate made in chat beforehand is disclosed there). The script is `cfg437_bx442.py`. The inputs are the Law et al. 2012 supplementary table: M* 6e10, M_gas 2e10 (star-formation-law inversion), V_rot 234 (+49/−29) km/s at 8 kpc, σ 71 km/s.

| reading | implied a₀ median (16–84%) | canonical | alt |
|---|---|---|---|
| A: V_c = V_rot | 1.27e-10 (3.9e-11 – 3.6e-10) | not diagnostic | favours flat |
| B: asymmetric-drift V_c | 3.06e-10 (1.3e-10 – 6.7e-10) | favours H(z) | favours H(z) |

The predictions are flat 9.4e-11 / 1.13e-10 and the H(z) rival 3.1e-10 / 3.7e-10.

**Verdict.** NOT DIAGNOSTIC on both footings.
- Whether the 71 km/s dispersion is counted as support moves the implied a₀ by about 2.4×, which spans both predictions. That is the CFG270 pressure-term lesson again.
- Of the reading-A draws, 30% have g_obs ≤ g_N, i.e. no root.
- There is one galaxy, and its gas mass is inverted from star formation, so it can never establish evolution.
- MUTATE (V × 1.81): reading B moves to 3e-9, so the estimator responds.

The Keck archive inventory (OSIRIS raw frames, no reduced cubes) is in ../_external_data/cfg437_work/osiris_programs.csv. A raw re-reduction would not remove this systematic.
