# TP03: finite vacuum diagrams and phase-current matching

The missing finite terms have now been calculated in the specified rigid
SU(5) model. They move the native-phase stability boundary but do not remove
its pressure failure at the two weak trial couplings tested here.

| Fixed matching-scale e | One-loop boundary X/Xmin | Finite matched boundary X/Xmin | Matched endpoint Pex/epsilonex | Matched cs^2 at X/Xmin=1.3 |
|---|---:|---:|---:|---:|
| 0.01 | 1.21339321 | 1.21394372 | 0.61414732 | -0.56038355 |
| 0.03 | 1.21339321 | 1.21818639 | 0.60916684 | -0.49404151 |

Each ratio uses its own corrected vacuum minimum. At e=.03 the minimum is
0.992790864 times its one-loop position; at e=.01 it is 0.999176076 times
that position. The endpoint has zero long-wavelength sound speed and a
positive fixed-charge radial curvature. At ratio 1.2 the matched sound speed
is still positive, .07895530 and .09813812 respectively. Thus this is a
pressure-rich branch ending in a later compressibility instability. It is
not a cold halo equation of state, and it is not unstable everywhere.

These are fixed-order matching calculations: f=1, h=lambda=e and
g=sqrt(29/200)e are specified at the fixed scale
Q^2=e/31+(e Xmin_one_loop)^2. The scale is held fixed during field
differentiation. TP02's running-boundary prescriptions remain distinct;
their e was specified at its own reference scale. No RG log is added a
second time to the explicit finite graphs. All trial parameters remain
unselected physical inputs.

## What was filled in

1. **All ten finite two-loop vacuum classes.** The full component vertices
   yield SSS, SS, FFS, barFFS, SSV, VS, VVS, FFV, barFFV and pure-gauge
   graphs, including ghosts and the DRbar-prime finite vector terms.
   The known normal heavy displacement is included exactly once in the
   reduced potential. See [full graph implementation](gauge_diagrams/full.py),
   [vertex derivation](two_loop/DERIVATION.md),
   [independent gauge review](two_loop/GAUGE_FULL_REVIEW.md), and
   [reduced scale check](gauge_diagrams/run_cs/result.json).
2. **The finite one-loop phase-current coefficient.** Exact broken-SUSY
   scalar and signed-Majorana fermion vertices are used, with the Landau
   scalar/vector derivative mixing and its finite projector contribution.
   Goldstones and gaugino mixing are retained. This uses no small-F Kahler
   substitution. See [component derivation](current_matching/DERIVATION.md),
   [implementation](current_matching/current.py), and
   [current controls](current_matching/run_current/result.json).
3. **A consistent occupied heavy response.** The vacuum shift, angular
   metric shift and quartic-charge term come from the same normal-field
   square. The full finite potential and current are combined with that
   square before the charge Legendre transform. See
   [order and state](ORDER_AND_STATE.md),
   [component-to-reduced current audit](CURRENT_PULLBACK_AUDIT.md), and
   [combined current scale check](run_current_pullback_v2/result.json).

For the native phase the grand potential is

    Omega = V - F omega^2 - J omega^4/2,
    n = 2 omega (F+J omega^2).

The equilibrium condition is partial_X Omega=0; the response follows after
the fixed-charge Legendre transform. The direct finite current by itself
changes F/Ftree by about -9.00e-7 at e=.01 and -8.08e-6 at e=.03 near the
endpoint. It moves the boundary only about 4e-8 and 4e-7 in X/Xmin.
The complete two-loop potential and occupied heavy response produce the
larger shifts shown in the table. The correction has an effect; it does
not rescue the pressure verdict.

## Verification and range

[The pressure record](run_pressure/result.json) contains 48 cases: two weak
couplings, four explicitly separated truncations, three actual field-step
root solves and two interpolation grids. The 21/29-node grids span
ln(X/Xmin_one_loop) in [-.05,ln(1.4)]; independent off-node evaluations and
direct e=.01 scaling checks agree below 3.2e-10 relative. The last two
field-step roots differ by less than 3.3e-11 and interpolation-grid roots by
less than 3.3e-10. A direct pressure-versus-charge derivative agrees to
1.4e-6 relative. These are numerical convergence measurements, not rigorous
error bars on the perturbation series.

Full SU(5) supersymmetric vacuum cancellation, degenerate-basis invariance,
individual-graph e^4 scaling, Ward identities, component current UV running,
independent real-simplex sunset checks and reduced vacuum/current scale
identities pass. The complete two-loop reduced vacuum scale identity agrees
to 2.4e-8 relative; combined current scale cancellation agrees to 5.8e-12
of the individual terms. See [source conventions](SOURCE_CHECKS.md) and
[final provenance verification](VERIFICATION.json). Individual vacuum
diagrams have large cancellations, so the total is not inferred from the
size of one diagram or from residual scale variation.

An [actual spectrum check](two_loop/run_gaps/result.json) at the matched
endpoints and ratio 1.3 compares omega^2 with the smallest positive scalar,
Weyl and vector squared masses, rather than only the reference singlet mass.
The largest ratio is 1.22e-9. Exact zero modes are counted separately and
retained; this supports the massive-mode low-frequency expansion at these
four points and does not bound the gapless response.

The pressure run used one numerical thread, 29.4 seconds and about 268 MB
peak RSS. All executions are bounded local experiments. Original TP01/TP02
sources, prior law corrections, solver/seals and simulation queue are
preserved. No Git mutation or production job was performed.

## What remains open

The calculation matches the finite vacuum and local angular current terms
needed for this finite-order circular-branch equation of state. It does not
compute the complete radial kinetic action, higher-derivative/nonlocal
massless response, anomalous-charge lifetime or nonperturbative gauge/IR
dynamics. The low-momentum thermodynamic sound-speed sign does not require
the radial kinetic coefficient, but a full finite-frequency spectrum does.
The native phase still has no selected cosmological charge density. The
previous massive-mode cold window still needs an actual population and
decay/collision calculation; these phase-current graphs do not supply one.
There is no all-orders remainder bound, universal physical no-go or gravity
completion. See [handoff](HANDOFF.md) for the next concrete dependencies.

Failed checks are retained and explained in [launch history](LAUNCH_HISTORY.md).
The initial combined-current residual test normalized a vanishing analytic
answer by roundoff; its corrected normalization uses the individual graph
sizes and changes no physics. The initial builder failed JSON serialization;
its exact initial sources and failure record are retained separately.
