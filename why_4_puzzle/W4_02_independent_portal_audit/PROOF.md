# W4-02 mathematical claims and derivations

Conventions: epsilon is energy per spatial volume, rho_DE=epsilon/c^2;
G_n is calibrated by g_N=G_n M/r^(n-1) in n spatial dimensions;
K_n=Omega_(n-1)G_n. All statements concern the displayed effective sectors.
The quadratic interpolation and a full covariant completion are not assumed.

## Claim A: a fixed-background constitutive family

For every integer n>=2, G_n,c,epsilon,xi>0 and gamma>=0, put

    a = sqrt(xi G_n epsilon),
    F(t) = -t-log(1-t)-t^2/2,   0<=t<1,
    W_xi(u;epsilon) = a^2/K_n F(u/a),
    L = -|grad Phi-K_n P|^2/(2K_n)-rho_b Phi
        -W_xi(K_n|P|;epsilon)-(gamma/2)|grad P|^2.

The claim is that W_xi is convex as a radial potential, vanishes together
with all derivatives with respect to epsilon at u=0, and gives the same
dimensionless simple-mu law for every xi in the algebraic spherical limit.
In that limit the stiffness contribution to the P equation is omitted.
Retaining stiffness does not preserve that algebraic equation.

Proof: [G_n]=L^n M^-1 T^-2 and [epsilon]=M L^(2-n) T^-2, so a is an
acceleration in every n. The positive series F(t)=sum_(j>=3) t^j/j gives

    K_n W'_xi=u^2/(a-u),
    W''_xi=u(2a-u)/(K_n(a-u)^2),
    W'_xi/u=u/(K_n(a-u)).

The last two quantities are positive for 0<u<a; the Hessian at the origin
is zero. For W(K_n|P|) the Hessian eigenvalues multiply these by K_n^2.
Rotations are preserved. The stiffness term has the same nonnegative gamma
for every xi.

For aligned spherical magnitudes the algebraic P variation is
`g-u=K_n W'_xi`, whence `u=ag/(a+g)`. Phi variation gives
`div(grad Phi-K_n P)=K_n rho_b`. Spherical flux integration therefore yields

    g_b=g-u=g^2/(a+g),
    y=x^2/(1+x),  x=g/a, y=g_b/a.

The choice of inward/outward signs is absorbed in the aligned magnitudes;
the vector equations have the conventional outward grad Phi for an attractive
Newtonian potential.

Because W_xi(0;epsilon) is identically zero as a function of epsilon, all its
source derivatives there vanish. If epsilon=V(chi)>0, its first and second
chi variations vanish on P=0. The metric-independent zero P configuration
also has zero first metric variation of this added potential. Thus the
potential and stiffness add no homogeneous vacuum contribution on that
background. No covariant kinetic term for P is specified by this claim.

