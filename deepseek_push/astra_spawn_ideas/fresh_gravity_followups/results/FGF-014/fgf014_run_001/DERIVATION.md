# FGF-014: coupled scale, scalar potential and pressure fluid

2026-09-30. Worker /root/coupled_dynamics. Conditional diagnostic extension of
SD1/MS1, not the operative filtered-MONO metric theory. Neither empirical
acceptance nor historical novelty is claimed.

## Premises and exact background

Let C=4piG, tau=K/c²>0, sigma=J/v_chi²>0, J>0, cs²>0, rho0>0.
Use SD1's local action with a=a_ref exp(chi), W_g=b=F^(-1),
Q F=sqrt(B²+aB), R F=B/[1-exp(-sqrt(B/a))]. At g0>0 define
lambda=b_g>0, mu=B/g0>0, q=g0 lambda-B, A=mu I+(lambda-mu)nn^T,
and m=U''-T_chi, T=-W_chi. Assume U'(chi0)=T(g0,a) and
m>q²/lambda; the cosh construction in FGF-010 is one sufficient realization.
Only this strict field Schur bound, not a particular global U, is needed here.

Adopt precisely MS1's artificial supported/subtracted background: scalar source
rho-rho0, fixed acceleration +g0 n in the matter Euler equation, affine
phi0=g0 n.x and periodic zero-mean perturbations. Background supports do not
respond. chi0 is constant and obeys the stated equilibrium equation. This is
an exact modified local model, not a physical homogeneous matter solution of
the unsupported action. Conserved quadratic perturbation energy does not
account for unmodelled external support reservoirs. Transverse fluid velocities
are neutral and excluded from the three longitudinal/field branches below.

## Equations, phases and determinant

Write psi=delta phi, eta=delta chi and delta=delta rho. Linearization gives

    tau psi_tt - div(A grad psi) + q partial_n eta = -C delta,
    sigma eta_tt - J Laplacian eta + m eta - q partial_n psi = 0,
    delta_tt = cs² Laplacian delta + rho0 Laplacian psi.

For exp[i(k.x-omega t)], x=omega², kp=k cos(theta),
Lambda=mu sin²(theta)+lambda cos²(theta), Dphi=Lambda k²-tau x,
Dchi=J k²+m-sigma x, these become

    Dphi psi + i q kp eta = -C delta,
    Dchi eta - i q kp psi = 0,
    (x-cs²k²) delta = rho0 k² psi.

Taking the determinant WITHOUT dividing by Dchi or x-cs²k² yields

    (Dphi Dchi-q² kp²)(x-cs² k²)+C rho0 k² Dchi=0.       (1)

Thus the proposed polynomial's signs and normalization are correct, including
roots at factors that would be lost by naive division.

With longitudinal displacement xi, delta=-i rho0 k xi. Define real-phase
coordinates by eta=i z, xi=i u/sqrt(C rho0). Dividing the energy normalization
by C gives a real symmetric generalized eigenproblem H y=x M y with

    H = [[Lambda k², -q kp, sqrt(C rho0) k],
         [-q kp, J k²+m, 0],
         [sqrt(C rho0) k, 0, cs² k²]],
    M = diag(tau, sigma, 1).

M is positive. H is the correctly phase-rotated stiffness and det(H-xM)
is minus the left side of (1). Hence every x is real. A negative x is a
negative potential direction and exponential growth, not a kinetic ghost or
an oscillatory complex-x instability. This normalization requires rho0>0;
the zero-density algebraic limit below keeps a formal test-fluid mode only.

## Exact instability band and its limits

Put y=k²>0, d=q² cos²(theta), nu=C rho0. The field block is positive because
Lambda(Jy+m)-d>0. Its fluid Schur complement is

    cs² y - nu/[Lambda-d/(Jy+m)].                         (2)

Consequently exactly one squared frequency is negative iff

    h(y)=cs² y[Lambda-d/(Jy+m)] < nu.                    (3)

All three are positive for h(y)>nu; at equality one is zero, with possible
linear-in-time displacement, and the other two are positive. Since

    h'(y)=cs²[Lambda-d m/(Jy+m)²] > 0,

