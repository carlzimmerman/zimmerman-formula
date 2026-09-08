# IC-2: constructive spatial completion of IC-1

Base checkpoint: `6dd851cf55039986b4ff1d1d88ca59c483328ca5`, 2026-09-08.
**OPEN.** This is a new explicit action revision. IC-1's pinned computation
is preserved; its homogeneous results do not assert local scalar stability.

Retain every definition, field and coupling of [IC-1](ACTION.md), including
the physical metric, positive canonical-clock normalization kappa, exact U,
w=(u-1)ln N, and Q=K-3 n.grad w. Fix ell=ln(9/5). Define

    J = -a_mu D^mu u/(4 ell^2) + 3 D_mu u D^mu u/(64 ell^2),

    S_IC2 = S_IC1 + (m/2) integral sqrt(-g) (Q^2/a0^2) J.

These are fixed coefficients, not functions chosen separately in different
sectors. The correction is quadratic in Q and contains only spatial auxiliary
gradients on clock leaves. It is not a new independent matter metric.

## Same-action bridges that must be checked

* For any exactly stationary branch with K=W=0, Q=0 and the correction and
  its first variations vanish. Thus the original static equations, including
  the non-negligible clock-source caveat, are unchanged. This does not supply
  a previously missing global stationary solution.
* For the homogeneous background of IC-1, a=Du=0; J and its first variations
  vanish. Thus that expanding solution is still a solution of IC-2.
* The correction vanishes identically on the homogeneous reduction, not just
  at the particular de Sitter solution: its homogeneous Dirac proof transfers.
* In the barred spatial metric coordinates, Q depends on metric velocities
  but not Ndot or udot. The primary integrability identity remains exact.
  The trace kinetic coefficient becomes -2/3+J/a0^2. The metric velocity
  block is invertible near the displayed homogeneous branch, where J=0;
  the surface J/a0^2=2/3 is a separate unanalysed stratum.
* A pure TT perturbation of this homogeneous background has a=Du=0, hence
  the correction contributes no TT quadratic term. The luminal positive
  tensor block is unchanged there, not automatically on every background.
* Ordinary S_m[g,psi] is unchanged and retains its own matter Ward identity.

The next calculation must derive the full scalar quadratic action from THIS
corrected action, reduce its constraints, and examine signs for all wave
numbers. A high-frequency limit is not a proof of full causality or of
acceptable horizon-scale evolution. Cosmological perturbations, local static
matching, zero-field control and PPN still belong to this same action revision.

The coefficient choice is a constructive solution of a quadratic compatibility
problem, not a first-principles derivation of a0, Lambda or primordial abundance.
No empirical or global novelty claim follows from it.
