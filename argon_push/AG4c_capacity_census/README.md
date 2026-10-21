# AG4c: tether-capacity census. NOT DIAGNOSTIC on both footings; n=2 survives

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (bbc2403d8).
- **Run:** `OMP_NUM_THREADS=1 nice -n 10 python3 ag4c.py`: seconds, exit 0. Outputs `ag4c.out`, `ag4c_results.json`.
  `AG4C_MUTATE=1` exits 1 (bites). Run 2026-10-20, with no 1024³ job live.
- **Settings:** κ = ½ fitted; footings never pooled; not theory closed.

| footing | SPARC points at g_bar ≥ 2a₀ | median σ(g_ph) | well-measured (σ ≤ 0.15 a₀) | reading |
|---|---|---|---|---|
| canonical | 519 in 42 galaxies | 2.06 a₀ (10th percentile 0.93) | 0 | **NOT DIAGNOSTIC** |
| alt | 453 in 38 galaxies | 1.92 a₀ (10th percentile 0.93) | 0 | **NOT DIAGNOSTIC** |

## What it means
- The cap separating the laws (n=2: g_ph < a₀/2; n=1: g_ph < a₀; 107/214 M☉/pc² on the canonical footing) only shows up where
  g_bar ≫ a₀.
- There, a 0.10 dex stellar mass-to-light uncertainty alone puts the error on g_ph at about 2a₀, more than ten times the
  0.15 a₀ needed. No in-repo dataset can see the cap.
- Data that could decide it, not pulled here: late-type strong lenses with kinematic mass-to-light ratios, or any tethered
  system whose baryonic mass at g_bar ≫ a₀ is known to ≲ 5% without stellar populations.

## Controls
- **K1:** the cap algebra; u(10⁶ a₀) = 0.999999 (n=1) and 0.500000 (n=2).
- **K2:** the Σ̄ caps, 213.76 / 106.88 M☉/pc² (canonical) and 258.3 / 129.2 (alt).
- **MUTATE:** g_obs = g_bar + 0.9 a₀ with errors ÷10 makes 164 / 158 points well-measured, and the run returns EXCLUDES n=2 on
  both footings: it bites.
- **Wording note:** frozen K1 says "to 1e-9". It is checked as a strict bound everywhere, plus the asymptote to 1e-5 at
  10⁶ a₀, where the true gap is a₀²/g_bar ≈ 1e-6.
