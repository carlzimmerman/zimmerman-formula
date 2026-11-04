# CT09 focused transport review

**Normalized claim.** For e=h=lambda=.003, g=sqrt(29/200)e, conditional initial frozen massless FD charged fermions at xi=.02, and the stated retained gravity action, the two-species momentum network is intended to furnish a charge- and energy-consistent history into a cold vacuum, with irreversible heavy-charge depletion and a cold photino population. The actually computed assertion is narrower: an equal-charge, unpolarized, finite-cell, action-averaged network with vacuum conversions, optimistic neutral-parent absorption, and an auxiliary massless-radiation energy ledger.

**Primary verdict: incomplete, with the smallest missing implication being the identification of this reduced collision operator with a physically irreversible, statistically consistent reaction network on the oscillating background.** Neither the finite NWA histories nor the static finite-width pole packet establishes that implication. This is not a universal no-go for trapping or weak production. Several useful discrete invariants do pass under the declared closure.

Review date: 4 November 2026. Fresh focused subagent review from raw derivation, code, tables and results; no implementation edits outside `transport_review/`. Review independence is a fresh reconstruction, not a claim of different-model independence. Exact hashes and manifest-validation records are in `PROVENANCE.json`.

## Dependency graph and obligation matrix

The required implication is:

1. Physical charged masses and inclusive vacuum vertices -> static conversion and pair-production kernels.
2. Kernels plus scalar/fermion occupation conventions -> a positive, charge-consistent, energy-consistent discrete generator.
3. A short correlation time and valid averaging hierarchy -> local, action-averaged kinetics on the changing scalar orbit.
4. Actual parent/cascade/neutral/gaugino distributions, including inverse reactions and statistics -> irreversible depletion, the correct force, and a photino momentum distribution.
5. A matched potential and spectrum, with controlled numerical error and continuation -> vacuum capture and the joint charged/photino targets.

Leaves 1-2 have substantial finite checks. Leaf 3 is conditional; leaf 4 is not supplied. The leading packet aligns its own stationary point with the tree scalar threshold, but this is not full finite mass/potential matching in leaf 5.

| Obligation | Result | Meaning |
|---|---|---|
| Fermion/scalar carrier normalization | Passed algebraically under equal populations | fC=2 fS compensates 12 scalar versus 24 fermion degrees; scalar inverse production has the required factor four. |
| Signed charge | Correct only in the stated symmetric sector | No separate positive/negative distributions are evolved. Charge zero is preserved by the charge-conjugate symmetry assumed in every reaction. General nonzero-charge evolution was not tested. |
| Conversion carrier count and positivity | Passed, finite checks plus matrix argument | Conversion columns sum to zero; off-diagonal entries are nonnegative. The matrix exponential preserves nonnegative carrier counts. |
| Conversion daughter energy | Passed inside represented daughter-energy range | Linear energy interpolation is exact there. Endpoint clamps give finite exceptions. |
| Pair-removal normalization | Passed algebraically; finite quadrature error quantified | Absorption removes two opposite-charge carriers per produced real parent. |
| Scalar/particle/radiation energy | Passed for the reduced bookkeeping, conditional for the full system | Removed bin energy is counted once. Omitted massive neutral forces and bath distributions are not certified by this identity. |
| Correct charged momentum shape | Conditional, not converged as a trajectory | Finite-cell sensitivity remains; daughter statistics and spin/state closures remain assumptions. |
| Phase quadrature/action averaging | Conditional | Old pole-location error and cold subtraction failure are real; matched leading improves these. Neither a short collision correlation time nor all phase/momentum errors is established. |
| Actual irreversible depletion/cold photinos | Not addressed by a completed physical network | Parent absorption, a gaugino event count and a radiation energy scalar cannot supply the required distributions. |

## Independent reconstruction of the collision and daughter maps

For one real parent of mass M, width Gamma to the selected charged species, m<M/2 and beta=sqrt(1-4m^2/M^2), start with the parent momentum and rest-frame decay angle:

    gamma = Gamma M/(2 pi^2) integral dP P^2/EP <f1 f2>angle.

The change E1=(EP+beta P z)/2, E2=EP-E1 gives Jacobian 2/(beta P), hence

    gamma = Gamma M/(2 pi^2 beta) integral_allowed dE1 dE2 f1 f2,
    |E1 E2-(M^2-2m^2)/2| <= p1 p2.

