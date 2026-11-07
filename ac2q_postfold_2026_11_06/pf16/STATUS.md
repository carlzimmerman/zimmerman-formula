# PF16: native dynamical regularity — partial results, target open

Research base: 1009c50a76 (PF15). No numerical evolution, regularizer, new
physical operator, or manuscript claim was added.

## What changed

1. The actual bounded on-branch BV equations force a continuous representative
   that is absolutely continuous in time in spatial L1. Its modulus is bounded
   by the time integral of slice variation. Uniform slice variation gives
   L1-Lipschitz time evolution. Consequently temporal derivative mass cannot
   concentrate on a null set of times crossed with the spatial circle.
   See CONDITIONAL_TIME_CONTROL.md. This is conditional on an existing native
   weak solution and its auxiliary/geometry bounds, not their propagation.
2. A positive density depending on r,theta and other variables with bounded
   frame derivatives cannot universally cancel acoustic compression: the
   cancellation conditions imply 2 A_q rho=0, whereas A_q>0. See
   ACOUSTIC_DENSITY.md. Nonlocal densities and uncontrolled derivative-variable
   dependence are outside this obstruction.
3. The conservative Riemann-gradient identity has a canonical diffuse BV
   interpretation via a curl cancellation. Its signed-measure identity does
   not itself propagate total variation. A source-variation bound and a native
   renormalization estimate remain unproved. See GRADIENT_BALANCE.md and the
   independent acoustic-density audit.

## Verdict against the requested target

The dynamical existence/uniqueness theorem is NOT established. Continuous
non-Lipschitz and spatial Cantor-type native continuations have neither been
constructed nor ruled out. Their time projection must obey the new regularity
condition, but this allows moving spatial Cantor measures. There is no native
same-incoming-data pair proving nonuniqueness and no universal nonexistence
result forcing an extension. AC2q is not yet demonstrated predictive beyond
breakdown; the missing proof cannot be converted into a claim of new physics.

## Route accounting and resumption

R1 local positive-density cancellation: excluded in its precise local-state
class. A nonlocal density would require a new bounded, positive construction
and is deferred; the broader transport route remains open.
R2 signed gradient balance: the diffuse conservative identity survives.
The attempted automatic absolute-value extension is invalid as a general
transport principle, as the explicit non-native signed-measure countertest
shows. Native source-variation/renormalization remains open, not refuted.
R3 temporal regularity: a conditional a priori theorem is proved; this rules
out a time-only singular activation mechanism inside the declared class.
It supplies no uniform outgoing bounds or comparison estimate between two
solutions. Full weak existence and uniqueness remain open.

Next substantive work must either derive a native source-variation and
renormalization/interaction estimate with uniform outgoing bounds, or construct
full constraint-compatible weak approximations and prove convergence/selection.
Reusing the smooth Riccati square, assuming the variation estimate at the
singularity, or treating bounded source as a source-difference estimate would
repeat known gaps. A full-switch or singular-metric extension of the weak
class needs separately specified equations and admissibility, not an implicit
change to this theorem's hypotheses.

Independent analytic audits are in review/. Hashes in PROOF_INDEX.json identify
revisions, not proof certificates. No external transport theorem is invoked
as a load-bearing step in PF16.
