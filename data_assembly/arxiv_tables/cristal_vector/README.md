# ALMA-CRISTAL model velocity profiles read from the paper's vector figure

`extract.py` reads `mass_profile_v4_2507.11600.pdf` (figs/mass_profile_v4.pdf of arXiv:2507.11600, ALMA-CRISTAL kinematics, z 4.4-5.7, 14 DysmalPy-modelled
disks). The PDF stores every curve as a polyline of exact vertices and all tick labels as text, so nothing is read by eye. No author was contacted; nothing is fitted.

## What each panel contains (paper's caption)
Intrinsic baryonic V_circ,bary, dark-matter V_circ,DM and total V_circ,tot **with an asymmetric-drift (pressure-support) correction**; f_DM(<R) = V_DM^2/V_tot^2 (right axis);
the intrinsic sigma_0 (red dashed line); the disk effective radius (grey dashed vertical); the folded 1D OBSERVED velocity profile (circles with error bars) and the same profile
extracted from the modelled cubes (squares).

## Validation (checks.txt)
- Every axis is calibrated from the major ticks and their printed labels, residual at most 0.004 pt; x = 0 sits at the left frame edge; the three columns share one x scale.
- **Internal, independent of the paper's table:** f_DM drawn on the right axis equals (V_DM/V_tot)^2 from the left axis to within 0.0096, and V_tot equals the quadrature sum of V_bary and
  V_DM to within 0.12%, over 0.15-8 kpc for all 14 panels.
- **Figure versus the paper's table:** sigma_0 and R_e,disk agree to the table's precision for 5 disks (03, 07a, 20, 23b, 23c). For the other 9 the figure differs from the table's posterior
  medians (one drawn model per galaxy): mostly within the table's quoted errors, but **CRISTAL-09 (R_e line 2.6 kpc vs 1.2) and CRISTAL-15 (sigma_0 67 vs 100 km/s, R_e line 0.5 vs 1.7 kpc)
  disagree beyond them.** Their curves may not be the tabulated fit.
- The 92 observed-profile markers match the 92 model-cube markers one to one once the legend symbols are removed (an earlier pass counted the legend symbol in panel 03 as a data point; fixed).

## Outputs
`cristal_curves.csv` (every curve vertex: id, curve, R kpc, value; V in km/s, f_DM dimensionless), `cristal_points.csv` (observed and model markers with error extents),
`cristal_validation.csv`, `cristal_outer_summary.csv`, `qa_replot.png` (the extracted data re-plotted, for comparison with the original figure).

## Result and what it does not say
At the outermost OBSERVED marker (R from 2.4 to 8.4 kpc) the model baryonic curve gives g_bar = V_bary^2/R below a0 (1.2e-10 m/s^2) for 7 of the 14 disks:
CRISTAL-02 0.63, -07a 0.95, -08 0.51, -12 0.60, -20 0.72, -23b 0.75, -23c 0.22 (others 1.7 to 4.7). The total (drift-corrected) model g_tot/a0 there is 0.72 (-02), 1.0 (-12), 1.3 (-20), 1.4 (-08).
**This is a model-based row, not a measurement of g_bar, for these reasons:**
1. The OBSERVED velocities (the circles) are far below the plotted V_circ: many sit at 20-100 km/s against a model V_circ of 130-320 km/s, because sigma_0 (50-110 km/s) is comparable to the
   rotation. These are pressure-supported systems whose 'circular velocity' comes from the asymmetric-drift correction.
2. The gas is [CII]-based, and in the DysmalPy model the baryonic mass is a fitted parameter constrained by the same kinematics together with a dark-matter halo, so g_bar here is not an
   independent baryon measurement.
3. The outermost observed markers rest on 1.6-5.5 beam elements per disk (table `R_out/beam`).
4. Curves beyond the outermost observed marker are model extrapolation; only values at or inside it are quoted.
5. CRISTAL-09 and -15 do not match the tabulated fit (above).
