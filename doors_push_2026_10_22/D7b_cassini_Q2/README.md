# D7b_cassini_Q2 — Cassini Q₂ of the canonical law, with and without the P5 turn-off

## Verdict: CRISP FINDING — Q₂ cannot see y_t; the canonical law fails Q₂ at every y_t

- The turn-off changes Q₂ by **+0.06 % to +0.69 %**. It *raises* Q₂ slightly; it does not lower it.
- Across the whole band y_t ∈ [60, 140], Q₂ moves by at most **1.6e-28 s⁻² = 0.052 σ** of Hees 2014.
- So the band is **not cut**, and no κ range is selected (band [60,140] ↔ κ ∈ [0.3415, 0.5267], unchanged).
- The canonical law **FAILS** the Hees 2014 2σ line (9.0e-27 s⁻²) at **every** y_t, both footings, all four
  external fields: **1.70–3.70×** (canonical a₀), **1.91–4.03×** (alt a₀). It also fails Park 2026 (5.2e-27).
- This failure belongs to the law's shape near y ≈ 1 (r ≈ 7000 AU), not to P5. P5 acts at y > 60, i.e. inside
  ~1000 AU, where the anisotropic phantom density contributes almost nothing to Q₂.

Script: `d7b_cassini_q2.py`, under 2 s, single thread. **7/8 checks PASS; K4 FAILS as frozen** (see below), so
the script exits 1. The `--mutate` run (the record's /√D kernel bug) gives 3/8. Criteria were frozen first
(commit c6a0b6f3c7); one post-result amendment explains K4. Every number is in `d7b_cassini_q2_results.json`.

## Inputs

- Q₂ convention: BN11 / Hees, δU = ½Q₂(z² − r²/3), MOND prediction positive.
- Bounds (external, as transcribed in `prep_2026/planetary_doors/BOUNDS.md`, not re-read here):
  Hees et al. 2014 Q₂ = (3 ± 3)e-27 s⁻² (primary, 2σ = 9.0e-27); Park+2026 (1.6 ± 1.8)e-27 (2σ = 5.2e-27).
- External field at the Sun, four values:
  - E0 = A60's framework Milky Way: g_N,e = 6.913e-11 m/s² (total 1.22e-10 canonical, 1.29e-10 alt).
  - E1/E2/E3 = kinematic total g_e = 1.9 / 2.2 / 2.6 × 9.36e-11 m/s² (record band, branchB lane).
  E0 is the most favourable case for the framework. It still fails (1.70× / 1.91×).
- y_t from the closure I(y_t) = 8π/κ²: **66.3803** at κ = ½ (32π). The quoted-Λ root is 66.2999 (0.12 % lower;
  both reproduced, K7). Thermal κ = Z/4π gives 8π/κ² = 118.435 and **y_t = 77.876**.

## Q₂ (s⁻²), Route M, canonical footing (E0, E1, E2, E3)

| y_t | Q₂ | × Hees 2σ |
|---|---|---|
| none | 1.525e-26, 2.376e-26, 2.785e-26, 3.309e-26 | 1.69–3.68 |
| 60 | 1.528e-26, 2.386e-26, 2.801e-26, 3.332e-26 | 1.70–3.70 |
| 66.38 | 1.528e-26, 2.385e-26, 2.799e-26, 3.329e-26 | 1.70–3.70 |
| 77.876 | 1.527e-26, 2.383e-26, 2.796e-26, 3.325e-26 | 1.70–3.69 |
| 140 | 1.526e-26, 2.379e-26, 2.790e-26, 3.316e-26 | 1.70–3.68 |

The alt footing is 1.90–4.03× at every row (table in `d7b_cassini_q2.out`). Q₂ at Saturn equals Q₂ at the Sun to 7e-16.

## Checks

- K1: an exact analytic limit was derived for this lane. For ν−1 = 1/y (the canonical tail alone), the eq-12
  integral collapses through the Legendre generating function to **q = −(16/49)√e_N**. Route M reproduces it to 5e-10.
- K2: the independent grid route gets the same limit to 1.8e-6. Its closed-form phantom density matches a
  brute-force divergence to 7e-10.
- K3: the two routes agree to 1.1e-3 at all 40 (footing, y_t, E) points, with the same sign.
- K5: BN11's AQUAL μ₁ value of 3.8e-26 is matched by our QUMOND value of 2.80e-26 (ratio 0.737, inside the
  frozen [0.70, 1.05]).
- K6 (limits), K7 (closure roots) and K8 (convergence: 7e-14 and 4e-7) all pass.
- **K4 FAIL**: against Desmond+2024's simple-ν anchors (as recorded), our |q| comes out at 0.974, 0.965 and 0.965 of
  them. The frozen tolerance was 3 %.
  - Truncating at v = 60 moves q by only 1e-5, so the gap is **not** a tail effect.
  - It is an anchor convention or transcription difference.
  - If our q is low, the FAILs only get stronger.

## Error found in the record

`real_research/reviews/branchB_q2_gate_2026/decider_q2_crosscheck.py:5-7` attributes the 0.965–0.973
anchor ratio to the v-tail ("tail falls as eN/v") and multiplies all Q₂ by CAL ≈ 1.03.
- The integral to v = ∞ gives the same 0.965–0.974.
- Cutting it at v = 60 changes q by ≤ 1.5e-5.

The CAL factor is therefore not a tail correction. It is a ~3 % rescaling of unknown origin. It does not change
any verdict there.

## What this does not show

- It assumes a static, uniform external field and uses QUMOND only; AQUAL runs about 1/0.74 higher (K5), so it would fail harder.
- It does not refit the ephemerides with this law's full field.
- It makes no claim about other turn-off shapes. It shows only that any cure acting at y ≳ 60 cannot reach Q₂,
  because Q₂ is set at y ~ 1.
- It does not reconcile the Q₂ failure with the RAR. That is the known class conflict
  (Desmond–Hees–Famaey 2024, already on record).
