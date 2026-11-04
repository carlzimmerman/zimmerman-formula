# Independent review of the universal-length candidate

**Normalized claim.** With the single fixed physical Gaussian length ell=3 kpc,
the action `U_N[rho]+U_ph[S_ell rho]`, simple nu, both original a0 footings, and
the original baryon population/cuts, there are numerically stable Milky Way
four-cut witnesses; the inherited Solar anomalous quadrupole amplitude is below
the Cassini ceiling.

**Primary verdict: conditional on numerical accuracy of the named MW solver
and its inherited observational premises.** The continuum incremental Solar
theorem is proved for positive Solar mass under its stated whole-space conventions. The
new total-phantom corollary below also passes its mathematical checks. The MW
part is computationally verified at the stated finite resolutions, with
substantial margins and no certified continuum error estimate. Neither part
establishes a generally viable gravity theory or an ephemeris likelihood.

This review independently reconstructed the key constants before reading the
author's completed proof. It inspected the new solver wrapper and selected
literal-source replay, and recalculated the recorded profile scores. It did
not run a fresh nonlinear MW solve. Development of the new total-tide corollary
was separately authorized during this review; that corollary is reviewer-authored
and self-reviewed, with additional algebraic checks communicated by the root
and proof author. It is not presented as an independent audit of itself.

## Dependency graph and obligation matrix

The model chain is: fixed Gaussian energy -> mandatory adjoint response ->
unchanged density/observation inputs -> finite MW solutions -> four-cut witnesses.
The Solar chain is: Gaussian source-field bound + global half-Hölder response
bound -> bounded anomalous increment -> integrable third-derivative Green kernel
-> operator-norm Hessian bound -> the inherited trace-free Q2 convention.
The separate total-tide chain replaces the first two leaves by `|A(u)|<=a0`.

| Obligation | Assessment |
|---|---|
| Variation of the energy and outer adjoint | passed, signs and 4pi G factors reconstructed |
| A single physical ell for all density | passed in definition and new MW wrapper |
| Literal finite U for point masses | requires ordinary Newtonian self-energy subtraction; not needed for the phantom bound |
| Gaussian point/source field supremum | passed, nonnegative finite increment required only for the incremental theorem |
| Global half-Hölder response constant 5^(1/4) | passed, including zero vectors and antiparallel directions |
| Third-derivative kernel tensor, angular moments, radial integral | passed by reconstruction |
| Incremental operator-norm constant <3 | passed for positive M; the null increment is exactly zero |
| Conversion to projected Q2 constant <6 | passed; no axial symmetry needed |
| Total phantom tide from incremental theorem alone | not implied; remedied by a separate authorized corollary |
| Ordinary Newtonian/background tide | outside these anomalous bounds; belongs in the standard dynamical background |
| Source/cut invariance and finite population coverage | passed for the 8,250 saved grid rows |
| Selected MW numerical refinement | passed for the 12 saved cases, conditional on solver accuracy |
| Strict Lh diagnostic | failed for all sampled four-cut witnesses and both selected refined witnesses |
| Full Solar ephemeris, other galaxies, relativistic/dynamical health | not addressed |

## Mathematical reconstruction

With `u=grad N S_ell rho`, varying
`-(4pi G)^(-1) integral H(|u|)`, where `H'(g)=g[nu(g/a0)-1]`, gives
`+(4pi G)^(-1) integral div A(u) N S_ell delta rho` after integration by parts.
Self-adjointness of N and S_ell then gives the claimed outer Gaussian and
`Delta Phi_ph=div A`. The Newtonian half factor yields N rho once because its
bilinear form is symmetric. The physical Newtonian term is unsmoothed. A fixed
prescribed external field can enter u for the local calculation; its fixed
ordinary potential is a separate background contribution to matter dynamics.

The action argument requires boundary/infrared conventions. The author states
the MOND infrared qualification. In addition, the literal Newtonian self-energy
of a point delta diverges at short distance; a point Sun is a valid input for
the smoothed phantom bound without being a finite-energy literal Newtonian
density. Usual point-source self subtraction or a resolved solar density is
needed if one insists on evaluating U itself. This does not alter the claimed
phantom increment or its bound. Reciprocity is qualified by existence of the
second variation, appropriate at zero-field singularities of simple nu.

For the increment, the enclosed normalized Gaussian mass satisfies
`M(x)<=min(c x^3/3,1)` with `c=sqrt(2/pi)`. Therefore the point field is bounded
by `min(cx/3,x^-2)`, whose crossing gives `(c/3)^(2/3)`. Convolution and a triangle
inequality extend this to any nonnegative source increment of finite mass M.
Negative increments or arbitrary signed total variation are not covered by
that particular mass statement; the total-phantom theorem does not need it.

