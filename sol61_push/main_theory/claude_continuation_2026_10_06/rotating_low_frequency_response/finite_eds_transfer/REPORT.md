# Finite-ξ EdS clock, metric and dust transfer

The finite-parameter first arrow is now explicit: an exact constrained linear Fourier evolution system for the actual circular zero-stress EdS carrier, with dynamical ordinary dust. It does not freeze the metric, hold the dust source fixed, or use a UV Poisson approximation. The geometric curvature agrees with the algebraically reduced Einstein trace whenever the initial 00 constraint holds, and that constraint propagates exactly.

Two bounded evolving examples begin at the slow-clock/Hubble crossover and produce about 2.7% extra ordinary-dust growth over t_i→100t_i. Weyl/GR with the *same evolved ordinary-dust density* differs by only about −1.3×10⁻⁵ at the endpoint. The increased Weyl amplitude relative to the original GR seed is predominantly the altered dust growth, not an additional cold lensing density. This is not an observational fit, a general bound on other initial modes, or a nonlinear halo construction.

## Actual action, background and state

The action and conventions are preserved from the parent:

S=∫√−g [(M−ξΣϕₐ²)R/2−½Σ(∂ϕₐ)²]+S_dust[g], χ=(ϕ₁+iϕ₂)/√2,
χ₀=√A t^(−1/2) exp[iω ln(t/t₀)], ω²=4ξ/3−1/4>0,
a=(t/t_i)^(2/3), H=2/(3t), ρ=4M/(3t²).

The full carrier background stress vanishes; the background metric and ordinary dust are exactly EdS. The interval must satisfy F=M−2ξA/t>0. This does not assert positivity for every t>0 at nonzero A. The derivation is four-dimensional and massless except for the curvature-induced carrier frequency; ξ is finite throughout this child calculation.

Newton gauge is ds²=−(1+2Ψ)dt²+a²(1−2Φ)dx². For a nonzero comoving Fourier k, p=k/a. Write δχ=χ₀(u+i v) and define the dust velocity by u_i=∂_i v_d at first order. Then dust conservation is

δ̇=3Φ̇+p²v_d, v̇_d=−Ψ,

with δ the proper dust density contrast in Newton gauge. The gauge-invariant comoving density is Δ_d=δ−3H v_d.

Use x=ln(t/t_i), prime=d/dx, r=2A/t, P=p²t², w_d=v_d/t, U=u′, V=v′. Thus r′=−r, P′=2P/3 and

F=M−ξr, F′=ξr, B=F+6ξ²r=M+ξ(6ξ−1)r,
δF=−2ξr u, δF′=−2ξr(U−u), Δ_d=δ−2w_d.

The state is (u,U,v,V,δ,w_d,Φ): seven first-order variables with one initial metric constraint. This supplies six physical scalar-sector initial data at k≠0. The numerical time normalization t_i=M=1 is explicit and does not fix a physical selector or mass.

## Direct constraint reconstruction

The covariant equations are

F Gμν=T_dμν+Σ[∂μϕ∂νϕ−½gμν(∂ϕ)²]+∇μ∇νF−gμν□F,
□ϕₐ−ξRϕₐ=0.

The traceless spatial equation gives F(Φ−Ψ)=δF, hence Ψ=Φ−δF/F. No matter anisotropic stress has been inserted.

For the momentum constraint, the mixed components are δT_d⁰ᵢ=ρ∂ᵢv_d, δT_can⁰ᵢ=−ϕ̇·∂ᵢδϕ and δ(∇⁰∇ᵢF)=∂ᵢ[−δḞ+HδF+ḞΨ]. Therefore

2F Φ′=−4M w_d/3+r(−u/2+ωv)+δF′−2δF/3−(4F/3+ξr)Ψ.

Define this right-hand side divided by 2F as E_Φ. The derivative of Ψ is then Ψ′=E_Φ−δF′/F+δF F′/F².

The mixed 00 equation multiplied by t² has residual

C=(4M−ξr)E_Φ+(8M/3)Ψ+2FPΦ−(4/3+P)δF−2δF′
  +r(−U/2+ωV+4ξu/3)+(4M/3)δ.

