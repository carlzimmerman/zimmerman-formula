# W4-08: positive MOND responses and normalization tests

Units c=hbar=1 unless stated. The physical target is xi=a0^2/(G epsilon_DE).
For one mediator with energy C2 h^2 at high gradient and C3|h|^3 at low
gradient, source q rho_b phi and physical g=q|grad phi|, spherical flux gives
G_n=q^2/(2Omega C2), a0=2qC2/(3C3) and
R=epsilon C3^2/C2^3; xi=8Omega/(9R). Omega=area S^(n-1).
The target R=128pi/9 is specific to n=3 and this force dictionary.
Energy asymptotes here include their derivative asymptotes.

## A. A complete homogeneous critical Dirac-band response

Take a physical finite two-dimensional Dirac band with positive velocity v,
energy edge L, positive band degeneracy per bulk layer spacing absorbed
into A>0, and a mass m=y h, h=|grad phi|, y>0. The negative filled-band
energy is

    -A[(L^2+y^2h^2)^(3/2)-|yh|^3].

One critical local quadratic coefficient C2=(3/2)A L y^2 cancels its
quadratic IR term. Above the raw band baseline, the homogeneous energy is

    E(h)=A[L^3+(3/2)L y^2h^2-(L^2+y^2h^2)^(3/2)+|yh|^3].

This specified fixed-background determinant has positive cubic IR and
quadratic UV: C3=A y^3 and C2=(3/2)A L y^2. Put t=yh/L>0. Its response
in units of 2C2 h is

    mu(t)=1+t-sqrt(1+t^2),
    mu+t mu'=1+2t-(1+2t^2)/sqrt(1+t^2).

Both are strictly positive and less than one. For positivity of the
second, compare squares of the positive sides:

    (1+2t)^2(1+t^2)-(1+2t^2)^2=4t+t^2+4t^3>0.

For its upper bound use (1+2t^2)^2-4t^2(1+t^2)=1>0. The radial and
tangential homogeneous static Hessians therefore have the claimed signs
at every h>0. With an independently supplied local time kinetic coefficient
2C2/c^2, the *adiabatic local toy* has subluminal linear speeds. That toy
does not replace the true frequency-dependent determinant below.

The same state's raw energy at h=0 is negative: epsilon_raw=-A L^3,
R_raw=-8/27. Setting epsilon=+sigma A L^3 gives R=8sigma/27, but adds a
new positive-vacuum prescription. It does not derive sigma=48pi.
The critical tuning itself is an input defining a critical surface, not
an asserted symmetry protection against all quantum corrections.

## B. Positive paired-spectrum energy with no separate offset added

Use equal bosonic and fermionic band weights, fermion squared gap z=y^2h^2,
boson squared gap z+Delta^2, with Delta>0. Grant the parent cancellation
prescription D=0 at Delta=0. The same regulated homogeneous energy is

    D(z)=A[(L^2+Delta^2+z)^(3/2)-(Delta^2+z)^(3/2)
           -(L^2+z)^(3/2)+z^(3/2)].

It has the integral representation

    D(z)=3A int_0^L k dk [sqrt(k^2+z+Delta^2)-sqrt(k^2+z)].

Thus D(0)>0, D'(z)<0 and D''(z)>0 for z>0, with D'(0) finite.
Choose the one critical subtraction B=-D'(0)>0 and E(h)=D(y^2h^2)+B y^2h^2.
Then E_z=D'(z)-D'(0)>0 and E_zz=D''(z)>0. Its tangential and radial
static Hessians are respectively 2y^2 E_z and 2y^2 E_z+4y^4h^2 E_zz,
strictly positive for h>0. This proves full homogeneous convexity without
a parameter scan. It does not prove dynamical health of all fermionic
and bosonic fluctuations in a nonuniform background.

For d=Delta/L, b=1+d-sqrt(1+d^2)>0 and
f=(1+d^2)^(3/2)-1-d^3>0, its actual homogeneous coefficients are

    epsilon_band=A L^3 f,
    C2=(3/2)A L y^2 b,
    C3=A y^3,
    R_band(d)=(8/27)f/b^3.

