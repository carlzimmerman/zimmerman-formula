# Independent local energy-direction diagnostic

**Claim tested.** At fixed N, use the exact-angular phase-averaged collision direction `dY/dN=Cbar/H` and centered action direction `dJ/dN=cov/(omega H)`. The reconstructed orbit energy should have zero derivative in the continuum phase-integral limit. Separately, the expansion direction `(dN,dY,dJ)=(1,0,−3J)` should give the independently evaluated FRW work.

**Primary verdict: computationally verified only in a stated range.** The local algebraic energy identity cancels to about 1e-22 μ⁴ per N. Resolvable physical tangent tests at the shared fresh state and the energy-relevant bulk of the refined warm state agree with the orbit-energy derivative to a few parts per million of the cancelling collision terms. The expansion derivative agrees to about 4e-8 relatively. These tests find no large rate/action normalization or gradient-factor error at the inspected states.

They do **not** explain away the cumulative history residual. Reconstructing a coupled action update around an existing physical backward-Euler population step produces a finite energy defect. This keeps discrete temporal centering/coupling accuracy as the next unresolved issue. Its signed contributions are not sufficient to assign the entire negative cumulative residual to one cause.

## What the identity requires

For the all-species orbit Hamiltonian,

    dE = omega dJ + t³ <E_a> dY_a       at fixed N.

The centered collision covariance is

    cov = t³ [<sum_a E_a C_a> − sum_a <E_a><C_a>].

Consequently the proposed collision tangent gives

    dE/dN = [cov+t³ Ebar.Cbar]/H
           = t³ <sum_a E_a C_a>/H = 0.

The last equality is the phase-local retained-particle collision invariant. It does not require the phase-averaged energy vector to be a local invariant. The expansion identity follows from `dJ/dN=−3J`, `∂E/∂N|J,Y=−3<rho+P>` and `<kin2>=omega J`.

The finite orbit implementation evaluates its action, period and energy averages by quadrature. Derivatives of the finite quadrature, including moving turning points, need not satisfy the continuum integral identities exactly. This diagnostic tests that difference; it does not assume it vanishes by construction.

## Inputs, perturbations and numerical resolution

The two frozen inputs are:

- `integration/run_fresh_exact002/result.json`, N=0.0003492778087575775;
- `history/run_refine002/result.json`, N=0.0021690179772784167.

For each, the actual forty-node, 25-group state and stored vacancy coordinates were reconstructed at 8, 16 and 24 orbit nodes. At every phase I built the exact finite-projection angular operator, evaluated C, and independently combined the phase moments. No history evolution or source-model modification was performed.

The event/gas energy grids agree within 5.56e-17 μ. The weighted local collision-energy derivative is at most 3.01e-22 μ⁴/N. The centered-vs-raw covariance difference is below 1.22e-34 in its native units. The final algebraic cancellation is at most 4.88e-22 μ⁴/N.

At the fresh state, the full positive linear collision tangent permits ε only up to approximately 4.4–4.7e-7. Thus ε=1e-6 was rejected; ε=1e-7, 5e-8, 1e-8 and 5e-9 were physical. Pairwise and quadratic extrapolations remove the leading finite-ε curvature contribution.

The first raw probe also exposed two numerical limits of the audit itself. Its base action used the returned quadrature action instead of retaining the identical target-J coordinate, and it attempted warm perturbations around ε=1e-62. Those changes are below floating-point resolution, so its huge raw warm derivative quotients are **not mathematical counterexamples**. `run002` retains the original target-J coordinate, rejects unresolved trials, and independently re-roots the same finite action integral with a tighter outer energy tolerance (`xtol=1e-30`, `rtol=1e-15`). This is an audit-only energy evaluation; the production source and trajectory were not changed. The production root tolerance acts on total energy and otherwise limits very small finite differences.

## Local collision and expansion results

Representative extrapolated collision-energy defects are:

| State/direction | Orbit nodes | dE defect [μ⁴/N] | Fraction of cancelling energy terms |
|---|---:|---:|---:|
| Fresh, full physical tangent | 8 | −1.11e-13 | −4.62e-6 |
| Fresh, full physical tangent | 16 | +9.85e-14 | +4.19e-6 |
| Fresh, full physical tangent | 24 | −1.17e-13 | −4.93e-6 |
| Refined warm, restricted bulk tangent | 8 | −1.10e-14 | −3.90e-6 |
| Refined warm, restricted bulk tangent | 16 | +3.66e-15 | +1.28e-6 |
| Refined warm, restricted bulk tangent | 24 | +1.53e-15 | +5.33e-7 |

