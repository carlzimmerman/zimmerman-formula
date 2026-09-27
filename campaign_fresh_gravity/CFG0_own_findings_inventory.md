# CFG0 — the framework's own findings: an inventory

This is the base every lane of the fresh campaign builds on (CHARTER rule 0). It lists the framework's own results, each
with its status and the file and commit that carry it. It was compiled from the repository at commit `3b22289d7`
(2026-09-27).

The companion script `CFG0_parameter_reduction.py` tests which of these results can fix, tie or remove the working
constructions' constants. `CFG0_README.md` gives the resulting constant count and says which findings each lane must use.

**Rules for citing from this list.**
- κ = ½ is **fitted**, never derived. Z = cH_Λ/a₀ = 2√(8π/3) = 5.7888 is κ restated; it is never ≈ 21.
- Both a₀ footings always: 9.3603 × 10⁻¹¹ m s⁻² (canonical, ρ_Λ) and 1.1312 × 10⁻¹⁰ m s⁻² (alt, ρ_total).
- A row marked WITHDRAWN or SUPERSEDED is listed so that nobody uses it. It is not a finding.
- A row marked NUMEROLOGY is a coincidence the record flagged. It is not a finding.
- A caveat attached to a row is part of the row. Quote it with the number.

**Status key.**

| status | meaning |
|---|---|
| VALIDATED | a committed runnable script reproduces it |
| PUBLISHED | deposited with a DOI (and, where noted, also validated) |
| RECORDED | prose or committed text only; no committed script or output reproduces it |
| WITHDRAWN / SUPERSEDED | the record retracted or replaced it; never cite it as a finding |
| NUMEROLOGY | a coincidence flagged by the record, or by CFG0; never a finding |

Commits are the latest commit touching the named file, abbreviated to nine characters. Paths are relative to the
repository root. Abbreviations: `chain/` = `real_research/derivation_chain_2026/`, `hub/` =
`real_research/cross_thread_review_2026_09_26/`, `papers/` = `qwen_claude_field_theory/papers_2026/`.

---

## 1. The core law and its coefficient

| # | Finding | Status | File(s) | Commit |
|---|---|---|---|---|
| F1 | a₀ = ξ c √(Gρ) is the only acceleration built from (G, c, ρ): the exponent matrix has \|det\| = 2, so (½, 1, ½) is unique. Admitting ħ destroys the uniqueness. κ and the choice of ρ are not fixed by it. | VALIDATED | `real_research/reviews/mi_third_category_search_2026.py`; `chain/FP0_core_postulates.py` (C1) | 7c4b3ef6b; 6123bd25b |
| F2 | a₀ = κ c √(Gρ_Λ) with κ = ½ FITTED: 9.3603e-11 (canonical) / 1.1312e-10 m s⁻² (alt). κZ = √(8π/3) identically. | VALIDATED (fitted input) | `chain/FP0_core_postulates.py` (C2, L0c) | 6123bd25b |
| F3 | κ measured: 0.465 ± 0.076 (BTFR intercept, estimator A) and 0.55 ± 0.17 (distance-free, estimator B, bulge M/L varied and bootstrapped). Both are consistent with ½. Always quote κ with its H₀. | VALIDATED | `real_research/reviews/mi_btfr_intercept_kappa_door_2026.py`; `papers/mnras_submission_2026_v2/paper_numbers.py` (S2e, S2f); `real_research/reviews/kappa_h0_convention_audit_2026.py` | 62f905dd9; a49751b6c; ed238836d |
| F4 | κ is not derivable in the present action class. The zero-mode theorem (k01); a sequestering-type global constraint misses by 10⁵ (k02); the one coefficient-shaped candidate not excluded, 0.461 (the horizon form), cannot be separated from ½ and is degenerate with the H₀ tension (k03). | VALIDATED; PUBLISHED (PAPER6, DOI 10.5281/zenodo.22559892) | `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py`, `k02_global_constraint_average.py`, `k03_half_vs_two_pi_precision.py` | d5cba7d34; 28c61fe68 |
| F5 | Further closed κ routes: the ε_tot slot is not live (KS01); the channel-count derivation of ½ is closed by a no-go (capstone); postquantum classical gravity gives κ = 1.30–1.45, ≥ 11σ off (L313–L314). | VALIDATED | `fable_independent_2026/kappa_slot_2026/KS01_slot_adjudication.py`; `opus_48_extended_research/kappa_audit_2026/CAPSTONE_kappa_nogo.md`; `real_research/cq_gravity_2026/L313_cq_rectification_lensing.py` | 75b678b6a; 96d7489a3; a4313508e |
| F6 | The four-form promotion (k04): a₀ and ρ_Λ come from one flux; κ = ½ ⟺ Z_q/β² = 7.96, a ratio nothing fixes; a₀ becomes environmental but stays invisible in galaxies. **Its "stable (F6)" verdict is withdrawn**: the construction is unstable for 2.39 < g_N/a₀ < 155 (XR31). | VALIDATED construction; health claim WITHDRAWN | `kappa_closure/k04_four_form_promotion_consistency.py`; `kappa_closure/k04_F6_CORRECTION_2026-09-27.md`; `hub/XR31_k04_f6_stability.py` | 2fb80ca12; c1932dcf8 |
| F7 | κ = ½ against Milgrom 2020's 1/(2π): a free SPARC fit gives κ ≈ 0.46 (canonical), so 1/(2π) is excluded in direction. The ½-over-1/(2π) preference (~2.2σ one-shape, 1.55σ shape-free) is conditional on the kernel. | VALIDATED (kernel-conditional) | `real_research/reviews/mi_a0_profile_likelihood_sparc_2026.py`; `mi_joint_overdetermination_2026.py` | 2b25fb72e; a0cc6d50a |
| F8 | a₀(z)/a₀(0) is exactly κ-blind (κ cancels), so the a₀(z) test probes the ρ_Λ tie, never κ. | VALIDATED | `real_research/reviews/mi_a0_sensitivity_survey_2026.py` | f8b149635 |
| F9 | The RAR at the fixed canonical a₀ with fitted Υ = 0.70: 0.108 dex over SPARC (FP1 C0: 0.1083). SPARC is convention-compatible and non-diagnostic of a₀'s value: anchoring is cheaper, not better. | VALIDATED | `real_research/rar_framework_a0_mlfit.py`; `chain/FP1_static_sector.py` | 0f63dacbe; 0592cd1e4 |

