# UD1 amendments

## A1 (2026-11-04, before any rotation-curve number of this lane was read)

Found at fetch: neither Mancera Piña+2022 (arXiv:2112.00017) nor the same team's follow-up Mancera Piña+2024 (A&A;
arXiv:2404.06537) tabulates V_circ(R). Owner standing rule 11-04 ("swing harder": build the natural inputs rather than
stop at NOT EVALUABLE) applies, so §1's stop is replaced by the following. Only the lane's inputs change; the law, the
labels (§3, §4) and the checks' intent are unchanged.

- **Primary becomes Mancera Piña+2024**, which supersedes 2022 with an inclination from deep optical imaging
  (i0 = 31° ± 2°, D = 78.7 ± 1.5 Mpc). 2022 (i0 = 32° ± 3°, D = 76 ± 5 Mpc) is the secondary, never pooled.
- **Baryons** are built from 2024's published functional forms and parameters (poly-exponential stars, Σ0 3.6703
  Msun/pc², R_pex 3.6155″, c1-c4; gas Σ0 3.953 Msun/pc², R1 0.676″, R2 375.220″, α 559.231, helium included as
  published), with their vertical structure (stars sech² of stated thickness, gas Gaussian z_d 1.3 kpc), midplane
  circular speed by numerical potential. Arcsec to kpc at D.
- **V_circ points and errors** are read from the authors' own vector figure (plot_mond.pdf in the arXiv source) as exact
  path coordinates, calibrated on the axis tick labels. Not digitised by eye; a raster figure would stop the lane.
- **K0 replaced:** (a) my V_gas, V_* reproduce the plotted curves in plot_mm_noDM.pdf to 3 %; (b) the MOND curve plotted in
  plot_mond.pdf (a0 = 1.2e-10, Gentile+2008 form, which is this lane's ν) is reproduced from my baryons to 3 %; (c) the
  paper's statement that i ≈ 12° brings the data onto that curve is reproduced to ±2°. A failure of (a) or (b) means no
  clean label.
- 2022's V_circ, if its figure (vcvdisp_fixed.pdf) is vector, is read the same way; its baryons use 2024's forms (2022's
  gas parameters are not given), said so in the label.

## A2 (2026-11-04, after reading the figure geometry, before any law number)

The paper's i = 12° points are not V_circ × sin(31°)/sin(12°): it rescales V_rot and keeps the asymmetric-drift term,
and its mass models scale the deprojected baryon surface densities with cos i. §4's frozen scan (all of V_circ and its
error × sin i0 / sin i, baryons fixed) stays the graded escape. Reported beside, not graded: the paper-consistent scan,
V_circ(i)² = (V_rot sin i0 / sin i)² + (V_circ0² − V_rot0²), baryon Σ × cos i / cos i0. V_rot is read from the right
panel of plot_kinematics.pdf (vector) the same way as A1. K0(c) uses this variant, since that is how the paper made its
statement.
