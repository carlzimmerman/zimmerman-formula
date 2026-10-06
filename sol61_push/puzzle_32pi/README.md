# 32pi puzzle: what Claude advanced and what remains missing

Checkpoint SOL61-RESUME-2026-10-05-A; base
`0893bc5cdef187ffb10ccb5b539cb469443d57f0`.
**Verdict: incomplete; the coefficient remains fitted.** This is self-review.
The target is C=Lambda c⁴/a0²=32pi on the vacuum-density footing, equivalently
a0=(c/2)sqrt(G rho_Lambda). The total-density footing is a different hypothesis.
See the [joint closure order](../CLOSURE_ROADMAP_2026-10-05.md).

## Advances since the Sol61 stop

Claude's `sonnet55_push/puzzle_32pi/` now contains p13–p45 and external-note
checks; the new formal files are under `fable_independent_2026/lean_2026/`.
This review prioritizes p21–p45's coefficient mechanism, p41–p44's empirical
normalization and the postulate-independence file. It does not rerun every lane.

| Result | What it establishes | Missing implication |
|---|---|---|
| Geometry, horizons, flux and external trace/anomaly notes | Many exact equivalences and scoped obstructions | No dynamical identification of a galaxy a0 with the required radius/curvature; several original broad no-gos were withdrawn in README section 12 |
| Formal postulate independence | Every positive kappa is admitted by the encoded algebraic premises with a freely chosen integral | Not an independence theorem for every physical action: I is a free positive number and the galaxy law is not implemented as a field equation |
| Symmetric BIMOND dictionary | A conditional vacuum ratio C=I_nu/2; symmetry can remove a prefactor | Complete kernel, vacuum boundary value and full-action health remain inputs |
| High-acceleration tail cutoff, p35/p39/p45 | A finite, positive integral and accurate asymptotic formula | y_t and cutoff shape are unselected; fitting either is not a derivation |
| Gas-point calibration, p41b/p42 | Less stellar-M/L sensitivity; gas-point kernel differences smaller than mixed-sample differences | Distance, sample selection and inter-galaxy scatter still limit a0 |
| WALLABY, p43 | A second sample consistent with SPARC within quoted statistical errors | Distance prescription moves the central value by about 33%; agreement is not coefficient discrimination |
| Forecasts and point-hypothesis likelihoods, p44 | Nearest vacuum-footing rivals are unresolved | Forecast needs its finite systematic-floor correction; evidence ratios condition on fixed cosmology and the declared error model |

The Lean Ingredients structure checks Einstein's normalization, a Schwarzschild
radius identity and a BIMOND vacuum identity with free I and fp. Models with and
without the target refute implication from those **specified** ingredients.
This correctly locates a missing premise, without excluding a microscopic
theory that restricts I or invalidating a phenomenological fit.

## Independently reproduced integral and its selection problem

For the k=2 cutoff, let T=y_t>0 and y=g_N/a0. The implemented conditional ratio is

    C(T)=integral_0^infinity y [sqrt(1+1/y)-1]/[1+(y/T)²] dy
        =integral_0^infinity 1/{[sqrt(1+1/y)+1][1+(y/T)²]} dy.

The second form avoids catastrophic cancellation at large y. Independent
40-digit quadrature gives

| T | C(T) |
|---|---|
| 100 | 77.8524211286 |
| 128 | 99.8129198953 |
| 129 | 100.5973510611 |
| 1000 | 784.4238093033 |

The target root is **T=128.9153707043**. This reproduces p45's numeric root;
its asymptotic fixed-point value is 128.9144. There is no contradiction between
those values. Our first run incorrectly compared to the rounded prose value
128.9 at tolerance 0.01; its failure is preserved in checkpoint_a. The corrected
comparison uses p45's recorded four-decimal root with half-unit rounding error.

For each y>0 the positive integrand strictly increases with T. C is continuous
for T>0 by domination on every compact T interval. For T<=1, the T=1
integrand is an integrable dominator, so C(T)->0 as T->0. Its integral over
[T,2T] grows at least proportionally to T for T>=1, so C(T)->infinity.
Consequently **every positive C is selected by a unique T** in this cutoff
family. Solving C(T)=32pi determines a fitted T; it does not predict C.
The closed form makes this parameter freedom calculable, not absent.

## Stronger identifiability check: keep the observed law exactly

Take the cutoff kernel at T=129 and add a compact C² tail deformation,

    delta_nu(y)=epsilon t³(1-t)³, t=(y-Y)/Y, Y<y<2Y,
    delta_nu(y)=0 otherwise.

All derivatives through order two match at the endpoints. The kernel and all
its predictions for y<=Y are **identical**. In the conditional vacuum dictionary,

    delta_C=integral y delta_nu(y) dy
           =epsilon Y² integral_0^1 (1+t)t³(1-t)³ dt
           =3 epsilon Y²/280.

Choose Y=1000 and epsilon=9.3333333333e-7. Then delta_C=0.01 exactly, including
zero change throughout y<=100. This is not observational evidence for that
deformation; it is a constructive demonstration of coefficient freedom.
It also preserves positive excess response and monotonicity. To certify the
latter uniformly on [Y,2Y], write a(y)=sqrt(1+1/y)-1 and note

    -nu_base'(y) >= a(2Y) [2Y/T²]/[1+(2Y/T)²]²,
    |delta_nu'(y)| <= (epsilon/Y) (3/16).

