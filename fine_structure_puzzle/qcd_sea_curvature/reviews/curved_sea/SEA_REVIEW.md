# Independent review: published sea-current moment

Normalized claim: the included disconnected ii contribution reported in Wang v3 Table II gives a finite-lattice, finite-time estimator of one proton current moment. It can be converted linearly into the slope of Fu v2's raw scalar subtraction amplitude along its specified imaginary-energy line, with conventional alpha_ref kept symbolic. It does not determine the complete physical-flavor sea response or a proton electromagnetic mass convolution.

Primary verdict: **correct only after a stated restriction**. The source-to-moment and moment-to-raw-amplitude conversion pass within the published estimator's limits. Restrict the Figure S3 attribution as recorded in SOURCE_DIAGRAM_CORRECTION.md: both upper drawings are computed same-loop disconnected Wick contractions with different nucleon contractions; the source text, rather than the second drawing, establishes vacuum subtraction. Frozen author artifacts are unchanged. No other blocking issue found in the focused normalization/source-data claim. Broad alternative-paper conclusions in the author's report were not re-audited here.

## Independence and exact revision

PRESEA_SOURCE_DERIVATION.md was saved from the primary Wang v3 and Fu v2 sources before opening the arriving sea_lattice target package. The independent derivation distinguishes raw calligraphic T1 from modified T1 and fixes the spatial and 2M normalization. The completed author package subsequently arrived and was compared against that derivation. This is an isolated-review pass, with the named local attribution correction; agreement alone is not evidence beyond the displayed derivation/source checks.

| Audited artifact | SHA-256 |
|---|---|
| sea_lattice/DERIVATION.md | a464a9946027f5f1f0c5d16aa4022daf3c368655c1809b44fc6eebf0db26c277 |
| sea_lattice/REPORT.md | 17f530b5460d4603c384c4b3cec2a8ddcc2292b8e650530a56fe547d08c745f7 |
| sea_lattice/INPUTS.json | 32be3b56028961a37cb09de6fc71f609926ed7aa2f7c6e0496b3ee84d0191b8b |
| sea_lattice/SOURCE_RECEIPTS.json | 027f9b288b22946206c7f0346be1ae0e9ae363b8e357be5d94339710b4178f3e |

SEA_CHECKS.json pins the actual audited bytes and verifies the first two primary-source receipt entries against locally retained files. No Git revision/dirty-state claim is made.

## Dependency graph and claim verdicts

`Wang current convention + spatial sum + state normalization -> t² moment -> reported included-disconnected estimator` is the source chain. `Fu tensor normalization -> raw U(Q²) -> cosine expansion -> U'_disc(0)` is the translation chain. The conventional electromagnetic prefactor is stripped algebraically. There is no arrow from that one moment to an all-momentum tensor or renormalized photon convolution.

| Claim | Primary verdict | Evidence and restriction |
|---|---|---|
| Table II reports 1.4(1.2), 0.1(1.8) in 10^-4 fm³ | externally proved in the exact required form | Wang v3 Table II, printed p6, visually checked and compared with TeX. These are source estimates with reported errors, not exact physical constants. Same included contribution is shared by proton and neutron. |
| Spatial/state normalization and alpha_ref stripping | proved as written | Equations(1),(7),(9), text after(14) give the factors below. The ii contribution precedes alpha_E^r; the conventional alpha_ref divides out without importing total polarizabilities, radius or magnetic moment. |
| Raw Fu derivative and numerical row transforms | proved as written | Fu v2 equations(12),(13),(15) plus cosine expansion give U'_disc(0)=−P_disc/(4pi alpha_ref). Printed rows become (−3.5e−5 ±3.0e−5)/(pi alpha_ref) and (−2.5e−6 ±4.5e−5)/(pi alpha_ref) fm³. |
| Application of that derivative identity as a physical numerical input | conditional on a named input | Conditional on the published finite-lattice, finite-time estimator and the source matching conventions. Its temporal truncation, omitted contractions, flavor inventory, scale/current normalization and unquantified systematics remain limits. |
| Figure S3 second drawing identifies vacuum subtraction | incomplete, with the smallest missing implication | Both drawings show the same closed two-current loop and differing nucleon contractions. Source prose independently establishes the subtraction; no drawing-to-factorization implication is supplied. See SOURCE_DIAGRAM_CORRECTION.md. |
| Only a bounded current moment has been acquired, not complete sea self-energy | proved as written | A single t² moment does not reconstruct momentum/tensor dependence; omitted SU(3)-vanishing classes are stated by the source. No complete flavor-resolved tensor, UV contacts or matching path derivative is inferred. |
| Signed-profile illustration preserves the stated constraints | proved as written | Exact rational moments and transform checked independently below. It is only a mathematical illustration in a broad signed-function class, not a constructed QCD spectrum or physical mass bound. |
| Inspected source archives contain no raw tensor/covariance dataset | computationally verified only in a stated range | Exact inventories of the two pinned archives were independently inspected: Wang57 regular files and Fu12, detailed below. This says nothing about all websites or all future data. |

