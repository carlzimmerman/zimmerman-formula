# CFG928 FROZEN CRITERIA: re-grade of CFG921's five posits with the IMF-corrected red-lens fact (C1) and clusters as a separate class (C2)

Block 920–929. The LEDGER reservation row says: "CFG928 = re-grade of CFG921's five posits with the IMF-corrected red-lens
fact (CFG926 R5) and clusters as a separate class".

These criteria were frozen on 2026-10-20 and committed ALONE, before any script of this lane exists and before this lane
computed any number.

**Kind:** RE-GRADE. Pre-registered, CONDITIONAL and POST-HOC-MOTIVATED (section 0). There are two declared changes and
nothing else.

**Standing rules:**
- κ = ½ is FITTED.
- The footings 9.3603e-11 / 1.1312e-10 m/s² are scored separately and never pooled.
- Only raw data and framework-native quantities are used.
- The extra mass is cold energy, not a particle.
- No knob scans. No posit constant is chosen here: each is re-fixed on the 83 LVD dwarfs exactly as in CFG921.
- Never "theory closed". Never "the data favour the framework".
- Any post-hoc change will be a dated, labelled AMENDMENT_A*.md, committed before the numbers it affects are reported.

## 0. Post-hoc status (read this first)

- **Designed after the earlier results.** This re-grade was designed after CFG921's result: all five posits FAIL, and the
  decisive facts are the red lenses (P2–P4) and the clusters (P2–P5). It was also designed after CFG926 R5 found that a
  literature IMF α–σ relation removes the red-lens excess, conditionally.
  - Both changes are motivated by those results.
  - A survivor here is therefore NOT evidence for its posit. Only its sealed prediction (section 6) can test it.
- **How C1 was selected.** C1 is the only one of six small reframings (CFG925 R1–R3, CFG926 R4–R6) that moved an excess, and
  it was picked for that reason.
  - This selection is disclosed. The trials factor (section 5) does not correct for it, because C1 is a change on the data
    side, not a posit.
- **C1 carries CFG926's condition:** disc galaxies stay near Chabrier.
  - If discs follow the same relation, CFG926 found the red/blue split barely moves (PARTIAL (MIXED)).
  - This lane reports that case as a diagnostic (section 3, C1-blue).

## 1. Question

Take CFG921's posits P1–P5 with their forms, inputs, brackets, dwarf calibration, estimators and grading rule unchanged, and
apply exactly two changes:
- **C1:** the red-lens fact is CFG926 R5's IMF-corrected value.
- **C2:** clusters are a separate class.

Which posits survive on the galaxy-scale facts, and which survive on all facts?

## 2. Record check and disclosure (NOT blind)

Read before freezing (targeted reads only):
- CFG921: README, FROZEN_CRITERIA (0abd82098), AMENDMENT_A1 (9585600db), cfg921.py in full, and the README's tables of
  observed values, predictions and nominal z.
- CFG926: README, AMENDMENT_A1, the R5 section of cfg926.py, and the R5 block of cfg926_results.json.
  - D_red = 0.17216 dex.
  - F1 before → after: 0.2934 → 0.1116 canonical, 0.2030 → 0.0216 alt.
  - SLUGGS Δ = 0.130: F1 0.1626 / 0.0724.
  - CFG850 colour window A_red: 1.451 → 1.208 canonical, 1.324 → 1.102 alt.
  - The nine IMF corners.
- CFG919: the build, lens_set and cells_lens code.
- LEDGER: the rows CFG920–927 and the 920–929 reservation row.
- LEDGER lines found by a search for UDG / tidal-dwarf tests, made while choosing the sealed-prediction class:
  - CFG7 FG041: tidal dwarfs are Newtonian.
  - CFG31: Coma UDGs, L23 stars-only isolated offset +0.397 / +0.357 dex.
  - CFG58: Coma UDGs, DF2/DF4 and tidal dwarfs under the cold-mass rule.

**Expectations formed before freezing**, from CFG921's committed table and CFG926's numbers (disclosed; nothing computed):
- **C1, primary.** P2–P4 predict the red lenses at 0.000–0.007. Against the corrected F1 (0.112 / 0.022, se 0.067), the
  nominal z is about −1.6 / −0.3. So F1 stops failing.
