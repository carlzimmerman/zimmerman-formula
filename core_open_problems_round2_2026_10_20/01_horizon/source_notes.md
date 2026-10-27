# Source authentication and predecessor credit

Access date: 2026-10-20 America/New_York (2026-10-21 UTC).
External sources below are primary papers. No novelty claim is made. The new
calculations are the explicitly stated transfers and audits in raw_derivation.md.

## External source used in this round

Shih-Yuin Lin and B. L. Hu, *New Insights into Uniformly Accelerated Detector in
a Quantum Field*, arXiv:gr-qc/0610024v1, 6 October 2006; Foundations of Physics
37, 480–490 (2007), DOI 10.1007/s10701-007-9120-1.
[Versioned primary PDF](https://arxiv.org/pdf/gr-qc/0610024v1),
[publication metadata](https://arxiv.org/abs/gr-qc/0610024).

The PDF was opened and read, including page 2, equation (4) for the oscillator
plus massless scalar action and equation (7) for the renormalized damped
oscillator equation. The text fixes gamma=lambda0^2/(8 pi m0). The trajectory
is prescribed, not varied. This verifies the Minkowski normalization and
the internal-coordinate interpretation. It does not prove a de Sitter
gravitational force law. Our de Sitter statement is independently derived
from the frozen conformal correlator by its commutator subtraction. Later
sections discuss fluctuations and radiation; we make no claim that these
observables are acceleration independent. No external PDF bytes are vendored;
the exact version and equation locations authenticate the citation.

## Frozen external dependencies from Round1

The versioned citations and their hypothesis checks are copied verbatim as
documentary material in frozen_inputs/source_notes.md. The only load-bearing
formula reused is the stationary conformal Wightman function and Planck rate;
Round1 independently verified its Fourier transform.

- Deser and Levin, arXiv:gr-qc/9706018v1, equation (8):
  [primary text](https://arxiv.org/html/gr-qc/9706018v1). This fixes the
  de Sitter temperature for the specified accelerated observer and field.
- Ali, Bhattacharya and Lochan, arXiv:2003.11046v2, equation (15) with the
  vacuum parameter zero:
  [primary text](https://arxiv.org/html/2003.11046v2). Their vacuum alpha is
  not this report's alpha=sqrt(H^2+a^2).
- Milgrom, arXiv:astro-ph/9805346v2, section IV:
  [primary text](https://arxiv.org/html/astro-ph/9805346v2). Retained as the
  source of the temperature-excess proposal; we do not use that proposal as
  a mechanical theorem in this round.

## Repository results retained rather than rediscovered

The Round1 publication is pinned to commit
8aa3f7046a7ae14a99f3515fd42df5bf061fb1db in the isolated publication clone
/private/tmp/core-open-publish.GPoQNP. Its exact report and source notes were
copied with git show; this does not rely on the moving main checkout HEAD.
frozen_inputs/provenance.json records source paths and byte hashes.

The three nodal files were read from the existing historical mechanism
directory, then copied with byte hashes. They are not other agents' Round2
work. They already establish:

| Predecessor | Existing result used |
|---|---|
| NODAL_RING_ORIGIN.md | Clifford nodal-ring spectrum; positive nonanalytic cubic after quadratic subtraction; finite-temperature rounding; free microscopic portal |
| NODAL_DYNAMICS.md | Homogeneous retarded polarization kernels, passive absorption, and nonlocal gapless response |
| NODAL_FORCE_LIMITS.md | Single-ring anisotropy, weak-source mass-law problem, and gapped gradient mass offset |
| Round1 report.md | Correct a0/aH normalization; exact CFG695 source; ordinary finite dipoles' wrong power; vacuum-offset and source-map gaps |

Round2's additional work is the Gaussian mechanical observable, canonical
P-source normalization of the finite-cutoff determinant, its inverse force
series and exact saturation test, the two finite-temperature tuning choices,
and the explicit same-model vacuum-counterterm family. The cubic term,
thermal rounding, and generic vacuum zero-mode freedom are not claimed new.
