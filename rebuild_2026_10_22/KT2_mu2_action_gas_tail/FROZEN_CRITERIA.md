# KT2_mu2_action_gas_tail: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-02: asked for the action behind KT1's idea, the Solar System, and tail data. κ = 1/2 FITTED. Footings never pooled. Not theory closed. No cold component, no particle. **Not blind:** KT1's table, lane K, K247 (tail-cutoff fit), K252 (cutoff as a local field) and STANDING's heat-filter line are read, and I worked Part A by hand first.

## Part A: action, symbolic
Static field phi, g = |grad phi|, auxiliary scalar chi, constant b:

L = -(1/8 pi G) [ (1 - chi^n) g^2 + (s/b)^2 U_n(chi) ],  dU_n/dchi = n (1-chi)^2 chi^(n-3).

Sympy must confirm, for n = 1, 2, 3, 4:
- A1: varying chi gives chi = 1/(1 + b g/s);
- A2: varying phi gives mu = 1 - (1 + bY)^(-n), Y = g/s;
- A3: deep slope n b, so kappa = 1/(n b); tail exponent n;
- A4: U_2 = 2 ln chi - 4 chi + chi^2 + C, with a log only for n = 1 and n = 2;
- A5: scale check, kappa invariant under G, rho, c rescaling; output follows b;
- A6, budget: with F(0) - F(Y_c) = rho c^2 and F(g) -> g^2 normalised at Y_c, kappa^2 = pi / (ln(1 + bY_c) + 1/(1 + bY_c) - 1) at n = 2 with kappa = 1/(2b). Print Y_c at kappa = 1/2, and the Y_c range for the rho_DE window. This is K247's trade in closed form, not a selection.

**Stated outcome before running.** The action gives n from chi's portal power and the 2 as d(chi^2)/dchi. It doesn't give b. b = 1 is the amplitude of U, which is premise A in a new place: both sector terms carrying 1/(8 pi). If A1 to A6 hold, Part A's label is **TRADE: 2 explained given the portal, b not**. Any other result is reported as found.

## Part B: gas-weighted tail, SPARC
KT1's kernel, grid, bootstrap, seed, statistic and labels, on points with gas share of Vb^2 at least 0.5 at the stated Upsilon. A galaxy needs at least 3 such points. Rows: Upsilon x 1, x 0.8, x 1.25, both footings; primary is x 1. The selection stays fixed from x 1 across rows, so Upsilon doesn't change which points count. Print the point count, the count at Y >= 3 and at Y >= 10, and max Y.

Added label, checked first: **NO LEVERAGE** if fewer than 30 selected points have Y >= 3.

Controls: planted (2,2) and (2,4) on the selected points, MUTATE shuffled g_obs with outputs `_MUTATE`, exit 1 by design.

## Part C: Solar System, by reading only
Report what the record's heat filter does for Cassini (STANDING line 199 and its source) and whether chi with a gradient term gives that filter. No new number unless the record's own script can be rerun as it stands. Filter from a gradient term is a Yukawa kernel, not a Gaussian, so expect not identical; say which.

Register row after the result. No download. Single thread, under 1 GB, minutes.
