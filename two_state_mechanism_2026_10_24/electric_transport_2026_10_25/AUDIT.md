# Self-review and reproducibility

Review type: same-agent independent checks, not external peer review.

Completed run `run`: exact Fourier oscillator propagation compared with direct
real-space kinetic/spring energy, uncoupled control, larger periodic box,
independent Cartesian integration of the shifted nodal free energy. Numerical
conservation does not validate the assumed material or continuum limit.
64/96 is a finite-box check at fixed microscopic spacing, not grid refinement.

Retained failed run `run_orbital`: its first assertion failure was the absolute
1e-5 energy-derivative check. Diagnostics at128sites,E=.03 showed derivative
errors .001503, .00001504, .000000133 at steps1e-5,1e-6,1e-7 respectively:
second-order finite-difference truncation, not energy nonconservation. The
corrected run uses1e-7; the pinned ORBITAL_ROUTE description's1e-6 refers to the
original invocation. v2's contract records the actual step.

Inspection also found a scientifically wrong, not-yet-reached assertion in v1:
it expected no local charge in the internal-only model. Broken inversion can
produce boundary polarization even without the site scalar potential. v2
replaces this with the appropriate zero-field neutrality check and retains all
internal-only boundary polarization in results. The scalar-position term still
changes charge transport substantially. Both source versions are preserved;
failed results are not used as scientific evidence.

Completed `run_orbital_v2`: exact charge count, zero-field density, inversion
and time-reversal checks for the proposed band, hydrogenic radial integral,
and occupied-energy derivative versus conjugate full position expectation.
There are18cases, each with two finite-difference auxiliary diagonalizations;
all are prescribed-field, fixed-counterion tests. The positive local cubic
mass conclusion is analytical, conditional on occupied lower band and cutoff;
these finite slabs do not validate the thermodynamic local-response limit.

Analytic self-review:
- Completing the oscillator square gives +Qg EO/K in H_eff, hence
  P=Q²E/K-QgO/K; sign and coefficient relation checked.
- Real-bond nodal displacement argument is limited to preserved real symmetry.
  Opposite-parity electric mass explicitly breaks inversion and evades it.
- In the orbital basis T=K, P=tau_z; kz tau_y and even tau_z obey both at E0;
  real tau_x is T-even, inversion-odd, as required for an electric dipole.
- Physical monopole and internal dipole positions belong to the same charge.
  Potential-drop versus induced-gap inequality is a local-band approximation,
  not a universal theorem about finite spectra or dynamical screening.
- Harmonic transport conserves energy but does not create entropy, dispose of
  halo mass, or demonstrate interband cooling. Rates shown in the derivation
  are conditional golden-rule relations, not computed formation rates.
- Size ordering is exact only for common homogeneous transport and comparable
  boundaries. The conditional thin-domain threshold .173785kpc is not used as
  an initial disk thickness, selector, or formation result.

All three manifests are checked against current source hashes; two completed,
one failed. No manuscript changes. No observational success or novelty claim.
