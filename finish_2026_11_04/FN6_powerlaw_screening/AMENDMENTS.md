# FN6_powerlaw_screening: amendments and readings

All dated 2026-11-04. The frozen criteria (`FROZEN_CRITERIA.md`, 5f0f4a5d99) are unchanged: no gate, line, grid point,
known answer or label was moved. Each item says when it was fixed.

- **Pre-grid**: written into the code before the grid ran. Only the engine tests and two test points had run:
  KA1's point (p 0, L_MW 2) and (p 0.4, L_MW 2). The test outputs are not kept.
- **Post-result**: decided after grid numbers were seen.

## Departures from "FN1b's engines unchanged" (pre-grid)

1. **T1 and T4 at small solar lengths.**
   - FN1b's exact linear response holds only when the smoothed Sun's field is far below the host field (σ = L/r_M ≫ 1).
   - FN6's Sun gets σ from 2e-4 to 6e9. KA2 itself sits at σ = 0.5.
   - Rule: the linear response where σ > 50 (FN1b's V2 and V3 checked it at 20 and 50 r_M); numeric engines at σ ≤ 50.
   - T1: KT33's `cassini_v2.quadrupole` (q_hessian; form R sets the outer width equal to the source width). This is the
     engine of FN1b's V2 and KA5.
   - T4: new code. CZ3's SO phantom monopole (verbatim) of the smoothed Sun is smoothed again by the same Gaussian,
     through the exact smeared-shell kernel (by parts, no density derivative). AZ12's orbit-averaged rate (verbatim)
     grades it.
   - Checks: V2 and V3R, numeric against the linear response at 20 and 50 r_M (max |ratio − 1| 4.9e-8 and 4.1e-9). An
     identity test at every σ used: with ν − 1 → 1, the result must equal the Sun smoothed at √2 σ (max 3e-7, line 1e-3).
2. **V1(c) not run.** It needs KT14's SO rows on all cells. It was reported only in FN1b and never changed a label.
3. **T2 graded on E1 only**, FN1b's graded field. E2, D3 and STRICT, which FN1b reported beside, are not computed.

## Readings of the frozen text (pre-grid)

4. **Dwarf mass.** Each dwarf's L comes from its own mass at each Υ_V of the scan, M = Υ_V L_V + 1.33 M_HI. This is how
   CZ2's HALF mode sets its length. The reported check K-HALF-dwarfs reproduces CZ2's HALF counts, 18 / 18.
5. **Milky Way cell mass.** Stars plus gas, KT25's width mass (KT33's `rho_cell` and `gas_mass`).
6. **SPARC mass.** KT19's Mb = 0.5 L[3.6] + 1.33 M_HI.
7. **Sun.** 1 M☉. Each gate uses its own GM, as FN1b does: KT33's for T1, AZ12's for T4.
8. **V4 (frozen lines).** Fornax at its own L for Υ_V = 1, 2 and 3, and NGC 2403 at its own L, at each grid point.
9. **V1 (a) and (b)** at the smallest and the largest cell length of each point.
10. **Convergence.** FN1b's refine-2 check, with each cell at its own L. Reported only.
11. **MUTATE design.**
    - Pooled shuffle of reference masses among the 181 systems: the Sun (1 M☉), the 24 dwarfs (M at Υ_V = 2), KT19's
      155 SPARC galaxies (Mb) and the Milky Way (the median in-prior cell mass, 6.63e10 M☉).
    - Each system's masses are scaled by M_assigned / M_reference. So the Υ scan and the spread over prior cells ride
      along.
    - **Post-result:** seeds 1–5 were chosen after the grid ran, before any MUTATE number.

## Scope beyond the minimum (post-small-grid, before any T0 number except KA1's)

12. **T0 at all 48 points per footing.** The caller allowed skipping T0 where a cheaper gate fails. Mapping it costs about
    35 s a point, so the full plane was run.

## Post-result additions (reported only; no label changed)

13. **Extended V4** (`fn6_v4x.py`).
    - FN1b's V4 lines, run on every dwarf and every SPARC galaxy at its own L, at the window points.
    - SPARC: all 155 galaxies are within 1e-3 at every window point (max 4.1e-4).
    - Dwarfs: 3 or 4 of 24 miss the line at (0.4, 1.5), (0.4, 2.0), (0.45, 2.0) and (0.45, 3.0). These are Sextans,
      Canes Venatici I, Andromeda IX and Andromeda XIV, all at small L.
14. **Dwarf grid check** (`fn6_v4x_grid.py`).
    - The missing dwarfs were recomputed on a radial grid twice as fine (n 4000).
    - V4 then passes for all but Andromeda IX at (0.45, 2.0), which reads 3.7e-3.
    - **No dwarf's pass or fail changes on either footing**, so every T2 count stands.
15. **Text fix only.** A comment in `fn6_small.py` and a printed header in `fn6_label.py` said "201 systems". The code
    built 181, because KT19's cuts leave 155 SPARC galaxies, not 175.
    - Both texts were corrected after the runs. No code changed and no output is affected.
    - `fn6_label.py` was rerun; its labels are unchanged.
16. **Wide-binary item** (`fn6_wb.py`), reported and not graded.
    - The curve is the l = 0 γ_r of a 1 M☉ point mass in form R at L(1 M☉).
    - Host field: CW1's primary, 1.9e-10, inverted to Newtonian.
    - L/r_M is held at its 1 M☉ value for every pair. It scales as M^(p − 1/2).
    - CW1's DR4 injection procedure is run against the frozen pipeline, imported read only (SHA-256 7c884e0e…, the same
      as CW1's).
