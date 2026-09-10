# Kepler-grade equation candidates: reference list

Author/project: Carl P. Zimmerman, Zimmerman gravity programme; AI-assisted compilation requested by Carl. Research snapshot: `25ebacace` (9 September 2026).

**Purpose:** a stable reference for seven claim families worth preserving in a dated priority record. “Kepler-grade” describes potential significance **if independently and repeatedly confirmed**, not their present status. This document establishes neither worldwide originality nor empirical truth nor a completed relativistic theory. A mathematical consequence can survive the failure of its original host action without rescuing that action.

Refer to entries as **K01–K07**. Lead with K01–K04; K05–K07 are supporting or conditional results. Equivalent expressions and corollaries are grouped rather than counted as separate discoveries. The list covers the audited shortlist, not every result in the repository.

## K01 — Exact cosmology–galaxy normalization

\[
Z=2\sqrt{8\pi/3}=\sqrt{32\pi/3}\simeq5.789,
\qquad
a_0=\frac{cH_\Lambda}{Z}
=\frac12c\sqrt{G\rho_\Lambda}
=c^2\sqrt{\frac{\Lambda}{32\pi}}.
\]

Here \(\rho_\Lambda=\Lambda c^2/(8\pi G)\) is mass density and \(H_\Lambda=c\sqrt{\Lambda/3}\). The half is **fitted/adopted, not derived**. The older critical-density version uses \(a_0=cH(z)/Z\); it is not the same evolving physical hypothesis as a constant-\(\Lambda\) version.

The proposed extension

\[
\frac{a_0(z)}{a_0(0)}=
\sqrt{\frac{\rho_{\rm DE}(z)}{\rho_{\rm DE}(0)}}
\]

is a test of this family, conditional on that tracking prescription. Constant \(\Lambda\) gives constant \(a_0\). Substitution into \(v_{\rm flat}^4=GM_ba_0\) fixes a proposed BTFR normalization, not a newly invented BTFR. Planck-mass/seesaw rewritings likewise are not additional laws.

**Potential significance:** a quantitatively fixed connection between galaxy dynamics and cosmic vacuum density, tested independently of its calibration.

