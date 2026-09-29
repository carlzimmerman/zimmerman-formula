<!-- Gate status refresh for candidate B. A NEW file; the frozen list closure_map/GATES.md is untouched. No new physics: every entry below is read from a committed output. -->
# Candidate B against the frozen gates: status refresh, 2026-09-29

**Scope.** This file restates the status of every row of the frozen list `closure_map/GATES.md` (frozen 2026-09-28, commit 653e5af9a), using everything committed since then:
- lanes CFG40–CFG59, plus CFG40 itself, which GATES.md did not cite;
- the referee notes 071301aab (CFG40–42) and 35eebbe99 (CFG48).

The row ids are GATES.md's, and each row carries one status.

**Rules applied.**
- The frozen list, its thresholds and its row ids are not moved.
- **Status** is candidate B as frozen: the law T1–T6 plus FG001 ownership.
- **Derived rule** is B's cold-mass rule, the sum S of CFG35/36, where a lane has scored it.
- A row with no committed change since GATES.md is **carried** and marked *reported (GATES.md)*.
- A row changed by a lane cites that lane's script and commit.
- **Verified** means the lane's scripts were re-run in every mode with a committed output, from a clean `git archive` export of HEAD a628e8a66, and the outputs matched the committed ones line for line apart from the timing field.
- Rows 1.25–1.26 are **new populations** scored since the freeze. They are not in the frozen list and are marked NEW.
- Nothing here says the theory is closed. κ = ½ and Ω_c h² stay fitted.

**Bottom line.**
- **Candidate B's gate record has not improved since the freeze. It has sharpened.**
- **The one clean pass of B's derived rule (SLUGGS) did not survive dynamical stellar masses.** The law's deficit grows to 4.0σ, and the rule leaves 2.6σ (CFG55).
- **The rule's gains and costs trade off.** It closes the ultra-faint failure but breaks the classical satellites and the LV field dwarfs. No single fraction of its debris reconciles the populations (CFG42, CFG45, CFG58, CFG59).
- **The top of the disk mass function is a new marginal failure of the law**, 2.3σ on the nine fastest super spirals (CFG40, CFG56).
- **At the action level**, Gap 1 and Gap 2 are scoped no-gos that collapse into one non-derivable object, and Gap 3 is partly filled (CFG43, CFG44, CFG48, CFG50). One stability expectation fell: a nonlocal enclosed-mass gate is second-variation stable (CFG48 G6, referee-reproduced).
- **a₀(z) at z ≈ 2.5 still cannot be scored** from the data on disk (CFG52, CFG54).

Status codes: PASS / FAIL / MARGINAL (within about 1σ of its bar, or passing only under a declared floor) / NS (not scorable, or not scored under B) / UNDECIDED.

## (1) Galactic dynamics

