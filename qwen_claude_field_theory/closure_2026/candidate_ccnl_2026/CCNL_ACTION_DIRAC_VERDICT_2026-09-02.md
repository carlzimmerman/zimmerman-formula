# CCNL action/Dirac verdict — 2026-09-02

## Status

**Exact exponential constitutive law: PASS. Ordinary localized CCNL action:
DEAD for the strict fried-chicken target. Global nonlocal existence question:
OPEN.**

The candidate tested is

\[
S=\int d^4x\sqrt{-g}\left\{
{c^4\over16\pi G}[R+a_0^2f(Z)]
+{K(Q)\over8\pi\widetilde G}
+\xi(\Box X-R_{\mu\nu}u^\mu u^\nu)
\right\}+S_m[g,\psi],
\]

with

\[
Z={4c^4\over a_0^2}\nabla_\mu X\nabla^\mu X,
\qquad
f_+(Z)=4-2(\sqrt Z+2)e^{-\sqrt Z/2}.
\]

The executable audit is `ccnl_action_dirac_audit_2026.py`, with regressions in
`test_ccnl_action_dirac_audit_2026.py`.

## What survives

Direct differentiation gives

\[
1-2f_+'(4y^2)=1-e^{-y}.
\]

The deep-MOND and Newtonian limits are exact. This part of the candidate is a
real construction result, not an assigned output.

## Decisive ordinary-action obstruction

After integrating the multiplier term by parts, the local auxiliary principal
kinetic block has the general form

\[
L_{\rm kin}={A\over2}\dot X^2+b\dot X\dot\xi,
\qquad
W=\begin{pmatrix}A&b\\b&0\end{pmatrix}.
\]

The audit calculates

\[
\det W=-b^2,
\qquad
\operatorname{rank}W=2.
\]

For the displayed CCNL normalization,

\[
A(y)=-8f_+'(4y^2)=-4e^{-y},\qquad b=1,
\]

so

\[
\boxed{W_{\rm CCNL}(y)=
\begin{pmatrix}-4e^{-y}&1\\1&0\end{pmatrix},
\quad \det W_{\rm CCNL}=-1}
\]

for every finite acceleration and also in the limiting regimes. The two
kinetic eigenvalues have product `-1`, hence opposite signs.

The Legendre map is explicitly inverted. It generates:

- no primary auxiliary constraint;
- no secondary auxiliary constraint;
- an empty `0 x 0` auxiliary Poisson-bracket matrix;
- zero first-class and zero second-class auxiliary constraints; and
- two auxiliary configuration degrees of freedom, one with negative kinetic
  sign.

The count is unchanged in the `k=0` and `k!=0` sectors.

Including the homogeneous scale-factor velocity does not restore degeneracy.
For the integrated FLRW principal block on
`(a_dot, X_dot, xi_dot)`, the audit obtains

\[
\det W_{\rm FLRW}
=12a^7\left(1+\xi_{\rm bg}+3e^{-y}\right).
\]

On the candidate branch \(\xi_{\rm bg}=0\), this is strictly positive and the
block has rank three for every finite \(y\). Thus mixing with the homogeneous
metric mode does not convert the regular auxiliary pair into constraints.

Choosing null/retarded initial values selects one history from this regular
Cauchy problem. It does not turn the four auxiliary initial data into
equal-time Dirac constraints. A numerical integration which starts with those
values and remains on the selected solution therefore demonstrates uniqueness
of that chosen solution, not removal of the other phase-space solutions.

## Source translation: the DW transport constant

The checked primary source is Deffayet and Woodard, *A Nonlocal Realization of
MOND that Interpolates from Cosmology to Gravitationally Bound Systems*,
arXiv:2512.10513v2, JCAP 04 (2026) 081, checked 2026-09-02.

Their equation (33) implies, along a flow tube,

\[
n(\mathcal M+f)=n_0(\mathcal M_0+f_0).
\]

Therefore the proposed initial condition \(\mathcal M_0=0\) gives

\[
\boxed{\mathcal M=-f+{n_0\over n}f_0},
\]

not \(\mathcal M=-f\) generically. Exact equality additionally requires
\(f_0=0\), or the different initial condition
\(\mathcal M_0=-f_0\). The paper itself describes the bound-system relation as
an approximate regime, not this new exact identity.

## Other unresolved strict gates

The full spatial variation contains the trace-free source

\[
f'(Z)\left(\partial_iX\partial_jX
-{\delta_{ij}\over3}|\nabla X|^2\right),
\]

whose squared norm for a nonzero gradient is

\[
{2\over3}f'(Z)^2|\nabla X|^4>0.
\]

It is weak-field second order, so it need not spoil linear `gamma=1`, but it
means exact nonlinear `Phi=Psi` has not been derived.

Likewise, Solar-System suppression estimates do not produce `beta` or
`alpha_1`, `alpha_2`, `alpha_3`. Those require the full boosted metric,
auxiliary backreaction, matter solution, and standard PPN gauge map.

Finally, the odd negative-`Z` continuation used for cosmology satisfies

\[
f(0^-)=f(0^+)=0,\qquad f'(0^-)=f'(0^+)=\tfrac12,
\]

but

\[
f''(0^-) = +\infty,\qquad f''(0^+)=-\infty.
\]

It is `C1` but not `C2` at the zero-field transition, so a controlled nonlinear
crossing prescription is still owed.

## Exact scope

This result kills CCNL **as the displayed ordinary localized action** under the
strict ban on hidden propagating auxiliary scalars and ghosts. It does not
exclude a genuinely nonlocal Schwinger-Keldysh/in-in construction whose
physical phase space, unitarity, causal variation, and PPN metric are derived
without treating retarded history data as canonical constraints. No such
completed construction is presently in the repository.
