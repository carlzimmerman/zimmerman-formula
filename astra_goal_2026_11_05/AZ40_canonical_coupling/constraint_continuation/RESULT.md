# Clock momentum survives; the static obstruction needs an on-shell gradient test

The complete healthy action is still open. Two missing implications now have
explicit answers. First, gravity does not force the independent clock's finite-k
momentum to vanish on the branch calculated below. Second, the earlier frozen
negative-energy coefficient includes an off-shell scalar force. On a static
solution that contribution becomes a gradient term, giving a useful sufficient
positivity bound instead of a universal large-s no-go. Neither result removes
AC1's exact nonlinear clock-caustic branch. Kappa=1/2 remains FITTED.

Base6a6a3a23a75e5f55dff4d9fcdf53b948b084dab7; scope frozen bddd5251c2.
This extends AZ40, while preserving the separate AC1/AC2/AC3 results. No action
is adopted. Equations below are internal derivations, with exact checks36/36.
Review provenance: author self-review, not independent review.

## 1. Exact FRW scalar constraints, with the independent clock retained

Take the canonical potential portal X-V(phi), a0(phi)^2=xi*G*V(phi), and the
independent tau of AZC1's action skeleton. Here M=Mpl, K=4piG=1/(2M^2),
Q=sqrt(-grad(tau)^2), n=-d tau/Q. Use the exact background

    ds^2=-dt^2+R(t)^2 dx^2, tau=t, P=0, phi=phi_bar(t),
    v=phi_bar_dot, 3M^2 H^2=v^2/2+V,
    Hdot=-v^2/(2M^2), vdot=-3Hv-V_phi.

There is no additional dust or other matter in this calculation. Set Lstar=0.
This restriction matters: [max(D.P,0)]^2 has no ordinary bilinear second
variation at D.P=0. One cannot simply import a Fourier stiffness kernel at
this background while claiming to have varied that switched action.
Keep mu_K>=0. The clock norm term and polarization have zero background
stress and zero first variations, so this scalar-only branch is on shell.
H!=0 and a nonzero comoving Fourier wave number are assumed throughout.

Use flat spatial gauge h_ij=R^2 delta_ij, N=1+alpha, N_i=partial_i B_shift,
q=delta phi, sigma=delta tau, and k=k_com/R. Gauge fixing the spatial
curvature fixes the scalar time diffeomorphism for H!=0; sigma is retained.
The linear acceleration and norm are

    delta A_i=partial_i(alpha-sigma_dot),
    delta Q=sigma_dot-alpha.

The H-dependent connection terms cancel in delta A_i. They must not be
replaced by a static-clock assumption. At P=0,

    W=K P^2/2+O(|P|^3/a0).

Thus the scalar dependence of a0 first enters at cubic order here. In one
real longitudinal Fourier quadrature, eliminating P gives

    k P(alpha-sigma_dot)-K P^2/2
      -> k^2(alpha-sigma_dot)^2/(2K).

Adding the norm penalty supplies mu_K^2(alpha-sigma_dot)^2/(2K).
This is a positive induced kinetic term, not a condition setting it to zero.

Before lapse and shift elimination, the canonical Einstein/scalar quadratic
Lagrangian divided by R^3 is

    qdot^2/2-v alpha qdot+(v^2/2-3M^2H^2)alpha^2
    -V_phi alpha q-(k^2+V_phiphi)q^2/2
    +k^2 B_shift(2M^2 H alpha-v q).

The induced polarization/norm square has no shift. Hence

    alpha=b q,                 b=v/(2M^2 H).

The lapse equation determines B_shift. In particular the (alpha,B_shift)
constraint Jacobian has determinant -4M^4 H^2 k^4, independently of the
coefficient of the induced square. It is invertible in the stated domain;
it supplies no additional equation setting sigma's momentum to zero.

