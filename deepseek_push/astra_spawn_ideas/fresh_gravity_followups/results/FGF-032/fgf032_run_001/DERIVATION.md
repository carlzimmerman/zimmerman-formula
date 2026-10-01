# FGF032: driven reference scale and time-dependent field coordinates

2026-09-30. Proof-only diagnostic-action result. This changes the reference
parameter into an externally prescribed protocol; it does not repeat the
old fixed-reference calculation with prescribed chi=log E. No stage17 proof
or audit output was read. No numerical example or cosmological solution is
asserted.

## 1. Exact model, regularity and dimensions

Let C=4piG, tau=K/c²>0, sigma=J/v_chi²>0, with J,S0,K,v_chi fixed in
physical units. Take a spatially uniform prescribed lambda(t) of class C2,
a_ref(t)=a_c exp lambda(t), actual a=a_c exp[chi+lambda(t)].
The field and interaction Lagrangian density is

 L_f+L_int=[tau phi_t²/2-W(g,a)
        +sigma chi_t²/2-J|grad chi|²/2-U(chi)]/C-rho phi,   (1)
 g=|grad phi|, U(chi)=S0[cosh(2chi)-1]/4.

Matter is the same mass-conserving barotropic action with internal energy
density e(rho), pressure p=rho e'(rho)-e(rho), and kinetic density
rho|v|²/2. Its equations are rho_t+div(rho v)=0 and
rho(v_t+v.grad v)=-grad p-rho grad phi. The earlier isothermal choice
e=cs²rho[log(rho/rho_*)-1] is allowed, but not needed for this balance.
No additional external body force, viscosity, heat source or time-dependent
matter parameter is supplied.

Use smooth solutions on a fixed spatial domain with well-defined traces and
finite energy/flux integrals. Work on g>0 where needed; the energy chain rule
also applies at points where the constitutive gradient has a justified
continuous extension. No PDE existence or well-posedness theorem at g=0
is claimed.

For Q, F(B;a)=sqrt(B²+aB), b=F^(-1), W(g,a)=integral_0^g b(s,a)ds.
Define mu=b/g, P=mu grad phi and

 T(g,a)=-a W_a=-W_chi=-W_lambda.                         (2)

Q gives T>0 for g>0, with T=0 at g=0. The balance algebra below holds
conditionally for any differentiable W with this same dependence on a;
the sign claim is attached to Q, and no M local action is invented.
No constitutive or source equation is changed to Newtonian gravity.

Units: phi has velocity², chi and lambda are dimensionless; W,U,T have
acceleration²; tau has inverse-velocity²; J has velocity^4, sigma has
velocity². Field energy densities are acceleration²/C. The protocol work
density T lambda_t/C has energy-density per time units.

## 2. Original equations and local matter-plus-field energy

Euler variation with lambda treated as prescribed gives

 tau phi_tt-div P=-C rho,
 sigma chi_tt-J Laplacian chi+U'(chi)=T(g,a).            (3)

There is no lambda equation. In particular one cannot impose a chosen
lambda trajectory and then invoke its nonexistent equation to remove work.

The dynamic MOND source relation is div P=C rho+tau phi_tt. In a one-
dimensional positive-gradient patch, B=b(phi_x,a) therefore satisfies
B_x=C rho+tau phi_tt, and its integrated flux difference contains the
additional tau integral phi_tt. The familiar static B_x=C rho or radial
enclosed-source inversion must not be inserted into this evolving problem
unless the required time-derivative term actually vanishes.

Set e_m=rho|v|²/2+e(rho). Continuity, Euler and the barotropic relation imply

 partial_t e_m+div[(e_m+p)v]=-rho v.grad phi.

Adding the interaction energy and its advection gives

 partial_t(e_m+rho phi)+div[(e_m+p+rho phi)v]=rho phi_t.  (4)

The separate field identities, obtained by multiplying (3) by their
velocities and keeping W's full time derivative, are

 partial_t[(tau phi_t²/2+W)/C]
   +div[-phi_t P/C]=-rho phi_t-T(chi_t+lambda_t)/C,

 partial_t[(sigma chi_t²/2+J|grad chi|²/2+U)/C]
   +div[-J chi_t grad chi/C]=+T chi_t/C.                (5)

The internal chi exchange cancels, and matter work cancels the phi term.
Thus the original balance energy density and flux are

 E=e_m+rho phi+
   [tau phi_t²/2+W+sigma chi_t²/2+J|grad chi|²/2+U]/C,

 S=(e_m+p+rho phi)v-[phi_t P+J chi_t grad chi]/C,

 partial_t E+div S=-T lambda_t/C.                     (6)

The sign also follows independently from -partial_t L at fixed original
coordinates: explicit partial_t L=T lambda_t/C. Positive lambda_t therefore
removes energy from this chosen system when Q has g>0; the sign corresponds
to decreasing W at fixed g, not a missing matter-work term.

