# TP01: corrected law and certificate dictionary

1 November 2026. The normalized target is to identify the isolated law actually
used by the stated action and numerical solvers, and to assign every cited
certificate only to its actual hypotheses. **Verdict: the former S=B identity
is refuted; the corrected dictionary is proved under the stated stationary
and scalar-ansatz restrictions.** This is a documentary correction retaining
the existing simple-μ action and its fit results, not an adoption of a new kernel.

The starting checkout was dirty at requested base
`0fe706856e8a897a9ab350be4931dbf36416ada4`. `INPUTS.json` pins the raw inputs;
the coordinator's `../initial_sources/` preserves both summary before-images.
`summary_corrections.patch` is against those initial dirty bytes, not Git HEAD.
`EDIT_RECORD.json` verifies that the entire frozen verdict before-image remains
an exact prefix, including its pre-existing corrections and dated additions.

## 1. Exact dictionary and domain

Let a₀>0, g_N>0, x=g/a₀ and y=g_N/a₀. The isolated algebra below requires
spherical stationary fields, μ_K=0 and no screening contribution. In a general
geometry the AQUAL PDE does not reduce to this algebraic relation. Distinguish
logarithmic curvature d²ln(g/a₀)/d(ln y)² from the curvature of any other graph.

| Object | S: executed simple-μ law | B: exact squared-excess law |
|---|---|---|
| μ(x), x>0 | x/(1+x) | (√(1+4x²)−1)/(2x) |
| ν(y), y>0 | (1+√(1+4/y))/2 | √(1+1/y) |
| Spherical identity | g²=g_N(g+a₀) | g²=g_N²+a₀g_N |
| Positive g/a₀ | (y+√(y²+4y))/2 | √(y²+y) |
| At y=1 | (1+√5)/2 | √2 |
| Acceleration excess | 0<g−g_N<a₀, limit a₀ | 0<g−g_N<a₀/2, limit a₀/2 |
| Log slope | (x+1)/(x+2) | (2y+1)/(2(y+1)) |
| Log curvature | x(x+1)/(x+2)³ | y/(2(y+1)²) |
| Curvature maximum | y=2, x=1+√3, value 1/(6√3) | y=1, value 1/8 |
| (g²−g_N²)/(a₀g_N) | (1+2x)/(1+x), varying from 1 to 2 | 1 |

Both kernels have the leading deep limit g²∼a₀g_N and hence the leading
circular-orbit BTFR v⁴∼GMa₀. The theorem `deep_tully_fisher` assumes the exact
deep relation g²=a₀g_N; it does not prove a finite-acceleration interpolation.

For S, y=x²/(1+x), so g−g_N=a₀x/(1+x) proves its strict excess bounds and
limits. For B, g−g_N=a₀y/(√(y²+y)+y), with denominator greater than 2y.
At zero baryonic field both positive branches extend continuously to g=0;
the displayed strict inequalities are for g_N>0.

The S logarithmic derivative follows from

    d ln y/d ln x = (x+2)/(x+1).

Its curvature derivative with respect to x is

    d[x(x+1)/(x+2)³]/dx = (−x²+2x+2)/(x+2)⁴.

There is exactly one positive stationary point, x=1+√3. The derivative is
positive before it and negative after it. Since y(x) is strictly increasing,
the global curvature maximum is at y=2. These are different landmarks from
the B certificates; sharing the deep asymptote does not identify them.

The smallest exact mismatch witness is a₀=g=1, g_N=1/2: S holds, while B
would require 1=3/4. At equal y the two predictions also obey

    (g_S/g_B)² = (1+x)²/(x²+x+1) ≤ 4/3,
    4(x²+x+1)−3(1+x)² = (x−1)².

S is strictly larger than B for positive y. The largest relative discrepancy
is 2/√3−1=15.4701%, attained at x=1 and y=1/2; it is 0.0624694 dex.
This is a prediction discrepancy with a common a₀, not a refitted likelihood.

## 2. External-field claims require their own hypotheses

For an *additional aligned scalar ansatz* take x>0, b=g_bar/a₀≥0 and e≥0,
with x μ(x+e)=b. The equations are

    S: x²+(e−b)x−b(1+e)=0,
    B: (x²−b²)(x+e)=bx.

