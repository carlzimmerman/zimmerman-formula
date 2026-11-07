# SV1 iter_1: does the GEOMETRY of the source, in the action's own nonlinear field, put hot systems above the law? FROZEN CRITERIA

Frozen before any script or graded number. Rules: closure_2026_11_06/SWARM_BRIEF.md. Kappa = 1/2 FITTED; not theory
closed. Adopts nothing. No new term, no new constant: the mechanism is the existing static sector of v3s / AC2q,
div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho_b, mu(x) = x/(1+x) (EQUATIONS_IN_ORDER.md 2.5; AC2q differs by <= 1.1e-10
relative, row 5.2 erratum). Both footings, a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt), never pooled.

## Hypothesis
Hot systems are measured with SPHERICAL analyses (spherical deprojection of the baryons, spherical HSE / Jeans masses,
orientation-stacked lensing). The plain law is applied to g_N_sph(r) = G M_b(<r)/r^2. If the source is flattened or
elongated, the action's exact AQUAL field differs from the law (curl term, non-uniform |grad Phi| on the shell). H: this
difference, for each class's real geometry, gives the observed class offsets while discs stay as QX8 graded them.

## Solver and sources
- QX4's axisymmetric AQUAL solver (closure_2026_11_06/QX4_udg/aqual.py), imported read-only. Equatorial symmetry, axis
  symmetry: oblate (q < 1) and prolate (q > 1) spheroids. Triaxial shapes are not solved (scope; the T1 theorem below
  covers them for the unweighted shell average).
- Profiles, in the spheroidal radius m^2 = R^2 + z^2/q^2: Hernquist rho ~ 1/[m (m+b)^3] (stars of ellipticals, early-type
  lenses), Plummer rho ~ (1 + m^2/b^2)^(-5/2) (dSphs; also the cored proxy for group / cluster gas). Late-type lens control:
  exponential disc rho ~ exp(-R/Rd) sech^2(z/zd), zd = 0.1 Rd.
- Scale symmetry: at fixed mu, the AQUAL solution depends only on b/r_M, r/b, q (r_M = sqrt(G M/a0)). The table is
  solved on b/r_M in {0.03, 0.1, 0.3, 1, 3, 10, 30}, q in {0.4, 0.6, 0.8, 1.0, 1.5, 2.5}, both profiles. Footings enter
  through each class's measured b/r_M. KA4 checks the symmetry.

## Statistics (per solve, on spheres of radius r)
- O1(r) = log10( <g_r>_Omega / g_law(g_N_sph(r)) ), solid-angle average. This is exactly the orientation-stacked
  lensing observable (stacking random orientations averages the 3D effective density to its monopole; its enclosed
  mass is r^2 <g_r>/G) and the unweighted spherical-mass estimate.
- O2(r) = log10( [<rho g_r>_Omega / <rho>_Omega] / g_law(g_N_sph(r)) ), tracer = the source density. This is exactly
  what spherical HSE / Jeans analysis returns (shell average of grad p = -rho grad Phi), with M_b(<r) from the spherical
  deprojection (exact enclosed mass).
- g_N_sph(r) from the deposited mass inside r; g_law = law S root (QX1 4.2).

## Class mapping (frozen; brackets are generous, the gate uses the MOST FAVOURABLE value in the bracket)
- Axis ratios graded: q in [0.4, 1.0] oblate and 1.5, 2.5 prolate for every class (wider than any class's measured
  intrinsic shape: X-ray giant ellipticals E0-E3, cluster / group X-ray gas projected eps <~ 0.3, dSph eps ~ 0.3).
- Measurement radii and b/r_M from the record's own loaders (QX5 qx5.py via QX20's build(), read-only), per footing:
  each hot point's x = g_N/a0 and y = r/r_M (QX20's V4, V5) give M(<r)/M = x y^2, inverted on the profile for r/b,
  hence b/r_M = y/(r/b). Ellipticals: Hernquist. X-COP and groups: Plummer (cored gas proxy). Points with x y^2 >= 0.995
  use r/b at that cap.
