# CQ1_screening_window: NO WINDOW for a tidal threshold T★ or a Vainshtein length ℓ on either footing; a fixed screening length L★ has a narrow WINDOW, [21.7, 27.0] pc canonical and [22.9, 24.6] pc alt; no vacuum combination lies in any window

κ = ½ FITTED; not theory closed. Footings are never pooled. No particle, no cold sector, no ΛCDM input. Nothing here says the data favour the framework.

Criteria are in `FROZEN_CRITERIA.md` (98d0cbbefe), committed alone before the script. Run with `OMP_NUM_THREADS=1 nice -n 10 python3 -I -B cq1.py`. It took 5 s, single thread, peak RSS 0.63 GB, and wrote `cq1.out` / `cq1.json` / `cq1.log` / `cq1.time`. The MUTATE twin wrote `cq1_MUTATE.*`. No download. No file outside this folder is edited.

The Cassini solver is CW1's `Solver`, read from `cw1_copy.py`. That file is a byte copy of CW1's `cw1.py` (SHA-256 b3be0ab9…); it is never edited and never run. CQ1 adds one line: F_r = F_θ = 0 at nodes x < rscr.

## Labels (G1–G6, the frozen line)

| family | footing | label | binding pair |
|---|---|---|---|
| (i) tidal threshold T★ | canonical | **NO WINDOW** | SPARC: T★ ≥ 2.24e-26 s⁻² > Pal 14 screened at r_h: T★ ≤ 1.40e-30 |
| (i) | alt | **NO WINDOW** | 2.98e-26 > 1.40e-30 |
| (ii) Vainshtein, T_V = c²/ℓ² | canonical | **NO WINDOW** | 2.24e-26 > Pal 14: 2.80e-30 |
| (ii) | alt | **NO WINDOW** | 2.98e-26 > 2.80e-30 |
| (iii) fixed length L★ | canonical | **WINDOW [21.7, 27.0] pc** | D10's floor against UGC 4483's 0.1 r_M |
| (iii) | alt | **WINDOW [22.9, 24.6] pc** | same |

**Vacuum scales.** No window contains a vacuum combination. Vacuum tides are at most 3.9e-34 / 5.7e-34 s⁻², even at N = 10³. Vacuum lengths are at least 3.1e7 / 2.6e7 pc, even at N = 10⁻³.

**Information only, not labels.**
- Without G3 (the globulars), (i) and (ii) open: T★ ∈ [2.24e-26, 3.99e-25] canonical and [2.98e-26, 3.51e-25] alt. For (ii) that is ℓ = 15.4–64.9 kpc and 16.4–56.3 kpc.
- With G3 at the cluster centre, or with SPARC's loose line r_screen ≤ r_M (T ≥ 2.24e-29 / 2.98e-29), (i) and (ii) stay closed.

## Part A: the bound

Mass balance makes G and ρ_Λ enter as Gρ_Λ. So every s⁻² quantity from {c, G, ρ_Λ, a0} is (Gρ_Λ)^p (a0/c)^(2−2p) × a number. On the framework's own tie, ρ_Λ = a0²/(κ²c²G), each of these is κ^(2−2p) Gρ_Λ, and every length is c²/a0 × a number.

| footing | Gρ_Λ | (a0/c)² | Λc² = 8πGρ_Λ | 32π² Gρ_Λ | Sun's saddle tide | MW 4πGρ_b | a0 / 10 kpc |
|---|---|---|---|---|---|---|---|
| canonical | **3.90e-37** | 9.75e-38 | 9.80e-36 | 1.23e-34 | 3.69e-25 (5,990 AU) / 2.49e-25 (6,826 AU) | 9.08e-30 | 3.03e-31 |
| alt | **5.70e-37** | 1.42e-37 | 1.43e-35 | 1.80e-34 | 3.38e-25 (6,167 AU) / 2.26e-25 (7,057 AU) | 9.08e-30 | 3.67e-31 |

(Saddle columns: g_e = 2.32e-10 / 1.9e-10, inverted to the Newtonian field.)

- **The hand estimate is VERIFIED.** Gρ_Λ is 0.975× and 1.42× of 4e-37.
- **NOT IN GAP on either footing.** Every vacuum tide lies below even the outskirts tide. To reach the band you would need a pure number of:
  - 7.8e5 / 6.4e5 for the outskirts;
  - 2.3e7 / 1.6e7 for the MW midplane;
  - 6.4e11 / 4.0e11 for the Sun's saddle.