This independently recovers the project's ordered-domain normalization. With wi=24 Tc^3 Wi/(2 pi^2), the fermion kernel coefficient 2 Gamma M/(24 beta) gives sum wi dfi/dtau=-2 gamma. With physical scalar occupation fC=2 fS, the scalar coefficient must be four times larger, 8 Gamma M/(24 beta), as implemented. Symmetrizing the cell area preserves the summed number identity; it does not remove finite quadrature error or derive the distribution.

For conversion A->B+massless neutral, the exact unpolarized two-body map is

    EB=(EA (mA^2+mB^2)/2 + p (mA^2-mB^2) z/2)/mA^2,
    rate=GammaA mA/EA.

The eight-angle deposition is a stochastic matrix P: each parent loses one carrier and deposits one charged daughter. Adjacent energy-cell weights satisfy sum P=1 and sum EB,cell P=EB,target whenever the target is inside the represented interval. After isotropic angular averaging the emitted energy per parent per tau is GammaA(mA^2-mB^2)/(2mA), independently of its momentum. The implemented generator and this independently derived moment agree in the tests below. This is a massless-neutral boost approximation; the input widths themselves include the small neutral mass.

For the new static finite-BW kernel, sigma is a physical particle-antiparticle pair cross section. In the symmetric sector n+=n-=n/2, gamma=n^2<sigma v>/4 and total carrier loss=2 gamma. Therefore

    Kij = PREF Tc^6 Wi Wj <sigma v_Moller>ij / 2

is the correct insertion into the existing scalar loss formula. The factor s/(4 Ei Ej) converting the CM sigma-v to the Moller pair flux is also correct. Removing the four constant-parent NWA scalar terms before adding this kernel avoids their double counting inside the declared |x-xpole|<.05 window. This algebra does not establish stationary-background applicability or control the window's omitted tails.

## Decisive finite checks and existing run statuses

An independent v2 run, `run_checks002`, completed with all declared invariant checks. It compared the implemented scalar pole kernel against an independently evaluated parent momentum/rest-angle integral, retaining exactly the same interpolated width/beta coefficient. Parent P/Tc was integrated to 100, with 256/512-node repeat differences below 1e-7 at the three points. There is no certified tail bound, and this tests the stated frozen FD diagnostic rather than every later nonthermal shape.

| Bulk bins | Initial FD number error | Scalar kernel relative error at the three cold points |
|---|---:|---:|
| 24 | -2.0089% | -7.68495%, -5.05733%, -6.71588% |
| 32 | -1.11975% | -4.28085%, -2.83706%, -3.79481% |
| 64 | -0.279354% | -1.13778%, -0.708232%, -0.966545% |
| 128 | -0.0746782% | -0.345523%, -0.182691%, -0.267220% |

The points are (x-xpole,Tc)=(-.001,.0005),(-1e-5,2e-5),(-1e-6,1e-5). Initial counts are compared with integral q^2/(exp(q)+1)dq=1.8030853547393915. These errors explain part of the grid-dependent initial Y; no rescaling was silently applied. At fixed bins the comparison also includes the cell-constant occupation approximation, so it should not be attributed entirely to the four energy-quadrature nodes.

Conversion tests used six (x,Tc) points on both sides of the mass crossing, including Tc=1e-5. Maximum column-sum error was 1.04e-25 and every off-diagonal entry was nonnegative. FD-weighted emission-energy errors were below 4.98e-8. Individual parent-cell errors reached 1.23104% in an extremely small high-momentum tail because endpoint clamping loses exact daughter energy. The stored maximum energy overflow is not an occupation-weighted error bound for arbitrary later distributions.

Additional issues are visible directly in the raw artifacts:

