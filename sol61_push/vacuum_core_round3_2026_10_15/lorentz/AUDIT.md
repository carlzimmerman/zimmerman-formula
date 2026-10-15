# Independent local audit of the Lorentz-vacuum obstruction

15 October 2026. Primary verdict: **proved as written**, within the specified
parity-even, derivative-free, twice-differentiable single-gauge L(S,P) class and
its prescribed electric restriction. This is a separate reconstruction by an
isolated agent using the same model family, not external peer review or a formal
proof certificate. It does not exclude the medium action, another vacuum phase,
additional fields, or every mathematical theory of the interaction.

Audited byte hashes (SHA-256):

- PROOF.md: `a40e10dfff284d97704dc88132dea6a879fe0410b8d272005ff42f33c22ec289`
- check_lorentz.py: `2891cc1fb82fdef786a12473d1f56060cca4567ef3fd2ab902a9a07f106926ed`
- LITERATURE.md: `f5662efa7e01053c52da25f014093cd969b126508e3840ba18e7c793b8f6c0b4`
- run_v1/results.json: `3871ba7063a8187eefe67ccfd227eb5e875a923219d8c7bffb802da07320fc66`
- run_v1/manifest.json: `a890e97b9cac8e3f298d2d7123c6a3ab7c824edd74e90321b09abeecd692f210`

## Full perturbation reconstruction and the physical mode

Start with arbitrary electric/magnetic perturbations e,b around E=E0 zhat,
B=0, with E0>0. At second order,

    deltaS=E0 e_z,     delta2S=(e^2-b^2)/2,
    deltaP=E0 b_z,     delta2P=e dot b.

Parity evenness gives L_P=L_SP=0 at P=0. With t=L_S and
p=L_S+E0^2 L_SS, the complete quadratic density is

    L2 = [t(e_x^2+e_y^2)+p e_z^2]/2
         -[t(b_x^2+b_y^2)+(t-E0^2 L_PP)b_z^2]/2.

This full expansion, rather than substituting a trial polarization alone,
shows that the electric and magnetic response matrices are diagonal. Thus
A_z=a(t,x), e_z=-a_t, b_y=-a_x is a closed polarization of the full linearized
field system. The free coefficient L_PP controls b_z and cannot change this
mode. If parity evenness is dropped, L_SP need not vanish and this decoupling
argument need not apply; the proof correctly keeps the parity hypothesis.

The linear displacement has only a z component -p a_t and is independent of z,
so div(deltaD)=0. The magnetic perturbation also has zero divergence. Faraday's
law is an identity because e,b come from a potential. Ampere's z equation is
`-p a_tt+t a_xx=0`; its other two components vanish. The nonzero field strength
makes this a physical transverse mode, rather than a gauge artifact.

For the retained Le, t=D0/(D0+E0)>0 and p=D0^2/(D0+E0)^2>0.
Therefore omega^2=(t/p)k_x^2, with phase, group and characteristic speed
sqrt(1+E0/D0)>1 in this direction. The positive kinetic and spatial energy
coefficients distinguish the cone violation from a ghost or gradient
instability. A constant source-free electric field is a local exact background
of this derivative-free gauge theory; no nonzero uniform charge density is
silently imposed.

## General slope and invariant regularity

For an arbitrary differentiable positive electric response with D'>0,
`t=D/E` and `p=D'`. The implication

    speed^2<=1  iff E D'>=D iff (D/E)'>=0

follows directly, without a classification theorem. If D/E approaches one as
E approaches zero and is nondecreasing throughout the interval, it cannot
subsequently equal the retained ratio below one at a positive E in that same
interval. The proof's restriction to one continuous Lorentz phase is essential;
it does not rule out an actual phase boundary.

Differentiating t=L_S(E^2/2,0) gives

    L_SS(E^2/2,0)=(dt/dE)/E
                 =-D0/[E(D0+E)^2].

This is unbounded as E decreases to zero, so a C2 extension in invariant
coordinates on an open neighborhood of (S,P)=(0,0) is impossible with the exact
small-positive-electric restriction. The claim concerns C2 regularity in the
invariants. It does not state that the Cartesian electric restriction lacks
C2 regularity, nor does it exclude formulations with additional variables.

## Source and computation obligations

The source convention check was independently repeated against Russo and
Townsend, [arXiv:2211.10689v3](https://arxiv.org/html/2211.10689v3), 11 January
2023: equations (1.1)--(1.5), then (2.19)--(2.24). Those supply compatible
invariants, quadratic conventions and the distinction between phase and group
speed. The selected response and full-matrix derivation above are local
calculations, not claims of the source's no-birefringence classification. No
novelty or exhaustive literature conclusion is made. The exact primary HTML
was read; no PDF cache authentication is claimed.

| Obligation | Result |
|---|---|
| Electric restriction fixes p and t | Passed by direct derivatives |
| Selected polarization belongs to full equations | Passed by full diagonal response matrices |
| Gauss and magnetic constraints | Passed, identically zero divergences |
| Free L_PP can repair the selected cone | Refuted within the hypotheses; it acts on the other polarization |
| General ED'>=D condition | Passed with positive D,D' |
| Invariant-C2 obstruction | Passed with exact restriction for all sufficiently small E>0 |
| Claim against all vacuum models or all EFT completions | Out of scope and not asserted |

An orthogonal symbolic reconstruction is stored in
`../action_join/check_lorentz_full_matrix.py`, with its own bounded-run manifest.
The parent's 10 identities and 3 controls were inspected as implementation
support; universal scope comes from the derivation, not the control count.
The decisive remaining branch is a different electric phase or extra physical
structure with its own matching and stability equations, not adjustment of
L_PP within this unchanged class.