The coupling y, band weight A (including species/hbar) and scale L cancel.
This is stronger than a bare vacuum-offset objection. A physical gap ratio
d nevertheless survives.

Let s=1+d, r=sqrt(1+d^2), u=r/s. Algebra gives

    f=b^2(s+2r)/2,
    R_band=(4/27)(1+2u)/(1-u),
    1/sqrt(2)<=u<1,
    R_band(d)=R_band(1/d),
    min_(d>0) R_band=(16+12sqrt(2))/27 at d=1.

The last follows because u^2=(1+d^2)/(1+d)^2 has its unique minimum at
d=1 and the displayed rational function is strictly increasing in u.
Reciprocal invariance is a mathematical property, not a demonstrated
microscopic symmetry interchanging a physical gap and a band edge.

Matching the target would require

    u=(96pi-1)/(96pi+2),
    d=[u^2 +/- sqrt(2u^2-1)]/(1-u^2).

These are imposed matching conditions on a free microscopic gap, not
predictions or results of a scan. For every positive algebraic d, R_band
is algebraic and therefore differs from 128pi/9 by pi's transcendence.
This is an exclusion only for that coefficient class, not arbitrary
interacting gap equations or transcendental microscopic amplitudes.

The positive epsilon_band must not be called epsilon_DE without its stress
and background dynamics. For the same physical cutoff, one sheet has

 rho=D(0),
 p_parallel=(3A/2) int_0^L k^2 dk[k/sqrt(k^2+Delta^2)-1],
 rho+p_parallel=(3A/2)L^2[sqrt(L^2+Delta^2)-L]>0.

This stress is not a Lorentz vacuum. A dynamical membrane tension or a
layer-density stabilizer changes the stress prescription and adds physics;
it is not implied by the positive homogeneous determinant. There is no
claimed complete supersymmetric realization of the whole gap family.

## C. Frequency, geometry and source-profile restrictions

In a translationally invariant continuum two-dimensional Dirac sector,
or a sufficiently smooth local UV realization, the quadratic mass bubble's
leading infrared nonanalytic term after local subtractions has dependence
proportional to

    sqrt(omega_E^2+v^2 k_parallel^2),

or sqrt(v^2 k_parallel^2-(omega+i0)^2) after retarded continuation.
For a gradient-mass coupling the scalar kernel also contains its external
gradient factors, giving k^2 times that square root, not a purely local
cubic-energy wave operator. The continuum starts at |omega|=v|k_parallel|.
At finite mass m, its pair threshold becomes sqrt(4m^2+v^2k_parallel^2).
For one two-component continuum Dirac fermion, rescaling v=1 and writing
p=sqrt(omega_E^2+k_parallel^2), Feynman parameterization gives

 Pi(p,m)=(p^2+4m^2)/(4pi p) arctan[p/(2|m|)]-2J(m),
 J(m)=int d^3l/(2pi)^3 1/(l^2+m^2).

The integral used here is
int d^3l/(2pi)^3 [(l^2+m^2)((l+p)^2+m^2)]^-1
=arctan[p/(2|m|)]/(4pi p). Subtracting Pi(0,m) removes J;
at m=0, Pi(p,0)-Pi(0,0)=p/8. This is a direct continuum bubble
calculation, not an attribution to the homogeneous Gross-Neveu potential.
The homogeneous finite-band energy does not specify its full nonuniform
kernel or band-projection vertex. A hard momentum-disk projection can add
nonanalytic boundary terms from the intersection of shifted disks; it
cannot be assumed to give only analytic UV corrections. The displayed
continuum kernel and pair threshold therefore carry the continuum/smooth
local UV assumption, not a claimed unique sharp finite-band kernel.
A local adiabatic expansion requires |omega|,v|k_parallel|<<m. This range
shrinks as h->0; static homogeneous convexity alone cannot establish an
all-radius MOND solution.

In a formal spherical deep-MOND profile, h=sqrt(GMa0)/(q r), so
v/(m r)=v q/[y sqrt(GMa0)] is independent of radius and depends on source
mass. A controlled adiabatic source range must satisfy that inequality;
one cannot infer it from low acceleration alone.

