# Submission Strategy — three-journal package for the de Sitter–Unruh modified-inertia program

**Author:** Carl P. Zimmerman (Briar Creek Tech; independent, no academic affiliation) · carl@briarcreektech.com
**Prepared:** 2026-07-21
**Scope:** coordinates the three editor-facing packages — `SUBMIT_PRD.md`, `SUBMIT_JCAP.md`, `SUBMIT_MNRAS.md` — into one submission plan.

This document does not restate the physics; it governs *how and in what order* the three manuscripts go out, how to firewall the overlap between them, and the one honesty rule that binds all three. The governing constraint throughout: an unaffiliated author submitting into modified gravity — a field with heavy amateur/crank traffic — must be impeccably calibrated (bold where earned, bounded where honest, falsifiable), and must never re-assert the publicly-retracted TOE/SM/derived-$a_0$ overclaims.

---

## PART 1 — DISTINCTNESS CHECK (self-plagiarism / salami-slicing firewall)

### 1.1 The three core results are genuinely different

| | PRD | JCAP | MNRAS |
|---|---|---|---|
| **Kind of paper** | Formal field theory + no-go theorem | Cosmological prediction + pre-registered test | Galaxy-dynamics data measurement |
| **Core result** | A covariant, ghost-free *modified-inertia* action (passive frame, 0 propagating dof) + an obstruction theorem: passive-kernel $a_0$ and single-metric MOND lensing cannot coexist ($D\wedge S\Rightarrow\lnot L$) | The parameter-free, $Z$-independent ratio $R\equiv a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}$, and a hashed pre-registered two-scale test of it | The exact identity $E=g_{\rm obs}^2-g_{\rm bar}^2=a_0\,g_{\rm bar}$, a gas-dominated SPARC slope measurement $\hat a_0=(0.84\text{–}1.36)\times10^{-10}$, and the $\Lambda$-inversion to within $\sim2\times$ Planck |
| **Primary evidence** | Symbolic proofs, Dirac dof count, truth table | DESI DR2 $w_0w_a$ posterior; Rubin/LSST forecast | Raw SPARC rotation curves |
| **Deliverable claim** | A theory-space structural statement | A falsifiable forward test (currently UNDECIDED) | A systematics-limited empirical box |
| **Fails if** | A term class outside the two lemmas is exhibited | $w\to-1$ (prediction dissolves) | A future gas-dominated slope near $3\times10^{-10}$ |

These are three distinct contributions in method, evidence base, and falsification condition. A theory paper, a cosmology-test paper, and a data paper is a normal and defensible three-venue split, not salami-slicing — provided the shared scaffolding below is handled openly.

### 1.2 Shared material that could trip a self-plagiarism / duplicate-submission flag

All three necessarily share four elements, and a suspicious referee who has seen a sibling paper (or the Zenodo deposits) could read the repetition as salami-slicing. The shared elements:

1. **The framework preamble** — $a_0=cH_\Lambda/Z$, $Z=\sqrt{32\pi/3}$, the de Sitter–Unruh MI reading, the kernel $\nu=\sqrt{1+1/y}$.
2. **The credit block** — Milgrom 1983/1999, AeST/Skordis–Zlosnik 2021, Limbach–Psaltis–Özel 2008.
3. **The honesty ledger** — $a_0$/$Z$/sign posited-not-derived; both cosmological footings carried; the retraction discipline.
4. **The two-footing fork** — $9.36\times10^{-11}$ vs $1.13\times10^{-10}$.

None of these is a *result*; each is context every paper legitimately needs. The risk is not the sharing — it is failing to *disclose* it. Two overlap hot-spots deserve specific attention:

- **PRD ↔ MNRAS: the relational $\sigma$-spread.** PRD names the non-adiabatic velocity-dispersion spread as the surviving MI≠MG discriminant (memo A10); MNRAS's held-back companion (Zenodo 21421896) is exactly that observable. **Firewall:** MNRAS already correctly keeps 21421896 out of the submission and cites it in one Discussion sentence; PRD must treat the $\sigma$-spread only as a named *pointer* (one sentence, cited to 21421896), never developing its phenomenology. Neither paper may present the $\sigma$-spread as its own result. As written, both comply — hold that line.
- **JCAP ↔ MNRAS: the two-footing fork and the BTFR/SPARC data.** JCAP uses the footing fork as an *evolution-law* choice (declining $\sqrt{\rho_{\rm DE}}$ vs rising $cHE(z)$) and touches SPARC only as the $z=0$ BTFR anchor; MNRAS uses the footing fork as a *value* normalization choice ($cH_\Lambda/Z$ vs $cH_0/Z$) measured on the SPARC RAR. These are different uses of the same fork on different observables — genuinely distinct, but the papers must **say so explicitly** so a referee does not see "the same two numbers twice." Add a one-line cross-reference in each (see 1.4).

