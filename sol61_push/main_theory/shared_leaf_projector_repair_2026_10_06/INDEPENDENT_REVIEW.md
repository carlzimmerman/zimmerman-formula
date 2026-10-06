# Independent review of the shared-leaf projector repair

Verdict: accepted for the stated covariant geometry and conditional n=3, Q=1 radiation high-frequency principal repair. No blocking mathematical error found. This does not establish finite-k health, exact static source preservation, cold abundance, or a coefficient selector. I reconstructed the geometric matrix identities and the physical principal frequency without importing the author's script functions; the action/constraint dependency is my independently derived frozen radiation calculation.

## Frozen inputs

- REPORT.md: d7467023b0b4d367e40dfbef8b96c16c7cbca2d5e36e3c0f07f0801f666692f6.
- checks.py: 6bd46080c1346631e0588c74cbd7d692bc315bbda8c8096519a7f5b4cb18f944.
- contract.json: 1fef87c5356020ec8af29339cbf6d4ce1cc3e84e73a451b035ddcff17155826a.
- provenance.json: 9d3ab4d90241ffdecd2b523b2d30bcde70e86b7a53c4f2ac8fbc350472669b37.
- Original radiation REPORT: df1df0faa1a4ff8abdf82cac3e386f79c8f0b1d555a409a378729214c9abbcf2; its final b check script is 6004f297a23e58eb9cdaa36874055390487f358220516201ad0c04945491ba31.

This review is outside the execution input set. No author scientific input was changed.

## Geometry and admitted domain

The common clock must remain timelike for both metrics. Its tangent leaf then carries two genuine positive definite covariant forms γ and γhat. For h=(γ+γhat)/2 and d=(γ−γhat)/2, hλ=h+λ d h^-1 d is positive definite for λ>0: its second term is positive semidefinite and the first strictly positive. Under a leaf basis change C, h and d transform by congruence; d h^-1 d does likewise. Thus the inverse embedded by tangent basis vectors is an actual contravariant spacetime tensor, annihilating dθ. Exchange reverses d twice. Clock relabeling does not change the tangent leaf or the normalized acceleration covectors. No external coordinate metric is needed.

The noncommuting case is essential. Whiten h and define Z=h^-1/2 d h^-1/2. Positivity of h±d gives −1<eig(Z)<1. Both metrics become I±Z in this one whitening chart; they need not commute in the original coordinates. Therefore

(γ^-1+γhat^-1)/2=h^-1/2(I−Z²)^-1h^-1/2,
hλ^-1=h^-1/2(I+λZ²)^-1h^-1/2.

Eigenvalue comparison gives Bλ≤h^-1≤Barith after congruence. Equality is allowed in directions in the kernel of d. The invariant is nonnegative for all real acceleration differences on this admitted clock domain; this does not extend it through loss of common timelikeness.

In θ=t, tangent basis vectors are coordinate spatial vectors even when shifts are retained. Each normal acceleration restricted to the leaf is ∂i ln lapse. Thus Iλ=(hλ^-1)^ij∂i ln(N/L)∂j ln(N/L)/a0² is exact, not a zero-shift-only identity.

## Preservation: the precise perturbative order

Homogeneous isotropic backgrounds have zero relative acceleration. The invariant's value and all first variations vanish there, including variations of the leaf tensor and of the clock. The retained constant envelope/volume/matter equations are unchanged. Its quadratic perturbation term changes only the background inverse-leaf coefficient multiplying the squared linear acceleration difference; variations of that inverse first multiply this square at cubic order.

At coincidence, d=O(ε), Δa=O(ε). The inverse difference is O(d²), so δI=O(ε⁴). M_eff'(0+) is finite; hence the action difference is O(ε⁴). This remains true with a simultaneously varying mean metric: its first-order variation cannot create a linear d difference. It preserves the action through third order and the Euler equations through second order, including the force from the norm-cube action. It does **not** imply preservation of the Euler equations through third order. The report's “cubic norm force” is understood as the force arising from the cubic norm term, not a general third-order Euler preservation theorem.

