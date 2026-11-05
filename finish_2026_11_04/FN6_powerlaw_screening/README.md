# FN6_powerlaw_screening: WINDOW on both footings. Canonical 3 of 48 grid points, every one resting on a single Milky Way cell; alt 9 of 48. No shuffle survives (0 of 5 at every point)

Criteria `FROZEN_CRITERIA.md` (5f0f4a5d99), committed alone before any script.

- **Not blind.** AX1, C6P, FN1b, KT16, KT17, KT25, CZ1–CZ5 and CFG820/CFG821 were read first.
- **Assumptions.** κ = ½ FITTED, held fixed. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s², never pooled.
  No cold component, no particle. No downloads.
- **What a window is.** A window is a two-number description (p, L_MW), not a derivation. No action here produces
  this length. Not theory closed. Nothing here says the data favour the framework.
- **Form graded.** Form R only: Φ = Φ_N + S Φ_ph[Sρ], where S is a Gaussian of width L = L_MW (M / 6e10 M☉)^p and M is
  each system's own baryonic mass.
- **Departures and readings.** All are in `AMENDMENTS.md`, dated, with pre-grid and post-result marked. The main one:
  at solar widths σ = L/r_M ≤ 50, T1 uses KT33's numeric Cassini engine and T4 uses a new numeric form-R planet
  engine, both checked against FN1b's linear response at 20 and 50 r_M.

## Labels (frozen rule)

| footing | label | passing points (p, L_MW in kpc) | count | shuffle (MUTATE) |
|---|---|---|---|---|
| canonical | **WINDOW** | (0.30, 1.5), (0.35, 1.5), (0.40, 1.5) | 3 of 48 | 0 of 5 survive at each point |
| alt | **WINDOW** | (0.30, 1.5), (0.30, 2.0), (0.35, 1.5), (0.35, 2.0), (0.40, 1.5), (0.40, 2.0), (0.40, 3.0), (0.45, 2.0), (0.45, 3.0) | 9 of 48 | 0 of 5 survive at each point |

- **Look-elsewhere.** 48 grid points per footing.
- **Canonical's T0 is one cell.** At each canonical point exactly one of the 1,375 in-prior cells passes, and it is the
  same cell each time.
  - The cell: BV2, Σ_b 50.5, M_bb 2.12e10, R_d 2.6, h 0.35 / 1.08, thick share 0.35, R_d,thick 2.0.
  - Its mass is 7.65e10 M☉ and its length 1.61–1.65 kpc.
  - It reads v_c 226.6–226.7 km/s and K 70.3–70.5 M☉/pc².
  - It holds at refine 2 (ΔK +0.04, Δv_c +0.02 km/s).
- **Alt's T0 is comfortable.** The alt points have 19–42 passing cells.

## Where each gate fails (failing gates; passing Milky Way cells of 1,375 in brackets)

| p \ L_MW, canonical | 1.0 | 1.5 | 2.0 | 3.0 |
|---|---|---|---|---|
| −0.50 | T0, T2, T3 (0) | T0, T2, T3 (0) | T2, T3 (3) | T2, T3 (2) |
| −0.25 | T0, T2, T3 (0) | T0, T2, T3 (0) | T2, T3 (4) | T2, T3 (4) |
| 0 | T0, T2, T3 (0) | T0, T2, T3 (0) | T2, T3 (2) | T2, T3 (6) |
| 0.10 | T0, T2, T3 (0) | T0, T2, T3 (0) | T0, T2, T3 (0) | T2, T3 (3) |
| 0.20 | T0 (0) | T2, T3 (1) | T0, T2, T3 (0) | T2, T3 (4) |
| 0.30 | T0 (0) | **PASS** (1) | T0, T3 (0) | T3 (4) |
| 0.35 | T0 (0) | **PASS** (1) | T0 (0) | T3 (4) |
| 0.40 | T0 (0) | **PASS** (1) | T0 (0) | T3 (4) |
| 0.45 | T0, T1, T4 (0) | T1, T4 (2) | T0 (0) | T3 (1) |
| 0.50 | T0, T1, T4 (0) | T1, T4 (2) | T0, T1, T4 (0) | T0, T1, T3, T4 (0) |
| 0.60 | T0, T1, T4 (0) | T1, T4 (2) | T1, T4 (1) | T0, T1, T4 (0) |
| 0.75 | T0, T1, T2, T4 (0) | T1, T4 (3) | T1, T4 (2) | T0, T1, T4 (0) |

