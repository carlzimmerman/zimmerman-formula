# Independent review of the corrected Gaussian epsilon scan

Reviewer: sibling agent `epsilon_review`, 2026-11-04. This review separates
the exact continuum operator, the finite Milky Way discretization, and the
finite epsilon coverage. It does not repeat the full observational scan.

The reviewed family is

```
Phi[rho] = N rho + S_sigma* Phi_ph[S_sigma rho],
sigma = epsilon sqrt(G M_b/a0),
nu(h) = 1/2 + sqrt(1/4 + 1/h).
```

Source and outer Gaussian standard deviations are equal. The width is fixed
during source variations. The Newtonian term is unsmoothed. Both original
acceleration footings, the 1,375 allowed baryon cells on each footing, the
external Solar field, and all observational cuts remain separate and fixed.
The Milky Way retains KT25's log-width rounding with step 0.005. This is a
scan of an authorized physical parameter, not a blind validation or a
derivation of that parameter.

## Implementation and coverage review

The Milky Way cache expands each original density into gas, bulge, and
exponential disk basis functions. Its gas coefficient is one, its bulge
coefficient is `M_bb/M_bulge_mcm`, and its disk coefficients reconstruct the
original surface density at R0, thick share, scale lengths and heights.
Linear filtering and Newtonian solution commute with this expansion; the
nonlinear phantom response is still evaluated separately for each cell.
Thus the cache is an acceleration of the KT33 construction, not an
approximation that averages baryon models. The epsilon=0.5 comparison to
KT33 and literal-density controls provide independent finite checks of the
implementation of this identity.

The imported KT33 code still uses the weighted adjoint of the normalized
Gaussian and the exact derivative of its finite cell energy. In particular,
after column normalization, the outer operation is not a second forward
source-filter call. Its cutoff, spherical-harmonic order and spatial lattice
remain numerical approximations that need checks at newly used widths.
For narrow kernels, an integrated negative-density check alone cannot
establish resolution: a normalized under-resolved radial kernel can approach
the identity numerically. For very broad kernels, keeping a 120 kpc filter
cutoff while sigma approaches that scale would not approximate the declared
whole-space Gaussian. The analytic large-width bound below avoids that latter
issue entirely.

The exact-width worker's dual acceleration is also algebraically sound.
Let l be the row that forms the inherited radial gradient at R0, including
its sine/cosine transform and bilinear interpolation. With `WL=L^T W`,

```
l S* [-L^-1 W^-1 G^T W A]
  = -[G L^-1 S(W^-1 l^T)]^T W A.
```

The Gaussian on the dual source is the forward S. The minus sign and absence
of an extra 4pi are correct for the KT33 phantom-potential convention.
Precomputing this row for each quantized width removes the per-cell final
Poisson solve without altering the observable. I checked the explicit
`radial_functional` against `Grid.interp_cells` at Z=0. Literal full solves
are retained to verify the implemented dual identity. The transitional
full-cut worker only skips states failing the necessary L1 cut; every L1
survivor receives the complete original cuts. Near a floating-point cut,
the dual comparison must be assessed relative to its reproduction error.

For a fixed cell with nominal radius R_M, every width is constant on a bin

```
exp(0.005*(k-1/2))/R_M < epsilon < exp(0.005*(k+1/2))/R_M.
```

Exact endpoints use the original Python round-to-even rule. Exhaustive
coverage of a bounded epsilon interval requires every intersecting width bin
for every cell, including endpoint bins. A shared coarse epsilon list does
not establish that coverage. Nor does smoothing alone prove that a radial
force, an observational chi-square, or the best model over the population is
monotone in epsilon. Any finite scan conclusion must retain these distinctions.

## Cassini findings and independently checked tail

The new Cassini wrapper imports the corrected KT33 formula without changing
the source/outer kernel, physical prefactor or origin-surface convention.
All sampled ceiling and signed-quadrupole crossings are searched. The
refined equality points are

```
canonical: epsilon = 0.5156064781076973,
alt:       epsilon = 0.5928184097198396.
```

At each crossing, refinement and an expanded radial domain preserve the
ceiling equality; the independent flux and density forms agree within
4.5e-14 in dimensionless q. The 407-point sweep per footing finds no sign
reversal. Its tiny-width apparent extrema occur on the almost constant
plain-QUMOND plateau and disappear as significant features on refinement.
This supports a single passing branch numerically; it is not a proof that
there can be no narrower unsampled branch.

