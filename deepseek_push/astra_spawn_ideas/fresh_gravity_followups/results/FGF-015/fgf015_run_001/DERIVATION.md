# FGF-015: conforming global modes of the actual hydrostatic slab

Written before implementation. Worker `/root/proof_precision`, actual Astra
agent; not a DeepSeek execution. The FGF-011 accepted result and all its
declared artifacts, the revised task, and the source-proposal hash were
verified before using their premises. The calculation is restricted to the
unfiltered Q/R scalar diagnostic, not the operative filtered-MONO or metric
theory. No literature search or empirical inference is included.

## Exact problem and boundary conditions

Keep C=4 pi G, constant vacuum scale a>0, sound speed cs>0, K>0, and the
accepted fixed-a scalar constitutive law. On a finite interval [0,d], use
the actual positive isothermal hydrostatic background

    cs² rho'=-rho g,   A g'=C rho,   A=b_g(g;a)>0.

The selected Q and R backgrounds have u(0)=B(0)/a=.01 and dimensionless
initial density r(0)=.1, on 0<=x a/cs²<=1. These are two of the four recorded
MS1 backgrounds and were included in the FGF-011 independent audit.
Background wall pressure and potential support are external. The boundary
conditions on perturbations are exactly xi=psi=0 at both endpoints; perturbed
scalar flux A psi' is free and is not also set to zero.

