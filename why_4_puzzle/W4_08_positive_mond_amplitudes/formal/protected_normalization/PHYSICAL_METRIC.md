# Disformal physical matter metric: gamma repair without scalar-charge selection

2026-10-20. Base `9a9ab4032`; criteria-only commit `2591280c8`.
This is the P3 calculation in `FROZEN_CRITERIA.md`. The original healthy
microscopic normalization goal remains open. No measured gamma, acceleration,
density or target value is an action input.

**Result.** A universal disformal matter metric can repair the conformal
two-potential relation. The TeVeS-shaped family below gives gamma=1 for a
continuous scalar charge Q while changing the actual scalar force fraction.
Invertibility, universal coupling and the displayed conservation identities
do not select Q. A saturated cone condition gives an additional restricted
obstruction only when explicitly imposed over a two-sided neighborhood.
No healthy quantum completion or protected amplitude selector is supplied.

## 1. What is held fixed and what is changed

Keep the Einstein/aether/rational-scalar action of
`../gravity_constraints/RESULT.md` fixed, including its real unit vector
u, c1-only coefficient M>0, and selected static scalar branch. Change the
physical coupling of every matter species to

    tilde_g_mu_nu=A(phi)^2[g_mu_nu+(1-B(phi)^2)u_mu u_nu],
    g(u,u)=-1, A>0, B>0, S_m=S_m[tilde_g,psi].

This defines different matter couplings to the same gravity action. It is
not an invertible rewriting of the whole action into other field variables.
The frozen P3 reference is phi0=0, A0=B0=1. Section 7 separately keeps
general constant A0,B0 and normalizes physical rods and clocks explicitly.

Write, at the reference state,

    alpha=d ln A/dphi, beta=d ln B/dphi, Q=alpha+beta.

The exact variation formulas below use these functions at the local phi;
the linear source/force dictionary uses their reference-state values.

For the dimension-one scalar convention of the rational model, alpha,beta,Q
have mass dimension minus one. A unit exponent after a scalar redefinition
does not fix the canonically normalized charge.

In D spacetime dimensions, rank-one inversion gives exactly

    tilde_g^mu_nu=A^(-2)[g^mu_nu+(1-B^(-2))u^mu u^nu],
    det(tilde_g)=A^(2D) B^2 det(g),
    sqrt(-tilde_g)=A^D B sqrt(-g).

In a g-orthonormal clock frame, tilde_g=A^2 diag(-B^2,1,...,1).
Thus A,B>0 give an invertible Lorentzian physical metric and a common
local time direction. These algebraic conditions contain no equation for
alpha or beta. They do not prove global causality or health of the full
gravity/scalar/clock system.

## 2. Source, test charge and conservation

For a static particle aligned with the clock, its action is

    -m int ds_tilde=-m int A(phi)B(phi)N dt.

At A0=B0=1 this is -m int[1+n+Q delta_phi]dt to first order. The same Q
therefore supplies both the weak dust source and the nonrelativistic test
force. Source mass m is measured in the physical frame. Choose Q>0 by
scalar orientation when writing h=|grad phi| and positive accelerations;
otherwise replace Q by |Q| in the acceleration scale and retain the signed
radial derivative. Q=0 has no leading scalar force of this form.

There is also an exact covariant source formula. Define the physical unit
clock U^mu=u^mu/(AB), so U_mu=AB u_mu, physical stress tilde_T, and
rho_U=tilde_T^{mu nu} U_mu U_nu, with both stress indices contravariant.
At fixed g and u,

    (1/sqrt(-tilde_g)) delta S_m/delta phi
      =alpha tilde_T-beta rho_U.

For an aligned perfect fluid in n spatial dimensions this is

    -Q rho+n alpha p.

Dust thus sources Q. Pressure and radiation need not have the conformal
trace charge. For the gamma=1 family in section 4, the source is
-Q(rho+n p), agreeing with the rho+3p structure of the TeVeS example in
three space dimensions. It is not legitimate to use Q rho for an arbitrary
relativistic or self-gravitating source.

