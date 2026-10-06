# Independent finite-EdS raw-equation and transfer audit

**Primary verdict: proved as written.** The exact seven-state constrained linear Fourier system, six physical scalar initial data at k≠0, trace/curvature closure and constraint propagation follow from the declared finite-ξ action. The numerical transfer values are independently checked as bounded solver evidence, not an interval-certified solution or a universal initial-data conclusion. The report correctly distinguishes altered ordinary-dust growth from the much smaller residual lensing response.

Frozen pins: REPORT.md `4c95a34f6a35510ce2b20d5738624afe4ad52f00f30799fbca49c7c63479f0b6`; equations.py `888cca2f72e220203b45a64c9d4e61d7706bf0e60df213b3e32ad34848ddc04a`; checks.py `41b00e76039041be4b7fda0d5a5404ca601ece253e52b4f19902d2a22e18f480`; transfer.py `6875be6a0a2f4a408fb79796bc746865bf7bb0c10e27b8e961956edb208f4e90`. Only this review was written. Raw parent action/background and the author's frozen report/scripts were read. A fresh symbolic reconstruction was executed inline without importing the author equations/checks.

## Claim and dependency graph

Finite two-real-scalar action + exact circular EdS background → metric Hamiltonian/momentum/anisotropic-stress equations and scalar/dust conservation → trace elimination → geometric closure and constraint transport → six-data transfer → two distinct GR source diagnostics. Domain: four spacetime dimensions, ξ>3/16, A>0, M>0, finite interval with F>0, k≠0. The limit ξ→∞ is not taken. Numerical tests cover only ξ=100,1000, S_i=.4M, t_i=M=1, zero initial relative carrier modes, and t/t_i in[1,100].

## Raw action reconstruction

Start from F=M−ξΣϕ² and

F Gμν=T_dμν+T_canμν+∇μ∇νF−gμν□F,
□ϕ_a=ξRϕ_a.

The trace is −FR=−ρ−Σ(∂ϕ)²−3□F, while □F=−2ξ[Σ(∂ϕ)²+ξRΣϕ²]. Consequently

(F+6ξ²Σϕ²)R=ρ+(1−6ξ)Σ(∂ϕ)².

This independently fixes the sign and trace denominator B; freezing R before metric variation would not give this row. For the exact EdS real-field norm r=2A/t, δΣϕ²=2ru and β=ω²+1/4=4ξ/3,

t²δΣ(∂ϕ)²=r[U−2ωV−2βu+2βΨ],
δB=2ξ(6ξ−1)ru.

Subtracting R_bg δB, with t²R_bg=4/3, cancels every undifferentiated u term. Thus t²δR=[4Mδ/3+(1−6ξ)r(U−2ωV+8ξΨ/3)]/B exactly. The fresh symbolic reconstruction confirms this cancellation modulo the actual background ω² relation.

## Metric signs and curvature closure

For positive expansion K_i^j=(H−Φdot−HΨ)δ_i^j and lapse1+Ψ, the ADM Hamiltonian gives δG⁰₀=2[p²Φ+3H(Φdot+HΨ)]. The mixed momentum component is δG⁰_i=−2∂_i(Φdot+HΨ). The chosen covariant dust velocity gives δT_d⁰_i=ρ∂_i v_d; canonical scalar momentum is −ϕdot·∂_iδϕ. The improvement momentum is ∂_i[−δFdot+HδF+FdotΨ]. These yield exactly the displayed E_Φ momentum row, including the **negative**4M w_d/3 term after moving it to the solved right side.

For the mixed00 improvement, direct lapse/extrinsic variation gives p²δF+3HδFdot−3Fdot Φdot−6HFdot Ψ. Combining it with δT_d⁰₀=−ρδ and δT_can⁰₀=−ϕdot·δϕdot+Ψϕdot² reproduces the raw00 expression. Its Φ′ coefficient is4F+3ξr=4M−ξr, and the Ψ coefficient collapses to8M/3 after ω²+1/4=4ξ/3. This independently reconstructs C, rather than only substituting the author's already solved equations.

The Ricci scalar follows from

R=R^(3)+KijKij+K²+2Kdot/N−2Δ_hN/N

at first order and zero shift. R^(3)=4a^−2ΔΦ. This gives

δR=−6Φdd−24HΦdot−6HΨdot−12(Hdot+2H²)Ψ+2p²(Ψ−2Φ),

t²δR=−6Φ″−10Φ′−4Ψ′−8Ψ/3+2P(Ψ−2Φ).

It also passes the constant-lapse check δR=−2R_bgΨ and the static Minkowski check. Differentiating the independently reconstructed E_Φ along the independently assembled scalar/dust flow gave exactly

C′=(ξr/2F)C,   t²δR_geom−t²δR_trace=−C/F.

These two symbolic identities were rerun outside the author script; both vanish identically. Thus initial C=0 propagates, the scalar equations use actual geometric curvature, and scalar/dust conservation genuinely hold on that constraint surface. The Bianchi inference of the remaining spatial trace equation is then noncircular: k≠0, vanishing temporal/momentum/anisotropic-stress residuals and true scalar/matter conservation force the scalar spatial-trace residual to vanish. No off-shell trace replacement is presented as full metric closure.

