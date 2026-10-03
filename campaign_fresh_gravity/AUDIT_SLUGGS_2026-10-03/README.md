# AUDIT_SLUGGS (2026-10-03): is the SLUGGS "+4.0σ" a genuine failure of the law, analysed on the framework's own terms?

**Scope.** This is a hostile, two-sided audit of the claim in CFG313 (`CFG313_native_collapse_mass/`, row P5J) that the massive early types in SLUGGS fail the bare law at +4.0σ on native inputs. P5J is not new arithmetic. It passes through CFG55's law-alone number (H1: +0.0970 ± 0.0243 dex, 3.99σ canonical; 3.65σ alt). So the audit goes back to CFG55's raw inputs and machinery (h50 → CFG38 → CFG55), and to the follow-up lanes CFG57 (hot gas), CFG76 (re-derivation), CFG111 (literature γ), CFG113/CFG105/CFG106 (anisotropy) and CFG317.

- **Script:** `audit_sluggs_recompute.py` (under 1 s). It was written for this audit and reads the raw TSVs directly. It imports nothing from h50, CFG38 or CFG55. The only shared code is the frozen kernel `nu_mono`, read-only from CFG4_common.
- **Outputs:** `audit_sluggs_recompute.out` and `_results.json`. The main run passes 2/2 checks.
- **MUTATE (a₀/100):** outputs are `_MUTATE.out` and `_MUTATE_results.json`. The offset rises from +0.098 to +0.245 dex (+8.6σ), so the estimator responds to a₀. My pre-set threshold, a rise of more than 0.15 dex, **fails** narrowly at +0.147. The threshold did not allow for the JAM re-calibration absorbing part of the change. The FAIL is kept as it fell.
- **Fixed inputs:** κ = ½ (fitted), both footings (9.36e-11 | 1.13e-10), kernel ν_mono. No knob scans and no downloads. The sensitivity rows only reproduce physics inputs that earlier committed lanes already declared (γ from Alabi+17, β = ±0.5).

## Independent recomputation (from the raw files)

