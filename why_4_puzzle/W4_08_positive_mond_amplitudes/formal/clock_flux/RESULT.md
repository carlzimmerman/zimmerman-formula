# Clock projection and flux: actual MOND branches, failed normalization

2026-10-20. Base b5e54cc3c; criteria-only commit 609570aa2.
**The original why-4 goal is not achieved.** A new fixed-clock branch
has positive rigid vacuum energy, a leading MOND cubic and an actual
Newtonian crossover. Its ratio is calculable but different from the
target, and a simple dynamical clock has a physical tilt instability.
A top-form branch gives exact MOND, but its own positive vacuum flux
cuts off the infrared enhancement. These are restricted results.

## 1. A regular clock-projected chiral coefficient

Use the chiral component operator and signature -+++ from
../protected_auxiliaries/SOURCES.md. Write A=(phi+i chi)/sqrt(2),
X=partial A.dot.partial A*, Y=(partial A)^2(partial A*)^2. Let

    L=-gX+g|F|^2+2w Re(F)+Lambda(Y-2X|F|^2+|F|^4),
    s0=f0^2=g/(6tau), w=-2g f0/3, g,tau,f0>0,
    J=(g^{mu nu}+u^mu u^nu) partial_mu A partial_nu A*, u^2=-1,
    D=s0-X+5J, Lambda=-tau s0/D.

On the timelike clock patch, D=s0+|u.dot.partial A|^2+4J>0.
Replacing 5 by eta gives L2=-5gX/6+eta gJ/6 at the fold.
Thus eta=5 cancels static quadratic stiffness while retaining time
kinetic. This cancellation and the auxiliary discriminant are imposed
conditions; no supersymmetry Ward identity here selects them.

A local superspace portal can be written with a second chiral T:
C=(T+Tbar)/sqrt(2), Xsuper=partial Phi.dot.partial Phibar,
Jsuper=Xsuper-(partial C.dot.partial Phi)
                    (partial C.dot.partial Phibar)/(partial C)^2.
Insert Lambda(Xsuper,Jsuper) into the standard saturated
(DPhi)^2(Dbar Phibar)^2 D-term with its 1/16 normalization. Its bosonic
lowest coefficient gives the displayed action on (partial C)^2<0.
This is a construction of the portal, not a healthy complete clock or
fermion/gravity theory. A real unit-vector clock can instead be embedded
near the real vacuum of a constrained chiral-vector super-aether; its
bosonic real tilt is the independently tested sector below.

## 2. Exact static branch and operational response coefficients

For a static real scalar, J=X=h^2/2 and Y=X^2. Put x=X/s0,r=F/f0.
The complex auxiliary equation with w nonzero forces F real. It becomes

    Q=r^3-(3+13x)r+2+8x=0,
    x=(r-1)^2(r+2)/(13r-8), 8/13<r<1.

The latter expression decreases strictly in r, giving a unique selected
branch for every x>0. Other real auxiliary roots are not thereby removed.
The exact displayed static energy is E=tau s0^2 e with

    e=6x-6r^2+8r+(x-r^2)^2/(1+4x).

As x tends to zero, r=1-sqrt(5x/3)+O(x), and
e=3+(40/3)sqrt(5/3)x^(3/2)+O(x^2). At infinity r tends to 8/13
and e_x tends to 25/4. Therefore the same branch has

    epsilon_rigid=g^2/(12tau)>0,
    E=epsilon_rigid+C3 |h|^3+O(h^4), C3=10sqrt(5g tau)/9,
    E~C2 h^2, C2=25g/48.

Unlike the earlier Taylor ratio, C2 here is the actual large-gradient
coefficient of the displayed action. This extrapolation still does not
prove a microscopic ultraviolet completion of a higher-derivative EFT.

At fixed r,
e_xx=2(1+4r^2)^2/(1+4x)^3>0,
e_rr=4(3r^2-3-13x)/(1+4x)<0.
Eliminating r gives e_on,xx=e_xx-e_xr^2/e_rr>0. Since e_on,x(0)=0,
the energy has positive radial and tangential gradient Hessians at h>0.
Its flux E_h increases from zero to infinity, so a prescribed spherical
displacement has a unique static inversion on this branch. This does
not prove central regularity, full coupled source evolution or a
minimum over all algebraic auxiliary branches.

For a single scalar source -q_source rho phi, the ultraviolet and
infrared Gauss laws are 2C2 h=D_source and 3C3 h^2=D_source, with
D_source=q_source M/(Omega r^(n-1)) in n>=2 space dimensions.
The inherited source dictionary then gives the conditional rigid ratio

    R_rigid=epsilon_rigid C3^2/C2^3=4096/1125,
    xi_conditional=32pi/(9 R_rigid)=125pi/128  (n=3).

This is neither the target nor a healthy gravitational prediction:
epsilon_rigid has not been promoted to the complete gravitating vacuum.
An allowed deformation D -> D+delta J^2/(s0+J), delta>=0, preserves
the vacuum, static cancellation and leading C3, but changes

    C2(delta)=g/2+g/[12(4+delta)],
    R_rigid(delta)=8000(4+delta)^3/[9(25+6delta)^3].

