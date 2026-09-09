# IC30 executed radial bridge checkpoint

Base 002fba201d1e8830a4e39818ea59c3f926bb51c9. Full theory **OPEN**.
All jobs are terminal. Both v2 manifests validated with their pinned inputs
and log hashes (validator exit0). No empirical, novelty or Lean certificate.

## Evidence and actual statuses

- Full existing-plus-new closure suite:400 tests,205.446s, child0/runner0.
  Recorded runner runtime206.019054s.
- Scientific derivation including all eight actual radial EL expressions:
  39 exact identity residuals zero; four50-digit boundary-jet diagnostics;
  seven50-digit auxiliary solutions. All scoped checks true.
  Runtime15.675825s, strict child2/runner1, full theory OPEN.
- The six new tests passed after actual red tests. The C2 trial's third-jet
  mismatch was real (q'''=-60,s'''=30); the C3 septic construction fixes it.
  The failed trial is described, not promoted to a smooth solution.

Exact argv arrays and important test statuses are in run_index.json and each
manifest. Strict exit2 deliberately refuses full-theory certification; the
runner's failed status is preserved, not silently changed to completed.
Both jobs used300s wall,2MiB log caps and cooperative one-thread limits,
without hard memory/affinity caps. No resource limit was reached.

## Strongest results from the same action

1. Actual spherical phase-action variation retains the shift, shear and all
   auxiliary equations, including eta_q and eta_w before pinning. General
   S-only coefficients are differentiated, not frozen during variation.
2. Independent radial/angular metric variations reproduce the full static
   equations and an off-shell radial coordinate Noether identity. The
   exponential constitutive relation and leading MOND/no-slip equations are
   conditional on the derived regular static branch and local ordering.
   Clock/vacuum terms are retained before taking any approximation.
3. Under stated leading static hypotheses, continuity with wc<0 implies
   r w'<0; the pinned side has w'=0. This forbids that direct C1 glue only.
   Some sampled formal jets are not weak-field configurations; they check
   differentiation, not existence of a physical galaxy.
4. Constructively, the varied momentum equation integrates to

       (r³ exp(3Q)s)'=-(1/2)r³ exp(3Q)q'.

   A C3 profile joining q0 to q-1 on radii1..2 solves this exactly and has
   outer s=7/(4r³). For constant t its outer shift is
   beta=H_shift*r+7t/(12r²), satisfying the shear equation as well.
   These normalizations are illustrative, not fitted predictions.
5. The same-action z equation is a monotone cubic for D>0,E4>=0. Its unique
   real solution is smooth through q=z=0. Fixed A=.1,D=.13,E4=.01 at S=.1
   yields z=.376410511452222263830200365580407167810762 at q=-1.
   The cubic's z Jacobian is .277002184775806825763877205950167251168287;
   the cubic and implicit-derivative residuals are below1e-40 at all seven
   points. This is a solved auxiliary equation, not a full constraint count.

## Adversarial self-review and mathematical proofreading

Reviewed IC30_RADIAL_BRIDGE.md and the new code only. The radial/angular
variation was kept independent until after differentiation; the u=0 stratum
was not certified by division, the eta derivatives were retained, and neither
PPN parameters nor ranks/DOF counts were assigned. Checked the cubic derivative
and collar boundary jets independently. No routine proofreading or
mathematical-token corrections were required after the final run inputs froze.
This is self-review, not independent peer review or a formal Lean proof.

## Next unavoidable coupled solve

The constructed collar does NOT satisfy E_S or the pin/w system yet. Nor has
it been evolved. Use the recorded E_S,E_w,E_z,E_ell equations with ONE fixed
globally extended D(S), solve them jointly with the momentum equation, and
then evolve Q,q using the other derived equations. On eta>0 enforce w=wc only
after variation; compute ell from E_w. At eta->0 demand bounded multiplier
compatibility E_w(without pin)=O(eta), and rederive preservation on the
eta=0 stratum instead of importing the pin's constraint rank.

The exact momentum integral and monotone z elimination reduce the unknowns
for that coupled solve. The shear tail permits approach to a homogeneous
exterior without artificially forcing zero shear at a finite endpoint.
This is a concrete construction input, not an argument that the remaining
constraints automatically have a solution.

All original global obligations remain in scope: full nonlinear Dirac
closure including k0, full PPN, controlled zero-field limit, healthy clock
and tensor modes on the transition, strong-coupling/causal support, a global
coefficient function, expanding realistic cosmology and empirical tests.
The a0–Lambda coefficient remains an imposed parameter relation.
