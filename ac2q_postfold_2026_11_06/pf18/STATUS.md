# PF18: conditional absolute-variation theorem; native closure still open

Base 191cfbc063. The requested unconditional transport estimate and full weak
existence/uniqueness theorem have not been proved.

## What was derived

The native integrating factor removes the opposite-family contribution to
acoustic divergence, leaving rho A_q W_sigma. Genuine self-compression remains;
its sign and singular part cannot be discarded. See NATIVE_WEIGHT.md.

In a C1 clock chart the exact signed wave equation is

    partial_tau mu_sigma+partial_x(lambda_sigma mu_sigma)=q_sigma,
    q_sigma=D_x(F_sigma/r)+(l R_base/(2r))dx.

PF17 controls the source norm by C(1+Z)^2. A checked signed-measure transport
theorem now gives an actual conditional estimate

    Z(t)<=Z(0)+C integral_0^t(1+Z(s))^2 ds

if the actual speeds obey a quantitative two-sided Osgood modulus with
integrable time coefficient, the wave masses are uniformly finite, and the
sources are integrable in measure norm. The proof uses forced flow
representation, not an unjustified sign test. See CONDITIONAL_TRANSPORT.md.
This permits certain non-Lipschitz speeds but does not cover arbitrary
continuous or Holder speeds. These are extra unproved dynamical hypotheses,
not new rules imposed on the action.

## Why this does not close the native theorem

The native constraints admit smooth bounded-TV cusp approximants whose
acoustic speeds have no uniform Osgood modulus. All auxiliary and initial
Einstein constraints are satisfied member by member. Thus the required
modulus does not follow from the established slice bounds. This does not
construct a nonsmooth spacetime continuation or disprove a further dynamical
regularization mechanism. See MODULUS_TEST.md.

Even when the conditional transport theorem applies to each proposed solution,
it only gives uniqueness for fixed speed and source. Comparing two coupled
solutions introduces the derivative of a speed-difference times a wave
measure, which need not be a measure source. No coupled comparison theorem
follows from the individual estimates. See COUPLED_COMPARISON.md.

## Verdict

AC2q has not been shown to uniquely continue through breakdown. Nor has a
native nonexistence or same-data nonuniqueness result proved that an extension
is necessary. Cantor continuations remain unconstructed and not universally
excluded. The conditional TV bound controls mass, not its singularity type.
No viscosity, entropy selection, new field or extra operator was adopted.

## Route status and next obligations

R1: opposite-family cancellation proved; it leaves native self-compression.
R2: conditional signed-measure transport estimate proved under the stated
Osgood and measure-class assumptions; its native dynamical hypotheses are open.
R3: deriving a uniform Osgood modulus from the established slice bounds is
ruled out by the cusp family. A time-integrable dynamical modulus, a genuinely
native interaction estimate avoiding that modulus, and a full weak
approximation/comparison construction remain open and deferred.

Future work must add an actual dynamical estimate or construction at those
steps. Reapplying the fixed-speed theorem without proving its hypotheses,
or applying it separately to two different native speeds, would not advance
the unresolved target. Independent review is in review/TRANSPORT_AUDIT.md.
No numerical experiment or physical extension was used.
