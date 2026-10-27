# Narrow primary-source checks

Checked 2026-10-19. Scope: convention verification and adjacent equilibrium
formulas, with an independent derivation in `VIRIAL_NORMALIZATION.md`.
No novelty claim or complete boson-star stability literature audit is made.
The project-local cache was queried for the exact versions below and returned
zero matches. No source PDF/text was retained or uploaded by this lane; a
retained-content SHA-256 is therefore unavailable. The source-byte pins in
`source_pins.json` refer to project antecedents, not these web sources.

## S1: equilibrium convention

Pierre-Henri Chavanis, *Mass-radius relation of Newtonian self-gravitating
Bose-Einstein condensates with short-range interactions: I. Analytical results*,
arXiv:1103.2050v2, header 22 August 2011.
[Exact primary version](https://arxiv.org/pdf/1103.2050v2).

Authentication: version header and author/title were read. Extraction:
Sec. II F, PDF p. 8, Eqs. (35)-(46). They state the TF reduction, n=1 profile,
radius, central-density relation and energies. Translation: their scattering
length a is this note's a_s; their configuration mass M is this note's
mathcal M; their Phi is this note's U. Substituting (3) agrees with (5)-(6).
Verdict: **verified** for those TF formulas. Quantum-pressure profiles have
tails (Sec. II E); the paper's Gaussian analysis is not an exact GP stability
theorem and is not used as one here. SP scaling (19) was independently checked
by substitution; no source's fitted numerical radius coefficient is used.

## S2: Love-number convention

Kent Yagi and Nicolas Yunes, *I-Love-Q Relations in Neutron Stars and their
Applications to Astrophysics, Gravitational Waves and Fundamental Physics*,
arXiv:1303.1528v3, header 30 November 2017 (internal date December 1).
[Exact primary version](https://arxiv.org/pdf/1303.1528v3).

Authentication: version header and author/title were read. Extraction:
Sec. VI B, Eqs. (49)-(51), and Sec. VII B 3, PDF p. 17, Eqs. (78)-(81).
They define Q=-lambda E and k2=3lambda/(2R^5), with G=c=1, and obtain
k2=(15-pi^2)/(2pi^2) for Newtonian n=1. Translation restores
lambda_T=2k2 R^5/(3G) for the STF conventions (12). The explicit exterior
potential and independent matching in (13) verify the factor and sign.
Verdict: **verified** on this spherical barotropic Newtonian static sector;
no neutron-star universality claim is imported to the scalar ensemble.

## Not used

The attempted exact primary URL arXiv:1103.2054v2 did not fetch successfully.
It supplies no support here. No theorem of full GP ground-state existence or
nonlinear stability is claimed on the basis of that unavailable version.

## Search scope

Discovery queries were `site:arxiv.org n=1 polytrope tidal Love number
(15 pi) Newtonian` and `site:arxiv.org Chavanis mass radius relation
Newtonian self gravitating Bose Einstein condensates repulsive 2011`.
Only the primary PDFs above support the source-dependent comparisons.
The note's mode-Hessian and ensemble implications are local derivations,
requiring their own mathematical review rather than a citation-chain argument.
