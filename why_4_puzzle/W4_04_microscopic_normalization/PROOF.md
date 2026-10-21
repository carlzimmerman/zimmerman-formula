# W4-04: normalization calculations

Natural units c=1 except where restored. Epsilon is physical energy density.
The claims below concern the explicitly specified models and limits.

## A. Operational amplitude invariant

Let n>=2 be spatial dimension, Omega=area(S^(n-1)), q,C2,C3,epsilon>0.
A scalar potential phi couples as `-q rho_b phi`; its physical acceleration
is `g=q|grad phi|`. Its rotationally invariant static energy has derivative
asymptotes `E'(h)~2C2 h` at high h and `E'(h)~3C3 h^2` at low h, h=|grad phi|.
These derivative asymptotes, not just undifferentiated energy asymptotes,
are assumptions. Static variation and flux integration outside a compact
spherical source of mass M give

    Omega r^(n-1) E'(h)=q M.

Consequently the force-law definitions are

    G_n=q^2/(2 Omega C2),
    a0=2q C2/(3C3),
    xi=a0^2/(G_n epsilon)=8 Omega C2^3/(9 epsilon C3^2).

In n=3 this gives xi=32pi C2^3/(9 epsilon C3^2). The target xi=1/4 is
equivalent, under these assumptions, to

    epsilon C3^2/C2^3=128pi/9.

This is a calculation target, not a premise imposed on a microscopic model.
Under field redefinition phi_new=s phi with s>0, the coefficient dictionary is
q_new=q/s, C2_new=C2/s^2, C3_new=C3/s^3; both forces and xi are unchanged.
Multiplying epsilon,C2,C3 by a common factor Z>0 also leaves xi unchanged:
Z^(3-1-2)=1. Thus a common loop factor, species multiplicity or explicit
hbar factor can cancel. This does not show that the three operators have
a common factor in a proposed theory. For a tensor+scalar model the measured
Newton G is not automatically the G_n above; the dictionary must be redone.

## B. Locally supersymmetric vacuum and Born-Infeld response

Take the bosonic sector of arXiv:1811.08424v3 Eq(4.12), with Planck factors
restored, canonical F and tension T>0:

    L_BI= -T[1+sqrt(1+F^2/(2T)-(F Ftilde)^2/(16T^2))]
          +3 Mp^2 m32^2,
    Mp^-2=8pi G,   V=2T-3Mp^2 m32^2.

Canonicalization of the source's parameters is F_c=sqrt(beta/m_BI)F,
T=beta m_BI, g_gauge^2=m_BI/beta. The parameters m_BI and m32 are distinct.
The restriction m32=0 gives T=V/2. In a purely electric sector,

    L(E)= -V+E^2/2+E^4/(8T)+O(E^6),
    c4 V=V/(8T)=1/4 on that restricted branch.

This last quarter is an electric susceptibility ratio, not xi. No
nonrenormalization beyond the displayed classical action is asserted.

For a canonical point charge Q and a probe charge/mass alpha, the exact
static solution of this local constitutive action is

    D=E/sqrt(1-E^2/T),
    D(r)=Q/[Omega r^(n-1)],
    E(r)=D/sqrt(1+D^2/T),  a_probe=alpha E.

The large-radius tail is r^(-(n-1)); the small-radius field saturates.
It is not a deep-MOND r^(-(n-1)/2) tail. This bosonic dimensional test does
not extend the special d=4 supersymmetry algebra to d=5.

Even the saturation scale a_star=|alpha|sqrt(T) has free ratio
`a_star^2/(G V)=alpha^2 T/(G V)`. More strongly, at fixed V,G and canonical
source data choose s>0 satisfying 2s^2 T>=V and set

    beta_s=s beta,  m_BI_s=s m_BI,
    m32_s^2=(2s^2T-V)/(3Mp^2).

The gauge coupling stays fixed, T_s=s^2T, V_s=V, but the response changes.
The m32=0 branch excludes this mutation by an additional restriction and
still has the wrong force law. A general arbitrary source coupling need
not have a fully audited supersymmetric matter completion for the wrong
force-law conclusion: that already follows from the constitutive sector.

For comparison, arXiv:1507.08264v6 Eq(1.3) has V=f^2-3Mp^2m32^2.
At fixed V>0, f^2=V+3Mp^2t^2, m32=t is a locally supersymmetric parameter
family. Its bosonic Einstein+V sector produces Schwarzschild-de Sitter,
not MOND. The equality radius (GM/H^2)^(1/3) is mass dependent.