On the matter equations, physical stress obeys
tilde_nabla_mu tilde_T^{mu nu}=0. This follows from the universal physical
matter action for arbitrary smooth A and B. The corresponding Einstein
stress exchanges energy and momentum with phi and u. For unconstrained
contravariant u variables, define

    J_phi=(1/sqrt(-g)) delta S_m/delta phi,
    J_rho=(1/sqrt(-g)) delta S_m/delta u^rho.

Then

    J_phi=A^D B(alpha tilde_T-beta rho_U),
    J_rho=A^D B A^2(1-B^2)g_mu_rho tilde_T^{mu nu} u_nu,
    nabla_mu T^mu_nu=J_phi partial_nu phi
                    +J_rho nabla_nu u^rho+nabla_mu(u^mu J_nu).

The unit multiplier and clock equations account for the clock exchange in
the total Ward identity. All these identities hold for arbitrary A,B;
none turns into an equation selecting their derivatives. Universal coupling
establishes the common source/test action, not a numerical scalar charge.

## 3. Operational force dictionary and both physical potentials

Use weak static potentials on subcurvature scales, an aligned clock and a
weak nonrelativistic source. Retain the leading physical-potential order,
so scalar self-gravity and source sensitivities are beyond the displayed
calculation. A weak-potential region in the actual UV branch is assumed.
For the fixed c1-only action,

    B_T=M_Pl^2-M/2, B_cos=M_Pl^2+M/2,
    Gt=1/(8pi B_T), Gcos=1/(8pi B_cos),
    Phi_E=Psi_E=n, n=-Gt m/r in three space dimensions.

The physical potentials, in
ds_tilde^2=-(1+2Phi_phys)dt^2+(1-2Psi_phys)dx^2, are

    Phi_phys=n+Q delta_phi,
    Psi_phys=n-alpha delta_phi,
    (Phi_phys+Psi_phys)/2=n+(beta/2)delta_phi.

The last combination controls the leading null deflection/time delay.
Its scalar coefficient is beta/2, whereas the dust force coefficient is Q.

For the selected rational branch,

    E-V0~C3 h^3 in the IR, E~C2 h^2 in the UV,
    C2=25g/48, C3=10sqrt(5g tau)/9, V0=g^2/(12tau).

In n>=2 spatial dimensions, with Omega_(n-1) the unit sphere area, the
linear-in-potential source approximation gives

    div[(E_h/h)grad phi]=Q rho,
    Omega_(n-1)r^(n-1) E_h=Q m(<r),
    Gs_n=Q^2/[2 Omega_(n-1) C2], a_s=2Q C2/(3C3),
    g_s,UV=Gs_n m/r^(n-1),
    g_s,IR=sqrt(Gs_n m a_s)/r^((n-1)/2).

Only n=3 gives the exterior 1/r acceleration. Nonlinear A,B and strong
sources can change the integrated scalar charge; the above equation is the
specified weak-source dictionary, not an all-source charge theorem.

In three space dimensions set

    Gs=Q^2/(8pi C2), Guv=Gt+Gs, f=Gs/Guv,
    a_IR=f a_s.

With U_T=Gt m/r, U_s=Gs m/r=-Q delta_phi, the UV potential ratio is

    gamma_UV=[Gt-(alpha/Q)Gs]/[Gt+Gs]
            =1-[(2alpha+beta)/Q]f.

This is the local unscreened UV coefficient. It is not a global PPN
expansion through the nonlinear MOND exterior. Motion relative to the
clock, compact-body sensitivities and screening remain separate problems.

