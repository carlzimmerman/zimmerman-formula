# Explicit Strong-Coupling Bounds and Vacuum-Adapted Coercivity

Carl P. Zimmerman, Briar Creek Tech — version 1.0, October 28, 2026.

This is a standalone preprint about finite-lattice SU(N) Hamiltonians.
The manuscript states all normalizations and distinguishes proved results,
conditional comparisons, and open continuum obligations.

## Results and limits

- An explicit, dimension-independent finite-system perturbative criterion
  gives a lattice gap at least 3 g²/16 for g² ≥ 59.9 in three spatial
  dimensions, for the stated magnetic normalization and every N ≥ 2.
- A fixed-block bound in the actual interacting vacuum is uniform in
  exterior volume; it is not uniform in the size of an elimination layer.
- A metric-normalized Schur comparison transfers gaps subject to exact
  operator and form-domain hypotheses.
- Counterexamples explain the BDL intermediate counting correction and
  why an unweighted Schur operator or automatic oscillator closure is unsafe.

This work does **not** prove continuum Yang–Mills existence, a continuum
mass gap, or confinement. It makes no global novelty or priority claim.
The methods build on the sources cited in the paper.

## Files

- main.tex, sections/: full manuscript source.
- verification/verify_release.py, RESULTS.json: exact finite arithmetic.
- formal/: two optional Lean certificates and pinned dependency manifests.
- provenance/: selected historical notes and their original constants script.
- review/: source-specific AI-assisted review and reconciliation records.
- MANIFEST.json: SHA-256 hashes for every other file in this source archive.

The separately deposited PDF is the version of record for this release.
Historical notes retain their original notation and approximate threshold
displays; the manuscript's hypotheses and upward-rounded sufficient
thresholds govern the release.

## Build

With Tectonic installed, from this folder:

    tectonic main.tex

A normal LaTeX distribution can instead run pdflatex main.tex twice.
The build needs the standard packages named in the preamble, including
amsmath, amssymb, amsthm, mathtools, booktabs, microtype, xurl
and hyperref. Tectonic downloads missing standard resources on its first
run. No external shell-escape or executable code is used by the document.

## Reproduce finite checks

Python 3.9 or later, standard library only:

    python3 verification/verify_release.py

This rewrites verification/RESULTS.json with the new run's timestamp,
environment and results. Optional repository provenance may be unavailable
outside the original checkout; the exact acceptance predicates do not
depend on it. A changed timestamp/report hash after rerunning is expected.
These checks certify only the finite constants, inequalities, matrix
arithmetic and polynomial identities listed in the report.
They do not formally verify the analytic proofs.

For optional Lean checks, install the exact toolchain in formal/lean-toolchain,
then from formal/ obtain the pinned Mathlib dependencies and run:

    lake exe cache get
    lake env lean I19_ym1_bdl_threshold.lean
    lake env lean I21_ym1_combinatorics.lean

The original Lake manifest is retained for dependency provenance.
The original project's default library targets are not included and
are not needed for these direct file checks. The certificates cover
scalar inequalities, finite sets and a three-qubit calculation only.

## Provenance, review and license

Earlier qualitative spectral paper: https://doi.org/10.5281/zenodo.22895866

Versioned repository archive containing the underlying later notes:
https://doi.org/10.5281/zenodo.23169118

The release review is AI-assisted and is not independent human peer review.
The manuscript includes the AI assistance disclosure and outstanding
mathematical obligations. Source history is evidence of provenance, not
proof of novelty or external use.

Manuscript, TeX and scientific prose: CC BY 4.0, attributed to Carl P.
Zimmerman. Code and formal proof sources: AGPL-3.0-or-later, with full
license text in LICENSE-AGPL-3.0.txt. See LICENSES.md.
