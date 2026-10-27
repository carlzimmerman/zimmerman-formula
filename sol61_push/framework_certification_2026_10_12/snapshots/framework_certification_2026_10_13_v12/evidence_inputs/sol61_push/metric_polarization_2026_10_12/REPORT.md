# Gravitational polarization after Claude's latest stress and lensing results

Continuation: [the adaptive reference-field calculation](REFERENCE_FIELD_RESULT.md) constructs and tests uniform-field cancellation, then derives its outer-tail and mass-scaling costs. The original result below is retained as the starting checkpoint.

12 October 2026. **A new connection within the inspected project work, not a discovery of established new physics.** A polarization field can source the Newtonian gravitational potential while retaining a convex energy after the gravitational constraint is eliminated, for fixed matter sources. This supplies a concrete intermediate construction between the separate stable scalar response and the metric response Claude needs. It does **not** establish relativistic lensing, stability with moving matter, absence of an external-field effect, or the origin of the acceleration scale.

The most useful outcome is a sharper research target: construct a covariant, stable response that retains information about a bound system. Merely making a polarization field gravitate does not provide that information. The simple construction below has an external-field effect and therefore does not close the project's mechanism.

## The work inspected

Starting checkpoint: `56c94a40d`; calculation checkpoint: `bfe743d37d0940e968f6de4dc612129fa906aea9`. The shared checkout is dirty and other chats are working concurrently. This note and its checks occupy a new directory and do not modify Claude's lanes or simulations.

The principal inputs are `campaign_fresh_gravity/MECHANISM_JOINT_2026-10-12.md`, CFG660, CFG661, CFG663, CFG665, CFG647, the assessment updated through CFG644/646/649, and `sol61_push/cold_production_2026_10_11/mechanism_2026_10_12/STABLE_SOURCED_RESPONSE.md`. CFG666 criteria appeared during this investigation; no result from that pending lane is assumed.

Claude's current results distinguish three problems. The prescribed spherical stress reproduces the law but fails as an independent fluid dynamics; the separate scalar response is stable with fixed sources but lacks a demonstrated lensing coupling; and candidate B's settling prescription overshoots the native shear test **conditional on its inherited initial conditions and background**. These are different failures. No result here reverses the shear verdict or reproduces its data analysis.

## 1 A quantitative check on the field energy shortcut

The existing scalar construction has

