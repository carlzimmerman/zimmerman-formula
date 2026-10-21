# Clock and top-form continuation

**The original goal is open.** Criteria-only commit 609570aa2 tests
new completions of the protected-auxiliary failure. [RESULT.md](RESULT.md)
contains the exact action, branch equations, force coefficients and
retained-mode obstructions. None yields a healthy microscopic xi=1/4.
Reviewed analytic/formal evidence: 65be2b68f. Campaign entries K693-K700
record the distinct scopes without adding a determinate physical trial.
The regenerated campaign integrity checks pass 4/4.

The fixed-clock chiral branch genuinely has positive rigid vacuum energy,
a leading cubic infrared response and a quadratic ultraviolet response.
The conditional ratio is R=4096/1125, giving xi=125pi/128 in the inherited
scalar-only dictionary. Its clock, stress and quantum bridges prevent
treating this as a determinate physical prediction. An allowed operator
deformation changes even that conditional ratio.

Promoting the clock reveals a physical homogeneous tilt tachyon in the
specified derivative-only unit-vector sector. A separate finite-gradient
chi mode has principal speed squared 75/67. The old timelike-root failure
is repaired; these are new retained-mode failures. Neither calculation
is an all-aether or all-gravity exclusion.

A top-form gives a separate exact MOND branch, including its Newtonian
crossover. Zero flux leaves its same-form vacuum energy zero. Nonzero
flux creates positive vacuum energy but restores a quadratic infrared
response and bounds force enhancement. A nominal target match would
remove the MOND window. The original action's extra branches cannot be
deleted using an unproved Legendre-Fenchel prescription.

[ClockTilt.lean](ClockTilt.lean) verifies seven algebraic statements:
the complete square, frequency sign, stiffness factorization/positivity,
conditional ratio and generic source bridge. The component, branch,
mode, force, actual-pi, gravity and quantum dictionaries remain analytic
inputs. W4-08 now has eight partial modules, not an end-to-end proof.

The true rational control file passes. Two separate controls falsely
assert stable tilt and a quarter ratio; each fails only at False, with
no import or type errors. Seven critical axiom prints use only standard
axioms. The first compile and independent unchanged final compile both
passed without warnings. [check_evidence.py](check_evidence.py) checks
source/dependency/object/log hashes, pins, limits and exact failures,
and binds the additional frozen contract to the raw runner manifests.

Reproduce from the repository root with fresh output directory names:

```sh
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py clock_flux/ClockTilt.lean clock_flux/runs/local_tilt
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py clock_flux/controls/Normal.lean clock_flux/runs/local_normal
```

Run TiltStable.lean and QuarterRatio.lean separately; each must exit 1
with an unsolved False goal. The shared existing pin and runner use one
worker, 1024 MiB, 30s CPU and 45s wall. No broad build, source download,
scan or reserved-file change. [SOURCES.md](SOURCES.md) and
[REVIEW.md](REVIEW.md) record external dictionaries and audit scope.
