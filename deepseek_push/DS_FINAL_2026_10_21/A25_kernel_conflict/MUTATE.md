# A25 mutation — set the canonical kernel to the quadrature, and the decision must collapse

## What is mutated

`CANON = "Q" if MUTATE else "L"` — i.e. the run adopts the record's kernel (quadrature `√(1+1/y)`) as the theory's,
which is exactly the claim this lane denies. Nothing else changes: the four kernels, their integrals, the target
73.19, the SPARC data, the planetary caps and the KiDS RAR are all the same objects, computed by the same code.

    python3 a25_checks.py --mutate      # exit 1, 10/14 checks PASS

## Mutated output (captured stdout, check lines only)

```
  K1   PASS max symbolic residual = 0.00e+00 over 4 kernel identities
  K2   PASS c = (1, 0.5, 0.0, ln-div): 0.999999994, 0.499999997, 3.72e-40, 0.03238051 ; beta = (0.5, 0, 0.5, 0.5): 0.50001, 5.0e-05, 0.50001, 0.50001
  K3   PASS closed forms certified: max rel 3.2e-26 (quad), 8.4e-12 (compact); dI/dY = 0.999999953 (L), 0.499999994 (Q); I_R(inf) = 12.987878804534
  K4   PASS rational forms exact (max rel 6.9e-13); asymptotics at y_t=100: L 1.9e-04, Q 1.2e-05
  K5   FAIL y_t(73.19): L 48.7877, Q 94.0539, M 63.6856, R none (sup 12.987879); canonical(Q) 94.0539
  K6   PASS band reproduced: Q(73.19)=94.0539 vs 94 (0.06%); Q(32pi)=128.9154 vs 128.9 (0.01%); L over-predicts by 1.963x
  K7   PASS I_R = 12.98787880 (2pi^4/15), 12.99 to 0.016%; 5.6x = 5.6353
  K8   PASS 32pi=3Z^2 exact; 73.19/32pi=0.72803; BRIEF Omega_L=0.6838 -> 68.74 (=68.89); a0(73.19)=1.0963e-10
  K9   FAIL fixed footing: dchi2(Q-canon) = 0.0, 0.0 ; dchi2(R-canon) = -147.9, -76.0
  K10  FAIL profiled: dchi2(Q-canon) = +0.00 ; dchi2(R-canon) = -17.23 ; a0(Q) = 1.200e-10 vs a0(canon) = 1.200e-10
  K11  PASS turn-off signature: max 0.00428 dex (L), 0.00115 dex (Q); SPARC dchi2 <= 0.11
  K12  PASS c*a0/B_E = 2557.4 (L), 1278.7 (Q), 0 (R); one y_t inside the planetary cap for L (margin 12.4x)
  K13  PASS KiDS RAR: dchi2(Q-L) = -10.90 (no separation); chi2/dof(L) = 3.65
    canonical kernel in this run: Q (quadrature (P2))
  K14  FAIL canonical = Q, expected L (the action's kernel)
A25 COMPLETE: 10/14 checks PASS.
```

## Why each failure is the right one

| id | normal | mutated | why the check has teeth |
|---|---|---|---|
| K5 | `canonical(L) 48.7877` | `canonical(Q) 94.0539` | the closure root is a *kernel-dependent number*; adopting the record's kernel moves the required `y_t` by a factor 1.93, which is precisely the discrimination the lane claims |
| K9 | `Δχ²(Q−canon) = 158.0 / 75.3` | `0.0 / 0.0`; `Δχ²(R−canon) = −147.9 / −76.0` | with the quadrature as canonical, the *same* SPARC data now puts L (and R) far ahead of it: the data reject the mutated choice by the same 148–158 that they rejected Q in the normal run |
| K10 | `Δχ²(Q−canon) = +17.05` | `+0.00`; `Δχ²(R−canon) = −17.23` | the `(A, a₀)`-profiled test inverts the same way, so the failure is not an artifact of the fixed footing |
| K14 | `canonical = L` | `canonical = Q` | the provenance assertion itself — the only kernel with a derivation is the action's — is what the mutation denies |

Note that **K6 and K7 still pass** under the mutation: they are statements about the record (`94`, `128.9`, `12.99`,
`5.6`), not about which kernel is the theory's. That is the correct behaviour — the mutation must break the
*decision*, not the arithmetic that reproduces the record's numbers.

## Restoring

`python3 a25_checks.py` (no flag) rewrites `a25_results.json` with `"mutate": false` and 14/14 PASS, exit 0. The
committed `a25_results.json` and `a25.out` are the **normal** run; only this file records the mutated output.