| id | observable | status 2026-09-29 (B) | since GATES.md (derived rule in *italics*) | evidence | verified |
|---|---|---|---|---|---|
| 1.01 | SPARC RAR | PASS (ν_mono 0.1003 / 0.0991) | *SPARC LSBs spared, S ≡ L (100%); SPARC dwarfs f_ex = 0 in all 110; SPARC +0.0009 dex with the rule (CFG39, already in GATES.md)* | CFG58 (3371b14ac), CFG42 (67c170fe7) | re-run: reproduced, re-run: reproduced |
| 1.02 | RAR intrinsic scatter | met | none | CFG4_galaxy_law.py | reported (GATES.md) |
| 1.03 | a₀ normalisation vs g† | PASS | none (see 3.11) | CFG4_galaxy_law.py, CFG1 | reported (GATES.md) |
| 1.04 | BTFR | met | the top of the mass function is new row 1.25 | CFG4_galaxy_law.py | reported (GATES.md) |
| 1.05 | kernel shape | ν_mono PASS; P2 ~2σ | none | CFG14 | reported (GATES.md) |
| 1.06 | halo surface density | met | none | CFG4_galaxy_law.py | reported (GATES.md) |
| 1.07 | MW classical dSphs | PASS 1.06 / 0.74 | *the rule over-predicts them, −1.78 / −1.90σ* | CFG42 (67c170fe7) | re-run: reproduced |
| 1.08 | M31 dSphs (LVD, Collins) | MARGINAL (1.21–1.63σ) | ***FAIL under the rule: M31 LVD −2.67σ**; Collins −0.02 (fine); the only one of seven gates the sum fails in the rule-readings harness* | CFG42, CFG45 (5518cfcd0) | re-run: reproduced, re-run: reproduced |
| 1.09 | MW ultra-faints | **FAIL** (refereed 3.8 / 3.5σ, 40 objects) | Binary-corrected dispersions on 8 systems: +0.21 (1.26σ, f free) against 1.8σ uncorrected on the same 8, so mostly lost power; 7 of 8 stay positive (CFG46). Multi-epoch, binary-cleaned: Boötes I +0.22 (2.46σ), Tucana II +0.47 (3.63σ), two objects (CFG51). *The rule closes the population offset (−0.06, −0.41σ; CFG42) but over-predicts the corrected set (−0.15, −1.17σ) and the cleaned pair (−0.21, −0.17).* | CFG46 (e6ecfd6ff), CFG51 (d7e6a6565), CFG42 | re-run: reproduced, re-run: reproduced, re-run: reproduced |
| 1.10 | LV dwarfs, statistic C | PASS 1.71 / 1.71 | statistic C passes under L and S; LV field dwarfs L −1.4 / −1.3σ (pass); ***S −3.47 / −2.70σ (FAIL)**; S switches off above M_b ≈ 2.3e7* | CFG58 | re-run: reproduced |
| 1.11 | cluster-infall BTFR | PASS | none | CFG7_hierarchy_fg001.py | reported (GATES.md) |
| 1.12 | tidal dwarfs | PASS (ownership exempt) | the blind, non-exempt version fails under L and S (change 0.000 dex): the pass rests on ownership | CFG58 | re-run: reproduced |
| 1.13 | outer-halo GCs | PASS (does not discriminate) | none | CFG7_hierarchy_fg001.py | reported (GATES.md) |
| 1.14 | NGC 1052-DF2 / DF4 | PASS at 20 Mpc (CONT distance) | the blind version fails under L and S (change 0.000): the pass rests on ownership | CFG58 | re-run: reproduced |
| 1.15 | Chae external-field signal | **FAIL** (refit 1.7–3.0σ) | none | CFG7 H7, CFG8 | reported (GATES.md) |
| 1.16 | Coma UDGs | PASS 1.33 / 1.11σ | *S = L (spared)* | CFG31; CFG58 | re-run: reproduced |
| 1.17 | binary galaxies | UNDECIDED (orbit-degenerate) | none | CFG30 | reported (GATES.md) |
| 1.18 | X-ray ellipticals | MARGINAL / FAIL (1.70 / 1.58σ) | *the rule 1.04σ (CFG36, in GATES.md)*; the hot-gas test's criteria are frozen but it has not run (no gas profiles in the repo; the fetch awaits the owner) | CFG32, CFG36; CFG57 (78a5a3a0a, criteria only) | reported (GATES.md); CFG57 not run |
| 1.19 | SLACS lensing vs dynamics | MARGINAL (1.5–1.7σ with the floor) | none | CFG33 | reported (GATES.md) |
| 1.20 | SLUGGS massive early types | **FAIL**, robust to the IMF: +0.080 (3.3σ) with SLUGGS masses; **+0.097 ± 0.024 (4.0σ; alt 3.65σ) with each galaxy's own JAM-calibrated stellar mass** (16 of 19) | ***the rule's pass does not survive dynamical masses:** +0.007 (0.4σ) with SLUGGS masses → +0.046 (2.6σ) with JAM masses (1.9σ under the Hernquist convention; 2.5σ without NGC 7457)*. No single debris fraction reconciles SLUGGS (φ ≥ 0.81) with M31 LVD (φ ≤ 0.30) (CFG59) | CFG55 (791083f7f), CFG59 (3371b14ac) | re-run: reproduced, re-run: reproduced |
| 1.21 | passive disks, 16 ATLAS3D + HI | PASS (+0.026, 0.3σ) | none (f_ex = 0 in all 16) | CFG37 | reported (GATES.md) |
| 1.22 | massive S0 / late spirals under the rule | law consistent | *the rule still over-predicts UGC 2487 (+0.139 dex); on four S0/S0a with HI to 30–97 kpc it is −0.105 ± 0.131 (0.8σ), and by outer-curve shape −1.22 / −1.04σ with power 0.98σ (cannot decide); together −1.25σ against the rule. Every measurement leans against the debris; none reaches 2σ* | CFG41 (42c87ead1), CFG53 (6a48c4e2e) | re-run: reproduced, re-run: reproduced |
| 1.23 | Milky Way | NS | none | CFG1 | reported (GATES.md) |
| 1.24 | environmental null | consistent | none | CFG6 | reported (GATES.md) |
| **1.25 NEW** | super spirals (Ogle+2019, 23; top of the disk mass function) | **MARGINAL / FAIL** | All 23: +0.105 ± 0.063 (1.67σ, with Simard+2011 bulges). **The nine fastest: +0.164 (2.34σ; H2 failed as declared).** Trend +0.166 (1.80σ). The point-mass escape is refuted; the 0.2-dex stellar-mass floor is the limit. *The rule cannot help (f_ex = 0 in all 23).* | CFG40 (e773982cd), CFG56 (33e1af197); referee 071301aab | re-run: reproduced, re-run: reproduced |
| **1.26 NEW** | massive HI disks (Di Teodoro+2023, 15, HI to 30–97 kpc) | PASS (law −0.028 ± 0.066 after the width-selection correction) | the law fits the blue disks' outer shapes (0.9σ) | CFG41, CFG53 | re-run: reproduced, re-run: reproduced |

