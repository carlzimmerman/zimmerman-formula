<!-- Frozen empirical gate list. Compiled 2026-09-28 by reading committed files (agent-assisted); nothing in the repo was edited to produce it. -->
> **Provenance and reliability.** This file was compiled by a delegated reader of the committed repository and then spot-checked by hand. Verified by hand against the committed files: the 42/48 recount and the failed harness control K2; the a₀(z) 'tied, not derived' status and the z ≈ 2.5 test's 2.57σ per object; the Chae cells (1.7 / 2.7 / 2.2 / 3.0σ); the group-level alt-footing budget cost (53.7 / 59.9); the README's stale binary-galaxy line. Those five corrections are already applied in the standing page (rev. 25). The other rows and the remaining flagged conflicts (items 6–10 of its conflict list) were not independently re-verified.
> Where it disagrees with a committed script output, the script wins. It is a map, not a result: nothing here says the theory is closed.

# FROZEN EMPIRICAL GATES for a complete theory of the program (frozen 2026-09-28, read-only research)

Nothing here judges the theory or proposes a fix. Every number below was read in a committed file (script `.out`/`.json`, README, LEDGER). Paths are relative to the repo root; `CFG` files are in `campaign_fresh_gravity/`.

## 0. Conventions and provenance

- **Footings:** canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2 (CHARTER). kappa = 1/2 FITTED. "can/alt" = canonical/alt.
- **Candidate B** = CFG4's target law (T1-T6) + FG001 hierarchical ownership; an *effective* description, not an action. Harness ledger for B (`CFG7_harness_fg097.out`): fitted 2 (kappa, Omega_c h^2), declared 5 (nu shape, x_e = 0.4, max rule T5, switch criterion, ownership rule), tied 1, derived 1 (Solar-System screening).
- **Thresholds** are the harness's (`CFG7_harness_fg097.py`): SPARC rms <= 0.110 dex; KiDS d chi^2 <= +9; lenient budget Omega_ph <= Omega_c = 0.265; X-COP identity within 20%; Bullet > 2x aperture baryons; CMB-lensing |pull| <= 2 sigma; forest deviation <= 0.10; every population gate <= 2.0 sigma. Gates outside the harness use the scoring lane's own declared bar (quoted).
- **Class column (CFG1, `CFG1_README.md`):** MI = MODEL-INDEPENDENT (data-side systematics budget < stake), SOFT (budget >= stake), CONT = CONTESTED (published analyses disagree), n.c. = not classed by CFG1 (CFG1 has 33 results: 14 MI, 11 SOFT, 8 CONT).
- **Excluded as not citable:** CFG2, CFG3, CFG5 (committed INCOMPLETE, "DO NOT CITE", commit 1cbaea5db); XR21/XR24/XR34/XR36 likewise.
- **Name collision:** "B-nu_mono" in `real_research/cross_thread_review_2026_09_26/XR3_obligations.md` is the C-H/K covariant branch (V0), not campaign candidate B. Group 5 statuses are for the C-H/K/V0 branch, the only covariant action on record; candidate B has no action.
- **Harness structure (from the rows in `CFG19_harness_rescore_results.json`):** 52 rows = 48 scored + 4 "BUDGET strict (reported)" rows not counted. Of 24 slots per footing, only SPARC, KiDS, lenient budget (x2 kernels each) and the four dwarf-satellite rows (MW classical, M31 LVD, M31 Collins, MW ultra-faints) differ between footings; the other slots print identical values on both. The 6 failing scored rows are 3 distinct gates x 2 footings (MW ultra-faints, Chae D1, Chae D2). B's Cassini row is a hard-coded True in the script (`rows.append(("Cassini (no constant)", ..., True, ...))`), read from FG001 H1.

## 1. The gate table

Status: PASS / FAIL / MARGINAL (within ~1 sigma of its bar, or passes only under a declared floor) / NS (not scorable or not scored under B).

### (1) Galactic dynamics

