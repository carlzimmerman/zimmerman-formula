# W4-08 continuation: dynamical gaps and a temporal-vector parent

2026-10-20. Raw analytic results; exact mathematical/physical scope stated
below. Base is the W4-08 result 4131def0e and frozen continuation 63afb2ca2.
The original goal, deriving xi=1/4 in a healthy microscopic theory and
verifying the chain in Lean, remains open. The new vector parent improves
a specific classical completion failure; it does not select an amplitude.

## A. Quantitative stress and a dynamical gap

Let d>0, r=sqrt(1+d^2), f=r^3-1-d^3. The fixed-cutoff paired-band stress is

    rho=A L^3 f,  N=rho+p_parallel=(3/2)A L^3(r-1).

The exact factorization f(r+d)=(r-1)(2r+d+1), together with r>1 and r>d,
gives rho/2<N<rho, or -rho/2<p_parallel<0. Thus no positive finite
collection of these bands, arbitrary vacuum offsets, and sectors with
nonnegative extra directional null stress can form a Lorentz vacuum.
It would require N_extra=-sum N_i<-sum rho_i/2. Health is NOT asserted to
imply this directional NEC assumption for all microscopic quantum sectors.

The bare energy cannot select a positive gap by minimization:

    d epsilon_band/dd=3A L^3 d(r-d)>0.

Introduce a common scale chi>0 in spacetime dimension D>=3 by
A=alpha chi^(D-3), L=ell chi, Delta=d ell chi. A dynamical stabilizer
changes the TOTAL potential, including its vacuum contribution, to

    V=chi^D F(t,d),  t=log(chi/mu).

For a C^2 potential at an interior equilibrium,

    F_d=0,  D F+F_t=0,  epsilon=-chi^D F_t/D,
    H_chichi=chi^(D-2)(D F_t+F_tt),
    H_chid=chi^(D-1)F_td, H_dd=chi^D F_dd.

With positive kinetic metric and F_dd>0, a positive-definite potential
Hessian (strict quadratic stability) with epsilon>0 requires

    F_t<0,  F_tt>D|F_t|+F_td^2/F_dd.

