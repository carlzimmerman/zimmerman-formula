# THE GENERALIZED COMPLETION — the full relativistic field theory, written out, scored gate by gate

**Status 2026-09-01: a complete relativistic action = THE_COMPLETION v9 (DOI 10.5281/zenodo.21895046)
with the two aether couplings AeST set to zero restored (c₂, c₄). It passes or has certified 9 of the 13
fried-chicken gates on v9's existing record; it owes ONE decisive calculation (gate 4, α₁/α₂ on the
generalized aether locus) and inherits one honest restatement (gate 2). Nothing below is a new
architecture — it is the minimal repair of the one theory that already passes the most.**

## The action

S = ∫d⁴x √−g { (c⁴/16πG)[R − 2Λ]
             − (K_B/2) F_μν F^μν  +  c₂ (∇_μA^μ)²  +  c₄ a_μ a^μ  +  λ (A_μA^μ + 1)
             + 2(2−K_B) a^μ ∇_μφ  −  (2−K_B) Y
             + (a₀²(Q)/8πG) · G( √Y / a₀(Q) )  −  2K(Q)  +  𝒜·B( Y/a₀² ) (Q−Q₀)²  }
  + S_m[ g_μν, ψ ]

with
  F_μν = ∇_μA_ν − ∇_νA_μ,        a^μ = A^ν∇_νA^μ   (aether acceleration; AeST's "J^μ"),
  Q = A^μ∇_μφ,                    Y = (g^{μν} + A^μA^ν) ∇_μφ ∇_νφ   (spatial gradient² of φ in the aether frame),
  G(y) = y² + 2(1+y)e^{−y} − 2    ⇒  dG/dY ∝ 1 − e^{−y},  y = √Y/a₀    (the exact exponential law, spec req 12),
  K(Q) = −M⁴ √( 1 − μ²(Q−Q₀)²/M⁴ )   (pure DBI, β=1 boundary-pinned; −K(Q₀) = ρ_Λ at the de Sitter minimum),
  a₀²(Q) = −κ² c² G · K(Q)          (the promotion: a₀²(Q₀) = κ²c²Gρ_Λ ⇒ a₀ = ½c√(Gρ_Λ) = c²√(Λ/32π) at κ=½),
  B(u) = u/(1+u)²                    (the a₀-bump, cluster sector; 𝒜 ≈ 1.7 Mpc⁻²),
  matter and light minimally coupled to the ONE metric g_μν.

**What is new relative to published v9: only c₂ and c₄.** Everything else is the published action.
GW170817: c_T = 1 EXACTLY regardless of c₂, c₄ (they contain no tensor modes; c₁₃ = K_B − K_B = 0).

## Gate scorecard (spec = FRIED_CHICKEN_SPEC.md)

| # | Gate | Status | Basis |
|---|---|---|---|
| 1 | exact μ=1−e^{−y}, deep-MOND v⁴=GM_b a₀ | **PASS — SOLID** | G(y) kernel; RAR 0.108 dex; BTFR a theorem of the a₀-line |
| 2 | N_grav=2 (+≤1 clock scalar) | **RESTATED (see below)** | 2 tensor + aether (2 spin-1, 1 spin-0) + φ = 6; no-ghost THEOREM at quadratic order (v9); spin-0 health at the repair locus OWED |
| 3 | Φ=Ψ, γ_PPN=1 | **PASS — SOLID** | Φ and Ψ derived independently; lensing 21.2σ→0.60σ; Mistele KiDS 40 kpc–2.2 Mpc |
| 4 | full PPN β,γ,α₁,α₂,α₃ | **γ PASS, α₃=0 PASS (exact), β SAFE (22+ orders); α₁, α₂ = THE OWED CALC** | at c₂=c₄=0: α₁=−2(K_B+2), α₂ ~1e-3 (KILL, V9_PPN_KILL_VERDICT.md). With c₂, c₄ free: NOT-COMPUTED — the decisive swing |
| 5 | ∇_μT^{μν}=0 for baryons | **PASS — by construction** | single metric, minimal S_m ⇒ Bianchi identity; script owed for the record |
| 6 | c_T=c, positive tensor KE | **PASS — SOLID, exact** | c₁₃=0; c₂,c₄ tensor-blind; stage 22 SVT |
| 7 | stability | **no-ghost THEOREM (quadratic) SOLID; aether spin-0 at repair locus OWED; no instantaneous channel iff c₁₄>0 finite** | c_S² = c₂(2−c₁₄)/(c₁₄(2+3c₂)) must be finite & positive; the repair must NOT land at c₁₄=0 |
| 8 | expanding FLRW | **PASS — SOLID** | real CLASS run, Δχ²=1.3 vs cosmic variance; w=−1 at the minimum |
| 9 | controlled y→0 | **PASS (standard AQUAL)** | λ_⊥=μ, λ_∥=1+(y−1)e^{−y} >0 ∀y>0; y=0 is the usual p-Laplacian degenerate point |
| 10 | GR/Newton recovery, G_N derived | **PASS — SOLID** | G_N = (1+J_Y)/J_Y · G̃ derived (wf3); solar system 1e-3457 |
| 11 | one physical metric | **PASS — SOLID** | minimal coupling; no disformal |
| 12 | exponential constitutive law | **PASS** | G(y) is exactly the spec's primitive |
| 13 | a₀ = c²√(Λ/32π) | **INPUT, honestly** | built in via the promotion a₀²(Q₀)=κ²c²Gρ_Λ; κ=½ FITTED; a₀(z)∝H(z) is the framework's prediction, not derived from this action (inverse-K(Q) problem open) |

## Gate 2, restated — not lowered
The universal theorem of 2026-08-31 (YORK_CAUSAL_GATE_VERDICT.md; FRIED_CHICKEN_VERDICT_2026-09-01.md)
proves **{MOND lensing} + {only 2 propagating DOF} + {causal single metric} is unsatisfiable** — every
causal MOND-lensing completion carries a dark field (v9 charge, DW ratio-lock, York instantaneity).
So gate 2 as written contradicts gate 3. The physically correct gate is
  **2′: every degree of freedom is EXPLICIT, COUNTED, and HEALTHY — no hidden scalar graviton, no
  disguised auxiliary, no ghost.**
This theory meets 2′ at quadratic order by theorem. Its dark sector is not a bolt-on: the aether+φ
condensate whose conserved shift-charge carries Ω_dm to the CMB is the SAME field whose minimum gives
w=−1. **The MOND scale and dark energy are one field's two faces — that is why a₀ ∝ c√(Gρ_Λ).**

## The one decisive calculation (launched 2026-09-01)
Generalized-aether PPN: recompute η_K, α₁, α₂ with c₂, c₄ free (c₁ = −c₃ = K_B, c₁₃ = 0), scalar drag
2(2−K_B)a·∇φ included, at the physical deep field J_Y = μ(u₀) = 1, using the FJ-controlled two-gauge
boosted-source pipeline (aest_j10/wf3_*). Pure-EA anchor: α₁ = −4c₁₄, so c₄ = −K_B zeroes it there.
Question: does the drag's K_B-independent piece (the "+2" in η_K) move with c₄, so that a locus
α₁ = α₂ = 0 exists INSIDE the healthy region 0 < c₁₄ < 2 with finite c_S² > 0?
  YES ⇒ this is the full relativistic field theory; remaining owed = spin-0 health at that locus,
        the solar-profile-background check, ∇T=0 script, a₀(z) from the action.
  NO  ⇒ the aether class is dead in full (not just AeST), and the completion is "MOND + dark field"
        through the nonlocal door only.
Either outcome is a result. Neither is faked.