## C. Common finite-temperature determinant

For N>0 identical free bosons, gamma>0, a homogeneous nonnegative spurion
X=h^2, m_eff^2=gamma X, and temperature theta>0, the high-temperature/small-mass
expansion m_eff/theta<<1 of the thermal free energy is

    F(X)=N[-pi^2 theta^4/90+gamma theta^2 X/24
           -gamma^(3/2) theta X^(3/2)/(12pi)+O(X^2 log X)].

Here theta denotes temperature, not the BI tension T. These are inputs from
the free thermal integral, not extrapolated to arbitrarily large X.
Let C2_th=N gamma theta^2/24, C3_th=-N gamma^(3/2)theta/(12pi).
The algebraic ratios are

    |F(0)| C3_th^2/C2_th^3=16/15,
    epsilon_rad C3_th^2/C2_th^3=16/5,
    epsilon_rad=3|F(0)|.

N,theta and a common gamma cancel, just as the invariant in A permits.
This is an example of a common microscopic amplitude ratio. It is not an
operational xi prediction: C3_th<0, the quadratic term dominates X->0,
the high-X thermal response is exponentially suppressed rather than C2_th X,
and the state has w=1/3 rather than vacuum stress. Bare/critical subtractions
or a dynamical medium would be additional input.

The common gamma cancellation must not be mistaken for rigidity against all
physical couplings. For a pair of bosonic groups with slopes gamma(1+t)
and gamma(1-t), |t|<1, their X=0 free energy and their total quadratic
coefficient stay fixed, while their cubic amplitude is multiplied by

    A(t)=[(1+t)^(3/2)+(1-t)^(3/2)]/2.

Strict convexity of z^(3/2) gives A(t)>1 for t!=0. Such unequal slopes are
forbidden if an exact O(N) symmetry requires equality; on that symmetric
free model the displayed thermal ratios do remain fixed. Even that special
model fails the sign, low/high-field and vacuum-stress conditions above.

At zero temperature a gapped four-dimensional determinant is locally
analytic in X around zero after the stated local renormalization; the
massless constant-background term has X^2 log X. In general d spacetime
dimensions its threshold power is X^(d/2), with logarithms in even d;
the thermal zero mode has power X^((d-1)/2), with logarithms where needed.
Thus a thermal d=4 cubic cannot be inferred from a gapped d=4 vacuum or
blindly continued to d=5. These statements are about the specified free
local effective-potential calculation, not every gapless interacting theory.

## D. A finite common zero-temperature determinant

Consider 12 real scalars, four at each squared mass M^2 times 1,2,3, and
three Dirac fermions at squared masses M^2 times 6/7,17/7,19/7. All scalar
curvature couplings are zeta=1/4. Define

    p(z)=sum_s (m_s^2)^z-4 sum_f (m_f^2)^z,
    q(z)=sum_s (1-6zeta_s)(m_s^2)^z+2 sum_f (m_f^2)^z.

The five cancellation conditions p(0)=p(1)=p(2)=q(0)=q(1)=0 hold exactly.
They ensure finiteness of the cosmological and Einstein coefficients of
this specified one-loop model, not every higher-curvature coefficient.
With the no-bare-vacuum and no-bare-Einstein prescription explicitly
assumed, its induced quantities are

    epsilon= hbar p'(2)/(64pi^2),
    1/G= hbar q'(1)/(12pi).

Both are positive for the displayed spectrum; the coefficient signs can be
certified by rational logarithm intervals. These formulas follow the
effective determinant convention of hep-th/9607104v1 section 2; its extra
constraint p'(2)=0 is not imposed here. Our spectrum is a constructed test
of a common finite origin, not a symmetry-selected particle spectrum or
a claimed microscopic model of the observed Universe.

For a constant nonnegative spurion X, shift every squared mass by gamma X,
gamma>=0. Binomial expansion shows that all five cancellations persist.
The effective potential near X=0 remains analytic because every mass is
strictly positive. No positive X^(3/2) term appears. Thus even the actual
finite common determinant does not yet generate the operational MOND
coefficient required by A. Its gamma is an independently specified local
source-spurion coupling; varying it changes response derivatives at X=0
while the vacuum and Einstein coefficients there remain fixed. This fact
alone would not disprove a common amplitude ratio if a suitable C3 existed:
the common gamma powers might cancel, as they do in C.

