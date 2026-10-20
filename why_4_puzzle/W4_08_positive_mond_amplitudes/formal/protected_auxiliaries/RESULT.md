# Protected auxiliaries: positive vacuum, branch health and normalization

2026-10-20. Base 02f2fae08, criteria-only commit 3a6b85cac.
**The original why-4 goal remains open.** An explicit supersymmetric
chiral prototype has positive rigid vacuum energy and a positive static
cubic correction, but fails the dynamical branch and force tests. A
Born-Infeld/FI model calculates a vacuum/nonlinearity relation but has
no MOND cubic. Neither forces the requested operational amplitude ratio.

## Chiral component model and an actual positive-vacuum fold

Use signature -+++, A=(phi+i chi)/sqrt(2), X=partial A.dot.partial A*,
Y=(partial A)^2(partial A*)^2, g>0, constant real Lambda, and W'=w:

    L_b=-gX+g|F|^2+Lambda[Y-2X|F|^2+|F|^4]+wF+wF*.

The bosonic auxiliary equation is F[g-2Lambda X+2Lambda|F|^2]+w=0.
For constant A,F the scalar quadratic coefficient is g+2Lambda|F|^2;
the fermion coefficient is g+3Lambda|F|^2. F has no bosonic kinetic term.
These source dictionaries are checked in SOURCES.md; subsequent branch
calculations are direct applications, not MOND claims made by the papers.

For w=0 the nonzero branch has |F|^2=X-g/(2Lambda), and

    L_noncanonical=Lambda(Y-X^2)-g^2/(4Lambda).

A constant vacuum requires Lambda<0. Its potential g^2/(4Lambda) is
negative, its ordinary scalar kinetic cancels, and its fermion kinetic
coefficient is -g/2. On one real scalar Y=X^2, constant Lambda leaves
no derivative response at all. This branch does not supply the target.

The linear superpotential permits a genuinely different result. Put
tau=-Lambda>0 and choose a double auxiliary root f0>0:

    f0^2=g/(6tau), w=-2g f0/3.

Since w is nonzero, the real coefficient multiplying F cannot vanish;
the complex auxiliary equation forces F to be real. At X=0,F=f0,

    V0=g^2/(12tau)>0,
    Z_A=2g/3>0, Z_psi=g/2>0,
    real auxiliary Jacobian=g-6tau f0^2=0.

This is positive energy with positive quadratic propagating kinetic
signs in the rigid constant-field calculation. It is not a regular
microscopic quantum vacuum or a supergravity stress calculation.
The double-root condition w^2=2g^3/(27tau) is an imposed discriminant
condition; off-shell supersymmetry alone does not impose it.

Writing F=f0+z, the branch equation becomes exactly

    X=z^2(3f0+z)/(f0+z).

The lower-F static branch gives, for X=h^2/2,

    E(h)=V0+(g/3)h^2+(2sqrt(g tau)/9)|h|^3+O(h^4).

Thus a regular polynomial off-shell model really can generate a positive
static cubic correction together with positive rigid vacuum energy.
Vacuum positivity by itself is not the obstruction.

## Exact timelike failure, including a decoupled physical ghost

Define y=F/f0 and x=2tau X/g. The exact normalized equation is

    P(x,y)=y^3-3(1+x)y+2=0,
    P(0,y)=(y-1)^2(y+2),
    P(x,1+z)=z^2(3+z)-3x(1+z).

For every real root and -1/4<x<0, y^2>3. An elementary proof uses
P=(y-1)^2(y+2)-3xy to exclude y>=0. If y<0 and y^2<=3, then y>=-2,
y^3>=3y and xy<=-y/4, giving P>=2+3y/4>=1/2, a contradiction.
ChiralFold.lean verifies this implication without numerical root finding.

On a homogeneous timelike real-phi background, the independent chi
quadratic action is

    L_chi,2=[g+2Lambda F^2-2Lambda X] chi_dot^2/2
             -[g+2Lambda F^2+2Lambda X]|grad chi|^2/2.

There is no linear chi variation in X or Y and hence no quadratic
chi--auxiliary or chi--real-field mixing. Its time coefficient is

    g(1+x-y^2/3)<0.

Therefore every surviving real auxiliary solution in that small-timelike
interval has an actual decoupled chi ghost in this specified model.
The critical y~1 branches disappear for x<0; the ghost branch tends
instead to y=-2. It is not a continuous ghost fluctuation on y=1.
The proposed critical vacuum lacks a real auxiliary continuation into
an open timelike neighborhood, and the alternative branch is unhealthy.
Positive quadratic coefficients exactly at the fold missed this failure.

## Force calibration prevents a spurious normalization claim

The cubic is not the leading infrared response: (g/3)h^2 survives.
With the usual scalar source/flux dictionary this gives Newtonian weak
fields, rather than a deep-MOND asymptote. Covariantly subtracting that
quadratic term also removes the scalar quadratic time kinetic. Restoring
time kinetic with a preferred clock is a new operator/sector to derive.

As an algebraic property of the displayed constant-coefficient action,
on the positive-cubic branch at large X,
F~2f0^3/X and E~gX+tau X^2. Its ultraviolet response is quartic,
not the required Newtonian quadratic crossover. This extrapolation does
not establish a physical ultraviolet completion of a truncated effective
action; an ultraviolet completion changing it would require a new check.

The arithmetic combination

    V0 C3_local^2/C2_local^3=1/9,
    C2_local=g/3, C3_local^2=4tau g/81,

is ONLY a nominal local Taylor ratio. C2_local is not an operational UV
force coefficient. It cannot be inserted into the campaign R/xi bridge.
The Lean theorem names this distinction explicitly.

