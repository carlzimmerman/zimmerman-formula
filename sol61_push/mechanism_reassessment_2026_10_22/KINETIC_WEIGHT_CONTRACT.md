# Kinetic derivative weighting and forced response

Prior turn produced progress: verified orbit coupling to a dilation trial. That mass-weighted statistic is not a damping rate. For f=F[Q]+, Q=-E-L²/2 (ra1, cutoff0), derivative at fixed L is f_E=-F. Thus sampling with f requires weight F/f=1/Q.

For a prescribed radial potential phi, the paired-harmonic susceptibility is
 Pi(z)=-M mean[sum_n 2(n Omega)^2 |phi_n|²/{Q[(n Omega)^2-z²]}].
Test A10000 with1024/4096 deterministic samples, n1..16, Fourier meshes1024/2048. Evaluate z=.827760+i epsilon, epsilon=.1,.03,.01. These are regularized forced responses, not self-consistent eigenvalues or a zero-width Landau limit. Check the high-frequency sum rule M mean[sum2(n Omega)^2 |phi_n|²/Q] = integral r²rho(phi')²dr, allowing sampled error but reporting it. Do not extrapolate a decay rate or reinterpret epsilon as physical damping.
