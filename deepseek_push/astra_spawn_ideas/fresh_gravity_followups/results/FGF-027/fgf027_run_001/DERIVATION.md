# FGF-027: explicit continuum gap beyond the first turn

2026-09-30. Diagnostic Q branch only. The parent /root proposed the initial
data, box and analytic-certificate route. This worker independently derived
the constants, first-exit proof, energy bound and dimensional realization.
This is an exact continuum bound, with a finite rational arithmetic audit;
it is not a computed orbit, a mesh spectrum or an empirical fit.

## 1. Dimensionally consistent selected family

Let C=4piG, c be the physical speed of light, and fix cs=10^6 m/s.
For each chosen positive reference acceleration a_*, set

 L=cs²/a_*, t_*=cs/a_*,
 rho_*=a_*²/(C cs²), phi_*=cs², E_*=a_* cs²/C,
 B=a_* u, g=a_* f, rho=rho_* r, x=L X, t=t_* S,
 xi=L zeta, psi=cs² P, chi=chi, eta=eta.

E_* is energy per transverse area. Choose physical parameters

 J=cs^4, S0=a_*², v_chi=cs, K=c²/cs².

These give dimensionless J=S0=cs²=1 and kinetic coefficients
K cs²/c²=1 and J/(v_chi² cs²)=1. Dimensionless source density is r,
so the dimensionful C is absorbed into rho_*; physical G is not set to one.
Positive K is a declared diagnostic parameter, not an inferred coupling.

Below, for readability, write x,B,rho,g,xi,psi for X,u,r,f,zeta,P.
The dimensionless background equations are

 B'=rho, rho'=-rho g, g=sqrt(B²+aB), a=exp chi,
 chi'=w, w'=U'-T, U'=sinh(2chi)/2.                    (1)

The ONLY selected IVP and full endpoint are

 B(0)=rho(0)=1, chi(0)=0, w(0)=1/10000, D=1/100.       (2)

The Q law is evaluated; no R or M stability result is asserted. The left
potential value can be fixed to zero and integrated via phi'=g. Both field
endpoints and wall pressures are induced by this solution. Total mass is
fixed under each member's perturbations but changes across prefix endpoints.
The family is not moving-wall evolution or a fixed-mass global sequence.

## 2. Exact analytic box and force bounds

Use the closed bootstrap box

 9/10<=B,rho<=11/10, |chi|<=1/100, |w|<=1/100.         (3)

Elementary exponential inequalities give
99/100<=a<=100/99<51/50. In particular a in [99/100,51/50].
With (3),

 g²>=81/100+891/1000=1701/1000>(13/10)²,
 g²<=121/100+561/500=583/250<(8/5)².

Thus 13/10<g<8/5. The Q inverse derivatives are

 A=b_g=2g/(2B+a), q=gA-B
     =(a/2)[1-a/sqrt(a²+4g²)]=aB/(2B+a)>0.
 T(g,a)=integral_0^g q(v,a)dv.                        (4)

Consequently q<=51/100 and
A> (13/5)/(161/50)=130/161>4/5.

To lower-bound T, integrate only v in [13/20,13/10], a subset of [0,g].
For this range sqrt(a²+4v²)>8/5, since
(99/100)²+4(13/20)²>64/25. Hence

 q(v,a)> (99/200)[1-(51/50)/(8/5)]=2871/16000,
 T> (13/20)(2871/16000)=37323/320000>11/100.

For the upper bound, q(v,a)<=a/2 gives T<(51/100)(8/5)=102/125<41/50.
Also |sinh(2chi)|/2<=|chi|exp(2|chi|)
 <=(1/100)/(1-1/50)=1/98<11/1000.
Therefore

 -21/25 < w' < -9/100.                               (5)

The constants are deliberately conservative; no transcendental approximation
or unvalidated numerical integration supplies these inequalities.

## 3. First-exit existence, turn and explicit full extension

As long as (3) holds, (1) and (5) imply for 0<=x<=D

 1<=B<=1+(11/10)D=1011/1000,
 1-(44/25)D=614/625<=rho<=1,
 |chi|<=D/100=1/10000,
 1/10000-(21/25)D=-83/10000<=w<=1/10000.

Every bound is strictly interior to the corresponding box faces. A putative
first box exit by time D contradicts these integrated estimates. The smooth
ODE thus exists through D in a compact regular region with positive B,rho,g.

Since w is strictly decreasing and w(0)>0, (5) implies its unique first zero
d_* satisfies

 1/8400 < d_* < 1/900 < D=1/100.                      (6)

The full selected prefix is therefore rigorously beyond the first turn.
At the final wall,

 -83/10000 < w(D) < -8/10000 <0.

The length extending beyond the turn obeys
D-d_*>1/100-1/900=2/225. These are dimensionless inequalities for this
same IVP prefix. No small centered substitute or fabricated ODE samples are
used. Physical lengths follow by multiplication by L.

## 4. Original nonsingular continuum energy bound

