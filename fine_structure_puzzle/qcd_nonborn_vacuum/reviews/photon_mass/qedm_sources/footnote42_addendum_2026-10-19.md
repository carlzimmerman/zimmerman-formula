# Endres v3 footnote [42]: bounded source addendum

Checked 2026-10-19. This addendum authenticates source content only; it does not derive an EFT basis or a tadpole coefficient.

**Successful primary routes:** `web__run.open` on the [unversioned arXiv PDF](https://arxiv.org/pdf/1507.08916) returns a six-page PDF whose footer reads arXiv:1507.08916v3, 11 Aug 2016. The [Jefferson Lab author-institution PDF](https://misportal.jlab.org/sti/publications/13965/attachments/8449/massive_qed2.pdf) independently returns the same equations and footnote. Explicit `...1507.08916v3` PDF requests failed with cache miss, so use the successful unversioned route and verify its footer. Bibliography: Endres, Shindler, Tiburzi, Walker-Loud, Phys. Rev. Lett. 117, 072002 (2016), [DOI](https://doi.org/10.1103/PhysRevLett.117.072002).

**Exact locator:** PDF page 6, footnote/reference [42]; arXiv browser text lines 598–604, JLab browser text lines 596–602. The footnote identifies the NLO local monomial as phi* phi psi-dagger psi, with a Higgsing scalar VEV. It then displays

\[
m_\gamma^2 A_\mu A_\mu\,\psi^\dagger\psi
\]

and says it “contributes to masses at N3LO”, while identifying its lack of gauge invariance. This is a six-word quotation; the displayed mathematical monomial is transcribed exactly.

**Adjacent convention:** PDF page 2, Eq. (1), uses canonical photon normalization, with coefficient 1/4 multiplying F-squared. The following analytic-considerations paragraph works at leading alpha=e^2/(4 pi), with expansion parameter m_gamma/M, and permits additional operators unconstrained by gauge invariance. Eq. (3) prints C e^2 for the different NLO local mass coefficient. The N3LO monomial in [42] has no printed Wilson coefficient, explicit e power, sign, denominator, symmetry factor, or matching equation. C in Eq. (3) must not be silently identified with its coefficient.

**Verdicts:** Existence of this monomial in the source and its stated N3LO mass counting: **verified**. Its explicit coefficient/e-power convention: **unverified**, because absent. A tadpole yielding an order-e^2 m_gamma^4 log(m_gamma^2) contribution: **not calculated or explicitly asserted in this source**. No inference about its sign or numeric coefficient is authenticated here.

**Application boundary:** The source describes massive-photon EFT mass curves. The checked passages do not construct a fixed pure-QCD two-current tensor contracted with a varying massive propagator. Nor do they determine whether the displayed monomial is independent, redundant by equations of motion, fixed by matching to that tensor, or combined with other local terms in a chosen basis. Therefore [42] alone supports neither an extra unknown contaminating coefficient for that fixed-tensor observable nor its exclusion. That application remains **conditional on a separate matching/basis argument**. This does not alter the earlier verified linear/quadratic response.

No full primary bytes retained; the note hash is in SHA256SUMS. No author-lane, other review notes, source cache, or Git state accessed.
