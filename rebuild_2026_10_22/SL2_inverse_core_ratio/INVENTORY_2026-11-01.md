# Measured-record inventory, 2026-11-01 (window 10-18 to today)

Read-only inventory for a derivation independent of Argon. No theory proposed; no line favoured. κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.

**Provenance tags.** [J] checked this pass in a result JSON or .out. [R] quoted from the lane's README, not rechecked in its JSON. [B] from a brief, summary or memory only: the lane itself was not opened. Paths are relative to `rebuild_2026_10_22/` unless they start with `campaign_`, `doors_` or `covariant_`.
**Dependency tags.** DATA = no framework rule in the number. EM1 = uses the fitted M200 line. HSE = hydrostatic masses. CORE = chosen core shape. RES = resolution-limited. NOISE = seed-limited. Υ = fixed or fitted mass-to-light. POST = post-result, no frozen verdict.
**Not covered.** About 330 lanes exist. I opened about 90 READMEs and read only title lines for the rest, so a title-only lane may hold more than is listed. SL1 and SL2 have no README or result yet (SL1 runs finished 08:39 today; SL2 is on `exact 3/19` in its log; NR2 is still running). Nothing from them is used.

---

## 1. FACTS

### 1a. Galaxies: SPARC and RAR
| Fact | Number | Lane | Depends on |
|---|---|---|---|
| Law fit, SPARC, rms at free Υ (A/B) | 0.0541 / 0.0537, Υ 0.52 / 0.44 (canonical / alt) | `X38_…`, `EM1_…` [R] | a₀ fixed; κ fitted |
| Halo-free dust fit, free M200, c ± 2σ | rms 0.031, Υ 0.32; halos scatter 0.51 dex about EM1's relation | `EM1_…` [R] | NFW; free per galaxy |
| Rule N, rms and Υ | 0.0682 / 0.0694, Υ 0.70 / 0.72; 68 % Υ [0.61, 0.81] | `ND1_…` [R], `NR1_…` [J] | EM1, CORE, RES |
| SPARC pass line in use | rms ≤ 0.110, Υ 0.50–0.80 | closure table [R] | owner's line, not data |
| Intrinsic RAR scatter as a separate statistic | **not located in the window**; 0.054 above is the grader's rms | flagged | |
| S_need = ρ₀r₀ by V_flat at Υ 0.50, M☉/pc² [95 %], n, lg M200 | 20–60: 68.6 [51.6, 85.0], 12, 9.97. 60–100: 102.7 [81.0, 124.2], 35, 10.59. 100–150: 143.2 [118.4, 199.8], 23, 11.13. 150–200: 150.2 [97.9, 190.5], 25, 11.76. 200–250: 215.1 [136.6, 272.1], 18, 12.11. 250–400: 411.7 [181.6, 596.0], 10, 12.27 | `ET1_…` [J first bins, R rest] | EM1, Υ, CORE. M200 × 0.5 moves 20–60 to [60.9, 118.3] and 100–150 to 230 |
| Same, free S and r₀, no M200 | 70.2 [52.8, 77.3], 107.7 [89.0, 136.6], 157.5 [136.6, 190.5] (lowest three) | `ET2_…` [R] | Υ, CORE; no EM1 |
| Rise robust to systematics | ρ > 0, p < 0.01 under six changes and 20 of 20 draws; worst cut ρ +0.415, p 0.0099 | `ET3_…` [R] | CORE tested across 72 cells (`ET6_…`) |
| Trend above 150 km/s | none, ρ −0.009, p 0.95; lg S_need on lg M200 +0.60 (p 0.003) below lg M 10.5, flat above (POST) | `ET1_…` [R] | EM1 |
| Bulge signal | none: bulged 195 vs 158, intervals overlap | `ET1_…` [R] | Υ |
| S_need vs Σ_coll | S_need = 32.4 ± 1.9 Σ_coll, χ² 5.35/5 across 20–400 km/s; flat S χ² 54.5; slope 0.238 ± 0.034 vs Σ_coll 0.247–0.254 | `CR2_…` [R] | EM1, Υ 0.50, native σ(M) |
| Υ by V_flat, rule N | 1.20, 1.14, 0.86, 0.54, 0.58, 0.74; ΔV at Υ 0.50: −4.3, −6.6, −12.1, −4.2, −13.9, −54.7 km/s | `X80_…`, `ND1_…` [R] | EM1, N |
| ΔV at high V_flat, all rules | N −17, −53; native −22, −49; **law −12.5, −40** (200–250, 250–400) | closure G6 [B] | Υ 0.50 |
| Surface-brightness slope of V_model/V_obs − 1 at 2 R_d, n 47, V_flat 60–120 | N1 −0.2273 ± 0.0685 [J]; N0 −0.173 ± 0.064; N2 −0.266; floor −0.262, alt −0.288; **law −0.016 ± 0.061, alt −0.023** | `HS1_…` | Υ 0.50; mass-only halo |
| Same, cuts (POST) | N1 at fixed V_flat −0.162 ± 0.077 (law +0.079 ± 0.066); on SBdisk at fixed V_flat −0.195 ± 0.065 (law +0.005); without 5 largest −0.134 ± 0.052; 2–4σ on 47 | `HS1_…` [R] | POST |
| Where the tilt lives | gas-dominated −0.311 (n 31), star-dominated flat, so not Υ | `HS1_…` via memory [B] | |
| S needed to flatten | lg S_need +0.315 ± 0.079 per dex SBeff, ρ +0.60, p 9e-6, median 109, scatter 0.27 dex | `HS1_…` [R] | EM1, Υ |
| Free Υ absorbs the tilt | N1 Υ × 1.65 per dex (p 4e-4), F × 1.86, law × 1.12 (p 0.32); fits sit at grid edge | `HS1_…` [R] | |
| Halo-mass line | lg M200 = 11.18 + 0.90 (lg M_b − 10) | `EM1_…` [R] | fitted on SPARC, law-matched |
| Native abundance match on GAMA | lg M200 at lg M_b 9, 10, 11, 11.5: 10.81, 11.88, 13.30, 14.58 (EM1 10.28, 11.18, 12.08, 12.53); slope 0.79; SPARC on it rms 0.168. Stack of generous choices 11.34; bright end unreliable | `AM1_…` [R] | PS, not a simulated HMF; no PS-to-M200 conversion |
| Bullet self-coupling bound, native cross-section | PASSES BOUNDS | `BU1_…` [R] | analytic |

