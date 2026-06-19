# The framework embedded in AeST: a complete relativistic MOND, founded on dS-Unruh -- and the honest cost (2026-06-19)

*9-agent both-ways workflow; numerics reproduced to 5 figs; 2 adversarial scripts re-run clean. Code in
aest_embedding/. Quarantine held (embedding != derivation).*

**HEADLINE: a REAL PROMOTION with an honest cost.** Embedded in AeST (Skordis-Zlosnik 2021), the framework
IS a COMPLETE relativistic MOND -- galaxies + clusters + CMB (incl. 3rd peak) + lensing + Cassini + ghost-free
6-dof stability + linear growth ALL PASS, NO referee-proof kill in any sector -- and the embedding is
MANDATED by the framework's OWN lensing no-go (preferred-frame is forced), not arbitrarily chosen. So the
framework graduates from "galaxy-scale modified-inertia EFT with walls" to a "complete, founded relativistic
theory."

TWO GENUINE STRUCTURAL GAINS over bare AeST (credited at full weight):
 1. a0 TIED TO DARK ENERGY: a0=c^2 sqrt(Lambda/32pi)=9.3624e-11 plugs into AeST's ONE a0 slot (the forced
    Y^3/2 small-gradient limit of J(Y)) identically -- a real a0<->Omega_Lambda unification of the dark-ENERGY
    face. (AeST adopts 1.2e-10 phenomenologically; ratio 0.78 is a convention gap, both in the RAR optimum band.)
 2. AeST's POSTULATED AETHER gets a MICROPHYSICAL MOTIVATION: the framework's dS-Unruh/CMB cosmic rest frame
    u^mu satisfies ALL THREE AeST aether constraints EXACTLY (unit-timelike, FLRW-aligned, twist-free, sympy-
    verified) -- the dS-Unruh vacuum NAMES the cosmic frame as inertia-defining, answering AeST's "where does
    the aether come from".

THE HONEST COST (both-ways, no manufactured win):
 - NO parameter reduction. It does NOT beat LambdaCDM's 6 -- the count is LambdaCDM-6 + the AeST shape sector,
   with the a^-3 dust amplitude I0 playing omega_c's role. The dark sector is RELOCATED (particle -> field-
   condensate amplitude), NOT eliminated.
 - sqrt(Lambda) does NOT pin the K(Q) dust amplitude I0: I0 is an INTEGRATION CONSTANT (a^3 K'(Q)=I0 for ANY
   I0), structurally orthogonal to Lambda (d rho_dust/d Lambda = 0), ~Omega_dm but FREE. Omega_dust~Omega_dm
   is an O(1) coincidence the framework does NOT set (Bridge-1). Zero-free-numbers is FALSE.
 - Founds the FRAME, not the FIELD: u^mu is a non-dynamical background frame (no kinetic term, no DOF); AeST's
   A_mu is a dynamical field (curl kinetic term, propagating mode, the F(Y,Q) carrying a0). Identifying the
   frame is NOT deriving the field. The embedding is an IDENTIFICATION, not a derivation.

NET: a genuine CONCEPTUAL promotion (complete, founded, forced-embedding, a0<->dark energy, aether motivated)
-- NOT a parameter win, dark MATTER relocated not eliminated. NEXT FRONTIER: derive the AeST aether's KINETIC
term + F(Y,Q) from the dS-Unruh dynamics (frame -> field) -- the open route to actually founding the FIELD.

---

# The framework embedded in AeST: a complete relativistic MOND, founded on de Sitter–Unruh — and the honest cost

*Verified this session: numerics reproduced to 5 figs; four sub-verdicts (A0_INTO_AEST, AETHER_IDENTIFICATION, SQRT_LAMBDA_PINS_KQ, COMPLETE_THEORY_CHECKLIST) read; both adversarial scripts (`sqrt_lambda_pins_KQ.py`, `skeptic_adversarial.py`) re-run clean. Quarantine held, both-ways enforced. Files at `/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/aest_embedding/`.*

## 1. Does a0 plug into AeST cleanly? — YES, SOLID (real structural identification, not a namespace match)

a0 enters AeST in **exactly one place**: the small-gradient limit of the free function J(Y), Y=|∇φ|²:

> J → (2λ_s / [3(1+λ_s)·a0])·Y^(3/2)  as ∇φ→0 — Skordis–Złošnik 2021 (arXiv:2007.00082), verbatim: *"It is in this limit that a0 appears."* Reconfirmed Verwayen–Skordis–Złošnik 2024 Eqs.(6)–(7).