- Vacuum lengths are c²/a0 = 3.1e10 / 2.6e10 pc. That is ~10⁹ times the L★ window.

## Part B: each gate's bound

| gate | canonical | alt |
|---|---|---|
| G1 Cassini, plain QUMOND at rscr = 0 | 6.06× ceiling | 6.60× ceiling |
| G1 smallest screening radius x_s,min | **0.733 r_M = 5,834 AU** (0.97 of the saddle) | **0.841 r_M = 6,093 AU** (0.99 of the saddle) |
| … tide there, 2GM/r_s³ (upper bound on T★, T_V) | 3.99e-25 s⁻² | 3.51e-25 s⁻² |
| G2 planets | Z = 0 at x_s,min; the planets alone need r_s ≥ 11 AU | same |
| G3 Pal 4 / Pal 14 at r = a: T(a) | 1.17e-29 / **1.40e-30** | same |
| G3 Pal 4 / Pal 14 at r = a: 2GM(<a)/a³ | 2.35e-29 / **2.80e-30** | same |
| G3 D10 floor (lower bound on L★) | **21.68 pc** | **22.85 pc** |
| G4 dwarfs, largest T(a) at Υ 3 / Υ 2 | 1.64e-30 / 1.09e-30 (Leo I) | same |
| G4 dwarfs, largest 2GM(<a)/a³ at Υ 3 / Υ 2 | 3.27e-30 / 2.18e-30 (Leo I) | same |
| G4 dwarfs, smallest a (upper bound on L★) | 120 pc (Leo T) | same |
| G5 MW: 4πGρ_b (B2b 0.1599; McMillan) | 9.08e-30 (6.08e-30) | same |
| G5 MW: 2g_N/R0 | 1.02e-30 | 9.50e-31 |
| G5 MW: H2 layer (upper bound on L★) | 90 pc | 90 pc |
| G6 SPARC, smallest M_b (UGC 4483, 4.91e7 M☉), r_M | 270 pc | 246 pc |
| … r_screen ≤ 0.1 r_M: T ≥ / L★ ≤ | **2.24e-26** / **27.0 pc** | **2.98e-26** / **24.6 pc** |

G3 rows are r = a for Pal 4 and Pal 14, with M = 1.6 L_V. They are the same on both footings.

The Cassini profile, q/ceiling for screening radius x_s:
- canonical: 5.41 at 0.3 r_M, 3.58 at 0.5, 1.27 at 0.7, 0.12 at 1.0;
- alt: 6.07, 4.54, 2.31, 0.30 at the same radii.

The plain value matches CW1's Solver bit for bit (K2). It is above AX1's 1.69–5.18×; CW1 puts the host's Newtonian field into ν, and that difference was not checked here.

**G7, wide binaries (report only).**
- (i) and (ii) screen a 1 / 2 M☉ binary out to:
  - 5.8 / 7.4 kAU canonical and 6.1 / 7.7 kAU alt at the Cassini end;
  - 15.2 / 19.2 kAU and 13.9 / 17.5 kAU at the no-G3 window's low end.
  - So they screen it **PARTLY**.
- (iii) at D10's floor screens to 4,470 / 4,710 kAU: it **SCREENS** them, and they are Newtonian at every separation.

## Reading
- **Cassini needs the screen to reach the Sun's saddle.** The Q2 source sits at 0.3–1 r_M. The smallest screened sphere is 0.97 / 0.99 of the distance to the point where the Sun's pull equals the Galaxy's. Any screen built on the Sun's own field must therefore be active at a tide of about 4e-25 s⁻².
- **Mass-scaled screens (i, ii) die on the globulars against SPARC.**
  - For a point mass, r_screen/r_M ∝ M^(−1/6).
  - If T★ or ℓ is low enough to screen Pal 14 at its half-light radius (5.3 / 5.8 r_M), it screens UGC 4483 far beyond 0.1 r_M. The bounds miss by 1.6e4 / 2.1e4 in T★ for (i) and 8.0e3 / 1.1e4 for (ii), i.e. a factor of 20–28 in radius.
  - Even NGC 2419's centre (4.7e-28 tidal, 9.4e-28 enclosed) lies below the SPARC line, so no outer globular can be screened anywhere in its body.
  - In (i), two other gates also collide with Pal 14 without SPARC: the MW midplane (9.08e-30 against 1.40e-30) and Leo I at Υ 3 (1.64e-30). In (ii), Leo I at Υ 3 does (3.27e-30 against 2.80e-30).
