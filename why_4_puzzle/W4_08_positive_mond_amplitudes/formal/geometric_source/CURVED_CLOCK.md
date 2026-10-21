# Actual curved vacuum and near-vacuum clock modes

2026-10-20. Base `f4d7d0e7a`; criteria-only commit `1a46afd06`.
This is P3 of `FROZEN_CRITERIA.md`. It improves a specified classical health
obligation, not the original microscopic normalization/quantum goal.
No target, measured quantity, scan, script or new Lean calculation enters.

**Result.** In the c1-only action the actual de Sitter clock/metric vector
and scalar sectors have positive reduced kinetic/restoring coefficients
for finite k and 0<M<M_Pl^2. The exact homogeneous finite-gradient Bianchi
tilt has curvature mass 2H_perp^2 minus its portal contribution. It decays
in a controlled sufficiently small-gradient future basin at each fixed
coupling in that open interval. This is not a finite-k finite-gradient
Bianchi stability theorem. The rational scalar still has zero vacuum
spatial stiffness and a singular real-auxiliary Hessian; quantum and
global source obligations remain open.

## 1. Fixed action, state and notation

Keep the action and rational coefficients of
`../gravity_constraints/RESULT.md` and `../clock_flux/RESULT.md`:

    S=int sqrt(-g)[B R/2-M(nabla_mu u_nu)(nabla^mu u^nu)/2
                    +lambda_u(u.u+1)+L_rational],
    B=M_Pl^2, 0<M<B, A=B-M, S_c=2B+M, B_cos=B+M/2.

The letter S_c is a coefficient, not the action. There is no matter source
in this mode calculation. At phi=constant, F=F0, u=partial_t the rational
sector supplies -V0, with V0=g^2/(12tau)>0. Its exact isotropic background is

    a=exp(Ht), H^2=V0/(3B_cos)>0.

Lapse variation is retained until the background and perturbative
constraints are imposed. The unit constraint is solved on its timelike
branch. All homogeneous rapidities below are relative to the ADM normal;
coordinate components u^i alone are not that relative velocity.

## 2. Transverse finite-k vacuum mode, including the shift

Fix the spatial vector metric gauge, and take transverse V_i,s_i:

    h_ij=a^2 delta_ij, N=1, s_i=a N^i, u_i=a V_i,
    partial_i V_i=partial_i s_i=0, X=k_com^2/a^2>0.

Thus u^i=V_i/a-N^i to linear order. The scalar lapse and scalar/tensor
metric modes cannot mix with this vector block by isotropy. Expanding the
unit-normalized vector and the extrinsic curvature directly gives, for
each transverse polarization and after spatial integrations by parts,

    L2/a^3=M/2[Vdot^2-(X+2H^2)V^2]
             +(M/2)X s V+(A/4)X s^2.

For example, before multiplying by -M/2 the aether derivative invariant
has quadratic part

    -Vdot^2+2H^2 V^2+X V^2-X s V+(X/2)s^2.

The EH contribution adds B X s^2/4, giving the displayed total A term.
For k nonzero the shift equation fixes

    s=-M V/A.

The constrained action and physical vector speed are therefore

    L2_red=a^3 M/2[Vdot^2-(2H^2+c_V^2 X)V^2],
    c_V^2=(2B-M)/(2A)>0,
    Vddot+3H Vdot+(2H^2+c_V^2 X)V=0.