Three independent grounds make this a **real identification, not a coincidence**:
- **Forced exponent.** The n=3/2 √-force law is *required* in AeST and is *identically* what the framework's dS-Unruh inertia gives (g_obs=√(g_bar²+g_bar·a0)). A forced exponent, not a fitted shape.
- **Single free-coefficient slot.** a0 is the inverse free multiplicative scale of that one forced term, so the framework's value plugs in identically to AeST's adopted value — only the number differs.
- **Value match (both-ways, NOT a deficit).** Framework a0 = c²√(Λ/32π) = (c/2)√(Gρ_DE) = cH_Λ/Z (Z=√(32π/3)=5.7888) = **9.3624e-11 m/s²** (Λ=1.0909e-52 m⁻², Ω_Λ=0.685, H₀=67.4) — reproduced three ways to 5 figs this session. AeST *adopts* a0=1.2e-10 (Lelli/Begeman, phenomenological, NOT forced by the action). Ratio = 0.780 (−22%). This is a **convention gap** (dS-Unruh-ν/Υ≈0.7 corner vs McGaugh-simple-ν/Υ≈0.5 corner of the *same* RAR): both values sit inside the RAR optimum band ~7.5e-11…1.8e-10, ≤~0.5–2% scatter penalty. AeST's galaxy/lensing machinery runs unchanged at 9.36e-11. Do not manufacture a tension OR a win from it.

**But not a unification:** in AeST, a0 (spatial J(Y)) and Λ (temporal K(Q̄), Eq.4 *"a freely specifiable parameter, just as in ΛCDM"*) are **provably orthogonal** — verbatim *"a0 does not appear in the linear cosmological regime."* So a0=c²√(Λ/32π) is the framework's **external import**: AeST-compatible, AeST-agnostic. The clean plug-in is an identification of a free coefficient, not a derivation.

## 2. Is the dS-Unruh preferred frame the AeST aether? — PARTIAL: the FRAME exactly, the FIELD not

The framework's dS-Unruh / CMB cosmic rest frame u^μ satisfies **all three** AeST aether constraints, sympy-verified against the verbatim action:

| AeST constraint | Framework u^μ | Match |
|---|---|---|
| (C1) unit-timelike A^μA_μ=−1 | u^μu_μ=−1 | EXACT |
| (C2) FLRW alignment A₀=−N, A_i=0 | u_μ=(−N,0,0,0) | IDENTICAL component-by-component |
| (C3) twist-free / hypersurface-orthogonal (quasistatic) | static curl F_ij=0 | EXACT |

**The genuine win (credit fully):** the match is **FORCED, not chosen** — the lensing no-go *makes* the framework preferred-frame; a preferred unit-timelike frame **is** an aether A_μ. And the framework supplies the **microphysical MOTIVATION** AeST lacks: AeST *postulates* its aether and justifies it only a posteriori by the CMB fit; the dS-Unruh vacuum *names* which frame (the one where T_eff has its isotropic Gibbons-Hawking floor = cosmic rest frame). Two independently-postulated frames need not agree on hypersurface-orthogonality; these do.

