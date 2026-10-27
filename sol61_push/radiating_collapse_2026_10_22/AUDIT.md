# RC-20261022 self-audit

Primary verdict for the user's joint target: **incomplete**. A reproducible universal remnant and preservation of all data/growth tests are not established. The finite radial family fails the common-mass diagnostic; instantaneous inner-profile convergence also fails. These are distinct outcomes, not implementation failures. Review provenance: self-review, no independent agent.

## Dependency and obligation matrix

| Obligation | Evidence | Status |
|---|---|---|
| Same material/field energy generates reciprocal forces | model.py Hamiltonian derivatives; three directional derivative comparisons | Passed in the declared discretization |
| No artificial matter cooling or removal | Matter update has only Hamiltonian forces; mass weights fixed; absorber acts only on field momenta | Passed by code inspection and mass/energy checks |
| Outward material transport allowed | Shell radii unconstrained inside the grid; crossing allowed; boundary reach raises an error | Passed; nonradial fragmentation excluded |
| Field export is separated from initialization noise and finite-radius exchange | Frozen-source control; absorber tally; signed r=6 flux; larger box and refined strong run | Conditional positive strong-phase export; weak baseline flux not treated as clean cooling |
| Bulk retention independent of tested regulator change | Refined unit-mass and heavy runs; M(<2) changes 0,0,.0078125 of initial mass in named pairs | Passed for those repeats, not a continuum theorem for every row |
| Converged instantaneous inner profile | Empirical CDF changes .219 then .152; gate .05 | Failed |
| Time-average inner aperture convergence | Two finest means differ .0283; gate .05 | Passed finite diagnostic only; no equilibrium inference |
| Common finite-time central mass | Long seed1,2,4 spread 1.233 of mean; gate .1 | Failed in stated family |
| Canonical endpoint energy budget | Convex field minimization at fixed cold profile; zero-spin endpoint; energy balance | Conditional on that endpoint and nonnegative-energy separated debris |
| No finite fastest linear fragmentation scale | Internal dispersion derivation, positive A'(k), nine finite scans | Proved in the stated unpumped static local regime; self-reviewed |
| Dwarf/rotation fits preserved | Snapshot sensitivity only, no refit; unconverged profiles and unevolved baryons | Not established |
| Full cosmological growth and cluster abundance | Homogeneous source structure identified; no cosmological population evolution | Not established |

## Critical reconstruction and caveats

1. The shell model is a variational projection, not the complete field theory. Spherical shape constraints eliminate angular torques and fragmentation. Crossing requires multiple shell currents and does not solve a unique single-stream continuation. Regulated inertia also alters very small-radius rotational barriers. These facts are explicit in CONTRACT.md and RESULT.md.
2. The gravitational pair energy is -m_i m_j/sqrt(max(r_i,r_j)^2+soft^2), with the self-shell half term. Its derivative matches the sorted enclosed-mass force. The same softening appears in the stated inertia regulator; neither is a physical mass selector. Shell crossing makes forces piecewise smooth, so formal second-order time accuracy alone is not a convergence guarantee.
3. The field force uses the derivative of deposited density, not an independently interpolated force. The finite-volume P divergence and gradient are adjoints under radial volume weights. Positive phase/polarization energies and the exterior loss tally account for the measured Hamiltonian balance.
4. Field-energy balance in a source-free radial region gives flux h*w_dot-d*z_dot*z_r. A finite-radius net flux can be negative during reversible near-field rearrangement. Absorber losses at different radii have different travel delays; only same-radius flux was compared for the box test. The heavy strong-phase signal exceeds energy error substantially and repeats to13.1%; this supports export but does not measure infinite-time cooling efficiency.
5. Conserved cold material is not carried by chi/P radiation in this action. Energy escape and material escape are therefore different observables. The outward-energy criterion is deliberately a candidate criterion, not a proof that no particle ever escapes at later times.
6. The endpoint inequality has the direction E_initial >= E_endpoint,min. If initial energy is more negative than the specified endpoint, losing positive energy cannot reach it without another negative-energy component or external work. Fixed-density field convexity does NOT prove that this density is the global ground state at that mass. Different profiles, bound envelopes and self-bound fragments are outside the exclusion. Initial seeds below the requested mass fail by material conservation, separately from the energy test.
7. The phase source vanishes at linear order about e=X=0. The local growing mode polynomial eps*y²+A*y-rho0=0 follows directly from the coupled density/P equations. Since A'(k)>0 and dy/dA<0, this branch has no finite fastest wavelength. It does not address expansion, velocity dispersion, shearing backgrounds or nonlinear fragmentation.
8. Snapshot observational summaries are explicitly withheld as physical fits. Agreement of a rotation-curve mean does not validate individual curves, scatter, baryonic response or a transient Jeans interpretation. The prior growth calculation is cited with its quasistatic/EdS limitations, not rebranded as a new cosmological test.

## Run accounting

Ordinary result checks: pilot8, survey21, long8, endpoint-energy10, linear11, snapshot-feedback37, refinement3 (98 total). These checks concern execution, invariants, coverage or finite diagnostics. The interpretation record separately contains five passed gates and two failed gates. A successful postcheck command means the findings were recorded, not that all gates passed. The first endpoint run failed during NumPy-boolean JSON serialization; corrected source and rerun preserve numerical equations and old evidence.

Figure rendered and visually inspected. Mathematical self-proofreading covered only the new checkpoint; no manuscript integration or historical-file rewrite. Exact sources and input hashes are recorded in the per-run manifests; final artifact inventory in CHECKPOINT_SHA256.json.
