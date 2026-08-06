# 03 — NUMERIC HAZARDS (read before writing any float arithmetic)

Each of these has **actually shipped a wrong result in this project**. The count is in brackets.

## H1 — `1 − exp(−x)` underflows to exactly 1.0 [3 times]

For x ≳ 37, `1.0 - math.exp(-x) == 1.0` in float64. Strict inequalities then read as equalities and checks pass
spuriously.

```python
# WRONG                          # RIGHT
1.0 - math.exp(-x)               -math.expm1(-x)
math.log(1.0 - math.exp(-x))     math.log1p(-math.exp(-x))   # and guard x -> 0 separately
```

## H2 — Catastrophic cancellation in a difference of nearly-equal quantities [2 times]

`√(1+a²) − 1` at a = 1e-7: the true value is 5e-15, but float64 knows `1+1e-14` to only ~1e-16 absolute, so the
difference carries ~2% error. Same disease: `1/D(s) − 1/s²` near s = 0, where both terms are ~1e18 and the
difference should be O(1) — 30 digits leave 1e-12 of noise and the check failed by 5.8e4.

```python
# WRONG                          # RIGHT (algebraic rewrite)
math.sqrt(1+a*a) - 1             a*a / (math.sqrt(1+a*a) + 1)
1/D(s) - 1/s**2                  use the series  -P/12 + s**2*(P**2/144 - Q/360)  for s < 1e-6
```
**Rule: if a check reads a difference of two nearly-equal large numbers, it is measuring rounding, not physics.**

## H3 — Overflow in the intermediate, not the answer [1 time]

`exp(s)/expm1(s)**2` overflows for s ≳ 350 even though the value is tiny. Rearrange to log space first.

## H4 — `x − 1` underflowing to exactly 0 kills `log10` [1 time]

`nu(y) - 1` at y = 1e11 is ~5e-12 → fine; at y = 1e17 it underflows to 0.0 and `log10(0)` blows up. Write the
quantity in log space from the start:
```python
def log_nu_minus1(y):            # log(nu-1) for nu = 1/(1-e^-sqrt y)
    s = math.sqrt(y)
    return -s - math.log1p(-math.exp(-s))
```

## H5 — Coarse grids reporting an extremum they never sampled [2 times]

A 6-point grid reported a minimum at 1.000× when the true minimum at 0.921× was never evaluated. A 0.15-step
scan reported "zero cells clear". **Refine any grid by 4× and confirm the answer does not move.**

## H6 — Tolerances loose enough to pass a real miss [1 time]

`abs(x - 2.1) < 0.8` is a 38% tolerance and it passed a 36% miss. **Pick the tolerance from the precision of
the method, never from the size of the discrepancy you are looking at.** If you had to widen a tolerance to make
a check pass, the check has failed.

## H7 — Variable rebinding clobbering a symbol [1 time]

`for nm, wv in SCAN:` overwrote the sympy symbol `wv = Symbol("w")` used 40 lines later, so a downstream
symbolic check silently compared an expression against a float. **Never reuse a name that holds a sympy symbol
as a loop variable.** Prefix loop variables (`_wc`, `cand_w`).

## H8 — Dropping a factor of c (or 2) between two lines [several]

`a_φ = c²√X`, not `c√X`. Check dimensions numerically at least once per script:
```python
assert abs(math.log10(abs(value)) - math.log10(abs(expected_order))) < 1.0, "wrong order of magnitude"
```

## Mandatory hygiene for every script

1. **Print the order of magnitude** of every physical result and eyeball it against `04_FRAMEWORK_FACTS.md`.
2. **Refine once.** Any grid, any quadrature, any series: run it again at 4× resolution / one more order and
   confirm the claim does not move. Print both.
3. **Prove by moving the number.** Change an input that *should* change the answer and confirm it moves by the
   predicted factor. Change one that should *not* and confirm it does not. Do at least one of each. This single
   habit has caught more errors here than everything else combined.
4. For symbolic work, **verify the closed form against a numeric evaluation** at 3 points. `sympy.simplify`
   returning something unproved is common — it not proving an identity does not mean the identity is false, and
   it proving one does not mean your expression was what you meant.
5. Use `mpmath` with `mp.dps >= 30` for oscillatory integrals, pole subtractions, and anything with a
   near-cancellation. Say in the docstring why the precision was needed.