The actual-V0 and Friedmann-inferred footings must both use this new Q:

    xi_V0=a_IR^2/(Guv V0)=f^3(125pi/128),
    3 B_cos H0^2=V0,
    epsilon_inf=3H0^2/(8pi Guv)=(Gcos/Guv)V0,
    xi_inf=xi_V0(Guv/Gcos)
          =(125pi/128) f^3(1+r)/[(1-r)(1-f)],
    r=M/(2M_Pl^2), 0<r<1/2 for the tensor-positive clock action.

The factor f^3 follows because the same Q determines source and test force;
it is not imported by retaining the old conformal charge. Neither density
footing supplies an equation selecting Q. In this calculation V0 is the
fixed rational-sector vacuum, not a newly added physical-matter vacuum term.

## 4. A genuine gamma repair and its continuous counterfamily

For f>0, gamma_UV=1 if and only if

    2alpha+beta=0.

If required at every reference scalar value in a connected interval,
this condition integrates to A^2 B=constant. It constrains a shape, not the
magnitude of Q. In particular, for every constant Q>0,

    A(phi)=exp(-Q phi), B(phi)=exp(2Q phi)

has alpha=-Q, beta=2Q, positive invertible metric and gamma_UV=1. Its
physical dust and null potentials both equal n+Q delta_phi. Nevertheless,
with the gravity and rational scalar coefficients held fixed,

    f=Q^2 B_T/(C2+Q^2 B_T)

varies continuously with Q. Hence its actual-V0 ratio and its inferred
ratio vary. Imposing xi_V0=1/4 would merely choose
f=[32/(125pi)]^(1/3), and therefore a scalar/matter charge. It is not a
selection mechanism. The conformal gamma-versus-target contradiction no
longer applies, because gamma=1 is independent of f in this new family.

