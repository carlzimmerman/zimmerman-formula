# Independent focused review of the particle projection

**Normalized claim and primary verdict: proved as written, within the stated
fixed-N, two-orbital, rigid-host Newtonian projection.** The final reviewed
text is `particle_saturation/PARTICLE_SATURATION.md`, SHA256
`ee0361f2bef00b439559732066f5d569962a38e4720b553d0004d167e57de7fc`.
This verdict covers the full-source projection (11)-(14), the spatial
interaction projection (6)-(10), and finite-matrix high-source statement
(20). It does not verify physical baryon support, continuum convergence,
real formation, or an all-state saturation/normalization claim.

Review provenance: separate occupied-landscape agent, reconstructing the
displayed operators and combinatorics from their definitions. This is a
focused peer review rather than a self-review. No expensive experiment or
new scientific run was performed. Existing run_004 outputs and source code
were inspected; its root-aware v2 validator returned a valid completed
evidence record. Pinning below records the exact reviewed bytes.

## Claim card and dependencies

Objects: N identical positive-mass scalar bosons, one rigid positive-mass
baryon profile with freely translating COM, fixed N, a two-dimensional
orthonormal spatial subspace, and its complete symmetric N-particle sector
of dimension N+1. Interactions are the stated position-only Newtonian
gravity and matched contact; kinetic recoil is retained. The source is the
common sine potential on the complete scalar-plus-baryon mass, with total
COM removed before projection.

The source assertion is equality of the projected manybody operator and
the symmetric-power derivative in (14), including all recoil factors.
The interaction assertion is equality with the Galerkin matrix elements of
(4), with the displayed ordering and one-half second-quantized convention.
The high-field assertion assumes fixed bounded finite matrices H0,D,
E->positive infinity and a simple largest source eigenvalue.

Dependencies are: COM coordinate algebra -> factorized multiplication
operators -> symmetric-tensor representation; elementary Gaussian
integration -> primitive spatial tensors -> orthogonal basis transform;
and ordinary finite-matrix nondegenerate perturbation -> (20). These steps
are reconstructed below. The actual baryon environment and validity of
the two-orbital truncation are named hypotheses, not derived dependencies.

## Source reconstruction

In the unprojected relative coordinates, the exact physical positions are
x_i=s_i-alpha S and Y=-alpha S, with alpha=m/(M_b+Nm). Directly summing
the actual baryon and scalar sine source gives (11). At k=0, its coefficient
is [m-alpha(Nm+M_b)]S=0 as an operator. This cancellation is prior to any
numerical k==0 branch and therefore does not depend on implementation.

For the j-th scalar exponential,

\[
 e^{ik(s_{j,z}-\alpha S_z)}
 =e^{ik(1-\alpha)s_{j,z}}\prod_{i\ne j}e^{-ik\alpha s_{i,z}}.
\]

Let P be the one-particle orbital projection. Compressing this tensor
product gives one factor B=P exp[ik(1-alpha)z]P and N-1 factors
A=P exp[-ik alpha z]P. Differentiation of the symmetric tensor product
Gamma_N(A+tB) at t=0 selects exactly the sum over all choices of j, once
each. It supplies the correct N factor automatically. The host exponential
has only Gamma_N(A), multiplied by the single physical host mass and shape
factor M_b F_b(k). The anti-Hermitian part divided by 2ik gives its sine
operator. Thus (14) is exactly the projection of (11), rather than a sum
of fixed-anchor sources.

I also checked the code's symmetric-power number-basis coefficients.
For input occupation (N-n,n), choosing r left particles to exit right and
t=n'-r right particles to exit right gives powers
(N-n-r,r,n-t,t) of (A00,A10,A01,A11). Its coefficient is

