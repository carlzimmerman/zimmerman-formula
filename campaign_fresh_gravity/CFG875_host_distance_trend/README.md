# CFG875 — does the dwarf excess fade with distance from the host at fixed g_bar?

Criteria: `FROZEN_CRITERIA.md` (bdc023e85, committed alone before the script; owner block 870–879; owner asked for the test).
Run: `python3 cfg875.py` (`CFG875_MUTATE=inject|shuffle` → separate outputs). Seconds, numpy only. κ = ½ fitted; ν_e; footings never pooled.
**Post-hoc motivation (disclosed in the criteria):** suggested by a CFG874 variant and run on the same dwarfs, so weaker than a test on new objects.

## Result — CLASS: **UNDECIDED** (both footings)
66 dwarfs (55 satellites with and without HI, 11 isolated; host distance 19–1350 kpc) in CFG874's g_bar window, with CFG874's
estimators (Υ_V = 2, gas counted). Fit Δ = a + b log g_bar + k log d_host.

| variant (canonical) | N | k (dex per dex of host distance) | partial ρ | class |
|---|---|---|---|---|
| **primary** | 66 | **−0.190 ± 0.150** (−1.3 se) | −0.16 | **UNDECIDED** |
| **M_V ≤ −6 (drops faint ultra-faints)** | 47 | **+0.004 ± 0.131** | −0.04 | UNDECIDED |
| satellites only (< 300 kpc) | 55 | −0.230 ± 0.236 | −0.17 | NOT DIAGNOSTIC |
| MW satellites + isolated | 40 | −0.195 ± 0.163 | −0.17 | UNDECIDED |
| M31 satellites + isolated | 37 | −0.039 ± 0.208 | −0.05 | NOT DIAGNOSTIC |
| Υ_SFH / no gas | 67 / 66 | −0.175 / −0.174 | −0.16 / −0.15 | UNDECIDED |
| full g_bar range | 83 | −0.258 ± 0.129 (−2.0 se) | −0.18 | WEAK TREND |
| step at 300 kpc | 66 | −0.097 ± 0.092 | +0.07 | UNDECIDED |

Alternative footing: identical k (the a0 change shifts Δ almost uniformly) → UNDECIDED.

**Reading.** The environmental reading predicts k ≈ −0.4; a universal small-system component predicts k = 0. The primary
k = −0.19 ± 0.15 sits between them, 1.3σ from each. The apparent trend comes from the faintest dwarfs:
- With M_V ≤ −6, k = 0.00 ± 0.13.
- With the full g_bar range, which adds the lowest-g ultra-faints, k = −0.26 ± 0.13.

Those ultra-faints are all MW satellites at 20–100 kpc and the most exposed to binary-inflated σ. Among brighter dwarfs, host
distance shows no sign of mattering. The M31 system, with larger distance errors, shows no trend either (−0.04 ± 0.21).

## Controls
- **K1 PASS:** the 11 isolated Δ equal CFG874's primary values exactly (max |ΔΔ| = 0).
- **MUTATE-inject** (−0.4 dex per dex added): k −0.590 ± 0.150 (−3.9 se) → ENVIRONMENTAL, as required.
- **MUTATE-shuffle** (host distances permuted): k +0.085 ± 0.123 → NO TREND, as required.

## Disclosed limits
Present-day distance is not orbital history. Binary inflation of the faintest satellites is untreated except via the M_V cut,
and that cut is a variant (not graded) whose importance was seen in this run. Stellar rotation is untreated. M31 distances are
less certain.
