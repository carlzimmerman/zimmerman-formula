# Free boundary refinement after first scan

First run found seven equilibrium branches, two radially damped and five with
positive discrete radial eigenvalues. Boundary pressure is represented by the
outer cell pressure, so radius errors are first order and appreciable. Preserve
that scheme and its first evidence. Refine all found branches at96 and144 cells,
and the strong-gravity branch at192 cells. Use saved BVP radii as starting
points, not fitted radii. Do not call the scan exhaustive: two strong-gravity
scan points failed. Compare limiting branch signs and radius approach, avoid
precise continuum growth-rate claims where convergence remains incomplete.
Check analytic phase potential, mass-step leakage and wall work separately.
Float64, one thread,240seconds. Only this investigation; push qualified result.