## 2. a₀(z)

| # | Finding | Status | File(s) | Commit |
|---|---|---|---|---|
| F10 | Flat a₀(z). The derived pressure law a₀² = κ²G(−p_Q), with the vacuum at w = −1, is flat (< 1% to z = 5). At z = 2.5 the framework's law gives 0.00 dex against ΛCDM's emergent +0.334 dex (2.5σ for one rotator at ±0.13 dex). Standing: untested (no clean z ≈ 2.5 rotator yet). | PUBLISHED (PAPER7 v3, DOI 10.5281/zenodo.22833314); VALIDATED | `fable_independent_2026/L273_desi_a0z_band.py`, `L274_a0z_theories_chart.py`; `nbody_2026/stage17_a0z_from_the_action_2026.py`; `papers/PAPER7_a0z_decisive_measurement_2026.tex` | 252f9e836; 46fcadae3; 8e6a39952 |
| F11 | a₀(z) ∝ √ρ_DE(z) for evolving dark energy (FP0 R3b). DESY5 gives a₀(2.5)/a₀(0) = 0.7956 (−0.099 dex), against the rival's +0.576. **Open conflict**: PAPER7 v3 and L273 Part 4 call this density mapping "rejected" by stage 17's pressure law, and XR20 finds that no local coupling realises it. CFG6 develops this branch. | VALIDATED at postulate level; contested | `chain/FP0_core_postulates.py` (R3b, added in 2f6aee236) | 6123bd25b |
| F12 | An action-level field tie reads √V, V = (ρ − p)/2 (XR20 T5): DESY5 gives +0.051 dex at z = 1 and −0.034 at z = 2.5. DESI's crossing of w = −1 needs a ghost. A healthy thawing field gives +0.07 to +0.16 dex at z = 2.5 and can erode the z ≈ 2.5 test. | VALIDATED | `hub/XR20_evolving_de_a0z.py` | a075ad7f7 |
| F13 | The a₀(z) exponent is undecided: η ∈ [0, 1.82] at 2σ; the a₀ ∝ H(z) rival (η = 1) survives. The registered deep-rotator test is data-gated (0 of the 2–4 clean rotators needed are on disk). | VALIDATED | `real_research/z2_eta_2026/Z2ETA_eta_bound_a0.py` | 9f7572c58 |
| F14 | The RC100 inversion, a₀ = (1 − f_DM) g_obs/[ln(1/f_DM)]², gives d log a₀/dz = −0.112 ± 0.063. It now **decides nothing**: 2.6–4.3σ across selection controls, calibration-conditional, not replicated on KMOS3D, a tie in level (L331). | SUPERSEDED as evidence | `papers/mnras_submission_2026_v2/paper_numbers.py` (S5); `real_research/rc100_audit_2026/L331_rc100_fairness_audit.py` | a49751b6c; 68c222f25 |
| F15 | MUSE-DARK III's apparent rise (+0.377 dex at z = 1) is non-diagnostic for the framework (constant-a₀ MOND shares it). A robust rise would kill the derived law. | RECORDED | `hub/XR20_README.md` (E5) | a075ad7f7 |

## 3. Action-level ties

| # | Finding | Status | File(s) | Commit |
|---|---|---|---|---|
| F16 | The Henneaux–Teitelboim unimodular tie. dΛ = 0 becomes a field equation, so a₀ = κc√(Gρ_Λ) holds on every solution. It adds no local mode and one global pair; FRW and PPN are untouched. It is a tie, not a derivation: κ is its coupling. Caveat: a matter vacuum energy moves the observed Λ but not a₀ (−0.023 dex at 0.1 ρ_Λ). The four-form tie (T2) fails health; the khronon's K (T3) gives the rival law. | VALIDATED; chain status TIED (FP0 L2b) | `hub/XR20_a0_lambda_tie.py`; `chain/FP0_core_postulates.py` | a075ad7f7; 6123bd25b |
| F17 | a₀ = (κ/√(24π)) c² K_∞ with K_∞ = √(3Λ). The khronon's CMC foliation and the unimodular clock are two structures that fit together, not one term; the local count is unchanged and the global count gains one pair. Overlap: unimodular shape dynamics (Gryb & Thébault 2012). | VALIDATED | `hub/XR30_one_clock.py` | 2a2d81f61 |
| F18 | P1's density is data-selected against the local density. The ρ_local fork (slope +0.5) is excluded on the public 175 SPARC at 13.0σ (internal SB), ~34σ (kNN) and ~7.5σ (UMa), with external nulls (2MRS 10.5σ, 2M++ 6.8σ, KT2017). A hybrid with \|slope\| ≲ 0.15 is not excluded; BIG-SPARC is not public. | VALIDATED | `real_research/predictions/a0_environmental_fork_test.py`; `real_research/reviews/sparc_environment_a0_REAL.py`; `real_research/reviews/project_sparc_a0_vs_cosmicweb.py`; `real_research/reviews/A0_COSMICWEB_ENVIRONMENT_2026-06.md` | 542c9f343; 3d8c0388f; d7afc1d41 |

## 4. Galaxy-scale laws and tests

