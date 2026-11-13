# DSC1 FROZEN CRITERIA: the crossing-speed joint on resolved outer rotation curves

TEST lane. Adopts nothing, relabels nothing, registers nothing. Written and committed alone, before any script of this lane
exists and before any number of this lane is computed. Footings never pooled (canonical a0 = 9.3603e-11, alt 1.1312e-10
m/s^2). Cold dark energy is a gravitating field component; no particle. kappa = 1/2 and the share 5.41 are FITTED. No
downloads, no web. One thread, under 2 GB.

## 0. The question

JNT2 / JNT2R (2026-11-13) both read JOINT FAILS ON G2 (coverage): with v*(z) = v*(0) / E(z), v*(0) = 668.5 / 807.9 km/s, the
massive RC100 discs at z 2.1 to 2.5 fall on the cold-dust (reference layout) side, and SRJ3 showed RC100's one point per disc
cannot weigh the halo. The joint's one distinctive statement is: **resolved discs ABOVE v*(z) follow the reference layout's
outer rotation curve (baryons + the reference cold dark energy halo at the record's share); discs BELOW follow the law.**
This lane grades that statement on every resolved outer curve on disk that meets the eligibility rule below.

## 1. Inventory and eligibility (fixed now from the READMEs, before any number)

Eligible = (a) per-point radius, velocity and error on disk; (b) extraction validated by its builder or used by a graded
record lane; (c) at least 4 points beyond the beam (or beam-corrected rings); (d) a baryon mass on disk that is NOT a fit to
the same kinematics; (e) a size and a dispersion for the pressure term; (f) a record lane has already built a baryon model
for these discs.

| set on disk | eligible here | why |
|---|---|---|
| Genzel+2017 six deep curves, `campaign_fresh_gravity/CFG400_genzel17_selfcal/cfg400_points.csv` (digitised from Fig. 1 of arXiv:1703.04310; PDF on disk outside the repo, sha256 9926059e...d5e4) with Table 1 as typed in CFG401's code | **yes (primary sample)** | graded by CFG400/401/402/405; Table 1 priors are SED + gas-scaling masses |
| Lelli+2023 zC-400569 and zC-488879, `data_assembly/lelli2023_rotcur_digitised/lelli2023_rotcur_digitised.csv` (read off a raster figure) with CFG278's baryons (SED M*, CO gas) | **zC-488879 yes; zC-400569's Lelli curve as a data bracket** (the same disc as Genzel's zC 400569) | CFG278 built the baryons |
| ALPAKA I rings (`data_assembly/arxiv_tables/alpaka1_digitised/`), CRISTAL (`.../cristal_vector/`), NOEMA3D (`data_assembly/noema3d/curves/`), KURVS (`.../kurvs_rc_profiles/`) | **no (inventory and membership only)** | no record lane built baryon models (gas conversion / line ratios / sizes) for their curves; CRISTAL's baryons are kinematic fits; KURVS has no gas measurement; NOEMA3D and KURVS curves are beam-smeared line-of-sight curves |
| SINS AO profiles (`data_assembly/sins_cubes/`) | no | extraction failed its own validation (C1) |
| KMOS3D cube fits, RC41 (Price+21), RC100, CFG568 | no | model parameters / one point per disc / archive metadata only |
| ALPINE rings (Jones+21) | no | 2 rings at ~1" (6-7 kpc) |

For the ineligible sets the lane reports, where a stellar mass is on disk, how many discs are above v*(z) on stars alone (a
lower bound on M_b), as "what data would".

## 2. Per-disc construction (Genzel six: CFG401's, which CFG402 and CFG405 reuse)

- Points: kind "v" rows; drop |offset| < FWHM = 0.6"; R = |offset| x (kpc/"); V = |v| / sin i; eV = max(err, 1) / sin i;
  both sides kept as separate points (CFG401 exactly).
- **Pressure support (the record's Genzel term, Genzel+2017 Table 1 note):** V_c^2 = V^2 + k x 3.36 sigma0^2 (R / R_1/2),
  R_1/2 = Table 1 n = 1 fit. Primary k = 1; brackets k = 0 (none) and k = 2 (double).
- Error per point in log10 V_c^2: sqrt((2 V eV / (V_c^2 ln 10))^2 + 0.05^2) (CFG401). The residual in log10 V_c^2 equals the
  residual in log10 g (same R).
- Baryons: CFG401's shape (stars (1 - f_gas) split into a Freeman disc of R_d = R_1/2 / 1.678 and a Hernquist bulge of
  R_e 1 kpc with Table 1 Mbulge/Mbaryon applied to the stars, as CFG401 does; gas Freeman disc at 2 R_d; f_gas = 1 - M*/M_b),
  NORMALISED to Table 1's prior M_baryon (no free normalisation: the halo scales with M_b, so M_b must be fixed).
  Brackets: MB- / MB+ = prior -1 / +1 sigma (Table 1's stated errors); MB-RC100 = RC100's logMbar for the same disc
  (reported; changes membership); MB-FIT = Genzel's fitted M_baryon (reported).
- zC-488879 (Lelli): CFG278's geometry: kpc/" 8.69; i 71.6 deg; V_rot as digitised (deprojected); M* = 5.2e10 (SED), f_bul
  0.63 as a Hernquist bulge of R_e 0.35" (CFG278 uses de Vaucouleurs; departure declared), disc R_e 0.88"; gas Freeman disc of
  the stellar disc's R_e with M_gas = alpha_CO L'_CO(1-0), L'(1-0) = 8.4e10 / 4.3; primary alpha_CO 4.3, bracket MB- alpha
  0.4, MB+ M* x 2 (0.30 dex, CFG278's declared SED error) at 4.3. Pressure: 3.36 sigma^2 R / R_e,disc with sigma = 15 km/s
  (CFG278's CO knob), k as above. No beam cut (beam-modelled 3DBarolo rings). Errors: mean of the two bar half-widths.
- Lelli bracket for zC 400569: Lelli's 15 points (kpc/" 8.45, CFG278; sigma 37 km/s for Halpha, 15 for CO) replace
  Genzel's points; baryons stay Genzel Table 1's.
- **Reference layout (exactly SRJ3's):** g_ref(R) = g_bar(R) + A G C_R(R) / R^2, C_R = X M_b m(R/r_s) / m(c_ta) (FRZ1's
  halo at the disc's z, M_ta = X M_b h / (1 - FB), Duffy c, r capped at r_ta), X = XTAB[z >= 1 -> z1.0] (55.72 / 55.73). SRJ2's
  `srj2_rc.py` executed read-only from its own path as SRJ3 does. A = 1 is the record's share; A = 0 baryons only.
- **The law:** g = glaw(g_bar, a0) (the record's SRJ chain kernel), a0 constant (JNT2's convention). Reported bracket: a0(z)
  tracking DE (CFG401's de(z)).

## 3. Membership (JNT2's frozen rules, `jnt2_common.py` imported read-only)

Primary: above iff v_L(M_b, z) > v*(z), i.e. log M_b > logMstar(ft, z), with the disc's primary M_b. Bracket MEAS (JNT2's
measured-speed rule): Table 1 vc(R_1/2) (Genzel) or the mean drift-corrected V_c of points within 0.35 R_e of R_e (Lelli
zC-488879) above v*(z). Under MB+/- and MB-RC100 the membership is recomputed with that M_b.

## 4. Statistics

- Per group (ABOVE, BELOW; per footing): chi2(A) = sum over discs and points of ((y - m_A) / e)^2, y = log10 V_c^2 observed,
  m_A from g_ref. A on a grid 0 to 6 step 0.005. Scale s2 = max(1, chi2_min / (N - 1)). **Interval: chi2(A) - chi2_min <= 4 s2
  (95 %)**; 68 % (<= 1 s2) reported. Best A per disc reported.
- **Power:** the 95 % interval excludes at least one of A = 0, 1, 2.
- **Outer shape (primary): S = mean(y, outer half) - mean(y, inner half)** per disc, halves split at the median radius of the
  disc's kept points (a point at the median goes to the inner half). Group difference D = inverse-variance mean over discs of
  (S_data - S_model), sigma_S per disc from the point errors (variance of each half mean), group sigma x sqrt(s2). Shape line
  holds iff |D| <= 2 sigma. Computed for the reference at A = 1, at best A, A = 0 (baryons only) and the law. Reported:
  V_out / V_peak (mean V_c of the two outermost points over the largest V_c) for the data and each model.

## 5. Labels (per footing)

ABOVE v*(z) (the joint predicts the reference layout):
- **NO POWER** if fewer than 3 discs above, or the 95 % interval excludes none of 0, 1, 2.
- **JOINT'S STATEMENT HOLDS ON THE RESOLVED DISCS** (a HIT, not a pass; awaits an independent re-grade) if A = 1 is inside the
  95 % interval and the reference's (A = 1) shape line holds.
- **JOINT'S STATEMENT FAILS ON THE RESOLVED DISCS** if A = 1 is outside the interval (say on which side), or the reference's
  shape line fails while A = 0, the best A (< 1) or the law passes it (say which).
- NO VERDICT (shape fits nothing) if A = 1 is inside, its shape line fails and no lighter model passes it.
BELOW v*(z) (the joint predicts the law), reported beside: NO POWER if fewer than 3 discs, or |chi2_law - chi2_ref(A=1)| < 4 s2
and both shape lines give the same outcome; else LAW HOLDS BELOW if the law's shape line holds and chi2_law - chi2_min(A) <=
4 s2, LAW FAILS BELOW otherwise.
**FRAGILE** if any of k = 0, k = 2, MB-, MB+, MEAS gives a different word. Reported only (no FRAGILE): MB-RC100, MB-FIT,
Lelli curve for zC 400569, DE-tracking a0, beam cut FWHM/2 (CFG400's).

## 6. Twins (separate `*_MUTATE*` outputs; each must bite)

- TW-N (no cold component: C_R = 0): chi2 flat in A, so the ABOVE word must become NO POWER (or differ).
- TW-D (halo doubled, C_R x 2): best A must move by a factor 0.5 +- 0.15 (or the word differ).

## 7. Known answers (must pass, else NO VERDICT)

- KA-G: CFG402's zC 406690 DE penalty 5.94 / 7.18 (canonical / alt) reproduced to 0.01 by executing CFG401's prelude read-only
  (CFG402's method), and my rebuilt Genzel points (k = 1, FWHM cut) equal CFG401's data arrays (max relative difference 1e-12).
- KA-S: SRJ3's K5 g_mod for zC 400569 (RC100 M_b, R_e 4.31 kpc, canonical) 4.4288e-10 m/s^2 within 1e-3 relative.
- KA-B: v*(0) = 668.5 / 807.9 km/s and logMstar(2) = 11.28 / 11.53 (JNT2).
- KA-SI: one disc's g_bar and g_ref at its outermost point recomputed by hand in SI (G 6.674e-11, Msun 1.989e30, kpc 3.0857e19)
  within 1 %.

## 8. Expectation and hand estimate (frozen)

Membership by hand (primary M_b, Table 1): canonical above = zC 406690 (log M_b 11.15 vs 11.12, on the edge), zC 400569 (11.40
vs 11.09), D3a 15504 (11.30 vs 10.99): 3 discs. Alt: zC 400569 (11.40 vs 11.34) and D3a 15504 (11.30 vs 11.23): 2, so alt ABOVE
is NO POWER by count. MEAS gives 5 / 3 above. MB-RC100 gives 1 / 0 (only D3a 15504 canonical).
Halo: M_ta ~ 56 x 2e11 x 0.67 / 0.84 ~ 9e12 Msun at z ~ 2.3, r_s ~ 40-60 kpc; inside 5-10 kpc C_R grows ~ R^2, so at 2 R_1/2
the reference roughly doubles g_bar (rising or flat outer curve), while CFG401/402 found zC 406690 and zC 400569 best fit by
Newtonian baryons (falling). Expect canonical ABOVE: best A ~ 0 to 0.3, A = 1 outside -> FAILS (P 0.5), HOLDS (P 0.15),
NO POWER (P 0.35, if the misfit scale s2 is large); FRAGILE likely (k = 2 lifts the outer points; MB- raises A). Alt ABOVE:
NO POWER (P 0.8). BELOW (COS4 01351, D3a 6397, GS4 43501, zC-488879): NO POWER to separate law from reference most likely
(P 0.5), LAW HOLDS (0.3), LAW FAILS (0.2). Beam smearing depresses inner velocities more than outer ones, so the data's S is
biased toward rising; that bias favours the reference and is not corrected here.

## 9. Files

`dsc1.py` (one script; `DSC1_TWIN=N|D` writes `dsc1_MUTATE_TWN|TWD.json/.out`), `dsc1.json`, `dsc1.out`, `RESULT.md`. Paths
relative to the script; no home paths; warnings suppressed. Owners' code executed read-only from its own path.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
