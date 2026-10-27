# Independent focused review of the shared finite-GP equilibrium proof

**Normalized claim.** For every fixed positive `tau,K,K_b,G,M_d,M_b`, the
energy in `equilibrium/EQUILIBRIUM.md` (3), on its stated nonnegative density
domain with the two separate masses fixed, has a finite attained infimum;
one minimizer is concentric, spherical and nonincreasing, and is a global
minimum against the full three-dimensional admissible domain. The `tau=0`
version drops the scalar H1 condition. The resulting constrained energetic
minimum has no negative admissible regular constrained Hessian direction.

**Primary verdict: proved as written.** This verdict concerns the continuum
functional and the energetic conclusion in §§1–3. The text's original-model
application retains its explicit EOS/EFT assumptions. Its dynamical spectral
conclusion is expressly conditional on its stated self-adjoint/skew-adjoint
Hamiltonian operator domains; no flow construction or nonlinear orbital
stability theorem is supplied or needed for the normalized claim.

Reviewed raw file: `sol61_push/shared_state_2026_10_19/equilibrium/EQUILIBRIUM.md`,
§§1–3, full-file SHA-256 at inspection
`a3808c4fba729e3d705689bffd821ecf6f3f2b68b73b2fd92e4cb02499b08351`.
The source record `equilibrium/SOURCE_CHECKS.md` was read. Review date:
19 October 2026. The reviewer is a different subagent from the author in the
same session, with a direct reconstruction from raw mathematical definitions;
this is not independent external refereeing or a fresh-model guarantee.

## Dependency graph and obligation matrix

| Implication | Leaf type | Outcome |
|---|---|---|
| Matched daughter contact plus declared degenerate baryon closure → functional (3) | model definition / declared state assumptions | passed in stated EFT; physical validity is conditional on its declared regime |
| Fixed masses and Newton near/far split → coercivity (5) | internal analytic estimate | passed |
| Rearrangement of both species → centered decreasing minimizing sequence for the unrestricted infimum | two geometric theorems | passed after exact source check |
| Weak subsequence → nonnegative radial decreasing limit with masses no larger than requested | weak compactness and closed convex cone | passed |
| Scalar Fisher information and positive internal energies → lower semicontinuity | internal convex representation / density topology | passed |
| Radial shell bound plus local singularity estimate → continuity of the full gravitational energy without prior tightness | internal estimate | passed |
| Missing-mass annulus → admissible competitor with strictly lower energy | internal construction and Fisher subadditivity | passed, including a zero weak limit |
| Attainment → full constrained energetic minimum and regular Hessian nonnegativity | variational implication | passed |
| Stationarity → displayed Euler–Poisson equations and Hessian coefficients | internal differentiation | passed |
| Finite-GP positive scalar and negative baryon chemical potential | local elliptic regularity / integrability | passed in `tau>0` portion as stated |
| Nonnegative Hamiltonian Hessian → exclusion of finite-energy growing eigenvectors | operator-domain conditional | conditional exactly as stated |
| Variational minimum → nonlinear orbital stability or uniqueness | no such arrow asserted | out of scope |
| Particular numerical BVP outputs → global minimizers | no such arrow asserted | out of scope |

## Critical reconstruction: continuity before mass retention

The exponent in the potential split is correct. For `p=5/3`, its dual
exponent is `5/2`, and the local Newton singularity has norm proportional to
`R^(1/5)`. Optimization gives

\[
 \|V\|_\infty\le C M^{1/6}\|\rho\|_{5/3}^{5/6},\qquad
 D(\rho,\rho)\le C M^{7/6}\left(\int\rho^{5/3}\right)^{1/2}.
\]

The interpolation `int rho_d^(5/3)<=M_d^(1/3)(int rho_d^2)^(2/3)` then gives
the sublinear negative terms `A^(1/3)` and `C_b^(1/2)` against the positive
linear internal energies. It bounds both species norms and the scalar
gradient energy uniformly along the minimizing sequence.

Radiality supplies the compactness fact needed here even before tightness.
For a radial positive density,

\[
 V(r)={M(r)\over r}+\int_r^\infty{dM(s)\over s}\le{M\over r}.
\]

Consequently, the double integral with at least one point outside a radius R
is at most `2 M^2/R`. This estimate does not assume the sequence has retained
its masses. On a fixed ball, the discarded diagonal region contributes at
most `C M ||rho||_(5/3) epsilon^(1/5)`, uniformly. The remaining bounded
continuous kernel is approximable by finite sums of product tests, so local
weak convergence suffices. Smooth radial cutoffs can replace hard ball and
diagonal boundaries if desired. Letting the cutoff parameters tend to their
limits proves `D_j→D_*` independently of mass retention. Thus the sign of
`E_*<=I` in the author's (7) is correct and noncircular.

