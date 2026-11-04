# Independent corrected-history review

**Claim audited.** The corrected exact-angular common-state calculation reaches `N=0.0021690179772784167` from its declared fresh FD initial packet, with intact restart ancestry, a genuinely integrated FRW-work ledger, and the stated finite solver/domain checks. The new four-parent trace envelope is a local frozen-bath result, not a universal coherence correction to that history.

**Primary verdict: correct only after a stated restriction.** The completed comparison checkpoint and its ancestry are authenticated, and I found no splice between the new early populations and the old late-memory endpoint. The result remains a finite, conditional numerical prefix. Its field action is **not a precision result**: the cumulative independent energy residual is about **22.23% of the remaining orbital excitation**, despite being only 1.44e-4 of the initial gas energy. The README's separation of early and late calculations is appropriate; an explicit orbital-error qualification should accompany any newly quoted action/turning-point comparison.

## Ancestry and cumulative conservation

The actual path is:

    run_initial001 [completed]
      → run_fresh_exact001 [failed target N=.01; usable bounded prefix]
      → run_fresh_exact002 [failed target N=.01; usable bounded prefix]
      → history/run_advance001 [failed target; usable bounded prefix]
      → history/run_advance002 [completed comparison target]

All five manifests validate against current project-root hashes. Failure of a larger requested target is retained; the completed final comparison does not relabel those earlier jobs as completed.

At every join the recorded N, q/W grid, initial population vector, and boundary group counts agree. The work-ledger jump is at most 6.33e-15 in units of the initial gas energy, consistent with orbit reconstruction roundoff. The reference energy remains `4.234568124685809e-9 μ⁴` and `gas0=3.4024207205983918e-9 μ⁴` throughout.

The initial exact driver starts from the actual fresh initial packet. `run_fresh_exact001` did not store its cumulative work as a separate state field; the v2 restart correctly reconstructs it from the prior genuine ledger residual, the original reference energy, and the reconstructed orbit energy. Later restarts carry `energy_reference_E` and `independent_work` explicitly. This preserves the earlier residual instead of resetting the reference at every checkpoint.

The ledger is independent of reconstructed energy changes. Each accepted step adds the trapezoidal integral of

    3 <kin2 + rho_gas + P_gas> dN

to the work. It does not set work equal to the negative energy increment. Centered collision covariance supplies the action update; local event energy and gas-force energy use the same common mass interpolation. The wrapper still retains interpolated source widths, so the earlier near-crossing rate-interpolation qualification remains.

The driver reads the preceding early state, the vertex background and the matched leading gravity packet. Its old CT09 imports provide lower-level model/potential definitions; the late hybrid distribution or memory kernel is not initialized or loaded into this history. The central README explicitly says the early and old late endpoints must not be spliced, and the inspected implementation respects that separation.

## The error scale that limits J

The authenticated endpoint is:

| Quantity | Stored finite result |
|---|---:|
| N | 0.0021690179772784167 |
| Charged fraction | 0.8099457087 |
| Charged yield | 3.0336014725e-7 |
| Action J | 2.3925782137e-6 |
| Turning points | 3.57673484 … 4.15575157 |
| Maximum fermionic occupation | 0.567558847 |
| `(E+work−Eref)/gas0` | −1.4395404436e-4 |

A fresh bounded read-only reconstruction gives:

    E                 = 4.203640504169990e-9 μ⁴
    U_min             = 4.201436744452412e-9 μ⁴
    E−U_min           = 2.203759717578259e-12 μ⁴
    E+work−Eref        = −4.897922233522580e-13 μ⁴
    |residual|/(E−Umin)= 0.2222530067.

Reconstructing the same fixed state/action with 16 and 32 orbit nodes changes this ratio negligibly; it does not remove the accumulated history residual. The independent ledger residual is also 22.2342% of `ωJ`.

This ratio is **not** a proved 22% error bar on J: a conservation residual alone cannot locate or sign the actual state/action error. It does show that the reported energy agreement cannot certify a precise remaining oscillation amplitude/action. At fixed population, `∂J/∂E=1/ω`; the residual therefore has an action-error *scale* comparable to 22% of the stored J. The current 0.001-of-gas acceptance threshold would permit an energy residual larger than the entire remaining orbital excitation.

The comparison record finds J 12.4943% above the old coarse-angle history and charged yield 0.41454% below it at the same N. These are differences between two numerical paths, with different angle treatment, phase order and accepted timesteps. The comparison source correctly declines to attribute them solely to angular integration. In particular the action difference is smaller than the present residual/excitation scale and needs timestep/coupling refinement before a precision interpretation. A successful one-period endpoint check cannot retroactively eliminate accumulated error from the earlier prefix.

The final advance's maximum predictor/corrector log-action discrepancy is 0.01821. That is an adaptive estimator, not an accumulated global error bound. The number solver's final coordinate residuals are small, but those checks do not supply the missing global field-action accuracy or phase/momentum convergence.

## Log-number solve and model limitations

