# FSP-008: full proton kernel route

**Outcome:** the full Born angular kernel is derived and benchmarked, including both scalar Compton amplitudes and the Born subtraction. A universal soft-photon coefficient of the physical charged-proton kernel follows under the stated massive-QCD analyticity assumptions. We also executed complete all-momentum point-Dirac convolutions. **The complete QCD proton response, its finite renormalization, the global vacuum response, R(alpha), and alpha remain uncalculated.** No numerical alpha or target coefficient was fitted or imported.

The complete first derivative in u=e² requires the vacuum-subtracted proton matrix element of two canonical currents, integrated against the photon propagator, with all quark-line contractions and current/action contacts. It also requires finite matching counterterms for the declared fixed-MSbar strong coupling/quark-mass path. In momentum space this uses the full angular combination `-3 T1(iQx,Q²)+(1-x²)T2(iQx,Q²)`, not just the subtraction line. [DERIVATION.md](DERIVATION.md) fixes the normalization, state convention and regulator.

The calculated Born kernel is

    M_u^B/m = (1/(2 pi²)) integral dz P(4m²z²) B(z),
    B(z) = z(3F1²-A)/2 + [(1+z²)A-3z² GM²](sqrt(1+z²)-z),
    A=F1²+z²F2²,  z=Q/(2m).

It equals the dispersive elastic integral **plus** the elastic Born subtraction of [WLCM 1203.0254v2](https://arxiv.org/abs/1203.0254v2). The extra subtraction matters: the linear-in-z contribution cancels. For a unit-charge proton with a gapped QCD spectrum, analytic form factors and a regular non-Born low-energy expansion, the finite soft Euclidean photon band therefore has

    lim_epsilon->0 M_u(0<Q<epsilon m)/(epsilon m) = 1/(4 pi²).

In alpha units this coefficient is 1/pi. It fixes an endpoint of the first electromagnetic mass kernel at u=0. It does not predict the full mass slope, justify extrapolation to Q of order m, or fix a gravitational H-linear coefficient.

For an independently specified point-Dirac verification theory, the full current kernel is exactly computable without any form factors. The finite band 0<Q<m gives

    M_u^D/m = (1+sqrt(5))/(64 pi²) + 3 log[(1+sqrt(5))/2]/(8 pi²)
            = 0.0234070168527004862797093949286.

The new [Erb–Meyer–Ottnad 2603.13086v1](https://arxiv.org/abs/2603.13086v1) photon regulator permits an all-momentum calculation. At Lambda=m, our complete point-Dirac integral is `M_u^D/m=0.0151027922649513257488119794161`. Ten Lambda/m choices are saved. Their ultraviolet-subtracted values approach the analytically derived regulator constant `(3/2-6 log 2)/(16 pi²)`. This constant is not silently relabeled an MSbar finite matching term. Point-Dirac results are kernel benchmarks in a different theory, not a physical-proton model.

A [separate calculation](DIRAC_MSBAR_MATCHING.md) then closes the finite matching for this elementary Dirac benchmark: dimensional regularization, including its evanescent numerator, gives `M_u^D,MSbar/m=[4+3 log(mu²/m²)]/(16 pi²)`. The exact PV-to-MSbar finite counterterm is `(5/2+6 log 2)/(16 pi²)` plus its scale logarithm. At mu=m the matched slope is exactly `1/(4 pi²)`. No datum is adjusted to obtain this constant. Its [own run](msbar_run_001/manifest.json) is completed and validates, preserving the original run's frozen inputs. This solves finite matching only in the elementary reference theory; using that counterterm for QCD would be incorrect.

The [bounded kernel run](run_001/manifest.json) has status `completed`; its current-input v2 manifest validates. It checked 14 exact identities, 24 independent numerical tensor-angle cases, five exact finite windows and ten all-momentum PV integrals in two integration variables at 60-decimal precision. The maximum angular discrepancy was about 1.50e-59; both PV quadratures agreed at the saved precision. The matching supplement checks six exact equalities and translates ten saved PV values. These are finite checks, not interval-certified estimates or full QCD simulations. See [results](run_001/RESULTS.json), [contract](COMPUTATION_CONTRACT.json) and [reproduction commands](REPRODUCE.md).

The 2026 factorization paper's actual lattice result is for HVP on an Mpi=286 MeV ensemble and excludes the counterterm. It improves a possible full-proton implementation; it does not provide proton data. The finite data search also authenticated [physical-point connected/disconnected elastic form-factor work, 1812.10311v2](https://arxiv.org/abs/1812.10311v2), as a promising input lead. Its numerical tables and full flavor inventory were not acquired/authenticated for use here, so no curve is digitized or substituted. The one inspected Zenodo lead was a presentation. No complete all-component physical-proton tensor dataset was acquired in this bounded search; no global absence claim is made. [Source receipts](SOURCE_RECEIPTS.json) record inspected pages, exact retained source versions and hashes.

The exact remaining step is to replace the formal physical-QCD F1,F2/non-Born tensor and all sea covariances with an authenticated numerical all-component observable, calculate its finite counterterm on the same parameter path, and combine the resulting M_u with the independent curved-vacuum A_u. The quotient derivative is `R_u=A_u/m³-3 R M_u/m`. A nonzero or universal part of M_u alone does not determine either term. This route supplies validated kernels and a physical infrared limit; it does not close that nonperturbative step.
