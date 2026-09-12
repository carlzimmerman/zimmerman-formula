# C003: independent vector-kick and fixed-NFW orbit audit

The specified fixed-potential realization fails the preregistered cluster retention gate: two independent 8192-particle ensembles give **0.80276 +/- 0.01280** and **0.77891 +/- 0.01249** at the cluster anchor. These are one-standard-error particle uncertainties; both 95% intervals lie above the allowed upper bound 0.70. Halving the timestep changes the common-seed cluster result by only 0.000038. This is a bounded failure of a prescribed fixed NFW potential and tracer distribution, not an exclusion of every self-gravitating or action-derived C003 completion.

No kick coefficient was adjusted: v_k=650 km/s, G0=0.382508632299176 per DE-weighted Gyr, and the integrated mean from z=6 to z=0 is 2.3077948724637416. The inputs reproduce L189_results.json. Fable and Hermes files were read but not changed. No commits were made.

## Cheapest discriminator: the escape threshold is not a probability

For a particle with speed v and isotropically oriented kick w,

    |v+w|^2 = v^2+w^2+2vw cos(theta),   cos(theta) uniform on [-1,1].
    P(bound | v,w) = clip((vesc^2-v^2-w^2)/(2vw)+1, 0, 2)/2.

L189 instead compares v^2+k*w^2 with vesc^2. Averaging an energy increment before applying a nonlinear escape threshold loses the angular probability and the cross terms between repeated kicks. Conditioning the initial Maxwellian on being bound gives:

| Host | Exact one-kick bound probability | L189 deterministic one-kick threshold |
| --- | ---: | ---: |
| Spiral | 0 | 0 |
| Milky Way | 0.040634 | 0 |
| Group | 0.679668 | 0.792921 |
| Cluster | 0.943499 | 0.982237 |

Independent 400,000-draw Cartesian Monte Carlo tests per host agree within the preregistered six-standard-error tolerance. The exact angular integral is numerical only in its final Maxwellian speed integration; its angular formula is elementary and exact. These probabilities are not enclosed-mass fractions and do not on their own determine a halo gate. L189 also multiplies by a self-similar expansion prescription; the orbit experiment replaces both its energy-threshold and expansion prescriptions.

## Equilibrium and host normalization

Use x=r/rs, m(x)=ln(1+x)-x/(1+x), and

    Phi(r) = -A ln(1+x)/x,   Phi(infinity)=0,
    A = vesc(anchor)^2 * x_anchor / [2 ln(1+x_anchor)].

If the specified sigma is interpreted as the local Maxwellian dispersion used by L189, the supplied sigma, vesc, and anchor cannot all describe an isotropic equilibrium NFW population. The isotropic Jeans integral fixes sigma once vesc and x are fixed:

| Host | Supplied sigma km/s | Predicted local NFW sigma km/s | rs kpc | Anchor kpc | Implied M200 Msun |
| --- | ---: | ---: | ---: | ---: | ---: |
| Spiral | 70 | 59.626 | 12.791 | 6.395 | 1.607e11 |
| Milky Way | 110 | 126.850 | 25.210 | 30.000 | 1.491e12 |
| Group | 300 | 250.911 | 173.684 | 382.104 | 2.201e13 |
| Cluster | 1000 | 736.050 | 423.876 | 1148.704 | 5.735e14 |

The orbit test fixes vesc and x_anchor. Sigma is then a prediction, not another fitted parameter. Spiral anchor=3Rd with Rd=2 kpc*(1.2e10/1e10)^0.35; MW anchor=30 kpc. Group and cluster anchors satisfy the R500 critical-density definition at H0=67.36 km/s/Mpc. Their masses consequently differ from the informal L189 host labels. Changing the physical normalization would define a different test and requires an explicit physical choice.

The initial velocity law is the Eddington-inverted isotropic NFW distribution function f(E), not a Maxwellian patched onto a Jeans second moment. The source potential remains the untruncated NFW potential. To make the tracer population finite while stationary, retain f(E) only for relative binding energy E>=psi(100 rs). This energy restriction is an integral of motion: it is not a reflecting radius or a position cut through a steady population. It changes the density at the tested anchors by at most 0.026% relative to the uncut DF. The inversion reconstructs the uncut NFW density to 0.014% and agrees with an independently integrated Jeans velocity second moment to 0.0059%.

The finite tracer population does not source the fixed force. The calculation therefore does not establish a self-consistent evolving halo, even though its initial isotropic phase-space distribution is stationary in the prescribed potential.

## Actual trajectories and finite results

Each ensemble has 8192 independently sampled, weighted tracers per host and exactly matched no-kick controls. Stratified radial sampling gives adequate inner statistics. Integrate Cartesian leapfrog trajectories from z=6 to z=0; apply genuinely isotropic vector kicks at independently sampled Poisson event times with DE-weighted intensity. All initially tagged particles remain kick-eligible, including after escape. No external-cell mean or clock-frame field is solved. Kicks are applied at the first timestep endpoint after the sampled event, with the same event list in the convergence pair.

