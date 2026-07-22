# MNRAS Submission — click-by-click instructions

**Kit contents (this folder):**

| File | What it is | Where it goes |
|---|---|---|
| `manuscript.tex` | MNRAS-class LaTeX source (mnras.cls, compiles clean with tectonic/pdflatex) | Upload at ScholarOne as "Main Document (TeX/LaTeX)" — optional at initial submission |
| `manuscript.pdf` | Compiled 8-page manuscript | Upload as the main document PDF (initial submission is format-flexible; this single PDF is sufficient) |
| `cover_letter.txt` | Final cover letter | Paste into the ScholarOne "Cover Letter" text box (or upload as a file) |
| `INSTRUCTIONS.md` | This file | Do not upload |

The manuscript is a reformat + calibration pass of the published Zenodo record
(DOI 10.5281/zenodo.21419735). Science content is identical; do not edit
numbers by hand — if anything must change, change the source paper and its
committed scripts first.

---

## Step 0 — ORCID (do this first, ~5 min)

1. Go to https://orcid.org/signin and sign in to the record
   **0009-0008-3508-7982** (this is the ORCID used in the manuscript and
   cover letter — do not create a second record).
2. Check the record shows your name and (optionally) Briar Creek Tech as
   employment. Public visibility for name is enough.
3. MNRAS **requires** an ORCID for the submitting author, and ScholarOne
   will ask you to authorize the link (Step 2.4).

## Step 1 — arXiv first (recommended, not required)

Posting to arXiv (**astro-ph.GA** — this is a galaxy-dynamics measurement
paper, not gr-qc) before journal submission is standard practice and lets
referees see a citable preprint.

**The endorsement hurdle:** new arXiv submitters to astro-ph.GA need an
*endorser*. What to do:

1. Create an account at https://arxiv.org/user/register with
   carl@briarcreektech.com.
2. Start a submission to astro-ph.GA; if arXiv asks for endorsement it will
   give you a **6-character endorsement code** and a link to send.
3. Send that code with a short, factual note to a professional contact who
   has published in astro-ph — the physicists from the 2026 email survey
   who replied substantively are the natural people to ask. Ask plainly:
   "Would you be willing to endorse me for astro-ph.GA? Paper attached;
   endorsement code X." Attach `manuscript.pdf`. Do not oversell; the
   paper's calibration speaks for itself.
4. If no endorsement materializes, **skip arXiv and submit anyway** — the
   Zenodo preprint (DOI 10.5281/zenodo.21419735) already provides public
   timestamped access, and MNRAS does not require an arXiv posting.
5. If the arXiv posting succeeds, put the arXiv ID into the reserved line
   in `cover_letter.txt` (marked `[arXiv ID: ______]`); if not, delete that
   bracketed clause before submitting.

Upload to arXiv: use `manuscript.tex` (arXiv compiles LaTeX itself; mnras.cls
is accepted — include it in the upload if arXiv's autocompiler asks for it;
it is on CTAN as the `mnras` package).

## Step 2 — Create the ScholarOne account

1. Go to **https://mc.manuscriptcentral.com/mnras**
2. Click **Create An Account** (top right).
3. Use **carl@briarcreektech.com** (the manuscript's contact address — keep
   these consistent).
4. Institution: enter "Briar Creek Tech (independent researcher)". There is
   no requirement to have a university affiliation.
5. When prompted, click **"Associate your existing ORCID iD"** and authorize
   with the 0009-0008-3508-7982 record. This must be done before submission
   can complete.

## Step 3 — Submit

1. Log in → **Author Centre** → **Start New Submission** → "Begin
   Submission" for a Main Journal article.
2. **Type:** Original Article.
3. **Title:** Reading the cosmological constant from gas-rich dwarf rotation
   curves: the a0-line and its systematic floor
4. **Abstract:** copy-paste from the PDF (it is 233 words, inside the
   250-word limit).
5. **Keywords:** pick from the MNRAS list to match the manuscript's keywords:
   gravitation; dark matter; dark energy; galaxies: kinematics and dynamics;
   galaxies: dwarf; methods: data analysis.
