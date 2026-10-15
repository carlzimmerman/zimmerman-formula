# The retained electric law has no submetric parity-even single-gauge Lorentz vacuum

VC3-L-001, 15 October 2026. This excludes one specified vacuum completion,
not every action, every phase boundary or the physical theory. The occupied
current medium has additional frame variables and is outside the hypotheses.

## Exact hypothesis and transverse mode

Use signature -+++, c=1 and a derivative-free, parity-even local gauge action
`L(S,P)`, with `S=(|E|^2-|B|^2)/2`, `P=E dot B`, and `L(S,P)=L(S,-P)`.
Assume it is twice differentiable about the nonzero purely electric background
under consideration and has precisely the retained electric restriction

\[
 L(E^2/2,0)=L_e(E)=D_0 E-D_0^2\log(1+E/D_0),\quad E>0,\quad D_0>0.
\]

Thus

\[
 D=L_e'=\frac{E}{1+E/D_0},\quad
 t=L_S=\frac DE=\frac1{1+E/D_0},\quad
 p=L_e''=\frac1{(1+E/D_0)^2}=t^2.
\]

Take a constant background `E=E zhat,B=0` and wavevector in the x direction.
In temporal gauge use the physical perturbation `A_z=a(t,x)` with other
perturbation components zero. Then `e_z=-a_t`, `b_y=-a_x`; its pseudoscalar
P is zero along the path. To quadratic order,

\[
 L_2={1\over2}p a_t^2-{1\over2}t a_x^2.                 \tag{1}
\]

Parity evenness gives `L_P=L_SP=0` on P=0, so this is an invariant polarization
of the full linearized equations, rather than a restricted trial that sources
an omitted mode. An arbitrary `L_PP` acts on the other polarization. The
linear Gauss constraint is satisfied: the perturbed displacement is along z
and has no z dependence. Residual gauge transformations cannot remove its
nonzero field strength.

The wave equation is `p a_tt-t a_xx=0`. Its constant-coefficient characteristic
speed is therefore

\[
 \boxed{\quad v^2={t\over p}=1+{E\over D_0}>1\quad(E>0).\quad}    \tag{2}
\]

Both kinetic and gradient coefficients are positive. This is a failure of
the imposed metric-cone condition, not a negative-energy/ghost calculation.
The conclusion is local on every such background, independent of L_PP or
how one extends L to magnetically dominated fields.

## A general differential obstruction, not just this rational law

For any positive electric response `D(E)>0` with `D'(E)>0`, the same mode has
`v^2=D/[E D']`. Requiring v<=1 at all E in an interval is equivalent to

\[
 E D'\ge D,\qquad \frac d{dE}(D/E)\ge0.                \tag{3}
\]

The retained law has decreasing `D/E` at every positive field. In particular,
a Lorentz vacuum with Maxwell limit `D/E->1` at zero and condition (3)
cannot rejoin the unchanged retained law `D/E<1` at any positive field while
keeping the condition throughout the interval. A smooth low-field change
alone cannot remove this obstruction if the exact law is restored at a
higher electric field within the same single-gauge Lorentz phase.

There is also a conditional invariant-regularity obstruction. The electric
restriction fixes

\[
 L_{SS}(E^2/2,0)={p-t\over E^2}
 =-{D_0\over E(D_0+E)^2}.
\]

It diverges negatively as E->0. Thus no extension that is C2 in the invariants
(S,P) on an open neighborhood of (0,0) can have this restriction at all small
positive S. This invariant statement is distinct from the fact that the
occupied electric function is C2 in Cartesian electric components at zero.
No stronger regularity conclusion about all conceivable field formulations
is inferred from this observation.

## Scope and allowed continuations

A Maxwell exterior has a different electric law `D=E`, and is not excluded.
It needs an actual matching surface, any surface charge/current and stress
accounting. A Lorentz-breaking medium/independent frame, additional physical
fields, derivative terms or a changed electric law also leave the hypotheses;
those additions need their own constraints and health calculation. This proof
does not settle them or identify their microscopic origin. It gives no claim
about ultraviolet completion or global chronology from a truncated effective
phase speed alone.

The first-order static mapping between the frozen scalar/vector action and
this current model must likewise be derived explicitly; a shared static
antiderivative does not identify their dynamics.

## Independent check and literature scope

The calculation above is self-contained. The standard invariant definitions
and quadratic expansion were checked against Russo and Townsend,
[arXiv:2211.10689v3](https://arxiv.org/html/2211.10689v3), equations (1.1)--(1.5).
The source is context and a convention check, not a substitute for deriving
(1)--(3). No no-birefringence classification is assumed here. The bounded
literature search and exact checks are recorded separately.
