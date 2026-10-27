# Candidate: mass-coordinate control of actual Q sources closes the moment budget

Root derivation, pending fresh independent audit. This new route was derived
after reading the independently frozen FGF052 reviewer proof and receiving the
author's energy-obstruction preview, before reading the new author's raw proof.
The preceding conditional moment criterion is a candidate dependency awaiting
its audit; its raw algebra is also given below. No blind rediscovery is claimed.
The mechanism here changes from unsigned total energy to actual characteristic
source integrals and a density bound on the actual low-velocity set.

## 1. Exact target and conventions

Use dimensionless X=(x-x*)/L, theta=v0 t/L and the full FGF051 equations,
with its dimensionless fixed positive coefficients C,tau,sigma,J,c,a_ref,S0.
Density is n_physical/nref=exp(q). Initial v=N f(X/ell), ell=N^-3,
f=(1-y^2)^2 for |y|<1, zero outside, exact C1,1 joins. Initial fields are
the inherited smooth hydrostatic fields, initial n=rho, p=w=0. Coefficients,
background and nref,L,v0 are fixed independently of N.

Fix B_dagger>15/8 and Theta=B_dagger ell/N. Choose symmetric endpoints
A=-ell-d N^-7/2, D=ell+d N^-7/2, fixed d>0 within the exterior protected
FGF051 strips. For sufficiently large N, smaller exterior subcones about
these endpoints have untouched hydrostatic initial data and width margin
O(N^-7/2) while all local propagation over Theta is O(N^-4). Local uniqueness
therefore makes their traces EXACTLY hydrostatic, including p=w=v=0 and
phi=phi0. This step is detailed in the independently frozen FGF052 proof
section 1; it does not follow merely from bounded edge values.

Suppose for contradiction a positive classical whole-packet branch survives
through Theta on the original background neighborhood and the common edge
cones. We only use its restriction to I=[A,D]. It has exact traces above.
No existence through Theta is asserted. The branch has n>0 and initially
g>0; an early exit of the g>0 field chart is excluded by the bootstrap below.
An earlier failure of classical regularity already defeats the survival claim.

## 2. A fixed compact field bootstrap independent of fluid derivatives

Let z=(R_+,R_-,Z_+,Z_-,chi), R_+=p+h, R_-=p-h,
h_g=b=sqrt(B_g/tau)>0, Z_+=w+d_s k,Z_-=w-d_s k,
d_s=sqrt(J/sigma), B=(sqrt(a^2+4g^2)-a)/2, a=a_ref exp chi.
At the central background point let z*=z0(0). Choose a fixed compact
neighborhood K of z* and a larger smooth chart neighborhood, with g bounded
away from zero and a>0. Every quantity depending smoothly on z is uniformly
bounded there. Choose a radius delta>0 such that |z-z*|<=2delta lies inside
that neighborhood; bootstrap |z-z*|<delta. Initial and endpoint deviations
are <=C0 ell for large N because their background is fixed smooth.

