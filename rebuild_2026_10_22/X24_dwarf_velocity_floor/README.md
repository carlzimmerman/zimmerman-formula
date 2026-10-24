# X24_dwarf_velocity_floor: the hosted-dwarf "wall" is a mass trend, and one velocity floor removes most of it

Criteria: `FROZEN_CRITERIA.md` (7a79903c3f, committed alone; **POST-HOC**: the idea came from looking at the per-system
numbers, disclosed in §6). κ = ½ FITTED. Footings never pooled. One new constant, c₀, calibrated on the isolated LG field
dwarfs only. Not "theory closed". Nothing here says the data favour the framework.

## Verdicts (both footings agree)

**Test A: MASS-DRIVEN.** At matched stellar mass (log M★ 5.4–6.8), hosted dwarfs carry the same extra as isolated field
dwarfs:

| | canonical | alt |
|---|---|---|
| hosted (N 23) − field (N 6), median E | +0.037 ± 0.134 (Z 0.27) | +0.021 ± 0.134 (Z 0.16) |
| field only (13): Spearman(E, log M★) | −0.731, p 0.003 | −0.731, p 0.003 |
| all dwarfs: Spearman(E, log M★) | −0.633 | −0.632 |

Gas-rich field dwarfs at low mass sit above the law as much as hosted ones (Leo T +0.41, Phoenix +0.40, Antlia B +0.28).
X19's field class read NONE because its members are mostly heavier than 10^6.5 M☉. **Being hosted adds nothing.** The
X19/X20 "hosted" EXTRA classes do not call for a host-keyed selector.

**Test B: FLOOR PARTIAL.** Model σ² = σ_iso² + c₀². c₀ is calibrated on the 13 field dwarfs and graded out of sample:

| | canonical | alt |
|---|---|---|
| c₀ (field) | **4.59 [4.01, 5.14] km/s** | **4.05 [3.41, 4.66] km/s** |
| H χ²: floor vs law (N 61) | **217 vs 637** | **195 vs 559** |
| bright M31 (25), residual | −0.02 ± 0.09 (Z −0.2), reproduced | +0.01 ± 0.09, reproduced |
| M31 others (5) | +0.13 ± 0.27, reproduced | +0.19 ± 0.28, reproduced |
| MW classical (8) | +0.05 ± 0.10, reproduced | +0.06 ± 0.11, reproduced |
| MW ultra-faints (31) | **−0.36 ± 0.09 (Z −3.9): overshoot** | **−0.28 ± 0.09 (Z −3.0): overshoot** |
| c₀ fitted on H (in-sample, reported) | 3.64 [3.47, 3.82] | 3.46 [3.29, 3.64] |

The floor turns three of the four dwarf classes from 2–5σ excesses into agreement, using a constant set on other galaxies.
It overshoots the ultra-faints: their binary-corrected σ (median 3.2 km/s) sits below the field's c₀. The field and H
values agree on alt and are about 2σ apart on canonical.

**Checks 7/7** (K0 reproduces X19; K1 round trip; K2 recovers an injected c₀ = 4; K3 0.13 GB). `--mutate` fails K0.

## What it costs and what it leaves

- **SPARC:** ΔE = 0.002 dex at V = 100 km/s, 0.02 at 30 km/s. Negligible.
- **Fails:** Crater II (E −0.44, the floor predicts +0.38) and Antlia II (+0.06 vs +0.22). These are the two "too cold",
  tidally exposed giants. A floor can only raise σ, so it makes them worse. Sagittarius and the M31 dEs are untouched.
- **Consistent with X22's forest gate.** The cold component must have c_s ≤ 6–13 km/s at z = 2–3; c₀ ≈ 3.5–4.6 sits below
  that. It is the same scale as the held medium's own sound mode in ZT11 (0.6–5.5 km/s in the disc), which there is
  density-keyed, not a floor.
- **Not derived.** c₀ is a new constant, and the quadrature form is phenomenological. No action term gives it yet. It does
  not touch clusters, growth or the MW disc.

## Consequence for the v3s verdict

The hosted dwarfs were the class that blocked every selector in X19 and broke universal late heating in X23. X24
re-reads them as a low-mass trend that hosted and field dwarfs share. Three of the four classes are reproduced by one
velocity floor of about 4 km/s. **The dwarf problem stops being a selector problem.** It becomes one small-scale constant
plus the ultra-faint overshoot and the Crater II / Antlia II cold outliers. Clusters, growth and the MW disc are unchanged.

## Files

`FROZEN_CRITERIA.md`, `x24_dwarf_velocity_floor.py`, `.out` / `_results.json`, `_MUTATE` outputs.

    OMP_NUM_THREADS=1 python3 x24_dwarf_velocity_floor.py            # exit 0, 7/7
    OMP_NUM_THREADS=1 python3 x24_dwarf_velocity_floor.py --mutate   # exit 1, K0 fails
