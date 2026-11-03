# KT23_ladder_distance_kappa: 1/2 CONSISTENT on both footings, but too loose to pin kappa. With no H0 in any distance (19 galaxies, TRGB / Cepheid / SN), the board law's outer rotation curves give a0 = 1.12e-10, so kappa 0.60 +- 0.14 (canonical) and 0.50 +- 0.12 (alt); it can't tell 1/2 from 0.482

Criteria: `FROZEN_CRITERIA.md`, alone first, confirmed landed. `kt23.py`, `kt23.out`, `kt23.json`, `kt23_MUTATE.out`, `kt23_MUTATE.json`. No download. κ = 1/2 FITTED in the record, not moved here. Not theory closed. Register K834. 16 s.

kappa_meas = 1/2 x a0_meas / a0_footing. Raw a0 is the footing-free number.

| sample | n | a0 (m/s^2) | sigma_ln (stat / Upsilon / gas / ladder) | kappa canonical | kappa alt |
|---|---|---|---|---|---|
| **primary, simple nu** | 19 | **1.125e-10** | 0.231 (0.145 / 0.166 / 0.021 / 0.067) | **0.60 +- 0.14** (z +0.72) | **0.50 +- 0.12** (z -0.03) |
| beside: standard nu | 19 | 1.402e-10 | 0.227 | 0.75 +- 0.17 | 0.62 +- 0.14 |
| beside: + Ursa Major | 32 | 0.971e-10 | 0.252 | 0.52 +- 0.13 | 0.43 +- 0.11 |
| beside: Hubble flow at H0 73 | 47 | 1.092e-10 | 0.375 | 0.58 +- 0.22 | 0.48 +- 0.18 |

Depth: y_out median 0.046 (0.015-0.20). Weighted mean of the primary: 1.20e-10.

## Reading
- **1/2 is consistent, and so is almost everything near it.** The error is 23 percent in a0, and kappa scales as a0, so 23 percent in kappa. 0.482 sits 0.1-0.9 sigma away. This doesn't pin kappa.
- **The H0-free number lands on the alt footing.** a0 1.12e-10 vs alt 1.13e-10; canonical's 9.36e-11 needs kappa 0.60 here. That isn't significant (0.7 sigma), but it's the direction.
- **The interpolating function moves kappa by 25 percent** (simple 0.60 / 0.50 vs standard 0.75 / 0.62) even at y_out 0.05. The deep limit isn't reached on SPARC, so "kappa" stays conditional on the board law's nu.
- **What limits it:** galaxy-to-galaxy scatter (stat 0.145; the 19 a0_i span 4.5e-11 to 3.1e-10) and mass-to-light (0.166). More ladder distances alone won't fix the second. The route to a sharp kappa is deep, gas-dominated dwarfs with TRGB distances, where Upsilon barely enters.
- The record's 0.450 +- 0.073 used H0 = 67.4 for distances; this lane's H0-free primary doesn't reproduce its smaller error.

## Checks
C1 residual at a0_i 6e-13. C2 injection 1e-10 recovered to 2.5e-13. C3 19 galaxies (>= 12). Exit 0. MUTATE (g_obs = g_bar): 19/19 have no a0 solution, exit 1.
