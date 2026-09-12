# The no-event floor: exact scope and application to L191

This is a model-specific consequence of ordinary probability, not a newly
discovered universal gravity law. It audits Claude's `9b97161a6` L191 result
without changing kick strength, event count, force, or a gate threshold.

## Derivation

Let `Z` be initial phase-space data with probability measure `mu`, `F0(Z)` the
unkicked flow to the measurement time, and `A>=0` any nonnegative measurement
weight (enclosed mass, annulus mass, or a time average). The potential and
boundary rule are prescribed and identical for the no-event and control
trajectories. Initial data and the Poisson event count `N` are independent,
with a common integrated rate `n`. Assume
`0<M0=E[A(F0(Z))]<infinity` and a finite expected hit-population
measurement weight. Finite-mass aperture measurements satisfy these
integrability assumptions; extended-real ratios are not considered here.

Conditioning on the zero-event subset gives

\[
 M_{\rm kick}=P(N=0)M_0+M_{N\ge1},\qquad M_{N\ge1}\ge0.
\]

Since `P(N=0)=exp(-n)`,

\[
 \boxed{f_{\rm ret}\equiv\frac{M_{\rm kick}}{M_0}
        =e^{-n}+(1-e^{-n})r_{\rm hit}\ge e^{-n}.}
\]

For n>0, `r_hit` is conditional mean hit-population weight divided by `M0`;
at n=0 define it as zero. It is
nonnegative but need not be below one for a local aperture: influx can add
mass. At `n>0`, equality holds if and only if the hit-population contribution
to that aperture vanishes. Thus `f=exp(-n)` is a *cleared-hit-population limit*,
not universal retention at every mass or radius. Two hosts can differ through
their surviving/returning hit populations even at a common event count.

The statement is about expectations, not ratios from independent finite
Monte Carlo realizations. Estimated ratios may lie below the expectation
floor because the no-event subset and independently sampled denominator are
noisy. Initial equilibrium is not required for the theorem, only the common
control evolution and stated independence.

## Original spiral gate

L191's selected event count is `n=2`, so the lower bound is approximately
`0.1353352832`. The original L189 spiral ceiling is `0.105=21/200`.
Consequently **no increase in kick velocity can make the n=2 fixed-potential
model meet that original ceiling in expectation**.

The necessary mean is instead

\[
 n\ge-\log(0.105)\simeq2.25379.
\]

This is a necessary bound, not a suggested refit or a sufficient condition.
The `PoissonFloor.lean` certificate proves the mixture lower bound and the
strict numerical inequality `exp(-2)>21/200` using Mathlib's proved
exponential bounds—not a supplied decimal assumption. It also proves that
the n=2 mixture cannot meet the original ceiling for any nonnegative hit
contribution. The Poisson law, measure decomposition, independence, and flow
correspondence are derived above, but not formalized in this Lean file.

L191's later relaxed spiral test uses `0.105*1.35=0.14175`; its stored value
`0.1281275` passes that relaxed point-estimate test, not the original ceiling.
The simulation result and exact floor are therefore not contradictory.

## How a genuinely coupled theory could escape the bound

The factorization fails if kicks alter the field experienced by unhit matter
through self-gravity or a shared clock response. Then the no-event trajectories
in the perturbed system need not equal the no-kick control. It also changes
if the integrated rate depends on initial position, velocity or history.
These are explicit possible mechanisms, not proof they work: the common field
and rate must be derived from an action, and the no-event population followed
through the modified field. This is the next test worth doing, instead of
harder kicks in another fixed-potential fit.

An absorbing boundary with an identical prescribed rule does not alone evade
the bound. An action-derived, coupled field can alter it; a phenomenological
removal of the unhit population cannot be called a derived escape.

## Prior work and attribution

Nadler and Benson, *Semianalytic model for decaying dark matter halos*,
Phys. Rev. D 111, 103522 (published 15 May 2025), write the corresponding
undecayed-plus-retained-daughter decomposition in equation (12), with
`f_d=1-exp(-t/tau)`. Their equations (10)-(11) retain the angular kick term.
This overlaps the basic mechanism and accounting; it does not derive C003's
clock trigger or its action. [Published primary PDF](https://journals.aps.org/prd/pdf/10.1103/PhysRevD.111.103522).

Source checked 2026-09-12 against the published PDF, pages 103522-3 and
103522-4. Cache lookup by exact DOI found no existing local cache; no PDF was
stored or new cache initialized. Search terms were “decaying dark matter
un-decayed fraction halo recoil exponential decay Peter 2010” and “decaying
dark matter heating halo escape velocity lifetime retained fraction”, through
web discovery, then primary APS verification. Classification: known mixture
accounting after notation translation; the aperture/Poisson argument is a
formal consequence under the extra common-flow hypotheses above. No global
novelty claim is supported or intended.