Here “physical energy” means the original preferred-frame action's specified
matter/field/interacting balance E. It is not a newly constructed covariant
metric energy and need not be positive for arbitrary self-gravitating states.

## 3. Integrated energy and boundaries

For any fixed volume V with outward normal n,

 d/dt integral_V E
   =-integral_boundaryV S.n -lambda_t/C integral_V T.  (7)

Both terms must be retained. With impermeable matter v.n=0 and
time-independent Dirichlet phi and chi at the wall, their time derivatives
vanish there and S.n=0. Then the sole remaining source is the explicit
reference work. Other boundaries may supply additional work; no assumed
global conservation follows without checking them.

For a smooth compact-time protocol whose lambda and lambda_t return to their
initial values, (7) still permits nonzero net work:
Delta integral E=-integral dt lambda_t integral T/C minus boundary transfer.
T depends on the responding fields, not solely on lambda. No closed-loop
zero-work identity is implied. This statement is conditional on an actual
smooth solution; no arbitrarily prescribed off-shell field history is passed
off as an on-shell manufactured check.

## 4. Exact coordinate change theta=chi+lambda(t)

Since lambda is spatially uniform,

 chi_t=theta_t-lambda_t, grad chi=grad theta,
 a=a_c exp theta.

Substitution of EVERY term in (1) gives

 L_tilde=[tau phi_t²/2-W(g,a_c exp theta)
       +sigma(theta_t-lambda_t)²/2-J|grad theta|²/2
       -U(theta-lambda)]/C-rho phi+L_matter.            (8)

Neither the shifted velocity nor the translated potential may be omitted.
In theta coordinates the equations are

 tau phi_tt-div P=-C rho,
 sigma(theta_tt-lambda_tt)-J Laplacian theta
                   +U'(theta-lambda)=T,

 equivalently sigma theta_tt-J Laplacian theta+U'(theta-lambda)
                   =T+sigma lambda_tt.               (9)

The additive lambda_tt term alone is NOT a complete account of the drive:
the potential argument remains time-dependent even when lambda_tt=0.
The map between solutions is exact only with correspondingly transformed
initial and boundary data. For example a fixed original wall chi=chi_b
becomes theta=chi_b+lambda(t), hence theta_t=lambda_t at that wall. Imposing
a fixed theta wall instead would be a different boundary problem.

The original energy in new variables is still

 E=e_m+rho phi+[tau phi_t²/2+W(g,a_c exp theta)
       +sigma(theta_t-lambda_t)²/2
       +J|grad theta|²/2+U(theta-lambda)]/C,             (10)

and S retains -J(theta_t-lambda_t)grad theta/C. It continues to obey (6).

## 5. Canonical Hamiltonian versus the original balance energy

The field momenta of the exactly transformed action are

 pi_phi=tau phi_t/C,
 pi_theta=sigma(theta_t-lambda_t)/C.

The matter coordinates are unchanged. Its Legendre energy is e_m+rho phi.
The canonical Hamiltonian density of (8) is therefore

 H_theta=e_m+rho phi+
       C pi_phi²/(2tau)+W/C+C pi_theta²/(2sigma)
       +lambda_t pi_theta+J|grad theta|²/(2C)
       +U(theta-lambda)/C
       =E+lambda_t pi_theta.                         (11)

The positive sign of this difference is required by using theta_t in the
Legendre transform while the kinetic velocity remains theta_t-lambda_t.
The exact canonical energy flux likewise differs:

 S_theta=(e_m+p+rho phi)v
          -[phi_t P+J theta_t grad theta]/C
        =S-J lambda_t grad theta/C.                  (12)

Explicit differentiation of (8) at fixed theta,theta_t,phi gives

 partial_t H_theta+div S_theta
       =pi_theta lambda_tt-U'(theta-lambda)lambda_t/C. (13)

This is the canonical time-current identity for the same driven system.
It is generally NOT the physical protocol power in (6).

