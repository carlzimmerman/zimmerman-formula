# Constrained rotating response: an ordered on-shell linear-operator limit

The zero-stress curvature carrier does have a slow, stable sourced response in a controlled limit of its exact EdS backgrounds. Eliminating the metric gives two real poles, with the slow frequency proportional to p²/Ω. The static force boost is at most 4/3 and the extra response contributes zero to the linear Weyl/lensing potential. Resonant driving can amplify force, but is neither a cold density nor a stationary MOND law. This closes a previously scalar-only local calculation, not the finite-parameter FRW/galaxy problem.

## Raw action and the limit

Use signature (−+++), c=ℏ=1, canonical real fields ϕ₁,ϕ₂ and χ=(ϕ₁+iϕ₂)/√2:

S=∫√−g [F R/2−½Σₐ(∂ϕₐ)²]+S_m[g], F=M−ξΣₐϕₐ²=M−2ξ|χ|².

M>0 has mass dimension 2. The parent report reconstructs the actual circular EdS solution χ₀=√A t^(−1/2) exp[iω ln(t/t₀)], H=2/(3t), ω²=4ξ/3−1/4>0, ordinary background dust ρ_bg=4M/(3t²), and exactly vanishing full carrier background stress. Here A has mass dimension 1; the coupling norm S below has mass dimension 2. No scalar mass is independently inserted.

Fix Ω>0 and S>0. For each ξ→∞ choose a local epoch T=ω/Ω and amplitude A=S T/(8ξ²), and evaluate on a finite local interval τ=t−T. Different members of this family have different action parameter ξ and amplitudes; this is not the late-time limit of one fixed model. Then

H→0, F→M, |χ₀|²→S/(8ξ²), Σ Fₐ²→S, ξR_bg→Ω²,

while the direction of Fₐ rotates at rate Ω. Background scalar amplitude and its canonical stress vanish, but Fₐ and its rotating derivative remain finite. The limiting Jordan quadratic action retains δF δR/2 and the scalar mass Ω². It is incorrect to drop ξR_bg just because R_bg tends to zero.

This is an ordered *linear-source derivative first, background-family limit second*. The nonlinear vertices proportional to ξ diverge. Perturbations must be arbitrarily small relative to the shrinking background amplitude; no uniform finite-density nonlinear neighborhood or EFT cutoff is established.

## Full metric reduction and the surviving dust term

At linear order the Jordan constraints are

M δGμν=Tμν+∂μ∂νδF−ημν□δF,  M δR=−T+3□δF.

The improvement term has identically zero divergence. T here is the trace of an additional conserved perturbative source, not ρ_bg. Background dust perturbations are absent as independent finite-amplitude degrees of freedom in this limiting response; the background matter's quadratic coupling must nevertheless be kept.

One transparent reduction uses g_E=(F/M)g_J. The Einstein scalar kinetic metric is δₐᵦ+3FₐFᵦ/(2M). The background dust's conformal second variation contributes

−ξρ_bg Σδϕₐ²/(2M) → −Ω²Σδϕₐ²/2.

Although ρ_bg→0, ξρ_bg/M→Ω². This equals the retained Jordan curvature mass; omitting it would produce a different, off-shell limiting operator. Rotating the canonical basis produces +Ω²(U²+V²)/2 and exactly cancels this mass. The extra conformal kinetic term is −3S ημν∂μU∂νU/(4M), equivalently +3S U̇²/(4M) minus its spatial gradient: the derivative of the rotating Fₐ cancels the apparent V contribution in ∂δF. It produces no additional gyro term.

Choose radial orientation δF=−√S U and δϕ=Rot(Ωτ)(U,V). Let Z=1+3S/(2M)>0. For a spatial Fourier mode of physical wavenumber p the fully metric-reduced limiting scalar action is

L₂=½Z U̇²+½V̇²+Ω(U V̇−V U̇)−½Z p²U²−½p²V²−√S J U/(2M),

where J=−T. Matter coupling follows from h_J=h_E−δF η/M: ½Tμνh_Jμν=½Tμνh_Eμν−δF T/(2M). For a nonrelativistic source J≈ρ the displayed source is negative, and the static δF response is positive. Tensor and Einstein metric constraints are those of ordinary linear GR with coefficient M; no lapse or shift is held fixed to manufacture Z.

## Retarded response and stability of this limit

The equations are Z(Ü+p²U)−2ΩV̇=−√S J/(2M), V̈+p²V+2ΩU̇=0. With e^(−iστ), a=p²−σ² and D=Z a²−4Ω²σ²,

U=−√S J a/(2M D), δF=S J a/(2M D).

The retarded prescription is σ→σ+i0. For p>0 the two positive poles are

