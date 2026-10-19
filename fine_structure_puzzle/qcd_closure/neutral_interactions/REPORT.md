# Complete first neutral interaction correction

The first interaction diagram omitted from the FSP-004 Gaussian neutral
ensemble is now calculated with all field modes retained. In the declared
minimal scalar EFT it has no inverse-radius spatial-stress term. An
independent pretarget derivation agrees. This is a soft-model result, not
physical QCD A_rho or an electromagnetic-alpha prediction.

## Actual diagram and matching paths

For canonical varphi=sqrt(kappa) phi on closed S3_R,

    S=integral[(grad varphi)^2/2-u cos(varphi/sqrt(kappa))],
    m^2=u/kappa>0, lambda=-m^2/kappa,

the first interaction is lambda varphi^4/24. There is no cubic vertex at
the stable minimum. Its three Wick contractions give the complete two-loop
interaction vacuum diagram

    W_2=(lambda/8) V G_R^2,
    G_R=-sqrt(m^2-R^-2)coth(pi sqrt(m^2 R^2-1))/(4pi),
    V=2pi^2 R^3.

The common finite-part/zeta tadpole subtraction and minimal curvature
coupling are fixed. The regime is mR>1, m/kappa small, fixed small L.
Higher vertices and multiple quartic vertices begin at the next loop order.
Hard metric matching and nonperturbative sectors are not calculated.

At fixed Lagrangian m,kappa, the flat-subtracted two-loop density is

    Delta f_2=lambda/(128pi^2)
          [(m^2-R^-2)coth^2(pi sqrt(m^2R^2-1))-m^2].

The actual spatial response tau_s=(1/L)partial_V W therefore starts at

    Delta tau_s,2=m^2/(384pi^2 kappa L R^2)+exponentially small.

At fixed flat pole mass M, the one-loop tadpole requires
delta m^2=-(lambda/2)G_infinity(M), G_infinity=-M/(4pi).
Including that mass insertion in the Gaussian determinant and making the
same flat subtraction completes a square:

    Delta f_2,pole=(lambda/8)[G_R(M)-G_infinity(M)]^2,
    Delta tau_s,2,pole=1/(1536pi^2 kappa L R^4)
                    +1/(1024pi^2 kappa L M^2 R^6)+... .

These are different parameter paths. The R^-2 **two-loop** term on the
first path is cancelled by the Gaussian mass retuning on the second. The
Gaussian one-loop curvature response itself still starts at R^-2. No claim
that the full stress starts at R^-4 follows. Arbitrary allowed independently
matched curvature and hard gravitational operators can change even-curvature
coefficients. Neither matching path creates a 1/R term in this diagram.

The isolated constant-mode contraction is -1/(8uV) in W, exactly matching
the compact uniform integral's leading correction. It is already part of
G_R^2. Appending it to the full field result would count it twice and omit
equally important mixed contractions.

Flat-pole matching alone also does not determine absolute unsubtracted
vacuum energy to this loop order: the classical cosine vacuum term changes
under retuning and needs higher-order vacuum/mass matching. Those extensive
terms cancel in the common flat subtraction used here. The result therefore
does not fix the unknown absolute metric functional needed for physical QCD.

## Evidence and independent review

[RAW_DERIVATION_v1.md](RAW_DERIVATION_v1.md) was saved before execution and
literature search. The calculation follows elementary Wick contraction,
the parent's exact S3 spectrum, flat tadpole matching and the metric
derivative, rather than a numerical coefficient fit. No claim of global
novelty is made. A bounded primary-literature search found broader
curved-space/sine-Gordon work; no external two-loop formula was imported.

[The independent reviewer](../reviews/neutral_interactions/REVIEW.md) saved
a separate derivation before target reads. It confirmed loop completeness,
the tadpole sign, both exact stresses, the constant mode and the asymptotic
powers. It also differentiated the parent's integrated determinant D11 by
hand, fixing partial_(m^2)W_1=VG_R/2. The script's similarly named determinant
check substitutes the analytic derivative; it is an algebraic normalization
check, not a numerical differentiation of an independently coded determinant.

`runs/two-loop-002/manifest.json` completed and validates: 16 exact symbolic
checks and 108 numerical checks at each of 70 and 95 working digits.
Largest scaled discrepancies were about 4.21e-71 and 2.54e-81. These are
finite observed errors, not interval certificates. The spectral tail has
separate analytic geometric and Euler--Maclaurin bounds; Poisson winding
integrals give an orthogonal tadpole check.

`two-loop-001` is preserved as failed. A contracted precision diagnostic
localized the failure to tiny library Hurwitz tails evaluated with an
absolute stopping criterion, then amplified by powers of the spectral
parameter. The new implementation uses explicit Euler--Maclaurin tails with
remainder bounds and preserves all tolerances. The diagnostic and the
failure are computation evidence, not counterexamples to the physics.
See [the precision record](SPECTRAL_CHECK_AND_PRECISION.md).

## Reproduction and remaining implication

The exact commands, software, limits and input/output hashes are in the
manifests. The current code is `check_two_loop_v2.py`, with
`COMPUTATION_CONTRACT_v2.json`. Use the installed computation-audit bounded
runner with those declared inputs and a new output directory; do not reuse
or alter an old run. The current child used a 60-second wall cap, 50-second
CPU cap, one conventional numerical thread and a 1-MiB log cap.

The first interacting soft diagram is closed. Full curved microscopic
fugacity/stiffness matching, hard/global gauge normalization, compact domain
walls, higher loops, physical matter, QED and the state/geometry bridge remain
uncomputed. The old source's microscopic g dictionary is not used: kappa and
u here are independently matched EFT parameters. Physical R(alpha) remains
open.
