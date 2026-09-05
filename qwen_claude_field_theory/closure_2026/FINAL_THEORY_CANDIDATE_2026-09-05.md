# The candidate, as of 2026-09-05 morning: a clock host, one dynamical MOND scalar, and the healing-length operator

Assembled from what the lead's G03 established, the spec's own wording, and f32/f33/g03b/g02c. Not a completion. Every "PASS" below is a computed statement with a committed script; every "OPEN" is unproved.

## The action (schematic where the lead's ACTION.md is definitive)
S = ∫√−g [ R/16πG − Λ ] + S_clock[τ; c₁₃ = 0, c₁₄ small, c₂ = λ] + S_φ[g, n, φ] + S_m[g, matter],
with n_μ = −∂_μτ/√(−(∂τ)²) the clock's unit normal (no aether vector), q_μν = g_μν + n_μn_ν, and the MOND scalar sector
  S_φ = −∫√−g { K(Q) + (2 − K_B) J( Y + ξ² q^{λσ}q^{μν}∇_λV_μ∇_σV_ν ) },  Q = n·∂φ,  V_μ = q_μ^ν∂_νφ,  Y = V·V,
J chosen so the static law is the exponential kernel's (requirement 12), ξ the coherence (healing) length. Matter minimally coupled to g (requirement 11).

## Why this and not the alternatives
- Requirement 2 forbids an aether vector's modes but admits "a genuine matter or clock scalar … counted separately and shown healthy": the clock τ and the scalar φ are exactly that; the tensor sector is untouched (c_T = c, requirement 6).
- Requirement 7 (spec line 68) already excludes elliptic-constraint carriers as instantaneous channels; the lead's C-H has an elliptic heat sector and its own report says the naive realisation fails the causal screen. A dynamical φ replaces that sector with a hyperbolic one.
- The scalar's aether-mixing PPN lock (the 08-31 AeST kill) is evaded by the operator, not by tuning: f32 (aether host) and f33 (clock host) show α₁'s scalar drag becomes −4(2−K_B)/(J_Y(1+ξ²k²)+1) exactly, and the scalar's α₂ drag is suppressed 3×10⁻⁵ at (ξk)² = 10⁴.

## Scorecard against the 13 requirements
| # | Requirement | Status | Basis |
|---|---|---|---|
| 1 | exponential static law | PASS in the static limit of J; the ξ term modifies it at k ≳ 1/ξ | g00 contract; f32 |
| 2 | N_grav = 2 + counted scalars | PASS: count (2 tensor + clock + φ) and HEALTH at the PPN corner — time-dependent quadratic action (f34): both scalar modes real, positive ω², positive norm for kξ = 0.01–100, tensor ω² = k²; requires the MOND scalar's time-kinetic sign K₂ < 0 (pipeline convention) and c₂ outside the band near −1/2 | f34, f33b |
| 3 | Φ = Ψ, lensing | PASS in the ladder (γ = 1 at every point) | f32/f33 tables |
| 4 | PPN derived | PASS at the Cassini floor: α₁ ≈ −4c₁₄ + O(10⁻⁷), α₂(clock) = −6×10⁻⁶, scalar drags suppressed, α₃ = 0, γ = 1 | f33 K1–K5 |
| 5 | matter conservation | PASS by minimal coupling (inherited from AeST-type hosts) | not recomputed |
| 6 | c_T = c | PASS (c₁₃ = 0 built in) | pipeline |
| 7 | causality | OPEN as judgment, now with numbers (f34): the MOND scalar is Bogoliubov, ω² = c_s²k²(1+ξ²k²) with c_s² ≈ 0.04 (units c), and the khronon is the fast khronometric mode, c_s² ≈ 4×10⁴ ∝ 1/c₁₄; no instability, no ghost; superluminal modes evade the Cherenkov bound; see CAUSALITY_EXPLAINER §4 | f34 |
| 8 | FLRW | PASS (g03e, minisuperspace in the pipeline's convention): expanding FLRW with H ≠ 0; the clock only renormalises the cosmological constant of gravitation, G_cos/G = 1/(1 + (c₁₃ + 3c₂)/2); Y = 0 on the background so J and the operator are inert; the scalar's Q-sector gives ρ_φ = QK′ − K with the conserved charge a³K′, i.e. a dust piece of free amplitude plus an a⁻⁶ correction (the AeST structure). BBN (|G_cos/G_N − 1| < 0.13) puts c₂ = 0.1 at the edge and admits c₂ ≤ 0.05; f34b shows those c₂ are healthy | g03e, f34b |
| 9 | zero-field limit | PASS for the spherical law and the symbol with the ξ term OUTSIDE J (g03c): symbol J_Y k² + ξ²k⁴ uniformly elliptic at y = 0; point-mass solution regular, Newton-exact inside, deep-MOND 1/r outside with the computed correction −ξ²/(r_M r) (0.1%); field nulls: the bare law's saddle anomaly is erased (suppression 10⁻²⁹ at the Earth–Sun saddle). General non-spherical existence theory not done | g03c |
| 10 | measured G | COMPUTED, and it is a LIABILITY (f35): G_N = G/(1 − c₁₄/2) × (1 + f_s), the clock part validated against Einstein-aether exactly; the scalar's Newtonian-regime share f_s ≈ 0.9/J_Y is present at r ≫ ξ and screened by the operator below ξ (by 10⁻⁴), so the measured G is scale-dependent: a Yukawa-like fifth force of range ξ and strength f_s in the Newtonian regime. Bound from data (g03f, El-Badry EDR3 with the pipeline's cuts, 25,058 pairs at g > 8a₀, 0.2–2.8 kAU, differential in separation): f_s = +0.08 ± 0.23 at ξ = 0.02 pc (95% upper 0.46), +0.13 ± 0.44 at 0.03 pc (95% upper 0.9 statistical, 1.4 with the subsample spread); the mass-ratio halves disagree at > 3σ, so DR3 is systematics-limited at f_s ~ 0.5. The data therefore require only J_Y,Newton ≳ 1–2; the earlier 'few per cent ⇒ J_Y ≳ 30' was an assumption. A few-per-cent bound needs DR4 and the q systematic under control; f34b shows the sector healthy at J_Y = 1 and 30 either way | f35, g03f |
| 11 | one metric | PASS | construction |
| 12 | exponential primitive | PASS | g02c's Qt(s) |
| 13 | a₀ = ½c√(Gρ_Λ) | not derived (κ fitted) | standing |

