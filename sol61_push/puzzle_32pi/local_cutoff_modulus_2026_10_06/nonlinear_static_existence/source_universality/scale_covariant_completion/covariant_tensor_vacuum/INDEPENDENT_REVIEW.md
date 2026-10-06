# Independent raw tensor-vacuum audit

Verdict: accepted for the report's conditional tensor-sector statement. No blocking mathematical correction found. The spatial minimizing-source limit alone does not determine a Lorentzian vacuum symbol. Under the separately hypothesized two-sided differentiable eliminated interaction with slope m=1/2, relative-TT derivatives cancel, while a de Sitter curvature term gives an algebraic relative-TT equation. Neither a ghost verdict nor a healthy nonlinear constraint count follows.

## Pinned objects and assumptions

Reviewed REPORT.md SHA256 912ad06793bb41e3c96819f3f7e72db104b44122b31c17bf48a74770cf848287 and checks.py SHA256 834c7132eb34b7a59efb2ef0b59ac98273936ab427f60e07b769e50e6d20a4dd. Inputs are read only. This review uses the repaired averaged metric contraction Υsym, not the unsymmetrized primary invariant. The quadratic tensor claim assumes coincident isotropic backgrounds, no anisotropic tensor stress, K>0, and M_eff(z)=−A+m z+o(z) on both sides of zero. Its proposed critical m comes only from the positive-z radial source branch. No new external theorem is required for the tensor-index calculation; the authenticated primary action/sign convention and source dictionary are pinned in the author's sources/provenance.

## Connection and contraction reconstructed independently

Put d=γ−hatγ, with each spatial perturbation transverse and traceless, and use the determinant-one exponential spatial metrics a²expγ. Direct Christoffel variation gives

δC⁰ij=a²(Hdij+dot dij/2), δCi0j=dot dij/2,
δCijk=(∂j dik+∂k dij−∂i djk)/2.

The H term in the first equation survives the subtraction: Γ⁰ij contains H times the perturbed spatial metric. In Γi0j the inverse spatial metric cancels that contribution. All connection traces vanish by TT conditions.

For the invariant's temporal contraction, g⁰⁰ΣCi0jCj0i gives −tr(dot d²)/4. The spatial contraction involving temporal indices gives tr(dot d²)/2+H tr(d dot d). Their sum is +tr(dot d²)/4+H tr(d dot d). For a Fourier mode choose the wave vector along one spatial axis; TT implies that the corresponding row/column of d vanishes. The remaining purely spatial connections contribute −tr[(∂d)²]/(4a²). Rotation gives the general wave-vector formula, and integration with vanishing surface terms gives the field-space expression. This argument works for any n≥3 and any transverse TT polarization, not only the two matrices used in the finite executable checks.

Thus Υsym²=tr[dot d²−a⁻²(∂d)²]/4+H tr(d dot d). At the coincident background C=0, inverse-metric variations multiply an already quadratic tensor and are cubic; averaging the two inverse metrics therefore changes no quadratic coefficient. Exponential TT metrics have equal determinant exactly, so k=1 and the constant interaction offset has no TT variation in these coordinates.

## EH normalization, action, and lower-order equation

The healthy conventional EH action is +KR in the opposite curvature convention to the primary paper. ADM gives each metric K/4 times the TT derivative quadratic form. For a plus wave exp(u),exp(−u), the determinant is one, trK=nH and trK²=nH²+dot u²/2; direct warped-product spatial curvature is −(∂u)²/(2a²). This fixes both normalization and relative sign without assuming another Planck-mass convention.

With s=(γ+hatγ)/2, the two EH quadratic forms yield coefficients K/2 for the mean and K/8 for d. Since z=−Υsym/(2χ_n a0²), the interaction derivative contributes −KmΥsym. The resulting relative derivative coefficient is K(1−2m)/8, agreeing with the report.

The remaining term is −Km∫a^nH tr(d dot d). For constant m and vanishing time-boundary variations it is +(Km/2)∫a^n(nH²+dot H)tr d². This term must be retained even when the derivative coefficient vanishes. The exact comparison equation is

(1−2m)(ddot d+nH dot d+p²d)/8−m(nH²+dot H)d/2=0.

At m=1/2 in de Sitter, the quadratic potential is KnH²tr d²/4 and its Euler equation is KnH²d/2=0. For H≠0 the unsourced relative tensor is algebraically zero; it is not a propagating mode with negative energy. At flat vacuum H=0 this entire relative quadratic form vanishes. The mean tensor retains positive ordinary derivative coefficients in either case. Whether the nonlinear theory maintains a constraint eliminating the relative tensor, exhibits an accidental linear degeneracy, or is strongly coupled is not settled by the quadratic calculation.

Isotropy ensures that scalar auxiliary/lapse perturbations and scalar/vector shifts do not carry the nonzero-wave-number TT representation, so they cannot restore this derivative coefficient via quadratic constraint elimination on this background. This is a tensor-block statement, not an all-helicity constraint audit. The difference perturbation at coincident backgrounds is invariant under diagonal linear diffeomorphisms; treating it as a lapse gauge mode would be incorrect.

## The missing continuation and order-of-limits leaf

The two-sided assumption is essential. Pure temporal TT variation has Υsym²>0 and hence z<0, whereas the source construction is supplied only on positive invariant arguments. Its m(0+)=1/2 cannot certify the coefficient for temporal variations. If M has a genuine common derivative at zero, M(z)=−A+mz+o(z) and z=O(perturbation²) suffice to compute this conditional quadratic interaction. A one-sided source derivative does not.

On the positive static reconstruction, first minimizing T at nonzero source and then tending to vacuum yields m→1/2. Holding T=0 first gives M(z,0)=−A and m=0. The positive vacuum potential curvature λ does not authorize exchanging those operations: the joint auxiliary action lacks the C² regularity required for the usual smooth implicit-function/quadratic-elimination argument. The source relation T~x^(7/4) also does not specify a minimizer for negative z. The report correctly leaves this ambiguity open instead of certifying either branch as the unique physical vacuum Hessian.

The smallest unresolved implication is admission of a fully defined Lorentzian off-shell interaction/auxiliary branch with a determinate vacuum variation and nonlinear constraints. This audit does not rule out every nonsmooth or differently continued interaction, establish a ghost, prove cosmic growth, or select λ or 32π.

## Executable evidence audited

Independently validated all four current manifests with the standard computation-audit validator against current input bytes: main_a32/32, control_H_a29/32 (three omitted-H contraction failures), control_slope_a31/32, control_vacuum_a31/32. Their intended negative assertions are not alternate theories excluded by check count. The executable directly builds connections, checks traces and n=3,4,5 contractions, independently evaluates ADM coefficients and the integration-by-parts Euler term, and distinguishes the two auxiliary limits. It implements representative polarizations; the general-n and all-TT extension above is a separate index proof. REPORT is excluded from execution inputs, while this review pins its exact hash independently. No author inputs or historical evidence were edited.
