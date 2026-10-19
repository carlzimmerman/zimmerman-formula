# A mixed electromagnetic chiral mass-shape test

**Viable, with a restricted domain.** The vacuum susceptibility and individual proton electromagnetic response obey a common leading infrared mass-shape relation:
\[
\boxed{\quad
\mathcal U(M)={2D_p(M)\over3\pi g_0^2D_\chi(M)}
=1\quad\hbox{at the retained chiral orders},\qquad
\lim_{M\to0^+}\mathcal U(M)=1
\quad}
\]
within the standard, termwise differentiable two-flavour chiral expansion and the conventions below. The unknown pion electromagnetic matching constant \(Z_0\), the pion decay constant and the leading local electromagnetic mass constants disappear. This is an unfitted cross-sector infrared prediction. It is not an exact finite-mass identity, a nonperturbative QCD theorem, a fixed-proton cosmological derivative, a calculation of \(c_H\), or an alpha selector.

The new curvature filters in section 5 additionally remove the next analytic mass counterterms. Their leading normalized ratio is also one, with smaller generic next-order mass dependence. None of the frozen electromagnetic report, sources or run inputs has been changed.

## 1. Family of theories and observables

Work in infinite flat volume, zero temperature and theta zero, with ordinary two-flavour QCD+QED and no external electromagnetic background. Fix the strong reference theory, strange-quark mass and positive light-quark mass ratio \(z=m_u/m_d\in(0,\infty)\). Vary their common positive light-quark mass. A concrete prescription uses full QCD+QED \(\overline{\rm MS}\) masses at a fixed ultraviolet scale \(\mu_q\), with their renormalized values kept independent of \(e^2\) during the charge derivative. Other conventions require the chain rules in section 6.

The canonical mass coordinate is the reference \(e=0\) pion mass parameter
\[
M^2=B_0(m_u+m_d),\qquad
w={z\over(1+z)^2},\qquad
\chi_0(M)=F_0^2M^2w.
\]
\(F_0,B_0,Z_0,g_0\) are the light-quark chiral-limit SU(2) matching constants at the fixed strange mass; \(g_0\) is the nucleon axial charge. They are constants of this EFT. A light-mass-dependent measured \(g_A(M,0)\) is a different object and must be differentiated when it occurs inside a mass-dependent amplitude.

Define charge coefficients with \(e^2=4\pi\alpha\), taking the derivative at each \(M>0\):
\[
V(M)=\left.\partial_{e^2}{\chi(M,e^2)\over\chi_0(M)}\right|_{e^2=0},
\qquad
B_p(M)=\left.\partial_{e^2}m_p(M,e^2)\right|_{e^2=0},
\]
\[
D_\chi(M)=\partial_{\ln M^2}V(M)
={M\over2}\partial_M V(M),\qquad
D_p(M)=\partial_M B_p(M).
\]
The derivative of the individual proton mass is needed. A proton–neutron splitting cancels the leading pion-cloud term used here.

Regulate the charged proton rest threshold, take the controlled infinite-volume/zero-photon-regulator limit at positive \(M\), then differentiate the resulting mass dependence and take \(M\to0^+\). The chiral limit is outside the finite-volume epsilon regime. Other hadrons integrated out of SU(2), including the Delta and eta-prime, must retain nonzero chiral-limit gaps. A simultaneous degenerate-Delta or large-\(N_c\) limit need not have the same low-energy formula. Require \(Z_0g_0\ne0\); otherwise the normalized relation is undefined.

## 2. Derive the relation from the two pion kernels

