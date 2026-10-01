# Autonomous global reference: energy, equilibrium and one extra stability condition

Root derivation fixed before reading new FGF033 worker or audit proofs.
This is an explicitly added diagnostic degree of freedom, not an adopted
vacuum mechanism or a local covariant completion of the user's framework.

## Model and total energy

Use the inherited Q fluid/phi/chi action on a fixed interval [0,d] per unit
transverse area, with C=4 pi G, tau=K/c²>0, sigma=J/v_chi²>0 and J>0.
Keep its original time-independent field Dirichlet walls and impermeable
matter walls. Replace the prescribed reference protocol by a dynamical real
coordinate lambda(t), spatially uniform, and add

    L_driver=I lambda_dot²/2-V(lambda),       I>0, V in C².

I is energy times time² per area; V is energy per area. No spatial density
or metric stress for this global coordinate is thereby specified. The field
scale is a=a_c exp(chi+lambda), with fixed positive a_c. All inherited
couplings and physical units stay fixed. V and I are new assumptions.

Variation in lambda uses partial_lambda L_field=+T/C, where
T=-a W_a and W(g,a)=integral_0^g b(v,a)dv, b the Q inverse. Thus

    I lambda_ddot+V'(lambda)=integral_0^d T/C dx.                  (1)

The original matter-plus-field energy obeys dE_fields/dt=-[F]_0^d
-lambda_dot integral T/C. The driver energy I lambda_dot²/2+V has
derivative +lambda_dot integral T/C by (1). Therefore

    dE_total/dt=-[F]_0^d=0                                     (2)

under the stated closed physical walls. Equation (2) is global conservation
of the specified autonomous action. It is not a constructed local covariant
energy-stress tensor; the original local field balance still has its exchange.
The dynamic MOND source remains B_x=C rho+tau phi_tt, and reduces to
B_x=C rho only at a static equilibrium. No Newtonian flux replacement occurs.

## Conservation does not supply an equilibrium

At a regular static equilibrium all original variables, including lambda,
are time independent. The local fluid/field equations are the inherited ones
with a_ref=a_c exp(lambda_0), and additionally

    V'(lambda_0)=integral_0^d T(g_0,a_0)/C dx.                   (3)

For Q, b_a=(a/sqrt(a²+4g²)-1)/2<0 for g>0. Hence T>0 wherever
g>0. On a nonzero-field regular slab the right side of (3) is strictly
positive. If V is identically constant, no such static equilibrium exists,
despite (2) and I>0. This excludes this minimal zero-restoring-force model,
not all possible autonomous completions or evolving solutions.

For general V, a local IVP solution from FGF030 does not automatically solve
(3). A V selected independently must satisfy (3) before any Hessian stability
claim applies. No linear term is fitted here to make a chosen slab pass.

## Full second variation at an actual equilibrium

Assume a smooth positive-density, positive-gradient equilibrium satisfying
ALL local equations, mass constraint, fixed walls and (3). Let u=(xi,psi,eta)
be the material displacement, delta phi and delta chi, each with zero traces,
and s=delta lambda be a single real variable. At the background define

    A=b_g>0, q=g A-B, S=T_chi|g=2T-gq.

