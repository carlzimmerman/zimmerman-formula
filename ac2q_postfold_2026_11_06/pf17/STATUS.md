# PF17: native source variation established; total variation still open

Base 7e341e6a08. The requested full dynamical theorem is not proved. This
phase removes the source-variation sub-obligation in a specified continuous
BV subclass; it does not remove the native absolute-value transport obligation.

## Established new results

For an existing on-branch solution with continuous spacetime BV clock gradient,
jointly Lipschitz auxiliaries, regular metric, controlled compact margins and
periodic inverse positivity:

- Exterior differentiation of the auxiliary one-form constraints gives spatial
  BV rates without first multiplying unknown rates by singular clock derivatives.
- The measure-forced periodic inverse bounds the rates and their spatial
  variation by C(1+Z). The actual Riemann source and acceleration contribution
  have slice measure norm at most C(1+Z)^2. The regular rolling potential is
  included with explicit bounded corrections.
- The source's slice Cantor component is a bounded homogeneous linear
  combination of the clock's Cantor gradients. This supplies no independent
  singular source, but is not a closed evolution equation for Cantor mass.

See SOURCE_VARIATION.md and CANTOR_SOURCE.md. The continuous-p hypothesis is
stronger than jump-free BV and is not a propagated conclusion.

## What the attempted TV and uniqueness routes found

The signed gradient equation plus a bounded-variation source still does not
justify its absolute-value inequality. GRADIENT_COUNTERTEST.md explicitly
shows nonzero continuous W1,1 potential/gradient evolution from zero data
for a prescribed continuous BV velocity, with zero source. This refutes the
automatic-gradient-Kato shortcut, not AC2q uniqueness.

Smoothing a continuous BV balance makes its scalar residual small in L1,
but differentiating that residual for a TV bound loses the smoothing scale.
No uniform native TV estimate follows from this argument. The checked
Bressan–De Lellis autonomous uniqueness theorem presupposes a different
closed system and its small-TV semigroup domain; native applicability is
not established. See SMOOTHING_AND_UNIQUENESS.md.

Thus the precise unresolved inequality is still a native version of

    Z(t) <= Z(0)+C integral_0^t (1+Z(s))^2 ds,

or an interaction-functional substitute strong enough for compactness.
Its source side is now justified within the declared class; its transport
side is not. Even this estimate would still require a full approximation
construction retaining all Einstein equations and a coupled comparison
estimate to establish existence and uniqueness.

## Scientific verdict

No continuous or Cantor native continuation has been constructed, excluded
universally, or shown uniquely selected from the breaking incoming solution.
No same-data pair of full native solutions has been produced. A physical
extension is therefore not proved necessary, and survival as a predictive
postbreak theory is not proved either.

R1 is resolved conditionally in the continuous-clock subclass. R2 remains
open: the automatic sign argument is ruled out; a specifically native
renormalization/interaction argument is deferred. R3 remains open: the
smoothing test and exact autonomous-theorem check do not supply the missing
native solution process. No regularizer, extra field, or entropy rule was
adopted. These deferred routes need a new native estimate or construction,
not another invocation of the already justified source bound.

Independent proof checks are in review/SOURCE_AUDIT.md. The exact source
inspection and smoothing calculation are recorded separately; they are not
claimed as a new external theorem. No numerical experiment was needed.
