# MUTATE — A53_medium_candidates

## Mutation

`--mutate` changes exactly one thing: **the identified isotherm is made even.**

```python
F_ID = f_tanh if MUTATE else f_langmuir      # theta = tanh(g/a0)  vs  theta = x/(1+x)
MEDIUM_NAME = "tanh(even)" if MUTATE else "langmuir(one-sided)"
```

Everything else — constants, grids, the reference law `g_N = g^2/(g+a0)`, the cap functions, the
three response functions, the frequency tables — is untouched. `tanh` and the Langmuir isotherm
agree on everything the law is usually *assumed* to need: `f(0) = 0`, `f'(0) = 1`, `f(inf) = 1`,
capacity 1, affinity 1, `C/s = 1`. They differ in one number, `f''(0)`: `-2` for the one-sided
hard core, `0` for the even (symmetric) saturating response.

That is the mutation with teeth, because the lane's whole static claim is: **the law's `g_N ∝ g^2`
requires a one-sided response.** An even medium has an odd `g_N(g)`, no `g^2` term, and a deep
limit that is a cube root. If the identification checks survive `tanh`, they are not testing
one-sidedness at all.

## Why it must break

For `theta = tanh(g/a0)`:

```
g_N = g - a0 tanh(g/a0) = g^3/(3 a0^2) - 2 g^5/(15 a0^4) + ...
```

so the deep exponent is `1/3`, not `1/2` (K5), there is no `x^2` term and the cubic coefficient is
`+1/3`, not `-1` (K6), the isotherm is not `x/(1+x)` (K16), the response is symmetric under
`A -> -A` (K22), and at the knee `g_N(a0)/a0 = 1 - tanh(1) = 0.2384`, not the law's `0.5` (K36).
Five checks fire; the other thirty-five — the canonical identities, the `f_p` family, the Langevin
and BI algebra, the cap table, the parity theorem, the drag, the gap — are about the *structure*
and survive, which is the correct behaviour: the mutation is aimed at the identification, not at
the algebra.

## Mutated output

```
K5  FAIL 0.333333345533 1e-06  # identified medium (tanh(even)): deep exponent 0.333333346 (must be 1/2); f''(0)=0.000000 (must be -2)
K6  FAIL -1 0                  # g_N/a0 = x^2 - x^3 + ... (law, cubic -1); n=2 even (cubic 0); identified medium must have c2=1, c3=-1 (got 0.000000, 0.333333)
K16 FAIL 0 1e-14               # single occupancy + N internal states ...; identified medium is that isotherm (dev 2.6e-01)
K22 FAIL 0 1                  # ... the identified medium is one-sided: |F'(1/2)-F'(-1/2)| = 0.0000 (even media give exactly 0)
K36 FAIL 0.238405844044 1e-12  # identified medium: g_N(g=a0)/a0 = 0.238406 (the law's 0.5; a dead medium cannot fake it)
A53 COMPLETE: 35/40 checks PASS.
FAILED: K5,K6,K16,K22,K36
```

Exit code 1. Full capture: `a53_MUTATE.out`.

## What the mutation does *not* break, and why that is right

| check | survives because |
|---|---|
| K1, K2, K2b, K2c, K3, K4 | they are about the **reference law** and the general one-scale theorem, not about the identified medium |
| K7–K15 | Langevin and BI are fixed functions; the mutation does not touch them |
| K17–K21, K23–K35 | cap structure, parity theorem, drag, gap, frequency tables — structural, medium-independent |

The one place where a survivor is *interesting*: K21 (the parity theorem) still passes under
`tanh`, because it is stated for a generic even `F(A) = A^2/2 + alpha A^4/4` and shows that the
`g^2` coefficient is identically zero. That is the theorem the lane uses to exclude Langevin and
BI, and it is independent of which medium is "identified". The mutation shows the theorem is not
circular: the even isotherm it excludes is exactly the one the mutated run proposes.
