# Dark energy and the smallest missing action bridge

Audit date: 2026-09-26. Starting repository base: `4e16ccf585f6fcc775a2f9d62ac30d329212e0af`, with pre-existing dirty/untracked work. At follow-up completion, HEAD was `03524d209b7ca0c3900f47ccf5dfe42f9187d7c3`; another task advanced the shared checkout, with no merge or commit by this audit. The new computation's manifest pins its actual starting revision. Existing artifacts were read, not edited. This independent subtask inspected the raw H061 source/certificate, the dark-energy synthesis, the k01 summary and k04 source, C-H/K L340/L353/L359, the DE1/DE2 code, and the dark-sector summaries. It did not rerun N-body work or reauthenticate external observational citations. A narrow primary-literature comparison is appended below. `dark_energy_source_provenance.json` records 17 source hashes at completion of the initial inspection; these are documentary hashes, not certification of earlier executions.

**Normalized claim.** A single nonparticle field sector supplies (i) positive constant vacuum stress, (ii) the MOND response with its absolute coefficient, and (iii) the independently clustering cosmological density, and the latest vacuum gate can be embedded in that same action without losing its successful limits.

**Primary verdict: incomplete, with the smallest missing implication being a single varied action connecting those three roles and the gate to the stated initial-value problem.** The exact vacuum equation of state is valid under explicit assumptions. Homogeneity does not force the time-dependent charge sector to its vacuum; the MOND derivative does not fix the additive vacuum constant. Neither failure rules out a nonparticle completion.

## 1. The three quantities must be distinguished before they can be unified

Use signature \((-+++ )\), \(c=1\), a future unit vector \(u^\mu\), and \(h^{\mu\nu}=g^{\mu\nu}+u^\mu u^\nu\). Define

\[
Q=u^\mu\partial_\mu\phi,\qquad
Y=h^{\mu\nu}\partial_\mu\phi\partial_\nu\phi,\qquad
X=-\tfrac12 g^{\mu\nu}\partial_\mu\phi\partial_\nu\phi
=\tfrac12(Q^2-Y).
\]

On homogeneous FRW, \(Y=0\) while \(Q=\dot\phi/N\) is generally nonzero. Homogeneity is not a scalar equation of motion. For a timelike first-derivative scalar with action \(\int\sqrt{-g}\,P(X)\), varying the metric gives

\[
T_{\mu\nu}=P_X\partial_\mu\phi\partial_\nu\phi+Pg_{\mu\nu},
\quad p=P,\quad \rho=2XP_X-P.
\]

Thus \(w=-1\iff XP_X=0\), **provided \(\rho\ne0\)**. The branch \(X=0\) need not be a stationary point of \(P\); the alternate branch is \(P_X=0\). Calling either a stable ground state additionally requires the appropriate perturbative/energy analysis. Positive vacuum energy requires \(P\) negative on that vacuum. A constant term \(P=-V\), \(V>0\), gives \(T_{\mu\nu}=-Vg_{\mu\nu}\), \(\rho+3p=-2V\): this is the precise acceleration mechanism.

H061's introductory \(X\) is a **spatially projected** invariant, but its stress formula is the **timelike k-essence** formula. The supplied Lean theorem correctly proves an algebraic identity for independently supplied real `X`, `fp`, and `f`; it does not derive the stress tensor for the projected action or prove that FRW fixes the scalar's charge. See `hy4_push/H061_where_dark_energy_is.py:57`, `:68`, `:164` and `hy4_push/lean/H061_where_dark_energy_is.lean:61`.

The three relevant data are:

| Role | Quantity | What establishes it |
|---|---|---|
| Vacuum acceleration | Absolute vacuum action value / gravitating stress \(V\) | Metric variation and a positive, conserved vacuum density |
| MOND response | Derivative of a spatial constitutive function and its normalization | Weak-field field equation; this does not determine an additive constant |
| Cosmological clustering | Charge/background amplitude plus perturbation and transport data | Scalar equation, initial conditions, and a viable nonlinear evolution |

These can belong to one field while remaining independent data. “One field” is not “one integration constant.”

## 2. One new exact discriminating check

Rather than fit an expansion history, vary the homogeneous scalar action directly:

