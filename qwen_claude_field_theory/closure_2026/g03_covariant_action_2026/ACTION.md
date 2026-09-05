# G03 candidate C-H: an explicit covariant clock/heat action

2026-09-04. **G03 OPEN.** This is one defined classical trial action for
T-B, the screened extension. It is not the strict T-A exponential AQUAL
target. Static matching below is at leading weak-field order on the stated
domain. Causality, physical mode count and full metric/clock variation are
not certified.

## Fields, constants and domain

Use signature (-+++), coordinates of length with x0=ct, and action in SI
units. G>0 has units m^3 kg^-1 s^-2; c has units m s^-1. Define
alpha=a0/c^2 (inverse length), with a0=9.3619e-11 or 1.1279e-10 m s^-2
in the inherited comparisons. xi>0 is one universal length and
b=xi^2/2 has units length squared. Lambda>=0 is a fixed cosmological
constant, not a field. Neither a0, xi nor Lambda is derived. The optional
relation a0=c^2 sqrt(Lambda/(32 pi)) is not imposed by the action.

The spacetime is a smooth Lorentzian slab with compact, closed, connected
spacelike leaves Sigma_tau, explicitly including T^3. Its only boundary
is the pair of initial/final leaves. There is no timelike spatial boundary
and no corner. The clock tau is a varied scalar of length dimension with
X=-g^{mu nu} partial_mu tau partial_nu tau>0. It defines

    n_mu = -partial_mu tau / sqrt(X),  N = X^(-1/2),
    h_mu nu = g_mu nu + n_mu n_nu,
    K_mu nu = h_mu^rho h_nu^sigma nabla_rho n_sigma,
    K = h^{mu nu} K_mu nu,
    a_mu = n^nu nabla_nu n_mu = D_mu ln N.

N is a covariant scalar after a clock labeling is chosen. The action is
invariant under smooth increasing relabelings tau -> f(tau); N changes
by a spatially constant factor. Calibrate the clock labeling on a specified
reference clock, so potential differences have a fixed normalization.
There is no fixed aether and no independent vector normalization multiplier:
n is constructed from the dynamical tau, and n^2=-1 identically. No clock
kinetic term is omitted: **the only clock terms are those displayed below**.
Whether their equations give healthy dynamics is an outstanding question.

Additional varied fields are U(x), dimensionless; W(z,x), dimensionless
for 0<=z<=b; L(z,x), of dimension length^-2; and lambda_0(x), also of
dimension length^-2. z is an auxiliary coordinate, not physical time.
W and L are spacetime scalars at each z. The metric g is the sole physical
metric for ordinary matter. The explicit matter example uses neutral
massive worldlines x_A and a Maxwell field A_mu; minimally coupled standard
matter may replace this example without introducing U or tau couplings.

This is an exact, spatially nonlocal **classical trial fundamental action**,
not a finite derivative EFT or a claim of a quantum UV completion. No
frequency or momentum cutoff is hidden. A later cutoff or derivative
truncation would define a different approximation and require a new gate.

## Intrinsic operator, measure and all endpoint terms

D is the Levi-Civita connection of each induced Riemannian metric h.
For a scalar F,

    Delta_h F = (1/sqrt(h)) partial_i(sqrt(h) h^{ij} partial_j F)
              = h^{mu nu} nabla_mu nabla_nu F + K n^mu partial_mu F.

The second equality includes the extrinsic-curvature term. For flat FLRW
the projected spacetime Hessian is a^-2 partial_i^2 F-3H F_dot; adding
K n(F)=3H F_dot gives the actual intrinsic Laplacian. Substituting the
projected Hessian alone changes the theory.

