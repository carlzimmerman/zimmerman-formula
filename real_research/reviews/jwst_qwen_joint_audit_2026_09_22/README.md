# A surviving matched-pair calculation, not a new law

The independent analysis reproduces a nontrivial candidate in Qwen attempt
3fe609a7abbb4a7db88e515b8fa40c2e. Its original checks were insufficient, but
the subsequent referee overstated its rejection: the saved output includes
nonuniform candidates at q=3,10,30, not only the identical reference.

Within the conservative Thomson model, two explicitly different clouds have
line second moments and mean delays equivalent to within 1% at the reported
approximate 95% Monte Carlo precision, while their joint moment E[v^2 D]
differs by 16.4% (35.7 combined Monte Carlo standard errors). This is a finite
calculation, not an exact matched-moment theorem or observational detection.

Parameters, with R=c=k_B*T0/m_e=1:

| Cloud | kappa(r) | T(r)/T0 | Exact mean D |
|---|---|---|---|
| A | 2 | 1 | 1 |
| B | (1+10 r^2)/3 | 1+0.4689264972650708 r^2 | 1 |

The fitted h is frozen before validation. Radius and central temperature are
fixed across clouds; the radial temperature profile is explicitly different.
These are theoretical fixtures, not two inferred JWST objects. Their complete
line shapes are NOT claimed equal: only their second moments are matched.

## Evidence and limits

Training uses 1,000,000 photons per call. Three independent validation batches
use 200,000 photons per cloud each. There are 4,800,000 total simulated photons
across all calls, including the cold comparison and the paired h=0/h=1 training
calls. The latter deliberately share spatial paths to estimate a temperature
response. Validation seeds are disjoint from training seeds.

For each spatial path A=sum_i T_i(1-mu_i), independence and zero mean of the
Maxwell electron velocities give E[v^2 | path]=2A. D depends only on that
path. Therefore E[v^2 D]=2E[AD]. This conditional average reduces Doppler
sampling noise without assuming the joint moment being tested. The explicit
Doppler draws provide an additional calibration. Temperature does not alter
spatial flights in this prescribed nonrelativistic Thomson model.

The retained width mismatch is -0.211%; its absolute mismatch plus 1.96 SE is
0.618%. The corresponding delay interval criterion is 0.776%; the mean delay
equality also follows exactly from the specified radial opacity. The joint
moment difference is 2.38345 +/- 0.06674 Monte Carlo SE in these units. Turning
off B's gradient breaks the spectral match, providing a physical negative
comparison. All declared checks pass; the manifest validates code/input/output
hashes and execution provenance, not mathematical truth.

`verify.py` is independently written analysis, but reuses the previous transport
implementation. It is not a second independent transport solver. Approximate
normal sampling intervals do not cover model error, observational uncertainty,
or hidden bugs in that shared solver. Training is explicitly synthetic model
matching, not independent measurement of an astronomical temperature profile.

## Bounded literature check, September 22 UTC

Primary abstracts inspected:

- Grier et al., [arXiv:1210.2397v2](https://arxiv.org/abs/1210.2397v2), report
  reconstructed velocity-delay maps in AGN. Joint spectral/timing information
  is already an established research approach.
- Mizumoto et al., [arXiv:1805.00046](https://arxiv.org/abs/1805.00046), simulate
  scattering-cloud line profiles and lag-energy behavior. Their outflowing
  X-ray model is different from these static thermal Thomson fixtures.

Searches covered electron scattering, velocity-delay maps, thermal broadening,
time delay, covariance and reverberation. This limited search does not establish
novelty of the exact pair or mixed moment. The general strategy is prior art;
no breakthrough or new-law claim is justified.

## Concrete next Qwen task

Reproduce this frozen pair using fresh seeds, then ask whether the *static full
line shape* already distinguishes it. Compute the fourth moment from explicit
Doppler draws, cross-checking E[v^4 | path]=3(2A)^2 for the same Gaussian
conditional model. Quantify kurtosis differences on held-out paths before
claiming that a timing measurement is necessary. Do not fit the joint moment.
If the static spectrum already separates the pair, report that limitation and
seek a genuinely stronger degeneracy rather than relabeling this one.