`initial_solver/log_number.py` applies sparse Newton in log coordinates to the conservative physical-number backward-Euler residual. The cap at 0.6 of fermionic measure affects its initial guess; the clipping of log corrections affects the search direction. Neither clips an accepted physical state. The hole/number sign chain and exact angular Jacobian were independently checked in the previous frozen review. This review additionally checked which solver is actually imported by the history driver: it is `initial_solver/log_number.py`, not the older `integration_solver/log_holes.py`.

The absolute number floor applies to nearly empty number coordinates, while explicit hole coordinates retain their relative scheme. The final chunk records physical-coordinate residual L1 ≤9.63e-16 and computed gross roundoff allowance ≤4.07e-15. The driver also evaluates its physical number balance separately. These are finite solver diagnostics; the fixed `32 ε` allowance is not a universal certified floating-error theorem for arbitrary event counts.

The final chunk has maximum occupied-parent forward omission 1.3353e-6 and integrated omitted forward measure 1.7869e-7. This is a reported forward-support diagnostic, not a bound on every omitted inverse/tail contribution. The forty-node `q≤80` finite projection and eight orbit phases remain part of the approximation. Exact angular integration does not establish convergence in those variables or make this an appropriate late hard-decay grid.

## Four-parent periodic trace envelope

The actual four massive neutral parents are **S1_1**, mass `sqrt(.006)`; S1_0 is the massless two-real-state modulus. The new matrix calculation rebuilds actual-x tensors, rather than transplanting late-pole parent indices/couplings.

For the declared frozen coefficients, the PSD covariance satisfies

    rho_dot = G − {D,rho}/2 − i[H,rho],
    Tr rho_dot ≤ S_max − gamma_min Tr rho,

when G is PSD, D has a positive uniform lower eigenvalue bound, and H is any Hermitian parent Hamiltonian. A PSD periodic response therefore has `Tr rho ≤ S_max/gamma_min`. A finite frozen-bath evolution starting at trace N₀ instead has trace at most `max(N₀,S_max/gamma_min)`.

At a fixed daughter bath, the constant gain term cancels between two parent-state current predictions. With Hermitian charged-current matrix A,

    |Tr A(rho−rho_ref)| ≤ ||A||op (Tr rho+Tr rho_ref).

Positive momentum and phase weights preserve this inequality. The phase-weighted version requires the declared node durations; the phase-uniform maximum-norm version permits any ordering/duration. Positive convex interpolation of the frozen node coefficients preserves the stated source/gap extrema. These arguments do not require instantaneous stationary elimination or a chosen within-parent Hermitian splitting.

I reconstructed the recorded trace/current aggregation exactly. Relative to the whole saved charged-current magnitude, the periodic-vs-stored-parent bounds are **0.540505% and 0.639552%**; phase-uniform bounds are **0.542187% and 0.639631%**. These bound the declared matrix model on **old `run_warm001` and `run_warm002` frozen baths**. The second old bath even has net charged return. The argument does not require those old histories to be physical, because they are inputs to a local conditional operator test.

The bound does **not** apply automatically to `history/run_advance002`, despite the first old snapshot sharing its N. Their populations, orbit and currents differ. It also does not bound accumulated abundance/action error, arbitrary changing daughter baths, uncomputed gain/loss corrections, another degenerate multiplet, or an unspecified nonlocal medium. An arbitrary Hermitian commutator can be admitted in the trace proof while keeping the tested gain/loss model fixed; that is not matching the actual medium self-energy. I re-read the finalized DERIVATION/STATUS trace-envelope sections; they respect this local scope.

Those finalized documents also state that broken-vector channels are excluded from this FFS/SSS operator and can be kinematically open in the warm region. The bound concerns the included whole25 current, not fully inclusive physical widths. This omission includes possible warm broken-vector **1↔2** reactions and should not be described only as missing gauge/vector 2-to-2 scattering.

## First remaining implication and provenance

The next numerical obligation is a refined common-state history that controls cumulative energy/action error relative to the shrinking excitation, with phase/momentum/timestep comparisons. The next physical bridge is coherent/common population transport along that new history, or a valid evolving-state closure bound, with the omitted open vector sector addressed, followed by transition to the late memory/cascade/loop sector with the same populations and retained hard momenta. The old late passive-tail failure remains conditional on its own endpoint. No cold-matter history is completed by joining these separate results.

The read-only control is `run002`, status **completed**. It took 0.491 s, measured peak RSS 294,223,872 bytes, and used a fresh v2 record with wall cap 180 s, CPU cap 175 s and one numerical thread. The earlier review harness `run001` failed before numerical work because it omitted the cascades import path; its exact source is archived locally and it supplies no mathematical evidence.

Ten inspected production/ancestry/coherence manifests validate, with their actual statuses preserved; the substantive control manifest also validates. Exact reviewed hashes, argv, versions, repository state, source archive binding and validation output are in `provenance.json`. I read the current README and the history driver/solver/work carry plus the coherence proof/API, and reconstructed endpoint orbit/error scales. I did not rerun the full trajectory, independently rebuild all four-state warm amplitudes, or audit the cascade worker's separately produced direct endpoint run. No source outside `independent_review/history_final/` was edited; prior reviews remain frozen.
