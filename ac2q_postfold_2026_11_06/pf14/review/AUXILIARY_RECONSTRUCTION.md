# Independent audit: local reconstruction and L1 stability

**Verdict: the on-branch reconstruction has local spatial existence near
homogeneous data and a uniform L1-to-L-infinity stability estimate in the
declared compact class.** These statements concern a prescribed clock
profile and geometry on one slice, not coupled temporal evolution.

Use fixed proper circle length L, coordinate z, area a=exp(2 beta), and
Pi=a P. The exact equations are

    A'=W_P(P)/r,
    Pi'=a[(rA-1)/gamma-r^2],    P=Pi/a.

All constants below may depend on positive upper/lower r,a bounds, L,
gamma, the compact cap range and a bound for A, but not on derivatives
of prescribed r,a. The hold potential is the same for the two profiles
at the fixed clock label.

## Difference system without an unsafe intermediate cap value

For two on-branch solutions set delta=first minus second and define

    k=(W_P(P1)-W_P(P2))/(P1-P2),

with the derivative value when P1=P2. The divided difference is taken
between the actual admissible P endpoints, so k has positive upper/lower
bounds on the compact cap interval. It does not evaluate W_P at the
possibly inadmissible intermediate Pi2/a1. Direct subtraction gives

    (delta A)'=b delta Pi+f1,
    (delta Pi)'=c delta A+f2,
    b=k/(r1 a1),    c=a1 r1/gamma,
    f1=-k Pi2 delta a/(r1 a1 a2)
       -W_P(P2)delta r/(r1 r2),
    f2=a1(A2/gamma-r1-r2)delta r+D2 delta a,
    D2=(r2 A2-1)/gamma-r2^2.

Thus |f|<=C(|delta r|+|delta a|), and b,c have fixed strictly positive
lower and finite upper bounds.

## Uniform periodic inverse

For M(z)=[[0,b],[c,0]], its fundamental matrix U with U(0)=I satisfies
det U=1 because tr M=0. It preserves the positive cone. Write
lambda=sqrt(b_min c_min) and
v0=(sqrt(b_min),sqrt(c_min)); then M(z)v0>=lambda v0.
The cooperative comparison inequality yields

    U(L)v0>=exp(lambda L)v0.

Therefore its Perron multiplier rho is at least exp(lambda L)>1.
The other multiplier is 1/rho, and

    |det(I-U(L))|=tr U(L)-2
                  >=2 cosh(lambda L)-2>0.

Uniform coefficient upper bounds bound U and U inverse by exp(CL).
The periodic variation-of-constants formula therefore gives

    ||delta A||infinity+||delta Pi||infinity
       <=C(||delta r||L1+||delta a||L1).

It also bounds the derivative difference in L1. This proves instantaneous
L1 stability of the auxiliary states, not L1 continuity of every
differentiated forcing used in the old expanded system. There is no
contradiction with the PF13 one-time loop test.

## Local spatial existence for measurable prescribed profiles

At constant r0,a0>0 take Pi0=P0=0 and A0=1/r0+gamma r0. The linearized
constant coefficient matrix is

    M0=[[0,Khold/(r0 a0)],[a0 r0/gamma,0]],

with eigenvalues +/-sqrt(Khold/gamma). Its periodic operator
partial_z-M0 is invertible from L-infinity to W1,infinity. For prescribed
r,a in a sufficiently small L-infinity neighborhood of r0,a0, write
Y=(A-A0,Pi) and the equation as

    (partial_z-M0)Y=F(r,a)+N(Y;r,a).

The forcing has norm O(||r-r0||infinity+||a-a0||infinity).
Continuity of W_PP near P=0 and positive r,a give a Lipschitz constant
for N on a small Y ball that tends to zero with the ball radius and
the parameter neighborhood. Thus the fixed inverse makes this map a
contraction on a small L-infinity ball. Its fixed point belongs to
W1,infinity even when the prescribed coefficients are merely measurable.
The proof uses no derivatives of r or a.

For sufficiently small neighborhoods the reconstructed fields retain
the positive strict branch margin Q0-1=gamma r0^2 and cap separation.
The hold law's limited regularity at P=0 is sufficient: W_P is C1 with
continuous derivative there; no high-order smooth IFT is being invoked.
The uniqueness test in the separate note identifies this local solution
as the only admissible periodic on-branch solution in the stated class.

This is local existence only. Neither global regular solvability for
arbitrary profiles nor cap-margin preservation follows from strict
convexity alone. No full-switch stability estimate is asserted here.

## Conditional temporal consequence

If prescribed r(t),a(t) remain in this common compact reconstruction
domain and are Lipschitz in time into L1, the estimate makes A(t),Pi(t)
Lipschitz in time into L-infinity. The spatial equations give uniform
spatial Lipschitz bounds, hence jointly Lipschitz representatives.
For a uniform-arclength gauge on a fixed coordinate circle with varying
ell(t), the equations acquire a common factor ell. The same proof adds
C|delta ell| to the estimate when ell has positive compact bounds; a
Lipschitz ell(t) gives the same temporal conclusion. A regularly varying
hold-law parameter adds its controlled parameter difference as well.

This does not prove the required time regularity of r,a after breakdown,
nor express the temporal auxiliary derivatives as a closed source map
on the coupled BV state space. It therefore supplies a useful spatial
reconstruction theorem without claiming a postbreak PDE existence or
uniqueness theorem.

Independent delegated audit, 2026-11-06; direct ODE/monotonicity proof.