| p \ L_MW, alt | 1.0 | 1.5 | 2.0 | 3.0 |
|---|---|---|---|---|
| −0.50 | T0, T2, T3 (0) | T2, T3 (11) | T2, T3 (30) | T2, T3 (38) |
| −0.25 | T0, T2, T3 (0) | T2, T3 (14) | T2, T3 (34) | T2, T3 (42) |
| 0 | T0, T2, T3 (0) | T2, T3 (17) | T2, T3 (38) | T2, T3 (43) |
| 0.10 | T0, T2 (0) | T2, T3 (18) | T2, T3 (38) | T2, T3 (43) |
| 0.20 | T0 (0) | T2 (19) | T2, T3 (38) | T2, T3 (45) |
| 0.30 | T0 (0) | **PASS** (20) | **PASS** (38) | T3 (43) |
| 0.35 | T0 (0) | **PASS** (19) | **PASS** (39) | T3 (44) |
| 0.40 | T0 (0) | **PASS** (21) | **PASS** (40) | **PASS** (39) |
| 0.45 | T0, T1, T4 (0) | T1, T4 (21) | **PASS** (42) | **PASS** (38) |
| 0.50 | T0, T1, T4 (0) | T1, T4 (22) | T1, T4 (41) | T1, T4 (39) |
| 0.60 | T0, T1, T4 (0) | T1, T4 (23) | T1, T4 (41) | T1, T4 (36) |
| 0.75 | T0, T1, T2, T4 (0) | T1, T4 (26) | T1, T4 (45) | T1, T4 (33) |

### How each gate binds

- **T1 Cassini and T4 planets bound p from above.**
  - Both fail at every p ≥ 0.5, and at p = 0.45 with L_MW ≤ 1.5. There the Sun's length falls below about 0.6–0.7 r_M.
  - T4 binds a little before T1: at (0.45, 1.5) canonical, Q2 is 1.0× the ceiling and Saturn's Z is 3.0.
  - At very small widths Q2 settles at about 6.1× / 6.6× the ceiling, the point-mass limit.
- **T2 dwarfs (15 of 24 needed) bound p from below.**
  - They fail at p ≤ 0.1, with 3 to 13 passing, and at p = 0.2 for L_MW ≥ 1.5 (13 or 14).
  - They pass at p ≥ 0.3 (15–18), except (0.75, 1.0) with 12.
- **T3 SPARC (SURVIVES needed) bounds L_MW from above.**
  - It fails at L_MW = 3 for p ≤ 0.45 (canonical) and p ≤ 0.35 (alt).
  - It also fails at p ≤ 0.1 (except alt (0.1, 1.0)), at p = 0.2 for L_MW ≥ 1.5 / ≥ 2, and at canonical (0.3, 2.0) and
    (0.5, 3.0).
- **T0 Milky Way (at least one cell needed) bounds L_MW from below.**
  - L_MW = 1 fails everywhere on both footings.
  - Alt passes at every L_MW ≥ 1.5 (11–45 cells).
  - Canonical never has more than 6 cells. It passes at L_MW = 1.5 only for p ≥ 0.2, at 2.0 only for p ≤ 0 or p ≥ 0.6,
    and at 3.0 for p ≤ 0.45.
  - Six canonical non-window points carry FN1b's [GRID-DEPENDENT] flag, each because one passing cell fails at
    refine 2: (−0.5, 3), (−0.25, 2), (−0.25, 3), (0, 2), (0, 3) and (0.4, 3). No window point is flagged.
- **The frozen hand estimate** was "p ≳ 0.35, Sun about 0.3 pc and screened". The window starts at p = 0.30. The Sun gets
  0.07–0.9 pc on canonical and 0.03–1.2 pc on alt.

### Window points: Q2 × ceiling / worst Z / dwarfs of 24 / SPARC Δrms / MW cells

