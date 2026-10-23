# Longer response: small fluctuations about a shifted bulk state

## Result and scope

The refined warm spherical medium completes t=120, three times the previous duration. Its initial bulk disturbance does not return to its original magnitude within that window. After t=30, the control-subtracted RMS-radius difference is predominantly a positive offset, rather than an oscillation of comparable size about zero. This supports finite-time redistribution into a shifted bulk state; it does not establish an asymptotic attractor, a damping rate, a physical formation mechanism, or novelty.

The coarse unperturbed control fails the outer-domain gate at t=113.705. The coarse perturbed trajectory and both refined trajectories complete. This is not a fully passing two-resolution long-time experiment. A boundary excursion by a representative particle is not proof of physical escape, instability, or evaporation. The current radius-10 domain and sampling need improvement before making such claims.

## Computation

Use unchanged live_discrete.py, with the same mesh equilibria and fixed A=10, gamma=.01, mass=1, anisotropy radius=1. The warm member is not the near-law cold member. Coarse: 32768 particles, 256 radial nodes, dt=.005; refined: 131072 particles, 512 nodes, dt=.0025. Each perturbation injects .0008 energy, with no friction or sink. These are direct runs, not evolutions performed within the bounded audit runner.

The failed coarse run was preserved as long_control_256.json. A diagnostic copy, live_long_diagnostic.py, retains the pre-failure trajectory and failure time without changing the force or integrator. Its prefix exactly reproduces the original short control. No trajectory is extrapolated past the failure.

## Separating offset from fluctuation

All entries below are the radius of the perturbed distribution minus the control radius, in dimensionless units. The standard deviation is within the indicated finite window, not a fitted damping envelope.

| window | coarse mean | coarse std | refined mean | refined std |
|---|---:|---:|---:|---:|
| 0–10 | .0131610 | .0305331 | .0128123 | .0304640 |
| 30–40 | .0133691 | .00233375 | .0109068 | .00172192 |
| 70–80 | .0142732 | .00298573 | .0127461 | .00132882 |
| 110–120 | incomplete | incomplete | .0114788 | .00164282 |

The refined final-window fluctuation is about 5.4% of the early-window fluctuation. This descriptive ratio must not be interpreted as a universal suppression factor: the early window contains the initial transient, and the late window is short. The late mean offset is about .67% of the unperturbed initial RMS radius. Late fluctuations do not decrease monotonically. The injected energy has not disappeared, so relaxation of a bulk observable need not mean return to the original distribution.

Over the common interval through t=113.7, the two response curves differ by .00281284 RMS and .0103641 at maximum. Control-radius drift grows to .00857215 coarse and .00461694 refined. This makes unresolved long-time numerical diffusion a relevant concern, despite good total-energy conservation.

## Numerical evidence, including failed checks

Maximum energy drift relative to the injected .0008 is .620% for the partial coarse control, .379% for the coarse perturbed run, .137% for the refined control, and .282% for the refined perturbed run. Maximum angular-momentum error is below 5.4e-14. Sampled q maxima remain below .50 coarse and .36 refined.

The bounded analysis in long_analysis_run has status FAILED: 8 of 10 audit checks pass. The two failed checks demand reproduction of every short-run summary value within 1e-10. Controls reproduce exactly; perturbed prefixes do not. Per-observable diagnostics are in long_prefix_diagnostics.json. The largest differences are 2.67e-9 in coarse maximum q and 1.76e-7 in refined median radius; RMS-radius differences are 2.14e-13 and 2.47e-10 respectively. Tiny initialization/root-solver differences are a plausible cause, but that cause was not independently isolated. The strict reproduction failure is retained rather than silently weakening the test. The manifest validates as an intact FAILED evidence record. It does not certify scientific success.

The plot long_response.png was visually inspected. No statistical error bars, asymptotic fit or novelty claim are justified by these runs. Analysis and interpretation are self-reviewed.

## What this changes

The earlier late/early RMS ratio conflated residual expansion with coherent fluctuation. The present test identifies that distinction and extends the observed small-fluctuation window. The next scientific question is whether the shifted coarse-grained state is selected by conserved energy and angular-momentum distributions, rather than arbitrary imposed cooling. Testing that requires independent particle/domain/time-step convergence and a near-law cold equilibrium. The phase-space packing constraint still forbids inferring cold halo formation from a warmer initial population without an additional justified mechanism.