| | canonical | alt |
|---|---|---|
| CFG55 committed (ν_RAR, 16 galaxies) | +0.0970 ± 0.0243 (3.99σ) | +0.0880 ± 0.0241 (3.65σ) |
| this audit, ν_RAR, same 16 | +0.0968 ± 0.0243 (3.99σ) | +0.0879 ± 0.0241 (3.65σ) |
| **this audit, ν_mono (the framework kernel), same 16** | **+0.0977 ± 0.0243 (4.02σ)** | **+0.0885 ± 0.0241 (3.67σ)** |
| this audit, ν_mono, 17 (NGC 821 restored; h50's key bug) | +0.1003 ± 0.0230 (4.36σ) | +0.0911 ± 0.0228 (3.99σ) |

- Per galaxy, the audit agrees with CFG55 to ≤ 0.003 dex.
- 13 of the 16 galaxies have a positive offset. The median offset is +0.099.
- The smallest leave-one-out value is 3.64σ.

## Audit table

| # | Item | What was done | Framework-correct? | Effect (dex; σ) |
|---|---|---|---|---|
| 1a | Data products | Individual GC radial velocities (Forbes+17 erratum Table 5, VizieR J/AJ/153/114). SLUGGS galaxy table: SBF distances, R_eff, V_sys, K-band log M*. ATLAS3D XV: (M/L)_JAM from the self-consistent, mass-follows-light model (A), plus L_r, r_½ and quality. ATLAS3D XX: Salpeter population M/L, used only in a reported row. No SLUGGS mass profiles, no stellar-kinematics JAM of the outer halo, no fitted dynamical mass of the outskirts. | Yes. The observable is σ_GC(R) measured directly from raw velocities. | — |
| 1b | ΛCDM or halo inputs in the law row | The file carries NFW-based columns (XX `fDM_Re`, `logML_stars`). CFG55's law row reads only `logML_JAM`, `logL`, `logr12`, `qual` and `Dist_Mpc` (and `logML_Salp` in a reported row). JAM model A has no halo. Moster/Mandelbaum/Dutton–Macciò enter only h50's NFW comparator and the *rule* rows, which are CFG313's subject. | **Clean.** No NFW or halo-derived quantity enters the law prediction or the observable. | 0 |
| 1c | Spot check, 5 galaxies (NGC 1023, 4365, 4374, 4486, 5846) | Raw ATLAS3D rows and GC counts were re-read and re-binned with my own code. Clipped GC counts: 113, 244, 41, 648, 210. Offsets: +0.104, +0.205, +0.201, +0.275, +0.213, against CFG55's +0.101, +0.207, +0.200, +0.273, +0.213. | Yes. | ≤ 0.003 per galaxy |
| 1d | Provenance flag (new) | The on-disk velocity table has 3,575 rows, but the galaxy table's N column sums to 4,492. Examples: NGC 1023 has 113 rows against N = 210; NGC 3377, 126 against 217; NGC 4365, 244 against 308. The cause was not determined; the erratum's text is not on disk. | Unknown. It affects every lane equally and its sign is unknown. | not quantifiable |
| 1e | h50 key bug (known, CFG76) | NGC 720 and NGC 821 are dropped. Restoring NGC 821 (offset +0.142) *raises* the failure. | Bug, but in the framework's favour. | +0.003 dex; +0.34σ |
| 2 | Stellar mass / IMF | The headline row is **IMF-free**. M* is calibrated so the law reproduces each galaxy's own JAM mass inside r_½. Population masses are not used. Under the law, the Salpeter mass already over-predicts the inner JAM mass in **15/16** galaxies (median +0.120 dex). The SLUGGS K-band masses over-predict it in 10/16 (+0.084). Nulling the outer offsets needs M* a median **+0.30 dex** above the JAM ceiling, which would over-predict the inner kinematics by +0.25 dex. The Salpeter row's 1.8σ (CFG55 R3) is therefore excluded by the galaxies' own inner dynamics. A measured IMF gradient (bottom-heavy core, lighter outskirts) lowers the outer stellar mass and *enlarges* the deficit. | Yes. This is the most framework-correct choice available: dynamics-calibrated, IMF-neutral. A Kroupa/Chabrier M/L would understate baryons, but it was not used in the headline. | Headline: 0. Any heavier IMF is excluded by the inner JAM. Side note: a measured Salpeter-like IMF at σ ≳ 230 km/s plus the law *over*-predicts the inner mass by about 0.05–0.12 dex, a separate inner tension of opposite sign. |
| 3 | Hot gas | Omitted from the headline, as in h50/CFG55. CFG57 added measured X-ray gas (Lakhchaura+18, Fukazawa+06) for the 7 covered galaxies, using the physically valid D1 run. It moves the law's mean by **0.010 dex**. Nulling with the measured profile shapes needs 20× to more than 100× the measured gas. M87's GCs reach 109 kpc but its X-ray field ends at 30 kpc, so the Virgo ICM beyond that is untested. M87 alone would need M_b about ×10 at its outer bins (σ ∝ M_b^¼). | Omission is a known baryon shortfall; its measured size is small. | −0.010 dex (≈ −0.4σ). M87 beyond 30 kpc: open, and only M87 |
| 4a | Geometry and kernel | Spherical Jeans with a Hernquist profile (a = R_e/1.8153). The algebraic law is exact in spherical symmetry. CFG55 used ν_RAR rather than ν_mono, a spec deviation. Using ν_mono makes it +0.0009 dex worse. Taking the Hernquist scale from ATLAS3D's r_½ instead gives 3.99σ. | Yes, apart from the kernel slip (negligible). | +0.001 dex; +0.03σ |
| 4b | Tracer slope γ | γ = 3 for every galaxy, the same tracer input for any gravity. With the Alabi+17 relation (2.49–3.43; 3-D slopes): **3.64σ** (alt 3.25σ). A *shared* shift to γ = 2.34 brings it to 2σ. Per-galaxy measured slopes are not on disk. | Framework-neutral input, but unmeasured per galaxy. | −0.015 dex; −0.4σ (Alabi). This is the main systematic. |
| 4c | Anisotropy β | Isotropic. In this audit: β = +0.5 gives 4.23σ, β = −0.5 gives 3.90σ, and Alabi γ with β = +0.5 gives 3.42σ (alt 2.95σ). CFG114/106: only the corner γ_i − 0.4 with β = +0.5 falls below 2σ (0.6σ), which is more radial than any measured GC system. CFG105: truncating the tracer makes radial orbits *worse* (5.0σ at 20 R_e). An Osipkov–Merritt profile with r_a = 3 R_e removes it (−0.8σ). | Framework-neutral; the mass–anisotropy degeneracy is real. | ±0.004 dex; ±0.2σ for constant β. Up to −3.4σ only in the joint extreme corner. |
| 4d | EFE | Not modelled. The internal field at the outermost bins is g/a₀ = 0.26 (M87) to 1.5. M87 is the cluster centre, so EFE does not apply to it. EFE can only *lower* the prediction. | Omission favours the framework. | ≤ 0 (enlarges the deficit), small. No g_ext table is on disk. |
| 4e | Rotation and bins | σ per bin includes rotation (≈ v_rms), which is the correct second moment for a non-rotating Jeans model. Outer bins are R > max(R_e, 2 kpc). With all bins: 4.30σ. | Yes. | +0.005 dex |
| 4f | Intracluster GCs (Virgo centrals) | Not removed. If present they inflate σ_obs. Without the 4 group/cluster centrals (N = 12): +0.056 dex, **2.76σ** (alt 2.34σ). | Unmodelled contamination; removing it would help the framework. | up to −0.04 dex; −1.3σ (upper bound, by exclusion) |
| 5 | Statistic | Unweighted mean over galaxies of each galaxy's mean outer log(σ_obs/σ_pred). The error is the galaxy-to-galaxy SEM (ddof 1). No error floor and **no shared systematic term**: the γ and β uncertainty is not propagated. Selection is neutral: ≥ 30 clean GCs, ≥ 2 bins and ATLAS3D coverage, with no cut on the offset. Recomputed independently: 4.02σ. | The arithmetic is correct. The **z is statistical-only**, conditional on γ = 3 and β = 0. | The 4.0σ overstates certainty. With a shared γ systematic, CFG106 found 4.6–47% of draws below 2σ, depending on how the relation's coefficients correlate. |
| 6 | ΛCDM contamination anywhere | None in the law row (1b). ΛCDM inputs enter only the rule rows (Moster/Mandelbaum collapse masses, NFW) and h50's comparator. | Clean. | 0 |

## Bottom line

**Genuine failure, and it was not an analysis error. Its significance is smaller than "4.0σ" reads.**

- **The raw data were cut and analysed on the framework's terms:** raw GC velocities, ν_mono, κ = ½ on both footings, IMF-free dynamical masses, and no ΛCDM input.
- **Recomputed independently** from the raw files, the deficit is +0.098 dex (4.0σ canonical, 3.7σ alt). With h50's dropped galaxy restored it is 4.4σ.
- **Every framework-neutral baryon lever on disk runs the wrong way or is too small:**
  - IMF: closed by the inner JAM ceiling.
  - Measured hot gas: −0.01 dex.
  - EFE and IMF gradients make it worse.
- **What remains soft is the tracer, not the gravity:**
  - The 4.0σ is a statistical error at an assumed γ = 3 and isotropic orbits.
  - Published-relation slopes give 3.6σ.
  - A shared γ ≈ 2.3, or the joint γ − 0.4 with β = +0.5 corner, brings it below 2σ.
  - Without the four group/cluster centrals it is 2.8σ (alt 2.3σ).
- **Honest wording:** the law under-predicts the outer GC dispersions of SLUGGS massive early types by about 0.08–0.10 dex. That sign is robust to every input on disk. Its significance is 2.8–4.4σ depending on tracer assumptions and on the centrals, and it is not decisive while per-galaxy GC density slopes and anisotropies are unmeasured. This is the familiar group/cluster-central residual of MOND-type laws (M87 +0.27, NGC 5846 +0.21, NGC 4365 +0.21, NGC 4374 +0.20).

## Framework-native corrections that would need a new frozen lane (none applied; no frozen result is retro-fixed)

1. **Per-galaxy GC density profiles (largest lever).** SLUGGS/Subaru GC surface-density fits (e.g. Pota+13; Kartha+14/16; Hargis & Rhode), deprojected to γ_i at the bin radii, with the outer truncation. **Not on disk.**
2. **Measured GC anisotropy** for M87, NGC 4365, NGC 4374 and NGC 5846, plus NGC 1407 as a check (e.g. Zhu+14 and Agnello+14 for M87; Pota+15 for NGC 1407). **Not on disk.**
3. **M87 / Virgo hot gas to about 110 kpc** (deprojected n_e(r) beyond CFG57's 30-kpc field). Also hot-gas masses for the uncovered nine (Babyk+18 / Humphrey+06 gas profiles). **Not on disk.** `humphrey2006_ellipticals.tsv` holds NFW+stars fits only and has no gas profile. CFG57's raw gas sources are git-ignored, and they stop at 20–45 kpc.
4. **IMF:** no lane is needed for the outer test, because the JAM ceiling binds. If wanted, the *inner* tension in row 2 could be tested with Conroy & van Dokkum 2012 spectroscopic IMFs (or van Dokkum+17 gradients) against the JAM mass at r_½. **Not on disk.**
5. **Provenance (1d):** the Forbes+17 erratum text (AJ 154, 80) is needed to explain why the velocity table has fewer GCs than the galaxy table's N. **Not on disk.**

Downloads for items 1–5 need the owner's explicit yes.
