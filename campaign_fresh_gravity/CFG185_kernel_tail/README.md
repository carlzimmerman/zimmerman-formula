# CFG185 — the high-g tails of ν_mono and P2 against the Solar System, reconciled with GATES 4.01

- **Criteria:** frozen in `FROZEN_CRITERIA.md` (572c4aefc), before any script.
- **Script:** `cfg185_kernel_tail.py`, about 1 s.
- **Runs:**
  - The main run passes 8 of 8 checks and exits 0.
  - MUTATE=1 removes FP1's floor, leaving the pure RAR kernel. C1, Q1a and Q1c then fail, and it exits 1. The control bites, as required.
  - The first run had two check-implementation errors, disclosed below and kept as `*_firstrun*`.

## Bottom line

**The relayed spin-off holds. As bare laws, neither kernel is Solar-System safe, and ν_mono's tail is worse than P2's: it never decays, and it grows logarithmically with g.**

- **ν_mono.**
  - FP1 builds ν_mono by flooring the RAR phantom's derivative at 0.05 H_P/(y + Y_P). Above the RAR peak (Y_P = 2.5396), that floor is the whole integrand.
  - So exactly: h(y) = h(Y_P) + 0.05 H_P ln((y + Y_P)/(2Y_P)). The table matches this analytic form to 8.5 × 10⁻⁹.
  - h never falls below H_P = 0.648 in the high-g regime, and reaches 1.640 where the table clamps (y = 10¹⁴).
  - Values of the anomalous acceleration h a₀ from the Sun, canonical footing:

    | place | h | h a₀ (m s⁻²) |
    |---|---|---|
    | Neptune | 0.957 | 9.0 × 10⁻¹¹ |
    | Earth | 1.177 | 1.10 × 10⁻¹⁰ |
    | Mercury | 1.239 | 1.16 × 10⁻¹⁰ |
    | the photosphere | 1.525 | 1.43 × 10⁻¹⁰ |

- **P2.** h → ½ − 1/(8y): the constant a₀/2 tail, 4.68 × 10⁻¹¹ m s⁻² (canonical).
- **The RAR kernel** decays exponentially: h = y/(e^√y − 1).
- **Against the record's verified planetary bounds** (δA_R ≤ 3.66 × 10⁻¹⁴ m s⁻² at Earth and 3.72 × 10⁻¹⁴ at Mars, 2σ; Sereno & Jetzer 2006 via EPM2004, in STANDING.md):

  | kernel | canonical, Earth | canonical, Mars | alt, Earth | alt, Mars |
  |---|---|---|---|---|
  | ν_mono | 3011× | 2894× | 3620× | 3479× |
  | P2 | 1279× | 1258× | 1545× | 1520× |

  - The relayed ranges (2.9–3.6 × 10³ and 1257–1540) are confirmed.
  - At Earth, ν_mono's anomaly is 2.35 times P2's.

## Reconciliation with GATES 4.01 (Q3)

- **The ratios above are the monopole.** In the strict (bare) law, the Sun carries its own phantom, which gives a sunward anomalous acceleration: constant for P2, slowly growing for ν_mono. It is measured against the planetary radial-acceleration bound δA_R from ranging.
- **GATES 4.01's "strict law would be 4.0–5.7× the ceiling" is a different quantity.** It is Q₂, the tidal quadrupole (s⁻²) of the Solar-System field in the Galaxy's external field, against Q₂ ≤ 5.2 × 10⁻²⁷ s⁻². Both numbers describe the same strict law, and both hold together; neither contradicts the other.
- **Candidate B passes 4.01 by ownership.** The phantom belongs to the host, and the Sun carries none. The host-phantom tide is 1.6–2.6 × 10⁻³¹ s⁻² (GATES 4.01). Under ownership the Sun carries no monopole either, so neither bare-law number applies to B, and no verdict changes.
- **What is wrong is any statement that ν_mono (or P2) is Solar-System safe as a bare law.**

## Q4 — the record

- A grep of the record's documents (565 files: root, campaign_fresh_gravity and its closure_map and lane READMEs, real_research and its reviews) finds one line matching "P2/ν_mono … Solar System safe": CFG121's README, line 7.
- On reading, it is a false positive. The safety that line mentions is door 3's, through its medium-density cap, not a claim about a bare kernel.
- No statement in scope says either kernel is Solar-System safe as a bare law.

## Disclosed departures

1. **The first run's C1 compared y(ν − 1)** computed from CFG4_common's ν_mono. At y ~ 10¹⁴, where ν − 1 ~ 10⁻¹⁴, float cancellation costs about 1% in h, so the check failed on precision (max 1.0 × 10⁻²), not on the kernel.
   - The fixed C1 compares CFG4_common's own h table (the exec'd FP1 namespace). Max difference 0, as h and as ν.
2. **The first run's C2 expanded to O(1/y²)** and compared the result with the O(1/y) form, so it failed on its own truncation. The expansion was (8y² − 2y + 1)/(16y²) = ½ − 1/(8y) + 1/(16y²). The fixed C2 truncates at O(1/y).
3. **Q4's scope was restricted to the record's documents** after a repo-wide glob over about 35,000 .md files did not finish. No Q4 output had been seen before the change.
- Neither control fix changes a number in Q1–Q3. Both are check implementations brought into line with the frozen text.

κ = ½ and Ω_c h² stay fitted. Nothing here changes candidate B's verdicts; it concerns bare kernels.
