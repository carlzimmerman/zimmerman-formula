# X67_tidal_screened_aqual

**Question (the owner, 10-29).** The external model's fourth proposal was X65's gated AQUAL pull with the μ argument
screened by C² = (ρ̄(<r)/ρ(r))², with a_crit = a₀/2. The owner said "run X67". Criteria were frozen first (e808cbbaaa),
together with an advance pre-flight: on a Burkert halo the screening reopens beyond about 20 r₀.

## Verdict: FAIL

| Failing condition | Detail |
|---|---|
| floor | RAISES, NO FLOOR on both footings |
| max() | BROKEN on both footings |
| j-robustness | j-DEPENDENT |
| threshold | THRESHOLD-INSENSITIVE |

Resolution is OK: 0.01 / −0.08 dex.

R ≡ ρ₀r₀ / (a₀/2πG), j = 0.1, N = 2000.

| M (M☉) | R_N | R_G canonical | R_G alt | MUTATE (a_crit = a₀) | boosted mass (canonical) | boost zone (r₀) |
|---|---|---|---|---|---|---|
| 1e9  | 0.21 | 0.46 | 0.41 | 0.47 | 92 % | 0.2–51 |
| 1e10 | 0.46 | 0.85 | 0.81 | 1.11 | 61 % | 0.2–105 |
| 1e11 | 1.15 | 1.74 | 1.26 | 1.83 | 21 % | 9–99 |
| 1e12 | 2.24 | 3.08 | 2.29 | 3.61 | 0 % | — |
| 1e13 | 4.77 | 4.28 | 3.69 | 5.04 | 0 % | — |
| 1e14 | 6.98 | 10.8 | 9.62 | 10.3 | 1 % | 95–108 |

**What happened:**
- The screening is gentler than in X65: lifts of 0.30 / 0.35 dex over the below-floor set, against 0.66 in X65.
- **No floor:** R still rises smoothly with mass (spread 0.27 / 0.30 dex across S).
- **Where it acts:** as pre-flighted, the boost acts over most of the halo out to 50–100 r₀ in low-mass halos, not only in
  the core.
- **max() BROKEN:** halos above the floor still move by 0.1–0.2 dex (1e12: 2.24 → 3.08; 1e14: 6.98 → 10.8). Some of that
  comes from transient boosting during collapse, since the final-state boosted mass is about 0.
- **j-DEPENDENT:** at 1e10, R_G is 1.23 / 0.85 / 0.50 for j = 0.05 / 0.1 / 0.2.
- **THRESHOLD-INSENSITIVE:** doubling a_crit lifts R by only 0.07 dex, so the outcome is not set by the a₀ term.

**Reading.** X65–X67 test three screenings of a gated extra pull on the cold sector: none, a core switch, and tidal C².
None produces a plateau at a₀/(2πG):
- unscreened, it raises every halo;
- switched, it heats cores;
- tidally screened, it gives a softer version of X65.

In this harness the final ρ₀r₀ tracks the Newtonian value and j smoothly. Nothing here pins it.

## Standing

- κ = ½ FITTED; not theory closed.
- The C⁴ action/field-equation mismatch was reduced to the field equation as written (see the criteria).
- Spherical symmetry; the cosmic web, Bullet Cluster and baryons are out of scope.

## Files and reproduction

Files: `FROZEN_CRITERIA.md`, `x67_tidal_screen.py`, `x67_tidal_screen.out` / `x67_results.json`,
`x67_tidal_screen_MUTATE.out` / `x67_results_MUTATE.json`.

    X67_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x67_tidal_screen.py
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x67_tidal_screen.py     # about 25 min, exit 0
