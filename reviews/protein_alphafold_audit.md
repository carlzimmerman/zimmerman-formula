# The "high AlphaFold scores" — what they are, and what they are not

**v12 · 2026-05-31 · audit of the Z² biotech / AlphaFold claim**

## The claim

`extended_research/biotech/`: peptide ligands were designed with aromatic residues "spaced at
Z² intervals," then scored with **AlphaFold-Multimer ipTM** (interface pTM). The headline
numbers (`BIOTECH_PEER_REVIEW.md`):
- **ipTM = 0.92** for a C2 homodimer,
- **ipTM = 0.82** for TNF-α.

These are "high confidence" interface scores (ipTM > 0.8). They are **genuine AlphaFold
outputs** — that part is real and I concede it.

## Why they are not evidence *for Z²*

1. **No Z² control.** Nowhere is it shown that peptides *not* spaced at Z² intervals score
   *lower*. Without that control, a high ipTM is attributable to AlphaFold's general behavior on
   designed peptides, not to the Z² spacing. This is the same flaw as the parity-4PCF "2/2": a
   number with no null/control carries ~no evidential weight for the specific hypothesis.
2. **The "symmetry dependence" IS an AlphaFold artifact, not a Z² discovery.** The repo's own
   peer-review note flags that C2 homodimers score higher (0.92) than the asymmetric TNF-α
   target (0.82). AlphaFold-Multimer is *known* to be over-confident on **symmetric homodimers**
   — symmetric interfaces are over-represented in the PDB training set and are the easy case. So
   the score ordering reflects AlphaFold's symmetry bias, which has nothing to do with Z².
3. **ipTM is a weak, over-confident proxy for real binding.** For *de novo designed* binders the
   literature (e.g. Bennett et al. 2023) shows AlphaFold-Multimer ipTM correlates poorly with
   experimental binding — high-ipTM designs routinely fail in the lab; you need the "initial
   guess" protocol and, ultimately, wet-lab validation. A high ipTM is a filter, not a result.

## What the repo's OWN honesty docs already say (and they are right)

`Z2_PROTEIN_RESEARCH_SEPARATION.md` (Carl, April 2026) already concluded:
- **De novo design FAILED completely: 0/375 sequences folded.**
- **Structure prediction ~48–55% Q3** (`bruteflow`: 24–83%, avg 48.6%) — *at or below* the 1974
  Chou–Fasman ceiling; "Z² as a competitive predictor" is **RETRACTED**.
- The 8D-manifold `d_eff` score was **RETRACTED as a tautology** (d_eff→8 for all proteins).
- The M4 pipeline's value: "Novel physics contribution: **None**" — it wraps ESMFold + pLDDT +
  MM/PBSA + ADMET (all standard tools). The pLDDT/AlphaFold *scores come from those tools, not
  from Z².*

So the framework's own assessment already says the high scores are AlphaFold's, not Z²'s. This
audit agrees and adds the technical reasons (no control; symmetry bias; ipTM ≠ binding).

## The Z²-specific protein claims, briefly (same pattern as the constants)

- **Backbone dihedral angles** "derived" as θ_Z²×(−11/6, −9/6, −25/6, +26/6): four *chosen
  rational* coefficients tuned to hit four well-known angles (−57°, −47°, −129°, +135°) that
  carry wide error bars (±7–15°). One free rational per angle = a fit, not a derivation —
  identical to α⁻¹=4Z²+3.
- **Normal-mode "resonance" p<10⁻²⁴** (modes near n/Z²): an implausibly large significance from 4
  proteins. The harmonics n/Z² are *dense* (spacing ~0.03), so *any* frequency lies near some n;
  the p-value almost certainly does not account for harmonic density / unit choice. A classic
  dense-comb artifact, not a 24-sigma physics detection.

## Bottom line

The high AlphaFold ipTM scores (0.92, 0.82) are **real AlphaFold numbers, produced by AlphaFold
doing AlphaFold things on designed symmetric peptides** — over-confident on symmetry, uncontrolled
for Z², and a weak proxy for actual binding. They are **not** evidence for the Z² framework, and
the repo's own April-2026 separation already retracted the Z²-as-predictor claim and called the
pipeline "no novel physics." Same lesson as the parity-4PCF and the constants: a high score with
no control or null is not a result. (The one genuinely worth-publishing-on-its-own item, per the
repo, is the *AlphaFold symmetry-dependence* observation — which is a statement about AlphaFold,
not about Z².)
