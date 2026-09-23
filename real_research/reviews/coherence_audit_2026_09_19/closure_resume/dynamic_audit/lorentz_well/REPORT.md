# Lorentz-well replacement: independent variational and static audit

**Verdict: correct only after a stated restriction.** Replacing −F(Q) by −F(s), s=sqrt(Q²−Y)>0, has exactly the proposed quadratic contribution and leaves the FRW kinetic matrix and linear lapse/shift constraints unchanged. The exponential well alone is a healthy timelike perfect fluid with intrinsic sound speed squared epsilon/s. This is not automatically a characteristic speed or stability theorem for the complete clock–MOND theory, whose other couplings remain. Static MOND cancellation is altered whenever the local well charge is nonzero.

The action under review has F(s)=−A exp[(s−Q0)/epsilon], A>0, epsilon>0. The future timelike homogeneous branch uses Q>0 and Y=0, so s=Q. All formulae below omit the common positive gravitational normalization. No claim about fixing kappa is made.

## Exact quadratic variation

Since Y starts at second perturbative order,

    s = Qfield − Y/(2 Qbar) + O(perturbation³),
    −F(s) = −F(Qfield) + F1 Y/(2 Qbar) + O(perturbation³).

With the ADM measure and Y=(P_x)²/a² at quadratic order this gives

    Delta L2 = a F1 (P_x)²/(2Qbar).

For Euler–Lagrange convention E_P=L_P−partial_x L_Px, its real-space contribution is −a F1 P_xx/Qbar. For a Fourier mode it is therefore

    Delta E_P = +a F1 k² P/Qbar.

The sign in the proposed correction is correct. F1<0 makes this a positive restoring contribution in the physical equation convention after reversing the archived EL sign. The term contains neither velocities nor lapse/shift perturbations, so the full reduced K and the lapse/shift solutions are unchanged. Only the undifferentiated P coefficient in the scalar equation changes, before solving for the accelerations. Reconstructing a differentiated constraint or a physical observable must use those **new** accelerations.

`check_well.py` verifies the contribution directly from the nonlinear ADM expressions N=1+e psi, scale=a exp(−e Phi), Qfield=(Q+e Pdot−e² shift)/N and Y=e²(P_x)²/scale². It checks that derivatives of Delta L2 with respect to psi, Phi, Pdot and shift vanish, and verifies the Fourier sign independently.

Homogeneous dynamics are exactly unchanged because s=Q on Y=0, including all homogeneous variations that preserve the FRW ansatz. Off a homogeneous background the difference is substantive, not a rewriting of −F(Q).

## Intrinsic fluid and ghost sign

Use X=−g^{mu nu}phi_mu phi_nu/2=s²/2 and pressure function p(X)=−F(sqrt(2X)). Direct differentiation gives

    p_X = −F_s/s,
    p_X+2X p_XX = −F_ss,
    c_s² = p_X/(p_X+2X p_XX) = F_s/(s F_ss).

Let n=−F_s=A exp[(s−Q0)/epsilon]/epsilon>0. Then

    −F_ss=n/epsilon>0,       −F_s/s=n/s>0,
    c_s²=epsilon/s,
    p=epsilon n,             rho=(s−epsilon)n,
    rho+p=s n.

Thus the isolated well has positive temporal and spatial quadratic coefficients. For s>epsilon it also has positive density and a subluminal intrinsic cone. For 0<s<epsilon the same local kinetic signs hold, but the cone is superluminal and the displayed density is negative. The s→0 limit is singular and has not been certified. The same homogeneous scalar block is

    L2_well = [n/(2epsilon)](deltaQ)² − [n/(2Q)] |grad P|²,

up to metric mixing and background terms. This is the standard pressure-supported fluid gradient term that the old clock-projected well lacked.

The covariant sector has no preferred-clock dependence: Q²−Y=−(dphi)² identically. Equivalently, for L(Q,Y)=−F(sqrt(Q²−Y)), the exact identity

    −2Q L_Y − L_Q = 0

holds for all admissible Q,Y. The script verifies this identity, not just a homogeneous two-jet. The full theory still contains preferred-clock terms, so only this sector has been removed from that dependence.

## Static MOND consequence

Write d=2−K_B. At small Y about a local timelike background,

    −d beta Y − F(sqrt(Q²−Y))
      = −F(Q) − d beta_eff Y + O(Y²),
    beta_eff = beta − F1/(2dQ) = beta+n/(2dQ).

