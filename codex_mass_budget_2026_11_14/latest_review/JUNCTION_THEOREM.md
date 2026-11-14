# A positive mass junction is not yet a conserved-current junction

Research checkpoint CJUMP_XJ1_2026_11_14. This is a new bounded mathematical
continuation, separate from the review of XJ1. It changes no frozen criterion,
lane label, manuscript or adopted model.

## Claim card and verdict

For an interior radius 0 < R < L, let C_B and C_R be nonnegative continuous,
nondecreasing cumulative cold-charge profiles on [0,L]. Assume
C_B(L) = C_R(L) = T and C_R(R) < T. Let Bar be the same continuous,
nondecreasing baryon profile on both sides. Set

    t = (T-C_B(R))/(T-C_R(R)),
    C_E(r) = C_B(r),                                  r <= R,
             C_B(R) + t [C_R(r)-C_R(R)],               R < r <= L.

**Static claim: proved as written under these hypotheses.** The junction has
no mass sheet, a nonnegative cold mass measure, total charge T, and the same
enclosed mass and spherical Newtonian force as Bar+C_B at r <= R. This does
not itself show that the source code's mode B equals the desired algebraic
force law; it proves preservation of whichever interior profile was supplied.

**Dynamic promotion: incomplete.** A profile constructed this way is not
therefore a solution of the clock-current or momentum/field equations. The
smallest additional requirement is the normal-current junction condition
below. No theorem here rules out every possible dynamical completion.

## Static proof and exact limits

The coefficient t is nonnegative. The two definitions agree at R; the
outside value at L is T. The Stieltjes measure dC_E equals dC_B inside and
t dC_R outside, with no atom at R. It is nonnegative. Consequently
M=Bar+C_E is continuous and nondecreasing. For a spherical Newtonian source,
g=GM/r^2 is continuous at R and unchanged inside. Outer shells change an
additive potential constant, not the inner force. The theorem invokes this
Newtonian spherical relation explicitly, not a full relativistic matching
theorem.

For differentiable profiles the cold densities at the interface are

    N_in = C_B'(R)/(4 pi R^2),
    N_out = t C_R'(R)/(4 pi R^2).

They are equal only if

    C_B'(R)/(T-C_B(R)) = C_R'(R)/(T-C_R(R)),

when both remaining charges are positive. A density jump is allowed by
Poisson's equation; continuity of enclosed mass does not force continuous
density. It also does not force a singular mass sheet.

At C_B(R)=T the outer cold density vanishes; at C_R(R)=T the displayed t is
undefined. These are degenerate cases requiring separate definitions.
R=0 reproduces the reference only when C_B(0)=C_R(0)=0. R=L can be defined as
the interior profile. XJ1 has explicit branches for these endpoint cases.

## Conserved-current theorem

Let a continuous spacetime metric and an interface F(t,r)=r-R(t)=0 be given.
Assume the current is piecewise smooth, finite on both sides, and contains
no delta-function surface charge or surface current. Write [A]=A_out-A_in.
Taking the distributional divergence of

    J = J_in H(-F) + J_out H(F)

gives the interface delta coefficient [J^mu] partial_mu F. Thus the necessary
condition for local conservation is

    [J^r] - Rdot [J^t] = 0.

This is exact for a conserved vector current, independently of the gravity
law. In curved coordinates it follows from the divergence of sqrt(-g) J;
continuity of the metric removes the common surface volume factor.

QX17's actual current is

    J^mu = n^mu rho_Q - lambda P^mu/Q,
    rho_Q = div[(1+gamma_L Pi_+)P]/Q + mu_K^2(Q-1)/K.

This is E3 of `closure_2026_11_06/QX17_covariant_field_equations/RESULT.md`.
The exact condition therefore is [J^mu] partial_mu F=0 with this full
current. The energy density in E4 is a different expression. Replacing
rho_Q by arbitrary fitted mass density, or discarding lambda P/Q at a thin
transition without an error estimate, would not establish this condition.

There is a useful exact restriction. QX17 E2's normal equation is

    lambda = (1+gamma_L Pi_+) n^mu partial_mu ln N_lapse
             + gamma_L n^mu partial_mu Pi_+.

In an exactly stationary interior with clock flow aligned with the timelike
Killing flow, the lapse and polarization divergence are constant along n.
Consequently lambda_in=0 exactly. In adapted static coordinates n_in^r=0,
and orthogonality n.P=0 gives P_in^t=0. Thus J_in^r=0 and
J_in^t=n_in^t rho_Q,in. This statement requires stationarity of the fields,
not merely a snapshot with radial velocity zero.

For a stationary interface the exterior must satisfy

    lambda_out P_out^r/Q_out = n_out^r rho_Q,out.

