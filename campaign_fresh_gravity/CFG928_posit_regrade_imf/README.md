# CFG928: re-grade of CFG921's five excess selectors with IMF-corrected red lenses and clusters as a separate class

**Bottom line.** With the red-lens excess IMF-corrected (CFG926 R5) and the clusters set aside, **P2 (velocity-space capture)
SURVIVES on the galaxy-scale facts on both footings**. It still **FAILS once the clusters are included**. Its survival is
weak in four ways:
- **FRAGILE:** without CFG667's +0.123 dex it fails on the canonical footing.
- **C1-DEPENDENT:** under CFG926's weaker SLUGGS and CFG850-window variants it drops to UNDERDETERMINED on the canonical
  footing.
- **Post hoc and conditional:** see the next section.
- **Not evidence for P2:** its fit is the best of 20 posit-framings tried.

The other posits:
- P4 is UNDERDETERMINED on both footings.
- P1, P3 and P5 FAIL on both footings, as in CFG921.
- No posit survives on all facts. The cluster excess (×1.75 / ×1.61, rising with g_bar) needs a separate explanation.

One sealed prediction, for P2 on ultra-diffuse galaxies, is committed in `SEALED_PREDICTION_P2.md`.

**This is a conditional, post-hoc-motivated test.**
- **Timing:** it was designed after CFG921's failures and after CFG926 R5 were seen.
- **Selection:** C1 is the one reframing, of six in CFG925/926, that moved an excess.
- **Condition:** C1 holds only if disc galaxies stay near Chabrier.

| posit (one constant, fixed on the 83 LVD dwarfs as in CFG921) | canonical | alt | galaxy-scale / all | labels | decisive |
|---|---|---|---|---|---|
| P1 stress coupling (c_*) | FAILS | FAILS | FAILS / FAILS | — | calibration impossible (as CFG921) |
| **P2 velocity-space capture (v_2 6.95 / 6.46 km/s)** | **SURVIVES (galaxy-scale)** | **SURVIVES (galaxy-scale)** | SURVIVES / FAILS | **FRAGILE** (V7); **C1-DEPENDENT** (canonical: C1-S, C1-W) | all facts: clusters F5 z −7.3 / −6.2, slope F6 −5.3 / −5.4 (robust) |
| P3 late binding + escape (v_w 27.6 / 23.9 km/s) | FAILS | FAILS | FAILS / FAILS | — | dwarf size split F10 min \|z\| 3.88 / 3.94 (local, below z_TF 4.37) |
| P4 phase-space-density capture (Q_* 5.04e-7 / 6.30e-7) | UNDERDETERMINED | UNDERDETERMINED | UNDERDETERMINED / FAILS | FRAGILE (V6 → SURVIVES (galaxy-scale) on both footings; V7 → canonical FAILS) | dwarf g_bar slope F8b z +2.17 / +2.19 |
| P5 QUMOND geometry (no constant) | FAILS | FAILS | FAILS / FAILS | — | dwarfs F0 −8.2 / −7.3 (robust) |

**Overall:**
- P2: SURVIVES (galaxy-scale), conditional.
- P4: UNDERDETERMINED.
- P1, P3, P5: FAIL.
- Survivors on all facts: none.

κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled. Raw data and framework-native quantities only. The
extra mass is cold energy, not a particle. No knob scans: no constant was refitted; the dwarf calibration is CFG921's
(max |Δθ| = 0). Not "theory closed". Nothing here says the data favour the framework.

- **Kind:** RE-GRADE (pre-registered; post-hoc-motivated; conditional). Block 920–929.
- **Criteria:** `FROZEN_CRITERIA.md`, ba971914e, committed alone before any script or number. No amendments.
- **Results:** 82a69be8f (script and all outputs).
- **Seal:** 3fa5a2bfc (`SEALED_PREDICTION_P2.md`, committed alone before this README; no UDG data opened).
- **Not blind:** CFG921's and CFG926's numbers were read before freezing. The expectations formed then are disclosed in
  criteria section 2, and the outcome matched them: P2 survives on galaxy-scale, P4 UNDERDETERMINED, P3/P1/P5 fail, canonical P2
  C1-dependent under S/W and fragile under V7.

## The two changes (and nothing else)

**C1: the red-lens fact.**
- The Sérsic n > 2 lens cells, behind F1 and the LS side of F7, are rebuilt through CFG919's own lens code at an M* shift of
  0.123 + D_red.
  - D_red = +0.17216 dex: CFG926's ATLAS3D α–σ relation at σ ≈ 186 km/s, read from its JSON.
- The n > 2 central-galaxy proxy follows the same shift, which is CFG921's convention.
- Discs stay at Chabrier.

