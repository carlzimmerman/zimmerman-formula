# CFG336: does a formation-epoch density for the native cold mass fix the ultra-faints?

- **Criteria:** `FROZEN_CRITERIA.md`, committed before any score (18a68e0ad).
- **Settings:** κ = ½ FITTED; both footings; ν_mono; inputs on disk only. No DM particle; the cold component's mass is required.
- **Run:** `python3 cfg336_formation_epoch.py` (about 5 s; 4/5 checks, exit 1: C1 fails as below). `CFG336_MUTATE=1 python3 cfg336_formation_epoch.py` (writes `_MUTATE` outputs; both MUTATE checks pass, C1 fails again). Then `python3 cfg336_lean_gen.py` and `cd fable_independent_2026/lean_2026 && lake env lean <abs path>/CFG336_certificate.lean`: 105 theorems, exit 0, no sorry.

**Verdict: NOT.** It fails under B's rule (S) and under the CFG4 T5 max bookkeeping (M), for every profile, on both footings.

## Formula
- M_c = M_b/f_b (CFG35/CFG313). Collapse at z_f gives the radius r_f = [3 M_c / (4π · 18π² ρ_m0 (1+z_f)³)]^{1/3}.
- P1 (primary): M_cold(<r) = M_c min(r/r_f, 1).
- Inputs: z_f = 8 (range 6–10) for M_V > −7.7, and 3 (range 2–4) otherwise. This is the a-priori class split. The LVD has ages for only 4 systems, and no SFH table is on disk.

## Why it cannot work (the mass budget, not the density)
- For **every one of the 40 MW ultra-faints**, the law's own phantom inside (4/3) r_half exceeds the **whole** native cold share (1−f_b) M_c = 5.36 M_b. The ratio is 1.57–11.0, median 3.5 (canonical), and 1.73–12.1 (alt). Lean certifies this per object.
- Under T5 "max" bookkeeping, no profile and no z_f can switch the cold term on. Under (S), f_ex depends only on the total masses, so it is 0 whatever z_f is (CFG313).
- Diagnostic (A, additive, which is NOT B's rule): putting all of M_c inside r gives +0.253 dex (2.39 σ). That is not even PARTIAL, and it pushes the LV field dwarfs to −3.0 σ.

| row (canonical; z canonical / alt) | UFD | MW classical | M31 Collins | M31 LVD | LV field |
|---|---|---|---|---|---|
| law = S (all profiles) = M·P1 | +0.325 (3.77 / 3.55) | +0.027 (0.32 / 0.09) | +0.064 (0.78 / 0.55) | +0.044 (0.60 / 0.42; M·P1 alt 0.32) | −0.044 (−0.60 / −0.85) |
| M·PB (all of M_c inside r) | +0.325 (3.77 / 3.55) | −0.067 | +0.015 | +0.036 | −0.186 (−1.92) |
| A·P1 (diagnostic) | +0.286 (3.16 / 2.99) | −0.008 | +0.001 | +0.008 | −0.096 |
| A·PB (diagnostic) | +0.253 (2.39 / 2.28) | −0.143 | −0.073 | −0.076 | −0.267 (−3.04) |

The outer globulars have no cold component, so they are unchanged (CFG333 R2).

## Screens (report only)
- **Mass multiplier needed (reading M, canonical).** To reach 2× the law error, M_c must be multiplied by k = 5.9 if all of it sits inside r, or by k = 31.5 under P1 at z_f = 8. To reach zero offset, k = 13.2 and 105.
- **Scatter and slope.** At fixed z_f, P1 gives M_cold(<r) ∝ M_b^{2/3}(1+z_f) r. That is a slope of 2/3, not the 0.52 of CFG335. With one z_f per class, the within-class scatter is zero, against the 0.6 dex CFG335 needs. So the idea explains neither the slope nor the scatter.

## Controls
- **C2 passes.** The AUDIT_UFD baseline is reproduced exactly.
- **C3 passes.**
- **C1 fails, and the failure is kept.** At z_f = 0, (S) reproduces CFG313 exactly. (M) moves one row, M31 LVD alt, by −0.0021 dex. CFG313 scored only (S), so (M) with the native mass has no record row to match. Under (M), the native cold share exceeds the phantom in some high-acceleration classical satellites (phantom/cold median 0.78 for the MW classicals).
- **MUTATE (z_f permuted, seed 336).** (A·P1) UFD rises by +0.011 dex (it degrades, as required). (M) stays inert in both runs.