* `resolved.py:10` placed the scalar threshold at sqrt(4*.006/e^2-2/(31e)), while the actual charged scalar formula requires sqrt(.006/e^2-2/(31e))=25.4000254000381. `resolved_v2.py` fixes this. The successful historical extended v1 result is therefore not a phase-resolved late scalar-pole history.
* `run_candidate_extended2_001` is a **valid failed record**: at N=3.4906651, Tc=1.41956e-4, it reports a 327418 relative period change and rate/omega=35.5552. Recomputing E-V-rho after switching to a tiny harmonic orbit can destroy the stable harmonic endpoint cancellation. This output does not demonstrate physical loss of averaging or physical escape. `Accurate` uses a force root and harmonic phase weights to avoid that specific failure.
* The tabulated near-threshold scalar mass was rounded to 12 decimals upstream (`scalar_network.py:73`). At x=25.4000254, `scalar_kernel` divides the width by beta reconstructed from this rounded value. Its width/beta coefficient is 7.36012e-8, versus 8.45792e-8 at the adjacent x≈25.4 point: an artificial approximately 13% drop close to threshold. The independent kernel benchmark intentionally keeps that coefficient unchanged; this input-interpolation error is additional. The new finite-BW replacement avoids that particular reconstruction for its selected pole.
* At Tc=1e-5 the completed matched-leading 24/32 runs give survival 5.93280e-6/5.06989e-6 and Y=2.17745e-12/1.87763e-12. The 14.5% survival change is not trajectory convergence. Charged RMS q changes 3.31183->3.27416. Their present charged rest-energy yields are 1.68665e-7/1.45441e-7 GeV, well above the 4.4e-11 GeV charged gate; no inference about an uncomputed later epoch follows.
* The action equation is reconstructed correctly from dJ/dE=Torb/(2pi), the averaged parameter derivatives of J, and scalar Hubble friction. Its collision term is the stated energy-rate covariance. `two_species.py:59` nevertheless clamps negative covariance corrections when log(J/J0)<-20. A separate v2 check `run_action001` finds the clamp **inactive at both saved matched-leading final states**: raw dlogJ/dN=-2.9999997127/-2.9999996741. This does not establish inactivity at every earlier step. There is also a log-J lower floor at -30.
* The local polynomial/spline joins at +/- .0018 have potential discontinuities below 2.21e-26 mu^4 in the finite check. This is small for the inspected trajectories, not a uniform smoothness proof. The leading profile ends at x=40, while the inherited `orbital` fallback still probes the spline at x=200 to form a barrier/action limit. Saved turning points remain below 40; a global barrier or escape claim is not certified by this extrapolation.
* `run_bw_control_001` checks angular integration, not radial-cell convergence. `run_bw_normalization3_001` passes the inclusive production/degeneracy normalization but fails its momentum-refinement check: the 64/128 BW-to-NWA loss ratios are .757555/.773217. That is a valid failed numerical-control record, not evidence of a factor-of-two mistake.
* `run_leading_bw_001` timed out after 240.05 seconds without its declared result. Its outcome is resource inconclusiveness. It supplies no completed finite-BW coupled trajectory.

All 23 manifest records selected in `PROVENANCE.json`, including failed and timed-out records, validated against current input/output hashes. Validation says that a record is internally valid; it does not turn a failed result into a pass.

## Local resonance rates, parent lifetimes and physical scope

There are two distinct reductions: averaging a specified local collision generator over a fast field orbit, and deriving that local collision generator in the first place. Checking H/omega and charged-loss/omega addresses only the first. It does not calculate the bath correlation time or establish frozen-background resonance scattering.

