# DR4MAP: every registered Gaia DR4 prediction, which rule scores it, and what is still open

Read-only audit, 2026-11-12. Gaia DR4 is due 2026-12-02 (ESA, provisional). Nothing was run: no scorer, no self-test,
no fetch. No frozen file was edited. Dates are first-commit dates from `git log --diff-filter=A` unless marked "in text".
Hashes of the frozen inputs were read with `shasum` only. This file decides nothing that is the owner's to decide; where
two registered values conflict it lays out both readings. kappa = 1/2 FITTED; footings never pooled; not theory closed.
Nothing here says the data favour the framework.

## 0. Summary

- **Items found: 32 registered or sealed DR4 entries**: 22 wide-binary (P0-P9, S1-S12), 9 Milky Way / vertical (M1-M9)
  and the void s^TX dipole (P10). Several are the same claim registered twice; the count is of entries, not of
  independent claims. Two of the 22 (S10, S12) are not registrations by their own record.
- **Governing for the adopted theory (wide binaries only):** CQ2's sealed prediction (v3s = Newton), scored by the D2 fork
  rows under owner decision D1 (a) of 2026-11-05, plus the R rule, with D7/D8 (2026-11-05b) and the seed-mean NSS-off
  entry (2026-11-05c, filed 2026-11-08). Quoted in section 2.
- **Milky Way rows (vertical structure, local density, Oort constants, K_z):** no registration exists for the adopted
  theory. The seals that exist belong to retired or non-adopted forms, none has a scorer for DR4 data, and every one needs
  a third-party Jeans or kinematic analysis that will not exist on 2026-12-02.