- **Galaxy-scale.**
  - P2 should SURVIVE on both footings: its other nominal z in CFG921 were below 2, and its dwarf-shape p was 0.87.
  - P4 should be UNDERDETERMINED: F8b +2.2 / about 2.0.
  - P3 should FAIL: F10, min |z| 3.9.
  - P1 should FAIL: calibration impossible.
  - P5 should FAIL: the dwarfs.
- **All facts.** P2–P5 should FAIL on the clusters, as in CFG921 (F5 min |z| 7.3 / 6.2).
- **Robustness.**
  - Under C1-S and C1-W, canonical F1 is about 0.15–0.16. P2's z is then about −2.2 to −2.4, so canonical P2 becomes
    UNDERDETERMINED (C1-DEPENDENT).
  - Under V7, the IMF correction applies without CFG667's +0.123 (F1 0.260 / 0.170 in CFG926). Canonical P2 likely FAILS
    there (FRAGILE).
- **UDGs.** If P2 survives, its UDG prediction at σ_law ≳ 15 km/s is ≲ 0.1 dex, far below CFG31's recorded Coma offset
  (about +0.4 dex). CFG31 used a different estimator and sample selection, but the sealed prediction may already be in
  tension with the record. It is sealed anyway (section 6). The test is left to a separate lane.

## 3. The two changes, and what stays

**C1: the red-lens fact.**
- The Sérsic n > 2 lens cells are rebuilt through CFG919's own lens code (lens_set + cells_lens) at an M* shift of
  0.123 + Δ_IMF.
  - These are the cells behind CFG921's F1 and the LS side of F7.
  - Δ_IMF = D_red, CFG926 R5's point value, read from cfg926_results.json (0.17216 dex).
- The central-galaxy proxy of the n > 2 lenses follows the same shift, in mass and in size. This is CFG921's own convention:
  lens_central takes the LS shift, as in its V7.
  - A Shen+03 R_e computed from the Chabrier-equivalent mass would be ×1/1.25. That lies inside the frozen R_e corner bracket
    ×{0.5, 1, 2}.
- Disc lenses (n < 2) are unchanged. This is CFG926's premise.

**C1 robustness variants.** Each is graded in full. They set a label only; the class does not change.
- **C1-S (SLUGGS ceiling).** Δ = CFG926's SLUGGS value, 0.130, read from the JSON.
- **C1-W (CFG850 window).** Δ_W is the smallest shift at which the graded F1 class mean has lost the fraction r_W of its
  uncorrected value.
  - r_W = 1 − ln A_red,after / ln A_red,before, from CFG926's window850 block: 0.493 canonical, 0.654 alt. This is the
    fraction CFG926's full correction removes on CFG850's colour window.
  - Δ_W is solved once per footing from the observed lens data alone, before any posit is graded: a 0.001-dex grid on
    [0, D_red], then bisection.
  - If F1 jumps across the target where a point crosses a window edge, the jump point is taken, and the F1 actually graded is
    reported.
- **Label.** If C1-S or C1-W changes a posit's combined class (section 4) on either footing, the posit is labelled
  **C1-DEPENDENT**.

**Diagnostic of C1's condition (no class weight).** C1-blue applies the same relation to the n < 2 lenses as well, at
CFG926's D_blue (0.159, read from the JSON). The discs' central proxy stays at CFG921's value. This is the case where the
premise is broken.

**C2: clusters as a separate class.** Each posit is graded twice.
- **(i) Galaxy-scale facts:** F0 (P5 only), F1 (with C1), F2, F3, F4, F7 (with C1), F8a, F8b, F9 and F10.
  - F5 and F6 are withheld. The joint χ² runs over F1–F4 (4 dof).
- **(ii) All facts:** F0–F10 with C1. The joint χ² runs over F1–F5 (5 dof).

**Unchanged from CFG921 (criteria 0abd82098 and AMENDMENT_A1):**
- the posit forms and inputs, and the bracket corners;
- the calibration on the 83 LVD dwarfs: CFG919 cells, GLS class mean, brentq, the lower root (A1-3), and θ± from the mean ± se;
- the fact estimators and fact sources;
- the per-fact z;
- the lenient-corner FAIL rule: min |z| ≥ 3 at EVERY corner, or the sign wrong at every corner; F8a p < 0.0027 at every σ_g
  corner;
