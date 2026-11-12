# CK3 frozen criteria: groups under the kicked collisionless carrier (predicted retention vs group mass)

Frozen before any CK3 script or CK3 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No new
particle beyond the record's carrier (L365-L390, as specified in RESOLUTION_2026_11_07.md). No LCDM input on the data
side; the LCDM-like halo enters ONLY as L388's reference normalisation (retention eps = carrier kept / carrier in L388's
LCDM twin run) and as XR13's NFW mass conversion that the record already used to place groups in L388's bins. Both are
labelled "LCDM-like reference" wherever they appear. Both footings, graded separately, never pooled:
- canonical: a0 = 9.3603e-11 m/s^2; alt: a0 = 1.1312e-10 m/s^2 (the record's full-precision values as carried by the
  SE2 / GB1 namespace, exactly as UA1).

Spec: closure_2026_11_07/RESOLUTION_2026_11_07.md, lane CK3 ("groups under the kick: predicted retained f versus group
sigma for the 20 Lovisari groups (L388's bins interpolated, both footings) against UA1's joint posteriors; the f-sigma
slope is the prediction"). CK1 / CK2 / CK4 are other lanes and are not done here.

**Not blind.** Read before this freeze: the resolution, UA1 (criteria, RESULT, ua1.py, ua1.json: class step +0.259
canonical / +0.221 alt, 95 % [+0.052, +0.459] / [+0.009, +0.415]), SE2's se2.py groups machinery, GB1 / QX5's Lovisari
loader, KD1's f-need diagnostic (groups f*0 / f*1 need 3.46 / 1.23 canonical, 2.86 / 0.93 alt, in units of M_b),
L388's .out and results JSON (pooled bin retention 0.34 / 0.50 / 0.68 / 0.85 at 575 ... 0.17 / 0.27 / 0.52 / 0.79 at
650 km/s; 120 per-halo masses and eps per kick; 2 halos below 6e13), XR13_door_cosmology.py section (i) and its .out
(5 of 20 groups below L388's lowest bin under its NFW conversion). No CK3 number has been computed.

No new data, no downloads. Inputs (all on disk, read-only):
- real_research/data/lovisari2015_groups.tsv (20 groups; M500, M2500, Mgas, kT; h70 as published), via QX5's loader
  as GB1 / SE2 / UA1 load it.
- real_research/dark_sector_2026/L388_linear_gate_pooled_results.json (numbers.retention_by_mass and numbers.halos:
  per-halo M(<1 Mpc/h) of the LCDM-like twin and eps per kick, three realisations 7 / 17 / 29).
- closure_2026_11_07/UA1_fragile_rows/ua1.py and ua1.json; closure_2026_11_06/SE2_step_as_systematics/se2.py (exec'd
  read-only, definitions only, writes never reached / redirected).
- real_research/cross_thread_review_2026_09_26/XR13_door_cosmology.py (its m_1mpch conversion, copied verbatim).

## 1. The carrier in the group (frozen)

- **Retention variable.** eps(M1) = L388's retained fraction of the carrier relative to the LCDM-like twin, as a
  function of M1 = M(<1 Mpc/h) of the LCDM-like twin halo (L388's own statistic, L371's bins).
- **Carrier mass in the group (primary, the resolution's convention = KD1's f-table units).** The retained carrier is
  f = R_c * eps in units of the group's baryon mass M_b, with R_c = 5.4 (the cosmic carrier-to-baryon ratio as written in
  the resolution; LCDM-like reference normalisation). It is entered exactly as KD1's f diagnostic and UA1's IMF factor
  enter: the baryon field is multiplied, b_tot = b_IMF + R_c * eps, and the residual of each point is
  D - dlaw(b_tot, gN, a0). The carrier is taken to follow the baryon profile at both radii (R2500, R500); its true
  profile inside the group is CK1's question, not this lane's (disclosed).
- Reported only (decides nothing): (a) R_c = 5.36; (b) the carrier Newtonian-additive (no law boost):
  M_pred = gl(b_IMF gN, a0) r^2 / G + R_c eps M_b.

## 2. Group mass -> L388's mass variable (frozen)

- Abscissa of the graded slope: **log10 M500** (Lovisari hydrostatic M500, h70 as published). The groups table has no
  member-galaxy sigma, so "group sigma" is graded through M500. Reported only: the same slope against
  log10 sigma_kT, sigma_kT = sqrt(kT / (mu m_p)), mu = 0.6 (kT in keV from the table).
- Conversion M500 -> M1: **XR13's m_1mpch verbatim** (NFW with Dutton-Maccio c200(M200), normalised so that
  M(<R500) = M500 at 500 rho_c, h = 0.6736, mass inside 1000/h kpc, in Msun; compared directly to L388's bin edges as
  XR13 did). LCDM-like reference, labelled. Reported only: M1 x 0.6736 (if L388's masses are read as Msun/h).

## 3. Interpolation and extrapolation rule (frozen)

- **Nodes.** For each kick, the four L371 bins (6e13-1e14, 1e14-1.5e14, 1.5e14-2.5e14, 2.5e14-1e17 in M1) of the
  pooled 120 halos: node x_k = median log10 M1 of the halos in bin k, node y_k = median eps of the halos in bin k
  (L388's statistic).
- **Interpolation:** eps linear in log10 M1 between adjacent nodes.
- **Below the lowest node (primary):** linear extrapolation in log10 M1 from the two lowest nodes, floored at 0.
  Reported only: flat at the lowest node's eps (XR13's upper-bound rule). If the label differs between the two, RESULT
  says so.
- **Above the top node:** flat at the top node's eps.
- **Kicks.** v_k in {550, 575, 600} km/s. 575 and 600 are L388 runs. **550 is not a run**: per halo,
  eps_550 = eps_575 + (eps_575 - eps_600) (linear in v_k), clipped to [0, 1], then the same binning; it is labelled
  "extrapolated, not a run" everywhere. (625 and 650 are reported only.)
- **Prediction error.** Bootstrap over L388's 120 pooled halos (with replacement, B = 2000, seed 3300; a resample with an
  empty bin is redrawn), nodes recomputed, groups re-interpolated. Each MC draw i of the data side is paired with
  bootstrap set i mod B.
