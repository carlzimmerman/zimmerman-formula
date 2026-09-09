# IC8–IC9: from shear integrability to optical alignment

2026-09-08. Scientific starting revision: `0aa6e0cef9f8b9f0e6fc7129bedfa12ef055914e`.
The subsequent Fable commit `0e20cf937` was inspected. Its independent IC7
reconstruction agrees with the earlier obstruction; its third-mode warning
is retained. These are new actions, not accumulated passes for IC7.
Full theory remains **OPEN**. Current constructive continuation:
[IC10_LOCAL_CLOCK.md](IC10_LOCAL_CLOCK.md).

## Common definitions

Use the physical metric, varied clock, six leaf momentum components, smooth
activation eta and boundary domain of [IC5_ACTION.md](IC5_ACTION.md).
Set xi=ln N, w=(u-1)xi, rho=bar pi/V, tau=bar pi_TF²/V²,
E=exp((4-3u)xi), C=Lambda+a0² U(u²). The unchanged trace density is

    L(rho,xi,u) = -E rho²/(3m) + m exp((3u-2)xi) C
                 - kappa exp((3u-4)xi)/2.

Here L denotes a Hamiltonian trace density, not the compact Lagrangian.
All constants, including alpha, b, F and U, are the fixed IC5 ones.
Numerical units are m=h0=1, kappa=6. The preferred U is not fitted anew.

## IC8: remove the shear momentum-curvature coupling

Put s8=xi+b u-1/4-2b/3, sigma=-1/4,
K8=2 exp(1/2+sigma s8)/m, J8=2E/(m K8), c8=m exp(u xi)J8.
On eta=1 replace the nongradient density by h8=K8 tau+L, retain
-m alpha exp(u xi)|D(xi+b u)|² and use curvature density -c8 bar R/2.
The global covariant Hamiltonian is H5 plus

    eta { 2 P_TF² (1/J8-1)/m - m(J8-1)Rhat/2
          + p² F Rhat/(2m a0²) + exp(w-xi) d8 Rhat² }.

d8 is the IC7 derivative-defined curvature-square coefficient, recomputed
from h8,c8 rather than copied from IC7: replace h,c in its M,v construction,
use the newly computed det Mstar, and the same smooth zero extension.
With Dt=partial_u-b partial_xi, K8_rho=Dt K8=0. The leading
(scalar momentum,tensor momentum,passive auxiliary) Hessian therefore has
block pattern ((a,0,d),(0,K8,0),(d,0,f)). Its curvature response vector
has no tensor component. Direct inversion proves the higher-order
antisymmetric coupling vanishes and that the recomputed square term
cancels the remaining quartic scalar term on the tested principal axes.

That is not sufficient: on the re-solved sheared background the even tensor
speed squared approaches approximately 1.00244, 1.01257 and 1.02487 on the
three axes. The script retains complex finite-frequency corrections.
This motivates a different auxiliary coordinate, not another numerical fit.

## IC9: the optical scalar and explicit action

Define S=(2-u)xi=xi-w, and

    J9=exp(-2w-1/6),  K9=2 exp(S+1/6)/m,  c9=m exp(S-1/6).

The full phase action is integral sqrt(-g)[2P:Q-H9]+Sm[g,psi], where

    H9 = H5 + eta {
       2 P_TF² (1/J9-1)/m - m(J9-1)Rhat/2
       + p² F Rhat/(2m a0²)
       - m alpha [|D S|²-|D(xi+b u)|²] }.

There is **no curvature-square term**. On eta=1 its exact canonical density is

    V [K9 tau+L-c9 bar R/2-m alpha exp(u xi)|bar D S|²].

Actual momentum variation gives P_TF=m J9 Q_TF/2 and p=-m Q. Substitution
gives the compact plateau Lagrangian

    m J9 (Q_TF²+Rhat)/2 - m Q²/3 - m C + kappa X
    + m alpha |D S|².

The code differentiates this Lagrangian separately and compares its
constrained quadratic Hessian to the canonical Hamiltonian reduction.
The lapse, auxiliary and longitudinal shift responses are retained.