- dSphs (bright M31; QX21 T2): Plummer at r = 1.305 b (3D half-mass), b/r_M in [1, 30].
- KiDS early-type lenses (QX21 T1): Hernquist, b/r_M in [0.1, 0.3], r/b in [10, 300]; late-type control: exponential
  disc, Rd/r_M in [0.1, 0.3], same r range.

## Predicted step and measured target (per class c, per footing)
- Dynamics classes (E, X, G, dSph): P_c = max over the class bracket of the per-class mean O2, plus |T_eff|, the SPARC
  mean shift from law to exact field at fixed U = 0.50 (QX8: 0.0090 canonical, 0.0094 alt), which is the most generous
  disc-side term (it lowers the disc anchor).
- KiDS: P = max over brackets of [O1(early) - O1(late)].
- Measured step Delta_c = class mean minus SPARC mean (QX20 KA1 values): E +0.1825 / +0.1894, X-COP +0.4401 / +0.4351,
  groups (f* 0.5) +0.2364 / +0.2266, bright M31 dSphs +0.199 / +0.188 (QX21 T2, already minus SPARC), KiDS +0.158.
  Reported secondary: E after Posacki IMF (QX26) +0.066 / +0.075.
- Errors sigma_c (measured): E 0.158 / 0.155 (QX18, CFG32-style with IMF); KiDS 0.064 (QX21); dSph 0.062 / 0.061
  ((median - lower 95 % bound)/1.96, QX21); X-COP and groups: standard error of the per-system mean offsets (sd/sqrt N),
  computed from the same loaders; groups add in quadrature the f* half-range (0.0816 / 0.0810).

## Labels per class per footing
- EXPLAINED: |P - Delta| <= 2 sigma and Delta > 2 sigma.
- COMPATIBLE, NOT NEEDED: |P - Delta| <= 2 sigma and Delta <= 2 sigma (the law alone is also inside).
- SHORT: P < Delta - 2 sigma. OVER: P > Delta + 2 sigma.
- iter_1 label: GEOMETRY EXPLAINS THE STEP only if no class is SHORT or OVER on either footing; otherwise GEOMETRY
  SHORT (or OVER), with the shortfall in dex.

## Theorem to certify (Lean, SV1_shell_bound.lean + _MUTATE twin)
T1: for weights w_i >= 0 summing to 1, radial components 0 <= g_i <= G_i (G_i = |grad Phi|), with Gauss's law
sum_i w_i mu(G_i/a0) g_i = g_N, mu(x) = x/(1+x): the weighted mean m = sum_i w_i g_i satisfies h(m) <= g_N with
h(g) = g^2/(a0 + g), hence m <= g_law(g_N). Equality needs every g_i = G_i = m. So the orientation-stacked lensing mass
and the unweighted spherical mass of ANY non-spherical source (triaxial included, g_r >= 0 on the shell) sit at or BELOW
the law. The numerical check NUM-T1: O1 <= +1e-3 in every solve with g_r >= 0 on the shell (grid tolerance).

## Known answers and controls
- KA1: q = 1 gives |O1|, |O2| <= 2e-3 at every graded radius (sphere: exact field = law).
- KA2 Gauss: <mu g_r>_Omega / g_N_sph = 1 to 2e-3.
- KA3: K (grid ladder 120x40 vs 180x60, six table cells incl. q = 0.4): |dO| <= 3e-3.
- KA4 scale symmetry: one cell solved at both footings' physical a0 with the same b/r_M: |dO| <= 1e-6.
- MUTATE M1 (Newton, mu = 1): O1, O2 must move by >= 0.1 dex at b/r_M >= 1 (the statistic sees the law). Bites if so.
- MUTATE M2 (planted +0.30 dex added to every P): at least one SHORT label must flip to EXPLAINED or COMPATIBLE. Bites
  if so (the gate can pass).
- MUTATE M3 (force the source spherical, q = 1, for every class): P must drop to |T_eff| +- 2e-3. Bites if the
  favourable-q P differs from it by > 2e-3.

## Discs and the other passes
No term is added: the equations are QX8's. SPARC/RAR (QX8), Cassini/PPN, c_T and galaxy lensing are the record's,
carried exactly. KiDS lensing is graded through O1 above.

Compute: nice -n 15, 1-2 threads, minutes. Outputs small (json / out, no field dumps).
Kappa = 1/2 FITTED; not theory closed.
