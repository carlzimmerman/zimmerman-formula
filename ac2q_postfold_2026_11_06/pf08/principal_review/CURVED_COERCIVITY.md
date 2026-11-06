# Independent audit: curved weighted auxiliary inverse

**Primary verdict: correct only after retaining the additional gradient
forcing -2P E_beta K/r.** With that correction, the weighted inverse
extends the previous coercivity estimate to controlled planar geometry
without differentiating matter stress. The later amplitude/variation
bootstrap and characteristic Riccati transfer remain separate obligations.

Conventions: M=Mpl^2>0, r=sqrt(2X), h=H_r, R=H_rr,
D_r=(A-2gamma r)/gamma, B=n(beta), E_beta=e(beta), and
K=div_2 n=e(theta)+omega(e). This K is a geometric expansion, not the
hold-law constant. Write the frame acceleration as a_n=-e(r)/r. The
flat coefficient a below is a different quantity.

## 1. Frame and mixed Einstein equations

The orthonormal connection is

    nabla_n n=a_n e, nabla_n e=a_n n,
    nabla_e n=K e, nabla_e e=K n,
    [n,e]=a_n n-K e.

Clock compatibility is a_n=n(theta)+omega(n)=-e(log r). For the warped
two-dimensional transverse plane,

    R_ne=-2 Hess(beta)_ne-2 B E_beta,
    Hess(beta)_ne=n(E_beta)-a_n B
                  =n(E_beta)+(e(r)/r)B.

The mixed Einstein equation therefore gives

    n(E_beta)=-(e(r)/r)B-B E_beta-T_ne/(2M).

The native on-shell auxiliary Hilbert stress has longitudinal form
h_ab H+coefficient*phi_a phi_b. Since e(phi)=0, T_ne=0. This conclusion
uses the on-shell polarization/auxiliary equations and excludes an extra
matter sector with nonzero mixed flux. No derivative of stress was used.

## 2. Exact differentiated auxiliary system

Take constant V and a0, so there is no explicit scalar-potential source.
The spatial constraints and scalar equation are

    e(A)=W_P/r, e(P)=D-2P E_beta,
    n(r)=-(h K+r^2 D_r u+W_P v+2B J)/R,
    u=n(A)/r, v=n(P)/r, J=h+P W_P/r.

The same acceleration cancellation as in the flat review gives

    e(u)=a u+b v+f K+f0,
    e(v)=c u+(-a-2E_beta)v+g_tilde K+j e(r)+g0,

where

    a=W_P D_r/(rR),
    b=W_PP/r+W_P^2/(r^3 R),
    c=r/gamma-r D_r^2/R=r(1-2gamma D)/(gamma R),
    f=(W_P/r^2)(1+h/(rR)),
    g=D/r-D_r h/(rR),
    g_tilde=g-2P E_beta/r,
    j=2P B/r^2,
    f0=2B W_P J/(r^3 R),
    g0=2P B E_beta/r-2B D_r J/(rR)+P T_ne/(M r).

For native matter the last T_ne term vanishes. Its sign is positive if
an additional mixed stress is retained.

The correction g_tilde-g comes from the commutator term K e(P), since
e(P)=D-2P E_beta. It cannot be called a bounded geometry source merely
because P and E_beta are bounded: K contains e(theta), which may become
large. It must be retained as gradient forcing.

All other displayed geometry-source signs follow directly by substituting
the mixed Einstein equation into -(2P/r)n(E_beta). In particular the
remaining e(r) term has the proposed positive coefficient 2P B/r^2.

## 3. Weighted coercivity and inverse bounds

Multiplying the product equation by exp(2beta) yields exactly

    e[exp(2beta)uv]=exp(2beta)[c u^2+b v^2
      +(g_tilde u+f v)K+j u e(r)+g0 u+f0 v].

The trace term -2E_beta uv cancels against e(exp(2beta)). More explicitly
set U=exp(beta)u, V=exp(beta)v. Their homogeneous coefficient matrix is

    [[a+E_beta, b], [c, -a-E_beta]],

which is precisely the traceless form used in COERCIVITY.md. Thus its
periodic kernel is zero and its L2 and L1-to-Linfinity inverse estimates
apply without differentiating coefficients or matter stress.

The conditions are substantive: a closed regular clock slice, controlled
proper length, bounded/nondegenerate exp(beta), bounded E_beta and other
coefficients, and uniform b,c positivity. The latter follows from compact
clock/cap bounds and a positive margin for 1-2gamma D. This is an inverse
estimate at each admissible slice, not a proof that evolution maintains
those conditions.

Write K=e(theta)+omega(e). With

    Fhat=exp(beta)(f,g_tilde),
    Ghat=exp(beta)(0,j),
    qhat=exp(beta)[(f0,g0)+(f,g_tilde)omega(e)],

