# Independent audit of the screened-kernel branch

The newest screened-kernel work is a useful constructive test, not closure.
Run from this directory (the tests import `screened_kernel` by module name):

```text
python3 -m unittest discover -s . -p 'test_*.py'
```

This gives **14/14**.  The direct causal requirement is intentionally not
passed:

```text
python3 screened_kernel.py --require-causal-screen   # exit 2
```

The algebraic residuals vanish and the proposed quadratic kernel matches the
screened static density, but the expanding linear Cauchy witness is marked
`FAIL`.  A compact annular initial perturbation produces a nonzero second time
jet of the gauge-invariant relational density inside a region whose original
canonical data vanish.  Under the stated regular-flow and metric-cone
assumptions this is an instantaneous-support obstruction.

The branch itself explicitly records that its nonlinear ADM expression only
matches the quadratic density: full metric/lapse variation, inverse-operator
domains, covariant clock restoration, functional constraints, PPN, and
nonlinear stability remain open.  Its current status is therefore
**causality-obstructed/open**, not a complete theory.
