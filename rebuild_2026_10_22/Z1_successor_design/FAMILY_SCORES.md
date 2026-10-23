# Z1 family scorecard: seven families against the requirements matrix

Rows are the matrix rows (`REQUIREMENTS_MATRIX.md`). Classes: **P** pass, **C** conditional, **F** fail, **O** open,
**U** untested, **–** not applicable. `(prov)` = rests on literature read here from arXiv abstract / ar5iv pages
(PROVISIONAL); such a cell is never shown better than C. `(Kn)` = this lane's sympy check. Footnotes give every source.
κ = ½ FITTED; numbers canonical / alt, never pooled. Nothing here says the data favour any family.

## 1. Grid

| row | v3s | v4 (AeST + γ_L) | TeVeS-type / BIMOND | dipolar (BLT) | P-medium (Codex) | superfluid (ref.) | env.-phase, local |
|---|---|---|---|---|---|---|---|
| R1 GW speed, pulsars | P ¹ | C (prov) ⁸ | F TeVeS (prov); C c_T=c class, BIMOND (prov) ¹⁴ | C (prov) ¹⁹ | – no metric sector (Y1) ²⁶ | U | U |
| R2 health, well-posedness | C ² | F ⁹ | U | **F (K1, K3)** ²⁰ | O: parent ill-posed on FRW ²⁷ | F (prov) ³¹ | F by theorem ³⁴ |
| R3–R5 law, MeerKAT, groups | C / P / P ³ | U (static law exact) ¹⁰ | U | C (prov), needs weak clustering ²¹ | O: law needs ℓ ≥ 134 kpc, growth ℓ ≤ 0.44 kpc ²⁸ | C (prov) ³² | – |
| R6 isolated LG dwarfs | P ³ | U | U | U | Y1 | U | – |
| R7 Cassini | P ⁴ | C ¹¹ | F (unscreened) ¹⁵ | F (prov) ²² | Y1 | U | – |
| R8 outer globulars | P ⁴ | U | F (unscreened) ¹⁵ | F (unscreened) ²² | Y1 | U | – |
| R9 wide binaries | O (sealed) ⁴ | U | O (law-first γ_v ≈ 1.17–1.20) ¹⁵ | O | Y1 | U | – |
| R10–R11 MW K_z, slope | F / F ⁵ | U | F / F (μ-family) ¹⁶ | F (prov) ²³ | Y1 | C (prov) ³² | – |
| R12 TDGs, DF2/DF4 | C (T3 reading) ⁶ | U | F (EFE AQUAL) ¹⁶ | F (prov) ²³ | Y1 | U | – |
| R13–R14 satellites, Coma UDGs | F ⁶ | U | F ¹⁶ | F (prov) ²³ | O: self-binding not certified ²⁹ | U | F by theorem ³⁴ |
| R15 cluster cores | F ⁷ | F ¹² | F (MOND class) ¹⁶ | F (law on baryons) ²³ | Y1 | C (prov; particle) ³² | – |
| R16 linear growth | F ⁷ | F ¹³ | O (prov) ¹⁷ | **C (K3): CDM only while 4πG\|Π\| ≪ a₀** ²⁴ | O: δ ∝ a^0.694 in the covariant parent ²⁷ | C (prov) ³² | F by theorem ³⁴ |
| R17 BBN | F literal; C with DBI ⁷ | P ¹³ | U | C (prov) ²⁴ | Y1 | U | – |
| R18 CMB | F ⁷ | F ¹³ | O (prov) ¹⁷ | C at risk (K3) ²⁴ | – (no Boltzmann sector) | C (prov) ³² | – |
| R19 isocurvature | O ⁷ | O | U | O | F for Codex's two-field origin ³⁰ | U | – |
| R20 a₀ tied to Λ | P (form; κ fitted) ¹ | C | U | C (K2) ²⁵ | P (units; κ fitted) | – | – |
| R21 strong field | P ¹ | U | U | U | – | U | – |
| R22–R23 lensing | C / O ³ | U | U | U | Y1 | U | – |
| R24 cosmic shear | O ⁷ | U | U | U | Y1 | U | – |

## 2. Ranking (one line each)

1. **v3s** (v3 + switched stiffness; adopted by the owner, 591ec436be). The best-verified chassis: GW at c, a closed
   3-DOF algebra, well-posed at saddles, screened Solar System and globulars, the law, MeerKAT, groups. Fails every
   cold-sector row (hosted dwarfs, clusters, growth, BBN, CMB) because its one cold field is the law's field (α ≡ 1).
2. **Codex's P-medium.** The only family with a live nonlinear self-binding mechanism. Its own parent-compliance table
   needs ℓ ≥ 134 kpc for the law and ℓ ≤ 0.44 kpc for growth (a 300× gap in one constant); the 3D core peak is not
   converged and binding is not certified (W1). Scored by lane Y1, still running.
