# A Cassini–vs–Ghost Pincer Closes the Khronometric-MOND Completion of Horizon-Scale Gravity

**Result: NO-GO for the exponential-kernel khronometric completion. Triangulated by three independent
analyses (two symbolic ADM reductions + Flanagan's published equations) and an independent check.
Honestly hedged where the literature hedges.**

## Abstract
FC-KH is a hypersurface-orthogonal khronometric (Hořava/Einstein-aether) completion of the
horizon-scale modified-gravity framework (a₀=½c√(Gρ_Λ)), with the MOND sector tuned to the exact
interpolation μ(y)=1−e^{−y}, y=a/a₀, on the PPN-null branch α=2β. We show it has no stability pass:
for **all a>a₀** the khronon no-ghost condition is violated, and the generalized khronometric
(β,λ) operators **cannot** cure it. This is one face of a general pincer: solar-system (Cassini)
safety forces μ→1 fast (the theory → GR at high a), which is exactly the boundary condition that
triggers the Flanagan khronon ghost and Bonetti–Barausse strong coupling; the ghost-free option
requires μ→1 slowly (a residual acceleration, → khronometric at high a), which carries a constant
∼a₀ solar-system tail excluded at ∼10⁴×. The exponential kernel sits at the Cassini-safe /
ghost-maximal corner. The whole single-foliation-scalar khronometric-MOND class is thereby closed.

## 1. Action
S = (c³/16πG)∫√−g[ R − ((β+3λ)/3)θ² − β σ² + f_FC(a) ] + S_m, a=|D_i ln N|, y=a/a₀,
f_FC(a)=−2Λ+α a²+2(2−α)a₀²[1−(1+y)e^{−y}]; χ=f'/2a=α+(2−α)e^{−y} ⇒ μ_phys=1−e^{−y} exactly (Bonetti–
Barausse normalization), G_N=2G/(2−α). Branch α=2β, β≲10⁻¹⁵ (GW170817), λ∼10⁻³. IR: 2 tensor+1 khronon.
Write W(y) with μ=W'/y; then W''(y)=1+(y−1)e^{−y}.

## 2. The khronon no-ghost condition and its violation (SOLID)
Flanagan (arXiv:2302.14846) analyzes exactly this class. His khronon quadratic action (Eq 42) has
kinetic tensor (Eq 32) h^{ij}=−(1/4πG)[χ̄(δ−n̂n̂)+(f̄''/2)n̂n̂]; the stability conditions (Eq 54,
verbatim) are **f'(a) ≤ a f''(a) ≤ 0**. In this notation f''=2(W''−1), so the longitudinal khronon
no-ghost is **W''(y) ≤ 1**, i.e. h_∥=(1−W'')/(4πG) ≥ 0. For the exponential kernel W''=1+(y−1)e^{−y},
so W''≤1 ⟺ **y≤1**: for all a>a₀, W''>1 ⇒ h_∥=(1−y)e^{−y}<0 (worst −0.135 at y=2, →0⁻ as y→∞).
General no-go (verified from scratch): any μ that reduces to GR at high a has y(1−μ)→0 at both y→0 and
y→∞ and >0 between ⇒ (y(1−μ))'<0 somewhere ⇒ W''>1 ⇒ ghost. Only the slow power-law tail μ=y/(1+y)
[which keeps a residual acceleration = khronometric, not GR, at high a] evades it.

## 3. The β,λ backbone cannot rescue it (SOLID, two independent routes)
- **Flanagan Eq 38 (literature):** in the slow-motion limit βσ²+(λ+β/3)θ² become
  β π_,ij² + (λ+β/3)(∇²π)² — **4-derivative spatial terms, zero time derivatives**. They do not enter
  the 2-derivative time-kinetic h^{ij} and cannot flip the sign of (1−W'') for a>a₀. They cure the
  generic high-k Minkowski instabilities (a UV fix), orthogonal to this IR transition ghost.
- **Full ADM reduction (independent):** three self-check-passing routes (each reproducing c_T²=1/(1−β)
  and c_s²=(α−2)(β+λ)/[α(β−1)(2+β+3λ)] to 16 digits) place the surviving f''-dependence in the radial
  sector with c²_{s,∥}∝f''(y)<0 on 1<y<38, and the identity c_s²·A_kin → 4/α−2 (β,λ-free as β→0)
  proves β,λ enter only the kinetic normalization, never the gradient. Either bookkeeping (kinetic
  ghost h_∥<0, or gradient c²<0) describes the SAME f''-zero pathology on a>a₀; β,λ cannot reach it.
Post-GW170817, |c_T−1|<10⁻¹⁵ forces |β|<2×10⁻¹⁵, closing even the β UV term; only λ(∇²π)² survives —
still 4-derivative spatial, still no cure.

## 4. Two honest corrections
- **Ellipticity ≠ stability.** The static MOND operator is elliptic ∀y>0 (λ_⊥=μ>0, λ_∥=W''>0). But
  W''>0 is the STATIC force-law Hessian; the dynamical khronon needs W''<1. For y>1: static-OK,
  khronon-ghost. The ellipticity result is true but stability-irrelevant.
- **Flanagan's hedge, now resolved.** Flanagan proves the CONDITION is violated near a∼a₀ (SOLID) but
  states solutions "might therefore be unstable" (footnote 7: a wrong-sign coefficient need not force a
  growing mode). An independent full-pipeline ADM reduction closes the hedge: it exhibits the explicit
  c²_{s,∥}<0 band AND quantifies the growth time in a galaxy transition shell at ~5×10³ yr (100 pc) to
  ~5×10⁴ yr (kpc) — vastly shorter than a ~10¹⁰ yr galaxy age. So this is a fast catastrophic
  instability, not merely a violated sufficient condition. Four independent analyses concur (two
  full ADM reductions agreeing to 1.5×10⁻¹⁶, Flanagan's published equations, and an independent
  check); all observational overlays (GW170817, α₁=0, 1PN) PASS, so the kill is internal, not a data
  tension.

## 5. The pincer (the general result)
Cassini/ephemerides ⟹ μ→1 fast ⟹ GR at high a ⟹ Flanagan ghost + B–B strong coupling.
Ghost-free ⟹ μ→1 slow ⟹ residual acceleration (khronometric at high a) ⟹ constant ∼a₀ tail ⟹
solar-system-excluded at ∼10⁴× (the "simple" kernel μ=y/(1+y) is the boundary case, and it is dead).
The exponential kernel is the Cassini-optimal / ghost-maximal corner. **No single-foliation-scalar
khronometric-MOND kernel simultaneously passes Cassini and the khronon no-ghost condition.**

## 6. Standing
The exponential-kernel khronometric completion is **closed**; more strongly, the pincer closes the
single-foliation-scalar khronometric-MOND class. With the single-metric pincer and the bimetric
no-gos, the khronometric branch of the completion is now a dead class. **Untouched:** the durable,
distinctive content — a₀=½c√(Gρ_Λ) and the falsifiable a₀∝H(z). The relativistic completion remains
the open problem; the khronometric route is not it.
