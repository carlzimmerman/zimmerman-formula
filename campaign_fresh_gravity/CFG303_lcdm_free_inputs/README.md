# CFG303: every a₀ input tagged, and the ΛCDM-halo-derived ones replaced with framework-native inputs

**Criteria.** `FROZEN_CRITERIA.md` was committed as **52976ec22** before any re-run. Addenda 1–3 were each written before the replacements they declare were evaluated; what had been seen at each point is stated in them.

**Owner direction (2026-10-02):** "we need to use all the data using our framework not ACDM assumptions!" and "we must use empirical evidence raw and unfiltered".

κ = ½ is FITTED. The cold mass is still required, and no dark-matter particle is added. No sentence here says the data favour a law.

## Bottom line
- **Inventory.** 164 input quantities: **52 RAW, 45 MODEL-OTHER, 35 LCDM-MODEL, 8 COMPARATOR**, and 24 lanes with no data input (tag NONE).
  - 19 of the 35 LCDM-MODEL rows were re-derived.
  - 5 cannot be replaced from what is on disk.
  - 11 were not re-run, each with its reason stated (forecasts, referees, a frozen preregistration, rows that are reported only).
- **What carried the LCDM-MODEL inputs.** The chart's RC100, CRISTAL and MUSE-DARK points all took their baryon side from halo fits. That includes the routes labelled "independent" and "SED": each still multiplied by the fit's (1 − f_DM) and divided by the fit's M_fit. The KURVS decision cell used a pressure correction calibrated on ΛCDM simulations.
- **Replaced by native baryons.** SED M★ plus measured or scaling gas, in a declared thin-disc geometry, through each lane's own committed estimator:
  - RC100's implied a₀ drops (Q2–Q3), or has no root at all (Q4).
  - The within-sample label changes from W-flat to W-mixed.
  - The rival's 4.6σ "weakest exclusion" in the MNRAS inversion becomes 2.2σ.
  - CRISTAL loses its one point that excluded flat a₀, and its H(z) pulls shrink to under 1σ.
  - MUSE-DARK's SED-route levels drop. No route shows a rise.
  - The KURVS "lean rival" holds only under the Kretschmer correction (and under P3). With the measured markers and the analytic P2, both laws under-predict ("neither").
- **Unchanged.** X-COP, the Amvrosiadis floors, the NOEMA3D bin and CFG90's pooled z ≥ 1.5 offsets do not move beyond their quoted errors.
- **Every native result is calibration-limited.** The shifts come from 0.05–0.10 dex of baryon mass and geometry, acting through the known lever of −2.5 to −4.8 dex per dex. That is the record's existing statement (CFG223, PAPER38) made concrete. None of it separates flat a₀ from a₀ ∝ H(z).

## The re-derived headlines (old → LCDM-free)
Primary native inputs:
- **RC100 sample B:** all 100 galaxies, with M★,SED from Table 3 column 6 (transcribed) plus CFG217's μ_t18 gas. g_bar uses CFG216's thin disc at R_e. g_obs is the authors' V_c(R_e) (MODEL-OTHER, `halo_in_fit = yes`).
- **RC100 sample A:** the 41 RC41 galaxies, with Price+21 SED M★ plus gas. **G2** is A with a point-mass bulge.
- **CRISTAL:** M★,SED/(1 − f_molgas) in the same thin disc.

The rule for "changed" is frozen §6:
- (a) a class or verdict word changes;
- (b) the central value moves outside the committed 68% interval;
- (c) a sign flips.