| # | Finding | Status | File(s) | Commit |
|---|---|---|---|---|
| F19 | The galaxy law P2, g_obs = √(g_bar² + g_bar a₀). Its form is Milgrom 1999's Eq. 9 (credit); the coefficient is the framework's. Consequences: the deep limit; the BTFR v⁴ = GMa₀; the landmark slope s(y) = (2y+1)/(2(y+1)) with the sum rule s(y) + s(1/y) = 3/2 and even curvature, (3/4, 1/8) at y = 1. Its a₀/2 tail is 1278× the Earth ephemeris bound, so the action's kernel must reach Newton faster. | VALIDATED | `chain/FP0_core_postulates.py` (R1, R2); `prep_2026/equation_book/EQUATION_BOOK.md` (E1) | 6123bd25b; 5eb65de5e |
| F20 | The pair estimator (E4): a₀ = (g₁² − R₁₂g₂²)/(R₁₂g₂ − g₁), in which D and i cancel identically (and Υ too for gas). SPARC's 10,196 pairs give a median of 1.5e-10. It supports a ladder-free, frame-free H₀ route that is data-limited (band 58–240 km/s/Mpc). | VALIDATED | `prep_2026/equation_book/`; `prep_2026/ladder_free_h0/` | 5eb65de5e |
| F21 | The elliptic deflection (E15): α(b) = (4GM/c²b)√(1+u²) E(1/(1+u²)), u = b/r_M. | VALIDATED | `prep_2026/equation_book/` | 5eb65de5e |
| F22 | The a₀-line, g_obs² − g_bar² = a₀g_bar, and its Λ-inversion from dwarf rotation curves. **Retired as exact**: it is the α = 1 identity, whose a₀/2 tail is 1278× the ephemeris bound, and it carries a 26.3% shape systematic. | PUBLISHED (DOI 10.5281/zenodo.21419735); SUPERSEDED | `real_research/papers/A0LINE_LAMBDA_2026.md`; `real_research/reviews/mi_alpha1_solar_system_2026.py` | b79740d85; 32297a745 |
| F23 | The closure theorem. Every single-radius statistic whose extra inputs enter multiplicatively is the RAR reparametrised: 10 of 12 proposed regularities, the BTFR included, move by < 3.3e-16 dex under a derangement shuffle. Only multi-radius, redshift or environment tests can carry new information. | VALIDATED | `hunt_2026/k_unexplained-regularities_closure.py` | d4343a4b3 |
| F24 | Renzo's rule at second order: 0.944 ± 0.135 against a predicted 1.000 (0.4σ). | VALIDATED | `hunt_2026/h115_renzo_second_order.py` | 54b177f48 |
| F25 | Donato's constant: ρ₀r₀ = 176.8 M☉/pc² from 162 Burkert fits, against Σ_M = a₀/(2πG) = 106.9 (canonical, +0.22 dex) / 129.0 (alt, +0.14 dex). Prior art: Milgrom 2009. | VALIDATED | `hunt_2026/h5_h95_h58.py` | c887b1f02 |
| F26 | The vertical-force front. Full AQUAL on McMillan-2017 baryons matches Σ_dyn (−0.4/+0.1σ) and, at f_M = 1.30, f_R = 0.90, the Eilers slope (+1.2σ), but not v_c (−11.5σ). **Caveat**: the pattern holds only at that hand-picked cell and inverts at the χ² minimum; the α = 2 kernel it used was since replaced. | VALIDATED, with a record caveat | `real_research/reviews/mi_aqual_mcmillan2017_2026.py`; `mi_aqual_mond_refit_2026.py` | 6fb320dda; d7733f9f4 |
| F27 | The directional-EFE test. The first firing (n = 16) gave Â = +2.95 (p = 0.029 one-sided); WALLABY (n = 25) gave Â = −1.70 ± 2.12. A 3σ test needs N ~ 1,157 (~6,000 after the l = 1 solve). Exploratory: never cite +2.95 without −1.70. | VALIDATED (exploratory) | `real_research/reviews/directional_efe_2026/confrontation.py`; `prep_2026/wallaby_firing/fire_wallaby.py` | 28e3abe15; f617640ae |
| F28 | The external-field effect is measured **against** the framework: the cluster-infall BTFR slope is +0.0033 ± 0.0304 against a predicted −0.1348 (4.5σ); Local Volume dwarfs 3.9σ. Re-run under L361 (XR4): 2.4–4.2σ and 3.87–4.48σ, combined ~4.5–6σ. A liability. | VALIDATED | `hunt_2026/k_contrarian_clusterbtfr.py`, `k_contrarian_dwarfefe.py`; `hub/XR4_data_gates.md` | d4343a4b3; 05627f376 |
| F29 | The SN-Ia host-mass step. The Pantheon+ step, −0.050 ± 0.007 mag (6.9σ), is reproduced, and its location coincides with Σ_a₀ = a₀/(2πG) = 107 M☉/pc² (log M* 9.6–10.2). But acceleration adds nothing beyond mass (partial ≈ −0.04 against ≈ −0.20), so the location is a coincidence. The null itself is underpowered (~18%): disfavoured, not excluded. | VALIDATED scripts (no committed output) | `real_research/snia_massstep_acceleration_test.py`, `snia_hoststep_sizextmatch.py`, `snia_hoststep_localSB.py`; `real_research/reviews/mi_snia_power_curve_2026.py` | d266228be; 9618b81d1; 405b304f1; 87812ee4e |
| F30 | Bulk flows. The framework's linear regime is Newtonian: β = 0.447 against ΛCDM's 0.440, where an unprotected MOND kernel needs 0.043–0.047. This separates the framework from MOND cosmology. | VALIDATED | `hunt_2026/h85_bulk_flow_null.py` | f33d4e86a |
| F31 | KiDS isolated lenses. The √(GM_b a₀) boost does not end inside KiDS: 3σ lower bounds on where it ends are > 1.67 / 2.07 / 3.44 / 2.77 Mpc in the four Brouwer+2021 bins (M_b = 1.50 / 3.66 / 6.01 / 9.13e10 M☉), on both footings. | VALIDATED | `hunt_2026/h72_where_the_boost_ends.py` | 61fa039ac |
| F32 | The self-acceleration medium (L247): p = P(a) with a matched law reproduces any kernel's phantom, derives the isothermal identification σ² = C/2, and is CMB-cold by construction. **L248: the medium lost the lensing-truncation test** (measured slope 0.537 ± 0.026, 17.6σ from truncation), so no bounded "halo is the phantom" reading can source weak lensing. | VALIDATED; its lensing role WITHDRAWN (L248) | `fable_independent_2026/L247_self_acceleration_medium.py`; `L248_lensing_mass_budget.py` | 84a31f3a6; 52b26a409 |
| F33 | The bounded-boost theorem: a parameter-free ceiling on the acceleration excess that a dark-matter halo cannot impose. It holds for 99.23% of SPARC beyond 2 kpc and fails 9.1-fold in X-COP cluster cores. | PUBLISHED (PAPER5 v4, DOI 10.5281/zenodo.22548669) | `papers/PAPER5_bounded_boost_2026.tex` | 7744a96c5 |

## 5. The Solar System, wide binaries and ξ