The respective bounds are 5.1567e-10 and 1.75e-10. Outside the support the
kernel is unchanged. Thus even positivity, monotonicity, the same low-y law
and the same asymptotic tail beyond 2Y do not fix the integral.

**Scope:** this disproves identifiability from those functional restrictions
and finite-range galaxy predictions. It does not prove that both kernels
arise from healthy relativistic actions, nor claim invisibility to every
high-acceleration or nonlocal measurement. A microscopic admissibility theorem
could distinguish them; that is exactly an additional premise we need.

## Corrected sample-size forecast

p44 explicitly posits per-galaxy log scatter s=0.604 and a shared Gaussian
systematic uncertainty f=sqrt(0.03²+0.085²)=0.0901388. Under that toy model,
the variance of the mean is s²/N+f². For a log separation Delta and a z-sigma
precision target, the consistent forecast is

    N >= z² s²/(Delta²-z² f²),   if Delta>z f.

If Delta<=z f there is no finite N meeting that precision target. The existing
N=(z s/Delta)² figures are **zero-floor forecasts**, even for comparisons
marked possible at the current floor. They cannot be used as sufficient N.

| Rival against kappa=1/2, vacuum footing | Delta ln a0 | Zero-floor N at 2 sigma | N with current floor |
|---|---|---|---|
| Same kappa on total density | 0.18917 | 40.8 | 444.3, hence at least 445 |
| Milgrom, vacuum footing | 0.08195 | 217.3 | No finite N |
| Verlinde, vacuum footing | 0.03583 | 1136.5 | No finite N |
| p40 cutoff prediction | 0.12511 | 93.2 | No finite N |

At 3 sigma even the total/vacuum comparison cannot pass with the stated floor.
The shared floor must fall below 4.10% to distinguish Milgrom at 2 sigma,
and below 1.79% to distinguish Verlinde. More galaxies only reduce the
independent component. These are Gaussian precision estimates, not a theorem
about test power, all distance calibrations or the true sampling distribution.
The rounded recorded scatter is used; a full raw-data reanalysis is deferred.

p44's reported Bayes factors are point-hypothesis likelihood ratios under
its fixed nuisance/cosmology prescription. Its weak preference for one density
footing should not be reported as a decisive model evidence calculation with
nuisance parameters integrated out. The formula correction does not change
the recorded point-hypothesis likelihood ratios themselves.

## What can close the puzzle

Three routes remain meaningfully distinct:

1. **A microscopic constitutive/UV selector.** Derive the whole kernel and its
   vacuum boundary condition in a fixed physical normalization. First test
   whether the mechanism removes T and the compact-tail freedom. Then compute
   its stress, source dictionary and radiative sensitivity. Any free y_t,
   f'(1), vacuum offset or coupling that changes C leaves the target open.
2. **A dynamical vacuum/response linkage.** A covariant symmetry, constraint
   or self-tuning mechanism must relate independently measured galaxy
   susceptibility to the gravitating vacuum. First vary a constant matter
   vacuum shift and a physically normalized response coupling separately.
   The older Sol61 offset/coupling counterfamilies must cease to be admissible,
   without eliminating the source or MOND window. No such mechanism is established.
3. **Empirical falsification/calibration.** Fit the canonical and alternative
   footings with shared distances, kernel, selection and stellar/gas nuisance
   parameters. The cheapest discriminating improvement is independent distance
   calibration, not another post-hoc list of attractive constants. This can
   reject an exact coefficient; an empirical match alone does not derive it.

Do not reopen the completed geometric/thermal scans unchanged. A horizon
route needs an actual observable galaxy-response bridge and a radius defined
independently of a0. A dimensional or topological restatement is insufficient.

The finite checks are in [closure_checks.py](closure_checks.py); the current
run is [checkpoint_b](runs/checkpoint_b/manifest.json), with raw stdout and
provenance. No coefficient-selection proof or full galaxy-likelihood rerun
is claimed. The puzzle remains OPEN.

## Concurrent-result addendum: p46, verified at 35b89edfd

While this checkpoint was being saved, p46 split the gas-point sample by
distance method. Its recorded output reports TRGB/Cepheid distances: 8 galaxies,
70 points, a0=1.158e-10 with 20.2% statistical uncertainty; Hubble-flow distances:
11 galaxies, 54 points, a0=6.970e-11 with 18.3%. The mixed fit remains 8.999e-11.
These are **reported results with code inspected**, not a fresh bootstrap rerun.
The higher value is closer to the total-density footing; accordingly the
mixed-sample p44 preference for the vacuum footing is not robust and should
not be carried as current positive evidence for that footing.

The groups contain different galaxies, so this comparison alone does not
identify distance bias as the cause. Under a rough independent-log-error
comparison their separation is about 1.9 sigma, not a decisive contradiction.
The script's printed median e_D/D uses the broader eligible TRGB/Cepheid
sample before the gas-point selection; it is not necessarily the error median
of the eight fitted galaxies. Precision, selection and calibration remain
open. The 445-galaxy correction above still follows from p44's stated toy
scatter and floor; it is not a new forecast for the eight-object subset.

This update strengthens the priority of a distance-method-aware hierarchical
fit with shared calibration uncertainties and galaxy-level scatter. It neither
selects the alternative footing nor derives 32pi. Source files and hashes are
recorded in [the addendum scope](../RESUME_ADDENDUM_2026-10-05.json).