The fresh cancelling terms are approximately 2.35–2.39e-8 μ⁴/N; the warm terms are 2.82–2.87e-9 μ⁴/N. The small signs/order dependence is not a demonstrated uniform quadrature error bound. It is, however, far below the large factor error or substantial local action-gradient inconsistency this test was designed to detect. The rates/covariance themselves still change at percent scale across these phase orders; this derivative check is not a full phase-convergence certificate for the trajectory.

At the refined warm state, the **full** linear tangent is physically inadmissible at every requested ε. Three ultra-small coordinates limit positive ε to approximately 1.7e-61, below numerical resolution. That full warm finite-difference test therefore remains inconclusive.

The separate `run003` explicitly removes only those three obstructing number-direction components, leaves the original field-action direction unchanged, and reports/subtracts the known missing linear energy term. Their removed number-direction L1 is about 3.76e-20 per N and their absolute energy budget is 9.75e-28 μ⁴/N, only 3.4e-19 of the cancelling bulk terms. All restricted trial populations obey the quantum bounds. The warm rows above are this explicitly restricted, energetically representative direction; they are not mislabeled as the full instantaneous collision tangent. No accepted physical state was clipped.

The independent expansion-only test is resolvable at both states. After extrapolation it agrees with `−3<kin2+rho+P>` within approximately 4e-8 relatively, with the smallest finite differences approaching floating-point resolution. This supplies no evidence for a substantial missing expansion-work coefficient.

## Existing-step population/action decomposition

I reused the saved log-solver output in `history/run_control_log002`: a physical conservative backward-Euler population step from the shared fresh state with ΔN=5e-5 and frozen old orbit geometry. I reconstructed the action predictor, endpoint-geometry covariance, log-action Heun update and FRW work without a new nonlinear population solve.

This is a diagnostic reconstruction, **not** a new accepted history step: the saved population solve uses `dt=ΔN/H_start`, whereas the history driver uses H at the midpoint. Its recalculated physical-number balance L1 is 2.33e-14, below the driver's declared absolute budget; its action predictor/corrector estimator is 0.002801.

Removing the known expansion factor from the log-action update gives a collision-only action. At fixed N its resulting energy change is **+6.1461e-15 μ⁴**. Including the reconstructed expansion and independently integrated work gives **+5.2888e-15 μ⁴**, or **1.5544e-6 of gas0**.

For clarity, the collision energy change can be decomposed identically as:

| Term | Energy [μ⁴] |
|---|---:|
| Actual population increment minus trapezoidal start/end number flux, contracted with the old energy gradient | −2.4992e-14 |
| Action/covariance geometry and log-transport remainder | +2.3026e-13 |
| Nonlinear Hamiltonian remainder beyond the old linear gradients | −1.9912e-13 |
| Sum: actual collision-only energy change | +6.1461e-15 |

Thus sizeable finite-step contributions cancel but leave a nonzero defect, even while the infinitesimal energy identity is accurate. The backward-Euler population increment is not the same increment as the trapezoidal start/end flux underlying the action update. Geometry/log transport and Hamiltonian curvature are also of the same finite-step order and cannot be discarded.

A fixed-N constant-energy comparison would give collision action 1.77869253377e-5, versus 1.77938995497e-5 from the reconstructed Heun update. Their difference is 3.6575e-4 of the starting action. This is a comparison diagnostic, not a repaired integration scheme or a new physical result.

The one-step residual here is positive, whereas the accumulated production residual is negative. Therefore this example establishes a discrete energy-consistency issue to investigate; it does **not** prove that one term alone causes the full cumulative error. A matched temporal-discretization comparison is the next discriminating check. No normalization fix is justified by these results.

## Scope and provenance

These local tests do not reduce the reported preferred refined-history residual: the existing `history/run_ledger001` records −1.534633957e-4 of initial gas energy, **23.8459% of its remaining orbital excitation**, versus 22.2253% for the larger-step branch. They do not certify J, isolate the old-vs-new 12.5% action difference, validate the full physical closure, or join the early population branch to the separate old late-memory branch. The conditional late passive-tail bound remains independent of this new warm prefix.

All three new manifests have status `completed` and validate against current input hashes. Their scientific interpretation is narrower than execution success: the raw warm quotients in `run001` are rejected as unresolved, the complete fresh tangent and expansion tests are in `run002`, and the restricted warm direction is in `run003`. Measured runtimes/RSS were 25.37 s/489.65 MB, 34.23 s/495.22 MB and 12.65 s/427.02 MB. Each used a fresh v2 bounded runner, wall cap 240 s, CPU cap 235 s, one numerical thread and observed RSS. No installation, Git operation, full history rerun or edit outside `independent_review/energy_diagnostic/` occurred.

Exact commands, reviewed source/data hashes, repository state, validator outputs and interpretation flags are in `provenance.json`. This is an independent local diagnostic and scope assessment; the previous reviews remain frozen. Work stopped after the requested bounded diagnostic, with no further production run or proposed source repair.
