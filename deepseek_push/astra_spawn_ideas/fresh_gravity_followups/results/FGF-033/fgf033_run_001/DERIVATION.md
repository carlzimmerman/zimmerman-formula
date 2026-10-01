# FGF033: an autonomous global reference coordinate

2026-09-30. Conditional proof-only diagnostic extension. No stage18 root or
audit proof was read. Conservation, equilibrium and stability are separate
obligations. No universal potential or desired reference history is supplied.

## 1. Action and the explicitly added degree of freedom

On one fixed finite slab [0,D], per unit transverse area, keep C=4piG,
tau=K/c²>0, sigma=J/v_chi²>0 and the original fluid/phi/chi action with
fixed physical J,S0,K,v_chi. Add one spatially uniform dynamical coordinate
lambda(t), with

 a=a_c exp(chi+lambda),
 L_driver=I lambda_dot²/2-V(lambda), I>0 constant.       (1)

V is one fixed autonomous C2 function, with units energy/area.
I has units energy*time²/area. Its value and the function V are NEW model
inputs. Lambda and its global momentum constitute one additional canonical
pair. This is not a gauge coordinate, a local scalar field, a local covariant
stress sector or a derived element of the user's core framework.

The inherited local field Lagrangian is

 [tau phi_t²/2-W(g,a)+sigma chi_t²/2-J chi_x²/2-U(chi)]/C-rho phi,
 U=S0[cosh(2chi)-1]/4, g=|phi_x|.

Matter is the mass-conserving barotropic fluid. For the static Hessian below
use the earlier isothermal internal energy e''(rho)=cs²/rho with cs²>0.
Fix the original physical phi and chi boundary values in time and impose
impermeable fluid walls. No boundary work or mean-T subtraction is added.

For Q, g=F(B;a)=sqrt(B²+aB), b=F^(-1), W_g=b,
T=-a W_a>0 for g>0. Write A=b_g>0 and q=gA-B>0 on a positive-gradient
static patch; T_chi denotes the partial derivative at fixed g and fixed
lambda, equal to T_lambda and to 2T-gq. All later coefficients are evaluated
at an actual equilibrium, not at a proposed unsupported configuration.

## 2. Global equation and exact energy conservation

Variation of the full action with respect to lambda yields

 I lambda_ddot+V'(lambda)=(1/C) integral_0^D T dx.       (2)

The inherited local energy/flux identity is still

 partial_t E+partial_x S=-T lambda_dot/C,

 E=e_m+rho phi+
   [tau phi_t²/2+W+sigma chi_t²/2+J chi_x²/2+U]/C,
 S=(e_m+p+rho phi)v-[phi_t P+J chi_t chi_x]/C,

where e_m=rho v²/2+e(rho), p=rho e'-e, and P=b(g,a) phi_x/g.
In an evolving solution the MOND source is
P_x=C rho+tau phi_tt, not the static enclosed-source formula.

Multiplying (2) by lambda_dot gives

 d/dt[I lambda_dot²/2+V]=+(lambda_dot/C) integral T dx.

Thus the exact total energy is

 E_total=integral E dx+I lambda_dot²/2+V,
 dE_total/dt=-[S]_0^D=0                               (3)

under the specified fixed fields and impermeable walls. The driver cancels
the prescribed-reference exchange of FGF032. Different boundaries require
their actual flux; neither boundary flux nor coupling is silently removed.
This is global conservation in this autonomous diagnostic model, not proof
that total potential energy is bounded below or that a stable equilibrium
exists. The added global coordinate does not supply a local energy/stress
tensor or a physical metric coupling.

## 3. Static force balance and constant-potential obstruction

A genuine static equilibrium must satisfy the local hydrostatic/field
equations AND

 V'(lambda0)=(1/C) integral_0^D T(g0,a0)dx,             (4)
 a0(x)=a_c exp[chi0(x)+lambda0].

In a positive-gradient patch the local equations are
B0'=C rho0, cs²rho0'=-rho0 g0, and
-J chi0''+U'(chi0)=T(g0,a0).
Incoming constitutive flux and all wall values retain their original meaning.
These equations and (4) must hold simultaneously for the ONE chosen V.

If V is identically constant, its left side in (4) vanishes. Q has T>=0 and
T>0 wherever g0>0. A regular nonzero-field slab has a positive-measure region
with T>0, so its integral is strictly positive: no such static equilibrium
exists. At any instant with nonzero field, (2) instead gives lambda_ddot>0
for this constant V. This does not prove indefinite runaway if the fields
later change, but it rules out the proposed static nonzero-field state.

Even V'(lambda0)=0 at an isolated point cannot support that state. An arbitrary
fixed-lambda equilibrium from FGF030 is not automatically an equilibrium of
(1). We do not define V' separately for each desired state, reconstruct V
from an H trajectory, or select its curvature to assert a desired outcome.

## 4. Full second variation at an actual equilibrium

