# The candidate written out in full (2026-09-05, night)

Every term, every parameter, its status, and what would kill it. "PASS" means a committed script with checks that can fail; "OPEN" means unproved. This is the most complete statement the repository can make tonight. It is a candidate, not a closure.

## 1. Fields and action
Metric g_μν; a clock scalar τ with unit normal n_μ = −∂_μτ/√(−g^{αβ}∂_ατ∂_βτ) and projector q_μν = g_μν + n_μn_ν (no aether vector: requirement 2 admits a clock scalar counted separately); a MOND scalar φ with Q = n^μ∂_μφ, V_μ = q_μ^ν∂_νφ, Y = V·V; matter minimally coupled to g_μν (requirement 11).

S = ∫d⁴x √−g { (1/16πG)[R − 2Λ] − c₁(∇_μn_ν)(∇^μn^ν) − c₂(∇·n)² − c₃(∇_μn_ν)(∇^νn^μ) + c₄(n·∇n)² − K(Q) − (2 − K_B) J( Y + ξ² q^{λσ}q^{μν}∇_λV_μ∇_σV_ν ) } + S_m[g, ψ_m]

in the PPN pipeline's sign convention (f31–f35, g03e). The healing-length term ξ²|∇⊥V|² is the coherence operator (f32); it may equivalently sit outside J with its own coefficient, which is the placement that keeps the static operator uniformly elliptic at zero field (g03c) with identical PPN.