For S, multiplying by 1+x+e is reversible because it is positive. When b>0,
the quadratic's constant term is negative, its roots have opposite signs and
its unique positive root is

    x = [b−e+√((b+e)²+4b)]/2.

When b=0, neither ansatz has a positive root: its nonnegative solution is x=0,
outside the certificates' x>0 domain. For S the zero-external-field response
is dx/de=−1/(x+2); for B the corresponding certified derivative is
−1/[2(b+1)]. These response formulas are conditional on a differentiable
solution branch and the aligned composition.

The original B certificate's squaring implication is reversible under its
x>0, e≥0, b≥0 sign hypotheses. Its uniqueness theorem states **at most one**
positive cubic root; positive-root existence is explicitly not certified in
that file. Neither scalar identity establishes the physical aligned ansatz
or the complete vector/PDE EFE. The P4 code instead imposes external-field
boundary data in its S-kernel AQUAL solve. Those existing numerical results
are not recomputed or regraded here.

## 3. Stationary action and units

For the nonrelativistic field convention μ(x)=dF(z)/dz at z=x², primitives
with F(0)=0 are

    F_S(x²)=x²−2x+2 ln(1+x),
    F_B(x²)=x√(1+4x²)/2+asinh(2x)/4−x.

The displayed covariant convention has Y=A·A/c⁴. Therefore use the geometric
inverse length a_geo=a₀/c² and u=√Y/a_geo, so

    J_S(Y)=Λ−2a_geo²[u−ln(1+u)],
    J_B(Y)=Λ+a_geo²[F_B(u²)−u²].

Differentiation gives 1+J'_S=μ_S(u) and 1+J'_B=μ_B(u). The summary previously
used SI a₀ in the geometric slot without stating c=1; the correction makes
its convention explicit. The B primitive is a comparison dictionary, not an
adopted replacement or proof of high-field admissibility, stability or a
complete covariant model. Changing kernels in a future model would require
new empirical fits and affected screening/health calculations.

