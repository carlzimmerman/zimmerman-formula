# VB1_vacuum_boundary: STOPPED BY THE MUTATE TWIN; the computed statistic reads MIXED. The larger sphere renormalises the whole halo (× 1.23 at every radius, M₂₀₀ +0.115 dex) and leaves its shape; on the keys G-OUT-M3 moves from +4.36 to +4.41. The outer shortfall is NOT a boundary artefact

Criteria: `FROZEN_CRITERIA.md` (dee3b10238), committed before any run. Runs: `run_vb1.sh` (queued behind ZN4 and the 1e12 ng 80 seeds; finished 2026-11-01 00:29). Grader `vb1_grade.py` → `vb1.out`, `vb1_results.json`, shape tables `vb1_shape_A.json`, `vb1_shape_B.json`. Post-result key read `vb1_keys.py` → `vb1_keys_A.out`, `vb1_keys_B.out` (+ `_results.json`). Argon's door D2 (`../ARGON_REPLY_2026-10-31_EVENING_SCORED.md`; its inner-mass prediction, received after the runs and before any measurement, `../ARGON_REPLY_2026-11-01_SEAL_AND_D2.md`). κ = ½ FITTED; footings never pooled; cold dark energy is a gravitating field component, never a particle; not theory closed. Nothing here says the data favour the framework.

## Runs
Same seed (1), mass 1e14, ng 48, same particle mass, softening and background; A has the initial sphere at RS 1.5 q_M (the standard zoom), B at 2.0 q_M (the IC grid's ceiling; Argon asked 2.25). Both collapsed with `x48_fast.py` and continued to z = 0 with `zn1_continue.py` unchanged.

| check | result |
|---|---|
| K1 run A's collapse equals X48's `M1e14_s1_ng48` | max \|dx\| 7.5e-9 Mpc, max \|d ln m(x)\| 7.5e-8: PASS |
| K2 particle mass equal | 6.907767e9 both: PASS |
| K3 softening equal | 7.6349e-3 Mpc both: PASS |
| K4 N_B/N_A against (2.0/1.5)³ | 2.3673 against 2.3704 (−0.13 %): PASS |

## Statistic (z = 0, run A's R500 = 0.5594 Mpc; band 2.18–3.17 R500 = 1.22–1.77 Mpc = 1.45–2.11 R200_A)

| | run A (RS 1.5) | run B (RS 2.0) | B/A |
|---|---|---|---|
| R200, lg M200 | 0.840 Mpc, 13.812 | 0.918 Mpc, 13.927 | +0.115 dex |
| ΔΣ in the band (three projections) | 1.233e13 M☉/Mpc² | 1.495e13 | **f_out 1.213 ± 0.012** (shot) |
| M(< 0.7 R500_A) | 3.43e13 | 4.22e13 | **f_in 1.230** |
| M(< 0.5, 1, 1.5, 2, 3, 4 R200_A) | | | 1.236, 1.229, 1.208, 1.178, 1.210, 1.230 |
| shape m(x) = M(< x R200)/M200 at x 0.2, 0.5, 1.45, 1.75, 2.11, 3 | | | 1.03, 1.04, 0.97, 0.96, 0.95, 0.96 |

Per-annulus f_out across the band: 1.23, 1.24, 1.22, 1.23, 1.23, 1.18, 1.16, 1.19.

**Gate as frozen:** f_out 1.21 lies between the FAIL line (1.15) and the PASS line (1.28), and f_in moved by 23 %, not ≤ 4 %: **MIXED**. **MUTATE (band at 1.5 × R500_A):** f_out 1.153, a change of −4.9 %, under the 10 % the criteria require: **DOES NOT BITE, the lane stops.** The statistic does not see its aperture because the ratio is the same at every radius: it measured a mass renormalisation, not an outskirts effect. That is the result, and it is reported as such rather than graded. Reading of the MUTATE line: the criteria say "run B measured with run A's R500 shifted by × 1.5"; here both runs' bands follow the shifted R500 (the statistic is a ratio at one physical aperture), which gives −4.9 % and stops. Shifting only run B's band against run A's unshifted one gives −43.5 % and would bite, but compares two different radii; the other session read it that way independently and agrees the verdict is MIXED either way. The stop is kept and the other reading named.

## What happened
The sphere at 2.0 q_M carries 2.37 × the particles. By z = 0 the halo is 23 % heavier at every radius from 0.5 to 4 R200_A, and its shape in units of its own R200 is unchanged outside x 0.2 (within 3–5 %, slightly lower in the band). The two collapses already differ at z_f (centre 0.73 Mpc apart; inner 0.2 r_f 1.7 × denser in B), so the larger sphere changed the collapse itself, not only the late infall; one seed, so the size of that change is not characterised. The keys use the shape at the fair-share M₂₀₀, so the renormalisation cannot reach them.

**Post-result key read (reported, not graded):** ZN3's grader with the 1e14 node replaced by run A's shape, then run B's (1e13 from ZN1, 1e15 from ZN3; one ng 48 seed in place of nine at ng 64, so A against B is the comparison).

| 1e14 node | X-COP's gas +0.111, f★ 0.034 / 0.0615 | measured gas +0.005 (GS4), G-OUT-M3 | class at +0.005 |
|---|---|---|---|
| run A (RS 1.5) | 15 of 15 both; G-OUT-M3 +1.46 / G-IN-Mall −1.31 | **+4.36 / +4.07** | X-COP ONLY |
| run B (RS 2.0) | 15 of 15 both; +1.49 / G-OUT-Mall +1.21 | **+4.41 / +4.12** | X-COP ONLY |

## Predictions on record
- Argon (at 2.25 q_M; VB1 runs 2.0, disclosed): f_out 1.18–1.24, later 1.16–1.26 → the number lands inside both ranges. ΔM(< 0.7 R500) +1.8 ± 1.2 % → **MISS** (+23 %). ΔM(< R200) +5.5 ± 2 % → **MISS** (+23 %). G-OUT-M3 from about +3.8 to about +2.4 → **MISS** (+4.36 to +4.41). The outer number is right for the wrong reason: Argon's mechanism was mass arriving in the 1.4–2.1 R₂₀₀ band from beyond 1.5 q_M with the inner halo held; what the run shows is the whole halo scaled, the band included, and the key's shape untouched. Since 2.0 < 2.25, a 2.25 run could only add more of the same.
- This session: f_out 1.05–1.15, f_in within 2 % → **MISS** on both; the premise (band fed mostly from inside 1.5 q_M) was wrong in the same way, the extra mass reaches every radius.

## What this closes
Argon's door D2, the vacuum boundary as the source of the × 1.4 outer shear shortfall. The boundary changes the halo's mass, not its shape; G-OUT-M3 on the measured gas scale stays at +4.4. ZN1's tail problem (budget 3.4 M₂₀₀ at r_ta against 2.2 held) is unchanged by this test. Nothing here says a larger sphere is the right zoom: the mass renormalisation at fixed Lagrangian peak is itself a statement that the isolated-sphere M₂₀₀ depends on RS, which ZN1's fair-share R₂₀₀ sidesteps by construction. Not pursued further without a new idea; no RS scan (the standing rule).

κ = ½ FITTED; c_f EXTERNAL where used; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.
