# Self-review and claim calibration

This is self-review, not independent verification or a full-PDE convergence proof.

The radial operator is self-adjoint after v=sqrt(w)*r*psi. Its kinetic quadratic form agrees with the independent weighted gradient sum. Production prefix-sum Poisson potentials agree with direct symmetric shell Green matrices. Centered finite differences of the self-energy agree with its Galerkin Hamiltonian gradient, confirming the 1/2 gravitational-energy factor and its full potential in the wave equation. Dealiased angular quadrature gives the correct Gram matrix and zero instantaneous self-torque in all three components. L=4 independent checks are recorded separately.

The source-free static linear test explicitly subtracts all negative-energy eigenstate overlap and uses a time-independent, closed Hamiltonian. Its bound mass remains ~1e-25 under Crank-Nicolson. It is a null control for spurious linear capture, not evidence that the nonlinear initial cloud starts unbound. Production cold clouds are already collectively bound.

Positive sink energy, outward current, and longer/finer/stronger-boundary calculations support emitted waves. They do not make finite-boundary energy ratios exact asymptotic spectra. The original log grid inadequately resolves outgoing wavelengths; its zero-loss pilots are not null evidence. Weak-sink wall reflections were a concern; the separate stronger/wider boundary run retains the qualitative transport and excessive central gravity. Combined changes do not identify the individual error contributions.

The first gas-free dt=.04 run fails the numerical ledger, stops at t=104 and is rejected. dt=.01 repairs the ledger to within the stated 1% energy/J gates. Rejected outputs and code versions are preserved. Conservation alone does not certify a correct dispersion relation or sufficient angular cutoff.

L=2 vs L=4 materially changes exported spin and half-mass radius. The transport fraction is therefore NOT angularly converged. The large central mass/stellar mismatch persists across those cases and the radial/boundary sensitivity, but is still only a failure of this finite common-history family under the stated stellar diagnostic. It is not an exclusion of every pre-stellar history.

Base initial states contain a spherical seed. The seed-free case tests l=0 creation, not a spurious zero Jz from coordinate choice. Its initial axis is tilted; analyze.py explicitly computes full initial/final/core J vectors and does not treat its recorded Jz flux as a validated total-spin flux. The aligned even-m base cases have negligible Jx/Jy. Low net spin, low angular gradient pressure, l=0 occupation and merely counterrotating material must remain distinct.

Stellar probes use saved MONOPOLE histories, a circular stationary initial ensemble and an analytic frozen control. They omit nonmonopole forces, finite-snapshot temporal structure, self-consistent birth/DF/backreaction and observational selection. Their initial dispersions are already incompatible. No observed stellar heating measurement or safe-birth conclusion is claimed.

The action, eta, inventory/catchment normalization, prescribed gas evolution, initial bound cloud and present-size normalization are assumptions. No host tide, cosmological expansion/capture, formation of the initial cloud or physical gas-feedback energy budget is computed. All such obligations remain open. Numerical field fluxes do not establish the real-world existence or controllability of a new cold-energy substance.
