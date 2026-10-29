# X66_core_gated_quarter_a0

**Question (the owner, 10-29).** After X65, the external model proposed a boost confined to the core. Gravity on the cold
sector is multiplied by max(1, (a₀/4)/g_σ) only where streams have crossed (Q > 0) and gravity still rises with radius
(dg_N/dr > 0). Here g_σ = √((π/3) G ρ σ_tot²). The owner said "run X66". Criteria were frozen first (8ff6656a33).

**By construction:** a₀/4 encodes R = 1 for an isotropic Burkert core (½ sphere-vs-slab × 0.509 Burkert geometry). A
pass would not have derived a₀/(2πG). It did not pass.

## Verdict: FAIL

| Failing condition | Detail |
|---|---|
| canonical floor | NO EFFECT |
| alt floor | LOWERS |
| max() | BROKEN on both footings |
| j-robustness | j-DEPENDENT |
| resolution | UNRESOLVED |
| threshold | THRESHOLD-INSENSITIVE |

R ≡ ρ₀r₀ / (a₀/2πG), j = 0.1, N = 2000.

| M (M☉) | R_N | R_G canonical | R_G alt | MUTATE (a₀/2) |
|---|---|---|---|---|
| 1e9  | 0.21 | 0.15 | 0.08 | 0.07 |
| 1e10 | 0.46 | 0.43 | 0.34 | 0.07 |
| 1e11 | 1.15 | 0.76 | 0.67 | 0.88 |
| 1e12 | 2.24 | 2.65 | 1.98 | 1.72 |
| 1e13 | 4.77 | 4.76 | 4.17 | 6.44 |
| 1e14 | 6.98 | 11.5 | 8.39 | 10.3 |

**What happened:**
- The boost barely engages. At the end of each run at most 3 % of the mass is boosted, and in most runs none is.
- Where it does engage, it acts impulsively during formation. The cap of 100 is hit at 1e9 in every footing and j, which
  heats the core and leaves it LESS dense. The median change over the below-floor set is −0.08 dex (canonical) and −0.19 dex
  (alt), with spread 0.45 / 0.63 dex.
- A stronger threshold (a₀/2) lowers R further (−0.56 dex), the opposite of a floor.
- The high masses move with no late-time boost: 1e14 goes from 7.0 to 11.5. The velocity-dependent, switched force acts
  transiently during collapse and changes the halos chaotically (|ΔE/E| up to 0.9 in G runs).
- j cases: R_G at 1e9 is 0.23 / 0.15 / 0.03 for j = 0.05 / 0.1 / 0.2. Resolution at 1e9 moves by −0.44 dex. This low-mass
  behaviour is not converged.

**Reading.** X65 and X66 bracket the problem:
- an extra pull acting over the whole halo (X65) raises every core and breaks max();
- a switched pull confined to the core (X66) heats cores instead of compressing them.

Neither makes a floor. Both mutations point the same way: switched, non-conservative boosts heat. A candidate must be a
conservative force from an action, not a threshold switch.

## Standing and process note

- κ = ½ FITTED; not theory closed. Spherical symmetry; the cosmic web, Bullet Cluster and baryons are out of scope.
- **Process note:** the first full run finished all 36 runs, then crashed while writing the verdict (a numpy bool in
  `j_cases`). The bool was fixed and the rows were recovered unchanged from the partial JSON (`x66_rows_recovered.json`).
  Grading ran on them with `X66_REGRADE=1` (`x66_regrade.out`). No run was repeated or altered.

## Files and reproduction

Files: `FROZEN_CRITERIA.md`, `x66_core_gate.py`, `x66_core_gate.out`, `x66_rows_recovered.json`, `x66_regrade.out`,
`x66_results.json`, `x66_core_gate_MUTATE.out` / `x66_results_MUTATE.json`.

    X66_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x66_core_gate.py
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x66_core_gate.py      # about 1 h
    X66_REGRADE=1 PYTHONHASHSEED=0 python3 x66_core_gate.py                      # regrade from recovered rows