For U=aV and conformal time eta, the exact temporal boundary is

    S2_red=(M/2)int d eta[U'^2-c_V^2 k_com^2 U^2]
            -(M/2)[(a'/a)U^2]_boundary.

Consequently U''+c_V^2 k_com^2 U=0. Its conformal canonical oscillator
energy is positive. This is an actual constrained finite-k vacuum mode,
not the fixed-metric diagnostic alone. It does not assert luminality with
respect to an independently chosen physical matter metric.

## 3. Longitudinal vacuum ADM reduction and temporal boundary

For a linear longitudinal aether perturbation, vorticity vanishes and a
time-coordinate choice aligns u with the ADM normal. Its physical scalar
degree of freedom then resides in the metric; it is not deleted by that
gauge choice. In this scalar sector

    nabla u.nabla u=K_ij K^ij-a_i a^i,
    S=int Nsqrt(h)[(A K_ij K^ij-B K^2+B R3+M a_i a^i)/2-V0].

Use N=1+n, h_ij=a^2 exp(2zeta)delta_ij, N_i=partial_i chi,
b=a^(-2)Delta chi, U=zetadot-Hn, X=k_com^2/a^2. Expanding this action
and using its background equation gives the raw bracket

    S2=(1/2)int dt a^3[-3S_c U^2+2S_c U b-M b^2
                       +X(2B zeta^2+4B n zeta+M n^2)].

The background metric-only temporal boundary already removed here is
-(9/2)S_c H a^3 zeta^2 at the endpoints. The linear background boundary
is removed along with the background equations. No division by lambda-1
at a GR endpoint is used: throughout this calculation M>0 and A>0.

Set

    C=2A S_c/M, D0=C H^2+M X.

For finite nonzero k, shift and lapse variations give exactly

    b=S_c U/M,
    n=(C H zetadot-2B X zeta)/D0.

After both substitutions the action before the last temporal integration is

    (1/2)int dt a^3[C zetadot^2
          -(C H zetadot-2B X zeta)^2/D0+2B X zeta^2].

Do not freeze X in its cross term: Xdot=-2HX and adot/a=H. Removing the
remaining endpoint term a^3 C H B X zeta^2/D0 yields

    S2_red=(1/2)int dt a^3[K_z zetadot^2-V_z zeta^2],
    K_z=C M X/D0>0,
    V_z=2B X^2[M(2B-M)X+C S_c H^2]/D0^2>0.

For audit, the cross coefficient in the bracket is 4C H B X/D0;
its integrated contribution to the bracket potential is minus
2C H^2 B X(C H^2+3M X)/D0^2. This gives the displayed V_z.

The actual redshifting equation is

    zetaddot+[H+2M H X/D0]zetadot+Omega_z^2 zeta=0,
    Omega_z^2=V_z/K_z
       =2B X[M(2B-M)X+C S_c H^2]/(C M D0)>0.

Friction is positive. Omega_z^2 increases with X and thus decreases in
time. Indeed, its X-dependent factor is X(aX+b)/(c+dX) with a,b,c,d>0;
its derivative has numerator ad X^2+2ac X+bc>0. Therefore
(zetadot^2+Omega_z^2 zeta^2)/2 is a nonincreasing Lyapunov function.
It is not identified with a conserved cosmological energy density.

As X tends to zero, the first-order system approaches zetaddot+H zetadot=0
with integrable O(X) coefficient errors. Its constant limiting evolution
has bounded matrix exponential (eigenvalues 0,-H). Variation of constants
and the integral inequality therefore give future boundedness for every
fixed finite initial k. In particular zeta freezes and the physical
intrinsic-curvature perturbation X zeta decays. This proof does not give a
uniform high-k bound or nonlinear/strong-coupling control.

The high-k squared scalar speed is B(2B-M)/(A S_c)>0. K_z tends to zero
as X tends to zero; that variable/constraint limit is not a proof that the
whole vacuum is regular or that a clock degree of freedom becomes gauge.

## 4. Strict homogeneous limit and the isometry caveat

At k=0 the transverse shift equation above is identically zero; its finite-k
inverse must not be imported. Work directly with a homogeneous unit vector
u=(sqrt(1+v^2),v/a,0,0). The exact unit constraint and the homogeneous
metric constraints leave the quadratic block

    L2=a^3[M vdot^2/2-M H^2v^2],
    v=I1 a^(-1)+I2 a^(-2).

Homogeneous lapse/scale-factor modes are scalars and anisotropic metric
modes are rank-two tensors; no bilinear vector mixing occurs. A homogeneous
shift is a coordinate choice when u_i/a is retained as the relative tilt.

The linear clock acceleration in the orthonormal frame is
delta a_hat=vdot+Hv. Since the background acceleration is zero, this is
gauge invariant. It is nonzero for the a^(-2) mode. The a^(-1) solution has
zero acceleration and is generated by a de Sitter metric isometry changing
the clock congruence. Explicitly, for a constant b_i a Killing generator is

    xi^0=b.x,
    xi^i=-b_i a^(-2)/(2H)-H[(b.x)x_i-b_i |x|^2/2].

Its Lie action on u=partial_t gives delta u^i=-b_i a^(-2), hence a physical
frame component proportional to a^(-1), with delta g=0. Whether that large
isometry is quotiented as gauge depends on boundary conditions. Both
fixed-FRW solutions cannot simply be counted as independent physical
homogeneous modes. The finite-k constrained modes in sections 2-3 avoid
this strict zero-mode ambiguity.

At this vacuum the rational scalar is separate at quadratic order. Its
time coefficient is K0=5g/6, its spatial stiffness vanishes, and its real
F Hessian vanishes at the auxiliary fold. Those facts are unchanged by the
positive clock/metric reductions. No full regular vacuum Hamiltonian or
quantum microscopic health follows from the clock result.

## 5. Exact homogeneous finite-gradient Bianchi tilt

Use the consistent background

    ds^2=-dt^2+a_perp^2(dx^2+dy^2)+a_parallel^2 dz^2,
    phi=pz, h=p/a_parallel, u=partial_t, F=f(h).

For the homogeneous odd perturbation introduce rapidity theta relative
to the ADM normal and a homogeneous scalar displacement varphi(t):

    u=cosh(theta)n-sinh(theta)e_z,
    d=(varphidot-p N^z)/N,
    X_scalar=(h^2-d^2)/2,
    J=X_scalar+[cosh(theta)d-sinh(theta)h]^2/2.

The rational coefficients below are evaluated on the regular finite-h
background branch:

    a_slope=E_X>0, j=L_J>0, K=a_slope+j.

Here a_slope is not a scale factor. The homogeneous aether invariant is
exactly

    nabla u.nabla u=2H_perp^2+H_parallel^2
                    +2H_perp^2 sinh(theta)^2-(thetadot/N)^2.

Thus the odd quadratic block, with volume W=a_perp^2 a_parallel, is

    L2/W=M thetadot^2/2-M H_perp^2 theta^2
            +K d^2/2-jh theta d+jh^2 theta^2/2.

Lapse and diagonal metric perturbations are even under the background's
combined spatial/scalar reflection and have no bilinear odd mixing.
The homogeneous shift must still be varied. Gravity and aether have no
homogeneous shift dependence in these relative variables, so it gives

    h(Kd-jh theta)=0.

For h>0 this imposes the zero scalar-momentum condition, rather than
assuming a special ensemble by hand. The auxiliary has no linear source
in d,theta and therefore contributes no extra quadratic elimination term.
After the shift constraint,

    L2_red=W M/2[thetadot^2-mu_theta^2 theta^2],
    mu_theta^2=2H_perp^2-m_t^2(h),
    m_t^2(h)=h^2 j a_slope/(KM),
    thetaddot+(2H_perp+H_parallel)thetadot+mu_theta^2 theta=0.

This is an equation on the actual evolving background. Its physical
perturbation includes delta(u.partial phi)=-(a_slope/K)h theta, nonzero at
finite h, so the finite-gradient tilt is not the acceleration-free vacuum
isometry. An instantaneous negative mu_theta^2 is not an all-time growth
theorem, and an instantaneous positive value is not an all-time stability
theorem on an arbitrary evolving background.

## 6. A controlled expanding near-vacuum basin at fixed finite coupling

Write a_perp=exp(alpha+beta), a_parallel=exp(alpha-2beta),
H=alphadot, v=betadot, and F_s(h)=h^2 E_X. The exact background equations
are

    3B_cos H^2-3A v^2=E(h),
    vdot+3Hv=-F_s/(3A),
    hdot=-(H-2v)h,
    Hdot=-3A v^2/B_cos-F_s/(6B_cos).

Take initial v=0 and the expanding constraint root. The branch has
E>=V0, E-V0=C3 h^3+O(h^4), F_s=3C3 h^3+O(h^4). Thus H>=H0,
where H0^2=V0/(3B_cos), and v<=0. These conclusions do not assume a
positive H_perp. They first imply h(t)<=h_i exp(-H0 t).

Choose h_* and C_F>0 such that 0<=F_s(h)<=C_F h^3 for 0<h<=h_*.
For h_i<=h_*, the exact damped integral gives

    |v(t)|<=C_F h_i^3 t exp(-3H0 t)/(3A)
            <=C_F h_i^3/(9A H0).

A sufficient explicit smallness condition is

    C_F h_i^3 < min[(9/4)A H0^2, M H0^2/8].

It proves H_perp=H+v>3H0/4, rather than assuming it in a bootstrap.
Also m_t^2<=F_s/M<H0^2/8, hence mu_theta^2>H0^2. The instantaneous
homogeneous quadratic Hamiltonian is positive in this basin, but is
time dependent and is not claimed conserved.

The constraint gives H-H0=O(h^3+v^2). Consequently H_perp,H_parallel
approach H0 with errors O((1+t)exp(-3H0t)), and m_t^2 has the same
integrable decay. The tilt equation approaches
thetaddot+3H0 thetadot+2H0^2 theta=0. Its limiting roots are -H0,-2H0.
Weighted variation of constants with the integrable coefficient errors
gives theta,thetadot=O(exp(-H0t)). This sector is cured in that controlled
near-vacuum basin, rather than merely acquiring a slower flat-space growth.
The smallness condition is not uniform as M tends to zero or A tends to
zero. It proves no finite-k finite-h Bianchi statement.

## 7. Relation to the old band and the remaining physical decision

At the previously tested point x=11/112,F/F0=3/4, initial zero shear has
H_bg^2=E/[3(B+M/2)] and m_t^2=(1210/41601)E/M. Its instantaneous
homogeneous mu_theta^2 is positive exactly when

    M/B>1210/27129.

This is only the sign at that initial state. The shear and h then evolve;
it is not a global stability threshold. Likewise
m_b^2/H_bg^2=(165/1698)(B/M+1/2) shows why the old flat WKB band cannot
be applied at arbitrary retained M/B. Its separated subcurvature growing
packet remains valid in its prior small-M/B, fixed finite-h validity window.
Taking h to zero at fixed M/B and taking M/B to zero at fixed h are
different limits.

Uncomputed here are the coupled finite-k finite-h Bianchi constraints and
nonautonomous spectrum, nonlinear/strong-coupling behavior, UV/cutoff
control, a global sourced halo and a quantum completion. Curvature restoring
terms do not select the physical matter charge Q: it is absent from this
matter-free calculation. Nor do they fix allowed cubic/vacuum response
deformations. A healthier clock sector therefore improves one obligation
without producing an amplitude-selection equation.
