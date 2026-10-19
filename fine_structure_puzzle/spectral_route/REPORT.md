# FSP-S: what a spectral mechanism must fix

Checkpoint FSP-000. Written 2026-10-18 America/New_York (2026-10-19 UTC).
Base Git revision `3c01aa2861bf576f4c2d942251eb9d2f89cae108`, dirty baseline.
Owner scope: `fine_structure_puzzle/spectral_route/` only.

**Result: alpha(0) is not derived.** A positive current spectrum determines a subtracted response and hence running, while a local Maxwell coefficient remains matching data. The strongest checked escape is exact reconstruction of protected coupling **functions** in particular string dualities; their vacuum moduli are still unselected. This is an obstruction for the premises specified below, not an impossibility theorem for UV theories.

## 1. What changes relative to the old lanes

Read-only inputs were TARGET.md; ALPHA_CHAIN_STATUS.md, especially C/J/N2/X1; C0_PREREGISTRATION.md; J_PREREGISTRATION.md; and J1/J2 code. C used a one-loop tower sum with a species cutoff; J added a vanishing bare Maxwell term and exposed the spectrum, hierarchy, and regulator dependence. No such spectrum fit is repeated here. The new question is whether positivity, anomaly matching, compactness, or an actual UV principle determines the subtraction coefficient, including finite matching terms.

The first uncertain implication is

\[
\text{physical spectrum and its consistency conditions}
\quad\Longrightarrow\quad
\text{unique absolute Maxwell coefficient}.
\]

For a prescribed background-current theory that implication is false: a local deformation leaves its absorptive data and stated consistency conditions unchanged. If a UV theory supplies additional restrictions, its application must be checked separately.

## 2. Conventions and an explicit dispersion relation

Use \(\hbar=c_{\rm light}=1\). Normalize the compact connection \(A\) so that a primitive Wilson line has integer charge one, not by rescaling \(A\) to put the kinetic coefficient to one. Write

\[
\mathcal L=-\frac{K}{4}F_{\mu\nu}F^{\mu\nu}+A_\mu j^\mu,
\qquad q_i\in\mathbb Z.
\]

If the electron has integer lattice charge \(q_e\), the Thomson limit is

\[
\alpha(0)=\frac{q_e^2}{4\pi K_{\rm phys}(0)}. \tag{1}
\]

The toy computation takes \(q_e=1\). A physical SM application must supply its actual lattice embedding; the electron need not be primitive.

First keep the charged matter theory ungauged and couple it to a background \(A\). Assume a Lorentz invariant, unitary vacuum, a conserved current, a gap \(s_0>0\) in its spectral support, and sufficient polynomial boundedness for one subtraction. Define the Minkowski scalar by

\[
i\int d^4x\,e^{iqx}\langle Tj_\mu(x)j_\nu(0)\rangle
=(q_\mu q_\nu-q^2\eta_{\mu\nu})\Pi(q^2),
\qquad \rho(s)=\frac1\pi\operatorname{Im}\Pi(s+i0)\ge0.
\]

The once-subtracted relation and its Euclidean form are

\[
\Pi(q^2)-\Pi(0)=q^2\int_{s_0}^{\infty}
\frac{\rho(s)\,ds}{s(s-q^2-i0)},
\]
\[
P(Q^2):=\Pi(0)-\Pi(-Q^2)
=Q^2\int_{s_0}^{\infty}\frac{\rho(s)\,ds}{s(s+Q^2)}\ge0. \tag{2}
\]

When this sector is weakly gauged, its contribution to the quadratic photon kernel is

\[
K(Q^2)=K(0)-P(Q^2),\qquad
\alpha(Q^2)^{-1}=\alpha(0)^{-1}-\frac{4\pi}{q_e^2}P(Q^2). \tag{3}
\]

Here (2) is exact for the specified background matter theory; (3) describes its contribution at leading order in gauging, with matter interactions treated exactly. Photon loops and other sectors must be added for full electromagnetic precision. The physical full 1PI residue in (1) is defined after those corrections. No identification of an arbitrary connected-current spectrum with an exact full photon 1PI spectrum is assumed.

In particular,

\[
\frac{dP}{d\log Q^2}
=Q^2\int_{s_0}^{\infty}\frac{\rho(s)\,ds}{(s+Q^2)^2}\ge0. \tag{4}
\]

