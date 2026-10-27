# Bounded relativistic-MOND literature overlap audit

Audit prepared 2026-09-09. Requested recent window: 2026-03-09 through 2026-09-09. This is a source/priority comparison, not an independent proof audit of every theory. First public preprint, later revision, and journal publication are distinguished. Local file dates are not themselves proof of public disclosure.

## Finding

No documented evidence of copying from Zimmerman was found in this bounded search. Several close architectural ingredients substantially predate the requested window. The most exact recent match—the Laplacian multiplier construction of Sangtawee, De Felice, and Karwan—is explicitly identified and adopted as an external mechanism in the repository. Other similarities concern established research programs or different equations. This does **not** prove that copying never happened, establish worldwide novelty, or substitute for comparing publicly archived versions of each Zimmerman claim.

## Recent candidates and date traps

### 1. Sangtawee–De Felice–Karwan: exact shared mechanism, acknowledged source

Jakkrit Sangtawee, Antonio De Felice, Khamphee Karwan, *Minimally modified gravity with Laplacian auxiliary constraints and an inflationary realization*. [arXiv metadata](https://arxiv.org/abs/2607.26031), [v1 full text](https://arxiv.org/html/2607.26031v1), [PDF](https://arxiv.org/pdf/2607.26031v1). First submitted **2026-07-28 17:41:47 UTC**, v1.

Equations (37)–(38) replace an auxiliary multiplier coupling by

\[
\sqrt\gamma(D^2\mu_I)[Q^I-P^I(N)],\qquad D^2[Q^I-P^I(N)]=0.
\]

With appropriate boundary conditions, nonzero spatial modes retain the original constraints; homogeneous multipliers disappear. Their mixed curvature–momentum invariants differ from the repository's MOND elliptic constraint. Generic rank statements require nondegeneracy and exclude the homogeneous/harmonic sector. Tensor propagation can contain a fourth-order spatial term; this is not automatically a luminal MOND completion. No MOND construction or Zimmerman reference was found in the inspected text/bibliography. The authors cite their earlier auxiliary-constraint literature, including [2020](https://arxiv.org/abs/2011.00805) and [2023](https://arxiv.org/abs/2302.02090) papers.

**Comparison:** the repository's `qwen_claude_field_theory/closure_2026/rotated_mmg_constitutive_2026/RMMG_GATE_REPORT.md` expressly says it applies this recent paper's mechanism. Its nonzero-mode Dirac block acquires momentum factors while the zero mode vanishes. Classification: **known mechanism after notation translation; adjacent, not identical, total theory**. This is evidence of an acknowledged source feeding into the repository, not evidence that the source copied the repository.

### 2. Yu–Hu–Gao: recent perturbative two-DOF construction

Yang Yu, Yu-Min Hu, Xian Gao, *Spatially covariant gravity with two degrees of freedom: A perturbative analysis up to cubic order*. [Metadata](https://arxiv.org/abs/2604.14490), [v1 text](https://arxiv.org/html/2604.14490v1). First submitted **2026-04-16 00:00:07 UTC**.

The paper studies polynomial spatially covariant actions with up to three derivatives, eliminating scalar propagation through cubic cosmological perturbations and obtaining five explicit Lagrangians. The stated perturbative result is not a general nonlinear Hamiltonian proof for an arbitrary MOND action. Searches within the primary text found neither “MOND” nor “Zimmerman.” Abstract, introductory scope, and selected technical sections were inspected; the entire derivation was not independently checked.

**Comparison:** already referenced in the repository's MMG/scalar-constraint investigations. Classification: **partial/adjacent prior construction**, not an exact match to the repository's interpolation function, source equation, or completed theory.

### 3. Bojowald–Duque: MOND paper is from 2023

Martin Bojowald, Erick I. Duque, *MONDified Gravity*. [Metadata](https://arxiv.org/abs/2310.19894), [primary PDF](https://arxiv.org/pdf/2310.19894), [journal](https://doi.org/10.1016/j.physletb.2023.138279). First submitted **2023-10-30 18:03:35 UTC**; Physics Letters B 847 (2023), 138279.

This is a spherically symmetric canonical emergent-metric construction without extra fields, not a completed arbitrary-background three-dimensional MOND theory. Equation (15) uses

\[
c_f(E^x)=1+\frac{\bar\lambda^2}{2}\left[\Lambda E^x-\log(E^x/c_0)\right].
\]

Their leading circular-speed condition is \(v_0^2=\bar\lambda^2(\mu^2\lambda_0^2-1)/2\); BTFR matching fixes a mass-dependent parameter combination. Here \(\mu\) is a lapse function, **not** the MOND interpolation function. The quoted acceleration coincidence is \(a_0\approx\sqrt{\Lambda/3}/(2\pi)\) in their units, not Zimmerman's half coefficient. The full 11-page PDF and bibliography were read; no Zimmerman citation was found.

**Comparison:** **partial/adjacent older prior art**. “No extra fields” alone does not establish identical constraints, observable predictions, or action.

Bojowald, Manuel Díaz, and Duque's *Perturbative emergent modified gravity on cosmological backgrounds: Kinematics* was first submitted **2025-07-18 20:42:29 UTC**, [arXiv:2507.14358](https://arxiv.org/abs/2507.14358). Its [Physical Review D publication](https://journals.aps.org/prd/abstract/10.1103/jwr9-48vn) is dated **2026-04-28**. Thus it is a recent journal appearance, not a newly disclosed idea within the requested window. Metadata and abstract were checked, not the full 90-page derivation. It extends cosmological perturbative kinematics and explicitly precedes the corresponding dynamical development.

### 4. Deffayet–Woodard: 2026 revision of a December 2025 proposal

Cédric Deffayet, R. P. Woodard, *A Nonlocal Realization of MOND that Interpolates from Cosmology to Gravitationally Bound Systems*. [Metadata](https://arxiv.org/abs/2512.10513), [v1](https://arxiv.org/html/2512.10513v1), [v2](https://arxiv.org/html/2512.10513v2), [journal](https://doi.org/10.1088/1475-7516/2026/04/081). First submitted **2025-12-11 10:34:29 UTC**; v2 **2026-04-30 17:01:54 UTC**. JCAP 04 (2026), 081.

Their invariant \(Z\) uses the gradient of \(\Box^{-1}(R_{\mu\nu}u^\mu u^\nu)\), fixed initial data, and

\[
f(Z)=\tfrac12Z e^{-\sqrt{|Z|}/3},\qquad
\partial_\mu(\sqrt{-g}u^\mu\mathcal M)
=-\partial_\mu(\sqrt{-g}u^\mu f(Z)).
\]

Their cosmological normalization is \(\rho_0=45a_0^2/(16\pi G)\). This is not a derivation of Zimmerman's \(a_0\)-vacuum coefficient. In the static limit \(Z=4(g/a_0)^2\), so their exponential is not the repository's \(\mu(y)=1-e^{-y}\). Transition dynamics and nonlinear structure tests remain follow-up problems in the paper. Primary main-text sections were read; no “Zimmerman” match was found in either version.

**Comparison:** **existing nonlocal source architecture with different constitutive law**. The repository's `NONLOCAL_MOND_PRIMARY_SOURCE_AUDIT_2026-09-01.md` explicitly audits this paper and does not claim its architecture as Zimmerman's invention. Earlier sufficient-lensing nonlocal MOND is [arXiv:1106.4984](https://arxiv.org/abs/1106.4984), June 2011.

### 5. Gabriel King: recent auxiliary-tensor candidate, PDF unavailable

Gabriel King, *Auxiliary-Tensor Derivation of Deep-MOND/AQUAL Cubic Scalar Response*, [Zenodo 20321267](https://zenodo.org/records/20321267), v1, **2026-05-21**. Primary record metadata was accessible; linked PDF retrieval failed, so no full-text or citation finding is claimed.

The record describes an algebraic tensor \(h_{ij}\), a coupling to \(\partial_i\Phi\partial_j\Phi\), and potential proportional to \((h_{ij}h^{ij})^n\). Eliminating it gives gradient power \(p=4n/(2n-1)\), with \(p=3\) at \(n=3/2\). The record does not present this as a complete relativistic/cosmological theory.

**Comparison:** **partial/adjacent at authenticated metadata level; exact overlap unverified**. The repository's scalar Legendre auxiliary \(\chi|\nabla\Phi|^2+V(\chi)\), with \(\chi=\mu(g/a_0)\), differs in field content and constitutive detail. General auxiliary elimination is insufficient evidence of copying. A full PDF comparison remains open.

## Older architectural precedents

### AeST and cosmological dust

Constantinos Skordis, Tom Zlosnik, *A new relativistic theory for Modified Newtonian Dynamics*, [arXiv:2007.00082](https://arxiv.org/abs/2007.00082), [v3 PDF](https://arxiv.org/pdf/2007.00082v3). First submitted **2020-06-30 19:50:52 UTC**; PRL 127, 161302 (2021).

Equation (5) contains a unit timelike vector, scalar, \(Q=A^\mu\nabla_\mu\phi\), projected spatial kinetic scalar \(Y\), a function \(\mathcal F(Y,Q)\), and vector–scalar coupling. In homogeneous cosmology, \(\mathcal K(Q)=-2\Lambda+\mathcal K_2(Q-Q_0)^2+\cdots\), with conserved charge \(\mathcal K_Q=I_0/a^3\), supplies a dust-like component. Its amount is integration data; \(\Lambda\) is freely specified. Action and cosmological/weak-field sections were inspected.

**Comparison:** clock/projected-gradient decomposition and charge-supported cosmological dust are **older partial/adjacent ingredients**, not new merely because a later construction employs them. This action is not the repository's specific two-scalar \(F(Q)\Theta\) model.

### Khronometric MOND and nondynamical-scalar gravity

Luc Blanchet, Constantinos Skordis, *Relativistic Khronon Theory in agreement with Modified Newtonian Dynamics and Large-Scale Cosmology*, [arXiv:2404.06584](https://arxiv.org/abs/2404.06584), [v1 PDF](https://arxiv.org/pdf/2404.06584v1). First submitted **2024-04-09 19:26:19 UTC**.

Its action (2.6) has \(R-2\mathcal J(Y)+2\mathcal K(Q)\), with clock-defined unit normal and acceleration invariant \(Y=A_\mu A^\mu/c^4\). A simple choice is \(\mathcal K(Q)=\mu^2(Q-1)^2\). Minkowski perturbations contain two tensor modes and a zero-frequency scalar; this is not a two-total-DOF result. Selected definitions, action, and perturbation sections were inspected. Classification: **older partial/adjacent**.

Other identifiable antecedents include [khronometric MOND, 2012](https://arxiv.org/abs/1205.0400), [Flanagan's 2023 analysis](https://arxiv.org/abs/2302.14846), [cuscuton, 2006](https://arxiv.org/abs/hep-th/0609150), and [extended cuscuton, first submitted 2018-09-28](https://arxiv.org/abs/1809.10935). These establish older research on preferred clocks and removing scalar propagation; they do not prove equivalence to the repository's action. Domènech–Ganz's [MOND/mimetic connection](https://arxiv.org/abs/2503.11174) first appeared **2025-03-14**, not March 2026. These bridge sources received selected-section or abstract inspection only.

### Four-form vacuum energy

F. R. Klinkhamer, G. E. Volovik, *Dynamic vacuum variable and equilibrium approach in cosmology*, [arXiv:0806.2805](https://arxiv.org/abs/0806.2805), [primary PDF](https://arxiv.org/pdf/0806.2805). First submitted **2008-06-17 17:42:56 UTC**.

A conserved vacuum variable can be realized by a four-form \(F_{\mu\nu\rho\sigma}=q\sqrt{-g}\,e_{\mu\nu\rho\sigma}\). Its gravitating vacuum density has the thermodynamic form \(\epsilon-q\epsilon_q\). Under the repository's convention \(P=-\epsilon\), this is \(qP_q-P\): **known after notation translation**. Introduction and defining action were inspected. The checked source did not supply the repository's MOND coupling \(a_0=\beta\sqrt G|q|\) or fix its half coefficient.

The repository's quadratic choice \(P=Zq^2/2\) leaves a coupling ratio in its coefficient. Four-form vacuum energy and the MOND-specific coupling should therefore be treated as separate priority claims, with the latter still requiring its own public-version comparison.

### Memory and modified inertia

Mordehai Milgrom, *Models of modified-inertia formulation of MOND*, [arXiv:2208.07073](https://arxiv.org/abs/2208.07073), first submitted **2022-08-15 08:41:56 UTC**. The primary abstract explicitly discusses time-nonlocal dynamics and an external-field response involving orbital-average external acceleration and a frequency-dependent factor, unlike a purely instantaneous external-field law. [*MOND as manifestation of modified inertia*](https://arxiv.org/abs/2310.14334), first submitted **2023-10-22 15:41:51 UTC**, continues this program. Abstract-level inspection only; no entire-kernel equivalence is claimed.

**Comparison:** memory/history dependence in MOND is **older partial/adjacent prior art**. A specific repository memory kernel, coherence invariant, relaxation law, or prediction could still differ.

Discovery-only recent lead: Ralf Krimke's *Ab Initio Derivation of MOND and Dark Matter Profiles: Causal Decoherence and Visco-Elastic Wakes in the KEFE Framework*, linked to [Zenodo 20254927](https://zenodo.org/records/20254927) and [20578743](https://zenodo.org/records/20578743), advertised as May/June 2026. Search/author-upload descriptions mention hydrodynamic memory, simple interpolation, and \(a_0=cH_0\). Primary record/PDF retrieval did not succeed. **Unverified lead, not evidence of an exact match or copying**; historical dates and equations require authentication before use.

## Repository comparison cautions

The inspected `fqtheta_clock_dust_2026/REPORT.md` records the specific action with \(-K(Q)+F(Q)\Theta+M^2a_0^2G(|V|/a_0)\), \(G(y)=y^2+2(1+y)e^{-y}-2\), and its own restricted degeneracy conditions. Its corrected local analysis leaves a scalar mode on the tested nonzero-wave-number branch. Its homogeneous charge has both dust-like and stiff contributions. It must not be represented as an already-established globally healthy two-DOF theory when comparing priority.

Likewise, the inspected August MMG paper retracts an earlier conditional-closure interpretation and records failed phenomenological/constraint checks. Priority in proposing an ansatz, obtaining a restricted calculation, and proving a complete viable theory are different claims. This report assesses structural overlap only; it does not upgrade those results.

## Search record and limitations

Searches used general web discovery, arXiv primary metadata/HTML/PDF, publisher metadata, Zenodo records, and local repository citations. Selected literal queries:

- `Bojowald Duque emergent MOND 2026 arxiv`
- `MOND "two degrees of freedom" 2026`
- `relativistic MOND 2026` with arXiv domain restriction
- `"MOND" "2026" "khronometric"`, `"MOND" "2026" "cuscuton"`
- `"MOND" "F(Q)" "Theta"`, `"F(Q)" "braiding" gravity`
- `"MOND" "Laplacian" 2026`, `"Auxiliary-Tensor Derivation" King`
- `"MOND" "four-form" 2026`, `"MOND" "vacuum" "flux" 2026`
- `MOND q theory vacuum energy Klinkhamer Volovik`
- `"MOND" "2026" "memory"`, `"MOND" "2026" "coherence"`
- `"MOND" "Helmholtz" "coherence" 2026`
- `"MOND" "Zimmerman" 2026 Sangtawee Bojowald`
- `Deffayet Woodard MOND 2026`, `"20254927" "Krimke"`, `"20578743" "Krimke"`

Backward tracing followed Sangtawee's 2020/2023 auxiliary-constraint references; Bojowald's 2023–2025 sequence; the nonlocal 2011–2025 program; AeST, khronometric, cuscuton, and four-form antecedents. Forward tracing distinguished 2026 revisions/publications from earlier first submissions.

Coverage is predominantly English-language gravity/astrophysics preprints and the closest discovered alternatives, not an exhaustive ADS/INSPIRE/Google Scholar citation census. No comprehensive text-similarity corpus or access-history investigation was performed. A failed search or missing name is not proof of independence, novelty, or misconduct. No source PDFs were retained locally and no extraction hashes were produced. Accessible primary sections and metadata were read through the browser tools; unavailable full-text candidates remain explicitly unverified. No global novelty assertion is made for the repository's exact \(F(Q)\Theta\) coefficients, memory kernel, or four-form/MOND coupling.