On this bootstrap let |g|<=Gbar and |lambda_Q|<=Lambda, where the Q speeds
are -b,+b. Let Hbar bound the regular parts of the two Q sources, excluding
-C n/tau, and let Zbar bound the two scale sources. These constants depend
only on K and fixed coefficients. Indeed the EXACT characteristic equations are

  D_(v+c) r=-g, D_(v-c) s=-g, r=v+cq,s=v-cq,
  D_-b R_+=B_chi k/tau+h_chi(w-bk)-C n/tau,
  D_+b R_-=B_chi k/tau-h_chi(w+bk)-C n/tau,
  D_-d_s Z_+=D_+d_s Z_-=(Tscale-U')/sigma,
  chi_theta=w.

There is no field derivative in those sources. The quantities k,w are field
state coordinates, not uncontrolled derivatives of z. Pressure is retained
in r,s. Characteristic intersections cause no division by a speed difference.

Any backward fluid characteristic in I reaches theta=0 or its first lateral
boundary contact. Until that contact it is inside I. Initial v>=0 and initial
q is uniformly bounded, while lateral values are hydrostatic v=0,q=log rho.
Taking Theta<=1, both r and s therefore obey

  r,s >= -L0,  L0=c Q0+Gbar,

where Q0 bounds |log rho| on the fixed background neighborhood. No upper
bound on r,s,v or on any first derivative is assumed. Consequently v>=-L0.
If v<=Vcut:=Lambda+1, then r+s=2v and r,s>=-L0 imply

  |q|<= (v+L0)/c <= (Vcut+L0)/c,
  n<=Ncut:=exp((Vcut+L0)/c).                           (1)

Thus the ACTUAL low-velocity set has a fixed density cap under the field
amplitude bootstrap, even if its position or number of components changes.
This uses both fluid momentum invariants; continuity alone would not give it.

## 3. Exact mass-potential bound along every Q path

Exact stationary endpoints give conserved M=int_A^D n=int_A^D rho=O(ell).
Define m(theta,X)=int_A^X n(theta,Y)dY. Continuity and nv(A)=0 give
m_theta=-nv and m_X=n. Therefore along any actual Q characteristic of
speed lambda=+/-b, between its initial or first lateral starting contact
theta=s0 and any terminal theta=t,

  d_s m(s,X(s))=-(v-lambda)n,  0<=m<=M.               (2)

Split this path measurably into H={v>Vcut} and L={v<=Vcut}. On H,
v-lambda>1. On L, (1) gives n<=Ncut and
|v-lambda|<=Ccut:=Lambda+max(L0,Vcut). Integrating (2) gives

  int_H (v-lambda)n
    =m(s0,X(s0))-m(t,X(t))-int_L (v-lambda)n
    <=M+Ccut Ncut(t-s0).

Hence, without a crossing-count assumption, Jacobian estimate, density-gradient
bound or confinement of future resonance sets,

  int_s0^t n(s,X(s))ds <= M+(Ccut+1)Ncut(t-s0).        (3)

Repeated entries into H and L are covered by the same total signed identity.
No individual high-speed segment is assigned the whole mass and then summed.
Equation (3) is uniform over both Q families and their terminal points.

## 4. Closing the field amplitude bootstrap

Integrate each Q equation from its initial or lateral contact. Those data
are within C0 ell of z*. Equations (3) and the bounded regular source give

  |R_+/- (t,X)-R_+/-*|
   <=C0 ell+Hbar t+(C/tau)[M+(Ccut+1)Ncut t].          (4)

Scale characteristics also stop at the first initial/lateral contact, where
data are within C0 ell of z*, so

  |Z_+/- (t,X)-Z_+/-*|<=C0 ell+Zbar t.

At each fixed X, chi_t=w gives
|chi(t,X)-chi*|<=C0 ell+sup_K|w| t. Thus all field coordinates obey

  sup_I |z(t)-z*| <= C1 ell+C2 t.                    (5)

The constants are fixed in N; even a very large Ncut is finite and fixed.
At t<=Theta=B_dagger N^-4, (5) is <delta/2 for all sufficiently large N.
This strictly improves the bootstrap. Continuity and the first-exit argument
exclude any exit from K before Theta while the supposed classical branch
exists. In particular a loss of g positivity cannot occur as an unexamined
escape from the proof. No uniform first-derivative bound or classical restart
is used in this conditional upper-horizon argument.

We have derived |g|<=Gbar throughout I on every such candidate continuation.
This is an ACTUAL source-amplitude bound, not an assumed force hypothesis,
not an energy-only inference, and not a bound on g_X. It includes all future
low-speed and resonance points via (1)-(3). The constants and sufficiently-large
N condition depend on the chosen background/coefficient cell.

## 5. Actual transfer estimate and first-moment contradiction

For physical interpretation the field momentum is
F=-C^-1 int(tau p g+sigma w k), with the dimensionless fixed C here.
Direct equations give total momentum P+F=P0 and

  P'= -int_I (ng-rho g0),  F'=int_I (ng-rho g0), F(0)=0.

Pressure contributes -c^2[rho]=int rho g0, rather than vanishing separately.
Using M conservation, n>0, (5) and |g0|<=G0 gives

  |F(t)|<=M(Gbar+G0)t,
  |int_0^Theta F(t)dt|<=M(Gbar+G0)Theta^2/2.           (6)

Thus the actual signed transfer is O(N^-11) in dimensionless first-moment
units, far below its required O(N^-6) scale. No sign assumption is needed.
Let I1=int_I X n, R0=D M-I1(0)>0. The exact identities imply

  I1(Theta)=I1(0)+P0 Theta-int_0^Theta F.

Positive density demands I1(Theta)<D M. Initial polynomial integration gives
P0/(MN)->8/15 and R0/(M ell)->1. Divide the lower bound from (6) by M ell:

  [P0 Theta-R0-M(Gbar+G0)Theta^2/2]/(M ell)
    -> (8/15)B_dagger-1 >0,

since Theta^2/ell=B_dagger^2 N^-5. This contradicts the positive-density
moment capacity for sufficiently large N. Therefore no such positive
classical whole-packet branch survives through

  T=B_dagger (L/v0)N^-4, for any FIXED B_dagger>15/8,

once N exceeds the explicit finite conditions implicit in the fixed constants.
The limiting equality B_dagger=15/8 is not claimed. This proves only an upper
horizon in the diagnostic initial family, not the type of an earlier endpoint,
not a constructed shock, not a weak continuation and not physical instability
of the operative theory. FGF048 supplies a separate actual short lower time;
this proof does not replace its coefficient with B_dagger.

## 6. Energy, controls, branches and provenance

The full energy and both field fluxes remain those of FGF051/052, with n phi
interaction and Q/scale source cancellations. Fixed hydrostatic endpoints have
zero full energy flux. Equation (6) is not obtained from treating that energy
as a positive gradient norm. Ordinary unsigned energy can still lose a power
of N; the new bound instead uses the actual density transport and pressure
invariants. Static zero-velocity hydrostatics has P=F=P0=0 and constant I1;
it satisfies the source bound and does not trigger the positive-P0 contradiction.

Restore g by v0^2/L, mass by nref L, momentum by nref L v0 and first moment
by nref L^2. The force-transfer bound becomes
|int F_physical dt|<=M_physical (Gbar_physical+G0_physical) T^2/2.
Both a0 normalizations 9.3619e-11 and 1.1279e-10 m/s^2 have their own
compatible fixed background/coefficient constants. Constant vacuum and each
separately frozen a0 E(z), E²=.315(1+z)^3+.685, remain distinct. An evolving
reference generally destroys exact stationary exterior data and adds protocol
work; it is excluded. Dynamic Q sources are retained; no RAR/M/filtered-MONO,
metric/photon/vacuum/two-DOF, criterion B, cosmology or empirical promotion.
No literature mechanism or historical novelty claim. No mathematical executable
computation was run; this is a new analytic candidate requiring independent
raw-proof audit before promotion. Failures preserved: unsigned energy loss,
continuity-only trace inference, separate-segment mass overcounting, assumed
future-resonance confinement, and equality at the asymptotic horizon constant.
