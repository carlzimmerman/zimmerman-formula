# IO-5: settle the surviving relaxed boundary, then refine

IO-4 Rj8b eta30 at time3000 retains qinner1, qouter~0 and parent-level
force error, but phase speed .000293 is not stationary. Continue its actual
stored endpoint without changing parameters to100000 additional internal
units. If it remains finite, repeat on n512 by interpolation of the settled
n256 phase, duration100000. No reset to an imposed law-phase profile.

Record stationarity, full phase Hessian, outermost q=.5 radius, mass fractions,
T force, E+Q and phase range. A negative eigenvalue or material drift prevents
calling it stable. The density/baryons remain fixed; even a finite-grid pass
is only a conditional phase-persistence/inner-force feasibility result.
