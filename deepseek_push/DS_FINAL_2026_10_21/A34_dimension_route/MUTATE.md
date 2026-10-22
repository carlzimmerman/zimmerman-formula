# A34 — mutations

Three mutations, each breaks exactly one declared check and nothing else. Run:

    python3 a34_checks.py --mutate=M1     # exit 1, 12/13
    python3 a34_checks.py --mutate=M2     # exit 1, 12/13
    python3 a34_checks.py --mutate=M3     # exit 1, 12/13

Captured stdout is in `a34_MUTATE_M1.out`, `a34_MUTATE_M2.out`, `a34_MUTATE_M3.out`; the
corresponding JSON is `a34_results_M1.json` etc. (the clean run writes `a34_results.json`).

## M1 — codimension-2 coefficient halved

`k1()` divides the extracted coefficient by 2, i.e. it pretends the 2-D Gauss law gives
`g = G_D λ / r` instead of `2 G_D λ / r` (the classic 4π-vs-2π slip).

    K1    FAIL g = (1) G_D lam / r ; flux = 4 pi G_D lam     exponent exactly -1, coefficient exactly 2
    A34 COMPLETE: 12/13 checks PASS.

Why it bites: the coefficient is the whole question in task 1. The check does not test "is the
exponent 1" alone; it tests the exact pair (exponent, coefficient), so a factor-2 bookkeeping
error — the single most likely error in this derivation — fails.

## M2 — tautology broken by 2 %

`k5()` adds 1/50 to the residual `κ_def − 1/n`.

    K5    FAIL a0 - cH/Z = 0 ; kappa_def - 1/n = 1/50        both residuals exactly 0
    A34 COMPLETE: 12/13 checks PASS.

Why it bites: K5 is the check that makes "κ = 1/n" a *definition*. If the identity were only
approximate, the tautology verdict would be wrong and the chain would have content. The mutation
shows the check is an exact symbolic identity test, not a numerical near-identity.

## M3 — deep-MOND slope changed from (D−2)/2 to (D−2)

`k8()` replaces the exponent `−(D−2)/2` by `−(D−2)` (and the corresponding v² exponent), i.e. it
uses the Newtonian exponent as if it were the deep-MOND exponent.

    K8    FAIL g ~ r^-(D-2)/2 ; v^2 ~ r^((4-D)/2); flat at D=[4]    flat iff D=4
    A34 COMPLETE: 12/13 checks PASS.

Why it bites: with the wrong exponent, v² ∝ r^{3−D} and flat rotation curves move to D = 3. The
check asserts flatness **iff D = 4** exactly, so any bookkeeping slip in the exponent moves the
selected dimension and fails. This is the check that carries the "flat rotation curves are a D=4
statement" result, and it is the one that would break first if the D-generalisation of the law were
wrong.

## What is *not* mutated

The look-elsewhere count (K11) is deliberately not mutated: it is a counting statement about a
declared pool, and changing the pool is a different analysis, not a bug. Its threshold is the
weakest in the lane (`>= 8 at D=4 and > 0 at D=5`), and that is stated in the report.
