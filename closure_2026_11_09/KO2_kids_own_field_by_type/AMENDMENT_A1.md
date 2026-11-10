# KO2 AMENDMENT A1 (post hoc: written after a model-only run of the kernel checks failed; no lensing number has been computed)

Committed alone, before `ko2.py` is changed or run on the lensing sums. It changes two known-answer definitions and the
resolution of the kernel tables. It changes no statistic, design, bracket, line or label rule.

## What happened

`ko2.py` was run in its model-only stage (`KO2_STAGE=kernels`: own columns, kernel tables, KA-2; the shear sums WG and WX are
not loaded in that stage; the weights WW and the lens catalogue were read to place realistic test cells). Output kept as
`ko2_run0_kernels_fail.out` (committed with the result), with the per-configuration detail appended. KA-2a and KA-2c passed. KA-2b and KA-2d failed. By the frozen rule that would be NO VERDICT,
so nothing past the kernel stage was run.

## 1. KA-2b: the reference was too coarse, and the tables have a real kink error

- The frozen reference draws the band as 200,000 point masses on a polar grid about the **neighbour** (500 shells x 400
  angles). When the lens circle lies inside the band, far from the neighbour, the grid spacing is comparable to the circle
  (at x 2.8, 400 angles are 0.044 apart; the circle is 0.08 across). The reference is then lumpy. In the worst far-band case
  it gives -3.4e-14 m/s^2 where the smooth tidal value is about -1e-17 (-(r^2 / 8) times the Laplacian of an x^-1 profile);
  the table gives -3.5e-18. Seven far-band failures are of this kind.
- The table also has a genuine error. J has slope breaks where the lens circle is tangent to a band edge, at r = |delta - x_e|
  and r = delta + x_e. Bilinear interpolation across a break on the frozen grid (801 x 561; steps 0.014 in ln r, 0.020 in
  ln delta) errs by up to about 0.5 % of a band's largest value in the realistic sample. The worst case is a near-concentric
  neighbour whose cell edge falls on the break: 4.3 % of that cell's value (outer band, bin 0, delta 1e-3).
- **Replacements.** (i) The reference becomes a direct quadrature of the band's surface density in polar coordinates about
  the **lens**: 4,096 angles, and radii on a log grid from 1e-4 of the cell's outer edge with 2,000 nodes up to it. The
  enclosed mass M(R) is accumulated from the circle means, and the cell average follows from the definition. It needs no
  ring decomposition, no arccos and no table. (ii) The tables are refined to 2,401 x 1,681 (steps 0.0046 and 0.0066). That
  cuts the break error by about a factor of three, at 258 MB in memory. The tolerance stays as frozen:
  |table - reference| <= 0.01 |reference| + 0.003 max|reference| of that band.

## 2. KA-2d: the expectation was wrong

- The frozen check compares the table at separation 1e-3 l with the concentric closed form, to 0.5 %, in all 13 bin-aligned
  cells. In the cells next to a band edge, an offset of 1e-3 l is not small against the cell. Next to the inner band's inner
  edge (x 0.025, cell width 0.008) it smooths the edge over 8 % of the cell. The off-centre truth differs from the concentric
  form by 5.5 % there. There the frozen reference and the table agree (both -0.651 against the concentric -0.689, in units of
  the law's cell value), so the check was wrong, not the table.
- **Replacement.** At separation 1e-3 l, cells not adjacent to a band edge must match the concentric closed form to 0.5 %.
  The cells adjacent to a band edge must match the new reference of section 1, under KA-2b's tolerance.

## 3. What has been seen

Only the kernel checks' numbers above. No WG, no WX, no amplitude, no ratio and no label has been computed. The lens-class
thresholds and counts have not been computed either; that step comes after the kernel stage.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