S here is a constitutive derivative, not the action or energy flux. The
fixed-lambda second variation is the original full form

    Q0[u]=integral [ c_s²((rho xi)')²/rho -2(rho xi)'psi
          +(A psi'²-2q eta psi'+J eta'²+(U''-S)eta²)/C ] dx.       (4)

The matter closure is the inherited isothermal one. No dynamical field has
been minimized out. Its kinetic mass form is

    N0[u]=integral [rho xi²+(tau psi²+sigma eta²)/C] dx.

W depends on chi and lambda only through their sum. Its new second-variation
terms are -2q s psi'/C-2S s eta/C-S s²/C. U depends only on chi;
the driver contributes V''(lambda_0)s². Therefore the full form is

    Q[u,s]=Q0[u]+2s ell[u]+k s²,
    ell[u]=-integral(q psi'+S eta)/C dx,
    k=V''(lambda_0)-integral S/C dx,
    N[u,s]=N0[u]+I s².                                        (5)

There is no direct xi-s term from rho phi, since that interaction is
independent of lambda. Fluid coupling remains inside Q0 and cannot be dropped
when responding to ell. The wall compatibility term that would arise from
minimizing psi is not discarded; this proof uses the unreduced form (4).

## Exact Schur condition in the full function space

Let X=H1_0(0,d)^3 in fixed reference units, chosen once before comparing
references. This avoids adding norms of dimensionally different fields.
Assume Q0 is a continuous symmetric coercive form on X: Q0[u]>=c0||u||_X²
with c0>0. This must be independently proved for the actual equilibrium;
FGF030 supplies such a statement only for its declared diagnostic family.
Smooth bounded q,S on a finite interval make ell continuous on X.

Let a0(u,v) be the polarization of Q0, so a0(u,u)=Q0[u]. There is a unique
z in X satisfying a0(z,v)=ell[v] for every v in X. Existence follows by
representing the continuous linear functional in the complete inner product
a0; equivalently minimize Q0[v]/2-ell[v]. Define

    beta=Q0[z]=ell[z]=sup_{u!=0} ell[u]²/Q0[u]>=0,
    Delta=k-beta.

Completing the square gives the exact continuum identity

    Q[u,s]=Q0[u+s z]+Delta s².                                 (6)

The map (u,s)->(u+s z,s) is bounded and invertible. Consequently Q is
coercive on X times R if and only if Delta>0. For Delta=0 the form is
nonnegative with exactly the one-dimensional kernel span{(-z,1)}. It has
no strict gap; the corresponding zero-frequency displacement can drift
linearly for nonzero initial velocity. For Delta<0 it has precisely one
negative form direction in the sense of negative index, witnessed by
(-z,1); there can be no two-dimensional negative subspace by (6).

For the regular fixed-interval wave system here, the positive kinetic inner
product N is equivalent to weighted L2 plus the real global coordinate.
The form domain embeds compactly into that space. Bounded smooth coefficients
and the above coercive Q0 imply a closed, lower-bounded full form with compact
resolvent. Its generalized self-adjoint spectrum therefore has one negative
squared-frequency mode when Delta<0, one zero mode when Delta=0, and a
positive gap when Delta>0. These are linear statements about the autonomous
time-reversal system. No nonlinear or global solution theorem follows.

Increasing finite I>0 changes kinetic weights and modal rates but not the
sign of Delta or the existence of the negative direction. Positive inertia
and conserved energy are thus insufficient for stability. The singular
I=0 constraint problem is outside this candidate and cannot be used to
erase the new degree of freedom while retaining this proof.

## Dynamical theta coordinates retain the global canonical pair

Now theta=chi+lambda is an autonomous point transformation of dynamical
coordinates, not the externally prescribed time change of FGF032. The scale
kinetic form becomes

    integral sigma(theta_t-lambda_dot)²/(2C) dx + I lambda_dot²/2.

Let pi_theta=sigma(theta_t-lambda_dot)/C. Its global conjugate momentum is

    P_lambda=I lambda_dot-integral pi_theta dx.

The canonical one-form identity is
integral pi_chi delta chi dx+p_lambda delta lambda
=integral pi_theta delta theta dx+P_lambda delta lambda,
where p_lambda=I lambda_dot in the old coordinates. Thus the scale/driver
part of the Hamiltonian kinetic energy is

    integral C pi_theta²/(2sigma) dx
       +(P_lambda+integral pi_theta dx)²/(2I).                  (7)

This is positive and nondegenerate. In velocity variables its zero set
requires lambda_dot=0 and theta_t=0; the potential/fluid positive inertias
remain as before. No extra momentum has vanished. There is one added global
canonical pair, not a gauge freedom or a proof about gravitational mode count.
The total Hamiltonian is the same conserved energy in the new coordinates;
there is no unbalanced externally prescribed lambda_dot*pi_theta correction
once the global Legendre transform is included.

The transformed perturbation zeta=eta+s satisfies zeta(0)=zeta(d)=s.
Equivalently zeta-s is in H1_0. Imposing zeta=0 independently at the walls
would change the problem and incorrectly remove allowed global variations.
The mapped quadratic form and kinetic rank are therefore identical to (5).

## Controls and remaining physical gap

The V-constant no-equilibrium result is an exact obstruction, not an unstable
eigenvalue calculation around a nonexistent background. For any actual
equilibrium satisfying the hypotheses, s=0 recovers Q0; u=-s z isolates
Delta exactly. Suppressing ell gives the generally wrong threshold k=0
instead of k=beta. Raising I cannot change that threshold. The theta momentum
and boundary controls detect treating the new coordinate as prescribed or
gauge. These are analytic controls; no numerical spectrum is claimed.

Both a0 values, 9.3619e-11 and1.1279e-10 m/s², remain separate reference
hypotheses. One may use fixed a_c and constant lambda offsets to represent
them, but (3) must hold separately for one declared V and the actual walls.
A frozen H reference is not an evolving H trajectory; no V or initial data
are reconstructed to force such a trajectory. Q and its action are explicit;
RAR, registered M and operative filtered MONO are not silently substituted.

The formal extension conserves global energy, but no physical V,I, equilibrium
family, local driver stress, metric/photon coupling, scale-vacuum interpretation
or two-gravitational-DOF construction is supplied. Even if Delta>0 were verified
for an actual candidate, that would only close its linear diagnostic stability
test. It would not close the physical theory or establish historical novelty.