## (2) Groups and clusters

| id | observable | status 2026-09-29 (B) | since GATES.md | evidence | verified |
|---|---|---|---|---|---|
| 2.01 | X-COP identity at 0.8 R500 | PASS 0.946 ± 0.080 | none | CFG4_clusters.py | reported (GATES.md) |
| 2.02 | Bullet Cluster | PASS 4.6× / 4.9× | none | CFG4_clusters.py | reported (GATES.md) |
| 2.03 | Lovisari X-ray groups | R500 MARGINAL; R2500 FAIL (2.57 / 2.63σ) | none | CFG34 | reported (GATES.md) |
| 2.04 | Local Group R0 | FAIL (3.0–4.8σ; not framework-specific) | none | CFG20, CFG23 | reported (GATES.md) |
| 2.05 | Harvey collisions; cluster counts | NS | none | CFG1 | reported (GATES.md) |

## (3) Cosmology and lensing

| id | observable | status 2026-09-29 (B) | since GATES.md | evidence | verified |
|---|---|---|---|---|---|
| 3.01 | CMB TT/TE/EE | met by construction | none | CFG4_cosmology.py | reported (GATES.md) |
| 3.02 | CMB lensing | PASS with the bound-only switch | none | CFG4_switch.py | reported (GATES.md) |
| 3.03 | growth, S8, RSD | met by allowance | none | CFG4_cosmology.py | reported (GATES.md) |
| 3.04 | BAO, P(k) | unchanged by construction | none | CFG4_cosmology.py | reported (GATES.md) |
| 3.05 | KiDS isolated lenses | PASS at x_e = 0.4 | none | CFG4_switch.py, CFG16 | reported (GATES.md) |
| 3.06 | cold budget | lenient PASS; strict FAIL (reported) | none | CFG4_target.py, CFG39 | reported (GATES.md) |
| 3.07 | budget vs KiDS | FAIL as declared; not decidable | none | CFG24, CFG27 | reported (GATES.md) |
| 3.08 | KiDS + LG shared edge | FAIL (not framework-specific) | none | CFG21–23 | reported (GATES.md) |
| 3.09 | density edge x_e | declared 0.4 | CFG48's referee note: CFG48's maximal-ball gate places a baryon-only edge at 0.11–0.24 r_ta against B's committed (phantom-inclusive) r_ta, below the window | CFG48 G2; 35eebbe99 | referee-reproduced (35eebbe99) |
| 3.10 | a₀(z) at z ≈ 2.5 | **NS (still)** | At z ≥ 1.5 no clean object on disk has g_bar < 0.3 a₀. Pooled z ≥ 1.5 g_bar < a₀ (N = 14): flat +1.0σ, rival −0.3σ, absorbed by a selection mock. PHIBSS: N = 0 at the frozen velocity radius. A decisive test needs 2–4 JWST IFU + ALMA discs at z ≈ 2.5 with mass calibration ≲ 0.1 dex. | CFG52 (9ffb95d57), CFG54 (8b6473b7a) | re-run: reproduced (no MUTATE output committed), re-run: reproduced |
| 3.11 | a₀ = κ c √(Gρ_Λ) | consistent; κ FITTED | The Unruh / de Sitter matching route to κ is retired (n = 2 gives κ = 1.447, 12.9σ from the BTFR κ). Reported, not re-run: like-for-like on H₀, κ = ½ and 1/2π are indistinguishable (97f30b36c). | CFG47 (1c375b449 → 4dfa7d995); 97f30b36c | re-run: reproduced; 97f30b36c reported |
| 3.12 | Lyman-α forest | PASS 0.00 | none | CFG4_switch.py | reported (GATES.md) |
| 3.13 | cosmic shear, JWST, Li-7, BBN, τ | NS | none | CFG1 | reported (GATES.md) |

## (4) Local and relativistic

