# DF3_fluid_next_gates AMENDMENT A1: before any graded number. Only the solver's known-answer controls had run

Corrections found while planning the code. kappa = 1/2 FITTED. Not theory closed.

1. **TOV control was misstated.** M_max scales as K^(3/4), not K^(3/2): at the top of the equation of state GM/(R c^2) is fixed, rho ~ K^(-3/2), R ~ K^(3/4). Line: K x 16 gives M_max x 8 within 3 %.
2. **TOV equation of state, made definite.** The full Fermi-gas P(x), rho_e(x) with g = 2, matched to the cell's K in its non-relativistic limit, in place of a hard cap at c/sqrt(3). It is Gamma 5/3 at low density and P = rho_e c^2/3 at high density, so it is the smooth form of the cap. Used as an equation of state only; no particle is adopted. Known answer added: m = neutron mass gives M_OV 0.71 Msun within 3 %.
3. **MUTATE's X-COP bite.** By hand before running: self-gravity x 4 can't move X-COP by 0.05 in a no-equilibrium cell or a point-mass cell, so that part would have no teeth. Replaced: fair share x 0.1 at (5/3, 100) must move X-COP's mean by over 0.05. Self-gravity x 4 stays on the Lane-Emden line. The Bullet flip is made definite: the sign of the parcel shift is reversed.
4. **Milky Way lines.** X5's stored law cells carry V_c(R0), K_z(R) and K_z(R0), not Ou's outer curve. So D4 grades V_c, K_z chi2, K_z(R0) on the 175 cells, on each footing, adding the fluid's field to those law values under reading N. Ou's chi2 reads NOT COMPUTED. McMillan's row carries V_c and K_z(R0) only. Under S, MW reads NOT COMPUTED, since the law's value would have to be re-solved.
5. **Bullet under S:** NOT COMPUTED, since S isn't additive on the law's map. S gets mass and Mach rows only.
