# FGF049 independent raw route, frozen before new proof exposure

Reviewer /root/fgf049_reviewer. This document was derived using only the task,
common contracts and OLD pinned ancestry. No new stage36 author, root or other
reviewer proof or mathematical preview was read. Proof-only; zero mathematical
executable computations. Administrative hashing does not test a theorem.

## Claim and verdict before exposure

The unconditional O(ell/V) upper positive classical lifespan transfer is
**incomplete, with the smallest missing implication**: a force/force-gradient
feedback gate, holding until the proposed upper comparison time or an already
identified admissible stopping event, has not been derived from the coupled
system. Below is a sufficient conditional gate proved directly. This is neither
a stable-solution counterexample nor a claim that the missing estimate is false.

Use exactly n_t+(nv)_x=0, v_t+v v_x+c^2(log(n/nref))_x=-g,
tau phi_tt=B_x-Cn, sigma chi_tt=J chi_xx+T-U_s'(chi), with g=phi_x>0,
a=a_ref exp(chi), B=(sqrt(a^2+4g^2)-a)/2, W_g=B, T=-W_chi,
U_s=S0(cosh(2chi)-1)/4, and all coefficients fixed positive. The smooth
hydrostatic data and exact zero-extended f(y)=(1-y^2)^2 on |y|<1 are unchanged.
Set ell=L/N^3, V=v0 N, omega=V/ell. The profile is C1,1, not C2.

## Exact moving-force identities

Set q=log(n/nref), r=v+cq, s=v-cq, alpha=r_x, beta=s_x and h=n^(-1/2).
With Dplus=partial_t+(v+c)partial_x, Dminus=partial_t+(v-c)partial_x,
D0=partial_t+v partial_x, the equations imply

    Dplus r=-g, Dminus s=-g,
    Dplus alpha=-(alpha+beta)alpha/2-g_x,
    Dminus beta=-(alpha+beta)beta/2-g_x,
    Dplus q=-beta, Dminus q=-alpha.

Hence for y=h alpha and z=h beta,

    Dplus y=-y^2/(2h)-g_x h,
    Dminus z=-z^2/(2h)-g_x h,
    D0 h=(y+z)/4.                                      (I)

These follow by differentiating characteristic integral formulas and their
C1 label Jacobians. No classical second derivative of v at the joins is used.
No g_t term occurs: differentiate the force spatially at the same time in the
characteristic formula. Pressure is retained through c>0 and both families.
Only the negative part of g_x opposes the desired comparison.

## A sufficient conditional transfer gate

On K0=[x*-R,x*+R], let G00=||g0||, Q0=||q0||,
h0=max rho^(-1/2), hmin=min rho^(-1/2), d=8/(3sqrt(3)). Fix

    A=2d h0, b=d hmin,
    Btime=(h0/A)(exp(8A/b)-1), H=h0+A Btime,
    eta=min{A/(2H Btime), b^2/(8H^2)}, T_N=Btime/omega.

All are positive, N-independent and have the units inherited from FGF045:
Btime and eta are dimensionless, A,b,H have inverse-square-root-density units.
Fix a positive time tau0 and force constant Gstar independent of N. Suppose a
positive classical solution exists through T_N on a cone covering the initial
patch, and throughout this cone

    |g|<=Gstar,   (-g_x)_+<=eta omega^2.                (G)

Set Lambda=max(tau^(-1/2),sqrt(J/sigma)); field characteristic speeds are at
most Lambda because 0<B_g<1. Choose
S_N=V+c Q0+Gstar tau0+2c+Lambda and K_t with inward slopes +/-S_N.
Take N sufficiently large that T_N<=tau0, ell+2S_N T_N<R, and
omega>=G00/(c d). Fluid invariants give |r|,|s|<=V+cQ0+Gstar t and a strict
speed margin; the standard first-exit cone argument justifies these integrations.
Every material/fluid/field backward characteristic lies in the earlier cone.
The plus characteristic from a_N=x*+ell/sqrt(3) remains inside K_t since its
distance from x* is <=ell+S_N t<R-S_N t. Thus the cone is not an assumed
invariant support, nor does it touch the crossing or walls.

Initially y,z<=A omega. Bootstrap y,z<2A omega. By (I), along material
trajectories h<=h0+A omega t<=H. Along either fluid characteristic the negative
quadratic term can be discarded, so

    y,z <= A omega+eta omega^2 H t
          <=(A+eta H Btime)omega <=(3A/2)omega.

This strictly improves the upper barrier. Therefore the h envelope is valid
on every compact classical existence slab under (G), even if y or z is very
negative. No absolute fluid gradient bound is presumed.

On the selected plus characteristic let w=-y. Hydrostatics gives
w(0)=rho(a_N)^(-1/2)(d omega+g0(a_N)/c)>=b omega. As long as w>=b omega,

    w'>=w^2/(2h)-eta omega^2 h >=w^2/(4h)>0,

because eta H^2<=b^2/8<b^2/4. This threshold cannot be crossed downward.
Integration gives

    1/w(t)<=1/(b omega)
             -log(1+A omega t/h0)/(4A omega).