| id | observable | status 2026-09-29 (B) | since GATES.md | evidence | verified |
|---|---|---|---|---|---|
| 4.01 | Cassini, ephemeris | PASS via ownership (effective law) | At the action level, every monotone local gate functional (E < 0, U, θ ≤ 0) is ON at the Sun (U_sun/U_MW = 9e16); the top-level-ball functional removes the Sun's own phantom (PARTIAL). The effective-law status is unchanged. | CFG48 G2 (0dba13349) | referee-reproduced (35eebbe99) |
| 4.02 | GW170817 | NS (no action) | none | — | reported (GATES.md) |
| 4.03 | lensing = dynamics | NS as derivation | none | XR3 | reported (GATES.md) |
| 4.04 | full PPN | NS for B | none | KM3 | reported (GATES.md) |
| 4.05 | wide binaries DR3 | CONT | none | CFG1 | reported (GATES.md) |
| 4.06 | wide binaries DR4 (2 Dec 2026) | NS until DR4 | Amendment 15 FILED (9f60163d3). Amendment 16 is a DRAFT, not filed (59e383ff3). | prep_2026/gaia_dr4_prep | reported |
| 4.07 | external-field effect | CONT | none | CFG1 O6 | reported (GATES.md) |
| 4.08 | preferred frame | NS | none | KM1 | reported (GATES.md) |

## (5) Theory consistency (an action for B)

| id | requirement | status 2026-09-29 | since GATES.md | evidence | verified |
|---|---|---|---|---|---|
| 5.01 | one explicit action | **FAIL / OPEN: no action produces B** | **Gap 3 partly filled:** the a₀–Λ tie acts on a conserved fluid's stress cap at no cost in local degrees of freedom, but a barotropic cap is excluded. **Gap 2 is a scoped no-go** that reduces to Gap 1's enclosed-mass object; the tidal-tensor closure fails reciprocity. **Gap 1 is a scoped no-go:** Gauss (a flux-gated field gives M_dyn = M_b beyond the edge), history (acausal inside an action, or a label as initial data), and the exchange's reaction (0.06–22 g_law; energy 23–50× the baryons' orbital kinetic energy, 18–179× under the committed r_ta). CFG49 (gate scalar) is not yet committed. | CFG43 (e42a98572), CFG44 (513ee4b28), CFG48 (0dba13349) + referee 35eebbe99, CFG50 (bb2a7b680) | re-run: reproduced, re-run: reproduced, re-run: reproduced (MUTATE=a fails D1, MUTATE=b fails D2, as its README declares); CFG48 referee-reproduced |
| 5.02 | stability (no ghost or gradient instability) | FAIL as varied (V0 region gate) | **A nonlocal enclosed-mass (Volterra) gate that reads baryon mass has no negative mode on 48 of 48 DE12 layers** (η_crit ≥ 13.7; referee-reproduced 96/96 with an independent grid and eigensolver). The dynamical-mass reading is unstable on 29 of 48 (every z ≤ 1 layer). This is a second-variation statement only: the first variation (an edge potential step of 0.2–8 c_s²) is not fed back. | CFG48 G6 | referee-reproduced (35eebbe99) |
| 5.03 | strong coupling G8 | bounded pass (frozen-background scope) | none | XC1, XC3, XC6 | reported (GATES.md) |
| 5.04 | Cauchy problem, causality | partial | none | XC2, XC5 | reported (GATES.md) |
| 5.05 | N_grav = 2 | orphaned | none | XR3 | reported (GATES.md) |
| 5.06 | matter conservation (Noether) | NS | the Noether identity for a gated MOND field is exact; its reaction on the baryons is 0.55–2.2 of their weight on DE12's layers | CFG48 G1 | referee-reproduced |
| 5.07 | GW c_T = c, one metric | c_T = 1 in the reduced sector | none | XR3 | reported (GATES.md) |
| 5.08 | zero-field limit | partial | none | XC2, XC5 | reported (GATES.md) |
| 5.09 | Newton/GR recovery | orphaned | none | XR3 | reported (GATES.md) |
| 5.10 | FLRW growth | partial | none | CV2 | reported (GATES.md) |
| 5.11 | dark mass as a state of the framework's field | **OPEN** | The exact target is derived: ρ_c g_tot = a₀ M_b(<r)/(4πr³), with the point-mass identities in Lean. No action derives it. Survivors are restatements only: a temperature-slaved fluid postulating the BTFR, and a locally virialised collisionless fluid with a postulated anisotropy. | CFG44 | re-run: reproduced |
| 5.12 | inner cold component | open requirement | CFG44's target gives the inner profile exactly for P2 (ν_mono departs by up to 2%) | CFG44 | re-run: reproduced |
| 5.13 | a₀–Λ relation | declared input; κ FITTED | the tie written into a fluid's stress cap (CFG43); the Unruh route retired (CFG47) | CFG43, CFG47 | re-run: reproduced, re-run: reproduced |

