# G03 continuation: full equations and a conditional causal failure

2026-09-05. **Overall OPEN.** The fully varied C-H action now has a
conserved-source causal failure on an explicitly specified noncompact
cylindrical branch. The original closed-leaf domain and realization of
the test source by the specified ordinary matter remain unresolved.
This is stronger than the earlier principal-block warning, but it is not
a universal MOND no-go, a physical mode count, or closure of T-A.

The action, q kernel, clock and fields are those of ACTION.md. No f32
operator has been added. The current f32 is a different aether-scalar
action; its output still records incomplete second-order normalization,
nonzero full preferred-frame parameters, and an unproved mode claim.
Its finite PPN ladder cannot supply equations or health for C-H.

## 1. Full localized variations

In this section all quantities are dimensional as in ACTION.md. Define
V_mu=D_mu U-a_mu, w_mu=D_mu W_b, q_b=q(w^2/alpha^2),
q'_b=nu(|w|/alpha)-1, and f_mu=q'_b w_mu.
After a spatial integration by parts the complete auxiliary Lagrangian is

    L_loc = 2 V^2 + 2 alpha^2 q_b
          + integral_0^b dz [L partial_z W + D_mu L D^mu W
                             + L a_mu D^mu W]
          + lambda_0(W_0-U).

This identity uses Delta_h W=nabla_mu(D^mu W)-a_mu D^mu W.
On closed leaves there is no spatial boundary term; the tangent flux has
zero normal contraction on temporal caps. It is the same action, not an
additional operator.

The auxiliary equations remain

    W_z=Delta_h W,  W_0=U,
    L_z=-N^-1 Delta_h(N L),
    L_b=4 N^-1 D_i(N f^i),  lambda_0=L_0,
    -4 N^-1 D_i(N V^i)-lambda_0=0.

Define the full lapse derivative, before auxiliary constraints are imposed,

    H = 2 V^2 + 4 V.a + 4 D_i V^i + 2 alpha^2 q_b
        + integral dz L(W_z-Delta_h W) + lambda_0(W_0-U).

Define the spatial metric derivative

    P^{ij} = (1/2) h^{ij} L_loc - 2 V^i V^j - 2 q'_b w^i w^j
             - integral dz [D^{(i}L D^{j)}W + L a^{(i}D^{j)}W].

Parentheses mean symmetrization with factor 1/2. The last integral is the
full localized heat stress. Dropping it freezes the metric dependence of
the filter and changes the equations. Define epsilon=-H/2 and
B_mu nu=epsilon n_mu n_nu+P_mu nu, with P fully spatial. The complete
metric equations, together with the listed auxiliary equations, are

    G_nn - Lambda = (8 pi G/c^4) T_m,nn + epsilon,
    G_ni          = (8 pi G/c^4) T_m,ni,
    G_ij + Lambda h_ij = (8 pi G/c^4) T_m,ij + P_ij.

These are projections of the varied metric equation, not just static
equations. In adapted coordinates every auxiliary term is independent of
the shift and of physical-time metric velocities. This derives the zero
auxiliary momentum projection; it is not an assumed absence of physics.
The Einstein-Hilbert metric variation and boundary prescription are retained.

For an explicit **off-shell clock equation**, let dot F=n^mu partial_mu F
and introduce the full covector

    A_mu = -4 partial_mu U + 4 a_mu
           + integral dz L partial_mu W,

    J_mu = 4 dot U partial_mu U + 4 q'_b dot W_b partial_mu W_b
           + integral dz [dot L partial_mu W + dot W partial_mu L]
           + A^rho nabla_mu n_rho - nabla_nu(n^nu A_mu).

The clock variation is exactly

    E_tau = nabla_mu[h^{mu nu} J_nu / sqrt(X)] = 0.

It follows by substituting delta n_mu=-h_mu^nu partial_nu(delta tau)/sqrt(X)
before integration by parts. The normal component of A_mu must not be
discarded: delta a_mu need not be spatial when n is varied. This is a
complete current expression, rather than a schematic delta S/delta tau.

On the auxiliary equations, the diffeomorphism identity and the independent
matter Ward identity reduce this clock equation to

    dot epsilon + K epsilon + K_ij P^{ij} = 0.

