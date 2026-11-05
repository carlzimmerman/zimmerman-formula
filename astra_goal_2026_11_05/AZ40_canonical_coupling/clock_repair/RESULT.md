# Tested gradient bound and an explicit bounded-expansion action candidate

The existing radial backgrounds pass the corrected static gradient bound.
For the clock, a bounded-expansion action provides a concrete way to exclude
the known volume-fold mechanism, and its homogeneous nonlinear collapse test
continues beyond the unmodified collapse time. This is a candidate repair,
NOT a completed healthy action: general inhomogeneous continuation and the
rolling-scalar coupled constraints remain unproved. Kappa=1/2 remains FITTED.

Base a6c19b3845fa8b48387e9a17dc3bacd9ef4f6df7. Scope frozen a43dd525d4;
cap extension f669c6e53a; nonlinear test bf032fb1b5. Author self-review only.
No other action lane, observational gate or adopted action is changed.

## 1. The gradient bound passes on the existing solved backgrounds

All24 original AC1 finite-box radial BVPs were regenerated with their original
physical equations, source subtraction, boundary conditions, continuation
order and two mesh/tolerance settings. These are the previously specified
quasistatic backgrounds, not full relativistic cosmological/galactic solutions.
The two radial variables are u=p/a_bar and d, with

    psi=psi_bar+epsilon*d, epsilon=2*(a_bar R/c^2)^2,
    A=a/a_bar=[sinh(psi/B)/sinh(1)]^(-n),
    n=(1-beta)/beta, B=2 sqrt(3(1-beta))/(3 beta),
    C=4pi/xi, xi=.5/(1+beta), Jbg=C*(A^2)_psi at psi_bar.

Let s=u/(A-u), J(s)=2log(1+s)-4s/(s+2)>0. The actual equation uses
Delta psi=epsilon*(U_psi-Jbg). Therefore the bound for the canonically
normalized scalar variation is

    B_J=epsilon*[A_psi^2(2C+J(s))+(A_psipsi/A_psi)*Jbg]
          -epsilon^2*(A_psipsipsi/A_psi)*|grad d|^2.

The Jbg term is essential and positive on these decreasing-sinh backgrounds.
The first run solved all24 models but failed serializing a NumPy integer;
SERIALIZATION_FAILURE.md preserves that implementation failure. The repaired
run changes only the integer serialization and is evidence/gradient_verified.

There are8 epsilon=0 controls, for which B_J=0 as required, and16 nonzero
models. All16 have a positive conservative spline envelope. Minimum B_J
across the four source/stiffness combinations at each beta and length is:

| beta | a_bar R/c^2 | minimum lower envelope B_J |
|---|---:|---:|
| 2/3 | 1e-4 | 2.0509348984e-6 |
| 2/3 | 1e-3 | 2.0509250309e-4 |
| .9 | 1e-4 | 1.4275060734e-6 |
| .9 | 1e-3 | 1.4274956909e-4 |

The negative-gradient contribution divided by a conservative lower bound on
the positive part is at most7.34668504e-6. This is a dimensionless ratio,
not an observational tolerance. The scalar gradients are far below this
particular static-energy obstruction on the tested solutions.

The bound is stronger than checking a finite sample alone. For each numerical
cubic spline, we find all component extrema and derivative extrema piece by
piece. With ymin,ymax and Dmax=max|d'| from that interpolation, monotonicity
of the sinh derivatives and J>=0 give

    B_J/epsilon >= 2C*|A_psi(ymax)|^2
      +|Jbg|*[n coth(ymax)+csch(ymax)^2/coth(ymax)]/B
      -epsilon*[n^2 coth(ymin)^2+(3n+2)csch(ymin)^2]*Dmax^2/B^2.

This also checks0<u<A across the spline by conservative separate envelopes.
The stored fine_splines.npz contains every fine solution's knots and cubic
coefficients. Floating-point extrema have a small explicit padding; they are
NOT directed-rounding interval certificates for the exact BVP solution.
No rigorous bound on the distance from the numerical spline to the exact
continuum BVP is claimed. Boundary assumptions of the parent energy estimate
still apply; this is not a complete dynamical spectrum or unrestricted
finite-box boundary-stability proof.

