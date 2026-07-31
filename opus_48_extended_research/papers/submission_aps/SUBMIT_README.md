# APS submission package — everything you need, in order

**Target journal: Physical Review D** (Particles, Fields, Gravitation, and Cosmology).
Short Regular Article, ~3 pages.

> **Not PRL.** PRL requires a claim of broad, high impact. This paper's own §II concedes that the
> coefficient is observationally indistinguishable from an existing published proposal, which is
> disqualifying for PRL and would be an instant desk reject. PRD is the correct venue and the honest one.

---

## 1. Before you submit — three things only you can do

| # | Action | Why it matters |
|---|---|---|
| 1 | **Supply the exact citation for the Karpathy tool.** In the `.tex` see `\bibitem{AutoresearchTool}` — it is a placeholder reading `[exact tool name to be supplied]`. | I could not verify the tool's name, author line or URL, and I will not invent a citation. A wrong reference in a methods section is exactly the kind of error that damages credibility with a referee. Fill in name + URL (and DOI if it has one). |
| 2 | **Verify the four references I flagged.** Items `Pikhitsa2010`, `Klinkhamer2011`, `Milgrom2020`, `Milgrom2022` — volume/page/arXiv numbers are from memory. | These sit in the prior-art section, which is the section doing the heavy lifting. A wrong volume number there looks like you haven't read the work you're crediting. |
| 3 | **Have one working physicist read §II.** | §II is what stops a referee saying "unaware of prior art." If it reads right to a specialist, the paper survives to review. |

---

## 2. Compile

```bash
pdflatex a0_half_dark_energy_rate.tex && pdflatex a0_half_dark_energy_rate.tex
```

REVTeX 4.2 ships with TeX Live and MacTeX. If `revtex4-2` is missing, install it or get it from
`https://journals.aps.org/revtex`.

---

## 3. Where to submit

**Portal:** `https://authors.aps.org/Submissions/`
Create an account, choose **Physical Review D**, then **New Submission**.

Upload the `.tex` source **and** the compiled PDF. APS wants source, not PDF only.

---

## 4. Metadata to type into the portal

**Title**
> The MOND acceleration scale is one half of the dark-energy gravitational rate

**Author / affiliation**
> Carl P. Zimmerman — Briar Creek Tech, Charlotte, North Carolina, USA
> (Corresponding author. Use whatever email you want on the public record — do not use a personal
> address you would rather not have indexed, since it appears on the published paper.)

**Manuscript type:** Regular Article

**Section / subject area:** Gravitation and Cosmology → *Cosmology* or *Modified gravity and dark
energy* (pick from the dropdown; the exact wording changes occasionally).

> **PACS numbers are not needed.** APS retired PACS in 2016. The portal asks you to pick subject
> categories from a menu instead.

**Suggested keywords:** MOND; acceleration scale; dark energy; cosmological constant; radial
acceleration relation; galaxy rotation curves.

**Suggested referees (optional, and I would supply them):** anyone who works on the MOND acceleration
scale and its cosmological coincidence will judge this fairly and quickly. Naming people who know the
Milgrom 1999/2020 literature is *in your interest* — they will confirm you have credited it correctly
rather than suspect you haven't.

**Opposed referees:** leave blank unless you have a specific reason.

---

## 5. Licence / copyright

At acceptance APS asks you to choose:

- **Standard:** transfer copyright to APS. Free. This is the default and is fine.
- **Open access (CC-BY):** requires an article-processing charge. Optional. Check the current fee on
  the APS site — I am not going to quote a price I can't verify.

You may post the submitted version to arXiv either way; APS permits this.

---

## 6. AI disclosure — already handled, but know why

APS policy is that AI tools **cannot be authors** and that their use must be **disclosed**. The
manuscript has a dedicated *Disclosure of AI assistance* section stating that you directed the work,
reviewed every load-bearing calculation, and take full responsibility, and that no AI system is an
author. That satisfies the requirement.

> Two notes. First: **verify the current wording of APS's AI/ethics policy on their site before you
> submit** — policies in this area are being revised often and I would rather you read the live version
> than trust my summary. Second: **you do not need a special "AI-friendly" journal.** Essentially every
> reputable venue accepts AI-assisted manuscripts with disclosure. Anything advertising itself as
> accepting AI-generated papers is a paper mill and would cost you more credibility than it buys.

---

## 7. arXiv (do this too, and ideally first)

Post to **arXiv** under `astro-ph.CO` with cross-list to `gr-qc`. You may need an endorsement for
`astro-ph.CO` if you have not posted there before — the arXiv system will tell you and will name
eligible endorsers.

Posting to arXiv first is standard, timestamps your priority, and does not affect PRD submission.

---

## 8. Cover letter

Use `COVER_LETTER.md` in this directory. Paste it into the portal's cover-letter box (plain text).

---

## 9. Honest expectation, stated once

The realistic outcomes at PRD, in order of likelihood:

1. **Referee asks for more content.** The paper's central claim is one rational coefficient in an
   otherwise known coincidence, and §II concedes it cannot be distinguished from `cH_Λ/2π`. A referee may
   well say "this is a restatement with a different O(1) factor." The defence is Eq. (1)'s closed form
   plus the falsifiable `a_0(z)` law of §VI — which is why that section is in the paper.
2. **Accepted as a short note** after revision.
3. **Rejected as insufficiently novel.**

Two things make outcome 3 less likely, and both are already done: the prior art is conceded *first*,
before the numbers, and the liabilities are handed over in §VII rather than left for a referee to find.
Papers get rejected far more often for appearing to overclaim than for having a modest claim honestly
stated.

If it is rejected on novelty, the natural next move is to bundle Eq. (1) with the modified-inertia
material (the covariant action and the structural theorems) into a longer PRD paper where the
coincidence is one section rather than the whole argument. Say the word and I will assemble that.
