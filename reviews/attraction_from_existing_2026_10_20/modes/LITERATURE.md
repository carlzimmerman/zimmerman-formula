# Bounded primary-source overlap check

Checked 20 October 2026. Question: is a conditional interaction between two
already density-coupled trapped occupations obtained by eliminating stable
Bogoliubov modes, and does that result supply the project's free/tether
operator dictionary? No literature-wide novelty assertion is sought.

## Exact overlap

Alexander Klein and Michael Fleischhauer, *Interaction of Impurity Atoms in
Bose-Einstein-Condensates*, [arXiv:cond-mat/0407809v1](https://arxiv.org/html/cond-mat/0407809v1),
30 July 2004; published in [Physical Review A 71, 033605](https://doi.org/10.1103/PhysRevA.71.033605)
(2005). The official arXiv header and submission record authenticate v1.

Their equations (1), (11), (15), and (18) give a density-coupled conditional
level shift with self shifts separated; (20)-(24) give the homogeneous
Bogoliubov momentum sum. The interaction uses the real cross overlap divided
by each positive excitation energy. Their finite box excludes its number
zero mode, and its cross shift can have either sign. This matches the
structure of RESULT (3) after setting `hbar=1`, `gamma=kappa/2`, and
identifying their density-mode overlaps with the factors in our `g_i`.
Their impurities have externally supplied state-dependent couplings and
traps; they do not establish the present same-scalar fragmentation,
canonical gravity, or free/tether states.

Checks: authenticated exact version, extracted formulas, checked coupling
normalization and overlap structure. Classification: **known after
translation of notation** for the general exchange mechanism. Project
application: **conditional** on the missing physical state/operator map.
No full text was retained; there is no retained primary-text hash.

## Adjacent range and approximation check

Moritz Drescher, Manfred Salmhofer, and Tilman Enss, *Medium-induced
Interaction Between Impurities in a Bose-Einstein Condensate*,
[arXiv:2303.01916v2](https://arxiv.org/html/2303.01916v2), 7 June 2023;
[Physical Review A 107, 063301](https://doi.org/10.1103/PhysRevA.107.063301)
(2023). The versioned official full text was inspected.

Their equation (2) defines the interaction by subtracting the separated
impurity energies. Section III.1, equation (6), derives a Yukawa density
tail by linearizing the condensate equation; it requires a small far-field
deformation. Their discussion also warns that higher orders eventually
dominate the exponential at very large separations. Their heavy external
impurities and independently specified impurity interaction do not solve
the same-species or free/tether identification here.

Checks: authenticated version, extracted the subtraction, range equation,
and stated limitation. Classification: **partial or adjacent result only**
for the project's physical state problem. The report's coefficient comes
from its explicit square completion and Fourier normalization, not from
transferring a fitted impurity coupling. No full text was retained.

## Search scope

Discovery queries were `Bose Einstein condensate induced Yukawa interaction
two impurities Bogoliubov static potential original paper` and `Recati
Klein Jaksch Zwerger phonon mediated impurity interaction Bose Einstein
condensate Yukawa 2005`. Searches used the available web index, followed by
the official versioned arXiv primary texts. The second paper's introduction
provides adjacent Yukawa, Efimov, and long-distance phonon references; no
exhaustive citation crawl or independent second-searcher novelty audit was
performed. Local predecessors inspected were the exact recent micro
response, occupied landscape, and memory notes pinned in `source_hashes.json`.
No absence-of-prior-art claim follows from this bounded check.
