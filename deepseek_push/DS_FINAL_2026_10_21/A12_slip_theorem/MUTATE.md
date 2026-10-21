# MUTATE — does the slip check have teeth?

`a12_checks.py --mutate` installs one mutation. It must break a declared check; if it did not,
K6 would be vacuous.

## Mutation M1 — "only the potential contributes to the traceless stress"

The theorem's quantitative content is the identity (E3)

    Π_net / σ_clock = K r W' = r g = Ψ,        Π_net = Π_W + Π_clock = (−uW') + (+2uW') = +uW'.

M1 assumes the clock operator `P^i D_i lnN` contributes **no** traceless stress, i.e. `Π_net → 2uW'`
(effectively `Π_net = −uW'` in the code's sign convention, |Π/σ| = 2rg instead of rg). This is a natural
mistake — the clock term is linear in `P`, so "it cannot carry a stress" is plausible — and it changes the
answer by exactly a factor 2, not by a sign that an `abs` would hide (an earlier M1 version that only
dropped the clock *sign* passed, because |−uW'| = |+uW'|; that mutation was discarded as toothless).

## Mutated output (verbatim, `python3 a12_checks.py --mutate`, exit 1)

```
K6 FAIL Pi/sigma=2*g*r == r g   # exact identity: net traceless stress / clock charge = local potential Psi
K11 PASS mutated_identity_delta=-3*g*r !=0   # MUTATION: only W contributes to the traceless stress -> K6 must FAIL

A12 COMPLETE: 10/11 checks PASS.
```

Full mutated stdout: `mutate.out`.

## What this proves

- K6 is a genuine two-term cancellation, not an identity that any single term satisfies: removing one
  of the two contributions breaks it at factor 2.
- The remaining checks (K1–K5, K7–K10) are insensitive to M1 by construction (they test the lemma, the
  classification, the profile integral, the counterexample and the data) — the mutation is surgical.

## Unmutated baseline (`python3 a12_checks.py`, exit 0)

```
K6 PASS |Pi/sigma|=g*r == r g   # exact identity: net traceless stress / clock charge = local potential Psi
A12 COMPLETE: 11/11 checks PASS.
```
