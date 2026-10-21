# Independent review of the first actual-pair analysis

The pinned `analyze_pairs.py` has no identified blocking algebra or implementation error. Its source terms, real-Y20 normalization, outgoing-sector sum and symplectic-coordinate conventions agree with the prior audited action. The completed `analysis_run_001` validates execution, conservative inventories and finite conditional coordinates. **It does not yet accept a weak persistent normal-mode energy or a collision-wide radiation law.**

This review did not execute field, eigenvalue, BVP, outgoing or projection routines. `sources_review_pair_analysis.json` pins source/cache/result bytes and records 114 passing receipt/arithmetic checks, including before/after receipt consistency. These are chiefly provenance checks, not 114 independent physics experiments. The original analysis has 183 passing declared controls and a valid v2 manifest. An independent sub-review by `/root/isolated_binding/charge_backreaction` found the same source-level conclusion.

## Source and reference bridge

The reviewed analysis SHA256 is `1919f140bad28a607064c13122bad9cc05f42d1537998a4ad38b0aa02c9682f1`. It correctly derives the canonical quadratic source N2 from the same Psi/X/chi action used by the field solver and prior natural-radiation calculation. With unit-angular-norm Y20, its three forcing weights are

    C0=1/sqrt(4pi), C2=sqrt(5)/(7sqrt(pi)), C4=3/(7sqrt(pi)).

The ell=0,2,4 source amplitudes and outgoing powers are combined correctly. There is no extra factor two or half: no-half K=1 applies to this real harmonic because the oscillatory energy term vanishes by Z^T GZ=0. The positive-time convention c(t)=A exp(i Omega t) matches the exploratory fit basis.

The Q136000/Q140000 caches come from the completed `matched_refs_run_004`, with 47 declared controls and retained earlier failures. Its discrete-profile metadata is explicit: these are interpolants of variational radial stationary references, not fresh continuum origin BVPs. Independent cache arithmetic gives unit kappa to about 1e-13, and the profile fields at all mode-grid nodes match the saved mode backgrounds to below 1e-12. This supports the radial API bridge, not exact stationarity on the cylindrical evolution grid or identification of either Q with uniquely bound collision charge.

The analysis now compares `reference_omega` and `fitted_omega` velocity frames, which is useful. Both still independently fit the **phase at each snapshot**. Therefore `reference_omega` does not by itself make the whole sampled trajectory a frozen carrier frame: theta(t) also needs theta_dot=omega_reference. In a weak reference perturbation the distinction is higher order; in this appreciably varying remnant, the derivative of the independently fitted phase need not agree with the frequency subtracted from momenta. This can affect the fitted coordinate rate. A separately authorized fixed-phase-propagation sensitivity is being performed in a new run; no old result is altered here.

## What the saved actual data establish

The in-phase reference-omega coordinates over t=80..240 are much larger than the isolated-static artifact (max isolated |c|^2=0.01123895). They are also stable under time-step halving and fairly stable across the two reference charges and tested frames:

| Reference Q | Conditional coordinate squared range | Maximum dt-halving change | Maximum spatial-refinement change | Maximum fitted/reference-frequency-frame change |
|---|---:|---:|---:|---:|
| 136000 | 377.50–2237.57 | 0.00926% | 9.47% | 1.91% |
| 140000 | 372.19–2207.77 | 0.00995% | 9.41% | 1.95% |

Changing Q136000 to Q140000 changes |c|^2 by at most 1.71% at these matched snapshots. This supports a reproducible large conditional quadrupole coordinate at the tested finite grids. It does not remove the reference/amplitude assumptions required to call that coordinate an independently stored mode energy.

For the same in-phase snapshots, the full canonical field mismatch over the projection sphere is about 0.45–0.59, and the ell2 displacement/velocity reconstruction residual fraction is about 0.10–0.53, with substantial late residuals. These norms include surrounding waves and other structure as well as the core; they alone do not prove a particular core-only mismatch. They do show that the full sampled state is not described by this single linear reference mode. The instantaneous carrier-frequency fit varies roughly -0.008 to +0.019 relative to the reference, and the X phase-lock diagnostic also varies appreciably. A one-peak axis diagnostic cannot convert these data into stationary-reference acceptance.

The seven t=120..240 complex-coordinate samples span only 1.153 reference cycles at Q136000 or 1.138 at Q140000. A constant, a positive-time fundamental and a positive second harmonic use six real linear coefficients, plus the searched frequency, against fourteen real observations. The frequency grid spacing 0.00005 is a search resolution, not a frequency uncertainty. The model omits possible negative harmonics and can fit nonlinear/gauge-mixed content. Its relative residual is normalized by the full coordinate including a constant component.

| Reference Q | Exploratory fitted rate | Reference Omega | Difference | Fit residual | Fundamental coefficient squared |
|---|---:|---:|---:|---:|---:|
| 136000 | 0.04910 | 0.0603874 | 18.69% lower | 0.02866 | 508.52 |
| 140000 | 0.04915 | 0.0595870 | 17.52% lower | 0.02918 | 502.12 |

Thus a low residual here is not independent confirmation of the cached linear eigenmode or a quantitative weak-mode K. A finite-amplitude coherent component could exist, but a nonlinear normal-mode interpretation needs additional amplitude/reference/gauge tests. The larger-separation run is sampled at the same absolute times despite a later encounter; it is not automatically a matched post-collision-age convergence test. Its exploratory residual is about 26%, which also does not close that issue.

## New reference radiation coefficients

The analysis obtains gamma_Y20=1.713591338e-5 at Q136000 and 1.671890928e-5 at Q140000, at L=60, N=1199. The outgoing work, residual, positivity and channel tests pass; only Psi+ is open. The two different reference charges should not inherit Q160000 rates without this calculation, and the script correctly recomputes them.

These are finite-reference weak-mode coefficients, not measured radiation rates of the nonlinear collision. No fresh box/mesh convergence of gamma at these two charges is performed in this analysis; earlier convergence at other charges is useful context rather than a substitute. Inserting the unaccepted fitted coefficients squared into gamma K/Omega would give about 0.144 and 0.141, so even that hypothetical single-mode slow-variation condition has not been demonstrated as a parametrically small quantity. No physical loss history is inferred from that insertion.

## Inventories and acceptance logic

The in-phase run ends with about 86.67% of total box Q inside r=20. Its net outward aperture-Q change is about 20205.6 and the outside-energy increase about 21013.5, whose ratio is 1.03998. This ratio combines signed inventory changes: it is not an asymptotic particle/radiation E/Q. The separated case even has negative net outward changes because it starts with more charge outside the fixed aperture. This demonstrates why the aperture warning must remain attached to these columns. No fixed core/wind mass budget follows from them.

The script imposes **no physical acceptance gate** on reference mismatch, amplitude, carrier drift, fit residual or persistence. Their failure to establish a weak mode leaves `all_checks_pass` true, because the implemented projection check is only finiteness. Its explicit conditional/exploratory labels accommodate this; a downstream summary must preserve that distinction. Passing 183 controls must not be rephrased as passing 183 mode-acceptance tests.

The calibrated outcome is: the finite full-action head-on evolution produces strong phase-dependent central concentration and a large, time-resolved conditional quadrupole coordinate above isolated grid artifacts. Acceptance of its magnitude as a weak normal-mode energy, extraction of a nonlinear mode frequency, and application of the weak gamma K^2 cooling law remain unresolved. No asymptotic escape, nonzero orbital-J transfer, physical mass/time normalization, population branching distribution, or four-dwarf mass/stellar-heating closure has been established.
