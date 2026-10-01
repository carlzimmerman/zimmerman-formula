# Fixed-mass, fixed-wall local response in the diagnostic Q model

Root worked out this argument before receiving an author route preview, but
the preview arrived before this file was saved. That chronology limits any
claim of complete informational isolation. No new worker proof or stage20
auditor file was read. A separate agent audits this root proof independently.
This is a local conditional theorem, not a physical potential construction.

## Hypotheses and the actual constrained variables

Fix physical interval [0,d], mass per area M>0, both endpoint values of phi
and chi, positive C=4piG, J, cs², a_c and inherited scale potential U(chi).
The reference parameter lambda is frozen for each local equilibrium, and
actual scale a=a_c exp(chi+lambda). The full action is the inherited diagnostic
Q action, with b(g,a)=(sqrt(a²+4g²)-a)/2, W_g=b, T=-a W_a and g=phi'>0.
Kinetic parameters remain fixed but do not enter this static response problem.

Assume one classical equilibrium at lambda0 with phi0,chi0 sufficiently smooth
(e.g. C3), uniformly positive rho0 and g0 on the closed finite interval, and
the reviewed full quadratic form Q0 continuous, symmetric and coercive on
H1_0(0,d)^3 in fixed reference units. The original local field equations are

 (b(phi',a))'=C rho,
 -J chi''+U'(chi)-T(phi',a)=0,
 cs² rho'=-rho phi'.

These use MOND constitutive flux, not Newtonian phi''=C rho. M and all wall
values are fixed as lambda changes. No equation V'=integral T/C is required
for this local branch; an autonomous-driver equilibrium is an additional
intersection considered only at the end.

## Eliminate density with its mass constraint intact

Hydrostatic balance gives cs² log rho+phi=constant. The only normalized
positive solution with mass M is

 rho_phi(x)=M exp(-phi(x)/cs²)/Z(phi),
 Z(phi)=integral_0^d exp(-phi(y)/cs²)dy.

For phi variation psi, writing <psi>_rho=M^-1 integral rho psi,

 r_psi=D rho_phi[psi]=-rho(psi-<psi>_rho)/cs²,
 integral r_psi=0.                                            (1)

The normalization derivative is essential; freezing it changes the problem.
For a regular fixed rho, the map from material displacement to density change
is an isomorphism H1_0 -> L2_0 (zero-integral L2 functions):

 r=-(rho xi)', xi(x)=-rho(x)^-1 integral_0^x r(y)dy.              (2)

Both traces vanish exactly because integral r=0. Uniform positivity and bounded
rho,rho' give bounded maps in both directions. This is a linear tangent-space
identification, not a claim that an H1 displacement by itself defines a
nonlinear positive-density diffeomorphism. The actual nonlinear branch uses
rho_phi, which is manifestly positive and normalized.

## Nonlinear map on an open positive-gradient set

Write phi=phi0+psi, chi=chi0+eta with Y=(H2 cap H1_0)^2 in fixed units.
In one dimension H2 embeds continuously in C1. Thus g>0 is open near the
uniformly positive g0, and rho_phi stays positive; exp and the nonzero Z are
smooth maps on the bounded neighborhood. Define F:Y times R -> L2^2 by

 F1=(-[b(phi',a)]'+C rho_phi)/C,
 F2=(-J chi''+U'(chi)-T(phi',a))/C.                             (3)

The source function and its coefficients are smooth for g>0,a>0. In 1D,
H1 is closed under multiplication with its norm estimate; phi' is H1 and
chi is H2. Writing the first derivative in (3) as
b_g phi''+b_chi chi' shows that (3) is continuously differentiable H2->L2
on this open set. Its derivative is continuous in operator norm; it is not
being asserted on all of H1, where positivity of phi' would not be open.

At the seed let A=b_g>0, q=gA-b, S=T_chi=2T-gq, m=U''-S. The derivative D is

 D1(psi,eta)=-[A psi'-q eta]'/C+r_psi,
 D2(psi,eta)=(-J eta''+m eta-q psi')/C.                         (4)

Its weak polarization B_red is symmetric. Its quadratic form is

 Q_red[psi,eta]=integral[A psi'²-2q eta psi'+J eta'²+m eta²]/C
                  - integral rho(psi-<psi>_rho)²/cs².          (5)

For every zero-integral r, completing the density square gives

 integral(cs²r²/rho+2r psi)
   =integral cs²(r-r_psi)²/rho
                  -integral rho(psi-<psi>_rho)²/cs².

Using (2), this is the exact minimization of full Q0 over the fluid tangent
variable, retaining both field Dirichlet domains. Full Q0 coercivity implies
Q_red coercivity on (H1_0)^2: substitute its minimizing density/displacement
into the full inequality and retain the field norms. This is static density
elimination for an equilibrium derivative, not removal of matter kinetics or
a dynamical mode. No Dirichlet field compatibility term is discarded.

## Actual inverse and a local branch

A continuous symmetric coercive B_red defines an equivalent complete inner
product on (H1_0)^2. Every L2 right side defines a continuous functional;
representing it in this inner product gives a unique weak H1_0 solution of
D y=f and an H1 bound. It is also H2: the second equation (4) expresses
eta'' as an L2 function. The first says (A psi'-q eta)' is L2. Thus the
flux A psi'-q eta is H1; because A is uniformly positive with bounded smooth
coefficients, psi'=(flux+q eta)/A is H1. This supplies the H2 estimate from
the H1 estimate and f, not just formal ellipticity. Conversely D maps Y
boundedly into L2^2. It is therefore a bounded isomorphism Y -> L2^2.

For completeness, take the seed inverse D0^-1 and iterate

 y_(n+1)=y_n-D0^-1 F(y_n,lambda).

At (0,lambda0) the derivative of this update in y vanishes. Continuity of
DF makes its norm less than1/2 on a small Y-ball and parameter interval.
Continuity of F(0,lambda), with F(0,lambda0)=0, makes the update map a
possibly smaller closed ball to itself. Iteration converges geometrically
to a unique local fixed point. Differences of the equation at neighboring
parameters and the nearby uniformly invertible derivative yield

 y_lambda=-(D_y F)^-1 partial_lambda F.

The continuous derivatives make this a C1 local branch in H2. Its density
is the normalized rho_phi, so mass and both wall traces are exactly fixed.
The C1 embedding preserves g>0 after shrinking the interval. Coefficients
and full quadratic forms vary continuously, so seed coercivity persists
on a possibly smaller local interval in the SAME fixed reference norms.
No explicit parameter radius, global continuation, or uniqueness outside
this neighborhood is proved.

## Susceptibility and the full autonomous restoring margin

At any point of this local branch, put u_lambda=(xi_lambda,psi_lambda,eta_lambda)
with r_lambda from (1) and xi_lambda from (2). Define the full bilinear form
a0 from Q0 and the linear functional

 ell[v]=-integral(q v_phi'+S v_chi)/C.

The weak parameter derivative of F is ell on the two field tests, since
b_lambda=-q and T_lambda=S. The density derivative solves the minimization
condition for every zero-integral density test. Combining those three tests
in the unreduced full form gives

 a0(u_lambda,v)=-ell[v] for every v in H1_0^3.

If z represents ell, a0(z,v)=ell[v], uniqueness implies u_lambda=-z.
Let beta=Q0[z]=ell[z]>=0. For R(lambda)=integral T(phi_lambda',a_lambda)/C,

 R'=integral[q psi_lambda'+S(eta_lambda+1)]/C
   =integral S/C-ell[u_lambda]
   =integral S/C+beta.                                       (6)

All derivatives refer to fixed mass, interval, physical coefficients and
original phi/chi wall values. Formula (6) does not give a sign for R'
without information on S and beta. At an actual autonomous equilibrium
V'(lambda*)=R(lambda*) for one independently specified V, the FGF033 margin is

 Delta=V''(lambda*)-integral S/C-beta=V''(lambda*)-R'(lambda*).

This relates the dynamical quadratic-form test to the constrained response
curve. It neither selects V nor creates its intersection; it does not prove
a fold or nonlinear stability when Delta=0.

## Why the old left-IVP derivative is not this response

For a more general family allowing M to vary, density differentiation adds
(rho/M) M_lambda to (1). The integrated density change is M_lambda, so (2)
cannot give a displacement vanishing at both walls unless M_lambda=0.
If endpoint values also vary, psi_lambda and eta_lambda have their actual
nonzero traces. They are not in the homogeneous form domain. Even with fixed
mass, a trace lifting w_b gives u_lambda=w_b+v with v in H1_0^3, and the weak
response equation becomes a0(v,t)=-ell[t]-a0(w_b,t). Hence v is generally
not -z. With changing mass one must additionally represent the nonzero-mass
tangent forcing. These are different equations, not negligible corrections.

The corresponding first derivative of the static energy makes boundary and
mass terms explicit. On equilibrium, for the density/field energy with rho phi
interaction and e''=cs²/rho, define chemical multiplier mu_c=e'(rho)+phi,
constant in space. For any differentiable equilibrium family on fixed [0,d],

 dE_stat/dlambda=-R+mu_c M_lambda
             +[b phi_lambda+J chi' chi_lambda]_0^d/C.          (7)

Bulk field variations vanish by their equations. Equation (7) exhibits the
terms missing if the old IVP family with moving mass/right-wall values is
mistaken for the constrained branch. R' always has its direct chain-rule
expression, but reduction to (6) needs the fixed constraints. No zero extra
term is assumed merely because all members individually satisfy equilibrium.

## Scope

The seed hypotheses are nonempty in the earlier short-slab diagnostic family,
but a selected seed has its own mass and endpoint data. This proof does not
connect two such seeds by one common fixed-wall/mass path, and does not show
that a neighborhood reaches the alternative a0 or a distant frozen H value.
Both a0=9.3619e-11 and1.1279e-10 m/s² remain separate hypotheses; constant
vacuum, frozen H reference and actual H trajectory remain distinct. Actual
scale a=a_c exp(chi+lambda) remains a diagnostic extension of the core.
No RAR/M action, filtered-MONO transfer, metric/photon coupling, local covariant
reservoir, physical V or observed source discrepancy is supplied. No numerical
computation or historical novelty/full-theory closure is claimed.
