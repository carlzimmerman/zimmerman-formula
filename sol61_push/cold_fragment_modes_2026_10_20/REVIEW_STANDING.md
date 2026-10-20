# Independent review of the standing quadrupole radiation diagnostic

20 October 2026. Bounded read-only review of `standing_radiation.py`, its contract, `standing_run_001`, and the reused completed chiral ell=4 response. Reviewed bytes are pinned in `sources_review_standing.json`. No physics solve was rerun.

**Assessment: accepted as a finite leading weak-amplitude response diagnostic.** Both the standing-run and reused `radiation_run_002` v2 manifests independently validate. The standing record has 172/172 passed checks. Angular multiplicities, mode-energy normalization, zero net intrinsic J, cached response scaling and positive-charge flux bookkeeping are consistent. No material algebra or implementation error was found within this scope.

## Normalization and angular content

The parent is

    z=A[Z H exp(+i Omega t)+c.c.]/r,
    H=(Y22+Y2,-2)/sqrt(2), integral H^2 dOmega=1,

with the established harmonic chirality convention. H is real. Consequently, unlike for a single chiral harmonic, the angular integral does not remove the potential time-dependent quadratic-energy term by itself. It nevertheless vanishes for an exact bound eigenmode because

    (W-Omega^2+i Omega G)Z=0,
    Z^T(W-Omega^2)Z=-i Omega Z^T G Z=0,

using transpose without conjugation and skew G. The code checks that coefficient directly, obtaining residual magnitudes below1.4e-13 in the reported cases. The remaining constant K is the same radial `dr[Omega^2 Z†Z+Z†WZ]` as for the cached chiral unit mode. Thus **K_parent=A^2**, with no extra factor one half or two.

Squaring the real angular pattern gives

    H^2=C0 Y00+C2 Y20+C4 Y40
          +(C44/2)Y44+(C44/2)Y4,-4,
    C0=1/sqrt(4pi), C2=-sqrt(5)/(7sqrt(pi)),
    C4=1/(14sqrt(pi)), C44=sqrt(5/(14pi)).

The numerical angular quadrature independently checks these signed coefficients, their pointwise reconstruction and unit norm. Multiplying the same action-derived complex quadratic radial force by those coefficients is correct in the no-half convention. The source uses squares rather than moduli for the 2Omega harmonic.

## Exact reuse and intrinsic angular momentum

The unperturbed fragment is spherical, so the radial outgoing operator depends on ell but not m. Each standing ell=4 source is a constant multiple of the pinned chiral ell=4 source on the same grid and background. Therefore its field response scales by that constant and its time-averaged flux/work by the constant squared. The total ell=4 standing weight relative to the chiral coefficient is exactly

    (C4/C44)^2+2(1/2)^2=1/70+1/2=18/35.

The code applies this weight correctly, retaining separate m=0,+4,-4 entries. Orthogonality removes cross terms from integrated mean fluxes. Matched mode/cache parameters, source reconstruction, prior receipt and manifest checks support this reuse; it does not duplicate the previous ell=4 solve. The outgoing library has the actual general-ell Hankel polynomial, so ell=4 is not being replaced by the old ell=2 fallback.

The real parent has zero integrated intrinsic J. The m=0 outgoing components have J=0; the equal-power m=+4 and-4 components have opposite J and cancel exactly. This is energy and charge emission with zero **net** intrinsic angular momentum, not a new net torque or an export of galactic orbital J.

## Numerical result, flux ledgers and convergence

At L=60, dr=.05 the coefficients are:

| Q | gamma_standing | Relative to chiral gamma | ell=0 fraction | ell=2 fraction | ell=4 fraction |
|---|---:|---:|---:|---:|---:|
| 80000 | 1.8310533145441595e-5 | 4.818123452000466 | .8893507692643751 | .0039093932430458445 | .10673983749257913 |
| 160000 | 1.441045010337569e-5 | 85.91282042898007 | .9932735438207234 | .0007403214939319804 | .0059861346853447685 |

These are mean outgoing K-power coefficients for the prescribed unit-K modal shape. The leading slow-amplitude law is `dK/dt=-gamma_standing K^2`. They are dimensionless classical coefficients, not inferred merger efficiencies or physical dwarf cooling times.

Only Psi+ is open at 2Omega. The summed edge fluxes correctly satisfy `Q_out/K_out=1/(2Omega)` and `E_out/K_out=1+omega/(2Omega)`. The remnant must lose emitted charge and adjust its background; a standing pattern with J=0 does not imply charge-neutral radiation. Discrete edge flux is used for the work identity, and continuum-amplitude flux separately defines gamma.

The relative total-coefficient box/mesh changes are .00355189/.00059205 for Q80000 and .0000270115/.000402175 for Q160000. They satisfy the declared five-percent criteria by a wide margin. These finite comparisons are not certified continuum error bounds. Recorded maximum RSS is84066304 bytes.

## Scope retained

The result demonstrates that this particular coherent standing preparation has a stronger leading scalar loss channel, dominated by ell=0, than the single chiral preparation at equal K. It does not predict how a merger prepares either angular pattern, the amount or distribution of K injected, capture probability, the fraction of a binding gap radiated, or a nonlinear invariant standing-mode trajectory. Static/fundamental backreaction and any mode redistribution require their appropriate standing-pattern treatment; a chiral initial-condition correction cannot simply be presumed to complete this different configuration.

There is no resulting four-dwarf mass-budget closure, selective assembly history, direct orbital transport mechanism, physical action-unit normalization or quantum completion. These limitations are already explicit in the reviewed contract/result and should remain attached when reporting or pushing the packet.