\[
L=Na^3K(Q),\quad Q=\dot\phi/N,\quad
K(Q)=-V+\frac A2(Q-Q_0)^2,\quad A>0.
\]

Variation of lapse, scale factor, and scalar respectively gives

\[
\rho=-a^{-3}\frac{\partial L}{\partial N}=QK_Q-K,
\quad p=(3Na^2)^{-1}\frac{\partial L}{\partial a}=K,
\quad I=a^3K_Q=\text{constant}.
\]

Hence

\[
Q=Q_0+\frac{I}{Aa^3},\qquad
\boxed{\rho=V+\frac{Q_0I}{a^3}+\frac{I^2}{2Aa^6}},\qquad
\boxed{p=-V+\frac{I^2}{2Aa^6}}.
\]

The exact continuity identity is \(a\,d\rho/da+3(\rho+p)=0\). At late times and \(Q_0I>0\), the leading excitation is positive dust. At \(I=0\), the same action is exactly vacuum. At \(Q_0=0\), its excitation is stiff, not dust. In particular, H061's implemented offset-DBI center is `Q0=0` (`:192`, `:197`); its local quadratic expansion does not by itself produce a leading dust term. This is not an objection to a different nonzero condensate clock state.

An exact counterexample to “homogeneity forces vacuum” uses \(a=A=Q_0=V=1\). The homogeneous states \(I=0\) and \(I=1\) have respectively \((\rho,p,w)=(1,-1,-1)\) and \((5/2,-1/2,-1/5)\). Both are initial data for the same homogeneous scalar action. Coupling gravity fixes each state's compatible initial expansion through the constraint; no Friedmann constraint selects \(I=0\) without additional initial data. The location of acceleration onset consequently depends on the charge as well as on \(V\): \(\rho+3p=-2V+Q_0I/a^3+2I^2/(Aa^6)\).

This one symbolic run also verifies the coordinate projector distinction and the additive-constant degeneracy directly. All 15 exact residuals vanish. It uses rational symbolic expressions, not numerical sampling; the result applies to the specified quadratic homogeneous family, not every khronon action.

Evidence: `dark_energy_homogeneous_check.py`, `dark_energy_homogeneous_contract.json`, `dark_energy_homogeneous_run/results.json`, and validated `dark_energy_homogeneous_run/manifest.json`. Python 3.9.6; SymPy 1.14.0; runtime 0.843 s; exit 0; 30 s timeout; 20 s CPU cap; thread setting 1 (cooperative). The manifest records input/result hashes, dirty state, and actual command. No numerical-library tolerance or random seed is involved.

## 3. What the previous identities do and do not establish

**Vacuum normalization.** Replacing \(P\) by \(P+C\) leaves \(P_X\), the scalar equation, and the non-gravitational derivative kernel unchanged; it changes \(\rho\mapsto\rho-C\), \(p\mapsto p+C\). Gravity sees the change. Therefore integrating a MOND kernel fixes its primitive only up to precisely the constant that matters for vacuum stress. Choosing `f(0)=-1` normalizes this constant; differentiating `f` cannot derive it. This agrees with the narrower zero-mode obstruction in `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py`.

**H061 A4.** `a0_can` is defined from `rho_L` at lines 132–138; `a0_nat` uses that value at line 210; `Lam_pred` inverts the definition at line 220. Its exact agreement is a unit/convention check, not an independent galaxy-to-vacuum prediction. The negative conclusion is about this implemented test, not about whether an independent galaxy measurement could constrain the relation.

**Offset DBI.** For \(K=-M^4+\mu^2L_D^2[1-\sqrt{1-(Q-Q_0)^2/L_D^2}]\), \(Q_0\) is an analytic stationary minimum. The square-root branch endpoints occur at \(|Q-Q_0|=L_D\), where the derivative is singular; H061's “branch point” explanation at lines 203–204 is incorrect. The vanishing symmetric derivative at the center does not fix the chosen offset \(-M^4\).

**Mode count.** \(\mu_n(Y)=1-(1+Y)^{-n}=nY+O(Y^2)\), so its logarithmic slope tends to 1 for every positive integer \(n\). The Lean file explicitly corrects the earlier Python prose on this point. Identifying \(n\) with two tensor polarizations still requires a microscopic coupling/normalization argument; the polynomial/probability identity supplies none. The family with rescaled argument \(\mu_n(\lambda Y)\) has the same mode count and deep coefficient \(n\lambda\). Setting \(\lambda=1\) by declaration does not derive \(\kappa=1/2\).