At T_N the right side is -1/(b omega), impossible for finite positive w.
Thus no positive classical solution covering this cone through T_N satisfies
(G). The stronger requirement |g_x|<=fixed constant is unnecessary; the
one-sided bound of size eta omega^2=O(N^8) suffices. The constants are
conservative and no sharp compression coefficient is claimed.

The invariant bounds also give finite positive density bounds for fixed N,
although they are exponential in N and therefore cannot serve as N-uniform
coefficient/source bounds. This distinction is essential below.

## Why old estimates do not verify G to T_N

FGF048 controls only t<=kappa/omega in matching fixed units with a sufficiently
small coefficient kappa. It bounds q excursion by integrating Afluid=O(N^4),
field gradients by O(1), and field gradient Lipschitz seminorms by O(N^7).
It proves g-g0=O(N^-4), g_x-g0_x=O(N^-1) there. Replacing kappa by Btime in
the final formulas is invalid: the first-gradient/state bootstrap used the
smallness of kappa. Indeed the scalar upper majorant A'=A^2+forcing ceases
to give a finite bound at an order-one rescaled time, before our deliberately
large Btime. Failure of that majorant is not blowup of the actual solution.

The exact dynamic source must remain

    B_g g_x+B_chi chi_x=Cn+tau p_t, p=phi_t.

Its positive Cn term does not prove g_x>=0 because p_t and B_chi chi_x are
uncontrolled. In the exact field characteristic chart Rplus/minus=p+/-hfield,
hfield_g=sqrt(B_g/tau), each source has H_q=-Cn/tau in its R components.
Thus differentiating introduces the actual -C n q_x/tau=-C n_x/tau.
Near density compression the coefficient Cn cannot be frozen at C rho.
Differentiating again introduces n(q_xx+q_x^2), interpreted weakly when needed.
An initial jet p_t=0 and g_t=0 supplies no bound for these accumulated terms.
A rectangular r,s bound gives n<=nref exp(O(N)); the source coefficient and
its derivatives can therefore be exponential in N. Multiplication by the
N^-4 time does not make that majorant small or prove a polynomial G gate.
The full scale contribution B_chi chi_x, T(g,a), U_s'(chi) and their
coefficient derivatives remain; freezing chi changes the problem.

## Continuation and endpoint limits

The conditional cone contradiction by itself classifies no earlier maximal
endpoint. For the diagonal coupled system on a compact positive-state chart,
bounded first gradients imply a linear integral inequality for the spatial
Lipschitz seminorm Htot, with coefficients bounded by the first-gradient and
state bounds. For each fixed N this propagates finite Htot from its finite
O(N^7) initial value; the PDE then supplies a C1 endpoint trace and the pinned
FGF047 construction supplies restart. Compatibility chi_x=k and phi_x=g
must propagate and hold at the trace. This establishes a sufficient gate only
on domains that admit restart with a retained buffer; an unbuffered cone tip
cannot be labeled a singularity.

Accordingly one must distinguish loss of first gradients, loss of positive
coefficient/state margins (n, g, a or chart compactness), loss of available
restart regularity, and physical-domain exit. If a common compact chart,
first-gradient bounds, higher-norm propagation and buffered containment are
proved, continuation follows; absent one of those proofs no unique endpoint
mechanism has been established. G alone does not bound the full scale chart.

## Energy and control

For p=phi_t,wscale=chi_t,k=chi_x the exact full energy/flux are

    E=nv^2/2+c^2n(log(n/nref)-1)+n phi
       +(tau p^2/2+W+sigma wscale^2/2+J k^2/2+U_s)/C,
    F=nv(v^2/2+c^2log(n/nref)+phi)-(pB+J wscale k)/C.

Fluid plus interaction exchange is np; Q exchange is -np-T wscale/C;
scale exchange is +T wscale/C. Hence E_t+F_x=0. On [a(t),b(t)] retain
F(a)-F(b)+b'E(b)-a'E(a); the shrinking cone energy is not conserved.
The zero-velocity hydrostatic tuple solves all four equations with p=wscale=0
and zero F on the actual patch. Initial excess energy O(V^2 ell)=O(N^-1)
controls no pointwise g_x or fluid gradient.

## Scope and provenance

Both a_ref=9.3619e-11 and 1.1279e-10 m/s^2 are separate fixed backgrounds;
constants may differ. Constant vacuum and separately frozen a0 E(z),
E^2=.315(1+z)^3+.685, are distinct from evolving-reference protocols with
work. Q, RAR, registered M, and filtered MONO remain distinct. The diagnostic
scale adds a DOF. No physical vacuum relation, metric/photon/two-DOF completion,
criterion B, calibrated cluster/cosmological evidence or historical novelty is
proved. No numerical samples, external theorem, literature mechanism, service,
commit or post-breakdown construction is used.

Proofread self-review: all displays and prose in this file checked; no
mathematical-token corrections after freeze. The raw route is conditional and
will not be overwritten by author-proof comparison.