Let t=u at fixed S. The derivative is
Dt=partial_u+xi/(2-u) partial_xi; the coefficient's derivative must be
included when applying Dt twice. Using xi=S/(2-u), define

    a_zeta=K9/12+L_rhorho/4-L_rhot²/(4 L_tt),
    B=m alpha exp(u S/(2-u)),  g_zeta=2(c9_S²/B-c9).

For the flat homogeneous principal-axis reduction,

    A0=diag(a_zeta,K9)/V,
    C2=V diag(g_zeta,c9/2)/B3²,
    cs²=a_zeta g_zeta/exp(2S),
    cT²=K9 c9/[2 exp(2S)]=1.

Both coefficients are independent of rho and of t at fixed S. The
vanishing momentum/curvature response removes the quartic and antisymmetric
terms without a counterterm. The actual Schur complement checks this,
rather than inserting their expected zeros into the numerical pencil.
The numerical coverage is the exact isotropic witness, a nearby isotropic
solution and three principal axes of a re-solved sheared solution; it is not
an exhaustive inhomogeneous or general-direction characteristic proof.

| IC9 background | computed cs² | computed cT² |
| --- | ---: | ---: |
| old expanding witness | 0.18193246958758054 | 1 |
| nearby isotropic solution | 0.2038297669082732 | 1 |
| sheared solution, each sampled axis | 0.1984584577038915 | 1 |

## Exact finite-wave test, not just the principal cone

At the expanding witness use f=exp(-1/2), canonical p_zeta=V f P,
x=exp(2/3) k_comoving²/bar A² and Tcal=-27/16+54/[5 ln(9/5)].
The code differentiates the actual H9 and then applies the momentum
constraint. In (zeta,P,delta xi,delta u), its normalized Hessian is

    M0 = [[24,0,16,-6], [0,0,2,-3/4],
          [16,2,-24,27], [-6,-3/4,27,-(16 Tcal+135)/8]].

The spatial addition is x G with G00=-2, G0a=-2 v_a,
Gab=-2 alpha v_a v_b, v=(4/3,-1/4). Eliminate the last two variables
by their actual linear equations, obtaining ((c,b),(b,a)). The exact equation is

    zeta_ddot = D(x) zeta_dot + E(x) zeta,
    D=-3-2x a'/a,
    E=-2x b'+(3+2x a'/a)b-a c+b².

In particular,

    a=9(16 Tcal+alpha x)/[2((64 Tcal+243)alpha x+432 Tcal-2916)].

This is positive and has no positive-x pole for Tcal>27/4, alpha>0.
Nevertheless D is nonconstant and E is rational, not a local polynomial
wave operator. The exact rational expressions and an IR growing band are
retained in the output. x->0 here is NOT the independent homogeneous sector.

The local scalar S also has a rational reduced response. The script solves
its auxiliary equations and computes V f times {delta S,delta S_dot} from
the reduced canonical bracket, including xdot=-2x and Vdot=3V. This flags a
physical locality obligation; it is not asserted to be a completed
retarded-observable or spacetime-causality no-go theorem.

A potential-only trial replaces -H_aux by the positive matrix
M=((24,-6),(-6,27/16)), with zero potential value/first jet at the witness.
It makes v_momentum^T(-M)^(-1)v=0 and hence a independent of x. Direct
variation still gives

    E=2 a x [1+2d(1-alpha)x]/[1-2 alpha d x],
    d=v^T(-M)^(-1)v<0.

The negative-x pole has nonzero residue: this particular repair does not
remove the spatial factor. It is not a no-go for other kinetic actions.
IC10 therefore changes the trace kinetic term as well and tests a local
clock action rather than assuming this factor is harmless.

## Audit scope

Self-review, with exact symbolic residuals and separate phase/compact-action
implementations; no new independent-agent audit or Lean certificate.
No IC6 strong auxiliary theorem is automatically transferred. Matter's
physical-metric Ward identity and the static first variations are preserved
by the explicit action differences, not by borrowed PPN values. Full
galactic matching, PPN, measured G, transition health and y=0 remain OPEN.
