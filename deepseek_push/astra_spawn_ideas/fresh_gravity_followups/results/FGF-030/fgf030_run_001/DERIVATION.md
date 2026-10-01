# FGF030: fixed physical couplings across four scale references

2026-09-30. Independently chosen coefficient box and constants for this task.
The energy-estimate method is inherited from reviewed FGF027. No stage16
candidate/audit was read. This is an analytic diagnostic Q comparison with
exact rational inequality checks, not a numerical orbit or observed fit.

## 1. One anchor and genuinely fixed physical parameters

Fix a_c=9.3619e-11 m/s², a_alt=1.1279e-10 m/s², cs=10^6 m/s and C=4piG.
Use ONE system of units for ALL members:

 L_c=cs²/a_c, t_c=cs/a_c, rho_c=a_c²/(C cs²),
 phi_c=cs², E_c=a_c cs²/C,
 x_phys=L_c x, t_phys=t_c t, B_phys=a_c B,
 g_phys=a_c g, rho_phys=rho_c rho,
 xi_phys=L_c xi, psi_phys=cs² psi, eta=delta chi.

E_c is energy per transverse area. Hold fixed

 J_phys=cs^4, S0_phys=a_c², K=c²/cs², v_chi=cs,
 physical length=L_c/100,
 B_phys(0)=a_c, rho_phys(0)=rho_c, chi(0)=0,
 chi_xphys(0)=1/(10000 L_c).

Thus dimensionless J=S0=1, K cs²/c²=1 and
J_phys/(v_chi² cs²)=1 in every member. Physical S0 does NOT follow a_ref².
Neither the units nor physical length nor left data are retuned.

Only the constitutive reference a_ref varies. Define
alpha=a_ref/a_c and beta=a_alt/a_c=112790/93619. The four separate stationary
cases are alpha=1, beta, E1, beta E1 with
E1=sqrt(641/200), because E(1)²=.315*8+.685=641/200.
Exact rational squares prove

 179/100 < E1 <1791/1000,
 1<beta<121/100, beta*(1791/1000)<11/5.

Hence ALL four lie in 1<=alpha<=11/5. The subsequent proof is uniform on
that entire alpha interval; its numerical audit is finite rational arithmetic
on the bounding constants, not a sampled parameter sweep.

The canonical and alternative constant-vacuum references are distinct
hypotheses. Their frozen H(z=1) references are two further stationary
comparisons, not a common dynamical cosmology or identical vacuum density.

## 2. Correct common-unit ODE, energy and kinetics

Write a=alpha exp chi, retaining the actual reference ratio. The common-unit
background equations are

 B'=rho, rho'=-rho g, g=sqrt(B²+aB),
 chi'=w, w'=sinh(2chi)/2-T(g,a),                      (1)
 (B,rho,chi,w)(0)=(1,1,0,1/10000), D=1/100.

The potential U=[cosh(2chi)-1]/4 is unchanged; there is no alpha² factor
in U or its derivatives. Q constitutive functions in anchor units satisfy

 A=b_g=2g/(2B+a)>0,
 q=gA-B=(a/2)[1-a/sqrt(a²+4g²)]>0,
 T(g,a)=integral_0^g (a/2)[1-a/sqrt(a²+4v²)]dv,
 m=cosh(2chi)-2T+gq.                                 (2)

The source law B'=rho is the dimensionless MOND constitutive-flux equation,
not a Newtonian force replacement. Physical force is g_phys=a_c g.

