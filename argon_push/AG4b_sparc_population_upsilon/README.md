# AG4b: n=1 vs n=2 on SPARC with stellar-population Υ. canonical NOT SIGNIFICANT, alt LEAN n=2; n=2 survives

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (bbc2403d8).
- **Run:** `OMP_NUM_THREADS=1 nice -n 10 python3 ag4b.py`: 8 s, 0.4 GB, exit 0. Outputs `ag4b.out`, `ag4b_results.json`.
  `AG4B_MUTATE=1` exits 1 (bites) and writes `_MUTATE` outputs.
- **When:** run 2026-10-20 12:50, after CFG654 NC2x was aborted by its swap guard at 12:44. No 1024³ job was live.
- **Settings:** κ = ½ fitted; footings never pooled; not theory closed.

| footing | primary: median paired rms d (n2 − n1) | z | power (n=1 / n=2 mocks recovered) | reading |
|---|---|---|---|---|
| canonical (9.3603e-11) | −0.0001 ± 0.0004 dex | +0.24 | 80% / 90%: DIAGNOSTIC | **NOT SIGNIFICANT** |
| alt (1.1312e-10) | −0.0014 ± 0.0005 dex | +2.52 | 80% / 90%: DIAGNOSTIC | **LEAN n=2** |

**n=2 survives AG4b:** z > −2 on both footings, which opens the AG4d gate.

## What it means
- AG3's n=2 preference at the canonical a₀ (−0.042 dex with Υ fixed) disappears once each galaxy's Υ is fitted under a
  stellar-population prior: z = +0.24.
- **S3, the law form and a₀ are degenerate (diagnostic, not graded).** With a₀ free:
  - n=1 wants a₀ = 9.33e-11, i.e. κ = 0.499 on the canonical footing.
  - n=2 wants a₀ = 1.148e-10, within one 0.01-dex grid step of the alt footing's 1.1312e-10.
  - So on SPARC, n=1 at the canonical a₀ and n=2 at the alt a₀ are the near-equivalent pairs. The alt footing's LEAN n=2
    reflects n=2 sitting near its own best a₀ there, while n=1 does not.
- **The secondary statistic disagrees on the canonical footing.** Σ Δχ²_min (n2 − n1) = +711, z −2.57, favouring n=1.
  This is reported, not graded; the pre-registered primary stands.
- **S2, MAP Υ:** the median is 0.506 (n=1) vs 0.601 (n=2) on the canonical footing, so n=2 needs heavier discs. About 22–25% of
  galaxies sit ≥ 3σ from the prior centre under either law.

## Controls
- **K1:** CFG695's n=1 global-Υ scan is reproduced (0.10091 @ 0.60 / 0.09943 @ 0.55). On the same global scan n=2 gives
  0.10827 @ 0.70 / 0.10355 @ 0.65 (reported).
- **K2, K3:** PASS.
- **Variants:** none changes the canonical reading. On the alt footing, V2 (distance and inclination term) and V3 (Q ≤ 2) drop it
  to NOT SIGNIFICANT, at z +1.77 and +1.72.
- **MUTATE:** an n=1-truth mock as the data reads FLIPS on both footings (z −2.19 / −2.28): it bites. The power rule sits
  exactly at its 80% line for the n=1 mocks; that is disclosed.