The nonminimal curvature coupling zeta=1/4 follows if the scalar couplings
are equal and the field counts are constrained as displayed. It is not xi
and cannot be identified with the MOND coefficient.

There is a finite coupling deformation even after regulator moments have
been removed. Change the sums of scalar curvature couplings at squared
mass ratios 1,2,3 by `t(1,-2,1)`, respectively. This preserves q(0),q(1)
and all p constraints, but

    delta(1/G)=-hbar t M^2 log(27/16)/(2pi).

The vacuum stays fixed. For sufficiently small t, positive G and the
constituents' ordinary kinetic signs persist; no full coupled stability
claim follows. The displayed positive-gamma flat spurion also has
`V_X(0)=hbar gamma p'(1)/(32pi^2)<0`. It is not a healthy standalone
positive scalar response without additional input.

There is also a consistency limit on promoting this particular flat-
background one-loop example to a self-gravitating vacuum. Its leading
Einstein estimate would give

    H^2/M^2=p'(2)/(2q'(1))  (derivatives evaluated at M=1).

The displayed spectrum has 3<H^2/M^2<4 by the same exact log intervals.
Thus it does not lie in the low-curvature regime H^2<<m_i^2 needed to
interpret the truncated induced Einstein action as its de Sitter solution.
The positive finite coefficients are a flat-background calculation, not
a constructed cosmological vacuum. This does not exclude other spectra
or a nontruncated induced action.

## E. String D3 and stabilized vacuum

For an unwarped D3 patch with endpoint coupling integral A, take

    lambda=2pi alpha',
    T3=1/[(2pi)^3 g_s alpha'^2],
    e^2=1/(T3 lambda^2)=2pi g_s,
    16pi G4=(2pi)^7 g_s^2 alpha'^4/V6.

Canonical electric threshold b=sqrt(T3) obeys e b=1/lambda=T_F1.
In the fixed-embedding pure-electric DBI truncation, the electric-component
saturation acceleration of a charged endpoint of mass m is T_F1/m.
For a stretched BPS state's mass m=T_F1 L, this component's formal scale
is 1/L, or c^2/L in SI. The total force on a dynamical BPS endpoint also
involves transverse scalars; it is not claimed to share this bound.
Even if the vacuum were C=T3, its threshold ratio would be

    xi_BI=V6/(pi^3 g_s alpha'^2 L^2).

The actual canonical electric field is D/sqrt(1+D^2/T3), D=Q/(4pi r^2);
the endpoint force is e times that field and its acceleration is e times
that field divided by its mass. Thus this is not operational xi. The
tree-level GKP Minkowski/no-scale background used here has net vacuum C=0
and a canceling D3 probe potential, not C=T3. This is a property of that
background, not a statement that all supersymmetric compactifications
have zero cosmological constant.

To test a stabilized nonzero vacuum, use the leading KKLT potential with
the actual uplift coefficient D defined as

    V(sigma)=[a A exp(-a sigma)/(2sigma^2)]
             [A exp(-a sigma)(1+a sigma/3)+W0]+D/sigma^3.

Assume a,sigma,A>0. Let x=a sigma>1 and B=A exp(-x). Then sigma^3 V=U(x)+D with
`U=x[B^2(1+x/3)+BW0]/2`. At a chosen x0>1 set

    W0=-B(2x0^2+4x0-3)/[3(x0-1)],
    D0=B^2 x0^2(x0+2)/[6(x0-1)],

where B is evaluated at x0 and W0,D0 are held constant when taking field
derivatives. Direct differentiation gives U+D0=U_x=0 and

    U_xx=B^2(2x0^3-3x0+4)/[6(x0-1)]>0.

Hence the displayed single-real-modulus leading potential has a stable Minkowski crossing at finite
volume, including x0>>1 where the nonperturbative expansion can be used.
The implicit-function theorem gives a neighboring stable stationary branch
for small deltaD, with `C=deltaD/sigma0^3+O(deltaD^2)` and
`dC/dD=1/sigma_*^3`. A finite smooth microscopic force scale therefore
has no universal ratio to C as C tends to zero from above in this potential.
This is an analytic EFT parameter family; realization of every choice by
quantized fluxes is not asserted, nor is a global string landscape no-go.
