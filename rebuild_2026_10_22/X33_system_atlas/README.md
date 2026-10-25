# X33_system_atlas: one per-object table of every system measured against the galaxy law, and what the misfits share

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (committed alone first). `AMENDMENT_A1.md` is POST-RESULT: S0c
fired the stop rule on an estimator mismatch, and the check code was changed before any finding was computed. κ = ½ FITTED.
Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled. No dark-matter particle. Not "theory closed". Nothing here says the
data favour the framework. This lane is descriptive: no constant is fitted and no verdict of another lane is changed.

Every number below comes from `x33_system_atlas.out`, `x33_findings.json` or `x33_atlas.csv`.

## The atlas

`x33_atlas.csv` has 677 rows and 0.29 MB. The columns are the frozen schema plus diagnostics. The residual axis is
"extra over the isolated law, dex in g", where positive means more acceleration than the baryons give under the law.

| class | N | residual source | axis |
|---|---|---|---|
| SPARC | 175 (68 small / 107 large; UMa members flagged) | median along the curve at the record's global Υ (CFG695) | exact |
| MW disc | 1 | P4 K_z(R₀) | approximate |
| Groups | 63 | P4's estimator, 2 × Δlog σ | approximate |
| Clusters | 326 (241 with A > 0 on canonical) | per-cluster X7/X21 MID-band lensing ratio | approximate, noisy |
| LG dwarfs | 89 | X1 iso Δ (EFE column alongside) | exact |
| Coma UDGs | 9 | S1 | exact |
| TDGs | 6 | X19 estimator | exact |
| DF2/DF4 | 2 | X19 estimator | exact |
| SLUGGS centrals | 4 | S4 R4 ν₁, no ownership, 2 × Δlog σ | approximate |
| Lens stacks | 2 | S2 | approximate; population stacks, never in object statistics |

## Step 0 (stop rule): all reproduced

- **S0a SPARC rms.** The per-galaxy-Υ rms is 0.05409 / 0.05372 against P4's isolated 0.05409 / 0.05372. P4's L★ 24 pc
  values are 0.05398 / 0.05351.
- **S0b SPARC small / large.** Counts are 68 / 107 on both footings. Means on the global-Υ isolated algebra are −0.0482 and
  −0.0475 against P4's −0.0456 and −0.0469 (canonical), within the declared 0.010.
- **S0c X1 class values (A1).** X1's JSON matches its printed digits. Reported only: the plain per-object medians sit
  0.01–0.05 dex below X1's class values. M31 others is the exception, +0.14 / +0.11 dex above. The cause is X1's estimator,
  which includes the Monte-Carlo draws.
- **S0d X21 KT terciles.** A = 1.0963 / 1.6504 / 2.1323 (canonical) and 1.0041 / 1.5133 / 1.9590 (alt), exact.
- **S0e P4 groups.** +0.010028 / −0.010269.
- **S0f P4 TDGs and DF2/DF4.** −0.6911 / −0.7282 and −1.9405 / −2.0284 ln.
- **S0g S1 Coma.** +0.32490 / +0.28546.

## Where the law is right (|resid| ≤ 0.05 dex)

**By class, as fraction law-right (canonical / alt) and median residual:**

| class | fraction law-right | median residual |
|---|---|---|
| SPARC | 0.29 / 0.27 | −0.039 / −0.052 |
| Groups | 0.06 / 0.10 | +0.071 / +0.030; 84 % within 2σ |
| LG dwarfs | 0.09 / 0.07 | +0.30 / +0.27 |
| Clusters | 0.05 / 0.06 | +0.37 / +0.34 (this per-object median is biased high, see Clusters below) |
| TDGs, DF2/DF4, SLUGGS, Coma UDGs | 0 (except 1 Coma galaxy on alt) | |
| MW disc | 0 | −0.143 / −0.164 |

**The law-right set is mostly SPARC.** In P_gal it holds 51 SPARC, 8 LG dwarfs and 4 groups on canonical, and 47 / 6 / 6
plus 1 Coma galaxy on alt. Its 10–90 % ranges in P_gal (canonical) are:
- log M_b 8.5–11.2, against 5.0–11.7 for all objects;
- log R_char −0.17 to 0.97 kpc;
- log Σ_half 0.5–3.0 M☉ pc⁻²;
- log x 10^−2.1 to 10^−0.7;
- log e_ext −1.6 to −1.2.

**Binned (P_gal).** The law-right fraction is about 0.30 in the upper two quartiles of Σ_half and of x. It is 0.05–0.09 in
the lower two. The median residual is +0.17 / +0.17 dex in the two lowest Σ_half quartiles and −0.02 / −0.04 in the two
highest (canonical). The low-Σ, low-x end is dominated by LG dwarfs, so this is largely a class contrast.

**In plain words.** The law is closest to right for massive (M_b ≳ 3e8 M☉), kpc-sized, rotation-supported discs of moderate
or high surface density, in weak external fields. Even there, only about 30 % of SPARC galaxies sit within ±0.05 dex at
one global Υ.

## What the misfits share (FDR-surviving; BH threshold p ≈ 0.020 / 0.021 over 284 / 285 tests per footing)

**The pooled raw correlations are class composition.** The MUTATE twin shuffles residuals within each class. It keeps 15
pooled raw correlations FDR-significant on each footing (for example P_gal M★, x and Σ_half, and P_all f_gas), and zero
within-class ones. So pooled correlations without centring describe which classes sit where, not a trend inside any class.
Only the within-class and class-centred results below are trends.