With material displacement xi, delta rho=-(rho xi)', the linear equations are

    xi_tt=-[cs² delta rho/rho+psi]',
    (K/c²)psi_tt-(A psi')'=-C delta rho.

The positive kinetic form is integral[rho xi_t²+(K/c²)psi_t²/C]dx/2.
The original potential form is

    2V=integral[cs²((rho xi)')²/rho+(A/C)psi'²
                 -2(rho xi)'psi]dx.

To verify the accepted factorization independently, expand the first square
and integrate 2cs² rho' xi xi'. Its remaining xi² coefficient is
cs² rho'^2/rho-cs² rho''=rho g'=C rho²/A. Integrating the coupling by parts
then gives

    2V=integral[cs² rho xi'²+(A/C)(psi'+C rho xi/A)²]dx
          +[cs² rho'xi²-2rho xi psi]_0^d.               (F1)

The endpoint term vanishes for the stated walls. Zero potential energy then
forces xi'=0 and xi=0, followed by psi'=0 and psi=0. Thus every nonzero
admissible longitudinal perturbation has strictly positive energy. A negative
eigenvalue in a conforming discretization is an implementation/audit failure
under these hypotheses, not a physical mode discovery.

## Units, actual coefficients and finite parameter box

Use chi=x a/cs², s=t a/cs, X=xi a/cs², P=psi/cs²,
u=B/a and r=C cs² rho/a². The background equations reduce to

    u_chi=r, r_chi=-r f(u), f(u)=F(a u;a)/a,
    A=1/f'(u), eta=K cs²/c².

Reconstruct the continuous background by integrating these two ODEs with a
dense solution. Compare it to the pinned MS1 samples; also check the independent
first integral r+integral_(u0)^u f(v)dv=r0. The trial space uses the actual
varying r and A, not a locally frozen substitute.

After removing a common positive energy factor a cs²/C, the kinetic and
potential bilinear forms are

    M[(X,P),(Z,Q)]=integral[r X Z+eta P Q]dchi,

    H[(X,P),(Z,Q)]=integral[r X'Z'
                        +A(P'+rX/A)(Q'+rZ/A)]dchi.     (F2)

The inertia choices are eta=.01,.04, corresponding exactly to K=2,8 at
one fixed cs/c=sqrt(.005). This is a declared toy ratio, not a source fit.
There are 2 branches x 2 inertias x 3 grids=12 primary parameter cells.
Each grid has N=64,128,256 interior nodes plus the two fixed endpoints.
The requested output is the ten smallest dimensionless Omega² eigenvalues,
eigenfunction samples, mass-matrix positivity, residuals and refinement gaps.

Both registered vacuum normalizations a=9.3619e-11 and 1.1279e-10 m/s²
restore physical angular frequencies through omega=(a/cs)Omega and physical
length through d=cs²/a for this unit-length dimensionless family. Holding
dimensionless u,r fixed also rescales B and rho when a changes: this is not
the same physical slab under two fitted laws. The separate H(z) prescription
is not inserted into this exact time-independent equilibrium; no expansion,
scale dynamics or H-dependent global mode is claimed.

## Conforming discretization derived from the squares

Use continuous piecewise-linear nodal basis functions with both endpoint
values removed for each field. Let N be the two local shape values and D
their derivatives on an element. Positive Gauss-Legendre quadrature weights
assemble the stiffness blocks

    H_XX = integral[r D^T D+(r²/A)N^T N],
    H_XP = integral[r N^T D], H_PX=H_XP^T,
    H_PP = integral[A D^T D].                           (F3)

The consistent mass blocks are M_XX=integral[r N^T N] and
M_PP=eta integral[N^T N], with zero mixed mass. Every quadrature contribution
to H is itself a sum of positive squares. Consequently the assembled form
retains positivity rather than relying on cancellation between pressure,
gravity and density-gradient terms.

An independent assembly checks the original form, using
d=-(r D+r' N) and exact r'=-r f(u): its blocks are
integral[d^T d/r], integral[d^T N] and integral[A D^T D].
The two matrices should agree to quadrature/background tolerance once the
Dirichlet endpoints are removed. This checks the integration-by-parts signs.
Rayleigh quotients of all returned modes are independently integrated from
the original form at higher quadrature order, not merely re-read from the
eigensolver diagonal.

Solve H v=Omega² M v with a symmetric generalized eigensolver. Check
Cholesky positivity of both M and H, M-orthonormality, direct residuals and
the independently integrated Rayleigh quotients. Record endpoint psi slopes
to demonstrate that Dirichlet values have not been supplemented with a
zero-flux condition. The grids with N=64,128,256 are not nested (they have
65,129,257 elements), so any monotone refinement observed is numerical
evidence, not a direct nested-space min-max guarantee.

## Controls and stopping criteria

1. Remove the original density-potential cross block. Both separate Dirichlet
   sectors must have positive lowest eigenvalues; this tests the sign of the
   kinetic and individual stiffness blocks.
2. As a separate periodic, supported/subtracted constant-background control,
   integrate xi=sin(kx), psi=cos(kx), rho=1, A=.5 over [0,2pi], with integer
   k=1,3 and eta=.01,.04. The original quadratic form must reproduce

       (Omega²-k²)(Omega²-A k²/eta)-k²/eta=0.

   The k=1 mode is negative in that deliberately different background. Applying
   (F1)'s positive-square formula there is invalid because hydrostatic balance
   fails; the falsely stabilized result is a decisive wrong-premise control.
3. Test xi=1, psi=0 on the actual slab as a deliberately nonadmissible trial
   function. The difference between original and squared integrals must equal
   [r']_0^1. Dropping that boundary term must fail measurably. This does not
   alter the physical eigenproblem or impose a new boundary condition.

Use binary64, deterministic inputs, eight quadrature nodes per element in the
primary assembly and twelve for the independent form/Rayleigh checks. Request
120-second wall and one numerical-library thread bounds, record their actual
enforcement through the computation-audit runner, and limit logs to 1 MiB.
No memory cap is claimed. Stop after the specified 12 primary cells and
controls. If a sign, residual or declared refinement check fails, preserve
that attempt and investigate before reporting any physical conclusion.
Finite spectra do not prove three-dimensional, free-boundary, nonlinear,
zero-field, variable-scale, non-isothermal, cosmological or filtered-MONO
stability. The accepted exact factorization supplies the sign theorem only
for this finite longitudinal boundary problem.
