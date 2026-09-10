# Development checks and rejected evidence

Before implementation, each of the four root helper test modules was run and
failed because the requested helper did not exist. The corresponding tests
were rerun after implementation. The exact failure/green commands use
`python3 -m unittest -v` and the relevant `test_*.py` filename from this folder.

The first `continue_seeds.py` development run omitted the coordinate guard in
the independent multiprecision pair constructor. At `u1=100` it returned
`Dcoord1` about `-2.1361e13`; similar false regular candidates appeared at
`u1=1000,10000`. These are invalid in the required orientation-preserving
chart and are **rejected**, irrespective of their tiny normalized optimizer
residuals. No claim or final formal evidence relies on that run.

The new regression
`test_high_precision_gate.PrecisionTests.test_extrapolation_outside_coordinate_branch_rejected`
was observed to fail (exit 1) before adding the missing branch guard and
passes afterward. The guard checks the real pressure root, positive target B,
and positive coordinate factors. Negative nonzero field-map determinant
`2(F-X f)` is not, by itself, rejected as a singular map.

A subsequent continuation predictor scales the *initial guess* for U2 with
the proposed U1. This changes solver conditioning, not any field equation or
physical parameter. Only a converged, branch-checked solution is retained.
The final bounded run records the precise resulting source hashes.

Independent review also reproduced an equal-mass algebraic match at
`f=1.05,F=.525,X=.5`, where the field-map determinant vanishes. The candidate
acceptance filter now rejects zero (but not negative nonzero) determinants;
the new regression was observed failing before this correction. Exceptional
zero next-control vectors are tested separately instead of being implicitly
classified as physical failures. The reported distinct-mass seeds are away
from these exceptional sectors.

The independent reviewer re-read the corrected source and confirmed both
reported defects resolved, with no remaining load-bearing issue in that
bounded recheck. This code review does not extend the mathematical scope.

Exploratory results are not asserted as exact numerical enclosures. In
particular, normalizing determinants can hide an absolute near-degeneracy;
the load-bearing seed reports therefore also retain actual N/B components,
individual required controls, direct raw-jet mismatches, independent
high-precision checks, and direct health evaluations.
