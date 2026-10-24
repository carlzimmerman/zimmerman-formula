# X19_selector_rank_test — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** Is there one physical variable V such that ordering every system class in the record by V reproduces the
required "extra cold mass" pattern? If yes, at what threshold V*?

Standing rules: κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt a₀ = 1.1312e-10 m s⁻², never pooled. No
dark-matter particle (the extra is "cold energy", a field). No knob scan: V* is read off the data ordering as the gap
between class intervals, never fitted to a χ². Not "theory closed". Nothing here may say the data favour the framework.

## 1. Required extra E (what a class needs above a baseline), and its label

E is in dex of acceleration, log₁₀(g_obs / g_baseline), with sd s. Z is the record's own significance against zero extra
where the record publishes one; otherwise Z = E/s.

**Baselines.**
- **B_iso (PRIMARY, verdict).** The isolated law on the baryons (AQUAL, μ = x/(1+x), no external field). This is the
  successor's baseline: Z★ owned units fall at g_host with no EFE (Z1 `DESIGN.md`, K6), and "adds nothing in isolated
  galaxies" is measured against it.
- **B_EFE (SECONDARY, reported qualifier).** v3s's static prediction: AQUAL solved in the host's field (exact MOND + EFE).
- B_N (Newton on baryons) is listed in the class table for context only.

**Label rule (L-S, verdict).** EXTRA if Z ≥ 2; NONE if Z < 1 (this includes every negative E); AMBIGUOUS if 1 ≤ Z < 2.
AMBIGUOUS classes are shown in the ordering but do not constrain a selector. Labels are set per footing.

**Label rule (L-B, reported).** The brief's literal pattern: SPARC, groups, the lightest tercile, the MW disc, UMa
members, TDGs and DF2/DF4 are NONE; T2, T3, the cosmic background, and every hosted dwarf class (MW classical, MW
ultra-faints, bright M31, M31 others, Crater II, Antlia II, Coma UDGs) are EXTRA; the isolated LG dwarfs are NONE.

## 2. The class table (rows; sources; both footings read separately)

Cluster cells are h = 0.672 (F1 PRIMARY); h = 0.686 is reported. Groups' record value is in log σ, so E = 2 × it.

