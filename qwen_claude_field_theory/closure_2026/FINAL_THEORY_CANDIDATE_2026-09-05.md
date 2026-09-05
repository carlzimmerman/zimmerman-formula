# The candidate, as of 2026-09-05 morning: a clock host, one dynamical MOND scalar, and the healing-length operator

**THE NUMBER (2026-09-05 night, g03g + g03h):** if the candidate is true, the pre-registered Gaia DR4 estimator (frozen shape, frozen bins, frozen cuts; nothing in the registration touched) returns **γ_v = 1.032 (canonical) / 1.040 (alt)**, DR4-sized error ±0.015; the registered band is 1.1614–1.1814 / 1.1917–1.2267 and Newton is 1.000. Orientation-averaged force boost at the Cassini floor ξ = 0.03/0.05 pc, registered external field 1.9 a₀, 1 M☉ pair: 1.002 (3 kAU), 1.006 (5), 1.014 (7), 1.025 (10), 1.040 (15), 1.052 (20), 1.064 (30) canonical; alt 1.002–1.088. Larger ξ lowers it. 3-D solver validated: single body vs the 2-D solve (6%), boost converged to 0.01% in resolution and box, AQUAL anisotropic Coulomb law reproduced at 100 kAU to 2–4%. One curve, one parameter bounded elsewhere, one dataset on a date: a DR4 result in the registered band kills the candidate; Newton within 2% below 10 kAU with a few-percent rise above 15 kAU is what it predicts. A second, overlooked handle: the aligned/perpendicular ordering of the boost FLIPS with separation (perpendicular larger below ~15 kAU, aligned larger above), a sign change the registered anisotropy statistic can read; the crossing separation is set by ξ.

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
| 10 | measured G | COMPUTED (f35, g03f), and the earlier 'free fifth force' reading is WITHDRAWN: G_N = G/(1 − c₁₄/2), the clock part validated against Einstein-aether exactly. The ladder's scalar share f_s ≈ 0.9/J_Y is not a free parameter in the candidate: J_Y is the exponential kernel's stiffness at the Galactic field, J_Y(y_e) = e^(y_e) − 1 ≈ 11 (canonical) / 7 (alt), so f_s ≈ 0.08 / 0.13 is the kernel's own external-field response ν_e − 1 = 0.09 / 0.15, i.e. the EFE phantom that the wide-binary boost already contains, screened below ξ (the knee). In the Newtonian regime (g ≫ a₀) the share is e^(−y): exponentially small. g03f's DR3 bound (f_s < 0.46 at ξ = 0.02 pc, < 0.9–1.4 at 0.03 pc) is consistent with this and constrains nothing new. No parameter remains free in the wide-binary prediction except ξ ≥ the Cassini floor | f35, g03f |
| 11 | one metric | PASS | construction |
| 12 | exponential primitive | PASS | g02c's Qt(s) |
| 13 | a₀ = ½c√(Gρ_Λ) | not derived (κ fitted) | standing |

Solar-System static gates for the operator's own static law, SOLVED EXACTLY (g03d: metric Newton + the MOND scalar's fourth-order law, Sun in the Galactic field, axisymmetric, both footings, three field inputs): floors ξ ≥ 0.03 pc (canonical) / 0.05 pc (alt); the quadrupole is the binding gate at 0.02 pc (1.05× the Park ceiling canonical), the phantom monopole inside Saturn binds on the alternate footing at 0.03 pc (1.10× Pitjev–Pitjeva at g_ext = 2.00×10⁻¹⁰); ξ → 0 reproduces G01's strict-AQUAL quadrupole to 0.05%. The proxy (g03b) had the same floors. T-B's double filter: 0.02/0.03 pc (G02). Wide binaries: aligned two-body tables (g02c) only; perpendicular orientation not computed.

## What would kill it
0. ~~The Newtonian-regime fifth force~~ — withdrawn as a separate item: it is the kernel's EFE response, already in the wide-binary boost (row 10).
1. The clock corner (c₁₄ ≲ 2.5×10⁻⁵ with c₁₃ = 0) being strongly coupled: linear stability with the scalar present is now established (f34); the strong-coupling scale of the khronon (∝ M_P√c₁₄) is not computed.
2. The causal gate refusing the Lifshitz dispersion.
3. ~~The nonlinear static law failing the three Solar-System gates when actually solved~~ — solved (g03d): it passes for ξ ≥ 0.03/0.05 pc.
4. Galactic phenomenology: the operator changes the disc phantom only at k ≳ 1/ξ, but this is asserted from G02's G1, not solved.

## Calculations, in order
1. Clock-host stability with φ: DONE (f34) — no time-derivative pole from the mixing; healthy for K₂ < 0; PPN corner re-derived there (f33b, 0 FAIL).
2. The nonlinear fourth-order static solve for the Sun in the external field: DONE (g03d), floors 0.03/0.05 pc.
3. Zero-field limit with the ξ term outside J (requirement 9): DONE for the spherical law and the symbol (g03c); the general existence theory of the fourth-order quasilinear problem remains.
4. FLRW background and the measured G: DONE (g03e, f35, g03f); the corner is c₂ ≤ 0.05, J_Y = e^(y_e) − 1 fixed by the kernel; f33's ladder explicitly at J_Y ≈ 11 remains a formality (the drag formula is J_Y-general).
5. Perpendicular wide-binary orientation: DONE (g03g, g03h) — THE NUMBER above. Next: a finer separation scan of the anisotropy sign flip (s = 12–22 kAU, θ = 0/90) and unequal-mass pairs.
