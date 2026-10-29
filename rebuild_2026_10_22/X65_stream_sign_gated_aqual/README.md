# X65_stream_sign_gated_aqual

**Question (the owner, 10-29).** An external model proposed AQUAL acting on the cold dark energy only, switched on by a
stream-sign order parameter Q (Q = 0 until shells cross). It claimed this enforces the core floor ρ₀r₀ = a₀/(2πG). We ran a
1D spherical-shell collapse and measured the core surface density against a₀/(2πG).
Criteria were frozen before any script (3c0c5e0231).

## Verdict: RAISES, NO FLOOR on both footings; max() BROKEN on both; j-DEPENDENT

R ≡ ρ₀r₀ / (a₀/2πG), from a Burkert fit to the 10–12 Gyr averaged profile. The N column is the Newtonian run; G is gated.

| M (M☉) | R_N canonical | R_G canonical | R_G alt | MUTATE (Q ≡ 1) |
|---|---|---|---|---|
| 1e9  | 0.21 | 0.99 | 0.85 | 0.14 |
| 1e10 | 0.46 | 2.00 | 1.73 | 0.27 |
| 1e11 | 1.15 | 3.86 | 3.27 | 0.53 |
| 1e12 | 2.24 | 6.95 | 6.14 | 1.36 |
| 1e13 | 4.77 | 12.9 | 10.3 | 2.64 |
| 1e14 | 6.98 | 20.2 | 19.9 | 6.10 |

**Below-floor set S = {1e9, 1e10}.** The median lift is 0.66 / 0.68 dex (canonical / alt). R_G spreads by 0.30 dex across S,
so FLOOR fails. R_G rises smoothly with mass and has no plateau at 1.

**Above-floor masses** are raised about ×3 as well, so max() is BROKEN.

**Why:** Q > 0.5 covers 94–100 % of the mass, out to 18–120 r₀. Q marks "inside splashback", not "inside the core". The
extra pull acts wherever g < a₀, which includes every halo's outskirts.

**j-DEPENDENT.** At 1e10, R_G is 2.83 / 2.00 / 1.36 for j = 0.05 / 0.1 / 0.2. In this harness the Newtonian core itself
depends on j (R_N 0.98 / 0.46 / 0.28). Core surface densities from 1D shells are partly set by the angular-momentum barrier.

**Resolution OK:** N = 1000 differs from N = 2000 by 0.04 dex (1e10) and 0.01 dex (1e11). **Pre-checks pass:** Newtonian
|ΔE/E| ≤ 0.2 %, and Q = 0 exactly on a single-valued map.

**Mutation (Q ≡ 1 from t = 0):** cores come out LOWER than Newtonian at low mass. Turning the gate on early deepens the
infall potential and heats the core. The harness responds to the gate (not insensitive).

## What this does and does not say

- It tests the gated pull as proposed. The proposal's −(φ − Φ_N)∇Q term was dropped (ill-defined with a discrete Q; stated
  in the criteria).
- Spherical symmetry cannot test the cosmic web or the Bullet Cluster.
- The external model's floor argument assumed a slab: "the pull at r₀ = 2πGρ₀r₀". A Burkert sphere's peak pull is
  0.2545 × 2πGρ₀r₀, so the floor is equivalent to "peak self-pull ≈ a₀/4".
- κ = ½ FITTED; not theory closed.

Follow-up: X66 tests the external model's second proposal (a boost gated to the core, with threshold a₀/4).

## Files and reproduction

Files: `FROZEN_CRITERIA.md`, `x65_shells.py`, `x65_shells.out` / `x65_results.json`, `x65_shells_MUTATE.out` /
`x65_results_MUTATE.json`.

    X65_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x65_shells.py
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x65_shells.py     # about 30 min, exit 0
