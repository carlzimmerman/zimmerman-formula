# CFG362: can inflation fix the cold fluid amount? (stochastic misalignment)

Criteria: `FROZEN_CRITERIA.md`, committed alone first in ece4d2f82.

**Verdict: CONDITIONAL-TESTABLE.** A long de Sitter phase erases the CFG288 wave field's start value and fixes the amount by the inflation Hubble rate H_I. The amount is relocated into H_I, not reduced: one new constant from outside the framework replaces one free amount. The cold MASS is still required.

| test | result |
|---|---|
| T0 | The moment equation reproduces <phi^2>_eq and N_rel to 6e-6. rho_c0/s0 = 4.37e-10 GeV. Window [2e-20, 2.78] eV, read from CFG360. |
| T1 | H_I = 1.9e-6 GeV (m = 2e-20 eV) up to 83 GeV (m = 2.78 eV); H_I ~ m^0.379 (3/8). g* x 2 moves H_I by only 4%. |
| T2 | Equilibration needs N_rel = 1e21 to 1e46 e-folds. That is inside the de Sitter entropy bound everywhere, by a factor 8.8e3 to 5e13. **The TCC conjecture (reported only) is violated by 1e19 to 1e44.** |
| T3 | Light field (m/H_I <= 3e-11), reheating possible (V^1/4 = 3e6 to 2e10 GeV) and onset before z = 1e5: all pass. Minimal coupling is declared, not tested. |
| T4 | Isocurvature P_S <= 3e-21, against the limit 8e-11: passes. |
| T5 | Predicted r = 6e-41 to 1e-25. Unobservable, so H_I cannot be measured independently. **Falsifier:** any primordial B-mode detection (r = 1e-3 means H_I = 7.8e12 GeV, 1e11 x above the window's top). It kills the *equilibrium* version for every fluid mass. A shorter inflation that never equilibrates goes back to a free amount. |
| T6 | The local amount is a random draw: 0.05 to 3.0 x the mean (5 to 95%). "Fixed" means fixed in distribution, to a factor ~60. |

Honest reading: this is the only route found so far that sets the amount by a dynamical mechanism. But it needs very low-scale inflation (H_I <= 100 GeV, which the framework does not supply) and an enormously long one, and it predicts nothing measurable except the absence of B-modes.

Run: `python3 cfg362_inflation_amount.py` (10/10, rc 0); `MUTATE=1 ...` (noise x10, T0a fails, 9/10, rc 1).
