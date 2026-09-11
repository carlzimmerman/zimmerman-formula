# Full-gradient clock evolution implementation plan

Base: 440dad1ed324594ad4768d9ff5d3ec4b841b3d30.
User approved the next calculation: finite-time, constraint-preserving evolution
of the previous normal-rest initial data, followed by justified Lean results.
Keep the live repo, same action, constant gamma and one global a0 diagnostic.

1. Derive the full-gradient equations from the existing unrestricted spherical
   action. Use state A,R,Kr,Ko,Q,chi_r and conserved dust variables. Do not
   reimpose R=r, chi_r=0 or a unit lapse after the initial instant.
   Test absence of N_t; compare the zero-gradient restriction with the verified
   initial-slice equations; retain the clock-preservation equation.
2. Differentiate the reconstructed P,W,V functions away from the homogeneous
   trajectory while evolving their original background coefficients. Test
   fixed-X/Y derivatives and initial coefficient agreement.
3. Solve the full lapse problem and evolve dust plus scalar and metric. Check
   Hamiltonian, momentum, clock constraint, dust mass, background controls,
   timestep/grid/domain refinement and constitutive-domain margins. Stop on
   caustics, loss of lapse invertibility, or unresolved numerical error.
4. Measure invariant areal acceleration and independent metric potentials.
   Compare with the global exponential law without inserting it into the RHS.
   A failed numerical method is not a mathematical no-go.
5. Formalize only proved algebraic/analytic statements in Lean. Do not certify
   the whole theory from hypotheses that merely assert the target requirements.
6. Run every created script and relevant existing tests, preserve commands,
   outputs and input hashes, review, commit and push scoped results.

Three complementary routes are the full-gradient continuation, invariant
constraint-propagation checks, and conditional formal proof. The first uncertain
gate is the general preserved lapse operator away from chi_r=0. If it fails,
record the actual obstruction rather than reverting to an initial-only solver.

Scientific completion still requires the original common-action MOND, lensing,
Dirac/DOF, PPN, stability, conservation, GW and cosmological requirements.
Neither a short evolution nor a Lean certificate of algebra suffices alone.

Attribution continues: Carl Zimmerman suggested the dynamical test after sharing
Brian Keating's video https://www.youtube.com/watch?v=HRnselv8Y6E; motivation only,
not a verified transcript or endorsement.