The large-width coefficient was derived independently in Fourier space.
Writing `eta=gext/a0`, the external-field linearization has phantom multiplier
`(nu(eta)-1) + eta nu'(eta) k_z^2/k^2`. The two Gaussians combine to variance
`2 epsilon^2`. The trace-free zz angular average is
`<mu^4-mu^2/3>=4/45`, giving

```
q = [2 eta nu'(eta)/(45 sqrt(pi))] epsilon^-3 + O(epsilon^-7)
  = -epsilon^-3/[45 sqrt(pi) eta sqrt(1/4+1/eta)] + O(epsilon^-7).
```

Parity removes the quadratic source-field term. The numerical tail controls
agree with this coefficient. The expression is for the signed trace-free
Hessian under the repository's convention, not an isotropic Hessian or a
complete ephemeris prediction.

I also checked the uniform Cassini bound in `cassini/README.md`. With
`c=sqrt(2/pi)`, the source field satisfies
`g <= (c/3)^(2/3) epsilon^-2`. For epsilon>=1, both footings therefore have
`eta/2 <= |g rhat + eta zhat| <= 3 eta/2`. Both `nu-1` and `abs(nu')`
decrease on this interval. The source Jacobian bound
`||J|| <= div(g rhat)+2g/r` and the angular factor
`(1/2) integral |3mu^2-1| dmu = 4/(3sqrt(3))` give the stated radial bounds.
Splitting at x=1 gives `I1 <= c^2/75+c exp(-1/2)` and
`I2 <= c^2/225+1/3`; the constants, signs, and powers are correct.
The separately checked rational slack yields

```
abs(Q2)/ceiling < 45/epsilon^3    for epsilon >= 1.
```

Consequently every epsilon>=4 passes this Cassini quadrupole criterion.
This is an analytic tail statement; it does not rely on interpolation of
the sampled quadrupoles.

## New continuum Milky Way tail bound

The following lemma is a new derivation from this review. Its hypotheses
are nonnegative finite source mass M, inversion symmetry about the origin,
no external field, the simple nu function, and equal source/outer isotropic
Gaussians of width sigma. All original continuum Milky Way baryon models
have those symmetries. It does not assume spherical baryons, compact support,
or pointwise monotonicity in sigma.

Here the continuum gas density means the intended, unclipped sech-squared
profile. The numerical source routine uses `cosh(min(|z|/h,300))` to avoid
overflow on its finite grid. Extending that numerical cap literally to
infinite z would create a positive constant floor and infinite total mass;
that function is not the continuum finite-mass source in this lemma. The
finite computation and the intended physical density agree to negligible
precision in the affected tail, but this distinction is mathematically
necessary.

Let `u=grad N(S_sigma rho)` and `A(u)=(nu(|u|/a0)-1)u`. If
`c=sqrt(2/pi)` and `kappa_bound=(c/3)^(2/3)`, the Gaussian point-source
Newtonian field obeys

```
F(x)/x^2 <= min(c*x/3,x^-2) <= kappa_bound,
||u||_infinity <= kappa_bound G M/sigma^2,
||A||_infinity <= sqrt(kappa_bound) sqrt(G M a0)/sigma.
```

Here F is the Gaussian enclosed-mass fraction. The field bound extends to
any nonnegative source by convolution and its total mass. The last
inequality uses
`(sqrt(h^2+4h)-h)/2 <= sqrt(h)` for h>=0.

It remains to bound the derivative of the outer-smoothed longitudinal
projection of A. Set sigma=1 temporarily and
`f(r)=erf(r/sqrt(2))/r`. With n the radial unit vector, its third derivative
is

```
D^3 f = a nnn + b (delta_ij n_k + delta_ik n_j + delta_jk n_i),
a = -15 U/r^4,  b = 3 T/r^4,
T = P(5/2,r^2/2),  U = P(7/2,r^2/2),  0 <= U <= T.
```

P is the regularized lower incomplete gamma function. These identities
follow by differentiating the Gaussian enclosed-mass expression. For unit
vectors v,w with t=v dot w, the angular mean of the squared norm of the
vector contraction `D^3 f[v,w]` is

```
r^-8 {15U^2-12UT+6T^2 + t^2(30U^2-54UT+27T^2)}.
```

The coefficient of t^2 is positive:
`30U^2-54UT+27T^2 = 30(U-0.9T)^2+2.7T^2`.
The maximum is therefore at t^2=1. Since U<=T,

```
mean_sphere |D^3 f[v,w]|^2
 <= (45U^2-66UT+33T^2)/r^8 <= 33T^2/r^8.
```

Angular Cauchy--Schwarz, followed by radial integration, gives

```
(1/(4pi)) integral |D^3 f[v,w]| d^3y
 <= sqrt(33) integral_0^infinity T(r)/r^2 dr
 = 2 c sqrt(33)/3.
```

