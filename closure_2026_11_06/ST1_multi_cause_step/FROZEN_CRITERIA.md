# ST1 frozen criteria: does the hot/cold step have several causes? Class by class, each with its own measured systematic

Frozen before any ST1 script or ST1 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No
dark-matter particle is adopted; HC1's fermion is graded only as the record's test object. Both footings, never pooled:
- canonical: a0 = 9.3603e-11 m/s^2, Lstar = 21.7 pc;
- alt: a0 = 1.1312e-10 m/s^2, Lstar = 22.9 pc.

No new data, no downloads. Every input is on disk and named below. Compute: one thread, under 1 GB, minutes.

## 0. Question and frame

The synthesis (ALL_GATES_NOGO_2026_11_06.md, exit 1) asks whether the step has several causes: IMF for early types,
tides / non-equilibrium for dSph satellites, mass systematics for Coma UDGs, leaving only clusters and groups for a new
ingredient.

ST1 uses GB1's battery exactly (criteria e9464bc8ce; gb1.py's loaders, gates and lines, exec'd read-only up to its
"# --- main" block). Only the data side of a class changes, by that class's frozen systematic below. The plain law
(GB1's L0: b = 1, F = 1, T = 0) is the prediction throughout. PASS lines are GB1's, unchanged.

Per class and footing ST1 reports: the raw step (GB1's L0 number), the systematic applied (size and source), the
residual, and PASS / FAIL / NO VERDICT against GB1's line.

## 1. Systematics, fixed now (size and source; nothing is tuned to close a gap)

**S-E. X-ray ellipticals (G4): IMF variation.** GB1's L1 on the elliptical points: b = f_IMF(sigma) with
log alpha = 0.38 log10(sigma_e/200) - 0.06 (Posacki+2015, vs Salpeter), f_IMF = max(alpha R_SK, 1), R_SK each galaxy's
Humphrey Salpeter/Kroupa ratio, sigma_e = 0.87 sigma_0 (QX26 SIG0, AP). Source: QX26 (c2cbd5086d). Robustness
reported (not graded): sigma_0 x 0.9 and x 1.1 (QX26's own bracket).

**S-K. KiDS early/late split (G7): IMF variation.** GB1's L1 with lens sigma filled by QX26's bracket: early
{130, 170, 210} km/s, late 60 km/s (Kroupa floor). Graded cell: PASS if G7 passes at all three early values, FAIL if it
fails at all three, MIXED otherwise (MIXED counts as not passing). Source: QX26.

**S-D. dSph satellites (G6): tides / non-equilibrium, as an equilibrium cut.**
- Estimator (fixed, not tuned): QX24's tidal susceptibility tau = R_e / r_J, r_J = d_host (M_W / 3 M_host)^(1/3),
  M_W = 4 sigma^2 R_e / G, M_host = V_c^2 d_host / G, V_c = 200 (MW) / 230 (M31) km/s, inputs from X1 x1_per_system.csv
  (rh_pc, sigma, d_host_kpc, host), per footing. Source: QX24 iter_1 (d4f3f62c47), code replayed verbatim.
- Line (fixed): a satellite is in tidal equilibrium if r_1/2 / r_J < 0.5, r_1/2 = (4/3) R_e, i.e. tau < 0.375. Source:
  Z2_satellite_systematics clean cut C1 (r_12 / r_t < 0.5), the record's frozen equilibrium line.
- Applied to the satellite classes only (bright M31, MW classical). LG field dwarfs are not satellites and are kept
  whole. A satellite with no tau (host not MW/M31, or missing input) is kept and counted.
- Graded: GB1's G6 statistic (median minus SPARC anchor, bootstrap 10,000, seed 21, 95 % CI contains 0 for each of
  the three graded classes) on the equilibrium subsets. A graded class with N < 5 after the cut is NO VERDICT (no
  power), never PASS.
- Reported, not graded:
  (a) pericentre reading: tau x 3^(2/3) (pericentre at d_host / 3, X20's A3 qualifier; r_J scales as d^(2/3));
  (b) QX24's strict line tau < 0.05 (known to leave about one system);
  (c) the T3b direction: Spearman of offset with log tau over the graded satellites, and a least-squares line
      offset = a + b log10 tau evaluated at tau = 0.375 and at the subset median. Stated in advance: a negative slope
      means tides cannot remove the step (the most tidally exposed sit lowest).

**S-U. Coma UDGs (G5): mass systematics with a stated source.** S1 (rebuild_2026_10_22/S1_v3_hosted_small) measures
the UDG offset as E = 2 ln(sigma_obs / sigma_pred) on the v3 prediction with Coma's EFE (dmean, Lstar floor, E-W) and
carries CFG948's systematic recipe, rerun on v3: M_* +-0.2 dex (s_M), sigma +-15 % (s_A), distance +-5 % (s_D). These
are the only UDG mass systematics with a stated source. Values read from s1_v3_hosted_small_results.json
(row "<foot>|S4 v3 dmean L*floor E-W": se, s_M, s_A, s_D, sigma_sys).
- Reading Q (quadrature): GB1's own G5 (residual mean vs 2 sigma_U, sigma_U = hypot(se, sigma_sys) / ln 10).
- Reading L (linear edge): every systematic set at its full stated edge in the direction that lowers the offset,
  summed linearly: residual = mean - (s_M + s_A + s_D) / ln 10, graded against 2 se / ln 10 (statistical only, so the
  systematic is not counted twice).
- Graded cell: PASS if either reading passes; FAIL only if both fail (the more generous reading decides).
- Reported, not graded (model choices, not data systematics): S1's host-field variants, field / 2 and dproj.

**Classes with no systematic in this lane.** X-COP (G2), groups (G3), SPARC (G1) and the Solar System (G8) keep GB1's
L0 cells. Reported only: QX26's IMF on X-COP and groups (GB1's L1 bracket), QX21 T3's hydrostatic-bias sign (lensing
masses >= hydrostatic) and QX30's cluster data-assumption audit (ROBUST), quoted from the record.

## 2. After the systematics: which classes remain, and the target

A class "remains above the law" if its systematic-applied cell is FAIL with a positive residual (for G6: a graded
class whose CI lies above 0; for G3: fewer than 16 of 20 groups inside, median residual > 0).

- Reported per remaining class and footing: the residual (dex), and the uniform extra baryon factor f that nulls it
  under GB1's L0 convention (b = 1 + f, F = 1; f solved by bisection on the class statistic: mean residual for G2, G4,
  G5; median residual over all points for G3 at f* = 0 and 1; median minus anchor for G6). This is a target statement,
  not a candidate.
