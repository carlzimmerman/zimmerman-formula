# Independent review of FSP-N normalization claims

**Normalized claim:** In a finite-dimensional, tree-level, CP-even electric effective theory with fixed charge lattice, positive-definite real symmetric kinetic matrix K, positive-semidefinite mass matrix M2 and conserved sources, the long-range electric-force coefficient is the charge bilinear of the massless propagator residue. With one surviving photon the residue is `n n^T/(n^T K n)`. Consequently, taking a hidden-photon mass to zero and taking momentum to zero need not commute, and fixed kinetic eigenvalues plus fixed charge integers need not fix the surviving photon's coupling.

**Primary verdict: proved as written**, for the corrected revision identified below and the stated tree-level regime. N1-N5's mathematical implications pass. This does not authenticate a UV completion, derive alpha(0), or establish that the exhibited deformations remain on any proposed UV critical surface.

Base checkpoint: **FSP-000**, Git **3c01aa2861bf576f4c2d942251eb9d2f89cae108**. The surrounding repository had pre-existing uncommitted work. Review performed by the delegated archive-audit agent, separately from the normalization note's author. I read the raw CLAIM.md before any implementation or computation output; the independent derivations below do not import the author's checker. No new numerical run, Lean compile or modification of normalization files was performed for this review. The only review artifact written is this file.

## Exact revision and audit provenance

Final reviewed `fine_structure_puzzle/normalization_gate/CLAIM.md`:

`SHA256 d2d1c0a3f6329607ffe45c310ef2a02b871ece33f22013321d741f6273ee6802`

Target contract `fine_structure_puzzle/TARGET.md`:

`SHA256 05e1f2fdc687882e4c55ddf7a6024cf58534d784eb07bcc2fc76d7ad0c0c3a7a`

The first read contained an overbroad introductory formula for “several massless fields.” I independently supplied the `r=3` counterexample below. The coordinator restricted the sentence to **all r fields massless** and added the general kernel formula, then reported the revised hash above. I reread that exact revision with numbered lines and verified its hash. No claim is made to have captured a pre-edit SHA-256 of the earlier text. The correction provenance is part of this review, not concealed as an initial pass.

Physical conventions: rationalized natural units, `D=partial+i q^T A`, `L=-F^T K F/4`; q is held fixed with its physical charge lattice. At static small momentum the coefficient C of `q^T propagator q=C/p^2+regular` gives `V(r)=C/(4 pi r)`, so `alpha_q=C/(4 pi)`. Multiple massless vectors define a force coefficient, without necessarily defining one physical photon.

## Dependency graph and obligation matrix

The mathematical leaves are finite-dimensional real linear algebra, the ordinary block inverse, and differentiation along an admissible smooth curve. The physical leaves are the chosen quadratic kernel, current conservation, charge-lattice identification, and interpreting the massless pole as the long-range electric force. No external theorem about UV completion or strong-coupling running is required for N1-N5.

| Obligation | Status | Evidence / limit |
|---|---|---|
| N1 transformations of K and q and invariant bilinear | **passed** | Direct inverse of `S^T K S`; integer lattice condition checked below. |
| N2 residue for a one-dimensional kernel | **passed** | Independent kernel/complement block inversion below, not the note's square-root proof. |
| General kernel formula added to Definitions | **passed** | Same block proof with a multi-dimensional kernel. |
| N2 independence of normalization of n | **passed** | Numerator and denominator both scale quadratically. |
| N2 integer Higgs example and discrete caveat | **passed** | For nonzero h and nonzero vev, `h^T n=0`; primitive representative has gcd 1. The inherited one-photon hypothesis excludes h=0/zero vev. |
| N3 direct inverse, mass limits and b=0 exception | **passed** | Exact 2x2 inverse and difference `b^2/[a(ac-b^2)]` below. |
| N4 fixed eigenvalues, fixed charge/Higgs vectors, continuous force variation | **passed** | Explicit entries, endpoints and an actual varying tangent below. |
| N4 perturbative anomaly claim | **passed** | Vectorlike Dirac pairs have cancelling chiral anomaly contributions. This is an allowed EFT example, not a UV existence proof. |
| N5 necessary tangent criterion and converse limitation | **passed** | Chain rule along an admissible curve. Actual tangents, not merely formal kernel vectors at a singular constraint presentation. |
| Higher-derivative/contact qualification | **passed in the usual EFT meaning** | Analytic O(z2) terms in the inverse propagator and analytic local source contact amplitudes do not alter the residue. A finite local F2 term changes K and is not an innocuous source contact term. |
| Charge basis / complex-coupling notation translation | **passed** | Independently checked primary preprint Section 2 as recorded below. |
| Magnetic running context | **passed within the cited perturbative EFT scope** | Exact version's Eqs. (5)-(7), not a universal strong-coupling assertion. |
| Unique physical photon and measured alpha in any new UV theory | **out of scope** | These are admission obligations to be checked in an application, not supplied by the note. |

