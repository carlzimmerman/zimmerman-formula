# Independent audit of the radial production control

Primary verdict: **conditional on a named input**: the isolated hidden sector,
collisionless neutral photino, dilute constant vacuum mother widths, and the
declared finite near-fold scaling family. The corrected energy/travel implication
is sound under these inputs. The computation supports a finite scan and one
evaluated boundary control, not a continuous-parameter or all-producer exclusion.

Audited on 3 November 2026 (local date), starting from the root CONTRACT and
production CONTROL_DERIVATION_v2.md, controls_v2.py, boltzmann_v3.py, kernels.py,
canonical/run_nearfold/result.json, and saved transport/control outputs. Subsequent
controls_v3.py and CONTROL_DERIVATION_v3.md were inspected after the producer
implemented the time/birth corrections reported below. This is an independent
derivation and implementation of the boundary check; it is not an independent
construction of the finite SUGRA pole masses or currents.

## Claim card and dependencies

For a cold radial mother prepared at SM temperature 20 MeV with fitted number
N_sigma, let its phase channel be closed and its vacuum widths into SU3, SU2,
U1 photinos and Goldstinos be constant. Assume Einstein expansion and isolated
positive-energy hidden stress with 0 <= P/rho <= 1/3, including surviving mothers,
all companions, hidden photons and gravitinos. With target photino rest density
0.265 rho_c and the stated recombination matter/pressure budgets, bound the
neutral population's average comoving travel after recombination.

Dependency graph:

1. Finite near-fold masses/slopes and leading Ward current -> vacuum partial
   widths, Bchi, lifetime. These are model/finite-order inputs, not rederived here.
2. Stress conservation -> monotone K=rho_hidden a^4 and post-rec H upper bound.
3. Dilute exponential mother law + SM entropy history -> lower birth quantiles.
4. Number normalization + finite-rec energy accounting -> necessary energy gate.
5. Collisionless q conservation + 2--4 -> late-travel lower integral.
6. The explicit 33 x 180 iterator + one two-equation boundary solve -> finite
   numerical evidence, without a uniform reduction over the continuous domain.

## Findings

| Severity | Locator | Finding/status |
| --- | --- | --- |
| P1 scope | production/CONTROL_DERIVATION_v2.md:8,27; inherited at v3:8,27 | Arbitrary companion thermalization is insufficient to justify a fixed vacuum Bchi and exponential total width. Blocking SU3/SU2 can increase the eventual photino branching fraction. The blanket statement that Pauli suppression only lowers the yield is false without a dilute/vacuum-width restriction. Direct source occupations are small at the inspected boundary, but arbitrary redistribution has not been bounded. Producer was notified and is writing a restricted standalone derivation. |
| P2 corrected | production/controls_v2.py:20--25; CONTROL_DERIVATION_v2.md:16,25,92 | The low-temperature C is not a global lower radiation coefficient through electron annihilation, and the full infinite decay mean is not literally a finite-rec lower bound. V3:18--27 uses initial Cmin, full pre-rec H upper integration and an incomplete-Gamma birth integral. Those corrections check. |
| P2 scope | production/controls_v3.py:74--88; boltzmann_v3.py:39--44 | 5,940 samples plus one boundary root do not establish a continuous optimum. r is varied while other near-fold data stay fixed; e uses the supplied leading scaling. The finite physical stationary points are separate evidence. The v3 prose explicitly disclaims global monotonicity. The code comment “Continuous optimum” is stronger than the calculation. |
| P2 scope | production/boltzmann_v3.py:48--50,127--134 | The mother abundance at 20 MeV is fitted initial data. Small harmonic misalignment fails the reported energy budget, and no actual preparation mechanism for the fitted state has been obtained. The harmonic calculation is not a nonlinear basin or metastability proof. |
| P2 scope | production/boltzmann_v3.py:110--111,127--128; controls_v3.py:44--45 | Neutral collisionlessness is checked only for the named heavy-contact operator class; complete finite SUGRA currents are still inputs. Ward survival is a necessary partial-current gate, not a computation of every photino decay channel. Stable transport and exact recombination rest-density bookkeeping should be distinguished when allowing up to 1% subsequent decay. |
| P3 numerical | production/controls_v3.py:14,38--43 | 64-node Gauss-Laguerre quadrature alone is not a rigorously certified lower bound. The independent positive truncated integral below is slightly smaller and still exceeds 1 kpc at the inspected boundary. |

