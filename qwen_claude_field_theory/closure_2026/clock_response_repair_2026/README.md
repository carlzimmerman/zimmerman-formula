# A coupled-clock response repair — not full gravity closure

Base checkpoint: `cbd7a4d683b68dd677f0e3706a2ebade970a6346`, 2026-09-10.
Objective remains Carl Zimmerman's full same-action relativistic MOND requirements.
Carl supplied the primordial-clock direction and the insistence on a global acceleration scale; this calculation develops that direction. It does not derive his fitted κ=1/2 or assert global novelty.

## Latest numerical/action checkpoint (2026-09-11)

See [fresh evolution and constraint energy](fresh_tangency_2026/REPORT.md).
Fresh states reproduce decreasing errors at 129->257, but the stronger
257->513 metric-tangency check deteriorates; late-time force/depletion claims
remain blocked by numerical consistency. A lapse-background cancellation
repair passes its regression and all 17 solver tests, but does not remove
that fine-grid failure. A separate exact Noether derivation supplies a weighted
constraint-energy balance, with four conditional Lean algebra certificates.
This is not physical-mode stability, a new MOND force law, or full theory closure.

## What changed

The review identified a missing clock/metric response in the L139→L152 fluid mapping. We now expand an explicit Einstein–cuscuton–χ action **with metric lapse, shift and scalar curvature included**. The scalar speed differs from the frozen-clock value 2C/K_QQ. Inverting the corrected expression yields an explicit coefficient that realizes a prescribed positive short-wavelength speed. This is a construction step, not just an exclusion.

The computation also derives the quadratic constraint chains independently at k≠0 and k=0. It does **not** certify the nonlinear constraints, the full MOND coupling, or cosmological spectra. One propagating χ field is counted openly; it is not hidden as an auxiliary and no particle-CDM component is added.

## Explicit sector and conventions

With signature −+++, c=1, Xτ=−∇τ·∇τ>0,

\[
S_{\rm sector}=\int\sqrt{-g}\,d^4x\left[
\frac{M^2}{2}(R-2\Lambda)+U(\tau)\sqrt{X_\tau}-V(\tau)
+K(Q)-C(Q,\tau)Y\right],
\quad n_\mu=-\frac{\nabla_\mu\tau}{\sqrt{X_\tau}},\quad
Q=n^\mu\nabla_\mu\chi,\quad Y=(g^{\mu\nu}+n^\mu n^\nu)\nabla_\mu\chi\nabla_\nu\chi.
\]

M² denotes a positive mass-squared coefficient (`M2` in code). The clock coefficient U>0 is `mu2`, allowed to depend on τ; its derivative is retained in constraint preservation. C_tau and C_Q are retained too. Constant U,C are special cases. This is the cosmological clock/dust **sector**, not a replacement claimed to supply galactic MOND by itself. A minimally coupled matter action can be appended, but its perturbations are not included in this sector-only calculation. A complete MOND metric/source coupling must still be chosen and varied; the existing incomplete leaf-MOND action is not silently assumed to solve that problem.

The non-MOND action here contains known types of operators. The particular inverse response formula is a project result; priority or novelty relative to literature has not been established.

## Background and derived quadratic action

Choose the monotone clock gauge τ=t and reconstruct U,V so that the background lapse is one. Set A=K_Q, B=K_QQ, assume A,B,Q,H>0, and use

\[
\dot A=-3HA,\quad \dot Q=-3HA/B,\quad
3M^2H^2=M^2\Lambda+V+QA-K,\quad
\dot H=-\frac{U+QA}{2M^2},\quad \dot V=-3HU.
\]

The last two equations include the clock enthalpy: it is not neglected or assumed to vanish. The code uses h_ij=a²exp(2ζ)δ_ij, N=1+α, N^i=∂^iβ/a², χ=χbar+σ, expands the ADM density before integrations by parts, and obtains

\[
\frac{L_2}{a^3}=M^2\left[-3(\dot\zeta-H\alpha)^2+
\frac{(\partial\zeta)^2-2\alpha\Delta\zeta+2(\dot\zeta-H\alpha)\Delta\beta}{a^2}\right]
+\frac B2(\dot\sigma-Q\alpha)^2-3A\sigma\dot\zeta
-\frac C{a^2}(\partial\sigma)^2+\frac A{a^2}\sigma\Delta\beta.
\]

Spatial integrations use periodic or decaying boundaries. The plane-wave representative follows from rotational invariance of the scalar quadratic FLRW sector; it is not a nonlinear reduction to a one-dimensional universe.

