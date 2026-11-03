# KT4_chi_force_coefficient: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-02: "derive kappa". κ = 1/2 FITTED. Footings never pooled, and none is used. Not theory closed. No cold component, no particle. **Not blind:** the algebra below was worked by hand first and the target is known.

## Reframing of KT3
Normalise the vacuum as ordinary vacuum energy, unit coefficient: L = -(1 - chi^2) g^2/(8 pi G) - rho c^2 [1 + alpha u(chi)], u' = (1-chi)^2/chi. **Added hypothesis:** the constant is -rho c^2, as for any vacuum. Then the free quantity is alpha, the coefficient of chi's force. It isn't a zero mode, since it enters chi's field equation.

## Checks
- R1, sympy: chi eom gives chi = 1/(1 + bY), with b^2 = 1/(4 pi alpha) and kappa^2 = pi alpha. So kappa = 1/2 needs alpha = 1/(4 pi). pi-parity follows: rational kappa^2 needs a 1/pi in alpha.
- R2, frozen alpha list, graded against rho_DE window [0.227, 0.607] and exact 1/2: 1, 2, 1/2 (no pi); 1/(4 pi) (marked TARGET, not a route); 1/(8 pi) (derivative of a 3D Gaussian fluctuation free energy, -T m^3/(12 pi), named, needs T).
- R3, can classical physics give the 1/(4 pi)? Integrate out a massless mediator with Green's function 1/(4 pi r) against a uniform source in a ball of radius R. Sympy: does the 4 pi survive the volume integral? Also the massive case, source uniform everywhere.
- R4, coincidence value: G(0) regulated = -m/(4 pi) in 3D keeps the 1/(4 pi), but only for a fluctuating field. State what sets the amplitude: T or hbar. Check whether dimensions allow hbar to cancel, using T_dS = hbar H/(2 pi): state pi-weight after substitution.

## Labels
**EXACT CANDIDATE** only if a listed route, not the TARGET row, gives alpha = 1/(4 pi) from an equation with no tuned input. **NEEDS FLUCTUATIONS** if classical exchange cancels the 4 pi and only a fluctuating field keeps it. **NO ROUTE** otherwise. None of these is a derivation unless the first, and then CFG894 §3 and §6 are still owed.

MUTATE: 8 pi G -> 4 pi G in the field term; kappa^2 expected to double the alpha coefficient's inverse relation, i.e. kappa^2 = pi alpha / 2. Separate `_MUTATE`, exit 1. No download. Seconds.
