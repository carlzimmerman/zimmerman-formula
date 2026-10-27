# FSP-007 sea OPE result

The hard same-sea-loop gluon coefficient and a controlled ultraviolet response have been evaluated without a numerical alpha or target fit. This supplies a genuine UV contribution, while the physical finite-mass infrared sea response remains unevaluated.

For canonical \(G^2\), \(a=\alpha_s/(4\pi)\), and \(S_Q=\sum Q_f^2\), the leading scalar Wilson coefficient is \(c_{1g}=aS_Q/3\). For u,d,s, \(S_Q=2/3\), even though \(\sum Q_f=0\). The two spin-two gluon coefficients, including their MS mixing poles and logarithms, are in DERIVATION equations (2)–(6). They are nonzero in the subtraction function. Their contribution to the full traced Compton tensor cancels exactly after an O(d) photon angular integral, before the dimensional regulator is removed.

For the explicitly declared theory of exactly three massless quark flavors in SU(3) QCD, a finite photon band \(Q_0<|Q|<2Q_0\) with no local retuning has the controlled limit

\[
\lim_{Q_0/m\to\infty}\frac{1}{m}\frac{\partial M_{\rm band}}{\partial e^2}\bigg|_{e=0}
=-\frac{\log4}{216\pi^2}\simeq-0.0006502823404878044.
\]

This is a dimensionless full-tensor band insertion. At this leading asymptotic order its surviving contribution is the scalar gluon hard-loop term, fixed by the trace anomaly. The baryon mass supplies its own units; no measured mass or strong coupling was inserted. This fixed-flavor massless theory is not physical finite-mass QCD with heavy thresholds.

The same model's asymptotic subtraction coefficient is \(\lim Q^2W_1/(2m^2)=4/81+4/25=424/2025\). The spin-two \(4/25\) term is canceled by the other tensor contribution in the full mass functional. This explicit example prevents a subtraction-only UV log from being mistaken for the complete mass divergence.

The scalar full-mass shell slope at finite masses is

\[
B_0=\frac3{16\pi^2}\sum Q_f^2 f_f^{(0)}
-\frac{S_Q}{16\pi^2\beta_0}\left(1-\sum f_f^{(0)}\right)+O(\alpha_s).
\]

It requires sigma fractions. The leading gluonic divergence is canceled by the strong-coupling counterterm at fixed renormalized parameters, and the quark divergence by the mass counterterms. The canonical gluon factors are exactly \(+1/1024\) for the shell and \(-1/1024\) for its counterterm after factoring out \(g_s^2S_Q\langle G^2\rangle/(\pi^4m^2)\). Source \(\delta g\) is a counterterm symbol with mass contribution \(-\delta g\,\partial M/\partial g\), opposite to an actual coupling boundary increment. DERIVATION equations (11)–(13) specify this sign and the necessary rescaled-field conversion.

The executed finite checks passed for 112 symmetric traceless basis tensors across d=2,…,8, including all nine four-dimensional directions, with 1,428 direct axis/projector contractions. They also checked both spin-two mixing pole cancellations, the gluon-fed scale-log cancellation, mass/coupling scalar counterterm factors, and singlet fixed points for n_f=1,…,16. The small computation used exact fractions; only the displayed pi/log evaluation uses double precision.

The authoritative execution is run_003/manifest.json, status completed, with all input hashes unchanged before/after. The installed manifest validator reports “valid evidence record (run status: completed); mathematical interpretation requires review.” run_001/FAILURE.md preserves an initial pre-exec launch failure when macOS rejected the optional address-space limit. The successful run used a 30-second wall timeout and a 10-second CPU limit, standard Python 3.9.6 and no installed dependencies. No Git command was executed; the manifest explicitly records that its conservative dirty=true field is not a Git observation.

Reproduce from the project root using a fresh output directory:

```bash
python3 fine_structure_puzzle/qcd_sea_curvature/sea_ope/run_audit.py --output fine_structure_puzzle/qcd_sea_curvature/sea_ope/run_reproduction
```

Primary inputs are pinned in SOURCE_RECEIPTS.json: Hill–Paz arXiv:1611.09917v2, Hill–Solon arXiv:1409.8290v1 and corrected Gasser et al. arXiv:1506.06747v3. Visible PDF equations were used where extracted Hill–Paz text had overlapping obsolete sign layers. Temporary PDFs and extracted text are hashed; no shared source cache was changed.

The residual physical inputs are the nonperturbative individual-proton sea Compton covariance over low/intermediate Q, disconnected scalar matrix elements if a topology separation is required, finite local matching constants, the complete common mass/coupling path, and the independent curved response A_rho. The ordinary quark/gluon OPE operator split is not an invariant decomposition of the entire sea topology because singlet operators mix. No physical R(alpha), finite-alpha completion, or curved-space quantity was evaluated. A fresh independent review should check the full-tensor normalization and counterterm translation before using this as evidence in the phase synthesis.
