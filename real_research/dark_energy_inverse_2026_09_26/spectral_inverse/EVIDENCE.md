# CD26-3 spectral inverse evidence

Both accepted manifests passed the installed mathbox
`validate_manifest.py MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula`,
including current input and output hash checks. There were no failed bounded
runs for this inverse route.

| Run | Evidence | Runtime | Recorded HEAD |
|---|---|---:|---|
| `run_001` | 30 exact symbolic checks, including controls | 1.260839 s | `738216fbd6932e37a8447297729e7d18108cf4cb` |
| `run_lean_001` | Nine compiled real-algebra theorems | 28.285175 s | `ecffd2af3623ff3e32318234fd51e1fac50b9126` |

The shared workspace was dirty and advanced concurrently. Each manifest
records the actual command array, source hashes before and after execution,
declared results, stderr/stdout, limits, software and repository state.
The first computation respected a 60 s wall and 50 s CPU cap. No random
sampling, observational fitting, or broad numerical simulation was performed.

Symbolic software: Python 3.9.6, SymPy 1.14.0.

- `check.py` SHA256: `a2999581d21070bc4d415fb0860c75f1fbc91dbef729386d99762b7051f12c13`
- `run_001/results.json` and stdout SHA256:
  `e6b1b260277569518a462a4517bcff7e37fd502736695c5e47f91f5d5af423a7`

The checks cover the lapse/logarithm inverse, scale invariance, profile
sensitivity, reinsertion, physical expansion factors, exact parameter and
source-offset degeneracies, divergence identities, periodic examples,
spatial-constancy rejection, zero-lapse counterexample, curvature/traceless
terms, and observation-design ranks. A count of algebraic checks is not a
count of physical theory requirements closed.

Lean used version 4.34.0-rc2 and the pinned local mathlib environment. The
accepted compiler process exited 0 with no errors or warnings. All nine
printed declarations depend only on `propext`, `Classical.choice`, and
`Quot.sound`.

- Lean source SHA256:
  `50291df476b0e2a021a06b95b326d61d5f86cd973bdf3f6c0620c5c358f6c11c`
- Lean results SHA256:
  `673af0985e5742f2a50f259ffa831527944ac28c05f0a1d142e3bc990c0ff3f4`
- Lean stdout SHA256:
  `d71b1f0646fbbec92f14a0ecdd5b782db1145315e8a1b203549019073a4ed565`

The formal statements certify supplied real-algebra bridges, including that
distinct positive trace couplings yield distinct vacuum constants while
preserving the displayed lapse/source/expansion relations. They do not
certify a continuum spectral inverse theorem, measured Newton calibration,
the full metric action, physical observations, or cosmological evolution.
Continuum integration, boundary arguments, and their exact hypotheses are
given separately in `REPORT.md`.
