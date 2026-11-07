# SE2: the hot/cold step as systematics, one joint budget per class. IN PART: X-COP, groups and Coma UDGs stay NOT EXPLAINED

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle. Footings graded separately, never pooled.

- Criteria: FROZEN_CRITERIA.md (f49a99a04c), committed alone before any script or number.
- Script: se2.py. It execs GB1's loaders and gates read-only, and execs ST1's script read-only for KA1 (its writes go to
  a temp dir outside the repo). One thread, about 5 s, peak RSS about 0.76 GB. A rerun gives a byte-identical se2.json.
- Outputs: se2.json / se2.out (main) and se2_MUTATE.json / se2_MUTATE.out (M1). Run main first: MUTATE reads se2.json.

**Lane label: STEP = SYSTEMATICS IN PART. Remaining: X-COP, groups, Coma UDGs.**
- The joint budget explains the X-ray ellipticals, the KiDS early/late split and the bright M31 dSphs on both footings.
- MW classical dSphs are NOT A TEST: with N = 8 the class never established a step.
- **Coma UDGs stay NOT EXPLAINED**, on both footings, at 3.7 / 3.5 sd with every knob drawn jointly.
- **CMB row: SEPARATE.** No key in the record passes the hot classes at all, so this is the frozen rule's reading. It does
  not prove that two causes exist.

## Admissibility (frozen before any data)

- **A1 tidal:** tau = R_e / r_J < 0.375, with r_J built from the observed dynamical mass M_W = 4 sigma^2 R_e / G (QX24 /
  ST1 estimator, Z2 C1 line).
- **A2 dynamical time:** t_cross = r_1/2 / sigma <= 0.1 t_orb.
- **What was removed:**
  - bright M31: 21 of 25 admissible. And I, XVII, XIX and XXV fail A1; And XIX also fails A2. These are the same four ST1
    cut.
  - MW ultra-faint: 30 of 31 (Bootes III fails both).
  - MW classical 8/8, M31 others 5/5 and Coma UDGs 9/9 all pass.
  - LG field 13/13 pass: no MW/M31 host term applies, so they pass by definition.
- **Coma UDGs:** tau 0.17-0.33 at S1's dmean, and t_cross / t_orb <= 0.046.
- **Pericentre reading** (tau x 2.08, reported only): bright M31 15/25, MW classical 7/8, Coma UDGs **1/9**.

## Priors (one rule: a stated +- range is 1 sigma; a bracket is uniform; a one-sided sign is 0, disclosed)

| Class | Knob | Prior | Source |
|---|---|---|---|
| ellipticals, KiDS, X-COP, groups | IMF | b = f_Posacki^lambda, lambda ~ N(1, 1) truncated >= 0 (Kroupa at -1 sigma) | QX26 (Posacki+2015), GB1 b_imf floor |
| ellipticals | sigma_0 scale | N(1, 0.1) | QX26 x0.9 / x1.1 |
| KiDS | early sigma_e | U[130, 210] km/s; late 60 (Kroupa floor) | QX26 |
| X-COP / groups | sigma_star | U[250, 350] / U[200, 300] km/s | GB1 fill brackets |
| groups | stellar share f* | U[0, 1] | GB1 f* 0 / 1 |
| dSphs | Upsilon_V | log10 ~ N(log10 2, 0.30), common to the class | E3 ledger / X1 (Upsilon 2, bracket 1-4) |
| dSphs | gas | 1.33 M_HI (LVD), upper limits U[0, UL]; share inside r_1/2 U[0, 0.5] | QX23 convention; the share is a frozen assumption |
| dSphs | distance | per system N(0, DM error / 5) dex | LVD distance_modulus errors (all present) |
| dSphs | anisotropy / estimator | common, a_c = median \|E-V - E-W\|: bright M31 0.116, MW classical 0.107, LG field 0.041 dex | X1 / S1 estimator rows |
| dSphs | membership / dataset | common, m_c in log sigma: bright M31 0.045 (Collins+2013, 9 matched), MW classical 0.014 (McConnachie 2012, 7), LG field 0.244 (McConnachie, 4) | alternative catalogues on disk |
| Coma UDGs (ln, 1 sigma, canonical / alt) | M*, sigma, distance | s_M 0.461, s_A 0.280, s_D 0.073 / 0.075 | S1 / CFG948 |
| Coma UDGs | anisotropy, sample, 3-D position | s_aniso 0.265, s_mem 0.039 / 0.041, s_pos 0.217 / 0.241 | S1 rows E-V, all 11, dproj |
| clusters, groups | hydrostatic bias | 0; it would only raise the step | QX21 T3 |
| ellipticals, UDGs | gas | NOT IN BUDGET; it would lower the step | QX18 neglect; no Coma HI on disk |
| ellipticals, KiDS | distance, photo-z, colour membership | NOT IN BUDGET (nothing on disk) | |