### 1b. Dwarfs and small systems
| Fact | Number | Lane | Depends on |
|---|---|---|---|
| LITTLE THINGS median E, 20 galaxies | N +0.138 / +0.132 (all 200 draws, lowest +0.129); F −0.041; law −0.025, rms 0.345 | `ND1_…` [R] | S below 1e10 RES |
| IC 1613 | law E −0.593 (Z −7.9); N −0.474 (−6.3). Optical i 34.4° [24.5–42.5], HI 37.9° [27.8–45.8]; P(rescue band) 0.07–0.14 | `ND1_…`, `RF2_…` [R] | e_int ≤ 0.10. Disfavoured, not excluded |
| Local Group, rule N on EM1 | UF +0.758 (Z +6.63), M31 bright +0.390, M31 other +1.006, classical +0.627, field +0.338: 0 of 5, all UNDER | `RG1_…` [R] | EM1 carried 3–6 dex down |
| Native profile on EM1 | UF +1.186 (+9.71), +0.515, +1.266, +0.614, +0.325 (+3.21): FAIL 5 of 5 | `OP1_…` [R] | EM1 |
| S_min by class, no M200 | UF 41, bright M31 31, M31 other 78, classical 71, field 54 (dex sd 0.08–0.33); band 46–64; Spearman r₁₂ −0.24, M★ −0.02, g_N +0.31 | `SN1_…` [R] | lower bound; CORE |
| M_need above EM1's whole M200 | 15/31 UF, 4/25 bright M31, 2/5, 1/8, 0/13 | `SN1_…` [R] | EM1 |
| Free M200 line admitted | near one common mass, lg M200 9.25–10.05 at lg M★ 4 (EM1 5.78); b −0.15 to +0.10; × 10³–10⁴ | `OP1_…` [R] | continuation inside 3ε; no test vs tides, counts, host |
| J0946 perturber | exceeds floor ceiling g ≤ 0.2545 a₀; R 152 / 46 free core; cusp R 80 / 48; never R ≤ 2 up to 1e14 | `PC1_…`, `ND1_…` [R] | lensing solution |
| Draco | core +0.838, cusp +0.541, above | `ND1_…` [R] | |
| Tides at pericentre | extra does not follow pericentric stress | `X25_dwarf_pericentre_tides` via Argon record [B] | PM orbits |
| Stars vs HI in 4 dwarfs; 25 faint rotators; below-law systems | NOT DIAGNOSTIC; lowest g_bar 10^−11.71, excess lives below 10^−12 | `campaign_fresh_gravity/CFG966_…`, `CFG940_…`, `CFG936_…` [R] | |

### 1c. Clusters and groups
| Fact | Number | Lane | Depends on |
|---|---|---|---|
| Core excess over the law on baryons | A_MID 1.68–1.72 ± 0.12 (Z +5.6 to +6.2), alt 1.54–1.58; most favourable corner 1.33–1.37 / 1.23–1.26 | `F1_cluster_cores` [R] | a₀; DATA on gas and shear |
| Known baryons omitted | short of central-mass need by × 4.1–5.5 (T2), × 5.3–6.7 (T3); only KT detected, MGAS500 NONE | `X21_…` [R]; `campaign_fresh_gravity/CFG922_…` EXCESS STANDS | law as baseline |
| Law on outer cluster shear | A 1.01 ± 0.09 / 0.93 ± 0.08 at 1.2–3 Mpc; × 1.8 inside 1 Mpc, 7σ; outer ∝ Mgas^0.9 (law 0.47, Newton 0.84) | `campaign_fresh_gravity/CFG687_…` via memory [B] | |
| Gas offset, pointed vs eRASS1, 45 clusters, M500 4.4e13–5.6e14 | **+0.0053 ± 0.0169**, rms 0.177; line +0.093; slope −0.100 ± 0.100; XMM +0.005 ± 0.020; Chandra +0.009 ± 0.043 | `GS4_…` [J] | DATA; h 0.70, Ωm 0.30 |
| X-COP's scale | +0.111 (own R500), +0.092 (eRASS1 R500); X-COP's two in range +0.122 ± 0.011 | `SM1_…`, `RF3_…`, `GS4_…` [R] | five clusters |
| SZ route | +0.029 ± 0.026; low-z half +0.07 ± 0.025, distant 0.00 ± 0.025; massive end only | `GS5_…` [R] | conditional on unaccepted A1 |
| eRASS1 h | 0.7000 | `GS3_…` [R] | DATA |
| Baryon share, M3 lensing clusters | log Y −0.135 to −0.116 ± 0.040; R₅₀₀ −0.115 ± 0.054; Rmax 2.06 gives −0.086 | `LF1_…` [R] | same shear as keys |
| X-COP hydrostatic share | −0.01 to −0.04, 0.12 dex above LF1 | `LF1_…` [R] | HSE |
| Lensing vs hydrostatic | g +0.069 ± 0.043, 50 pairs NOT POWERED; +0.031 ± 0.020, 81 clusters, POST; pairs stop at R₅₀₀ | `HL1_…`, `HL2_…` [R] | A1 unaccepted |
| 15 keys, native z = 0 on measured gas, f★ 0.034, h 0.672: meas / pred (Z) | G-OUT-M1 0.60/0.32 (+0.79), M2 0.90/0.60 (+1.90), **M3 1.56/1.04 (+4.41)**, **Mall 1.10/0.71 (+3.36)**, **G-MID-T3 2.27/1.68 (+2.17)**, G-OUT-T1 0.48/0.48, T2 0.73/0.63, T3 1.18/0.92, G-OUT-all 0.84/0.71, b 1.66/1.02, G-IN-all 2.10/2.99 (−0.49), G-IN-Mall 2.47/3.04 (−0.50), G-MID-T1 1.16/1.01, T2 1.75/1.23 (+1.54), b 2.41/1.56 | `ZN4_…/zn4_results.json` [J] | ng 80; no gas, BCG response; isolated spheres |
| Same at f★ 0.0615 | M3 +4.13, Mall +3.15, T3 +2.00 | same [J] | |
| Same on X-COP's gas +0.111 | 15 of 15, M3 +1.53 / +1.18 | `ZN4_…` [R] | rejected by GS4 |
| Same on eRASS1 own gas | 11 and 12 of 15, +4.53, +4.25 | `ZN4_…` [R] | |
| X-COP hydrostatic, native | +0.013, 0.075; by x −0.032, +0.011, +0.041, +0.038, +0.006; passes 94 %, 92 % of draws | `ZN4_…` [R] | HSE. Without HSE UNDETERMINED (`RF3_…`) |
| Hydrostatic bias | XRISM few % vs miss 0.12–0.16 dex | evening brief §8 [B] | |
| EM1 line + native shape on measured gas, ng 80 | 14 of 15; M3 +2.39 / +2.10 (FC1 map), +2.73 / +2.45 (frozen map); X-COP −0.042, 0.082; 0 of 100 full passes | `OP2_…` [R] | EM1 carried 2–3 dex |
| Rule N on X-COP | −0.186, 0.214 FAIL | `RG1_…` [R] | CORE, HSE |
| Groups, 63, Z | N +1.45 to +1.51 (`X80_…`, `NR1_…`) or +1.62 (see §7); native +2.08 frozen map, +1.91 FC1 map | [R] | EM1 |
| Groups hot-gas split | D negative, measured [−0.511, −0.076]; prediction D +0.311; power 0.45 | `HG2_…`, `RG1_…` [R]; but see §7 | conditioning (FM1) |
| SLUGGS | N +0.125, Zc +6.1, 1 of 4; literal R2 EXCLUDED inside r₁/₂; GC window lift +0.17 dex | `RG1_…`, `SR1_…` [R] | |
| Cluster source-size excess | SOURCE-SIDE SYSTEMATIC | `X13_…` [R] | |

