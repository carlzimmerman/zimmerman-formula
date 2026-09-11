# Exact initial-slice reduction of the fixed cubic clock action

Base `62a6ee68703f8c89e6bbf66eb1a69b114dc18a83`. Verdict: **computationally
verified formal rational-jet identities under the stated slice restrictions**.
This is an initial-data calculation, exact in the baryon density amplitude;
it is not a spacetime solution, a full constraint classification, or a MOND
theorem. The parent directory separately solves the initial constraint BVP.

## Conventions and the clock equation before restriction

Use the action in `../../cubic_background_completion/README.md`, signature
−+++, constant gamma, and positive extrinsic curvature on expansion. Put
`mu=M²`. The metric is

    ds² = -N² dt² + A²(dr+v dt)² + R² dOmega².

`A` here is the radial metric coefficient, never the homogeneous shift charge.
All action densities are per solid angle; physical integrals include `4 pi`.
The clock gauge `tau=t` requires its gradient to be timelike and future-oriented,
with `N>0`. Let `u=chi_r`, `Q=(chi_t-vu)/N`, `Y=u²/A²`, `K=k+2h`, where
`k=Kr` and `h=Ktheta`. Partial derivatives `P_t`, `P_tX`, `P_tt` hold **X fixed**;
`W_t` holds Y fixed. All slice coefficients below are evaluated at `(X,Y)=(q²,0)`.

Variation of tau at fixed metric and chi gives

    E_tau = P_t-V_t+s W_t-div[W n-2Q W_Y Dchi],
    s = sqrt(-grad(tau)²).

In this clock gauge the explicit `W_t` terms cancel, leaving `E_tau=-T`, with

    T = V_t-P_t+WK-2 W_Y kY-2Q Jsp,
    Jsp = (A R²)^(-1) d_r[R² W_Y u/A].

For example, the direct density variation is

    N A R² E_tau = N A R²(P_t-V_t)+A R² W_t
                  -d_t(A R² W)+d_r[v A R² W+2N R² Q W_Y u/A].

The script checks this against the displayed T for general spherical fields,
before any gradient is set to zero. The constant cubic term has no explicit
tau variation; it enters the preservation equation through the metric and chi
equations. Matter is independent of tau and chi.

## Initial constraints and geometry

At one time set `R=r`, `u=0`, `Q=q`, `k=h=H`, and `v=0`, with q,H spatially
uniform and equal to the repaired background values. The shift can be continued
with `v_t=0` for this calculation. Do **not** impose `R=r` at later times:
`R_t=N r H` and `A_t=N A H` on the initial slice.

Momentarily normal-rest dust has `theta_r=0`, future normal velocity U_d=1,
and normal energy density equal to its proper rest density `rho_b(r)`. Its
lapse source is `-A r² rho_b`; its shift and spatial stress sources vanish.
The exact Hamiltonian, momentum and tau constraints reduce to

    R3 = 2 rho_b/mu,       E_v = 0,       V_t-P_t+3HW = 0,
    R3 = (2/r²)[1-A^(-2)+2r A_r/A³].

Define `I(r)=integral_0^r rho_b(s)s² ds`. Regularity integrates the first
constraint exactly:

    f=A^(-2)=1-I/(mu r).

Require `f>0`; crossing f=0 leaves this spatial chart. For smooth even density,
`f=1-rho_b(0)r²/(3mu)+O(r⁴)`, so A(0)=1 and A_r(0)=0. For compact support,
the exterior has `f=1-M_coordinate/(4 pi mu r)`, where
`M_coordinate=4 pi I(infinity)`. This is **not** the proper rest mass
`4 pi integral A rho_b r² dr`; the distinction matters at nonlinear amplitude.

## Actual time equations and lapse preservation

Write

    J = 2q P_X-6 gamma Hq²,
    B = 2P_X+4q²P_XX,
    Bhat = B-12 gamma qH+6 gamma²q⁴/mu,
    C = 2q P_tX+3 gamma q²W/mu,
    Theta = H+gamma q³/mu,
    S = W-2q²W_Y,
    L = Delta_h N = [N_rr+(2/r-A_r/A)N_r]/A².

Directly reducing the varied metric trace and chi current gives

    -2mu K_t-6 gamma q²Q_t = -2mu L+N(3qJ+rho_b)+3W,
    -2 gamma q²K_t+(B-12 gamma qH)Q_t
        = -2 gamma q²L-3NHJ-2q P_tX.

The coefficient matrix for `(K_t,Q_t)` has determinant `-2mu Bhat` and inverse

    [[-(B-12 gamma qH)/(2mu Bhat), -3 gamma q²/(mu Bhat)],
     [-gamma q²/(mu Bhat),                       1/Bhat]].

It is not described as a physical reduced kinetic Hessian. Assuming
`mu != 0`, `Bhat != 0`, the exact solution is

    Q_t = -[N(3J Theta+gamma q²rho_b/mu)+C]/Bhat,
    K_t = L-[N(3qJ+rho_b)+3W]/(2mu)-3 gamma q²Q_t/mu.

In particular `Q_t` has no Laplacian of N. However `chi_t=Nq` generates
`chi_tr=q N_r` and `chi_trr=q N_rr`. Differentiating the full tau equation
**before restricting** gives

    0 = T_t = V_tt-P_tt+3H W_t+W K_t-2q P_tX Q_t-2q²W_Y L.

