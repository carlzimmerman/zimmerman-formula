# SCS3 AMENDMENT A1 (post hoc, AFTER the frozen R0-R3 axial map run; committed alone, before any A1 number)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**The frozen reading stays first.** The labels from the frozen criteria (R0-R3 for AX, the frozen 20-shell mask) are computed
and reported first, as frozen. A1 adds a second reading beside it.

**What changes in the A1 reading.**
1. **Inner mask in radius as well as in cells.** Every cell with r below the R0 grid's mask edge (the outer face of R0's 20th
   shell, about 0.010 R_d) is masked at every resolution, in addition to the frozen first 20 shells: in the maps, route L,
   route L-tilde, the region and route 2's active cells.
2. **More axial resolutions.** AX adds R4 = (243, 121) and R5 = (364, 182) (base counts, ratio 1.5 continued, same A2 radial
   scaling). The three-grid rule of section 3 runs on the finest three (R3, R4, R5); the multi-resolution error clause
   becomes max(E, |Q_inf(R3-R5) - Q_inf(R2-R4)|). "Diverging" is read on (R3-R5) and (R2-R4). Route 2 runs at R4 (and R5)
   where the block LU stays below 4 GB peak RSS; Gamma_2^2's rule runs on its finest three resolutions.
3. Everything else is unchanged: backgrounds, quantities, thresholds, lines, known answers (KA1's isolated check is extended
   to R4 and R5 with the A1 mask), MUTATE arms (M2's spike keeps 10 (h_R0/h)^2, now through R5), labels and PL's settings
   (PL keeps R0-R1 and the two-grid rule, with the A1 mask).

**Why, and what was seen first (post hoc).**
- A smoke test on one background (expo, log M_b 10.45, 0.1 a0, canonical) at R0-R3, then the frozen AX map run at R0-R3 on
  all 32 axial backgrounds and the 16 isolated primaries.
- The isolated primaries have D.P > 0 in every unmasked cell at R0-R3 (both footings).
- On 11 of the 32 axial backgrounds (all 0.1 a0 Kuzmin but log M_b 10.9 canonical, plus the 9.4 expo at 0.1 a0 and the
  9.4 Kuzmin at 0.01 a0, both footings) route L's maximum at R3 sits at r ~ 1e-5 r_e on the axis (theta ~ 1 deg), the first
  unmasked shell: the inner-boundary artefact SCS2's A3 describes, which at R3 reaches past the 20-shell mask. Its e-folding
  time is 3-26 Myr against 0.8-55 Gyr at R0-R2 on the same backgrounds. Under the frozen rule these backgrounds cannot
  converge, so the frozen AX label is expected to be NO VERDICT.
- On the other 21 (and on all 32 at R0-R2) the maximum sits at r = 0.82-1.05 r_e, theta 119-146 deg (the flank of the total
  field's null, which is on the axis at about 0.85 r_e). Gamma_L^2 grows by 2-24 % per refinement there; on some backgrounds the
  successive differences shrink (e.g. expo 9.4 at 0.01 a0, canonical: e-folding 29.6, 27.8, 26.7, 26.2 Gyr) and on others they
  are nearly constant (expo 10.45 at 0.1 a0, canonical: 1.74, 1.69, 1.63, 1.57 Gyr), i.e. R0-R3 are not yet in the
  asymptotic range there. That is the reason for R4 and R5: the 2D solves take about 1 s at R3.
- A diagnostic solve of that one background at R5 (base 364, 182) with the frozen mask put route L's maximum on the inner
  artefact (r ~ 6e-6 r_e). That is the reason for item 1. No value of route L away from the artefact was read at R4 or R5.
- Also seen: the razor-thin sheet's surface phantom minimum is negative on the smoke-test background at R0-R3 but halves with
  each refinement (-8354, -4007, -1791, -813 Msun/kpc^2), i.e. the frozen trigger for the thick-disc twin is met literally;
  the twin runs as frozen.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