Not addressed in this focused review: independent authentication of the report's BMW, QCDSF, RM123 and ensemble-scale-setting papers; the completeness or success of its web/GitHub data search; the full-Fu optimized curve as numerical input; any UV tensor/RG coefficient. These rows are not silently passed. The primary Wang/Fu formulas suffice for the bounded moment conversion reviewed here.

## Source extraction and normalization

X.-H. Wang et al., *Nucleon electric polarizabilities and nucleon-pion scattering at the physical pion mass*, [arXiv:2310.01168v3](https://arxiv.org/abs/2310.01168v3), 30 August 2024, defines the spin-averaged forward tensor with an explicit 1/2 in(1). Its ground-state completeness in(9) includes 1/(2E); the text after(14) states the nucleon normalization 2ML³ while the Npi state uses L³. The intermediate-state amplitudes are not imported by this review. In(7),

`P_disc = alpha_E^{ii,disc} = −alpha_ref/(12M) integral dt t² H_disc(t)`,

`H_disc(t)=integral d³x sum_(i=1)^3 <N|T Ji(x)Ji(0)|N>_disc,sub`.

The ii components are summed. For the reduced summed correlator `C_sum=H_disc/(2M)`, its t² moment is `−6P_disc/alpha_ref`. If one instead defines the spatially averaged reduced correlator `C_avg=H_disc/(6M)`, the result is `−2P_disc/alpha_ref`. The 2M state factor and the factor3 spatial average are separate. Neither changes the source's already summed formula.

Y. Fu et al., *Lattice QCD calculation of the subtraction function in forward Compton amplitude*, [arXiv:2411.03141v2](https://arxiv.org/abs/2411.03141v2), 1 February 2025, uses tensor normalization 1/(8pi M) in(1). Its raw calligraphic amplitude on the specified kinematic line is

`U(Q²)=mathcal T1(i|Q|,Q²)=−integral dt cos(|Q|t) H(t)/(24pi M)`.

Equation(13) defines a different object, `V(Q²)=−4pi alpha_ref[U(Q²)−U(0)]/Q²`. Equations(13),(15) imply `V(0)=alpha_2=alpha_E^{ii}` and `U'(0)=−alpha_2/(4pi alpha_ref)`. The table row therefore determines the raw slope estimator, or the modified function's zero limit. It determines neither the modified function's slope nor either function at all momenta. No extra spatial factor is applied to Fu's 1/(24pi M), which already includes the 1/3 average.

The published disconnected row does not include the elastic/Born residual alpha_E^r. Dividing it by the source's conventional alpha_ref strips one known prefactor. It is not a fitted alpha, a full dynamical sea-charge derivative or a physical-alpha prediction. Alpha_ref remains symbolic; no numerical electromagnetic or hadron calibration is newly inserted into the transformation.

## Data and scope receipts

SOURCE_CHECKS.json records the retained primary versions, hashes, byte counts and exact archive member inventories. Authentication uses title/authors/version banners in the retained primary PDFs, source TeX agreement and visual inspection of Wang Table II/Figure S3 and Fu printed p3. The Fu arXiv v2 metadata were also checked online. Old-version browser fetches for Wang/Kubis did not succeed; their retained exact primary PDFs were inspected rather than treating a failed fetch as source evidence.

| Primary source | PDF SHA-256 | Exact-source archive SHA-256 |
|---|---|---|
| Wang2310.01168v3 | c216213c240e2a2b01457874a3e0e0f49fc6319623501358923d41ac3a61de4e | fa6d93e893b89bca42221fe4f6fbf65bbca3a0edc1f96d9559a443371b5df098 |
| Fu2411.03141v2 | 3361b8ef1a047b0578c8ae9afccc3641a79878451932881220be7910d8831438 | 138915310cdda2eb3539277098e0966e0784841e14bb3f9b55b619d9e0347635 |

Wang's archive contains 57 regular files:54 PDF figures, one TeX, one BBL, one BIB. Fu's archive contains12:10 PDF figures, one TeX and one BBL. No raw H_munu array, configuration/bootstrap samples or covariance file was identified in these archives. Plot PDFs can support visual inspection; they do not recover the full tensor or joint statistical covariance. This is an exact inventory of specified archives, not a global data-unavailability claim or a completed GitHub search.

The source's Figure S3 estimator uses t0=0.77fm(24D),0.72fm(32Dfine), with current-to-source/sink separation parameter Delta t=0.96fm,0.86fm. These are finite-window estimates, statistically compatible with zero. No ensemble combination or continuum extrapolation is performed. The same reported p/n component cancels in their difference and should not be treated as two independent measurements.

Wang states that disconnected diagrams vanishing in the flavor-SU(3) limit were omitted. At unequal strange/light masses this does not prove physical flavor completeness. The inspected source does not give enough flavor-separated data to reconstruct a full light/strange charge inventory. The ensembles have dynamical 2+1 QCD sea quarks; that fact does not turn the selected zero-charge current moment into a complete finite-charge QCD+QED sea derivative. Current renormalization and ensemble scale setting are inherited conditional inputs, not reconstructed here.

## Independent bounded arithmetic check

Command: `python3 fine_structure_puzzle/qcd_sea_curvature/reviews/curved_sea/check_exact_sea.py`.

Completed on CPython3.9.6/macOS26.5.2 arm64. SEA_CHECKS.json records target hashes, primary receipt comparisons and literal row transforms in exact rational arithmetic. For the author's signed profile with c=(7,−112,243,−128), k=(1,2,3,4), exact arithmetic gives `sum c/k=0`, `sum c/k³=0`, `sum c*k=0`, and

`2 sum c*k/(z+k²) = 5040 z²/[(z+1)(z+4)(z+9)(z+16)]`.

Hence its zeroth and second temporal moments vanish, the leading 1/z cosine-transform tail vanishes, and F(1)=252/85. Integrating the rational transform gives `4992log2−2916log3`, numerically256.6372915990387. These calculations validate only the stated mathematical example and rounded-data arithmetic. They are independent review evidence, not a retroactive claim that the author packet contained a manifest-backed run.

## Remaining gap and strongest safe statement

The safely reusable new input is the published, included-disconnected finite-window moment and its exact normalization/linear conversion, subject to the local Figure S3 attribution correction and source systematics. It is more information than a connected-only estimator, but it is not a complete sea mass response.

The cheapest meaningful next acquisition is a flavor/topology-resolved, unoptimized proton current tensor H_munu(x), normalized nucleon/vacuum subtraction, current-renormalization convention and joint samples/covariance, together with temporal/source-sink metadata. All physical contraction classes and the renormalized photon-kernel/contact matching on a declared strong/quark-mass path are required before computing a full sea self-energy. No complete proton mass derivative, curved A_rho, R(alpha), finite-alpha function or alpha root is established by this review.
