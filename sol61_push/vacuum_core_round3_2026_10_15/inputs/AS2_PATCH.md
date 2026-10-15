# An occupied-phase magnetic response that repairs the zero-electric-field defect

AS2-PATCH-001, 15 October 2026. A **new specified constitutive candidate**, not a
property of the unchanged response audited in `../joint_audit/REPORT.md`.
This construction removes one nonlinear differentiability obstruction wherever
the neutral current is timelike and has positive density. It does not extend
the material frame to vacuum, prove nonlinear well-posedness or select a
microscopic magnetic response.

## Domain and inherited discriminator

Write `E=|E_U|`, `D0>0`, `t=(1+E/D0)^-1`, `p=t^2`, `x=1-t` and
`h=h_s(1-s_s^2)>0`. The material EOS is smooth on positive density and
`0<=s_s^2<1`. For the single neutral current the inherited local cone test is

\[
 F_E(\beta)=p-\beta-
 {E^2(t-\beta)^2\over h+E^2(t-\beta)}>0,
 \quad 0<\beta<t.                                      \tag{1}
\]

The old principal proof derives (1) for `E>0`; the zero-field case is checked
separately below. In this law `hcrit=E^2 x` exactly. On `h>hcrit`, define

\[
 \beta_L=p{h-h_{\rm crit}\over h-E^2(t-p)},\qquad
 \beta_P=\beta_L{h\over h+h_{\rm crit}}.
\]

For `E>0`, this is the old engineered response, with
`0<beta_P<beta_L<p<t` and `F_E(beta_P)>0`.
It has `beta_P=1-2E/D0+O(E^2)` at fixed positive density. Consequently the
old magnetic action includes `+|E_U| B_U^2/D0`, which is not differentiable
at zero electric vector with a nonzero magnetic field.

## Explicit smooth blending rule

Choose the density-dependent scale

\[
 a^2={D_0^2 h\over16(D_0^2+h)}>0.
\]

Let `0<=chi(s)<=1` be a smooth cutoff equal to one for `s<=1/4` and zero
for `s>=1`. An explicit choice is

\[
 j(z)=\begin{cases}e^{-1/z}&z>0,\\0&z\le0,\end{cases}\qquad
 \chi(s)={j(1-s)\over j(1-s)+j(s-1/4)}.
\]

The denominator is positive for every real s. For `E^2<=a^2/4`, define
`beta_new=1/4` directly, **without evaluating beta_P at zero**. Elsewhere on
`h>hcrit`, define

\[
 \boxed{\quad \beta_{\rm new}
 =\chi(E^2/a^2)\,{1\over4}
  +[1-\chi(E^2/a^2)]\,\beta_P.\quad}                    \tag{2}
\]

The constants one quarter, sixteen and the cutoff are chosen constitutive
inputs. They are not derived parameters or fits.

## Every blend point remains inside the same causal cone window

Where `chi>0`, one has `E<a`, hence

\[
 {E\over D_0}\le{1\over4},\quad
 {E^2\over h}\le{1\over16},\quad
 t\ge{4\over5},\quad p\ge{16\over25},\quad x\le{1\over5},\quad
 {h_{\rm crit}\over h}\le{1\over80}.
\]

In particular the parent response is defined throughout the nonzero-field
blend region. The constant-quarter response has `0<1/4<t` and

\[
 F_E(1/4)\ge {16\over25}-{1\over4}-{1\over16}
 ={131\over400}>0.                                    \tag{3}
\]

Here `0<t-1/4<1` and the denominator in (1) is at least h.
The sign of (1) is the sign of

\[
 N_E(\beta)=h(p-\beta)-E^2(t-\beta)(t-p),               \tag{4}
\]

since its denominator is positive. This numerator is affine in beta.
Both endpoints of (2) have positive numerator and lie in `(0,t)`, so their
convex blend does too. Where `chi=0`, the parent proof applies unchanged.
Thus the constructed response preserves the old sufficient all-angle
principal cone and positive-energy conditions on its stated occupied branch.
It does not weaken the inequality by testing only selected angles.

At `E=0`, (2) is locally the constant one quarter. The electric quadratic
Hessian is I, the frame mixing vanishes with the background E, and the
transverse gauge speed squared is one quarter. The material sound speed
remains its EOS value below one. This direct limit avoids the undefined
background field direction in the old `E>0` notation.

## Regularity and what this repair does not establish

At each positive density, a is positive and smooth. Equation (2) is exactly
constant in an open neighborhood of the zero electric vector. The cutoff is
flat at both join endpoints; away from zero the electric norm and parent
response are smooth on the strict gate domain. The magnetic coefficient is
therefore smooth as a function of the electric vector and positive density
there. The magnetic action is differentiable also at `E_U=0, B_U!=0`.

The retained electric function has expansion

\[
 L_e(E)=E^2/2-E^3/(3D_0)+O(E^4).
\]

As a function of the electric vector it is C2 at zero, rather than C-infinity.
Thus this construction supplies a C2 occupied-phase action in the current and
field variables, not an analytic action or a general PDE existence theorem.
The material current must remain timelike with positive density.

Changing beta does not change a pure-electric static background's value or
first variations: every beta-dependent term is multiplied by B_U squared.
Its quadratic current/gauge energy changes through beta, and remains positive
by (1)--(4). The regular-core fluid Hessian is unchanged. The joint quadratic
energy calculation applies with this new beta as well as with the parent,
because beta-density derivatives still start at cubic order when B_U=0.

As the density tends to zero, `a^2~h/16` tends to zero. No uniform open field
neighborhood is supplied along the infinite tail. In fact this coefficient
has no continuous joint vacuum limit at `(h,E)=(0,0)`: along `E=0` it is
one quarter, while along `E=a(h)` the cutoff is zero, `hcrit/h->0`, and
`beta_P->1`. Thus this particular patch does not furnish a continuous vacuum
coefficient continuation, not merely an unverified one. For the regular-core
background, `h~r^-5` while `E^2~r^-4`; ultimately the cutoff vanishes and
the parent response is recovered. The outgoing-radiation obstruction and the
undefined vacuum material frame therefore remain. The central source is
still fixed. This is a specific repair of the occupied zero-electric-field
regularity defect, not completion of a physical galaxy or the full theory.
