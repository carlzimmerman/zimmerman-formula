# Exact-version derivative-action source check

**Correction, 2026-10-19:** the electric all-IBP matching verdict below is
superseded by
[ADDENDUM_2026-10-19_COMMON_PV.md](ADDENDUM_2026-10-19_COMMON_PV.md).
Magnetic/digamma/beta correspondence remains verified; the finite electric
source-to-common-PV correspondence is unresolved. Frozen source hashes,
raw derivations and run artifacts are unchanged.

Checked 2026-10-19 UTC. Source: D. Diakonov and M. Oswald,
*Covariant derivative expansion of Yang-Mills effective action at high
temperatures*, official [hep-ph/0303129v2](https://arxiv.org/abs/hep-ph/0303129v2),
18 June 2003; published as Phys. Rev. D **68**, 025012,
[doi:10.1103/PhysRevD.68.025012](https://doi.org/10.1103/PhysRevD.68.025012).

The official version-specific PDF was downloaded and its title/version
authenticated. SHA-256:
`8100b29c88f620c19a30cef5c4dd84f4092320911ae70cb9aa8d89353f6756af`.
The PDF was kept temporarily outside the repository; no full source text or
PDF was copied into tracked research output. The preexisting project cache
was queried first and had no exact-version hit.

## Extracted formulas and convention translation

The source's equations (18), (23)--(26) have the stipulated component action
and determinant, with source `S_1loop=-Gamma_1`. Its `T=1/L`, `phi=h`,
`nu=x=Lh/(2pi)`. Source equations (67), (69), (72) and (91) give the
parallel electric and magnetic logweight coefficient

`L*11/(48pi^2)[2 log(M L/(4pi))-psi(x)-psi(1-x)]`.

Equations (73) and (92) give the UV relation
`1/g_PV^2(M)=11/(12pi^2)log(M/Lambda_PV)` to one-loop order.
These establish the derivative/digamma and beta-coefficient comparison in
REPORT.md. Source equations (48)--(49) give the same periodic quartic
potential. PDF printed pages 7, 10, 12--15 were read as extracted text;
pages 12, 14 and 15 were also inspected as pixels. No fermionic or
non-Cartan derivative coefficient is imported.

Verdict for the declared Cartan bulk profile: **verified, known after
translation of notation**, with an independently derived bubble/heat-kernel
proof of the coefficient. This is not a novelty claim or finite-ball source
theorem. The source's assumptions are a local slow-variation expansion,
periodic fields and a holonomy chamber away from massless charged modes.

## Equation-of-motion and surface check

The source's (82), on h>0 Cartan backgrounds, reads

`S_EOM=(1/(12pi)) integral (Lh/pi-1) Delta h`.

It is zero pointwise on `h=v-1/r` away from the core. Direct integration by
parts, retaining the surface term, gives

`S_EOM=-(L/(12pi^2)) integral (grad h)^2`
`       +(1/(12pi)) integral_boundary (Lh/pi-1) partial_n h`.

This identity is sufficient for the project comparison. It also exposes a
printed inconsistency in (83): its positive coefficient of
`(E_i.A4)^2/|A4|^3` fails this identity. For a general A4 the corresponding
bulk term derived from (82) has a negative coefficient. The discrepancy is
visible already for positive Cartan h, since the two terms proportional to
`E^2/h` must cancel after differentiation of `A4/|A4|`; (83) as printed adds
them. This is a focused algebraic check of the two printed formulas, not a
claim about the paper's other results. Equation (83) is not used as evidence.

Application limits: even though (82) vanishes on the shell, independent
surface/domain terms in a finite-radius determinant are not thereby zero.
The periodic potential and local derivative coefficients do not prove the
metric response of a physical confining vacuum.