For the Hölder step, the dimensionless radial response magnitude
`f(r)=(sqrt(r^2+4r)-r)/2` is increasing and concave with f(0)=0 and f(r)<=sqrt(r).
Concavity implies `f(s+t)-f(s)<=f(t)`. For vectors of lengths r,s, set
`p=|r-s|` and `t=sqrt(rs)|n-m|`. Then

    |A_dimless(r n)-A_dimless(s m)|^2
      <= p + sqrt(rs)|n-m|^2
      <= p + 2t <= sqrt(5) sqrt(p^2+t^2).

Since the final square root is the original vector separation, restoring a0
gives exactly `|delta A|<=5^(1/4) sqrt(a0 |delta u|)`. No division by a
background-field lower bound occurs, so Newtonian saddles do not invalidate it.

For the kernel, differentiating the radial Hessian of
`F(r)=erf(r/sqrt(2))/r` gives coefficients `a=-15U/r^4`, `b=3T/r^4`, where
`T=P(5/2,r^2/2)` and `U=P(7/2,r^2/2)`. Contracting with unit v,w and writing
`z=v dot w` yields the angular mean square

    r^-8 [15U^2-12UT+6T^2
           +z^2(30U^2-54UT+27T^2)].

The coefficient of z^2 is positive. At z^2=1 the expression is
`45U^2-66UT+33T^2<=33T^2`, using 0<=U<=T. The last inequality follows from
`U(45U-66T)<=0`. Integration by parts gives
`integral_0^infinity T(r)/r^2 dr=integral T'(r)/r dr=2c/3`.
Scaling ell restores one inverse length in the L1 kernel norm. Taking the
supremum over unit v,w is already the operator norm; no component-to-matrix
sqrt(3) factor is missing.

Combining with the source bound gives the factor
`5^(1/4) K`, with `K=(2c sqrt(33)/3)(c/3)^(1/3)<2`, hence less than 3.
For a symmetric Hessian J, the spectral bound
`|n^T J n-tr(J)/3|<=(4/3)||J||op` follows by using the eigenvalues in [-||J||,||J||].
Multiplication by the inherited 3/2 convention gives factor 2, so the stated
incremental bound `|delta Q2|<6 sqrt(G M a0)/ell^2` is correct. The convention is
the project's trace-free diagnostic, not an independently rederived Cassini
data-analysis normalization.

One harmless strict-inequality edge case requires an explicit restriction: if
the general nonnegative increment has M=0, both sides vanish and the strict
inequality should be replaced by equality, or the general statement should use
`<=`. The Solar application has M>0. This correction was communicated to the
author for a separate note, without altering the pinned proof file.

## Total versus incremental Solar signal

The original theorem correctly states that it bounds the change caused by
adding the Sun to a fixed arbitrary background. It does not by itself bound
the pre-existing Galactic phantom Hessian. Thus the word “total” could not be
inserted into that theorem merely because its bound is background-independent.

The new separately authorized [total-phantom corollary](TOTAL_PHANTOM_BOUND.md)
closes this amplitude-level issue for simple nu. Its global response satisfies
`|A(u)|<a0`. Applying the same integrable kernel directly gives

    ||D^2 Phi_ph,out||op < (46/15) a0/ell,
    |Q2_ph,total(n)| < (92/15) a0/ell.

This holds for every axis, location, and almost-everywhere finite field u under
the whole-space inverse-Laplacian convention, with no independent homogeneous
anomalous quadratic potential added. At ell=3 kpc the exact conservative
arithmetic gives:

| Footing | Total phantom Q2 upper bound | Fraction of 5.2e-27 s^-2 |
|---|---:|---:|
| canonical | 6.2017540161e-30 s^-2 | 0.001192645004 |
| alt | 7.4948710437e-30 s^-2 | 0.001441321355 |

The new `total_bound_001` run checks rational constants, including a rational
lower bound on pi, and conservatively includes decimal and binary64 versions
of physical inputs. Its manifest completed and validates. This proves an
anomalous amplitude bound, not an ephemeris fit. The ordinary Newtonian Galactic
tide remains a standard-background modeling obligation; the theorem does not
bound it or reinterpret it as phantom gravity. An isotropic Hessian component
is also norm-bounded here, but no independent observational isotropic cut is
claimed.

## MW implementation and evidence audit

`mw/search.py` calls the unchanged KT34 Cached scan with
`explicit_widths={i: sig for i in ids}`. That explicit argument overrides the
epsilon-width branch. The function still computes RM for reporting, but neither
RM nor the dummy epsilon=0 controls the operator: every selected row receives
the requested exact physical sigma. There is no mass rounding or hidden identity
filter. Each component source is smoothed once, the phantom potential is computed
with the inherited simple nu, and its weighted adjoint is applied outside before
adding the unsmoothed Newtonian potential.

