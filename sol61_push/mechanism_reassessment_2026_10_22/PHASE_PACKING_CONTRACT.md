# Phase-space occupation and global virial feasibility, before computation

For nonnegative collisionless f<=fmax, derive the minimal local total velocity second moment at fixed density by filling a velocity ball. This is a classical phase-space bound, not a fermion assumption. Combine it with the stationary finite spherical virial identity for the identified medium with stiffness:

 2T+(3gamma/2) integral rho² dV=integral rho r(gNb-R) dV.

This avoids the local-patch or isotropy assumptions of earlier damping comparisons. Boundary terms must vanish; do not apply to the infinite streaming construction. Reintegrate the four accepted fixed-mass equilibria from cold_limit_run with their recorded central potentials, and compare direct kinetic moments, force virial and the occupation lower bound. Use velocity-space normalization rho_hat=integral f dv and omit common4pi in spatial integrals. Then F=A/(16sqrt2 pi/15) for f=F Q_+.

Require relative virial residual<1e-5, kinetic energy above its packing bound, consistent reproduced mass within1e-5, and integral-grid refinement below1e-5. No primordial fmax is supplied, so do not invent an empirical exclusion or declare a selected equilibrium reachable. Preserve original scripts/evidence.
