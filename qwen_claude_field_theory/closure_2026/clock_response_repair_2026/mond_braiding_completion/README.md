# Same-action MOND coupling: bracket gate and covariant completion

Base `81ef7508749fe36fcad8882ea494fe567d868e67`, 2026-09-10.
Previous turn: progress (published clock-sector proofs and sourced lapse
solutions). Full objective unchanged and **OPEN**: one derived action must
meet MOND, lensing, gravitational-mode, PPN, conservation, GW, stability,
FLRW/CMB and boundary requirements. This checkpoint does not certify that.

Carl explicitly requires a derived theory, not a phenomenological fit. No
data were fitted here. The new interaction coefficient remains symbolic and
undetermined. Its covariant form is an action hypothesis, not something shown
to be uniquely selected by nature. The earlier reconstructed P/W functions,
the exponential target, and κ=1/2 must not be relabeled first-principles outputs.

## 1. Bare acceleration mixing: actual weak bracket counterexample

Start with the same clock action as `../dirac_operator/README.md`, and try
\(\delta S=\int\sqrt{-g}\,\eta a^\mu D_\mu\chi\), constant η.
In clock gauge its density is \(\eta\sqrt h D_iN D^i\chi\), so integration
by parts adds \(C_b=\partial_i(\eta\sqrt h D^i\chi)\) to the Hamiltonian
constraint. It is lapse-affine; that alone does not preserve the constraint
algebra. η here is a trial mixing coefficient, not κ.

For h=diag(e²ᵃ,e²ᵇ,e²ᶜ), fields depending on x, and
Kₓ=\(\dot a/N\), etc., functional differentiation gives the additional bracket

\[
\{C_\eta[N],C_\eta[L]\}-\{C_0[N],C_0[L]\}
=\int dx\,\eta\sqrt h h^{xx}
[(K_x-K_y-K_z)\chi'-Q'](LN'-NL').
\]

The script checks the discarded boundary term exactly. This is not merely a
nonzero off-shell expression. On a periodic cell choose flat h, spatially
constant χ, Q=q+ε sin(x), pₐ=P₀≠0, and

\[
p_b=p_c=P_0/4+\frac{M^2}{P_0}(\rho_\chi+M^2\Lambda).
\]

Then C=0 and Hᵢ=0 pointwise; η's potential term vanishes. Choose ε small
enough to stay in the original logarithm domain. The usual momentum density
Hₓ=−pₐ′ vanishes. For N=1 and L=sin(x), the extra bracket is
**πηε≠0**. Therefore the previous C self-closure cannot be inherited.
This does not itself count the new theory's modes or exclude other constraints.

## 2. Constructive response: retain the covariant companion terms

Test instead the explicitly specified extension

\[
S_\gamma=S_{\rm clock}+\int d^4x\sqrt{-g}\,\gamma X\Box\chi,
\qquad X=-\nabla_\mu\chi\nabla^\mu\chi,
\]

with constant γ and the same minimally coupled physical matter metric.
This cubic interaction is known kinetic gravity braiding, not claimed new;
see SOURCE.md. We do not transfer its usual one-scalar result to the combined
two-clock system without recalculating constraints.

For Kᵢⱼ=½ℒₙhᵢⱼ, explicit integration gives, modulo boundary terms,

\[
\frac{\mathcal L_\gamma}{N\sqrt h}
=\gamma[-\tfrac23Q^3K+2QK_{ij}\chi^i\chi^j
+2Q^2D^2\chi+\chi^iD_iY].
\]

`derive.py` verifies this against the divergence definition of □χ for an
arbitrary plane metric and scalar, including both boundary currents. There
is no lapse derivative in this representation. The cubic interaction also
changes canonical momenta and the constraint operator: the old lapse
source, background history and ellipticity certificates cannot be reused.

The actual seven-velocity Hessian is differentiated before taking its Schur
complement. With B=2P_X+4Q²P_XX, X=Q²−Y, it gives

\[
\mathcal B=B-4\gamma QK+4\gamma D^2\chi
+\frac{2\gamma^2X(Y+3Q^2)}{M^2}.
\]

The six-metric block determinant is −16(M²)⁶; the full determinant is that
factor times 𝓑. These are computed determinants, not assigned ranks.
Where 𝓑≠0 the velocity map is regular. This is **not** a physical scalar
energy test or a completed Dirac count. Singular branches require separate
analysis. Neither γ nor the coefficient κ=1/2 has been derived.

## 3. Independent weak static equations

