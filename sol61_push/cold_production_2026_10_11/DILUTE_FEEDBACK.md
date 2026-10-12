# Stimulated and inverse feedback in the 1 MeV decay example

2026-10-11. The previous turn found a dilute parameter regime of the same
positive-square action. This turn tests the two feedback mechanisms that
were problematic for the lighter, highly occupied shell. Results are
conditional on a prescribed exponential source amplitude and the stated
kinetic treatment; they are not a full source-plus-field evolution.

## A uniform occupation bound including stimulated pair production

Set tau=Gamma*t, r=Omega/Gamma, and d=Delta/Gamma. In the interaction picture,
the exact two-mode Bogoliubov equations for the prescribed pump are

    alpha'=-i r exp(-tau/2) exp(+i d tau) beta,
    beta'=+i r exp(-tau/2) exp(-i d tau) alpha,
    alpha(0)=1, beta(0)=0.

They preserve |alpha|²-|beta|²=1. Hence

    d asinh(|beta|)/d tau <= r exp(-tau/2),
    |beta(tau)|² <= sinh²[2r(1-exp(-tau/2))] <= sinh²(2r).

The differential inequality is understood through the usual absolute-value
bound at zeros. It applies to every detuning in this prescribed-pump model;
it is not an inference from sampling four detunings. At d=0, the bound is
saturated exactly. For the saved 1 MeV candidate,

    sinh²(2r)=2.8604440853e-5.

This improves the previous Born triangle-inequality bound 1.1442e-4 and
retains stimulation. A gross two-daughter Bose decay factor (1+f1)(1+f2)
can then exceed unity by at most 5.72097e-5 if both occupations obey the bound.
The calculation does not separately evolve the source amplitude: prescribing
its vacuum exponential is the approximation being checked, not a conclusion
of these two-mode equations.

Numerical integration at d=0,0.5,2,10 through tau=30 agrees with the exact
resonant solution and preserves Bogoliubov normalization to 5e-15. The largest
occupation correction relative to the Born peak across these samples is
9.535e-6, at resonance. Small sampled corrections support the analytic
uniform bound; they are not a uniform relative-error bound in the far tails.

## An integrable occupation envelope

An occupation bound alone is insufficient to bound the integrated inverse
rate over infinitely many modes. Integration by parts in the beta integral,
using |alpha|<=cosh(2r) and |alpha'|<=r exp(-tau/2)sinh(2r), gives

    f(Delta,tau) <= f_peak C²/[1+4Delta²/Gamma²],
    f_peak=4r²,
    C=1+cosh(2r)+r sinh(2r)=2.0000286043.

For a retained daughter line |2Delta/Gamma|<=L with L=1000, its energy integral
therefore satisfies

    I=integral_line f(e) de <= f_peak C² (Gamma/2) atan(L).

This is a bound for the prescribed-pump spectral model over the declared
line. It does not extend the constant-matrix-element model to arbitrary
ultraviolet energy or bound physical off-resonant preparation tails.

## Inverse source formation: a useful exact phase-space cancellation

For uncorrelated isotropic daughter occupations and initially empty
incoherent source modes, the earlier exact decay kinematics give source gain
Gamma_lab times the angular average of f1*f2. Write

    P=sqrt[e_b(2M+e_b)], p_star=sqrt(M²-4m²)/2,
    g_b=P(M+e_b)/(2pi²), b=P*p_star/M,
    Gamma_lab=Gamma_vac*M/(M+e_b).

Then g_b*Gamma_lab/(2b)=Gamma_vac*M²/(4pi²*p_star), independent of recoil.
Changing variables from (e_b,e1) to (e1,e2), and enlarging the kinematically
allowed integration region to the entire retained line squared, gives

    R_inverse <= Gamma_vac [M²/(4pi²*p_star)] I².

This is a conservative upper bound, not a numerical estimate from a singular
bare elastic resonance. Normalize twice this rate by the initial daughter
charge density and by Gamma_vac. The resulting bound is

    inverse charge fraction per vacuum lifetime <= 1.22577e-8

for line-contained daughters obeying the envelope. With that same envelope
maintained, integrating over ten lifetimes gives at most 1.22577e-7 of initial
charge through these inverse reactions. This is only a short-time feedback
screen, not a lifetime-integrated cosmological bound.

A complementary comparison bound for an initially empty incoherent source
mode with daughter occupations <=f_max is B<=f_max²=8.18214e-10 under the
corresponding gain-loss equation. It does not apply to the original prepared
coherent source itself.

## What the bounds do and do not resolve

These checks support weak stimulated corrections and weak *uncorrelated,
line-contained* inverse feedback during the short dilute decay episode.
They differ sharply from the dense 193.5 eV example. They do not bound connected
source-pair memory: a daughter pair produced from a source is correlated, and
its coherent return is part of the full decay problem, not an independent
f1*f2 collision. The assumed vacuum exponential also omits threshold-memory
and preparation effects. Gamma/(M-2m)=8.54e-6 is a useful scale separation,
not a proof that all such corrections are negligible.

The line cutoff and outside-line contributions must remain explicit in any
full calculation. The previous narrow-line number integral misses about
0.064% at L=1000 asymptotically under its own constant-DOS approximation;
that number fraction does not by itself bound an arbitrary physical tail's
inverse rate. Neither report supplies a renormalized, fully self-consistent
quantum evolution.

`dilute_feedback.py` passes 22 checks covering the exact resonant solution,
normalization, analytic occupation and spectral bounds, boosted phase-space
cancellation and feedback scales. Its manifest validates recorded provenance.
All changes are in the existing cold-production research folder.

The dilute branch is now a better-supported conditional preparation route
than the densely occupied shell. The next missing production calculation is
self-consistent source decay with its continuum memory and preparation
specified, or a controlled error bound justifying the exponential reduction.
Cosmological evolution and the repo's halo/acceleration selector are still
separate, unresolved obligations.