Integrating -v*b*q*qdot by parts WITH the evolving R^3 measure gives

    S2 = integral dt R^3 {
           qdot^2/2-(k^2+m_Q^2)q^2/2
           +C_k(sigma_dot-b q)^2/2 },
    C_k=2M^2(k^2+mu_K^2)>0,
    m_Q^2=V_phiphi-(1/(R^3 M^2))*d/dt(R^3 v^2/H).

The velocity Hessian is R^3 diag(1,C_k), of rank two. These are two scalar
configuration degrees of freedom in this quadratic sector after both scalar
coordinate gauges and the two metric constraints are accounted for. This is
not a nonlinear all-background Dirac count. k=0,H=0 and switched stiffness
are outside the rank statement. At k=0,mu_K=0 the clock term degenerates.

Since sigma is cyclic in THIS linearized action,

    j_k=R^3 C_k(sigma_dot-b q),       j_k_dot=0.

It can take arbitrary small nonzero values. At fixed j_k the Routhian is

    R_j=R^3[qdot^2/2-(k^2+m_Q^2)q^2/2]
          -b j_k q-j_k^2/(2R^3 C_k),

and consequently

    qddot+3H qdot+(k^2+m_Q^2)q=-b j_k/R^3,
    sigma_dot=b q+j_k/(R^3 C_k).

Zero j_k is a consistent linear initial-data sector on this branch, but it
is not a metric constraint or a property of every perturbation. Conversely,
nonzero j_k alone is not evidence of instability; its evolution is explicit.

## 2. Local mode momentum is not the total Noether charge

This distinction prevents another proposed shortcut. For the mu_K=0 action,
tau enters only through its normalized gradient n and derivatives of n.
Let E_mu denote the covariant Euler derivative with respect to n^mu, including
the P orthogonality multiplier, before restricting n to a normalized gradient.
Holding g,P,phi fixed, direct differentiation gives

    delta n^mu=-(h^{mu nu}/Q)*partial_nu(delta tau),
    delta Q=n^nu partial_nu(delta tau).

Writing F(Q)=mu_K^2(Q-1)^2/(2K), the actual tau equation is

    nabla_nu J^nu=0,
    J^nu=h^{mu nu} E_mu/Q-F_Q n^nu.

For mu_K=0 this representative J is tangent to the tau leaves. That does
NOT imply the clock has no evolution or that E_mu=0: E contains derivatives
of P and the metric, and only its projected divergence is constrained.
In the flat-gauge quadratic calculation, integrating the P term spatially
gives sigma_dot*div_phys(P). The canonical momentum density is therefore

    j(x)=R^3[div_phys(P)+(mu_K^2/K)(sigma_dot-alpha)].

At mu_K=0 its spatial integral vanishes with periodic or decaying boundary
conditions. Still, j(x)=j0*cos(k_com*x) is nonzero and has zero spatial mean.
Its finite-k amplitudes are exactly the j_k above. Improvements of a Noether
current can move this spatial-divergence contribution between its components;
they do not eliminate the local canonical initial data. Equating zero TOTAL
clock charge with j_k=0 for every mode would be an invalid inference.

## 3. Evolving-background continuation: the charge need not grow physically

For an exact scalar-only exponential potential V=V0 exp(-lambda phi/M),
0<lambda^2<6, the scaling solution has

    epsilon=lambda^2/2, R proportional to t^p, p=1/epsilon,
    v=lambda M H, b=lambda/(2M), m_Q^2=0.

This is an exact model and the late exponential limit of the sinh potential,
not the finite-y scalar/dust solution. The scalar equation is

    qddot+3H qdot+(k_com^2/R^2)q=-b j_k/R^3.

In conformal time, with u=R*q, it becomes exactly

    u''+[k_com^2-R''/R]u=-b j_k.

Thus a nonzero clock momentum is a definite source, not an arbitrary extra
mass guessed from a frozen frequency plot. At mu_K=0 its direct contribution
to sigma_dot is j_k/(2M^2 k_com^2 R). The mode normalization requires finite
k_com; this expression is not a homogeneous k_com=0 limit.

