# MNRAS submission package, version 3.2 (prepared 2026-10-03: RC100 on the journal table and on framework-native inputs)

Manuscript: *The galactic acceleration scale and the cosmological constant: the coefficient on SPARC, and what it takes
to measure its redshift evolution* (retitled in v3.1; the v3 title named the H0 degeneracy, now one paragraph).
**v3.2:** 16 pages in `mnras.cls`, 6 figures, 12 tables, 63 references (64 if the PAPER6 citation is kept), 3 appendices;
abstract 239 words by a plain whitespace count (249 with every math span counted as one word; limit 250). v3.2 revises
v3.1 (tag `mnras-v3.1`, 51413cc1b) in place; section 7f lists every change. (v3.1: 15 pages, 62 references, abstract 234/245.)
v3.1 revised v3 (commit 32f9a609c) in place, answering the hostile referee report
`campaign_fresh_gravity/CFG290_mnras_v3_referee/REFEREE_REPORT.md` (c1851ae6d; 1 CRITICAL, 10 MAJOR, 20 MINOR, 8 NIT);
section 7e answers every finding. It supersedes `../mnras_submission_2026_v2/` and, through it, `../mnras_submission_2026/`.
Journal rules below were checked on 2026-09-21 and not re-checked for v3 or v3.1. Items marked **[author]** need the author.

## 0. OPEN ITEMS FOR THE OWNER (decide before submission; the text is kept neutral)

- [x] **PAPER6 — DECIDED 2026-10-02 by the author: drop the citations (`\papersixfalse`, the default build).** Former TODO-PAPER6: Zenodo 10.5281/zenodo.22559892 (PAPER6, still v1 of concept 22559891) carries the
  four-form "stable (F6)" verdict withdrawn in the repository on 2026-09-27 (XR31, `kappa_closure/k04_F6_CORRECTION_2026-09-27.md`;
  on the DO-NOT-CITE list). Both variants are prepared and both build cleanly:
  - **Default (in the build now): `\papersixfalse`.** The two citations are removed: Section 3.5 mentions the earlier
    estimator-B variant (0.551 ± 0.043) without a citation, Section 5 drops the zero-mode sentence, Data Availability lists
    two Zenodo records. 62 references. Cover letter: variant `[PAPER6-REMOVED]`, which still declares the PAPER6 posting as
    an earlier note on the same coefficient (MNRAS asks for prior postings of parts of the work) and says why it is not cited.
  - **Alternative: `\papersixtrue`.** Both citations kept, each with "its four-form section is superseded"; 63 references
    (Zimmerman 2026a/b/c = kappa/a0z/wall, in list order). Cover letter: variant `[PAPER6-NOTE]`.
  - To switch: change the one line `\papersixfalse` → `\papersixtrue` in the .tex, regenerate the .bbl (section 1 note), run
    `reproduce_all.sh`, then `make_upload_bundle.py` (it reads the switch, picks the cover-letter variant, and refuses to run if
    the built bibliography disagrees with the switch). A third route the referee lists, depositing a PAPER6 v2/erratum
    first, is not prepared (no deposits in this revision).
