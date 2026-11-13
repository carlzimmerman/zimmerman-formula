# ALP1 FROZEN CRITERIA: the crossing-speed joint on the ALPAKA I ring curves

TEST lane. Adopts nothing, relabels nothing, registers nothing. Written and committed alone, before any script of this lane
exists and before any number of this lane is computed. Footings never pooled (canonical a0 = 9.3603e-11, alt 1.1312e-10
m/s^2). Cold dark energy is a gravitating field component; no particle. kappa = 1/2 and the share 5.41 are FITTED. No
downloads. Web pages were READ (not downloaded) for three conversion numbers, listed in section 3. One thread, under 2 GB.
Template: DSC1 (criteria 34edc4c9e7, script 370952bd28, RESULT 86497cf4c3), whose construction is reused wherever it applies.
The blind twin lane ALP1R is not opened.

## 0. The question

JNT2's crossing-speed joint: the law's layout holds in systems slower than v*(z) = v*(0) / E(z), v*(0) = 668.53 / 807.93 km/s
(canonical / alt); faster systems keep the cosmic share as cold dust in the reference layout. Its distinctive statement:
**resolved discs ABOVE v*(z) follow the reference layout (baryons + SRJ3's reference cold dark energy halo at the record's
share); discs BELOW follow the law.** DSC1 graded it on 7 Genzel / Lelli discs (fragile hit above, fragile fail below) and
named the ALPAKA I rings as the nearest next data. This lane builds a baryon model for each ALPAKA disc and grades the
statement on them.

## 1. Sample (all on disk; what each file is)

`data_assembly/arxiv_tables/` (ALPAKA I = Rizzo+2023, arXiv:2303.16227, A&A 679, A129):
- `alpaka1_digitised/alpaka1_vrot_digitised.csv`: every ring of the 19 secure discs, digitised from the paper's raster
  figure `vrot.png` (sha256 bc03fa11...b6), panel V (rotation, deprojected by the authors' 3D tilted-ring fit, BBarolo,
  beam-modelled, NOT pressure-corrected: the paper defers asymmetric drift to a later paper) and panel sigma; R in kpc
  (top-axis calibration), value, and the plotted 1-sigma band edges. Validation (`alpaka1_vrot_validation.csv`,
  `checks.txt`): V_max and V_ext within 1.6 % / 1.3 % of the paper's table, kpc/" within 2 %.
- `alpaka1_digitised/alpaka1_outer_summary.csv`: R_ext and the dashed optical R_e where the paper drew one (IDs 1, 6, 8, 9,
  18, 20, 28 only).
- `alpaka1_sample.csv` (z), `alpaka1_properties.csv` (M* STARDUST SED, Chabrier, with error; MS / SB class; L' of the
  observed line in 1e10 K km/s pc^2), `alpaka1_alma_obs.csv` (which line), `alpaka1_kinematics.csv` (sigma_m, the mean
  dispersion, with errors; upper limits for IDs 3, 7, 28), `alpaka1_geometry.csv` (inclinations; reported only).
- `campaign_fresh_gravity/CFG229_class_m_gold/cfg229_inputs_static.csv`: Dunne+2022 per-galaxy optimised multi-tracer H2
  masses (class M) matched by position for IDs 15, 18, 19, 20, 22 (`logMH2`, H2 only; the gravitating gas is 1.36 x).

The 19 discs with rings: IDs 1, 2, 3, 6, 7, 8, 9, 11, 12, 13, 15, 18, 19, 20, 22, 23, 24, 25, 28 (z 0.56 to 3.63; 2 to 5
rings each). **ID 24 (ADF22.5) has no stellar mass on disk and none is read here: it is listed with its gas-only M_b
(a lower bound) and its membership, and is NOT in any graded group.** Graded sample: 18 discs.

## 2. Points and pressure support

