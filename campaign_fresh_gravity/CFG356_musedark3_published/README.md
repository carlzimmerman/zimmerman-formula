# CFG356 -- MUSE-DARK III as published (A&A 709, L16, 2026): version check against CFG190 / CFG198 / CFG199 / CFG236, and the mass-method crux

**Reading and comparison only. No new computation**, so no frozen criteria. Nothing was re-run, because nothing material changed (section 2).

## 1. Which version was read, and how

- **The A&A route failed.** The A&A PDF URL (`aanda.org/articles/aa/pdf/2026/05/aa59230-26.pdf`) and the DOI resolver (10.1051/0004-6361/202659230) both returned HTTP 403. The 772-byte HTML error page was deleted and not kept.
- **arXiv:2604.22613 has ONE version, v1** (submitted 24 Apr 2026). The abs page shows Comments "Accepted in A&A" and Journal-ref "A&A 709, L16 (2026)".
- **The v1 PDF is the accepted manuscript**, not a pre-referee draft:
  - its running header reads "A&A proofs: manuscript no. paper_v4";
  - its acknowledgements thank the anonymous referee.
  - So it is the refereed text. Only A&A's copy-editing could differ, and that could not be checked (403).
- **The PDF is kept outside the repo:** `../_external_data/arxiv_pdf/2604.22613v1.pdf` (11 pages, 1,516,976 bytes, sha256 `c4a97a051101862e0ce9d5b477641c560b6b07e8ee8d57b195429d320e9d7d1e`).
  - Every number below was read from the text extracted from the PDF (`pdftotext -layout`), not from a summariser.
  - Nothing else was downloaded.
- **Earlier lanes never read the PDF.** CFG190, CFG198 and CFG236 read III only through abstract-level or summariser notes (CFG236 frozen criteria, item 6). This lane is the first direct reading of the PDF text.

## 2. Version check against the record's inputs: nothing material changed

| Item | Record (CFG190 / CFG198 / CFG236) | Published text (v1 = accepted) | Material? |
|---|---|---|---|
| a₀ at z∼1, one-parameter fit on the full sample | 2.38 ± 0.1 (×10⁻¹⁰) | 2.38 +0.12/−0.10, **95% CI** (Eq. 2) | no (asymmetry only) |
| Linear law a₀(0) + a₁z | a₀(0) = 1.0 ± 0.04; a₁ = 1.59 ± 0.10 | Eq. 4: 1.0 ± 0.04 and 1.59 ± 0.10, 95% CI. The abstract, Sect. 4 and the Conclusions print a₁ = 1.59 +0.11/−0.10 | no (an internal ±0.01 inconsistency in the paper) |
| Error convention | 95% CI (verified in the CFG190 addendum) | 95% CI for Eqs. 2, 4, D.1, D.2, E.4, E.5; per-point velocity errors are 1σ (16–84%, App. B) | no |
| "z ≈ 0.87" | CFG190 evaluates the law at z = 0.87 | The paper says only "z∼1"; 0.87 appears nowhere in the text | wording only: 1.0 + 1.59 × 0.87 = 2.38, so the record's "a₀(0.87)/a₀(0) = 2.38" is a ratio to the paper's own fitted a₀(0) = 1.0. Against SPARC's 1.2 it is 1.98 |
| Sample | III's 79 galaxies (not identifiable in the files); the release has 126 (127 ids); CFG236 E4 used III-like cuts (n = 76) | 79 star-forming galaxies, M★ > 10^8.8, 0.33 < z < 1.44, "regular", log Z < 15000, i > 30°, v/σ > 1 (App. A) | no. The "regular" flag and the log Z cut are still not in the released files, so the 79 still cannot be rebuilt |
| Mass method | M★ fitted inside the GalPaK3D DC14 disc–halo model; HI = constant surface density; Dalcanton–Stilp pressure support | Same (App. B). M★ "is not fixed by photometric priors", but is fitted jointly with log(M★/M_halo) and V_vir. **No H₂ term in a_bar** | no |
| Radial cut | -- | r < 2 kpc excluded; the paper says this changes a₀ by < 10% | new detail, not used by the record (CFG198/236 work at R_e) |
| Binned a₀ | -- | four equal-count z bins: 1.99 → 2.71 (×10⁻¹⁰); intrinsic scatter 0.13 → 0.19 dex | new to the record, consistent with it |
| Systematics sections | not read directly | App. C (disc-mass systematics), D (best halo per galaxy), E (MOND refits), F (corner plot) | read here for the first time (section 3); no new data product |
| Data release | `dark-matter.osu-lyon.fr/data/catalogues/` + per-galaxy DC14 runs (manifest sha256 in `data_assembly/musedark_catalogues/`) | The paper points to `dark.univ-lyon1.fr/data-releases/` | same collaboration site under another hostname; release identity **not verified** (no fetch made; the on-disk files carry no version stamp) |

