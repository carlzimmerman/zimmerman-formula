# FGF045 root attempt: conditional short lifespan with pressure and bounded force

2026-10-06. Independent construction before reading any stage32 author/reviewer
proof or conclusion. This is a local fixed-potential diagnostic. It excludes a
positive C1 solution on a specified short cone for sufficiently large N; it does
not construct a solution or invoke a continuation/existence theorem.

Fix a closed regular interval U=[x*-R,x*+R] on the positive side of the inherited
Q crossing, strictly away from its center and physical walls. Background rho>0,
phi0 and g=phi0_x are smooth there, cs² rho_x=-rho g. Take cs>0, fixed nref>0,
eta=n/nref, and the exact initial profile v=V f((x-x*)/ell), n=rho, with
V=v0 N, ell=L/N³, A=V/ell=(v0/L)N4. f=(1-y²)² on |y|<1, otherwise zero;
f is C1,1 and f' has extremal magnitude D=8/(3 sqrt(3)).
All constants below except A,V,ell and explicit N thresholds are independent N.
Assume a positive C1 solution of the actual equations on the cone considered:

n_t+(nv)_x=0,  v_t+v v_x+cs²(log eta)_x=-g(x).                       (1)

No stationary velocity, fixed support, or incoming mass assumption is made.

## Characteristic identities, including the force

Set r=v+cs log eta, l=v-cs log eta, D±=partial_t+(v±cs)partial_x.
Direct substitution yields D+ r=-g and D- l=-g. Set alpha=r_x,beta=l_x.
Differentiation along their characteristic families gives

D+ alpha=-(alpha+beta)alpha/2-g',
D- beta=-(alpha+beta)beta/2-g'.                                    (2)

These identities require no second spatial derivative in the final equations:
for C1 solutions, differentiate the integral characteristic formula with
respect to the initial label. The characteristic Jacobian solves the scalar
linear variational ODE with coefficient (alpha+beta)/2. This proves the
continuous-gradient integral version of (2). Piecewise smooth C1,1 initial
endpoints are allowed; no second-derivative continuity is assumed.

Put w=eta^(-1/2), a=w alpha, b=w beta. From D+log eta=-beta and
D-log eta=-alpha, cancellation of the mixed terms in (2) gives

D+ a=-a²/(2w)-w g',   D- b=-b²/(2w)-w g'.                         (3)
D0 w=(a+b)/4, D0=partial_t+v partial_x.                           (4)

Pressure is retained in cs, the characteristic speeds, and both gradients.
The force-gradient term is not dropped. These are elementary identities of
(1), not a pressureless approximation or a cited shock mechanism.

## Cone and coefficient bounds

Fix a small physical T0>0. Let G=sup_U |g| and M=sup_U |g'|, and
B=cs sup_U |log(rho/nref)|. Initial |r|,|l|<=V+B. On a characteristic
cone whose backward characteristics stay in U, |r|,|l|<=V+B+Gt.
Choose speed C_N=V+B+G T0+cs+u*, where u*>0 is any fixed physical speed,
and cone K_t=[x*-R+C_N t,x*+R-C_N t]. The same characteristic bounds give
|v±cs|<C_N for t<=T0. A first-exit/bootstrap argument therefore keeps every
backward +,- and material characteristic from K_t in the earlier K_s. The
cone is nonempty for the times used below. This local argument does not assert
anything about evolution through the nonsmooth background crossing or walls.
It also gives, at each finite N, finite positive upper/lower bounds on n
through log eta=(r-l)/(2cs), though not bounds uniform in N.

Let W0=sup_U sqrt(nref/rho), w0=inf_U sqrt(nref/rho)>0.
For A>=G/cs, the initial positive parts of a,b are bounded by
P0<=p A, p=W0(D+1). Let W(t)=sup_Kt w and P(t)=sup_Kt max(0,a,b).
Equations (3)-(4) along their respective contained characteristics imply

P(t)<=P0+M integral_0^t W(s)ds,
W(t)<=W0+(1/2) integral_0^t P(s)ds.                              (5)

Upper envelopes can be used if a supremum is not attained. Iterating the
nonnegative Volterra kernel, or solving the corresponding equality system,
gives k=sqrt(M/2) and

W(t)<=W0 cosh(kt)+(P0/(2k))sinh(kt).                             (6)

At M=0 interpret the second term as P0 t/2. For kt<=1, cosh(kt)<=2
and sinh(kt)/(kt)<=2, hence with s=A t

w(t,x)<=W(t)<=2W0+p s =: Wbar(s).                               (7)

