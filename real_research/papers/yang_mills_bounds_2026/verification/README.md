# Exact arithmetic checks

Run with Python 3.9 or later, using only its standard library:

```sh
python3 verification/verify_release.py
```

Run that command from the paper directory, or pass the script's absolute path
from any directory. The script replaces only `verification/RESULTS.json`. A
nonzero exit status indicates a failed check or execution error. No network,
third-party packages, original repository files, or Lean installation is
required. Original sources are hashed as optional documentary provenance when
the script runs inside the original repository; they are never imported or
executed. Copying this verification directory elsewhere still permits all
mathematical checks to run.

The script checks:

- Both exact rational witnesses printed in the manuscript, their strict
  supersolution and derivative slacks, the link thresholds 42.4, 59.9 and
  73.4, and the two-dimensional vertex threshold 42.3.
- The exact four-link sector sums, upward rational square-root bounds, and
  degree-eight majorant at the fixed rational witness
  `mu = 7714031583367/257393552939521`. It verifies
  `mu - lambda*q(mu) >= 0` and `2*lambda*q'(mu) < 1` for
  `lambda = 1190829/100000000 = 0.01190829`. Polynomial values are also
  evaluated independently by Horner's rule.
- The safe three-dimensional threshold `x = 599/10 = 59.9`, incidence `D=4`,
  and `(32/3)*D/x^2 <= lambda`. It checks the rational identity behind the
  uniform-in-`N` coefficient, rather than inferring that bound from a scan.
- The corrected BDL bookkeeping constant, exhausting exactly `k=1,2,3,4`:
  the maximum is `7168 <= 8192`.
- The three-qubit support counterexample using explicit integer 8-by-8
  matrices, basis index `4*u+2*v+w`, and vacuum matrix element `-1`.
- The `M=1` Schur-metric counterexample: an exact Gram factor and a vacuum
  orthogonal trial vector give Rayleigh quotient `2/5 < 1/2`; the corrected
  metric comparison gives `1/3`.
- The first two retained oscillator sectors, with exact effective levels
  `6/5` and `84/29`, which do not have the harmonic ratio two. The elimination
  in the second sector uses rational coefficients of `sqrt(2)`, without
  approximating that radical.
- Formal Laurent-polynomial identities for the finite-block exponent
  `A/s+B*s`, its stated optimizer, and the squared optimized value. These
  are algebra checks, not a heat-kernel calculation.

All mathematical predicates use exact integers, fractions, or polynomial
coefficient comparisons. There are no random samples, tolerances, spectral
truncation scans, or floating-point optimizations. The sole floating-point
quantity in the report is elapsed wall-clock time.

These checks validate finite arithmetic, not the analytic lemmas that connect
that arithmetic to a lattice spectral gap. They do not verify the BDL operator
estimates, their infinite-dimensional extension, heat-kernel bounds, Schur
operator domains, or the exclusion of higher oscillator sectors. Those steps
require the manuscript's arguments. They do not construct continuum
Yang--Mills theory, certify novelty, or recompile the separate Lean files.

`RESULTS.json` records all exact witnesses and slacks, Python/platform data,
repository revision and observed dirty state when available, source and script
hashes before/after execution, run status, and a SHA-256 of its canonical
`results` payload. The script is the only computational input; the original
source paths are documentary dependencies. Repository metadata may include
unrelated work and varies between environments. Run metadata varies between
executions; the canonical mathematical payload should not.

The report explicitly distinguishes its payload hash from a file hash: a file
cannot contain its own ordinary SHA-256 without self-reference. It is not a
separate validated mathbox v2 run manifest. The enclosing release manifest
should hash `verify_release.py`, this README, and `RESULTS.json` as ordinary
release files.
