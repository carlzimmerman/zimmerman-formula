# QX3: CMB-lensing shape and linear growth, mechanisms inside the action

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Rules: ../SWARM_BRIEF.md.
Lean: fable_independent_2026/lean_2026/QX3_dust_eos.lean (12 theorems, 0 sorry, standard axioms; MUTATE twin fails on its
4 declared false claims).

| Iteration | Mechanism | Label |
|---|---|---|
| (record) WG1-WG6 | the a0 law on the linear web, baryons-only start, every rule | FAIL (shape) |
| iter1 | AC2q's dark-energy clock (c_s^2 = 1) | FAIL, no-go: (k_J/k)^2 <= 0.0065 on graded scales |
| iter2 | v3s's K(Q) sector = n = 1 polytrope, k_J = mu_K | lensing shape PASS (chi^2 8.57) but no window: needs mu_K >= 4e4, galaxies need <= 79 |
| iter3 | every barotropic K(Q) (lambda_J ~ rho^beta) | FAIL: 35/2,501 members avoid galaxies and pass the forest, all fail growth (best Delta chi^2 92.6 vs 4) |

**Door labels.**
- CMB-lensing shape: FAIL for every mechanism tried in the action. A dust-like sector gets the shape right, and on its own
  it fits PR4 as well as FFP10 does. No sector whose clustering depends only on its own density can do that and also keep the
  law's galaxy pass.
- Linear growth: same verdict.
What is still untried is a sector whose Jeans scale is set by the local acceleration or environment, i.e. switched by the a0
law itself. That is a new term, not yet in the action.