- **Paper I is now published** as A&A 708, A112 (2026). The record cited it as arXiv:2506.19721.
- **Verdict on the version:** the published text is the version the record used; it adds no new table or per-galaxy product.
  - So the CFG198/199/236 pipeline was **not re-run** (task rule: stop after the crux reading).
  - The record's numbers (drift −0.72 dex/z; route (ii) −0.04 [−0.45, +0.35]) stand as committed (405713e57).

## 3. The crux: why trust the halo-fit masses over the stellar-population masses?

### 3a. How the paper derives its baryons (App. B)

- **Stars:** v_disk takes its shape from a Multi-Gaussian Expansion of the ionised-gas surface brightness; its normalisation is M★, which is a free parameter of the DC14 fit, constrained by the kinematics.
- **HI:** a parametric profile with constant Σ_HI. No direct HI data.
- **Bulge:** a Hernquist bulge, only for the 4 galaxies with B/T > 0.2.
- **H₂:** not in a_bar at all.
- **Pressure support:** a_tot comes from v_c² = v_⊥² + v_AD².
- **Both accelerations come from one model.** The paper itself says a_tot and a_bar "are derived from the same underlying model rather than independently" (App. C).

### 3b. The paper's own robustness checks, and what each shows

1. **Halo profile (App. D).** With the best halo per galaxy, a₀|z∼1 = 2.61 +0.13/−0.09, a₀(0) = 1.05 ± 0.05, a₁ = 1.63 +0.13/−0.12. The rise survives, but every variant still fits M★ dynamically inside a halo model.
2. **MOND refits (App. E):**
   - per-galaxy free a₀: median 2.27, spread 1.3×10⁻¹¹ to 9.6×10⁻¹⁰;
   - RAR from the MOND fits: a₀|z∼1 = 2.19 +0.12/−0.10, a₀(0) = 1.03 ± 0.05, a₁ = 1.20 ± 0.10;
   - direct regression of per-galaxy a₀ on z: a₁ = 1.42 +0.94/−0.89. The interval type is not stated; it is the weakest of the paper's z-trend numbers.
   - **Key for the crux:** with a₀ fixed at 1.2 the MOND fits are worse, AND their M★ comes out about 0.28 dex above the DC14 masses, and also above the SED masses. So in the paper's own MOND test, flat a₀ costs heavier discs, not a failed fit.
3. **Disc-mass systematics (App. C):**
   - The paper says the dynamical M★ agree with SED masses (Paper I Fig. 11), "showing that the potential systematic uncertainties in M⋆ are negligible".
   - Its K-band M/L ratios are lower than SPARC's 0.6 and consistent with Drory+04 at these redshifts.
   - **The reconciling shift is z-dependent.** Bringing every bin to a₀ = 1.2 needs M★ offsets of about +0.2 dex in the lowest-z bins rising to about +0.45 dex in the highest (Fig. C.1). The paper calls these unsupported by its consistency checks.
   - **Unmodelled H₂ is of the same size.** The paper states that typical molecular gas fractions of about 30–50% at z ∼ 1 (Freundlich+19) imply a systematic of about 0.2 dex in the total disc mass. This is not propagated into a₀(z).

### 3c. The record's best answer

1. **The halo-fit masses carry a ΛCDM halo-model prior.** M★ is fitted jointly with a DC14 halo, whose inner shape is tied to M★/M_halo by ΛCDM hydrodynamical simulations.
   - The owner's standing rule is to use framework-native inputs, not ΛCDM-laden ones.
   - The paper's MOND refit is the framework-native check, and in it flat a₀ is bought with heavier discs (+0.28 dex).
2. **"Good agreement with SED" is a statement about the level, not the z-trend.**
   - On the released tables the fitted-minus-SED mass difference has median −0.11 dex but slope **−0.72 [−0.97, −0.50] dex/z** (CFG198, reproduced by CFG236).
   - About 60% of that slope survives at fixed SED mass: −0.43 [−0.72, −0.15] dex/z. Over the bins' z range that is roughly the size of the paper's own reconciling shift (+0.2 → +0.45 dex), and it has the same sign: the fitted masses fall below SED at high z.
   - So the paper's "negligible" is not shown for the quantity that drives a₀(z).
