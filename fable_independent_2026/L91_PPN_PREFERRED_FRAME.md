# L91 — the PPN / preferred-frame gate: F(Q)Θ BEATS the α₁ kill that killed AeST, structurally

`L91_ppn_preferred_frame.py` + `.out` (**17 checks, 17 PASS**; PASS = the printed statement is true).
The decisive gate that killed the predecessor. The v9 AeST completion was **killed 2026-08-31** because
its preferred-frame parameter α₁ = −2(K_B+2) was un-tunable and O(1), violating |α₁| ≲ 1e-4 by ~4 orders.
This lane asks whether astra's integrable-clock F(Q)Θ action passes where AeST failed. It reproduces
astra's structure faithfully (imports nothing from `qwen_claude_field_theory/`; reads no HASH/PREREG).

Astra's action: S = ∫√−g [M²/2 R − ΛM² − K(Q) + F(Q)Θ + M²a₀²G(|V|/a₀)], Θ=∇·n, n_μ=−∂_μT/√(−(∂T)²),
Q=n·∂φ, G(y)=y²+2(1+y)e⁻ʸ−2, affine F=fQ, K=k₂Q²+AQ+B, **k₂=3f²/4M² degeneracy-locked**.

## Controls — the AeST α₁ kill reproduced first, so the gate provably has teeth

- **C1 — the AeST closed form.** α₁ = −4c₁₄ − 4(2−K_B)/(J_Y+1) (from `hunt_2026/f31_ppn_k4_alpha1.py`,
  STANDING.md L45). At the AeST identification c₁₄=K_B this equals the banked −4(2+K_B J_Y)/(1+J_Y)
  **symbolically for all K_B, J_Y**, and at J_Y=1 gives **α₁ = −2(K_B+2)** (memory value). Verified.
- **C2 — un-tunable.** Over the physical box (c₁₄≥0 no spin-1 ghost, K_B∈[0,0.25] BBN, J_Y∈[0.5,2]
  MOND-natural), **min|α₁| = 2.33 ≈ 2×10⁴ over the 1e-4 bound**. α₁=0 forces c₁₄=−(2−K_B)/(J_Y+1) < 0,
  **a spin-1 ghost** (the "lock", f31); L69(iv)'s alternate escape needs c₁₄>2 ⟹ α₁~8. Kill confirmed.
- **C3 — α₃ is NOT where AeST died.** AeST α₃=0 (Lagrangian theory, no prior geometry ⟹ semi-conservative;
  f31 confirms). So the fierce pulsar bound |α₃|≲1e-20 was satisfied by AeST too — **the discriminator is
  α₁**, and that is where the gate's teeth are.

## F(Q)Θ — the five PPN parameters

| param | value | basis | bound | verdict |
|---|---|---|---|---|
| γ | **1** | static no-slip Φ=Ψ (Ψ″−Φ″=0, QUMOND source; L80) | \|γ−1\|≲2e-5 | **PASS** |
| β | **1** | deep-Newtonian: μ=1−e⁻ˣ→1 at 1 AU, 1−μ≈e⁻⁶ᵉ⁷≈0 (both footings) | \|β−1\|≲1e-4 | **PASS** |
| α₃ | **0** | semi-conservative theorem (covariant Lagrangian, no prior geometry) | \|α₃\|≲1e-20 | **PASS** |
| α₁ | residual, **not the AeST killer** | both AeST pieces structurally absent (below) | \|α₁\|≲1e-4 | **CONDITIONAL** |
| α₂ | residual, same structure | AeST's 1e4–1e5× kill does not transfer | \|α₂\|≲1e-7 | **CONDITIONAL** |

