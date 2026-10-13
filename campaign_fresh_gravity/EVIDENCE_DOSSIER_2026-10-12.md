# Evidence dossier, 2026-10-12

A single record of every raw-data test of the framework that the committed record has scored, what each one found, and the predictions sealed before their data exist. It makes no new claims and runs nothing new. Every number is copied from a committed file and cited by lane ID and path (all paths relative to the repository root). Sources: `campaign_fresh_gravity/THEORY_v2_CANDIDATE_2026-10-12.md`, `THEORY_v1_2026-10-09.md`, `ASSESSMENT_2026-10-09.md`, `STANDING_2026-09-29.md`, `LEDGER.md`, `CFG678_one_action_contract/SCORECARD.md`, the sealed lanes listed in §3, and `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`.

κ = ½ is fitted. The two a₀ footings are reported separately and never pooled. The cold energy's mass is an input. No dark-matter particle is proposed. No closure is claimed, and no preference of the data for the framework over ΛCDM is claimed (`STANDING_2026-09-29.md` §5).

---

## Summary (plain English)

1. **Strong:** the law fits raw SPARC rotation curves at 0.100 dex rms with one fitted constant (Newton: 0.2755), and the round cold-energy rule beats the MOND phantom disc on the Milky Way's vertical force. Removing cold energy breaks clusters, the Bullet Cluster and Local Group timing while leaving galaxies unchanged (CFG4, CFG514/516, CFG624), so the cold energy's mass is required.
2. **Failing:** on raw KiDS-1000 cosmic shear, Theory v1's settling rule is excluded (Δχ² +68.7, CFG596). The capped condensed-baryon source is still narrowly excluded (+14.0, CFG636). Both results depend on inherited ΛCDM initial conditions. Massive early-type galaxies at 50–100 kpc are short of mass (CFG529; CFG669 Z 3.4; SLUGGS CFG528b).
3. **Open:** no varied action produces the theory (CFG678: no candidate passes). κ = ½, Ω_c/Ω_b = 5.364 and the settling rate α are inputs, the energy receiver is unidentified, and the merger verdicts are provisional.
4. **What decides it next:** the framework-native 1024³ raw-KiDS run of Theory v2 (CFG650 T12, then T1; due 2026-10-13/14), then the sealed ALMA predictions (2026-11-06, 2026-11-28) and the sealed Gaia DR4 predictions (2026-12-02).
5. Gaia DR4's wide binaries can only kill candidate B, never confirm it, because Newton and ΛCDM predict the same γ = 1.000.

---

## 1. The law and the theory

**The law, in one line:** a₀ = κ c √(G ρ_DE), with κ = ½ **FITTED** (measured κ = 0.42 ± 0.10 canonical / 0.35 ± 0.08 alt, CFG493, "consistent but not discriminating"). The two footings are a₀ = 9.36 × 10⁻¹¹ m s⁻² (canonical, ρ_Λ) and 1.13 × 10⁻¹⁰ m s⁻² (alt). They are never pooled (`THEORY_v2_CANDIDATE_2026-10-12.md` §2 A1). The kernel is g = ν(g_N/a₀) g_N with the repaired ν_mono (A2). The law also implies a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)) (A4, CFG549).

**Theory v2 (candidate) in one sentence** (verbatim, §1):

> Gravity's acceleration scale is set by dark energy, a₀ = κc√(Gρ_DE); a cold, collisionless, gravity-only component ("cold energy", Ω_c/Ω_b = 5.364) settles into the profile that this law demands **only around a bound system's own condensed baryons (stars + cold gas) and only from that system's own supply**, handing the released energy to dark energy; everywhere else (hot halo gas, cluster outskirts, filaments, mergers, the early universe) cold energy remains ordinary cold matter.

Status: candidate. It replaces Theory v1's settling rule, which raw KiDS-1000 excluded (CFG596). It has not yet had its own framework-native raw-data test (CFG650).

---

## 2. What the data say

Labels:
- **RAW**: measured data against a framework-native prediction (owner rule 2026-10-10, `ASSESSMENT_2026-10-09.md` header).
- **CONTEXT ONLY**: the prediction or yardstick uses ΛCDM machinery (HMcode, BAHAMAS, ΛCDM halo mass functions, SHMR, Tinker/Duffy). It carries no verdict weight.
- **COND-IC**: a native PM verdict that is conditional on inherited ΛCDM initial conditions and background (astra audit 5c31fcad4: "tests candidate B's settling on inherited ΛCDM initial conditions and background, not the law or every completion").
- **BENCHMARK**: compared with the same-pipeline S0, not with data (5c31fcad4).