3. **The SED route is not clean either.** CFG236 found that SED M★ + H₂ (H₂ from a scaling relation) exceeds the model's own dynamical mass within R_e in about 30% (low z) and 52% (high z) of galaxies. The excess comes mostly from the H₂ term, so the SED route over-predicts the dynamics in about half the high-z galaxies.
   - On that route the slope is −0.04 [−0.45, +0.35]: flat, E(z) and III's law are all inside, so it is **non-diagnostic**.
4. **So which mass is right is unsettled.** The defensible wording (CFG236) is unchanged: "MUSE-DARK III's a₀ rise is not recovered on SED M★ + H₂; the data on disk cannot say whether the fitted masses or the SED route are biased."

### 3d. The one measurement that would settle it

- **What is needed:** a per-galaxy, z-binned molecular-gas measurement (CO, or dust-continuum gas) for III's galaxies, above all the highest-z bin, where the reconciling offset is +0.45 dex.
  - H₂ is the term III leaves out and the term that drives the SED route's over-prediction.
  - It would directly decide whether the missing +0.2 → +0.45 dex is cold gas, rising with z, or absent.
- **What is public (from memory, not verified in this lane):**
  - ASPECS covers the HUDF with ALMA, and MUSE-selected stacks exist (Inami+2020).
  - But ALMA band 3 sees CO(2–1) only at z ≈ 1.0–1.7 and CO(1–0) only at z < 0.37. Only the top bin is covered, mostly as stacks or limits for galaxies below 10^10 M★.
  - **The z ≈ 0.4–1.0 bins have no public CO** for galaxies of this mass. That needs new ALMA band 4/5 time.
- **The second-best measurement:** the resolved SED stellar-mass maps (MGE fits of pixel-by-pixel SED fits, Paper I) for each of the 79 galaxies, with the 79 identified. They are not in the on-disk release, and III shows them only as curves for two galaxies (Fig. B.1).
- The record's gas-calibration lesson applies (CFG238): a single-tracer gas prescription is 0.2–0.7 dex uncertain at high z, so only multi-tracer gas at matched luminosity would reach the ~0.1 dex level needed.

## 4. Verdict for the record: UNCHANGED

- The published A&A L16 text equals the arXiv v1 the record used: same numbers, same 95% CI convention, same sample definition, same DC14 dynamical-mass method, no H₂ in a_bar, and no new per-galaxy product.
- III's rise is still not recovered on SED M★ + H₂. Which mass is right is still unsettled. MUSE-DARK II's null bTFR evolution (0.00 ± 0.06 dex) still conflicts with III's law within the same collaboration (CFG190).
- **The kill rule** (a ROBUST a₀ rise kills flat a₀(z), the framework's distinctive law) **is NOT triggered.** The rise is method-dependent: it lives in the halo-fit masses, and the paper's own MOND test shows flat a₀ is bought with +0.28 dex heavier discs.
- **Nothing here favours flat a₀ either.** No detection either way. κ = ½ is fitted.
- **New to the record (minor):**
  - (i) "a₀(0.87)/a₀(0) = 2.38" is a ratio to III's own fitted a₀(0) = 1.0. The paper's 2.38 is an absolute a₀ at "z∼1" (against SPARC's 1.2 it is ×1.98).
  - (ii) III's own App. C gives a z-dependent reconciling mass shift (+0.2 → +0.45 dex) and an unpropagated ~0.2 dex H₂ systematic of the same order.
  - (iii) In III's MOND refit, fixed a₀ = 1.2 gives M★ +0.28 dex above DC14.

## Addendum: the A&A typeset version (2026-10-06)
The owner supplied the published A&A PDF (A&A 709, L16; it is not stored in the repo). A full-text numeric diff against arXiv:2604.22613v1 finds only typesetting differences: the DOI and arXiv identifiers, licence text, one error bar printed +0.11 in the abstract, and 0.2 vs 0.200 formatting. Every headline number matches: 2.38, a1 = 1.59, the 79 galaxies, 0.33 < z < 1.44, 2.61, 2.19, +0.28 dex, the +0.45 dex reconciling shift, and the "negligible" M* systematics sentence. The verdict above is unchanged.
