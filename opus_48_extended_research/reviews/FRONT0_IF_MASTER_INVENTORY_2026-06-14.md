# Front 0 — the interpolation-function master inventory (2026-06-14)

*Grep + classify EVERY interpolation function (IF) in `real_research/` + `opus_48_extended_research/`. For each: the
formula, its CLASSIFICATION, what it is LABELED, the front it feeds, and whether it is LOAD-BEARING (transition/EFE
regime, IF matters) or DEEP-MOND-ONLY (IF-irrelevant). This is the map the other fronts regrade against.*

The framework's OWN IF is **dS-Unruh / Unruh-MOND**: `g_obs = sqrt(g_N^2 + g_N a0)`  <=>  `nu(y)=sqrt(1+1/y)`,
y=g_N/a0. Distinct from normal-MOND: simple-mu `nu=1/2+sqrt(1/4+1/y)`; standard-mu/F4 `nu=sqrt(1/2+1/2 sqrt(1+4/y^2))`;
McGaugh-RAR `nu=1/(1-exp(-sqrt(y)))`; AQUAL/QUMOND field eqs.

## Quantified IF spread (the triage key)

`nu_simple/nu_dsU` g_obs ratio: +0.5% (y=100), +4.1% (y=10), **+9.4% (y=3, EFE op-pt)**, **+14.4% (y=1)**, +15.5%
(y=0.5), +11.6% (y=0.1), +4.6% (y=0.01). Deep-MOND nu*y/sqrt(y): dSU 1.005 / simple 1.051 (y=1e-2) -> both ->1.000
by y=1e-4. **So: IF is load-bearing in TRANSITION (y~0.3-3) and EFE (y_ext~1.7-2.2); IF-robust (<1%) by y<1e-3.**
Verified: BTFR V^4=GMa0 IF-robust to <1% at flat-curve outer points (y<1e-3); deep-dSph sigma~(Ma0)^{1/4} likewise.

---

## Inventory by IF family (counts: simple 56, dS-Unruh 77, standard/F4 8, McGaugh 27 raw hits)

### A. simple-mu `nu=0.5+sqrt(0.25+1/y)`  (= mu=x/(1+x)) — the normal-MOND IF most often standing in for framework

| file:line | labeled as | front | load-bearing? |
|---|---|---|---|
| `real_research/efe_clinch_framework.py:95-96` | **"framework, EFE_paper.tex Eq.62"** | EFE clinch Method (b) | **EFE — but verdict UNCHANGED** (banked dS-Unruh re-run r=+0.218->+0.213, still null) |
| `real_research/reviews/widebinary_chae2601_confront.py:45` | **"framework ... simple-mu pure-EFE cap"** | wide-binary vs Chae 2026 (LIVE, uncommitted) | **EFE — LOAD-BEARING, MOVES** (see recompute) |
| `real_research/reviews/widebinary_saadting_2603_confront.py:39` | framework band (simple = upper edge) | wide-binary vs Saad-Ting 2026 (LIVE) | **EFE — band over-wide** (see recompute) |
| `real_research/predictions/door4_ultraprecision.py:66-68` | **"framework a0, simple-mu" HEADLINE scatter** | paper RAR/MDAR scatter 0.195 dex | **transition — LOAD-BEARING under weighting** |
| `real_research/predictions/door6_galaxy_clusters.py:94-96` | the cluster eta IF | SCORECARD ROW 17 (eta) | **transition (y_med=0.48) — LOAD-BEARING** |
| `real_research/predictions/door1_gravitational_lensing.py:36,107` | **"framework lensing RAR"** | KiDS lensing-RAR pass | transition — mild (deep-MOND boost) |
| `real_research/predictions/predictions_catalog.py:28`, `door4_mdar_evolution.py:36` | framework prediction | catalog / MDAR-z | transition |
| `real_research/reviews/project_efe_check.py:23`, `project_decision_matrix.py:18` | "simple" | EFE checks | EFE |
| `real_research/reviews/clusters_eta_audit.py:22`, `precision_rar_test.py:89`, `redteam_rar_framework_a0.py:108` | "simple" (one of several) | cluster/RAR audits | transition |
| `real_research/reviews/aest_*`, `toe_law/agent*_*` (~20 files, `nu_simple`) | "simple" (one rung of an IF ladder) | DSSYK/AEST gauntlets | mixed — run alongside dS-Unruh |
| **`opus_48_extended_research/reviews/HOSTILE_RECHECK_baryon_budget.py:50`** | **"framework dSU/simple" (CONFLATION)** | cluster baryon-budget regrade | **transition — mislabels simple AS dSU** |
| `opus_48_extended_research/reviews/{cluster_eta_independent_regrade,mi_vs_aqual_route2,no_extra_mass_steelman,...}.py` | "simple-mu" (correctly, alongside dS-Unruh) | cluster/MI regrades | transition — CLEAN (both shown) |

