# Zero-broadening resonance-curve diagnostic

Prior turn established stable frequency but unresolved linewidth. At fixed u=L², the continuum absorptive matrix is
 B_n(omega)=F pi² omega integral du sum_roots[T_r C_n C_n^T/|n partial_E Omega_r|],
 with n Omega_r(E,u)=omega. Using Tr=2pi/Omega at the root gives2pi³F integral du C_n C_n^T/|partial_E Omega_r|.

Use64/128 Gauss action data and PCHIP interpolation in E to locate all polynomial roots within the sampled E interval. Report excluded endpoint slivers explicitly; this first diagnostic is not a certified complete-support integral. Compare matrices and a fixed approximate mode projection; flag small resonance derivatives. No damping rate until real principal-value response, endpoint coverage, interpolation and u-quadrature convergence are established.

## Endpoint and direct-orbit repair

Endpoint completion is performed with circular-orbit limits and direct cutoff-energy orbits. An interpolated coefficient spot check failed despite close64/128 agreement; preserve that probe. Refine every bracketed resonance with direct orbit periods, evaluate its Fourier coefficients directly, and evaluate its energy derivative by centered differences. Check a subset with1024 versus2048 phase nodes and halved derivative step. PCHIP still supplies brackets; it is not a completeness proof for arbitrarily narrow additional root pairs.