The last equality follows by integration by parts using
`T'=c r^4 exp(-r^2/2)/3`. Restoring sigma gives an additional factor
sigma^-1 for this kernel norm. The physical Green function supplies the
`1/(4pi)` already included above. Hence

```
||grad g_ph,outer||_infinity
 <= K sqrt(G M a0)/sigma^2,
K = (2 c sqrt(33)/3) (c/3)^(1/3) = 1.965073088... < 2.
```

For an elementary safe constant, `c<.8`, `sqrt(33)<5.75` and
`(c/3)^(1/3)<.65` imply `K<1.99334<2`. Inversion symmetry makes
`g_ph,outer(0)=0`. Integrating its derivative on a straight segment proves
the uniform force bound

```
|g_ph,outer(x)| <= 2 sqrt(G M a0) |x|/sigma^2.
```

At the equatorial observation radius R0, the radial phantom force can
therefore increase the squared circular speed by at most
`2 sqrt(G M a0) R0^2/sigma^2`. Including the worst logarithmic width
rounding error, this yields

```
v_c(R0)^2 <= v_N(R0)^2
  + 2 sqrt(Gk_solver M a0k_solver) R0^2 exp(0.005)
      /(epsilon^2 R_M,width^2).
```

The units in this application must be kept literally separate:
`Gk_solver=G_SI M_sun/(KPC_solver*1e6)` and
`a0k_solver=a0_SI KPC_solver/1e6`, while `R_M,width` uses the original
`Gk_width=4.30091e-6` and `KPC_width=3.0857e19`. The tempting replacement
of the numerator by `2 a0k_width R0^2/R_M,width` misses a factor
`sqrt(G_SI M_sun/(Gk_width KPC_width*1e6))=1.0000123...`.
The accepted arithmetic uses the direct physical expression above. No new
physical mass or scale is selected by this inequality.

Using the frozen KT33 doubled-grid Newtonian speeds and nominal masses,
the largest upper bounds at epsilon=2.5 are 213.601921 km/s canonical and
217.867430 km/s alt. Both are below the necessary L1 lower bound 219.9 km/s.
The expression decreases for every larger epsilon, so this gives a uniform
large-width exclusion of the stated Milky Way family. Even allowing every
Newtonian speed an extra 1 km/s and every physical source mass an extra 1%
while keeping its assigned width fixed leaves upper bounds 214.603914 and
218.870866 km/s. These explicit allowances quantify robustness; they do not
constitute certified error bounds for the baseline density integration.

Accordingly, the analytic force lemma is independent of discretization;
its application to this numerical baryon family is conditional on the
recorded Newtonian baseline and mass normalization being accurate within
the displayed margins. It is not a proof that every finite discrete
harmonic filter satisfies the same continuum kernel inequality.

The sibling `epsilon_cassini` independently reconstructed the source-field
bound, third-derivative tensor, angular moments, sigma scaling, projection
normalization and inversion argument. That fresh review found the small
width/solver gravitational-unit mismatch and the continuum interpretation
of the numerical cosh cap described above. Both are retained explicitly.

The reproducible accepted arithmetic is `review/tail_bounds_v2.py`, with
`review/contract_tail_v2.json` and `review/tail_002/results.json`. Its bounded
manifest validates with status `completed`; all 2,750 rows and exact rational
slack checks pass. The original `review/tail_001` is preserved: it completed
its stated arithmetic but omitted the small unit correction, and is
superseded rather than counted as an accepted physical upper bound. The
analytic lemma remains separate from both numerical arithmetic records.
An independently written scalar replay in
`cassini/mw_tail_audit_001/results.json` obtains the same bounds on all
2,750 cells using solver constants extracted from their source file; its
bounded manifest also validates as completed. The maximum discrepancy of
the stored finite-grid total mass from the nominal mass is 1.84e-6
relatively, well inside the explicit 1% robustness allowance.

## Independent completed-coverage audit

The independent `review/coverage_audit.py` rebuilds the state counts from
the frozen KT33 masses and cells, using direct integer bounds rather than
the production overlap loop. For one cell and closed band [lo,hi], the
covered width integers satisfy

```
ceil(log(lo*R_M)/0.005 - 1/2) <= k
    <= floor(log(hi*R_M)/0.005 + 1/2).
```

It compares each cell's count and the population at every individual width,
rechecks the original scalar cut labels of all recorded full-cut survivors,
checks uniqueness and domain membership, and recomputes the passing pairs.
The independent bounded run `review/coverage_001` completed and its manifest
validated. All checks passed.

