# Sea-current temporal moment and its limited Compton implication

## Authenticated convention

[Wang et al., arXiv:2310.01168v3](https://arxiv.org/abs/2310.01168v3), equations (1),(4),(7),(9)-(11), Table II and supplemental subsection “Contributions from disconnected diagrams”/Figure S3, supplies a nonperturbative sea datum. The source is the accepted PRL version, revised 2024-08-30. Table II on PDF page 6 was checked against the TeX and visually against the PDF. Its two disconnected rows are also shared by proton and neutron. Define

\[
H_{disc}(t)=\int d^3x\sum_{i=1}^3 H^{ii}_{disc}(t,\mathbf x),\qquad
P_{disc}=\alpha_E^{ii,disc}
=-\frac{\alpha_{ref}}{12M}\int dt\,t^2H_{disc}(t).
\]

The spatial components are **summed**, not averaged. Source equation (1) has a factor 1/2 multiplying the Fourier transform of the spin-averaged current tensor. The proton state normalization is the relativistic one in equation (9), with completeness measure d^3Q/[(2pi)^3 2E]; the text below equation (14) also states <N|N>=2ML^3. No additional spin or spatial factor is inserted here. The source's intermediate-state normalization below (11) differs and is already included in its amplitudes; those amplitudes are not numerically imported.

The source decomposes the total polarizability as alpha_E=alpha_E^{ii}+alpha_E^r. Equation (10) gives alpha_E^r in terms of electric charge, anomalous magnetic moment and charge radius. The extracted **disconnected ii row** precedes addition of alpha_E^r. Neither alpha_E^r nor a total/PDG polarizability is imported. The row is a QCD current moment multiplied by alpha_ref for conventional polarizability units, not an electromagnetic measurement used to calibrate that moment. The declared QCD ensemble and its physical scale setting remain conditional inputs. The printed source does not expose the numerical alpha_ref or native normalization needed to reconstruct an entirely numerical bare-unit moment here, so alpha_ref remains symbolic.

The source uses 2+1-flavor domain-wall QCD ensembles, 24D and 32Dfine, spatial sizes approximately 4.63 and 4.58 fm, inverse lattice spacings 1.023(2) and 1.378(5) GeV, 207 and 82 configurations. The local vector-current normalization is imported by the authors from Feng, Jin and Riberdy, arXiv:2108.05311; this normalization was not independently reconstructed here. The lattice-spacing calibration is a QCD hadron calibration; the cited ensemble-method paper Ma et al., arXiv:2308.16755v2, Table I explicitly states Omega-mass scale setting. Thus this is not a no-input prediction of QCD parameters. No source bare coupling/mass matching derivative is inferred from the reported moment.

## Exact conversion to the raw Fu amplitude

Use a separate symbol U for Fu's raw scalar amplitude, avoiding the PDF's collapsing of calligraphic and modified T symbols. [Fu et al., arXiv:2411.03141v2](https://arxiv.org/abs/2411.03141v2), equations (1),(12)-(15), defines

\[
U(Q^2)=\mathcal T_1(i|Q|,Q^2)
=-\frac1{24\pi M}\int dt\,\cos(|Q|t)H(t),
\]

\[
V(Q^2)=-\frac{4\pi\alpha_{ref}}{Q^2}[U(Q^2)-U(0)],
\qquad \alpha_2=V(0)=-\frac{\alpha_{ref}}{12M}\int dt\,t^2H(t).
\]

The 1/3 spatial averaging needed to extract raw T1 is already in Fu's 1/(24pi M). Expanding cos yields

\[
U'_{disc}(0)=\frac1{48\pi M}\int dt\,t^2H_{disc}(t)
=-\frac{P_{disc}}{4\pi\alpha_{ref}}.
\]

Applying this linear transformation to the **printed** Table II rows gives

\[
U'_{disc}(0)\big|_{24D}
=\frac{-3.5\times10^{-5}\ \pm\ 3.0\times10^{-5}}{\pi\alpha_{ref}}\;\mathrm{fm}^3,
\]
\[
U'_{disc}(0)\big|_{32Dfine}
=\frac{-2.5\times10^{-6}\ \pm\ 4.5\times10^{-5}}{\pi\alpha_{ref}}\;\mathrm{fm}^3.
\]

The errors are the transformed source marginal statistical errors, not total theory errors. The input rounding alone can shift each displayed central numerator by up to 1.25e-6 fm^3 if the displayed one-decimal rounding is nearest rounding; no unrounded source data were acquired. There is no numerical alpha in this conversion, no fit and no combination of the ensembles. The amplitude relation is for a common source tensor and normalization. Its application to the reported row is a **finite-truncation estimator**: it does not certify an infinite-time/continuum derivative. It evaluates an imported nonperturbative sea moment, not the full proton mass derivative.

## Which sea contraction was actually seen

Figure S3's two upper drawings were visually inspected from the separate source PDFs gram_disc1.pdf and gram_disc2.pdf. The first has both currents on a single closed quark loop alongside the nucleon correlator. The second is the product of that two-current vacuum loop and nucleon correlator that is subtracted. The surviving observable is their gauge-ensemble covariance, not the discarded vacuum expectation alone. This directly matches the missing same-loop contraction class of FSP-006. Source equation (11)'s following paragraph explicitly describes the vacuum subtraction.

For degenerate u,d,s propagators the electromagnetic sum is Tr Q^2=2/3, while Tr Q=0; same-loop two-current terms survive. This charge algebra does not certify the numerical flavor implementation. The source and its TeX do not provide flavor-separated loop data or an explicit light/strange coefficient inventory. The authors state that disconnected diagrams vanishing in the SU(3) limit were omitted. At physical unequal strange/light masses that is not a completeness proof. The Table II result is therefore the **source's reported same-loop disconnected moment**, not an authenticated complete physical u,d,s sea moment. The equality of the reported proton and neutron contribution also makes it invisible to p-n.

## Why the moment cannot determine a mass kernel

The disconnected covariance does not have a positive spectral measure: the paragraph after Wang equation (11) includes an explicitly negative vacuum-subtraction spectral term. Therefore a positive-measure inequality cannot be assumed. Even a zeroth-moment Ward constraint plus this second temporal moment is insufficient. A concrete signed-profile illustration, in dimensionless time tau, is

\[
h(\tau)=7e^{-|\tau|}-112e^{-2|\tau|}+243e^{-3|\tau|}-128e^{-4|\tau|}.
\]

It obeys integral h=0, integral tau^2 h=0, and sum c_k k=0 (which removes the leading inverse-Q^2 cosine-transform tail). Its cosine transform for z=Q^2 is

\[
F(z)=2\sum_{k=1}^4\frac{c_k k}{z+k^2}
=\frac{5040z^2}{(z+1)(z+4)(z+9)(z+16)}.
\]

Thus F(0)=F'(0)=0 but F(1)=252/85, and its convergent positive integral is 4992 log 2-2916 log 3, approximately 256.637291599. These rational identities and the displayed logarithm were checked in exploratory Python commands. They are not a preserved bounded-run computation; no manifest-backed run is claimed. This is a mathematical non-identifiability example for the stated moment constraints, not a proposed physical QCD tensor, not an evaluated proton contribution and not a proof of unbounded physical QCD mass shifts. Complete spatial/momentum dependence, contraction coverage and contact/UV matching impose further requirements. A finite temporal window moment supplies still less information.

For the proton mass insertion, a photon-kernel convolution needs all tensor components and spacetime separations together with the scalar/gluonic matching counterterms along a declared quark-mass/strong-coupling path. Neither the moment nor the raw imaginary-energy subtraction curve alone supplies that input.
