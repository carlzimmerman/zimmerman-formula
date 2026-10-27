# Coordinator reconstruction and independent-route reconciliation

This is post-exposure checking, not a third blinded derivation. Root read the
independent frozen proof and the author proof, and checks their final exact
bytes named in CHECK_RECORD.json. Root's earlier candidate carries its own
explicit preview-before-freeze limitation and separate independent audit.

For terminal X(t)=x, j(s)=partial_x X(s;t,x) satisfies j'=lambda_x j,
j(t)=1, hence j=exp(-integral_s^t lambda_x). Differentiating the integrated
R equation gives the author's exact (5), including j times total F_x and n_x.
R+_x-R-_x=2b g_x+2H_chi k supplies (6) with its minus density-source sign.
No linear-superposition or static-field premise follows from this accounting.

For r=v-lambda, direct differentiation yields
D_lambda(j n/r)=-j n_x-j n D_v r/r^2. With a cutoff, an extra
j n D_lambda theta/r term appears. Substituting full momentum gives the
three terms J,P,L and retains pressure and transition derivatives. The
coefficient of n_x after combining pressure is exactly
1-theta+c^2(theta/r^2-theta'/r); it need not be small in the slow region.
Two fast terminal traces combine as -n/(v+b)+n/(v-b)=2bn/(v^2-b^2),
whose contribution to g_x is -Cn/[tau(v^2-b^2)]. This is one term of an
actual-solution decomposition, not a sign theorem for total g_x.

The two backward field paths separate because their positive b speeds point
apart in backward time. The density mass between them has derivative
-r_plus n_plus+r_minus n_minus, yielding the stated wedge flux identity.
Material mass labels instead give D_lambda M=-r n. Fixed-sign transport
controls swept mass; multiple crossings count multiplicity. Neither identity
controls endpoint densities or terminal spatial derivatives.

The sufficient absolute estimate (16) follows from b>=bmin and the positive
part triangle inequality. The fast pressure estimate (17) includes both
families, jmax, c^2/(delta V)^2 and the time-order integral (T-s) sup|n_x|.
Fubini on a classical compact slab is legitimate. An N-uniform trace bound
is still needed; finite values for each N are insufficient. Compact field
states alone do not bound j because its exponent integrates lambda_x.

## Separate reviewer counterexample, reconstructed here

The independent reviewer supplies a stronger test of the mass-only shortcut
than the author's static bump. Take constant U>b>0, v=U,
n=nbg+(M/epsilon)psi((x-Ut)/epsilon), psi smooth nonnegative of mass one with psi(0)>0.
This exactly satisfies continuity. Along constant field speeds -b,+b with
unit weights,
Iplus=[n(0,x+bt)-n(t,x)]/(U+b),
Iminus=[n(0,x-bt)-n(t,x)]/(U-b).
At x=Ut for fixed t in [t0,t1], t0>0, both initial bumps miss the feet for
small enough epsilon. Subtraction gives
Iplus-Iminus=2b M psi(0)/[(U^2-b^2)epsilon]>0.
A finite spatial cone chosen to contain the moving peak over that interval
makes the time integral of its positive spatial supremum diverge while the
excess mass and relative-speed separation stay fixed. Root recomputed the
path arguments, integrals, sign and scaling. This is accepted ONLY as a
continuity-only functional inequality counterexample. It does not solve the
full momentum/Q/scale system or use the prescribed initial hydrostatic density.
It neither disproves the actual coupled feedback budget nor supports a claim
of instability of the physical theory.

## Correction and scope accounting

The independent reviewer self-detected an error in its frozen ancillary
pointwise display (3.4): the D_lambda u sign and a lambda_x term were wrong.
Its timestamped correction preceded reading the root candidate and author
proof. Root verified the correction by inserting continuity and momentum.
The original integral identity, cutoff expression and auxiliary counterexample
are unaffected; the uncorrected ancillary display must not be reused.
Original bytes, correction and exposure records are preserved, not overwritten.

Root's exact Riemann inversion separately exposes denominators v-lambda+/-c.
On the actual initial datum, V f-b0-c is negative at both edges and positive
at the center for large N, so each half contains an acoustic intersection.
The independent root audit checks this elementary obstruction to whole-packet
separation. A denominator zero is not a singularity of the original PDE.

Full energy keeps both field fluxes and all boundary work. Hydrostatic
zero-velocity control reconstructs stationary g0_x from the complete source
formula; the density term alone need not vanish. Positive g_x contributes
zero adverse budget. Both normalizations and fixed/frozen/evolving histories
remain separate; evolving reference requires explicit work and chart-time
terms. Diagnostic Q does not transfer to RAR/M/MONO or metric/photon/2DOF.

The author metadata verifier was inspected, not rerun: it overwrites the
frozen VALIDATION.json. Root instead verified all input/artifact/freeze maps
with read-only hashes. That administrative replay limitation is not a proof
defect. No mathematical executable computation or observational test occurred.

Actual-family verdict remains incomplete at signed low-speed/transition,
pressure and endpoint traces, plus chart/Jacobian control over the full horizon.
NEXT_ROUTE.md changes to nested bounded-speed edge patches, asking whether
a distinct N^-7/2 local time covers B* N^-4 there. It is an unproved proposal;
even success would not supply the full-cone or later-resonance bound.
