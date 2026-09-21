# MNRAS submission package, version 2 (prepared 2026-09-21)

Manuscript: *The galactic acceleration scale and the cosmological constant: the coefficient measured, its degeneracy
with H0, and a redshift test.* 10 pages in `mnras.cls`, 5 figures, 8 tables, 39 references, 2 appendices.
This package supersedes `../mnras_submission_2026/` (2026-09-06); section 7 lists what changed and why.
Journal rules below were checked against the MNRAS Instructions to Authors, the MNRAS open-access and author-charges
pages and the RAS Editorial Code of Practice on 2026-09-21. Items marked **[author]** need the author.

## 1. What is here

| file | role |
|---|---|
| `mnras_a0_lambda_v2.tex`, `references.bib`, `mnras_a0_lambda_v2.bbl` | manuscript source (class `mnras`, options `fleqn,usenatbib`; style `mnras.bst`) |
| `mnras_a0_lambda_v2.pdf` | compiled manuscript with a placeholder in place of the e-mail address |
| `fig1_rar.pdf` … `fig5_rc100.pdf` | figures, vector PDF, one per file |
| `paper_numbers.py` → `paper_numbers.out`, `paper_numbers.json` | every number in the text that is not from the three repository estimators; 29 checks that can fail |
| `make_figures.py` | builds the figures from the same functions (5 checks) |
| `reproduce_all.sh` | re-runs the three repository estimators, the two scripts above and the LaTeX build; stops on any failure |
| `make_upload_bundle.py` | writes the git-ignored `upload_bundle/` (section 4); the build is gated on the checks |
| `COVER_LETTER.md` | cover-letter text |
| `.gitignore` | keeps `author_private.tex`, `upload_bundle/` and build intermediates out of the repository |

Rebuild everything: `bash reproduce_all.sh`. Build the upload files: `python3 make_upload_bundle.py`.

## 2. Before uploading **[author]**

1. **Read every sentence.** The author of record answers the referee. Check in particular: the two κ estimators and
   their error budgets (Section 3); the against-interest statements (estimator B's error bar; "one galaxy does not
   decide"; the RC100 check "is not a measurement"); Section 6; and the AI disclosure in the Acknowledgements, which
   must describe the tools actually used. Edit it if it does not.
2. **E-mail.** `author_private.tex` (git-ignored, one line: `\newcommand{\authoremail}{...}`) holds the address. The
   tracked `.tex` and `.pdf` never contain it; `make_upload_bundle.py` typesets it only inside `upload_bundle/`.
3. **Affiliation.** The title page reads `Briar Creek Tech, USA`. MNRAS asks for a full address; add city and state
   in the `.tex` if wanted, then re-run `make_upload_bundle.py`.
4. **ORCID.** Link 0009-0008-3508-7982 to the ScholarOne account.
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
| `01_manuscript_for_review.pdf` | the **single file** uploaded at first submission (MNRAS does not compile LaTeX at this stage; limit 10 MB, this one is 0.3 MB) |
| `02_title_abstract_keywords.txt` | title, running head, abstract (250 words, the limit), six keywords from the MNRAS list, funding and conflict statements: paste into the form |
| `03_cover_letter.txt` | paste into the cover-letter box |
| `04_alt_text_for_figures.txt` | alt text, now required for every figure at submission |
| `05_source_for_acceptance.zip` | not needed yet: the source archive MNRAS asks for after acceptance (`.tex`, `.bbl`, `.bib`, `fig1.pdf`–`fig5.pdf`, readme) |

Steps:
1. Log in at the MNRAS ScholarOne site (mc.manuscriptcentral.com/mnras); create an account if needed and attach the ORCID.
2. Start a new submission; manuscript type **Paper** (Main Journal). A Letter is limited to five pages and must argue
   for rapid publication; this is neither.
3. Paste title, abstract and keywords from file 02. Enter funding "none" and conflict of interest "none".
4. Upload file 01 as the main document. Add the alt text for each figure from file 04 where the form asks for it.
5. Paste the cover letter (file 03). It carries the three required declarations: AI use, conflicts of interest and the
   earlier Zenodo postings. MNRAS asks that the letter does not summarise the results; this one does not.
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
- *"κ = 1/2 is numerology."* The paper does not claim it: Table 5 shows four candidates the data cannot separate, the
  likelihood ratio between 1/2 and 0.461 is e^-0.02, and Section 6 opens with "the coefficient is not derived".
- *"The mass-to-light ratio decides everything."* Section 3.2 and Table 2 show it; Section 3.4 derives the 9.5 per
  cent floor; Section 6 states the value of Υ that would exclude κ = 1/2.
- *"A constant a0 is just MOND."* Stated in Sections 5.1(a) and 6: the test separates constancy from the H(z) coupling
  and from the ΛCDM-emergent rise, not the Λ anchor from a bare constant.
- *"The ΛCDM prediction is not one number."* Section 5.1(c) and Table 6 give the range (+0.23 to +0.46, and +0.56 for
  a second scaling); the smallest plausible rise is used as the decision value, and halo-to-halo scatter is in the odds.
- *"The RC100 inversion is circular."* Section 5.3 calls it a consistency check, names the three reasons, and quotes
  the weakest significance (2.6σ) rather than the strongest (4.3σ).
- *"MUSE-DARK III finds a0 rising."* Cited and discussed in Section 5.3 together with the flat Tully–Fisher zero point
  from the same survey (MUSE-DARK II); the conclusion drawn is that z ≈ 1 is undecided.
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

## 8. Not verified

- OUP announced an updated AI-disclosure policy on 2026-09-10; the policy page would not load during the check. Read
  it before submitting and adjust the Acknowledgements sentence if it asks for more detail.
- The charge in USD or EUR (only the GBP figure is on the journal's pages).
