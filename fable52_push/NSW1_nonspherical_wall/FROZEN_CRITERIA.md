# NSW1 (non-spherical wall): FROZEN CRITERIA, committed alone before any NSW1 script, Lean file or graded number

**Status: FROZEN 2026-11-09.** Drafted earlier the same day on the owner's "Yes, draft it". Frozen by the lane session on the
lead session's go-ahead, which relays the owner's words in the lead session, "keep going on research bro", read together
with the standing rule of 2026-11-02 (launch search lanes without asking). That is the whole of the authority: the owner did
not review this file. Sections 12 and 13 record what was settled and what changed between the reviewed draft and this file.

TEST lane, quarantined. Adopts nothing and relabels nothing. Not registered; does not edit fable52_push/README.md, any PAPER
file, the closure register or the memory index. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), graded
separately and never pooled. A FAIL is verified as hard as a PASS. No LCDM input, no download, no new data.

Id check before writing: `ls -d fable52_push/NSW* closure_2026_11_09/NSW*` finds nothing; `git log --all --oneline | grep -i
NSW1` finds nothing; no folder named NSW1 anywhere in the checkout.

## 0. Question

SWT1's two results on a switched law were proved for a sphere around point baryons: T1 (a law-on region shows exactly M_b
from outside) and T3 (the wall pressure, with SNP1 A.1's cap F_w <= a0 M_b). Discs are flat, and SNP1's RESULT lists
"non-spherical walls" among the things it does not test. **Do T1 and the force cap survive for a flat source and a
non-spherical wall, and can any axisymmetric wall shape supply the factors the record says are missing?**

The missing factors, from the record:
- force: a shell of the 2 sigma minimum share outweighs the wall force by **3.8 / 4.9** (KO1 RESULT, bottom line item 4 and
  section 6; Lean `shell_unsupported_iff`); SNP1 A.3 puts the static shortfall at about 5 (scaling, not run);
- filling: law-on down to KiDS's lowest tabulated g_bar needs a filling of 0.29 against an allowance of 0.0231 (SWT1, x12.6),
  0.0265 / 0.0259 with external fields (EMV1, **x10.9 / x11.2**), 0.0197 with growth (GAL1, x14.7).

## 1. Record checked before drafting: what is done, what is new

- **Done.** SWT1 T1, T3 (sphere, point baryons; Lean). SNP1 A.1-A.3 (sphere; Lean). EMV1: one **spherical** bubble around
  point baryons in a uniform external field, axisymmetric nonlinear solve with the exact exterior map (emv1_solver.py); this
  already covers a non-spherical field for the filling statistic T2, not a non-spherical wall or source.
- **Done, law on everywhere (no wall).** SV1 iter_1 and QX32: flattened and elongated sources in the law's own field (QX4's
  axisymmetric solver; a Lean shell bound). They show that source shape moves shell-averaged pulls by under 0.01 dex. No wall.
- **Not done anywhere** (`git grep -il "free.boundary\|obstacle problem\|non-spherical\|oblate\|axisymmetric"` over
  fable52_push, closure_2026_11_09, closure_2026_11_06, action_search_2026_11_05, read hit by hit): a wall that is not a
  sphere; a disc source inside a wall; the wall pressure when the field meets the wall obliquely; the wall as a free boundary.
- **New here:** (i) T1 for any wall and source; (ii) the wall pressure with a tangential field, in closed form; (iii) the
  force cap for any axisymmetric wall; (iv) the filling cost of a non-spherical bubble; (v) the wall as a free boundary.

## 2. The model (no new constant)

- SWT1's class, sharp wall: div[(1 - S / (1 + u)) grad Phi] = 4 pi G rho_b, u = |grad Phi| / a0, S = 1 in Omega (law on),
  S = 0 outside (Newton). At the wall Phi and the normal flux are continuous: mu(u_in) dPhi/dn (in) = dPhi/dn (out),
  mu = u / (1 + u). Baryons only, total M_b. The cold component (cold dark energy) is not a source in the field solve; it
  enters only through the record's lines in Section 5 and as the carrier in B3.
