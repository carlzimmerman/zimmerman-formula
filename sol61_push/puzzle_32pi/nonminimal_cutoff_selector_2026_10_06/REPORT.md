# Nonminimal cutoff stabilization: a mechanism, but not a coefficient selector

Multiplying both Einstein and projected interaction terms by a positive cutoff-dependent prefactor F(u), u=ln T, changes the vacuum stationarity condition. Positive power laws and positive monomial sums still produce only unstable extrema. The conventional unshifted positive quadratic F=F0+αu² can instead stabilize a finite cutoff, but every such vacuum satisfies T<exp[4/(d−2)]. In four dimensions its conditional Λ/a0² is below πe²/4≈5.804, rather than 32π. A freely shifted quadratic can stabilize *any* finite cutoff, proving that stability alone is not a selector. These are common-vacuum action-level results, not full relative/clock health or sourced MOND completion.

## 1. Declared two-metric action and critical source normalization

Use d=n+1, n≥3, signature −+++, K>0, χn=(n−1)/(2(n−2)), a0>0, f²>0. Retain the UV-normalized projected interaction from the frozen dynamical cutoff action, M(0,T)=−A(T),

A(T)=2∫_0^∞ y b(y)/[1+(y/T)²]dy, b(y)=sqrt(1+1/y)−1.

The changed action is

S=K∫F(u)[Vg Rg+Vh Rh+2χn a0² v M(I,T)]
 −(f²/4)∫[Vg g^{μν}+Vh hatg^{μν}]∂μu∂νu,
v=sqrt(Vg Vh), F>0.

u is distinct from the shared foliation clock. The projected acceleration invariant is the parent's nonnegative exchange-even invariant; coincidence makes it and its first variation zero. This report does not alter that operator or pool any separate relative-sector health result. Canonical kinetic remains positive. There is no extra potential or fitted vacuum offset. F choices are declared new curvature couplings, not deductions from Claude's cutoff fit.

Multiplying Einstein alone fails the critical leading MOND cancellation. At fixed u in a local weak static leaf, each Einstein scalar has L=K(n−1)[(n−2)(grad ζ)²+2grad ν·grad ζ]. Its spatial constraint gives ζ=−ν/(n−2). Summing a pure relative lapse pair ±νrel/2 leaves −Kχn(grad νrel)². The projected term with M_I(0)=1/2 supplies +Kχn(grad νrel)². With Einstein-only F the sum is Kχn(1−F)(grad νrel)². Multiplying both terms by F preserves cancellation at every constant cutoff. This leading-order fact does not preserve the old full source law when u varies: nonminimal curvature derivatives and the canonical scalar equation must be included.

## 2. Both constant-u metric equations and the common Einstein frame

At coincidence g=hatg, the two independently varied metric equations at constant u give

2K F Gμν=−V0 F A gμν/2,
M0=4K, V0=2Kχn a0²,
Λ=V0 A/M0=χn a0² A/2.

The determinant variation supplies one quarter per sector. No hatted equation has been dropped. Nonconstant u also gives 2K(gμν Box−∇μ∇ν)F on each metric's left hand side and half the total canonical scalar stress on coincidence. The full scalar density equation contains

(f²/2)[Vg Box_g u+Vh Box_h u]
 +K F_u(Vg Rg+Vh Rh)+2Kχn a0²v[F_u M+F M_u]=0.

On the constant common vacuum, R=2dΛ/(d−2), and this equation becomes

p_A=β q_F, p_A=A_u/A, q_F=F_u/F, β=2/(d−2).

Thus a metric-only assignment of constant T is incomplete. The foliation row is satisfied at coincidence, but this does not classify its perturbations or relative metric modes.

The exactly exchange-even common sector has Jordan action M0 F R/2−f²(∂u)²/2−V0 F A. With gE=F^{2/(d−2)}gJ it becomes Einstein gravity with

U=V0 A F^{-β},
Z_E=f²/F+M0(d−1)/(d−2) q_F²>0.

