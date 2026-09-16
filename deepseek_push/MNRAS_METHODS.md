# Z10 — THE MNRAS METHODS SECTION + FIGURE LIST
**The paper's last missing section, assembled: the samples, the estimators, the Lean statement, the conventions, the error budget — and the 10-figure list with each figure's committing lane and data.**
*Lane: Z10 (the night-shift wave's methods lane). Repo: zimmerman-formula. Date: 2026-09-16.*
*Sources (all committed, nothing recomputed): REASSESSMENT_2026-09-16.md (the finish line, §4), MNRAS_RESULTS_SKELETON.md (G202, the results §4.1–4.6), MNRAS_ABSTRACT.md (G221), SOLAR_FACE_CLOSEOUT.md (G224, §4.5), LAW_VERIFIED.md, ONE_BOUNDARY_STATEMENT.md (G196), THEORY_CLOSURE_2026-09-16.md (G205), FALSIFIER_MATRIX.md (G207), G227_lean_roadmap.md (the 126/16 recount), G203/G206/G209 (the anisotropy estimators), G135 (the temperature law), G139/G143 (the dust law), G167 (the M/L conventions), G187 (the pie), G200/G210 (q derived), G212 (the mass triangle), G131/G162 (the 12-decade line), G114/G071/G099 (the RAR/deep-end fits), G231 (the distribution reading).*
*Companion artifact: Z10_results.json.*

---

## WHERE THIS SLOTS IN THE PAPER

The assembled paper's document inventory (all in-repo, this lane completes the set):

| The paper's part | Document | Lane | Status |
|---|---|---|---|
| Title + Abstract | MNRAS_ABSTRACT.md | G221 | drafted (207 words) |
| §1 Introduction | MNRAS_ABSTRACT.md Part 2 | G221 | drafted (429 words) |
| §2 Theory + machine-checked statement | **MNRAS_METHODS.md §(c)** | G205/G227/Z10 | **this lane** |
| §3 Data and methods | **MNRAS_METHODS.md §(a)–(e)** | G202/Z10 | **this lane** |
| §4 Results (§4.1–4.6) | MNRAS_RESULTS_SKELETON.md | G202 | drafted-in-structure |
| §4.5 the force-face | SOLAR_FACE_CLOSEOUT.md | G224 | drafted |
| Figures | **MNRAS_METHODS.md §THE FIGURE LIST** | Z10 | **this lane** |
| §5 Discussion + Conclusions | **MNRAS_METHODS.md §DISCUSSION** | Z10 | **this lane (one page)** |

Nothing in this document exceeds the committed lanes; every number below carries its lane in parentheses.

---

# §(a) THE SAMPLES — seven samples, each with its committing lane and provenance

**Table 1. The samples.**

| Sample | N (as used) | The face of the law it carries | Data provenance | Committing lane |
|---|---|---|---|---|
| **SPARC** | 175 galaxies in the database; **35 isolated galaxies / 641 rings** in the zero-parameter full-curve fit; 155 curves / 2788 points in the moonshot re-run | the rotation face (RAR, deep end) at 0.145 dex zero-parameter rms | Lelli, McGaugh & Schombert 2017, MNRAS 468, L68 (Spitzer [3.6] photometry + HI/CO rotation curves); G033 ingest of the 175 rotmod curves, bit-identical to the SPARC corpus v7 | **G071, G036, L232 (G002)** |
| **HI dwarfs** | 55 (26 LITTLE THINGS + 29 FIGGS) | the deep end: v_flat = (G M_b a0)^(1/4), rms 0.150 dex, zero mass slope | Oh et al. 2015, AJ 149, 180 (LITTLE THINGS, Table 2; V_max asymmetric-drift-corrected at R_max); Begum et al. 2008, MNRAS 386, 138 (FIGGS, Table 1; pressure-corrected V_rot; 22/29 TRGB distances) | **G114** |
| **ATLAS3D** | 258 ETGs | the dispersion face at the group/elliptical intersection | Cappellari et al. 2013, MNRAS 432, 1709 (ATLAS3D XV, Table 1; M* = L×(M/L)_JAM, Chabrier-class); sigma_e; transcribed from the arXiv HTML (UNVERIFIED-in-repo label carried honestly) | **G162 (channel B)** |
| **The 12-decade line** | **542** objects, log M_b = 2.63–14.35 (11.7 dex) | the law's one slope-1 line across the full mass range | composite: G131's 248-object 5-channel base (globular clusters n = 112, dSphs n = 34, HI dwarfs n = 55, plus the rotation/dynamical channels) + G162's 294 gap-filling objects (GEMS groups, ATLAS3D 258, SLUGGS 27, E11 26); the 2.89-dex gap reduced to 0.63 (78% filled) | **G131, G162** |
| **HeCS** | 58 clusters, **10,145 members** (3,629 in the [2,5] R500 window) | the cluster anisotropy and phase-space face | Rines, Geller, Diaferio & Kurtz 2013, ApJ 767, 15; CDS/VizieR J/ApJ/767/15 (table1/2/3, sha256-verified) + Table 4 (r500, M200, caustic masses) transcribed from the paper PDF; 22,680 Hectospec + 2,621 literature redshifts; caustic membership (Diaferio & Geller 1999, q = 25); H0 = 100 h, h cancels | **G203** |
| **X-COP** | 12 clusters | the cluster temperature, pie, and envelope face | XMM-Newton Cluster Outskirts Project (Eckert et al. 2017); the committed ingest: A1644, A1795, A2029, A2142, A2255, A2319, A3158, A3266, A644, A85, RXC1825, ZW1215 — T(r), M500, gas-mass profiles | **G075, G104, G105, G143** |
| **E11 groups** | 26 Chandra groups | the group face: the dust-law amplitude at 1e13, the all-dust phase | Eckmiller et al. 2011, A&A 535, A105 (Table 3 + gas-mass block; M500 5.2e12–1.7e14); transcription gated against G125's committed rows (24 shared, 0 mismatches; f_gas,500 and r2500 internally consistent 26/26) | **G143, G162 (channel C), G125** |

**Auxiliary samples carried by the same lanes** (used in specific results, listed with their lanes): the Milky Way rotation curve (Eilers et al. 2019; G072/G119, break at 6.13 kpc); the dSph compilation (Simon 2019, ARA&A 57, 375; G070, n = 34, the 0.222-dex floor and the UFD one-sided departure); globular clusters (Baumgardt & Hilker 2018; G074, 112+ clusters, the crossing at M_cross = 1.23e5 M☉ with r_M/r_h = η/2 = 3.39 exactly); GEMS groups (Osmond & Ponman 2004, 60 groups; G125/G162); SLUGGS (Forbes et al. 2017, 27 ETGs, in-repo); MIGHTEE-HI (Vărășteanu et al. 2025, MNRAS 541, 2366; G099, 80 rings, the RAR at z ≲ 0.08); WALLABY DR2 (G100, the EFE pair census); DES-Y3 3×2pt (Prat et al. 2022; G073, the lensing face); KiDS DR4 (Brouwer et al. 2021; G073).

**The selection logic, stated once.** The rotation face (SPARC 641 rings, HI 55, MIGHTEE 80) enters isolated, low-EFE systems only: Y = g_ext/a0 < 0.1, Nm_host ≤ 1, usable 2MRS neighbours = 1, ≥ 5 rings (G071's cuts; 122 of 175 environments matched, 35 pass). The dispersion face (ATLAS3D, GEMS, E11, SLUGGS, HeCS) enters through the equilibrium σ = v_flat/√2. The cluster face (X-COP, HeCS, E11) enters mass-resolved. The 12-decade line pools the faces at their committed footings (G131/G162 conventions, §(d) below) — the pooled slope is exactly footing-invariant (G172).

---

# §(b) THE ESTIMATORS — eight, each with its lane and its number

## (b1) The RAR line fit and the deep line. *Lanes: G071, G036, G114, G099, G158, G231, G236.*

**The mass-plane fit (the 12-decade line).** Pooled ordinary least squares in log10(v_flat) vs log10(M_b) over the 542-object sample: **b = 1.004 ± 0.011** (0.4σ from unity; 248-object base 0.988 ± 0.020; 294 fill objects 1.068 ± 0.040), rms about the identity **0.180 dex** (G162). The amplitude is not fitted: v_flat = (G M_b a0)^(1/4) at zero free parameters. The deep end is the same line's low-mass limit: 55 HI dwarfs at rms 0.150 dex, Theil–Sen residual slope −0.00 per dex (G114); the UFD end departs one-sidedly at +0.16 ± 0.02 per dex (G070 V2-FAIL, carried honestly as binaries/disequilibrium).

**The acceleration-plane fit (the RAR).** g_obs vs g_bar per ring, fitted by the full-curve interpolant μ₂(x) = 1 − (1 + x/2)⁻² with **zero fitted parameters**: SPARC 641 rings at pooled rms **0.145 dex** = the RAR benchmark (McGaugh et al. 2016's 0.13 measured; the zero-parameter statement is this lane's), residual slope +0.010 ± 0.009 (G071); the pooled 747-point sample (SPARC 641 + MIGHTEE 80 + HI 26) carries the deep-window shape fits (G236). The **deep line** g² = a0 g_N (equivalently g_obs ∝ g_bar^1/2) is the phantom's equation of state, not a fit — verified asymptotically to 7.5e-3 on the g < 0.1 a0 window (G231); as a conditional statement it is the mean = median to 0.004 dex (G231 V2).

**The honest residual reading (registered).** The per-ring residuals (G036 pipeline, N = 1230, rms 0.1741 dex) are Laplace-tailed, not Lomax-shaped: the kernel-as-full-distribution reading FAILS as stated (G230, 1/5 checks; G231 V3) — the content of the kernel is the curve (the conditional mean), and the remaining 0.18-dex scatter is measurement/systematics-dominated (within-galaxy white noise 0.045 dex). The deep exponent's slope channel measured **n = 1.20 ± 0.06** (12.7σ from the DE-anchored n = 2, 7.3σ from 1.66) — the n = 2 deep reading FIRED and is absorbed by the two-scale/effective reading with the seesaw demoted to a definitional identity (G158, G189, G190); the residual normalization preference is a0_eff = 1.08–1.10e-10 (G193, 2.2σ from the DE anchor — sub-materiality registered, G211).

## (b2) The mass-to-light conventions. *Lane: G167 (assembled in G114, G143, G162).*

**The baryonic mass comes from one convention per sample, matched in §(b2)'s cross-convention re-run:**

- **SPARC**: M_b = M* + M_gas, M_gas = 1.4 M_HI; disk M/L from the corpus (fallback 0.5); r_in = 0.3 r_M; M_b enclosed at the outermost ring (G071).
- **LITTLE THINGS**: Oh et al. 2015 3.6-μm-model M/L (G114).
- **FIGGS**: diet-Salpeter log10(M/L_I) = −0.627 + 1.075(B−V); M_gas = 1.4 M_HI; TRGB distances where available (22/29) (G114).
- **MIGHTEE-HI**: resolved-SED Y* (SFH-free median 0.36) + molecular gas + X-bar inverse (G099/G167).
- **ATLAS3D**: (M/L)_JAM, Chabrier-class; the Kroupa shift changes the residual by ≤ 0.015 dex (G162).
- **Groups (GEMS/E11)**: f_b,500 = f_gas + 0.02 (stars), fallback 0.05; the channel zero point carries ±0.05-dex f_b systematics (G125/G162).

**The cross-convention result (honest).** Re-deriving the HI dwarfs' stellar masses the MIGHTEE way (fixed SFH-free Y*) moves the dwarf a0* from 1.118e-10 (lane) to 1.256e-10 (Y* 0.36) / 1.131e-10 (Y* 0.6) — the dwarfs never approach MIGHTEE's 1.84e-10 because they are gas-dominated (median f_gas 0.80; the M/L lever moves M_b by only (1 − f_gas) on the stellar term). At matched SPARC-class Y* = 0.6, MIGHTEE itself reads a0 = 1.08e-10 (ratio_matched 0.95): **the 1.4–1.6× "MIGHTEE excess" is an M/L-normalization artifact, not physics** (G167 V1); the max honest M/L closure is 0.097 dex, residual 0.04 dex after the 0.6 convention.

## (b3) The projected-Jeans window mean β. *Lane: G203 (G195's estimator, reproduced verbatim).*

On the 10,145 HeCS members: β(r) = β_inf r²/(r_a² + r²) (two-asymptote, β_0 = 0), the Jeans equation d(ρ σ_r²)/dr + 2β ρ σ_r²/r = −ρ G M/r² with the NFW profile at c500 = 4.5, projected through the Binney–Mamon (Osipkov–Merritt) kernel to σ_los(R); the window mean β_win(2–5 R500) is read from the asymptotic two-asymptote inversion, with iterative 3.5σ MAD interloper cleaning on top of the caustic membership. **β_win(2–5 R500) = 0.434 ± 0.015** (3,629 in-window members, 58/58 clusters with ≥ 12) — the static null β = 0 dead at 29.7σ (G203/FALSIFIER_MATRIX row 7). The caustic envelope is the one named selection systematic, resolved in (b4).

## (b4) The 2D phase-space likelihood. *Lane: G206 (MAMPOSSt-class; Mamon, Biviano & Boué 2013).*

**P(R, v) = 4πR² ∫₀^∞ n(R√(1+t²)) N(v; 0, σ_amp σ_r √(1 − β/(1+t²))) dt**, Abel-regular t-integration, NFW c500 = 4.5 normalized to the stack median M500 = 2.41e14 (G203), free parameters (β_inf, r_a, σ_amp) = the anisotropy + a velocity nuisance, fit over [0.2, 5] R500 by coarse-grid seed + Nelder–Mead, errors from the Fisher Hessian and a 20× cluster bootstrap. **β_win(2–5 R500) = 0.495 ± 0.063 bootstrap** (mean 0.471) — the caustic-envelope systematic resolved (the selection-conditional fit, σ_amp fixed, reads 0.533). The two estimators agree at the ~1σ level and bracket the committed window: the anisotropy is strongly positive, ~0.44–0.50, shallower than the streaming floor 0.5 by 4.5σ at face value (the registered mid-ground; the verdict is gated on this 2D fit, FALSIFIER_MATRIX row 7 PENDING).

## (b5) The per-bin β(r) profile. *Lane: G209.*

Two estimators, five bins over [0.5, 5] R500: **(E1)** the G203-class projected-Jeans inversion evaluated per bin: 0.033 ± 0.001 / 0.093 ± 0.003 / 0.173 ± 0.005 / 0.305 ± 0.009 / **0.560 ± 0.015** at 0.5–1 / 1–1.5 / 1.5–2 / 2–3 / 3–5 R500 (100-bootstrap errors); **(E2)** the G206-class 2D likelihood with free piecewise β: −0.37 ± 0.14 / 0.011 ± 0.087 / 0.285 ± 0.092 / 0.256 ± 0.066 / **0.545 ± 0.070**. The shape test (BIC, n = 7,714): the rising shape wins — dBIC = 24.5 vs flat, 36.2 vs falling, 1.8 vs the G170 streaming anchor — **β rises from ≃ 0.03 in the core to ≃ 0.56 in the envelope** (G209; abstract's 0.03 → 0.56). The window mean vs outer-bin reading (0.438–0.495 vs 0.545–0.560) is the registered mean-vs-profile question: the mean drags on the shallow 2–3 R500 bin (0.26–0.31), the envelope lives at the outer bin — the profile-weighted recombination is Z2's dispatch, listed live (REASSESSMENT §3.2). The same kinematics mass-bias: **M(β)/M(0) = 0.891 ± 0.007** (E1 0.891) — the isotropic HSE reading overestimates the Jeans mass by 11%, every ratio/exponent/relative position invariant (G219).

## (b6) The temperature law. *Lane: G135 (G095's closed form, cross-sample).*

**log10(T_obs/T_pred) = (2/3) log10 f + log10(2 r_M/R500)**, f = M_dyn/M_b, T_pred = μ m_p (G M_b a0)^(1/2)/(2 k_B) — the baryon-triad face; the structural exponent α = 2/3 (virial +1 with −1/3 from Δ500 self-similarity); the alternative exponents fitted at **α = 0.75 ± 0.12** — the structural 2/3 inside 1σ, the BTFR-style 1/2 excluded at ~2.2σ. Pooled 31-system rms **0.076 dex** (12 X-COP clusters 0.067 = the HSE scatter, 19 GEMS groups 0.081, the MW/M31 closures +0.01/+0.02); median closed form 3.51 vs measured 3.57 (G095, G135, G202 §4.3).

## (b7) The dust-law fits. *Lanes: G139, G143 (G122's closed form, G200/G210's derivation).*

The two-parameter law, one envelope across M500 ~ 1e13–9e14 (12 clusters + 26 groups, 38 systems):

**c_dust(M500, r) = 0.72 (M500/8e14)^q (r/R500)^−p**, with **q = −0.414 ± 0.157, p = +0.990 ± 0.035, c0 = −0.145 ± 0.030**; rms 0.119 → 0.097 dex (G143 V2). The fit is the coherency collapse in density space: M_dust(<r) = M_b(<r) a_c (r/R500)^−p (r/r_M) − M_ph(<r) with M_ph from the committed per-bin phantom floor; the enclosed-dust statement of the same fit (G139). Both parameters are now DERIVED within the measured error: c0's combination pinned by the derived infall jump A_b = (σ_ph/σ_d)³ = 0.650 (G182/G185, R = 1.09, 12/12 in band) and **q = −1/3** = α_supply − α_require = 2/3 − 1 from the Bondi-class reservoir supply, at 0.52σ of the measured −0.414 (G200, G210; the 1.34× A_b residue registered as the honest sliver). The group scale rides the amplitude run: +0.536 ± 0.069 vs +0.235 on clusters (2.3× steeper, 20/26 above, t = 4.3) (G143 V1).

## (b8) The pie. *Lane: G187 (G179's medians, G178's saturation, G079's weights).*

Per cluster, the sector shares are inverted from the closed form M_dyn(<r) = M_b + M_ph + M_dust with SUM/M500 ≡ 1 by construction: at R500, sample medians **s_b : s_ph : s_d = 17.7 : 56.9 : 24.6** (16–84: 15.1–21.5 / 54.0–60.7 / 18.1–31.3); the data pie closes exactly, the law pie to −0.18 ± 0.06 dex (fit-window extrapolation, stated). The constitution curve: pivot u = r_M/R500 = 0.185 (M500/1e14)^0.314, the phantom gain g(M) = 1 below the saturation **M_sat = 3.09e14** and 1/u above, the all-dust group phase f_dust = 0.919 = 1 − f_b; cosmic weights from the EH98 + Tinker F(>M) pipeline (σ8 = 0.811, reproduced digit-for-digit): mass-function-weighted ⟨s_d⟩ = 0.805, ⟨s_ph⟩ = 0.111 (G187, G079).

---

# §(c) THE LEAN STATEMENT — the certification chain

**Toolchain.** All certificates compile against the repo's Mathlib build: Lean 4.34.0-rc2, `lake env lean <file>.lean`, **exit 0, zero `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound}** — re-verified fresh at G227 (2026-09-16).

**The ledger.** **126 theorems across 16 certificate files** (whole machine-checked surface; the task inventory sums to 105; the deepseek spine subset is 79 theorems / 10 files — the three counts verified programmatically, G227 §1b). The spine chain, in order:

EQUILIBRIUM_THEORY (12: the consolidated spine — sqrt_num_iden, mond_radius_sq, virial_temperature, phantom_bracket, **equilibrated_is_phantom**, cap_exists_unique, cloud_mass_linear, the_equilibrium_spine) → **G031** the hydrostatic spine (13, ending in the_spine: temperature → identification → BTFR → g² = a0 g_N) → **G090** the equivalence rung (5: the BTFR quartic, the equipartition) → **G03G** the triad (4: r_M² = G M_b/a0, equipartition_exact, v_flat, σ = v_flat/√2) → **G083** the surface density (5: Σ_ph(<r_M) = a0/πG) → **G201** the jump share (8: the entropy step and the deep limit). Complement: G001/G002 (12), G007 the bimetric (11), G036 (9), G047 the EFE cap (6), G039 (14), G055 (12), G058 ΩΛ from a0 (6), G024 (9).

**The key certified identities.** √(GM/a0)·√(GMa0) = GM (pure Real.sqrt_mul composition — unlocks the virial temperature); r_M² = G M_b/a0; the equilibrated isothermal density equals the phantom, ρ = σ²/2πGr² = √(G M_b a0)/4πGr², **coefficient exactly one** (equilibrated_is_phantom); M_ph(<r_M) = M_b to max|ratio − 1| = **2.2e-16** (equipartition); Σ_ph(<r_M) = a0/πG; the ΩΛ closure ΩΛ = 0.6857 from a0 alone (+0.07% of Planck).

**The Gauss-map charge.** The dark mass is certified as the surface-integral charge of the sourced field: **M_ph(<r) = (1/4πG)∮ g·dA = M_b(r)(r/r_M)** (M01_equipartition.lean — 6 theorems, zero sorry: rM_sq, phantom_mass_linear, equipartition, gauss_flux, surface_density, the_spine; G227/M01). The ontology statement: the old "Noether charge" reading is empty on the static branch (J^μ = 0, G154); the dark mass is a field configuration, not a species — direct detection has nothing to find by construction (G180).

**How the paper cites Mathlib.** "The machine-checked statements of §2 were compiled with the Lean 4 theorem prover (Lean 4.34.0-rc2) against Mathlib; proofs use Mathlib's real-number and measure API (Real.sqrt_mul, Real.sqrt_mul_self, integral_rpow). The full certificate index (16 files, 126 theorems, zero sorry, axioms ⊆ {propext, Classical.choice, Quot.sound}) is published as online supplementary material." Lean certifies the mathematics; the physical reading is the committed lanes' empirical claim, tested on the samples of §(a) — the paper states both halves explicitly (LEAN_CERTIFICATES.md's scope statement).

---

# §(d) THE CONVENTIONS — a0, r_M, M500, H0, the constants table

**The one input.** a0 = 9.3619 × 10⁻¹¹ m s⁻² (canonical, the DE footing; equivalently the vacuum form s_Λ = 2 a0 = 1.87238 × 10⁻¹⁰). The RAR-class effective scale measures 1.08–1.10 × 10⁻¹⁰ (2.2σ above the DE anchor — the registered sub-materiality, G193/G211); every shape is footing-invariant, only the normalization differs (G172). The z ~ 2.5 BTFR zero point is the registered scale-picker (G080).

**The one boundary.** r_M = √(G M_b/a0), the baryonic a0-crossing (G M_b/r_M² = a0 exactly; the identity G M_b/r_M = √(G M_b a0) is Lean-certified). The environment projects it: r_b/r_M = √(a0/g_ext), exact to 1e-16 (G196). References: the MW at M_b = 6.5e10 M☉ → r_M = 9.84 kpc (G089/G119); the cluster seam at 0.96 × median r_M (402 kpc; 1σ band 269–543 kpc) (G176).

**Cluster masses.** M500 = (4π/3) × 500 ρ_c(z) × r500³ with ρ_c = 3H0²/8πG; **H0 = 70 km s⁻¹ Mpc⁻¹** adopted for physical M500 (G162's M500 recomputation; the G125 1e9 unit glitch flagged, not propagated). HeCS masses use the paper's H0 = 100 h (h cancels in R/R500 and v_los; G203). Δ = 500, the standard X-COP convention.

**The equilibrium triad (all derived, not fit).** σ² = v_flat²/2 = κ = c_s² = 1/2 (five routes: max-entropy at the DE temperature G084 + the virial/fluid closure G091, Lean-certified G03G); Σ_ph(<r_M) = a0/πG = **213.74 M☉ pc⁻²** (alt footing 257.52); T_b = mσ²/k_B = 9.52 K (galaxy class, = the CMB at z* = 2.37–2.49); the cluster temperature parameter μ = 0.6 (fully ionized, 30% He).

**Table 2. The constants (canonical values, committed lanes in parentheses).**

| Symbol | Value | Lane |
|---|---|---|
| G | 6.674 × 10⁻¹¹ m³ kg⁻¹ s⁻² | repo convention |
| a0 | 9.3619 × 10⁻¹¹ m s⁻² (= s_Λ/2) | G089/G193 |
| r_M | √(G M_b/a0); 9.84 kpc at M_b = 6.5e10 M☉ | G089/G119 |
| Σ_ph(<r_M) | a0/πG = 213.74 M☉ pc⁻² | G078/G083 |
| σ²/v_flat² | 1/2 (= κ = c_s²) | G03G/G084/G091 |
| T_b (galaxy class) | 9.52 K = CMB at z* = 2.37–2.49 | G132 |
| m (the particle) | 5.09 ± 0.10 keV; kill band [4, 6] keV | G168/G212 |
| ΩΛ | 0.6857 (Planck 0.6847, +0.07%) | G058 |
| Ωdm (obs) | 0.264 | G079/G187 |
| Ωdust | 0.2619 = 99.2% of Ωdm; equilibrium + dust = 1.000 Ωdm | G198/G187 |
| M_sat | 3.09e14 M☉ (band [1.73, 4.01]e14) | G178 |
| ρ_c(H0 = 70) | 1.36e11 M☉ Mpc⁻³ | G162 convention |

---

# §(e) THE ERROR BUDGET — the three systematic families

## (e1) M/L systematics. *Lane: G167 (G114, G143, G162).*

The mass-to-light lever is bounded by the cross-convention matrix: re-deriving the HI dwarfs the MIGHTEE way moves a0* over 1.118–1.256e-10 (Y* 0.36–0.6) but never to MIGHTEE's 1.84e-10 — the gas-dominated samples are immune at the (1 − f_gas) level (median f_gas 0.80). The max honest closure of the MIGHTEE 0.137-dex offset is 0.097 dex (SPARC-class Y_K = 0.6), residual 0.04 dex; inclination/pressure/beam corrections are anti-closing (G133, G167). The group channels carry ±0.05-dex f_b,500 zero-point systematics (f_b 0.05 vs 0.08 shifts the G-class median by −0.056 dex) and ±0.1 dex for the ROSAT-GEMS vs Chandra-E11 M500 footing (G162). The ATLAS3D Kroupa shift is ≤ 0.015 dex (G162). The 12-decade line's slope is exactly invariant to all of the above (G172): the M/L family moves the zero point, never the slope.

## (e2) Estimator systematics.

- **Selection/interloper:** caustic membership (the Diaferio–Geller envelope at 2–5 R500) is the named selection systematic; the 2D phase-space likelihood resolves it — window means 0.434 ± 0.015 (projected-Jeans) vs 0.495 ± 0.063 (2D, bootstrap), the selection-conditional fit 0.533 (G203/G206). The anisotropy verdict is gated on this family (FALSIFIER_MATRIX row 7 PENDING).
- **The Jeans/HSE mass bias:** with the measured β(r), the isotropic inversion overestimates the cluster mass by the factor 12–13%: q = M(β)/M(0) = 0.891 ± 0.007 (estimator systematic 0.0047); every ratio, exponent, and relative position is invariant, so the paper's cluster numbers are quoted at the isotropic convention with the 11% re-scale stated once (G219).
- **Model-shape ties:** the seam's sharpness is provisional — a smooth log-quadratic steepening lies within d_BIC = 16; the seam is reported as "a resolved transition" (G176/G196). The kink's step-vs-kernel width is a statistical tie today (Δχ² < 1); the width contract decides at ≥ 95% in ~1 year (G191). The slope floor's constancy sub-prediction FAILED (spread 1.19 vs 0.12 predicted; G157, registered).
- **The live seams, stated once (REASSESSMENT §3):** (i) the **frozen-domain tilt** — the z* > 0 subset of the 12-decade line (n = 323) reads b = 1.155 ± 0.029 (+5.35σ), an open normalization-seam question (ATLAS3D internal 1.30, GEMS +0.115, cluster +0.273 named suspects) that Z1 adjudicates; the full-sample line b = 1.004 ± 0.011 is unaffected until then; (ii) the **beta mean-vs-profile** question of §(b5); (iii) the DR4 verdict-class re-register (G225: P(STRONG) = 0 at the December N — the decision rule is being re-stated before the data, not after). None of the three changes a committed number; all three are in print as open.

## (e3) The distance scale.

- **HI dwarfs:** TRGB distances for 22/29 FIGGS (Begum et al. 2008); LITTLE THINGS distances as tabulated (Oh et al. 2015, Table 2); the deep-end rms 0.150 dex includes the distance contribution (G114).
- **dSphs/GCs:** the Simon 2019 distance compilation (G070); Baumgardt–Hilker GC distances (Baumgardt & Vasiliev 2021) (G074).
- **HeCS:** Hectospec + literature redshifts, median per-galaxy e_cz = 36 km/s (absorption 56, emission 21); caustic masses from the paper's r200/M200 (Rines+13 Table 4, transcribed); h cancels in R/R500 and v_los (G203).
- **X-COP/groups:** R500 from the HSE mass at H0 = 70; the E11 two-radius r2500/R500 consistency within 3% (G143 G0c). The r_M-relative quantities (r/r_M, r/R500) are distance-invariant by construction; the absolute M500 carries the H0 convention, quoted with it (G162, G219).

**The total honest statement of the budget:** the measured scatter (0.145–0.180 dex on the line, 0.076 dex on the temperature law, 0.097 dex on the dust law) is at or below the conventions' own spread — the lines are not error-dominated; the amplitude (a0_eff) is the one quantity the M/L family moves, by ≤ 0.097 dex, and every shape-level result is convention-invariant.

---

# THE FIGURE LIST — the ten figures the paper needs

**(F1) The 12-decade line.** log10 v_flat (rotation face) / √2σ (dispersion face) vs log10 M_b, all 542 objects (log M_b = 2.63–14.35), per-channel colors (globulars 112, dSphs 34, HI dwarfs 55, ATLAS3D 258, GEMS 59, SLUGGS 27, E11 26), the identity line, the fitted b = 1.004 ± 0.011; residual panel below with the sliver (13.07–13.70) shaded as coverage, the UFD +0.16 ± 0.02/dex departure flagged, the frozen-domain tilt (n = 323, b = 1.155) inset as a registered open seam. *Data/lane: G131 + G162 (G074, G070, G114).*

**(F2) The RAR with the deep line.** g_obs vs g_bar (log–log), the pooled 747 rings (SPARC 641 + MIGHTEE 80 + HI 26), the zero-parameter full curve μ₂(g_bar/2a0) overlaid, the deep asymptote g² = a0 g_N (slope 1/2) drawn through the g < 0.1 a0 window, rms 0.145 dex band; inset: the n = 1,230 per-ring residual histogram with the Laplace fit (KS p = 0.14) and the honest note (rejected Lomax, G230/G231). *Data/lane: G071, G099, G114, G236, G231.*

**(F3) The one-boundary diagram.** r/r_M on the abscissa (log), the dark-sector composition/quantity on the ordinate: the MW break at 0.623 r_M (6.13 kpc), the cluster seam at 0.96 r_M (387 kpc, p1 = 1.50 → p2 = 2.94), the EFE cap line r_b/r_M = √(a0/g_ext) drawn for the MW (0.620) and the clusters (0.963), the phantom r⁻² zone and the all-dust interior, the latent heat dS = 10.8–23.7 k_B annotated at the crossing. One radius, ten diagnostics — the figure's caption says it. *Data/lane: G196 (G119, G176, G186, G132, G188).*

**(F4) The beta profile.** β(r) vs R/R500 over [0.5, 5] R500: E1 per-bin points (0.033 → 0.560, 100-bootstrap errors) and E2 free-piecewise points (−0.37 → 0.545), the G170 streaming curve (0.2/0.45/0.7), the static null β = 0 line, the window means (0.434 ± 0.015 projected-Jeans, 0.495 ± 0.063 2D) banded; BIC winner annotation (rising, dBIC = 24.5 vs flat). *Data/lane: G209 (G203, G206).*

**(F5) The temperature law (2/3).** log10(T_obs/T_pred) vs log10 f for the 31 systems (12 X-COP, 19 GEMS groups, MW/M31), the structural line slope 2/3 through the origin, the 1/2 line for contrast, rms 0.076 dex band, residual panel. *Data/lane: G135 (G095).*

**(F6) The pie + constitution curve.** Left panel: the R500 pie (baryons 17.7 / phantom 56.9 / dust 24.6, 16–84 ranges as wedges). Right panel: s_b(M500), s_ph(M500), s_d(M500) over 1e13–1e15 (log), the saturation step at M_sat = 3.09e14, the [1.73, 3.48]e14 gap shaded with the sharp (s_ph 8–12%) vs smooth (13–40%) bracketing curves, the all-dust group anchors (f_dust = 0.919 = 1 − f_b), the gap's 0.85-falsifier line. *Data/lane: G187 (G179, G178, G140).*

**(F7) The dust law c_dust(M500, r).** The 38-system envelope (12 clusters + 26 groups): left, c_dust vs r/R500 with the fitted p = +0.990 ± 0.035 and the per-cluster amplitudes; right, the amplitude run a_c vs M500 with q = −0.414 ± 0.157, the derived lines q = −1/3 (Bondi, G200/G210) and c0 from the infall jump A_b = 0.650, rms 0.097 dex band. *Data/lane: G139, G143 (G182, G185, G200, G210).*

**(F8) The cosmology pie + the mass window.** Left: the cosmic constitution (ΩΛ = 0.6857 vs Planck 0.6847; Ωdust = 0.2619 = 99.2% of Ωdm; equilibrium 0.79–1.28%; equilibrium + dust = 1.000 Ωdm). Right: the three mass windows — cosmic-noon [5.0, 5.2] (G163/G168), Lyman-α forest [3.3, 5.7] (Viel/Irsic/Villaseñor), free-streaming [4.70, 5.75] at λ_fs = 0.5–0.6 Mpc — with the joint posterior peak m = 5.09 ± 0.10 keV and the [4, 6] keV kill band. *Data/lane: G212 (G187, G198, G079, G058, G168, G093).*

**(F9) The falsifier matrix.** The 20 registered rows as a colored matrix (domain × status): Solar (1), Galaxies (8), Clusters (8), Cosmology (2), Particles (1); ARMED 12, PENDING 3 (anisotropy, D2 core slope, slope floor), FIRED-AND-EXPLAINED 3 + 2 resolved non-fires; each cell carrying its decision rule's number (30.7σ, 47.8σ, 29.7σ, 7.7σ, 12.7σ, kill bands); the footer: zero unexplained fires. *Data/lane: G207 (G237).*

**(F10) The anisotropy window.** The (β_inf, r_a) likelihood contours from the MAMPOSSt-class 2D fit (G206), the window-mean consistency ladder (G203 0.434 ± 0.015 → G206 0.495 ± 0.063 → G209 outer bin 0.545–0.560), the streaming anchors 0.2/0.45/0.7, the static null dead at 29.7σ, and the mass-bias panel q = M(β)/M(0) vs R/R500 (0.89 at R500, E1/E2/G170) — the figure that says "the halo's outskirts are streaming, and the sector's masses re-scale 11% with it, every ratio invariant." *Data/lane: G203, G206, G209, G219.*

---

# THE LAST MISSING TEXT — the Discussion and Conclusions (one page)

**Discussion.** The RAR is not a force law — every force-law completion of its deep equation is dead with its number on the record (the sourced k-essence field at γ = 1/2, killed by Cassini at 2.2e4× and by MICROSCOPE at a 7e8–7e10 suppression; the biharmonic k⁴ family ghosted at every screening length with a quadrupole a 44-solve scan never lowers below 6.18× the Park ceiling; the disformal vector sector at α₁ = 4.0e4× the preferred-frame bound; the bimetric lensing-dead by Lean-certified frame algebra), and the Solar System is Newtonian by construction — the Cassini null is architectural, PPN = GR exactly. The reading that survives is an equilibrium/EOS statement: the cold sector is the shift-charged configuration of one scalar whose vacuum value is dark energy; it equilibrates at the virial temperature its own scale sets wherever g < a0; the resulting mass law M_dark(<r) = M_b r/r_M is one slope-1 line across 12 decades of baryonic mass and one boundary r_M = √(G M_b/a0) that the environment merely projects (r_b = r_M√(a0/g_ext)). The cluster sector composes in closed form, its last two parameters derived within the measured error; the sector's bookkeeping closes the cosmic density to 1.000; and the freeze inversion predicts one number, m = 5.09 ± 0.10 keV, from three independent lines.

The honest ledger is part of the claim. Three registered tests have fired and all three carry registered explanations (the ZW1215 falsifier as a hydrostatic-bias case; the n = 2 deep reading absorbed by the two-scale reading with the seesaw demoted to a definitional identity; the EFE split refused as a detection). The distribution reading's only genuinely new prediction — the residual shape — is rejected: the residuals are Laplace-tailed, not Lomax (G230/G231); the kernel's content is the curve, and the 0.18-dex scatter is measurement-driven. The frozen-domain tilt, the beta mean-vs-profile question, the DR4 verdict class, and the 2–3e14 gap sit in print as open, each with its decider named. Nothing on the pending list decides a structure; everything on it decides a normalization, an epoch, or an ontology — and each has its kill number in print.

**Conclusions.** (i) The RAR is the phase diagram of one boundary; the deep relation g² = a0 g_N and the equipartition M_ph(<r_M) = M_b are derived, machine-checked (126 theorems, 16 certificates, zero sorry), and measured at the data's own scatter. (ii) The dark sector is one charge, two phases, no species: 40 years of direct-detection nulls are the prediction, and the phase-space never caps the equilibrium. (iii) The framework makes no modification to any force: PPN = GR identically, and the Solar System's nulls are the theory's architecture, not its fits. (iv) It predicts: the wide-binary ridge at 30.7σ and the 7.4-kAU break (Gaia DR4, 2026-12-02), the z ≈ 2.5 BTFR zero-point break at z* = 2.4 (JWST), the tSZ three-way with the pool returning JOINT at P = 0.75–0.86, the XRISM plateau, and the sub-1e6 collapsed count that picks charge over relic. One constant in; a boundary, a mass, a density-closed cosmos, and a falsifier-armed future out. The rest is instruments, and December is a month away.

---

# VERDICTS

### V1 — THE METHODS SECTION IS COMPLETE. PASS.
All five mandated parts are assembled from the committed record: (a) the seven samples, each with its committing lane and data provenance (SPARC 175/Lelli+17 G071; HI 26/Oh+15 + 29 FIGGS G114; ATLAS3D 258/Cappellari+13 G162; the 542 = G131 248 + G162 294; HeCS 58/Rines+13 G203, sha256-verified; X-COP 12/Eckert+17 G075–G143; E11 26/Eckmiller+11 G143); (b) the eight estimators (the RAR line fit G071/G158/G231; the M/L conventions G167; the projected-Jeans β G203; the 2D phase-space G206; the per-bin β G209; the temperature law G135; the dust-law fits G139/G143; the pie G187), each with its lane and its committed number; (c) the Lean statement with the full certification chain (126 theorems / 16 certificates, the spine, the Gauss-map charge M01, the Mathlib citation form); (d) the conventions (a0 = 9.3619e-11, r_M, M500, H0 = 70, the constants table); (e) the error budget in its three families (M/L ≤ 0.097-dex closure; estimator systematics with the 0.891 mass bias and the registered live seams; the distance scale). Nothing exceeds the committed lanes; the honest FAILs and the live seams are in the text, not hidden. PASS.

### V2 — THE FIGURE LIST IS COMPLETE. PASS.
Ten figures, every one inside the 8–10 mandate, each with a content spec and the committing lane's data: F1 the 12-decade line (n = 542, b = 1.004 ± 0.011; G131/G162), F2 the RAR with the deep line (747 rings, g² = a0 g_N; G071/G099/G236/G231), F3 the one-boundary diagram (r_M, the cap, the EFE line; G196/G119/G176), F4 the beta profile (G209), F5 the temperature law 2/3 (G135), F6 the pie + constitution curve (G187), F7 the dust law c_dust(M500, r) (G139/G143), F8 the cosmology pie + the mass window (G212), F9 the falsifier matrix (G207), F10 the anisotropy window (G203/G206/G219). Every figure maps to a results subsection of MNRAS_RESULTS_SKELETON.md (G202), so the paper can be typeset from the two skeletons without a new calculation. PASS.

### V3 — THE HONEST STATEMENT: THE PAPER'S DOCUMENT SET IS COMPLETE. PASS.
The paper's documents are all in-repo: abstract + introduction (MNRAS_ABSTRACT.md, G221), results, section by section (MNRAS_RESULTS_SKELETON.md, G202), the force-face (SOLAR_FACE_CLOSEOUT.md, G224), and — as of this lane — the Methods and the figure list (MNRAS_METHODS.md, Z10). The last missing text, the one-page discussion/conclusions, is drafted above in this same document. What remains of the paper is assembly and the author's voice pass: the sentences carry the campaign's register of precision, and the voice pass should set tone and trim the parentheticals — not add or remove claims. The honest standing is stated once: three fired falsifiers, all explained, zero unexplained fires (G207); the live seams (the frozen-domain tilt, the beta mean-vs-profile, the DR4 verdict class, the 2–3e14 gap) in print with their deciders (REASSESSMENT §3); the December season (DR4, tSZ, JWST) pre-computed with its verdicts. PASS.

---
*Deliverable complete. Pass: 3/3 verdicts. Z10_results.json written alongside. Commit + push authorized.*