| lane / statement | committed (LCDM-MODEL input) | LCDM-free | recorded statement |
|---|---|---|---|
| **CFG223 chart, RC100 Q1** (z 0.81) | s* 1.84, 68% [1.44, 2.05]; pulls flat +2.54, H(z) +0.58 | B 1.48 [95%: 0.88, 2.99]; A 1.27; G2 1.11; pulls flat +0.50, H(z) −0.09 | unchanged by (b) (inside the committed 68%); the flat pull falls from +2.5 to +0.5 |
| **RC100 Q2** (z 1.36) | 2.10 [1.48, 2.79] | B 1.01 [no root, 3.51]; A and G2 no root | **changed** (b) |
| **RC100 Q3** (z 2.01) | 1.57 [1.25, 2.04]; H(z) pull −2.62 | B 0.84 [no root, 2.24]; H(z) −0.44 | **changed** (b) |
| **RC100 Q4** (z 2.26) | 0.99 [0.80, 1.14]; flat −0.03, H(z) −5.66 | **no root** (16 of 27 discs have D ≤ 1); flat −3.51, H(z) −4.13 | **changed** (a): root → no root. The native baryons meet or exceed the dynamics |
| RC100 pooled (100) | 1.45 [1.09, 2.06] (same estimator, committed route) | B 0.82 [no root, 1.30]; 41 of 100 discs have D ≤ 1 | — |
| **CFG223 caption counts** (8 figure points, 95% / ±0.15 / ±0.30) | flat 7/8/8 (the exception was CRISTAL R_e fit); H(z) 4/5/7 | flat 7/7/8 (the exception is now RC100 Q4, no root); H(z) 4/4/5 | flat count unchanged; the exception moves |
| **CFG216 within-sample slopes** (ν_mono, canonical) | flat −0.030 [−0.073, +0.002], rival −0.091 [−0.129, −0.055]; **W-flat** | B: flat −0.139 [−0.219, −0.054] (z vs flat-true −3.4), rival −0.185 (z vs rival-true −5.2): **W-mixed**. A: W-none (flat −0.041, rival −0.104). The committed route on A is also W-none | **changed** (a) for the full sample: δ_flat drifts negative with z once the Tacconi-scaled gas is in the baryons (CFG217's "more gas" direction). On the RC41 overlap the class does not change |
| **MNRAS v3.1 S5** (closed-form RC100 inversion; paper l. 516–535, 635) | N 99; slope −0.111 ± 0.063; median â₀ 1.39e-10; weakest exclusion of H(z) 4.6σ | B: N **59** (41 galaxies leave the paper's f window because their native D ≤ 1.02); slope −0.122 ± 0.098; median â₀ 2.11e-10 (biased high: the window drops the Newtonian-floor discs); weakest H(z) 2.2σ. A: N 22, slope −0.12 ± 0.13, 0.9σ | the paper already says the result "is not a measurement". Its quoted N, median and slope all move. **The manuscript was not edited; any change is the owner's call** |
| **CFG90 pooled z ≥ 1.5** (STANDING §4; CFG289) | committed flat +0.137 / rival −0.034 (N 15); corrected file flat +0.035 / rival −0.131 (N 13) | native flat +0.040 (+0.28σ), rival −0.125 (−0.90σ), N 12 | unchanged against the corrected-file reading |
| **CFG223 CRISTAL R_e** (z 5.2) | fit route 1.87 [95%: 1.16, 5.65], the only point excluding flat; pulls proxy −2.49, H(z) −3.55. "Independent" route 2.91 [0.001, 18.9] | six discs: 2.01 [0.001, 14.9]; 9-disc set: 0.67 [0.001, 14.0]; pulls flat +0.26, proxy −0.39, H(z) −0.55 | **changed** (a): no CRISTAL point excludes flat any more, and H(z)/proxy are no longer at −2.5 to −3.6. No information either way (the bars span the plot) |
| **CFG223 CRISTAL R_out** | fit route 1.21 [0.26, 3.97] at the table R_out (a model curve beyond the last marker: LCDM-MODEL); H(z) pull −3.39 | at the outermost data marker: 1.95 [0.001, 8.78], H(z) −0.78 (just outside the 95% interval); table-R_out variant 1.90 | **changed** (b) |
| **CFG213 Z5** "the rival is disfavoured on the fit route only" | fit route: rival robustly DISFAVOURED-under, flat not robust | native (9 discs): flat robustly CONSISTENT; rival NOT robust (DISFAVOURED-under only at α = 1.68 with ν_mono) | consistent with the recorded wording (fit route only); natively the rival is not robustly disfavoured |
| **CFG213 Z1.4 NOEMA3D** | both CONSISTENT | both CONSISTENT (flat −0.007, rival −0.062) | unchanged |
| **CFG262 MUSE-DARK** (bD; z 0.52 / 0.88 / 1.20) | route (i) DC14: 1.22 / 3.05 / 4.53 (rise +0.570 ± 0.094). Route (iii) "SED": 1.58 / 3.32 / 1.71. Route (ii): 0.46 / 1.02 / 0.36. Routes (ii)/(iii) still carry f_DM and M_fit | native (iii), no HI: **1.21 / 2.11 / 0.66**, z3 − z1 = −0.26 ± 0.28 (H(z) expects +0.18). Native (ii): 0.22 / 0.27 / no root. HI at the prior ceiling lowers both | levels **changed** (b); "route (i)'s rise travels with the fitted masses" and "FLAT vs H(z) NOT POSSIBLE" stand (no rise on native baryons; flat inside 95% in 4/6 rows, H(z) in 2/6) |
| **KURVS decision cell** (μ 0.67, measured markers; CFG189) | P4 Kretschmer (LCDM-MODEL): flat +0.125 (+2.4σ), rival −0.021 (−0.4σ), **lean rival** | **P2 (primary): flat +0.375 (+6.8σ), rival +0.228 (+4.3σ): neither.** P3: lean rival (+3.8 / +1.1σ). P1: neither. P0: lean flat (−1.9 / −4.5σ). Over the 6 marker sets × 4 LCDM-free prescriptions: lean flat 4, lean rival 7, neither 13. P2 break-even gas: flat μ 6.2, rival 3.6 | **changed** (a): the recorded "lean rival" is a property of the VELA-calibrated correction (and of P3). The standing wording ("not a detection either way; turns on pressure support and gas") holds |
| **CFG274 Amvrosiadis** (chart floors) | α_CO 0.92 (from an assumed f_dm = 0.25): 7 of 8 no root; 075.1 s* 6.9 | α 0.8: 7 of 8 (075.1 s* 8.5); α 4.36: 8 of 8 no root | unchanged ("7 of 8 no root, near-Newtonian"; 8/8 at the Galactic conversion) |
| **X-COP identity** (STANDING §1) | R500 from the NFW header: identity/measured 0.946 ± 0.080; η 1.82 (canonical, ν_mono) | R500,FORW (median −0.005 dex): 0.947 ± 0.087; η 1.79 | unchanged |

## Where no framework-native replacement exists on disk
Any fetch below would need the owner's yes, given in the right chat. Nothing was fetched.
- **X-ray ellipticals (§3, B +0.280 dex).** g_obs is Humphrey+06's best-fit NFW+stars model. The native replacement needs the deprojected T(r) and n_e(r) of all seven galaxies. Only NGC 4649's n_e(r) and a few 10-kpc values are on disk.
- **The derived rule's collapse masses** (SPARC +0.0009, the SLUGGS rule, the satellites' −2.67σ / −3.47σ, CFG286, CFG293). These are Mandelbaum halo-model masses or Moster+13 SHMR masses. The framework supplies no collapse mass, which is Gap 2's open target. The law-only rows do not use them.
- **MUSE-DARK II's bTFR M_bar** (CFG190's II = 0.00 ± 0.06). Its HI comes from NeutralUniverseMachine, which is built on ΛCDM merger trees. Replacing it needs the per-galaxy M★ and H₂ columns; only log M_Bar is on disk.
- **GN20's 2 R_e rows** (the NFW model's enclosed mass, extrapolated). Replacing them needs Übler+24's measured outer points or the cubes.
- **Velocities from halo-containing fits, inside the data** (RC100 V_c, CRISTAL V_rot/σ₀/R_e, NOEMA3D V_c, MUSE-DARK's DC14 slit curve, GN20 at R_e). These were kept as MODEL-OTHER, and their halo dependence is disclosed.
  - No measured RC100 or MUSE-DARK curve is on disk. The MUSE-DARK maps exist only as PNGs.
  - CRISTAL's observed markers (`cristal_vector/cristal_points.csv`) and NOEMA3D's are on disk, but they are beam-smeared and have never been scored. A frozen lane could use them.
- **Gaia DR4's g_ext** (a McMillan-type MW model with an NFW halo). It enters only the bare-law floor. The preregistration is frozen, and already carries the alternative V_c²/R₀.

## Controls and what failed
| script | checks | notes |
|---|---|---|
| `cfg303_rc100_cristal_LCDMFREE.py` | **15/16** | **FAIL kept: the S5 identity control** (N 100 against 99). `cfg303_posthoc_s5_identity.py` (post hoc, labelled, 1/1) shows the cause: rebuilding f = 1 − (1 − f_DM) in floating point moves the one galaxy at exactly f_DM = 0.02 (U4 22199) inside the paper's open window. Rounding restores the committed S5 exactly. That single edge galaxy moves the S5 statistics by up to 24% (relative). All other identity, swap-back and MUTATE controls pass, including T1/T2 (the transcription) |
| `cfg303_kurvs_LCDMFREE.py` | 5/5 | The K21 path reproduces CFG189 exactly, and the P2 mapping reproduces CFG141's committed P2 cell exactly (difference 0). Reported: the P3 mapping differs from CFG141's committed P3 by 0.02 dex, because CFG189's error propagation reweights the pool (the CFG189 framework is used throughout, as declared). Variant BS emits CFG184's own RuntimeWarnings (matmul) |
| `cfg303_musedark_LCDMFREE.py` | 3/3 | All 18 committed rows reproduced to 0 |
| `cfg303_amvrosiadis_LCDMFREE.py` | 3/3 | |
| `cfg303_xcop_LCDMFREE.py` | 3/3 | The MUTATE run skips the audit's pressure diagnostic, which feeds no row (declared in the script) |
| `cfg303_cfg90_noema_LCDMFREE.py` | 3/3 | cfg90 runs on a symlink overlay; its original-file run now reproduces the committed pooled numbers |
| `build_inventory.py` | 5/5 | |

## Disclosures
- **The RC100 Table 3 columns 5–8 were transcribed by one reader** from the rendered raster images of the local PDF. They pass three checks:
  - **T1:** column 7 equals the corrected CSV in all 100 rows, with names and z;
  - **T2:** the 7 bulge cells equal the committed CSV's mistaken values;
  - **T3:** column 6 against Price+21's SED M★ gives median 0.000 dex, 41/41 within 0.09 dex.
- **Sample B's gas** uses CFG217's committed μ_t18, which has no δMS term. RC100's own prior includes δMS (median +0.27 dex). With it, the median gas would be about 0.06 dex higher in baryon mass, moving the native s* further down.
- **The native geometry is CFG216's thin disc.** The fits' own baryon geometry (a diagnostic only, built from f_DM) is 0.95× that disc at the median, so geometry alone accounts for about +0.02 dex of the native g_bar. The native M_bar is +0.07 dex (B) and +0.10 dex (A) above the joint-fit posteriors.
- **CRISTAL's 9-disc set** includes three dust-gas upper limits used as values, as CFG213's route did. The six-disc set excludes them.
- **The MUSE-DARK primary has no HI**, so its baryons are a lower limit by the HI. The prior-ceiling and fitted-Σ_HI variants are printed.
- **The S5 inversion's window removes galaxies with D ≤ 1.02**, so its native median â₀ is not a level estimate.
- **Not re-run, with reasons in INVENTORY.csv:**
  - CFG218 (forecast ladder) and CFG219/221 (forecasts);
  - CFG215 (non-diagnostic by construction);
  - CFG222's proxy-fit statement and CFG254 (a theory contact test);
  - CFG269's pool (its CRISTAL inputs are re-derived here);
  - the KROSS ladders (CFG161/165/167 already hold P0–P3);
  - the referees;
  - CFG97 A3 and CFG32 R1 (reported-only rows whose headlines already use native masses).
- **Runs.** Every run was made in a scratch mirror from `git archive` of 52976ec22. The MUSE-DARK run needs the DC14 run files beside the repository, as CFG262 does; the mirror reached them through a symlink. The SPARC and KMOS3D symlinked files did not extract into the mirror, and none of these runs needs them.
- **Observation, not edited:** `CFG90_a0z_rederivation/cfg90.py` line 13 hard-codes an absolute home path. It is another lane's committed file; flagged for the owner.

## Files
- **Frozen criteria:** `FROZEN_CRITERIA.md` (committed), `FROZEN_CRITERIA_ADDENDUM_1.md`, `_2.md`, `_3.md`.
- **Inventory:** `INVENTORY.csv` (164 rows; columns: lane, dataset, quantity, source, how the authors derived it, tag, halo_in_fit, what it feeds, native replacement on disk, evidence file, CFG303 status), built by `build_inventory.py` (`build_inventory.out`).
- **New input:** `rc100_table3_cols5to8_transcribed.csv`.
- **Re-runs:** for each, a `.py`, an `.out` and a `_results.json`, all suffixed `_LCDMFREE`: `cfg303_rc100_cristal`, `cfg303_kurvs`, `cfg303_musedark`, `cfg303_amvrosiadis`, `cfg303_xcop`, `cfg303_cfg90_noema`. Per-galaxy tables: `cfg303_rc100_pergalaxy_LCDMFREE.csv`, `cfg303_cristal_pergalaxy_LCDMFREE.csv`.
- **Post hoc:** `cfg303_posthoc_s5_identity.py` / `.out` / `_results.json`.

Run each from the repository root, e.g. `python3 campaign_fresh_gravity/CFG303_lcdm_free_inputs/cfg303_rc100_cristal_LCDMFREE.py`. Run times:
- about 5 min: rc100_cristal;
- about 4 min: musedark;
- seconds: the others.
