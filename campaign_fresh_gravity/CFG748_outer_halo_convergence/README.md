# CFG748: given time and mass, collisionless cold energy fills the halo onto the law out to ~20 r_M; slow beyond

**Label (frozen rules): C1 FAIL, C2 STALLED.** Both are driven by one point: the mass-starved start at 50 r_M. Two controls also
fail and are disclosed: K2 for the cold-infall run, and a MUTATE tooth that does not bite.

- **Criteria:** `FROZEN_CRITERIA.md` (3eedeacd4), committed alone first.
- **Script:** `python3 cfg748.py <state>` for state ∈ law | uniform | half | mutate (about 10 min each, single thread)
  → `cfg748_<state>.json`.
- **Settings:** CFG747 dynamics (critical tether cancels the cold energy's self-gravity; cubic push u²/a₀); R₀ = 200;
  t_end = 10000; N = 4000; radial shells. κ = ½ FITTED; the cold energy's mass is required; no particle species; not "theory
  closed".

## m(<r)/r by time window (law = 1)

| start | window | r = 2 | 5 | 10 | 20 | 50 |
|---|---|---|---|---|---|---|
| law (control) | all five | 0.998 | 0.998 | 0.998 | 1.000 | 1.000 |
| uniform (cold infall) | 1000–2000 | 0.873 | 0.794 | 0.707 | 0.594 | 0.513 |
| | 5000–6000 | 1.002 | 0.994 | 0.999 | 0.991 | 0.948 |
| | **9000–10000** | **0.999** | **1.001** | **0.998** | **0.996** | **0.945** |
| half (mass-starved) | 1000–2000 | 0.999 | 0.995 | 0.971 | 0.899 | 0.733 |
| | 5000–6000 | 1.000 | 1.001 | 1.000 | 0.971 | 0.782 |
| | **9000–10000** | **1.001** | **0.999** | **1.002** | **0.985** | **0.813** |

ΔE/E: law 4.9e-13; uniform **3.2e-3** (K2 bar 1e-3: FAIL); half 1.2e-4. Escaped mass: 2.09 (uniform), 0.15 (half).

## Verdicts as frozen
- **C1 FAIL.** The half start misses at 50 r_M (0.813). The uniform start passes every radius in the last window (0.945–1.001).
- **C2 STALLED.** For half at 50 r_M, the gap shrank 0.267 → 0.187, less than the required half. Every other outer gap in both
  runs closed by far more than half (for example, uniform at 20 r_M: 0.406 → 0.004).
- **K2 FAIL** for uniform (3.2e-3). The violent cold collapse onto the reflecting inner boundary at r = 0.5 costs leapfrog
  accuracy. The law and half runs conserve energy to 5e-13 / 1.2e-4.
- **MUTATE does not bite.** With no cold-energy force the shells oscillate through the centre rather than piling up: m(2)/2 =
  1.42 in the last window, against the 1.5 tooth. Its windows swing between 0.42 and 1.42 at r = 2, which shows the profile is
  not held without the force. The frozen tooth was a poor design; it is not changed here.

## Reading
1. **The CFG747 outer deficit was mainly time and mass.** A cold infall with the law's total mass fills the halo onto the law
   within 0.4% out to 20 r_M, and to within 6% at 50 r_M, by t ≈ 5000–10000.
2. **A mass-starved halo fills from the inside out.** It holds the law to 20 r_M, but at 50 r_M it is still at 0.81 and rising
   slowly, because mass must fall in from 50–200 r_M. The frozen reading of this is STALLED. The data look like slow filling,
   but this lane does not establish that.
3. **Prediction in the making.** The law should hold inside ~10–20 r_M in every system. Beyond that, a halo's cold energy
   approaches the law at a rate set by its supply and age, and a supply-limited system shows an outer **deficit**. That is the
   opposite sign to the C3 early-type excess, so C3 is not explained by this.
4. **Limits.** Radial orbits; point baryonic mass; cubic W; reflecting inner boundary; one N; K2 failure in one run. Angular
   momentum is next (CFG749).
