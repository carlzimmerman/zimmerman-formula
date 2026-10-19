# FSP-007: sea quarks and curved QCD

**The full physical R(alpha)=A_rho/m_p^3 and its constrained charge dependence remain uncalculated.** No alpha value or cosmological target was fitted. This phase evaluates additional sea and gravitational-response components; their different kinematics and quark-mass regimes prevent adding them into a physical ratio.

## New sea data, with a definite remaining kernel

The [sea-data route](sea_lattice/REPORT.md) authenticates a disconnected proton-current moment in Wang et al., arXiv:2310.01168v3, Table II. The two published ensembles give 1.4(1.2) and 0.1(1.8), in 10^-4 fm^3, for the disconnected part of the indicated electric-polarizability moment. These are separate ensemble results, not combined here into a fitted number or interpreted as a proof of vanishing sea response.

This is a new measured QCD data functional beyond the previous connected-only stencil. Its published electromagnetic unit prefactor is retained symbolically as alpha_ref; it is not used as a proposed value of alpha. The source's spatial-current sum, state normalization and the relation to a raw Euclidean Compton slope are audited in the lane. The moment precedes an experimentally supplied residual term; full flavor/current coverage, truncation, continuum and covariance limits remain explicit. The public source archive does not provide the full current tensor and covariance needed for the mass convolution.

Fresh source review corrects one diagram attribution in the frozen lane: the two Figure S3 drawings are two computed same-loop contractions with different nucleon Wick contractions. The second drawing is not identified by the source as a vacuum-subtraction product. Vacuum subtraction is established separately by the text after equation (11). The [correction note](reviews/curved_sea/SOURCE_DIAGRAM_CORRECTION.md) preserves the original files and exact source evidence. The published table and its numerical transformation are unchanged.

A static value and a low-momentum slope do not determine that convolution. Exact inverse-data counterexamples in the sea lane and [coordinator calculation](coordinator/UV_MATCHING.md) preserve those moments and a leading ultraviolet coefficient while changing the intervening function. These are demonstrations of information insufficiency, not alternative microscopic QCD solutions. In particular a vacuum-subtracted sea covariance has no automatic positive spectral measure from which to infer a mass bound.

## An evaluated short-distance sea contribution

The [OPE calculation](sea_ope/REPORT.md) derives the hard same-loop gluon coefficient, scalar/twist-two mixing and the full photon angular integral. Spin-two contributions that appear in the subtraction function cancel in the complete traced tensor. For the declared massless three-flavor SU(3) theory, a photon band Q0<|Q|<2Q0 has the asymptotic zero-charge response

lim_(Q0/m -> infinity) (1/m) partial_(e^2) M_band = -log(4)/(216 pi^2) = -0.0006502823404878044.

No empirical alpha, mass or strong coupling enters that limit. It is a finite-band response in a fixed-flavor massless theory, not the complete physical sea mass. Finite masses require sigma fractions, and physical high scales require threshold matching. The source's gluon OPE operator is not an invariant decomposition of the entire sea topology: singlet quark/gluon operators mix and soft contractions remain.

The scalar ultraviolet logarithm cancels against the required mass/strong counterterms. The source counterterm delta g has mass contribution -delta g partial_g M; confusing it with a boundary-coupling increment reverses the sign. Independently, the [mixed-running calculation](coordinator/UV_MATCHING.md) shows how the common local scale direction is removed by proton matching. In the massless limit its contributions to A_rho and m_p scale in the ratio three to one and cancel from A_rho/m_p^3, conditional on that coefficient existing. This does not cancel or evaluate the finite infrared sea response.

## A calculated unconditioned vacuum response

The [curved-response calculation](curved_response/REPORT.md) evaluates the leading chiral two-pion cut of the vacuum trace correlator:

rho_Theta(s)=sum_a (s+2M_a^2)^2 sqrt(1-4M_a^2/s)/(32pi^2).

Its third dispersive moment has a closed finite-cutoff expression. Extending the LO pion formula formally over its entire cut gives 17 sum_a M_a^-2/(2240pi^2); the physical full moment additionally needs higher chiral orders and the QCD tail. The cutoff expression permits an actual low-energy contribution without extrapolating the pion formula into the UV. Twenty independent spectral/Feynman-parameter kernel checks agree within the stated numerical tolerance.

The charged-pion mass contribution is computed as a function of e^2 with the independent strong coefficient C left explicit. The primary curved chiral source also supplies an independent electromagnetic curvature operator k15 and photon corrections. Its isolated moment contribution is calculated, with normalization and scale dependence retained. Neither mass splitting alone nor an assumed value of k15 gives the full charge response.

The scheme-independent object is the spectral cut. Its dispersive R(-Box)R coefficient is not the total gravity-EFT coefficient if an independent local dimension-six term is present. More decisively, this derivative-curvature term vanishes on homogeneous round S4. The k15 positive-mass local sphere expansion has even powers of H, so it is not an adjustable linear-H coefficient. A flat quadratic response is therefore not turned into the global one-point vacuum energy by setting momentum equal to H. The unconditioned sphere functional and its remainder still need to be measured or derived.

## Current literature and the missing prediction

A genuinely new 2026 QCD-dark-energy paper was checked in [LATEST_QCD_DE_CHECK.md](coordinator/LATEST_QCD_DE_CHECK.md). It implements cosmological phenomenology while retaining a conjectural geometry transfer and unevaluated c_H. Its fits were not imported. This updates the literature boundary without claiming that current work has already computed the missing vacuum/proton matching.

All finite results above are conditional on their declared QCD parameters, source conventions and effective-theory regimes. They cannot be combined by setting missing matrix elements to zero or choosing normalizations to obtain 137. The physical calculation still needs the full individual-proton current kernel including sea terms, common mass/charge/strong matching, and unconditioned curved vacuum stress or partition-function differences with controlled continuum and radius limits. These routes remain open, with concrete next data and contact measurements in the handoff.
