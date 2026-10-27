# QED_M primary-source verification (bounded, blind review)

Checked 2026-10-19. Task: authenticate the small photon-mass response of charged-hadron masses and the limiting prescription. No candidate coefficient or projector was supplied. No author-lane files, other new notes/reviews, Git state, source cache, or author contacts were accessed. Only this note is written.

## S1: infinite-volume mass response

Michael G. Endres, Andrea Shindler, Brian C. Tiburzi, André Walker-Loud, *Massive Photons: An Infrared Regularization Scheme for Lattice QCD+QED*, Phys. Rev. Lett. **117**, 072002 (2016), [DOI](https://doi.org/10.1103/PhysRevLett.117.072002), [arXiv:1507.08916v3](https://arxiv.org/pdf/1507.08916v3), 11 Aug 2016. Metadata and v3 PDF text authenticated.

Page 2, Eq. (3), at leading order in alpha, defines

\[
\Delta_\gamma M=M(\alpha,m_\gamma)-M(\alpha,0),\qquad
\Delta_\gamma M^{\rm LO}=-\frac{\alpha Q^2}{2}m_\gamma,
\]
\[
\Delta_\gamma M^{\rm NLO}=\left(Ce^2-\frac{\alpha Q^2}{4\pi}\right)\frac{m_\gamma^2}{M},\qquad
\Delta_\gamma M^{\rm N^2LO}=O(m_\gamma^3/M^2).
\]

Here alpha=e^2/(4 pi), Q is charge in units of e (proton Q=1), and M is the hadron mass. The source calls the quadratic term analytic; C is an unfixed local coefficient. Neither a quadratic logarithm nor explicit cubic magnetic/radius coefficients are printed. The latter two orders are not determined by charge alone. The EFT uses Landau gauge and includes additional operators unconstrained by gauge invariance. Footnote [39] requires dynamical pions when m_gamma reaches roughly 2 m_pi; [42] identifies a local NLO operator. Verdict: **verified** for these displayed terms; **unverified** for any more detailed cubic formula or quadratic-log assertion.

## S2: zero mode and controlled single-volume use

Same authors, *Photon mass term as an IR regularization for QCD+QED on the lattice*, PoS(LATTICE2015)078, [arXiv:1512.08983v1](https://arxiv.org/pdf/1512.08983v1), 30 Dec 2015, [publisher PDF](https://pos.sissa.it/251/078/pdf). Version and full PDF text authenticated.

Page 3, Eq. (2), for 0<tau<<T:

\[
C(\tau)\propto e^{-M\tau-x\tau^2},\qquad x=\frac{2\pi\alpha Q^2}{m_\gamma^2L^3T}.
\]

Thermal winding terms are exponentially suppressed in this argument. Page 4, Eqs. (4)-(5), give

\[
\delta_LM^{\rm LO}=2\pi\alpha Q^2m_\gamma[I_1(z)-z^{-3}],\quad
\delta_LM^{\rm NLO}=\frac{\pi\alpha Q^2m_\gamma^2}{M}[2I_{1/2}(z)+I_{3/2}(z)],\quad z=m_\gamma L,
\]
\[
I_n(z)=\frac{1}{2^{n+1/2}\pi^{3/2}\Gamma(n)}\sum_{\nu\in\mathbb Z^3\setminus\{0\}}\frac{K_{3/2-n}(z|\nu|)}{(z|\nu|)^{3/2-n}}.
\]

The subtraction implements the separately treated temporal zero mode. Figure 2's caption permits an extrapolation at fixed ML only while omitted finite-volume effects remain below mass-splitting errors; this is not an unrestricted interchange of limits. S1 Eq. (2) additionally states x vanishes as T tends to infinity at fixed L and m_gamma.

## S3: limit order and convention cross-check

M. A. Clark, M. Della Morte, Z. Hall, B. Hörz, A. Nicholson, A. Shindler, J. T. Tsang, A. Walker-Loud, H. Yan, *QED with massive photons for precision physics: zero modes and first result for the hadron spectrum*, PoS(LATTICE2021)281 (2022), [DOI](https://doi.org/10.22323/1.396.0281), [arXiv:2201.03251v1](https://arxiv.org/html/2201.03251v1), 10 Jan 2022. Exact-version HTML and PDF metadata authenticated.

Section 2 requires L to infinity at fixed m_gamma, then m_gamma to zero. Section 3 assumes T>>L for its finite-volume formulas. Section 3.1, Eqs. (17)-(27), separately treats temporal and spatial zero modes; the latter yield additional finite-size effects, so subtracting the tau^2 term is not a complete zero-mode analysis. The displayed saddle-point result is approximate in 1/V and simplifies to scalar propagation. Section 5.3, Eqs. (34)-(36), repeats the linear/quadratic expansion but writes the local term C alpha. Thus its C equals 4 pi times S1's C when the formulas describe the same convention. Its mass extrapolation also stops before explicit cubic coefficients. Verdict: **verified** limit prescription and normalization translation; detailed proton cubic coefficient **unverified**.

## S4: hierarchy caveat (adjacent primary analysis)

Z. Davoudi, J. Harrison, A. Jüttner, A. Portelli, M. J. Savage, *Theoretical aspects of quantum electrodynamics in a finite volume with periodic boundary conditions*, Phys. Rev. D **99**, 034510 (2019), [published PDF](https://scoap3-prod-backend.s3.cern.ch/media/files/45937/10.1103/PhysRevD.99.034510.pdf), [DOI](https://doi.org/10.1103/PhysRevD.99.034510), published 28 Feb 2019. Publisher-version metadata and PDF text authenticated.

Page 5, discussion preceding Section III: QED_M suppresses volume effects exponentially for suitable m_gamma L; controlled EFT separation additionally requires m_gamma/m_H<<1, where m_H is the lightest hadron mass. This primary paper's main calculations concern QED_L, not an explicit infinite-volume QED_M cubic response. It cannot by itself authenticate that coefficient.

## Scope, application, and retention

This was source authentication plus equation extraction and notation translation, not a candidate-proof audit or a derivation of omitted terms. The known mass response is **known after translation of notation**. A newly proposed linear/differential projector applied to that known response would, on this evidence, be a method translation (or a formal corollary if the algebra is exact), not evidence for a new physical coefficient. Its usefulness or genuinely additional subtraction content requires a separate check. No supplied projector was available to check.

Searches used the web index plus arXiv and publisher/author-institution primary versions, with exact QED_M titles and combinations of massive photon / photon mass / hadron mass shift / proton / NRQED / quadratic / logarithm / cubic / magnetic moment / charge radius. S1's bibliography and S3's backward citation to S1 were checked; searches found later citations and adjacent finite-volume literature. A same-searcher second pass used magnetic/radius and explicit cubic terminology. No separate specialist or exhaustive forward-citation database audit occurred. Explicit infinite-volume magnetic/radius cubic coefficients were not found in the checked QED_M primary sources; this is a bounded nonverification, not an absence theorem or novelty claim.

Full source bytes were not retained, respecting the no-cache instruction; source SHA-256 values are unavailable. Browser PDF screenshots failed, so equation extraction used primary PDF text and exact-version HTML cross-checks. No .mathbox evidence or project claim status was recorded. A sibling SHA256SUMS file hashes this note only.