- Points: every V-panel ring (no beam cut: the rings are beam-modelled, as DSC1 treated Lelli's 3DBarolo rings). R = R_kpc.
- Error per ring: e_V = mean of |band_hi - V| and |V - band_lo|, floored at 5 km/s; in log10 V_c^2:
  sqrt((2 V e_V / (V_c^2 ln 10))^2 + 0.05^2) (DSC1 / CFG401 form, 0.05 dex floor).
- **Pressure support (Genzel / DSC1 term): V_c^2 = V^2 + k x 3.36 sigma_m^2 (R / R_e)**, sigma_m = the table's mean
  dispersion (IDs 3, 7, 28: the published upper limit used as a value), R_e = the stellar R_e of section 3. Primary k = 1;
  brackets k = 0 (none) and k = 2 (double). These discs are dynamically cold (V/sigma 3 to 21): the term is small except
  where V/sigma <= 6 (IDs 3, 6, 7, 15, 25, 28), where at R = R_e it adds 3.36 / (V/sigma)^2 = 9 % to 37 % to V^2. The per-disc
  size of the term at the outermost ring is printed.

## 3. Baryon model per disc (frozen)

- **Stars:** M* from `alpaka1_properties.csv` in one thin exponential (Freeman) disc, R_d = R_e / 1.678. No bulge (none on
  disk that is not a fit to the same kinematics; the JWST decompositions of IDs 1, 3, 13 in `alpaka_jwst2026_*` fit the
  rotation curve and are not used). **Stellar R_e = the dashed optical R_e where drawn (IDs 1, 6, 8, 9, 18, 20, 28), else
  R_ext / 1.2 (CFG227 / CFG229's rule; median R_ext/R_e of the seven with both is 1.23).** For those 11 discs the size is a
  convention, not a measurement.
- **Gas:** one Freeman disc with R_e,gas = R_ext / 1.2 (the CO / [CI] extent convention), for every disc.
  - Class M (IDs 15, 18, 19, 20, 22): M_gas = 1.36 x 10^logMH2 (Dunne+2022, on disk via CFG229).
  - CO discs (1, 2, 3, 6, 7, 8, 9, 11, 12, 23, 25, 28; and 24 listed only): M_gas = alpha_CO x L'_J / r_J1, with **r_J1 = the
    Bothwell+2013 SMG medians (Table 3, arXiv:1205.1511): r21 0.84, r32 0.52, r54 0.32, r65 0.21** (r43 0.41, r76 0.18 not
    needed) and **alpha_CO = 4.36 for the paper's MS class, 0.8 for SB** (Msun (K km/s pc^2)^-1, helium included; Bolatto /
    Downes & Solomon values as quoted in Carilli & Walter 2013, arXiv:1301.0371, read: "alpha_CO ~ 0.8" starbursts, "~4"
    MW; 4.36 is the record's frozen Galactic value, CFG272). ID 24 (no class): 4.36.
  - [CI](2-1) disc (ID 13): M_gas = alpha_CI x L'_CI(2-1) / R_CI, alpha_CI = 17.0 (Dunne+2022 calibration, on disk in
    `data_assembly/MULTI_TRACER_GAS_2026-09-30.md`; read as including helium), R_CI = L'_CI(2-1) / L'_CI(1-0) = 0.33
    (optically thin LTE at the excitation temperature 29.1 K of Walter+2011 as quoted by Carilli & Walter 2013; computed
    from the [CI] level energies 23.6 / 62.5 K, A10 7.93e-8, A21 2.68e-7 s^-1, nu 492.16 / 809.34 GHz).
- **Gas bracket (frozen, FRAGILE):** GAS- : CO discs alpha_CO 0.8 with r_J1 = 1 (CFG272's floor); class M x 10^-0.3; ID 13
  R_CI = 1 (gas / 3). GAS+ : CO discs alpha_CO 4.36 for every class with the Carilli & Walter CSG ratios where defined (r21
  0.97, r32 0.56) and Bothwell's otherwise; class M x 10^+0.3; ID 13 x 2.
- **Stellar mass bracket (frozen, FRAGILE): M* x 10^-0.3 and x 10^+0.3** (CFG229's declared outer stellar band: SED, SFH,
  IMF and AGN contamination; 7 of the graded discs host AGN or are SB).
- **Size bracket (frozen, FRAGILE):** all R_e (stars and gas) x 1.5 and / 1.5.
- **Reported (not FRAGILE):** STARS (gas set to zero: the stars-only lower bound DSC1 used for membership); CONV-ALL (class-M
  discs converted with the L' rule instead of Dunne's masses).

**PROVISIONAL inputs read from web pages (each read twice, two separate fetches with different questions, values agreed):**

| number | value | source page |
|---|---|---|
| r21, r32, r54, r65 (SMG medians) | 0.84, 0.52, 0.32, 0.21 | Bothwell+2013 Table 3, ar5iv 1205.1511 |
| CSG r21, r32 | 0.97, 0.56 | Carilli & Walter 2013 Table 2, ar5iv 1301.0371 |
| alpha_CO starburst / MW | ~0.8 / ~4 | Carilli & Walter 2013 Sect. 4, ar5iv 1301.0371 |
| [CI] T_ex at high z | 29.1 +- 6.3 K | Carilli & Walter 2013 (quoting Walter+2011), ar5iv 1301.0371 |

The ALPAKA paper's own page was read: it gives no gas conversion, no gas mass, no R_e numbers and no pressure correction.
Every M_gas of a CO or [CI] disc is therefore PROVISIONAL (a conversion chosen here); the class-M masses are on disk but
inherit Dunne's normalisation; every R_e from the R_ext / 1.2 rule is a convention.

## 4. Reference layout, the law, membership

- **Reference layout (SRJ3's, as DSC1):** g_ref(R) = g_bar(R) + A G C_R(R) / R^2, C_R = X M_b m(R/r_s) / m(c_ta), FRZ1's
  halo at the disc's z with M_ta = X M_b h / (1 - FB), r capped at r_ta, X = XTAB[z >= 1 -> z1.0, else z0.0]; SRJ2's
  `srj2_rc.py` executed read-only from its own path. A = 1 the record's share; A = 0 baryons only.
- **The law:** g = glaw(g_bar, a0), a0 constant.
- **Membership (JNT2's frozen primary rule, `jnt2_common.py` read-only):** above iff log M_b > logMstar(ft, z), M_b = M* +
  M_gas of the variant (recomputed under every bracket). **Bracket MEAS (JNT2's measured-speed rule):** above iff the
  measured V_c (k = 1) at the stellar R_e, linearly interpolated between rings (clamped to the ring range), exceeds v*(z).

## 5. Statistics

- **Per group (ABOVE, BELOW; per footing):** y = log10 V_c^2 (SI), model m = log10(g R). chi2(A) summed over discs and rings,
  A on 0 to 6 step 0.005; s2 = max(1, chi2_min / (N - 1)); 95 % interval chi2 - chi2_min <= 4 s2, 68 % <= 1 s2. Best A per
  disc reported. chi2 of the law and of A = 0, 1 reported. Mean residual (data - model) per group for A = 0 and the law.
- **Power:** the 95 % interval excludes at least one of A = 0, 1, 2; fewer than 3 discs is NO POWER.
- **Outer shape S (DSC1's):** mean y over the outer half minus the inner half (split at the median ring radius; a ring at
  the median goes inner); group D = inverse-variance mean of S_data - S_model, sigma x sqrt(s2); the shape line holds iff
  |D| <= 2 sigma. For the reference at A = 1, best A, A = 0, and the law. V_out / V_peak reported.
- **Reach:** R_max / R_e per disc (for the 11 convention discs this is 1.2 by construction and says nothing).
- **SHAPE-ONLY test (frozen):** each disc gets a free baryon scale beta (M* and M_gas together, the halo recomputed with
  beta M_b), log10 beta flat on [-1, +1] step 0.02 (prior: one dex either way, so the amplitude carries no information);
  chi2_shape(A) = sum over discs of the minimum over beta; A grid 0 to 6 step 0.05; same s2, interval and power rule. **The
  shape speaks iff that 95 % interval excludes at least one of 0, 1, 2.** Membership stays at the primary M_b. Run for the
  primary variant and each FRAGILE bracket (reported).

## 6. Labels (per footing)

ABOVE v*(z):
- **NO POWER** if fewer than 3 discs above, or the 95 % interval excludes none of 0, 1, 2.
- **JOINT'S STATEMENT HOLDS ON THE ALPAKA DISCS** (a HIT, not a pass; awaits the blind twin) if A = 1 is inside the 95 %
  interval and the reference's (A = 1) shape line holds.
- **JOINT'S STATEMENT FAILS ON THE ALPAKA DISCS** if A = 1 is outside the interval (say which side), or the A = 1 shape line
  fails while A = 0, best A < 1 or the law passes it. The parenthesis says what fits instead: "a lighter halo" if 0 < best A < 1
  and the best-A shape line holds; "baryons alone" if A = 0 is
  inside the interval; "the law" if chi2_law - chi2_min <= 4 s2; **"nothing: the baryon model exceeds the dynamics" if the
  best A is 0 and the A = 0 group mean residual (data - model) is below -2 x its error (sigma_mean = sqrt(s2 / sum 1/e^2)).**
- NO VERDICT (shape fits nothing) if A = 1 is inside, its shape fails and no lighter model passes.
BELOW v*(z), beside (DSC1's rule): NO POWER if fewer than 3 discs, or |chi2_law - chi2_ref(A=1)| < 4 s2 and both shape lines
give the same outcome; else LAW HOLDS BELOW if the law's shape line holds and chi2_law - chi2_min <= 4 s2; LAW FAILS BELOW
otherwise.
**FRAGILE** if any of k0, k2, GAS-, GAS+, MS-, MS+, RE x 1.5, RE / 1.5, MEAS gives a different word (first word block, before
the parenthesis). Reported only: STARS, CONV-ALL.

## 7. Twins (separate `*_MUTATE*` outputs; each must bite)

- TW-N (no cold component, C_R = 0): chi2 flat in A, so an ABOVE word with power must become NO POWER (or the interval must
  become the whole grid).
- TW-D (halo doubled): best A must move by 0.5 +- 0.15 (or the word differ); if best A is 0 in the main run, the bite is
  read from the upper edge of the 95 % interval, which must halve within 0.15 relative.

## 8. Known answers (must pass, else NO VERDICT)

- KA-B: v*(0) = 668.53 / 807.93 km/s (0.01), logMstar(2) = 11.28 / 11.53.
- KA-D (a DSC1 number with this lane's code): the reference cold acceleration of D3a 15504 at R = 12.948 kpc (Genzel Table 1
  M_b from CFG401's prelude, executed read-only) equals DSC1's `gcold_script` 1.16520e-10 to 1e-3, and SRJ3's K5 g_mod for
  zC 400569 4.4290e-10 (DSC1's KA-S) to 1e-3.
- KA-SI: one ALPAKA disc's outermost ring recomputed by hand in SI (G 6.674e-11, Msun 1.989e30, kpc 3.0857e19; Freeman
  formula and NFW written out separately): g_bar, g_cold and g_obs = V_c^2 / R within 1 %.
- KA-L: the [CI] ratio R_CI = 0.33 recomputed from the stated constants to 0.01.

## 9. Expectation and hand estimate (frozen, before any number)

- **Membership by hand** (logMstar = 13.21 - 4 log10 E(z) canonical, +0.25 alt): logMstar ~ 12.66 (z 0.56), 11.76 (1.45),
  11.20 (2.10), 10.90 (2.5), 10.51 (3.09), 10.21 (3.63) canonical. The z < 1.7 discs (1, 2, 3, 6, 7, 8, 9, 11, 12) are below
  on both footings. At z >= 2.1, M* alone already puts 15, 18, 20, 22, 23, 25, 28 above canonical (DSC1's inventory 7 / 5);
  with gas (ID 13's [CI] gas is ~4e11 under the frozen conversion, ID 19's class-M gas 1.6e11) expect 9 above canonical
  (13, 15, 18, 19, 20, 22, 23, 25, 28) and 7 to 9 alt; below: the 9 low-z discs.
- **Amplitude:** CFG229 found g_obs below g_bar at R_ext for ALPAKA 15, 18, 19, 20, 22 with class-M gas (D = 0.20 to 0.46;
  baryons over the spherical dynamical mass 3 to 6). Expect the same here: baryons alone already overshoot most above
  discs, so best A = 0 at the floor, A = 1 above the interval, and the A = 0 mean residual well below zero. **Expected ABOVE
  word: JOINT'S STATEMENT FAILS (A = 1 above the interval; nothing fits: the baryon model exceeds the dynamics), P 0.6;
  NO POWER P 0.25 (if s2 is huge); HOLDS P 0.15.** FRAGILE likely through GAS- / MS- (lighter baryons let a halo back in) and
  RE x 1.5.
- **BELOW** (z 0.56 to 1.63): CO(2-1) MS discs with alpha 4.36 give gas 1e10 to 1e11; expect baryons near or above the
  dynamics for several; law and A = 1 both near Newton at these accelerations (g_bar / a0 ~ 5 to 30). Expect NO POWER
  (P 0.4), LAW FAILS BELOW (P 0.4, overshoot), LAW HOLDS (P 0.2).
- **Shape-only:** 2 to 5 rings per disc, reach 0.8 to 3.5 R_e (1.2 by construction for 11 discs), the halo nearly
  proportional to R^2 x const inside 6 kpc: **expect the shape not to speak (interval spans 0 to 2) on both sides, P 0.8.**
- Hand estimate for ID 18 at R_ext 4.98 kpc: stars 1.2e11 in R_d 0.83 kpc and gas 1.36 x 10^11.68 = 6.6e11 in R_d 2.47 kpc:
  enclosed-mass shortcut g_bar ~ G (1.2e11 + 0.55 x 6.6e11) Msun / R^2 ~ 6.674e-11 x 4.8e11 x 1.989e30 / (1.537e20)^2 ~
  2.7e-9 m/s^2, against g_obs = (466 km/s)^2 / 4.98 kpc ~ 1.4e-9: baryons alone ~ 2x the dynamics; the reference halo at
  A = 1 adds of order 1e-10 to 3e-10 inside 5 kpc. So A will not be weighed by ID 18.

## 10. Files

`alp1.py` (one script; `ALP1_TWIN=N|D` writes `alp1_MUTATE_TWN|TWD.json/.out`), `alp1.json`, `alp1.out`, `RESULT.md`. Paths
relative to the script; no home paths; warnings suppressed. Owners' code executed read-only from its own path.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