\[
 e={D^2\over2a}+{\beta p^3\over3}
       +{\gamma\over2}\left[(p')^2+{2p^2\over r^2}\right],
 \quad D={\alpha M\over4\pi r^2},
 \quad p={B\over r}-{\gamma\over\beta r^2}+O(r^{-3}),
 \quad B^2={\alpha M\over4\pi a\beta}.
\]

For a compact spherical source, write the scalar's asymptotic acceleration as \(V^2/r\), where \(V^2=\alpha B/a\). Substitution gives the normalization-independent leading term

\[
 e={M V^2\over12\pi r^3}
    +{1\over r^4}\left({G_s M^2\over8\pi}+{\gamma B^2\over2}\right)
    +O(r^{-5}),\qquad G_s={\alpha^2\over4\pi a}.
\]

The positive gradient term alone contributes \(3\gamma B^2/(2r^4)\); the change in the cubic term subtracts \(\gamma B^2/r^4\). Both must be included. A noncompact baryon tail can change subleading terms; the displayed coefficient assumes the compact-source exterior.

By comparison, an ordinary spherical mass distribution producing acceleration \(V^2/r\) needs

\[
 \rho_{\rm req}={V^2\over4\pi G r^2},\qquad
 {e_{\rm leading}/c^2\over\rho_{\rm req}}={GM\over3c^2r}.
\]

For an illustrative baryonic mass \(10^{11}M_\odot\), this ratio is \(5.32\times10^{-8}\) at 30 kpc and \(1.60\times10^{-8}\) at 100 kpc. The tail's integrated energy grows logarithmically, whereas the required halo mass grows linearly. Rescaling \(\alpha,a,\beta\) while preserving the force amplitude cannot change this leading coefficient.

**Scope:** this rules out identifying the existing static energy density divided by \(c^2\) with the required ordinary halo density in the asymptotic regime. It is not a complete relativistic lensing no-go: pressure, constraints, time-dependent backgrounds and nonminimal couplings require a covariant action. The joint synthesis already notes that field stress is too small; the explicit coefficient and tail calculation sharpen that existing point.

## 2 Put the polarization in the gravitational constraint

Let \(\mathbf g=\nabla\Phi\), so physical acceleration is \(-\mathbf g\), and let \(\mathbf Q\) be an outward polarization with units of mass per area. On a fixed Newtonian background take the exploratory Lagrangian density

\[
 \mathcal L={I\over2}|\dot{\mathbf Q}|^2
 -{ |\nabla\Phi|^2\over8\pi G}-\rho_b\Phi
 +\mathbf Q\cdot\nabla\Phi-U(|\mathbf Q|)
 -{\gamma\over2}|\nabla\mathbf Q|^2,
\]
\[
 U(q)=2\pi Gq^2+{b\over3}q^3,\qquad I,b,\gamma>0.
\]

Here \(\rho_b\) is fixed externally; the model has no advected cold mass. The kinetic term is a new assumption, not derived from the project's carrier. Variation gives

\[
 \nabla^2\Phi=4\pi G(\rho_b+\nabla\cdot\mathbf Q),
 \qquad I\ddot{\mathbf Q}
 =\nabla\Phi-4\pi G\mathbf Q-b|\mathbf Q|\mathbf Q
       +\gamma\nabla^2\mathbf Q.
\]

Thus the response changes the gravitational potential itself. It is not an extra scalar force appended to the matter equation while leaving that potential unmodified. This remains Newtonian: there is only one potential here, not a verified pair of relativistic lensing potentials.

### Constraint reduction and stability

Use a periodic domain with the mean density subtracted in Poisson's equation, or boundary conditions supporting the orthogonal Helmholtz decomposition without surface contributions. Write \(\mathbf Q=\mathbf Q_L+\mathbf Q_T\), with \(\mathbf Q_L\) longitudinal, and fix the mean gravitational field. Then

\[
 \nabla\Phi=\mathbf g_N+4\pi G\mathbf Q_L.
\]

After solving the instantaneous gravitational constraint, the Hamiltonian, up to a source-only constant, is

\[
 H_{\rm red}=\int\!d^3x\left[
 {I\over2}|\dot{\mathbf Q}|^2+2\pi G|\mathbf Q_T|^2
 +{b\over3}|\mathbf Q|^3+{\gamma\over2}|\nabla\mathbf Q|^2
 -\mathbf Q\cdot\mathbf g_N\right].
\]

The crucial sign check is that the gravitational contribution is **negative**, \(-|\nabla\Phi|^2/(8\pi G)\), in the constrained energy. It cancels the longitudinal quadratic part of \(U\), leaving a positive transverse term. Replacing gravity by a positive square without performing this reduction would not prove this result.

For fixed sources the last term has zero second variation. At a stationary field with \(q=|\mathbf Q|\), the second variation is

\[
 \delta^2 H_{\rm red}=\int\!d^3x\left[
 I|\delta\dot{\mathbf Q}|^2+4\pi G|\delta\mathbf Q_T|^2
 +bq|\delta\mathbf Q|^2
 +{b\over q}(\mathbf Q\cdot\delta\mathbf Q)^2
 +\gamma|\nabla\delta\mathbf Q|^2\right]\ge0.
\]

The cubic Hessian is zero at \(q=0\), by continuity. Convexity establishes an energy minimum whenever a stationary solution with the specified boundary data exists. With positive inertia, no negative stiffness mode of this reduced fixed-source problem produces exponential growth. A zero homogeneous mode is not a spectral gap; damping, attraction, global PDE existence and live-matter stability are not proved. A homogeneous background used in the Fourier checks is a local Hessian diagnostic, not a periodic sourced equilibrium.

### The force follows from the stationary equation

For spherical \(\mathbf Q=q(r)\hat r\), the equations reduce to

\[
 -\gamma\left(q''+{2q'\over r}-{2q\over r^2}\right)+bq^2=g_N,
 \qquad g=g_N+4\pi Gq.
\]

This is the same radial boundary-value equation as the earlier stable scalar construction after rescaling its source and coefficients. The earlier finite-stiffness solutions are consequently relevant mathematical evidence, but were not rerun or relabelled as relativistic evidence here. When \(\gamma=0\),

\[
 g=g_N+4\pi G\sqrt{g_N/b}.
\]

Choosing \(b=16\pi^2G^2/a_0\) yields \(g=g_N+\sqrt{a_0g_N}\) and \(V_\infty^4=GMa_0\). This is an imposed coefficient and a deep-regime construction. It is not the project's full interpolation kernel, a Solar-System-safe law, or a derivation of \(a_0\).

## 3 The next obstruction is visible already

This construction does **not** give environment-independent bound systems. In a locally uniform polarization background \(q_e\hat n\), consider a longitudinal perturbation of wavenumber \(k\). Along and perpendicular to \(\hat n\), respectively,

\[
 {\delta g\over\delta g_N}
 =1+{4\pi G\over 2bq_e+\gamma k^2},
 \qquad
 {\delta g\over\delta g_N}
 =1+{4\pi G\over bq_e+\gamma k^2}.
\]

These follow directly from the reduced Hessian. The internal response depends on the external background and is anisotropic: an external-field effect. Stiffness does not remove this dependence. This candidate therefore fails to supply the joint synthesis's required EFE-blind behavior. That is an algebraic property of this model; no new satellite-data exclusion has been performed.

There are four further unresolved requirements:

1. A covariant completion must derive both metric potentials, their lensing combination, and all physical kinetic modes. A possible operator to investigate is a clock-acceleration coupling to a spacelike polarization. Merely writing this operator does not fix its lapse, shift, clock and tensor constraints.
2. Photons and tensor waves must follow the same characteristic cone in the actual inhomogeneous solution. A shared metric symbol alone does not establish this.
3. Universally coupled extra cold matter also sources \(\Phi\). The response then sees it as well as baryons. The construction does not prevent double counting or establish the required cosmological abundance.
4. The exact quadratic coefficient is critical tuning. Reducing it makes the longitudinal vacuum energy negative at sufficiently long wavelength; increasing it makes the sufficiently weak response linear instead of square-root. No symmetry protecting this tuning or tying the vacuum offset to \(a_0\) has been found.

## Prior art and the meaning of novelty

[Blanchet and Le Tiec, arXiv:0804.3518v2](https://arxiv.org/pdf/0804.3518v2), equations 4.15 and 4.22, already give precisely the quadratic and cubic coefficients used above. With our outward \(\mathbf Q\) opposite their inward polarization, their effective density has the same sign. **The static constitutive law is known after notation translation.** Their dynamical dipolar medium is not the independent positive-inertia field assumed here, so neither its stability nor its instability transfers automatically. The contribution here is the explicit constrained fixed-source energy check for this chosen kinetic replacement and its connection to today's project fork.

[Skordis and Zlosnik, arXiv:1905.09465v1](https://arxiv.org/pdf/1905.09465), equations 13 and 18, exhibit a modified-gravity class whose tensor waves and photons share propagation speed and Shapiro delay. This limits the interpretation of CFG665: its photon-only cone-tilt exclusion does not by itself prove that ordinary cold mass is the only possibility. The cited class is not a completion of the present model, and it does not remove the project's separate EFE objections.

[Bekenstein and Sanders, astro-ph/9311062v1](https://arxiv.org/pdf/astro-ph/9311062), sections 2–5, provide older scalar-tensor lensing obstructions. Their hypotheses are not transferred as a theorem to this vector/clock proposal; the relevant lesson is to compute stress and the physical metric together.

Search boundary: primary arXiv/APS discovery using scalar-field energy and lensing, gravitational polarization and critical potential, and polarization Hamiltonian/longitudinal/transverse convexity; project searches in `sol61_push`, the recent CFG660–669 files and the joint synthesis. Full primary passages of the three sources above were inspected via the web tool, not cached. This is a bounded same-author literature check, not a systematic novelty review. No claim of a previously unknown theory is made.

## Verification and research decision

The computation contract preceded the run. `check.py` verifies five exact symbolic identities, a periodic 9-cubed Helmholtz energy reduction, orthogonality, 140 finite Hessian matrices, and two sign/tuning controls. All ten grouped checks pass. The raw/reduced energy discrepancy is \(3.55\times10^{-15}\). The manifest validates input/output hashes and execution provenance. These finite checks support the displayed derivation; they do not certify a covariant theory.

Self-audit verdict: **correct only after a stated restriction** — fixed external sources, specified Helmholtz boundary conditions, instantaneous Newtonian gravity, and assumed positive polarization inertia. Lensing, tensor characteristics and evolving matter remain unverified. No independent reviewer was used. Mathematical proofreading found no remaining local notation errors in this report.

Executed routes: ordinary field-energy identification fails asymptotically; direct gravitational polarization passes the reduced fixed-source energy test; its external-field response fails the desired environment independence. None is a complete mechanism. The existing conditional shear exclusion remains in force.

**Next discriminating work:** a covariant response with a dynamical variable that retains a bound system's history, tested first on the complete constrained quadratic action and a satellite in an external field. It must explain how that variable is formed and transported rather than assign each galaxy a label. The present calculation supplies a controlled reference model and an explicit external-field failure against which such a proposal can be tested. This next route is open and deferred; no qualifying action has yet been constructed. Repeating a large settling simulation does not answer this structural question.