The selected deformed branch exists for all delta>=0. Static convexity
survives on a nonzero interval near delta=0 by uniform endpoint
asymptotics and compact-range continuity; it is not claimed for all
delta. Even this conditional ratio is not protected against operators.

## 3. Retained modes and an actual dynamical-clock instability

Set t=(x-r^2)/(1+4x), z=x/(1+4x),
B=1+t/3-2t^2/3=E_X/g. Then -1<t<1/4 and

    Z_phi/g=1+t/3+t^2/6>=5/6,
    Z_chi/g=Z_phi/g-2z/3>2/3,
    G_phi,perp=E_X, G_phi,parallel=E_X+2X E_XX,
    G_chi,parallel=gB, G_chi,perp=g(B-2z/3)>0.

All these fixed-clock static-background coefficients are positive at
finite h>0. In particular B=(t+1)(3-2t)/3. At zero gradient the
spatial Hessians vanish. On aligned purely timelike J=0,X<0, F=f0
continues exactly, both time coefficients are 5g/6, and the real
scalar's spatial coefficient is zero. The old missing timelike root
is repaired, but this is not a regular positive spatial vacuum symbol.

There is also a decoupled chi characteristic outside the metric cone.
At the exact lower-branch point x=4/9,r=2/3, F^2=X, so

    K_chi=67g/75, G_chi,parallel=g, v_chi^2=75/67>1.

No invariant has a linear chi variation, so eliminating F, the real
scalar or the clock cannot alter this quadratic mode. This is a
principal speed of the displayed preferred-frame action, not a proof
of the front velocity of a different ultraviolet completion.

More decisively, make the clock a physical derivative-only unit vector
in fixed metric. Its real homogeneous tilt has L_clock,2=M v_dot^2/2,
M>0, with no homogeneous restoring potential. Around phi=H z, let v
be the tilt along z and varphi a homogeneous real scalar fluctuation.
For the reduced real action define

    a=E_X=-(L_X+L_J)>0, j=L_J>=0, K=-L_X=a+j.

Normalized u=(sqrt(1+v^2),0,0,-v) gives, through quadratic order,
J=X_static+H^2v^2/2-Hv varphi_dot. Consequently

    L2=K varphi_dot^2/2-jHv varphi_dot+jH^2v^2/2+M v_dot^2/2.

X and J have no linear variation in this homogeneous sector. F has no
linear source and adds no omitted quadratic term; chi also decouples.
The scalar momentum p=K varphi_dot-jHv is conserved. At its admissible
value p=0, completing the square yields the clock Routhian

    L_v=M v_dot^2/2+H^2 j a v^2/(2K),
    omega^2=-H^2 j a/(KM)<0  when H nonzero and j>0.

For this model j=5tau s0 (X-F^2)^2/D^2 tends to 5g/6 near the fold,
so the instability occurs at arbitrarily small nonzero static gradients.
At x=4/9, j=0; the chi test there is a separate obstruction.
A rational point x=11/112,r=3/4 gives t=-1/3 and, for g=54,
a=44,j=5,K=49. Thus omega^2/H^2=-220/(49M).

This mode is also present in the real flat-background derivative sector
of the specified super-aether. Full gravitational constraints, varying
halo backgrounds or additional clock operators require new analysis;
the fixed-metric homogeneous result is not an all-aether no-go.
For the narrower L(X,J) class with a physical finite-M unit tilt, zero
static vacuum stiffness and positive finite time coefficient imply
j(0)=K(0)>0. If these coefficients are continuous, positive MOND a(h)
then triggers this same tilt test sufficiently near zero. Merely adding
another regular function of X,J cannot repair that restricted limit.

A P(X_T) clock, X_T=-(partial T)^2/2>0, has
K_T=P_X+2X_T P_XX, C_T=P_X and
rho_T+p_T=2X_T P_X. Positive C_T gives nonvacuum clock enthalpy.
A constant offset does not change it. The P_X=0 limit loses quadratic
spatial stiffness and needs a separate higher-derivative analysis.
This statement is not a universal microscopic NEC claim.

A separate quadratic discriminator applies AFTER all constraints to
an isotropic physical action L2=(q_dot^T K q_dot-partial_i q^T G partial_i q)/2,
with real symmetric K>0 and spatial block G=[[0,B],[B^T,C]], C>0.
Its Schur complement is -B C^(-1) B^T, so G is positive semidefinite
iff B=0. Nonzero spatial mixing gives a negative physical generalized
eigenvalue and omega^2=-c_bad^2 k^2. This does not exclude pure time
mixing: K=[[Z,mu],[mu,Kc]]>0, G=diag(0,C) has squared speeds zero
and CZ/(Z Kc-mu^2)>0. The zero-speed mode is still degenerate.
For a massive clock, low-frequency elimination instead induces a
negative O(k^4/m^2) stiffness correction; the two-derivative high-frequency
Gram test is a different regime. Mixing vanishing with the background
can also evade a constant-mixing test. Mixed time-space derivatives,
higher spatial derivatives and unreduced constraints require the full
characteristic pencil. This algebra supplies a discriminator, not an
all-clock or all-gravity prohibition.