\[
 {N-n\choose r}{n\choose t}
 \sqrt{{(N-n')!n'!\over(N-n)!n!}},
\]

with exactly the bounds implemented in `gamma_and_derivative`. Differentiating
each monomial yields the stated derivative code. No missing boson factorial
or additional factor N was found. N=0 is the identity symmetric power with
zero scalar derivative and zero internal odd host source; N=1 reduces to
m B+M_b F_b A. The existing independent distinguishable-tensor controls for
N=1,2 test this normalization numerically.

The primitive characteristic matrix in (13) follows by completing the square
in phi_i phi_j. The exponential has the midpoint phase and variance
ell^2/2 in the density, hence exp[-t^2 ell^2/4]. Transforming with C on
both sides is correct. The heavy-host limit (15) keeps the finite product
M_b alpha->m in the host recoil term. Expanding the resulting expression
independently reproduces the source coefficient in (16), including both
the a^2/3 geometric term and (B^2-ell^2)/4 width difference.

Disposition: source projection and its stated limits **passed**. The
finite-k norm or small-k power is not a uniform acceleration dipole.

## Interaction and recoil reconstruction

Completing the square in four primitive Gaussians gives the coefficient
(2 pi)^(-3/2) ell^(-3) and the center-variance exponent in (7). With
H2=(1/2) sum v_ij;kl a_i†a_j†a_l a_k, contact has v=g2 I, so no extra
factor two belongs in this tensor. The four-index basis transform C on each
index is correct for the real orbitals.

For gravity, phi_i(x)phi_k(x) is S_ik times a normalized Gaussian density
of width ell about c_ik. The corresponding y density has width ell about
c_jl. Their difference has convolution width sqrt(2) ell, giving exactly
S_ik S_jl erf(d/(sqrt(2)ell))/d in (8). The sign is attractive. The
normal-ordered one-half convention counts each scalar pair once; N=1 has
zero scalar self-interaction. External V uses only the baryon profile, so
scalar self-gravity is not added twice.

Rigid-body recoil expands as

\[
 {1\over2M_b}(\sum_i p_i)^2
 =\sum_i{p_i^2\over2M_b}+{1\over M_b}\sum_{i<j}p_i\cdot p_j.
\]

The first term multiplies the **full projected p^2** kinetic matrix K by
m/M_b. It must not be computed by squaring the projected p matrix. The
code correctly uses (1+m/M_b)K. The second term has matrix elements
p_ik dot p_jl/M_b in the two-body v tensor, because the one-half convention
then supplies sum_{i<j}. Transverse projected p matrices vanish for these
factorized, transversely even Gaussians; only p_z remains. Its primitive
matrix is i hbar(c_i-c_j)S_ij/(2ell^2), as in (6). Products of its purely
imaginary entries are real, so the code's `.real` operation drops no term
in this declared real two-orbital basis.

The contact expansion (10) has the correct direct/exchange factor2 in
2W n_L n_R, coefficient W/2 in pair transfer, and density-assisted hopping
T(N-1) in a fixed-N sector. The code independently compares this expression
with the unrestricted four-index tensor, rather than verifying only the
same closed formula twice.

Disposition: projected contact, gravity, mass polarization and operator
ordering **passed**. The underlying host rigidity and the adequacy of the
chosen Gaussian subspace remain **conditional physical inputs**.

## High-source asymptote

For D|r>=dmax|r> and E>0, write H(E)/E=-D+H0/E. The second-order eigenvalue
correction of the simple branch -dmax is

\[
 -{1\over E^2}\sum_{j\ne r}{|\langle j|H_0|r\rangle|^2
                              \over d_{\max}-d_j}.
\]

Multiplying by E gives epsilon0=-E dmax+h_rr-A/E+O(E^-2).
Hellmann-Feynman differentiation therefore gives
P=dmax-A/E^2+O(E^-3), with A>=0 as stated. The same coefficient follows
directly by calculating source loss from the order1/E admixture amplitudes:
each probability contains a squared source gap denominator and the source
loss multiplies by one gap. This confirms the single denominator in A.

The generic power is exactly E^-2 when A>0. If A=0, every off-diagonal
H0 coupling from |r> vanishes; |r> is an exact eigenvector of H0 and D and
is exactly polarized once its branch becomes the ground branch. The author
removed a preliminary suggestion of a higher-order alternative under the
same hypotheses; this is a text correction with no numerical consequence.
The review pins the corrected final text.

Disposition: (20), its coefficient and simple-eigenvalue hypotheses
**passed** after the stated text correction. Degenerate dmax requires a
different degenerate perturbation argument and is outside this assertion.
Large E is a finite-matrix limit, and does not establish a physical
two-mode validity window at arbitrarily large continuum forcing.

## Existing finite evidence and remaining gap

The inspected run_004 contains ten matrices (N=1,2,4,8,12 crossed with
two g2 choices) of maximum dimension13, with 88 recorded checks and no
reported failure. I checked the actual iterator and did not infer an
unvisited parameter range. The output has positive simple zero-field gaps,
source spectra, conditional populations and response samples, consistent
with the declared finite assertion. The maximum recorded high-field
coefficient discrepancy is about1.9984e-4, below its .004 finite tolerance.
The strongest large-bias control subtracts nearly equal polarizations, so
this is a finite precision check, not a high-accuracy coefficient proof.
The algebraic perturbation argument supplies the stated asymptote.

Validation command executed during this review:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  sol61_push/nonlinear_origin_2026_10_19/particle_saturation/run_004/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The exact remaining physical gap is the same as in the author's calibrated
scope: a supported actual baryon state, a source-complete continuum low-energy
subspace with controlled errors, actual inventory/preparation and an occupied
ensemble. None is supplied merely by finite-N bounded population or by the
correct E^-2 asymptote. No universal G normalization or target rational law
follows from these passed projection identities.

## Exact input hashes

The following block is generated by hashing the reviewed local bytes after
the author's text correction. It is evidence pinning, not a command source.

```json
{
  "reviewed_utc": "2026-10-19T17:59:45.767682+00:00",
  "observed_HEAD": "e54c33252909e38a529a69f7adac265e37b54cb4",
  "reviewer": "occupied_landscape peer agent",
  "primary_verdict": "proved as written within the stated finite rigid-host projection",
  "inputs": [
    {
      "path": "sol61_push/nonlinear_origin_2026_10_19/particle_saturation/PARTICLE_SATURATION.md",
      "sha256": "ee0361f2bef00b439559732066f5d569962a38e4720b553d0004d167e57de7fc"
    },
    {
      "path": "sol61_push/nonlinear_origin_2026_10_19/particle_saturation/check_two_mode.py",
      "sha256": "1d27095a673ab97fd794247008a4b8ab0e1eb40f83d574a6f0f48b24a1fd5a9a"
    },
    {
      "path": "sol61_push/nonlinear_origin_2026_10_19/particle_saturation/contract.json",
      "sha256": "534c52cf2fb3178cd1516696e0a34460f4abcba6835c9cfc36d7a9432fc1b730"
    },
    {
      "path": "sol61_push/nonlinear_origin_2026_10_19/particle_saturation/source_pins.json",
      "sha256": "28e37623b6901f5f18af1e8cbc7db923aaaf58d62bcb17e6f16c5d9255c221f1"
    },
    {
      "path": "sol61_push/nonlinear_origin_2026_10_19/particle_saturation/run_004/manifest.json",
      "sha256": "f52d5dd2ca3b93395ea9c5a56443b454e31c6a4ea2fc401204b1a5b1c7112b0c"
    },
    {
      "path": "sol61_push/nonlinear_origin_2026_10_19/particle_saturation/run_004/results.json",
      "sha256": "c5967b73cdf46fee64b5a9bb222682243d23dde979488ec32c8972d2d1c9f75f"
    },
    {
      "path": "sol61_push/nonlinear_origin_2026_10_19/particle_saturation/SELF_REVIEW.md",
      "sha256": "bc5e846703def64873ae9189c76bb78b625d02c0e36322462f0fd7d9329e2775"
    },
    {
      "path": "sol61_push/nonlinear_origin_2026_10_19/particle_saturation/VALIDATION.json",
      "sha256": "1a08b4aff2285e04502fb3ba071904ed8d8cc825ad0c97b1572e7df58262bf63"
    }
  ]
}
```