| red-lens fact (E in ln; dex = E/ln 10) | canonical F1 | alt F1 | F7 = DW − LS (canonical / alt) | role |
|---|---|---|---|---|
| CFG921, uncorrected (+0.123 only) | +0.293 ± 0.067 (+0.127 dex) | +0.203 ± 0.067 | +0.628 / +0.627 | K1, MUTATE uncorr |
| **C1 primary (+0.123 + 0.172)** | **+0.112 ± 0.066 (+0.048 dex)** | **+0.022 ± 0.066 (+0.009 dex)** | +0.772 / +0.772 | class |
| C1-S, SLUGGS ceiling (+0.123 + 0.130) | +0.163 (45% removed) | +0.072 | +0.722 / +0.722 | C1-DEPENDENT label |
| C1-W, CFG850-window equivalent (+0.123 + 0.141 / 0.132) | +0.149 (49.3% removed) | +0.070 (65.4%) | +0.735 / +0.724 | C1-DEPENDENT label |
| C1 + V7, IMF without CFG667 (+0.172 only) | +0.260 | +0.170 | +0.625 / +0.625 | FRAGILE label |
| C1 + V6, floor 0.10 dex | +0.108 ± 0.111 | +0.018 ± 0.111 | +0.817 / +0.817 | FRAGILE label |
| C1-blue diagnostic: discs also shifted (+0.159) | F1 as primary; F2 −0.112 ± 0.084 | F2 −0.203 ± 0.084 | as primary | no class weight |

**C2: clusters are a separate class.** Each posit is graded twice:
- **(i) galaxy-scale facts:** dwarfs (F0 for P5), red lenses (C1), blue lenses, SPARC small and large, DW − LS, dwarf shape,
  slope, gas and size splits. F5 and F6 are withheld; the joint χ² runs over F1–F4.
- **(ii) all facts:** F0–F10. The joint χ² runs over F1–F5.

**Unchanged from CFG921:**
- the forms, inputs and brackets;
- the calibration on the 83 LVD dwarfs. The θ are identical to CFG921's: max |Δθ| = 0;
- the estimators;
- the lenient-corner FAIL rule: min |z| ≥ 3 at every corner, or the sign wrong at every corner;
- the SURVIVES rule;
- the variants V6 and V7;
- the fact sources.

## Results (C1 primary, galaxy-scale grading, nominal z)

| posit | F1 red | F2 blue | F3 SS | F4 SL | F7 DW−LS | F8b dwarf slope | F9 gas | F10 size | dwarf shape p | joint χ²/4 (p) |
|---|---|---|---|---|---|---|---|---|---|---|
| P2 canonical | −1.7 | −0.1 | −1.6 | −0.0 | +0.7 | −0.7 | +0.3 | +1.5 | 0.87 | 5.5 (0.24) |
| P2 alt | −0.3 | +0.9 | −0.7 | +1.1 | +0.1 | −0.5 | +0.3 | +1.7 | 0.88 | 2.5 (0.65) |
| P3 canonical / alt | −1.6 / −0.3 | 0.0 / +1.0 | −1.4 / −0.5 | 0.0 / +1.1 | +0.6 / 0.0 | +0.7 / +0.8 | +0.1 / +0.1 | **+3.9 / +3.9** | 0.61 / 0.57 | 4.4 / 2.5 |
| P4 canonical / alt | −1.7 / −0.3 | −0.1 / +0.9 | −1.6 / −0.6 | 0.0 / +1.1 | +0.8 / +0.2 | **+2.2 / +2.2** | 0.0 / 0.0 | −0.8 / −0.3 | 0.33 / 0.32 | 5.2 / 2.4 |
| P5 canonical / alt | −1.4 / 0.0 | +0.1 / +1.1 | −1.6 / −0.7 | 0.0 / +1.1 | **−6.0 / −6.0** | **+4.0 / +4.0** | +0.6 / +0.5 | **+7.6 / +7.6** | 2e-18 / 2e-15 | F0 **−8.2 / −7.3** |

**What C1 changed.**
- P2–P4 still predict the red lenses at about 0. Their red-lens predictions are +0.000 to +0.006, because velocity-scale
  selectors switch off at the central σ ≈ 121 km/s of the n > 2 proxy.
- What moved is the target. The red-lens failure that killed P2–P4 in CFG921 (min |z| 4.38 / 3.03 for P2) falls to 1.7 / 0.3.
- F7 moves from z +1.6 to +0.7.

**What C2 changed.** Nothing in the numbers: it removes the cluster facts from the galaxy-scale grade. On all facts P2–P5 fail
exactly as in CFG921 (F5 min |z| 7.28 / 6.19; F6 5.31 / 5.38), robust to the trials factor.

