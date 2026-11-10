# SCS2 RESULT: is the static clock stable around discs?

TEST lane. Adopts nothing. Not registered. kappa = 1/2 FITTED; not theory closed. Footings canonical (a0 9.3603e-11 m/s^2)
and alt (1.1312e-10) are reported separately and never pooled. Criteria 158c4cf770; amendments A1 847f24db0b (before any
number), A2 cb6ac0fe9a and A3 ac13205c89 (post hoc, before any graded route), A4 3cf66462aa (post hoc, after the graded
frozen-fit route-1 run).

## Labels (canonical / alt)

| Family | Label | Reading |
|---|---|---|
| **Isolated discs**: razor-thin exponential and Kuzmin at log M_b 9.4, 10.45, 10.7, 10.9; thick disc; disc + bulge; R_d x 0.5 and x 2 | **STABLE / STABLE** | D.P > 0 in every cell, on both grids. No growing mode on either route. |
| External field along the axis (0.01 and 0.1 a0; 2D) | **NO VERDICT / NO VERDICT** | Unstable in regions on both routes and both grids. The magnitudes are not converged. |
| External field in the plane (0.01 and 0.1 a0; 3D, one grid) | **NO VERDICT / NO VERDICT** | Unstable in regions on both routes. There is only one grid. |

The labels are read off the outputs by scs2_labels.py (scs2_labels.out).
- **Isolated discs.** Every graded known answer passes. KA1's frequency test passes with A4's fit (1.2e-3) and fails with
  the frozen fit (3.9 %); see the disclosures.
- **External-field families.** NO VERDICT because a known answer fails: KA4's two-resolution clause fails on the
  magnitudes for 22 of 32 axial backgrounds (the sign agrees on all 32), and the 3D grid has only one resolution. In
  addition, route 2's literal pencil tolerance is cleared on only 18 of 48 coarse rows, although every one of the 48 is
  negative (section 5).

**What it means for form B's disc halo.**
- Form B's static state around an isolated disc is linearly stable with gravity coupled. The clock's gradient coefficient
  is G = n_d + D.P (SCS1). With no dust of its own it is the law's phantom density, and this lane finds that density
  positive everywhere around every isolated disc it solved, from the edge of the masked core (0.002 R_d on the fine grid,
  0.01 R_d on the coarse) out to 1000 R_d.
- So nothing grows, at any wavenumber, in any direction, for m = 0, 1, 2. The disc case that SCS1 left open is closed for
  isolated discs, in the linear sense and for these disc models.
- Negative phantom density, and with it growth, appears only when a uniform external field is imposed. Form B does not use
  that effect for hosted dwarfs, so the external-field brackets bound what the action's static state would do in a field.
  They are not form B's prediction.
- Where it is negative:
  - in a band around the plane through the disc perpendicular to the external field, outside about r_e = sqrt(G M a0)/g_e
    (closed form below, Lean-checked);
  - at the null of the total field on the axis, about 0.75 to 1 r_e from the disc, on the side where the disc's pull
    opposes g_e.
- The growth there is slow: e-folding 0.9 to 2.4 Gyr at 0.1 a0 and 27 to 75 Gyr at 0.01 a0 (route 2). It is bounded in
  wavenumber at gamma_L = 0; with the stiffness on, the rate rises with k^2 (Lean).

## 1. The covariant symbol on a general background (item 1)

SCS1's full covariant 3+1 symbol (its Hessian rebuilt from its committed source, copied, not imported) was compared with
the hand closed form

    omega^2 = G (1 - K m)/m,   G = div Pbar = tr H/(1+u) - g.H.g/(a0 |g| (1+u)^2),   m = khat.J''.khat,
    J''_par = 1/(K (1+u)^2),  J''_perp = 1/(K (1+u)),

on 6 generic backgrounds with no symmetry (ln N a random cubic in x, y, z), along, across and oblique to the field, at kr
1e3 and 1e5.
- **Agreement:** 36 frozen rows, maximum relative difference 5.28e-6 (line 1e-3), with the same sign throughout: **PASS**.
- **Negative-G check:** none of the six frozen seeds has G < 0, so the same seeds were also run with H negated (seeds 7-12,
  an addition beyond the frozen list). All six then have G < 0, and those 36 rows agree too (5.28e-6, same sign).