For χ=qt+σ and physical potentials Φ,Ψ, the script constructs the spatial
Ricci tensor and independently varies both metric potentials. The retained
quadratic derivative action is

\[
\mathcal L_2=M^2[(\nabla\Psi)^2-2\nabla\Phi\cdot\nabla\Psi]
+2\gamma q^2\nabla\Phi\cdot\nabla\sigma
-C(\nabla\sigma)^2-\rho_b\Phi.
\]

Here C=P_X(q²,τ)−W_Y(0,τ) in the frozen coefficient reduction. Spatial
variation gives ∆(Φ−Ψ)=0: equal potentials follow only with matching
homogeneous/boundary modes. The Φ and σ equations are separate Euler
derivatives. This is a leading-derivative static result, not PPN γ or a
nonlinear MOND solution. Potential-dependent mass terms and time dependence
are not included in this diagnostic.

## 4. Exact two-radius obstruction in the stated reduced action

Do not drop the spatial cubic term when asking for nonlinear phenomenology.
In the local weak-field radial reduction, let u=σ′, g=Φ′, b=2γq², and let
F(Y) be a shared spatial scalar energy function. Up to boundaries its action is

\[
L_r=r^2[-M^2g^2+bgu-F(u^2)]-\frac{4\gamma}{3}ru^3.
\]

On a regular zero scalar-charge branch the actual radial currents give

\[
F_Yu+\frac{2\gamma u^2}{r}=\frac{bg}{2},\qquad
g-\frac{bu}{2M^2}=g_N.
\]

Here g_N=M_b/(8πM²r²) is the bare Einstein-source acceleration, not an
independently measured Newton constant for the full theory.
Imposing the target \(g_N=g(1-e^{-g/a_0})\) requires

\[
u=\frac{2M^2}{b}g e^{-g/a_0},\qquad
F_Y(u^2)=\frac{bg}{2u}-\frac{2\gamma u}{r}.
\]

At fixed finite g>0, compare two different source masses at distinct radii
having that same g_N. They require the same u and F_Y but different 1/r.
Subtracting their equations gives

\[
2\gamma u^2(1/r_1-1/r_2)=0.
\]

Thus nonzero γ,u force r₁=r₂, contradicting the two-source comparison.
`CubicRelations.lean` proves this implication and the metric-flux relation;
both compile without `sorry`. Lean does not prove the approximation from the
full action to this reduced model, nor derive the inserted exponential target.

**Exact scope:** this is a theorem about the displayed radial action with one
source-independent F(Y), constant γ and q, zero radial charge, no time-current
divergence, and only the stated baryonic metric source. The actual clock
P(X,τ) depends on X=q²/N²−Y and carries a nonzero density; replacing it by
F(Y) and omitting that density is an additional approximation, not an identity.
Potential-dependent coefficients, singular weak-field scaling, time-dependent
branches and extra operators are outside the exclusion. It is not a universal
KGB, MOND, or first-principles gravity no-go.

## 5. Review, provenance, and next calculation

Two separately tasked audits checked the prior clock source/ellipticity and
the new ADM/static reduction. The latter independently reproduced the
integration-by-parts signs and radial currents, while emphasizing the scope
conditions above. Independent review is not a substitute for proof.

The clock numerical audit is preserved separately in
`../lapse_residual_audit/`. It finds second-order differential residual
convergence, despite roundoff matrix residuals; neither is promoted to a
continuum certificate. No prior source or evidence was overwritten.

`run_001/checks.json` contains exact argv, cwd, raw output and actual exits:
the new symbolic derivation, two Lean lemmas, original ellipticity regression,
and original sourced-lapse regression all exit 0. The computation manifest
pins inputs and results. Execution success is not theory closure.

Next calculate the **full time-dependent scalar current, metric source and
tertiary constraint of Sγ**, retaining P(X,τ), the reconstructed clock density
and the changed cosmological background. Determine whether those actual terms
can supply the contribution missing from the reduced radial model. Do not
choose a different F for each halo or fit an external force to cancel it.
Only if this same-action gate survives do PPN, CMB/galaxy evolution and a
formal global-constraint proof become justified next steps. The target remains
one derived theory, not a collection of compatible-looking certificates.

No Kepler-grade empirical prediction is claimed. Carl's primordial-clock
direction motivates the retained dynamical clock; the cubic operator's prior
authors receive attribution in SOURCE.md. Mathbox research-program,
computation-audit, proof-audit, and literature-check separated the constructive
action step, exact restricted obstruction, and open physical implications.