The summary's unversioned BS24 “Eq. 35” locator is removed. The Oct 28 review
had proposed arXiv:2404.06584v1 Eqs. (44)–(45), but the coordinator's direct
primary-source check found different numbering. The authenticated locators
are [arXiv:2404.06584v1](https://arxiv.org/pdf/2404.06584v1), §III.A.6,
Eq. (3.21), p.11 for the stationary equation and §III.A.7, Eq. (3.22), p.12
for the kernel relation. Eq. (2.5) defines Y, with A as physical acceleration
in Eq. (2.3); J has inverse-length-squared units. This is the coordinator's
source verification, not an independent source reauthentication by this
route. The direct kernel algebra above supplies the internal dictionary.
No new source download was performed by this route.

## 4. Dependency and certificate audit

| Leaf / implication | Exact hypothesis and outcome |
|---|---|
| Literal J_x → S kernel | Exact differentiation with the stated geometric units; passed |
| Isolated spherical S PDE → S algebra | Requires stationary μ_K=0 unscreened spherical reduction; passed in this restriction |
| Existing P4/CL3 law functions → S | Raw pure functions extracted by AST without importing solver engines; verified on the declared finite grid |
| `EQB_A0LINE_uniqueness.affine_excess_unique` | ν(y)>0 for every y>0, y²(ν²−1)=αy+β for every y>0, and ν(y)√y→1 at 0+; then β=0, α=1 and ν=√(1+1/y). Conditional B theorem; no action supplies its affine premise |
| `simple_nu_not_linear` | Explicit S countervalues exclude squared excess linear through the origin; no rewrite needed |
| `EQB_S1_rar_landmarks` | Assumes B and y>0; its anchor, slopes, reciprocal curvature and sum rule belong to B |
| `TOEBestAttempt.newton_recovery` | g,g_N,a≥0 and g²=g_N²+a g_N imply g_N≤g≤g_N+a/2; a B theorem |
| `TOEBestAttempt.deep_tully_fisher` | Positive orbital radius and exact deep relation; shared deep-regime algebra, not an interpolation selector |
| `EQB_S5_efe_cubic` | B μ plus aligned scalar composition; sign assumptions as above; at-most-one-positive-root conclusion. No existence or PDE theorem |
| `V3_PICTURE_2026_10_23.coupling_one_is_law` | Its α=1 conclusion b(1+x)=x² is S; the summary's “a₀-line” label was misleading |

The original certificate files were read and remain unchanged. The new
`LawDictionary.lean` adapts only S balance, its Newtonian excess, scalar S EFE,
the exact mismatch witness and the algebraic ratio bound. It does not import
or rewrite the old EQB statements. Formal algebra, symbolic identities,
finite numerical comparisons and physical validation have distinct scopes.

## 5. Current entry points and edit boundaries

Directly corrected `covariant_push_2026_10_22/V3_FULL_PICTURE.md`: J units,
authenticated version-specific source locator, spherical identity, Newtonian bound,
landmarks, affine-certificate premises, scalar EFE, coupling label, schematic
and certificate inventory. Added one dated scoped erratum to
`V3S_FINAL_VERDICT_2026-10-24.md`; all earlier bytes are preserved.

Inspected the current links and neighboring claims in root `README.md`,
`covariant_push_2026_10_22/THEORY_V3_DRAFT.md` and
`rebuild_2026_10_22/THEORY_STATEMENT_2026-10-26.md`. The current links do not
assert the false S=B identity themselves. The draft correctly declares
μ=x/(1+x); its generic “exact law” wording is not an explicit B certificate.
The historical README kernel alternatives and the separately audited route-E
floor-emergence claim are not rewritten by this correction. No paper,
sealed prediction, empirical input or formal theorem was edited.

## 6. Verification and remaining work

`contract.json` states the exact finite assertion and input closure. The
checker performs 20 symbolic identities, the exact counterexample, the
existing P4/CL3 pure-function comparison on 2001 logarithmic y points from
10⁻¹⁰ to 10¹⁰, 25 positive-b scalar EFE cases and four zero-b boundaries.
The handwritten algebra above supplies the universal implications.

The runner's unsupported macOS CPU-affinity request was rejected before
output creation. Retrying with a 1 GB RLIMIT_AS also failed before launch;
both `*_001/manifest.json` records preserve that outcome. Successful retries
omit unsupported affinity/address-space enforcement and retain 60 s wall,
50 s CPU and one numerical thread. The arithmetic run `run_002` completed at
72,482,816 bytes peak RSS, with all 24 checks passed and its manifest validated
against current inputs. Its 20 symbolic identities are distinct from the four
regression/boundary check groups.

The first actual adapter compile, `adapter_002`, exposed tactic/API errors.
After those were corrected, `adapter_003` compiled all five theorems but used
5.76 GB with the broad Mathlib import. Narrowing only the imports produced
`adapter_004`: compiler exit 0, all five axiom footprints exactly
`{propext, Classical.choice, Quot.sound}`, and no `sorryAx`, at 1,542,733,824
bytes observed peak child RSS. Its manifest remains **failed** because the
explicit 1 GB RSS assertion failed. The theorem-compilation result and the
resource failure are both retained; no resource gate was relaxed. This was
one adapter, not a whole-library build. No further Lean run is needed for
the documentary correction.

`LAUNCH_PRECHECK.json` and the run manifests state these limits; no unprovided
memory hard cap is claimed. Historical failed manifests pin their historical
script bytes; current-input validation is asserted only for `run_002` and
`adapter_004`, the latter with its failed resource status. Final file hashes,
proofreading and outcome reconciliation are in `VERIFICATION.json`.

No empirical fit, full-library Lean build, source download or production
simulation was performed. No scientific parameter or coefficient is selected
by these repairs. The actionable documentary mismatch is corrected; a single
predictive physical completion remains a separate open problem. Independent
cross-review is recorded in the coordinator's
`../COORDINATOR_DICTIONARY_AUDIT.md`, which independently reconstructs S/B,
the landmarks and the S EFE quadratic. It was read only after this route's
adapter statements and proofs were final. Agreement is not physical validation.
