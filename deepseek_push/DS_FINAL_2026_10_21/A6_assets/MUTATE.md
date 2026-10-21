# MUTATE — A6_assets

Two mutations are wired into `a6_checks.py`, both of them in the saddle section (the only
section whose result depends on a convention rather than on algebra).

| flag | mutation | rationale |
|---|---|---|
| `--mutate` (default) | `SIGN = -1` in `rho_cold = -div(g-g_N)/(4 pi G)` | the *silent* error: the convention `div g = -4 pi G rho` is what makes the pancake density negative and therefore what makes the no-go exist. Flip it and the identical computation reports positive cold density exactly where the law demands negative mass; the asset quietly becomes a null statement. |
| `--mutate=nu` | `nu(y) -> 1`, `dnu -> 0` (cold sector switched off, pure Newton) | the *gross* error: if the medium carries no polarization there is no cold density at all, so every saddle number must collapse. |

`K1` is deliberately **independent of `SIGN`**: it computes `div u` by central differences
of `u = (nu-1) g_N` with the physical sign hard-coded in `rho_cold_fd`. So a sign error
fails the algebra-validation check itself (relative error 2.00 = a pure flip), not just
the downstream ones.

## Captured output — `python3 a6_checks.py --mutate` (exit 1)

```
K1  FAIL max rel err 2.00e+00                        < 1e-4
K2  FAIL rho_panc/rho_axis = -0.1769                 < 0
K3  FAIL 89.3                                        -89 +-15%
K4  FAIL d(-33)=11.8 Mpc, rho(3Mpc)=485              d(-33) > 8 Mpc
K4b FAIL ratio 33.1, col_neg -1.57 Msun/pc2          -33 +-10% and 4.63 - 5.5
K5  FAIL -1.10 Msun/pc2                              1.4 - 4.2 (claim 1.9-2.1)
K6  FAIL 2.42 Msun/pc2 (net/|neg| = 2.19)            net < 0
K7  PASS spread 0.597%                               < 2%
K8  FAIL solid-angle fraction 0.737                  0.05 - 0.40
K9  FAIL N(3sig)=8.45e+04 pairs, 120.7x              multiple in 8 - 18
K10..K20 PASS                                        (sympy: no rho_cold involved)
A6 COMPLETE: 12/21 checks PASS.
```

**9 of 21 break**, all nine in the saddle section. The single survivor, `K7`, tests
`|rho| sqrt(r)` — sign-blind by construction, which is exactly what it should be; the
mutation must not be able to hide behind an absolute value, and it does not, because the
other eight catch it.

## Captured output — `python3 a6_checks.py --mutate=nu` (exit 1)

```
K1  FAIL max rel err inf                            < 1e-4
K2  FAIL rho_panc/rho_axis = +nan                    < 0
K3  FAIL 0.0                                         -89 +-15%
K4  FAIL d(-33)=1.0 Mpc, rho(3Mpc)=0                 d(-33) > 8 Mpc
K4b FAIL ratio 0.0, col_neg 0.00 Msun/pc2            -33 +-10% and 4.63 - 5.5
K5  FAIL 0.00 Msun/pc2                               1.4 - 4.2 (claim 1.9-2.1)
K6  FAIL 0.00 Msun/pc2 (net/|neg| = nan)             net < 0
K7  FAIL spread inf%                                 < 2%
K8  FAIL solid-angle fraction 0.000                  0.05 - 0.40
K9  FAIL N(3sig)=inf pairs, infx                     multiple in 8 - 18
K10..K20 PASS
A6 COMPLETE: 11/21 checks PASS.
```

The two mutations differ by exactly one check (`K7`): with `nu = 1` the cusp amplitude is
zero, so even the sign-blind test sees it, whereas a sign flip leaves `|rho|` untouched.
That is the whole design of the check pair, and it is why `K7` is written on the modulus
and `K2/K3/K8` on the signed value.