- [x] **AI disclosure — DECIDED 2026-10-02 by the author: Claude, OpenAI, DeepSeek, GLM, Qwen and Gemini models were used; the Acknowledgements and cover letter now name all six, and the two model-produced inputs (MIGHTEE digitisation: DeepSeek; rotation-curve corpus: GLM) are named in the Acknowledgements.** Former TODO-AI-DISCLOSURE: The Acknowledgements and the cover letter still name only "Anthropic's Claude, through
  Claude Code" and unspecified "models from OpenAI". The referee (finding 10) asks whether other models produced inputs.
  Inputs of this paper that live in, or were committed from, model-named repository folders (traced through the paper's
  scripts, the four repository estimators it runs, and every lane cited in Appendix C with its common modules):
  1. `deepseek_push/data2/mightee2025_rar_digitized_points.csv` — the 80 digitised MIGHTEE-HI points (Section 3.8, Table 5,
     Fig. 3; `paper_numbers.py` S6). Added in commit e7cf8a93f, message prefixed "deepseek: G099".
  2. `glm53_push/data/rotation_curve_corpus_v7.json` — the per-galaxy fitted disc mass-to-light ratios of the pitfall
     paragraph (Section 3.8, last row of Table 5, grey point of Fig. 3b; S6i). Added in commit d193fc3b0, prefixed "glm53:".
  3. `sonnet55_push/puzzle_32pi/agents/Z1_causal_horizon_a0z/` (module `zcommon`, its `lcdm_native` proxy curve) — imported
     read-only by CFG223 (whose implied-a0 estimator CFG262 uses for the MUSE-DARK levels quoted in Section 4.3), by CFG229
     (on CFG262's import path) and by CFG269 (the z ≥ 4 pools, now cited qualitatively). The paper quotes no number of the
     proxy itself. Added in commit 1138d817f ("puzzle_32pi wave 4").
  4. `real_research/reviews/deep_a0eff_audit_2026_09_25/` (cited in Appendix C as the audit trail of the pitfall) re-runs
     `deepseek_push` lanes and reads the `glm53_push` corpus.
  5. `qwen_claude_field_theory/` — the paper's own directory: every paper script and the text. The commits of the MNRAS
     directories (v2, v3) carry no model prefix; other files under `qwen_claude_field_theory/` were committed with "qwen",
     "qwen3.827b:" and "openai" prefixes, none of which touched the MNRAS directories.
  No input was found in `gemini38_flash_push/`, `gemini_38_flash_push/`, `openai_push/`, `qwen38_push/`, `grok_push/`,
  `kimik3_push/`, `gemma4_push/`, `glm_moe_push/`, `hermes_push/`, `hy4_push/`, `nemotron_push/`, `sol61_push/` or the
  `opus_4*` folders. The owner should state which models actually produced items 1–5 (and the text) and the OpenAI model
  name(s); the orchestrator then edits the Acknowledgements sentence (marked `% TODO-AI-DISCLOSURE` in the .tex) and the
  cover-letter paragraph. Folder names alone do not establish which model did the work.
- [ ] **TODO-RUN [author] (finding 30).** The v3 wording "a script that the author has run" / "I ran every script myself"
  was replaced by statements that are true without it ("produced by a public script whose checks can fail"; "one command
  reproduces every number and figure"). If the owner runs `bash reproduce_all.sh` personally (about 2 minutes) before
  submitting, the stronger wording may be restored.
- [ ] **TODO-TAG [orchestrator] (finding 27).** Data Availability now names the tagged release **`mnras-v3.2`**. After committing
  v3.2, create that git tag (`git tag mnras-v3.2 <commit>` and push it), or replace the phrase with the commit hash
  (`mnras-v3.1` exists at 51413cc1b). A Zenodo
  snapshot DOI of the reproduction package is not minted (no deposits in this revision); it can be added on acceptance.
- [ ] **[author] Title.** v3.1 retitles the paper (finding 11). Revert in the .tex and COVER_LETTER.md if not wanted.

## 1. What is here

| file | role |
|---|---|
| `mnras_a0_lambda_v3.tex`, `references.bib`, `mnras_a0_lambda_v3.bbl` | manuscript source (class `mnras`, options `fleqn,usenatbib`; style `mnras.bst`) |
| `mnras_a0_lambda_v3.pdf` | compiled manuscript with a placeholder in place of the e-mail address |
| `fig1_rar.pdf`, `fig2_kappa.pdf`, `fig_deep.pdf`, `fig3_laws.pdf`, `fig4_amplification.pdf`, `fig5_rc100.pdf` | Figures 1–6 in that order (the older files keep their names; the bundle renames them fig1–fig6), vector PDF |
| `paper_numbers.py` → `paper_numbers.out`, `paper_numbers.json` | every number in the text that is not printed by a repository estimator; **v3.2: 100 checks: 48 identity, 13 model, 32 data, 7 injection** (Appendix C's tally is itself checked, S7n); about 35 s |
| `make_figures.py` | builds the figures from the same functions (6 checks) |
| `reproduce_all.sh` | re-runs the repository estimators, the H0 audit, L332 (in scratch mirrors only), the earlier profile likelihood, the two scripts above and the LaTeX build; stops on any failure; ends with "ALL STEPS PASSED" |
| `make_upload_bundle.py` | writes the git-ignored `upload_bundle/` (section 4); gated on the checks, on both abstract counts and on the PAPER6 switch |
| `COVER_LETTER.md` | cover-letter text with the two PAPER6 variants |
| `.gitignore` | keeps `author_private.tex`, `upload_bundle/`, `reproduce_outputs/` and build intermediates out of the repository |

Rebuild everything: `bash reproduce_all.sh`. Build the upload files: `python3 make_upload_bundle.py`.
**The .bbl:** plain `tectonic` does not refresh it. After any bibliography change: copy the .tex, .bib and figures to a
scratch directory, run `tectonic --keep-intermediates --keep-logs mnras_a0_lambda_v3.tex` there, check the log for
undefined references, and copy the .bbl back (done for v3.2: 63 entries, Lee et al. 2025 added; no undefined references;
v3.1: 62 entries).

## 2. Before uploading **[author]**

1. **Section 0 first** (PAPER6, AI disclosure, running the scripts, the tag, the title).
2. **Read every sentence.** The author of record answers the referee. Check in particular: the H0 convention (Section 3.1)
   and Table 7, which change every SPARC κ relative to v3; estimator C (Section 3.6), which replaces v3's profile-likelihood
   paragraph (that analysis used a different transition function; see 7e); the Desmond (2023) sentence and Table 8
   (Section 3.9, against interest); the gated decision value and the design (Sections 4.1 and 4.4, Tables 11–12), which
   replace v3's "two to four rotators"; the RC100 paragraph (Section 4.3), which no longer quotes any significance against
   the rivals; Appendix B; Section 5; the Acknowledgements.
3. **E-mail.** `author_private.tex` (git-ignored, one line: `\newcommand{\authoremail}{...}`) holds the address. The
   tracked `.tex` and `.pdf` never contain it; `make_upload_bundle.py` typesets it only inside `upload_bundle/`.
4. **Affiliation.** The title page reads `Briar Creek Tech, USA`. MNRAS asks for a full address; add city and state
   in the `.tex` if wanted, then re-run `make_upload_bundle.py`.
5. **ORCID.** Link the author's ORCID (second line of the git-ignored `author_private.tex`) to the ScholarOne account.
6. **Decide how the open-access charge will be met** (section 3) before submitting, because a waiver request is
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
| `01_manuscript_for_review.pdf` | the **single file** uploaded at first submission (MNRAS does not compile LaTeX at this stage; limit 10 MB, this one is 0.39 MB) |
| `02_title_abstract_keywords.txt` | title, running head, abstract (234 words plain, 245 with math spans as words; limit 250), six keywords from the MNRAS list, funding and conflict statements: paste into the form. Check the word count ScholarOne reports after pasting |
| `03_cover_letter.txt` | paste into the cover-letter box (the PAPER6 variant matching the .tex switch) |
| `04_alt_text_for_figures.txt` | alt text for every figure, built from `paper_numbers.json` |
| `05_source_for_acceptance.zip` | not needed yet: the source archive MNRAS asks for after acceptance (`.tex`, `.bbl`, `.bib`, `fig1.pdf`–`fig6.pdf`, readme) |

Steps:
1. Log in at the MNRAS ScholarOne site (mc.manuscriptcentral.com/mnras); create an account if needed and attach the ORCID.
2. Start a new submission; manuscript type **Paper** (Main Journal).
3. Paste title, abstract and keywords from file 02. Enter funding "none" and conflict of interest "none".
4. Upload file 01 as the main document. Add the alt text for each figure from file 04 where the form asks for it.
5. Paste the cover letter (file 03). It carries the three required declarations: AI use (section 0), conflicts of interest
   and the earlier Zenodo postings. MNRAS asks that the letter does not summarise the results; this one does not.
6. Non-preferred referees: optional, with reasons. There is no field for suggesting referees.
7. Confirm the Data Availability statement (it is in the manuscript) and the use-of-AI declaration.
8. Check the PDF proof that ScholarOne builds, then submit. If applying for a waiver, send the form now (section 3).

What happens next: a manuscript number (MN-26-…); median time to a first decision about 33 days (RAS statistics for
2024). Revision windows: 45 days (minor), 3 months (moderate), 6 months (major). Every rejection is confirmed by a
second editor; "Reject" without an invitation to resubmit is final, with an appeal to the Editor-in-Chief within a month.

## 5. After acceptance

Upload `05_source_for_acceptance.zip` (rebuilt with the final text), sign the CC BY licence, pay or confirm the waiver,
and update the Zenodo records with the journal DOI.

## 6. What a referee is likely to ask, and where the paper answers (v3.1)

- *"The coincidence is old; Limbach et al. already ran the test."* Yes: the Introduction says so and describes their
  result (both couplings excluded at the formal errors; with systematics a marginal preference for the dark-energy
  coupling). What the paper adds is what the test requires: the amplification analysis, the gate and the halo mass it
  selects, N as expected odds and as probability, the shared-calibration result and the Fisher bound. Section 4.2 explains
  why a Tully–Fisher test at high acceleration and z ≤ 1.2 (law (b) at most +0.30 dex there) cannot decide.
- *"Your ΛCDM decision value is for the wrong haloes."* Fixed in v3.1: +0.22 dex is the Dutton–Macciò rise for the haloes
  of the gate's discs (M200 = 3e10–1.8e11 at z = 2.5, from V_f = 83–125 km/s); the Duffy et al. relation gives +0.43 and is
  carried as a shared model systematic (Table 11, σ_sys columns).
- *"Odds of 20:1 is not the chance of 20:1."* Table 11 gives both: expected odds of 20:1 need N = 5/5/8 at 0.10/0.13/0.20 dex,
  where the chance of reaching 20:1 is only 0.53–0.68 and misleading evidence occurs in up to 10 per cent of trials; 90 per
  cent power needs 9/12/20.
- *"κ = 1/2 is numerology."* The paper does not claim it: three estimators on one stated H0 convention (0.45 ± 0.07,
  0.58 ± 0.18, 0.43 ± 0.08) all admit 1/2 and also 1/2π; Desmond (2023) puts 1/2 at 2.6σ on the ρ_Λ footing, stated against
  interest; Table 8 shows the coefficient follows the mass-to-light treatment; Section 5 opens with "the coefficient is not derived".
- *"Your κ mixes H0 conventions."* Fixed: SPARC's Hubble-flow distances are moved to H0 = 67.4 (the convention of ρ_Λ);
  Table 7 gives all three estimators on four conventions; the H0 inversion is redone self-consistently.
- *"The mass-to-light ratio decides everything."* Section 3.2 and Table 2 show it; Section 3.4 derives the 9.5 per cent
  floor; Section 5 states the Υ that would exclude κ = 1/2 (0.56 on the adopted convention).
- *"A constant a0 is just MOND."* Stated in Sections 4.1(a) and 5.
- *"RC100 shows a0 is flat."* It does not, and v3.1 quotes no significance against the rivals: the slope −0.11 ± 0.06 is
  erased by a −0.05 dex/z baryonic-mass drift (the halo law then about 2σ away; H(z) within 1σ at −0.10); f_DM tracks
  RC100's own baryonic-mass prior (ρ = +0.33, p = 0.036); RC100's own flagged rows move the slope by 0.3σ; the table is
  arXiv:2209.12199v1; KMOS3D does not reproduce the pattern.
- *"Your estimators just return the a0 you put in."* Section 3.7: injections return a known a0; estimator A's assumed-a0
  dependence is a sensitivity test on the real data (and labelled so in v3.1).
- *"MIGHTEE-HI finds a0 = 1.69e-10."* Section 3.8, Tables 5 and 8: with the survey's SED ratios the surveys disagree by
  5.0–7.5σ; with its fixed Υ_K = 0.6 they agree at Υ_disc = 0.5–0.6 (0.7 and 2.0σ) but not at 0.7 (3.1σ).
- *"MUSE-DARK III finds a0 rising."* Section 4.3 states it at face value (+0.30 dex against 1.2e-10, +0.38 against their own
  a0(0) = 1.0e-10); in the public per-galaxy products the rise is not recovered with SED stellar masses plus molecular gas,
  and the data cannot say which masses are biased (methods: Appendix B).
- *"KURVS favours a0 ∝ H(z)."* Reported against interest; under the simulation-calibrated correction the rival's central
  value sits at zero, and the lean ends for a 4.5 per cent lower velocity scale, 1.5 M* of gas or 0.6 of the pressure
  calibration (methods: Appendix B).
- *"Four galaxies are enough if the gas calibration is shared."* No: Table 12, a shared 0.10 dex error takes the recommended
  eight galaxies from 20:1 to 2.5:1; 20:1 from the sample means needs δ_c ≤ 0.06 dex (halo) or 0.15 dex (H(z)).
- *"Are there any targets?"* Section 4.4 says no published object passes every gate, and gives the mass–radius condition.

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

## 7e. Version 3.1 (2026-10-02): the response to the CFG290 referee report, finding by finding

Scripts first, then text. Every new number is printed and checked by `paper_numbers.py` (85 checks, 0 FAIL);
`reproduce_all.sh` ends with ALL STEPS PASSED; `make_upload_bundle.py` builds (0.39 MB PDF). Uncommitted: the
orchestrator verifies, commits and sends v3.1 to a second referee.

**New design numbers (Table 11; gated decision value Δ = +0.216 dex at z = 2.5, σ_int 0.091, σ_h 0.135 dex):**

| σ_m [dex] | N for expected 20:1 | P(reach 20:1) there (worse case) | P(wrong way) there (worse case) | N for 90% power | with σ_sys = 0.10: N_20 / N_90 | with σ_sys = 0.20: N_20 / N_90 |
|---|---|---|---|---|---|---|
| 0.10 | 5 | 0.68 | 0.07 | 9 | 10 / 29 | 14 / 40 |
| 0.13 | 5 | 0.55 | 0.10 | 12 | 13 / 44 | 20 / 63 |
| 0.20 | 8 | 0.53 | 0.10 | 20 | 27 / 110 | 48 / 167 |

The v3 designs at the gated value: two at 0.10 dex 4.4:1, three at 0.13 dex 6.1:1, four at 0.20 dex 4.5:1 (P(20:1) 0.15/0.32).
Shared calibration: 20:1 from the sample means needs δ_c ≤ 0.058 dex (halo; v3: 0.09) and ≤ 0.155 dex (H(z)).

| # | sev. | finding | response |
|---|---|---|---|
| 1 | CRIT | +0.33 dex is for 1e12 Msun; the gate's haloes give +0.18–0.26 | **Fixed.** S4 computes the gate at a0 = 9.36e-11 → V_f 83/105/125 km/s → M200(z = 2.5) = 3.0e10–1.8e11 for V_f/V200 = 1.0–1.2 → Dutton–Macciò +0.17 to +0.25; decision value +0.216 (central example, M200 7.9e10), reproducing CFG290 R8 (S4c2). The Duffy relation (+0.43) is carried as a shared prior width σ_sys = 0.10/0.20 on the halo law (composite hypothesis; Table 11). Tables 11–12, abstract, Sections 4.1/4.4, Conclusions (v)/(vii), Fig. 4 and Table 9 (new "halo, gate" column) redone. Not done: calibrating the ΛCDM side on simulated low-mass discs inverted at y < 0.3 (stated in Section 4.1 as not done). |
| 2 | MAJ | "odds" = exp⟨ln B⟩, not P(20:1) | **Fixed.** "Expected odds" defined; Monte Carlo of the exact likelihood ratio in S4 (reproduces CFG290 R3 to 0.001, S4s); P(20:1), P(wrong way) and N for 90 per cent power in Table 11 and the text (S4u). |
| 3 | MAJ | mixed H0 convention in κ | **Fixed.** SPARC Hubble-flow distances × 73/67.4 throughout (Section 3.1; `load_sparc(hf=)`); Table 7 gives A, B, C on four conventions, computed (A from the repository audit's q_HF = 0.202, S3e reproduces the audit to 0.002); estimator B on the adopted convention 0.584 (R9's value); Fig. 2(b) bars computed from those boxes, asymmetry explained in the caption; the H0 inversion is self-consistent (A 57 ± 15, B 73 ± 15); the profile likelihood is now estimator C in Table 6, Fig. 2(b) and the abstract. Also corrected: v3 said the Hubble-flow galaxies lie at the low-acceleration end; the audit (D4) shows the high-acceleration end. |
| 4 | MAJ | Limbach+08 ran the test | **Fixed.** Introduction describes their result; novelty statement rewritten around what the test requires; Milgrom (2017) and law (b) at z = 2 (×3.0, below his ~4) discussed (Sections 4.1, 4.3). |
| 5 | MAJ | selective κ citations | **Fixed.** Desmond (2023) sentence (κ_Λ = 0.636 ± 0.053; 1/2 at 2.6σ on ρ_Λ, 0.6σ on ρ_crit; 0.461 at 3.3σ; cH0/2π at 1.5σ) in Section 3.9, the abstract and Conclusion (ii), checked against R8 (S3g); new Table 8 of published a0 on both footings with each paper's M/L treatment (incl. Vărăşteanu 2025/2026); Li 2018, Rodrigues 2018, the McGaugh 2018 and Kroupa 2018 replies, Rodrigues 2018b and Marra 2020 in the Introduction. κ = 1/2 stays fitted; the footing-conditional statement is kept (on either common footing Milgrom's 2π form is at least as close as 1/2; S3i). |
| 6 | MAJ | RC100 near-5σ phrasing | **Fixed.** No significance against either rival is quoted ("we attach no significance to the formal distance"); slope −0.11 ± 0.06; −0.05 dex/z erases the preference (halo law about 2σ, −0.075 → 1σ), −0.10 brings H(z) within 1σ (S5e). |
| 7 | MAJ | RC100 disclosures | **Fixed.** (a) CFG217 G2 ρ = +0.33, p = 0.036, n = 41 (Price et al. 2021 masses; S5j); (b) RC100's own flags re-derived in S5d (rows 67, 83; 14 below 2.3; slope −0.089/−0.095, ≤ 0.35σ); (c) arXiv:2209.12199v1 named. "No mass model enters" replaced by "adds no mass model to the authors' own". |
| 8 | MAJ | re-analyses without methods; gas bracket self-sourced; CFG269 C1 | **Fixed.** Appendix B gives estimator, inputs and error model for MUSE-DARK and KURVS and the design of the post hoc MIGHTEE mocks (labelled post hoc); the lanes' interpolating function is stated (= eq. (nu) to 1e-6 for y ≤ 1, ≤ 2.4% above; S7m). "P" is gone; the z ≥ 4 paragraph is qualitative and discloses CFG269's C1 failure (S7g). Gas bracket: see 7. |
| 9 | MAJ | PAPER6 v1 cited | **Pending owner (TODO-PAPER6).** Both variants prepared and building; default removes the citations. |
| 10 | MAJ | AI disclosure | **Pending owner (TODO-AI-DISCLOSURE).** Input trace in section 0; text kept as stated, marked TODO. |
| 11 | MAJ | scope | **Partly.** Section 4 folded into Section 3.10 (one paragraph); Sections 2.2–2.3 compressed to one paragraph and Z dropped; title, abstract and Introduction now lead with what the a0(z) test requires. The order κ → redshift test is kept, because the redshift section uses the local calibration and conventions of Section 3 and a full reordering is better judged by the second referee. |
| 12 | MIN | abstract length | **Fixed.** 234 plain / 245 math-as-words; the bundle now gates on both. |
| 13 | MIN | KlinkhamerKopp DOI | **Fixed.** 10.1142/S021773231103711X (Crossref: Klinkhamer & Kopp, MPLA 26, 2783–2791). |
| 14 | MIN | comparator slopes mislabelled | **Fixed.** Matched comparators fitted by OLS at RC100's redshifts: +0.22 (H(z)), +0.15 (halo, 1e12). |
| 15 | MIN | "three decades" | **Fixed.** "about four decades". |
| 16 | MIN | MUSE-DARK wording | **Fixed.** "not recovered with SED stellar masses plus molecular gas; the data cannot say which masses are biased" (abstract, Section 4.3, Conclusion (vi)). |
| 17 | MIN | Ciocan's rise vs a different calibration | **Fixed.** +0.30 against 1.2e-10 and +0.38 against their own a0(0) = 1.0e-10; their interval corrected to 2.38 (+0.12/−0.10), 95 per cent. Verified from arXiv:2604.22613v1 HTML (eqs 2 and 4), page read 2026-10-02. |
| 18 | MIN | MIGHTEE mocks label; V25/V26 results | **Fixed.** Mocks labelled post hoc (with method, Appendix B); V26's bTFR zero-point trend (8.7σ forward, 3.4σ inverse, attributed to selection) and V25's tentative evolution added (arXiv abstracts). |
| 19 | MIN | KURVS "favours the rival" | **Fixed.** "the rival's central value sits at zero". |
| 20 | MIN | combined likelihood ratio | **Fixed.** Per estimator: A e^−0.22, B e^+0.12, C e^−0.31; no product formed. |
| 21 | MIN | check labels | **Fixed.** I4 → S2i (data; a sensitivity test); S2e, S5f, S7b, S7d, S7f, S7h → identity; S7k/S7l removed. Tally 85 = 39/13/28/5, checked against Appendix C (S7n). |
| 22 | MIN | Fig. 4 bars | **Fixed.** Bars are the sample-mean standard error of the recommended design (8 at 0.20 dex: 0.08/0.09 dex), labelled. |
| 23 | MIN | Fig. 2(b) bars hard-coded | **Fixed.** Computed from the convention boxes in `paper_numbers.py`; B is the current estimator. |
| 24 | MIN | B's H0 range from the old variant | **Fixed.** 0.489–0.584 for the current estimator (Table 7). |
| 25 | MIN | MIGHTEE colour groups | **Fixed.** Caveat stated (18 colours, 19 galaxies, 11-point group spanning 0.22 dex); slope without it 0.60 ± 0.09 vs 0.56 (S6k). |
| 26 | MIN | gate a0 unstated | **Fixed.** Working a0 9.36e-11 → 1.7e8 (R/kpc)² (S4 prints 1.679e8; 1.794e8 at a0 = 1e-10). |
| 27 | MIN | frozen snapshot; arXiv-v1 caveats | **Partly.** Tagged release `mnras-v3.1` named (TODO-TAG: create the tag); no Zenodo snapshot minted (no deposits). FS+18 and Umehata+26 v1-only caveat added with references. |
| 28 | MIN | intermediate-file errors in text | **Fixed.** RC100 transcription → one sentence in Data Availability; pitfall stated generally. |
| 29 | MIN | Mayer+23 redshift | **Fixed.** "between z = 0 and 2" (their abstract). |
| 30 | MIN | "has run every script" | **Partly (owner).** Wording made literally true; TODO-RUN. |
| 31 | MIN | ΛCDM and constancy | **Fixed.** Softened (Section 5, "Constancy is shared"). |
| 32 | NIT | compress 2.2–2.3, drop Z | **Fixed.** |
| 33 | NIT | Zenodo DOI types | **Fixed.** a0z now cites version DOI 22833314 (v3, with its title); kappa (22559892) and wall (23108862) are version DOIs (Zenodo API, 2026-10-02). |
| 34 | NIT | small figure text, rotated ½, Υ glyph | **Fixed.** STIX fonts (upright Υ), no text below 7 pt, unrotated "1/2"; label collisions removed (PNGs inspected). |
| 35 | NIT | figure file names | **Kept** (the bundle renames them fig1–fig6, as the referee asks). |
| 36 | NIT | PDF metadata | **Fixed.** hyperref pdftitle/pdfauthor. |
| 37 | NIT | "match the prediction" | **Fixed by removal.** The deep-slope sentence left the abstract for length; Conclusion (iii) says "agrees with the slope of equation (nu)". |
| 38 | NIT | reproduce_all rewrites tracked files | **Fixed.** L332 runs in scratch mirrors and its JSON is compared byte for byte with the committed one; only the paper's own products are rewritten (stated in the script header and Appendix C). |
| 39 | NIT | "one or two at z = 8–14" | **Moot.** The z ≥ 4 paragraph no longer quotes counts. |

**Found during the revision (not in the report):**
- **The v3 "third route" used a different transition function.** `mi_a0_profile_likelihood_milgrom_footing_2026.py` fits
  g_obs² = g_bar² + g_bar a0, not equation (nu), on the tabulated distances (κ_Λ = 0.575). Re-implemented as estimator C
  with equation (nu) on the adopted convention it gives 0.434 ± 0.040 (stat), 0.43 ± 0.08 total; the committed numbers are
  reproduced exactly by the same code given that script's inputs (S3f). The function moves C by 0.105 (> its statistical
  error; S3h), so the footing preference of a profile likelihood is function-dependent; v3's "Δχ² 7.0 vs 5.3" paragraph
  is withdrawn from the paper.
- **Consequences of the adopted H0 convention,** reported as they fall: the standard fit at Υ = 0.5 gives 1.05e-10 (1.19
  on the tabulated distances, kept as a replication, S2a); κ = 1/2 needs Υ_disc = 0.555 (ρ_Λ) and 0.465 (ρ_crit, now just
  below the 0.5–0.7 population range); the deep band gives 0.50/0.44/0.40; MIGHTEE's fixed-Υ_K value vs SPARC is now
  0.7/2.0/3.1σ (was −0.3/1.0/2.1σ); under the adopted convention A and C put 1/2 on ρ_crit at 2.1–2.2σ.
- **The odds formatter** printed 10^11 as "10^11" (LaTeX 10¹1); fixed to 10^{11}.

**Check criteria changed in v3.1, and why (disclosed so that no pass is mistaken for an unchanged test):**
- **S2g:** v3 required the deep-band κ in [0.40, 0.60]; under the adopted convention Υ_disc = 0.7 gives 0.397 and the check
  failed. It now tests what the text says: the deep band does not remove the M/L dependence (spread > 0.08).
- **S5b, S5d, S5e, S5i:** the checks of exclusion significances against the rivals were removed with the statements
  (finding 6). The new S5e tests rows of the drift table; its tolerances (< 2.2σ for "about 2σ", < 1.1σ for "about 1σ")
  were set after seeing the table, and the check says so.
- **S6g:** v3 required agreement within 2.5σ at every SPARC disc ratio; under the adopted convention Υ_disc = 0.7 is at 3.1σ.
  It is now an against-full-agreement check (agree at 0.5–0.6, not at 0.7; the M/L change moves the disagreement by > 4σ).
- **S6i:** an intermediate edit changed this criterion while the pitfall arrays were still on the tabulated distances; once
  they used the same convention the original criterion (factor > 1.5) held (1.67–2.18) and was restored.
- **S4c, S4d, S4i, S4l, S4n, S4r:** rewritten for the gated value; **S4h** now includes the gate's lightest haloes, so its
  threshold is 0.15 dex (smallest value 0.172) and the text reads "0.17–0.6 dex".
- **S7k, S7l** (the committed profile likelihood as quoted) removed; superseded by S3f (exact replication) and S3i.
- **New:** S2a2, S2i, S3e–S3j, S4c2, S4r2, S4s–S4v, S5j, S6k, S7m, S7n.

**Literature checks made for v3.1 (Crossref JSON, arXiv API Atom, Zenodo API; read, nothing saved):** KlinkhamerKopp2011
DOI; Li 2018 (A&A 615, A3); Rodrigues 2018 (Nat. Astron. 2, 668) and its reply (2, 927); McGaugh 2018 (2, 924);
Kroupa 2018 (2, 925); Marra 2020 (MNRAS 494, 2875; arXiv:2002.03946); Tacconi 2018 (ApJ 853, 179); Tacconi 2020 (ARA&A 58,
157); Bolatto 2013 (ARA&A 51, 207); Bertemes 2018 (MNRAS 478, 1442; the Stripe82 CO–dust paper, arXiv:1803.08926);
Geesink 2026 (ACE dust-to-gas, arXiv:2609.20926, preprint); Price 2021 (ApJ 922, 143); Förster Schreiber 2018 (ApJS 238, 21);
Umehata 2026 (ApJ 997, 79; arXiv:2502.01868); Zenodo 22563139/22833314/23108862/22559892. Abstract-level statements used:
Limbach+08, Milgrom 2017, Mayer+23, Desmond 2023, Vărăşteanu+25/26 (from `cfg290_abstract_reads.out` and the arXiv API).
Ciocan+26 eqs 2 and 4 from the arXiv HTML (265 kB page read).

## 7f. Version 3.2 (2026-10-03): RC100 on the journal table and on framework-native inputs

**Owner direction:** "we need to use all the data using our framework not ACDM assumptions!" Sources: CFG305 (journal
tables, 6c907be69), CFG303 (inputs tagged by origin; LCDM-free re-derivations, 2d9bdc1b9), CFG307 (ALESS 122.1 stress test),
CFG308 (CRISTAL stress test). kappa = 1/2 is FITTED; the cold mass is still required. Not deposited, not submitted.

**Scripts.**
- `paper_numbers.py`: input switched to `real_research/data/rc100_nestorshachar2023_table3_PUBLISHED.csv` (sha256 8a7ed57a…;
  the journal's Table B1, CFG305); the arXiv-v1 CORRECTED file and the first transcription are still run, for old -> new.
  New: the **framework-native route** (CFG303 route B) is computed inside the script by exec'ing CFG303's committed code
  read-only (its helpers, `xi`, the per-galaxy loop, `s5_table`) with CFG216's `disc_v2` and CFG217's `mu_t18`, exactly as
  CFG303 loads them; on the arXiv-v1 table it reproduces CFG303's committed S5 numbers to 0 (check S5k). New S7 reads of
  CFG303 (MUSE-DARK, KURVS, CRISTAL), CFG308, CFG307 and CFG305's Umehata geometry. CFG217 G2 now read from CFG305's
  journal-table re-run (unchanged: rho +0.33, p 0.036, n 41).
- Checks 85 -> 100 (identity 39 -> 48, model 13, data 28 -> 32, injection 5 -> 7). New: S5k-S5r, I5n, S7o-S7t. Reworded:
  S5e (v3.1's tolerance "-0.05 within 0.5 sigma of constancy" FAILS on the journal table, +0.6 sigma; v3.2's wording is
  "within 1 sigma", post hoc, labelled), S5h (journal vs arXiv-v1: 6 primary cells, rows 78 and 87; only row 87 enters
  the inversion), S5i (records the S5e verdict move against interest: v3.1 wording true on arXiv v1, false on the journal).
- `make_figures.py`: Fig. 6 (file fig5_rc100.pdf) now has two panels, (a) native (N 59), (b) the f_DM comparison (N 99);
  Fig. 5's RC100 band uses the native y (16-84%: 0.91-7.20).
- `reproduce_all.sh`: step 5 runs L332 with both the CORRECTED and the PUBLISHED tables (T1, K1 and the overlap count unchanged).
- `make_upload_bundle.py`: data statement (journal table, tag mnras-v3.2, CRISTAL) and the alt text of Figs 5-6.

**RC100 numbers (old -> new).**
| quantity | v3.1 (arXiv v1, f_DM) | v3.2 native route B (primary) | v3.2 f_DM comparison |
|---|---|---|---|
| N in the window | 99 | 59 (41 have g_bar,nat >= g_obs) | 99 |
| d log a0/dz | -0.111 +- 0.063 | -0.122 +- 0.098 | -0.092 +- 0.064 |
| median a0 | 1.39e-10 | 2.11e-10 (biased high: floor discs dropped) | 1.49e-10 |
| comparators (halo / H(z), OLS) | +0.15 / +0.22 | +0.15 / +0.23 | +0.15 / +0.22 |
| drift -0.05 | +0.02 +- 0.06 | +0.02 +- 0.09 (0.2 sigma) | +0.04 +- 0.06 (0.6 sigma) |
| flagged rows dropped | -0.09 / -0.10 | -0.14 +- 0.11 | -0.07 +- 0.06 |
The native route is identical on the arXiv-v1 and journal tables (row 87 is a Newtonian-floor disc on both). The
journal refit moves the f_DM slope by +0.30 sigma. The weakest formal H(z) exclusions (comparison 4.4, native 2.2 sigma)
are printed by the script and NOT quoted in the text. RC100 decides nothing.

**Text changes.**
- Header comment: version 3.2.
- Abstract: the RC100/MUSE/KURVS sentence now states the native-input results (no rise; 41 at the Newtonian limit; drift
  erases any trend; MUSE-DARK rise disappears; KURVS lean needs a simulation-calibrated correction). 239/249 words.
- Section 4 (amplification): RC100's y on native baryons (median 2.4, 0.9-7.2, 2 of 100 below 0.3; 0.2 dex -> 0.8 dex);
  Fig. 5 caption says so.
- Section 4.3, RC100: rewritten. Native route primary (SED M* + Tacconi gas, thin disc, eq. rc100 with f = 1 - g_bar/g_obs);
  41 floor discs; N 59, -0.12 +- 0.10; the f_DM inversion labelled as the comparison ("the authors' halo-model dark
  fraction"), -0.09 +- 0.06; the journal table used and checked (arXiv-v1 caveat dropped); the five reasons now give both
  routes (flags, selection controls, drift); KMOS3D's below-baryons fraction tied to RC100's 41 native floor discs.
- Section 4.3, MUSE-DARK: the SED routes' numbers replaced by CFG303's native ones (-0.26 +- 0.28 dex; with H2 the highest
  third has no root, 21 of 36); the earlier SED-route numbers kept in parentheses as the halo-normalised comparison.
- Section 4.3, KURVS: one added passage: the lean needs the Kretschmer (LCDM-simulation) calibration; with the measured
  points and analytic corrections, P2 reads 'neither' and the 24 cells split 4 / 7 / 13.
- Section 4.3: new paragraph "Native inputs at z ~ 2-5": CRISTAL (no native point excludes constancy; CFG308 NOT
  DISCRIMINATING, 59% / 24% of 1008 cells) and ALESS 122.1 (CFG307 NOT ROBUST; no root in 44% of 540 cells; one-axis range
  no root to about 20x). Lee et al. (2025) cited (new reference).
- Fig. 6 caption: two panels.
- Conclusions 5 ("factors of 5 and 4", native y) and 6 (rewritten on the native record).
- Acknowledgements: Lee et al. (2025) table added. AI disclosure unchanged (six providers).
- Data Availability: tag `mnras-v3.2`; the journal table (Table B1) used and checked against journal and arXiv v1; the J0901+1814
  refit and the row-78 slip described; Umehata+26 now checked against the journal (its 870 um fit differs, no status change);
  FS+18 still arXiv v1 only.
- Appendix B: MUSE-DARK routes (ii)/(iii) redefined without halo-fit normalisation; new "Native inputs" paragraph.
- Appendix C: tally 100 / 48 / 13 / 32 / 7; paper_numbers bullet; CFG305, CFG303, CFG307, CFG308 listed.
- Kept: PAPER6 dropped (`\papersixfalse`); kappa = 1/2 fitted; the cold mass required; no MeerKAT (PAPER40) sentence added.

**Not verified in v3.2.**
- CFG303's transcription of RC100 column 6 (SED M*) is one reader's, from the arXiv-v1 raster; T3 matches Price+21 for the
  41 RC41 galaxies (median 0.000 dex). CFG305 states the journal's row-87 log M* is unchanged (10.96); the other 99 rows of
  column 6 were not compared with the journal.
- The native gas is CFG217's mu_t18 without the delta_MS term (disclosed in Appendix B).
- ALESS 122.1 is named without a citation of its data sources (CFG229 uses Dunne et al. 2022 gas and Calistro Rivera et al.
  2018 kinematics); neither is in references.bib. **[author/orchestrator]** add them, or drop the name, before submission.
- The Lee et al. (2025) entry was taken from `citations/REFERENCES.bib` (A&A 701, A260; doi 10.1051/0004-6361/202555362)
  and not re-checked against the journal page.

## 8. Not verified
- **v3.1:** the MUSE-DARK, KURVS, MIGHTEE-mock and z ≥ 4 numbers are the committed outputs of the repository lanes; they
  were not re-run here (Appendix B describes their methods; `paper_numbers.py` checks only that the text quotes them).
- **v3.1:** CFG217 G2's 41 galaxies are the RC41 overlap of Price et al. (2021) as identified by name in that lane; the
  identification and the RC41 masses were not re-checked here.
- **v3.1:** Desmond (2023) is converted as published; whether his inference used SPARC's tabulated Hubble-flow distances
  as prior centres (the text says it "starts from SPARC's tabulated distances") was not checked in the body of the paper.
- **v3.1:** the statement that the ACE and Stripe82 sources use their own conversions comes from CFG224b's README (which read
  the arXiv HTML tables); the 0.2–0.7 dex bracket is CFG224b's committed output, not re-derived.
- **v3.1:** body-level statements carried over from v2/v3 and not re-read: Jeanneau+26's 70 per cent gas share, Übler+17's
  −0.44/−0.27 dex, Vărăşteanu+25 Table 3 and the K_s median 0.35, Marasco+25's 0.72, the OLAS M0717-02064 parameters.
- **v3.1:** the MNRAS rules in sections 3–4 and the current keyword list were not re-checked.
- **v3 (resolved in v3.2 by CFG305):** the published RC100 table differs from arXiv v1 in row 87 (refit) and our row-78 sigma0
  was a slip; Umehata+26's journal 870 um fit differs from v1 (no status change). FS+18 is still checked against arXiv v1 only.
- **v3:** the KURVS tables were not in the CFG287 audit (stated in the Data Availability statement).
- **v3:** CFG289's commit message and `data_assembly/rc100_provenance/README.md` say "10 rows" of log M_baryon; the files differ
  in 9 such cells (7 bulge + 2 typos; 9 + 2 + 1 + 5 = 17). The paper uses the count from the files (check S5h).
- **v3:** PAPER38 is cited as Zimmerman 2026b for its a0(z) content only, at v1.3 (DOI 10.5281/zenodo.23108862).
- The figure number of the MIGHTEE-HI radial acceleration relation in the published MNRAS version (the arXiv v1 HTML shows it as
  fig. 11; the repository's G099 lane calls it fig. 3). The manuscript does not quote a figure number.
- OUP announced an updated AI-disclosure policy on 2026-09-10; the policy page would not load during the check. Read
  it before submitting and adjust the Acknowledgements sentence if it asks for more detail (section 0).
- The charge in USD or EUR (only the GBP figure is on the journal's pages).
