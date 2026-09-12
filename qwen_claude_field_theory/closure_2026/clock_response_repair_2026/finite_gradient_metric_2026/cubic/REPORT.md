# Cubic scalar–metric principal elimination at finite gradient

2026-09-12. Owner `/root/fixed_action_escape`. Base and actual archived
checkout: `706cd625f648079d318aa968b59fbd45850720f2`, dirty.

**Result:** the cubic term contributes explicit anisotropic corrections of
order gamma squared after its metric mixing is eliminated with Einstein's
equation. At the earlier proposed longitudinal marginal points, these
corrections make the affine-jet discriminant more negative for every coupling
strength under the stated timelike/domain hypotheses. Numerical evaluation
with the unchanged gamma=1e-6 action preserves all ten prior longitudinal
counterexamples. Five additional physical-q fixtures with nonzero Hessian
also retain negative discriminants. None is claimed to be an on-shell
finite-gradient cosmology.

The calculation does not assume that a small gamma can be ignored. In fact,
the already present order-gamma P/W coefficient corrections change one of
the sampled discriminants by about 45%, although they do not change its sign.

## Covariant variation and Einstein elimination

Use signature -+++, constant gamma, and

\[
 v_\mu=\nabla_\mu\chi,\quad
 X=-v_\mu v^\mu,\quad H_{\mu\nu}=\nabla_\mu\nabla_\nu\chi,
 \quad B=\Box\chi.
\]

The action term is **+ gamma X Box(chi)**. With
E_chi=(delta S/delta chi)/sqrt(-g), its scalar variation is

\[
 E_3=2\gamma\left[B^2-H_{\mu\nu}H^{\mu\nu}
                         -R_{\mu\nu}v^\mu v^\nu\right].
\]

The full scalar equation includes the unmodified clock terms:

\[
 E_\chi=2\nabla_\mu(P_Xv^\mu)
       -2\nabla_\mu(sW_Y h_\tau^{\mu\nu}v_\nu)+E_3=0,
 \qquad s=\sqrt{X_\tau}.
\]

To derive E3, direct variation first gives
2 gamma div(B v)+gamma Box(X). The covariant commutator identity
Box(X)=-2 H:H-2 v dot grad(B)-2 Ric(v,v) then cancels the third derivatives.
This commutator, with the displayed curvature sign convention, is an
analytical input to the computation.

Inverse-metric variation and integration by parts give

\[
 T^3_{\mu\nu}
 =2\gamma\left[Bv_\mu v_\nu
       -2v_{(\mu}H_{\nu)\alpha}v^\alpha
       +g_{\mu\nu}v^\alpha v^\beta H_{\alpha\beta}\right].
\]

Parentheses include one-half. An equivalent form is
2 gamma B v_mu v_nu + gamma(v_mu grad_nu X+v_nu grad_mu X)
- gamma g_mu_nu v dot grad(X). The calculation retains all ten independent
components of the symmetric Hessian and all four components of v. It checks
the cancellation of the metric-Euler terms using

\[
 \delta\Box\chi=\delta g^{\mu\nu}H_{\mu\nu}
 +v_\mu\nabla_\nu\delta g^{\mu\nu}
 -\tfrac12 v^\alpha\nabla_\alpha(g_{\mu\nu}\delta g^{\mu\nu}).
\]

The integrated-by-parts identity is another analytical input; the script
mechanizes its resulting tensor contractions, not all differential geometry.
It also checks that the cubic affine principal stress has zero leading
divergence after H_mu_nu is replaced by xi_mu xi_nu sigma, as required by
the principal Einstein source constraint.

For trace reversal, bar(T)_mu_nu=T_mu_nu-g_mu_nu T/2, direct contraction gives

\[
 T^3=2\gamma[-XB+2vHv],\qquad
 v^\mu v^\nu\bar T^3_{\mu\nu}
       =\gamma X[XB+4vHv].
\]

Insert R_mu_nu=bar(T)_mu_nu/M^2 into E_chi, where the remaining stress has
at most first derivatives of these scalar fields. The explicit second-metric
derivative coupling is removed. Its scalar principal feedback is

\[
 \boxed{\Delta Z^{\mu\nu}_{\gamma^2}
 =-\frac{2\gamma^2X}{M^2}
       (Xg^{\mu\nu}+4v^\mu v^\nu).}
\]

Here Z multiplies nabla_mu nabla_nu sigma in E_chi. For a general background
Hessian, direct linearization of the remaining cubic self-Hessian terms adds

\[
 \Delta Z^{\mu\nu}_{H}
       =4\gamma[B g^{\mu\nu}-H^{\mu\nu}].
\]

The numerical affine cases set H_mu_nu=0, not gamma=0. The clock equation
has no direct cubic term, and its metric terms remain one derivative lower
than its elliptic principal block after this elimination. The preceding
clock Schur complement therefore applies with the actual frozen P/W jets
when its denominator F is nonzero. The parent metric-principal work handles
the gauge and metric reconstruction statements separately.

## Anisotropic characteristic coefficients

In the clock rest frame let v_cov=(Q,b,0,0), Y=b^2, w=b dot n,
z=w^2, and X=Q^2-Y. Define p=P_X, r=P_XX and

\[
 C=W_Y+2zW_{YY},\quad F=W-2Q^2C-2zW_Y,
\]
\[
 K=2p+4Q^2r,\quad B_0=8Qrw,\quad
 G=2p-4rz-2sC\frac{W-2zW_Y}{F}.
\]