## Re-verification log (clean export of HEAD a628e8a66; each script in every mode that has a committed output)

Every run's output matched its committed file line for line (timing stripped); `diff` counts differing lines; `rc` is the exit code, which equals the one each lane records (1 where a declared hypothesis or MUTATE control fails). CFG48 was re-verified separately (referee note 35eebbe99). CFG49 (gate scalar) is not committed and is not included.

```
CFG40_super_spirals.py [main] rc=1 diff=0
CFG40_super_spirals.py [MUTATE1] rc=1 diff=0
CFG41_massive_spirals_hi.py [main] rc=1 diff=0
CFG41_massive_spirals_hi.py [MUTATE1] rc=1 diff=0
CFG41_selbias_mc.py [main] rc=0 diff=0
CFG42_satellites_rule.py [main] rc=1 diff=0
CFG42_satellites_rule.py [MUTATE1] rc=1 diff=0
CFG45_rule_readings.py [main] rc=1 diff=0
CFG45_rule_readings.py [MUTATE1] rc=1 diff=0
CFG46_ufd_binary_corrected.py [main] rc=1 diff=0
CFG46_ufd_binary_corrected.py [MUTATE1] rc=1 diff=0
CFG51_walker_ufd.py [main] rc=1 diff=0
CFG51_walker_ufd.py [MUTATE1] rc=1 diff=0
CFG53_passive_disk_shapes.py [main] rc=1 diff=0
CFG53_passive_disk_shapes.py [MUTATE1] rc=1 diff=0
CFG54_phibss_a0z.py [main] rc=1 diff=0
CFG54_phibss_a0z.py [MUTATE1] rc=1 diff=0
CFG55_sluggs_dynamical_masses.py [main] rc=1 diff=0
CFG55_sluggs_dynamical_masses.py [MUTATE1] rc=1 diff=0
CFG56_super_spirals_bulge.py [main] rc=1 diff=0
CFG56_super_spirals_bulge.py [MUTATE1] rc=1 diff=0
CFG58_rule_more_populations.py [main] rc=1 diff=0
CFG58_rule_more_populations.py [MUTATE1] rc=1 diff=0
CFG59_universal_debris_fraction.py [main] rc=0 diff=0
CFG59_universal_debris_fraction.py [MUTATE1] rc=1 diff=0
CFG43_fluid_tie/A1_action_field_equations_dof.py [main] rc=0 diff=0
CFG43_fluid_tie/A1_action_field_equations_dof.py [MUTATE1] rc=1 diff=0
CFG43_fluid_tie/A1_action_field_equations_dof.py [MUTATE2] rc=1 diff=0
CFG43_fluid_tie/A2_frw_flat_a0_and_dust_limit.py [main] rc=0 diff=0
CFG43_fluid_tie/A2_frw_flat_a0_and_dust_limit.py [MUTATE1] rc=1 diff=0
CFG43_fluid_tie/A2_frw_flat_a0_and_dust_limit.py [MUTATE2] rc=1 diff=0
CFG43_fluid_tie/A3_cap_entry_form_and_obstruction.py [main] rc=0 diff=0
CFG43_fluid_tie/A3_cap_entry_form_and_obstruction.py [MUTATE1] rc=1 diff=0
CFG43_fluid_tie/A3_cap_entry_form_and_obstruction.py [MUTATE2] rc=1 diff=0
CFG44_fluid_target/B1_target_and_hydrostatics.py [main] rc=0 diff=0
CFG44_fluid_target/B1_target_and_hydrostatics.py [MUTATE1] rc=1 diff=0
CFG44_fluid_target/B2_barotropic_nogo.py [main] rc=0 diff=0
CFG44_fluid_target/B2_barotropic_nogo.py [MUTATE1] rc=1 diff=0
CFG44_fluid_target/B3_local_closures.py [main] rc=0 diff=0
CFG44_fluid_target/B3_local_closures.py [MUTATE1] rc=1 diff=0
CFG44_fluid_target/B4_actions_reciprocity.py [main] rc=0 diff=0
CFG44_fluid_target/B4_actions_reciprocity.py [MUTATE1] rc=1 diff=0
CFG47_unruh_matching/CFG47_unruh_matching.py [main] rc=0 diff=0
CFG47_unruh_matching/CFG47_unruh_matching.py [MUTATE1] rc=1 diff=0
CFG47_unruh_matching/CFG47_unruh_matching.py [MUTATE2] rc=1 diff=0
CFG52_a0z_feasibility/feas.py [main] rc=0 diff=0
CFG52_a0z_feasibility/mock_bias.py [main] rc=0 diff=0
CFG52_a0z_feasibility/pooled.py [main] rc=0 diff=0
CFG50_tidal_closure/D1_action_reciprocity.py [MUTATE=0] rc=0 diff=0
CFG50_tidal_closure/D1_action_reciprocity.py [MUTATE=a] rc=1 diff=0
CFG50_tidal_closure/D1_action_reciprocity.py [MUTATE=b] rc=0 diff=0
CFG50_tidal_closure/D2_wellposed_nogo.py [MUTATE=0] rc=0 diff=0
CFG50_tidal_closure/D2_wellposed_nogo.py [MUTATE=a] rc=0 diff=0
CFG50_tidal_closure/D2_wellposed_nogo.py [MUTATE=b] rc=1 diff=0
```

