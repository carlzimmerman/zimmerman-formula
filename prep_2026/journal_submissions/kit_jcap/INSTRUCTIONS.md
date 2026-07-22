# JCAP submission — click-by-click instructions

**Kit contents (this folder):**

| file | what it is | where it goes |
|---|---|---|
| `manuscript.tex` | LaTeX source (article class, JCAP-structured) | uploaded as source (or held until revision stage) |
| `manuscript.pdf` | compiled manuscript, 15 pp | the file you actually submit initially |
| `cover_letter.txt` | final cover letter | pasted into the submission form's "cover letter / comments to the editor" box |
| `INSTRUCTIONS.md` | this file | not uploaded anywhere |

JCAP accepts an **initial PDF-only submission in any single-column format** —
you do **not** need the official `jcappub.sty` template for the first round.
If the paper reaches acceptance/revision, reformat `manuscript.tex` with the
JCAP template (download from the JCAP author pages) at that stage; the
structure (title/abstract/keywords/numbered sections/numeric citations) is
already template-shaped so the port is mechanical.

---

## Step 0 — ORCID first (10 minutes, do this before anything)

1. Go to https://orcid.org and sign in as **0009-0008-3508-7982**
   (carl@briarcreektech.com).
2. Under **Works → Add → Search & link** (or "Add DOI"), attach the Zenodo
   deposits so the record is externally checkable before an editor looks:
   - 10.5281/zenodo.20737162 (a0(z) law + DESI)
   - 10.5281/zenodo.21440407 (cross-scale test, v2)
   - 10.5281/zenodo.21478568 (Rubin/LSST pre-registration)
   - 10.5281/zenodo.21403470 (MI field theory companion)
   - 10.5281/zenodo.21419735 (SPARC a0-line companion)
   - 10.5281/zenodo.21478981 (a0kit software)
3. Set employment/affiliation to "Briar Creek Tech" so the journal's
   ORCID-pull matches the cover page.

## Step 1 — arXiv (recommended first, but do NOT let it block the journal)

- Target category: **astro-ph.CO** (primary), cross-list **gr-qc**.
- Reality check: with no institutional email and no prior arXiv history in
  the category, you will need an **endorsement** for astro-ph.CO. What to do:
  1. Create/log in to your arXiv account (https://arxiv.org/user/register)
     using carl@briarcreektech.com, and link your ORCID iD
     (Account → Link ORCID).
  2. Start a submission; if arXiv asks for endorsement it shows you an
     **endorsement code**. Send that code with a short, factual note to a
     neutral acquaintance who already publishes in astro-ph.CO and has read
     the work. **Do not** ask anyone you might suggest (or who might serve)
     as a referee, and do not cold-email the field's big names for
     endorsement — that reads as lobbying.
  3. If no endorser is available within ~a week, **submit to JCAP anyway**
     (journal submission does not require arXiv) and post to arXiv later —
     a journal manuscript number, and eventually acceptance, makes
     endorsement/moderation easier. A delayed arXiv post is normal, not a
     rejection.
- If the arXiv post succeeds first, add the arXiv ID to the JCAP submission
  form and to the cover letter line "The work is not under consideration
  elsewhere" (e.g. "Preprint: arXiv:26MM.NNNNN").

## Step 2 — Create the JCAP account

1. Go to **https://jcap.sissa.it** (JCAP is run by SISSA Medialab with IOP
   Publishing).
2. Click **Login / Register** (top right) → **Create an account**. Use
   carl@briarcreektech.com. Affiliation: "Briar Creek Tech". Country: USA.
3. In the account/profile page, **link your ORCID iD**
   (0009-0008-3508-7982) — the site has an ORCID connect button; use it
   rather than typing the number, so the iD is authenticated.

## Step 3 — Submit

1. From your JCAP author area click **Submit a new article**.
2. Article type: **regular article**. Section: cosmology / dark energy.
3. Title: paste exactly the manuscript title (with the formula).
4. Abstract: paste the manuscript abstract (plain-text the math as needed).
5. Author: single author, Carl P. Zimmerman, Briar Creek Tech,
   carl@briarcreektech.com, ORCID 0009-0008-3508-7982 (should auto-fill from
   the linked profile — verify it appears).