h(0)=0 and h(infinity)=infinity, there is exactly one positive threshold yJ.
It is the positive root of

    cs² Lambda J yJ² + [cs²(Lambda m-d)-nu J] yJ -nu m=0. (4)

For d>0 it exceeds nu/(cs² Lambda); the scale field increases static attractive
susceptibility. For d=0 it equals the old MS1 threshold. The threshold depends
on neither K nor v_chi: these set rates, not inertia of H. At fixed finite
positive parameters, H/k² tends to diag(Lambda,J,cs²), so the three limiting
x/k² are {Lambda/tau, v_chi², cs²}, as an unordered multiset even at degeneracy.
No extra arbitrarily short-wave unstable branch occurs under these premises.
This is not uniform in singular limits J=0, cs=0, zero background field or
vanishing Schur margin, all excluded from the theorem.

Checks of the exact reductions:

* q=0: (1) factors into Dchi times
  Dphi(x-cs²k²)+nu k²=0, precisely MS1 and a free chi oscillator.
* rho0=0: (1) is the SD1 field determinant times (x-cs²k²).
  The last factor is the limiting test-fluid mode; no finite fluid energy
  remains at exactly zero density in unnormalized variables.
* K->0 at k>0: psi becomes constrained. Eliminating it from H gives

      Heff = [[Jk²+m-d/Lambda, q cos(theta) sqrt(nu)/Lambda],
              [q cos(theta) sqrt(nu)/Lambda, cs²k²-nu/Lambda]],
      Meff = diag(sigma,1).

  These two finite branches obey (1) with tau=0. The third frequency squared
  diverges as Lambda k²/tau. One cannot count the cubic as three finite
  modes after setting tau=0 or interchange this singular limit with k=0.

A deliberately reversed matter-coupling sign would turn the minus nu term
in MS1 into plus nu and misses its negative mode. A positive U'' alone does
not enforce m>d/Lambda. Violation of the field Schur premise can already make
a field mode negative at rho=0; it is not a counterexample to (3).

## Units, core framework and tested domain

For numerical checks use acceleration unit a_star, velocity unit c, length
L=c²/a_star, time L/c, potential c², J unit c⁴, m unit a_star², q unit a_star.
Thus tau dimensionless=K, sigma dimensionless=J/v_chi² with v_chi in units c,
nu dimensionless=C rho0 L²/c²; dimensional omega=(a_star/c) omega_hat,
k=(a_star/c²) k_hat, rho0=nu a_star²/(C c²). This produces rescaled toy
families, not the same physical density held fixed while changing a_star.

Restore a_star separately for a0=9.3619e-11 and 1.1279e-10 m/s², each at
constant-vacuum a_star=a0 and the frozen comparison snapshot a_star=a0 E(3),
E(3)=sqrt(.315*4³+.685). No time-dependent H-history solution follows.
The vacuum-defined reference may be a_ref=kappa c sqrt(G rho_Lambda).
A dynamical effective local scale changes the literal pointwise constant-vacuum
reading; this task does not repair or silently remove that incompatibility.
No missing mass is inferred: constitutive coefficients use Q or R throughout.
M is not evaluated, since no analogous local M action is registered here.

The finite experiment checks 288 coefficient cells: Q/R; B/a=.01,1,100;
cos(theta)=0,.6,1; m=q²/lambda+margin with margin=.1,1;
cs=.1,.4; nu=.01,1; K=.2,2; J=.7,v_chi=.6 fixed. At each cell use
k/kJ=.01,.1,.5,.99,1,1.01,2,10,100. Binary64 generalized symmetric
eigenvalues are compared with inertia, polynomial residuals and q=0/rho=0
reductions. A separate K sequence checks the two constrained finite branches.
These finite controls support implementation; equations (2)-(4) supply the
conditional general proof. They are neither observed cluster data nor a
physical inhomogeneous coupled background.

Next discriminating target: derive the quadratic energy and boundary terms
for a genuinely hydrostatic, spatially varying chi-plus-fluid slab, to decide
whether the unstable local band overlaps any valid slowly varying regime.
The fixed-scale slab theorem cannot simply be transferred to responsive chi.
