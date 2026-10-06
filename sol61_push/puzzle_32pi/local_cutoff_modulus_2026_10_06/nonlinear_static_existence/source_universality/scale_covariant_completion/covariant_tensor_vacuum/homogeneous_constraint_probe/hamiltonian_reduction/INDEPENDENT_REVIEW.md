# Independent homogeneous Hamiltonian review

**Primary verdict: accepted as written under the stated regular, homogeneous, rank-three assumptions. No blocking mathematical error found.** The positive critical patch and the negative regular patch are results after the common Hamiltonian constraint and an admissible local clock choice. They do not amount to a full spatial ghost count or a result for the nonsmooth MOND auxiliary completion.

Frozen inputs independently hashed:

- REPORT.md: `3a2dceec1b5b20257d985f582f7b45eac41e941e58521b868ce3d36bd4981472`.
- checks.py: `5741bbe934f6ae771eeb4e59c68a2932d14ab449441c9fed5a3c8b00c4c68e7e`.

I read the raw both-lapse parent action and the frozen report/script. For an independent exact check I constructed the nonzero connection differences `C000=u`, `C0ii=vC`, `Ci0i=Cii0=w` in four spacetime dimensions and performed index sums with each diagonal metric. I did not import the author's functions. Specifically S1 is the inverse-metric contraction of Cαμλ Cλνα; S2 is the product of the metric-contracted upper C trace and lower C trace; S3 and S4 are their metric norms; S5 is the complete metric norm of C. Averaging the two metric contractions and rebuilding the raw Einstein-Hilbert plus interaction kinetic action gives the matrices below exactly. These finite algebraic checks corroborate the analytic reduction, not a field-theory existence theorem.

## Constraint reconstruction

Under N=ell exp(r/2), L=ell exp(−r/2), the relative lapse rate is dot r. The common lapse derivative cancels before variation. The contractions have common-lapse weight −2, and the geometric-mean volume weight +1. Hence the action indeed has the exact form

`L = dot q^T G(q) dot q/(2ell) − ell U(q,T)`,

with q=(alpha,beta,r) and positive U at A>0. On det G≠0 the only primary constraints are p_ell=0 and p_T=0. The Hamiltonian is ell C with C=p^T G^-1 p/2+U. Their preservation gives C=0 and U_T=0. The latter is equivalent to T=0 since its prefactor is strictly positive. The bracket of p_T with T is nonzero; equivalently U_TT=2K chi_n a0² lambda exp[n(alpha+beta)/2]>0. Preservation fixes the auxiliary multiplier. Eliminating this second-class pair does not change the q,p canonical brackets. The remaining pair p_ell,C is first class, and C has no tertiary constraint: after auxiliary reduction {C,C}=0 and there is no explicit time dependence.

Thus the ten-dimensional canonical space has two first-class and two second-class constraints, leaving four phase dimensions, or two local homogeneous configuration degrees. This count is for the declared finite-dimensional model with a fixed fiducial coordinate cell; it is not a count of finite-k field helicities. Constant residual coordinate rescaling does not supply an additional arbitrary-time lapse constraint in this model. Singular det G surfaces require a separate algorithm.

For ell=1, Hamilton's equations are dot q=G^-1 p and dot p_i=dot q^T (partial_i G) dot q/2−partial_i U. They are smooth on the open invertible patch. Ordinary local ODE existence plus exact preservation of C provides on-shell homogeneous admission from the supplied finite constraint data. Homogeneity and isotropy make the spatial off-diagonal/vector equations vanish, while the scale variations give each diagonal spatial equation and the ell/r variations retain both lapse equations. This does not establish spatial PDE well-posedness.

## Independent reduced kinetic reconstruction

At the critical position data the raw index-sum calculation returns

`G = [[4041/256,−4143/16,45/16], [−4143/16,1755,45], [45/16,45,0]]`,

`det G=−14258025/128`, and for v0=(1,1/4,0), `v0^T G v0=−1023/256`. Its inertia is two positive and one negative; it is not negative definite. The potential is 16A and scaling v0 by sqrt(8192A/1023) solves C=0 exactly. Alpha is initially monotone and the rank stays three in a sufficiently small neighborhood. This yields a genuine local homogeneous solution, without requiring r to remain constant.

Eliminating ell at F=dot q^T G dot q/2<0 gives `LJ=−2sqrt(−FU)`. Direct differentiation gives

`Hess_v LJ = ell^-1 [G−(Gv)(Gv)^T/(v^T Gv)]`.

The null vector is v, as required by time reparametrization. Restricting to an internal-clock slice removes this null direction; for a negative-norm constrained v it removes one negative inertia direction of G. In the alpha clock slice at the critical datum I obtain

`R_beta,r = [[3357498,231120],[231120,16875]]/341`,

with determinant 9505350/341 and positive first minor. It is positive definite. The lapse choice here is ell=1 on the scaled constrained data, so no unreported overall negative factor occurs.

For the regular m=xi=1/4, eta=0 coincident representative, the independent raw Hessian in (h1,h2,u) is

`K [[−45/4,−3/4,3/4], [−3/4,−45/4,−3/4], [3/4,−3/4,−1/4]]`.

Changing to tau=(alpha+beta)/2 and zeta=alpha−beta gives mean component −24K, no mean-relative cross term, and relative block

`K [[−21/4,3/4],[3/4,−1/4]]`.

The relative block determinant is 3K²/4 and its first minor negative: both directions are negative. The exact coincident de Sitter solution has H²=a0² A/6 and satisfies the common constraint. Since the constrained velocity is exclusively along tau, the Jacobi projection removes the mean direction and leaves precisely this negative block. These signs are consequently not merely the unreduced gravitational conformal sign or a bare relative-lapse Hessian. The report appropriately stops short of a full finite-k ghost spectrum, unrestricted reduced-Hamiltonian unboundedness, or an all-BIMOND exclusion.

## Evidence validation and remaining implication

I independently ran validate_manifest.py with the repository root for all four current manifests. Every record validates against current artifact hashes:

| Record | Result | Interpretation |
|---|---:|---|
| main_a | 30/30 | Exact checks pass |
| control_rank_a | 30/31 | Rejects negative critical reduced kinetic inferred from rank alone |
| control_count_a | 30/31 | Rejects three-mode count after omitting the common constraint |
| control_regular_a | 30/31 | Rejects positive classification of the regular reduced block |

Each control has exactly its declared unique failure. Validation establishes evidence consistency, not the physical verdict by itself. The raw constraint and Jacobi derivation above establish the restricted verdict. No author execution input was changed, and this peer note is not a runner input.

The regular linear action's algebraic T=0 equation and the off-coincident invertible patch cannot be transplanted into the actual source auxiliary envelope. Nor do these examples decide the full scalar/vector constraint spectrum, gradients, critical TT degeneracy, or a nonlinear source-compatible Lorentzian completion. Both examples admit data for arbitrary positive A and lambda; neither selects the vacuum coefficient. These are the exact remaining physical and normalization implications, and the report states them adequately.