For a merely local minimum with F_dd>0, positive semidefiniteness gives
the weak inequality >= instead; a strict minimum can have flat quadratic
directions. These are potential-Hessian conditions; they do not give pole
masses without kinetic normalization. Exact scale invariance gives epsilon=0
and a flat scale direction. A single logarithm F=P(d)+B(d)t has

    chi^2 H_chichi=-D^2 epsilon,
    chi^2 H_relaxed=-D^2 epsilon-chi^D [B'(d)]^2/F_dd.

Consequently positive energy gives a negative radial curvature and
excludes even a degenerate local minimum for this single-log completion.
The precise broader condition excluded by strict quadratic stability is
F_tt<=D|F_t|; there is no unrestricted claim about all perturbative flows.
Single-field Coleman-Weinberg overlap already exists in
sol61_push/puzzle_32pi_dilaton_2026_10_14/RESULT.txt. The paired-band
application adds the dynamical gap and its mixing, not a new universal
Coleman-Weinberg theorem.

The total frozen-background ratio would be
R_total=8F_*/(27alpha ell^3 b_gap^3), b_gap=1+d-sqrt(1+d^2).
Using the old band-only numerator after adding U or running would omit
the stabilizer's vacuum energy. Modulus relaxation in an actual source
still needs a separate operational force calculation.

## B. Temporal-vector constraint instead of a scalar regulator

In a fixed preferred time, take Y=A0>0 and

 L=Z dot phi^2/2-f(Y)|grad phi|^2/2+gamma Y^3/6
   +(|dot A-grad Y|^2-|curl A|^2)/2
   -mV^2(Y)|A|^2/2-epsilon0-q rho phi,
 f(Y)=f_inf Y/(Y+b), mV^2(Y)=kV gamma Y,
 Z=f_inf, f_inf,b,gamma,q>0, 0<kV<=1.

This is a preferred-frame vector action with a Proca-type second-class
constraint, NOT an asserted gauge-invariant UV theory. The momenta are
p_phi=Z dot phi, pi=dot A-grad Y and pY=0. After integration by parts,

 H=p_phi^2/(2Z)+(pi^2+B^2)/2+mV^2 A^2/2
   +f(Y)h^2/2-gamma Y^3/6-Y div pi+epsilon0+q rho phi,
 C=f' h^2/2-gamma Y^2/2+kV gamma A^2/2-div pi=0,
 C_Y=-a,  a=gamma Y+f_inf b h^2/(Y+b)^3>0.

The pair (pY,C) is second class on Y>0. Its matrix may have nonzero
{C,C}, but its inverse's secondary-secondary block is zero, so physical
(phi,p_phi),(A,pi) brackets remain canonical. A unique positive Y root
exists iff f_inf h^2/(2b)+kV gamma A^2/2-div pi>0; arbitrary canonical
phase space is not covered. On the constraint,

 H_on=p_phi^2/(2Z)+(pi^2+B^2)/2
      +f_inf Y^2 h^2/[2(Y+b)^2]+gamma Y^3/3+epsilon0+q rho phi.

The displayed source-free terms are nonnegative for epsilon0>=0.
Integrated positivity requires the discarded boundary term be zero or
accounted for. It does not certify quantum unitarity or cosmological stress.

Around A=0 with positive y and phase-gradient H, let u=delta phi.
The linear constraint eliminates delta Y as

    delta Y=[f' H dot grad u-div delta pi]/a.

The reduced quadratic Hamiltonian is

 H2=p^2/(2Z)+(delta pi^2+delta B^2)/2+M^2 delta A^2/2
    +f|grad u|^2/2+[f'H dot grad u-div delta pi]^2/(2a)>=0

with strict positivity after boundary conditions exclude the constant-phi
zero mode.
This replaces the scalar-regulator tachyon by a genuine temporal-vector
constraint. Its coefficients can vary on the regular static background;
the completed quadratic form remains positive there. A general nonzero-A
background requires a new characteristic calculation.

For a frozen A=0 background let g=f'H dot k_hat. Squared scalar/longitudinal
frequencies w obey

 (Zw-K)(w-M^2 c)-M^2 eta^2=0,
 c=1+k^2/a, eta=gk^2/a, K=k^2(f+g^2/a).

Transverse modes have w=k^2+M^2. Principal squared speeds z obey

 z^2-(alpha+beta+delta)z+alpha beta=0,
 alpha=M^2/a, beta=f/Z, delta=g^2/(aZ).

For M^2=kV gamma y, Z=f_inf, 0<alpha<=1, 0<beta<1. At any angle theta,

 (1-beta)(a-M^2)-f'^2 H^2 cos^2(theta)/f_inf
 =b(gamma y-M^2)/(y+b)
    +f_inf b^2 H^2 sin^2(theta)/(y+b)^4 >=0.

The two roots are positive and <=1. At the endpoint kV=1,
some modes can be luminal. This is a classical principal-symbol result
for this specified action and background class, not a quantum front-
velocity calculation. A fixed positive vector mass instead fails the
small-y cone bound.

## C. Spatial response and a regular spherical source

At A=0 the static equations are

    div(f(Y)grad phi)=q rho,
    -Delta Y+[gamma Y^2-f'(Y)|grad phi|^2]/2=0.

The homogeneous quadratic static response is nonlocal:

 E2_static=f|grad u|^2/2+S(a-Delta)^(-1)S/2,
 S=f'H dot grad u.

Its Fourier stiffness is f k^2+g^2 k^2/(a+k^2). The old auxiliary
constitutive response is the k^2<<a limit, not the full kernel.

For a nonzero smooth nonnegative compact radial source in three space
dimensions, put D(r)=qM(r)/(4pi r^2), h=D/f(y), and
alpha_r=bD(r)^2/(2f_inf). The Y equation is the Euler equation of

 J_R[y]=4pi int_0^R r^2[(y')^2/2+gamma y^3/6+D(r)^2/(2f(y))]dr,
 1/f(y)=(1+b/y)/f_inf.

This functional is strictly convex. For y(R)=Y_R>0, truncation gives
y<=M where M>=max[Y_R,(2||alpha_r||_infty/gamma)^(1/4)]. The positive
solution of -Delta v+(gamma M/2)v=0 with the same boundary data is a
subsolution. Thus y>=v>0, including y(0)>=Y_R kR/sinh(kR),
k^2=gamma M/2. The direct variational method followed by comparison
and elliptic regularity gives a unique positive regular finite-ball branch.

For the global decaying branch, outside the source D=d0/r^2 and
C^4=b d0^2/(gamma f_inf). Choose outer data y_R(R)=C/R. Uniform local
positivity follows from w=delta v: let (-Delta+c)v=s>=0, with s compactly
supported in an annulus where alpha_r>0. For small delta, the negative
term -alpha_r/(delta^2 v^2) dominates on that support; off it,
-c delta v+gamma delta^2v^2/2<=0. Yukawa decay gives w(R)<=C/R.
Combined with a uniform constant upper bound, local elliptic compactness
gives a positive regular global limit.

Exterior comparison supplies a_*/r<=y<=A_*/r, with 0<a_*<=C<=A_*.
For W=ry the exact exterior ODE is

    W''=gamma[W^2-C^4/W^2]/(2r).

A bounded positive W cannot cross C with nonzero derivative: subsequent
curvature would push it outside its bounds. Above C it must decrease
convexly; below C it must increase concavely. A different limiting value
would give signed nonintegrable 1/r curvature. Hence W->C. The maximum
principle gives uniqueness among positive regular radial y solutions
tending to zero; phi retains an additive constant.
This analytic existence/asymptotic argument was independently reconstructed;
it is not currently formalized in Lean.

Consequently

    y~C/r,
    g=g_N+sqrt(a0 g_N)[1+o(1)],
    G=q^2/(4pi f_inf), a0=q sqrt(gamma b^3/f_inf).

The bare Newtonian coefficient is calibrated by the f->f_inf limit;
the existence of an observational Newtonian window also depends on the
source and scale regime. Exact y=C/r solves the exterior equations but
need not match a regular interior. The general-dimensional local profile
y proportional to r^(-(n-1)/2) has Delta y/y=(n-1)(3-n)/(4r^2); the exact
harmonic cancellation is specific to n=3.

After subtracting the constant epsilon0 baseline, the isolated-space
energy has the usual logarithmic MOND divergence, and phi grows
logarithmically. This is not a finite-energy isolated
vacuum or a cosmological matching result.

## D. What is still missing microscopically

At y=h=0 the constraint curvature and the longitudinal time coefficient
a/(a+k^2) vanish. The quadratic vector action becomes Maxwell while phi
loses spatial stiffness. Finite limiting speeds do not prove a regular
quantum vacuum or protect the degenerate constraint from radiative terms.

A concrete microscopic pressure analogy is the direct free Dirac integral

 P(mu)=g int d^2k/(2pi)^2 (mu-vk)theta(mu-vk)=g mu^3/(12pi v^2).

For layer density nu and electrochemical mu=eY this gives
gamma=nu g e^3/(2pi v^2), and fermion energy mu P_mu-P=2P=gamma Y^3/3.
This reproduces a static term, not the full dynamical parent. Finite-density
polarization is frequency/momentum dependent and nonlocal. A gauge-invariant
realization of f(Y), the electrochemical potential, layer geometry and
gravitating preferred-clock stress has not been supplied. Fermion
enthalpy is nonzero; this is not a microscopic dark-energy vacuum.

The vacuum baseline remains epsilon0 and

    R=8epsilon0/(9gamma b^3),  xi=4pi gamma b^3/epsilon0.

No constraint, cone inequality, regular source solution or pressure
coefficient fixes epsilon0/(gamma b^3). Thus no xi=1/4 selection follows.
An independent mechanism tying the quantum vacuum and response amplitudes
is still required, together with a protected regular zero-field theory.