The spatial part is D_i P^{ij}+a_i P^{ij}+epsilon a^j=0, a spatial
diffeomorphism identity on the auxiliary equations. Together these express
nabla_mu B^{mu nu}=0. They do not assert that epsilon is freely prescribable
on every branch; that is tested below.

The new script compares this off-shell clock current directly to a clock
variation of L_loc on smooth time/space grids. Errors are <=1.26e-11 at
32 and 48 points per direction. Independent lapse and conformal spatial
variations give errors <=1.75e-11. Omitting the displayed heat stress leaves
a resolved error about 1.509e-4. These are bounded float64 checks of the
derived variations, not an unrestricted nonlinear well-posedness proof.

## 2. An actual nonzero solution and its domain qualification

A uniform nonzero gradient of a real single-valued U cannot live globally
on the original compact leaves. Rather than call the old affine flat
background a solution, the following exact Einstein-Maxwell branch is
constructed. It uses the **same action with an explicit domain extension**
to complete leaves R x S^2. This extension is not a proof for the original
compact topology.

Use dimensionless lengths alpha times physical length and dimensionless
time alpha c t. Set alpha=1 in the following formulas; Lambda means
Lambda/alpha^2, b=(alpha xi)^2/2. Let y>0,

    p=s=y(1-exp(-y)),  f=y exp(-y),  q=q(s^2).

Choose a lower positive root of

    a=p+f exp(a^2 b),  V=p-a,  E=exp(a^2 b),

and take

    ds^2=-exp(2 a x) dt^2 + dx^2 + R^2 dOmega^2,
    tau=t,  U=p x,  W(z,x)=p x,
    L(z,x)=4 a f exp[a^2(b-z)],  lambda_0=L(0,x).

The intrinsic heat operator is the complete-cylinder heat semigroup.
It preserves affine U and acts on exp(a x) by exp(a^2 b) exp(a x),
which fixes the lapse-weighted multiplier solution. This defines the
non-L^2 background extension explicitly. Perturbations use this fixed
background and heat operator, with bounded/decaying spatial responses.
Infinite background action is subtracted. Admissibility under a stronger
weighted finite-energy boundary condition is not assumed proved.

The auxiliary sources are constants in an orthonormal frame:

    epsilon = a^2-p^2-q,
    P_parallel = -epsilon,
    P_perp = V^2+q+2 p f [exp(a^2 b)-1].

Choose

    R^-2 = a^2+2 Lambda-2(q-p f),
    rho_EM = a^2+Lambda-P_perp > 0.

Here rho_EM denotes (8 pi G/c^4) times physical Maxwell energy density,
divided by alpha^2. A source-free electric field along x has normalized
stress (rho_EM,-rho_EM,rho_EM,rho_EM). Its constant orthonormal magnitude
sets rho_EM. Maxwell's equation is satisfied because
partial_x[sqrt(-g) F^{xt}]=0. The Einstein tensor is

    G_nn=R^-2,  G_xx=-R^-2,  G_perp=a^2.

Thus every background metric, clock, auxiliary and Maxwell equation is
satisfied. The script derives the Einstein tensor from Christoffel symbols;
it does not assign it. Four backgrounds at alpha xi=.2, Lambda=.03 have
positive R^-2 and Maxwell energy density, with equation residuals below
1e-11. The values y=2.0569 and 2.4781 are also inspected; they are parameter
values here, not a claimed Galactic field conversion on this curved branch.

The dimensionless .2 filter-width examples are not the G02 Solar-System
parameter band. A separate 70/90-digit transfer check below considers
alpha xi=1e-8 and 1e-12 without relying on cancellation-prone float64
constraint solves. Neither a0 footing supplies a different action or kernel.

## 3. The earlier integration datum survives the exact equations