- the sign rule;
- the SURVIVES rule: at the nominal corner every graded fact has |z| < 2 and no sign is wrong, F8a p ≥ 0.05, and the joint
  χ² p ≥ 0.05;
- P5's ⟨δ⟩ from CFG921's quadrature (A1 included);
- the variants:
  - V6: floor 0.10 dex.
  - V7: no CFG667 +0.123 on the n > 2 lenses. Under C1 the shift is then Δ_IMF alone.
  - If V6 or V7 changes a posit's combined class on either footing, it is labelled FRAGILE.
- CFG921's INJECT control is inherited, not re-run: the grading code and estimators are identical (K1).

## 4. Classes

**Per posit and footing.**
- class_gal = CFG921's grade on (i), and class_all = CFG921's grade on (ii). Each is FAILS, SURVIVES or UNDERDETERMINED by
  CFG921's rule.
- The combined class:
  - **SURVIVES (all):** class_all = SURVIVES and class_gal = SURVIVES.
  - **SURVIVES (galaxy-scale):** class_gal = SURVIVES and class_all ≠ SURVIVES.
  - **FAILS:** class_gal = FAILS. The posit fails even with the clusters set aside.
  - **UNDERDETERMINED:** class_gal = UNDERDETERMINED.
- Both components are always reported.

**Overall per posit.**
- If both footings give the same combined class, that is the overall class.
- If both footings are survivors at different levels, the overall class is SURVIVES (galaxy-scale).
- Otherwise it is UNDERDETERMINED (SPLIT BY FOOTING), with both footings reported.

**Labels.** None of these changes the class:
- FRAGILE (V6 or V7);
- C1-DEPENDENT (C1-S or C1-W);
- "robust to the trials factor" or "local" for each FAIL.

## 5. Trials factor (recomputed)

- **N_T = 20:** five posits × four fact framings ever graded on them:
  - CFG921 V0;
  - CFG921 VC;
  - CFG928 galaxy-scale;
  - CFG928 all.
- **Bonferroni threshold.** The correction runs over N_T × 11 = 220 tests at two-sided p = 0.0027.
  - z_TF = Φ⁻¹(1 − 0.0027/440) ≈ 4.37, computed exactly in the script.
  - CFG921 used N_T 5 and z_TF 4.06.
- **Robust or local.** A FAIL is "robust to the trials factor" if any of these holds:
  - its decisive |z| ≥ z_TF;
  - a sign is wrong at every corner;
  - for F8a, its max p < 2Φ(−z_TF).

  Otherwise it is "local".
- **Survivors.** Any survivor is labelled "best of 20 posit-framings tried, post-hoc-motivated, conditional on C1".

## 6. Survivors: the cluster statement and one sealed prediction

**Cluster statement.** For every posit that SURVIVES (galaxy-scale) on a footing, the README reports:
- its constant θ (with θ±);
- its nominal cluster predictions F5 and F6, from the "all" grading;
- what a separate cluster explanation must then supply: observed minus predicted, in E and in ×g, plus the F6 slope.

**Sealed prediction: ONE, with a target class fixed now.** The target class is pressure-supported ultra-diffuse galaxies
(UDGs) with measured stellar or globular-cluster velocity dispersions.
- **Status of the class.** No UDG is graded in CFG921 or CFG928.
- **Not blind with respect to the record.** Section 2 lists what was seen. No UDG data file is opened by this lane before the
  seal, and L23's data are not opened at all.
- **Formula.** The prediction is the posit's own dwarf self-consistent solution with the calibrated θ (CFG921 section 4, as
  coded in dw_pred). Its inputs are M*, R_e (r12 = 4/3 R_e), M_g,in and σ_g.
  - E is taken relative to the isolated ν_e law. It is EFE-free, like the record's dwarf numbers, and the posits carry no host
    variable.
- **Declared representative inputs.** No object data are used.
  - M* ∈ {3e7, 1e8, 3e8} M☉ × R_e ∈ {1.5, 2.5, 4.0} kpc.
  - Gas-free (w = 1) is primary.
  - The gas-bearing variant has M_g,in = M*/2, with σ_g at the nominal 10 km/s and the corners 6 and 20.
  - Each prediction is given with its θ± spread, on each footing where the posit survives.