So the gradient coefficient is isotropic: G = n_d + D.P, whatever the background. The kinetic coefficient m is
anisotropic, but positive and below 1/K in every direction (Lean: aniso_kinetic_pos, Km_lt_one). At mu_K = 0, omega^2 has
the sign of G (Lean: sign_omega2). The stability condition is therefore G >= 0 almost everywhere, as the criteria stated.

## 2. Backgrounds

The law's static AQUAL equation div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho_b, with mu(x) = x/(1+x), was solved by
finite volume on (ln r, theta[, phi]) with Picard iteration. Residuals were 4e-9 to 9.4e-9 (line 1e-8).

**Disc models.**
- Scale lengths: R_d = R_50/1.678 with Shen et al. 2003's late-type R_50(M), **quoted from memory, not downloaded**.
- Thickness: h_z from Bershady 2010.
- Bulge: B/T = 0.2, a_b = 0.2 R_d.

**Grids.**
- Fine 72-107 x 36 and coarse 48-72 x 24, extended by A2 to r_min = 1e-4 R_d with the same ln r spacing. The first 20
  shells are masked (A3).
- r_max is 1e3 R_d when isolated, and max(1e3 R_d, 10 r_e) with an external field.
- The 3D in-plane field runs on the frozen coarse grid only (about 72 x 16 x 16 over a quarter of the sphere, using the
  mirror symmetries).

**What the external-field bracket represents.** The disc sits in a uniform field g_e, and the field enters only through
the law's own nonlinear equation and its linearised far field at r_max. That is the law's external-field effect at the
level of the static state. In form B as the decision file states it, hosted dwarfs do not use it. Here it is a bracket on
the action's static state in such a field, not a graded form-B row.

## 3. Where D.P is negative (maps)

From scs2_maps.json, which uses the frozen threshold D.P < -1e-6 max|D.P|.

| Family | Negative off-plane cells | Q_neg/Q_pos | Where |
|---|---|---|---|
| Isolated (all 40 per footing, both grids) | **0** (sheet cells positive too) | 0 | none; min D.P +25 to +450 Msun/kpc^3 |
| Axis field 0.01 a0 | 41-260 | 0.037-0.137 | r = 0.75-2.7 r_e, theta 64-168 deg |
| Axis field 0.1 a0 | 484-734 | 0.105-0.227 | r = 0.76 r_e out to the grid edge, theta 2-173 deg |
| Plane field 0.01 a0 | 211-579 | 0.38-0.48 | r = 0.86-8.9 r_e, around the disc's axis |
| Plane field 0.1 a0 | 1157-1779 | 0.77-0.91 | r = 0.72 r_e out to the grid edge |

The negative regions have two sources, both read off the maps and the closed form.
- **The far field.** The solver's own boundary data is the linearised external-field potential, Phi = g_e x_par - A/s with
  s = sqrt(r_perp^2 + x_par^2/(1 + L_e)), L_e = 1/(1 + g_e/a0). For it,

      K D.P = -L_e A [r_perp^2 - 2 x_par^2/(1 + L_e)] / ((1 + L_e) s^5)

  (sympy-exact in scs2_farfield.py; signs in Lean: farfield_band_negative, farfield_cone_positive). It is negative in the
  band r_perp^2 > 2 x_par^2/(1 + L_e) around the plane perpendicular to the field, and positive in the cones along it. In
  the solved axial maps at r >= 3 r_e, by sign alone:
  - at least 93 % of negative cells lie inside the band;
  - at least 88 % of band cells are negative;
  - at least 86 % of axis-cone cells are positive.

  At 0.01 a0 the far field lies below the frozen magnitude threshold, so the thresholded counts there are zero.
- **The null.** Within 3 r_e the negative charge sits around the null of the total field, on the axis on the side where
  the disc's pull opposes g_e, and next to it.

