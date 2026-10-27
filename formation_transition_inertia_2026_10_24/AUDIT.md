# Self-audit: FT-I / FT-B1

Primary verdict: **incomplete, with the smallest missing implication being
a physically specified local formation process that creates and retains
the required state and density profile.** No completed trajectory here
establishes that mechanism. This audit is not independent peer review.

## Dependency checks

| Obligation | Evidence | Status |
|---|---|---|
| Initial density does not encode the desired galaxy law | Independent truncated Plummer quantiles, dark scale 3/10/30 | Passed for new runs |
| Positive masses and phase fractions | Fixed positive shell masses, q=sin²(pi x/2) | Passed in finite model |
| Positive kinetic completion of reversible pump | Cyclic-rotor square and Routh reduction in DERIVATION.md | Passed conditionally on global ansatz |
| Reciprocal force and phase work | Directional full-energy and finite-difference force checks | Passed in recorded test states |
| Dissipation has a receiver | Explicit positive Qdot, integrated Q | Passed as bookkeeping; microscopic receiver unknown |
| Angular exchange conserves J | Antisymmetric torque sum and recorded drift | Passed in finite model |
| Variable barrier pays its force | dU/dC dC/dR included and gradient tested | Passed in recorded test state |
| FT-B1 no-go applies to arbitrary shell rearrangements | Square completion plus equal-mass rearrangement proof | Passed under named hypotheses |
| FT-B1 rules out all formation models | Variable C, local phases, torque and external work evade hypotheses | False; not claimed |
| Transient conversion is persistent formation | Pilot and implicit histories | Failed for completed tested trajectories |
| High q alone reproduces disk dynamics | Additional moving-state forces and unconstrained mass profile | False; not claimed |
| A simulation timeout is a physical failure | Several explicit histories timed out | False; recorded inconclusive |
| Numerical trajectories are converged in continuum | Refinement status and accepted segments only | Not established globally |
| Observations validate the new coupling | No catalogue likelihood evaluated | Not addressed |
| Parameters follow from microphysics | alpha, I, drag, viscosity, virial proxy, beta | Not addressed |

## Adversarial reconstruction and limitations

1. The velocity-linear Routh term contributes no reduced energy. Its work
   cancels between radial and internal motion. Treating it as an external
   phase force would fail the energy identity.
2. Physical baryonic angular velocities differ from j_i/r_i² while the
   rotor pumps. The plots report the Newtonian gravitational monopole, not
   a full synthetic observed rotation curve. No RAR success is claimed.
3. Free-mass binding uses cold particles' unchanged angular momenta. It
   cannot establish eternal retention in an evolving potential.
4. A single phase x is shared by the reservoir. The lower-bound proof and
   formation failures must not be extended to spatial conversion fronts.
5. The proof uses equal baryon masses; it does not silently apply the
   rearrangement step to unequal weights. Actual runs have equal masses.
6. The constant-C proof is not applied to the contraction or torque routes.
7. The dimensionless bound is identical across four mass/size choices by
   scaling of the initial all-F Plummer model. Those repeated numbers are
   not four independent empirical confirmations. Three shell resolutions
   test the numerical evaluation of that bound, not physical generality.
8. Exact analytic inequalities are distinguished from floating-point
   evaluations of their margins. No interval certificate is claimed.
9. The independently inherited a0 branches are not pooled; only the
   canonical value is used. No implication about kappa=1/2 is established.
10. Receiver heat's tiny relativistic mass contribution is omitted in this
    Newtonian model, as in the parent. No covariant completion is claimed.

## Mathematical proofreading self-review

Scope: newly written CONTRACT files, DERIVATION.md and BARRIER_BOUND.md.
Checked definitions, energy signs, factors of two, cumulative-vs-shell mass,
ordered angular-momentum notation, hypotheses and finite-evidence language.
No mathematical-token corrections were made as proofreading. Physical and
mathematical limitations are listed above; they are not typographical issues.
