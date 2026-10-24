# X21_cluster_switch_anatomy: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. Theory frozen as v3s
(`covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md`). κ = ½ FITTED. Footings canonical a₀ 9.3603e-11 / alt
1.1312e-10 m s⁻², reported side by side, never pooled. No dark-matter particle. No fitted knob as a cure. Never "theory
closed". Never "the data favour the framework". Inputs and classes: `ASSUMPTION_LEDGER.md`.

## 0. Question

The eRASS1 × KiDS stack of 326 clusters sits at A_MID ≈ 1.5–1.7 × the law in MID (X2's bins 3–5, 0.46–1.42 Mpc; the brief's
"0.3–1 Mpc" is this band) (F1, X2, X7, X11, X13). X7 finds the lightest MGAS500 tercile at A ≈ 1 and the heavier two at
≈ 1.8, but grades the MID mass trend UNDECIDED (step Δχ² 4.2–4.6 < 9; quintiles not monotone). X19 calls the split "cluster T1
NONE, T2/T3 EXTRA" near M_b ≈ 8e12 M☉ and notes it is partly built in, because the terciles are cut on MGAS500.

(i) Is the cluster "switch" a real threshold, a smooth trend, or an artefact of binning on MGAS500? (ii) What does the
per-cluster excess track? (iii) Can known baryons that the model omits supply the heavy terciles' excess (+0.26 dex), with
the right mass dependence?

**Seen before freezing (disclosed).** BRIEF; X7 README, criteria and `x7_analysis.py` (full), the key layout of its results
JSON and its all-cluster / tercile CAL numbers (README); X13 README and the key layout of its JSON (`reference`,
`corrections`); X2 `x2_cluster_outskirts.py` (model, `gas`, `model`, `stack_model`, the GS/PS needed-amount block); F1
`f1_cluster_cores.py` (model section) and ledger rows A12/B10; CFG922 README (census, brackets, classes) and the field names
of `cfg922_census_A1.json`; CFG929 README (top); CFG688 script; CFG726 README (top); ZT2B README; X19 README (cluster rows).
Availability counts computed before freezing (no A value): the 326 X7 clusters all match the eRASS1 FITS by NAME with
MGAS500 identical; KT > 0 for 106; CFG688's redMaPPer rule (< 2′, |Δz| < 0.04) matches 83; 281 of the 326 match CFG687's 318
exactly by position (CFG922 census order = CFG687 order); 214 of CFG922's 318 have a measured, non-zero BCG mass.
**No A_MID, slope, step or budget number of this lane exists.**

## 1. Data, statistic, cells

- **Per-cluster arrays:** X7's committed `x7_measure_percluster.npz` (equal to X2's replay; X7 K1). Nothing is re-measured.
- **Model:** X2's C\* (F1 PRIMARY + CFG814 r⁻³ gas beyond 2.2 R500 + Chae+21 noclu EFE via F2's solver + reduced shear), built
  with X2's functions exec'd read-only from its source text exactly as `x7_analysis.py` does (sha256 recorded).