On the accelerating branch p>1, k_com/(R H) tends to zero. With R=t^p in
fixed time units, the leading long-wavelength solutions are

    q_h = constant, t^(1-3p),
    q_j = -b j_k t^(2-3p)/(2-3p).

These solve the leading equation with the gradient term omitted. They are
not exact finite-k solutions. Gradient corrections are asymptotically
subleading since k^2/H^2 tends to zero. The charge-driven term decays. The
constant scalar mode induces sigma proportional to t, but its physical clock
tilt |grad_com sigma|/R scales as t^(1-p) and decays. The direct charge
contribution to sigma integrates t^(-p), approaching a constant for p>1.
These linear asymptotics do not prove nonlinear regularity or remove AC1's
finite-amplitude, smooth-initial-data caustic counterexample.

The instantaneous Hamiltonian in these particular variables is

    H2=p_q^2/(2R^3)+R^3(k^2+m_Q^2)q^2/2
          +b j_k q+j_k^2/(2R^3 C_k).

For mu_K=0 on the exponential solution, its q/charge Schur coefficient is
k^2(1-epsilon). It is positive during acceleration. It is not a conserved
cosmological energy: coefficients and the boundary transformation used above
are time dependent. No instability conclusion is drawn just from its sign
on a decelerating branch or for mu_K!=0.

## 4. Static energy: identify the force term before diagnosing a background

This section returns to K=4piG=1 and the static Newtonian reduction. It is
not the full relativistic stress/constraint energy. Put a=a(phi)>0,
V=Cpot*a^2 with Cpot=1/(xi G)>0, and p=|P| in 0<p<a. Let Pi_L be the
orthogonal longitudinal projector with the specified fixed-source boundary
conditions. Eliminating the Newtonian lapse gives, up to a source constant,

    E=integral [|grad phi|^2/2+V+W(P,a)-P.g_b]
        -||Pi_L P||^2/2+E_stiffness,
    W=a[-p-a log(1-p/a)].

Here g_b is fixed, curl-free, and E_stiffness, when included, has a
nonnegative second variation and no phi dependence in this static reduction.
One may set it to zero. Scalar stress corrections to the gravitational
constraint, relativistic geometry, moving clocks and sources are excluded.

Use ||Pi_L P||^2=||P||^2-||Pi_T P||^2 and define the local function

    U(p,a)=Cpot*a^2+W(p,a)-p^2/2, s=p/(a-p)>0,
    h(s)=s+s/(1+s)-2log(1+s),
    J(s)=2log(1+s)-4s/(s+2).

Direct derivatives at fixed p, followed by substitution p=a*s/(1+s), give

    U_pp=s(s+2)>0, U_pa=-s^2,
    U_aa=2Cpot+s^2-2s+2log(1+s),
    U_a=a[2Cpot-h(s)],
    U_aa-U_pa^2/U_pp=2Cpot+J(s)>0.

The uniform sign follows from J(0)=0 and
J'(s)=2s^2/[(1+s)(s+2)^2]>0. The transverse P curvature is s>0.
This extends AZC1's convexity calculation by retaining the canonical scalar's
nonlinear field map a(phi), not assuming a is linear in phi.

With a1=a_phi, a2=a_phiphi, the zero-wave-number scalar Schur curvature is

    M_static=a1^2[2Cpot+J(s)]+a2*a[2Cpot-h(s)].

The last term is precisely a2*U_a. This is the origin of the earlier
large-s limit M_static/s -> -a*a2. It is a curvature on an arbitrary frozen
configuration; if U_a!=0, a constant scalar there does NOT solve its static
field equation. This does not invalidate the earlier algebra. It limits the
inference one can draw from it about physical solutions.

A uniform stationary toy configuration instead satisfies h(s*)=2Cpot.
Since h(0)=0, h'=s^2/(1+s)^2>0 and h tends to infinity, there is exactly
one s*>0. For a constant fixed source field g_b>0 aligned with P, the P
equation is g_b=a*s*^2/(1+s*). The stationary scale is therefore

    a=g_b*(1+s*)/s*^2.