**Robustness of P2's survival:**

| scenario | canonical | alt | why |
|---|---|---|---|
| C1 primary | SURVIVES (galaxy-scale) | SURVIVES (galaxy-scale) | all nominal \|z\| < 2 |
| C1 + V6 (floor 0.10 dex) | SURVIVES (galaxy-scale) | SURVIVES (galaxy-scale) | larger floor softens F1 |
| C1 + V7 (no CFG667 +0.123) | **FAILS** (F1 min \|z\| 3.95, local) | UNDERDETERMINED (F1 −2.57) | the IMF alone removes only part of the excess |
| C1-S (SLUGGS ceiling) | **UNDERDETERMINED** (F1 −2.47) | SURVIVES (galaxy-scale) | 45% removed (canonical) |
| C1-W (CFG850 window) | **UNDERDETERMINED** (F1 −2.26) | SURVIVES (galaxy-scale) | 49% removed (canonical) |
| C1-blue diagnostic (premise broken) | SURVIVES (galaxy-scale) (F2 +1.34) | UNDERDETERMINED (F2 +2.43) | disc lenses fall below the law |

So P2's galaxy-scale survival on the canonical footing needs both of the following:
- CFG667's +0.123 dex stellar-mass correction;
- the full point-value IMF correction (≥ about 60% of the red-lens excess removed).

On the alt footing it is robust to the S/W variants, but not to V7 or to C1-blue.

**P4.** P4 is UNDERDETERMINED on both footings. Its phase-space selector predicts too shallow a dwarf g_bar slope:
−0.30 against −0.66 observed, z +2.2, min over corners 1.98 / 2.01. Under V6 it SURVIVES (galaxy-scale) on both footings, so
it is labelled FRAGILE.

**P3.** P3 still FAILS on the dwarf size split: predicted d −0.66 against −1.36 ± 0.18, min |z| 3.88 / 3.94. This failure has
nothing to do with the lenses or clusters. It is local: it is below both the recomputed z_TF of 4.37 and CFG921's 4.06 (in CFG921, P3's robust label came from its red-lens F1, 4.19).

## P2: constant, clusters, sealed prediction

- **Constant.**
  - v_2 = 6.9503 km/s canonical (θ± 7.848 / 6.103) and 6.4575 km/s alt (7.344 / 5.617), from CFG921's dwarf calibration.
  - The value is still close to the record's 7.5 km/s clump scale. CFG921 flagged that as a coincidence.
- **Clusters.**
  - P2 predicts no cluster excess: F5 = +3e-6 / +2e-6, and the slope F6 = −4e-6 / −3e-6.
  - A separate cluster explanation must therefore supply the whole observed excess: E = +0.560 ± 0.077 (×1.75 in g) canonical
    and +0.476 ± 0.077 (×1.61) alt (CFG687's A_MID is 1.910 / 1.754).
  - That excess must rise with g_bar at +0.83 / +0.84 per dex.
  - The cluster census cannot supply it: CFG922 found the excess STANDS. The IMF cannot either: CFG926 found NO EFFECT.
- **Sealed prediction** (`SEALED_PREDICTION_P2.md`, 3fa5a2bfc). Target: pressure-supported ultra-diffuse galaxies.
  - **What it predicts.** P2 predicts that gas-free UDGs sit nearly on the isolated law:
    - E = +0.02 to +0.14 ln (+0.01 to +0.06 dex) canonical, and +0.016 to +0.105 alt, for M* = 3e7–3e8 M☉;
    - the value is set by σ_law (12–23 km/s), not by size.
  - **Kill line.** For N ≥ 5 UDGs on the CFG880/919 estimator, P2 is excluded if |⟨E_obs⟩ − ⟨E_pred⟩| ≥ 3 combined se, per
    footing.
  - **Disclosed.** The record's CFG31 Coma-UDG offset (+0.40 dex, L23's estimator) would exclude P2 if it holds under this
    estimator. That comparison is not made here.

## Trials factor

- **N_T = 20:** five posits × four framings graded on them (CFG921 V0, CFG921 VC, CFG928 galaxy-scale, CFG928 all).
- **Threshold:** Bonferroni over 220 tests gives z_TF = 4.373 (CFG921: 4.060).
- **Robust FAILs:**
  - P5: dwarfs.
  - P2–P5 on all facts: clusters.
- **Local FAILs:**
  - P3: F10, 3.88 / 3.94.
  - C1 + V7: P2–P4 on F1, 3.4–3.95.
- **Selection not counted.** The selection of C1 from six reframings is not in N_T. It is disclosed instead, as the
  post-hoc label.

