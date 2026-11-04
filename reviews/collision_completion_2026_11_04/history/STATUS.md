# Corrected finite warm checkpoint

The requested comparison checkpoint was reached at exactly
`N=0.0021690179772784167`, with `Tc/mu=.004647167475555158`.
The preferred numerical state is **`run_refine002/result.json`**. It uses a
maximum N step of `5e-5` after the shared fresh002 prefix. It is preferred for
the smaller step, not because its energy ledger is more accurate.

This is a finite warm checkpoint. The complete cooling history, physical
four-state singlet closure, late charged relic and cold photino abundance remain
open. The gas-normalized energy check does not certify the action or trapping
accuracy: its accumulated error is about 24% of the remaining orbital excitation.

## Preferred state and comparison

| quantity | refined corrected state | old coarse-angle warm state |
|---|---:|---:|
| charged fraction of original FD carriers | .8100369103 | .8133172513 |
| charged yield | 3.033943063e-7 | 3.046229377e-7 |
| inner turning point | 3.581337295 | 3.557128548 |
| outer turning point | 4.158546805 | 4.103292712 |
| potential minimum | 3.866937045 | 3.827589802 |
| action | 2.377475335e-6 | 2.126843467e-6 |
| U1-gaugino yield | 1.039589723e-9 | 1.073040366e-9 |
| SU2-gaugino yield | 2.381636359e-9 | 2.422495253e-9 |
| SU3-gaugino yield | 8.548284792e-9 | 8.557915505e-9 |
| maximum fermion occupation | .5289571 | nearly 1 |

The corrected charged yield is .4033% lower. U1, SU2 and SU3 yields differ by
−3.1174%, −1.6866% and −.1125%, respectively. Their normalized momentum-shape
L1 differences are 10.586%, 11.107% and 9.457%. The old alternating soft-bin
pattern and near-unit soft saturation are absent in the corrected state.
The precise corrected soft profile is not time converged.

The corrected and old histories also differ in phase quadrature and accepted
step sequence. The comparison does not attribute every difference solely to
the angular correction. `run_compare_refined_old001` contains every group and
the complete soft-cell comparison.

## Numerical controls and remaining precision

The actual fresh002 frozen-operator step compared the validated number-floor
solver with the frozen log-number solver. Both gave the same charged and U1
numbers and entropy increase. The former needed 85 iterations and 92.6 s; the
latter needed 5 iterations and 6.18 s. Physical number residuals were about 1e-16. This control
is `run_control_log002`; the initial import-path failure is retained in
`run_control_log001` and its source `control_log.py`.

The floor changes the nonlinear stopping scale for nearly empty number
coordinates. It is not a population cutoff. The log predictor changes only the
initial Newton guess; accepted states solve the conservative number equation
without clipping. Fermion holes remain explicit. Endpoint populations below
1e-80 demonstrate that no state floor was imposed.

The larger-step corrected route used a cap of 2e-4 with adaptive action and number
controls. The refinement used a cap of 5e-5 after the same fresh002 ancestor. At the
common endpoint the refined versus larger-step differences are:

| quantity | relative difference |
|---|---:|
| charged yield | +.01126% |
| action | −.63124% |
| U1 yield | −1.13663% |
| SU2 yield | −1.21107% |
| SU3 yield | −.36430% |

These are observed differences, not rigorous error bounds. Both paths share
the unrefined interval before `N=.0003492778087575775`. The two corrected
branches also show material soft-cell differences despite close total charged
numbers. `run_compare_refinement001` records both distributions.

The independent work ledger is

`DeltaE = E(N) + W_FRW(N) - E_reference`,

with cumulative FRW work integrated from the original reference. No restart
resets either quantity. The common reference is
`E_reference=4.234568124685809e-9`, and the gas normalization is
`3.402420720598392e-9` in mu units. Actual orbital excitation is

`E_exc = E(N) - min_x [V(x)+rho_particles(x,N)]`.

| route | DeltaE/gas normalization | abs(DeltaE) | E_exc | abs(DeltaE)/E_exc |
|---|---:|---:|---:|---:|
| larger steps | −1.43954044e-4 | 4.89792223e-13 | 2.20375972e-12 | 22.2253% |
| refined | −1.53463396e-4 | 5.22147038e-13 | 2.18966862e-12 | 23.8459% |

At the refined endpoint, 8.6821% of its excitation corresponds to the inherited
prefix error, and 15.1638% to the added error after that prefix. The smaller
step did not monotonically reduce the cumulative work residual. Therefore
neither route is a precision-certified action or trapping prediction.
`run_ledger001` reconstructs the minima and checks the common reference.

## Direct endpoint control

`run_direct001` starts from **`run_advance002`**, the larger-step corrected
endpoint, not from the preferred refined state. It evolves one actual field
period with 128 direct scalar/quantum collision steps and analytic angular
integration. All local energy, positivity and fermion-bound checks pass.
The duration is `6824255.947953 mu^-1`, with 128 accepted steps, no rejected
steps and at most 3 Newton iterations. Maximum local work residual is
`3.20056e-7` relative to the control's starting energy. The maximum
parent-weighted omitted forward measure fraction is `2.22445e-5`; this is a
finite-support diagnostic, not a bound on arbitrary inverse production.

The charged ratio is `.9999619007`; action changes from
`2.392578954e-6` to `2.389369681e-6`. Its local work test does not erase the
inherited cumulative error. Both the inherited work and the original reference
are retained in its exported state. This is a local control at the named
larger-step state, not a direct validation of the refined history.

## Ancestry and scope

The common starting chain is

`integration/run_initial001 -> integration/run_fresh_exact001 -> integration/run_fresh_exact002`.

The larger-step branch is

`history/run_advance001 -> history/run_advance002`.

The preferred smaller-step branch is

`history/run_refine001 -> history/run_refine002`.

The first continuation of each branch stopped deliberately at its wall-budget
checkpoint. Its manifest has failed target status because the final requested
N was not yet reached; all physical checks passed and the next manifest pins
the exact checkpoint bytes. This is not a physical exclusion or an unchanged
solver stall.

All successful scientific runs have fresh v2 manifests, explicit input closure,
one numerical thread, wall<=240s, CPU<=235s and measured RSS. Exact source and
output hashes, statuses and validation are in `PROVENANCE.json`. All prior
cascade sources were read-only throughout this work package.

Future continuation must start from a named corrected state and preserve its
all 25 distributions, mixed coordinates, action and cumulative work/reference.
**Do not splice an old late endpoint into this corrected trajectory.** Before
promoting a physical candidate, control energy/action error relative to the
shrinking excitation, refine the shared prefix and phase/momentum resolution,
and resolve the declared fourfold singlet coherence and omitted physical
channels. The full cold history remains open.
