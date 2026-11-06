# PF01: AC2q fold and post-fold predictivity

Base checkpoint: 60263a84e20aaa1c98ba3729708f4171d059a253.
Owner: current Codex chat. New directory only; preserve AC7–AC12 and X14.
Authorized target: determine whether AC2q survives as written, needs an extension,
or fails. A reduced-model obstruction is not a no-go theorem for the full action.

## Definitions and target
AC2q is AC7's covariant action, with X>0, |KP|<a0, and stiffness
-gamma/2 {max(D.P+2X,0)^2-(2X)^2}. Work from the action, not labels.
Distinguish (i) finite compression J=1e-3, (ii) true J=0 crossing,
(iii) bounded-density gradient catastrophe, (iv) weak shock continuation.
A survival claim requires a specified solution class, admissibility rule,
unique/convergent observables, conservation and a controlled connection to
AC2q. No numerical viscosity may be silently interpreted as action physics.

## Route portfolio and preregistered discriminators
R1: Native pressure and smooth breakdown. Derive the planar principal system
q_t+(qv)_x=0, v_t+(v^2/2+gamma max(q,0))_x=F, with q=P_x+s^2,
F=W_P-Phi_x at the leading PN order used in AC10. Check native pressure
p=gamma max(q,0)^2/2. For F=0, gamma=1, positive-charge simple wave
c=1+0.4 sin(x), q=c^2, v=2(c-1), x periodic on [0,2pi), derive first
characteristic breaking exactly. This is a principal-system test, not a full
sourced spacetime solution. Inspect AC10 threshold and post-crossing rules.

R2: Weak continuation. Derive mass, Bernoulli/velocity, momentum and energy
jump conditions independently. Test whether a finite positive-charge shock
with no surface degrees of freedom satisfies them simultaneously. Check
small-amplitude and equal-state limits; retain failures of attempted extensions.
Compare potential-flow and momentum-conservative continuations, explicitly
not two solutions of the same fully specified weak theory.

R3: Numerical discriminator. First-order Rusanov finite volume in (q,v) and
(q,m=qv), periodic simple-wave data above, N=256,512,1024,2048; CFL=0.4.
Before breaking: compare at t=0.3 with the exact characteristic solution;
errors should decrease on refinement. After breaking: t=1.5, compare density,
charge, integrated momentum, energy, and gravity-source primitive. Use exact
symmetric-collision Riemann branches at gamma=1,q0=1,U=1 as independent
jump checks, and U=0.01,0.1,1,10 to distinguish weak/strong shock effects.
Floating RH identities tolerance 1e-10 times state/flux scale; symbolic
identities exact. Charge conservation tolerance 1e-10. Report convergence
numbers rather than assert continuum uniqueness from a finite ladder.
Controls: reversed/compressive-wave derivative must change predicted breaking;
wrong pressure coefficient must violate the momentum jump check. No original
physical canonical/alt inputs are pooled; these dimensionless local tests do
not regrade either footing.

## Interpretation
- Smooth positive-charge breakdown in the reduced equations disproves smooth
  globality there, not the full covariant Cauchy problem.
- Incompatible jump conditions exclude only the stated finite-jump/no-defect
  continuation. Distributional defects, unresolved oscillations, full scalar
  corrections and higher derivatives remain explicit possible continuations.
- Different conservative-variable solvers establish a continuation ambiguity
  of smooth equations, not nonuniqueness after fixing a weak formulation.
- Do not inherit X14's claim that every completion needs a new constant.
- Needs completion (scoped): as-used PN equations do not supply a demonstrated
  physically conservative post-break prescription; further physics or a
  derived weak-solution rule is required. Full-action failure needs a controlled
  counterexample or independent obstruction within its exact domain.

## Execution and evidence
Use bounded, single-thread local runs, hashes and computation-audit manifests.
Record script, contract, input revision, libraries, output and mutation tests.
No downloads, deposits, heavy queue jobs, parameter adoption or shared edits.
Independent review not authorized separately; self-review explicitly labelled.
