# Latest results and a concrete way forward

19 October 2026. Checkpoint LRP-2026-10-19-01. The physical theory and all-time kinetic confinement remain open. This review produced bounded empirical checks and analytic lemmas, not a completed theory or a validated new universal constant.

## What the latest results change

CFG854's symbolic fit did not validate a new formula because its power control failed. CFG856's extra circular speed, calibrated at 9.42 km/s on selected Milky Way dwarfs, is compatible with its held-out SPARC test but fails its literal universal-amplitude gate on M31. CFG857 finds no significant size dependence. CFG855 finds that simple numerical expressions near 5.364 occur at an ordinary look-elsewhere rate. None of those results derives a new physical parameter.

CFG853 excludes its specified common-fragment dynamical-friction transport, including the Sextans-independent comparison; it does not exclude all cold-core histories. The newer full-feedback kinetic result `ZAR-2026-10-19-09-CL` supplies an exact bare-response obstruction and a conditional resolvent route, leaving embedded modes, frequency geometry and nonlinear work control open. The newer condensate packet `CL-2F-2026-10-19-01` reports progress on classical linear nonradial stability and a continuation toward the MeV benchmark; its polar GR transfer, formation, abundance and nonlinear/quantum limitations remain material. These existing packets were read, not scientifically rerun or certified by this review.

CFG858 completed during this review at commit `62bedfa6b`: all six tested dwarf profiles were screened by the stiffness term, rather than supplied with extra acceleration, on both footings over its stated length grid. Its reported sign-flip control produces overshoot. This is the stored lane's finite result, not a universal comparison theorem or a scientific rerun here. The 31 pc numerical coincidence is not a mechanism.

## New empirical check

The raw M31-minus-Milky-Way log extra-speed gap decomposes exactly as

    +0.181680 dex = +0.191404 dex - 0.009724 dex,
                    law velocity    normalized excess

because `log Vx = log Vlaw + 0.5 log10(10^Delta - 1)`. The selected hosts have different stellar-mass distributions and nearly equal mean Delta. Equal baryonic acceleration does not imply equal law circular velocity. This algebra explains the raw geometric-mean split without establishing that every host-conditioned signal is an artefact: CFG857's size-conditioned coefficient still contains a normalized-excess contribution of +0.131636 dex with descriptive bootstrap SE 0.061230. Its design codes both Milky Way and field objects as the reference, so the coefficient compares M31 with that pooled reference. An independent satellites-only check still finds a +0.151084 dex size-conditioned extra-speed coefficient on the canonical footing.

The new forward check retained all 29 existing CFG828 dwarfs, including the four canonical near/below-law rows excluded by CFG856/857. A constant added variance and a proportional-law model gave almost tied whole-host predictive errors over all 24 satellites (0.1628 versus 0.1590 dex in log dispersion). Restricting to 16 low-acceleration satellites apparently favors the proportional model (0.1938 versus 0.1453), but removing Hercules reverses that ranking. The descriptive bootstrap interval spans zero. **No model preference is established.** These are equal-object prediction scores, not a measurement-error likelihood or a correction of the original selection function. See [the empirical packet](empirical/README.md).

## Two analytic checks make the next fit more discriminating

The whole-tracer projected virial identity gives `3 S = <r g>`. Therefore an added `Vx^2/r` acceleration changes the global LOS variance by exactly `Vx^2/3`, irrespective of tracer profile or anisotropy. A common independent constant LOS variance gives the identical global moment. Multiple populations can falsify their shared residual prediction, but identical global residuals cannot separate these two explanations. The next fit must use resolved information, matched selection and physically consistent populations. The [derivation and radial kernel](VIRIAL_AND_PROFILE.md) include a 13-check numerical fixture and a mutation that fails all nine projection comparisons. The Plummer/isotropic radial example is explicitly a formal Jeans fixture, not a positive-distribution physical realization.

The [kinetic endpoint derivation](KINETIC_ENDPOINT.txt) supplies a useful admissibility gate. An isothermal component reacts to total gravity, so on an exact flat-speed segment `2 s_c^2 = Vx^2 + r g0`; the familiar `s_c=Vx/sqrt(2)` requires self-dominance. A nonnegative isotropic energy distribution also obeys `rho_Psi >= rho/(2 Psi)`. With the full deep-law response to cored baryons, central acceleration proportional to `r^(1/2)` requires at least an `r^(3/2)` density drop, rather than an exactly quadratic-flat core. A positive lowered-Maxwellian distribution constructs a finite endpoint class under an explicit potential-depth condition. Its state parameters, supply, formation and stability are not selected by that construction.

## A genuinely different analytic continuation

The [critical-frequency screening proof](KINETIC_SCREENING.md) establishes an exact comparison model where bare resonant work grows as log time, but full finite-rank feedback gives

    sup_t |W_g(t)| <= 2(1 + nu_c/g),  g>0.

The mechanism is spectral: a resolvent varying as `1/log` can have a jump density vanishing as `1/log^2`, which makes accumulated work bounded. Consequently the bare logarithm does not by itself close the feedback route. A broader local cancellation lemma and rank-one inversion identity are included.

The next analytic task is to isolate the actual equilibrium's critical-frequency channels and test the **regular dressed inverse** and its scalar `ell((I-R)^(-1)v)`. A nonzero bare diagonal is insufficient. The note's proposed local shell reduction remains conditional on the stated geometry and operator regularity, and has not been independently audited here. Global harmonic summation, edge behavior and nonlinear actual-path work remain separate obligations. This is a new direction relative to the current checkpoint, not a global novelty claim.

## Recommended continuation and evidence

Prioritize a homogeneous resolved stellar fit retaining Hercules and other near/below-law controls, holding out a whole host and conditioning on law velocity or mass. Start from nonnegative distribution functions in the same total potential, not an arbitrary smoothed mass curve. Existing Sextans population data offer a concrete test, but their selected Gaussian widths are not already certified whole-population virial moments. In parallel, test the dressed critical-frequency scalar before assuming frequency extrema make the kinetic route fail.

All new work is isolated in this directory. The campaign ledger, sealed predictions, manuscripts and other researchers' jobs were left untouched. The target and ancestry are in `TARGET.json`; the request began at `18a81657e3e77d81f152fa73ca558dbc85ab6414`, the empirical snapshot observed `bb25c4ddd46bbecfbad2e32c88a9802ac0e55cc2`, and the final source review observed `62bedfa6b6c363eb17ac4a21c24194d847e76f3b`. Inputs and results are pinned by hashes. The three empirical manifests and the main projection manifest record completed runs; the projection mutation records an expected failure.

The [fresh mathematical audit](MATHEMATICAL_AUDIT.txt) independently rederives the bounded priority lemmas under their stated hypotheses. It does not audit the actual-shell operator reduction. The [fresh empirical audit](EMPIRICAL_AUDIT.txt) reconstructs the inputs and refits the prediction models by a different optimizer, confirming all pooled and single-deletion scores within 1.2e-9 dex; it audits rather than reruns the bootstrap loops. These are same-team independent checks, not external peer review or formal certificates. The copied empirical packet remains byte-for-byte unchanged; the pooled-reference clarification was added only to this review's summary, so the original packet inventory remains valid.

Replay the empirical calculation in a fresh scratch directory with `python3 reviews/latest_results_push_2026_10_19_codex/empirical/replay.py` from the repository. Profile-run argv and tolerances are in its v2 manifest. The independent audit checker retains its original scratch paths as an execution record. `CHECKPOINT.json` records evidence scope and continuations; `PACKET_SHA256.json` inventories this review.
