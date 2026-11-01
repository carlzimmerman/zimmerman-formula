# CL5_agn_gas_cycles: gas cycles NOT REACHED AT CEILING; softening to the limits would not close the puzzle either

Criteria: `FROZEN_CRITERIA.md` (3f6005c165), amendment A1 (before any script or number).

## Part A: black-hole-capped gas cycles, gravity only (frozen verdict: NOT REACHED AT CEILING)
R at 10 Gyr, need ≤ 0.846 (1e14), ≤ 0.809 (1e13).

| run | M_f (cap) | share of E_AGN | R vs frozen STATIC | R vs same-gas control (post-result) |
|---|---|---|---|---|
| 1e14, N 10, ε_c 1 | 0.0283 (gas) | 0.95 | 1.025 | 0.917 |
| 1e14, N 10, ε_c 0.3 | 0.0090 (energy) | 0.30 | 1.011 | |
| 1e14, N 10, ε_c 0.05 | 0.0015 (energy) | 0.05 | 1.007 | |
| 1e14, N 3, ε_c 1 | 0.0283 (gas) | 0.29 | 1.086 | |
| 1e14, N 40, ε_c 1 | 0.0075 (energy) | 1.00 | 1.000 | |
| 1e14, a_f 0.02, ε_c 1 | 0.0076 (gas) | 0.23 | 1.029 | 0.951 |
| 1e14, BOUND (all gas, uncapped) | 0.10 | 2.98 | 0.918 | |
| 1e13, N 10, ε_c 1 | 0.0283 (gas) | 0.21 | 1.026 | 0.910 |
| 1e13, N 10, ε_c 0.05 | 0.0069 (energy) | 0.05 | 1.018 | |

K1, K2 (≤ 2.7e-5), K3, monotonic MUTATE and BOUND sensitivity pass.

**A bias in the frozen control, found after the result.** The frozen STATIC has no moved gas at a_f, but every cycled run does, so that
extra central mass contracts the halo (control/STATIC 1.08–1.13). This makes the frozen R pessimistic. `cl5_control.py` puts the same M_f at a_f with no bursts.
Against it the ceiling runs end at R 0.91–0.95: about 8 % softening, still short of the 15–19 % needed. There is no build-up over time: the ratio swings
with cycle phase (1e14: 0.856 0.947 1.000 0.927 0.844 0.978 1.000 0.917 at 1.25 Gyr steps), touching 0.844 only mid-cycle. The verdict is unchanged. The control is reported, not graded.

**Why it stops short.** Net work into the cold component at the ceiling is 7e-3 E_unit, about a quarter of what CL4 requires (0.026 at 1e14, 0.036 at 1e13). The gas available in the core
caps the moved mass well below the fluctuation that worked at galaxy scale (M_f/M_cold(<a_f) is small, and the rest of the gas sits too far out).

## Part B: stipulated η 21.2 / 14.3 / 14.3 (not a prediction)
| f★ | canonical | alt |
|---|---|---|
| 0.034 | **TARGET PASSES** (Υ 0.52, rms 0.0687, groups +1.66) | BREAKS: SPARC line (Υ 0.44; X78: the a₀ law's) |
| 0.0615 | BREAKS: G-IN-Mall OVER | BREAKS: SPARC line, G-IN-Mall OVER |

K4 (CE1 reproduced, |d| 0) and MUTATE (Υ +0.040) pass.

Reported, canonical, LS1 bins (median Υ, ΔV at Υ 0.50): V_flat 150–200 0.55, −6.4; **200–250 0.61, −18.6**; 250–400 0.77, −57.9.

**So softening clusters alone is not the answer.** With 1e12 at SPARC's limit (η 21.2) the Milky Way analogs miss by −18.6 km/s, worse than −7.8 at η 25.9 and better than −34.7 at c_f 4. The population line wants η(1e12) ≤ 21.2; the analogs want it higher. The tension is inside SPARC, at 1e12, and is not only galaxies against clusters.

## Limits
Prescribed histories, spherical, one seed, halo formed at t = 0, no gas physics simulated, only one return-time form. Round gas numbers (0.10, a_g 0.20) and the AGN inputs are PROVISIONAL. ε_c 0.05 is from memory. R is
measured at x_c ≈ 0.017 and applied to the x_c 0.001 values, with η scatter of about ±1 %. Cluster η is ng 48 until A4 finishes. Other cluster mechanisms (non-spherical mergers, an unknown coupling) are not tested. Not simulated: a gas-rich proto-cluster past.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Cold dark energy is a gravitating field component, never a particle.