No H-inequality reversal or mother/companion double counting was found. In
boltzmann_v3.py:84--95, removing one mother deposits its energy once. The two
phase insertions each have number dns Baa, so together represent two phases;
the subsequent two daughters per phase give the correct 4 Baa Ba_chi cascade
multiplicity.

## Independent reconstruction

Conservation gives

    d(rho_h a^4)/d ln a = (rho_h-3P_h) a^4 >= 0.

For a mother that decays at a_d, its combined mother/daughter contribution at
recombination is at least m_sigma min(a_d,a_rec). This includes surviving mothers
and does not add their energy to their daughters. Therefore the exact finite-rec
floor is N_sigma m_sigma E[min(a_d,a_rec)]. Discarding all births beyond a
guaranteed time t_min,rec gives the weaker valid floor used in v3:

    N_sigma m_sigma sqrt(pi Cmin/(2 Gamma)) P(3/2,Gamma t_min,rec),

where P is the regularized incomplete gamma. With constant vacuum branching and
direct production only, N_sigma >= rho_chi,0/(2 Bchi mchi). The inequality remains
conservative if photinos later decay, since more mothers are required.

For the stipulated photon/electron/neutrino entropy convention,

    K_SM,early = (pi^2/30) 10.75 (4/11)^(4/3) T_gamma,0^4,
    K_SM,late  = (pi^2/30) [2+5.25(4/11)^(4/3)] T_gamma,0^4.

SM stress conservation implies monotone K_SM. Hence the analytic relativistic
endpoint Cmin=sqrt(K_SM,early/(3 Mp^2)) is a global conservative coefficient
after the source is prepared. Independently,

    Cmin/C_lowT = 0.9109097066663274,
    a_birth(u) >= sqrt(a_i^2+2 Cmin u/Gamma) >= sqrt(2 Cmin u/Gamma).

At recombination E-m <= p^2/E = 3P per mode implies the stated energy gate if
the rest-mass budget is imposed there. For later a, nonnegative pressure gives

    rho_h(a) <= rho_h(a_rec) (a_rec/a)^3 <= Kmax/(a_rec a^3).

This is the correct H upper direction. Before recombination, monotone K gives
rho_h <= Kmax/a^4. Including baryons and Lambda is necessary in the early H upper
bound; v3 includes both. In the independent check the simpler constant bound

    Cpre^2 = [K_SM,late+Kmax+rho_b,0 a_rec+rho_L,0 a_rec^4]/(3 Mp^2)

gives t_min,rec >= (a_rec^2-a_i^2)/(2 Cpre). The residual exponent at the corrected
boundary is smaller than -45,503,800. A relativistic post-rec path bounded using
only Omega_b=.05 is below 38,585 Mpc, so the producer's 100,000 Mpc tail-removal
factor is conservative. This closes the finite late-production tail for the
inspected source law; it does not exclude a mother prepared much later.

For a dark photino decay to the residual U1 photon and gravitino, all products
belong in hidden K; the residual U1 photon has not been identified with observed
electromagnetism. Thus this decay does not create an SM leakage exception.
For a fixed proper lifetime, later births have larger q and larger survival
probability. Their post-rec path is also increasing with q. Weighting by final
survival therefore increases the mean late path for the already-born population.
The recombination rest-density allowance must still include the slightly larger
pre-decay photino number if its budget is translated from today's density.

## Independent finite calculation and source normalization

