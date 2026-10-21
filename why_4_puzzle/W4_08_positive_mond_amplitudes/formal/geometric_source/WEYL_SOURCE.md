# Integrable Weyl scalar: physical degree, source and normalization

2026-10-20. Base f4d7d0e7a; criteria-only commit 1a46afd06.
**The original healthy microscopic xi=1/4 goal remains open.**
This is Scholz's integrable-Weyl scalar cubic, distinct from W4-11/Q4's
Weyl-Rtilde^2/Einstein-Proca model, Weyl-Mannheim and anomaly cancellation.
The primary version/publisher and exact extraction pins are in SOURCES_WEYL.md.
No observed a0,H0,density,charge or target selects a coefficient here.
Use c=hbar=1 and signature -+++. xi_W denotes the source's hierarchy
parameter, not the campaign's operational xi=kappa^2.

## 1. Published action and the exact boundary of this audit

The source has a weight -1 scalar phi and integrable scale connection
varphi. In the spacelike Milgrom regime its densities divided by sqrt(-g) are

    L_H=(xi_W phi)^2 R_W/2,
    L_2=-alpha [D(xi_W phi)]^2/2,
    L_3=-beta xi_W^3 phi^(-2)|D phi|^3/3,
    L_mass=xi_W^2 phi D^2 phi (A_mu A^mu),
    L_V=-lambda phi^4,          A_mu A^mu=-1.

The declared matter coupling is S_m[g_E,Y]. A is an additional
nondynamical timelike vector, of weight -1. The quadratic, cubic and
mass terms are multiplied by a spacelike-gradient switch and a regime
function. The paper expressly does not derive transition dynamics from
that function. We examine the pure regime where both factors are one.
No derivative of a varying switch is discarded as if it were constant.

There are inequivalent possible variational prescriptions: external fixed
A, an independently varied constrained A, a normalized khronon normal,
or a unit constraint solved before variation. The following constrained
closure is an explicit diagnostic, not silently the published external-A
recipe. A complete spectrum/source claim for the latter needs its own
off-shell matter/background prescription.

## 2. What remains after Einstein gauge

Local rescaling acts as

    g->Omega^2 g, phi->Omega^(-1)phi,
    varphi->varphi-d log Omega,          varphi=dtheta locally.

The invariant variables on a phi>0 patch are

    ghat=(phi/phi0)^2 g,
    sigma=theta-log(phi/phi0), b=varphi-d log phi=d sigma,
    D phi=-phi b.

In Riemann gauge theta=0, phi=phi0 exp(-sigma). In Einstein gauge
phi=phi0 while varphi=d sigma. A nonzero b cannot be removed by a Weyl
gauge transformation, so this scalar need not be a pure Stueckelberg mode.
If an additional condition D phi=0 is imposed, b=0 and the cubic vanishes.
One must not use that extra condition to count a propagating MOND scalar.

Define the natural-unit scales

    M^2=xi_W^2 phi0^2, a=phi0/xi_W,
    V0=lambda phi0^4=lambda a^2 M^2.

phi0 and M,a have mass dimension one; sigma,alpha,beta,lambda,xi_W are
dimensionless. Take phi0,xi_W,beta>0, and lambda>0 for positive vacuum;
alpha is unrestricted until the explicit phase choice is made.
The published hierarchy convention uses the measured MOND scale; it is
not a microscopic selecting equation and is not an input to our calculation.

## 3. A consistently enforced unit vector removes the improvement stress

In Einstein gauge, with X=(partial sigma)^2 and F=Box sigma+X,

    R_W=R(ghat)-6 Box sigma-6X,
    L_mass=-M^2 F A^2.

For an independent vector without derivative dynamics, add its multiplier:

    L_A=-M^2 F A^2+ell(A^2+1),
    E_A=2(ell-M^2 F)A_mu=0,     E_ell=A^2+1=0.

Since A is nonzero, ell=M^2 F. Eliminating both constraints gives
L_A=+M^2(Box sigma+X). The multiplier's metric variation cancels the
normalization contribution that would result from varying A^2 at fixed
components. The same reduced action follows if A is identically normalized
before variation, including A=-dT/sqrt[-(dT)^2] on its timelike patch.
This mass operator alone then has no remaining khronon dependence.

Modulo an ordinary boundary term, the resulting action is

    L_E=M^2 R/2-M^2(alpha+4)X/2
                    -beta M^2 X^(3/2)/(3a)-V0,       X>0.

For a fixed external A whose components are held while the metric varies,
delta(A^2) is nonzero. Its associated stress cannot also be computed by
setting delta(A^2)=0. Conversely its published normalization stress cannot
be imported into the constrained closure above. A dynamical A action could
change this result, but would add field equations, stress and physical modes.

For a covariant scalar/vector sector, using unconstrained contravariant
A and E_A=(1/sqrt(-g))delta S/delta A, the diffeomorphism identity reads

    nabla_mu T^mu_nu=E_sigma partial_nu sigma
       +E_A,rho nabla_nu A^rho+nabla_mu(A^mu E_A,nu).

An external vector need not satisfy E_A=0; the extra terms must be handled
by its specified background/physical sector. This does not prove a global
inconsistency of the published recipe or force nonconservation on every
special static background. It identifies the missing variational bridge.

## 4. Retained scalar symbol and its vacuum limit in this closure

Let sigma=Hz+pi in a local orthonormal static patch, H>0, beta>0.
The reduced scalar quadratic derivative action is

    L2=K pidot^2/2-K|grad_perp pi|^2/2-K_parallel(pi_z)^2/2,
    K=M^2[alpha+4+beta H/a],
    K_parallel=M^2[alpha+4+2beta H/a].