The authenticated fixed-quark-mass susceptibility calculation of [Gorghetto–Villadoro, arXiv:1812.01008v2, equations (34)–(36)](https://arxiv.org/abs/1812.01008v2) and the baryon calculation of [Müller–Meißner, arXiv:hep-ph/9903375v1, equation (3.4)](https://arxiv.org/abs/hep-ph/9903375v1) imply
\[
V(M)=K_\chi^r(z,\bar\mu)
-{Z_0\over8\pi^2}\left[1+\log{M^2\over\bar\mu^2}\right]
+O(M^2\log^k M^2),
\]
\[
B_p(M)=L_p-{3g_0^2Z_0\over16\pi}M
+O(M^2\log M^2).
\]
The order symbols specify chiral powers, with dimensions supplied by fixed hadronic scales. At the next meson order \(k\le2\) is sufficient for the local/two-loop mass powers checked here. The source's complete leading meson combination is
\[
K_\chi^r={20\over9}(k_5^r+k_6^r)
+{4\over9}(1+3\Delta)k_7^r,\qquad
\Delta={1-z\over1+z}.
\]
\(L_p\) is the leading local one-baryon electromagnetic mass coefficient. In the invariant-operator convention of the frozen report,
\(L_p=-F_0^2(f_1+f_3+f_2)/2\). Its value and even its convention do not enter the shape test.

For clarity, these expressions can be independently recovered before the small-charge expansion. Set \(\delta_\pi=2e^2F_0^2Z_0\). The charged Goldstone determinant and the heavy-baryon pion self-energy supply
\[
\delta(\chi/\chi_0)_{\rm loop}
=-{(M^2+\delta_\pi)\log[(M^2+\delta_\pi)/\bar\mu^2]
-M^2\log(M^2/\bar\mu^2)\over16\pi^2F_0^2},
\]
\[
\delta m_{p,\rm loop}
=-{g_0^2\over16\pi F_0^2}
\big[(M^2+\delta_\pi)^{3/2}-M^3\big].
\]
Differentiate in \(e^2\) at zero first and then in the stated mass coordinates:
\[
D_\chi=-{Z_0\over8\pi^2},\qquad
D_p=-{3g_0^2Z_0\over16\pi},\qquad
{D_p\over D_\chi}={3\pi\over2}g_0^2.
\]
Both signs agree for positive \(Z_0\). The shared \(Z_0\) cancels in the ratio. \(F_0^2\) already cancels between the pion mass shift and the loop denominators. The normalized axial charge is independently measurable in pure QCD; no numerical alpha or matching constant is assigned.

## 3. Same-order operators and the first contamination

At meson order \(e^2p^2\), a zero-momentum vacuum operator contains one light-mass spurion. Dividing its susceptibility by \(\chi_0\propto M^2\) leaves a constant along fixed \(z\); the full source expression lists precisely \(K_\chi^r\). Derivative operators vanish on the uniform vacuum. A local \(e^2\log M^2\) term would be nonanalytic in the quark masses and is not an independently adjustable operator in standard chiral matching.

At baryon order \(e^2\), all local electromagnetic mass operators give constants in \(B_p\). At the next odd order \(e^2p\), the source's on-shell mass calculation explicitly finds only the pion-splitting loop. Its local third-order derivative terms multiply the residual nucleon energy or pion fields and do not supply an on-shell, zero-pion mass. A local \(e^2M\) operator would be nonanalytic in the light quark masses and is absent. This is why the coefficient of the linear \(M\) term is protected at this order.

Higher orders are different. Baryon \(e^2M^2\) local terms and \(e^2M^2\log M^2\) loops give \(D_p\) corrections of order \(M\) and \(M\log M^2\). Some logarithmic coefficients contain unknown lower-order baryon constants. Meson \(e^2M^2\log^k M^2\) terms in the fractional susceptibility give \(D_\chi\) corrections of order \(M^2\log^k M^2\). Consequently the ordinary ratio has generic leading contamination of order
\[
\mathcal U(M)-1
=O\!\left({M\over\Lambda_\chi}\log{M\over\bar\mu}\right)
+O\!\left({M^2\over\Lambda_\chi^2}\log^2{M\over\bar\mu}\right).
\]
This estimates powers within the EFT, not a numerical error bar or a rigorous uniform all-order remainder bound for QCD.

The LECs \(F_0,Z_0,g_0\) are constant at this order. If amplitudes are instead expressed using \(F_\pi(M)\), the effective pion splitting, and \(g_A(M)\), their usual corrections start at \(M^2\log M^2\) or analytic \(M^2\). Applying the mass derivatives to those quantities produces only subleading terms; omitting their derivatives would be inconsistent. Normalizing the final test with the independently computed \(g_A(M,0)^2\) preserves the limiting value one.

## 4. The two infrared limits cannot be exchanged

The unexpanded one-loop kernels give, at fixed positive \(e^2\),
\[
D_\chi(M,e^2)=-{Z_0\over8\pi^2}
 {M^2\over M^2+\delta_\pi},\qquad
D_p(M,e^2)=-{3g_0^2Z_0\over16\pi}
 {M\over\sqrt{M^2+\delta_\pi}},
\]
\[
{2D_p(M,e^2)\over3\pi g_0^2D_\chi(M,e^2)}
=\sqrt{1+{\delta_\pi\over M^2}}.
\]
At fixed positive charge both shapes tend to zero and their ratio diverges. At zero charge first the normalized ratio is one. The finite-charge expression only diagnoses nonuniformity of these one-loop terms; it is not a complete fixed-charge chiral theory. The promised test is the sequential zero-charge response, mass shape, and chiral limit.

## 5. Curvature filters remove the next analytic counterterms

Let \(\mathcal L=(M/2)\partial_M=\partial_{\ln M^2}\). Define
\[
\widetilde D_\chi=\mathcal L(1-\mathcal L)V,\qquad
\widetilde D_p=(\partial_M-M\partial_M^2)B_p,
\]
where \(\partial_M^2\) is the second derivative. These are differential projections on actual local EFT mass powers. They do not assign or fit any coefficients.

For \(s=M^2\), their actions are
\[
\mathcal L(1-\mathcal L)s^n=n(1-n)s^n,\qquad
(\partial_M-M\partial_M^2)M^p=p(2-p)M^{p-1}.
\]
They kill constants and the next analytic \(M^2\) terms while retaining the leading \(-A\log M^2\) and \(-dM\) shapes:
\[
\widetilde D_\chi=-{Z_0\over8\pi^2},\qquad
\widetilde D_p=-{3g_0^2Z_0\over16\pi},\qquad
\widetilde{\mathcal U}
={2\widetilde D_p\over3\pi g_0^2\widetilde D_\chi}=1
\]
at the retained leading orders. Their effect on the first logarithmic corrections is
\[
\mathcal L(1-\mathcal L)[cM^2\log(M^2/\bar\mu^2)]=-cM^2,
\]
\[
\mathcal L(1-\mathcal L)[cM^2\log^2(M^2/\bar\mu^2)]
=-2cM^2[\log(M^2/\bar\mu^2)+1],
\]
\[
(\partial_M-M\partial_M^2)[bM^2\log(M^2/\bar\mu^2)]=-4bM.
\]
Thus standard next-order baryon single logs leave generic \(O(M/\Lambda_\chi)\) contamination rather than \(O(M\log M)\), while meson double logs reduce to \(O(M^2\log M)\). Unknown constants multiplying loop logarithms remain; these filters improve the test without determining its subleading correction. They require a termwise differentiable chiral expansion and can amplify statistical errors when estimated from lattice data.

## 6. Renormalization and mass conventions

Keep both the ultraviolet quark-mass scale \(\mu_q\) and the chiral subtraction scale \(\bar\mu\) fixed during the primitive mass derivatives. Writing \(A=Z_0/(8\pi^2)\), scale invariance of
\(V=K_\chi^r(\bar\mu)-A[1+\log(M^2/\bar\mu^2)]\)
requires
\[
{dK_\chi^r\over d\log\bar\mu}=-2A.
\]
Choosing \(\bar\mu=M\) moves the logarithm into \(K_\chi^r(M)\); differentiating its running gives the same \(-A\) shape. It does not remove the prediction or create an independent adjustable infrared logarithm. Likewise the barred baryon constants in the source's equation (3.9) explicitly contain \(\log M_{\pi^0}\); they must not be held fixed in a mass scan at the expense of fixed-scale renormalized constants.

For \(t=e^2\) and a finite mass change \(m_i'=m_i[1+t a_i+O(t^2)]\), a fixed-primed-mass derivative obeys
\[
\left.\partial_t O\right|_{m'}
=\left.\partial_t O\right|_m
-\sum_i a_i m_i\partial_{m_i}O_{\rm QCD}.
\]
For constant \(a_i\), the leading vacuum change is
\[
V'(M)-V(M)
=-{a_um_d+a_dm_u\over m_u+m_d}
+O(M^2\log M^2).
\]
It is constant along fixed \(z\), so its leading mass shape vanishes. The proton change starts at \(M^2\), since its pure-QCD mass is a chiral-limit constant plus analytic \(M^2\) and nonanalytic \(M^3\) terms. Its \(M\)-derivative vanishes in the chiral limit. Fixed-scale ultraviolet running and regular invariant-mass conversions have this protected form. A regular alpha-dependent strong-scale conversion similarly adds pure-QCD mass-shape terms whose leading constants are projected out.

The qualification is essential. A finite-at-each-positive-mass choice \(a_u=a_d=a_{\rm IR}\log(M^2/\bar\mu^2)\) shifts \(D_\chi\) by \(-a_{\rm IR}\). Its induced proton term still has a vanishing leading shape as \(M\to0\). The naive normalized limit therefore changes. Such a prescription changes the charge-switching path in an infrared-dependent way; it is not chirally regular. For the basic limiting relation, sufficient restrictions are bounded chiral limits of the conversion coefficients and vanishing \(\partial_{\ln M^2}a_i\). Standard chiral analytic conventions provide the stated correction powers. A general mass-dependent description of the same physical path must retain all compensating chain-rule terms.

Normalization and coordinates also matter. Replacing \(\chi_0\) by the full separately computed pure-QCD susceptibility \(\chi(M,0)\) preserves the asymptotic limit because their ratio tends to one. An arbitrary constant rescaling of the reference denominator does not. A charge-dependent charged-pion mass used in the denominator or as the mass coordinate can introduce extra \(e^2/M^2\) terms and does not define this test. The canonically normalized \(e=0\) pion pole mass is allowed, since
\(M_{\pi,0}=M[1+O(M^2\log M^2)]\); its coordinate Jacobians tend to one.

## 7. A concrete unfitted lattice observable

Generate a family of pure-QCD ensembles at common light mass \(m_i=\lambda r_i\), fixed positive \(r_u/r_d\), fixed strange mass and strong reference scale, at sufficiently large volume. For each positive \(\lambda\), measure:

1. The pure-QCD pion pole mass \(M_{\pi,0}\), topological susceptibility \(\chi(\lambda,0)\), and renormalized nucleon axial charge \(g_A(\lambda,0)\).
2. The zero-charge current-current response \(\chi_e(\lambda)=\partial_{e^2}\chi|_0\), with matching counterterms for the specified fixed masses and strong input.
3. The **individual proton** response \(m_{p,e}(\lambda)=\partial_{e^2}m_p|_0\), extracted from its matched two-point function, including disconnected/sea terms.

No simulation value of the target alpha is needed for these derivatives. The current-current insertion formalism is authenticated in [de Divitiis et al., arXiv:1303.4896v1, section 2](https://arxiv.org/abs/1303.4896v1). The continuum/infinite-volume response must be matched before the chiral limit. Shared ensembles and mass retunings imply correlated errors.

The direct observable test, without LO susceptibility normalization, is
\[
V_{\rm obs}(M_{\pi,0})={\chi_e\over\chi(\lambda,0)}
=\left.\partial_{e^2}\log\chi\right|_0,\qquad
B_{\rm obs}(M_{\pi,0})=m_{p,e},
\]
\[
\mathcal U_{\rm obs}
={2\,\partial_{M_{\pi,0}}B_{\rm obs}\over
3\pi g_A(\lambda,0)^2\,
\partial_{\ln M_{\pi,0}^2}V_{\rm obs}}
\ \longrightarrow\ 1.
\]
The filtered version replaces the derivatives by the section 5 projectors in the same \(e=0\) pole-mass coordinate. The ordinary relation is the minimal test; the filtered version also tests whether the anticipated next-order analytic mass dependence has been removed. Neither requires fitting a vacuum or proton electromagnetic constant.

Common-mass Feynman–Hellmann insertions can obtain the mixed mass derivatives directly. With \(S_\lambda=\partial_\lambda S_{\rm QCD}=\int\sum_i r_i\bar q_iq_i\), the matched photon insertion \(\mathcal I\), and total topological charge \(\mathcal Q\),
\[
\chi_e=-{1\over V}\langle\mathcal Q^2;\mathcal I\rangle,\qquad
\partial_\lambda\chi_e=
{1\over V}\langle\mathcal Q^2;\mathcal I;S_\lambda\rangle
-{1\over V}\langle\mathcal Q^2;\partial_\lambda\mathcal I\rangle.
\]
These are connected cumulants, with all mass-dependent counterterms differentiated. Normalization derivatives must also be retained in
\(\partial_\lambda(\chi_e/\chi)\). The proton mixed derivative follows by differentiating its two-point insertion before extracting the asymptotic rest energy, with overlap and vacuum terms included. At LO,
\(\partial_{\ln M^2}=\lambda\partial_\lambda\) and
\(\partial_M=(2\lambda/M)\partial_\lambda\); measured \(M_{\pi,0}(\lambda)\) supplies the exact practical Jacobian.

## 8. Evidence and independent review

The current run is mixed_chiral/run_001. It completed **38 exact symbolic checks**, and the installed manifest validator accepts the record against the current inputs. Python 3.9.6 and SymPy 1.14.0 were observed. No numerical alpha, random sampling, fitted LEC or experimental mass enters. Caps were 30 seconds wall time, 20 seconds CPU, 1 MiB logs and conventional one-thread limits.

The script derives both shapes from the actual unexpanded pion kernels, then checks the normalized relation, cancellation of local constants and \(F_0,Z_0\), RG running, mass-convention shifts and a counterexample for an infrared-dependent convention, the two curvature projections, the listed next-order logarithmic limits, and canonical pion-coordinate Jacobians. These are finite symbolic assertions about the stated chiral expansion; they do not prove uniform control of every term of physical QCD.

The command and hashes are in run_001/manifest.json; the executable is mixed_response.py and its contract is contract.json. For regeneration, choose a fresh runner output directory and use the recorded argv with its output path changed accordingly. Validation:

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_prediction/electromagnetic/mixed_chiral/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula

The independent derivation was saved before reading the coordinator's raw mixed-chiral derivation. A read-only child auditor separately checked the same-order operators, scale running, mass-convention chain rule, order of limits, and the improved filters; its verdict and restrictions are saved in REVIEW.md. There is no claim that the relation is new in the literature.

The next concrete physical result would be a continuum, infinite-volume measurement of \(\mathcal U_{\rm obs}(M_{\pi,0})\) or its filtered version, approaching the stated chiral regime with matched charge and mass insertions. The leading limit is predicted; the approach requires higher-order EFT information or data with correlated uncertainties. This test supplies no geometric vacuum matching and consumes no alpha target.