On each closed leaf take the self-adjoint nonpositive Laplace-Beltrami
operator in L^2(Sigma,sqrt(h)d^3x), with its H^2 domain and spectral heat
extension. If -Delta_h e_j=lambda_j e_j, the kernel is

    K_b(x,x') = sum_j exp(-b lambda_j) e_j(x) e_j(x')^*,
    S F(x) = integral sqrt(h(x')) d^3x' K_b(x,x') F(x').

The kernel is fixed by h and the closed topology; no Green-function or
homogeneous-solution choice is concealed. The constant mode has gain one.
On a flat torus it is the periodic image sum of the Gaussian of standard
deviation xi. The isolated R^3 limit and its fixed-mass infrared subtraction
are **not part of the domain proof here**. On a compact flat static leaf,
the source perturbation must have zero mean for its Poisson equation to
exist; positive mean density belongs to a time-dependent background.

Let s=y(1-exp(-y)), y>=0, and set

    q(s^2) = 2 s y - [y^2+2(1+y)exp(-y)-2] - s^2.

Use the unique nonnegative inverse, q(0)=0. For s>0,
q'(s^2)=nu(s)-1, nu(s)=y/s. The composite q(|p|^2) is C^1 at p=0,
but not C^2 there. Thus the first variation extends to zero gradient while
the regular linearized tangent does not.

With W_b=W(b,x), define the action completely by

    I = c^3/(16 pi G) integral_M d^4x sqrt(-g) {
          R - 2 Lambda
          + 2 h^{mu nu}(D_mu U-a_mu)(D_nu U-a_nu)
          + 2 alpha^2 q(h^{mu nu}D_mu W_b D_nu W_b / alpha^2)
          + integral_0^b dz L(z,x) [partial_z W(z,x)-Delta_h W(z,x)]
          + lambda_0(x)[W(0,x)-U(x)]
        }
        + c^3/(8 pi G) sum_caps integral d^3x sqrt(|gamma|) epsilon K_out
        - sum_A m_A c integral_A ds_A
        - (1/(4 mu_0 c)) integral_M d^4x sqrt(-g) F_mu nu F^{mu nu}.

Here F=dA, mu_0 is the electromagnetic vacuum permeability, ds_A is
positive proper length, gamma is the induced boundary metric,
epsilon=r_mu r^mu=-1 on the caps, and K_out=gamma^{mu nu}nabla_mu r_nu
uses the outward normal r. Consequently the final cap contributes -K
and the initial cap +K. These Gibbons-Hawking-York terms are exactly the
ones that convert the R action to

    integral sqrt(-g) [R^(3)+K_mu nu K^{mu nu}-K^2]

on this no-spatial-boundary domain. The sign follows from
R=R^(3)+K_mu nu K^{mu nu}-K^2+2 nabla_mu(n^mu K-a^mu).
There is no omitted S_aux or additional boundary action. Every summand in
the braces has dimension length^-2, including dz L partial_z W and
lambda_0(W_0-U). The prefactor then gives action units.

For the variational problem fix the induced metric and the embedding of
the temporal caps. Clamp tau and its first derivative there (or restrict
variations to the interior). The clock's variations and derivatives on
the caps vanish, so no additional clock surface variation survives.
Matter has the ordinary fixed endpoint/Dirichlet variational prescription.
W_0 and W_b are varied, not prescribed; L has no independently imposed
z-endpoint value. Temporal endpoint variations of the scalar fields may
be fixed without affecting the interior equations. There are no spatial
surface terms on a closed leaf. These are action-boundary conditions,
not a proved admissible Cauchy-data count.

## Auxiliary equations and what is actually eliminated

In adapted coordinates sqrt(-g)=N sqrt(h). Varying L and lambda_0 gives

    partial_z W = Delta_h W,   W_0=U,   W_b=S U.

Define f^i=(nu(|D W_b|/alpha)-1) D^i W_b. Integration by parts in z and
on the leaf gives the remaining auxiliary conditions

    partial_z L = -N^-1 Delta_h(N L),
    L_b = 4 N^-1 D_i(N f^i),
    lambda_0 = L_0,
    -4 N^-1 D_i[N(D^i U-a^i)] - lambda_0 = 0.

Thus L_0=S^dagger_N L_b, where

    S^dagger_N = N^-1 S N

is the adjoint for the action measure N sqrt(h), not generally S itself.
On a flat static weak-field background N=1 at the retained order, and
the outer adjoint becomes exactly the required S. The nonlinear curved
action must retain the N factors. The code checks this distinction and
the endpoint transport on nonconstant discrete metrics and lapses.

Solving W forward in z and L backward from its terminal condition supplies
no arbitrary diffusion-endpoint function. This establishes elimination as
a leafwise variational representation; **it does not prove the absence
of physical-time modes in the full clock/metric system**. The action has
the redundant U -> U+C(tau), W -> W+C(tau) freedom. Its constant leaf mode
can be fixed without solving an inverse Laplacian. No Poisson inverse is
used to define S.

The remaining initial data are the metric/clock data and matter data
subject to their actual constraints. Their independent number, the
allowed clock momentum and whether extra spatial integration data are
physical are unresolved; no guessed Dirac count is supplied. The scalar
diagnostic below makes that unresolved point concrete.

## Derivation of the weak static identification

Set tau=x0 on a stationary branch with shift zero and write independent
metric functions

    ds^2 = -exp(2 phi)(dx0)^2 + exp(-2 psi) delta_ij dx^i dx^j.

This is a reduction of the specified metric; U is still an independent
field. Define Psi=c^2 psi for the spatial metric potential. For K=0,
after integration by parts the Einstein-Hilbert spatial
term is exactly exp(phi-psi)[2|grad psi|^2-4 grad phi dot grad psi].
The acceleration square is 2 exp(phi-psi)|grad U-grad phi|^2.
Expand with phi,psi,U=O(c^-2), alpha=a0/c^2, fixed physical potentials
and xi, and Lambda negligible on the patch (or subtract its background).
The q term retains its full acceleration ratio. The leading density in
units c^3/(16 pi G), before any metric potential is eliminated, is

    2|grad psi|^2 - 4 grad phi dot grad psi
    + 2|grad U-grad phi|^2 + 2 alpha^2 q(|grad S U|^2/alpha^2).

Variation of psi gives Delta(psi-phi)=0. With the specified periodic
nonzero-mode conditions, psi=phi up to the fixed constant normalization.
Filter and constitutive stresses modify that statement beyond the leading
weak order; Phi=Psi is not claimed as an exact nonlinear identity.

The minimally coupled particle action expands as
integral dt [m v^2/2 - m c^2 phi - m c^2], deriving the physical potential
Phi=c^2 phi=c^2 ln N. Define u=c^2 U. Multiplying by dx0=c dt gives

    I_NR = integral dt d^3x { L_m,kin - rho Phi
             - [2 grad Phi dot grad u - |grad u|^2
                - a0^2 q(|grad S u|^2/a0^2)]/(8 pi G) }.

The metric variation therefore derives Delta u=4 pi G rho; U was not
named Newtonian by fiat. The U equation gives

    Delta Phi = 4 pi G rho + S* div[(nu(|grad S u|/a0)-1)grad S u].

Both filters and the unsmoothed Newtonian source are present. At xi=0 this
is T-Q for general sources, not T-A; T-Q and T-A share their spherical
law. Matter and photons see the same metric, but PPN gamma, preferred-frame
parameters and exact lensing equality require further derivation.

## Early variation and causal screen

For A=b Delta_h, the metric variation is
delta S=integral_0^1 exp((1-v)A) delta A exp(vA) dv.
The tests compare this Frechet derivative with direct metric differences
on curved periodic finite-volume leaves and differentiate both the
volume/gradient terms and the filter. Freezing S produces a resolved
error. These finite tests validate an implementation of this variation;
they do not supply the full covariant metric and clock equations.

Varying the normalized clock gives
delta_tau n_mu=-h_mu^nu partial_nu(delta tau)/sqrt(X). This must be
propagated through h, a, K and Delta_h, including the heat variation. It
has not yet been reduced into a complete clock equation. Diffeomorphism
invariance defines that equation unambiguously, but does not replace it.
The minimally coupled matter action separately obeys its usual
diffeomorphism identity, so on its matter equations nabla_mu T_m^{mu nu}=0.
No auxiliary matter force was inserted; the full gravitational off-shell
identity and its constraint implications are still to be checked.

An unconstrained scalar-wave attempt at the filter fails a precise early
causal test. For (partial_t^2-Delta) v=S rho in c=1 units on R^3,

    G_ret(t,r)=theta(t) t (2 pi xi^2)^(-3/2)
               exp[-(r^2+t^2)/(2xi^2)] sinh(rt/xi^2)/(rt/xi^2).

It is positive at every r>t>0. At xi=1,t=0.2,r=3 it is
0.000146723970701. This is a **FAIL for that scalar realization only**.
An elliptic lapse or the leaf heat kernel alone does not establish a
physical acausal signal in a constrained metric theory. The present
action requires its physical curvature response, including the shift
and all constraints, to decide whether such a channel survives.

There is a second concrete warning. Freeze a nonzero external constitutive
background, omit lower-derivative background stresses, and write
C(k)=exp(-xi^2 k^2)[A+B(khat.ehat)^2], A=nu-1, B=s nu'. The scalar ADM
principal block, with all three spatial fields independent, is

    L_2 = -6 psi_dot^2 + 4 k^2 beta psi_dot
          +2 k^2 psi^2 -4 k^2 phi psi
          +2 k^2(U-phi)^2 +2 k^2 C U^2
          -rho_s phi + j_s beta -t_s psi.

Source symbols here include the common 16 pi G/c^4 normalization;
j_s=rho_s_dot for a conserved source. U=phi/(1+C). The shift equation
is 4k^2 psi_dot+j_s=0. It integrates to

    psi=-rho_s/(4k^2)+F(k),   phi=F(k)(1+C)/C,
    phi+beta_dot=psi+3 psi_ddot/k^2-t_s/(4k^2),

for k!=0 and C!=0. The physical Bardeen combination cancels the explicit
lapse dependence. In this truncated block, the modified static branch
therefore depends on a spatial integration function F; it is not selected
by the instantaneous source. Zero initial F does not dynamically generate
the advertised static MOND lapse. This is an exact algebraic obstruction
to declaring that **truncated block** a complete adiabatic MOND response.
It is not a proof against the full action: background stresses, scalar/
tensor mixing, the clock equation and consistency of the background must
be restored, especially before an omega->0 limit. C=0 directions are
exceptional constraints and must be treated without division.

Restoring tau=x0+pi with the metric frozen gives a related diagnostic:
the gradient/acceleration square plus q tangent, after eliminating U,
has coefficient 2k^2 C/(1+C) for pi_dot^2 and no displayed restoring
term. This coefficient changes sign with wavevector orientation at the
two inherited backgrounds. This is a **decoupling warning**, not a ghost
proof before metric mixing and constraints are reduced. It cannot be
used to assign a physical DOF count.

The next unavoidable calculation is the constrained retarded response of
the full metric/clock equations on an actual nonzero-background solution,
keeping the heat-kernel stress. Determine whether F is constrained,
physical frozen data, or an inadmissible branch and whether measurable
R_0i0j has spacelike response. Resolve this before a large Dirac or PPN
calculation. k=0, C=0 and y=0 need their own equations, not continuation
through the divided formulas.
