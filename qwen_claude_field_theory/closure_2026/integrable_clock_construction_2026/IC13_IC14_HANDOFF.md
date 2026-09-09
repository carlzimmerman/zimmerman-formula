# Current constructive handoff: IC13, IC14, early history and supernova audit

**Full theory OPEN.** Prior checkpoint `2f661ddbf` is pushed. These are
explicitly distinguished action revisions, not a union of successful tests.

## Strongest new constructive result

[IC14](IC14_MATTER_SQUARE.md) replaces the off-shell matter-response potential
by a square in the conformal auxiliary `z=exp(2w)`:

    L = F(X) - (z-z0(X))²/(2t) + zY,   t=1/10.

`F` is the IC11 vacuum pressure and `z0` is its original implicit auxiliary
root, not a fitted coefficient table. Varying the action gives the exact
unique positive root `z=z0+tY` for timelike canonical matter `Y>=0`.
This avoids the prior finite-matter fold. An exact conditional matrix argument
gives positive kinetic terms, causal aligned cones, and a nondegenerate
canonical auxiliary pair when its stated coefficient inequalities hold.
All 101 tested coefficient samples satisfy them; the relative-flow controls
also pass, without a claim for arbitrary flow or a continuous interval proof.

This is the strongest local matter construction here. It is not yet a global
phase action or a source of the required galactic MOND/lensing equations.
Its boundaries and its field-dependent coefficients cannot be ignored when
extending it. Only canonical massless matter was tested, not all baryonic fluids.

## Transition repair: exact advance and remaining failure

[IC13](IC13_SHEAR_REPAIR.md) modifies the trace-free momentum coefficient so
the scalar UV momentum Hessian becomes

    a13 = a12+d+a12²/d >= 3d/4 > 0,   d=eta(1-eta).

The apparent denominator has a proved smooth extension for this particular
switch. A matched curvature term preserves the isotropic tensor cone.
Actual variation exposes momentum-curvature mixing; a further curvature-square
term cancels its leading quartic instability. The remaining scalar speed is
still vastly too high at the tested evolving background (speed squared about
5.65e6 relative to the physical light cone). IC13 is therefore not viable as
the final theory. Its momentum, gradient and time-dependent terms must be
controlled together, rather than repaired by changing one inferred speed.

IC14's matter result has NOT been inserted into IC13 and revaried. No combined
health, global constraint count or cosmology claim is made.

## Carl's early-universe priority: a quantified missing calculation

Carl explicitly asked whether the mathematics before cosmic recombination
must be done. This prompted the following early-history scope check; the
physical importance of recombination is not claimed as a new discovery.

IC14 preserves the IC11 vacuum pressure. Its full inherited eta=1 component
has endpoints S=.0223221351755312 and .230122302771867. The actual physical
scale-factor growth is

    Delta ln A = .2953458091533101,   A_final/A_initial=1.34359090439.

Independent charge endpoints and quadrature agree within 3.06e-56 at 55-digit
precision. All 1001 sampled vacuum cones are healthy. The isolated X^16 term
would have w=cs²=1/31, but its sampled energy fraction never exceeds 28.98%;
no energy-dominant era of that fluid was demonstrated.

This short vacuum interval is not a radiation era or a recombination solution.
For scale only, ln(1101)=7.003974; no endpoint has been calibrated to today or
recombination. Next derive a sourced background containing radiation, baryons
and the chosen clock, then its coupled photon/baryon/metric/clock perturbations.
Those calculations must produce the physical expansion, acoustic propagation
and growth while preserving activation and auxiliary regularity.

Fable's latest L20 computation was rerun successfully. It concerns the old
IC10 pressure and a different X² deformation; its original past-boundary
finding remains valid in that scope, not transferable to IC14 by name alone.

## Supernova evidence, corrected without presuming a winner

[The full-covariance reanalysis](../supernova_reaudit_2026/REPORT.md) corrects
the older fit's interpretation, restores the public STAT+SYS covariance,
and identifies the independent calibration test. The inherited galaxy GLS
a0 was fitted using a different kernel; it is not automatically the a0 of the
required exponential law. Next fit that exact kernel with independent galaxy
distances and shared calibration uncertainty before claiming a cosmic tie.

[The Sarkar consistency note](../supernova_reaudit_2026/SARKAR_CONSISTENCY.md)
separates a published-correction baseline from the disputed age/directional
analysis, which has not been reproduced here. It also derives the conditional
constant-Lambda identity `q0=1/2-16 pi[a0/(cH0)]²`. Deceleration would challenge
that inherited background combination too, not automatically validate MOND.
For source provenance, the accessible Sarkar methods PDF was
`arXiv:2606.09650v1` (8 June 2026; PDF compiled 9 June), equations (5)-(6).
The Wiseman counteranalysis was read in its published June 2026 version.
Neither complete author data-processing pipeline was reproduced here.

## Verification and immediate continuation

The full construction suite now passes 244 tests (exit 0). IC13 and IC14 strict
reports exit 2; neither is a full-theory certificate. The L20 run and independent
early-span calculation exit 0. All five new v2 evidence manifests validate.
Exact commands, outputs, statuses and file inventory are in
[the run index](ic13_ic14_run_001/run_index.json).

The full-covariance supernova script also exits 0, and the three new exact
background-consistency tests pass (exit 0), including an independent reviewer
rerun. Its preferred v2 evidence is `supernova_reaudit_2026/run_002`; the
earlier run and legacy manifest are retained with their stated metadata limits.

Provenance correction: the older ic11_run_001 pack pinned its 39 declared
artifacts, but omitted several legacy modules loaded through dynamic imports.
It remains a valid record of its declared inputs, not a complete dependency
snapshot. The new regression pins all 52 construction Python files, IC4's
runtime-read action document, other mathematical definitions and L20 inputs
(64 artifacts total). Old evidence is retained rather than silently refreshed.

The best next action construction is a regular global extension of IC14's
matter response with independently controlled scalar momentum and spatial
blocks. It must then pass sourced weak-field and early-universe calculations
from that same action. No global novelty, empirical confirmation, PPN closure,
cluster solution or completed theory is announced.