The mass |yh| can be obtained spectrally from analytic linear couplings
to gradient components using two kinetic and three mutually anticommuting
mass matrices in a four-component 2D Dirac Hamiltonian. This doubles a
minimal two-component Dirac content and changes the band weight A. It
does not remove a layer geometry or produce a four-dimensional Lorentz
vacuum. A discrete set of componentwise sheet masses can instead yield
an anisotropic sum of cubes; an isotropic continuum assumption is additional.
Neither implementation is certified here as a complete local UV gravity
model. These are specific response constructions with explicit limits.

For a true interacting Gross-Neveu order parameter sigma with V~|sigma|^3,
coupling a physical source as -J sigma and minimizing does not allow one
to set sigma=yh. Its minimized contribution instead scales negatively as
|J|^(3/2). A gradient-mass identification or a constrained order parameter
must be derived in a separate completion, not inferred from the exponent.

## D. A documented two-field superfluid parent

Take the d=4 two-field superfluid of arXiv:2009.03003v3, signature +---,
Mp^-2=8piG. Define K_+/-=(partial theta_+/-)^2, Z=K_++K_--m^2 and

 L=1/2[(partial r_-)^2+r_-^2(K_--m^2)]-lambda4 r_-^4/4
   +(2Lambda/3)Z sqrt(|Z|)-lambda theta_+ rho_b-V0.

The theta_- symmetry is exact; its conserved-charge ensemble permits
theta_-=mu t. The sourced theta_+ is not assigned an exactly conserved
chemical potential. On a locally constant sourced branch set
u=mu^2-m^2>0, q=|grad theta_+|, s^2=q^2-u>0, r_-^2=u/lambda4,
with all couplings m,Lambda,lambda4,lambda positive. The MOND regime is
0<u<<q^2<<m^2. Here q denotes the phase gradient, not section A's source
coupling. For a spherical source, neglecting derivatives of the background
coefficients, source flux gives

    4pi r^2 2Lambda q sqrt(q^2-u)=lambda M_b,
    a_+=lambda q,
    a0=lambda^3/(8piG Lambda)=alpha^3 Lambda^2/Mp,
    lambda=alpha Lambda/Mp.

This uses the tensor-force calibration of G; dark-matter tensor gravity
also contributes to the total force. Section A's single-mediator R must
not be imported into this model. Its actual invariant would be
xi=8pi alpha^6 Lambda^4/epsilon_DE. No equation in the displayed action
sets epsilon_DE=32pi alpha^6 Lambda^4.

The source Appendix-B parent replaces the fractional term by

    F(B,r_+)=B/2+C(r_+)B^3,
    B=(partial r_+)^2+r_+^2 Z,
    C(r)=Lambda^4/[6(Lambda_c^2+r^2)^6].

At Lambda_c=0 and in the amplitude-gradient approximation its stationary
spacelike branch has R^2=r_+^2=Lambda s. For positive finite a=Lambda_c^2,
the stationary y=r_+^2 obeys

    Lambda^4 s^4 y^2(y-a)=(y+a)^7,
    y=Lambda s-2a+O(a^2/(Lambda s)).

The implicit-function derivative at a=0 is nonzero. Small positive a
therefore regularizes the amplitude denominator on a nearby local branch.
No claim of exact equality to the fractional theory at finite a follows.

For the unsourced parent let T_v=dot r_+^2+r_+^2(dot theta_+^2+dot theta_-^2)
and W=|grad r_+|^2+r_+^2(|grad theta_+|^2+|grad theta_-|^2+m^2).
Both are nonnegative. Its velocity-space energy is

    H_+=(T_v+W)/2+C(r)(T_v-W)^2(5T_v+W)>=0.

The Legendre map is not globally convex. This identity is not a proof of a
globally single-valued canonical quantum Hamiltonian or a UV completion.