## Posterior step per class x footing (dex; median, 68 % and 95 % intervals; GB1 L0 data, plain law)

| Class | Footing | raw stat-only 95 % | joint median | 68 % | 95 % | z | P(s <= 0) | Label |
|---|---|---|---|---|---|---|---|---|
| X-ray ellipticals | canonical | [+0.076, +0.350] | +0.067 | [-0.064, +0.179] | [-0.201, +0.271] | 0.55 | 0.30 | EXPLAINED |
| | alt | [+0.057, +0.327] | +0.050 | [-0.078, +0.159] | [-0.218, +0.252] | 0.42 | 0.34 | EXPLAINED |
| KiDS early/late | canonical | [+0.032, +0.282] | +0.085 | [-0.000, +0.162] | [-0.087, +0.233] | 1.03 | 0.16 | EXPLAINED |
| | alt | [+0.033, +0.286] | +0.084 | [+0.001, +0.163] | [-0.085, +0.235] | 1.03 | 0.16 | EXPLAINED |
| X-COP | canonical | [+0.442, +0.499] | **+0.440** | [+0.412, +0.463] | [+0.372, +0.484] | 15.8 | 0 | **NOT EXPLAINED** |
| | alt | [+0.408, +0.467] | **+0.408** | [+0.380, +0.431] | [+0.341, +0.451] | 14.8 | 0 | **NOT EXPLAINED** |
| groups | canonical | [+0.353, +0.388] (f* 0) | **+0.232** | [+0.156, +0.318] | [+0.078, +0.362] | 3.04 | 0.0025 | **NOT EXPLAINED** |
| | alt | [+0.317, +0.349] (f* 0) | **+0.194** | [+0.119, +0.279] | [+0.041, +0.324] | 2.55 | 0.0087 | **NOT EXPLAINED** |
| bright M31 dSphs (21 admissible) | canonical | [+0.101, +0.445] | +0.228 | [+0.006, +0.455] | [-0.213, +0.685] | 1.00 | 0.15 | EXPLAINED |
| | alt | [+0.089, +0.433] | +0.219 | [-0.006, +0.447] | [-0.225, +0.676] | 0.96 | 0.17 | EXPLAINED |
| MW classical dSphs (8) | canonical | [-0.049, +0.544] | +0.257 | [+0.021, +0.498] | [-0.204, +0.742] | 1.08 | 0.14 | NOT A TEST (no power) |
| | alt | [-0.057, +0.532] | +0.249 | [+0.016, +0.486] | [-0.218, +0.717] | 1.05 | 0.14 | NOT A TEST (no power) |
| Coma UDGs (9 admissible) | canonical | [+0.901, +1.343] | **+1.120** | [+0.823, +1.421] | [+0.541, +1.718] | 3.72 | 0.0001 | **NOT EXPLAINED** |
| | alt | [+0.854, +1.301] | **+1.075** | [+0.774, +1.372] | [+0.472, +1.673] | 3.53 | 0.0003 | **NOT EXPLAINED** |
| LG field dwarfs (control) | canonical / alt | [-0.027, +0.164] / [-0.035, +0.153] | -0.024 / -0.033 | | [-1.03, +0.98] / [-1.05, +0.98] | | | NOT A TEST (no step) |