6. Keywords: `modified gravity; dark energy equation of state; supernova
   type Ia - standard candles; redshift surveys; rotation curves of
   galaxies`.
7. Upload **`manuscript.pdf`** as the article file. (If the form insists on
   source, upload `manuscript.tex` too — it compiles standalone with no
   figure files.)
8. Paste **`cover_letter.txt`** into the cover-letter/comments field. Add
   this one referee-facing line at the top of the comments box (it is
   strategy, not part of the letter): *"Note for the editor: this is a
   pre-registered falsifiable-program article whose current verdict is
   honestly UNDECIDED; it is best served by a referee who evaluates test
   design and pre-registration methodology rather than expecting a
   detection."*
9. Suggested referees: keep them **topical, not personal** — test-design /
   dark-energy-phenomenology people. List none as excluded (you have no
   conflicts; requesting exclusions without cause reads badly).
10. Submit. Save the manuscript number the confirmation email gives you.

## Step 4 — Timeline and what to expect

- Acknowledgement + editor assignment: days.
- First referee report: typically **1–3 months** for JCAP. Silence for 8
  weeks is normal; a polite status query via the author area at ~10 weeks is
  fine.
- Realistic outcome for this paper: **major revisions or reject-and-resubmit
  on first pass. Expect it; it is not a verdict on the program.** An
  unaffiliated-author MOND-adjacent submission will get a skeptical referee;
  the manuscript is built for that reader (frozen protocol, both-ways
  bounds, committed scripts).

## Step 5 — On major revisions (the important part)

- **Iterate; do not withdraw.** Answer every referee point in a numbered
  response letter, quoting the referee verbatim, and where the referee is
  right say so and change the text. The calibration discipline (posited-not-
  derived, both footings, wellhead credit, UNDECIDED verdict) is
  non-negotiable — never "fix" a referee complaint by overclaiming.
- If the referee asks for the official template: port `manuscript.tex` into
  `jcappub.sty` (mechanical; the section structure already matches).
- If the referee asks for figures: the three planned figures are already
  reproducible from committed scripts (`desi_posterior_a0z.py`,
  `galaxy_a0z.py` + `bigwheel_update.py`, `forecast_rubin_a0z.py`) — note
  that `galaxy_a0z.png` as committed still carries the pre-v2 "clean, 1
  object" Big-Wheel label; regenerate the ladder figure with the v2
  transitional labeling (from `bigwheel_update.py` outputs) before including
  it in any revision.
- Only if two independent referees reject on **scope** grounds ("not novel
  enough for a full article"), fall back per the submission strategy:
  Phys. Rev. D (as a phenomenology paper) or MNRAS (as a methods paper) are
  the named alternates — but exhaust the JCAP revision cycle first.

## Bookkeeping after submission

- Record the manuscript number + submission date in
  `prep_2026/journal_submissions/` (append to SUBMIT_JCAP.md).
- Per SUBMISSION_STRATEGY.md Part 2: JCAP goes out ~4–8 weeks **after** the
  PRD submission is in and has a manuscript number, and the MNRAS data
  companion trails or runs parallel. Do not burst-submit all three the same
  week.
- One repo hygiene item this kit already fixed: the canonical
  `real_research/papers/A0Z_CROSSSCALE_2026.md` had two stray closing-tag
  lines after the references (now removed). If the Zenodo v2 deposit's
  attached `.md` carries the same artifact, upload a corrected file as a new
  Zenodo version at your convenience (the .tex/.pdf were clean, so this is
  cosmetic).
- A new traceability script `prep_2026/rubin_prereg/significance_vs_z.py`
  (reproduces the z-dependent significances quoted in Limitations item 1;
  exit 0, PASS) should be **committed to the repo before submission** so the
  "every quantitative figure is produced by a committed script" sentence in
  the cover letter is exactly true.