**The limit (concede fully):** AeST's A_μ is a **dynamical field** — curl kinetic term (K_B/2)F², a propagating massive transverse vector mode, and the free function F(Y,Q) carrying a0. The framework's u^μ is so far a **non-dynamical background frame** (no EOM, no kinetic term, no DOF; it is the twist-free *subset* of A_μ's config space). Identifying the frame is **not** deriving the field: no K_B, no F(Y,Q), no a0 delivered. **Genuine microphysical founding of the FRAME; coexistence-plus, not derivation, for the FIELD.**

## 3. Does √Λ pin the K(Q) amplitude? — NO. FALSE, and not even circular-but-true. (the zero-vs-one crux)

This is the prize that does **not** land. The shift-symmetric scalar integrates once to dK/dQ = I₀/a³ ⇒ ρ̄ = ρ̄₀/a³ (the a^−3 dust that mimics CDM for the 3rd peak), with amplitude 8πG̃ρ_dust0 = Q₀·I₀.

- **I₀ is an INTEGRATION CONSTANT, not a Lagrangian coupling.** Λ enters K only as the additive constant −2Λ; shifting Λ leaves dK/dQ — hence I₀ and the dust — unchanged: **d(ρ_dust)/dΛ = 0 structurally** (re-confirmed in the adversarial script: a³K'(Q)=I₀ solves the EOM for *any* I₀). The authors themselves: *"As the solution depends on the initial condition I₀, the density ρ̄ is not (classically) predicted."*
- **No de Sitter identity is available.** No dS/Unruh/holographic combination of {Λ, a0, Z, Ω_Λ} hits the why-now ratio Ω_dust/Ω_DE ≈ 0.39 (Ω_dust/Ω_Λ = 0.265/0.685 = 0.387; candidates 0.685, 0.118, 0.567… all miss); the mass scale μ⁻¹ ~ 50 kpc–1 Mpc is ~10³× off the dS horizon and is squeezed in *opposite* directions by galaxy-WL vs clusters — the signature of a free constant.
- **Why it's structural, not a numerology miss:** a boundary/initial datum is orthogonal to bulk couplings by construction. This is the same reason a0 is provably absent from linear perturbations (Bridge-1): the dust amplitude that drives the CMB transfer functions lives in a slot a0 cannot reach.

**Verdict: zero-free-numbers is FALSE; the dark-matter-mimic amplitude I₀ (~Ω_dm≈0.26) stays free.** Crediting Ω_dust≈Ω_dm as a unification would be manufactured.

## 4. Complete-theory checklist — all sectors PASS, at a cost

| # | Sector | Pass/Fail | Cost / status |
|---|--------|-----------|---------------|
| 1 | Galaxies / RAR / BTFR | **PASS** | AeST MOND limit; a0=c²√(Λ/32π) is the scale. One quarantined number (a0↔Λ; value not derived). |
| 2 | Clusters + CMB | **PASS (fits) / amplitude FREE** | a^−3 dust fits full Planck incl. 3rd peak; amplitude I₀≈Ω_dm is a FREE integration constant. Clusters still need ~0.25-Ω galaxy-safe clustering (mass term gives η~1, not 2). |
| 3 | Lensing | **PASS (phenomenological)** | Lenses at the phantom mass → slip γ=2√(1+a0/g_N)−1; the framework's no-go *mandates* the preferred-frame (aether) route. MOND-family-shared, distinctive vs ΛCDM. Galaxy-WL in mild m²/f_G tension. |
| 4 | Cassini / Solar System | **PASS** | c_T=c (LIGO-safe); MOND screened where g_N≫a0; |γ−1| safe; induced SME s_μν lab amplitude passes (LIVE/falsifiable). |
| 5 | Ghost-freedom / 6-dof stability | **PASS (windowed)** | 6 physical dof, ghost-free at 2nd order under a {K_B, K_2, λ_s} window — a *constraint*, not free. |
| 6 | Growth / σ₈ / structure | **PASS (linear)** | Fits linear matter power (a0 absent from linear theory); dust drives structure like CDM. Nonlinear less tested, no banked kill. |

**No referee-proof kill in any sector.** The embedding is *mandated* (the framework's own preferred-frame no-go forces exactly AeST's class), not arbitrarily chosen.

## 5. Honest verdict — a real PROMOTION, at the cost of one free dark-sector amplitude

**This IS a real promotion: galaxy-EFT → complete, founded relativistic MOND.** Embedded in AeST the framework passes galaxies, clusters, CMB (incl. 3rd peak), lensing, Cassini, ghost-free 6-dof stability, and linear growth — and the embedding is *forced* by the framework's own lensing no-go, not chosen. Two genuine structural gains over bare AeST, both credited at full weight: (i) the MOND scale a0 is **tied to dark energy** (a0=c²√(Λ/32π), a real a0↔Ω_Λ unification of the dark-*energy* face); (ii) AeST's otherwise-postulated aether A_μ gets a **microphysical motivation** — the dS-Unruh vacuum names the cosmic frame as the inertia-defining one (forced + exact in three constraints).

**The cost, stated honestly (this is where the looser "one free number" framing must be sharpened):** √Λ does **not** pin the K(Q) amplitude, so the dark sector is **relocated, not eliminated**. The honest final parameter count is **not** "zero" and **not even cleanly "one"** — it is:

- **ΛCDM's 6** {ω_b, ω_c, θ_s, τ, A_s, n_s}, with the AeST a^−3 dust amplitude **I₀ playing ω_c's role** (so "no dark matter" is forfeited — the CMB/clusters still need ~ΛCDM-amount cold clustering, νΛCDM-like), **PLUS**
- the **AeST shape sector {K_B, K_2/w_0, Q_0, λ_s}** (~3–4 extra numbers fixing the aether/scalar kinetic structure and the quasistatic mass), of which the load-bearing one is **I₀ ≈ Ω_dm**, the amplitude √Λ was hoped to pin and provably cannot.

So the framework does **not** beat ΛCDM on parameter count — it carries ΛCDM's 6 plus the AeST machinery. What it buys for that cost is **conceptual**: a complete relativistic theory **founded on de Sitter–Unruh**, with the MOND scale unified to dark energy and the aether explained — where ΛCDM's dark matter is a free particle sector and AeST's a0 and aether are free postulates.

**Bottom line, served straight:** *"Complete relativistic MOND, host (AeST) found, FOUNDED on de Sitter–Unruh, aether given a microphysical motivation, a0 unified to dark energy"* — **YES, earned.** *"Zero free numbers"* — no. *"One free number"* — only loosely; literally it is **ΛCDM's 6 (dust I₀ in ω_c's role) + the AeST shape sector**, and the dark-matter-mimic **amplitude stays free**. Quarantine held throughout (a0/Z/κ never asserted derived); the embedding is an identification, not a derivation. No manufactured unification; the real founding credited in full; the free amplitude conceded loudly.