The signs follow directly from δG⁰₀=2[3H(Φ̇+HΨ)+p²Φ], δT_d⁰₀=−ρδ, and
δ(∇⁰∇₀F−□F)=p²δF+3HδḞ−3ḞΦ̇−6HḞΨ.

An algebraic solve for the initial Φ uses coefficient

∂C/∂Φ=2FP−ξr(8M+ξr)/(6F).

This coefficient is nonzero for the tested initial data. It can vanish in other domains; the seven-state evolution itself does not divide by it after initialization. No universal initial chart claim is made.

## Exact Einstein trace and scalar evolution

Taking the metric trace and using the scalar equations gives

(F+6ξ²Σϕ²)R=ρ+(1−6ξ)Σ(∂ϕ)².

At first order the background scalar norm satisfies
ϕ̇·δϕ̇=(r/t²)[−U/2+ωV+(ω²+1/4)u].
Using ω²+1/4=4ξ/3, all undifferentiated u terms cancel in the trace. The result is

𝓡≡t²δR=[(4M/3)δ+(1−6ξ)r(U−2ωV+8ξΨ/3)]/B.

This is the full on-shell trace reduction, not δR inferred from an algebraic MOND force. The relative scalar equations become

U′=2ωV−Pu−½(Ψ′+3E_Φ)−(8ξ/3)Ψ−ξ𝓡,
V′=−2ωU−Pv+ω(Ψ′+3E_Φ),
u′=U, v′=V.

The remaining equations are δ′=3E_Φ+P w_d, w_d′=−Ψ−w_d, Φ′=E_Φ. These equations implement actual dust acceleration and source evolution.

## Geometric closure: no omitted metric evolution

Independently reconstruct the metric Ricci scalar in Newton gauge:

t²δR_geom=−6Φ″−10Φ′−4Ψ′−(8/3)Ψ+2P(Ψ−2Φ).

Differentiate E_Φ using the full seven-state equations and r′=−r, P′=2P/3. Exact rational algebra modulo ω²=4ξ/3−1/4 yields

t²δR_geom−𝓡=−C/F, C′=(ξr/2F)C.

Since F′=ξr, the residual has exact propagation C(x)=C(x_i)√[F(x)/F(x_i)]. Thus C(x_i)=0 implies C≡0 on any regular finite interval F>0; the scalar curvature used by the scalar equations is exactly the geometric curvature. The temporal metric evolution is not silently omitted. The spatial trace equation follows from the covariant Bianchi identity: at k≠0 the momentum and traceless spatial equations, scalar and dust conservation and vanishing C leave no independent spatial-trace residual. Conversely the explicit identities above check this reduction rather than assuming constraint preservation. The k=0 homogeneous/gauge sector is excluded.

For ξ>3/16 and A>0, B=M+ξ(6ξ−1)r>0. On any finite interval with F bounded away from zero, the seven-state linear ODE has smooth bounded coefficients and a unique finite linear transfer operator. The slow-clock/Hubble crossover introduces no denominator or singularity in these equations. This is regular finite-time linear evolution, not a theorem excluding growth or an EFT/nonlinear stability certificate.

The r→0 GR growing solution is independently recovered: Φ=Ψ=Φ₀ constant, w_d=−Φ₀, δ=−(3P/2+2)Φ₀ and Δ_d=−3PΦ₀/2. This fixes the reference normalizations without a subhorizon approximation.

## Bounded evolving transfer and physical diagnostics

For each ξ=100 and 1000 choose initial S_i=8ξ²A/t_i=0.4M, t_i=M=1, A=0.4/(8ξ²), and Z_i=1+3S_i/(2F_i). Set

k²=H_i²+2H_iΩ_i/√Z_i, H_i=2/3, Ω_i=ω.

The *parent ordered-limit reference frequency* √(k²+Ω_i²/Z_i)−Ω_i/√Z_i then equals H_i. This is a crossover diagnostic, not the exact eigenfrequency of the finite-ξ evolving system. Ω_i/H_i≈17.3 or 54.8; the entire purpose is to retain background evolution when this reference slow period is Hubble-sized.