For the existing constant-alpha quadratic gradient block, eliminating the spatial metric potential first gives

    L_grad = −(2−alpha)|grad psi|²
             +2d grad psi·grad P−d beta_eff|grad P|².

Completing the square shows the residual scalar coefficient is

    beta_eff−d/(2−alpha).

The old choice beta=d/(2−alpha) therefore leaves the positive scalar-flux floor

    Delta beta=n/(2dQ)=rho/[2dQ(Q−epsilon)] > 0,

where rho is the **local** well rest density in the action's normalization. It cannot be assigned the cosmological homogeneous value inside a galaxy without a local solution. This completes only the quadratic spatial derivative block; lapse-mass/density-response terms and a nonlinear environmental alpha can change the full finite-wavelength static solution.

At nonzero local density the asymptotic zero-gradient MOND cancellation is lost. A Q-dependent counterterm beta=beta_cancel+F1/(2dQ) cancels the new quadratic gradient exactly and restores the old quadratic system. Such a counterterm would undo the proposed quadratic perturbation repair, even if it changed nonlinear terms. Suppressing local charge instead is physically different and must be derived from the solution.

## Nonlinear charge suppression and the sonic boundary

At finite Y, s=sqrt(Q²−Y), the added transverse static flux coefficient is n(s)/s, or Delta beta(Y)=n(s)/(2d s). At fixed Q,

    n(s)/n(Q)=exp[(sqrt(Q²−Y)−Q)/epsilon]
             ≈exp[−Y/(2Qepsilon)] when Y/Q² is small.

This can suppress the local charge/floor strongly while preserving the homogeneous background. However, the well's longitudinal stationary flux derivative is

    d[(n(s)/s) p]/dp
      = (n/s)[1+Y/s²−Y/(s epsilon)],       p²=Y.

It is positive precisely when

    Y s < epsilon Q²,

which is the subsonic condition Y/Q²<c_s²=epsilon/s. At larger gradients the isolated well's stationary equation is not elliptic along the flow. This is not by itself a temporal ghost: a stationary boundary problem can cross a sonic point while the covariant fluid remains hyperbolic. The remaining MOND operator adds its own transverse and longitudinal stiffness, and **the total** operator has to be tested. Exponential charge suppression is therefore a possible finite-gradient mechanism, not a free proof that galaxies recover the old MOND law.

For a stationary phase phi=omega t+P(r), the local value is s²=omega²/N²−h^{rr}P_r² when shift is zero. The lapse, scalar gradient and charge profile must be solved together and must stay timelike. A local density cannot be selected independently after choosing this phase and boundary data.

## Exact Legendre form and one static counterexample

The original exponential time well has the auxiliary form

    −F(Q)=extremum_n [n Q−U(n)],
    U(n)=n[Q0+epsilon log(epsilon n/A)−epsilon],
    U'(n)=Q0+epsilon log(epsilon n/A),  U''(n)=epsilon/n>0.

The Lorentz replacement uses the same convex rest potential but replaces nQ by n sqrt(Q²−Y). Around Y=0 its additional gradient cost is −nY/(2Q). At quadratic order the auxiliary action is

    delta_n delta_Q − epsilon (delta_n)²/(2n) − nY2/(2Q).

Eliminating delta_n=n delta_Q/epsilon gives

    n(delta_Q)²/(2epsilon) − nY2/(2Q).

This independently exposes the exact kinetic/gradient ratio epsilon/Q and its connection to the convex Legendre potential. Away from Y=0, n is the **rest-frame** charge density; the canonical clock-slicing density is nu=dL/dQ=nQ/s, so they must not be conflated on a tilted background. The Legendre energy density in that slicing is rho+nY/s. The coordinate temporal Hessian is n[Q²/(epsilon s²)−Y/s³], positive on s>epsilon.

An exact rational local event shows that the old static ellipticity certificate cannot carry over unchanged. Set

    alpha=1/40000, d=9/5, beta=72000/79999,
    s=Q0=1, epsilon=1/10^9, n=93/50,
    Y=1/10^8, Q²=100000001/100000000, a0=1/10,

with A=epsilon n. Take the stated deep-MOND longitudinal coefficient

    B_L,old=beta+2 beta² sqrt(Y)/a0,
    B_L,well=n/(2d s)[1+Y/s²−Y/(epsilon s)].

For the symmetric static spatial principal block

    M=[[2−alpha,−d], [−d,d B_L]],