[Drewes, Mendizabal and Weniger, arXiv:1202.1301v2](https://arxiv.org/html/1202.1301v2), section 3, assumptions 1-3 and equation (8), derive kinetic behavior with localized self-energies and separation between correlation, damping and background-variation scales. They explicitly discuss the extra care required near thresholds and resonances. Their hypotheses do not identify the parent's lifetime with the correlation time relevant to production.

Consequently **Gamma_parent<omega_field alone does not invalidate a weak-production Markov source**. A continuum of incoming states can dephase rapidly even when the produced parent lives longer. Conversely, a small production rate alone does not establish a stationary Breit-Wigner kernel on a narrow pole that is swept by the background. The needed correlation/dephasing or explicit dynamical calculation is absent here. This is a conditional source application, not an external theorem proving or disproving CT09.

The saved matched-leading final states quantify why the two issues cannot be conflated:

* omega/mu=2.17363e-8; the four neutral-width eigenvalues are 1.30557e-9 to 2.50066e-9 mu. Thus Gamma/omega=.06006-.11505, and parent lifetimes are approximately 1.38-2.65 full orbital periods. Prompt decay within a single orbit is not a valid elimination argument. These parents still decay much faster than H, so cosmological elimination could be justified with a suitable orbit/cascade treatment.
* The phase sweep at the pole gives |d(M-2m)/dtau|/Gamma^2≈935-3982 across the two states and width eigenmodes. These are diagnostics of a rapidly swept *narrow detuning*, not a calculated memory correction or a proof that all Markov production fails.
* The final charged RMS single-particle kinetic energy is about 1.38-1.42e-8 mu. Its inverse is of order an orbital timescale, while the pole is narrower. An actual pair correlation/dephasing calculation is needed; substituting either 1/m or 1/Gamma without justification does not settle it.

The coherent pole matrix is a valuable static vacuum scattering input. Treating its scalar parents independently may preserve the total empty-parent production trace, but does not derive their subsequent coherent/medium branching. An actual finite-width exit already includes its neutral branching and incoming width; it is not the same process as absorbing every produced neutral parent.

## Remaining physical gap and strongest safe statement

The missing collision factors include final-state Bose enhancement and Pauli blocking, occupied-parent inverse decays, and gaugino inverse conversions. Schematically, F->S+lambda involves fF(1+fC)(1-flambda) minus the inverse fC flambda(1-fF), with momenta evaluated on their actual daughter map. Pair inverse production similarly needs its occupied-parent reverse term. Empty daughter occupation is an initial condition, not a preserved theorem. Carrier count cannot be interpreted as irreversible loss when a neutral parent regenerates charged daughters.

The omitted neutral cascade can carry rest mass and field-dependent energy, hence a force. Assigning all removed particle energy to massless radiation makes the reduced energy identity close, but changes that force and redshifting law. Charge-preserving conversions also change force and momentum; zero collisions is not a substitute for the actual conversion network. Finally, an integrated gaugino event count and radiation energy do not identify photinos among the neutral products or determine their momentum/coldness distribution.

**Strongest safe statement:** the specified symmetric, unblocked reduced network has the correct carrier normalization, positive conversion map, number identities, and a consistent discrete energy ledger within its approximations. Static FD kernel accuracy improves with cell refinement, and a matched leading potential permits finite computed positive-X bounded orbits through Tc=1e-5. The present 24/32 histories are numerically sensitive, historical pole results contain identified artifacts, and no completed physical vacuum-capture/heavy-depletion/cold-photino history follows. The new finite-width insertion has the correct pair-count factor, but its full history is currently resource-inconclusive and its dynamical locality remains conditional.

The cheapest further numerical check is to stabilize normalization/cell integration and use common initial physical counts before comparing trajectories. The decisive physical check is a bounded one-orbit weak-production calculation with the actual time-dependent detuning, parent density matrix/decay hazard and daughter force, compared to the local rate after independently measuring dephasing. Neither task should silently rescue the audited output or be reported as a completed cosmological history.

## Execution and provenance

Own authorized checks used the installed mathbox v2 runner, wall<=180 s, CPU<=175 s, one numerical thread, measured process RSS, no address-space or affinity cap. `run_checks002` completed in 2.462 s runner time (0.856 s child work), peak RSS 115097600 bytes; `run_action001` completed with 0.185 s child work, peak RSS 75268096 bytes. Software: Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4, mpmath 1.3.0, macOS arm64. The first check attempt `run_checks001` failed only while serializing a NumPy Boolean; its source and failed manifest were retained, and a separately named corrected script produced the completed record.

Commands and exact input closures are in the runner manifests and contracts. Verification was:

    python3 <installed computation-audit>/scripts/validate_manifest.py MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula

This was applied to the selected records listed in `PROVENANCE.json`. No project implementation was changed by this reviewer. The recorded shared commit in these runs is cf9242edf7a71bcaed424d8f4f2d550b21ddc19e with dirty=true; the hashes, rather than that moving shared commit, identify the actual reviewed revisions. The external source was authenticated/read through the web tool; no local source copy or source-cache hash was created.

The companion `PROVENANCE.json` pins 99 artifacts, includes every selected manifest's input closure, and records the exact successful validations and unsuccessful run statuses. It is the authoritative hash inventory for this review.

## Final-checkpoint addendum: completed late hybrid segment

This addendum reviews the subsequently completed `kinetics/run_hybrid_bw_001`, `run_hybrid_control_001`, `run_source_diagnostic_001`, and `gravity_resonance/run_continuation002`, together with their raw code and manifests. It also records the later static `run_bw_normalization4_001` control. No new physics calculation or trajectory was run by this reviewer for the addendum. The primary verdict remains **incomplete**.

`resume_bw.py` reconstructs the 24-bin matched-leading NWA endpoint's scalar/fermion cell populations, action, comoving radiation and integrated work at Tc=1e-5. Its work reconstruction preserves the existing energy-ledger discrepancy rather than resetting it. It then switches to the local static coherent finite-BW scalar-pole kernel and evolves to Tc=1e-6. This is a completed **hybrid** history with an explicit change of collision model; the successful late continuation is not a full finite-BW history from the original initial state.

The hybrid result has `partial=false`, all three declared checks true, and 233 accepted steps with no rejected steps. It ends at N=8.44618219 with charged survival 1.71731386e-6, Y=6.30287893e-13, and energy-ledger error 1.12378417e-4 in the original initial-gas-energy normalization. The maximum reported local rate/omega is 1.08516e-4. Its turning points are 25.4000220544 and 25.4000287457, inside the retained potential domain. The conditional charged yield is **1109.59 times** the 10%-DM charged gate Y=5.68037557e-16. Gauge emissions per initial carrier remain .2584292125; no late photino distribution is generated.

The completed endpoint control doubles angular nodes 12->24 and then phase nodes per split 4->8. Number loss/H changes .5182678723->.5182678887->.5183044087: approximately 3.16e-8 angular and 7.05e-5 phase relative differences. The action derivative remains approximately -2.999999999187. These are useful checks of the **instantaneous static kernel at one fixed endpoint**, not abundance convergence, radial-cell convergence, or a dynamical locality test. They do not remove the earlier 24/32 trajectory sensitivity.

The later 64/128/256-bin static normalization control passes its stated thresholds. At x=25.399, Tc=.0005, the 256-bin BW/NWA loss ratio is .767085624 versus the coherent neutral-exit probability .769839063, a .3577% discrepancy; the 128->256 ratio change is approximately .793%. This strengthens the static pair-count and branching normalization check. The earlier failed normalization3 record remains retained, and this single prescribed FD point does not establish convergence of the 24-bin hybrid history.

The direct-source diagnostic estimates only the named F<->S+gaugino conversion contribution. With the explicitly assumed U1 fraction 1/6, it obtains Ychi=1.58080988e-8 and .00376271 of the DM energy budget, or about **.376%**. Its photino mass input is .00010473075 GeV and the numerical initial charged yield is 3.67019627e-7. The 1/6 split uses the massless Casimir limit. This estimate is not an inclusive upper bound on neutral cascades, a bath-consistent yield solution, or a cold momentum distribution; the auxiliary radiation ledger is correctly not reinterpreted as photino abundance.

`run_continuation002` starts from this specific completed hybrid endpoint and grants permanent pole alignment, the maximum fixed-coefficient scalar-pair cross section at every velocity, and removal of all neutral exits forever. Its comparison uses

    dY/dt = -s sigma_max Y^2/2,
    Yfuture >= [1/Yendpoint + s_endpoint sigma_max/(2 H_endpoint)]^-1.

This follows within the stipulated factorized symmetric pair model by bounding the future integrated loss with the redshifted initial visible-radiation comparison. The resulting remaining yields are 1.22787916e-13 for vacuum widths and 2.37285597e-14 after granting complete blocking of every FFS neutral width. They remain **216.16 and 41.7729 times the charged gate**, respectively. The latter is an intentionally favorable auxiliary positive-width model, not the result of evolving an actual blocked bath. The conclusion is restricted to this endpoint and this fixed pole coefficient model. It does not bound uncomputed early histories, additional loss channels/poles, pair correlations, changing self-energies or a full nonlocal medium operator.

The earlier full `run_leading_bw_001` timeout is unchanged and retained. The hybrid completion updates the record of what finite late evolution exists; it does not close the correlation-time/locality, delayed parent/coherence, statistical/inverse-reaction, massive-neutral-force or photino-distribution gaps identified above. All five addendum manifests validated against their current complete input/output hashes. Their exact hashes, raw source/input closures, run statuses and validation outputs are appended as a separate snapshot in `PROVENANCE.json`, preserving the original 99-artifact review snapshot.