Direct equivalence check: from (9),
partial_t pi_theta-J Laplacian theta/C=(T-U')/C.
Apply a time derivative to H_theta-E=lambda_t pi_theta and a divergence to
S_theta-S=-J lambda_t grad theta/C. Adding the source -T lambda_t/C from
(6) gives exactly the right side of (13). All signs and C factors agree.

Integrated on V, H_total=E_total+lambda_t integral pi_theta and

 dH_total/dt=-integral_boundaryV S_theta.n
       +integral_V[pi_theta lambda_tt-U'lambda_t/C].   (14)

Even if the original physical boundary flux vanishes, the canonical flux
need not: the moving theta wall contributes
-J lambda_t grad theta.n/C. Discarding that term after the coordinate
change would falsely alter the integrated energy law.

A different choice of total-time-derivative convention in the Lagrangian can
also change canonical energy expressions. Equations (11)-(14) use exactly
(8), without discarding or adding time boundary terms. Such bookkeeping
changes cannot erase the original balance (6).

## 6. Why an autonomous replacement is a different model

Replacing (8) by

 L_auto=[tau phi_t²/2-W(g,a_c exp theta)+sigma theta_t²/2
               -J|grad theta|²/2-U(theta)]/C-rho phi+L_matter

would replace the actual scale equation by
sigma theta_tt-J Laplacian theta+U'(theta)=T.
It differs from (9) by U'(theta)-U'(theta-lambda)+sigma lambda_tt.
The two actions are not generally related by the exact coordinate change.

Their Lagrangian difference is

 L_auto-L_tilde=[sigma theta_t lambda_t
          -sigma lambda_t²/2-U(theta)+U(theta-lambda)]/C.

The linear-velocity term is a total derivative only after accounting for
the remainder -sigma theta lambda_tt/C. The shifted-potential difference
also remains. A purely time-only term can leave the equations unchanged but
still change the canonical energy convention. None of these possibilities
licenses deleting all protocol dependence.

For constant nonzero lambda0, the exact transformation is autonomous but has
U(theta-lambda0). Replacing this by U(theta) still changes the selected cosh
potential center. For lambda identically zero, the exact and replacement
actions coincide, providing a necessary limiting control.

## 7. Exact controls and missing conservation obligation

1. Constant lambda on an interval: lambda_t=lambda_tt=0. Original and
   canonical energies and fluxes agree, and their explicit work terms vanish.
   The translated potential is retained if the constant is nonzero.
2. Instantaneous zero rate but nonzero acceleration: at lambda_t=0,
   E has zero instantaneous protocol power and H_theta=E, yet
   partial_t(H_theta-E)=pi_theta lambda_tt need not vanish. This verifies
   that equality of instantaneous values does not equate their derivatives.
3. Constant nonzero rate: lambda_tt=0 does not remove the drive.
   Equation (6) has -T lambda_t/C, and (13) has -U'lambda_t/C together with
   the distinct canonical flux and momentum-energy relation.
4. Positive-rate Q control: T>0 at nonzero g, so the sign of physical
   reference work is negative for lambda_t>0. Reversing it contradicts
   W_lambda=-T and -partial_t L.
5. Kinetic mutant: using sigma theta_t/C instead of pi_theta misses the
   term -sigma lambda_t/C and fails the exact Legendre relation.
6. Potential mutant: replacing U(theta-lambda) by U(theta) fails (9) and
   the constant-nonzero-lambda control for the cosh potential.
7. Boundary mutant: fixed chi walls become driven theta walls. Fixing both
   coordinate descriptions to time-independent wall values is not equivalent.
8. All local identities use continuity, Euler and BOTH field equations.
   An arbitrary off-shell scale or matter history leaves equation residuals;
   no such history is counted here as evidence of conservation.

The exact missing obligation for a closed system is a dynamical source whose
energy/flux absorbs +T lambda_t/C locally (or +lambda_t integral T/C in the
uniform global-protocol description). If one merely postulates a uniform
driver action L_drv(lambda,lambda_t), its necessary equation would be

 d/dt partial_Ldrv/partial_lambda_t-partial_Ldrv/partial_lambda
          =integral_V T/C,

and its energy would gain +lambda_t integral T/C, canceling (7)'s explicit
work when all boundary transfers are also accounted for. This is an
obligation, not a supplied driver action: no kinetic sign, local stress,
metric coupling, vacuum interpretation or desired history follows.
A uniform mechanical driver is not automatically a local covariant sector.

## 8. Reference/history bookkeeping and scope

Use the fixed canonical anchor a_c=9.3619e-11 m/s² and
beta=(1.1279e-10)/a_c. Constant-vacuum references are separately lambda=0
and lambda=log beta. Separate prescribed H-history comparisons are
lambda=log E(z(t)) and lambda=log beta+log E(z(t)), with
E²=.315(1+z)^3+.685. The constant shift changes T through actual a but adds
no lambda_t. A frozen history value is constant and has no protocol work.
For a time-dependent choice, z(t) is an external input, not solved here.
No expansion equation or Hubble-friction term is imported.

J,S0,K,v_chi, matter parameters and physical units remain fixed. The core
reference identity a_ref=kappa c sqrt(G rho_Lambda,ref) would require its
own interpretation for a time-varying rho_Lambda,ref. Actual a also depends
on chi. The previous literal constant-vacuum actual-scale incompatibility
is not repaired by either a prescribed protocol or theta relabeling.

The result is an exact conditional energy-accounting statement for the chosen
diagnostic action. It is not a new cosmological mechanism, a proof that a
prescribed H(t) solves any equation, an M local action, filtered-MONO transfer,
physical metric/photon completion, empirical fit or full-theory closure.
No numerical experiment or manufactured solution was necessary or performed.