Initialize δ_i=1 as a unit linear transfer coefficient, w_di=2/(3k²+4), u_i=U_i=v_i=V_i=0, and solve the exact C_i=0 for Φ_i. A physical solution multiplies all perturbations by an arbitrarily small ε; this is not a finite-density overdensity. The growing GR reference has the same initial ordinary-dust density and velocity, Φ_GR=−2/(3k²+4). Independent clock waves are explicitly set to zero in this selected initial condition; their effects are not universally bounded by these examples.

Integrate t_i→100t_i with DOP853 at rtol 10⁻⁹ and 3×10⁻¹⁰ and independent Radau at 10⁻⁹, atol=rtol/100. Monitor C, F and B. Outputs include Newton Φ,Ψ, Weyl W=(Φ+Ψ)/2, rest and comoving dust density. Each diagnostic distinguishes two GR references:

1. Evolved *original GR seed*: W/Φ_GR and Δ_d/Δ_dGR measure history/transfer change.
2. GR sourced by the *same actual evolved dust*: W_dGR=−ρΔ_d/(2Mp²)=−2Δ_d/(3P). W/W_dGR measures the residual Weyl contribution beyond ordinary dust, using an exact gauge-invariant GR identity rather than the Newton-gauge rest density.

Development output at t=100 gives:

| ξ | Weyl/original GR | comoving dust/original GR | Weyl/GR same actual dust |
|---|---:|---:|---:|
|100|1.0272464|1.0272602|0.9999865873|
|1000|1.0276301|1.0276433|0.9999870835|

The last residual is negative and small in these particular examples. These rows do not imply zero carrier stress at perturbative order; they show that a Weyl increase relative to a seed can be mostly altered ordinary-dust growth. At t=100, p/Ω is 1.428 or 0.793; the first case has left the low-p regime, but the exact evolution remains valid. At t=10 both are below one. Neither endpoint is evaluated with a frozen UV force law.

## Scope and next implication

The exact equations and constraint identities apply to finite-ξ linear modes on this declared EdS solution, at k≠0 and F>0. The displayed numerical transfer is bounded in time, parameters and initial data. Standard solvers and tolerance agreement are evidence for that transfer, not a validated interval-arithmetic trajectory certificate or a universal spectral-health proof.

The physical perturbation amplitude ε must keep |εu|,|εv|, potentials and dust contrast small throughout; large relative clock responses cannot be extrapolated to a halo. The parent's nonuniform shrinking-source warning persists if one subsequently takes its singular family limit. This child does not take that limit, nor does it supply a nonlinear amplitude-independent neighborhood.

A genuine cold response, if present, now requires an independent carrier/dust initial-data prescription, a sustained excess lensing/source density and a nonlinear bound-source solution. No cold abundance, MOND √mass law, radiation transfer, CMB prediction or 32π selector follows. The first finite EdS linear arrow has been made explicit and tested; source formation and nonlinear matching remain open.

REPORT is excluded from runner execution inputs. Source/HEAD hashes and declared tested range are in provenance.json and contract.json. Parent frozen inputs are read-only. Development outputs are retained separately from authoritative runs.

## Authoritative bounded runs

`runs/exact_main_a` passes 22/22 exact checks; `transfer_main_a` passes 22/22 bounded transfer checks. The trace-mixing control fails the two geometric/constraint closure identities; the dropped-dust-momentum control fails six checks: its raw constraint, both closure identities and three GR-growing-limit identities. The omitted-initial-constraint control fails the two initial-constraint tests and the six sampled constraint-residual tests, while its numerical solvers continue successfully. These are expected negative controls, not evidence that the corrected model failed. All five standard manifests validate against frozen execution inputs.

The two DOP853 tolerances and independent Radau agree with maximum scaled state discrepancies recorded in `runs/transfer_main_a/results.json`; no greater validation domain is asserted. The tabulated sampled constraint residuals are about 10⁻¹² or smaller. REPORT and this run-summary prose are excluded execution inputs; there are no historical standard runs with stale mathematical inputs in this child. Development preflights are explicitly separate.