The full local quadratic action at Lambda_c=0 includes both radial modes.
Put R^2=Lambda s, S^2=u/lambda4, A_-=S^2/2, perturbations
a_+=delta theta_+, b=delta theta_-, sigma=delta r_+, eta=delta r_-,
and Q=grad theta_+ dot grad a_+. The quadratic Lagrangian is

 L2=(partial sigma)^2+R^2[(partial a_+)^2+(partial b)^2]
    -2R^2(mu dot b-Q)^2/s^2-4R sigma(mu dot b-Q)-4s^2 sigma^2
    +1/2(partial eta)^2+A_-(partial b)^2+2S mu eta dot b-u eta^2.

Its time Hessian is positive if

    K_micro=A_-+R^2-2R^2 mu^2/s^2>0.

The static quadratic energy completes into

 V2=|grad sigma|^2+R^2|grad a_+|^2+(A_-+R^2)|grad b|^2
    +R^2Q^2/s^2+4s^2[sigma-RQ/(2s^2)]^2
    +1/2|grad eta|^2+u eta^2.

Writing B1=4R^2mu Q/s^2-4Rmu sigma+2Smu eta, its Hamiltonian is

 H2=p_sigma^2/4+p_a^2/(4R^2)+(p_b-B1)^2/(4K_micro)+p_eta^2/2+V2.

This proves local sourced-branch quadratic positivity in the stated open
parameter range. It omits background gradients and is not a global halo
perturbation theorem. A small positive Lambda_c preserves strict local
signs by continuity. The charge susceptibility with radial modes relaxed,
chi_-=(partial n_-/partial mu)_q, is

 n_-=mu[u/lambda4+2Lambda s],
 chi_-=(u+2mu^2)/lambda4+2Lambda s-2Lambda mu^2/s
       =2K_micro+2mu^2/lambda4+2Lambda mu^2/s>0.

There is a further causal qualification. Adiabatically relax the radial
modes below their gaps and write Q_parallel=grad theta_+ dot k_hat,
B0=Lambda s, C0=B0+Lambda Q_parallel^2/s, D0=A_-+B0,
K_eff=A_-+B0-Lambda mu^2/s+mu^2/lambda4 and
zeta=2Lambda mu Q_parallel/s. The two phase speeds z=omega^2/k^2 obey

    P(z)=(B0 z-C0)(K_eff z-D0)-zeta^2 z/4,
    P(1)=-Lambda mu^2 Q_parallel^2/(s lambda4)<0

for nonzero Q_parallel. With positive leading coefficient and P(0)>0,
one root exceeds the metric light speed squared. This is a low-energy
characteristic statement, not a calculated front velocity of a UV theory.

The finite-charge state also has
epsilon+P_perp=mu n_->0, independently of adding V0. It is not a Lorentz
vacuum. The regular amplitude parent at finite positive Lambda_c has
classical empty-vacuum energy V0 at r_+=r_-=0. The fractional EFT instead
gives V0+2Lambda m^3/3 at constant phases; its Lambda_c=0 amplitude origin
is singular. Neither prescription fixes V0. At q=0 and
mu>m the matched timelike parent stationary point instead has L_rr=8Z>0,
so its radial grand-potential curvature is negative. The local sourced
branch does not establish a stable homogeneous cosmological continuation.

Changing lambda by a small physical factor t changes a0 by t^3 and xi by
t^6, while keeping medium parameters and vacuum baseline fixed. Strict
local health inequalities persist under sufficiently small source changes.
No amplitude-selection identity follows from local stability or charge
conservation. These failures concern this specified parent, not all
superfluids or all interacting microscopic mechanisms.

## E. An exact constrained MOND response and its completion test

This is an explicit construction, not an attribution to a microscopic
source. In n>=2 spatial dimensions and a specified preferred time, let

 L=Z_t dot phi^2/2-f(y)|grad phi|^2/2+gamma y^3/6-epsilon0-q rho_b phi,
 f(y)=f_inf y/(y+b),  y>=0,

with Z_t,f_inf,b,gamma,q>0 and no derivatives of y. At h=|grad phi|>0,
the nondynamical constraint U_y=0 for U=f(y)h^2/2-gamma y^3/6 gives

 y(y+b)=sqrt(f_inf b/gamma)h,
 y=[sqrt(b^2+4sqrt(f_inf b/gamma)h)-b]/2.