At this solution M_static=a1^2[2Cpot+J(s*)]>0. In the corresponding frozen
parallel static block, adding k^2 and nonnegative polarization stiffness
preserves this sign. This is a stationary solution of the stated Newtonian
toy reduction, not a cosmological matching solution or a galaxy prediction.
As in AC1's fixed-acceleration ensemble, a is source-dependent here.

## 5. An on-shell sufficient bound for spatially varying static backgrounds

Suppose the static background is smooth and solves

    Delta phi=a1*U_a,

with a1 nonzero of fixed sign. Take q=delta phi vanishing at the boundary
(or compactly supported), and admissible P perturbations with the same
projector boundary conditions. Set f=|a1|>0. Completing the radial P square
and using its positive transverse curvature gives

    delta^2 E >= integral {
       |grad q|^2+[a1^2(2Cpot+J)+(a2/a1)Delta phi]q^2 }.

The discarded pieces are the radial completed square, s|delta P_perp|^2,
||Pi_T delta P||^2 and any nonnegative stiffness second variation. There
is no discarded negative gravitational projector contribution.

Integration by parts gives the exact identity

    integral [|grad q|^2+(a2/a1)Delta phi*q^2]
      = integral { f^2 |grad(q/f)|^2
                    -(a3/a1)|grad phi|^2*q^2 },
    a3=a_phiphiphi.

Consequently a sufficient on-shell static energy condition is

    B(x)=a1^2[2Cpot+J(s)]-(a3/a1)|grad phi|^2 >= 0

pointwise. Then delta^2 E>=0 in the stated perturbation/boundary class.
Strictness/coercivity needs the corresponding positive lower bounds and
boundary assumptions; no uniform bound at p=0 or a1=0 is claimed.
This is sufficient, not necessary: violating B>=0 does not prove a negative
mode, because the positive derivative and P-square terms may still dominate.

For the actual sinh portal a=a_star*sinh(y)^(-n), y=(phi-phi_star)/B0>0,
n=(1-beta)/beta>0,

    a3/a1=[n^2 coth(y)^2+(3n+2)csch(y)^2]/B0^2 > 0.

Thus the unresolved static obstruction can be tested through an explicit
scalar-gradient bound. There is no remaining universal negative term linear
in s in this on-shell lower bound. J grows only logarithmically and is positive;
one must solve for gradients rather than infer them from the frozen value of s.
A linear portal a(phi) has a3=0 and automatically meets this static sufficient
condition, but changes the cosmological construction; this is not adoption of
that alternative or a proof of its acceleration history.

## 6. Evidence, source check, and what remains

verify.py independently expands the quadratic ADM expression, eliminates its
constraints, reconstructs the scalar mass with evolving measure, checks the
Legendre/Routh transforms, the exact exponential/conformal equations, derives
the static Hessian from W, and checks the factorization including its boundary
term. Main36/36. Reversing the induced clock kinetic sign fails4 checks
(32/36). Omitting the on-shell gradient remainder fails2 (34/36). Mutants are
expected nonzero exits, retained separately, not failed mathematical claims.
Each run takes about one second and has a v2 input/output-hash manifest.

A primary-source cross-check of the unmodified Einstein/scalar ADM starting
point used Maldacena, astro-ph/0210603v5 (6 May2005), section2, official HTML
read2026-11-05: https://arxiv.org/html/astro-ph/0210603v5 . The dictionary is
exp(rho)=R, rho_dot=H, and its Mpl=1 is restored as M here. The displayed ADM
and background equations agree. This verifies that limited starting point;
the source has no independent tau/P sector and proves none of the new clock
or static-energy claims. No full text was retained; no novelty claim is made.

Remaining dependencies are concrete:

1. The FRW rank result excludes switched stiffness and nonzero background P.
   Derive the charged-background constraint operator before carrying its rank
   or j_k conservation into a galaxy.
