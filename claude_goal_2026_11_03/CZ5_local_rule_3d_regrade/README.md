# CZ5_local_rule_3d_regrade: LOC FAILS ON BOTH FOOTINGS. On the 3D field the local filter rule fails Cassini (13.3x canonical, 18.1x alt). Its dwarfs still pass (17/24). No filter form on record survives

Criteria `FROZEN_CRITERIA.md` (c805085c2f), committed alone before the script. Run `OMP_NUM_THREADS=1 python3 -I -B cz5.py` (5 min, peak RSS 1.50 GB; no 1024³ run was live), output `cz5.out` / `cz5.json`, timing `cz5.time`; MUTATE twin `cz5_MUTATE.*`. No download. No file outside this folder is edited. κ = ½ FITTED, held fixed. Footings never pooled. No cold component, no particle. Not theory closed. Nothing here says the data favour the framework.

**The one change from CZ2.** The local rule ξ_loc = |g|²/(|∇|g|| g*) now takes |g| from the **vector** Newtonian field, the system plus the host's uniform field, with the full 3D gradient. CZ2 used the spherical quadrature √(g_int² + g_e²).

| gate | canonical | alt |
|---|---|---|
| T0 Milky Way (carried, KT26) | 0 cells, FAIL | 30 cells, PASS |
| **T1 Cassini, 3D** | **13.3× ceiling, FAIL** | **18.1× ceiling, FAIL** |
| T2 dwarfs, 3D (line 15/24) | 17/24, PASS | 17/24, PASS |
| T3 SPARC (carried, KT27) | d rms +0.0129, FAIL | +0.0031, PASS |
| T4 planets, 3D (Z ≤ 2) | worst 3.1e-7, PASS | worst 6.8e-7, PASS |
| **Label** | **LOC FAILS: MW, Cassini, SPARC** | **LOC FAILS: Cassini** |
| STRICT (dwarfs ≥ plain in 3D) | pass (17 vs 17) | fail (17 vs 18) |

## Dwarfs, row by row (E1, the graded field; Fornax at Υ = 2, obs 11.7 ± 0.9 km/s)
| row | what it is | canonical | alt |
|---|---|---|---|
| R0 | CZ2's code, verbatim | 17/24, 11.94 | 17/24, 12.52 |
| R1 | 1D, field-gather (the construction alone) | 17, 11.99 | 17, 12.57 |
| R3 | 1D ξ, vector ν argument | 17, 11.96 | 17, 12.54 |
| **R2** | **3D, graded** | **17, 12.07** | **17, 12.66** |
| plain, 3D | no filter, vector ν | 17, 12.59 | 18, 13.15 |

R2 passes the same 17 dwarfs as CZ2's LOC. E2 (the MW + M31 vector sum, beside) gives R2 16/24 on both footings and plain 16 / 17.

## Reading
- **This is the frozen re-grade CW1 asked for.** CZ2–CZ4 recorded LOC as surviving on alt, but only because of the spherical quadrature.
  - On the real field, the Sun's pull and the Galaxy's cancel at a saddle about 0.75–0.85 r_M toward the Galactic centre.
  - There |g| → 0, so ξ_loc → 0. The Sun's phantom isn't smoothed in the region that sets the Cassini quadrupole.
  - Cassini goes from 0.0039× / 0.021× to 13.3× / 18.1×.
- **Nothing else moves.** The dwarfs keep 17/24 with the same set; Fornax shifts 0.1 km/s. The planets pass by seven orders.
  - The dwarfs are mostly internally dominated where their light is. Any saddle lies outside the stars.
  - At the planets, ξ is set by the Sun's own steep field.
- **So the record's filter line has no survivor.**
  - Fixed widths fail Cassini (HALF on both footings, CZ2) or the planets (CZ3).
  - The tidal rules fail the Milky Way once the vertical tide is in (KT29–KT32).
  - The local rule fails Cassini on the 3D field (here).
- **What fails is the class, not a tuning.** Any rule whose width scales like |g|^p / |∇|g|| with p > 1 sends ξ → 0 wherever the total field vanishes. Every system in an external field has such a point.
  - This is a reading. No class theorem was graded here.
  - A rule built on the system's own tidal field (TID, TF) has no such zero. Those rules fail the Milky Way instead.

## As hard as a fail
- **The Cassini number is robust.** CW1 tested the gradient against finite differences (1e-9) and the result at 2× radial resolution, L 128 with 192 μ nodes, and a wider grid. CZ5 reproduces CW1 to 1e-4 (K3).
- **T0 and T3 are carried.** In the midplane, symmetry makes the 3D ξ equal to the 1D one at the evaluation point. KT26's single MW width and the (R, z) variation of ξ are inherited and not graded here. On alt they can't change the label: T1 alone fails.
- **The Sun is an isolated point mass in a uniform Galactic field.**
  - CZ4's neighbourhood (disc tide, nearby stars) adds tidal accelerations of order 1e-14 m/s² near 6,000 AU. The fields at the saddle are of order 1e-10.
  - That can move the saddle, but it can't remove the zero of |g|.
  - This is an estimate. It wasn't computed here.
- **The construction is field-gather.** K5 shows it equals CZ2's density-row smoothing at constant width (18/24 reproduced). The scatter form is degenerate for a point source, because ξ → ∞ at the mass.
- **The dwarf virial integral uses only the l = 0 phantom field.** That is exact for a spherical tracer.
- **Development fix before the frozen run.** In a component test, the bilinear table lookup missed K2's point-mass line (1.7e-3 against 1e-4). The direct table values were right to 1.5e-5. The lookup was changed to bicubic, with a denser ξ grid, giving a maximum error of 2.6e-5 over 400 random points. The frozen run then passed K2.
- **Memory.** Peak RSS was 1.50 GB, above the 1 GB small-job guideline. No 1024³ run was live.

## Checks (all pass)
- K1: CZ2 reproduced (17 / 18 / 18, Fornax 11.94 / 12.52).
- K2: table, Plummer limit 0, large r 1.5e-8, point-mass limit 1.6e-5.
- K3: Cassini vs CW1, 1e-4.
- K4: planets vs CW1, 4e-4.
- K5: constant width, 18 / 18.

## MUTATE (ν ≡ 1), `cz5_MUTATE.out`
Every σ is Newtonian: dwarfs 3/24 in every row, Fornax 4.84 km/s. Cassini and the planet rates are 0. The alt label becomes "FAILS: T2 dwarfs". Exit 1 by design.