## 4. A top form: exact MOND and the fixed-flux obstruction

In D spacetime dimensions let dC_(D-1)=f vol_D. With a specified clock,
take s=h^2, P(f)=gamma f^6/6 and k(f)=F_inf f^2/(f^2+b), all constants
positive. The bulk action includes Z(u.dot.partial phi)^2/2+P-k s/2
-epsilon0-q_source rho phi. The canonical flux and fixed-flux energy are

    q=P'(f)-k'(f)s/2, dq=0,
    E_q=epsilon0+qf+k(f)s/2-P(f).

The boundary term is -int_boundary q C at fixed q. Equivalently use the
first-order bulk integrand P-k s/2-qf and the form term -int dq wedge C.
Varying q gives dC=f vol_D. The -qf term is essential: with gamma=6,
f=1,s=0,q=6, correct same-form energy is 5; omitting it gives -1.
The primary pure-top-form boundary/stress dictionary is in SOURCES.md.

At q=0 the nonzero branch Y=f^2 satisfies

    Y(Y+b)=sqrt(F_inf b/gamma) h,
    E_0-epsilon0=gamma Y^3(3Y+2b)/(6b),
    C2=F_inf/2, C3=F_inf^(3/2)/(3sqrt(gamma b^3)).

It gives exact g=g_N+sqrt(a0 g_N) in three space dimensions, with
G=q_source^2/(4pi F_inf), a0=q_source sqrt(gamma b^3/F_inf).
Its scalar stiffnesses are F_inf Y/(Y+b) and 2F_inf Y/(2Y+b),
both positive and below F_inf at Y>0, so Z>=F_inf controls those scalar
cones with a fixed clock. This is a conditional branch construction.
Its same-form vacuum energy is zero; epsilon0 is still independent.

The original analytic action also has f=0 at q=0 for every s, with
E=epsilon0. Its velocity Lagrangian is nonconvex; no single-valued
canonical H(q,s) represents all sheets. The global Legendre-Fenchel
supremum is finite and selects the nonzero extrema at q=0,s>0, but its
reverse conjugate is the convex envelope of the original action. It
changes the theory and does not justify deleting the f=0 solution.
No propagating free top-form scalar is added; this observation does
not establish the scalar portal's branch/energy/quantum health.

For nonzero q choose the outer branch aligned with q. Its zero-gradient
Y0 obeys |q|=gamma Y0^(5/2), and its SAME-form vacuum energy is
epsilon_form=5gamma Y0^3/6>0. The exact constraint and force obey

    s=gamma (Y+b)^2[Y^2-Y0^(5/2)Y^(-1/2)]/(F_inf b), Y>=Y0,
    g/g_N=1+b/Y<=1+b/Y0.

The infrared stiffness F_inf Y0/(Y0+b) is nonzero. The true infrared
response is quadratic; an intermediate cubic window requires Y0<<Y<<b.
Using the zero-flux C3 anyway would give the obsolete NOMINAL ratio

    R_nominal=(20/27)(Y0/b)^3.

Matching that expression to 128pi/9 demands (Y0/b)^3=96pi/5>1,
removing the cubic window and bounding g/g_N by
1+(5/(96pi))^(1/3)<2. This is a counterfactual diagnostic, not a target
input or an operational amplitude prediction.

Near the original inner branch, for fixed h>0 and small nonzero q,

    f=-qb/(F_inf h^2)+O(q^3),
    E_q-epsilon0=-bq^2/(2F_inf h^2)+O(q^4),
    E_hh=-3bq^2/(F_inf h^4)+O(q^4)<0.

The analytic inverse exists near f=0 at fixed h>0, making the differentiated
expansion valid locally. With the specified positive time kinetic and
fixed clock this is an actual scalar gradient instability. At fixed
flux a branch-labelled Hamiltonian need not be unbounded below; the
problem is not a universally inferred top-form ghost.

Membrane charge changes canonical q, not nonlinear f. If the integrated
spatial C coordinate has period 2pi/e, its canonical momentum is
q=q_ref+Ne. This conditional compactness calculation leaves e and its
relation to gamma b^3 free. Gauge invariance permits lower powers of f
and does not protect the pure f^6 critical action. No membrane tension
or charge relation removes the finite-flux force cutoff just derived.

## 5. Exact formal scope and remaining constructive opening

ClockTilt.lean verifies the complete square, negative frequency sign,
static-stiffness factorization/positivity, conditional ratio arithmetic
and generic source bridge. Physical component dictionaries, branch
existence/asymptotics, retained-mode reduction, gravity, quantum health
and actual pi are explicit analytic inputs. It does not prove a healthy
microscopic normalization. The original goal remains active.

The next viable change must address the retained clock/metric constraint
system or use a different invariant structure, and derive a protected
same-state vacuum relation. A fixed clock, imposed discriminant,
convexified branch prescription, finite-flux Taylor match or added vacuum
constant does not meet those requirements. Curvature/aether operators
with full gravitational constraint reduction remain untested here;
their effects cannot be inferred from the fixed-metric tilt theorem.
