# UD2: the a0 law on the giant low-surface-brightness disc Malin 1 (FROZEN CRITERIA)

Committed alone, before any script, fetched table or number of this lane exists in the repository. κ = ½ is FITTED. Not
theory closed. Footings never pooled. Not blind: published MOND-type fits of Malin 1 exist and are known in outline.
Adopts nothing. Companion to UD1 (AGC 114905); same law, same labels.

## 0. Why

Owner 2026-11-04: "do these" (AGC 114905 and Malin 1). Malin 1 has a disc over 100 kpc across at very low surface
density, so its outer HI reaches deep below a0, but its bright inner bulge/high-surface-brightness core carries a
stellar mass-to-light uncertainty. Record check: 0 files in campaign_fresh_gravity, rebuild_2026_10_22, data_assembly
name Malin 1. One galaxy excludes nothing (owner rule).

## 1. Data (fetched after this commit)

- **Primary:** Lelli, Fraternali & Sancisi 2010 (A&A; HI rotation curve and mass model of Malin 1; id resolved at fetch):
  the tabulated V(R) with errors, inclination i0 ± σ_i, distance, and the published baryon components (gas; bulge and
  disc stellar profiles with their stated mass-to-light or masses).
- **Secondary:** any later published Malin 1 rotation curve with a table (e.g. a newer HI or IFU curve) reported beside,
  never pooled.
- If no tabulated rotation curve with baryon components (or the profiles to build them) is available, the lane stops as
  NOT EVALUABLE (no digitising).

## 2. The law

As UD1 §2: g = ν(g_b/a0) g_b, ν(y) = ½ + √(¼ + 1/y); both footings a0 = 9.3603e-11 and 1.1312e-10 m s⁻²; no parameter
fitted to the rotation curve. Stellar mass-to-light ratios as published (the authors' preferred values); if the paper
gives a range rather than one value, the primary is the range's stated fiducial and both ends are reported.

## 3. Grade (per footing, published i0 and published M/L)

- **All points:** χ² with published errors; CONSISTENT p ≥ 0.05, FAIL p < 0.01, TENSION between. Primary label.
- **Outer disc (reported, also labelled):** points where the published stellar bulge contribution to V_b² is below 10 %,
  so the label there does not lean on the bulge M/L.
- Reported beside, not graded: bulge M/L at both ends of the published range (or ×0.5 and ×2 if none is given, said so).

## 4. Inclination

As UD1 §4: scan 5°-90°, i_best and p ≥ 0.05 range; RESCUED WITHIN ERRORS if the range overlaps i0 ± 2σ_i, else NOT
RESCUED with distance in σ_i. If no σ_i is published, ±5° is used and said to be assumed.

## 5. External field

Reported only, as UD1 §5 (g_e/a0 = 0.01, 0.03, assumed).

## 6. Checks

K0 reproduce the published baryon curve to 2 %; K1 no fitted M/L, a0 or distance; MUTATE ν ≡ 1 must be worse than the
law on both footings, separate outputs; rerun byte-identical.

Output: per footing, all-points and outer-disc χ², p, labels, i_best, rescue label; EFE rows; checks. Nothing is a
verdict on a theory.