For k≠0 the momentum equation gives α=ζdot/H+Aσ/(2M²H). Introduce u=σ−Qζ/H, physical wavenumber squared q²=k²/a², and

\[
d=\frac{QA}{2M^2H},\quad e=-\frac{3A}{B}+\frac{QU}{2M^2H^2},\quad
f=\frac{BQU}{2M^2H^2},\quad b=A-2CQ,\quad D=U-QA+2CQ^2.
\]

After the time-dependent change of variables and its boundary terms,

\[
\frac{L_2}{a^3}=\frac B2(\dot u-du)^2-\frac{3A^2u^2}{4M^2}-Cq^2u^2
+\zeta\left[f(\dot u-du)+\frac{q^2b}{H}u\right]
+\frac12\left(ef-\frac{q^2D}{H^2}\right)\zeta^2.
\]

The actual kinetic coefficient and high-frequency speed are therefore

\[
\mathcal K(q)=B-\frac{f^2}{ef-q^2D/H^2},\qquad
c_{\rm eff}^2=\frac{2C-b^2/D}{B}
=\frac{2C(QA+U)-A^2}{B(U-QA+2CQ^2)}.
\]

A second expansion of the covariant two-field density in a local inertial frame reproduces this speed by eliminating the clock from its computed spatial Hessian. The U→∞ frozen-clock limit returns 2C/B; C=A/(2Q) returns the k-essence control A/(QB).

## Constructive coefficient

Define m=U/(QA)>0, c_ad²=A/(QB) and choose a target ratio 0<r≤1. The action coefficient

\[
\boxed{C(Q,\tau)=\frac{K_Q}{2Q}\,
\frac{1+r(Q,\tau)[m(Q,\tau)-1]}{1+m(Q,\tau)-r(Q,\tau)}}
\]

gives, by substitution into the action-derived short-wavelength expression,

\[
c_{\rm eff}^2=r\,c_{\rm ad}^2,\qquad
D=\frac{QA\,m^2}{1+m-r}>0.
\]

This constructs a family; it does not determine the freely chosen function r from first principles. For B>0, f>0, e<0, the derived kinetic coefficient is positive for every q²>0 (and its regular q²→0 limit). This does not replace the separate homogeneous analysis. Subluminality of the high-frequency cone additionally needs r c_ad²≤1. The e<0 condition is independent of choosing a positive UV speed. An initial trial m=0.1, Q=A=M²=H=1, B=100, r=0.1 failed at small q; it is preserved as a negative control. The illustrative m=0.01 trial satisfies e<0 and positive kinetics.

Lean certifies five conditional real-algebra statements: denominator positivity, the repaired D identity, D positivity, the exact response ratio, and kinetic positivity. It does not formalize the variation or the physical meaning of their inputs.

## Actual constraints, not inserted counts

All statements here concern the quadratic scalar sector after spatial scalar gauge and τ=t gauge fixing. They do not count the omitted nonlinear diffeomorphism system by arithmetic.

At k≠0 the canonical variables before eliminating auxiliaries are (ζ,σ,α,β) with their momenta. Primary constraints are p_α and p_β. The shift secondary fixes β=−p_ζ/(2a³M²q²); its two-by-two Poisson matrix is computed. After that canonical auxiliary elimination the lapse secondary and its preservation give

\[
\mathcal C=H(p_\zeta+3a^3A\sigma)+Qp_\sigma-2a^3M^2q^2\zeta,\quad
\mathcal T=-\frac{U}{2M^2}(p_\zeta+3a^3A\sigma)+a^3q^2b\sigma,
\]

\[
\{\mathcal T,\mathcal C\}=-a^3\left[\frac{3QAU}{2M^2}+q^2D\right]\ne0.
\]

Preservation fixes α through a fourth-stage constraint; the next equation fixes its primary multiplier. The script computes the assembled six-by-six Poisson matrix and its rank, including both lapse/shift primaries and all derived constraints. Its generic rank is six: six second-class, zero remaining first-class constraints in this gauge-fixed scalar system, leaving one scalar canonical pair. Preservation of the eliminated shift relation fixes the shift multiplier and cannot introduce a new constraint because its bracket is nonzero. The independent u,ζ formulation yields the same one-pair result from its computed two-by-two matrix.

At k=0 the momentum equation vanishes and is **not divided by k²**. Set I=a³A≠0. The independent homogeneous chain is

