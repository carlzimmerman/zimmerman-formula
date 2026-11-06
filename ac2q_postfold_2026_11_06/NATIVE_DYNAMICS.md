# PF03: exact time-dependent planar matter equations and short-wave check

Criteria: bdaee092bf. This executes the first N1 continuation in HANDOFF.md.
Fixed flat metric, planar fields only; it is not the coupled Einstein problem.
Natural units c=1. Scalar gradient timelike, with a=phi_t>0 and b=phi_x,
r=sqrt(a^2-b^2)>0, u=P_t, d=P_x, X=r^2/2. The orthogonal unit vector is
 e=(-b,a)/r and the constrained polarization is P^mu=P e^mu.

## Exact nonlinear first-derivative formulation

D=(a d-b u)/r is the spatial divergence D.P. The geometric identity
P.A=div(P^mu)-D makes the acceleration term equivalent to -D modulo a boundary
term. The full planar matter densities are therefore

    L_on  = -D + X - V - W - gamma D^2/2 - 2 gamma D X,
    L_off = -D + X - V - W + 2 gamma X^2.

These keep the exact relativistic normalization, canonical scalar term, and
native stiffness. W and its phi dependence must be kept in the field equations.
Set L_D=-(1+gamma(D+2X)), L_X=1-2gamma D on the on-branch, and
L_D=-1, L_X=1+4gamma X on the off-branch. With

    D_a=b(a u-b d)/r^3,  D_b=a(b d-a u)/r^3,

currents are

    J_phi^t = L_X a + L_D D_a,
    J_phi^x = -L_X b + L_D D_b,
    J_P^t = -L_D b/r,
    J_P^x = L_D a/r.

The exact flat equations are partial_t J_phi^t+partial_x J_phi^x=L_phi and
partial_t J_P^t+partial_x J_P^x=-W_P. Here L_phi includes -V_phi-W_phi
(and any explicitly phi-dependent coefficients if the model specifies them).
This is a useful formulation for future constrained evolution; it has not been
numerically evolved in this checkpoint. A background held fixed for the symbol
below need not itself solve these sourced equations.

## Frozen-background principal test

At a=s>0, b=u=0, P_x=d, define H=W_PP>0. The quadratic coefficients are
A=L_aa, B=-L_bb, C=L_ad+L_bu, G=-L_dd. For the on-branch,

    A=1-2gamma d,
    B=1-gamma d+(d+gamma d^2)/s^2,
    C=(1+gamma d-gamma s^2)/s,
    G=gamma.

For the off-branch,

    A=1+6gamma s^2,
    B=1+2gamma s^2+d/s^2,
    C=1/s, G=0.

There is no rest-frame P_t^2 kinetic term. The Fourier matrix, including H, is

    [ -A omega^2+B k^2       C omega k ]
    [ C omega k              G k^2+H ].

Its single omega^2 root is

    omega^2 = B k^2 / [A+C^2 k^2/(G k^2+H)].

The determinant and elimination agree symbolically. Where denominators are
nonzero, the on-branch is asymptotically proportional to k^2, with coefficient

    gamma(s^2-gamma d s^2+d+gamma d^2)
    / [gamma s^2(1-2gamma d)+(1+gamma d-gamma s^2)^2].

The off-branch frequency tends to H[d+s^2+2gamma s^4]. Thus this local block
contains no automatic high-k k^4 dispersion, and no second propagating frequency
branch that can simply be identified with a new entropy/heat carrier. Negative
limiting values or degenerate coefficients require separate stability analysis;
no all-background health claim is made. At gamma=0 the two roots agree exactly.

This check weakens the simplest native-dispersion escape: the exact scalar terms
do not reveal a k^4 regulator omitted by the leading model. It does NOT prove
that all nonlinear solutions shock, that finite-k dispersion is irrelevant,
or that gravitating or oscillatory continuations cannot work. Metric constraints
are absent, so these formulas must not replace AC7's coupled dispersion grading.

## Retained failed check and correction

native001 failed two checks: an independently written expected on-branch B had
+gamma*d where the differentiated action gives -gamma*d; the predicted UV
coefficient inherited that mistake. Expansion by hand confirms it:
D=d[1+b^2/(2s^2)]+O(b^4) at fixed a=s,u=0, while X=(s^2-b^2)/2.
The -2gamma D X term contributes +gamma*d*b^2/2 to L, hence -gamma*d to B.
The symbolic action, Hessian and determinant were unchanged. native_dynamics.py,
native001 and their failed checks are preserved. native_dynamics_v2.py corrects
only the two hand expectations; native002 passes 21/21. This is an expectation
error, not a rejected physical action or an altered frozen test.

Dropping C in the determinant makes both independent-root comparisons fail in
native_mutate002. It detects the kinetic mixing required for the correct result.
All interpretation is self-reviewed; no independent audit or full evolution.