Solar-System static gates for the operator's own static law, SOLVED EXACTLY (g03d: metric Newton + the MOND scalar's fourth-order law, Sun in the Galactic field, axisymmetric, both footings, three field inputs): floors ξ ≥ 0.03 pc (canonical) / 0.05 pc (alt); the quadrupole is the binding gate at 0.02 pc (1.05× the Park ceiling canonical), the phantom monopole inside Saturn binds on the alternate footing at 0.03 pc (1.10× Pitjev–Pitjeva at g_ext = 2.00×10⁻¹⁰); ξ → 0 reproduces G01's strict-AQUAL quadrupole to 0.05%. The proxy (g03b) had the same floors. T-B's double filter: 0.02/0.03 pc (G02). Wide binaries: aligned two-body tables (g02c) only; perpendicular orientation not computed.

## What would kill it
0. The Newtonian-regime fifth force of range ξ (f35): DR3 bounds it at f_s < 0.46 (ξ = 0.02 pc) to < 0.9–1.4 (0.03 pc) (g03f); DR4's Newtonian bins with the mass-ratio systematic controlled are the kill test, at the level 0.9/J_Y,N.
1. The clock corner (c₁₄ ≲ 2.5×10⁻⁵ with c₁₃ = 0) being strongly coupled: linear stability with the scalar present is now established (f34); the strong-coupling scale of the khronon (∝ M_P√c₁₄) is not computed.
2. The causal gate refusing the Lifshitz dispersion.
3. ~~The nonlinear static law failing the three Solar-System gates when actually solved~~ — solved (g03d): it passes for ξ ≥ 0.03/0.05 pc.
4. Galactic phenomenology: the operator changes the disc phantom only at k ≳ 1/ξ, but this is asserted from G02's G1, not solved.

## Calculations, in order
1. Clock-host stability with φ: DONE (f34) — no time-derivative pole from the mixing; healthy for K₂ < 0; PPN corner re-derived there (f33b, 0 FAIL).
2. The nonlinear fourth-order static solve for the Sun in the external field: DONE (g03d), floors 0.03/0.05 pc.
3. Zero-field limit with the ξ term outside J (requirement 9): DONE for the spherical law and the symbol (g03c); the general existence theory of the fourth-order quasilinear problem remains.
4. FLRW background and the measured G: DONE (g03e, f35); the wide-binary bound on f_s from DR3: DONE (g03f, weak: J_Y,N ≳ 1–2); the corner is c₂ ≤ 0.05 with J_Y,N free above ~2; f33's ladder explicitly at J_Y = 30 and the DR4-level bound remain.
5. Perpendicular wide-binary orientation.