### 1.3 Verdict

No true salami-slicing: no single result is split across two papers, and each paper's falsification condition is unique to it. The one genuine adjacency (the $\sigma$-spread) is already firewalled by keeping it out of both submissions as anything more than a cited pointer. The remaining risk is *cosmetic* (shared preamble reading as duplication) and is neutralized by transparent companion-citation, below.

### 1.4 The companion-citation firewall (mandatory in all three)

Each manuscript must contain a short **"Related work by the author"** note (in the introduction or a footnote, not hidden) that:

1. Names the other two submissions as companion papers in preparation/under review, one clause each, stating the *distinct* result of each so the boundary is explicit. E.g. in PRD: *"The cosmological $a_0(z)$ test (companion, JCAP submission) and the SPARC $a_0$-line measurement (companion, MNRAS submission) treat the phenomenology; the present paper is confined to the field-theory construction and the obstruction theorem."*
2. Cites the underlying Zenodo deposits by DOI as the timestamped preprint record, and states that these are the author's own prior deposits released for reproducibility — this is the standard preprint disclosure, not duplicate publication.
3. On the JCAP↔MNRAS footing adjacency, adds the one-line distinction: JCAP — *"the value-normalization fork (canonical vs $H_0$) is examined empirically in the companion SPARC measurement; here only the evolution-law footing is under test"*; MNRAS — the mirror sentence.

**Which Zenodo deposits each cites as companions** (from the three packages, consolidated):

- **PRD** consolidates 21403470 (+erratum 21415677), concept 21253644, 21418816, 20973740; cites (not consolidates) the JCAP-side 20737162 / 21440407 / 21478568 and the MNRAS-side 21419735 as companions.
- **JCAP** consolidates 20737162, concept 21440407, 21478568; cites (not consolidates) the field-theory 21403470 and the MNRAS-side 21419735 as companions; must *not* lean on the covariant completion.
- **MNRAS** submits 21419735 alone; cites 21421896 as a one-line companion (the $\sigma$-spread) and the PRD/JCAP deposits as companions.

Because the consolidation sets are **disjoint** (21403470/21253644/21418816/20973740 vs 20737162/21440407/21478568 vs 21419735), no Zenodo deposit is the primary source of two submissions. That disjointness is the cleanest single fact to state to any editor who raises duplication.

---

## PART 2 — SUBMISSION ORDER + TIMING

**Recommended order: PRD first, JCAP second, MNRAS third (MNRAS as the data companion, can trail or run parallel).**

### 2.1 PRD first — reasoning
- **Most referee-tested and most rigorous.** Its backbone (the no-go, 20973740) already survived an adversarial review; the field-theory results are machine-verified (Dirac closure, Herglotz kernel, truth table). It is the paper least exposed to "under-calibrated amateur" dismissal because its content is a *theorem and a construction*, checkable line-by-line, not a phenomenological fit.
- **It sets the honest frame for the whole program.** PRD's central move is to publish a result that *cuts against* the program's own most distinctive claim (single-metric MOND lensing is obstructed). Leading with the paper that most visibly refuses to overclaim establishes the author's calibration credibility before the two more data-contingent papers land. If a referee or editor later cross-reads, the first thing they find is self-critical rigor.
- **It is the least time-sensitive**, so it can absorb the longest review cycle without a data clock running against it.

### 2.2 JCAP second — reasoning
- It is a **forward, pre-registered** test with a live clock (Rubin/LSST calibrated SN sample, ~2027+). Getting the pre-registration into peer review *before* the deciding data exist is the entire point of a pre-registration — so it should not wait for the full PRD cycle to finish, but it benefits from PRD being on record first (it can cite the field-theory companion as "under review" and lean on the established calibration reputation).
- Its current verdict is honestly **UNDECIDED** ($2.0\sigma$), so there is no detection to rush; the value is the committed protocol. Submitting ~1–2 months after PRD (once PRD is at least under review with a manuscript number) is the sweet spot.