Verification:

- All24 BVP pairs converge. Maximum normalized profile discrepancy3.3541e-7,
  below the unchanged1e-4 requirement.
- Maximum normalized envelope difference between the two solves1.3581e-11,
  below1e-3. The regenerated old summaries agree to1.2594e-17.
- Recovering the original Schur curvature from B_J+Delta|A_psi|/|A_psi|
  gives maximum normalized residual4.7974e-15.
- Omitting Jbg makes that identity fail in every model; even the smallest
  maximum normalized error is.6418. This catches a physically important
  misuse of the cosmological subtraction.
- Physical polarization domain, active switch and the zero-epsilon limit
  pass. Runtime4.2seconds, one numerical-library thread.

No result here transfers automatically to the changed action below.

## 2. Which simple clock repairs actually fail the discriminator

### Canonical clock: works in a narrow setting, not a general clock guarantee

For a free canonical clock in fixed1+1 Minkowski,

    tau=t+f(x-t)+g(x+t),
    Q^2=tau_t^2-tau_x^2=(1-2f')(1+2g').

For the same unit-gradient initial data as the geodesic example,
tau_x=-p(x), tau_t=sqrt(1+p(x)^2), the two factors initially are
sqrt(1+p^2)+p and sqrt(1+p^2)-p. Each is positive and thereafter merely
translates. For bounded p, Q^2 has the positive lower bound
exp[-2 asinh(max|p|)]. Smooth free waves therefore avoid that planar clock
failure. This is an exact improvement over the pressureless eikonal equation.

It does NOT supply a general clock repair. In3+1 fixed Minkowski choose
smooth spherical data

    tau(0,r)=f(r)=.1 exp[-(r^2-100)^2/400], tau_t(0,r)=1.

They have |f'|<=.4, hence Q^2>=.84 initially. To see the bound, put
z=(r^2-100)/20. Then |f'|=.2*(r/10)*|z|exp(-z^2),
r/10<=1+sqrt(|z|), and each of |z|exp(-z^2), |z|^(3/2)exp(-z^2) is<=1.
The free spherical wave is smooth, but at its center

    tau_t(t,0)=1+2f'(t)+t f''(t),
    tau_t(0,0)=1, tau_t(10,0)=-1.

By continuity it reaches zero; tau_r(t,0)=0 by spherical symmetry, so Q=0
at a finite time. The scalar field itself has no wave caustic: it fails to
remain a timelike clock. This distinction matters for the action.

There is a second obstruction on fixed de Sitter. A homogeneous free clock
has tau_dot proportional to R^-3. The exact massless mode
cos(k eta)+k eta sin(k eta) tends to a spatially varying constant; its
physical spatial gradient falls as R^-1 while its time derivative falls as
R^-2. An initially small mode therefore eventually overwhelms the homogeneous
timelike gradient. Finally, adding canonical clock pressure to the actual
P.A action does not yield a free wave equation: P responds to acceleration.
None of these free-field proofs is silently promoted to the coupled action.

Hard identification tau=f(phi) removes the independent geodesic clock, as in
AC2, but still requires preservation of timelike grad(phi). The free-field
counterexample explains why that requirement cannot be replaced by the words
"canonical scalar." The separate single-clock work remains a candidate route.

### Expansion squared alone: the native cancellation is decisive

For a frozen flat gravity/clock block, write M=Mpl, zeta the spatial curvature,
alpha the lapse, X=delta Theta, and c(k) the induced lapse-gradient coefficient.
Adding -M^2 b X^2/2, b>0, gives

    L2/M^2=3 zetadot^2-2 zetadot X-b X^2/2
              +k^2 zeta^2+2k^2 alpha*zeta+(c(k)k^2+mu_K^2)alpha^2.

Eliminating both X and alpha gives the kinetic coefficient3+2/b>0 and

    omega^2 = b*k^2*[(1-c)k^2-mu_K^2]
                  /[(2+3b)*(c*k^2+mu_K^2)].