| Footing and band | Cell-width states | Distinct widths | Result |
|---|---:|---:|---|
| canonical, [0.515606478108, 2.5] | 435,481 | 354 | no L1 passes; maximum vc=216.989125 km/s |
| alt, [0.592818409720, 2.5] | 397,062 | 326 | no L1 passes; maximum vc=218.178474 km/s |
| canonical, [0.3, 0.515606478108] | 150,398 | 147 | 25 all-cut passing states |
| alt, [0.44, 0.592818409720] | 83,407 | 98 | 57 all-cut passing states |

There are 832,543 exhaustively evaluated cell-width states in the bands
above the numerical Cassini thresholds, all below the necessary 219.9 km/s
local-speed cut. The maximum negative-mass upper bounds there are below
9.8e-7, and the weighted mass checks pass. Literal dual/full comparisons
agree within the declared tolerance. This enumeration does not assume
monotonicity and leaves no untested MW width bins in those closed bands.

The transitional runs give finite-model passing suprema
0.3135487841273574 canonical and 0.4652841727713697 alt. Their passing
closed covers within the tested transition bands are respectively
[0.3, 0.3135487841273574] and [0.44, 0.4652841727713697]. These are upper
edges of quantized numerical bins, not continuum estimates accurate to all
printed digits. The independent audit checks 2,507 and 770 necessary-cut
survivors respectively. Every other enumerated state fails L1 and cannot
pass all four cuts.

The completed `mw/checks_run` independently reevaluates every transitional
necessary-cut decision. Its closest rejected distances from the L1 boundary
are 8.6246e-5 km/s canonical and 0.0017621 km/s alt, whereas the largest
dual/full disagreements are 5.4e-9 and 3.6e-9 km/s. The prefilter therefore
did not discard a state within its measured numerical reproduction error.
Its positive-basis-coefficient assertion also justifies the conservative
negative-mass bound used throughout the width enumeration.

At three times spatial resolution, the worst local speeds in the
Cassini-admissible bands are 217.004300 and 218.192876 km/s. Increasing the
filter cutoff from 300 to 600 kpc leaves these displayed values unchanged.
The checked epsilon=2.5 endpoint is similarly stable. Those changes remain
far below the L1 rejection margins. These are empirical convergence tests,
not certified continuum errors for every state.

The transition endpoints are more sensitive. `mw/endpoint_run` shows that
the canonical last passing bin at doubled/tripled resolution fails L3 at
four/five times resolution, shifting its selected passing edge down one
bin to about 0.311985. Some alternate terminal candidates also change their
K(R0) or Ou grade under refinement. They cannot be promoted to sharp
continuum endpoints or exhaustive fine-grid counts. The useful physical
comparison is therefore an MW upper edge around 0.31 canonical and 0.46 alt,
far below the Cassini thresholds; the exact finite-grid bin data are retained
above for reproducibility.

## Disposition and remaining qualifications

Primary verdict: **computationally verified in the stated finite ranges,
with an independently checked analytic large-width bound conditional on
the numerical Newtonian baseline and continuum mass normalization**.

The Milky Way needs substantially less smoothing than the numerically
observed Cassini passing branches allow. Every MW width state from those
Cassini onsets through 2.5 fails a necessary cut, and the continuum tail
bound excludes every larger width under its named baseline qualification.
Consequently no common window is found for this fixed Gaussian model and
original baryon family. This is much stronger than a sparse epsilon scan.

The remaining global qualification lies primarily on the Cassini side:
the 407-point sweep and refined crossings do not constitute an
interval-certified proof against an arbitrarily narrow lower-width Cassini
island. Finite-grid observational accuracy is also empirical. Thus a
practical rejection of this specified Gaussian route is supported, while
an unconditional theorem for all positive widths is not claimed. A
universal claim over all Gaussian kernels, varying source prescriptions,
or other baryon families would not follow from these results.

Only KT34 review artifacts were written by this reviewer. Original KT33
and earlier inputs were read and hash-pinned, never changed. The bounded
review arithmetic and coverage runs used Python 3.9.6, no randomness,
30-second wall and 20-second CPU limits, one numerical thread, and 1 MiB
log caps. Their contracts, before/after input hashes, statuses and output
hashes are retained beside each result. A completed manifest is evidence
of execution, not a substitute for the mathematical review above.

Final mathematical proofreading covered this review's new text and displayed
formulas. Display delimiters and local notation were checked. No unrelated
file or mathematical token was corrected as proofreading. The substantive
unit correction and continuum-source qualification came from the independent
proof audit and are recorded explicitly above.