- **Without the globulars, a mass-scaled screen fits.** T★ of a few e-26 to 4e-25 s⁻² (ℓ ≈ 15–65 kpc) passes Cassini, the planets, the dwarfs, the MW midplane and the SPARC line. No vacuum number reaches it: it lies 11–12 decades above Gρ_Λ.
- **The fixed length (iii) survives, but narrowly.**
  - At D10's floor, L★ is 0.080 r_M (canonical) and 0.093 r_M (alt) of UGC 4483, so the window rests on the one-decade reading of "≪". At 0.05 r_M, both close.
  - D10's own sensitivities are quoted here, not rerun. Binary fraction 0.5 gives 25.94 / 26.99 pc, and the E-W estimator gives 25.89 / 26.75 pc. Either would close alt's window and leave canonical's open by 4 %. D10's MF-slope M/L floors (3–10 pc) would widen it.
  - The upper end scales as √M_b of the smallest SPARC galaxy.
- **(iii)'s SPARC bound is not a statement about v3s.** Embedded systems in v3s screen on L★ (D10). An isolated galaxy screens only within l_γ = L★²/2r_M, which is ≈ 0.9 pc for UGC 4483 at 22 pc. This is a reading; it was not graded here.

## As hard as a fail
- **Checks: 6/6 PASS.**
  - K0: the copy is byte-identical and the patch is one line.
  - K1: cw1.json's K3 Cassini numbers are reproduced exactly (rel 0).
  - K2: CW1's unpatched Solver gives the same plain QUMOND Q2 (rel 0).
  - K3: direct screened solves equal the tail integral, to 2.3e-14.
  - K4: per_dec 400, L 96, n_μ 128 moves x_s,min by 0.57 %.
  - K5: peak RSS was 0.63 GB.
- **MUTATE (ν ≡ 1) fails K1, as required** (exit 1). The Q2 source vanishes, so x_s,min → 0. The labels do not move. They are set by G3 against G6, not by the solver: Cassini binds no family.
- **Translations are frozen readings.**
  - G3 for (i) and (ii) is "screened at r_h". "Screened at the centre" closes too.
  - G4 uses Υ 3, the top of CZ5's grid. At Υ 2, Leo I no longer collides in (i) or (ii), but the SPARC line still closes both.
  - G6's "≪" is frozen as 0.1. The loose r ≤ r_M line still closes (i) and (ii).
- **Point-mass and Plummer tides, not full fields.**
  - The Galactic tide at the Sun (≤ 9e-30) is far below 4e-25.
  - Hosts add ≤ 1.7e-33 to the clusters.
  - SPARC uses the point-mass r_screen. For an extended disc this overestimates the screened radius, except where the local density tide is large; G5 covers the MW case.
- **Zeroing F inside r_s** keeps the outer monopole (Gauss). It moves the interior phantom onto the sphere, which the curl-free projection includes. Zeroing the phantom density instead is a different screen and was not run.

## Inputs
| input | class | source |
|---|---|---|
| a0 footings, κ = ½ | FITTED | record |
| ρ_Λ = a0²/(κ²c²G) | FRAMEWORK-NATIVE (the tie) | record |
| Cassini ceiling 5.2e-27 s⁻², g_e 2.32e-10 / 1.9e-10 | RAW / SURVEY-CALIBRATION | CW1 (Hees) |
| planets' EPM / INPOP bounds | RAW | RQ3 tolerances via CW1's `planets()` (CZ3 / AZ12) |
| Pal 4, Pal 14, NGC 2419, Pal 3: L_V, r_h,l, R_GC; Υ_V 1.6; L★ floor | SURVEY-CALIBRATION / record | D10's results json |
| 24 dwarfs: V mag, r_h, D, M_HI | RAW + SURVEY-CALIBRATION | McConnachie 2012 csv, CZ5's selection |
| ρ_b(R0, 0) 0.1599 / 0.1071 M☉/pc³, R0 8.122 kpc | SURVEY-CALIBRATION | CZ4's printed values |
| SPARC L[3.6], M_HI | RAW + SURVEY-CALIBRATION | Lelli et al. 2016 mrt, KT19's loader |
| ΛCDM inputs | none | |

## Commits
- Criteria: 98d0cbbefe.
- Script and results: this commit.
