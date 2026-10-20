# Primary-source checks

Checked online 2026-10-20; no source downloaded or retained, so no retained
source-file hashes exist. Mathematical deductions and applications below are
separate from the sources' claims. The online HTML/PDF rendering datelines
are inconsistent; bibliographic versions use arXiv's version identifiers.

## Nonlinear electric-magnetic duality

Gibbons and Rasheed, *Electric-Magnetic Duality Rotations in Non-Linear
Electrodynamics*, [hep-th/9506035v2](https://arxiv.org/pdf/hep-th/9506035v2),
27 August 1995, sections 2-4, equations 2.3-2.7 and 4.2. The delegate
authenticated and extracted these derivative conditions and the Born-Infeld
example. They do not fix an additive Lagrangian constant. The source's
duality integration constant is distinct from absolute vacuum energy.
Application: with canonical normalization Z=T/b^2, a physical threshold
alpha b becomes alpha_c sqrt(T). Thus its ratio to G times vacuum energy
is `(alpha_c^2/G)(T/C)`; the quarter is not supplied by field normalization.
This application is a direct local derivation, not a source theorem about
MOND. The Born-Infeld force shape also requires a separate bridge to MOND.

## DBI screening / dark-energy proposal

Cai and Wang, *Dark matter superfluid and DBI dark energy*,
[1511.00627v3](https://arxiv.org/html/1511.00627v3), 23 January 2016,
equations 14,17-18,27-31,33. Both coordinator and delegate inspected the
primary version. With their reduced Planck convention, set
`T=Lambda^4`, `epsilon_phi=T gamma`, `eta=r_DBI/r_M`. Their equations imply

    a0=eta^2 sqrt(T)/(2g Mpl),
    xi=2pi eta^4/(g^2 gamma),  gamma<=1,  w_phi=-gamma^-2.

The matching eta=1 and coupling g are choices. Achieving a quarter would
require `g^2 gamma=8pi eta^4`. The interaction-inclusive density adds another
sector-splitting parameter. Independent expansion of their action gives
time kinetic Hessian `-gamma^3`; its sign precludes positive perturbation
energy in this scalar model. The source leaves its ghost problem unresolved.
This audits that proposal; it is not a no-go for all DBI completions.

## Mathematical input

Claim C in PROOF.md uses the classical theorem that pi is transcendental.
The independent reviewer and coordinator checked the explicit
`transcendental_pi` theorem in the primary
[AFP formal proof](https://isa-afp.org/browser_info/current/AFP/Pi_Transcendental/Pi_Transcendental.html)
on 2026-10-20. We inspected that source; we did not rebuild Isabelle locally.
The rational-function valuation argument is supplied in full locally. The earlier local
one-pi Lean theorem proves a more restricted irrationality-based statement;
this lane does not claim to extend or compile that Lean artifact.