The affine scalar characteristic is
(K+delta K)c^2+(B0+delta B)c-(G+delta G)=0. Writing
t=2 gamma^2 X/M^2 gives the actual metric corrections

\[
 \delta K=t(4Q^2-X),\qquad
 \delta B=8tQw,\qquad
 \delta G=-t(X+4z).
\]

The homogeneous controls are delta K=6 gamma^2 Q^4/M^2 and
delta G=-2 gamma^2 Q^4/M^2, agreeing with the existing cubic principal
audit. No coupling expansion is used in these affine corrections.

Let Xi0=B0^2/4+KG. The full affine quarter-discriminant is exactly

\[
 \Xi_t=\Xi_0+tA+t^2D,
\]
\[
 A=32Q^2rz+(4Q^2-X)G-K(X+4z),\qquad
 D=X(X-4Q^2+4z).
\]

At the proxy marginal relation s=p(W-2Q^2C)/(WC), the exact identities are

\[
 \Xi_0=-8pz\left(r+\frac{KQ^2C W_Y}{WF}\right),
\]
\[
 A=-8pz-2pX-4rX(Q^2-z)
       -(4Q^2-X)\frac{8pQ^2CzW_Y}{WF},
\]
\[
 D=-3X^2-4X(Y-z).
\]

If M^2,p,r,W,C,W_Y,F>0, X=Q^2-Y>0, and 0<=z<=Y, then t>=0,
A<0 and D<0. For z>0, Xi0<0 and hence Xi_t<0 for every t>=0.
At z=0, Xi0=0 and Xi_t<0 whenever t>0. This is a conditional algebraic
obstruction for affine local jets at a proxy zero. It neither classifies
arbitrary background Hessians nor rules out other nonlinear solutions of
the action. The identities remain pointwise statements when the positive
coefficient jets themselves depend on gamma.

## Frozen numerical action and nonzero-Hessian fixtures

The prior audit's five unstable epochs and both q conventions are reused.
No roots are reinterpreted as solved finite-gradient backgrounds. Separate
columns retain (a) isolated explicit gamma-squared metric feedback on the
previous gamma0 jets and (b) the actual unchanged model's P/W jets at
gamma=1e-6, including their existing order-gamma terms. For each convention,
the finite-gamma proxy marginal relation is also solved anew for Y without
changing any coefficient function.

At the first reference-q longitudinal root:

| Quantity | Value |
|---|---:|
| Prior Xi0 | -2.42113017705e-4 |
| Explicit metric-feedback shift of Xi | -3.14903128883e-12 |
| delta K | +4.09781305225e-12 |
| delta B | +1.08158173267e-13 |
| delta G | -1.36629453822e-12 |
| Xi including actual finite-gamma P/W jets | -2.17061590747e-4 |

All ten old longitudinal roots retain negative Xi with the actual finite-gamma
jets and metric feedback. The final reference-q example changes from
-4.05359 to -2.24476 after those coefficient corrections, about a 45% change
in magnitude. Thus the small explicit metric-feedback size does not justify
dropping every gamma-dependent effect near a cancellation.

For the physical-q cases, the original sourced H and Qdot are recomputed
from the existing homogeneous background equations. The local ansatz
chi=C(t)+b_comoving*x on that FLRW geometry has orthonormal Hessian

\[
 H_{00}=\dot Q,\quad H_{0x}=-H\sqrt Y,\quad
 H_{xx}=H_{yy}=H_{zz}=-HQ.
\]

It gives the independently checked direct cubic corrections
delta K_H=-12 gamma H Q, delta B_H=-8 gamma H w,
delta G_H=-4 gamma(Qdot+2HQ). Adding a gradient to the old geometry is a
kinematic fixture; its backreaction and new constraints have not been solved.
With actual gamma=1e-6 jets, all five physical-q longitudinal examples still
have Xi<0:

| Original a | Xi including metric feedback and nonzero Hessian |
|---|---:|
| 1.000000 | -2.0800240e-4 |
| .750137 | -2.4553453e-3 |
| .562705 | -2.7181547e-2 |
| .422105 | -2.2315504e-1 |
| .316637 | -2.2489249e-1 |

The first example has phase speeds approximately
-.00955535 +/- .00661509 i. This is a principal-symbol failure at the stated
local jets, not a claim that these inhomogeneous data form a global solution.

## Verification, status and remaining implication

Fourteen exact symbolic checks and six tests passed. The tests include a
large-gamma software control, so an implementation that simply drops gamma
cannot pass them. The bounded execution and manifest validation returned
exit 0. A peer independently checked the contractions, Hessian signs, and
discriminant polynomial, then reran the six tests and validation successfully.
The computation-audit and proof-audit workflows distinguish the analytical
covariant identities from the exact contractions and finite numerical runs.
Mathematical self-review covered this report's conventions and formula mapping.

The next missing implication is an actual finite-gradient solution and its
constraints, with a full principal analysis at that solution. Affine-jet
sign identities and the finite nonaffine fixtures do not establish an
all-background no-go, a nonlinear degree count, a complete cosmology, or a
CMB prediction. No coefficient reconstruction, extra particle dark matter,
old-source edit, or commit was performed by this work package.

See [commands and provenance](COMMANDS.md).