"Verdict as frozen" is the source lane's own label.

### 2a. Passes and consistent results

| # | test | data | framework result | competing expectation on record | verdict as frozen | lane |
|---|---|---|---|---|---|---|
| P1 | SPARC radial acceleration relation | RAW (SPARC) | weighted rms 0.1003 / 0.0991 dex (ν_mono, can / alt) against the frozen line ≤ 0.110; no-cold-energy run 0.100 / 0.101; astra 0.133–0.137 dex on 2,693 points | Newton (GR + Λ, ν = 1): 0.2755 dex, fails the same line | PASS | CFG4_galaxy_law (`STANDING_2026-09-29.md` §1, RE-RUN-CLEAN); CFG624; CFG678 C2 + MUTATE; Theory v2 §5 |
| P2 | Milky Way vertical force, round cold energy vs phantom disc | RAW (MW vertical-force data) | round rule beats QUMOND's phantom disc in 32/32 cells; MUTATE restores the rejection | QUMOND phantom disc rejected | PASS (vs the phantom disc) | CFG514, CFG516 (`ASSESSMENT_2026-10-09.md` Passes) |
| P3 | External outer rotation-curve slopes | RAW (153 SPARC galaxies) | mean Δslope −0.003 / −0.009 ± 0.02, including galaxies where the law predicts a decline | — | PASS (no bias); localises the MW slope tension to the MW | CFG533 |
| P4 | Groups on the baryonic Faber–Jackson relation (Tian+26, 1,400 systems) | RAW (published relation) | consistent supply closes groups at +0.06 to +0.00 dex (+0.03 / +0.01 with the paper's aperture); slope followed over 7 dex in g_bar | — | PASS (CFG540's +0.15 dex was an accounting error, RESOLVED) | CFG540, CFG543 |
| P5 | X-COP inner band and Bullet main core, condensed source (Theory v2) | RAW (X-COP; Paraficz+16 lensing, PROVISIONAL) | derived reservoir: X-COP inner band 0.86 / 0.89 PASS; Bullet main z +0.30 (core 0.79 of lensing) | under candidate B's own rules the reservoir is empty: X-COP η 1.82 / 1.68 and Bullet main z −3.4, FAIL | PASS (inner band, main core only) | CFG637 (criteria e67940c56, result e56fe96ba) |
| P6 | Primary CMB safety | structural check (engine) | only extra source is the catchment-gated term; P1 ≡ P0 at z_i = 49; expected turnaround peaks in the last-scattering volume 10^−1232 | — | PRIMARY CMB SAFE | CFG649 (966658646) |
| P7 | Tidal dwarfs, ownership rule (Arm C) | RAW (Lelli+2015, six tidal dwarfs) | Newtonian: χ² = 1.09 for 6 | the law acting with the host's external field is worse by Δχ² = +5.2 to +12.0 | passes its own kill test | `PREREGISTRATION_DR4.md` Arm C (c) |
| P8 | MW classical dSphs; massive HI discs | RAW | 1.06 / 0.74σ (CFG42); −0.028 ± 0.066 (CFG41, CFG53) | — | PASS [RE-RUN-CLEAN] | `STANDING_2026-09-29.md` §1 |
| P9 | Coma UDGs; X-COP identity; Bullet (candidate B, carried from GATES.md) | RAW | 1.33 / 1.11σ (CFG31); X-COP 0.946 ± 0.080 and Bullet 4.6× / 4.9× (CFG4_clusters) | — | PASS (REPORTED-ONLY, later RE-RUN-CLEAN per the 09-29 verification sweep); X-COP and Bullet superseded by CFG637 (P5, F7, F8) | `STANDING_2026-09-29.md` §1, line 80 |
| P10 | MW satellites under the census edge | RAW | 2/39 unbound | — | PASS | CFG515 |
| P11 | Local a₀ from MeerKAT MIGHTEE-HI (47 deep discs) | RAW (catalogue + raw-spectrum widths) | a₀ = 1.31e-10 (68% 1.27–1.42e-10; recipe ±0.128 dex), frame-corrected; with the flux-scale systematic, 0.9–1.31e-10 | — | CONSISTENT with the alt footing (+0.064 dex); canonical +0.146 dex, just outside the recipe width, bracketed only on the single-dish flux scale | CFG301, CFG304, CFG306, CFG309 (`STANDING_2026-09-29.md` §a₀ local level) |
| P12 | κ from three M/L-insensitive routes | RAW | 0.42 ± 0.10 / 0.35 ± 0.08 | — | CONSISTENT BUT NOT DISCRIMINATING (floor = HI flux scale; kernel choice moves κ more than the ½ vs 1/√π gap) | CFG493 (01e24734d) |
| P13 | Cassini quadrupole | RAW (Cassini Q₂ bound) | κ = ½ survives in the filtered chassis over ξ ∈ [0.030, 0.15] pc, both footings (floor +1.1 / +1.5σ) | bare ν_mono fails +8.7 / +9.7σ; strict AQUAL fails 3.8–5.5× | CONDITIONAL (CFG678 C1 COND) | CFG357; CFG678 |
| P14 | Local Group timing, with cold energy | RAW (M31 tangential motion, full errors) | shared-catchment rule z_full −0.1 to +1.0; strict radial statistic still z +4.4 | ΛCDM's own timing mass misses the UNGC flow identically (CFG548: shared tension) | CONDITIONAL / DATA-ISSUE, fragile | CFG515, CFG522, CFG548 |