3. **Dipolar (Blanchet–Le Tiec).** Single metric, a Λ–a₀ link, CDM-like linear growth. But its linear sector is CDM in
   disguise plus a ghost (K1, K3), it is unscreened (Solar System, globulars), it carries the AQUAL EFE, and its ΛCDM
   equivalence needs 4πG|Π| ≪ a₀, which fails at recombination (x ≈ 11–14).
4. **v4 (AeST + γ_L).** Ill-posed wherever the aether twists (I1); runs away on FRW for the dust shape tried (C7);
   cannot supply cluster cores (H2). Most galaxy tiles never computed.
5. **TeVeS-type / BIMOND.** Original TeVeS is in the class GW170817 excludes (prov); the c_T = c TeVeS class and BIMOND
   survive R1 (prov) but inherit the unscreened-law failures (Cassini, globulars) and the MOND-class ones (hosted EFE,
   clusters, MW). Cosmology unexplored here.
6. **Environment-dependent phase, local selector.** Every local selector the record tried is closed by a theorem:
   Theorem G (gates in θ, u), Theorem S (label-free tethers hover), D-T′ (any local hold cancels self-gravity), the
   μ-pincer (pressure cannot keep the cold mass out of galaxies), J1 (potential depth), V1 (density). The design in
   `DESIGN.md` is this family with a **non-local** selector.
- Reference only: **Khoury-type superfluid** (an eV axion-like particle; Lorentz-invariant completions lose global
  hyperbolicity in the MOND regime (prov); hybrid MOND–CDM models radiate Cherenkov via a slow matter-coupled mode (prov));
  **ΛCDM** (a particle). Plain MOND and the canonical rules are scored in `explainers/crispy_fried_chicken_flavors.md`.

## 3. This lane's checks on the dipolar family (`z1_successor_design.out`, K1–K3)

- **K1.** BLT's printed non-relativistic equations (85)–(86) follow from L = ½v² + v·ξ̇ + U(x) + ξ·∇U − W(σξ)/σ with
  the mixing sign +1, and only with it. The kinetic matrix [[1, 1], [1, 0]] has det −1 (eigenvalues −0.618, +1.618): one
  negative-energy direction. This agrees with the record's AG6C H5 (provisional) and with Blanchet–Heisenberg's own
  decoupling-limit ghost (prov).
- **K2.** The dielectric matching W₂ = 4πG, W₃ = 32π²G²/a₀ is reproduced exactly. BLT's Λ = 3α²(2πa₀/c²)² maps to the
  framework's a₀ = κc√(Gρ_Λ) as κ = Z/(4πα): α ≈ 0.8 gives κ = 0.576; κ = ½ needs α = 0.921. Like the record's κ, α is
  not derived.
- **K3.** (a) The anchor (monopole) stays at rest at linear order iff W₂ = 4πG. (b) With y = x + ξ the Lagrangian is
  ½ẏ² − ½ξ̇² + U(y) − W/σ to first order in ξ: the gravitating points y are **geodesic dust** and ξ is a ghost whose
  tachyonic growth ξ̈ = 4πGσ̄ξ keeps the anchor still. So BLT's linear "CDM-like growth" is CDM. (c) The cubic term equals
  the quadratic one when the polarization's own field 4πGΠ reaches a₀; beyond it (d) the anchor is pushed at x times
  the field. At recombination the record's x ≈ 11–14 (`R/X0_explanation_map/MAP.md:22`), so the weak-clustering
  assumption and the claimed ΛCDM equivalence are not established there.

## Footnotes (sources)

