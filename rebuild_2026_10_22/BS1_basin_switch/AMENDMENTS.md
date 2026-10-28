# BS1_basin_switch: AMENDMENTS (committed alone, before the script and before any BS1 number)

Written 2026-10-27, after reading the harnesses and the on-disk catalogues, before writing `bs1_basin_switch.py`.
FROZEN_CRITERIA.md (aabf665e07) is not edited. Each item below fixes a point the frozen text leaves open or that cannot be
implemented literally. None was chosen from a BS1 result; no BS1 number existed when this file was written.

κ = ½ FITTED. Footings never pooled. Not "theory closed".

## A1. Domain of F2's cold-gas relation

- F2 applies log f_cold = −0.69 log M★ + 6.63 to the KiDS lens catalogue, binned over 8.5 ≤ log M★ ≤ 11.0
  (`F2_outer_lensing/f2_outer_lensing.py`, `BIN_EDGES`). "Where the record has it" is read as that range.
- Inside it: M_b = M★ (1 + f_cold). Outside it: M_b = 1.2 M★ (the record's star factor).
- M★ is used as measured at the catalogue distance (no h rescaling).
- Applies to KT2017 members, to UNGC LG members other than the four CFG522 systems, and to dwarf singletons.

## A2. The SPARC galaxy's own term in M_basin

- For a matched SPARC galaxy, its own term is its own M200 exactly as CL2 computes it: SPARC M_b and the grading
  background's R1 relation (bg A 11.18/0.90, bg B 11.20/0.90). Its own KT2017 row is excluded from the Ks sum.
- Every other member uses the frozen A_c2b_refit R1 relation on Υ_K L_K (A1, A3).
- **Why:** the frozen text keeps the CL2 flag for a lone galaxy, and the basin contains the galaxy. With this term the
  alone case equals CL2 in both backgrounds, and M_basin ≥ own M200.
- **Reported variant:** the literal all-Ks sum, with the SPARC galaxy's own Ks row on the A relation.

## A3. K-band luminosities and missing entries

- **KT2017:** L_K comes from Ksmag at the group Dist (`kt2017_groups_full.tsv`), with M_K,⊙ = 3.28 mag and no
  extinction correction.
- **UNGC (LG members):** L_K = 10^KLum, the catalogue's own column.
- **Missing values:**
  - A member without Ksmag or KLum is skipped (counted; M_basin is a lower bound).
  - A matched group without Dist is treated as unmatched, so the CL2 flag is kept (counted).

## A4. LG membership set and masses

- **Members:** every UNGC row with a finite frame R < R0_data (CFG548 frame, f31 = 2/3). The distance-quality cut
  applies only to the R0_data fit.
- **Masses:**
  - MW, M31, M33 and the LMC take CFG522's baryons: 6e10, 1.2e11, 8e9, 3e9 M☉ (JSON D6, and the M33 + LMC entry).
  - Their UNGC rows are `Milky Way`, `MESSIER031`, `MESSIER033` and `LMC`.
- **Satellites:** X1 rows with host MW or M31 are LG members by frozen rule (f), whatever their R.

## A5. X1 field dwarfs to UNGC rows

- **Name map:**

  | X1 name | UNGC row |
  |---|---|
  | Aquarius | DDO210 |
  | Cetus | Cetus |
  | IC 1613 | IC1613 |
  | Leo A | LeoA |
  | Leo T | LeoT |
  | NGC 6822 | NGC6822 |
  | Pegasus dIrr | Pegasus |
  | Phoenix | Phoenix |
  | Sagittarius dIrr | Sag dIr |
  | Tucana | Tucana |
  | UGC 4879 | UGC04879 |
  | WLM | WLM |

- **Antlia B** is absent from the UNGC (2013), so it has no frame position. Its basin is itself and it keeps its CL2
  flag. Reported variant: Antlia B placed at the UNGC row of NGC 3109.
- The basin mass of a lone dwarf is the A relation on its X1 log M★, with M_b from A1.

## A6. SPARC galaxies inside the LG

- Each SPARC galaxy is matched to the UNGC by position (0.05°). If its frame R < R0_data, rule (a) applies and its basin
  is the LG. Otherwise rule (b) applies (KT2017).

## A7. CL3 variant

- L = 3.75 with CL3's per-footing threshold, as CL3 graded it: T = 12.2357 (canonical) and 12.5739 (alt).
- The lensing line is carried from CL3's committed JSON, since lensing is unchanged by construction.
- The Milky Way under this variant uses c_f(M) at L = 3.75.

## A8. R0_data error

- Bootstrap the selected (R, V_r) pairs with replacement: numpy `default_rng(20261027)`, 400 draws, straight-line
  least-squares refit each time.
- σ = standard deviation of the R0 draws.

## A9. K0 tolerance

With every basin set to the system alone:
- **CL2:** every numeric leaf of CL2's committed `S9_L4` grade (both footings) must agree within 1e-6 (absolute, or
  relative where |x| > 1), and the fail lists must be identical.
- **HO2:** the box classes and line counts must be equal, and the McMillan K_z(R0) and its z within 1e-6.
- **HO3:** the 13 field E and Z within 1e-6.

## A10. Branch for the Milky Way box

- Every X5 box cell takes the LG basin flag, because the basin uses CFG522's MW baryons, not each cell's.
- A switched cell carries the halo of its own M200 and c_f (HO2's grade).

## A11. MUTATE

- The basin flags are inverted at their source.
- K1 recomputes each system's flag independently from the basin table and compares it with the branch applied. Under
  MUTATE every applied branch disagrees, so K1 fails and the run exits 1.
