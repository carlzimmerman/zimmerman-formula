# Scoped no-go: exact MOND versus tensor luminality

## Exact claim

Consider the covariant clock action

\[
S=\frac1{16\pi G}\int d^4x\sqrt{-g}\left[
R-2\Lambda-2\lambda(\Delta_h\chi-R_{\mu\nu}n^\mu n^\nu)
+2a_0^2Q(Y)\right]+S_m[g,\psi],
\]

where

\[
n_\mu=-\frac{\nabla_\mu T}{\sqrt{-\nabla T\cdot\nabla T}},\qquad
Y=\frac{h^{\mu\nu}\nabla_\mu\chi\nabla_\nu\chi}{a_0^2},
\]

and exact exponential MOND requires

\[
\mu(y)=1-e^{-y},\qquad 2Q_Y=e^{-y},\qquad
Q(y^2)=1-(1+y)e^{-y}+C.
\]

On a regular spherical branch with finite \(y>0\), this exact MOND law is
incompatible with exact tensor luminality relative to the minimally coupled
physical metric. That contradiction is the load-bearing scoped no-go. It does
not rely on a nonlinear no-slip claim, a generic nonlinear degree count, or the
interpretation of the special flat-background scalar.

## Exact spherical MOND branch

Varying the radial reduction with respect to `chi` before integrating gives

\[
\frac{d}{dr}\left[r^2\left(\lambda_r+e^{-y}\chi_r\right)\right]=0,
\qquad y=\frac{|\chi_r|}{a_0}.
\]

On the positive-gradient chart,

\[
\lambda_r=\frac{C_{\rm aux}}{r^2}-a_0y e^{-y}.
\]

A regular centre with finite \(y\) cannot support the singular auxiliary flux,
so \(C_{\rm aux}=0\). Therefore

\[
\boxed{\lambda_r=-a_0y e^{-y}<0}\qquad(0<y<\infty).
\]

The additive constant in \(Q\) shifts only the effective cosmological constant;
it does not change this equation.

## Exact tensor cone and contradiction

The ADM form of the same action contains

\[
\mathcal L_{\rm kin}=(1-2\lambda)(K_{ij}K^{ij}-K^2)
+2K\mathcal L_n\lambda.
\]

For a transverse-traceless perturbation, \(K=0\), so the principal density is

\[
\mathcal L_{\rm TT}^{\rm principal}
=\frac{1-2\lambda}{2}\dot h_{\rm TT}^2
-\frac12(\nabla h_{\rm TT})^2,
\qquad
c_T^2=\frac1{1-2\lambda}.
\]

Exact equality with the light cone of the minimally coupled physical metric
requires \(c_T^2=1\), hence \(\lambda=0\) pointwise on the open radial branch and
therefore \(\lambda_r=0\). The exact MOND equation instead requires
\(\lambda_r=-a_0y e^{-y}\ne0\) at every finite nonzero MOND gradient. Thus

\[
\boxed{\text{exact exponential MOND}+\text{exact physical-metric }c_T=c
\quad\text{is impossible in this action class}.}
\]

This contradiction alone gives the scoped `DEAD` verdict for the displayed
scalar curvature-sourced elliptic action class.

## Corrected trace-free metric result

The complete static trace-free spatial equation is

\[
\left[N R_{ij}-D_iD_jN
+2N D_{(i}\lambda D_{j)}\chi
+2\lambda D_{(i}N D_{j)}\chi
-2D_{(i}\lambda D_{j)}N
+2NQ_YD_i\chi D_j\chi\right]^{\rm TF}=0.
\]

The auxiliary trace-free terms start at quadratic weak order. At linear order,
the finite-\(k\) equation is

\[
k^2(\Phi-\Psi)=0,
\]

so ordinary boundary conditions give

\[
\boxed{\gamma=\Psi/\Phi=1}.
\]

At the next order the same equation determines the second-order slip. On the
leading shell \(\chi=\Phi=\Psi=u\), it contains

\[
(p_2-n_2)''+u u''-\mu(u')^2=0.
\]

A nonzero quadratic source is therefore not a fatal linear no-slip residual.
The coupled second-order metric equations must be solved before any nonlinear
no-slip verdict is made.

## Restored-clock special branch

The finite-momentum scalar calculation concerns only the special flat branch

\[
\bar\lambda=0,\qquad \Lambda_{\rm eff}=0,
\qquad \bar\chi=\text{constant},\qquad k>0.
\]

After restoring the Stueckelberg clock perturbation \(\pi\), its quadratic
contribution is a total derivative and its Euler--Lagrange equation vanishes.
The surviving gauge-invariant scalar has zero clock projection and is built
from the `zeta`/`ell`/`chi` sector. Its reduced action is

\[
L_{\rm red}=6\dot\zeta^2-2k^2\zeta^2,
\qquad \omega^2=k^2/3.
\]

Thus the mode is not the clock mode on this branch. This is an exact
special-branch diagnostic, not a generic nonlinear degree-count theorem and
not the basis of the action-class verdict above.

## Homogeneous sector and Ward statement

For homogeneous FLRW, \(\Delta_h\chi=0\) and \(R_{nn}=-3\ddot a/a\). The
`lambda` equation therefore permits coasting,

\[
\ddot a=0,
\qquad a(t)=At+B,
\]

including \(H\ne0\). This equation alone neither proves a viable coasting
cosmology nor supplies the remaining homogeneous field equations and
perturbation analysis.

Ordinary matter appears only in the minimally coupled \(S_m[g,\psi]\). The
standard analytic Ward implication is therefore

\[
\nabla_\mu T^{\mu\nu}=0
\]

on the matter equations, conditional on the stated covariant coupling. This is
not recorded as an independent computational pass for the full candidate.

## Scope and nonclaims

- The theorem applies to the displayed scalar curvature-sourced elliptic action,
  a regular source-free spherical auxiliary branch, finite \(y>0\), and exact
  physical-metric tensor luminality.
- Linear no slip passes; nonlinear no slip is unresolved, not falsified.
- The restored-clock scalar statement is restricted to the flat
  \(\bar\lambda=0\), \(\Lambda_{\rm eff}=0\), finite-\(k\) branch.
- No generic nonlinear Dirac closure, universal degree count, physical-ghost
  theorem, or complete PPN extraction is claimed.
- Coasting expansion is admitted by the multiplier equation, but full FLRW
  viability remains unresolved.
- The relation \(a_0=c^2\sqrt{\Lambda/(32\pi)}\) is external input, not a result
  of this action.
- This is not a universal relativistic-MOND no-go. Genuinely nonlocal actions
  are one possible direction among others, including different local tensorial
  couplings, extra fields, or a different constrained phase space.

## Verdict

The exact-exponential scalar curvature-sourced elliptic action class is
**DEAD under the stated exact-luminality requirement**, solely because its
regular MOND branch requires \(\lambda_r\ne0\) while exact tensor luminality
requires \(\lambda=0\) pointwise. The broader existential target remains
**OPEN**.
