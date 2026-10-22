# A75 — MUTATIONS

Invoke with **either** `A75_MUTATE=<name> python3 a75_checks.py` or `python3 a75_checks.py --mutate <name>`.
Each mutation changes **one** input of the live parameter set, must make at least one named check FAIL,
and exits **1**. The captured runs are `a75_MUTATE_<name>.out`; the unmutated run is `a75.out` (24/24, exit 0).

**16 mutations, all exit 1. 24/24 checks are killed by at least one mutation — none had to be deleted.**

| # | name | the one input changed | exit | checks broken (measured value in the mutated run) |
|---|---|---|---|---|
| 1 | `occupancy` | drop site exclusion: `θ = z` (Maxwell–Boltzmann) instead of `z/(1+z)` | 1 | K1 `rel 5.46e-01`; K2 `rel 3.70e-01`; K4 `rel 5.94e+00`; K5 `F identity rel 1.42e+00`; K6 `C_mu` changes sign/magnitude |
| 2 | `drive_energy` | the drive enters as an energy, `z = e^{g/k_BT}`, not as an activity `g/a0` | 1 | K2 `rel 8.51e-01`; K3 `dθ/dT = −1.51e-04` (no longer 0); K6 `C_g = −1.2e-11 ≠ 0` |
| 3 | `fermi_nocouple` | two-level gate coupling `λ = 0` | 1 | K7 `dθ/dT = 0.0000` (the gate loses its temperature dependence) |
| 4 | `twopi_drop` | `λ_T = c/H` instead of `2πc/H` | 1 | K9 `ratio 3.1663e+08`; K12 `c²/λ_T rel 5.3e+00`; K23 `ratios 1.000000 / 39.478` |
| 5 | `temp_H0` | `T` uses `H0` instead of `H_Λ` | 1 | K9 `m_Pc²/kT 1.6451e+09`; K11 `a_sat 1.042205e-10`; K12 `a_U 6.5484e-10`; K13 `ratio 0.826917` |
| 6 | `eta_three` | `η = 3γ` instead of `η = γ` | 1 | K8 `λ_C 29.4245 pc` vs A56 `16.9883 pc` (rel 7.3e-01) |
| 7 | `disp_linear` | `ω = p` instead of `ω = (α/Q)^{1/2} p²` for the fifth mode | 1 | K14 `quad/closed 1.0e+00`; `log10 ratio −122.70` |
| 8 | `entropy_norm` | horizon entropy `S = A/(2l_P²)` instead of `A/(4l_P²)` | 1 | K16 `S_cell 1.0519e+105`; K17 `a0_ent 6.093964e-11` (rel 2.9e-01) |
| 9 | `mu_eps` | site binding energy tuned to `ε = −k_BT_dS` | 1 | K18 `g(μ=kT)/a0 = 1.000000`, `θ = 0.500000` (the route "works" only by this tuning) |
| 10 | `cell_one` | one gate for the whole horizon, `N_cells = 1` | 1 | K19 `q/a0 = 1.0000e+00` |
| 11 | `kappa_half` | force `a0 = c²√(Λ/32π)` (the `R = 4` closure) | 1 | K12 `rel 7.9e-02`; K13 `ratio 1.085402`; K17 `rel 7.9e-02`; K20 `R = 4.000000000` (in `{1,2,4}`); K21 `ratio 1.000000`; K23 `rel` |
| 12 | `law_const` | add a fixed acceleration `1e-12 m/s²` to `g_N` | 1 | K22 `rel 6.6e-02` (homogeneity broken) |
| 13 | `mP_offby2` | carrier mass `m_P → 2m_P` | 1 | K9 `m_Pc²/kT 3.9788e+09` vs `λ_T/λ_C 1.9894e+09` |
| 14 | `a0_slope_sign` | `da0/dT` has the other sign | 1 | K3b `fd/analytic rel 2.00e+00` |
| 15 | `premise_true` | **assert the premise**: `λ_T := λ_C` | 1 | K9 `ratio 1.0000e+00`; K10 `L*_req 0.000 Gpc`; K12 `c²/λ_T rel 2.0e+09` |
| 16 | `mP_tiny` | carrier mass `m_P → 10⁻¹⁰ m_P` (light enough to be populated) | 1 | K9 `m_Pc²/kT 1.9894e-01`; K15 `log10 n = +0.657`, `log10 ρ ratio −84.70` |

## Coverage — every check has teeth

| check | killed by |
|---|---|
| K1 | occupancy |
| K2 | occupancy, drive_energy |
| K3 | drive_energy |
| K3b | a0_slope_sign |
| K4 | occupancy |
| K5 | occupancy |
| K6 | occupancy, drive_energy |
| K7 | fermi_nocouple |
| K8 | eta_three |
| K9 | twopi_drop, temp_H0, mP_offby2, premise_true, mP_tiny |
| K10 | premise_true |
| K11 | temp_H0 |
| K12 | twopi_drop, temp_H0, kappa_half, premise_true |
| K13 | temp_H0, kappa_half |
| K14 | disp_linear |
| K15 | mP_tiny |
| K16 | entropy_norm |
| K17 | entropy_norm, kappa_half |
| K18 | mu_eps |
| K19 | cell_one |
| K20 | kappa_half |
| K21 | kappa_half |
| K22 | law_const |
| K23 | twopi_drop, kappa_half |

## Notes on the design

- Every mutation is a **physical** one-input change, not a sign flipped inside a check: dropping the site
  exclusion, using an energetic rather than an activity drive, decoupling the thermal gate, changing the
  thermal-wavelength convention, the horizon used for the temperature, the stiffness ratio `η/γ`, the
  dispersion of the fifth mode, the entropy normalisation, the site binding energy, the number of gates,
  the closure value of `a0`, the law's homogeneity, the carrier mass, the sign of `da0/dT`, and finally
  simply **asserting the premise** (`premise_true`).
- `premise_true` is the decisive one: if `λ_T = λ_C` were true, K9, K10 and K12 would all pass — they fail,
  which is the numerical statement that the action's carrier is not at its thermal wavelength.
- No check was deleted. Every one of the 24 fails under at least one recorded mutation, and each check
  compares two independently computed quantities (a symbolic identity against a finite difference, a
  closed form against a quadrature, an action-derived expression against a quoted external number).