\[
p_\alpha,\quad H(p_\zeta+3I\sigma)+Qp_\sigma,\quad
p_\zeta+3I\sigma,\quad \alpha+\frac{p_\sigma}{a^3BQ}.
\]

Its computed four-by-four bracket matrix has rank four. In a fixed finite comoving cell it leaves one global canonical pair, not a propagating Fourier wave. Additional global dilation/boundary identifications must be specified before interpreting that pair. No H=0 condition is imposed. Limits U=0, A=0, H=0, r=0 or D=0 require separate constraint analyses; none is certified by substituting into a generic-rank result.

## An expanding background family, with explicit limitations

For constant m choose a monotone background Qbar(τ) and set U(τ)=m Qbar K_Q(Qbar), V(τ)=m ρ_χ(Qbar), where ρ_χ=QK_Q−K. Then

\[
H^2=\Lambda/3+(1+m)\rho_\chi/(3M^2),\qquad
\dot V=-3HU
\]

follow consistently from the charge equation and satisfy Raychaudhuri. The code checks those identities and samples a concrete cosh K background at 37 logarithmically spaced scale factors 10⁻⁶≤a≤10³. It uses r=A_t/(A_t+K_Q), which rises approximately as a³ when K_Q≫A_t. The parameters and every sample are recorded in the results. This construction reconstructs U,V as functions of the background clock: it is not an independent microphysical derivation of those functions, and the finite sampling is not a proof of stability for all cosmic time.

There are no raw empirical data in this experiment. It supplies an action-derived candidate for subsequent data tests, not a CMB, cluster, lensing or galaxy fit. Radiation/baryon perturbations, recombination and their background contributions must be added and recalculated, not borrowed from the earlier free-fluid run. The scale-factor normalization and r-function parameters are inputs. No local/environmental a₀ is introduced; a₀ and its fitted Λ relation are not derived or modified in this sector.

## Immediate bottlenecks: finite wavelengths, then interactions

The boxed construction fixes the **high-frequency** speed, not a scale-independent fluid sound speed at all wavelengths. From the exact auxiliary denominator, the crossover is

\[
q_{\rm mix}^2=-efH^2/D>0\quad(e<0).
\]

Its ratio to H in the illustrative background is approximately 669.4 at a=10⁻³ and 237.5 at a=1. These are model diagnostics, not observed scales. Thus even k/a≫H does not automatically justify replacing the coupled equations by their UV sound speed. The first next calculation must evolve the **finite-k equations from the recorded reduced action**, including their time dependence and metric response. In particular, the extremely small early-time UV speed in this sample does not certify CMB-safe clustering.

The price of the repair is visible analytically. With ε=2CQ/A,

\[
\epsilon-\frac1{1+m}=\frac{r m^2}{(1+m)(1+m-r)}.
\]

Cold early-time response can put the coefficient extremely close to the zero-gradient boundary. Exact symbolic engineering avoids floating-point cancellation but does **not** establish radiative stability or a safe interaction cutoff. Small m also makes D small. The other unavoidable computation is the **cubic reduced action, canonically normalized interaction scales and nonlinear constraint preservation on a spatially varying χ background**. That distinguishes a genuine healthy repair from an accidentally degenerate linear branch. The current quadratic positivity certificate cannot answer it.

The other live route remains the explicitly varied DHOST curvature extension in `../kgb_healthy_matching_2026/`; its coefficients and certificates are not merged into this different action. A third route is the non-power-law EOS reopening identified in the review. This checkpoint prioritizes the coupled-clock repair because it directly addresses the broken action-to-fluid map.

## Evidence and known failed execution attempts

- Initial algebra run: exit 1 at the positive-kinetic assertion for the m=0.1 trial; this was a genuine rejected parameter point, now retained as a negative control.
- One extended run: interrupted with exit 130 while a generic symbolic solver simplified a linear multiplier equation. Replaced that operation with direct affine solution; the equations were not weakened.
- Initial Lean build: missing cached module from a broad import. Narrowed imports to the three required tactics without installing packages. A subsequent definition needed the standard `noncomputable` qualifier for real division; the final five theorem proofs are unchanged in mathematical scope.
- `run_checks.py` records exact executed commands and exits, the complete algebra output, Lean axiom reports and the existing ten-check review regression. The bounded-run manifest pins inputs and environment.

The original complete-theory objective is **OPEN**. Neither a small sound speed, a green suite, a formal algebra certificate, nor a finite parameter sample is a completed law of nature.
