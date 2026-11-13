# KAP1: commit ids and the lead's re-run (dated addition, 2026-11-12)

No number, word or line of the lane changes. RESULT.md stays as the lane wrote it.

## Commit ids (local / origin)

| Commit | Local | Origin |
|---|---|---|
| FROZEN_CRITERIA (alone) | 3116ad793b | 05df560c55 |
| Attempts (script, outputs, twin) | 681cfa10b7 | 6af0fb2222 |
| RESULT | a6025e7958 | a82529b31c |

## Re-run by the lead

`kap1.py` from a copy, one thread, then `KAP1_MUTATE=1`. `kap1.json`, `kap1.out`, `kap1_MUTATE.json` and
`kap1_MUTATE.out` equal the committed files byte for byte. The main run exits 0; the twin exits 1. Word reproduces:
KAPPA NOT DERIVED.

Checked by hand: lemma L1's dimension count. With G (L^3 M^-1 T^-2), rho (M L^-3), M_b (M) and a0 (L T^-2), the only
dimensionless product is a0 / (G rho^(2/3) M_b^(1/3)). So a condition built from those four alone either holds for
every a0 or makes a0 depend on mass; a universal a0 = kappa c sqrt(G rho) needs c from somewhere else.

A reproduction of the arithmetic, not an independent re-derivation. The lane ran for about eight minutes and tried
three routes; it closes the routes built on this week's new inputs and does not exhaust relativistic ones.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