**Resolution (KA4's clause applied to every background with a coarse twin, scs2_resolution.py).**
- All 72 twins agree on the sign of the map.
- The isolated ones agree on everything: zero negative charge on both grids, minimum D.P within 7 %.
- The 32 axial external-field twins agree on the sign everywhere, but not on the magnitudes:
  - the charge fraction is within 20 % on 26 of 32 (worst: 0.186 fine against 0.354 coarse, alt Kuzmin 9.4 at 0.1 a0);
  - the minimum D.P is within 20 % on 15 of 32 (the coarse grid is 20 to 35 % shallower).

  **KA4 therefore fails for the external-field family**, and the label rule makes that family NO VERDICT.

## 4. Route 1 (WKB symbol at frozen points)

Route 1 is the full covariant symbol (SCS1's Hessian, Hermitian part) and the hand form at the frozen points of every fine
background, along, across and azimuthal to the local field, at kr 10, 1e3 and 1e5. The points per background:
- up to 3 most negative cells;
- up to 3 cells at a sign change;
- 4 references: two cells above the plane at R_d and at 3 R_d, the axis cell at R_d, and 45 degrees at 3 R_d.

Phi's derivatives come from a local cubic fit on a 5 x 5 (x 5) stencil. The labels use the **A4** fit (in ln r, theta[,
phi]); the frozen fit (in R, z) is kept beside it.

| | A4 fit (graded) | Frozen fit |
|---|---|---|
| KA1 vs SCS1 | 1.2e-3 **PASS** | 3.9e-2 **FAIL** |
| Symbol against hand, kr >= 1e3 | max 3.0e-3 | max 6.8e-4 |
| Fit G against grid D.P at the reference points | 0.98-1.02 (isolated); 0.99-1.03 (axial field) | 0.95-1.08 |
| **Isolated discs, growing rows** | **0 / 720 per footing** (symbol and hand) | 0 / 720 per footing |
| Axial field, growing rows (canonical / alt) | 702 / 666 of 1440 | 594 / 576 of 1440 |
| Plane field (3D), growing rows | 99 / 135 of 720 | 288 / 288 of 720 |

**Where it grows (A4, axial field), e-folding time:**
- 0.1 a0: 1.1 Gyr upward. At least 0.77 of the local free-fall time 1/sqrt(4 pi G |rho_loc|) and at least 3.8 r/v_c.
- 0.01 a0: 31 Gyr upward. At least 5.4 free-fall times and at least 12 r/v_c.
- At every growing row the symbol's omega^2 is the same at kr 1e5 as at kr 1e3, to 5 digits. The growth is **bounded in
  k** at gamma_L = 0, as the hand form says.
- With the stiffness on, omega^2 = G (1 + gamma_L m k^2 - K m)/m falls without bound in k^2 wherever G < 0 (Lean
  stiffness_unbounded). That was not evaluated numerically here; it is a hand-form bracket, as frozen.

**Route 1's weak spot: the cells where D.P is most negative.**
- They sit at the null of the total field, where the field turns over across the stencil.
- There the fit's G is only -0.16 to 0.65 of the grid's D.P on the axial backgrounds (same sign at 23 or 24 of 24 points
  per footing and field strength).
- On the coarse 3D grid it is -0.30 to -0.15 under A4: the opposite sign at all 12 points. Under the frozen fit it is
  0.12 to 0.24, same sign.
- So route 1's rates at those cells are not quantitative. Route 2, which uses the grid's D.P directly, and the maps carry
  the external-field regions.


## 5. Route 2 (global)

**Axisymmetric backgrounds.** The constraint-surface pencil L_G zeta = lambda H zeta with H > 0. By Sylvester's law of
inertia, the number of negative lambda equals the number of negative eigenvalues of L_G.
- Dense generalized eigensolves (n <= 3000) for m = 0, 1, 2 and both parities.
- On the fine external-field grids (n > 4000): the inertia of L_G at m = 0; m = 1, 2 are carried by the coarse grid.
- ARPACK did not converge on these pencils. That is why dense solves and inertia replace the frozen sparse eigensolve.