Retention is the kicked/control ratio of weighted enclosed mass, averaged over the final 0.5 Gyr. Error bars use independent particle samples within each radial stratum, including covariance between matched kicked and control trajectories. Repeated time samples and the timestep pair are not counted as independent simulations.

| Host | Seed 307011, dt=1 Myr, retention +/- SE | Independent seed 307012, dt=2 Myr | Common-seed 1-vs-2 Myr difference |
| --- | ---: | ---: | ---: |
| Spiral | 0.110764 +/- 0.008576 | 0.123456 +/- 0.009111 | 0.000706 |
| Milky Way | 0.110633 +/- 0.006506 | 0.121407 +/- 0.006860 | 0.000071 |
| Group | 0.253793 +/- 0.008912 | 0.270386 +/- 0.009313 | 0.000339 |
| Cluster | 0.802764 +/- 0.012801 | 0.778908 +/- 0.012494 | 0.000038 |

The follow-up spiral gate f<=0.15 from the latest reviewer note in `hermes_push/STATE.md` is passed by the point estimates in all finite runs. This is not the original L189 ceiling f<=0.105, nor a confidence-bound certification of the spiral gate. The cluster gate 0.45<=f<=0.70 fails in all runs; the fine-run 95% interval is [0.77767,0.82785], and the independent-run interval is [0.75442,0.80340]. L189's value was 0.593567.

As an additional bounded diagnostic, the MW-like host retains 0.51162 +/- 0.01323 and 0.49409 +/- 0.01340 in the physical 100-300 kpc shell near z=0.4. These are well above 0.14, but this host has M200=1.491e12 Msun, not exactly 1e12 Msun. These numbers neither implement the exact registered KiDS host nor project a lensing observable.

All matched no-kick controls pass the declared drift and energy tests. Across runs, early-to-late enclosed control mass drifts by at most 1.85%; the worst 99th-percentile no-kick relative energy error is 0.0130%. Some close central passages have larger maximum errors (5.24% in a coarse run; maximum 0.832% in the refined run). The timestep comparison shows small observed retention changes for these sampled realizations; it is not a rigorous error bound or certification of every orbit. Work-subtracted energies also audit the integrator between vector kicks.

## Verification and provenance

Computation-audit and verification-before-completion skills were used. Twenty independent force/DF/control/convergence/sampling checks passed; the scientific cluster gate failed. A zero execution exit status records successful computation, not passage of that physical gate.

All four runs have schema-v2 bounded-run manifests. They record actual argv, run HEAD=5a87447af258ec132f6cedb5170dc8dd4c03f038, the existing dirty worktree, source hashes before and after execution, result/log hashes, package versions, UTC start times, exit statuses, and effective resource limits. The audited L189 source checkpoint is 1f0306787590840947e8e22cadfcabb9e162bb8d; the intervening commit did not alter those inputs. All four manifests passed validate_manifest.py with --root after the runs, including input freshness and output hashes.

| Run | Actual subset | Runtime seconds | Exit |
| --- | --- | ---: | ---: |
| analytic_001 | Four exact angle integrals and independent Monte Carlo checks | 3.44 | 0 |
| convergence_001 | 8192/host, seed307011, dt2 and1 Myr | 147.93 | 0 |
| replication_001 | 8192/host, seed307012, dt2 Myr | 66.02 | 0 |
| verification_001 | Twenty independent invariant and persisted-result checks | 0.57 | 0 |

The shared main contract describes the maximum planned family; each manifest's actual command and results specify the subset executed, as listed here. Computation uses Python3.9.6, NumPy1.26.2, SciPy1.11.4; the provenance runner uses Python3.11. No network dependency or coefficient search is involved. Cooperative numerical-library thread cap=1; orbit runs have 360-second wall and 330-second per-process CPU caps.

Executable sources: audit_orbits.py and verify_results.py. Inputs/contracts: contract.json and verification_contract.json. Evidence: analytic_001/, convergence_001/, replication_001/, verification_001/, each containing manifest.json, results.json, stdout.txt, stderr.txt. The exact regeneration commands are stored as argv arrays in each manifest. Use fresh output directories when rerunning the bounded runner.

## What remains physically missing

This test cannot supply the C003 action, energy-momentum bookkeeping, clock-frame field, spatial/velocity gate, or collision integral. It does not evolve the host's self-gravity as particles leave or establish how that gravity combines with the MOND sector. It omits baryonic response, halo assembly and infall, cosmological expansion of the outer population, and lensing projection. A live self-gravitating response can differ materially from a fixed potential, so the result must not be promoted to a universal C003 no-go.

The next discriminating calculation is to replace the prescribed force by the source and field equations actually derived from the proposed action, while keeping the same kick constants, matched stationary controls, Poisson event lists, and observational definitions. Arbitrarily reducing the force after this failed gate would be a new unproved prescription rather than an action closure.