σ±=√(p²+Ω²/Z)±Ω/√Z,
σ₋=√Z p²/(2Ω)+O(p⁴/Ω³), σ₊=2Ω/√Z+O(p²/Ω).

The source susceptibility a/D decomposes into positive residues A₋/(σ₋²−σ²)+A₊/(σ₊²−σ²), where
A₋=(p²−σ₋²)/[Z(σ₊²−σ₋²)], A₊=(σ₊²−p²)/[Z(σ₊²−σ₋²)], A₋+A₊=1/Z.

Canonical momenta P_U=Z U̇−ΩV and P_V=V̇+ΩU give

H₂=(P_U+ΩV)²/(2Z)+(P_V−ΩU)²/2+Zp²U²/2+p²V²/2.

This is positive for p>0 (semidefinite at p=0). It is the conserved corotating/helical quadratic Hamiltonian. Both high-p characteristic speeds are 1; the pole group derivative p/√(p²+Ω²/Z) is below 1. These statements concern this linear limit, not a nonlinear ultraviolet completion. There is no damping: a finite pulse leaves oscillations, and perpetual resonant forcing has no bounded steady response. A large driven amplitude at σ₋ is not a relaxed cold component.

## Source and force dictionary

Take g₀₀=−1−2Ψ and gᵢⱼ=(1−2Φ)δᵢⱼ. Then

Ψ_J=Ψ_E−δF/(2M), Φ_J=Φ_E+δF/(2M),
Φ_J+Ψ_J=Φ_E+Ψ_E.

Thus the additional scalar is conformal and contributes no extra linear Weyl lensing potential for the same conserved source. Source/observer calibration and nonlinear propagation are separate obligations.

A Fourier source with wavevector p in the z direction can be explicitly conserved: contravariant T⁰⁰=ρ, T⁰ᶻ=σρ/p, Tᶻᶻ=σ²ρ/p², all other components zero. Its trace is T=−ρ+σ²ρ/p². Therefore J≈ρ only for |σ|≪p, which includes the slow pole for p≪Ω. The scalar formula above remains trace-exact; the following Newton force formula is nonrelativistic.

In this slow-source regime Ψ_E=−ρ/(2Mp²)+O(σ²/p²) corrections, so

Ψ_J/Ψ_E=1+[S/(2M)] p²(p²−σ²)/D.

At σ=0 this becomes 1+S/(2MZ)=(2M+4S)/(2M+3S)∈(1,4/3). Static low-p enhancement equals this bound, rather than becoming a new scale-dependent cold mass. At a driven pole the force susceptibility grows, while the conformal scalar still cancels from Φ+Ψ. No MOND √mass law, cold abundance or 32π coefficient is selected: S, Ω and homogeneous waves remain independent data. Linear source dependence also cannot by itself establish nonlinear MOND.

## Orders of limits and exact remaining implication

At finite ξ, the scalar's slow period is ~Ω/p². A local frozen calculation requires not merely Ω≫H and p≫H, but σ₋≫H and all background coefficient rates. For Z of fixed finite size this leaves √(ΩH)≪p≪Ω as a possible low-frequency adiabatic window. At p²/Ω≲H the full nonautonomous EdS metric+dust+scalar system is mandatory. Taking σ→0 in the limiting susceptibility is not proof that an actual finite-ξ cosmological source relaxes to that static state.

For a fixed comoving mode in the parent EdS solution, p∝t^(−2/3), Ω∝t^(−1), hence p/Ω∝t^(1/3). The history changes regimes; ordered frozen low-p limits do not describe its entire future. The next missing arrow is the finite-ξ sourced FRW system with background dust perturbations, evolving scalar amplitude/rotation and physical initial/boundary data, followed by a nonlinear bound-source branch. No cold density or selector has been established here.

## Evidence scope

Exact algebraic controls reconstruct the limiting coefficients, retained dust mass, full trace coefficient, canonical action/Hamiltonian, conserved source, pole/residue formulas and metric dictionary. They are bounded symbolic checks supporting the derivation, not substitutes for the finite-ξ FRW missing arrow. REPORT is not an execution input; final run-summary prose does not change the frozen algebraic evidence. Requested base is 85251b027; actual inspected HEAD and input SHA-256 hashes are in provenance.json. No external theorem is needed for the local derivation; source anchors are the parent action audits listed in SOURCES.md.

Authoritative `runs/main_a` passes 37/37 exact checks. Four controls each pass 36/37 and reject their declared single change: omission of metric-trace kinetic mixing, omission of the background-dust quadratic mass, reversal of the radial source orientation, or assigning conformal scalar response to Weyl lensing. All five standard manifests validate against frozen inputs. The development-only `preflight_a` radical simplification failure is retained; it is not fresh authoritative evidence. `preflight_b` and the standard runs use the common-denominator identity with separately verified pole factorization. No report file was pinned as an execution input.
