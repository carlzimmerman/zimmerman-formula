# Energy limits how far rearrangement can reduce portal pressure

Status: an analytic bound on the softened interaction's mean pressure
functional at fixed mean intensity and a specified excess-energy budget.
It allows arbitrary intensity distributions. It is not a lower bound on
the full dynamical sound speed or on total instantaneous relativistic
stress, and is not a cosmological evolution calculation.

## A distribution-independent inequality

In units A_* S_0, write the local interaction energy and pressure as

    x=S/S_0 >= 0,
    u(x)=sqrt(1+x^2)-1,
    p(x)=1-1/sqrt(1+x^2).

Define the difference d=x-u(x). It lies in [0,1), and direct elimination
of x gives the exact relation

    p=f(d),    f(d)=d^2/(d^2-2d+2).

The function is monotone and convex on that interval:

    f'(d)=2d(2-d)/(d^2-2d+2)^2 >= 0,
    f''(d)=4(1-d)(2+2d-d^2)/(d^2-2d+2)^3 > 0.

Therefore Jensen's inequality gives, for any normalized spatial or
statistical average with finite mean x,

    <p> >= f(<d>) = f(<x>-<u>).

If <u> is bounded above by an available dimensionless energy E_*, then

    <p> >= f(max(0, <x>-E_*)).

A feasible budget automatically keeps <x>-E_* below one: u(x)>=x-1.
If E_*>=<x>, this bound becomes zero and provides no restriction. The
bound need not be sharp; the mean-x constraint contains additional
information not used by the Jensen step.

This explains why extreme clumping is not a free way to erase pressure.
At fixed mean x, concentrating the material into arbitrarily dense clumps
makes <u> approach <x>, because u becomes linear at high density. Such
rearrangement needs that energy budget. When E_* is smaller, a strictly
positive pressure floor remains regardless of the intensity distribution.

## Connection to the charged energy bound

On a fixed flat background, after subtracting the constant vacuum term,
the positive-square action satisfies

    D=E_material-mQ >= integral U(S) dV.

The added portal U is nonnegative, and all other terms in that completed-
square identity remain nonnegative. Thus a known upper bound on
D/(V A_* S_0) supplies E_* for the inequality. At leading NR order fixed
charge fixes mean S through the number normalization. In the exact
relativistic theory mean S is not identical to charge; the inequality
is conditional on its specified value and does not assume that exact
relativistic evolution conserves mean S.

Negative gravitational binding energy cannot be inserted into D while
retaining this flat-background argument. Expansion changes energy by
work, and boundaries can transport energy. The present inequality is
therefore a local constitutive/energy constraint with stated conditions,
not a claim that D is conserved through cosmological or halo evolution.

The pressure functional p is the NR interaction-pressure contribution
(or the corresponding interaction term in a virial decomposition).
Other kinetic, conversion, gradient and virial boundary terms are not
included. A positive bound on this term alone must not be called a bound
on the full instantaneous relativistic pressure tensor.

## Examples tied to the production sample

Rescale the saved endpoint intensity distribution to mean x=1. It has

    <u>=0.5059266840,
    <p>=0.2522973578.

For an illustrative NR energy budget, retain its source charge fraction
0.3638167932 and add the source rest-gap energy, but assume negligible
initial kinetic energy. In units A_* S_0, the gap adds 0.1445070938 at
mean x=1, giving the declared budget E_*=0.6504337778. The bound is then

    <p> >= 0.0858686153.

The inequality permits exchanging that nonnegative budget between the
portal, kinetic energy and source gap; it does not require a fixed final
source fraction. It only uses <u><=E_*. The illustrative budget is not a
verified upper bound on the actual evolving cosmological state: additional
kinetic energy or other terms must be included when applying the result
to that state. The theorem and the numerical budget example have different
levels of generality.

For comparison, rescaled sample examples give:

| Mean x | Initial portal pressure | Declared total excess budget | Pressure lower bound |
|---|---:|---:|---:|
| 0.1 | 0.0082131 | 0.0230236 | 0.0031995 |
| 1 | 0.2522974 | 0.6504338 | 0.0858686 |
| 10 | 0.8122100 | 10.5453027 | 0 |

All entries use the same A_* S_0 units. The high-density example illustrates
where this particular energy bound ceases to be informative.

## Homogenization also redistributes energy

At mean x=1, a uniform intensity has u=sqrt(2)-1=0.4142135624. Removing
the sample's fluctuations lowers interaction energy by 0.0917131216 per
A_* S_0. If the source fraction is held fixed and that energy becomes NR
kinetic energy in a closed box, the trace-averaged kinetic pressure rises
by two-thirds of the released energy. The resulting sum would be

    p_uniform+(2/3) energy_release=0.3540352999,

compared with the initial interaction pressure 0.2522973578. This is an
energy-accounting example, not a claim that the dynamics homogenizes the
field or keeps chemical composition fixed. Reactions could store some
energy as a rest gap, and transport could move it elsewhere. One cannot
remove the interaction energy from the accounting while also asserting
that the process is conservative.

## Verification and implication

portal_energy_pressure.py checks the exact pressure-deficit relation and
positive derivatives at rational parametrizations, then checks Jensen
bounds and convex homogenization energy on the saved empirical sample.
All 19 checks pass; the manifest validates provenance. The general proof
is the displayed monotonicity/convexity argument, not the finite checks.
The result and interpretation are self-reviewed.

The preceding turn held the fluctuation distribution fixed. This turn
shows that allowing its shape to change does not permit arbitrary loss of
portal pressure at a limited fixed-volume energy budget. It does not
supply the missing time-dependent stress closure: sound response depends
on how energy and correlations move during a perturbation. A successful
cold-energy construction must still evolve those quantities and derive
the repo's density and acceleration law. Those requirements remain open.