6. **Authors:** just you; ORCID should auto-fill from the account link.
7. **Files:**
   - `manuscript.pdf` as **Main Document**. Initial MNRAS submission is
     format-flexible: a single self-contained PDF is explicitly acceptable;
     full mnras.cls source is only needed at the revision/acceptance stage
     (and you already have it: `manuscript.tex`).
8. **Cover letter:** paste `cover_letter.txt` into the cover-letter field.
9. **Data availability:** the manuscript contains a "Data and Software
   Availability" section (SPARC public data; the self-verifying GitHub repo;
   a0kit Zenodo DOI 10.5281/zenodo.21478981; preprint DOI
   10.5281/zenodo.21419735). If the form asks separately, restate that
   section.
10. **Suggested reviewers:** ScholarOne asks for names. Suggest researchers
    in galaxy dynamics / RAR systematics / MOND phenomenology who are NOT
    SPARC co-authors (Lelli/McGaugh/Schombert are the data providers — fine
    as reviewers if the editor picks them, but suggesting them yourself
    looks like conflict). Reasonable pool to pick 3-4 from:
    - Harry Desmond (Portsmouth) — RAR statistics and systematics
    - Benoit Famaey (Strasbourg) — MOND phenomenology reviews
    - Kyu-Hyun Chae (Sejong) — rotation-curve tests of MOND
    - Indranil Banik (St Andrews/Portsmouth) — MOND tests
    - Tobias Mistele (Case Western) — MOND theory + rotation curves
    Add a note in the "comments to editor" that the systematic budget
    (Section 4) is the part most in need of scrutiny.
11. Review the PDF proof ScholarOne builds, tick the originality/single-
    submission declarations (both true: Zenodo/arXiv preprints do not count
    as prior publication under MNRAS policy), and **Submit**.

## Step 4 — What happens next (expectations)

- **~1-2 weeks:** an editor/assistant editor is assigned; possible desk
  triage. The calibrated cover letter and reproducibility statement exist
  precisely to survive this step.
- **~1-3 months:** first referee report.
- **Most likely outcome: major revision.** For a paper in this territory
  from an independent author, a long, demanding first report is the GOOD
  outcome — it means it was refereed, not desk-rejected. **Iterate; do not
  withdraw.** Answer every point, in both directions (concede what is true,
  push back with committed scripts where the referee is wrong). The
  referee-anticipation memo in `../SUBMIT_MNRAS.md` (Part 2, R1-R10) has
  pre-drafted honest answers to the ten hardest expected attacks — start
  every response from there.
- If rejected with referee reports: fix what is real, then the fallback
  chain is MNRAS → A&A → PASA (per `../SUBMISSION_STRATEGY.md`). Do not
  burn venues by resubmitting unchanged.

## Notes / deviations

- **Compiler:** the PDF in this kit was compiled with tectonic (XeTeX
  engine) against the CTAN `mnras` class, exit 0, no undefined references.
  It also compiles with standard pdflatex on any TeX Live that has the
  `mnras` package (Overleaf: set class to mnras, works out of the box).
- **Figures:** the initial submission is text+tables, matching the published
  Zenodo record (which has no embedded figures). If the referee or editor
  asks for figures, the four planned panels already exist as committed
  outputs: `prep_2026/a0_line/fire_slope_fig.png` (the a0-line),
  `fire_linearity_fig.png` (the rival-kernel fingerprint),
  `fire_lambda_fig.png` (the Lambda-inversion), plus the budget table as a
  forest plot (build from Table 2). Add them at revision with proper
  captions rather than delaying the initial submission.
- **Table 3** carries a per-row sigma_lnLambda column (0.32 full-gas, 0.26
  TRGB) — this matches `est_gls_results.json` (s_ln_lam = 0.257 for the
  TRGB set) and fixes the blanket-caption drift the adversarial re-review
  flagged. Do not "simplify" it back to a single 0.32.
