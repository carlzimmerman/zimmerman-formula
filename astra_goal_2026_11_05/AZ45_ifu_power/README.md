# IN PROGRESS — nonlinear population forecast pending; pilot mutation UNRESOLVED

Kappa=1/2 FITTED; not theory closed. Criteria616d7954c8 were committed
alone before cubes or fitted numbers. This lane uses FN3's nonlinear
cube engine with explicitly synthetic masses, gas and geometry. It
does not call the old Planck15 mass conversion or Native background.
The synthetic mass-residual rise is not literally an injected a0(z)
history; own response levers are required for that interpretation.

## Evidence so far

- Known answers56/56: independent Gaussian channel integration, PSF DC
  normalization, restricted one-parameter noise-free stellar-mass recovery
  on both footings and both rungs, exact regression and coverage fixture.
- All24 flat-truth, HI6 forward-cube pairs pass. Maximum relative change
  is0.0015047809 versus0.005. This does not yet cover every noisy/gas/rise
  population realization's truth cube; that audit remains required.
- One canonical template at S/N30, free HI, has four fit pairs. Reference,
  doubled-a0 noise-free, and main noisy pairs pass the0.01dex line. The
  mutation pair FAILS:0.02905983dex change. This control is UNRESOLVED.
  It is not silently upgraded because both optimizer starts converged.
- Noise-free doubling a0 shifts the fitted log stellar mass by
  -0.18787385/-0.18788614dex (coarse/fine), not the copied-0.30 value.
  Noisy shifts need population calibration against these own levers.
- The main noisy fit gives Delta=-0.28701286/-0.28745296dex. This is
  one noise realization, not a population bias estimate or power result.
- SIGTERM while the fine reference pilot is live exits75 with an atomic
  checkpoint. Resuming restarts that interrupted deterministic fit;
  its scientific file is byte-identical to uninterrupted output. A
  completed-case resume exits0. A separate one-case batch exits75 with
  one completed record, as intended while the grid remains unfinished.

The original system-Python3.9 NNLS solver failed before the first cube
with `too many iterations`. Both sanitized tracebacks are retained.
The unchanged model runs in the existing Python3.13.9/numpy1.26.4/
scipy1.14.1 environment. Nothing was installed. Pilot RSS remains below
0.4GB; the known-answer pass took5.3seconds and fits take seconds to
tens of seconds. Exact runtimes and source hashes accompany outputs.

## Remaining work and full grid

`batch.py --plan` verifies4032 unique cases:576 noise-free lever fits,
2304 noisy main fits and1152 independent mutation fits. Each case uses
two starting points. This is multi-hour work and must use heavyq after
the light-tier work; it has NOT been queued or completed. The batch
refuses an unqueued long run and monitors each worker's RSS. Full
footprint measurement for the queue declaration is still required.

Also pending: the complete population grader, all truth-cube convergence
pairs, the512/1024 resampling calculation for all sample sizes/systematic
floors, and final calibration/power labels. Neither the pilot nor a
Fisher substitute answers the lane's requested nonlinear forecast.
The failed pilot tolerance stays frozen. No adoption or real-cube
download follows from this work.

## Reproduce pilots

Use the recorded existing conda Python environment. From the repo root,
with LANE=astra_goal_2026_11_05/AZ45_ifu_power:

    python LANE/controls.py
    python LANE/batch.py --plan
    python LANE/worker.py --template 0 --rung 1 --foot canonical --mode reference --resume

For each mode reference,double,main,mutate, run worker with rung1 and2;
the default tag is pilot. Existing completed files require --resume
(identity checked); a new --tag gives a fresh calculation. Then:

    python LANE/check_pilot.py
    python LANE/check_resume.py --tag contract_fresh
    python LANE/batch.py --tag batch_fresh --max-cases 1 --resume

Expected exits: controls0, check_pilot1 for the unresolved mutation,
check_resume0, one-case batch75. The resume test requires a fresh tag
and the uninterrupted fine reference pilot. It stops its own test worker
only, never shared queue jobs. Completed but scientifically unresolved
fits return0; science and process status are deliberately separate.

## Population-statistics implementation checkpoint

population.py now implements the frozen equal-third OLS slope and its
within-third sampling variance, exactly balanced four-template resampling,
identical512/1024 prefixes, all three trend floors, Wilson95% intervals,
and Monte Carlo gate agreement. This module accepts all36 residuals and
rejects an incomplete array; it supplies no missing nonlinear fits.

check_population.py passes13/13 independent checks, including the analytic
slope/variance, Gaussian95% coverage0.94928 in16,384 seeded draws (three-sigma
tolerance0.00511), exact template balance, prefix identity, known power
fixtures and missing-replicate rejection. A fresh run is byte-identical.
Run with the recorded conda Python and warnings treated as errors:

    python -W error astra_goal_2026_11_05/AZ45_ifu_power/check_population.py

During implementation, NumPy's three-column matrix-vector operation emitted
floating-point warnings despite finite correct fixture results. Explicit
three-term elementwise sums remove that backend path; all analytic checks
then pass with warnings raised as errors. No criterion changed. Source
hashes and versions accompany population_checks.json. The full4032-case
fit grid and its calibration/provenance-aware population grader remain
pending; no observational power forecast follows from these fixtures.
