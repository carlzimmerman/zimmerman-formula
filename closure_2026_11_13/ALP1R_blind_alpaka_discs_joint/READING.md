# ALP1R READING (frozen criteria): the crossing-speed joint on the ALPAKA I ring curves, blind build

Written 2026-11-13 and committed ALONE, before any script of this lane exists and before any number of this lane is
computed. TEST lane: adopts nothing, relabels nothing, registers nothing. Footings canonical (a0 = 9.3603e-11 m/s^2) and alt
(1.1312e-10 m/s^2), graded separately, never pooled. Cold dark energy is a gravitating field component; no particle.
kappa = 1/2 and the share 5.41 are FITTED. One thread, under 2 GB. No downloads. ALP1 (same question, other agent) is not
opened until RESULT_BLIND.md is committed.

## 0. What I read before this freeze (blindness record)

- JNT2 `FROZEN_CRITERIA.md`, `RESULT.md` and `jnt2_common.py` (boundary, primary membership rule).
- DSC1 `FROZEN_CRITERIA.md` at 34edc4c9e7 only (`git show`), and DSC1's `dsc1.py` by grep and lines 20-70 only, to locate the
  ALPAKA files and the reference-halo code (SRJ3's construction). I saw no DSC1 number. DSC1's folder listing showed its
  RESULT.md and outputs exist; none was opened. The ALP1 folder was seen to exist in a directory listing; nothing in it was
  opened.
- SRJ3 `RESULT.md` and `srj3.py`; SRJ2 `srj2_rc.py` lines 1-50 (the halo construction).
- ALPAKA files: `data_assembly/arxiv_tables/alpaka1_{sample,properties,geometry,kinematics,alma_obs}.csv`,
  `alpaka1_digitised/` (README, checks, outer summary, ring file), `alpaka_jwst2026_*.csv`, and the README rows on ALPAKA.
- Earlier high-z disc lanes, for conventions: CFG272 README and criteria (grep), CFG229 README and criteria (grep) and its
  `cfg229_inputs_static.csv` (Dunne+22 gas rows for ALPAKA 15, 18, 19, 20, 22), the ADF22.5 look-up record
  (`data_assembly/adf22_5_literature_2026-10-02/`, values read directly from PDFs in an earlier, owner-approved lane).
- **Not blind to the order of magnitude:** CFG229's README states that with SED stars and Dunne+22 gas, ALPAKA 15, 18, 19,
  20, 22 have g_obs / g_bar = 0.20 to 0.46 at R_ext (baryons ABOVE the dynamics), and CFG272 that 13 and 23 have stars-only
  D 0.44 / 0.86. I have seen these; they shaped the floor rule in section 6. I computed nothing from them.
- No memory file other than the five named in the brief. No web page was read for this lane (section 3 says why).

## 1. Sample: every ALPAKA disc with a ring curve on disk

19 discs (the paper's secure discs), IDs 1, 2, 3, 6, 7, 8, 9, 11, 12, 13, 15, 18, 19, 20, 22, 23, 24, 25, 28, at z 0.561 to
3.630 (10 of them at z >= 2: 13, 15, 18, 19, 20, 22, 23, 24, 25, 28). The brief says "19 at z 2.2 to 3.6"; the files hold
19 at z 0.56 to 3.63. **Primary sample = all 19** (the joint's statement is about which side of v*(z) a disc is on, at any
z); the z >= 2 subset is reported.

| file | what it is |
|---|---|
| `alpaka1_digitised/alpaka1_vrot_digitised.csv` | every ring: R (arcsec, kpc), V_rot or sigma (panel V / sigma), plotted 1-sigma band edges; digitised from the paper's raster figure (arXiv:2303.16227 `vrot.png`), validated against the table V_max / V_ext (median 0.7 / 0.8 %); 2 to 5 rings per disc, 61 velocity rings |
| `alpaka1_digitised/alpaka1_outer_summary.csv` | R_ext and the dashed optical R_e where the paper drew it (IDs 1, 6, 8, 9, 18, 20, 28) |
| `alpaka1_properties.csv` | M* (authors' STARDUST SED, Chabrier; AGN templates for AGN hosts), e_M*, MS / SB type, line luminosity L' of the observed line (1e10 K km/s pc^2, no excitation correction) |
| `alpaka1_alma_obs.csv` | observed line per disc (CO(2-1) ... CO(7-6), [CI](1-0), [CI](2-1)), beam |
| `alpaka1_geometry.csv` | inclinations i_HST, i_ALMA with errors; the footnote star |
| `alpaka1_kinematics.csv` | V_max, V_ext, sigma_ext (for the measured-speed rule) |
| `data_assembly/adf22_5_literature_2026-10-02/*.csv` | ID 24 (ALPAKA has no M*): M* 10^10.64 (Huang+25 / Umehata+26 Table 1), measured L'CO(1-0) 10^10.66, F444W fixed n = 1 R_e 1.55 kpc (semi-major); read directly from PDFs by an earlier approved lane |
| `campaign_fresh_gravity/CFG229_class_m_gold/cfg229_inputs_static.csv` | Dunne+22 optimised-tracer gas (1.36 x 10^logMH2) for 15, 18, 19, 20, 22: a reported bracket only |

Rings are the authors' 3D tilted-ring (3DBarolo) values, beam-modelled: no beam cut (reported: the count of rings inside
half the beam major axis).

## 2. Baryon model per disc (frozen)

- **Stars:** M* from `alpaka1_properties` (ID 24: 10^10.64 from the ADF22 record). One thin exponential (Freeman) disc,
  R_d = R_e / 1.678. **No bulge**: no bulge mass on disk that is not a fit to these kinematics (the 2601.03338 bulges of
  IDs 1, 3, 13 come from a rotation-curve decomposition). Reported only: 30 % of the stars in a Hernquist bulge (a = 1 kpc / 1.815).
- **Stellar size R_e:** the dashed optical R_e where drawn (1, 6, 8, 9, 18, 20, 28); ID 24: 1.55 kpc (F444W, n = 1); else
  **R_e = R_ext / 1.2** (CFG227 / CFG229's rule; the median R_ext / R_e of the discs with both is 1.23). Declared, not measured,
  for 11 discs. Bracket RE-/RE+: R_e / 1.5 and x 1.5.
- **Gas mass (molecular only; HI neglected, stated as left out).** M_gas = alpha x L'_line / r, frozen now:
  - CO line ratios r_J1 = L'_J / L'_(1-0): r21 0.77, r32 0.54, r43 0.42 (Tacconi+2018's MS ladder), r54 0.32, r65 0.21, r76
    0.18 (an SMG ladder). **These six values are written from memory of the literature, not read in this lane: PROVISIONAL.**
    ID 24 uses its measured L'CO(1-0) directly (no ratio).
  - [CI]: alpha_CI(1-0) = 17.0 Msun / (K km/s pc^2) including helium (Dunne+22's value as I recall it: PROVISIONAL);
    [CI](2-1): L'(2-1) / L'(1-0) = 0.55 declared (PROVISIONAL), so alpha = 17.0 / 0.55.
  - alpha_CO (including helium): **4.36 for type MS and for ID 24 (unclassified)**; **0.8 for type SB** (DSFG / ULIRG
    convention; taken as total gas, as CFG272). For SB discs the [CI] alpha is scaled by the same 0.8 / 4.36.
  - Bracket **GAS-LO**: every disc at alpha_CO 0.8 (and [CI] alpha x 0.8 / 4.36) with r = 1 (thermalised): CFG272's floor B1.
    Bracket **GAS-HI**: every disc at alpha_CO 4.36 (MS value for SB discs too), ratios as primary.
  - Reported only (no FRAGILE): **GAS-D**, Dunne+22's per-galaxy gas for 15, 18, 19, 20, 22 (others primary).
- **Gas extent:** a second Freeman disc with the stellar R_d (high-z CO and stellar sizes are comparable). Reported only:
  gas R_d x 2 (CFG401's convention).
- **Stellar-mass bracket (frozen): MB- / MB+ = M* x 10^(-0.2) / 10^(+0.2)** (the gas is unchanged).
- **g_bar(R)** = the sum of the two discs' in-plane Freeman fields (Bessel form), R in kpc from the ring file.
- **Pressure support:** V_c^2 = V^2 + k x 3.36 sigma^2 (R / R_e) per ring with the ring's own digitised sigma; primary k = 1,
  brackets k = 0 and k = 2. Size by hand from the table at the outermost ring, 3.36 (R_ext / R_e) / (V_ext / sigma_ext)^2 with
  R_ext / R_e = 1.2 where not drawn: ID 1 0.009 (V/sigma 21); 2 0.011 (19); 3 0.11 (6, sigma an upper limit); 6 0.09 (6, ratio
  1.00); 7 0.16 (5, upper limit); 8 0.045 (11, 1.63); 9 0.022 (12, 0.79); 11 0.028 (12); 12 0.063 (8); 13 0.082 (7); 15 0.25 (4);
  18 0.060 (14, 3.50); 19 0.082 (7); 20 0.064 (7, 0.94); 22 0.063 (8); 23 0.009 (21); 24 0.033 (11); 25 0.11 (6); 28 0.31 (5,
  2.34, upper limit). So the term is < 10 % for 13 discs and 25 to 31 % for 15 and 28.
- **Inclination:** the inclination the authors deprojected with is taken as i_ALMA where the table carries the footnote star
  (IDs 3, 18, 22, 28), else i_HST, else i_ALMA (PROVISIONAL reading of the star; CFG229 says ALMA for 22). Its error sets a
  per-disc nuisance prior (section 4). Reported only: the other inclination.

## 3. Why no web reading

The numbers not on disk are the line ratios, alpha_CI, and 11 optical sizes. The sizes are not tabulated in ALPAKA I
(README: plots only), so a web read cannot supply them without per-galaxy papers; the ratios and alpha are conventions
whose spread is larger than any single reading would settle, and GAS-LO / GAS-HI cover it. So every such number is
DECLARED and PROVISIONAL, and the gas brackets are FRAGILE-gating.

## 4. Membership, statistics, power

- **Boundary:** v*(z) = a0 / (10 (1 + 5.41) H0 E(z)), H0 = 67.4 km/s/Mpc, Om = 0.3153, a0 constant; recomputed in SI.
- **Primary (JNT2's model rule):** above iff v_L = (10 G (1 + 5.41) M_b H(z))^(1/3) > v*(z), M_b = M* + M_gas of the primary
  baryon model (recomputed under MB-/MB+, GAS-LO/HI). **Bracket MEAS:** above iff the table's V_ext > v*(z).
- **Data per ring:** y = log10(V_c^2 / (km/s)^2); error e = sqrt((2 V e_V / (V_c^2 ln 10))^2 + 0.05^2), e_V = max(|band_hi -
  band_lo| / 2, 1 km/s).
- **Models:** reference g_A(R) = g_bar(R) + A G C_R(R) / R^2 with SRJ3's halo exactly (FRZ1's halo at the disc's z, M_ta =
  X M_b h / (1 - FB), X = XTAB[z >= 1 -> z1.0, else z0.0], C_R = X M_b m(r / r_s) / m(c_ta), r capped at r_ta), computed with
  SRJ2's `srj2_rc.py` prefix executed read-only (as SRJ3); A = 0 baryons only, A = 1 the record's share. Law: g = g_N / 2 +
  sqrt(g_N^2 / 4 + a0 g_N) with g_N = g_bar. Model y = log10(g R).
- **AMPLITUDE test (baryons fixed):** per disc a nuisance offset delta in log V^2 with a Gaussian prior sigma_inc = 2 log10(e)
  cot(i) sigma_i (sigma_i the mean of the two tabulated errors, radians; floor 0.02 dex), minimised analytically:
  chi2(A) = sum over discs of min_delta [sum_rings ((y - m_A - delta) / e)^2 + (delta / sigma_inc)^2]. A on 0 to 6, step 0.005.
- **SHAPE-ONLY test (free baryon scale):** per disc a free baryon scale mu (stars and gas together, the halo re-solved for
  mu M_b) with the prior log10 mu in [-1.0, +0.5] (grid step 0.02); no delta (mu absorbs it); chi2_S(A) = sum of per-disc
  minima over mu. Best mu per disc reported (the dynamics-implied baryon scale). Membership is NOT moved by mu (reported).
- **Scale and intervals:** s2 = max(1, chi2_min / (N - p)), p = 1 (amplitude) or 1 + n_discs (shape). 95 %: chi2 - chi2_min
  <= 4 s2; 68 %: <= s2. **Power: the 95 % interval excludes at least one of A = 0, 1, 2.**
- **Outer shape:** per disc S = y(outermost ring) - y(innermost ring); sigma_S = sqrt(e_out^2 + e_in^2). Group D = inverse-
  variance mean of (S_data - S_model); sigma_D = sqrt(s2 / sum(1 / sigma_S^2)). Shape line holds iff |D| <= 2 sigma_D. Computed
  for A = 1, best A, A = 0 and the law (in the shape test at each model's own best mu). Each curve's reach R_last / R_e is
  reported.
- **Baryon floor (frozen, from section 0's disclosure):** a group is AT THE BARYON FLOOR if the median over its discs of the
  median ring residual y - m_(A=0) (amplitude test, delta = 0) is below -0.15 dex. Then the amplitude test cannot weigh a
  halo (baryons alone already exceed the dynamics), and **the group's word is taken from the SHAPE-ONLY test**, said so in
  the label. Otherwise the word is the amplitude test's, and the shape-only word is reported beside it.

## 5. Labels per footing (primary membership)

ABOVE v*(z), from the gating test:
- **NO POWER** if fewer than 3 discs above, or the 95 % interval excludes none of 0, 1, 2.
- **JOINT'S STATEMENT HOLDS ON THE ALPAKA DISCS** (a HIT, not a pass) if A = 1 is inside the 95 % interval and the A = 1
  shape line holds.
- **JOINT'S STATEMENT FAILS ON THE ALPAKA DISCS** if A = 1 is outside the interval (side stated), or the A = 1 shape line fails
  while A = 0, the best A (< 1) or the law passes it. Say which of a lighter halo (best A < 1), the law and baryons alone
  (A = 0) fits (fits = within 4 s2 of the family minimum, the law by chi2_law - chi2_min, and its shape line holds).
- NO VERDICT (shape fits nothing) if A = 1 is inside, its shape line fails and nothing lighter passes.
BELOW v*(z), the word beside: **NO POWER** if fewer than 3 discs, or |chi2_law - chi2(A = 1)| < 4 s2 and both shape lines
give the same outcome; else **LAW HOLDS BELOW** if the law's shape line holds and chi2_law - chi2_min(A) <= 4 s2, else **LAW
FAILS BELOW**.
**FRAGILE** if any of k = 0, k = 2, MB-, MB+, GAS-LO, GAS-HI, RE-, RE+, MEAS changes a word. Reported only: GAS-D, the other
inclination, gas R_d x 2, a 30 % bulge, the cosmic-share halo (X = 5.41 instead of XTAB, re-solved), the z >= 2 subset.
The whole label is **NO VERDICT** if a known answer fails or a twin fails to bite.

## 6. Twins (separate `*_MUTATE*` outputs) and known answers

- **TW-N** (no cold component, C_R = 0): chi2 flat in A. Bites iff, in the gating test of the ABOVE group, the main run's
  chi2(2) - chi2(0) exceeds 4 s2 in absolute value (the halo carries information that TW-N removes) and TW-N's is < 1e-6; or the
  ABOVE word changes.
- **TW-D** (halo doubled, C_R x 2): bites iff the ABOVE word changes, or the 95 % upper bound of A (the best A when interior)
  moves by a factor 0.5 +- 0.15.
- **KA-B:** v*(0) = 668.53 / 807.93 km/s from SI constants (G 6.67430e-11, Msun 1.98892e30, Mpc 3.0857e22 m) to 0.01 km/s.
- **KA-S:** SRJ3's K5 g_mod for zC 400569 (RC100: z 2.24, log M_b 10.95, R_e 4.31 kpc, canonical, X = XTAB z1.0):
  g = G (M_b / 2) / R_e^2 + G C_R(R_e) / R_e^2 = 4.4288e-10 m/s^2 within 1e-3 relative, with my halo call.
- **KA-SI:** for one disc's outermost ring, g_bar (Freeman disc by independent numerical integration of the surface density
  in SI) and the halo term (NFW from rho_m and 200 rho_m, SRJ3's second route) within 1 %.
- **KA-D:** my ring loader reproduces the table's V_ext as the mean of the last two digitised rings within 2 % for every disc.

## 7. Expectation and hand estimate (frozen, before any number)

- v*(z) canonical: 669 / 488 (z 0.56) / 290 (z 1.45) / 211 (2.10) / 177 (2.50) / 142 (3.09) / 118 (3.63) km/s; alt x 1.208.
  log M* boundary: 12.66 (0.56), 11.76 (1.45), 11.62 (1.6), 11.20 (2.1), 10.91 (2.5), 10.61 (2.94), 10.51 (3.09), 10.20
  (3.63); alt + 0.083.
- Primary M_b by hand: ID 20 3.2e11 + 1.45e11 = 4.6e11; 15 2.5e11 + 1.8e11; 13 1.2e11 + 2.8e11 ([CI](2-1) at 17 / 0.55);
  19 8e10 + 6e10; 22 7e10 + 5e10; 23 5.3e11 + 4e11; 24 4.4e10 + 2.0e11; 25 1.1e11 + 4e10; 28 1.3e11 + 3e11; 18 1.2e11 +
  1.35e11. **So all 10 discs at z >= 2 are ABOVE on both footings; the 9 at z < 2 are BELOW** (IDs 3, 6, 7, 8, 9 near 2e11
  against 5.8e11 at z 1.45). Under GAS-LO the z >= 2 discs stay above (stars alone exceed the boundary for most).
- Amplitude: for ID 20 at R 3.5 kpc the stars alone give V ~ 470 km/s and the baryons ~ 570 against 220 observed; the
  record's CFG229 found D 0.2 to 0.5. **Expected: both groups AT THE BARYON FLOOR (P 0.85)**, so the words come from the
  shape-only test.
- Shape-only: 2 to 5 rings per disc reaching ~1.2 R_e (by the R_e rule) to 3.5 R_e (ID 18); inside ~5 kpc the halo grows like
  g ~ const while the disc field falls slowly, so shape alone weighs A weakly. Expect **ABOVE: NO POWER (P 0.55), FAILS
  with A = 1 too heavy (P 0.30), HOLDS (P 0.15)**; best mu ~ 0.2 to 0.5 (the baryon model 2 to 5 times heavy). **BELOW: NO
  POWER (P 0.6), LAW HOLDS (0.25), LAW FAILS (0.15).** FRAGILE likely (P 0.6) through GAS-LO or RE+/RE-.
- Twins: TW-D should bite if there is power; TW-N may fail to bite if the shape test has no A-information (P 0.35), which would
  make the label NO VERDICT.

## 8. Files

`alp1r.py` (one script; env `ALP1R_TWIN=N|D` writes `alp1r_MUTATE_TWN|TWD.json/.out`), `alp1r.json`, `alp1r.out`,
`RESULT_BLIND.md`, then `RESULT.md` (comparison). Paths relative to the script; no home paths. Owners' code executed
read-only from its own path; nothing written outside this folder.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
