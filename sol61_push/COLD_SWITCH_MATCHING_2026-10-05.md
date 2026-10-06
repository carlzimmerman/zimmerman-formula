# Necessary matching between a conserved cold halo and a phantom switch

Coordinator derivation during the three-lane campaign. This is an algebraic
matching condition, not an action or a successful halo model.

Let F(r) be a fixed physical cold enclosed mass, P(r) the unsuppressed phantom
enclosed mass of a specified baryon law, and assume F,P >= 0. In a spherical
effective force dictionary, suppose the dark contribution is F+W P. To match
the **radial** max prescription exactly,

    F(r) + W(r) P(r) = max(F(r), P(r)),

the switch is uniquely determined at P>0:

    W(r) = max(0, 1 - F(r)/P(r)).

At P=0 the identity leaves W undetermined; setting W=0 is a convention, not a
consequence of the equality. Then 0<=W<=1. Keeping F fixed avoids the alternative
identification Mc=[F-P]_+, which cannot be a nonnegative material density where
its enclosed mass decreases. This alternative changes the mechanism: the
MOND response is suppressed by the cold budget, rather than consuming physical
cold mass. It applies only to this force-level decomposition, not automatically
to a gated Lagrangian or the historical edge-only mass prescription.

If F and P are nondecreasing, max(F,P) is nondecreasing and admits a
nonnegative total effective density in the distributional sense. Its phantom
piece [P-F]_+ can have negative radial derivative; effective response density
is not thereby material density. At a crossing there may be a density jump,
but the enclosed mass is continuous for continuous F,P.

## Why this is not already a derived switch

Multiplying a gravitational action term B by a field-dependent W adds

    delta(W B) = W delta B + B delta W.

A field equation obtained by multiplying the old response by W omits the
second term. Here W depends on both cold and baryon configurations through
cumulative F/P, so that missing term includes source reaction and a nonlocal
functional derivative. Inserting the force-level identity after variation
does not construct the required conserved action. A smooth approximation to
max additionally changes the exact matching condition.

The main-theory and cold-component lanes therefore meet at a concrete next
arrow: construct and vary a cold-responsive action whose solved force law has
this suppression, or show that another positive-density assembly mechanism
produces the required observations without the radial max. Formation labels
alone do not establish it. The 32pi lane must then evaluate its coefficient
for that same action; an integral from an ungated reduction cannot be silently
transferred to it.

This statement neither fixes abundance nor identifies the cold field, and does
not imply that all interpretations of T5 are impossible. In particular,
matching a single outer radius leaves freedom in the inner profile.
