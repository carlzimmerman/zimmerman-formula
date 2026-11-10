# SCS3 (static clock, discs in a uniform external field): FROZEN CRITERIA, committed alone before any SCS3 script, Lean file or number

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. kappa = 1/2 FITTED; not theory closed. Footings
canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), never pooled. The component is cold dark energy, never a particle. No
LCDM input, no download. This lane does not edit fable52_push/README.md, any PAPER72 file, the register, the decision files,
or SCS1's / SCS2's files (SCS2's scripts are copied into this folder, not imported or edited).

Id check: `ls -d fable52_push/SCS3*` found nothing; `git log --all --oneline | grep -i scs3` found nothing. Started by the
fable52 lead session on the owner's instruction ("keep pushing all open lanes until we get closure") to take SCS2's two
external-field families (NO VERDICT / NO VERDICT) to a verdict: the last part of PAPER72's open item 2.

## 0. The question

Action (A) at mu_K = 0, n_d = 0, gamma_L = 0, gravity coupled (SCS1/SCS2's system, unchanged). The static clock's gradient
coefficient is G = n_d + D.P = D.P (the law's phantom density). Around an isolated disc it is positive everywhere (SCS2,
STABLE / STABLE). With a uniform external field g_e it is negative in regions, and SCS2 could not converge the magnitudes.
SCS3 asks: with three or more resolutions (axial field, 2D) and two or more (in-plane field, 3D), do the growth rate and the
region converge, and to what?

## 1. Families, backgrounds and resolutions (SCS2's, extended in resolution only)

Backgrounds are SCS2's exactly (its scs2_aqual.py, copied: same solver, Picard tolerance 1e-8, A2/A3 inner treatment, first
20 shells masked, Dirichlet linearised far field at r_max = max(1e3 R_d, 10 r_e), r_e = sqrt(G M a0)/g_e):
- **AX (axial field, 2D axisymmetric, full theta):** razor-thin exponential and Kuzmin discs; log M_b 9.4, 10.45, 10.7, 10.9;
  g_e = 0.01 and 0.1 a0 along the axis. 16 backgrounds per footing.
- **PL (in-plane field, 3D):** the same two shapes; log M_b 9.4 and 10.9; g_e = 0.01 and 0.1 a0 in the plane. 8 per footing.

Resolutions, refinement ratio rho = 1.5 in every direction (base counts before SCS2's A2 radial scaling):
- AX: R0 = (nr 48, ntheta 24) [SCS2 coarse], R1 = (72, 36) [SCS2 fine], R2 = (108, 54), R3 = (162, 81). (Full-theta grids
  carry 2 x ntheta cells, as in SCS2.) All four are required.
- PL: R0 = (48, 16, 16) [SCS2's grid], R1 = (72, 24, 24); R2 = (108, 36, 36) is run only if one R2 solve's peak RSS is below
  4 GB (measured on the first R2 solve and reported); otherwise PL uses the two-grid rule of section 3.

## 2. Quantities per background and resolution

Q_neg/Q_pos and minimum D.P as SCS2 (off-plane cells, frozen threshold D.P < -1e-6 max|D.P|), plus:
- **Route L (local symbol, exact).** At mu_K = 0 the WKB growth is omega^2 = G (1 - K m)/m, maximised over directions at
  khat parallel to the local field, where K m = 1/(1+u)^2, so (1 - K m)/m = K u (2 + u) (Lean). The local growth rate is
  Gamma_loc^2 = -4 pi G_N D.P u (2 + u) on cells with D.P < 0, u = |grad Phi|/a0. Route L's quantity is
  **Gamma_L = max over off-plane unmasked cells of Gamma_loc**, its location (r/r_e, r/R_d, theta), and the e-folding time
  1/Gamma_L. (Off-plane: the two sheet cells of the razor-thin and Kuzmin discs are excluded; see 2c.)
- **Route L-tilde (the discrete operator's symbol).** Route 2's operator keeps J''_rr and J''_tt and drops J''_r-theta, so
  its high-k limit is G (1 - mt)/mt with mt = min(J''_rr, J''_tt). Gamma_Lt = max over the same cells. It is the value route
  2 must approach, and is used only for the route-2 consistency check (KA5).
- **Route 2 (global pencil).** L_G zeta = lambda H zeta exactly as SCS2 builds it (A1 crop max(30 R_d, 3 r_e)), lowest
  eigenvalue at m = 0 (and m = 1, 2 at R0 and R1). Above SCS2's dense limit (n > 3000) the lowest eigenvalue is found by
  shift-invert Arnoldi on T = M L_G, M = L_chi^-1 - L_phi^-1, through the sparse 3n block system
  [L_chi a = L_G x, L_phi c = L_G x, a - c - sigma x = b], with sigma at the rigorous lower bound
  lambda_min >= min over faces of (G_f/J_f) (Lean: H >= L_chi and G_f >= (G_f/J_f) J_f), so no eigenvalue lies below sigma
  and the eigenvalue nearest sigma is the lowest. Route 2's rate is Gamma_2 = c sqrt(-lambda_min). In 3D (PL) route 2 is
  SCS2's Rayleigh certificate (sign) at every resolution, plus the pencil by the same block method where the block LU peak
  RSS stays below 4 GB (reported where not run).
- **Region.** The negative-D.P region's inner and outer radius (in r_e and R_d), theta range, whether it touches the disc
  (any negative off-plane cell with r < 5 R_d and |z| < 1 R_d), and the region where Gamma_loc > 1/t_H (t_H = 13.8 Gyr,
  the age of the universe: at least one e-fold in a Hubble time), with the same extents.
- **2c. The sheet.** For the razor-thin sheets the plane cells carry a surface density, so their cell D.P scales as 1/(cell
  thickness) and Gamma_loc there is not a convergent quantity. The convergent one is the surface phantom density
  Sigma_ph(R) = sum over the sheet cells of D.P x (r dtheta). It is reported per resolution: its minimum, and where it is
  negative (R/R_d). **If Sigma_ph is negative at R1-R3 at any R**, the razor-thin model's sheet rate is unbounded as the sheet
  thins (a property of the zero-thickness idealisation, not a rate), and the lane then runs the **thick-disc twin**
  (Bershady h_z, SCS2's 'thick' deposit) in the same fields at the same resolutions (AX at R0-R3; PL at R0-R1), graded by the
  same rule over all its cells (no sheet exclusion): it supplies the disc-body rate.

## 3. Convergence rule (graded)

For each graded quantity Q (Gamma_L^2, Gamma_2^2 = -lambda_min, Q_neg/Q_pos, the region's inner radius in r_e), with h_i
the cell size at resolution i (h_{i+1} = h_i/1.5):
- **Three or more resolutions (AX).** On the finest three: d1 = Q_mid - Q_coarse, d2 = Q_fine - Q_mid.
  - Monotone (d1 d2 > 0) and |d2| < |d1|: observed order p = ln(d1/d2)/ln 1.5; Q_inf = Q_fine + d2/(1.5^p - 1); error
    E = 1.25 |d2|/(1.5^p - 1) (Roache's GCI with the three-grid safety factor). With four resolutions the error is
    max(E, |Q_inf(finest three) - Q_inf(coarsest three)|).
  - Already flat: if |d1| and |d2| are both <= 2 % of |Q_fine|, Q_inf = Q_fine, E = max(|d1|, |d2|).
  - Oscillating (d1 d2 < 0): Q_inf = mean of the finest two, E = max(|d1|, |d2|).
  - **Converged** iff the order (when used) lies in [0.5, 6] and E <= 0.20 |Q_inf|.
  - **Diverging** iff monotone with |d2| >= |d1| on the finest three and on the coarsest three (no finite limit indicated).
- **Two resolutions (PL, if R2 is not run).** p = the median observed order of the same quantity over the AX family on the
  same footing (or 2 if AX gives none); Q_inf = Q_1 + (Q_1 - Q_0)/(1.5^p - 1); E = 3 |Q_1 - Q_0|/(1.5^p - 1) (two-grid
  safety factor 3). Converged iff E <= 0.25 |Q_inf|. If R2 is run, the three-grid rule applies.

## 4. Labels (per family, per footing; the field strengths 0.01 and 0.1 a0 also reported separately)

- **STABLE:** on every background of the family, the negative-D.P region (off-plane, and the sheet / thick-disc body) is empty
  on the finest two resolutions, or Q_neg/Q_pos converges to <= 0.02 with E including 0 and route 2 has no negative lambda on
  the finest resolution it ran.
- **UNSTABLE (converged growth):** on every background of the family Gamma_L^2 converges to a positive value, route 2 is
  negative on every resolution it ran, Gamma_2^2 converges (AX; PL: sign on both grids plus pencil where run), KA5 holds, and
  the region's inner radius converges. Reported: Gamma_L (Richardson) with error, e-folding time, location, region.
- **UNSTABLE, RATE UNBOUNDED:** negative on every resolution on both routes, but Gamma_L^2 is Diverging (section 3) on at least
  one background while the sign converges. Reported with the observed growth with resolution and where.
- **NO VERDICT:** a known answer fails; routes disagree in sign; or the convergence rule is met neither way.
The thick-disc twin, if run (2c), is labelled by the same rule and reported beside the razor-thin family's label; the family's
label is the more unstable of the two only if both are converged.

## 5. Known answers (graded; each must pass for its family's label)

- **KA1 (SCS2's isolated discs):** the 16 isolated primaries per footing (razor-thin and Kuzmin, 4 masses) at R0 and R1 have
  D.P > 0 in every unmasked cell (SCS2's result), and stay so at R2 and R3; route 2's lambda_min > 0 at R0 (dense, SCS2's
  setting) on the log M_b 10.45 primaries, equal to SCS2's scs2_route2_part*.json values to 1e-6 relative.
- **KA2 (SCS2's external-field numbers):** at R0 and R1 the AX maps reproduce SCS2's scs2_resolution.json fractions and
  minimum D.P (fine and coarse) to 1e-6 relative on all 32 axial backgrounds, and route 2's R0 lambda_min (dense) reproduces
  SCS2's 48 coarse axial rows to 1e-6; the PL R0 maps reproduce scs2_maps.json's PL entries (Q_neg/Q_pos, min D.P) to 1e-6.
- **KA3 (Richardson on known sequences):** Q(h) = Q_inf (1 + c h^p) with p = 1, 2 and Q_inf, c random: Q_inf recovered to
  1e-6 relative and labelled Converged; Q(h) = h^-1 labelled Diverging.
- **KA4 (two-grid rule against three grids):** the PL two-grid rule applied to AX's R1/R2 must give Q_inf within the AX
  three-grid error (finest three) for Gamma_L^2 on at least 28 of 32 AX backgrounds; otherwise the two-grid rule is not
  trusted and PL's label needs R2.
- **KA5 (route 2 against its own symbol):** on AX, |Gamma_2^2(inf) / Gamma_Lt^2(inf) - 1| <= 0.25 on every background with a
  converged pair (a global mode below the local bound would show here as a ratio > 1.25; then route 2's rate is reported as
  the rate and the label notes it; a ratio < 0.75 is a disagreement: NO VERDICT).
- **Reported, not graded:** the far-field closed form in the plane perpendicular to g_e (from SCS2's sympy-exact far-field
  phantom with u -> x_e = g_e/a0):

      Gamma_ff^2(r) = G M (2 + x_e) / (s^3 r^3),   s^2 = 1 + L_e = (2 + x_e)/(1 + x_e),

  i.e. close to the Newtonian Kepler rate of the baryonic mass at r (Lean); compared with Route L in the band at 4-8 r_e
  (0.1 a0) at the finest grid. Also a domain check: one background (expo, log M_b 10.45, 0.1 a0, both footings) at R1 with
  r_max = 20 r_e, Gamma_L compared with r_max = 10 r_e.

## 6. MUTATE twins (separate outputs; each must bite)

- **M1 tilt sign flipped (G -> -D.P):** the most-unstable cell must move out of the D.P < 0 region on every AX background,
  and the isolated primaries (KA1 set) must turn unstable (Gamma_L > 0).
- **M2 grid artefact:** add to D.P a negative spike in one cell at r = r_e on the axis (the axis cell, theta = 0 or pi,
  with the larger |grad Phi|, i.e. away from the null) whose amplitude is 10 x (h_R0/h)^2 x |min D.P at R0|. The convergence rule must then call Gamma_L^2 Diverging or not Converged on every AX background
  (it must not report a converged rate).
- **M3 Richardson:** the KA3 sequences with the order formula's ratio inverted (p = ln(d2/d1)/ln 1.5) must fail KA3.
- **M4 Lean twin:** false versions of every Lean statement must fail to compile.

## 7. Physical reading (required if a family is UNSTABLE)

- The converged e-folding time against (a) the disc's orbital time 2 pi R/v_c at R = 2.2 R_d, (b) the orbital time at the
  most-unstable location, (c) t_H = 13.8 Gyr (number of e-folds in t_H).
- The region in R_d and r_e; whether it reaches the disc (r < 5 R_d); the region where Gamma_loc > 1/t_H.
- An LMC-like satellite (log M_b 9.4 bin, g_e ~ 0.1 a0) and a disc in a group (0.01-0.1 a0): affected within a Hubble time
  or not; whether the uniform-field model applies there (r_e against the distance to the host: about 50 kpc for the LMC).
- Say which it is: a slow instability confined to a region of the halo, or a disc destroyed. Linear only: the nonlinear
  outcome is not computed.

## 8. Lean (fable_independent_2026/lean_2026)

Statements, with a twin of false versions: the reduction (1 - K m)/m = K u (2 + u) along the field and K u across it, and
the growth sign (Gamma^2 > 0 iff D.P < 0, zero at u = 0); the far-field plane identity Gamma_ff^2 = G M (2 + x)/(s^3 r^3);
the Richardson identities (three values Q_inf + C t^-i give the ratio t and Q_inf = Q_2 + (Q_2 - Q_1)/(t - 1)); the route-2
lower bound (N >= c q, D >= q > 0, c < 0 give N/D >= c).

## 9. Resources and rules

Single-threaded BLAS; at most three processes at once; checkpoint each background's result to a partial json as it lands;
SIGTERM writes the partial file and exits. Solver caches go to the scratchpad, not the repo. Commit messages end "Adopts
nothing. kappa = 1/2 FITTED; not theory closed." Explicit-path commits only.

## 10. Disclosure: expectations before any SCS3 number

From SCS2's published far-field phantom (its RESULT.md) I derived, before any SCS3 number, Gamma_ff^2 = G M (2 + x)/(s^3 r^3)
in the band; at log M_b 10.45, 0.1 a0, canonical, r = r_e (65 kpc) this gives an e-folding time of about 1.7 Gyr, inside
SCS2's coarse 1.0-2.4 Gyr. So I expect: the band's rate converges (it is set by the smooth far field at r ~ r_e), the null
contributes little (u -> 0 there, so Gamma_loc -> 0 even where D.P is most negative), and both families come out UNSTABLE
(converged), slow, confined to r >~ r_e, far outside the disc. I do not know the sheet's sign in an external field (SCS2's
plane minima were negative for the razor-thin exponential disc in an axial field), nor whether the null's D.P diverges with
resolution. Not results.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