**Bookkeeping is not clustering.** A flatness residual supplies a density budget after expansion and other component inputs are specified; it does not determine the charge mode's origin, its transfer function, sound speed, anisotropic stress, or stream crossing. `deepseek_push/WHAT_IS_DARK_ENERGY.md:56` already concedes the coefficient is measured, and `:59` concedes the density consistency exercise is not a cosmology. Its global claims that every relativistic modified-gravity completion is dead and only one parameter is open are incompatible with treating the later C-H/K + switch + carrier construction as the current candidate. Those claims should not be imported as premises.

## 4. The vacuum gate is useful phenomenology with an unvaried bridge

The current construction proposes

\[
U=\widetilde x(\Omega_\Lambda/\Omega_{\Lambda0})^p,
\quad\widetilde x=\frac{9(R^{(3)}+\sigma_{ij}\sigma^{ij})}{4K^2},
\quad\Omega_\Lambda=\frac{3\Lambda}{K^2}.
\]

On the stated FRW background this gives \(x_{c,\mathrm{eff}}=x_{c0}E^{2p}\). The DE1 edge law then follows, within its isolated deep-MOND/step-switch approximation:

\[
r_e\simeq\frac{(GM_ba_0)^{1/4}}{\sqrt{x_{c0}}H_0E^{1+p}},\qquad
y_{\rm edge}\simeq\frac{x_{c0}H_0^2\sqrt{GM_b}}{a_0^{3/2}}E^{2+2p}.
\]

DE1 reports that the previously used \((p,x_{c0})=(2,2)\) fails its canonical \(10^{11}M_\odot,z=2.5\) flagship. This is evidence against that phenomenological cell under its conventions, not against every vacuum-related gate. DE1 imports \(E^2=0.3138(1+z)^3+0.6862\) (`:111`), so this test does not derive a background expansion from C-H/K. DE2's own scope (`:54`) excludes a full projected shear likelihood and a rerun of cluster/clearing/Harvey dynamics at new gate cells. At inspection the DE2 output stopped after mock construction, and its README retained a results placeholder; this audit does not promote its hypothesis to a result.

Being a local scalar is necessary for this proposed gate, but is not its action-level implementation. If a gate factor multiplies a MOND term,

\[
\delta[W(U)\mathcal L_M]
=W(U)\delta\mathcal L_M+\mathcal L_M W'(U)\delta U.
\]

The second term contributes to the clock and metric equations. In a patch holding \(R^{(3)}+\sigma^2\) fixed, \(\partial U/\partial K=-(2+2p)U/K\). The full variation also contains curvature and shear terms. Switching a Poisson force using a prescribed mask does not compute these terms. Checking one volume-preserving TT ansatz is not a full principal-symbol or tensor-action audit in an inhomogeneous transition region. The action must also specify the \(K=0\) limit, where its displayed ratio is undefined; a saturated smooth function can sometimes have a regular limit, so the ratio alone does not establish a pathology.

The latest dark-sector simulations use a posited transport/trigger prescription. L353 supplies an explicit reciprocal subtraction coupling: kernel-invisible carrier feels Newtonian gravity while baryons feel the extra phantom. It does not supply the carrier's covariant internal dynamics or derive its kick. L380's finite PM window, L381's shape-dependent merger test, and L374's finite 1D condensate failure therefore constrain candidate realizations without establishing a unique microscopic field.

## 5. A viable route consistent with no new dark-matter particle species

“No particle species” allows a classical gravitational/clock field to have stress, conserved charge, and independent initial data. It does not allow erasing those data from its equations. A formal `no_particle_source` theorem about a model's source definition proves that definition's consequence; it cannot experimentally exclude particle ontologies. Conversely a simulation's particles may be numerical samples of a classical phase-space distribution and do not themselves assert microscopic particles. What matters is deriving that distribution's evolution from the chosen field.