- **When the numbers are computed.** The script computes these numbers after the main grading, and only for galaxy-scale
  survivors.
- **Kill line (form frozen now).** Take a future sample of N ≥ 5 UDGs, measured with the CFG880/919 estimator: Wolf σ at r12,
  M* = 2 L_V, M_b/2 inside r12, the isolated ν_e law and E = 2 ln(σ_obs/σ_law).
  - The posit is EXCLUDED on that footing if the sample-mean observed E differs from the sample-mean predicted E by
    ≥ 3√(se_obs² + σ_pred²).
  - The predicted E uses each galaxy's own inputs through the sealed formula.
- **Commit order.** SEALED_PREDICTION_<posit>.md is written after the main run. It is committed alone, before the README and
  before any UDG data are opened.

If no posit survives on the galaxy-scale facts, no seal is written, and the README says so.

## 7. Controls

Any K failure stops the lane: no class is reported (exit 2).

**K-tests.**
- **K0.** cfg921.py is exec'd read-only up to its MAIN section, with writes refused and sys.exit trapped. Its own K1–K7 must
  pass inside the exec; CFG919's and CFG914's checks run through it.
- **K1 (C1 and C2 off).** This lane's pipeline must reproduce CFG921's committed cfg921_results.json. The pipeline is: the lens
  rebuild at shift 0.123, this lane's copy of obs_struct, and CFG921's grade.
  - Scope: V0, V6, V7 and VC; both footings; every posit.
  - Compared items:
    - the class;
    - θ, θ+ and θ− at every σ_g corner;
    - every nominal fact (pred, z, sign flag);
    - min |z| over corners;
    - F8a χ² and p;
    - joint χ² and p;
    - the failed set;
    - the decisive fact;
    - robust_TF, at CFG921's z_TF 4.06;
    - CFG921's classes block;
    - the observed facts (value, se).
  - Tolerance: numbers within 1e-12 (absolute, or relative for |x| > 1); strings exactly.
- **K2.** The lens rebuild:
  - at shift 0.123 it equals CFG919's build(f, {}), and at 0.0 it equals build(f, {noshift}), exactly (cells and covariance,
    both footings);
  - this lane's obs_struct copy equals CFG921's obs_struct for V0, V6 and V7 (every array and index).
- **K3.** CFG926's numbers are reproduced through this lane's path to ≤ 1e-9:
  - F1 at 0.123 + D_red equals CFG926's target_F1.res;
  - F1 at 0.123 + 0.130 equals CFG926's SLUGGS F1;
  - F1 at 0.123 equals CFG926's obs;
  - r_W is recomputed from the JSON's A_red values.

**MUTATE runs.** Each writes its own outputs.
- **MUTATE uncorr** (CFG928_MUTATE=uncorr → cfg928_MUTATE_uncorr.out / .json; exit 1 = bites).
  - C1 is off: the red lenses are back at +0.123 only. C2 is on.
  - It bites only if every posit and footing returns CFG921's classes:
    - galaxy-scale = CFG921's VC classes;
    - all = CFG921's V0 classes;
    - no SURVIVES anywhere;
    - every CFG921 FAIL is a FAIL here.
- **MUTATE sign** (CFG928_MUTATE=sign → cfg928_MUTATE_sign.out / .json; exit 1 = bites).
  - C1 and C2 are on.
  - M1a: the reversed surplus (P1–P4). M1b: the sign-flipped nominal predictions (P1–P4).
  - Each is graded on the galaxy-scale facts and on all facts, on both footings.
  - It bites only if all 32 cases FAIL.

**Run order:** K-only (CFG928_KONLY=1), then MUTATE uncorr, then MUTATE sign, then main.

## 8. Compute and hygiene

- One core (OMP_NUM_THREADS=1, nice -n 10), < 1 GB, one process at a time. Nothing is downloaded.
- No other lane's file is edited. cfg921.py (and through it CFG919/914/880/883/687) is exec'd read-only. CFG926's JSON is
  read only.
- Outputs:
  - cfg928.py → cfg928.out and cfg928_results.json;
  - the K-only run → cfg928_K.out and cfg928_results_K.json;
  - the MUTATE runs are named by mode.
- Commits use explicit paths only.

κ = ½ FITTED; footings never pooled; not theory closed.
