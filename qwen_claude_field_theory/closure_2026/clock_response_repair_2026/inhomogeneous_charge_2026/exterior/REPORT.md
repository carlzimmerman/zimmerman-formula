# The inherited exterior is already a decisive local test

2026-09-12. **Conditional obstruction, with bounded numerical support:** at
the first stored `radiation_002` epoch, a regular constraint-compatible
localized configuration whose complete principal jet approaches that physical
homogeneous background cannot have a real propagating scalar characteristic
cone everywhere. This does not construct such data, exclude every epoch, or
exclude a different asymptotic state of the unchanged action.

## Actual exterior, not the reference coefficient history

The script reads the six declared archive rows, evaluates the original frozen
constitutive model at the physical `q`, and solves the same background linear
system for physical `Qdot` and clock rate. It neither refits coefficients nor
reruns a cosmological history. At `Y=0`, direct contraction of the cubic
principal tensor with the physical FLRW Hessian gives

\[
F=W-2Q^2W_Y,
\quad K=2P_X+4Q^2P_{XX}-12\gamma HQ+6\gamma^2Q^4/M^2,
\]
\[
G=2P_X-\frac{2sW_YW}{F}-4\gamma(\dot Q+2HQ)
 -2\gamma^2Q^4/M^2,\qquad Kc^2-G=0.
\]

Here `P_X`, `P_XX` and `W` already include their original gamma-dependent
coefficient corrections. The Hessian is
`diag(Qdot,-H Q,-H Q,-H Q)` in the local orthonormal frame. Thus both the
linear-gamma Hessian term and quadratic-gamma Einstein feedback are retained.
An independent implementation of these homogeneous contractions is compared
against `finite_gradient_metric_2026/cubic/cubic_debraiding.py`.

At the first **stored** epoch, `a=1`, which is not the earliest cosmological
time in the backward archive:

- physical `Q=0.9078321505772312`, reference `qbar=0.9090909090909091`;
- `H=0.5191118192004086`, `Qdot=-0.04158816556400951`,
  `s=1.0317810692809903`, `gamma=1e-6`, `M2=1`;
- `F=0.0008493856065188155`, `K=2.1843810604921483`;
- `G=-0.0033944731415078457`, quarter-discriminant
  `Xi=K G=-0.007414822840659022`;
- `c²=-0.0015539748091127742`, hence `c=±0.039420487174980146 i`.

The two reevaluated background constraint residuals have absolute value below
`1.4e-17`. The source background is numerical, not an interval-certified exact
root. Eighty-digit Decimal evaluation confirms the sign for the same rounded
coefficient inputs; it does **not** supply eighty-digit background accuracy.

## Why a localized interior does not remove this exterior branch

At this isotropic exterior, `K>0` and `G<0` make the reduced propagating scalar
quadratic `K omega²-G |k|²` strictly positive on every nonzero real covector.
It is a definite scalar principal form, not merely an advected or shifted real
cone. This refers to the propagating chi factor, not the entire constrained
system: tensor metric waves remain null, and the auxiliary clock elimination
has its own exceptional `k=0` case.

On a regular on-shell background with `s>0`, `M2>0`, nonzero spatial wavevector
and nonsingular clock block, the cubic Einstein mixing can be eliminated by
trace reversal. The previous principal audit supplies this analytical mapping.
The non-real scalar branch is non-null and is not removable by residual
harmonic gauge. Constraint compatibility is a hypothesis, not a result of
pasting a gradient onto the archive.

For a compactly supported change of the **complete principal jet**, an exact
exterior point already has the same negative discriminant. More generally,
suppose those jets converge to the displayed background along any spatial
ray. This must include the covariant chi Hessian, the clock gradient and
norm, the metric/frame data entering these objects, and the constitutive
arguments. Merely requiring the scalar spatial gradient to decay does not
control an oscillating second derivative. Regular denominators and continuity
then imply `Xi(r) -> Xi_infinity < 0`. Taking the error smaller than
`-Xi_infinity/2` gives `Xi(r)<Xi_infinity/2<0` sufficiently far out. The real
square-completion identity prohibits real scalar speeds there. Hence the
necessary real-spectrum condition for strong hyperbolicity of the physical
reduced propagation system fails, irrespective of the interior profile.

The parent `AsymptoticCone.lean` formalizes the quadratic algebra, definiteness
and negative radial-limit implication. Its five lemmas were independently
compiled, with only `propext`, `Classical.choice` and `Quot.sound`. It assumes
the limit of the principal coefficients; it does not derive that limit from
constraint data, formalize the covariant field equations, or certify these
numerical signs.

## Orthogonal constraint-reduced check and bounds

The existing `transfer_evolve.mode_system` retains six scalar/radiation/dust
states after its action-derived constraints. At the same physical epoch, its
frozen eigenvalue with largest real part, divided by physical `k/a`, is
`0.0392752394`, `0.0394079079`, `0.0394192487`, and `0.0394203635` for
`k=100,1000,10000,100000`. These approach the independent `|Im c|`; radiation
pairs approach `±i/sqrt(3)`. The highest-k normalized eigen residual is
`2.55e-17`; the unscaled constraint matrix condition is `1.35e9`, so this is a
bounded floating-point cross-check, not a numerical theorem about all k.

Five tests passed in 2.964 seconds. The hash-pinned `run_001` completed in
3.278 seconds under a 90-second cap; its manifest validates. The classifier
can return either sign and rejects a singular clock denominator. The earlier
archive samples at `a=0.178173...` and `a=0.100258...` instead give positive
`c²`. Neither is declared a full stability pass. No claim is made for every
epoch or for continuous time intervals between sampled rows.

Regenerate the five tests with `python3 -B -m unittest discover -s` followed
by this directory and `-p test_exterior.py -v`. `run_bounded.py` generates a
new evidence run only when its declared output directory is absent; preserve
the existing archive rather than overwriting it.

## What can evade this specific argument

A nonzero-gradient or otherwise different asymptotic principal jet, an epoch
without this negative exterior discriminant, or a finite domain containing no
such exterior is outside this result. Each still needs actual constraints,
lapse/clock preservation and its own full principal analysis. A finite box
that **retains** an open region with this negative continuum principal symbol
does not remove the local high-frequency problem by imposing outer boundary
conditions. A numerical wavelength cutoff changes the question and is not a
strong-hyperbolicity certificate. Failure of Hessian convergence also evades
the stated limit hypothesis, but is not evidence of a healthy localized
continuation.

The proof-audit and computation-audit skills separated the exact conditional
implication from numerical source evidence. No external novelty assertion or
new mechanism is claimed.
