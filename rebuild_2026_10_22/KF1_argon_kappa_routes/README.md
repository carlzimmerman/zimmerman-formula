# KF1_argon_kappa_routes: NOTHING FORCED. R2 and R4 are door X7 again, R1 and R3 give no number

Criteria: `FROZEN_CRITERIA.md` (8f14af0da8), alone first, not blind. `AMENDMENT_A1.md` adds R4, which arrived mid-run. `kf1.py`, `kf1_r4.py`, `kf1.out`, `kf1_MUTATE.out`, `kf1_r4.out`. kappa = 1/2 FITTED. Footings never pooled. Not theory closed.

| Route | Label | Why |
|---|---|---|
| R1 field stress | NO NUMBER | Stops before any kappa |
| R2 Phi_H / L | VOID, MENU | 1/2, 1.447, 1.772 at the three lengths. Only the length with no field equation behind it gives 1/2 |
| R3 law's quadratic | NO NUMBER | Holds for every a0. Its high-g limit, excess a0, is the law's Solar System problem |
| R4 lambda dX/dr = X0 | VOID, TRADE | kappa = 1/(2 xi), no dependence on the kinetic prefactor |

- Uniform rho makes a horizon where 2GM/(c^2 r) = 1, at J = G rho r^2/c^2 = 3/(8 pi). The routes need J = 1, the forbidden premise of door X7.
- For the de Sitter quadratic potential the gradient at R is c^2/R, not Phi/R, so R2's step holds for 1/r potentials only. True gradient: kappa 2.894.
- Einstein's coupling 8 pi G to 4 pi G moves the horizon and leaves R2 at 1/2 (`kf1_MUTATE.out`): R2 never reads the field equation. Rules section 5: void.
- R2 gives 1/2 for any density, so it can't choose a footing.
- R4's 1/2 is the 2 in g_00, since X0 and dX/dr scale together with the prefactor. The kinetic term's 1/2 is not the source.

What is left, from all four: forcing kappa = 1/2 is the same as forcing xi = 1, a length exactly c/sqrt(G rho). No field equation in the record does that (CFG891).

## Argon's later reply, R5: kappa = sqrt(2/(3 pi)) = 0.4607, a0 = c H_DE / 2 pi. Not forced either
Hand algebra, not in the frozen tests. Argon's step is k T = hbar H / 2 pi, so a = c H / 2 pi. Unruh is k T = hbar a / (2 pi c), so equating the two temperatures cancels the 2 pi and gives a = c H. The 0.4607 needs the 2 pi kept by hand. It is the record's Z = 2 pi value, inside door X3, and today's data can't separate it from 1/2 (needs a0 to 2.8 %). The claim that any derivation must carry sqrt(pi) is stronger than the record, which has a pi-parity result for routes built from a0 and H only, and CFG891's R18, where pi cancels. Register K808, audit class, adds no trial.

## Argon's R6: U_pair = (1/2) G M rho r^2, mean of g = G rho r over [0, R0]. VOID
Hand algebra, not in the frozen tests. Doing the two-point integral over a uniform sphere gives g = (4 pi/3) G rho r, or (8 pi/3) G rho r with w = -1 active mass. So the pi returns with the d^3x' integral, and g = G rho r is written in, not obtained. With the real g, the same steps give c H / 2, kappa 1.447. The mean over [0, R] gives 1/2 by choice of average: the endpoint gives 1, the volume-weighted mean 3/4. R0 = c / sqrt(G rho) is xi = 1 again. Register K809.

## Argon's R7: u = r Phi, mass gap k^2 = G rho / c^2 "per steradian". VOID
Hand algebra, not in the frozen tests. The reduction is exact, and it gives u'' = 4 pi G rho r, so the 4 pi stays on the source. rho is a source there, not a mass term. A term rho u is a new coupling, and its coefficient is posited, which Argon states. That posit is xi = 1. The standard coefficient 4 pi G rho / c^2 gives kappa 1.772, already in T1. Step 1's g^2/(8 pi G) = rho c^2 gives kappa sqrt(8 pi) = 5.01 and isn't used in the result. Register K810.

## R8, Claude's own try: kappa^2 = 8 pi / F0. NO NUMBER
Hand algebra. The law's action has F = y^2 - 2y + 2 ln(1+y) + F0, rational coefficients and F0 free, so kappa = 1/2 needs F0 = 32 pi with nothing supplying it. Direction sums, boundary terms and a separate vacuum sector don't fix it. Register K811.

## R9, Argon's causal-diamond trace: kappa 1 or 0.7071. VOID, algebra error
A normalised average of a constant returns the constant, so the 4 pi in the source does not cancel. Done correctly the trace reading gives sqrt(4 pi) = 3.545, a miss. Its 1/2 at w = 0 is the c^2/4 it inserts, its F is wrong (dF/dt fails), and its d = 4 value of 0.7071 does not follow from its own general-d formula. Register K812.