**Priority record:** the [17 March root commit](https://github.com/carlzimmerman/zimmerman-formula/commit/84f2393113a087f05abd1bab0200c76384330009) contains the exact denominator with critical density. The [18 March commit](https://github.com/carlzimmerman/zimmerman-formula/commit/0d2f73d060651923779c359a08aac8accda8d606) contains the dark-energy expression as a future floor; [4 June](https://github.com/carlzimmerman/zimmerman-formula/commit/a86de892df44b9be2626b84d1c068b6934fd5e49) adopts dark-energy tracking. Git dates alone do not authenticate first public disclosure. General MOND–cosmology links are older; the prior audit located no authenticated exact fixed-Z counterpart, not proof of universal priority.

## K02 — Central tidal identity and three-frequency test

Define \(H_{ij}=\partial_i\partial_j\Phi_{\rm ph}(0)\), \(D=\operatorname{tr}H\), and \(Q_2=H_\perp-H_\parallel\), relative to the external-field axis. Let \(s_e=y(1-e^{-y})\) be the filtered Newtonian external acceleration divided by \(a_0\), and \(\lambda(y)=1+(y-1)e^{-y}\). Then

\[
\frac{Q_2}{D}=\frac{2y}{5[3\lambda(y)-y]},
\qquad
2y(\omega_r^2-\omega_\phi^2)
=3[5\lambda(y)-y](\omega_\phi^2-\omega_z^2).
\]

**Scope:** spherical perturbing source, isotropic convergent filter, constant nonzero background and linear constitutive response. The frequency form additionally requires a stable harmonic-core circular orbit perpendicular to the external field, with infinitesimal radial/vertical oscillations. At \(D=0\), use the division-free relation in the source report. The frequency equation is an orbital translation, not a second independent discovery.

**Potential significance:** linked tidal/orbital observables whose ratio cannot be independently tuned by source mass or filter amplitude. This is not an established nonlinear Solar-System law.

Sources: [tidal derivation](../qwen_claude_field_theory/closure_2026/filtered_tidal_relation_2026/REPORT.md), [frequency derivation](../qwen_claude_field_theory/closure_2026/two_body_frequency_2026/REPORT.md). These reports identify the known external-field machinery and the narrower central-response corollary.

## K03 — Compact-pair harmonic force and sixth-power crossover

For total mass \(M=m_1+m_2\),

\[
\ddot{\mathbf r}=-\frac{GM}{r^3}\mathbf r-h(M)\mathbf r+\cdots,
\qquad
h(M)\sim\frac29\frac{\sqrt{GMa_0}}{\xi^2},
\qquad
r_{\rm eq}^{6}\sim\frac{81}{4}\frac{GM\xi^4}{a_0}.
\]

**Scope:** isolated Gaussian-filtered compact/deep limit, \(GM/(a_0\xi^2)\to0\), separation small compared with \(\xi\), and fixed positive mass fractions. The crossover follows from balancing the Newtonian and harmonic accelerations. Do not combine this isolated limit with K02's external-field-dominated limit. These leading coefficients are not unique to the exponential interpolation.

**Potential significance:** with one independently fixed universal \(\xi\), a distinctive \(r_{\rm eq}\propto M^{1/6}\) prediction rather than a separately adjusted scale for every system.

Sources: [onset action and asymptote](../qwen_claude_field_theory/closure_2026/smoothed_onset_action_2026/REPORT.md), [both-source force variation](../qwen_claude_field_theory/closure_2026/two_body_frequency_2026/REPORT.md). The crossover is part of this family, not another independent law.

## K04 — Inverse orbital spectrometer and cross-orbit null

For circular frequency \(\Omega\), radial epicyclic frequency \(\kappa_r\), and isolated spherical exact-exponential force law, define

\[
q=\frac{\kappa_r^2}{\Omega^2},\quad
L=\frac{q-1}{3-q},\quad
Y=-L-W_{-1}(-Le^{-L}),\qquad 1<q<2.
\]

Then

\[
a_0=\frac{r\Omega^2}{Y},\qquad
GM=r^3\Omega^2(1-e^{-Y}).
\]

**Potential significance:** infer both constants from orbital clocks, then test them across independent radii/orbits. A single orbit supplies an estimator, not an overconstrained test. The finite-eccentricity extension supplies a branch-conditional cross-orbit null cancelling common mass, distance and absolute clock calibration; full definitions and inverse ambiguities are in the source.

**Status:** conditional exterior mathematics. The original HPI-Delta host is dead as a complete theory; a viable replacement must retain the relevant exterior branch. Existing epicyclic and Lambert-W mechanics are not claimed as original.

Source: [spectrometer, finite-eccentricity null and literature scope](../qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026/REPORT.md).

## K05 — Fixed outer-rotation correction

\[
v^2=\sqrt{GMa_0}+\frac{GM}{4r}
+\frac{7(GM)^{3/2}}{96r^2\sqrt{a_0}}+O(r^{-3}).
\]

**Scope:** isolated point-mass spherical branch, asymptotically deep MOND, with \(\mu(g/a_0)g=GM/r^2\) and \(\mu(y)=1-e^{-y}\). It is not an exact finite-radius fit for an arbitrary extended galaxy.

**Value:** a kernel-discriminating prediction. It is a mathematical consequence of an already-known interpolation function, not an independently new gravity law. Preserve the expansion and observational protocol without claiming invention of its underlying kernel. Here \(G\) is the coupling in the stated weak-static force law, not an independently derived measurement of the covariant theory's Newton constant.

Sources: [exact-exponential prediction ledger](../hunt_2026/EXACT_EXPONENTIAL_PREDICTION_LEDGER_2026-09-03.md), [spherical derivation](../qwen_claude_field_theory/closure_2026/rotated_mmg_constitutive_2026/RMMG_GATE_REPORT.md).

## K06 — Particular four-form/MOND coupling and feedback

In the reduced model's natural-unit convention,

\[
a_0=\beta\sqrt G\,|q_4|,\qquad
P(q_4)=(Z_4/2+b\beta^2)q_4^2,
\qquad
\kappa^2=\frac{2\beta^2}{Z_4+2b\beta^2}.
\]

Notation here deliberately distinguishes four-form flux \(q_4\) from K04's orbital ratio and kinetic coefficient \(Z_4\) from K01's number \(Z\). Define \(\varepsilon_{\rm vac}=q_4P_{q_4}-P\) and \(\kappa^2=a_0^2/(G\varepsilon_{\rm vac})\). The ratio follows from that stated gravitating energy; \(\kappa=1/2\) requires choosing \(Z_4/\beta^2=8-2b\), not a prediction fixing that ratio.

**Value:** preserve the MOND-specific coupling, action and feedback derivation, not ownership of four-form vacuum physics. The shorthand environmental formula with switch-off near \(155a_0\) omits a normalization factor in the current paper and must not be cited as an exact universal law. Its branch boundary and relativistic realization require further work. This is not presently a Kepler-grade empirical prediction.

Sources: [k04 computation](../kappa_closure/k04_four_form_promotion_consistency.py), [Paper 6](../qwen_claude_field_theory/papers_2026/PAPER6_kappa_no_go_2026.tex).

## K07 — Conditional clock-rate inference

\[
Q_0=\frac{g_{\rm tot}-g_N}{cv}.
\]

**Scope:** positive excess acceleration and the particular speed/flow identification in the source paper. Here \(Q_0\) has inverse-length units; \(cQ_0\) is the corresponding temporal rate. Explicit \(a_0\) cancels algebraically, but identifying the scalar force with that flow is an additional physical assumption.

**Value:** preserve the proposed conditional inference, not a claim of a measured universal clock rate. The motivating full-dark-sector embedding was subsequently excluded. Numerical band and \(K''\) conversions need the qualifications identified by the audit; they are not asserted here. This is not presently a Kepler-grade law.

Sources: [Q0 paper](../opus_48_extended_research/papers/PINNING_Q0_IN_AEST.md), [subsequent retractions](../RETRACTIONS.md).

## What a priority record needs

For each family preserve: the exact equation and notation; hypotheses and failure cases; earliest matching public version; derivation/code and reproducible inputs; prior-art distinctions; and a specified observation that could falsify it. A commit records this reference list, not retrospective first-publication proof. No observational confirmation, global novelty, plagiarism finding or complete-theory certification is claimed here. This document compiles existing work; it introduces no new physical derivation or experiment.
