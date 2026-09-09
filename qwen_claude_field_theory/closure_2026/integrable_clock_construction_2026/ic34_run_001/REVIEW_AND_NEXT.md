# IC34 terminal review: nonlinear many-step evolution

Base 9e7bf25b9ae48e287537fa708d7ae252be272951.
Original full-theory goal **OPEN**. Self-review, not independent or formal certification.

## What actually advanced

IC33 repaired a missing metric evolution equation but still tested one time
tangent. IC34 derives the same action's general plane-symmetric equations and
advances spatially varying metric, momentum, shear, and two fluids over many
time steps. Generated fluid gradients are retained.

Only the nondynamical lapse/z/multiplier equations are solved at RK stages.
The momentum constraint and matter charges are NEVER projected or normalized.
Their preservation is therefore a separate check on the coupled evolution.
The action coefficient function is the fixed IC32 repaired 81-node approximation;
no state or source redefines it.

This periodic cosmological experiment does not replace the still-missing
spherical galaxy-to-cosmology matching problem.

## Actual execution and provenance

| Job | Child exit | Runner exit | Wall seconds | Interpretation |
|---|---:|---:|---:|---|
| evolution | 2 | 1 | 47.948946 | 13 scoped checks true; strict mode retains full-theory OPEN |
| tests | 0 | 0 | 288.557805 | 413 tests; unittest elapsed 287.973 seconds |

Both manifests validated with exit 0 using the repository root. Pinned input and
output hashes match. Validation is provenance evidence, not theorem certification.
Exact child and runner commands are in run_index.json. Both jobs are terminal.
Caps: 420 seconds wall, 2 MiB logs, one cooperative numerical-library thread per
job; no hard memory or CPU-affinity limit.

Ten exact symbolic checks cover the varied metric/constraint equations,
independent three-dimensional Ricci construction, and canonical matter transport.
The three additional checks cover evolution, refinement and the zero-mode control.
No ranks, DOF counts or PPN values are supplied by these flags.

## Finite numerical results

All four main runs reached T=.2 in model units with initial sinusoidal amplitude
.02. They took 10, 20, 40, 40 real RK4 steps, respectively.

| N | dt | Maximum unprojected momentum residual | Maximum relative matter-charge drift |
|---:|---:|---:|---:|
| 32 | .02 | 6.334224672456868e-13 | 3.348876731479322e-12 |
| 32 | .01 | 5.4333708853927966e-14 | 2.036149027162537e-13 |
| 32 | .005 | 1.2488668239392797e-14 | 1.176836406102666e-14 |
| 64 | .005 | 1.9054795990733875e-14 | 1.3100631690576847e-14 |

Successive final-state time differences:
1.5658117025196816e-8 and 9.599880890220902e-10; ratio 16.310740939658167.
The final-state difference between N32 and N64 at dt=.005, on common nodes,
is 3.978151141836861e-12.

At N64,dt=.005:
- maximum solved lapse residual 6.4519925784085e-14;
- maximum shear-gauge residual 3.6295619287862735e-13;
- maximum z residual 1.8388068845354155e-16;
- maximum multiplier equation residual 3.552713678800501e-15;
- maximum fluid Legendre residual 2.4839228708484623e-16;
- final maximum fluid gradient 2.9900426365790752e-5;
- minimum accepted normal volume expansion K/3: .8284929140123022;
- minimum accepted active-pin margin: 2.2403937382694816;
- final homogeneous anisotropy Xi: 6.493739920694252e-8.

The largest lapse residual among all four runs is 3.3605555768633183e-12,
not the smaller N64 value. The expansion and pin minima above are over accepted
states; an additional pin-domain guard is checked at RK stages.
The aggregate initial-to-final state norm mixes field units and is not an
observable amplitude or a Hubble-rate measurement.

Fourth-order-looking temporal convergence is observed in this range, not
proved uniformly for the piecewise C2 action coefficient. Fourier aliasing,
continuum existence, and all-wavelength stability are not certified.

## The zero-mode calculation that mattered

The independently varied shear equation is

    Xidot = beta' + t sh.

On a periodic domain, integration gives

    Xidot = average_x(t sh).

Vanishing unweighted mean shear does not imply that this weighted mean vanishes.
The retained homogeneous metric mode produces an initial gauge residual
8.389122729823839e-15. Suppressing its rate, with the same initial physical
fields, produces 9.699165410478883e-7. That adverse control is preserved.

The canonical coefficient of Xidot in the reduced action is (4/3) integral(J sh dx).
This identifies a retained homogeneous metric canonical sector; it does not
supply the full functional Dirac count or permit calling it a harmless gauge
mode without further analysis.

## Development and self-review record

The three new regression tests initially failed because the implementation was
absent. The first implementation had a missing closing parenthesis in diagnostic
assembly; its syntax error was exposed and repaired. Targeted tests then passed
before the final bounded full-suite run.

The longer T=.2 time/refinement pilot and suppressed-zero-mode control were
executed before the final contract. Their successful numerical values reproduce
in the recorded run. No failed construction was deleted, and no parameter was
refitted to manufacture the retained-mode result.

Mathbox computation-audit enforced separate finite-evidence and full-theory
claims, controls and pinned provenance. Proof-audit/self-review checked the
global zero-mode compatibility and independent evolution equations.
Proofreading covered IC34_PERIODIC_EVOLUTION.md and the new equations; the
Newton Jacobian explicitly uses C_vac to avoid double-counting the matter
S derivative. No external theorem, empirical or global novelty claim is made.

## Next indispensable construction

Return to the missing physical connection: derive and solve the off-pin,
inhomogeneous evolution/constraint system through the active-pin to unpinned
exponential-MOND transition. Retain the independently varied metric equations,
generated matter stresses, and zero-mode compatibility. Derive matching data
and multiplier regularity rather than imposing a static join or dividing
silently by a vanishing activation.

The periodic result is not enough to certify that connection. Full nonlinear
Dirac closure, the healthy separately counted clock, global coefficient
extension, k=0/y=0 strata, causal response and strong coupling, full PPN/measured
Newton constant, and empirical cosmology/galaxy/binary/cluster/CMB tests remain
original requirements. Positive expansion in this toy run is not a realistic
recombination history. The a0-Lambda coefficient remains input; Lean is not
available on the checked PATH.