## Independent derivation of N2 and the general formula

Start from the kernel itself, `B(z)=M2+zK`, with fixed finite-dimensional K>0 and M2>=0. Choose an orthonormal Euclidean basis Q for `ker M2` and a complementary orthonormal basis U. Symmetry and `M2 Q=0` imply

`[Q,U]^T B(z) [Q,U] = [[z A, z B], [z B^T, C+zD]]`,

where `A=Q^T K Q>0` and `C=U^T M2 U>0`. For sufficiently small positive z, `C+zD` is invertible, with a finite inverse tending to C^-1. Its Schur complement is

`T(z)=z A-z^2 B(C+zD)^-1 B^T = z[A+O(z)]`.

Hence `z T(z)^-1 -> A^-1`. The off-diagonal block of the full inverse is `-T(z)^-1 z B(C+zD)^-1=O(1)` and the lower block is O(1), so multiplying those blocks by z sends them to zero. Transforming back gives

`lim(z->0+) z B(z)^-1 = Q(Q^T K Q)^-1 Q^T`.

For any full-column-rank basis N of the same kernel, write `N=Q T` with invertible T; substituting cancels T and T^T. Thus the same residue is

`N(N^T K N)^-1 N^T`.

When the kernel is one-dimensional take `N=n`. Contracting with q twice proves N2's exact formula. It also covers `q^T n=0`, when that source has zero long-range electric force. If r=1 and M2=0, the massive block is empty and the formula reduces directly to K^-1. If M2>0 has no kernel, the residue is zero. These boundary cases are consistent.

Finite dimension and fixed matrices supply the positive gap on the massive complement automatically; no gap uniform in a varying hidden mass is implied. This is exactly why N2 can hold at every fixed positive m while the limits in N3 still fail to commute. For an infinite tower accumulating at zero, this finite-dimensional argument does not apply.

The note's independent square-root proof is also correct: `ker(K^-1/2 M2 K^-1/2)=K^1/2 ker M2`, not `K^-1/2 ker M2`. Its stated projection has the correct K powers on each side.

**Earlier scope error and its correction.** Let `r=3`, `K=I`, `M2=diag(0,0,1)` and `q=(1,1,1)`. There are two massless fields, but the exact charge-contracted kernel is `2/z+1/(z+1)`, with residue 2. The earlier phrase would have used `q^T K^-1 q=3`. The corrected sentence now restricts this inverse-K formula to M2=0 and gives the projected-kernel formula for partial masslessness. This resolves the counterexample.

## Independent N1, N3 and N4 checks

**N1.** Since `(S^T K S)^-1=S^-1 K^-1 S^-T`, contraction with `q'=S^T q` exactly recovers `q^T K^-1 q`. For a primitive integral charge basis, preserving all integer q in both directions requires `S^T` and its inverse to have integer entries, i.e. S in GL(r,Z). Real changes of field coordinates are legitimate descriptions only if the period/charge lattice is transformed as well. A scalar rescaling of A without the compensating q/K changes is not a normalization-independent prediction.

**N3.** Set `Delta=ac-b^2>0`. Direct inversion gives

`(zK+M2)^-1 = 1/[z(Delta z+a m^2)] * [[c z+m^2,-b z],[-b z,a z]]`.

For q=(1,0), multiplying the upper-left entry by z yields exactly the note's rational function. At fixed m>0 its zero-momentum limit is 1/a. Setting m=0 first yields c/Delta for all z>0. Their difference is

`c/Delta-1/a = b^2/(a Delta)`,

strictly positive for b!=0 and zero when b=0. More generally, along `m^2=rho z`, fixed `rho>=0`, the limit is `(c+rho)/(Delta+a rho)`. The continuum of joint limits explicitly shows nonuniformity as the massive gap closes. It is not a failure of decoupling at fixed positive gap.

The source's tree-level interpretation is appropriately restricted: after the hidden vector is massive, the massless-pole charge coupling at fixed a is independent of b, although finite-momentum amplitudes, heavy eigenmasses and radiative matching can depend on b. In the exactly massless theory, `1/(a-b^2/c)` is the combined long-range force coefficient seen by q, which need not belong to one unique photon.

**N4.** Adopt `R=[[cos theta,-sin theta],[sin theta,cos theta]]`. Then

`a=cos^2 theta+2 sin^2 theta`,

`b=-sin theta cos theta`,

`c=sin^2 theta+2 cos^2 theta`.

