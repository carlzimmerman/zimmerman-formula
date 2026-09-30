# Why the tested horizon identification does not select 8π

Base checkpoint: eb9936a4d1cce68465ae0897dcc4fff71386ce2b. This advances the horizon-definition and dynamics obligations of the original joint galaxy/vacuum goal. The exact coefficient remains unresolved.

## Theory and local quadratic calculation

Use the covariant clock/polarization action from EXPANSION_BRIDGE_COMPLETENESS_RESULTS.md, replacing its cubic operator by the subtracted gapped operator

−βM²[(P²+p*²)^(3/2)−p*³]/Θ,

with p*>0, β>0, λ>1, and independently chosen U. Around P=0, Θ=3H, its expansion adds −βM²p* P²/(2H). Thus the total quadratic polarization potential is −M²ξP² with

ξ=1+δ, δ=βp*/(2H)=p*/a0,b, a0,b=2H/β.

Fluctuations of Θ multiply P² only at cubic order. This statement relies on the subtraction: it does not apply to the un-subtracted self-sourcing model's vacuum kinetic sector.

In the local large-wave-number limit, take spatial metric exp(2ζ)δij, lapse 1+n, scalar shift χ, and physical wave number k. Put B=λ−1>0, S=3λ−1=3B+2, v=dot(ζ). In units M²/2 the kinetic quadratic form is

−3Sv²−2Sv k²χ−B k⁴χ².

Eliminating χ=−Sv/(Bk²) leaves αv² with α=2S/B>0. The polarization sector is 4pkn−2ξp²; eliminating p=kn/ξ supplies ηk²n², η=2/ξ. The integrated intrinsic curvature supplies k²(2ζ²+4nζ). For example, this follows directly from R3=exp(−2ζ)[−4∇²ζ−2(∇ζ)²], expanded with N√h=(1+n)exp(3ζ) and integrated by parts.

Eliminating n=−ξζ gives

L2=(M²/2)[(2S/B)dot(ζ)²−2δk²ζ²],
cs²=δB/S.

These are local quadratic kinetic and gradient signs and a principal-sector speed, not complete de Sitter, nonlinear, strong-coupling, or causal health. In particular, solving gravitational constraints can introduce nonlocal response; a stable quadratic dispersion does not prove that every observable follows this cone. Higher-spatial-derivative completions can also invalidate a constant-speed ultraviolet extrapolation.

## Three distinct horizon tests

The chosen homogeneous vacuum metric in stationary areal coordinates is

ds²=−dt²+(dr−Hr dt)²+r²dΩ², u_mu dx^mu=−dt.

Its metric horizon is r=1/H, so Λr²=3 for Λ=3H². No parameter β enters this geometric identity.

If one extrapolates the derived scalar speed as a constant-speed cone throughout this background, its radial effective line element is −cs²dt²+(dr−Hr dt)². An inward characteristic has dr/dt=Hr−cs, stationary at rcone=cs/H. Equivalently, in the flat expanding slicing, the future event distance for this assumed cone is a(t)∫_t^∞ cs/a(t') dt'=cs/H. This is a conditional cone calculation, not an independently established horizon of the full theory.

For this foliation and stationary Killing vector K=∂t, u_mu K^mu=−1 everywhere. Therefore the usual stationary universal-horizon condition u·K=0 has no locus on this homogeneous branch. This calculation does not exclude differently foliated solutions or a distinct cosmological trapping definition.

## The new compatibility obstruction

The acceleration radius r*=1/(2a0,b)=β/(4H) obeys Λr*²=Cb/4, where Cb=Λ/a0,b²=3β²/4. The desired 8π is therefore a reformulation of Cb=32π until an independent radius definition is supplied.

Identifying the conditional scalar cone radius with r* requires

cs²=β²/16=Cb/12,
δ=(S/B)Cb/12.

At Cb=32π this gives δ=8πS/(3B)>8π≈25.133, because S/B=3+2/B>3. In contrast, the finite MOND regime of the gapped force law requires δ≪1. Even the necessary weaker requirement δ<1 implies Cb<12B/S<4. Thus this particular scalar-cone identification is incompatible with the proposed MOND window, even when U is free. Superluminality is not itself the obstruction; the required gap is.

This differs from the previous un-subtracted vacuum self-sourcing obstruction. Here the vacuum is independently adjustable, but the tested radius identification fails. Neither result excludes the original target across all theories. The bare a0,b-to-observed-a0 mapping remains conditional.

## Source and evidence scope

[Jacobson, arXiv:1001.4823v2](https://arxiv.org/html/1001.4823v2), equations (2), (9), (10), gives the infrared preferred-foliation action and its relation to hypersurface-orthogonal Einstein-aether theory. It also distinguishes action equivalence from equivalence of all solutions. Our signature is (−+++), intrinsic-curvature coefficient is one, and η above corresponds to its lapse-acceleration coefficient. Our polarization stiffness ξ is unrelated to that paper's intrinsic-curvature coefficient ξ. The speed and inequalities above were derived directly, not imported as a claim that the new nonlinear operator is already known to be healthy.

SciSpace discovery returned this paper, the de Sitter scalar study arXiv:1008.5048, and universal-horizon thermodynamics papers. The latter are discovery leads only; no black-hole theorem was transferred to cosmology. An attempted CERN PDF retrieval of arXiv:0909.3525 encountered an anti-bot page and is not evidence for an unread formula. No novelty claim is made.

`expansion_bridge_gap_cones.py` and its contract verify fourteen exact identities. The bounded runner saves raw output, result JSON, input hashes, and a validated manifest under `runs/expansion_bridge_gap_cones`. The inequalities follow algebraically from B>0; they are not inferred from a finite parameter scan.

Next remaining implication: a physical mechanism must select β and a vacuum curvature together, without defining its radius from a0 or prescribing a propagation speed to reproduce 8π. Additional operators could decouple the gap from the scalar speed, but that alone would create another free coupling rather than select the coefficient. Such a modification needs an independent microscopic or symmetry constraint before it is a promising solution route.
