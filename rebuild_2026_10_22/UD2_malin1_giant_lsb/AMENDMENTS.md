# UD2 amendments

## A1 (2026-11-04, before any baryon or law number of this lane was read)

Found at fetch: Lelli, Fraternali & Sancisi 2010 (arXiv:1003.1312) tabulates the rotation curve (Table 3: four rings at
12.5, 37.5, 62.5 and 87.5 kpc, with errors; i0 = 38° ± 3°, D_A = 322 Mpc). The baryon components are not tabulated: the
gas surface density profile and the HSB/LSB stellar profiles appear only in figures. As UD1 A1 (owner rule: build,
don't stop), §1's stop is replaced:

- **Baryon components** are read as exact path coordinates from the authors' vector EPS figures in the arXiv source.
  Each is converted to PDF with Ghostscript (-dEPSCrop, -dSAFER), and the axes are calibrated on the tick labels. A
  raster figure stops the lane.
  - **Primary:** DecoHL.eps, the HSB-LSB decomposition at the authors' preferred table values M_HSB/L_R = 3.3 and
    M_LSB/L_R = 0.9 (LSB from colours via Bell+2003, HSB maximised). Gas includes helium (×1.4) and the (1+z)⁴ dimming
    correction, as published.
  - **Reported beside:** the components of Mond2comp_malin1.eps (their MOND fit: HSB 3.7, LSB 0.5).
  - **Ends (§3):** HSB × 0.5 and × 2 (no range is published except "cannot be higher than 5" for the single-component
    model), LSB 0.5 and 0.9.
- **K0 replaced:**
  - (a) The plotted rotation-curve dots in each figure match Table 3 to 1 km/s, which checks the calibration.
  - (b) The paper's plotted MOND fit (Mond2comp, a0 = 3000 (km/s)²/kpc, "simplest formulation", standard
    μ(x) = x/√(1+x²)) is reproduced from its own plotted components to 2 %.

  A failure of (a) or (b) means no clean label.
- Components are evaluated at the Table 3 radii by linear interpolation along the extracted curve. The distance (D_A
  from H0 = 70 with a q0 term) is the published one: it is an input of the paper, not of this lane, and is said so.
- §4's frozen scan stands as written (V and errors × sin i0 / sin i, baryons fixed). The authors' remark that an outer
  inclination of 32° would match MOND is context only.
