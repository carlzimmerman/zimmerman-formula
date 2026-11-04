# Next calculation for the filtered gravity branch

This is a review recommendation, not a new empirical result or a blind
preregistration. Current kappa=1/2 remains fitted; canonical and alternative
footings remain separate. Route E stays retired. Existing seals are unchanged.

## Question

Does the narrow KT25 window survive when the source smoothing and the force
on matter are derived from the same energy?

Use the actual simple-nu kernel of KT14–27. For a declared fixed normalized
Gaussian S, the candidate reduced energy and resulting potential are

    U[rho] = U_N[rho] + U_ph[S rho],
    Phi[rho] = Phi_N[rho] + S* Phi_ph[S rho].

This changes the equation currently graded. Existing passing labels do not
transfer. The old nu_mono parent and the CFG653 high-pass model are separate
comparators, not substitutes for this calculation.

## First checks

1. Use the same discrete volume-weighted inner product for Poisson solves,
   gradients/divergences, and the filter adjoint. Derive S*=W^-1 S^T W on a
   nonuniform grid. Boundary treatment must be included in the adjoint.
2. Verify reciprocal source perturbations and net-force behavior on asymmetric
   sources; a spherical test alone can hide the defect. The periodic examples
   in this review supply an independent benchmark.
3. Recover Newtonian gravity when nu=1 and ordinary QUMOND when S=I. Check
   exterior truncation, mass accounting, and spatial refinement. Do not waive
   the inherited gas-mass or SPARC-envelope checks merely because they failed
   in the earlier implementation.

The analytic reciprocal-Jacobian condition has been established in this review.
The proposed observational solver has not been implemented or verified here.

## Smallest observational discriminator

Use KT25's existing canonical candidate values and saved near-pass Milky Way
cells. Apply the outer adjoint to the phantom contribution, and recompute
radial acceleration and the complete vertical field. Recompute the Solar
System quadrupole with that same force prescription and matching boundary
conventions. Include the plain-QUMOND and source-only results as controls.

Keep the original prior corner visible: the recorded nine Milky Way cells
are not robust interior solutions, no star-count-share .12 cell passes, and
the stricter vertical scale-length test fails. Report shifts against those
small margins. Do not change the thick-disc prior or refit epsilon after
seeing the new result and call it confirmation.

This stage declares a fixed width for each controlled source problem. Even
if both calculations survive, that is a conditional diagnostic, not a common
law assigning xi to the whole Universe. No full-galaxy survey rerun is justified
until the existing near-pass behavior is understood under the corrected map.

## The next required physical definition

If the fixed-width diagnostic survives, define one filter on an unsplit matter
distribution containing a host, a satellite, and compact sources. The result
must be unchanged when one source is arbitrarily relabelled as two sources.
A rule xi=kappa sqrt(G M_system/a0) has not defined this operation.

For a state-dependent S[rho], vary the entire map A[rho]=S[rho]rho. The matter
potential includes DA[rho]* Phi_ph[A[rho]], not just a row-wise convolution
with a width evaluated from observed accelerations. Specify the state equation,
its boundary conditions, and all independent scales before computing data
scores. Check extrema and homogeneous-density regions, where derivative ratios
used in tidal widths can become singular. A numerical clip is an extra input.

Action-based geometric response, including generalized QUMOND, is a legitimate
alternative construction. Its additional functions or constants must be counted
honestly and its predictions derived. It does not automatically derive kappa,
the filter length, cluster lensing, or early cosmology.

## Disposition at the first checkpoint

- **Fails reciprocity/force tests:** implementation or action mismatch; no
  astrophysical conclusion.
- **Consistent operator loses the fixed candidate window:** this completion at
  these premises is not the hoped-for repair; preserve the failure before any
  materially changed proposal.
- **Consistent operator keeps the window:** retain a conditional spatial-response
  lead, then address source composition and the common scale definition.
- **Only an object-by-object fitted width works:** report a phenomenological
  prescription, not a derived universal force law.

After a common definition exists, the next serious falsification is a joint
Milky Way radial/vertical and host/Fornax calculation with independent baryons,
then the wider galaxy/cluster/merger requirements. A pass at the first checkpoint
does not answer those remaining questions.