- **⭐⭐ THE −4c₁₄ VECTOR PIECE IS STRUCTURALLY ABSENT.** Expanding F(Q)Θ=fQΘ to O(ε²) gives **only the
  cross term f·δQ·δΘ — no (δΘ)² and no (δQ)² from F** (verified in exact sympy). The clock's expansion
  Θ=∇·n enters F(Q)Θ **linearly**, so the clock carries **no bare kinetic term** (no (∇·n)², no aμaᵘ, no
  shear²). It is a constrained, hypersurface-orthogonal khronon (zero vorticity), **not an Einstein-aether
  vector**. The only (δQ)² is the scalar's own time-kinetic term from K(Q), with **k₂=3f²/4M² locked** to
  f by the degeneracy relation (fewer knobs than AeST). No aether sector ⟹ **the −4c₁₄ piece has no analog**.
- **⭐⭐⭐ THE −4(2−K_B)/(J_Y+1) DRAG PIECE IS ABSENT — the SAME feature that escaped the deep-MOND kill.**
  The AeST drag is the α₁ face of the coupling **C[n,φ]=2−K_B**, which L69 identified as the deep-MOND
  killer: a **separate MOND scalar coupled to the clock's acceleration through the lapse** (hypothesis H2).
  The integrable clock **violates H2 — MOND lives inside the clock, no separately-lapse-coupled scalar** —
  so C[n,φ]=0 and the drag piece **→ 0** (verified). This is the exact structural feature by which L66/L69
  found the action escapes the deep-MOND instability; here it is shown to **remove the α₁ drag piece too**.
- **⭐ THE RESIDUAL α₁ IS GENERICALLY NEGLIGIBLE, THE OPPOSITE OF AeST's O(1).** With both AeST pieces gone,
  the residual preferred-frame response comes only from the clock-scalar braid **f·Q₀·δΘ** at the local
  cosmological clock rate Q₀. Dimensionally **α₁ ~ f Q₀/M² ~ H₀/M ~ 1e-61** for natural f (M sets G=1/8πM²).
  Driving it to O(1) needs a **fine-tuned enormous f ~ M²/Q₀ ~ M_Pl²/H₀ (~1e61)** — *not* forced by a₀
  (a₀ lives in the separate M²a₀²G term) nor by the dust. This is a tuning **away** from the natural value,
  unlike AeST where O(1) was forced.

## Verdict — NOT A KILL; CONDITIONAL PASS (leans PASS)

- **It beats AeST, structurally, not by tuning.** AeST's α₁=−2(K_B+2) was O(1) and un-tunable because
  **both** its pieces are forced (the vector-kinetic −4c₁₄ and the separate-scalar-through-the-lapse drag).
  **F(Q)Θ has neither sector.** So the O(1) un-tunable kill is gone. **Confidence HIGH** — this is
  structural and matches the repo's own L66/L69 mechanism from the other side.
- **γ=1, β=1, α₃=0 pass outright.** The fierce pulsar bound |α₃|≲1e-20 is satisfied **structurally** (it was
  never the discriminator — AeST died on α₁, not α₃).
- **α₁, α₂ are strictly CONDITIONAL.** They are *not* the AeST killers and are generically ~1e-61, but the
  **exact O(w) coefficient needs astra's quasi-static local Q₀ calibration + the O(w) braid solve**, which
  astra has done only cosmologically. **PASS CONDITION: |f Q₀/M²| ≲ 1e-4** (natural f gives ~1e-61; violated
  only by fine-tuning f up ~1e57 over the natural value). **Confidence MODERATE-HIGH** they pass; strictly
  UNDECIDED in exact magnitude.
- **Scope, stated plainly.** This lane establishes γ, β, α₃ and the structural *absence* of both AeST α₁
  pieces from astra's exact action. It does **not** compute the exact residual α₁/α₂ — that is astra's
  uncomputed local-Q₀ calibration and the boosted O(w) weak-field solve (the same computation astra names
  as "the omitted full khronon/aether and PPN sectors" in the REPORT). κ=½ stays fitted; nothing here
  favours any framework over ΛCDM.

Both a₀ footings carried where dimensional (canonical 9.36e-11, alternate 1.13e-10 m/s²); a₀ enters only
the deep-Newtonian β check, and both give 1−μ ≈ e⁻⁶ᵉ⁷ ≈ 0 at 1 AU.