| # | Finding | Status | File(s) | Commit |
|---|---|---|---|---|
| F34 | The coherence-length law (f29): QUMOND on a smoothed Newtonian potential with one new length ξ passes the Solar System and keeps the wide-binary boost, with the knee moved to 15–20 kAU; globulars want ξ ~ 50–140 pc (Pal 3 discordant). **Its floors (0.03–0.045 pc) are superseded**: 0.07/0.10 pc (exponential carrier) and 0.10/0.15 pc (ν_RAR) for the carried kernel (g03x); 0.0243/0.0268 pc for the chain's AQUAL double filter (F37). "Helmholtz behaves the same" was false (f30). | VALIDATED; floors SUPERSEDED | `hunt_2026/f29_coherence_length_law.py`, `f30_ppn_screening_door.py`; `qwen_claude_field_theory/closure_2026/g03x_nurar_carrier_and_cassini.py` | 47c46ff7c; 073805d4b |
| F35 | ξ as a healing length: the operator ξ²\|∇⊥V\|² inside J gives the Bogoliubov dispersion ω² = c_s²k²(1 + ξ²k²) and reproduces the coherent stiffening's α₁ exactly (f32). The mass ħ/(ξc) = 2e-22 eV at 0.03 pc is recorded as a coincidence (N1). | VALIDATED (f32); the mass is NUMEROLOGY | `qwen_claude_field_theory/closure_2026/ONE_NEW_THING_2026-09-04.md`; `hunt_2026/f32_ppn_k4_spatial_gradient_operator.py` | aaa63289d |
| F36 | Every Solar-System screening is a threshold mass. At fixed y a local key sees only C ~ M^½; ξ's window reads a₀ξ²/G ∈ [0.4, 7e6] M☉. No constant-free route exists (cubic Galileons screen galaxies; BDEF's Galileon replaces ξ with another fitted length). ξ is the gravity core's one knob. | VALIDATED | `chain/FP17_screening_without_xi.py` | a60b18e02 |
| F37 | The chain's Solar-System floors: the AQUAL double filter needs ξ ≥ 0.0243 / 0.0268 pc (the Saturn monopole binds). The strict law (ξ → 0) fails Cassini 4–7.6× and its a₀/2 tail fails the ephemerides 1279× / 1545×. | VALIDATED | `chain/FP1_static_sector.py`; `chain/FP7_aqual_type_repair.py` (A4) | 0592cd1e4; 17a90e572 |
| F38 | Gaia DR4. At ξ's floor the chain predicts γ̂ = 1.0725 (canonical) / 1.0900 (alt). DR4 can kill the chain only from above. A separation-resolved statistic would measure ξ to σ(ln ξ) ~ 0.2. | VALIDATED (hub re-run pending) | `hub/XR22_prereg_statistic.py`, `XR22_force_law.py` | 661ea3cff |
| F39 | The Gaia DR4 pre-registration: frozen. Never edit its past content; amendments are append-only and are the author's call. | PUBLISHED (DOI 10.5281/zenodo.21702746, v4) | `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md` | 779e76934 |
| F40 | The Oort-cloud / comet-anisotropy side-front. The solar Oort spike is EFE-dominated; the surviving signal is directional (~7% in spike position, ~17% in injection rate), and the ν₀-correlated pair with DR4 is the framework-specific object. **Flag, not ruled on**: stage 76's ν₀ pin collapses the pair toward 16.7%, indistinguishable from constant-a₀ MOND's 17%. | PUBLISHED (DOI 10.5281/zenodo.21966646); VALIDATED | `real_research/tabby_exo_oort_a0_2026.py`; `opus_48_extended_research/papers/OORT_CLOUD_EFE_INSTRUMENT.md`; `nbody_2026/stage76_nu0_recombination_pin_2026.py` | cd0a3394a; e32db65d1; 9be932ff7 |
| F41 | The SME / Lorentz bridge: a₀ induces (does not derive) s^μν = A(u^μu^ν + η^μν/4), which passes all 27 gravity-sector bound rows by ≥ 5 orders (α = 2 re-derivation), unobservably. **The DOIs' live-test margins, computed on the retired α = 1 tail, are superseded**: s^TX is not live. | VALIDATED; PUBLISHED (DOIs 10.5281/zenodo.20978308, 21137568; live-test claim SUPERSEDED) | `real_research/reviews/mi_sme_bridge_alpha2_2026.py`; `real_research/reviews/stx_target.py` | 94b1c6609; 09ba0c4eb |

## 6. Clusters and lensing