It is a maximum of U in y, not an ordinary stable propagating amplitude.
The positive reduced energy and its coefficients are

 E(h)=gamma y^3(3y+2b)/(6b),
 C3=f_inf^(3/2)/(3sqrt(gamma)b^(3/2)), C2=f_inf/2,
 E'/h=f_inf y/(y+b), E''=f_inf 2y/(2y+b).

For h>0 both eigenvalues are positive and below f_inf. A time coefficient
Z_t=f_inf/c^2 therefore gives subluminal local scalar speeds. The
source-free reduced Hamiltonian pi_phi^2/(2Z_t)+E+epsilon0 is nonnegative
above a nonnegative epsilon0.

The exact canonical constraints are p_y=0 and C=U_y=0. On the solution,

 A_c=-C_y=gamma y(2y+b)/(y+b)>0,
 {chi_a(x),chi_b(x')}=[[0,A_c],[-A_c,0]] delta(x-x').

They are second class and remove y's canonical pair, leaving the physical
phi bracket canonical. At h=y=0, A_c=0 and the rank changes: no regular
perturbative quantum vacuum has been established at that point.

Spherical flux D=qM/[Omega r^(n-1)] with D=E'(h) gives

 D=sqrt(gamma f_inf/b)y^2,
 h=D/f_inf+(gamma b^3/f_inf^3)^(1/4)sqrt(D),
 G_n=q^2/(Omega f_inf), a0=q sqrt(gamma b^3/f_inf),
 g=g_N+sqrt(a0 g_N),
 R=8epsilon0/(9gamma b^3).

Thus this reduced scalar actually supplies an attractive MOND term and a
Newtonian UV. Its independent epsilon0 does not select R.

An ordinary positive kinetic regulator eta(dot y^2-c_y^2|grad y|^2)/2,
eta>0, does not give a stable massive parent. At zero spatial momentum,
spatial phi-mixing vanishes and L_yy=A_c>0, so

    mass_y^2=-A_c/eta<0.

The tachyon grows faster as eta->0+. The constraint-only escape is singular.
An off-shell gauge/SUSY auxiliary could in principle remain nondynamical,
but no such completion of this precise positive branch is supplied. The
real y>=0 Euclidean integral diverges for the displayed unreduced sign;
a suitable unitary contour and protection of the rank-changing constraint
remain unproved. The classical reduced theory is not thereby invalidated,
but it is not a demonstrated healthy microscopic quantum model.

Test positive vacuum energy generated by the same auxiliary instead of
epsilon0: set epsilon0=0 and add -J y to L, J>0. Now

 U_J=f(y)h^2/2-gamma y^3/6+J y,
 y0=sqrt(2J/gamma), epsilon_FI=gamma y0^3/3>0,
 E_J(h)=epsilon_FI+f(y0)h^2/2+f'(y0)^2 h^4/(8gamma y0)+O(h^6).

The actual IR energy is quadratic, not cubic. G_IR/G_UV=1+b/y0 is finite;
there is no operational deep-MOND amplitude ratio on this branch. A
deliberately nominal diagnostic using the J=0 cubic would instead be

 R_nom=(8/27)(y0/b)^3.

Its target matching would impose y0/b=(48pi)^(1/3)>5, eliminating the
intermediate cubic window y0<<y<<b and giving G_IR/G_UV<6/5. This is
not a prediction of R: the true IR C3 assumption already failed. At its
constant-field vacuum the auxiliary contribution has vacuum stress in
the fixed-clock scalar description; full gravitating stress still needs
a clock/gravity completion. It retains the positive-kinetic-regulator
tachyon, with A_c=gamma y0 at h=0.

Locally analytic auxiliary actions with a nonzero auxiliary Hessian give
analytic functions of h^2 by the implicit-function theorem. This particular
cubic depends precisely on the failed regularity condition at h=0. The
claim does not exclude exact microscopic constraints with additional
fields or a different quantum definition.
