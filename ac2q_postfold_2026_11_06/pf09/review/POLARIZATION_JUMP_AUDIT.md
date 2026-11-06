# Independent audit: bounded polarization-jump defects

**Verdict: proved in the candidate's restricted bounded-layer class,
with proper normalization and trace assumptions explicit below.** The
argument does not require continuous P, but it does require more than
uniform convergence of phi and bounded field amplitudes alone.

For bounded r,A,P, unit-clock rapidity and cap-separated constitutive
sources, the only possible surface term in the on-shell Hilbert stress
is

    S_ab=-weaklimit(mu Q n_a n_b), Q=1 on mu support.

The normal component is nonpositive. A no-dipole stress balance gives
S_NN=0, hence n.N=0 on multiplier mass in the measure-weighted sense.
This fixes the singular stress to negative-energy dust tangent to the
clock; it supplies no independent arbitrary pressure.

Bounded e(A)=W_P/r on controlled crossing clock slices gives a common
layer A value only with the appropriate regular outer trace anchoring.
Require strong common outer A traces (or directly common A convergence
on multiplier mass), and regular crossing geometry. Let s=T(phi)>0
be the derivative along the **unit** future tangent of the interface.
If coordinate time is used instead, its lapse conversion must be included.

With the explicitly assumed multiplier-weighted convergence of this
tangential derivative, n.N=0 gives r=s on multiplier mass. For nonzero
mass, Ar=1 therefore forces A_star=1/s. Outer clock kinematics gives
r_out<=s, whereas Q_out=A_star r_out>=1. Thus Q_out=1 and r_out=s on
both sides. Such a defect cannot connect strictly on-branch Q>1 endpoint
states. Rapid correlations of a nonconvergent tangential clock derivative
with mu remain excluded by hypothesis, not by this algebra.

## Open-off/open-off endpoints

If Q=1 in one-sided open neighborhoods, A=1/r and e(A)=W_P/r give
a=e(log r)=-W_P at each endpoint. Merely Q=1 at an isolated switching
trace would not justify differentiating it this way.

With bounded regular metric derivatives and the dust orientation above,
bounded r^2 and transverse terms carry no delta, so mu_surface=-[P]
for a downward jump, using a consistently oriented proper normal. The
Einstein normal and transverse equations give

    [E]=mu_surface/(2M), [a]=mu_surface/(2M).

The first follows from the singular part T_nn=-2M e(E); the second
from zero transverse surface stress, equivalently [E]-[a]=0. Thus

    [W_P]=[P]/(2M).

The native normalization is essential and was checked directly:
`action_search_2026_11_05/AC2_single_clock/ACTION.md` defines
Khold=4 pi G and M=Mpl^2=1/(8 pi G) on lines 9–10.
`AC7_charge_switch/README.md` explicitly inherits AC2's definitions.
Hence Khold=1/(2M) is a native identity, not merely the M=1 numerical
fixture. Since

    W_PP=Khold/(1-Khold |P|/a0)^2>=Khold

with strict inequality except at the single point P=0, every distinct
finite-cap endpoint pair has a strictly greater secant slope. The required
equality is impossible unless [P]=0. The proposed native off/off defect
is therefore excluded.

As a boundary check, in a different normalization Khold<1/(2M), symmetric
endpoints +/-p with p=(a0/Khold)(1-2M Khold) satisfy the secant equality.
This is an algebraic counterexample to a generalized parameter-free claim,
not a native AC2q layer or a counterexample to the as-written normalization.

These exclusions assume pure multiplier stress: cap/source concentrations,
unbounded H or boosts, singular geometry, and unspecified nonlinear weak
products can invalidate that reduction. No pair of valid native singular
continuations or unique admissibility law is produced here.

Independent delegated audit, 2026-11-06, with direct inspection of the
native normalization sources and POLARIZATION_JUMP_ROUTE.md.