| (p, L_MW) | L(1 M☉) | canonical | alt |
|---|---|---|---|
| (0.30, 1.5) | 0.88 pc | 1.5e-5 / 4.2e-5 / 17 / +0.0028 / 1 | 1.8e-5 / 5.1e-5 / 18 / +0.0001 / 20 |
| (0.35, 1.5) | 0.25 pc | 6.3e-4 / 1.7e-3 / 18 / +0.0017 / 1 | 7.4e-4 / 2.1e-3 / 18 / −0.0004 / 19 |
| (0.40, 1.5) | 0.073 pc | 2.6e-2 / 7.2e-2 / 18 / +0.0010 / 1 | 3.1e-2 / 8.8e-2 / 18 / −0.0007 / 21 |
| (0.30, 2.0) | 1.17 pc | fails T0, T3 | 7.5e-6 / 2.2e-5 / 17 / +0.0021 / 38 |
| (0.35, 2.0) | 0.34 pc | fails T0 | 3.1e-4 / 9.0e-4 / 18 / +0.0009 / 39 |
| (0.40, 2.0) | 0.098 pc | fails T0 | 1.3e-2 / 3.7e-2 / 18 / +0.0002 / 40 |
| (0.40, 3.0) | 0.15 pc | fails T3 | 3.8e-3 / 1.1e-2 / 18 / +0.0041 / 39 |
| (0.45, 2.0) | 0.028 pc | fails T0 | 5.2e-1 / 1.5 / 18 / −0.0002 / 42 |
| (0.45, 3.0) | 0.042 pc | fails T3 | 1.6e-1 / 4.6e-1 / 18 / +0.0027 / 38 |

## Known answers

- **KA1 PASS, both footings, exactly.** p = 0 with L_MW = 2.0 reproduces FN1b's 2 kpc row in form R, all 8 items equal,
  floats bit for bit.
  - T1: Q2 6.656845e-42 / 7.800713e-42 s⁻², i.e. 1.28e-15 / 1.50e-15 × the ceiling.
  - T4: worst Z 3.546e-15 / 4.331e-15.
  - T2: 6 / 6 dwarfs, Fornax 6.1629 / 6.2832 km/s.
  - T3: Δrms +0.0607 / +0.0498, FAILS SPARC.
  - T0: 2 [GRID-DEPENDENT] / 38 cells, with the same line counts.
- **KA2 PASS.** p = ½ with L = r_M/2 gives the Sun σ = 0.500000000000. In KT25's form (SO, flux) it reads 1.1785× the
  ceiling on canonical, against CZ2's 1.179. Alt reads 2.9702 against CZ2's 2.97 (reported).
  - The same point in form R reads 1.32× / 1.95× (reported).
- **K-HALF-dwarfs PASS (reported).** The per-Υ power-law length at p = ½, L = r_M/2, in SO form, gives CZ2's HALF counts,
  18 / 18.

## MUTATE (masses shuffled among systems before L is assigned)

**0 of 5 shuffles survive at any of the 9 window points, on either footing** (90 runs).
- **The pool.** Reference masses were shuffled among 181 systems: the Sun, the 24 dwarfs, KT19's 155 SPARC galaxies and
  the Milky Way. Seeds 1–5.
- **Every run fails T2 and T3.** Dwarfs 5–14 of 24; SPARC Δrms +0.017 to +0.176.
- **T1 and T4 pass.** In all five seeds the Sun drew a galaxy's mass (4.8e8 to 5.9e9 M☉), so its length was 0.2–1.2 kpc.
- **T0 not run.** Every run failed T2 first.
- **Reading.** The window is a mass scaling, not a universal length in disguise.
- **Not run.** A within-population shuffle (dwarfs among dwarfs, galaxies among galaxies).

## Failed checks and caveats

