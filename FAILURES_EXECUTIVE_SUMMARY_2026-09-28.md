# The framework's largest-σ failures — executive summary (2026-09-28)

Every row is quoted from a committed file, named in the last column. A σ is given as the source states it.

The four tables separate four very different things:
- **A.** failures of the **current best version**;
- **B.** liabilities recorded against an **earlier reading** and never re-scored;
- **C.** the kills that **ended earlier constructions**;
- **D.** big numbers that were **withdrawn or shown not to be framework-specific**.

Mixing them overstates or understates the damage.

"The current best version" is **candidate B**: CFG4's target law plus FG001's hierarchical ownership, with κ = ½ fitted. It passes 42 of the 48 gates in the programme's harness (`campaign_fresh_gravity/CFG19_harness_rescore_results.json`).

## Bottom line

1. **The largest standing failure of the current version is the Milky Way's ultra-faint dwarfs: real, and 3.5–3.8σ once refereed** (CFG28), not the first-quoted 7.5–8.0σ. The other scored one is Chae et al.'s external-field signal: 4.1–4.3σ in their fits, 1.7–2.2σ refit under the framework's own law.
2. **Binary galaxies, the biggest unscored risk, are now scored (CFG30), and they do not discriminate.**
   - The "1.8–1.9× too fast" result assumed circular orbits.
   - Under B's own timing orbits (pairs still falling in, no halo friction), the mean speeds come out right: A = 1.05–1.12. ΛCDM's halos then over-predict. Under circular orbits it is the reverse.
   - Neither law's simple orbit model fits how the speeds fall with separation or rise with mass.
   - The timing reading also makes the Local Group 1.6–1.75× too fast.
   - Which orbits apply turns on whether B's dark component exerts dynamical friction, and B must specify that.
3. **The dark sector carries 5–7σ tensions** (the cold budget against KiDS lensing; KiDS against the Local Group). They are real in the programme's machinery but not decisive: standard ΛCDM halos fail the same machinery by as much or more.
4. **The largest numbers in the record killed earlier constructions, not the current one:** 43,479σ, 21σ, 15.6σ, 13–34σ, 9σ and 8.5σ.
5. **The Coma ultra-diffuse galaxies pass under B's own rule (CFG31).**
   - They sit at 1.3 / 1.1σ, not the recorded 4.9σ. That number belonged to the external-field reading B dropped.
   - The pass is only as strong as B's ownership rule, which Gaia DR4 tests.
6. **Several famous big numbers are withdrawn or overstated:** Lyman-α "6–8σ", Coma "19.4σ", MUSE "12–16σ" and SPARC-vs-P2 "> 99.9%". Never cite them as failures.

## A. The current best version (candidate B): scored failures, largest first

| # | failure | significance | status | source |
|---|---|---|---|---|
| A1 | Milky Way ultra-faint dwarf satellites | **3.8σ / 3.5σ** after the adversarial referee (CFG28: the 9 dropped upper limits restored, a systematic floor added); first quoted as 7.97 / 7.52σ, statistical only | **standing and real, but overstated before**: tides, noise and binaries do not explain it. Binaries are bounded by the published simulations (CFG29): the offset persists where binaries are weakest, and Eridanus II and Ursa Major I exceed any binary ceiling. The external-field reading fails them at 13σ | `CFG7_hierarchy_fg001*`, `CFG18_satellite_infall_gas*`, `CFG28_ufd_referee*`, `CFG29_ufd_binary_audit*` |
| A2 | cold budget vs KiDS-1000 lensing (the phantom's edge) | **5.4–5.7σ** canonical, **6.7–7.0σ** alt (Δχ² 29.4–49.3 against KiDS's own best) | **not decidable** with this machinery: it misfits standard ΛCDM halos by Δχ² ≥ 50 | `CFG24_budget_associations*`, `CFG27_edge_thread_closure*` |
| A3 | a universal phantom edge vs KiDS + the Local Group's zero-velocity radius | **5.1–7.1σ** (sharp edge), 5.5–7.4σ (soft edge) | **not framework-specific**: standard ΛCDM halos in the same test score T = 24.5–72.5 against the framework's 26–28 | `CFG21_kids_lg_joint*`, `CFG22_soft_edge*`, `CFG23_lcdm_control*` |
| A4 | Chae et al.'s external-field signal (D1 / D2) | **4.08σ / 4.29σ** in their fits; **1.7–2.2σ** canonical (2.7–3.0σ alt) refit under the framework's own law | **standing, reduced** | `CFG7_hierarchy_fg001*`, `CFG8_chae_kernel*` |
| A5 | Local Group zero-velocity radius at KiDS's floor edge | **3.0–4.8σ** | not framework-specific (A3) | `CFG20_lg_edge*`, `CFG23_lcdm_control*` |
| A6 | the kernel P2's transition shape vs SPARC | **~2σ** (p ≈ 0.03) canonical | the contract kernel ν_mono is fully consistent | `CFG14_shape_calibration*` |
| A7 | the strict cold budget at x_e = 0.4 (reported row) | Ω_ph 0.229 vs 0.159 | reported, not scored; superseded by A2's association-level budget | `CFG19_harness_rescore_results.json` |
| A8 | the edge derived from infall (splashback, FG016) | 0.18–0.27, below the window [0.31, 0.48] | its KiDS kill is **not framework-specific** | `CFG7_edge_fg016*`, `CFG25_fg016_lcdm_control*` |