| # | class | B_iso source (E, s, Z) | B_EFE source |
|---|---|---|---|
| 1 | SPARC small (M_b ≤ 3e9 M☉, global Υ) | P4 JSON `tiles.T1.footings.<f>.classes_global_U.small` (mean, se; v3 with Chae g_e, which moves it < 0.001 dex) | same |
| 2 | SPARC large (M_b > 3e9) | `….classes_global_U.large` | same |
| 3 | Groups (BFJR, Tian+26, 63) | P4 JSON `tiles.T3.footings.<f>.v3_isolated` (mean, tot, Z); P4 README T3 | same (group field not on disk; P4 caveat) |
| 4 | Clusters T1 (lightest Mgas500 tercile) | X7 JSON `bins["terciles|<f>|h0672"][0].MID` (A_CAL, s_CAL, Z_CAL); X7 .out "terciles … [GRADED]" | same (cluster EFE ≤ 0.02 in A, X2 (c1)/(c2)) |
| 5 | Clusters T2 | `…[1].MID` | same |
| 6 | Clusters T3 | `…[2].MID` | same |
| 7 | MW disc (K_z,1.1 at R₀) | P4 JSON `tiles.T4.models.B1_McMillan17.<f>["F0|L24"].K_R0` vs 66.4 ± 2.2 (Bovy & Rix; P4 README T4); E = log₁₀(66.4/K_R0) | same |
| 8 | LG field, isolated (13) | X1 JSON `class_stats["<f>|LG field|primary|iso AQUAL L*0"]` (median, sd); X1 README :80 | `…|AQUAL + EFE L*0 (exact MOND + EFE)` |
| 9 | MW classical (8) | `class_stats["<f>|MW classical|primary|iso AQUAL L*0"]`; X1 README :75 | AQUAL + EFE key |
| 10 | MW ultra-faints (31) | `…|MW ultra-faint|…` ; :76 | idem |
| 11 | bright M31 dSphs (25) | `…|bright M31|…` ; :77 | idem |
| 12 | M31 others (5) | `…|M31 others|…` ; :78 | idem |
| 13 | Crater II | `…|indiv:Crater II|…` ; :95 | idem |
| 14 | Antlia II | `…|indiv:Antlia II|…` ; :96 | idem |
| 15 | Coma UDGs (9) | S1 JSON `coma["<f>|S2 AQUAL isolated L*0 E-W"]` (meanE_dex, z_sys); S1 README :8 | `coma["<f>|S3 AQUAL + EFE dmean L*0 E-W"]` |
| 16 | UMa members (27 per galaxy) | U1 JSON `u1_a2_field_frame_results.json` `numbers.F5.footings.<f>.A4.any_radius.per_galaxy` (offset vs field points in the same g_bar bins); U1 README F5 | same (no EFE solve on disk) |
| 17 | TDGs (6) | P4 JSON `tiles.T5.footings.<f>.T_law_isolated` (rbar, se) | `tiles.T5.footings.<f>.L24.T` |
| 18 | DF2/DF4 (2) | `tiles.T5.footings.<f>.U_law_isolated` (rbar, se in ln of g; ÷ ln 10 to dex) | `….L24.U` |
| 19 | Cosmic background | E = log₁₀(1 + Ω_c/Ω_b) with Ω_c/Ω_b = 5.364 (record's cosmic ratio, Z1 DESIGN; R16/R18 of Z1 REQUIREMENTS_MATRIX): a dust that grows from z ≈ 1100 is REQUIRED, so the label is EXTRA by requirement, not by a Z | same |

The ordering in V uses class members where the record has per-system data (rows 1–3, 8–18 and the cluster terciles);
rows 7 and 19 are single systems or bands (§3).

## 3. Candidate variables V (computed from the record's own catalogue values; never fitted)

Each V is evaluated at the radius where E is measured: r_{1/2} = 4/3 R_e (pressure-supported dwarfs and UDGs, Wolf, as
X1/S1), R_out (TDGs, as P4), the last measured radius (SPARC, UMa), R_e (groups, as P4/Tian), r = 0.548 Mpc (cluster MID
band 0.3–1 Mpc, log-centre), R₀ (MW).

| id | V | definition | verdict-bearing? |
|---|---|---|---|
| V1 | baryonic mass M_b | record mass (SPARC 1.33 M_HI + Υ₀ L[3.6] with the CFG695 global Υ₀; dwarfs log M★ from X1/S1 CSVs; TDG M_bar; DF2/DF4 M★; groups logMbar; clusters 1.2 × MGAS500 (F1's f★ = 0.20); MW 6.646e10 (P4 B1)) | yes |
| V2 | velocity scale σ (and T_vir = μ m_p σ²/k, μ = 0.6, same ordering) | σ_LOS (dwarfs, UDGs, DF2/DF4, groups), V/√2 (rotators: V_obs at the last point, TDG V_circ, MW v_c(R₀)), √(kT/μm_p) from eRASS1 KT (clusters) | yes |
| V3 | mean enclosed baryonic density ρ_b(<r) | M_b(<r)/(4/3 π r³), with M_b(<r_{1/2}) = M_b/2 for dwarfs; clusters from F1's β-model (r_c = 0.15 R500, β = 2/3) normalised to MGAS500 at R500, × 1.2 | yes |
| V4 | internal acceleration x = g_N,bar(r)/a₀ | G M_b(<r)/r² / a₀ (per footing) | yes |
| V5 | host external field e = g_e/a₀ | record values: X1/S1 CSV `x_e_mid` / `x_e_dmean`; P4 T5 `ge`; SPARC and UMa from Chae's env (U1's convention: law of the mean of log_eN_maxclu/noclu × 1.2e-10); clusters the X2 band [noclu, maxclu]; MW: M31 (1e11 M☉, S1 host label) at 785 kpc through the law; groups: not on disk (N/A) | yes |
| V6 | potential depth \|Φ\|/c² | Newtonian baryonic, zero at infinity (J1's convention): internal G M_b(<r)/r plus the integral of the outer baryons where profiles exist (clusters, β-model to 3 Mpc), plus the host term g_N,host·d (point-mass host, g_N,host = inverse law of g_e) | yes (J1 found it fails; reported for completeness) |
| V7a | hot-gas fraction f_hot = M_hot/M_b | clusters 1/1.2 (F1 convention); SPARC, dwarfs, UDGs, TDGs, DF2/DF4, MW (McMillan17 has no hot halo) 0 by catalogue; groups N/A (Tian's M_bar composition not on disk) | yes |
| V7b | X-ray/virial temperature kT | eRASS1 KT for clusters (finite rows only); 0 (no X-ray gas) for every non-cluster row; background 0.26 eV (T = T_CMB(1+z)) | yes |
| V8 | baryon fraction f_b = M_b/M_dyn | M_dyn from the observed kinematics at the same r (Wolf for dwarfs; V²r/G for rotators; eRASS1 M500 at R500 for clusters) | **reported only**: M_dyn shares the data that define E (BY-CONSTRUCTION RISK) |
| V9 | relaxation number N_orb = t_age / t_orb | t_orb = 2π r / v, v = √3 σ (pressure) or V (rotation); t_age = 13.8 Gyr except where the record holds an age (TDG: tmerg/torb from Lelli's table; DF2/DF4: CFG657 ages); clusters use 13.8 Gyr (upper bound; disclosed) | yes |
| V10a | environment density ρ_env | host's mean enclosed total density at d: 3 g_e/(4πG d) where d is on disk (hosted dwarfs, Coma, TDGs, DF2/DF4); ρ̄_m (field) for SPARC, groups, clusters; N/A for UMa | yes |
| V10b | hosted flag H | 1 if the record places the system in a host's field (rows 9–18), else 0 | yes (binary; enters the two-variable search) |
| V11 | formation-mode flag O | 1 = tidal/collisional origin (TDGs, DF2/DF4), 0 otherwise | **reported only** (a label, not a catalogue measurement) |

Cosmic background (row 19) values where V is defined on FRW: ρ_b over z ∈ [0, 1100] (Ω_b ρ_crit(1+z)³, h = 0.672,
Ω_b = 0.049); x over the record's linear-field band: "passes a₀ at z ≥ 84–101 (15.6 a₀ at z = 1100)", late fields x ≪ 1
(LEDGER:705; Z1 matrix "Local selectors"), i.e. [0, 15.6]; e = 0; kT = 0.26 eV; f_hot = 0; N_orb = 0; ρ_env = ρ̄_m(z)
band. M, σ, Φ: N/A (not placeable); for these V the background is reported "not placeable" and the verdict runs on bound
systems only (qualifier stated).

## 4. The rank rule

For each class and V: the interval [lo, hi] is the 16–84 % range of members (N ≥ 3), [min, max] for N < 3, or the stated
band (clusters' e, the background). Values compared in log₁₀ V (binary flags as 0/1).

- **V separates** (per footing, per labelling) iff
  (a) there is a gap: max(hi over NONE) < min(lo over EXTRA) (direction UP) or max(hi over EXTRA) < min(lo over NONE)
  (direction DOWN). V* = the geometric centre of the gap (reported, not fitted).
  (b) **graded amounts are monotone in V**: among the EXTRA classes ordered by their median V, no pair is reversed (E
  falls while V moves away from V*) by more than √(s_i² + s_j²). A V that passes (a) and fails (b) is "SEPARATES,
  NOT GRADED" and does not count as a selector.
  (c) every decisive class has a value. A V that is N/A for a decisive bound-system row is INCOMPLETE (reported, cannot be
  the verdict selector). For the background see §3.
- **Offending classes.** For each V and direction, the misordered classes at the best threshold (the threshold between
  sorted interval edges with the fewest NONE intervals reaching above it plus EXTRA intervals reaching below it; ties:
  report all) are named.
- **Strict variant (reported):** [min, max] for every class.
- **Two-variable separation** (run only if no single V separates on a footing): axis-aligned rules on two verdict-bearing
  V (incl. H), "(s₁V₁ > a) AND/OR (s₂V₂ > b)", s = ±1, thresholds between interval edges; a rule separates iff every
  EXTRA box satisfies it entirely and every NONE box violates it entirely. Report every separating pair (the minimal
  separator is two variables by construction; list them all) or, if none, the best pairs with their offenders. A
  reported-only run adds O (V11) and f_b.

## 5. Verdict classes (primary: B_iso, L-S labels, 16–84 % intervals, h 0.672)

- **SINGLE SELECTOR FOUND: V (threshold V\*)** — at least one verdict-bearing V separates (a + b + c) on both footings.
- **ONLY TWO-VARIABLE SEPARATION: (V1, V2)** — no single V does; at least one pair separates on both footings.
- **NO LOW-DIMENSIONAL SELECTOR** — neither on either footing.
- **UNDECIDED** — the footings disagree in class; or fewer than 2 EXTRA or 2 NONE decisive classes; or the step-0 stop
  rule fires.

Qualifiers reported (no verdict weight): B_EFE; L-B; strict intervals; cluster h 0.686; background placeability.

## 6. Step 0 (stop rule)

Each row's E (and s, Z) is read from the committed JSON key above and compared with the printed value in the lane's
`.out` / README (tolerance: the printed digits). Independent recomputations where cheap: TDG and DF2/DF4 isolated-law
means from the Lelli CSV and CFG657 inputs (P4 K9 formula, tolerance 1e-3); X1 class medians from `x1_per_system.csv`
(plain median vs JSON median; tolerance 0.03 dex, reported); cluster tercile membership (109/108/109) and median MGAS500
(3.30e12 / 1.17e13 / 2.92e13) from X2's per-cluster npz; SPARC split counts 68/107; UMa N = 27–28. A decisive row that
cannot be reproduced is marked; **if more than two rows fail, stop** (verdict UNDECIDED).

## 7. Step 2 (reported only)

For any V that separates (or the minimal pair): grep the record (`campaign_fresh_gravity/LEDGER.md`, `rebuild_2026_10_22`,
`covariant_push_2026_10_22`, `doors_push_2026_10_22`) for an action-level mechanism keyed to it. State whether it would be
new physics (+1 constant) and what it predicts for a class not in the test (fossil vs ordinary groups; the Bullet
Cluster offset).

## 8. Checks and MUTATE

- K0: every decisive row reproduces (§6).
- K1: the independent recomputations agree within tolerance.
- K2 (positive control): V_oracle = 10^(−E_raw), with E_raw re-derived from the per-system/committed raw tables at load
  time (not from the class table), must separate under L-S on both footings. It checks the rank machinery.
- K3: rank-rule unit tests on synthetic tables (one separable, one not, one separable-but-ungraded) give the right answer.
- K4: unit identities (law inverse g_N = g²/(g + a₀) round trip ≤ 1e-12; σ(KT) for 1 keV = 405 km s⁻¹ ± 1 %).
- K5: peak RSS < 1 GB.

**MUTATE** (`X19_MUTATE=1`): swap E, s, Z between MW ultra-faints and the LG field dwarfs, and between clusters T1 and T3,
in the class table only. Required: **K0 FAILS** (swapped rows no longer match their JSON) and **K2 FAILS** (the oracle,
built from the unswapped raw tables, no longer separates the swapped labels). Outputs `*_MUTATE.*`; exit 1.

## 9. Compute

One script, single thread, `nice -n 15`, < 1 GB, minutes. No downloads. `PYTHONHASHSEED=0`. Outputs `.out`,
`_results.json`, a per-class CSV. Every README number comes from these.
