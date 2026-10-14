# CFG766 FROZEN CRITERIA: pre-flight — does any RC100 galaxy reach the clock-diagnostic regime within observed radii?

Date: 2026-10-13. Block CFG760–769. Committed ALONE before any CFG766 script or number. κ = ½ FITTED; not "theory closed".

## Why
CFG765: separating the orbital and universal formation clocks needs y = g_bar/a₀ ≤ 0.17 at the measured radius. RC100
(Nestor Shachar+2023, the record's CORRECTED table, z 0.6–2.5) is the largest high-z sample in the record.

## Method (read only: real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv)
R_need = √(G M_bar/(0.17 a₀)) (point-mass baryons, favourable: an extended disc reaches the y threshold at the same or a smaller
radius only beyond its mass, never inside it at higher y). Ratio ρ = R_need/R_e per galaxy, both footings.

## Test
- **R1. REACHABLE iff ≥ 10 galaxies have ρ ≤ 3** (≈ the outer extent of individual high-z kinematics), on both footings.
  NOT REACHABLE otherwise.
- Reported: the ρ distribution, and the count with ρ ≤ 5.

**MUTATE** (`CFG766_MUTATE=1`): threshold y = 1.7 instead of 0.17. R1 must then be REACHABLE. Exit 1 iff it bites.
