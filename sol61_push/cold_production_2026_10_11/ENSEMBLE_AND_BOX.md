# Ensemble variation and the finite-box limitation

2026-10-11. Follow-up to [QUANTUM_HANDOFF.md](QUANTUM_HANDOFF.md).
This checks random-realization dependence in the spatial calculation and
box dependence in the earlier Gaussian stage. These are distinct tests.

## Five spatial realizations

Use the 1e-4 mean-daughter-charge handoff, dq=0.4, N=24, time step at most
0.005, and the same source adjustment and correlated sampling prescription.
The original seed 471901 is supplemented by 471902 through 471905 in
[matched_ensemble.py](matched_ensemble.py). All runs end at absolute x=100.

| Random seed | Daughter charge fraction | Moving source charge fraction |
|---|---:|---:|
| 471901 | 0.627668 | 0.294391 |
| 471902 | 0.682720 | 0.240921 |
| 471903 | 0.610767 | 0.220663 |
| 471904 | 0.596599 | 0.215454 |
| 471905 | 0.619708 | 0.190566 |

Across these five draws, the daughter mean is 0.62749 and sample standard
deviation 0.03296. Moving-source mean is 0.23240 and sample standard deviation
0.03902. These summarize a tiny ensemble in one box; they are not confidence
bounds, a converged ensemble prediction or a cosmic yield. Charge fractions
of the remaining uniform source complete each row's total to one.

The four additional runs pass all eight charge/energy diagnostics. Charge
drift stays below 7.82e-11 and reduced-energy drift below 1.64e-5. Endpoint
outer-mode charge is below 1.64e-8. See [additional results](matched_ensemble_run/results.json),
[manifest](matched_ensemble_run/manifest.json), and the original seed in
[matched spatial results](matched_spatial_run/results.json). Numerical
conservation is not a substitute for ensemble or box convergence.

The evidence supports substantial conversion and substantial moving-source
population across these samples. It does not single out a precise fraction.

## Why this box fluctuates so much

Let F_j be the mean charge carried by pair j. In the high-occupation pure
Gaussian limit, the Wigner-sampled charge of a pair has variance approximately
F_j^2. Thus the initial total daughter charge's relative standard deviation
is approximately 1/sqrt(N_eff), where

\[
 N_{\rm eff}={(\sum F_j)^2\over\sum F_j^2}.
\]

For the original dq=0.4 box, N_eff=12, giving about 28.9% relative variation
at the early handoff. This is a property of the narrow amplified spectrum
and discrete box, not a failure of random sampling. Later nonlinear dynamics
need not preserve that relative spread.

## Larger boxes: early quantum growth

[box_handoff.py](box_handoff.py) decreases dq at fixed physical momentum
cutoff q<=2. The box side scales as 1/dq and the physical initial source
quantum count as 1/dq^3, so vacuum weights are recomputed for every box.
This differs from increasing N at fixed dq, which changes the ultraviolet
cutoff without changing the box.

The Gaussian system can be reduced exactly to shells of integer squared
momentum because modes within a shell have identical detuning and initial
data. A shell of degeneracy d carries F_shell=d F_pair,
C_shell=d C_pair and w_shell=d/N_source. Substituting these into the equations
reproduces their sum exactly. Nonlinear *spatial* dynamics do not retain this
reduction; it is used only for the homogeneous Gaussian stage.

| dq | Retained pairs | Handoff x at mean fraction 1e-4 | Effective occupied pairs | Initial charge relative standard deviation |
|---|---:|---:|---:|---:|
| 0.4 | 257 | 73.768510 | 12.0 | 28.87% |
| 0.2 | 2,084 | 73.146662 | 20.46 | 22.11% |
| 0.1 | 16,700 | 73.079728 | 219.41 | 6.75% |
| 0.05 | 133,880 | 73.178123 | 1,499.40 | 2.58% |

All four integration/charge checks pass. [Results](box_handoff_run/results.json)
and [manifest](box_handoff_run/manifest.json) preserve shell degeneracies,
occupations and anomalous moments for future spatial initialization.
The reported standard deviations use the exact Gaussian formula including
the half-quantum contribution; the high-occupation N_eff expression agrees
at the displayed precision.

The dq=0.4 shell calculation includes all integer points at q=2. The earlier
floating-radius enumeration retained 245 pairs, excluding twelve boundary
pairs by roundoff. These off-resonant boundary modes are effectively empty;
the handoff time agrees to the reported precision. This boundary-convention
difference is disclosed, not silently treated as identical enumeration.

The onset time changes by less than one dimensionless unit across the tested
boxes, but does not converge monotonically. The last two differ by about
0.0984. No continuum limit is declared from these data. Most importantly,
these larger boxes have **not yet been evolved through the nonlinear spatial
stage**. Their better early mode sampling does not validate the coarse box's
final conversion fraction.

## Research decision

The route survives the first ensemble test: all five coarse-box realizations
convert substantial charge while populating moving sources. The next
load-bearing test is nonlinear evolution in a larger physical box, using
its saved vacuum-grown shell covariance, with sufficient grid cutoff and
time-step checks. Expansion and quantum-correction control remain separate
obligations. The repository's source-origin, abundance, halo profile and
vacuum-dependent acceleration scale are still not derived.
