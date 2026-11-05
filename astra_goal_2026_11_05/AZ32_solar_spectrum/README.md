# UNDECIDED full W4c; radial ladder and restricted TT diagnostic PASS

Tier 1 lane 2. New computations on both footings reproduce and refine the
radial bracket spectrum. They do not establish the full coupled relativistic
mode spectrum. Kappa = 1/2 FITTED; not theory closed. L_star=24 pc FITTED.
Criteria committed first: `453735a1b9`. Prior V3X/CT14 results were known.

| New check | canonical | alt | frozen line |
|---|---:|---:|---:|
| lowest-three-root change, 24 to 32 cells/decade | 0.0203013 | 0.0205155 | diagnostic |
| change, 32 to 48 | 0.0136169 | 0.0135057 | <0.05 |
| old 40-digit answers, max relative difference | 7.54e-10 | 4.56e-10 | <=1e-8 |
| fresh 30-digit check, relative difference | 3.22e-15 | 3.11e-15 | <=1e-8 |
| minimum omega squared, units a0/r_M | 2.82991e-5 | 2.26281e-5 | >0 |
| restricted TT speed envelope at 100 Hz | 5.12658e-32 | 6.19501e-32 | <=7e-16 |

All radial background residual, positivity and numerical checks passed.
The ladder includes l=0,1,2,3,4 and both coefficient brackets; JSON stores
each case separately. Both backgrounds are newly solved at the inherited
30/48 resolution. The 24/32/48 ladder refines the spectral discretisation,
not the background grid or an unrestricted three-dimensional perturbation.
Main spectral run: 56.2 seconds, parent peak RSS 174 MB; child memory is
recorded under `background_resources`. One thread throughout.

## What the tensor source does and does not establish

The [GW170817 primary report](https://arxiv.org/abs/1710.05834v2), abstract,
gives a fractional propagation-speed interval of -3e-15 to +7e-16. This is
not a bound on a finite-wavelength squared root at an arbitrary wavelength.
No source for V3X's 1e-10 finite-root threshold was established. Its original
failure is retained; this lane does not retroactively widen that criterion.

The newly recomputed TT-only quadratic action has no added quadratic
derivative term. Its frozen-background mass scan gives the small numbers in
the table; the exact group velocity at 80-digit precision confirms the
small-mass estimate. The GR/massless controls pass. The observational source
provides the comparison interval, not a justification for neglecting mixing
with polarization, lapse or other constrained variables. Controlling that
mixing and the propagation background is the missing implication. Thus this
diagnostic does not close full W4c or claim a cosmological waveform prediction.

## Negative controls and their limits

Reversing the stiffness in the scalar gradient operator fails positivity on
both footings. It also fails the stored known-answer and convergence checks.
The most negative eigenvalue grows with resolution; it is not a converged
finite growth rate. `audit_control.py` independently constructs 60-digit
negative Rayleigh witnesses at l=4, both brackets, both footings, and every
24/32/48 rung. Since A is positive definite, congruence preserves inertia:
these witnesses certify negative modes of the discrete control without
relying on float64's extreme eigenvalue. All twelve witnesses are negative.

Adding 1e-8 to the tensor gradient coefficient yields a speed excess about
5e-9 on both footings, outside the same observational interval. The control
fails the actual speed check; no mutation flag supplies the failure label.
Both mutation commands exit1; both main commands exit0. Resume checks return
the same checkpoint payloads with unchanged source fingerprints.

## Reproduce

From the repository root, with one thread:

```sh
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ32_solar_spectrum/run.py --resume
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ32_solar_spectrum/run.py --mutate --resume
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ32_solar_spectrum/audit_control.py
```

For a fresh recomputation use a clean checkout without the generated
`main/` and `mutate/` directories, then omit `--resume`. Do not delete live
checkpoints. `--part spectrum` and `--part tensor` run the parts separately.
The spectrum imports audited definitions read-only, without executing the
historical scripts' output-writing sections. Input hashes and software
versions are in each provenance JSON. SIGTERM yields at a completed case;
the background child uses the inherited RSS watchdog. The small independent
Rayleigh audit is restartable, not a queued heavy calculation.

Exact next calculation: derive and solve the constrained mixed-mode tensor
problem on an on-shell screened background, showing which characteristic or
group speed can be compared to the observational propagation interval.
