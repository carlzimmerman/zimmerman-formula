# Primary-source checks and provenance scope

Checked 2026-10-19 using the web reader. No remote full text was retained in
the repository or copied into this lane. The project-local authorized
literature cache was queried for `Sommerfeld` before acquisition and returned
zero matches. Source bytes were not downloaded or cached, so there is no
retained remote-file hash; stable source versions/locators are given below.

1. **S. Cassel, _Sommerfeld factor for arbitrary partial wave processes_,
   arXiv:0903.5307v1, 30 March 2009.** Official
   [versioned HTML](https://arxiv.org/html/0903.5307v1) and
   [versioned PDF](https://arxiv.org/pdf/0903.5307v1) were both opened.
   Checked Eqs. (22), (29), (44)-(45), plus the local S-wave production
   discussion after Eq. (12). Authentication: author/title/version/date
   identified on the official arXiv page; extraction: equations read from
   its HTML and PDF text. Application verdict **verified** for the Coulomb
   S-wave origin enhancement, with `M_Cassel=m`, `A_Cassel=alpha_G`,
   `beta=k/m`, and `x=alpha_G/beta=2eta`. His finite-range Yukawa
   approximation is not used. The identical-pair coefficient, bound weights
   and gravitational source cancellation are derived in this lane and
   are not attributed to Cassel. This check establishes no formation rate.

2. **I. J. Thompson, NIST Digital Library of Mathematical Functions,
   Chapter 33, online version 1.2.7 (2026-06-15).** Checked
   [33.2.5-6](https://dlmf.nist.gov/33.2#E5),
   [33.5.1](https://dlmf.nist.gov/33.5#E1), and
   [33.22(v)](https://dlmf.nist.gov/33.22#v). Authentication: official
   NIST domain, chapter author and displayed current version. Extraction:
   equations and hydrogenic-bound-state identification read directly.
   Application verdict **verified** for the Coulomb normalization and
   small-radius power. The attractive case uses DLMF's parameter equal
   to minus the positive `eta` in this lane. The normalized Laguerre
   residue is also derived explicitly and numerically integrated here.
   This is an official reference-work cross-check, independent of the
   research-paper source above, rather than an original attribution claim.

3. **NIST, 2022 CODATA recommended constants, complete ASCII table.**
   [Official table](https://physics.nist.gov/cuu/Constants/Table/allascii.txt),
   checked rows for Newtonian `G`, `G/(hbar c)`, `h`, and `hbar`.
   Application verdict **verified** for the declared constants and unit
   conversion. The experiment uses the tabulated central value
   `G=6.67430e-11 SI` and exact SI definitions for `h`, `c`, and eV. Printed
   numerical digits describe a deterministic computation of that declared
   central value; they do not assert smaller experimental uncertainty in G.

The digamma bound-sum identity, infrared cancellation, state preparation
formula, hard-wall lower bound, mass-source identity, and leading matched
contact estimate are project derivations. No external theorem was silently
used to upgrade them into a universal many-body or formation claim.
No novelty search or global overlap claim was attempted.

# Final proofreading

Scope: the new `GRAVITATIONAL_SPECTRUM.md` and this source record only.
Routine edits: checked display delimiters, variable definitions, citations,
units and separation of exact/leading/conditional statements.
Mathematical-token changes during proofreading: none.
Unresolved issues: local contact/source Wilson coefficients remain a stated
matching obligation; finite computation uses arbitrary precision rather
than certified intervals. Parent independent proof audit is separate.
Validation: bounded `run_002` completed; runner-v2 manifest validation passed.
