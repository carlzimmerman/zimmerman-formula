# Continuation guardrails

Current result: **not solved**. Read README and DERIVATION before another run.
Ten bounded experiment records exist; do not count optimizer flags, nearly
unit q, imposed gravity or positive coarse Hessians as a physical solution.

## What was new and what survived

An independent conserved interface charge has E_Q=k/I. Its exact variation
supplies outward radial force and resists loss of interface contrast.
Polarization capacity I=int F(u)|grad q| supplies a mass-dependent chemical
offset that is constant in a pure interior; that is a legitimate way to
change conversion energy without a bulk acceleration there. Independent area
tension supplies a competing inward radial force. All associated phase,
species and mixed Hessian terms were included and finite-difference checked.

Neither ingredient is a derivation from the original formula. Q is supplied,
not formed. Beta1000 is a modified phenomenological barrier. Live baryons,
total-density relaxation and local charge transport have not been simulated.

## Closed tested routes and false positives

1. Plain area charge: outer ripple storage and loss of the converted core.
2. Strong barrier plus plain charge: attractive n128/256 candidate fragments
   at n512. Negative material pressures already invalidate its simple closure.
3. Response charge: retains full density derivative, but response stiffness
   still permits fragmented charge storage. Constant original stiffness does
   not recover all gates in the tested cells.
4. Response charge plus tension, k100,tau.1,beta1000: excellent interior law
   and free exterior through n512; layered phase profile; a negative local
   kinetic-stress bound excludes arbitrary nonnegative kinetic anisotropy
   at this prescribed density and zero outer T traction. Displacements do not
   return to the same radius despite positive finite-grid phase Hessians.
5. Targeted traction repair k120,tau1: positive isotropic pressures for both
   species through n1024, so the previous pressure exclusion is not universal.
   But interior-force error rises .00906 -> .2207 -> .9086 at n256/512/1024.
   Phase fractions remain almost pure. Plus/minus .2 kpc shifts do not restore;
   errors become .564 and 3.956. This is not a working galaxy-law branch.

## Do not repeat

Do not rescan these cells under a renamed interaction. Do not freeze contrast,
conserve T number, impose an exterior phase, omit the charge mass derivative,
or hide extra interfaces. Do not claim a spherical wall-coordinate minimum
proves field stability. Positive pressure is only necessary for kinetic
equilibrium, and no distribution function was constructed. Negative U at an
appreciable population is a stronger exclusion than negative isotropic P;
tiny trace-population negatives are numerically insignificant.

A new continuation must change a specific failed assumption and test the
coupled matter balance and continuum wall restoration, not only phase energy.
If density is released, recovering the galaxy law becomes an output to test.
If charge is retained, its formation and transport must be supplied rather
than relabeling preloaded Q as spontaneous inside-out conversion.

All sources/results are local snapshots. No manuscript or unrelated experiment
was overwritten. Reports are self-reviewed. No external scientific theorem
or new observational evidence was invoked. Validation commands and results
are in validation.json and the per-run manifests.
