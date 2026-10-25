# X33_system_atlas: frozen criteria (committed alone with ASSUMPTION_LEDGER.md, before any script or number)

κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt a₀ = 1.1312e-10 m s⁻², never pooled. No dark-matter particle.
Not "theory closed". Nothing here may say the data favour the framework.

## 0. What this lane is

A descriptive atlas. It builds one per-object table of every system the record has measured against the galaxy law
(isolated AQUAL, μ = x/(1+x), ν₁(y) = (1 + √(1 + 4/y))/2), then asks, from the data alone, where the law is right and what
the misfits share. It is NOT a new theory test. No constant is fitted, no knob is scanned, and no class verdict of any other
lane is changed. Every residual is either read from a committed record output or recomputed by the record's own estimator
from the record's own inputs; step 0 shows the recomputation reproduces the record.

Lane directory: `rebuild_2026_10_22/X33_system_atlas/`. Script `x33_system_atlas.py`. Outputs `x33_atlas.csv`,
`x33_findings.json`, `x33_system_atlas.out`; MUTATE twin `X33_MUTATE=1` → `x33_findings_MUTATE.json`,
`x33_system_atlas_MUTATE.out` (no MUTATE atlas CSV).

## 1. Unified schema (one row per object; NaN where unavailable)

Minimum columns, in this order:

`id, class, subclass, morphology_T, M_b, M_star, M_gas, f_gas, R_char_kpc, R_last_kpc, Sigma0, V_char_kms, sigma_kms, x_char,
e_ext, hosted, z, resid_dex_can, resid_err_can, resid_dex_alt, resid_err_alt, quality, source`

Extra columns (after these): `morph_label, Sigma_half, D_Mpc, inc_deg, L36, M_HI, R_eff_kpc, R_disk_kpc, V_flat_kms, Q,
Ups_fit_can, Ups_fit_alt, resid_perU_med_can, resid_perU_med_alt, rms_curve_can, rms_curve_alt, resid_wmean_can,
resid_wmean_alt, resid_efe_can, resid_efe_alt, KT_keV, MGAS500, L500, R500_kpc, uma_member, in_pool`.

Units: masses M☉; radii kpc; Sigma0 and Sigma_half M☉ pc⁻²; velocities km s⁻¹; x_char = g_N,bar/a₀ and e_ext = g_e/a₀
on the canonical footing (properties are footing-independent descriptors; residuals carry both footings).

Definitions used for every class unless §2 says otherwise:
- M_b = M_star + M_gas; f_gas = M_gas / M_b.
- Sigma_half = M_b / (2π R_char²) (mean baryonic surface density inside the half-mass radius proxy R_char).
- Sigma0: SPARC = Υ★ × SB_disk (central disc surface density from the 3.6 µm disc fit); every other class = Sigma_half.
- sigma_kms is the measured 1-D dispersion where the system is dispersion-supported; V_char_kms = V_flat (SPARC),
  V_circ (TDGs), else √3 σ.

Classes (subclass in brackets): `SPARC` (small / large by M_b ≤ 3e9 M☉ at the global Υ, as X19; `uma_member` flag),
`MW disc`, `Groups`, `Clusters` (T1 / T2 / T3 by X7's MGAS500 tercile bounds), `LG dwarfs` (X1's `cls` label, e.g. MW
ultra-faint), `Coma UDGs`, `TDGs`, `DF2/DF4`, `SLUGGS centrals`, `Lens stacks` (blue / red; population stacks, not objects).

## 2. Residual per class → common axis "extra over the law, dex in g" (primary baseline: the isolated law, B_iso)