### 1d. Milky Way, lensing, CGM
| Fact | Number | Lane | Depends on |
|---|---|---|---|
| MW on halo-free baryons (Valenti+16 bulge 2.0 ± 0.3e10; LN16 R_d 2.64 ± 0.13; BH&G16 thick share 12 ± 4 %) | canonical OS1 0 of 625 cells; alt, N one cell each at thick +2σ, R_T −2σ, R_t −2σ, Σ_b +1σ | `RF1_…` A1–A4 [R] | kinematics themselves not halo-free |
| MW on McMillan baryons | N V_c 202.8 vs Eilers 229.1 ± 4.6, z −5.6; K_z 67.9 passes | `RG1_…` [R] | McMillan ΛCDM-processed |
| Law on MW | K_z(R₀) 76.7–80.9 vs 66.4 ± 2.2, +4.7 to +6.6σ | `X5_…`, `GD2_…` [R] | |
| KiDS isolated lenses Δχ²(halo − law) | FC1 +434; native on EM1 +366 (χ² 520); on AM1 +2850 | `KN1_…` [R] | Brouwer+21; relative only; tested models fail absolute fit (V3S 10-27 note) |
| Amplitude A = data/model by colour, EM1 | blue 1.053 ± 0.095 (Δ log M200 +0.03), red 1.649 ± 0.083 (+0.32), all 1.494 ± 0.054 (+0.26); law 0.878, 1.313, 1.207 | `BL1_…` [R] | shape still favours law |
| Mass shift on matched G09 hosts | lensing +0.17 [+0.05, +0.28]; satellites +0.78 = method systematic | `GH1_…` [R] | |
| Inside 300 kpc, A | E k=3 1.20 / 1.16; N 1.45; law 1.45; Z 1.80; E k=1 2.19 | `RF4_…` via brief [B] | no two-halo |
| Two-halo from own counts | UNSEPARABLE: per-bin amplitude 5.5 ± 0.9, 1.3 ± 4.3, −7.8 ± 18.8, 22.0 ± 4.6, p 0.003 | `RF4_…` [R] | |
| Clean lenses | S3 NOT POWERED; S1 shortfall 2.3σ; red M★ +0.295 removes tension; S_strict Q +1.02, S_x300 +0.13; 10 of 20 classes move on clone rule | `SI1_`, `SI2_`, `SI3_`, `SC2_…` [R] | M★ scale; clone rule |
| Unseen neighbours | 0.1–0.2 M☉/pc², no help | `UN1_…` via brief [B] | |
| tSZ MW-mass centrals | no detection, null χ² 7.2/7, p 0.41 | `GH5_…` [R] | |
| FRB DM | never read; power gate failed | `GH6_…` [R] | NON-DIAGNOSTIC |
| kSZ, DR1 | A(1.8) 0.26 ± 0.19 (A = 1 Zhang's gas); M★ offset −0.19 dex gives 0.24 ± 0.19 | `GH8_`, `GH9_…` [R] | velocity pipeline |
| kSZ, DR2 published | A(1.8) 0.448 ± 0.105; miscentred 0.54 ± 0.13; A(1) 0.75 ± 0.18; gas 2.1e11 vs need 4.7e11 | `GH10_dr2_…`, `GH11_ksz_…` [R] | misfit is shape; two-halo open |

### 1e. Cosmology and strong tests
| Fact | Number | Lane | Depends on |
|---|---|---|---|
| Raw BAO native a₀(z)/a₀(0) | 0.91 [0.76, 1.03], 0.94 [0.71, 1.12], 0.91 [0.33, 1.21] at z 1, 1.5, 2.33; rival a₀ ∝ H 1.76, 2.35, 3.49; constant DE 1.97–2.61σ hint | `campaign_fresh_gravity/CFG689_…` via memory [B] | native r_d from A1 pair; K9 failed as frozen |
| RF5 a₀ on its background | canonical 9.35–9.41e-11, alt 1.129–1.134e-10; a₀(2.33) 7.3–8.1e-11 | `RF5_…` [R] | κ fitted |
| Early-dust window (raw plik-lite, DES Y3 ξ+, CPL on raw BAO + SN) | z_on ∈ [3e4, 1e6], both footings; 2e4 misses by 100; 1.2e4 fails plik; z_on ≤ 4000 and v3s khronon UNDETERMINED (not converged); forest NOT DIAGNOSTIC | `RF5_…` [R], summary [B] | grid top 1e6 |
| Abundance | light spectator fails isocurvature by 2e8–6e8; kinetic absorption Ω_c h² 1.4e-8; verdict UNDETERMINED | `X1_seedfree_abundance` [R] | carrier assumed |
| Shear attribution in theory v2 | gas expulsion M3 carries 118–126 % of lead; cold rules add 0.5–2.6 % power | `campaign_fresh_gravity/CFG963_…` [R] | |
| Cassini Q₂ | unscreened law fails 2.44–4.59× (AQUAL); screened passes by 1e7–1e9 at L★ 24–90 pc; L*_C ≤ 0.069 / 0.111 pc | `doors_push_2026_10_22/D7d_…` [R], E2 via memory [B] | applies to law with stiffness. A Newtonian route E halo has no such term |
| PPN, pulsars for C1 window | survives whole window | `X15_`, `X16_…` [R title] | v3s family |
| Wide-binary kill line | R − 1 ≥ max(0.01, 3σ_R); σ_R 0.075 at N 30,000 | `campaign_fresh_gravity/OWNER_DECISION_2026-10-21…` | MOCK |

### 1f. Zooms (collisionless dust + Λ on background A, ±ZK1 kernel; no gas)
| Mass | ng | η_conv (68 %) | η_S at ε cut | c₂₀₀ z=0 | M200/nominal | S z_f, M☉/pc² | Lane |
|---|---|---|---|---|---|---|---|
| 1e8 | | not read | | 13.75 | lg 7.94 | not read | `OP1_…` [R] |
| 1e9 | | not read | | 12.07 | lg 8.93 | not read | `OP1_…` [R] |
| 1e10 | 64 | 29.26 [27.13, 29.48] | 23.19 | 11.21 | 0.81 | 44.2 [41.3, 49.5] | `X80_`, `ZN2_…` [R] |
| 1e11 | 64 | 24.34 [24.34, 30.16] | 20.37 | 10.26 | 0.78 | 79.1 [75.3, 86.6] | same |
| 1e12 | 64 | 25.94 [23.89, 26.53] | 20.83 | not read (`zn2_low_shapes.json`) | not read | 134.9 [132.5, 145.5] | `CE1_`, `X77_` |
| 1e12 | 80 | 21.53 [14.55, 24.89]; per-seed 12–34 | | | | | `AQ1_…` [J via NR1] |
| 1e13 | 48 / 64 | 17.67 [16.73, 19.86] / 23.54 | 13.79 / 19.07 | 6.47 | 0.718 | not read | `CE1_`, `X77_`, `ZN1_` |
| 1e14 | 48 / 64 | 16.91 [15.68, 18.39] / 22.10 | 14.39 / 18.93 | 5.94 → 5.42 (ng 80) | 0.683 → 0.669 | not read | `ZN4_…` [J] |
| 1e15 | 64 → 80 | | | 4.43 → 4.09 | 0.579 (ng 80) | | `ZN4_…` [J] |

- **Cusps:** at ng 64 a/a_cusp within 0.2 in 9/9 (NFW, Einasto); NFW ratio 0.95–1.06 over 21 runs. "Zoom cores = cusp seen through the resolution cut." r_conv is on the 3ε floor in 6/9. `X81_…` [R]
- **η is flat with mass:** 0.026 per dex, 1e10–1e12, NOISE. `X80_…`. S exponent 0.242 smooth, 0.239 converged, 1e10–1e12. `CR2_…` [R]
- **η is fit-range-dependent:** 19–25 at z_f to 34–40 at z = 0 at 1e13–1e14 only because r_vir grows. `ZN1_…` [R]. ng 80 z = 0: 29.99, 23.06 at 1e14, 1e15. `zn4_readouts.out` [J]
- **Self-similar:** 1e8, 1e9 c₂₀₀ ratios to trend 0.84, 0.89; M/r² at 3ε 0.89, 0.88. `OP1_…` [R]
- **Inner frozen after z_f:** M(<r)/M(<r, z_f) at r/r_f 0.1, 0.2, 0.5, 1, 1.5: 0.975, 1.053, 1.152, 1.185, 1.229 (1e14); slope past R200 2.65–2.68. `ZN1_…` [R]
- **Resolution:** c₂₀₀ falls 9 %, 8 % at ng 80; η(1e14) ratio 0.88; η(1e12) 0.83 [0.55, 1.12]. Each ng draws its own field. No ng 80 at 1e10, 1e11 yet (NR2 running). `ZN4_`, `AQ1_` [R]
- **Boundary:** sphere RS 2.0 vs 1.5, one seed, 1e14: f_out 1.2127, f_in 1.230, M200 × 1.30 (+0.115 dex), shape 3–5 %. `VB1_…` [J]. Halo mass scales with the sphere: nominal mass is not a fixed number.
- **UV:** kick and P(k) cut move c, η_S, m(x) under 4 %. r₋₂ c_f unperturbed 10.07 vs 7.01, 7.50: mostly noise. `UV1_…` [R]
- **Spin:** ρ(S, spin) −0.453, p 0.018, 27 zooms; S scatter 0.150 dex at 1e12, 0.102 at 1e13, 1e14. `HS1_…` [R, B]
- **Limits common to all:** isolated spheres, no baryons in the shape runs, thin closing shell (median γ about −29; 94–180 of 1,318 cells outside −40 to 60), ε fixed fraction, ng 80 top.

### 1g. Contraction
| Fact | Number | Lane | Depends on |
|---|---|---|---|
| Live disc grown at 1e12, nine same-seed pairs | R_live 2.154 [1.65, 2.52]; f_Q 0.872 [0.54, 1.07]; Q live at r/R_d 2, 3, 4, 6, 10: 2.29, 1.94, 1.69, 1.47, 1.35 (Blumenthal 2.53, 1.96, 1.74, 1.46, 1.28). R_live 1.47, 1.75, 2.15 at z 0.5, 0.25, 0 | `LC1_…` [R] | gravity only, one mass; 1 R_d at 3ε |
| Contraction on FC1 rule | Υ 0.31 / 0.31 at R 1; Gnedin 0.34 / 0.35; rms 0.0728; R 0.30 still Υ 0.48 and two G-MID keys fail; clusters pass at R 1 | `CN1_…` [R] | groups uncontracted |
| Contraction on native profile | Υ 0.44 / 0.41 (f_Q 0.872), rms 0.0726; by V_flat Υ 0.55, 0.69, 0.57, 0.32, 0.40, 0.53; ΔV −3.4, −1.9, −3.7, **+22.1, +12.6**, −0.9 | `OP3_…` [R] | clusters NOT contracted, ungraded; f_Q from 1e12 only |
| HS1 tilt under Blumenthal | f 0, 0.5, 1: −0.227, −0.159, −0.100; mean δ −0.019, +0.050, +0.114 | `HS1_…` [R] | POST |

### 1h. Feedback budgets
| Fact | Number | Lane | Depends on |
|---|---|---|---|
| SN energy to soften cusp to η 21.2 | ε_req median 0.017 [0.006, 0.023], max 0.040; 74/175 active; ρ with M200 +0.59. Energy only, no channel | `BE1_…` [R] | η from CE1; E_SN per 100 M☉ |
| Impulsive outflow, gravity only, measured gas | R 0.932 (need ≤ 0.817); reached at 2.2× gas, ε_SN 1.61; coupling 0.3 misses at every cadence | `CM1_`, `CM3_`, `RF6_…` [R] | one galaxy, 40 cycles, one seed |
| Cluster energy | E_req 6.7e59 erg (1e13), 2.3e61 (1e14). SN ε 6.71, infall 10.5 EXCLUDED; BH 0.075 | `CL4_…` [R] | provisional inputs, 0.1 M_BH c² |
| BH, gravity only | best R 0.986 (need 0.845), 0.917 (0.809); uncapped 0.948, 0.917 | `BH1_…` [R] | closed box |
| Central load needed | 0.02–0.05 M200, 4–11× in-place; 1e14 R 0.79–0.81 | `BH2_…`, `RF6_…` [R] | stipulated |
| Gas cycles | NOT REACHED at ceiling: R 1.025, same-gas control 0.917; cap 0.0283 above X-COP 0.0086–0.0186; reached only at 0.0566 | `CL5_…`, `RF6_…` [R] | robust on measured gas |
| One coupling | galaxy ε 0.00128 vs cluster 0.078, ratio 61 (alt 57); two fractions on two sources 0.116 vs 0.078, overlap only, ε rises with mass inside SPARC | `OC1_…` [R] | bookkeeping only |

### 1i. Argon's claims, scored
| Claim | Measured | Score | Source |
|---|---|---|---|
| η(ng 80)/η(ng 64) 1e14 1.09 ± 0.05 | 0.88 | WRONG sign | `AQ1_…` |
| c_f(1e14, ng 80) 10.8; c_f(1e15) 11.6; η ratio 1.11 | 6.12; 6.54; 0.97 | WRONG | `AQ1_…` |
| X-COP at ng 80 barely survives; c₂₀₀(1e15) 12–13 | +0.013, 0.075; c₂₀₀ down 9 % | WRONG | `AQ1_…` |
| G-OUT-M3 > +2.5 at ng 80 on measured scale | +4.41 | RIGHT | `AQ1_…` |
| η_conv(1e12) ratio 1.035, η 25.5; c_f 7.95 | 0.83 [0.55, 1.12]; 21.5; 7.43 | WRONG, ratio noise-limited | `AQ1_…` |
| VB1 ΔΣ outer +18 to +24 % | +21.3 ± 1.2 % | RIGHT number; stated at 2.25, run at 2.0 | `VB1_`, `AQ1_` |
| VB1 ΔM(<0.7 R500) +1.8 %, ΔM(<R200) +5.5 %, M3 → +2.4 | +23.0 %, +22.9 %, +4.41 | WRONG, mechanism not what happened | `AQ1_…` |
| Velocity kick removes spike, c_f 4.5–5.5 | no effect | WRONG | `UV1_…` |
| HS1 slope +0.085; law 0.00 | −0.227; −0.016 | WRONG sign; law CLOSE; test right | `HS1_…` |
| LITTLE THINGS lines | fail 200 of 200 | WRONG | `ND1_…` |
| ZN1 G-IN-Mall worst, −1.65 | −1.73 | RIGHT; class X-COP ONLY reversed | `ZN1_…` |
| ρ₁₀ 1.25, ρ₁₁ 1.126; ρ₁₁ 0.96, ρ₁₀ 0.92 | 1.128, 0.938 | ρ₁₀ first HIT, ρ₁₁ second HIT; two different predictions | `X80_`, seal reply |
| c_f formula 14.26, 9.62 at low mass | 7.36, 6.64 | WRONG | `X80_…` |
| Live contraction fail lines (1.25, 1.45) | 2.15 | fail line reached, as Argon's test said | `LC1_…` |
| Retention curve f_ret; "outer over-prediction was template artefact" (D6); group estimate Z −2.8 to −3.4 | rejected as knob; BA2 no class change; inputs inconsistent | NOT RUN / WRONG / NOT A RESULT | scored reply, seal reply |
| Assembly-epoch multipliers | 4–7 % vs 40–50 % needed | WRONG | `AE1_…` |
| Numeric checks of 10-31 | Ω_m(z_f), σ(M) table wrong; S × 1.26 conclusion right | MIXED | `ARGON_REPLY_2026-10-31` |
| Stop seal | cluster half fires on measured gas only; galaxy branch 1 not armed; "95 % CI" undefined; "and" vs "or" unstated | UNRESOLVED; questions pending | `ARGON_QUESTIONS_2026-11-01.md` |

---

## 2. CLOSED DOORS
D = decisive on inputs tested. C = conditional on the named input. All are numerical, none a theorem.

**Core shape and tails.** X68 reshape at fixed mass: zero-sum (D). X70_soft_floor, X69: soft floor, split Burkert, cored NFW fail; soft floor shifts 53 % of SPARC (D). TL1, GC3, GX1: r⁻⁹ᐟ⁴ or infall tail, χ² 190 vs 141, law 66; fixes X-COP or outskirts, not both (D). X40, X40b: fixed core radius, no native rule raises cluster Σ (D). IJ1: isothermal Jeans at BU1's cross-section, cores too small (C: cross-section). X44, X45: c_f ≈ 4 from self-similar infall (1.85) or peak curvature: no (D). SC1: self-coupled law SPARC only (C). CS2: atlas law no better out of sample (C). OS1: Σ ∝ σ^q breaks dwarfs (C).

**a₀ floor and acceleration keys.** X65–X67 gated, quarter-a₀, tidal AQUAL (D). X47 tether (D). X50 floor ≠ phantom (D). PS1, PS2 phase-space cap (D). DF1, DW1, X28 named-physics floor, flattening, acceleration key (D). X25_floor velocity floor ≠ sound speed (D). X80 no plateau: R 0.414 at 1e10 (C: ng 64). Dielectric exclusion = law's phantom (D). MF1 H₂ cooling mass: NOT DIAGNOSTIC (C). Bounded-boost ceiling: calculus wrong (D). X56 "never weaker than law" fails (D).

**Switches and selectors.** J1, X19 potential, σ, acceleration keys (D). X58 mass-keyed (D). X59 formation epoch (C: EPS). X62 environment: nothing passes at any c_f (D). X61 high-z: NOT DIAGNOSTIC. X31 feedback selector, CFG914 density threshold, CFG919 pressure support, CFG921, CFG928 posits: no common ordering (mostly D). DT1, CF1, CF2, CL1–CL3, BS1, CSM1: threshold and switch family; HO1, HO2 held-out fail (C). X57, X60: exclusion, two-phase: not established.

**Cold-sector dynamics and conversion.** X37 conversion to DE with orbits (D). X54, X23, X24b, X29, DH1, CFG958: exchange or late heating: raw KiDS halves the sheet, wrong sign (C). X34, RF5: late release z_on < 1e4 fails raw χ² (D for 1.2e4; UNDETERMINED below 4000). PH1, M1, M5, X26, X30: two-phase, trilemma, equilibrium (C). CFG930, CFG932 energy-limited settling, all 36 corners (D). CFG965 stiffness lump (D). CFG949, CFG959 FRAGILE. CFG915 population labels, CFG913 mobility CONTRADICTED.

**Baryon response.** X39, CN1, LC1, OP3: full contraction breaks SPARC on every rule, Υ 0.31–0.44 (C: f_Q 0.87 from one mass; no compensating channel run with gas). CM1, CM2, CM3 outflows: reach at coupling 1 only (C, RF6). SH1 SN softening alone fails; pass needs R 0.685 at clusters, unsupplied (C). BH1, BH2, CL5 BH channels at clusters (D for CL5 on measured gas). CL4 SN, infall in clusters (C: provisional). OC1 one coupling misses 60× (D as bookkeeping; dissipative portal unmodelled). AE1 assembly epoch (D). BC1 BCG in stars already (D). GT1 gas-state rule, M3 +3.25 / +2.72 (D). DS1 hot displacement (D). NM1 member halo pooling (D). X52 tidal truncation at current distance: no effect (C). X51, CFG934, CFG937 cooling floor: partial, fragile (C).

**Masses.** X55 one relation for SPARC + KiDS: 4.6σ, 4.3σ on all colours; BL1 shows blue need none (C). AM1 native match breaks SPARC, rms 0.168 (C: PS, single colour). X76 fair share on observed baryons 0.2–0.3 dex lighter than EM1 (C). MA1 budget M200: passes z = 0, G-IN-Mall −2.33 at z_obs; ZN4 fails with it (C). G2 pre-infall retention (D on native). OP1 free line = post hoc (C).

**Native concentration and η.** X48, X74, NL1, FP2: r₋₂ c_f breaks SPARC, estimator artefact (X77), so these verdicts are weak as to c_f (C). CE1 converged η on the floored rule: FAIL both f★ at ng 48 clusters (C: rule since removed). A5 c_f 7.43: SPARC SETTLED FAIL on c_f rule (C). X76_cf scatter P_line 0.001 (D). UV1 kick, P(k) cut (D). VB1 boundary at RS 2.0 (C: one seed; 2.25 not runnable on grid). ZN4 resolution as cluster cause (D to ng 80).

**Gas scale.** GS4 offset as cluster fix, 5 SE (D). GS5 agrees (C: A1). GX2 eRASS1 correction no (D). CFG922, CFG929, NU1: baryon census cannot close excess (D). HL2 no mass gap (C: R₅₀₀). CFG967 catalogue two-halo no effect (C). X2, X30 sheet (C). GA1, DY1, AP1 HG2 sign audits: see §7.

**Lensing and CGM.** GH2–GH11 fair-share CGM to 1.82 R_vir: BELOW NEED (C: shape, two-halo). RF4 two-halo template unseparable (D for own-count template). KN1 native on KiDS (D relative). UN1, UN2 neighbours, group skirts (C). X79 native η for MW, KiDS (C). ZT5 SPLIT.

**Carrier, abundance, κ.** QC1 QCD volume, chance level, slip (D). CR1 R1–R7 none survives (C). CR2 self-coupling origin of slope, alt invalid (C). X1 light spectator isocurvature, 2e8+ (D at computed points). CFG893, CFG897–CFG911 κ doors: ½ only in menus or posits; none derives (D as far as tried). DSF-21, GF2 "κ derived": restatements (D). CA1 covariant self-coupling: shape only, one new constant (C).

**Covariant family.** v3s frozen: passes as galaxy law, fails as gravity + cosmology, growth rows relabelled UNDETERMINED by RF5. AeST H2, MOG X9, braneworld K1, Q7 DBI, CFG938 (ill-posed on FRW), CFG944–CFG954 LDT, SCT: not surviving or partial; not reread here [B].

**Other.** IC 1613: EF1 external field, FD1 about half the gap, IN2, RF2 inclination (C: e_int). Z2, X20, X25, X24 hosted-dwarf systematics: extra stands, mass trend. S1 hosted: see lane. CFG892 binaries in classical dSphs: see lane, not read.

---

## 3. FITTED, BY-HAND, OR UNDERIVED
| Number | Value | Origin | Used by |
|---|---|---|---|
| κ | ½ | FITTED on the law. `CFG894`–`CFG911`; DSF-21 = Milgrom 1999 postulate | a₀ law only since 10-31 |
| a₀ footing | ρ_Λ (9.3603e-11) or ρ_total (1.1312e-10) | choice; alt needs κ ≤ 0.44 (X78) | law |
| M200 line a, b | 11.18, 0.90 | fitted on SPARC against the law; slope 0.90 has no origin (OP2) | N, OP2 |
| f_c | 0.8405 | native Ω_c/Ω_m "as quoted by FC1"; Ω_c, Ω_b from background fit, abundance UNDETERMINED | N, native |
| f★ | 0.034, 0.0615 | measured range, both reported | clusters |
| η(M) | 25.94, 23.54, 22.10 (ng 64 anchors) ; ρ₁₀ 1.128, ρ₁₁ 0.938 | measured, but estimator choice (cusp fit at x_c 0.001, smooth-core form); scatter 12–34 | N |
| Core shape | smooth core ρ₀/(1 + x²)^(3/2), or Burkert | "stays chosen by hand (X70)"; relayed from external model; zooms give cusps | N |
| c_f = 4 | external, formation concentration | never native; c_f-equivalents 5–8 | X43, floored rules |
| η_S 10.82 | from c_f = 4 | not native | X70–X73 |
| Limits η 21.2, 14.3 | SPARC Υ floor, G-IN-Mall | grading limits, set by data + rule | CE1, BE1, CL4 |
| Υ 0.50 and window 0.50–0.80 | line | stellar-population prior, grader's | all SPARC |
| q_f | 0.892 / 0.748 | fitted on SPARC | OS1, GR1 |
| ε cut | 0.01 r_f | numerical; sets x_c 0.03 | X77 values |
| z_f | collapse redshift tag (1.326 at 1e10, 1.137 at 1e11, 0.56 at clusters) | convention | Σ_coll |
| Δ_vir | 18π²ρ_m in X77, X43 | convention, against keys' M definition | η |
| RS 1.5 q_M | zoom sphere | numerical; M200 × 1.30 at 2.0 | all zooms |
| f_Q 0.872 | LC1 | measured at 1e12 only; carried to all SPARC masses | OP3 |
| q_contract 0 at clusters, ε in SL2 | by hand, fitted | SL2's own label | SL2 |
| Gas scale | +0.005 (measured), +0.092, +0.111 | measured vs chosen | ZN4 |
| h | 0.672, 0.686, 0.70 | native backgrounds and eRASS1's | clusters |
| Ω_c/Ω_b | from background, not derived | G16 open; QC1 fails | everywhere |

---

## 4. OWNER DECISIONS IN FORCE
1. **10-31, floor out.** "Working rule from now on (native version N): S_cold(M) = f_c η(M_t) Σ_coll(M_t) at every mass, M_t = M/f_c, with η from the native zooms: ρ₁₀ 1.128, ρ₁₁ 0.938 (X80), CE1's table above that. The fitted-slope variants N1 and N2 are not adopted… The core shape stays chosen by hand (X70)." `OWNER_DECISION_2026-10-31_NO_FLOOR.md`. Same file: "a₀ leaves the cold sector"; "The a₀ law is now a separate statement"; retired "the RAR and the a₀ line emerge" and Σ_floor(z) ∝ a₀(z). The later "working statement" in that file is marked "not a new owner decision".
2. **10-25, flagship.** "Law + cold dark energy" as PAPER61's theory; draft only, no Zenodo deposit until owner says go. Memory `project_owner_adopts_law_plus_cold_dark_energy.md`; `THEORY_PROGRESS_SUMMARY_2026-10-31.md` §1 [floor part superseded by 10-31].
3. **Name.** Cold dark energy, never "cold dark matter" or "CDM-like" (10-25). Memory `feedback_cold_fluid_name.md`.
4. **Raw or native only.** Raw measurements against framework's own predictions; 10-25 "ΛCDM IS NONSENSE, DO NOT USE IT": no Planck 5.364, no ΛCDM background, no "passes by construction". Memory `feedback_raw_data_framework_native.md`.
5. **10-23 board rule.** Board = current best theory only; recompute every tile. Memory. Main board still v3s; see §7.
6. **10-20 ALMA, 10-21 DR4.** `campaign_fresh_gravity/OWNER_DECISION_2026-10-20_ALMA_GOVERNING_PLANS.md` (CFG806, CFG809 govern; one disc excludes nothing, per index line). `…2026-10-21_DR4_KILL_LINE.md`: "Gaia DR4 kills the sealed wide-binary prediction (CFG740) if and only if R − 1 ≥ max(0.01, 3σ_R)". DR4 prereg frozen. Dates: ALMA 11-06, 11-28; DR4 12-02.
7. **10-30 queue.** X80 before A5 (`X80_…/AMENDMENT_A1.md`).
8. **Standing:** no dark-matter particle; never "theory closed"; never say data favour the framework; v3s "theory frozen, no new lanes"; no deposit without go; preemptible heavy compute (10-23); SM bridge walled unless a new forced kernel.
9. **Open, awaiting owner** (`CLOSURE_TABLE_2026-11-01_DRAFT.md`): retire route E's cold sector, keep, or conditional; accept HL1 A1, GS5 A1; restate G8; PAPER61, PAPER65 still carry the floor.

---

## 5. SCALE TABLE
"Asks" comes from data at a stated assumption. "Gives" comes from zooms with no baryons. `—` = nothing measured. S in M☉/pc².

| lg M200 | Data ask (assumption) | Zooms give | Gap / flag |
|---|---|---|---|
| 8 | Dwarfs: S_min 31–78 (no M200; lower bound). Free line wants about one mass 9.25–10.05 at lg M★ 4 (not 5.78) | c₂₀₀ 13.75; S not read | M200 at this scale UNMEASURED except as a fit. Dwarf mass, not shape, is the miss |
| 9 | Same; rule S 29.4 below every class | c₂₀₀ 12.07; S not read; rule extrapolated | **Flag:** no direct S comparison; EM1 carried 3–6 dex |
| 9.97 | S_need 68.6 [51.6, 85.0] (EM1, Υ 0.5); free r₀ 70.2 | 44.2 [41.3, 49.5] ng 64 z_f; cold rule S 53; η_conv 29.3; c₂₀₀ 11.21 | need/give about 1.3 on rule; ng 80 running. M200 weak link. Υ 1.20 |
| 10.59 | 102.7 [81.0, 124.2]; free 107.7 | rule 69 | about 1.5; Υ 1.14; HS1 tilt here |
| 11.13 | 143.2 [118.4, 199.8]; free 157.5 | 79.1 at 1e11; rule 90; η_conv 24.3 | about 1.6; Υ 0.86 |
| 11.76 | 150.2 [97.9, 190.5] | rule 134 | inside; Υ 0.54. Contraction gives ΔV +22 here |
| 12.11 | 215.1 [136.6, 272.1]; KiDS Δ +0.17 to +0.32, blue +0.03 (EM1) | 134.9 ng 64 at 1e12; rule 162; η_conv 25.9 → 21.5 ng 80; contraction R_live 2.15 | inside before contraction. Measured contraction needs a compensating response of about the whole effect |
| 12.27 | 411.7 [181.6, 596.0] | rule 175 | ΔV −55; law −40 too; small n (10) |
| 13 | Groups Z within 2 (+1.45 to +2.08); η ≤ 14.3 for G-IN-Mall on the floored S rule; S_need extrapolated ratio A/f_cη 2.18 (CR2) vs clusters' limit | η_conv 17.67 ng 48, 23.54 ng 64; c₂₀₀ 6.47 ng 64; M200/nominal 0.718 | **Flag:** two opposite reads: shear limit says over, S_need extrapolation says under. No ng 80 at 1e13. Groups have lower bounds only (CS1) |
| 14 | Keys: inner limit η ≤ 14.3; X-COP passes with native; outer meas/pred 1.5 in M3, Mall; G-MID-T3 1.35 (measured gas). Baryon share log Y −0.12 to −0.135 on same shear | η_conv 22.1 ng 64; z = 0 profile c₂₀₀ 5.42 ng 80; M200/nominal 0.67; inner frozen | Inner profile OK on keys (G-IN −0.5), outer short. **HSE and shear disagree 0.12 dex at fixed gas; unresolved** |
| 15 | X-COP only, hydrostatic; M3 reaches M500 5.6e14. No HSE-free mass on disk | c₂₀₀ 4.09 ng 80; η z = 0 23.06; M200/nominal 0.579 | **Flag:** nothing HSE-free measured |

Mass-line comparison at each scale, relative to EM1: dwarfs × 10³–10⁴ (fit), blue KiDS +0.03, G09 +0.17, red +0.32, AM1 +0.7 at lg M_b 10, X76 fair share −0.2 to −0.3, cluster fair share about −0.11 at lg M_b 13.5 (14.22 vs 14.33).

---

## 6. UNEXPLOITED (measured regularities with no follow-up lane that I found; grep-based, could be incomplete)
1. **MGAS-tercile vs KT-tercile outer keys.** On measured gas, meas/pred is M1 1.88, M2 1.50, M3 1.50, Mall 1.55, against T1 1.00, T2 1.16, T3 1.28, all 1.18. Ratio computed by me from `ZN4_…/zn4_results.json`; no README states it. Note X21: KT detected, MGAS500 not. Errors are large on M1. May partly reflect the template history (`BA2_…`).
2. **S_need/Σ_coll one number:** 32.4 ± 1.9, χ² 5.35/5 over 20–400 km/s (`CR2_…`). SL2 is now testing a related ratio; amplitude not derived.
3. **Need/native ratio 1.2–1.6 at Υ 0.50** across SPARC, A/f_cη 1.49, 2.18, 2.28 at 1e12–1e14 (`CR2_…`). Flat-ish step, not run against a mechanism.
4. **S_min has no correlation with r₁₂, M★, g_N** (−0.24, −0.02, +0.31), band 46–64 (`SN1_…`). Noted, "not adopted"; no lane asks why it's near-constant.
5. **Near-common dwarf mass 10^9.25–10^10** (`OP1_…`): untested against tides, counts or host budget, as the README says.
6. **EM1 crosses fair share near lg M_b 14** (`OP2_…`, K2: 14.33 vs 14.22), "may be a coincidence".
7. **Υ pattern.** Falling from 1.20 to about 0.54 at 150–200 km/s, then rising to 0.74–0.78 at 250–400, in N and native alike (`X80_`, `ZN2_`, `OP3_…`). ET1 grades bulges; no lane targets the V-shape.
8. **Shortfall at 250–400 km/s common to law and all halos**: −40 to −55 km/s (closure G6). n 10. No dedicated lane in the window beyond ET1, LS1.
9. **Blumenthal reduces HS1's tilt:** −0.227 to −0.100 at f 1 (`HS1_…`). OP3 graded contraction on the native profile; HS1 under LC1's f on the native profile not found.
10. **S vs spin,** ρ −0.453, p 0.018 in 27 zooms (`HS1_…`), right sign, about half the need. No lane propagates S scatter ranked by spin onto SPARC.
11. **M200/nominal falls with mass:** 0.81, 0.78, 0.718, 0.669–0.683, 0.579; and VB1's × 1.30 with sphere size. ARGON_QUESTIONS item 2 asks; no lane corrects nominal tags.
12. **GS4's scatter 0.177 dex and X-COP's own +0.122 while others read about 0:** cause of X-COP's high read (`GS4_…`) not pursued beyond SM1's definition mismatch.
13. **GS5's split:** low-z, large-θ +0.07 ± 0.025 vs distant 0.00 (`GS5_…`).
14. **LF1 depends on Rmax:** −0.135 at 3 Mpc vs −0.086 at 2.06. Mass outside aperture "not excluded"; no test.
15. **Two-halo amplitude by lens bin** 5.5, 1.3, −7.8, 22.0 (`RF4_…`): called a template failure; not studied as a signal.
16. **kSZ shape:** "no template has the 2′ dip"; rise past 0.9 Mpc (`GH10_`, `GH11_…`).
17. **Colour split in KiDS:** blue +0.03, red +0.32 (`BL1_…`) while the law has A 0.878 and 1.313 on the same split. Red M★ scale (+0.12 measured, +0.17 IMF) "not yet pushed through RF4's grade" per evening brief §5.7.
18. **Outer cluster shear ∝ Mgas^0.9** (`CFG687`; richness split `CFG688`, not read). Evening brief does not list it.
19. **OP2 + OP3 never graded together;** contraction on clusters ungraded (closure table "not settled").
20. **ZN1's late mass lands outside r_f, inner frozen,** vs `M_fair at r_ta 3.4 M200 vs zoom's 2.2` budget mismatch (memory, ZN1). Budget disagreement not followed.
21. **Peer side-lanes in `X48_…/stable_stress_search/`, `gravitational_strain/`:** entropy polytrope with finite core equilibria and weaker contraction; collapse pilot "heats and bounces". Not graded on any gate; not read beyond the header.
22. **Baryonic dynamical friction,** f_clump 2–3 %: "still untested" (evening brief §4). Not a measured regularity, but a stated gap.

---

## 7. CONTRADICTIONS
1. **Rule N's HS1 slope.** Closure table G1t and evening brief give N −0.227 ± 0.069. That is N1, which the owner did not adopt. ND1: native N −0.173 ± 0.064 (−2.70σ). Owner file −2.70σ is right for N.
2. **N's groups Z.** Closure G2 and brief: +1.62. X80, NR1: +1.45 to +1.51. OP2 says `+1.62` is the grader's S-rule path. Not reconciled in the closure draft.
3. **ZN2 frozen read.** Owner file and evening brief: Υ 1.01 / 0.97. README_A1: 0.84 / 0.81 with low-mass zooms; the earlier value was clamped. Both FAIL, but the quoted number is stale.
4. **RF3's knife edge** G-OUT-M3 +2.03 at ng 64 vs ZN4 +2.10 at ng 80. Failures §E still says resolution undetermined: superseded by ZN4.
5. **G-OUT-M3 at GS4, f★ 0.0615:** +4.06 (§E, RF3 memory) vs +4.07 (ZN4's ng 64 column). Trivial.
6. **RF1's README title** says UNDETERMINED; its A1–A4 block and §E say canonical FAILS. Title stale.
7. **X77 "lands at the window at every mass"** (memory index; README body) vs its own A4 read: × 1.33, × 1.32 over limit at clusters. Memory stale.
8. **η has at least five meanings:** X77 η_S at ε cut; X81 η_conv with no cut; ZN1, ZN4 η at z = 0 (29.99, 34.06); η from c_f = 4 (10.82, 14.83); c_f-equivalent. Tables mix them; AQ1's ng 80 ratio 0.88 is z = 0, NR1's 0.83 is η_conv at z_f.
9. **c_f at 1e14:** 10.07 (ng 64 r₋₂), 6.12 (ng 80 r₋₂), 7.08 (η-equivalent ng 64, `NR1_…*.out`), about 5 (X77 ng 48). SL2's criteria name 7.08 and reject the relay's 10.1. UV1, X77 call r₋₂ noise, but AQ1 scores Argon against it.
10. **Halo-mass direction.** X76 fair share on observed baryons: EM1 too heavy by 0.2–0.3 dex. AM1: EM1 too light by 0.7 dex. KiDS: too light by 0–0.32. OP1 dwarfs: too light by 3–4 dex. EM1 "3–4 times too common" (AM1) vs "2.7–4.1 halos per galaxy" (memory): consistent.
11. **HG2's negative sign.** GA1, DY1, AP1: survives. FM1: conditioning artefact, the statistic cannot see an excess. RG1 still grades D +0.311 as FAIL against [−0.511, −0.076]. Later lanes didn't reconcile this with FM1.
12. **Clean-lens tension.** SI2 title "tension gone"; SC2 "neither reads TENSION GONE"; SI3 NO VERDICT; closure says open. The difference is frozen clone rule vs per-lens, and M★ scale.
13. **BE1, CL4 "sufficient if coupled" vs CM1, BH1, CL5 "not reached".** Different questions: energy budget vs a gravity-only channel. Often quoted without the distinction.
14. **GH11 frozen Q3 prints BUDGET SUPPLIED; README reads NOT SHOWN.** Memory says never quote.
15. **Main board.** Memory (X38 line, owner 10-29): rebuild main board for route E after A4. Owner file and memory 10-31: "main board stays v3s". Not resolved.
16. **Current theory labels.** Memory index lists v3s "CURRENT THEORY" (10-23) and flagship law + cold dark energy with floor (10-25); owner 10-31 removes the floor. The `V3S` file and PAPER61/65 still reflect earlier states. THEORY_PROGRESS_SUMMARY §1 still states Σ ∝ σ^q, q on SPARC.
17. **S_min band:** SN1 frozen 46–64 vs owner file's "flat S of about 56–85 with a shallower M200 line". Different fits, not flagged where quoted.
18. **OP1's P3.** Frozen shares (0.48–0.75 inside 3ε) were actually inside 9ε; corrected to 0.00. The body table above the correction still shows the old values.
19. **Local Group, "4 of 5".** X49 title still says a₀-floor halos fit four of five; that rule is removed. Separately, the rule N and native numbers differ: +0.758 vs +1.186 at UF, so "Z +3.1 to +6.6" applies to rule N only.
20. **Argon "6 of 7" vs "all wrong sign".** Memory says all resolution lines wrong sign; AQ1: η(1e12) band covers Argon's value, so that one is noise-limited.
21. **ID collisions:** X1, X20, X23, X24, X25, X69, X70, X74, X76, X77, X78, GH10, GH11, IC1 each name two lanes. Cite full directory names. "X80" in older files may mean X81.
22. **Group-scale sign in §5.** The S_need extrapolation (CR2) and shear limit point opposite ways at 1e13; no lane compares them directly.

## Unverified flags
Numbers tagged [B] came from briefs or memory and were not opened in the lane: CFG687, CFG689, E2, X25 tides, HS1's gas-dominated −0.311 and spin line (partly in README), RF4's inside-300 kpc table, UN1, XRISM line, closure G6. `S at z_f` for 1e8, 1e9, 1e13–1e15 and c₂₀₀, M200/nominal at 1e12 were not read, though they probably exist in `zn2_low_shapes.json` and the X77, X80 outputs. Closed-door lines for covariant-family lanes rely on title lines and memory.
