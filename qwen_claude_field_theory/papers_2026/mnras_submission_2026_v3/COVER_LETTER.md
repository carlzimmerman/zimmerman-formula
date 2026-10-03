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
[PAPER6-NOTE] keeps that citation with a note. (2) The AI-use paragraph names the tools as stated so far; it must be
finalised by the author (TODO-AI-DISCLOSURE).

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
[/PAPER6-REMOVED]
[PAPER6-NOTE]
The manuscript is original, has not been published in a journal and is not under consideration elsewhere. Earlier
versions of parts of the work were posted by me on the Zenodo repository, which is not peer reviewed
(DOI 10.5281/zenodo.22559892, DOI 10.5281/zenodo.22833314 and DOI 10.5281/zenodo.23108862). All three are cited in
the manuscript, which states where its results supersede them; the four-form section of the first is superseded.
[/PAPER6-NOTE]

Use of AI tools. Generative AI tools were used in preparing this work, and the use is disclosed in the
Acknowledgements. Large language models from several providers (Anthropic's Claude, mainly through the Claude Code tool;
OpenAI models; DeepSeek; Zhipu AI's GLM; Alibaba's Qwen; and Google's Gemini) assisted with derivations, with
transcribing and digitising published data, with writing the analysis code and with drafting the text. No AI tool
is an author. I have reviewed the entire content and take full responsibility for it. All analysis code is public,
each script contains checks that can fail, and one command reproduces every number and figure.

Conflicts of interest: none. Funding: none.

Data and code are public; the Data Availability statement gives the repository and its tagged release, and the sources
of the public data used (SPARC; the published table of Nestor Shachar et al. 2023, checked against the journal and the
arXiv versions; the MIGHTEE-HI radial acceleration points, digitised from the figure of Vărăşteanu et al. 2025, whose
digitised values are in the repository; the tables of Price et al. 2021, Puglisi et al. 2023 and Lee et al. 2025; the
public per-galaxy products of the MUSE-DARK survey; and the published fits of Vărăşteanu et al. 2026).

I have no request to exclude particular editors or referees.

Yours faithfully,

[SIGNATURE]

---