If the exterior is specifically polarization-free dust (P_out=0), positive
charge and inward n_out^r are incompatible with that stationary junction.
This restricted no-go uses the exact current. It does not assume every
XJ1 reference-density snapshot is polarization-free, which XJ1 never solves.

For a moving interface with this stationary interior, the required exterior
polarization flux is more generally

    lambda_out (P_out^r-Rdot P_out^t)/Q_out
      = rho_Q,out (n_out^r-Rdot n_out^t)
        + Rdot n_in^t rho_Q,in.

This is a concrete boundary condition for the missing field solution.
If P_out^r-Rdot P_out^t is nonzero, it fixes the required lambda_out/Q_out;
that value must also satisfy E2, the metric/stress equations and the
constitutive law. It is not a freely tunable sink. If the denominator is
zero, the displayed right side must vanish without this channel.

COL1 derives the weak-field, gamma_L=0, Newtonian reduction

    N = mu_K^2 h/K + div P,
    partial_t N + div(N v) = 0,
    Laplacian Phi = 4 pi G (rho_b+N).

Only in that stated regime is the same N both the leading gravitating
cold density and a purely advected charge. The omitted lambda P/Q and W
terms are post-Newtonian for the smooth regime analyzed in COL1; no such
smallness proof is supplied here for a sharp transition layer.

For this advective reduction the condition becomes

    N_out(v_out-Rdot) = N_in(v_in-Rdot).

For a standing interior v_in=0 and N_out>0,

    v_out = Rdot (1-N_in/N_out).

Consequences, each conditional on pure advective charge and no surface
reservoir:

1. A stationary interface (Rdot=0) cannot join a standing interior to
   inward flow with N_out>0. It requires v_out=0.
2. An outward-moving interface (Rdot>0) with inward outer flow requires
   N_in>N_out. If N_in<N_out it requires outward flow.
3. If N_in=N_out>0, a finite interface speed cannot connect unequal
   velocities.
4. A surface reservoir removes the first obstruction by accumulating
   charge. Its total charge S obeys

       Sdot = 4 pi R^2 {N_in(v_in-Rdot)-N_out(v_out-Rdot)}.

   With stationary boundary and static interior, Sdot=-4 pi R^2 N_out v_out.
   Infall therefore adds positive surface charge and changes the specified
   mass profile. It cannot be silently added while retaining XJ1 unchanged.

Allowing a nonadvective flux j_extra changes the condition to
[N v+j_extra]-Rdot[N]=0. Whether QX17's full leafwise flux supplies the
required amount is an explicit open field-equation question, not a reason
to promote the advective obstruction into a full-action no-go.
For the stationary interior just derived, its Newtonian form fixes

    j_extra,out/N_out = Rdot (1-N_in/N_out)-v_out.

The profile audit supplies N_in/N_out. A tracked-halo velocity/front-speed
history and polarization solution are still needed to evaluate the right
side numerically and determine whether the required flux exists.

## Exact examples and finite experiment

For L=T=1, C_B(r)=r, C_R(r)=r^2 and R=1/2, t=2/3 and
N_in/N_out=3/2. Positive density, mass continuity and total mass all hold.
A stationary boundary with inward velocity fails current conservation;
Rdot=2 and v_out=-1 satisfy it. Current conservation alone therefore does
not exclude all moving junctions. Conversely C_B(r)=r^2, C_R(r)=r gives
t=3/2 and N_in/N_out=2/3: positive static matching requires outward outer
flow if the front grows and the inside stands still.

`check_junction.py` verifies these rational examples and symbolic identities,
then measures the actual XJ1 k=2,3 one-sided cold densities at z=0 and the
12 forest redshifts on both footings. Its slope test refines the relative
radius step from 1e-4 to 1e-5 to 1e-6. It does not assign velocities to
snapshot profiles, rerun shell trajectories or infer a halo history by
identifying equal mass-bin indices at different redshifts.

## Dependency and review record

| Obligation | Status |
|---|---|
| Static nonnegative mass/force matching under stated assumptions | Proved by direct construction |
| Distributional normal-current condition | Proved directly |
| QX17 exact-current identification | Read from E3; no new derivation of the action |
| N as gravitating, advected density | Conditional on COL1's stated Newtonian reduction |
| One-sided density values on XJ1 grid | Numerical; see run manifest and report |
| Full QX17 interface fields, stress and polarization equations | Not addressed |
| Time-dependent assembly, finite charge supply, stability, caustic selection | Open |

The static/theorem derivations are self-reviewed new work. The source-code
reading is an independent review of the pre-existing XJ1 construction. The
research route remains open: next solve the full normal-current and
constitutive matching problem for one tracked halo before another survey
gate is used as evidence of dynamical closure.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