- If the remaining set is exactly {X-COP, groups}: RESULT states the reduced target "clusters and groups only, with
  discs, dSphs and UDGs excluded". Otherwise RESULT states the target the record actually leaves (the remaining set).

## 3. Reduced battery and the two record test objects

Reduced battery = GB1's G1-G8 with each corrected class's data side replaced by its ST1 systematic-applied version
(G4 IMF, G7 IMF bracket, G6 equilibrium subsets, G5 readings Q/L), all lines unchanged. G9 (CMB) stays as the record
has it: not re-graded here.

A conditional reading is also reported: the brief's hypothetical battery in which G5 and G6 are dropped (dSphs and
UDGs treated as explained), whatever section 2 finds.

Test objects, graded from their committed record numbers (no re-solve):
- HC1's thermal fermion (m 11.1377 eV, hc1.json, criteria c207d70254), rule TOT.
- QX12 iter_3's isothermal sea (qx12_i3.json, b605c9fd7c / A1 9c7497b4cc), at c_min and over its whole c_s0 scan.

Rule (first-order, stated): a corrected class's candidate residual = the candidate's record residual minus the L0
shift that the ST1 systematic produces on that class (shift = L0 residual raw - L0 residual corrected, per footing).
For the rows with no systematic (G1, G2, G3, G8) the record cell is used unchanged. For QX12 iter_3, where the record
carries X-COP and group numbers per c_s0, the scan is read directly: the sea passes the reduced battery only if some
c_s0 passes G2 and the groups line, and the corrected galaxy rows.

## 4. Known answers (KA FAIL means stop; nothing is graded)

- KA1: every GB1 L0 graded number (G1 Z and rms; G2 mean and rms; G3 n_pass f* 0/1 and medians; G4 mean; G5 mean and
  z; G6 three graded classes' medians-minus-anchor and CIs; G7 R; G8 uses) equals gb1.json's to 1e-9, per footing.
- KA2: S-E reproduces QX26's elliptical D_imf (qx26.json foot.<f>.ellipticals.D_imf) to 1e-6, per footing.
- KA3: S-K reproduces QX26's KiDS bracket residuals R (qx26.json foot.<f>.kids.bracket.{130,170,210}.R) to 1e-4.
- KA4: the tau replay reproduces QX24's T3 tau p10 / p50 / p90 (qx24.json) to 1e-9 on the same set, per footing.
- KA5: S-U reads S1's se and sigma_sys with hypot(se, sigma_sys) / ln 10 equal to GB1's sigma_U to 1e-12.
- KA6: HC1's G2 and G3 cells and QX12 iter_3's c_min X-COP mean are read back equal to their RESULT/README values
  (HC1 X-COP +0.392 / +0.360 to 5e-4; QX12 -0.713 / -0.724 to 5e-4).

## 5. MUTATE twins (separate outputs st1_MUTATE.*)

- M1 (frozen, must FAIL): Newton (b = 1, F = 0) on the systematic-corrected battery. It must FAIL G1 on both
  footings, or the run reports NO POWER.
- M2 (frozen, must FAIL): the IMF correction inverted (b = 1 / f_IMF on each elliptical point) on G4. It must FAIL G4
  on both footings, or the S-E reading has no power.
- M3 (frozen, must change): the tidal line set to tau < 1e9 (no cut) must reproduce GB1's L0 G6 numbers exactly; the
  cut line set to 0 must give NO VERDICT. If either does not, the S-D code is wrong.

## 6. Labels

Per class: EXPLAINED (systematic-applied cell PASS on both footings), PARTLY (raw FAIL, residual reduced but cell FAIL
on at least one footing), NOT EXPLAINED (residual reduced by less than a third of the raw step on either footing, cell
FAIL), NO VERDICT (no power).

Lane label:
- **MULTI-CAUSE, CLUSTERS AND GROUPS ONLY** if after the systematics only G2 and G3 remain, on both footings;
- **MULTI-CAUSE IN PART (remaining set)** if some but not all non-cluster classes are explained;
- **ONE STEP STANDS** if no class is explained.
Test objects: PASSES THE REDUCED BATTERY / FAILS (rows), per footing, plus the conditional reading.

Any change after this freeze is disclosed in RESULT.md as post-freeze.

Kappa = 1/2 FITTED; not theory closed.
