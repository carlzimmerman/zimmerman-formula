# A58 — mutation controls

A check that cannot fail is not a check. Each mutation below perturbs **one** input of
`a58_checks.py`, leaves everything else fixed, and must break at least one declared check.
Baseline is `36/36 PASS`, exit 0. Mutated runs exit 0 iff at least one check fails (the
mutation is confirmed); the captured outputs are `a58_MUTATE_<id>.out`.

Run: `python3 a58_checks.py --mutate=<z|r32|kappa>`

---

## M1 `--mutate=z` — perturb the closure constant by 0.1 %

`Z = 2√(8π/3)` is multiplied by 1.001. This is the smallest perturbation that a rounding
could plausibly produce, and it must be visible in every quantity derived from `Z`.

```
K1   FAIL 5.794598847            5.788810036 +/-1e-8
K2   FAIL 0.1727470747           0.1725745002 +/-1e-9
K4   FAIL 0.0342335              0.035196 +/-2e-5
K5   FAIL 0.0777610              >0.03, expect 0.078683
MUTATION z: 4/36 checks FAIL.
MUTATION CONFIRMED
```

Teeth: K1 is the identity `2√(32π/3) = 2Z`; K2 is `a0/(cH_Λ) = 1/Z` (the measured side is
mutation-independent, so the *prediction* moves); K4 is the 3.520 % deviation of the 1/12
reading, which collapses to 3.423 %; K5 is the 7.868 % gap from 1/2 to the nearest ladder
entry, which collapses to 7.776 %. A 0.1 % error in `Z` is a 0.1 % error in every κ claim —
that is why the constant is carried to nine digits.

## M2 `--mutate=r32` — use 32 instead of 32π in `a0 = c²√(Λ/32π)`

This is the single most common transcription error in this literature (dropping the π from
the Einstein 8π/3 bookkeeping). It must break the value of `a0`, not merely its label.

```
K2   FAIL 0.3061862178           0.1727470747 +/-1e-9
K3   FAIL 1.657984e-10           9.354173e-11 +/-2e-5
K8   FAIL 4.360e-01              <1e-3 (internal)
MUTATION r32: 3/36 checks FAIL.
MUTATION CONFIRMED
```

Teeth: `a0` becomes 1.658e-10 (77 % high), so `a0/(cH_Λ)` becomes 0.306 — not `1/Z`;
K3's absolute value misses by 77 %; and K8, which compares the Λ-derived `a0` with the
ρ_Λ-derived one, misses by 44 %. Every κ claim then shifts with it: the "horizon ratio"
becomes 1/3.27 instead of 1/5.79, which is how a bookkeeping error of this kind silently
rewrites the numerology built on it.

## M3 `--mutate=kappa` — set κ to the 1/12 value (0.4824008) in the closure

This is the substantive mutation: it asks what happens if one believes the "1/12 of the
horizon" reading rather than κ = 1/2. The closure `I(y_t) = 8π/κ²` must move `y_t`.

```
K11  FAIL 71.1517 ; alt -0.30626 66.30 +/-2e-3 ; -0.306
MUTATION kappa: 1/36 checks FAIL.
MUTATION CONFIRMED
```

Teeth: `y_t` moves from 66.30 to 71.15, **+7.3 %**. This is the quantitative answer to
"is 1/12 harmless?" — it is not: a 7.3 % shift in the turn-off that closes `Λ`. The 1/12
reading lands at 71.15 (still inside the theory's [60, 140] band); the alt footing lands at
46.01 (outside it). K11 is the check that ties κ to the gate sector, so breaking it is the
signal that the two answers are not independent.

---

## Negative control

Mutation runs write `a58_results_MUTATE_<id>.json`, so the deliverable `a58_results.json`
always holds the baseline. (The first version of this harness overwrote it on every
`--mutate` run — the same class of defect as K14's vacuous pass: an artifact that silently
stops being what it claims to be.)

`python3 a58_checks.py` with no flag: `36/36 PASS`, exit 0, 0.4 s. The three mutations
together fail 4 + 3 + 1 = 8 check-instances across three disjoint check sets
({K1,K2,K4,K5}, {K2,K3,K8}, {K11}); no check fails in the baseline. K2 appears in both M1
and M2 because it is downstream of both `Z` and the 32π normalisation — that is intended.

## A mutation of the *check*, recorded because it is the defect this lane charges

The first version of K14 passed with **zero roots**: `sympy.solve(g**2 + a**2, g)` returns
`[]` when `g` is declared `positive=True`, and `all(...)` over an empty list is vacuously
true. The check therefore "verified" the n=2 branch points by asserting nothing. It was
replaced with `sp.roots`, which returns `{-I*a: 1, I*a: 1}`, and the check now asserts
`len(bp) == 2`, `Re = 0`, `|Im| = a`. The lesson is the one A31 applied to A22's
`if den == 0: alpha1 = 0`: a branch that asserts the answer is not a check, and a
universal quantifier over an empty set is the same branch in disguise.
