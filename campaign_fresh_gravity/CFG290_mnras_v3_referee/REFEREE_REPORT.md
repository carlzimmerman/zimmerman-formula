# CFG290 — hostile referee report on the MNRAS v3 manuscript

**Manuscript:** "The galactic acceleration scale and the cosmological constant: the coefficient measured, its degeneracy with H0, and a redshift test" (`qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/`, commit 32f9a609c).
**Referee lane:** CFG290, 2026-10-02. Read-only on the manuscript. κ = ½ is FITTED; the cold mass is still required.
**Evidence:** `cfg290_referee_checks.py` (+ `.out`, `_results.json`), `cfg290_reference_check.py` (+ `.out`), `cfg290_abstract_reads.py` (+ `.out`), `number_trace.csv`, and a full re-run of `reproduce_all.sh` in an isolated mirror (see `README.md`).

## Recommendation: MAJOR REVISION

The numbers are reproducible. `reproduce_all.sh` passes all steps from a clean export, and `paper_numbers.out` comes out byte-identical. Of 73 quoted values traced to a source, 66 match, 3 match only partly and 3 do not. The paper is also unusually careful about what it does not claim: κ is not derived, no existing sample decides, the cold mass is still required, and nothing says the data favour the framework.

It is not publishable as it stands, for four reasons.
1. **The design overstates its odds.** The headline design (two to four lensed rotators reaching 20:1) uses the ΛCDM rise for 10¹² M☉ haloes. The gate it proposes selects discs in haloes of 3×10¹⁰ to 2×10¹¹ M☉. There the paper's own concentration–mass relation predicts +0.18 to +0.26 dex, and the quoted designs reach only about 5:1.
2. **"Odds" means expected log-odds.** The chance of actually reaching 20:1 is 0.59–0.77 at the recommended designs.
3. **The headline κ uses mixed H₀ conventions.** The Hubble-flow distances are on H₀ = 73 and ρ_Λ is on 67.4, and the paper does not disclose this. The repository's own audit calls a different value operative. This sits badly with Section 4, whose message is that κ cannot be quoted without H₀.
4. **The novelty is overstated and key literature is missing.** Limbach, Psaltis & Özel (2008) already confronted the ρ_Λ- and H₀-coupled laws with Tully–Fisher data to z = 1.2. Desmond (2023)'s headline a₀ puts κ = ½ at 2.6σ on the paper's preferred footing but is cited only for a scatter value.

Much of Section 5.3 rests on the author's own repository re-analyses, which the manuscript does not describe. A focused paper on what it takes to measure a₀(z) would be publishable: the amplification analysis, the gate, the shared-calibration result and the conditioning bound. **The desk-rejection risk in the current form is moderate.** Reasons: the topic sits near numerology, there is heavy reliance on self-deposited Zenodo notes and internal lane IDs, and one of the three headline questions (Section 4) is a one-line identity.

**Counts by severity:** 1 CRITICAL, 10 MAJOR, 20 MINOR, 8 NIT.

---

## Findings

### CRITICAL

**1. [CRITICAL] The ΛCDM decision value (+0.33 dex) is for 10¹² M☉ haloes, but the gate selects discs in haloes of 3×10¹⁰ to 2×10¹¹ M☉, where the paper's own relation gives +0.18 to +0.26 dex. The abstract's "two to four rotators decide at 20:1" then fails by about a factor of 5 in odds.**

*Where:*
- Abstract (l.32);
- Section 5.1(c) (l.450: "We adopt +0.33 as the decision value because it is near the low end");
- Section 5.4 (l.559–575), Tables 9 and 10;
- Conclusion (viii) (l.648);
- Fig. 4.

*The problem:*
- The gate examples have M_b = 2×10⁹ to 10¹⁰ M☉ and V_f ≃ 85–130 km/s (paper_numbers S4).
- At z = 2.5 that means M₂₀₀ = V₂₀₀³/(10 G H(z)) ≈ 3×10¹⁰ to 2×10¹¹ M☉, for V_f/V₂₀₀ = 1–1.2.
- With Dutton & Macciò (2014), the paper's primary relation, Δ_halo there is +0.18 to +0.26 dex (`cfg290_referee_checks.out` R8). At 10¹¹ M☉ it is +0.227.