This is a restricted operator check, not the complete rolling-scalar spectrum.
At P=0 with no active polarization stiffness, c=1. For mu_K=0 the restoring
force is exactly zero, irrespective of b. For mu_K>0 the expression is negative.
Thus an expansion-squared term alone cannot be advertised as a nondegenerate
caustic regulator at the native polarization null. The same cancellation
persists if b is replaced by a positive spatial-wave-number-dependent b(k).

A bare acceleration counterterm -eta*M^2*A_mu A^mu,0<eta<1, changes c to1-eta
and repairs this simple linear sign at mu_K=0. But its static spherical law is

    g_b=(1+eta)g-a*g/(a+g),
    g_b/g -> eta as g->0.

It replaces the exact deep-MOND square-root law by a linear response at
sufficiently low g. Setting eta=0 restores MOND and the null cancellation.
That is a mathematical tradeoff, not a permitted observational pass.

The nondegenerate alternative tested here is unswitched positive polarization
stiffness: c(k)=1/[1+Lstar^2*k^2/2]. With mu_K=0,

    omega^2 = [b/(2+3b)]*(Lstar^2/2)*k^4 > 0, k>0.

This changes the native switch and introduces dispersive rather than a finite
metric-speed propagation cone in this operator test. Positive omega^2 does not
by itself establish nonlinear regularity or acceptable causal propagation.

## 3. An explicit candidate action, rather than an imposed zero-charge sector

Keep independent tau and phi, signature(-+++), X_phi=-grad(phi)^2/2,
Q=sqrt(-grad(tau)^2)>0, n=-d tau/Q, Theta=nabla_mu n^mu, A=n.nabla n,
and P spatial to n. Set mu_K=0 and replace the switched stiffness by the
smooth unswitched term. Define

    Z=Theta-Theta_star(phi),
    Fcap(Z)=M^2 b T^2 [sqrt(1-Z^2/T^2)-1], b>0,T>0, |Z|<T.

Here T is a new maximum deviation of expansion, with inverse-time units;
b is a new dimensionless coefficient. They are not predicted by the old action.
The candidate is

    S=integral sqrt(-g) {
        M^2 Rcurv/2+X_phi-V(phi)+P.A-W(p,a(phi))
        -gamma/2*(D.P)^2+Fcap(Theta-Theta_star(phi))
        +lambda_P n.P } + S_m[g],
    p=K sqrt(P.P), K=4piG, W=a^2/K[-p/a-log(1-p/a)],
    gamma=K Lstar^2/2>0, a^2=xi G V.

For the chosen sinh scalar/dust branch, a concrete branch-preserving choice is

    Theta_star(phi)=sqrt[6V/(M^2(1+beta))]*coth(y),
    y=(phi-phi_star)/B, B=2M sqrt(3(1-beta))/(3beta).

It is exactly3H on that branch. Fcap(0)=Fcap'(0)=0, so its homogeneous
background equations are unchanged there. This choice is engineered from the
selected branch; it is not a universal density identity or a derivation of xi.
The normalization remains kappa^2=xi(1+beta)/2.
A literally static clock with Theta=0 is inside the cap domain only when
|Theta_star(phi)|<T; a cosmologically matched local clock need not have
Theta=0. This is another condition for its own background solve, not a free
static-limit assumption.

An equivalent auxiliary form, useful for equations and numerics, is

    Fcap=M^2[-lambda_c Z+T sqrt(lambda_c^2+b^2 T^2)-b T^2],
    Z=T*lambda_c/sqrt(lambda_c^2+b^2 T^2).

Eliminating lambda_c yields the displayed square root. For finite lambda_c,
|Z|<T automatically. The effective local expansion coefficient is

    -Fcap''/M^2=b/[1-Z^2/T^2]^(3/2)>0.

