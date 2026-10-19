# FSP-Q: a QCD topological-vacuum bridge, tested rather than fitted

Parent: FSP-001. New lane under FSP-002-OPEN; Git `3c01aa2861bf576f4c2d942251eb9d2f89cae108`, dirty baseline. Source horizon: 2026-10-18. Only this lane's directory was written. Exact old-input hashes are in `INPUTS.json`; primary versions, PDF/text hashes and equation locators are in `SOURCES.json`.

**Result.** A physically motivated QCD-vacuum mechanism supplies a conditional connection between the acceleration scale and the QCD scale. It has not calculated the charge-normalized Maxwell coefficient or the electron Yukawa. Granting its cosmological term, a bounded exact calculation exhibits an alpha-varying family preserving vacuum acceleration and proton mass when the light-quark mass remains independent. An independent light-quark-mass input and calculated matching functions could remove this freedom; that is a concrete, potentially productive next discriminator. This is not a general exclusion of a QCD/vacuum origin for alpha.

## 1. What QCD actually generates

For canonically normalized **pure-QCD** fields and relativistically normalized proton states (with \(m_p\) initially denoting that theory's proton mass),

\[
T^\mu{}_{\mu}={\beta_s(g_s)\over2g_s}[G^a_{\mu\nu}G^{a\mu\nu}]_R
 +\sum_q(1+\gamma_{m_q})[m_q\bar q q]_R,
\qquad \langle p|T^\mu{}_{\mu}|p\rangle=2m_p^2.
\]

The trace identity and normalization follow from Metz–Pasquini–Rodini, [arXiv:2006.11171v2](https://arxiv.org/abs/2006.11171v2), equations (12) and (23). The paper also checks the scheme dependence of separate quark/gluon traces. A percentage assigned to a particular Hamiltonian term is therefore not an independent extra equation fixing the mass.

For the physical QCD+QED mass, the total trace also includes the electromagnetic anomaly \(\beta_e(e)[F_{\mu\nu}F^{\mu\nu}]_R/(2e)\) and consistently matched mass anomalous terms. The matching function below includes those effects; the displayed pure-QCD identity alone is not its complete trace decomposition.

The natural prediction has the form

\[
m_p=\Lambda\,C_p(\widehat m_u/\Lambda,\widehat m_d/\Lambda,
\widehat m_s/\Lambda,\ldots,\bar\theta,\alpha),
\]

where the hats denote an agreed renormalization-invariant mass convention and \(C_p\) is a nonperturbative matching function. The anomaly supplies scale breaking and the dynamics, but its RG integration constant still needs a boundary condition. Vacuum \(\langle0|T^\mu{}_{\mu}|0\rangle\) and connected one-proton matrix elements are different observables; equating them is an extra claim, not this Ward identity.

The primary ALPHA calculation, [Dalla Brida et al., Nature **652**, 328–334 (2026)](https://www.nature.com/articles/s41586-026-10339-4), Methods equations (5)–(9), writes the exact RG invariant \(\Lambda_x=\mu\varphi_x(g_x(\mu))\). Its beta coefficients give at one loop

\[
\alpha_s^{-1}(\mu)={b_{n_f}\over2\pi}\ln{\mu\over\Lambda_{n_f}},
\qquad b_{n_f}=11-\frac{2n_f}{3}.
\]

That work obtains \(\Lambda_{\overline{\rm MS}}^{(3)}=344.4(8.7)\,\mathrm{MeV}\), equation (3), after experimental hadronic inputs set its units. This measured calibration is not used as a prediction or fitting target here. The unspecified hadronic scale called approximately 100 MeV in the topological proposal is not automatically this particular scheme's Lambda parameter.

## 2. The actual physical bridge tried

The candidate is the response of QCD topological vacuum sectors to global geometry, distinct from ordinary propagation of a massive hadron. The current primary source is van Waerbeke–Zhitnitsky, [arXiv:2506.14182v4, 8 October 2026](https://arxiv.org/abs/2506.14182v4), sections II.C–D. Equations (4)–(7) posit

\[
\Delta\epsilon_{\rm vac}=c_H H\Lambda^3,
\qquad H^2={8\pi G\over3}\Delta\epsilon_{\rm vac},
\qquad \bar H={8\pi G\over3}c_H\Lambda^3.
\]

These equations use \(\hbar=c=1\). The paper explicitly identifies the extension from the hyperbolic calculation to de Sitter as an assumption: a first-principles de Sitter computation is unavailable, and its numerical coefficient is not supplied. Its footnote 6 absorbs a light-quark factor \(m_q/\Lambda\) into \(c_H\); its subsequent time-dependent extension adds another response function. Thus the de Sitter relation is the strongest clean conditional test, rather than an established QCD cosmological prediction.

The earlier [Urban–Zhitnitsky, arXiv:0909.2684v4](https://arxiv.org/abs/0909.2684v4), equation (1.1), gives a finite-manifold estimate

\[
\Delta\epsilon_{\rm vac}\simeq
{2N_f|m_q\langle\bar q q\rangle|\over m_{\eta'}L}.
\]

Its boundary scale \(L\sim H^{-1}\), condensate, eta-prime mass and geometry cannot be silently replaced by known pure integers. This formulation motivates the leading chiral dependence tested below.

To compare to the supplied framework relation, define its \(\rho_\Lambda\) as **mass density**, so \(\epsilon_\Lambda=\rho_\Lambda c^2\), and reserve \(k_\kappa\) for the framework's dimensionless coefficient to avoid confusing it with the source's hyperbolic curvature symbol. In the conditional asymptotic de Sitter state,

\[
a_0=k_\kappa c\sqrt{G\rho_\Lambda},\qquad
\rho_\Lambda={3\bar H^2\over8\pi G},\qquad
a_0=k_\kappa c\sqrt{3\over8\pi}\,\bar H.
\]

Writing \(m_\Lambda=\Lambda/c^2\) when Lambda is an energy, restoring SI units gives

\[
\boxed{\quad
m_\Lambda^3={\hbar^2 a_0\over
k_\kappa c_H\sqrt{8\pi/3}\,G c^2},\qquad
{a_0\hbar^2\over Gc^2m_p^3}
=k_\kappa\sqrt{8\pi/3}\,{c_H\over C_p^3}.
\quad}
\]

This is a derived **conditional matching equation**, with the unknowns visible. It is not a new derivation of the proton mass by writing a cube root of the dimensional acceleration combination. In particular, neither \(C_p=1\) nor \(c_H=1\) is licensed. It also concerns \(\bar H\), not an arbitrary epoch's \(H_0\); applying it today requires the vacuum evolution to have been solved. Neither this QCD proposal nor its coupling to the framework has been added to the frozen theory.

## 3. Exact bounded discriminator

The authorized new experiment is `discriminator_v2.py`, run through the computation-audit bounded runner as `run_002`. It contains two linked algebraic checks of the same question: do transmutation and hadron/vacuum matching erase the charge and mass integration constants?

First, in the QCD+QED product-gauge theory with six Dirac quarks, match the strong coupling successively at \(m_t,m_b,m_c\). Continuity at these matching masses holds at the order used; [Chetyrkin–Kniehl–Steinhauser, arXiv:hep-ph/9708255v2](https://arxiv.org/abs/hep-ph/9708255v2), introduction, explicitly distinguishes it from higher-order finite decoupling corrections. Exact algebra gives

\[
\ln\Lambda_3={7\over9}\ln\Lambda_6
 +{2\over27}(\ln m_c+\ln m_b+\ln m_t),
\]
\[
\ln\Lambda_3={7\over9}\ln M
 -{2\pi\over9}\alpha_s^{-1}(M)
 +{2\over27}\sum_{h=c,b,t}\ln m_h.
\]

Logs use one fixed reference unit. Both sequential substitution and the independent telescoping invariant \(b_3\ln\Lambda_3-b_6\ln\Lambda_6=(2/3)\sum_h\ln m_h\) agree, and the scale weights sum to one. Thresholds therefore transmit heavy-quark mass inputs; they do not create a charge boundary condition.

In the same stated one-loop product-gauge truncation,

\[
\alpha_0^{-1}=A+{2\over3\pi}\ln{M\over m_e}
+\sum_h{2N_cQ_h^2\over3\pi}\ln{M\over m_h}+\Delta,
\qquad A=\alpha^{-1}(M).
\]

Here \(Q_c=Q_t=2/3\), \(Q_b=-1/3\), \(N_c=3\); \(\Delta\) denotes other fixed matching terms. This is **not full Standard Model evolution above the electroweak scale** and is not a precision calculation of alpha(0). In particular, confined light quarks are not integrated down as free charged fermions; their low-energy vacuum polarization requires nonperturbative matching.

Grant known \(c_H,C_p\) and fixed light-quark ratios in the leading pure-QCD limit. For parameters

\[
(\alpha_s^{-1}(M),\ln m_c,\ln m_b,\ln m_t,A,\ln m_e),
\]

the derivative matrix of \((\ln\bar H,\ln m_p,\alpha_0^{-1},\ln m_e)\) is

\[
J=\begin{pmatrix}
-2\pi/3&2/9&2/9&2/9&0&0\\
-2\pi/9&2/27&2/27&2/27&0&0\\
0&-8/(9\pi)&-2/(9\pi)&-8/(9\pi)&1&-2/(3\pi)\\
0&0&0&0&0&1
\end{pmatrix}.
\]

The first two rows have exact rank one; the full matrix has rank three. Varying \(A\) changes alpha without changing \(\bar H,m_p\). Varying \(\ln m_e\) also leaves the vacuum/proton constraints unchanged. This conclusion is explicitly restricted to the leading limit: the next check restores electromagnetic sensitivity of both matching functions.

## 4. Electromagnetic proton mass does not get discarded

The proton contains electrically charged quarks, so its rest mass does depend on alpha. The leading correction is a renormalized electromagnetic self-energy proportional to alpha times a strong-interaction Compton amplitude, plus counterterms. This structure is displayed in [Walker-Loud–Carlson–Miller, arXiv:1203.0254v2](https://arxiv.org/abs/1203.0254v2), equations (2)–(3). Their quoted numerical electromagnetic **proton–neutron splitting** must not be substituted as the individual proton electromagnetic mass. The QCD/QED separation also requires a quark-mass renormalization convention.

To allow that dependence, Taylor-expand the candidate's leading chiral matching, using an effective light-quark mass \(q\) and **fixed but uncomputed** matching constants:

\[
\bar H=d\,q\Lambda^2(1+v\alpha),\qquad
m_p=(C_0+c_\gamma\alpha)\Lambda+c_q q.
\]

The coefficient \(d\) includes \((8\pi G/3)\) and the topological matching coefficient. These equations keep the light-quark factor in \(c_H\), the leading proton sigma-term dependence and electromagnetic terms in both functions. They are a declared leading approximation, not a fit to proton/dark-energy data; no numerical choice for any coefficient is made. Higher chiral terms, mass splittings and mixed QCD/QED corrections are outside this computation.

For \((\Lambda,q,\alpha)\), the \((\Lambda,q)\) minor of the Jacobian of \((\bar H,m_p)\) is

\[
\det J_{\Lambda q}=-d\Lambda^2(1+v\alpha)D,
\qquad D=C_0+c_\gamma\alpha-2c_q q/\Lambda.
\]

On the regular domain \(d,\Lambda,q>0\), \(1+v\alpha\ne0\), \(D\ne0\), the implicit-function theorem leaves a local alpha-varying curve preserving both outputs. Its tangent, normalized by \(\delta\alpha=1\), is

\[
\delta\Lambda=-{c_\gamma\Lambda-c_q qv/(1+v\alpha)\over D},
\qquad
\delta q=-q\left({2\delta\Lambda\over\Lambda}
 +{v\over1+v\alpha}\right).
\]

The script verifies this tangent by exact Jacobian multiplication and independently by eliminating \(q=\bar H/[d\Lambda^2(1+v\alpha)]\). Thus even including the proton's electromagnetic response does not select alpha while a light-quark-mass boundary remains free. The criterion \(D\ne0\) is stated rather than presumed a theorem of real QCD. It holds throughout the ordinary chiral neighborhood of a nonzero \(C_0\), away from exceptional cancellation. Other strange/light-quark parameters, if freed, add possible directions rather than supply missing equations.

**Positive control.** If \(q\) is independently fixed and the constants really have been calculated, the remaining \((\Lambda,\alpha)\) Jacobian has determinant

\[
dq\Lambda^2[2c_\gamma-C_0v+c_\gamma v\alpha],
\]

which is generically nonzero. Such a model can in principle infer alpha from vacuum acceleration and proton mass. If \(c_\gamma=v=0\), that selector disappears. This control prevents promoting a leading pure-QCD null direction into an all-orders no-go theorem.

## 5. The electron and macroscopic baryons remain distinct

The Standard Model operator \(-y_e\bar L H e_R+\mathrm{h.c.}\), after a specified Higgs vacuum, gives \(m_e=y_e v_{\rm EW}/\sqrt2\) before the stated radiative matching. A QCD vacuum coefficient supplies no equation for that Yukawa. Consequently \(m_p/m_e\), atomic reduced masses, and the ratio of an atomic orbital scale to a strong-interaction radius remain additional targets. The electron mass cannot be inferred from a successful QCD proton-mass calculation alone.

Likewise a galaxy's baryonic mass is a sum over numbers of nuclei, electrons and other components, including nuclear binding and thermal contributions. A proton rest-mass mechanism does not generate the baryon asymmetry, the number of stars/gas particles, a stellar initial-mass function or a mass-to-light calibration. Helium/metal fractions and isotope-dependent binding energies are independent composition data. The strong and electromagnetic matching thresholds of the microscopic calculation are not a substitute for those astronomical inputs.

## 6. Interpretation, provenance and next discriminator

The current run `run_002/manifest.json` has `run.status=completed`; all **16** exact algebraic checks passed. Manifest validation with the installed v2 validator and `--root` returned a valid evidence record. Python 3.9.6, SymPy 1.14.0; no random sampling, no fitted coefficients, no numerical alpha target. Caps: 30 seconds wall time, 20 seconds CPU, 1 MiB logs and conventional one-thread limits. The implementation checks the sequential/telescoping threshold invariant, scaling dimension, exact rank/null vectors, the explicit electron threshold response, a second elimination of the chiral tangent, and the known-quark-mass positive control. A successful execution verifies these finite symbolic assertions in their declared model, not the physical existence of the cosmological term. The parent independently checked the SI matching, chiral minor/tangent and positive-control determinant and found agreement under the stated assumptions; current electron-threshold bookkeeping is sent for review.

The initial `discriminator.py`, `contract.json` and `run_001` are preserved. Its 15 exact checks passed for a partial QED formula with a fixed remainder; self-review identified that displaying a variable electron mass also requires its threshold response. The current version adds that term and its check. Both runs preserve the same vacuum/proton null directions and rank results. This was a bookkeeping limitation of the initial model, not a failed cosmological mechanism or a failed execution.

The old Koide/QCD-running script concerns common-scale running quark masses, rather than vacuum response; ZD02 concerns enclosed galactic mass accounting, rather than nucleon mass generation. The preceding alpha UV/gauge work already records independent gauge coefficients and thresholds. This lane adds the explicit QCD topological-vacuum candidate, its source-current assumption check, and an electromagnetic-sensitive hadron/vacuum matching discriminator. No formula grammar search or recycled numerical power match was run.

The **first unresolved physical implication** is the extension to physical four-dimensional QCD in de Sitter, with a regulator, vacuum subtraction and light-quark masses specified, yielding a definite \(c_H\). The next selector test is to compute, in one consistent scheme,

\[
R_{\rm QCD}(\alpha,\widehat m_q/\Lambda,\bar\theta)
={c_H\over C_p^3},\qquad
S_\gamma={\partial\ln R_{\rm QCD}\over\partial\ln\alpha},
\]

and determine whether the framework or an independent microscopic principle fixes the quark-mass ratios. With those inputs held independently, the boxed dimensionless matching equation is a genuine held-out alpha test. It needs an isolated root and a nonzero, sufficiently well-determined \(S_\gamma\); otherwise the inferred uncertainty is amplified as \(\delta\ln\alpha\simeq\delta\ln R/S_\gamma\). Fitting \(c_H\) to the observed dark-energy density would consume the proposed test. The electron Yukawa still needs its own mechanism.

`SOURCES.json` separates source authentication, equation extraction and conditional project application. Public PDFs were fetched into temporary storage and hashed; full papers were not copied into tracked artifacts. The first unprivileged retrieval failed from DNS restrictions, and the permitted network retrieval succeeded; this was an acquisition failure, not failed physics. No run failed. Search coverage is bounded to this mechanism and its QCD/mass prerequisites; no general novelty claim is made.