- L388 ran at canonical a0 only; the same retention is used on both footings (disclosed). The data side differs by
  footing.

## 4. The data side: UA1's joint posterior, per group (frozen)

UA1's groups machinery is reused unchanged: NDRAW = 20,000, SE2's stat / nuisance streams and UA1's new-knob stream
(f* ~ U[0, 1], IMF lambda and sigma_star, b_nt ~ U[0, 0.20], d_f, c_g, cross-catalogue shift m_G), single widths.
- **Per-group need eps_need,g (per draw):** the eps that makes the mean of group g's two point residuals zero,
  residual = D - dlaw(b_IMF + R_c eps, gN, a0), by bisection on eps in [(0.01 - b_IMF) / R_c, 10] (negative eps =
  the law already over-predicts; kept, not clipped, so the slope is unbiased). Per-group posteriors (median, 68 %, 95 %)
  are reported.
- **Data slope b_data (per draw):** OLS slope of eps_need,g against log10 M500,g over a bootstrap resample of the 20
  groups (own stream, seed 3301 + 0 canonical / 1 alt). Units: eps per dex of M500.
- **Predicted slope b_pred:** OLS slope of eps_pred,g against log10 M500,g over the 20 groups, per bootstrap set; reported
  as median and 68 % half-width (its error).

## 5. Tests, pass lines and labels (per v_k, per footing; stated in advance)

- **A (slope):** Delta_i = b_data,i - b_pred,(i mod B). **A passes iff the 95 % central interval of Delta contains 0.**
- **A power (MUTATE, flat retention):** flat model eps_flat = the mean of eps_pred,g over the 20 groups (same level,
  slope 0). Delta_flat = b_data - 0. **The flat model must FAIL A** (95 % interval of b_data excludes 0). If it passes,
  test A has NO POWER.
- **B (level, the class step):** UA1's statistic (median residual over the 40 points of the bootstrapped groups, full
  budget) with b_tot = b_IMF + R_c eps_pred,g (paired bootstrap set). **B passes iff its 95 % central interval contains
  0** (UA1's EXPLAINED rule). B has power on the record (UA1: raw stat-only interval excludes 0 -> NOT EXPLAINED).
- **Label:** FAIL if B fails, or if A is powered and fails. PASS if B passes and A is powered and passes. NO POWER if B
  passes and A is unpowered.
- Reported only: B with the flat model; per-group count of groups whose eps_need 95 % interval contains eps_pred
  (median); the sensitivities in sections 1-3; v_k 625 / 650.

## 6. Known answers (a KA failure stops grading)

- **KA1 (L388 to 0):** the per-halo medians in L388's bins at 575 / 600 / 625 / 650 equal the committed
  retention_by_mass values and counts exactly (difference 0).
- **KA2 (UA1 to 0):** with eps = 0 (no carrier) the CK3 class-step posterior equals UA1's post_groups2 draw for draw
  (array_equal), and its summary equals ua1.json's groups post exactly, both footings.
- **KA3 (XR13 placement):** XR13's m_1mpch puts exactly 5 of the 20 groups below L388's lowest bin edge (6e13).

## 7. Outputs

ck3.py -> ck3.json / ck3.out (KA1-KA3, per-group table, A, B, labels) and ck3_MUTATE.out (the flat-retention
model's A and B). Small files, no arrays beyond 20-row tables, no home paths. Peak RSS reported (line: < 1 GB). Any
change after this freeze is a numbered, dated amendment in RESULT.md.

Kappa = 1/2 FITTED; not theory closed.
