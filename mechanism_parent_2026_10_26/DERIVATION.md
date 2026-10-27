# A density-tracking internal field: conditional mechanism, not closure

## Definitions and hypotheses

Use metric (-,+,+,+), c=1. J^mu=n u^mu is an effective conserved medium current,
u.u=-1 and n>0. This hydrodynamic variable need not count fundamental particles;
its existence is an assumption, not a demonstrated property of cold dark
energy. A current-constraint multiplier enforces nabla_mu J^mu=0. The
irrotational fluid action is -epsilon(n)+J^mu partial_mu theta; circulation
labels would be required for a general vortical fluid. Define
w=n epsilon'(n)>0 and c_s^2=n epsilon''(n)/epsilon'(n), with 0<c_s^2<1.
Results below concern a uniform rest state and local longitudinal perturbations,
without gravity, conversion, background chi gradients or the phase carrier.

Let chi be the outgoing real scalar and s a real internal medium field. They
are new completion assumptions. M>0, h and lambda are constant input parameters.
Neither s nor J is being asserted to be an observed particle species.

## Route 1: a conserved charge alone is insufficient

For constant g1, integral g1 J^mu partial_mu chi is a boundary term when
nabla.J=0. Its bulk Euler derivative vanishes. If conversion gives nabla.J=Gamma,
it sources -g1 Gamma instead; that is a different premise. This reproduces the
earlier obstruction and rules out only the pure conserved-current route.

## Route 2: ordinary mediator exchange changes the static equation of state

Put Y=J^mu partial_mu chi. An algebraic heavy field with

    L_s = -M^2 s^2/2 + a n s + h s Y

gives s=(a n+hY)/M^2 and

    Delta L = a^2 n^2/(2M^2) + ah nY/M^2 + h^2 Y^2/(2M^2).

The desired compression term arrives with a density potential and a kinetic
companion. The first lowers static energy and can change stability. Dropping
these terms while retaining only the middle one is not this mediator theory.
This construction fails the requirement of unchanged local static energy.

## Route 3: explicit tracking parent

Consider the covariant classical action density (without sqrt(-g))

    L = -epsilon(n)+J.partial theta
        - (partial chi)^2/2 - (partial s)^2/2
        - M^2 (s-lambda n)^2/2 + h s Y.

The completed square is an assumption tying the density counterterm to the
mediator coupling. It is not fixed by a0, Lambda or symmetry established here.
The exact internal-field equation is

    (M^2-Box)s = M^2 lambda n + hY.

At frequencies and inverse lengths small compared with M, solving this equation
in a derivative expansion gives, at leading algebraic order,

    s = lambda n + hY/M^2,
    Delta L_eff = g2 nY + alpha Y^2/2,
    g2=h lambda,                 alpha=h^2/M^2 >= 0.

The first derivative correction includes -(lambda^2/2)(partial n)^2. The
expansion has a cutoff; it is not a new fundamental higher-derivative theory.
Homogeneous heavy-field solutions require initial data and are not removed by
writing this low-frequency particular solution. A retarded inverse must not
be inserted into an ordinary single-copy variational action without care.

In the nonrelativistic rest-frame limit, nY=n^2 chi_t+n j.grad chi. Thus the
leading term reproduces the density-weighted current structure, subject to a
consistent normalization between n and the old material mass density rho.
It does not by itself reproduce the Schrödinger quantum gradient, alignment,
carrier, gravity or nonlinear conversion of the full CC benchmark.

Varying chi in the parent gives

    Box chi = h nabla_mu(s J^mu).

Equivalently chi_tt-lap chi=-h nabla.(sJ) in flat space. For conserved J and
s approximately lambda n, the source is g2 J.partial n. Continuity implies
u.partial n=-n nabla.u, hence the compression source is -g2 n^2 nabla.u.
It is nonzero in a compressing medium even though total J charge is conserved.
The exact parent source is h J.partial s; finite response time is retained.
The chi shift current is -partial^mu chi+h s J^mu. Its conservation accounts
for scalar plus medium charge, not separately conserved scalar momentum.

## Quadratic Hamiltonian of the parent

Set n=n0, s0=lambda n0 and chi constant. Let xi be a longitudinal displacement,
delta n=-n0 div xi, and b=delta s. The term h s0 J.partial chi is a boundary
term for the full conserved current. Up to quadratic order the remaining action
is therefore

    L2 = w |xi_t|^2/2 - w c_s^2 (div xi)^2/2
         + (b_t^2-|grad b|^2)/2
         - M^2 (b+lambda n0 div xi)^2/2
         + (chi_t^2-|grad chi|^2)/2 + h n0 b chi_t.

With p_chi=chi_t+h n0 b, p_b=b_t and p_xi=w xi_t,

    H2 = |p_xi|^2/(2w)+p_b^2/2+(p_chi-h n0 b)^2/2
         + w c_s^2(div xi)^2/2 + |grad b|^2/2
         + M^2(b+lambda n0 div xi)^2/2 + |grad chi|^2/2.

