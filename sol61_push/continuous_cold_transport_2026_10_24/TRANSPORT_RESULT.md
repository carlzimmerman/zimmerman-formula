# CCT-002 outcome: some anisotropic export, no successful core formation

Six completed dimensionless wave-Poisson runs, at 48^3/64^3, tested the proposed conservative mechanism with a ledgered absorbing boundary. They do not establish an observational four-dwarf solution or a physical radiation efficiency. They are a new candidate model, not v3s or the shared L1 engine.

## Measured result

| run | mass removed | initial Jz removed | initial/final half-mass radius | J-ledger residual |
|---|---:|---:|---:|---:|
| spin, 48^3, L24 | 1.942% | 19.62% | 0.911 | -6.74% |
| reversed spin, 48^3 | 1.942% | 19.62% | 0.911 | same magnitude |
| no spin, 48^3 | 1.076% | not applicable | 0.911 | absolute drift <1e-9 |
| spin, 64^3, L24 | 1.939% | 19.69% | 0.918 | -6.66% |
| spin, half dt, 48^3 | 1.939% | 19.60% | 0.911 | -6.74% |
| spin, padded L32 at same dx | 1.825% | 23.57% | 0.911 | +0.0070% |

The positive spinning cases have a nonzero angular-momentum-carrying outgoing component by the measured boundary ledger. We did NOT measure its individual harmonic amplitudes, certify a free far-zone spectrum, or show that everything absorbed is unbound. There is no binary collision term.

Time-step and resolution comparisons pass their stated 10%/0.01 observable tolerance; reversed-spin symmetry passes. The L24 cases FAIL the frozen 2% angular-ledger gate. Padding reduces that residual dramatically and changes the spin-export estimate by about 20%; therefore the base-box number is not a converged physical transport coefficient. Energy-ledger residuals are <=7.4e-6 of initial |E| in base cases and 4.1e-6 in the padded case. The absorber's removed Hamiltonian is positive in these cases, but its interpretation as energy at infinity is not certified: the periodic zero-mean potential changes its reference with box size and changing total mass.

Most decisively, **all six cases fail the 1.5 contraction target and the final-quarter stationarity target**. All spinning cases fail the 50% spin-export target. Half-mass radius expands by about 9–10%, with ~17% late variation in the representative spinning cases. Even after the angular ledger is improved, this initial patch has not formed the requested low-spin dense core by T=30. A smaller core containing a minority of the mass is not excluded by a half-mass-radius diagnostic; that would not establish the near-total retention needed by the older Sextans branch.

Observed process peak memory was <=114 MB on macOS (ru_maxrss is bytes); one numerical thread. No heavy job or automation was started. The attempted nice adjustment and process inventory were sandbox-denied, so no priority adjustment/process inspection is claimed. The first run failed at JSON serialization after the numerical loop; this was a numpy scalar encoding issue, repaired without changing the numerical algorithm and rerun. FAILED_ATTEMPTS.json retains it.

## What the Sextans comparison actually says

The older source audit gives only 1.146% of remaining cold stock outside the target core, or q=M_out/M_core=0.011593. It also reports a separate newer population/stock problem, so this is a conditional reference branch, not an agreed observational budget.

The toy spinning patch loses 1.83–1.94% of its initial mass while removing only 20–24% of its spin and failing to contract. If that normalised total stock were identified with the older Sextans stock, it would exceed the receiver allowance before forming the core. This is a failure of that mapping, not a measured Sextans prediction or a no-go for all field initial states. The toy eta, initial shear and widths were specified, not derived from dwarf histories.

There is a useful mode-capacity restriction independent of the toy rate. In CCT-001's nonrotating Gaussian core family, eta=sqrt(G M_c R_c/C), C=3 sqrt(2pi)/2. Outgoing free modes with |m|<=m_max obey

    lambda_removed = |Delta Jz|/[M_c sqrt(G M_c R_c)]
                   <= m_max q/sqrt(C).

At the older receiver allowance, m_max=2 permits lambda_removed<=0.01196; m_max=8 permits <=0.04783. These are dimensionless spin capacities, NOT measured primordial spins. High-m modes or a larger mass allowance could change this, but their excitation and escape must be calculated, not selected to fit. Our simulation did not restrict its spectrum to |m|<=2, so the quadrupole bound is not its measured mode count.

A separate compact-launch constraint sharpens the energy/spin tradeoff. For an initially bound patch, final nonrotating Gaussian core and no external energy source, available escape energy is at most alpha G M_c^2/R_c with alpha=1/(2 sqrt(2pi)). A ballistic/WKB test-mass envelope launched at R_c in -GM_c/r has K_launch <= (alpha+q) G M_c^2/R_c. Cauchy–Schwarz then gives

    lambda_removed^2 <= 2 q (alpha+q),
    q_min = [sqrt(alpha^2 + 2 lambda_removed^2)-alpha]/2.

This diagnostic is conditional on that launch geometry, energy bound and negligible envelope self-gravity. It is NOT a bound on all coherent stress fluxes, tunnelling waves, external tides or other radiation fields. Launching farther out or exchanging spin with a bound outer envelope changes it. It exposes why an outer receiver can be physically necessary even when waves exist; no mass-free sink is licensed.

## Gravity and the other two dwarfs

No Fornax/Leo I pass can be claimed: no live stellar tracer or their radial likelihoods were evolved. Moving mass just outside an aperture still acts on outer stars, as the source receiver audit already shows.

The wave simulation has only Newtonian Poisson gravity. It therefore does not derive the original baryonic acceleration law. If one instead sources unchanged spherical AQUAL with both masses,

    g mu(g/a0) = G (M_b+M_c)/r^2,

then g is increased relative to the baryon-only law. In the deep limit the ratio is sqrt(1+M_c/M_b). This is an added-source response; whether it is a duplicate depends on the action and which mass was already represented by its held field. Adding a direct Newtonian cold force on top of this already cold-sourced AQUAL solution counts the cold response again. Conversely, baryon-only AQUAL plus cold Newtonian gravity is a phenomenological split until derived from one reciprocal action. None of these variants inherits the toy's evidence automatically. capacity_and_coupling.json records all three algebraic recipes without treating any as the derived framework.

Thus the tested prescription DOES NOT meet the joint requirement: sufficient selective core formation, allowed four-dwarf masses/heating, and a gravity coupling without double counting.

## Next obligation, without tuning four efficiencies

First derive or explicitly choose the reciprocal galaxy-law/cold-field action. Then test an early, bound rotating patch with an extended live receiver and compare it against this failed initial patch. Before interpreting higher-m emission as a solution, measure its frequency/amplitude and its positive-energy outward flux, and retain host tides and stellar heating in the eventual dwarf mapping. Use a single eta and a generated distribution of density/spin histories; do not give Draco and Sextans individually chosen collapse efficiencies while manually clearing Fornax and Leo I. The old/new Sextans stock likelihood must also be reconciled.

This route remains OPEN, with failed initial conditions and numerical-boundary limitations preserved. No frozen criteria, publications or shared navigation were changed.

Reproduce small diagnostics: `python3 sol61_push/continuous_cold_transport_2026_10_24/analyze_transport.py`.
Simulation commands and inputs: TRANSPORT_CONTRACT.md, BOX_CHECK_A1.md, transport_runs/RUN_RECEIPT.json. The original script is archived as transport_preA1.py with its receipt-matching hash; transport.py adds only the L option for the padding check. Histories and scalar ledgers are in transport_runs/*.json.