**Within class (both footings unless noted; ρ ± bootstrap):**

- **LG dwarfs (89).** The residual rises as the system gets fainter, smaller and more diffuse:
  - log M★: ρ −0.65 ± 0.06 (Bonferroni);
  - log r_h: −0.64 / −0.63 (Bonferroni);
  - log Σ_half and log x: −0.43 (Bonferroni);
  - e_ext: +0.32 / +0.33 (stronger host field, more extra).

  Inside the MW ultra-faints, log M★ gives −0.45 / −0.47. The "above" dwarfs (resid > +0.2: 54 / 50) are fainter (median
  log M★ 4.6 / 4.3 against 7.0 / 7.5 for the law-right ones), smaller and more often hosted.
  - Caveat: the residual is built from M and r, so mass and size errors push the correlation negative. The size of that
    effect is not computed here.
- **SPARC small (68).** The residual rises with surface density: log Σ₀ +0.44 / +0.46 and log Σ_half +0.42. It also rises
  with R_last (+0.35 / +0.34) and falls with type T (−0.30 / −0.32).
- **SPARC large (68 with an environment).** The residual falls in stronger external fields: log e_ext −0.46 / −0.44
  (canonical Bonferroni). Over all of SPARC, alt gives −0.23 (FDR).
- **SPARC, all (alt only).** log Σ₀ +0.20; the class-centred pool gives the same.
- **SPARC data quality (flagged systematic).** Q: ρ −0.40 / −0.42 (Bonferroni), so lower-quality curves sit lower.
- **SPARC "below" galaxies (resid < −0.2: 25 / 27).** Against the law-right SPARC galaxies they are:
  - later type: median T 10 against 6;
  - lower Σ₀: log 1.75 against 2.48 / 2.53;
  - smaller: R_last log 0.73 against 1.21;
  - lighter: log M_b 9.24 against 10.0;
  - more gas-rich: f_gas 0.59 against 0.39;
  - lower quality: Q 2 against 1.

  These are gas-rich, low-surface-brightness late-type dwarfs.
- **Groups (63).** The residual rises with log Σ_half (+0.45) and log x (+0.37). Its correlation with σ (+0.90) shares the
  observable, so it is not a finding.
- **Clusters (312 ranked on A_i).** Weak positive correlations with R500 (+0.14) and L500 (+0.14), and with MGAS500 on alt
  only (+0.13). KT is not significant per object (ρ +0.09, p 0.36). X21's stacked KT trend needs the stack weights.
- **Correlations that share the observable.** V or σ against the residual (for example MW ultra-faints +0.81, Coma +0.82)
  are listed in the JSON with this flag and are never used as findings.

## Outlier highlights (worst 5 % by |resid|, canonical)

- **SPARC.** CamB −0.83 (Z −13.8), UGC02455 −0.74, F574-2 −0.69, UGC07577 −0.68, PGC51017 −0.66, F563-V1 −0.62. All are
  low-mass late types sitting below the law at the global Υ.
- **Groups.** NGC4993 −0.98 (Z −1.5) and NGC3311 +0.64 (Z +14.2).
- **LG dwarfs.** Carina III +1.34, Segue 1 +1.25 (Z 5.7), Willman 1 +1.22, Andromeda XXVII +1.22, Eridanus IV +1.18 (Z 7.7).
- **Coma.** J130005.40+275333.0 +0.80.
- **TDGs and DF.** NGC7252NW −0.89 and DF4 −0.94.
- **SLUGGS.** NGC5846 +0.30 (Z 6.6).
- **Lens stacks.** The red stack is +0.118 (Z 5.7); the blue stack is −0.096 on alt.
- **Clusters.** The cluster outliers are shape-noise artefacts (|Z| ≈ 0.1), not physical.

## Clusters, read carefully

Single-cluster lensing ratios are noisy, with shape-noise error only. On canonical, 85 of 326 have A ≤ 0 and no log
residual. Their per-object median (+0.37) is biased upward by that cut. The class level is X7/X21's stacked A
(1.10 / 1.65 / 2.13 in KT terciles, reproduced in S0d), not this median.

## Checks

| check | normal | MUTATE |
|---|---|---|
| S0a–S0g | PASS | PASS (by construction) |
| K_rows | PASS | PASS |
| K_size | PASS | — |
| K_ident (16 named rows equal their sources) | PASS | **FAIL** (2/16) |
| K_plant (planted ρ with log Σ₀ in SPARC: +0.64 / +0.68, p 3e-21 / 1e-24) | PASS | **FAIL** (ρ −0.02, p 0.77) |
| K_null (FDR-surviving within-class correlations) | 16 / 21 | 0 / 0 |

Normal run: 11/11 checks PASS, exit 0. MUTATE: 8/10, exit 1, as required. Runtime 27 s, RSS 0.29 GB.

## Limits

- The MW, groups, clusters and SLUGGS axes are approximate.
- The SPARC residual uses one global Υ and the isolated algebraic law, with no disc solve (P4 D1 gives up to −0.10 dex at
  the lowest Σ₀).
- Groups have no external field on disk.
- The binary hosted flag is excluded from Spearman (fewer than 3 distinct values) and enters only the Mann–Whitney tests.
- Correlations are descriptive. This does not overrule X19 (no low-dimensional selector).

## Reproduce

`PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x33_system_atlas.py` (add `X33_MUTATE=1` for the twin).
