# MNRAS submission package, version 3 (prepared 2026-10-02)

Manuscript: *The galactic acceleration scale and the cosmological constant: the coefficient measured, its degeneracy
with H0, and a redshift test.* 14 pages in `mnras.cls`, 6 figures, 10 tables, 49 references, 2 appendices; abstract
247 words (by the bundle script's count, which counts each math span as one word; 250 by a plain whitespace count).
This package supersedes `../mnras_submission_2026_v2/` (2026-09-25; it carries `SUPERSEDED.md`) and, through it,
`../mnras_submission_2026/` (2026-09-06). Section 7d lists what changed for v3 and why; sections 7–7c record the
earlier revisions. Journal rules below were checked against the MNRAS Instructions to Authors, the MNRAS
open-access and author-charges pages and the RAS Editorial Code of Practice on 2026-09-21 (not re-checked for v3).
Items marked **[author]** need the author.

## 1. What is here

| file | role |
|---|---|
| `mnras_a0_lambda_v3.tex`, `references.bib`, `mnras_a0_lambda_v3.bbl` | manuscript source (class `mnras`, options `fleqn,usenatbib`; style `mnras.bst`) |
| `mnras_a0_lambda_v3.pdf` | compiled manuscript with a placeholder in place of the e-mail address |
| `fig1_rar.pdf`, `fig2_kappa.pdf`, `fig_deep.pdf`, `fig3_laws.pdf`, `fig4_amplification.pdf`, `fig5_rc100.pdf` | Figures 1–6 in that order (the deep-regime figure is Figure 3; the older files keep their names), vector PDF, one per file |
| `paper_numbers.py` → `paper_numbers.out`, `paper_numbers.json` | every number in the text that is not from the repository estimators; 71 checks, each labelled by kind: 28 identity (arithmetic, or a quoted committed output; no evidence), 7 model, 30 data, 6 injection. It reads the CORRECTED RC100 transcription and re-runs the inversion on the earlier one beside it (old → new table in its output, section S5) |
| `make_figures.py` | builds the figures from the same functions (6 checks) |
| `reproduce_all.sh` | re-runs the three repository estimators, the KMOS3D replication lane (L332, and L332 again in a scratch mirror with the corrected RC100 file), the footing profile likelihood, the two scripts above and the LaTeX build; stops on any failure (v3 fixes v2's script, whose `&& echo` lines let a failed build or diff pass) |
| `make_upload_bundle.py` | writes the git-ignored `upload_bundle/` (section 4); the build is gated on the checks |
| `COVER_LETTER.md` | cover-letter text |
| `.gitignore` | keeps `author_private.tex`, `upload_bundle/` and build intermediates out of the repository |

Rebuild everything: `bash reproduce_all.sh`. Build the upload files: `python3 make_upload_bundle.py`.

## 2. Before uploading **[author]**

1. **Read every sentence.** The author of record answers the referee. Check in particular: the two κ estimators and
   their error budgets (Section 3); the footing paragraph of Section 3.8 (a third estimator puts κ = ½ on the ρ_Λ
   footing 1.8σ below its best fit, stated against interest); the deep regime of Section 3.7 (the digitised MIGHTEE-HI points and the mass-to-light argument); the against-interest statements (estimator B's error bar; "one galaxy does not
   decide"; the RC100 check "is not a measurement"; MUSE-DARK III as the strongest published result against
   constancy; the KURVS lean towards a0 ∝ H(z)); the common-mode calibration paragraph and Table 10 (Section 5.4);
   Section 6; and the AI disclosure in the Acknowledgements, which must describe the tools actually used. Edit it if
   it does not.
2. **E-mail.** `author_private.tex` (git-ignored, one line: `\newcommand{\authoremail}{...}`) holds the address. The
   tracked `.tex` and `.pdf` never contain it; `make_upload_bundle.py` typesets it only inside `upload_bundle/`.
3. **Affiliation.** The title page reads `Briar Creek Tech, USA`. MNRAS asks for a full address; add city and state
   in the `.tex` if wanted, then re-run `make_upload_bundle.py`.
4. **ORCID.** Link the author's ORCID (second line of the git-ignored `author_private.tex`) to the ScholarOne account.
5. **Decide how the open-access charge will be met** (section 3) before submitting, because a waiver request is
   sent at the same time as the submission.

## 3. Cost

MNRAS has been fully open access since January 2024. There are no page charges, but every accepted Paper carries an
article processing charge: **£2,356** (Letters £1,122). Fellows of the RAS receive 20 per cent off (£1,885) and give
their membership number when paying. The corresponding author signs the licence (CC BY is the only option) and is
liable for the charge. Nothing is paid at submission.

Waivers: full or partial waivers are granted case by case by the RAS and OUP (the journal's open-access page gives
financial hardship as an example); there is no separate rule for unaffiliated authors. To apply, complete OUP's
waiver application form and e-mail it to the OUP author-support address given in the Instructions to Authors **at the
same time as the submission**. The journal's open-access page gives a second OUP address for the same purpose; copy
both. Do **not** mention the waiver in the cover letter: the request is handled separately from editorial review and
the editors do not see it.

## 4. Submitting (ScholarOne)

Run `python3 make_upload_bundle.py`. It writes:

| file in `upload_bundle/` | where it goes |
|---|---|
| `01_manuscript_for_review.pdf` | the **single file** uploaded at first submission (MNRAS does not compile LaTeX at this stage; limit 10 MB, this one is 0.4 MB) |
| `02_title_abstract_keywords.txt` | title, running head, abstract (247 words by the script's count, 250 by a plain count; limit 250), six keywords from the MNRAS list, funding and conflict statements: paste into the form. Check the word count ScholarOne reports after pasting |
| `03_cover_letter.txt` | paste into the cover-letter box |
| `04_alt_text_for_figures.txt` | alt text, now required for every figure at submission |
| `05_source_for_acceptance.zip` | not needed yet: the source archive MNRAS asks for after acceptance (`.tex`, `.bbl`, `.bib`, `fig1.pdf`–`fig6.pdf`, readme) |

Steps:
1. Log in at the MNRAS ScholarOne site (mc.manuscriptcentral.com/mnras); create an account if needed and attach the ORCID.
2. Start a new submission; manuscript type **Paper** (Main Journal). A Letter is limited to five pages and must argue
   for rapid publication; this is neither.
3. Paste title, abstract and keywords from file 02. Enter funding "none" and conflict of interest "none".
4. Upload file 01 as the main document. Add the alt text for each figure from file 04 where the form asks for it.
5. Paste the cover letter (file 03). It carries the three required declarations: AI use, conflicts of interest and the
   earlier Zenodo postings (three DOIs in v3). MNRAS asks that the letter does not summarise the results; this one does not.
6. Non-preferred referees: optional, with reasons. There is no field for suggesting referees.
7. Confirm the Data Availability statement (it is in the manuscript) and the use-of-AI declaration.
8. Check the PDF proof that ScholarOne builds, then submit. If applying for a waiver, send the form now (section 3).

What happens next: a manuscript number (MN-26-…); median time to a first decision about 33 days (RAS statistics for
2024). Revision windows: 45 days (minor), 3 months (moderate), 6 months (major). Every rejection is confirmed by a
second editor; "Reject" without an invitation to resubmit is final, with an appeal to the Editor-in-Chief within a month.

## 5. After acceptance

Upload `05_source_for_acceptance.zip` (rebuilt with the final text), sign the CC BY licence, pay or confirm the waiver,
and update the Zenodo records with the journal DOI.

## 6. What a referee is likely to ask, and where the paper answers

- *"The coincidence is old."* The Introduction says so and credits Milgrom (1983, 1999, 2020), Limbach, Psaltis & Özel
  (2008), Blanchet & Le Tiec, Klinkhamer & Kopp, and Verlinde. The claimed additions are the error budget, the floor,
  the H0 degeneracy and the design of the redshift test.
- *"κ = 1/2 is numerology."* The paper does not claim it: Table 6 shows four candidates the data cannot separate, the
  likelihood ratio between 1/2 and 0.461 is e^-0.02, and Section 6 opens with "the coefficient is not derived".
- *"The mass-to-light ratio decides everything."* Section 3.2 and Table 2 show it; Section 3.4 derives the 9.5 per
  cent floor; Section 6 states the value of Υ that would exclude κ = 1/2.
- *"A constant a0 is just MOND."* Stated in Sections 5.1(a) and 6: the test separates constancy from the H(z) coupling
  and from the ΛCDM-emergent rise, not the Λ anchor from a bare constant.
- *"The ΛCDM prediction is not one number."* Section 5.1(c) and Table 7 give the range (+0.23 to +0.46, and +0.56 for
  a second scaling); the smallest plausible rise is used as the decision value, and halo-to-halo scatter is in the odds.
- *"The RC100 inversion is circular / your estimators just return the a0 you put in."* Section 3.6 and Appendix B: every
  estimator is fed synthetic data with a KNOWN a0 (0.7, 1.0, 1.3 × the κ = ½ value) built on the real baryons and returns it
  (standard fit < 1%, deep band < 2.1%, shape-only < 2.3% through a 20% distance error); the RC100 inversion returns injected
  trends to 0.01 dex/z; estimator A moves 0.6% when its correction is iterated to its own output. Of the 51 checks, the 15
  identities are labelled as carrying no evidence (v3: 71 checks, 28 identities).
- *"MIGHTEE-HI finds a0 = 1.69 × 10^-10, nearly twice your value."* Section 3.7, Table 5 and Fig. 3(b): with the survey's own SED
  mass-to-light ratios (K_s median 0.35) κ_Λ = 0.90 ± 0.07 and the two surveys disagree by 4.0–6.6σ; the survey's own refit with a
  fixed Υ_K = 0.6 gives 0.58 ± 0.05, consistent with SPARC (0.3–2.1σ); Marasco et al. (2025) find a K_s median of 0.72. The paper
  states that the deep-regime amplitude is set by the mass-to-light convention, not by the relation.
- *"The deep slope is not 1/2."* Equation (25): the relation's own slope over the sampled window is 0.56–0.58, not 1/2, and the
  per-galaxy slopes match it (0.1–1.6σ) while excluding 0.75 at 4.2–4.9σ; the statistic is injection-tested (I6).
- *"RC100 shows a0 is flat."* The paper says it does not: Section 5.3 shows the verdict is erased by a 0.05 dex/z drift in the
  baryonic-mass calibration, one edge galaxy moves it 0.4σ, and an independent KMOS3D sample does not reproduce the pattern
  (27–54% of its z > 1.9 galaxies rotate below their own Newtonian baryons). Existing data decide nothing. The halo law is
  disfavoured at 2.5–4.3σ across the selection controls (v3, corrected transcription; 2.6–4.3σ in v2).
- *"Your RC100 table is wrong."* It was: the repository's earlier transcription had 17 wrong cells (CFG287/CFG289). v3 uses the
  corrected file, says so once in Section 5.3, and `paper_numbers.py` re-runs the inversion on both files (check S5i: no
  statement changes; the slope moves by 0.0008 dex/z).
- *"MUSE-DARK III finds a0 rising."* Section 5.3 states it at face value as the strongest published result against
  constancy, then shows that in the survey's public per-galaxy products the rise appears only with the masses fitted
  jointly with the dark halo (+0.57 ± 0.09 dex across the thirds, against +0.18 for H(z)); with SED masses ± H2 it is
  −0.11 ± 0.49 / +0.04 ± 0.14, and which mass is right is not settled (an SED bias of 1.8–2.2 dex/z would be needed, but
  SED + H2 exceeds the model's dynamical mass in many high-z galaxies). Route-dependent: neither the rise nor constancy is established.
- *"KURVS favours a0 ∝ H(z)."* Section 5.3 reports the +3.3σ / −0.1σ decision cell against interest and why it is not a
  detection: the tabulated velocities are the authors' model at R_max (measured markers: +2.4 / −0.4), and the lean ends for a
  4.5% lower velocity scale, at 1.5 M* of gas or at 0.6 of the pressure calibration; likelihood ratio 0.5–1.7 with nuisances.
- *"MIGHTEE-HI/LADUMA finds a 5σ evolution."* Section 5.3: within the sample the slope is −1.04 ± 1.51 per unit z (consistent
  with both laws; the rival changes a0 by only 4.5% over z < 0.09); the SPARC-anchored 5σ flips sign with the M/L convention
  (+5.23 vs −4.80) and in mocks its formal error is 5.2× too small.
- *"κ = 1/2 beats Milgrom's 1/2π."* The paper does not say so: like for like on H0 the profile likelihood gives Δχ² 7.0 (½ on
  ρ_crit) vs 5.3 (cH0/2π); ½ is ahead of 1/2π only with both on the ρ_Λ footing (64 vs 154), where both sit below that
  estimator's best fit (Section 3.8).
- *"Four galaxies at 0.20 dex cannot be enough if the gas calibration is shared."* Correct, and v3 says so: Table 10 and the
  common-mode paragraph of Section 5.4 (20:1 needs a shared calibration ≤ 0.09 dex against the halo law, ≤ 0.16 dex against
  H(z); a 0.10 dex shared error takes four galaxies from 29:1 to 4:1); the conditioning paragraph explains why deep galaxies
  need an external calibration (CFG240).
- *"Are there any targets?"* Section 5.4 says no published object passes every gate, and gives the mass–radius condition.

## 7. What changed from the 2026-09-06 package and from the Zenodo deposits

1. **Scope.** The aether–scalar zero-mode theorem, the four-form construction and the Gaia DR4 two-arm registration are
   no longer in this paper (they remain in the Zenodo records). This is a single-argument empirical paper.
2. **The redshift law.** The earlier draft wrote the prediction as √ρ_DE(z), "0.82 at z = 2.5 with DESI". The
   prediction here is constancy; the density mapping appears only to show the test is robust to it (−0.09 to −0.11 dex).
3. **Estimator B's error bar was too small.** With the bulge mass-to-light ratio varied over 0.6–0.8 and a bootstrap
   over galaxies, 0.551 ± 0.043 becomes **0.55 ± 0.17** (`paper_numbers.py`, checks S2e, S2f). The likelihood ratio
   between 1/2 and 0.461 drops from e^1.4 to e^-0.02.
4. **One galaxy does not decide the redshift test.** With intrinsic scatter (0.09 dex after amplification) and
   halo-to-halo scatter (0.13 dex) included, one object at 0.13 dex gives 4:1, not 20:1. Two at 0.10, three at 0.13 or
   four at 0.20 dex are needed (check S4i). The paper says that this supersedes the deposited single-object design.
5. **Lensing enters the budget.** g_bar is magnification-free but g_obs ∝ μ^1/2, so δlog μ enters multiplied by
   A_obs/2 ≈ 1.3; the magnification requirement tightens from 0.08 to about 0.05 dex.
6. **RC100.** The 3.9σ against the halo-emergent rise does not survive every selection control; the paper quotes the
   range 2.6–4.3σ and the slope range −0.14 to +0.01 (checks S5c, S5d).
7. **Thermal identification.** Equating the Unruh and de Sitter temperatures gives a0 = cH_Λ (κ = 2.89, excluded), not
   cH_Λ/2π; the 2π forms are Milgrom's (2020, his eq. 3) statement of the coincidence and are cited as such.
8. **Sign convention.** The deposited pre-registration defines Δ_BTFR = −log10[a0(z)/a0(0)] but quotes +0.33 for a rise;
   this paper defines Δ = log10[a0(z)/a0(0)] throughout, so a rise is positive.
9. **Bibliography.** 28 entries re-verified against arXiv and Crossref; `Singh2026` dropped (a conference sketch, not a
   derivation); MUSE-DARK II and III, Limbach et al., Mayer et al. and Keller & Wadsley added with what each reports.

## 7b. Revision of 2026-09-25 (after checking every repository commit since the first package)

1. **RC100 downgraded to "decides nothing"** (repository lanes L331, L332, reproduced in `paper_numbers.py` S5e–S5g): the
   inversion's slope moves from −0.11 to +0.02 under a −0.05 dex/z baryonic-mass drift (halo law then within 2σ) and to
   +0.16 ± 0.07 under −0.10 (constancy 2.3σ off); the one galaxy at the f_DM = 0.02 edge moves it 0.4σ; the KMOS3D
   replication failed on a common-mode input problem. The abstract, Section 5.3, the RC100 figure caption (now Fig. 6) and Conclusion (vii) say so.
2. **Injection tests added** (Section 3.6; checks I1–I5) and **every check labelled by kind**, so no identity is presented as
   evidence (Appendix B).
3. **Deep band reported** (Section 3.2): κ = 0.56 / 0.49 / 0.44 at Υ_disc = 0.5 / 0.6 / 0.7 for g_bar < 0.1 a0 with the quality
   cut; equal weight on points with > 10% velocity errors lowers each by ~0.1 (stated).
4. **MUSE-DARK III stated at face value** as the strongest existing evidence against constancy (+0.3 dex at z ≈ 1), next to
   the flat Tully–Fisher zero point of MUSE-DARK II from the same survey.
5. **Prior art added:** Oppenheim & Russo (2024, arXiv:2402.19459) and the reply of Hertzberg & Loeb (2024, JCAP 09, 046).
6. **The one plausible target named:** OLAS M0717-02064 (Hirtenstein et al. 2019, ApJ 880, 54), from the verified ledger
   `prep_2026/a0z_crossscale/highz_target_ledger_verified_2026.py`; the old candidate list is superseded.
7. **H0 wording:** only the product κH0 is structural; the match of 0.461 and ½ to the SH0ES and Planck H0 is called a
   numerical coincidence.
8. **Not in the paper, but checked because it would contradict it:** the repository's "joint deep a0_eff = 0.717 ± 0.059,
   4.77σ below canonical" (deepseek O04b) rests on a SPARC channel whose deficit is carried by a corpus's
   per-galaxy mass-to-light ratios (compiled earlier in this project, not by a third party; corrected 7c) (median 1.17, up to 15, applied to bulges); with 3.6 µm population values the same
   statistic is 1.4–1.9. Audit: `real_research/reviews/deep_a0eff_audit_2026_09_25/D01_deep_a0eff_ml_audit.py`.
9. The κ = ½ derivation claims of 2026-09-21/22 (PD22, I14) were closed by the repository's own audit
   (`opus_48_extended_research/kappa_audit_2026/CAPSTONE_kappa_nogo.md`); the paper's "κ is not derived" stands.

## 7c. Revision of 2026-09-25, evening: the deep regime in two surveys

1. **New Section 3.7, Table 5, Fig. 3 and equation (25).** In the window g_bar < 0.2 a0 the kernel's own slope is
   β(y) = 1 + n(y) = 1/2 + √y/4 + …, i.e. 0.56–0.58 at the sampled points, not 1/2. Per-galaxy slopes (median over galaxies with
   ≥ 3 points): SPARC 0.62 / 0.61 / 0.58 at Υ_disc = 0.5 / 0.6 / 0.7 (125 / 120 / 116 galaxies), MIGHTEE-HI 0.60 ± 0.08 (17);
   differences from the kernel +1.6 / +1.3 / +0.1 / +0.5σ; 0.75 excluded at 4.2–4.9σ and the Newtonian slope at 12σ; a line through
   all SPARC points agrees too (0.53–0.57 vs 0.56). Amplitude: SPARC κ_Λ = 0.60 / 0.52 / 0.46 (brackets 1/2); MIGHTEE-HI 0.89 ± 0.13
   (our window fit; returns the survey's 1.69e-10 to 1.2%), 0.90 ± 0.07 at the survey's SED ratios, 0.58 ± 0.05 at its fixed
   Υ_K = 0.6. At face value the surveys disagree by 4.0–6.6σ; at comparable ratios they agree (0.3–2.1σ). Checks S6a–S6j and I6
   in `paper_numbers.py` (11 new; 51 in all).
2. **The pitfall paragraph.** Per-galaxy disc ratios fitted to the rotation curves (the corpus behind the repository's
   "deep a0_eff 0.72", compiled earlier in this project: median 1.17, up to 15, log-correlation 0.92 with the Newtonian
   no-dark-matter ratio) give κ_Λ = 0.28 ± 0.03 in the same window, a factor 1.7–2.2 low (check S6i). Audit trail:
   `real_research/reviews/deep_a0eff_audit_2026_09_25/` (D01–D04), cited in Appendix B.
3. **MIGHTEE-HI data.** Vărăşteanu et al. (2025, MNRAS 541, 2366; doi 10.1093/mnras/staf1079; arXiv:2504.20857) publish the
   radial acceleration relation only as a figure. The 80 points were extracted from the vector graphics of the arXiv figure
   (`deepseek_push/data2/mightee2025_rar_digitized_points.csv`, lane G099); one marker colour is one galaxy (the colour encodes
   each galaxy's baryonic surface density; 18 colours for 19 galaxies, two share one). Their Table 3 refits (1.69 ± 0.13, 2.06 ± 0.15,
   1.08 ± 0.09, 1.47 ± 0.13 × 10^-10) and the K_s SED median of 0.35 were read from the paper on 2026-09-25. Marasco et al. (2025,
   A&A 695, L23; doi 10.1051/0004-6361/202553925) give the K_s median of 0.72. Both references verified against Crossref.
4. **Where it shows.** Abstract (one sentence; 248 words), Section 3.8 (the deep regime as a consistency test, not a third
   estimator), Section 6 (the mass-to-light limitation now names MIGHTEE-HI), new Conclusion (iii), Data Availability,
   Appendix B. Tables 5–8 of the previous version are now 6–9, and Figures 3–5 are now 4–6 (all cross-references are labels).

## 7d. Version 3 (2026-10-02): corrected RC100 input and the redshift record since 2026-09-25

Scripts first, then text. Every new number is printed and checked by `paper_numbers.py` (S4m–S4r, S5h–S5i, S7a–S7l).

1. **RC100 input corrected.** `paper_numbers.py` now reads `real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv`
   (CFG289, 51c70923f; sha256 a1778d75…, checked by S5h). The earlier transcription differed from arXiv:2209.12199 Table 3 in
   17 cells: 9 log M_baryon (7 of them the adjacent log M_bulge column, 2 typos), 2 V_c, 1 f_DM, 5 names; one deep-regime flag
   flips (row 44). Three cells enter the inversion (rows 36, 43, 44). What moved (old → new; the full table is in
   `paper_numbers.out`, section S5): slope −0.112 → −0.111 ± 0.063; median â0 1.385 → 1.386 × 10⁻¹⁰; scatter 0.383 → 0.391 dex;
   control | g_obs −0.138 → −0.141; control | y +0.008 → +0.011; weakest halo-law exclusion 2.58 → 2.51σ (text 2.6 → 2.5σ);
   weakest H(z) exclusion 4.67 → 4.59σ (text 4.7 → 4.6σ); edge-galaxy slope −0.085 → −0.084; drift rows move ≤ 0.001.
   No statement changes (S5i). The L332 KMOS3D lines the paper quotes (T1, K1, "93 not in RC100") are identical with the
   corrected file (`reproduce_all.sh` step 5). Not quoted by the paper but moved by the correction: L323's RC100 stress slope
   (−0.100 → −0.055; for the CFG289 reader table).
2. **κ footing.** Section 3.8 adds the like-for-like profile likelihood (`real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.py`):
   cH0/2π and ½ on ρ_crit are indistinguishable (Δχ² 5.3 vs 7.0); ½ beats 1/2π only on the ρ_Λ footing (64 vs 154), where
   both sit below the estimator's best fit (κ = ½ at 1.8σ clustered, stated against interest; the gas-scale systematic is not
   in that error). Abstract, Section 6 and Conclusion (ii) say the 2π forms fit as well. "κ is not derived" stays.
3. **MUSE-DARK III revised to route-dependent** (CFG198/199/236, CFG262): v2's "strongest existing evidence against
   constancy" at face value is kept as the face-value statement and then qualified: the rise travels with the halo-fitted
   masses; SED routes are non-discriminating; which mass is right is not settled.
4. **KURVS added** (CFG140/160/165/189/194): a lean towards a0 ∝ H(z), reported against interest, not a detection; the
   tabulated velocities are the authors' model at R_max.
5. **MIGHTEE-HI/LADUMA added** (CFG279, CFG258; Vărăşteanu et al. 2026, arXiv:2608.03576, preprint): slope consistent with
   both laws; the anchored 5σ flips sign with M/L.
6. **z ≈ 2.5–14 record** (CFG255–286, CFG269; one paragraph): no sample measures a0; complete pools at z 4–14 MARGINAL at
   ±0.15 dex, NOT POSSIBLE at ±0.30 dex.
7. **The design reconciled with PAPER38/CFG240.** New paragraph and Table 10: a shared baryon calibration does not average
   down (exact KL divergence with covariance s²I + σ_C²J; reduces to v2's eq. 42 at σ_C = 0, check S4m); 20:1 needs a shared
   calibration ≤ 0.09 dex (halo) / ≤ 0.16 dex (H(z)); the present gas bracket 0.2–0.7 dex at z ≈ 2.2 is 0.09–0.48 dex on M_b.
   The CFG240 Fisher conditioning is recomputed for the paper's kernel (S4q reproduces CFG240's committed table) and the T4
   floor is checked on random designs (S4p). Abstract and Conclusion (viii) carry the calibration requirement. No conflict
   with v2's numbers remains: v2's odds were for independent errors and are kept, labelled as such.
8. **Data integrity:** one sentence in the Data Availability statement (CFG287: 22 sources, 3703 sampled cells in 29 tables,
   no transcription mismatch, no erratum; KURVS tables not in that audit) and the Appendix B lines for CFG289/CFG287.
9. **Limitations:** the cold matter is still required (one sentence); the zero-mode citation is scoped to the class examined.
10. **References:** + Puglisi et al. 2023 (MNRAS 524, 2814) and Kretschmer et al. 2021 (MNRAS 503, 5238), both checked
    against Crossref on 2026-10-02; + Vărăşteanu et al. 2026 (arXiv API, 2026-10-02); + Zimmerman 2026b (PAPER38 v1.3, DOI
    10.5281/zenodo.23108862; v1.3 deposited 2026-10-02, replacing the v1.2 citation). A `\nocite` after `\maketitle` makes mnras.bst's 2026a/b/c suffixes follow the list order.

## 8. Not verified
- **v3:** whether the published RC100 Table 3 (ApJ 944, 78) equals the arXiv v1 copy that both transcriptions were checked
  against (CFG287 lists it as OPEN). The Data Availability statement says so.
- **v3:** the KURVS tables were not in the CFG287 audit (stated in the Data Availability statement).
- **v3:** CFG289's commit message and `data_assembly/rc100_provenance/README.md` say "10 rows" of log M_baryon; the files differ
  in 9 such cells (7 bulge + 2 typos; 9 + 2 + 1 + 5 = 17). The paper uses the count from the files (check S5h).
- **v3:** PAPER38 is cited as Zimmerman 2026b for its a0(z) content only, at v1.3 (DOI 10.5281/zenodo.23108862, deposited
  2026-10-02), which corrects v1.2's Gaia DR4 paragraph; nothing the manuscript cites from it changes.
- **v3:** CFG269's committed run exits 1 from its frozen control C1 (two never-pooled multi-radius HZ9 rows, disclosed in
  that lane); the bins quoted here are its committed values.
- **v3:** the MNRAS rules in sections 3–4 were not re-checked on 2026-10-02.

- The figure number of the MIGHTEE-HI radial acceleration relation in the published MNRAS version (the arXiv v1 HTML shows it as
  fig. 11; the repository's G099 lane calls it fig. 3). The manuscript does not quote a figure number.
- OUP announced an updated AI-disclosure policy on 2026-09-10; the policy page would not load during the check. Read
  it before submitting and adjust the Acknowledgements sentence if it asks for more detail.
- The charge in USD or EUR (only the GBP figure is on the journal's pages).