This supplies screening and an Adler-type derivative, not \(K(0)\). A contemporary lattice example computes subtracted HVP functions and uses the Thomson value as the boundary datum: Conigli et al., [arXiv:2502.10159v1](https://arxiv.org/html/2502.10159v1), §2.2, (1)–(3). Their Euclidean \(\bar\Pi\) equals our \(P/q_e^2\) after current-normalization translation; their Euclidean tensor sign differs from our Minkowski scalar convention.

## 3. The local term is not removed by the proposed constraints

For the background generating functional, the finite local change

\[
W[A]\longmapsto W[A]+\frac{c}{4}\int F_{\mu\nu}F^{\mu\nu}
\]

in Euclidean conventions shifts the real transverse contact coefficient by \(c\). It changes neither \(\rho\), separated-point current correlators, nor (2)/(4). Once \(A\) is dynamical, a change of the **total** kinetic coefficient is physical matching data and changes the charge-normalized coupling. A mere renormalization-scheme change instead redistributes the local pieces between the matter functional and bare term while preserving the total physical kernel. These are different operations.

The following claims concern the specified class, not arbitrary UV completions:

| Proposed condition | What is fixed | Why the absolute coefficient survives |
|---|---|---|
| Spectral positivity | \(\rho\ge0\), sign of (4) | A transverse local contact term has no discontinuity. Positivity of the photon kinetic term imposes an inequality. |
| Compact charge lattice | Integer \(q_i\), primitive Wilson line, allowed fluxes | \(\int F\wedge *F\) depends on the metric and is not a quantized characteristic number. Its positive coefficient is continuous. |
| Perturbative gauge anomaly cancellation | \(\sum q_i^3=0\), mixed gravitational condition \(\sum q_i=0\) for left Weyl charges | Both are independent of \(K\). One Dirac fermion has left-Weyl charges \((1,-1)\) and satisfies both for every \(K>0\). |
| 't Hooft anomaly matching | Anomaly coefficients of a specified global symmetry | A gauge invariant \(F^2\) contact term changes no gauge variation. A nonzero uncancelled gauge anomaly would obstruct gauging rather than select its strength. |
| External-field trace anomaly / current central charge | Logarithmic response in a chosen normalization | A finite \(\int F^2\) term is Weyl invariant in four dimensions and does not alter that anomaly. A derivative does not determine its integration constant. |

There is also a physical local EFT family, rather than just a background-functional convention: vectorlike QED actions with the same compact lattice, fermion content and fixed renormalized mass, but different positive Maxwell coefficients at a specified finite UV matching scale. They preserve these conditions in a common perturbative regime. Their fully gauged spectra can differ at higher orders. The claim here is **not** that distinct interacting QED couplings have identical exact full spectra.

The focused sufficiency claim “positive spectral data, anomaly matching, and a compact lattice determine the Maxwell coefficient” is therefore **refuted within this background-current / finite-cutoff EFT class**. The counterterm operation is the smallest counterexample. A special UV completion may forbid or determine that operation through additional physical data.

## 4. Strongest simple closure and a discriminating computation

Try the stronger boundary principle

\[
K(Q^2)\to0\quad(Q^2\to\infty),\qquad
K(Q^2)=\int_{s_0}^{\infty}\frac{\rho(s)\,ds}{s+Q^2}.
\]

If the integral converges, this would imply

\[
K(0)=\int_{s_0}^{\infty}\frac{\rho(s)}s\,ds. \tag{5}
\]

This really would remove the contact freedom **conditional on** an independently justified boundary condition and a fully fixed spectral density. Ordinary four-dimensional nontrivial UV CFT currents have dimension three, \(\langle JJ\rangle\sim C_J/x^6\), and a positive nonzero asymptotic spectral constant. Then (5) diverges logarithmically. The usual once-subtracted relation remains well-defined. Thus positivity does not turn ordinary 4d current data into (5). This conditional observation does not exclude a different dynamical UV construction or a sum rule involving other sectors and different assumptions.

For the cheapest exact-shape test, take one free Dirac current of mass \(m\) and primitive charge one:

\[
\rho_D(s)=\frac{1}{12\pi^2}
\left(1+\frac{2m^2}{s}\right)\sqrt{1-\frac{4m^2}{s}}
\,\theta(s-4m^2). \tag{6}
\]

Equation (2) must agree with the independent Feynman-parameter expression

\[
P_D(Q^2)=\frac{1}{2\pi^2}\int_0^1 dx\,x(1-x)
\log\left[1+\frac{Q^2}{m^2}x(1-x)\right]. \tag{7}
\]

The checks also recover \(P_D(Q^2)=Q^2/(60\pi^2m^2)+O(Q^4/m^4)\) and the asymptotic logarithmic slope \(dP_D/d\log Q^2\to1/(12\pi^2)\).

Make the attempted closure maximally favorable by truncating (6) to \(4m^2\le s\le\Lambda^2\), with \(\Lambda>2m\). Set

\[
K_c(Q^2)=c+\int_{4m^2}^{\Lambda^2}
\frac{\rho_D(s)}{s+Q^2}\,ds,\qquad c\ge0. \tag{8}
\]

All kernels in (8) are positive for Euclidean \(Q^2\ge0\). The same background spectrum, primitive lattice, and vanishing anomalies admit all \(c\); \(K_c(\infty)=c\). Even imposing the strong boundary \(c=0\) leaves

\[
\alpha(0)^{-1}=\frac{1}{3\pi}
\left[\frac{v^3}{3}-2v+2\operatorname{arctanh}v\right],
\qquad v=\sqrt{1-4m^2/\Lambda^2}. \tag{9}
\]

The formula follows by substituting \(s=4m^2/(1-v^2)\). Its large-ratio limit is

\[
\alpha(0)^{-1}=\frac{1}{3\pi}
\left[\log\frac{\Lambda^2}{m^2}-\frac53
+O(m^4/\Lambda^4)\right]. \tag{10}
\]

The constant in this explicitly specified band model is fixed, not a fit or an arbitrary scheme offset. The remaining scale ratio is free. A hard upper spectral band is a diagnostic positive-response model, **not an asserted local UV-complete QFT**. It evades the constant-UV-spectrum premise by construction; that construction requires a physical explanation before it can describe nature.

Executed examples (no measured alpha or measured mass supplied):

| \(\Lambda/m\) | \(\alpha^{-1}(0)\), \(c=0\) | \(c=1\) | \(c=10\) |
|---:|---:|---:|---:|
| \(10^2\) | 0.8004086427 | 13.3667792571 | 126.4641147863 |
| \(10^4\) | 1.7776561047 | 14.3440267190 | 127.4413622483 |
| \(10^8\) | 3.7321510350 | 16.2985216494 | 129.3958571786 |

The shift is exactly \(4\pi c\), before numerical rounding. The continuum of ratios survives at \(c=0\). No target proximity test was performed.

These are kernel-defined effective coefficients, not precision predictions of fully gauged QED. The \(c=0\) examples have strong effective coupling, so their leading-weak-gauging interpretation is not controlled. The physical EFT counterfamily can instead be restricted to sufficiently large \(c>0\) in a common perturbative window; the mathematical subtraction diagnostic does not require that restriction.

Three boundaries must not be conflated: (i) a zero bare Wilsonian coefficient in a specified microscopic regulator, (ii) the physical momentum-subtraction condition \(K(Q_*^2)=0\), and (iii) the large-Euclidean-momentum condition used in (8). They are not equal without a matching derivation. In particular, imposing a divergent physical gauge coupling at a finite scale and extrapolating a one-loop calculation to that point does not establish controlled matching.

## 5. Checked modern escape routes

These are scoped primary-source checks, not an exhaustive classification.

**Neutral current bootstrap.** Karateev, Kravchuk, Manenti, Reehorst and Vichi, [arXiv:2512.20710v2](https://arxiv.org/html/2512.20710v2), §2 (2.1)–(2.7), §4: four-dimensional parity invariant CFTs with global U(1), using neutral \(\langle JJJJ\rangle\). The normalized anomaly combination is bounded; canonical current normalization cannot be imposed using this neutral sector. A mixed system containing charged operators is a concrete improvement. Even isolated charge-normalized matter data would still require a dynamical gauging/UV condition fixing (1). Application to an alpha derivation: **inapplicable with the presently checked hypotheses**.

**Gauge–gravity tower coincidence.** Heidenreich, Reece and Rudelius, [arXiv:1712.01868v2](https://arxiv.org/abs/1712.01868v2), §2 (2.1)–(2.7), §3: near-sLWGC-saturating charged towers can make gauge and gravitational strong-coupling scales parametrically agree. The logarithms, constants, tower spacing, domination of the species count by charged states and UV coupling matter. This supplies no exact subtraction normalization. Application: **conditional parametric relation, not a numerical closure**.

**Exact emergence via string duality.** Blumenhagen, Cribiori, Gligovic and Paraskevopoulou, [arXiv:2309.11551v3](https://arxiv.org/html/2309.11551v3), §2.2 and §§3.2, 4, 5: protected prepotentials are reconstructed in particular asymptotic type-IIA \(\mathcal N=2\) settings, using complete towers and specified regularizations or a dual quantum theory. The exact-emergence notion is broader than “everything comes from one loop.” Their (4.8), \(\mathcal F_0^{\rm het}=ST^2/2+h^{(1)}(T)+h^{(\rm np)}(e^{-8\pi^2S})\), visibly retains scalar vacuum parameters. Thus UV data can fix local pieces **within a theory**, while the selected vacuum remains missing here. No SM vacuum selection or Thomson matching is supplied by this source. Application: **genuine structural escape, conditional on additional vacuum physics**.

**Recent protected \(F^4\) evidence.** Artime, Blumenhagen and Paraskevopoulou, [arXiv:2504.05392v2](https://arxiv.org/html/2504.05392v2), §2.2, §3 and §5: a six-dimensional protected \(F^4\) amplitude at a special K3 orbifold/Wilson-line locus supports a prescription for excluding heavy wrapped D4 contributions. The instanton cancellation is checked through five instantons; the six-instanton case has technical difficulties. It concerns a higher-derivative coupling at specified moduli and does not fix four-dimensional electromagnetic \(F^2\). Application: **adjacent evidence, not the needed normalization theorem**.

**Photon S-matrix bootstrap and gravitational positivity.** Häring et al., [arXiv:2211.05795v1](https://arxiv.org/html/2211.05795v1), §1 (6), §2, appendix E.2, constrain four-photon low-energy coefficients using analyticity and unitarity, without fixing a charged probe's primitive electric charge. Alberte et al., [arXiv:2012.05798v1](https://arxiv.org/html/2012.05798v1), §4, give a new-physics cutoff scaling \(\Lambda_{\rm new}\lesssim(emM_{\rm Pl})^{1/2}\) conditional on a treatment that discards the massless gravitational t-channel pole; they discuss the caveat. These are constraints on combinations of couplings, masses and UV physics, not a unique \(e\). Application: **bounds/conditional constraints, not a closure**.

## 6. Computation provenance and self-audit

`spectral_check.py`, `contract.json`, and the current manifests pin conventions, finite domains, precision and output hashes. `runs/main_003/manifest.json` has status **completed**, exit 0: 65 assertions at each of 70 and 100 digits, with agreement of the two integral forms to the declared absolute \(10^{-40}\) tolerance and stability of reported P values to \(10^{-33}\). The sign mutation in `runs/sign_control_001/manifest.json` has status **failed**, exit 1 as intended: 11 assertions fail at each precision. Both current manifests validate with the skill validator. This is high-precision floating quadrature, not interval certification. The symbolic argument establishing the continuous local family does not depend on numerical tolerances.

Failures are retained. `main_001` could not launch because the host rejected the requested RLIMIT_AS setting (`ValueError: current limit exceeds maximum limit` in a minimal direct reproduction). The retry omitted that optional memory cap while preserving wall, output, CPU and thread limits. `main_002` failed one overly ambitious numerical-precision check: evaluating \(v\) near one in (9) at 50 digits lost about 16 digits, giving an absolute residual \(1.276\times10^{-38}\) at \(\Lambda/m=10^8\), above the unchanged \(10^{-40}\) tolerance. Its 80-digit evaluation passed. Precision was increased to 70/100 digits; no tolerance or mathematical domain was relaxed. The original script and contract are retained under `archive_inputs/`; historical input hashes refer to that original content, not the revised current script.

| Self-audit obligation | Result |
|---|---|
| Primitive lattice and electron factor distinguished | Passed: (1), toy \(q_e=1\) only. |
| Spectral signs and normalization | Passed: threshold spectrum (6), independent integral (7), low-Q and UV-slope benchmarks, sign control. |
| Local shift versus mere scheme change | Passed: different total matching coefficient changes physics; scheme redistribution does not. |
| Background versus fully gauged spectrum | Restricted explicitly: no isospectral exact-QED assertion. |
| Strong boundary convergence | Conditional: (5) needs UV falloff; positive constant spectrum fails it. |
| Toy spectral-band physical admissibility | Not established; deliberately excluded from the claims. |
| UV completion fixing the matching term and vacuum | Not supplied. This is the decisive remaining gap. |
| Full SM running, electroweak matching, hadronic and higher-order precision | Not performed; no absolute prediction exists to run. |

Proof review and mathematical proofreading were self-reviews, not independent certification. New-file coverage: this report and the computation. No mathematical-token changes arose from the final proofreading pass.

## 7. Concrete continuation and admission gate

The promising physical question is **vacuum selection in an explicit UV theory with computable absolute matching**, rather than another positive tower sum. The checked exact-emergence examples show why a bare EFT counterterm objection alone is not a global obstruction: extra UV structure can calculate local terms. They do not select which vacuum realizes electromagnetism.

The next bounded action is to choose one concrete four-dimensional compactification with a specified primitive U(1), stabilized scalar vacuum, and controlled threshold calculation. Before evaluating alpha, differentiate its charge-normalized physical kinetic coefficient along every allowed scalar flat direction. A nonzero derivative along an unstabilized direction rejects predictivity immediately; if none remain, enumerate the remaining discrete vacuum and charge-embedding choices, derive the complete finite matching coefficient, and only then run to the Thomson limit. The choice must be independently motivated before comparing any number to the measured answer.

For a bootstrap continuation, the analogous gate is a mixed charged-operator/current system that isolates an actual dynamical gauge theory and a unique critical coupling plus its relevant deformation/threshold trajectory. Determining only \(C_J\), an anomaly ratio, a positivity cone, or a function \(K(t)\) does not satisfy that gate. Neither continuation is represented as executed or as a present solution.

Regeneration and exact source checks are in `README.md`, `source_records.json` and `provenance.json`.