The cap is a variational term, not an added viscosity. In tau-adapted ADM
coordinates Theta is the trace of extrinsic curvature. The action uses spatial
lapse derivatives and first metric time derivatives, with auxiliary P and
lambda_c; no explicit lapse time derivative or second metric time derivative
is introduced in this chart. This structural observation is not a complete
nonlinear Dirac constraint-rank proof on every background.

Its clock variation is explicit. Since Fcap'=-M^2 lambda_c,

    E_n_mu(cap)=M^2 partial_mu lambda_c,
    J_cap^nu=(M^2/Q)h^{nu mu} partial_mu lambda_c,
    delta_phi L_cap=+M^2 lambda_c*Theta_star,phi*delta phi.

The projected divergence of J_cap enters the actual tau equation. The old
P=0,Q=1 geodesic construction no longer solves the whole system for arbitrary
spatially varying compression. On an entire P=0 branch with suitable zero-flux
boundary conditions, the tau equation reduces to the elliptic condition on
lambda_c; a nonuniform geodesic expansion cannot simply be prescribed for free.
These modifications must also be retained in new sourced-background equations.

## 4. What the cap proves geometrically, and what it does not

For the proper-volume Jacobian Jvol of a regular timelike congruence,

    d log Jvol/ds=Theta.

If |Theta_star(phi)|<=Hstar_max on a finite proper-time interval, the cap gives

    Jvol(s)>=Jvol(0)*exp[-(T+Hstar_max)*s]>0.

Thus the original volume-fold mechanism, whose expansion diverges to minus
infinity, cannot occur within a regular solution staying in this domain.
For the planar geodesic example Theta=-lambda_0/(1-lambda_0*s) and
Theta_star=0, with0<lambda_0<T, the old trajectory reaches -T at
s=1/lambda_0-1/T, before its unmodified fold1/lambda_0. The changed equations
must depart from that trajectory or cease to have a regular solution.

That final alternative cannot be hidden. Fcap remains finite at |Z|=T even
though its derivative and lambda_c diverge. A cap is NOT automatically an
infinite positive-energy barrier. It might replace the fold by failure at the
cap, unbounded shear, lapse degeneration, scalar blow-up or loss of a timelike
clock. The Jacobian argument alone proves none of their exclusions.
The next calculation supplies a nontrivial nonlinear example in which finite-
time continuation actually works, rather than assuming it from the inequality.

## 5. Exact nonlinear collapse test: vacuum Bianchi I

Isolate EH+Fcap(Theta), with Theta_star=0,P=0 and no rolling scalar. This is
a nonlinear test of the proposed operator, not a solution of the full
sinh-portal candidate. Use proper time, volume V=product of directional scale
factors, Theta=Vdot/V and sigma^2=(1/2)sum_i(H_i-Theta/3)^2.
Anisotropy momenta are conserved because Fcap depends only on the trace:

    sigma^2=S0/V^2, S0>0.

Varying the lapse BEFORE setting it to1 gives exactly

    Theta^2/3+b T^2[1/sqrt(1-Theta^2/T^2)-1]=S0/V^2.

Set r=-log(sqrt(1-Theta^2/T^2)). On the contracting branch,

    T^2[(1-exp(-2r))/3+b(exp(r)-1)]=S0/V^2,
    Theta=-T sqrt(1-exp(-2r)),
    Vdot=Theta V.

The left side is zero at r=0, strictly increasing, and unbounded, since
its derivative is T^2[2exp(-2r)/3+b exp(r)]>0. For every V>0 there is
one finite r>0 and a smooth contracting solution. Moreover

    V0 exp(-Tt)<=V(t)<=V0

for all finite t>=0. On any finite interval this bounds the shear, r,
lambda_c=b*Theta*exp(r), and all directional Hubble rates. The right-hand
side of the V equation remains smooth on the resulting compact positive
V interval, so the solution extends through every finite proper time.
The directional scale factors and their derivatives stay finite and nonzero
on such intervals. This is an analytic finite-time continuation result for
this homogeneous sector, not merely a successful finite integration.

The remaining trace equation is also satisfied, not discarded. Writing
f=Fcap/M^2, volume variation of the minisuperspace action gives

    (-2/3+f'')*Theta_dot-2sigma^2=0