Every displayed contribution is nonnegative. For nonzero longitudinal k and
c_s^2>0 the oscillator Hamiltonian is positive definite. This proves local
linear energetic stability in this sector; it is not global nonlinear stability
of the full framework. Dust c_s=0 has a zero-frequency density mode and must be
handled as a semidefinite limiting case.

## Exact dispersion and causal principal cone

Define D=M^2 lambda^2 n0^2/w, H=h n0, B=M^2 lambda n0 and x=omega^2. The
Hermitian frequency matrix, with exp(i k z-i omega t), is

    [ w((c_s^2+D)k^2-x),  -i B k,                 0 ]
    [ i B k,              k^2+M^2-x,      i H omega ]
    [ 0,                 -i H omega,          k^2-x ].

Its determinant vanishes exactly when

    w[(c_s^2+D)k^2-x][(k^2+M^2-x)(k^2-x)-H^2 x]
      -B^2 k^2(k^2-x)=0.

At k=0 there are two zero roots and a massive root M^2+H^2. At large k the
principal squared speeds are c_s^2+D, 1 and 1. Thus this homogeneous linear
parent has no faster-than-light characteristic if

    0 <= D <= 1-c_s^2.

The density-mediator cross term has only one spatial derivative; b chi_t has
one time derivative. Neither changes these principal speeds. Massive-mode
phase velocity is not a signal/front velocity. No arbitrary-background or
curved-space hyperbolicity claim is made.

## The compulsory kinetic term resolves the old local cone defect conditionally

Eliminate b only at low frequency and k. Put
A=1+H^2/M^2 and C=g2 n0^2. The effective L2 is

    L2_eff = w |xi_t|^2/2-w c_s^2(div xi)^2/2
             + A chi_t^2/2-|grad chi|^2/2-C div xi chi_t.

The squared phase speeds v obey

    A v^2-[1+A c_s^2+C^2/w]v+c_s^2=0,
    C^2/w=(A-1)D.

Here v denotes speed squared, not speed. For 0<c_s^2<1 and C!=0, the lower
root lies below c_s^2 and the upper above it. Evaluating the polynomial at1
gives (A-1)(1-c_s^2-D). Therefore the upper low-energy speed is <=1 exactly
when D<=1-c_s^2 (for A>1). At A=1 the uncoupled speeds are c_s and1.
This agrees with the parent principal-cone condition.

If one discards the alpha Y^2 term while keeping g2, A becomes1 at C!=0 and
the polynomial at1 is negative: the upper speed exceeds1. The earlier
superluminal local branch can therefore result from omitting a term required
by this particular parent. Adding the term changes the model and all prior
numerical trajectories require new validation. No claim is made that this is
the unique relativistic completion or that its coefficients have been derived.

## Static cost: exact locality is not free

With chi constant and a prescribed nonuniform static n, the parent minimizes

    E_s = integral [|grad s|^2+M^2(s-lambda n)^2]/2.

In Fourier space s_k=M^2 lambda n_k/(M^2+k^2), and the minimized excess energy
per Fourier norm is

    Delta E_k = lambda^2 M^2 k^2 |n_k|^2/[2(M^2+k^2)] >=0.

It vanishes for uniform n, but not generally for a galaxy profile. The first
long-wave term is lambda^2 |grad n|^2/2. Exact inherited static forces are not
preserved at finite M. At fixed g2 and alpha, lambda=g2/(M sqrt(alpha)), so
this correction can be parametrically small as M increases, while
D=g2^2 n0^2/(alpha w) is unchanged. This is a classical family, not evidence
of perturbative quantum control: h=M sqrt(alpha) also grows.

Uniform local causality across a density range requires

    alpha >= g2^2 n^2/[w(n)(1-c_s(n)^2)]

throughout that range. A bound at one density does not suffice. For w roughly
proportional to n and nonzero constant g2, no finite constant alpha covers
arbitrarily large density. A cutoff, changed high-density physics or a derived
density-dependent completion is necessary; an invented gate is not a solution.

## What this mechanism would do, and what remains missing

Gravity can compress the medium; its internal s equilibrium changes; the
derivative interaction drives chi; outgoing chi transports energy while the
same action gives the reciprocal reaction. No assigned friction is necessary.
This supplies a concrete local parent candidate for one link in the chain.

It does not guarantee sufficiently rapid radiation. Constant sources build
near fields; time-varying sources radiate, and the extra inertia can reduce
frequencies. The full finite-body scattering/escape problem, total-mass
redistribution, phase conversion, moving boundary and galaxy law must still
be solved together. Existing CC pulse measurements are evidence for the OLD
action, not measurements of this new parent's efficiency. The values of g2,
M, alpha, the medium EOS and kappa=1/2 remain underived.
