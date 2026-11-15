# CLR1: does form B close the cluster residual that plain MOND leaves (Combes, 106 HIFLUGCS clusters)? FROZEN CRITERIA

Committed alone, before any CLR1 script exists and before any CLR1 number is computed. TEST lane: it adopts nothing, relabels
nothing, never edits the scorecard or other lanes' files. kappa = 1/2 FITTED; not theory closed. Footings canonical
(a0 = 9.3603e-11 m/s^2) and alt (a0 = 1.1312e-10 m/s^2), graded side by side, never pooled. Cold dark energy is a gravitating
field component with w about 0, never a particle, never called cold dark matter. Nothing here says the data favour the framework.

## 0. The question and the paper

Combes, arXiv:2611.08702v1 (5 Nov 2026), "Modified Newtonian Dynamics and galaxy clusters": on the extended HIFLUGCS sample
(106 clusters and groups, Chen et al. 2007), hydrostatic Newtonian masses from beta models, MOND (RAR function, a0 = 1.2e-10)
lowers the needed mass by 4-10x; a residual "dark" mass of about half the gas mass remains, concentrated inside a core of
20-30 kpc in cool-core clusters. The paper tabulates no per-cluster numbers (plots only; the SI appendix is not in the arXiv
file). **Its inputs are public per cluster:** Chen et al. 2007 (A&A 466, 805; arXiv:astro-ph/0702482) Tables 1-5 give, for all
106, z, T_m, beta, r_c, n_center, t_cool, Mdot (Tables 1, 2), double-beta fits for the 49 that need them (Table 3), and T_h, L_X,
M500, r500, f_gas, M_gas,500 (Tables 4, 5). So CLR1 rebuilds Combes's setup cluster by cluster, checks it against her
aggregates, and grades form B on the same profiles. VizieR has no copy of these tables (queried 2026-11-14: "Table or Catalog
not found: J/A+A/466/805"); the arXiv TeX source is the only machine-readable copy found.

## 1. Inputs (hashes; downloads untracked under `_external_data/clr1_combes/`, data only)

| id | what | sha256 |
|---|---|---|
| I1 | Combes 2026, `paper/combes_2611.08702.pdf` (arxiv.org/pdf/2611.08702v1) | fbe00afc3302a4ca37b46965826e3a9aee36b9d53d2d0f3e8cf325c76515dac6 |
| I1h | same, `paper/combes_2611.08702.html` (arxiv.org/html/2611.08702v1) | 359c77077dbf29ba1037e0f6c178b7a9c7bde9782591eabebe1f45f1a55dd573 |
| I2 | Chen et al. 2007 source, `chen2007/src.tar` (arxiv.org/e-print/astro-ph/0702482) | 5fdf14427f2c0ce1fa46210faf053e986488d3733fe8b0caa49c7dfdbe744d26 |
| I2t | its `chenyAAfinal.tex` (Tables 1-5 at TeX lines 565-1000) | f37cba9c78f84f712117beb50d894f654289836eadb4c201cad21e8071567bc2 |
| I3 | ZN4 native cold shape `rebuild_2026_10_22/ZN4_cluster_resolution/zn4_shapes.json` (read only) | 3f979d4fe532998e1dbb29d9ec54485888695e1edca9e54353f4ec5610fc37ab |
| I4 | footing backgrounds `closure_2026_11_06/QX15_cmb_primary_likelihood/qx15.json` (h, omega_b, omega_d) | 587c6b00716a6116e59bb23fc4b0006c679f5f615fdf4a796b7bcf64102b144b |
| I5 | X-COP files `real_research/data/xcop/` (KA-X and the overlap cross-check only); `xcop_r500_ettori2019.json` | 0b7d69463b1a55ae96380203a788e5f2f20dfe118652f3bd769d74da7dc6a20d |

- **Transcription.** `clr1_transcribe.py` (written after this commit) parses Tables 1-5 of I2t into the tracked
  `clr1_chen2007_inputs.csv`, one row per cluster, every value with its source (table number and TeX line). Combes's aggregate
  numbers are typed into the tracked `clr1_combes_aggregates.csv` with their location (abstract / section / table / line of
  `combes_raw.txt`, the pdftotext dump of I1). Parse checks (each must hold or the lane stops): 106 clusters (Tables 1+2),
  106 rows in Tables 4+5 with matching names, 49 rows in Table 3, every Table 3 name present in Tables 1/2.
- **Data convention of I2:** H0 = 50 km/s/Mpc, Omega_m = 1, Omega_L = 0 (TeX line 155); r500 is where the mean density is
  500 rho_c; errors 68 % except T and L_X at 90 %. Combes states no H0; KA-C below tests her numbers on I2's frame as published.

## 2. Recipe (Combes's setup, rebuilt; all in SI)

Constants: G 6.67430e-11, m_p 1.67262192e-27 kg, keV 1.602176634e-16 J, Msun 1.98841e30 kg, kpc 3.0856775814913673e19 m,
mu = 0.61. Radial grid per cluster: 60 points log-spaced from 20 kpc to R500 (plus R500 itself).

1. **Gas density shape.** Single beta (Table 1/2 beta, r_c) or, for the 49 Table 3 clusters, Chen's double beta:
   n(r)^2 = n01^2 a1^(-3 b1) + n02^2 a2^(-3 b2), a_i = 1 + (r/r_ci)^2, with n0i^2 proportional to S0i / (r_ci B_i),
   B_i = sqrt(pi) Gamma(3 b_i - 1/2) / Gamma(3 b_i) (the projection integral of a beta model). Only the ratio n01/n02 enters.
2. **Gas mass.** M_gas(<r) = integral of 4 pi r^2 n(r) dr, normalised so that M_gas(<r500_Chen) = Chen's M_gas,500 (Table 4/5).
   (Bracket G1: normalised from n_center instead, rho_gas = 1.17 m_p n_e.)
3. **Hydrostatic Newtonian mass.** M_dyn(<r) = -(k T(r) r / (mu m_p G)) (dlnT/dlnr + dln n/dlnr), T_h from Table 4/5 (values in
   parentheses, estimated by Chen from L_X-T, used as given). **Cool cores** (Mdot > 0, Combes's weak-CC + CC): T(r) =
   T_h (0.8 + 0.2 r / r_T) for r < r_T and T_h beyond, r_T = 0.1 r500 (Combes: "a linear increase with radius, with the central
   gas temperature 20% lower"; she does not give the radius; brackets T3, T4). NCC: isothermal T_h.
4. **Stars.** Galaxies: Giodini et al. 2009, f_star,500 = 0.05 (M500 / 5e13)^-0.37, total f_star,500 M500 inside R500,
   radial shape that of M_dyn (galaxies trace the total mass; Combes does not say; bracket S3). BCG+ICL: DeMaio et al. 2020,
   log M*(<100 kpc) = 0.37 log(M500 / 2e14) + 11.92, Hernquist M(<r) = M_H r^2 / (r + a)^2 normalised to M* at 100 kpc,
   a = R_e / (1 + sqrt 2), **R_e = 30 kpc** (Combes gives no R_e; brackets S1). M_vis = M_gas + galaxies + BCG+ICL.
5. **Combes's MOND.** RAR: g_obs = g_bar / (1 - exp(-sqrt(g_bar / a0))), a0 = 1.2e-10, inverted numerically for g_bar given
   g_obs = G M_dyn / r^2; M_MOND = g_bar r^2 / G; M_dark = M_MOND - M_vis. Simple function bracket: g_obs = g_bar nu(g_bar/a0),
   nu(y) = 1/2 + sqrt(1/4 + 1/y) (Combes's mu = x / sqrt(1 + x^2) is NOT this; she writes nu^2 = (1 + sqrt(1 + 4/y^2)) / 2, used
   for KA-C2 exactly as she writes it).
6. **Frames.** (i) **Combes frame**: I2's numbers as published (H0 50, EdS), used for KA-C only. (ii) **Footing frame (graded)**:
   each cluster rescaled by s = D_A(z; footing) / D_A(z; H0 50 EdS), footing h and Omega_m = (omega_b + omega_d) / h^2 from I4,
   flat, w = -1 background: lengths x s, M_dyn at fixed angle x s (T fixed), M_gas at fixed angle x s^(5/2); then R500 re-solved
   from M_dyn with rho_c(z) of the footing; Giodini and DeMaio re-evaluated at the new M500. **a0 at each cluster's z by the
   record's convention:** a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) = 1 for w = -1 (FINAL15, AZ2), so a0 is the footing's constant.

## 3. The four rows, as required / predicted mass (dynamical-mass space)

Per cluster and radius, Q = M_dyn(<r) / M_pred(<r); log10 Q > 0 means mass still missing (residual remains), < 0 over-prediction.

| row | M_pred | footing-dependent? |
|---|---|---|
| Newton baryons | M_vis | no |
| Combes MOND (RAR, a0 1.2e-10) | g_RAR(G M_vis / r^2) r^2 / G | no (reported beside) |
| law only (record's mu = x/(1+x), footing a0) | glaw(G M_vis / r^2, a0) r^2 / G, glaw(g) = g/2 + sqrt(g^2/4 + a0 g) (RB1's) | **yes** |
| **form B (graded)** | M_vis + M_cold; Newtonian gravity, no law boost on hot gas, no EFE (RB1 section 0) | only via h (1e-4) |

**Form B's cold.** M_cold(<r) = f_c M200 m(r / R200), f_c = R/(1+R), R = 5.41, m = ZN4's native z = 0 shape (I3) interpolated in
log M200 between the 1e14 and 1e15 stacks, M proportional to r^2 below the tabulated x, constant beyond x_edge; R200 solved
from the anchor (RB1's `m_native` and `solve_R200` COPIED, with the footing's rho_c instead of h 0.7 / Omega_m 0.3). Two anchors:
- **A1 (amount; outer cell):** cold(<R500) = R M_vis(<R500), i.e. f_ret = 1 at R500: B's minimum cold with nothing lost. At R500
  Q_B = M_dyn / ((1+R) M_vis) exactly. Q_B < 1 there breaks B's ceiling (a hard fail); Q_B > 1 is B's one-sided allowance
  (baryons lost), stated as "residual remains, B's retained cold does not close it", never as proof the baryons were lost.
- **A2 (location; middle and core cells):** cold(<R500) = M_dyn(R500) - M_vis(R500) (0 if negative): the amount the edge needs,
  so the inner cells test only where B puts its cold against where the mass is needed (Combes's question (b)).
- The central galaxy's phantom is part of the cold, not an addition (RB1); no extra term.

## 4. Statistic, cells, sigma budget, words

- **Classes (Combes's Table 2 rule on Chen's Mdot):** NCC Mdot = 0; weak-CC 0 < Mdot < 60; CC Mdot > 60 Msun/yr. Graded per
  class, never pooled (All reported).
- **Regions (cells):** OUTER: log Q at R500 (A1). MIDDLE: per-cluster median log Q over grid points in [0.1, 0.5] R500 (A2).
  CORE: per-cluster mean log Q over grid points in [20, 30] kpc (A2). 3 classes x 3 regions = 9 graded cells per footing.
- **Cell statistic:** median over the class's clusters of per-cluster log10 Q; 95 % interval from 10,000 bootstrap resamples of
  clusters (seed 1114). Per-cluster measurement errors are not propagated (the spread among clusters holds them, as RB1).
- **Sigma budget (systematic band):** |log Q| <= 0.08 dex (20 %): temperature calibration about 10 % (0.04 dex) and hydrostatic
  bias of 0-20 % (half range 0.05-0.1 dex) in quadrature. Statistical part = the bootstrap interval.
- **Cell word:** RESIDUAL REMAINS if the interval's lower end > +0.08; OVER-PREDICTS if its upper end < -0.08; CLOSED otherwise.
  NO POWER if the interval's half-width > 0.15 dex. NOT EVALUABLE if < 5 clusters, or **DATA-INCONSISTENT** if the Newton
  baryons row in that cell OVER-PREDICTS (visible mass above the hydrostatic total: no model adding non-negative mass can fit;
  excluded from the word, reported).
- **Word per footing (form B):**
  - **"FORM B CLOSES THE RESIDUAL"** iff every evaluable graded cell is CLOSED and at least one cell per region is evaluable.
  - **"STILL FAILS [cells, direction]"** if any evaluable cell is RESIDUAL REMAINS or OVER-PREDICTS (listed with direction).
  - **"NO VERDICT"** if a cell's bracket set (section 5, counted brackets) contains both RESIDUAL REMAINS and OVER-PREDICTS while
    the central run calls it CLOSED, or if any cell would decide the word but is NO POWER.
  - **NOT EVALUABLE** only if fewer than 5 clusters per class survive the parse (it will not apply if the parse holds).
  - **FRAGILE** appended if any single counted bracket changes the footing's word.
- Combes MOND, law only and Newton get the same cell words, printed beside (law only per footing). They do not enter B's word.

## 5. Brackets (written before the run; each rerun in full, footing frame)

Counted toward FRAGILE / NO VERDICT:
- **H (hydrostatic bias):** M_dyn / (1 - b), b = 0.1 and 0.2.
- **S1 (BCG+ICL):** R_e = 15 and 60 kpc; **S2:** DeMaio M* x 2 and / 2 (M/L and ICL extent). **S3 (galaxies):** Giodini x 1.5 and
  / 1.5; galaxy profile following the gas instead of M_dyn.
- **G1 (gas extrapolation):** gas from n_center (rho = 1.17 m_p n_e) instead of Chen's M_gas,500; **G2:** single beta for all 106.
- **T1 (temperature calibration):** T x 0.9 and x 1.1. **T2:** T_m instead of T_h. **T3:** cool-core gradient off (isothermal);
  r_T = the single-beta r_c. **T4:** central T = 0.5 T_h (a strong cool core; Combes calls lower central T unphysical, stated).
- **R:** R = 5.562. **N1 (native shape, inner):** below x = 0.05 the cold continued with the shape's own log slope over
  x = 0.05-0.1 instead of the tabulated inner profile (red-teams the zooms' inner resolution).
- **P (core resolution):** core cell restricted to clusters where 25 arcsec (ROSAT PSPC) is <= 10 kpc.
Reported only (not counted): Combes frame (h 0.5, EdS) for every row; h 0.7 / Omega_m 0.3 (X-COP convention); NFW with Duffy
2008 c200 in place of the native shape (EXTERNALLY CALIBRATED); A1 in the inner cells and A2 at R500; Combes's simple function.

## 6. Red-team of the data team's assumptions (stated before the run)

- **Hydrostatic equilibrium and spherical symmetry** (Chen, Combes): non-thermal pressure biases M_dyn low by 10-20 % at R500
  (bracket H), larger in mergers (NCC). Galaxy-kinematic masses for HIFLUGCS differ by up to 50-80 % (Combes 3.2): reported, not
  bracketed. Mass at 20-30 kpc from a beta fit is a fitting-function extrapolation, not a measurement.
- **ROSAT PSPC resolution:** about 25 arcsec on axis, worse in RASS (36 clusters): at z 0.05 that is about 25 kpc, i.e. the core
  cell is at the resolution limit for most clusters (bracket P). The core radius r_c of a CC cluster is about 30 kpc, so
  Combes's "residual concentrated within 20-30 kpc" sits where the gas profile is least constrained.
- **Temperature:** ASCA two-temperature T_h (90 % errors), 14 of 106 from L_X-T; a single global T applied at 20 kpc. Real cool
  cores fall to 0.3-0.5 T_h, which lowers the inner mass through T and raises it through dlnT/dlnr (brackets T1-T4).
- **Gas extrapolation to R500:** ROSAT beta models extrapolated; outer slopes steepen beyond r500 in XMM/Chandra profiles, so beta
  models overstate M_gas near R500 (bracket G1, G2; X-COP overlap check below).
- **BCG + ICL:** scaling relation, no per-cluster photometry; M/L and the ICL extent change the core by factors of ~2 (S1, S2).
- **h:** Chen's H0 = 50 makes f_gas proportional to h^-3/2 about 1.6x higher than at the footing h; whether Combes rescaled is not
  stated (KA-C decides which frame reproduces her numbers; the graded frame is the footing's either way).
- **X-COP overlap (reported):** 11 HIFLUGCS clusters are X-COP clusters (A85, A644, A1644, A1795, A2029, A2142, A2255, A2319,
  A3158, A3266, ZwCl1215). Their beta-model M_dyn and M_gas (rescaled to X-COP's h 0.7 / Omega_m 0.3) are compared with X-COP's
  M_FORW and M_GAS at 0.3, 0.5 and 1.0 R500(Ettori): median log ratios printed.

## 7. Known answers (each can fail; a failure stops the lane before any word)

- **KA-P (parse):** section 1's counts; class counts NCC / weak-CC / CC = 56 / 25 / 25 exactly (Combes Table 2).
- **KA-U (units, in SI):** (a) Chen's M500 reproduced from T_h and the beta fits (isothermal, Chen's formula) at Chen's r500 in
  the Combes frame: median ratio within [0.97, 1.03] for single-beta clusters and within [0.95, 1.05] for double-beta clusters;
  (b) M500 / (4 pi/3 r500^3) / rho_c(z), rho_c(z) = rho_c0(H0 50) (1+z)^3, median within [450, 550]; (c) a hand value: A0085's
  Newtonian 3 beta k T r / (G mu m_p) asymptote in Msun printed and checked against a second, independent evaluation in cgs.
- **KA-C (Combes's own MOND residual, Combes frame, RAR, a0 1.2e-10):** her radius for "M_dark/M_MOND on average 0.41" is not
  stated, so two definitions are printed: D1 both at R500 (negative dark allowed); D2 plateau dark mass max(delta M(r <= R500))
  over M_MOND(R500). **KA-C1:** the mean over 106 lies in [0.33, 0.49] under D1 or D2. **KA-C2:** with her simple function and the
  same definition, the mean lies in [0.45, 0.61] and exceeds the RAR mean. **KA-C3:** median M_dyn / M_MOND at R500 in [3, 10]
  (she writes 4-10 and 4-20). **KA-C4:** median M_dark / M_gas at R500 (same definition) in [0.3, 1.0] ("roughly twice lower").
  Tolerances are wide because she gives no R_e, no r_T, no galaxy profile and no H0; stated plainly. If KA-C fails in the Combes
  frame, it is also tried in the footing frame and reported; the lane stops before any word only if it fails in both.
- **KA-X (RB1 X-COP, code COPIED from RB1R's `rb1r.py`):** f_ret at the last kept gas-grid radius, M_FORW, R 5.41, for A1795,
  A2029, A2142, A2319, A644, A85, ZW1215: 0.885, 0.934, 1.235, 1.259, 2.216, 1.095, 0.511 each to 0.001, median 1.095.
- **KA-I (identities):** form B under A1 gives Q_B(R500) = M_dyn / ((1+R) M_vis) to 1e-8; m_native(1) = 1 to 1e-3; the RAR
  inversion round-trips to 1e-10; with a0 -> 1e-30 the MOND rows equal the Newton row to 1e-8.

## 8. MUTATE and null twin (separate outputs `clr1_MUTATE.out` / `.json`)

- **M1 (must bite):** cold shape stretched r x 3 under A2: the CORE cells must move by >= 0.10 dex (the core test can see the
  cold's shape). If not, the CORE region is NO POWER for B.
- **M2 (must bite):** Combes's recipe with a0 -> 1e-30: KA-C1's statistic must leave [0.33, 0.49] under the definition that
  passed (the KA can fail).
- **M3 (must bite):** R x 2 under A1: every OUTER cell must move by >= 0.15 dex.
- **Null twin Z1 (must not bite):** radial grid 240 points instead of 60 and bootstrap seed 1115: every graded cell median moves
  < 0.01 dex and no cell word changes. **Z2:** canonical vs alt B rows equal to 0.005 dex.

## 9. Hand estimates (before any number)

- Footing frame: Chen's f_gas about 0.16 at h 0.5 becomes about 0.10 at h 0.674 (x 0.64); Giodini stars about 0.02 at
  4e14; BCG about 0.003. M_vis / M_dyn about 0.125 at R500, so Q_B(R500) about 8 / 6.41 = 1.25 (+0.10 dex): OUTER on the
  RESIDUAL REMAINS side of the line, borderline, and FRAGILE to hydrostatic bias the other way only if b < 0. 45 % OUTER
  RESIDUAL REMAINS in at least one class, 10 % over-predicts.
- MIDDLE: RB1's gate 3 found the native shape within 0.04 dex of X-COP inside R500; 70 % CLOSED.
- CORE: the native shape is m proportional to x^2 below x about 0.02 (seen in I3 when reading the keys), so at 25 kpc B's cold
  is about 1-2e12 Msun; a CC beta model at 6 keV, r_c 30 kpc, gives M_dyn about 4e12 there and M_vis about 5e11 -> CC CORE
  RESIDUAL REMAINS (+0.3 dex), 65 %. NCC CORE: r_c about 300 kpc gives M_dyn below the BCG at 25 kpc -> DATA-INCONSISTENT, 70 %.
- Overall: 65 % STILL FAILS [CC core, residual remains], likely FRAGILE under T4 / S2 / N1. 15 % CLOSES.
- Combes's MOND: residual +0.15 to +0.25 dex at R500 in the footing frame (larger than in her frame); law only larger again
  (smaller a0, mu = x/(1+x)). KA-C1: 65 % passes in the Combes frame.

## 10. Seen before freezing (disclosed)

Combes's full text (pdftotext and the arXiv HTML, two WebFetch summaries); Chen's Tables 1-3 and the first rows of Tables 4-5
printed in the terminal while locating them (values seen by eye, not computed on); RB1's criteria, A1 and RESULT; RB1R's
RESULT_BLIND and `rb1r.py` (loader); RB1's `m_native` / `solve_R200` code; ZN4 m(x) at x 0.01-1 for both stacks; footing h
(0.67408 / 0.67400). One hand check of Chen's r500 convention on A0085 (mean density / rho_c0 = 586, / rho_c0 (1+z)^3 = 498).
No CLR1 Q, residual, class statistic or word has been computed.

## 11. Limits (stated now)

Aggregate check only against Combes (she tabulates no per-cluster values); her unstated choices are frozen here and
bracketed. Beta-model hydrostatic masses from ROSAT/ASCA, 2007 calibration. Form B is graded as RB1 froze it (R fixed, native
cold shape, Newtonian gravity in clusters); no EFE, no lensing, no non-thermal pressure model. A residual at the edge is B's
one-sided allowance, not a falsification; only an OVER-PREDICTS outer cell breaks B's ceiling.

## 12. Operational

`python3 -I -B`, paths as arguments, one thread, nice; light compute. Files: `clr1_transcribe.py` -> `clr1_chen2007_inputs.csv`,
`clr1_combes_aggregates.csv`; `clr1.py` -> `clr1.out` / `clr1.json`, `clr1_MUTATE.out` / `.json`; `RESULT.md`. Commits local,
explicit paths, order: criteria, scripts, results; subjects carry no outcome word. Not pushed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