2. The static bound is now explicit. Evaluate it on solutions of the stated
   Newtonian equations, then add the omitted relativistic/time-dependent
   constraints. A favorable static bound is not a dynamical spectrum.
3. Independent-clock caustics are still an exact counterexample to unrestricted
   smooth-clock regularity. Choosing j_k=0 in a linear calculation does not
   erase those finite-amplitude data. A regularity mechanism or a changed action,
   such as the separately defined single-clock candidate, is still required.
4. xi remains free. None of these manipulations derives kappa=1/2.

These are partial mathematical results toward the action, not closure of it.

## 7. Applicability checks after the derivation

SWITCHED_CLOCK.md supplies a separate finite-Galerkin convexity proof with
gamma>=0 and the actual positive-part stiffness. Its positive conjugate
kinetic functional retains freely specifiable nonzero clock momentum. It is
not an ordinary Fourier Hessian and is not a continuum regularity theorem.
This removes the proposed finite-regulator zero-charge shortcut without
pretending the switch is differentiable to second order at P=0.

The existing AC1 radial backgrounds have a frozen cosmological scalar-force
subtraction. Their equation is of the form

    Delta phi=U_phi-J_background,

not Delta phi=U_phi. The section5 bound therefore does not transfer unchanged.
For a field-independent prescribed J_background, the corresponding energy
contains -J_background*phi. Its second derivative is zero, but substitution
of the background equation changes the sufficient bound to

    B_J=a1^2(2Cpot+J(s))+(a2/a1)J_background
                                -(a3/a1)|grad phi|^2.

For decreasing sinh a(phi), a1<0,a2>0, and the canonical background source
V_phi(phi_infinity)<0, this extra term is positive. In dimensionless AC1
variables psi=epsilon*d, with scalar gradient energy |grad psi|^2/(2epsilon),
the mass bound for the canonically normalized variation is

    epsilon*[A_psi^2(2Cpot+J)+(A_psipsi/A_psi)J_background]
       -(A_psipsipsi/A_psi)*epsilon^2|grad d|^2,
    Cpot=4pi/xi, J_background=Cpot*(A^2)_psi at psi=0.

This follows by the same integration-by-parts identity. It has not been
numerically evaluated here; the existing 24 converged radial profiles and
positive finite-element spectra are not claimed as tests of this new bound.
A sampled positive bound would still need interval/control-of-interpolation
work before being called a uniform analytic certificate on a numerical BVP.

## 8. The nonlinear zero-current counterexample remains

The current formula in section2 gives a direct corollary of AC1's exact branch.
For P=0,Q=1,A=0 and lambda_P=0, every n-dependent first variation vanishes:
E_mu=0 and F_Q=0. Hence J^mu=0 pointwise, not merely after spatial integration.
Nevertheless the clock can focus. In a regular flat FRW metric, label planar
unit-clock geodesics by x(t0)=r and choose their conserved spatial momentum
p(r)=-lambda_c*r*exp(-r^2/L^2), lambda_c>0. At the central trajectory the exact
characteristic Jacobian is

    partial x/partial r at r=0
      =1-lambda_c*integral[t0,t] dt/R(t)^2.

For any finite regular interval t0<t1 that integral is positive. Choosing
lambda_c larger than its reciprocal forces a crossing before t1. Initial
unit-gradient tau data are smooth; scalar, metric and dust (if included in
this exact background branch) remain regular. The argument uses the original
normalization-preserving geodesic characteristics, not a linear extrapolation.
See AC1_canonical_portal/EXACT_CLOCK_OBSTRUCTION.md for the full construction.

Thus even imposing the stronger pointwise zero covariant current cannot by
itself guarantee a globally smooth independent clock. This is a new logical
connection to the AZ40 proposed zero-charge escape, not a new caustic example.
It does not prove that every chosen physical cosmological clock crosses or
that weak continuation is impossible. It does prove that zero charge alone
is not the missing regularity mechanism for this action class.
