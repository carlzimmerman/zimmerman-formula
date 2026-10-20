# CFG876 — is the dwarfs' cold component universal? (large, cold dwarfs never used in CFG870)

Criteria: `FROZEN_CRITERIA.md` (21fab6d76, committed alone before the script; owner block 870–879). Run: `python3 cfg876.py`
(`CFG876_MUTATE=halve` → `cfg876_MUTATE_halve.out`). Seconds, numpy only. κ = ½ fitted; ν_e; footings never pooled.

## Result — CLASS: **BROKEN** (both footings)
CFG870's cored component (V_x 10.65 / 10.59 km/s, r_c 104 pc), read as a universal cold-energy temperature floor
(σ0 ≈ 7.5 km/s), applied with no refit to the 18 large dwarfs (r12 ≥ 312 pc) that CFG870 never used (Υ_V = 2, gas counted):

| canonical | N | E = ⟨ln σ_obs/σ_pred⟩ | individual failures (z ≤ −3 at Υ_V = 1) | class |
|---|---|---|---|---|
| **law + component (primary)** | 18 | **−0.201 ± 0.099** | **3**: Crater II −11.0, Antlia II −4.7, Cassiopeia III −3.7 | **BROKEN** |
| law alone | 18 | +0.241 ± 0.105 | 0 | (reported) |
| supply-capped component (≤ 53.6 M_b) | 18 | −0.185 ± 0.092 | 2: Crater II −4.9, Cassiopeia III −3.7 | (reported) |
| small out-of-sample dwarfs (r12 < 312 pc) | 15 | −0.008 ± 0.139 | 1 | (reported: holds) |

Alternative footing: E −0.217 ± 0.099, 4 failures (adds Andromeda XXV) → BROKEN.

**Reading.**
- **The universal floor is excluded.** An extended isothermal cold atmosphere at σ0 ≈ 7.5 km/s in every dwarf over-predicts
  the large, diffuse ones. Its mass grows ∝ r, so it sets a line-of-sight floor near 6.2 km/s, which Crater II (2.3 km/s) and
  Antlia II (6.0 km/s at r12 3.2 kpc) do not reach.
- **Compact dwarfs still fit.** The 15 out-of-sample dwarfs with r12 < 312 pc fit (E −0.01 ± 0.14).
- **On average, large dwarfs sit between the two models:** above the law alone (+0.24) and below law + component (−0.20).
- **The data want a compact component.** Its mass must stop growing within a few hundred pc, not continue as an extended
  atmosphere.
- **The record already holds that finite form:** CFG871's law-linked clump, M = 81σ⁴/(4Ga0) ≈ 6e6 M_⊙, which caps at r_t = G M/V_x²
  ≈ 200 pc. CFG872 found that this clump cannot supply the most extreme compact dwarfs (6/25). The two lanes squeeze the
  component from both sides.
- **Two failures are partly the law's own.** Crater II's law-alone prediction (3.9 km/s) already exceeds its observed 2.3 km/s,
  and Cassiopeia III's law-alone prediction (10.4) exceeds 8.4. The record's law has no external-field effect, and no tidal
  truncation is modelled. Both dwarfs are known to be tidally affected.

**For the cold-energy equations:** the bath dispersion σ_J² of CFG638 cannot be a universal floor σ0² that every bound region
relaxes to. The dwarf excess must be a finite, compact cold mass, not a thermal atmosphere.

## Controls
- **K1 PASS:** the predictor reproduces CFG870's T2 E exactly on both footings (|diff| ≤ 2e-17).
- **MUTATE-halve** (σ_obs × 0.5 on B): E −0.89 (−9 se), 10 failures → BROKEN. The control bites.

## Disclosed limits
Not blind to the literature fact that Crater II and Antlia II are cold. No EFE or tides modelled. Υ_V = 2 for all (no
SFH-based values). Faint M31 satellites carry large σ and distance errors. The MW-only subset is small (N = 3).