## Scalar, dust and physical state count

For δχ=χ_bg(u+iv), χ_bgdot/χ_bg=(−1/2+iω)/t. Dividing the varied scalar equation by χ_bg leaves damping1/t, gyro terms∓2Ω times the relative derivatives, the metric derivative source χ_bgdot(Ψdot+3Φdot), the lapse source−2ξR_bgΨ, and−ξδR. Transforming to x=ln t cancels the1/t damping against the second-derivative chain rule and gives exactly U′ and V′ in the report.

Dust is minimally coupled here. With u_i=∂_i v_d, its geodesic equation is v_d_dot=−Ψ and continuity is δdot=3Φdot+p²v_d, hence w_d′=−Ψ−w_d. Under a scalar time shift η, δ→δ+3Hη and v_d→v_d+η, so Δ_d=δ−3Hv_d=δ−2w_d is gauge invariant.

Two canonical scalar fields supply four data, dust supplies two, and the Newton-gauge potential adds one constrained datum. The raw constraint has ∂C/∂δ=4M/3≠0, independently checked symbolically. Therefore the constraint manifold has dimension six even where the selected initialization chart solving Φ degenerates. The report appropriately restricts its particular Φ initialization to its nonzero coefficient. Its k=0 exclusion is necessary for the spatial Bianchi/gauge reduction. For ξ>3/16, B=M+ξ(6ξ−1)r>0. F bounded away from zero makes the finite-time ODE regular, with no denominator singularity at a slow-period/Hubble crossover. This proves regular transfer, not absence of growing physical modes or nonlinear matter caustics.

## Numerical source amplitude and evidence

The state initialization δ_i=1 is a unit transfer coefficient; multiply the entire perturbation by ε to obtain a physical weak perturbation. The report explicitly requires ε to keep dust, potentials and relative carrier modes small throughout. Fixed finite parameters and interval allow an arbitrarily small amplitude, but no uniform amplitude bound survives the singular parent limit. Initial u,U,v,V=0 is a selected mode prescription, not a derived formation history. The k formula sets only the **reference ordered-limit** slow pole equal to H_i; it is not an exact finite-system eigenmode identification.

Independently validated all five standard manifests with current input/output hashes via computation-audit validate_manifest.py --root PROJECT. exact_main_a passes 22/22; transfer_main_a passes 22/22. control_trace_a passes 20/22, rejecting both geometric/constraint identities. control_momentum_a passes 16/22, rejecting raw momentum, both closures and three GR growing controls. control_initial_constraint_a passes 14/22: its numerical solvers still succeed, but two initial-constraint and six sampled residual checks fail as intended. This is a meaningful physical-constraint control.

The correct transfer compares two DOP853 tolerances and Radau, all using the same independently audited RHS. Maximum scaled-state differences are 7.6414e−8 and 6.6202e−8. Only four epochs are explicitly sampled; these are not certified dense-output error bounds or a between-node constraint trajectory proof. F positivity on the tested interval also follows analytically from F increasing with time, not only sample values.

## What the Weyl numbers mean

The original GR seed has constant Φ_GR=−2/(3k²+4) and Δ_GR=−3PΦ_GR/2, so W/Φ_GR measures changed evolution from that seed. A different diagnostic is instantaneous GR sourced by the **same actual evolved dust density and momentum**:

W_dGR=−ρΔ_d/(2Mp²)=−2Δ_d/(3P).

This exact comoving GR constraint is not a quasistatic Poisson estimate based on Newton-gauge rest density. Nor is it a second GR evolution with the modified model's entire dust history prescribed; it is an instantaneous source normalization.

At the endpoint, W/original-GR≈1.0272464 or 1.0276301 and Δ_d/original-GR≈1.0272602 or 1.0276433. The same-actual-dust Weyl ratios are instead .9999865872679 and .9999870834829. Reading all three solver outputs independently gives cross-solver spreads 6.88e−15 and 2.44e−14 for that diagnostic, far below its approximately −1.3e−5 residual; this does not upgrade the result to interval-certified absolute precision. The approximately 2.7% Weyl increase is predominantly **ordinary dust growth**, not an extra cold lensing density. Finite background scalar stress can generate a nonzero Weyl contribution, unlike the strict parent's linear conformal limit, but these two examples do not establish a large one or a universal bound across initial modes.

## Obligation verdicts and exact remaining arrow

Raw finite action/trace, momentum/00 signs, scalar/dust rows, constraint curvature closure and state count: **passed**. Five manifest provenance records and the stated bounded transfer: **passed in their numerical scope**. Broad spectral/nonlinear health, independent carrier initial-data production, radiation history, observational prediction and 32π selection: **not addressed and not claimed**.

The finite EdS linear arrow is genuinely closed under its domain hypotheses. The next load-bearing implication is a physically supplied initial carrier/dust state and a sustained excess source/lensing response, followed by a nonlinear bound-source branch. The transfer is neither a cold abundance mechanism nor a √M MOND law, and its two chosen modes cannot rule out other finite-ξ responses. No author input or git state was changed.