`static_witness.py` obtains the exact signs

    det M_old = 11664/1999975 > 0,
    det M_new = −535479983488514879907/31999600000000000000 < 0
              ≈ −16.7339586585.

Meanwhile the well's temporal Hessian is exactly

    9300000092999999907/5000000000 > 0.

This event is timelike but supersonic: Y/Q²>epsilon/s. It refutes transfer of that constant-alpha stationary ellipticity statement to all timelike local jets of the new action. It is **not** an actual global halo solution, a temporal ghost, or a growing-mode theorem. It also uses the explicitly supplied deep-MOND coefficient rather than certifying a complete interpolation function or environmental-alpha completion.

## Existing project variants and a sign warning

The bounded repository search covered Markdown/Python/TeX in `real_research`, `fable_independent_2026`, `deepseek_push`, and subsequently `qwen_claude_field_theory/closure_2026`, using explicit Q²−Y, P(X), Lorentz-invariant and density-well patterns. It found substantial prior structural work, so this architecture is not new to the project:

- `qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_transport/repair.py`, lines 20–30 and 67, explicitly constructs K(Q)−C(Q)Y−D(Y)=P(Q²−Y) and verifies the same exact clock/bracket-defect identity. Its README sections 2–4 describe polynomial then logarithmic P(X) sectors with a separate lapse-independent W(Y). Those are different actions from this exponential well with acceleration mixing; their health or failure cannot be transferred.
- `fable_independent_2026/L138_velocity_lemma_is_particle_specific.py`, section B2, already derives the intrinsic Lorentz-invariant relation c_s²=K_Q/(QK_QQ). Its empirical claims were not re-audited here.
- `real_research/clock_2026/L289_carrier_requirements.py` adds a **second** minimally coupled X_chi carrier while switching off the MOND scalar's roll. It is therefore not the proposed same-field replacement. More seriously, its implemented line 51 has L_chi=−G1 deltaX−G2 deltaX²/2, while lines 91 and 102 use G1,G2>0. Consequently p_X=−G1<0 and p_X+2X p_XX=−(G1+2X G2)<0 on X=C²: its isolated carrier has the wrong kinetic sign even though the ratio c_s² is positive. Line 86 also states the density sign for +F despite implementing −F. Its old growing-root calculation cannot serve as evidence for a healthy positive-density carrier. This exponential proposal avoids that sign issue because F1,F2<0.

No exact same-field exponential −F(sqrt(Q²−Y)) replacement was found in this bounded search. That is a repository search result, not a global novelty claim. No external theorem or observational bound is imported into this audit.

## Lean certificate of the exact local event

`StaticWitness.lean` explicitly defines alpha, d, beta, s, epsilon, n, Y, a0 and Q² over the reals. It defines the old/new 2-by-2 matrices and derives their actual `Matrix.det` expressions. Ten theorems check the square root of Y, the determinant bridge, all three exact rational values, their signs, the timelike/supersonic conditions, and the combined local tradeoff. Every printed axiom list contains only `propext`, `Classical.choice` and `Quot.sound`; no `sorryAx` is used.

`verify_lean.py` compiles with the existing `fable_independent_2026/lean_2026` host (Lean 4.34.0-rc2), independently reruns the symbolic event, and checks that its exact fractions match the Lean theorem statements. The bounded run and pinned inputs/results are recorded in `run_verified_lean/manifest.json`. The formal boundary is explicit: Lean certifies this matrix/event algebra; the variational action-to-matrix derivation remains the adjacent symbolic/mathematical audit. A finite local jet certificate proves neither a global halo solution nor a dynamical failure.

## Scope and next test

The exact correction and ghost-free intrinsic-fluid statement pass on their stated timelike branch. Positive K for the full FRW scalar system carries over because the correction changes no velocity Hessian or linear constraint. Full gradient/Jeans behavior, physical transfer norms, nonlinear interactions and static MOND compatibility remain separate obligations.

The next decisive test is the parent's complete corrected phase evolution, followed by the total static transverse/longitudinal operator on an actual local-charge solution. A local short transient cannot certify an entire response family: the parent reports a separate large transfer witness for the old response_n4 at a=.1 over Delta N=.5, which was outside this agent's earlier two-interval audit and is not independently verified here.

All new artifacts are confined to `dynamic_audit/lorentz_well/`; earlier artifacts remain unchanged. Exact results and provenance are in the bounded computation manifest. Final self-proofreading checked only this report and found no unresolved local sign/notation mismatch.
