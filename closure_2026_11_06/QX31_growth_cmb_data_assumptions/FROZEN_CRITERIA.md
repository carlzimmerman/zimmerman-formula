# QX31 frozen criteria: are the growth / CMB-lensing failures artefacts of LCDM assumptions inside the data products?

Frozen before any re-derivation number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Rules: ../SWARM_BRIEF.md.
Footings canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2, never pooled. The record's machinery is used read only
(imported or copied unchanged, with the source cited); no record file is edited.

## Step 0: what the record already audited (not redone here)

| Prior audit | What it covered | Use here |
|---|---|---|
| CFG917 (0289e4ad4, A1 187f895aa) | PR4 lensing package rule B = W X + M X - F; K3b' proves the PS1 fiducial correction = full linear-correction windows x FFP10; disclosure 2 lists FFP10 as the fiducial for normalisation, N1, MC correction and covariance, unsized | the rule is reused; the sizing against the WG/QX3 gaps is NEW |
| X22 ASSUMPTION_LEDGER (a2b532e3c6) | forest line = L346 bands (PM vs LCDM reference) + L319 WDM fitting formula (LCDM-calibrated), flagged | provenance reused; sizing vs the QX3/QX27/QX7 forest gaps is NEW |
| CFG885 (9e6fb31b8) | B21 KiDS ESDs carry flat-LCDM distances (Om 0.2793, h 0.70); native rescale T 0.968-1.062, no class flips | reused; the shift-statistic cancellation for QX7/QX10/QX27 G2 is NEW |
| E1_input_audit INPUT_LEDGER (doors_push_2026_10_22) | rows I01-I41 incl. I28 (B21 ESDs) | reused |
| CFG680-685 RAW BAO; CFG682 native Om 0.3085 | BAO from raw geometry | BAO is not graded by any failure in scope; listed only |
| QX15 KA-P2 side finding | profiling CamSpec nuisances moves chi^2 by 732 at the published test point | used as the computed size of foreground-nuisance freedom |

Not on disk / not consumed: ACT DR6 lensing bandpowers (no failing lane uses them; not on disk), fsigma8/RSD and S8
(no failing lane in scope grades against them; "growth" in QX3/QX27 is the PR4-lensing Delta chi^2 of a Jeans-suppressed
spectrum). Those rows are listed in ASSUMPTION_LEDGER.md as NOT CONSUMED.

## Admissible corrections (count toward a label)

A correction is admissible only if it is (i) documented by the data release, (ii) computable from the published products
on disk, (iii) framework-native (it moves the products from the LCDM fiducial to the framework's own model or to the
measured sky), and (iv) has no free knob.
- V1 (fiducial phi-phi response): grade with W only, i.e. without the published phi-phi linear correction M X - F. The record
  applies M X - F (CMB-marginalised). |S(V1) - S(V0)| is the size of the fiducial-C^phiphi dependence (normalisation and N1
  response) that the record already corrects; it bounds what a different fiducial choice could do.
- V2 (full non-marginalised PS1 linear correction): B = W X + sum_XY M^XY C^XY + M^PP X - F_PS1 with the PS1 covariance and
  the CMB spectra C^XY set to the measured sky, represented by FFP10's lensed spectra (the package's own reference; K2
  checks the windows' units by reproducing F_PS1). This replaces the CMB-marginalised constant (built at a package
  reference CMB) by the explicit correction.

## Bounds (reported, never count as admissible; they test robustness)

- V3 (most generous model covariance): Cov_bb' -> s_b s_b' Cov_bb' with s_b = max(1, B_b^model / d_b) evaluated at the
  amplitude being fitted (cosmic-variance inflation wherever the model exceeds the data; never shrinks). No knob: it is the
  upper limit of what a signal-dependent covariance could do.
- V4 (MC normalisation correction + foreground residual, documented sizes PROVISIONAL): add (0.05 d_b)^2 to each diagonal
  element (an uncorrelated 5 % per-bin freedom, larger than the few-percent sizes quoted for PR4).
- V5 = V3 + V4 together.

## Graded statistics and gaps (record numbers, reproduced by V0)

A. CMB-lensing SHAPE, law alone (WG2-WG6, wg6_shape_diag cases, plus the two alt-footing runs on disk:
   WG2 R1 TIE B2 2.1e-9 alt and WG4 R1 DE B2D 2.1e-9 alt). S = shape chi^2 after best amplitude (package rule, 9 bins,
   8 dof). Line L_A = chi^2_8(p = 0.01) = 20.09. Gap = S_record - 20.09. Also reported: per-bin model/data at L 28 and L 377.