Supersymmetry also permits regular derivative-dependent coefficient
functions. For the local bosonic deformation
Lambda(X)=Lambda0+Lambda1 X+O(X^2), set u=Lambda1 f0^2/Lambda0.
The vacuum values and double-root condition stay fixed, while

    (F-f0)^2=(1-u)X/3+O(X^(3/2)),
    Z_A=g(4+u)/6,
    R_local=(64/9)[(1-u)/(4+u)]^3, -4<u<1.

This is a deformation test, not a target assignment or a claim that all
deformed theories are healthy. Off-shell supersymmetry alone does not
protect even the nominal ratio against the permitted operator freedom.

## Protected vector auxiliary: exact source class and Schur relation

The ordinary/minimal bosonic nonlinear-electrodynamics class has

    L=ell(S+D^2/2,P)-xi_FI D.

Let A=ell_x, b=ell_xx, c=ell_xP, d=ell_PP, H=A+D^2 b. On a smooth
auxiliary branch, direct elimination gives

    Lbar_S=A,
    Lbar_SS=A b/H, Lbar_SP=A c/H,
    Lbar_PP=d-D^2 c^2/H,
    det Hessian_(S,P) Lbar=(A/H)(b d-c^2).

The source convexity class A>0, b>=0, d>=0, c^2<=bd has H>0 and
preserves this invariant-Hessian positivity. With an analytic local action
and gradient portal, regular elimination remains analytic in s=h^2.
For merely C2 data it remains C2, which already excludes s^(3/2).
The source's electric-convexity and
causality necessity statements have explicit domains, recorded in
SOURCES.md; they do not classify every supersymmetric D action.

An auxiliary Hessian's negative sign alone is NOT a physical ghost
proof. In particular b<0,H<0 could still give A b/H>0. Nonconvex
branches require actual propagating, global-energy and quantum checks.

For the particular proposed portal -f(D)s/2, with no additional mixed
operators, replace H by A+D^2b-s f''/2. Its static energy satisfies

    E''(s)=f'^2/(4H),
    Lbar_SS=b(A-s f''/2)/H.

A positive responding cubic branch has H>0 wherever f' is nonzero.
If it approaches a finite regular cusp with H0=0,D0 nonzero,A0>0,
then b0=-A0/D0^2<0; finite f'' gives Lbar_SS<0 sufficiently near it.
At D0=0, the same degeneracy requires A0=0, losing ordinary photon
kinetic. These are restricted portal tests, not a universal exclusion.

For parity-even ell at P=0, the sign gives a direct local causality test:
choose grad phi parallel to an arbitrarily small constant magnetic B,
both along z; use a photon wave along x with electric polarization y.
Then delta s=0, grad phi.dot.k=0 and Lbar_SP=0, so there is no linear
scalar or other-polarization mixing.
The mode has v^2=1-(Lbar_SS/Lbar_S)B^2>1. At each fixed small s, choose
B small enough to stay on its smooth D branch. General ell_xP nonzero
requires a mixed-polarization analysis; this simple eigenmode proof does
not cover it or unspecified additional supersymmetric portal operators.

## Born-Infeld/FI: a calculated positive-energy relation, wrong response

In the source's displayed rigid normalization, take T>0,
B=sqrt(1+xi_FI^2/T), and use the +xi_FI D convention. Exact elimination
gives

    D0=-xi_FI/B, H0=B^3>0,
    L_on=T[1-B sqrt(1-2S/T-P^2/T^2)].

Canonical photon normalization gives T_eff=T B and

    epsilon_displayed=T(B-1),
    0<=epsilon_displayed/T_eff=1-1/B<1.

This is a genuine calculated relation between displayed vacuum energy
and photon nonlinearity, not just parameter counting. But it spans a
free FI/tension ratio and remains analytic; no MOND C3 exists. A
gravitating vacuum interpretation additionally needs a specified
supergravity completion and vacuum reference. The rigid source itself
discusses a constant shift as irrelevant to its electromagnetic dynamics.

Replacing xi_FI by xi_FI-eta s as a diagnostic produces, after critical
linear subtraction, eta^2 s^2/(2B^3)+O(s^3), an h^4 correction. This
replacement is our hypothetical portal, not a supersymmetric operator
established by that source.

## General criticality and remaining scope

A C2 auxiliary action with invertible FULL auxiliary Hessian gives a C2
reduced action by implicit elimination, regardless of vacuum coordinate
or vacuum value. A nonzero vacuum coordinate alone does not remove a
cusp. With x=a-a0, both

    L=gamma x^3/6-c x s/2-epsilon0,
    L=gamma x^6/6-c x^2 s/2-epsilon0

give E=epsilon0+c^(3/2)s^(3/2)/(3sqrt(gamma)) on selected branches.
The second has zero linear null-source overlap at the vacuum. Thus a
nonzero overlap is necessary only for a specified square-root fold,
not all higher-criticality cusps. Both have singular vacuum Hessians.
They are auxiliary branches, not healthy ordinary-scalar energy minima.

If ordinary microscopic variables instead minimize a smooth Hamiltonian
over a fixed common neighborhood, the unchanged vacuum trial gives
E(s)<=E0+C2 s+O(s^2), excluding a positive leading correction C3s^(3/2).
The pure-static constraint-pair rank statement additionally requires
commuting secondary constraints; rank loss is not by itself new gauge
symmetry or a propagating ghost diagnosis.

The remaining protected-auxiliary opening needs an explicitly different
multi-field/clock or generalized-D action, with a regular real dynamical
neighborhood and actual retained mode analysis. It must also derive a
cubic-leading static MOND force, a Newtonian crossover, gravitating
positive vacuum stress and the independent ratio. No result here supplies
those missing implications or a second determinate physical prediction.