| # | Finding | Status | File(s) | Commit |
|---|---|---|---|---|
| F42 | Cluster standing. On X-COP the kernel accounts for **48%** of the dynamical mass at R500 and leaves 52%; η = 1.72–2.08 depending on the kernel (2.084/1.917 for the a₀-line kernel, 1.865/1.722 for MS08's). Clusters need cold collisionless mass of ~6.8× the baryons inside 400 kpc, with ρ ∝ r^−1.53 over 40–750 kpc. "74–89% removed" and "~32% removed" are withdrawn (W1, W2); η = 2.334 is specific to eRASS1. | VALIDATED | `nbody_2026/stage44_cluster_caveats_verified_2026.py`; `real_research/reviews/clusters_eta_audit.py`; `nbody_2026/stage33_potential_depth_solve_2026.py`; `qwen_claude_field_theory/closure_2026/g04a_cluster_source_phase_space.py`; `real_research/cluster_outer_slope_2026/COS1_cluster_outer_slope.py` | cd63d3fa9; f2b07589c; 43836b2a4; 2c937dcf6; e9e792d03 |
| F43 | The merger lanes (L370–L372): El Gordo is slightly easier with the phantom; Harvey kills hollow-core carriers; a two-channel carrier passes the alt set. | VALIDATED | `real_research/merger_infall_2026/L370_boosted_infall_mergers.py`, `L371_harvey_slow_kick_carrier.py`, `L372_gated_slow_kick_carrier.py` | 77f79072c; fe4fb762d; 8850550c4 |
| F44 | SLACS strong lensing from baryons plus the phantom needs a stellar IMF 0.118 ± 0.013 dex above the spectroscopic relation; the phantom supplies only 9.5–11% of the Einstein mass. | VALIDATED | `hub/XR33_lensing_imf.py` | 92fe59705 |
| F45 | The KiDS-vs-Hubble-flow pincer is in the data (FP18). At face value no static profile fits both KiDS's isolated lenses and the Local Volume flow (9.8σ, ΛCDM included); six comparability systematics bring it to 2.3σ: UNDECIDED. Model-independent bound: ΔΣ(R) ≤ M(<R)/(πR²). | VALIDATED | `chain/FP18_kids_vs_hubble_flow_data.py` | 09990b398 |
| F46 | Spectroscopically isolated late-type centrals lens at A = 2.19 ± 1.46 of the mixed-type level (S/N 1.5), so the pincer stays UNDECIDED; deciding it needs ~2,100 such centrals (FP21). | VALIDATED | `chain/FP21_isolated_spiral_lensing.py` | bb368ad2a |
| F47 | The Milky Way's outer curve (XR29): the Gaia DR3 decline needs M* = 7.3–8.2e10 M☉ (4–5σ above the censuses); ΛCDM needs a concentration 1.9–3.8σ high. | VALIDATED (hub re-run pending) | `hub/XR29_mw_outer_curve.py` | 633c161b5 |

## 7. The dark sector

| # | Finding | Status | File(s) | Commit |
|---|---|---|---|---|
| F48 | The GDM degeneracy theorem. Linear cosmology constrains the dark sector only through (w, c_s², c_vis²) plus an amount; at (0, 0, 0) it is CDM exactly. "0σ both ways": it removes an argument against a non-particle dark sector and supplies none for it. Liabilities: the w₀ squeeze (one-scalar constructions only; FL1 removes it in V0) and substructure, which leans particle. | VALIDATED | `real_research/reviews/mi_particle_vs_mode_2026.py` | 77b3b9884 |
| F49 | The dark sector as a ghost condensate. The amount I₀ ≈ Ω_dm is robustly free: it is a shift-charge mean, thermal physics sets only variances, and the thermal route falls ~72 orders short. Only sign(I₀) > 0 is forced. **"S8 neutral by theorem" is withdrawn as a theorem** (only the quasi-static reading is neutral). | PUBLISHED (within DOI 10.5281/zenodo.20773004); VALIDATED; the S8 theorem WITHDRAWN | `opus_48_extended_research/reviews/GHOST_CONDENSATE_2026-06-19.md`, `GHOST_CONDENSATE_CONSEQUENCES_2026-06-19.md`, `door_runs/door_E_amount_pin.py`; `real_research/reviews/mi_cosmo_perturbations_2026.py` | 7a71d1ead; ff4459e2d |
| F50 | Condensate dust breaks down at the first stream crossing; only a wave field passes (L374). The particle-mesh box cannot resolve it (L382). Even with clearing, the field needs m ≳ 2–5e-19 eV (L383). | VALIDATED | `real_research/condensate_dust_2026/L374_condensate_dust_shell_crossing.py`, `L382_fuzzy_field_in_the_box.py`, `L383_wave_field_zoom_in.py` | 4366a5625; 9b6e560f8; f091dc718 |
| F51 | FL1: the dark fluid is a superfluid order parameter, which is new field content (V0 has one propagating scalar). The condensate dust is its Thomas–Fermi limit. It is GDM (0, 0, 0) to 3e-16 for m ≥ 2e-19 eV, and a classical field (occupation ~1e77). The mass is still required. | VALIDATED | `real_research/dark_fluid_2026/FL1_order_parameter.py` | 40c6ae144 |
| F52 | FK1: the ~600 km/s kick as a phase change of the order parameter. ε Re Φ² splits its real parts, with ε/m² = v_k²/(2c² − v_k²) = 1.84–2.35e-6 for 575–650 km/s; φ_Hφ_H → φ_Lφ_L leaves at v_k; the quartic must be (Im Φ²)²; the coupling must be K-gated (q > 3/4). A construction: ε, λ₀, q and the misalignment are declared. | VALIDATED (construction) | `real_research/dark_fluid_kick_2026/FK1_kick_as_phase_change.py` | c2e1fa119 |
| F53 | FL2 and FL3: the kick potential fits V0's dark slot (kernel-invisible; the K-gate stiffens the khronon; the splitting can carry no gate). The fluid swirls in quantised vortices without disturbing the clock's slices. | VALIDATED | `real_research/dark_fluid_2026/FL2_dark_slot_with_the_kick.py`, `FL3_swirl_and_the_clock.py` | e96b71eb0; ba60f163f |
| F54 | Reciprocity (FP4, FP8): no kick can be powered by the MOND sector. Unbinding the flagship's dark mass costs 7.2–11.9× the host's whole MOND field energy, and every MOND-sector coupling clears clusters before z = 2.5 galaxies. The kick's energy must be the dark field's own. | VALIDATED | `chain/FP4_kick_from_action.py`; `chain/FP8_current_coupling_kick.py` | 702abada3; ba59740a6 |
| F55 | FP15, the dark sector's constants. ε is irreducible (the only Z₄-odd term) and fitted (the flagship sets the lower end, Harvey the upper). ζ, q and m are fitted by data: ζ's band is ×1.16 wide at the floor mass, and sharing q with the separator fails the web. The amount and the misalignment are initial data; the amount has ΛCDM's ω_c status. | VALIDATED | `chain/FP15_zero_knob_dark_sector.py`; `chain/FP20b_rescore_fp15_fp16_fp19.py` | 138f73b69; 3924bb8c2 |
| F56 | FP16: with re-accretion the dark-sector window is **empty** (0/8 cells). Clusters recapture the escaped daughters, so X-COP fails at every kick from 575 to 650 km/s (X-COP alone would need ~1,050 km/s). No verdict flips with the exact projector (FP20b). | VALIDATED | `chain/FP16_daughter_reaccretion.py`; `chain/FP20b_rescore_fp15_fp16_fp19.py` | b3f5759a4; 3924bb8c2 |
| F57 | XR16: the fluid's conversion surface clears the flagship radius by z = 2.5 on the record's grid (S at r_F ≤ 7e-5). | VALIDATED | `hub/XR16_fluid_conversion_surface.py` | b667f56bb |
| F58 | XR19: once seeded in halos, the conversion runs through the collapsed and turned-around web at z ≲ 1.5 and percolates (F_tot(0) = 0.74–0.91 across the band). It does not run through voids or at z ≳ 3. | VALIDATED | `hub/XR19_web_runaway.py`, `XR19_front_physics.py` | b55775ce0 |
| F59 | XR32: FK1's conversion alone lowers survey S8 to 0.752–0.766, but leaves cluster counts 5–9σ below eRASS1, DESI RSD −2.2σ and CMB lensing −1.6σ against ACT, with a +0.098 eV neutrino-mass-like suppression; there is a counts-vs-X-COP pincer on recapture. | VALIDATED | `hub/XR32_matter_power.py`, `XR32_survey_s8.py`, `XR32_README.md` | fa341733d |
| F60 | The Λ-triggered carrier (L319/L320) was the first carrier to pass the strict forest and S8 together. RC100 goes 3.0–3.4σ against it, it has no window (X-COP overshoots), and it is incompatible with C-H/K (L345). The author stopped the carrier chain as knob-fitting. | VALIDATED; chain STOPPED | `real_research/dark_sector_2026/L319_lambda_triggered_kicked_decay.py`, `L320_carrier_highz_price_rc100.py`, `README.md` | a4313508e; 6dc375e88 |
| F61 | The Lyman-α b-cutoff: the sign of the framework's predicted shift is robust across every fork; its size is a weak tension, 0.4–0.9σ on the calibration channel. The "6–8σ" exclusion is withdrawn (W5). | VALIDATED; the exclusion WITHDRAWN | `real_research/reviews/mi_forest_bcut_data_2026.py` and its `mi_forest_*` siblings | 20d8b52da |

## 8. The derivation chain's derived results

| # | Finding | Status | File(s) | Commit |
|---|---|---|---|---|
| F62 | FP1: the ungated C-H/K core's static law is QUMOND with a double heat filter; P2 embeds exactly (closed-form primitive) and is healthy with no repair. | VALIDATED | `chain/FP1_static_sector.py` | 0592cd1e4 |
| F63 | FP2 and FP5: c_T = 1; PPN γ = 1 and α₃ = 0; α_c ≤ 3.2e-9; the moving-source response is static MOND iff c₂ ≠ 0; the canonical count is 2 tensor modes + 1 khronon scalar, and the heat filter adds no mode. | VALIDATED | `chain/FP2_relativistic_consistency.py`; `chain/FP5_dof_and_a0_field.py` | 24aae971e; a26136bc4 |
| F64 | FP3: a local gate on the MOND energy has a non-negative second variation iff it is concave (with a chord bound); σ₈ within 2% caps the web's MOND on-fraction at ~2e-3; the ungated core fails σ₈ (18–27). | VALIDATED | `chain/FP3_cosmology_linear.py` | 9b265b331 |
| F65 | FP6: the band-pass as an action (C-H's heat branch read at two diffusion times); Gauss compensation (an isolated system weighs only its baryons beyond ~2L); the KiDS–Local Group pincer turned into a truncation scale. | VALIDATED | `chain/FP6_gate_survey.py` | 9d9e75369 |
| F66 | FP7: the AQUAL-type repair. The chassis is forced; the static law is two-field AQUAL (P2 exact in spherical symmetry); FRW is GR; the MOND term has zero tangent; c_T = 1; the AQUAL floors are 0.0243/0.0268 pc. Inertia alone cannot separate web and galaxies (σ₈ needs λ_eff ≥ 1e7, tracking allows ≤ 2.8e4). | VALIDATED | `chain/FP7_aqual_type_repair.py` | 17a90e572 |
| F67 | FP9: the yield floor J_Y = J_P2 + 2y_th√Y (unique statics, admissible on the AQUAL root); no host-independent Mpc length can be built from (a₀, Λ, G, c). | VALIDATED | `chain/FP9_web_galaxy_separator.py` | b510eebfe |
| F68 | FP10–FP12. FK1 in the chain: the flagship passes in the history reading; X-COP and shear fail in place. The MW–M31 timing with baryons only reaches −109.3 km/s on the first approach (no flyby needed; a past flyby excluded). Group zero-velocity radii overshoot by +0.20 dex (LG, M81, IC 342); Cen A is matched. | VALIDATED | `chain/FP10_internal_splitting_dark_sector.py`, `FP11_local_group_flyby.py`, `FP12_local_volume_groups_r0.py` | d9cb8b837; 4ad7b15bd; 59e537955 |
| F69 | FP13: the web's own running fixes n (n_eff = 2.06 on the actual field). **H_S as a separator is withdrawn**: it is linearly ill posed (XR18; FP13's A1 erratum). | VALIDATED; H_S WITHDRAWN | `chain/FP13_separator_from_state.py`; `hub/XR18_second_variation.py` | 27faacc84; 53854a459 |
| F70 | FP14, the zero-knob core: c₂ → ∞ is regular on Minkowski and FRW (a multiplier); α_c is a regulator; ξ is the one knob. **Errata**: its "σ₈ unchanged for λ = 0–100" was measured at the c₂ floor (XR25); c₂ = ∞ is singular at black-hole universal horizons at O(α_c) (OPEN). | VALIDATED, with errata | `chain/FP14_zero_knob_core.py` | 03db97f14 |
| F71 | FP19: H_K1, a well-posed separator with one declared constant (L_Λ = 2.9 Mpc; window 2.8–4.6 Mpc with the exact projector) plus three natural choices. It passes σ₈, the forest, the flagship, SPARC and KiDS at z = 0.25 and 0.4. Its prices: KiDS at z = 0.7 comes out at +500/+524 (a prediction), and the LG R0 fails. XR18b: linearly well posed and causal (criterion B); the nonlinear free-boundary problem is OPEN; λ must be declared ≤ 0.03. | VALIDATED | `chain/FP19_hs_repair.py`; `chain/FP20b_rescore_fp15_fp16_fp19.py`; `hub/XR18b_ramp_lambda.py` | 0c18c582f; 3924bb8c2; 3c0cf3c37 |
| F72 | FP20: the KiDS projection bug is fixed; none of the chain's deciding KiDS verdicts flips. | VALIDATED | `chain/FP20_esd_projection_fix.py` | 7a8c25321 |
| F73 | FP22, who feels MOND. The action as written implies that all matter does. The adopted reading puts FK1 on the root's Einstein-frame metric g̃ = g + (1 − e^−2χ) n n: baryons source and feel the phantom, with no new field or constant, at the price of dark–baryon free-fall universality where χ ≠ 0. CMB lensing is excluded in the all-matter reading; in the adopted reading it passes Planck and ACT linearly and fails ACT on halofit (≥ 3.8σ), so it is undecided until the nonlinear phantom is computed. | VALIDATED | `chain/FP22_who_feels_mond.py` | bfe9a2fe5 |

## 9. The review lanes' constructive results

(XR16, XR19, XR20 and XR30 appear above as F57, F58, F12/F16 and F17.)

| # | Finding | Status | File(s) | Commit |
|---|---|---|---|---|
| F74 | XR25: binary pulsars, preferred-frame PPN and GW170817 pass because α_c is tiny. λ is a regulator for strong fields but a knob in the MOND regime unless declared ≤ 0.03 (now declared: XR18b). | VALIDATED | `hub/XR25_lambda_regulator.py`, `XR25_ppn_preferred_frame.py`, `XR25_pulsar_radiation.py`, `XR25_cmc_compact_objects.py` | 43cfa1692 |
| F75 | XR26: at z ≳ 10 the chain's linear equations reduce to GR + CDM (TT/TE/EE equal ΛCDM's to 7.8e-8), and BBN is standard; the φ̇ = 0 initial condition is load-bearing. | VALIDATED (hub re-run pending) | `hub/XR26_cmb.py`, `XR26_bbn.py`, `XR26_linear_equations.py` | 68135cb7a |
| F76 | XR23: the abundance of massive halos at high z equals ΛCDM's, so the JWST baryon ceiling is unchanged; δ_c is not fixed by the theory. | VALIDATED | `hub/XR23_collapse_threshold.py`, `XR23_mass_function_ceiling.py` | 6b7ab8243 |
| F77 | XR27: none of M*'s three external-field failures flips at any band-pass L; the dwarf failures are inherited from MOND at Υ_V = 2. | VALIDATED | `hub/XR27_efe_favouring.py` and siblings | 3e55fdff2 |
| F78 | XR4: the "~30 Local Volume groups R0" follow-up is not runnable (only 6–8 of 161 UNGC disturbers give a stable R0); the EFE-against results survive L361. | VALIDATED | `hub/XR4_data_gates.md` and its scripts | 05627f376 |