The shape A=exp(-varphi), B=exp(2varphi) is Bekenstein's TeVeS metric,
Eq.21-23 of
[astro-ph/0403694v6](https://arxiv.org/html/astro-ph/0403694v6).
It retains free k,K,ell (Eq.25-26), displays a0 and GN (Eq.62,66), and obtains
gamma=1 (Eq.94-98). This is a primary example of the remaining normalization
freedom. Its full spectrum is not imported into our different fixed action.

Writing varphi=Q phi moves Q into the scalar kinetic/response coefficients,
C2_varphi=C2/Q^2 and C3_varphi=C3/Q^3. It does not remove the physical
freedom exhibited by changing Q at fixed original C2,C3,V0. The continuous
counterfamily above is a changed physical coupling, not this rewriting.

## 5. Characteristics and an explicitly added saturated-cone rule

For example, a minimally coupled physical matter scalar on a frozen clock
frame has derivative density

    A^(D-2)/(2B) psidot^2-A^(D-2)B |grad psi|^2/2.

It has positive local time/spatial coefficients for A,B>0 and characteristic
speed B in g-orthonormal coordinates. Its physical speed is one. Equivalently,
the characteristic polynomial is proportional to -omega^2/B^2+|k|^2.
The conformal A drops out of this cone. At a matter-free background the new
matter coupling does not alter the gravity/clock principal operator. A
finite-density coupled principal system needs its own kinetic/constraint
analysis; metric invertibility alone does not establish that analysis.

The fixed c1-only action has

    c_T^2=1/(1-M/M_Pl^2).

Thus the P3 choice B0=1 does not itself make the tensor and physical matter
cones coincide when M>0. A shared local time direction is weaker than exact
equality of their null cones. Neither statement alone establishes global
causality for a general vector with vorticity.

Here is a precise restricted discriminator. Add the assumptions that

1. c_T is independent of phi in the fixed gravity action;
2. B(phi0)=c_T;
3. c_T<=B(phi) throughout a two-sided open phi-neighborhood of phi0.

Then B has a local minimum at phi0, so B'(phi0)=0 and beta=0. Exact equality
of the cones throughout that neighborhood also gives beta=0. Combining this
with gamma_UV=1 and f>0 would force alpha=0, hence Q=0, contradicting a
nonzero scalar force. This added saturated-neighborhood rule therefore
excludes this nontrivial gamma repair for the fixed action.

The added rule is not a consequence of Lorentzian invertibility or a universal
causality theorem. A strict unsaturated inclusion B0>c_T leaves an open
neighborhood admitting arbitrary finite slopes. The family
A=A0 exp(-Q delta_phi), B=B0 exp(2Q delta_phi) then keeps gamma=1 and the
continuous Q freedom within a sufficiently small neighborhood. A one-sided
field domain, a different cone ordering, or phi-dependent gravitational
principal coefficients also changes the hypotheses of this discriminator.

## 6. What a symmetry or protected construction must still supply

The displayed diffeomorphism Ward identity holds for every A,B, so it does
not fix alpha/beta or Q. An exact scalar shift acting with fixed g,u and
invariant massive-matter action would force A and AB to be constant: spatial
and temporal metric variations separately vanish, giving alpha=beta=0.
The clock's unit constraint or a khronon relabeling symmetry does not change
that conclusion into a nonzero protected scalar charge. A compensating
metric/matter transformation is possible only after its invariance is shown
for the entire fixed gravity/rational/matter action.

A claimed SUSY or gauge realization must exhibit such an action and a
normalized identity, rather than identifying a unit exponent with a
canonical coupling. Even if a symmetry fixed the relation B proportional
to A^(-2), it would still need to fix the physical combination
Q^2 B_T/C2, together with the vacuum/IR/UV response relation on the stated
density footing. No such identity follows from the checked TeVeS example or
from the present bosonic action. This bounded check does not prove its absence
in every possible microscopic completion.

Changing only the physical matter coupling also leaves the inherited
matter-free rational clock instability untouched. A kinematic gamma repair
therefore supplies neither the health requirement nor the missing amplitude
selection. No new Lean algebra is needed merely to repeat the already
checked tensor/scalar cube identity.

## 7. Constant-background conversion beyond the normalized P3 reference

This section is an explicit extension, not a change to the frozen A0=B0=1
P3 convention. Merely saying that the physical background is Minkowskian
does not remove a physical tensor/matter cone ratio. Starting with g=eta
and arbitrary constants A0,B0>0, use physical coordinates

    t_phys=A0 B0 t, x_phys=A0 x.

These normalize tilde_g, while g need not have unit light speed in those
coordinates. Hold the scalar coordinate fixed and define coefficients per
physical time and physical volume. In three space dimensions,

    C2_phys=C2/(A0^2 B0), C3_phys=C3/(A0 B0),
    V_phys=V0/(A0^4 B0),
    Gt_phys=A0^2 B0 Gt, Gs_phys=A0^2 B0 Gs,
    Guv_phys=A0^2 B0 Guv, f_phys=f,
    a_s_phys=a_s/A0, a_IR_phys=a_IR/A0,
    Gcos_phys=(A0^2/B0)Gcos, H_phys=H/(A0 B0).

For example, these follow directly by converting the static action measure
dt d^3x and its spatial derivatives, and by converting the homogeneous
kinetic density -3 B_cos a^3 H^2. They assume constant phi and A0,B0;
a rolling conformal/disformal background requires new cosmological work.

The actual energy-density ratio and potential ratio remain

    xi_Vphys=a_IR_phys^2/(Guv_phys V_phys)=xi_V0,
    gamma_UV=1-[(2alpha+beta)/Q]f.

But if density is inferred using Guv_phys,

    epsilon_inf_phys=(Gcos_phys/Guv_phys)V_phys,
    xi_inf_phys=xi_V0 B0^2(Guv/Gcos)
               =(125pi/128) f^3 B0^2(1+r)/[(1-r)(1-f)].

The physical tensor speed is c_T/B0, so equality with matter at the
reference state would set B0=c_T, rather than being implied by coordinate
normalization. These factors are reference conversions, not a mechanism
selecting B0, Q or the vacuum amplitude.
