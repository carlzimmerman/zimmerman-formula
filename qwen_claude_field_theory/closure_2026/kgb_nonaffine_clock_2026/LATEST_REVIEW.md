# Review of concurrent CMB / parameter-space claims

Reviewed actual diffs and executable files, not commit titles alone:
`727af1f7a`, `5fe3bc30c`, and `3363fda06` (L121, AQUAL positivity, L122).
The root verification suite reruns the literal L121 checks and compiles the
concurrent Lean file. These are unchanged inputs; this review edits none of them.

## What can be kept

The new exponential, simple and standard kernel theorems prove positivity of
the displayed transverse/longitudinal expressions for strictly positive y.
For their correctly identified AQUAL Hessians this establishes pointwise
ellipticity. It does not include y=0, uniform ellipticity, the complete coupled
kinetic matrix, nonlinear Dirac closure, or the physical metric sourcing map.
The exponential kernel therefore remains a reasonable fixed constitutive input;
its full action placement, rather than this isolated positivity check, needs work.

L121 correctly distinguishes two different time dependences numerically. Its
benchmark arithmetic is reproducible. The detailed same-action cosmology audit
is in `cosmology/`; it includes the previously omitted mapped baryon terms.

## What the evidence does not permit

1. **A constant global a0 is not a local fitted a0.** With a constant Lambda,
   Carl's input a0=(c/2)sqrt(G rho_Lambda) is constant. Substituting H(z) for
   sqrt(rho_Lambda) during radiation/matter domination changes the hypothesis.
   L122 Axis 5 cannot eliminate constant global a0 by rejecting local-density
   fits, nor call H-tracking an established consequence of Carl's relation.

2. **a0/(cH) is not a CMB verdict.** Mode acceleration depends on perturbation
   amplitude and wavelength; its dynamics must come from the action. L121 uses
   an LCDM benchmark with Omega_m=.315, not this particle-free action's solved
   background. Two of its six checks (`PEAK-2`, `VERDICT-1`) are literal True.
   Neither their exit status nor equality-redshift arithmetic derives a
   universal third-peak exclusion or a successful H-tracking rescue.

3. **Restricted scalar failures do not eliminate all propagating clocks.**
   A power-law RAQUAL sound-speed formula, a particular KGB background, and a
   particular deep-MOND instability concern different restricted models.
   They are not a theorem for all F/P/G clock actions. The explicitly counted
   clock allowed by the user's requirements must be judged in the SAME action.
   Our locally healthy derivative-conformal examples are not a completed theory,
   but preclude inferring universal local scalar sickness from those examples.

4. **A lapse Hessian or an isolated elliptic operator is not full constraint
   closure.** First-class classification requires all constraints and their
   preservation/Poisson brackets. Calling the Hamiltonian constraint first-class
   while listing nonlinear termination as unverified is an unfinished argument.
   Likewise, a two-jet kernel positivity theorem does not certify the full
   cuscuton/metric/matter system, all kernels, or a zero-field limit.

5. **The surviving architecture is not proved unique.** L122's 'ONE
   architecture + ONE open axis' conclusion exceeds its scoped exclusions.
   Its own remaining PPN and nonlinear-constraint gates already exceed one
   axis. The correct reduction is a list of conditionally excluded families,
   explicit surviving examples, and untested function/branch sectors.

## Efficient replacement

A later commit, `293b4e70a` (L123), adds another overbroad inference. The exact
counterclaim audit in `l123_review/` varies the standard P=X^N action and
refutes its universal stiff-tail assertion. Its conditional Lean sign/range
certificates do not claim a CMB solution. Vanishing one displayed Poisson
bracket term also does not certify an added sector's full ghost freedom.
Three of L123's physical verdict checks are literal True. Its program is
rerun unchanged by `run_supplement.py`, with this interpretation caveat.

Use the exact full-real-axis curvature criterion and matched-mass cancellation
proved in `variation/`, rather than rescan arbitrary F_XX ranges. Preserve F/f
and P/G along the trajectory; do not independently reset them. Before expanding
cosmological parameter scans, solve common-mass compatibility and the physical
source/clock boundary normalization. Then evolve the same functions and mapped
matter on FLRW and derive its perturbations. None of these steps requires a
per-galaxy a0 or an unannounced switch to a0 proportional to H(z).

Credit: Carl Zimmerman specifically prompted the global-versus-local a0 audit
and the requirement to join CMB, galaxies, lensing and time observables. His
fitted coefficient remains credited as an input, not relabeled a derivation.
