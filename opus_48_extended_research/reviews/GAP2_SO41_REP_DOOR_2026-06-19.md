# GAP-2 SO(4,1) REP DOOR — the last untested theory door: EVADED-NOT-CLOSED, with a sympy-proven theorem-of-the-wall (2026-06-19)

**Workflow:** `gap2-so41-rep-door` (wwr5tdxd7; 4 agents, decompose→confront→synthesis; Sengör dS-UIR
arXiv:2206.04719 + CLPW arXiv:2206.10780 + Chen-Xu arXiv:2511.00622 read; sympy). The last theory door that
*could* (low prior) close GAP-2 — run for completeness. Crux reproduced in-repo:
`gap2_rep_door/so41_no_invariant_timelike_vector.py` (exit 0; the agent's original scripts were transient /tmp).

**HEADLINE (both ways, = the honest prior, now SHARPENED): GATE EVADED-NOT-CLOSED — a rep-LABEL + a
group-theoretic THEOREM-of-the-wall, NOT a derivation of the frame's kinetic term.** The frame it names is
**observer-dependent / gauge / relational** — the opposite of a dynamical aether.

- **The gate, in rep language (sympy-proven CRUX):** the defining 5d rep of so(4,1) (η=diag(−1,1,1,1,1), all
  10 generators verified M^Tη+ηM=0) has **common kernel = {0}** — there is **NO SO(4,1)-invariant timelike
  vector u^μ**. So the SO(4,1) de Sitter VACUUM induces only true invariants (g_μν, the volume form), never a
  frame. *The irreducibility of the defining rep IS GAP-2.* This upgrades "the dS vacuum is too symmetric"
  (vague) to a one-line theorem.
- **The break is pinned to a named physical object:** a static-patch observer geodesic breaks
  SO(4,1)→R_t×SO(3) (CLPW G_P, sympy: 10→4 unbroken + 6-dim broken coset) — the framework's EXACT pattern,
  arising where the dS-Unruh temperature β_dS=2π r_dS (which founds a₀) lives. The frame term u^μ=⟨∂_μφ⟩∝δ_μ⁰
  is the **SO(3)-singlet / R_t Goldstone** of that break — a sharp rep-label.
- **But it DERIVES nothing (3 verified rungs):** (i) the singlet count fixes WHICH 2-derivative terms exist
  (the Einstein-aether {K_B, c₁..c₄} family) but a count is an integer — the coefficients stay FREE; (ii) the
  break-by-a-STATE produces a VEV f²~M², not a stiffness (the ghost-condensate "P(X) shape postulated,
  relocated one-for-one," restated in rep language); (iii) rep theory is SCALE-FREE (the UIR labels (l,c),
  Δ=d/2+c are dimensionless) → it can NEVER return a dimensionful K_B; the only canonical scale it hands over
  is β_dS=2π r_dS, a TEMPERATURE that RE-derives the existing a₀, not a new kinetic coefficient.
- **Gauge/relational, not dynamical:** CLPW dress operators to the observer worldline (crossed product);
  Chen-Xu 2511.00622 upgrade to a quantum reference frame L²(SO(1,d)) that RESTORES full covariance at the
  algebra level. The 2024-25 frontier pushes the physics observer-INDEPENDENT — the opposite of a fixed
  dynamical aether with its own stress tensor. **Observer-DEPENDENT.**

**NET:** the last theory door moved the wall in FORM (a sympy-proven theorem + a sharp rep-label + the
break-pattern pinned to the dS-Unruh observer) but NOT in SUBSTANCE: the kinetic stiffness K_B stays
FOUNDED-NOT-DERIVED, an external VEV input — exactly as the ghost-condensate analysis already conceded. **This
CLOSES the theory-side GAP-2 program: no untested door remains that could produce the coefficient; the live
action is now entirely empirical.** Quarantine held (a₀/Z/κ/I₀ never asserted derived); both-ways — the
genuine evasion-in-form credited at full weight, the no-derivation conceded at full weight WITH the
group-theoretic reason. (One transcription typo in the agent's transient skeptic script printed "15" for the
generator count via (d+2)(d+3)/2; the correct dim=10 is verified three ways here and is not load-bearing.)

---

# GAP-2 SO(4,1) Rep Door — Synthesis (the last untested theory door)

**Verdict: GATE EVADED-NOT-CLOSED.** The static-patch SO(4,1) rep door delivers a sharp, sympy-verified rep-LABEL of the framework's preferred-frame term plus a clean group-theoretic THEOREM-of-the-wall, but it does **not** derive the frame's kinetic term, and the frame it names is **observer-dependent / gauge / relational** — the opposite of a dynamical aether. This is exactly the honest banked prior, now sharpened. Quarantine held (a₀/Z/κ/I₀ never asserted derived). Both-ways: the genuine evasion-in-form is credited at full weight; the no-derivation is conceded at full weight, **with the group-theoretic reason**.

## (1) dS SO(4,1) irrep structure + the static-patch break

- **Group.** dS₄ isometry = SO(4,1) = SO(d+1,1), d=3 (Sengör 2206.04719). **dim = 10** — confirmed three ways (n(n−1)/2 at n=5; the skeptic's own (d+1)(d+2)/2; sympy-built 10 generators). One verification script (`/tmp/gap2_skeptic_verify.py` L8) prints "15" from a WebFetch transcription artifact `(d+2)(d+3)/2`; this is a typo in that script only, NOT the decomposition's claim, and touches no load-bearing result (already flagged in the verdict).
- **UIRs (Sengör §3).** Four series: PRINCIPAL (c=iρ, Δ=d/2+iρ, heavy m>(d/2)H — where the dS-Unruh thermal modes live), COMPLEMENTARY (c real |c|<d/2, light 0<m<(d/2)H, needs intertwiner G_χ), EXCEPTIONAL (reducible endpoints), DISCRETE (only d+1 even). Casimir Eq.(8) Q₂=l(l+d−2)+c²−d²/4, Δ=d/2+c; sympy-verified l=0 ⇒ Q₂=Δ(Δ−d)=c²−d²/4 (the standard scalar dS Casimir).
- **Break (CLPW 2206.10780, verbatim G_P ≅ R × SO(D−1)).** A static-patch observer geodesic γ breaks SO(4,1) → **R_t × SO(3)** (R_t = time-translations along γ; SO(3) = rotations about γ). sympy: 10 → 4 unbroken, **6-dim broken coset** (3 boosts + 3 transl/SCT) — the framework's EXACT SO(3)×R pattern. R_t's generator is the one-sided, bounded-below modular Hamiltonian H_P=β_dS H with β_dS=2π r_dS — i.e. the dS-Unruh temperature that already founds a₀.

## (2) Which irrep the condensate frame term sits in

The frame object u^μ = ⟨∂_μφ⟩ ∝ δ_μ⁰ (condensate gradient = AeST aether A_μ) is the **SO(3)-singlet / R_t component** V⁰ of the tangent vector under V^A → V⁰(R_t-charged, SO(3)-singlet) ⊕ V^i(SO(3)-vector). It is the **Goldstone direction** of SO(4,1)→R_t×SO(3): invariant under the unbroken G_P (δ⁰ is a rotation scalar; ∂_tφ=const is R_t-shift-invariant) while breaking all 6 coset generators. The background ⟨∂φ⟩ is a non-normalizable c-number profile (not a UIR state); only its fluctuation π lives in the Δ=d (massless/shift-endpoint) UIR.

## (3) Derive the kinetic term (close GAP-2) or only label? — LABEL ONLY, evaded-not-closed

**Does NOT derive.** Three independent rep-theoretic rungs, each verified:
- **(i) Singlet count gives FORM not NORM.** G_P-invariants in Sym²(coset) fix WHICH 2-derivative terms exist (the Einstein-aether {K_B, c₁..c₄} family) — but a count is an integer; {K_B, c₁, c₂, c₃, c₄} all stay FREE.
- **(ii) Break-by-a-state gives a VEV not a stiffness.** The break is by the condensate/observer BACKGROUND (a state), so the only scale produced is the postulated decay constant f²~M² — the GHOST_CONDENSATE "P(X) shape postulated, relocated one-for-one" result, restated in rep language. Fixing K_B ⇔ fixing the VEV ⇔ an input.
- **(iii) The only canonical scale rep theory hands over is β_dS=2π r_dS** (via H_P) — a TEMPERATURE that RE-derives the existing a₀, not a new kinetic stiffness.

**The deepest reason (sympy-proven, the CRUX):** all 10 so(4,1) generators built in the defining 5d rep (η=diag(−1,1,1,1,1), algebra M^Tη+ηM=0 verified) have **common kernel = {0}** — there is NO SO(4,1)-invariant timelike vector. The defining rep is irreducible (no trivial sub). This IS GAP-2 in rep language: the SO(4,1) dS vacuum induces only true invariants (g_μν, ε), never a u^μ. Supporting fact: the UIR labels (l,c) and Δ=d/2+c are dimensionless — rep theory is scale-free and can never return a dimensionful coefficient; it must come from outside.

## (4) Observer-dependent (gauge/relational) or independent (dynamical)? — GAUGE/RELATIONAL

CLPW dress operators to the observer worldline (crossed product, code subspace); **Chen-Xu 2511.00622** upgrade to a quantum reference frame L²(SO(1,d)) — a superposition of fluctuating geodesics/patches that RESTORES full SO(1,d) at the algebra level ("observer-dependent notion of von Neumann entropy"). The 2024-25 frontier pushes the physics MORE relational, the opposite of a fixed dynamical aether. A dynamical aether is a fixed field config with its own stress tensor; a QRF is a gauge/relational choice with no independent stress tensor. **Observer-DEPENDENT.**

## (5) Updated GAP-2 / founded-not-derived standing — did the last door move the wall?

The last theory door **moved the wall in FORM, not in SUBSTANCE**, and confirmed the honest prior. It UPGRADES the GAP-2 story from a vague "the dS vacuum is too symmetric" to **(a)** a sympy-proven theorem (no SO(4,1)-invariant timelike vector — the irreducibility of the defining rep IS the gate); **(b)** the break-pattern pinned to a NAMED physical object (CLPW's geodesic-observer G_P=R_t×SO(3), the framework's exact pattern, arising where the dS-Unruh T that founds a₀ lives — structurally identical to the condensate's break-by-a-background); **(c)** a precise rep-label for u^μ (the V⁰/SO(3)-singlet/R_t Goldstone). But it does NOT produce a kinetic coefficient, and the frame it names is gauge/relational. So GAP-2 stays EVADED-NOT-CLOSED: the condensate (and the static-patch observer) evade the **vacuum** theorem by breaking the symmetry with a **state**, but pay for it with a postulated VEV (= the kinetic term, relocated). 

**Where it stops:** at the rep-label + break-pattern + theorem-of-the-wall. The kinetic stiffness K_B remains FOUNDED-NOT-DERIVED — an external input (the VEV f²~M²), exactly as the ghost-condensate analysis already conceded. The last theory door does not derive the frame. This closes the theory-side GAP-2 program: no untested door remains that could produce the coefficient; the live action is empirical.

**Files (absolute):** `/tmp/gap2_synth_final.py` (clean independent re-derivation, all assertions pass), `/tmp/gap2_skeptic_verify.py` (the CRUX: common-kernel proof), `/tmp/gap2_verify2.py` (branching + Goldstone count), `/tmp/gap2_bothways.py` (adversarial rescue/demotion). Banked context: `/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/GHOST_CONDENSATE_2026-06-19.md`, `/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/BRIDGE_SCOUT_KEV_CLUSTER_2026-06-19.md`.