| | canonical | alt |
|---|---|---|
| Isolated, 240 rows (120 fine, 120 coarse) | every lambda_min > 0: 8.46e-13 to 1.02e-10 kpc^-2; L_G positive definite | 8.44e-13 to 1.01e-10 kpc^-2 |
| Point mass (KA1), 6 rows | 7.46e-12 | 7.42e-12 |
| Axis field, fine, m = 0 (16) | L_G negative on 16/16 (L_G min/max -7.9e-7 to -5.5e-5) | 16/16 (-7.7e-7 to -5.7e-5) |
| Axis field, coarse, 48 rows | lambda_min < 0 on 48/48: 0.01 a0 -1.9e-15 to -1.1e-14 kpc^-2 (e-fold 32-75 Gyr); 0.1 a0 -1.8e-12 to -1.0e-11 (1.0-2.4 Gyr) | 0.01 a0 -2.5e-15 to -1.4e-14 (27-65 Gyr); 0.1 a0 -2.3e-12 to -1.4e-11 (0.88-2.2 Gyr) |
| Plane field (3D, coarse), 16 rows | Rayleigh numerator zeta.L_G.zeta < 0 on 16/16 (checkerboard on interior negative cells; LOBPCG lowest negative at 0.1 a0) | 16/16 |

**The frozen pencil tolerance.** It reads "no lambda < -1e-10 max|lambda|", and on the coarse axial rows it is cleared on
only 18 of 48 (6 canonical, 12 alt).
- The largest |lambda| is the stiffest mode of the innermost cells (2e-2 to 7e-2 kpc^-2). The negative modes live at
  r ~ r_e, up to 1e5 times farther out.
- The negative eigenvalues are real, not rounding. L_G's own inertia is negative with margin 1e4 to 1e5 over the same
  relative tolerance, and Sylvester fixes the count. They are also smooth across m, shape and mass.
- Read literally, though, the routes "disagree" on 30 coarse rows. That is a second reason the external-field family is
  NO VERDICT under the frozen rule.

## 6. Known answers

| | Result |
|---|---|
| KA1 point mass (map, both routes) | D.P > 0 in every cell; route 2 lambda_min 7.4e-12 kpc^-2 > 0; route 1 no growing row. **PASS** |
| KA1 frequencies vs SCS1 (log M_b 10.45, 30 kpc, kr 1e3) | Frozen fit: omega^2 r^2 3.9 % above SCS1's in every direction and on both footings, **FAILS** (line 1e-2). A4 fit: 1.1167e-7 against 1.1154e-7 radial and 4.9838e-8 against 4.9785e-8 tangential (canonical); max 1.2e-3 over both footings and three directions. **PASS** |
| KA2 Kuzmin closed form | max relative error of |grad Phi| 6.6e-3 (line 1e-2). **PASS** |
| KA3 planar slab = TPA1 | 144 rows, relative 1.7e-15; e-folds 5.03e6 to 6.25e8 yr. **PASS** |
| KA4 residual and two resolutions | Residual max 9.9e-9. Graded on the primaries (both zero): **PASS**. Applied to every twin: isolated 40/40, external field along the axis 10/32 (magnitudes; sign 32/32): **FAILS for that family** |
| KA5 phantom mass | Point mass 7.0e-13 / 6.4e-10 (line 1e-3); discs at 30 R_d, max 1.6e-2 (line 2e-2). **PASS** |
| Item 1 | 5.28e-6 (line 1e-3). **PASS** |

## 7. MUTATE (separate outputs)

Route 2 ran on 10 backgrounds: the primaries at log M_b 10.45 (both shapes and footings, both grids) and the 0.1 a0 axial
bracket (coarse, both footings). Route 1 ran at the frozen points of the same primaries plus the 0.1 a0 axial bracket
(fine), with the A4 fit (scs2_wkb_MUTATE_{M1,M2,M3}_A4.json).

| Arm | Route 2 | Route 1 | Bites? |
|---|---|---|---|
| **M1** tilt sign flipped (G -> -D.P) | Isolated: L_G negative on 48/48, lambda_min -2.2e-2 to -2.9e-1 kpc^-2 (stable -> unstable). Axial field: still negative, because the bulk of positive D.P becomes negative. | Isolated: 144/144 rows grow. Axial field: all 90 rows that grew in the A4 main run stop growing (unstable -> stable) | **BITES** (both directions) |
| **M2** planar divergence (along-field part only) | Isolated: L_G negative on 48/48, lambda_min -3.7e-7 to -1.1e-6 kpc^-2 (stable -> unstable) | Isolated: 144/144 rows grow | **BITES** |
| **M3** decoupled (no clock-metric mixing) | lambda_min changes by a factor 7.3 to 10.3; no sign flips (isolated 48 rows stay positive, axial 6 stay negative) | omega^2 changes by at least 2.2e-2 on all 324 rows; no sign flips | **BITES** |

