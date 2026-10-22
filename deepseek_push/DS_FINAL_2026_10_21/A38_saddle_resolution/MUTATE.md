# MUTATE — A38

Two silent errors are injected, one per lane, and each is the *exact* mistake that lane is suspected
of. Neither touches the physics or the solver; both change only the bookkeeping that converts a
dimensionless column into a quoted number.

Run:

```
python3 a38_checks.py                     # 17/17 PASS
python3 a38_checks.py --mutate=config     # K9 fails
python3 a38_checks.py --mutate=completion # K10 and K12 fail
```

## 1. `--mutate=config` — the (M_b, d) rescaling dropped

**Injected:** `U_A13 := U_A6`, i.e. the two lanes are treated as if they had used the same pair
(1.4e11 M☉ at 780 kpc) when A13 in fact used 8e10 at 0.77 Mpc.

**What the lane then sees.** The configuration factor becomes 1.000, so the factorisation
`3.529 / 2.159 = configuration × completion` requires a completion ratio of 1.635 instead of 1.238.
That is 32 % larger than any completion difference the two theories actually have, and it cannot be
absorbed by any of the four definitional suspects (all measured at ≤0.8 % in K11–K13). The lane would
be forced to invent a numerical error in one of the codes.

**Caught by:** K9 — `1.0000 × 1.2382 = 1.2382` against `3.529/2.159 = 1.6345`, **24 % off**.
Everything else passes: this mutation is invisible unless the two factors are separated, which is the
point.

## 2. `--mutate=completion` — QUMOND substituted for the theory

**Injected:** `S_AQ := |negative column| / U_A6`, i.e. A6's algebraic completion is allowed to stand
for the theory's field equation. This is not a hypothetical: it is A6's actual calculation.

**What the lane then sees.** The recommended table entry becomes 3.471 M☉/pc² instead of 2.867, and
the "cross-check" of the completion ratio becomes 1.000 — the two completions are declared identical.

**Caught by:**
* K10 — independent completion ratio `1.0000` against the required `1.2382`;
* K12 — the table entry `3.471` falls outside the 2.7–3.1 window.

K5–K8 still pass, because the AQUAL solve itself is untouched. The mutation therefore isolates
exactly one thing: *which theory the answer belongs to*.

## Why these two

The whole finding of this lane is that the 1.5× is a product of two factors, 1.306 and 1.24, and that
neither is a numerical error. A mutation test that only perturbs the numerics would not test that
claim. Each mutation here deletes one factor and shows that the lane's decisive check — the
factorisation, or the completion cross-check — fails immediately and unambiguously, while the
solver's own controls stay green.
