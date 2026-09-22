# Source checks for YM-C1-RG-1

Checked 2026-09-22. Scope: whether an existing primary result supplies the
vacuum-subtracted spectral comparison needed to transport I15 to weak
coupling and the continuum. This is an application check, not a global
novelty search. No recent claimed Clay proofs were used as evidence.

## Chatterjee: theorem statement and application checked

- Sourav Chatterjee, *A probabilistic mechanism for quark confinement*,
  [arXiv:2006.16229v5](https://arxiv.org/pdf/2006.16229v5), 26 March 2021,
  35 pages; published CMP 385 (2021), 1007--1039,
  DOI [10.1007/s00220-021-04086-y](https://doi.org/10.1007/s00220-021-04086-y).
- Authentication: arXiv's version history and the version stamp on PDF p.1.
- Exact source: section 2.1 (pp.3--4), Definition 2.3 and Theorem 2.4
  (p.7), together with the qualification on pp.7--8.
- Source hypotheses: `G` is a closed connected subgroup of `U(n)`,
  `d>=2`, with fixed coupling `beta`. A source-local function at edge `e`
  depends only on links sharing a plaquette with `e`; distance means
  distance between the two supporting edge midpoints.
- Source theorem: if all such `[-1,1]`-valued functions have exponential
  covariance decay uniformly under all cube boundary conditions, center
  symmetry is unbroken. For irreducible
  representations nontrivial on the center, every Gibbs state satisfies a
  rectangular Wilson-loop area law.
- Translation: source `d=4` is Euclidean spacetime; I15 `d=3` is spatial.
  Source `beta` is the coefficient of unnormalized `Re Tr` in a classical
  Gibbs specification. It is not the coefficient of the canonical
  quantum Hamiltonian without a separate anisotropic transfer-matrix
  dictionary. Decay constants may depend on `G,beta,d`.
- Application verdict: **does not supply the missing estimate**. I15's
  gap in the canonical physical state does not establish the source's
  all-boundary covariance assumption, weak-coupling control, or continuum
  uniformity. The theorem's direction is clustering to confinement.
- Classification: adjacent conditional implication; not a solution to the
  current spectral transport obligation.
- Retention: PDF read through the primary web source; no local PDF cache
  retained, so no PDF SHA-256 claimed. No independent reconstruction of
  the 35-page proof is claimed.

## Balaban: authenticated paper, exact theorem unverified in this run

- Tadeusz Balaban, *Large field renormalization. II. Localization,
  exponentiation, and bounds for the R operation*, CMP 122 (1989),
  355--392. Published September 1989; revised 10 June 1988.
- Primary publisher locator:
  [10.1007/BF01238433](https://link.springer.com/article/10.1007/BF01238433).
  Author-institution bibliographic corroboration:
  [Rutgers repository](https://scholarship.libraries.rutgers.edu/esploro/outputs/journalArticle/Large-field-renormalization-II-Localization-exponentiation/991031665237504646).
- The publisher identifies Theorem 1 as its ultraviolet stability result,
  but the accessible page contains abstract and metadata rather than the
  theorem's hypotheses and statement. That is insufficient to authenticate
  a detailed theorem extraction.
- Exact-source attempts: publisher PDF endpoint returned the subscription
  article page; Project Euclid's volume/issue endpoint returned a short
  challenge page rather than its archive; INSPIRE's DOI record had no
  document URL; an archive search endpoint failed; the ICM proceedings
  candidate exceeded the web reader's size limit. None establishes a
  mathematical obstruction.
- Existing project source-cache lookup by exact DOI found no cache.
  A scoped filename search found no retained local Balaban PDF.
- Verdict: **exact theorem unverified; not a proof dependency**. This run
  cannot assert that Balaban supplies the required Schur-metric coercivity,
  terminal strong-coupling comparison, or a uniform weak-coupling mass gap.
  The report's elementary partition-function example is independent of
  the inaccessible theorem.
- Retention: no primary PDF obtained, so no cache hash or extraction claim.

## Search boundary

Discovery used exact author/title/DOI queries, publisher and Rutgers
records, arXiv, INSPIRE, and Project Euclid. The Chatterjee result was
checked in a pinned primary PDF, not inferred from an abstract. For
Balaban, bibliographic authentication succeeded and theorem extraction
did not. Search snippets, secondary commentary, and claimed new solutions
were excluded from load-bearing evidence. No claim of novelty is made
for the elementary spectral/error-budget lemmas.
