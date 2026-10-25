# Audit and scope

Disposition: finite implementation and numerical checks verified within reported
bounds; physical inference conditional on chosen bosonic/coherent mean-field
state, uniform local background, vacuum force matching and inventory prescription.
No independent reviewer, exact many-body solver or proof checker was used.

Checked algebra: in units omega0², D11=Q², D22=Q²/epsilon²+1/epsilon-epsilon,
D12=-(1+epsilon)/sqrt(epsilon). Thus epsilon² det D =
t²+epsilon*(1-epsilon²)*t-epsilon*(1+epsilon)², t=Q². The stable threshold is
unique and positive. Equal-mass eigenvalues Q²-2,Q²+2 verify signs independently.
For epsilon1 the dipole vector lies entirely on the gapped upper branch.

Three independent representations: 2x2 matrix eigenmodes, direct complex
resolvent, and Fourier Schrödinger field acceleration. The latter independently
recovers the mass factors and linear force coefficients and converges with
perturbation amplitude. The nonlinear FFT solver uses the same Hamiltonian with
Strang splitting. Timestep refinement is second order; reported errors use every
full timestep. The quadratic ODE checks use 101 sampled times, not every internal
step. The denominator for energy error is a positive component scale rather
than a possibly cancelling signed initial energy.

Spectrum output returns no stationary spectral weights when either eigenvalue
is nonpositive. Eigenvalues/charge residues remain recorded for algebraic
diagnostics. No unstable mode is counted as a stable critical excitation.
No integration over all k or ultraviolet zero-point energy is claimed; these
would require vacuum subtraction/renormalization and occupation/depletion control.
All short 3D runs are weakly nonlinear; spatial agreement there does not establish
convergence in collapse or a strongly correlated phase.

Physical scan is 3eps*241m=723 parameter points and four numeric profiles per
point. 378 points satisfy the stated wave-speed cutoff in every profile. The
scan's separation criterion is an explicitly limited Jeans-stability proxy,
not the user's actual tether/free-population criterion. Its analytic failure
is not evidence that all quantum media or the intended mechanism are impossible.
Mass threshold ordering holds for any common epsilon>0 under the displayed
inventory and wavelength conventions. Inventory fraction or boundary wavelength
changes alter thresholds; freely choosing these per galaxy is not authorized
as a first-principles derivation.

The species-exchange symmetry reduction epsilon1 is discussed as an optional
hypothesis. It does not eliminate the need to derive a viable state, dynamics
and microscopic mass. Matter/antimatter annihilation is not represented; the
two Schrödinger species conserve separate numbers in this approximation.
No microscopic rates are inferred from the macro wave solver.

No charge-conserving spectrum has been shown to supply the previously required
nonlinear static response. The full longitudinal interacting response cannot
be inserted as an irreducible Maxwell susceptibility without double counting.
The figure was visually inspected; sources and evidence are unchanged after runs.