## Addendum, 2026-09-29, after CFG67 and CFG68 (appended; the rows above are unchanged)

- **Row 1.25 (super spirals): SHARED by standard halos.** Through CFG56's exact machinery, ΛCDM with Mandelbaum's blue halos also misses the nine fastest: +0.121 dex, z₉ = 2.26 against the law's +0.164, z₉ = 2.34.
  - CFG68's H1 failed as declared.
  - The verdict depends on the halo relation (Moster over-predicts) and on the lensing error at these masses (the +1σ halos pass).
  - Source: CFG68, 358564486. Its criteria were frozen in 1808d8bee, and its main and MUTATE runs were re-run by this session.
- **The new KiDS colour-split failure (next to gate 3.05): B-SPECIFIC.**
  - CFG61 (3c03f9678) gives ~3.7σ, which is a reported χ² row (LEDGER CFG61-note).
  - ΛCDM reproduces the split through the same machinery: χ² 6.5/7 with colour-split halos and 6.9/7 with colour-blind Moster halos (CFG67, f1df7889a).
  - The failure belongs to B's mass-independent dark mass, not to the machinery.



## Corrections, 2026-09-29, after a referee sweep and CFG57 (appended; the rows above are unchanged)

- **Line 23 and row 1.20, "no single fraction of its debris reconciles the populations".** This is true at the frozen 1σ-per-population acceptance.
  - At 2σ, CFG59's ten populations share φ in [0.52, 0.71] (canonical) and [0.33, 0.66] (alt).
  - With CFG71's dynamical SLUGGS, the 2σ intersection is empty only because of SLUGGS (2.6σ at φ = 1).
  - Source: CFG75, e17cf2cf8.
