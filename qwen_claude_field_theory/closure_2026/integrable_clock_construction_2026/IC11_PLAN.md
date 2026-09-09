# IC11 constructive repair and empirical interface

Base checkpoint: `347950889570a839af41f6bef0c8bcba7531d02a`.
Previous goal turn: progress, because new executable evidence identified an
early-time clock kinetic failure inside the actual IC10 plateau.
The full target remains [FRIED_CHICKEN_SPEC](../FRIED_CHICKEN_SPEC.md), not a
vacuum-only or homogeneous-only theory. The user authorized continued execution
and scoped commit/push, including parallel work. Existing unrelated edits remain
untouched.

## Design and execution

1. **Pressure repair**: test a convex additional pressure depending on the
   Einstein-frame clock kinetic invariant alone. Preserve the original U and
   the vacuum auxiliary equation; recompute energy, expansion and activation.
   Owner: clock_pressure_repair. New `ic11_clock_pressure.py`, its test and note.
2. **Transition completion**: continue the full momentum-dependent switch,
   including both switch derivatives. Derive the finite-wave auxiliary pencil;
   repair its spatial quadratic form and tensor coefficient, then test the
   scalar momentum Hessian rather than assuming positivity. Owner:
   transition_completion; `ic10_transition.py`, its test, and new
   `ic11_transition_completion.py`, its test and note.
3. **Matter gate**: add an ordinary massless canonical scalar minimally coupled
   to the physical metric. Derive its coupled kinetic/gradient matrices after
   algebraic auxiliary elimination. Test an auxiliary-curvature correction
   `-b*(P0_w)^2/2` that preserves the vacuum stationary pressure but changes the
   response to matter. Owner: root; new `ic11_matter_gate.py`, its test and note.
4. **Empirical interface**: use the exact exponential law on X-COP and the
   mass-ratio-correct deep-MOND two-body law on the existing galaxy-pair sample.
   Distinguish required source profiles from sources predicted by the clock.
   Owner: cluster_pair_target; separate `cluster_pair_clock_target_2026/`.

Each computation gets tests before implementation, an actual executable run,
negative controls and explicit range/nonclaims. Finite samples are not a global
proof. The branches are not automatically composable: a successful pressure
repair changes the homogeneous transition equations. Recompute that combined
action before claiming combined success. After source review, run the relevant
existing tests, record source hashes/commands/exits, and push only owned files.

## Matter-gate test contract

For `L=P0(S,w)+f(exp(-2S)/2)+exp(2w)*Y-b*P0_w(S,w)^2/2`, use
`X=exp(-2S)/2`, solve `L_w=0` in `-S/2<w<0`, and compute
`K=L_vv-L_vw*L_ww^-1*L_wv` for `v=(sqrt(2X),sqrt(2Y))`.
The spatial matrix is `D=diag(L_X,L_Y)`. Tests compare to independent numerical
derivatives in velocity coordinates, check the vacuum pressure invariance,
recover the uncoupled matter cone at Y=0, and reject roots outside the chart.
Eigenvalues of K and of the generalized pair (D,K) are computed, never inserted.