Script: review/production_control_independent.py. Contract:
review/production_independent_contract.json. Valid completed v2 manifest:
review/run_production_independent_v2/manifest.json. The run took under one second,
one numerical thread, wall cap 60 s, CPU cap 55 s; measured peak RSS 56,786,944 B.
The earlier failed run is preserved: it found an inadequate fixed bracket in a
diagnostic occupation root, subsequently replaced by the exact Lambert-W formula.
It was not a physical counterexample.

The independent code imports no production modules. It reconstructs partial
widths from raw masses/slopes, reproduces old e=0.004349075159276599, r=
1.0012822849600351 boundary Gamma, Bchi and K ratio, and then conservatively changes
the birth coefficient and resolves the energy boundary:

    r = 1.0012429075534721,
    Gamma = 3.1936520960954595e-30 GeV,
    Bchi = 7.758873807804447e-5,
    post-rec travel lower control > 1.8142417055503244 kpc.

The travel calculation uses only sqrt(u)<=10, integrates its positive first
moment analytically, and lowers all velocities with the maximal momentum in
that interval. It therefore avoids relying on the producer's Laguerre evaluation
of sqrt(u). The producer's corrected v3 boundary gives 1.8146629844511208 kpc;
the difference is approximately 0.023%, well below the comparison-gate margin.
This does not certify all grid values or a global minimum.

At u=1, the independent unbackreacted RD source occupations per helicity are
9.06e-7 (chi), 1.56e-7 (SU3), and 3.27e-7 (SU2). These are diagnostic direct-stream
values, not an arbitrary-kinetic-solution bound.

Primary source checked: Yong Tang and Yue-Liang Wu, *On Thermal Gravitational
Contribution to Particle Production and Dark Matter*, arXiv:1708.05138v2,
26 October 2017, section III and Table I, accessed through
https://arxiv.org/html/1708.05138v2. Their interaction and unpolarized cross-section
conventions with kappa=2/Mp and one Majorana final species give
sigma_gamma_gamma=s/(640 pi Mp^4). Direct angular and MB radial integration
independently gives the number source 3 T^8/(20 pi^5 Mp^4), or
0.0004901645464580079 T^8/Mp^4. The identical incoming event factor cancels the
two produced particles. The four-real-Higgs, 45-Weyl and 12-gauge-generator
coefficients, and the stated zeta(4) quantum factors, agree after the same
degree-of-freedom translation. This authenticates the direct source only,
not production and cascade of the whole hidden heavy spectrum.

## Obligation matrix and safe conclusion

| Obligation | Result |
| --- | --- |
| K monotonicity and H upper direction | Passed under isolated positive hidden stress |
| Finite-rec energy floor and lower birth map | Passed for corrected v3; v2 literal formulas need restriction |
| Number and mother/phase multiplicities | Passed for direct vacuum-width and declared cascade laws |
| One corrected boundary travel control | Independently verified numerically, with a conservative alternate integral |
| Source/time/Planck/number normalization | Passed for the direct gravitational source and supplied cosmology |
| Arbitrary companion medium feedback | Not addressed; vacuum-width kinetics must be named |
| Continuous parameter minimum | Not addressed; finite iterator and one boundary control only |
| Full neutral kinetic/current completion | Conditional on named heavy-contact and leading-current inputs |
| Fitted mother's preparation and metastability basin | Not addressed by transport |

Strongest safe statement: in the declared dilute near-fold source controls,
the corrected finite energy/lifetime scan and inspected saturation boundary
remain warmer than the 1 kpc gate, even after conservative entropy and late-tail
corrections. Actual finite-action stationary examples transported separately
are also warm in the two reported companion endpoints. The work has not supplied
a controlled producer yielding all dark matter, nor ruled out every embedding,
late preparation, interacting neutral sector, or heavy-spectrum gravitational
cascade. The cheapest next check is to finish the announced dilute-source
restriction and quadrature convergence record; a stronger exclusion needs a
uniform parameter reduction and controlled medium effects.
