# Independent action review: Weyl source and curved clock

2026-10-20. Reviewer: critical_gauge_current. Base f4d7d0e7a;
criteria-only commit1a46afd06. No unresolved mathematical objection was
found within the explicit prescriptions and limits below. This is an
analytic cross-review, not a microscopic health certificate or a full
formal proof. The original normalization goal remains open.

## Exact reviewed artifacts

- `WEYL_SOURCE.md`, SHA256
  `c22d9b33f73e02f9498ace95334f954969c7c182779bc5a46837baa5870d3f8d`.
- `SOURCES_WEYL.md`, SHA256
  `e01333ba0a97b0c72a78e46fa2a78b4009dd71e52d11b72b8d7c18c1f6dd5149`.
- `CURVED_CLOCK.md`, SHA256
  `cc734eccbcda67b27d39fbc36de75f0dfc33927325805afb24ac597e5336453a`.
- `SOURCES_CLOCK.md`, SHA256
  `4a0f5d95a3c6c8cc8ed742789047c3c967b20d1eafae67a156b5339e955d36b3`.

The review reconstructed raw equations after the authors saved their
packets. Later changes require checking the affected dependencies.

## P2. Weyl reduction and source: reconstructed checks

The invariant ghat=(phi/phi0)^2 g and b=varphi-d log phi are correct on
the stated positive-scalar patch. A nonzero b=d sigma survives a Weyl
gauge change; imposing Dphi=0 would be an additional condition that removes
the cubic. The hierarchy a=phi0/xi_W is distinct from operational xi.

I independently reduced the normalized-vector prescription. Varying the
vector and its unit multiplier fixes ell=M^2(Box sigma+X); elimination
gives +M^2(Box sigma+X). Combining its X term with -3M^2 X from Weyl
curvature and -alpha M^2 X/2 gives -M^2(alpha+4)X/2. The residual Box
term is an ordinary boundary term under the stated pure-phase assumptions.
The multiplier's normalization stress cancels; this stress cannot be
imported from a different fixed-component external-vector variation.
The displayed vector diffeomorphism Ward identity has the correct signs.

For literal same-compensator matter, the two metric/scalar chain-rule
terms cancel exactly, and variation at fixed ghat gives zero direct sigma
charge. Thus the normalized closure's scalar equation is unsourced by
baryonic mass. This does not exclude a boundary-supplied profile or prove
that every possible external-vector/background formulation is inconsistent.
The report correctly distinguishes its consistent closure from the source's
published recipe and leaves that recipe's variational bridge unresolved.

Direct expansion of -C X^(3/2) at a nonzero spacelike gradient gives the
reported positive time coefficient and longitudinal coefficient twice as
large at alpha=-4. The resulting squared speed2 and the kinetic coefficient
tending to zero at zero gradient are correctly separated from a universal
UV no-go. In the scalar-terms-off pure phase, the retained Weyl Hilbert
term gives C2=3M^2; merely saying the scalar is inactive would not remove it.

Both conditional force dictionaries reconstruct. The source-recipe map
gives xi=32pi/(lambda beta^2) only after granting that unproved source/map.
The changed q matter action instead has G_UV=G(1+q^2/3) and the stated
q^6/(1+q^2/3)^3 factor. These are endpoint calculations, not transition
solutions. The field/parameter redefinition preserves M,C3,V0 and
lambda beta^2, so its remaining invariant is not a normalization artifact.
The restored c factors cancel in the conditional physical xi as stated.

## P3. Curved clock constraints: reconstructed checks

For the transverse block I separately obtained the shift constraint and
c_V^2=(2B-M)/[2(B-M)]. The de Sitter curvature term is +2H^2 in the
reduced restoring frequency. The substitution U=aV produces the displayed
conformal oscillator after its temporal boundary. This verifies the finite-k
constrained mode, rather than relying solely on the fixed-metric tilt.

In the longitudinal ADM calculation, the kinetic expansion gives
-3S_c U^2+2S_c U b-Mb^2. Shift elimination gives C=2(B-M)S_c/M;
lapse elimination gives D0=CH^2+MX and the stated n. Keeping Xdot=-2HX
in the cross-term integration reproduces both K_z and positive V_z.
Its contribution to the bracket potential is exactly
-2CH^2BX(CH^2+3MX)/D0^2. Freezing X would change this result.

The reduced friction and frequency are positive. The elementary derivative
of X(aX+b)/(c+dX) has the stated positive numerator. Therefore its oscillator
Lyapunov function decreases. The additional bounded limiting-system and
integrable-O(X) argument establishes future boundedness and freezing at
each fixed finite initial k; no uniform high-k or nonlinear bound follows.

The strict k=0 qualification checks: the displayed Killing generator
annihilates the de Sitter metric and generates the a^-1 clock congruence
change. The other a^-2 solution has nonzero gauge-invariant acceleration.
The finite-k constraint inverse cannot be used to settle the zero-mode
boundary/gauge quotient, and the text does not do so.

For finite-gradient homogeneous Bianchi tilt, I reconstructed the exact
aether invariant, the rational odd-sector terms and the shift equation
h(Kd-jh theta)=0. Eliminating it gives
mu_theta^2=2H_perp^2-h^2 j E_X/(KM). The quoted physical perturbation
of u.partial phi is nonzero at finite h. The auxiliary has no linear odd
source, so no quadratic elimination term is missing on the regular branch.

The Bianchi lapse constraint, shear equation, h redshift and Hdot follow
from the homogeneous kinetic density -3B_cos H^2+3(B-M)v^2 and E(h).
The integral bound on v uses H>=H0 and h<=h_i exp(-H0t), not an assumed
positive H_perp. The 9/4 and 1/8 smallness factors then imply
H_perp>3H0/4 and mu_theta^2>H0^2. Its coefficient errors decay integrably;
weighted variation of constants gives the stated e^-H0t tilt decay.
The instantaneous finite-h threshold and WKB ratio also check algebraically.
They are correctly not promoted to an all-time finite-k Bianchi theorem.

The improved clock sector does not fix the independent matter charge or
cubic/vacuum deformation, and does not repair the rational scalar's zero
vacuum spatial stiffness or auxiliary fold. Those limitations are retained.

## Source authentication and independence limits

I independently read the exact primary Scholz2510.17704v3 HTML header
(23June2026) and the displayed operator, unit-vector, matter and transition
assumptions in section2.1. The publisher version EPJC86:857 and its date
remain the source-card author's authentication; I did not repeat that
publisher retrieval. No external result is used to replace the action
reductions above. The older Foster--Jacobson gr-qc/0509083v2 convention
card is inherited; the present curved coefficients were derived directly.

I authored `GRAVITY_PHASE.md` and `SOURCES_PHASE.md`; this document is not
an independent review of those files. Their separate reviews come from
the other agents. I also contributed an earlier pure-BM de Sitter packet;
that different action is not counted as fresh independent evidence for
the present c1-only reduction. Rational-sector coefficients and previously
checked source facts are explicitly inherited inputs. The new P2/P3
equations above were reconstructed independently. No scripts, builds,
source downloads, Lean edits or end-to-end kernel proof were performed
or claimed in this review.