*What happens to the odds at Δ = 0.227* (same intrinsic and halo scatter, closed form verified by Monte Carlo):

| design | odds at Δ = 0.33 | odds at Δ = 0.227 |
|---|---|---|
| two galaxies at 0.10 dex | 24.6:1 | 5.1:1 |
| three galaxies at 0.13 dex | 53:1 | 7.3:1 |
| four galaxies at 0.20 dex | 29:1 | 5.2:1 |

About eight galaxies at 0.20 dex are needed for ~27:1 (R3).

*A second, unpropagated uncertainty:* with Duffy et al. (2008) the same haloes give +0.43. The choice of concentration–mass relation moves the decision value by ~0.2 dex, comparable to σ_m, and the odds do not carry it. The g_max-at-fixed-M₂₀₀ proxy is itself a heuristic, not a ΛCDM prediction for the statistic the decision rule uses.

*Fix:*
- Evaluate Δ_halo at the halo mass implied by the gate, via abundance matching or V_f → V₂₀₀.
- Treat the concentration–mass relation and the proxy as a model systematic, i.e. a composite hypothesis with a prior on Δ.
- Redo Tables 9–10, the abstract's N and Conclusion (viii).
- Preferably, calibrate the ΛCDM side on simulated low-mass discs inverted at y < 0.3 in the same way (cf. Mayer et al. 2023).

### MAJOR

**2. [MAJOR] "Odds of 20:1" is exp⟨ln B⟩, not the probability of reaching 20:1.**

*Where:* eq. (σ) l.565–567, eq. (lnB) l.571–575, Table 9, Table 10, abstract, Conclusion (viii).

*What the numbers are* (Monte Carlo, R3):

| design | P(reach 20:1), constancy true / halo true | P(evidence points the wrong way) |
|---|---|---|
| idealised rule σ = Δ/2.45 | 0.50 | 0.11 |
| N = 2 at 0.10 dex | 0.60 / 0.72 | 0.06–0.09 |
| N = 3 at 0.13 dex | 0.70 / 0.77 | 0.05–0.07 |
| N = 4 at 0.20 dex | 0.59 / 0.66 | 0.07–0.09 |
| N = 4 at 0.20 dex, δ_c = 0.10 (Table 10) | 0.16 / 0.23 | — |

*Fix:* Call the quantity "expected log-odds". Report the power, P(ln B > ln 20 | each hypothesis), and the probability of misleading evidence. Size N for, say, 90% power.

**3. [MAJOR] The headline κ values rest on a mixed, undisclosed H₀ convention.**

*Where:* abstract; Table 2; eq. (kappaA); Section 3.5 l.297; Table 6; Fig. 2(b); Section 4 l.410; Section 6 l.631.

*The problem:*
- SPARC's 97 Hubble-flow distances (f_D = 1, counted in R7) assume H₀ = 73 (SPARC MRT note 2). ρ_Λ is built from H₀ = 67.4.
- The repository's own audit, `kappa_h0_convention_audit_2026.py` (run by `reproduce_all.sh` step 3; check C4), designates the Planck-consistent R1 convention as OPERATIVE. The values on each convention:

| quantity | as tabulated (mixed) | R1 (Planck-consistent) | R2a / R2b |
|---|---|---|---|
| κ_A (estimator A) | 0.465 ± 0.076 | 0.450 ± 0.074 | 0.430 / 0.416 |
| κ_B (paper's estimator B, re-implemented, R9) | 0.547 | 0.584 | — |
| standard fit at Υ_disc = 0.5 | 0.636 | 0.560 | — |
| Υ_disc needed for κ = ½ | 0.621 | 0.555 | — |

The mixed value of κ_A is the maximum of the 2×2 box.

*Why it matters:*
- The paper never states the H₀ = 73 convention, although its own Section 4 says such a claim "should say so".
- The Fig. 2(b) grey bars are hard-coded in `make_figures.py` and asymmetric. A's bar shows only [0.450, 0.465] and omits R2 (0.416–0.430, away from ½). B's bar shows the full [0.492, 0.589], including R2b's move toward ½.
- Section 4's inversion "estimator A gives H₀ = 63 ± 10" uses data whose Hubble-flow distances already assume 73.

*Fix:* State the convention. Make the Planck-consistent values primary, or show both, throughout. Compute the convention box in `paper_numbers.py` for both estimators. Redo the Section 4 inversion self-consistently.

**4. [MAJOR] Limbach, Psaltis & Özel (2008) is presented as having only proposed the test, but they performed it.**

*Where:* Introduction l.59; Section 5.3 l.547.

*The problem:*
- Their arXiv abstract: they confronted the cH₀- and ρ_Λ-coupled a₀(z) laws with two Tully–Fisher data sets to z = 1.2. Both couplings were excluded at the formal errors. With systematics they marginally favoured the dark-energy coupling. This is the paper's question (iii), on the same Λ coupling, already answered once at z ≤ 1.2.
- Milgrom (2017) says the Genzel et al. discs all but exclude ≈4a₀ at z ≈ 2. Law (b) gives ×3.0 at z = 2, so the paper should say whether law (b) is already disfavoured.

*Fix:* Rewrite the novelty statement around what is actually new: the amplification analysis, the deep gate, the shared-calibration result, the Fisher floor and the ΛCDM comparator. Discuss the 2008 result and why it is not decisive.

**5. [MAJOR] The κ discussion cites selectively.**

*Where:* Section 3.8, Table 6, abstract.

*What is left out:*
- **Desmond (2023)** is cited only for σ_int = 0.034 dex. Its headline result is a₀ = (1.19 ± 0.04 ± 0.09)×10⁻¹⁰, from a full joint inference over distance, inclination, luminosity and M/L. That is κ_Λ = 0.636 ± 0.053:
  - κ = ½ at 2.6σ;
  - 0.461 at 3.3σ;
  - ½ on the ρ_crit footing at 0.6σ;
  - cH₀/2π at 1.5σ (R8).
- **The paper's own third route** (the profile likelihood, κ_Λ = 0.575, ½ at 1.8σ clustered) is in the text but missing from Table 6, Fig. 2(b) and the abstract's "consistent with both".
- **Vărăşteanu et al. (2026)** measure a₀ = (1.50 ± 0.05)×10⁻¹⁰ (κ_Λ ≈ 0.80) from 130 galaxies. This is not discussed in the κ section.
- **Missing papers:** Li et al. 2018 (A&A 615, A3); Rodrigues et al. 2018 (Nature Astronomy 2, 668) and the replies; Marra et al. 2020.

*Fix:* Add a table of published SPARC a₀ values converted to κ on both footings, with each paper's Υ prior. Table 2 already shows that the Υ prior centre sets κ. Add the profile likelihood as a third row of Table 6, and qualify the abstract sentence.

**6. [MAJOR] The formal RC100 significances against the rivals conflict with the record's standing rule.**

*Where:* Section 5.3, l.535: "the halo law is disfavoured at 2.5σ to 4.3σ and the H(z) law at 4.6σ or more". The main treatment is 5.4σ against H(z).

*The rule:* The adopted status record (STANDING §4, CFG217) classifies RC100 as gas-route-limited, "not to be quoted as a ~5σ result". The memory rule is "RC100 decides nothing; never quote 5σ".

*What is missing:* The paper says β = −0.05 dex/z brings the halo law within 2σ. It does not say that β = −0.10 brings H(z) to 1.0σ (tilt table: +0.160 ± 0.069 against 0.230).

*Fix:* Drop the σ values against the rivals, or put them in a table explicitly labelled "formal, conditional on RC100's mass models". Give the drift that erases each exclusion: halo −0.05, H(z) −0.10 dex per unit z.

**7. [MAJOR] The RC100 disclosures are incomplete. This bears on the owner's question "are we sure RC100 did it right?"; see the RC100 section below.**

*Where:* Section 5.3, l.524–537; Data Availability.

*Three omissions:*
- **(a) f_DM tracks RC100's baryonic-mass prior.** On the corrected table, CFG217 G2 finds Spearman ρ = +0.33, p = 0.036, n = 41. RC100's gas comes from the Tacconi+2020 scaling relations. So "No mass model enters beyond the published f_DM" (l.529) is misleading: f_DM is the authors' mass-model output.
- **(b) RC100's own internal flags are not mentioned.**
  - Rows 67 (zC 405501) and 83 (K20 ID5) have V_c² < 3.36σ₀², so V_rot(R_e)² < 0 by their eq. 8.
  - Fourteen more rows fall below their V_rot/σ₀ = 2.3 cut at R_e.
  - Re-derived from the table in R2; this matches CFG287/CFG289.
  - Dropping the flagged rows moves the slope from −0.111 ± 0.063 to −0.089 ± 0.061 (without the 2 eq.-8 rows) or −0.095 ± 0.062 (without all 16). That is 0.3σ: robust, but it must be stated.
- **(c) The table is the arXiv v1 copy**, not the published ApJ table. v1 is the only arXiv version of 2209.12199, and CFG287 records the copy as marked "Submitted to ApJ". Neither 2209.12199v1 nor ApJ 944, 78 is named as such in the text.

*Fix:* Add one sentence on each of (a)–(c). Replace l.529's sentence with "the inversion adds no mass model to the authors' own".

**8. [MAJOR] Key results rest on the author's own repository re-analyses, which the manuscript does not describe.**

*Where:* Section 5.3, l.539–549; Section 5.4, l.598; Appendix B.

*The problem:*
- These results are reported without methods:
  - the MUSE-DARK per-galaxy re-analysis (asymmetric-drift term, gas, how the thirds were chosen, how errors were computed; N is not even given — 109 in the lane, 79 in Ciocan);
  - KURVS with the Kretschmer correction and a "decision cell";
  - the MIGHTEE mocks;
  - the z ≥ 4 pools, whose statistic "P" is never defined.
- The gas-prescription bracket "0.2–0.7 dex at z ≈ 2.2" is load-bearing in the abstract's conclusion. It is sourced to the author's own Zenodo note (Zimmerman2026wall); the underlying comparison is ACE against Stripe82.
- `paper_numbers.py` only checks that the text quotes those committed outputs (identity checks).
- The lane quoted for z ≥ 4 (CFG269) fails its own frozen control C1 in its committed output (max |dev| 1.9×10⁻³ against a 10⁻⁴ tolerance).

*Fix:* Add a methods appendix for each re-analysis, or reduce each to a sentence citing only published results. Source the gas bracket to primary literature (the ACE and Stripe82 dust-to-CO papers; Tacconi et al. 2018/2020; an α_CO review such as Bolatto et al. 2013). Fix or disclose CFG269's C1.

**9. [MAJOR] A cited Zenodo record carries a known, uncorrected error.** *(Owner's call.)*

*The facts:*
- Zimmerman2026kappa (DOI 10.5281/zenodo.22559892) is still v1 (2026-09-06). Concept record 22559891 has no later version (checked against the Zenodo API).
- Its four-form section's "stable (F6)" verdict was shown wrong in the repository on 2026-09-27: XR31, `kappa_closure/k04_F6_CORRECTION_2026-09-27.md`. It is on the DO-NOT-CITE list.
- The manuscript cites the record twice: for the old estimator-B error bar and for the zero-mode degeneracy in Section 6. The cover letter declares it as an earlier posting.

*Fix:* Before submission, deposit a v2 or erratum, or add "its four-form section is superseded", or drop the citation.

**10. [MAJOR, verify] The AI-use disclosure may be incomplete.**

*The facts:*
- The Acknowledgements and the cover letter name Claude (via Claude Code) and unspecified "models from OpenAI".
- Inputs the paper uses sit in repository tracks named after other models:
  - the digitised MIGHTEE-HI points, `deepseek_push/data2/` (commit message prefixed "deepseek:");
  - the per-galaxy M/L corpus of the pitfall paragraph, `glm53_push/data/`.
- The paper's own directory is `qwen_claude_field_theory/`.

*Fix:* If DeepSeek, GLM or Qwen models produced any of these inputs, code or text, name them, and name the OpenAI model(s). If these are only lane labels, nothing changes, but the question should be expected.

**11. [MAJOR] The scope dilutes the paper's real contribution.**

*What is thin:*
- Section 4 is a one-line identity: a₀ ∝ κH₀ at fixed Ω_Λ. Its only other content is a numerical coincidence that the paper itself disowns.
- Sections 2.2–2.3 (the dimensional analysis, four rewritings and Z) are textbook.
- The κ "measurement" re-derives the known M/L degeneracy of the SPARC a₀ (McGaugh+16's ±0.24 systematic; Desmond 2023). Its new element is the 9.5% floor.

*What is valuable but buried:* the amplification analysis (Table 8, Fig. 5), the gate, the shared-calibration result and Fisher bound (Table 10, l.598–618), and a critical census of high-z samples.

*Fix:* Restructure. Lead with the a₀(z) measurement problem; compress κ into one section and Section 4 into a paragraph. This also lowers the desk-rejection risk.

### MINOR

**12. [MINOR] The abstract is exactly 250 words by a plain count** (262 if each math span counts as a word; R1). ScholarOne may count differently. Trim about 20 words.

**13. [MINOR] Wrong DOI for KlinkhamerKopp2011.** 10.1142/S0217732311037042 resolves to Bernal, Capozziello, Cristofano & De Laurentis, MPLA 26, 2677. The correct DOI is 10.1142/S021773231103711X (pp. 2783–2791), from a Crossref search. The other 48 entries match Crossref, arXiv or Zenodo (`cfg290_reference_check.out`).

**14. [MINOR] The comparator slopes are mislabelled.**

*Where:* l.533, "the mean slopes of laws (b) and (c) over this range are +0.23 and +0.13".

These are means from z = 0 to 2.5. Fitted by the same OLS at RC100's own redshifts they are +0.225 and +0.153 (R2). The paper's label is conservative for the halo law: the exclusion would be 4.2σ, not 3.9σ, in the main treatment.

*Fix:* Use the matched comparator, or relabel the numbers.

**15. [MINOR] "Three decades" should be "four".**

*Where:* l.618, "it would need three decades in y".

The paper's own Fisher numbers need y from 0.001 to 17 (4.2 decades) or from 0.01 to about 275 (4.4 decades).

**16. [MINOR] The MUSE-DARK wording in the abstract and Conclusion (vii) overstates the contrast.**

*Current wording:* the rise "appears only with dynamically fitted stellar masses … and not with SED masses (−0.11 ± 0.49 and +0.04 ± 0.14)".

Route (ii) is uninformative: −0.11 ± 0.49 is consistent with route (i)'s +0.57 at 1.4σ.

*Fix:* Use STANDING's defensible wording: "not recovered with SED stellar masses plus molecular gas; the data cannot say which masses are biased".

**17. [MINOR] Ciocan's rise is quoted against a different calibration.**

*Where:* l.539, "Δ ≃ +0.3 relative to the local 1.2×10⁻¹⁰".

In their own fit a₀(0) ≈ 1.0, which gives Δ ≈ +0.38. Comparing against SPARC's 1.2 mixes calibrations, which the decision rule itself forbids, and it understates an against-interest result.

*Fix:* Quote both values.

**18. [MINOR] The MIGHTEE-HI/LADUMA mock statements need a label, and two of the authors' own results are missing.**

*Where:* l.543.

- The 5.2× ratio and the 11–32% come from post hoc runs of a declared scenario with unverified inputs (CFG258 README), not from mock samples "of the same design". Label them as post hoc mock results.
- Mention two results stated in the abstracts:
  - Vărăşteanu et al. (2026)'s own bTFR zero-point trend (8.7σ in the forward fit, 3.4σ in the inverse fit, attributed to selection);
  - Vărăşteanu et al. (2025)'s "tentative" a₀ evolution.

**19. [MINOR] KURVS is called "the one in-regime reading whose central value favours the rival".** The record's CFG165 notes that P3 also leans toward the rival, in 12 of 24 cells.

*Fix:* Say "under the simulation-calibrated correction the rival's central value sits at zero".

**20. [MINOR] The combined likelihood ratio treats the estimators as independent.**

*Where:* l.359, ln LR = −0.02 "from the two together".

This sums two likelihoods, right after the text says the estimators share galaxies and are not averaged. Separately: A gives −0.10 and B gives +0.09 (R6).

*Fix:* Report each separately.

**21. [MINOR] Several check labels are wrong.**

*Where:* Appendix B and `paper_numbers.py`.

- I4 is a sensitivity test (no synthetic data) but is labelled "injection".
- These checks cannot fail on data but are labelled "data":
  - S2e (a code replication);
  - S5f (a string match on a committed JSON);
  - S7b, S7d, S7f, S7h, S7l (arithmetic on committed numbers).
- So about 23 checks, not 30, can fail on data, and five, not six, are injections.

*Fix:* Relabel.

**22. [MINOR] Fig. 4's ±0.13 dex bars show the idealised one-object rule that Section 5.4 rejects** (one object at 0.13 dex gives 4:1).

*Fix:* Show the sample-mean or δ_c-limited error of the recommended design, or label the bars "idealised".

**23. [MINOR] The Fig. 2(b) grey bars are hard-coded** in `make_figures.py`, and B's bar comes from the old B variant. Compute both bars in `paper_numbers.py` (see finding 3).

**24. [MINOR] The H₀ range "0.49–0.59" quoted for estimator B belongs to the old variant** (Υ_bul fixed at 0.7, central value 0.551; h0 audit D6). The quoted estimator (0.547) gives 0.584 under R1 (R9). Recompute.

**25. [MINOR] The MIGHTEE-HI galaxies are identified by marker colour, which is not a clean identifier.**

There are 18 colour groups for 19 galaxies. The largest group has 11 points spanning only 0.22 dex in g_bar, which looks like two galaxies merged (R7).

*Fix:* State this, and give the per-galaxy slope result without that group.

**26. [MINOR] The gate formula uses an unstated a₀.** "M_b < 1.8×10⁸ (R/kpc)²" is computed with a₀ = 1.0×10⁻¹⁰ (paper_numbers l.430). With 9.36×10⁻¹¹ it is 1.68×10⁸. State which.

**27. [MINOR] Data Availability needs a frozen snapshot and two more arXiv-v1 caveats.**

- The repository is very large and mutable. Cite a frozen snapshot of the reproduction package (a Zenodo DOI, or a commit hash or tag).
- Like RC100, FS+18 and Umehata+25, which feed the z ≥ 2.5 census, were checked against arXiv v1 only (CFG287).

**28. [MINOR] Two paragraphs report errors in the author's own intermediate files.**

- The RC100 transcription paragraph (l.524): one sentence in Data Availability is enough.
- The pitfall paragraph (l.332): state the point generally (fitted M/L ratios absorb the discrepancy) without "a compilation assembled earlier in this project".

**29. [MINOR] The Mayer+2023 redshift may be wrong.** Their abstract gives the factor-of-about-3 rise from z = 0 to z = 2, not 2.3. Check the body and adjust "+0.48 dex … 2.3".

**30. [MINOR] Make the "author has run every script" claim literally true.** The Acknowledgements say "a script that the author has run"; the cover letter says "I ran every script myself". The owner should run `reproduce_all.sh` personally before submitting (about one minute), or the wording should change.

**31. [MINOR] Soften the claim about ΛCDM and constancy.**

*Where:* l.633, constancy "would require ΛCDM to produce an acceleration scale that stays fixed while the haloes that set it evolve".

The inferred scale for galaxies at fixed baryonic mass need not follow g_max of a fixed-mass halo.

### NIT

**32. [NIT]** Sections 2.2–2.3 can be compressed to one paragraph. Z is κ restated, as the paper itself warns; drop it.

**33. [NIT]** The DOI types are inconsistent across the three Zenodo self-citations. a0z uses the concept DOI 22563138, which resolves to v3 (22833314) with a longer title; kappa and wall use version DOIs. Cite the versions actually used.

**34. [NIT]** Some figure text is small and hard to read:
- text at 5.6–6.4 pt at MNRAS column width (Fig. 2(b) labels, the Fig. 3(a) legend, Fig. 3(b)'s "estimator A");
- the rotated "½" in Fig. 2(b);
- Υ renders like "Y" in DejaVu Serif.

**35. [NIT]** Figure file names are out of order (fig_deep is Fig. 3, fig3_laws is Fig. 4). The acceptance bundle renames them; keep it that way.

**36. [NIT]** The PDF has no Title or Author metadata (add hyperref pdfinfo).

**37. [NIT]** In the abstract, "match the prediction" should read "match the slope of the fitted relation".

**38. [NIT]** `reproduce_all.sh` rewrites tracked files in place: `paper_numbers.out`/`.json`, the figures, the PDF, and `real_research/dark_sector_2026/L332_kmos3d_trend_replication_results.json`, which is outside the paper directory. Say so in Appendix B, or write to `reproduce_outputs/`.

**39. [NIT]** l.545, "the one or two at z = 8–14": the complete bin has two objects.

---

## RC100: are we sure RC100 did it right?

**What can be checked here:**
- **The input table.** The corrected transcription matches RC100's arXiv v1 Table 3. Check S5h passed: sha256, exactly 17 changed cells, 3 of them entering the inversion. The published ApJ table was not compared; it was not readable.
- **RC100's own consistency.**
  - Two rows violate their own eq. 8 at R_e (rows 67 and 83). Fourteen more fail their V_rot/σ₀ = 2.3 cut at R_e. These were re-derived from the table here and match CFG287.
  - f_DM tracks their baryonic-mass prior (ρ = +0.33, p = 0.036). Gas comes from scaling relations.
  - **So RC100's f_DM and M_bar are model outputs, not measurements, and some rows are internally inconsistent.** Whether RC100 "did it right" cannot be established from the table.
- **The paper's use of RC100.**
  - It is robust to those defects: dropping the flagged rows moves the slope by 0.3σ.
  - The transcription fix moves it by less than 0.001 dex per unit z.
  - The paper calls the result "not a measurement" and lets a 0.05 dex per unit z drift erase it.

**Against the owner's checklist:**

| item | status |
|---|---|
| (i) never leans on RC100 as support | mostly met; fails on the l.535 σ sentence (finding 6) |
| (ii) says f_DM and M_bar are the authors' model outputs | partly met: gas from scaling relations and the halo priors are stated; the tracking of the mass prior is not (finding 7a) |
| (iii) mentions the internal flags | not met (finding 7b) |
| (iv) says arXiv v1, not the journal version | partly met: "the arXiv version" plus the Data Availability caveat; it should say v1 explicitly (finding 7c) |

## Banned phrasings and the status record

- **No violations found of:**
  - "the data favour the framework";
  - κ derived ("The coefficient is not derived", Section 6);
  - dark matter absent (Section 6 states that the cold matter is still required);
  - Z ≈ 21 (Z = 5.79, with the tautology warning);
  - "theory closed";
  - the Unruh route for κ = ½ (it gives cH_Λ and is excluded);
  - any other DO-NOT-CITE number checked.
- **Two items touch the record:**
  - the RC100 "4.6σ or more" (finding 6);
  - the citation of PAPER6 v1 (finding 9).
- **Consistent with STANDING_2026-09-29:**
  - κ = ½ fitted;
  - like for like on H₀, ½ and 1/2π indistinguishable;
  - MUSE-DARK route-dependent (wording, finding 16);
  - KURVS a lean, not a detection;
  - MIGHTEE-HI/LADUMA unable to separate the laws;
  - no z ≳ 2.5 sample measures a₀;
  - a calibration of ≈0.1 dex needed.

## MNRAS compliance

| item | status |
|---|---|
| abstract ≤ 250 words | at the limit (250 plain); trim (12) |
| ≤ 6 keywords from the MNRAS list | 6, all on the list |
| AI disclosure in Acknowledgements and cover letter, software named | present; Claude Code named, OpenAI models unnamed; possibly incomplete (10) |
| Data Availability statement | present; add a frozen snapshot DOI (27) |
| figure alt text | present for all six figures (`make_upload_bundle.py` → bundle file 04); consistent with the figures |
| single PDF ≤ 10 MB | 0.40 MB, 14 pages |
| no e-mail or home paths in tracked files | clean: `git grep` at 32f9a609c and a byte scan of the PDF and figures; the e-mail appears only in the git-ignored bundle |
| references complete, with DOIs | 49 entries; every journal entry has a DOI; one DOI is wrong (13); 5 preprints have no journal version (arXiv API) |
| cover-letter tone | formal; does not summarise results; declares AI use, conflicts and postings; lists the PAPER6 DOI (9) |

## Figures

- **Fig. 1:** correct. The curves differ by at most 0.050 dex against 0.144 dex scatter; both footings are shown.
- **Fig. 2:**
  - (a) correct, both footings;
  - (b) the grey bars are hard-coded and asymmetric (3, 23), the "½" label is illegible, and the third estimator is missing (5);
  - (c) correct.
- **Fig. 3:** shows what the text says; some text is small (34).
- **Fig. 4:** the ±0.13 dex bars show the superseded one-object rule (22). The halo band does not reflect the gated halo mass (1).
- **Fig. 5:** correct.
- **Fig. 6:** correct, with its caveats in the caption.
- **Axis labels and units:** present throughout.
