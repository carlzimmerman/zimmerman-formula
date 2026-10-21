# Latest results after the main equation audit

20 October 2026. The reviewed `EQUATIONS_AND_MECHANISMS.md` is preserved at
SHA256 `c99fecfa0198d652cfbeebe4d2992d3f3f1a35506a3bd0f6f4b53281c6e65a5d`.
This addendum updates its homogeneous-stability and Claude-arrival status
without pretending the original goal is complete.

## Same-action homogeneous linear stability

[BULK_MODES.md](BULK_MODES.md) derives all five real amplitudes, including
charged-X rotation and the neutral field's different kinetic normalization.
The 10 by10 mode calculation passes35 checks at k=0,.001,.01,.1,1,10,100.
The low-k sound result matches thermodynamics to5.61e-7 relative. The
floating-point k=0 symmetry pair is explicitly preserved and separately
classified; it is not claimed to be exactly imaginary numerically.

There is also an algebraic sufficient condition, distinct from that finite
test. At an exact homogeneous stationary background with I>0,

    D=MX^2-4omega^2>0, B=U''(h)>0,
    S=2I[2(lambda-g^2/D)-a^2/B]>0,

the canonically normalized W0 is positive semidefinite, and
W(k)=W0+k^2*identity is positive definite for every k>0. The rotation matrix
G is skew. Therefore the quadratic fluctuation energy is positive and
conserved, making the mode generator similar to a skew-symmetric matrix
at every nonzero k. Its spectrum is imaginary under those hypotheses.

The numerical coexistence point has S=.999829693 and positive amplitude
eigenvalues with smallest .943767673. This is not an interval enclosure
of an exact nonlinear root, a stability proof for finite fragments, a
nonlinear phase diagram, or a measurement of escaped energy/J. The next
outgoing-boundary finite-fragment test remains necessary.

There are now **97 passed implementation checks across three completed
runner-v2 records**: run_00143, run_00319, and
bulk_run_001/repaired_run35. Two failed attempts remain in place: the old
uniform grand-potential calculation and a syntax-error bulk launch. The
completed peak RSS remains below187MB. Checks are neither independent
empirical confirmations nor full-theory closure.

## Claude CFG932: concrete missing-mass obstruction

[CLAUDE_CFG932_ARRIVAL.md](CLAUDE_CFG932_ARRIVAL.md) pins the local script,
outputs and exact input records. Its provisional saved output calls the
two-sided matter drift NON-CONSERVING and the efficiency window
BRACKET-DEPENDENT. Arithmetic reproduction is not physical validation:

- Six primary S_A corners use zero-cost entries arising from **no crossing
  despite positive surplus**, rather than no surplus. Five distinct system
  rows are affected before repeated cluster-BH corners.
- Sixteen system rows clip the law-fill radius while leaving supplied cold
  mass outside the smooth endpoint ledger. Eleven have a genuine inner
  equal-mass crossing, so their local cost can still be interpreted as that
  restricted diagnostic. The other five do not have such an endpoint.
- Clipped whole-catchment costs also omit a nonzero mass/energy boundary
  term. The code's cumulative profile jumps to the supplied mass outside
  the edge while its smooth mass derivative omits that receiver shell.

For example, the canonical EPS0.01/L100 Draco-like row leaves
5.33053e8 solar masses unplaced but assigns zero core cost. This feeds the
empty-window logic. The current class must not be promoted to a validated
physical feedback window before specifying a receiver and recomputing the
ledger. The audit does not edit/regrade Claude's frozen test.

[MASS_LEDGER_REPAIR.md](MASS_LEDGER_REPAIR.md) supplies the exact integration-
by-parts boundary term and a possible outer-shell accounting completion,
including shell self-energy and conditional orbit energy. This makes the
repair concrete: extend the fill boundary, specify a bound/escaping receiver,
or leave the endpoint undefined. It does not establish the formation or
stability of the receiver, an outflow rate, or the actual four-dwarf fit.

## Remaining first gate

The original goal remains **OPEN**. There is now an explicit common classical
matter model, bounded stationary fragments and a conditionally stable bulk
phase. The next physical implication is channel-resolved escaping E,Q,p and
galaxy-centred orbital J from finite same-action fragments, with an explicit
receiver, a conserved mass/charge ledger and the actual stellar observables.
`NEXT_TEST.json` retains that test. The normalization, abundance, cosmology,
force/metric choice and four-dwarf stock/selection gates remain open.