- **Per-cluster MID sums (boost convention, CAL leakage):** n_i = Σ_{j∈MID} W_ij B_j (D_ij − leakP_ij,t), d_i = Σ_{j∈MID} W_ij
  P_ij (C\*), W = 1/E², B = the stack boost (X7's DAT construction). A(S) = Σ_S n / Σ_S d. This is X7's A_CAL for any S.
- **Cells:** 2 footings × 2 native h (0.672, 0.686) = 4 cells, never pooled. A class needs all 4 cells.
- **Errors (the record's):** σ_STAT = max(σ_boot, σ_jk); σ_boot = 2000-draw cluster bootstrap (default_rng([20261024, key]));
  σ_jk = X2's 30 equal-count RA patches restricted to the selection.

## 2. Step 0 (stop rule)

Reproduce from the committed arrays, with my code:
- **S0-a:** X7's all-cluster A_MID (A, A_CAL) and its terciles' and quintiles' per-bin A_CAL and σ_STAT (X7 JSON `bins`, X7's
  bootstrap keys 100+k / 200+k) to ≤ 1e-9 absolute, in all 4 cells.
- **S0-b:** X7's MID tercile and quintile CAL Δχ²_S1 and Δχ²_S2 (X7 JSON `trend`) to ≤ 0.05. The per-bin σ_leak cannot be rebuilt
  (X7's per-group templates are in a scratch file, not committed); this lane uses σ_leak,b = σ_leak,ALL × √(Σ_ALL d / Σ_b d)
  (≤ 0.002; declared approximation). Everything else in X7's CAL covariance (coherent v vᵀ + u uᵀ from the all-cluster s_×, s_RR,
  κ_b) is rebuilt exactly.
- **S0-c:** X13's all-source A_MID and Z_STAT (`reference.<cell>.A_ALL`, `Z_ALL_STAT`) to ≤ 1e-6. X13's selection-corrected
  size-halves A_MID (`corrections.<cell>.sel`) is quoted from its JSON. This lane never splits sources, so X13's selection
  correction does not apply to any number here (X13: the all-source estimator has no split and is unaffected).
- **Stop:** if S0-a or S0-c fails, the lane stops and reports. S0-b failing is reported and the binned Δχ² tables carry the
  flag; the graded tests (§3) do not use σ_leak,b.

## 3. Re-binning without MGAS500 (step 2; graded)

**Variables V (each on its own available subset of the 326):**
- V1 KT (eRASS1 `KT` > 0; 106), x = log10(V / median).
- V2 redshift (eRASS1 `BEST_Z`; 326), x = V − median.
- V3 X-ray luminosity (eRASS1 `L500`; 326), x = log10(V / median).
- V4 concentration / cool-core proxy c_X = `L300kpc` / `L500` (326), x = V − median. eRASS1 has no cool-core flag; this is the
  only relaxation-type quantity in the catalogue.
- V5 richness λ (CFG688's committed redMaPPer TSV, CFG688's match rule: nearest within 2′ and |Δz| < 0.04; 83), x = log10.
- V6 BCG stellar mass (CFG922 A1 census `bcg_med`, measured clusters with bcg_med > 0, matched to the 326 by exact position via
  CFG687's npz), x = log10.
- V7 central stellar-to-gas ratio S_cen / gas_cyl (CFG922 A1 census, measured clusters, matched), x = log10.
- Control V0 = MGAS500, unbinned, x = log10 (reported; does not count as a "non-MGAS500" variable). eRASS1 M500 reported only.

**Per V, per cell (unbinned, no bins anywhere in the graded test):**
- (a) **Linear:** minimise Σ_i (n_i − (a + b x_i) d_i)² / d_i over the subset (the 1/d weight makes the constant fit equal the
  ratio-of-sums A). Z_lin = b / σ_STAT(b).
- (b) **Median step:** Δ_med = A(V ≥ median) − A(V < median); Z_med = Δ_med / σ_STAT(Δ).
- (c) **Scanned step:** breaks at subset quantiles q = 0.20, 0.25, …, 0.80; T = max_q |Δ(q)| / σ_perm(q), σ_perm(q) the standard
  deviation of Δ(q) over 2000 permutations of V among the subset's clusters (default_rng([20261024, 7000 + code])); p_scan =
  fraction of permutations with T_perm ≥ T. V\* = the break at the max. Also p_lin = permutation p of |b|.
- (d) **Joint shape fit:** a + b x + c H(x − x_med), same weights; Z_b, Z_c with σ_STAT from the same bootstrap/jackknife.
- Reported only: Spearman ρ(V, MGAS500); the trend at fixed mass (a + b x_V + m log10(MGAS500/median), Z_b).

**Dependence class per V:** DETECTED if min over cells of max(Z_lin², Z_med²) ≥ 9; NONE if max over cells of max(Z_lin², Z_med²)
< 4; WEAK otherwise.
**Shape per DETECTED V:** THRESHOLD if in all 4 cells |Z_c| ≥ 2, |Z_b| < 2 and p_scan ≤ 0.01; SMOOTH if in all 4 cells |Z_b| ≥ 2
and |Z_c| < 2; otherwise SHAPE UNRESOLVED.

**Binned tables (reported, never graded):** terciles of each V on its subset (np.quantile 1/3, 2/3) and quintiles for the
326-cluster V (and V0); per bin A_MID,CAL, σ_STAT, Z; X7's GLS shapes S0 / S1 / S2 (step at the T1|T2 edge, X7's convention)
with X7's CAL covariance (§2 S0-b approximation for σ_leak,b); Δχ²_S1, Δχ²_S2, BIC-preferred shape.

## 4. Trend verdict (frozen classes; V ∈ {V1 … V7})

- **REAL THRESHOLD at V\***: some V is DETECTED with shape THRESHOLD (V\* reported per cell).
- **SMOOTH TREND in V**: some V is DETECTED with shape SMOOTH, and none is THRESHOLD (all such V named).
- **BINNING ARTEFACT**: every V1 … V7 is NONE and V0 (MGAS500 unbinned) is not DETECTED.
- **UNDECIDED**: otherwise (including a DETECTED V with SHAPE UNRESOLVED, or V0 DETECTED with every other V NONE, which is
  reported as "MGAS500-specific").
- Disclosed: 7 variables are tested; the DETECTED line (Δχ² ≥ 9 in all 4 correlated cells) is not trial-corrected.

## 5. Baryon budget (step 3; graded)

**Needed extra baryons** for A_MID,CAL = 1 in each selection S ∈ {all 326, X7's MGAS500 terciles T1, T2, T3}, per cell, with
X2's own C\* components (no new shape): **GS** (λ × the C\* gas profile, sourcing AQUAL) and **PS** (central point mass λ × Mg500,
sourcing AQUAL). Each is evaluated on a fixed λ grid and solved per selection on Σ_S n = Σ_S d(λ) by monotone interpolation.
λ is a diagnostic of the required mass, never carried into any model. If A(S) ≤ 1, the need is 0. Needed mass per cluster:
PS λ Mg500,i; GS λ M_gas,i(< 0.5 Mpc, 3D) (reported).

**Bracket of omitted known baryons (record only; matched 281 clusters; inside the CFG922 R < 0.5 Mpc cylinder):**
- measured stars incl. BCG: CFG922 A1 S_up (upper) and S_cen (central);
- stellar M/L: × 3.78 / 1.78 = 2.12 on the upper end (CFG922's SLACS α_max over Chabrier);
- cold atomic gas: f_HI,95 = 0.196 × stars (CFG922, xGASS); molecular gas not on disk: bracket set equal to the HI bracket;
- **generous bracket** B_up = 2.12 S_up (1 + 0.196 + 0.196), counted wholly as omitted (the f\* = 0.20 stars already in the model
  are not subtracted); **central** B_cen = S_cen − 0.20 gas_cyl (the measured stars beyond what the model already holds);
- ICL: not on disk (CFG922: NOT TESTABLE). Reported as the needed multiple k_ICL = (Σ need_PS − Σ B_up) / Σ S_up.
- Cross-check, reported: X-COP's stellar M\*/M_gas(< 0.5 Mpc) upper end 0.104 (CFG922).

**Mass dependence (reported per tercile):** median S_cen / gas_cyl and S_up / gas_cyl, against needed PS mass / Mg500.
**MATCH** if the needed fraction and the bracket fraction both rise (or both fall) from T1 to T3; **MISMATCH** otherwise.

**Budget classes (graded on T2 and T3, PS need, all 4 cells):**
- **BARYON BUDGET CLOSES IT**: Σ B_up ≥ Σ need_PS in both T2 and T3 in all 4 cells, and the mass dependence is MATCH.
- **BARYON BUDGET INSUFFICIENT**: Σ B_up < Σ need_PS in T2 or T3 in all 4 cells, and k_ICL > 10 there (CFG922's declared ×10
  implausibility scale).
- **UNDECIDED**: otherwise.
Sums are over the matched clusters of the selection (need_PS for the same clusters).

## 6. Checks (each prints `K# PASS|FAIL value threshold`; script ends `X21 COMPLETE: n/m checks PASS.`; exit 0 iff all pass)

- **K0:** step-0 S0-a (≤ 1e-9) and S0-c (≤ 1e-6).
- **K1:** catalogue join: eRASS1 MGAS500 by NAME equals the npz Mgas500 (rel ≤ 1e-12), and the CFG922 match has |Δz| ≤ 1e-3.
- **K2:** synthetic plants with the real d_i (noiseless n_i = a(x_i) d_i): a step plant (1 + 0.8 H) is recovered by (b) and (d)
  to ≤ 1e-9 with b = 0; a linear plant (1.3 + 0.4 x) by (a) and (d) to ≤ 1e-9 with c = 0.
- **K3:** the λ solver: at the solved λ the selection's model sum equals Σ n to ≤ 1e-4 relative; λ = 0 reproduces C\* exactly.
- **K4:** peak RSS < 1 GB.
- S0-b is reported as a line, not a check.

**MUTATE twin** (`X21_MUTATE=1`; outputs `_MUTATE`): the cluster labels (every catalogue variable, MGAS500 included) are shuffled
across clusters with a fixed seed before anything else. **K0 and K1 must FAIL**, and the script must exit 1.

## 7. Run

`OMP_NUM_THREADS=1 nice -n 15`, one thread, < 1 GB, minutes. No downloads, no KiDS re-read, nothing in `compute_queue/`.
Commit by pathspec; never push.