Positive K and K_parallel give a hyperbolic positive-kinetic scalar at
that fixed background; pi_c=sqrt(K)pi is its canonical local variable.
At alpha=-4, K=beta M^2 H/a>0 and c_parallel^2=2, c_perp^2=1.
The wider longitudinal cone is reported, not converted into a universal
UV-completion no-go. K tends to zero as H tends to zero, so the pure
Milgrom branch supplies no regular canonical zero-gradient vacuum mode.
Alpha>-4 supplies a quadratic infrared response; alpha<-4 has negative
time kinetic near zero within this same branch.

These are the retained scalar symbols of the explicit normalized closure.
They are not the full constrained spectrum of an unspecified external-A
theory, transition action or sourced curved halo. Outside the Milgrom
regime the retained Hilbert term alone contains -3M^2 X. Merely setting
the added scalar terms to zero does not variationally eliminate sigma.
The spacelike and switched timelike limits cannot be joined into a regular
vacuum spectrum by asserting that the scalar is inert there.

## 5. The same compensator gives zero direct matter charge

A Weyl-invariant massive point action using the same compensator is

    S_particle=-y int phi ds_g=-y phi0 int ds_ghat.

It gives universal attraction through ghat but zero direct sigma charge.
More generally, for literal S_m[ghat,Y], with matter variables in their
Einstein-variable convention, the chain rule gives the density identity

    2g^{mu nu} (delta S_m/delta g^{mu nu})
                           +phi(delta S_m/delta phi)=0.

The two terms are respectively
-sqrt(-ghat) T_hat and +sqrt(-ghat) T_hat. In Einstein variables
delta S_m/delta sigma at fixed ghat is zero. Omitting its phi variation
in a different frame leaves an uncancelled matter-trace source in this
combination. The source's placeholder matter tensor and external-vector
calculus need an explicit action-level explanation before that trace
source is transferred to a new microscopic theory.

In the normalized closure, literal S_m[ghat] consequently gives

    nabla_mu{M^2[alpha+4+(beta/a)sqrt(X)]partial^mu sigma}=0.

A boundary-supplied scalar profile is possible; its charge is not thereby
fixed by baryonic mass. The missing implication is a sourced branch,
not simply a numerical value for an already operational MOND coefficient.

If sigma is admitted as the local integrable scalar potential, local Weyl
symmetry also permits a changed matter action S_m[exp(2q sigma)ghat].
Any q is allowed by that symmetry. Its dust/test charge is q and its local
canonical charge is q/sqrt(K). This is a new matter coupling, not the
published S_m[ghat] or a whole-action change of field coordinates.

## 6. Conditional force normalization and a physical counterfamily

Choose q>0 by scalar orientation for the positive-force formulas. For a
genuinely sourced local static cubic, the n>=2 spatial Gauss law is
3C3 div(|grad sigma|grad sigma)=q rho and
3C3 Omega_(n-1)r^(n-1)h^2=q m, h=|grad sigma|.
Only n=3 gives a 1/r scalar acceleration; a source/test q must be included
twice before comparing with a force-calibrated Newton constant.

Even granting the paper's quoted weak-field trace-source/metric map,

    G=1/(8pi M^2), div(h grad sigma)=8pi G a rho/beta,
    g_scalar=h, a_IR=2a/beta, V0=lambda a^2 M^2,
    xi=a_IR^2/(G V0)=32pi/(lambda beta^2).

Beta=2 labels a_IR by a; it does not fix the remaining ratio. This is a
conditional arithmetic consequence of that map, not a repaired derivation
of its variational source or a healthy amplitude prediction.

For the changed q matter action and the two pure phase actions of the
normalized closure, the unscreened Einstein phase has C2=3M^2,
Gs=q^2 G/3 and G_UV=G(1+q^2/3), rather than automatic screening.
The cubic phase gives g_scalar^2=2q^3 a Gm/(beta r^2), hence

    a_IR=2q^3 a/[beta(1+q^2/3)],
    xi=32pi q^6/[lambda beta^2(1+q^2/3)^3].

This endpoint dictionary does not supply the unprovided transition action.
Further screening must be derived from an additional operator/state.

The continuous deformation lambda->c lambda, c>0, preserves every Weyl
weight, G, cubic coefficient and matter prescription while changing V0.
Within the finite-static-gradient closure it leaves K and K_parallel
unchanged; it is not a claim of unchanged global curved solutions or
vacuum quantum health. Moreover, the reparameterization

    phi->s phi, xi_W->xi_W/s, beta->s^2 beta, lambda->lambda/s^4

leaves M,C3,V0 invariant and sends a->s^2 a. Thus lambda beta^2 is a
physical invariant, not an 8pi or scalar-normalization convention trick.
All displayed operators are separately Weyl invariant. No checked Ward,
BPS or RG equation fixes this invariant; such an embedding remains open.
For restored units let a_geom be the inverse-length version of a
(a_energy/(hbar c) if expressed initially as an energy). Since the metric
potential sigma is dimensionless, a_IR,phys=2c^2 a_geom/beta and the
constant energy density is epsilon=lambda c^4 a_geom^2/(8pi G).
Their ratio a_IR,phys^2/(G epsilon) is again 32pi/(lambda beta^2).

The strongest constructive next step is a complete variational matter and
vector completion preserving the intended stress/source, followed by its
regular retained vacuum/transition spectrum. An independent equation for
the invariant vacuum/cubic ratio remains necessary even if that succeeds.