The last term is essential: `d_t Jsp=q W_Y L`. Omitting it incorrectly changes
the lapse principal coefficient from S to W. The current check likewise
retains the generated `d_t(Delta_h chi)=q L` and the braiding radial flux.
All terms involving the arbitrary `N_t` cancel.

Elimination gives the exact initial lapse equation

    S Delta_h N+(delta0+c_rho rho_b)N+F0=0,
    delta0 = 3J[-Wq/(2mu)+C Theta/Bhat],
    c_rho = -W/(2mu)+gamma q² C/(mu Bhat),
    F0 = V_tt-P_tt+3H W_t-3W²/(2mu)+C²/Bhat.

For the repaired background, the checked identities include

    P_X=J/(2q)+3 gamma qH,    P_XX=(B0-J/q)/(4q²),
    P_t=-J qdot-6 gamma q²H qdot,
    P_tX=(-3HJ-B0 qdot)/(2q)+3 gamma(H qdot+q Hdot),
    W=U-2 gamma q²qdot,      Hdot=-(qJ+U)/(2mu),
    V_t=-J qdot-3HU.

The differentiated background tau identity includes the chain term
`2q qdot P_tX`. It gives `F0=-delta0`, rather than setting the source to zero.
Thus the BVP used in the parent directory is

    S Delta_h N+(delta0+c_rho rho_b)N=delta0.

The zero-baryon control has f=1 and solves this equation with N=1, recovering
`Q_t=qdot`, `K_t=3Hdot`. At gamma=0 the independent first-derivative action
control is reproduced, including `c_rho=-W/(2mu)` and the same S. With nonzero
density a unit lapse is generally **not** a solution.

## Individual metric equation and actual dust acceleration

The tracefree equation, also checked against the varied action, is

    k_t-h_t = [N_rr-(A_r/A+1/r)N_r]/A²
              -N[A_r/(A³r)-(1-A^(-2))/r²].

Combining it with the trace and Hamiltonian yields

    h_t = f N_r/r-N[I/(2mu r³)+qJ/(2mu)]-W/(2mu)-gamma q²Q_t/mu.

Direct contraction of the metric's Christoffel connection with the initial
dust geodesic gives `d²R/ds_d²=r(h_t/N+H²)-f N_r/N`. Relative to the
homogeneous geodesic areal acceleration, the inward acceleration is therefore

    g_areal = I/(2mu r²)
              +r[U(1-N)+2 gamma q²(Q_t-qdot)]/(2mu N).

This is an invariant areal-radius diagnostic of the chosen initial branch,
not a stationary rotation-curve or universal algebraic force law. It differs
from the acceleration relative to clock observers, `-N_r/(N A)`.
The dust equations independently give `theta_rt=N_r`,
`(A r² rho_b)_t=0`, and `rho_b,t=-3NH rho_b` on the slice. The generated
radial velocity and later evolution must not be suppressed.

## Boundary hypotheses, scope, and evidence

At a regular origin use `N_r(0)=0`. If `S != 0` the central series satisfies
`6S N2+(delta0+c_rho rho_b(0))N0-delta0=0`. An asymptotically background
exterior would require `N->1`; the finite-ball parent calculation instead
imposes `N(r_outer)=1`. This is specified boundary data, not a derived
cosmological matching condition. Even outside compact matter the lapse obeys
an equation on the curved exterior f, not the flat Laplacian exactly.

If `S>0`, `-delta0>0`, `-c_rho>0`, and f stays positive, the finite-ball
maximum-principle bounds used by the parent are consistent with this equation.
They concern the chosen uniform-clock, normal-rest initial branch; neither
that argument nor this certificate excludes a distinct later-time or
quasistatic branch. No full spatial constraint algebra, global evolution,
caustic avoidance, asymptotic matching, or empirical theory follows here.

The reproducible commands and SHA-256 input/output hashes are recorded in
`run_001/manifest.json` and `run_002/manifest.json`. The executions observed
HEAD `1aa856e618036168d2998ae1ab37c73ca7a9348d` after the parent task advanced
the branch; the five authoritative action/matter input files are unchanged
from the starting base above. Both manifests validate with current inputs.

| Run | Actual child command (from repository root) | Exit | Result |
|---|---|---|---|
| 001 | `python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_infall_2026/slice_action/derive.py` | 0 | 37 slice identities; 36 imported action identities; 8.95 s |
| 002 | `python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_infall_2026/slice_action/test_slice.py -f` | 0 | 4 tests; 9.11 s |

The runs use Python 3.9.6 and SymPy 1.14.0, with a 45-second wall cap,
35-second CPU cap, and a cooperative single-thread environment cap. No
memory or CPU-affinity cap was imposed. Both manifest-validation commands
exited 0. The derivation SHA-256 is
`b678759bec545be5e2757c9c284f3e4d56d6d159fb2437eb3727edd952c15617`.

The first test-only revision
failed as expected because the derivation was absent; the acceleration test
also failed before its checks were added. A tracefree residual convention
was corrected after its explicit nonzero residual showed that covariant-metric
variation carries `-mu G^r_r`; the zero set and reported shear formula did not
change. Final commands, exits and identity counts are reported with these runs.
No files outside this directory were changed by this subtask. Mathbox
proof-audit, computation-audit, and conservative mathematical self-review
determine the distinction between exact identities and unproved physics.