- **Row 1.18 cited CFG57 as its hot-gas test, but CFG57's frozen question is the SLUGGS deficit (row 1.20).**
  - CFG57 has now run (9b071a024; data d409c19be) and is non-diagnostic by its frozen map.
  - The measured hot gas moves the law's SLUGGS mean by 0.010 dex: +0.163 → +0.153 ± 0.028, which is 5.4σ on the seven covered galaxies (alt 5.1σ). It moves the rule's mean to +0.066 (3.0σ).
  - Row 1.20 stands: the measured gas cannot close the deficit. Gas beyond the X-ray fields is untested (M87's GCs reach 109 kpc against a 30-kpc field).
  - Re-run status: this session only.
- **The addendum's "KiDS split B-SPECIFIC" is about the early-minus-late difference.** The same machinery's absolute profiles fail for ΛCDM too (CFG67 H3: 29.6 and 27.9/7).


## Addendum after CFG76 (appended 2026-09-29; the rows above are unchanged)

- **Line 22 and row 1.20: the SLUGGS significances rest on a fixed GC density slope, γ = 3.** This comes from CFG76 (276c78784, post hoc).
  - The law's JAM-calibrated offset is +0.017 (0.7σ) at γ = 2.0 and +0.134 at 3.6. It is zero at γ ≈ 1.83. The rule's offset is zero at γ ≈ 2.45.
  - Without the four group and cluster centrals (N = 12), the law is at +0.055 (2.7σ) and the rule at +0.026 (1.3σ).
  - Row 1.20 stays FAIL at γ = 3 as run, with this qualifier. The "2.6σ at φ = 1" in the corrections above is the same γ = 3 number.
- **h50's name-key artefact drops NGC 720 and NGC 821.** A disclosed re-run of CFG55 (`CFG55_h50_keyfix.py`) corrects the keys: the JAM sample of 17 gives law +0.0996 (4.3σ) and rule +0.0513 (2.9σ). It was re-run independently by CFG76 (+0.100 / +0.053) and by this session.


## Clarification to row 3.10 (appended 2026-09-29; the row above is unchanged)

- **"A decisive test needs 2–4 JWST IFU + ALMA discs at z ≈ 2.5 with mass calibration ≲ 0.1 dex"** paraphrases CFG52 (9ffb95d57). It applies to flat a₀ against a₀ ∝ H(z).
  - CFG52's own sentence: 2–4 discs with 5–10% velocity errors and independent mass errors of 0.1–0.2 dex would give 3σ, but a correlated mass-scale systematic caps the test near 2.3σ whatever the sample size. So the calibration must reach about 0.1 dex.
  - **Against ΛCDM-native (+0.334 dex) the cap is 1.3σ** at the 0.25-dex floor. Reaching 3σ there needs the floor to fall to about 0.11 dex (CFG63 7b8640ded).


## Corrections at adoption (appended 2026-09-29; the rows and addenda above are unchanged; this addendum supersedes them where they differ)

- **The KiDS split** (the CFG67/CFG68 addendum's "The failure belongs to B's mass-independent dark mass, not to the machinery"): the KiDS early/late lensing split is B-SPECIFIC relative to the ΛCDM comparator, for the early-minus-late difference only. It is shared by any model whose predicted difference at fixed g_bar is negligible, NOT by every colour-blind model (a colour-blind Moster halo fits it at 6.9/7, CFG67). It is robust to the repo's own jackknife covariance (4.4σ in the 1-halo bins, CFG88 ef7c1d303) and to a twice-stricter isolation (4.1σ, amplitude 0.97 ± 0.19, CFG96 d2e97eb53); reduced but not removed by B's own stellar-mass calibration (2.8σ released / 3.6σ jackknife, CFG95 7214b5c62); fragile only to systematics a jackknife cannot see.
  - The law's χ² is the zero-model χ² (CFG77 a736715f8).
  - ΛCDM's absolute profiles fail in the same machinery too: 29.6 and 27.9/7 (CFG67 H3).
- **Row 1.08.** M31 LVD's −2.67σ depends on the error recipe: −2.67 / −1.74 / −1.97 / −1.49σ across four recipes, and −1.49σ under CFG91's frozen one (CFG91 abb698467).
- **Row 1.09.**
  - The rule's −0.15 (−1.17σ) on the binary-corrected set is a clamp artefact: the collapse-mass floor used there is 0.013, against CFG42's 0.133 (CFG78 9e7f778bc).
  - The luminosity ordering is not detected on the 40 objects and only flagged on 8 (CFG83 b41ca5f55).
- **Row 3.10** (CFG90 0137d584d):
  - CFG52's counts reproduce only with its undocumented conventions.
  - The pooled N = 14 (flat +1.0σ, rival −0.3σ) excludes the +1.14-dex object GS4 01529. Keeping it gives flat +0.17 to +0.22 dex and flips the rival's sign.
  - PHIBSS's N = 0 is a knife-edge on an assumed velocity radius (lowest g_bar/a₀ = 1.097).
- **Row 5.01, "a barotropic cap is excluded", overstates.** A barotropic saturating cap is a scoped screening result. In CFG43's own referee paragraph the window is convention-dependent, from about 11× up to 10⁴–10⁵ in mass (CFG43 README).


## Addendum after CFG99 (appended 2026-09-29; the rows above are unchanged)

- **Row 3.10: the a₀(z) test is NOT FEASIBLE from the KMOS3D cubes** (CFG99, run as CFG89; criteria 6eb7ae539, lane 029968534).
  - A first Hα extraction from all 739 cubes measures rotation out to a median 0.6″ (4.9 kpc; 1.5 R_e; 1.3 PSF FWHM) at z ≥ 1.9.
  - Of 74 clean discs, only 2 (canonical) and 3 (alt) have g_bar < a₀ at the last measured radius, against a gate of 5. The median disc is at g_bar ≈ 4 a₀.
  - The count moves with the model gas: 1 to 8 across its factor-2 bracket.
  - The velocities there come back about 28% low in injection tests (beam smearing; declared control C1c failed and kept).
  - With the table-based lanes (CFG52, CFG54, CFG90), the on-disk data cannot run the z ≈ 2.5 test. It needs deeper or higher-resolution data with measured gas.


## Addendum after CFG110 (appended 2026-09-29; the rows above are unchanged)

- **The KiDS rows (next to gate 3.05):** Within colour classes the KiDS 1-halo lensing signal shows no detectable dependence on stellar mass. B's mass-independence gives 22.2/14 (p 0.075) and the colour-split ΛCDM 25.2/14; the two are not discriminated (power 8.8, below the declared 9). The colour-blind Moster ΛCDM is rejected (105/14). So, relative to the colour-blind ΛCDM, B and ΛCDM each fail one KiDS test; relative to the colour-split ΛCDM, the colour split stays B-specific. The signal depends on type, not on mass within a type. All of this is at the re-measurement's jackknife errors; satellites and calibration systematics are not covered (CFG110 2f05b5303). The reading that B gets the mass-independence right rests on a non-detection in a power-limited test.


## Addendum after CFG111 (appended 2026-09-29; the rows above are unchanged)

- **Row 1.20, SLUGGS:** With each SLUGGS galaxy's published GC density slope in place of the fixed γ = 3, the law's JAM-calibrated deficit stays at 3.6σ (alt 3.2σ; 2.2σ without the four centrals). The slopes come from Alabi+2017's literature relation, γ 2.49–3.43, verified against its Table 1. The γ that would null the massive centrals is far below their published values: NGC 4365 needs 1.06 against 2.56, and no γ ≥ 1 nulls M87. So the γ caveat does not rescue the law. B's derived rule fits with the same slopes: 1.55σ (alt 1.64σ), and −0.66σ with population masses. Isotropic orbits are assumed (CFG111 6e1b04092).


## Correction after CFG100 (appended 2026-09-29; the rows above are unchanged)

- **The KiDS rows (the CFG110 addendum above):** CFG100 (a51dfe756) is an independent re-derivation of CFG110 and reproduces every headline: B 22.20/14 (p 0.0746), colour-split ΛCDM 25.16, colour-blind Moster 105.04, power 8.77. It corrects the reading in three ways. (1) 'B gets the mass-independence right' is not supported; only a non-rejection is. The 14-dof test has power 0.41 against ΛCDM-size mass dependence and 0.11 against half of it. The sharper 1-dof amplitude is A = 0.33 ± 0.34, so ΛCDM-size dependence is disfavoured at about 2σ (statistical only) and half of it is not excluded. Read: B is not rejected, and ΛCDM-size mass dependence within a class is disfavoured at about 2σ. Likewise 'not on mass within a type' means no detectable dependence at this power. (2) B and the colour-split ΛCDM are not discriminated. B's p ranges from 0.005 to 0.08 across the mass-split edges, and the order flips: B is better at q25/q75, ΛCDM at q40/q60. Dropping late-class bin 9 makes ΛCDM beat B (p 0.88 vs 0.31). The power of 8.8 against the threshold of 9 is razor-thin (10.35 with pair weights). (3) Only the colour-blind Moster rejection is robust: it holds through the bin set and ×1.5 errors. Its size is not robust: χ² 49–230 for M* ± 0.1 dex, and 79 with M200m. It also rests on the Moster mapping as coded. The jackknife has no photo-z, intrinsic-alignment or satellite terms.


## Addendum after CFG112–CFG114 (appended 2026-09-29; the rows above are unchanged)

- **Row 1.20, SLUGGS, GC orbits and the joint degeneracy (CFG113 1db2d3a69, CFG114 2a83f369e). At the published slopes, any constant GC anisotropy in the measured range (β −0.5 to +0.5) leaves the law's deficit at 3.4σ or more (alt 2.9σ), and no β < 1 nulls it. But with slopes and orbits varied together, it falls below 2σ at the corner where both are favourable: every γ_i − 0.4 with β = +0.5 gives 0.6σ (alt 0.1σ). That corner is more radial than any measured GC system. The deficit exceeds 2σ in 23 of the 25 cells (alt 21). The rule is conditional in the opposite corner: it fits in 13 of 25 cells and fails wherever the slopes are 0.2 or more steeper than published (2.1–3.5σ). So SLUGGS alone cannot make either reading clean. Measured GC slopes and anisotropy for M87, NGC 4365, NGC 4374 and NGC 5846 would decide it.**
- **The derived rule's support:** CFG111–CFG113 qualify the line 'The derived rule has no clean support left'. With published GC slopes the rule fits SLUGGS on its own (1.55σ with JAM masses, −0.66σ with population masses), and it keeps fitting for isotropic or radial GC orbits (0.56σ at β = +0.5). But one debris fraction still does not fit all ten populations at 2σ: SLUGGS's window [0.77, 1] misses the other nine's [0.23, 0.71] by 0.06 in φ (alt 0.11), with the M31 LVD binding (CFG112 670356510). That NO is fragile. It opens if every γ_i is lowered by 0.2 or with SLUGGS's population masses, and radial orbits were not tested in it. The line's clause 'not with dynamical SLUGGS masses' therefore stands, narrowly. The 1σ NO and the satellite failures do not depend on SLUGGS.
