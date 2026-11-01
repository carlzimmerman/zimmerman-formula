# Necessary energetic screen of the three completed dilute endpoints

Apply the already-reviewed fluid and canonical-kinetic radial Hessians to
exactly the three full endpoints obtained by the fixed dilute continuation:
(.2,weak_diffuse), (.2,strong_compact), (.4,weak_diffuse), epsilon=.01.
No parameters or forcing profiles change and no failed endpoint is replaced.

The imposed baryonic potential contributes integral rho Phi_b to the energy.
It is linear in Eulerian rho, so has no additional Eulerian Hessian term.
At the new constrained equilibrium the first variation of the *total* energy
is constant mu; second-order density-path terms cancel at fixed dark mass.
The self-gravity Hessian still uses dark density only. Consequently the same
Q and canonical shear expressions apply, evaluated on the new background.
The old zero-baryon homology identity is not reused.

Reconstruct each endpoint through the exact frozen .025 continuation and
verify it against its saved observables. Use the same 12 displacement modes,
scalar tolerance3e-7, 256/512 quadrature, positivity/reciprocity/mass checks,
negative margin threshold and refinement gates. Report Rayleigh values only.
Positive tested values do not prove continuum or kinetic stability, formation,
or that the selected branch is dynamically reached. Static contraction is
not an observed galaxy prediction. Same resource caps as CONTRACT.md.
