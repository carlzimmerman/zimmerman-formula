# MUTATE — A24 wide-binary contradiction

## The mutation

`python3 a24_checks.py --mutate` removes the Galactic external field from the EFE check:
`y_ext → 0` in the same quadrature that K5 uses (`two_body(y_tot(2 Msun, 20 kAU), q=1, y_ext=0)`).

This is the mutation that matters, because "the external field is what carries the answer" is the
entire claim of the lane. If the check still passed with `y_ext = 0`, K5 would be testing the
quadrature rather than the EFE and the lane would have no result.

## Result: the mutation bites

```
[MUTATE] drop the external field from the EFE check (y_ext -> 0)
K5m FAIL 1.3980 |g-1.1814|<0.005   [MUTATED: EFE removed; K5 must fail]

MUTATION BIT: K5 FAILED as required.

A24 COMPLETE: 10/11 checks PASS.
```

Exit code **1** (the script exits non-zero iff any declared check fails).

- Unmutated: `γ_v(20 kAU) = 1.1811` — 0.0003 from the registered Arm A top 1.1814. K5 PASS.
- Mutated: `γ_v(20 kAU) = 1.3980` — 0.2166 above the band top, 7.8 σ_tot away. K5m FAIL.

The mutated value 1.3980 is the **isolated** exact two-body prediction: dropping the Galaxy returns the
number the October record would have had if it had used the exact composition instead of the
total-mass one. It shows the two effects are separable and that the check is sensitive to the right
one.

## A second, implicit mutation (recorded, not run by the flag)

Changing the mass from 2.0 to 1.5 M☉ at fixed separation moves γ_v by −0.0845, and changing the kernel
from canonical to the n = 2 quadrature law moves it by +0.1053. Neither is large enough to break K5
(both are < 0.11, while the check's tolerance is 0.015 for the canonical value): the check is
deliberately tight on the EFE and loose on the bookkeeping choices, because the lane's question is
which of those choices the framework is entitled to make.

## What the mutation does **not** demonstrate

It does not prove that 1.181 is right and 1.398 is wrong — both are correct predictions of the same law
under different assumptions about the argument of ν. What it proves is that the number the framework
registers is the one with the external field in it, and that removing the field is a real, numerically
decisive change rather than a relabelling.