the forcing is Fhat e(theta)+Ghat e(r)+qhat. Subtracting constant parts
as in the flat proof gives the useful estimate

    ||(u,v)||_infinity <= C[osc(theta)+osc(r)
       +osc(Fhat) TV(theta)+osc(Ghat) TV(r)+||qhat||_1].

Constants depend only on the stated compact bounds and length, not on
derivatives of these coefficient functions. A small-amplitude bootstrap
must actually control the indicated coefficient oscillations. Bounded
geometry alone does not imply they are small; for example spatial
variation of exp(beta) multiplies the generally nonzero base value of g.

Near the homogeneous P=0 state, f and j vanish at the base point. Their
smallness can help even when B is order one. Once u,v are bounded, the
two first-order equations directly bound e(u),e(v) by a constant times
1+|e(r)|+|e(theta)|, under bounded geometry/spin connection. This avoids
the earlier generic derivative-of-inverse concern.

## 4. Additional geometry derivative identities

The mixed equation and commutator give

    e(B)=(K-B)E_beta-T_ne/(2M).

The normal Einstein constraint gives

    e(E_beta)=K B+(B^2-3E_beta^2)/2-T_nn/(2M).

For example G_nn=B^2-3E_beta^2-2[e(E_beta)-K B], which fixes the
sign in the second equation. These identities control spatial derivatives
of the beta-frame geometry linearly in K plus bounded stress. No matter-
stress derivative is needed. They are useful additional ingredients for
differentiating the characteristic source.

They do not automatically control every spin-connection/gauge derivative
or prove the global constraint propagation estimate. Those must be
handled in the selected metric gauge and in the eventual evolution proof.

## 5. Conditional characteristic-gradient cancellation

There is an elementary two-family cancellation worth separating from
the unfinished PDE reduction. Suppose exact local characteristic
variables z_plus,z_minus satisfy

    D_plus z_plus=S_plus,
    D_minus z_minus=S_minus,
    D_plus=partial_t+lambda_plus partial_x,

with a uniformly positive gap lambda_plus-lambda_minus. Let
w_plus=partial_x z_plus. Its differentiated equation contains

    -lambda_plus,plus w_plus^2
    -lambda_plus,minus w_plus w_minus.

For y_plus=exp(eta)w_plus, choose

    partial_minus eta=lambda_plus,minus/(lambda_plus-lambda_minus).

Because D_plus z_minus=S_minus+(lambda_plus-lambda_minus)w_minus,
this choice cancels the displayed mixed quadratic term exactly. Locally
eta can be obtained by integrating in z_minus while holding the other
state parameters fixed. Parameter dependence, source derivatives, and
metric terms generate additional terms; they are not removed by this
identity. The pure quadratic coefficient remains the genuine-nonlinearity
coefficient multiplied by the positive weight factor.

For the present model, deriving exact such variables with varying A and
geometry, and bounding all remaining differentiated sources using the
inverse and Einstein estimates, is still required. In particular the
weight identity does not itself control the opposite-family gradient or
the total-variation bootstrap. It is a candidate next algebraic step,
not a completed shock-formation theorem.

## 6. Status of the proposed high-frequency bootstrap

On a fixed controlled clock slice, amplitude delta=k^(-1/2) and total
variation O(sqrt(k)) can make the oscillation-times-variation terms O(1).
Together with bounded qhat this yields bounded u,v, while compression
can be order sqrt(k). The spatial auxiliary derivatives then enter only
linearly in state gradients. This is real structural progress toward a
subquadratic remainder estimate.

To turn it into formation, one must still propagate these amplitude/TV
and geometric bounds on the actual coupled solution, identify compressive
initial data satisfying all constraints, control the opposite family and
the parameter-dependent characteristic source, and keep every domain and
hyperbolicity margin until the contradiction. A failure of one of those
margins is a different event and cannot silently be counted as the
claimed gradient catastrophe.

## Verdict matrix and provenance

| Obligation | Status |
| --- | --- |
| Mixed Einstein identity and native T_ne=0 | passed on shell |
| Candidate g K plus only bounded remainder | corrected: retain -2P E_beta K/r |
| Exact f0,g0 and weighted trace cancellation | passed |
| Curved periodic coercive inverse | passed with stated compact/length bounds |
| No stress derivatives in these inverse/geometry identities | passed |
| Small-amplitude coefficient-oscillation bootstrap | not yet propagated |
| Two-family mixed quadratic cancellation | passed as an algebraic identity for a diagonal system |
| Full coupled formation or avoidance | not established |

Independent delegated proof audit, 2026-11-06. Direct frame, warped-Ricci,
and first-order-system derivations. No numerical experiment or imported
formation theorem was used.
