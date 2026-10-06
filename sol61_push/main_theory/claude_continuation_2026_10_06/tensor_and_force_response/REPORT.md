# Zero background stress is not zero gravitational response

The same curvature-only carrier examined in ../REPORT.md changes tensor propagation and scalar-mediated force even on its exactly zero-stress circular EdS solution. This note quantifies those effects before asking whether they replace cold mass. It retains the original action and does not transfer a constant-mass carrier fit or an unrelated scalar-tensor result into the galaxy regime.

## Action and exact tensor block

Use the parent's conventions and two canonical real fields ϕ_a, χ=(ϕ₁+iϕ₂)/√2:

S=∫√−g [F(ϕ)R/2−Σ_a(∂ϕ_a)²/2]+S_dust,
F=M−ξΣ_aϕ_a²=M−2ξ|χ|².

On χ=√A t^−1/2 exp[iωln(t/t₀)], ω²=4ξ/3−1/4>0, ordinary-dust EdS remains exact because the **full** carrier stress vanishes. Nevertheless

F(t)=M(1−α/t), α=2ξA/M>0.

For spatial metric a²exp(γ), γ trace-free and transverse, det expγ=1. The ADM extrinsic term has KijKij−K²=−6H²+tr(γdot²)/4 at quadratic order; its spatial-curvature block is −tr(∂γ)²/(4a²). The homogeneous Fdot K boundary term has no TT velocity contribution because K=3H in this volume-preserving parameterization. Homogeneous scalar kinetic terms likewise carry no TT source. Thus

S_T²=1/8∫dt d³x a³F[γdot_ij²−(∂γ_ij)²/a²],
q_T=F, c_T²=1,
γddot+(3H+Fdot/F)γdot+p²γ=0.

This is the actual decoupled tensor block on the isotropic solution, not a fixed-metric scalar claim. The script independently evaluates diagonal exp(γ,−γ,0) extrinsic and warped-spatial curvature controls to check both coefficients. F>0 is necessary for positive tensor kinetic and gradient coefficients; F=0 is a degeneracy, not a healthy passage. It does not by itself settle all scalar/constraint health.

For EdS, damping is 2/t+α/[t(t−α)]. The homogeneous tensor solution includes ln(1−α/t)/α; its derivative is 1/[t(t−α)], with the usual −1/t decaying limit as α→0. High-frequency tensor propagation gives γ amplitude ∝1/(a√F). This WKB statement needs p≫H,Fdot/F and their variation scales, **not** p≫the internal carrier rotation, since the exact circular F has no phase oscillation. Its propagation-only distance ratio is d_L,GW/d_L,EM=√(F_observe/F_emit); source emission/coupling calibration is an additional issue.

## Early positivity restricts late renormalization

If the same exact branch is required to have F>0 throughout t≥t_i>0, monotonic F requires α<t_i. At any t_f>t_i,

δ_f≡(M−F_f)/M=α/t_f<t_i/t_f≡r,
M/F_f<1/(1−r).

In EdS r=(a_i/a_f)^(3/2). This is an exact action inequality, with no empirical time interval chosen. Requiring F>0 at every t>0 instead forces A=0 on this ξ>3/16 branch. A finite-start effective theory may evade that global condition; its start and initial data must be specified. Near-F=0 choices at late times cannot simultaneously keep this branch tensor-positive from a much earlier epoch. A nonzero zero-stress carrier is therefore physically consequential but has limited **late** Planck renormalization under early tensor positivity.

## Ordered ultraviolet static source dictionary derived directly

At a finite epoch define F_a=∂F/∂ϕ_a=−2ξϕ_a and

S_F=Σ_a F_a²=8ξ²A/t=4ξ(M−F).

Consider a weak conserved nonrelativistic source in a local static patch, with physical momentum p≫Ω,H,|Fdot/F| and all relevant background/mass rates, where Ω=ω/t. The source frequency must be small relative to p. In this ordered limit scalar mass/rotation terms can be neglected. It is **not** the response at p≪Ω, nor a full cosmological density-perturbation limit.

For metric ds²=−(1+2Ψ)dt²+(1−2Φ)dx² the leading varied equations are

F δGμν=Tμν+∂μ∂νδF−ημν∆δF,
∆δϕ_a=−F_a δR/2,
∆δF=−S_F δR/2,
(F+3S_F/2)δR=ρ.

The last line follows from the metric trace FδR=ρ+3∆δF. Retaining that trace compensation is essential. The 00 and traceless-spatial equations yield

∆Φ=ρ(F+S_F)/[F(2F+3S_F)],
∆Ψ=ρ(F+2S_F)/[F(2F+3S_F)],
∆(Φ+Ψ)=ρ/F.

Hence, for this UV static response,