- **15 conflicts or gaps need an owner decision or a pre-data fix before 2026-12-02** (section 4). Four bear directly on
  the headline label: C1 (do the frozen stability requirements gate "v3s EXCLUDED"?), C3 (the filed seed-mean entry is not
  wired into the release-day script), C4 (CFG816's CONTAMINATION-LIMITED label is dropped by the final scorer), C5
  ("canonical decides" vs "each footing its own verdict").
- **A Newtonian sky is survival for the adopted theory, never confirmation.** v3s vs Newton is NOT SEPARABLE (CQ2). DR4 can
  kill v3s from above; it cannot confirm it.

## 1. The registry

Columns: id; prediction and kill line; source and first commit; theory version; later decisions that supersede or keep
it; scorer on disk and whether its frozen inputs match; status today.

### 1A. Wide binaries, the pre-registration family (`prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`, first commit f617640aeb 2026-07-16; current sha256 20677265..., equal to Amendment 22's "after" digest)

| id | prediction / kill line | source, first commit | theory | superseded or kept by | scorer, inputs | status |
|---|---|---|---|---|---|---|
| P0 | framework-MI gamma_v band 1.05-1.10, point 1.09; framework-as-MG 1.137; MOND benchmark 1.33. Section 1.5 z-rule: consistent \|z\| < 2, disfavored \|z\| > 3, sigma_tot = sqrt(sigma_fit^2 + 0.02^2); "canonical footing decides; alt footing reported" | prereg section 1.1 / 1.5, f617640aeb 2026-07-16 | 2026-07 modified-inertia program | 1.09 superseded for 2-30 kAU by A1 (07-27), then A3/A4 (07-30/31), A8 (08-03), A9 (08-09), A10 (08-13). 1.137 marked STALE (A4(i)); pipeline `GAMMA_MG` carries "STALE". The section 1.5 z-rule, sigma_sys 0.02, guard zone and stability requirements remain the frozen error model | `wide_binary_pipeline.py` (sha256 7c884e0e..., matches the release checklist section 3 pin) prints these as `[7(e)]` quoted thresholds, no verdict word | SUPERSEDED as a target; error model and guard zone still bind |
| P1 | A1 gated branch: 1.0004-1.0006 in 2-30 kAU; p = 3 excess beyond about 50 kAU; five falsifiers | A1, 1a018751e2 2026-07-27 | MI, gated | A6 (2b25fb72e9, 08-02): "Amendment 1's basis is withdrawn"; A7 lists it as "basis withdrawn" | none | WITHDRAWN (still quoted as live in the scorecard section 7 list) |
| P2 | ungated alpha = 2 target 1.0310 (1.0218-1.0472) | A3/A4/A7, 07-30 to 08-02 | MI, alpha = 2 | A8 (08-03) moves to 1.1582; A9 to MG 1.2139 / 1.2592 provisional; A10 supersedes | none | SUPERSEDED |
| P3 | **Arm A**: 1.1614-1.1814 canonical / 1.1917-1.2267 alt; no-verdict edge 1.23; Arm A falsified below 1.056 (A11(d)) | A10, 40ca6ad7ff 2026-08-13 | AQUAL-EFE kernel as modified gravity | Kept unchanged by A11-A22. Its floor is the law-first anchor of the D2 rows (owner D2 (a), 11-05). G018 (09-13) calls Arm A "Cassini-dead". Not the adopted theory | pipeline constants `GAMMA_TARGET` 1.1614 / `_TOP` 1.1814 / `_ALT` 1.1917 / `_ALT_TOP` 1.2267 / `NOVERDICT_EDGE` 1.23: match | IN FORCE as a row and as the anchor; not adopted |
| P4 | **Arm B**: corrected to 1.0000 +- 0.0025 both footings; killed from above at gamma-hat >= 1.084 | A11 5a865128fc 09-06; corrected A12 779e769343 09-09 | covariant candidate, carrier reading | A12(g): "not a testable arm"; ceilings 1.0450 / 1.0300 "vacuous" | pipeline `GAMMA_B_PRED` 1.0000, `GAMMA_B_KILL` 1.084: match | IN FORCE, not testable, not adopted |
| P5 | **Arm C**: 1.000 exactly, pooled 3-30 kAU, both footings and g_ext; z_C = (gamma-hat - 1)/sigma_tot; falsified for 1.084-1.23 only if the frozen stability requirements pass (ladder within 1 sigma_fit, kappa in [0.95, 1.05], NSS-off probe toward the verdict), else "systematic-limited, no verdict" | A13, fc64ffaac6 2026-09-27 | hierarchical ownership reading (FG001) | Kept by A14-A22. Review 11-05 calls the theory retired but notes "Arm C's rows are numerically v3s's". No decision revokes the rows | `dr4_ready_1/arm_c_rows.py` (7fa07e69f5): prints sigma_tot with 0.02 and the z row; header says stability requirements "NOT evaluated here", operator reads them from the log | IN FORCE as rows; see C1, C2 |
| P6 | derivation chain ceiling: 1.000 <= gamma_v <= 1.0725 canonical / 1.0900 alt; falsified at >= 1.157 / 1.174 if stability passes; separation-resolved r_b statistic measures xi (not a verdict statistic) | A14, 30f4cce9f5 2026-09-28 | derivation chain (FP7/FP14) | Kept. Reporting rule 7(e) extended to the ceilings | `amdt14_distances.py` (6e515fd8fb) prints distances to the ceilings and A20 lines. The xi statistic lives only in `XR22_prereg_statistic.py` (`sepbins`, 661ea3cffe) and is in no runbook step (C12) | IN FORCE, report-only |
| P7 | anisotropy falsifier gamma_perp - gamma_par (A2(f), A3(c), A8(f), A11(d2)); quoted only when MEASURABLE (neither projected fit on a grid edge) | A2-A11; A20 f1f104adab 2026-10-03 | MI/MG arms | A20 governs quoting | pipeline `[aniso]` lines; `amdt14_distances.py` prints `[A20]` | IN FORCE, conditional |
| P8 | settling working model: gamma = 1.000, scored by Arm C's rows unchanged; falsified with Arm C for 1.084-1.23 with stability passing | A21, 347f358871 2026-10-06 | 2026-10-06 settling model (cold fluid settles to the law's target) | Kept. Closest registered reading to form B (2026-11-09); no decision links them (C2) | `arm_c_rows.py` | IN FORCE as rows |
| P9 | CFG800 R rule, as defined by A22: sigma_R = max(sigma_tot, R's own error); KILLED iff R - 1 >= 0.01 and >= 3 sigma_R; CONSISTENT needs 2 sigma_R <= 0.01 (unreachable); "FRAMEWORK KILLED" means CFG740's stiffness construction only | A22, a553a4a663 2026-10-15; CFG800 criteria aa71ca5107 10-15 | CFG740 stiff hedgehog | Restated by the 10-21 kill-line note (sigma_R from N_R, kill needs about R >= 1.22 at N_R 2,100); D7 N5 (R input = registered catalogue, `--declare-neutral non_single_star`); D7 N7 (CFG740 falsifier 1 beyond ~37 kAU and falsifier 2 not scored) | `CFG816_dr4_r_statistic_scoring/cfg816_r.py` (bee2b59f2b; criteria d9eed26ebc), ONCE ONLY on DR4; its classify() matches A22. It also carries a frozen CONTAMINATION-LIMITED downgrade that the final scorer drops (C4) | IN FORCE |
| P10 | Section 2, s^TX boost dipole (DR4-era ephemerides) | prereg section 2, 2026-07-16 | MI-era preferred frame | A5 (08-02) voids section 2's DETECT/KILL bands; review 11-05: "void" | `stx_dipole_template.py`, not in any runbook | VOID |

### 1B. Wide binaries, sealed or registered outside the pre-registration

| id | prediction / kill line | source, first commit | theory | superseded or kept by | scorer, inputs | status |
|---|---|---|---|---|---|---|
| S1 | **CQ2: v3s wide binaries screened and Newtonian.** gamma_r - 1 <= 4.45e-5 canonical / 4.01e-5 alt at 30 kAU; through the frozen pipeline gamma_inf identical to Newton's in every realisation (1.0019 / 1.0100 are the pipeline's Newton draws, not a v3s offset). v3s vs Newton NOT SEPARABLE; vs plain QUMOND SEPARABLE. "This seal adds no rule" | `cq_lanes_2026_11_04/CQ2_v3s_dr4_seal/`, criteria 532e0dc567, seal 95303af61c, 2026-11-04 | **v3s (adopted 11-04, 7ac515f958)** | Kept by 11-05 D1 (a) (scored as the screened reading of the D2 rows plus R); by the Pi^6 blend adoption 11-07 ("every graded label unchanged"; the seal was computed with v3s's raw kink, not re-run under the blend); by form B 11-09 ("every sealed prediction, scored as frozen") | scored by `dr4_outcome_map.py` (below), not by a CQ2 script | **GOVERNING PREDICTION** |
| S2 | **D2 fork rows** (whole-catalogue gamma-hat): medium-first/screened excluded iff gamma-hat - 1 >= 3 sigma and not >= 3 sigma below the anchor; law-first excluded iff anchor - gamma-hat >= 3 sigma; sigma = sqrt(sigma_fit^2 + sigma_sys^2). A1: gate sigma_sys < 0.048 / 0.058. A3 (owner, 10-22): sigma_sys(b) primary; (a), (e), (g2) must agree; (c), (d), (f) and the section 1.5 stability gate (g3) "no verdict weight" | `NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md`, 8658130bd0 2026-10-22 (A1-A3 same day) | law-first vs medium-first fork | 11-05 D1-D6 (a); D7, D8 (11-05b); NSS-off entry replaced by the seed mean (11-05c, filed 11-08) | `dr4_push_2026_11_05/DP3_release_day/dr4_outcome_map.py` (7b3d933e3f; criteria d66d012f57). Anchor 1.1614 / 1.1917, Newton 1.000, gate 0.048 / 0.058, D5 BOTH EXCLUDED, A3.2 robustness: match. It does not evaluate the section 1.5 stability requirements (C1). sigma_sys comes from `dp3_sigma_sys.py`, whose seed-mean option is not passed by the release script (C3) | **GOVERNING RULE** |
| S3 | **11-05 outcome map** (arithmetic on S2): at N 30,000, sigma_sys 0.020 canonical: <= 0.917 sub-Newton NO VERDICT; 0.917-1.079 law-first excluded ("v3s survives"); 1.079-1.083 UNDECIDED; 1.083-1.23 v3s EXCLUDED; > 1.23 guard. Alt: 1.083-1.109 BOTH EXCLUDED. Edges move with N and sigma_sys (at DP2's N about 8,000: screened-excluded edge 1.125 / 1.157 / 1.184 by error model) | `OWNER_DECISION_2026-11-05_DR4_FORKS.md`, 413c1c8e24 2026-11-05 | v3s vs bare law | Kept; collected in `closure_2026_11_07/PREDICTIONS_2026_11_07.md` section 1 (52d4f27840) | `dr4_outcome_map.py` self-test reproduces the map (20/20 per runbook; not re-run here) | IN FORCE (bands are illustrations; the 3-sigma rule is operative) |
| S4 | CW1: bare law (plain QUMOND) 1.149 +- 0.027 / 1.208 +- 0.007; LOC1/LOC3/E55/HALF forms | `cw_lanes_2026_11_04/CW1_wide_binary_seal_dr4/`, criteria da6917883b, seal e7672a30e1 2026-11-04 | bare a0 law, unscreened | 11-05 D2 (a): reported as information, does not anchor the rows | printed as information by `dr4_outcome_map.py` | INFORMATION |
| S5 | FN6 screening-length window: points 1.00-1.04 (p <= 0.4); alt p 0.45 1.13-1.21; EXCLUDED if \|gamma-hat - gamma_inf\| > 3 sigma_tot at every point; Newton through the same pipeline 0.9919 / 0.9794 | `finish_2026_11_04/FN6_powerlaw_screening/SEALED_PREDICTION_DR4.md`, 7ab147288d 2026-11-04 | description, not adopted | 11-05: "description, not adopted"; D3 (a) Newton = 1.000 | none on the release path; printed as information | INFORMATION |
| S6 | CFG740: stiff hedgehog envelope gamma_v - 1 <= 8.9e-4 at 50 kAU, 2.0e-2 at 236 kAU; falsifiers: gamma_v >= 1.01 at s <= 50 kAU; log-slope not 2 | `campaign_fresh_gravity/CFG740_sealed_wb_slope2/`, criteria c4f88c6eed, seal 1be4101aff 2026-10-13 (sha256 5336fd99...) | stiff hedgehog, same s^2 form as v3s, older L* 5.754 pc | Scored only through R (P9). D7 N7: falsifier 1 beyond ~37 kAU and falsifier 2 not scored | `cfg816_r.py` | IN FORCE via R |
| S7 | G018: binned gamma_v(s) rising from about 1.06 (1-3 kAU) to 1.10-1.11 (20-30 kAU); "Newton kills the field half"; own text uses "confirm" | `glm53_push/G018_dr4_binned_prediction.py`, 0dbe430d33 2026-09-13 | September equilibrium identification (mu_2 EFE bracket) | No decision retires or keeps it. Scorecard: "superseded by v3s, still ARMED in the matrix" | no scorer of its own | STALE, unresolved (C9) |
| S8 | Falsifier matrix row 1, "the DR4 ridge" (G088/G165): plateau in [1.047, 1.11] at 10-30 kAU; P-s excess +18.4 % at 30.7 sigma; break at 7.4 kAU. Kill: Newtonian level AND Newtonian P-s ridge. Row text also quotes "Arm A falsified below 1.056; Arm B falsified >= 1.129" | `deepseek_push/FALSIFIER_MATRIX.md`, 14a237c04d 2026-09-16; Z03 re-register 8caa817d08 2026-09-16 (DISFAVORED reserved for "ridge absent"; 9/9 unreachable) | September deepseek identification | Arm B's 1.129 was corrected to 1.084 by prereg A12 on 09-09, before this row; not updated. No decision retires it; status ARMED | `deepseek_push/dr4_scorer.py` (0a2bffa908 2026-09-16). Inputs do NOT match the registration: it needs per-pair (P_yr, s, gamma_v) rows, which the frozen pipeline does not produce (it fits one pooled gamma-hat); fixed sigma 0.028; prints CONFIRMED-STRONG / CONFIRMED-WEAK, contrary to the prereg honesty rule and owner D6. Its default run is the mock. Not run here | STALE, unresolved (C9) |
| S9 | Matrix row 13, footing K1: the DR4 ridge at the RAR scale kills a0_DE-alone | matrix, 2026-09-16 (G190) | deepseek | Contact log 09-25: K3's reference scale is an artefact; K1 rests on row 1 | none (G190 has no script, per the matrix log) | STALE |
| S10 | deepseek PREDICTIONS E6/E7: gamma_v rising 1.002 -> 1.047 to 30 kAU; 7.4 kAU break | `deepseek_push/PREDICTIONS.md`, 1e8bc9b34b 2026-09-14 | deepseek | G026's own output: must not be represented as registered (scorecard section 7) | dr4_scorer.py rows | NOT A REGISTRATION by its own record |
| S11 | KT20: filter suppresses the boost below 5-8 kAU, equals plain QUMOND above about 15 kAU ("PREDICTION, nothing graded") | `rebuild_2026_10_22/KT20_filter_wide_binaries/`, 94562be676 2026-11-03 | KT17 filter | CW1 (11-04) says KT20/KT21 carried the CZ1 defect | none | INFORMATION, defect noted by CW1 |
| S12 | gemini38: 1.116-1.135 at 20 kAU | `gemini38_flash_push/*REPORT.md` | quarantined exercise (the "fried chicken" reports) | owner quarantine of that exercise | none | NOT A REGISTRATION |

Not counted as predictions but on the DR4 path: D2 lane sigma_sys recipe (`d2_sigma_sys_defs.py`, 51030bbb6c 10-22);
CFG943 readiness (7356bb671d 10-20); Amendments 15-19 (cut mapping, cut 9 SFD98 primary, cut 13 literal primary, cut 12
counted tables, sigma_build and the seed-sensitive label, sync transport); the 10-21 kill-line note (35ea5e1bed); D7 N9
(cut 13 `cones-literal` for the primary, `extract-builder` for the Amendment 18 sweep).

### 1C. Milky Way, vertical structure, local density, Oort constants

| id | prediction / kill line | source, first commit | theory | superseded or kept by | scorer | status |
|---|---|---|---|---|---|---|
| M1 | Matrix row 2, double-map: two-scale vertical dark structure at R0 (D1 fall 4.2x; D2 column 27.8 vs NFW 6.6; D3 negative outer bin 180-562 pc). Kill: single-scale profile or positive dark mass at 300-560 pc | matrix 14a237c04d 09-16; G092 4dd5676d1d 09-15; `deepseek_push/DR4_AMENDMENT_12.md` ae3ebf6ece 09-15 | September phantom slab + sech^2 dark disk | The deepseek "Amendment 12" was never appended to the prereg (the prereg has its own, different Amendment 12, 09-09; the prereg contains no vertical rows). Status ARMED | `dr4_scorer.py` (inputs: a vertical-z catalogue that no DR4 release product supplies) | STALE, unresolved |
| M2 | Matrix row 3, funnel: z_c(R) = a0/(16 pi G rho_b(R)), 34.7 / 140.6 / 1357 pc at R 4 / 8.2 / 15 kpc, flare e^(R/3). Kill: z_c(R) flat or random | matrix 09-16; G076/G112; deepseek "Amendment 12" | same | same | `dr4_scorer.py` | STALE, unresolved |
| M3 | Matrix row 26, halo saturation: total dark column < a0/(4 pi G) = 68.5 Msun/pc^2. Kill: DR4 column >= 68.5 | matrix (ZD07, 2026-09-23) | deepseek | ARMED | none | no scorer |
| M4 | Matrix row 29, kinematic face: Oort A = (Omega/4)(1 - s beta), B = -(Omega/4)(3 + s beta); kill: \|dlnVbar/dlnR + 0.41\| > 0.15 at R0 | matrix (ZD10, 1f06e9de74 2026-09-23) | deepseek | ARMED | none | no scorer |
| M5 | Matrix row 31, local density: rho_dark(R0) = 0.008 +- 0.002; column 67.2 = 98.1 % of 68.5. Kill: column >= 68.5 or rho outside 0.008 +- 0.002 | matrix (ZD13, 5717375b97 2026-09-23) | deepseek | ARMED | none | no scorer |
| M6 | CFG553: K_z(R, z), V_c(R), outer slopes, local dark density, Sigma_1.1, sigma_z, V_c at 30-60 kpc for RM-v / RM-phi vs PD (QUMOND) vs NFW; frozen per-prediction labels (FRAMEWORK-SUPPORTED / -EXCLUDED / BOTH EXCLUDED / NOT DIAGNOSTIC) with R0, distance-scale and tracer robustness | `campaign_fresh_gravity/CFG553_sealed_gaia_dr4_predictions/`, 43fb646121 2026-10-10 | round cold-energy rule (cold sector) | Cold sector retired 11-01, whose decision table says sealed predictions are "scored as frozen, including route rows: ... Gaia DR4". Form B (11-09) reopens the cold sector for one reading and keeps route E's native rule N and core rules retired; it does not say whether RM is inside B | none (only `cfg553_predict.py`, the prediction generator) | SEALED, theory status unclear (C10) |
| M7 | S3 v3 MW seal: CFG553's P1-P5 for v3 plus P6, an EFE azimuthal asymmetry A(R) = 1.8 / 3.0 / 4.1 / 5.2 / 8.2 % at 15 / 20 / 25 / 30 / 60 kpc; CFG553 rules verbatim | `rebuild_2026_10_22/S3_v3_mw_seals/SEALED_V3_MW_DR4.json`, ec0c57d236 2026-10-23 | v3 (before v3s) | v3s's adopted scope (11-04) excludes "the Milky Way joint fit"; v3's outer slope already SHAPE EXCLUDED on DR3 (Z -4.37 / -4.62) | none | SEALED, out of the adopted scope |
| M8 | GD1: route E OS1 Milky Way for DR4: V_c(R0) 200-210 km/s (4-6 sigma below Eilers), K_z(R0, 1.1)/2 pi G 67-70 | `rebuild_2026_10_22/GD1_route_e_mw_dr4/`, 2eeff4935d 2026-10-26 | route E (retired 11-01) | retired with route E | none | a lane result, not a seal; RETIRED theory |
| M9 | glm53 G026 E1-E4: slab scale 140.6 pc and exponents (scorecard row) | glm53_push, September | deepseek/glm53 | as M2 | none | as M2 |

## 2. Which registration governs for the theory the record currently adopts

The record's current adoption chain: v3s adopted as the a0 law's action, scoped (2026-11-04, 7ac515f958); the Pi^6 blend
adopted as its stiffness (2026-11-07, 71e4014cd5, "v3s scope and every graded label unchanged"); form B adopted as the
form the record closes on (2026-11-09), which keeps "v3s as the law's action inside its adopted scope; every sealed
prediction, scored as frozen" and says "Gaia DR4 (2026-12-02): the pre-registration is unchanged and is scored as frozen."

**Wide binaries.** The governing decision is `OWNER_DECISION_2026-11-05_DR4_FORKS.md` (413c1c8e24), section 3:

> "Ruling (owner, 2026-11-05): D1 (a), D2 (a), D3 (a), D4 (a), D5 (a), D6 (a) ADOPTED. ... Consequences, stated now: v3s is
> scored in DR4 as the screened / medium-first reading of the frozen D2 rows plus the R rule; the law-first anchor stays
> Arm A's floor; Newton = 1.000; gamma-hat <= 1 - 3 sigma is NO VERDICT for every reading; in the alt overlap of section 2b
> the reading is BOTH EXCLUDED; a Newton-side reading is worded "v3s survives", never "confirmed"."

Completed by: 11-05b (d71a111d1d) D7 N4 (NSS-off rung built by `build(drop_nss=True, smax_kau=30)`, NOT IMPLEMENTED if its
DR3 check fails; a shift below 1 sigma_fit passes), N5 (R input = registered catalogue), N7, N9, and D8 (a) (sigma_sys(b) as
frozen); 11-05c (filed 2026-11-08, a35171230f): the NSS-off entry of sigma_sys(b) is the K = 50 seed mean
gamma-hat_0 + Delta-bar; the 10-21 kill-line note (sigma_R from N_R). The prediction is CQ2.

**Milky Way rows.** The record does not say. v3s's scope excludes the Milky Way joint fit; no decision after 11-04 names a
vertical, local-density or Oort prediction for v3s or form B; the 11-05 decisions cover wide binaries only. The only text
that touches them is the 11-01 retirement ("Sealed predictions ... scored as frozen, including route rows: ... Gaia DR4"),
which keeps retired-theory seals scorable without attributing them to the adopted theory.

## 3. Status today, in one paragraph

On the day, the record supports exactly one scored confrontation for the adopted theory: the pooled gamma-hat of the
frozen pipeline on the DR4 catalogue, read through `dr4_outcome_map.py` per footing, with R from `cfg816_r.py` beside it.
Arm A, B, C, the chain ceiling, the settling model, CW1 and FN6 are printed as rows or information. The deepseek ridge and
vertical rows, G018 and CFG553 / S3 have no scorer that can run on 2026-12-02 and no decision that says whether they count.
At DP2's realistic N (about 8,000, 583697a4f7) a Newtonian sky reads decisive against the bare law with probability about
0.80 at sigma_sys 0.020 and 0.12-0.40 at DR3's 0.0375 (11-05c section 2).

## 4. Conflicts and ambiguities to settle before 2026-12-02

Each item: what conflicts, what each reading means on the day, what an owner decision would need to state. None is
decided here.

**C1. Do the frozen stability requirements gate "v3s EXCLUDED"?**
- Prereg section 1.5: "Stability requirements for any non-Newtonian verdict (frozen): every strictness-ladder variant
  must shift gamma_hat by < 1 sigma_fit; kappa within [0.95, 1.05]; the NSS-off contamination probe must move gamma_hat
  TOWARD the verdict value ... Any failure -> systematic-limited, no verdict." Arm C (A13) and the settling model (A21)
  repeat this for their 1.084-1.23 falsification row. D7 N4 refers to "boost-side verdicts" and "systematic-limited" outcomes.
- D2 A3 (owner, 10-22): the section 1.5 stability gate (g3) is "computed and reported beside the verdict with no verdict
  weight". `dr4_outcome_map.py` never assigns "systematic-limited"; it prints only the N4.3 reminder. On DR3 the stability
  gate FAILED on both footings (largest ladder shift 0.075 > sigma_fit 0.055).
- On the day, gamma-hat of about 1.12 with a ladder rung moving by more than 1 sigma_fit reads "v3s EXCLUDED (screened
  reading)" under the scorer and "systematic-limited, no verdict" under Arm C's rows, which are numerically the same
  prediction. Arm C also uses the frozen sigma_sys 0.020 while the D2 rows use sigma_sys(b) and a gate, so the two can split
  on sigma alone.
- A decision would state: whether the section 1.5 stability requirements (and the kappa window) apply to SCREENED_EXCLUDED
  and BOTH_EXCLUDED; if they do, the scorer change needed (new code, own criteria, pre-data); and which line is the headline
  when the D2 rows and Arm C's rows disagree.

**C2. Which registered wide-binary reading belongs to form B?**
- Form B (11-09) says only "scored as frozen". The frozen pre-registration's cold-fluid reading is A21's settling model
  (Arm C's rows); the 11-05 decisions attribute DR4 to v3s through the D2 rows. PAPER72 rule 5 ("a body that brought no
  charge has no halo") implies a Newtonian binary but is not a sealed prediction.
- On a boost, the record would say "v3s EXCLUDED" without saying whether form B falls with it; on a Newtonian sky it would
  say "v3s survives" without naming form B.
- A decision would state which seal and which rows score form B (CQ2 via D1, A21 via Arm C's rows, or both reported), so the
  word "survives" or "excluded" attaches to the form the record closes on.

**C3. The filed seed-mean NSS-off entry is not wired into the release-day path.**
- 11-05c is FILED (2026-11-08). `dr4_release_day.sh` step O12 (line 233) calls `dp3_sigma_sys.py` without
  `--nss-off-seed-mean`, so it computes sigma_sys(b) with the superseded single-seed entry. The option's help text still
  says "draft ... NOT FILED". No runbook step runs the DR4 K = 50 sweep (`dp7_seed_mean.py --release dr4 ... --K 50`,
  DP7 RESULT section 7, about 70-80 min, 4.0-4.3 GB per fit, archive delta fetches needing a go). The script only pins the
  decision's sha256 (f704278a77).
- 11-05c also leaves to "the owner's call on release day" whether G7's cone query covers the pre-NSS candidate set or the
  rung uses `--missing-cones extract-fallback` (139 pairs on DR3). The runbook's own rule is that none of its open items may
  be decided after the data.
- On the day, run as scripted, the binding error term would be the one the owner replaced; on DR3 the two entries differ
  enough to move (b) from 0.0375 / 0.0412 to the 0.020 floor.
- Needed before release: a pre-data fix of the wrapper and runbook (new step, own criteria, DR3 equivalence), and a dated
  decision on the cone-coverage choice.

**C4. The R label: CFG816's CONTAMINATION-LIMITED rule vs the final scorer.**
- CFG816 frozen criteria (d9eed26ebc) and `cfg816_r.py`: a primary KILLED becomes "CONTAMINATION-LIMITED, not KILLED" if the
  NSS-screened branch is not KILLED or f_tail differs by more than 2 sigma. `dr4_outcome_map.py` reads only R, sigma_R and N
  from the JSON and recomputes the label, so it prints KILLED where CFG816 prints CONTAMINATION-LIMITED.
- D7 N5 declares `non_single_star` neutral in the R input, so the NSS-screened branch equals the primary and only the f_tail
  test can trigger the downgrade.
- A decision would state which R label is quoted, and whether the NSS-screened branch is meant to be vacuous under N5.

**C5. "Canonical footing decides" vs one verdict per footing.**
- Prereg section 1.5: "canonical footing decides; alt footing reported". D2 A3.4, the 11-05 map and the scorer: each footing
  its own verdict line, never pooled; a split is reported as a split.
- On the day a canonical / alt split (likely in the alt overlap 1.083-1.109) has no headline under the later texts and a
  canonical headline under the prereg.
- A decision would state whether the prereg's "canonical decides" still names a headline footing, or is superseded.

**C6. sigma_sys(b) ladder membership (runbook O6, open).** RUWE < 1.2 is implemented in `seed_sweep.py --ladder` and
`dp3_sigma_sys.py --stage-a` but was declared unimplementable in the D2 recipe. On DR3 it moves alt (b) 0.0412 -> 0.0350. The
11-05c text mentions "RUWE if O6 adds it". A decision would list the rungs that enter (b) on DR4.

**C7. Optional neighbour tables for cut 13 (Amendment 16(b)).** Whether `gaia_source_environment` and
`crowded_field_source` are searched is "a release-day decision recorded before the data are opened". Not yet recorded.

**C8. Archive account and login (runbook G2, O3).** None of the tools logs in; a registered account helps only with a login
hook (new code, tested). Owner-only.

**C9. Stale "ARMED" wide-binary rows with their own scorer.** Matrix row 1 / G088 / G165 / Z03 (band [1.047, 1.11], P-s
ridge, 7.4 kAU break), G018, E6/E7. No decision retires or keeps them. `dr4_scorer.py` cannot ingest the frozen
pipeline's output and prints "CONFIRMED". Row 1 quotes Arm B killed at >= 1.129, corrected to 1.084 by A12 a week earlier.
A Newtonian sky "kills the identification" by row 1 and is "survival" for v3s, so the record would print a kill and a
survival for one result. A decision would state whether these rows are scored, reported as information, or retired, and
that `dr4_scorer.py` is not run (or what replaces its inputs).

**C10. Milky Way rows have no adopted-theory owner.** CFG553 (cold-sector RM rule), S3 (v3), GD1 (route E), matrix rows
2, 3, 26, 29, 31. None has a DR4-data scorer; each needs a published Jeans / Oort / K_z analysis, which will not exist on
2026-12-02. A decision would state which, if any, are scored for form B or v3s, by which frozen rule (CFG553 sections 4-5
is the only fully specified one), and that they are scored when such an analysis is published, not on release day.

**C11. Newton reference.** CQ2/CW1 Newton draws 1.0019 / 1.0100, FN6's 0.9919 / 0.9794, D2 / prereg 1.000, same pipeline
hash. Resolved by D3 (a) (1.000; draws as information). The scorecard's "KT1 (CQ2): 1.0019 / 1.0100" quotes the draws as
the prediction; text only.

**C12. A14(c)'s separation-resolved xi statistic is registered but in no runbook step.** It is a measurement, not a
verdict. A decision would state whether it is run on the day (XR22 `sepbins`) or left unrun.

**C13. Pipeline freeze hash.** The prereg's own manifest lists `wide_binary_pipeline.py` sha256 669fecc4...; the file was
retargeted after filing (last commit 2a18b570e8, 2026-09-22) and is now 7c884e0e..., pinned by the release checklist
section 3 (2026-09-28) and the DP3 wrapper. No filed amendment records the new hash. Text only, unless the owner wants it
recorded.

**C14. Stale summaries.** Root `STANDING.md` "Live fronts" still names Arm A as the DR4 front and has no DR4 addendum after
11-04; PAPER67 v1.2 says a Newtonian result counts against the law and does not cite CQ2 (review 11-05). Text only; the
11-05 D6 wording rule governs what is said on the day.

**C15. A3's anchor values vs D2 (a).** A3 (owner, 10-22) names the AQUAL values (1.167 / 1.199, and 1.145 / 1.173 at the
alternative g_ext) and says both g_ext values are scored. D2 (a) (owner, 11-05, later) keeps Arm A's floor and reports the
others as information; the scorer prints an "information split". At N 30,000 a gamma-hat near 1.07 is law-first excluded on
the Arm A anchor and not on the alternative-g_ext AQUAL anchor. Resolved by the later decision on its face; listed so the
split line is not read as a second verdict.

## 5. On the day: checklist (order from `RELEASE_DAY_RUNBOOK_DR4.md` and `RELEASE_DAY_CHECKLIST.md`)

Before 2026-12-02: settle C1-C10 by dated, pre-data owner decisions or fixes (new files, committed alone; no frozen file
edited). Every archive step needs the owner's yes naming step, table, size and time, written as `GO <step>` in
`dr4_push_2026_11_05/DP3_release_day/OWNER_APPROVAL_DR4.md`.

**Read first:** `PREREGISTRATION_DR4.md` sections 1.2-1.5 and Amendments 13-22; `RELEASE_DAY_CHECKLIST.md` sections 0-7;
the D2 note with A1-A3; `campaign_fresh_gravity/OWNER_DECISION_2026-10-21_DR4_KILL_LINE.md`; the three 11-05 owner
decisions (05, 05b, 05c); `cq_lanes_2026_11_04/CQ2_v3s_dr4_seal/SEALED_PREDICTION.md`; the DP3 runbook; DP7 RESULT section 7.

**Inputs that must be frozen and match before any byte is opened** (`dr4_release_day.sh --check`, 27 pins):
`wide_binary_pipeline.py` 7c884e0e...; `build_catalog.py` 46452daf...; `fetch_extract.py` d826f688...; prereg 20677265...
(all four checked today with `shasum`: match); both 11-05 decisions, 11-05c, the D2 note, the kill-line note, CFG825's four
files, the dr4_ready_1 tools and manifest template, the D2 sigma_sys recipe. CFG816's once-only slot
`cfg816_r_dr4_results.json` must be absent. Free disk >= 20 GB; no other python job > 2 GB; no 1024^3 run.

**Order:**
1. R0 self-tests (driver, `amdt14_distances.py`, `arm_c_rows.py`, `make_pair_table.py`, `dr4_outcome_map.py`). Offline.
2. G1 save the published data model; write `spec_dr4.json` (renames only) and `manifest_dr4.json` (cut 9 = SFD98, A16(a);
   cut 12 counted tables, A17). Record the C7 optional-table decision here, before data.
3. G2 account (owner logs in himself).
4. G3 base extract (`DP5 fetch_extract_dr4.py`), about 7 M rows, about 2.8 h.
5. G4 `build_catalog.py --release dr4` (stages A-F).
6. G5 NSS id files for the six A17 tables (`fetch_nss_dr4.py`) and the `all_source_flags` join.
7. G6 candidate dump (`--cut13 extract-builder`), pre-brief (`dr4_q1_estimate.py`), count queries, plan check.
8. G7 cut-13 neighbour cones (`q1_cones_dr4.py`, caps in the GO line; about 39,000 queries, about 47 h serial). Apply the
   pre-decided C3 cone-coverage choice (pre-NSS set or extract-fallback).
9. G8 primary build, `--cut13 cones-literal` passed explicitly (D7 N9), through `dp6_with_a17.py`.
10. O9 frozen pipeline `--catalog`, then `amdt14_distances.py --log` (A14 ceilings, A20) and `arm_c_rows.py --log` (Arm C /
    A21 rows; check the stability requirements from the log by hand, C1).
11. G10 Amendment 18 sweep (`seed_sweep.py --mode g-only --K 50 --cut13 extract-builder`), `seed_label.py`.
12. G11 NSS-off rung (DP1 REPRODUCED). If C3 is fixed: the DR4 seed-mean sweep `dp7_seed_mean.py --release dr4 --K 50
    --cut13 cones-literal`.
13. O12 `dp3_sigma_sys.py` with `--nss-off-seed-mean <dp7 dr4 json>` (11-05c; not in the script today, C3) and the C6 rung
    list; `make_pair_table.py --declare-neutral non_single_star` (D7 N5).
14. G14 ONCE ONLY `cfg816_r.py --dr4 pairs_dr4.csv`; record its own label (C4). Variant catalogue information only.
15. O15 `dr4_outcome_map.py` per footing: guard, sub-Newton, gate, D2 rows, A3.2 robustness, R, splits.
16. Write `RESULT_2026-12-02.md`: label lines verbatim; raw gamma-hat, sigma_fit, every sigma_sys, both distances, R block,
    splits, NSS-off status, A14 / A20 / Arm C lines, sigma_build and seed label. "v3s survives", never "confirmed"; no
    verdict word beyond the filed labels. Commit with explicit paths only.

Not on the day: CFG553, S3, GD1 and matrix rows 2, 3, 26, 29, 31 (no DR4-data scorer; they wait for published analyses and
for C10); `dr4_scorer.py` (C9); section 2 s^TX (void).

## 6. What this audit could not resolve

- Whether CQ2's screening margin holds under the Pi^6 blend adopted on 11-07 (CQ2 was computed with v3s's raw kink); the
  blend decision says labels are unchanged but records no wide-binary re-run.
- Whether CFG553's round rule (RM-v / RM-phi) is inside form B or among the retired cold-sector rules.
- Whether `dr4_outcome_map.py`'s self-test still passes (not run, by instruction); the 20/20 figure is the runbook's.
- The SDSS DR20 wide-binary audit (`research_closure_2026_11_12/sdss_dr20_wide_binary_audit/`, uncommitted, another
  session's work today) screens the DR3 dry-run membership (6,180 cones-literal pairs) and lists four APOGEE follow-up
  priorities; it changes no registered number. The RV-screened ladder rung has no implementation, and SDSS data could
  feed one only through a pre-data decision; the audit notes DR3 identifiers need cross-release mapping for DR4.
- Earlier registries in `real_research/` and `opus_48_extended_research/` (June to August) that mention DR4 were not read
  one by one; the scorecard classes them retired (inertia arm closed 08-08).