- **No check failed in the graded runs.** These pass: K-src (FN1b's source SHA-256), K-sample, K-cells, K-VC1, K-grid,
  KA1, KA2, V2, V3R, the planet identity test at every σ used (max 3e-7), V1 at every T0 point, and K-finite.
  - Every process exited 0.
- **NOT EVALUABLE flags.** The frozen V4 (Fornax at its own L) misses at 8 points with p ≥ 0.5, so T2 is not evaluable
  there. Each of those rows already fails T1 and T4.
- **Extended V4 (post-result, reported).**
  - At the window points, all 155 SPARC galaxies are within FN1b's V4 line at their own L (max 4.1e-4).
  - 3 or 4 dwarfs miss it at (0.4, 1.5), (0.4, 2.0), (0.45, 2.0) and (0.45, 3.0).
  - On a radial grid twice as fine, all but Andromeda IX at (0.45, 2.0) pass (3.7e-3).
  - **No dwarf's pass or fail changes**, so the counts stand (`fn6_v4x.out`, `fn6_v4x_grid.out`).
- **Not computed:**
  - E2, D3 and STRICT for the dwarfs;
  - V1(c);
  - CZ4's environment bounds;
  - a Helmholtz kernel;
  - SPARC beyond KT19's spherical approximation.
- **Peak RSS:**
  - small gates 0.44 GB per process (three in parallel);
  - Milky Way 0.91 GB per footing;
  - V4 checks 0.22 and 0.82 GB;
  - wide binaries **1.77 GB, above the 1 GB target**: the frozen pipeline's 1M-pair population (CW1 reported 1.2 GB).
  - One thread per process, nice 15. No 1024³ run was live; the SY1 search was.
- **Runtimes:**
  - small grid about 6.5 min per part;
  - Milky Way 26 / 29 min (all 48 points);
  - MUTATE 4–5 min per seed;
  - wide binaries 21 s.

## Reported, not graded

**Length at 1 M☉ against wide-binary separations (1–30 kAU).** r_M is 7,961 AU on canonical and 7,241 AU on alt.

| footing | p | L(1 M☉) | in r_M |
|---|---|---|---|
| canonical | 0.30 | 180,700 AU | 22.7 |
| canonical | 0.35 | 52,300 AU | 6.6 |
| canonical | 0.40 | 15,100 AU | 1.9 |
| alt | 0.30–0.45 | 5,800 to 241,000 AU | 0.80 to 33 |

The l = 0 γ_r of a 1 M☉ pair, form R, with CW1's primary host field 1.9e-10 inverted to Newtonian:
- p ≤ 0.35: within 0.6 % of Newton out to 30 kAU.
- p = 0.40: 1.04–1.19 at 30 kAU.
- Alt p = 0.45: 1.40–1.45 at 30 kAU.

**DR4 γ_v through the frozen pipeline.** CW1's injection procedure was run against the pipeline, imported read only
(SHA-256 7c884e0e…), with 4 realisations each. A prediction only.

| footing | Newton | CW1's plain QUMOND | window points |
|---|---|---|---|
| canonical | 0.992 | 1.149 | 1.004, 1.002, 1.035 |
| alt | 0.979 | 1.208 | 1.004–1.040 for p ≤ 0.4; 1.213 at (0.45, 2.0); 1.126 at (0.45, 3.0) |

- **The approximation.** One curve per point, at the 1 M☉ ratio L/r_M. That ratio scales as M^(p − ½).
- **Reading.** Except for alt's p = 0.45 points, the window reads close to Newtonian wide binaries, as the frozen hand
  estimate expected.

**p beside known screening.** The window spans p = 0.30–0.40 on canonical and 0.30–0.45 on alt. A Vainshtein radius
scales as M^(1/3). 1/3 falls inside both spans, between the grid values 0.30 and 0.35. This is a reading only: the
Gaussian kernel here is not a Vainshtein mechanism, and nothing derives this p.

## Files and how to run

- **Scripts.**
  - `fn6_small.py`: T1–T4. `--part K/N`, or `--mutate SEED --points p:L,...`.
  - `fn6_mw.py`: T0, one footing per process. `--all` maps the plane; `--mutate SEED`.
  - `fn6_label.py`: frozen labels, KA1 and KA2, MUTATE summary.
  - `fn6_v4x.py` and `fn6_v4x_grid.py`: post-result V4 checks.
  - `fn6_wb.py`: the wide-binary item.
- **Usage.** Run with `OMP_NUM_THREADS=1 nice -n 15 python3 -I -B <script>`.
- **Engines.** FN1b's `fn1b_small.py` and `fn1b_mw.py` pieces are copied verbatim in marked blocks, with SHA-256 checks of
  the sources. KT33's `cassini_v2` and `mw_reciprocal` are imported read only from FN1b's `vendor_kt33/`.
- **Outputs.**
  - `fn6_small_part{0,1,2}of3.{jsonl,out,json}` (per point, checkpointed);
  - `fn6_mw_{canonical,alt}.{jsonl,out,json}`;
  - `fn6_small_mutate_s{1..5}.*`;
  - `fn6_label.{out,json}`;
  - `fn6_v4x*.{out,json}`;
  - `fn6_wb.{out,json}`.