## 2. Parameters and their values
| parameter | value / range | fixed by |
|---|---|---|
| c₁ = −c₃ = K_B | c₁₃ = 0 exactly | c_T = c (requirement 6, GW170817) |
| c₁₄ = c₁ + c₄ | ≈ 10⁻⁵ (> 0) | α₁ = −4c₁₄ + drag (f33): Solar-System bound; positivity for health |
| c₂ (khronometric λ) | ≤ 0.05 (0.1 at the edge) | BBN on G_cos/G_N = 1/(1 + 3c₂/2) (g03e); healthy for 0.01–0.1 (f34b) |
| K(Q) = K₂(Q − Q₀)² near the condensate | K₂ < 0 in this convention (healthy sign of the scalar's time-kinetic term, f34); |K₂| sets c_s² = (2−K_B)J_Y/|K₂| | linear stability; the dust amplitude C in a³K′ = C is a free cosmological initial datum (g03e) |
| J(Y) | fixed by the kernel, see §3 | the static law |
| ξ | ≥ 0.03 pc (canonical) / 0.05 pc (alt), a constraint, not derived | Cassini quadrupole, Saturn monopole, sunward gate (g03d, exact solve); the operator's own zero-field limit (g03c) |
| a₀ | 9.3619×10⁻¹¹ / 1.1279×10⁻¹⁰ m s⁻² | the framework's two footings; a₀ = ½c√(Gρ_Λ) is an optional relation, κ = ½ fitted (requirement 13 not derived) |
| G_N | G/(1 − c₁₄/2) (f35, = Einstein-aether's exactly) | measured Newton constant, requirement 10 |

## 3. The kernel a scalar carrier can carry (g03j)
With the scalar sourced by matter, J_Y√Y = g_N for a spherical source, so the scalar's own force g_φ = g_tot − g_N must be a non-decreasing function of g_N for a single-valued J, and its longitudinal stiffness dg_N/dg_φ = J_Y + 2YJ_YY must be positive. For the exact exponential kernel g_φ = a₀ y e^(−y) peaks at y_tot = 1 (g_N = 0.632 a₀) and falls, with negative stiffness for 1 < y < 38 — the FC-KH instability band a₀ < a < 38a₀ and f21's phantom maximum are this one fact. Therefore requirement 1 as literally written (exact exponential AQUAL at all accelerations) cannot be carried by a healthy scalar. The candidate's kernel is:
- exponential, μ = 1 − e^(−y), for y_tot ≤ 1 (the whole deep-MOND and transition regime up to g_N = 0.632 a₀);
- a monotone scalar force beyond, g_φ = (a₀/e)(g_N/0.632a₀)^p with small p ≥ 0 (p = 0 is the saturated limit; p > 0 keeps the stiffness strictly positive).
Its signature: the RAR lies +0.02 to +0.05 dex above the pure exponential at g_N = 2–10 a₀ and rejoins it above 30 a₀ (g03j). SPARC could not separate kernels at the 0.07 dex level (f25); BIG-SPARC can. In the Solar System the saturated scalar force a₀/e would be 940× the sunward gate; the coherence length screens it to a few per cent of the gate (g03j estimate; g03d exact: 0.14 at Neptune for ξ = 0.03 pc). So the same length that passes Cassini is what makes the scalar carrier admissible at all.

## 4. Static and cosmological limits (all computed)
- Static: ∇·[μ∇Φ] − ξ²Δ²ψ = 4πGρ for the total potential Φ = Φ_N + ψ, the operator acting on the scalar part only (g03d); ξ → 0 is exact AQUAL (G01 reproduced to 0.05%); Solar-System floors 0.03/0.05 pc.
- Zero field: uniformly elliptic with the term outside J; deep-MOND far field g = √(GMa₀)/r · (1 − ξ²/(r_M r)) (g03c, 0.1%); the Solar-System saddle anomaly is erased by 10⁻²⁹ (a null prediction).
- PPN (static ladder, boosted, Will dictionary): γ = 1, α₃ = 0, α₁ = −4c₁₄ + O(10⁻⁷), α₂(clock) = −6×10⁻⁶, scalar drags suppressed by 3×10⁻⁵ at (ξk)² = 10⁴ and further at the Cassini floor (f33, f33b).
- Linear health with time dependence: tensor ω² = k² exactly; two scalar modes, real positive ω², positive norm for kξ = 0.01–100 at the corner; the MOND scalar is Bogoliubov, ω² = c_s²k²(1 + ξ²k²); the clock is the fast khronometric mode with c_s² ∝ 1/c₁₄ (f34, f34b).
- FLRW: G_cos/G = 1/(1 + 3c₂/2); the operator and J are inert on the background (Y ≡ 0); the scalar gives dust of free amplitude plus a⁻⁶ (g03e).

## 5. Predictions that can lose
1. **Gaia DR4 wide binaries:** the frozen estimator returns γ_v = 1.032 (canonical) / 1.040 (alt), ± 0.015, against the registered band 1.16–1.23 and Newton 1.000 (g03g, g03h). Force boost 1.002 (3 kAU) → 1.064 (30 kAU) at the Cassini floor; larger ξ lowers it.
2. **The anisotropy sign flip, derived (g03k) and measured (g03i):** linearising the static law about the Galactic field gives the screened anisotropic Green's function Φ̂(k) = −4πGM(1 + ξ²k²)/[μ_e k²(1 + L cos²θ_k) + ξ²k⁴], L = y_e μ′(y_e)/μ_e, so the anisotropy of the boost depends on s/ξ and y_e only and its zero is s_× = x_×(y_e)·ξ exactly, r_e-independent; the quadrature gives x_× = 2.51 (canonical, y_e = 1.9) and 2.63 (alt, y_e = 1.573), decreasing from 3.14 at y_e = 1 to 2.38 at y_e = 3. The 3-D nonlinear scan measured 2.53 ± 0.05 and 2.63 ± 0.05 with s_×/r_e varying 2.5–6.8. At the Cassini floor s_× = 16.0 kAU (canonical) / 26.6 kAU (alt); perpendicular pairs are boosted more inside, aligned more outside. Bare AQUAL and bare QUMOND each keep one fixed ordering; only a coherence length flips it.
3. **The RAR bump:** +0.02 to +0.05 dex at g_N = 2–10 a₀ relative to the exponential kernel (g03j). Confronted with SPARC on f25's design (a₀ and M/L profiled jointly, 999 paired galaxy resamplings; g03l): the completed kernel's MSE is 0.04141–0.04150 dex² against 0.04121 (exponential) and 0.04060 (RAR); the paired difference to the exponential kernel is [−0.0001, +0.0003] dex² (95%), undecided; to the RAR kernel [+0.0000, +0.0014], mildly disfavoured at 95–99% exactly as the exponential kernel itself is. SPARC neither sees nor excludes the bump; BIG-SPARC's transition bins are the test.
4. **The saddle null:** no Bekenstein–Magueijo anomaly at any Solar-System field null (g03c).
5. **Newtonian-regime wide binaries:** no fifth force beyond the EFE response (f35 corrected, g03f).

## 6. What remains open
Requirement 7 as judgment (Lifshitz dispersion, superluminal clock mode; no instability, no Cherenkov exposure); the khronon's strong-coupling scale at small c₁₄ (literature: ∝ M_P√c₁₄, astrophysically irrelevant, not computed here); the dark sector's clustering — now computed at the Jeans level (g03m): inside a structure the scalar dust's stiffness is the kernel's own J_Y at the local field, so its Jeans length is environment-dependent; with the repository's own cluster acceleration at R500 (0.5 a₀) and representative densities, clusters at R500 capture the dust for |K₂| > 2.6×10⁶ while galaxy outskirts (KiDS) do not until |K₂| > 5×10⁹ and galaxy cores never inside that range: a factor-2000 window in K₂ where the KiDS-versus-cluster pincer is evaded. The captured FRACTIONS (≤ 14% around galaxies, 32–46% in clusters) still need the accretion calculation; the Coma UDG kill is not addressed; galactic phenomenology of the operator beyond the transfer estimate; unequal-mass wide binaries (a resolution-independent common-mode force is an open numerical item); the existence theory of the non-spherical fourth-order law; κ = ½ and a₀ underived. None of these is a computed failure. All are listed so that nobody calls this closed.
