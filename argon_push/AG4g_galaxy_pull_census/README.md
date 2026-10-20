# AG4g: per-galaxy pull census. Stage 1 EXCESS (real); stage 2 VOID as frozen; A1 (post hoc): no lead, and the strongest departures look like data systematics

- **Criteria:** `FROZEN_CRITERIA.md` (3b46d4b8b). **Addendum A1, post hoc:** `ADDENDUM_A1_POST_HOC.md` (f765c605d), committed
  alone before any A1 number.
- **Runs:** all three ran beside the live NC2x job, under the owner's 10-20 small-job rule.
  - `ag4g.py`: 10 s, 0.20 GB, exit 1 because K3 failed.
  - MUTATE: exit 1, it bites.
  - `ag4g_a1.py`: 3 s, 0.13 GB, exit 0.
- **Settings:** κ = ½ fitted; not theory closed.

## Stage 1: more galaxies need a non-stellar-population Υ than the stated errors allow. **EXCESS** (frozen, graded)
| fit | large pulls (\|p\| ≥ 3) | law-true mocks (200) | reading |
|---|---|---|---|
| n=1, canonical (primary) | 13 of 170 (7.6%): 7 high, 6 low | mean 0.0, max 1 | **EXCESS** (p < 0.005) |
| n=1, alt | 14 | mean 0.0, max 1 | EXCESS |
| n=2, alt | 14 | mean 0.1, max 1 | EXCESS |

- The fit includes each galaxy's coherent distance and inclination error (median 0.11 dex). Without it, 39 galaxies (22.9%)
  sit at ≥ 3σ, which reproduces AG4b.
- The largest pulls:
  - UGC06787 and UGC03580: −5.0, at the grid floor, i.e. Υ ≈ 0.16. Both are T = 1–2 early spirals with bulges. UGC06787 is
    already on the record's disturbance list (AG3b).
  - UGC00731 (+4.9), UGC08286, IC2574, UGC08837, NGC5985, UGC00128, NGC1705, NGC0024, NGC4217, CamB, UGC12506.
- K1 (reproduces AG4b's fraction, 39 of 170) and K2 (mock mean pull −0.001) PASS.

## Stage 2: what predicts the pulls?
- **Frozen permutation scan: VOID.**
  - It flagged Q (signed, ρ −0.28) and Inc (signed, ρ −0.23).
  - **K3 FAILED:** 46 of 50 law-true mocks also produced a Holm lead. The pulls are not exchangeable across galaxies when
    the law is true, because the estimator's bias depends on each galaxy's errors and acceleration regime.
  - MUTATE did bite: an injected Hubble-type dependence was flagged (ρ +0.61).
- **A1, mock-calibrated null (post hoc): no A1 lead.**
  - The minimum Holm p is 0.109. 200 mocks cannot go below Holm 22 × 1/201, a resolution floor declared in A1 beforehand.
  - K3-A1 PASS: 0 of 50 fresh mocks gave a false lead.
- **Eight tests sit outside ≥ 99% of the law-true mocks (p_emp ≤ 0.01). Reported, not graded:**
  - **Signed pull vs data quality and geometry:** Q (data −0.28 vs mocks +0.01), Inc (−0.23 vs +0.01), Hubble-flow distance
    (+0.19 vs −0.02).
  - **|pull| vs galaxy brightness and structure:** in law-true mocks, |pull| grows with L[3.6], SBdisk and V_flat (+0.25),
    and falls with gas fraction and T (−0.23 / −0.27). In the data it is flat for all of them (+0.02 to +0.06).

## Reading
- The excess of strongly pulled galaxies is real.
- Its pattern points to measurement systematics, not to a property the law misses:
  - galaxies with lower quality flags and higher inclination pull low;
  - Hubble-flow distances pull high;
  - the pulls do not follow galaxy type, gas fraction or surface brightness the way a law-true universe would.
- Plausible causes: non-circular motions or warps (Q), inclination errors beyond the quoted ones, and Hubble-flow distance
  errors. The bulge-dominated early spirals at the Υ floor point to bulge–disc decomposition.
- **No crisp physics lead.**
- If wanted, a dedicated check of the 13 pulled galaxies against independent distances (TRGB or Cepheid) and kinematic
  inclinations would decide between the systematic causes. That is a new lane; it is not run here.