### B. dS-Unruh / framework canon `sqrt(g^2+g a0)` or `nu=sqrt(1+1/y)` — the CORRECT framework IF

| file:line | labeled | front |
|---|---|---|
| `real_research/rar_framework_a0_mlfit.py:22`, `framework_a0_law_of_nature.py:51`, `coefficient_posit_attack.py:229`, `clusters_framework_a0.py:68`, `sparc_efe_real_externalfield.py:33`, `sparc_efe_per_galaxy_environment.py:21` | "framework emergent/MI shape" | RAR / coeff / clusters / EFE (in-house) |
| `real_research/rar_emergent_discriminate.py:35`, `reviews/desitter_unruh_RAR_test.py:38`, `predicted_a0_rar_consistency.py:49`, `modified_inertia_pressure_test.py:53` | "de Sitter-Unruh DERIVED" | RAR-shape discriminators |
| `real_research/reviews/efe_vs_z_recompute.py:26`, `efe_declining.py:28`, `clusters_eta_audit.py:28` | framework | EFE-vs-z / clusters |
| `real_research/reviews/toe_law/{agentDD,agentY,agentKK,agentN5,agentW,agentBB,mi_f4_*}` `nu_fw`, `agentJ_massbin_phase.py:162`, `public_data/agentGG_jwst_highz.py:103` | "framework nu sqrt(1+1/y)" | DSSYK gauntlets / JWST |
| `opus_48_extended_research/reviews/{efe_clinch_framework_dsunruh,mi_vs_aqual_*,density_a0_*,HOSTILE_r*,cluster_*,AUDIT_rar_*}.py` | dS-Unruh (the audit-grade corrections) | EFE/RAR/cluster regrades |

### C. standard-mu / F4 `nu=sqrt(0.5+sqrt(0.25+1/y^2))` (= mu=x/sqrt(1+x^2))

| file:line | labeled | front | note |
|---|---|---|---|
| `real_research/reviews/widebinary_saadting_2603_confront.py:40` | **"framework's DSSYK-sharp interp"** | wide-binary vs Saad-Ting | **mislabel — standard-mu is NOT the framework IF**; it is the LOWER cap edge (1.04) |
| `real_research/reviews/widebinary_chae2601_confront.py:46` | (lower edge) | wide-binary vs Chae | lower cap edge |
| `real_research/reviews/clusters_eta_audit.py:24`, `cluster_eta_independent_regrade.py:69`, `HOSTILE_RECHECK_baryon_budget.py:51` | "standard" (alongside others) | cluster ladders | clean |
| `real_research/reviews/scaling_mond_action.py:48`, `radion_mond_bridge.py:53` | **"AQUAL interpolation"** | radion/scaling theory-bridge | theory derivation, NOT a data verdict |
| `real_research/reviews/toe_law/agentG_lab_bridge.py:40`, `mi_f4_*` | F4 / standard | gauntlets | clean |

### D. McGaugh-RAR `nu=1/(1-exp(-sqrt(y)))` — the actual SPARC-fit g-dagger function

`door4_ultraprecision.py:74`, `clusters_eta_audit.py:26`, `project_efe_sparc_test.py:41`, `project_cluster_a0z_xray.py:34`,
`project_erass1_cluster_a0_fork.py:78`, `cmb_modinertia_oscillator.py:430`, `cassini_quadrupole_framework.py:28`, and
~14 `toe_law/agent*` files (`nu_rar`/`nu_mcg`). Always labeled "McGaugh/RAR" (correctly) and used as a cross-check
shape, never standing in AS the framework. CLEAN.

### E. AQUAL / QUMOND field-equation realizations
`scaling_mond_action.py`, `radion_mond_bridge.py` (mu=x/sqrt(1+x^2) solved via Poisson); `efe_forecast_figures.py` +
`efe_evolution_forecast.py` (`mu=x/(1+x)` QUMOND EFE solve, **a0=1.2e-10**). Theory-bridge / forecast-figure scripts.

---

## The contamination map (normal-MOND IF labeled as / standing in for framework dS-Unruh)

**LOAD-BEARING (transition/EFE — IF moves or distorts the number):**
1. `widebinary_chae2601_confront.py:45` — simple-mu cap **1.247** labeled framework; dS-Unruh cap **1.142**. MOVES the
   gap to measured 1.600 from -2.3sig -> -3.0sig (correcting makes it WORSE — clean retraction, same as commit 6d2dc02e).
