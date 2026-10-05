# CFG340: the pre-reionisation cold-share candidate on the big systems

> κ = ½ is FITTED. The cold component's mass is still required; no dark-matter particle is added. Nothing here says the theory is closed.

**Frozen verdict: FAIL** (criteria `FROZEN_CRITERIA.md`, a1e50f7fc, committed before any number).

The failure does not come from R. The candidate (M_c = R M_b/f_b, max bookkeeping, P1 profile at z_f = 3) already breaks three big populations at **R = 1**, where B's committed rule passes them. B passes them because its switch keeps the cold term off there. The candidate's max bookkeeping has no switch, and P1's compact r_f puts a flat-v_c cold term inside the radii these data probe.

| population | B baseline | candidate at R = 1 (z_f 3) | R_max (both footings) | R_plaus (upper, source) | ratio |
|---|---|---|---|---|---|
| S1 SPARC log M★ ≥ 10 | CFG45 S 98% < 0.03; Δrms +0.0009 | A3 72% / 89%; Δrms +0.043 | fails at R = 1 | 3 (PROVISIONAL) | < 1/3 |
| S2 SPARC dwarfs | 100%; Δrms +0.0009 | A3 100%; Δrms **+0.0075** (limit 0.005) | fails at R = 1 | 12.3 (CFG317 LV-field R_ind, yield +0.1) | < 0.08 |
| X1 X-ray ellipticals | S z +1.04 | z +0.78 | **9.45** | 3 (PROVISIONAL) | 3.15 |
| K1 KiDS isolated lenses | law χ² 162.6 / 154.8 | Δχ² **+29.1** / +6.7 (limit 9) | fails at R = 1 | 3 (PROVISIONAL) | < 1/3 |
| C1 X-COP | identity 0.946 ± 0.080 | 0.946 (= identity, 12/12 beyond r_f) | **1.32** | 1.2 (PROVISIONAL; record f_b/f_bar ≈ 1.05) | 1.10 |

**z_f brackets (reported):**
- z_f = 4: FAIL, the same three populations fail at R = 1.
- z_f = 2: FAIL, with S2 R_max 1.15 and K1 R_max 1.28, both below their R_plaus; S1 still fails at R = 1.

**Post hoc** (no verdict depends on it): each failing population passes only if its cold mass is below the cosmic share. The limits are R ≤ 0.24 (S1), ≤ 0.75 (S2) and ≤ 0.83 (K1).
- Mechanism, massive spirals: for M_b = 1e11 M☉, r_f ≈ 70 kpc gives cold v_c ≈ 180 km/s. At R_HI that exceeds the law's phantom.
- Mechanism, dwarfs: the cold v_c stays flat all the way to the centre, while the phantom vanishes there. So the inner RAR points move even though R_HI does not.

**Reported only, SLUGGS h50** (B is red there, z +3.3): at R = 1 the candidate gives z +1.19 / +1.10. At R = 3 it overshoots (−3.9). Beyond the five dwarf populations, this is the one place where the candidate helps at R = 1.

## Controls
- **C0a–d pass:** the law and identity reproduce B's committed numbers to 0 / 1e-9. These are CFG39's SPARC rms0, CFG4_switch's KiDS ν_mono χ², CFG45's X-ray law z and CFG4_clusters' identity 0.9457.
- **The "R = 1 passes everywhere" check FAILS and is kept.** That failure is the finding.
- **R_max is contiguous** on a 0.1-dex grid.
- **MUTATE** (R = 30 on all of SPARC) is flagged failing: A3 is 0%, Δrms +0.73. This is uninformative, given that R = 1 already fails.

## Lean
`CFG340_bounds.lean`: 6 theorems over rational bounds (Mathlib, no sorry). They cover the three FAIL edges against R_plaus, X1 ≥ 2 R_plaus, C1 between 1× and 2×, and the FAIL decision. Compile with `cd fable_independent_2026/lean_2026 && lake env lean <abs path>/CFG340_bounds.lean`.

## Files and run
- `cfg340_big_systems.py`: about 5 s. The main run exits 1 (5/6 checks); the MUTATE run exits 0 (5/5).
- Outputs: `cfg340_big_systems{,_MUTATE}.out` / `_results.json`.
- Run: `python3 campaign_fresh_gravity/CFG340_preion_candidate_big_systems/cfg340_big_systems.py` (set `CFG340_MUTATE=1` for the control).
- Harnesses, all exec'd read-only: CFG45 prefix, CFG4_galaxy_law prefix, the FP1 KiDS slice with FP20's projector (CFG4_switch K3 logic), and the CFG4_clusters prefix.
- Data: SPARC comes from SPARC_Lelli2016c.mrt and the rotmod files (never SPARC_table.txt). Nothing was downloaded.
