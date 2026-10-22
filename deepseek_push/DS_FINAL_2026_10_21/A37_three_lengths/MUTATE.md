# A37 — mutations

Five mutations, one per identity family. Each sets a length to the *wrong one* (or the wrong
root) and must break a check; every one exits 1. Captured outputs: `a37_MUTATE_M1.out` …
`a37_MUTATE_M5.out`.

Run as `python3 a37_checks.py --mutate M1` etc.

| id | mutation | physics it breaks | check(s) that fail | score |
|---|---|---|---|---|
| **M1** | `σ_c → c` in the hierarchy | makes the cold medium relativistic, so the stiffness length *is* the MOND length | **K4** (`L*/L_MOND = 1`, `log₁₀ = 0`, `L* = 3.11e10 pc`) | 9/10 |
| **M2** | `κ := 2ell_1/L` (the "diameter" reading of the cell) | identifies the cell radius with half the MOND length twice over | **K2** (`R − 1/κ² = 3Λc⁴/(32πa₀²) ≠ 0`), **K3** (solution sets no longer coincide) | 8/10 |
| **M3** | `L* := c²/a₀` — the brief's own error (FINAL #16) | uses the MOND length as the stiffness length | **K1** (`L* = 9.6021e26 m = 3.11e10 pc`, separation 0 decades), **K9** (`m/H₀ = 0.20` instead of 2.62e8) | 8/10 |
| **M4** | the cell length inserted in the 32π box | forces `Λell_1² = 32π` when it is `8π` | **K7** (`Λell_1²/32π = 1.0000`, not 0.25) | 9/10 |
| **M5** | treat `L = 2ell_1` as a definition rather than the closure | erases the 0.06 % footing residue that distinguishes the identity from a measurement | **K10** | 9/10 |

## Captured output

```
$ python3 a37_checks.py --mutate M1        # exit 1
K4  FAIL L*/L_MOND = (sigma_c/c)^2 = 1.0000e+00, log10 = 0.0000; L* = 31118238990.717 pc
A37 COMPLETE: 9/10 checks PASS.

$ python3 a37_checks.py --mutate M2        # exit 1
K2  FAIL max residual 3*Lambda*c**4/(32*pi*a0**2)
K3  FAIL three solutions identical: a0 = c^2 sqrt(Lambda/32 pi); L/ell_1(footing)=1.99876
A37 COMPLETE: 8/10 checks PASS.

$ python3 a37_checks.py --mutate M3        # exit 1
K1  FAIL L_MOND=9.6021e+26 m (31.12 Gpc); ell_1=4.8040e+26 m (15.57 Gpc); L*=9.6021e+26 m (31118238990.72 pc)
K9  FAIL lambda_P = L*/sqrt2 = 22003917808.9199 pc; m/H0 = 2.021426e-01
A37 COMPLETE: 8/10 checks PASS.

$ python3 a37_checks.py --mutate M4        # exit 1
K7  FAIL cell in box: Lambda ell_1^2/32pi = 1.0000 (R=1.000)
A37 COMPLETE: 9/10 checks PASS.

$ python3 a37_checks.py --mutate M5        # exit 1
K10 FAIL L/ell_1 = 2.000000 at a0(32pi) = 9.354173e-11; 1.998755 at the BRIEF footing
A37 COMPLETE: 9/10 checks PASS.
```

## Why these five

They are exactly the five ways the record's glyphs can be swapped, and each is a real site from
§3 of the report rather than a synthetic perturbation:

- **M1** is the hierarchy's only content: `(σ_c/c)²`. If the medium were relativistic there would
  be no hierarchy to explain.
- **M2** is A27's "diameter vs radius" question, taken as a definition of `κ`.
- **M3** is the brief's `L* = c²/a₀`, recorded at `FINAL_THEORY.md:588`, which A30 caught.
- **M4** is `FINAL_THEORY.md:134` read with `FINAL_THEORY.md:28`'s definition of `ell_0`.
- **M5** is the difference between `L = 2ell_1` as an identity and as the closure that *defines*
  the canonical footing; confusing them is how `ΛL² = 32π` gets quoted at a footing where it is
  false by 0.06 %.

## What the mutations do not touch

The audit (K5, K6) and the symbol table (K8) are structural: they read the lanes and the table,
so no physics mutation can move them. `--mutate` deliberately leaves them alone — a mutation
that changed a grep result would be testing the scanner, not the physics.