## B. Liabilities recorded against the earlier phantom-only reading, never re-scored under candidate B

These come from the 2026-09-03 sweep (`predictions_2026/SECOND_LAW_HUNT_2026.md`, scripts in `hunt_2026/`). That sweep scored the phantom-only reading with the host's external field. Candidate B changes that reading in two ways:
- it adds a cold component (clusters and baryon-rich systems keep the cosmic share);
- it drops the external field for top-level systems.

| # | item | recorded | what candidate B changes | status |
|---|---|---|---|---|
| B1 | **binary galaxies** | external-field branch **26σ**. Isolated two-body branch: pairs move **1.5–1.8×** faster than predicted (+0.25 dex), **5.4σ** in the strictest-isolation shell; ΛCDM gives A = 0.90–1.06 | **Re-scored (CFG30).** With circular orbits, even the most generous baryons leave A = 1.51 / 1.44 (12.9 / 11.7σ). But the circular model fails the data's own separation profile for both laws (6.5σ, 5.4σ). B's own timing orbits give A = 1.12 / 1.05 (1.06 / 0.99 after the estimator's bias), and ΛCDM's halos then over-predict (0.46). The timing reading leaves three tensions: the profile (4.2σ), the mass trend (5.3σ; ΛCDM misses it by 4.7σ the other way) and MW–M31, 1.6–1.75× too fast | **orbit-degenerate, not an established failure.** Decided by whether B's dark component exerts dynamical friction (`campaign_fresh_gravity/CFG30_binary_galaxies_referee*`; the originals `hunt_2026/h48_h69_binary_galaxies.out`, `h48_h69b_relative_isolation.out`) |
| B2 | Coma ultra-diffuse galaxies | +1.16 dex above the external-field prediction; **4.9σ / 4.7σ** (equilibrium), 2.7σ (first infall) | **Re-scored (CFG31).** UDGs are accreted under ownership: the isolated law of their infall baryons, no external field. That gives +0.23 / +0.19 dex = **1.3 / 1.1σ** (stars only 2.3 / 2.1σ); DF44 alone 0.7σ; consistent with the M31 satellites under the same rule (0.4σ) | **passes under B's rule.** The 4.9σ belongs to the external-field reading. The pass is only as strong as the ownership rule, which DR4 tests (`campaign_fresh_gravity/CFG31_coma_udgs_under_b*`; `fable_independent_2026/L23_udg_verify.out`) |
| B3 | the a₀ ladder (a₀ fitted per system class) | the cluster rung **6.3σ** from the deep-tail value (a phantom-only reading) | **Re-scored (CFG34).** Under B the clusters close (X-COP 0.7σ). The new group rung (20 X-ray groups) is short 1.41 / 1.33× at R500 (**1.8 / 1.5σ**, with a generous hydrostatic allowance) and 1.88× inside R2500 (**2.6σ**). The shortfall tracks the baryons groups have lost (ρ = −0.96) | **the 6.3σ does not apply to B.** B's cosmic share, tied to today's baryons, is short in baryon-depleted groups and ellipticals: a design constraint on T5 (`campaign_fresh_gravity/CFG34_groups_and_the_ladder_under_b*`; `hunt_2026/h20_a0_ladder.out`, `h7_groups_hot_gas.out`) |
| B4 | X-ray ellipticals | need a factor **1.69** more boost (recorded as "1.69 dex"; it is a factor, 0.23 dex) | **Re-scored (CFG32).** B's prediction is the law, and the max rule is not an escape (at each radius it over-predicts 10 kpc 2.4–5.5×). Per-galaxy offsets give +0.28 / +0.25 dex (a factor 1.9 / 1.8) at **1.7 / 1.6σ** with the IMF and radial-range floor. The shortfall grows outward in 7 of 7. It is carried by NGC 720, 4649 and 4472, which would need 9–15× their stellar mass in hot gas | **large but not established.** Decided by the deprojected gas profiles, which are not yet in the repository (`campaign_fresh_gravity/CFG32_xray_ellipticals_under_b*`; `hunt_2026/h10_h18_xray_hse.out`) |
| B5 | clusters and groups: η 1.8–2.1 with no step; CLASH needs a₀ × 18.4; X-COP cores η 2.7–2.9 | as recorded | B's cold component; **X-COP passes** in B's harness | the others not individually re-scored |
| B6 | Bullet cluster peaks | phantom only: short ×3.2 | **passes** in B (main 4.6×, sub 4.9×) | **resolved in B** |
| B7 | SLACS Einstein radii | 14–18% short at a Salpeter IMF | **Re-scored (CFG33)** as a lensing-vs-dynamics test inside B. The lenses need 1.20–1.27× Salpeter stellar mass; B's own law on ATLAS3D dynamics gives 0.85–0.86× at the same dispersion. The gap is +0.16 dex: **1.5–1.7σ with a 0.10-dex cross-survey floor, 7–8σ statistically** | **passes only within the floor.** Decided by lensing and dynamics of the same galaxies on one stellar-population model (`campaign_fresh_gravity/CFG33_slacs_lensing_vs_dynamics*`; `hunt_2026/h53_h54_slacs_lenses.out`) |
| B8 | Fundamental Plane tilt | a theorem: the kernel cannot produce it | applies to the kernel | not re-scored |
| B9 | reionization optical depth | +1.4–2.2σ "in every branch" | — | not re-scored |
| B10 | vertical force K_z | one-line estimate over by 30–37%, scale length 4.5σ | the full-AQUAL calculation gives f_M = 1.30 with the Eilers slope; fails only the v_c normalisation | **superseded** (`hunt_2026/h24_h33_h61.out`) |
| B11 | tidal dwarfs (+2.84σ); outer-halo globular clusters (M/L_V 0.76) | as recorded | Newtonian under ownership | **pass** in B's harness |
| B12 | DiskMass Υ_K; warp onset | Υ_K 0.58 vs 0.31; the external-field radius is the worst warp scale | — | not re-scored |

## C. Kills that ended earlier constructions (why they were abandoned), largest first

| # | construction | the kill | source |
|---|---|---|---|
| C1 | the MMG constraint-first chassis (PAPER2) | γ_PPN = 0: **43,479σ** against Cassini's Shapiro delay; α₁ = +4, **2.5×10¹⁹** over the pulsar bound | `RETRACTIONS.md` (2026-08-27) |
| C2 | pure modified inertia | lensing excludes it at **21σ** | `RETRACTIONS.md` |
| C3 | a₀ = 2cH_Λ (de Sitter–Unruh via Deser–Levin) | **15.6σ** | `RETRACTIONS.md` |
| C4 | the local density ρ_local as a₀'s source | **13–34σ** on 175 SPARC galaxies (the framework's ρ_Λ wins) | `EMPIRICAL_TESTS.md` (A14) |
| C5 | PAPER8's foliation theory | **9σ** in the cluster ΔΣ shape; 1.49–1.99× short in mass at R500 | `fable_independent_2026/THE_COMPLETE_THEORY_2026-09-08.md` |
| C6 | the alternative closure's universal drift | **8.5σ** (PSR J0737−3039) | `STANDING.md` |
| C7 | khronon dust | KiDS Δχ² **+374** (gate < 100) | `STANDING.md` (BSK3) |
| C8 | PAPER24/25's disformal clock | GW170817: a **1.8–2.3 yr** delay against the observed 1.7 s | `real_research/reviews/THE_THEORY_AS_IT_STANDS_2026-09-22.md` (CK01; errata deposited) |
| C9 | the switch variable of C-H/K | GW170817: ≥ **19 h** early against 1.74 s | same file (L351) |
| C10 | the v9 AeST embedding | PPN α₁ = −2(K_B + 2), untunable; α₂ orders of magnitude over | `STANDING.md` |
| C11 | the exact α = 1 law | a sunward anomaly **1278×** over the ephemeris bound | `STANDING.md`, `EMPIRICAL_TESTS.md` |
| C12 | clusters, phantom only | η(R500) = 2.33: +0.405 dex, **4.05 / 2.70 / 2.03σ** against 0.10 / 0.15 / 0.20-dex absolute floors | `STANDING.md` §4; resolved in B by the cold component |
| C13 | the phantom active-mass law; the Λ-triggered carrier | **~4σ** (L315); RC100 **3.0–3.4σ** (L320) | `STANDING.md` |
| C14 | the AeST realisation at Cassini's quadrupole | **3–15σ** (shared with MOND) | `STANDING.md` |

