# SCS2 AMENDMENT A3 (post hoc; committed alone, before any graded route)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**What changes.**
1. The inner boundary layer of A2 is defined in cells, not in radius: the first 20 radial shells of every grid are masked,
   which puts the edge at about 0.010 R_d on the coarse grid and 0.0022 R_d on the fine one. A2's mask was r < 10 r_min.
2. For the thin discs (razor-thin exponential, Kuzmin, the disc of disc + bulge), the mass inside r_min enters as the
   sheet's flux through the inner sphere, distributed in proportion to |cos theta|, instead of uniformly over the sphere. The
   bulge and the thick disc keep the uniform share.

Nothing else changes.

**Why, and what was seen first (post hoc).**
- The first full map run under A2 failed KA4 on the isolated Kuzmin discs. On the coarse grid a few cells just outside the
  mask (r = 1.05 to 1.6e-3 R_d, on the axis and next to the plane) had D.P down to -3.8e7 Msun/kpc^3; the fine grid gave
  positive minima. One fine-grid axis cell was also negative for Kuzmin at log M_b 9.4 and for the R_d x 2 bracket.
- All of these sit at the first 1 to 3 shells past the mask. The inner-boundary error decays over a fixed number of cells
  (about 12 to 15 on either grid), not over a fixed radius.
- A direct check with both changes found zero negative cells in all 32 primary solves (2 shapes, 4 masses, 2 footings,
  2 grids), with the minimum D.P agreeing between grids within 7 %.
- Kuzmin's phantom is positive off the plane in closed form, so these cells were numerical.
- The first full map output is kept as scs2_maps_run1.json / .out.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