## 10. Published consolidations (read with their notes)

| # | Record | Status | File | Commit |
|---|---|---|---|---|
| F79 | PAPER29 v3 (the equilibrium reading, DOI 10.5281/zenodo.22776494) and PAPER30 (what survives verification, DOI 10.5281/zenodo.22803511). **Never cite from them**: 5.09 keV, the 2.55-keV line, z* = 2.4, or "180 theorems closes the loop" (the WAVE-32 audit, L261). | PUBLISHED, with do-not-cite items | `papers/PAPER29_equilibrium_reading_2026.md`; `papers/PAPER30_swarm_verified_ledger_2026.md`; `fable_independent_2026/L261_wave32_audit.py` | 0916483a0; e6aeda53a; 2954698c4 |
| F80 | PAPER32 (the moving phantom, DOI 10.5281/zenodo.22967076); PAPER33 v2 (the khronon route, DOI 10.5281/zenodo.22967954; v1's cubic repair withdrawn); PAPER34 v2 (a dark sector the kernel cannot see, DOI 10.5281/zenodo.22984587; v3 not deposited). | PUBLISHED | `papers/PAPER32_moving_phantom_2026.pdf`; `papers/PAPER33_khronon_route_2026.pdf`; `papers/PAPER34_kernel_blind_dark_sector_2026.pdf` | d16d5650d; a7ca28475; 022c6dd5d |
| F81 | THE_COMPLETION v9 (DOI 10.5281/zenodo.21895046): the relativistic field theory that carried a₀ = κc√(Gρ_Λ). Its dark sector is excluded, and its AeST-embedding PPN route was killed. | PUBLISHED; dark sector SUPERSEDED | `opus_48_extended_research/papers/THE_COMPLETION.md` | 3bc062ecf |

---

## Numerology the record flags (never findings)

| # | Coincidence | Flagged by |
|---|---|---|
| N1 | ħ/(ξc) = 2e-22 eV at ξ = 0.03 pc (the "fuzzy mass"). It is 721× below the chain's dark-mass floor (CFG0 R2). | ONE_NEW_THING; CFG0 |
| N2 | ε/m² = κ¹⁹, i.e. v_k = κ⁹c = 585.5 km/s (chance 0.35). | FP10, FP15 E3 |
| N3 | ξ_q = ((ħ/m)²/a₀)^⅓ = 1.6–3.3 pc; (c²/a₀)(32π)⁻⁶ = 0.030 pc. | FP14, FP17 |
| N4 | (ħc/G)^{3/2}/m_p² = 1.85 M☉ inside ξ's mass window (the proton mass is not in the gravity core). | FP17 M3 |
| N5 | L_Λ = (a₀/H_Λ²) κ⁸ = 3.63 Mpc (chance 80%). | FP19 B1 |
| N6 | m_P^¼ (ħH₀)^¾ = 2.5e-18 eV and m_P^¼ (ħa₀/c)^¾ = 5.7e-19 eV in the mass window (chance 0.67). | FP15 M5 |
| N7 | "Z = 5.789 matches via Friedmann": a tautology (the H cancels for any ρ with H² = 8πGρ/3). | the coefficient-footing audit |
| N8 | Ω_c = κ⁴√(8π/3)/Ω_Λ = 0.2642, Planck's central value at h = 0.674. The grammar it comes from produces 1.9 such hits within 1σ by chance, and no mechanism exists. | CFG0 R9 (new) |
| N9 | h/(m v_k) = 0.036–0.110 pc, the kicked daughters' de Broglie wavelength, inside ξ's window (the reduced ħ/(m v_k) fails the floor). The family lands with chance 0.96. | CFG0 R2 (new) |
| N10 | L_Λ ≈ v_k/(3H₀) = 2.84 Mpc, or ½ × 0.555 v_k/H_Λ = 2.86 Mpc, inside the σ₈-tight window (chance 0.90–0.98 for the grammar). | CFG0 R8 (new) |
| N11 | q = n − ¼ = 7/4 (n_t ∝ L⁻², with H_K1's n = 2) reproduces the data-pinned q exactly, but post hoc (chance 0.5). | CFG0 R5 (new) |
| N12 | δ_t0 ≈ 1 + δ_ta(z = 0) = 11.76, ΛCDM's turnaround contrast today, sits 6.6% below FP15's floor-mass band: a one-epoch coincidence, since the turnaround contrast's own running is the wrong way. | CFG0 R4 (new) |

## Withdrawn or superseded (do not cite)

| # | Item | Replaced by / why | Where |
|---|---|---|---|
| W1 | "The kernel removes 74–89% of cluster dark matter" | At R500 it accounts for 48% and leaves 52% (too favourable) | `RETRACTIONS.md` (f3162921e); `nbody_2026/stage44_cluster_caveats_verified_2026.py` |
| W2 | "~32% removed / ~68% needed" | incoherent (additive combination); withdrawn the same day | `real_research/reviews/mi_third_category_search_2026.py` (7c4b3ef6b) |
| W3 | κ = 0.551 ± 0.043 as the clean distance-free determination | the error bar held Υ_bul fixed: 0.55 ± 0.17 | `papers/mnras_submission_2026_v2/SUBMISSION_CHECKLIST.md`; `RETRACTIONS.md` |
| W4 | "S8 neutral by theorem" | refuted as a theorem; neutral only in the quasi-static reading | `real_research/reviews/mi_cosmo_perturbations_2026.py` |
| W5 | Lyman-α "6–8σ" exclusion | the kernel was evaluated at y instead of x: 0.4–0.9σ | `RETRACTIONS.md`; `real_research/reviews/mi_forest_bcut_data_2026.py` |
| W6 | the a₀-line as an exact law | the α = 1 kernel is retired (ephemeris tail 1278×) | `real_research/reviews/mi_alpha1_solar_system_2026.py` |
| W7 | the s^TX margins (~9.6×, 1.50×, 1.24×) and s^TX as a live test | not live under α = 2 | `real_research/reviews/mi_sme_bridge_alpha2_2026.py` |
| W8 | the DESI-CPL a₀(z) bump "+6% at z ≈ 0.4"; PAPER7 v1's −0.09 dex as the prediction; PAPER7 v2 (stale PDF) | never self-consistent with w = −1; the pressure law is flat | `RETRACTIONS.md`; PAPER7 v3 |
| W9 | "RC100 shows a₀ is flat" | decides nothing | MNRAS v2 package (S5) |
| W10 | η = 2.334 as universal; "clusters at 21.6 a₀ at R500"; "2.084/1.917" without the kernel named | eRASS1-specific; 21.6 a₀ is the core (R500 is at 0.33–0.58 a₀); quote 1.72–2.08 with the kernel | `RETRACTIONS.md` |
| W11 | k04's "stable (F6)" | unstable for 2.39 < g_N/a₀ < 155 | `kappa_closure/k04_F6_CORRECTION_2026-09-27.md`; `hub/XR31_k04_f6_stability.py` |
| W12 | FP13's A1 (H_S well posed); FP14's "σ₈ unchanged for λ = 0–100"; FP19's "λ any value ≲ 100" and "the ⟨K⟩_h read acts at k = 0 only" | XR18; XR25; XR18b | chain README errata |
| W13 | FP6's `esd_of_M` projection; H_Y's KiDS pass at z = 0.4 | fixed by FP20; H_Y fails at z = 0.4 | `chain/FP20_esd_projection_fix.py` |
| W14 | L320's level claim; L368's "passes every gate"; L381's Harvey verdict; L342's KiDS lead; GP4's alt window; PAPER33 v1's repair | a tie (L323/L331); one-realisation artefact (L369); mixed switch cells; withdrawn; single realisation (P34d); wrong (PAPER33 v2) | the respective lanes |
| W15 | "Pure MI predicts zero directional asymmetry" | retracted | `STANDING.md` |
| W16 | item 71's "67% pair-midpoint deficit"; item 25's a₀ = 1.14e-10 from the deep tail | a saddle artefact (0–2%, opposite sign); biased +0.0985 dex (corrected 9.04e-11) | `hunt_2026/h71b_saddle_forecast.py`; `hunt_2026/h102_gas_dominated_a0.py` |
| W17 | "No dark matter in galaxies" as a result | the slogan is "no dark-matter particle" only | `RETRACTIONS.md` |
| W18 | γ_v = 1.2139/1.2592 as the settled target; γ_v = 1.032/1.040; f29's floors for the carried kernel | bracket 1.11–1.16/1.13–1.21 (Amendment 10); 1.0450/1.0300 (Amendment 11); g03x | `RETRACTIONS.md`; `prep_2026/gaia_dr4_prep/` |
| W19 | the Coma UDG kill at "19.4σ" | 4.9σ canonical / 4.7σ alt (the amplitude stands) | `fable_independent_2026/L23_udg_verify.py` |
| W20 | 5.09 keV; the 2.55-keV line; z* = 2.4; "180 theorems closes the loop"; the BH*/LRD coincidence as a framework result | the WAVE-32 audit; the BH* audit | `fable_independent_2026/L261_wave32_audit.py`; `real_research/bhstar_audit_2026/BHSTAR_AUDIT_AND_DOOR_SWING_2026-09-22.md` |
| W21 | the dS-Unruh reading of κ = ½; Z ≈ 21 | Milgrom 1999's 2cH_Λ is excluded; Z = 5.7888 | the equation book; the coefficient-footing audit |
| W22 | L247's medium as the source of weak lensing | L248 (17.6σ from truncation) | `fable_independent_2026/L248_lensing_mass_budget.py` |
| W23 | "~30 LV groups' R0: a 4.5σ decision this month" | not runnable (6–8 of 161) | `hub/XR4_data_gates.md` |
| W24 | THE_COMPLETION v9's dark sector; the v9 AeST-embedding PPN route | excluded; α₁ un-tunable | `STANDING.md`; `opus_48_extended_research/papers/THE_COMPLETION.md` |

## Counts

- **81 findings (F1–F81).**
  - 73 are validated by a committed script. Five of them are also published with a DOI (F4, F10, F40, F41, F49).
  - 5 are published records whose scripts are not named here (F33, F39, F79, F80, F81).
  - 1 is recorded only (F15).
  - 2 are superseded as a whole and kept for what they teach (F14 as evidence, F22 as an exact law).
- Within the 81, **8 rows have a named part withdrawn or superseded**: F6, F32, F34, F41, F49, F61, F69, F81. Cite only the
  surviving part.
- **10 rows carry a caveat that must be quoted with the number**: F7 (kernel-conditional), F11 (contested), F26 (hand-picked
  cell), F27 (exploratory), F29 (underpowered, no committed output), F38, F47 and F75 (hub re-run pending), F60 (the chain
  was stopped), F70 (errata).
- **12 numerology items (N1–N12)**; N8–N12 are new in CFG0.
- **24 withdrawn or superseded entries (W1–W24).**