### 2.3 MNRAS third / parallel — reasoning
- It is the **cleanest standalone data paper** and the least dependent on the others, so it is the safest to run in parallel if bandwidth allows — but placing it third lets it cite both companions as established and inherit the calibration reputation.
- It is the natural **data companion** to JCAP (the $z=0$ SPARC anchor that JCAP's galaxy-side ladder rests on lives here), so JCAP-then-MNRAS lets JCAP point forward to it and MNRAS point back.
- If any single paper is likely to draw the "unaffiliated MOND author" reflex hardest, it is a measurement paper with a bold headline ($\Lambda$ from rotation curves). Sending it last, after two calibrated papers are on record, is the defensive play.

### 2.4 Timing summary
1. **PRD now** (most rigorous, sets the frame, no data clock).
2. **JCAP ~4–8 weeks later** (pre-registration clock favors sooner; wants PRD on record first).
3. **MNRAS third or parallel** (data companion; benefits most from two prior calibrated papers).

Do **not** submit all three the same week to three journals: a burst of three near-identical-preamble submissions from an unaffiliated author is the pattern editors associate with the crank-filter. Staggering with explicit companion citations reads as a coordinated research program instead.

---

## PART 3 — INDEPENDENT-AUTHOR PLAYBOOK

### 3.1 ORCID
- Register/confirm an **ORCID iD** and put it on all three cover pages and in all three arXiv submissions. For an unaffiliated author it is the single cheapest credibility signal — it links the Zenodo deposits, the arXiv posts, and the journal submissions into one verifiable identity and shows a coherent track record rather than a one-off.
- Ensure the Zenodo DOIs are attached to the ORCID record before submitting, so the "author's own prior deposits" disclosure is externally checkable.

### 3.2 arXiv-first and the endorsement reality
- **Post each paper to arXiv before (or at) journal submission.** All three journals (PRD, JCAP, MNRAS) accept and expect arXiv preprints; an arXiv ID on the cover letter is a strong normalcy signal and lets referees pull the paper independently.
- **Endorsement is the real friction for an unaffiliated author.** With no `.edu`/institutional affiliation and (presumably) no prior arXiv submissions in these categories, Carl will need an **endorsement** to post to `gr-qc`, `astro-ph.CO`, and `hep-th`. Plan for this explicitly:
  - The right primary categories: **PRD → `gr-qc`** (cross-list `hep-th`); **JCAP → `astro-ph.CO`** (cross-list `gr-qc`); **MNRAS → `astro-ph.GA`** (cross-list `astro-ph.CO`).
  - Endorsement is per-category, so posting PRD to `gr-qc` first and establishing a record can ease later `astro-ph` posts (arXiv auto-endorses once a category history exists).
  - **Do not** cold-email the suggested referees for an endorsement — that conflates two roles and looks like lobbying. Endorsement should come from a neutral acquaintance already publishing in the category, or via arXiv's endorsement-request mechanism to someone who has read the work. If no endorser is available, submit to the journal first; a journal manuscript number and eventual acceptance is itself an arXiv-credibility path, and some authors post post-acceptance.
  - Be prepared for the possibility that the first arXiv post is delayed pending endorsement; this is normal and is not a rejection. Do not let it hold up the *journal* submission, which does not require arXiv.

### 3.3 Cover-letter suggested referees + exclusions
- **Suggested referees** are already listed appropriately per package (PRD: Skordis, Woodard, Blanchet, Famaey, Zlosnik; MNRAS: galaxy-dynamics/SPARC-RAR/MOND-phenomenology specialists; JCAP: route to a test-design/pre-registration-literate referee). Keep them **topical, not personal** — suggest for expertise, and state "editors to select independently." Suggesting the field's leading experts (including those whose work the paper contends with, e.g. Skordis/Zlosnik for AeST) signals confidence, not evasion.
- **Exclusions:** Carl should list **no personal exclusions** unless there is a genuine, disclosable conflict (there is none — he has no affiliation, no collaborators, no rivals in the ordinary sense). Requesting exclusions without cause reads as defensiveness and is itself a mild crank-tell. If asked, the honest answer is "none."
- Across the three packages, avoid suggesting the **same** referee for two papers where possible, so the reviews stay independent; the natural expertise split (field-theorists for PRD, cosmologists for JCAP, galaxy-dynamicists for MNRAS) makes this easy.

### 3.4 Preempting the crank-filter (the through-line for all three)
The packages already do most of this; consolidated, the crank-filter countermeasures are:
1. **Reproducibility over authority.** Every load-bearing number reproduces from committed, exit-0 scripts; invite the referee to run them. This is stated in all three cover letters — keep it.
2. **State the retraction discipline once, plainly.** Each cover letter should note (as JCAP's and PRD's do) that earlier over-broad TOE/SM claims were publicly retracted and that the present scope is strictly the $a_0$ reframing. This *preempts* a referee who finds the earlier claims — owning it disarms it.
3. **Credit generously and early.** Milgrom, AeST, LPO2008 in the first two pages of each. An amateur over-claims originality; a calibrated author credits precisely.
4. **Bound both ways.** Every "works" is matched with a "here is the real limitation." The referee-anticipation memos are the strongest single crank-filter defense — where the honest answer is "yes, that's a real limitation," it says so. Do not let the manuscript-body tone drift more bullish than the memos.
5. **No banned register.** No proves/solved/confirms/definitive/TOE anywhere (theorem/no-go/obstruction as mathematical objects are fine).
6. **One institutional email, one affiliation line, ORCID, no other personal detail.**

---

## PART 4 — THE ONE CROSS-CUTTING HONESTY RULE

**In every one of the three papers, without exception:** the *value* of $a_0$, the normalization $Z=\sqrt{32\pi/3}$, and the coupling *sign* are **posited inputs, not derived** — state this at first mention and in the ledger/scope box; credit **Milgrom (1983/1999)** for the kernel $\nu=\sqrt{1+1/y}$ at the point of use, **AeST/Skordis–Zlosnik (2021)** for the covariant modified-*gravity* MOND-scale realization, and **Limbach–Psaltis–Özel (2008)** for the $a_0\propto\sqrt{\rho_{\rm DE}}$ coincidence; carry **both cosmological footings** on every $a_0$-valued number; and **never** use overclaiming register (proves/solved/confirms/definitive/TOE) or re-assert any derived-$a_0$/Standard-Model/theory-of-everything claim. The distinctive content that *is* claimed is only: the $cH_\Lambda/Z$ coefficient, the modified-*inertia* (not modified-gravity) reading and its covariant passive-frame completion, and the falsifiable $a_0(z)\sim\sqrt{\rho_{\rm DE}}$ law — nothing more.

---

## EXECUTIVE SUMMARY (6 lines)

1. **Three genuinely distinct results** — PRD = covariant MI action + lensing obstruction theorem; JCAP = the parameter-free $a_0(z)=\sqrt{\rho_{\rm DE}}$ pre-registered test; MNRAS = the SPARC $a_0$-line slope + $\Lambda$-inversion — no result is split across papers, so this is a program, not salami-slicing.
2. **Only cosmetic overlap** (shared preamble/credit/footing fork) plus one real adjacency (the $\sigma$-spread, PRD↔MNRAS); firewall it by keeping the $\sigma$-spread a one-line cited pointer in both, and disclosing companions explicitly — the three consolidation sets of Zenodo DOIs are disjoint, which is the clean fact to tell any editor.
3. **Order: PRD first** (most rigorous, adversarially-reviewed core, sets the honest frame), **JCAP second** (pre-registration clock, wants PRD on record), **MNRAS third/parallel** (cleanest data companion, inherits calibration reputation); stagger, never burst-submit.
4. **Independent-author playbook:** ORCID on everything; arXiv-first into gr-qc/astro-ph.CO/astro-ph.GA with endorsement planned (do not let it delay journal submission, do not solicit endorsement from suggested referees); topical suggested referees, no personal exclusions.
5. **Preempt the crank-filter** by reproducibility-over-authority, owning the public retraction up front, crediting generously, bounding both ways, and banning overclaim register.
6. **One binding honesty rule for all three:** $a_0$/$Z$/sign posited-not-derived, credit Milgrom + AeST + LPO2008, carry both footings, no overclaim — claim only the $cH_\Lambda/Z$ coefficient, the modified-inertia completion, and the falsifiable $a_0(z)$ law.

---

*File: `/Users/carlzimmerman/new_physics/prep_2026/journal_submissions/SUBMISSION_STRATEGY.md`. Governs `SUBMIT_PRD.md`, `SUBMIT_JCAP.md`, `SUBMIT_MNRAS.md`.*
