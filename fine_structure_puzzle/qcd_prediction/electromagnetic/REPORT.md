# QCD-E: explicit electromagnetic chiral terms and the missing geometric response

Owner QCD-E, parent FSP-003/FSP-002. This lane calculates actual terms of the pion vacuum determinant and nucleon self-energy. No alpha target, observed vacuum density, assigned matching coefficient, fitted proton electromagnetic mass, or numerical LEC estimate enters the computation.

**Result.** The universal two-flavour electromagnetic pion loop is

\[
\left({\delta\chi_{\rm top}\over\chi_0}\right)_{\pi^\pm{\rm loop}}
=-{e^2 Z\over8\pi^2}
 \left[1+\log {M^2\over\bar\mu^2}\right],
\qquad
\delta m_{p,\pi^\pm}^{\rm EM}
=-{3e^2g_A^2 ZM\over16\pi}+O(e^4).
\]

Here \(M^2=B(m_u+m_d)\) and the leading charged-pion mass shift is \(2e^2F^2Z\). The first term also gives the fractional pion-loop correction to the source's \(m_q\Sigma\) numerator for two degenerate quarks, with \(\Sigma=-(\langle\bar uu\rangle+\langle\bar dd\rangle)/2\) the flavour average. These are genuine calculated contributions. Neither is the complete electromagnetic response, and a flat-space susceptibility is not the linear-in-\(H\) vacuum coefficient. Independent meson and baryon matching constants survive. The calculation therefore advances the response problem but does not determine the physical \(R=c_H/C_p^3\) or an isolated alpha root.

## 1. Fixed inputs and domain

Use \(\hbar=c=1\), \(e^2=4\pi\alpha\), zero temperature, infinite flat volume for the chiral calculation, positive light masses, and \(\theta\) near zero. The low-energy theory is SU(2) chiral perturbation theory with the strange quark integrated out and held fixed. \(F,B,Z,g_A\) denote matching quantities of the reference theory at \(e=0\); their electromagnetic corrections at the stated order are represented by the appropriate additional operators.

A fixed quark mass means an independently determined **renormalized full QCD+QED \(\overline{\rm MS}\) mass at the specified scale \(\mu_q=2\) GeV**, not a free-quark pole mass. Keep this convention and scale fixed as alpha changes. An RG-invariant mass can replace it only with the full corresponding QCD+QED conversion specified. The chiral subtraction scale \(\bar\mu\) is a different scale. Its dependence cancels between chiral logarithms and LECs. Changing the quark-mass convention reallocates electromagnetic effects between mass shifts and counterterms; it is not a physical prediction.

The formulas below first describe fixed strong reference parameters and these renormalized quark masses. A conversion is required before applying the parent's fixed-RG-invariant-mass constrained derivative: if \(m_i(\mu_q)=\widehat m_i U_i(\alpha,\Lambda/\mu_q)\), then fixed \(\widehat m_i\) does not mean fixed \(m_i(\mu_q)\) when either alpha or Lambda changes. Section 6 states both paths explicitly. Holding measured pion masses fixed instead would require additional retuning and would be a third derivative.

## 2. Leading electromagnetic vacuum term vanishes in the theta curvature

The leading potential, with the electric charge factored out of \(Q\), is

\[
V_2(U,\theta)=-{F^2\over4}\operatorname{tr}
(\chi_\theta U^\dagger+U\chi_\theta^\dagger)
-e^2 C\operatorname{tr}(QUQU^\dagger),\qquad
Q=\operatorname{diag}(2/3,-1/3).
\]

Here \(\chi_\theta=2B\,\operatorname{diag}(m_u,m_d)e^{i\theta/2}\); \(U\) is the SU(2) Goldstone field. The diagonal quark-vacuum phase matrix can equivalently include the common theta phase, which cancels in the Dashen trace.

For the aligned diagonal vacuum, \(U\) commutes with \(Q\). Thus
\(\operatorname{tr}(QUQU^\dagger)=\operatorname{tr}Q^2=5/9\), independent of theta. The Dashen operator changes charged-pion fluctuations but contributes no \(O(e^2p^0)\) topological susceptibility. Minimizing the quark-mass term gives

\[
E_2(\theta)=-F^2B
\sqrt{m_u^2+m_d^2+2m_um_d\cos\theta},
\qquad
\chi_0=F^2B{m_um_d\over m_u+m_d}.
\]