1. `CP/C8_instantaneous/README.md:14`; `CP/C5_health/README.md:9`; `R/P3_v3_strong_field/README.md:3`; `CP/V3_FULL_PICTURE.md:33`.
2. `R/X3_switched_stiffness/README.md:3`; `reviews/v3_constraint_algebra_2026_10_23/README.md:8`; `reviews/v3s_soft_side_strong_coupling_2026_10_23/` (d27e01f42e). 2D/3D evolution open.
3. `R/P4_v3_galaxy_tiles/README.md:16`–`:18`; `R/X1_hosted_recount/README.md:80`; `R/S2_v3_lowg_lensing/README.md:20`–`:22`; `R/F2_outer_lensing/README.md:3`; `R/P2_spec_isolated_lensing/README.md:3`.
4. `CP/C6_literal_cassini/README.md:7`; `DP/D10_native_Lstar/README.md:3`; `TD:85` (sealed WB prediction).
5. `R/P4_v3_galaxy_tiles/README.md:19`; `R/X5_mw_joint_baryons/README.md:7`–`:8`; `TD:108`.
6. `R/U1_v3_dust_content/README.md:15`; `R/P4_v3_galaxy_tiles/README.md:20`; `R/S1_v3_hosted_small/README.md:7`–`:8`; `R/X1_hosted_recount/README.md:8`.
7. `R/F1_cluster_cores/README.md:3`; `R/S4_v3_muK_clusters/README.md:9`; `R/X4_growth_native_cap/README.md:15`; `R/Q6_v3_class/README.md:5`, `:20`; `R/Q7_bs25_cosmology/README.md:3`; `R/F3_growth_audit/README.md:8`. R19: the abundance is an initial condition with no stated origin.
8. AeST's tensor speed c is a design property of Skordis–Złośnik 2021 (prov); no record lane computed it for v4.
9. `R/I1_gammaL_causality/README.md:3`.
10. `TD:94` (H1: capped F gives the law exactly); the AQUAL-disc SPARC solve was never run for v4 (`explainers/crispy_fried_chicken_flavors.md:172`).
11. H1: Q₂ ≤ 7e-8 of Park's bound (static solve), but the Sun in the Galaxy's field has no well-posed slice (I1): `explainers/crispy_fried_chicken_flavors.md:52`.
12. `TD:95` (H2).
13. `TD:98` (C7 runaway; Cosh at g = 0.75 Δχ² +119); `TD:94` (H1: BBN λ_s = ∞).
14. Boran, Desai, Kahya, Woodard, arXiv:1710.06168 (prov; the abstract does not name TeVeS — "TeVeS is in that class" is this lane's reading of its disformal coupling); Skordis & Złośnik, arXiv:1905.09465 (prov; a TeVeS-type class with c_T = c); Milgrom, arXiv:1308.5388 (prov; BIMOND's H₊ sector is linearised GR with its vacuum waves; c is an inference).
15. The record's unscreened-law results: `DP/E2_field_equation/README.md:8` (Cassini), `DP/D7c_q2_rar_gate/README.md:7` (no unscreened law in the record's family passes Q₂ and SPARC), `TD:86` (globulars). That TeVeS's or BIMOND's interpolating function lies in D7c's family is not checked here.
16. Plain-MOND cells reused for AQUAL-type laws with an EFE: `R/S1_v3_hosted_small/README.md:7`–`:8`, `R/P4_v3_galaxy_tiles/README.md:19`–`:20`, `R/F1_cluster_cores/README.md:3`, `R/X0_explanation_map/MAP.md:18`–`:26`.
17. Not read here; TeVeS's and BIMOND's cosmologies are unexplored in the record (`R/X0_explanation_map/MAP.md:101`–`:103`; CFG230 cells are memory labels, `MAP.md:138`).
19. Blanchet & Le Tiec, arXiv:0804.3518 (prov): an action inside GR, so the tensor sector is GR's; Blanchet & Heisenberg, arXiv:1505.05146 (prov): "gravitational sector safe" in the bigravity version.
20. This lane, K1 and K3(b); `argon_push/AG6C_relativistic_completion/README.md:98`–`:103` (H5, provisional); arXiv:1505.05146 (prov, a ghost in the dark-matter sector in the decoupling limit).
21. arXiv:0804.3518 §IV (prov): MOND follows only if the monopolar density stays σ ≪ ρ_b ("weak clusterisation", to be validated by N-body); `campaign_fresh_gravity/CFG121_door3_dipolar_dm/README.md` (the Newtonian dipolar medium fails G1 for extended baryons with any single polarisation law; scoped no-go).
22. arXiv:0804.3518 §IV (prov): a constant extra pull εa₀ on planets "a priori ruled out by Solar System observations"; CFG121 S4: an uncapped monopole pull a₀/2, 468× the line.
23. BLT's static law ∂(μg) = −4πGρ_b with μ = 1 + χ is AQUAL-type with an EFE (prov), so it inherits the plain-MOND cells of footnote 16.
24. This lane, K3; `R/X0_explanation_map/MAP.md:22` (x ≈ 11–14 at z ≈ 1100); arXiv:0804.3518 (prov: ΛCDM at first order; background Λ + dust).
25. This lane, K2.
26. `R/Y1_pmedium_flavor/FROZEN_CRITERIA.md` (Y-T1: no tensor sector ⇒ NOT COMPUTABLE).
27. `LEDGER:697` (CFG938: covariant parent CONDITIONAL; no linear self-gravity), `LEDGER:699` (CFG941: growth exponent a^0.694); memory of WT-02 / PAPER57 v1.1 (ill-posed on FRW; c_T = c not structural) — not re-read here.
28. `R/Y1_pmedium_flavor/ASSUMPTION_LEDGER.md:19`, `:55` (Codex's parent_compliance: law needs ℓ ≥ 133.8 kpc, growth ℓ ≤ 0.44 kpc).
29. `R/W1_pmedium_3d_scaleup/README.md` verdict table (strong peak NOT CONVERGED; binding NOT CERTIFIED).
30. `R/X1_seedfree_abundance/README.md:3`.
31. `data_assembly/DOORS_LITERATURE_STATUS_2026-09-29.md:50` (Hertzberg+ 2105.02241, prov).
32. Berezhiani & Khoury, arXiv:1507.01019 (prov); `data_assembly/DOORS_LITERATURE_STATUS_2026-09-29.md:48`–`:49`; STANDING.md:296 (condensate μ-pincer). A particle: reference only.
34. `LEDGER:705` (Theorem G), `LEDGER:709` (Theorem S), `LEDGER:707` (D-T′, L-G, T-O2), `STANDING.md:296` (μ-pincer), `TD:96` (J1), `TD:114` (V1).