The trace is 3 and determinant 2 identically; both eigenvalues are positive and fixed. With h=(0,1), the unbroken direction is n=(1,0), so N2 gives `4 pi alpha=1/a`. It equals 1 at theta=0 and 1/2 at theta=pi/2, with continuous interpolation. At theta=pi/4 an actual curve within the fixed-eigenvalue constraint manifold has

`d(4 pi alpha)/dtheta = -sin(2theta)/a^2 = -4/9`,

so this is also a concrete nonzero admissible tangent for the N5 test. At theta=0 the first derivative vanishes although alpha varies at second order; this verifies the note's warning that a vanishing derivative at one point does not prove local constancy.

Holding the labelled q and h fixed prevents explaining the family as one field-coordinate change: since q and h span R2, `S^T q=q` and `S^T h=h` force S=I. Additional relabellings or dualities might identify some points, but no continuous identification removing the demonstrated force variation is supplied. The anomaly statement can be realized with a vectorlike q-charged Dirac fermion and the h-charged scalar; scalars do not generate perturbative chiral gauge anomalies and the fermion's left-handed charges occur as a cancelling pair.

## N5's exact logic and interpretation limits

Let an admissible differentiable curve gamma(s) stay in the actual model's constraint set, with gamma(0)=lambda and gamma'(0)=v. Differentiating `F(gamma(s))=0` gives `DF v=0`. If A is locally constant on that admissible set, differentiating `A(gamma(s))` gives `dA(v)=0`. A nonzero derivative along one actual such curve refutes local constancy. This proves the necessary condition in N5.

At a regular constraint point the tangent space is ker DF. At a singular presentation, a vector in ker DF need not be an actual tangent: `F(x)=x^2=0` has DF=0 at x=0 but only the zero admissible tangent. The wording “admissible” and the final paragraph correctly prevent turning every algebraic kernel vector into a valid physical deformation. For implementation, either enforce a regular-level-set condition or construct an admissible curve. Differentiability of F and A and a nonzero coupling, where A is its inverse, are implicit in this differential statement.

Similarly, the statement about higher derivatives should retain its standard meaning: after including all local z-linear quadratic coefficients in K, adding an analytic `O(z^2)` inverse-kernel term leaves the leading Schur complement `zA` intact. A local conserved-source contact amplitude is analytic at z=0 and has no simple pole. A finite Maxwell counterterm changes K itself; it can change the coupling. Nonanalytic massless-loop kernels and an infinite accumulation of thresholds are outside this tree-level analytic premise.

## Primary-source checks, separately attributed

The local `fine_structure_puzzle/sources/` inventory contained bibliography notes rather than cached primary full text. I independently retrieved the following exact primary versions on 2026-10-19 UTC. No copyrighted full text was retained and no local primary-source hash is claimed.

- Del Zotto, Heckman, Kumar, Malekian and Wecht, [*Kinetic Mixing at Strong Coupling*, arXiv:1608.06635v2](https://arxiv.org/pdf/1608.06635), 12 February 2017, matching the cited published title/authors. Section 2, Eqs. (2.5)-(2.8), gives the kinetic action in a charge basis and the complex coupling matrix. Comparing its coefficient `-Im(tau_ij) F_i F_j/(16 pi)` with this note's `-K_ij F_i F_j/4` yields `K=Im(tau)/(4 pi)`. This verifies the convention translation; it is not a source proof of N2-N5. The DOI retrieval returned an internal error, so the authenticated version used here is the primary preprint rather than the journal PDF.
- Newey, Terning and Verhaaren, [*Schwinger vs Coleman: Magnetic Charge Renormalization*, arXiv:2407.13823v2](https://arxiv.org/html/2407.13823v2), 21 November 2024. Eqs. (5)-(7) explicitly use inverse electric/magnetic coupling renormalization, an invariant product and the associated charge quantization convention. This supports the narrow contextual statement about running. The authors' perturbatively controlled effective-theory setting is retained; no universal nonperturbative beta function or absolute coupling is inferred.

Checks performed: version/title/author authentication, extraction of the cited equations and notation translation/application. No novelty search or literature census was performed. Established normalization conventions are background; the finite-dimensional implications above were checked directly.

## Remaining gap and cheapest next check

No unclosed implication remains in N1-N5 for this finite tree-level mathematical claim. The first physical uncertainty is whether a candidate UV model fixes the **projected kinetic coefficient and surviving charge** after its actual symmetry breaking and threshold matching. A free Maxwell deformation is not automatically admissible on a UV critical surface. The cheapest next check is to identify the candidate's genuine admissible tangent directions and contract its actual massless kernel with the explicitly normalized electron charge. A nonzero response along one such tangent disproves that candidate's local predictivity; absence of that response alone does not establish global uniqueness or the measured alpha.
