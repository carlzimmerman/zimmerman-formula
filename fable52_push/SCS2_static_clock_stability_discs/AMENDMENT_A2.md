# SCS2 AMENDMENT A2 (post hoc; committed alone, before any graded run)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**What changes.**
1. The solver's inner radius is r_min = 1e-4 R_d (it was 0.02 R_d). The number of radial cells is scaled by
   ln(r_max/1e-4 R_d) / ln(r_max/0.02 R_d), so the spacing in ln r of every frozen grid is unchanged. The frozen 48 / 72 radial
   cells become about 72 / 107 isolated and are scaled the same way with an external field.
2. The inner boundary layer, r < 10 r_min = 1e-3 R_d, is masked in the D.P maps, in the frozen-point selection, in KA2 and in
   route 2. Route 2's domain becomes the annulus [1e-3 R_d, crop] with Dirichlet ends.
3. KA5 is computed from Gauss's law on the field at the sphere: the flux of grad Phi/(1 + u) through it, divided by 4 pi G,
   so the masked layer does not enter.

Nothing else changes: no line, grid in angle, background, known answer, MUTATE arm or label rule.

**What was seen first (post hoc).** A smoke test of the solver at log M_b 10.45, canonical, on the fine grid:
- The isolated Kuzmin and exponential discs had negative D.P only in the 3 to 8 innermost shells, at about -8e8 Msun/kpc^3.
- KA2's maximum error, 0.21, was in the innermost shell.
- Rerunning Kuzmin with r_min = 0.002 R_d moved both to the new innermost shells (0.0025 to 0.0067 R_d). They are an
  artefact of the zero-flux inner sphere with a spherical enclosed-mass source under a flat disc.
- Outside 0.2 R_d, KA2's error is 5.9e-3 (r_min 0.02 R_d) and 5.3e-3 (r_min 0.002 R_d), inside the frozen 1e-2 line.
- The same test showed negative D.P out to 224 kpc for the 0.1 a0 axial-field bracket. That is reported only after the
  graded run.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