## D. Withdrawn, overstated or not framework-specific: never cite these as failures

| number as once stated | correct reading | source |
|---|---|---|
| MW ultra-faints "7.97σ" | **3.8 / 3.5σ**: 9 upper limits had been dropped and no systematic floor applied (CFG28); the failure itself stands | `campaign_fresh_gravity/CFG28_ufd_referee*` |
| Lyman-α forest "6–8σ exclusion" | **0.4–0.9σ**: the kernel was evaluated at the wrong acceleration | `RETRACTIONS.md`, `EMPIRICAL_TESTS.md` (A9) |
| Coma UDGs "19.4σ" | **4.9σ / 4.7σ** (equilibrium), 2.7σ (first infall); the amplitude stands | `fable_independent_2026/L23_udg_verify.out` |
| MUSE-DARK III: a₀ rising, "12–16σ" against the flat law at face value | **non-diagnostic**: ΛCDM simulations produce the same apparent rise, and it is method-localised | `real_research/A0Z_MUSE_DARK_III_CONFRONTATION.md` |
| "SPARC excludes P2 at > 99.9%" | **~2σ**: the bootstrap under-covered the spread about 5× | `campaign_fresh_gravity/CFG14_shape_calibration*` |
| clusters "367σ" | meaningless (statistics only); the floor-limited value is 4.05σ | `STANDING.md` §4 |
| KiDS + Local Group "5–7σ" | **not framework-specific** (ΛCDM worse) | `campaign_fresh_gravity/CFG23_lcdm_control*` |
| budget vs KiDS "5.4σ" | **not decidable** with the present machinery | `campaign_fresh_gravity/CFG27_edge_thread_closure*` |
| FG016's KiDS kill | **not framework-specific** | `campaign_fresh_gravity/CFG25_fg016_lcdm_control*` |

## What decides the rest

- **Gaia DR4 (2 December 2026).** Candidate B's ownership rule predicts wide binaries are exactly Newtonian, and dies at γ̂ ≥ 1.084. Standard-MOND wide binaries (1.16–1.23) die on a Newtonian result (`prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`, Amendments 13–14).
- **a₀ at z ≈ 2.5.** The flat law predicts a zero-point shift of 0.00; ΛCDM expects +0.33 dex (PAPER7 v3).
- **B1 is scored (CFG30) and does not decide.** Deciding it needs two things:
  - an orbit distribution derived from each law's own assembly history (N-body grade);
  - a statement from B on whether its dark component exerts dynamical friction.

κ = ½ is fitted, not derived. Nothing here says the theory is closed.