Nor is this a uniform relative-error theorem after critical cancellations, or preservation of a finite noncoincident galaxy solution. Metric and clock variations of the new tensor are load-bearing for that problem. The report explicitly retains this obligation.

A pure linear TT perturbation on the homogeneous isotropic background has no lapse-gradient acceleration difference. The interaction consequently contributes no quadratic TT term; the retained shear operator gives the same positive 1−η coefficient and cT²=1/(1−η) for 0<η<1. This is a scoped quadratic tensor statement.

## Raw constrained radiation principal check

The actual CY² fluid and both shift/shear/lapse rows are retained in the pinned radiation action. Changing the zero-background acceleration invariant only changes Γ at quadratic order. The three-auxiliary leading determinant remains −Γ(g+j)², so the regular high-k elimination is legitimate for positive Γ. Direct variation gives u=−αχ and the displayed ng,nh solution. Their physical velocity Gram is A(wdot+rχdot)²+Eχdot² with A,E>0.

I separately reconstructed the spatial Schur complement. Substitution produces −2Tχ(χdot+ew)−T(2αℓ+T/Γ)χ². Using actual evolving Tdot/T=r(H−e)+α(2ℓ+H2), and then R=w+rχ, its relative stiffness is T[T/Γ−rH−αH2]. Omitting this time derivative would change the physical gradient and is rejected by the boundary control.

For isotropic leaf metrics the eigenvalue of hλ^-1 in a wave direction is

2PgPh/[(Pg+Ph)(1+λδ²)], δ²=(Pg−Ph)²/(Pg+Ph)².

The factor K a³ follows from the actual interaction coefficient 2K a0² M_eff'(0)=K a0², not an assigned force normalization. Thus Γ=Γcrit/(1+λδ²), Γcrit=Ma³PgPh/(Pg+Ph), and stiffness is λT(rH+αH2)δ². It is strictly positive on the unequal-scale admitted radiation interval, with the radiation principal speed unchanged at 1/3.

A fresh exact symbolic reconstruction gives

ωrel²=λPgPh(Pg−Ph)²/[b0(Pg+Ph)(Ph²+Pg²/L²)], b0=3(1−η)/η,

and zero residual against the report. The admitted L=1/8,Ph/Pg=1/4,η=1/4 fixture gives visible c_rel²=λ/5125. Harmonic λ=0 and equal spatial scales have zero relative leading stiffness, not strict positive sound propagation. No general-n or arbitrary-Q matter stability result is imported from the geometric n-dimensional construction.

## Finite-k and evidence limitations

For ℓ≠0 the exact auxiliary matrix determinant starts positively at small k, Γℓ²(A+B)D, and negatively at high k, −Γ(g+j)². Since the new Γ is a positive k² coefficient, at least one finite-k auxiliary chart rank loss remains. This alone is neither a ghost nor a proven physical singularity; original constraints/canonical variables must be audited at it. Positive UV characteristic coefficients are therefore an actual repair of the previous principal defect, but insufficient for full health. The η→0, k→0 and spatial-coincidence limits are nonuniform exceptions as stated. A finite EFT range must also admit the principal hierarchy before it becomes a physical prediction.

I independently ran the manifest validator on all four current records: all returned exit 0. Raw result inspection found main 20/20; harmonic 20/21 with the declared false strict-positivity assertion; boundary 19/20 with only evolving_gradient_schur false; projector 19/20 with only new_geometric_stiffness false. Harmonic is an interpretation rejection assertion rather than a full mutated-action execution. The two other controls mutate the relevant coefficient/time-boundary calculation. These bounded checks corroborate the algebra and provenance; the matrix/constraint derivation supplies the mathematical claim. No full body likelihood or cosmological abundance follows.
