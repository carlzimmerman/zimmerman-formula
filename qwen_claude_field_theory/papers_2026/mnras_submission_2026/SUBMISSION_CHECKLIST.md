# MNRAS submission package — checklist (prepared 2026-09-06)

Everything in this directory is what the journal asks for. Items marked **[you]** need the author; everything else is done.

## 1. What is in this directory

| file | role |
|---|---|
| `mnras_a0_lambda_coefficient.tex` | the manuscript, MNRAS class (`mnras.cls` v3.0, `usenatbib`, `fleqn`), 7 pages typeset |
| `references.bib` | 44 references, natbib/`mnras.bst` style |
| `fig1_kappa_h0.pdf`, `fig2_fourform.pdf`, `fig3_dr4_rule.pdf`, `fig4_a0z.pdf` | the four figures (vector PDF, one- and two-column widths) |
| `make_figures.py` | regenerates the figures from the stated formulas and committed numbers; asserts the H₀-lock ratio (0.998), the 155 a₀ switch-off and the 2 kAU shift |
| `mnras_a0_lambda_coefficient.pdf` | the compiled manuscript (upload as the "PDF for review" and also the source) |
| `COVER_LETTER.md` | cover letter text for the ScholarOne field |
| `SUBMISSION_CHECKLIST.md` | this file |

Rebuild: `tectonic mnras_a0_lambda_coefficient.tex` (fetches `mnras.cls` and `mnras.bst` from CTAN automatically), or `pdflatex; bibtex; pdflatex; pdflatex` with the MNRAS class installed. Regenerate figures: `python3 make_figures.py`.

## 2. Before you upload — the author's items

- **[you] E-mail.** Replace the `\thanks{E-mail: to be inserted ...}` text in the `.tex` with your e-mail (MNRAS requires a corresponding-author e-mail in the author block). Recompile.
- **[you] Affiliation line.** `Briar Creek Tech, USA` — add a city/state if you want it on the paper.
- **[you] Read every sentence.** The manuscript was drafted with AI assistance and states so. You are the author of record; the referee will address you. In particular check that you are comfortable with: Section 2's account of the two κ estimators and their H₀-convention shifts (from `real_research/reviews/kappa_h0_convention_audit_2026.py`), Table 1, the against-interest statements in Section 6.1, and the Acknowledgements disclosure.
- **[you] Two bibliography entries are flagged `verify before submission`** in `references.bib`: `Singh2026` (arXiv:2601.04290; the title is as recorded in the repository's prior-art ledger) and `Jeanneau2026` (arXiv:2603.28856; title from the data ledger). Open both arXiv pages and correct title/authors if needed. All other entries carry DOIs.
- **[you] Suggested referees (optional).** ScholarOne asks for them; none are named here on purpose.
- **[you] ORCID.** 0009-0008-3508-7982 is in the cover letter; link it in your ScholarOne account so it appears on the paper.

## 3. Submitting (ScholarOne)

1. Go to https://mc.manuscriptcentral.com/mnras and create or log into an author account (use the ORCID login option so the ORCID is attached).
2. "Submit a manuscript" → article type **Main Journal** (this is 7 pages; MNRAS Letters is capped at 5 pages and would need cutting Sections 3.3–3.4 and 6.2).
3. Title, running head (short title is set in the `.tex`: "The coefficient of the a₀–Λ relation"), abstract (paste from the `.tex`; it is under the 250-word limit), keywords: `gravitation -- dark energy -- galaxies: kinematics and dynamics -- cosmological parameters -- binaries: visual -- galaxies: high-redshift` (six, all from the MNRAS keyword list).
4. Upload files: the `.tex` and `.bib` as **Main Document** source, the four figure PDFs as **Figure** files (name them as in the `.tex`), and the compiled PDF. ScholarOne builds its own review PDF; check it.
5. Cover letter: paste `COVER_LETTER.md`.
6. Declarations you will be asked for (answers prepared):
   - **Originality / not under consideration elsewhere:** yes; Zenodo preprints of parts exist (cited in the paper), which MNRAS permits.
   - **Conflicts of interest:** none.
   - **Funding:** none.
   - **Data availability:** the statement is in the manuscript (public GitHub repository + Zenodo DOIs; SPARC public; El-Badry catalogue Zenodo 4435257).
   - **Use of AI tools:** MNRAS/OUP policy requires disclosure of generative-AI use in the preparation of the manuscript and does not permit AI tools as authors. The Acknowledgements section discloses it; tick the corresponding box and repeat the sentence in the cover letter (already there).
   - **Licence:** MNRAS standard licence to publish (no charge) or Open Access (APC applies; RAS/OUP read-and-publish agreements cover some institutions — Briar Creek Tech will not be covered, so standard licence unless you want OA).
   - **Page charges:** none for MNRAS; colour figures are free online.
7. Submit. You will receive a manuscript ID (MN-26-XXXX). Typical first-referee turnaround is 4–10 weeks.

## 4. What to expect from a referee, and where the manuscript already answers it

- *"The zero-mode result is elementary."* The paper says so itself (Section 3.2) and states why it is worth writing down: the programme's own literature and some entropic derivations implicitly assumed otherwise. The content is the two repairs (3.3, 3.4) and the four-form reframing (4), not the theorem.
- *"Prior art: Milgrom 1999, Blanchet & Le Tiec, Klinkhamer & Kopp."* Cited in the Introduction with their coefficients; Table 1 shows the excluded ones. The paper claims no derivation.
- *"The κ measurements are model-dependent (kernel, Υ, distances)."* Section 2 gives the floor, the Υ relocation, and the H₀-convention range explicitly; the referee is being handed the caveats, not hiding them.
- *"The four-form section is a construction, not a theory."* Stated in Section 4 and the Discussion; its one computed prediction (the 2 kAU shift) is what makes it more than a remark.
- *"Pre-registrations are not results."* The DR4 pre-registration is a hash-stamped public document with a frozen pipeline that has been run end to end; the z ≈ 2.5 test is defined with gates and a statistic. MNRAS has published forecast/test-design papers; the cover letter frames them as the paper's third contribution, not its only one.
- *"The framework has no dark sector / cosmology."* Acknowledged in the Discussion; the tests are coefficient-blind and independent of it.
- *"Why not arXiv?"* MNRAS does not require an arXiv posting. If you want one, you need an endorsement in astro-ph.GA or gr-qc; the accepted MNRAS version can be posted after acceptance under the journal's green-OA terms.

## 5. After submission

- Do not modify `PREREGISTRATION_DR4.md` or any `*_HASH.txt` while the paper is under review (the paper cites Amendment 11 by its hash).
- If the referee asks for changes to numbers, change the scripts first, re-run, then the text; keep the `.out` files committed.
- When DR4 lands (December 2026), the paper's Table 2 is the scoring rule; the result goes into a follow-up, not a revision of this paper.