The narrow route is to keep \(\kappa\) empirical while assembling one action and count every dynamical mode and integration constant explicitly. The same-clock near-condensate branch above is a concrete nonparticle source of dust before caustics, but it is not yet a nonlinear transport completion. L374 tests only its stated truncated equations, initial flow, warmth and dispersion range; its failure does not rule out all regularized same-field theories. A complex wave field can represent multiple streams, but introducing it is additional dynamical field content unless an explicit constraint or derivation identifies it with the original clock's degrees of freedom.

The cleanest existing candidate for tying the *scale* to the vacuum is k04's four-form promotion: \(a_0=\beta\sqrt G|q|\), \(P(q)=Zq^2/2+b\beta^2q^2\), \(\epsilon=qP_q-P\), giving \(\kappa^2=2\beta^2/(Z+2b\beta^2)\). This links the scale amplitudes while leaving a coupling ratio free. It is a different construction from “one scalar zero-gradient vacuum,” with a flux datum and no four-form local propagating mode in the isolated four-form sector. Once the MOND term depends on \(q\), the conserved object is the full \(\partial\mathcal L/\partial q\), not necessarily spatially constant \(q\); k04's environmental feedback is therefore part of the proposal. The exact vacuum constancy must not be exported unqualified into coupled environments. This audit credits the displayed algebra, not k04's full numerical/stability claims or external-source authentication.

**Cheapest next deciding calculation:** specify one smooth action for the gate and carrier, vary it before numerical evolution, and determine its constraints/principal symbol on a homogeneous state and one transition patch. Demand (a) the wanted vacuum/dust split, (b) the MOND static equation including gate variations, (c) reciprocal baryon/carrier forces, and (d) a nonsingular counted evolution through the gate. A failure identifies a concrete operator to change. A pass justifies rerunning the established phenomenological gates with that action's actual equations. Another density-coincidence calculation or larger simulation with the old prescribed mask does not decide this bridge.

## 6. Obligation matrix and evidence boundary

| Obligation | Result |
|---|---|
| Constant positive vacuum has \(w=-1\) and negative active gravitational density | Passed under the stated stress/conservation assumptions |
| FRW homogeneity forces the scalar/clock sector to vacuum | Failed; exact homogeneous counterexample above |
| MOND derivative alone fixes the absolute vacuum energy or \(\kappa\) | Failed in the additive-constant action class |
| One nonparticle field can possess a dust-like charge branch | Passed for the stated quadratic homogeneous sector, leading \(a^{-3}\) term |
| Its amplitude is fixed by the vacuum state | Failed without additional initial-condition/constraint input |
| The latest phenomenological gate is realized by one healthy varied action | Not addressed by the inspected simulations; exact missing bridge |
| Existing finite carrier and shell-crossing checks establish a universal no-go or a complete cosmology | Not established; their scopes are finite and model-specific |
| Full observational likelihood without imported reference transfer/background | Not run by this audit |

The new computation's interpretation is **implementation and exact assertion verified for the declared quadratic homogeneous sector**. The broader claim remains incomplete. No Lambda-CDM abundance, expansion history, matter particle, or empirical likelihood was assumed in the new check.

## 7. Primary-literature overlap check

Checked 2026-09-26: Luc Blanchet and Constantinos Skordis, *Relativistic Khronon Theory in agreement with Modified Newtonian Dynamics and Large-Scale Cosmology*, [arXiv:2404.06584v2](https://arxiv.org/html/2404.06584v2), dated 27 November 2024. Versioned arXiv HTML authenticated the source; equations (47), (52)–(54) explicitly give the conserved initial-condition amplitude and quadratic homogeneous solution. No full-paper or observational validation is asserted.

Translation: after stripping the common action-density prefactor, set \(A=2\mu^2\), \(Q_0=1\), \(V=0\), \(I=I_0\), and our \(Q=\overline{\mathcal Q}\). Equation (53) is our charge solution; (54) is our dust-plus-stiff density divided by \(8\pi G\) in \(c=1\) units, matching the paper's action normalization (6). The constant offset \(V\) in our audit is an independently explicit extension; it does not alter the charge equation. **Classification: known after translation of notation**, independently rederived here to discriminate repository claims. Search scope was this named primary source and the existing local comparison note, not a novelty survey. The source was inspected online; no local source copy/hash is claimed.
