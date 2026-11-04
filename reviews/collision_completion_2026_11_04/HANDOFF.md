# CC10 continuation checkpoint

User instruction: work out the missing collisions, neutral cascades and resonance memory computationally. The broader objective remains a weak-coupling retained vacuum with heavy charged carriers removed and sufficient cold photinos. That broader objective has not been achieved.

## Start here

Read [README.md](README.md), [CONTRACT.md](CONTRACT.md), and the [independent final review](independent_review/final/REVIEW.md). The physical baseline is the leading pole-aligned trajectory packet, e=.003, mu=2e6 GeV, xi=.02. Do not substitute the separately normalized finite local gravity packet. Previous published physics ancestry is `370cb35bc08d13f2a8c0dfa9adee161e1665ead2`; this phase began at shared revision `fd417eea045a0b6259b8efff5e20ca62a2e14f7e`. Source/output hashes fix actual computation inputs while the shared branch advances independently.

No Git mutation or publication was authorized for this new phase. Work is confined to this directory; preserve prior TP06/CT09 and unrelated working files.

## What is settled within its declared model

- The 25-group SSS/FFS collision operator includes inverse reactions, Bose/Pauli factors and actual massive daughters. Its exact finite angular integration and physical-number Jacobian have independent checks. The old global two-angle warm calculation had 30–40% RHS errors and false soft-state saturation; do not promote that trajectory as physical evidence.
- `cascades/angular_fast.py` is the frozen production angular builder. `initial_solver/log_number.py` supplies the tested positive solver with explicit vacancy coordinates and physical residual budgets. All primary APIs, hashes, controls and historical failures are in their owned handoffs/provenance.
- The preferred late memory stage evolves scalar momentum shape and retains actual neutral cascade cohorts. It gives Ycharged=1.72351105e-13, versus 6.27471e-13 for its stationary control. This stage retains the old slow orbit and old early endpoint. It is not the continuation of the newly corrected common early history.
- The passive future bound grants the coherent peak forever. It still leaves 142.43 times the charged gate (vacuum widths), or 37.97 times with all fermionic exits blocked. The proof covers arbitrary periodic Hermitian detuning and additional positive local absorption under the fixed production/width and mass-envelope assumptions. It does not cover an unspecified active/nonlocal medium or other depletion reactions.
- The terminal octet/triplet have nonzero gauge-pair loop widths: rest lifetimes 7.10557 ms and 10.9650 microseconds. Hence 83.84-times-DM neutral rest energy is intermediate storage, not final stable overclosure.
- Their conditional soft-gaugino decays produce very hot photinos: mean propagation 302.73/80.78 Mpc. Under the late-stage normalization their rest density is 9.01e-8 of DM. The soft vertex is not a certified on-shell amplitude, particularly the triplet's 15.3% gauge-parameter variation. Direct gauge radiation is separately counted; this is not the full mixed-branch radiation ledger.

## Corrected common early state

The durable fresh ancestry is

    integration/run_initial001
      -> integration/run_fresh_exact001
      -> integration/run_fresh_exact002
      -> history/run_advance001
      -> history/run_advance002

The larger-step comparison `history/run_advance002/result.json` reaches exactly N=.0021690179772784167, matching the old warm checkpoint's cooling interval. It stores full Y, explicit fermion vacancies, scalar action, field energy and cumulative independent expansion work. Its charged fraction is .80994571, Ycharged=3.03360147e-7, J=2.39257821e-6, modeled radial orbit 3.57673484–4.15575157, minimum 3.86322330, and maximum fermion occupation .56756. The old coarse checkpoint was .81331725 with nearly saturated soft bins. The corrected U1 yield differs by about−2%, while normalized U1/SU2/SU3 shapes change by roughly9–10%.

The preferred smaller-step state is `history/run_refine002/result.json` at the same exact N. It gives Ycharged=3.03394306e-7, charged fraction .81003691, J=2.37747533e-6, modeled orbit 3.58133729–4.15854681, minimum 3.86693704 and maximum fermion occupation .52896. Relative to the larger-step state, charged yield changes by .0113%, U1 by 1.14% and J by .631%. Its cumulative energy residual is5.22147e-13 mu^4, 23.846% of the remaining excitation, so the energy-work error did not converge under this step-cap change. Keep both states and the shared-prefix error visible.

These are finite common-state results, not final relic abundances. The cumulative independent work residual is−1.43954e-4 of the initial gas scale. It is about22% of the remaining orbital excitation, so the action and its 12.5% difference from the old trajectory are not precision-certified. Read `history/` for subsequent timestep and direct-orbit controls; the first two fresh jobs were honestly failed at their larger requested endpoint but retain useful positive prefixes. Their numerical ghost-cell stalls are not a physical pressure or vacuum failure.

`warm_coherence/` resolves a further local question using actual-x4-state matrices. The four massive singlets are S1_1[94..97]; S1_0 is the two-real-state massless modulus. Large internal coherent changes in P-only currents do not imply a large total warm correction. Read its final phase/trace bounds, keeping their two frozen-bath scope separate from the corrected trajectory and the full cooling history.

## First remaining implications

1. Establish convergence of the common field/action history at the orbital-excitation scale, including its inherited early prefix. A small error relative to total gas energy is insufficient when the oscillation energy has become small. The endpoint direct check tests a local orbit, not accumulated history error. `independent_review/energy_diagnostic/` tests the local action gradient and finite-step centering; it must not be read as a completed global correction. Algebraic collision-energy cancellation and independently differentiated bulk directions pass locally to parts-per-million accuracy. A reused finite BE/Heun step nevertheless has a nonzero energy defect, leaving discrete temporal/coupling accuracy as a live diagnosis rather than a normalization-factor correction.
2. Continue the corrected distributions toward the cold gravitational well with adequate soft and hard momentum support. The warm fixed q<=80 grid cannot represent arbitrarily late hard neutral decays. Do not splice old late populations onto the new early state.
3. Couple occupied neutral matrix populations and the actual memory kernel to that same state where needed. Warm frozen-bath bounds are not a uniform proof over a new history; the late passive result is a separate conditional branch.
4. Complete the on-shell neutral-to-two-gaugino three-point matching, including the missing finite momentum and gauge-completion pieces. A derivative of the gaugino threshold at zero external momentum is not that amplitude.
5. `vector_probe/` confirms a real open P→VV warm decay with 1.63–1.98% width-trace contribution (up to 8.95% as a coherent relative quadratic form), closed at the cold pole. Its kinematic eligible-parent coverage is not a missing-rate bound. Match the open warm broken-vector1-to-2 decays/inverses and any material vector/gauge 2-to-2 reactions and complete the mixed-gaugino/radiation ledger before a cosmological abundance/BBN claim. Propagate entropy and expansion consistently. No external portal, entropy dilution or new production sector has been introduced.
6. Check the full gravity/transverse stability requirements along any resulting cold history. Local spectrum health and a tuned vacuum normalization do not constitute a predictive dark-energy relation.

Every experiment remains separately bounded (one numerical thread, wall<=240s, CPU<=235s, measured RSS). Use fresh source versions/run directories, preserve failed sources and record exact dependency closures. Verify the current primary manifests; historical current-path validator differences must be explained by exact archived source bytes. `VERIFICATION.json` aggregates integrity checks and rechecks all 896 pinned prior TP06/CT09 artifacts.
