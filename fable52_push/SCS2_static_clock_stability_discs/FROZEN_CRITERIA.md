# SCS2 (static clock, discs): FROZEN CRITERIA, committed alone before any SCS2 script, Lean file or number

TEST lane, quarantined. Adopts nothing and relabels nothing. Not registered. kappa = 1/2 FITTED; not theory closed. Footings
canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), never pooled. No LCDM input, no download. This lane does not edit
fable52_push/README.md, any PAPER72 file, the register, the decision files, the memory index, or SCS1/TPA1/FB1 files.

Id check: `ls -d fable52_push/SCS2*` found nothing; `git log --all --oneline | grep SCS2` found nothing. Asked for by the
fable52 lead on the owner's instruction ("Yes, run it", lead chat), as the item SCS1 left open under "Non-spherical baryons".

## 0. The question

Around flattened baryons, is the static clock of action (A) (mu_K = 0, no dust of its own: form B's disc halo) linearly
stable with gravity coupled? Where is G = n_d + D.P negative, how much of the halo's charge sits there, and how fast does
anything grow?

## 1. System (as SCS1, frozen)

Action (A) at S = 1, gamma_L = 0 (stiffness on as a hand-form bracket only), mu_K = 0, n_d = 0, Newtonian gauge,
quasi-static metric, P eliminated by the Legendre maximum. Background: the law's own static equation
div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho_b, mu(x) = x/(1 + x) (AQUAL form; PAPER70 at mu_K = 0), static clock.

**Item 1 (general background, no symmetry).** Route 1 (SCS1's full covariant 3+1 symbol, code copied, not imported) is
compared with the hand closed form omega^2 = K G [(1 - K m) k^2 - mu^2 Qbar^2]/(mu^2 Qbar^2 + K m k^2), G = Qbar n_d +
div Pbar, m = khat.J''.khat with J'' anisotropic (1/(K(1+u)^2) along the field, 1/(K(1+u)) across), on 6 generic
backgrounds with no symmetry (ln N a random cubic polynomial in x, y, z with galaxy-scale magnitudes; seeds 1-6), 3
directions (along the field, across it in a random plane, a random oblique), kr 1e3 and 1e5. Line: relative 1e-3. If it
holds, the sign condition is G > 0 (with 0 < K m < 1 for every direction, Lean); if not, the lane states what more it needs.

## 2. Backgrounds (solved, frozen)

Solver: finite volume on (x = ln r, theta, phi), Picard iteration with damping and sparse direct solves (the scheme of the
record's QX4_udg/aqual.py, generalised: full theta range when the plane symmetry is broken, phi cells for the in-plane
external field). Residual line 1e-8. Dirichlet at r_max: Phi = const when isolated; with an external field g_e, the
linearised far field Phi = g_e x_par - G M/(mu_e sqrt(1 + L_e)) / sqrt(r_perp^2 + x_par^2/(1 + L_e)), mu_e = mu(g_e/a0),
L_e = 1/(1 + g_e/a0). Grids: r from 0.02 R_d to r_max = 1e3 R_d (isolated) or 10 r_e (with an external field, r_e =
sqrt(G M a0)/g_e), log-uniform.

- Masses: log M_b 9.4, 10.45, 10.7, 10.9 (the four KiDS bins).
- Scale length: R_d = R_50/1.678 with R_50 = 0.10 kpc (M/Msun)^0.14 (1 + M/3.98e10 Msun)^0.25 (Shen et al. 2003,
  MNRAS 343, 978, late types, eq. 18; **quoted from memory, not downloaded**; the verdict is also run with R_d x 0.5 and x 2
  for log M_b 10.45 as a reported bracket).
- **Primary (isolated):** razor-thin exponential disc Sigma = M/(2 pi R_d^2) exp(-R/R_d) (deposited in the two theta cells
  at the plane: thin to the grid); Kuzmin disc with a = R_d.
- **Brackets:** thick exponential disc, rho proportional to exp(-R/R_d - |z|/h_z), h_z = 0.196 R_d^0.633 kpc (Bershady 2010,
  as in the record's TS1); exponential disc plus a Hernquist bulge (B/T = 0.2, a_b = 0.2 R_d; stated choice); the razor-thin
  exponential and the Kuzmin disc each in a uniform external field of 0.01 and 0.1 a0, along the axis (axisymmetric) and in
  the plane (3D; masses 9.4 and 10.9 only, coarse grid nr 48, ntheta 16 over the upper half, nphi 16 over half a turn, using
  the z and y mirror symmetries).
- **What the external-field bracket represents:** a disc held in a uniform external field in the law's own nonlinear
  equation (the law's external field effect). Form B, as the decision file states it, does not use that effect for hosted
  dwarfs; the bracket shows what the action's static state does in such a field and is reported, not graded as form B.

## 3. Maps and routes

- **D.P map.** Per cell, K D.P = div(grad Phi/(1 + u)) by the same finite-volume fluxes the solver uses
  (= lap Phi - K rho_b). Reported per background: the sign map; the volume where D.P < -1e-6 max|D.P|; the halo-charge
  fractions Q_neg/Q_pos and Q_neg/(Q_pos + Q_neg) inside r_max; where the negative cells sit (theta band, r range, on or off
  the axis); the plane cells' sheet value reported separately.
- **Route 1 (WKB, full covariant).** At frozen points per background: the 3 most negative off-plane cells (at least 2 cells
  from the plane and the boundaries), up to 3 cells adjacent to a sign change, and 4 references (theta two cells above the
  plane at R_d and 3 R_d; the axis cell at r = R_d; 45 degrees at 3 R_d). N's derivative tensors from a local cubic fit of
  Phi in (R, z) over a 5 x 5 cell stencil, converted to Cartesian tensors with the axisymmetric chain rule. kr 10, 1e3, 1e5;
  directions along the local field, across it in the meridional plane, azimuthal. Hand G from the fit is compared with the
  grid D.P (reported).
- **Route 2 (global).** Axisymmetric backgrounds: the constraint-surface generalized eigenproblem -C zeta = lambda H zeta,
  H = (A_chi^-1 + A_phi^-1)^-1 (symmetric positive definite), C the gradient form with the grid G, for m = 0, 1, 2 on two
  resolutions (nr x ntheta = 48 x 24 and 72 x 36 over the solver's domain, cropped at 30 R_d with Dirichlet there); stable
  iff no lambda < -1e-10 max|lambda|. 3D (in-plane field): the exact Rayleigh criterion with sparse C only (H is positive
  definite, so lambda_min < 0 iff zeta.(-C).zeta < 0 for some zeta): trial functions localized on the negative-G cells.
- Variational statement used: at mu_K = 0 the clock is linearly stable iff G >= 0 almost everywhere (from -C zeta =
  lambda H zeta with H > 0 and C = -int G |grad zeta|^2), and the local growth where G < 0 is omega^2 = G (1 - K m)/m,
  bounded in k; with the stiffness on, omega^2 = G (1 + gamma_L m k^2 - K m)/m, which rises with k^2 (Lean).

## 4. Labels (per footing; isolated discs first, then brackets)

- **STABLE:** no growing mode anywhere examined (route 1: no growing root at any frozen point; route 2: no lambda below the
  tolerance for m = 0, 1, 2 at both resolutions, or no negative Rayleigh quotient in 3D).
- **UNSTABLE IN REGIONS:** growing modes exist. Reported: the regions, the fraction of the halo's charge in them, e-folding
  times beside the local free-fall time 1/sqrt(4 pi G |rho_loc|) and r/v_c, and whether the rate is bounded in k without the
  stiffness and rises with k with it.
- **NO VERDICT:** a known answer fails, or the two routes disagree.

## 5. Known answers (all must pass)

- **KA1** A point mass (Plummer core 1e-3 R_d) through the axisymmetric machinery: D.P > 0 in every off-core cell; STABLE by
  both routes; route-1 frequencies at log M_b 10.45, 30 kpc equal SCS1's (omega^2 code 1.1154e-7 radial, 4.9785e-8
  tangential) to 1 %.
- **KA2** Kuzmin field against its closed form (above the plane, the law applied to the point mass at z = -a): relative error
  of |grad Phi| <= 1e-2 in every cell at least 3 cells off the plane and inside 100 a.
- **KA3** A planar slab (TPA1's model) through route 1 reproduces TPA1's negative D.P and its growth (e-folding 5.03e6 to
  6.25e8 yr on TPA1's points, three digits).
- **KA4** Solver residual <= 1e-8 at both resolutions; the negative-cell charge fraction and the minimum G agree between the
  two resolutions within 20 % (or both zero).
- **KA5** The phantom mass inside a sphere of radius r: equal to M_b (nu(y) - 1) to 1e-3 for the point mass at 10 r_M, and to
  2 % for the isolated discs at 30 R_d.

## 6. MUTATE (separate outputs; each must bite)

- **M1** tilt sign flipped (G -> n_d - D.P): must turn the isolated discs' stable regions unstable and, in an external-field
  bracket with negative cells, those cells stable.
- **M2** planar divergence (div Pbar replaced by its component along the field, d(Pbar . ghat)/ds only): must turn a stable
  region unstable.
- **M3** mixing dropped (decoupled): must change omega^2 by >= 1e-3 without changing any sign.

## 7. Lean (fable_independent_2026/lean_2026)

Closed forms used: the anisotropic kinetic form is positive definite (J''_par > 0, J''_perp > 0); 0 < K m < 1 for every
direction; omega^2 has the sign of G at mu_K = 0; the Rayleigh sign statement (H > 0 implies the sign of lambda_min is the
sign of min zeta.(-C).zeta); the stiffness form unbounded for G < 0; the Kuzmin image identity in closed form. Twin with
false versions.

## 8. Disclosure: expectations before any number

- The lead's: an isolated Kuzmin disc has D.P > 0 everywhere (a positive sheet plus a displaced point mass's halo), so
  STABLE; negative regions only with an external field.
- Mine: the same for Kuzmin (exact: off the plane the field is a displaced point mass's law field, whose phantom is
  positive); for the razor-thin exponential disc I do not know the sign map in the AQUAL form; with an external field I
  expect negative D.P on the axis through the null of the total field, on the side where the internal field opposes g_e,
  and therefore UNSTABLE IN REGIONS for those brackets, with bounded rates. Not results.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
