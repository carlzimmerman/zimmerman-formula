# Cover letter

Paste the text between the rules into the ScholarOne "Cover Letter" box. MNRAS asks that the cover letter does not
summarise the results; it is read by the Editorial Office only. It must carry the AI-use disclosure, the conflict of
interest statement and the declaration of earlier postings. Do not mention a fee waiver here (that request goes
separately to OUP; see SUBMISSION_CHECKLIST.md, section 3). `make_upload_bundle.py` writes a plain-text copy with
the signature block completed: it replaces [SIGNATURE] with the byline name and affiliation of the manuscript and the
ORCID from the git-ignored `author_private.tex`, and adds the e-mail.

**Two items are owner decisions (SUBMISSION_CHECKLIST.md, section 0).** (1) The earlier-postings paragraph exists in
two variants. `make_upload_bundle.py` keeps the one that matches the `\papersixfalse` / `\papersixtrue` line of the .tex
and drops the other: [PAPER6-REMOVED] is the default (the manuscript does not cite Zenodo 10.5281/zenodo.22559892),
[PAPER6-NOTE] keeps that citation with a note. (2) The AI-use paragraph was finalised from the author's statement of the
models used on 2026-10-02 and extended to ten named model families on 2026-10-05 (SUBMISSION_CHECKLIST.md, section 0); it
matches the Acknowledgements.

---

Dear Editor,

I submit the manuscript "The galactic acceleration scale and the cosmological constant: the coefficient on SPARC, and
what it takes to measure its redshift evolution" for consideration as a Paper in Monthly Notices of the Royal
Astronomical Society.

[PAPER6-REMOVED]
The manuscript is original, has not been published in a journal and is not under consideration elsewhere. Earlier
versions of parts of the work were posted by me on the Zenodo repository, which is not peer reviewed
(DOI 10.5281/zenodo.22833314 and DOI 10.5281/zenodo.23108862); both are cited in the manuscript, which states where its
results supersede them. A further note of mine on the same coefficient (DOI 10.5281/zenodo.22559892) contains an
earlier form of one of the estimators; it is not cited, because one of its sections has been superseded.
A separate note of mine on the MIGHTEE-HI catalogue (DOI 10.5281/zenodo.23142559) is cited for one comparison value.
[/PAPER6-REMOVED]
[PAPER6-NOTE]
The manuscript is original, has not been published in a journal and is not under consideration elsewhere. Earlier
versions of parts of the work were posted by me on the Zenodo repository, which is not peer reviewed
(DOI 10.5281/zenodo.22559892, DOI 10.5281/zenodo.22833314 and DOI 10.5281/zenodo.23108862). All three are cited in
the manuscript, which states where its results supersede them; the four-form section of the first is superseded.
A separate note of mine on the MIGHTEE-HI catalogue (DOI 10.5281/zenodo.23142559) is cited for one comparison value.
[/PAPER6-NOTE]

Use of AI tools. Generative AI tools were used in preparing this work, and the use is disclosed in the
Acknowledgements. Large language models (Anthropic's Claude, mainly through the Claude Code tool; OpenAI models;
DeepSeek; Zhipu AI's GLM; Alibaba's Qwen; Google's Gemini and Gemma; Tencent's Hunyuan; Moonshot AI's Kimi; and xAI's
Grok) assisted with writing code and analysis scripts, with literature checks, with transcribing and digitising
published data, and with drafting the text. Two model-produced inputs are named in the Acknowledgements (the digitised
MIGHTEE-HI points, DeepSeek; the rotation-curve compilation with fitted mass-to-light ratios, GLM); both were checked
against their sources by script. No AI tool is an author. I checked every result, have reviewed the entire content
and take full responsibility for it. All analysis code is public, every number is produced by a public script whose
checks can fail, and one command reproduces every number and figure.

Conflicts of interest: none. Funding: none.

Data and code are public; the Data Availability statement gives the repository and its tagged release, and the sources
of the public data used (SPARC; the published table of Nestor Shachar et al. 2023, compared with the journal and the
arXiv versions; the MIGHTEE-HI radial acceleration points, digitised from the figure of Vărăşteanu et al. 2025, whose
digitised values are in the repository; the tables of Price et al. 2021, Puglisi et al. 2023 and Lee et al. 2025; the
ALESS 122.1 measurements of Amvrosiadis et al. 2025, Calistro Rivera et al. 2018 and Dunne et al. 2022; the public per-galaxy products of the MUSE-DARK survey; and the published fits of Vărăşteanu et al. 2026).

I have no request to exclude particular editors or referees.

Yours faithfully,

[SIGNATURE]

---
