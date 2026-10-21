# A10 mutations — do the checks have teeth?

`python3 a10_checks.py --mutate` (or `A10_MUTATE=1`) turns on four mutations of the *claim under test*,
each of which must turn its check red. The unmutated run is `a10.out` (18/18 PASS, exit 0); the mutated run
is `a10_MUTATE.out` (17/21 PASS, **exit 1**).

| id | mutation | check it must break | result |
|---|---|---|---|
| **K1** | use the **b=2** member where the claim says the b=1 member *is* P2 | K1 (b=1 kernel ≡ `g²/(g+a0)`) | **FAIL** |
| **M1** | set the b=1 tail coefficient to `1/2` instead of `1` | K7 (`lim y(ν−1) = 1/b`) | **FAIL** |
| **M2** | assert the 2π cell count gives `κ = 1/2` exactly | K9 (no count gives 1/2) | **FAIL** |
| **M3** | assert the b=2 capacity is `a0`, not `a0/2` | K6 (`sup (g−g_N)/a0 = 1/b`) | **FAIL** |

Each mutation is the *neighbouring* physical claim, not a typo: K1 is "the two kernels are the same theory",
M1 is "the anomaly is a0/2 for both kernels", M2 is "the modular count lands on the canonical κ", M3 is
"both kernels have the same capacity". These are exactly the four confusions a reader could make, so the
failures show the checks discriminate the claims rather than the arithmetic.

## Recorded mutated output

```
$ python3 a10_checks.py --mutate
A10 -- one principle for two postulates: exact test of candidates (i)/(ii)/(iii)
a0_can = 9.3600e-11 m/s^2 (INPUT, BRIEF Sec.4);  kappa = 0.50 FITTED;  footings never pooled
mutate = True
...
  [FAIL] K1   |b=2 kernel - g^2/(g+a0)| = (-g**2 + (-a_0 + sqrt(a_0**2 + 4*g**2))*(a_0 + g)/2)/(a_0 + g)  |  THRESHOLD: identically 0 (sympy simplify)  |  b=1 is exactly P2; b=2 is not
...
  [PASS] K9   min_N |kappa(N)-1/2|/(1/2) = 0.0787 at kappa(2pi)=0.460659 ; N(1/2)=5.7888  |  THRESHOLD: > 0.01 (no admissible count gives 1/2)  |  nearest count is 7.9% away
...
  [FAIL] M1   mutated tail coeff b=1 -> 1/2  |  THRESHOLD: must equal 1  |  MUTATION: flipping the tail coefficient
  [FAIL] M2   mutated claim kappa(2pi)=0.460659 == 1/2  |  THRESHOLD: must equal 0.5 to 1e-6  |  MUTATION: asserting the count lands on 1/2
  [FAIL] M3   mutated claim capacity(b=2)=1/2 a0  |  THRESHOLD: must equal 1 a0  |  MUTATION: asserting the quadrature capacity is a0

A10 COMPLETE: 17/21 checks PASS.
$ echo $?
1
```

Note the shape of the mutated K1 residual: it is a nonzero *symbolic* expression, not a numerical tolerance
failure — the identity is checked by `sympy.simplify`, so no threshold can be tuned to make b=2 pass.

## What the mutations do **not** test

- The SPARC measurement (K15–K17) is not mutated: those checks report a *limitation* (the Υ lever arm
  exceeds the b-split), and their pass condition is that the limitation is real. A meaningful mutation would
  be to fake a smaller Υ lever, which is a different claim about the data rather than about the theory.
- K10's irrationality is a `sympy` assumption plus a one-line proof (Lindemann); the numeric scan printed as
  a control (`161/932`, residual 2.9e-07) is *not* the proof and is labelled as a control in the output.
