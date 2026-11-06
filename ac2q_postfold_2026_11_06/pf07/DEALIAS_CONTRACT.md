# PF07 aliasing hypothesis and discriminating test

The adapted homogeneous mode Jacobian has the expected imaginary principal
frequencies (exploratory diagnose_modes.py), yet finite-amplitude evolution
excites near-cutoff modes. In the curvature-subtracted RHS, continuum product
rules cancel second derivatives of the lapse. Collocation product rules fail
at the spectral cutoff on an inhomogeneous background. Hypothesis: aliasing
of this cancellation causes spurious high-frequency growth.

Compare a finite-difference Jacobian of the adapted constrained RHS with and
without zero-padding states to three times the odd grid size before evaluating
nonlinear products, constraints and derivatives; project RHS Fourier coefficients
back. This is spectral Galerkin evaluation, not physical viscosity. Record
largest real eigenvalue for n=15,31. Step sizes for derivatives b=1e-9,r=1e-6;
repeat at half sizes if interpretation depends on precision. Include homogeneous
control. Then test n31/63 with dt .0025 and half, t<=.5 initially, if benchmarks
and residuals pass. Increase to t1/2 only with shared-time convergence.

The padded-grid initial state is projected to the represented coarse spectrum.
Report its constraint re-solve and domain margins; this is a spectrally truncated
approximation of the same initial family, not identical arbitrary exact data.
Padding is an evaluation technique and cannot be used as a postshock closure.
No success is inferred from a less unstable spectrum alone.