Keep the physical H1_0 perturbation domain for xi,psi,eta on [0,D].
The dimensionless original quadratic potential Q=2V/E_* and kinetic mass
norm N (whose frequency quotient is Omega²) are

 Q=integral {[(rho xi)']²/rho-2(rho xi)'psi
         +A psi'²-2q eta psi'+eta'²+m eta²} dx,
 N=integral[rho xi²+psi²+eta²]dx,
 m=cosh(2chi)-2T+gq.                                 (7)

This preserves the fluid, potential and scale couplings. It uses no expression
dividing by w beyond the turn. Since T<41/50 and gq>0,
m>1-82/50=-16/25.

The elementary inequality (u+v)²>=u²/2-v² applied to the fluid square gives

 [(rho xi)']²/rho >= (rho/2)xi'²-(rho'^2/rho)xi²
                >= (9/20)xi'²-(352/125)xi²,          (8)

because rho'^2/rho=rho g²< (11/10)(64/25)=352/125.
Integration by parts gives -2 integral(rho xi)'psi=2 integral rho xi psi';
the dropped endpoint is precisely -2[rho xi psi]=0 by the declared walls.

Young inequalities allocate one quarter of A psi'² to each cross term:

 2rho xi psi' >= -(A/4)psi'²-(4rho²/A)xi²,
 -2q eta psi' >= -(A/4)psi'²-(4q²/A)eta².

Using A>4/5, rho<=11/10 and q<=51/100 gives
4rho²/A<=121/20 and 4q²/A<=2601/2000. Therefore

 Q >= integral[(9/20)xi'²+(2/5)psi'²+eta'²
              -(8866/1000)xi²-(3881/2000)eta²]dx
   >= (2/5)||u'||_2²-9||u||_2², u=(xi,psi,eta).       (9)

All component norms here are dimensionless in Section 1's fixed scales.
No field is statically or dynamically discarded.

For Dirichlet functions, ||u||_2²<=D²||u'||_2²/pi².
Using pi²>9 and D=1/100, (9) implies

 Q >= (3999/10000)||u'||_2²,
 Q >= 35991||u||_2²,
 N <= (11/10)||u||_2²,
 inf_(u!=0) Q/N >=359910/11 >32700.                   (10)

These are lower bounds on the FULL continuum form and generalized spectral
infimum. They are not finite-element eigenvalues, interpolation estimates or
a positivity inference from finite sampling. The same conservative bound
32700 applies to every shorter prefix D'<=1/100; its endpoint parameters
are induced anew from (2). In particular the entire segment beyond d_* up
to 1/100 is certified, with its actual negative w region.

The proof uses a strong small-domain derivative bound. It does NOT exhibit
failure of the earlier shortness condition or claim to evade it. Its new
content is a fully specified regular continued prefix, explicit first-turn
bracket and an explicit continuum gap with kinetic weights.

## 5. Wall compatibility and controls

No static elimination was needed in (7)-(10). If psi is minimized, its square
still leaves [integral(C_dimless rho xi-q eta)/A]²/integral(1/A), with
C_dimless=1. Claiming this exact residual vanishes is forbidden. The lower
bound instead controls the full original form, including both fields.

The finite arithmetic certificate verifies every displayed rational comparison,
the strict first-exit margins, the turn bracket, the Young budgets, and (10).
These are exact Fraction checks; it does not evaluate an approximate orbit.

Negative/domain controls:
- An alleged upper T bound 1/10 is below the derived lower bound and is
  rejected; a too-small force drive would invalidate the turn certificate.
- A claimed first-zero-free endpoint conflicts with w(D)<-8/10000.
- Spending three quarters of A psi'² on EACH coupling leaves negative
  remaining stiffness and is rejected, unlike the two valid quarter budgets.
- For the purely algebraic nonadmissible fixture rho=xi=1, psi=x on [0,D],
  the integrated coupling is 2D but the original coupling is zero; the
  endpoint -2D restores equality. Dropping it outside Dirichlet conditions
  fails. This is not a second hydrostatic model.
- Removing a MOND term is not tested as if it were the same Q problem:
  g²=B²+aB and B'=rho remain explicit throughout.

## 6. Both reference normalizations and distinct histories

Use a_*=a0 separately for a0=9.3619e-11 and 1.1279e-10 m/s².
As a distinct stationary comparison use a_*=a0 E(3),
E(3)²=.315*4³+.685=4169/200. All four are restorations of the same
dimensionless Q family, not four observational fits or dynamically evolved
cosmologies. Changing a_* also changes rho_*, S0 and physical length.
No R-law orbit or bound was evaluated.

For each of those four references the exact statements are

 physical d_*=L d_*dimless in (cs²/(8400 a_*),cs²/(900 a_*)),
 full length=cs²/(100 a_*),
 extension beyond turn > 2cs²/(225 a_*),
 physical omega_min² >=32700 (a_*/cs)²,                (11)

with cs=10^6 m/s, K=(299792458/10^6)², J=10^24 m^4/s^4,
v_chi=10^6 m/s, S0=a_*², and initial rho=a_*²/(4piG cs²).
The first-exit and continuum gap proofs are independent of numerical G
because it enters the density unit, not the dimensionless source equation.

The reference may obey a_*=kappa c sqrt(G rho_Lambda,ref), but actual
a(x)=a_* exp chi(x) varies. The literal pointwise constant-vacuum actual-a
interpretation is still incompatible without additional physical changes.
No registered M action, filtered-MONO, physical photon/metric, nonlinear/3D,
free-wall, measured-size, empirical-likelihood or theory-closure result follows.
All parameter and wall choices here are illustrative.

Next useful work should constrain or derive those free coefficients and
physical boundary data, or test a specifically different longer regime with
a controlled continuum estimate. Another mesh spectrum on this already
certified interval would add little and is not requested.