## Controls

| control | result |
|---|---|
| K0 | cfg921.py exec'd read-only to its MAIN section (writes refused, sys.exit trapped): its own K1–K7 pass, and with them CFG919's and CFG914's checks |
| K2 | lens rebuild at shift 0.123 / 0.0 equals CFG919's build(f, {}) / build(f, {noshift}) exactly (cells and covariance, max diff 0); this lane's obs_struct copy equals CFG921's for V0, V6, V7 (max diff 0) |
| **K1** | **C1 and C2 off: CFG921 reproduced exactly.** 40 posit records (V0, V6, V7, VC × 5 × 2), the observed facts and the classes block; max rel diff 0, no mismatches |
| K3 | CFG926 R5 through this lane's path: F1 at 0.123 (obs, se), at 0.123 + D_red and at 0.123 + 0.130 equal CFG926's numbers to 6e-17; r_W 0.4926 / 0.6543 |
| MUTATE uncorr | **BITES.** With the red lenses back at +0.123 and C2 on, CFG921's classes return: galaxy-scale = CFG921 VC (P2 F1 min \|z\| 4.38 / 3.03; P4 canonical FAILS, alt UNDERDETERMINED), all = CFG921 V0 (all FAIL), no survivor |
| MUTATE sign | **BITES.** All 32 cases FAIL, with C1 and C2 on. M1a, reversed surplus: calibration impossible. M1b, sign-flipped predictions: F10 sign. Both footings, both framings |
| UDG path self-check (added, no class weight) | the 83 LVD dwarfs' own (M*, M_g,in, r12) through the sealed-prediction path reproduce CFG921's g_bar, σ_law, w, ρ̄ and E_pred to 2e-15 |

CFG921's INJECT control is inherited, not re-run. The grading code and estimators are identical (K1).

## What this means for the cold sector

- **IMF-dependent survival.** If old spheroids have the ATLAS3D-like IMF (and discs do not), a single dwarf-calibrated
  velocity-scale selector (P2, v_2 ≈ 7 km/s) is no longer excluded by the galaxy-scale facts. It reproduces the dwarf excess,
  its g_bar and size trends, and red and blue lenses and SPARC near the law.
- **Clusters need something separate.** The cluster-core excess still needs a separate explanation that P2 does not provide.
  That is a second ingredient, so "one selector for everything" stays excluded.
- **Narrow margin.** On the canonical footing P2's survival needs CFG667's +0.123 dex and the full IMF point value. With the
  weaker IMF readings it is UNDERDETERMINED, and without CFG667 it FAILS.
- **Next test.** The sealed UDG prediction is the test of P2, along with an IMF measurement for KiDS-like red lenses that is
  independent of the law.

## Limitations

- **C1 is conditional on discs staying near Chabrier.** C1-blue shows the alt footing loses P2's survival if discs share the
  relation.
- **Lens inputs are proxies.** Lens central masses, sizes and f_P are proxies, as in CFG921. Under C1 the n > 2 central proxy
  follows the shifted mass in size too (CFG921's convention). A Chabrier-based Shen+03 size would be ×0.8, inside the
  R_e × {0.5, 2} corners. P2–P4's red-lens predictions are ≈ 0 either way.
- **C1-W is a translation.** It turns CFG926's colour-window removal fraction into the F1-cell statistic through an effective
  shift. It is not CFG850's estimator itself.
- **No independent check of the red-lens excess.** The +0.123 (CFG667) and the IMF relation (ATLAS3D OLS) both come from the
  record. No independent lensing-side IMF check exists here.
- **Dwarf inputs are CFG921's.** That means Υ_V = 2, CFG880 gas and the Wolf estimator. CFG925 found the estimator choice does
  not matter.
- **The UDG prediction is not blind with respect to the record** (see the seal's disclosure).

## Reproduce

One core, < 0.5 GB, about 20–60 s each; nothing downloaded. Run order: K, MUTATE uncorr, MUTATE sign, main.
- `CFG928_KONLY=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg928.py` → `cfg928_K.out`, `cfg928_results_K.json` (exit 0)
- `CFG928_MUTATE=uncorr ...` → `cfg928_MUTATE_uncorr.out`, `cfg928_results_MUTATE_uncorr.json` (exit 1 = bites)
- `CFG928_MUTATE=sign ...` → `cfg928_MUTATE_sign.out`, `cfg928_results_MUTATE_sign.json` (exit 1 = bites)
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg928.py` → `cfg928.out`, `cfg928_results.json` (exit 0)

No other lane's files were edited. cfg921.py is exec'd read-only, and through it CFG919/914/880/883/687. CFG921's and CFG926's
JSON files are only read.
