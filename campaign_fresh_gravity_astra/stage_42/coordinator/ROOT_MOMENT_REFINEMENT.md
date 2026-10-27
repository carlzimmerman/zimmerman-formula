# Conditional refinement of the nonstationary-boundary moment error

Coordinator candidate requiring audit. The old FGF055 planning identities were
already available. The author's new progress preview (wide cone, O(epsilon)
field and O(epsilon²) fluid endpoint bounds, coarse O(epsilon³) bulk capacity
error) arrived before this note was written. No new raw proof or independent
reviewer derivation was read. This is an after-preview reconstruction, not
blind discovery. All bounds below are conditional on the actual full-system
bounds requested in FGF055; this note does not establish those bounds.

Fixed physical coefficients, finite V>0, fixed Btime>0, horizon
T=Btime epsilon/V, A=x*-2epsilon,D=x*+2epsilon, L_I=4epsilon.
Let rho,g0 be smooth background functions, rho>0, with bounded derivatives
near x*. Suppose every existing positive classical prefix through T has

    0<n<=Nbar, |g-g0|<=Cg epsilon on [A,D],
    |v(A)|,|v(D)|<=Cv epsilon²,
    |n(A)-rho(A)|,|n(D)-rho(D)|<=Cn epsilon².

All constants are independent of epsilon for the fixed physical cell. They
need not be uniform when field speeds tend to infinity. Initial n=rho,
v=V f((x-x*)/epsilon), exact original polynomial joins. The actual coupled
Q/scale source and isothermal Euler equations remain in force.

Put j=nv, M=int n, P=int nv, I=int_A^D(x-A)n, and
Delta=L_I M-I. Exact continuity and fluid momentum give

    M'=j(A)-j(D),
    P'=-[nv²+cs² n]_A^D-int ng,
    I'=P-L_I j(D),
    Delta'=L_I j(A)-P.

Hydrostatic cs² rho_x=-rho g0 gives

    R=[nv²+cs²(n-rho)]_A^D+int_A^D(ng-rho g0),
    P'=-R,
    Delta(T)=Delta0-P0 T+int_0^T(T-t)R(t)dt
                                  +L_I int_0^T j(A,t)dt.       (1)

No endpoint current is zeroed. The right current cancels only in the exact
combination Delta'=L_I M'-I', not by an assumed no-flux wall. Positivity implies
Delta(T)>0. The same leading initial capacity and momentum from the pinned
polynomial give Delta0=8rho*epsilon²+O(epsilon³) and
P0 T=(16/15)rho* Btime epsilon²+O(epsilon³).

The given endpoint velocity bounds imply

    |M(t)-M0|<=2Nbar Cv epsilon² t = O(epsilon³), 0<=t<=T.

Split the bulk force exactly, with g*=g0(x*):

    int(ng-rho g0)
      =int n(g-g0)+g*(M-M0)+int(g0-g*)(n-rho).          (2)

The first term is at most4Nbar Cg epsilon². If K0 bounds |g0_x|,
then |g0-g*|<=2K0 epsilon and
int|n-rho|<=4epsilon(Nbar+rhobar). Thus the last term is at most
8K0(Nbar+rhobar)epsilon². The middle term is O(epsilon³), as above.
Consequently the bulk residual is O(epsilon²), sharper than bounding ng and
rho g0 separately by O(epsilon). This uses mass near-conservation, not an
unproved pointwise small density change in the interior. Interior n-rho may
be order one; total variation and density-gradient control are not required.

Pressure endpoint residual is O(epsilon²); kinetic endpoint stress is
O(epsilon⁴). Therefore R=O(epsilon²) uniformly through T, and

    |int_0^T(T-t)R(t)dt|=O(epsilon⁴),
    |L_I int_0^T j(A,t)dt|=O(epsilon⁴).                 (3)

The leading strict gap for Btime>15/2 is still O(epsilon²). Initial background
Taylor errors remain O(epsilon³) under these conservative estimates. The
refinement changes the dynamical error bound, not the factor15/2 or the
parameter gate. It neither establishes upper survival failure independently
of the assumed actual bounds nor supplies existence/maximal continuation.

To keep field accounting explicit, write mf=-(tau p g+sigma w k)/C and
Sf=(g B_Q-W+tau p²/2+sigma w²/2+Jk²/2-U_s)/C. Then

    (P+int mf)'=-[nv²+cs²n+Sf]_A^D.

This generally is NOT zero here. In particular int mf is not P0-P: its
boundary stress must be retained. Fluid residual R in (1) has not silently
been replaced by the stationary-collar field-transfer expression. For the
complete energy density E and flux F from the pinned full Q/scale/fluid
system, (int_A^D E)'=F(A)-F(D), generally nonzero. No field stress/energy flux
is bounded or deleted by the assumptions of this narrow note beyond what
actually follows from the underlying solution. These balances are consistent
with (1)--(3) and do not need field waves to be slower than matter.

At V=0 the original H is stationary and every residual vanishes; the formulas
using epsilon/V do not apply. Both a0 values require separate compatible H
and Q speeds. Constant and individually frozen H histories are separate;
evolving reference excluded. Q/RAR/M/filtered MONO remain distinct, with
actual MOND source retained. No physical metric/photon/two-DOF, criterion B,
observational or historical novelty claim. Zero mathematical computations.
