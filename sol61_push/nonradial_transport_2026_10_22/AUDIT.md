# Self-audit NT-20261022

Primary verdict for the user's full claim: **incomplete, with the smallest missing implication** being a derived nonlinear mass partition from supplied initial phase space. Evidence here does not connect linear footprints to bound stationary remnants or their observable profiles.

Claim cards:
1. For the declared cold, frozen-profile, quadratic quasistatic sheet, a finite fastest linear wavelength exists. Internal derivation and numerical verification; no equilibrium-formation claim.
2. For fixed-geometry central pair interactions independent of mass, cold nonradial transport respects the stated mass/time similarity. Internal uniform proof; finite numerical checks corroborate it. Conclusion restricted to this reduced regime.
3. A compact compensating rearrangement preserving mass and centroid changes its Fourier profile first at k². Internal Taylor bound |exp(iu)-1-iu|≤u²/2, averaged over a positive mass distribution. No inference about growth history from a profile bound.
4. These mechanisms select real core masses and distributions and preserve all fits. Not established.

Dependency graph: inherited action -> quadratic fixed-phase elimination -> 3D kernel -> vertical average -> sheet dispersion -> selected wavelength. Selected wavelength + supplied Σ + chosen footprint convention -> patch mass (not a remnant). Quadratic elimination -> softened pair Hamiltonian -> reciprocal forces -> conserved total L/E and scaling family. Full nonlinear action -> mass partition -> stationary profiles -> dynamical baryon response -> dwarf/rotation/cluster/growth tests remains unresolved.

Checks and scope:
- Surface-density normalization explicitly carries 4π; converting circular area yields π²Σ/(4k²). The preferred wave number has kstar²=(sqrt5-1)/2, not kstar equal to that number.
- H→0 gives the razor-thin kernel. Force uses the average of two vertical profiles; replacing it by the midplane expression would be a different model.
- Sheet peak is a true interior maximum: derivative changes sign at the single interior root and F vanishes at both endpoints.
- Rotation subtraction checked against the constant-k three-variable matrix spectrum. Nonaxisymmetric transient growth does not contradict axisymmetric stability.
- Nine Fourier integrals, six thickness values, five surface-density values, thirty shearing waves, three tighter repeats. No full parameter-space coverage asserted.
- Pair forces independently checked against finite energy differences; total torque checked separately. Discrete integration conserves L to roundoff, energy to the declared tolerance. No inference of spatial convergence from conservation.
- Fixed initial inner particle labels avoid conflating torque with radial advection. Their L increases in the reported cases. Transfer diagnostic can exceed one because counterrotation allows absolute exchanges greater than net L.
- Mass similarity includes velocities, spin ratio, time rescaling and fixed softening; it is not a theorem for the full logarithmic action or prescribed physical-time endpoints.
- The prior-seed L/(M j) inventory applies only to the stated central potential and sign constraint. Extended self-gravitating sheets need their own force and equilibrium calculations.
- Finite thickness is frozen; no vertical equilibrium, velocity dispersion, phase/polarization validity bound, field radiation or live baryons is supplied.

Ordinary checks: 14 sheet + 19 transport + 6 postcheck = 39, all pass. Interpretation gates: qualitative torque repeat passes; 0.01 absolute L-distribution precision fails; absolute mass selection fails in the quadratic family; full nonlinear dwarf/rotation/growth joint test is not performed (recorded false to prevent promotion). A completed runner is not a claim that those gates passed.

Provenance: self-review only, not independent audit. Original base revision b0ced915c8a722595eedef88ac8d63c57a0208ca. Per-run manifests record actual observed revision, dirty state, input hashes and output hashes. No .mathbox ledger is present; local evidence format retained. Earlier cold_fragment_modes uses a different scalar action and cannot supply missing masses for this route.

Proofreading self-review applied to RESULT.md and this audit: definitions, signs, units, k/k² distinctions, numerical table entries and links checked. No mathematical-token corrections to inherited files. No unrelated files reviewed or edited.