| id | observable / data | must reproduce | threshold | B status (can / alt) | script | class |
|---|---|---|---|---|---|---|
| 1.01 | SPARC RAR, 175 gal, 3389 pts | g_obs = nu(g_bar/a0) g_bar, a0 fixed, one global Upsilon_disk (0.5-0.8) | rms <= 0.110 dex | PASS. nu_mono 0.1003 (U .61) / 0.0991 (.57); P2 0.1083 (.70) / 0.1035 (.65) | CFG4_galaxy_law.py; CFG7_harness_fg097.py | MI (A03a) |
| 1.02 | RAR intrinsic scatter | deterministic in baryons | <= 0.043-0.048 dex (95%); ML 0.041-0.046 | met (CFG4 H4; per-footing split not printed in README) | CFG4_galaxy_law.py | MI |
| 1.03 | a0 normalisation vs SPARC g-dagger | a0 inside g† = 1.20 ± 0.02 ± 0.24 (x1e-10); kappa vs 0.465 ± 0.076 (BTFR), 0.55 ± 0.17 | inside sys band | PASS both (0.94-1.13). a0 and Upsilon degenerate: at Upsilon 0.50 best a0 = 1.78e-10 (P2) / 1.37e-10 (nu_mono) | CFG4_galaxy_law.py (H2b); CFG1 (A03b, O3) | SOFT |
| 1.04 | BTFR, 124 clean V_flat | slope -> 4; A_obs 52-59 Msun/(km/s)^4 | law's outer-radius v within 0.053 dex of A_obs | met; deep limit 1/(G a0) = 80.5 (can) / 66.6 (alt) sits 0.07-0.17 dex above; free slope 3.68-3.76 | CFG4_galaxy_law.py (H5) | MI form / SOFT kappa |
| 1.05 | kernel transition shape (SPARC) | P2 (beta=1) not excluded | calibrated p >= 0.05 | nu_mono PASS (p 0.57-1.0). P2 MARGINAL/FAIL: beta-hat 0.48/0.55, p ~ 0.03 (can, both noise models; alt model A), 0.13 (alt model B) = ~2 sigma | CFG14_shape_calibration.py | n.c. |
| 1.06 | halo surface density | Burkert rho0 r0 = 10^(2.14-2.25) Msun/pc^2 (Donato 10^(2.15 ± 0.2)) | inside | met; nu_mono median-max Sigma_ph = 0.89 Sigma_M (declared 0.4-0.8, failed as declared) | CFG4_galaxy_law.py (H6) | n.c. |
| 1.07 | MW classical dSphs | isolated law, infall baryons | <= 2 sigma | PASS 1.06 / 0.74 | CFG7_hierarchy_fg001.py | n.c. |
| 1.08 | M31 dSphs: LVD (34), Collins (14) | same | <= 2 sigma | MARGINAL. Passes only after CFG18: LVD 1.63/1.24, Collins 1.44/1.21 (before: 2.60/2.16, 2.54/2.32 FAIL). Not blind (robustness test of FG001's exploratory H8) | CFG18_satellite_infall_gas.py; CFG19_harness_rescore.py | SOFT (A05d) |
| 1.09 | MW ultra-faints (31 + 9 limits) | offset consistent with 0 | <= 2 sigma | FAIL 7.97 / 7.52 sigma in the harness (FG001, statistical only); refereed 3.8 / 3.5 sigma (+0.325 / +0.304 dex, Kaplan-Meier + 0.077-dex floor). Tides, noise, binaries do not explain (CFG28 H1,H2; CFG29 H1,H2 passed) | CFG7_hierarchy_fg001.py; CFG28_ufd_referee.py; CFG29_ufd_binary_audit.py | n.c. |
| 1.10 | LV dwarfs, statistic C (N=92) | obs +0.080 ± 0.047; B predicts 0 | <= 2 sigma | PASS 1.71 / 1.71 | CFG7_hierarchy_fg001.py | MI (A05b) |
| 1.11 | cluster-infall BTFR (N=314) | slope +0.0033 ± 0.0304; zero point -0.0119 ± 0.0092 | <= 2 sigma | PASS 0.11 / 1.30 (both footings) | CFG7_hierarchy_fg001.py | SOFT (A05a, slope) |
| 1.12 | tidal dwarfs (6, Lelli+15) | Newtonian | chi^2 for 6 objects | PASS chi^2 1.09 (p 0.98) | CFG7_tdg_fg041.py | n.c. |
| 1.13 | outer-halo globular clusters (10 can / 16 alt) | Newtonian M/L_V in [1.0, 2.5] | inside range | PASS 1.70 / 1.73. Does not discriminate (law needs 1.04 / 0.99; FG001 H2 failed as declared) | CFG7_hierarchy_fg001.py | n.c. |
| 1.14 | NGC 1052-DF2 / DF4 | Newtonian at 20 Mpc | <= 2 sigma | PASS DF2 0.01, DF4 0.78. (DF4, u02 measurement: 2.28 sigma) | CFG7_hierarchy_fg001.py (H6) | CONT (A05e; 13 vs 22.1 ± 1.2 Mpc) |
| 1.15 | Chae SPARC external-field signal, D1 (143), D2 (90) | ownership predicts e = 0 | <= 2 sigma | FAIL 4.08 / 4.29 sigma (Chae's fits; same on both footings). CFG8 refit: P2 1.7 (can) / 2.7 (alt), nu_mono 2.2 / 3.0 sigma; H1 (<= 2 sigma) failed for 3 of 4 cells | CFG7_hierarchy_fg001.py (H7); CFG8_chae_kernel.py | SOFT (A05f) |
| 1.16 | Coma UDGs (11) | isolated law of infall baryons | <= 2 sigma | PASS 1.33 / 1.11 sigma (+0.234 / +0.195 dex). Stars only 2.30 / 2.08; external-field rival 4.9 / 4.7. Not blind; not in the 48 | CFG31_coma_udgs_under_b.py | MI (A05c: +0.92-1.01 dex over EFE-suppressed; +0.40 over isolated MOND) |
| 1.17 | binary galaxies (2MRS pairs, d3 > 5 r_p, N=1830) | amplitude A = 1 | H3 bar A in [0.80, 1.25] | UNDECIDED. Circular: A = 1.511 / 1.443 (12.9 / 11.7 sigma) FAIL. B timing orbits: 1.116 / 1.047 PASS (H3); profile -4.2 / -4.1 sigma FAIL (H4); mass trend +5.3 sigma; MW-M31 1.60 / 1.75x too fast. Control C3 failed marginally (estimator 5.5% high) | CFG30_binary_galaxies_referee.py | n.c. |
| 1.18 | X-ray ellipticals (7, Humphrey+06) | offset -> 0 | <= 2 sigma | MARGINAL/FAIL. +0.280 / +0.254 dex (x1.91 / 1.79) = 1.70 / 1.58 sigma (H1 failed); Salpeter alone 1.45 / 1.26. With derived rule: 1.04 / 1.03 sigma (CFG36); colour-blind rule -0.10 / -0.19 sigma (CFG35) | CFG32_xray_ellipticals_under_b.py; CFG35; CFG36 | n.c. |
| 1.19 | SLACS lenses, lensing vs dynamics | alpha_lens = alpha_dyn at same sigma | <= 2 sigma incl. 0.10-dex floor | MARGINAL. Gap +0.15-0.17 dex = 1.5-1.7 sigma with floor; 6.9-7.8 sigma statistical; H3 failed (2.7 vs 3 sigma). kappa_bar at Salpeter 0.81-0.86 | CFG33_slacs_lensing_vs_dynamics.py | CONT (A06) |
| 1.20 | SLUGGS massive early types (19) | offset -> 0 | <= 2 sigma | law alone FAIL +0.080 (3.3 sigma) / +0.065 (2.7); derived rule PASS +0.007 (0.4) / +0.002 (0.1) | CFG38_sluggs_massive_passive.py | n.c. |
| 1.21 | passive disks, 16 ATLAS3D + HI | law fits | <= 2 sigma | PASS +0.026 (0.3 sigma) / +0.011 (0.13) | CFG37_passive_disks.py | n.c. |
| 1.22 | massive S0 / late spirals under the derived cold-mass rule | f_ex = 0, d log v(R_HI) < 0.03 dex in every galaxy | per-galaxy 0.03 dex | FAIL on one galaxy: UGC 2487 +0.139 dex (CFG36 H2). Colour-blind rule: UGC 2885 +0.300 dex (CFG35 H2 FAIL). SPARC rms 0.1003 -> 0.1012 (CFG39) | CFG35; CFG36; CFG39 | n.c. |
| 1.23 | Milky Way: curve 13-27 kpc; M* 5.0-6.1e10; Sigma_dyn(K_z) 68-74 Msun/pc^2 | census-compatible | — | NS (not scored under B) | CFG1_evidence_audit.py (A17a/b, O7) | CONT / MI marginal / SOFT |
| 1.24 | environmental null | a0 independent of ambient density | +0.5 (rho_local fork) excluded | consistent (a0 sourced by rho_Lambda). Slopes +0.052 ± 0.043 (2MRS), -0.046 ± 0.081 (2M++); +0.5 excluded 10.42 / 6.74 sigma. "13-34 sigma" has no committed .out (CFG1 O2) | CFG6_a0z_evidence.py (C7) | MI (O2) |

### (2) Groups and clusters

| id | observable / data | must reproduce | threshold | B status | script | class |
|---|---|---|---|---|---|---|
| 2.01 | X-COP, 12 clusters at 0.8 R500 | dark mass = max(phantom, cosmic share) | identity ratio within 20% | PASS 0.946 ± 0.080 both footings (footing-independent: cosmic share wins 12/12). Additive reading 1.27-1.37 (8.4-10.6 sigma) FAIL | CFG4_clusters.py | SOFT (A09b, bias 0.000-0.142); eta(R500) = 2.33 [1.55-2.80] MI (A09a) |
| 2.02 | Bullet Cluster (Clowe+06) | collisionless mass at galaxies > 2x aperture baryons | > 2x | PASS 4.6x main / 4.9x sub | CFG4_clusters.py | MI (A09c) |
| 2.03 | 20 Lovisari X-ray groups | M_HSE/M_B within 2 sigma | 2 sigma | R500 MARGINAL 1.41 / 1.33 (1.80 / 1.49 sigma); R2500 FAIL 1.88 (2.57 / 2.63 sigma); shortfall tracks f_b, rho = -0.958 | CFG34_groups_and_the_ladder_under_b.py | n.c. |
| 2.04 | Local Group R0 = 0.93 ± 0.12 Mpc (0.96/0.91 ± 0.11 in CFG1) | zero-velocity radius | R0 <= 1.17 (2 sigma) | FAIL. Untruncated 1.92-2.02 Mpc; at KiDS floor 1.285-1.505 (3.0-4.8 sigma high). ΛCDM control in the same machinery: T = 24.5-72.5 vs framework 26-28 | CFG20_lg_edge.py; CFG23_lcdm_control.py | MI marginal (A08); pincer SOFT (A07c) |
| 2.05 | Harvey 72 collisions; cluster counts (eRASS1 0.86 ± 0.01 vs SPT 0.795 ± 0.029) | — | — | NS | CFG1_evidence_audit.py (A09d, A19) | CONT |

### (3) Cosmology and lensing

| id | observable / data | must reproduce | threshold | B status | script | class |
|---|---|---|---|---|---|---|
| 3.01 | CMB TT/TE/EE, Omega_c h^2 = 0.1200 ± 0.0012 | GR + CDM at z >~ 10 | — | met by construction (T4; amount FITTED as in ΛCDM). CFG4_cosmology 5/6 (H3, XR19 cross-check tolerance, failed as run) | CFG4_cosmology.py | MI (A10) |
| 3.02 | CMB lensing 8-400: Planck 1.011 ± 0.028, ACT 1.013 ± 0.023 | amplitude | abs(pull) <= 2 sigma | PASS 1.000 (-0.39 sigma) with the bound-only switch; if the phantom is ADDED in bound regions 1.060 (+1.75 sigma, linear) / 1.528 (+18 sigma, halofit); no switch 1.149 (+4.9 sigma) | CFG4_switch.py (H4); CFG7_harness_fg097.py | MI data; verdict equipment-dependent (CFG1 B01/B03/B04) |
| 3.03 | growth, S8, RSD | LCDM linear growth; S8 >= 0.752; f sigma8 d chi^2 <= 4; late allowance F_max = 1 at <= 600 km/s | as stated | met by allowance | CFG4_cosmology.py (H2) | CONT (S8, A12b); MI (RSD, A12a) |
| 3.04 | BAO, P(k) shape | LCDM background to ~1%; DESI DR1 | — | unchanged by construction | CFG4_cosmology.py | MI (A12a) |
| 3.05 | KiDS-1000 isolated lenses, 4 bins, 0.3-2.6 Mpc | isolated-lens ESD | d chi^2 <= +9 | PASS at declared x_e = 0.4, A <= 2: P2 -10.7 / -10.9, nu_mono -12.4 / -11.3. Self-consistent floor 0.341 / 0.348 vs budget edge 0.341 / 0.338: closed by 0.0003 (P2) / 0.010 (nu_mono) can; alt by ~0.05 | CFG4_switch.py; CFG7_harness_fg097.py; CFG16_selfconsistent_floor.py | MI < 0.3 Mpc (A07a); SOFT beyond (A07b) |
| 3.06 | cold budget vs Omega_c | sum of phantoms <= cold mass | lenient <= 0.265; strict <= 0.159 | lenient PASS 0.188 / 0.190 (can), 0.217 / 0.219 (alt); strict (reported, uncounted) FAIL on all 4 cells: 0.229 / 0.230 (can), 0.264 / 0.266 (alt) vs 0.159. With derived rule +0.003-0.007 | CFG4_target.py; CFG11/12/17/24; CFG39_harness_with_rule.py | n.c. |
| 3.07 | budget vs KiDS, joint | edge above KiDS floor and below budget edge | cost <= 9 (declared) | FAIL as declared: association ownership 29.4 / 32.9 (can, 5.4-5.7 sigma), 45.4 / 49.3 (alt, 6.7-7.0); group ownership alt 53.7 / 59.9. Ruled "not decidable": smallest standard-halo spread S = 50.2 | CFG24_budget_associations.py; CFG27_edge_thread_closure.py | SOFT |
| 3.08 | KiDS + LG one shared edge | joint T | T <= 9 | FAIL sharp edge T_min 26.2-27.8 (5.1-5.3 sigma) can, 31.9-33.4 alt; soft edge 29.8-30.8. Standard halos in same machinery T = 24.5-72.5 | CFG21_kids_lg_joint.py; CFG22_soft_edge.py; CFG23_lcdm_control.py | SOFT |
| 3.09 | density edge x_e | derived, not declared; window [0.31, 0.48] | — | B: declared 0.4. Derived splashback 0.175-0.271: KiDS d chi^2 +51 to +95 (candidate C, 34/48). Standard-halo control also misses KiDS (chi^2 173.0 vs 104.7) | CFG7_edge_fg016.py; CFG25_fg016_lcdm_control.py | — |
| 3.10 | a0(z): z ~ 2.5 BTFR zero point | flat 0.00 dex; ΛCDM-native +0.334 dex | 3 rotators at ±0.10 dex or 4 at ±0.20 | NS (0 of the 2 registered deep-MOND rotators; MUSE-DARK III rise a1 = +1.59 ± 0.105 non-diagnostic). 2.57 sigma per object at 0.13 dex (3.22 if a0 follows the DESI density branch; 2.20-2.35 or 1.48-1.93 under a healthy thawing field); DESI-DR2 branches move a0(2.5) by -0.10 to +0.14 dex | CFG6_a0z_evidence.py; CFG6_a0z_branches.py | CONT (A04, O4) |
| 3.11 | a0 = kappa c sqrt(G rho_Lambda) | kappa = 1/2 vs 0.465 ± 0.076, 0.55 ± 0.17 | 1 sigma | consistent (0.46, 0.29 sigma); FITTED; valid only if Lambda is a true cosmological constant | CFG1_evidence_audit.py (O3) | SOFT |
| 3.12 | Lyman-alpha forest, z = 2-3 | linear power within ~10-15% | forest deviation <= 0.10 | PASS 0.00 (bound-only switch); CFG1 B05/B06: linear proxies, OPEN | CFG4_switch.py (H4) | SOFT (A13) |
| 3.13 | cosmic shear (A18), JWST (A14), Li-7 (A15b), BBN (A15a), tau_reion | — | — | NS under B (BBN standard by T4 per CHARTER; tau_reion +1.4-2.2 sigma "every branch", not re-scored) | CFG1_evidence_audit.py | SOFT / MI (BBN) |

### (4) Local and relativistic

| id | observable / data | must reproduce | threshold | B status | script | class |
|---|---|---|---|---|---|---|
| 4.01 | Cassini gamma - 1 = (2.1 ± 2.3)e-5; ephemeris Q2 = (1.6 ± 1.8)e-27 s^-2 | Newtonian at g >> a0 | Q2 <= 5.2e-27 s^-2 (2 sigma) | PASS via ownership: host-phantom tide 1.6-2.6e-31 s^-2, margin 2.0e4-3.3e4. Strict law would be 4.0-5.7x the ceiling | CFG7_hierarchy_fg001.py (H1) | MI (A01) |
| 4.02 | GW170817 speed | c_T = c to 1e-15 | — | NS (no action) | none for B | MI (A16) |
| 4.03 | lensing = dynamics (Phi = Psi, gamma_PPN = 1) | derived independently | — | NS as derivation: B's lensing is the effective dark density in GR (T2). C-H/K: equal potentials in the static block (conditional) | XR3_obligations.md (row 3) | — |
| 4.04 | full PPN beta, alpha1-3 | derived | pulsar/ephemeris limits | NS for B. C-H/K: beta = gamma = 1 derived (reduced static sector); alpha1 = -4 alpha_c, alpha2 = alpha_c(alpha_c - c2)/(2 c2); full assembled action ORPHANED | real_research/khronon_momentum_2026 (KM3) | — |
| 4.05 | wide binaries, Gaia DR3 | boost | — | contested (1.0-1.4) | CFG1_evidence_audit.py (A02) | CONT |
| 4.06 | wide binaries, Gaia DR4 (2 Dec 2026) | gamma-hat | Arm C (B's rule): 1.000, dead at >= 1.084 (stability checks passing); 1.056-1.084 disfavoured | NS until DR4. Arm A 1.16-1.18 (can) / 1.19-1.23 (alt) dies if Newtonian; chain law ceiling 1.0725 / 1.0900 | prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md (Amdts 13-14) | CONT (A02) |
| 4.07 | external-field effect | see 1.10, 1.11, 1.15, 1.16; directional EFE O6 | — | B drops the EFE by ownership; O6: A-hat +2.95 (p 0.029, n=16) vs -1.70 ± 2.12 (n=25) | CFG1_evidence_audit.py (O6) | CONT |
| 4.08 | moving-galaxy / preferred frame | a0 must not track CMB-frame speed | — | NS. KM1: a0 would track CMB-frame speed by 2w^2/(eps c^2) (10-30% at L297's eps) | real_research/khronon_momentum_2026 (KM1) | — |

### (5) Theory consistency (FRIED_CHICKEN_SPEC, 13 requirements; status of the C-H/K/V0 branch)

| id | requirement | must reproduce | threshold | status | script | class |
|---|---|---|---|---|---|---|
| 5.01 | one explicit action (spec "most important requirement") | all gates from ONE action; both branches never pooled | — | V0 (the one covariant action) is not complete: its region gate is an open obstruction | real_research/chk_v0_2026 (CV1-CV4, README) | — |
| 5.02 | stability: no ghost / gradient instability (req 7, G5) | | c_gate <= gas sound speed | FAIL as varied. Gate second variation lands on baryons: c_gate 1526-3741 km/s at z = 0.25 vs gas 37 / 117; growth 2.0-4.9e4 H at k = 1/kpc. No universal repair harmless (DE13) | real_research/dark_energy_2026/DE12_*.py, DE13_*.py | — |
| 5.03 | strong coupling G8 (req 7) | | Lambda_sc >> E | bounded pass, frozen-background decoupling scope: M_sc >= 8.5e8 GeV (footing-independent); conditional at full-action scope; the README's peer-review correction restricts XC1/XC2 labels | real_research/extra_crispy_2026/XC1, XC3, XC6 | — |
| 5.04 | Cauchy problem / causality by criterion B (req 7) | global time function, no backward signal; mixed Cauchy well-posed | — | leaf problem convex for nu_mono at any positive lapse (XC5); khronon hyperbolic only for alpha_c > 0 (alpha_c = 0: minimal Horava, Cauchy fails); OPEN: strong hyperbolicity of GR + BPS khronon, nonlinear time function; UV khronon 4.4e2-7.9e5 c, causal on foliation (linear, frozen) | XC2, XC5 | — |
| 5.05 | N_grav = 2 (req 2, G4) | | counted, healthy | one extra khronon scalar, positive kinetic energy for alpha_c > 0, c2 > 0 (reduced block); Dirac classification of the assembled action ORPHANED | XR3_obligations.md (row 2) | — |
| 5.06 | conservation of ordinary matter, Noether (req 5, G9) | | — | NS: identity for the assembled action with f varied ORPHANED | XR3_obligations.md (row 5) | — |
| 5.07 | GW sector c_T = c (req 6); one metric (req 11) | | — | c_T = 1 (beta = 0, TT sector, isotropic backgrounds); anisotropic gate-on backgrounds not computed. Earlier switch variables killed by GW170817 (>= 19 h early; disformal clock 1.8-2.3 yr) | XR3_obligations.md (rows 6, 11) | — |
| 5.08 | zero-field limit y -> 0 (req 9) | | Osgood uniqueness | isolated / planar zeros controlled; around an open zero-field region response scales as sqrt(eps), fails Osgood | XC2; XC5 | — |
| 5.09 | Newton/GR recovery, measured G derived (req 10) | | — | G_N = G/(1 - alpha_c/2) in the reduced sector; assembled action ORPHANED | XR3_obligations.md (row 10) | — |
| 5.10 | expanding FLRW, k = 0 (req 8) | | growth sigma8 | ungated growth fails (sigma8 18-27); FRW with leaf average gives GR's Friedmann equation; gate varied on FRW open | CV2; XR3_obligations.md (row 8) | — |
| 5.11 | dark mass as a state of the framework's own field | kernel-invisible, survives stream crossing, keeps khronon a global time function | mass still required | action level ORPHANED; minimal condensate dust breaks at first stream crossing | XR3_obligations.md (row D) | — |
| 5.12 | inner cold component (FG004 / CFG9 / CFG10) | phantom inside baryons | — | reported open requirement: a relaxed cold component overshoots the law by +0.13 to +0.15 dex at g_bar > a0; CFG10 pressure-Gauss-law excluded (+0.17 dex), shell-theorem charge within 0.002-0.003 dex of P2 | CFG7_groundstate_fg004.py; CFG9; CFG10 | — |
| 5.13 | a0-Lambda relation (req 13); exponential law (req 12) | may be a declared input | do not fake a derivation | declared input; kappa = 1/2 fitted; flat a0(z) by construction in the action | XR3_obligations.md (rows 12, 13) | — |

## 2. Gates FAILED or MARGINAL for candidate B, and by how much

Counted in the 48 (after CFG19): 6 failing rows = 3 distinct gates.
1. **MW ultra-faints (1.09):** 7.97 / 7.52 sigma in the harness; 3.8 / 3.5 sigma refereed (+0.325 / +0.304 dex). Persists where binaries are weakest (3.8 / 3.5 sigma); Eridanus II and Ursa Major I exceed the 4.5 km/s single-epoch ceiling by 2.3-2.4 sigma.
2. **Chae D1 / D2 (1.15):** 4.08 / 4.29 sigma; refit under the framework's law 1.7 (P2, can), 2.7 (P2, alt), 2.2 (nu_mono, can), 3.0 (nu_mono, alt).

Reported but not counted:
3. **Strict cold budget (3.06):** FAIL on all four cells, 0.229-0.266 vs 0.159 (1.44-1.67x, computed here).

Scored outside the 48:
4. **X-ray groups inside R2500 (2.03):** 1.88 = 2.57 / 2.63 sigma; R500 marginal 1.8 / 1.5 sigma.
5. **Local Group R0 (2.04):** 3.0-4.8 sigma high at KiDS's floor; not framework-specific (ΛCDM T 24.5-72.5 vs 26-28).
6. **KiDS vs budget (3.07):** 29.4-49.3 d chi^2 (5.4-7.0 sigma); "not decidable" (S = 50.2). **KiDS + LG (3.08):** 5.1-7.1 sigma sharp edge; not framework-specific.
7. **Binary galaxies (1.17):** circular 11.7-12.9 sigma; timing profile -4.2 / -4.1 sigma, mass trend +5.3 sigma, MW-M31 1.60-1.75x. Orbit-degenerate.
8. **X-ray ellipticals (1.18):** 1.70 / 1.58 sigma (x1.91 / 1.79). **SLACS (1.19):** 1.5-1.7 sigma under the floor, 6.9-7.8 statistical.
9. **P2 kernel (1.05):** ~2 sigma (p ~ 0.03); nu_mono consistent.
10. **UGC 2487 under the derived rule (1.22):** +0.139 dex.
11. **Marginal passes:** M31 dSphs (1.21-1.63 sigma, after CFG18), LV dwarfs 1.71 sigma, cluster-infall zero point 1.30, Coma UDGs 1.33 / 1.11 (stars only 2.30 / 2.08), KiDS window closed by 0.0003-0.010 (can) / ~0.05 (alt).
12. **Theory group:** V0 region gate obstructed (5.02); G8 only at decoupling scope (5.03); several requirements ORPHANED (5.05, 5.06, 5.09, 5.11).
13. **Not scorable until data exist:** DR4 wide binaries (2 Dec 2026), a0(z ~ 2.5).

## 3. Where STANDING (or the README) conflicts with, or omits, a script output

1. **"42 of 48":** CFG19 recounts by substituting 4 rows; the CFG7 harness `.out` still prints B 38/48 and its own K2 control check FAILED (flags FG004 and FG016 lane controls). CFG39 H1 FAILED; the LEDGER says "42/48 inferred, not established". STANDING does not mention the four strict-budget failures outside the 48.
2. **Stale inputs in the failing rows:** the harness still carries FG001's 7.97 / 7.52 sigma (UFDs) and 4.08 / 4.29 sigma (Chae); CFG28's 3.8 / 3.5 and CFG8's refit are not substituted (CFG19 README says so for Chae).
3. **Chae:** STANDING says "1.7-2.2 sigma"; CFG8 gives 1.7 / 2.7 / 2.2 / 3.0 (can P2 / alt P2 / can nu_mono / alt nu_mono), H1 failed for 3 of 4. FAILURES_EXECUTIVE_SUMMARY states the alt 2.7-3.0. CFG8 C1 control failed as declared (NGC 5055 -1.26 sigma; noiseless C1b unbiased to 0.08 sigma).
4. **Binary galaxies:** README standing rev. 24 says they "have not been recomputed under ownership"; CFG30 (STANDING, LEDGER) did.
5. **a0(z):** STANDING calls flat a0(z) "derived"; CFG4 T1 lists it as TIED (unimodular tie); CFG6: any DE history flat only on branch A, evolving branches shift a0(2.5) by -0.10 to +0.14 dex; CFG1 O4: CONTESTED. STANDING's "decisively either way" vs CFG6: 2.57 sigma per object at 0.13 dex, 1.48-2.35 sigma under a healthy thawing field; CFG1 O4: registered test cannot run (0 of 2 rotators).
6. **Alt footing "at the margin (45-49)":** that is association ownership; group ownership gives 53.7 / 59.9 (CFG24 `.out` lines 91-92), above S = 50.2 (CFG27).
7. **rho_local null "13-34 sigma"** (FAILURES C4): no committed `.out` (CFG1 O2); CFG6 C7 re-derives 10.42 / 6.74 sigma.
8. **DF2/DF4:** harness scores PASS at 20 Mpc; CFG1 classes the gate CONTESTED (distance).
9. **Theory scope:** extra_crispy README's peer-review correction restricts the XC1/XC2 labels; STANDING does not mention G8 or the Cauchy problem.
10. **Other control failures kept as run:** CFG30 C3 (marginal), CFG20 C1b (2.7e-6 Mpc), CFG7 FG004/FG016 controls, CFG39 H1 (threshold-scan artefact).