once the lapse constraint is used. Differentiating that constraint and using
sigma^2_dot=-2Theta*sigma^2 gives exactly the same equation on the contracting
branch. Thus the algebraic constraint plus shear conservation and the volume
ODE solve the homogeneous spatial equations as well as the lapse equation.

Unmodified vacuum GR instead gives V=V0-sqrt(3S0)t and reaches zero at
V0/sqrt(3S0). The comparison holds V0 and shear momenta fixed; the initial
trace expansion differs because each theory has its own lapse constraint.

Six numerical corroborations use T=V0=1,b=.1,1,10 and S0=1/3,3, through
five times that unmodified collapse time. All six continue with positive V
and a strictly interior cap argument. Representative S0=1/3 values are:

| b | V at original collapse time t=1 | V at t=5 |
|---:|---:|---:|
| .1 | .38000818 | .00696197 |
| 1 | .48170882 | .00916927 |
| 10 | .75702401 | .04981188 |

All11 checks pass. Maximum two-tolerance volume disagreement3.883e-10;
maximum normalized constraint residual9.253e-14. For b=.1 the final gap
1+Theta/T is only1.06e-10 and |lambda_c| reaches6877: the system approaches
the boundary stiffly, even though it does not hit it at finite time.

There is no bounce or bounded-curvature claim. As t tends to infinity,
V tends toward zero, shear and auxiliary momentum grow without bound, and
the cap is approached asymptotically. This postpones the homogeneous volume
singularity to infinite proper time; it does not make every curvature bounded.
An inhomogeneous clock fold on a regular background is a different problem.

## 6. What now gets us closer to an action

The static scalar obstruction tested here is not triggered on the existing backgrounds.
The clock needs genuinely changed equations, not a zero-charge declaration.
The displayed candidate does that and has (a) an explicit volume-fold exclusion
condition, (b) a favorable restricted dispersive operator, and (c) an exact
nonlinear sector with finite-time continuation through the old collapse time.
It remains an OPEN candidate because the following cannot be inherited:

- General inhomogeneous evolution through the old clock-fold event, including
  P, lapse, shift, the rolling scalar and the cap auxiliary equation. In
  particular, rule out a finite-time cap/shear/lapse singularity.
- Full coupled perturbations and constraint rank on its actual cosmological
  and charged backgrounds. The frozen gravity/clock operator omits those terms.
- Its own matched galaxy backgrounds and gradient-bound test. The old24 solves
  omit cap forces and use the old switch, even though that switch is active
  on their radial profiles. Their successful bounds are not new-action evidence.
- Observations, causal/strong-coupling tests and a principle fixing free scales.
  b,T,xi,Lstar and the potential/branch choices remain premises.

This is a concrete action candidate with proved limited mechanisms and executed
falsification tests, not a claim that the complete action has been found.

## Sources and evidence boundaries

Babichev, arXiv:1602.00735v2 (14Feb2016), section1, official HTML read2026-11-05,
confirms the free1+1 canonical superposition as the baseline. Its planar
characteristic discussion is not a theorem of timelike preservation for the
coupled3+1 clock. The spherical witness here is derived directly from the
linear wave equation. https://arxiv.org/html/1602.00735v2

Mukohyama, arXiv:0906.5069v3 (16Aug2009), states the plane-symmetric vacuum
result for projectable Horava gravity with lambda!=1. Projectability and the
absence of matter differ from this local-lapse scalar/polarization action;
that result is inapplicable as proof of the proposed repair.
https://arxiv.org/html/0906.5069v3 . No full source text was retained and no
novelty claim is made for limiting-expansion constructions.

clock_math.py passes28/28 exact checks. Reversing the expansion sign fails6
(22/28), including the kinetic and frequency witnesses. The Bianchi test has
its own11/11 report. V2 manifests pin inputs, versions, bounds and outputs.
The analytic global-in-time Bianchi claim rests on the monotonic constraint
and finite-interval bounds above; six runs do not supply its proof.