Reported only, as in GB1: MW ultra-faint (30 admissible) +0.583 / +0.572, 95 % [-0.022, +1.194] / [-0.031, +1.176],
reads EXPLAINED. M31 others (5) reads NOT A TEST (no power).

**Class labels (both footings agree in every row):**
- EXPLAINED: ellipticals, KiDS, bright M31.
- NOT EXPLAINED: X-COP, groups, Coma UDGs.
- NOT A TEST: MW classical.

## Verifying each label as hard as the other

**Coma UDGs, NOT EXPLAINED.**
- Leaving out any one of the six knobs keeps the 95 % interval clear of 0. The tightest case is canonical without s_D,
  at [+0.54, +1.72].
- Reading every edge as 2 sigma (half widths, post-freeze) gives [+0.77, +1.48] / [+0.72, +1.43].
- Reading every edge as 1/2 sigma (widths x2, frozen, reported) gives [+0.007, +2.24] on canonical, which still clears 0
  by a hair. On alt it gives [-0.06, +2.21], which contains 0. **At doubled widths the alt footing would read EXPLAINED.**
- The label rests on the graded admissibility using today's dmean. On the pericentre reading, only 1 of 9 UDGs is
  admissible, so the class would be NOT A TEST.

**X-COP, NOT EXPLAINED.**
- z is 15. Even with doubled widths the interval is [+0.23, +0.48] / [+0.20, +0.45].
- The IMF alone moves the median by only 0.03 dex.

**Groups, NOT EXPLAINED.**
- The label rests on f* ~ U[0, 1].
- With f* = 1 and the IMF prior, the median is +0.144 [+0.011, +0.209] canonical (still excludes 0) and +0.106
  [-0.027, +0.170] alt (contains 0).
- With doubled widths the interval is [-0.08, +0.36] / [-0.12, +0.32], which contains 0 on both footings.
- **Groups are the most fragile NOT EXPLAINED.**

**Bright M31, EXPLAINED.** This reverses ST1's NOT EXPLAINED. ST1 graded only the tidal cut for dSphs. SE2 adds
Upsilon_V, anisotropy, membership, gas and distance.
- Any one of Upsilon_V (alone [-0.11, +0.60]), anisotropy (alone [-0.04, +0.55]) or membership (alone [-0.003, +0.52])
  is enough on its own to bring 0 inside the interval. Removing any one knob keeps 0 inside.
- With half widths it still contains 0: [-0.028, +0.524] / [-0.042, +0.513].
- Caveat (post-freeze diagnostic): the frozen rule draws each class's budget on its own. A Upsilon_V shift shared with
  the LG field dwarfs was not imposed. The satellite-minus-field difference has no power on disk: stat-only
  [-0.02, +0.44], because the LG field's own dataset term is 0.24 dex.

**Ellipticals and KiDS, EXPLAINED.** Both are carried by the IMF prior alone. sigma_0 and sigma_e move nothing on
their own. With half widths they still contain 0. KiDS is thin: its 68 % interval starts at 0.000 / +0.001.

## CMB row: SEPARATE

Read from the committed record, with no re-solve:

| Key (commit) | G9 (CMB) | Hot classes |
|---|---|---|
| KD1 K(Q) dust, unpinned (6c7f83ed02) | PASS (lensing chi^2 8.56) | G2 FAIL, G3 FAIL (G1-G7 all FAIL) |
| HC1 thermal fermion 11.14 eV (c207d70254) | FAIL (166-194) | G2 FAIL, G3 FAIL |
| LD1 late-decaying cold (d7db4e3403) | FAIL (46.3 / 53.0) | cluster f today 0.33 / 0.19 vs ~4 needed |
| EN1 shock-entropy field, 3 variants (eae8892550) | FAIL, carried (sigma = 0 before shocks) | G2 FAIL, G3 FAIL |
| QX12 iter_2 host-temperature step (7a1afa9b6b) | not graded (hot early; needs QX7's clock, KILLED) | FAIL |
| QX12 iter_3 isothermal sea (b605c9fd7c) | not graded | X-COP passes at 0 of 60 c_s0 |
| QX3 iter1-iter3 in the action (0240c8e31d, 602db4263d) | FAIL; iter2 shape PASS only at mu_K >= 4e4 (galaxies <= 79) | clusters FAIL (QX2 / QX5) |
| QX15 primary CMB with a cold component (1013e0362e) | PASS | that component is KD1/QX7's, retained by hosts; QX7 KILLED |

- No single key passes both G9 and the hot classes, so the label is SEPARATE.
- The keys that pass G9 (KD1, QX15's cold component) fail every hot class. No key in the record passes the hot classes
  at all, so SEPARATE here is a statement about the record, not a proof of two causes.
- SE1 had no committed result when this ran. The row should be re-read once SE1 lands.

## Known answers and MUTATE

| Check | canonical | alt | line |
|---|---|---|---|
| KA1: ST1 exec'd read-only vs committed st1.json (473 numbers + 255 labels) | 0 differ | (both footings inside) | exactly 0: **PASS** |
| KA2: SE2 machinery at ST1's settings (G4, G7, G6, G5, G3, G2) | max 0.0 | max 2.2e-16 | 1e-12: PASS |
| KA3: 9 UDG mean and se from the CSV vs S1 JSON | 0.0 | 0.0 | 1e-12: PASS |
| M2: zero-width priors reproduce the no-nuisance posteriors | 11/11 | 11/11 | must hold: HOLDS |
| **M1: inverted IMF bracket** (lambda ~ N(-1, 1), <= 0) | medians rise: ellipticals +0.278, KiDS +0.147, X-COP +0.041, groups +0.080. KiDS and ellipticals go EXPLAINED -> NOT EXPLAINED | +0.273, +0.147, +0.041, +0.080; same flips | must bite: **BITES** |

## Disclosed

1. **The IMF truncation is heavy-leaning.** lambda ~ N(1, 1) truncated at 0 has mean 1.29, heavier than Posacki. This
   favours explaining. The half-width reading (lambda sd 0.5, mean about 1.0) still reads EXPLAINED for the ellipticals
   ([-0.09, +0.26] / [-0.11, +0.25]) and for KiDS ([-0.04, +0.23] on both footings).
2. **The anisotropy width is a proxy.** It is the v3/EFE E-V vs E-W estimator difference (X1), applied to the plain-law
   Wolf data side.
3. **Name matching (frozen normalisation) left some systems unmatched in McConnachie 2012:** WLM, LGS 3 and Sextans,
   whose names carry parenthetical text. The LG field's 0.24 dex dataset term comes from old against new sigma for
   Cetus and Tucana (17.0 vs 8.3, 15.8 vs 6.2 km/s).
4. **The groups power rule had two raw readings (f* 0 and f* 1).** The script calls "no power" only if both contain 0.
   Both exclude 0, so either reading gives the same label.
5. **M2 ran in the main output, not in se2_MUTATE.*,** where the criteria had placed it. It is a code check and passed.
6. **Post-freeze additions, reported only; no label depends on them:** the half-width reading, the leave-one-out /
   knob-alone diagnostic, and the shared-Upsilon satellite-minus-field difference. They were added after the first main
   run. Every graded cell is byte-identical before and after, because the statistical and nuisance random streams are
   separate.
7. **Not in budget, by sign:**
   - The hydrostatic bias for X-COP and groups is set to 0; it would raise their step.
   - Gas in the ellipticals and the Coma UDGs is not on disk; it would lower their step.
   - Distance, photo-z and colour membership for KiDS and the ellipticals are not on disk.
8. **The UDGs' s_k come from S1's full 9-galaxy sample.** No UDG was removed, so this approximation was never used.
9. **The per-class rule lets each dSph class take its own Upsilon_V draw.** A shared Upsilon_V across dwarf classes and
   across the SPARC anchor is not imposed.
10. **Not blind.** ST1, GB1, S1, CFG948 and QX18-QX26 numbers were seen before the freeze.

Kappa = 1/2 FITTED; not theory closed.
