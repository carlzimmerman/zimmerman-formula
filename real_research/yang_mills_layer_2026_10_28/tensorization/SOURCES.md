# Source checks for the tensorization route

Date checked: 2026-10-28. No novelty claim or broad literature survey.

## [W] Exact conditional-variance tensorization input

- Liming Wu, *Poincaré and transportation inequalities for Gibbs measures
  under the Dobrushin uniqueness condition*.
- Annals of Probability **34** (2006), no. 5, 1960–1989.
- DOI: `10.1214/009117906000000368`.
- Exact inspected version: `arXiv:math/0611635v1`, 21 November 2006,
  electronic reprint of the published article.
- Primary source: <https://arxiv.org/pdf/math/0611635v1>.
- Locators: PDF pages 4–6; definition (2.3), Theorem 2.1 / inequality (2.4),
  Theorem 2.2 / inequality (2.7). The proof of Theorem 2.1 is on PDF pages
  8–12; the trivial measurable-space metric is expressly admitted on page 4.
- Cache lookup: exact version absent. Source inspected through the web PDF
  tool; no PDF retained in this agent's assigned write scope, no byte hash
  claimed. A read-only attempt to hash downloaded primary PDF bytes failed
  at DNS resolution in the shell network sandbox; no source bytes were written.
  Metadata and theorem text authenticated from the primary PDF.
- Implication verified: for a finite product of a common measurable spin
  space with the discrete metric, spectral radius of the actual Dobrushin
  matrix below one gives the approximate variance tensorization used in
  PROOF.md §2. Its second-moment assumption is automatic. Combining with the
  already proved local gradient gaps gives (4).
- Dictionary: source sites = selected equal-size link blocks; spin space =
  SU(N)^m; source conditional specification = actual ψ² conditional measure
  at fixed exterior; source λ1 is the heat-bath gap, not a quantum gap.
- Verdict: theorem translation **verified**; actual Yang–Mills hypothesis
  `sup_y r_sp(C(y))<1` **unproved**. No finite-range assumption is supplied
  or needed. The resulting Yang–Mills application is **conditional**.
- Overlap: Theorem 1 is a **formal corollary not stated** in these lattice
  gauge conventions; no novelty asserted.

## Otto–Reznikoff discovery, not a supporting leaf

The publisher metadata for Felix Otto and Maria G. Reznikoff,
*A new criterion for the logarithmic Sobolev inequality and two applications*,
JFA 243 (2007), 121–157, DOI `10.1016/j.jfa.2006.10.002`, was located.
Exact publisher full text returned HTTP 403. It is therefore **not used**
as a theorem source. PROOF.md §3 contains a complete Poincaré proof on compact
product manifolds; no Euclidean-to-compact or logarithmic-Sobolev translation
is assumed. No originality claim is made for that criterion.

## Project inputs (actual bytes read)

Paths below are relative to repository root.

- `real_research/papers/yang_mills_bounds_2026/sections/vacuum.tex`
  SHA-256 `45b33bb7448c25ba0323b38478febd63ccc34958271cd1869e5facd09df872e0`.
- `real_research/reviews/yang_mills_continuum_2026_09_22/layer/PROOF.md`
  SHA-256 `f3c0019709434127acb62a96c5ba6a0c731ebeb36e87bef3aae167bce02b494c`.

The assigned base revision was `5bb77f83c618cab437a705c7aa19d7fe0b7aead7`;
the shared checkout reported `9c9d980ba0a972f1661de3b64d8296ea7edd5af6`
when inspected. Claims are pinned to the actual artifact hashes above;
arrival order and the observed HEAD are not used to assert supersession.