The frozen-fit route-1 MUTATE runs (scs2_wkb_MUTATE_{M1,M2,M3}.json) give the same pattern on the isolated discs: M1 and M2
make 144/144 rows grow, and M3 makes 0/144 grow.

## 8. Lean (fable_independent_2026/lean_2026)

SCS2.lean compiles with exit 0; all 13 theorems depend only on the standard axioms (propext, Classical.choice,
Quot.sound): lagrange3, aniso_kinetic_pos, Km_lt_one, sign_omega2, quotient_neg, quotient_nonneg, nu_antitone,
law_solves, far_field_exponent, kuzmin_sheet, stiffness_unbounded (SCS1's statement, copied), farfield_band_negative,
farfield_cone_positive. SCS2_MUTATE.lean holds 7 false versions with the true proofs; each fails (7 errors, exit 1). The
last four true theorems and the last two false ones were added after the first compile, to cover the criteria's Lean list
(the stiffness form and the Rayleigh sign) and the far-field band found in the maps. compile.txt and compile_MUTATE.txt are
the recompiles of the whole files.

## 9. What this does not settle

- **The nonlinear outcome.** Where the external-field brackets grow, nothing here says what the growth turns into:
  saturation, a reshaped halo, or a clock that leaves the static branch. The isolated label is linear stability only.
- **The collapse.** Whether a free-falling clock reaches this static state at all is untouched (FB1 item 2 stays open).
  Stability of an end state is not a path to it.
- **Real disc structure.** These are smooth axisymmetric discs at four masses. Spiral arms, bars, gas, warps, a
  non-exponential profile, satellites, and a disc whose own baryons evolve are not modelled. Scale lengths come from a
  relation quoted from memory. A disc in a group or cluster sits in an external field, which is the regime that is NO
  VERDICT here.
- **The cosmological background.** Not addressed. At the mu_K the CMB needs, SCS1 found the static state Jeans-unstable at
  the free-fall rate; this lane keeps mu_K = 0 throughout.
- **Approximations.** Newtonian order, quasi-static metric, WKB with frozen coefficients at points (route 1), and the
  constraint-surface pencil with the J''_r-theta cross term dropped (route 2: the face weights use J''_rr on r-faces and
  J''_theta-theta on theta-faces). Dropping that term keeps H positive by construction and leaves L_G's inertia, which
  carries the verdict, unchanged. It does change the size of each lambda.

## 10. Anything wrong in SCS1, TPA1 or FB1

- **SCS1 and FB1** say that around flattened systems "the law's phantom density can be negative in places", and FB1
  carries the disc case as the open stability item.
  - For **isolated** discs that is not what the law does here: D.P is positive everywhere around every isolated disc
    solved (razor-thin, Kuzmin, thick, with bulge, R_d x 0.5 to 2, four masses, both footings). For Kuzmin it is also
    positive in closed form.
  - Negative phantom density appears here only with an external field: in the far-field band and at the null.
  - So the open item should read "discs in an external field", not "discs".
  - Neither file is edited.
- **TPA1** (gradient-unstable, e-folding 5 Myr to 0.6 Gyr in the law-on phase) came from its planar background, where
  D.P = p' < 0. SCS1 had already traced this.
  - A finite disc does not reproduce that background: the razor-thin disc's own sheet cells have positive D.P, and the
    planar slab's negative D.P appears in none of the isolated discs.
  - KA3 reproduces TPA1's numbers exactly in TPA1's slab (1.7e-15), so TPA1's arithmetic stands. Its physical reading
    for discs does not.
- **Nothing found wrong** in SCS1's covariant symbol: item 1 extends it to backgrounds with no symmetry at 5.3e-6, and
  KA1 under A4 matches it to 1.2e-3.

## Disclosures

- **A1** (route 2's crop reaches 3 r_e) came before any number. **A2** and **A3** are post hoc, after a smoke test and
  after the first map run (both kept: scs2_maps_run1.*), and before any graded route.
- **A4 is post hoc after a graded run.** The KA1 frequency comparison, a frozen known answer, was missing from the
  route-1 script. I added it after the main frozen-point run had started (SCS2_ONLY=KA1, scs2_wkb_KA1.json), and it
  **failed**: 3.9 % against a 1 % line.
  - The cause is the frozen local fit (a cubic in R, z over a 5 x 5 stencil). The background is fine: at that cell the
    solver's D.P is within 0.75 % of the closed form.
  - A4 adds a fit in the grid's own coordinates (ln r, theta[, phi]) and was committed alone before any A4 number.
  - Both fits' outputs are kept. Route 1's labels are read from A4 because KA1 passes with it.
- **A bug in my first A4 launch.** The switch was named FIT, and the script already defined a dict FIT = {} further
  down, which shadowed it. The first "A4" runs (KA1, the main run and two MUTATE arms) therefore used the frozen fit and
  reproduced its numbers to six digits. I caught this from that coincidence. Those runs were stopped and their outputs
  deleted, the switch was renamed FITMODE, and everything A4 was rerun. Every _A4 file here comes from the rerun.
- scs2_wkb.json (frozen fit) was produced by the script before the KA1 block and the A4 switch were added. With
  SCS2_FIT and SCS2_ONLY unset, the current script runs the same frozen-point code and also runs KA1.
- **KA4.** As coded, the graded KA4 covered the primaries only. scs2_resolution.py applies the frozen clause to every
  twin, and it fails for the axial external-field family (section 3). That failure is part of the label.
- **Item 1.** The 6 added seeds (H negated) are beyond the frozen list, added because the frozen seeds had no G < 0.
- **Route 2 methods.** Dense solves and inertia replace ARPACK, which did not converge. On the fine external-field grids
  m = 1, 2 were not run (n > 4000); the coarse grid carries them. In 3D the test is the frozen Rayleigh certificate; LOBPCG
  is reported but did not converge to the lowest mode at 0.01 a0.
- **Shen et al. 2003** is quoted from memory, so the R_d brackets x 0.5 and x 2 matter: both are STABLE.
- **The far-field check** (scs2_farfield.py) is reported, not graded. The outermost cells sit next to the solver's
  Dirichlet boundary, which imposes the linearised far field, so agreement there is partly built in. Cells at
  3 to 10 r_e are interior.
- **Resources.** Up to five single-thread processes ran at once (route 2 in three parts, route-1 runs beside them).
  Route 2's main parts peaked at 2.2 GB RSS, above the ~1.5 GB guide; every other job stayed under 1.5 GB. The machine has
  16 cores, and load stayed near 7. Nothing was downloaded.

## Files

- Criteria and amendments: FROZEN_CRITERIA.md, AMENDMENT_A1.md - AMENDMENT_A4.md.
- Backgrounds and maps: scs2_aqual.py -> scs2_maps.json / .out (first run scs2_maps_run1.*). Solver caches are not
  committed (regenerated by the script into $SCS2_CACHE).
- Route 1: scs2_wkb.py -> scs2_wkb.json / .out (frozen fit; item 1, KA3, frozen points), scs2_wkb_KA1.json / .out (KA1
  with the frozen fit, run alone), scs2_wkb_A4.json / .out (A4 fit: KA1 and the frozen points), and
  scs2_wkb_MUTATE_{M1,M2,M3}{,_A4}.json / .out.
- Route 2: scs2_route2.py -> scs2_route2_part{0,1,2}.json / .out and scs2_route2_MUTATE_{M1,M2,M3}.json / .out.
  scs2_route2.json / .out is an early 4-background smoke run, kept.
- Reported checks: scs2_resolution.py -> scs2_resolution.json / .out; scs2_farfield.py -> scs2_farfield.json / .out.
- Labels: scs2_labels.py -> scs2_labels.json / .out (reads the outputs above; no new computation).
- Lean: SCS2.lean, SCS2_MUTATE.lean, compile.txt, compile_MUTATE.txt.

Not registered. Does not edit fable52_push/README.md, any PAPER72 file, the register, the decision files, or SCS1's,
TPA1's or FB1's files.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
