# A8 — mutation: the C3 ordering must fail when reversed

Two mutation channels, both with captured evidence.

## 1. `A8_C3_MUTATE.lean` — a false variant of C3 that must not compile

The file contains the *real* supporting lemmas (copied from
`A8_C3_law_ordering.lean`, all proven) and two deliberately false statements:

| mutant | statement | truth |
|--------|-----------|-------|
| `gCanon_le_gQuad_MUTANT` | `g_c <= g_q` for all `gN, a0 > 0` | **false**: `g_q < g_c` strictly (proven in C3) |
| `gCanon_eq_gQuad_MUTANT` | `g_c = g_q` for all `gN, a0 > 0` | **false**: the gap is `a0 gN^2/(g_c(g_c+g_q)) > 0` |

Numerical counterexample (python, not a proof): `gN = 1`, `a0 = 1` gives
`g_q = 1.414213562`, `g_c = 1.618033989`, gap `0.203820426`, so both mutants are
false on the very first point of the positive quadrant.

### Captured compiler output (`A8_C3_MUTATE.out`, verbatim)

```
/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/DS_FINAL_2026_10_21/A8_lean/A8_C3_MUTATE.lean:73:4: error: linarith failed to find a contradiction
gN a0 : ℝ
hgN : 0 < gN
ha0 : 0 < a0
hcgt : gN < gCanon gN a0
h : gCanon gN a0 ^ 2 - gQuad gN a0 ^ 2 = gN * (gCanon gN a0 - gN)
a✝ : gQuad gN a0 ^ 2 < gCanon gN a0 ^ 2
⊢ False
failed
/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/DS_FINAL_2026_10_21/A8_lean/A8_C3_MUTATE.lean:87:4: error: linarith failed to find a contradiction
case h2
gN a0 : ℝ
hgN : 0 < gN
ha0 : 0 < a0
hcgt : gN < gCanon gN a0
h : gCanon gN a0 ^ 2 - gQuad gN a0 ^ 2 = gN * (gCanon gN a0 - gN)
a✝ : gQuad gN a0 ^ 2 < gCanon gN a0 ^ 2
⊢ False
failed
EXIT=1
```

Both mutants are rejected at the exact step where the (true) difference-of-squares
identity is asked to support the (false) reversed inequality. Note the shape of the
refutation: the arithmetic derives `gQuad^2 < gCanon^2`, i.e. the *opposite* of the
mutant, from the same identity the real proof uses. The mutation therefore tests the
direction of the inequality, not merely "some tactic fails".

## 2. `a8_lean_checks.py --mutate` — a false numerical claim must fail a check

Normal run: `A8 COMPLETE: 8/8 checks PASS.` (exit 0).
Mutated run replaces K5 by the false "one twelfth of the horizon" identity
(`|1/(2Z) - 1/12| < 1e-3`).

### Captured output (`a8_lean_checks_MUTATE.out`, verbatim)

```
# MUTATED RUN: K5 asserts the false 1/12 identity
K1 PASS 4/4 clean build logs 4/4
K2 PASS 40/40 theorems with exactly the allowed axioms 40/40
K3 PASS 4/4 sources free of 'sorry' 4/4
K4 PASS mutant rejected error + EXIT=1  # A8_C3_MUTATE.lean
K5 FAIL |1/(2Z)-1/12|=3.040204e-03 1e-3 (MUTATED CLAIM)
K6 PASS a0/(cH_Lam)=0.172747074736 vs 1/Z=0.172747074736 rel=0.00e+00; a0 formula=9.3542e-11 vs quoted rel=6.23e-04 rel<1e-9 and a0 rel<2e-3  # H_Lam=c*sqrt(Lam/3)=1.806234e-18
K7 PASS gq=1.414213562 < gc=1.618033989, gap=0.203820426 0<gap<=min(gN,a0)=1  # witness gN=a0=1
K8 PASS max|gc/sqrt(a0gN)-1|=5.00e-05 max|gq/sqrt(a0gN)-1|=5.00e-09 1e-4  # delta=gN/a0 in {1e-8,1e-10}
A8 COMPLETE: 7/8 checks PASS.
EXIT=1
```

The measured deviation `3.04e-3` is `1/(2Z) - 1/12` exactly as expected from
`1/(2Z) = 0.086373537` vs `1/12 = 0.083333333` (3.65% relative). The mutation is
rejected by the check, so K5 is not a tautology.
