# AX1 common engine: FROZEN CRITERIA, committed alone before any script or number

Shared by every AX1 class lane (`BIMOND/`, `AeST/`, `khronon/`, `nonlocal/`, `v3s/`). Each class has its own FROZEN_CRITERIA, committed alone before its run. κ = ½ FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. **Not blind:** every record number below is seen (D7b, D7c, E2, C6). Not theory closed. Nothing here says the data favour the framework. The cold sector stays retired; nothing here reinstates it. CMB and clusters out of scope, open.

## What the engine computes (script `common/ax1_engine.py`, one thread, seconds, no download)

1. **QUMOND Cassini Q2**, independent code: KT16's integral form at ξ = 0, Q2 = |q| · 1.5 a0/r_M, r_M = √(GM/a0), GM = 1.32712440018e20 m³/s². The phantom ∇·[(ν−1)∇φ_N] of the Sun in a uniform Newtonian external field g_Ne. ν takes the **Newtonian** field (QUMOND convention; no MOND field fed to ν). Fields: E0 g_Ne = 6.913e-11 (A60, the framework Milky Way); E1/E2/E3 total g_e = 1.9/2.2/2.6 × 9.36e-11, converted to g_Ne by solving x(1 + A(x)) = g_e/a0 per ν. Grid: ln r from 1e-7 to 1e5 r_M, 20000 points; 200-point Gauss–Legendre in μ.
2. **Saturn monopole**: δg = g_N A(y), y = g_N/a0, at a = 9.5826 AU (isolated; the external field is a 1e-6 correction there).
3. **Record reads, by JSON, never by eye:** D7c SPARC paired z (`SPARC[foot][key]['vs']['L']['z']`), D7c QUMOND Q2 (known answer), E2 AQUAL Q2 (`R1['<foot>|none']`, `R1['<foot>|66.3803']`, `R3[key]`), C6 screened Q2 and planets (v3s only).

Candidate static functions A = ν − 1, fixed now, no scan: **law** A = (√(1+4/y) − 1)/2 (the owner's law, exact); **law + turn-off** A/(1 + (y/66.3803)²) (D7b's P5 form, y_t from the record's closure; reported because a free function may carry it); **β ∈ {2.5, 3, 4, 5, 6}**, ν = (1 + y^−β)^{1/2β}, the D7c members that pass SPARC. Nothing else.

## Gates and tolerances (set now)

- **G1 SPARC.** Law and law + turn-off: PASS by identity (the turn-off acts at y > 60, above SPARC). β members: D7c's paired statistic **against the law L**, PASS if z ≥ −2 (D7c's own line), read from JSON. D7c's full label (worst comparator) and S1 reading are reported.
- **G2a Q2.** PASS if Q2 ≤ 9.0e-27 s⁻² (Hees+2014 (3 ± 3)e-27, 2σ upper) **at all four fields**. Park+2026 (5.2e-27) reported. QUMOND-type classes use this engine at the exact footings; AQUAL-type classes use E2's AQUAL values (E2 ran at 9.36e-11 / 1.13e-10; the 3e-5 / 1e-3 rounding is stated, not corrected).
- **G2b monopole.** PASS if δg(Saturn) ≤ 7.0e-15 m/s² (Fienga & Minazzoli 2024 via `prep_2026/planetary_doors/BOUNDS.md`).
- **G2c PPN γ, α1, α2.** Cassini γ − 1 = (2.1 ± 2.3)e-5; |α1| < 1e-4 (LLR), |α2| < 2.4e-7 (solar spin); pulsar bounds 4e-5 and 2e-9 reported (as AS3). From each class's literature [PROVISIONAL] or record lane; no new PPN derivation.
- **G3, G4.** From the class literature [PROVISIONAL] and record lanes, each entry marked P / F / O with its source. GW170817: |c_T/c − 1| < ~1e-15.

**Class label per footing:** PASS if one candidate passes G1, G2a–c, G3 and G4. FAIL [gates, numbers] if every candidate fails a computed or published gate. OPEN [what] if a candidate survives every computed gate but a G3/G4 entry is O. A failed check means no clean label.

## Checks (exit 0 only if all pass)

- **K1 known answer (PAPER58/D7b):** law QUMOND Q2 at D7c's a0 (9.36e-11, 1.13e-10) reproduces D7c's `L` values, 8 cells, max |rel| ≤ 1e-2. This is the plain-QUMOND limit reproducing PAPER58's QUMOND Cassini number (1.70–3.70× / 1.91–4.03× Hees).
- **K2:** β ∈ {2.5, 3, 4, 5, 6} reproduce D7c's Q2, 40 cells, max |rel| ≤ 1e-2.
- **K3 resolution:** doubling both grids changes Q2 by ≤ 1e-3 (law, canonical E0 and E3).
- **K4 spherical identity:** at Saturn, g_N(1 + A_law) equals the algebraic root g_N/2 + √(g_N²/4 + a0 g_N) to 1e-12.
- **MUTATE twin** (`--mutate`): A ≡ 0 (Newton). K1 must FAIL and every Q2 must be 0. Output `_MUTATE`, exit 1.
- **Byte-identical rerun:** each class run is done twice; the two JSON files must have the same SHA-256.