For u=(xi,psi,eta) in the fixed zero-trace space H1_0(0,D)^3, the original
regular quadratic potential Q2=2V/E_c and kinetic mass norm N are

 Q2=integral {[(rho xi)']²/rho-2(rho xi)'psi
          +A psi'²-2q eta psi'+eta'²+m eta²}dx,
 N=integral[rho xi²+psi²+eta²]dx.                     (3)

The dimensionless frequency quotient is Omega²=Q2/N and physical
omega²=(a_c/cs)² Omega² for EVERY case, not (a_ref/cs)² Omega².
Both positive field kinetic terms remain in N. All component norms in the
proof use these fixed anchor units.

Right wall field values and pressure are induced by each IVP, so they and
total background mass need not coincide across alpha. Mass is conserved
under perturbations within each member. This is no moving-wall dynamics,
fixed-total-mass family across references or empirical normalization fit.

## 3. Chosen uniform analytic box

Choose the bootstrap box

 9/10<=B,rho<=11/10, |chi|<=1/100, |w|<=1/40.          (4)

Since exp(-1/100)>99/100 and exp(1/100)<100/99,

 99/100<a< (11/5)(100/99)=20/9<9/4.

Then
g²>81/100+(99/100)(9/10)=1701/1000>(13/10)² and
g²<121/100+(9/4)(11/10)=737/200<4, so

 13/10<g<2, A> (13/5)/(89/20)=52/89>1/2, q<9/8.      (5)

For a positive lower bound on T, integrate only v in [13/20,13/10],
which lies inside [0,g]. Throughout that subinterval,

 1+4v²/a²>1+4(13/20)²/(9/4)²=2701/2025>(23/20)².

Therefore a/sqrt(a²+4v²)<20/23 and

 q(v,a)>(99/200)(3/23)=297/4600,
 T>(13/20)(297/4600)=3861/92000>1/25.                 (6)

On the other hand, q(v,a)<=a/2 gives T< (9/8)*2=9/4.
The fixed U obeys
|U'|<=|chi|exp(2|chi|)<=1/98<11/1000. Hence

 -23/10 < w' < -1/40.                               (7)

Indeed the tighter intermediate bounds are
w'>-9/4-11/1000=-2261/1000>-23/10 and
w'<11/1000-1/25=-29/1000<-1/40. No approximate exp, sinh, sqrt or ODE
values enter these coefficient inequalities.

## 4. Box closure, turn brackets and shared physical endpoint

As long as (4) holds, integrate the bounds for 0<=x<=D:

 1<=B<=1+(11/10)D=1011/1000<11/10,
 rho>=1-(11/10)*2D=489/500>9/10, rho<=1,
 |chi|<=D/40=1/4000<1/100,
 w>=1/10000-(23/10)D=-229/10000>-1/40,
 w<=1/10000<1/40.

Every face stays strictly interior. The standard first-exit contradiction
therefore keeps all four IVPs in the compact smooth regular box through D;
local existence extends throughout this interval. This is a continuum ODE
enclosure, not observations of sampled trajectory points.

Equation (7) makes w strictly decreasing. Each member has exactly one first
scale-slope zero d_* within the COMMON bracket

 1/23000 < d_* <1/250<D=1/100.                        (8)

At D, -229/10000<w(D)<-3/20000<0. Thus each full fixed physical length reaches
past its own scale turn. Every extension beyond the turn exceeds
1/100-1/250=3/500 in anchor length units. The member-specific turns need
not agree; only their common enclosure is proved.

No singular formula dividing by w is used beyond the turn. It is chi'
that changes sign, not the positive gravitational field g.

## 5. Uniform continuum gap in the original form

The fluid square in (3) obeys

 [(rho xi)']²/rho >=(rho/2)xi'²-(rho'^2/rho)xi²
                  >=(9/20)xi'²-(22/5)xi²,

because rho'^2/rho=rho g²<(11/10)*4=22/5.
With xi=psi=0 at both walls,
-2 integral(rho xi)'psi=2 integral rho xi psi'; the exact omitted endpoint
is -2[rho xi psi]=0. Allocate A psi'²/4 to each coupling:

 2rho xi psi'>=-(A/4)psi'²-(4rho²/A)xi²,
 -2q eta psi'>=-(A/4)psi'²-(4q²/A)eta².

The box gives
4rho²/A<242/25, 4q²/A<81/8,
m>1-2*(9/4)=-7/2.
Therefore

 Q2>= integral[(9/20)xi'²+(1/4)psi'²+eta'²
               -(352/25)xi²-(109/8)eta²]dx
    >=(1/4)||u'||_2²-15||u||_2².                    (9)

This bound retains both fields and every coupling, irrespective of w's sign.
For H1_0, Dirichlet Poincare and pi²>9 with D=1/100 imply

 Q2>=(1499/6000)||u'||_2²,
 Q2>=22485||u||_2²,
 N<=(11/10)||u||_2²,
 inf_(u!=0) Q2/N>=224850/11>20400.                   (10)

Consequently every one of the four stationary cases satisfies the SAME
physical continuum lower bound

 omega_min² >=20400 (a_c/cs)²,                       (11)

on the SAME physical interval L_c/100. The bound is conservative and does
not imply equal spectra or equal background profiles. It also applies to
shorter same-reference prefixes, with their newly induced right endpoints.

This is a continuum lower-bound theorem, not positivity of a finite
eigensolver output. The arithmetic certificate checks rational constants;
the analytic inequalities and first-exit/energy argument establish the
uniform claim. No mesh, ODE samples, spectral approximation or calibrated
physical likelihood is produced.

The original field-energy boundary flux is zero at the selected fixed
traces. If static potential elimination is used later, its Dirichlet square
still leaves [integral(rho xi-q eta)/A]²/integral(1/A). This exact rank-one
term has not been falsely set to zero; here no field is eliminated at all.

## 6. Reference cases and controls against hidden retuning

Case labels are canonical vacuum, alternative vacuum, canonical frozen H1,
alternative frozen H1. In all four, length, time unit, S0,J,K,v_chi,cs,
left B,rho,chi and physical initial scale gradient are identical. Only
alpha in a=alpha exp chi changes.

At alpha=1 the ODE, units, coefficients and domain recover the FGF027
canonical case exactly. Its earlier stronger gap >32700 remains valid
there. The shared >20400 lower bound is deliberately weaker because it
covers the changed-reference cells uniformly. FGF027's other restored
families retuned S0 and length; they are not used as results for these cells.

Exact controls in the rational certificate:
- Square the proposed E1 enclosure endpoints and verify 641/200 is strictly
  between them. Every alpha is enclosed; alpha is not set to1 by fiat.
- For each of the three noncanonical cases alpha²!=1. Retuning physical
  S0 to a_ref² would therefore change fixed S0 by alpha², and replacing
  L_c by cs²/a_ref would change physical length by 1/alpha. These mutations
  are rejected, not treated as equivalent nondimensionalization.
- The force at the initial point has g0²=1+alpha. Holding g0²=2 while
  changing alpha contradicts the actual Q initial-force equation.
- Frequency restoration uses a_c/cs for every row. Inserting an alpha²
  factor in the common gap would use a different time unit.
- An undersized T upper bound, overspent Young stiffness budget, or a
  no-turn claim at the final wall violates an exact certificate comparison.
- The algebraic nonadmissible fixture rho=xi=1,psi=x has original coupling
  zero, integrated coupling 2D and endpoint -2D. This detects a boundary
  term incorrectly dropped outside the selected Dirichlet domain.

No failed old shortness inequality is demonstrated. This remains a strong
small-domain certificate, now at fixed physical couplings and initial data.

## 7. Physical interpretation and exact residual gap

The constant-vacuum references a_c and a_alt may separately be assigned
a_ref=kappa c sqrt(G rho_Lambda,ref), with adopted kappa. The frozen H1
references are distinct stationary choices; this calculation does not solve
an evolving H trajectory, conserve energy between different reference
members or assert the same vacuum density for different a_ref.

The actual a(x)=a_ref exp chi(x) varies, so the literal pointwise
constant-vacuum actual-a incompatibility remains. Q source balance is used
throughout. Neither the RAR law nor a registered M local action was evaluated.
No new metric/photon action, empirical endpoint calibration, observed
normalization preference, nonlinear/3D stability, free-boundary result or
theory closure follows.

This certificate shows that these four reference choices do not destroy
linear fixed-wall stability of the specified diagnostic slab when physical
couplings and left data are held fixed. It supplies no likelihood favoring
one normalization. The material open question is whether the fixed couplings
and induced boundary model are independently physically justified; another
small stable toy spectrum would not answer it.
