# G00 — Freeze and authenticate (2026-09-04, roadmap FRIED_CHICKEN_ROADMAP_2026-09-04.md §6)

## The four targets, distinguished (none may be silently substituted for another)

| ID | Name | Equation (static, weak field) | Where it lives | Track |
|---|---|---|---|---|
| T-A | **exact exponential AQUAL** (the strict target) | ∇·[(1 − e^{−\|∇Φ\|/a₀})∇Φ] = 4πG_N ρ_b, one potential Φ felt by matter and light | FRIED_CHICKEN_SPEC requirement 1; `aqual_solar_gate_2026/`; `theory_2026/aqual_solver_2026.py` (with μ_exp) | A |
| T-Q | **exact-inverse QUMOND** | Δu = 4πGρ_b; ΔΦ = 4πGρ_b + ∇·[(ν(\|∇u\|/a₀) − 1)∇u], ν(s) = y/s with s = y μ_exp(y), i.e. ν is the exact inverse partner of μ_exp (f21's `nu_muexp`; the roadmap's ν(s)) | Milgrom 2010 eqs (3)–(6); f21/f23 "μ_exp" rows; `smoothed_onset_action_2026` at ξ = 0 | parent of B |
| T-R | **empirical RAR kernel** | g_obs = ν_RAR(g_bar/a₀) g_bar, ν_RAR = [1 − e^{−√y}]^{−1}; in AQUAL variables the parametric pair μ(u) = 1 − e^{−u}, x = u²/μ(u), u = √y | THE_COMPLETION §1.1; every phenomenology script; f23/f24/f29/f30 numbers | phenomenology only |
| T-B | **double-filter extension** | Δu = 4πGρ_b; ΔΦ = 4πGρ_b + S∇·f(∇Su), f(p) = [ν(\|p\|/a₀) − 1]p, ν the T-Q inverse partner, S = e^{ξ²Δ/2} (Gaussian, std ξ), S* = S on flat isolated space; the output filter is compulsory (it is the adjoint the variation inserts) | roadmap §4; `smoothed_onset_action_2026/REPORT.md` (action varied, 10 tests) | B |

Relations that hold and ones that do not: T-A and T-Q share both limits and differ in the transition (f21: up to 0.073 dex in g_obs); T-R ≠ T-Q (f21, f23; SPARC cannot separate T-Q from T-R once a₀ and M/L are profiled, f25/f26; T-A's spherical relation equals T-Q's only for spherical sources). T-B → T-Q as ξ → 0 (spherical); "recovering the spherical relation at ξ = 0 does not prove general-source AQUAL" (roadmap §2). f29 and f30 used T-R with a single Gaussian filter and no output filter; their floors are **not** T-B floors and are not reused in G02.

## Frozen inputs
a₀ canonical 9.3619×10⁻¹¹, alternate 1.1279×10⁻¹⁰ m s⁻² (both, always); GM☉ = 1.32712440018×10²⁰ m³ s⁻²; observed Galactic field at the Sun 2.32×10⁻¹⁰ m s⁻² with endpoints 2.00 / 2.64×10⁻¹⁰ (±2 × the repository's 0.16×10⁻¹⁰); Park et al. 2026 Q₂ likelihood (central 1.6, σ 1.8, two-sigma ceiling 5.2 ×10⁻²⁷ s⁻²) and Pitjev & Pitjeva 2013 extra-mass bound inside Saturn's orbit (< 6.7×10⁻¹¹ M☉) as observational inputs, recomputed from the model observable, not copied as ceilings. Sign convention: Φ_N = −GM/r; Φ₂ = c₂ r² P₂; Q₂ = −3c₂ a₀^{3/2}/√(GM) with sign retained (Park eq. 6; `aqual_solar_gate_2026/CONTRACT.md`). a₀ = (c/2)√(Gρ_Λ) is preserved as an optional relation, not a derivation; κ = ½ is fitted.

## What is authenticated (g00_provenance.py)
SHA-256 of every authoritative script and of the two symbolic caches, with the producing source recorded; the three existing regression commands re-run with real exit codes; the f31 / f31b / f31c results re-read from their outputs and reconciled with their prose.

## f31 reconciliation (roadmap G00, fourth item)
f31's numbers: drag piece of α₁ = 4(2−K_B)/(J_Y+1)·[J_Y(ξk)²/(J_Y+1) − 1] for the trace operator (D²φ)² — suppressed at (ξk)² ≈ 1, then growing linearly. f31b: the growth is the χχ stiffening itself, not the background pieces. f31c: coherent stiffening J_Y → J_Y(1+ξ²k²) of the whole Y sector gives exactly −4(2−K_B)/(J_Y(1+ξ²k²)+1) (the screened door as a reference); the covariant Hessian-squared operator fails identically to the trace operator. f31's earlier verdict prose predated its numbers and is replaced (commit of 2026-09-04 night). **Status: k⁴ PPN gate for the aether-scalar host OPEN on the operator; FAIL for (D²φ)² and |D_μD_νφ|²; the operator that realises (A) from an action is not in hand.** These are host-specific diagnostics on an AeST-type action, not PPN values of the T-B action, which has no covariant form yet.

## Stop condition
The target is unambiguous (T-A strict; T-B screened, with its parent T-Q and its own filter convention) and the provenance is reproducible: proceed to G01 and G02.
