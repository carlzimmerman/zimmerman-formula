# CFG871 — is the dwarf cold core's size set by its dispersion through the law, r_c ≈ (9/2) σ²/a0?

Criteria: `FROZEN_CRITERIA.md` (9418bfeea, before the script). Run: `python3 cfg871.py` (MUTATE `CFG871_MUTATE=1`). Seconds.

## Result — CLASS: **LAW-LINKED CORE CONSISTENT** (inside the 1σ range on both footings; the upper bound on r_c is weak)
Hypothesis H-LINK: the extra cold component is a self-gravitating isothermal clump whose own gravity obeys the law in the deep regime,
σ⁴ = (4/81) G M a0 and r_c ≈ r_M = √(G M/a0) → **r_c,pred = (9/2) σ²/a0**.
| | canonical | alt |
|---|---|---|
| r_c from the 7 binary-corrected UFDs (V_x refit consistently) | best 133 pc; 1σ 76–383; 2σ 51–3000 | best 139 pc; 1σ 76–650; 2σ 50–3000 |
| σ at best r_c | 7.95 km/s | 8.04 km/s |
| **r_c,pred = (9/2) σ²/a0** | **98 pc (ratio 0.74) — inside 1σ** | **83 pc (0.60) — inside 1σ** |
| implied clump mass M = 81σ⁴/(4Ga0) | 6.5e6 M_⊙ | 5.6e6 M_⊙ |
| mean density inside r_c | 0.66 M_⊙/pc³ | 0.50 M_⊙/pc³ |
- K1: at r_c = 104 pc the V_x inversion gives 10.65 km/s = CFG870. MUTATE (coefficient 1, Newtonian-like r_c = σ²/a0 ≈ 20 pc): OUTSIDE the
  2σ range on both footings — the UFDs' lower bound on the core excludes it, so the law's coefficient 9/2 matters.
- **Reading:** if the dwarfs' extra cold component is a clump whose own gravity follows the galaxy law, its velocity scale (σ ≈ 8 km/s) and its
  core (~90–100 pc) are not independent: one number, the clump mass ~6e6 M_⊙, sets both through a0. The two fitted numbers of CFG870 reduce to
  one, consistent with the data. **Limits:** the UFDs bound r_c from below (≳ 50–75 pc) but barely from above, so this is consistency, not a
  sharp confirmation; why the clump mass is ~6e6 M_⊙ in every faint dwarf, and why it is absent in rotating dwarfs' dynamics (it is only
  hidden there), remain open. The clump's own law-boost is an assumption of H-LINK (in the record the law is sourced by baryons; whether
  cold energy self-boosts is not settled).

κ = ½ fitted; cold energy mass required; not theory closed.
