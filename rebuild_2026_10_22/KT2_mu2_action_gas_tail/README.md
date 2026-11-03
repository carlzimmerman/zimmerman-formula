# KT2_mu2_action_gas_tail: TRADE, NO LEVERAGE. An exact action gives mu_n and explains the 2 given a chi^2 portal, but leaves the factor b = 1. Gas-dominated SPARC points never reach Y >= 3

Criteria: `FROZEN_CRITERIA.md` (2d6860f198), alone first, confirmed landed before the run, **not blind**. `kt2.py`, `kt2.out`, `kt2.json`, `kt2_MUTATE.out`, `kt2_MUTATE.json`. No download. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Register K816. Exit 2, because the planted control fails.

## Part A: action. All sympy checks pass
L = -(1/8 pi G) [ (1 - chi^n) g^2 + (s/b)^2 U_n(chi) ],  dU_n/dchi = n (1-chi)^2 chi^(n-3).

Varying chi gives chi = 1/(1 + b g/s). Varying phi gives mu = 1 - (1 + bY)^(-n). Slope n b, tail exponent n, kappa = 1/(n b). For n = 2, U_2 = 2 ln chi - 4 chi + chi^2 + C.

- **What it explains.** Slope equals tail because both come from the portal power chi^n. Deep in MOND, chi -> 1 and 1 - chi^2 -> 2(1 - chi), so the 2 is d(chi^2)/dchi. A quadratic portal is the lowest power even in chi, which is a reason to prefer n = 2. It isn't forced: U contains a term odd in chi, so chi -> -chi isn't a symmetry of the action.
- **What it doesn't.** kappa = 1/(2b). b = 1 is the amplitude of U: the term is c^2 rho U / (8 pi b^2). That needs the vacuum term to carry the same 1/(8 pi) as the field term, which is premise A in a new place. **The target moved to b; it isn't derived.** chi is non-dynamical here and no field equation fixes it beyond the elimination above.
- **Budget, A6.** With F(0) - F(Y_c) = rho c^2: kappa^2 = pi / (ln(1 + bY_c) + 1/(1 + bY_c) - 1). This is K247's trade in closed form. kappa = 1/2 needs Y_c = 10^5.89, g_c = 1.46e-4 m/s^2; the rho_DE window needs Y_c from 10^4.22 to 10^26.57. Nothing here sets Y_c, so it swaps kappa for a cutoff.

Label: **TRADE: 2 explained given the portal, b not**, as stated before running.

## Part B: gas tail. NO LEVERAGE
Gas share >= 0.5: 54 galaxies, 437 points, **0 at Y >= 3, max Y 0.3** on rho_DE. Gas-dominated points sit at low acceleration, so the high-g tail is always measured with stars in it. SPARC can't supply star-free tail data with this selection, whatever the fit does.

Slope on these points, rho_DE: n 68 percent 1.8 to 2.3 at Upsilon as stated; 1.7 to 2.1 at x 0.8; 2.0 to 2.5 at x 1.25. rho_crit: 2.2 to 2.7, 2.0 to 2.5, 2.4 to 3.0. As stated, that's kappa 0.43 to 0.56 on rho_DE and 0.37 to 0.45 on rho_crit, 68 percent, without an Upsilon error. A description, not a forcing, and s uses H0 67.4 and Omega_L 0.685 as in L232.

**Controls.** Planted (2,2) and (2,4) both FAIL: p comes back at 6.5 to 8 regardless, so the fit has no tail information, and by the criteria that reads NO VERDICT on p. MUTATE FAILED its threshold: shuffled rms 0.2106 against 0.1555, a rise of 0.055, not 0.1, as this narrow range of g has less spread to shuffle. NO LEVERAGE doesn't rest on either: it's a point count.

## Part C: Solar System, reading only
The record already has a mechanism. L340: the kernel acts on the heat-filtered field, the Sun's high-y field never reaches it, and the tail vanishes at xi >= 0.03 pc. By my arithmetic, the Sun's g at 0.03 pc is about 1.5e-10 m/s^2, Y about 1. That answers "stiffening hides the tail": around a star the filtered field never gets high enough to enter the tail. I did not rerun it, and it doesn't address the quadrupole for mu_2 specifically.

- A gradient term for chi gives a Yukawa kernel, (1 - l^2 Laplacian)^-1, not L340's Gaussian. So this action doesn't derive the filter. xi stays a floor, not an output.
- **The filter works against A6.** If filtered fields stay well below Y_c, the tail that the budget integrates to 10^5.89 is never realised. Both can hold only if the budget is a statement about the function alone.

## Limits
One family. chi is added by hand. Galaxy-equal weights, no point errors or per-galaxy Upsilon. L340 is on a construction the record has since moved on from, read here as a mechanism only.