### 2b. Failures, exclusions and tensions

| # | test | data | framework result | competing expectation on record | verdict as frozen | lane |
|---|---|---|---|---|---|---|
| F1 | Cosmic shear, candidate B / Theory v1 settling (all-baryon source, census supply), canonical | RAW (KiDS-1000, DES Y3 ξ±), COND-IC | own 1024³ L100 gravitating P(k,z): KiDS Δχ² +68.7 (every robustness variant ≥ +43.9; T-OWN passes; NZ1 bites); DES +22.4, tooth fails; own boost 1.19 / 1.25 / 1.21 at k 0.3 / 0.5 / 1 | same-pipeline S0 fits | **EXCLUDED** on KiDS; DES NOT DIAGNOSTIC; alt footing not completed | CFG596 (41efda383); scope 5c31fcad4 |
| F2 | Cosmic shear, census-capped condensed source (step toward Theory v2) | RAW (KiDS-1000, DES Y3), COND-IC | KiDS +13.97 (robust min +9.19, T-OWN passes); DES +7.01; own boost 1.058 / 1.056 / 1.056 | same-pipeline S0 | **EXCLUDED, narrowly**; DES NOT DIAGNOSTIC. It is a census cap, not a phase law: the PM cannot tell hot from condensed baryons (astra bd8981d3d), so a pass would not have established A5 either | CFG636 (54c6a393f); scopes bd8981d3d, 5c31fcad4 |
| F3 | KiDS isolated (f30) lenses, inner bins | RAW lensing; environment term ΛCDM-built (validated on isolated samples) | census edge χ² 45.6 / 35.8 (sharp), 54.1 / 42.4 (smooth) of 15 | — | FAIL both footings (CFG678 C3 FAIL; hot-gas and cool-gas escapes closed, CFG580–582) | CFG529, CFG580–582 |
| F4 | KiDS early-type excess at matched baryonic mass (law predicts early/late ratio 1) | RAW lensing, no ΛCDM ingredient | near-IR Ks masses: +0.280 ± 0.083 (Z 3.4); LePhare +0.249 (Z 2.4); Taylor +0.181 (Z 1.7). Caveat: constant M/L_K may inflate it by ~0.05–0.15 | — | EXCESS PERSISTS (robust on near-IR; Taylor is the outlier) | CFG668 (1be76f204), CFG669 (600c41c1e) |
| F5 | SLUGGS central ellipticals | RAW (measured GC profiles and anisotropy) | joint best case +0.07 / +0.06 dex mean (3.5σ / 2.8σ, statistical only); M87, NGC 4365, NGC 5846 +0.09–0.14 dex | — | GENUINE TENSION | CFG466, CFG492, CFG528/528b |
| F6 | MW outer slope, 15–27.5 kpc | RAW (Gaia DR3 red-giant + inversion curves) | decline steeper than the law's; combined Z −3.6 / −3.9 (RM-v can / alt) | a fitted NFW fails the same statistic (Z −3.4, post hoc) | SHAPE EXCLUDED as frozen; depends on the distance scale; DR4 decides | CFG532, CFG532b |
| F7 | X-COP at R200, condensed source | RAW | cluster mass 33–40% short (η 1.49 / 1.66) | — | FAIL (depends on CFG634's supply convention and on the settled phantom extending past R200) | CFG637 |
| F8 | Bullet sub-cluster | RAW (lensing PROVISIONAL) | all baryons plus the full cold supply = 0.71 of the measured M(<250 kpc) | — | TENSION (input-mass-limited) | CFG629, CFG637 |
| F9 | Early-type age signal vs Theory v2's A5 (post-hoc mechanism test) | RAW lensing | A5 predicts A_pred −0.061 / −0.061 vs raw A +0.166 ± 0.071; D_pred −0.145 vs +0.94 / +0.86 | — | **FAILS, WRONG SIGN**, both footings | CFG651 (97f815fd4) |
| F10 | Ultra-faint dwarfs, the law | RAW (binary-cleaned) | +0.325 dex (3.8σ) | ΛCDM's pass window spans 3.5–5 decades of halo mass | FAIL, NON-DISCRIMINATING | CFG42, CFG51, CFG73, CFG74 (`STANDING_2026-09-29.md` §3) |
| F11 | Settling rate: mergers vs galaxies | RAW Bullet/Harvey offsets in the framework's merger pipeline | mergers allow only α = 0; α = 0.1, 0.3 and ∞ EXCLUDED (Z_B +5.9 to +8.1); galaxies prefer α ≳ 0.5 (unscorable on mergers); deficit-gated mobility: VG-1 UNDETERMINED | — | TENSION in limited form; **PROVISIONAL**: progenitors carry only 16–36% of the measured core mass (CFG625) | CFG621–623, CFG625, CFG639 Part B (860d46186) |
| F12 | Variant: no cold energy (baryons + the law only) | RAW | galaxies identical (SPARC 0.100 / 0.101); X-COP gets 55–60% of the measured mass (13–15σ); Bullet lensing stays on the gas (Z_B +7.9); LG timing −208 / −225 vs −109 km/s | — | variant EXCLUDED: cold energy's mass is required | CFG624 (criteria 803cef306) |
| F13 | Variant: the law as a force on stars | RAW (Gaia DR3 wide binaries; cluster-satellite lensing) | no-EFE force: estimator pinned ≥ 1.50 vs 1.075 ± 0.055 (7.7σ / 8.3σ); force with EFE: boosts 1.4–2.9× vs the 10–20× needed (χ² 61–107/5) | — | both force readings EXCLUDED; the material-phantom (cold energy) reading survives | CFG447 (07b922691), CFG478 |
| F14 | Variant: a response sector that does not lens | RAW (KiDS-1000 + SPARC overlap, 324 points) | over-predicts SPARC by +0.155 / +0.158 dex rms | — | H-NL EXCLUDED: the extra pull must lens like mass | CFG663 (f5a9d1fe5); CFG670 (Lean) |
| F15 | Variant: isotropic cold-energy pressure | RAW SPARC | rms 0.177 / 0.187 vs 0.100 / 0.101 | — | EXCLUDED; anisotropic form is ill-posed (CFG660, CFG661) | CFG660 |
| F16 | Variant: dark-energy clock a₀_eff = f² c H_Λ | RAW SPARC | shape disfavoured (bias −0.063 alt / −0.042 can) | — | clock family closed | CFG666 |
| F17 | KiDS early/late split (candidate B, 09-29 machinery) | RAW lensing vs a ΛCDM comparator in the same pipeline | law χ² 28.1/7 (= zero-model); 4.4σ with the jackknife; 2.8σ on B's own M* calibration | colour-split ΛCDM 6.5/7; colour-blind Moster 6.9/7 | B-SPECIFIC relative to the ΛCDM comparator, for the difference only; shared by any model with negligible predicted difference at fixed g_bar | CFG88, CFG96 (`STANDING_2026-09-29.md` §3, §5 qualifiers) |
| F18 | Structure growth on the gravitating field | BENCHMARK vs S0, not data | passes at 256³ (0.063–0.082), fails at 512³ (0.150–0.193; σ8 +3–5%) | — | FAIL as a benchmark only; earlier growth "passes" were on the particle field; never cite growth as fixed | CFG555; PAPER45 v2.2 (DOI 10.5281/zenodo.23240863); 5c31fcad4 |

### 2c. Not diagnostic, conditional, or context only

| # | test | data | result | label | lane |
|---|---|---|---|---|---|
| N1 | Native shear at 512³ | RAW KiDS / DES, COND-IC | Δχ² +24 / +4 (can), +30 / +6 (alt); KiDS p 0.008 / 0.001 | NOT DIAGNOSTIC under frozen rules; leans against | CFG592 |
| N2 | Shear with HMcode × BAHAMAS × halo-model R(k) | CONTEXT ONLY | A_mod_eff 1.03–1.46 vs 0.82–0.86 | downgraded to context (owner rule 10-10) | CFG590, CFG591 |
| N3 | Halo-model sizes, required profile, H-CB halo-model deficit | CONTEXT ONLY | — | context | CFG556, CFG557, CFG559, CFG593, CFG634 |
| N4 | FRB DM scatter (Sharma+26, 114 FRBs) | CONTEXT ONLY (Tinker/Duffy/Moster) | A = 0.944 / 0.877; f_ret = 1 at Z −7 to −9 | neither CONSISTENT nor the f_ret = 1 exclusion counts as native | CFG632; astra a9bba9f84 |
| N5 | CMB lensing, candidate B canonical | partial box | ΔA = +1.3% (range +0.9% to +7.9%); particle field +0.17% | CONDITIONAL (Theory v2 expected lower, untested); ACT-range context reads UNSAFE | CFG649 |
| N6 | Lensing beyond cluster baryons (8–40′) | RAW (Quaia + DR16Q, DESI DR2 geometry) | K = +0.0008 ± 0.0021; κ(8–40′) < 0.0026 (2σ) | NOT DECIDED: the law's amplitude was not frozen (rough deep-MOND halo scale ~1.5σ above, not frozen) | CFG680 (a5b5c1f87); CFG678 C4 |
| N7 | Background counts behind clusters | RAW (KiDS DR5, DES Y6, quasars) | lensing NOT DETECTED as frozen | NOT DIAGNOSTIC | CFG680 A1/A2 |
| N8 | a₀ over redshift, existing discs | RAW + native inputs | RC100 is gas-route-limited and "not to be quoted as a ~5σ result" (CFG217); native inputs make CFG216 W-mixed, MUSE-DARK shows no rise on any native route, nothing separates the laws (shifts 0.05–0.10 dex inside the calibration wall, CFG303); CRISTAL NOT DISCRIMINATING (CFG308) | NOT DIAGNOSTIC | CFG216, CFG217, CFG303, CFG308, CFG535, CFG547 |
| N9 | a₀(z) vs DESI | DESI DR2 | a₀(z)/a₀(0) pinned to about ±0.04 dex | constraint, not a test | CFG512 (Theory v1 A3) |
| N10 | Early-type age signal itself | RAW lensing | raw ESD ×1.46 (Z +2.33, CFG700); at fixed Taylor mass +0.032 ± 0.080 (Z 0.4, CFG667); on Ks masses +0.082 ± 0.089 (Z 0.9, CFG669) | NOT ROBUST (stellar-mass artefact likely) | CFG585, CFG586, CFG631, CFG700, CFG667, CFG669 |
| N11 | MW HI flaring; outer HI dispersion | RAW | all models consistent with σ free; no qualifying σ measurement | NOT DIAGNOSTIC; never a phantom-disc win | CFG574, CFG575 |
| N12 | DiskMass σ_z | RAW | every model over-predicts (RM 1.39–1.43, PD 1.64–1.69, Newton 1.60 on S4G h_z) | NOT DIAGNOSTIC; front closed without a pass | CFG576–578 |
| N13 | Strong-lens perturbers (J0946, B1938) | RAW | J0946 dark solution EXCLUDED (×13 its light limit); luminous solution CONSISTENT; B1938 A and V not diagnostic | NOT DIAGNOSTIC (model-selection-limited) | CFG671 |
| N14 | B1938+666 A photometry vs sealed CFG673 | RAW (JWST GO 8281) | all injection teeth fail | NOT DIAGNOSTIC; never cite the 29.7 AB point estimate | CFG674 |
| N15 | FLIMFLAM FRB halo gas | RAW | σ(f_halo) 0.264 > 0.25 gate; MUTATE not detected | NON-DIAGNOSTIC | CFG628 |
| N16 | Ω_c/Ω_b = 5.364 from dimensionless monomials | theory | chance-level; nothing derives 5.364 | — | CFG642 |

**Counts** (rows above, by frozen label): **14 pass or consistent** (P1–P14; P11–P14 are only consistent or conditional, and P9 is partly superseded). **18 fail, are excluded, or are in tension** (F1–F18). Of these, 11 are fails or tensions of the theory as built (F1–F11), 5 are excluded variants (F12–F16) that constrain its form, F17 is a model comparison and F18 is a benchmark. **16 not diagnostic, conditional or context only** (N1–N16).

---

## 3. Sealed predictions (frozen before the data exist)

Each was committed, with a SHA-256 of its results file where one exists, before the release. Sealed files are never edited; changes go in new dated files.

| prediction | commit / hash | data release | framework predicts | rivals predict | kill condition |
|---|---|---|---|---|---|
| **Gaia DR4 wide binaries** (Arm C = candidate B; settling model registered by Amendment 21) | prereg frozen 2026-07-16; Amendment 21 commit 347f35887 (2026-10-06), sha256 after 4a005c03…bfb5 (`prep_2026/gaia_dr4_prep/AMENDMENT21_HASH.txt`) | **2026-12-02** | γ_v = 1.000 (exactly Newtonian), both footings; structural, no parameter moves it | Arm A (the bare law with EFE): floors 1.1614 canonical / 1.1917 alt (band to 1.23); Newton, ΛCDM, Arm B: 1.000 | γ̂ in 1.084–1.23 with the frozen stability requirements passing (ladder within 1σ_fit, κ ∈ [0.95, 1.05], NSS-off probe) falsifies Arm C and the settling model. A Newtonian result is survival only, never confirmation |
| **Milky Way vertical force and rotation, Gaia DR4** | CFG553, commit 8fb1f2c62 (2026-10-10), criteria 43fb64612, sha256 f8bea44f44c8117ddd395c08e476315a774aabce7289a36c4e506c6f11ccf4b9 | **2026-12-02** | K_z(R0, 1.1 kpc)/2πG: RM-v 74.07 (68.25–79.87) can / 75.55 (69.66–81.41) alt M☉ pc⁻²; Oort limit ρ_tot,mid RM-v 0.1156 / 0.1166 M☉ pc⁻³; σ_z(R0) RM-v 16.83 / 16.93 km/s; dlnV/dlnR (15–27.5 kpc) RM-v −0.1478 / −0.1364; V(60 kpc) RM-v 178.1 / 186.0 km/s | QUMOND phantom disc: K_z 90.05 / 94.78, ρ_tot,mid 0.1601 / 0.1688, σ_z 19.26 / 19.76; NFW fitted to Ou+24: K_z 76.25, slope −0.1739, V(60) 166.5. RM-v vs NFW in the disc NOT SEPARABLE | per prediction × footing × form: FRAMEWORK-EXCLUDED if d(m,F) ≥ 3 and d(m,R) ≤ 2; BOTH EXCLUDED (d ≥ 3 for both) also counts as a framework fail. DR3's ~−0.3 slope would make P2 BOTH EXCLUDED |
| **ALMA GS4_24110** (z 1.997, [CI] + dust, 0.09″) | CFG571, commit 259f7825c (2026-10-09), criteria 5f68a68c3, sha256 be27457db6bad870a734c52d2bad92c6669cde53ca7a81553e79154dbedc3714 | **2026-11-28** | gas inside R_e of log M_gas 9.1–10.7 (F-DESI, branch-dependent; stellar-mass branch moves it 0.6 dex) | a₀ ∝ H(z) and the ΛCDM-feedback RAR-equivalent scale: FLOOR in every branch (stars alone exceed what they allow) | negligible gas puts F-DESI "in trouble"; ~10¹⁰ M☉ or more puts both rivals below their own stars. One disc = demonstration; the criteria exclude nothing on it |
| **ALMA U4_27928** (z 1.419, CO 0.07″) | CFG571 (as above) | **2026-11-06** | conditional on V_c at 2R_e = 8.3 kpc: at 225 km/s, log M_gas ≈ 9.2–9.8 | at 225 km/s both rivals FLOOR; at 250–300 the framework needs 0.2–0.9 dex more gas than R-H | below V_c ≈ 200 km/s no model is tested |
| **KURVS CO survey** (2026.1.00363.S) | CFG571 (as above) | not yet observed | 7 discs; F-DESI vs R-H separation 0.19–0.21 dex (pressure branch) / 0.30–0.31 dex (no-pressure) | a₀ ∝ H(z) | forecast only 1.0–1.6σ; leans, cannot decide |
| **a₀–siren consistency** | CFG676, commit 634f276da (2026-10-12), criteria 692981e55, sha256 9defe3223431fbde08882dd7d50d7010bc870135625a493c322b747d302f1599 | future GW standard sirens | with DESI DR2 w0wa, Δlog a₀ = +0.014 to +0.037 at z 0.5, node near z 1, −0.059 to −0.068 at z 2, −0.111 to −0.151 at z 3 | a₀ ∝ H(z): +0.47 to +0.49 at z 2, +0.65 to +0.66 at z 3 | sirens and galaxy dynamics must agree; no numerical kill line frozen. CFG677: 3,000 bright sirens do not reach the required precision |
| **No cold-energy spike around black holes** | CFG675, commit e12d4881d (2026-10-12), sha256 d153665c…ac37ac; v2 correction 5e0b67a13, sha256 4c2cc32e…89f1 | LISA, 2030s | vacuum-GR IMRI waveforms; framework ceiling dephasing 1.6e-4 / 1.9e-4 cycles (v2) | particle-DM static spike: 1.5e6 cycles | required environmental density ≥ 10× the ceiling at r ≤ 1e-3 pc with baryons bounded. CFG677: an IMRI probes ~1e-9–1e-8 pc and cannot test shallow profiles at the ceiling |
| **J0946+1006 perturber** (JWST GO 12088) | CFG672 (dir CFG667_j0946_jwst_prereg), commit 52f4363bf (2026-10-12), criteria 44bf95584, sha256 7c3029fa5dc3d7f9302b3e464679e780bb7488089611a7a95e1060529fc769fd | unobserved on 2026-10-12; no date on record | baryonic dwarf: Q = M_lens/M_b ≤ Q_max = 1.08 / 1.09 inside 0.3 kpc, 1.17 / 1.21 inside 0.6 kpc, 1.80 / 1.98 inside 1 kpc | ΛCDM allows both outcomes | SURVIVES Q_obs ≤ 1.25 Q_max; EXCLUDED Q_obs > 3 Q_max |

**Sealed before viewing, data already public:** CFG673 (dir CFG668_b1938_jwst_prereg), commit 90c0618be (2026-10-12), sha256 9162427fb4a10de1ea938f398316a81b908998d1d2da2775f4d8ae46e198c04e. B1938+666 perturber A must show stars at F277W 26.4–29.6 (can) / 29.8 (alt) AB (F115W 26.9–30.9 / 31.0). It is EXCLUDED if the 2σ limit is fainter than 30.8 / 31.0 (F115W 32.1 / 32.2). Status: own modelling NOT DIAGNOSTIC (CFG674). This dataset can confirm but never exclude it. The production PyAutoLens fit was frozen at c29c55493 and has not been run.

**Pre-declared tests on existing data (frozen before any run, not before the data):**
- **CFG650 T1 / T12.** Theory v2's own raw-KiDS / DES test at 1024³: criteria 3087298c7, addendum c1c03ad5b, due 2026-10-13/14 (Theory v2 §6). Classes: EXCLUDED if Δχ² ≥ 9 and the robustness minimum ≥ 9; CONSISTENT if Δχ² < 4 and the robustness maximum < 9. T12 (M1 + M2) is a POST-PREVIEW owner selection and is labelled so in every report. T1 (M1–M4) stays primary. Verdicts are conditional on the inherited inputs.
- **CFG652.** eFEDS hot-gas groups (11c7906ef). Its own forecast says NOT DIAGNOSTIC is likely.
- **CFG681.** BAO from raw distances (fe91fd3bc).
- **CFG549** (firewalled, sha256 f110566e…820c, 0dfb051c9). From its own ingredients the framework predicts Λ plus a settling trickle of Δρ_DE/ρ_DE ≈ 2–8.5e-7, which is below any sensitivity.

---

## 4. What would kill it

Theory v2 §7, verbatim:

> - T12 and T1 both EXCLUDED on raw KiDS by the frozen rule.
> - a₀ rising with redshift (a robust rise ⇒ KILL of the flat law).
> - Gaia DR4 MW K_z or wide binaries outside the sealed predictions.
> - Any requirement for a new tuned constant to pass the gates above.

Sealed kill conditions (from §3):
- **Wide binaries:** γ̂ in 1.084–1.23 with the stability requirements passing (Amendment 21 / Arm C).
- **MW (CFG553):** any prediction labelled FRAMEWORK-EXCLUDED or BOTH EXCLUDED, per footing and form, robust to R0, distance scale and tracer.
- **ALMA (CFG571):** a sealed prediction failing on release (Theory v1 §7). For GS4_24110, negligible gas inside R_e counts against F-DESI. The criteria call one disc a demonstration.
- **J0946 (CFG672):** Q_obs > 3 Q_max.
- **B1938 A (CFG673):** a 2σ limit fainter than 30.8 / 31.0 AB (F277W) or 32.1 / 32.2 (F115W).
- **LISA (CFG675):** required density ≥ 10× the ceiling at r ≤ 1e-3 pc with baryons bounded.

---

## 5. Known weaknesses

- **κ = ½ is fitted.** Twelve derivation attempts failed (Theory v1 A2). Measured κ is 0.42 ± 0.10 / 0.35 ± 0.08 (CFG493), and κ is kernel-conditional at 0.46–0.60 (CFG468). The GF2 "κ derived" result is the SIS ratio, not the law's κ, and is not cited as a derivation.
- **Ω_c/Ω_b = 5.364 is an input.** No formula beats chance (CFG642). Its origin is not derived (CFG507). The supply postulate failed six derivation attacks (CFG461, 462, 488, 490, 494, 497).
- **The energy receiver's identity is open.** Passive vacuum is excluded (astra local_sink_reaction). The ghost-condensate receiver is a sketch for export only (CFG635). No single field does both dark jobs without tuned constants (CFG635). A canonical partner cannot follow DESI's w = −1 crossing (CFG542).
- **α is free** (CFG539, CFG542). Mergers allow only α ≈ 0 while galaxies want α ≳ 0.5 (CFG623, CFG598/620). The merger α verdicts are provisional because the progenitors carry 16–36% of the measured core mass (CFG625). The deficit gate narrows the tension but does not remove it (CFG639).
- **ICs and background are inherited from ΛCDM.** Every native PM verdict (CFG596, CFG636, CFG650) uses Planck-fit parameters, an EH transfer normalised to σ8 = 0.811, ΛCDM back-scaling and a ΛCDM-provenance Δ_ta (astra 5c31fcad4). Of the 59 halo ingredients, 17 are ΛCDM-inherited (CFG594).
- **No action exists.** No candidate passes the one-action contract (CFG678). Candidate B has no varied action, so A1–A6 are UNTESTED, and it has no legal bound-only switch (CFG48). The cold-energy sector as a field-stress medium is ill-posed (CFG660, CFG661).
- **The condensed/hot split is a census cap,** not a derived phase law (astra bd8981d3d). Deriving it is Theory v2 open problem 1.
- **Clusters at R200 and the Bullet sub** are short (CFG637, CFG629).
- **The age signal.** Theory v2's A5 predicts the wrong sign (CFG651). The signal itself is now not robust: it fades on Ks masses (Z 0.9, CFG669) and is likely a stellar-mass artefact (CFG667). The early-type mass excess at 50–100 kpc is separate and does persist (CFG669, Z 3.4).
- **Gaia DR4 cannot confirm candidate B.** It shares γ = 1.000 with Newton and ΛCDM (`STANDING_2026-09-29.md` §4–5).

Not cited, by the record's own rules: any "growth fixed" claim (CFG555 / PAPER45 v2.2), CFG372's withdrawn growth pass, the BH*/LRD coincidence, the Ω_Λ-from-a₀ rung (circular), a₀ ∝ H(z) as the distinctive prediction (the flat law is), CFG216 as a ~5σ result, CFG674's 29.7 AB point estimate, and CFG575 as a phantom-disc win.