At an equilibrium, the canonical common scalar mass is mψ²=U[p_A'−βq_F']/Z_E; prime here means d/du. A negative bracket is a genuine homogeneous de-Sitter scalar tachyon in this consistent even sector: δψddot+(d−1)HEδψdot+mψ²δψ=0 has a growing solution. This is not a statement about every possible full-theory completion. A positive bracket establishes this scalar vacuum minimum, not all relative-mode stability.

## 3. Exact retained cutoff slope and instability of power laws/sums

Set h(y)=yb(y)=1/[sqrt(1+1/y)+1]. For v=ln(y/T), J=∫h(exp(u+v))/(2cosh v)dv and A=2e^u J. Define ℓ(s)=(1−1/sqrt(1+e^{-s}))/2, strictly decreasing in s, and positive normalized measure μ proportional to h(exp(u+v))/(2cosh v).

Differentiation and an integrable integration-by-parts boundary give

p_A=1+Eμℓ, Eμℓ=Eμ tanh v,
p_A'=Covμ(ℓ(u+v),tanh v)<0.

The exact double covariance integral has opposing differences and positive full support. Var ℓ<1/16, Var tanh v<1, so −1/4<p_A'<0. Endpoint dominated convergence gives p_A→3/2 as u→−∞ and p_A→1 as u→∞, with 1<p_A<3/2 at all finite u. Also h<1/2 yields A(T)<πT/2. This self-contained derivation is independently pinned to the sibling cutoff-log-slope proof; no external convexity theorem is imported.

For F=T^q, U has one finite stationary point iff 1<βq<3/2. It is a strict maximum because (log U)''=p_A'<0. Outside this interval there is no finite equilibrium, including endpoint equalities. q is free; choosing q=p_A(T0)/β places that unstable point at any desired cutoff but does not select it.

For any finite positive monomial sum F=Σc_i T^{q_i}, c_i>0, q_F is the weighted mean of q_i and q_F'=Var(q_i)≥0. Thus (log U)''=p_A'−βVar(q_i)<0 everywhere. Every equilibrium is unstable. The logarithmic slope is strictly decreasing, so at most one finite root; it exists when its two endpoint slopes 3/2−βq_min and 1−βq_max have opposite strict signs. Finite endpoints of zero slope do not create a root. Neither argument applies to arbitrary positive F.

## 4. Conventional positive quadratic: actual finite stabilization, wrong conditional scale

Choose F=F0+αu², F0>0,α>0 (equivalently a positive canonical-scalar squared curvature coupling). Its q_F=2αu/(F0+αu²), with derivative of either sign. Any equilibrium has u>0 and

1<p_A=βq_F<2β/u,
0<u<2β=4/(d−2).

Hence d=4 forces T<e². The constant-vacuum parameter dictionary then gives Λ/a0²=A/2<πe²/4. No measured source a0 is silently substituted for this action parameter.

A concrete existence condition is α/F0>9/(4β²). The log-potential slope is positive at u=0 and at u≥2β, while at u=sqrt(F0/α) its second term βq_F exceeds 3/2>p_A. There are consequently at least two extrema, including a minimum in the sign-changing sense. Strict positive quadratic curvature is shown for sufficiently large α/F0 as follows: its positive-u limiting slope is p_A(u)−2β/u. A unique root lies in (4β/3,2β); on this interval its derivative is p_A'+2β/u²>−1/4+1/(2β)>0 for d≥4. The implicit function theorem therefore supplies a nearby strict minimum for all sufficiently large finite α/F0. This is a local vacuum existence/stability theorem; not a global cosmological attractor proof.

A bounded d=4 illustration F0=1,α=10 gives a maximum at u≈0.0587614243 (T≈1.06052220) and minimum at u≈1.84657477945 (T≈6.33807300). At the minimum A≈9.24627978528 and (logU)''≈0.504859432919>0, so Λ/a0²≈4.62313989. Independent precision/representation quadratures check these numbers; they are numerical corroboration, not a certified root isolation proof. No target cutoff was inserted. f² affects canonical masses and perturbation coupling, not these extrema.