The existing density basis, its coefficients, original prior filter and original
four cuts are unchanged. The enumeration covers 1,375 rows per footing and width
for three widths, totaling 8,250. A read-only replay recomputed chi-squared K,
chi-squared Ou, the fitted logarithmic K scale h, and all cut booleans from the
saved profiles and frozen observation arrays, with zero discrepancies. It also
checked cell/index identity and exact physical width on every row. The resulting
four-cut pass counts are:

| ell [kpc] | canonical | alt | strict passes |
|---|---:|---:|---:|
| 2.5 | 3 | 45 | 0 on both |
| 3.0 | 5 | 39 | 0 on both |
| 3.5 | 0 | 31 | 0 on both |

The cuts used are the intersected local-speed tests centered at 229.1 with
half-width 9.2 km/s and 229.052972972973 with twice 4.644955108173499 km/s;
`cK<=67.45934792232582`; `|K0-66.4|<=4.4`; and
`cO<=59.89250004508689`. Strict additionally requires `|h-2.72|<=.30`.

`mw/refine.py` reconstructs the literal density for frozen canonical cell 1374
and alternate cell 1227, avoiding reliance on the cached decomposition for the
selected replay. All six cases per footing pass the four primary cuts. At the
finest spatial setting, refine=5, their scores are:

| Footing | vc [km/s] | K0 | cK | cO | h [kpc] |
|---|---:|---:|---:|---:|---:|
| canonical | 226.383541 | 69.807995 | 42.811482 | 49.059541 | 3.259835 |
| alt | 225.933377 | 69.227201 | 45.318902 | 36.917752 | 3.267359 |

The closest displayed primary margin is canonical K0, still 0.992005 below its
70.8 upper bound. Both h values fail the 3.02 strict upper limit, and that failure
is stable. Spatial refinement, filter radii 120/240 kpc, outer-domain factors
1/2, mass preservation, negative-source-tail gates, and selected weighted-adjoint
and reciprocity checks are recorded. At refine 5 the negative-source mass
fractions are 5.56e-10 and 8.57e-10. These checks demonstrate numerical stability;
they are not rigorous error enclosures and do not establish all fine-grid pass
counts. The new wrapper does not resolve every inherited solver approximation.

Both witnesses are BV2 models with thick scale length 2.0 kpc and share .35;
both have the maximum listed bulge mass 2.12e10 solar masses. The canonical
witness also uses the largest baryon surface density and both largest scale
heights. The success is therefore within the permitted structured population,
not a broad interior fit or a B175-only success. The historical UX5 stress list
also mentions an a0-times-1.5 sensitivity experiment; no such new-law run was
part of these fixed-a0 tests. This remains an unperformed sensitivity check,
not an extra hidden primary cut or a reason to relabel the verified four cuts.

The continuum source interpretation retains the intended unclipped sech-squared
gas profile. A numerical cosh overflow cap should not be extended literally into
an infinite-mass physical density. The finite grid source and the whole-space
analytic operator remain distinct objects, connected here by refinement evidence.

## Provenance and strongest safe statement

The review inspected the shared checkout at HEAD
`e6e031a163b1bdef3d97eca26d4fd70d663cbf88`; files, not that moving shared HEAD,
pin this audit. SHA-256 values read before the review are:

- Incremental proof README: `529a12ab95a7b56048b6bac7ef7f72691ed191d89408957342564ff751a59761`
- MW search.py: `82a785faab4a46d75f52bffb8ceac83a5ed706a8beac1da737a2032b55c210cc`
- MW refine.py: `045b78cd0f5590915c00569dc52c716ac2886e7a465280e8b10bf23188bda5ae`
- MW universal_grid_001/results.json: `f96322bcc97cbf3294a7bd43ea0cb7594504128f9c53320a6dd8d064cec9f61f`
- MW universal_refine_001/results.json: `547184f262d05430055e4909ddd7032451a9705d5d3e67fc21c7f862237038f1`

The read-only score replay imported the frozen observation arrays but did not
call the original `lines` function; it implemented the displayed formulas
directly. It is an inspection check, not a new solver run or independently
bounded computation record. The original MW run manifests and the new exact
arithmetic manifest were separately validated with the installed mathbox
`validate_manifest.py MANIFEST --root "$PWD"`. The new bounded arithmetic record
pins its own program, proof note and physical/kernel inputs. No old source,
data, criteria, or completed evidence was modified by this review.

The strongest safe statement is a specified one-length nonrelativistic energy
with finite, numerically stable four-cut MW witnesses on both frozen footings
and analytic bounds satisfying the inherited Solar phantom quadrupole amplitude
cut, including its total phantom background. Strict Lh fails. The cheapest
remaining numerical checks are the named historical sensitivity stress and
independent nonlinear solver confirmation of the selected witnesses. Predictions
for dwarfs, other galaxy curves, lensing, cosmology, and a healthy relativistic
completion remain separate scientific obligations.