Set \(z=m_u/m_d\) and \(w=m_um_d/(m_u+m_d)^2=z/(1+z)^2\). The aligned pion mass obeys
\[
M_\theta^2=B\sqrt{(m_u+m_d)^2-4m_um_d\sin^2(\theta/2)},\quad
(M_\theta^2)'_0=0,\quad (M_\theta^2)''_0=-M^2w.
\]

These facts are checked directly from the action, rather than inferred from an arbitrary response coefficient.

## 3. Calculate the electromagnetic vacuum loop

In the finite chiral subtraction convention matching the pure-QCD logarithm of [Gorghetto–Villadoro, arXiv:1812.01008v2, Appendix A.1](https://arxiv.org/abs/1812.01008v2), one real pion contributes

\[
V_1(y)={y^2\over64\pi^2}
\left(\log{y\over\bar\mu^2}-{1\over2}\right).
\]

There are two charged real modes, with
\(y=M_\theta^2+\Delta_\pi^2\) and \(\Delta_\pi^2=2e^2F^2Z\).
Differentiate their determinant twice in theta, subtract the zero-charge determinant, and expand to first order in \(\Delta_\pi^2\):

\[
\delta\chi_{\rm loop}
=-M^2w\,\Delta_\pi^2
 {d^2\over d(M^2)^2}
 \left\{{M^4\over32\pi^2}
 \left(\log{M^2\over\bar\mu^2}-{1\over2}\right)\right\}
=-{M^2w\Delta_\pi^2\over16\pi^2}
 \left(1+\log{M^2\over\bar\mu^2}\right).
\]

Division by \(\chi_0=F^2M^2w\) yields the result above. The independent calculation which expands in \(\Delta_\pi^2\) first and differentiates theta second agrees exactly. A scalar subtraction \(1/2\mapsto c\) changes this fractional correction by
\(\Delta_\pi^2(2c-1)/(32\pi^2F^2)\), an analytic local term; the logarithmic mass coefficient is unchanged.

There is also a useful explicit alpha function for this one-loop contribution before expanding the charged mass:
\[
\left({\delta\chi\over\chi_0}\right)_{\rm loop}
=-{(M^2+\Delta_\pi^2)\log[(M^2+\Delta_\pi^2)/\bar\mu^2]
       -M^2\log(M^2/\bar\mu^2)\over16\pi^2F^2},
\]
\[
\partial_{\ln\alpha}
\left({\delta\chi\over\chi_0}\right)_{\rm loop}
=-{\Delta_\pi^2\over16\pi^2F^2}
  \left[1+\log{M^2+\Delta_\pi^2\over\bar\mu^2}\right].
\]
Both follow from the same determinant and are checked exactly. They retain only the leading charged-mass insertion inside one loop, and are not a complete higher-order alpha calculation. The displayed linear \(e^2\) expansion assumes positive \(M\) before expansion; it is not uniform as \(M\to0\) at fixed charge. At positive \(\Delta_\pi^2\), the continuous chiral limit of this loop fraction is instead
\(-\Delta_\pi^2\log(\Delta_\pi^2/\bar\mu^2)/(16\pi^2F^2)\).
The susceptibility itself still vanishes with its leading mass factor. No physical alpha was substituted into these functions.

The complete leading electromagnetic expression in the fixed-quark-mass variables is the source's equation (36):

\[
\chi_{\rm top}=\chi_0[1+\delta_{\rm QCD}
+e^2K_\chi^r
-{e^2 Z\over8\pi^2}(1+\log(M^2/\bar\mu^2))+\cdots],
\]
\[
K_\chi^r={20\over9}(k_5^r+k_6^r)
       +{4\over9}(1+3\Delta)k_7^r,\qquad
\Delta={m_d-m_u\over m_d+m_u}.
\]

Thus at this order \(\partial_{\ln\alpha}\ln\chi_{\rm top}\) contains the displayed \(e^2\) correction, including \(K_\chi^r\). The known nonanalytic term alone has a subtraction-scale dependence; it must not be reported as a physical numerical slope by itself. The meson LECs can in principle be independently matched using QCD current correlators or lattice QCD+QED. Their resonance-model estimates are not a first-principles alpha prediction. In particular, the paper's main-text numerical correction using pion-mass and decay inputs is not used here as either the fixed-quark-mass derivative or \(c_H\).

## 4. Direct contact with the source's condensate numerator

The older proposed coefficient is proportional to \(2N_fm_q\Sigma/m_{\eta'}\), with an inverse geometric length supplying the fourth mass dimension; see [Urban–Zhitnitsky, arXiv:0909.2684v4, equation (1.1)](https://arxiv.org/abs/0909.2684v4). For two degenerate quarks \(m_u=m_d=m\), \(M^2=2Bm\). The electromagnetic piece of the charged determinant is

\[
\delta E_{\rm loop}
={\Delta_\pi^2M^2\over16\pi^2}\log{M^2\over\bar\mu^2}.
\]

At zero theta, the flavour-averaged product is
\[
m\Sigma=-{m\over2}\partial_m E
       =-{M^2\over2}\partial_{M^2}E.
\]
Consequently
\[
{\delta(m\Sigma)_{\rm loop}\over(m\Sigma)_0}
=-{\Delta_\pi^2\over16\pi^2F^2}
 \left(1+\log{M^2\over\bar\mu^2}\right),
\qquad (m\Sigma)_0={F^2M^2\over2}.
\]

This independently reproduces the fractional susceptibility loop in the degenerate limit. At leading chiral order \(\chi_0=m\Sigma/2\), so the proposed dimensional numerator would be \(8\chi_0/m_{\eta'}\). This translation is restricted to that degenerate source approximation; it is not a general identity between the physical geometric response and the physical topological susceptibility.

Even granting a fixed geometric prescription, the candidate's logarithmic response has the form
\[
d\log A_H=d\log(m\Sigma)-d\log m_{\eta'}
              +d\log({\rm geometric\ matching}),
\qquad A_H=c_H\Lambda^3.
\]
Neither the eta-prime electromagnetic matching nor the geometry response is supplied by this flat SU(2) calculation. The flavour-singlet field has already been integrated out. A U(3) anomaly/EM matching calculation or a corresponding nonperturbative correlator is needed to compute its derivative. Substituting the measured eta-prime mass at every alpha would impose an extra mass constraint.

One leading statement does survive restoring a singlet phase: replacing \(U\) by \(e^{i\phi_0}U\) leaves \(\operatorname{tr}(QUQU^\dagger)\) unchanged. The Dashen operator therefore gives no direct \(O(e^2p^0)\) singlet mass either. This removes that particular possible eta-prime contribution, while leaving the mass/anomaly-dependent operators, loops and pole-mass matching unresolved.

## 5. Calculate the individual proton terms

The invariant baryon electromagnetic Lagrangian of [Müller–Meißner, arXiv:hep-ph/9903375v1, equations (2.28)–(2.29)](https://arxiv.org/abs/hep-ph/9903375v1) contains \(F^2\bar N(f_1O_1+f_2O_2+f_3O_3)N\). In this operator-defined convention, at \(U=1\) and \(Q_N=e\,\operatorname{diag}(1,0)\),

\[
O_1=O_3={e^2\over2}{\bf1},\quad O_2={e^2\over2}\tau_3,\quad
\delta m_p^{\rm local}=-{e^2F^2\over2}(f_1+f_3+f_2),\quad
\delta m_n^{\rm local}=-{e^2F^2\over2}(f_1+f_3-f_2).
\]

The sign is fixed by the mass operator \(-m_N\bar NN\), and the dimensions by \([f_i]=({\rm mass})^{-1}\). The preprint's printed equation (3.8) has a different isoscalar sign and lacks the \(F^2\) appearing in (2.28). This lane does not propagate that inconsistent printed formula. The local masses above are derived directly from its invariant Lagrangian; the unambiguous splitting is \(\delta m_p-\delta m_n=-e^2F^2f_2\).

The same paper's equation (3.4) supplies a clean one-loop term:

\[
\delta m_N^{(3),{\rm EM}}
=-{g_A^2\over16\pi F^2}
 \big[(M^2+\Delta_\pi^2)^{3/2}-M^3\big]
=-{3g_A^2M\Delta_\pi^2\over32\pi F^2}+O(e^4)
=-{3e^2g_A^2ZM\over16\pi}+O(e^4).
\]

It is equal for proton and neutron. At the stated chiral order it is the nonanalytic \(e^2\sqrt{m_q}\) contribution. The derivative of the individual proton mass therefore includes both this term and the local constant above:
\[
\left.\partial_{\ln\alpha}\log m_p\right|_{\Lambda,m_i}
={1\over m_p}\left[
-{e^2F^2\over2}(f_1+f_3+f_2)
-{3e^2g_A^2ZM\over16\pi}+\cdots\right].
\]

Higher chiral orders add further loop and local terms. The shared pion cloud and the isoscalar \(f_1+f_3\) contribution both cancel in the proton–neutron difference. An electromagnetic splitting cannot determine this individual derivative. An elastic-only Cottingham number likewise omits inelastic/subtraction and mass-renormalization contributions. No such number is used here.

## 6. The unknown coefficients do not cancel by chiral symmetry

This is a statement about actual operators: the meson \(k_i\) operators govern a zero-baryon vacuum functional, whereas \(\bar NN O_i\) governs a one-baryon sector. At zero baryon density the latter has no external nucleon legs; closed high-energy baryon effects have already been matched into meson constants. Chiral symmetry supplies no equality eliminating the one-baryon isoscalar matching constant using \(K_\chi^r\).

For the fixed-ratio derivative of \(R\), the local baryon term contributes
\[
-3\,{\delta m_p^{\rm local}\over m_p}
= {3e^2F^2\over2m_p}(f_1+f_3+f_2).
\]
The numerator has no compensating occurrence of this one-baryon operator. A numerical correlation after a full QCD calculation would be additional dynamical information, not an EFT cancellation.

For fixed renormalized masses \(m_i(\mu_q)\) **and fixed proton mass**, the precise constraint is
\[
S_{\overline{\rm MS}}=a_\alpha-{b_\Lambda\over a_\Lambda}p_\alpha,\qquad
a_\Lambda=\left.\partial_{\ln\Lambda}\log m_p\right|_{\alpha,m_i(\mu_q)},\quad
b_\Lambda=\left.\partial_{\ln\Lambda}\log A_H\right|_{\alpha,m_i(\mu_q)},
\]
where \(p_\alpha=\partial_{\ln\alpha}\log m_p\) and
\(a_\alpha=\partial_{\ln\alpha}\log A_H\) hold Lambda and the same renormalized masses fixed. This follows directly by eliminating \(d\log\Lambda\) from the proton constraint and requires \(a_\Lambda\ne0\). It accounts for the explicit reference-scale dependence of the running masses.

For the parent's fixed-invariant-mass convention, first convert all mass and charge derivatives with \(m_i(\mu_q)=\widehat m_i U_i\). For example,
\[
p_\alpha^{\widehat m}=p_\alpha^{m}
+\sum_i p_i^m\left.\partial_{\ln\alpha}\log U_i\right|_\Lambda,
\qquad
h_\alpha^{\widehat m}=h_\alpha^{m}
+\sum_i h_i^m\left.\partial_{\ln\alpha}\log U_i\right|_\Lambda.
\]
Here \(p_i^m=\partial_{\ln m_i}\log m_p\), \(h_i^m=\partial_{\ln m_i}\log A_H\) at fixed Lambda and alpha. After that common convention conversion, \(x_i=\widehat m_i/\Lambda\), \(a_\Lambda=1-P\), \(b_\Lambda=3-Q\), and the parent's formula applies:
\[
S_{\rm constrained}=h_\alpha-
 {3-Q\over1-P}p_\alpha,\qquad
P=\sum_i{\sigma_i^p\over m_p},\quad
Q=\sum_i\partial_{\ln x_i}\log c_H.
\]
Here \(h_\alpha=\partial_{\ln\alpha}\log c_H|_x\),
\(p_\alpha=\partial_{\ln\alpha}\log C_p|_x\), and
\(\sigma_i^p=\widehat m_i\partial_{\widehat m_i}m_p\) in that invariant convention. The baryon constant survives at first order as
\[
{\partial S_{\rm constrained}\over\partial f_3}
={3-Q\over1-P}\,{e^2F^2\over2m_p}.
\]
In the fixed-\(\overline{\rm MS}\) path its analogous coefficient is
\((b_\Lambda/a_\Lambda)e^2F^2/(2m_p)\). Mass-conversion terms introduce no independent relation fixing \(f_3\). There is no cancellation on an ordinary regular branch; \(Q=3\) would be a special additional dynamical condition, and \(P=1\) invalidates the invariant-mass implicit-function branch. The source's leading \(m_q\Lambda^2\) dimensional coefficient has \(Q\simeq1\), before higher chiral corrections, rather than a symmetry forcing \(Q=3\).

## 7. Exact nonperturbative response observables

The derivative is in principle calculable without supplying a numerical alpha. Integrate the free photon field in a fixed Euclidean geometry \(g\) and define the renormalized insertion

\[
\mathcal I_g={1\over2}\int_{x,y}
 j_\mu(x)D_g^{\mu\nu}(x,y)j_\nu(y)
 +\mathcal I_g^{\rm ct},
\qquad S_{\rm eff}=S_{\rm QCD}+e^2\mathcal I_g+O(e^4).
\]

Measures include the metric determinants; \(j_\mu=\sum_fQ_f\bar q_f\gamma_\mu q_f\). Counterterms implement the specified fixed renormalized quark masses and strong matching, and local vacuum/curvature subtraction. The contact terms include mass operators and the gluonic operator. The underlying current-current expansion and required matching are derived in [de Divitiis et al., arXiv:1303.4896v1, section 2, equations (2)–(7)](https://arxiv.org/abs/1303.4896v1). Our notation includes the factor \(1/2\) in \(\mathcal I\).

Define \(W_g=-\log Z_g\) and the Euclidean effective-action density \(f_g=W_g/V_g\). In a flat translation-invariant ground state this equals its vacuum energy density after the specified subtraction. On a curved geometry it is not automatically the gravitating energy density. For total gluonic topological charge \(\mathcal Q\), CP symmetry at theta zero gives
\[
\partial_{e^2}f_g={\langle\mathcal I_g\rangle\over V_g},\qquad
\partial_{e^2}\chi_{\rm top}
=-{1\over V_g}\langle\mathcal Q^2;\mathcal I_g\rangle.
\]

The second identity here describes the flat susceptibility used above; more generally it holds for \(\partial_\theta^2 f_g\) at fixed geometry and volume. These insertions are different observables. Their geometric difference would compute the effective-action-density coefficient
\[
\partial_{e^2}A_H^{f}=
\lim_{H\to0^+}{1\over H}
\left[
{\langle\mathcal I_{g_H}\rangle\over V_{g_H}}
-{\langle\mathcal I_{\rm flat}\rangle\over V_{\rm flat}}
\right],
\]
with the same state, regulator, subtractions and matching, provided this limit and interchange of derivatives exist. This equals the required response of \(A_H=c_H\Lambda^3\) only if the source's energy density is defined to be \(f_g\) or an appropriate metric-variation relation has been established. The gravitating response otherwise requires the metric derivative of \(\partial_{e^2}W_g=\langle\mathcal I_g\rangle\), including the metric dependence of the insertion, regulator and subtraction. A known \(\langle\mathcal Q^2;\mathcal I\rangle\) evaluates neither that stress response nor the geometric free-energy difference.

For illustration, on a closed round four-sphere suppose the complete matched effective action has the form \(W(H)=V(H)f(H)\), \(V(H)\propto H^{-4}\), the stress is maximally symmetric, and a specified continuation identifies its coefficient with a Lorentzian vacuum density. A uniform metric rescaling gives
\[
\rho(H)=f(H)-{H\over4}\partial_H f(H).
\]
Consequently \(f(H)-f(0)=A_H^f H+\cdots\) gives
\(\rho(H)-\rho(0)=\tfrac34 A_H^f H+\cdots\), and the same factor multiplies the electromagnetic derivative. It is not valid to drop this factor by naming \(W/V\) an energy density. A hyperbolic product geometry, a nonhomogeneous state or independently varied compact direction requires its appropriate metric variation; a single diagonal family of \(W\) values does not determine all stress components.

For a proton two-point correlator \(C_p(T)=\langle N_p(T)\bar N_p(0)\rangle\), the individual rest-energy derivative is
\[
\partial_{e^2}m_p=\lim_{T\to\infty}{1\over T}
\left[
{\langle N_p(T)\bar N_p(0)\mathcal I_{\rm flat}\rangle\over C_p(T)}
-\langle\mathcal I_{\rm flat}\rangle
\right].
\]

All sea, disconnected and valence terms and the mass/strong counterterms belong in the insertion. A photon mass or specified finite-volume QED prescription is needed before extracting the charged state; take the controlled infinite-volume/zero-regulator rest threshold. Gauge-invariant dressing or a specified gauge treatment of charged interpolators must be fixed. These prescriptions are part of an executable lattice measurement, not extra measured alpha data.

## 8. Matching and covariance

An independently matched \(Z\), \(g_A\), meson LEC, sigma term or individual proton insertion can be used as a conditional hadronic input. If extracted from a simulation at a known nonzero alpha, record that alpha as a calibration input; it cannot then be counted as a held-out prediction of alpha. Expanding at \(e=0\) with the known rational quark charges avoids importing the target charge into the derivative itself. No lattice derivative value is imported in this lane.

When a measured proton mass fixes the strong scale, the proton response determines the required retuning. The same proton mass also appears in \(R_{\rm observed}\propto m_p^{-3}\); its uncertainty and the retuning are correlated. Meson masses used to set lattice spacing, quark masses used to tune ensembles, and matching LECs can have shared covariances. Keeping them fixed simultaneously without the matching Jacobian can change the intended path. Neither a Lambda convention change nor a covariance treatment supplies the missing geometry insertion.

## 9. Executed audit and reproduction

The current run is run_003. Its manifest has status completed and validates against the present input hashes. All 29 exact symbolic checks pass. They include the diagonal Dashen potential, stationary vacuum curvature, the two orders of differentiating the charged determinant, agreement with the pure-QCD and QED logarithms, the unexpanded charged-mass kernel and its derivative/chiral limit, finite-subtraction dependence, the degenerate condensate derivative, baryon invariant operators, the nonanalytic nucleon loop, and zero-charge/equal-mass benchmarks. SymPy handles exact expressions; there is no numerical sampling or tolerance.

Python 3.9.6 and SymPy 1.14.0 were observed. The command is recorded as an argv array in run_003/manifest.json. Regenerate with the installed computation-audit runner, contract_v3.json, inputs chiral_response_v3.py and SOURCE_INPUTS.json, a fresh output directory, and:

    python3 fine_structure_puzzle/qcd_prediction/electromagnetic/chiral_response_v3.py --output <fresh-output-directory>/result.json

The runner enforces 30 seconds wall time, 20 seconds CPU, 1 MiB combined logs and conventional one-thread limits. Validation:

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_prediction/electromagnetic/run_003/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula

The first contract invocation was rejected before execution because its conventions field had the wrong JSON type; contract_invalid.json preserves it. Run_001 then failed because SymPy did not simplify \(\sqrt{m_u^2+2m_um_d+m_d^2}\) to \(m_u+m_d\) automatically. Its script, contract and failed manifest remain intact. Version 2 writes the same positive-root mass as \(\sqrt{(m_u+m_d)^2-4m_um_d\sin^2(\theta/2)}\); no physical assertion changed. This was a symbolic-normal-form failure, not a counterexample to the susceptibility. Run_002 completed 24 checks; version 3 adds the five checks of the unexpanded one-loop kernel and the chiral-limit qualification. Public-source acquisition had a DNS failure and one wrong-version 404, both corrected after exact version authentication.

Outcome: **implementation and finite symbolic assertion verified in the stated chiral domain**. This is not verification of the de Sitter mechanism, the physical LECs, a complete individual proton self-energy, or a numerical alpha root.

## 10. First unresolved implication and executable continuation

The first missing implication remains the independent geometric **stress-energy** observable \(A_H=c_H\Lambda^3\). A flat susceptibility or condensate calculation does not establish its value or its electromagnetic derivative, and a curved \(W/V\) response still needs the metric-variation bridge. Even if that geometric bridge were granted, meson EM matching, eta-prime EM matching and the individual proton's isoscalar EM response remain necessary. The displayed terms establish nonzero contributions to the stated flat-space chiral observables; they do not prove that the physical \(c_H\) response is nonzero. The operator analysis demonstrates why the matching unknowns do not cancel automatically.

The next physical calculation is a common-scheme measurement of the current-current insertion in (i) the proton two-point function, (ii) the theta-susceptibility/condensate sector, and, once a definite geometry/state is supplied, (iii) the geometry-subtracted vacuum functional together with the metric variation giving stress. Record quark-mass and scale retunings rather than fitting a vacuum coefficient. The formulas in section 7 specify the observables and signs, with the distinction between \(f_g\) and \(\rho_g\) retained; the current chiral calculation supplies infrared benchmarks for their mass dependence. A deformed-QCD or lower-dimensional geometry computation elsewhere in FSP-003 is a controlled benchmark, not the missing physical four-dimensional matching.