A further exact common-sector prediction holds for either a shifted or unshifted quadratic. Put z=α(u−uc)²/F0. At a stable equilibrium z>1, q_F=p_A/β and q_F'=p_A²(1−z)/(2β²z). Therefore 0<(logU)''<p_A²/(2β), while Z_E/M0≥(d−1)p_A²/[(d−2)β²]. Since HE²=2U/[M0(d−1)(d−2)],

0<mψ²/HE²<(d−2)/2.

In d=4 the stable cutoff mass is below the de-Sitter Hubble rate. Thus this common scalar is not a rapid-oscillation cold component merely because it has a minimum. The statement does not exclude other relative/clock sectors or all possible cold mechanisms.

## 5. Stable arbitrary-cutoff counterfamily with a free curvature origin

To distinguish stabilization from selection, let any finite T0>0 be given and u0=ln T0. Let p=p_A(u0), β=2/(d−2)≤1. Choose

v0=4β/(3p), uc=u0−v0,
α/F0=9p²/(8β²), F(u)=F0+α(u−uc)².

At u0, αv0²/F0=2, q_F=p/β and q_F'=−p²/(4β²). The common vacuum equation is exactly satisfied and

(logU)''=p_A'(u0)+p²/(4β)>−1/4+p²/(4β)>0.

Thus every finite cutoff can be made a strict common vacuum minimum with positive F and canonical kinetic. These parameters encode the desired cutoff; they are a counterfamily to uniqueness, not an independent motivation for a specific number. The shifted origin is additional input. The unshifted natural quadratic's small-cutoff bound does not constrain this larger action family.

## 6. Newton normalization and operational limits

At constant u the individual Jordan tensor Einstein coefficient is 2K F. For Gauss units ΔΦ=Ω_(n−1) G_Nρ its tensor Newton normalization is

G_N,tensor=(n−2)/[(n−1)Ω_(n−1)2K F].

This follows from the trace-reversed Newton equation, not from declaring G_N unchanged when F varies. The summed common sector has coefficient M0F=4KF and therefore half this tensor normalization for the same total mirrored source. These two source conventions must not be pooled.

A nonminimal scalar can also change the operational measured force. In the restricted common-sector weak source problem, Jordan matter couples conformally in the Einstein frame with derivative −q_F/(d−2). On a locally frozen regular vacuum with a canonical common scalar, momentum pE much larger than background rates, the static source response has tensor-normalized boost

1+M0 q_F²/[(d−2)(d−3)Z_E] * pE²/(pE²+mψ²).

For a stable minimum this is the usual screened scalar exchange. In the light/UV limit its boost is less than 1+1/[(d−1)(d−3)], hence less than 4/3 in d=4 for f²>0. An unstable maximum does not supply a stationary stable long-wavelength force problem. This formula is for the consistent common/mirrored source sector, not a proven ordinary-visible-only two-metric MOND solution. Such a source excites relative and clock constraints, and the new u field changes the kernel and curvature variations. The full operational visible Newton and MOND a0 calibration remains an explicit obligation. Classical units are retained; no hbar or empirical Newton calibration is inserted.

## 7. Evidence and next implication

Checks reconstruct both metric/common vacuum factors, general-d scalar stationarity, Einstein-frame kinetic/mass signs, actual critical cancellation, monomial variance, the quadratic equilibrium bound, shifted strict-stable counterfamily, and bounded positive-integral quadratures. Negative controls omit the nonminimal scalar metric-trace contribution, assert a power-law minimum, or retain critical cancellation after changing Einstein alone. Current runs are separately recorded. No all-NLO, all modified-gravity, source-health or observational theorem follows.

The constructive advance is finite cutoff stabilization by a conventional positive curvature coupling, together with an exact failure to produce the target conditional coefficient and a stable arbitrary-cutoff counterfamily once the free curvature origin is allowed. The first missing full-theory implication is a conserved ordinary-source and relative/clock completion determining its operational Newton/MOND normalization. A microscopic rule fixing F and its origin remains necessary for true 32π selection.
