# MUTATE — what must break, and why it is not a strawman

Run: `python3 a4_checks.py --mutate` (full captured output: `mutate.out`, exit code 1).

## The mutation

The mutation assigns the **quadrature** law's strong-field content to the **canonical** law:

| quantity | correct (canonical) | mutated |
|---|---|---|
| constant anomaly `Δg/a₀` | `1` | `1/2` (A_CONST) |
| `lim y(ν−1)` | `1` | `1/2` (TAIL_CAN) |
| closure leading coefficient | `π/2` (CLOSURE) | `π/4` |
| closure constant | `C_can = −0.8862943611` | `C_quad = −0.1107867951` (C_MODEL) |

This is the exact error the tasking itself contained once (it asserted the canonical law had a
`1/√y` tail and, implicitly, that the two laws could share the quadrature's cure) and the error
anyone would make by carrying the published `1279×` / `y_t ≈ 94–129` numbers across to the
canonical member without redoing the algebra.

## Mutated output (check lines)

```
K1   PASS 1                        1 exactly (sympy)        g-g_N -> 1*a0 ; quadrature -> 1/2*a0
K2   FAIL 1278.68852               2558 (=2x1279) +-0.2%    a0/B_E=1278.69  a0_alt/B_E=1543.72  ratio/(2*1279)=0.499878
K3   FAIL 1                        1 exactly (sympy)        lim y(nu_can-1)=1 lim y(nu_quad-1)=1/2 lim sqrt(y)(nu_can-1)=0 -> both tails 1/y, NOT 1/sqrt(y)
K4   PASS -0.999999785             -1 +-1e-6                d ln(nu-1)/d ln y over 1e6..1e8
K5   PASS 1.00000021               1 +-1e-3                 linear divergence (exponent 1), NOT 3/2;  slope_quad=1.00000006
K6   FAIL -0.886294393             -0.8862943611 +-1e-6     identity ratio=8 ; asym closure rel.err=1.04
K7   FAIL 132.437858               66.2999 (exact root)     closure (pi/2)y_t - ln(y_t/4) + C_can = Lambda c^4/a0^2 reproduces the exact root
K8   PASS 1.97068312               in [1.90,2.05]           published closure reproduced to 0.00191 ; transplant over-predicts Lambda
K9   PASS 0.0119718493             < 1 (ratio anom/bound)   worst = Neptune ; Uranus/Neptune(*) use the Saturn bound as an over-tight stand-in
K10  PASS 9.13970811               > 2 (factor margin)      compatible: one y_t does both jobs
K11  PASS 1.06066017               > 0 everywhere           min over u in (0,a0]; divergence only at u=0, positive and integrable
K12  PASS 1060.26232               > 10                     the cure is gradient-stable; instability only for y_t < 0.06253
K13  PASS 2557.37705               > 1 (excluded)           any interpolation with a 1/x term in mu has a constant anomaly c*a0; c must be < 0.000391

A4 COMPLETE: 9/13 checks PASS.
```

## What each broken check proves

- **K2** is the ephemeris gate. With `Δg = a₀/2` it reports 1278.69, i.e. it reproduces the
  *published* 1279 and fails the canonical 2558 by exactly 2×. So K2 is not a tautology on `a0`:
  it distinguishes the two members of the framework.
- **K3** is the tail-coefficient assertion (`lim y(ν−1) = 1`, with `√y(ν−1) → 0` excluding the
  1/√y hypothesis). The mutation's 1/2 is the quadrature's coefficient and is rejected.
- **K6** is the closure-asymptotics check: the mutated closure no longer describes the exact
  canonical integral (residual 104% instead of 4.3×10⁻⁴), so the check has teeth on the
  *functional form* of the closure, not just on a prefactor.
- **K7** is the `y_t` inversion. The mutated closure inverts to 132.44 while the exact integral
  root is 66.30 — a 99.8% discrepancy that the check rejects. This is the load-bearing
  "one `y_t`" number, and it cannot be reached with the quadrature's coefficients.

Checks that stay PASS under mutation are the ones the mutation does not touch: K4/K5 (the exact
tail exponent and divergence exponent — sympy/numeric facts about the canonical law), K8 (the
normalization cross-check, which is computed from the unmutated exact quadrature integral),
K9–K12 (planet gate, compatibility, response, patched monotonicity), K13 (the general `c = lim
x(1−μ)` gate, computed from exact μ's). That is the intended pattern: a mutation of the physics
input breaks the physics checks and leaves the mathematical certificates intact.