The source dependence at finite polarization is nontrivial:

    epsilon d_epsilon W = a^2/(2K_n) [2F(t)-tF'(t)],
    2F(t)-tF'(t) = -sum_(j>=3) (j-2)t^j/j < 0.

The exact deformation is

    xi -> s^2 xi,  a -> s a,
    W_(s^2 xi)(u;epsilon)=s^2 W_xi(u/s;epsilon),  s>0.

It preserves the properties above at fixed epsilon. The physical force scale
changes. For constant G_n and xi it gives the same tracking relation
`a(t)/a(t0)=sqrt(epsilon(t)/epsilon(t0))` for all xi. Nevertheless
`a^2/(G_n epsilon)=xi` ranges over all positive numbers. Fixing these
properties alone therefore does not imply xi=1/4.

## Claim B: a preferred-frame scalar with subluminal linear response

This is a separate explicit toy; it is not claimed to equal the stiffened P
action, the quadratic interpolation, or a complete cosmological theory.
In flat spacetime with a specified preferred time, fix the same epsilon>0,
K_n,c>0 and use the physical potential Phi with fixed source coupling:

    L = (partial_t Phi)^2/(2K_n c^2)-E_a(|grad Phi|)-rho_b Phi-epsilon,
    E_a(g) = [g^2/2-a g+a^2 log(1+g/a)]/K_n,
    a = sqrt(xi G_n epsilon), xi>0.

For a locally constant background gradient g>0 and nondynamical fixed source,
the scalar has positive time kinetic energy, nonnegative source-free field
energy after subtracting the common vacuum epsilon, and a strictly hyperbolic
principal symbol with characteristic cone inside the matter Minkowski cone.
It gives the simple-mu spherical static law and has the same Newton G_n at
large acceleration for every xi. These are local statements on those
backgrounds, not global nonlinear well-posedness or full-system stability.

Derivation: E_a(0)=0 and E'_a=g^2/[K_n(a+g)]>=0. Let
`mu=g/(a+g)`. The transverse and longitudinal eigenvalues of the spatial
Hessian of E_a are mu/K_n and

    E''_a = [1-a^2/(a+g)^2]/K_n = (2mu-mu^2)/K_n.

Dividing by the time kinetic coefficient gives

    v_T^2/c^2=mu,
    v_L^2/c^2=2mu-mu^2.

Both are strictly between zero and one at every finite g>0; the speed in an
arbitrary direction is between these two. At g=0 the spatial principal symbol
degenerates. At g->infinity both speeds approach c. The source-free Hamiltonian
above its fixed vacuum is `(partial_t Phi)^2/(2K_n c^2)+E_a(g)>=0`.
The static equation is `div(mu grad Phi)=K_n rho_b`, giving Claim A's
spherical law. The same calculation applies in n spatial dimensions.
Here the vacuum term is an externally fixed common constant, not a covariant
stress-tensor construction. The dependence of a on a varying dynamical
epsilon can be added at the effective level but its coupled perturbations
are outside this proposition.

The exact cone relation `v_L^2/c^2=2(v_T^2/c^2)-(v_T^2/c^2)^2` is common to
all xi. Even positive subluminal response and its high-field luminal limit
do not distinguish xi within this class.

### Supplemental quadratic-law member

This analytic extension was added after the first symbolic run, before its
independent review. It is not counted as an originally frozen numeric trial,
and the current checker does not test its formulas.

For the framework's quadratic branch `g^2=g_b^2+a g_b`, define instead

    h_a(g)=(sqrt(a^2+4g^2)-a)/2,
    E_a^Q(g)=[g sqrt(a^2+4g^2)/4+(a^2/8)asinh(2g/a)-a g/2]/K_n.

Use the same preferred-frame scalar action as Claim B with E replaced by
E^Q. Direct integration gives `K_n (E^Q)'=h_a(g)`, so the spherical static
equation gives exactly `g_b=h_a(g)` and therefore the quadratic branch.
The squared characteristic speeds, in units of c^2, are

    v_T^2/c^2=h_a(g)/g=2g/(sqrt(a^2+4g^2)+a),
    v_L^2/c^2=h'_a(g)=2g/sqrt(a^2+4g^2).

Each is strictly between zero and one for a,g>0. The potential energy starts
at zero and has positive derivative. The same fixed-vacuum and arbitrary-xi
conclusion therefore holds for this separate quadratic effective toy, with
the same limitations at g=0 and for a full covariant completion.

## Claim C: scope of pi parity

In four spacetime dimensions assume Friedmann
`H_Lambda^2=(8pi/3)G rho_DE` and put `q=a0/(c H_Lambda)`.
Then `kappa^2=(8pi/3)q^2`.

If `q=R(pi)` for a nonzero rational function R(z) with algebraic
coefficients, kappa^2 cannot equal 1/4. Indeed equality would make
`z R(z)^2-3/32` vanish at pi. Since pi is transcendental, that rational
function must vanish identically (after clearing denominators).
But its proposed identity `z R(z)^2=3/32` has order at zero
`1+2 ord_0(R)=0`, impossible for integral ord_0(R).

The monomial subcase q=A pi^m, A algebraic nonzero and m integer, gives the
usual odd-power expression `(8/3) A^2 pi^(2m+1)`.
The hypothesis on R is essential. For the prescription
`a0=c^2/sqrt(A_dS)`, `A_dS=4pi c^2/H_Lambda^2`, one obtains
`q=1/sqrt(4pi)` and `kappa^2=2/3`. This is not a selection mechanism, but it
shows that horizon inputs alone do not imply the coefficient-field hypothesis.
The standard transcendence of pi is the external mathematical leaf; no claim
of a new transcendence proof or exhaustive classification is made here.
