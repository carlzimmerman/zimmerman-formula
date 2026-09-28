# CFG21 — one number for the edge conflict: KiDS and the Local Group, jointly

Script: `CFG21_kids_lg_joint.py`, about 20 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. With the LG term dropped, H0 fails (rc = 1).
- The main run exits 1, because H1 failed.

## The statistic

One universal phantom edge x_e is scored against both data sets:
- **KiDS isolated lenses:** CFG16's exact machinery, with the self-consistent 2-halo caps.
- **The LG's zero-velocity radius:** CFG20's committed R₀(x_e), against 0.93 ± 0.12 Mpc.

The operative statistic is the standard parameter-difference tension, T(x_e) = [χ²_KiDS(x_e) − min χ²_KiDS] + χ²_LG(x_e), minimised over x_e. With one shared parameter, T_min ≈ σ².

**Disclosure.** The first-written statistic, Δχ²_KiDS against the untruncated law plus χ²_LG, asked for min ≤ 9. The first run (MUTATE) showed KiDS's own best edge sits 35–38 below that reference, so that statistic passes trivially. It was revised before any main run, and the first-written values are still reported.

## Results

**C1 (control):** CFG16's committed floors and CFG20's committed R₀ grid are reproduced exactly.

| row | KiDS's own best x_e | LG's own best x_e | joint best x_e | T_min | ≈ σ |
|---|---|---|---|---|---|
| canonical P2, LG 1.145e11 | 0.62 | 0.13 | 0.56 | 26.2 | **5.1** |
| canonical ν_mono, LG 1.145e11 | 0.63 | 0.13 | 0.57 | 27.8 | **5.3** |
| canonical P2 / ν_mono, LG 1.72e11 | 0.62 / 0.63 | 0.10 | 0.51 / 0.53 | 41.0 / 42.7 | 6.4 / 6.5 |
| alt P2 / ν_mono, LG 1.145e11 | 0.62 / 0.63 | 0.11 | 0.55 / 0.56 | 31.9 / 33.4 | 5.6 / 5.8 |
| alt P2 / ν_mono, LG 1.72e11 | 0.62 / 0.63 | 0.10 | 0.49 / 0.51 | 48.3 / 50.6 | 6.9 / 7.1 |

- **H0** (the LG raises the joint minimum by more than 9 in every case): pass.
- **H1** (a universal edge is jointly acceptable, T_min ≤ 9): **FAILED**.

## Standing

**A universal sharp edge is excluded at 5–7σ by KiDS and the Local Group together.**
- KiDS alone wants the phantom to run to about 0.6 r_ta, which is far past the cold budget's ~0.35 and the collapse's own splashback (0.18–0.27).
- The LG wants it to stop near 0.1 r_ta, which is about 200 kpc for the MW.

The target law's shape needs to change, not just its edge. The next lane tests the obvious candidate: a *soft* edge, where the phantom's ρ ∝ r⁻² gives way to ρ ∝ r⁻³ like collapsed matter instead of stopping dead.

Nothing here says the theory is closed.