- Units: r_M = sqrt(G M_b / a0), y(r) = G M_b / (a0 r^2). In these units the problem depends only on shape ratios (KA9).
- **Sources** (axisymmetric, symmetric about the plane): P point; E exponential disc, rho ~ exp(-R / R_d) sech^2(z / z_d),
  z_d = 0.1 R_d (SV1's late-type profile), R_d / r_M in {0.1, 0.3, 1}; K Kuzmin disc (known answers only). Disc mass outside
  the wall is dropped and the rest renormalised to M_b; this is under 1e-3 of the disc in every solved case.
- **Walls:** spheroids about the disc's axis, m^2 = R^2 + z^2 / q^2 = a^2, q = c / a in {0.2, 0.35, 0.5, 0.7, 1, 1.4, 2, 3}
  (q < 1 oblate, flattened like the disc), equatorial semi-axis a / r_M in {3, 10, 30, 100}; and the free-boundary walls of B3.
  One corner is not solved: R_d = r_M inside a = 3 r_M, where a fifth of the disc would lie outside the wall and the exterior
  would not be vacuum (every a = 3 r_M wall is inadmissible by construction, Section 5).
- At the wall: d = normal flux / a0 (continuous), e_t = tangential field / a0 (continuous), u the law's field magnitude just
  inside, n its normal part, so n u / (1 + u) = d and u^2 = n^2 + e_t^2.

## 3. Part A: exact statements to prove or refute (Lean 4 + Mathlib where algebraic; `NSW1.lean`, twin `NSW1_MUTATE.lean`)

- **A1 compensation for any shape.** The equation is in divergence form and the flux is grad Phi outside the wall, so the
  exterior monopole is exactly M_b for every wall and every source. Consequence: for a projected radius beyond the wall's
  projected extent the stacked lensing signal is that of M_b alone, at every inclination. The divergence theorem is cited;
  Lean certifies the algebraic steps; KA1 and KA3 check it numerically. Reported, not exact: the exterior quadrupole.
- **A2 wall pressure with a tangential field (new; hand algebra, to certify).** The force per unit area on whatever carries
  the switch is the integral of J over S across the wall at fixed d and e_t (SWT1 T3's identity; TPA1 item 4b's force
  density -Lam_law grad S). Claimed closed form:

      p_wall = (a0^2 / 4 pi G) W_g,   W_g = u - ln(1 + u) - n^2 / (2 (1 + u)^2).

  Limits: e_t = 0 gives SWT1's W(u); d = 0 (field along the wall) gives J's bracket u - ln(1 + u). Lean: the antiderivative
  step d/du [u^2 / 2 - d sqrt(u^2 - e_t^2)] = S(u) u / (1 + u) with S(u) = (1 + u)(1 - d / sqrt(u^2 - e_t^2)), and both limits.
- **A3 pointwise bounds.** (a) W(u) <= W_g <= u - ln(1 + u) at fixed u. (b) **To prove or refute:** W_g <= sqrt(d^2 + e_t^2),
  i.e. p_wall <= a0 |g_out| / (4 pi G) with g_out the Newtonian field just outside. (c) Deep limit, leading order:
  W_g = e_t^2 / 2 + n^2 u - u^3 / 3, which is (2/3) n^3 + e_t^2 / 2 when e_t << n.
- **A4 the cap for any wall.** If A3(b) holds, the total normal force F_n = integral of p_wall over the wall obeys
  F_n <= a0 M_b Gamma_w, Gamma_w = (integral of |g_out| dA) / (4 pi G M_b) >= 1, with Gamma_w = 1 exactly when the wall is an
  equipotential of the exterior field. Then also: the column a wall element can carry is at most a0 / (4 pi G).
- **A5 cold shells.** A thin static shell with no tangential stress (SNP1's carrier) can rest on the wall only if g_out is
  normal to it everywhere, so Gamma_w = 1 and SNP1 A.1's cap F_n <= a0 M_b holds for every shape.
- **A6 deep-limit comparison (the free-boundary mathematics).** In the deep limit the interior operator is the 3-Laplacian,
  the conformally invariant case in three dimensions, and to leading order in u the wall is an equipotential of the interior
  field. To prove or refute with the comparison principle, point source at the centre: d >= y(r_min) at the wall points
  nearest the centre and d <= y(r_max) at the farthest; and F_n = (2/3) a0 M_b times the flux-weighted mean of sqrt(d), so
  (2/3) a0 M_b sqrt(d_min) <= F_n <= (2/3) a0 M_b sqrt(d_max).
A statement that cannot be proved is listed NOT CERTIFIED with its numerical check beside it; a refuted one is listed REFUTED
with the counterexample. The twin carries false versions (wrong power of 1 + u, tangential term dropped, a false bound) and
must fail to compile.

## 4. Part B: numbers

- **B1 solver.** Coordinates fitted to the wall: x = m X_w(mu), the wall is the surface m = 1 and is sharp (S = 1 inside).
  Axisymmetric finite volume in ln m and mu on Gauss-Legendre cells (EMV1's layout) with the cross terms of the oblique
  metric; Newton on the discrete residual. Exterior: Laplace with the exact Dirichlet-to-Neumann map on the wall itself, in
  the confocal spheroidal harmonics whose coordinate surface is the wall (the sphere is the limit); for B3's walls, which are
  not spheroids, the exterior multipole series collocated on the wall. Point baryons: the Newtonian flux through a small inner
  surface (y >= 1e6 on it). Discs: mass deposited in cells. Law-everywhere reference for each source in the same coordinates,
  the monopole flux imposed on a far outer surface; QX4's aqual.py as an independent cross-check of one disc reference.
  Smooth walls, S = (1 - tanh((m - 1) / w)) / 2 with w in {0.04, 0.02, 0.01} extrapolated to w = 0, are used only for the
  second force route and the virtual-work check (KA1, KA7). The production grid is fixed by the known answers before any
  graded number.
- **B2 per case (source x wall), per footing:** exterior monopole and quadrupole; d, e_t, u, n along the wall; F_n and the
  dilation moment, the integral of p_wall (x . n) dA, by the surface route (A2's closed form on the sharp wall); the largest
  column p_wall / |g_out| in units of a0 / (4 pi G); Gamma_w; the in-plane field against the law-everywhere reference; the
  orientation-averaged lensing signal against the reference, in annuli of 0.05 dex from 0.1 r_M (for an isotropic
  distribution of orientations the stacked signal is exactly the projection of the spherically averaged effective mass:
  baryons, phantom density and wall layer); the linear polarizability along the axis (m = 0) and across it (m = 1) from the
  tangent problems of the converged state in a uniform external field, and its orientation mean
  alpha_bar = (alpha_par + 2 alpha_perp) / 3 times the bubble's volume V.
- **B3 free boundary (Bernoulli problem).** Sources E. The wall is the surface on which p_wall equals a uniform exterior
  pressure: mean-density cold component with dispersion 17.5, 35, 52.5 km/s at z 0 (SWT1 E3's bubbles, p = RHO_D0 sigma^2
  with swt1.py's RHO_D0), M_b at KiDS's four bins. Start from SWT1's sphere, move each wall point along its normal by
  (p_wall - p_ext) / |dp/dn|, stop at |p_wall / p_ext - 1| <= 1e-3 everywhere. Report the shape, the volume against the
  spherical bubble, and B2's statistics.

## 5. Statistics and lines (per footing)

- **Reach.** R_len = the largest projected radius out to which the orientation-averaged lensing signal stays within 10 % of
  the law-everywhere reference. The reference sphere of a case is the spherical wall around point baryons with the same R_len.
- **Admissible** (discs untouched): the in-plane field, extrapolated to a sharp wall, is within 5 % of the law-everywhere
  reference at every R <= 9 r_M (HE1 G1's 10 r_M, less a margin for the wall itself). Inadmissible cases, which include
  every a = 3 r_M wall by construction, are listed and take no part in the label.
- **Gamma_F = F_n(case) / F_n(reference sphere):** the force available at equal reach. **Line 3.8 / 4.9** (KO1).
- **Gamma_C = [V |alpha_bar|](reference sphere) / [V |alpha_bar|](case):** the gain in the lensing allowance at equal reach,
  through SWT1 T2's Maxwell-Garnett sum with orientation-averaged inclusions. **Line 10.9 / 11.2** (0.29 over EMV1's allowance).
- Reported beside them: F_n in a0 M_b, Gamma_w, the largest column in M_sun / pc^2, the same ratios against the sphere of
  equal volume and of equal equatorial radius, and every statistic for the inadmissible cases.

## 6. Labels (per footing)

- **CAP LIFTS:** some admissible case has Gamma_F at or above its line, or Gamma_C at or above its line. This reopens a route;
  it passes no gate of the theory, and a follow-up lane would have to put the carrier in (HE1's envelope on the lifted shape).
- **CAP HOLDS:** every admissible case has Gamma_F < 2 and Gamma_C < 2. Then the spherical numbers of SWT1, SNP1 and KO1
  stand for flat geometry to within a factor of two, and SNP1's untested item "non-spherical walls" is closed.
- **PARTIAL:** some admissible case has a ratio of 2 or more and none reaches a line. Reported with the case; not enough.
- **NO VERDICT:** a known answer fails, or A2 is neither certified nor matched by KA6 and KA7.
- A3(b), A4 and A6 are stated CERTIFIED / NOT CERTIFIED / REFUTED beside the label and do not enter it.

## 7. Known answers (must pass)

- KA1 compensation and the sphere: (a) the exterior effective mass is M_b to 1e-6 in every solved case; (b) sphere, point
  baryons, at swt1.json's six KA_W1 values of y: the interior is nu(y) to 1e-6 and the surface route gives 4 pi a^2 p_wall
  equal to the 'closed' values to 1e-8; (c) the volume route (integral of J |grad S| through the smooth wall, w -> 0) gives
  the same force to 2e-4 at y = 1e-3, 0.1 and 1.
- KA2 polarizability of the sphere: SWT1's alpha_law (transcribed) reproduces EMV1 RESULT's printed alpha_law at its eight
  canonical walls to the printed digits; the m = 0 and m = 1 responses of a spherical wall equal alpha_law to 1e-3 at
  y_w = 1e-4, 1e-3, 1e-2, 0.1 and 1.
- KA3 Newtonian limit (y >= 1e5 everywhere inside): the field is the source's Newtonian field to 1e-4 for every shape, and
  F_n / (a0 M_b Gamma_w) is within 2e-3 of 1, Gamma_w by quadrature of the Newtonian field (SWT1 KA-W2's limit).
- KA4 Kuzmin disc of scale r_M, law everywhere: g = nu(|g_N| / a0) g_N (Brada and Milgrom's exact solution) to 2e-3 at
  radii 0.5 to 20 r_M and heights of at least 0.3 r_M.
- KA5 linear spheroids, mu = 0.1, 0.5, 2, q = 0.2, 0.5, 2: alpha_par and alpha_perp against the depolarization closed forms
  to 1e-3 (tests the fitted coordinates, the exterior map and the m = 1 response).
- KA6 oblique planar wall: A2's closed form against the quadrature of J over S on a 5 x 5 grid of (d, e_t) from 1e-3 to 1e2,
  relative 1e-8; and against differencing the full Lagrangian of a slab in a uniform oblique field (SWT1 KA-W3's method), 1e-5.
- KA7 at q = 0.5 and 2, a = 3 and 10 r_M, point baryons: the surface route and the volume route (w -> 0) agree on F_n and
  on the dilation moment to 1e-3; and virtual work (the full Lagrangian differenced under a dilation of the smooth wall at
  fixed sources, w = 0.02) agrees with the volume route's dilation moment at the same w to 1e-2.
- KA8 convergence: every Gamma of an admissible case moves by under 2 % between the production grid and one refined by 1.5
  in both directions. The production grid may be refined before the graded run until this holds; the grids used are stated.
- KA9 scale symmetry: two masses at the same a / r_M, q and R_d / r_M give the same ratios to 1e-6.
- KA10 the whole chain on a sphere: for q = 1 and point baryons at a = 10, 30, 100 r_M the solver's orientation-averaged
  signal equals the closed form (nu inside, the layer at the wall) to 2e-3 at R <= 0.8 a, and Gamma_F and Gamma_C equal 1
  to 1e-2.

## 8. MUTATE (separate output files; each must fail)

- M1 tangential term dropped (W(u) at the full magnitude u in place of W_g): KA6 and KA7 must fail at oblique incidence.
- M2 flux condition mutated (dPhi/dn continuous, EMV1's M-FLUX): KA1's exterior mass must leave M_b.
- M3 sign of the S J term flipped: the force is inward on every wall element.
- M4 power check, the gate must be able to fire: a planted thin linear insulating disc (q = 0.05, mu = 0.01), graded at equal
  equatorial radius, must return Gamma_C >= 5 through the same pipeline.
- Lean twin, as in Section 3.

## 9. Disclosure: what I read and estimated before drafting

Read: the FROZEN_CRITERIA, RESULT and amendment of SWT1; the RESULT of SNP1 and EMV1; the FROZEN_CRITERIA of HE1 and TPA1 (for
format; their folders are not touched); KO1 RESULT sections 5 and 6; the heads of SV1, QX32 and QX4's solver; emv1_solver.py's
header. **No NSW1 number has been computed, no script written, no solve run.** Everything below is hand algebra, unverified.

- A1 follows from Gauss's law in one line; I expect it CERTIFIED.
- A2's closed form: integration by parts of J dS at fixed d and e_t. Both limits checked by hand; not checked numerically.
- A flattened wall at fixed equatorial radius raises F_n roughly as 1 / q in the deep regime, because the flux leaves through
  the near faces: it is the force of a nearer wall. At equal reach I expect **Gamma_F between 0.7 and 1.5**.
- A thin insulating disc costs (8/27) a^3 in V |alpha_bar| against 2.09 a^3 for its circumscribed sphere, a factor 7.1 at
  equal equatorial radius. But a thin bubble does not keep the law's field in its own plane beyond about its half-thickness
  (tangential continuity hands the plane the exterior Newtonian field). At equal reach I expect **Gamma_C between 0.5 and 2**.
- Source flatness enters as (R_d / a)^2: under 1 % for a >= 10 R_d. I expect cases E and P to agree for a >= 10 r_M.
- Column bound a0 / (4 pi G): about 53 / 65 M_sun / pc^2.
- **Expected label: CAP HOLDS / CAP HOLDS**, with A3(b) the statement most likely to come out NOT CERTIFIED. Three hand
  estimates in this push were wrong before their runs; this one is to be distrusted in the same way.

## 10. What the lane does not decide

- Formation and dynamics (SNP1's question), non-axisymmetric walls (bars, triaxial shapes), several galaxies at once.
- The cold component's own gravity on the field (exterior vacuum here), and any carrier other than B3's uniform pressure.
- The v3s stiffness and screening terms (gamma_L = 0, mu_K term dropped, as in SWT1).
- External fields beyond linear response (EMV1 did the sphere).
- KiDS itself: no shear data is read. Whether discs carry the law's field to Mpc radii is KO2's question.

## 11. Operational

One thread (thread variables set to 1, nice 10), preemptible (checkpoint after every solve, yield on SIGTERM), not started
while a 1024^3 run is live. My count: a few hundred nonlinear axisymmetric solves with their linear response problems, tens of
minutes to a few hours (an estimate, not timed). Files: nsw1.py -> nsw1.json / .out; nsw1.py --mutate M1|M2|M3|M4 ->
nsw1_MUTATE_<arm>.json / .out; NSW1.lean, NSW1_MUTATE.lean, compile.txt, compile_MUTATE.txt (no home paths); RESULT.md (label
first, then Part A's table, then the ratios per case). Commits with explicit paths only. A known answer that fails, or a frozen
line that turns out wrong, is handled by an amendment file committed alone before the next run; this file is not edited.

## 12. Choices settled at freeze

The draft left six choices open. They were settled by the lead session as drafted, not individually by the owner:
1. Tolerances: 10 % for the lensing reach, 5 % inside 9 r_M for admissibility.
2. Lines 3.8 / 4.9 and 10.9 / 11.2; the factor 2 under which the label reads CAP HOLDS.
3. Families: q from 0.2 to 3, a from 3 to 100 r_M, R_d / r_M from 0.1 to 1.
4. B3's free-boundary walls enter the label.
5. The lane does not wait for HE1 or KO2.
6. Folder: fable52_push/NSW1_nonspherical_wall.

## 13. Changes between the reviewed draft and this file (made at freeze, before any script or number)

Made by the lane session while working out how the frozen statements can be computed. None of them touches the question, the
field equation, Part A's statements, the statistics, the tolerances, the lines, the labels, the MUTATE arms or Section 9.
- B1: the wall is sharp, in coordinates fitted to it, with the exact exterior map on the wall. The draft had a smooth switch
  on a spherical grid extrapolated in its width, which cannot give the fields at the wall (d, e_t, u, n) directly. Smooth
  walls are kept for the second force route and the virtual-work check only.
- B2: the orientation average of the lensing signal is taken exactly through the spherical average of the effective mass;
  the draft had eight inclinations. The annuli (0.05 dex from 0.1 r_M) are now stated.
- Section 2: one family corner is not solved (R_d = r_M inside a = 3 r_M), and disc mass outside the wall is dropped.
- Known answers restated for the sharp wall: KA1 (compensation now in every case; the volume route to 2e-4), KA2 (a grid of
  y_w, both responses), KA3 (y >= 1e5, since at 1e4 the law itself departs from Newton by 1e-4), KA4 (scale and radii
  stated), KA7 (a = 3 r_M added; virtual work against the volume route at the same width, to 1e-2), KA8 (grid refinement in
  place of the wall width), KA10 (new: the chain on a sphere).
- Section 11: the solve count.

Hand statements made between the draft and this freeze, unverified, entering nothing above; Section 9 is left as drafted:
- The lead session re-derived A2's closed form by hand, independently, and it agrees.
- A hand proof of A3(b) was found: with t the squared cosine of the angle between the interior field and the normal,
  |g_out|^2 - W_g^2 is concave in t and non-negative at t = 0 and t = 1. Section 9's expectation that A3(b) is the statement
  most likely to come out NOT CERTIFIED is therefore already doubtful.
- In B3 the wall's size in r_M is fixed by the dispersion alone (hand: about 100 to 220 r_M), so a disc's imprint on the
  wall's shape is of order (R_d / a)^2, at most 1e-4, below B3's own stopping line. B3 is expected to return spheres.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