This is the needed density lower control. It was DERIVED from actual pressure
and force equations; no uniform density cap or positive-gradient cap is assumed.

## Compressive characteristic and contradiction

Start the + characteristic at x_N=x*+ell/sqrt(3). Here f'=-D and
alpha(0)= -D A-g(x_N)/cs. On our positive side g>0, so
-a(0)/A>=d, d=w0 D>0. (The proof could use d/2 for an arbitrary sign
of bounded g after increasing N; that extension is not needed.)

Define z(s)=-a(t,X+(t))/A. Equation (3) gives

z_s=z²/(2w)+(w g')/A² >= z²/(2w)-M w/A².                        (8)

Choose the fixed dimensionless number

S=(2W0/p)[exp(8p/d)-1].                                         (9)

It may be very large; no useful numerical sharpness is claimed. Increase N
until all of these explicit gates hold:
A>=G/cs; S/A<=T0; k S/A<=1;
M Wbar(S)²/A²<=d²/4;
ell/sqrt(3)+2 C_N S/A<R.                                       (10)

They can all hold: A~N4, C_N~N, ell~N^-3. The last gate keeps the
forward chosen characteristic strictly inside K_t, since its displacement is
at most C_N t. Equation (7) applies on its full interval if a C1 solution
exists there. While z>=d, (8) and (10) imply

z_s>=z²/[4 Wbar(s)]>0.                                         (11)

Thus z stays >=d by continuity. Integrating (1/z)'<=-1/[4Wbar(s)]
yields

1/z(S)<=1/z(0)-(1/(4p))log(1+p S/(2W0))
       <=1/d-2/d<0,                                            (12)

which is impossible for finite positive z. There is no positive C1 solution
on that entire cone through T_N=S/A=(SL/v0)N^-4 for all sufficiently large N.
In particular no N-independent common smooth lifespan can cover these local
initial data. This is a conditional lifespan obstruction, not a local existence
or actual shock-construction theorem. If a smooth evolution is supplied and
persists up to a maximal endpoint within this cone, the Riccati estimate forces
loss of bounded gradients before the bound; the characteristic r,l bounds
preclude finite-N zero or infinite density while those identities hold. No
post-breakdown weak solution or entropy selection has been constructed.

The roots of the argument are a negative initial gradient of order N4 and the
linear-in-scaled-time bound on reciprocal square-root density. The crude finite
S in (9) closes the logarithmic comparison integral; replacing its denominator
by Wbar(S) would give an unhelpful inequality and is not used.

## Exact energy, source residual and controls

With e(n)=cs² n(log(n/nref)-1), define H=nv²/2+e+n phi0.
Directly multiply momentum by nv and use continuity to obtain

partial_t H+partial_x Q=0,
Q=v[nv²/2+cs² n log(n/nref)+n phi0].                            (13)

A fixed time-independent potential does no unaccounted work: its interaction
term cancels -nv g. Integrating conserves H only on a domain with appropriate
zero energy flux, or includes the actual boundary work otherwise. The moving
cone has boundary contributions; no global energy conservation claim follows
there without those terms. A smooth full-wall realization, if supplied, obeys
its corresponding conditional energy identity. This removes the prescribed-
velocity energy defect of FGF044 only for actual smooth fluid solutions.

Frozen Q fields still have Rphi=C(n-rho), C=4piG, and Rchi=0; there is no
reason for Rphi to vanish for this actual fluid evolution. No bound on its
post-initial size or a full gravity solution is inferred here. No Newtonian
missing-mass substitution is made. Zero velocity with n=rho exactly solves
(1) and has Q=0: the hydrostatic control has no order-N4 negative gradient
and does not satisfy our compression premise.

Both a_ref=9.3619e-11 and 1.1279e-10 m/s² use their own signed-Q background.
The cs, nref, v0,L,R and force bounds keep physical units: A,k are inverse time,
G acceleration, M inverse time squared, w,p,d,S dimensionless. Constant-vacuum
and frozen H(z) comparisons remain separate from an evolving reference. No
transfer to RAR/M, filtered MONO, criterion B, physical metric/photon/DOF,
conserved scale reservoir, observations, historical novelty or theory closure.
The unbounded diagnostic speed sequence is not a physical superluminal claim.

Attempt limitations: all existence statements are hypotheses, not proved local
well-posedness. No numerical runs, no estimate of a sharp breakdown time, no
nonlinear continuation, no transport/flux theorem after breakdown. The next
missing physical step remains an admissible solution of the coupled system;
one may first test whether dynamic Q/scale fields preserve the force-gradient
control needed here. This does not follow from an energy bound alone.
