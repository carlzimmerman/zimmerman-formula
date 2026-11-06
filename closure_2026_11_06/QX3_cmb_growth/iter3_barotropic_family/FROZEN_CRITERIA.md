# QX3 iter3 frozen criteria (pre-planned mutation, run only if iter2 FAILs): every barotropic K(Q)

Frozen before any graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Rules: ../../SWARM_BRIEF.md.

## Mechanism class

Generalise K to any power, p = A (Q - 1)^n with n > 1. The dust is then barotropic, and its Jeans length depends on its own density:
lambda_J proportional to rho^beta, with beta = (2 - n)/(2 (n - 1)), derived and Lean-certified (exponent identity). n = 2 is iter2
(beta = 0). The class is swept to prove that no member passes. This is a class proof, not a fit: (beta, mu0) with
mu0 = k_J at the present cosmic mean dust density; beta in [-2, 2] (41 values), mu0 log-spaced 1e-1 to 1e5 Mpc^-1 (61 values).

## Gates (same data and lines as iter2)

- G2': the iter2 ODE with k_J(rho_d) = mu0 (rho_d/rho_d0)^(-beta), taken at the iter2 G1 worst-corner best fit, with amplitude
  refit. Pass if Delta chi^2 <= 4.
- G3': dust avoids capture if lambda_J = 2 pi / k_J, evaluated at the galaxy's turnaround density (5.55 x cosmic mean at
  z_c = 2), is at least the turnaround radius of a 10^11.5 Msun halo (cosmic-mean definition, framework-native background
  from iter2's corner). Pass if lambda_J >= r_ta.
- Lyman-alpha forest G4': clustering is needed down to 0.42 Mpc/h comoving at z = 3 (X22's number). Pass if
  2 pi / (a k_J) <= 0.42/h Mpc at z = 3, at the cosmic mean density.

## Label

- PASS if any (beta, mu0) passes G2', G3' and G4' together. Report it; it would then need its own full regrade.
- FAIL (class no-go on this grid) if none does. Report the map and the closest member.
- MUTATE: flip G3' to require lambda_J <= r_ta. Members must then pass G2'+G3'+G4' somewhere, or the sweep has no power.