| class | residual (dex) | error | mapping to dex in g | EFE-baseline column |
|---|---|---|---|---|
| SPARC | median along the curve of log₁₀(g_obs / g_law(g_bar)), g_bar at the record's global Υ (CFG695 U₀ per footing: Υ_disc, 1.4 Υ bulge), isolated algebraic ν₁ | √(σ_stat² + s²): σ_stat = 1/√Σ(1/σ_i²), σ_i = 2 eV/(V ln10); s² = P4's distance + inclination offset variance | exact (same quantity) | none (EFE moves P4's rms < 0.001 dex) |
| SPARC (extra) | at P4's per-galaxy Υ (L★ 24 pc row, `U_rms`): median and rms along the curve, isolated algebraic | — | exact | — |
| MW disc | log₁₀(66.4 / K_z,1.1(R₀)), P4 T4 B1_McMillan17 F0\|L24 | 2.2/(66.4 ln10) | **APPROXIMATE**: vertical force, not g_R | none |
| Groups | 2 × [log σ_obs − log σ_law] (P4's group_logsig, ν₁, Hernquist, whole system) | 2 × e_logσ (Tian+26 column) | **APPROXIMATE** (σ² ∝ g at fixed radius; the virial weighting differs) | none |
| Clusters | log₁₀ A_i, A_i = n_i / d_i per cluster in X7's MID band, CAL numerator, C\* model, h 0.672 (X21's arrays) | shape noise only: √(Σ_band W B²) / d_i, divided by (A_i ln10) | **APPROXIMATE** (lensing ΔΣ data/law ratio ≈ mass ratio ≈ g ratio in the band); NaN when A_i ≤ 0 | none |
| LG dwarfs | X1 `Delta[iso AQUAL L*0]` | X1 `sdMC[...]` | exact (X1's E is dex in g) | X1 `Delta[AQUAL + EFE L*0 ...]` |
| Coma UDGs | S1 `coma[f|S2 AQUAL isolated L*0 E-W].per` E / ln10 | sE / ln10 | exact | S1 `S3 AQUAL + EFE dmean L*0 E-W` |
| TDGs | log₁₀[(V²/R) / g_law(GM_bar/R²)] at R_out (Lelli+15; X19's K1 estimator) | P4 T5 L0 T_points `s` | exact | P4 T5 L24 T_points `r` |
| DF2/DF4 | 2 ln(σ / σ_law) / ln10, r½ = 4/3 R_e, half the stellar mass (X19's K1 estimator) | P4 T5 L0 U_points `s` / ln10 | exact | P4 T5 L24 U_points `r` / ln10 |
| SLUGGS centrals | 2 × CFG528b offset (log σ_obs/σ_pred), v3 kernel ν₁ without ownership, row "J joint best case" (S4 R4 `nu1_noown`) | 2 × offset / Z | **APPROXIMATE** (log σ → log g by × 2) | none |
| Lens stacks | log₁₀ A, S2 ladder L4 (v3 at y_e = 0) | sA / (A ln10) | **APPROXIMATE**; stacks, never in per-object statistics | S2 L5 (primary y_e) |

Sign: positive = the system shows more acceleration than the law gives from its baryons ("extra"); negative = less.

**Pool sets.** P_gal = SPARC, Groups, LG dwarfs, Coma UDGs, TDGs, DF2/DF4, SLUGGS centrals (dynamical residuals,
mapping exact or ×2). P_all = P_gal + Clusters. MW disc (single, K_z) and Lens stacks are never pooled. Footings are never pooled.

## 3. Property list (analysed in log₁₀ where positive; `hosted`, `morphology_T`, `Q`, `uma_member` linear)

log M_b, log M_star, f_gas, log R_char, log Sigma_half, log Sigma0, log V_char, log σ, log x_char, log e_ext, hosted, z,
morphology_T (SPARC only), and SPARC-only diagnostics D_Mpc, inc_deg, Q, R_last. Clusters also KT, MGAS500, L500, z.
**By construction, never graded:** Ups_fit (chosen by minimising the residual), rms_curve, and anything built from
σ_obs or V_obs against a residual built from the same σ_obs or V_obs: V_char and σ are reported for every class and
FLAGGED "shares the observable" in the table; they never enter the "misfits share" statement.

## 4. Analysis plan (both footings separately)

(a) **Spearman** ρ between the residual and each property, within each class with N ≥ 8 finite pairs, and within P_gal and
P_all. Error: bootstrap 1000 resamples (seed fixed, PYTHONHASHSEED = 0), 16–84 % half-width. p from the Spearman
t-approximation. Within-class subclasses with N ≥ 20 (SPARC small / large, LG MW ultra-faint, bright M31) also reported.
Pooled ρ also reported with the class median subtracted from each residual ("within-class pooled"), so between-class offsets
cannot drive it.

(b) **Binned residual.** Medians (bootstrap 16–84 %) in quartile bins of morphology T (SPARC: T 0–3, 4–6, 7–8, 9–11),
Sigma0, f_gas, R_char, V_char and x_char, per class with N ≥ 20 and for P_gal and P_all; edges are the pooled set's
quartiles.

(c) **Outliers.** The worst 5 % by |residual| in each class (at least 1 per class with N ≥ 2), canonical and alt, each with
its properties and its Z = resid/err.

(d) **Where the law is right.** Law-right objects: |resid| ≤ 0.05 dex. Per class: the fraction law-right (bootstrap error).
Per property (P_gal and P_all): the 10–90 % range of the law-right objects, and the fraction law-right in each quartile bin.
**What misfits share:** "above" (resid > +0.2 dex) and "below" (resid < −0.2 dex) objects against the law-right set, per
property, by Mann–Whitney U (two-sided), P_gal and P_all, and within SPARC and LG dwarfs.

**Trials.** Every p-value of (a) and (d) enters one family per footing. Benjamini–Hochberg FDR at q = 0.05 is the primary
significance; Bonferroni at α = 0.05 is reported beside it. Only FDR-surviving results may be called "significant" in the
README; the rest are "not significant after trials". The same rule applies to MUTATE.

## 5. Step 0 (stop rule: if any of S0a–S0g fails, write the atlas and the .out, write no findings, exit 1)

- **S0a** SPARC: my per-galaxy-Υ isolated algebraic pooled rms equals P4 `T1.footings.f.iso_perUps.rms` within 1e-4, and
  P4's L★ 24 pc rms (0.054 / 0.054) within 0.001, both footings; N = 175.
- **S0b** SPARC small / large counts equal P4 `classes_global_U` N exactly; the class weighted-mean residuals at the
  global Υ (isolated algebraic) are within 0.010 dex of P4's (which includes the solved EFE; declared approximation).
- **S0c** LG dwarfs: plain class medians of X1's iso Delta equal X1's printed `.out` class values within 0.03 (X19's K1
  rule), for the 7 X19 classes, both footings.
- **S0d** Clusters: X21's KT-tercile A (canonical h0672, alt h0672) reproduced from my per-cluster (n_i, d_i) within 1e-9;
  N with KT > 0 = 106; tercile n = 35 / 35 / 36.
- **S0e** Groups: per-group mean of log σ_obs − log σ_law equals P4 `T3.footings.f.v3_isolated.mean` within 1e-6; N = 63.
- **S0f** TDG and DF2/DF4 means equal P4 `T_law_isolated.rbar` and `U_law_isolated.rbar` within 1e-3.
- **S0g** Coma: mean of my per-galaxy dex equals S1 `meanE_dex` within 1e-9.

## 6. Other checks

- **K_rows**: counts per class: SPARC 175, MW disc 1, Groups 63, Clusters 326, LG dwarfs = X1 CSV rows per footing, Coma 9,
  TDGs 6, DF2/DF4 2, SLUGGS 4, Lens stacks 2.
- **K_size**: `x33_atlas.csv` < 2 MB.
- **K_ident** (MUTATE must FAIL): eight named rows equal their source values within 1e-9 (CamB SPARC per-galaxy-Υ
  weighted mean vs P4 `wmean`; Crater II, Antlia II, Bootes I iso Delta vs X1 CSV; DF2 vs P4 U_points; NGC5291N vs P4
  T_points; DFX1 vs S1 per; NGC4486 vs CFG528b), both footings.
- **K_plant** (positive control; MUTATE must FAIL): a planted column resid + 0.10 × standardised log Sigma0 (SPARC only)
  is added BEFORE the MUTATE shuffle; its SPARC Spearman with log Sigma0 must survive the FDR within the family, both
  footings. The planted column is never reported as a finding.
- **K_null**: the MUTATE run's FDR-surviving within-class count is reported (expected ≈ 0); normal run's count reported.

## 7. MUTATE (`X33_MUTATE=1`)

After step 0 and the plant, every residual column (primary, EFE, per-Υ, planted) is permuted within each class (seed fixed,
one permutation per class shared by both footings). The analysis then runs unchanged. K_ident and K_plant must FAIL (exit
1). Step 0 is unaffected by construction (it reads the sources, and within-class shuffles keep class medians).

## 8. Reporting

README numbers come only from `x33_findings.json` / `.out` / `x33_atlas.csv`. Correlations are descriptive: no causal
reading, no claim that any property "selects" the cold-mass amount (X19 found no low-dimensional selector; this lane does
not overrule it). Class-level residual offsets on approximate axes (§2) are quoted with their mapping flag.
