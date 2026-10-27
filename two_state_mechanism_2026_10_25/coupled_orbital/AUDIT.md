# Self-review and reproducibility

Same-agent review; no external peer review or claimed breakthrough.
Four completed provenance records: run, run_refine, run_quantum, run_figure.
Sources are immutable after their runs. Imported solver.py is pinned in the
refinement dependency closure; figure inputs include both raw result files.

## Construction and checks

- Density and dipole come from the same two-orbital covariance. Ionic -Q is
  retained in both the fixed neutral reference and its displacement polarization.
  Source charge is mean zero; zero-mode pseudoinverse never supplies a neutralizing
  background for a nonneutral physical simulation. The independent off-manifold
  gradient test does use that pseudoinverse extension as stated in code.
- Skew-adjoint central derivative makes the dipole term +d grad(phi) tau_x;
  force on negative ions is +Q grad(phi). Finite differences give orbital-gradient
  error9.70e-8 and ionic-gradient error7.61e-9. The Coulomb energy is counted once.
- Free, electrostatic and deformation subflows conserve their respective
  Hamiltonians to6.83e-13 or better. Weighted orbital Gram preservation checks
  all occupations, beyond trace alone. No state renormalization is performed.
- Link-current commutator independently reproduces particle-density derivative.
  Adding internal/ionic polarization current verifies local charge continuity
  to2.39e-16; direct finite differences of deposited charge agree4.28e-10.
- Representative4³ and6³ dt refinements exhibit quadratic total-energy error.
  Report small electric-energy normalization alongside large band-energy
  normalization. The saved error maxima use sampled observation times, not every
  integrator step; this limitation applies to all reported maximum drifts.
- The no-source, non-circulating thermal band stays stationary in density and
  ions (wavefunction phases still evolve). The no-source circulating control
  shows why circulating preparation energy cannot be called source cooling.
- All19 dynamical runs use the stated material coefficients except the explicit
  g=0 control. There are9 main initial-state points,2 additional dt refinements,
  a g0 control, a no-source stationary control, one6³ circulating case; plus5
  refinement/continuation runs. None is a galaxy population sample.
- The larger grid changes probe wavelength and initial circulating state.
  Periodic Lz has a seam and is not conserved by this lattice. No claim of
  continuum convergence, physical rotational support or virial equilibrium.
- Small ionic displacements (order1e-3 in representative tests) are consistent
  with the stated linear charge-deposition approximation, but no general
  large-displacement, melting or unbound-ion model has been validated.

## Quantum benchmark

Expand the complete electric square before quantizing. Keep both countercharge
stiffening kappa Q² and constant kappa d²/2. The same cross term fixes g_q.
Hamiltonian is full Rabi, with counter-rotating terms. Occupation16/24 comparison
and edge populations check oscillator truncation; this is not exact infinite-
Hilbert-space proof. Energy agreement and parity expectation values are separate
checks. On resonance min excited population.00394325 does not imply99.6% of
*total* energy is transported: it is orbital population transfer accompanied by
phonon and interaction energy. Recurrence is explicit in the figure.

The model is a single local countercharge mode; it is not an exact reduction of
the entire3D lattice. Its stiffness has the same numerical value as the lattice
spring, but selected-mode eigenfrequencies in that lattice must be derived.
The published CEID abstract was visible through web search; direct publisher
open returned403. No full-text formula from that source is used. The numerical
benchmark independently demonstrates the mean-field limitation.

## Claim boundaries

No Maxwell retardation, photons, live gravity, continuum mass spectrum, mobile
reference lattice, positive tethered species, counterion dissociation, actual
capture, spontaneous formation or galaxy acceleration-law test. The orbital
mass uses the actual instantaneous field, but this does not validate its bulk
critical spectrum in the finite lattice or its astrophysical parameter mapping.
The stage is evidence of implemented coupling and a quantum correction needed
for cooling, not evidence that the original galaxy objective has been achieved.