Assume an actual equilibrium satisfying (4), positive smooth rho0,A and
regular coefficients on the fixed interval. Set
u=(xi,psi,eta), delta rho=r=-(rho0 xi)', ell=delta lambda, where ell is
spatially uniform. The ORIGINAL boundary domain is

 u in X=H1_0(0,D)^3, ell in R.                         (5)

Total mass is fixed under these perturbations. As in FGF023,
e'(rho0)+phi0 is spatially constant, so the second-order density term
multiplying the first variation vanishes by the actual mass constraint.

Let d(x)=T_chi(g0,a0), m=U''(chi0)-d. The second variation of W is

 delta²W=A psi'²-2q psi'(eta+ell)-d(eta+ell)².          (6)

The local chi potential and gradient contribute U'' eta²+J eta'²;
lambda has no spatial gradient. Therefore the COMPLETE potential Hessian is

 Q_full[u,ell]=Q0[u]+2 ell L[u]+kappa ell²,             (7)

 Q0[u]=integral {cs² r²/rho0+2r psi
        +(A psi'²-2q eta psi'+J eta'²+m eta²)/C}dx,

 L[u]=-(1/C) integral[q psi'+d eta]dx,
 kappa=V''(lambda0)-(1/C) integral d dx.               (8)

There is no direct ell-r term: matter couples to phi, not directly to lambda.
Responsive matter is nevertheless included in Q0 and in its inverse below.
No U'' ell² or U'' eta*ell term belongs in original coordinates, because
the original U depends on chi alone, not on chi+lambda.

The quadratic kinetic form is

 2K2=integral[rho0 xi_dot²+(tau psi_dot²+sigma eta_dot²)/C]dx
                               +I ell_dot².          (9)

It is positive for the stated parameters. Neither positivity of I nor energy
conservation determines the sign of (7). All factors in L and kappa have
energy/area units, since ell is dimensionless.

## 5. Exact Schur criterion, including its functional gate

Use a positive fixed-lambda result ONLY if its action, actual background,
physical coefficients, fixed mass and domain (5) match. In particular assume
the symmetric polarization B0 of Q0 is bounded and coercive on X after
fixed positive reference-unit scalings:

 Q0[u]=B0(u,u)>=c0||u||_X², c0>0.

Mere pointwise strict positivity without this operator/domain control is not
the assumption. The reviewed FGF030 form can supply this gate for its
matching fixed-lambda background, but still cannot supply (4) for an arbitrary V.

L is a bounded functional on X. Let z in X be the unique weak solution

 B0(z,v)=L[v] for every v in X,
 S=L[z]=B0(z,z)>=0.                                   (10)

Then exact completion of the quadratic form gives

 Q_full[u,ell]=Q0[u+ell z]+(kappa-S)ell².              (11)

Accordingly:
- kappa>S is necessary and sufficient for a positive/coercive FULL form
  on X times R under the fixed-lambda coercivity assumption.
- kappa=S gives the nonzero null vector (u,ell)=(-z,1), including (0,1)
  when L=0. The linearized second-order dynamics permits neutral linear-time
  drift along this zero-restoring-force vector; nonlinear behavior is open.
- kappa<S gives an explicit admissible negative-energy direction (-z,1).
  There is exactly one negative potential direction in the inertia sense,
  because the only residual nonpositive block is one dimensional.

For smooth compact-domain coefficients the original regular differential
form, plus this finite-dimensional coupling, has the usual compact
mass-space embedding. Positive kinetic form (9) preserves the sign/inertia.
Thus under the stated form assumptions kappa>S yields a positive longitudinal
spectral gap, and kappa<S yields one negative squared-frequency mode.
No numerical gap or growth rate is supplied. I affects rates and kinetic
norms but not the static criterion kappa>S for any fixed finite I>0.

This criterion retains the ORIGINAL full Q0. No field has been minimized
by setting a completed local square to zero. If one computes z by static
field elimination, Dirichlet compatibility and its positive rank-one term
must remain; dropping it changes Q0^-1 and therefore changes S. The source
L includes q psi', whose boundary integral can be converted to -q' psi
only because psi has the declared zero traces.

## 6. Dynamical theta coordinates retain the global pair

Now theta=chi+lambda is a TIME-INDEPENDENT change of the extended
configuration coordinates (chi,lambda) -> (theta,lambda). Lambda is a
dynamical coordinate, unlike the prescribed function in FGF032. The exact
autonomous action becomes

 integral { [tau phi_t²/2-W(g,a_c exp theta)
    +sigma(theta_t-lambda_dot)²/2-J theta_x²/2
    -U(theta-lambda)]/C-rho phi+L_matter }dx
    +I lambda_dot²/2-V(lambda).                       (12)

Its momenta are

 pi_theta(x)=sigma(theta_t-lambda_dot)/C,
 Ptheta=integral pi_theta dx,
 p_lambda_new=I lambda_dot-Ptheta.                    (13)

The original driver momentum is p_lambda_old=I lambda_dot, so
p_lambda_new=p_lambda_old-Ptheta. This follows as well from the exact
canonical one-form identity
integral pi_chi dchi+p_lambda_old dlambda
 =integral pi_theta dtheta+p_lambda_new dlambda.

The full Hamiltonian is

 H=integral {e_m+rho phi+C pi_phi²/(2tau)+W/C
         +C pi_theta²/(2sigma)+J theta_x²/(2C)
         +U(theta-lambda)/C}dx
       +(p_lambda_new+Ptheta)²/(2I)+V(lambda).          (14)

It equals E_total, with no leftover lambda_dot Ptheta term. That term
appears in the field-only Legendre transform, but is canceled by the
global momentum contribution when lambda is dynamical. Applying the
prescribed-parameter energy relation to the combined system would double
count the coordinate effect.

The velocity quadratic form
integral sigma(theta_t-lambda_dot)²/C dx+I lambda_dot²
is strictly positive: zero forces lambda_dot=0 and then theta_t=0.
Its invertible map back to (chi_t,lambda_dot) preserves full kinetic rank.
For any finite positive field mass discretization the matrix Schur
complement of the theta block is exactly I, not zero; the continuum
bounded transform gives the same rank statement. No numerical discretization
is used here. There remains one additional GLOBAL canonical pair.

## 7. Coupled endpoint domain and global momentum flux

Original fixed chi walls transform to

 theta(0,t)-lambda(t)=chi_b0,
 theta(D,t)-lambda(t)=chi_bD.

Thus theta_t at BOTH walls equals lambda_dot. At perturbative level,
zeta=delta theta=eta+ell satisfies

 zeta(0)=zeta(D)=ell, zeta-ell in H1_0.                (15)

Imposing zeta=0 independently while also preserving eta=0 would force
ell=0 and discard the allowed driver mode by changing the boundary problem.
It is not a gauge reduction.

The second variation directly in these admissible theta variables is

 integral {cs²r²/rho0+2r psi+
   [A psi'²-2q zeta psi'-d zeta²+J zeta'²
                      +U''(zeta-ell)²]/C}dx+V''ell²,

with kinetic term
integral[rho0 xi_dot²+(tau psi_dot²
             +sigma(zeta_dot-ell_dot)²)/C]dx+I ell_dot².
Substitution zeta=eta+ell exactly reproduces (7)-(9).

A useful global momentum boundary check follows from the scale equation:

 Ptheta_dot=(1/C) integral(T-U')dx+(J/C)[theta_x]_0^D,

 p_lambda_new_dot=(1/C) integral U' dx-V'
                                  -(J/C)[theta_x]_0^D. (16)

Ignoring the endpoint relation in (15) and varying lambda at fixed independent
theta walls would miss this boundary contribution. The exact total energy
still has zero physical wall flux, because theta_t-lambda_dot=chi_t=0
there. Equations (13)-(16) preserve the global driver equation (2) and the
original boundary domain.

## 8. Controls and physical limit

- V constant: energy conservation holds but no static nonzero-field
  equilibrium exists. A mean-T subtraction would change (2), not solve it.
- Frozen ell=0 recovers the original Q0 and its local kinetic form.
- Formal L=0 limit gives the independent scalar test kappa>0; I>0 alone
  does not suffice.
- A positive bare kappa need not suffice when S>0. The elementary algebraic
  fixture Q0(x)=x², L(x)=x, kappa=1/2 gives
  Q_full=(x+ell)²-ell²/2 despite positive kinetic weights. This is a Schur
  control, not a claimed hydrostatic equilibrium or a tuned physical V.
- Missing -d ell² or -2d eta*ell terms violates the direct expansion (6).
- Replacing the shifted kinetic velocity by theta_t or fixing independent
  zero theta traces changes rank, energy or the domain; it is not equivalent.
- No prescribed H trajectory is selected by conservation or by solving a
  coordinate identity.

With a_c=9.3619e-11 as an anchor, constant lambda0=0 and
lambda0=log[(1.1279e-10)/a_c] represent the two registered reference choices.
Their separate frozen H reference shifts add log E(z), E²=.315(1+z)^3+.685.
Each candidate still must satisfy ONE chosen V's force balance (4); none
is an automatic autonomous equilibrium. An actual H trajectory would require
the coupled time-dependent equations, not just a frozen comparison.

Actual a=a_c exp(chi+lambda) still varies independently of a literal
constant-vacuum actual-scale identity. The global source is a diagnostic
addition with new inertia, potential and initial-data pair, not a derivation
of the core scale, required gravitational degree count or vacuum sector.
No RAR or registered M action, filtered-MONO, local covariant metric/photon,
observational, nonlinear/3D or theory-closure result follows.

The precise remaining task is an independently specified, physically justified
V and interpretation of this global sector, followed by actual simultaneous
equilibrium and Schur checks. Merely choosing V' and V'' to satisfy (4) and
(11) at a desired state would be parameter fitting, not the missing derivation.
