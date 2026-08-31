# Neda frontier — 2026-08-31 (khronometric-MOND candidate seeded)

## Architecture search: EXHAUSTED
no_new_streak ~72k iterations. The relativistic-MOND completion space is a closed pincer; all
single-metric and standard/derivative bimetric routes are dead classes (DC-013..DC-020). Only a
preferred-frame carrier (aether/khronon) legally carries MOND lensing. Neda is now a TARGETED-CALC
frontier, not an architecture generator — if a proposal dedupes to a dead class, the exhaustion
detector firing (NO_VIABLE_CANDIDATE_IN_GRAMMAR) is the correct scientific outcome. Do NOT invent a
new architecture to avoid exhaustion.

## LIVE CANDIDATE — FC-KH v1.0 (khronometric MOND, hypersurface-orthogonal aether)
S = (M_Pl^2/2) ∫√-g [ R − (β+3λ)/3 θ² − β σ_{μν}σ^{μν} + f_FC(a) ] + S_m,
  n_μ = −∇_μT/√(−∇T·∇T),  a_μ = n^ν∇_ν n_μ,  a=√(a_μa^μ),  y=a/a₀,
  f_FC(a) = −2Λ + α a² + 2(2−α) a₀² [ 1 − (1+y) e^{−y} ].
Normalization identity (Bonetti–Barausse convention μ=(1−χ/2)/(1−α/2), χ=f'/2a):
  χ(y) = α + (2−α) e^{−y}  ⇒  μ_phys(y) = 1 − e^{−y} EXACTLY at every acceleration,  G_N = 2G/(2−α).
Observational branch: α = 2β (PPN-null: α₁=α₂=0), β ~ 1e-15 (GW170817: c_T²=1/(1−β)), λ ~ 1e-3–1e-1.
High-a limit → khronometric gravity (α a² − 2Λ_eff), NOT GR (avoids the BB strong-coupling limit).
IR content: 2 tensor + 1 khronon (no spin-1; n_μ hypersurface-orthogonal).

## DEAD sub-branch — pure-BM exponential (β=λ=0)
f_B = −½ f_FC ⇒ f_B'' = −α − (2−α) e^{−y}(1−y). Sign flip of the longitudinal khronon kinetic at
y_crit = 1 + eα/2 ≈ 1 ⇒ radial khronon is a GHOST for a>a₀ (Flanagan-level, pure f(a) theory).
The PPN-safe α=2β~1e-15 CANNOT cure it: curing by the α a² term alone needs α > 2/(e²+1) = 0.238,
15 orders too big. So the pure exponential f(a)-only theory is DEAD; the tiny α does not rescue it.

## THE ONE TERMINAL GATE (PASS / KILL) — the only calc worth compute now
Derive the FULL β,λ≠0 spherical quadratic scalar operator on the nonlinear MOND background ā(r):
expand T=T̄+π, δg; eliminate lapse+shift; obtain
  S²_scalar = ½∫[ K(r,k) π̇² − G(r,k)(∇π)² − M(r,k) π² ].
Green light iff K>0 AND G>0 (and c_sc²=G/K sane) THROUGH a(r)/a₀ ~ 1.
Mechanism that keeps this OPEN not dead: the β,λ terms are purely SPATIAL (∂∂π)², but the shift
constraint (δN_i sourced by π̇) feeds them into the time-kinetic on reduction — toy: A_eff = A₀ + g²/M,
so β,λ CAN add a positive time-kinetic near a~a₀. NOT certified (K,G>0 across the whole transition,
radial AND tangential, uncomputed). Also confront P7/DC-010/014: does GW170817→β≈0 + screening
reintroduce strong coupling with only λ as the backbone?

## AeST cousin — α₁,α₂ result (workflow wn8klys0x, SOLID, adversarially verified)
No AeST paper DERIVES or even ASSERTS α₁=α₂=0 — AeST PN-safety is scalar SCREENING (J~Y^{p≥3/2}),
NOT a preferred-frame symmetry (papers claim only γ_PPN=1 via Φ=Ψ). The Maxwell aether point (c123=0)
is a GENUINE α₂ simple pole with FROZEN spin-0 (c_S²=0) — a strong-coupling degenerate point, the
OPPOSITE of benign; aether α₁=−4K_B is finite-nonzero. ⇒ the AeST route does NOT hand us α=0 for free;
the khronometric α=2β construction is the cleaner preferred-frame-null, but inherits the SAME terminal
transition-stability gate above.

## Overnight
Ollama is DOWN as of launch ⇒ Neda runs ALEATORIC-ONLY (PRNG + gates, no interpretive architect).
Expect fast exhaustion. NO git commits (AR_GIT_COMMIT unset), NO pushes ever.
