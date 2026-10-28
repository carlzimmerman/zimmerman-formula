# Basin / kappa independent push — frozen contract

Base checkpoint: `7954d48377463cafcae3e8dbb09454134aef384f`.
Owner: delegated basin_kappa lane. Date: 2026-10-28.
Write scope: this directory only. Existing dirty work is preserved.
The coordinator explicitly overrode inherited commit instructions because `.git`
is read-only. Freeze by SHA-256 before execution; no commit or push.

Target: independently test the proposed acceleration-at-turnaround switch;
execute a genuinely different, cheap basin discriminator; clarify the physical
versus conventional content of kappa. Success is a derivation or scoped
obstruction, not a new asserted field equation. Kappa = 1/2 remains FITTED.
Canonical and alt footings are separate throughout.

## Assumption / input ledger (before numerical results)

| input | classification | source / interpretation |
|---|---|---|
| a0 = 9.3603e-11, 1.1312e-10 SI | FRAMEWORK-NATIVE phenomenological, fitted kappa | THEORY_EQUATIONS_2026-10-28.md, BS1 script |
| T = 10^12.2357, 10^12.5739 solar masses | FRAMEWORK-NATIVE data-located L, inherited collapse rule | BS1 README, CL3 one-number variant, separate footings |
| LG log basin mass = 12.3925; R0 = 794.7 kpc | FRAMEWORK-NATIVE processed mass / SURVEY-CALIBRATION geometry | BS1 README; not a new raw-data inference |
| t0 = 13.821005106655473 Gyr | FRAMEWORK-NATIVE background with CMB-fit parameters, hence EXTERNALLY CALIBRATED | G2_preinfall_retention/g2_preinfall_retention_results.json and ASSUMPTION_LEDGER.md |
| t0 bracket 10 to 20 Gyr | specified sensitivity scenarios, not fitted | tests dependence on the preceding calibrated age |
| G = 6.67430e-11, c = 299792458, solar mass = 1.98847e30 kg; pc = 3.0856775814913673e16 m; yr = 365.25 days | unit / physical constants, stipulated | calculations only, no present precision claim |
| H_Lambda = sqrt(32 pi/3) a0_canonical/c | FRAMEWORK-NATIVE, conditional on fitted kappa | algebraic rewrite of canonical equation (1); not an independent prediction |
| Newtonian isolated radial shell with cosmological constant | specified diagnostic model | derived energy equation, not the frozen covariant parent |
| spherical simple-law shell plus constant vacuum repulsion | specified diagnostic model | integrated g from equation (2); not a claimed cosmological completion |
| smooth spherical pressureless initial data, annular exterior mass | specified counterexample class | AQUAL radial flux shell theorem, no NFW or survey prior |
| AQUAL kinetic F and minimal scalar matter coupling | conditional normalization audit class | existing kappa offset obstruction, not a new action proposal |

No raw measurements are newly scored. No QUMOND, EFE recipe, halo mass function,
LCDM concentration, simulation, download, field-equation fit or new parameter
is used. AQUAL changes radial flux; stiffness is not modeled, so claims about
screened/derivative-extended equations are excluded. Native H0 does not enter
the switch; the age sensitivity explicitly bounds the calibrated background
input. SPS, h conversions, cluster labels and BS dust abundance do not enter.

## Routes and discriminators

R1: derive finite-age Newtonian first-turnaround with and without Lambda;
derive the distinct static balance radius. Compute the mass at which g_N=a0.
Separately compute thresholds for the actual simple-law g=a0, first as a
postprocessing diagnostic of Newtonian radii, then under the integrated
simple-law toy dynamics. The same ~10^20 estimate is supported only to the
precision and convention actually found. No equality of static balance and
zero velocity is assumed. Boundary g=a0 is not identified with total net
acceleration including vacuum.

R2: construct two smooth spherical pressureless initial conditions with the
same local matter/velocity/force data but opposite basin-mass flags, using an
exterior shell. Prove the general restriction on any local rule depending on
these jets. Also derive the pressureless Newtonian scaling symmetry and show
it has no absolute collapse mass. Failure of a local trigger does not refute
nonlocal dynamics or establish a replacement mechanism.

R3: explicitly transform scalar normalization and show the measurable
combination kappa is invariant. Exhibit the independent additive constant in
the simple-law primitive. Scope: an audited obstruction already anticipated
by the record, not a new universal no-go and not a claim that a fitted
physical parameter is a convention.

## Checks and outcome lines

K1: symbolic simple-law identities, potential derivative and normalization
invariants hold exactly.
K2: Newtonian turnaround quadrature at zero vacuum gives pi/(2 sqrt(2));
independent transformed Simpson quadrature agrees with adaptive quadrature
within 2e-7 relative error at every reported root.
K3: original dimensional energy integral and nondimensional integral agree;
threshold residuals < 2e-7, with positive radicands throughout sampled interior.
K4: for the stipulated age bracket and both footings report every threshold,
not a selected value. Compare to the inherited T without retuning it.
K5: shell counterexample has zero local force differences and opposite
basin flags; similarity transforms preserve the dust equations exactly.
K6: mutation must alter a real critical calculation and make at least one
check fail. Normal and mutated outputs remain separate.

Command planned: `OMP_NUM_THREADS=1 nice -n 15 python3 .../basin_kappa.py`
through the mathbox bounded runner; single thread, less than 1 GB RSS,
less than two minutes. No heavy simulation. Proofs receive a separate
adversarial self-review; coordinator may independently review.

## AMENDMENT A1 (pre-result, environment only)

The first runner launch performed no computation: macOS does not support its
requested CPU affinity cap, and sandbox setpriority for `nice -n 15` was
denied. Omit `--max-cores` and `nice` for this bounded, single-threaded job.
Keep 90 s wall time, 60 s CPU time, thread limits and measured peak RSS.
No mathematical input, criterion or numerical tolerance changes.
