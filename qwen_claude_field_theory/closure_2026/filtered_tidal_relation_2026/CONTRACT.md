# Filter-independent central tidal relation: computation contract

Continue the static action in ../smoothed_onset_action_2026; do not alter it.
Decision: does its linear response around a nonzero constant filtered
Newtonian background constrain the central anomalous monopole and quadrupole
independently of isotropic smoothing shape/length and source mass?

H is the Hessian of the additional (phantom) potential, not the singular
Newtonian point-source Hessian or the physical tidal acceleration tensor -H.
Q2=H_perp-H_parallel and D=trace(H)=4 pi G rho_ph(0). Background s_e=y mu(y)
is the filtered Newtonian gradient/a0, not automatically the measured
physical external acceleration. mu=1-exp(-y); nu is its exact inverse partner.

Analytic domain: y>0, constant background, leading source-amplitude response,
spherical source, real isotropic self-adjoint filter commuting with flat
derivatives, finite radial spectral integral. Physical use also requires
filtered source gradient much smaller than the ambient gradient. No claim
about the nonlinear Sun, non-spherical sources or cosmological k=0 modes.
At zero trace use the division-free identity rather than its singular ratio.

Finite surrogate: derive angular moments with SymPy and separately integrate
the full directional Hessian by spherical quadrature. Test Gaussian,
Helmholtz and rational quartic filters, widths 0.4/1/2.5, Gaussian source
radii 0/0.3/2 and several y values; independent rotated axes. Float64,
deterministic angular nodes and adaptive radial quadrature. Verify the exact
constitutive Jacobian by finite differences of the existing nonlinear flux.
Vary angular resolution and compare known analytic radial integrals.

Outputs: runnable script/tests, numerical results, provenance manifest and
report with a bounded prior-art comparison. Passing means the displayed
linear-response relation survived those checks, not that gravity is closed
or a prediction was detected. No gravitational DOF/PPN/cosmology certification.
No observational data are used. Novelty remains a separate source question.