2. `widebinary_saadting_2603_confront.py:39-40` — band [1.04 (standard-mu, mislabeled "DSSYK-sharp"), 1.30 (simple-mu)]
   BRACKETS but does not equal the framework dS-Unruh cap 1.142/1.179. Upper edge OVERSTATES; true value vs Saad-Ting
   DE-projection (1.56) is FURTHER (more tension).
3. `door4_ultraprecision.py:66` — HEADLINE RAR scatter 0.195 dex computed on simple-mu. On dS-Unruh: 0.2018 dex at
   framework a0; a0-optimum and weighted penalty differ materially (below).
4. `door6_galaxy_clusters.py:96` — cluster eta on simple-mu; transition regime (y_med=0.48). dS-Unruh eta is HIGHER
   (2.334 vs simple 2.149 median; see cluster_eta_independent_regrade). Compounds the published row-17 fix.
5. `HOSTILE_RECHECK_baryon_budget.py:50` + `ell_desitter_unruh_horizon.py:280` — simple-mu **commented "= dS-Unruh"**
   (false equivalence). Benign ONLY if cluster is deep-MOND; it is TRANSITION (y=0.48), so the conflation hides a
   ~13-15% eta shift.

**NON-LOAD-BEARING (deep-MOND — IF-irrelevant, named for completeness):**
- `efe_clinch_framework.py:95` simple-mu labeled "Eq.62" — but banked dS-Unruh re-run leaves verdict UNCHANGED
  (r=+0.218 p=0.148 -> r=+0.213 p=0.211; Method (a) already used dS-Unruh).
- BTFR (`mond_first_principles.py`, `framework_a0_law_of_nature.py`), dwarf sigma (`door2_dwarf_spheroidals.py`),
  early-galaxy density — all deep-MOND sqrt(GMa0), IF-robust to <1% (verified).
- a0(z) bridge (`efe_vs_z_recompute.py` ratio, `efe_forecast` growth ratio) — IF CANCELS in the differential
  (growth ratio a0-invariant; though the absolute offset is IF-dependent, it is small ~0.06 dex at z=0).

## RAR a0-optimum across IF x M/L x weighting (the load-bearing both-ways grid)

| cell | dS-Unruh(FW) a0_opt / penalty@9.355 | simple-mu | McGaugh |
|---|---|---|---|
| Y=0.50 unweighted | 1.207e-10 / +2.28% | 0.926e-10 / +0.00% | 0.947e-10 / +0.01% |
| Y=0.50 err-weighted | 1.744e-10 / **+38.7%** | 1.297e-10 / +12.2% | 1.335e-10 / +14.7% |
| Y=0.70 unweighted | 0.858e-10 / +0.25% | 0.628e-10 / +4.42% | 0.649e-10 / +3.93% |
| Y=0.70 err-weighted | 1.203e-10 / +6.47% | 0.858e-10 / +0.75% | 0.892e-10 / +0.25% |

On the framework's OWN dS-Unruh IF, UNWEIGHTED, the optimum BRACKETS 9.355e-11 (0.858e-10 at Y=0.70 .. 1.207e-10 at
Y=0.50), penalty <=2.3% — convention-COMPATIBLE, NON-diagnostic, consistent with the MEMORY rule. The IF is most
load-bearing under ERROR-WEIGHTING: dS-Unruh's softer high-g knee pushes its weighted optimum UP (1.2-1.74e-10),
penalty up to 38% at Y=0.50 — because weighting upweights the high-y points where dS-Unruh and simple-mu diverge most.
**agentW banked, best-Upsilon-per-IF unweighted: framework sqrt(1+1/y)=0.1969, simple=0.1951, McGaugh=0.1950,
F4=0.1984 — all within 0.0034 dex. Unweighted RAR is IF-non-diagnostic; weighting is where the IF bites.**

## Bottom line for the regrade

The contamination is REAL and present in MULTIPLE scripts; its load-bearingness VARIES exactly as the physics
predicts. Wide-binary caps (chae/saadting) are the clearest LOAD-BEARING contamination — correcting to dS-Unruh moves
the cap DOWN (1.247->1.142), WORSENING the gap to the measured anomaly (no manufactured win). The EFE clinch and all
deep-MOND fronts (BTFR/dSph) are IF-robust. door4/door6/lensing carry simple-mu labeled framework in the
transition regime — load-bearing at the ~5-15% level, to be regraded by the cluster + RAR fronts. Two scripts
literally comment "simple = dS-Unruh" — a false equivalence to flag.
