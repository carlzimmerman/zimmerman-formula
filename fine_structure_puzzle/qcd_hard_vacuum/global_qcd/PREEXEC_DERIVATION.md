# Closed SU(3) vacuum normalization beyond the one-plaquette sector

FSP-010. Written before the bounded calculation. The physical A and its charge derivative remain unknown. This is a new microscopic strong-coupling calculation, not physical light-quark data. The inherited Haar, free pion, topology-conditioned and finite-radius estimators are inputs, not new results here.

## Defined microscopic system and exact anchor

Let K_n be the cubical boundary of [0,n]^5, n positive integer. It is a closed four-dimensional cell complex homeomorphic to S4. Every link carries SU(3), every link measure is normalized Haar, and

    Z_n({β_p}) = integral product_links dU exp[sum_p (β_p/3) Re Tr U_p].

All link configurations are integrated; there is no restriction to a topological charge. This coarse Wilson regulator does not give an invariant continuum topological-sector decomposition. The normalization is Z_n(0)=1 exactly. The usual +sum β_p Wilson constant can be restored explicitly; it is not silently discarded in a comparison between geometry-dependent actions. There are no dynamical quarks or photon in this particular computation.

K_n with unit weights has polyhedral intrinsic curvature concentrated on its lower-dimensional strata. It is not a round smooth sphere, nor the slow-curvature physical regulator. The checked primary source hep-lat/9606013v1 distinguishes SH[N] (this complex, n=N-1) from the radially projected weighted S[N], equation (3), and explicitly notes the finite-β metric distortions. We use its connectivity, not its U(1) numerical data or a claimed SU(3) continuum theorem.

The absolutely normalized thermodynamic integration identity is

    log Z_n(β) = integral_0^β db sum_p <Re Tr U_p/3>_b.

Unlike a normalized topological ratio, this fixes the integration constant of this declared regulator. Its finite polynomial computed below is an actual value of log Z to specified perturbative order, not just a formal expectation to be supplied.

## First genuinely connected non-Abelian polymer

Put x=β/6 and c0(β)=integral_SU3 dU exp[x(Tr U+Tr U†)]. Factor c0 at each plaquette. A nontrivial character on an isolated boundary link integrates to zero. Consequently a surviving multi-plaquette support has no link incident to only one occupied plaquette. The bounded enumeration will independently check that on K_1 the only such supports of at most six distinct plaquettes are the forty boundaries of elementary three-cubes. This finite coverage claim is restricted to K_1; the general elementary-cube contribution and cell counts do not depend on that enumeration.

For an elementary cube surface, choose the six fundamental traces with coherent orientation. Each of twelve links appears once as U and once as U†. The elementary matrix orthogonality integral is

    integral dU U_ij U†_kl = δ_il δ_jk / 3.

The resulting color-index contraction has eight free vertex indices and twelve factors 1/3. It equals 3^(8-12)=1/81. Both coherent orientations contribute. Thus the square-free mixed coefficient is

    [product_(p in boundary c) β_p] log Z = 2/(81*6^6) = 18/18^6.

Disconnected cumulant subtractions vanish for that support because every proper nonempty subset has a boundary link. This is a connected full-measure contribution linking six distinct plaquettes. It cannot be obtained from product c0 alone. The independent tensor contraction in the script identifies all index loops using union-find; it does not insert the claimed number 1/81 as its answer.

If there are no additional supports through total degree six, then

    log Z_n = N2(n) log c0(β) + 18 N3(n) (β/18)^6 + O_n(β^7).

For K_1 the support enumeration is the finite completeness check. For general n the displayed cube term is exact but a universal completeness claim requires a separate support argument; the report will distinguish these.

## Cell counts and the absence of a cubic term at this order

A k-cell is specified by k unit intervals and 5-k grid vertices; it is on the boundary precisely when at least one fixed coordinate is 0 or n. Hence

    Nk(n)=binom(5,k) n^k[(n+1)^(5-k)-(n-1)^(5-k)].

In particular N2=60 n^4+20 n^2 and N3=40 n^4. The connected elementary-cube contribution is 720 n^4 (β/18)^6. Both this and the local c0 sector contain no n^3 term. This is a statement about calculated coefficients, not an all-order theorem, a continuum limit, or a physical QCD zero.

At fixed lattice spacing a the polyhedral four-volume is 10(na)^4. Treating the known count polynomials as their smooth extension, their uniform dilation stress is

    rho_truncated = -6 log(c0)/a^4 -72(β/18)^6/a^4 -log(c0)/(a^4 n^2).

This contains an explicit curvature/stratum correction of order 1/(na)^2 but no 1/(na) term through the stated order. The result is not assigned H of the round sphere. Changing β with a matched physical line would add its derivative; no such trajectory is computed here.

## Finite normalized value and conservative certified remainder

For K_1 set M=N2=80 and V(U)=sum ReTr U_p/3, |V|<=M. If P6 is the Taylor polynomial of Z through degree six, Taylor's theorem gives

    |Z(β)-P6(β)| <= exp(M |β|)(M |β|)^7/7!.

For real β>=0 Jensen gives Z>=exp(β <V>_0)=1. A positive computed P6 then gives

    |log Z-log P6| <= remainder/min(1,P6).

This bound is extremely conservative but needs no unproved cluster-convergence theorem or infinite-volume exchange. A declared tiny rational β will give an actual nonzero connected correction resolved against this finite remainder. It is an algorithmic benchmark, not a claimed physical coupling or geometry fit. No sampled data are used.

## Additional normalization handoff, kept separate

For a separately specified curved fermion discretization M_f=1-κ_f B_f whose Grassmann integral is normalized to det M_f(0)=1, exact mass integration at fixed geometry is

    W(β,{κ_f}) = W(β,0) + sum_f integral_0^(κ_f) dk <Tr[(1-k B_f)^(-1) B_f]>.

All other already integrated flavors are retained in each expectation. There is no unresolved additive function of geometry once the common bare measure and local gravitational terms have been specified; evaluating these integrals and matching their local counterterms remain real tasks. This identity alone supplies no light-quark numerical answer. The source 2112.06340v2 equations (4)-(8) verifies its flat Wilson convention; it does not construct B_f on K_n. We will not apply its flat spin factor 16 κ^4 to a curved cell complex without a spin/transport construction.

## Planned orthogonal checks and non-claims

Exact rational SU(3) c0 coefficients will be computed independently by Dynkin-label tensor products and partitions/standard Young tableau dimensions. Cell generation is checked against the count polynomial for n=1,2,3. Closed cube contractions are checked by explicit color identifications for N=2,3,4 (N=3 is the physical gauge group of the declared model). Closed-cell d1 ranks are checked modulo two primes where feasible and compared with N1-N0+1, using actual boundary matrices. The square-free support enumeration is exhaustive only at n=1 and support <=6.

No physical quarks, charge-response insertion, common-path renormalization, round-S4 continuum, uniform large-radius remainder, physical A, proton mass or R is computed. A finite small-β remainder is not uniform in n. The continuation is a weighted round-sphere action plus normalized fermion mass integration and radius/continuum matching; this package does not declare those data absent worldwide.