Consider spherical perturbations with radial spatial gauge h_xx=1,
areal radius r=R exp(zeta), lapse N=exp(a x+n), shift N^x=v,
and U=p x+u. On the static background the quadratic kinetic term is

    (R^2/N)[-4 chi_dot zeta_dot + 4 v' zeta_dot - 2 zeta_dot^2],

where chi is retained before imposing the radial gauge. The auxiliary
action has no shift term. The exact linear momentum constraint in vacuum
is partial_x(N^-1 zeta_dot)=0. For localized data it gives zeta_dot=0.

Since the exact background satisfies epsilon+P_parallel=0, the full
clock equation linearizes to

    partial_t delta C = 0,
    delta C = delta epsilon + 2(epsilon+P_perp) zeta.

The Hamiltonian equation and Maxwell's fixed-charge perturbation then give

    delta C = 2(k^2+a^2) zeta

for source-free Fourier perturbations with k!=0. Both epsilon and r are
constant on the background, so their perturbations, and this combination,
are invariant under infinitesimal coordinate changes. This is not merely
a gauge-dependent lapse integration constant.

The actual lapse/U constraints are solved with the full heat response.
Writing sigma=exp(-b k^2), the endpoint heat perturbation is

    delta W_b = sigma u + 2 i p zeta (1-sigma)/k.

The second term is the metric variation of the intrinsic Laplacian:
delta Delta_h W_bar=2 i k p zeta. It cannot be removed by retaining only
the scalar filter. The multiplier transport uses (a+i k)^2 and the
nonconstant background L(z), including lapse and volume variation.
All its moments are integrated analytically in the script.

Twenty background/wavenumber cases solve both constraints, and the
independently evaluated radial metric equation agrees to <=2.3e-14 in
the specified normalized residual. Nonzero zeta gives nonzero delta C;
the auxiliary constraints do not simply set it to zero on this branch.
This is evidence for physical initial-data content, **not a generic DOF
integer, ghost diagnosis, or a count on other backgrounds**. The angular
metric equation determines the shift evolution, as used next.

At k=0, constant u and n are normalization freedoms and the 2x2 block
must not be inverted. With fixed Maxwell charge the radius equation is
4(2 rho_EM-R^-2) zeta=0, nondegenerate in the tested backgrounds. Changing
the background charge or affine slope is a change of boundary data.
Neither the k!=0 result nor the y=0 singular tangent is continued through
this exceptional sector.

## 4. Retarded curvature response to a conserved external source

Now add an externally prescribed linear conserved stress perturbation,
with all components normalized by 8 pi G/c^4. For any smooth compact
function Z(t,x), set

    rho_s = 2(-Z_xx+a^2 Z),
    q_s   = 2 exp(-a x)(Z_tx-a Z_t),
    p_x,s = 2[-exp(-2a x) Z_tt+a Z_x-a^2 Z],
    p_perp,s = 0.

Direct symbolic differentiation gives

    exp(-a x) rho_s,t + q_s,x + 2a q_s = 0,
    exp(-a x) q_s,t + p_x,s,x + a(rho_s+p_x,s) = 0.

These are the full background matter conservation equations in this
sector. Choose Z to vanish for t<=0 and set the initial delta C to zero.
The clock, Hamiltonian and momentum equations then consistently give
zeta=Z, with the declared decaying spatial prescription. Maxwell remains
on its fixed-charge solution. The independently checked radial metric
equation holds with p_x,s; the angular equation fixes v_t'. Thus the
calculation uses all scalar metric equations, not the lapse alone.

In particular, the 2D radial curvature variation is independently derived
from the perturbed metric as

    delta R^(2) = -2[n_xx+2a n_x+exp(-2a x) v_tx].

The radial orthonormal tidal curvature is R_(n x n x)=-R^(2)/2. Using
the angular metric equation, its response is

    delta R_(n x n x)
       = delta P_perp - 4 rho_EM Z
         + exp(-2a x) Z_tt - Z_xx - a Z_x + p_perp,s.

Every term except delta P_perp is local in the compact source. Outside
its support the measurable response is exactly delta P_perp. In local
GR the auxiliary term is absent and the exterior response is zero in
this test. This control prevents confusing an elliptic metric potential
with a physical signal.

Solving the full C-H constraints gives delta P_perp(k)=T(k) Z(k).
T contains both the heat variation and the weighted multiplier stress.
It is instantaneous in physical time. Its nonconstant transfer and its
nonlocal spatial action are computed rather than assumed. For the y=2
example, T(.1) is about 3.6432-.01449 i while T(50) is approximately
-16.92299+.00146 i. Opposite wavenumbers are complex conjugates.

The spatial source is the second derivative of the smooth compact bump
exp[-1/(1-(x/.45)^2)] on |x|<.45, and zero outside. It has zero continuum
mean. The numerical DC component removed before inversion is reported
explicitly: from 9.6e-6 on the coarsest mesh down to 8.2e-9 on the finest.
This is a finite quadrature correction, not a solved k=0 equation.

Four box/mesh controls give the radial curvature at x=1, per unit temporal
source factor, as

| Box length | Mesh | Exterior curvature |
|---|---:|---:|
| 12 | 1024 | -54.45178 |
| 12 | 2048 | -54.48737 |
| 18 | 2048 | -54.47578 |
| 18 | 4096 | -54.49183 |

The source and all its derivatives vanish at that observation point.
The shortest coordinate null travel time from its support is
integral_(.45)^1 exp(-a x) dx=0.13351909. A smooth temporal source can
already be nonzero at t=.005 while vanishing for t<=0. The computed
instantaneous curvature is therefore outside the metric causal future.
Amplitudes can be uniformly reduced to remain in linear response.

At alpha xi=1e-8 and 1e-12, an independent 70/90-digit implementation
finds the same qualitative nonlocal transfer: T/alpha^2 is near 2.16536
at small k xi and approaches -15.48075 at large k xi. The crossover
moves toward larger k xi; finite source/support convergence was not
repeated at these tiny parameter values. A first development assertion
incorrectly required a resolved difference between two points on the
low-k plateau. It failed and is preserved; comparing the explicitly
tested low- and high-k ranges implements the intended nonconstancy check.
No kernel or numerical tolerance was changed.

## 5. What fails, and what is still not proved

**The conserved-external-source causal criterion fails on this cylindrical
response problem**, conditional on the stated Fourier/decaying boundary
prescription and the numerical convergence controls. This is a physical
curvature response with the shift retained; it supersedes the earlier
unconstrained-wave toy as the strongest adverse evidence for C-H.

It does not yet establish DEAD for the complete original specification:

- R x S^2 is an explicit extension of the earlier compact domain. Its
  fixed background and response prescription must not be silently
  substituted for the original closed-leaf problem. Stronger weighted
  finite-energy conditions or another inverse prescription need their own
  admissibility and response analysis.
- A conserved external linear stress tensor is a necessary source-consistency
  check, but this constructed source has not been realized by the explicit
  particle/Maxwell matter equations. Its signed perturbation is not itself
  a positive material density. Whether two admissible ordinary-matter
  histories realize such a difference remains an essential physical gap.
- Fourier-box checks are not a certified continuum error bound or a
  nonlinear initial-value proof. The exact cylinder is also a special
  constant-radius branch, not a generic Galactic background.

Thus **G03 OPEN, with a conditional causal FAIL** is the strongest supported
status. If the cylindrical extension and arbitrary conserved external
linear sources are admitted as required causal tests, that version of C-H
is rejected by this test. This does not reject every double-filter or
MOND completion. No action change is proposed to conceal the result.

The next decisive work is narrow: determine whether the source and
boundary prescription are admissible for the intended same-action
matter/domain, or reproduce the curvature-support failure with two
ordinary-matter histories on a permitted background. Resolve this before
any PPN tuning or full Dirac calculation. The full metric/clock variation
is now available for that task.

## 6. Reproduction and portability

Run the two new scripts from the repository root using python3:
g03_full_variation.py and g03_retarded_screen.py in this study directory.
Their manifests contain complete portable commands, source hashes,
arithmetic and bounds. The full-variation diagnostic has 9 checks; the
retarded screen has 8 after the high-precision control was added.
Successful diagnostic execution uses rc=0 even when the physical causal
criterion is FAIL. The result JSON distinguishes these meanings.

Machine-specific absolute prefixes have been removed from the serialized
handoff/evidence, and future producer commands use repository-relative
references or dynamic resolution. Historical content hashes are retained
in portability_record.json alongside hashes of the rewritten display
bytes. Scientific numbers and failed-run history are not deleted.
The fresh G03 inventory authenticates the current displayed files.

No commit or push was requested or performed in this continuation. All
changes are confined to the G03 study. The Mathbox computation/proof audit
distinctions are used throughout; the displayed equations and new prose
also received a conservative mathematical self-review.
