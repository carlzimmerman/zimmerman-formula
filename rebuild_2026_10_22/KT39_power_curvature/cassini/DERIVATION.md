# General-power Cassini calculation

The candidate is P=xR(z), z=x+s^p, s=lambda^2 H:H in Solar rM/a0 units.
The exact searched powers are p=5/4,3/2,7/4; each is combined with the same
six physical lengths on both footings. This is a phenomenological parameter
search in the generalized-action framework. It is not a dynamical-health
theorem or a derived fundamental law.

## Full response and radial product derivatives

Let g=g0(r)n+eta e_z, H=gp nn+gt(I-nn), gp=g0', gt=g0/r. The common simple-Q
primitive has Q(0)=0 and Q'=nu_simple(sqrt z). Put

```
C=R-1+xR', beta=p lambda^2 s^(p-1),
A=Cg, B=DH, D=beta xR', S_ph=div A-double_div B.
```

For lambda>0 the radial Solar Hessian norm is positive at every finite
radius, both for the exterior point field and for a finite Gaussian source.
Thus s>0 and the ordinary radial derivatives are

```
h=s^p,
h'=h p s'/s,
h''=h[p s''/s+p(p-1)(s'/s)^2],
beta'=beta(p-1)s'/s,
beta''=beta[(p-1)s''/s+(p-1)(p-2)(s'/s)^2],
z'=x'+h', z''=x''+h''.
```

The exact lambda=0 branch sets h,beta and their derivatives to zero. It
does not evaluate 0/0 or insert a numerical floor. For E=xR', retain
D'=beta'E+beta E' and D''=beta''E+2beta'E'+beta E''. The scaled derivative
formulas from KT38 calculate E',E'' without forming overflowing z^3.

The angular Green and density expressions are geometric identities and
are unchanged:

```
a=integral (3mu^2-1) C(g0+eta mu) dmu,
b=integral C[eta(3mu-5mu^3)+g0(1-3mu^2)] dmu,
d=integral (3mu^2-1) D dmu,
q_A=(3/2) integral b/r d(log r),
q_B=6 integral (gp-gt)d/r^2 d(log r).
```

For the point field q_B=-18 integral d/r^5 d(log r). The differential
calculation includes every beta derivative above. Outer boundary terms are
retained. All previous source artifacts and validated integrals remain
read-only; none of their empirical grades is assumed for a new power.

## Noninteger powers at zero Hessian

Fix g!=0 and let H approach zero. The energy correction from curvature is
generically proportional to |H|^(2p); B is proportional to
|H|^(2p-2)H at leading order. Consequently the energy is C^2 at H=0 for
every tested power. It is not generally C^3 for p=1.25 or 1.5; at p=1.75
it is C^3 but not generally C^4. B is C^1 for all three, but is not generally
C^2 for p<=1.5. A pointwise classical double divergence across H=0 is
therefore not automatically defined; the variational source remains meaningful
as a weak derivative of B. This limitation must not be hidden by clipping s.

For a transverse smooth spatial zero, the potentially singular second
derivative behaves like distance^(2p-3); at p=1.25 it is integrable but
unbounded, and at p=1.5 it can be direction-dependent. This local description
is not a general regularity theorem for every source. The joint g=H=0 point
also retains the usual MOND nonanalyticity, so the fixed-g statement above
must not be misread as global C^2 regularity in all variables.

The finite Solar calculations never encounter H:H=0. At infinity s tends
to zero and is handled by its integrable radial limit. The exact zero-length
and Newtonian controls are separate algebraic branches. Static uniform-field
linear-response behavior does not establish dynamical or relativistic health.

## Origin contacts and Gaussian point-source limit

For a regular radial core g0=kr+O(r^3), let s0=3lambda^2 k^2 and
z0=eta^2+s0^p. With x derivatives holding H fixed,

```
C_x=2R'+xR'', D_xx=p lambda^2 s0^(p-1)(2R''+xR'''),
q_A,contact=8k eta^2 C_x/15,
q_B,contact=-(8/3)k^3 eta^2 D_xx.
```

A Gaussian has k proportional to sigma^-3. Since R^(j)=O(z^-j-1/2) at
large z, both contacts vanish as

```
O(eta^2 sigma^(9p-3)/lambda^(3p)).
```

The Gaussian-limit proof from KT37/38 extends without relying on numerical
sampling. Rodrigues' identity gives

```
|b|<=C[eta^2g^3|C_xx|+eta^4g^3|C_xxx|],
|d|<=C eta^2g^2|D_xx|.
```

At large z, |C_xx|<=Cz^-5/2 and |C_xxx|<=Cz^-7/2. For p>1,
beta<=p lambda^2 z^((p-1)/p), and z>=s^p>=2^p lambda^(2p)g^(2p)/r^(2p).
These imply the uniform core estimates, for every sigma<=delta,

```
|q_A(core)|<=C[eta^2 delta^(15p-7)/lambda^(5p)
               +eta^4 delta^(21p-7)/lambda^(7p)],
|q_B(core)|<=C eta^2 delta^(9p-3)/lambda^(3p).
```

To check the powers, substitute g=sigma^-2 f(v), v=r/sigma. The three
integrands become v^(5p-1)f^(3-5p), v^(7p-1)f^(3-7p), and
v^(3p)|f'-f/v|/f^(3p). All are O(v^2) at zero. At large v their powers
are 15p-7, 21p-7, and 9p-3, respectively. All are positive for p>1, so
integration up to delta/sigma gives exactly the stated uniform bounds.

Gaussian mean-density monotonicity supplies a uniform high-z core, as in
the previously reviewed proof. Exterior coefficients converge to their point
values. For eta>0 the A radial tail is O(r^-7), and the B tail is
O(r^(-6p-3)); both are uniformly integrable for the tested powers. The
uniform core estimates, vanishing contacts, and exterior dominated convergence
therefore prove the fixed-p, fixed-positive-lambda Gaussian STF limit.

This is an observable-specific regularization statement, not permission to
square a distributional Newtonian Hessian, regulator independence, or a
simultaneous lambda-to-zero theorem. The p=1 and p=2 endpoint calculations
are additionally compared with their previously validated numerical results.

## Bounded verification contract

Compute all 18 declared (p,ell) choices on both footings, using base
8000x160 and fine 16000x320 quadrature with expanded radial domain. Apply
the unchanged 2e-4 relative Green/density and refinement gates. Test tensor
API agreement separately for each p, exact Newtonian and zero-external-field
controls, and shared ell=0 QUMOND/contact controls. At ell=1.5 kpc, test
Gaussian widths .5,.1,.01,.001,5e-7 rM for each power and footing; use
rmin=max(1e-10,.001sigma) with analytic contacts, plus half/quarter-cutoff
checks for the broadest core. Keep all completed and failed evidence.