G_force=1/(8πF) × (2F+4S_F)/(2F+3S_F),
G_lens=1/(8πF),
1≤G_force/G_lens<4/3,
Φ/Ψ=(F+S_F)/(F+2S_F)∈(1/2,1].

The limiting endpoint 4/3 requires S_F/F→∞. The tensor/Einstein-frame principal scalar kinetic metric δ_ab/F+3F_aF_b/(2F²) is positive for F>0; this is only a local principal statement, not a coupled finite-wavelength background stability proof. No measured Solar-System or galaxy constraints are inserted here.

Relative to G_bare=1/(8πM), the exact UV enhancement at δ=(M−F)/M is

G_force/G_bare=[2(1−δ)+16ξδ]/[(1−δ)(2(1−δ)+12ξδ)].

Combining early positivity with the principal force bound gives

G_lens/G_bare<1/(1−r),
G_force/G_bare<4/[3(1−r)].

For a declared example r=1/100, these are below 1.011 and 1.347. These are conditional mathematical controls, not an observed cosmic interval or an empirical exclusion. Large ξ can saturate the scalar 4/3 even when δ is tiny, but cannot remove the bound. If Newton's constant is instead calibrated by a local experiment in this same homogeneous UV environment, its uniform G_force is already the measured normalization: multiplying matter by the same factor elsewhere is not an independently generated cold abundance. In that same regime G_lens/G_measured=(2F+3S_F)/(2F+4S_F)∈(3/4,1], so lensing is not enhanced relative to that force calibration. Time/environment changes or the low-p branch require a new source calculation. Comparing a bare action coefficient with the measured constant silently would manufacture apparent missing mass.

## Exact radial/phase scalar rows expose the missing low-p implication

To avoid importing the UV formula, write δχ=χ₀(u+iv) with u,v real, on the actual EdS solution. In the fixed metric the exact linear scalar equations are

uddot+udot/t−2Ω vdot+p²u=0,
vddot+vdot/t+2Ω udot+p²v=0,
p=k/a, Ω=ω/t.

With Newtonian-gauge metric perturbations retained, their right sides are respectively

−(Ψdot+3Φdot)/(2t)−2m_eff²Ψ−ξδR,
Ω(Ψdot+3Φdot),
m_eff²=ξR=4ξ/(3t²).

These come from the actual varied scalar equation; δR is the perturbed Ricci scalar, not an independent assigned source. The radial perturbation changes δF, while the phase is coupled by rotation. Full metric/dust constraints and source conservation must still be solved to turn these rows into a force law. In particular the lapse source term proportional to m_eff²Ψ cannot be discarded when p≪Ω.

Freezing these **probe** rows only in an allowed adiabatic window gives determinant

(p²−σ²)²−4Ω²σ²=0,
σ_±²=(√(p²+Ω²)±Ω)².

At p≪Ω the slow branch has σ_-≈p²/(2Ω), not σ≈p. Even if p≫H, its freezing additionally needs p²/(2Ω)≫H and comparable coefficient-rate conditions. If that fails, the evolving radial/phase/metric system must be retained. These probe frequencies are not the coupled gravitational dispersion or an actual galaxy force. The next missing arrow is precisely the sourced low-p radial/phase constraint/evolution reduction; this note neither declares it harmless nor assumes that it reproduces the 4/3 ultraviolet result.

## Result and evidence scope

Zero homogeneous T is compatible with a nonzero observable gravitational coupling; the earlier stress obstruction is not an invisibility claim. This particular shortcut cannot provide arbitrarily large late UV lensing or force enhancement while staying tensor-positive from a much earlier epoch. Its homogeneous background still supplies no cold density, and no mass/abundance/32π selector follows. A changed low-p response, other histories or nonlinear inhomogeneous states are outside that bounded conclusion.

checks.py verifies exact TT coefficients/damping and homogeneous integral, source trace/Poisson/slip identities, force inequalities, relative radial/phase rows and their adiabatic probe limits. Intended controls freeze F incorrectly, omit scalar trace compensation, or import UV dispersion into low p. The derivations are from the explicit action; no external named theorem or new observational fit is invoked. Original parent report/checks remain unchanged. The first development attempt assigned a positive assumption to ∆δF although it is negative for positive ρ in the UV trace equation; SymPy rejected the solution. That implementation assumption was corrected before freezing inputs.

Authoritative main_a passes 26/26. Controls fail exactly the TT friction assertion (freeze_F), three trace/Poisson assertions (omit_scalar_trace), and the low-p slow-frequency assertion (import_UV_lowp). All four standard manifests independently validate against current inputs/outputs. Limits: 30 s wall, 20 s CPU, cooperative one-thread cap; no memory/affinity cap. REPORT.md is outside execution inputs, so this run-summary append does not stale evidence. Development preflight is not authoritative evidence.