B. QX3 iter2 G2 at the G1 worst corner (omega_b 0.0215, H0 65, n_s 0.95): mu_min on iter2's 26-point grid (record 25119)
   against mu_max 79.4 (G3, unchanged). Gap: log10(mu_min / mu_max) = 2.50 dex. Also Delta chi^2 at mu = 79.4 (line 4).
C. QX3 iter3 closest member (beta 1.4, mu0 1.585e4): Delta chi^2 92.59 vs 4.
D. QX27 G6b closest graded row (n 6 canonical, sigma0 1843.5 km/s, z_h 10, adiabatic): Delta chi^2 230.9 vs 4.
   (a0 does not enter B-D at linear order, QX3 assumption A-web: one computation serves both footings, stated.)
E. Record-sized only (no regrade possible or needed; computed from on-disk record numbers):
   - QX15 MB baryons-only primary CMB, Delta chi^2 +172,848 / +166,612 vs line 25; foreground freedom = QX15's own 732.
   - EB1b seeds: no clump collapses before z 0.48 (p05); QSO1 needs z >= 7.05.
   - KiDS lines (QX7 iter_4/5 G6, QX10 G6, QX27 G2): the graded statistic is a SHIFT in mean log(g_obs/g_pred) between two
     models on the same data; a multiplicative Sigma_crit/h rescale T of g_obs cancels exactly; only the radius
     conversion R = theta D_A moves, by delta ln D_A (native h 0.674, Om 0.3085 vs fiducial 0.70, 0.2793 at z_l 0.15-0.35);
     bound |delta shift| <= 3 |shift| |delta ln D_A| (enclosed-mass slope <= 3). Gap: QX10 shifts 0.15-0.27 vs 0.05.
   - Forest line (QX3 iter3 G4', QX27 G6c, QX7 G4'): the line 0.42/h Mpc is LCDM-hydro-calibrated (X22 ledger). Size of the
     thermal-history / emulator dependence = ratio of WDM half-mode lengths across the published bound range
     1.9-5.3 keV (PROVISIONAL range) through L319's formula. Gap: lambda_J(z 3) 490-1020 Mpc vs 0.646 Mpc (QX27).

## Label rule (per failure, per footing where it applies)

- ARTEFACT: an admissible variant (V1 or V2) flips the record's verdict (A: S <= 20.09; B: mu_min <= mu_max; C/D:
  Delta chi^2 <= 4; E: crosses its line).
- PARTIAL: no flip, but an admissible variant moves the graded statistic by >= 25 % of the gap (A: |dS| >= 0.25 gap;
  B: |d log10 mu_min| >= 0.625 dex; C/D: |d Delta chi^2| >= 0.25 (Delta chi^2 - 4); E: >= 25 % of the stated gap).
- ROBUST: otherwise. A ROBUST label also states whether the bounds V3-V5 flip it (if a bound flips it, the label is
  "ROBUST (admissible), NOT ROBUST to bound Vn", and the bound's non-admissibility is stated).
Sizing rule stated in advance: the WG1/WG6 shape miss is 14x at L 28 and 0.08x at L 377 (a factor ~175 across the band);
a few-percent normalisation, MC, foreground or distance effect cannot be an artefact of that size, and the README will say so
plainly if the numbers agree.

## Checks

- K1: package unit tests through this lane's code: CMB-marginalised FFP10 chi^2 8.37 (CFG917 K3e 8.3724) and non-marginalised
  PS1 at FFP10 8.705 (CFG917 K3b' 8.7094), each within 0.01.
- K2: F_PS1 = sum_XY M^XY C^XY_FFP10 + M^PP X_FFP10 per bin within 1e-3 relative (units check for V2).
- MUTATE twin (V0 = record rule): must reproduce wg6_shape_diag.out per-bin model/data (3 significant figures) and shape
  chi^2 (within 1); iter2 worst-corner G2 rows (within 0.05 in Delta chi^2) and mu_min 25119; iter3 closest 92.59 and QX27
  n 6 canonical 230.9 (within 0.1). Any miss: that part is NO VERDICT.
- MUTATE-bite: rerun with M scaled x10 (qx31_MUTATE outputs). The V1/V2 distances must grow by a large factor, showing the
  pipeline sees the correction terms.
