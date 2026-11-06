# QX18 frozen criteria: the a0 law on the 7 Humphrey+2006 X-ray ellipticals

Frozen before any QX18 script exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No dark-matter particle.
Rules: closure_2026_11_06/SWARM_BRIEF.md.

**Id.** The orchestrator asked for "QX17". closure_2026_11_06/QX17_covariant_field_equations already uses QX17
(d6c0fe3a0c), so this lane is QX18.

## Why

QX16 (closure_2026_11_06/QX16_elliptical_binding_fix/) fixed a late-binding bug. With each galaxy's own mass model,
the plain law's residual on these 7 galaxies is +0.210 (canonical) and +0.189 (alt) dex at 2, 4, 8 Re, Kroupa M*/L.
QX16 reported this and did not grade it. Later lanes graded these galaxies only as SHIFTS (G7). The baseline itself
has never been graded against a line on its own terms.

Prior record on the same galaxies, the same table (real_research/data/humphrey2006_ellipticals.tsv), and the same NFW+stars
models:

- h10 (hunt_2026/h10_h18_xray_hse.py) / FAILURES_EXECUTIVE_SUMMARY B4: median boost 1.69x / 1.57x short over 5-70 kpc,
  Kroupa.
- CFG32 (campaign_fresh_gravity/CFG32_README.md): +0.280 +- 0.165 / +0.254 +- 0.161 dex at 5-70 kpc, under its 2-sigma
  line with the IMF and radial-range floor: "large but not established". The shortfall grows outward in 7/7.
- RQ3 A26b: law +0.2802 / +0.2536, Z +1.70 / +1.58, under |Z| <= 2.

QX18 grades the 2, 4, 8 Re baseline against the G7 line, 0.15 dex, which later lanes used for these galaxies. It
neither replaces nor relabels CFG32. Its significance-based label stands as it is.

## Data and mass models

- **Observed total mass M_obs(r).** Humphrey's best-fit NFW + stars: M_vir includes the stars; M_h = M_vir - ups_fit
  L_K; NFW with c, R_vir; stars are a Hernquist profile with a = Re/1.8153 and mass ups_fit L_K. This is QX5's
  per-row-bound (fixed) function, unchanged. ups_fit enters only the observed total-mass model, which is the X-ray
  fit, never the baryons.
- **Baryons M_b(r) = Upsilon_pop L_K** in the same Hernquist profile. Hot gas is neglected: the repository has no
  deprojected gas profiles. Neglecting gas can only make the law under-predict MORE, so a positive offset is an upper
  bound on the law's miss. The gas mass each galaxy would need to null its offset is reported.
- **M*/L rule, fixed before grading.** The primary IMF is **Kroupa** (ups_krou). The record already fixed it for this
  sample before this test: h10, CFG32 (primary) and QX5's frozen criteria all use Kroupa. **Salpeter** (ups_salp) is
  reported as the IMF systematic. ups_fit is NOT allowed as the baryonic M/L: it was fitted jointly with an NFW halo,
  which makes it LCDM-processed.

## The law, and the action's field

- g = g_law(g_N) = g_N/2 + sqrt(g_N^2/4 + a0 g_N), QX5's glaw: the simple nu, whose inverse mu = x/(1+x) is certified
  in QX4's Lean file.
- M_law(r) = g_law(G M_b(r)/r^2) r^2/G.
- These are spherical models. In spherical symmetry the action's exact static (AQUAL) field equals the algebraic law:
  the curl term vanishes. QX11 uses the same spherical identity. So this test grades the action as well as the law.
- Two footings, never pooled: a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt) m/s^2.

## Statistic

- Per galaxy: d_i = mean over r = 2, 4, 8 Re of log10(M_obs(r)/M_law(r)).
- **Graded: D = mean of the seven d_i.** This equals the mean over all 21 points, QX16's statistic.
- Reported, not graded: the median of the d_i, all 21 points, the CFG32-style error (galaxy-to-galaxy std/sqrt 7
  combined with |D_Salpeter - D_Kroupa|), and the mass trend described below.

## Lines

Per footing, Kroupa primary:

- **PASS** if |D| <= 0.15 dex (the G7 line).
- **FAIL** if |D| > 0.15 dex. If D > 0 the law under-predicts.

The label is per footing. The Salpeter value is reported as the systematic; it does not set the label. The label
says exactly this: the a0 law on these X-ray ellipticals' published NFW+stars masses, Kroupa baryons, gas neglected,
graded at the G7 line. It is not a significance test, and CFG32's is.

## Mass trend (reported, informative)

- Spearman rank correlation of d_i against log M_vir, and against log L_K.
- Comparison with the record's group and cluster plain-law offsets (RQ3 B2 groups +0.16 / +0.35 at R500 / R2500
  canonical; X-COP +0.468 / +0.435 from QX2). Read as a ladder: ellipticals, then groups, then clusters.

## Known answer and controls (separate outputs)

- **KA1:** Kroupa D reproduces QX16's fixed +0.210 / +0.189 to within 1e-3 dex (QX16 prints 3 decimals).
- **KA2:** in the spherical case, the law-mode M_law at a test point matches an independent numerical AQUAL-identity
  evaluation, |g_law/g_N| times g_N, to 1e-12.
- **MUTATE M1 (Newton, nu = 1):** D must exceed 0.15 on both footings (FAIL), or the test has no power.
- **MUTATE M2 (planted +0.3 dex on M_obs):** D must shift by +0.300 +- 1e-9. A planted -0.3 dex shift must also move
  D by -0.300 +- 1e-9, and must change the label whenever |D +- 0.3| crosses 0.15.

If a MUTATE does not bite, no label stands.