The Fisher supremum in (6) also has the correct normalization: maximizing
`grad(a).z-a|z|^2` gives `|grad a|^2/(4a)=|grad sqrt(a)|^2`. It is lower
semicontinuous for the chosen local weak density topology. The domain closes
at the weak limit by finiteness of this relaxed expression.

## Critical reconstruction: annular recovery of all lost species mass

Let the lost species masses be `delta_d,delta_b` and their sum `delta>0`.
The add-back is a *density* sum, not an unsupported sum of scalar amplitudes;
its scalar amplitude is the square root of that sum. The Fisher inequality
in the proof therefore supplies precisely the needed admissibility and
gradient bound.

Because the centered limiting species are nonincreasing,
`rho_i(r)<=3 M_i/(4 pi r^3)` on the annulus. The added density is `O(R^-3)`
there and has fixed mass. Hence the scalar contact increment is `O(R^-3)`;
the baryon `5/3` increment is `O(R^-2)`; and Fisher subadditivity bounds the
quantum increment by `O(R^-2)`. Core–shell Newton interaction is nonpositive.
The shell self-gravity alone is

\[
 -{G\delta^2\over2R}D(\eta,\eta),\qquad D(\eta,\eta)>0.
\]

Its `1/R` magnitude dominates the positive increments for sufficiently large
finite R. The construction restores the *two requested masses exactly*.
It remains valid if one species is wholly lost or if the entire weak core is
zero; no unproved nonzero-core assumption is hidden. Therefore
`I<=E_comp<E_*<=I` is a valid contradiction. No strict subadditivity theorem
or one-component minimizer theorem is being imported to supply this step.

## Equations, Hessian and the exact stability qualification

Differentiating in the scalar amplitude gives
`-tau Delta f+(2K f^2+U)f=mu_d f`; differentiating in baryon density gives
`(5/2)K_b rho_b^(2/3)+U=mu_b` on its positive set. This yields the displayed
positive-part baryon relation. Integrability forces `mu_b<0`: `mu_b=0`
would produce an `r^(-3/2)` tail because `rU(r)→-G(M_d+M_b)`, while positive
`mu_b` gives a nondecaying density. The finite-GP scalar positivity claim uses
`tau>0`, a nonzero nonnegative solution, local elliptic regularity, and the
strong maximum principle. It is not extended to a compact TF scalar.

The exact second derivatives are `tau/2 int rho_d |grad(a/rho_d)|^2`,
`2K int a^2`, `(5/3)K_b int rho_b^(-1/3)b^2`, and `-G D(a+b,a+b)`.
They agree with (11). At a global constrained minimum the finite regular
two-sided tangent Hessian is nonnegative. One-sided free-boundary directions
must retain the admissibility qualification in the text; an undefined or
infinite density second derivative is not an extra finite negative mode.

For the stated Hamiltonian eigenproblem `JLz=lambda z`, with all the displayed
pairings meaningful, skew-adjointness gives
`Re(lambda)<z,Lz>=0`. If `Re(lambda)>0`, nonnegative self-adjoint L forces
`Lz=0`, inconsistent with a nonzero-eigenvalue eigenvector. The paper
correctly makes this a conditional eigenmode statement rather than an
unconditional evolution theorem. It does not establish a strictly positive
gap, uniqueness of the constrained minimizer, completeness of the modes or
nonlinear orbital stability.

## External-source check and limits of this audit

I independently opened the author-hosted [Burchard lecture notes](https://www.math.utoronto.ca/almut/rearrange.pdf),
*A Short Course on Rearrangement Inequalities*, June 2009, copyright
25 June 2009. Theorem 4.1, printed page 33, gives the nonnegative triple
rearrangement inequality for functions with finite positive superlevel sets.
The Newton kernel satisfies that condition and is already decreasing;
the theorem applies to every scalar/baryon pair. Theorem 4.7, printed page 36,
applies to `W^(1,p)` functions; `p=2`, `f=sqrt(rho_d)` gives the scalar
gradient inequality. Equimeasurability preserves both species masses and
internal integrals. Their applications are verified. No PDF was retained
and no retained-file hash is claimed.

The two geometric theorem arrows were authenticated and extracted directly;
the internal compactness and shell steps were reconstructed independently.
No numerical output, full-GP BVP implementation, §4 TF-limit convergence
claim, full source spectrum or original-model production process was audited
in this focused review. No changes to the author's files were made.

Exact remaining gap for the normalized existence/minimum claim: none found.
The cheapest next step for a physical application is an explicitly selected
minimizer in the EFT-valid regime, followed by its source-preserving normal
mode problem. An arbitrary stationary BVP branch must not inherit the
minimum's Hessian sign without a separate identification or check.
